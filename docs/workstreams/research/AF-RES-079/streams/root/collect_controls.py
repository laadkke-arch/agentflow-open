"""Read public control sources and record current HTTP arrivals, not link history."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
URLS = {
    "c01-oldnotes": "https://scikit-learn.org/0.9/whats_new.html",
    "c01-sourceforge": "https://scikit-learn.sourceforge.net/0.9/whats_new.html",
    "c01-newnotes": "https://scikit-learn.org/stable/whats_new/older_versions.html",
    "c01-rawnotes": "https://raw.githubusercontent.com/scikit-learn/scikit-learn/0.9/doc/whats_new.rst",
    "c01-alias": "https://raw.githubusercontent.com/scikit-learn/scikit-learn/0.9/scikits/learn/__init__.py",
    "c01-tag08": "https://api.github.com/repos/scikit-learn/scikit-learn/git/ref/tags/0.8",
    "c01-tag09": "https://api.github.com/repos/scikit-learn/scikit-learn/git/ref/tags/0.9",
    "c02-about": "https://pillow.readthedocs.io/en/stable/about.html",
    "c02-porting": "https://pillow.readthedocs.io/en/stable/porting.html",
    "c02-original": "https://pythonware.com/products/pil/",
    "c02-original-registry": "https://pypi.org/project/PIL/",
    "c02-new-registry": "https://pypi.org/project/Pillow/",
    "c02-transfer": "https://api.github.com/repos/python-pillow/Pillow/issues/1535",
    "c02-transfer-comments": "https://api.github.com/repos/python-pillow/Pillow/issues/1535/comments?per_page=100",
    "c02-patch": "https://mail.python.org/pipermail/image-sig/2010-August/006480.html",
    "c03-old": "https://docs.python.org/3.11/library/imp.html#imp.find_module",
    "c03-live": "https://docs.python.org/3/library/imp.html#imp.find_module",
    "c03-new": "https://docs.python.org/3.12/library/imp.html",
    "c03-migrate": "https://docs.python.org/3.12/whatsnew/3.12.html#imp",
    "c03-rawold": "https://raw.githubusercontent.com/python/cpython/v3.11.0/Doc/library/imp.rst",
    "c03-rawnew": "https://raw.githubusercontent.com/python/cpython/v3.12.0/Doc/library/imp.rst",
    "c03-pr": "https://api.github.com/repos/python/cpython/issues/98040",
}

class TextReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.ids = set()

    def handle_data(self, text):
        if text.strip():
            self.text.append(text.strip())

    def handle_starttag(self, tag, attrs):
        self.ids.update(v for k, v in attrs if k == "id")

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({"status": code, "url": req.full_url,
                           "location": headers.get("Location")})
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(item):
    key, url = item
    row = {"probe_id": key, "requested_url": url,
           "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "transport": "urllib GET / ChatGPT cloud sandbox",
           "historical_redirect_claim": False}
    try:
        redirects = Redirects()
        opener = urllib.request.build_opener(redirects)
        try:
            response = opener.open(urllib.request.Request(url, headers={"User-Agent": "AF-RES-079-public-research"}), timeout=20)
        except urllib.error.HTTPError as exc:
            response = exc
        content = response.read()
        body = content.decode("utf-8", errors="replace")
        row.update(status=response.status, arrived_url=response.geturl(),
                   chain=redirects.chain + [{"status": response.status, "url": response.geturl()}],
                   sha256=hashlib.sha256(content).hexdigest(),
                   bytes=len(content),
                   access_status="opened" if 200 <= response.status < 300 else "failed")
        (CACHE / (key + ".txt")).write_text(body)
        if "html" in response.headers.get("Content-Type", ""):
            soup = TextReader()
            soup.feed(body)
            row["requested_fragment_present"] = (
                url.split("#", 1)[1] in soup.ids if "#" in url else None)
            readable = "\n".join(soup.text)
        else:
            readable = body
        (CACHE / (key + "-read.txt")).write_text(readable)
    except Exception as exc:
        row.update(status=None, error=str(exc), access_status="failed")
    return row

def main():
    CACHE.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        rows = list(executor.map(fetch, URLS.items()))
    (ROOT / "http-probes.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))

if __name__ == "__main__":
    main()
