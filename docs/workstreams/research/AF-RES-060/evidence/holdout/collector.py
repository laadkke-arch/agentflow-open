#!/usr/bin/env python3
"""AF-RES-060 public first-revision collector. No network before stage2 gate."""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
TAGS = ("jsonschema", "json-ld")
FROM = 1688169600
TO = 1704067199
API = "https://api.stackexchange.com/2.3"


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def gate():
    p = ROOT / "stage2-gate.json"
    if not p.exists():
        raise SystemExit("BLOCKED: root has not provided stage2-gate.json")
    g = json.loads(p.read_text())
    if g.get("root_confirmed") is not True or not re.fullmatch(r"[0-9a-f]{40}", g.get("stage2_remote_sha", "")):
        raise SystemExit("BLOCKED: stage2 gate lacks root-confirmed remote SHA")
    return g


def get_api(route, params):
    gate()
    url = API + route + "?" + urlencode(params)
    started = now()
    receipt = {"url": url, "opened_utc": started, "endpoint_role": "question_metadata" if route == "/questions" else "question_revision"}
    try:
        with urlopen(Request(url, headers={"User-Agent": "AF-RES-060 public-source research"}), timeout=25) as response:
            body = response.read()
            receipt.update(http_status=response.status, bytes=len(body), response_sha256=hashlib.sha256(body).hexdigest())
        payload = json.loads(body)
        # Log technical envelope only: never answer statistics, users, or comments.
        for k in ("has_more", "backoff", "quota_remaining", "error_id", "error_name", "error_message"):
            if k in payload:
                receipt[k] = payload[k]
        receipt["completed_utc"] = now()
        with (ROOT / "requests.jsonl").open("a") as out:
            out.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        if "error_id" in payload:
            raise RuntimeError("API error: " + str(payload.get("error_name")))
        # Do not ignore server backoff or use alternate identities.
        if payload.get("backoff", 0):
            seconds = payload["backoff"]
            if seconds > 55:
                raise RuntimeError(f"backoff {seconds}s exceeds this bounded collection call; resume after required delay")
            time.sleep(seconds)
        return payload
    except Exception as exc:
        if "completed_utc" not in receipt:
            receipt.update(completed_utc=now(), error_type=type(exc).__name__, error=str(exc))
            with (ROOT / "requests.jsonl").open("a") as out:
                out.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        raise


def safe_question(item):
    return {k: item[k] for k in ("question_id", "creation_date", "tags", "title", "link") if k in item}


def collect_frame():
    g = gate()
    if (ROOT / "frame.json").exists():
        raise SystemExit("Frame already frozen locally; inspect it rather than overwrite")
    frames = []
    for tag in TAGS:
        questions = {}
        page = 1
        envelope = []
        while True:
            payload = get_api("/questions", {"site": "stackoverflow", "tagged": tag, "fromdate": FROM, "todate": TO, "sort": "creation", "order": "asc", "pagesize": 100, "page": page})
            received = [safe_question(x) for x in payload.get("items", [])]
            for q in received:
                questions[q["question_id"]] = q
            ordered = sorted(questions.values(), key=lambda q: (q["creation_date"], q["question_id"]))
            envelope.append({"page": page, "metadata_items_received": len(received), "has_more": payload.get("has_more", False)})
            if not payload.get("has_more"):
                break
            if len(ordered) >= 20 and received and max(q["creation_date"] for q in received) > ordered[19]["creation_date"]:
                break
            page += 1
            if page > 20:
                raise RuntimeError("Unresolved tie boundary after 20 metadata pages; preserve gap")
        rows = []
        for rank, q in enumerate(ordered[:20], 1):
            rows.append({"tag": tag, "rank": rank, **q, "created_utc": dt.datetime.fromtimestamp(q["creation_date"], dt.timezone.utc).isoformat(), "current_tags": q.get("tags", [])})
        frames.append({"tag": tag, "rows": rows, "metadata_page_envelope": envelope, "unfilled_frame_positions": max(0, 20-len(rows))})
    write_json(ROOT / "frame.json", {"stage2_remote_sha": g["stage2_remote_sha"], "frozen_utc": now(), "fromdate": FROM, "todate": TO, "order": ["creation_date", "question_id"], "frames": frames})
    print(json.dumps({"frame_frozen": True, "counts": {f['tag']: len(f['rows']) for f in frames}}, ensure_ascii=False))


