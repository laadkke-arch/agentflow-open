#!/usr/bin/env python3
"""Recover only opened-event identity, times, and head/base SHAs from GH Archive.

No unfiltered event body is written or printed. This script never opens proposal
snapshots, query files, current PR pages, or retrieval results. Grouped streams
produce incremental projections for a separate body-blind provenance reader.
"""
import argparse
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timedelta, timezone
import gzip
from hashlib import sha256
import json
from pathlib import Path
import re
import shlex
import sys
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"
DEFAULT_TARGETS = {
    "kubernetes/enhancements": [1433, 1438, 1439, 1444, 1445, 1447, 1448,
        1450, 1452, 1454, 1457, 1458, 1461, 1462, 1463, 1466, 1467, 1473, 1474],
    "rust-lang/rfcs": [2856],
}
RECOVERY_REASONS = {
    "no_unique_precreation_opening_head_candidate",
    "post_creation_date_in_opening_candidate_ancestry",
    "possibly_capped_current_commit_list",
}
COMPRESSED_LIMIT = 128 * 1024 * 1024
UNCOMPRESSED_LIMIT = 2 * 1024 * 1024 * 1024
LINE_LIMIT = 8 * 1024 * 1024
SECONDS_LIMIT = 120
LOCK = threading.Lock()


def now():
    return datetime.now(timezone.utc).isoformat()


def append(filename, row):
    with LOCK:
        with (EVIDENCE / filename).open("a") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")


def target_metadata(only_numbers=None):
    wanted = {(repository, number) for repository, numbers in DEFAULT_TARGETS.items()
              for number in numbers if not only_numbers or number in only_numbers}
    frame = {}
    with (ROOT / "recipient/recipient_frame.csv").open() as stream:
        for row in csv.DictReader(stream):
            key = row["repository"], int(row["pr_number"])
            if key in wanted:
                if key in frame:
                    raise ValueError("Duplicate allowlisted PR in metadata frame")
                frame[key] = {"repository": key[0], "pr_number": key[1],
                              "created_at": row["created_at"]}
    prior = {}
    with (ROOT / "recipient/recipient_attempts.jsonl").open() as stream:
        for line in stream:
            row = json.loads(line)
            key = row.get("repository"), row.get("pr_number")
            if row.get("stage") == "inspect_initial_commit" and key in wanted:
                reason = row.get("structural_exclusion_reason")
                if reason in RECOVERY_REASONS:
                    prior[key] = {"recovery_reason": reason,
                        "prior_opening_head_candidate_sha": row.get("opening_head_candidate_sha"),
                        "prior_inspection_utc": row.get("retrieved_at_utc")}
    if set(frame) != wanted or set(prior) != wanted:
        raise ValueError("Every target requires a unique frozen-frame identity and logged restoration failure")
    return sorted(({**frame[key], **prior[key]} for key in wanted),
                  key=lambda row: (row["created_at"], row["repository"], row["pr_number"]))


def hourly_groups(targets, hour_offset):
    groups = defaultdict(list)
    for target in targets:
        stamp = datetime.fromisoformat(target["created_at"].replace("Z", "+00:00"))
        stamp += timedelta(hours=hour_offset)
        url = f"https://data.gharchive.org/{stamp:%Y-%m-%d}-{stamp.hour}.json.gz"
        groups[url].append(target)
    return list(groups.items())


def project(event, wanted, line_number):
    if event.get("type") != "PullRequestEvent":
        return None
    repository = event.get("repo", {}).get("name")
    payload = event.get("payload", {})
    key = repository, payload.get("number")
    if key not in wanted or payload.get("action") != "opened":
        return None
    request = payload.get("pull_request", {})
    head = request.get("head", {}).get("sha")
    base = request.get("base", {}).get("sha")
    if not all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value)
               for value in [head, base]):
        raise ValueError("Matching opening event lacks valid head/base SHA identifiers")
    return {"repository": repository, "pr_number": payload["number"],
        "action": "opened", "event_created_at": event.get("created_at"),
        "pull_request_created_at": request.get("created_at"),
        "head_sha": head, "base_sha": base, "archive_line_1based": line_number}


class LimitError(Exception):
    pass


class CountingReader:
    def __init__(self, response, started):
        self.response = response
        self.started = started
        self.count = 0
        self.hasher = sha256()

    def read(self, size=-1):
        if time.monotonic() - self.started > SECONDS_LIMIT:
            raise LimitError("Wall-clock budget exceeded")
        data = self.response.read(65536 if size < 0 else size)
        self.count += len(data)
        self.hasher.update(data)
        if self.count > COMPRESSED_LIMIT:
            raise LimitError("Compressed-byte budget exceeded")
        return data


