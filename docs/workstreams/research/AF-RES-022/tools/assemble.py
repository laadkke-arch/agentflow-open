#!/usr/bin/env python3
"""Assemble AF-RES-022 research ledgers without changing the stream originals.

Run from the repository root. This is deterministic except for no timestamp: all
timestamps come from the recorded source/audit inputs. It does not fetch sources.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
STREAMS = ("adr", "apache", "rust", "b")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_csv(path, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


sources = []
decisions = []
sampling = []
costs = []
for stream in (*STREAMS, "crossfield"):
    folder = BASE / "streams" / stream
    for row in json.loads((folder / "sources.json").read_text()):
        row["stream"] = stream
        sources.append(row)
    if stream == "crossfield":
        continue
    for row in read_jsonl(folder / "decisions.jsonl"):
        row["stream"] = stream
        row["raw_record_family"] = row["record_family"]
        if row["sample"] == "A":
            row["record_family"] = row["record_family"].split(":", 1)[0]
        decisions.append(row)
    for row in read_csv(folder / "sampling.csv"):
        row["stream"] = stream
        sampling.append(row)
    for row in read_csv(folder / "costs.csv"):
        row["stream"] = stream
        row["original_cost_kind"] = row["cost_kind"]
        row["original_unit"] = row["unit"]
        if row["cost_kind"] == "unconfirmed_counterfactual":
            row["cost_kind"] = "researcher_counterfactual_unknown"
        if row["cost_kind"] == "actual_logged_effort_scope_unconfirmed":
            row["cost_kind"] = "observed_effort_unattributed"
        if not row["unit"]:
            row["unit"] = "unreported"
        costs.append(row)

for row in sources:
    if row["source_id"] == "B-030":
        row["stream_observed"] = row["observed"]
        row["observed"] = "후속 코드가 cls=PathEncoder를 호출하고 JSONEncoder 호환 하위클래스로 Path를 변환한다. 기존 디렉터리 순회·중복 비교 목적을 유지하고, 후속판에 추가한 YAML은 convert_results로 별도 변환한다."

for row in json.loads((BASE / "evidence/input-audit.json").read_text()):
    row["stream"] = "fixed_inputs"
    sources.append(row)

# Central provenance overrides preserve the source stream's original count flag.
override_file = BASE / "evidence/source-count-overrides.json"
overrides = json.loads(override_file.read_text()) if override_file.exists() else []
by_source = {row["source_id"]: row for row in sources}
for correction in overrides:
    row = by_source[correction["source_id"]]
    row["stream_count_in_minimum"] = row["count_in_minimum"]
    row["count_in_minimum"] = correction["count_in_minimum"]
    row["counting_note"] = correction["reason"]
    row["same_work_as"] = correction.get("same_work_as")
    if correction.get("count_category"):
        row["stream_count_category"] = row["count_category"]
        row["count_category"] = correction["count_category"]

audit = json.loads((BASE / "streams/apache/awareness-audit.json").read_text())
audit_rows = {row["id"]: row for row in audit["rows"]}
by_case = {row["id"]: row for row in decisions}
for row in decisions:
    row["raw_stream_flags"] = {key: row.get(key) for key in (
        "awareness_unknown", "connected_chain", "strict_discovery_change", "later_available")}
    if row["sample"] == "A":
        row["initial_awareness_audit"] = audit_rows[row["id"]]
        row["initial_focal_awareness_unknown"] = audit_rows[row["id"]]["baseline_known"] is None
        row["available_awareness_completion_candidate"] = audit_rows[row["id"]].get(
            "available_awareness_completion_candidate", False)
        row["actual_scoped_execution"] = audit_rows[row["id"]]["actual_execution"]
    if row["stream"] == "apache":
        original_mail = {
            "A09": "AP-M25-ORIG", "A10": "AP-M26-ORIG", "A11": "AP-M27-ORIG",
            "A12": "AP-M28-ORIG", "A13": "AP-M29-ORIG", "A15": "AP-M31-ORIG", "A16": "AP-M33-ORIG",
        }
        if row["id"] == "A14":
            proposal_source = by_source["AP-D30"]
            row["proposal"] = {"date": "2019-01-08T00:19:37.000Z", "precision": "second:observed_design_revision",
                               "url": proposal_source["url"], "source_ids": ["AP-D30"],
                               "date_kind": "직접 읽은 구체 Catalog 설계 v2. 상위 Hive 통합 필요는2018-10-09; 전체 최초 제안/사적 구상일은 미확인"}
        else:
            sid = original_mail[row["id"]]
            proposal_source = by_source[sid]
            row["proposal"] = {"date": proposal_source["published_or_version"].split(";")[0],
                               "precision": "second:public_message_header", "url": proposal_source["url"],
                               "source_ids": [sid], "date_kind": "직접 읽은 원 공개 제안 메일; 사적 최초 필요/전체 최초 공개일을 보증하지 않음"}
    elif row["stream"] == "rust":
        source_id = next(s for s in row["source_ids"] if s.startswith("RUST-F0"))
        row["proposal"] = {"date": row["originating_proposal_date"], "precision": "second:public_PR_created_at",
                           "url": by_source[source_id]["url"], "source_ids": [source_id],
                           "date_kind": "공개 PR 생성시각; 초안 commit author time/사적 최초필요와 별개"}
    if row["id"] == "A06":
        row["alternatives"][0]["availability_reference"] = "formal_decision_not_initial_proposal"
        row["alternatives"][0]["availability_timeline_note"] = (
            "최초안2019-03-22에는 최종 AAD 조건 미제공;2019-04-12 공급기능 병합은2019-04-30 문서결정 전. "
            "소비자1.0.0 고정 사용은2019-05-03 lockfile에서 확인. 최초안에 AAD 요구가 확정됐는지도 미확인.")
    if row["id"] == "B08":
        row["stream_final_choice"] = row["final_choice"]
        row["final_choice"] = "Path를 보존하다 JSON 출력 경계에서 JSONEncoder 호환 확장점 사용; 후속판에 추가한 YAML은 별도 자체 변환"
    row["date_interpretation"] = (
        "Public proposal creation, commit author time, current-comment metadata, and private first "
        "need/cognition are different. Missing revision history does not establish when the present "
        "wording first appeared. See precision/date_kind/unknowns and timeline.csv.")

# A cost absence remains an explicit row rather than disappearing from its denominator.
covered = {row["case_id"] for row in costs}
for case_id, decision in by_case.items():
    if case_id in covered:
        continue
    cost_id = "GLOBAL-COST-" + case_id + "-UNKNOWN"
    costs.append({
        "cost_id": cost_id, "case_id": case_id,
        "cost_kind": "researcher_counterfactual_unknown", "value": "", "unit": "unreported",
        "scope": "해당 선택의 실제 투입과 조기 소개로 줄일 비용: 미확인",
        "reported_by": "해당 수량을 보고한 결정자 기록을 찾지 못함", "reported_date": "",
        "url": decision["original_url"],
        "avoided_cost_evidence": "없음. 미보고를 0비용으로 처리하지 않음",
        "reused_work": "제안/기존 대안의 비교와 실제 유지 노동량은 별개이며 수량 미확인",
        "limitation": decision["minimum_next_record"],
        "stream": "global_audit", "original_cost_kind": "researcher_counterfactual_unknown",
        "original_unit": "unreported",
    })
    decision.setdefault("cost_ids", []).append(cost_id)

for row in costs:
    if row["cost_id"] == "BC06":
        row["reported_date_original"] = row["reported_date"]
        row["reported_date"] = "2019-05-16T10:01:22Z/2019-06-06T09:13:26Z"
        row["reported_date_precision"] = "comment creation-to-update interval; first wording unconfirmed"
        row["limitation"] += " 개별 댓글 created/updated 구간이며 현재 시간 진술의 최초 작성일은 미확인."
        row["avoided_cost_evidence"] = "button/div 표시를 이해한 별도 리뷰 문제이므로 inert 미인지·도입·철회 비용으로 귀속할 수 없음"
    elif row["cost_id"] == "BC02":
        row["scope_original"] = row["scope"]
        row["scope"] = "2018-10-05에 열린 WIP PR의 현재 Status 절이 회고하는 초기 코드베이스 작업; 정확한 작업일/문구 최초일 미확인"
        row["reported_date_original"] = row["reported_date"]
        row["reported_date"] = "current body of PR opened 2018-10-05T12:29:23Z; wording date unknown"
        row["reported_date_precision"] = "PR created time does not date current body wording"
        row["limitation"] += (
            " PR updated_at=2019-04-29T19:10:08Z는 객체 갱신 시각이다. 본문의 하루 진술이 "
            "2018-10-05에 이미 있었는지는 편집 이력 없이 확정하지 않음.")

write_json(BASE / "sources.json", sources)
(BASE / "decisions.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in decisions))
write_csv(BASE / "sampling.csv", sampling)
write_csv(BASE / "costs.csv", costs)

timeline = []
for decision in decisions:
    row = {"case_id": decision["id"], "sample": decision["sample"]}
    for field in ("need", "proposal", "first_public_implementation", "decision", "implementation"):
        value = decision.get(field, {})
        row[field + "_date"] = value.get("date") or "미확인"
        row[field + "_precision"] = value.get("precision") or "unknown"
        row[field + "_url"] = value.get("url") or ""
        row[field + "_scope"] = value.get("date_kind") or value.get("note") or value.get("scope") or value.get("summary") or ""
    row["originating_proposal_date"] = decision.get("originating_proposal_date") or ""
    row["awareness_records"] = json.dumps(decision.get("awareness", []), ensure_ascii=False)
    row["earliest_observed_code"] = json.dumps(decision.get("earliest_observed_code", decision.get("first_public_implementation", {})), ensure_ascii=False)
    row["later_release"] = json.dumps(decision.get("implementation", {}).get("later_release", {}), ensure_ascii=False)
    row["minimum_next_record"] = decision["minimum_next_record"]
    timeline.append(row)
write_csv(BASE / "timeline.csv", timeline)

A = [r for r in decisions if r["sample"] == "A"]
B = [r for r in decisions if r["sample"] == "B"]
counted = [r for r in sources if r["count_in_minimum"]]
source_counts = Counter(r["count_category"] for r in counted)
counts_by_stream = {}
for stream in (*STREAMS, "crossfield", "fixed_inputs"):
    group = [r for r in sources if r["stream"] == stream]
    counts_by_stream[stream] = {"ledger_rows": len(group), "counted": sum(r["count_in_minimum"] for r in group),
                               "categories": dict(Counter(r["count_category"] for r in group if r["count_in_minimum"]))}

stats = {
    "schema": "AF-RES-022/statistics-v1", "observation_window": ["2018-01-01", "2024-12-31"],
    "followup_cutoff_utc": "2026-11-22", "selection_freeze_commit": "00c2a14633e7503880f4aceb7c4909845298b3d7",
    "unit": "one team's one choice; multiple dependent documents do not create extra cases",
    "A": {
        "n": len(A), "by_family": dict(Counter(r["record_family"] for r in A)),
        "projects": sorted(set(r["project"] for r in A)),
        "screened_before_caps": 29, "excluded_before_caps": 5, "deferred_after_caps": 28,
        "inaccessible_selected_originals": 0,
        "strict_discovery_change": sum(r["strict_discovery_change"] for r in A),
        "strict_ids": [r["id"] for r in A if r["strict_discovery_change"]],
        "connected_chain": sum(r["connected_chain"] for r in A),
        "connected_chain_ids": [r["id"] for r in A if r["connected_chain"]],
        "initial_focal_known": audit["counts"]["baseline_known_count"],
        "initial_focal_unknown_ids": audit["counts"]["baseline_unknown_ids"],
        "available_awareness_completion_candidates": audit["counts"]["initial_awareness_completion_candidates_available"],
        "excluded_later_required_feature_ids": audit["counts"]["excluded_later_required_feature_ids"],
        "record_completion_scenarios": audit["counts"]["record_completion_scenarios"],
        "known_constraint_correction": audit["counts"]["known_solution_constraint_correction_and_execution"],
        "private_first_need_unknown": 24, "first_lifetime_cognition_unknown": 24,
        "first_public_code_unknown": sum(not r["first_public_implementation"].get("date") for r in A),
        "actual_scoped_execution_yes": audit["counts"]["actual_scoped_execution_yes"],
        "actual_scoped_execution_unknown_ids": audit["counts"]["actual_scoped_execution_unknown_ids"],
        "outcomes": dict(Counter(r["outcome"] for r in A)),
        "discovery_positives_promoted_from_date_proxy": 0,
        "direct_focal_solution_unawareness": 0,
        "reviewer_only_explicit_unaware_ids": ["A21"],
        "notes": "Not a random sample, population incidence, or causal effect. Public need/proposal dates are not private first need dates."
    },
    "B": {
        "n": len(B), "unique_additions": len(B), "linked_A_duplicates": 0,
        "source_families": {"github_discussion_or_pr": 8, "author_retrospective": 1},
        "candidate_url_rows": len([r for r in sampling if r["stream"] == "b"]),
        "candidate_access": dict(Counter(r["access"] for r in sampling if r["stream"] == "b")),
        "strict_discovery_change": sum(r["strict_discovery_change"] for r in B),
        "strict_ids": [r["id"] for r in B if r["strict_discovery_change"]],
        "connected_chain": sum(r["connected_chain"] for r in B),
        "connected_chain_ids": [r["id"] for r in B if r["connected_chain"]],
        "dated_example_only_ids": [r["id"] for r in B if r.get("dated_example_chain")],
        "direct_unaware_decision_actor_ids": [r["id"] for r in B if any(a["kind"] == "explicit_unaware" and a["role"] == "decision_maker" for a in r["awareness"])],
        "requester_only_unaware_ids": ["B04"],
        "late_feature_ids": ["B01", "B06"], "incompatible_existing_feature_ids": ["B02"],
        "outcomes": dict(Counter(r["outcome"] for r in B)),
        "notes": "Purposefully recruited discovery cases; never pooled with A for incidence."
    },
    "sources": {"ledger_rows": len(sources), "counted_unique_originals": len(counted),
                "excluded_or_auxiliary_rows": len(sources)-len(counted), "categories": dict(source_counts),
                "by_stream": counts_by_stream, "independent_case_count_is_not_document_count": True},
    "costs": {"rows": len(costs), "covered_unique_cases": len(set(r["case_id"] for r in costs)),
              "kinds": dict(Counter(r["cost_kind"] for r in costs)),
              "reported_numeric_cases": sorted(set(r["case_id"] for r in costs if r["value"])),
              "directly_measured_causal_savings_cases": 0, "author_estimated_saving_rows": 0,
              "aggregate_sum": None, "sum_reason": "units, scope and attribution differ; no measured early-link counterfactual"},
    "aspirational_targets": {
        "connected_chain_at_least_6": {"observed": sum(r["connected_chain"] for r in decisions), "target": 6,
                                       "ids": [r["id"] for r in decisions if r["connected_chain"]], "met": False},
        "late_discovery_production_self_retention_at_least_3": {"observed_strict": 0, "candidate_ids": ["B01", "B02", "B09"], "target": 3, "met": False}
    },
    "limitations": [
        "Unobserved awareness record completion is not a strict causal upper bound.",
        "Crossfield cases X-P1/X-P2/X-E1/X-E2 and supporting X-S1 are outside A/B.",
        "Same producer/repository release and review records are dependent evidence lineages.",
        "Exact private origins, historical deployment and labor savings remain unconfirmed."
    ]
}
write_json(BASE / "evidence/statistics.json", stats)

manifest = []
for relative in ["sources.json", "decisions.jsonl", "sampling.csv", "costs.csv", "timeline.csv", "evidence/statistics.json"]:
    path = BASE / relative
    manifest.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
write_json(BASE / "evidence/assembled-input-hashes.json", manifest)
print(json.dumps({"cases": len(decisions), "A": len(A), "B": len(B), "sources": len(sources),
                  "counted": len(counted), "categories": dict(source_counts), "cost_rows": len(costs)}, ensure_ascii=False))
