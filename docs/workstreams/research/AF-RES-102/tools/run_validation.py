#!/usr/bin/env python3
"""Run gates on an already-committed clean SHA; persist receipts only afterward."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TASK = Path(__file__).resolve().parents[1]
REPO = TASK.parents[3]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO).decode().strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-sha", required=True)
    args = parser.parse_args()
    if git("rev-parse", "HEAD") != args.expected_sha:
        raise SystemExit("HEAD does not match explicit result SHA")
    if git("status", "--porcelain"):
        raise SystemExit("Start must be clean; do not write receipts before the clean gate")
    commands = [
        ("research_structure", ["python", "-B", "docs/workstreams/research/AF-RES-102/tools/verify.py"], 120),
        ("session_check", ["python", "-B", "-m", "workbench.session", "check", "docs/workstreams/research/AF-RES-102/manifest.json", "--fetch"], 180),
        ("cloud_check", ["python", "-B", "scripts/cloud_check.py", "--environment", "codex-cloud", "--fetch-contract", "--require-clean"], 700),
    ]
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    started = utc()
    for name, command, timeout in commands:
        begin = utc()
        print(json.dumps({"starting": name, "utc": begin, "target_sha": args.expected_sha}), flush=True)
        try:
            proc = subprocess.run(command, cwd=REPO, env=env, capture_output=True, text=True, timeout=timeout)
            record = {"name": name, "command": command, "started_utc": begin, "finished_utc": utc(), "exit_code": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr, "timed_out": False}
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout or b""
            err = exc.stderr or b""
            record = {"name": name, "command": command, "started_utc": begin, "finished_utc": utc(), "exit_code": None, "stdout": out.decode() if isinstance(out, bytes) else out, "stderr": err.decode() if isinstance(err, bytes) else err, "timed_out": True}
        results.append(record)
        print(json.dumps({"completed": name, "exit_code": record["exit_code"], "utc": record["finished_utc"]}), flush=True)
    # All gate commands have now completed at the same clean checked-out SHA.
    end_sha = git("rev-parse", "HEAD")
    end_status = git("status", "--porcelain")
    outdir = TASK / "evidence/validation"
    outdir.mkdir(parents=True, exist_ok=True)
    cloud_path = REPO / ".workbench/cloud-check.json"
    cloud = json.loads(cloud_path.read_text()) if cloud_path.exists() else None
    copied_logs = []
    if cloud is not None:
        shutil.copyfile(cloud_path, outdir / "cloud-check.receipt.json")
        for check in cloud.get("checks", []):
            for key in ("stdout_log", "stderr_log"):
                value = check.get(key)
                if not isinstance(value, str):
                    continue
                path = Path(value)
                if not path.is_absolute():
                    path = REPO / path
                if path.is_file() and path.resolve().is_relative_to((REPO / ".workbench").resolve()):
                    dest = outdir / (check["name"] + "." + key + ".log")
                    shutil.copyfile(path, dest)
                    copied_logs.append({"check": check["name"], "stream_key": key, "original_path": value, "saved_path": str(dest.relative_to(TASK)), "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()})
    for r in results:
        for stream in ["stdout", "stderr"]:
            data = r.pop(stream).encode()
            name = r["name"] + "." + stream + ".txt"
            (outdir / name).write_bytes(data)
            r[stream + "_file"] = "evidence/validation/" + name
            r[stream + "_sha256"] = hashlib.sha256(data).hexdigest()
    receipt = {
        "target_sha": args.expected_sha, "started_utc": started, "finished_utc": utc(),
        "source_end_before_persisting_receipts": {"sha": end_sha, "porcelain": end_status, "clean": not end_status},
        "commands": results,
        "cloud_session_validation": cloud.get("session_validation") if cloud else None,
        "common_log_copies": copied_logs,
        "scope": "Research-file consistency plus explicit repository contract check and repository common checks. No historical example build, browser integration, or human review.",
        "actual_manifest_check": "session_check above is explicit; common check-all discovery may report count0 because this manifest is not in docs/tasks.",
        "passed": all(x["exit_code"] == 0 for x in results) and end_sha == args.expected_sha and not end_status,
        "later_receipt_commits_not_in_test_scope": True,
    }
    (outdir / "run.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"receipt": str((outdir / "run.json").relative_to(REPO)), "target_sha": args.expected_sha, "passed": receipt["passed"], "cloud_sessions": receipt["cloud_session_validation"]}, ensure_ascii=False), flush=True)
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
