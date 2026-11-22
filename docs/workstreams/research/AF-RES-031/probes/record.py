"""Run one stage and retain its byte streams and provenance."""
import argparse
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import subprocess
from time import monotonic


def sha256(path):
    return hashlib.file_digest(path.open("rb"), "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("--target", required=True)
    parser.add_argument("--input", action="append", default=[], type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("command required")
    args.out.mkdir(parents=True, exist_ok=True)
    paths = {kind: args.out / f"{args.id}.{kind}" for kind in ("stdout", "stderr")}
    input_hashes = {str(path): sha256(path) for path in args.input}
    start = datetime.now(UTC)
    tick = monotonic()
    with paths["stdout"].open("wb") as stdout, paths["stderr"].open("wb") as stderr:
        try:
            process = subprocess.run(
                command, cwd=args.cwd, stdout=stdout, stderr=stderr, timeout=args.timeout
            )
            code = process.returncode
        except subprocess.TimeoutExpired:
            stderr.write(b"\nrecord.py: timed out\n")
            code = 124
        except OSError as error:
            stderr.write(f"\nrecord.py: {error}\n".encode())
            code = 127
    receipt = {
        "id": args.id,
        "target": args.target,
        "utc": start.isoformat(),
        "cwd": str(args.cwd),
        "argv": command,
        "inputs_sha256": input_hashes,
        "wall_s": round(monotonic() - tick, 3),
        "exit_code": code,
        "streams": {
            kind: {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for kind, path in paths.items()
        },
    }
    (args.out / f"{args.id}.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"{args.id} exit={code} wall_s={receipt['wall_s']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
