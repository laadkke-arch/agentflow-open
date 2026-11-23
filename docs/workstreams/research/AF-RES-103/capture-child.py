#!/usr/bin/env python3
"""Capture the frozen Lua's child calls, then relay bytes and exit code."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    name = Path(sys.argv[0]).name
    out = Path(os.environ["AF103_CHILD_DIR"])
    seq = len(list(out.glob("*/call.json"))) + 1
    event = out / f"{seq:02d}-{name}"
    event.mkdir()
    args = [os.environ["AF103_REAL_" + name.upper()], *sys.argv[1:]]
    data = sys.stdin.buffer.read()
    (event / "stdin").write_bytes(data)
    if name == "pdflatex":
        shutil.copyfile("diagram.tex", event / "diagram.tex")
    start = datetime.now(timezone.utc)
    try:
        process = subprocess.run(args, input=data, capture_output=True, timeout=90)
        code, stdout, stderr = process.returncode, process.stdout, process.stderr
    except (OSError, subprocess.TimeoutExpired) as exc:
        code, stdout, stderr = 125, b"", str(exc).encode()
    end = datetime.now(timezone.utc)
    if name == "pdflatex":
        for filename in ("diagram.log", "diagram.pdf"):
            if Path(filename).exists():
                shutil.copyfile(filename, event / filename)
    (event / "stdout").write_bytes(stdout)
    (event / "stderr").write_bytes(stderr)
    (event / "call.json").write_text(json.dumps({
        "tool": name, "argv": args, "cwd": str(Path.cwd()), "started_utc": start.isoformat(),
        "finished_utc": end.isoformat(), "exit": code,
    }, indent=2) + "\n")
    sys.stdout.buffer.write(stdout)
    sys.stderr.buffer.write(stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
