"""Capture the pinned original body of each selected work. Run in a fresh directory."""

import argparse
import gzip
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from source_io import MAX_BODY, retrieve, sha, utc

ROOT = Path(__file__).resolve().parent


def lines(path):
    with Path(path).open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def jsonl(path, rows):
    with Path(path).open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    target = args.output
    target.mkdir(parents=True, exist_ok=False)
    (target / "body").mkdir()
    start, started = time.perf_counter_ns(), utc()
    catalogue = lines(ROOT / "urls.jsonl")

    def capture(row):
        raw, receipt = retrieve(row["url"], MAX_BODY)
        row = {"work_id": row["work_id"], **receipt}
        if raw is not None:
            path = f"body/{row['work_id']}.gz"
            stored = gzip.compress(raw, mtime=0)
            (target / path).write_bytes(stored)
            row.update(body_file=path, stored_bytes=len(stored), stored_sha256=sha(stored))
        return row

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(capture, catalogue))
    jsonl(target / "manifest.jsonl", rows)
    timing = dict(start_utc=started, end_utc=utc(), campaign_wall_ns=time.perf_counter_ns()-start,
                  successful=sum(row["complete"] for row in rows), works=len(rows),
                  requests=sum(row["http_attempts"] for row in rows),
                  retries=sum(row["retries"] for row in rows),
                  body_bytes=sum(row["read_bytes"] for row in rows))
    (target / "timing.json").write_text(json.dumps(timing, indent=2)+"\n")
    print(json.dumps(timing))
    for row in rows:
        print(row["work_id"], row["http_status"], row["read_bytes"], row["error"])
    return 0 if timing["successful"] == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
