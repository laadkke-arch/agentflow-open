"""Bind and finalize the additional metadata-only prefix archive checks."""

import argparse
import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "evidence" / "prefix-archive-checks.jsonl"


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def key(row):
    return row["repository"], row["pr_number"]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append(path, data):
    with path.open("a") as handle:
        for row in data:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def bind():
    targets = {key(row): row for row in rows(HERE / "recipient_prefix_archive_targets.jsonl")}
    path = HERE / "recipient_archive_bindings.jsonl"
    existing = {key(row): row for row in rows(path)}
    added = []
    for number, row in enumerate(rows(LEDGER), 1):
        k = key(row)
        assert k in targets
        assert row["usable_projection"] and row["status"] == "opened_event_head_base_recovered"
        assert row["archive_complete"] and row["matching_event_count"] == 1 and len(row["matches"]) == 1
        event = row["matches"][0]
        assert key(event) == k and event["action"] == "opened"
        assert event["pull_request_created_at"] == row["created_at"] == targets[k]["created_at"]
        assert event["head_sha"] == row["archived_opening_head_sha"]
        assert event["base_sha"] == row["archived_opening_base_sha"]
        binding = {
            "repository": k[0], "pr_number": k[1], "archive_opened_event_verified": True,
            "matched_event_count": 1, "event_type": "PullRequestEvent",
            "event_type_basis": "Protocol auditor filtered public archive records to PullRequestEvent/opened before projection.",
            "event_action": "opened", "event_created_at": event["event_created_at"],
            "pull_request_created_at": event["pull_request_created_at"],
            "archived_head_sha": event["head_sha"], "archived_base_sha": event["base_sha"],
            "archive_url": row["archive_url"], "archive_compressed_sha256": row["compressed_sha256_consumed"],
            "archive_line_1based": event["archive_line_1based"], "archive_complete": True,
            "archive_checked_utc": row["checked_utc"], "evidence_projection_path": str(LEDGER.relative_to(ROOT)),
            "evidence_projection_line_1based": number,
            "evidence_projection_row_sha256": sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()),
            "method_amendment_commit": "8358b5e75ca45fd9bf0e26cab70e2acc1bc39493",
        }
        if k in existing:
            assert existing[k] == binding
        else:
            added.append(binding)
    append(path, added)
    print(json.dumps({"added_bindings": [{"repository": row["repository"], "pr_number": row["pr_number"]} for row in added]}))


def finalize():
    target_rows = rows(HERE / "recipient_prefix_archive_targets.jsonl")
    targets = {key(row): row for row in target_rows}
    projections = {key(row): row for row in rows(LEDGER)}
    assert len(targets) == len(projections) == 11
    attempts_path = HERE / "recipient_attempts.jsonl"
    attempts = rows(attempts_path)
    inspections, inspection_lines = {}, {}
    for number, row in enumerate(attempts, 1):
        if row["stage"] in {"inspect_initial_commit", "inspect_archived_opening"}:
            inspection_lines.setdefault(key(row), []).append(number)
            if row["stage"] == "inspect_archived_opening" and key(row) in targets:
                inspections[key(row)] = row
    assert len(inspections) == 11, "Some archived first diffs remain uninspected"
    assert all(row["archive_opened_event_verified"] for row in inspections.values())
    assert all(row["structural_exclusion_reason"] == "no_added_or_renamed_proposal_markdown_in_archived_opening_diff" for row in inspections.values()), "A newly eligible path or capped diff requires renewed recipient selection"
    assert all(not row["added_design_paths"] and not row["compare_file_cap_possible"] for row in inspections.values())
    frame_path = HERE / "recipient_frame.csv"
    selection_path = HERE / "recipient_selection.json"
    before = {"frame_sha256": sha(frame_path.read_bytes()), "selection_sha256": sha(selection_path.read_bytes())}
    for source, name in [(frame_path, "recipient_frame_before_prefix_verification.csv"), (selection_path, "recipient_selection_before_prefix_verification.json")]:
        dest = HERE / name
        assert not dest.exists(), "Before-check record already exists"
        shutil.copyfile(source, dest)
    with frame_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        frame = list(reader)
    for row in frame:
        k = row["repository"], int(row["pr_number"])
        if k in targets:
            assert row["screening_state"] == "excluded" and row["primary_chronological_prefix"] == "true"
            row["initiality_status"] = "archive_opened_event_verified"
            row["selection_reason"] = "no_added_or_renamed_proposal_markdown_in_archived_opening_diff"
            row["inspection_attempt_lines_1based"] = ";".join(map(str, inspection_lines[k]))
    with frame_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(frame)
    selection = json.loads(selection_path.read_text())
    selection["primary_prefix"]["archive_verified_excluded_heads"] = 15
    selection["primary_prefix"]["surviving_history_excluded_heads_with_initiality_uncertainty"] = 0
    selection["annotated_frame_sha256"] = sha(frame_path.read_bytes())
    selection["limitations"] = [text for text in selection["limitations"] if not text.startswith("Eleven primary-prefix")]
    selection["limitations"].append("All fifteen primary-prefix structural exclusions are now checked against archived opening base-to-head comparisons. Added and renamed Markdown paths were both considered; each inspected opening diff has neither under the repository's proposal directory.")
    selection["prefix_archive_verification"] = {
        "completed_at_utc": now(), "projection_path": str(LEDGER.relative_to(ROOT)),
        "projection_file_sha256": sha(LEDGER.read_bytes()), "rows": 11,
        "opening_heads_matching_reconstruction": sum(row["archived_opening_head_sha"] == targets[k]["opening_head_candidate_sha"] for k, row in projections.items()),
        "new_proposal_paths_found": 0, "selected_identities_changed": False,
        "before_state": before, "before_frame_path": str((HERE / "recipient_frame_before_prefix_verification.csv").relative_to(ROOT)),
        "before_selection_path": str((HERE / "recipient_selection_before_prefix_verification.json").relative_to(ROOT)),
    }
    selection_path.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n")
    event = {"stage": "archive_prefix_verification_complete", **selection["prefix_archive_verification"],
             "after_frame_sha256": sha(frame_path.read_bytes()), "after_selection_sha256": sha(selection_path.read_bytes()),
             "target_packet_sha256_unchanged": sha((HERE / "recipient_targets.jsonl").read_bytes()),
             "donor_material_read": False, "followup_outcomes_read": False}
    append(attempts_path, [event])
    print(json.dumps(event))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["bind", "finalize"])
    args = parser.parse_args()
    bind() if args.mode == "bind" else finalize()
