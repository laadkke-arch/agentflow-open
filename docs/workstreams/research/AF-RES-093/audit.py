"""Read-only reconciliation of AF-RES-093 source rows and reported denominators."""
from collections import Counter
import csv
from datetime import datetime
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
    field_slots = {}
    for case in CASES:
        payload = indexed[case, "B"]["record"]
        filled, missing = [], []
        for index, candidate in enumerate(payload["candidates"]):
            for field in ("next_operation", "reference_target", "preserve_value"):
                value = None
                if candidate is not None:
                    if field in payload:
                        container = payload[field]
                        value = container.get(candidate.get("id")) if isinstance(container, dict) else container
                    else:
                        value = candidate.get("referent" if field == "reference_target" else field)
                (filled if value is not None and value != "" else missing).append(f"candidate{index + 1}.{field}")
        field_slots[case] = {"filled": len(filled), "slots": 6, "missing": missing}
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
        canonical = {}
        for row in rows:
            if row["is_first30"] == "true":
                canonical.setdefault(int(row["event_rank"]), row)
        ordered = [canonical[n] for n in range(1, 31)]
        chronological = sorted(ordered, key=lambda r: (
            datetime.fromisoformat(r["created_utc"].replace("Z", "+00:00")),
            int(r["issue_id"] or r["number"]),
        ))
        assert [r["url"] for r in ordered] == [r["url"] for r in chronological], project
        assert {r["url"] for r in ordered[:3]} == selected, project
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
    source_ids = {r["source_id"] for r in sources}
    assert len(source_ids) == len(sources)
    for judgment in judgments:
        assert set(filter(None, judgment["post_source_ids"].split(";"))) <= source_ids, judgment["request_id"]
    counted = [r for r in sources if r.get("counted") is True]
    for row in sources:
        assert {"url", "reopen_url", "published_at", "accessed_utc", "version", "locator",
                "observation", "questions", "limitations", "work_id", "event_id", "counted"} <= row.keys(), row["source_id"]
        assert row.get("url") and row.get("limitations")
        if row.get("counted") is True:
            assert row.get("accessed_utc"), row["source_id"]
        elif not row.get("accessed_utc"):
            # Do not manufacture precise timestamps for excluded discovery
            # reads. Require an explicit missing-time reason and a bound.
            assert row.get("accessed_utc_window") or (row.get("accessed_utc_limit") and row.get("recorded_utc")), row["source_id"]
    # A work lineage may contain distinct help/code/test files. Count the
    # documents and those shared lineages separately, never as independent votes.
    counted_work_ids = [r["work_id"] for r in counted]
    document_ids = [r.get("document_id", r["url"].split("#")[0]) for r in counted]
    assert len(document_ids) == len(set(document_ids)), "counted duplicate document URL"
    opened_issue_events = sorted({r["event_id"] for r in counted if r["event_id"].startswith(("inkscape-issue-", "pillow-issue-"))})
    normalized_categories = Counter()
    for row in counted:
        category = {"initial_request": "new_requests", "new_request": "new_requests",
                    "official_versioned": "versioned_official", "official_candidate": "versioned_official"}.get(row["category"], row["category"])
        normalized_categories[category] += 1
    summary = {
        "request_slots": 6, "method_slots": 12,
        "candidate_pairs": sum(indexed[c, "A"]["record"]["candidates"][1] is not None for c in CASES),
        "extra_field_slots": {"filled": sum(v["filled"] for v in field_slots.values()), "total": 36, "by_case": field_slots,
                              "limit": "non-null text only; does not certify intent, observed success, or a true subsequent operation"},
        "missing_candidate2": [c for c in CASES if indexed[c, "A"]["record"]["candidates"][1] is None],
        "frames": frames, "metrics": metrics,
        "changed_judgment": [c for c in CASES if indexed[c, "A"]["judgment"] != indexed[c, "B"]["judgment"]],
        "source_rows": len(sources), "counted_unique_primary": len(counted),
        "counted_work_lineages": len(set(counted_work_ids)),
        "source_categories": dict(Counter(r["category"] for r in counted)),
        "counted_event_ids": len({r["event_id"] for r in counted}),
        "event_id_count_limit": "includes specification/implementation/test families; not independent user incidents",
        "directly_opened_issue_events": opened_issue_events,
        "directly_opened_issue_event_count": len(opened_issue_events),
        "identified_regression_issue_without_original_thread": ["tdf116413"],
        "normalized_source_categories": dict(normalized_categories),
        "excluded_rows_without_exact_access_utc": sum(not r.get("accessed_utc") for r in sources if not r.get("counted")),
        "zero_denominator_rule": "산출 불가; never interpret 0/0 as zero error",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
