"""Replay the locked B/C ranker, apply the preread Gate, and count paired effects."""

import argparse
import csv
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

from project import load_predecessors, read_jsonl, read_module


HERE = Path(__file__).resolve().parent
GRADES = ("direct", "partial", "conflict", "unconfirmed")
POLICIES = ("B", "C", "Gate")
PREVIOUS = {"B": None, "C": "B", "Gate": "C"}
STAGES = {"investigation": 8, "display": 3}
PINS = {
    "af122": (
        "aliases.csv", "catalog.csv", "prepare.py", "replay.py",
        "evidence/query-inputs.jsonl", "evidence/controls-query-inputs.jsonl",
    ),
    "af126": ("capture.py", "replay.py"),
}


def coverage(rows, ids, features, name):
    indexed = {(r["request_id"], r["feature_id"]): r for r in rows}
    expected = {(rid, fid) for rid in ids for fid in features}
    if set(indexed) != expected or len(rows) != len(expected):
        raise ValueError(f"{name}: require exactly one row for every request and card")
    return indexed


def check_projection(view, request, prepare, legacy):
    basic = {key: view[key] for key in legacy.VIEW_FIELDS}
    extra = {key: view[key] for key in ("korean_retained_runs", "korean_words")}
    if prepare.sha(prepare.packed(basic)) != view["projection_sha256"]:
        raise ValueError("legacy projection SHA differs")
    if prepare.sha(prepare.packed(extra)) != view["extended_projection_sha256"]:
        raise ValueError("Korean projection SHA differs")
    if view["view"] != "raw" or view["view_sha256"] != request["nfc_sha256"]:
        raise ValueError("replay needs the frozen natural-symbol first-body view")
    size = view["normalized_codepoints"]
    if size != request["normalized_codepoints"] or view["original_sha256"] != request["original_sha256"]:
        raise ValueError("first-body size or fingerprint differs")
    for span in request["spans"] + view["symbol_spans"]:
        text = span.get("excerpt", span.get("before"))
        start, end = span["start"], span["end"]
        if not (0 <= start < end <= size and end - start == len(text)):
            raise ValueError("span lies outside the NFC codepoint interval")
        if unicodedata.normalize("NFC", text) != text:
            raise ValueError("span isn't NFC")
        if "sha256" in span and span["sha256"] != prepare.sha(text):
            raise ValueError("excerpt fingerprint differs")
    if set(view["exact_ids"]) != {span["feature_id"] for span in view["symbol_spans"]}:
        raise ValueError("symbol occurrences disagree with the lexical view")
    for word, starts in view["english_positions"].items():
        if any(not 0 <= start < start + len(word) <= size for start in starts):
            raise ValueError("English word lies outside the NFC text")
    for run in view["korean_retained_runs"]:
        for item in run:
            if item:
                start, text = item
                if not (0 <= start < start + len(text) <= size and prepare.KOREAN_WORD.fullmatch(text)):
                    raise ValueError("Korean word lies outside the NFC text")


def gate_order(rid, positive, review):
    displayed, scanned = [], []
    for fid in positive[:STAGES["investigation"]]:
        scanned.append(fid)
        if review[rid, fid]["gate"] == "pass":
            displayed.append(fid)
            if len(displayed) == STAGES["display"]:
                break
    return displayed, scanned


def location_change(before, after):
    if before is None and after is None:
        return "outside"
    if before is None:
        return "entered"
    if after is None:
        return "left"
    return "up" if after < before else "down" if after > before else "same"


def costs(rid, policy, scanned, review):
    # Explicit counters for the policy's modeled on-demand reader. Offline
    # sealing examined all pairs and is reported separately from these counts.
    request_spans, clauses = set(), set()
    for fid in scanned:
        row = review[rid, fid]
        request_spans.update(filter(None, row["request_spans"].split("|")))
        clauses.add(row["card_clause_url"])
    return {
        "request_id": rid,
        "policy": policy,
        "examined_cards": len(scanned),
        "extra_request_clauses": len(request_spans),
        "extra_card_clauses": len(clauses),
        "extra_clauses": len(request_spans) + len(clauses),
        "examined_card_ids": "|".join(scanned),
        "request_span_ids": "|".join(sorted(request_spans)),
        "card_clause_urls": "|".join(sorted(clauses)),
    }


