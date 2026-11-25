"""Collect or replay AF-RES-252's public GET responses using only Python and curl."""
import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import html
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import random
import re
import secrets
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent
API = "https://api.stackexchange.com/2.3"
CROSSREF = "https://api.crossref.org/works"
START, END = 1325376000, 1735689599
TAGS = {"postgresql", "greatest-n-per-group"}
TAG_PARAM = "postgresql;greatest-n-per-group"
FRAME_LIMIT, CANDIDATE_LIMIT, ANON_PAGE_LIMIT = 120, 12, 25
CALIBRATION = 138641
STOP = set("a an the how can i to of in for from with postgresql postgres sql".split())
TOKEN = re.compile(r"[a-z][a-z0-9_]*")
METHOD_WORDS = re.compile(
    r"\b(?:distinct\s+on|row_number|dense_rank|rank|lateral|group\s+by|window\s+functions?)\b",
    re.I,
)
WRAPPER = ".items .has_more .quota_max .quota_remaining .backoff .error_id .error_name .error_message"
CREDIT = "shallow_user.display_name shallow_user.link"
QBODY = (
    "question.question_id question.title question.body question.creation_date "
    "question.last_edit_date question.link question.content_license question.owner"
)
FILTERS = {
    "frame": "question.question_id question.creation_date question.tags question.closed_date question.closed_reason",
    "origin": QBODY + " " + CREDIT,
    "revision": (
        "revision.post_id revision.revision_guid revision.revision_number revision.creation_date "
        "revision.revision_type revision.body revision.title revision.last_body revision.last_title "
        "revision.content_license revision.user " + CREDIT
    ),
    "search": "question.question_id question.tags",
    "duplicate": (
        "question.question_id question.closed_date question.closed_reason question.closed_details "
        "closed_details.original_questions original_question.question_id original_question.title "
        "original_question.answer_count original_question.accepted_answer_id"
    ),
    "destination": QBODY + " question.accepted_answer_id question.answer_count " + CREDIT,
    "answer-meta": "answer.answer_id answer.question_id answer.score answer.creation_date",
    "answer-body": (
        "answer.answer_id answer.question_id answer.body answer.creation_date answer.last_edit_date "
        "answer.link answer.is_accepted answer.content_license answer.owner " + CREDIT
    ),
}
FRAME_PARAMS = {
    "site": "dba", "tagged": TAG_PARAM, "fromdate": START, "todate": END,
    "sort": "creation", "order": "asc", "pagesize": 100,
}
CROSSREF_QUERIES = {
    "shannon": {"query.bibliographic": "A Mathematical Theory of Communication"},
    "kuhn-1900": {
        "query.bibliographic": "The Structure of Scientific Revolutions",
        "filter": "from-pub-date:1900-01-01,until-pub-date:1900-01-01",
    },
}
PACKET_FILES = ("reader/origins.jsonl", "reader/destinations.jsonl", "mapping.json")
FRAME_FIELDS = (
    "frame_position", "question_id", "creation_epoch", "creation_utc", "raw_position",
    "page", "page_position", "receipt", "tags", "closed_date", "closed_reason", "candidate",
    "duplicate_position", "calibration_overlap",
)
QUERY_FIELDS = (
    "candidate", "question_id", "input_version", "revision_guid", "current_receipt",
    "revision_receipts", "first_public_revision_guid", "title_original", "title_unescaped",
    "all_tokens", "excluded_tokens_and_reasons", "remaining_tokens", "query", "query_state",
    "method_terms",
)


class Missing(ValueError):
    """A request or a required observation could not be verified."""


def require(condition, message):
    if not condition:
        raise Missing(message)


def utc():
    return datetime.now(timezone.utc)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jsonl_bytes(values):
    return "".join(json.dumps(v, ensure_ascii=False, sort_keys=True) + "\n" for v in values).encode("utf-8")


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def save(root, name, data):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


def status_document(provider, body, exit_code, http, connect):
    if connect not in (0, 200) and not http:
        return "proxy_connect_failed", None
    if not http:
        return "transport_failed", None
    try:
        data = json.loads(body)
    except (UnicodeError, ValueError):
        data = None
    if not 200 <= http < 300:
        return "http_error", data
    if exit_code != 0:
        return "incomplete_transfer", data
    if not isinstance(data, dict):
        return "invalid_json_object", data
    if provider == "stackexchange":
        if "error_id" in data or "error_name" in data:
            return "api_error", data
        fields_ok = (
            isinstance(data.get("items"), list)
            and isinstance(data.get("has_more"), bool)
            and all(type(data.get(key)) is int for key in ("quota_max", "quota_remaining"))
        )
    else:
        message = data.get("message")
        fields_ok = (
            data.get("status") == "ok"
            and data.get("message-type") == "work-list"
            and isinstance(message, dict)
            and isinstance(message.get("items"), list)
            and type(message.get("total-results")) is int
            and message["total-results"] >= len(message["items"])
        )
    if not fields_ok:
        return "invalid_wrapper", data
    items = data["items"] if provider == "stackexchange" else data["message"]["items"]
    if not all(isinstance(item, dict) for item in items):
        return "invalid_item", data
    return ("ok_nonempty" if items else "ok_empty"), data


