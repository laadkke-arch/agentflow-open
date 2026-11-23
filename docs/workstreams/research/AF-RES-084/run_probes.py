"""Run new prespecified probes and point to prior and author observations."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PRIOR = "152f5261ab9a35ab675ab003931ac4dc89966b55:docs/workstreams/research/AF-RES-080"
MODES = ("positive", "boundary")


def utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(text):
    return [json.loads(line) for line in text.splitlines() if line]


def read_prior(name):
    return subprocess.check_output(["git", "show", f"{PRIOR}/{name}"], cwd=ROOT, text=True)


def differences(expected, observed, prefix=""):
    if isinstance(expected, dict) and isinstance(observed, dict):
        mismatches = []
        for key, value in expected.items():
            qualified = f"{prefix}.{key}" if prefix else key
            if key not in observed:
                mismatches.append({"field": qualified, "expected": value, "missing": True})
            else:
                mismatches.extend(differences(value, observed[key], qualified))
        return mismatches
    if type(expected) is not type(observed) or expected != observed:
        return [{"field": prefix, "expected": expected, "observed": observed}]
    return []


def prepare(work, wheel, runtime, expected_python):
    command = [str(runtime), "-I", "-c", "import platform; print(platform.python_version())"]
    if subprocess.check_output(command, text=True).strip() != expected_python:
        raise SystemExit(f"Wrong interpreter for Python {expected_python}: {runtime}")
    staging = work / "wheels"
    artifact = staging / wheel["name"]
    staging.mkdir(parents=True, exist_ok=True)
    if not artifact.exists() or sha(artifact) != wheel["sha256"]:
        partial = artifact.with_suffix(".part")
        subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                        "--max-time", "45", wheel["url"], "-o", str(partial)], check=True)
        if partial.stat().st_size != wheel["size"] or sha(partial) != wheel["sha256"]:
            raise SystemExit(f"Artifact does not match pinned metadata: {wheel['name']}")
        partial.replace(artifact)
    env = dict(os.environ, UV_CACHE_DIR=str(work / "uv-cache"))
    venv = work / f"{artifact.stem}-{expected_python}"
    venv_cmd = ["uv", "venv", "--clear", "--python", str(runtime), str(venv)]
    subprocess.run(venv_cmd, env=env, check=True)
    python = venv / "bin" / "python"
    install = ["uv", "pip", "install", "--no-index", "--no-deps", "--python",
               str(python), str(artifact)]
    subprocess.run(install, env=env, check=True)
    return python, artifact, install


def run_new(plan, pins, runtimes, work):
    plan_digest = sha(ROOT / "fixtures/plan.json")
    fixture = ROOT / "fixtures/probe.py"
    fixture_digest = sha(fixture)
    for edition in plan["matrix"]:
        case, role = edition["case"], edition["role"]
        pin = pins[f"{edition['package']}=={edition['version']}"]
        runtime = runtimes[edition["python"]]
        python, artifact, install = prepare(work, pin["file"], runtime, edition["python"])
        for mode in MODES:
            expected = plan["cases"][case][mode]
            command = [str(python), "-I", str(fixture), case, mode]
            result = subprocess.run(command, capture_output=True, text=True, timeout=25)
            observed = json.loads(result.stdout) if result.returncode == 0 else {}
            fingerprint = {k: observed.get(k) for k in ("implementation", "platform", "python", "version", "package")}
            fingerprint.update(python_executable_sha256=sha(python.resolve()),
                               wheel_sha256=sha(artifact), wheel_url=pin["file"]["url"],
                               tag_commit=pin["tag_commit"])
            mismatches = differences(expected["expect"], observed.get("observed", {}))
            if result.returncode == 0:
                mismatches.extend(differences(
                    {k: edition[k] for k in ("python", "version", "package")}, observed))
            yield {
                "id": f"{case}-{role}-{mode}", **edition, "mode": mode, "actor": "AF-RES-084",
                "record_source": "new", "status": "ran", "utc": utc(), "input": expected["input"],
                "expected": expected["expect"], "observed": observed.get("observed"),
                "process_exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                "expectation_matches": result.returncode == 0 and not mismatches,
                "mismatches": mismatches, "environment": fingerprint, "plan_sha256": plan_digest,
                "fixture_sha256": fixture_digest, "command": command, "install_command": install,
            }


def prior_runs(plan):
    previous = {row["id"]: row for row in read_jsonl(read_prior("runs.jsonl"))}
    for case, ids in plan["inherited_reference"].items():
        for run_id in ids:
            row = previous[run_id]
            assert row["seat_id"] == case and row["status"] == "ran" and row["axis"] == "reference"
            # Preserve previous observables and exits with the original authorship.
            yield {
                "id": run_id, "case": case, "mode": row["mode"], "role": "inherited-reference",
                "actor": "AF-RES-080", "record_source": "inherited", "status": "ran-in-080",
                "source": f"{PRIOR}/runs.jsonl", "utc": row["utc"], "input": row["input"],
                "package": row["package"], "version": row["version"], "python": row["python"],
                "expected": row["expected"], "observed": row["actual"], "stdout": row["stdout"],
                "stderr": row["stderr"], "process_exit": row["returncode"],
                "environment": {"platform": row["platform"], "wheel_sha256": row["install"]["wheel_sha256"]},
                "plan_sha256": row["plan_sha256"], "fixture_sha256": row["fixture_sha256"],
            }


def remaining_runs(plan):
    versions = {row["case"]: row for row in read_jsonl((ROOT / "versions.jsonl").read_text())}
    for case, why in plan["exact_not_run"].items():
        for mode in MODES:
            row = plan["cases"][case][mode]
            yield {"id": f"{case}-exact-{mode}", "case": case, "mode": mode, "role": "exact",
                   "record_source": "planned", "actor": None, "status": "not-run",
                   "version": None, "python": None, "process_exit": None, "observed": None,
                   "input": row["input"], "expected": row["expect"], "reason": why}
    for case, row in versions.items():
        question = row["question"]
        yield {"id": f"{case}-author-question", "case": case, "mode": "report", "role": "author-question",
               "record_source": "author", "status": question["status"], "actor": question["actor"],
               "version": question["version"], "python": question["python"], "process_exit": None,
               "observed": question["output"], "function": question["function"],
               "source_id": question["source_id"]}
        success = row["success"]
        if success["source_id"]:
            yield {"id": f"{case}-author-followup", "case": case, "mode": "report", "role": "author-followup",
                   "record_source": "author", "status": success["status"], "actor": success["actor"],
                   "version": success["version"], "python": success["python"], "function": success["function"],
                   "process_exit": success["exit_code"], "observed": success["stdout"],
                   "source_id": success["source_id"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", action="append", default=[], metavar="VERSION=PATH")
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    runtimes = dict(item.split("=", 1) for item in args.python)
    runtimes = {key: Path(path).absolute() for key, path in runtimes.items()}
    runtimes.setdefault("3.12.14", Path(sys.executable))
    plan = json.loads((ROOT / "fixtures/plan.json").read_text())
    pins = json.loads((ROOT / "fixtures/wheels.json").read_text())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    failed = False
    with args.out.open("w", encoding="utf-8") as handle:
        for group in (prior_runs(plan), remaining_runs(plan), run_new(plan, pins, runtimes, args.work.absolute())):
            for row in group:
                handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
                handle.flush()
                if row["record_source"] == "new":
                    matched = row["expectation_matches"]
                    failed = failed or not matched
                    print(row["id"], "matched" if matched else json.dumps(row["mismatches"], ensure_ascii=False))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
