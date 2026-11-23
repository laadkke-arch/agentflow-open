#!/usr/bin/env python3
"""Normalize AF-RES-050 read-only research streams; no participant raw rows copied."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNKNOWN = "미확인"
CATEGORIES = {
    "original_papers": "fixed_paper", "original_paper": "fixed_paper",
    "fixed_primary": "fixed_paper", "fixed_paper": "fixed_paper",
    "study_materials": "author_supplement", "author_supplement": "author_supplement",
    "implementation": "task_implementation", "task_rubric_implementation": "task_implementation",
    "independent_task_rubric_tool_artifact": "task_implementation",
    "method_or_additional": "method_or_additional", "methods_or_additional": "method_or_additional",
}
REQUIRED = {"fixed_paper": 8, "author_supplement": 6, "task_implementation": 6, "method_or_additional": 4}
# Substantively inspected independent primary works outside the allocation quota.
# Not selected as software supplement families, not copies of fixed-study papers.
EXTRA_PRIMARY = {"RT-S01", "RT-S02", "RT-S03", "RT-S04", "RT-T01", "RT-T02"}

def jdump(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=False)

def first(d, *keys, default=UNKNOWN):
    for key in keys:
        if key in d and d[key] is not None:
            return d[key]
    return default

def array(v):
    if v is None: return []
    return v if isinstance(v, list) else [v]

def cell(v):
    if v is None: return UNKNOWN
    if isinstance(v, (list, dict)): return jdump(v)
    if isinstance(v, bool): return "true" if v else "false"
    return v

def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for d in rows:
            w.writerow({k: cell(d.get(k)) for k in fields})

sources = []
seen_ids = set()
counted_works = set()
for path in sorted((ROOT / "streams").glob("*/sources*.jsonl")):
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        d = json.loads(line)
        sid = d["source_id"]
        assert sid not in seen_ids, sid
        seen_ids.add(sid)
        direct = bool(d.get("direct_read", False))
        category = CATEGORIES.get(first(d, "quota_category", "allocation", "count_category", default=None))
        requested = bool(d.get("quota_eligible", d.get("count_minimum", d.get("counted_unique", False))))
        work = first(d, "work_id", default="attempt:" + sid)
        eligible = direct and requested and category is not None and work not in counted_works
        if eligible: counted_works.add(work)
        findings = first(d, "findings", "observed", "verified_content", default=[])
        r = {
            "source_id": sid,
            "study_ids": array(first(d, "study_ids", "study_id", default=[])),
            "question_ids": array(first(d, "question_ids", "questions", default=[])),
            "publisher": first(d, "publisher", default="source host; see stream record"),
            "title": first(d, "title", default=work),
            "work_id": work,
            "publication_work_id": first(d, "publication_work_id", default=work),
            "material_kind": first(d, "material_kind", "source_kind", "kind", "material_type"),
            "quota_category": category if eligible else None,
            "quota_count": int(eligible),
            "substantive_unique_primary_count": int(eligible or sid in EXTRA_PRIMARY),
            "url": d["url"],
            "checked_at_utc": first(d, "checked_at_utc", "checked_utc", "utc_interval"),
            "utc_basis": first(d, "utc_basis", "checked_utc_meaning", "checked_utc_precision", "timestamp_basis", default="stream timestamp; exact retrieval granularity is limited to source record"),
            "version": first(d, "version", "sha"),
            "locator": first(d, "locator", default="listed URL request/response; original material not obtained" if not direct else UNKNOWN),
            "findings": array(findings),
            "limitations": array(first(d, "limitations", default=[])),
            "assessment": first(d, "polarity", "stance", "judgment", "assessment", default="미확인"),
            "direct_read": direct,
            "status": first(d, "status", "support_status", default="direct_read" if direct else "failed_attempt"),
            "duplicate_of": first(d, "duplicate_of", default=None),
            "duplicate_group": first(d, "duplicate_group", default=work),
            "evidence_lineage": array(first(d, "evidence_lineage", "lineage", default=[])),
            "minimum_missing_material": first(d, "minimum_missing_material", "minimum_material", "minimum_to_change_answer", "next_minimum", "minimum_next_material", default=None),
            "record_origin": str(path.relative_to(ROOT)) + ":" + str(lineno),
            "evidence_refs": array(first(d, "web_refs", "evidence_refs", "tool_ref", default=[])),
        }
        if not direct:
            r["attempt_or_error"] = first(d, "error", "attempt", "verified_content", "observed", "limitations", default="see original stream record")
        sources.append(r)

(ROOT / "sources.jsonl").write_text("\n".join(jdump(x) for x in sources) + "\n")
source_by_id = {d["source_id"]: d for d in sources}
counts = Counter(d["quota_category"] for d in sources if d["quota_count"])
count_data = {
    "source_record_count": len(sources),
    "direct_read_record_count": sum(d["direct_read"] for d in sources),
    "failed_or_unread_record_count": sum(not d["direct_read"] for d in sources),
    "unique_substantive_primary_works_read": sum(d["substantive_unique_primary_count"] for d in sources),
    "unique_primary_work_ids_counted": [d["source_id"] for d in sources if d["substantive_unique_primary_count"]],
    "quota_eligible_unique_works": sum(counts.values()),
    "quota": {k: {"observed": counts[k], "required": n, "filled": min(counts[k], n), "shortfall": max(n-counts[k], 0)} for k,n in REQUIRED.items()},
    "filled_quota_slots": sum(min(counts[k], n) for k,n in REQUIRED.items()),
    "required_quota_slots": 24,
    "additional_primary_work_ids_without_quota": sorted(EXTRA_PRIMARY),
    "excluded_from_counts": "metadata, search results, failed opens, same-package component files, same-paper author/publisher/TeX versions, overlapping thesis chapters and eXoa lineage repeats, guide/policy materials",
    "interpretation": "25+ substantive primary works may be read while the required8+6+6+4 allocation remains unmet; extra methods or excluded supplemental studies cannot replace missing author research packets/tasks.",
}
(ROOT / "evidence/source-counts.json").write_text(json.dumps(count_data, ensure_ascii=False, indent=2) + "\n")

joins = []
outcomes = []
for sub in ("ncq-exoa", "blueprint-codemend", "unakite-strata", "root"):
    base = ROOT / "streams" / sub
    for typ, target in (("joins", joins), ("outcomes", outcomes)):
        data = json.loads((base / (typ + ".json")).read_text())
        for index, d in enumerate(data, 1):
            d = dict(d)
            d["_origin"] = "streams/" + sub + "/" + typ + ".json#" + str(index)
            if typ == "outcomes" and d.get("outcome_id") == "BC-O04":
                # Separate tasks/endpoints; preserve original composite record as provenance.
                for suffix, endpoint, rubric, uncertainty, budget in (
                    ("A", "directed code-quality ordinal rank", d["directed_rubric"], d["directed_reported_uncertainty"], 600),
                    ("B", "exploratory chart-quality ordinal rank", d["exploratory_rubric"], d["exploratory_reported_uncertainty"], 900),
                ):
                    split = {k:v for k,v in d.items() if not k.startswith("directed_") and not k.startswith("exploratory_")}
                    split.update(outcome_id="BC-O04" + suffix, parent_record="BC-O04", endpoint=endpoint,
                                 comparison="Blueprint vs Control; " + ("directed" if suffix == "A" else "exploratory") + " task",
                                 quality=rubric, reported_uncertainty=uncertainty, task_budget_seconds=budget,
                                 transform_note="Separate endpoints required by SCOPE; no values or analysis rule changed")
                    split["unit"] = "ordinal rank; individual values unavailable" if suffix == "A" else "ordinal rank sum"
                    split["missing_terms"] = ["stable person/task identity across sorted plots", "individual quality ranks", "grader blinding/reliability"]
                    if suffix == "B":
                        split.update(reported_treatment=94, reported_control=116, total_task_time="fixed900s exploratory task; no variable completion-time endpoint")
                    else:
                        split["missing_terms"].append("individual time/completion-status linkage")
                    split["formula_if_raw"] = "Independent-arm ordinal ranks for this task; time-quality co-analysis requires the same person/task key. " + ("Directed elapsed time has a600s limit." if suffix == "A" else "Exploratory task uses a fixed900s budget, so do not estimate time-to-completion from these ranks.")
                    target.append(split)
                continue
            target.append(d)

def source_ids(d):
    v = first(d, "source_ids", "sources", default=[])
    if not v and d.get("outcome_id","").startswith("O-NA-"):
        s=d["outcome_id"]
        v = ["NA-003-CSV" + s[-1]] if "SNIPPET" in s else ["NA-001" if s[-2:] in ("01","02","03") else "NA-002"]
    return array(v)

def source_urls(d):
    ids=source_ids(d)
    return array(d.get("source_url")) + [source_by_id[x]["url"] for x in ids if x in source_by_id]

jrows = []
for d in joins:
    jrows.append({
        "join_id":d["join_id"],"study_id":d["study_id"],"experiment":first(d,"experiment","substudy"),
        "unit":first(d,"unit","relation"),"design":first(d,"design","allocation"),
        "keys":first(d,"candidate_person_trial_key","desired_keys","candidate_key","join_key","key","fields"),
        "cardinality":first(d,"cardinality","expected_cardinality","cardinality_expected"),
        "source_file":first(d,"source_file","file_rows","locator"),
        "source_version":first(d,"source_version"),"source_urls":source_urls(d),
        "input_rows":first(d,"source_rows","input_records","join_before_rows","left_rows","actual_raw_left_rows"),
        "target_rows":first(d,"target_trial_rows","target_trials","target_directed_trials","target_person_task_trials","target_graph_positions","target_people"),
        "target_basis":first(d,"target_trial_rows_basis","target_basis","target_trial_basis","expected_cardinality"),
        "joined_rows":first(d,"join_after_rows","joined_rows","actual_joined_rows"),
        "left_unmatched":first(d,"unmatched_left","left_unmatched"),
        "right_unmatched":first(d,"unmatched_right","right_unmatched"),
        "key_unique_count":first(d,"candidate_key_count","left_unique_keys","unique_full_row_keys"),
        "null_key_rows":first(d,"null_candidate_keys","null_key_rows","null_keys"),
        "exact_duplicate_records":first(d,"exact_duplicate_records"),
        "key_nonunique_excess":first(d,"candidate_key_nonunique_excess"),
        "duplicate_groups":first(d,"duplicate_full_row_groups","duplicate_keys","duplicate_key_groups","duplicates"),
        "execution":first(d,"execution","join_executed","actual_join_run","raw_join_execution"),
        "permitted_comparison":first(d,"allowable_comparison","allowed_comparison","permitted_comparison","meaning","conclusion"),
        "missing_fields":first(d,"missing_fields","missing_keys","tables_needed"),
        "minimum_new_file":first(d,"minimum_new_file","minimum_file","missing_minimum"),
        "source_ids":source_ids(d),"evidence_pointer":d["_origin"],"details_json":d
    })
    r=jrows[-1]
    if d["join_id"] in ("J-NA-01","J-NA-02"):
        r["design"]="same people, different tasks; baseline always first; no order counterbalance"
        r["duplicate_groups"]="미확인 for P×T repeated groups; normal1:N snippet relation, not erroneous duplicate rows"
    if d["join_id"]=="J-NA-04":
        r.update(design="independent randomized arms within4Java-expertise strata",target_rows=96,target_basis="24people×4tasks planned slots; not observed participant records")
    if d["join_id"]=="J-US-AGG":
        r.update(cardinality="1:1 on unique(condition,task),6aggregate rows each side",source_version="arXiv2102.06231v2; SHA256 in streams/unakite-strata/audit-arxiv-source.json")
    if d["join_id"]=="BC-J03":
        r["target_rows"]="40 person-task trials /120 planned successive-subtask opportunities;60opportunities per condition"
write_csv(ROOT / "joins.csv", list(jrows[0]), jrows)

orows = []
for d in outcomes:
    orows.append({
        "outcome_id":d["outcome_id"],"study_id":d["study_id"],"experiment":first(d,"experiment"),
        "comparison":first(d,"comparison"),"evidence_type":first(d,"evidence_type","estimation_level","status"),
        "endpoint":first(d,"endpoint"),"unit":first(d,"unit"),"denominator":first(d,"denominator","population","n_people","n_treatment","target_rows"),
        "control":first(d,"control","reported_control","numerator_control","reported_numerator_control"),
        "treatment":first(d,"treatment","experimental","reported_treatment","numerator_treatment","reported_numerator_treatment"),
        "time_origin":first(d,"start","time_start_event"),"time_end":first(d,"end","time_stop_event"),
        "selection_time":first(d,"selection_time"),"total_task_time":first(d,"total_task_time","full_task_time"),
        "activity_time":first(d,"activity_time","active_labor"),
        "quality":first(d,"quality","quality_definition","quality_link","quality_failure_cap"),
        "failures":first(d,"failures","quality_failure_cap","noncompletion_categories"),
        "time_limit":first(d,"time_limit_seconds","timeout_seconds","time_limit"),
        "estimate_or_reason":first(d,"estimate","uncertainty_or_not_estimated","uncertainty","reported_uncertainty","reason","statistic"),
        "uncertainty":first(d,"uncertainty_or_not_estimated","uncertainty","reported_uncertainty"),
        "formula":first(d,"permitted_formula","formula_if_raw"),
        "missing_terms":first(d,"missing_terms","minimum_material"),
        "source_ids":source_ids(d),"source_urls":source_urls(d),
        "source_location":first(d,"source_locator","source_location","locator"),"evidence_pointer":d["_origin"],"details_json":d
    })
    r=orows[-1]; oid=d["outcome_id"]
    denom={
        "BC-O02":"E9/C8 successful completers; original independent allocation E10/C10",
        "BC-O03":"E10/C10 assigned people; completion numerator E9/C8",
        "BC-O04A":"independent E10/C10 people; directed-task ordinal quality",
        "BC-O04B":"independent E10/C10 people; exploratory-task ordinal quality",
        "BC-O05":"20 crossover people; analyzed subtask-time row nE/nC 미확인; planned60subtask opportunities/condition",
        "BC-O06":"planned E60/C60 successive subtask opportunities from20crossover people; actual attempts 미확인",
        "O-RT-02":"E1 independent E25/C25 people; protocol350person-problem slots, not observed rows",
        "O-RT-03":"E2 independent E15/C15 people; protocol210person-problem slots, not observed rows",
    }
    if oid in denom:r["denominator"]=denom[oid]
    if oid in ("O-NA-01","O-NA-02","O-NA-03"):
        r["denominator"]="same10analyzed people perform both conditions on different tasks;20planned person-trials within this cohort; baseline first"
        r["time_origin"]="task attempt begins; exact recorded clock mapping unavailable"
        r["time_end"]="last package installation used for final task" if oid=="O-NA-01" else "author-verified specification-satisfying JavaScript result; exact eventclock mapping unavailable"
    if oid in ("O-NA-01","BC-O01"):
        r["selection_time"]={"C":r["control"],"E":r["treatment"],"unit":"seconds","statistic":"median" if oid=="O-NA-01" else "mean first-paste latency"}
    if oid in ("O-NA-02","O-NA-03","BC-O02"):
        r["total_task_time"]={"C":r["control"],"E":r["treatment"],"unit":"seconds","statistic":"median" if oid.startswith("O-NA") else "mean among successful completers"}
    if oid in ("O-NA-04","O-NA-05","O-NA-06","O-NA-07","O-NA-08"):
        r["time_limit"]="40minutes whole4-task session; not40min/task"
        if oid in ("O-NA-04","O-NA-05","O-NA-06"):
            r["time_origin"]="session/task-sequence start; exact eventclock unprovided"
            r["time_end"]="next relevant document dwell>30s; task3/4 inseparable; not exact final submission"
            r["total_task_time"]={"C":r["control"],"E":r["treatment"],"unit":"minutes:seconds","definition":"cumulative document-inferred completion among included completers"}
        if oid=="O-NA-07":
            text="40min within-session all-task pass; non-pass eXoaDocs9/12 and JavaDocs11/12, combining wrong/incomplete/timeout without individual classification"
            r["quality"]=text;r["failures"]=text
    if oid in ("BC-O01","BC-O02","BC-O03","BC-O04A"):
        r["time_limit"]="600s directed-task limit; first-paste endpoint separately defined"
    if oid=="BC-O04B":r["time_limit"]="900s fixed exploratory-task budget, not a time-to-success cap"
    us={
        "O-US-01":("Unakite vs Google Docs; same adapted source page, independent arms","participant declares done or cannot make further progress"),
        "O-US-02":("prebuilt Unakite comparison table/snippets vs same original page set;16-person crossover","third gold-standard legitimate explanation"),
        "O-US-03":("Strata feature bundle vs Unakite base tables; independent arms","done/no-further-progress declaration or600s cap"),
    }
    if oid in us:r["comparison"],r["time_end"]=us[oid]
write_csv(ROOT / "outcomes.csv", list(orows[0]), orows)

fixed=[
("S01","software-primary","NCQ","SWB-E10~12","ncq-exoa"),
("S02","software-primary","eXoaDocs","SWB-E01~04","ncq-exoa"),
("S03","software-primary","Blueprint","Ewa-02~04","blueprint-codemend"),
("S04","software-primary","CodeMend","Er-03","blueprint-codemend"),
("S05","software-primary","Unakite","Er-01/02","unakite-strata"),
("S06","software-primary","Strata","Er-04","unakite-strata"),
("X01","cross-domain-design","Chan2011","XD-CHAN2011","root"),
("X02","cross-domain-learning","Schwonke2009","XL-SCHWONKE2009","root"),
]
srows=[]
for order,(sid,layer,family,effects,sub) in enumerate(fixed,1):
    bpath=ROOT/"streams"/sub/"baseline.json"; b=json.loads(bpath.read_text())
    baseline=b.get(sid) if isinstance(b,dict) else [x for x in b if x.get("study_id")==sid]
    spath=ROOT/"streams"/sub/"studies.json"
    details=[x for x in json.loads(spath.read_text()) if x.get("study_id")==sid] if spath.exists() else baseline
    refs=[x["source_id"] for x in sources if sid in x["study_ids"]]
    srows.append({"study_id":sid,"stratum":layer,"family":family,"dependency_effect_ids":effects,
        "selection_order":order,"availability":"미확인: allocation×time×final-quality participant ledger not recovered; partial artifacts recorded separately",
        "status":"retained regardless of availability; partial evidence","rule_commit":"f3c8de473b52a64c92c862cc64927ce787525c1a",
        "baseline_commit":"35576f16914c9f62b5c4d91bf015092b2e93aa34",
        "source_ids":refs,"join_ids":[x["join_id"] for x in joins if x["study_id"]==sid],
        "outcome_ids":[x["outcome_id"] for x in outcomes if x["study_id"]==sid],
        "baseline_pointer":"streams/"+sub+"/baseline.json","search_and_version_details":details})
write_csv(ROOT/"studies.csv",list(srows[0]),srows)
print(jdump({"sources":len(sources),"unique_substantive_primary":count_data["unique_substantive_primary_works_read"],
             "quota_unique":count_data["quota_eligible_unique_works"],"filled_quota_slots":count_data["filled_quota_slots"],
             "quota":count_data["quota"],"studies":len(srows),"joins":len(jrows),"outcomes":len(orows)}))