def public_headers(raw):
    # Do not retain cookies, internal routing headers, or any request headers.
    allowed = {
        "content-type", "content-encoding", "date", "retry-after",
        "x-rate-limit-limit", "x-rate-limit-interval", "x-concurrency-limit",
    }
    result = {}
    for line in raw.decode("latin1").splitlines():
        if line.startswith("HTTP/"):
            result = {}
        key, sep, value = line.partition(":")
        if sep and key.lower() in allowed:
            result[key.lower()] = value.strip()
    return result


@dataclass(frozen=True)
class Page:
    items: list
    receipt: str
    has_more: bool


class Archive:
    def __init__(self, output, offline=False, retry_failed=False):
        self.output = output
        self.directory = output / "receipts"
        self.offline = offline
        self.retry_failed = retry_failed
        self.entries = [
            json.loads(path.read_bytes()) for path in sorted(self.directory.glob("*.meta.json"))
        ]
        self.new_requests = 0

    def read(self, entry):
        name = entry["body_file"]
        require(name in (None, entry["id"] + ".body"), "Unexpected receipt body path")
        raw = (self.directory / name).read_bytes() if name else b""
        stored_sha = entry["body_sha256"]
        require(stored_sha == (digest(raw) if name else None), f"{entry['id']} SHA-256 mismatch")
        require(entry["body_bytes"] == len(raw), f"{entry['id']} byte count mismatch")
        status, data = status_document(
            entry["provider"], raw, entry["curl_exit"], entry["http_status"], entry["connect_status"],
        )
        require(status == entry["status"], f"{entry['id']} reclassification mismatch")
        return data

    def before_request(self, provider, method, url):
        now = utc()
        wait_until = now
        previous = sorted(
            (entry for entry in self.entries if entry["provider"] == provider),
            key=lambda entry: entry["utc_end"],
        )
        if previous and provider == "stackexchange":
            last = previous[-1]
            latest_quota = next(
                (entry for entry in reversed(previous) if entry["quota_remaining"] is not None), None,
            )
            if latest_quota and latest_quota["quota_remaining"] == 0:
                reset_bound = datetime.fromisoformat(latest_quota["utc_end"]) + timedelta(hours=24)
                require(now >= reset_bound, f"Quota exhausted at {latest_quota['id']}. Earliest retry {reset_bound}")
            wait_until = max(wait_until, datetime.fromisoformat(last["utc_end"]) + timedelta(seconds=1))
        for entry in previous:
            end = datetime.fromisoformat(entry["utc_end"])
            if entry["method"] == method:
                wait_until = max(wait_until, end + timedelta(seconds=entry["backoff"] or 0))
            retry_after = entry["response_headers"].get("retry-after")
            if entry["http_status"] in (429, 503) and retry_after and retry_after.isdecimal():
                wait_until = max(wait_until, end + timedelta(seconds=int(retry_after)))
            if entry["url"] == url and provider == "stackexchange":
                wait_until = max(wait_until, end + timedelta(seconds=60))
        delay = (wait_until - now).total_seconds()
        require(delay <= 30, f"Provider wait until {wait_until.isoformat()}. Resume the same operation")
        if delay > 0:
            time.sleep(delay)

    def request(self, key, provider, method, base_url, params):
        url = base_url + "?" + urlencode(params)
        attempts = sorted(
            (record for record in self.entries if record["key"] == key),
            key=lambda record: record["attempt"],
        )
        for record in attempts:
            require(record["url"] == url, f"Request input changed for {key}. Preserve the earlier archive")
        if attempts:
            last = attempts[-1]
            data = self.read(last)
            if last["status"].startswith("ok_"):
                return last, data
            if self.offline or not self.retry_failed:
                raise Missing(f"{key}: {last['status']} ({last['id']})")
        require(not self.offline, f"{key}: receipt missing")
        self.before_request(provider, method, url)
        number = len(attempts) + 1
        receipt_id = f"{key}.{number}"
        start = utc()
        with tempfile.TemporaryDirectory(prefix="af252-get-") as temp:
            headers = Path(temp) / "headers"
            body = Path(temp) / "body"
            command = [
                "curl", "-q", "--silent", "--show-error", "--compressed",
                "--proto", "=https", "--connect-timeout", "10", "--max-time", "45",
                "--fail-with-body", "-D", str(headers), "-o", str(body),
                "-w", "%{http_code} %{http_connect}", url,
            ]
            proc = subprocess.run(command, capture_output=True, check=False)
            raw = body.read_bytes() if body.exists() else b""
            response_headers = public_headers(headers.read_bytes()) if headers.exists() else {}
        end = utc()
        match = re.fullmatch(rb"(\d{3}) (\d{3})", proc.stdout)
        http, connect = tuple(map(int, match.groups())) if match else (0, 0)
        status, data = status_document(provider, raw, proc.returncode, http, connect)
        wrapper = data if isinstance(data, dict) and provider == "stackexchange" else {}
        fields = ("has_more", "quota_max", "quota_remaining", "backoff", "error_id", "error_name")
        body_file = receipt_id + ".body" if raw else None
        entry = {
            "id": receipt_id, "key": key, "attempt": number, "url": url,
            "request_parameters": params, "provider": provider, "method": method,
            "utc_start": start.isoformat(), "utc_end": end.isoformat(),
            "http_status": http, "connect_status": connect, "curl_exit": proc.returncode,
            "curl_stdout": proc.stdout.decode("ascii", errors="replace"),
            "curl_stderr": proc.stderr.decode("utf-8", errors="replace").strip(),
            "response_headers": response_headers, "status": status,
            "body_file": body_file, "body_sha256": digest(raw) if raw else None, "body_bytes": len(raw),
            **{field: wrapper.get(field) for field in fields},
        }
        if body_file:
            save(self.directory, body_file, raw)
        save(self.directory, receipt_id + ".meta.json", json_bytes(entry))
        self.entries.append(entry)
        self.new_requests += 1
        require(status.startswith("ok_"), f"{key}: {status} ({receipt_id})")
        return entry, data

    def se(self, key, method, path, params):
        receipt, data = self.request(key, "stackexchange", method, API + path, params)
        return Page(data["items"], receipt["id"], data["has_more"])

    def filter(self, purpose):
        fields = sorted(set((WRAPPER + " " + FILTERS[purpose]).split()))
        page = self.se("filter-" + purpose, "filter-create", "/filters/create", {
            "base": "none", "include": ";".join(fields), "unsafe": "false",
        })
        require(len(page.items) == 1 and not page.has_more, f"{page.receipt}: expected one filter")
        item = page.items[0]
        included = item.get("included_fields")
        require(isinstance(included, list), f"{page.receipt}: missing included_fields")
        require(set(fields) == set(included), f"{page.receipt}: included_fields differs from the requested set")
        token = item.get("filter")
        require(item.get("filter_type") == "safe" and isinstance(token, str) and token,
                f"{page.receipt}: missing safe filter token")
        return token

    def audit(self):
        for entry in self.entries:
            self.read(entry)
        return {
            "attempts": len(self.entries),
            "entries": [{k: e[k] for k in (
                "id", "provider", "status", "http_status", "connect_status", "curl_exit", "body_sha256",
            )} for e in self.entries],
        }


