#!/usr/bin/env python3
"""Run narrow official CPython tests today, in the corresponding tagged installs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import time

CASES = [
    ("netrc", "3.10.1", "test.test_netrc.NetrcTestCase.test_security"),
    ("netrc", "3.11.2", "test.test_netrc.NetrcTestCase.test_security"),
    ("imap", "3.13.2", "test.test_imaplib.NewIMAPSSLTests.test_ssl_verified"),
    ("venv", "3.13.5", "test.test_venv.BasicTest.test_isolation"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    rows = []
    for name, version, test in CASES:
        folder = args.cache / f"python-{version}"
        record = json.loads((folder / "build.json").read_text())
        src = folder / "source" / f"cpython-{record['commit']}" / "Lib"
        module = src / ("test/" + test.split(".")[1] + ".py")
        cmd = [record["binary"], "-B", "-W", "default", "-m", "unittest", "-v", test]
        with tempfile.TemporaryDirectory(prefix="af028-official-") as work:
            env = {"PATH": "/usr/bin:/bin", "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8",
                   "TZ": "UTC", "PYTHONPATH": str(src.resolve())}
            start = time.monotonic()
            cp = subprocess.run(cmd, env=env, cwd=work, capture_output=True, timeout=20)
        rows.append(dict(contract=name, tag=record["tag"], commit=record["commit"], test=test,
                         command=cmd, source_url=f"https://raw.githubusercontent.com/python/cpython/{record['commit']}/Lib/test/{module.name}",
                         source_sha256=sha256(module.read_bytes()).hexdigest(),
                         rc=cp.returncode, wall_s=round(time.monotonic()-start, 4),
                         stdout_sha256=sha256(cp.stdout).hexdigest(), stderr_sha256=sha256(cp.stderr).hexdigest(),
                         stdout=cp.stdout.decode(), stderr=cp.stderr.decode(), observation="current official test rerun"))
    args.out.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    print([(r["contract"], r["tag"], r["rc"]) for r in rows])


if __name__ == "__main__":
    main()
