#!/usr/bin/env python3
"""Recalculate AF-RES-101 from sealed evidence; standard library, no network.

Run without arguments from any directory.  Only evidence/reconciliation.json is
written.  Semantic source judgments remain inputs: this program checks their
consistency, provenance, windows, denominators and filter arithmetic.  It does
not infer author knowledge from thanks, acceptance, or a research execution.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit


BASE = Path(__file__).resolve().parent
OUTPUT = BASE / "evidence/reconciliation.json"
CASE_IDS = ["IM-A1", "IM-A2", "IM-U1", "IM-U2", "TY-A1", "TY-A2", "TY-U1", "TY-U2"]
EXPECTED_VALID = {"TY-A1-C2", "TY-A2-C1", "TY-A2-C2"}
EXPECTED_BLANKS = {"IM-A2-C3", "IM-U2-C3", "TY-A2-C3", "TY-U2-C1", "TY-U2-C2", "TY-U2-C3"}
SEALED_SOURCE_ROWS = 191
EXPECTED_COMMITS = {
    1: "9d646592613ba2fd9c52bc9bbf3dbc28bac68693",
    2: "4e7539906eb03abd46e6910643ed5317f97ddb45",
    3: "c68b40e646dffcc41261ea21974c2bbfeab53348",
}
# The two records explicitly refer to the same edited code/error episode.
# This is an evidence linkage, not an automatic rule merging all trials of a
# candidate.  Any additional execution record must be linked explicitly.
MODIFIED_EPISODE_RECORDS = {"IM-A1-R2", "IM-A1-C137114172"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def timestamp(value):
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00").replace(" UTC", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no UTC offset: " + str(value))
    return parsed.astimezone(timezone.utc)


def optional_int(value):
    return None if value is None or value == "" else int(value)


def truth(value):
    if value is True or str(value).lower() == "true":
        return True
    if value is False or str(value).lower() == "false":
        return False
    return None


def json_cell(row, key, default=None):
    value = row.get(key)
    return default if value is None or value == "" else json.loads(value)


def supported(value):
    return isinstance(value, str) and value.startswith("지지")


def unknown(value):
    return value is None or value in ("", "미확인", "unknown", "not_stated")


def ordered_ids(values):
    order = {case: n for n, case in enumerate(CASE_IDS)}
    return sorted(values, key=lambda cid: (order.get(cid.rsplit("-C", 1)[0], 99), cid))


class Audit:
    def __init__(self):
        self.errors = []
        self.checks = 0
        self.inputs = {}
        self.raw_inputs = {}

    def check(self, condition, code, location, expected=None, actual=None):
        self.checks += 1
        if not condition:
            self.errors.append({"code": code, "location": location, "expected": expected, "actual": actual})

    def equal(self, actual, expected, code, location):
        self.check(actual == expected, code, location, expected, actual)

    def read(self, relative):
        if relative not in self.raw_inputs:
            data = (BASE / relative).read_bytes()
            self.raw_inputs[relative] = data
            self.inputs[relative] = {"sha256": sha256(data), "bytes": len(data)}
        return self.raw_inputs[relative]

    def json(self, relative):
        return json.loads(self.read(relative))

    def jsonl(self, relative):
        return [json.loads(line) for line in self.read(relative).decode("utf-8").splitlines() if line.strip()]

    def csv(self, relative):
        return list(csv.DictReader(io.StringIO(self.read(relative).decode("utf-8"), newline="")))


def filter_candidates(rows, policy, decision_overrides=None, omitted=None):
    """Return the first two surviving original candidates in each request."""
    decision_overrides = decision_overrides or {}
    omitted = omitted or set()
    result = {"excluded_ids": [], "surviving_ids": [], "returned_ids": [], "per_case": {}, "positions": {}}
    for case in CASE_IDS:
        case_rows = sorted((r for r in rows if r["case_id"] == case), key=lambda r: int(r["original_rank"]))
        survivors = []
        excluded = []
        for row in case_rows:
            cid = row["candidate_id"]
            if truth(row["blank"]) is True or cid in omitted:
                continue
            decision = decision_overrides.get(cid, row[policy + "_decision"])
            if decision == "exclude":
                excluded.append(cid)
                result["positions"][cid] = {"survivor_rank": None, "returned_rank": None, "rank_shift": None}
            elif decision == "keep":
                survivors.append(cid)
                rank = len(survivors)
                result["positions"][cid] = {
                    "survivor_rank": rank,
                    "returned_rank": rank if rank <= 2 else None,
                    "rank_shift": int(row["original_rank"]) - rank,
                }
            else:
                raise ValueError(f"invalid {policy} decision for {cid}: {decision}")
        result["per_case"][case] = {"excluded_ids": excluded, "surviving_ids": survivors, "returned_ids": survivors[:2]}
        result["excluded_ids"].extend(excluded)
        result["surviving_ids"].extend(survivors)
        result["returned_ids"].extend(survivors[:2])
    for name in ("excluded", "surviving", "returned"):
        result[name + "_count"] = len(result[name + "_ids"])
    return result


def metric(eligible, a_ids, b_ids, *, unit="candidate", comparison="excluded"):
    denominator_ids = ordered_ids(eligible)
    a = ordered_ids(set(denominator_ids) & set(a_ids))
    b = ordered_ids(set(denominator_ids) & set(b_ids))
    count = len(denominator_ids)
    return {
        "unit": unit,
        "comparison": comparison,
        "denominator": count,
        "denominator_ids": denominator_ids,
        "A": {"numerator": len(a), "numerator_ids": a, "rate": len(a) / count if count else None},
        "B": {"numerator": len(b), "numerator_ids": b, "rate": len(b) / count if count else None},
        "rate_status": "계산 가능(해당 범위만)" if count else "산출 불가",
        "request_clusters": sorted({cid.rsplit("-C", 1)[0] for cid in denominator_ids}),
    }


def source_group(source):
    category = source.get("category")
    sid = source["source_id"]
    if category == "selected_request":
        return "selected_requests"
    if category == "cross_domain_official":
        return "cross_domain_official_manual_tests"
    if category == "supplemental_primary":
        return "supplemental_primary"
    if category == "official_imagemagick":
        return "imagemagick_documents_implementations"
    if category == "upstream_test_bundle" and sid.startswith("IM-"):
        return "imagemagick_upstream_tests"
    if category in ("official_document", "official_implementation") and sid.startswith("TY-"):
        return "typst_documents_implementations"
    if category == "upstream_test" and sid.startswith("TY-"):
        return "typst_upstream_input_expected_bundles"
    return "unclassified"


def canonical_source_url(url):
    parsed = urlsplit(url)
    path = parsed.path
    if parsed.netloc == "raw.githubusercontent.com":
        pieces = path.strip("/").split("/", 3)
        if len(pieces) == 4:
            return "github:" + "/".join(pieces)
    if parsed.netloc == "github.com" and "/blob/" in path:
        return "github:" + path.strip("/").replace("/blob/", "/", 1)
    return parsed.netloc.lower() + path.rstrip("/")


def noneligible_reason(assessment):
    """Classify existing semantic judgments; do not flatten them to 'missing'."""
    validity = assessment.get("validity", "")
    output = assessment.get("required_output_status", "")
    if output.startswith("반박"):
        code = "literal_required_output_refuted"
    elif assessment.get("valid_output_operation_on_research_input") is True:
        code = "supported_output_prior_actual_attempt_unconfirmed"
    elif validity.startswith("literal_token_fails"):
        code = "literal_token_counterexample_intended_call_conditional"
    elif validity.startswith("reference_version_counterevidence"):
        code = "reference_library_counterevidence_historical_version_unknown"
    elif validity.startswith("literal shell-argument"):
        code = "literal_argument_counterevidence_original_execution_unknown"
    elif validity.startswith("conditional core CLI"):
        code = "core_cli_supported_whole_wrapper_unverified"
    elif validity == "parameter_under_specified_conditional":
        code = "underspecified_parameters_conditional"
    elif validity.startswith("algorithmic proposal"):
        code = "algorithm_and_required_decoder_output_unverified"
    elif "QR" in validity:
        code = "image_operation_supported_required_decoder_output_unverified"
    elif "perspective" in validity or "planar" in validity:
        code = "planar_component_supported_required_automation_unverified"
    else:
        code = "unclassified"
    reasons = [assessment.get(k) for k in ("required_output_reason", "hard_constraint_reason", "actual_observation") if assessment.get(k)]
    return {
        "candidate_id": assessment["candidate_id"],
        "reason_code": code,
        "required_output_status": output,
        "hard_constraint_status": assessment.get("hard_constraint_status"),
        "hard_constraints": assessment.get("hard_constraints", []),
        "validity": validity,
        "reason": " ".join(reasons),
        "literal_evidence_status": assessment.get("literal_evidence_status"),
        "source_ids": assessment.get("source_ids", []),
        "observation_receipt": assessment.get("observation_receipt", assessment.get("execution_receipt")),
        "limitations": assessment.get("limitations", assessment.get("unknowns", [])),
    }


def run(audit):
    initial = audit.csv("initial.csv")
    frame = audit.csv("frame.csv")
    candidates = audit.csv("candidates.csv")
    followup = audit.csv("followup.csv")
    assessments = audit.json("evidence/assessment.json")
    sources = audit.jsonl("sources.jsonl")
    source_counts = audit.json("evidence/source-counts.json")
    seals = {
        1: audit.json("evidence/seals/initial.json"),
        2: audit.json("evidence/seals/candidates.json"),
        3: audit.json("evidence/seals/behavior-followup.json"),
    }
    commits = audit.jsonl("evidence/seals/commits.jsonl")
    transport = audit.json("evidence/seals/transport-normalization.json")
    im_candidates = audit.json("evidence/imagemagick/candidate-part.json")
    ty_candidates = audit.json("evidence/typst/candidate-part.json")
    im_assessments = audit.json("evidence/imagemagick/stage3/assessment-part.json")
    ty_assessments = audit.json("evidence/typst-official/assessment.json")
    audit.read("SCOPE.md")
    initial_by_id = {r["case_id"]: r for r in initial}
    candidate_by_id = {r["candidate_id"]: r for r in candidates}
    assessment_by_id = {r["candidate_id"]: r for r in assessments}
    part_candidates = {r["candidate_id"]: r for r in im_candidates + ty_candidates}
    part_assessments = {r["candidate_id"]: r for r in im_assessments + ty_assessments}
    expected_ids = {f"{case}-C{n}" for case in CASE_IDS for n in (1, 2, 3)}

    # Frozen hashes: accept only recorded bytes or a documented CRLF -> LF form.
    normalization = {row["path"]: row for row in transport["rows"]}
    source_additions = sources[SEALED_SOURCE_ROWS:]
    audit.check(len(source_additions) in (0, 2), "post_stage3_method_addition_count", "sources.jsonl", "0 or 2", len(source_additions))
    for source in source_additions:
        audit.equal(source.get("category"), "reproduction_method", "post_stage3_method_only", source["source_id"])
        audit.equal(source.get("counted"), False, "post_stage3_methods_not_counted", source["source_id"])
    if source_additions:
        additions_receipt = audit.jsonl("evidence/reproduction-sources.jsonl")
        for source in source_additions:
            audit.equal(source.get("raw_source_record"), "evidence/reproduction-sources.jsonl", "method_addition_receipt_locator", source["source_id"])
        original_additions = [{k: v for k, v in source.items() if k != "raw_source_record"} for source in source_additions]
        audit.equal(original_additions, additions_receipt, "method_additions_match_direct_read_receipt", "sources.jsonl")
        audit.check(bool(source_counts.get("post_stage3_method_additions")), "method_additions_disclosed", "source-counts.json")
    sealed_files = {
        1: ["SCOPE.md", "frame.csv", "initial.csv"],
        2: ["candidates.csv", "evidence/imagemagick/candidate-part.json", "evidence/typst/candidate-part.json"],
        3: ["followup.csv", "evidence/assessment.json", "sources.jsonl", "evidence/source-counts.json",
            "evidence/imagemagick/stage3/assessment-part.json", "evidence/typst-official/assessment.json"],
    }
    seal_checks = []
    for stage, paths in sealed_files.items():
        entries = {r["path"]: r["sha256"] for r in seals[stage]["files"]}
        for relative in paths:
            data = audit.read(relative)
            expected = entries.get(relative)
            observed = sha256(data)
            note = "exact sealed bytes"
            valid = observed == expected
            extra_verification = {}
            if relative == "sources.jsonl" and source_additions:
                prefix = b"".join(data.splitlines(keepends=True)[:SEALED_SOURCE_ROWS])
                prefix_hash = sha256(prefix)
                valid = prefix_hash == expected
                note = "Original 191 rows preserved byte-for-byte; two uncounted reproduction-method rows appended after stage 3."
                extra_verification = {"preserved_prefix_rows": SEALED_SOURCE_ROWS, "observed_prefix_sha256": prefix_hash, "post_stage3_added_ids": [s["source_id"] for s in source_additions]}
            elif relative == "evidence/source-counts.json" and source_additions:
                original_counts = dict(source_counts)
                original_counts["ledger_rows"] = SEALED_SOURCE_ROWS
                original_counts.pop("post_stage3_method_additions", None)
                reconstructed = (json.dumps(original_counts, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
                reconstructed_hash = sha256(reconstructed)
                valid = reconstructed_hash == expected
                note = "Only ledger_rows and disclosed post_stage3_method_additions may differ; reconstructed stage-3 receipt hash must match."
                extra_verification = {"reconstructed_stage3_sha256": reconstructed_hash, "allowed_changed_fields": ["ledger_rows", "post_stage3_method_additions"]}
            transport_row = normalization.get(relative)
            if transport_row:
                audit.equal(transport_row["preupload_sha256"], expected, "transport_preupload_matches_seal", relative)
                normalized_hash = sha256(data.replace(b"\r\n", b"\n"))
                audit.equal(normalized_hash, transport_row["committed_sha256"], "documented_lf_hash", relative)
                valid = valid or (observed == transport_row["committed_sha256"] and transport_row["crlf_to_lf_only"] is True)
                note = "sealed CRLF or documented LF bytes; parsed records unchanged"
            audit.check(valid, "frozen_file_hash", relative, expected, observed)
            seal_checks.append({"stage": stage, "path": relative, "sealed_sha256": expected, "observed_sha256": observed, "valid": valid, "scope": note, **extra_verification})
    commit_lines = audit.read("evidence/seals/commits.jsonl").splitlines(keepends=True)
    for stage in (2, 3):
        prefix_expected = next(r["sha256"] for r in seals[stage]["files"] if r["path"] == "evidence/seals/commits.jsonl")
        prefix_observed = sha256(b"".join(commit_lines[:stage - 1]))
        audit.equal(prefix_observed, prefix_expected, "append_only_commit_receipt_prefix", f"stage{stage}")
        seal_checks.append({"stage": stage, "path": "evidence/seals/commits.jsonl", "preserved_prefix_rows": stage - 1, "sealed_sha256": prefix_expected, "observed_prefix_sha256": prefix_observed, "valid": prefix_observed == prefix_expected})
    normalized_commits = []
    for raw_record in commits:
        stage = int(raw_record["stage"])
        record = dict(raw_record)
        record["remote_sha"] = raw_record.get("remote_sha", raw_record.get("commit"))
        record["parent_sha"] = raw_record.get("parent_sha", raw_record.get("parent"))
        record["remote_ref_verified_utc"] = raw_record.get("remote_ref_verified_utc", raw_record.get("remote_verified_utc"))
        if not record.get("sealed_utc") and raw_record.get("seal_file"):
            seal_path = raw_record["seal_file"]
            prefix = "docs/workstreams/research/AF-RES-101/"
            if seal_path.startswith(prefix):
                seal_path = seal_path[len(prefix):]
            linked_seal = audit.json(seal_path)
            audit.equal(int(linked_seal["stage"]), stage, "commit_linked_seal_stage", f"stage{stage}")
            record["sealed_utc"] = linked_seal["seal_utc"]
        normalized_commits.append(record)
    commit_by_stage = {int(r["stage"]): r for r in normalized_commits}
    audit.equal(len(commit_by_stage), len(commits), "unique_commit_stages", "commits.jsonl")
    for stage in (1, 2, 3):
        record = commit_by_stage.get(stage, {})
        audit.equal(record.get("remote_sha"), EXPECTED_COMMITS[stage], "recorded_remote_commit", f"stage{stage}")
        audit.equal(record.get("sealed_utc"), seals[stage]["seal_utc"], "recorded_seal_time", f"stage{stage}")
        audit.equal(record.get("parent_sha"), seals[stage]["parent_remote_sha"], "commit_parent_matches_seal", f"stage{stage}")
        seal_relative_paths = {item["path"] for item in seals[stage]["files"]}
        seal_relative_paths.add({1: "evidence/seals/initial.json", 2: "evidence/seals/candidates.json", 3: "evidence/seals/behavior-followup.json"}[stage])
        audit.check(all(p.startswith("docs/workstreams/research/AF-RES-101/") or p in seal_relative_paths for p in record.get("changed_paths", [])), "commit_owned_path", f"stage{stage}")
        if record.get("remote_ref_verified_utc"):
            audit.check(timestamp(record["remote_ref_verified_utc"]) >= timestamp(record["sealed_utc"]), "remote_verification_after_seal", f"stage{stage}")
    audit.check(timestamp(seals[1]["seal_utc"]) < timestamp(seals[2]["seal_utc"]) < timestamp(seals[3]["seal_utc"]), "ordered_stage_seals", "seals")

    # Recruitment rows and first two eligible requests in each frozen stratum.
    audit.equal(len(initial), 8, "request_slot_count", "initial.csv")
    audit.equal(set(initial_by_id), set(CASE_IDS), "request_ids", "initial.csv")
    audit.equal(len({r["question_id"] for r in initial}), 8, "unique_selected_request_events", "initial.csv")
    audit.equal(len(frame), 87, "frame_count", "frame.csv")
    tag_counts = dict(Counter(r["tag"] for r in frame))
    audit.equal(tag_counts, {"imagemagick": 60, "typst": 27}, "frame_tag_counts", "frame.csv")
    audit.equal(len({r["question_id"] for r in frame}), len(frame), "no_cross_tag_duplicate_requests", "frame.csv")
    windows = {
        "2024-H1": (timestamp("2024-01-01T00:00:00Z"), timestamp("2024-06-30T23:59:59Z")),
        "2024-H2": (timestamp("2024-07-01T00:00:00Z"), timestamp("2024-12-31T23:59:59Z")),
    }
    audit.equal(sorted({r["window"] for r in frame}), ["2024-H1"], "extension_not_needed", "frame.csv")
    selected_rows = [r for r in frame if r["selected_slot"]]
    audit.equal({r["selected_slot"] for r in selected_rows}, set(CASE_IDS), "selected_frame_slots", "frame.csv")
    for tag in ("imagemagick", "typst"):
        tag_rows = [r for r in frame if r["tag"] == tag]
        sorted_rows = sorted(tag_rows, key=lambda r: (timestamp(r["created_utc"]), int(r["question_id"])))
        audit.equal([r["question_id"] for r in tag_rows], [r["question_id"] for r in sorted_rows], "creation_then_numeric_id_order", tag)
        audit.equal([int(r["frame_rank"]) for r in tag_rows], list(range(1, len(tag_rows) + 1)), "consecutive_frame_ranks", tag)
        for stratum in ("attempt", "unspecified"):
            eligible = [r for r in sorted_rows if r["stratum"] == stratum and truth(r["eligible"]) is True]
            selected = [r for r in sorted_rows if r["stratum"] == stratum and r["selected_slot"]]
            audit.equal([r["question_id"] for r in selected], [r["question_id"] for r in eligible[:2]], "first_two_eligible_in_stratum", f"{tag}/{stratum}")
    for row in frame:
        start, stop = windows[row["window"]]
        audit.check(start <= timestamp(row["created_utc"]) <= stop, "recruitment_window", row["question_id"])
        audit.check(bool(row["reason"]), "recruitment_disposition_reason", row["question_id"])
        if row["selected_slot"]:
            initial_row = initial_by_id[row["selected_slot"]]
            for key in ("question_id", "initial_revision_guid", "initial_body_sha256", "created_utc", "tag", "stratum", "frame_rank"):
                audit.equal(initial_row[key], row[key], "initial_frame_join", f"{row['selected_slot']}/{key}")
    for row in initial:
        audit.check(timestamp(row["judged_at_utc"]) <= timestamp(seals[1]["seal_utc"]), "initial_judgment_before_seal", row["case_id"])
        audit.check(all(row[k] for k in ("initial_revision_url", "initial_body_sha256", "purpose", "required_output", "source_id", "original_location")), "initial_required_fields", row["case_id"])

    # Re-run A/B from the independent identity fields, then verify frozen ranks.
    audit.equal(len(candidates), 24, "candidate_slot_count", "candidates.csv")
    audit.equal(set(candidate_by_id), expected_ids, "candidate_slot_ids", "candidates.csv")
    audit.equal(len(assessments), 24, "assessment_slot_count", "evidence/assessment.json")
    audit.equal(set(assessment_by_id), expected_ids, "assessment_slot_ids", "evidence/assessment.json")
    audit.equal(set(part_candidates), expected_ids, "agent_candidate_slot_ids", "candidate-part.json")
    actual = [r for r in candidates if truth(r["blank"]) is False]
    actual_ids = {r["candidate_id"] for r in actual}
    blank_ids = {r["candidate_id"] for r in candidates if truth(r["blank"]) is True}
    audit.equal(len(actual), 18, "actual_candidate_count", "candidates.csv")
    audit.equal(blank_ids, EXPECTED_BLANKS, "blank_slots", "candidates.csv")
    order_keys = {}
    for row in candidates:
        cid, case = row["candidate_id"], row["case_id"]
        part = part_candidates[cid]
        assessment = assessment_by_id[cid]
        audit.equal(row["question_id"], initial_by_id[case]["question_id"], "candidate_request_join", cid)
        audit.equal(int(row["original_rank"]), int(cid.rsplit("-C", 1)[1]), "candidate_rank_in_id", cid)
        audit.equal(truth(row["blank"]), bool(assessment["blank"]), "assessment_blank_consistency", cid)
        audit.equal(truth(row["blank"]), bool(part.get("blank")), "agent_candidate_blank_consistency", cid)
        audit.check(timestamp(row["judged_utc"]) <= timestamp(seals[2]["seal_utc"]), "candidate_judgment_before_seal", cid)
        for policy, field in (("A", "same_product_as_known_actual_use"), ("B", "same_operation_as_actual_attempt")):
            expected = "blank" if cid in blank_ids else ("exclude" if truth(row[field]) is True else "keep")
            audit.equal(row[policy + "_decision"], expected, "filter_from_independent_identity", f"{cid}/{policy}")
            audit.equal(assessment.get(policy + "_decision"), row[policy + "_decision"], "assessment_keeps_frozen_filter", f"{cid}/{policy}")
        if cid in blank_ids:
            audit.check(bool(row["blank_reason"]), "blank_reason", cid)
            audit.check(not row["first_proposal_utc"] and not row["operation"], "no_invented_blank_candidate", cid)
            continue
        proposal = timestamp(row["first_proposal_utc"])
        start = timestamp(initial_by_id[case]["created_utc"])
        audit.check(start <= proposal <= start + timedelta(days=30), "proposal_30_day_window", cid)
        audit.check(bool(row["product_identity_proof"]) and bool(row["operation_identity_proof"]), "separate_identity_evidence", cid)
        if case.startswith("TY"):
            key = part["ordering_key"]
            audit.equal(int(proposal.timestamp()), key[0], "proposal_order_timestamp", cid)
            audit.equal(row["operation"], part["operation"], "frozen_operation_join", cid)
            order_keys[cid] = key
        else:
            origins = json_cell(row, "origin_evidence", [])
            earliest = min(origins, key=lambda item: (timestamp(item["at_utc"]), item.get("comment_id") or item["post_id"]))
            audit.equal(proposal, timestamp(earliest["at_utc"]), "first_origin_time", cid)
            # The one equal-time/post tie in IM is pre2 versus pre3.  Retain the
            # original HTML location and extract its ordinal rather than sorting
            # on the already assigned candidate rank.
            location = earliest["body_location"]
            match = re.search(r"\bpre(\d+)\b", location)
            position = int(match.group(1)) if match else 0
            order_keys[cid] = [int(proposal.timestamp()), earliest.get("comment_id") or earliest["post_id"], position]
            audit.equal(row["operation"], part["operation"], "frozen_operation_join", cid)
    for case in CASE_IDS:
        case_ids = [r["candidate_id"] for r in actual if r["case_id"] == case]
        audit.equal(case_ids, sorted(case_ids, key=lambda cid: order_keys[cid]), "time_id_body_candidate_order", case)
        audit.equal(len({tuple(order_keys[cid]) for cid in case_ids}), len(case_ids), "distinct_candidate_order_keys", case)
    a_filter = filter_candidates(candidates, "A")
    b_filter = filter_candidates(candidates, "B")
    for policy, result in (("A", a_filter), ("B", b_filter)):
        for row in candidates:
            cid = row["candidate_id"]
            position = result["positions"].get(cid, {"returned_rank": None, "rank_shift": None})
            returned = optional_int(row[policy + "_returned_position"])
            audit.equal(returned, position["returned_rank"], "first_two_survivors", f"{cid}/{policy}")
            shift = optional_int(row[policy + "_rank_shift"])
            if position["returned_rank"] is not None or shift is not None:
                audit.equal(shift, position["rank_shift"], "recorded_rank_shift", f"{cid}/{policy}")
            elif cid not in blank_ids and row[policy + "_decision"] == "keep":
                # Typst records a shift only for returned positions. IM also
                # records surviving third-place shifts. Neither is exclusion.
                audit.check(position["survivor_rank"] > 2, "omitted_nonreturned_shift_only", f"{cid}/{policy}")
    audit.equal((a_filter["excluded_count"], a_filter["returned_count"]), (9, 7), "A_summary", "candidates.csv")
    audit.equal((b_filter["excluded_count"], b_filter["returned_count"]), (0, 14), "B_summary", "candidates.csv")
    b_only = set(b_filter["returned_ids"]) - set(a_filter["returned_ids"])
    a_only = set(a_filter["returned_ids"]) - set(b_filter["returned_ids"])
    audit.equal((len(b_only), len(a_only)), (7, 0), "exclusive_return_counts", "candidates.csv")

    # 90-day records and candidate-specific independent knowledge labels.
    audit.equal(len(followup), 8, "followup_request_count", "followup.csv")
    audit.equal({r["case_id"] for r in followup}, set(CASE_IDS), "followup_case_ids", "followup.csv")
    ground_truth = {}
    events = []
    for row in followup:
        case = row["case_id"]
        start = timestamp(initial_by_id[case]["created_utc"])
        stop = start + timedelta(days=90)
        audit.equal(timestamp(row["window_from_utc"]), start, "followup_window_start", case)
        audit.equal(timestamp(row["window_through_utc"]), stop, "followup_window_end", case)
        audit.equal(truth(row["acceptance_used_for_knowledge_or_execution"]), False, "acceptance_not_ground_truth", case)
        case_events = json_cell(row, "author_events", [])
        audit.equal(len(case_events), int(row["author_event_count"]), "followup_record_count", case)
        for event in case_events:
            event_time = timestamp(event["event_utc"])
            evidence = event.get("evidence", {})
            if isinstance(evidence, list):
                evidence = evidence[0] if evidence else {}
            event_url = event.get("url") or evidence.get("url")
            event_id = event.get("event_id") or f"{case}:{event['kind']}:{event_url}"
            targets = event.get("candidate_ids", event.get("targets", []))
            audit.check(start <= event_time <= stop, "followup_90_day_window", event_id)
            audit.check(bool(event_url), "followup_original_url", event_id)
            audit.check(set(targets) <= actual_ids, "followup_targets_are_actual_candidates", event_id)
            audit.check(all(cid.startswith(case + "-C") for cid in targets), "followup_targets_same_request", event_id)
            events.append({**event, "record_id": event_id, "case_id": case, "original_url": event_url, "targets_normalized": targets})
        for gt in json_cell(row, "candidate_ground_truth", []):
            cid = gt["candidate_id"]
            audit.check(cid not in ground_truth, "unique_candidate_ground_truth", cid)
            audit.check(cid.startswith(case + "-C"), "ground_truth_request_join", cid)
            ground_truth[cid] = gt
    audit.equal(set(ground_truth), actual_ids, "ground_truth_covers_actual_only", "followup.csv")
    audit.equal(len(events), 12, "followup_total_records", "followup.csv")
    audit.equal(len({e["record_id"] for e in events}), len(events), "unique_followup_records", "followup.csv")

    valid_ids, known_ids, newly_aware_ids = set(), set(), set()
    historical_ids, exact_execution_ids, reported_execution_ids = set(), set(), set()
    noneligible = []
    for cid in ordered_ids(actual_ids):
        assessment = assessment_by_id[cid]
        part = part_assessments[cid]
        row = candidate_by_id[cid]
        gt = ground_truth[cid]
        research_valid = (assessment.get("valid_output_operation_on_research_input") is True
                          and assessment.get("distinct_from_initial_actual_operation") is True
                          and supported(assessment.get("required_output_status")))
        audit.equal(assessment["research_valid_distinct_denominator_eligible"], research_valid, "research_eligibility_from_behavior_fields", cid)
        part_valid = (part.get("valid_output_operation_on_research_input") is True
                      and part.get("distinct_from_initial_actual_operation") is True
                      and supported(part.get("required_output_status")))
        audit.equal(research_valid, part_valid, "agent_official_flags_agree", cid)
        if cid.startswith("IM"):
            audit.equal(part.get("eligible_valid_alternative_denominator"), research_valid, "IM_agent_denominator_agrees", cid)
        if research_valid:
            valid_ids.add(cid)
            baseline = initial_by_id[row["case_id"]]
            audit.equal(baseline["stratum"], "attempt", "valid_loss_has_actual_baseline", cid)
            audit.check(bool(json_cell(baseline, "actual_used_products", [])) and bool(baseline["operation_attempted"]), "valid_loss_actual_use_evidence", cid)
            audit.equal(truth(row["same_operation_as_actual_attempt"]), False, "valid_loss_frozen_difference", cid)
            audit.check(all(supported(item["status"]) for item in assessment.get("hard_constraints", [])), "valid_loss_required_conditions_supported", cid)
        else:
            excluded = noneligible_reason(assessment)
            audit.check(excluded["reason_code"] != "unclassified", "noneligible_reason_classified", cid)
            audit.check(bool(excluded["reason"]), "noneligible_reason_evidence", cid)
            noneligible.append(excluded)
        known = gt.get("positive_independent_prior_knowledge_evidence") is True and gt.get("knowledge_denominator_eligible") is True
        audit.equal(assessment["full_candidate_prior_knowledge_denominator_eligible"], known, "prior_knowledge_independent_evidence_agrees", cid)
        if known:
            known_ids.add(cid)
        if supported(gt.get("explicit_new_awareness")):
            newly_aware_ids.add(cid)
        audit.equal(assessment["full_candidate_new_awareness"], gt["explicit_new_awareness"], "new_awareness_gt_agrees", cid)
        if supported(gt.get("execution_report")):
            reported_execution_ids.add(cid)
        if gt.get("exact_candidate_execution_verified") is True:
            exact_execution_ids.add(cid)
        if assessment.get("historical_original_input_and_version_verified") is True:
            historical_ids.add(cid)
        audit.check(cid.startswith(("IM-", "TY-")), "no_Q7_candidate_in_denominators", cid)
    audit.equal(valid_ids, EXPECTED_VALID, "research_valid_distinct_ids", "assessment.json")
    audit.equal(len(noneligible), 15, "noneligible_comparison_count", "assessment.json")
    audit.equal(known_ids, set(), "full_candidate_prior_knowledge_count", "followup.csv")
    audit.check(all(unknown(ground_truth[cid].get("already_knew_before_proposal")) for cid in actual_ids), "full_candidate_prior_knowledge_unknown", "followup.csv")
    audit.equal(newly_aware_ids, set(), "explicit_new_awareness_count", "followup.csv")
    audit.check(all(unknown(ground_truth[cid].get("explicit_new_awareness")) for cid in actual_ids), "newness_unknown_not_negative", "followup.csv")
    audit.equal(historical_ids, set(), "historical_original_replay_count", "assessment.json")
    audit.equal(exact_execution_ids, set(), "exact_OP_execution_count", "followup.csv")
    audit.equal(reported_execution_ids, {"IM-A1-C1"}, "modified_OP_report_candidate", "followup.csv")

    # Deduplicate only the two evidence-linked records of this failed episode.
    execution_records = [e for e in events if "execution_report" in e.get("codes", []) or supported(e.get("execution_report"))]
    audit.equal({e["record_id"] for e in execution_records}, MODIFIED_EPISODE_RECORDS, "execution_episode_record_links", "followup.csv")
    audit.check(all("failure_reported" in e.get("codes", []) for e in execution_records), "execution_records_report_failure", "IM-A1-C1")
    audit.check(any("candidate_modified" in e.get("codes", []) for e in execution_records), "modified_code_marker_present", "IM-A1-C1")
    audit.check(all(e["targets_normalized"] == ["IM-A1-C1"] for e in execution_records), "execution_records_same_candidate", "IM-A1-C1")
    for event in execution_records:
        audit.check(timestamp(event["event_utc"]) >= timestamp(candidate_by_id["IM-A1-C1"]["first_proposal_utc"]), "execution_after_proposal", event["record_id"])
    modified_episodes = []
    if {e["record_id"] for e in execution_records} == MODIFIED_EPISODE_RECORDS:
        modified_episodes.append({
            "episode_id": "IM-A1-C1-modified-failure-2024-01-07",
            "candidate_id": "IM-A1-C1",
            "record_ids": sorted(MODIFIED_EPISODE_RECORDS),
            "record_urls": [e["original_url"] for e in sorted(execution_records, key=lambda e: e["event_utc"])],
            "record_count": len(execution_records),
            "execution_report": "supported_modified_candidate",
            "outcome": "reported_failure",
            "exact_frozen_candidate_execution": "미확인",
            "linkage_basis": "The comment refers to the error inserted in question revision 2; that revision comments out alpha(off). One linked episode, not two trials.",
        })
    success_records = [e["record_id"] for e in events if "execution_success" in e.get("codes", []) or e.get("successful_execution_verified") is True]
    audit.equal(success_records, [], "no_explicit_success_record", "followup.csv")

    # Count independently read unique source files/events, excluding mirrors,
    # other anchors, repeated revisions and paired expected-image duplicates.
    source_ids = [s["source_id"] for s in sources]
    audit.equal(len(source_ids), len(set(source_ids)), "unique_ledger_source_ids", "sources.jsonl")
    counted = [s for s in sources if s.get("counted") is True]
    groups = dict(Counter(source_group(s) for s in counted))
    counted_ids = [s["source_id"] for s in counted]
    audit.equal(len(sources), source_counts["ledger_rows"], "ledger_row_count_receipt", "source-counts.json")
    audit.equal(len(counted), source_counts["counted_unique"], "unique_source_count_receipt", "source-counts.json")
    audit.equal(set(counted_ids), set(source_counts["counted_ids"]), "source_id_count_receipt", "source-counts.json")
    audit.equal(groups, source_counts["groups"], "source_group_count_receipt", "source-counts.json")
    core = len(counted) - groups.get("supplemental_primary", 0)
    audit.equal(core, source_counts["mandatory_core_unique"], "mandatory_core_count_receipt", "source-counts.json")
    audit.equal((len(counted), core), (35, 29), "research_source_totals", "sources.jsonl")
    audit.check(len(counted) >= 24 and core >= 24, "source_total_minimum", "sources.jsonl")
    audit.equal(groups.get("selected_requests"), 8, "eight_distinct_request_sources", "sources.jsonl")
    audit.check(groups.get("imagemagick_documents_implementations", 0) >= 3, "IM_document_minimum", "sources.jsonl")
    audit.check(groups.get("typst_documents_implementations", 0) >= 3, "TY_document_minimum", "sources.jsonl")
    audit.check(groups.get("imagemagick_documents_implementations", 0) + groups.get("typst_documents_implementations", 0) >= 8, "combined_document_minimum", "sources.jsonl")
    audit.check(groups.get("imagemagick_upstream_tests", 0) + groups.get("typst_upstream_input_expected_bundles", 0) >= 4, "upstream_test_bundle_minimum", "sources.jsonl")
    audit.equal({s["source_id"] for s in counted if s.get("category") == "selected_request"}, {r["source_id"] for r in initial}, "selected_source_initial_join", "sources.jsonl")
    audit.equal({s["source_id"] for s in counted if s.get("category") == "cross_domain_official"}, {"CD-GIT-MAN", "CD-GIT-TEST", "CD-FFMPEG-MAN", "CD-FFMPEG-FATE"}, "Git_FFmpeg_two_sources_each", "sources.jsonl")
    canonical_urls = [canonical_source_url(s["fixed_url"]) for s in counted]
    audit.equal(len(canonical_urls), len(set(canonical_urls)), "no_counted_anchor_or_mirror_duplicates", "sources.jsonl")
    for source in counted:
        sid = source["source_id"]
        fields = ("direct_open_url", "fixed_url", "checked_at_utc", "author_publisher", "lineage", "version_section_locator", "fingerprint", "observed", "limits_unknown")
        audit.check(all(source.get(k) for k in fields), "counted_source_traceability_fields", sid)
        timestamp(source["checked_at_utc"])
        audit.check(source_group(source) != "unclassified", "counted_source_group", sid)
        audit.check(bool(re.search(r"\b[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?\b", json.dumps(source["fingerprint"]))), "counted_source_fingerprint", sid)
    for assessment in assessments:
        audit.check(set(assessment.get("source_ids", [])) <= set(source_ids), "assessment_source_ids_exist", assessment["candidate_id"])

    # Independent metrics: none substitutes for another.
    attempted_same_ids = {cid for cid in actual_ids if truth(candidate_by_id[cid]["same_operation_as_actual_attempt"]) is True}
    rerecommended_ids = known_ids | attempted_same_ids
    known_metric = metric(known_ids, a_filter["returned_ids"], b_filter["returned_ids"], comparison="actually_returned")
    known_metric.update({"unknown_count": len(actual_ids - known_ids), "unknown_ids": ordered_ids(actual_ids - known_ids)})
    rerecommendation = metric(rerecommended_ids, a_filter["excluded_ids"], b_filter["excluded_ids"])
    rerecommendation.update({"unknown_count": len(actual_ids - rerecommended_ids), "unknown_ids": ordered_ids(actual_ids - rerecommended_ids)})
    valid_metric = metric(valid_ids, a_filter["excluded_ids"], b_filter["excluded_ids"])
    valid_metric.update({
        "scope": "Fixed research release and labeled research inputs. Original required output and constraints supported; different from the earliest actual operation. Not historical author success or novelty.",
        "comparison_ineligible_count": len(noneligible),
        "comparison_ineligible_ids": [r["candidate_id"] for r in noneligible],
        "comparison_ineligible_reasons": noneligible,
        "comparison_ineligible_reason_counts": dict(sorted(Counter(r["reason_code"] for r in noneligible).items())),
    })

    # Literal sensitivity: the first comment's short example omits minus.
    adapted_ids = {cid for cid in valid_ids if assessment_by_id[cid].get("validity") == "supported_operation_with_mode_label_correction"}
    audit.equal(adapted_ids, {"TY-A2-C2"}, "literal_sensitivity_adapted_candidate", "assessment.json")
    strict_ids = valid_ids - adapted_ids
    strict_metric = metric(strict_ids, a_filter["excluded_ids"], b_filter["excluded_ids"])
    strict_metric.update({"removed_ids": ordered_ids(adapted_ids), "reason": "The first comment renders s_2 without superscript minus. Applying #red to the original expression is a separate researcher fixture, not evidence that the literal first example preserved it.", "receipt": "evidence/typst-official/run-receipt.json", "run_ids": ["a2-c2-exact", "a2-c2-original-expression"]})
    audit.equal((strict_metric["denominator"], strict_metric["A"]["numerator"], strict_metric["B"]["numerator"]), (2, 2, 0), "literal_sensitivity_counts", "assessment.json")

    # Merge only the proposed perspective pair; no replacement search or fill.
    merge_omitted = {"IM-U2-C2"}
    merge_a = filter_candidates(candidates, "A", omitted=merge_omitted)
    merge_b = filter_candidates(candidates, "B", omitted=merge_omitted)
    audit.equal((len(actual_ids - merge_omitted), merge_a["returned_count"], merge_b["returned_count"]), (17, 6, 13), "perspective_merge_sensitivity", "candidates.csv")
    audit.check(all(part_candidates[cid].get("duplicated_relation") for cid in ("IM-U2-C1", "IM-U2-C2")), "perspective_merge_has_frozen_caution", "IM-U2")

    # Change only the disputed RMagick wrapper boundary; other decisions fixed.
    wrapper_candidate = "IM-A1-C2"
    wrapper_a = filter_candidates(candidates, "A", decision_overrides={wrapper_candidate: "keep"})
    audit.equal(candidate_by_id[wrapper_candidate]["wrapper_name"], "RMagick", "wrapper_sensitivity_identity", wrapper_candidate)
    actual_products = json_cell(initial_by_id["IM-A1"], "actual_used_products", [])
    audit.check(all("rmagick" not in product.lower() for product in actual_products), "RMagick_not_baseline_actual_wrapper", "IM-A1")
    audit.check(bool(part_candidates[wrapper_candidate].get("product_identity_sensitivity")), "wrapper_sensitivity_frozen_evidence", wrapper_candidate)
    audit.equal((wrapper_a["returned_count"], b_filter["returned_count"]), (8, 14), "wrapper_boundary_return_counts", "candidates.csv")
    audit.equal(set(wrapper_a["returned_ids"]) - set(a_filter["returned_ids"]), {wrapper_candidate}, "only_C2_changes_wrapper_return", "candidates.csv")

    # Known CLI core is not the whole Ruby/Open3 proposal and remains rank 3.
    known_core_ids = {cid for cid in actual_ids if assessment_by_id[cid].get("known_core_sensitivity", {}).get("eligible") is True}
    audit.equal(known_core_ids, {"IM-A1-C3"}, "known_core_sensitivity_ids", "assessment.json")
    audit.check(all(ground_truth[cid].get("partial_core_familiarity") is True for cid in known_core_ids), "known_core_followup_agrees", "followup.csv")
    known_core_removal = metric(known_core_ids, a_filter["excluded_ids"], b_filter["excluded_ids"], unit="core operation only")
    known_core_return = metric(known_core_ids, a_filter["returned_ids"], b_filter["returned_ids"], unit="core operation only", comparison="actually_returned")
    audit.equal((known_core_removal["denominator"], known_core_removal["A"]["numerator"], known_core_removal["B"]["numerator"], known_core_return["A"]["numerator"], known_core_return["B"]["numerator"]), (1, 1, 0, 0, 0), "known_core_counts", "assessment.json")

    return {
        "schema_version": 1,
        "task_id": "AF-RES-101",
        "scope": "Local arithmetic/consistency verification of committed research evidence. No new source reads, user trials, network calls or Q7 observations enter the main denominators.",
        "counts": {"requests": len(initial), "frame": len(frame), "frame_by_tag": tag_counts, "candidate_slots": len(candidates), "actual_candidates": len(actual), "blank_slots": len(blank_ids), "blank_ids": ordered_ids(blank_ids), "followup_records": len(events)},
        "sealed_filter_results": {"A": a_filter, "B": b_filter, "B_only_returned_count": len(b_only), "B_only_returned_ids": ordered_ids(b_only), "A_only_returned_count": len(a_only), "A_only_returned_ids": ordered_ids(a_only), "original_order_keys": order_keys, "rank_shift_convention": "original_rank minus survivor_rank; Typst's frozen blank shift for nonreturned third survivors remains a missing display value, not exclusion"},
        "independent_denominators": {
            "rerecommendation_removed": rerecommendation,
            "different_valid_operation_loss_research_scope": valid_metric,
            "already_known_full_method_actually_returned": known_metric,
        },
        "awareness": {
            "observed_candidate_ids": ordered_ids(actual_ids), "observed_candidate_count": len(actual_ids),
            "explicit_new_evidence_count": len(newly_aware_ids), "explicit_new_evidence_ids": ordered_ids(newly_aware_ids),
            "newness_unknown_count": len(actual_ids - newly_aware_ids), "newness_unknown_ids": ordered_ids(actual_ids - newly_aware_ids),
            "newness_rate": None, "rate_status": "산출 불가", "interpretation": "0 explicit positive records among 18 inspected candidates is not 0% learning and not 18 known-negative labels.",
        },
        "author_execution": {
            "reported_candidate_ids": ordered_ids(reported_execution_ids), "reported_candidate_count": len(reported_execution_ids),
            "modified_failure_episode_count": len(modified_episodes), "modified_failure_record_count": len(execution_records), "modified_failure_episodes": modified_episodes,
            "execution_report_unknown_count": len(actual_ids - reported_execution_ids), "execution_report_unknown_ids": ordered_ids(actual_ids - reported_execution_ids),
            "exact_frozen_candidate_execution_count": len(exact_execution_ids), "exact_frozen_candidate_execution_ids": ordered_ids(exact_execution_ids),
            "exact_execution_unknown_count": len(actual_ids - exact_execution_ids), "exact_execution_unknown_ids": ordered_ids(actual_ids - exact_execution_ids),
            "explicit_success_record_count": len(success_records), "explicit_success_record_ids": success_records,
            "success_rate": None, "rate_status": "산출 불가", "interpretation": "One modified-code failure report; no success observation. No researcher run is counted as an author run.",
        },
        "additional_historical_replay_layer": {
            "verified_count": len(historical_ids), "verified_ids": ordered_ids(historical_ids),
            "unknown_count": len(actual_ids - historical_ids), "unknown_ids": ordered_ids(actual_ids - historical_ids),
            "historical_valid_loss": metric(valid_ids & historical_ids, a_filter["excluded_ids"], b_filter["excluded_ids"]),
            "scope": "Original author version and original input jointly verified. Additional layer, not a retroactive redefinition of the research-operation denominator. Known literal/reference counterevidence is retained separately.",
        },
        "sensitivities": {
            "strict_literal_preserves_original_expression": strict_metric,
            "merge_IM_U2_perspective_pair": {"merged_into": "IM-U2-C1", "merged_away_ids": sorted(merge_omitted), "effective_actual_count": len(actual_ids - merge_omitted), "effective_actual_ids": ordered_ids(actual_ids - merge_omitted), "original_blank_count": len(blank_ids), "empty_or_merged_slot_count": len(blank_ids | merge_omitted), "A": merge_a, "B": merge_b, "scope": "Sensitivity only: missing sign/bounds prevent asserting identical operations in the main frozen table. No external replacement."},
            "RMagick_wrapper_boundary_only": {"changed_identity_candidate_ids": [wrapper_candidate], "A": wrapper_a, "B_returned_count": b_filter["returned_count"], "B_returned_ids": b_filter["returned_ids"], "scope": "Only IM-A1-C2 switches from engine-level match to distinct wrapper not actually used in the initial body. All other frozen decisions remain fixed."},
            "known_core_not_whole_candidate": {"removal": known_core_removal, "actual_return": known_core_return, "B_surviving_ids": ordered_ids(known_core_ids & set(b_filter["surviving_ids"])), "B_nonreturned_ids": ordered_ids(known_core_ids - set(b_filter["returned_ids"])), "scope": "Already quoted grouped CLI only. Open3/Shellwords familiarity unknown. Never merged into the full-candidate denominator."},
        },
        "source_counts": {"ledger_rows": len(sources), "counted_unique": len(counted), "mandatory_core_unique": core, "groups": groups, "counted_ids": counted_ids, "counted_source_canonical_urls": canonical_urls, "minimum_checks": {"unique_primary_at_least_24": len(counted) >= 24, "selected_requests_8": groups.get("selected_requests") == 8, "IM_documents_at_least_3": groups.get("imagemagick_documents_implementations", 0) >= 3, "TY_documents_at_least_3": groups.get("typst_documents_implementations", 0) >= 3, "documents_combined_at_least_8": groups.get("imagemagick_documents_implementations", 0) + groups.get("typst_documents_implementations", 0) >= 8, "upstream_bundles_combined_at_least_4": groups.get("imagemagick_upstream_tests", 0) + groups.get("typst_upstream_input_expected_bundles", 0) >= 4, "Git_and_FFmpeg_each_manual_and_test": groups.get("cross_domain_official_manual_tests") == 4}},
        "cross_domain": {"source_ids": ["CD-GIT-MAN", "CD-GIT-TEST", "CD-FFMPEG-MAN", "CD-FFMPEG-FATE"], "included_in_main_candidate_denominator": False, "role": "Q7 auxiliary operation-identity calibration only"},
        "seal_verification": {"checks": seal_checks, "recorded_commits": [{k: row.get(k) for k in ("stage", "remote_sha", "parent_sha", "sealed_utc", "remote_ref_verified_utc")} for row in normalized_commits], "scope": "Local recorded seal/prefix checks. Recorded remote verification is not a fresh GitHub read by this script."},
    }


def main():
    audit = Audit()
    report = {}
    if len(sys.argv) != 1:
        audit.check(False, "unexpected_arguments", "command_line", "no arguments", sys.argv[1:])
    try:
        report = run(audit)
    except Exception as error:
        audit.check(False, "unhandled_input_or_schema_error", "recalculate.py", "valid frozen input schema", f"{type(error).__name__}: {error}")
    report.update({
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "command": "python -B docs/workstreams/research/AF-RES-101/recalculate.py",
        "script_sha256": sha256(Path(__file__).read_bytes()),
        "input_fingerprints": audit.inputs,
        "validation_check_count": audit.checks,
        "validation_errors": audit.errors,
        "exit_code": 1 if audit.errors else 0,
        "determinism": "With unchanged input bytes and script, only generated_utc changes on repeated runs.",
    })
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT.relative_to(BASE)), "validation_checks": audit.checks, "validation_error_count": len(audit.errors), "exit_code": report["exit_code"], "counts": report.get("counts"), "source_counts": {k: report.get("source_counts", {}).get(k) for k in ("counted_unique", "mandatory_core_unique")}}, ensure_ascii=False))
    if audit.errors:
        print(json.dumps(audit.errors, ensure_ascii=False, indent=2), file=sys.stderr)
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