def question_tags(item):
    tags = item.get("tags")
    require(isinstance(tags, list) and all(isinstance(tag, str) for tag in tags), "Question tags missing")
    return set(tags)


def frames(archive):
    token = archive.filter("frame")
    raw_rows, seen = [], set()
    newest = START
    cutoff = None
    for number in range(1, ANON_PAGE_LIMIT + 1):
        page = archive.se(f"frame-p{number}", "questions", "/questions", {
            **FRAME_PARAMS, "page": number, "filter": token,
        })
        require(not page.has_more or page.items, f"{page.receipt}: empty with has_more")
        for offset, item in enumerate(page.items, 1):
            question_id, created = item.get("question_id"), item.get("creation_date")
            require(type(question_id) is int and question_id not in seen, f"{page.receipt}: missing or repeated id")
            require(type(created) is int and newest <= created <= END, f"{page.receipt}: date/order inconsistency")
            require(TAGS <= question_tags(item), f"{page.receipt}: returned a row outside the two-tag frame")
            reason, closed = item.get("closed_reason"), item.get("closed_date")
            require(
                (type(closed) is int and isinstance(reason, str) and bool(reason.strip()))
                or (closed is None and reason is None),
                f"{page.receipt}: incomplete closure fields",
            )
            seen.add(question_id)
            newest = created
            raw_rows.append({
                "question_id": question_id, "creation_epoch": created,
                "creation_utc": datetime.fromtimestamp(created, timezone.utc).isoformat(),
                "raw_position": len(raw_rows) + 1, "page": number, "page_position": offset,
                "receipt": page.receipt, "tags": ";".join(item["tags"]), "closed_date": closed,
                "closed_reason": reason, "calibration_overlap": question_id == CALIBRATION,
            })
            if len(raw_rows) == FRAME_LIMIT:
                cutoff = created
        if not page.has_more or (cutoff is not None and newest > cutoff):
            break
    else:
        raise Missing("Frame incomplete at the anonymous page limit")
    ordered = sorted(raw_rows, key=lambda row: (row["creation_epoch"], row["question_id"]))[:FRAME_LIMIT]
    duplicate_count = 0
    for position, row in enumerate(ordered, 1):
        is_duplicate = (row["closed_reason"] or "").strip().casefold() == "duplicate"
        duplicate_count += is_duplicate
        row["frame_position"] = position
        row["duplicate_position"] = duplicate_count if is_duplicate else None
        row["candidate"] = duplicate_count if is_duplicate and duplicate_count <= CANDIDATE_LIMIT else None
    return ordered, {
        "provider_rows_observed": len(raw_rows),
        "frame_rows": len(ordered),
        "verified_shortfall_to_cap": FRAME_LIMIT - len(ordered),
        "boundary_epoch": cutoff,
        "boundary_rows": sum(row["creation_epoch"] == cutoff for row in raw_rows),
        "last_page": number,
        "last_receipt": page.receipt,
        "last_has_more": page.has_more,
        "duplicate_rows": duplicate_count,
        "candidate_rows": min(CANDIDATE_LIMIT, duplicate_count),
        "duplicate_rows_above_cap": max(0, duplicate_count - CANDIDATE_LIMIT),
        "verified_candidate_shortfall": max(0, CANDIDATE_LIMIT - duplicate_count),
    }


