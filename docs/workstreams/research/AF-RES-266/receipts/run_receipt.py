"""Run an audit command and keep its argv, timing, exit, input hashes and raw streams."""
import argparse
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--input", type=Path, action="append", default=[])
    parser.add_argument("--checked-sha")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[0] == "--" else args.command
    base = str(args.prefix)
    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    stdout, stderr = Path(base + ".stdout.txt"), Path(base + ".stderr.txt")
    inputs = {str(path): sha256(path) for path in args.input}
    started = utc()
    with stdout.open("wb") as output, stderr.open("wb") as error:
        try:
            code = subprocess.run(command, stdout=output, stderr=error, check=False).returncode
        except OSError as exc:
            error.write((str(exc) + "\n").encode())
            code = 127
    receipt = {
        "argv": command, "cwd": os.getcwd(), "checked_commit": args.checked_sha,
        "platform": platform.platform(), "started_utc": started, "finished_utc": utc(),
        "inputs_sha256": inputs, "exit_code": code,
        "stdout_sha256": sha256(stdout), "stderr_sha256": sha256(stderr),
    }
    Path(base + ".run.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
