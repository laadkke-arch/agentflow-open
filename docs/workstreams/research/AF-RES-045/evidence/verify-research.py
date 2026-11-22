#!/usr/bin/env python3
"""Offline AF-RES-045 schema, seal, source-quota and arithmetic verification.

Run from the repository root:
    python -B docs/workstreams/research/AF-RES-045/evidence/verify-research.py
    python -B docs/workstreams/research/AF-RES-045/evidence/verify-research.py \
      --output docs/workstreams/research/AF-RES-045/evidence/verification.json

Stdlib only; no network, downloads, Git mutations, or outcome interpretation.
Inputs are read once. Requests/predictions/SCOPE/frame must match the seal;
sources/amendments may be appended. UTC is the only intentionally varying output.
Exit 0: structural checks and source quotas pass. Exit 1: quotas incomplete.
Exit 2: malformed input or structural/seal violation. An absent outcomes.csv is
reported as pending; --require-outcomes makes its absence a structural failure.
Outcome support counts are declared-field counts, never inferred from prose.
The reviewer is a same-model separate-context agent, not an external assessor.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import sys

OWNED = Path(__file__).resolve().parent.parent
SEALED_FILES = ("requests.csv", "predictions.csv", "SCOPE.md", "frame.csv")
EXPECTED_CASES = {"M01", "M02", "M03", "AUD01", "AUD02", "AUD03"}
ALLOCATION_MAP = {
    "consumer_requests": "consumer_requests",
    "donor_spatial": "donor_spatial",
    "donor_temporal": "donor_temporal",
    "donor_other": "donor_other",
    "comparison": "independent_comparison",
    "independent_comparison": "independent_comparison",
    "receiver_followup": "receiver_followup",
    # Exposed legacy alias; parent canonical integration uses receiver_followup.
    "followup": "receiver_followup",
}
RELATION_GROUP = {
    "different_conditional": "different",
    "different": "different",
    "different_model": "different",
    "same_conditional": "same",
    "same": "same",
    "underdetermined": "underdetermined",
}
OUTCOME_BOOLEAN_FIELDS = (
    "matched_normal", "matched_boundary", "strict_pair_denominator_member",
    "unique_support", "both_rejected",
)


def utc(value):
    """Parse a recorded timestamp; require an explicit timezone."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing timestamp")
    result = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp lacks timezone")
    return result.astimezone(timezone.utc)


def duplicate_values(values):
    return sorted(str(k) for k, n in Counter(values).items() if n > 1)


def csv_bool(value):
    """Frame uses True/False; outcome booleans are separately checked lowercase."""
    if value in ("true", "True"):
        return True
    if value in ("false", "False"):
        return False
    raise ValueError("not a true/false CSV value: " + repr(value))