def all_pages(archive, key, method, path, params):
    records, receipts = [], []
    for number in range(1, ANON_PAGE_LIMIT + 1):
        page = archive.se(f"{key}-p{number}", method, path, {**params, "page": number, "pagesize": 100})
        require(not page.has_more or page.items, f"{page.receipt}: empty with has_more")
        receipts.append(page.receipt)
        records.extend((item, page.receipt, idx) for idx, item in enumerate(page.items, 1))
        if not page.has_more:
            return records, receipts
    raise Missing(f"{key}: incomplete metadata at the anonymous page limit")


def single(page, field, expected):
    require(not page.has_more and len(page.items) <= 1, f"{page.receipt}: invalid single-item response")
    if not page.items:
        return None
    item = page.items[0]
    require(item.get(field) == expected, f"{page.receipt}: wrong {field}")
    return item


def title_query(title):
    unescaped = html.unescape(title)
    tokens = TOKEN.findall(unescaped.lower())
    kept, excluded = [], []
    for position, word in enumerate(tokens, 1):
        if word in STOP:
            excluded.append([position, word, "stopword"])
        elif len(kept) == 4:
            excluded.append([position, word, "limit"])
        else:
            kept.append(word)
    return {
        "title_original": title, "title_unescaped": unescaped,
        "all_tokens": json.dumps(tokens, ensure_ascii=False),
        "excluded_tokens_and_reasons": json.dumps(excluded, ensure_ascii=False),
        "remaining_tokens": json.dumps(kept, ensure_ascii=False),
        "query": " ".join(kept) if len(kept) >= 2 else "",
        "query_state": "eligible" if len(kept) >= 2 else "vacant_under_two_tokens",
        "method_terms": json.dumps(METHOD_WORDS.findall(unescaped), ensure_ascii=False),
    }


def question_body(item, receipt):
    require(
        isinstance(item.get("title"), str) and isinstance(item.get("body"), str),
        f"{receipt}: question title/body missing",
    )


def origin(archive, question_id, candidate):
    current_page = archive.se(f"origin-{question_id}", "questions-by-id", f"/questions/{question_id}", {
        "site": "dba", "filter": archive.filter("origin"),
    })
    current = single(current_page, "question_id", question_id)
    require(current is not None, f"{current_page.receipt}: public current post absent")
    question_body(current, current_page.receipt)
    require(type(current.get("creation_date")) is int, f"{current_page.receipt}: creation_date missing")
    revisions, receipts = all_pages(
        archive, f"revisions-{question_id}", "revisions", f"/posts/{question_id}/revisions",
        {"site": "dba", "filter": archive.filter("revision")},
    )
    require(all(row.get("post_id") == question_id and type(row.get("creation_date")) is int
                for row, _, _ in revisions), f"{receipts[-1]}: revision identity/date mismatch")
    revisions.sort(key=lambda record: (record[0]["creation_date"], record[0].get("revision_number", 0)))
    initial_rows = [
        (row, receipt, position) for row, receipt, position in revisions
        if row.get("revision_number") == 1
        and row.get("creation_date") == current["creation_date"]
        and isinstance(row.get("title"), str) and isinstance(row.get("body"), str)
    ]
    require(len(initial_rows) <= 1, f"{receipts[-1]}: ambiguous initial revision")
    initial = initial_rows[0] if initial_rows else None
    post = initial[0] if initial else current
    first_public = revisions[0] if revisions else None
    query_row = {
        "candidate": candidate, "question_id": question_id,
        "input_version": "initial_revision" if initial else "current_no_complete_initial",
        "revision_guid": post.get("revision_guid"),
        "current_receipt": current_page.receipt, "revision_receipts": ";".join(receipts),
        "first_public_revision_guid": first_public[0].get("revision_guid") if first_public else None,
        **title_query(post["title"]),
    }
    return query_row, post, {
        "current_receipt": current_page.receipt,
        "revision_receipts": receipts,
        "selected_revision_row": list(initial[1:]) if initial else None,
        "first_public_row": list(first_public[1:]) if first_public else None,
    }


