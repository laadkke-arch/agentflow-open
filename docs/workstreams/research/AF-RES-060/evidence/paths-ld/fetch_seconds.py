"""Acquire only the frozen first/second links for the LD shard; never rank."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import urllib.request
import urllib.error

HERE = Path(__file__).parent
PLAN = [
    ("SC034-D2", "https://json-everything.net"),
    ("SC034-D3", "https://docs.json-everything.net"),
    ("SC036-D2", "https://tools.ietf.org/html/draft-wright-json-schema-01"),
    ("SC036-D3", "http://tools.ietf.org/html/draft-zyp-json-schema-04"),
    ("SC038-D2", "https://json-schema.org/draft/2019-09/schema"),
    ("SC039-D2", "https://bowtie.report/#/?language=typescript&language=javascript"),
    ("SC040-D2", "https://pypi.org/project/json-schema-utils"),
    ("LD008-D2", "https://www.w3.org/TR/json-ld11/"),
    ("LD008-D3", "https://rubygems.org/gems/rdf"),
]


def fetch(item):
    key, original_url = item
    row = {"id": key, "original_url": original_url, "attempts": [], "status": "failed"}
    urls = [original_url]
    if original_url.startswith("http://"):
        urls.append("https://" + original_url[7:])
    for url in urls:
        attempt = {"requested_url": url, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-060 documented research; bounded primary-source reading"})
            with urllib.request.urlopen(request, timeout=35) as response:
                payload = response.read()
                mime = response.headers.get("Content-Type", "")
                suffix = ".json" if "json" in mime and "html" not in mime else ".html"
                path = HERE / "raw" / (key + suffix)
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(payload)
                attempt.update({"http_status": response.status, "final_url": response.url, "bytes": len(payload), "content_type": mime})
                row.update({"status": "fetched_not_yet_window_read", "fixed_url": response.url, "raw_file": str(path.relative_to(HERE)), "sha256": hashlib.sha256(payload).hexdigest(), "charset": response.headers.get_content_charset() or "utf-8", "acquired_utc": attempt["utc"]})
        except Exception as error:
            attempt["error"] = type(error).__name__ + ": " + str(error)
        row["attempts"].append(attempt)
        if row["status"] != "failed":
            break
    return row


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch, PLAN))
    (HERE / "web-seconds.json").write_text(json.dumps(results, indent=2) + "\n")
    for row in results:
        print(row["id"], row["status"], row.get("fixed_url"), len(row["attempts"]))
