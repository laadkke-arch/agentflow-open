"""Capture public PR pages or normalize already captured connector snapshots."""

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

FRAME = {
    "9580": ("pydata/xarray", "main"),
    "9588": ("pydata/xarray", "main"),
    "9589": ("pydata/xarray", "main"),
    "9618": ("pydata/xarray", "supplement"),
    "7575": ("scikit-image/scikit-image", "main"),
    "7576": ("scikit-image/scikit-image", "main"),
    "7579": ("scikit-image/scikit-image", "main"),
    "7589": ("scikit-image/scikit-image", "main"),
}
ENDPOINTS = {
    "metadata": "pulls/{pr}",
    "issue_comments": "issues/{pr}/comments",
    "reviews": "pulls/{pr}/reviews",
    "inline": "pulls/{pr}/comments",
    "commits": "pulls/{pr}/commits",
    "timeline": "issues/{pr}/timeline",
}
PAGE_SIZE = 25


def capture(root):
    for pr, (repo, _) in FRAME.items():
        directory = root / pr
        directory.mkdir(parents=True, exist_ok=True)
        for kind, endpoint in ENDPOINTS.items():
            resource = f"repos/{repo}/{endpoint.format(pr=pr)}"
            for page in range(1, 36):
                path = resource if kind == "metadata" else f"{resource}?per_page={PAGE_SIZE}&page={page}"
                result = subprocess.run(
                    ["gh", "api", "--include", "-H", "Accept: application/vnd.github+json", path],
                    text=True, capture_output=True, check=False,
                )
                headers, separator, body = result.stdout.partition("\n\n")
                link = next((line.split(":", 1)[1].strip() for line in headers.splitlines()
                             if line.lower().startswith("link:")), None)
                record = {
                    "kind": kind, "pr": pr, "repo": repo, "page": page,
                    "per_page": None if kind == "metadata" else PAGE_SIZE,
                    "url": f"https://api.github.com/{path}",
                    "observed_utc": datetime.now(timezone.utc).isoformat(),
                    "http_link": link, "ok": result.returncode == 0 and bool(separator),
                }
                if record["ok"]:
                    record["data"] = json.loads(body)
                else:
                    record["error"] = result.stderr
                (directory / f"{kind}-{page}.json").write_text(json.dumps(record), encoding="utf-8")
                if not record["ok"] or kind == "metadata" or not record["data"]:
                    break


def read_pages(directory, kind):
    files = sorted(directory.glob(f"{kind}-*.json"), key=lambda path: int(path.stem.split("-")[-1]))
    if [int(path.stem.split("-")[-1]) for path in files] != list(range(1, len(files) + 1)):
        raise ValueError(f"non-consecutive pages for {directory.name} {kind}")
    return [json.loads(path.read_text(encoding="utf-8")) for path in files]


def records(pages):
    for page in pages:
        if page["ok"]:
            data = page["data"]
            yield from data if isinstance(data, list) else [data]


def record_key(kind, item):
    if kind == "timeline":
        return f"{item['event']}:{item.get('id', item.get('sha', item.get('node_id')))}"
    return str(item.get("id", item.get("sha")))


