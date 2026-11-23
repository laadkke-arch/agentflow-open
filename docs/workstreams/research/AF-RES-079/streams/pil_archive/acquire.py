"""Fetch original PIL archive/provenance without installing or running it."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).parent
URLS = [
    ("debian-index", "https://archive.debian.org/debian/pool/main/p/python-imaging/"),
    ("orig", "https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7.orig.tar.gz"),
    ("dsc", "https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7-2.dsc"),
    ("debian-patch", "https://archive.debian.org/debian/pool/main/p/python-imaging/python-imaging_1.1.7-2.diff.gz"),
    ("debian-image-patched", "https://sources.debian.org/data/main/p/python-imaging/1.1.7-2/PIL/Image.py"),
    ("debian-copyright", "https://sources.debian.org/data/main/p/python-imaging/1.1.7-2/debian/copyright"),
    ("supplier-2010", "https://mail.python.org/pipermail/image-sig/2010-August/006480.html"),
]


def fetch(item):
    key, url = item
    chain = []

    class Redirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            chain.append({"url": req.full_url, "status": code, "location": newurl})
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    row = {"probe_id": key, "opened_url": url,
           "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "chain": chain}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-079 research"})
        response = urllib.request.build_opener(Redirect).open(request, timeout=40)
        data = response.read()
        cache = ROOT / "cache" / key
        cache.write_bytes(data)
        row.update(status=response.status, arrived_url=response.url,
                   content_type=response.headers.get("Content-Type"),
                   bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                   sha1=hashlib.sha1(data).hexdigest(), md5=hashlib.md5(data).hexdigest(),
                   cache_file=str(cache.relative_to(ROOT)), access="opened")
    except Exception as error:
        row.update(status=getattr(error, "code", None), arrived_url=getattr(error, "url", url),
                   access="failed", error=repr(error))
    return row


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        rows = list(pool.map(fetch, URLS))
    with (ROOT / "http-receipts.jsonl").open("w") as output:
        for row in rows:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(json.dumps({k: v for k, v in row.items() if k != "chain"}, ensure_ascii=False))
