"""Audit joins, action budgets and separation of frozen retrieval evidence.

Reads the current observation ledgers and frozen stage2 slots. Does not rerun
provider tests or alter their receipts. Outputs only the review receipt.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import subprocess

HERE = Path(__file__).resolve().parent
TASK = HERE.parents[1]
REPO = HERE.parents[5]
PREFIX = "docs/workstreams/research/AF-RES-056/"
STAGE2 = "b765a189aa2a1f5982a4994fc0476273abbf7127"
PIN = "d5199551f758ba067612979ae32ec35693640ccf"
inputs = {}


def data(name):
    value = (TASK / name).read_bytes()
    inputs[name] = {"sha256": hashlib.sha256(value).hexdigest(), "bytes": len(value)}
    return value


def table(name):
    return list(csv.DictReader(io.StringIO(data(name).decode())))


def obj(name):
    return json.loads(data(name))


windows = table("windows.csv")
judgments = table("judgments.csv")
slot_bytes = subprocess.check_output(["git", "show", STAGE2 + ":" + PREFIX + "slots.csv"], cwd=REPO)
slots = list(csv.DictReader(io.StringIO(slot_bytes.decode())))
slot_by_key = {(s["case_id"] + "-" + s["method"], s["slot"]): s for s in slots}
input_slots = {"git_ref": STAGE2, "sha256": hashlib.sha256(slot_bytes).hexdigest()}
active = [r for r in windows if r["catalog_id"]]
empty = [r for r in windows if not r["catalog_id"]]
main = [r for r in judgments if r["catalog_id"] and r["method"] in {"L", "V"}]
diagnostic = [r for r in judgments if r["method"] == "diagnostic"]
empty_judgments = [r for r in judgments if not r["catalog_id"]]
trials = defaultdict(list)
for r in active:
    trials[r["trial_id"]].append(r)
checks = []


def canonical_source(source_id):
    return {"WIN-01-V2": "WIN-01", "WIN-02-V2": "WIN-02"}.get(source_id, source_id)


def check(name, condition, detail):
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


check("dimensions", [len(windows), len(judgments), len(active), len(empty), len(main), len(empty_judgments), len(diagnostic)] == [52, 19, 5, 47, 3, 15, 1], "52 window rows = 47 unfilled slots + 5 action rows; 19 judgments = 15 empty comparisons + 3 trials + 1 outside diagnostic.")
check("window_ids_unique", len(set(r["window_id"] for r in windows)) == len(windows), "No action or empty placeholder reused as another row.")
check("empty_slots_exactly_once", Counter((r["comparison_id"], r["slot"]) for r in empty) == Counter(k for k, s in slot_by_key.items() if not s["catalog_id"]), "All and only 47 frozen unfilled slots represented once.")
check("empty_slot_states", all(r["window_status"] == slot_by_key[r["comparison_id"], r["slot"]]["status"] for r in empty), "45 observed-no-match and 2 pool-exhausted are not access failures.")
check("empty_rows_have_no_actions", all(not r["trial_id"] and not r["action_index"] and not r["source_id"] and not r["final_url"] for r in empty), "No fictional read trial for an empty slot.")
check("active_slots_join", all((r["catalog_id"], r["posted_rank"], r["case_id"], r["method"]) == tuple(slot_by_key[r["comparison_id"], r["slot"]][k] for k in ["catalog_id", "original_rank", "case_id", "method"]) for r in active), "Every action belongs to frozen JS-4-V/S1, SC-032/rank32.")

expected_paths = {"JS-4-V-P1": ["WIN-01"], "JS-4-V-P2": ["WIN-01", "WIN-02"], "JS-4-V-P3": ["WIN-01", "WIN-03"]}
for trial, sources in expected_paths.items():
    rows = sorted(trials.get(trial, []), key=lambda r: int(r["action_index"]))
    check("trial_sequence_" + trial, [int(r["action_index"]) for r in rows] == list(range(1, len(sources) + 1)) and [canonical_source(r["source_id"]) for r in rows] == sources, "Predeclared direct/read-first-link/read-second-link paths only; explicit v2 IDs retain the same document identity.")
    check("action_budget_" + trial, len(rows) <= 2 and all(int(r["trial_action_count"]) == len(rows) for r in rows), {"actual_actions": len(rows)})
    judgment = next(r for r in main if r["trial_id"] == trial)
    check("judgment_sources_" + trial, judgment["source_ids"].split(";") == [r["source_id"] for r in rows], "Exact versioned source IDs join the same trial; no other trial or outside diagnostic enters this judgment.")
    check("judgment_unknown_" + trial, judgment["C1_status"] == judgment["C2_status"] == judgment["classification"] == "미확인", "Neither generic validation nor standard text upgraded to a condition proof.")
check("all_expected_trials_only", set(trials) == set(expected_paths), "No second representative exists; no extra path constructed.")
check("same_provider_version", all(r["snapshot_sha_or_hash"] == PIN for r in active if canonical_source(r["source_id"]) == "WIN-01") and len(set(r["source_id"] for r in active if canonical_source(r["source_id"]) == "WIN-01")) == 1, "One fixed README response and extraction version reused across three logical paths.")
check("first_action_uses_frozen_destination", all(r["original_url"] == slot_by_key[r["comparison_id"], r["slot"]]["url"] for r in active if r["action_index"] == "1"), "Source-first URL comes from frozen catalog.")
check("empty_comparison_judgments", Counter(r["comparison_id"] for r in empty_judgments) == Counter(set(r["comparison_id"] for r in empty) - {"JS-4-V"}), "15 empty method-comparisons, not 47 candidates or trials.")
check("outside_diagnostic_separate", len(diagnostic) == 1 and diagnostic[0]["trial_id"] == "OUTSIDE-BUDGET" and diagnostic[0]["within_budget"] == "no", "C2 compiled fixture cannot increase main partial count.")
check("main_no_diagnostic_source", all(set(canonical_source(s) for s in r["source_ids"].split(";")) <= {"WIN-01", "WIN-02", "WIN-03"} for r in main), "WIN-06 enum code and EXEC-SC032 excluded from main windows.")

execution = obj("evidence/windows/sc032-execution.json")
fixture_hash = hashlib.sha256(data("evidence/windows/schema_fixture.cpp")).hexdigest()
check("diagnostic_fixture_hash", fixture_hash == execution["fixture_sha256"], "Reviewed fixture equals recorded executed fixture; not independently rebuilt by auditor.")
check("diagnostic_output_matches_cases", json.loads(execution["run_stdout"]) == execution["cases"], "Structured cases reproduce recorded stdout.")
check("diagnostic_outcomes", execution["build_exit_code"] == execution["run_exit_code"] == 0 and [c["actual_validator_accept"] for c in execution["cases"]] == [True, False, True], "C2 positive accepted; datatype near negative rejected; missing pii accepted by C2-only schema.")

readme_v2 = obj("evidence/review/SC-032-rendered-window-v2.json")
home_v2 = obj("evidence/review/SC-032-home-rendered-window-v2.json")
check("readme_rendered_correction", readme_v2["v1_rendered_visible_words"] == 487 and readme_v2["v2_visible_words"] == 500 and readme_v2["v2_source_line_end"] == 106 and readme_v2["first_two_destination_urls_unchanged"], "Installed pandoc GFM -> HTML text-node measurement, not an invented count.")
check("homepage_same_response_correction", home_v2["v1_raw_window_recovered_exactly"] and home_v2["v1_rendered_visible_words"] == 479 and home_v2["v2_visible_words"] == 500 and home_v2["v2_source_end_line"] == 105, "The original cached page text, not a later live page, supplies the corrected boundary.")
check("corrections_do_not_change_judgments", not readme_v2["combined_changed"] and not home_v2["combined_changed"], "Added build instructions and community dates do not establish C1/C2.")
schema_retry = obj("evidence/windows/schema-json-retry.json")
check("headingless_JSON_stays_unknown", schema_retry["words"] == 168 and all(r["C1"] == r["C2"] == r["combined"] == "미확인" for r in active if r["source_id"] == "WIN-03"), "Transport recovery is distinct from an undefined heading-based window; no success constructed.")

receipt = {
    "reviewer": "/root/authority_records; same-model within-team reviewer, no independent runtime reexecution",
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "input_state": "Working-tree observation files before stage3 seal; exact hashes below identify the audited version.",
    "frozen_slots": input_slots,
    "input_receipts": inputs,
    "counts": {"window_rows": len(windows), "empty_rows": len(empty), "action_rows": len(active), "logical_paths": len(trials), "distinct_candidates": len(set(r["catalog_id"] for r in active)), "distinct_document_responses": len(set(r["source_id"] for r in active)), "judgment_rows": len(judgments), "main_trial_judgments": len(main), "empty_comparison_judgments": len(empty_judgments), "outside_diagnostic_judgments": len(diagnostic), "main_complete_candidates": 0, "main_partial_candidates": 0, "main_unconfirmed_candidates": 1},
    "trial_action_counts": {trial: len(rows) for trial, rows in trials.items()},
    "observed_window_ranges": {r["source_id"]: r["section_or_range"] for r in active},
    "rendered_corrections": {"README": {"v1_raw_words": 500, "v1_visible_words": 487, "v1_last_source_line": 99, "v2_visible_words": 500, "v2_last_source_line": 106}, "homepage": {"v1_raw_words": 500, "v1_visible_words": 479, "v1_last_source_line": 96, "v2_visible_words": 500, "v2_last_source_line": 105}},
    "action_budget_vs_window_validity": "P3 has two document-opening actions; its headingless JSON response still lacks a valid predeclared content boundary.",
    "reviewer_initial_recommendation": "Preserve v1 and treat the rendered calculation as a post-hoc boundary sensitivity; do not silently overwrite the original observation.",
    "root_correction_decision": "Root preserved v1 and applied v2 in the working-tree ledger as a mechanical extraction correction to the already specified rendered-text rule, disclosing post-observation exposure and unchanged outcomes. This audit records both interpretations and does not claim unexposed v2 measurement; remote seal remains a publication followup.",
    "diagnostic_oracle_caution": "desired_full_contract_accept in original fixture/stdout is a two-analysis-condition expected value, not proof that original name/description/nonempty guards were satisfied.",
    "checks": checks,
    "structural_and_correction_checks_passed": all(c["passed"] for c in checks),
    "publication_followup": "Recheck that sealed final windows and SCOPE use v2 positions/hashes while retaining v1, exact link lines, P1 single-action wording and P3 boundary caveat.",
}
(HERE / "window-audit-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"checks": len(checks), "passed": receipt["structural_and_correction_checks_passed"], "failed": [c["check"] for c in checks if not c["passed"]], "counts": receipt["counts"], "observed_ranges": receipt["observed_window_ranges"]}, ensure_ascii=False))
raise SystemExit(0 if receipt["structural_and_correction_checks_passed"] else 1)
