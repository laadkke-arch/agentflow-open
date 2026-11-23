"""Run the prespecified inputs in isolated, hash-checked official releases."""

import argparse
import getpass
import hashlib
import json
import platform
import subprocess
import sys
import time
import urllib.request
import venv
from datetime import datetime, timezone
from pathlib import Path


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_environment(workspace, package, release, version):
    """Install one verified upstream wheel in a new environment per edition."""
    artifact = next(item["distribution"] for item in release["pinned_artifacts"]
                    if item["wheel_metadata_version"] == version)
    wheel = workspace / artifact["filename"]
    if not wheel.exists():
        with urllib.request.urlopen(artifact["url"], timeout=20) as response:
            wheel.write_bytes(response.read())
    assert sha256(wheel) == artifact["sha256"], wheel.name
    prefix = workspace / f"venv-{package}-{version}"
    venv.EnvBuilder(with_pip=True, clear=True).create(prefix)
    python = prefix / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    command = [str(python), "-I", "-m", "pip", "--isolated", "--disable-pip-version-check",
               "install", "--no-index", "--no-deps", str(wheel)]
    result = subprocess.run(command, text=True, capture_output=True, timeout=45, check=False)
    receipt = {"command": command, "returncode": result.returncode, "stdout": result.stdout,
               "stderr": result.stderr, "wheel_url": artifact["url"], "wheel_sha256": sha256(wheel),
               "wheel_bytes": wheel.stat().st_size, "requires_python": artifact["requires_python"]}
    return python, receipt


def read_field(obj, key):
    for name in key.split("."):
        if not isinstance(obj, dict) or name not in obj:
            return {"field_missing": True}
        obj = obj[name]
    return obj


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root, workspace = args.root.resolve(), args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    plan_path, fixture = root / "fixtures/execution-plan.json", root / "fixtures/probe.py"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    release = json.loads((root / "evidence/release-evidence.json").read_text(encoding="utf-8"))["packages"]
    assert tuple(plan["seats"]) == ("CC01", "CC02", "AC01", "AC02")
    assert tuple(plan["seats"]["CC01"]) and len(plan["seats"]) == 4
    environments = {}
    with args.output.open("w", encoding="utf-8") as stream:
        for seat, spec in plan["seats"].items():
            package = spec["package"]
            for axis in ("reference", "exact"):
                edition = spec[axis]
                if edition and (package, edition) not in environments:
                    environments[package, edition] = make_environment(workspace, package, release[package], edition)
                for mode in ("positive", "boundary"):
                    entry = spec[mode]
                    row = {"id": f"{seat}-{axis}-{mode}", "seat_id": seat, "axis": axis, "mode": mode,
                           "package": package, "version": edition, "question_version": spec["question_version"],
                           "actor": getpass.getuser(), "role": "Codex Cloud / isolated wheel probe",
                           "python": platform.python_version(), "platform": platform.platform(),
                           "plan_sha256": sha256(plan_path), "fixture_sha256": sha256(fixture),
                           "input": entry["input"], "expected": entry["expect"], "utc": now(),
                           "user_code": spec["user_code"]}
                    if edition is None:
                        row.update(status="not-run", blocker="No exact official package release tied to the author's successful execution.",
                                   command=None, returncode=None, actual=None)
                    else:
                        python, install = environments[package, edition]
                        command = [str(python), "-I", str(fixture), seat, mode]
                        start = time.monotonic()
                        if install["returncode"] != 0:
                            row.update(status="not-run", blocker="Wheel installation failed", command=command,
                                       returncode=None, actual=None, install=install)
                        else:
                            result = subprocess.run(command, text=True, capture_output=True, timeout=20, check=False)
                            data = json.loads(result.stdout) if result.returncode == 0 else None
                            if data:
                                assert (data["version"], data["package"]) == (edition, package)
                            actual = None if data is None else data["result"]
                            differences = {key: {"expected": value, "observed": read_field(actual, key)}
                                           for key, value in entry["expect"].items()
                                           if read_field(actual, key) != value}
                            row.update(status="ran", command=command, returncode=result.returncode,
                                       actual=actual, different_from_expectation=differences,
                                       stdout=result.stdout, stderr=result.stderr, install=install,
                                       elapsed_ms=round((time.monotonic() - start) * 1000, 2))
                    stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"Recorded {len(plan['seats']) * 4} planned runs to {args.output}")


if __name__ == "__main__":
    main()
