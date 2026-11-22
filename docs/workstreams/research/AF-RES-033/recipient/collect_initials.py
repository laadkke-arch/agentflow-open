#!/usr/bin/env python3
"""AF-RES-033 recipient-only collection. Never print PR outcomes or discussions.

The metadata frame is sealed separately. Run proposal collection only after root GO.
The opening snapshot is a candidate reconstructed from retained commit ancestry
and dates. Original-first certainty cannot be established by this API alone.
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


def ancestors(sha, commits):
    """Return ancestors retained in the current PR commit list, without dates."""
    result, pending = set(), list(commits[sha]["parent_shas"])
    while pending:
        parent = pending.pop()
        if parent in commits and parent not in result:
            result.add(parent)
            pending.extend(commits[parent]["parent_shas"])
    return result


def commit_files(repository, sha):
    """Project commit metadata; patches and commit messages are never exposed."""
    url = f"{API}/repos/{repository}/commits/{sha}?per_page=100&page=1"
    files, urls, tree_sha = [], [], None
    while url:
        detail, link = request_json(url)
        if detail.get("sha") != sha:
            raise ValueError("Commit metadata identity changed")
        urls.append(url)
        tree_sha = detail["commit"]["tree"]["sha"]
        files.extend({"path": f["filename"], "status": f["status"],
                      "blob_sha": f["sha"],
                      **({"previous_path": f["previous_filename"]}
                         if "previous_filename" in f else {})}
                     for f in detail.get("files", []))
        url = next_url(link)
    return sorted(files, key=lambda f: f["path"]), tree_sha, urls


def tree_blob_at_path(repository, tree_sha, path, cache, request_urls):
    """Resolve a path using tree metadata only, never a contents/blob request."""
    parts = pathlib.PurePosixPath(path).parts
    for index, part in enumerate(parts):
        if tree_sha not in cache:
            url = f"{API}/repos/{repository}/git/trees/{tree_sha}"
            tree, _ = request_json(url)
            if tree.get("sha") != tree_sha or tree.get("truncated"):
                raise ValueError("Tree identity mismatch or truncated tree")
            cache[tree_sha] = tree["tree"]
            request_urls.append(url)
        entries = [entry for entry in cache[tree_sha] if entry["path"] == part]
        if len(entries) != 1:
            return None
        entry = entries[0]
        if index == len(parts) - 1:
            return entry["sha"] if entry["type"] == "blob" and entry["mode"] in ("100644", "100755") else None
        if entry["type"] != "tree":
            return None
        tree_sha = entry["sha"]
    return None


def inspect_initial(repository, number):
    row = frame_row(repository, number)
    url = f"{API}/repos/{repository}/pulls/{number}/commits?per_page=100&page=1"
    commits, request_urls = [], []
    while url:
        data, link = request_json(url)
        if not isinstance(data, list):
            raise ValueError("PR commits response was not a list")
        request_urls.append(url)
        for commit in data:
            commits.append({"sha": commit["sha"],
                "author_date": commit["commit"]["author"]["date"],
                "committer_date": commit["commit"]["committer"]["date"],
                "parent_shas": [p["sha"] for p in commit.get("parents", [])],
                "api_position_1based": len(commits) + 1})
        url = next_url(link)
    if not commits:
        raise ValueError("No surviving PR commit available")
    by_sha = {commit["sha"]: commit for commit in commits}
    if len(by_sha) != len(commits):
        raise ValueError("Duplicate SHA in paginated current PR commit list")
    first = commits[0]
    eligible = [commit for commit in commits if commit["committer_date"] <= row["created_at"]]
    earlier = set().union(*(ancestors(commit["sha"], by_sha) for commit in eligible))
    tips = [commit for commit in eligible if commit["sha"] not in earlier]
    safe = {
        "stage": "inspect_initial_commit", "repository": repository,
        "pr_number": number, "created_at": row["created_at"],
        "original_url": row["original_url"], "commits_request_urls": request_urls,
        "retrieved_at_utc": utcnow(), "initial_commit_sha": first["sha"],
        "initial_author_date": first["author_date"],
        "initial_committer_date": first["committer_date"],
        "surviving_commits": commits,
        "commit_list_possible_250_cap": len(commits) >= 250,
        "precreation_tip_candidates": tips,
        "opening_head_candidate": None,
        "opening_head_candidate_sha": None,
        "initiality_status": "opening_snapshot_reconstructed_from_surviving_history_original_first_unproven",
        "original_first_certainty": False,
        "opening_head_certainty": False,
        "opening_head_rule": "unique topologically maximal retained PR commit with committer date <= PR creation; dates and current history do not prove historical opening head",
        "suppressed_fields": ["commit message", "PR title", "PR body", "state",
                              "merge data", "closure data", "comments", "patches", "later commit bodies"],
        "timestamp_eligible": False, "structural_eligibility": False,
        "first_commit_files": [], "added_design_paths": [],
        "all_added_proposal_paths": [], "commit_metadata_request_urls": [],
        "opening_tree_request_urls": [],
    }
    if len(tips) != 1 or safe["commit_list_possible_250_cap"]:
        safe["structural_exclusion_reason"] = ("possibly_capped_current_commit_list" if safe["commit_list_possible_250_cap"]
            else "no_unique_precreation_opening_head_candidate")
        append_attempt(safe)
        return safe
    opening = tips[0]
    safe["opening_head_candidate"] = opening
    safe["opening_head_candidate_sha"] = opening["sha"]
    lineage = ancestors(opening["sha"], by_sha) | {opening["sha"]}
    safe["timestamp_eligible"] = all(by_sha[sha]["committer_date"] <= row["created_at"]
        and by_sha[sha]["author_date"] <= row["created_at"] for sha in lineage)
    if not safe["timestamp_eligible"]:
        safe["structural_exclusion_reason"] = "post_creation_date_in_opening_candidate_ancestry"
        append_attempt(safe)
        return safe
    ordered, pending = [], set(lineage)
    while pending:
        ready = sorted((sha for sha in pending if not (set(by_sha[sha]["parent_shas"]) & pending)),
                       key=lambda sha: by_sha[sha]["api_position_1based"])
        if not ready:
            raise ValueError("Cycle in projected PR commit ancestry")
        ordered.extend(ready)
        pending.difference_update(ready)
    prefix = "text/" if repository == "rust-lang/rfcs" else "keps/"
    proposals, opening_tree = {}, None
    for sha in ordered:
        files, tree_sha, urls = commit_files(repository, sha)
        safe["commit_metadata_request_urls"].extend(urls)
        if sha == first["sha"]:
            safe["first_commit_files"] = files
        if sha == opening["sha"]:
            opening_tree = tree_sha
        for file in files:
            path = file["path"]
            if file["status"] == "removed":
                proposals.pop(path, None)
            elif file["status"] == "renamed" and file.get("previous_path") in proposals:
                proposals[path] = proposals.pop(file["previous_path"])
            elif file["status"] == "added" and path.startswith(prefix) and path.lower().endswith(".md"):
                origin = {"added_at_commit_sha": sha, "original_added_path": path,
                          "original_added_blob_sha": file["blob_sha"]}
                safe["all_added_proposal_paths"].append({"path": path, **origin})
                proposals[path] = origin
    safe["earliest_proposal_commit_sha"] = (safe["all_added_proposal_paths"][0]["added_at_commit_sha"]
        if safe["all_added_proposal_paths"] else None)
    safe["opening_tree_sha"] = opening_tree
    tree_cache = {}
    for path, origin in sorted(proposals.items()):
        if not path.startswith(prefix) or not path.lower().endswith(".md"):
            continue
        blob_sha = tree_blob_at_path(repository, opening_tree, path, tree_cache, safe["opening_tree_request_urls"])
        if blob_sha:
            safe["added_design_paths"].append({"path": path, "status": "added", "blob_sha": blob_sha, **origin})
    safe["structural_eligibility"] = bool(safe["added_design_paths"])
    if not safe["structural_eligibility"]:
        safe["structural_exclusion_reason"] = "no_added_proposal_markdown_survives_at_opening_candidate"
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


def require_inspected_design(repository, number, sha, path, blob_sha):
    """Bind a requested snapshot to retained PR/commit metadata before fetching it."""
    log_path = ROOT / "recipient_attempts.jsonl"
    if not log_path.exists():
        raise ValueError("Inspect the frozen-frame PR before restoring a snapshot")
    with log_path.open() as stream:
        inspections = [json.loads(line) for line in stream if line.strip()]
    matches = [entry for entry in inspections
        if entry.get("stage") == "inspect_initial_commit"
        and entry.get("repository") == repository
        and entry.get("pr_number") == number
        and entry.get("opening_head_candidate_sha") == sha
        and entry.get("timestamp_eligible") is True
        and entry.get("structural_eligibility") is True
        and any(file.get("path") == path and file.get("status") == "added"
            and file.get("blob_sha") == blob_sha for file in entry.get("added_design_paths", []))]
    if not matches:
        raise ValueError("Snapshot tuple is not an eligible added design at a logged PR opening-head candidate")
    return matches[-1]


def restore(repository, number, sha, path, blob_sha):
    row = frame_row(repository, number)
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
        raise ValueError("Expected immutable commit and blob SHA identifiers")
    if pathlib.PurePosixPath(path).is_absolute() or ".." in pathlib.PurePosixPath(path).parts:
        raise ValueError("Unsafe path")
    inspection = require_inspected_design(repository, number, sha, path, blob_sha)
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
        "original_url": row["original_url"], "initial_commit_sha": inspection["initial_commit_sha"],
        "snapshot_commit_sha": sha, "opening_head_candidate_sha": sha,
        "earliest_proposal_commit_sha": inspection.get("earliest_proposal_commit_sha"),
        "initial_blob_sha": blob_sha, "initial_path": path,
        "bound_inspection_retrieved_at_utc": inspection["retrieved_at_utc"],
        "commit_path_blob_bound_to_inspected_pr": True,
        "fixed_url": f"https://github.com/{repository}/blob/{sha}/{path}",
        "raw_fixed_url": f"https://raw.githubusercontent.com/{repository}/{sha}/{path}",
        "blob_request_url": url, "retrieved_at_utc": utcnow(),
        "snapshot_path": str(dest.relative_to(ROOT.parent.parent.parent.parent.parent)),
        "snapshot_absolute_path": str(dest),
        "snapshot_sha256": hashlib.sha256(content).hexdigest(),
        "snapshot_raw_sha256": hashlib.sha256(content).hexdigest(),
        "snapshot_canonical_lf_sha256": hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest(),
        "source_crlf_count": content.count(b"\r\n"),
        "source_lone_cr_count": content.count(b"\r") - content.count(b"\r\n"),
        "raw_source_bytes_preserved": True,
        "bytes": len(content), "line_count": len(content.decode("utf-8").splitlines()),
        "git_blob_sha_verified": True, "model_has_read_full_snapshot": False,
        "original_first_certainty": False, "opening_head_certainty": False,
        "initiality_status": "opening_snapshot_reconstructed_from_surviving_history_original_first_unproven"}
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
