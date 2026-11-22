"""Append post-seal evidence and produce the 12-row outcome ledger.
Never rewrites frozen requests/predictions/SCOPE/frame. Safe to rerun.
"""
import csv, json, pathlib, collections
P = pathlib.Path(__file__).resolve().parents[1]
E = P / "evidence"
SEAL = "0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1"
def jread(name): return json.loads((E/name).read_text())
def jl(name): return [json.loads(x) for x in (E/name).read_text().splitlines() if x]
sources=[json.loads(x) for x in (P/"sources.jsonl").read_text().splitlines() if x]
known={r["source_id"] for r in sources}
new=jl("matplotlib12-outcome-sources.jsonl")+jl("audacity-outcome-sources.jsonl")+jl("matplotlib3-outcome-sources.jsonl")+jread("method-review.json").get("source_revisits",[])
for r in new:
    r=dict(r)
    for dest, aliases in {"url":["source_url"],"publication_date":["published_at"],"changed_date":["modified_at"],"checked_utc":["accessed_utc"],"exact_locator":["locator","location"],"questions":["question_ids"],"case_ids":["cases"]}.items():
        if dest not in r:
            r[dest]=next((r[k] for k in aliases if k in r), None)
    r.setdefault("publisher","publisher identified in cited primary work")
    r.setdefault("kind","direct_source_revisit")
    r.setdefault("final_url",r.get("url"))
    r.setdefault("edition_id","edition in cited locator")
    r.setdefault("confirmed","See exact locator and source notes")
    r.setdefault("limitations","No additional count for revisit")
    r.setdefault("duplicate_of",None)
    r.setdefault("minimum_count",False)
    r.setdefault("allocation",None)
    r.setdefault("phase","after_prediction_seal")
    r["canonicalized_by"]="evidence/assemble-outcomes.py"
    if r.get("allocation")=="followup": r["allocation"]="receiver_followup"
    if r.get("allocation")=="comparison": r["allocation"]="independent_comparison"
    if r["source_id"]=="AUD-O360":
        r["original_proposed_minimum_count"]=r["minimum_count"]
        r["minimum_count"]=False
        r["allocation"]=None
        r["duplicate_of"]="AUD-O6165"
        r["minimum_count_reason"]="Conservative same-change dedup: release corroborates6165 and adds no unique fixture; raw proposal retained."
    if r["source_id"]=="REV-AUD-NR242":
        r["work_id"]="audacity-source-release:2.4.2"
        r["duplicate_of"]="AUD-API242-NR"
    if r["source_id"]=="RMO04":
        r.pop("reopened_utc",None) # first open time retained; later read exact second was not logged
    if r["source_id"] not in known:
        sources.append(r);known.add(r["source_id"])
