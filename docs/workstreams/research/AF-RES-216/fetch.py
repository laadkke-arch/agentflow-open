"""Capture public PyPI metadata bodies and HTTP receipts without installing anything."""

import argparse
import gzip
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RELEASES = (
    ("matplotlib", "3.9.0"),
    ("matplotlib", "3.9.1"),
    ("matplotlib", "3.9.1.post1"),
    ("pytest", "8.0.2"),
    ("pytest", "8.1.0"),
    ("pytest", "8.1.1"),
)
PROJECTS = tuple(dict.fromkeys(project for project, _ in RELEASES))
SIMPLE_TYPE = "application/vnd.pypi.simple.v1+json"
HTML_TYPE = "text/html"
API_TYPE = "application/json"
HEADERS = (
    "Date", "Age", "Cache-Control", "ETag", "Vary", "Content-Encoding",
    "Content-Length", "X-PyPI-Last-Serial", "X-Cache",
)


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def endpoints(group):
    for number, (project, version) in enumerate(RELEASES, 1):
        if group == "api":
            yield f"V{number:02}", project, version, f"https://pypi.org/pypi/{project}/{version}/json", API_TYPE
        else:
            yield f"H{number:02}", project, version, f"https://pypi.org/project/{project}/{version}/", HTML_TYPE
    if group == "api":
        for number, project in enumerate(PROJECTS, 1):
            yield f"I{number:02}", project, None, f"https://pypi.org/simple/{project}/", SIMPLE_TYPE


def capture(out, source_id, project, version, url, mime, timeout):
    request = Request(url, headers={
        "Accept": mime,
        "Accept-Encoding": "identity",
        "User-Agent": "AF-RES-216 public metadata verification/1",
    })
    receipt = {
        "kind": "observed_public_https", "source_id": source_id, "project": project,
        "version": version, "request_url": url, "request_accept": mime,
        "started_utc": utc(), "received_utc": None, "final_url": None,
        "http_status": None, "content_type": None, "response_headers": {},
        "body": None, "body_bytes": None, "sha256": None, "error": None,
    }
    try:
        try:
            response = urlopen(request, timeout=timeout)
        except HTTPError as exc:
            response = exc
        with response:
            receipt["final_url"] = response.geturl()
            receipt["http_status"] = response.status
            receipt["content_type"] = response.headers.get("Content-Type")
            receipt["response_headers"] = {
                key: response.headers[key] for key in HEADERS if key in response.headers
            }
            body = response.read()
        receipt["received_utc"] = utc()
    except (URLError, OSError, ValueError) as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["finished_utc"] = utc()
        return receipt

    extension = "html" if mime == HTML_TYPE else "json"
    filename = f"{source_id}-{project}{'-' + version if version else ''}.{extension}.gz"
    (out / filename).write_bytes(gzip.compress(body, compresslevel=9, mtime=0))
    receipt.update(body=filename, body_bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
    actual_type = (receipt["content_type"] or "").split(";", 1)[0].strip().lower()
    encoding = receipt["response_headers"].get("Content-Encoding", "identity")
    if receipt["http_status"] != 200:
        receipt["error"] = f"HTTP {receipt['http_status']}"
    elif actual_type != mime or encoding != "identity":
        receipt["error"] = f"Expected {mime} with identity encoding, got {actual_type} / {encoding}"
    elif mime != HTML_TYPE:
        try:
            document = json.loads(body)
            array = document["files" if mime == SIMPLE_TYPE else "urls"]
            if not isinstance(array, list):
                raise ValueError("file records are not an array")
            if mime == SIMPLE_TYPE and document["name"].lower() != project:
                raise ValueError("Simple project mismatch")
            if mime == API_TYPE and (
                document["info"]["version"] != version or document["info"]["name"].lower() != project
            ):
                raise ValueError("version JSON identity mismatch")
        except (KeyError, ValueError, TypeError, AttributeError) as exc:
            receipt["error"] = f"JSON validation: {exc}"
    receipt["finished_utc"] = utc()
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", choices=("api", "html"), required=True)
    parser.add_argument("--out", required=True, type=Path, help="new directory for this attempt")
    parser.add_argument("--timeout", type=float, default=35.0, help="socket timeout in seconds")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    receipts = []
    for endpoint in endpoints(args.group):
        receipt = capture(args.out, *endpoint, args.timeout)
        receipts.append(receipt)
        print(f"{receipt['source_id']} {receipt['http_status']} {receipt['content_type']} "
              f"{receipt['body_bytes']} {receipt['sha256']} {receipt['received_utc']}", flush=True)
        if receipt["error"]:
            print(f"{receipt['source_id']}: {receipt['error']}", file=sys.stderr)
    (args.out / "http.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8")
    return int(any(row["error"] for row in receipts))


if __name__ == "__main__":
    raise SystemExit(main())
