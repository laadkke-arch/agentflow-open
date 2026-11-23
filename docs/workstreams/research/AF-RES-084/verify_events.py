"""Select a unique GitHub opened event from supplied local JSONL or gzip files."""

import argparse
from copy import deepcopy
from datetime import datetime, timedelta
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def body_hashes(body):
    def digest(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    return {
        "raw_sha256": digest(body),
        "lf_sha256": digest(body.replace("\r\n", "\n").replace("\r", "\n")),
    }


def event_row(record, target):
    payload = record.get("payload", {})
    issue = payload.get("issue", {})
    repo = record.get("repo", {})
    if (
        record.get("type") != "IssuesEvent"
        or payload.get("action") != "opened"
        or repo.get("id") != target["repo_id"]
        or issue.get("id") != target["issue_id"]
        or issue.get("number") != target["number"]
        or issue.get("created_at") != target["created_utc"]
    ):
        return None

    event_id = record.get("id")
    event_utc = record.get("created_at")
    author = issue.get("user", {}).get("login")
    actor = record.get("actor", {}).get("login")
    if not isinstance(event_id, (int, str)) or not str(event_id).isdigit():
        return None
    if not isinstance(event_utc, str) or not event_utc.endswith("Z"):
        return None
    try:
        if datetime.fromisoformat(event_utc) < datetime.fromisoformat(target["created_utc"]):
            return None
    except ValueError:
        return None

    body = issue.get("body")
    if (author or "").casefold() != target["author"].casefold():
        body = None
    if (actor or "").casefold() != target["author"].casefold():
        body = None
    if not isinstance(body, str):
        body = None
    return str(event_id), event_utc, body


def select(records, target):
    candidates = set()
    for record in records:
        row = event_row(record, target)
        if row is not None:
            candidates.add(row)
    if len(candidates) != 1:
        return {
            "status": "unknown",
            "reason": "no-opened-record" if not candidates else "ambiguous-opened-record",
            "candidate_count": len(candidates),
        }
    event_id, event_utc, body = candidates.pop()
    if body is None:
        return {
            "status": "unknown",
            "reason": "body-or-author-unverified",
            "event_id": event_id,
            "event_utc": event_utc,
            "candidate_count": 1,
        }
    return {
        "status": "verified",
        "event_id": event_id,
        "event_utc": event_utc,
        **body_hashes(body),
        "candidate_count": 1,
    }


def read_events(paths):
    for path in paths:
        reader = gzip.open if path.suffix == ".gz" else open
        with reader(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


def archive_urls(utc, *, include_next=False):
    first = datetime.fromisoformat(utc).replace(minute=0, second=0, microsecond=0)
    hours = [first]
    if include_next:
        hours.append(first + timedelta(hours=1))
    return [f"https://data.gharchive.org/{hour:%Y-%m-%d}-{hour.hour}.json.gz" for hour in hours]


def self_test():
    target = {"repo_id": 100, "issue_id": 200, "number": 9, "created_utc": "2022-01-01T23:59:58Z", "author": "reporter"}
    opened = {
        "type": "IssuesEvent",
        "id": "1000",
        "created_at": "2022-01-01T23:59:58Z",
        "actor": {"login": "reporter"},
        "repo": {"id": 100},
        "payload": {
            "action": "opened",
            "issue": {
                "id": 200, "number": 9, "created_at": target["created_utc"],
                "user": {"login": "reporter"}, "body": "one\r\ntwo  \r",
            },
        },
    }
    positive = select([opened], target)
    assert positive["status"] == "verified"
    assert positive == select([opened, deepcopy(opened)], target)
    assert positive["raw_sha256"] != positive["lf_sha256"]
    assert positive["lf_sha256"] == body_hashes("one\ntwo  \n")["raw_sha256"]
    assert positive["lf_sha256"] != body_hashes("one\ntwo\n")["lf_sha256"]

    for id_field in ("repo_id", "issue_id", "number", "created_utc"):
        assert select([opened], dict(target, **{id_field: None}))["status"] == "unknown"

    later = deepcopy(opened)
    later["payload"]["action"] = "closed"
    assert select([later], target)["status"] == "unknown"
    comment = deepcopy(opened)
    comment["type"] = "IssueCommentEvent"
    comment["actor"]["login"] = "somebody-else"
    assert select([comment], target)["status"] == "unknown"
    wrong_actor = deepcopy(opened)
    wrong_actor["actor"]["login"] = "somebody-else"
    assert select([wrong_actor], target)["reason"] == "body-or-author-unverified"
    assert select([{"created_at": target["created_utc"]}], target)["status"] == "unknown"
    current = {"body": opened["payload"]["issue"]["body"], **positive}
    assert select([current], target)["status"] == "unknown"
    changed = deepcopy(opened)
    changed["payload"]["issue"]["body"] += "\nadded"
    assert select([changed], target)["raw_sha256"] != positive["raw_sha256"]
    assert select([opened, changed], target)["reason"] == "ambiguous-opened-record"
    missing = deepcopy(opened)
    missing["payload"]["issue"]["body"] = None
    assert select([missing], target)["reason"] == "body-or-author-unverified"
    assert select([opened, missing], target)["reason"] == "ambiguous-opened-record"
    assert select([opened, dict(opened, id="1001")], target)["reason"] == "ambiguous-opened-record"
    assert archive_urls(target["created_utc"], include_next=True)[-1].endswith("2022-01-02-0.json.gz")
    print("Restoration controls passed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    targets = {row["case"]: row for row in json.loads((ROOT / "fixtures/targets.json").read_text())}
    if args.case not in targets or not args.paths:
        parser.error("supply one --case and at least one archive JSONL/gzip file")
    print(json.dumps(select(read_events(args.paths), targets[args.case]), sort_keys=True))


if __name__ == "__main__":
    main()
