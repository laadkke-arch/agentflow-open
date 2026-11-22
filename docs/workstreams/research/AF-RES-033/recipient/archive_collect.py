#!/usr/bin/env python3
"""Explicit archived PullRequestEvent/opened restoration for AF-RES-033.

Uses only projected archive bindings and the separately projected connector cache.
No current-history date flag is synthesized. Opening-event provenance remains
separate from the legacy surviving-history method and its failures.
"""
import argparse
import base64
import hashlib
import importlib.util
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
API = "https://api.github.com"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

core = load_module("recipient_core_archive", ROOT / "collect_initials.py")
bridge = load_module("recipient_bridge_archive", ROOT / "connector_collect.py")
core.request_json = bridge.cached_request
request_json = bridge.cached_request


def binding(repository, number):
    row = core.frame_row(repository, number)
    entries = [json.loads(line) for line in (ROOT / "recipient_archive_bindings.jsonl").read_text().splitlines() if line.strip()]
    matches = [entry for entry in entries if entry["repository"] == repository and entry["pr_number"] == number]
    if len(matches) != 1:
        raise ValueError("Expected exactly one projected archive binding")
    event = matches[0]
    if not (event["archive_opened_event_verified"] is True and event["matched_event_count"] == 1
            and event["event_type"] == "PullRequestEvent" and event["event_action"] == "opened"
            and event["pull_request_created_at"] == row["created_at"]):
        raise ValueError("Archive event is not uniquely bound to the frozen-frame opening")
    for key in ("archived_head_sha", "archived_base_sha"):
        if not re.fullmatch(r"[0-9a-f]{40}", event[key]):
            raise ValueError("Archive binding has a non-immutable SHA")
    permitted_ledgers = {
        (ROOT.parent / "evidence" / name).resolve()
        for name in ("archive-recovery-checks.jsonl", "prefix-archive-checks.jsonl")
    }
    projection_path = pathlib.Path(event["evidence_projection_path"]).resolve()
    if projection_path not in permitted_ledgers:
        raise ValueError("Unexpected archive projection ledger")
    projected_lines = projection_path.read_text().splitlines()
    line_number = event["evidence_projection_line_1based"]
    if not isinstance(line_number, int) or not 1 <= line_number <= len(projected_lines):
        raise ValueError("Archive projection line is unavailable")
    projection = json.loads(projected_lines[line_number - 1])
    canonical = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(canonical).hexdigest() != event["evidence_projection_row_sha256"]:
        raise ValueError("Archive projection row hash differs from binding")
    if not (projection.get("status") == "opened_event_head_base_recovered"
            and projection.get("usable_projection") is True and projection.get("archive_complete") is True
            and projection.get("matching_event_count") == 1 and len(projection.get("matches", [])) == 1):
        raise ValueError("Archive projection does not establish one complete matching opening event")
    match = projection["matches"][0]
    if not (projection["repository"] == repository and projection["pr_number"] == number
            and projection["created_at"] == row["created_at"] and match["repository"] == repository
            and match["pr_number"] == number and match["action"] == "opened"
            and match["pull_request_created_at"] == row["created_at"]
            and match["event_created_at"] == event["event_created_at"]
            and match["head_sha"] == projection["archived_opening_head_sha"] == event["archived_head_sha"]
            and match["base_sha"] == projection["archived_opening_base_sha"] == event["archived_base_sha"]
            and match["archive_line_1based"] == event["archive_line_1based"]
            and projection["archive_url"] == event["archive_url"]
            and projection["compressed_sha256_consumed"] == event["archive_compressed_sha256"]):
        raise ValueError("Archive head/base tuple or source identity drifted from the audited projection")
    return row, event


def inspect(repository, number):
    row, event = binding(repository, number)
    head, base = event["archived_head_sha"], event["archived_base_sha"]
    url = f"{API}/repos/{repository}/compare/{base}...{head}?per_page=100&page=1"
    comparison, _ = request_json(url)
    if comparison.get("base_commit", {}).get("sha") != base:
        raise ValueError("Archived comparison base does not match the event base")
    files = sorted(({"path": item["filename"], "status": item["status"], "blob_sha": item["sha"],
        **({"previous_path": item["previous_filename"]} if item.get("previous_filename") else {})}
        for item in comparison.get("files", [])), key=lambda item: item["path"])
    commits = comparison.get("commits", [])
    record = {"stage": "inspect_archived_opening", "repository": repository,
        "pr_number": number, "created_at": row["created_at"], "original_url": row["original_url"],
        "retrieved_at_utc": core.utcnow(), "archive_opened_event_verified": True,
        "archive_binding": event, "archived_head_sha": head, "archived_base_sha": base,
        "snapshot_commit_sha": head, "comparison_request_url": url,
        "opening_comparison_files": files, "compare_file_cap_possible": len(files) >= 300,
        "comparison_total_commits": comparison.get("total_commits"),
        "comparison_commit_metadata": commits,
        "comparison_commit_metadata_complete": comparison.get("total_commits", len(commits)) == len(commits),
        "first_comparison_commit_sha": commits[0]["sha"] if commits else None,
        "first_comparison_commit_limit": "First commit returned for archived base-to-head comparison; not claimed to be the first authored draft or the first commit that added the selected proposal.",
        "initiality_status": "archive_opened_event_verified",
        "opening_head_certainty": True, "original_first_commit_certainty": False,
        "structural_eligibility": False, "added_design_paths": [],
        "head_tree_request_urls": [],
        "suppressed_fields": ["PR title", "PR body", "state", "merge data", "closure data", "comments", "patches", "commit messages"]}
    if record["compare_file_cap_possible"]:
        record["structural_exclusion_reason"] = "archive_compare_file_list_may_be_capped"
        core.append_attempt(record)
        return record
    prefix = "text/" if repository == "rust-lang/rfcs" else "keps/"
    candidates = [file for file in files if file["status"] in ("added", "renamed")
                  and file["path"].startswith(prefix) and file["path"].lower().endswith(".md")]
    if candidates:
        commit_url = f"{API}/repos/{repository}/git/commits/{head}"
        commit, _ = request_json(commit_url)
        if commit.get("sha") != head:
            raise ValueError("Archived head object identity mismatch")
        tree_sha = commit["tree"]["sha"]
        record["head_commit_request_url"] = commit_url
        record["opening_tree_sha"] = tree_sha
        cache = {}
        for file in candidates:
            actual = core.tree_blob_at_path(repository, tree_sha, file["path"], cache, record["head_tree_request_urls"])
            if actual != file["blob_sha"]:
                raise ValueError("Archived compare path/blob does not match opening head tree")
            record["added_design_paths"].append({**file, "head_tree_path_blob_verified": True})
    record["structural_eligibility"] = bool(record["added_design_paths"])
    if not record["structural_eligibility"]:
        record["structural_exclusion_reason"] = "no_added_or_renamed_proposal_markdown_in_archived_opening_diff"
    core.append_attempt(record)
    return record


