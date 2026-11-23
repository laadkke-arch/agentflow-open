"""Combine project ledgers without dropping exclusions or rewriting frozen purposes."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ["ggplot2", "matplotlib"]


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=["1", "2"])
    args = p.parse_args()
    rows = []
    summary = {}
    for project in PROJECTS:
        directory = ROOT / "evidence" / project
        filename = "stage1-frame.csv" if args.stage == "1" else "frame.csv"
        path = directory / filename
        local = list(csv.DictReader(path.open(encoding="utf-8")))
        for row in local:
            row["project_frame"] = path.relative_to(ROOT).as_posix()
        eligible = [row for row in local if row.get("eligible") == "YES"]
        for row in eligible:
            text = "AF106|" + row["project"] + "|" + row["old_section_path"]
            assert row["hash_sha256"] == hashlib.sha256(text.encode()).hexdigest(), row["page_path"]
            assert row["purpose_visual"] and row["purpose_api"], row["page_path"]
        summary[project] = {"rows": len(local), "eligible": len(eligible),
                            "excluded": len(local) - len(eligible),
                            "exclusion_counts": dict(Counter(row["exclusion"] for row in local if row["eligible"] != "YES")),
                            "asset_kinds": dict(Counter(row["asset_kind"] for row in eligible)),
                            "source_frame_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        rows.extend(local)
    write_csv(ROOT / "frame.csv", rows)
    summary["total"] = {"rows": len(rows), "eligible": sum(row["eligible"] == "YES" for row in rows),
                        "unique_project_paths": len({(row["project"], row["page_path"]) for row in rows})}
    (ROOT / "evidence" / ("stage" + args.stage + "-frame-summary.json")).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
