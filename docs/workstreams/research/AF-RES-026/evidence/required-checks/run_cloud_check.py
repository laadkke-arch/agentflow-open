#!/usr/bin/env python3
"""Run the unchanged common checker in a disposable, owned-path Git clone.

Example from the repository root:
PYTHONDONTWRITEBYTECODE=1 python \
  docs/workstreams/research/AF-RES-026/evidence/required-checks/run_cloud_check.py \
  --commit ed14e806a5a7bf4e6195fd12024c482d31768449

The source checkout is read only. The clone's origin is the public GitHub repo.
The common scripts are not changed, gates are not suppressed, and failed logs
are retained. Only this wrapper's fresh temporary directory is removed.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import uuid


OWNED = Path(__file__).resolve().parents[2]
SOURCE = OWNED.parents[3]
PUBLIC_ORIGIN = "https://github.com/laadkke-arch/agentflow-open.git"


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(path):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, check=True,
                          capture_output=True, text=True, timeout=10).stdout.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--remote-clone", action="store_true",
                        help="obtain all objects directly from public GitHub instead of copying local objects")
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        parser.error("--commit requires the complete 40-character commit SHA")
    if git_head(SOURCE) != args.commit:
        parser.error("source HEAD differs from the requested reviewed commit")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = Path(__file__).resolve().parent / run_id
    output.mkdir()
    temporary = Path(tempfile.mkdtemp(prefix="cloud-check-temp-", dir=OWNED / "evidence"))
    checkout = temporary / "checkout"
    temp_files = temporary / "tmp"
    temp_files.mkdir()
    env = os.environ.copy()
    env.update(TMPDIR=str(temp_files), PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1",
               GIT_TERMINAL_PROMPT="0")
    command = [sys.executable, "scripts/cloud_check.py", "--environment", "chatgpt-web-pro", "--fetch-contract"]
    receipt = {
        "schema": 1, "started_utc": now(), "completed_utc": None,
        "requested_commit": args.commit, "source_checkout_head_before": git_head(SOURCE),
        "clone_method": "unfiltered_public_remote" if args.remote_clone else "independent_local_copy",
        "source_checkout_head_after": None, "checker_checkout_head_start": None,
        "checker_checkout_head_end": None, "checker_origin": PUBLIC_ORIGIN,
        "checker_command": command, "checker_cwd": str(checkout),
        "wrapper_command": [sys.executable, *sys.argv],
        "environment_overrides": {k: env[k] for k in ("TMPDIR", "PYTHONDONTWRITEBYTECODE", "PYTHONUTF8", "GIT_TERMINAL_PROMPT")},
        "common_code_modified": False, "timeout_seconds": 570,
        "status": "preparing", "exit_code": None, "checker_status": None,
        "copied_artifacts": [], "temporary_path": str(temporary), "temporary_removed": False,
        "limitations": "Common workbench checks, not proof of research source truth or strategy effects. Source checkout HEAD is recorded separately from the tested clone.",
    }
    receipt_path = output / "run-receipt.json"

    def save():
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def prepare(argv, cwd):
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=45)
        with (output / "preparation.log").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"utc": now(), "command": argv, "cwd": str(cwd), "exit_code": result.returncode}) + "\n")
            stream.write(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError("preparation command failed; see preparation.log")

    save()
    print("COMMON_CHECK_OUTPUT=" + str(output), flush=True)
    result_code = 1
    try:
        # --no-hardlinks produces an independent object store. No worktree is
        # registered in the source checkout and no source Git metadata changes.
        clone_source = PUBLIC_ORIGIN if args.remote_clone else str(SOURCE)
        prepare(["git", "clone", "--quiet", "--no-hardlinks", "--no-checkout", clone_source, str(checkout)], SOURCE)
        prepare(["git", "checkout", "--quiet", "--detach", args.commit], checkout)
        prepare(["git", "remote", "set-url", "origin", PUBLIC_ORIGIN], checkout)
        receipt["checker_checkout_head_start"] = git_head(checkout)
        receipt["common_script_sha256"] = {
            name: digest(checkout / name)
            for name in ("scripts/cloud_check.py", "scripts/check.py", "scripts/acceptance.py", "workbench/session.py")
        }
        receipt["checker_started_utc"] = now()
        receipt["status"] = "running"
        save()
        print("COMMON_CHECK_STARTED=" + receipt["checker_started_utc"], flush=True)
        with (output / "stdout.log").open("w", encoding="utf-8") as stdout, (output / "stderr.log").open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(command, cwd=checkout, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                result_code = process.wait(timeout=570)
            except subprocess.TimeoutExpired:
                receipt["outer_timeout"] = True
                # cloud_check handles KeyboardInterrupt by killing its current
                # check's separate process group and saving a failed receipt.
                os.killpg(process.pid, signal.SIGINT)
                try:
                    process.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
                result_code = 124
        receipt["checker_completed_utc"] = now()
        receipt["checker_checkout_head_end"] = git_head(checkout)
        receipt["common_script_sha256_after"] = {name: digest(checkout / name) for name in receipt["common_script_sha256"]}
        if receipt["common_script_sha256_after"] != receipt["common_script_sha256"]:
            receipt["common_code_modified"] = True
            result_code = 1
        if receipt["checker_checkout_head_start"] != args.commit or receipt["checker_checkout_head_end"] != args.commit:
            receipt["checkout_identity_error"] = True
            result_code = 1
    except Exception as exc:
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)}
        result_code = 1
    finally:
        if checkout.is_dir():
            workbench = checkout / ".workbench"
            patterns = ["cloud-check.json", "acceptance.json", "check-*.log",
                        "cloud-check-logs/*/*.log", "runs/*/*/receipt.json",
                        "runs/*/*/stdout.txt", "runs/*/*/stderr.txt"]
            artifacts = sorted({path for pattern in patterns for path in workbench.glob(pattern) if path.is_file()})
            for path in artifacts:
                relative = path.relative_to(workbench)
                destination = output / "checker-artifacts" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if path.stat().st_size > 2_000_000:
                    receipt.setdefault("oversize_artifacts_not_copied", []).append(relative.as_posix())
                    continue
                shutil.copyfile(path, destination)
                receipt["copied_artifacts"].append({"source_relative_path": ".workbench/" + relative.as_posix(),
                                                    "saved_as": destination.relative_to(output).as_posix(),
                                                    "bytes": destination.stat().st_size, "sha256": digest(destination)})
            common_receipt = workbench / "cloud-check.json"
            if common_receipt.exists():
                common = json.loads(common_receipt.read_text(encoding="utf-8"))
                receipt["checker_status"] = common.get("status")
                receipt["checker_exit_code"] = common.get("exit_code")
                receipt["session_validation"] = common.get("session_validation")
                if common.get("status") != "passed" and result_code == 0:
                    result_code = 1
            if (workbench / "source.bundle").exists():
                receipt["bundle_not_retained"] = {"bytes": (workbench / "source.bundle").stat().st_size,
                                                  "reason": "Acceptance records the bundle digest; the large bundle is not a final artifact."}
        receipt["source_checkout_head_after"] = git_head(SOURCE)
        receipt["exit_code"] = result_code
        receipt["status"] = "passed" if result_code == 0 else "failed"
        receipt["completed_utc"] = now()
        save()  # Keep the evidence even if temporary cleanup fails.
        if temporary.is_relative_to(OWNED / "evidence") and temporary.name.startswith("cloud-check-temp-"):
            shutil.rmtree(temporary)
            receipt["temporary_removed"] = not temporary.exists()
            save()
    print("COMMON_CHECK_RESULT=" + json.dumps({"status": receipt["status"], "exit_code": result_code,
                                              "checker_status": receipt["checker_status"],
                                              "receipt": str(receipt_path), "temporary_removed": receipt["temporary_removed"]}), flush=True)
    return result_code


if __name__ == "__main__":
    raise SystemExit(main())