def origins(archive):
    frame_rows, stats = frames(archive)
    queries = [origin(archive, row["question_id"], row["candidate"]) for row in frame_rows if row["candidate"]]
    artifacts = {
        "frame.csv": csv_bytes(FRAME_FIELDS, frame_rows),
        "queries.csv": csv_bytes(QUERY_FIELDS, [row for row, _, _ in queries]),
        "frame-stats.json": json_bytes(stats),
    }
    return artifacts, queries, stats


def route_a(archive, question_id, query):
    if not query:
        return {"status": "vacant_under_two_tokens", "question_id": None, "pages": []}
    token = archive.filter("search")
    subset, raw, pages, seen, repeats = [], [], [], set(), []
    signature = digest(query.encode("utf-8"))[:20]
    for number in range(1, ANON_PAGE_LIMIT + 1):
        try:
            page = archive.se(f"advanced-{signature}-p{number}", "advanced-search", "/search/advanced", {
                "site": "dba", "q": query, "tagged": TAG_PARAM, "sort": "relevance", "order": "desc",
                "pagesize": 5, "page": number, "filter": token,
            })
            require(len(page.items) <= 5 and (not page.has_more or page.items),
                    f"{page.receipt}: invalid search page size")
            pages.append(page.receipt)
            for offset, item in enumerate(page.items, 1):
                qid = item.get("question_id")
                require(type(qid) is int, f"{page.receipt}: missing search question_id")
                tags = question_tags(item)
                require(TAGS & tags, f"{page.receipt}: returned a row outside the two-tag OR query")
                row = {
                    "id": qid, "raw_position": len(raw) + 1, "page": number, "page_position": offset,
                    "receipt": page.receipt,
                }
                if qid in seen:
                    repeats.append(row)
                seen.add(qid)
                raw.append(row)
                if TAGS <= tags and len(subset) < 5:
                    subset.append({**row, "and_position": len(subset) + 1})
        except Missing as error:
            stop = "receipt_failure"
            failure = str(error)
            break
        if len(subset) == 5 or not page.has_more:
            stop = "five_and_items" if len(subset) == 5 else "has_more_false"
            failure = None
            break
    else:
        stop = "anonymous_page_limit"
        failure = "AND subset did not reach five and provider reported more pages"
    chosen = next((row for row in subset if row["id"] != question_id), None)
    state = "incomplete" if failure else "selected" if chosen else "vacant_no_nonself_in_subset"
    return {
        "status": state, "question_id": chosen["id"] if chosen else None,
        "selected_position": chosen, "raw_top5": raw[:5], "and_first5": subset, "pages": pages,
        "rows_read": len(raw), "additional_pages": max(0, len(pages) - 1), "duplicate_raw_rows": repeats,
        "stop": stop, "reason": failure,
    }


def route_b(archive, question_id):
    page = archive.se(f"duplicate-{question_id}", "questions-by-id", f"/questions/{question_id}", {
        "site": "dba", "filter": archive.filter("duplicate"),
    })
    item = single(page, "question_id", question_id)
    require(item is not None, f"{page.receipt}: origin public question absent")
    require((item.get("closed_reason") or "").strip().casefold() == "duplicate",
            f"{page.receipt}: closure state has changed since frame")
    details = item.get("closed_details")
    require(isinstance(details, dict), f"{page.receipt}: closed_details missing")
    array = details.get("original_questions", [])
    require(isinstance(array, list) and all(
        isinstance(ref, dict) and type(ref.get("question_id")) is int for ref in array
    ), f"{page.receipt}: invalid original_questions")
    first = array[0]["question_id"] if array else None
    if first == question_id:
        state = "vacant_self_first"
    elif first is None:
        state = "vacant_empty" if "original_questions" in details else "vacant_array_absent"
    else:
        state = "selected"
    return {"status": state, "question_id": first, "receipt": page.receipt, "ordered_ids": [
        item["question_id"] for item in array
    ]}


def credit(item, url):
    owner = item.get("user") or item.get("owner") or {}
    return {
        "url": url, "display_name": owner.get("display_name"), "author_url": owner.get("link"),
        "license": item.get("content_license"),
    }


