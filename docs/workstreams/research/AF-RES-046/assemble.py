#!/usr/bin/env python3
"""Normalize already-read stream ledgers; no network calls or upstream code execution."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STREAMS = ("pandas", "sklearn", "crossdomain", "root")
ALIASES = {
    "pr_original": "pr_origin", "pr_origin": "pr_origin",
    "review_decision": "review_decision",
    "commit_test": "commit_test", "commit_or_test": "commit_test",
    "link_target": "linked_original", "linked_original": "linked_original",
    "cross_domain_music_operating_rule": "music_rule",
    "cross_domain_music_edit_ledger": "music_ledger",
    "cross_domain_map_edit_ledger": "map_ledger",
    "cross_domain_map_object_versions": "map_versions",
}

def first(row, *keys, default=""):
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return default

def scalar(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if value is None:
        return ""
    return str(value).replace("\r\n", " / ").replace("\n", " / ").replace("\r", " / ")

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(name, rows):
    keys = list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: scalar(value) for key, value in row.items()})

def canonical_work(row):
    url = first(row, "url", "source_url")
    match = re.search(r"github\.com/([^/]+/[^/]+)/(pull|issues)/(\d+)(?:#pullrequestreview-(\d+))?", url)
    if match:
        repo, kind, number, review = match.groups()
        return f"github:{repo}:review:{review}" if review else f"github:{repo}:{'pr' if kind == 'pull' else 'issue'}:{number}"
    match = re.search(r"github\.com/([^/]+/[^/]+)/(?:commit|blob)/([0-9a-f]{40})(?:[/#]|$)", url)
    if match:
        return "git:" + match.group(1) + ":" + match.group(2)
    return row["work_id"]

def sources():
    output, used, source_ids, inputs = [], {}, set(), {}
    for stream in STREAMS:
        folder = ROOT / "streams" / stream
        files = [folder / "sources.jsonl"]
        files += sorted(folder.glob("sources-supplement*.jsonl"))
        for path in files:
            if not path.exists():
                continue
            inputs[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if not line.strip():
                    continue
                raw = json.loads(line)
                sid = raw["source_id"]
                if sid in source_ids:
                    raise ValueError("duplicate source_id " + sid)
                source_ids.add(sid)
                proposed = bool(first(raw, "count_in_minimum", "minimum_count", default=False))
                work = canonical_work(raw)
                allocation = first(raw, "allocation", "minimum_allocation", default="supplementary")
                count = proposed and work not in used
                duplicate = used.get(work) if proposed and not count else raw.get("duplicate_of")
                if count:
                    used[work] = sid
                output.append({
                    "source_id": sid, "work_id": work, "original_work_id": raw["work_id"],
                    "edition_id": raw.get("edition_id"), "url": first(raw, "url", "source_url"),
                    "final_url": raw.get("final_url"), "publisher": raw.get("publisher"),
                    "kind": raw.get("kind"), "published_at": first(raw, "published_at", "publication_date", default=None),
                    "modified_at": first(raw, "modified_at", "modified_date", default=None),
                    "checked_utc": raw.get("checked_utc"), "checked_utc_precision": raw.get("checked_utc_precision", "as recorded by stream"),
                    "location": raw.get("location"), "finding": raw.get("finding"),
                    "limitation": first(raw, "limitation", "limitations"),
                    "questions": first(raw, "questions", "question_ids", default=[]), "case_ids": raw.get("case_ids", []),
                    "duplicate_of": duplicate, "count_in_minimum": count,
                    "allocation": ALIASES.get(allocation, allocation),
                    "raw_count_in_minimum": proposed, "raw_allocation": allocation,
                    "read_status": first(raw, "access_status", "read_status", "reading_method", default="stream semantic reading receipt"),
                    "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
                })
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    return output, inputs

def baselines():
    frame = {row["slot_id"]: row for row in read_csv(ROOT / "frame.csv") if row.get("slot_id")}
    output = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / "baselines.csv"
        for number, row in enumerate(read_csv(path), 1):
            slot = row["slot_id"]
            meta = frame[slot]
            output.append({
                "slot_id": slot, "stratum": meta["stratum"], "repository": row["repository"],
                "pr_number": first(row, "pr_number", "pr"), "pr_url": first(row, "pr_url", "proposal_url"),
                "author": first(row, "author_login", "proposal_author"), "requirement": row["requirement"],
                "pre_link_choice": first(row, "prechoice", "implementation"),
                "initial_candidate_sha": first(row, "initial_candidate_sha", "pre_link_sha"),
                "pre_link_review_sha": first(row, "prelink_review_sha", "pre_link_sha"),
                "parent_sha": first(row, "initial_parent_sha", "base_parent"),
                "original_review_base": row.get("original_review_base", "미확인; commit parent is not asserted to be review base"),
                "git_author_date": first(row, "initial_candidate_author_date", "commit_author_date"),
                "git_committer_date": first(row, "initial_candidate_committer_date", "commit_committer_date"),
                "public_anchor": first(row, "prelink_public_anchor_at", "platform_public_observation_bound"),
                "public_anchor_url": row.get("prelink_public_anchor_url", ""),
                "first_public_head_verified": first(row, "first_public_head_verified", "first_public_upload_exact"),
                "first_public_head_limitation": first(row, "first_public_head_reason", "limitation"),
                "tests": first(row, "tests", "regression_test_contract"), "known_alternatives": row["known_alternatives"],
                "first_qualifying_link": first(row, "first_qualifying_link", default=meta.get("first_link_url", "")),
                "first_link_at": first(row, "first_qualifying_link_at", default=meta.get("first_link_at", "")),
                "first_link_location": row.get("first_qualifying_link_location", "see events.csv and frame.csv"),
                "window_start": first(row, "created_at", default=meta["created_at"]),
                "window_end": first(row, "window_end_90d", default=meta.get("window_end", "")),
                "window_end_source": row.get("closure_source", "see case-level outcomes when completed"),
                "source_ids": row["source_ids"], "limitation": first(row, "limitation", "current_base_head_warning"),
                "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
            })
    output.sort(key=lambda x: (0 if x["slot_id"].startswith("N-") else 1, x["slot_id"]))
    write_csv("baselines.csv", output)
    return output

def events():
    output = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / "events.csv"
        for number, row in enumerate(read_csv(path), 1):
            output.append({
                "event_id": row["event_id"], "slot_id": row["slot_id"], "pr_number": first(row, "pr_number", "pr"),
                "event_type": first(row, "event_type", "type"), "actor": first(row, "actor", "speaker"),
                "actor_role": row["actor_role"], "public_at": first(row, "public_at", "platform_at"),
                "comment_created_at": first(row, "comment_created_at", "authored_at"),
                "review_submitted_at": row.get("review_submitted_at", ""),
                "author_date": row.get("author_date", ""), "committer_date": row.get("committer_date", ""),
                "sha": row.get("sha", ""), "original_commit_id": row.get("original_commit_id", ""),
                "review_id": row.get("review_id", ""), "url": row["url"], "location": row["location"],
                "observed": first(row, "summary", "observed"), "target_url": row.get("target_url", ""),
                "link_class": row.get("link_class", ""), "within_primary_window": first(row, "within_primary_window", "in_main_window"),
                "public_time_limitation": first(row, "public_time_limit", "publication_note"),
                "source_ids": first(row, "source_ids", "source_id"),
                "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
            })
    write_csv("events.csv", output)
    return output

def optional_csv(name):
    rows = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / name
        if not path.exists():
            raise FileNotFoundError(path)
        for number, raw in enumerate(read_csv(path), 1):
            rows.append({**raw, "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number})
    write_csv(name, rows)
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("evidence", "all"), default="evidence")
    args = parser.parse_args()
    src, inputs = sources()
    baseline = baselines()
    ev = events()
    counts = {"sources_receipts": len(src), "counted_unique_works": sum(x["count_in_minimum"] for x in src),
              "allocation": dict(Counter(x["allocation"] for x in src if x["count_in_minimum"])),
              "baseline_rows": len(baseline), "event_rows": len(ev)}
    if args.stage == "all":
        for name in ("changes.csv", "labor.csv"):
            counts[name] = len(optional_csv(name))
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(), "stage": args.stage, "counts": counts,
               "source_input_sha256": inputs, "boundary": "Field normalization and work deduplication of directly-read evidence; not upstream test execution or causal validation."}
    (ROOT / "evidence" / "assembly.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False))

if __name__ == "__main__":
    main()
