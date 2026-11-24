"""Take a bounded sample of public responses and local parsing/storage cost."""
from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import sqlite3
from statistics import median
import subprocess
from tempfile import TemporaryDirectory
from time import perf_counter_ns
import xml.etree.ElementTree as ET

CF = "https://raw.githubusercontent.com/cloudflare/cloudflare-docs"
CU = "https://raw.githubusercontent.com/curl/curl"
SAMPLES = (
    ("M01", "curl", "feed", "https://github.com/curl/curl/releases.atom"),
    ("M02", "curl", "full_html", "https://github.com/curl/curl/releases/tag/curl-8_17_0"),
    ("M03", "curl", "body", f"{CU}/curl-8_17_0/RELEASE-NOTES"),
    ("M04", "Cloudflare", "body", f"{CF}/f31ae08b8eda3b570d13a2df9556d9d914b7772d/"
     "src/content/changelog/workers/2025-09-26-analytics-engine-sql-enhancements.mdx"),
    ("M05", "Cloudflare", "body", f"{CF}/879bf0a48ec04f2690be42416f2c3826e3c906ee/"
     "src/content/changelog/workers/2026-01-01-microfrontends.mdx"),
    ("M06", "curl", "body", f"{CU}/curl-8_14_0/RELEASE-NOTES"),
    ("M07", "Mozilla", "native_index", "https://product-details.mozilla.org/1.0/firefox_history_major_releases.json"),
    ("M08", "Cloudflare", "native_feed", "https://developers.cloudflare.com/changelog/rss/workers.xml"),
    ("M09", "curl", "native_index", "https://curl.se/docs/releases.html"),
)


class ReleaseHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.times = []

    def handle_starttag(self, tag, attrs):
        if tag == "relative-time":
            self.times.extend(value for name, value in attrs if name == "datetime")


def inspect(body, mode):
    text = body.decode("utf-8")
    if mode in {"feed", "native_feed"}:
        root = ET.fromstring(text)
        return {"items": len(root.findall("{*}entry")) or len(root.findall("./channel/item")),
                "kind": root.tag}
    if mode == "full_html":
        parsed = ReleaseHTML()
        parsed.feed(text)
        return {"time_elements": len(parsed.times), "first": parsed.times[0]}
    if mode == "native_index" and text.lstrip().startswith("{"):
        return {"count": len(json.loads(text))}
    lines = text.splitlines()
    if lines and lines[0] == "---":
        end = lines[1:].index("---") + 1
        dates = [line.partition(":")[2].strip() for line in lines[:end] if line.startswith("date:")]
        return {"lines": len(lines), "declared_date": dates[0]}
    return {"lines": len(lines), "head": lines[0][:80] if lines else ""}


def sample(work, entry):
    sample_id, publisher, mode, url = entry
    path = work / (sample_id + ".body")
    result = subprocess.run([
        "curl", "-sS", "--location", "--max-redirs", "4", "--max-time", "24",
        "--max-filesize", "2000000", "--retry", "0", "--user-agent", "AgentFlow-Research/1.0",
        "--output", str(path), "--write-out",
        "%{http_code}\t%{num_redirects}\t%{size_download}\t%{size_header}\t%{time_total}\t%{url_effective}",
        url,
    ], capture_output=True, text=True, check=False)
    status, redirects, body_size, header_size, elapsed, final_url = result.stdout.split("\t")
    row = dict(id=sample_id, publisher=publisher, mode=mode, url=url, final_url=final_url,
               utc=datetime.now(UTC).isoformat(timespec="seconds"), curl_exit=result.returncode,
               status=status, calls=1 + int(redirects), body_bytes=int(body_size),
               header_bytes=int(header_size), elapsed_ms=round(float(elapsed) * 1000, 3),
               parse_ms="", sqlite_ms="", metadata_bytes="", sqlite_file_bytes="", sha256="",
               parsed="", access=result.stderr.strip())
    if result.returncode or status != "200":
        return row
    body = path.read_bytes()
    assert len(body) == row["body_bytes"]
    parse_time, store_time = [], []
    row["sha256"] = sha256(body).hexdigest()
    for repeat in range(5):
        t0 = perf_counter_ns()
        facts = inspect(body, mode)
        parse_time.append((perf_counter_ns() - t0) / 1e6)
        metadata = json.dumps({"facts": facts, "url": url, "sha256": row["sha256"]}, sort_keys=True)
        db_path = work / f"{sample_id}-{repeat}.sqlite"
        db = sqlite3.connect(db_path)
        db.execute("CREATE TABLE artifact (id TEXT PRIMARY KEY, meta TEXT NOT NULL, content BLOB NOT NULL)")
        t0 = perf_counter_ns()
        with db:
            db.execute("INSERT INTO artifact VALUES (?, ?, ?)", (sample_id, metadata, body))
        store_time.append((perf_counter_ns() - t0) / 1e6)
        assert db.execute("SELECT length(content) FROM artifact").fetchone()[0] == len(body)
        db.close()
    row.update(parse_ms=round(median(parse_time), 4), sqlite_ms=round(median(store_time), 4),
               metadata_bytes=len(metadata.encode()), sqlite_file_bytes=db_path.stat().st_size,
               parsed=json.dumps(facts, sort_keys=True), access="opened")
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    with TemporaryDirectory(prefix="af152-sample-") as tmp:
        rows = [sample(Path(tmp), spec) for spec in SAMPLES]
    with args.out.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
