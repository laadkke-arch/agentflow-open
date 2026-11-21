"""Run the same bounded workbench checks in a checkout on any Python 3.12+ host.

The environment label is supplied by the caller, not proof of a cloud account.
This command accepts no shell commands, credentials, or remote execution jobs.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import signal
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def git_state(root):
    result = {"commit": None, "dirty": None}
    try:
        result["commit"] = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
            text=True, timeout=10, check=True).stdout.strip()
        result["dirty"] = bool(subprocess.run(
            ["git", "status", "--porcelain"], cwd=root, capture_output=True,
            text=True, timeout=10, check=True).stdout.strip())
    except (OSError, subprocess.SubprocessError):
        result["error"] = "Git checkout identity could not be read"
    result["clean"] = not result["dirty"] if result["dirty"] is not None else None
    return result


def github_context():
    # Do not copy the event payload or the process environment into public evidence.
    result = {key: os.environ.get(name) for key, name in (
        ("event_name", "GITHUB_EVENT_NAME"), ("event_sha", "GITHUB_SHA"),
        ("run_id", "GITHUB_RUN_ID"), ("run_attempt", "GITHUB_RUN_ATTEMPT"))}
    result.update(pr_head_sha=None, pr_base_sha=None)
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        try:
            path = Path(event_path)
            if path.stat().st_size > 5_000_000:
                raise ValueError("event too large")
            event = json.loads(path.read_text(encoding="utf-8"))
            pr = event.get("pull_request") or {}
            result["pr_head_sha"] = (pr.get("head") or {}).get("sha")
            result["pr_base_sha"] = (pr.get("base") or {}).get("sha")
        except (OSError, ValueError, AttributeError):
            result["metadata_error"] = "GitHub event metadata could not be read"
    return result


def checks(fetch_contract):
    return [
        ("doctor", [sys.executable, "-m", "workbench", "doctor"], 30),
        ("acceptance", [sys.executable, "scripts/check.py", "--require-git"], 420),
        ("research-case", [sys.executable, "-m", "workbench", "run",
                           "reference-audit", "discovery"], 60),
        ("original-smoke", [sys.executable, "workbench/verify.py"], 30),
        ("sessions", [sys.executable, "-m", "workbench.session", "check-all",
                      *(["--fetch"] if fetch_contract else [])], 60),
    ]


def stop_process_tree(proc):
    """Bound test children as well as the entry script, on Linux and Windows."""
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True, timeout=10, check=False)
        except (OSError, subprocess.SubprocessError):
            pass
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if proc.poll() is None:
        proc.kill()


def run_check(root, directory, name, argv, timeout, result):
    env = os.environ.copy()
    env.update(PYTHONPATH=str(root), PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    kwargs = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
              if os.name == "nt" else {"start_new_session": True})
    stdout, stderr, proc = "", "", None
    try:
        proc = subprocess.Popen(argv, cwd=root, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True,
                                encoding="utf-8", errors="replace", **kwargs)
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            result.update(status="passed" if proc.returncode == 0 else "failed",
                          exit_code=proc.returncode)
        except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
            stop_process_tree(proc)
            stdout, stderr = proc.communicate(timeout=10)
            timed_out = isinstance(exc, subprocess.TimeoutExpired)
            result.update(status="timed_out" if timed_out else "interrupted",
                          exit_code=124 if timed_out else 130)
            stderr += "\nCheck timed out.\n" if timed_out else "\nCheck interrupted.\n"
    except (OSError, subprocess.SubprocessError) as exc:
        result.update(status="failed", exit_code=1, error=type(exc).__name__)
        stderr += "\nCould not complete the check: " + type(exc).__name__ + "\n"
    finally:
        if proc is not None and proc.poll() is None:
            stop_process_tree(proc)
            proc.wait(timeout=10)
        result["completed_at"] = now()
        for stream, content in (("stdout", stdout), ("stderr", stderr)):
            path = directory / f"{name}.{stream}.log"
            path.write_text(content, encoding="utf-8")
            result[stream + "_log"] = path.relative_to(root).as_posix()
    print(f"[{name}] {result['status']} (exit {result['exit_code']})", flush=True)
    if stdout:
        print(stdout, end="" if stdout.endswith("\n") else "\n", flush=True)
    if stderr:
        print(stderr, end="" if stderr.endswith("\n") else "\n", file=sys.stderr, flush=True)
    return stdout


def execute(root, environment, fetch_contract=False, require_clean=False):
    root = Path(root).resolve()
    out = root / ".workbench"
    directory = out / "cloud-check-logs" / uuid.uuid4().hex
    directory.mkdir(parents=True)
    path = out / "cloud-check.json"
    receipt = {
        "schema": 1, "scope": "workbench checks, not product or browser integration",
        "environment": environment, "environment_is_caller_label": True,
        "platform": platform.platform(), "python": platform.python_version(),
        "started_at": now(), "completed_at": None, "status": "running",
        "exit_code": None, "source_start": git_state(root), "github": github_context(),
        "contract_fetch_requested": fetch_contract, "require_clean": require_clean, "checks": [],
        "session_validation": {"status": "not-executed", "reason": "not_reached"},
    }
    receipt["github"]["checked_out_sha"] = receipt["source_start"]["commit"]

    def save():
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
        temporary.replace(path)

    save()  # An externally killed runner leaves an incomplete record, never a pass.
    exit_code = 0
    try:
        if require_clean and receipt["source_start"]["clean"] is not True:
            exit_code = 1
            receipt["error"] = "clean_checkout_required_at_start"
        else:
            for name, argv, timeout in checks(fetch_contract):
                result = {"name": name, "command": argv, "timeout_seconds": timeout,
                          "started_at": now(), "status": "running", "exit_code": None}
                receipt["checks"].append(result)
                save()
                stdout = run_check(root, directory, name, argv, timeout, result)
                if name == "sessions":
                    try:
                        receipt["session_validation"] = json.loads(stdout)
                    except ValueError:
                        receipt["session_validation"] = {
                            "status": "failed", "reason": "invalid_checker_output"}
                        if result["exit_code"] == 0:
                            result.update(status="failed", exit_code=1)
                save()
                if result["exit_code"] != 0:
                    exit_code = result["exit_code"] or 1
                    break
    except KeyboardInterrupt:
        exit_code = 130
    except Exception as exc:
        exit_code = 1
        receipt["error"] = type(exc).__name__
    finally:
        receipt.update(completed_at=now(), source_end=git_state(root),
                       status="passed" if exit_code == 0 else "failed", exit_code=exit_code)
        if receipt["source_start"]["commit"] != receipt["source_end"]["commit"]:
            receipt.update(status="failed", exit_code=1, error="checkout_changed_during_checks")
        elif require_clean and receipt["source_end"]["clean"] is not True:
            receipt.update(status="failed", exit_code=1)
            receipt.setdefault("error", "clean_checkout_required_at_end")
        save()
    print("CLOUD_CHECK_RECEIPT=" + str(path), flush=True)
    print("CLOUD_CHECK_RESULT=" + json.dumps({
        "status": receipt["status"], "exit_code": receipt["exit_code"],
        "checked_out_sha": receipt["github"]["checked_out_sha"],
        "require_clean": require_clean,
        "source_start": receipt["source_start"], "source_end": receipt["source_end"],
        "session_validation": receipt["session_validation"]}, ensure_ascii=False), flush=True)
    return receipt["exit_code"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True,
                        help="Descriptive label, e.g. codex-cloud or github-actions-ubuntu")
    parser.add_argument("--fetch-contract", action="store_true",
                        help="Fetch the session integration ref; active checks fail if fetch fails")
    parser.add_argument("--require-clean", action="store_true",
                        help="Fail unless Git reports a clean checkout both before and after checks")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,47}", args.environment):
        parser.error("environment must be a short lowercase label")
    return execute(ROOT, args.environment, args.fetch_contract, args.require_clean)


if __name__ == "__main__":
    raise SystemExit(main())
