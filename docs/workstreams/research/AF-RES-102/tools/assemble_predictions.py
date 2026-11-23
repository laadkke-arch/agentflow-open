#!/usr/bin/env python3
"""Normalize already selected project ledgers; never fetch outcomes or select cases."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    rows = []
    for folder in ("ggplot2", "matplotlib"):
        p = ROOT / "evidence" / folder
        ed = json.loads((p / "editions.json").read_text())
        oldbase = ed["old"].get("base_url", ed["old"].get("fixed_base_url"))
        for r in csv.DictReader((p / "predictions.csv").open(newline="")):
            vacant = r.get("vacant", r.get("vacancy")) == "True"
            section = r.get("section_path", r.get("old_section_path", ""))
            stratum = {"old_resource_absent": "old_asset_absent",
                       "resource_retained_source_changed": "asset_retained_source_changed"}.get(r["stratum"], r["stratum"])
            rows.append({
                "case_id": r["case_id"], "project": r["project"], "stratum": stratum,
                "slot": r.get("slot", r.get("stratum_rank")),
                "old_version": ed["old"]["version"], "new_version": ed["new"]["version"],
                "old_source_sha": ed["old"]["source_sha"], "new_source_sha": ed["new"]["source_sha"],
                "old_publication_sha": ed["old"]["publication_sha"], "new_publication_sha": ed["new"]["publication_sha"],
                "old_section_path": section, "purpose": r.get("purpose", ""),
                "old_section_url": oldbase + section if section else "",
                "old_resource_path": r.get("old_resource_path", r.get("old_asset_path", "")),
                "source_path": r["source_path"],
                "old_source_blob": r.get("old_source_blob", r.get("source_blob", "")),
                "new_source_blob": r.get("new_source_blob", r.get("new_blob_at_old_source_path", "")),
                "legacy_path_present": r.get("legacy_path_present", r.get("legacy_asset_path_present", "")),
                "source_blob_changed": r.get("source_blob_changed", r.get("corresponding_source_blob_changed", "")),
                "new_page_path_present": r.get("new_page_path_present", r.get("new_body_same_path_present", "")),
                "prediction_U": "미확인" if vacant else r["prediction_U"],
                "prediction_recorded_utc": r["prediction_utc"],
                "vacant": str(vacant), "vacancy_reason": r.get("vacancy_reason", ""),
                "new_provisional_section_url": r.get("new_provisional_section_url", r.get("new_section_provisional_url", "")),
                "new_provisional_resource_url": r.get("new_provisional_resource_url", r.get("new_resource_provisional_url", "")),
                "hash_sha256": r.get("sorting_hash", r.get("hash_sha256", "")),
                "new_body_asset_ci_reads": "0",
                "intentional_blind_spot": r.get("alias_blind_spot", r.get("rule_misses", "")),
                "project_ledger": f"evidence/{folder}/predictions.csv",
                "project_exposure": f"evidence/{folder}/stage2.json",
            })
    assert len(rows) == 12 and len({r["case_id"] for r in rows}) == 12
    with (ROOT / "predictions.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"slots": len(rows), "filled": sum(r["vacant"] == "False" for r in rows),
                      "vacant": sum(r["vacant"] == "True" for r in rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