def restore(repository, number, sha, path, blob_sha):
    row, event = binding(repository, number)
    if sha != event["archived_head_sha"]:
        raise ValueError("Restore SHA must be the uniquely bound archived opening head")
    records = [json.loads(line) for line in (ROOT / "recipient_attempts.jsonl").read_text().splitlines() if line.strip()]
    matches = [entry for entry in records if entry.get("stage") == "inspect_archived_opening"
        and entry.get("repository") == repository and entry.get("pr_number") == number
        and entry.get("archived_head_sha") == sha and entry.get("archive_opened_event_verified") is True
        and entry.get("archive_binding") == event
        and entry.get("structural_eligibility") is True and any(file["path"] == path
        and file["blob_sha"] == blob_sha and file.get("head_tree_path_blob_verified") is True
        for file in entry.get("added_design_paths", []))]
    if not matches:
        raise ValueError("Restore tuple has no verified archive/head-tree inspection")
    inspection = matches[-1]
    url = f"{API}/repos/{repository}/git/blobs/{blob_sha}"
    data, _ = request_json(url)
    if data.get("sha") != blob_sha or data.get("encoding") != "base64":
        raise ValueError("Unexpected archive blob identity/encoding")
    content = base64.b64decode(data["content"])
    actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
    if actual != blob_sha:
        raise ValueError("Archived blob content does not match the original Git SHA")
    decoded = content.decode("utf-8")
    filename = f"{repository.replace('/', '-')}-pr-{number}-{sha[:12]}-{pathlib.PurePosixPath(path).name}"
    dest = ROOT / "originals" / filename
    dest.parent.mkdir(exist_ok=True)
    if dest.exists() and dest.read_bytes() != content:
        raise ValueError("Refusing to overwrite unequal archived source bytes")
    dest.write_bytes(content)
    record = {"stage": "restore_archived_snapshot", "repository": repository,
        "pr_number": number, "created_at": row["created_at"], "original_url": row["original_url"],
        "archive_opened_event_verified": True, "archive_binding": event,
        "archived_head_sha": sha, "archived_base_sha": event["archived_base_sha"],
        "snapshot_commit_sha": sha, "first_comparison_commit_sha": inspection["first_comparison_commit_sha"],
        "initial_blob_sha": blob_sha, "initial_path": path,
        "fixed_url": f"https://github.com/{repository}/blob/{sha}/{path}",
        "raw_fixed_url": f"https://raw.githubusercontent.com/{repository}/{sha}/{path}",
        "blob_request_url": url, "retrieved_at_utc": core.utcnow(),
        "snapshot_path": str(dest.relative_to(ROOT.parent.parent.parent.parent.parent)),
        "snapshot_absolute_path": str(dest), "snapshot_sha256": hashlib.sha256(content).hexdigest(),
        "snapshot_raw_sha256": hashlib.sha256(content).hexdigest(),
        "snapshot_canonical_lf_sha256": hashlib.sha256(content.replace(b"\r\n", b"\n")).hexdigest(),
        "source_crlf_count": content.count(b"\r\n"), "bytes": len(content),
        "line_count": len(decoded.splitlines()), "git_blob_sha_verified": True,
        "head_tree_path_blob_verified": True, "raw_source_bytes_preserved": True,
        "model_has_read_full_snapshot": False, "initiality_status": "archive_opened_event_verified",
        "opening_head_certainty": True, "original_first_commit_certainty": False,
        "first_commit_limit": inspection["first_comparison_commit_limit"]}
    core.append_attempt(record)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["inspect", "restore"])
    parser.add_argument("repository", choices=["rust-lang/rfcs", "kubernetes/enhancements"])
    parser.add_argument("number", type=int)
    parser.add_argument("--sha")
    parser.add_argument("--path")
    parser.add_argument("--blob-sha")
    args = parser.parse_args()
    try:
        if args.mode == "inspect":
            result = inspect(args.repository, args.number)
        else:
            if not all([args.sha, args.path, args.blob_sha]):
                parser.error("restore requires sha, path and blob-sha")
            result = restore(args.repository, args.number, args.sha, args.path, args.blob_sha)
        print(json.dumps({"status": "complete", "result": result}, ensure_ascii=False))
    except bridge.NeedRequest as request:
        print(json.dumps({"status": "request_needed", "request_url": request.url, "cache_path": request.cache_path}))

if __name__ == "__main__":
    main()