def destination(archive, question_id):
    page = archive.se(f"destination-{question_id}", "questions-by-id", f"/questions/{question_id}", {
        "site": "dba", "filter": archive.filter("destination"),
    })
    question = single(page, "question_id", question_id)
    result = {"question_id": question_id, "question_receipt": page.receipt, "answer_id": None}
    if question is None:
        return {**result, "status": "vacant_destination_absent"}, None, None
    question_body(question, page.receipt)
    q_url = question.get("link") or f"https://dba.stackexchange.com/questions/{question_id}"
    result["question_attribution"] = credit(question, q_url)
    answer_id = question.get("accepted_answer_id")
    if answer_id is not None:
        require(type(answer_id) is int, f"{page.receipt}: invalid accepted_answer_id")
        result["answer_rule"] = "accepted_answer_id"
    else:
        records, receipts = all_pages(
            archive, f"answer-meta-{question_id}", "answers-on-question",
            f"/questions/{question_id}/answers",
            {"site": "dba", "filter": archive.filter("answer-meta"), "sort": "votes", "order": "desc"},
        )
        seen = set()
        for item, receipt, _ in records:
            aid = item.get("answer_id")
            require(
                item.get("question_id") == question_id and type(aid) is int and aid not in seen
                and type(item.get("score")) is int and type(item.get("creation_date")) is int,
                f"{receipt}: incomplete or repeated answer metadata",
            )
            seen.add(aid)
        require(type(question.get("answer_count")) is int and len(records) == question["answer_count"],
                f"{receipts[-1]}: answer count differs from the question observation")
        result["answer_metadata_receipts"] = receipts
        result["answer_metadata_count"] = len(records)
        if not records:
            return {**result, "status": "vacant_no_answers"}, question, None
        item, receipt, position = min(
            records, key=lambda rec: (-rec[0]["score"], rec[0]["creation_date"], rec[0]["answer_id"]),
        )
        answer_id = item["answer_id"]
        result.update(answer_rule="score_desc_creation_id_asc", answer_metadata_position=[receipt, position])
    page = archive.se(f"answer-{answer_id}", "answers-by-id", f"/answers/{answer_id}", {
        "site": "dba", "filter": archive.filter("answer-body"),
    })
    answer = single(page, "answer_id", answer_id)
    result.update(answer_id=answer_id, answer_receipt=page.receipt)
    if answer is None:
        return {**result, "status": "vacant_selected_answer_absent"}, question, None
    require(answer.get("question_id") == question_id and isinstance(answer.get("body"), str),
            f"{page.receipt}: answer question/body mismatch")
    a_url = answer.get("link") or f"https://dba.stackexchange.com/a/{answer_id}"
    result["answer_attribution"] = credit(answer, a_url)
    return {**result, "status": "question_and_answer"}, question, answer


POST_URL = re.compile(
    r"(?:(?:https?:)?//)?(?:[\w.-]+\.)?(?:stackexchange\.com|stackoverflow\.com|"
    r"serverfault\.com|superuser\.com)/(?:q|a|questions|answers|posts)/\S+",
    re.I,
)
POST_ANCHOR = re.compile(r"^/(?:q|a|questions|answers|posts)/\d|^#(?:answer-)?\d+", re.I)
BANNER = re.compile(
    r"^\s*(?:possible duplicate\b|duplicate of\b|marked as duplicate\b|"
    r"this question already has an answer here\b|this question has been asked before\b)",
    re.I,
)
SQL_START = re.compile(r"(?:^|\n)\s*(?:SELECT|WITH|UPDATE|DELETE|EXPLAIN)\b", re.I)
BLOCKS = {"p", "div", "aside", "blockquote", "pre", "li", "ul", "ol", "tr", "table", "h1", "h2", "h3"}
VOID = {"br", "hr", "img", "meta", "input", "link", "source", "wbr"}


class PostText(HTMLParser):
    """Return plain text with route-suggestive structures removed."""
    def __init__(self, origin):
        super().__init__(convert_charrefs=True)
        self.origin = origin
        self.stack = [("", [], False)]
        self.redactions = {"banner": 0, "post_link": 0, "origin_sql": 0}

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in VOID:
            if tag in {"br", "hr"}:
                self.handle_data("\n")
            return
        href = attrs.get("href") or ""
        classes = attrs.get("class") or ""
        if tag == "a" and (POST_URL.search(href) or POST_ANCHOR.search(href)):
            kind = "post_link"
        elif tag in {"aside", "div", "blockquote"} and re.search("post-notice|duplicate", classes, re.I):
            kind = "banner"
        else:
            kind = False
        hide = "silent" if tag in {"script", "style", "iframe", "object"} else kind
        self.stack.append((tag, [], hide))

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        self.handle_endtag(tag)

    def handle_data(self, data):
        self.stack[-1][1].append(data)

    def handle_endtag(self, tag):
        matching = next((idx for idx in range(len(self.stack) - 1, 0, -1)
                         if self.stack[idx][0] == tag), None)
        if matching is not None:
            while len(self.stack) > matching:
                self.close_node()

    def close_node(self):
        tag, parts, hide = self.stack.pop()
        text = "".join(parts)
        if not hide and tag in {"p", "blockquote", "aside"} and BANNER.search(text):
            hide = "banner"
        if not hide and self.origin and tag in {"pre", "code"}:
            detect = SQL_START.search(text) or METHOD_WORDS.search(text)
            if detect:
                hide = "origin_sql"
        if hide == "silent":
            return
        if hide:
            self.redactions[hide] += 1
            text = {"post_link": "[post link redacted]", "banner": "", "origin_sql": "[SQL redacted]"}[hide]
        if tag in BLOCKS:
            text = "\n" + text.strip("\n") + "\n"
        self.handle_data(text)

    def masked(self, body):
        self.feed(body)
        self.close()
        while len(self.stack) > 1:
            self.close_node()
        text = "".join(self.stack[0][1])
        text, count = POST_URL.subn("[post URL redacted]", text)
        self.redactions["post_link"] += count
        return re.sub(r"\n{3,}", "\n\n", text).strip(), self.redactions


