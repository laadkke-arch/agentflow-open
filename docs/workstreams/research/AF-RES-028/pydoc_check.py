#!/usr/bin/env python3
"""Distinguish the installed command name from the working pydoc module route."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    rows = []
    for version in ("3.10.1", "3.11.1"):
        base = args.cache / ("python-" + version)
        record = json.loads((base / "build.json").read_text())
        prefix = Path(record["binary"]).parent
        with tempfile.TemporaryDirectory(prefix="af028-pydoc-") as work:
            name = "af_doc_fixture"
            Path(work, name + ".py").write_text('"""AF028DOCSENTINEL"""\n')
            env = {"PATH": str(prefix), "HOME": work, "LC_ALL": "C.UTF-8", "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1"}
            checks = [
                ("pydoc", ["/bin/sh", "-c", "command -v pydoc; pydoc af_doc_fixture"]),
                ("pydoc3", [str(prefix / "pydoc3"), name]),
                ("module", [record["binary"], "-B", "-m", "pydoc", name]),
            ]
            for route, command in checks:
                begin = time.monotonic()
                ran = subprocess.run(command, env=env, cwd=work, capture_output=True, timeout=10)
                rows.append(dict(cell_id="A028-20", route=route, tag=record["tag"], commit=record["commit"], argv=command,
                                 rc=ran.returncode, stdout=ran.stdout.decode(), stderr=ran.stderr.decode(),
                                 stdout_sha256=sha256(ran.stdout).hexdigest(), stderr_sha256=sha256(ran.stderr).hexdigest(),
                                 sentinel=b"AF028DOCSENTINEL" in ran.stdout, env_path=str(prefix),
                                 wall_s=round(time.monotonic() - begin, 4)))
    args.out.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    print([(r["route"], r["tag"], r["rc"], r["sentinel"]) for r in rows])


if __name__ == "__main__":
    main()
