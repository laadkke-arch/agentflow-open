#!/usr/bin/env python3
"""Version gate and optional JN1 reproduction. Never install or download tools."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EXECUTION = ROOT / "execution"
EXPECTED = {"jq": "jq-1.7.1", "pandoc": "pandoc 3.1.11"}
ENVIRONMENT = {"jq": "AF088_JQ_BIN", "pandoc": "AF088_PANDOC_BIN"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def preflight():
    binaries = {}
    for tool in ("jq", "pandoc"):
        requested = os.environ.get(ENVIRONMENT[tool], tool)
        resolved = shutil.which(requested)
        entry = {"requested": requested, "path": resolved, "expected_first_line": EXPECTED[tool], "exact_match": False}
        if resolved:
            binary = Path(resolved).resolve()
            entry.update({"resolved_path": str(binary), "binary_sha256": sha(binary.read_bytes()), "command": [resolved, "--version"]})
            try:
                result = subprocess.run(entry["command"], capture_output=True, text=True, timeout=10)
                first = result.stdout.splitlines()[0] if result.stdout.splitlines() else ""
                entry.update({"exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                              "observed_first_line": first,
                              "exact_match": result.returncode == 0 and first == EXPECTED[tool]})
            except (OSError, subprocess.TimeoutExpired) as error:
                entry["error"] = str(error)
        binaries[tool] = entry
    with (ROOT / "candidates.csv").open(newline="") as handle:
        candidates = list(csv.DictReader(handle))
    references = {row["tool"]: {"tag": row["tag"], "tag_sha": row["tag_sha"]} for row in candidates}
    return {
        "checked_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "reference_contract": references,
        "candidates_csv_sha256": sha((ROOT / "candidates.csv").read_bytes()),
        "binaries": binaries,
        "all_exact_versions": all(item["exact_match"] for item in binaries.values()),
        "conversion_execution": "not_run",
        "installation_or_network_download": "not_attempted",
        "gate_rule": "Exact first version line required; version string alone does not establish original build provenance.",
    }


def run_jn1(report):
    if not report["binaries"]["jq"]["exact_match"]:
        report["conversion_execution"] = "not_run_version_mismatch_or_missing"
        return 2
    relative = "inputs/JN1/R1-weather.json"
    index = json.loads((EXECUTION / "inputs/index.json").read_text())
    entry = next(row for row in index["entries"] if row["path"] == relative)
    path = EXECUTION / relative
    content = path.read_bytes()
    if sha(content) != entry["sha256"]:
        report["error"] = "JN1 extracted input hash mismatch"
        return 3
    original = ROOT / entry["source_path"]
    if sha(original.read_bytes()) != entry["source_sha256"]:
        report["error"] = "JN1 frozen question hash mismatch"
        return 3
    data = json.loads(content)
    programs = [
        ("rain", ".DailyForecasts | map(.Day.RainProbability)", [d["Day"]["RainProbability"] for d in data["DailyForecasts"]]),
        ("air_and_pollen_index_1", ".DailyForecasts | map(.AirAndPollen[1].Value)", [d["AirAndPollen"][1]["Value"] for d in data["DailyForecasts"]]),
    ]
    runs = []
    for label, program, expected in programs:
        command = [report["binaries"]["jq"]["path"], program, str(path)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        try:
            observed = json.loads(result.stdout)
        except json.JSONDecodeError:
            observed = None
        runs.append({"label": label, "command": command, "input_sha256": entry["sha256"],
                     "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                     "expected_from_frozen_input": expected, "observed_json": observed,
                     "matches": result.returncode == 0 and observed == expected})
    report["conversion_execution"] = "JN1_R1_only"
    report["runs"] = runs
    report["scope_limit"] = "Reference-build result on R1 input; does not establish R0 complete input, original user version, or historical user execution."
    return 0 if all(run["matches"] for run in runs) else 1


def main():
    parser = argparse.ArgumentParser()
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--preflight", action="store_true")
    choice.add_argument("--require", choices=("jq", "pandoc"), help="require only the selected exact version; no conversion")
    choice.add_argument("--run-jn1", action="store_true", help="run two JQ-map projections only after the exact jq gate succeeds")
    args = parser.parse_args()
    report = preflight()
    if args.run_jn1:
        code = run_jn1(report)
    elif args.require:
        code = 0 if report["binaries"][args.require]["exact_match"] else 2
    else:
        code = 0 if report["all_exact_versions"] else 2
    report["process_exit_code"] = code
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
