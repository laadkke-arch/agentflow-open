"""Join path-only project predictions and verify allocation before outcome access."""
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from assemble_frames import write_csv

ROOT = Path(__file__).resolve().parents[1]
rows = []
checks = []
for name in ["ggplot2", "matplotlib"]:
    base = ROOT / "evidence" / name
    frame = list(csv.DictReader((base / "frame.csv").open()))
    initial = {r["page_path"]: r for r in csv.DictReader((base / "stage1-frame.csv").open())}
    eligible = [r for r in frame if r["eligible"] == "YES"]
    population = Counter(r.get("signal_stratum") or r.get("stratum") for r in eligible)
    for row in frame:
        old = initial[row["page_path"]]
        for key in ["eligible", "exclusion", "old_section_path", "old_resource_path", "purpose_visual", "purpose_api", "hash_sha256"]:
            assert row.get(key, "") == old.get(key, ""), (name, row["page_path"], key)
    local = list(csv.DictReader((base / "predictions.csv").open()))
    assert len(local) == 6
    for stratum in ["A", "M", "G"]:
        candidates = sorted([r for r in eligible if (r.get("signal_stratum") or r.get("stratum")) == stratum],
                            key=lambda r: (r["hash_sha256"], r["old_section_path"]))
        chosen = sorted([r for r in local if r["stratum"] == stratum], key=lambda r: int(r["slot"]))
        assert len(chosen) == 2
        assert [r["old_section_path"] for r in chosen if r["vacant"] == "NO"] == [r["old_section_path"] for r in candidates[:2]]
        assert sum(r["vacant"] == "YES" for r in chosen) == max(0, 2 - len(candidates))
    for row in local:
        row["prediction_recorded_utc"] = row.get("prediction_recorded_utc") or row.get("prediction_utc", "")
        row["new_provisional_section_url"] = row.get("new_provisional_section_url") or row.get("provisional_return_url", "미확인")
        row["new_provisional_resource_url"] = row.get("new_provisional_resource_url") or row.get("provisional_payload_url", "미확인")
        row["tree_evidence_url"] = row.get("tree_evidence_url") or row.get("new_tree_evidence_url", "")
        row["stratum_population"] = population[row["stratum"]]
        row["vacancy_reason"] = row.get("vacancy_reason") or (row.get("limitation", "") if row["vacant"] == "YES" else "")
        row["original_purpose_target"] = row["purpose_visual"]
        row["primary_visual_U_target"] = row.get("primary_visual_U_target") or row["purpose_visual"]
        row["specific_method_target"] = row.get("specific_method_target") or row["purpose_api"]
        row["project_ledger"] = (base / "predictions.csv").relative_to(ROOT).as_posix()
        row["new_body_asset_patch_reads"] = row.get("new_body_asset_patch_reads") or "0"
        assert row["prediction_recorded_utc"]
        if row["vacant"] == "YES":
            assert row["prediction_U"] == "미확인"
        else:
            source = next(r for r in eligible if r["old_section_path"] == row["old_section_path"])
            present = source.get("legacy_path_present") or source.get("new_legacy_asset_present")
            expected = "YES" if present in ["YES", "True", "true"] else "NO" if present in ["NO", "False", "false"] else "미확인"
            assert row["prediction_U"] == expected, (name, row["case_id"], present)
        rows.append(row)
    checks.append({"project": name, "eligible": len(eligible), "population": dict(population),
                   "frozen_stage1_fields_unchanged": True, "hash_selection_correct": True})
assert len(rows) == 12
assert len({r["case_id"] for r in rows}) == 12
actual = [r for r in rows if r["vacant"] == "NO"]
assert len({(r["project"], r["old_section_path"]) for r in actual}) == len(actual)
write_csv(ROOT / "predictions.csv", rows)
out = {"utc": datetime.now(timezone.utc).isoformat(), "checks": checks, "pair_slots": len(rows),
       "filled_pairs": len(actual), "vacancies": len(rows) - len(actual),
       "predictions": dict(Counter(r["prediction_U"] for r in actual)),
       "predictions_sha256": hashlib.sha256((ROOT / "predictions.csv").read_bytes()).hexdigest(),
       "interpretation_limit": "Source-set rule amended after path exposure but before labels; MP purpose abstraction appended after selection but before labels. Original purpose is retained and must also be scored."}
(ROOT / "evidence" / "stage2-root-validation.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out, ensure_ascii=False))
