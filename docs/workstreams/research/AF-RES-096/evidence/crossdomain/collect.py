"""Read pinned upstream primary texts for the Q7 calibration only.

Never accesses Stack Overflow or the experimental jq/Pandoc corpus.
Full fetched text remains in this owned subtree so exact line references can be
rechecked; sources.jsonl is the separately reviewed short-source ledger.
"""
import datetime as dt
import hashlib
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
PINS = {
    "sphinx": ("sphinx-doc/sphinx", "v8.1.3", "a1510de4777eaa2e569435f95b05f6f3293d7035", "2024-10-13T20:23:48Z"),
    "gdal": ("OSGeo/gdal", "v3.10.0", "35a44cc570cdf4dbd55611e4bd61da76e56bc221", "2024-11-01T15:42:59Z"),
    "proj": ("OSGeo/PROJ", "9.5.1", "41f79ccfe107d3951dac6826f289b55d17cc3b81", "2024-12-01T11:34:42Z"),
}

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def fetch(url, name, category="auxiliary"):
    record = {"url": url, "started_utc": now(), "category": category}
    try:
        with urllib.request.urlopen(url, timeout=40) as response:
            raw = response.read()
            record.update(status=response.status, final_url=response.url,
                          sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
        text = raw.decode("utf-8")
        dest = ROOT / "raw" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        record.update(local_path=str(dest.relative_to(ROOT)), success=True)
    except Exception as exc:
        record.update(success=False, error=f"{type(exc).__name__}: {exc}")
        text = None
    record["finished_utc"] = now()
    with (ROOT / "receipts.jsonl").open("a") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False))
    return text

def file(project, path, name):
    repo, tag, sha, date = PINS[project]
    return fetch(f"https://raw.githubusercontent.com/{repo}/{sha}/{path}", name, "Q7-primary-candidate")

if __name__ == "__main__":
    if sys.argv[1] == "trees":
        (ROOT / "pins.json").write_text(json.dumps(PINS, indent=2) + "\n")
        for key, (repo, tag, sha, date) in PINS.items():
            fetch(f"https://api.github.com/repos/{repo}/commits/{sha}", f"metadata/{key}-commit.json")
            text = fetch(f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1", f"metadata/{key}-tree.json")
            if text:
                tree = json.loads(text)
                print(key, "truncated", tree.get("truncated"))
                print("\n".join(x["path"] for x in tree.get("tree", []) if any(token in x["path"].lower() for token in ["graphviz", "osr_ct", "transformation.rst", "network.rst", "gie/basic", "gie/grid", "test_network", "test_factory"]) and x.get("type") == "blob"))
    elif sys.argv[1] == "file":
        file(sys.argv[2], sys.argv[3], sys.argv[4])
