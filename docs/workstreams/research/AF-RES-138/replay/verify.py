"""Independently recompute slots, transitions, and denominators from the frozen CSVs."""

import argparse
import csv
import json
from collections import Counter
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
POLICIES = ("B", "C", "Gate", "Conditional")
STAGES = {"investigation": 8, "display": 3}
LOCATIONS = {"ranks.csv": "ranks.csv", "transitions.csv": "transitions.csv",
             "slots.csv": "evidence/slots.csv", "editor-cost.csv": "evidence/editor-cost.csv",
             "alias-audit.csv": "evidence/alias-audit.csv"}


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_jsonl(path):
    return [json.loads(row) for row in path.read_text(encoding="utf-8").splitlines()]


def count_frame(frame):
    summary = {}
    purpose = {r["issue_id"] for r in frame if r["layer"] == "purpose" and r["issue_id"]}
    neutral = {r["issue_id"] for r in frame if r["layer"] == "neutral" and r["issue_id"]}
    for layer in ("purpose", "neutral"):
        rows = [r for r in frame if r["layer"] == layer]
        returned = [r for r in rows if r["slot_status"] == "returned"]
        unique = {r["issue_id"]: r for r in returned}
        summary[layer] = {
            "planned": len(rows), "returned": len(returned), "unique_issues": len(unique),
            "unique_bodies_opened": sum(r["opening_access"] == "opening" for r in unique.values()),
            "unique_authors": len({r["author_key"] for r in unique.values() if r["author_key"]}),
            "issues_without_author": sum(not r["author_key"] for r in unique.values()),
            "same_issue_duplicate_slots": sum(r["selection"] == "duplicate" for r in returned),
            "lineage_duplicate_issues": sum(bool(r["body_lineage_of"]) for r in unique.values()),
            "previously_opened_issues": sum(bool(r["prior_id"]) for r in unique.values()),
            "query_surface_slots": sum(r["query_surface"] == "true" for r in returned),
            "target_form_unique_issues": sum(bool(r["four_target_forms"]) for r in unique.values()),
            "slot_decisions": dict(Counter(r["selection"] for r in rows)),
        }
    summary["cross_layer"] = {"shared_issues": len(purpose & neutral), "neutral_only_issues": len(neutral - purpose),
                              "purpose_after_overlap_exclusion": len(purpose - neutral)}
    return summary


def independent_orders(rid, scores, display, allow_conditional):
    positive = [fid for fid, score in sorted(scores.items(), key=lambda pair: (-pair[1], pair[0])) if score > 0]
    investigation = positive[:8]
    shown = investigation[:3]
    candidate = None
    if display is not None:
        shown = [fid for fid in investigation if display[rid, fid]["gate"] == "pass"][:3]
        if allow_conditional and len(shown) < 3:
            candidate = next((fid for fid in investigation
                              if fid not in shown and display[rid, fid]["conditional_eligible"] == "yes"), None)
            if candidate:
                shown.append(candidate)
    return investigation, shown, candidate


