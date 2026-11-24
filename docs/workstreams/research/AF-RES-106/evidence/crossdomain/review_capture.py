"""Reopen Q7 primary sources without overwriting the first receipt or raw bytes."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import urllib.error
import urllib.request
import urllib.parse

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review-raw"
REQUESTS = [
    ("IIIF-P3", "https://iiif.io/api/presentation/3.0/", "iiif-presentation-3.html"),
    ("IIIF-CS1", "https://iiif.io/api/content-state/1.0/", "iiif-content-state-1.html"),
    ("RIJKS", "https://iiif.micr.io/PJEZO/manifest", "rijksmuseum-manifest.json"),
    ("FITZ", "https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json", "fitzwilliam-manifest.json"),
    ("JATS-FIG", "https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html", "jats-1.3-fig.html"),
    ("JATS-XREF", "https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html", "jats-1.3-xref.html"),
    ("PLOS-XML", "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript", "plos-spark.xml"),
    ("PLOS-HTML", "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031", "plos-spark.html"),
]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def public_url(url):
    parts = urllib.parse.urlsplit(url)
    if "X-Amz-" in parts.query:
        return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return url


def receive(item):
    identifier, url, name = item
    row = {"source_id": "CD106-REVIEW-" + identifier, "url": url,
           "started_utc": utc(), "method": "urllib HTTP GET; no browser rendering",
           "first_snapshot": name, "first_sha256": hashlib.sha256((ROOT/name).read_bytes()).hexdigest()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-106 public research review"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
            row.update(http_status=response.status, final_url=public_url(response.url),
                       content_type=response.headers.get("Content-Type"),
                       sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
                       preserved_path="review-raw/" + name)
        (OUT/name).write_bytes(data)
        row["same_bytes_as_first_snapshot"] = row["sha256"] == row["first_sha256"]
    except urllib.error.HTTPError as error:
        row.update(http_status=error.code, error=str(error))
    except Exception as error:
        row.update(error=type(error).__name__ + ": " + str(error))
    row["completed_utc"] = utc()
    return row


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        rows = list(executor.map(receive, REQUESTS))
    (ROOT/"review-network-receipts.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2)+"\n")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
