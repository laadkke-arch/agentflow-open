#!/usr/bin/env python3
"""Recheck AF-RES-026 bookkeeping without changing research inputs.

Run from the repository root, for example::

    python docs/workstreams/research/AF-RES-026/verify.py --require-report \
      --record evidence/verification.json

Relative --record paths are relative to this script's owned directory. A
repository-relative path already pointing inside that directory also works.
Only the requested receipt is written. No network requests, SQL executions,
Git mutations, or regeneration of the research data are performed.

PASS means that the recorded data satisfy these mechanical checks. It does
not prove full-text reading, historical authenticity, the correctness of the
human judgments, or a causal effect of the unsent I/C/Q messages. The receipt
records the LOCAL Git HEAD; remote exact-SHA readback remains a separate gate.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE_COMMIT = "b420fb7e1e01f4a366512fa71c0f507051aa6a19"
SEAL_COMMIT = "68fc97fadceb46f9945a71fcc53730e29f6c62bf"
CASE_IDS = {f"{family}{n:02d}" for family in "SPC" for n in range(1, 9)}
STRATEGIES = ("I", "C", "Q")
SEALED_FILES = ["initial.jsonl", "frozen-responses.jsonl", "frame.csv"] + [
    f"streams/{family}/{name}"
    for family in ("sqlite", "postgres", "curl")
    for name in ("initial.jsonl", "frozen-responses.jsonl")
]
SOURCE_FIELDS = (
    "id related_q case_ids url published_or_revised fixed_version checked_utc "
    "read_locations observed limitations producer lineage count_in_minimum "
    "count_reason kind"
).split()
ANALYSIS_BOOLS = (
    "original_confirmed strict_unexposed supplier_also_requester "
    "q_value_already_T0 q_new_author_value_strict "
    "q_completed_same_variable_direct_answer q_new_value_generous_sensitivity "
    "q_still_unconfirmed_after_window T0_original_goal_facts_sufficient "
    "T0_original_goal_facts_sufficient_with_declared_version_assumption "
    "candidate_change_from_new_author_value reported_progress_broad "
    "external_user_new_successful_execution supplier_new_development "
    "decision_acceptance_existing_workflow reported_failure_other_actual_intervention "
    "source_consultation_report"
).split()
ANALYSIS_INTS = (
    "actual_clarification_roundtrips_primary actual_clarification_roundtrips_technical_only "
    "implementation_conversation_extra_pairs candidate_count"
).split()
TABLE_HEADERS = [
    ["질문 ID·원판 시각", "최초 목적·필수 조건의 원문 URL·위치", "빠진 변수와 봉인한 질문",
     "실제 응답 주체·값·시점", "사용 또는 판정 변화", "미확인"],
    ["전략 I·C·Q", "전체·최초판 확정·직접 답 분모", "근거 있는 승인·오승인·보류",
     "실제 진전 보고·관측 창", "실제 왕복·대리 비용", "반례"],
    ["사례 ID", "최초판의 사용과 후보 URL", "추가 사실로 유지·변경된 제안",
     "당시 공식 근거 절", "필요한 근거 전부 인용 여부", "사용자 행동·대체 설명"],
    ["Q 번호·주장·적용 범위", "근거 원문 URL·정확한 절 또는 실행 영수증",
     "확인한 내용·분자·분모", "반례를 찾은 곳과 결과", "미확인·판단을 바꿀 최소 자료"],
]
WEAKNESS_HEADER = [
    "중요한 불일치·약점", "근거 ID·URL", "영향을 받는 결정",
    "다음 조사 질문·찾을 자료·최소 확인",
]


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def boolean(value):
    if isinstance(value, bool):
        return value
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"expected a Boolean, got {value!r}")


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no time-zone offset")
    return parsed.astimezone(timezone.utc)


def source_ids(value):
    return [item.strip() for item in re.split(r"[;|]", value) if item.strip()]


def compact(issues, limit=12):
    return {"issue_count": len(issues), "examples": issues[:limit]}


class Audit:
    def __init__(self):
        self.checks = []
        self.inputs = {}
        self.cache = {}
        self.head = None

    def check(self, name, passed, detail=None):
        self.checks.append({"check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    def issues(self, name, issues, detail=None):
        self.check(name, not issues, compact(issues) if issues else detail)

    def skip(self, name, detail):
        self.checks.append({"check": name, "status": "SKIP", "detail": detail})

    def section(self, name, function):
        try:
            function()
        except Exception as exc:
            self.check(name, False, {"error": type(exc).__name__, "message": str(exc)[:500]})

    def raw(self, relative):
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"input outside owned path: {relative}")
        key = path.relative_to(ROOT).as_posix()
        if key not in self.cache:
            raw = path.read_bytes()
            self.cache[key] = raw
            self.inputs[key] = sha256(raw)
        return self.cache[key]

    def text(self, name):
        return self.raw(name).decode("utf-8-sig")

    def json(self, name):
        return json.loads(self.text(name))

    def jsonl(self, name):
        return [json.loads(line) for line in self.text(name).splitlines() if line.strip()]

    def csv(self, name):
        return list(csv.DictReader(io.StringIO(self.text(name))))

    def core(self):
        self.initial_rows = self.jsonl("initial.jsonl")
        self.frozen_rows = self.jsonl("frozen-responses.jsonl")
        self.initial = {row["case_id"]: row for row in self.initial_rows}
        self.frozen = {row["case_id"]: row for row in self.frozen_rows}
        self.frame = self.csv("frame.csv")
        self.seal = self.json("evidence/t0-seal.json")
        self.sources = self.json("sources.json")
        self.source_map = {row["id"]: row for row in self.sources}
        self.analysis_rows = self.csv("analysis.csv")
        for row in self.analysis_rows:
            for key in ANALYSIS_BOOLS:
                row[key] = boolean(row[key])
            for key in ANALYSIS_INTS:
                row[key] = int(row[key])
        self.analysis = {row["case_id"]: row for row in self.analysis_rows}
        self.strategies = self.csv("strategy.csv")
        self.judgments = self.csv("judgments.csv")
        self.metrics = self.json("evidence/metrics.json")
        self.overrides = self.json("adjudication-overrides.json")
        self.pairs = self.json("evidence/actual-roundtrips.json")
        self.schema = self.json("schema.json")
        self.raw("verify.py")
        self.check("core_files_read", True, {"files": len(self.inputs)})

    def sample_and_seal(self):
        issues = []
        for label, rows in (("initial", self.initial_rows), ("frozen", self.frozen_rows),
                            ("analysis", self.analysis_rows)):
            ids = [row["case_id"] for row in rows]
            if len(ids) != 24 or set(ids) != CASE_IDS:
                issues.append(f"{label}: expected 24 distinct S/P/C01–08 IDs")
        families = Counter(row["family"] for row in self.initial_rows)
        if families != Counter({"S": 8, "P": 8, "C": 8}):
            issues.append(f"family distribution: {dict(families)}")
        selected = [row for row in self.frame if row["decision"] in ("selected", "included")]
        if len(self.frame) != 149 or len(selected) != 24 or {r["case_id"] for r in selected} != CASE_IDS:
            issues.append("frame must contain 149 ledger rows and 24 selected distinct cases")
        if len({row["frame_id"] for row in self.frame}) != len(self.frame):
            issues.append("frame_id values are not unique")
        self.issues("sample_frame", issues, {"cases": 24, "families": dict(families), "frame_rows": len(self.frame)})

        issues = []
        for name in SEALED_FILES:
            expected = self.seal["files"].get(name)
            if not expected or sha256(self.raw(name)) != expected:
                issues.append(f"sealed hash mismatch: {name}")
        self.issues("t0_nine_immutable_hashes", issues, {"checked_files": SEALED_FILES})
        self.skip("scope_worktree_hash", "SCOPE.md may contain postseal annotations; its current hash is deliberately not constrained.")

        issues = []
        exclusions = {row["case_id"] for row in self.seal["exposure_exclusions"]}
        exposed = {row["case_id"] for row in self.frozen_rows if row["followups_read_before_freeze"] is True}
        confirmed = {cid for cid, row in self.initial.items()
                     if row["original_version"]["status"] == "confirmed" and row["original_version"]["full_body_read"] is True}
        if confirmed != CASE_IDS or exclusions != {"S01"} or exposed != exclusions:
            issues.append("recorded originals/exposure exclusions disagree with the 24/23 design")
        for cid in CASE_IDS:
            if self.analysis[cid]["original_confirmed"] != (cid in confirmed):
                issues.append(f"{cid}: normalized original flag differs")
            if self.analysis[cid]["strict_unexposed"] != (cid not in exclusions):
                issues.append(f"{cid}: normalized exposure flag differs")
        for key, value in (("case_count", 24), ("strategy_message_count", 72), ("frame_rows", 149),
                           ("original_identity_and_full_text_observed", 24), ("strict_unexposed_cases", 23)):
            if self.seal.get(key) != value:
                issues.append(f"seal {key} differs from {value}")
        self.issues("recorded_originals_and_exposure", issues,
                    {"recorded_originals": len(confirmed), "strict_unexposed": len(CASE_IDS - exclusions),
                     "note": "Metadata consistency, not independent proof of server receipt or historical authenticity."})

    def frozen_messages(self):
        issues = []
        max_chars = 0
        for cid in sorted(CASE_IDS):
            initial, frozen = self.initial[cid], self.frozen[cid]
            for label, row, fields in (("initial", initial, self.schema["fields_initial"]),
                                       ("frozen", frozen, self.schema["fields_frozen"])):
                missing = set(fields) - row.keys()
                if missing:
                    issues.append(f"{cid} {label}: missing {sorted(missing)}")
            if not re.fullmatch(r"[0-9a-f]{64}", initial["input_sha256"]):
                issues.append(f"{cid}: invalid input SHA256")
            if initial["input_sha256"] != frozen["input_sha256"]:
                issues.append(f"{cid}: initial/frozen input hash mismatch")
            candidates = initial["candidate_uses"]
            if len(candidates) > 2 or {c["id"] for c in candidates} != set(frozen["candidate_ids"]):
                issues.append(f"{cid}: candidate IDs changed or exceed two")
            # A candidate may cite one principal source in initial.jsonl while
            # the frozen responses also cite contextual/negative evidence.
            # Extra source records are not extra candidate uses.
            if not {c["source_id"] for c in candidates}.issubset(set(frozen["candidate_source_ids"])):
                issues.append(f"{cid}: frozen sources omit a candidate's principal source")
            for source_id in frozen["candidate_source_ids"]:
                if source_id not in self.source_map:
                    issues.append(f"{cid}: unresolved frozen source {source_id}")
            if initial["frozen_question"] != frozen["Q"]:
                issues.append(f"{cid}: initial question and frozen Q differ")
            if not isinstance(frozen["followups_read_before_freeze"], bool):
                issues.append(f"{cid}: exposure field must be a Boolean")
            for strategy in STRATEGIES:
                message = frozen[strategy]
                if not isinstance(message, str) or not 0 < len(message) <= 300:
                    issues.append(f"{cid}/{strategy}: message must contain 1–300 Unicode code points")
                max_chars = max(max_chars, len(message))
                if len(re.findall(r"https?://[^\s]+", message)) > 2:
                    issues.append(f"{cid}/{strategy}: more than two candidate URLs")
        self.issues("frozen_72_messages", issues, {"messages": len(self.frozen_rows) * 3, "maximum_unicode_chars": max_chars})

    def source_ledger(self):
        issues = []
        ids = [source["id"] for source in self.sources]
        if len(ids) != len(set(ids)):
            issues.append("duplicate top-level source IDs")
        for source in self.sources:
            sid = source["id"]
            missing = set(SOURCE_FIELDS) - source.keys()
            if missing:
                issues.append(f"{sid}: missing fields {sorted(missing)}")
                continue
            if not isinstance(source["count_in_minimum"], bool):
                issues.append(f"{sid}: count_in_minimum is not a JSON Boolean")
            for field in SOURCE_FIELDS:
                if field not in ("related_q", "case_ids", "count_in_minimum") and not source[field]:
                    issues.append(f"{sid}: empty {field}")
            if not isinstance(source["case_ids"], list) or set(source["case_ids"]) - CASE_IDS:
                issues.append(f"{sid}: unknown case IDs")
            if not isinstance(source["related_q"], list) or set(source["related_q"]) - {f"Q{i}" for i in range(1, 9)}:
                issues.append(f"{sid}: unknown question IDs")
            if not re.match(r"https?://", source["url"]):
                issues.append(f"{sid}: no public HTTP(S) source URL")
            try:
                timestamp(source["checked_utc"])
            except (ValueError, TypeError):
                issues.append(f"{sid}: invalid checked_utc")
        counted = [s for s in self.sources if s["count_in_minimum"] is True]
        work_keys = [s.get("unique_work_key") for s in counted]
        if not all(work_keys) or len(set(work_keys)) != len(work_keys):
            issues.append("counted sources require distinct nonempty unique_work_key values")
        conversations = [s for s in counted if s["kind"] in ("conversation", "public_support_conversation")]
        conversation_cases = [cid for s in conversations for cid in s["case_ids"]]
        if len(conversations) != 24 or Counter(conversation_cases) != Counter(CASE_IDS):
            issues.append("conversation minimum must represent exactly the 24 selected cases once each")
        providers = [s for s in counted if s["kind"] in
                     ("provider_document", "provider_test", "provider_historical_document", "provider_source")]
        historical = []
        for source in providers:
            dated = re.search(r"\b(\d{4}-\d{2}-\d{2})", source["published_or_revised"])
            relevant = [self.initial[cid] for cid in source["case_ids"]] or self.initial_rows
            if dated and source["fixed_version"] and dated.group(1) <= min(r["submitted_utc"][:10] for r in relevant):
                historical.append(source["id"])
        cross = [s for s in counted if s["kind"] in ("cross_guideline", "cross_observation")]
        if len(counted) < 36 or len(historical) < 8 or len(cross) < 4:
            issues.append(f"minimum not met: total={len(counted)}, dated pre-T0 providers={len(historical)}, cross={len(cross)}")
        for prefix in ("X-L", "X-S"):
            domain = [s for s in cross if s["id"].startswith(prefix)]
            if len(domain) < 2 or not {"cross_guideline", "cross_observation"}.issubset({s["kind"] for s in domain}):
                issues.append(f"{prefix}: need a guideline and an observation from distinct counted works")
        self.issues("source_schema_and_minima", issues,
                    {"source_rows": len(self.sources), "counted_unique_works": len(counted), "conversation_works": len(conversations),
                     "dated_pre_T0_provider_works": len(historical), "cross_field_works": len(cross),
                     "note": "Dates and read locations are recorded assertions; the script does not certify reading."})

        recorded = self.json("evidence/source-counts.json")
        expected = {"frame_rows": len(self.frame), "frame_decisions": dict(Counter(r["decision"] for r in self.frame)),
                    "source_rows": len(self.sources), "unique_external_works_counted": len(counted),
                    "counted_by_kind": dict(Counter(s["kind"] for s in counted))}
        issues = [f"source-counts.{key} differs" for key, value in expected.items() if recorded.get(key) != value]
        if sorted(recorded.get("counted_source_ids", [])) != sorted(s["id"] for s in counted):
            issues.append("source-counts.counted_source_ids differs")
        self.issues("source_counts_recomputed", issues, expected)

    def judgment_pairs(self):
        issues = []
        grouped = defaultdict(list)
        supplementary = []
        for row in self.judgments:
            key = (row["case_id"], row["candidate_id"], row["condition_id"])
            grouped[key].append(row)
            cid = row["case_id"]
            if cid not in CASE_IDS:
                issues.append(f"unknown judgment case {cid}")
                continue
            allowed = set(self.frozen[cid]["candidate_ids"]) or {"NONE"}
            if row["candidate_id"] not in allowed:
                issues.append(f"{key}: candidate outside the frozen set")
            refs = source_ids(row["technical_source_ids"])
            if not refs or set(refs) - self.source_map.keys():
                issues.append(f"{key}/{row['timepoint']}: unresolved or empty technical source IDs {refs}")
            if not row["technical_url"] or not row["technical_locator"]:
                issues.append(f"{key}: missing technical URL/locator")
            if row["technical_verdict"] not in ("supported", "conflict", "unknown"):
                issues.append(f"{key}: unknown technical verdict")
            if row["action_verdict"] not in ("reported_progress", "reported_failure", "no_report", "unknown"):
                issues.append(f"{key}: unknown action verdict")
            if row["action_verdict"] in ("reported_progress", "reported_failure") and not (row["action_url"] and row["action_locator"]):
                issues.append(f"{key}: action claim lacks its own URL/locator")
            if row.get("actual_execution_by_researcher") not in (None, "", "False"):
                issues.append(f"{key}: unexpected researcher execution claim")
            supplemental = row["condition_kind"] in ("example_not_actual_query", "sensitivity_only", "newly_stated_option")
            if supplemental:
                if not row.get("adjudication_basis"):
                    issues.append(f"{key}: example/sensitivity row lacks explicit basis")
                if row["timepoint"] == "T0":
                    supplementary.append("/".join(key))
        for key, rows in grouped.items():
            if len(rows) != 2 or Counter(r["timepoint"] for r in rows) != Counter({"T0": 1, "T1": 1}):
                issues.append(f"{key}: requires exactly one T0 and one T1")
                continue
            for field in ("condition_kind", "candidate_version", "comparison_version", "actual_version_scope"):
                if rows[0].get(field, "") != rows[1].get(field, ""):
                    issues.append(f"{key}: T0/T1 {field} changed")
        if {row["case_id"] for row in self.judgments} != CASE_IDS:
            issues.append("not every case has judgment pairs")
        self.issues("judgments_sources_and_paired_conditions", issues,
                    {"rows": len(self.judgments), "paired_conditions": len(grouped),
                     "separately_marked_example_sensitivity_pairs": supplementary})

    def strategies_and_actions(self):
        issues = []
        keys = [(row["case_id"], row["strategy"]) for row in self.strategies]
        if len(keys) != 72 or set(keys) != {(cid, s) for cid in CASE_IDS for s in STRATEGIES}:
            issues.append("strategy.csv must have exactly one row per 24×I/C/Q")
        approved = {strategy: set(cases) for strategy, cases in
                    self.overrides["grounded_full_use_approval_cases_by_strategy"].items()}
        for row in self.strategies:
            cid, strategy = row["case_id"], row["strategy"]
            a, f = self.analysis[cid], self.frozen[cid]
            status = a[strategy + "_technical_status"]
            expected = {
                "denominator_all": True, "denominator_original_confirmed": a["original_confirmed"],
                "denominator_strict_unexposed": a["strict_unexposed"],
                "denominator_direct_answer": a["q_completed_same_variable_direct_answer"],
                "denominator_non_supplier": not a["supplier_also_requester"],
                "technical_status": status, "bounded_statement_or_route_supported": status == "supported_limited",
                "grounded_full_use_approval": cid in approved[strategy],
                "unsupported_approval": status == "unsupported_approval", "contradicted_approval": status == "contradicted_approval",
                "hold_for_current_goal": status == "hold" if strategy != "Q" else a["q_still_unconfirmed_after_window"],
                "T0_original_goal_facts_sufficient": a["T0_original_goal_facts_sufficient"],
                "Q_value_already_T0": a["q_value_already_T0"], "Q_new_author_value_strict": a["q_new_author_value_strict"],
                "Q_public_value_still_unconfirmed": a["q_still_unconfirmed_after_window"],
                "Q_new_value_generous_sensitivity": a["q_new_value_generous_sensitivity"],
                "candidate_change_from_new_author_value": a["candidate_change_from_new_author_value"],
                "reported_progress_broad": a["reported_progress_broad"],
                "external_user_new_successful_execution": a["external_user_new_successful_execution"],
                "supplier_new_development": a["supplier_new_development"],
                "same_fixed_candidate_execution_of_hypothetical_message": "not_applicable_message_never_sent",
                "actual_primary_roundtrips": a["actual_clarification_roundtrips_primary"],
                "actual_roundtrip_counts_shared_across_strategies": True,
                "expected_additional_roundtrips_lower_bound_if_answered": int(strategy == "Q"),
                "expected_wait_hours": "미확인", "input_sha256": f["input_sha256"],
                "message_unicode_chars": len(f[strategy]),
                "message_link_count": len(re.findall(r"https?://[^\s]+", f[strategy])),
            }
            for field, value in expected.items():
                observed = boolean(row[field]) if isinstance(value, bool) else int(row[field]) if isinstance(value, int) else row[field]
                if observed != value:
                    issues.append(f"{cid}/{strategy}: {field} differs")
            if strategy == "Q" and status != "question_not_approval":
                issues.append(f"{cid}: Q is not an approval")
        for cid, row in self.analysis.items():
            known, new = row["q_value_already_T0"], row["q_new_author_value_strict"]
            if known and new or row["q_still_unconfirmed_after_window"] != (not (known or new)):
                issues.append(f"{cid}: overlapping or incomplete strict Q-value classification")
            if row["q_completed_same_variable_direct_answer"] and not new:
                issues.append(f"{cid}: direct-answer denominator requires a completed new author value")
            if row["candidate_change_from_new_author_value"] and not new:
                issues.append(f"{cid}: candidate change attributed to absent new author value")
            if row["reported_progress_broad"] and not (row["progress_url"].startswith("http") and row["progress_kind"]):
                issues.append(f"{cid}: reported action lacks separate observation URL/kind")
            if any(row[k] for k in ("external_user_new_successful_execution", "supplier_new_development", "decision_acceptance_existing_workflow")) and not row["reported_progress_broad"]:
                issues.append(f"{cid}: progress subtype absent from broad observed progress")
        self.issues("strategies_and_unsent_observed_distinction", issues,
                    {"rows": len(self.strategies), "note": "Actual reports remain observational; hypothetical waiting and shared actual pairs are not added as treatment effects."})

    def roundtrips_and_metrics(self):
        issues = []
        primary, implementation = self.pairs["primary_pairs"], self.pairs["implementation_pairs"]
        pair_keys = []
        for pair in primary + implementation:
            request = pair.get("request_url", pair.get("request", ""))
            response = pair.get("answer_url", pair.get("response", ""))
            pair_keys.append((pair["case_id"], request, response))
            if pair["case_id"] not in CASE_IDS or not request.startswith("http") or not response.startswith("http"):
                issues.append("actual roundtrip lacks a selected case and two public message URLs")
            if not isinstance(pair["wait_hours"], (int, float)) or pair["wait_hours"] < 0:
                issues.append(f"{pair['case_id']}: invalid observed pair delay")
        if len(pair_keys) != len(set(pair_keys)):
            issues.append("duplicate actual pairs across primary and implementation windows")
        primary_counts = Counter(pair["case_id"] for pair in primary)
        implementation_counts = Counter(pair["case_id"] for pair in implementation)
        for cid, row in self.analysis.items():
            if row["actual_clarification_roundtrips_primary"] != primary_counts[cid]:
                issues.append(f"{cid}: normalized primary pair count differs")
            if row["implementation_conversation_extra_pairs"] != implementation_counts[cid]:
                issues.append(f"{cid}: normalized implementation pair count differs")
        self.issues("distinct_actual_message_pairs", issues,
                    {"primary_pairs": len(primary), "implementation_pairs_separate": len(implementation), "counted_once_not_three_times": True})

        rows = self.analysis_rows
        subsets = {
            "all_24": rows,
            "original_confirmed": [r for r in rows if r["original_confirmed"]],
            "strict_unexposed": [r for r in rows if r["strict_unexposed"]],
            "direct_answer_only": [r for r in rows if r["q_completed_same_variable_direct_answer"]],
            "non_supplier_requesters": [r for r in rows if not r["supplier_also_requester"]],
            "extra_original_corroboration": [r for r in rows if r["family"] in ("S", "C") or r["case_id"] in ("P04", "P05")],
        }
        issues = []
        if set(self.metrics["subsets"]) != set(subsets):
            issues.append("metric subset names differ from defined subsets")
        approved = {strategy: set(cases) for strategy, cases in
                    self.overrides["grounded_full_use_approval_cases_by_strategy"].items()}
        for name, subset in subsets.items():
            group = self.metrics["subsets"].get(name, {})
            ids = {r["case_id"] for r in subset}
            expected = {
                "denominator": len(subset), "case_ids": sorted(ids),
                "counts": {key: sum(r[key] for r in subset) for key in ANALYSIS_BOOLS},
                "strategy_dispositions": {s: dict(Counter(r["technical_status"] for r in self.strategies if r["strategy"] == s and r["case_id"] in ids)) for s in STRATEGIES},
                "grounded_full_use_approvals_by_strategy": {s: len(ids & approved[s]) for s in STRATEGIES},
                "actual_primary_roundtrip_pairs": sum(primary_counts[cid] for cid in ids),
                "zero_denominator_rates": "해당 없음" if not subset else "not_population_rate",
            }
            for field, value in expected.items():
                if group.get(field) != value:
                    issues.append(f"metrics.subsets.{name}.{field} differs")
        expected_top = {
            "cases": 24, "strategy_messages": 72,
            "direct_answer_denominator": sum(r["q_completed_same_variable_direct_answer"] for r in rows),
            "actual_distinct_primary_clarification_pairs": len(primary),
            "actual_implementation_clarification_pairs_separate": len(implementation),
            "actual_distinct_pairs_total": len(primary) + len(implementation),
            "actual_primary_pair_wait_hours": [p["wait_hours"] for p in primary],
        }
        for field, value in expected_top.items():
            if self.metrics.get(field) != value:
                issues.append(f"metrics.{field} differs")
        unknown = sorted(r["case_id"] for r in rows if not r["original_confirmed"])
        if sorted(self.metrics["unknown_original_extremes"]["unknown_cases"]) != unknown:
            issues.append("unknown-original extremes have the wrong case set")
        wide = sorted(r["case_id"] for r in rows if r["q_new_value_generous_sensitivity"])
        sensitivity = self.metrics["weak_author_value_sensitivity"]
        if sensitivity["case_ids"] != wide or sensitivity["max_if_all_three_weak_interpretations_accepted"] != len(wide):
            issues.append("weak-value sensitivity differs from its separate case set")
        if sensitivity["strict_new_values"] != sum(r["q_new_author_value_strict"] for r in rows):
            issues.append("sensitivity table's strict baseline differs")
        self.issues("all_metric_denominators_recomputed", issues,
                    {"subsets": {name: len(subset) for name, subset in subsets.items()}})

        counts = {key: sum(r[key] for r in rows) for key in ANALYSIS_BOOLS}
        target = {"original_confirmed": 24, "strict_unexposed": 23, "q_value_already_T0": 8,
                  "q_new_author_value_strict": 0, "q_completed_same_variable_direct_answer": 0,
                  "q_still_unconfirmed_after_window": 16, "candidate_change_from_new_author_value": 0}
        issues = [f"recorded conclusion {key}: expected {value}, got {counts[key]}"
                  for key, value in target.items() if counts[key] != value]
        expected_statuses = {"I": {"supported_limited": 13, "hold": 11},
                             "C": {"supported_limited": 14, "hold": 9, "unsupported_approval": 1},
                             "Q": {"question_not_approval": 24}}
        for strategy, expected in expected_statuses.items():
            actual = dict(Counter(r["technical_status"] for r in self.strategies if r["strategy"] == strategy))
            if actual != expected:
                issues.append(f"{strategy}: expected {expected}, got {actual}")
        for strategy, expected in (("I", 4), ("C", 2), ("Q", 0)):
            if len(approved[strategy]) != expected:
                issues.append(f"{strategy}: declared full-use approval count differs from {expected}")
        self.issues("declared_conclusions_regression", issues,
                    {"Q_values": {k: counts[k] for k in target}, "strategy_statuses": expected_statuses,
                     "note": "These are checks of declared coding outcomes, not independently inferred truth."})

    def report(self):
        content = self.text("RESULT.md")
        lines = content.splitlines()
        nonempty = [i for i, line in enumerate(lines) if line.strip()]
        issues = []
        if not nonempty or not lines[nonempty[0]].startswith("# "):
            issues.append("RESULT must begin with one level-one title")
        tables = markdown_tables(lines)
        if len(tables) < 5 or [t["header"] for t in tables[:4]] != TABLE_HEADERS:
            issues.append("the first four RESULT table headers are missing or out of required order")
        if len(nonempty) < 2 or not tables or tables[0]["start"] != nonempty[1]:
            issues.append("table 1 must start immediately below the title, ignoring blank lines")
        if not tables or tables[-1]["header"] != WEAKNESS_HEADER or len(tables[-1]["rows"]) != 3:
            issues.append("the final weaknesses table must have the exact header and exactly three data rows")
        elif nonempty[-1] != tables[-1]["end"]:
            issues.append("RESULT must end at the third weaknesses row")
        self.issues("report_required_tables", issues, {"table_count": len(tables), "final_weakness_rows": 3})

        self_check = self.text("SELF_CHECK.md")
        missing = [f"Q{i}" for i in range(1, 9) if not re.search(rf"(?<![A-Za-z0-9])Q{i}(?!\d)", self_check)]
        self.issues("self_check_q1_through_q8", missing, "Presence check only; counterevidence quality still needs review.")
        acceptance = self.json("evidence/acceptance-evidence.json")
        issues = []
        if not isinstance(acceptance, list) or not acceptance:
            issues.append("acceptance evidence must be a nonempty array")
        else:
            conditions = []
            for number, row in enumerate(acceptance, 1):
                if not isinstance(row, dict) or not {"condition", "met", "evidence", "note"}.issubset(row):
                    issues.append(f"acceptance row {number}: missing required fields")
                    continue
                conditions.append(row["condition"])
                if not isinstance(row["condition"], str) or not row["condition"].strip():
                    issues.append(f"acceptance row {number}: empty condition")
                if not isinstance(row["met"], bool):
                    issues.append(f"acceptance row {number}: met must be a JSON Boolean")
                if not isinstance(row["evidence"], (str, list, dict)) or not row["evidence"]:
                    issues.append(f"acceptance row {number}: missing evidence reference")
                if not isinstance(row["note"], str) or (row["met"] is False and not row["note"].strip()):
                    issues.append(f"acceptance row {number}: an unmet condition needs a note")
            if len(conditions) != len(set(conditions)):
                issues.append("duplicate acceptance condition names")
        self.issues("acceptance_evidence_schema", issues,
                    {"conditions": len(acceptance), "declared_unmet": sum(r.get("met") is False for r in acceptance),
                     "note": "A declared gap does not itself invalidate a correctly recorded WITH_GAPS handoff."})

    def git_ownership(self, base):
        def git(*arguments):
            return subprocess.run(["git", "-C", str(ROOT), *arguments], capture_output=True, timeout=20, check=False)

        probe = git("rev-parse", "--show-toplevel")
        if probe.returncode:
            self.skip("git_owned_path", "No local Git worktree; inspect remote commit changed paths separately.")
            return
        repo = Path(probe.stdout.decode().strip()).resolve()
        owned = ROOT.relative_to(repo).as_posix() + "/"
        head = git("rev-parse", "HEAD")
        self.head = head.stdout.decode().strip() if head.returncode == 0 else None
        diff = git("diff", "--name-only", "--no-relative", "-z", base, "--")
        untracked = git("ls-files", "--others", "--exclude-standard", "--full-name", "-z")
        if diff.returncode or untracked.returncode:
            self.skip("git_owned_path", f"Cannot compare the available local worktree with {base}; remote ownership check remains required.")
        else:
            paths = {p.decode("utf-8", errors="replace") for p in (diff.stdout + untracked.stdout).split(b"\0") if p}
            outside = sorted(path for path in paths if not path.startswith(owned))
            self.issues("git_owned_path", outside,
                        {"base": base, "local_head": self.head, "changed_or_untracked_files": len(paths), "owned_path": owned})
        historical = git("show", f"{SEAL_COMMIT}:{owned}evidence/t0-seal.json")
        if historical.returncode:
            self.skip("t0_seal_local_commit_copy", "The known remote seal commit is not present locally; remote readback remains separate.")
        else:
            self.check("t0_seal_local_commit_copy", sha256(historical.stdout) == sha256(self.raw("evidence/t0-seal.json")),
                       {"seal_commit": SEAL_COMMIT, "note": "Local object comparison; not a new remote verification."})

    def stable_inputs(self):
        changed = [name for name, expected in self.inputs.items() if sha256((ROOT / name).read_bytes()) != expected]
        self.issues("input_files_stable_during_run", changed, {"hashed_inputs": len(self.inputs)})


def table_cells(line):
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|"):
        stripped = stripped[:-1]
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", stripped)]


def markdown_tables(lines):
    tables, index, fenced = [], 0, False
    while index < len(lines) - 1:
        if lines[index].lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            index += 1
            continue
        cells = table_cells(lines[index + 1])
        separator = cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)
        if not fenced and "|" in lines[index] and separator:
            start = index
            header = table_cells(lines[index])
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip() and "|" in lines[index] and not lines[index].lstrip().startswith(("```", "~~~")):
                rows.append(table_cells(lines[index]))
                index += 1
            tables.append({"start": start, "end": index - 1, "header": header, "rows": rows})
        else:
            index += 1
    return tables


def receipt_path(argument):
    supplied = Path(argument)
    if supplied.is_absolute():
        path = supplied.resolve()
    elif (Path.cwd() / supplied).resolve().is_relative_to(ROOT):
        path = (Path.cwd() / supplied).resolve()
    else:
        path = (ROOT / supplied).resolve()
    if not path.is_relative_to(ROOT) or path == ROOT:
        raise ValueError("--record must name a file inside docs/workstreams/research/AF-RES-026/")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--require-report", action="store_true", help="also require RESULT, SELF_CHECK and acceptance-evidence schema")
    parser.add_argument("--record", metavar="PATH", help="write the execution receipt only, inside the owned path")
    parser.add_argument("--base", default=BASE_COMMIT, help="local Git base for owned-path comparison")
    args = parser.parse_args()
    try:
        destination = receipt_path(args.record) if args.record else None
    except ValueError as exc:
        parser.error(str(exc))
    started = datetime.now(timezone.utc).isoformat()
    audit = Audit()
    audit.section("core_files_read", audit.core)
    for name, method in (("sample_and_seal", audit.sample_and_seal), ("frozen_messages", audit.frozen_messages),
                         ("source_ledger", audit.source_ledger), ("judgment_pairs", audit.judgment_pairs),
                         ("strategies_and_actions", audit.strategies_and_actions),
                         ("roundtrips_and_metrics", audit.roundtrips_and_metrics)):
        audit.section(name, method)
    if args.require_report:
        audit.section("report_requirements", audit.report)
    audit.section("git_metadata", lambda: audit.git_ownership(args.base))
    audit.section("stable_inputs", audit.stable_inputs)
    if destination and destination.relative_to(ROOT).as_posix() in audit.inputs:
        audit.check("receipt_destination", False, "The receipt cannot overwrite an input file.")
        destination = None
    exit_code = int(any(check["status"] == "FAIL" for check in audit.checks))
    if destination:
        receipt = {"executed_utc": started, "command": [sys.executable, *sys.argv], "head": audit.head,
                   "input_sha256": dict(sorted(audit.inputs.items())), "checks": audit.checks, "exit_code": exit_code}
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            audit.check("receipt_write", False, f"{type(exc).__name__}: {exc}")
            exit_code = 1
    for check in audit.checks:
        print(f"{check['status']:4} {check['check']}")
        if check["status"] == "FAIL":
            print("     " + json.dumps(check["detail"], ensure_ascii=False))
    totals = Counter(check["status"] for check in audit.checks)
    print(f"Checks: {totals['PASS']} PASS, {totals['FAIL']} FAIL, {totals['SKIP']} SKIP; exit {exit_code}.")
    print("Mechanical consistency only: no certification of full-text reading, historical truth, or causal strategy effects.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
