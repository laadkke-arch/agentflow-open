"""Verify AF-RES-046 sklearn ledger units; no upstream code is executed."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent


def read_csv(name):
    with (ROOT / name).open(newline="") as stream:
        return list(csv.DictReader(stream))


sources = [json.loads(line) for name in ("sources.jsonl", "sources-supplement.jsonl")
           for line in (ROOT / name).read_text().splitlines()]
ids = {row["source_id"] for row in sources}
assert len(ids) == len(sources), "Duplicate source ID"
counted = [row for row in sources if row["count_in_minimum"]]
assert len({row["work_id"] for row in counted}) == len(counted), "Double-counted work"
cases = json.loads((ROOT / "cases.json").read_text())
slots = {row["slot_id"] for row in cases}
assert slots == {"N-S1", "N-S2", "N-S3", "N-S4", "L-S1", "L-S2"}
rows_by_file = {name: read_csv(name) for name in
                ("frame.csv", "baselines.csv", "events.csv", "changes.csv", "labor.csv")}
assert len(rows_by_file["frame.csv"]) == 80
assert Counter(row["stratum"] for row in rows_by_file["frame.csv"]) == {"natural": 40, "link": 40}
for name, rows in rows_by_file.items():
    if name == "frame.csv":
        continue
    for row in rows:
        assert row["slot_id"] in slots, (name, row["slot_id"])
        refs = {item for item in row.get("source_ids", "").split(";") if item}
        assert refs <= ids, (name, refs - ids)
assert len(rows_by_file["baselines.csv"]) == len(rows_by_file["labor.csv"]) == 6
for case in cases:
    assert set(case["source_ids"]) <= ids
    assert case["strict"] is False
    assert case["labor"] is False and case["paired_quality_time"] is False
assert next(row for row in rows_by_file["labor.csv"] if row["slot_id"] == "L-S1")["actual_changed_files"].endswith("sklearn/exceptions.py")
assert next(row for row in rows_by_file["labor.csv"] if row["slot_id"] == "L-S2")["link_to_first_same_author_patch_seconds"] == "139292"
assert next(row for row in cases if row["slot_id"] == "L-S1")["same_author_change"] is None
result = {
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "command": "python -B docs/workstreams/research/AF-RES-046/streams/sklearn/verify_stream.py",
    "kind": "ledger consistency only; retrospective upstream tests not run",
    "selection_remote_sha": "994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f",
    "bundle2_remote_sha": "03df204224d89d5c7d6c3976116fc0ff047f9865",
    "rows": {name: len(rows) for name, rows in rows_by_file.items()},
    "source_receipts": len(sources),
    "minimum_unique_works": len(counted),
    "minimum_by_allocation": dict(Counter(row["allocation"] for row in counted)),
    "screening_attempt_receipts": len((ROOT / "screening-attempts.jsonl").read_text().splitlines()),
    "confirmed": {"natural_prs": 4, "natural_links": 0, "additional_prs": 2,
                  "additional_links": 2, "explicit_reading": 0, "first_discovery": 0,
                  "first_link_same_author_change": 1, "same_author_change_unknown": 1,
                  "including_other_author_change": 2, "strict": 0,
                  "direct_human_time": 0, "author_timed_selfreport": 0,
                  "comparable_quality_time_pairs": 0},
    "limitations": ["First public upload identities and body editions not fully fixed",
                    "L-S1 force-push lost original author follow-up history",
                    "Selection outcome masking imperfect; excluded25272 later committer edition",
                    "No external independent human adjudication; no causal savings estimate"],
    "input_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                     for name in (*rows_by_file, "sources.jsonl", "sources-supplement.jsonl",
                                  "screening-attempts.jsonl", "cases.json", "counterexamples.md")},
    "status": "passed_local_ledger_checks",
}
(ROOT / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
