"""Join captured review IDs to specific local Git objects and path ancestry."""

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import subprocess

from retrieve import FRAME, dump_lines, read_pages, records


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=False, text=True, capture_output=True)


def ancestor(repo, earlier, later):
    if not earlier or not later:
        return None
    status = git(repo, "merge-base", "--is-ancestor", earlier, later).returncode
    return {0: True, 1: False}.get(status)


def inspect_pr(snapshot, repo, pr):
    pull = next(records(read_pages(snapshot, "metadata")))
    head = pull["head"]["sha"]
    base = pull["base"]["sha"]
    merge = pull["merge_commit_sha"] if pull["merged"] else None
    listed = list(records(read_pages(snapshot, "commits")))
    reviews = {item["id"]: item for item in records(read_pages(snapshot, "reviews"))}
    clock = datetime.now(timezone.utc).isoformat()
    local_ref = git(repo, "rev-parse", f"pr{pr}").stdout.strip()
    commit_rows = []
    for item in listed:
        sha = item["sha"]
        local = git(repo, "show", "-s", "--format=%T%x09%P%x09%aI%x09%cI", sha)
        parts = local.stdout.strip().split("\t") if local.returncode == 0 else [None] * 4
        tree, parent_text, author_utc, committer_utc = parts
        commit_rows.append({
            "sha": sha, "tree": tree, "parents": (parent_text or "").split(),
            "author_login": (item["author"] or {}).get("login"), "git_author_time": author_utc,
            "git_committer_time": committer_utc, "remote_parent_count": len(item["parents"]),
            "remote_subject": item["commit"]["message"].splitlines()[0],
            "reachable_from_pr_head": ancestor(repo, sha, head),
        })
    merge_parents = git(repo, "show", "-s", "--format=%P", merge).stdout.split() if merge else []
    rows = [{
        "pr": pr, "kind": "refs", "observed_utc": clock, "base_api": base,
        "head_api": head, "head_git": local_ref, "merge": merge, "merge_parents": merge_parents,
        "head_is_merge_ancestor": ancestor(repo, head, merge), "listed_commits": pull["commits"],
        "commit_objects": commit_rows,
    }]
    for item in records(read_pages(snapshot, "inline")):
        sha = item["original_commit_id"]
        path = item["path"]
        review_id = item["pull_request_review_id"]
        review = reviews.get(review_id, {})
        submitted = review.get("submitted_at")
        blob = git(repo, "rev-parse", "--verify", f"{sha}:{path}")
        parent = git(repo, "show", "-s", "--format=%P", sha)
        rows.append({
            "pr": pr, "kind": "anchor", "observed_utc": clock, "url": item["html_url"],
            "id": item["id"], "parent_id": item.get("in_reply_to_id"), "review": review_id,
            "created_utc": item["created_at"], "submitted_utc": submitted,
            "visible_no_earlier_than": max(item["created_at"], submitted) if submitted else item["created_at"],
            "original_sha": sha, "original_line": item.get("original_line"),
            "original_start_line": item.get("original_start_line"), "path": path,
            "original_hunk_header": item["diff_hunk"].partition("\n")[0],
            "original_hunk_sha256": hashlib.sha256(item["diff_hunk"].encode()).hexdigest(),
            "parents": parent.stdout.split() if parent.returncode == 0 else None,
            "blob": blob.stdout.strip() if blob.returncode == 0 else None,
            "original_is_head_ancestor": ancestor(repo, sha, head),
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshots", type=Path)
    parser.add_argument("git_repos", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = []
    for pr, (repo, _) in {**FRAME, "7699": ("scikit-image/scikit-image", "comparator")}.items():
        rows.extend(inspect_pr(args.snapshots / pr, args.git_repos / repo.split("/")[-1], pr))
    dump_lines(args.output, rows)


if __name__ == "__main__":
    main()
