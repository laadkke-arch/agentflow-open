"""Read public GH Archive hourly files; emit only the requested issue opened event.

Never print comments, status, comment counts or unrelated events. Raw bodies stay
in the task's ignored private directory. This is source recovery, not a test of rg.
"""
import concurrent.futures
import datetime
import gzip
import hashlib
import json
import pathlib
import sys
import urllib.request

BASE = pathlib.Path(__file__).resolve().parents[2]
PRIVATE = BASE / "private" / "ripgrep"

def recover(number):
    raw = json.loads((PRIVATE / f"issue-{number}.json").read_text())
    issue = raw["data"]
    stamp = datetime.datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    url = f"https://data.gharchive.org/{stamp:%Y-%m-%d}-{stamp.hour}.json.gz"
    record = {"issue": number, "url": url, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-070-public-research"})
        with urllib.request.urlopen(request, timeout=50) as response:
            record["http_status"] = response.status
            record["compressed_content_length"] = response.headers.get("Content-Length")
            with gzip.GzipFile(fileobj=response) as stream:
                for line_no, line in enumerate(stream, 1):
                    if b'"IssuesEvent"' not in line or b'"BurntSushi/ripgrep"' not in line:
                        continue
                    event = json.loads(line)
                    payload = event.get("payload", {})
                    target = payload.get("issue", {})
                    if event.get("repo", {}).get("name", "").lower() != "burntsushi/ripgrep" or payload.get("action") != "opened" or target.get("number") != number:
                        continue
                    (PRIVATE / f"opened-{number}.json").write_text(json.dumps(event, ensure_ascii=False, indent=2))
                    body = target.get("body") or ""
                    record.update({"found": True, "event_id": event["id"], "line": line_no, "event_created_at": event["created_at"], "body_sha256": hashlib.sha256(body.encode()).hexdigest(), "current_body_equal": body == issue.get("body"), "body_chars": len(body)})
                    break
                else:
                    record.update({"found": False, "lines_scanned": line_no})
    except Exception as error:
        record.update({"found": False, "error_type": type(error).__name__, "error": str(error)})
    record["ended_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (PRIVATE / f"recovery-{number}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2))
    return record

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for result in executor.map(recover, map(int, sys.argv[1:])):
            print(json.dumps(result, ensure_ascii=False), flush=True)
