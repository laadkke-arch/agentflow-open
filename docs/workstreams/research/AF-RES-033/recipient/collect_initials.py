#!/usr/bin/env python3
"""AF-RES-033 recipient-only collection. Never print PR outcomes or discussions.

The metadata frame is sealed separately. Run proposal collection only after root GO.
Only retained current-history first commits are claimed; original-first certainty
cannot be established by this API alone.
"""
import argparse
import base64
import csv
import datetime as dt
import fcntl
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
API = "https://api.github.com"


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def append_attempt(row):
    with (ROOT / "recipient_attempts.jsonl").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        stream.flush()
        fcntl.flock(stream, fcntl.LOCK_UN)


def request_json(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "af-res-033-recipient",
            })
            with urllib.request.urlopen(request, timeout=40) as response:
                return json.load(response), response.headers.get("Link", "")
        except Exception as exc:
            append_attempt({"stage": "request_error", "request_url": url,
                "retrieved_at_utc": utcnow(), "attempt": attempt,
                "error": type(exc).__name__ + ": " + str(exc)})
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def frame_row(repository, number):
    with (ROOT / "recipient_frame.csv").open() as stream:
        matches = [r for r in csv.DictReader(stream)
                   if r["repository"] == repository and int(r["pr_number"]) == number]
    if len(matches) != 1:
        raise ValueError("Expected one PR from the frozen metadata frame")
    return matches[0]


def next_url(link):
    match = re.search(r'<([^>]+)>; rel="next"', link)
    return match.group(1) if match else None


def inspect_initial(repository, number):
    row = frame_row(repository, number)
    url = f"{API}/repos/{repository}/pulls/{number}/commits?per_page=1&page=1"
    data, _ = request_json(url)
    if not isinstance(data, list) or not data:
        raise ValueError("No surviving PR commit available")
    commit = data[0]
    safe = {
        "stage": "inspect_initial_commit", "repository": repository,
        "pr_number": number, "created_at": row["created_at"],
        "original_url": row["original_url"], "commits_request_url": url,
        "retrieved_at_utc": utcnow(), "initial_commit_sha": commit["sha"],
        "initial_author_date": commit["commit"]["author"]["date"],
        "initial_committer_date": commit["commit"]["committer"]["date"],
        "initiality_status": "earliest_surviving_current_history_commit_original_first_unproven",
        "original_first_certainty": False,
        "suppressed_fields": ["commit message", "PR title", "PR body", "state",
                              "merge data", "closure data", "comments", "later commits"],
    }
    safe["timestamp_eligible"] = (
        safe["initial_committer_date"] <= row["created_at"]
        and safe["initial_author_date"] <= row["created_at"])
    url = f"{API}/repos/{repository}/commits/{commit['sha']}?per_page=100&page=1"
    files = []
    safe["commit_metadata_request_urls"] = []
    parents = []
    while url:
        detail, link = request_json(url)
        safe["commit_metadata_request_urls"].append(url)
        parents = [p["sha"] for p in detail.get("parents", [])]
        files.extend({"path": f["filename"], "status": f["status"],
                      "blob_sha": f["sha"]} for f in detail.get("files", []))
        url = next_url(link)
    safe["parent_commit_shas"] = parents
    safe["first_commit_files"] = sorted(files, key=lambda f: f["path"])
    prefix = "text/" if repository == "rust-lang/rfcs" else "keps/"
    safe["added_design_paths"] = [f for f in safe["first_commit_files"]
        if f["status"] == "added" and f["path"].startswith(prefix)
        and f["path"].lower().endswith(".md")]
    safe["structural_eligibility"] = bool(safe["timestamp_eligible"] and safe["added_design_paths"])
    append_attempt(safe)
    return safe


def audit_force_push(repository, number):
    frame_row(repository, number)
    url = f"{API}/repos/{repository}/issues/{number}/events?per_page=100&page=1"
    request_urls, events = [], []
    while url:
        data, link = request_json(url)
        request_urls.append(url)
        if not isinstance(data, list):
            raise ValueError("Issue events response was not a list")
        for event in data:
            if event.get("event") == "head_ref_force_pushed":
                events.append({k: event.get(k) for k in
                    ("id", "event", "created_at", "commit_id", "commit_url")})
        url = next_url(link)
    safe = {"stage": "force_push_audit", "repository": repository,
        "pr_number": number, "retrieved_at_utc": utcnow(),
        "request_urls": request_urls, "force_push_events": events,
        "audit_complete_for_returned_pages": True,
        "only_event_type_exposed": "head_ref_force_pushed",
        "limitation": "Absence of retained REST force-push events does not prove the first surviving commit was the original submission; REST does not document a beforeCommit field."}
    append_attempt(safe)
    return safe


def restore(repository, number, sha, path, blob_sha):
    row = frame_row(repository, number)
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
        raise ValueError("Expected immutable commit and blob SHA identifiers")
    if pathlib.PurePosixPath(path).is_absolute() or ".." in pathlib.PurePosixPath(path).parts:
        raise ValueError("Unsafe path")
    url = f"{API}/repos/{repository}/git/blobs/{blob_sha}"
    data, _ = request_json(url)
    if data.get("sha") != blob_sha or data.get("encoding") != "base64":
        raise ValueError("Unexpected blob identity or encoding")
    content = base64.b64decode(data["content"])
    actual_git_sha = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
    if actual_git_sha != blob_sha:
        raise ValueError("Git blob SHA check failed")
    content.decode("utf-8")
    filename = f"{repository.replace('/', '-')}-pr-{number}-{sha[:12]}-{pathlib.PurePosixPath(path).name}"
    dest = ROOT / "originals" / filename
    dest.parent.mkdir(exist_ok=True)
    if dest.exists() and dest.read_bytes() != content:
        raise ValueError("Refusing to overwrite an unequal immutable snapshot")
    dest.write_bytes(content)
    safe = {"stage": "restore_snapshot", "repository": repository,
        "pr_number": number, "created_at": row["created_at"],
        "original_url": row["original_url"], "initial_commit_sha": sha,
        "initial_blob_sha": blob_sha, "initial_path": path,
        "fixed_url": f"https://github.com/{repository}/blob/{sha}/{path}",
        "raw_fixed_url": f"https://raw.githubusercontent.com/{repository}/{sha}/{path}",
        "blob_request_url": url, "retrieved_at_utc": utcnow(),
        "snapshot_path": str(dest.relative_to(ROOT.parent.parent.parent.parent.parent)),
        "snapshot_absolute_path": str(dest),
        "snapshot_sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(content), "line_count": len(content.decode("utf-8").splitlines()),
        "git_blob_sha_verified": True, "model_has_read_full_snapshot": False,
        "initiality_status": "earliest_surviving_current_history_commit_original_first_unproven"}
    append_attempt(safe)
    return safe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["inspect", "audit", "restore"])
    parser.add_argument("repository", choices=["rust-lang/rfcs", "kubernetes/enhancements"])
    parser.add_argument("number", type=int)
    parser.add_argument("--sha")
    parser.add_argument("--path")
    parser.add_argument("--blob-sha")
    args = parser.parse_args()
    if args.mode == "inspect":
        result = inspect_initial(args.repository, args.number)
    elif args.mode == "audit":
        result = audit_force_push(args.repository, args.number)
    else:
        if not all([args.sha, args.path, args.blob_sha]):
            parser.error("restore requires sha, path and blob-sha")
        result = restore(args.repository, args.number, args.sha, args.path, args.blob_sha)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
