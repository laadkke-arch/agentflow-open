"""Fetch the fixed cross-domain primary files; raw text stays in ignored _cache.

This is a source acquisition utility, not an execution of any upstream tests.
"""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
SPECS = [
    ("XG1", "OSGeo/gdal", "35a44cc570cdf4dbd55611e4bd61da76e56bc221", "doc/source/programs/gdalwarp.rst"),
    ("XG2", "OSGeo/gdal", "35a44cc570cdf4dbd55611e4bd61da76e56bc221", "autotest/utilities/test_gdalwarp_lib.py"),
    ("XG3", "OSGeo/PROJ", "41f79ccfe107d3951dac6826f289b55d17cc3b81", "docs/source/operations/transformations/vgridshift.rst"),
    ("XS1", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "doc/usage/extensions/inheritance.rst"),
    ("XS2", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "tests/test_extensions/test_ext_inheritance_diagram.py"),
    ("XS3", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "tests/roots/test-ext-inheritance_diagram/index.rst"),
    ("XS4", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "sphinx/ext/inheritance_diagram.py"),
    ("XG4", "OSGeo/PROJ", "41f79ccfe107d3951dac6826f289b55d17cc3b81", "docs/source/resource_files.rst"),
    ("XS5", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "tests/roots/test-inheritance/dummy/test.py"),
    ("XS6", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "tests/roots/test-inheritance/diagram_w_2_top_classes.rst"),
    ("XS7", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "tests/roots/test-inheritance/diagram_module_w_2_top_classes.rst"),
    ("XS8", "sphinx-doc/sphinx", "a1510de4777eaa2e569435f95b05f6f3293d7035", "doc/usage/extensions/graphviz.rst"),
    ("XV1", "graphviz/graphviz.gitlab.io", "51d048c433e5a80ab51915876b695c971544fe54", "content/en/docs/cli/_index.md"),
]

def fetch(spec):
    sid, repo, commit, path = spec
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"
    fixed = f"https://github.com/{repo}/blob/{commit}/{path}"
    if repo == "graphviz/graphviz.gitlab.io":
        url = f"https://gitlab.com/{repo}/-/raw/{commit}/{path}"
        fixed = f"https://gitlab.com/{repo}/-/blob/{commit}/{path}"
    rec = {"source_id": sid, "repo": repo, "commit": commit, "path": path,
           "direct_url": url, "fixed_url": fixed,
           "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            raw = response.read(); status = response.status
        text = raw.decode("utf-8")
        target = ROOT / "_cache" / f"{sid}{Path(path).suffix}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        rec.update(status=status, body_sha256=hashlib.sha256(raw).hexdigest(),
                   git_blob_sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest(),
                   bytes=len(raw), chars=len(text), lines=len(text.splitlines()),
                   cached_body=str(target.relative_to(ROOT)))
    except Exception as exc:
        rec.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    rec["checked_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return rec

if __name__ == "__main__":
    receipts = ROOT / "acquisition-receipts.jsonl"
    prior = {}
    if receipts.exists():
        prior = {r["source_id"]: r for r in map(json.loads, receipts.read_text().splitlines())}
    missing = []
    for spec in SPECS:
        row = prior.get(spec[0])
        cached = ROOT / row["cached_body"] if row and row.get("cached_body") else None
        if cached and cached.exists():
            assert hashlib.sha256(cached.read_bytes()).hexdigest() == row["body_sha256"], spec[0]
        else:
            missing.append(spec)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, missing))
    with receipts.open("a") as stream:
        for row in rows:
            previous = prior.get(row["source_id"])
            if previous and previous.get("body_sha256") and row.get("body_sha256"):
                assert previous["body_sha256"] == row["body_sha256"], row["source_id"]
            stream.write(json.dumps(row, ensure_ascii=False)+"\n")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    print(json.dumps({"verified_existing": len(SPECS)-len(missing), "fetched": len(rows),
                      "upstream_tests_executed": 0}))
