"""Public read-only acquisition. Later revisions/status are never printed in stage 1."""
import datetime
import hashlib
import html
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

BASE = Path(__file__).resolve().parents[2]
CACHE = BASE / ".cache/imagemagick"
OUT = BASE / "evidence/imagemagick"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def main():
    qs = json.loads((OUT / "questions-h1-masked.json").read_text())["items"]
    ids = ";".join(str(q["question_id"]) for q in qs)
    receipts, revisions = [], []
    for page in range(1, 11):
        url = f"https://api.stackexchange.com/2.3/posts/{ids}/revisions?site=stackoverflow&filter=withbody&pagesize=100&page={page}"
        fetched = now()
        try:
            response = urllib.request.urlopen(url, timeout=45)
            raw = response.read()
            data = json.loads(raw)
        except Exception as error:
            (OUT / f"failure-h1-revisions-{page}.json").write_text(json.dumps({"url":url,"utc":fetched,"error":str(error)},indent=2))
            raise
        (CACHE / f"revisions-h1-{page}.json").write_bytes(raw)
        receipts.append({"url":url,"utc":fetched,"status":response.status,"sha256":hashlib.sha256(raw).hexdigest(),"items":len(data.get("items",[])),"has_more":data.get("has_more"),"quota_remaining":data.get("quota_remaining"),"backoff":data.get("backoff")})
        revisions.extend(data.get("items", []))
        if data.get("backoff"):
            time.sleep(min(data["backoff"],60))
        if not data.get("has_more"):
            break
    else:
        raise RuntimeError("revision paging incomplete after 10 pages")
    (OUT / "acquisition-h1.json").write_text(json.dumps(receipts,ensure_ascii=False,indent=2))
    initial=[]
    for rank,q in enumerate(qs,1):
        found=[r for r in revisions if r.get("post_id")==q["question_id"] and r.get("revision_number")==1 and "body" in r]
        found.sort(key=lambda r:(r.get("creation_date",0),r.get("revision_guid","")))
        first=found[0] if found else None
        rec={"rank":rank,"current_metadata":q,"first_revision":first,"revision1_variants":len(found),"raw_first_body_sha256":hashlib.sha256(first["body"].encode()).hexdigest() if first else None}
        initial.append(rec)
    (CACHE / "initial-h1.json").write_text(json.dumps(initial,ensure_ascii=False,indent=2))
    lines=[]
    for rec in initial:
        q=rec["current_metadata"]; r=rec["first_revision"]
        lines += [f"## Rank {rec['rank']} / {q['question_id']} / current title: {html.unescape(q['title'])}",f"Current tags: {q['tags']}"]
        if r:
            lines += [f"First revision: {r.get('revision_guid')} / {r.get('creation_date')} / title: {r.get('title')} / tags: {r.get('tags')}",r['body']]
        else:
            lines += ["FIRST REVISION MISSING"]
    (CACHE / "initial-h1-readable.md").write_text("\n\n".join(lines))
    print(json.dumps({"pages":len(receipts),"questions":len(initial),"initial_missing":[r["current_metadata"]["question_id"] for r in initial if not r["first_revision"]],"cross_tag_ids":[r["current_metadata"]["question_id"] for r in initial if "typst" in r["current_metadata"].get("tags",[]) or "typst" in (r["first_revision"] or {}).get("tags",[])],"quotas":[r["quota_remaining"] for r in receipts]}))

if __name__ == "__main__":
    main()
