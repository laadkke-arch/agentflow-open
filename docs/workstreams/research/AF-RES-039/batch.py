"""Supervise AF-RES-039 packets without passing the grader files to the consumer."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from prepare import ROOT, SEED, sha, storage

ENV_NAMES = {
    "PATH", "LANG", "LC_ALL", "TZ", "SSL_CERT_FILE", "SSL_CERT_DIR", "CURL_CA_BUNDLE",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY",
    "http_proxy", "https_proxy", "all_proxy", "no_proxy",
}
PILOT_REFS = {"R01", "G05"}


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def worker_env(sandbox):
    env = {key: value for key, value in os.environ.items() if key in ENV_NAMES}
    for key in ("HOME", "TMPDIR", "XDG_CACHE_HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME"):
        env[key] = str(sandbox)
    return env


def read_manifest():
    return [json.loads(line) for line in (ROOT / "inputs.jsonl").read_text().splitlines()]


def file_access_audit(log, sandbox):
    """Summarize actual successful opens. Runtime/library/CA files remain visible."""
    count = Counter()
    inputs = set()
    unexpected = set()
    for line in log.read_text(errors="replace").splitlines():
        if not re.search(r'\bopen(?:at2?)?\(', line) or not re.search(r' = \d+(?:<.*>)?$', line):
            continue
        match = re.search(r'"([^"]+)"', line)
        if not match:
            continue
        path = match[1]
        count["successful_opens"] += 1
        if path == str(sandbox):
            continue
        relative = path.removeprefix(str(sandbox) + "/")
        if not relative.startswith("/"):
            if relative in {"replay.py", "store.json"} or relative.startswith("received/"):
                inputs.add(relative)
            elif relative != ".":
                unexpected.add(relative)
        elif path.startswith(("/workspace/", "/tmp/")):
            unexpected.add(path)
    return {
        "audit": "strace open/openat/openat2 successful file opens",
        "successful_opens": count["successful_opens"],
        "packet_and_own_work_files": sorted(inputs),
        "unexpected_workspace_or_tmp_open_paths": sorted(unexpected),
        "os_sandbox": "managed executor; no additional filesystem namespace",
    }


def one(row, packet_bytes, output, phase):
    if sha(packet_bytes) != row["input_sha256"]:
        raise ValueError(f"{row['run_id']} packet pin mismatch")
    with tempfile.TemporaryDirectory(prefix="af039-single-") as scratch:
        sandbox = Path(scratch)
        consumer = sandbox / "replay.py"
        shutil.copyfile(ROOT / "replay.py", consumer)
        (sandbox / "store.json").write_bytes(packet_bytes)
        names = sorted(path.name for path in sandbox.iterdir())
        trace_path = sandbox.with_suffix(".trace")
        task = "boundary" if phase == "boundary" else row["task"]
        worker_args = [sys.executable, "-I", "-B", "replay.py", task]
        trace = shutil.which("strace")
        script_args = ([trace, "-f", "-qq", "-e", "trace=open,openat,openat2", "-o", str(trace_path)]
                       if trace else []) + worker_args
        started_utc, started = utc(), time.monotonic()
        child = subprocess.run(script_args, cwd=sandbox, env=worker_env(sandbox), capture_output=True)
        try:
            audit = file_access_audit(trace_path, sandbox) if trace_path.exists() else {
                "audit": "unavailable", "unexpected_workspace_or_tmp_open_paths": None}
        finally:
            trace_path.unlink(missing_ok=True)
        try:
            result = json.loads(child.stdout)
        except (ValueError, UnicodeDecodeError):
            result = {
                "error": "RUNNER_NO_RECEIPT", "instrumentation": "unknown",
                "stderr_last_line": child.stderr.decode(errors="replace").splitlines()[-1:],
                "logical_gets": None, "http_exchanges": None,
            }
        if (sandbox / "received").exists():
            shutil.move(sandbox / "received", output / row["run_id"])
        result.update(
            phase=phase, event="run", run_id=row["run_id"], order=row["order"],
            pair_index=row["pair_index"], configuration=row["configuration"], ref_id=row["ref_id"],
            task=row["task"], request_task=task, tool_exit_code=child.returncode,
            supervisor_started_utc=started_utc, supervisor_finished_utc=utc(),
            supervisor_elapsed_seconds=round(time.monotonic() - started, 6),
            initial_directory=names, input_expected_sha256=row["input_sha256"],
            replay_sha256=sha(consumer.read_bytes()), worker_command=[Path(sys.executable).name, *worker_args[1:]],
            file_access=audit, application_cache="new process, cwd, home and cache; no carryover",
        )
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("boundary", "main", "replication"))
    parser.add_argument("--capture-dir", type=Path, required=True)
    parser.add_argument("--journal", type=Path, required=True)
    args = parser.parse_args()
    capture_dir = args.capture_dir.resolve()
    capture_dir.mkdir(parents=True, exist_ok=True)
    if list(capture_dir.iterdir()):
        parser.error("capture directory must be empty")
    packets = storage()
    cases = read_manifest()
    if args.phase == "boundary":
        cases = [row for row in cases if row["ref_id"] in PILOT_REFS and row["task"] == "current"]
    elif args.phase == "replication":
        cases = [row for row in cases if row["ref_id"] in PILOT_REFS]
    print(json.dumps({"phase": args.phase, "count": len(cases), "seed": SEED, "started_utc": utc()}), flush=True)
    with args.journal.open("x", encoding="utf-8") as journal:
        for row in cases:
            data = packets[(row["ref_id"], row["configuration"])][1]
            result = one(row, data, capture_dir, args.phase)
            journal.write(json.dumps(result, ensure_ascii=False) + "\n")
            journal.flush()
            print(result["run_id"], result.get("logical_gets"), result.get("http_exchanges"),
                  result["tool_exit_code"], flush=True)
    return int(any(row["tool_exit_code"] for row in map(json.loads, args.journal.read_text().splitlines())))


if __name__ == "__main__":
    sys.exit(main())