def describe_gate(fid, positive, scanned, display, review, rid):
    if fid in display:
        return "display"
    if fid not in positive:
        return "zero_score"
    if fid not in positive[:STAGES["investigation"]]:
        return "investigation_cap"
    if fid not in scanned:
        return "display_cap"
    if review[rid, fid]["gate"] != "hold":
        raise ValueError("a scanned passing card must be displayed")
    return "gate_hold"


def make_ranks(request, view, replay, legacy, features, aliases, glossary, alias_sha, review, truth):
    rid = request["request_id"]
    hits, _ = replay.find_aliases(view["korean_retained_runs"], glossary)
    data, orders = {}, {}
    for policy in ("B", "C"):
        ranks, positive, _ = replay.ranking(
            rid, "raw", view, policy, replay.eligible_hits(hits, policy),
            features, aliases, legacy, alias_sha
        )
        data[policy] = ranks
        orders[policy] = {"investigation": positive[:STAGES["investigation"]],
                          "display": positive[:STAGES["display"]]}
    positive_c = [row["feature_id"] for row in data["C"] if row["score"] > 0]
    display_gate, scanned = gate_order(rid, positive_c, review)
    orders["Gate"] = {"investigation": orders["C"]["investigation"], "display": display_gate}
    data["Gate"] = data["C"]
    rank_rows, slot_rows, changes, inspections = [], [], [], []
    for policy in POLICIES:
        policy_scanned = scanned if policy == "Gate" else []
        inspections.append(costs(rid, policy, policy_scanned, review))
        previous = PREVIOUS[policy]
        new_positions = {stage: {fid: i for i, fid in enumerate(orders[policy][stage], 1)}
                         for stage in STAGES}
        old_positions = {stage: {fid: i for i, fid in enumerate(orders[previous][stage], 1)}
                         if previous else {} for stage in STAGES}
        for number, score in enumerate(data[policy], 1):
            fid = score["feature_id"]
            grades = truth[rid, fid]["grade"]
            investigate = new_positions["investigation"].get(fid)
            display = new_positions["display"].get(fid)
            old_i = old_positions["investigation"].get(fid)
            old_d = old_positions["display"].get(fid)
            reasons = {}
            for stage, old, new in (("investigation", old_i, investigate), ("display", old_d, display)):
                change = location_change(old, new) if previous else "baseline"
                reasons[stage] = change
                if change in ("entered", "left", "up", "down"):
                    changes.append({
                        "request_id": rid, "layer": request["layer"], "from": previous, "to": policy,
                        "stage": stage, "feature_id": fid, "grade": grades, "change": change,
                        "old_position": old, "new_position": new,
                    })
            rank_rows.append({
                "layer": request["layer"], "window": request["window"], "request_id": rid, "policy": policy,
                "feature_id": fid, "score": score["score"], "zero_score": score["score"] == 0,
                "overall_position": number, "positive_rank": score["positive_rank"],
                "investigation_rank": investigate, "display_rank": display, "grade": grades,
                "symbol_points": score["symbol_points"], "alias_points": score["alias_points"],
                "english_points": score["english_points"], "alias_ids": score["alias_hits"],
                "alias_positions": score["alias_positions"], "english_positions": score["english_positions"],
                "gate_scanned": fid in policy_scanned,
                "gate_decision": review[rid, fid]["gate"] if fid in policy_scanned else "",
                "reason": (describe_gate(fid, positive_c, scanned, display_gate, review, rid)
                           if policy == "Gate" else score["reason"]),
                "investigation_change": reasons["investigation"], "display_change": reasons["display"],
                "previous_investigation_rank": old_i, "previous_display_rank": old_d,
                "nfc_sha256": view["view_sha256"], "projection_sha256": view["projection_sha256"],
            })
        for stage, count in STAGES.items():
            selected = orders[policy][stage]
            for slot in range(1, count + 1):
                fid = selected[slot - 1] if slot <= len(selected) else ""
                slot_rows.append({
                    "request_id": rid, "layer": request["layer"], "policy": policy, "stage": stage,
                    "position": slot, "feature_id": fid, "grade": truth[rid, fid]["grade"] if fid else "",
                    "vacancy": not fid,
                    "reason": ("ranked" if fid else "gate_capacity_empty"
                               if stage == "display" and policy == "Gate" else "positive_candidates_exhausted"),
                })
    return rank_rows, slot_rows, changes, inspections, [
        {"request_id": rid, **hit, "counts_in_replay": hit["first_policy"] in ("B", "C")}
        for hit in hits
    ]


