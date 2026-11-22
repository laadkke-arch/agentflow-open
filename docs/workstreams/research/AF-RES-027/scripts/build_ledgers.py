"""Build the unified ledgers and denominator counts from fixed collector records.
No external software is installed or executed; dates measure only labelled endpoints.
"""
import collections,copy,csv,json
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(name): return json.loads((ROOT/name).read_text())
def keyed(rows,key="reference_id"): return {r[key]:r for r in rows}
def compact(x):
    if x is None: return ""
    if isinstance(x,(dict,list)):return json.dumps(x,ensure_ascii=False,separators=(",",":"))
    if isinstance(x,bool):return str(x).lower()
    return x
def write_csv(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT/name).open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
        w.writerows({k:compact(v) for k,v in r.items()} for r in rows)
def time_of(point): return (point or {}).get("time",(point or {}).get("date"))
def url_of(point):return (point or {}).get("url")
def delta(a,b):return (datetime.fromisoformat(b.replace("Z","+00:00"))-datetime.fromisoformat(a.replace("Z","+00:00"))).total_seconds()
def mask_text(x):
    if isinstance(x,dict):return "; ".join(str(k)+": "+str(v) for k,v in x.items())
    return x or "미확인"

def main():
    refs=[json.loads(x) for x in (ROOT/"references.jsonl").read_text().splitlines()]
    refmap=keyed(refs)
    sources=read("sources.json"); smap={s["source_id"]:s for s in sources}
    def urls(ids):return list(dict.fromkeys(smap[i]["original_url"] for i in ids if i in smap))
    hu=keyed(read("collectors/homebrew/upstream.json")); hc=keyed(read("collectors/homebrew/chains.json"));hv=keyed(read("collectors/homebrew/verdicts.json"))
    cu=keyed(read("collectors/conda/upstream.json"));cc=keyed(read("collectors/conda/chains.json"));cv=keyed(read("collectors/conda/verdicts.json"))
    bh=keyed(read("collectors/homebrew-b/cases.json"),"case_id")
    bc=keyed(read("collectors/conda-b/cases.json"),"case_id")
    upstream=[];chains=[];verdicts=[];intervals=[]
    for rid in sorted(hu|cu):
        ref=refmap[rid]; home=rid.startswith("A-H")
        u=(hu if home else cu)[rid]; c=(hc if home else cc)[rid];v=(hv if home else cv)[rid]
        deploy={} if home else u.get("deployment",{})
        event=u.get("event_id")
        sids=u.get("change_source_ids",u.get("source_ids",[]))
        if home: sids=[u["historical_recipe_source_id"]]+sids
        ur={"reference_id":rid,"sample":"A","ecosystem":ref["ecosystem"],"consumer_project":ref["consumer_project"],
            "event_id":event,"event_observed":bool(event),"relation":u["relation"],
            "relation_detail":u.get("relation_detail",u.get("identity_event_observation")),
            "old_reference_token":ref["raw_reference"],"historical_recipe_version":u.get("historical_version",(u.get("before") or {}).get("version")),
            "historical_recipe_url":u.get("historical_recipe_url",(u.get("before") or {}).get("url")),
            "before_commit":u.get("before_sha",(u.get("before") or {}).get("recipe_commit")),
            "after_commit":u.get("after_sha",(u.get("after") or {}).get("recipe_commit")),
            "after_version":(u.get("after") or {}).get("version"),
            "change_url":(u.get("upstream_source_urls") or [u.get("diff_url")])[0],
            "proposal_time":u.get("proposal_date",u.get("proposal_time")),
            "source_commit_time":u.get("source_commit_date",u.get("source_time")),
            "merge_time":u.get("merge_date",u.get("merge_time")),
            "artifact_available_lower":u.get("actual_user_effective_lower",deploy.get("time")),
            "artifact_available_upper":u.get("actual_user_effective_upper",deploy.get("time_upper",deploy.get("time"))),
            "artifact_available_url":deploy.get("url"),"availability_meaning":u.get("actual_user_effective_status",deploy.get("kind")),
            "consumer_actual_exposure_time":None,"consumer_actual_exposure_status":"미확인; source recipe 또는 업로드와 실제 solver/실행을 구별",
            "source_url_status":"직접 읽은 고정 Git 원문 또는 공식 API; sources의 실패 행과 구별",
            "normalized_catalog_url":ref["normalized_catalog_url"],"literal_consumer_catalog_url_present":False,
            "normalized_catalog_html_status":"미확인; 원래 참조는 package/channel 문자열이며 정규화 URL은 연구자가 생성",
            "output_before":u.get("output_before",u.get("original_reference")),
            "output_after":u.get("output_after",u.get("notes")),"expected_function":ref["purpose"],
            "source_ids":sids,"evidence_urls":urls(sids),
            "limits":u.get("actual_user_effective_reason",u.get("limits")),
            "collector_details":u}
        if rid=="A-H02":ur["proposal_time"]="2024-10-18T16:38:49Z";ur["source_ids"]+=["BH-S04"]
        if rid=="A-H06":ur["proposal_time"]="2021-01-04T05:50:42Z";ur["source_ids"]+=["BH-S05"]
        ur["evidence_urls"]=urls(ur["source_ids"])
        upstream.append(ur)
        t0=c.get("T0",{});tu=c.get("Tu") or {};to=c.get("first_consumer_observation",c.get("To")) or {}
        tc=c.get("consumer_correction_commit",c.get("Tc")) or {}
        tr=c.get("Tr") or {}
        last=c.get("last_confirmed_source") or {}
        window=c.get("window") or {}
        if home:
            tu={}
            # First observation must be a demonstrated state/report, not a speculative commit title.
            if rid=="A-H02":to={}
            if rid=="A-H01":to={**c["static_recheck"],"url":smap["H-U18"]["original_url"],"kind":"CURRENT_STATIC_CONTRADICTION_WITH_OLD_CALL; not historical failure date"}
        source_release=c.get("first_matching_corrected_release") if home else tr
        ch={"reference_id":rid,"sample":"A","ecosystem":ref["ecosystem"],"consumer_project":ref["consumer_project"],"event_id":event,
            "T0":time_of(t0),"T0_url":url_of(t0),
            "Tu":time_of(tu),"Tu_upper":tu.get("time_upper"),"Tu_url":url_of(tu),
            "Tu_meaning":tu.get("kind",c.get("Tu_status")),"Tu_is_exact_consumer_exposure":False,
            "To":time_of(to),"To_url":url_of(to),"To_kind":to.get("kind",to.get("type")),
            "Tc":time_of(tc),"Tc_url":url_of(tc),"Tc_scope":tc.get("scope",tc.get("note")),
            "Tr":time_of(tr),"Tr_url":url_of(tr),"Tr_kind":tr.get("kind"),
            "Tr_exact_first_runtime_deployment":False,"known_source_release":source_release,
            "chain_status":c.get("chain_status"),"strict_five_point_complete":False,
            "window_start":window.get("start",window.get("start_lower",c.get("observation_window_start"))),
            "window_start_upper":window.get("start_upper",tu.get("time_upper")),
            "window_end":window.get("end",window.get("end_lower",c.get("observation_window_end"))),
            "window_end_upper":window.get("end_upper",window.get("end_upper_if_windows_artifact")),
            "window_anchor_limit":window.get("anchor_limitation",c.get("window_status","artifact availability, not exact consumer exposure")),
            "window_end_source":window.get("end_source_commit"),"window_end_source_url":window.get("end_source_url"),
            "last_confirmed_commit":last.get("sha",window.get("end_source_commit")),
            "last_confirmed_time":last.get("date",window.get("end_source_time")),
            "last_confirmed_url":last.get("url",window.get("end_source_url")),
            "after_window_first_known_change":c.get("after_window_first_known_change",c.get("after_window_first_known_correction")),
            "censoring":c.get("censoring"),"upstream_to_consumer_latency_eligible":False,
            "actual_human_misrecommendation_harm":"미확인",
            "next_immutable_input":c.get("next_immutable_input",c.get("next_minimum_evidence")),
            "collector_details":c}
        chains.append(ch)
        ab=v.get("record_ablation",{})
        evidence=v.get("minimal_evidence_source_ids",v.get("evidence_ids",[]))
        verdicts.append({"reference_id":rid,"sample":"A","ecosystem":ref["ecosystem"],"consumer_project":ref["consumer_project"],
            "verdict":v["verdict"],"verdict_scope":v.get("purpose_fit_scope",v.get("verdict_scope")),
            "failure_evidence_level":"DIRECT_PARTY_REPORT_FOR_SPECIFIED_ACTIVITY" if rid in ("A-C04","A-C06") else "NO_MATCHING_EXECUTED_FAILURE_VERIFIED",
            "intentional_historical_pin":"미확인; immutable reference/version constraint alone is not intent",
            "intentional_compatibility_pin":"temporary NumPy<1.19 explicitly for compatibility" if rid=="A-C04" else "미확인",
            "opposite_explanation":v.get("counterexplanation",v.get("alternative_explanation")),
            "L1_address_only":ab.get("address_only",mask_text(v.get("mask_L1"))),
            "L2_function_version":ab.get("with_expected_function_version",mask_text(v.get("mask_L2"))),
            "L3_source_time_relation":ab.get("with_source_history_and_times",mask_text(v.get("mask_L3"))),
            "minimal_evidence_ids":evidence,"minimal_evidence_urls":urls(evidence),
            "remaining_question":v.get("remaining_question",v.get("lightest_sufficient_for_identity",v.get("lightest_sufficient_for_need",v.get("lightest_sufficient_for_output")))),
            "independence":v.get("independence",v.get("author_lineage")),
            "actual_harm":"미확인","mask_method":"same-reader structural field masking; not independent blinded efficacy test",
            "collector_details":v})
        intervals.append({"interval_id":rid+"-TuTc","reference_id":rid,"sample":"A","reference_variant":"sealed original purpose",
          "metric":"upstream effective change → same-purpose consumer correction","eligible":False,"numeric_role":"NOT_ESTIMATED",
          "start":time_of(tu),"start_upper":tu.get("time_upper"),"end":time_of(tc),"lower_seconds":None,"upper_seconds":None,
          "source_ids":c.get("source_ids",u.get("change_source_ids",[])),
          "reason":c.get("latency_reason",c.get("censoring")),"censoring":c.get("censoring")})
    # B Homebrew overlaps are linked, never new A rows.
    aup=keyed(upstream);ach=keyed(chains);av=keyed(verdicts)
    for bid,aid in [("B-H01","A-H02"),("B-H03","A-H06")]:
        for dest,src in [(upstream,aup),(chains,ach),(verdicts,av)]:
            r=copy.deepcopy(src[aid]);r.update(reference_id=bid,sample="B",linked_A_reference=aid);dest.append(r)
    u2=bh["B-H02"];r2=refmap["B-H02"]
    upstream.append({"reference_id":"B-H02","sample":"B","ecosystem":"Homebrew","consumer_project":r2["consumer_project"],
        "event_id":"HB-PYTHON-DEFAULT-2020","event_observed":True,"relation":"VERSION_SUCCESSOR",
        "relation_detail":"default python/python3 switches3.7→3.8; old minor retained as versioned formula",
        "historical_recipe_version":"3.7.8","after_version":"3.8.3",
        "before_commit":"be1ba3b4ba9549afdaff7bd35f2649b9df04fd8a","after_commit":"56a265eb11a92c05efa050a565b5c9af1b97067c",
        "change_url":smap["BH-S02"]["original_url"],"proposal_time":"2020-05-18T19:28:26Z","source_commit_time":"2020-07-08T08:12:59Z",
        "merge_time":None,"artifact_available_lower":None,"artifact_available_upper":None,"availability_meaning":"미확인",
        "consumer_actual_exposure_status":"미확인","source_ids":u2["upstream_source_ids"],"evidence_urls":urls(u2["upstream_source_ids"]),
        "limits":"PR merged_at is null despite fixed source and merge-trigger comment; first actual distribution not established"})
    chains.append({"reference_id":"B-H02","sample":"B","ecosystem":"Homebrew","consumer_project":r2["consumer_project"],"event_id":"HB-PYTHON-DEFAULT-2020",
        "T0":u2["T0"],"T0_url":r2["consumer_file_url"],"Tu":None,"Tu_meaning":"미확인","To":u2["To"],"To_url":smap["BH-S10"]["original_url"],
        "To_kind":"SOURCE_REQUIREMENT_RETAINED","Tc":None,"Tr":None,"strict_five_point_complete":False,
        "chain_status":"PARTIAL_RETAINED_PURPOSE_UPSTREAM_DELIVERY_UNRESOLVED",
        "window_end":None,"window_anchor_limit":u2["provisional_observation_end"],
        "last_confirmed_commit":u2["last_verified_commit"],"last_confirmed_time":u2["To"],"last_confirmed_url":smap["BH-S10"]["original_url"],
        "censoring":u2["censoring"],"actual_human_misrecommendation_harm":"미확인","next_immutable_input":u2["next_required"],"collector_details":u2})
    verdicts.append({"reference_id":"B-H02","sample":"B","ecosystem":"Homebrew","consumer_project":r2["consumer_project"],
        "verdict":"MAINTAINED_FOR_PURPOSE","verdict_scope":"Python3.8 satisfies documented>=3.5/3.6 lower bound; actual execution unknown",
        "intentional_historical_pin":"미확인","opposite_explanation":"Borg cask/formula and FUSE edits concern different references/functions",
        "L1_address_only":"Same formula family does not reveal installed alias or Python minor",
        "L2_function_version":"Borg runtime/headers lower bound makes3.8 textually eligible",
        "L3_source_time_relation":"Distinguishes other install corrections and remembers alias-dependent upgrade behavior",
        "minimal_evidence_ids":["BH-S02","BH-S07","BH-S08","BH-S09","BH-S10","BH-S11"],
        "minimal_evidence_urls":urls(["BH-S02","BH-S07","BH-S08","BH-S09","BH-S10","BH-S11"]),
        "remaining_question":u2["next_required"],"actual_harm":"미확인"})
    for bid,c in sorted(bc.items()):
        u=c["upstream"];o=c["consumer"];event={"B-C01":"CF-MATPLOTLIB-ROOT-2019","B-C02":"CF-MAMBA-SPLIT-2021","B-C03":"CF-QT-META-2022"}[bid]
        upstream.append({"reference_id":bid,"sample":"B","ecosystem":"conda-forge","consumer_project":o["project"],"event_id":event,"event_observed":True,
            "relation":c["relation"],"relation_detail":c["selected_event"],"before_commit":u["before_commit"],"after_commit":u["after_commit"],
            "proposal_time":u["proposal_date"],"merge_time":u["merge_date"],"artifact_available_lower":u["deployment_date"],
            "artifact_available_upper":u["deployment_date"],"artifact_available_url":u["deployment_url"],"availability_meaning":u["deployment_scope"],
            "consumer_actual_exposure_status":"미확인; artifact contents checked, matching consumer execution not recovered",
            "output_after":u["artifact"],"source_ids":c["source_ids"],"evidence_urls":urls(c["source_ids"]),"collector_details":u})
        winurl=o.get("window_url")
        if not winurl and o.get("window_snapshot"):
            path=refmap[bid]["consumer_path"]
            winurl="https://github.com/"+o["project"]+"/blob/"+o["window_snapshot"]+"/"+path
        chains.append({"reference_id":bid,"sample":"B","ecosystem":"conda-forge","consumer_project":o["project"],"event_id":event,
            "T0":o["old_date"],"T0_url":o["old_url"],"Tu":u["deployment_date"],"Tu_url":u["deployment_url"],"Tu_meaning":u["deployment_scope"],
            "To":o.get("first_post_source_date"),"To_url":o.get("first_post_source_url"),"To_kind":"SOURCE_CHECKPOINT; not matching runtime",
            "Tc":None,"Tr":None,"strict_five_point_complete":False,"chain_status":"PARTIAL_NO_ORIGINAL_PURPOSE_CORRECTION_PROVEN",
            "window_start":u["deployment_date"],"window_end":o["window_end"],"window_end_source":o["window_snapshot"],"window_end_source_url":winurl,
            "last_confirmed_commit":o["window_snapshot"],"last_confirmed_time":o.get("window_snapshot_date"),"last_confirmed_url":winurl,
            "after_window_first_known_change":o.get("later_observation"),"censoring":c["censoring"],
            "actual_human_misrecommendation_harm":"미확인","next_immutable_input":c["next_first_action"],"collector_details":c})
        verdicts.append({"reference_id":bid,"sample":"B","ecosystem":"conda-forge","consumer_project":o["project"],
            "verdict":"UNDECIDABLE" if bid=="B-C03" else "MAINTAINED_FOR_PURPOSE","verdict_scope":c["verdict"],
            "intentional_historical_pin":"미확인","opposite_explanation":c["counterexample"],
            "L1_address_only":"Does not identify consumer output, API/CLI role, or version-matrix purpose",
            "L2_function_version":o["purpose"],"L3_source_time_relation":c["censoring"],
            "minimal_evidence_ids":c["source_ids"],"minimal_evidence_urls":urls(c["source_ids"]),
            "remaining_question":c["next_first_action"],"independence":c.get("independent_consumer_limit","distinct project; not full author-independence proof"),
            "actual_harm":"미확인","collector_details":c})
    # Exactly six B-primary denominators: append empty primary-event delays.
    for ch in chains:
        ch.setdefault("Tu_is_exact_consumer_exposure",False)
        ch.setdefault("Tr_exact_first_runtime_deployment",False)
        ch.setdefault("upstream_to_consumer_latency_eligible",False)
        if ch["sample"]=="B" and ch.get("Tu"):
            ch.setdefault("window_anchor_limit","selected artifact availability, not exact consumer exposure; contents or source checkpoint only")
    for bid in sorted(bh|bc):
        ch=next(x for x in chains if x["reference_id"]==bid)
        ur=next(x for x in upstream if x["reference_id"]==bid)
        intervals.append({"interval_id":bid+"-TuTc","reference_id":bid,"sample":"B","reference_variant":"original preselected B event/purpose",
           "metric":"upstream original event → same-purpose consumer correction","eligible":False,"numeric_role":"NOT_ESTIMATED",
           "start":ch.get("Tu"),"end":None,"lower_seconds":None,"upper_seconds":None,"source_ids":ur.get("source_ids",[]),"reason":ch.get("censoring"),"censoring":ch.get("censoring")})
    def measured(iid,rid,sample,variant,metric,start,end,sids,scope,role="SOURCE_PUBLICATION",eligible=True):
        seconds=delta(start,end)
        intervals.append({"interval_id":iid,"reference_id":rid,"sample":sample,"reference_variant":variant,
          "metric":metric,"eligible":eligible,"numeric_role":role,"start":start,"end":end,
          "lower_seconds":seconds,"upper_seconds":seconds,"lower_days":seconds/86400,"upper_days":seconds/86400,
          "source_ids":sids,"scope":scope,"runtime_effect_verified":False,"first_runtime_deployment_verified":False,"censoring":"not a runtime-delay claim"})
    c=cc["A-C04"]
    measured("A-C04-TcRC","A-C04","A","same docs-env correction","source edit → first observed published RC source edition",time_of(c["Tc"]),time_of(c["Tr"]),["C-F15","C-F18","C-F56"],"v1.1.0rc0 source file; rendered dev-docs deployment unknown")
    measured("A-C04-TcStable","A-C04","A","same docs-env correction","source edit → first observed stable source edition",time_of(c["Tc"]),time_of(c["first_stable_release"]),["C-F15","C-F20","C-F19"],"v1.1.0 source file; separate from RC and doc server")
    c=cc["A-C06"]
    measured("A-C06-TcSource","A-C06","A","same macOS dependency floor","source edit → first observed stable source edition",time_of(c["Tc"]),time_of(c["Tr"]),["C-F25","C-F29","C-F57"],"v5.3.2 source requirement; installer and GUI success unverified")
    # H02 arithmetic is deliberately INELIGIBLE as a first-publication interval.
    h=hc["A-H02"];r=h["first_matching_corrected_release"];t=time_of(h["consumer_correction_commit"])
    intervals.append({"interval_id":"A-H02-AssetMetadata","reference_id":"A-H02","sample":"A","reference_variant":"same Brewfile edit",
       "metric":"source edit → current asset created_at/updated_at values","eligible":False,"numeric_role":"METADATA_ARITHMETIC_ONLY",
       "start":t,"end":r["asset_created_at"],"end_upper":r["asset_updated_at"],
       "lower_seconds":delta(t,r["asset_created_at"]),"upper_seconds":delta(t,r["asset_updated_at"]),
       "lower_days":delta(t,r["asset_created_at"])/86400,"upper_days":delta(t,r["asset_updated_at"])/86400,
       "source_ids":["H-C01","H-R01","H-R02","R-S01"],"scope":"Content checked in actual archive; metadata is not a proved first-public-access bound",
       "censoring":"NOT_A_DISTRIBUTION_INTERVAL","runtime_effect_verified":False,"first_runtime_deployment_verified":False})
    # Retain the explicitly conditional NumPy arithmetic outside all primary delay counts.
    c=cc["A-C04"];ci=c["conditional_metadata_interval"]
    intervals.append({"interval_id":"A-C04-ConditionalMetadata","reference_id":"A-C04","sample":"A","reference_variant":"conditional Linux CPython artifacts",
        "metric":"conditional artifact upload → pin commit","eligible":False,"numeric_role":"CONDITIONAL_METADATA_ONLY",
        "start":c["Tu"]["time"],"start_upper":c["Tu"]["time_upper"],"end":c["Tc"]["time"],
        "lower_seconds":ci["lower_seconds"],"upper_seconds":ci["upper_seconds"],"lower_days":ci["lower_seconds"]/86400,"upper_days":ci["upper_seconds"]/86400,
        "source_ids":["C-F50","C-F15","C-F54"],"scope":ci["definition"],"reason":ci["why_conditional"],"runtime_effect_verified":False})
    aux=bc["B-C03"]["auxiliary_repair"]
    measured("B-C03-R2-UploadCommit","B-C03","B_AUX","R2 Python3.11/PyQt5.15; NOT original Qt5.12 purpose",
      "selected Linux repair artifact upload → source restoration",aux["upstream_repair_upload"],aux["consumer_return_commit_date"],
      ["BC-S24","BC-S25","BC-S26"],"Later repair of same new-version purpose; not the original2022 split; not A","SCOPED_SOURCE_RESPONSE")
    measured("B-C03-R2-UploadMerge","B-C03","B_AUX","R2; not extra attempt",
      "selected Linux repair artifact upload → default-branch merge",aux["upstream_repair_upload"],aux["consumer_return_merge_date"],
      ["BC-S24","BC-S25","BC-S26"],"Merge is separate from source author/committer date and CI activation","SCOPED_SOURCE_INTEGRATION")
    measured("B-C03-R2-CommitRelease","B-C03","B_AUX","R2; not extra attempt",
      "restoration source edit → first known published source edition",aux["consumer_return_commit_date"],aux["source_release_date"],
      ["BC-S26","BC-S27"],"v2.3.1 final file already restored qt; workaround ancestry does not prove a separately deployed workaround")
    upstream.sort(key=lambda x:x["reference_id"]);chains.sort(key=lambda x:x["reference_id"]);verdicts.sort(key=lambda x:x["reference_id"])
    write_csv("upstream.csv",upstream);write_csv("chains.csv",chains);write_csv("verdicts.csv",verdicts);write_csv("intervals.csv",intervals)
    assembled={"upstream":upstream,"chains":chains,"verdicts":verdicts,"intervals":intervals}
    (ROOT/"evidence/consolidated-cases.json").write_text(json.dumps(assembled,ensure_ascii=False,indent=2)+"\n")
    groups={}
    for sample in ["A","B"]:
        for eco in ["Homebrew","conda-forge"]:
            rs=[r for r in refs if r["sample"]==sample and r["ecosystem"]==eco];ids={r["reference_id"] for r in rs}
            us=[u for u in upstream if u["reference_id"] in ids];vs=[v for v in verdicts if v["reference_id"] in ids]
            noevent=sum(not u["event_observed"] for u in us)
            groups[sample+":"+eco]={"consumer_projects":len({r["consumer_project"] for r in rs}),"references":len(rs),
                "deduplicated_selected_upstream_events":len({u["event_id"] for u in us if u["event_id"]}),
                "strict_complete_chains":0,"partial_chains":len(rs)-noevent,"no_relevant_event_observed":noevent,
                "verdicts":dict(collections.Counter(v["verdict"] for v in vs))}
    ccounts=collections.Counter(s["minimum_category"] for s in sources if s["count_toward_minimum"])
    totals={"A_references":12,"A_projects":len({r["consumer_project"] for r in refs if r["sample"]=="A"}),
        "A_by_ecosystem":{"Homebrew":6,"conda-forge":6},"B_attempts":6,"B_A_overlap":2,"B_new_reference_records":4,
        "B_projects":6,"distinct_A_B_projects":len({r["consumer_project"] for r in refs}),
        "A_selected_upstream_event_keys":len({u["event_id"] for u in upstream if u["sample"]=="A" and u["event_id"]}),
        "B_selected_upstream_event_keys":len({u["event_id"] for u in upstream if u["sample"]=="B" and u["event_id"]}),
        "A_B_deduplicated_selected_upstream_event_keys":len({u["event_id"] for u in upstream if u["event_id"]}),
        "event_count_semantics":"distinct selected supplier edit/episode groups, including routine version successors; not statistical independence or failure episodes. Auxiliary repairs not included.",
        "A_verdicts":dict(collections.Counter(v["verdict"] for v in verdicts if v["sample"]=="A")),
        "B_verdicts":dict(collections.Counter(v["verdict"] for v in verdicts if v["sample"]=="B")),
        "A_strict_complete_chains":0,"B_original_strict_complete_chains":0,"A_strict_Tu_Tc_pairs":0,
        "formal_right_censored_primary":0,"formal_left_censored_primary":0,"left_censored_secondary":0,
        "secondary_predecessor_reference_unresolved":1,
        "A_source_commit_to_published_source_pairs":3,"A_source_commit_to_published_source_reference_count":2,
        "H02_first_distribution_interval_eligible":False,
        "B_auxiliary_source_response_pairs":1,"B_auxiliary_source_integration_pairs":1,"B_auxiliary_source_release_pairs":1,
        "A_direct_party_failure_report_references":2,"A_verified_human_misrecommendation_harm":0,
        "A_human_harm_unconfirmed":12,"A_declared_historical_reproduction_pin":0,
        "source_ledger_rows":len(sources),"conservative_unique_originals":sum(ccounts.values()),
        "source_minimum_categories":{"A_historical":ccounts["historical"],"upstream":ccounts["upstream"],
          "consumer_followup":ccounts["followup"]+ccounts["consumer_followup"],"B_additional_historical":ccounts["consumer_historical"]+ccounts["b_consumer_original"],
          "cross_domain":ccounts["cross_domain_upstream"]+ccounts["cross_domain_consumer"]},
        "groups":groups,"independent_consumer_caveat":"A-C06 shared maintainer lineage excluded from independent corroboration credit; other distinct projects are not automatically independent authors. H6 and selected C01/C02 author comparisons documented; never interpret A12 as12 independent experiments.",
        "verification_scope":"source/diff/metadata/archive-content inspection; no historic target software build, CI rerun, GUI test or measured user harm"}
    (ROOT/"evidence/counts.json").write_text(json.dumps(totals,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(totals,ensure_ascii=False))
if __name__=="__main__":main()
