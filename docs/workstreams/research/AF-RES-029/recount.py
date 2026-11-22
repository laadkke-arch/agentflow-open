"""Deterministic AF-RES-029 evidence join. No web queries or semantic inference.

The frozen input/route ledgers are not rewritten. Initial masked judgments stay
separate from exposed append-only reconciliation. --check compares generated
bytes with the committed/reporting files and fails on a mismatch.
"""
import argparse, copy, csv, hashlib, io, json
from collections import Counter
from pathlib import Path
from urllib.parse import urldefrag

P = Path(__file__).resolve().parent
def readj(path): return json.loads((P / path).read_text())
def rows(path): return [json.loads(x) for x in (P / path).read_text().splitlines() if x.strip()]
def norm(url): return urldefrag(url)[0]
def dump(obj): return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
def jline(obj): return json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n"
def csvtext(rs, fields):
    s=io.StringIO(newline=""); w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n");w.writeheader()
    for r in rs: w.writerow({k:(json.dumps(r.get(k),ensure_ascii=False,sort_keys=True) if isinstance(r.get(k),(list,dict)) else r.get(k,"")) for k in fields})
    return s.getvalue()
def verdict(ps, surface):
    vals=[x[surface+"_status"] for x in ps]
    assert vals and all(x in ("supported","conflict","unverified") for x in vals)
    return "conflict" if "conflict" in vals else "unverified" if "unverified" in vals else "supported"
def event_status(cs, scope, surface):
    vals=[c[scope+"_verdict_"+surface] for c in cs]
    return "empty" if not vals else "supported" if "supported" in vals else "unverified" if "unverified" in vals else "conflict"