def paired_effects(transitions, ids, policy, stage):
    changes = [t for t in transitions if t["request_id"] in ids and t["to"] == policy and t["stage"] == stage]
    counts = Counter((t["grade"], t["change"]) for t in changes)
    return {"gain_direct": counts["direct", "entered"], "lose_direct": counts["direct", "left"],
            "add_conflict": counts["conflict", "entered"], "remove_conflict": counts["conflict", "left"]}


def summarize(requests, views, truth, slots, transitions, inspections, frame):
    groups = {name: {r["request_id"] for r in requests if r["layer"] == name} for name in ("A", "B", "G1", "G2")}
    groups.update({name: {r["request_id"] for r in requests if r["window"] == name} for name in ("G2-how", "G2-want")})
    groups["symbol:yes"] = {rid for rid, view in views.items() if view["exact_ids"]}
    groups["symbol:no"] = set(views) - groups["symbol:yes"]
    groups["role:data"] = {r["request_id"] for r in requests if r["role"].startswith("data_")}
    groups["role:tensor"] = set(views) - groups["role:data"]
    groups["combined:observed"] = set(views)
    frames = {group: Counter((r["access"], r["eligibility"]) for r in frame
                             if r["layer"] == group or r["window"] == group)
              for group in ("A", "B", "G1", "G2", "G2-how", "G2-want")}
    direct = {rid for (rid, _), row in truth.items() if row["grade"] == "direct"}
    metrics = []
    for group, ids in groups.items():
        base_grades = Counter(row["grade"] for (rid, _), row in truth.items() if rid in ids)
        for policy in POLICIES:
            counts = {"group": group, "policy": policy, "requests": len(ids),
                      "pairs": sum(base_grades.values()), "direct_available_requests": len(direct & ids),
                      **{f"pair_{grade}": base_grades[grade] for grade in GRADES}}
            for stage, cap in STAGES.items():
                stage_slots = [s for s in slots if s["policy"] == policy and s["stage"] == stage
                               and s["request_id"] in ids]
                slot_grades = Counter(s["grade"] for s in stage_slots)
                if len(stage_slots) != cap * len(ids):
                    raise ValueError("slot denominator disagrees with request count")
                counts[f"{stage}_capacity"] = len(stage_slots)
                counts[f"{stage}_vacant"] = slot_grades[""]
                counts.update({f"{stage}_{grade}": slot_grades[grade] for grade in GRADES})
                counts.update({f"{stage}_{key}": value for key, value in paired_effects(
                    transitions, ids, policy, stage
                ).items()})
            counts["extra_clauses"] = sum(c["extra_clauses"] for c in inspections
                                          if c["policy"] == policy and c["request_id"] in ids)
            metrics.append(counts)
    return metrics, {group: {"|".join(k): v for k, v in sorted(counts.items())} for group, counts in frames.items()}


