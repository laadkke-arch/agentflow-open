#!/usr/bin/env python3
"""Check the assembled ledger against original records; never print source prose."""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parent.parent
ORIGINAL = ["evidence/jq/sources.jsonl", "evidence/pandoc/sources.jsonl",
            "evidence/jq/sources-note.jsonl", "evidence/pandoc/sources-note.jsonl",
            "evidence/crossdomain/sources.jsonl"]
ADDITIONAL = ["evidence/post-jq/source-note.jsonl", "evidence/post-pandoc/sources-note.jsonl",
              "evidence/intake/sources-note.jsonl"]
BUCKET = {"main_official_manual_implementation": "main_manual_implementation",
          "adjacent_official_manual_implementation": "adjacent_manual_implementation"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x]


def run():
    errors = []
    original_map = {(f, i): x for f in ORIGINAL for i, x in enumerate(rows(BASE / f), 1)}
    additional_map = {(f, i): x for f in ADDITIONAL for i, x in enumerate(rows(BASE / f), 1)}
    inputs = {**original_map, **additional_map}
    unified_path = BASE / "sources.jsonl"
    unified = rows(unified_path)
    baseline = json.loads((HERE / "source-count-normalized.json").read_text())
    baseline_eligible = {x["source_id"]: x for x in baseline if x["eligible"]}
    source_inputs_changed = []
    original_audit = json.loads((HERE / "source-count-audit.json").read_text())
    for item in original_audit["input_ledgers"]:
        if sha((BASE / item["path"]).read_bytes()) != item["sha256"]:
            source_inputs_changed.append(item["path"])
    if source_inputs_changed:
        errors.append({"check": "original_ledger_changed_after_independent_count", "paths": source_inputs_changed})
    seen = collections.Counter()
    eligible_seen = {}
    checks = []
    for row in unified:
        key = (row["original_note_file"], row["original_note_line"])
        seen[key] += 1
        matches = key in inputs and row["original_note"] == inputs[key]
        if not matches:
            errors.append({"check": "original_note_provenance", "source_id": row["source_id"], "key": key})
        eligible = row["minimum_count_eligible"]
        if key in additional_map and eligible:
            errors.append({"check": "post_or_intake_in_minimum", "source_id": row["source_id"]})
        if eligible:
            sid = row["source_id"]
            if sid in eligible_seen:
                errors.append({"check": "duplicate_eligible_source_id", "source_id": sid})
            eligible_seen[sid] = row
            old = baseline_eligible.get(sid)
            if old is None:
                errors.append({"check": "new_eligible_id", "source_id": sid})
            else:
                expected = BUCKET.get(old["count_bucket"], old["count_bucket"])
                if row["minimum_category"] != expected:
                    errors.append({"check": "eligible_category_changed", "source_id": sid,
                                   "expected": expected, "actual": row["minimum_category"]})
                if row["body_sha256"] != old["source_sha256"]:
                    errors.append({"check": "eligible_hash_changed", "source_id": sid})
                if row["original_url"] != old["original_url"]:
                    errors.append({"check": "eligible_original_url_changed", "source_id": sid})
        checks.append({"source_id": row["source_id"], "original_note_file": key[0],
                       "original_note_line": key[1], "original_note_exact": matches,
                       "minimum_count_eligible": eligible, "category": row["minimum_category"]})
    missing = sorted(set(inputs) - set(seen))
    duplicate = [key for key, number in seen.items() if number != 1]
    if missing:
        errors.append({"check": "missing_original_records", "keys": missing})
    if duplicate:
        errors.append({"check": "duplicated_original_records", "keys": duplicate})
    if set(eligible_seen) != set(baseline_eligible):
        errors.append({"check": "eligible_set_mismatch", "missing": sorted(set(baseline_eligible)-set(eligible_seen)),
                       "extra": sorted(set(eligible_seen)-set(baseline_eligible))})
    identity_groups = collections.defaultdict(list)
    for row in eligible_seen.values():
        identity_groups[row["independent_source_key"]].append(row["source_id"])
    duplicates = {key: ids for key, ids in identity_groups.items() if len(ids) > 1}
    if duplicates:
        errors.append({"check": "unified_identity_duplicate", "groups": duplicates})
    counts = dict(sorted(collections.Counter(x["minimum_category"] for x in eligible_seen.values()).items()))
    result = {"audit": "unified-source-v2", "observed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "source_file_sha256": sha(unified_path.read_bytes()), "observed_rows": len(unified),
              "original_ledger_rows": len(original_map), "additional_ledger_rows": len(additional_map),
              "post_ledger_rows": sum(k[0].startswith("evidence/post-") for k in additional_map),
              "intake_ledger_rows": sum(k[0].startswith("evidence/intake/") for k in additional_map),
              "counted_rows": len(eligible_seen), "baseline_counted_rows": len(baseline_eligible),
              "eligible_categories": counts, "eligible_identity_duplicate_groups": duplicates,
              "embedded_original_records_checked": len(checks),
              "post_or_intake_minimum_contribution": sum(row["minimum_count_eligible"] for row in unified
                                                        if row["original_note_file"] in ADDITIONAL),
              "original_ledger_changes": source_inputs_changed,
              "checks": checks, "errors": errors, "error_count": len(errors),
              "status": "PASS" if not errors else "FAIL",
              "first_observation_retained": "unified-source-audit-initial.json",
              "first_observation_correction": "Initial checker was constructed after a 109-row inspection; concurrent assembly completed 168 rows before it ran. Its 59 extra-record flags were auditor-scope errors for authorized post49/intake10 rows. Original109 provenance and eligible46 already matched. No source changes were made to resolve them.",
              "post_outcome_prose_read_by_model": False,
              "limit": "Exact normalization/provenance/hash/category verification; does not independently endorse the truth of post-outcome prose or regrade primary judgments."}
    (HERE / "unified-source-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ["status", "error_count", "observed_rows", "original_ledger_rows",
                                          "post_ledger_rows", "intake_ledger_rows", "counted_rows",
                                          "eligible_categories", "post_or_intake_minimum_contribution", "errors"]}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(run())
