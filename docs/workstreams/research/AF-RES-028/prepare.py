#!/usr/bin/env python3
"""Rehydrate the recorded public SSL fixtures and Debian Tk/X11 supplements."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent


def fetch(url, name, expected, folder):
    dest = folder / name
    if not dest.exists():
        partial = dest.with_suffix(dest.suffix + ".part")
        subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location", "--max-time", "45",
                        "--output", str(partial), url], check=True)
        partial.replace(dest)
    if sha256(dest.read_bytes()).hexdigest() != expected:
        raise ValueError(f"SHA-256 mismatch for {url}")
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixtures", required=True, type=Path)
    ap.add_argument("--system", required=True, type=Path)
    args = ap.parse_args()
    for folder in (args.fixtures, args.system):
        folder.mkdir(parents=True, exist_ok=True)
    for row in json.loads((HERE / "probes/fixtures.json").read_text()):
        fetch(row["url"], row["name"], row["sha256"], args.fixtures)
    with tempfile.TemporaryDirectory() as work:
        for row in json.loads((HERE / "receipts/system-archives.json").read_text()):
            package = fetch(row["url"], row["archive"], row["sha256"], Path(work))
            subprocess.run(["dpkg-deb", "-x", str(package), str(args.system)], check=True)


if __name__ == "__main__":
    main()