def scan_group(group, execution_id, hour_offset):
    url, targets = group
    started = time.monotonic()
    wanted = {(target["repository"], target["pr_number"]) for target in targets}
    matches = {key: [] for key in wanted}
    attempt = {"stage": "archive_stream_result", "execution_id": execution_id,
        "url": url, "method": "GET", "targets": targets, "hour_offset": hour_offset,
        "started_utc": now(), "unfiltered_event_persistence": False}
    append("archive-recovery-attempts.jsonl", {**attempt, "stage": "archive_stream_start"})
    reader = None
    lines = uncompressed = 0
    complete = False
    try:
        request = urllib.request.Request(url, headers={
            "User-Agent": "AF-RES-033-provenance-recovery", "Accept-Encoding": "identity"})
        with urllib.request.urlopen(request, timeout=30) as response:
            attempt.update(http_status=response.status, final_url=response.url,
                content_length=response.headers.get("Content-Length"),
                etag=response.headers.get("ETag"), last_modified=response.headers.get("Last-Modified"))
            if response.headers.get("Content-Length") and int(response.headers["Content-Length"]) > COMPRESSED_LIMIT:
                raise LimitError("Declared compressed archive size exceeds budget")
            reader = CountingReader(response, started)
            with gzip.GzipFile(fileobj=reader, mode="rb") as archive:
                while True:
                    line = archive.readline(LINE_LIMIT + 1)
                    if not line:
                        complete = True
                        break
                    lines += 1
                    uncompressed += len(line)
                    if len(line) > LINE_LIMIT or uncompressed > UNCOMPRESSED_LIMIT:
                        raise LimitError("Uncompressed-line or total-byte budget exceeded")
                    if time.monotonic() - started > SECONDS_LIMIT:
                        raise LimitError("Wall-clock budget exceeded")
                    if b'"PullRequestEvent"' not in line:
                        continue
                    if not any(json.dumps(repository).encode() in line for repository, _ in wanted):
                        continue
                    projected = project(json.loads(line), wanted, lines)
                    if projected:
                        matches[(projected["repository"], projected["pr_number"])].append(projected)
        attempt["status"] = "scanned_complete"
    except Exception as exc:
        attempt.update(status="bounded_failure", error_type=type(exc).__name__, error=str(exc))
    attempt.update(ended_utc=now(), elapsed_seconds=round(time.monotonic() - started, 3),
        archive_complete=complete, lines_scanned=lines, uncompressed_bytes_scanned=uncompressed)
    if reader:
        attempt.update(compressed_bytes_read=reader.count,
                       compressed_sha256_consumed=reader.hasher.hexdigest())
    append("archive-recovery-attempts.jsonl", attempt)
    results = []
    for target in targets:
        found = matches[(target["repository"], target["pr_number"])]
        tuples = {(event["head_sha"], event["base_sha"], event["pull_request_created_at"]) for event in found}
        usable = len(tuples) == 1 and all(event["pull_request_created_at"] == target["created_at"] for event in found)
        status = ("opened_event_head_base_recovered" if usable else
                  "conflicting_or_mismatched_opened_events" if found else
                  "no_match_in_complete_hour" if complete else "not_resolved")
        result = {"execution_id": execution_id, **target, "archive_url": url,
            "checked_utc": now(), "hour_offset": hour_offset, "archive_complete": complete,
            "status": status, "usable_projection": usable, "matching_event_count": len(found),
            "matches": found, "unfiltered_event_persistence": False}
        if usable:
            result["archived_opening_head_sha"], result["archived_opening_base_sha"], _ = next(iter(tuples))
        if reader:
            result["compressed_sha256_consumed"] = reader.hasher.hexdigest()
        append("archive-recovery-checks.jsonl", result)
        results.append(result)
        with LOCK:
            print(json.dumps(result, sort_keys=True), flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--hour-offset", type=int, default=0, choices=[-1, 0, 1])
    parser.add_argument("--only", nargs="*", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.only and not set(args.only).issubset({n for ns in DEFAULT_TARGETS.values() for n in ns}):
        parser.error("--only must be a subset of the root-authorized target list")
    targets = target_metadata(set(args.only or []))
    groups = hourly_groups(targets, args.hour_offset)
    execution_id = "archive-recovery-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    execution = {"stage": "execution_command", "execution_id": execution_id,
        "started_utc": now(), "command": shlex.join(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "amendment_commit": "8358b5e75ca45fd9bf0e26cab70e2acc1bc39493",
        "targets": targets, "target_count": len(targets), "hourly_archive_count": len(groups),
        "hour_offset": args.hour_offset, "workers": args.workers,
        "compressed_limit": COMPRESSED_LIMIT, "uncompressed_limit": UNCOMPRESSED_LIMIT,
        "line_limit": LINE_LIMIT, "wall_clock_limit_seconds": SECONDS_LIMIT,
        "request_timeout_seconds": 30, "unfiltered_event_persistence": False}
    if args.dry_run:
        print(json.dumps(execution, sort_keys=True))
        return
    append("archive-recovery-attempts.jsonl", execution)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        batches = list(pool.map(lambda group: scan_group(group, execution_id, args.hour_offset), groups))
    results = [row for batch in batches for row in batch]
    print(json.dumps({"execution_id": execution_id, "targets": len(results),
        "usable_projections": sum(row["usable_projection"] for row in results),
        "complete_archive_scans": sum(batch[0]["archive_complete"] for batch in batches),
        "archives_requested": len(groups)}, sort_keys=True))


if __name__ == "__main__":
    main()
