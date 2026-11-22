#!/usr/bin/env python3
"""Rebuild AF-RES-037 analytical ledgers. No network or writes outside owned_path.

The CSVs are research data exports, not formatted workbooks. Raw stream records
remain intact; corrections, exclusions and interpretive flags remain explicit.
Run from any directory with Python 3: python -B <this file> [--check].
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
STREAMS = ("csswg", "gdal", "b", "root")
REQUIRED_SOURCE = (
    "source_id original_url pinned_url_or_version publisher published_or_event_date "
    "checked_utc locator source_kind verified_fact limitation question_ids case_ids "
    "duplicate_group counted"
).split()


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def serial(value):
    if value is None:
        return "미확인"
    if isinstance(value, (dict, list, bool)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def csv_text(rows, columns):
    target = io.StringIO(newline="")
    writer = csv.DictWriter(target, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: serial(row.get(k, "미확인")) for k in columns})
    return target.getvalue()


def category(row):
    old = row.get("count_category", "")
    kind = row["source_kind"]
    if old in ("A_initial_recipient", "A_initial_receiver"):
        return "A_initial"
    if kind == "donor_rule":
        return "donor_rule_or_design"
    if old in ("independent_counter", "independent_counterrecord") or kind == "independent_counterrecord":
        return "independent_counterrecord"
    if old in ("recipient_followup", "receiver_followup", "recipient_implementation_test", "recipient_decision"):
        # A font archive already predates the source-first retrospective essay.
        if row["source_id"] == "B-S32":
            return "recipient_antecedent_additional"
        return "recipient_followup"
    if old == "recipient_implementation_antecedent":
        return "recipient_antecedent_additional"
    if kind == "B_initial_primary":
        return "B_initial_additional"
    if old == "recipient_initial":
        return "recipient_baseline_additional"
    return "uncounted"


def source_rows():
    rows = []
    seen_ids = set()
    counted_groups = {}
    corrections = read_json("streams/csswg/source-corrections.json")
    for stream in STREAMS:
        path = f"streams/{stream}/sources.jsonl"
        for line_no, line in enumerate((ROOT / path).read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            missing = set(REQUIRED_SOURCE) - set(row)
            assert not missing, (path, line_no, missing)
            sid = row["source_id"]
            assert sid not in seen_ids, sid
            seen_ids.add(sid)
            row["stream_record"] = f"{path}:{line_no}"
            row["raw_duplicate_group"] = row["duplicate_group"]
            row["duplicate_group"] = row["duplicate_group"].casefold().strip()
            row["raw_counted"] = row["counted"]
            row["raw_count_category"] = row.get("count_category", "미확인")
            row["count_category"] = category(row)
            if sid in corrections:
                correction = corrections[sid]
                assert row[correction["field"]] == correction["original"]
                row["applied_correction"] = correction
                row[correction["field"]] = correction["corrected"]
            if sid in ("B-S21", "B-S22"):
                row["duplicate_group"] = "gdal-gmljp2-axis-correction2008"
                row["work_group_correction"] = "독립 검토 후 동일 Trac2131 변경의 연속 시험13569/코드13570을 보수적으로 한 작품 처리; 원장50→49, 사건12→12. 원 B 원장값 보존."
                if sid == "B-S22":
                    row["counted"] = False
            if row["counted"]:
                assert row["count_category"] != "uncounted", sid
                group = row["duplicate_group"]
                assert group not in counted_groups, (sid, counted_groups.get(group), group)
                counted_groups[group] = sid
            rows.append(row)
    # Cross-stream aliases are not independent works.
    aliases = {"lilypond-essay": "lilypond-essay", "gdal-rfc20": "gdal-rfc20"}
    for row in rows:
        row["duplicate_group"] = aliases.get(row["duplicate_group"], row["duplicate_group"])
    supplement_path = "streams/review-counts/countertype4.json"
    if (ROOT / supplement_path).exists():
        supplement = read_json(supplement_path)
        for index, raw in enumerate(supplement["new_sources"]):
            row = dict(raw)
            assert not (set(REQUIRED_SOURCE) - set(row))
            assert row["source_id"] not in seen_ids
            seen_ids.add(row["source_id"])
            assert row["counted"] is False
            row["stream_record"] = f"{supplement_path}:new_sources[{index}]"
            row["raw_duplicate_group"] = row["duplicate_group"]
            row["duplicate_group"] = row["duplicate_group"].casefold().strip()
            row["raw_counted"] = False
            row["raw_count_category"] = row.get("count_category", "미확인")
            row["count_category"] = "uncounted"
            rows.append(row)
    return rows


def frame_rows():
    rows = []
    for raw in read_json("streams/csswg/frame.json"):
        rows.append(dict(
            frame_id=f"A-CSS-{raw['rank']:02d}", stratum="A", registry="CSSWG",
            query_or_range=raw["registry_query"], language="English",
            ordering=raw["ordering"], rank=raw["rank"], number=raw["number"],
            created_or_search_utc=raw["created_utc"], url=raw["original_url"],
            title=raw["observed_title"], status=raw["status"], case_id=raw.get("case_id") or "해당 없음",
            selected=raw["status"] == "included", reason=raw.get("reason", "미확인"),
            initial_url=raw.get("initial_url", "미확인"), initial_version=raw.get("initial_version", "미심사"),
            duplicate_of=raw.get("duplicate_of", "미확인"),
            title_provider_exposed=raw.get("title_provider_exposed", "미심사"),
            initial_sources=raw.get("initial_source_named", "미심사"),
            outcome_exposure=raw.get("later_outcome_exposure_before_freeze", "미심사"),
            exposure_note=raw.get("exposure_note", "미심사"),
            counts_toward_sampling_cap=True, raw_record_json=raw,
        ))
    for raw in read_json("streams/gdal/frame.json"):
        selected = raw["disposition"] == "selected"
        in_period = selected or raw["disposition"] == "placeholder_not_proposal"
        rows.append(dict(
            frame_id=raw["screen_row"], stratum="A", registry="GDAL numbered RFC",
            query_or_range="2018-01-01..2024-12-31; first substantive numbered proposal; preperiod boundary separately retained",
            language="English", ordering="first substantive proposal date asc, RFC number asc",
            rank=raw.get("rank_in_eligible_prefix") or "해당 없음", number=raw["registry_number"],
            created_or_search_utc=raw["created_utc"], url=raw["initial_url"],
            title=raw.get("title", raw["screen_row"]), status=raw["disposition"],
            case_id=raw.get("case_id") or "해당 없음", selected=selected, reason=raw["reason"],
            initial_url=raw["initial_url"], initial_version=raw["initial_version"],
            duplicate_of=raw["duplicate_of"], title_provider_exposed=raw.get("title_provider_exposed"),
            initial_sources=raw.get("source_name_in_initial", []), outcome_exposure=raw["outcome_visibility"],
            exposure_note=raw.get("boundary_amendment", "현재 목록/검색 metadata 노출; 선정에 사용하지 않음"),
            counts_toward_sampling_cap=in_period, raw_record_json=raw,
        ))
    b = read_json("streams/b/frame.json")
    for query in b["queries"]:
        for raw in query["retained_first10"] + query["remaining_returned_metadata"]:
            selected = raw.get("status") in ("selected", "selected_with_access_gap")
            rows.append(dict(
                frame_id=raw.get("frame_id", f"{query['query_id']}-overflow-{raw['rank']:02d}"),
                stratum="B", registry=query["field"], query_or_range=query["query"],
                language=query["language"], ordering=query["requested_sort"], rank=raw["rank"], number="해당 없음",
                created_or_search_utc=query["performed_utc_interval"], url=raw["url"],
                title=raw["title"], status=raw["status"], case_id=raw.get("case_id") or "해당 없음", selected=selected,
                reason=raw.get("reason", "고정 최초10 밖; 본문 미심사"),
                initial_url=raw["url"], initial_version="최초 제안판 여부는 chains.csv; 검색 결과 순위의 최초 열람",
                duplicate_of=(raw.get("reason") if raw.get("status") == "duplicate" else "원 사건 기준 중복 없음/미심사"),
                title_provider_exposed="출처 명시 경로", initial_sources="chains.csv 또는 미심사",
                outcome_exposure="B는 출처·회고가 보이는 탐색; A의 결말 비노출 표본 아님",
                exposure_note=b["visibility_limitations"],
                counts_toward_sampling_cap=raw["rank"] <= 10, raw_record_json={"query_id": query["query_id"], **raw},
            ))
    return rows


def evidence_refs(value):
    refs = set()
    if isinstance(value, dict):
        for item in value.values():
            refs.update(evidence_refs(item))
    elif isinstance(value, list):
        for item in value:
            refs.update(evidence_refs(item))
    elif isinstance(value, str):
        refs.update(re.findall(r"\b(?:CSS-\d{3}|GDAL-(?:M\d+|C[A-Z0-9]+|V[\d-]+|P\d+|H\d+|\d{3})|B-S\d+|ROOT-(?:P\d+|C\d+|AUX\d+|META\d+|F\d+))\b", value))
    return refs


def case_rows(sources):
    decisions = read_json("evidence/case-decisions.json")
    initial = {}
    followups = {}
    for stream in ("csswg", "gdal", "b"):
        for row in read_json(f"streams/{stream}/initial.json"):
            initial[row["case_id"]] = row
        rows = read_json(f"streams/{stream}/followup.json")
        rows = rows["cases"] if isinstance(rows, dict) else rows
        for row in rows:
            followups[row["case_id"]] = row
    source_ids = {r["source_id"] for r in sources}
    chains = []
    judgments = []
    for decision in decisions:
        case_id = decision["case_id"]
        before = initial[case_id]
        after = followups[case_id]
        refs = sorted(set(decision["evidence_ids"]) | evidence_refs(after))
        assert not (set(refs) - source_ids), (case_id, set(refs) - source_ids)
        mapping = after.get("objects_authority", after.get("object_authority", after.get("mapping", {})))
        strict_complete = all(decision[k] for k in (
            "contemporary_source_confirmed", "author_citation_primary_confirmed",
            "exact_donor_mechanism_confirmed", "changed_same_initial_baseline_confirmed",
            "reflection_confirmed"))
        relaxed_complete = all(decision[k] for k in (
            "contemporary_source_confirmed", "author_citation_primary_confirmed",
            "exact_donor_mechanism_confirmed", "changed_same_baseline_with_retrospection_confirmed",
            "reflection_confirmed"))
        assert strict_complete == (decision["strict_code"] == "C3"), (case_id, "code/criteria conflict")
        chain = dict(
            stratum=decision["stratum"], case_id=case_id, decision_unit=decision["decision_unit"],
            initial_url=before.get("initial_url", before.get("pinned_url_or_version", before.get("direct_original_url", before["original_url"]))),
            initial_version=before.get("initial_version", before.get("initial_public_definition", "미확인")),
            initial_date=before.get("created_utc", before.get("initial_proposal_public_utc", before.get("published_or_event_date", "미확인"))),
            original_purpose=decision["purpose"], preproposal_choice=decision["before_choice"],
            initial_proposal_choice=decision["initial_choice"], final_choice=decision["after_choice"],
            changed_independent_part=decision["changed_part"],
            donor_publication_P=decision["donor_publication_P"], donor_contemporary_public_V=decision["donor_public_V"],
            historic_index_I="미확인", author_exposure_A=decision["author_exposure_A"],
            new_to_this_research=True, author_new_to_principle=decision["author_new_to_principle"],
            causal_level=decision["strict_code"], same_purpose_reflection=decision["reflection"],
            tests_executed=False, implementation_scope=decision["implementation_scope"],
            timeline_json=after.get("timeline", []), object_authority_json=mapping,
            source_ids=refs, unresolved=decision["unknowns"],
            views_json=after.get("views", after.get("viewpoints", decision.get("views", {}))),
            strict_complete=strict_complete, relaxed_complete=relaxed_complete,
            code_baseline_standards_sensitivity=decision["code_baseline_sensitivity"],
            raw_initial_record=before, raw_followup_file=("streams/csswg/followup.json" if case_id.startswith("A-C") else "streams/gdal/followup.json" if case_id.startswith("A-G") else "streams/b/followup.json"),
        )
        chains.append(chain)
        for interpretation in ("strict_initial_proposal", "retrospective_analogy_same_baseline"):
            judgments.append(dict(
                stratum=decision["stratum"], case_id=case_id, interpretation=interpretation,
                baseline="frozen selected first proposal / B earliest restored proposal; retrospective initial records retain limits",
                code=decision["strict_code"] if interpretation == "strict_initial_proposal" else decision["relaxed_code"],
                reason=decision["strict_reason"] if interpretation == "strict_initial_proposal" else decision["relaxed_reason"],
                contemporary_source_confirmed=decision["contemporary_source_confirmed"],
                author_citation_primary_confirmed=decision["author_citation_primary_confirmed"],
                explicit_change_confirmed=decision["explicit_change_strict"] if interpretation == "strict_initial_proposal" else decision["explicit_change_relaxed"],
                actual_reflection_confirmed=decision["reflection_confirmed"],
                exact_donor_mechanism_confirmed=decision["exact_donor_mechanism_confirmed"],
                changed_same_baseline_confirmed=decision["changed_same_initial_baseline_confirmed"] if interpretation == "strict_initial_proposal" else decision["changed_same_baseline_with_retrospection_confirmed"],
                complete_chain=strict_complete if interpretation == "strict_initial_proposal" else relaxed_complete,
                plausible_mechanism=decision["plausible_mechanism"],
                positive_grade_reversed_by_counterevidence=decision["positive_grade_reversal_confirmed"],
                historical_positive_control_eligible=strict_complete if interpretation == "strict_initial_proposal" else relaxed_complete,
                conditional_recovery_rate="해당 없음" if not (strict_complete if interpretation == "strict_initial_proposal" else relaxed_complete) else "미실행; 검색 실험 없음",
                input_object=mapping.get("input", "미확인"),
                preserved_identity=mapping.get("same_object", mapping.get("identity_preserved", "미확인")),
                decision_authority=mapping.get("decision_actor", mapping.get("actor", mapping.get("authority", "미확인"))),
                before_state=mapping.get("state_before", mapping.get("before_state", "미확인")),
                after_state=mapping.get("state_after", mapping.get("after_state", "미확인")),
                output_constraint=mapping.get("output_constraint", mapping.get("constraint", mapping.get("output_constraints", "미확인"))),
                counterexample=decision["counterexample"], competing_explanation=decision["competing_explanation"],
                break_condition=decision["break_condition"], evidence_ids=refs,
                unknowns=decision["unknowns"], primary_claims_not_observation=decision.get("reported_not_observed", "미확인 값을 관측값으로 바꾸지 않음"),
            ))
        if decision["code_baseline_sensitivity"]:
            extra = judgments[-2].copy()
            code_complete = all(decision[k] for k in ("contemporary_source_confirmed", "author_citation_primary_confirmed", "exact_donor_mechanism_confirmed", "changed_preexisting_code_confirmed", "reflection_confirmed"))
            extra.update(interpretation="sensitivity_standards_inclusive_preexisting_code", baseline="prepatch executable code, not frozen RFC proposal", code="C3-conditional-compliance" if code_complete else "incomplete", reason="원안 기준을 바꾸고 지도 인터페이스 표준을 포함할 때 B02의 독립 GMLJP2 패치 사슬을 평가. 사후 감도이며 주집계로 합치지 않음.", explicit_change_confirmed=decision["changed_preexisting_code_confirmed"], changed_same_baseline_confirmed=decision["changed_preexisting_code_confirmed"], complete_chain=code_complete, historical_positive_control_eligible=code_complete, conditional_recovery_rate="미실행; 검색 실험 없음" if code_complete else "해당 없음")
            judgments.append(extra)
    return chains, judgments, decisions


def aggregate(sources, frames, chains, judgments, decisions):
    counted = [r for r in sources if r["counted"]]
    category_counts = dict(sorted(collections.Counter(r["count_category"] for r in counted).items()))
    groups = [r["duplicate_group"] for r in counted]
    assert len(groups) == len(set(groups))
    ids = [c["case_id"] for c in chains]
    assert len(ids) == len(set(ids)) == 12
    selected = [r for r in frames if r["selected"]]
    assert set(r["case_id"] for r in selected) == set(ids)
    assert len(selected) == 12
    table2 = []
    for interpretation in ("strict_initial_proposal", "retrospective_analogy_same_baseline"):
        for stratum in ("A", "B"):
            rows = [r for r in judgments if r["stratum"] == stratum and r["interpretation"] == interpretation]
            metrics = {field: sum(r[field] is True for r in rows) for field in (
                "contemporary_source_confirmed", "author_citation_primary_confirmed", "explicit_change_confirmed",
                "actual_reflection_confirmed", "complete_chain", "positive_grade_reversed_by_counterevidence",
                "plausible_mechanism", "historical_positive_control_eligible")}
            table2.append(dict(stratum=stratum, interpretation=interpretation, unique_cases=len(rows), ids=[r["case_id"] for r in rows], **metrics))
    sensitivity = [r for r in judgments if r["interpretation"] == "sensitivity_standards_inclusive_preexisting_code"]
    strict_eligible = {s:sum(r["complete_chain"] for r in judgments if r["stratum"] == s and r["interpretation"] == "strict_initial_proposal") for s in ("A", "B")}
    a_without_c03 = [r for r in judgments if r["stratum"] == "A" and r["case_id"] != "A-C03" and r["interpretation"] == "strict_initial_proposal"]
    return dict(
        source_record_count=len(sources), distinct_counted_primary_works=len(counted), count_categories=category_counts,
        source_ids_by_category={category:[r["source_id"] for r in counted if r["count_category"] == category] for category in category_counts},
        raw_stream_record_counts={s:sum(r["stream_record"].startswith(f"streams/{s}/") for r in sources) for s in STREAMS},
        supplementary_countertype4_records=sum(r["stream_record"].startswith("streams/review-counts/countertype4.json") for r in sources),
        frame_rows=len(frames), frame_rows_by_registry=dict(collections.Counter(r["registry"] for r in frames)),
        b_first10_rows=sum(r["stratum"] == "B" and r["counts_toward_sampling_cap"] for r in frames),
        selected_case_count=12, selected_ids=ids, A_B_event_overlap=[],
        source_eligibility=dict(A_initial_minimum=8, donor_minimum=6, recipient_followup_minimum=6, independent_counter_minimum=4, total_minimum=24),
        table2_rows=table2,
        sensitivity=dict(condition="standards inclusive AND preexisting-code baseline; not frozen proposal baseline", numerator=sum(r["complete_chain"] for r in sensitivity), denominator=sum(c["stratum"] == "B" for c in decisions), ids=[r["case_id"] for r in sensitivity if r["complete_chain"]]),
        strict_eligible=strict_eligible, conditional_recovery_rate={s:"해당 없음" if n == 0 else "미실행; 검색 실험 없음" for s,n in strict_eligible.items()},
        no_actual_search_recall_experiment=True,
        sensitivity_exclude_A_C03=dict(A_cases=len(a_without_c03), A_complete=sum(r["complete_chain"] for r in a_without_c03), original_sample_unchanged=True),
        baseline_reclassification_examples={"A-G03":"기존 원안 설명을 신규 변화로 바꾸면 설명 후보1을 얻지만 C3 접점 미충족", "B02":"기존 RFC 정책을 신규 변화로 바꾸면 설명 후보1; 코드 기준 감도와 구별"},
        limitations=["고유 원문 총수는 직접 읽은 범주 총수이며 실제 인과 donor 수가 아니다", "B-S21/S22 같은 변경 묶음 보수적 합산으로 raw50→49", "원문 미확인은 해당 역사의 부재가 아니다", "후대 비교 규칙은 당시 인과 원문으로 세지 않는다"],
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sources = source_rows()
    frames = frame_rows()
    chains, judgments, decisions = case_rows(sources)
    recount = aggregate(sources, frames, chains, judgments, decisions)
    source_ids = {r["source_id"] for r in sources}
    for decision in decisions:
        assert set(decision["evidence_ids"]) <= source_ids
    outputs = {
        "sources.jsonl": "".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in sources),
        "frame.csv": csv_text(frames, list(frames[0])),
        "chains.csv": csv_text(chains, list(chains[0])),
        "judgments.csv": csv_text(judgments, list(judgments[0])),
        "evidence/recount.json": json_text(recount),
        "evidence/source-locations.json": json_text({r["source_id"]:{"sources_jsonl_line":i,"raw":r["stream_record"],"url":r["original_url"],"locator":r["locator"]} for i,r in enumerate(sources,1)}),
    }
    if args.check:
        differences = [p for p, text in outputs.items() if not (ROOT / p).exists() or (ROOT / p).read_text(encoding="utf-8") != text]
        assert not differences, ("Derived outputs differ", differences)
    else:
        for path, text in outputs.items():
            (ROOT / path).write_text(text, encoding="utf-8")
    print(json.dumps({"mode":"check" if args.check else "rebuild", "source_records":len(sources), "unique_primary":recount["distinct_counted_primary_works"], "categories":recount["count_categories"], "frame_rows":len(frames), "cases":len(chains), "judgment_rows":len(judgments), "strict_complete":recount["strict_eligible"], "sensitivity":recount["sensitivity"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
