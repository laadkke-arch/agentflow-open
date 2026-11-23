"""Read-only reconciliation of AF-RES-093 source rows and reported denominators."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ("I1", "I2", "I3", "P1", "P2", "P3")
EXTRA = {"next_operation", "reference_target", "referent", "preserve_value"}


def jl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def csv_rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def stripped(payload):
    result = {k: v for k, v in payload.items() if k not in EXTRA}
    result["candidates"] = [
        {k: v for k, v in c.items() if k not in EXTRA} if c is not None else None
        for c in result["candidates"]
    ]
    return result


def main():
    records = jl(ROOT / "records.jsonl")
    indexed = {(r["request_id"], r["mode"]): r for r in records}
    assert len(records) == len(indexed) == 12
    assert set(indexed) == {(c, m) for c in CASES for m in ("A", "B")}
    for row in records:
        size = len(json.dumps(row["record"], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        assert size == row["utf8_bytes"], (row["request_id"], row["mode"], size, row["utf8_bytes"])
        assert row["judgment"] in {"묶음", "분리", "유보"}
    for case in CASES:
        assert stripped(indexed[case, "A"]["record"]) == stripped(indexed[case, "B"]["record"]), case
    pre = json.loads((ROOT / "evidence/preseal-summary.json").read_text())
    for relative, expected in pre["fragments"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative

    frame = csv_rows(ROOT / "frame.csv")
    frames = {}
    for project in ("inkscape", "pillow"):
        rows = [r for r in frame if r["project_key"] == project]
        first = {int(r["event_rank"]) for r in rows if r["is_first30"] == "true" and r["event_rank"]}
        assert first == set(range(1, 31)), (project, first)
        selected = {r["url"] for r in rows if r["selected_for_study"] == "true"}
        assert len(selected) == 3, (project, selected)
        frames[project] = {"raw_rows": len(rows), "first30_events": len(first), "selected": len(selected)}

    judgments = csv_rows(ROOT / "judgments.csv")
    assert len(judgments) == 12
    assert {(r["request_id"], r["method"]) for r in judgments} == set(indexed)
    for row in judgments:
        record = indexed[row["request_id"], row["method"]]
        assert row["pre_judgment"] == record["judgment"]
        assert int(row["record_bytes"]) == record["utf8_bytes"]
        if row["scorable"] == "true":
            assert row["truth"] in {"묶음", "분리"}
            assert row["post_source_ids"] and row["post_urls"] and row["expected"]
            assert int(row["candidate_count"]) == 2
    for case in CASES:
        two = [r for r in judgments if r["request_id"] == case]
        assert len({r["truth"] for r in two}) == 1
        assert len({r["scorable"] for r in two}) == 1

    metrics = {}
    for mode in ("A", "B"):
        rows = [r for r in judgments if r["method"] == mode]
        scored = [r for r in rows if r["scorable"] == "true"]
        decided = [r for r in scored if r["pre_judgment"] != "유보"]
        split = [r for r in decided if r["truth"] == "분리"]
        merge = [r for r in decided if r["truth"] == "묶음"]
        wrong_merge = sum(r["pre_judgment"] == "묶음" for r in split)
        wrong_split = sum(r["pre_judgment"] == "분리" for r in merge)
        metrics[mode] = {
            "pre": dict(Counter(r["pre_judgment"] for r in rows)),
            "truth_available": len(scored), "truth_missing": 6 - len(scored),
            "scored_decisions": len(decided),
            "false_merge": {"numerator": wrong_merge, "denominator": len(split), "all_truth_split": sum(r["truth"] == "분리" for r in scored)},
            "unnecessary_split": {"numerator": wrong_split, "denominator": len(merge), "all_truth_merge": sum(r["truth"] == "묶음" for r in scored)},
            "all_error": {"numerator": wrong_merge + wrong_split, "denominator": len(decided)},
            "abstentions": sum(r["pre_judgment"] == "유보" for r in rows),
            "payload_utf8_bytes": sum(r["utf8_bytes"] for r in records if r["mode"] == mode),
            "payload_denominator": 6,
        }

    sources = jl(ROOT / "sources.jsonl")
    assert len({r["source_id"] for r in sources}) == len(sources)
    counted = [r for r in sources if r.get("counted") is True]
    for row in sources:
        assert row.get("url") and row.get("accessed_utc") and row.get("limitations")
    # A work lineage may contain distinct help/code/test files. Count the
    # documents and those shared lineages separately, never as independent votes.
    counted_work_ids = [r["work_id"] for r in counted]
    document_ids = [r.get("document_id", r["url"].split("#")[0]) for r in counted]
    assert len(document_ids) == len(set(document_ids)), "counted duplicate document URL"
    summary = {
        "request_slots": 6, "method_slots": 12,
        "candidate_pairs": sum(indexed[c, "A"]["record"]["candidates"][1] is not None for c in CASES),
        "missing_candidate2": [c for c in CASES if indexed[c, "A"]["record"]["candidates"][1] is None],
        "frames": frames, "metrics": metrics,
        "changed_judgment": [c for c in CASES if indexed[c, "A"]["judgment"] != indexed[c, "B"]["judgment"]],
        "source_rows": len(sources), "counted_unique_primary": len(counted),
        "counted_work_lineages": len(set(counted_work_ids)),
        "source_categories": dict(Counter(r["category"] for r in counted)),
        "counted_event_ids": len({r["event_id"] for r in counted}),
        "zero_denominator_rule": "산출 불가; never interpret 0/0 as zero error",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
