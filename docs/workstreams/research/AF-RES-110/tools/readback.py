"""Read a pushed AF-RES-110 result and representative raw evidence by fixed SHA."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from time import sleep

from prototype import git
from summarize import ROOT, json_rows

REPOSITORY = "laadkke-arch/agentflow-open"
MATERIAL = (
    "RESULT.md", "manifest.json", "SCOPE.md", "frame.csv", "issue-frame.csv", "catalog.jsonl", "queries.jsonl",
    "truth.csv", "runs.jsonl", "ranks.csv", "changes.csv", "sources.jsonl", "SELF_CHECK.md", "reproduce.md",
    "evidence/acceptance-evidence.json", "evidence/replay.json", "evidence/replacement.json", "evidence/summary.json",
)
REPRESENTATIVE = (
    "DOC-SP-X1-old", "DOC-SP-X1-current", "DOC-PA-G2-current", "READ-PABULK-current",
    "DOC-DA-X1-current", "DOC-DA-X1-code-current", "DOC-GD-X2-old", "DOC-GD-X2-code-current",
)


def iso():
    return datetime.now(timezone.utc).isoformat()


def http_get(kind, id_, url, expected, expected_location):
    receipt = {"kind": kind, "id": id_, "url": url, "expected_sha256": expected}
    for _ in range(2):
        try:
            with urlopen(Request(url, headers={"User-Agent": "AF-RES-110 fixed result readback"}), timeout=12) as response:
                data = response.read()
                actual = hashlib.sha256(data).hexdigest()
                receipt.update({
                    "arrival_url": response.url, "status": response.status, "sha256": actual,
                    "bytes": len(data), "matched": actual == expected, "utc": iso(),
                })
                if expected_location:
                    lines = [int(m) for m in re.findall(r"\d+", expected_location)]
                    assert lines and max(lines) <= len(data.splitlines())
                    receipt["source_line_span_present"] = True
                    receipt["source_location"] = expected_location
                return receipt
        except (HTTPError, OSError) as exc:
            receipt.update({"matched": False, "error": str(exc), "utc": iso()})
            sleep(0.25)
    return receipt


def main(sha, output, require_remote_head):
    assert git("rev-parse", "HEAD").decode().strip() == sha
    assert not git("status", "--porcelain").strip()
    branch_name = "refs/heads/work/research-af-res-110"
    remote = git("ls-remote", "origin", branch_name).decode().split()
    assert len(remote) == 2 and remote[1] == branch_name, remote
    if require_remote_head:
        assert remote[0] == sha, remote
    if remote[0] != sha:
        git("merge-base", "--is-ancestor", sha, remote[0])
    owned = ROOT.relative_to(ROOT.parents[3])
    raw_root = f"https://raw.githubusercontent.com/{REPOSITORY}/{sha}/"
    requests = []
    for name in MATERIAL:
        path = (owned / name).as_posix()
        data = git("show", f"{sha}:{path}")
        requests.append(("pushed_result", name, raw_root + path, hashlib.sha256(data).hexdigest(), None))
    sources = {row["source_id"]: row for row in json_rows(ROOT / "sources.jsonl")}
    for key in REPRESENTATIVE:
        row = sources[key]
        requests.append(("representative_source", key, row["arrival_url"], row["source_sha256"], row["location"]))
    started = iso()
    with ThreadPoolExecutor(max_workers=8) as executor:
        receipts = list(executor.map(lambda item: http_get(*item), requests))
    result = {"started_utc": started, "completed_utc": iso(), "checked_commit": sha,
              "observed_remote_ref": remote[1], "observed_remote_sha": remote[0], "checks": receipts,
              "matched": sum(r["matched"] for r in receipts), "total": len(receipts)}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "checks"}))
    return int(result["matched"] != result["total"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--require-remote-head", action="store_true")
    options = parser.parse_args()
    raise SystemExit(main(options.commit, options.output, options.require_remote_head))
