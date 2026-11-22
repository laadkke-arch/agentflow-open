#!/usr/bin/env python3
"""Corroborate eleven prefix exclusions using the existing archive projector.

Only opening-event identity, times, and head/base SHAs are projected. This
wrapper preserves all previous archive files and writes separate prefix ledgers.
No source bodies, PR titles, queries, or outcomes are displayed or persisted.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import shlex
import sys


EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parent
TARGETS = ROOT / "recipient/recipient_prefix_archive_targets.jsonl"
TARGETS_SHA256 = "51dbf3856b25a181b67bc3350a86db974c65771b0bf430684be4be58b532fbee"
EXPECTED = {
    ("rust-lang/rfcs", 2842), ("rust-lang/rfcs", 2847),
    *(('kubernetes/enhancements', n) for n in
      (1429, 1430, 1431, 1434, 1436, 1437, 1442, 1443, 1449)),
}
MODULE_PATH = EVIDENCE / "archive-recovery.py"
spec = importlib.util.spec_from_file_location("existing_archive_recovery", MODULE_PATH)
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)
OUTPUTS = {
    "archive-recovery-attempts.jsonl": "prefix-archive-attempts.jsonl",
    "archive-recovery-checks.jsonl": "prefix-archive-checks.jsonl",
}
PRESERVED = [
    "opening-archive-attempts.jsonl", "opening-archive-checks.jsonl", "opening-archive.md",
    "archive-recovery-attempts.jsonl", "archive-recovery-checks.jsonl", "archive-recovery.md",
    "archive-recovery.py", "initial-source-binding-audit.md", "initial-source-binding-checks.json",
]


def canonical_hash(row):
    data = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def append(filename, row):
    """Route existing scanner writes to the new ledgers, requiring full scans."""
    if filename not in OUTPUTS:
        raise ValueError("Unrecognized output ledger")
    if filename == "archive-recovery-checks.jsonl":
        strictly_usable = (row.get("usable_projection") is True
                           and row.get("archive_complete") is True
                           and row.get("matching_event_count") == 1
                           and len(row.get("matches", [])) == 1)
        row["usable_projection"] = strictly_usable
        if not strictly_usable and row.get("status") == "opened_event_head_base_recovered":
            row["status"] = "opened_event_not_uniquely_verified_in_complete_archive"
        row["archived_head_matches_reconstruction"] = (
            row["archived_opening_head_sha"] == row["prior_opening_head_candidate_sha"]
            if strictly_usable else None)
        row["audit_scope"] = "eleven_prior_structural_exclusions_opening_head_corroboration"
    with archive.LOCK:
        with (EVIDENCE / OUTPUTS[filename]).open("a") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")


archive.append = append


def target_metadata():
    raw = TARGETS.read_bytes()
    if sha256(raw).hexdigest() != TARGETS_SHA256:
        raise ValueError("Authorized target metadata changed")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    keys = [(row["repository"], row["pr_number"]) for row in rows]
    if len(rows) != 11 or len(set(keys)) != 11 or set(keys) != EXPECTED:
        raise ValueError("Target identities do not match the authorized eleven")
    with (ROOT / "recipient/recipient_frame.csv").open() as stream:
        frames = [row for row in csv.DictReader(stream)
                  if (row["repository"], int(row["pr_number"])) in EXPECTED]
    if len(frames) != 11:
        raise ValueError("Frozen frame identity missing or duplicated")
    frame = {(row["repository"], int(row["pr_number"])): row["created_at"] for row in frames}
    attempts = (ROOT / "recipient/recipient_attempts.jsonl").read_text().splitlines()
    projected = []
    for row in rows:
        key = row["repository"], row["pr_number"]
        if row["created_at"] != frame[key]:
            raise ValueError("Target creation time differs from frozen frame")
        line_number = row["inspection_attempt_line_1based"]
        prior = json.loads(attempts[line_number - 1])
        if not (prior.get("stage") == "inspect_initial_commit"
                and prior.get("repository") == row["repository"]
                and prior.get("pr_number") == row["pr_number"]
                and prior.get("created_at") == row["created_at"]
                and prior.get("opening_head_candidate_sha") == row["opening_head_candidate_sha"]
                and prior.get("retrieved_at_utc") == row["inspection_retrieved_at_utc"]
                and re.fullmatch(r"[0-9a-f]{40}", row["opening_head_candidate_sha"])):
            raise ValueError("Target does not match its logged prior inspection")
        projected.append({
            "repository": row["repository"], "pr_number": row["pr_number"],
            "created_at": row["created_at"],
            "prior_opening_head_candidate_sha": row["opening_head_candidate_sha"],
            "prior_inspection_utc": row["inspection_retrieved_at_utc"],
            "prior_inspection_attempt_line_1based": line_number,
            "prior_inspection_canonical_sha256": canonical_hash(prior),
        })
    return sorted(projected, key=lambda row: (row["created_at"], row["repository"], row["pr_number"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 5))
    parser.add_argument("--hour-offset", type=int, default=0, choices=[-1, 0, 1])
    parser.add_argument("--only", nargs="*", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.only and not set(args.only).issubset({number for _, number in EXPECTED}):
        parser.error("--only must be within the authorized eleven")
    targets = target_metadata()
    if args.only:
        targets = [row for row in targets if row["pr_number"] in args.only]
    groups = archive.hourly_groups(targets, args.hour_offset)
    preserved = {name: sha256((EVIDENCE / name).read_bytes()).hexdigest() for name in PRESERVED}
    execution_id = "prefix-archive-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    execution = {
        "stage": "execution_command", "execution_id": execution_id,
        "started_utc": archive.now(),
        "command": shlex.join(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "reused_scanner_path": str(MODULE_PATH),
        "reused_scanner_sha256": sha256(MODULE_PATH.read_bytes()).hexdigest(),
        "target_metadata_path": str(TARGETS), "target_metadata_sha256": TARGETS_SHA256,
        "authorization": "Root-authorized eleven-prefix closure before remote input freeze",
        "prior_archive_recovery_amendment": "8358b5e75ca45fd9bf0e26cab70e2acc1bc39493",
        "targets": targets, "target_count": len(targets), "hourly_archive_count": len(groups),
        "workers": args.workers, "hour_offset": args.hour_offset,
        "compressed_limit": archive.COMPRESSED_LIMIT,
        "uncompressed_limit": archive.UNCOMPRESSED_LIMIT,
        "line_limit": archive.LINE_LIMIT, "wall_clock_limit_seconds": archive.SECONDS_LIMIT,
        "request_timeout_seconds": 30, "unfiltered_event_persistence": False,
        "preserved_evidence_sha256_before": preserved,
    }
    if args.dry_run:
        print(json.dumps(execution, sort_keys=True))
        return
    append("archive-recovery-attempts.jsonl", execution)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        batches = list(pool.map(lambda group: archive.scan_group(group, execution_id, args.hour_offset), groups))
    results = [row for batch in batches for row in batch]
    after = {name: sha256((EVIDENCE / name).read_bytes()).hexdigest() for name in PRESERVED}
    summary = {
        "stage": "execution_summary", "execution_id": execution_id, "ended_utc": archive.now(),
        "target_count": len(results), "usable_projection_count": sum(row["usable_projection"] for row in results),
        "matching_reconstruction_count": sum(row["archived_head_matches_reconstruction"] is True for row in results),
        "different_reconstruction_count": sum(row["archived_head_matches_reconstruction"] is False for row in results),
        "complete_archive_count": sum(batch[0]["archive_complete"] for batch in batches),
        "archives_requested": len(groups), "prior_evidence_unchanged": preserved == after,
        "preserved_evidence_sha256_after": after,
    }
    append("archive-recovery-attempts.jsonl", summary)
    print(json.dumps(summary, sort_keys=True))
    if preserved != after:
        raise RuntimeError("A previously written evidence artifact changed during prefix execution")


if __name__ == "__main__":
    main()