def dump_lines(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def summarize(root, output):
    output.mkdir(parents=True, exist_ok=True)
    evidence = output / "evidence"
    evidence.mkdir(exist_ok=True)
    coverage, page_receipts, public_index = [], [], []
    for pr, (repo, layer) in FRAME.items():
        directory = root / pr
        captures = {kind: read_pages(directory, kind) for kind in ENDPOINTS}
        items = {kind: list(records(pages)) for kind, pages in captures.items()}
        unique = {kind: {record_key(kind, item): item for item in group} for kind, group in items.items()}
        graph = read_pages(directory, "threads")
        thread_groups = list(records(graph))
        threads = thread_groups[0].get("review_threads", []) if thread_groups else []
        graph_ids = {str(comment["database_id"]) for thread in threads for comment in thread["comments"]}
        rest_ids = set(unique["inline"])
        graph_match = "equal" if graph and graph[0]["ok"] and graph_ids == rest_ids else "unverified"
        aliases = {
            "commented": set(unique["issue_comments"]),
            "reviewed": set(unique["reviews"]),
            "committed": set(unique["commits"]),
        }
        overlap = Counter()
        for item in unique["timeline"].values():
            kind = item["event"]
            if str(item.get("id", item.get("sha"))) in aliases.get(kind, set()):
                overlap[kind] += 1
        edit_status = {
            "metadata": "updated_at is PR activity; body edit history unavailable from endpoint",
            "issue_comments": "updated_at compared with created_at; older contents not returned",
            "reviews": "submitted_at; no body edit field in REST response",
            "inline": "updated_at also changes on review submission; older contents not returned",
            "replies": "same edit limits as inline",
            "commits": "immutable object; separate author and committer clocks",
            "timeline": "projected rows; same limits as original collections",
            "threads": "nested updated_at supplied; raw cursors and historical bodies not exposed",
        }
        for kind in (*ENDPOINTS, "replies", "threads"):
            source_kind = "inline" if kind == "replies" else kind
            pages = graph if kind == "threads" else captures[source_kind]
            raw = items.get(source_kind, [])
            distinct = list(unique.get(source_kind, {}).values())
            if kind == "replies":
                raw = [row for row in raw if row.get("in_reply_to_id")]
                distinct = [row for row in distinct if row.get("in_reply_to_id")]
            elif kind == "inline":
                raw = [row for row in raw if not row.get("in_reply_to_id")]
                distinct = [row for row in distinct if not row.get("in_reply_to_id")]
            elif kind == "threads":
                raw = threads
                distinct = list({thread["id"]: thread for thread in threads}.values())
            valid = [page for page in pages if page["ok"]]
            last = valid[-1] if valid else {}
            is_paged = kind not in ("metadata", "threads")
            empty_terminal = bool(last) and is_paged and last.get("data") == [] and len(valid) == len(pages)
            cap = kind == "commits" and len(distinct) >= 250
            parent_misses = [row["in_reply_to_id"] for row in distinct
                             if row.get("in_reply_to_id") and str(row["in_reply_to_id"]) not in rest_ids]
            duplicates = len(raw) - len(distinct)
            coverage.append({
                "repo": repo, "pr": pr, "layer": layer, "category": kind,
                "received": len(raw), "unique": len(distinct), "same_endpoint_duplicates": duplicates,
                "timeline_reposts": sum(overlap.values()) if kind == "timeline" else "",
                "nonempty_bodies": sum(bool((row.get("body") or "").strip()) for row in distinct),
                "edited_timestamp_delta": sum(bool(row.get("created_at") and row.get("updated_at")
                                                   and row["created_at"] != row["updated_at"]) for row in distinct),
                "response_pages": len(valid) if kind != "threads" else "",
                "last_data_page": max((page.get("page", 1) for page in valid if page["data"]), default="") if kind != "threads" else "",
                "terminal_empty_page": last.get("page", "") if empty_terminal else "",
                "page_proof": ("empty next page" if empty_terminal else "single object" if kind == "metadata" and valid
                               else f"REST ID set {graph_match}; cursors hidden" if kind == "threads" and valid else "open"),
                "http_link_or_has_next": last.get("http_link") or "not exposed",
                "current_visible": ("matched REST IDs; cursor unavailable" if kind == "threads" and graph_match == "equal"
                                    else "closed" if (empty_terminal and not cap) or (kind == "metadata" and valid)
                                    else "unverified"),
                "missing_or_limited": (f"unmatched parent IDs {parent_misses}" if parent_misses else
                                       "REST cap possibly hit" if cap else "historical edits and deletions unknown"),
                "edit_scope": edit_status[kind],
                "observed_utc_first": valid[0]["observed_utc"] if valid else "",
                "observed_utc_last": last.get("observed_utc", ""),
                "evidence_url": last.get("url", f"https://github.com/{repo}/pull/{pr}/files") if valid else "",
            })
        for kind, pages in captures.items():
            for page in pages:
                rows = list(records([page]))
                page_receipts.append({
                    "pr": pr, "kind": kind, "page": page["page"], "per_page": page["per_page"],
                    "url": page["url"], "observed_utc": page["observed_utc"], "http_link": page.get("http_link"),
                    "response_ok": page["ok"], "n": len(rows), "ids": [record_key(kind, row) for row in rows],
                    "normalized_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
                    "failure": page.get("error"),
                })
        if threads:
            page_receipts.append({
                "pr": pr, "kind": "threads", "page": None, "observed_utc": graph[0]["observed_utc"],
                "method": "GitHub connector GraphQL wrapper", "has_next_page": None,
                "nested_has_next_page": None, "n": len(threads), "max_nested": max(len(t["comments"]) for t in threads),
                "rest_missing_ids": sorted(graph_ids - rest_ids), "graphql_missing_ids": sorted(rest_ids - graph_ids),
                "threads": [{"thread_id": t["id"], "comment_ids": [c["database_id"] for c in t["comments"]]}
                            for t in threads],
            })
        for kind, group in unique.items():
            for key, item in group.items():
                if kind == "timeline" and str(item.get("id", item.get("sha"))) in aliases.get(item["event"], set()):
                    continue
                body = item.get("body")
                public_index.append({
                    "pr": pr, "kind": kind, "id": key, "url": item.get("html_url") or item.get("url"),
                    "event": item.get("event"), "parent_comment_id": item.get("in_reply_to_id"),
                    "review_id": item.get("pull_request_review_id"), "path": item.get("path"),
                    "original_line": item.get("original_line"), "original_commit": item.get("original_commit_id"),
                    "commit": item.get("commit_id") or item.get("sha"),
                    "created_or_submitted_utc": item.get("created_at") or item.get("submitted_at"),
                    "updated_utc": item.get("updated_at"),
                    "actor": (item.get("user") or item.get("actor") or item.get("author") or {}).get("login"),
                    "body_chars": len(body) if body else 0,
                    "body_sha256": hashlib.sha256(body.encode()).hexdigest() if body else None,
                })
    with (output / "coverage.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(coverage[0]))
        writer.writeheader()
        writer.writerows(coverage)
    dump_lines(evidence / "public-pages.jsonl", page_receipts)
    dump_lines(evidence / "public-index.jsonl", public_index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshots", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--live", action="store_true", help="download fresh public REST pages through authenticated gh")
    args = parser.parse_args()
    if args.live:
        capture(args.snapshots)
    summarize(args.snapshots, args.output)


if __name__ == "__main__":
    main()
