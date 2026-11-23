"""Re-read the four exact public opened-hour archives; print a verification receipt.

This does not alter evidence or use authentication, proxies, or alternate URLs.
Network errors remain errors; an unavailable initial body is never inferred.
"""

import datetime
import gzip
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def verify(expected):
    receipt = {
        "case_id": expected["case_id"],
        "url": expected["archive_url"],
        "started_utc": utc(),
        "event_found": False,
        "verified": False,
    }
    try:
        request = urllib.request.Request(
            expected["archive_url"],
            headers={"User-Agent": "AF-RES-074-public-research"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            receipt.update(http_status=response.status, arrival_url=response.url)
            with gzip.GzipFile(fileobj=response) as archive:
                for line in archive:
                    event = json.loads(line)
                    if str(event.get("id")) != expected["event_id"]:
                        continue
                    issue = event["payload"]["issue"]
                    digest = hashlib.sha256(issue.get("body", "").encode()).hexdigest()
                    receipt.update(
                        event_found=True,
                        event_id=event["id"],
                        issue_id=issue["id"],
                        body_sha256=digest,
                        verified=(
                            event["type"] == "IssuesEvent"
                            and event["payload"]["action"] == "opened"
                            and event["repo"]["name"].lower() == "osgeo/gdal"
                            and issue["id"] == expected["issue_id"]
                            and issue["number"] == expected["issue_number"]
                            and digest == expected["initial_body_sha256"]
                        ),
                    )
                    break
    except urllib.error.HTTPError as error:
        receipt.update(http_status=error.code, error=str(error))
    except Exception as error:
        receipt["error"] = repr(error)
    receipt["finished_utc"] = utc()
    return receipt


if __name__ == "__main__":
    records = json.loads(
        Path(__file__).with_name("selected-initial-recovery-addendum.json").read_text()
    )
    results = []
    for record in records:
        result = verify(record)
        results.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    raise SystemExit(0 if all(row["verified"] for row in results) else 1)