def counter_dict(values):
    return dict(sorted(Counter(str(v) for v in values).items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="JSON file inside this owned path; otherwise stdout")
    parser.add_argument("--require-outcomes", action="store_true")
    args = parser.parse_args()
    checks = []
    warnings = []
    cache = {}
    result = {
        "verifier": "AF-RES-045 offline arithmetic/schema verifier v1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "owned_path": str(OWNED),
        "review_type": "same-model separate-context; not external independent review",
        "interpretation_limit": "No support or strict eligibility is inferred from source/outcome prose.",
    }

    def check(name, passed, observed=None, expected=None, kind="structural"):
        item = {"check": name, "passed": bool(passed), "kind": kind}
        if observed is not None:
            item["observed"] = observed
        if expected is not None:
            item["expected"] = expected
        checks.append(item)
        return bool(passed)

    def read_bytes(name):
        if name not in cache:
            cache[name] = (OWNED / name).read_bytes()
        return cache[name]

    def read_json(name):
        return json.loads(read_bytes(name).decode("utf-8"))

    def read_csv(name, required):
        reader = csv.DictReader(io.StringIO(read_bytes(name).decode("utf-8-sig")))
        fields = reader.fieldnames or []
        rows = list(reader)
        check(name + ":required_columns", set(required) <= set(fields),
              sorted(set(required) - set(fields)), "no missing columns")
        check(name + ":unique_header", len(fields) == len(set(fields)), fields)
        check(name + ":well_formed_rows", all(None not in row and None not in row.values() for row in rows))
        return rows, fields

    try:
        seal = read_json("evidence/prediction-seal.json")
        receipt = read_json("evidence/reveal-receipt.json") if (OWNED / "evidence/reveal-receipt.json").exists() else {}
        seal_time_text = receipt.get("seal_committed_at") or seal.get("created_utc")
        seal_time = utc(seal_time_text)
        result["seal"] = {
            "commit": receipt.get("seal_sha"), "comparison_timestamp": seal_time_text,
            "timestamp_basis": "commit receipt" if receipt.get("seal_committed_at") else "seal JSON creation only",
            "remote_text_equality_declared_in_receipt": receipt.get("verified_remote_prediction_text_equal"),
            "early_exposures_original_strings": seal.get("early_exposures", []),
            "protected_files": list(SEALED_FILES),
            "append_allowed_not_hash_enforced": ["sources.jsonl", "amendments.md"],
        }
        hash_checks = {}
        for name in SEALED_FILES:
            actual = hashlib.sha256(read_bytes(name)).hexdigest()
            expected = seal.get("files", {}).get(name)
            hash_checks[name] = {"expected": expected, "actual": actual, "matches": actual == expected}
            check("sealed_hash:" + name, actual == expected, actual, expected)
        result["protected_hashes"] = hash_checks

        requests, request_fields = read_csv("requests.csv", (
            "request_id", "source_id", "normal_input", "boundary_input",
            "prior_outcome_exposure", "cross_case_exposure",
        ))
        predictions, prediction_fields = read_csv("predictions.csv", (
            "prediction_id", "request_id", "candidate_id", "donor_source_ids",
            "preferred_choice", "normal_prediction", "boundary_prediction",
            "preseal_pair_relation", "phase",
        ))
        frame, frame_fields = read_csv("frame.csv", (
            "frame_id", "repository", "exposure_rank", "issue_number", "title",
            "created_at", "url", "selected", "request_id",
        ))
        sources = [json.loads(line) for line in read_bytes("sources.jsonl").decode("utf-8").splitlines() if line.strip()]
        result["schemas"] = {"requests.csv": request_fields, "predictions.csv": prediction_fields,
                             "frame.csv": frame_fields, "sources.jsonl_union": sorted({k for row in sources for k in row})}
        for name, rows, key, expected_count in (
            ("requests", requests, "request_id", 6),
            ("predictions", predictions, "prediction_id", 12),
            ("frame", frame, "frame_id", 60),
        ):
            ids = [row.get(key, "") for row in rows]
            check(name + ":count", len(rows) == expected_count, len(rows), expected_count)
            check(name + ":nonempty_unique_ids", all(ids) and len(ids) == len(set(ids)), duplicate_values(ids))
        request_ids = {row["request_id"] for row in requests}
        check("requests:expected_case_ids", request_ids == EXPECTED_CASES, sorted(request_ids), sorted(EXPECTED_CASES))
        req_by_id = {row["request_id"]: row for row in requests}
        pred_by_id = {row["prediction_id"]: row for row in predictions}
        pred_by_request = defaultdict(list)
        for row in predictions:
            pred_by_request[row["request_id"]].append(row)
        check("predictions:request_references", set(pred_by_request) == request_ids, sorted(pred_by_request), sorted(request_ids))
        check("predictions:two_candidates_each", all(len(pred_by_request[k]) == 2 and {p["candidate_id"] for p in pred_by_request[k]} == {"P1", "P2"} for k in request_ids))
        check("predictions:required_text_populated", all(all(row.get(k, "").strip() for k in ("donor_source_ids", "normal_prediction", "boundary_prediction", "preseal_pair_relation")) for row in predictions))
        check("predictions:sealed_phase", {row["phase"] for row in predictions} == {"sealed_before_outcomes"}, sorted({row["phase"] for row in predictions}))

        grouped_frame = defaultdict(list)
        for row in frame:
            grouped_frame[row["repository"]].append(row)
        expected_repositories = {"matplotlib/matplotlib": "layout", "audacity/audacity": "selection"}
        check("frame:two_repositories", set(grouped_frame) == set(expected_repositories), sorted(grouped_frame))
        frame_summary = {}
        for repository, keyword in expected_repositories.items():
            rows = grouped_frame[repository]
            ranks = [int(row["exposure_rank"]) for row in rows]
            chronological = [(utc(row["created_at"]), int(row["issue_number"])) for row in rows]
            check("frame:" + repository + ":30_ranks", ranks == list(range(1, 31)), ranks, list(range(1, 31)))
            check("frame:" + repository + ":created_then_issue_order", chronological == sorted(chronological))
            check("frame:" + repository + ":2019_to_2024", all(2019 <= dt.year <= 2024 for dt, _ in chronological))
            check("frame:" + repository + ":current_title_keyword", all(keyword in row["title"].lower() for row in rows))
            check("frame:" + repository + ":unique_issues", len(rows) == len({row["issue_number"] for row in rows}))
            selected = [row for row in rows if csv_bool(row["selected"])]
            check("frame:" + repository + ":selected3", len(selected) == 3, len(selected), 3)
            frame_summary[repository] = {"rows": len(rows), "selected_request_ids": [row["request_id"] for row in selected],
                                         "selected_issue_numbers": [row["issue_number"] for row in selected]}
        selected_ids = [row["request_id"] for row in frame if csv_bool(row["selected"])]
        check("frame:selected_request_join", len(selected_ids) == 6 and set(selected_ids) == request_ids, selected_ids)
        result["frame"] = {"by_repository": frame_summary,
                           "scope": "Current-title exposure ordered by creation timestamp and issue number; this does not reconstruct titles at creation or validate qualitative eligibility."}

        source_ids = [row.get("source_id") for row in sources]
        check("sources:nonempty_unique_ids", all(source_ids) and len(source_ids) == len(set(source_ids)), duplicate_values(source_ids))
        check("sources:minimum_count_boolean", all(type(row.get("minimum_count")) is bool for row in sources))
        source_by_id = {row.get("source_id"): row for row in sources}
        counted = [row for row in sources if row.get("minimum_count") is True]
        work_ids = [row.get("work_id") for row in counted]
        check("sources:counted_work_ids_present_unique", all(work_ids) and len(work_ids) == len(set(work_ids)), duplicate_values(work_ids))
        check("sources:counted_duplicate_of_empty", not any(row.get("duplicate_of") for row in counted), [row.get("source_id") for row in counted if row.get("duplicate_of")])
        check("sources:counted_allocation_known", all(row.get("allocation") in ALLOCATION_MAP for row in counted), sorted({str(row.get("allocation")) for row in counted if row.get("allocation") not in ALLOCATION_MAP}))
        grouped_works = defaultdict(set)
        for row in counted:
            if row.get("work_id"):
                grouped_works[ALLOCATION_MAP.get(row.get("allocation"), "UNKNOWN:" + str(row.get("allocation")))].add(row["work_id"])
        allocation_counts = {key: len(value) for key, value in sorted(grouped_works.items())}
        all_donor_works = set().union(*(grouped_works[k] for k in ("donor_spatial", "donor_temporal", "donor_other")))
        unique_counted_works = {x for x in work_ids if x}
        quotas = {
            "consumer_requests": (len(grouped_works["consumer_requests"]), 6, "exact"),
            "donor_spatial": (len(grouped_works["donor_spatial"]), 3, "minimum"),
            "donor_temporal": (len(grouped_works["donor_temporal"]), 3, "minimum"),
            "donor_total": (len(all_donor_works), 8, "minimum"),
            "receiver_followup": (len(grouped_works["receiver_followup"]), 6, "minimum"),
            "independent_comparison": (len(grouped_works["independent_comparison"]), 4, "minimum"),
            "all_unique_primary": (len(unique_counted_works), 24, "minimum"),
        }
        for name, (actual, required, operator) in quotas.items():
            check("quota:" + name, actual == required if operator == "exact" else actual >= required,
                  actual, {"operator": operator, "count": required}, kind="quota")
        referenced_source_ids = {row["source_id"] for row in requests}
        referenced_source_ids.update(part.strip() for row in predictions for part in row["donor_source_ids"].split(";") if part.strip())
        missing_source_ids = sorted(referenced_source_ids - set(source_by_id))
        check("sources:sealed_request_and_donor_references", not missing_source_ids, missing_source_ids)
        referenced_time_results = {}
        for source_id in sorted(referenced_source_ids & set(source_by_id)):
            row = source_by_id[source_id]
            recorded = row.get("checked_utc") or row.get("accessed_utc")
            try:
                parsed = utc(recorded)
                referenced_time_results[source_id] = {"checked_utc": recorded, "before_seal": parsed < seal_time}
            except ValueError:
                referenced_time_results[source_id] = {"checked_utc": recorded, "before_seal": None, "error": "timestamp missing or non-ISO/timezone absent"}
        check("sources:sealed_references_read_before_seal", all(item["before_seal"] is True for item in referenced_time_results.values()) and not missing_source_ids)
        result["sources"] = {
            "records": len(sources), "counted_records": len(counted), "counted_unique_works": len(unique_counted_works),
            "uncounted_records": len(sources) - len(counted),
            "raw_counted_allocation_record_counts": counter_dict(row.get("allocation") for row in counted),
            "normalized_counted_allocation_unique_work_counts": allocation_counts,
            "normalization_map": ALLOCATION_MAP,
            "quotas": {name: {"observed": actual, "required": required, "operator": operator} for name, (actual, required, operator) in quotas.items()},
            "sealed_reference_read_timestamps": referenced_time_results,
            "temporal_boundary_work_ids_from_method_review": [source_by_id[sid]["work_id"] for sid in ("TD01", "TD02", "TD03") if sid in source_by_id and source_by_id[sid].get("minimum_count") is True],
            "domain_limit": "TD04 is film color masking, not a fourth time-boundary work. Different publishers do not by themselves establish different domains. Allocation checks do not prove historical availability or same-input evidence.",
        }

        relations = {}
        for case, rows in sorted(pred_by_request.items()):
            values = {row["preseal_pair_relation"] for row in rows}
            check("pair_relation:" + case + ":consistent", len(values) == 1, sorted(values))
            relations[case] = sorted(values)[0] if len(values) == 1 else "INCONSISTENT"
        check("pair_relations:known_strings", all(value in RELATION_GROUP for value in relations.values()), relations)
        explicit_exposure = {case for case, row in req_by_id.items() if row.get("prior_outcome_exposure", "").startswith("있음:")}
        cross_case = {case for case, row in req_by_id.items() if row.get("cross_case_exposure", "").strip()}
        current_only_ids = {"TD03", "TD04", "TD04b"}
        current_only_cases = {row["request_id"] for row in predictions if set(part.strip() for part in row["donor_source_ids"].split(";")) & current_only_ids}

        def population(name, removed):
            retained = sorted(request_ids - removed)
            groups = Counter(RELATION_GROUP.get(relations.get(case), "unknown") for case in retained)
            return {"name": name, "removed_case_ids": sorted(removed), "retained_case_ids": retained,
                    "case_count": len(retained), "original_relation_counts": counter_dict(relations.get(case) for case in retained),
                    "broad_group_counts": {key: groups[key] for key in ("different", "same", "underdetermined", "unknown")},
                    "support_rate": None, "support_rate_reason": "This is a sealed-prediction population count, not an observed support denominator."}
        result["sealed_pair_classification"] = {"relations_original_strings": relations,
            "case_counts": counter_dict(relations.values()), "row_counts": counter_dict(row["preseal_pair_relation"] for row in predictions)}
        result["sensitivity_populations"] = [
            population("all sealed slots", set()),
            population("exclude explicit preseal outcome exposure", explicit_exposure),
            population("also exclude cross-case postrequest-source exposure", explicit_exposure | cross_case),
            population("exclude pairs using known current-only donor editions", current_only_cases),
        ]
        result["sensitivity_basis"] = {
            "exposure_original_strings": {case: req_by_id[case]["prior_outcome_exposure"] for case in sorted(explicit_exposure)},
            "cross_case_original_strings": {case: req_by_id[case]["cross_case_exposure"] for case in sorted(cross_case)},
            "known_current_only_source_ids_from_method_review": sorted(current_only_ids),
            "historical_limit": "Excluding those IDs does not certify the historical public editions of all remaining sources.",
        }

        m01p2 = pred_by_id.get("M01-P2", {})
        result["m01_semantic_warning"] = {
            "preferred_choice_original": m01p2.get("preferred_choice"),
            "boundary_prediction_original": m01p2.get("boundary_prediction"),
            "flag": "Different intervention choices are not opposite success predictions.",
            "reason": "M01-P2 already predicts that whole-raster scaling fails to repair internal bbox/aspect differences. Its B label is explicitly a near-miss hypothesis. Do not infer a uniquely rejected candidate solely because B fails or promote qualitative operator agreement into the strict denominator.",
            "original_relation_preserved": relations.get("M01"),
        }
        warnings.append("M01: different_conditional is preserved; P2 already anticipates failure of scaling internal geometry.")

        outcome_path = OWNED / "outcomes.csv"
        if outcome_path.exists():
            required = ("prediction_id", "request_id", "judgment", "evidence_levels", "matched_normal",
                        "matched_boundary", "strict_pair_denominator_member", "unique_support", "both_rejected",
                        "pair_disposition", "relation_after_read")
            outcomes, outcome_fields = read_csv("outcomes.csv", required)
            result["schemas"]["outcomes.csv"] = outcome_fields
            out_ids = [row.get("prediction_id") for row in outcomes]
            check("outcomes:12_rows", len(outcomes) == 12, len(outcomes), 12)
            check("outcomes:one_row_each_prediction", len(out_ids) == len(set(out_ids)) and set(out_ids) == set(pred_by_id), duplicate_values(out_ids))
            check("outcomes:prediction_request_join", all(row.get("prediction_id") in pred_by_id and row.get("request_id") == pred_by_id[row["prediction_id"]]["request_id"] for row in outcomes))
            boolean_counts = {}
            declared_true_cases = {}
            for field in OUTCOME_BOOLEAN_FIELDS:
                values = [row.get(field, "") for row in outcomes]
                check("outcomes:" + field + ":lowercase_boolean", all(value in ("true", "false") for value in values), counter_dict(values))
                boolean_counts[field] = counter_dict(values)
                declared_true_cases[field] = sorted({row.get("request_id") for row in outcomes if row.get(field) == "true"})
            strict_by_case = {case: {row.get("strict_pair_denominator_member") for row in outcomes if row.get("request_id") == case} for case in sorted(request_ids)}
            pair_flags_consistent = all(len(values) == 1 and values <= {"true", "false"} for values in strict_by_case.values())
            check("outcomes:strict_pair_flag_consistent", pair_flags_consistent, {case: sorted(values) for case, values in strict_by_case.items()})
            declared_n = len(declared_true_cases["strict_pair_denominator_member"]) if pair_flags_consistent else None
            result["outcomes"] = {
                "present": True, "rows": len(outcomes),
                "field_value_counts_original_strings": {field: counter_dict(row.get(field, "") for row in outcomes) for field in ("judgment", "evidence_levels", "pair_disposition", "relation_after_read")},
                "boolean_field_counts_original_strings": boolean_counts,
                "declared_true_request_ids_by_field": declared_true_cases,
                "strict_denominator_cases_from_explicit_consistent_flags": declared_n,
                "strict_conditional_rate_display": "해당 없음" if declared_n == 0 else "not calculated; verifier reports declared counts only",
                "strict_denominator_inferred_from_prose": False,
                "unique_support_true_rows": sum(row.get("unique_support") == "true" for row in outcomes),
                "both_rejected_true_rows": sum(row.get("both_rejected") == "true" for row in outcomes),
                "note": "True row counts and distinct request IDs are both exposed. No new support/eligibility decision is made, and original sealed pair relation is not overwritten by relation_after_read.",
            }
        else:
            check("outcomes:presence_if_required", not args.require_outcomes, False, args.require_outcomes)
            result["outcomes"] = {"present": False, "status": "pending", "strict_denominator": None,
                                  "reason": "No outcomes.csv yet; absence is not an observed denominator of zero."}

        # Exact index arithmetic, separate from any executable receiver behavior.
        def fixture(fs, fft_n):
            df = Fraction(fs, fft_n)
            low = math.floor(Fraction(1000) / df)
            high = math.ceil(Fraction(2000) / df)
            return {"fs_hz": fs, "fft_n": fft_n, "bin_spacing_hz": float(df),
                    "low_included_bin": low, "low_center_hz": float(low * df),
                    "high_exclusive_bin": high, "high_center_hz": float(high * df),
                    "last_included_center_hz": float((high - 1) * df),
                    "old_bin86_hz": float(86 * df), "old_bin86_inside": low <= 86 < high}

        base = fixture(48000, 2048)
        low, high = base["low_included_bin"], base["high_exclusive_bin"]
        def hard_db(k):
            return Fraction(-6 if low <= k < high else 0)
        def geometric_log_db(k, radius):
            return sum((hard_db(j) for j in range(k - radius, k + radius + 1)), Fraction(0)) / (2 * radius + 1)
        boundary = high
        geometric5 = geometric_log_db(boundary, 2)
        normal_geometric5 = geometric_log_db(64, 2)
        linear5_gain = sum(10 ** (float(hard_db(j)) / 20) for j in range(boundary - 2, boundary + 3)) / 5
        check("arithmetic:AUD03:frozen_indices", (low, high) == (42, 86), [low, high], [42, 86])
        check("arithmetic:AUD03:normal_log_gain", normal_geometric5 == hard_db(64) == -6)
        check("arithmetic:AUD03:first_excluded_log_gain", geometric5 == Fraction(-12, 5) and hard_db(boundary) == 0)
        m03 = {"factor0.01_max0.99": Fraction(1, 2) / Fraction(99, 100),
               "factor0.001_max0.099": Fraction(1, 2) / Fraction(99, 1000),
               "factor0.1_max9.9": Fraction(1, 2) / Fraction(99, 10)}
        result["arithmetic"] = {
            "kind": "Researcher-defined conditional models only; not Audacity/Matplotlib execution or public acceptance-test evidence.",
            "AUD03": {"fixed_fixture": base, "normal_bin": 64, "normal_frequency_hz": 1500,
                "normal_A_db": float(hard_db(64)), "normal_B_db": float(normal_geometric5),
                "first_excluded_A_db": float(hard_db(boundary)), "first_excluded_B_geometric5_db": float(geometric5),
                "first_excluded_B_geometric5_db_exact": str(geometric5),
                "first_excluded_B_gain": 10 ** (float(geometric5) / 20),
                "lower_bin_center_below1000": base["low_center_hz"] < 1000,
                "kernel_variants_first_excluded_db": {**{"symmetric_geometric_radius" + str(radius): float(geometric_log_db(boundary, radius)) for radius in range(4)},
                    "arithmetic_linear5": 20 * math.log10(linear5_gain), "inside_only_smoothing": 0.0},
                "unit_variants": [fixture(48000, 2048), fixture(48000, 4096), fixture(44100, 2048)],
                "unit_variant_limit": "Each new first-excluded index has the same -2.4dB toy relation for a sufficiently wide selected band; keeping index86 changes physical frequency and may move it inside.",
                "feasibility_limit": "Post-reveal parent correction reports local #undef of spectral editing in NoiseReduction.cpp. No model result establishes an enabled receiver API."},
            "M03": {"assumptions": "linear non-inverted limits [0,max(arr)], exact data coordinate0.5; actual colorbar limits must be checked separately",
                "data_y_fraction": {key: {"exact": str(value), "decimal": float(value)} for key, value in m03.items()},
                "axes_center_y": 0.5, "purpose_flip": "If y-datum0.5 rather than vertical container center is the requirement, data anchoring for y can become appropriate; full default(.5,.5) also uses x data units, so horizontal centering needs a separate/blended transform."},
            "AUD01": {"one_frame_at25fps_seconds": float(Fraction(1, 25)), "one_sample_at48000_seconds": float(Fraction(1, 48000)),
                "frame_to_sample_ratio": 1920, "point_getter_bounds": [1.25, 1.25],
                "exception": "W3C temporal fragment a>=b is invalid-and-ignore; do not map it to a valid editor point-selection getter."},
            "AUD02": {"identical_colors_WCAG_ratio": 1, "black_white_WCAG_ratio": 21,
                "warning": "Sealed colloquial contrast0 is zero visible difference, not ratio0. Native-app policy and essential-color exceptions require separate justification."},
        }
        warnings.extend([
            "Sources/amendments hashes are intentionally not enforced after seal; their current hashes are recorded.",
            "A source quota pass does not prove matching-input followup, historical donor availability, or author adoption.",
            "M02/AUD01 same predictions and AUD02 underdetermined must not become discriminating successes automatically.",
            "Run after root integration is complete; multiple files are read once each, not as a filesystem-atomic snapshot.",
        ])
        if (OWNED / "outcomes.csv").exists():
            policy_rows = list(csv.DictReader((OWNED / "outcomes.csv").open()))
            policies = {}
            for label, field, disp in [
                ("complete_comparison_post_reveal", "strict_pair_denominator_member", "pair_disposition"),
                ("original_wording_lenient", "original_wording_lenient_case_member", "lenient_case_disposition"),
                ("operator_only_sensitivity", "operator_only_case_member", "operator_only_disposition")]:
                policy_cases = sorted({r["request_id"] for r in policy_rows if r.get(field) == "true"})
                policies[label] = {"explicit_flag_field": field, "case_ids": policy_cases,
                    "denominator": len(policy_cases), "unique_support": len({r["request_id"] for r in policy_rows if r.get(field)=="true" and r.get("unique_support" if label=="complete_comparison_post_reveal" else "lenient_unique_support")=="true"}), "both_rejected": len({r["request_id"] for r in policy_rows if r.get(field)=="true" and r.get("both_rejected")=="true"}),
                    "indeterminate_cases": sorted({r["request_id"] for r in policy_rows if r.get(field)=="true" and r.get(disp)=="판정불가"}),
                    "numerator_source": "explicit unique_support/lenient_unique_support false flags; no prose inference",
                    "rate_interpretation": "해당 없음" if not policy_cases else "No unique support established; not an effect-absence or failure-rate estimate"}
                for cid in sorted({r["request_id"] for r in policy_rows}):
                    vals={r.get(field) for r in policy_rows if r["request_id"]==cid}
                    check("policy_consistency:"+label+":"+cid, len(vals)==1, sorted(str(v) for v in vals), "one explicit value per case")
            result["denominator_policies"] = policies
            result["eligibility_policy_limit"] = "Complete comparison is a post-reveal strengthening of the original same-input wording. Original-wording lenient M01 and operator-only M01/M03 sensitivities are preserved separately."
    except (OSError, ValueError, KeyError, TypeError, csv.Error, json.JSONDecodeError) as exc:
        check("input_exception", False, {"type": type(exc).__name__, "message": str(exc)})

    result["input_sha256"] = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(cache.items())}
    result["checks"] = checks
    result["warnings"] = warnings
    structural_failures = [item["check"] for item in checks if not item["passed"] and item["kind"] == "structural"]
    quota_failures = [item["check"] for item in checks if not item["passed"] and item["kind"] == "quota"]
    result["summary"] = {"structural_pass": not structural_failures, "source_quotas_pass": not quota_failures,
                         "structural_failures": structural_failures, "quota_failures": quota_failures,
                         "passed_checks": sum(item["passed"] for item in checks), "total_checks": len(checks)}
    result["exit_code"] = 2 if structural_failures else 1 if quota_failures else 0
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        target = args.output.resolve()
        try:
            target.relative_to(OWNED)
        except ValueError:
            parser.error("--output must be inside " + str(OWNED))
        if target in {(OWNED / name).resolve() for name in cache} or target == Path(__file__).resolve():
            parser.error("--output must not overwrite an input or this verifier")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(encoded, encoding="utf-8")
        print(json.dumps({"output": str(target), "summary": result["summary"], "exit_code": result["exit_code"]}, ensure_ascii=False, sort_keys=True))
    else:
        sys.stdout.write(encoded)
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
