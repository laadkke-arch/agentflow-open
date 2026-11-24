"""Recount the public ledgers and check their references and required table positions."""

from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_KEYS = {
    "archive.csv": "archive_id", "selection.csv": None, "events.csv": "event_id",
    "pairs.csv": "pair_id", "contrasts.csv": "contrast_id",
}
FLOORS = {"experiment": 8, "event_record": 4, "original_example": 4,
          "genetic_edition": 2, "storyboard": 2}
FINAL_TABLE = "| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |"


def load_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def close_table(text):
    table = text.strip().splitlines()[-5:]
    return (
        table[0] == FINAL_TABLE
        and table[1].startswith("| --- |")
        and all(line.startswith("| ") and line.endswith(" |") for line in table[2:])
    )


def check():
    ledger = ROOT / "sources.jsonl"
    sources = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    ids = {row["source_id"] for row in sources}
    if len(ids) != len(sources):
        raise ValueError("duplicate source ids")
    required = set(sources[0])
    empty_source_fields = sum(
        1 for row in sources for key in required if row.get(key) in (None, "", [])
    )
    if empty_source_fields:
        raise ValueError("source entries have missing fields")

    counted = [row for row in sources if row["counted"]]
    work_ids = {row["work_id"] for row in counted}
    by_category = Counter(row["category"] for row in counted)
    if any(row["access"] != "success" for row in counted) or len(work_ids) != len(counted):
        raise ValueError("source floor counts only distinct successful original works")
    if any(by_category[kind] < minimum for kind, minimum in FLOORS.items()):
        raise ValueError("source floor omitted by category")

    summaries = {}
    ledgers = {name: load_csv(name) for name in CSV_KEYS}
    for name, key in CSV_KEYS.items():
        rows = ledgers[name]
        empty = sum(value in (None, "") for row in rows for value in row.values())
        unknown = sum("미확인" in value for row in rows for value in row.values() if isinstance(value, str))
        duplicate = len(rows) - len({row[key] for row in rows}) if key else 0
        refs = {s for row in rows for s in row.get("source_ids", "").split(";") if s}
        if empty or duplicate or refs - ids:
            raise ValueError(f"ledger integrity failure in {name}")
        summaries[name] = {"rows": len(rows), "empty_cells": empty, "unconfirmed_cells": unknown,
                           "duplicate_ids": duplicate, "dangling_source_ids": sorted(refs - ids)}

    planned = ledgers["selection.csv"]
    planned_keys = [(r["study"], r["layer"], r["planned_slot"]) for r in planned]
    paired = ledgers["pairs.csv"]
    paired_keys = [(r["work_id"], r["layer"], r["planned_slot"]) for r in paired if r["planned_slot"] != "적용 외"]
    if planned_keys != paired_keys or len(planned_keys) != len(set(planned_keys)):
        raise ValueError("planned slots were replaced, reordered, or duplicate")
    event_records = [int(row["record"]) for row in ledgers["events.csv"]]
    if event_records != list(range(1, len(event_records) + 1)):
        raise ValueError("not all exported candidate records are linked")
    strict = sum(int(row["strict"]) for row in paired)
    result_text = (ROOT / "RESULT.md").read_text(encoding="utf-8")
    first_tables = [line for line in result_text.split("\n\n")[1:4] if line.startswith("| ")]
    if len(first_tables) != 3 or not close_table(result_text):
        raise ValueError("result tables out of place")
    handoff = ROOT / "HANDOFF.md"
    if handoff.exists() and not close_table(handoff.read_text(encoding="utf-8")):
        raise ValueError("handoff does not end in the three-row table")

    return {
        "sources": {"rows": len(sources), "distinct_work_ids": len({r["work_id"] for r in sources}),
                    "access_counts": dict(Counter(row["access"] for row in sources)),
                    "counted_distinct_works": len(work_ids), "counted_by_category": dict(by_category),
                    "uncredited_rows": len(sources) - len(counted), "empty_required_fields": empty_source_fields,
                    "duplicate_source_ids": len(sources) - len(ids), "sha256": sha256(ledger.read_bytes()).hexdigest()},
        "ledgers": summaries,
        "selection_by_layer": dict(Counter(r["layer"] for r in planned)),
        "planned_placeholders": sum(r["selection_status"] == "미확인" for r in planned),
        "pair_rows_by_layer": dict(Counter(r["layer"] for r in paired)),
        "strict_pairs": strict,
        "questions_present": sorted({q for r in sources for q in r["questions"]}),
        "result_tables_in_required_positions": True,
        "handoff_table_checked": handoff.exists(),
    }


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, sort_keys=True, indent=2))
