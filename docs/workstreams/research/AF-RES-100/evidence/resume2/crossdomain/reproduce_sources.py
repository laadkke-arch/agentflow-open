#!/usr/bin/env python3
"""Verify frozen bodies and display the cited source sections; no target execution.

Use --refetch to retrieve the manifest's immutable raw URLs again. A changed
body is rejected by SHA256 before replacing its cache entry. No packages are
installed, no source repositories are cloned, and no source code is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refetch", action="store_true")
    parser.add_argument("--source", help="Display only a source ID, while still verifying its body")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    workstream = here.parents[2]
    rows = [json.loads(line) for line in (here / "sources.jsonl").read_text().splitlines() if line.strip()]
    selected = [row for row in rows if not args.source or row["source_id"] == args.source]
    if not selected:
        raise SystemExit("No source matches the supplied ID")
    for row in selected:
        cached = workstream / row["cached_body"]
        if args.refetch:
            request = urllib.request.Request(row["raw_url"], headers={"User-Agent": "AF-RES-100-crossdomain-evidence-replay"})
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
            if hashlib.sha256(body).hexdigest() != row["sha256"]:
                raise RuntimeError(f"Refetched hash differs: {row['source_id']}")
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(body)
        body = cached.read_bytes()
        if hashlib.sha256(body).hexdigest() != row["sha256"]:
            raise RuntimeError(f"Cached hash differs: {row['source_id']}")
        lines = body.decode("utf-8").splitlines()
        for section in row["sections"]:
            print(f"\n{row['source_id']}: {section['section']} ({section['line_start']}-{section['line_end']}, inclusive)")
            for line_number in range(section["line_start"], section["line_end"] + 1):
                print(f"{line_number:5}: {lines[line_number - 1]}")


if __name__ == "__main__":
    main()