def save_csv(path, rows, fields=None):
    if fields is None:
        fields = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run(root, af122, af126, output):
    prepare, legacy, capture = load_predecessors(af122, af126)
    sys.modules["capture"] = capture
    replay = read_module("af126_replay", af126 / "replay.py")
    features, aliases, _, _ = legacy.read_inputs(af122)
    glossary = capture.aliases_by_phrase(prepare, af122 / "aliases.csv")
    if len(features) != 16 or len(glossary) != 12:
        raise ValueError("expected the exact card pool and 12 active aliases")
    requests = read_jsonl(root / "requests.jsonl")
    ids = {r["request_id"] for r in requests}
    projection = read_jsonl(root / "replay/inputs.jsonl")
    views = {r["request_id"]: r for r in projection}
    if set(views) != ids or len(ids) != len(requests) or len(views) != len(projection):
        raise ValueError("each unique request needs exactly one view")
    review = coverage(prepare.read_csv(root / "display-review.csv"), ids, features, "display review")
    truth = coverage(prepare.read_csv(root / "truth.csv"), ids, features, "truth")
    if any(r["grade"] not in GRADES for r in truth.values()) or any(r["gate"] not in ("pass", "hold") for r in review.values()):
        raise ValueError("unexpected preclassified truth or gate status")
    spans_by_request = {r["request_id"]: {span["span_id"] for span in r["spans"]} for r in requests}
    for key, row in review.items():
        spans = spans_by_request[key[0]]
        if not set(filter(None, row["request_spans"].split("|"))) <= spans:
            raise ValueError("gate points outside frozen request span IDs")
    alias_sha = legacy.file_sha(af122 / "aliases.csv")
    boundary_count = replay.boundary_checks(prepare, legacy, glossary, features, aliases, alias_sha)
    ranks, slots, transitions, inspections, aliases_found = [], [], [], [], []
    for r in requests:
        view = views[r["request_id"]]
        check_projection(view, r, prepare, legacy)
        batch = make_ranks(r, view, replay, legacy, features, aliases, glossary, alias_sha, review, truth)
        for target, rows in zip((ranks, slots, transitions, inspections, aliases_found), batch, strict=True):
            target.extend(rows)
    frame = prepare.read_csv(root / "frame.csv")
    if {row["source_id"] for row in frame if row["selection"] == "selected"} != ids:
        raise ValueError("frame and selected requests disagree")
    metrics, recruitment = summarize(requests, views, truth, slots, transitions, inspections, frame)
    output.mkdir(parents=True, exist_ok=True)
    tables = {
        "ranks.csv": (ranks, None),
        "slots.csv": (slots, None),
        "transitions.csv": (transitions, ["request_id", "layer", "from", "to", "stage", "feature_id", "grade",
                                             "change", "old_position", "new_position"]),
        "editor-cost.csv": (inspections, None),
        "alias-audit.csv": (aliases_found, ["request_id", "alias_id", "feature_id", "first_policy", "phrase", "start",
                                             "end", "last_start", "token_start", "token_end", "last_token", "prefix",
                                             "suffix", "particle", "counts_in_replay"]),
        "metrics.csv": (metrics, None),
    }
    for name, (rows, fields) in tables.items():
        save_csv(output / name, rows, fields)
    files = ("requests.jsonl", "replay/inputs.jsonl", "frame.csv", "display-review.csv", "truth.csv",
             "replay/project.py", "replay/run.py")
    return {
        "request_count": len(requests), "boundary_assertions": boundary_count,
        "fixed_input_sha256": {name: legacy.file_sha(root / name) for name in files},
        "predecessor_input_sha256": {
            tag: {name: legacy.file_sha(parent / name) for name in PINS[tag]}
            for tag, parent in (("af122", af122), ("af126", af126))
        },
        "frame_counts": recruitment,
        "output_rows": {name: len(rows) for name, (rows, _) in tables.items()},
        "output_sha256": {name: legacy.file_sha(output / name) for name in tables},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=HERE.parent)
    parser.add_argument("--af122", type=Path, required=True)
    parser.add_argument("--af126", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = run(args.data, args.af122, args.af126, args.out)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
