"""Acquisition, timing and receipts based on AF-RES-139 replay/common.py."""
import base64
import csv
import hashlib
import io
import json
import os
import resource
import subprocess
import tarfile
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, TZ="UTC", LANG="C.UTF-8", LC_ALL="C.UTF-8")


def utc():
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_in(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8") as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def read_jsonl(path):
    with path.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source]


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def cpu_seconds():
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    return time.process_time() + children.ru_utime + children.ru_stime


def process(argv, cwd=None, timeout=180):
    start, cpu = time.perf_counter(), cpu_seconds()
    record = {"command": [str(x) for x in argv], "cwd": str(cwd or Path.cwd()), "opened_utc": utc()}
    try:
        result = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True, timeout=timeout, check=False)
        record.update(exit=result.returncode, stdout=result.stdout.decode(errors="replace"),
                      stderr=result.stderr.decode(errors="replace"))
    except subprocess.TimeoutExpired as exc:
        record.update(exit=None, error="timeout", stdout=(exc.stdout or b"").decode(errors="replace"),
                      stderr=(exc.stderr or b"").decode(errors="replace"))
    return record | {"wall_ms": round((time.perf_counter() - start) * 1000, 3),
                     "cpu_ms": round((cpu_seconds() - cpu) * 1000, 3)}


class Http:
    """Per-condition in-process URL cache. Only successful complete bodies are cached."""
    def __init__(self):
        self.cache = {}

    def get(self, url, limit=60_000_000):
        if url in self.cache:
            raw, prior = self.cache[url]
            return raw, {"url": url, "opened_utc": utc(), "cache": "local_url_hit",
                         "source_sha256": prior["sha256"], "bytes": 0, "status": None}
        event = {"url": url, "opened_utc": utc(), "cache": "miss", "method": "GET",
                 "accept_encoding": "identity", "bytes": None, "status": None}
        request = urllib.request.Request(url, headers={
            "User-Agent": "AF-RES-143 research replay", "Accept-Encoding": "identity",
        })
        start = time.perf_counter()
        try:
            try:
                response = urllib.request.urlopen(request, timeout=20)
            except urllib.error.HTTPError as exc:
                response = exc
            with response:
                event.update(status=response.code, final_url=response.url,
                             content_encoding=response.headers.get("Content-Encoding"),
                             content_type=response.headers.get("Content-Type"),
                             etag=response.headers.get("ETag"), last_modified=response.headers.get("Last-Modified"),
                             link=response.headers.get("Link"))
                raw = response.read(limit + 1)
            event.update(bytes=len(raw), sha256=sha(raw))
            if len(raw) > limit:
                raise ValueError("body exceeds bound")
            if event["status"] == 200:
                self.cache[url] = raw, event
        except (OSError, ValueError) as error:
            event.update(error=str(error))
            raw = None
        event.update(wall_ms=round((time.perf_counter() - start) * 1000, 3))
        return (raw if event["status"] == 200 else None), event


def archive(raw, dist, package, version):
    checks = {"sha1": hashlib.sha1(raw).hexdigest() == dist["shasum"]} if dist.get("shasum") else {}
    for candidate in (dist.get("integrity") or "").split():
        algorithm, digest = candidate.split("-", 1)
        checks[algorithm] = base64.b64encode(hashlib.new(algorithm, raw).digest()).decode() == digest
    if not checks or not all(checks.values()):
        raise ValueError(f"integrity failure {package}@{version}: {checks}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        files = {member.name.removeprefix("package/"): tar.extractfile(member).read()
                 for member in tar if member.isfile() and member.name.startswith("package/")}
    manifest = json.loads(files["package.json"])
    if (manifest["name"], manifest["version"]) != (package, version):
        raise ValueError(f"archive name/version mismatch {package}@{version}")
    return files, manifest, checks
