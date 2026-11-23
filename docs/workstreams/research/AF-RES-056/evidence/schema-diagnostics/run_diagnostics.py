"""Run only the fixed, post-ranking diagnostic fixtures in selected-cases.json.

This is not a full JSON Schema Test Suite runner and cannot certify a product.
No remote references, package installation, or candidate ranking occurs here.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import importlib.metadata
import inspect
import json
import platform
from pathlib import Path
import sys

import jsonschema


HERE = Path(__file__).resolve().parent
INPUT = HERE / "selected-cases.json"
OUTPUT = HERE / "runtime-receipt.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    raw = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = []
    for case in raw["cases"]:
        cls = getattr(jsonschema, case["validator_class"])
        cls.check_schema(case["schema"])
        instance = copy.deepcopy(case["instance"])
        before = copy.deepcopy(instance)
        kwargs = {}
        if case["format_checker"]:
            kwargs["format_checker"] = jsonschema.FormatChecker()
        validator = cls(copy.deepcopy(case["schema"]), **kwargs)
        errors = list(validator.iter_errors(instance))
        observed_valid = not errors
        checked = case["check_suite_expectation"]
        rows.append({
            "id": case["id"],
            "fixture_source_url": case["fixture_source_url"],
            "suite_sha": case["suite_sha"],
            "case_pointer": case["case_pointer"],
            "validator_class": case["validator_class"],
            "format_checker": case["format_checker"],
            "schema": case["schema"],
            "input_before": before,
            "input_after": instance,
            "instance_mutated": before != instance,
            "suite_expected_valid": case["suite_expected_valid"],
            "suite_expectation_applied": checked,
            "observed_valid": observed_valid,
            "matches_fixture_expectation": observed_valid == case["suite_expected_valid"] if checked else None,
            "errors": [{"validator": e.validator, "message": e.message,
                        "instance_path": list(e.absolute_path),
                        "schema_path": list(e.absolute_schema_path)} for e in errors],
            "main_trial": False,
            "budget": case["budget"],
        })
    mismatches = sum(r["matches_fixture_expectation"] is False for r in rows)
    versions = {name: importlib.metadata.version(name) for name in ("jsonschema", "referencing", "jsonschema-specifications")}
    package_sources = {}
    for module in (jsonschema, jsonschema.validators, jsonschema._keywords):
        path = Path(inspect.getfile(module))
        package_sources[module.__name__] = {"path": str(path), "sha256": sha256(path)}
    result = {
        "status": "executed diagnostic only",
        "command": "python -B docs/workstreams/research/AF-RES-056/evidence/schema-diagnostics/run_diagnostics.py",
        "utc_started": started,
        "utc_finished": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "executable": sys.executable,
        "python_version": platform.python_version(),
        "packages": versions,
        "package_source_hashes": package_sources,
        "input_sha256": sha256(INPUT),
        "script_sha256": sha256(Path(__file__)),
        "fixed_doc_version": "python-jsonschema 4.23.0@cfe8a4071672b9652c8f083faed1c4ffa7d67705",
        "version_guard": "Installed runtime version is recorded above; this execution is not evidence that v4.23.0 itself passed.",
        "suite_cases_executed": len(rows),
        "suite_expectation_cases": sum(r["suite_expectation_applied"] for r in rows),
        "format_profile_controls": sum(not r["suite_expectation_applied"] for r in rows),
        "fixture_mismatches": mismatches,
        "scope": "Only these inputs/options on this local package build. No complete-suite or historical-version conformance claim; no main L/V success.",
        "rows": rows,
        "exit_code": 1 if mismatches else 0,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("utc_started", "utc_finished", "packages", "suite_cases_executed", "suite_expectation_cases", "format_profile_controls", "fixture_mismatches", "exit_code")}, ensure_ascii=False))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
