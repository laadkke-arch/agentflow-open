"""Independent, read-only review of root AF-RES-106 report/ledger consistency.

Writes only this reviewer's evidence/crossdomain/final-root-review.json.
Does not import the report generator or its validation implementation.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
REPO = ROOT.parents[3]
SEAL = "8054c2221d4023ba03c904d96f13928219d36c3d"
checks = []


def check(name, condition, detail=None):
    checks.append({"name": name, "passed": bool(condition), "detail": detail})


def table_blocks(text):
    result, rows = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            rows.append([v.strip() for v in re.split(r"(?<!\\)\|", line)[1:-1]])
        elif rows:
            result.append(rows)
            rows = []
    return result


def rows(name):
    with (ROOT / name).open() as f:
        return list(csv.DictReader(f))


def read_json_list(value):
    return json.loads(value) if value else []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = (ROOT / "RESULT.md").read_text()
self_check = (ROOT / "SELF_CHECK.md").read_text()
reproduce = (ROOT / "reproduce.md").read_text()
blocks = table_blocks(result)
predictions = rows("predictions.csv")
lineage = rows("lineage.csv")
returns = rows("returns.csv")
frame = rows("frame.csv")
counts = json.loads((ROOT / "counts.json").read_text())
sources = [json.loads(s) for s in (ROOT / "sources.jsonl").read_text().splitlines() if s]
allowlist = json.loads((HERE / "source-count-review.json").read_text())
new = {r["case_id"]: r for r in lineage if r["edition"] == "new"}
old = {r["case_id"]: r for r in lineage if r["edition"] == "old"}
ret = {r["case_id"]: r for r in returns}

check("report_starts_with_required_recruitment_table", result.startswith("| 프로젝트·층·자리 |"))
check("first_three_table_sizes", [len(x) - 2 for x in blocks[:3]] == [12, 24, 12])
check("first_three_table_column_counts", all(len(r) == n for b, n in zip(blocks[:3], [6, 7, 6]) for r in b))
check("ending_exactly_three_weakness_rows", len(blocks[-1]) - 2 == 3 and result.rstrip().endswith("|"))
check("ending_headers", blocks[-1][0] == ["가장 중요한 불일치·약점", "다음 조사 제안·직접 열 자료 또는 실행할 입력", "어떤 관측이면 판단을 바꿀지"])
check("unique_cases_and_slots", len(predictions) == 12 and len(set(r["case_id"] for r in predictions)) == 12 and len(lineage) == 24 and len(returns) == 12)
check("each_case_has_both_editions", all(Counter(r["edition"] for r in lineage if r["case_id"] == p["case_id"]) == {"old": 1, "new": 1} for p in predictions))
check("filled_vacant_case_counts", Counter(p["vacant"] for p in predictions) == {"NO": 8, "YES": 4})
check("filled_vacant_edition_counts", Counter(r["vacant"] for r in lineage) == {"NO": 16, "YES": 8})

for p, table_row in zip(predictions, blocks[0][2:]):
    case = p["case_id"]
    check(case + ":recruitment_case_order", case in table_row[0])
    check(case + ":frozen_prediction_and_time_in_table", p["prediction_U"] in table_row[4] and (p["prediction_utc"] or p["prediction_recorded_utc"]) in table_row[4])
    check(case + ":tree_source_in_table", (p["new_tree_evidence_url"] or p["tree_evidence_url"]) in table_row[2])
    if p["vacant"] == "NO":
        check(case + ":old_and_provisional_urls_in_table", p["old_section_url"] in table_row[1] and (p["provisional_return_url"] or p["new_provisional_section_url"]) in table_row[3])
    else:
        check(case + ":vacancy_not_an_observed_negative", "결원" in table_row[5] and new[case]["U_original_purpose"] == "미확인")

for r, table_row in zip(lineage, blocks[1][2:]):
    case = r["case_id"] + ":" + r["edition"]
    check(case + ":lineage_table_case_and_version", table_row[0] == r["case_id"] + "·" + r["version"])
    check(case + ":G_literal_unknown", r["G"] == "미확인" and table_row[5] == "미확인")
    if r["vacant"] == "YES":
        check(case + ":vacant_table_explicit", "결원" in table_row[1] and "미확인" in table_row[2])
        continue
    check(case + ":fixed_html_and_DOM_fragment", (r["github_read_url"] or r["github_section_url"]) in table_row[1] and "`#" + r["actual_fragment"].lstrip("#") + "`" in table_row[1])
    check(case + ":payload_source_and_hashes", all(v in table_row[2] for v in [r["payload_url"], r["source_url"], r["payload_sha256"][:12], r["source_sha256"][:12]]))
    check(case + ":P_arrival_labels", all(v in table_row[3] for v in ["P " + r["P"], "옛 경로 P " + r["legacy_path_P"], "옛 fragment " + r["old_fragment_arrival"]]))
    check(case + ":purpose_method_labels", all(v in table_row[4] for v in ["원 목적 " + r["U_original_purpose"], "일반 역할 " + r["U_visual_role"], "핵심 API " + r["method_core_api"], "사전 구체 방법 " + r["method_specific"], "원 구성 " + r["method_original_exact"]]))
    paths = read_json_list(r["evidence_files"])
    check(case + ":evidence_paths_exist", bool(paths) and all((ROOT / path).is_file() for path in paths))

recomputed = {}
for axis, count_key in [("U_original_purpose", "main_original_purpose"), ("U_visual_role", "main_visual_role")]:
    axis_out = []
    for group in counts[count_key]:
        ps = [p for p in predictions if p["project"] == group["project"] and p["stratum"] == group["stratum"]]
        tally = Counter({key: 0 for key in ["TP", "FP", "FN", "TN", "vacancies", "prediction_abstentions", "observed_unknown", "actual_positive", "actual_negative"]})
        for p in ps:
            if p["vacant"] == "YES":
                tally["vacancies"] += 1
                continue
            prediction, observation = p["prediction_U"], new[p["case_id"]][axis]
            if observation == "YES":
                tally["actual_positive"] += 1
            elif observation == "NO":
                tally["actual_negative"] += 1
            else:
                tally["observed_unknown"] += 1
            if prediction not in ["YES", "NO"]:
                tally["prediction_abstentions"] += 1
            elif observation in ["YES", "NO"]:
                tally[{("YES", "YES"): "TP", ("YES", "NO"): "FP", ("NO", "YES"): "FN", ("NO", "NO"): "TN"}[(prediction, observation)]] += 1
        key = group["project"] + ":" + group["stratum"] + ":" + axis
        check(key + ":recomputed_confusion", all(tally[k] == group[k] for k in tally), dict(tally))
        check(key + ":FPR_denominator", group["FPR"]["numerator"] == tally["FP"] and group["FPR"]["denominator"] == tally["actual_negative"])
        check(key + ":zero_denominator_not_zero_rate", tally["actual_negative"] != 0 or group["FPR"]["value"] == "산출 불가")
        axis_out.append({"project": group["project"], "stratum": group["stratum"], **tally})
    recomputed[axis] = axis_out

for p, table_row in zip(predictions, blocks[2][2:]):
    case = p["case_id"]
    r = ret[case]
    check(case + ":return_decision_table", case in table_row[0] and r["decision"] in table_row[3])
    group = next(g for g in counts["main_original_purpose"] if g["project"] == p["project"] and g["stratum"] == p["stratum"])
    denominator = "층 실제 양성 {actual_positive}/음성 {actual_negative}/실측 미확인 {observed_unknown}/예측 유보 {prediction_abstentions}/결원 {vacancies}".format(**group)
    check(case + ":return_denominators", table_row[2] == denominator)
    if p["vacant"] == "YES":
        continue
    expected_error = {("YES", "YES"): "TP", ("YES", "NO"): "FP", ("NO", "YES"): "FN", ("NO", "NO"): "TN"}[(p["prediction_U"], new[case]["U_original_purpose"])]
    check(case + ":return_error", p["prediction_U"] + "→" + new[case]["U_original_purpose"] + " " + expected_error in table_row[1])
    old_fixed = old[case]["github_read_url"] or old[case]["github_section_url"]
    new_fixed = new[case]["github_read_url"] or new[case]["github_section_url"]
    check(case + ":return_fixed_positions", old_fixed in table_row[3] and new_fixed in table_row[3] and "`#" + new[case]["actual_fragment"].lstrip("#") + "`" in table_row[3])
    check(case + ":return_cost", "추가 문서 " + r["logical_document_visits"] + ", HTTP " + r["additional_content_http_reads"] in table_row[3])
    check(case + ":return_change_condition", r["change_condition"] in table_row[5])
    receipts = read_json_list(r["additional_content_http_receipts"] or r["http_receipt_files"])
    check(case + ":return_receipts", len(receipts) == int(r["additional_content_http_reads"]) and all((ROOT / x).is_file() for x in receipts))

eligible = [r for r in frame if r["eligible"] == "YES"]
check("frame_803_eligible547", len(frame) == 803 and len(eligible) == 547)
check("all_eligible_hashes_exact_case", all(hashlib.sha256(("AF106|" + r["project"] + "|" + r["old_section_path"]).encode("utf-8")).hexdigest() == r["hash_sha256"] for r in eligible))
for group in counts["main_original_purpose"]:
    candidates = sorted((r for r in eligible if r["project"] == group["project"] and (r["stratum"] or r["signal_stratum"]) == group["stratum"]), key=lambda r: (r["hash_sha256"], r["old_section_path"]))
    selected = [p for p in predictions if p["project"] == group["project"] and p["stratum"] == group["stratum"] and p["vacant"] == "NO"]
    check(group["project"] + ":" + group["stratum"] + ":selected_first_two", [r["old_section_path"] for r in candidates[:2]] == [p["old_section_path"] for p in selected])

for name in ["frame.csv", "predictions.csv", "SCOPE.md", "EVALUATION_TARGETS.md"]:
    rel = (ROOT / name).relative_to(REPO).as_posix()
    sealed = subprocess.check_output(["git", "show", SEAL + ":" + rel], cwd=REPO)
    check(name + ":sealed_bytes_unchanged", sealed == (ROOT / name).read_bytes())

countable = [r for r in sources if r["countable"]]
check("source_rows_670_countable38", len(sources) == 670 and len(countable) == 38)
check("source_count_matches_independent_allowlist", set(r["id"] for r in countable) == set(allowlist["counted_ids"]))
check("source_countable_ids_unique", len(set(r["id"] for r in countable)) == 38)
check("source_countable_all_direct_read", all(r["direct_read"] for r in countable))
check("allowlist_category_totals", allowlist["total"] == 38 and allowlist["duplicate_work_keys"] == [] and allowlist["duplicate_ids"] == [] and allowlist["inherited_exact_hits"] == [])
check("self_check_Q1_to_Q7", all(any(row[0].startswith("Q" + str(i) + " ") for row in table_blocks(self_check)[0][2:]) for i in range(1, 8)))
check("strict_unused_not_claimed", "미사용 잔류 파일 사례가 아니다" in result and "엄격한 반례는 미확보" in result)
check("purpose_axes_and_timing_limit_disclosed", "경로/선택 노출 뒤" in result or "경로/선택 노출 뒤" in self_check)
check("methods_vs_G_and_render_limit_disclosed", "G16판" in self_check and "브라우저" in reproduce and "미확인" in reproduce)
check("reproduce_ten_candidates", "검색 후보5개+의미상 후보5개 총10본문" in reproduce)
check("reproduce_exact_required_commands", all(command in reproduce for command in ["python -B -m workbench.session check docs/workstreams/research/AF-RES-106/manifest.json --fetch", "python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean"]))
check("reproduce_writing_scripts_restricted_to_copies", "별도 복사본에서만" in reproduce and "입력 파일을 바꾸지 않고" in reproduce)

missing_links = []
for name in ["RESULT.md", "SELF_CHECK.md", "reproduce.md"]:
    for label, url in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", (ROOT / name).read_text()):
        if not re.match(r"^[a-z]+:", url):
            target = url.split("#")[0]
            if target and not (ROOT / target).exists():
                missing_links.append({"document": name, "label": label, "target": target})
check("no_unexpected_missing_report_links", all(r["target"] in ["VALIDATION.md", "HANDOFF.md"] for r in missing_links), missing_links)

out = {
    "reviewed_utc": datetime.now(timezone.utc).isoformat(),
    "reviewer": "crossdomain_review; separate same-family AI; aware of reported outcomes; no new blind adjudication",
    "scope": "Independent read-only report/ledger/selection/denominator/source-allowlist consistency review. Prior direct Q7 and source audits are linked separately. Not a fresh semantic census of all 547 examples, browser execution, historical build verification, or repository contract/cloud check.",
    "reviewer_initial_parser_correction": "First review run reported 316/318: reviewer incorrectly used only stratum, which is blank for GG rows. The sealed union schema stores GG in signal_stratum and MP in stratum. Corrected this reviewer's column fallback, without changing any input or conclusion; final run follows.",
    "seal": SEAL,
    "git_head_at_review": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
    "artifact_sha256": {name: digest(ROOT / name) for name in ["RESULT.md", "SELF_CHECK.md", "reproduce.md", "counts.json", "lineage.csv", "returns.csv", "predictions.csv", "frame.csv", "sources.jsonl"]},
    "checks": checks,
    "checks_total": len(checks),
    "checks_passed": sum(c["passed"] for c in checks),
    "checks_failed": [c for c in checks if not c["passed"]],
    "confusion_recomputed": recomputed,
    "required_table_rows": [len(b) - 2 for b in blocks[:3]],
    "ending_weakness_rows": len(blocks[-1]) - 2,
    "counted_primary_materials": len(countable),
    "counted_ids_match_prior_independent_review": True,
    "pending_result_commit_tasks": ["Exact clean result-SHA session and cloud checks", "Fixed-SHA GitHub readback and return-fragment reinspection", "VALIDATION receipt document", "Last standalone HANDOFF commit"],
    "wording_correction_requested": {"file": "SELF_CHECK.md", "issue": "Its initial wording could be read as only 4 access failures total. GG has 4 DisabledError failures and crossdomain/probe-failures.json separately has 4 failed Q7 probes (3 web Internal Error plus 1 HTTP403).", "denominator_impact": "none; all failure responses count0", "status": "Requested parent to scope GG4 and mention Q7 probes separately; check final file for applied wording."},
    "prior_reviews": ["review-final.json", "CROSSDOMAIN_FINAL.md", "source-count-review.json", "source-count-review.md"],
}
(HERE / "final-root-review.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"checks_total": out["checks_total"], "checks_passed": out["checks_passed"], "failed": out["checks_failed"], "rows": out["required_table_rows"], "source_count": len(countable)}, ensure_ascii=False))
