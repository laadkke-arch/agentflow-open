"""Validate research artifact joins, immutable evidence and required presentation.

This is an artifact check. It does not turn an unverified supplier predicate or
methodological acceptance gap into a passed condition.
"""
import argparse,csv,hashlib,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).resolve().parent
REPO=P.parents[3]
def readj(n):return json.loads((P/n).read_text())
def rows(n):return [json.loads(l) for l in (P/n).read_text().splitlines() if l.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output");ap.add_argument("--handoff",action="store_true");a=ap.parse_args();checks=[]
    def chk(cond,met,ev,note=""):checks.append(dict(condition=cond,met=bool(met),evidence=ev,note=note))
    for n in ["input-seal.json","common-seal.json","route-seal.json","masked-seal.json","reader-initial-seal.json"]:
        s=readj("evidence/"+n);bad=[k for k,v in s["files"].items() if not (P/k).exists() or sha(P/k)!=v]
        chk("immutable_"+n,not bad,"evidence/"+n,json.dumps(dict(files=len(s["files"]),mismatches=bad)))
    required=["SCOPE.md","manifest.json","frame.csv","questions.jsonl","routes.jsonl","visits.jsonl","returns.jsonl","judgments.csv","pairs.csv","sources.jsonl","RESULT.md","SELF_CHECK.md","PROGRESS.md","evidence/acceptance-evidence.json","evidence/failure-trace.jsonl"]
    if a.handoff:required+=["HANDOFF.md"]
    chk("required_files_present",all((P/n).exists() for n in required),required)
    r=subprocess.run([sys.executable,"-B",str(P/"recount.py"),"--check"],cwd=REPO,capture_output=True,text=True)
    chk("deterministic_recount_matches_saved_files",r.returncode==0,"recount.py --check",r.stdout+r.stderr)
    facts=readj("evidence/report-facts.json");shape=readj("evidence/result-table-shape.json")
    chk("independent_denominator12",facts["independent_events"]==12,"evidence/report-facts.json")
    chk("36_observations_44_candidates_381_predicates_762_surfaces",all(facts["source_counts"][k]==v for k,v in {"original_route_observations":36,"candidate_rows":44,"predicate_rows":381,"surface_judgments":762}.items()),"evidence/source-counts.json")
    pairs=list(csv.DictReader((P/"pairs.csv").open()));preds=list(csv.DictReader((P/"judgments.csv").open()))
    chk("csv_row_counts",len(pairs)==12 and len(preds)==381,["pairs.csv","judgments.csv"])
    chk("all_non_supported_predicates_have_reason_and_next_source",all(p["missing_or_conflict"] and p["next_minimum_source"] not in ("","null") for p in preds if p["returned_status"]!="supported"),"judgments.csv","No unseen facts are converted to support.")
    # Verify all full scopes against independent event/candidate conjunctions.
    cs=rows("evidence/candidate-decisions.jsonl")
    for scope in ["partial","whole"]:
        for surf in ["opened","returned"]:
            for rt in "CAB":
                count=sum(any(c[scope+"_verdict_"+surf]=="supported" for c in cs if c["question_id"]==p["question_id"] and c["route"]==rt) for p in pairs)
                st=next(x for x in facts["strata"] if x["label"]=="all_12_"+scope+("_opened" if surf=="opened" else ""))
                chk(f"{rt}_{scope}_{surf}_event_count",count==st["successes"][rt],"pairs.csv",f"{count}/12")
    trace=rows("evidence/failure-trace.jsonl")
    chk("failure_trace36_unique",len(trace)==36 and len({(t["question_id"],t["route"]) for t in trace})==36,"evidence/failure-trace.jsonl")
    cby={c["candidate_token"]:c for c in cs};bad=[]
    for t in trace:
        for c in t["returned_candidates"]:
            now=cby[c["candidate_token"]]
            if any(c[k]!=now[k] for k in ["partial_verdict_opened","partial_verdict_returned","whole_verdict_opened","whole_verdict_returned"]):bad.append(c["candidate_token"])
    chk("failure_trace_does_not_change_candidate_scores",not bad,"evidence/failure-trace.jsonl",str(bad))
    source=(P/"sources.jsonl").read_bytes().splitlines(keepends=True);old=b"".join(source[:121]);supp=b"".join(source[121:])
    original=readj("evidence/observation-assembly.json")["output_artifacts"]["sources.jsonl"]["sha256"]
    chk("source_prefix_preserved",hashlib.sha256(old).hexdigest()==original,"sources.jsonl first121 rows")
    chk("source_suffix_exact_supplement",supp==(P/"supplementary/sources.jsonl").read_bytes(),"sources.jsonl after121")
    cnt=facts["source_counts"];chk("qualified_source_minima",cnt["first_design_groups"]>=12 and cnt["returned_AB_supplier_groups"]>=12 and cnt["cross_field_groups"]>=4 and cnt["qualified_union_groups"]>=28,"evidence/source-counts.json",str(cnt["qualified_union_groups"]))
    chk("64_raw_flag_count_not_substantive_total",cnt["raw_direct_flag_groups"]==64 and cnt["all_direct_document_groups"]==59,"evidence/source-counts.json")
    overlay=rows("evidence/visit-classification-corrections.jsonl");raw={v["visit_id"]:v for v in rows("visits.jsonl")}
    audit=readj("audits/final-recount-crosscheck.json")["response_classification"]["proposed_corrections"]
    chk("all12_response_corrections_match_audited_ids",{v["visit_id"] for v in overlay}=={v["visit_id"] for v in audit} and len(overlay)==12,["evidence/visit-classification-corrections.jsonl","audits/final-recount-crosscheck.json"])
    chk("correction_original_values_match_preserved_visits",all(raw[c["visit_id"]]["substantive_original_body_read"]==c["original_substantive"] and raw[c["visit_id"]]["metadata_or_unusable_body_response"]==c["original_metadata_or_unusable"] for c in overlay),"visits.jsonl")
    cost=facts["strata"][0]["costs"]
    chk("corrected_body_response_counts",[(cost[r]["substantive_original_body_responses"],cost[r]["metadata_or_unusable_body_responses"]) for r in "CAB"]==[(20,1),(25,3),(17,9)],"evidence/report-facts.json")
    chk("requests_dual_debits_reconcile116",sum(cost[r]["navigation"]+cost[r]["body_opens"]-cost[r]["dual_debit_operations"] for r in "CAB")==116,"routes.jsonl")
    chk("response_categories_reconcile116",sum(cost[r]["substantive_original_body_responses"]+cost[r]["metadata_or_unusable_body_responses"]+cost[r]["failed_body_open_attempts"] for r in "CAB")+36==116,"evidence/report-facts.json","36 searches +62 substantive +13 metadata +5 failed responses.")
    budget=facts["budget"]
    chk("find_alternative_four_violations_eight_pairs",set(budget["find_as_navigation_violations"])=={"Q06-B","Q07-B","Q09-A","Q11-B"} and len(budget["find_as_navigation_compliant_pairs"])==8,"evidence/report-facts.json#budget")
    # Validate table boundaries rather than counting wrapped source text as rows.
    result=(P/"RESULT.md").read_text();lines=result.splitlines();tables=[];cur=[]
    for line in lines:
        if line.startswith("|"):cur.append(line)
        elif cur:tables.append(cur);cur=[]
    if cur:tables.append(cur)
    chk("title_immediately_followed_by_required_table",lines[0].startswith("# ") and next(x for x in lines[1:] if x.strip()).startswith("| 질문 ID·전체/부분"),"RESULT.md")
    chk("required_table_order_rows",[len(t)-2 for t in tables[:3]]==[12,51,len(facts["strata"])] and [len(re.split(r"(?<!\\)\|",t[0]))-2 for t in tables[:3]]==[8,7,6],"RESULT.md",str([len(t)-2 for t in tables[:3]]))
    chk("all12_events_in_first_table",{re.match(r"\| (Q\d+)",l)[1] for l in tables[0][2:]}=={f"Q{i:02d}" for i in range(1,13)},"RESULT.md")
    for name in ["RESULT.md"]+(["HANDOFF.md"] if a.handoff else []):
        ls=(P/name).read_text().rstrip().splitlines();tail=[];i=len(ls)-1
        while i>=0 and ls[i].startswith("|"):tail.insert(0,ls[i]);i-=1
        chk(name+"_ends_with_exact3_weakness_rows",len(tail)==5 and tail[0].startswith("| 가장 중요한 불일치 또는 약점"),name)
    selfcheck=(P/"SELF_CHECK.md").read_text()
    chk("selfcheck_all_method_questions",all(f"연구 Q{i}" in selfcheck for i in range(1,9)),"SELF_CHECK.md")
    chk("selfcheck_required_columns","| 주장 | 근거 주소·위치 또는 탐색 실패 영수증 | 자기 결론을 뒤집을 조건 | 실제 반증을 찾은 경로와 결과 | 남은 미확인 |" in selfcheck,"SELF_CHECK.md")
    ac=readj("evidence/acceptance-evidence.json")
    chk("acceptance_schema_boolean_conditions",all(isinstance(c["met"],bool) and all(k in c for k in ["condition","evidence","note"]) for c in ac["conditions"]),"evidence/acceptance-evidence.json")
    chk("gaps_not_hidden",sum(not c["met"] for c in ac["conditions"])==8 and ac["status"]==facts["status"]=="REVIEW_READY_WITH_GAPS","evidence/acceptance-evidence.json")
    chk("zero_denominators_NA",all(x["condition_status"]=="해당 없음" for x in facts["strata"] if x["n"]==0),"evidence/report-facts.json")
    chk("postseal_probes_not_experimental_visits",len(rows("visits.jsonl"))==116 and not any(v["route"] not in "CAB" for v in rows("visits.jsonl")),"visits.jsonl")
    prior=readj("evidence/prior025-event-exclusion.json");chk("prior025_twelve_events_distinct",len(prior["prior_events"])==12 and not prior["exact_initial_url_overlap"],"evidence/prior025-event-exclusion.json")
    # Every file changed from the original assigned integration, including untracked work, is owned.
    base="172c6bc37bdf91b91c86b9b3be29cb5b44fa4971"
    changed=set(subprocess.check_output(["git","diff","--name-only",base],cwd=REPO,text=True).splitlines())
    changed.update(subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=REPO,text=True).splitlines())
    chk("all_authored_paths_owned",all(x.startswith("docs/workstreams/research/AF-RES-029/") for x in changed),"git diff base; git ls-files --others",str(len(changed)))
    head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=REPO,text=True).strip()
    report=dict(checked_utc=datetime.now(timezone.utc).isoformat(),target_head=head,input_state="Current worktree; hashes below pin any not-yet-committed report inputs.",command="python -B docs/workstreams/research/AF-RES-029/validate_results.py",handoff_mode=a.handoff,
        checks=checks,failed_conditions=[c["condition"] for c in checks if not c["met"]],method_gaps_are_not_test_failures=True,
        input_hashes={n:sha(P/n) for n in required if (P/n).is_file()})
    if a.output:
        f=(P/a.output).resolve();assert f.is_relative_to(P);f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"target_head":head,"checks":len(checks),"failed":report["failed_conditions"]},ensure_ascii=False))
    return int(bool(report["failed_conditions"]))
if __name__=="__main__":raise SystemExit(main())