def collect_bodies(tag):
    gate()
    frame = json.loads((ROOT / "frame.json").read_text())
    # A question may occur in both canonical-tag frames. Recruitment rows are
    # keyed by (tag, question_id), while the immutable first-body cache is keyed
    # by question_id and may be reused without erasing either frame position.
    current = {(x["tag"], x["question_id"]): x for x in json.loads((ROOT / "revision-index.json").read_text())} if (ROOT / "revision-index.json").exists() else {}
    rows = next(x["rows"] for x in frame["frames"] if x["tag"] == tag)
    for q in rows:
        qid = q["question_id"]
        row_key = (tag, qid)
        if row_key in current:
            continue
        record = {"tag": tag, "rank": q["rank"], "question_id": qid, "created_utc": q["created_utc"], "current_tags": q["current_tags"], "current_title": html.unescape(q.get("title", "")), "url": q.get("link", f"https://stackoverflow.com/questions/{qid}"), "initial_revision_url": f"https://stackoverflow.com/revisions/{qid}/1", "read_status": "not_read", "body_work_id": f"SO-question-{qid}", "body_cache_reused": False}
        prior_same_body = next((r for r in current.values() if r["question_id"] == qid and r.get("body_sha256") and (ROOT / ".cache" / f"{qid}.json").exists()), None)
        if prior_same_body:
            for key in ("revision_guid", "revision_number", "initial_title", "initial_tags", "initial_tags_status", "body_sha256", "body_utf8_bytes", "first_revision_records", "first_revision_body_records"):
                if key in prior_same_body:
                    record[key] = prior_same_body[key]
            record.update(body_cache_reused=True, reused_from_row={"tag": prior_same_body["tag"], "rank": prior_same_body["rank"], "question_id": qid}, acquisition_status="first_revision_cache_reused_not_yet_read", acquisition_utc=now(), lineage_note="Same question/first revision is one external work; both tag-frame positions remain. Acquisition reuse does not mark either screening row read.")
            current[row_key] = record
            write_json(ROOT / "revision-index.json", sorted(current.values(), key=lambda r: (TAGS.index(r['tag']), r['rank'])))
            print(json.dumps({"tag":tag,"rank":q['rank'],"question_id":qid,"acquisition_status":record['acquisition_status'],"reused_from_tag":prior_same_body['tag']},ensure_ascii=False),flush=True)
            continue
        try:
            page = 1
            initial = []
            while True:
                payload = get_api(f"/posts/{qid}/revisions", {"site": "stackoverflow", "filter": "withbody", "pagesize": 100, "page": page})
                # Keep first revision only; no user, editor comment, vote/answer data.
                for r in payload.get("items", []):
                    if r.get("revision_number") == 1:
                        initial.append({k:r[k] for k in ("revision_guid", "revision_number", "revision_type", "creation_date", "post_id", "post_type", "body", "title", "tags") if k in r})
                if not payload.get("has_more"):
                    break
                page += 1
                if page > 20:
                    raise RuntimeError("initial revision not resolved within 20 revision pages")
            candidates = [r for r in initial if r.get("body")]
            if not candidates:
                record.update(read_status="unavailable", gap="revision_number=1 body absent; no current-body replacement")
            else:
                candidates.sort(key=lambda r: (r.get("creation_date", 0), r.get("revision_guid", "")))
                selected = candidates[0]
                body = selected["body"]
                record.update(revision_guid=selected.get("revision_guid"), revision_number=1, initial_title=html.unescape(selected.get("title", "")), initial_tags=selected.get("tags"), initial_tags_status="present" if "tags" in selected else "not_in_initial_payload", body_sha256=hashlib.sha256(body.encode()).hexdigest(), body_utf8_bytes=len(body.encode()), acquisition_status="first_revision_acquired_not_yet_read", acquisition_utc=now(), first_revision_records=len(initial), first_revision_body_records=len(candidates))
                # Transient direct-reading cache only; ignored by Git.
                write_json(ROOT / ".cache" / f"{qid}.json", selected)
        except Exception as exc:
            record.update(read_status="unavailable", gap=f"{type(exc).__name__}: {exc}")
        current[row_key] = record
        write_json(ROOT / "revision-index.json", sorted(current.values(), key=lambda r: (TAGS.index(r['tag']), r['rank'])))
        print(json.dumps({"tag": tag, "rank": q['rank'], "question_id": qid, "acquisition_status":record.get('acquisition_status',record['read_status'])},ensure_ascii=False),flush=True)


def show_bodies(tag, start, stop):
    gate()
    rows = json.loads((ROOT / "revision-index.json").read_text())
    for r in rows:
        if r['tag'] != tag or not start <= r['rank'] <= stop:
            continue
        p = ROOT / ".cache" / f"{r['question_id']}.json"
        if not p.exists():
            print(json.dumps(r,ensure_ascii=False))
            continue
        d = json.loads(p.read_text())
        print(json.dumps({"tag":tag,"rank":r['rank'],"question_id":r['question_id'],"revision_guid":r['revision_guid'],"current_tags":r['current_tags'],"initial_tags":r['initial_tags'],"initial_title":r['initial_title'],"body":d['body']},ensure_ascii=False,indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['show-plan','collect-frame','collect-bodies','show-bodies'])
    p.add_argument('--tag', choices=TAGS)
    p.add_argument('--start',type=int,default=1)
    p.add_argument('--stop',type=int,default=20)
    args = p.parse_args()
    if args.action == 'show-plan':
        print(json.dumps({'network_requests':0,'tags':TAGS,'fromdate':FROM,'todate':TO,'first_per_tag':20,'sort':['creation_date','question_id'],'gate_present':(ROOT/'stage2-gate.json').exists()}))
    elif args.action == 'collect-frame':
        collect_frame()
    elif args.action == 'collect-bodies':
        if not args.tag: p.error('--tag required')
        collect_bodies(args.tag)
    elif args.action == 'show-bodies':
        if not args.tag: p.error('--tag required')
        show_bodies(args.tag,args.start,args.stop)


if __name__ == '__main__':
    main()
