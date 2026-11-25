"""Compare pinned evidence to an independent browser and extraction run."""
import argparse
import hashlib
import json
from pathlib import Path
import re

BROWSER_KEYS = ("load", "callbacks", "geometry", "materials", "textureSelections", "draw",
                "frame", "decode", "extensionsRequired", "decoder", "graphics", "error")
LOOPBACK = re.compile(r"http://127\.0\.0\.1:\d+")
BLOB = re.compile(r"(blob:http://loopback/)[\da-f-]{36}", re.I)


def json_read(path):
    return json.loads(path.read_text())


def normalize(text):
    text = LOOPBACK.sub("http://loopback", text)
    return BLOB.sub(r"\1<id>", text)


def signature(data):
    outcome = data["outcome"]
    result = {k: outcome[k] for k in BROWSER_KEYS if k in outcome}
    result["server"] = sorted((e["category"], e["url"], e["status"], e["bodyBytes"], e["bodySha256"])
                              for e in data["serverHttp"])
    result["browser_http"] = sorted((e["event"], normalize(e["url"]), e.get("status", 0), e.get("error") or "")
                                    for e in data["browserHttp"] if e["url"].startswith(("http:", "https:")))
    result["non2xxWithoutFinish"] = sorted((normalize(e["url"]), e["status"]) for e in data["non2xxWithoutFinish"])
    result["console"] = sorted((e["type"], normalize(e["text"])) for e in data["console"])
    result["blocked"] = data["blocked"]
    result["entrySha256"] = data.get("sha256")
    result["case"] = data["id"]
    result["probe"] = outcome if data["id"] == "offline-probe" else None
    return json.loads(normalize(json.dumps(result, ensure_ascii=False)))


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def compare_round(archived, clean, number):
    rdir = f"round-{number}"
    env = json_read(clean / rdir / "environment.json")
    stored = json_read(archived / rdir / "environment.json")
    for key in ("chromium", "playwright", "node", "architecture", "flags"):
        assert env[key] == stored[key], (rdir, key)
    cases = env["cases"] + ["offline-probe"]
    for case in cases:
        base = json_read(archived / rdir / f"{case}.json")
        copy = json_read(clean / rdir / f"{case}.json")
        assert not any(copy.get(k) for k in ("executionError", "outstandingRequests", "pageErrors"))
        a, b = signature(base), signature(copy)
        for key in set(a) | set(b):
            assert a.get(key) == b.get(key), (rdir, case, key, a.get(key), b.get(key))
        f = copy["outcome"].get("frame", {}).get("png") if copy["outcome"].get("frame") else None
        if f:
            assert f["sha256"] == sha(clean / rdir / f["path"]) == sha(archived / rdir / f["path"])
        print(f"equal {rdir}/{case} HTTP, result, frame{' (+PNG)' if f else ''}")
    return len(cases)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("evidence", type=Path)
    cli.add_argument("clean", type=Path)
    cli.add_argument("rounds", type=int, nargs="+", choices=(1,2))
    args = cli.parse_args()
    archived, clean = args.evidence / "receipts", args.clean
    a = json_read(archived / "input-manifest.json")
    b = json_read(clean / "input-manifest.json")
    assert a["epub_archive"] == b["epub_archive"]
    keys = ("group", "path", "git_blob", "bytes", "sha256")
    assert [tuple(row[k] for k in keys) for row in a["files"]] == [tuple(row[k] for k in keys) for row in b["files"]]
    print(f"equal {len(a['files'])} input/runtime files and EPUB archive")
    for output in ("python-static.json", "node-static.json"):
        assert json_read(archived / output)["entries"] == json_read(clean / output)["entries"], output
    for key in ("archive_sha256", "python", "infozip"):
        assert json_read(archived / "epub-read.json")[key] == json_read(clean / "epub-read.json")[key]
    a = json_read(archived / "validator.json")
    b = json_read(clean / "validator.json")
    assert a["version"] == b["version"]
    for left, right in zip(a["results"], b["results"], strict=True):
        assert left["id"] == right["id"] and left["entrySha256"] == right["entrySha256"]
        # The validator loads external resources concurrently. Compare relative names and their results.
        assert sorted(left["calls"], key=lambda c: c["relative"]) == sorted(right["calls"], key=lambda c: c["relative"])
        assert left["report"]["issues"] == right["report"]["issues"], left["id"]
    print("equal both container extractors, EPUB extraction and validator observations")
    count = sum(compare_round(archived, clean, round_id) for round_id in args.rounds)
    print(f"equal {count} browser cases including probes")


if __name__ == "__main__":
    main()
