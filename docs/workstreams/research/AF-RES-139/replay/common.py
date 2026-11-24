"""Shared receipts and archive checks adapted from the pinned AF-RES-135 replay."""
import base64
import csv
import hashlib
import io
import json
import pathlib
import subprocess
import tarfile
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKAGE = "simple-statistics"
REGISTRY = "https://registry.npmjs.org/simple-statistics"
UPSTREAM = "https://github.com/simple-statistics/simple-statistics"
GIT_API = "https://api.github.com/repos/simple-statistics/simple-statistics"


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


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def git(repo, *args, missing=False):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
    if result.returncode and not missing:
        raise RuntimeError(result.stderr.decode())
    return result.stdout if result.returncode == 0 else None


class Fetcher:
    def __init__(self, cache):
        self.cache = pathlib.Path(cache)
        self.cache.mkdir(parents=True, exist_ok=True)

    def get(self, url, limit=100_000_000):
        key = sha(url.encode())
        body = self.cache / (key + ".bin")
        meta = self.cache / (key + ".json")
        if meta.exists():
            return (body.read_bytes() if body.exists() else None), json_in(meta) | {"cache_hit": True}
        info = {"url": url, "opened_utc": utc(), "cache_hit": False}
        start = time.perf_counter()
        raw = None
        for attempt in range(1, 4):
            try:
                headers = {"User-Agent": "AF-RES-139 evidence replay", "Accept-Encoding": "identity"}
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
                    content = response.read(limit + 1)
                    if len(content) > limit:
                        raise ValueError("response byte limit exceeded")
                    raw = content
                    info.update(status=response.status, final_url=response.url, bytes=len(raw),
                                sha256=sha(raw), content_type=response.headers.get("Content-Type"),
                                last_modified=response.headers.get("Last-Modified"), link=response.headers.get("Link"))
                break
            except (OSError, ValueError) as error:
                info.update(status=getattr(error, "code", "error"), error=str(error), bytes=None)
                if info["status"] in (403, 404, 410, 451):
                    break
        info.update(attempts=attempt, completed_utc=utc(), wall_ms=(time.perf_counter() - start) * 1000)
        if raw is not None:
            body.write_bytes(raw)
            info.pop("error", None)
        write_json(meta, info)
        return raw, info


def archive(raw, dist, version):
    checks = {"sha1": hashlib.sha1(raw).hexdigest() == dist["shasum"]} if dist.get("shasum") else {}
    integrity = dist.get("integrity", "")
    for candidate in integrity.split():
        algorithm, digest = candidate.split("-", 1)
        checks[algorithm] = base64.b64encode(hashlib.new(algorithm, raw).digest()).decode() == digest
    if not checks or not all(checks.values()):
        raise ValueError(f"integrity failure {version}: {checks}")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        files = {member.name.removeprefix("package/"): tar.extractfile(member).read()
                 for member in tar if member.isfile() and member.name.startswith("package/")}
    manifest = json.loads(files["package.json"])
    if (manifest["name"], manifest["version"]) != (PACKAGE, version):
        raise ValueError(f"archive name/version mismatch {version}")
    return files, manifest, checks
