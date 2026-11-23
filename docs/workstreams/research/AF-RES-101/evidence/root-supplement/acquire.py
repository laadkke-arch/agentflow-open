"""Re-fetch explicitly recorded public sources into ignored cache; no recoding."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import io
import json
import tarfile
import urllib.request

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
CACHE = ROOT / ".cache/root-supplement"
CACHE.mkdir(parents=True, exist_ok=True)
old = json.loads((OUT / "acquisition.json").read_text())


def fetch(rec):
    r = {"id": rec["id"], "url": rec["url"], "accessed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(r["url"], headers={"User-Agent": "AF-RES-101 public-source reproduction"}), timeout=40) as response:
            data = response.read()
            r["status"] = response.status
        (CACHE / (r["id"] + ".raw")).write_bytes(data)
        r.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        r["matches_recorded_sha256"] = r["sha256"] == rec["sha256"]
        if r["id"] == "quick-magick-package":
            with tarfile.open(fileobj=io.BytesIO(data)) as gem:
                payload = gem.extractfile("data.tar.gz").read()
            with tarfile.open(fileobj=io.BytesIO(payload)) as package:
                code = package.extractfile("lib/quick_magick/image.rb").read()
            (CACHE / "quick-magick-package-image.rb").write_bytes(code)
            r["file_sha256"] = hashlib.sha256(code).hexdigest()
        if r["id"] == "rubygems-quick-magick":
            r["mutable_registry_metadata"] = True
    except Exception as error:
        r["error"] = repr(error)
    return r


rows = list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(fetch, [r for r in old if "sha256" in r]))
(CACHE / "acquisition-replay.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
raise SystemExit(1 if any("error" in r or (not r.get("matches_recorded_sha256") and not r.get("mutable_registry_metadata")) for r in rows) else 0)
