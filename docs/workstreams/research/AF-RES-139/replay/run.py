"""Install each frozen release in a fresh npm directory and call its public package name."""
import argparse
import concurrent.futures
import json
import os
import resource
import shutil
import subprocess
import time
from pathlib import Path

from common import ROOT, json_in, read_csv, sha, utc, write_json, write_jsonl


def measure(argv, cwd, env, timeout):
    start = time.perf_counter()
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    started_utc = utc()
    stdout, stderr, returncode = "", "", None
    try:
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout, check=False)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b"").decode(errors="replace")
        stderr = f"{(exc.stderr or b'').decode(errors='replace')}\n{exc}"
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    receipt = {"command": argv, "cwd": str(cwd), "started_utc": started_utc, "finished_utc": utc(),
               "exit": returncode, "stderr": stderr, "stdout_bytes": len(stdout.encode()),
               "wall_ms": (time.perf_counter() - start) * 1000,
               "cpu_user_ms": (after.ru_utime - usage.ru_utime) * 1000,
               "cpu_sys_ms": (after.ru_stime - usage.ru_stime) * 1000}
    return stdout, receipt


def run_version(task):
    cohort, directory, cache, release, lock_data = task
    version = release["version"]
    path = directory / version
    path.mkdir()
    env = os.environ | {"LANG": "C.UTF-8", "TZ": "UTC", "npm_config_cache": str(cache), "npm_config_update_notifier": "false"}
    write_json(path / "package.json", lock_data["package_json"])
    write_json(path / "package-lock.json", lock_data["lock"])
    for name in ("probe.cjs", "resolve.mjs"):
        shutil.copyfile(ROOT / "replay" / name, path / name)
    input_path = ROOT / "replay/inputs.json"
    initial_lock = sha((path / "package-lock.json").read_bytes())
    row = {"run_id": cohort + "-" + version, "cohort": cohort, "intended_version": version,
           "launch_path": str(path), "npm_cache": str(cache), "lock_origin": "current npm 11.9.0 frozen v3",
           "lock_before": initial_lock, "distribution": release["tarball_url"], "archive_sha256": release["archive_sha256"]}
    if initial_lock != lock_data["lock_sha256"]:
        return row | {"status": "lock_serialization_mismatch", "expected": lock_data["lock_sha256"]}
    stdout, install = measure(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"], path, env, 90)
    row["install"] = install | {"stdout": stdout}
    row["lock_after_install"] = sha((path / "package-lock.json").read_bytes())
    if install["exit"] != 0:
        return row | {"status": "install_error"}
    stdout, receipt = measure(["node", "probe.cjs", str(input_path)], path, env, 12)
    row["node_process"] = receipt
    try:
        result = json.loads(stdout)
    except json.JSONDecodeError:
        return row | {"status": "probe_error", "node_stdout": stdout}
    if result["status"] != "ok":
        return row | result
    observed = {
        "package": result["package"] == "simple-statistics", "version": result["version"] == version,
        "entry": result["entry_relative"] == release["entry"], "entry_bytes": result["entry_sha256"] == release["entry_sha256"],
        "lock": result["lock_sha256"] == row["lock_after_install"] == initial_lock,
        "direct": result["direct"] == lock_data["direct"], "runtime": result["runtime"] == str(CONTROL["node"]),
    }
    return row | result | {"verifications": observed, "status": "ok" if all(observed.values()) else "provenance_mismatch"}


CONTROL = json_in(ROOT / "replay/inputs.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort", required=True)
    for name in ("folder", "cache", "output"):
        parser.add_argument("--" + name, required=True, type=lambda value: Path(value).resolve())
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    assert subprocess.check_output(["node", "--version"], text=True).strip() == CONTROL["node"]
    assert subprocess.check_output(["npm", "--version"], text=True).strip() == CONTROL["npm"]
    args.folder.mkdir()
    args.cache.mkdir()
    rows = [row for row in read_csv(ROOT / "releases.csv") if row["status"] == "included"]
    locks = json_in(ROOT / "replay/locks.json")["versions"]
    tasks = [(args.cohort, args.folder, args.cache, row, locks[row["version"]]) for row in rows]
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(run_version, tasks))
    write_jsonl(args.output, records)
    print(f"{args.cohort}: {sum(record['status'] == 'ok' for record in records)}/{len(records)} public runtime releases")
    for record in records:
        if record["status"] != "ok":
            print(record["run_id"], record["status"], record.get("verifications", {}))


if __name__ == "__main__":
    main()
