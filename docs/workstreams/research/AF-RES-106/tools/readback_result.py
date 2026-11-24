"""Reopen immutable GitHub result files and original returned HTML fragments."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import csv
import datetime
import hashlib
import json
import subprocess
import urllib.request
import urllib.error
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
OUT = ROOT / "evidence/validation"
PREFIX = "docs/workstreams/research/AF-RES-106/"


class Ids(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def request(job):
    result = {k: v for k, v in job.items() if k != "expected_bytes"}
    result["requested_utc"] = utc()
    url = urllib.parse.urldefrag(job["url"])[0]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-106-result-readback"})
        with urllib.request.urlopen(req, timeout=55) as response:
            raw = response.read()
            result.update(status=response.status, final_url=response.url, content_type=response.headers.get("Content-Type"))
        digest = hashlib.sha256(raw).hexdigest()
        result.update(received_utc=utc(), bytes=len(raw), sha256=digest)
        if "expected_bytes" in job:
            result["committed_bytes_equal"] = raw == job["expected_bytes"]
        if job.get("expected_sha256"):
            result["fingerprint_equal"] = digest == job["expected_sha256"]
        if job.get("fragment"):
            parser = Ids()
            parser.feed(raw.decode("utf-8"))
            result["actual_fragment_present"] = job["fragment"] in parser.ids
        result["passed"] = result["status"] == 200 and all(result.get(k, True) for k in ["committed_bytes_equal", "fingerprint_equal", "actual_fragment_present"])
    except Exception as error:
        result.update(received_utc=utc(), status=getattr(error, "code", None), error=str(error), passed=False)
    result["browser_scroll_or_execution"] = "미실시"
    return result


def main():
    run = json.loads((OUT / "run.json").read_text())
    head = run["result_sha"]
    assert len(head) == 40
    paths = ["RESULT.md", "SELF_CHECK.md", "counts.json", "lineage.csv", "returns.csv", "sources.jsonl", "reproduce.md", "SCOPE.md", "manifest.json", "INDEX_PROPOSAL.md", "PRODUCT_OPTIONS.md",
             "tools/verify.py", "tools/recalculate.py", "evidence/source-reconciliation.json", "evidence/crossdomain/source-count-review.json", "evidence/ggplot2/FINAL_AUDIT.md", "evidence/matplotlib/FINAL_AUDIT.md", "evidence/crossdomain/CROSSDOMAIN_FINAL.md", "evidence/ggplot2/review-matplotlib.json",
             "evidence/ggplot2/payloads/new-scale_shape.png", "evidence/ggplot2/payloads/new-position_jitterdodge.png", "evidence/matplotlib/payloads/MP-A2-new-0.png", "evidence/matplotlib/payloads/MP-G2-new-0.png", "evidence/crossdomain/plos-figure7.png"]
    jobs = []
    for path in paths:
        expected = subprocess.check_output(["git", "show", head + ":" + PREFIX + path], cwd=REPO)
        jobs.append({"kind": "fixed_result_file", "path": PREFIX + path, "result_sha": head,
                     "url": "https://raw.githubusercontent.com/laadkke-arch/agentflow-open/" + head + "/" + PREFIX + path,
                     "expected_bytes": expected, "expected_sha256": hashlib.sha256(expected).hexdigest()})
    with (ROOT / "lineage.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            if row["vacant"] == "YES":
                continue
            jobs.append({"kind": "fixed_original_section", "case_id": row["case_id"], "edition": row["edition"],
                         "url": row["section_url"], "fragment": row["actual_fragment"], "expected_sha256": row["body_sha256"]})
    with (ROOT / "returns.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            if row["vacant"] == "YES":
                continue
            for key in ["old_rendered_url", "new_rendered_url"]:
                if row.get(key):
                    jobs.append({"kind": "version_site_static_return", "case_id": row["case_id"], "role": key,
                                 "url": row[key], "fragment": urllib.parse.urlsplit(row[key]).fragment})
    started = utc()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(request, jobs))
    record = {"started_utc": started, "finished_utc": utc(), "result_sha": head,
              "scope": "Exact committed GitHub artifacts/representative outputs, fixed original DOM ids and returned Matplotlib version-site ids. HTTP/static parse only; not browser navigation or historical generation.",
              "requests": len(results), "passed_count": sum(r["passed"] for r in results), "failed_count": sum(not r["passed"] for r in results), "rows": results}
    (OUT / "readback.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in record.items() if k != "rows"}, ensure_ascii=False, indent=2))
    if record["failed_count"]:
        print(json.dumps([r for r in results if not r["passed"]], ensure_ascii=False, indent=2))
    raise SystemExit(0 if not record["failed_count"] else 1)


if __name__ == "__main__":
    main()
