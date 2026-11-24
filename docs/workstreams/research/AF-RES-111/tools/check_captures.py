"""Reopen the public originals and compare their pinned character ranges."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from verify import ROOT, jsonl


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "AF-RES-111 evidence reproduction"})
    with urllib.request.urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8"), response.geturl()


def reopen(source):
    """Read the original issue and code publication surfaces only."""
    url = source["source_url"]
    if "github.com/" in url and "/issues/" in url:
        html, arrival = download(url)
        embedded = re.search(
            r'<script[^>]*data-target="react-app.embeddedData"[^>]*>(.*?)</script>', html, re.S
        )
        if embedded is None:
            raise ValueError("GitHub embedded issue body unavailable")
        data = json.loads(embedded.group(1))
        issue = data["payload"]["issueViewerRoute"]["data"]["repository"]["issue"]
        return {"body": issue["body"], "title": issue["title"]}, arrival, issue["updatedAt"]
    if "gitlab.com/" in url and any(part in url for part in ("/-/issues/", "/-/work_items/")):
        raw, arrival = download(source["actual_url"])
        issue = json.loads(raw)
        return {"body": issue["description"], "title": issue["title"]}, arrival, issue["updated_at"]
    if "github.com/" in url and "/blob/" in url:
        url = url.replace("github.com/", "raw.githubusercontent.com/").replace("/blob/", "/")
    elif "gitlab.com/" in url and "/-/blob/" in url:
        url = url.replace("/-/blob/", "/-/raw/")
    text, arrival = download(url)
    return {"body": text}, arrival, source["edition"]


def verify_public():
    facts = jsonl(ROOT / "facts.jsonl")
    seeds = {x["case_id"]: x for x in json.loads((ROOT / "evidence" / "writer-seeds.json").read_text())}
    sources = {s["source_id"]: s for s in jsonl(ROOT / "sources.jsonl")}
    needles = {}
    for case in facts:
        cid = case["case_id"]
        for part in seeds[cid]["source_segments"]:
            needles.setdefault(cid, []).append({
                "id": cid + "/" + part["condition"], "field": part["field"], "quote": part["quote"],
                "start": part["start"], "end": part["end"], "sha256": part["field_sha256"],
            })
        for f in case["evidence"]:
            src = f["source"]
            needles.setdefault(src["source_id"], []).append({
                "id": f["evidence_id"], "field": "body", "quote": src["quote"],
                "start": src["origin_start"], "end": src["origin_end"], "sha256": src["origin_sha256"],
            })

    def check(sid):
        try:
            body, arrival, version = reopen(sources[sid])
            rows = []
            for part in needles[sid]:
                text = body[part["field"]]
                left, right = part["start"], part["end"]
                rows.append({"id": part["id"], "span": [left, right],
                             "origin_sha256": digest(text), "expected_origin_sha256": part["sha256"],
                             "match": text[left:right] == part["quote"] and digest(text) == part["sha256"]})
            return {"source_id": sid, "arrival": arrival, "version": version, "status": "read",
                    "utc": datetime.now(timezone.utc).isoformat(), "spans": rows}
        except (ValueError, OSError, KeyError) as exc:
            return {"source_id": sid, "status": "unavailable", "error": str(exc),
                    "utc": datetime.now(timezone.utc).isoformat(), "spans": []}

    with ThreadPoolExecutor(max_workers=5) as group:
        records = list(group.map(check, sorted(needles)))
    expected = sum(len(v) for v in needles.values())
    verified = sum(p["match"] for rec in records for p in rec["spans"])
    return {"expected": expected, "verified": verified, "sources": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = verify_public()
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"public origin spans {result['verified']}/{result['expected']}")
    if result["expected"] != result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
