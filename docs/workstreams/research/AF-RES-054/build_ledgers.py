"""Build AF-RES-054 aggregate ledgers from the three auditable research streams.

This script reads only local summaries. It neither fetches sources nor constructs
participant outcomes. Unknown values are written as 미확인, never coerced to zero.
"""
from pathlib import Path
from datetime import datetime, timezone
import collections
import csv
import json

ROOT = Path(__file__).resolve().parent
STREAMS = ["baseline-methods", "software", "crossdomain", "root"]
STREAMS += sorted(p.parent.name for p in (ROOT / "streams").glob("resume-*/sources.jsonl"))
SLOTS = ["B01", "B02", "S01", "S02", "S03", "S04", "E01", "D01"]
REQUIRED = ["source_id", "work_id", "자료종류", "원본_URL", "최종_URL", "발행자",
            "확인_UTC", "판_또는_SHA", "쪽_절_행_셀", "관련_Q와_사례_ID", "확인한_내용",
            "확인범위와_한계", "지지_또는_반증", "직접열람_상태", "중복_계보"]


def read(path):
    return json.loads((ROOT / path).read_text())


def cell(value):
    if value is None:
        return "미확인"
    if isinstance(value, (dict, list, tuple, bool)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def csv_write(path, rows, columns):
    with (ROOT / path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: cell(row.get(c)) for c in columns})


def pick(row, *keys):
    for k in keys:
        if k in row:
            return row[k]
    return None