def label(seed, kind, identifier):
    return kind + "-" + digest(f"{seed}:{kind}:{identifier}".encode())[:20]


def masked_title(title, is_origin):
    title = POST_URL.sub("[post URL redacted]", html.unescape(title))
    return METHOD_WORDS.sub("[method redacted]", title) if is_origin else title


def collect_routes(archive, queries, seed):
    source_rows, destination_posts, path_rows, origin_map = [], {}, [], []
    for query, question, evidence in queries:
        qid, number = query["question_id"], query["candidate"]
        source_label = label(seed, "O", qid)
        text, masking = PostText(origin=True).masked(question["body"])
        source_rows.append({
            "label": source_label, "candidate_position": number,
            "title": masked_title(question["title"], True), "body_text": text,
        })
        origin_map.append({
            "label": source_label, "question_id": qid, "candidate_position": number,
            "calibration_overlap": qid == CALIBRATION, "input_version": query["input_version"],
            "attribution": credit(question, f"https://dba.stackexchange.com/questions/{qid}"),
            "masking": masking, **evidence,
        })
        for path in ("AB" if number % 2 else "BA"):
            item = {"origin_label": source_label, "path": path, "destination_label": None}
            try:
                route = route_a(archive, qid, query["query"]) if path == "A" else route_b(archive, qid)
                item["route"] = route
                if route["status"] == "selected":
                    dest_id = route["question_id"]
                    if dest_id not in destination_posts:
                        destination_posts[dest_id] = destination(archive, dest_id)
                    metadata, dest, answer = destination_posts[dest_id]
                    item["destination_status"] = metadata["status"]
                    item["logical_question_bodies"] = int(dest is not None)
                    item["logical_answer_bodies"] = int(answer is not None)
                    if dest is not None:
                        item["destination_label"] = label(seed, "D", dest_id)
            except Missing as error:
                item["failure"] = str(error)
            path_rows.append(item)
    target_rows, target_map = [], []
    for qid, (meta, q, a) in sorted(destination_posts.items()):
        dest_label = label(seed, "D", qid) if q is not None else None
        metadata = {"label": dest_label, **meta}
        if q is not None:
            q_text, q_redactions = PostText(origin=False).masked(q["body"])
            a_text, a_redactions = PostText(origin=False).masked(a["body"]) if a else (None, None)
            target_rows.append({
                "label": dest_label, "title": masked_title(q["title"], False),
                "question_text": q_text, "answer_text": a_text,
            })
            metadata["masking"] = {"question": q_redactions, "answer": a_redactions}
        target_map.append(metadata)
    random.Random(seed).shuffle(target_rows)
    shared_answers = 0
    for left, right in zip(path_rows[::2], path_rows[1::2]):
        if left["destination_label"] and left["destination_label"] == right["destination_label"]:
            target = next(row for row in target_map if row["label"] == left["destination_label"])
            shared_answers += target["status"] == "question_and_answer"
    mapping = {
        "seed": seed, "origins": origin_map, "routes": path_rows, "destinations": target_map,
        "physical_question_bodies": sum(row[1] is not None for row in destination_posts.values()),
        "physical_answer_bodies": sum(row[2] is not None for row in destination_posts.values()),
        "logical_question_bodies": sum(row.get("logical_question_bodies", 0) for row in path_rows),
        "logical_answer_bodies": sum(row.get("logical_answer_bodies", 0) for row in path_rows),
        "paired_same_answer": shared_answers,
    }
    ready = all(
        "failure" not in row and row["route"]["status"] != "incomplete"
        for row in path_rows
    )
    return mapping, source_rows, target_rows, ready


def packet_artifacts(mapping, origin_rows, destination_rows, ready):
    if ready:
        files = {
            PACKET_FILES[0]: jsonl_bytes(origin_rows),
            PACKET_FILES[1]: jsonl_bytes(destination_rows),
            PACKET_FILES[2]: json_bytes(mapping),
        }
        counts = (len(origin_rows), len(destination_rows),
                  len(mapping["origins"]) + len(mapping["routes"]) + len(mapping["destinations"]))
    else:
        files, counts = {}, (None,) * len(PACKET_FILES)
    manifest = {
        "status": "ready" if ready else "blocked",
        "reading_order": [
            {"file": name, "records": count, "sha256": digest(files[name]) if ready else None}
            for name, count in zip(PACKET_FILES, counts)
        ],
    }
    return {**files, "packet-manifest.json": json_bytes(manifest)}


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=False, capture_output=True)


def verify_seal(output, seal, artifacts):
    require(seal and re.fullmatch(r"[0-9a-f]{40}", seal), "Provide the full Git commit of the origin seal")
    require(git(output, "merge-base", "--is-ancestor", seal, "HEAD").returncode == 0,
            "The seal must be committed in this branch history")
    prefix = git(output, "rev-parse", "--show-prefix")
    require(prefix.returncode == 0, "Seal must be inside the repository")
    for name, data in artifacts.items():
        committed = git(output, "show", f"{seal}:{prefix.stdout.decode().strip()}{name}")
        require(committed.returncode == 0 and committed.stdout == data, f"Seal differs on {name}")
        require((output / name).read_bytes() == data, f"Working tree differs on {name}")


