"""Represent absence explicitly; preserve the phase-II observations in Git."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    log = {"phase_ii_commit": "b3aa200fce66f0635e74aa39c4cb008cafd86eff", "observation_or_denominator_changed": False, "files": []}
    for path in (ROOT / "frame.csv", ROOT / "versions.csv"):
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            rows = list(reader)
        changes = []
        source_fields = {}
        for row_i, row in enumerate(rows, 2):
            if path.name == "frame.csv":
                source = ROOT / row["source_file"]
                if str(source) not in source_fields:
                    with source.open(newline="") as f:
                        source_fields[str(source)] = set(next(csv.reader(f)))
                applicable = source_fields[str(source)]
            else:
                applicable = set(fields)
            for field in fields:
                if row[field] != "":
                    continue
                reason = "unrecorded applicable field"
                replacement = "미확인"
                if path.name == "frame.csv" and field not in applicable:
                    replacement, reason = "해당 없음", "union-schema field belongs to another collection"
                elif path.name == "frame.csv" and field == "case_id":
                    replacement, reason = "해당 없음", "unselected candidate has no assigned case"
                elif path.name == "frame.csv" and field == "duplicate_of_raw":
                    replacement, reason = "해당 없음", "not recorded as a duplicate"
                elif path.name == "versions.csv" and field in ("reference_period", "vintage_values") and row["case_id"].startswith("N-P"):
                    replacement, reason = "해당 없음", "software manual has no statistical reference period/value vintage sequence"
                row[field] = replacement
                changes.append({"csv_record": row_i, "field": field, "before": "", "after": replacement, "reason": reason})
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
        grouped = {}
        for change in changes:
            group = (change["field"], change["after"], change["reason"])
            grouped.setdefault(group, []).append(change["csv_record"])
        grouped_changes = [{"field":field, "before":"", "after":after, "reason":reason, "csv_records":records} for (field,after,reason),records in grouped.items()]
        log["files"].append({"file": path.name, "before_sha256": before, "after_sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "changed_cells": len(changes), "grouped_changes": grouped_changes})
    (ROOT / "evidence/normalization-log.json").write_text(json.dumps(log,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({r["file"]:r["changed_cells"] for r in log["files"]},ensure_ascii=False))


if __name__ == "__main__":
    main()