(P/"sources.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in sources))
preds=list(csv.DictReader((P/"predictions.csv").open()))
sp={c["request_id"]:c for c in jread("matplotlib12-outcomes.json")["cases"]}
au={c["request_id"]:c for c in jread("audacity-outcomes.json")["cases"]}
m3=jread("matplotlib3-outcomes.json")["cases"][0]
rows=[]
for pred in preds:
    cid=pred["request_id"];pid=pred["prediction_id"]
    r=dict(prediction_id=pid,request_id=cid,seal_sha=SEAL,preseal_pair_relation=pred["preseal_pair_relation"],judgment="미확인",qualified_evidence="",evidence_levels="",decision_urls="",code_test_urls="",evidence_edition="",normal_observed="미확인",boundary_observed="미확인",matched_normal="false",matched_boundary="false",same_operation_input_purpose_verified="false",strict_pair_denominator_member="false",unique_support="false",both_rejected="false",pair_disposition="판정불가",relation_after_read="",author_donor_adoption="미확인",local_receiver_run="not_executed",revision_history="",minimum_next_evidence="")
    if cid in sp:
        c=sp[cid];p=next(x for x in c["predictions"] if x["prediction_id"]==pid)
        r["qualified_evidence"]=p["classification"]+"; "+p["reason"]
        r["evidence_levels"]="D;R_report"+(";C_related;T_other_input;L_related" if cid=="M01" else ";S_later")
        r["decision_urls"]="; ".join(e["url"] for e in c["evidence"] if e["level"] in ["D","R"] and e.get("url"))
        r["code_test_urls"]="; ".join(e["url"] for e in c["evidence"] if e["level"] in ["S","C","T","L"] and e.get("url"))
        r["evidence_edition"]="; ".join(str(e.get("edition_utc","")) for e in c["evidence"] if e.get("url"))
        r["normal_observed"]=c["normal_input_status"]
        r["boundary_observed"]=c["boundary_input_status"]
        r["judgment"]="판별불가" if cid=="M02" else "미확인"
        r["pair_disposition"]="판별불가" if cid=="M02" else "판정불가"
        r["relation_after_read"]=c["pair_discrimination"]["reason"]
        r["author_donor_adoption"]=c["novelty"]["adoption_record"]
        r["revision_history"]="current first body; immutable creation edition unverified; comments may have edits"
        r["minimum_next_evidence"]=c["minimum_next_test"]
    elif cid=="M03":
        c=m3;p=next(x for x in c["judgments"] if x["prediction_id"]==pid)
        r["judgment"]=p["judgment"];r["qualified_evidence"]=p["qualified_evidence"]
        r["evidence_levels"]=";".join(c["evidence_levels"])
        r["decision_urls"]=c["decision_url"]+"; "+c["requester_report_url"]
        r["code_test_urls"]=c["code_change"]["url"]+"; "+c["test"]["url"]
        r["evidence_edition"]="comments2019-03-06; PRhead"+c["code_change"]["head"]+"; merge"+c["code_change"]["merge"]
        r["normal_observed"]=c["normal_evidence"];r["boundary_observed"]=c["boundary_evidence"]
        r["relation_after_read"]="좌표단위별 출력 예측은 다르지만 두 입력의 동일조건 후속 기록이 없음. 후보P2의 중심목적 위반을 원리 자체의 반증으로 쓰지 않음."
        r["revision_history"]=c["revision_history"];r["minimum_next_evidence"]=c["minimum_next_evidence"];r["author_donor_adoption"]=c["author_donor_adoption"]
    else:
        c=au[cid];p=next(x for x in c["judgments"] if x["prediction_id"]==pid)
        r["judgment"]=p["judgment"];r["qualified_evidence"]=p["reason"]
        r["evidence_levels"]={"AUD01":"D;C_third_choice;R_report_other_input;L","AUD02":"D_assertion;D_deferral;C_comparison","AUD03":"C_baseline_correction;C_cleanup;no_same_input_T_or_R"}[cid]
        r["decision_urls"]=c["decision"]["url"]
        if cid=="AUD01":
            r["code_test_urls"]=c["implementation"]["url"]+"; "+c["wrapper_followup"]["url"]+"; "+c["release"]["url"]
            r["evidence_edition"]=c["implementation"]["merge_commit"]+"; "+c["wrapper_followup"]["merge_commit"]
            r["boundary_observed"]="후속 제3명령C의 실행보고 그림: Start2.62385/End5.29415. 봉인1.25/2.50와point입력 아님."
        elif cid=="AUD02":
            r["code_test_urls"]=c["subtask"]["closing_comment"]+"; "+c["independent_comparison"]["url"]
            r["evidence_edition"]="511comment2445034377/2024-10-29;2713comment1150354103/2022-06-08"
        else:
            r["code_test_urls"]=c["post_seal_correction"]["baseline_url"]+"; "+c["post_seal_correction"]["after_url"]
            r["evidence_edition"]="2.4.2 16d52f63a4183bba77ef7305d14622958dc0d1d5;2024 "+c["implementation"]["commit"]
            r["revision_history"]=c["post_seal_correction"]["affected"]
        r["pair_disposition"]="판별불가" if cid in ["AUD01","AUD02"] else "판정불가"
        r["relation_after_read"]=p["reason"]
        r["author_donor_adoption"]=c["author_donor_adoption"]
        if cid!="AUD03":r["revision_history"]=c["revision_history"]
        r["minimum_next_evidence"]=c["minimum_next_evidence"]
    r['comparison_rule_version']='post-reveal complete-comparison requirement; see amendments; not identical to prespecified wording'
    r['original_wording_lenient_case_member']=str(cid=='M01').lower()
    r['operator_only_case_member']=str(cid in ['M01','M03']).lower()
    r['lenient_unique_support']='false'
    r['lenient_case_disposition']='판정불가' if cid=='M01' else '분모외'
    r['operator_only_disposition']='판정불가' if cid in ['M01','M03'] else '분모외'
    r['boundary_qualitative_match']=str(pid=='M01-P1').lower()
    r['boundary_qualitative_judgment']='조건부 지지_R_report; exact normal/B outputs absent' if pid=='M01-P1' else '미확인'
    r['operator_acceptance_match']=str(pid in ['M01-P1','M02-P1','M02-P2','M03-P1']).lower()
    rows.append(r)
with (P/"outcomes.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
counted=[r for r in sources if r["minimum_count"]]
print(json.dumps({"sources_records":len(sources),"unique_counted":len(counted),"allocation":dict(collections.Counter(r["allocation"] for r in counted)),"outcome_rows":len(rows),"judgments":dict(collections.Counter(r["judgment"] for r in rows))},ensure_ascii=False))