def collection_seed(output, offline):
    path = output / "receipts" / "route-state.json"
    if path.is_file():
        return json.loads(path.read_bytes())["seed"]
    require(not offline, "No retained route-state seed for replay")
    return secrets.token_hex(16)


def crossref(archive):
    results = {}
    for key, query in CROSSREF_QUERIES.items():
        cursor, rows, current, seen = "*", 2, [], set()
        result = {"status": "observed", "pages": current}
        results[key] = result
        try:
            for page in range(1, 3):
                meta, data = archive.request(f"crossref-{key}-p{page}", "crossref", "works", CROSSREF, {
                    **query, "sort": "score", "order": "desc", "rows": rows, "cursor": cursor,
                })
                message = data["message"]
                items = message["items"]
                keys = [row.get("DOI") for row in items]
                require(len(items) <= rows and all(isinstance(doi, str) and doi for doi in keys),
                        f"{meta['id']}: missing DOI or overlong page")
                item_keys = [doi.casefold() for doi in keys]
                duplicates = sorted(seen & set(item_keys) | {key for key in item_keys if item_keys.count(key) > 1})
                seen.update(item_keys)
                current.append({
                    "receipt": meta["id"], "cursor_in": cursor, "cursor_out": message.get("next-cursor"),
                    "total_results": message["total-results"], "doi_in_provider_order": keys,
                    "duplicate_dois": duplicates,
                })
                if len(items) < rows:
                    result["status"] = "normal_zero" if page == 1 and message["total-results"] == 0 else "short_page"
                    break
                cursor = message.get("next-cursor")
                require(isinstance(cursor, str) and cursor, f"{meta['id']}: missing next cursor")
            else:
                result["status"] = "two_page_observation_limit"
        except Missing as error:
            result.update(status="incomplete", reason=str(error))
    return results


def run(args):
    output = args.output.resolve()
    offline = args.phase in {"audit", "replay", "replay-crossref"}
    archive = Archive(output, offline=offline, retry_failed=args.retry_failed)
    if args.phase == "audit":
        return archive.audit()
    if args.phase == "probe-frame":
        page = archive.se("frame-default-diagnostic", "questions", "/questions", {
            **FRAME_PARAMS, "page": 1, "filter": "default",
        })
        return {"scope": "diagnostic only", "receipt": page.receipt, "rows": len(page.items)}
    if args.phase in {"crossref", "replay-crossref"}:
        result = crossref(archive)
        expected = json_bytes(result)
        name = "receipts/crossref-state.json"
        if args.phase == "crossref":
            save(output, name, expected)
        else:
            require((output / name).read_bytes() == expected, f"Reparse differs on {name}")
        require(all(row["status"] != "incomplete" for row in result.values()),
                "At least one Crossref response unavailable. See receipts/crossref-state.json")
        return result
    if args.phase == "frame":
        rows, info = frames(archive)
        save(output, "frame.csv", csv_bytes(FRAME_FIELDS, rows))
        save(output, "frame-stats.json", json_bytes(info))
        return info
    # Routes use only previously archived origin evidence until the Git seal is verified.
    if args.phase in {"routes", "replay"}:
        artifact_archive = Archive(output, offline=True)
    else:
        artifact_archive = archive
    origin_files, queries, info = origins(artifact_archive)
    if args.phase == "origins":
        for name, data in origin_files.items():
            save(output, name, data)
        return {**info, "unsealed_query_rows": len(queries)}
    verify_seal(output, args.seal, origin_files)
    seed = collection_seed(output, offline)
    mapping, source_rows, target_rows, ready = collect_routes(archive, queries, seed)
    files = packet_artifacts(mapping, source_rows, target_rows, ready)
    files["receipts/route-state.json"] = json_bytes(mapping)
    if offline:
        for name, data in files.items():
            require((output / name).read_bytes() == data, f"Reparse differs on {name}")
        archive.audit()
    else:
        # Keep the manifest as the last visible write for this packet.
        for name, data in files.items():
            if name != "packet-manifest.json":
                save(output, name, data)
        save(output, "packet-manifest.json", files["packet-manifest.json"])
    require(ready, "Routes incomplete. Inspect receipts/route-state.json and the blocked manifest")
    return {"phase": args.phase, "new_gets": archive.new_requests, "packet": json.loads(files["packet-manifest.json"])}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=(
        "frame", "probe-frame", "origins", "routes", "crossref", "audit", "replay", "replay-crossref",
    ))
    parser.add_argument("--output", type=Path, default=ROOT)
    parser.add_argument("--retry-failed", action="store_true", help="Preserve prior attempts and retry a failed GET")
    parser.add_argument("--seal", help="Git commit containing frame.csv, frame-stats.json and queries.csv")
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except (Missing, FileNotFoundError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json_bytes(result).decode(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
