#!/usr/bin/env python3
"""Verify frozen bodies and cited boundaries without storing external source text.

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
    parser.add_argument("--source", help="Verify only the selected source ID")
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
        text = body.decode("utf-8")
        lines = text.splitlines(keepends=True)
        checked_sections = []
        for section in row["sections"]:
            start, end = section["line_start"], section["line_end"]
            if not 1 <= start <= end <= len(lines):
                raise RuntimeError(f"Invalid line interval: {row['source_id']}")
            prefix = "".join(lines[: start - 1])
            excerpt = "".join(lines[start - 1 : end])
            expected_bounds = (len(prefix), len(prefix) + len(excerpt), len(prefix.encode("utf-8")), len(prefix.encode("utf-8")) + len(excerpt.encode("utf-8")))
            actual_bounds = tuple(section[key] for key in ("char_start", "char_end", "byte_start", "byte_end"))
            if expected_bounds != actual_bounds:
                raise RuntimeError(f"Section boundaries differ: {row['source_id']}")
            raw_excerpt = body[section["byte_start"] : section["byte_end"]]
            if raw_excerpt != excerpt.encode("utf-8") or hashlib.sha256(raw_excerpt).hexdigest() != section["excerpt_sha256"]:
                raise RuntimeError(f"Section hash differs: {row['source_id']}")
            checked_sections.append({"section": section["section"], "line_start": start, "line_end": end, "excerpt_sha256": section["excerpt_sha256"], "boundaries_verified": True})
        print(json.dumps({"source_id": row["source_id"], "fixed_url": row["fixed_url"], "body_sha256": row["body_sha256"], "verified_body": True, "sections": checked_sections}))


if __name__ == "__main__":
    main()
