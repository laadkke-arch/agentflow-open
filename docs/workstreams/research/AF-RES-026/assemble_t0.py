"""Merge the already frozen family files without changing individual records.

Run from any directory. No network, no outcome data, no source-body copies.
The initial seal receipt is intentionally written separately and is not rebuilt.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAMILIES = ("sqlite", "postgres", "curl")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name in ("initial.jsonl", "frozen-responses.jsonl"):
        lines = []
        for family in FAMILIES:
            source = ROOT / "streams" / family / name
            records = source.read_text(encoding="utf-8").splitlines()
            assert len(records) == 8, (family, name)
            lines.extend(records)
        parsed = [json.loads(line) for line in lines]
        assert len({row["case_id"] for row in parsed}) == 24
        if name == "frozen-responses.jsonl":
            for row in parsed:
                for strategy in ("I", "C", "Q"):
                    assert 0 < len(row[strategy]) <= 300, (row["case_id"], strategy)
        (ROOT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")

    rows, fields = [], []
    for family in FAMILIES:
        with (ROOT / "streams" / family / "frame.csv").open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            for field in reader.fieldnames:
                if field not in fields:
                    fields.append(field)
            rows.extend(reader)
    with (ROOT / "frame.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"cases": 24, "messages": 72, "frame_rows": len(rows),
                      "sha256": {name: digest(ROOT / name) for name in
                                 ("initial.jsonl", "frozen-responses.jsonl", "frame.csv")}}, indent=2))


if __name__ == "__main__":
    main()
