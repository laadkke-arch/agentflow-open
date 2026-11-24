"""Independently recount committed frame, truth, rank, and source rows."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from project import read_jsonl


LAYERS = ("A", "B", "G1", "G2")
POLICIES = ("B", "C", "Gate")


def csv_file(root, relative):
    with (root / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def recount(root):
    frame = csv_file(root, "frame.csv")
    requests = read_jsonl(root / "requests.jsonl")
    truth = csv_file(root, "truth.csv")
    ranks = csv_file(root, "ranks.csv")
    ledger = read_jsonl(root / "sources.jsonl")
    gates = csv_file(root, "display-review.csv")
    metrics = csv_file(root, "evidence/metrics.csv")
    costs = csv_file(root, "evidence/editor-cost.csv")
    ids = {r["request_id"] for r in requests}
    expected_cards = {f"{family}{index:02}" for family in "DT" for index in range(1, 9)}
    pairs = {(rid, cid) for rid in ids for cid in expected_cards}
    for table in (truth, gates):
        assert {(r["request_id"], r["feature_id"]) for r in table} == pairs and len(table) == len(pairs)
    assert {(r["request_id"], r["feature_id"], r["policy"]) for r in ranks} == {
        (*pair, policy) for pair in pairs for policy in POLICIES
    }
    assert len(ranks) == len(pairs) * len(POLICIES)
    sources = {r["source_id"]: r for r in ledger}
    assert len(ledger) == len(sources)
    assert all(r["url"].startswith("https://") and r["location"] and r["timestamp_precision"]
               and r["confirmed"] and r["limit"] for r in ledger)
    assert all(r["source_id"] in sources for r in frame if r["source_id"])
    assert all(r["source_id"] in sources for r in requests)
    assert all(r["card_source_id"] in sources for r in gates)
    assert all(r["source_id"] in sources for r in read_jsonl(root / "evidence/lexical-probes.jsonl"))
    eligible_sources = [r for r in ledger if r["count_for_external_minimum"]]
    assert all(r["access"] == "success" for r in eligible_sources)
    assert len({r["work_id"] for r in eligible_sources}) == len(eligible_sources)

    displayed = {}
    for rid in ids:
        for policy in POLICIES:
            ordered = [r for r in ranks if r["request_id"] == rid and r["policy"] == policy]
            assert ordered == sorted(ordered, key=lambda r: (-int(r["score"]), r["feature_id"]))
            for r in ordered:
                if int(r["score"]) == 0:
                    assert not r["investigation_rank"] and not r["display_rank"]
            i = [r["feature_id"] for r in ordered if r["investigation_rank"]]
            d = [r["feature_id"] for r in ordered if r["display_rank"]]
            assert len(i) <= 8 and len(d) <= 3 and [cid for cid in i if cid in d] == d
            displayed[rid, policy] = (i, d)
        assert displayed[rid, "C"][0] == displayed[rid, "Gate"][0]

    index = {(r["group"], r["policy"]): r for r in metrics}
    rows = {}
    for layer in LAYERS:
        seen = [r for r in frame if r["layer"] == layer]
        selected = {r["source_id"] for r in seen if r["selection"] == "selected"}
        assert selected == {r["request_id"] for r in requests if r["layer"] == layer}
        source_rows = [r for r in seen if r["access"] == "opening" or r["alternative_access"] == "opening"]
        rows[layer] = {
            "planned_slots": len(seen),
            "first_body_views": len(source_rows),
            "unique_opening_urls": len({sources[r["source_id"]]["url"] for r in source_rows}),
            "unique_opening_works": len({sources[r["source_id"]]["work_id"] for r in source_rows}),
            "excluded": sum(r["eligibility"] == "excluded" for r in seen),
            "duplicates": sum(r["eligibility"] == "duplicate" for r in seen),
            "unknown": sum(r["eligibility"] in ("unknown", "unconfirmed") for r in seen),
            "no_returned_id": sum(r["eligibility"] == "no_id" for r in seen),
            "accepted": len(selected),
            "authors": len({r["author_key"] for r in seen if r["source_id"] in selected}),
            "all_author_keys": len({r["author_key"] for r in seen if r["author_key"]}),
            "all_unknown_authors": sum(not r["author_key"] for r in source_rows),
        }
        truth_layer = [r for r in truth if r["request_id"] in selected]
        for policy in POLICIES:
            metric = index[layer, policy]
            direct = [r for r in truth_layer if r["grade"] == "direct"]
            assert int(metric["requests"]) == len(selected)
            assert int(metric["pairs"]) == len(truth_layer)
            assert int(metric["pair_direct"]) == len(direct)
            assert int(metric["direct_available_requests"]) == len({r["request_id"] for r in direct})
            for stage, width in (("investigation", 8), ("display", 3)):
                current = [r for r in ranks if r["request_id"] in selected and r["policy"] == policy
                           and r[f"{stage}_rank"]]
                grades = Counter(r["grade"] for r in current)
                assert int(metric[f"{stage}_vacant"]) == width * len(selected) - len(current)
                for grade in ("direct", "partial", "conflict", "unconfirmed"):
                    assert int(metric[f"{stage}_{grade}"]) == grades[grade]
                old_policy = {"B": "B", "C": "B", "Gate": "C"}[policy]
                old = {(r["request_id"], r["feature_id"], r["grade"]) for r in ranks
                       if r["request_id"] in selected and r["policy"] == old_policy and r[f"{stage}_rank"]}
                new = {(r["request_id"], r["feature_id"], r["grade"]) for r in current}
                for difference, prefix in ((new - old, "gain"), (old - new, "lose")):
                    assert int(metric[f"{stage}_{prefix}_direct"]) == sum(item[2] == "direct" for item in difference)
                assert int(metric[f"{stage}_add_conflict"]) == sum(item[2] == "conflict" for item in new - old)
                assert int(metric[f"{stage}_remove_conflict"]) == sum(item[2] == "conflict" for item in old - new)
            assert int(metric["extra_clauses"]) == sum(int(r["extra_clauses"]) for r in costs
                                                      if r["policy"] == policy and r["request_id"] in selected)

    return {
        "frame": rows, "frame_total_rows": len(frame),
        "request_count": len(requests), "request_author_count": len({r["author_key"] for r in requests}),
        "display_review_rows": len(gates), "truth_rows": len(truth), "rank_rows": len(ranks),
        "source_rows": len(ledger), "source_access": dict(Counter(r["access"] for r in ledger)),
        "counted_external_works": len(eligible_sources),
        "counted_by_kind": dict(Counter(r["kind"] for r in eligible_sources)),
        "pytorch_reopen_or_new": dict(Counter(r["lineage"] for r in eligible_sources if "lineage" in r)),
        "paired_effects_recounted_from_rank_positions": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(json.dumps(recount(args.data), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
