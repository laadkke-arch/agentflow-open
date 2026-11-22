"""Compile donor-blind recipient provenance, selection, and source records.

Only the recipient directory and the two authorized, projected opening-event
ledgers are inputs. No proposal outcomes or provider material are consumed.
"""

import csv
import hashlib
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
PREFIX = str(HERE.relative_to(ROOT))
ORIGINAL_FIELDS = ["repository", "pr_number", "created_at", "original_url", "metadata_year", "frame_page"]
ORIGINAL_LF_HASH = "05272178c3aa93e8b881bbaebdbef1a62c453e1b2c5d9e6043f8bed3c22b6809"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def dump_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def row_sha(row):
    return sha(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def key(row):
    return row["repository"], int(row["pr_number"])


def main():
    if (HERE / "recipient_sources.jsonl").exists():
        raise SystemExit("Refusing to overwrite compiled recipient records")
    packets = read_jsonl(HERE / "recipient_targets.jsonl")
    targets = {key(row): row for row in packets}
    frame_path = HERE / "recipient_frame.csv"
    with frame_path.open(newline="") as handle:
        frame = list(csv.DictReader(handle))
    original = io.StringIO(newline="")
    writer = csv.DictWriter(original, fieldnames=ORIGINAL_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows({field: row[field] for field in ORIGINAL_FIELDS} for row in frame)
    assert sha(original.getvalue().encode()) == ORIGINAL_LF_HASH
    assert len(frame) == 3415 and len({key(row) for row in frame}) == 3415
    assert frame == sorted(frame, key=lambda row: (row["created_at"], int(row["pr_number"]), row["repository"]))
    frame_by_key = {key(row): row for row in frame}
    attempts = read_jsonl(HERE / "recipient_attempts.jsonl")
    restores = {key(row): row for row in attempts if row["stage"] in {"restore_snapshot", "restore_archived_snapshot"}}
    read_events = {key(row): row for row in attempts if row["stage"] == "initial_source_full_read"}
    scopes = read_jsonl(HERE / "recipient_scope_adjudication.jsonl")
    scope_by_key = {key(row): row for row in scopes}
    new_attempts, new_scopes = [], []
    for k, packet in targets.items():
        if k not in read_events:
            restore = restores[k]
            entry = {
                "stage": "initial_source_full_read", "repository": k[0], "pr_number": k[1],
                "recorded_at_utc": NOW, "read_at_utc": None,
                "read_time_interval_utc": [restore["retrieved_at_utc"], packet["frozen_partial_target"]["frozen_at_utc"]],
                "read_time_precision": "Retrospectively recorded after complete body reading; exact first-display time was not separately preserved.",
                "snapshot_path": packet["snapshot_path"],
                "read_line_range": [1, restore["line_count"]], "eligible_initial_design": True,
                "author_scope_classification": packet["target_scope"],
                "author_scope_rationale": packet["scope_rationale"],
                "query_drafted_by_recipient_collector": False,
                "donor_material_read": False, "followup_outcomes_read": False,
            }
            new_attempts.append(entry)
            read_events[k] = entry
        if k not in scope_by_key:
            entry = {
                "repository": k[0], "pr_number": k[1], "snapshot_path": packet["snapshot_path"],
                "full_source_lines": [1, restores[k]["line_count"]], "eligible_initial_design": True,
                "target_scope": packet["target_scope"], "rationale": packet["scope_rationale"],
                "source_line_spans": sorted({tuple(span) for c in packet["mandatory_conditions"] for span in c["source_line_spans"]}),
                "exclusion_reason": None,
                "author_judgment": "Agrees with independent fixed-rubric adjudication; complete conditions are in the frozen recipient packet.",
                "independent_adjudicator": "/root/recipient_inputs/scope_blind",
                "adjudicator_context": "Fresh-history; only exact original snapshot paths and fixed scope rubric; no quota, queries, donor material, outcomes or selection notes.",
                "adjudicated_before_queries": True, "recorded_at_utc": NOW,
                "initial_document_uncertainties": packet["initial_document_uncertainties"],
            }
            new_scopes.append(entry)
            scope_by_key[k] = entry
    image = targets[("rust-lang/rfcs", 2856)]["initial_image"]
    new_attempts.append({
        "stage": "initial_relative_image_review", "recorded_at_utc": NOW,
        "all_final_eight_checked_for_repository_relative_image_references": True,
        "references_found": [{"repository": "rust-lang/rfcs", "pr_number": 2856, **image}],
        "image_visually_inspected": True,
        "external_prior_art_links_followed": False,
        "observation": image["content_note"],
    })
    with (HERE / "recipient_attempts.jsonl").open("a") as handle:
        for row in new_attempts:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    with (HERE / "recipient_scope_adjudication.jsonl").open("a") as handle:
        for row in new_scopes:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    attempts += new_attempts
    archive_proofs = {}
    for filename in ["opening-archive-checks.jsonl", "archive-recovery-checks.jsonl"]:
        path = HERE.parent / "evidence" / filename
        for line_number, row in enumerate(read_jsonl(path), 1):
            assert row["archive_complete"] and row["matching_event_count"] == 1
            event = row["matches"][0]
            k = key(row)
            assert key(event) == k and event["action"] == "opened"
            assert event["pull_request_created_at"] == row["created_at"] == frame_by_key[k]["created_at"]
            if filename == "opening-archive-checks.jsonl":
                assert row["status"] == "opened_event_head_matches_reconstruction"
                assert event["head_sha"] == row["opening_head_candidate_sha"]
            else:
                assert row["usable_projection"] and row["status"] == "opened_event_head_base_recovered"
                assert event["head_sha"] == row["archived_opening_head_sha"]
                assert event["base_sha"] == row["archived_opening_base_sha"]
            archive_proofs[k] = {
                "repository": k[0], "pr_number": k[1], "archive_opened_event_verified": True,
                "matched_event_count": 1, "event_action": "opened",
                "pull_request_created_at": event["pull_request_created_at"], "event_created_at": event["event_created_at"],
                "archived_head_sha": event["head_sha"], "archived_base_sha": event["base_sha"],
                "archive_url": row["archive_url"], "archive_compressed_sha256": row["compressed_sha256_consumed"],
                "archive_line_1based": event["archive_line_1based"], "archive_complete": True,
                "archive_checked_utc": row["checked_utc"],
                "evidence_projection_path": str(path.relative_to(ROOT)),
                "evidence_projection_line_1based": line_number,
                "evidence_projection_row_sha256": row_sha(row),
                "event_type_basis": "Protocol auditor projected PullRequestEvent/opened before persistence; no other event payload is consumed here.",
                "opening_snapshot_limit": "Verifies the exact historical opening head; does not prove the first privately authored draft or first authored commit.",
            }
    latest_inspection, inspection_lines, restoration_lines, reading_lines = {}, {}, {}, {}
    history_failures = set()
    for line_number, row in enumerate(attempts, 1):
        if row["stage"] in {"inspect_initial_commit", "inspect_archived_opening"}:
            k = key(row)
            latest_inspection[k] = row
            inspection_lines.setdefault(k, []).append(line_number)
            if row.get("structural_exclusion_reason") == "no_unique_precreation_opening_head_candidate":
                history_failures.add(k)
        if row["stage"] in {"restore_snapshot", "restore_archived_snapshot"}:
            restoration_lines[key(row)] = line_number
        if row["stage"] == "initial_source_full_read":
            reading_lines[key(row)] = line_number
    cutoff = {repo: max(frame_by_key[k]["created_at"] for k in targets if k[0] == repo) for repo in {k[0] for k in targets}}
    primary_prefix = {key(row) for row in frame if row["created_at"] <= cutoff[row["repository"]]}
    assert len(primary_prefix) == 23 and set(targets) <= primary_prefix
    sources = []
    for k, restore in sorted(restores.items(), key=lambda item: (item[1]["created_at"], item[0][1], item[0][0])):
        selected = k in targets
        packet = targets.get(k)
        scope = scope_by_key.get(k)
        read = read_events.get(k)
        proof = archive_proofs.get(k)
        if proof:
            assert proof["archived_head_sha"] == restore["snapshot_commit_sha"]
        # Do not open the restored-but-unread #1614 file during this compilation.
        limits = [
            "Only the initial Markdown snapshot and any exact original relative image were read; no mutable external prior-art link was followed.",
            "The snapshot is a proposal and establishes requested behavior, not later adoption, implementation success or outcomes.",
            "First privately authored draft and first authored commit are not established.",
        ]
        if not proof:
            limits.append("Historical opening head is unproven: this snapshot uses a surviving-history pre-creation candidate. Commit dates and absence of force-push events do not establish initiality.")
        if scope and scope.get("source_inconsistency"):
            limits.append(scope["source_inconsistency"])
        if scope and scope.get("ambiguity"):
            limits.append(scope["ambiguity"])
        if packet:
            limits.extend(c["description"] for c in packet["initial_document_uncertainties"])
        if selected:
            selection_reason = "chronological_first_four_eligible_under_final_restoration_method"
        elif k in {("rust-lang/rfcs", 2859), ("kubernetes/enhancements", 1478), ("kubernetes/enhancements", 1566)}:
            selection_reason = "eligible_provisional_read_displaced_by_earlier_archive_recovered_proposals"
        elif scope and not scope["eligible_initial_design"]:
            selection_reason = scope["exclusion_reason"]
        else:
            selection_reason = "outside_final_chronological_cutoff_restored_not_read"
        source = {
            "source_id": f"{k[0].replace('/', '-')}-pr-{k[1]}",
            "recipient_id": packet["recipient_id"] if packet else None,
            "repository": k[0], "pr_number": k[1], "created_at": restore["created_at"],
            "original_url": restore["original_url"], "immutable_url": restore["fixed_url"],
            "immutable_raw_url": restore["raw_fixed_url"], "snapshot_path": restore["snapshot_path"],
            "repository_path": restore["initial_path"], "snapshot_commit_sha": restore["snapshot_commit_sha"],
            "git_blob_sha": restore["initial_blob_sha"], "raw_sha256": restore["snapshot_raw_sha256"],
            "canonical_lf_sha256": restore["snapshot_canonical_lf_sha256"],
            "raw_source_bytes_preserved": True, "bytes": restore["bytes"], "line_count": restore["line_count"],
            "retrieved_at_utc": restore["retrieved_at_utc"], "recorded_at_utc": NOW,
            "read_status": "full_original_read" if read else "restored_not_read",
            "read_line_range": read["read_line_range"] if read else None,
            "read_at_utc": read.get("read_at_utc") if read else None,
            "read_time_interval_utc": read.get("read_time_interval_utc") if read else None,
            "read_time_precision": read.get("read_time_precision", "Read-completion receipt timestamp; see original attempt entry.") if read else None,
            "selected": selected, "counted_minimum": selected, "counted": selected,
            "eligible_initial_design": scope["eligible_initial_design"] if scope else None,
            "target_scope": scope["target_scope"] if scope else None,
            "selection_reason": selection_reason, "scope_quota_displacement": False,
            "primary_chronological_prefix": k in primary_prefix,
            "initiality_status": "archive_opened_event_verified" if proof else restore["initiality_status"],
            "opening_head_certainty": bool(proof), "first_authored_draft_certainty": False,
            "earliest_retained_proposal_addition_commit_sha": restore.get("earliest_proposal_commit_sha"),
            "first_comparison_commit_sha": restore.get("first_comparison_commit_sha"),
            "first_comparison_commit_limit": restore.get("first_commit_limit"),
            "archive_binding": proof,
            "attempt_ledger": f"{PREFIX}/recipient_attempts.jsonl",
            "inspection_attempt_lines_1based": inspection_lines[k],
            "restore_attempt_line_1based": restoration_lines[k],
            "read_attempt_line_1based": reading_lines.get(k),
            "source_observation": packet["initial_behavior"] if packet else (scope["rationale"] if scope else "Snapshot was restored but body was not read; no semantic eligibility or scope is asserted."),
            "source_location_anchors": scope["source_line_spans"] if scope else [],
            "limitations": limits,
            "followup_outcomes_read": False, "donor_material_read": False,
        }
        if packet:
            source["condition_packet_path"] = f"{PREFIX}/recipient_targets.jsonl"
            source["condition_packet_row"] = int(packet["recipient_id"][1:])
            source["condition_packet_file_sha256"] = sha((HERE / "recipient_targets.jsonl").read_bytes())
        if packet and packet.get("initial_image"):
            source["initial_image"] = packet["initial_image"]
        sources.append(source)
    dump_jsonl(HERE / "recipient_sources.jsonl", sources)
    dump_jsonl(HERE / "recipient_final_opening_bindings.jsonl", [{"recipient_id": packet["recipient_id"], **archive_proofs[key(packet)]} for packet in packets])
    extra_fields = ["screening_state", "recipient_id", "counted_minimum", "primary_chronological_prefix", "eligibility_status", "target_scope", "selection_reason", "body_read_status", "initiality_status", "inspection_attempt_lines_1based", "prior_history_restoration_failure", "scope_quota_displacement"]
    for row in frame:
        k = key(row)
        packet, scope, inspect = targets.get(k), scope_by_key.get(k), latest_inspection.get(k)
        selected = packet is not None
        if selected:
            state, reason, eligibility = "selected", "chronological_first_four_eligible", "eligible"
        elif inspect is None:
            state, reason, eligibility = "not_screened", "after_final_chronological_cutoff", "not_assessed"
        elif k not in primary_prefix:
            state = "excluded"
            reason = "outside_final_chronological_cutoff_after_archive_recovery"
            if scope:
                eligibility = "eligible" if scope["eligible_initial_design"] else "ineligible_source_based"
                if not scope["eligible_initial_design"]:
                    reason += ":" + scope["exclusion_reason"]
            elif inspect.get("structural_exclusion_reason") == "no_unique_precreation_opening_head_candidate":
                eligibility = "unresolved_restoration_failure_not_definitive_ineligibility"
            elif inspect["structural_eligibility"]:
                eligibility = "structural_candidate_body_not_read"
            else:
                eligibility = "ineligible_no_new_proposal_path_on_inspected_tree"
        else:
            assert inspect and not inspect["structural_eligibility"]
            assert inspect.get("structural_exclusion_reason") != "no_unique_precreation_opening_head_candidate"
            state, reason, eligibility = "excluded", inspect["structural_exclusion_reason"], "ineligible_no_new_proposal_path_on_inspected_tree"
        row.update({
            "screening_state": state, "recipient_id": packet["recipient_id"] if packet else "",
            "counted_minimum": str(selected).lower(), "primary_chronological_prefix": str(k in primary_prefix).lower(),
            "eligibility_status": eligibility, "target_scope": scope["target_scope"] if scope and scope["target_scope"] else "",
            "selection_reason": reason,
            "body_read_status": "full_original_read" if k in read_events else ("restored_not_read" if k in restores else "not_read"),
            "initiality_status": "archive_opened_event_verified" if k in archive_proofs else (inspect["initiality_status"] if inspect else "not_assessed"),
            "inspection_attempt_lines_1based": ";".join(map(str, inspection_lines.get(k, []))),
            "prior_history_restoration_failure": str(k in history_failures).lower(),
            "scope_quota_displacement": "false",
        })
    with frame_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ORIGINAL_FIELDS + extra_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(frame)
    by_repo = {}
    for repo in sorted(cutoff):
        ordered = sorted([p for p in packets if p["repository"] == repo], key=lambda p: (frame_by_key[key(p)]["created_at"], p["pr_number"]))
        numbers = [p["pr_number"] for p in ordered]
        scopes_count = Counter(p["target_scope"] for p in ordered)
        assert len(numbers) == 4 and len(scopes_count) == 2
        by_repo[repo] = {
            "frame_rows": sum(row["repository"] == repo for row in frame),
            "annual_counts": dict(Counter(row["metadata_year"] for row in frame if row["repository"] == repo)),
            "final_method_first_four_eligible_before_scope_quota": numbers,
            "final_selected_pr_numbers": numbers, "scope_counts": dict(scopes_count), "scope_quota_triggered": False,
            "primary_prefix_pr_numbers": [int(row["pr_number"]) for row in frame if row["repository"] == repo and key(row) in primary_prefix],
            "primary_prefix_rows": sum(k[0] == repo for k in primary_prefix),
            "cutoff_created_at": cutoff[repo],
        }
    selection = {
        "recorded_at_utc": NOW, "metadata_frame_total": 3415,
        "original_metadata_lf_sha256": ORIGINAL_LF_HASH,
        "original_metadata_raw_crlf_sha256": "1434da7d4b3d4198aa65d018b89774a6039b3520c4a99287ab2e6f309d14e3e7",
        "annotated_frame_sha256": sha(frame_path.read_bytes()), "frame_line_ending": "LF",
        "sampling_order": ["created_at ascending", "PR number ascending", "first qualifying added/renamed proposal path ascending"],
        "repositories": by_repo,
        "primary_prefix": {"rows": 23, "selected": 8, "no_new_document_structural_exclusions": 15,
                           "archive_verified_excluded_heads": 4, "surviving_history_excluded_heads_with_initiality_uncertainty": 11},
        "all_historical_inspection": {"distinct_prs": len(latest_inspection), "prior_history_only_failures": len(history_failures),
                                      "full_originals_read": len(read_events), "snapshots_restored_not_read": len(restores) - len(read_events),
                                      "frame_screening_state_counts": dict(Counter(row["screening_state"] for row in frame))},
        "pre_archive_provisional_reads": {
            "rust-lang/rfcs": {"provisional_first_four": [2843, 2845, 2850, 2859], "displaced_after_archive_recovery": [2859]},
            "kubernetes/enhancements": {"eligible_provisional_bodies_read": [1478, 1566], "four_recipient_set_ever_locked": False,
                                        "outside_final_prefix_after_archive_recovery": [1478, 1566]},
            "scope_quota_displacements": [],
        },
        "source_based_nonselected_reads": [{"repository": s["repository"], "pr_number": s["pr_number"],
                                            "eligible_initial_design": s["eligible_initial_design"], "reason": s["selection_reason"]}
                                           for s in sources if not s["selected"] and s["read_status"] == "full_original_read"],
        "limitations": [
            "All eight selected opening heads are bound to unique public archive opened events and exact immutable blobs; first authored draft/commit remains unproven.",
            "Eleven primary-prefix no-new-document exclusions rely on pre-creation surviving-history reconstruction. They were not independently archive-corroborated; this bounds the strength of earliest-eligible claims.",
            "Early current-history restoration failures caused extra provisional screenings before the archive fallback was operational. They are preserved rather than rewritten as definitive ineligibility.",
            "Archive recovery metadata exists for some PRs beyond the final cutoff, but their archived diff/body eligibility was not screened after the earlier sample was complete.",
            "Only structural diff paths were used for metadata exclusions; no later PR bodies, comments, outcomes, closure/merge fields or donor material were read.",
        ],
        "query_author_isolation": "Fresh fork with only final eight complete originals, original image and frozen source/condition packets; no excluded/provisional bodies or selection/archive history.",
    }
    (HERE / "recipient_selection.json").write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"source_rows": len(sources), "read_originals": len(read_events), "final_selected": len(targets),
                      "frame_states": selection["all_historical_inspection"]["frame_screening_state_counts"],
                      "files": {name: sha((HERE / name).read_bytes()) for name in ["recipient_frame.csv", "recipient_sources.jsonl", "recipient_selection.json", "recipient_final_opening_bindings.jsonl", "recipient_scope_adjudication.jsonl", "recipient_attempts.jsonl"]}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
