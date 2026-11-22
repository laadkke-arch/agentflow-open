"""Normalize the three readers' recorded judgments and reproduce denominators.

This program is bookkeeping. It does not infer truth from keywords, conduct
an experiment, or turn missing author reports into failures. Explicit editorial
decisions are recorded in adjudication-overrides.json and source-level audits.
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def jsonl(name):
    return [json.loads(line) for line in (ROOT / name).read_text(encoding="utf-8").splitlines() if line.strip()]


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def csvout(name, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                             for key, value in row.items()})


def first(row, keys, default=None):
    return next((row[key] for key in keys if key in row), default)


def main():
    initials = {row["case_id"]: row for row in jsonl("initial.jsonl")}
    frozen = {row["case_id"]: row for row in jsonl("frozen-responses.jsonl")}
    cases = jsonl("case-analysis.jsonl")
    assert len(cases) == 24 and set(initials) == {r["case_id"] for r in cases}
    overrides = json.loads((ROOT / "adjudication-overrides.json").read_text(encoding="utf-8"))
    pg_cost = json.loads((ROOT / "streams/postgres/clarification-cost-audit.json").read_text(encoding="utf-8"))
    approved = {strategy: set(ids) for strategy, ids in
                overrides["grounded_full_use_approval_cases_by_strategy"].items()}
    wide = set(overrides["generous_new_value_sensitivity_cases"])
    rows, strategies, all_pairs, implementation_pairs = [], [], [], []
    for case in cases:
        cid = case["case_id"]
        family = cid[0]
        src = case.get("strategies", case)
        known = bool(first(case, ["q_value_already_available_in_T0", "q_value_known_before_followups", "q_value_known_in_T0"], False))
        new = bool(first(case, ["q_value_recovered_strict", "q_new_author_value_observed", "q_value_fill_eligible"], False))
        direct = bool(first(case, ["q_actual_same_variable_question_and_direct_answer", "q_same_variable_asked_in_actual_thread"], False))
        # A question having been asked is not by itself a completed direct answer.
        direct = direct and new
        whole = bool(first(case, ["T0_facts_sufficient_for_entire_original_goal", "t0_original_goal_facts_sufficient_without_version_assumption", "T0_original_goal_fully_sufficient"], False))
        whole_version = bool(first(case, ["t0_original_goal_facts_sufficient_under_stated_candidate_version"], whole))
        change = bool(first(case, ["proposal_changed_because_of_new_Q_value", "new_author_information_changes_candidate_verdict", "technical_fitness_changed_by_eligible_new_author_fact"], False))
        progress = bool(case.get("actual_author_reports_progress", False))
        kind = first(case, ["actual_progress_kind", "actual_author_progress_kind"], "none_observed")
        progress_url = first(case, ["actual_author_reports_progress_url", "actual_author_progress_url"], "") or ""
        roundtrip = case.get("actual_clarification_roundtrips", 0)
        if isinstance(roundtrip, dict):
            pair_count = roundtrip["count"]
            pairs = roundtrip.get("pairs", [])
            technical_pairs = roundtrip.get("strict_technical_input_only_count", pair_count)
        else:
            pair_count = roundtrip
            pairs = case.get("actual_clarification_pairs", [])
            technical_pairs = pair_count
        if family == "P":
            # P originally counted only the frozen variable; use the later
            # audit of all nine actual response pairs for the common definition.
            audited = [pair for pair in pg_cost["pairs"] if pair["case_id"] == cid and pair["counted_clarification_roundtrip"]]
            pair_count = len(audited)
            pairs = [{"request_url": pair["respondent_url"], "answer_url": pair["author_url"],
                      "wait_hours": pair["calendar_hours"], "same_as_frozen_variable": pair["same_frozen_variable"]} for pair in audited]
            technical_pairs = pair_count
        assert pair_count == len(pairs) or pair_count == 0, (cid, "pair records")
        all_pairs.extend({"case_id": cid, **pair, "section": "primary_conversation"} for pair in pairs)
        if case.get("implementation_conversation_extra_roundtrip"):
            implementation_pairs.append({"case_id": cid, **case["implementation_conversation_extra_roundtrip"]})
        semantic = overrides.get("case_overrides", {}).get(cid, {})
        if "strict_new_author_value" in semantic:
            new = semantic["strict_new_author_value"]
        if "strict_candidate_change_from_new_author_value" in semantic:
            change = semantic["strict_candidate_change_from_new_author_value"]
        row = {
            "case_id": cid, "family": family,
            "original_confirmed": initials[cid]["original_version"]["status"] == "confirmed",
            "strict_unexposed": cid != "S01",
            "supplier_also_requester": cid in ("C06", "C07"),
            "q_value_already_T0": known, "q_new_author_value_strict": new,
            "q_completed_same_variable_direct_answer": direct,
            "q_new_value_generous_sensitivity": cid in wide,
            "q_value_status": case["q_variable_status"],
            "q_still_unconfirmed_after_window": not (known or new),
            "T0_original_goal_facts_sufficient": whole,
            "T0_original_goal_facts_sufficient_with_declared_version_assumption": whole_version,
            "candidate_change_from_new_author_value": change,
            "reported_progress_broad": progress, "progress_kind": kind, "progress_url": progress_url,
            "external_user_new_successful_execution": cid == "S01",
            "supplier_new_development": cid == "C06",
            "decision_acceptance_existing_workflow": cid == "C05",
            "reported_failure_other_actual_intervention": bool(case.get("actual_author_reports_failure", False)),
            "source_consultation_report": bool(case.get("actual_author_reports_source_consultation", False)),
            "actual_clarification_roundtrips_primary": pair_count,
            "actual_clarification_roundtrips_technical_only": technical_pairs,
            "implementation_conversation_extra_pairs": int(bool(case.get("implementation_conversation_extra_roundtrip"))),
            "candidate_count": len(initials[cid]["candidate_uses"]),
            "root_url": initials[cid]["root_url"], "submitted_utc": initials[cid]["submitted_utc"],
            "adjudication_note": semantic.get("note", "계열 판독의 제한된 주장과 원 목표 범위를 분리; 자기 점검"),
        }
        for strategy in ("I", "C", "Q"):
            status = src[strategy].get("technical_status", "question_not_approval") if strategy != "Q" else "question_not_approval"
            srow = {"case_id": cid, "strategy": strategy,
                    "denominator_all": True, "denominator_original_confirmed": row["original_confirmed"],
                    "denominator_strict_unexposed": row["strict_unexposed"],
                    "denominator_direct_answer": direct,
                    "denominator_non_supplier": not row["supplier_also_requester"],
                    "technical_status": status,
                    "bounded_statement_or_route_supported": status == "supported_limited",
                    "grounded_full_use_approval": cid in approved.get(strategy, set()),
                    "unsupported_approval": status == "unsupported_approval",
                    "contradicted_approval": status == "contradicted_approval",
                    "hold_for_current_goal": status == "hold" if strategy != "Q" else not (known or new),
                    "T0_original_goal_facts_sufficient": whole,
                    "Q_value_already_T0": known, "Q_new_author_value_strict": new,
                    "Q_public_value_still_unconfirmed": not (known or new),
                    "Q_new_value_generous_sensitivity": cid in wide,
                    "candidate_change_from_new_author_value": change,
                    "reported_progress_broad": progress,
                    "external_user_new_successful_execution": row["external_user_new_successful_execution"],
                    "supplier_new_development": row["supplier_new_development"],
                    "same_fixed_candidate_execution_of_hypothetical_message": "not_applicable_message_never_sent",
                    "actual_primary_roundtrips": pair_count,
                    "actual_roundtrip_counts_shared_across_strategies": True,
                    "expected_additional_roundtrips_lower_bound_if_answered": 1 if strategy == "Q" else 0,
                    "expected_wait_hours": "미확인",
                    "message_link_count": len(re.findall(r"https?://[^\s]+", frozen[cid][strategy])),
                    "message_unicode_chars": len(frozen[cid][strategy]),
                    "input_sha256": frozen[cid]["input_sha256"],
                    "source_case_record": "case-analysis.jsonl#" + cid,
                    "note": "미전송 문구의 정적 대조. 전략별 실제 진행/비용의 인과 차이가 아님."}
            strategies.append(srow)
            row[strategy + "_technical_status"] = status
        rows.append(row)

    csvout("analysis.csv", rows)
    csvout("strategy.csv", strategies)
    dump("evidence/actual-roundtrips.json", {"primary_pairs": all_pairs, "implementation_pairs": implementation_pairs,
        "not_frozen_Q": True, "note": "C06 implementation pair is also within30 days but displayed in the separate implementation column; count distinct pairs once."})
    subsets = {
        "all_24": rows,
        "original_confirmed": [r for r in rows if r["original_confirmed"]],
        "strict_unexposed": [r for r in rows if r["strict_unexposed"]],
        "direct_answer_only": [r for r in rows if r["q_completed_same_variable_direct_answer"]],
        "non_supplier_requesters": [r for r in rows if not r["supplier_also_requester"]],
        "extra_original_corroboration": [r for r in rows if r["family"] in ("S", "C") or r["case_id"] in ("P04", "P05")],
    }
    aggregate = {}
    bool_fields = [key for key, value in rows[0].items() if isinstance(value, bool)]
    for name, subset in subsets.items():
        ids = {r["case_id"] for r in subset}
        result = {"denominator": len(subset), "case_ids": sorted(ids),
                  "counts": {key: sum(r[key] for r in subset) for key in bool_fields},
                  "strategy_dispositions": {strategy: dict(Counter(r["technical_status"] for r in strategies if r["strategy"] == strategy and r["case_id"] in ids)) for strategy in ("I", "C", "Q")},
                  "grounded_full_use_approvals_by_strategy": {strategy: len(ids & approved.get(strategy, set())) for strategy in ("I", "C", "Q")},
                  "actual_primary_roundtrip_pairs": sum(r["actual_clarification_roundtrips_primary"] for r in subset),
                  "zero_denominator_rates": "해당 없음" if not subset else "not_population_rate"}
        aggregate[name] = result
    metric = {
        "cases": 24, "strategy_messages": len(strategies), "subsets": aggregate,
        "direct_answer_denominator": sum(r["q_completed_same_variable_direct_answer"] for r in rows),
        "actual_distinct_primary_clarification_pairs": len(all_pairs),
        "actual_implementation_clarification_pairs_separate": len(implementation_pairs),
        "actual_distinct_pairs_total": len(all_pairs) + len(implementation_pairs),
        "actual_primary_pair_wait_hours": [r["wait_hours"] for r in all_pairs],
        "unknown_original_extremes": {"unknown_cases": [r["case_id"] for r in rows if not r["original_confirmed"]],
            "note": "원판 미확인 0이므로 전부 성립/불성립 양끝은 동일. S01 노출 민감도와 구별."},
        "weak_author_value_sensitivity": {"strict_new_values": sum(r["q_new_author_value_strict"] for r in rows),
            "max_if_all_three_weak_interpretations_accepted": len(wide), "case_ids": sorted(wide),
            "candidate_change_upper_if_P03_local_reading_accepted": 1,
            "note": "진실의 통계적 구간 아님. P03 지시대상, S04 상충 주장, C05 부분 선호를 넓게 읽는 코딩 민감도."},
        "source_counts_file": "evidence/source-counts.json",
        "notes": ["Q의 8개 기존 값은 질문의 성과가 아니라 재질문 반례다.",
                  "전략별 제한 판정(I13/C14)과 전체 사용 승인(I4/C2)을 혼합하지 않는다. S08 C에는 원래 NOT NULL 조건이 빠져 전체 승인에서 제외한다.",
                  "진전3은 S01 자가성공/C05 수용/C06 공급자개발이며 서로 다른 관측이다.",
                  "기술 오승인0은 미전송 문구의 확인된 충돌0; P04/C 근거부족1을 숨기지 않는다."]}
    dump("evidence/metrics.json", metric)
    summary_rows = []
    for name, group in aggregate.items():
        ids = set(group["case_ids"])
        for strategy in ("I", "C", "Q"):
            selected = [row for row in strategies if row["case_id"] in ids and row["strategy"] == strategy]
            summary_rows.append({"subset": name, "strategy": strategy, "denominator": len(selected),
                "limited_support": sum(r["bounded_statement_or_route_supported"] for r in selected),
                "grounded_full_use_approval": sum(r["grounded_full_use_approval"] for r in selected),
                "unsupported_approval": sum(r["unsupported_approval"] for r in selected),
                "contradicted_approval": sum(r["contradicted_approval"] for r in selected),
                "hold_or_unfilled_Q_value": sum(r["hold_for_current_goal"] for r in selected),
                "already_T0_Q_value": sum(r["Q_value_already_T0"] for r in selected),
                "strict_new_Q_value": sum(r["Q_new_author_value_strict"] for r in selected),
                "rate_note": "해당 없음(분모0)" if not selected else "기술 통계; 모집단/인과 효과 추정 아님"})
    csvout("strategy-summary.csv", summary_rows)
    print(json.dumps({"cases": len(rows), "strategy_rows": len(strategies), "subsets": {name: result["denominator"] for name, result in aggregate.items()},
                      "strict_new_Q_values": metric["weak_author_value_sensitivity"]["strict_new_values"]}, indent=2))


if __name__ == "__main__":
    main()
