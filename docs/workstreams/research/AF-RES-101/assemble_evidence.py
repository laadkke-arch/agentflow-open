"""Join completed observations without modifying the two frozen CSVs."""
from pathlib import Path
import csv
import datetime as dt
import json
from collections import Counter

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return json.loads((ROOT / path).read_text())


def dump(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_csv(path, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / path).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows({k:json.dumps(v,ensure_ascii=False,separators=(",",":")) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in rows)


def normalize(s, path, line):
    cases = s.get("case_ids", s.get("case_id", []))
    if isinstance(cases, str): cases = [cases]
    sid = s.get("source_id", s.get("id"))
    fp = s.get("fingerprint") or {}
    if s.get("sha256"): fp.setdefault("sha256", s["sha256"])
    if s.get("git_blob_sha1"): fp.setdefault("git_blob_sha1", s["git_blob_sha1"])
    locator = s.get("version_section_locator", s.get("version_section"))
    if not locator:
        locator = str(s.get("version", "")) + "; " + str(s.get("section_or_lines", s.get("location", "")))
    relation = s.get("claim_relation", s.get("supports_or_refutes"))
    if relation is None:
        relation = {"supports":s.get("supports_claims",[]),"refutes":s.get("refutes_claims",[])}
    return {"source_id":sid,"q":s.get("q",s.get("questions",[])),"case_ids":cases,
            "category":s.get("category",s.get("count_category","method")),
            "original_url":s.get("original_url"),
            "direct_open_url":s.get("direct_open_url",s.get("directly_opened_url",s.get("original_url"))),
            "fixed_url":s.get("fixed_url",s.get("pinned_url")),
            "checked_at_utc":s.get("checked_at_utc",s.get("checked_utc",s.get("confirmation_utc"))),
            "analyst_review_completed_utc":s.get("analyst_review_completed_utc"),
            "author_publisher":s.get("author_publisher",str(s.get("author",""))+" / "+str(s.get("publisher",""))),
            "lineage":s.get("lineage",s.get("event_or_authorship_lineage")),
            "version_section_locator":locator,"fingerprint":fp,
            "observed":s.get("observed",s.get("confirmed")),"claim_relation":relation,
            "limits_unknown":s.get("limits_unknown",s.get("limitations")),
            "counted":s.get("counted",False),"duplicate_reason":s.get("duplicate_reason"),
            "observation_receipt":s.get("observation_receipt",s.get("receipt",s.get("source_record"))),
            "raw_source_record":str(path.relative_to(ROOT)),"raw_source_record_line":line}


# Contract/prior-work reading is operational calibration, not new study evidence.
contract = load("evidence/start/contract-read.json")
contract_rows = []
for i, entry in enumerate(contract["contract_files"] + contract["research_input_blobs"], 1):
    ref = entry.get("ref",contract["start_commit"])
    url = "https://github.com/laadkke-arch/agentflow-open/blob/" + ref + "/" + entry["path"]
    prior = "AF-RES-097" in entry["path"]
    contract_rows.append({"source_id":f"CONTRACT-{i:02}","q":["Q1","Q2","Q4"],"case_ids":[],
        "category":"operating_contract_or_calibration","original_url":url,"direct_open_url":url,"fixed_url":url,
        "checked_at_utc":contract["read_at_utc"],"author_publisher":"laadkke-arch / agentflow-open repository",
        "lineage":"repository operating instructions or AF-RES-097 predecessor work",
        "version_section_locator":ref + "; " + entry["path"] + ("; HANDOFF / requested first and return tables / reconciliation only" if prior else "; startup contract; central JSON only AF-RES-101 entry"),
        "fingerprint":{"git_blob_sha1":entry.get("blob",entry.get("start_blob")),"sha256":entry.get("sha256")},
        "observed":("이전 연구의 제품명·조작·입력·판 구분 및 분모만 교정용으로 읽었다. 기존24회 실행/Pillow/100-P1은 재실행·재채점하지 않았다." if prior else "허용경로·의존성·봉인/검사 절차를 확인했다. 계획판 대비 변경은 dot-control.json뿐이고 연구브리프/운영규칙 blob은 동일하다."),
        "claim_relation":"출발 계약과 교정 범위","limits_unknown":"새8사건이나 고유자료 최소량에 산입하지 않음. 이전 RESULT 도구응답 일부 부가설명 노출은 SCOPE에 기록.",
        "counted":False,"duplicate_reason":"operational/calibration input, excluded from new primary-evidence minimum"})
(ROOT / "evidence/start/sources-contract.jsonl").write_text("".join(json.dumps(s,ensure_ascii=False)+"\n" for s in contract_rows))

sources = []
for path in sorted((ROOT / "evidence").rglob("*sources*.jsonl")):
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip(): sources.append(normalize(json.loads(line),path,i))
api_fingerprints = load("evidence/start/api-doc-fingerprints.json")
for source in sources:
    if source["source_id"] in api_fingerprints:
        extra = api_fingerprints[source["source_id"]]
        source["fingerprint"]["current_reread"] = extra
        source["observation_receipt"] = "evidence/start/api-doc-fingerprints.json"
assert len({r["source_id"] for r in sources}) == len(sources), "source ID collision"
required = ["source_id","direct_open_url","checked_at_utc","author_publisher","lineage","version_section_locator","fingerprint","observed","limits_unknown"]
missing = [{"source_id":r["source_id"],"fields":[k for k in required if not r.get(k)]} for r in sources]
missing = [r for r in missing if r["fields"]]
dump("evidence/source-schema-review.json", {"checked_utc":NOW,"missing_fields":missing})
(ROOT / "sources.jsonl").write_text("".join(json.dumps(s,ensure_ascii=False)+"\n" for s in sources))

counts = Counter()
for s in sources:
    if not s["counted"]: continue
    sid = s["source_id"]
    group = ("selected_requests" if sid.startswith("SO-") else
             "imagemagick_documents_implementations" if sid.startswith("IM-O") else
             "imagemagick_upstream_tests" if sid.startswith("IM-T") else
             "typst_documents_implementations" if sid.startswith("TY-D") else
             "typst_upstream_input_expected_bundles" if sid.startswith("TY-T") else
             "cross_domain_official_manual_tests" if sid.startswith("CD-") else
             "supplemental_primary")
    counts[group] += 1
dump("evidence/source-counts.json", {"generated_utc":NOW,"ledger_rows":len(sources),"counted_unique":sum(counts.values()),"groups":dict(counts),
    "mandatory_core_unique":sum(v for k,v in counts.items() if k!="supplemental_primary"),
    "counted_ids":[s["source_id"] for s in sources if s["counted"]],
    "rule":"same file sections/mirrors/revisions and paired expected images count once; unselected screening requests count zero"})

frozen = list(csv.DictReader((ROOT / "candidates.csv").open()))
im = {r["candidate_id"]:r for r in load("evidence/imagemagick/stage3/assessment-part.json")}
ty = {r["candidate_id"]:r for r in load("evidence/typst-official/assessment.json")}
supp = {r["candidate_id"]:r for r in load("evidence/root-supplement/assessment.json")["candidates"]}
assessments = []
valid_distinct = {"TY-A1-C2","TY-A2-C1","TY-A2-C2"}
for c in frozen:
    sid=c["candidate_id"]; r = dict(im[sid] if sid in im else ty[sid])
    r.update(case_id=c["case_id"],candidate_id=sid,blank=c["blank"]=="True",
        A_decision=c["A_decision"],B_decision=c["B_decision"],
        A_returned_position=c["A_returned_position"],B_returned_position=c["B_returned_position"],
        original_proposal_url=c["original_proposal_url"],original_fixed_url=c["original_fixed_url"],
        frozen_original_links=json.loads(c["original_links"]),
        historical_original_input_and_version_verified=False,
        research_valid_distinct_denominator_eligible=sid in valid_distinct,
        full_candidate_prior_knowledge_denominator_eligible=False,
        full_candidate_new_awareness="미확인")
    if sid in supp: r["supplemental_source_and_probe_assessment"] = supp[sid]
    if sid=="TY-A1-C1":
        r.update(required_output_status="반박(CSS literal); Typst 적용 미확인",validity="literal_CSS_grammar_counterevidence_and_unprovided_host",
                 source_ids=["SUP-CSS-BORDERS"],official_urls=["https://www.w3.org/TR/2020/CR-css-backgrounds-3-20201222/#border-shorthands"],
                 actual_observation=supp[sid]["finding"],limitations=[supp[sid]["limits"]],
                 final_root_review_utc=NOW,root_review_is_after_OP_summaries=True)
    assessments.append(r)
assert len(assessments)==24
dump("evidence/assessment.json",assessments)

im_follow = load("evidence/imagemagick/stage3/followup-part.json")
ty_follow = load("evidence/typst/stage3/followup-part.json")
follow=[]
for inv in im_follow["case_inventory"]:
    case=inv["case_id"]; events=[e for e in im_follow["events"] if e["case_id"]==case]
    cg=[]
    for r in assessments:
        if r["case_id"]!=case or r["blank"]:continue
        cg.append({"candidate_id":r["candidate_id"],"already_knew_before_proposal":"미확인",
            "explicit_new_awareness":"미확인","execution_report":r.get("execution_report","미확인"),
            "input_version_output_linked_execution":"미확인","rejection":"미확인","old_method_retained":"미확인",
            "positive_independent_prior_knowledge_evidence":False,"knowledge_denominator_eligible":False,
            "response_evidence":[e for e in events if r["candidate_id"] in e.get("candidate_ids",[])],
            "partial_core_familiarity":r.get("prior_known")=="partial_core_only"})
    follow.append({"case_id":case,"question_id":inv["question_id"],"window_from_utc":inv["t0_utc"],"window_through_utc":inv["cutoff_utc"],
        "author_events":events,"author_event_count":len(events),"candidate_ground_truth":cg,
        "already_knew_before_proposal":"미확인","explicit_new_awareness":"미확인",
        "execution_report":"지지(수정 C1의 실패보고1건)" if case=="IM-A1" else "미확인",
        "input_version_output_linked_execution":"미확인","rejection":"미확인","old_method_retained":"미확인",
        "current_acceptance":inv["current_acceptance"],"acceptance_used_for_knowledge_or_execution":False,
        "public_result_or_patch_links":[],"limits":im_follow["limitations"],"coded_utc":im_follow["review_completed_utc"],
        "source_record":"evidence/imagemagick/stage3/followup-part.json"})
for r in ty_follow:
    follow.append({"case_id":r["case_id"],"question_id":r["question_id"],"window_from_utc":r["window_from_utc"],"window_through_utc":r["window_through_utc"],
        "author_events":r["author_events"],"author_event_count":len(r["author_events"]),"candidate_ground_truth":r["candidate_ground_truth"],
        **{k:r[k] for k in ["already_knew_before_proposal","explicit_new_awareness","execution_report","input_version_output_linked_execution","rejection","old_method_retained"]},
        "current_acceptance":r["current_accepted_answer_id"],"acceptance_used_for_knowledge_or_execution":False,
        "public_result_or_patch_links":r["public_result_or_patch_links_in_author_records"],"limits":r["limitations"],"coded_utc":r["coded_utc"],
        "source_record":"evidence/typst/stage3/followup-part.json","followup_summary":r["followup_summary"],
        "known_method_outside_candidates":r["known_method_outside_candidates"]})
assert len(follow)==8 and sum(r["author_event_count"] for r in follow)==12
write_csv("followup.csv",follow)
dump("evidence/followup-cases.json",follow)
dump("evidence/original-current-comparison.json",{"imagemagick":im_follow["first_current_comparison"],"typst":load("evidence/typst/stage3/original-vs-current.json"),
    "body_changed_requests":3,"actual_attempt_history_changed_requests":1,"purpose_detail_changed_requests":1,
    "A_filter_definite_changes":0,"B_filter_definite_changes":0,"request_denominator":8,
    "non_inference":"0 definitive filter changes does not erase actual-history or goal-constraint changes; frozen baseline remains earliest public revision."})
print(json.dumps({"source_counts":dict(counts),"unique_sources":sum(counts.values()),"source_missing_fields":missing,"assessment_slots":len(assessments),"followup_requests":len(follow)},ensure_ascii=False))
