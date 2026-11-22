#!/usr/bin/env python3
"""Build only the missing Tk extension from the two pinned CPython source trees."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("cache", "system", "out"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for version in ("3.10.1", "3.10.4"):
        base = args.cache.resolve() / f"python-{version}"
        release = json.loads((base / "build.json").read_text())
        src = base / "source" / f"cpython-{release['commit']}"
        path = base / "install/lib/python3.10/lib-dynload/_tkinter.cpython-310-x86_64-linux-gnu.so"
        include = args.system.resolve() / "usr/include"
        command = ["cc", "-O3", "-fPIC", "-shared", "-DWITH_APPINIT=1", f"-I{include / 'tcl8.6'}", f"-I{include}",
                   f"-I{src / 'Include'}", f"-I{src}", "Modules/_tkinter.c", "Modules/tkappinit.c",
                   "-ltk8.6", "-ltcl8.6", "-o", str(path)]
        start = time.monotonic()
        log = args.out / f"tk-{version}.log"
        with log.open("wb") as output:
            proc = subprocess.run(command, cwd=src, stdout=output, stderr=subprocess.STDOUT, timeout=90)
        wall = round(time.monotonic() - start, 4)
        rows.append(dict(tag=release["tag"], commit=release["commit"], cwd=str(src), argv=command,
                         rc=proc.returncode, wall_s=wall, log=log.name, log_sha256=sha(log),
                         ext_sha256=sha(path) if proc.returncode == 0 else None))
    (args.out / "tk-repair.json").write_text(json.dumps(rows, indent=2) + "\n")
    if any(row["rc"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