def success(cs, scope="partial", surface="returned"): return event_status(cs,scope,surface)=="supported"
def top1_success(cs, first, scope="partial"):
    if not first:return False
    first=norm(first)
    for c in cs:
        ps=[x for x in c["predicates"] if x["scope"]==scope]
        if ps and all(x["returned_status"]=="supported" and any(set(map(norm,s)) <= {first} for s in x["returned_support_sets"]) for x in ps): return True
    return False
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");args=ap.parse_args()
    qs=rows("questions.jsonl"); qmap={q["id"]:q for q in qs}
    returns={(r["question_id"],r["route"]):r for r in rows("returns.jsonl")}
    route={(r["question_id"],r["route"]):r for r in rows("routes.jsonl")}
    visit_corrections=rows("evidence/visit-classification-corrections.jsonl")
    visits_by_id={v["visit_id"]:v for v in rows("visits.jsonl")}
    for vc in visit_corrections:
        v=visits_by_id[vc["visit_id"]];assert v["substantive_original_body_read"]==vc["original_substantive"]
        ctr=route[(vc["question_id"],vc["route"])]["actual_counters"]
        ctr["substantive_original_body_responses"]+=int(vc["corrected_substantive"])-int(vc["original_substantive"])
        ctr["metadata_or_unusable_body_responses"]+=int(vc["corrected_metadata_or_unusable"])-int(vc["original_metadata_or_unusable"])
    key=readj("judging/key.json")["packets"]
    masked=[]
    for reader in (1,2,3):
        masked+=rows(f"judging/reader_{reader}/judgments.jsonl")
    assert len(masked)==36 and len({r["packet_id"] for r in masked})==36
    corrections=rows("judging/reconciliation.jsonl") if (P/"judging/reconciliation.jsonl").exists() else []
    correction_map={}
    for c in corrections:
        if c.get("kind")!="predicate_correction":continue
        k=(c["packet_id"],c["candidate_token"],c["predicate_id"])
        assert k not in correction_map
        correction_map[k]=c
    joined=[]; observations={}; initial_top1={}; predicate_rows=[]; line_checks=[]
    evidence={f.stem:json.loads(f.read_text()) for f in (P/"judging/evidence").glob("*.json")}
    for raw in masked:
        r=copy.deepcopy(raw); pid=r["packet_id"]; km=key[pid];qid=km["question_id"];rt=km["route"]
        assert r["question_id"]==qid
        initial_top1[(qid,rt)]=top1_success(raw["candidates"],km["first_document_url"])
        pkt=readj(f"judging/packets/{pid}.json")
        assert {c["candidate_token"] for c in r["candidates"]}==set(km["candidates"])
        pcs={c["candidate_token"]:c for c in pkt["candidates"]}
        cs=[]
        for c in r["candidates"]:
            tok=c["candidate_token"];ck=km["candidates"][tok]; pc=pcs[tok]
            required={p["id"] for scope in ("partial","whole") for p in qmap[qid][scope+"_must"]}
            assert {p["predicate_id"] for p in c["predicates"]}==required,(qid,tok,"predicate coverage")
            assert len(c["predicates"])==len(required)
            for pd in c["predicates"]:
                corr=correction_map.get((pid,tok,pd["predicate_id"]))
                if corr:
                    for k,v in corr["changes"].items():pd[k]=v
                for surface in ("opened","returned"):
                    assert pd[surface+"_status"] in ("supported","conflict","unverified")
                    evs=pd.get(surface+"_evidence",[])
                    for e in evs:
                        eid=e.get("evidence_id")
                        if eid:
                            assert eid in evidence,(qid,tok,eid)
                            assert eid in {v["evidence_id"] for v in pkt["opened_evidence"]},(qid,tok,"outside packet evidence",eid)
                        if surface=="returned" and e.get("url"):
                            assert norm(e["url"]) in {norm(z["url"]) for z in pc["citations"]},(qid,tok,"uncited document",e)
                    sets=pd.get(surface+"_support_sets",[])
                    if pd[surface+"_status"]=="supported":
                        assert sets,(qid,tok,pd["predicate_id"],"no support sets")
                        if surface=="returned":
                            assert all(set(map(norm,s)) <= {norm(z["url"]) for z in pc["citations"]} for s in sets)
                    else: assert not sets,(qid,tok,pd["predicate_id"],"unsupported has sufficient sets")
                row=dict(judgment_id=f"{qid}-{rt}-{ck['original_rank']:02d}-{pd['predicate_id']}",question_id=qid,route=rt,original_rank=ck["original_rank"],
                    packet_id=pid,candidate_token=tok,candidate_name=c["name"],scope=pd["scope"],predicate_id=pd["predicate_id"],
                    frozen_predicate=pd.get("requirement",pd.get("frozen_predicate",next(x["predicate"] for x in qmap[qid][pd["scope"]+"_must"] if x["id"]==pd["predicate_id"]))),
                    opened_status=pd["opened_status"],returned_status=pd["returned_status"],opened_evidence=pd.get("opened_evidence",[]),
                    returned_evidence=pd.get("returned_evidence",[]),opened_support_sets=pd.get("opened_support_sets",[]),returned_support_sets=pd.get("returned_support_sets",[]),
                    missing_or_conflict=pd.get("missing_or_conflict"),next_minimum_source=pd.get("next_minimum_source"),novelty=c["novelty"],
                    reader=raw["reader"],reading_type="initial separate same-model masked context" if not corr else "exposed append-only reconciliation",
                    original_judgment_file=f"judging/{raw['reader']}/judgments.jsonl",exposure=r.get("exposure_notes"),correction_id=corr.get("correction_id") if corr else "")
                predicate_rows.append(row)
            for scope in ("partial","whole"):
                for surface in ("opened","returned"):
                    expected=verdict([x for x in c["predicates"] if x["scope"]==scope],surface)
                    if not any((pid,tok,x["predicate_id"]) in correction_map for x in c["predicates"]):assert c[scope+"_verdict_"+surface]==expected,(qid,tok,scope,surface)
                    c[scope+"_verdict_"+surface]=expected
            st=readj(f"common/{qid}/start.json")
            prefixes=st.get("allowed_url_prefixes", [v for z in st.get("allowed_providers",[]) for v in z["prefixes"]])
            urls=list(dict.fromkeys(norm(z["url"]) for z in pc["citations"]))
            isknown=[any(u.startswith(p) for p in prefixes) for u in urls]
            provider_relation="known_common_provider" if isknown and all(isknown) else "mixed_known_external" if any(isknown) else "outside_common_provider"
            c.update(question_id=qid,route=rt,original_rank=ck["original_rank"],packet_id=pid,reader=raw["reader"],
                     citations=pc["citations"],original_document_urls=urls,provider_relation=provider_relation,
                     first_route_document=km["first_document_url"],prior_025_exact_overlap=False,
                     prior_025_family_overlap=(qid=="Q02" or (qid=="Q08" and "Bazel" in c["name"]) or qid=="Q03"),
                     practical_caller_caveat=(qid=="Q01"))
            cs.append(c);joined.append(c)
        cs.sort(key=lambda x:x["original_rank"]);observations[(qid,rt)]=dict(packet_id=pid,candidates=cs,empty=not cs,exposure_notes=r.get("exposure_notes"),reader=raw["reader"],empty_reason=r.get("empty_reason",r.get("empty_reason_or_limit","")))
    joined.sort(key=lambda x:(x["question_id"],"CAB".index(x["route"]),x["original_rank"]))
    predicate_rows.sort(key=lambda x:(x["question_id"],"CAB".index(x["route"]),x["original_rank"],x["scope"],x["predicate_id"]))
    pairs=[]
    exposure_audit=readj("audits/resume-exposure-overlap.json")
    sampling_exposed=set(exposure_audit["event_sets"]["sampling_outcome_or_later_recovery_exposed"]["excluded_events"])
    strict_exposed=set(exposure_audit["event_sets"]["strict_any_recorded_current_status_followup_exposed"]["excluded_events"])
    alt_violations={f"{q}-{r}" for (q,r),v in route.items() if r!="C" and v["cost_sensitivity"]["A_B_exceeds_two_navigation_operations"]}
    for q in qs:
        qid=q["id"];pr=dict(question_id=qid,ledger=q["ledger"],original_scope=q["scope"],period=q["period"],independent_unit="one first-design event",
            common_readable_official=(qid!="Q02"),sampling_outcome_exposed=qid in sampling_exposed,strict_status_followup_exposed=qid in strict_exposed,
            opposite_route_exposure_recorded=False,same_worker_memory_possible=True,strict_find_budget_pair_compliant=all(f"{qid}-{rt}" not in alt_violations for rt in "AB"),
            prior_025_exact_event_overlap=False,Q01_practical_Go_adapter_unverified=(qid=="Q01"))
        for rt in "CAB":
            cs=observations[(qid,rt)]["candidates"];rr=route[(qid,rt)]
            for scope in ("partial","whole"):
                for surface in ("opened","returned"):
                    pr[f"{rt}_{scope}_{surface}"]=int(success(cs,scope,surface))
                    pr[f"{rt}_{scope}_{surface}_status"]=event_status(cs,scope,surface)
                pr[f"{rt}_{scope}_top1_returned"]=int(top1_success(cs,rr["returned_document_urls_in_original_order"][0] if rr["returned_document_urls_in_original_order"] else None,scope))
            pr[f"{rt}_partial_top1_initial_reader"]=int(initial_top1[(qid,rt)])
            pr[f"{rt}_partial_new_target"]=int(success([c for c in cs if c["novelty"]=="new_target"]))
            pr[f"{rt}_partial_new_component"]=int(success([c for c in cs if c["novelty"]=="new_component_in_named_family"]))
            pr[f"{rt}_partial_same_named_use"]=int(success([c for c in cs if c["novelty"]=="same_named_use"]))
            pr[f"{rt}_partial_known_provider"]=int(success([c for c in cs if c["provider_relation"]=="known_common_provider"]))
            pr[f"{rt}_partial_external_provider"]=int(success([c for c in cs if c["provider_relation"]=="outside_common_provider"]))
            pr[f"{rt}_empty"]=int(not cs)
            pr[f"{rt}_candidate_count"]=len(cs)
            for k,v in rr["actual_counters"].items():
                if k in ["navigation","body_opens","web_operations","substantive_original_body_responses","failed_body_open_attempts","metadata_or_unusable_body_responses","document_url_count","within_page_find_operations","tool_elapsed_ms_sum","dual_debit_operations"]:pr[f"{rt}_{k}"]=v
            pr[f"{rt}_started_utc"]=rr.get("started_utc")
            pr[f"{rt}_ended_utc"]=rr.get("ended_utc")
            pr[f"{rt}_top1_url"]=rr["returned_document_urls_in_original_order"][0] if rr["returned_document_urls_in_original_order"] else ""
            pr[f"{rt}_returned_document_urls"]=rr["returned_document_urls_in_original_order"]
        a,b=pr["A_partial_returned"],pr["B_partial_returned"]
        pr["partial_pair"]="both_success" if a and b else "A_win" if a else "B_win" if b else "both_no_success"
        pr["whole_pair"]="both_no_success"
        pr["A_partial_increment_over_common"]=int(a and not pr["C_partial_returned"])
        pr["B_partial_increment_over_common"]=int(b and not pr["C_partial_returned"])
        pairs.append(pr)
    def agg(label, sub, scope="partial",surface="returned", suffix=None, practical=False):
        suf=suffix or f"{scope}_{surface}"
        def val(p,rt):return 0 if practical and p["question_id"]=="Q01" else p[f"{rt}_{suf}"]
        n=len(sub);a=sum(val(p,"A") for p in sub);b=sum(val(p,"B") for p in sub);c=sum(val(p,"C") for p in sub)
        both=sum(bool(val(p,"A") and val(p,"B")) for p in sub)
        no=sum(not val(p,"A") and not val(p,"B") for p in sub)
        aw=sum(bool(val(p,"A") and not val(p,"B")) for p in sub);bw=sum(bool(val(p,"B") and not val(p,"A")) for p in sub)
        costs={rt:{k:sum(p[f"{rt}_{k}"] for p in sub) for k in ["navigation","body_opens","web_operations","substantive_original_body_responses","failed_body_open_attempts","metadata_or_unusable_body_responses","document_url_count","within_page_find_operations","tool_elapsed_ms_sum","dual_debit_operations"]} for rt in "CAB"}
        return dict(label=label,events=[p["question_id"] for p in sub],n=n,condition_status="applicable" if n else "해당 없음",scope=scope,surface=surface,score_column=suf,
            successes=dict(C=c,A=a,B=b),both_success=both,both_no_success=no,A_win=aw,B_win=bw,empty={rt:sum(p[f"{rt}_empty"] for p in sub) for rt in "CAB"},costs=costs,unknowns_retained_in_denominator=True)
    strata=[agg("all_12_partial",pairs),agg("all_12_whole",pairs,"whole"),agg("all_12_partial_opened",pairs,surface="opened"),
        agg("all_12_whole_opened",pairs,"whole","opened"),agg("readable_common_11", [p for p in pairs if p["common_readable_official"]]),
        agg("strict_find_budget_pairs", [p for p in pairs if p["strict_find_budget_pair_compliant"]]),
        agg("sampling_outcome_excluded", [p for p in pairs if not p["sampling_outcome_exposed"]]),
        agg("strict_status_followup_excluded", [p for p in pairs if not p["strict_status_followup_exposed"]]),
        agg("recorded_opposite_route_excluded", [p for p in pairs if not p["opposite_route_exposure_recorded"]]),
        agg("fully_fresh_pair_only",[]),
        agg("prior025_broad_family_excluded",[p for p in pairs if p["question_id"] not in ("Q02","Q03","Q08")]),
        agg("top_first_URL",pairs,suffix="partial_top1_returned"),agg("top_first_URL_initial_reader_interpretation",pairs,suffix="partial_top1_initial_reader"),agg("Q01_caller_boundary_required",pairs,practical=True)]
    for ledger in ["go","python","numpy"]:
        sub=[p for p in pairs if p["ledger"].lower()==ledger];strata += [agg("ledger_"+ledger,sub),agg("ledger_"+ledger+"_whole",sub,"whole")]
    for scope in ["whole","partial"]:
        sub=[p for p in pairs if p["original_scope"]==scope];strata +=[agg("request_"+scope,sub),agg("request_"+scope+"_whole_support",sub,"whole")]
    for suffix in ["partial_new_target","partial_new_component","partial_same_named_use","partial_known_provider","partial_external_provider"]:
        strata.append(agg(suffix,pairs,suffix=suffix))
    source_rows=rows("sources.jsonl");base=readj("evidence/observation-assembly.json")
    first={r["duplicate_group"] for r in source_rows if r.get("counted_initial_minimum")}
    supplier={r["duplicate_group"] for r in source_rows if r.get("counted_supplier_AB_minimum")}
    cross={r["duplicate_group"] for r in source_rows if r.get("counted_cross_field_minimum")}
    all_direct_raw={r["duplicate_group"] for r in source_rows if r.get("direct_read")}
    all_direct={r["duplicate_group"] for r in source_rows if r.get("counted_initial_minimum") or r.get("supplier_original_count_eligible") or r.get("schema")=="AF-RES-029-supplementary-v1"}
    source_counts=dict(source_rows=len(source_rows),attempt_rows=len(rows("attempts.jsonl")),first_design_groups=len(first),returned_AB_supplier_groups=len(supplier),cross_field_groups=len(cross),
        qualified_union_groups=len(first|supplier|cross),all_direct_document_groups=len(all_direct),raw_direct_flag_groups=len(all_direct_raw),excluded_nonoriginal_group_ids=sorted(all_direct_raw-all_direct),independent_design_events=12,cross_field_cases=2,
        original_route_observations=36,original_AB_observations=24,candidate_rows=len(joined),predicate_rows=len(predicate_rows),surface_judgments=2*len(predicate_rows),
        experimental_web_operations=len(rows("visits.jsonl")),counting_limits="Repeated URLs, excerpts, first-design reuse, post-seal rereads, failures and snippets do not enlarge the required groups.",
        by_question=[dict(question_id=q,first_design_groups=len({r["duplicate_group"] for r in source_rows if r.get("counted_initial_minimum") and q in r.get("linked_questions",[])}),
            returned_AB_supplier_groups=len({r["duplicate_group"] for r in source_rows if r["duplicate_group"] in supplier and any(m["question_id"]==q and m["route"] in ("A","B") for m in r.get("returned_membership",[]))}),
            direct_document_groups=len({r["duplicate_group"] for r in source_rows if r["duplicate_group"] in all_direct and q in r.get("linked_questions",[])})) for q in qmap])
    facts=dict(schema="AF-RES-029-final-recount-v1",basis="Initial masked judgments plus explicit exposed reconciliation; no new search evidence",
        status="REVIEW_READY_WITH_GAPS",independent_events=12,source_counts=source_counts,strata=strata,
        budget=dict(original_declared_compliant_AB=24,body_and_URL_compliant_AB=24,find_as_navigation_violations=sorted(alt_violations),
            find_as_navigation_compliant_AB=24-len(alt_violations),find_as_navigation_compliant_pairs=[p["question_id"] for p in pairs if p["strict_find_budget_pair_compliant"]],
            server_transfer_bytes="미계측",server_token_cost="미계측",local_serialized_bytes_not_transfer=True),
        candidate_verdicts={scope+"_"+surface:dict(Counter(c[scope+"_verdict_"+surface] for c in joined)) for scope in ("partial","whole") for surface in ("opened","returned")},
        predicate_verdicts={surface:dict(Counter(p[surface+"_status"] for p in predicate_rows)) for surface in ("opened","returned")},
        novelty_candidate_counts=dict(Counter(c["novelty"] for c in joined)),
        semantics_are_documentary_not_runtime=True,independent_human_readers=0,same_model_separate_masked_readers=3,
        empty_observations=[f"{q}-{rt}" for (q,rt),o in sorted(observations.items()) if o["empty"]],
        corrections_applied=len(correction_map),visit_classification_corrections=len(visit_corrections),source_count_basis="Append-only sources.jsonl; counted flags and conservative duplicate groups, not search hit counts.",
        input_hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ["questions.jsonl","returns.jsonl","routes.jsonl","visits.jsonl","sources.jsonl","judging/key.json","judging/reconciliation.jsonl","audits/resume-exposure-overlap.json","evidence/visit-classification-corrections.jsonl"]+[f"judging/reader_{i}/judgments.jsonl" for i in (1,2,3)]})
    outputs={
      "judgments.csv":csvtext(predicate_rows,list(predicate_rows[0])),
      "pairs.csv":csvtext(pairs,list(pairs[0])),
      "evidence/candidate-decisions.jsonl":"".join(jline(c) for c in joined),
      "evidence/observation-decisions.jsonl":"".join(jline(dict(question_id=q,route=rt,**{k:v for k,v in o.items() if k!="candidates"},
          candidate_tokens=[c["candidate_token"] for c in o["candidates"]],
          **{scope+"_"+surface:event_status(o["candidates"],scope,surface) for scope in ("partial","whole") for surface in ("opened","returned")})) for (q,rt),o in sorted(observations.items())),
      "evidence/report-facts.json":dump(facts),
      "evidence/source-counts.json":dump(source_counts)}
    changed=[]
    for name,txt in outputs.items():
        f=P/name
        if not f.exists() or f.read_text()!=txt:
            changed.append(name)
            if not args.check:f.parent.mkdir(parents=True,exist_ok=True);f.write_text(txt)
    print(json.dumps(dict(mode="check" if args.check else "write",events=len(pairs),observations=len(observations),candidates=len(joined),predicate_rows=len(predicate_rows),different_files=changed,
        primary=strata[0]["successes"],top1=next(x for x in strata if x["label"]=="top_first_URL")["successes"]),ensure_ascii=False))
    return int(bool(changed)) if args.check else 0
if __name__=="__main__":raise SystemExit(main())
