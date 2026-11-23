#!/usr/bin/env python3
"""Read the immutable public result from GitHub and compare exact committed bytes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request

OWNED = "docs/workstreams/research/AF-RES-102/"
REPO = "https://raw.githubusercontent.com/laadkke-arch/agentflow-open/"
DEFAULT_PATHS = [
    "RESULT.md", "SELF_CHECK.md", "reproduce.md", "SCOPE.md", "manifest.json",
    "frame.csv", "predictions.csv", "lineage.csv", "sources.jsonl", "counts.json",
    "evidence/stage1-seal.json", "evidence/prediction-seal.json",
    "evidence/ggplot2/audit.json", "evidence/matplotlib/audit.json",
    "evidence/cross-domain/audit.json", "evidence/cross-domain/trees-audit.json",
    "evidence/cross-domain/wheel-audit.json",
    "evidence/representative/index.json",
    "evidence/representative/GG-G1-old.png", "evidence/representative/GG-G1-new.png",
    "evidence/representative/MP-C1-old.png", "evidence/representative/MP-C1-new.png",
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def read_one(commit, path):
    url = REPO + commit + "/" + OWNED + path
    row = {"path": OWNED + path, "url": url, "started_utc": utc()}
    try:
        expected = subprocess.check_output(["git", "show", commit + ":" + OWNED + path])
        req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-102-source-audit"})
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read()
            row.update(status=response.status, final_url=response.geturl(),
                       mime=response.headers.get("Content-Type"), bytes=len(body))
        row.update(sha256=hashlib.sha256(body).hexdigest(),
                   git_bytes_sha256=hashlib.sha256(expected).hexdigest(),
                   exact_bytes_match=body == expected)
        row["ok"] = row["status"] == 200 and row["exact_bytes_match"]
    except Exception as exc:
        row.update(ok=False, error_type=type(exc).__name__, error=str(exc))
    row["finished_utc"] = utc()
    return row


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--commit", required=True)
    p.add_argument("--output")
    p.add_argument("--path", action="append")
    a = p.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", a.commit):
        raise SystemExit("An exact 40-character commit is required")
    paths = a.path or DEFAULT_PATHS
    if any(x.startswith("/") or ".." in Path(x).parts for x in paths):
        raise SystemExit("Only relative task-owned files are accepted")
    started = utc()
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda path: read_one(a.commit, path), paths))
    result = {"command": "python -B .../tools/readback.py --commit " + a.commit,
              "target_commit": a.commit, "started_utc": started, "finished_utc": utc(),
              "scope": "Read fixed GitHub result/report/raw-evidence projections/reproduction files; no external source re-test, UI/reader execution or generation proof",
              "files": rows, "passed": sum(x["ok"] for x in rows), "requested": len(rows),
              "exit_code": 0 if all(x["ok"] for x in rows) else 1}
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if a.output:
        output = Path(a.output)
        if not str(output).startswith(OWNED):
            raise SystemExit("Output must stay in the task-owned path")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text)
    print(text)
    raise SystemExit(result["exit_code"])


if __name__ == "__main__":
    main()
