#!/usr/bin/env python3
"""Post-seal2 public follow-ups for the eight preregistered AF-RES-100 cases.

Run `python -B .../fetch_public_outcomes.py fetch` once, then use `read --case
J1 --part answers|questions|comments|timeline`. Full third-party payloads remain
under the ignored evidence/_cache/resume2-outcomes directory. This script does
not execute jq, Pandoc, Docker, R, Typst, or any submitted code.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
CACHE = ROOT / "evidence/_cache/resume2-outcomes"
BASE = "https://api.stackexchange.com/2.3/"
SEALED_COMMIT = "5d81bcbeb5f1248fc1dd2ce2d825cf6467353673"
REV_FILTER = "!1emQP-6jyLbLgZ0cpDxNT(1d"
SOURCES = OUT / "sources.jsonl"


def utc(ts=None):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat() if ts is not None else dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def cases():
    return json.loads((ROOT / "protocol.json").read_text())["cases"]


class Client:
    def __init__(self):
        OUT.mkdir(parents=True, exist_ok=True)
        CACHE.mkdir(parents=True, exist_ok=True)
        self.sources = [json.loads(x) for x in SOURCES.read_text().splitlines()] if SOURCES.exists() else []
        self.by_url = {x["url"]: x for x in self.sources if x.get("status") == "success"}
        self.not_before = 0.0
        self.failures = []

    def record(self, row):
        row["source_id"] = f"SO-API-{len(self.sources)+1:04d}"
        self.sources.append(row)
        with SOURCES.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return row

    def request(self, path, params):
        url = BASE + path + "?" + urllib.parse.urlencode(params)
        previous = self.by_url.get(url)
        if previous and (ROOT / previous["cache_path"]).exists():
            data = json.loads((ROOT / previous["cache_path"]).read_bytes())
            return data, previous
        while time.time() < self.not_before:
            remaining = self.not_before - time.time()
            print(f"API backoff: waiting {remaining:.1f}s", flush=True)
            time.sleep(min(remaining, 30))
        started = utc()
        row = {"kind": "api_response", "url": url, "started_utc": started,
               "post_seal_commit": SEALED_COMMIT, "request_method": "GET"}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AF-RES-100-postseal-public-followup-research/1.0"})
            with urllib.request.urlopen(req, timeout=40) as response:
                raw = response.read()
                row["http_status"] = response.status
                row["response_date"] = response.headers.get("Date")
            data = json.loads(raw)
            filename = "response-" + sha(url)[:20] + ".json"
            (CACHE / filename).write_bytes(raw)
            row.update(cache_path=str((CACHE / filename).relative_to(ROOT)), sha256=sha(raw),
                       bytes=len(raw), finished_utc=utc(), item_count=len(data.get("items", [])),
                       has_more=data.get("has_more"), quota_remaining=data.get("quota_remaining"),
                       backoff_seconds=data.get("backoff", 0), status="success")
            if data.get("backoff"):
                self.not_before = time.time() + data["backoff"]
            if "error_id" in data:
                row.update(status="api_error", error_id=data["error_id"], error_name=data.get("error_name"), error_message=data.get("error_message"))
            receipt = self.record(row)
            if row["status"] != "success":
                self.failures.append(receipt)
                return {}, receipt
            self.by_url[url] = receipt
            print(f"{receipt['source_id']}: {path}, {row['item_count']} items, quota {row['quota_remaining']}", flush=True)
            return data, receipt
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            row.update(status="fetch_error", finished_utc=utc(), error_type=type(exc).__name__, error_message=str(exc))
            if isinstance(exc, urllib.error.HTTPError):
                row["http_status"] = exc.code
                raw = exc.read()
                filename = "failed-" + sha(url)[:20] + ".txt"
                (CACHE / filename).write_bytes(raw)
                row.update(cache_path=str((CACHE / filename).relative_to(ROOT)), sha256=sha(raw), bytes=len(raw))
                retry_after = exc.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    row["retry_after_seconds"] = int(retry_after)
                    self.not_before = time.time() + int(retry_after)
            receipt = self.record(row)
            self.failures.append(receipt)
            print(f"FETCH FAILURE {receipt['source_id']}: {exc}", flush=True)
            return {}, receipt

    def pages(self, path, **extra):
        items = []
        for page in range(1, 101):
            params = {"site": "stackoverflow", "pagesize": 100, "page": page, **extra}
            data, receipt = self.request(path, params)
            for item in data.get("items", []):
                item["_source_id"] = receipt["source_id"]
                item["_api_url"] = receipt["url"]
                items.append(item)
            if not data.get("has_more"):
                break
        else:
            raise RuntimeError("Pagination safety limit reached; retrieval is incomplete")
        return items


def role(user_id, qowner, aowner=None):
    if user_id is None:
        return "unknown_or_deleted"
    if user_id == qowner:
        return "questioner"
    if aowner is not None and (user_id == aowner or isinstance(aowner, (set, list, tuple)) and user_id in aowner):
        return "answerer"
    return "other_participant"


def public_meta(item, qowner, aowner=None):
    allowed = ("question_id", "answer_id", "post_id", "post_type", "comment_id", "revision_guid",
               "revision_number", "revision_type", "creation_date", "last_edit_date", "last_activity_date",
               "is_accepted", "accepted_answer_id", "answer_count", "comment_count", "link",
               "timeline_type", "detail", "post_link", "content_license", "is_rollback", "set_community_wiki",
               "_source_id", "_api_url", "_metadata_source_id", "_metadata_api_url")
    result = {k: item[k] for k in allowed if k in item}
    user = item.get("owner", item.get("user", {}))
    uid = user.get("user_id")
    result.update(author_user_id=uid, author_role=role(uid, qowner, aowner))
    for field in ("creation_date", "last_edit_date", "last_activity_date"):
        if field in item:
            result[field.replace("_date", "_utc")] = utc(item[field])
    for field in ("body", "last_body", "title", "last_title", "comment"):
        if field in item:
            result[field + "_sha256"] = sha(item[field])
            result[field + "_chars"] = len(item[field])
    if "revision_guid" in item:
        result["revision_url"] = f"https://stackoverflow.com/revisions/{item['revision_guid']}/view-source"
    if "comment_id" in item:
        result["comment_url"] = f"https://stackoverflow.com/questions/{item['post_id']}#comment{item['comment_id']}_{item['post_id']}"
    return result


def fetch():
    selected = cases()
    client = Client()
    ids = ";".join(str(c["question_id"]) for c in selected)
    questions = client.pages(f"questions/{ids}", filter="withbody", sort="creation", order="asc")
    answers = client.pages(f"questions/{ids}/answers", filter="withbody", sort="creation", order="asc")
    accepted_ids = {q.get("accepted_answer_id") for q in questions} - {None}
    missing_accepted = accepted_ids - {a["answer_id"] for a in answers}
    if missing_accepted:
        answers += client.pages("answers/" + ";".join(map(str, sorted(missing_accepted))), filter="withbody")
    posts = [q["question_id"] for q in questions] + [a["answer_id"] for a in answers]
    revisions = client.pages("posts/" + ";".join(map(str, posts)) + "/revisions", filter=REV_FILTER) if posts else []
    # The frozen-revision filter deliberately omitted editor identities in the
    # blinded phase. Fetch ordinary revision metadata only after the seal, and
    # retain separate provenance for body bytes and editor attribution.
    revision_metadata = client.pages("posts/" + ";".join(map(str, posts)) + "/revisions", filter="withbody") if posts else []
    meta_by_guid = {r["revision_guid"]: r for r in revision_metadata}
    for rev in revisions:
        meta = meta_by_guid.get(rev["revision_guid"], {})
        for key, value in meta.items():
            if not key.startswith("_") and key not in {"body", "last_body"}:
                rev[key] = value
        if meta:
            rev["_metadata_source_id"] = meta["_source_id"]
            rev["_metadata_api_url"] = meta["_api_url"]
    bundle = {"post_seal_commit": SEALED_COMMIT, "retrieved_utc": utc(), "cases": [], "failures": []}
    index = {"post_seal_commit": SEALED_COMMIT, "retrieved_utc": utc(), "followup_window_days": 30,
             "window_policy": "Inclusive question-creation through creation plus 30*86400 seconds. Current answers and all returned revisions are recorded separately with in_window flags.",
             "cases": []}
    for case in selected:
        qid = case["question_id"]
        q = next((q for q in questions if q["question_id"] == qid), None)
        case_answers = [a for a in answers if a["question_id"] == qid]
        start = int(dt.datetime.fromisoformat(case["creation_utc"]).timestamp())
        end = start + 30 * 86400
        pids = [qid] + [a["answer_id"] for a in case_answers]
        comments = client.pages("posts/" + ";".join(map(str, pids)) + "/comments", filter="withbody", sort="creation", order="asc", fromdate=start, todate=end)
        timeline = client.pages(f"questions/{qid}/timeline", fromdate=start, todate=end)
        revs = [r for r in revisions if r.get("post_id") in pids]
        qowner = (q or {}).get("owner", {}).get("user_id")
        aowners = {a["answer_id"]: a.get("owner", {}).get("user_id") for a in case_answers}
        answerer_ids = set(aowners.values()) - {None}
        raw_case = {"case_id": case["case_id"], "question_id": qid, "window_start_utc": utc(start),
                    "window_end_utc": utc(end), "question": q, "answers": case_answers,
                    "revisions": revs, "comments": comments, "timeline": timeline}
        bundle["cases"].append(raw_case)
        meta = {k: v for k, v in raw_case.items() if k not in {"question", "answers", "revisions", "comments", "timeline"}}
        meta["question"] = public_meta(q, qowner) if q else None
        for field in ("answers", "revisions", "comments", "timeline"):
            meta[field] = []
            for item in raw_case[field]:
                pid = item.get("post_id", item.get("answer_id"))
                m = public_meta(item, qowner, answerer_ids)
                m["within_30_days"] = start <= item.get("creation_date", -1) <= end
                if "comment_id" in item:
                    m["comment_url"] = f"https://stackoverflow.com/questions/{qid}#comment{item['comment_id']}_{item['post_id']}"
                meta[field].append(m)
        original = ROOT / f"evidence/_cache/requests/{qid}.html"
        if original.exists():
            original_body = original.read_text(encoding="utf-8")
            meta["original_body_sha256"] = sha(original_body)
            meta["current_equals_original_body"] = q is not None and sha(q.get("body", "")) == sha(original_body)
        index["cases"].append(meta)
    bundle["failures"] = client.failures
    index["failures"] = client.failures
    (CACHE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "retrieval-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(bundle["cases"]), "questions": len(questions), "answers": len(answers), "revisions": len(revisions), "failures": len(client.failures)}, indent=2))


def read(case_id, part):
    data = json.loads((CACHE / "bundle.json").read_text())
    c = next(c for c in data["cases"] if c["case_id"] == case_id)
    qowner = (c["question"] or {}).get("owner", {}).get("user_id")
    aowners = {a["answer_id"]: a.get("owner", {}).get("user_id") for a in c["answers"]}
    answerer_ids = set(aowners.values()) - {None}
    print(json.dumps({k: c[k] for k in ("case_id", "question_id", "window_start_utc", "window_end_utc")}, indent=2))
    if part == "questions":
        original = ROOT / f"evidence/_cache/requests/{c['question_id']}.html"
        print("FROZEN ORIGINAL\n" + original.read_text())
        print("CURRENT QUESTION METADATA\n" + json.dumps(public_meta(c["question"], qowner), indent=2))
        revs = sorted([r for r in c["revisions"] if r.get("post_id") == c["question_id"]], key=lambda r: (r.get("creation_date", 0), r.get("revision_number", 0)))
        previous = original.read_text()
        for rev in revs:
            print("REVISION\n" + json.dumps(public_meta(rev, qowner, answerer_ids), indent=2))
            if "comment" in rev:
                print("EDIT COMMENT " + rev["comment"])
            if "title" in rev:
                print("TITLE " + rev["title"])
            if "body" in rev and rev["body"] != previous:
                print("".join(difflib.unified_diff(previous.splitlines(True), rev["body"].splitlines(True), fromfile="prior", tofile="revision")))
                previous = rev["body"]
    elif part == "answers":
        for answer in sorted(c["answers"], key=lambda x: x["creation_date"]):
            aid = answer["answer_id"]
            print("CURRENT ANSWER\n" + json.dumps(public_meta(answer, qowner, aowners[aid]), indent=2))
            print(answer.get("body", "[body absent]"))
            previous = None
            for rev in sorted([r for r in c["revisions"] if r.get("post_id") == aid], key=lambda r: (r.get("creation_date", 0), r.get("revision_number", 0))):
                print("ANSWER REVISION\n" + json.dumps(public_meta(rev, qowner, aowners[aid]), indent=2))
                if "comment" in rev:
                    print("EDIT COMMENT " + rev["comment"])
                if "body" in rev:
                    if previous is None:
                        print("EARLIEST RETURNED BODY\n" + rev["body"])
                    elif previous != rev["body"]:
                        print("".join(difflib.unified_diff(previous.splitlines(True), rev["body"].splitlines(True), fromfile="prior", tofile="revision")))
                    previous = rev["body"]
    elif part == "comments":
        for comment in sorted(c["comments"], key=lambda x: (x["creation_date"], x["comment_id"])):
            print(json.dumps(public_meta(comment, qowner, answerer_ids), indent=2))
            print(comment.get("body", "[body absent]"))
    else:
        print(json.dumps(c["timeline"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("fetch")
    rp = subs.add_parser("read")
    rp.add_argument("--case", required=True)
    rp.add_argument("--part", choices=("questions", "answers", "comments", "timeline"), required=True)
    args = parser.parse_args()
    if args.command == "fetch":
        fetch()
    else:
        read(args.case, args.part)