def recompute(path, replay=None):
    if replay:
        for regenerated, committed in LOCATIONS.items():
            assert (replay / regenerated).read_bytes() == (path / committed).read_bytes(), regenerated
    frame = read_csv(path / "frame.csv")
    requests = {r["request_id"]: r for r in read_jsonl(path / "requests.jsonl")}
    cards = {r["feature_id"]: r for r in read_csv(path / "evidence/card-clauses.csv")}
    assert len(frame) == 120 and len(cards) == 16
    picks = {r["selected_request_id"]: r for r in frame if r["selection"] == "selected"}
    assert set(picks) == set(requests)
    assert len({row["author_key"] for row in picks.values()}) == len(requests)

    pair_keys = set(product(requests, cards))
    judgments = []
    for file in ("display.csv", "truth.csv"):
        data = read_csv(path / file)
        pairs = {(r["request_id"], r["feature_id"]): r for r in data}
        assert set(pairs) == pair_keys and len(data) == len(pair_keys)
        judgments.append(pairs)
    display, truth = judgments
    sources = read_jsonl(path / "sources.jsonl")
    source_by_id = {s["source_id"]: s for s in sources}
    assert len(source_by_id) == len(sources)
    for (rid, fid), row in display.items():
        assert row["request_source_id"] in source_by_id
        assert row["card_source_id"] in source_by_id
        assert set(row["request_spans"].split("|")) <= {s["span_id"] for s in requests[rid]["spans"]}
        standard = truth[rid, fid]
        assert standard["supporting_source"] in source_by_id
        assert set(standard["request_spans"].split("|")) <= {s["span_id"] for s in requests[rid]["spans"]}

    ranks = read_csv(path / "ranks.csv")
    rank_by_key = {(r["request_id"], r["policy"], r["feature_id"]): r for r in ranks}
    assert len(ranks) == len(rank_by_key) == len(requests) * len(POLICIES) * len(cards)
    all_slots = read_csv(path / "evidence/slots.csv")
    slot_by_key = {(s["request_id"], s["policy"], s["stage"], int(s["position"])): s for s in all_slots}
    assert len(all_slots) == len(slot_by_key) == len(requests) * len(POLICIES) * sum(STAGES.values())
    order = {}
    for rid, policy in product(requests, POLICIES):
        rows = {fid: rank_by_key[rid, policy, fid] for fid in cards}
        scores = {fid: int(row["score"]) for fid, row in rows.items()}
        if policy in ("Gate", "Conditional"):
            assert scores == {fid: int(rank_by_key[rid, "C", fid]["score"]) for fid in cards}
        investigate, show, conditional = independent_orders(
            rid, scores, display if policy in ("Gate", "Conditional") else None,
            policy == "Conditional",
        )
        for stage, expected in (("investigation", investigate), ("display", show)):
            rank_field = stage + "_rank"
            actual = [fid for fid in sorted(rows, key=lambda k: int(rows[k][rank_field] or 999))
                      if rows[fid][rank_field]]
            assert actual == expected, (rid, policy, stage)
            order[rid, policy, stage] = expected
            for i in range(1, STAGES[stage] + 1):
                seat = slot_by_key[rid, policy, stage, i]
                fid = expected[i - 1] if i <= len(expected) else ""
                assert seat["feature_id"] == fid
                assert (seat["vacancy"] == "True") == (not fid)
                assert (seat["visibility"] == "conditional") == (stage == "display" and bool(fid) and fid == conditional)
                assert seat["grade"] == (truth[rid, fid]["grade"] if fid and seat["visibility"] != "conditional" else "")
        if policy == "Conditional":
            gate = order[rid, "Gate", "display"]
            assert show[:len(gate)] == gate and len(show) - len(gate) in (0, 1)

    data = read_csv(path / "transitions.csv")
    transitions = {(t["request_id"], t["from"], t["to"], t["stage"], t["feature_id"]): t for t in data}
    assert len(data) == len(transitions) == len(requests) * 3 * 2 * 16
    for rid, before, after, stage in ((rid, p, q, stage)
            for rid in requests for p, q in zip(POLICIES[:-1], POLICIES[1:], strict=True) for stage in STAGES):
        old = {fid: i for i, fid in enumerate(order[rid, before, stage], 1)}
        new = {fid: i for i, fid in enumerate(order[rid, after, stage], 1)}
        entered = set(new) - set(old)
        removed = set(old) - set(new)
        shared = set(old) & set(new)
        expected = dict.fromkeys(entered, "entered") | dict.fromkeys(removed, "left")
        expected.update({fid: {-1: "down", 0: "same", 1: "up"}[(old[fid] > new[fid]) - (old[fid] < new[fid])]
                         for fid in shared})
        for fid in cards:
            t = transitions[rid, before, after, stage, fid]
            assert t["change"] == expected.get(fid, "outside")
            assert t["old_position"] == str(old.get(fid, "")) and t["new_position"] == str(new.get(fid, ""))

    costs = read_csv(path / "evidence/editor-cost.csv")
    aliases = read_csv(path / "evidence/alias-audit.csv")
    groups = {"combined": set(requests)}
    groups.update({layer: {rid for rid in requests if requests[rid]["layer"] == layer} for layer in ("purpose", "neutral")})
    totals = {}
    for name, ids in groups.items():
        metrics = {"requests": len(ids), "authors": len({requests[rid]["author_key"] for rid in ids}),
                   "pairs": len(ids) * len(cards), "truth": dict(Counter(truth[rid, fid]["grade"]
                   for rid, fid in pair_keys if rid in ids)), "policy": {}, "transitions": {}}
        for policy in POLICIES:
            seats = [s for s in all_slots if s["policy"] == policy and s["request_id"] in ids]
            stats = {stage: {"visibility": dict(Counter(s["visibility"] for s in seats if s["stage"] == stage)),
                             "grades": dict(Counter(s["grade"] or "ungraded" for s in seats if s["stage"] == stage))}
                     for stage in STAGES}
            stats["ranks"] = dict(Counter(r["reason"] for r in ranks if r["policy"] == policy and r["request_id"] in ids))
            stats["total_clauses"] = sum(int(c["extra_clauses"]) for c in costs
                                         if c["request_id"] in ids and c["policy"] == policy)
            stats["conditional_checks"] = sum(int(c["conditional_checks"]) for c in costs
                                             if c["request_id"] in ids and c["policy"] == policy)
            metrics["policy"][policy] = stats
        for before, after in zip(POLICIES[:-1], POLICIES[1:], strict=True):
            transitions_for_pair = [t for t in data if t["from"] == before and t["to"] == after and t["request_id"] in ids]
            stats = {}
            for stage in STAGES:
                stage_rows = [t for t in transitions_for_pair if t["stage"] == stage]
                stats[stage] = dict(Counter(t["change"] + ":" + t["grade"] for t in stage_rows
                                            if t["change"] in ("entered", "left", "up", "down")))
            metrics["transitions"][before + "→" + after] = stats
        totals[name] = metrics
    counted = {s["work_id"]: s for s in sources if s["read_ok"] and s["minimum_count"]}
    assert len(counted) == sum(s["read_ok"] and s["minimum_count"] for s in sources)
    return {"frame": count_frame(frame), "policy": totals, "aliases": dict(Counter(a["first_policy"] for a in aliases)),
            "reads": {"unique_counted": len(counted), "by_kind": dict(Counter(s["kind"] for s in counted.values())),
                      "by_novelty": dict(Counter(s["read_status"] for s in counted.values())),
                      "source_rows": len(sources)},
            "rows": {"ranks": len(ranks), "transitions": len(data), "slots": len(all_slots),
                     "paired_policies_per_request": 3, "display": len(display), "truth": len(truth)},
            "verification": "independent sort, occupancy and set-difference recount with exact ledger joins"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT)
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()
    print(json.dumps(recompute(args.data, args.replay), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
