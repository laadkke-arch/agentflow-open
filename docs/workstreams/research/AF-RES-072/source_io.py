"""Bounded public HTTP reads and timing, shared by capture and live search."""

import datetime
import hashlib
import time
import urllib.error
import urllib.parse
import urllib.request

MAX_BODY = 1_048_576
DISPLAY = 1_200
MAX_OPENS = 4
WINDOW = 220


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds")


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.hops = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.hops.append(dict(status=code, source=req.full_url, target=newurl))
        next_url = urllib.parse.urlsplit(newurl)
        if next_url.scheme != "https" or next_url.username or next_url.password:
            raise urllib.error.URLError("redirect outside public HTTPS")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def retrieve(url, remaining):
    """Return the complete body (if available) and an application-layer receipt."""
    start = time.perf_counter_ns()
    redirects = Redirects()
    opener = urllib.request.build_opener(redirects)
    request = urllib.request.Request(url, headers={
        "User-Agent": "AF-RES-072 public research",
        "Accept-Encoding": "identity",
    })
    receipt = dict(utc=utc(), url=url, final_url=url, http_status=None, error=None,
                   redirects=redirects.hops, http_attempts=1, retries=0,
                   headers={}, read_bytes=0, body_sha256=None, complete=False)
    data = None
    try:
        with opener.open(request, timeout=10) as response:
            receipt["http_status"] = response.status
            receipt["final_url"] = response.url
            receipt["headers"] = {
                key.lower(): response.headers[key] for key in
                ("Content-Length", "Content-Encoding", "ETag", "Last-Modified", "Age", "Via", "X-Cache", "Date")
                if key in response.headers
            }
            length = response.headers.get("Content-Length")
            encoding = response.headers.get("Content-Encoding", "identity")
            if encoding != "identity":
                receipt["error"] = "unsupported-content-encoding"
            elif length is not None and int(length) > remaining:
                receipt["error"] = "declared-length-exceeds-remaining"
            else:
                # Count chunks already returned even if a later read fails.
                chunks = []
                while receipt["read_bytes"] < remaining:
                    chunk = response.read(min(65536, remaining - receipt["read_bytes"]))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    receipt["read_bytes"] += len(chunk)
                data = b"".join(chunks)
                receipt["body_sha256"] = sha(data)
                if length is not None and len(data) != int(length):
                    receipt["error"] = "short-body"
                elif length is None and len(data) == remaining:
                    receipt["error"] = "length-unknown-at-limit"
                elif not data:
                    receipt["error"] = "empty-body"
    except urllib.error.HTTPError as error:
        receipt["http_status"] = error.code
        receipt["final_url"] = error.url
        receipt["error"] = f"HTTPError: {error.reason}"
        error.close()
    except (OSError, ValueError) as error:
        receipt["error"] = f"{type(error).__name__}: {error}"
    receipt["elapsed_ns"] = time.perf_counter_ns() - start
    receipt["complete"] = data is not None and receipt["error"] is None
    return (data if receipt["complete"] else None), receipt
