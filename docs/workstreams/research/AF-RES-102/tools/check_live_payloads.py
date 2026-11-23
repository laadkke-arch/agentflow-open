#!/usr/bin/env python3
"""Resolve the remaining byte risk for the four reader-facing Matplotlib URLs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def utc():
    return datetime.now(timezone.utc).isoformat()


def fetch(item):
    case, payload = item
    fixed = payload["url"]
    url = "https://matplotlib.org/3.7.0/" + fixed.split("/3.7.0/", 1)[1]
    row = {"case_id": case, "original_url": url, "fixed_url": fixed,
           "expected_sha256": payload["sha256"], "started_utc": utc(),
           "countable": False, "duplicate_reason": "Live mirror of the already-read pinned payload; no new work"}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "AF-RES-102-return-url-audit"}), timeout=45) as response:
            b = response.read()
            row.update(status=response.status, final_url=response.geturl(),
                       mime=response.headers.get("Content-Type"), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
                       png_signature=b[:8] == b"\x89PNG\r\n\x1a\n")
        row["exact_bytes_match"] = row["sha256"] == row["expected_sha256"]
        row["ok"] = row["status"] == 200 and row["png_signature"] and row["exact_bytes_match"]
    except Exception as exc:
        row.update(ok=False, error_type=type(exc).__name__, error=str(exc))
    row["finished_utc"] = utc()
    return row


def main():
    data = json.loads((ROOT / "evidence/matplotlib/main-audit-raw.json").read_text())
    selected = [(r["case_id"], x) for r in data["records"]
                if r["edition"] == "new" and not r.get("vacancy") for x in r["first_payloads"]]
    assert len(selected) == 8
    started = utc()
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, selected))
    result = {"started_utc": started, "finished_utc": utc(), "requested": len(rows),
              "passed": sum(r["ok"] for r in rows), "records": rows,
              "scope": "Four returned live versioned pages' first-image src and 2x srcset payloads; resolve current byte availability separately from mutable full HTML. Not a render/execution/generation test.",
              "exit_code": 0 if all(r["ok"] for r in rows) else 1}
    (ROOT / "evidence/live-payload-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result["exit_code"])


if __name__ == "__main__":
    main()