def main():
    now = datetime.now(timezone.utc).isoformat()
    sources = []
    for stream in STREAMS:
        f = ROOT / "streams" / stream / "sources.jsonl"
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            assert set(REQUIRED) <= set(r), (stream, r.get("source_id"))
            r["stream_file"] = f.relative_to(ROOT).as_posix()
            r["quota_category_original"] = r.get("quota_category", "uncategorized")
            r["quota_category"] = {
                "author_dataset": "author_data",
                "additional_primary_outside_selection": "additional_primary",
            }.get(r["quota_category_original"], r["quota_category_original"])
            # The substantive author plan was read, but conservative counting
            # does not add it to the same study's package or certify timing.
            if r["source_id"] == "BM-P01":
                r["counting_note"] = "Read author protocol; conservatively excluded from the unique-work minimum and prospective-preregistration quota. Separate-agent reviewer would allow an extra work; either convention leaves strict material quota short."
            sources.append(r)
    ids = [r["source_id"] for r in sources]
    assert len(ids) == len(set(ids)), "duplicate source IDs"
    source_lookup = {r["source_id"]: r for r in sources}
    (ROOT / "sources.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in sources) + "\n")
    indexed = []
    works = {}
    status_counts = collections.Counter()
    for line, r in enumerate(sources, 1):
        status_counts[r["직접열람_상태"].split(":")[0]] += 1
        indexed.append({"source_id": r["source_id"], "sources_jsonl_line": line,
                        "work_id": r["work_id"], "category": r["quota_category"],
                        "direct_status": r["직접열람_상태"], "url": r["최종_URL"],
                        "location": r["쪽_절_행_셀"], "count_flag": r.get("count_toward_minimum", False)})
        if r.get("count_toward_minimum"):
            assert "실패" not in r["직접열람_상태"], r["source_id"]
            works.setdefault(r["work_id"], {"work_id": r["work_id"], "category": r["quota_category"],
                                          "first_source_id": r["source_id"], "first_source_line": line,
                                          "url": r["최종_URL"], "source_ids": []})
    for r in sources:
        if r["work_id"] in works:
            works[r["work_id"]]["source_ids"].append(r["source_id"])
    category = collections.Counter(w["category"] for w in works.values())
    counts = {
        "generated_utc": now, "all_read_attempt_rows": len(sources),
        "unique_counted_primary_works": len(works), "minimum_required_unique_works": 22,
        "status_row_counts": dict(status_counts), "category_counts": dict(category),
        "strict_allocation": {
            "new_original_papers_selected_slots": {"observed": category["new_paper"], "required": 6,
                "note": "4 named new leads include Casdoc, whose assigned-comparator eligibility fails at full Methods. Only3 new assigned-comparison studies remain."},
            "all_new_original_papers_read_including_diagnostics": {"observed": category["new_paper"] + category["additional_primary"], "required": 6,
                "note": "Reading total only:4 selected new papers plus4 diagnostic papers. The latter include different interventions and a reanalysis; they never replace eligible sample slots."},
            "baseline_papers": {"observed": category["baseline_paper"], "required": 2},
            "separate_author_datasets": {"observed": category["author_data"], "required": 4,
                "note": "Package components, README, CSV, script, questionnaire and tutorials count once per package."},
            "separate_intervention_materials": {"observed": category["intervention_material"], "required": 4,
                "experiment_binary_identity_verified": 0,
                "note": "One independently identified DesignPatternDoc implementation repository; exact21-person experiment binary remains unverified. Embedded package materials do not add unique works."},
            "original_methods": {"observed": category["methods"], "required": 4},
            "preregistration_or_direct_replication": {"observed": category["prereg_or_replication"], "required": 2,
                "note": "Urry2021 direct replication and Bichler2026 analytical replication of the separate2016/2022 original cohort. Bichler2026 reuses E01's115-person subset, not an independent E01 cohort. The2016 author plan is not certified prospectively registered."},
        },
        "counting_rules": ["Unique work_id, not URL or file count", "Failed opens, metadata-only badges, repository inputs, mirrors and translations excluded", "A package's files are one work", "BM-P01 is an extra substantive protocol reading but not added to the conservative minimum", "Reading quota and sample eligibility are separate"],
        "counted_works": list(works.values()), "full_requirement_status": "부분 충족"
    }
    (ROOT / "evidence/source-counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2) + "\n")
    csv_write("evidence/source-index.csv", indexed, list(indexed[0]))

    studies = []
    for stream in STREAMS[:3]:
        for r in read(f"streams/{stream}/studies.json"):
            r = dict(r)
            r["case_id"] = pick(r, "case_id", "study_id")
            r["stream_file"] = f"streams/{stream}/studies.json"
            studies.append(r)
    assert {r["case_id"] for r in studies} == set(SLOTS)
    studies.sort(key=lambda r: SLOTS.index(r["case_id"]))
    (ROOT / "evidence/study-register.json").write_text(json.dumps(studies, ensure_ascii=False, indent=2) + "\n")

    frame = []
    for stream in ["software", "crossdomain"]:
        for r in read(f"streams/{stream}/frame.json")["records"]:
            frame.append({"record_type": "retained_metadata", "frame_id": r["frame_id"],
                          "source": r.get("source"), "domain": pick(r, "domain", "field"),
                          "query_or_metadata_url": pick(r, "query_id", "metadata_url"),
                          "returned_order": pick(r, "returned_order", "native_return_rank"),
                          "publication_date": pick(r, "original_paper_date", "publication_date"),
                          "permanent_id": pick(r, "original_paper_id", "doi", "permanent_id", "repository_id"),
                          "title": r.get("title"), "url": r.get("url"),
                          "duplicate_cohort": r.get("duplicate_cohort"),
                          "decision": pick(r, "eligibility", "decision"), "reason": r.get("reason"),
                          "slot": pick(r, "selected_slot", "study_slot"),
                          "post_fulltext_status": "S03는 Methods에서 별도 배정 대조군 없음; 교체 안 함" if pick(r, "selected_slot", "study_slot") == "S03" else None,
                          "raw_record_file": f"streams/{stream}/frame.json", "details_json": r})
    for r in studies:
        slot = r["case_id"]
        frame.append({"record_type": "required_slot", "frame_id": "SLOT-" + slot, "source": "fixed baseline" if slot[0] == "B" else "bounded frame",
                      "domain": pick(r, "stratum", "layer"), "title": pick(r, "study", "title"),
                      "url": pick(r, "source_url", "paper_url"), "slot": slot,
                      "decision": "vacant" if slot in ["S04", "D01"] else "retained lead; no outcome-driven replacement",
                      "post_fulltext_status": pick(r, "postfreeze_scope_resolution", "primary_endpoint_status", "classification"),
                      "reason": pick(r, "reason", "unknown", "needed"), "raw_record_file": r["stream_file"],
                      "details_json": {"selected_slot": slot, "is_new_slot": slot[0] != "B"}})
        if slot == "E01":
            frame[-1]["permanent_id"] = "doi:10.1037/edu0000433"
            frame[-1]["publication_date"] = "2019-12 (author metadata, month precision); alternative2020-10 issue date"
            frame[-1]["post_fulltext_status"] = "원논문·SAV231분석행 직접 확인; 원 배정N/사람키/시각/원 이진 통과선 미확인"
            frame[-1]["details_json"]["date_limit"] = "DOI creation date is not publication date; within-October day order is unresolved under mixed-date interpretation"
    csv_write("frame.csv", frame, ["record_type", "frame_id", "source", "domain", "query_or_metadata_url", "returned_order", "publication_date", "permanent_id", "title", "url", "duplicate_cohort", "decision", "reason", "slot", "post_fulltext_status", "raw_record_file", "details_json"])

    def urls(source_ids):
        return list(dict.fromkeys(source_lookup[s]["최종_URL"] for s in source_ids if s in source_lookup))

    endpoints, joins, bounds = [], [], []
    for stream in STREAMS[:3]:
        for r in read(f"streams/{stream}/endpoints.json"):
            sid = r.get("source_ids", [])
            endpoints.append({"endpoint_id": r["endpoint_id"], "case_id": pick(r, "case_id", "study_id"),
                              "unit": r.get("unit"), "task_or_endpoint": pick(r, "endpoint", "task", "definition"),
                              "condition": r.get("condition"), "N_definition": pick(r, "N", "denominator", "population", "N_each_task_each_arm"),
                              "time_start": pick(r, "time_start", "start"), "time_end": pick(r, "time_end", "stop", "end"),
                              "deadline_seconds": pick(r, "deadline_seconds", "cap_seconds", "time_limit_seconds"),
                              "clock_limit": pick(r, "deadline_scope", "cap_precision", "time_limit_scope", "deadline_caveat"),
                              "training": r.get("training"), "quality_original": pick(r, "quality_definition", "quality", "criterion", "q_definition"),
                              "missing_or_withdrawal": pick(r, "failure_vs_missing", "missing_policy", "withdrawal", "score_missing_analyzed"),
                              "classification": r.get("classification"), "source_ids": sid, "source_urls": urls(sid),
                              "stream_record_file": f"streams/{stream}/endpoints.json", "details_json": r})
            if r["endpoint_id"] == "E01-final":
                endpoints[-1]["deadline_seconds"] = None
                endpoints[-1]["nominal_or_approximate_duration_seconds"] = 2100
                endpoints[-1]["clock_limit"] = "Approximately35-minute final test; enforced submission deadline and actual timestamps unverified"
                endpoints[-1]["missing_or_withdrawal"] = "분석231행 KPost결측0; 원래 배정 후 결측·회기탈락 수는 미확인"
            if r["endpoint_id"] == "S03-primary":
                endpoints[-1]["deadline_seconds"] = None
                endpoints[-1]["nominal_or_approximate_duration_seconds"] = 2400
                endpoints[-1]["clock_limit"] = "40-minute planned work; optional up-to20-minute extension offered to all13, used by3; not a common hard deadline"
            if r["endpoint_id"] == "DX-E02-immediate-delayed":
                endpoints[-1]["N_definition"] = "선정8자리 밖 진단: 모집143명; 공개 분석112명;143명 배정표 왼쪽 결합 아님"
                endpoints[-1]["condition"] = r.get("intervention")
                endpoints[-1]["task_or_endpoint"] = "Immediate and one-week delayed problem-solving/ratings; distinct occasions"
            if r["endpoint_id"] == "DX-D02-CAD":
                endpoints[-1]["N_definition"] = "선정8자리 밖 진단: 같은6명이 두 인터페이스를 교차 수행; 질의 수와 사람 수는 다름"
                endpoints[-1]["training"] = "별도 훈련/피드백20분"
                endpoints[-1]["clock_limit"] = "각 인터페이스20분; 과제 순서 선택·건너뛰기 허용"
        for r in read(f"streams/{stream}/joins.json"):
            sid = r.get("source_ids", [])
            joins.append({"join_id": r["join_id"], "case_id": pick(r, "case_id", "study_id"),
                          "left_table": pick(r, "left_table", "left_used", "left_required"),
                          "key": pick(r, "required_key", "key", "join_key", "person_key"),
                          "planned_units": r.get("expected_protocol_units"),
                          "observed_assignment_rows": r.get("observed_raw_allocation_rows"),
                          "left_input_rows": pick(r, "left_rows", "left_observed_rows", "pre_join_rows"),
                          "right_input_rows": pick(r, "right_rows", "right_observed_rows", "right_rating_rows"),
                          "event_rows": pick(r, "raw_events", "observed_event_rows"),
                          "event_aggregation": pick(r, "event_aggregation", "event_aggregated_rows"),
                          "joined_rows": pick(r, "joined_rows", "after_each_left_join_rows", "post_join_rows", "after_assignment_left_join_rows"),
                          "duplicate_keys": pick(r, "duplicate_keys", "duplicate_IDs_each"),
                          "unmatched_left": pick(r, "unmatched", "unmatched_posttask", "left_unmatched_each", "unmatched_left_rows", "unlinked_assignment_rows"),
                          "withdrawn_rows": r.get("withdrawn_rows"),
                          "target_joint_success_rows": r.get("raw_joint_success_rows"),
                          "target_join_performed": False,
                          "actual_other_join": r.get("joined_rows") is not None or r.get("after_each_left_join_rows") is not None,
                          "status": pick(r, "status", "failure_location"), "failure_location": r.get("failure_location"),
                          "minimum_resume_input": pick(r, "smallest_resume_input", "left_required"),
                          "source_ids": sid, "source_urls": urls(sid),
                          "stream_record_file": f"streams/{stream}/joins.json", "details_json": r})
            if r["join_id"] == "S01-roster-artifacts":
                joins[-1]["event_rows"] = r["right_rows"]["Newton_events"]
            if joins[-1]["minimum_resume_input"] is None:
                joins[-1]["minimum_resume_input"] = {
                    "S01": "Original functional-completion checklist and final-submission definition;24 condition units' validated clock/status/grade keyed by person,task,condition,period",
                    "S02": "Original enforced-stop/overrun rule, person-ID crosswalk and restored task-validation/source/diagram records",
                    "S03": "Task success/extension ledger could support descriptive completion; assigned format contrast did not exist and requires a new design, not an imputed row",
                    "S04": "New preregistered metadata search for an eligible public-package study; do not replace after observing outcomes",
                    "D01": "Eligible2018–2025 example-aid/control CAD study with author public package in a newly frozen search frame",
                    "DX-D02": "Six-person query/period/attempt ledger plus original correctness flags and assigned interface order",
                }.get(joins[-1]["case_id"])
        for r in read(f"streams/{stream}/bounds.json"):
            sid = r.get("source_ids", [])
            bid = r["bound_id"]
            alternate = "author-completion" in bid or "task3" in bid
            is_diff = any(x in bid.lower() for x in ["difference", "diff-"]) or bid == "B02-task3"
            bounds.append({"bound_id": bid, "case_id": pick(r, "case_id", "study_id"),
                           "endpoint_scope": "secondary; never copied into primary joint endpoint" if alternate else "primary joint or missing-data record",
                           "condition_or_contrast": pick(r, "condition", "contrast"),
                           "unit": "rate difference" if is_diff else "assigned units or explicitly analyzed-only denominator",
                           "N": pick(r, "N", "N_assigned"), "N_analyzed": r.get("N_analyzed"),
                           "t": r.get("t"), "q": r.get("q"), "q_definition": r.get("q_definition"),
                           "observed_joint_x": pick(r, "x", "x_observed"),
                           "lower": pick(r, "L", "difference_lower"), "upper": pick(r, "U", "difference_upper"),
                           "rate_or_difference_interval": r.get("rate_range"),
                           "integer_extreme_tables": pick(r, "unknown_t_endpoint_tables", "extreme_tables"),
                           "table_meaning": "x=q only weak conditional t envelope; Table XII same-clock partial-submission sensitivity in details_json; not established full-publication sharp t range" if "unknown_t_endpoint_tables" in r else None,
                           "classification": pick(r, "status", "classification"),
                           "reason": pick(r, "reason", "interpretation"),
                           "sampling_uncertainty": pick(r, "sampling_uncertainty") or "미실시; identification range is not a sampling confidence interval",
                           "source_ids": sid, "source_urls": urls(sid),
                           "stream_record_file": f"streams/{stream}/bounds.json", "details_json": r})
            if "author-completion" in bid:
                bounds[-1]["observed_secondary_count"] = r.get("x")
                bounds[-1]["observed_joint_x"] = None
            if bid in ["E01-DIFF-T0", "E01-DIFF-T1"]:
                bounds[-1]["condition_or_contrast"] = "worked examples − problem solving; " + ("압박 없음" if not r["pressure"] else "압박 있음")
                bounds[-1]["N_analyzed"] = [r["N_T_analyzed"], r["N_C_analyzed"]]
    calculation = read("evidence/calculation-check.json")
    example = calculation["illustration_only_same_margins_opposite_sign"]
    for arm in ["treatment", "control"]:
        r = example[arm]
        bounds.append({"bound_id": "ILL-" + arm, "case_id": "ILL", "endpoint_scope": "constructed arithmetic example, not study observations",
                       "condition_or_contrast": arm, "unit": "hypothetical assigned people", "N": r["N"], "t": r["t"], "q": r["q"],
                       "observed_joint_x": None, "lower": r["lower"], "upper": r["upper"],
                       "rate_or_difference_interval": r["rate_interval"], "integer_extreme_tables": [r["lower_table"], r["upper_table"]],
                       "table_meaning": "same exact margins, both feasible integer extremes", "classification": "범위만; 산술 반례",
                       "reason": "Do not use illustrative q=8 as Blueprint or any study's actual quality count.",
                       "source_ids": [], "source_urls": [], "stream_record_file": "evidence/calculation-check.json", "details_json": r})
    bounds.append({"bound_id": "ILL-difference", "case_id": "ILL", "endpoint_scope": "constructed arithmetic example, not study observations",
                   "condition_or_contrast": "treatment-control", "unit": "rate difference", "N": [10, 10],
                   "lower": "-1/10", "upper": "1/5", "rate_or_difference_interval": ["-1/10", "1/5"],
                   "classification": "범위만; 양 부호 허용", "reason": "same exact N/q/t, opposite feasible pairings",
                   "sampling_uncertainty": "not a CI", "source_ids": [], "source_urls": [],
                   "stream_record_file": "evidence/calculation-check.json", "details_json": example["contrast"]})
    for name, rows in [("endpoints", endpoints), ("joins", joins), ("bounds", bounds)]:
        columns = list(dict.fromkeys(k for r in rows for k in r))
        csv_write(name + ".csv", rows, columns)
        for r in rows:
            missing = set(r.get("source_ids", [])) - set(source_lookup)
            assert not missing, (name, missing)
    validation = {"generated_utc": now, "status": "passed", "source_rows": len(sources),
                  "unique_counted_works": len(works), "source_schema_required_fields": len(REQUIRED),
                  "frame_metadata_rows": sum(r["record_type"] == "retained_metadata" for r in frame),
                  "frame_slot_rows": sum(r["record_type"] == "required_slot" for r in frame),
                  "endpoint_rows": len(endpoints), "join_rows": len(joins), "bound_rows": len(bounds),
                  "slot_ids": SLOTS, "missing_source_references": [],
                  "note": "Validation of ledger consistency, not certification that all research quotas or target outcomes were obtained."}
    (ROOT / "evidence/ledger-build-check.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(validation, ensure_ascii=False))


if __name__ == "__main__":
    main()
