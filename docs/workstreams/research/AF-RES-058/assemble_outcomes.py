"""Assemble aggregate outcomes without converting modeled percentages to counts."""
from __future__ import annotations
import csv
import json
from pathlib import Path

B = Path(__file__).resolve().parent
def load(p):
    j = json.loads((B / p).read_text())
    return j.get("rows", []) if isinstance(j, dict) else j
def csvfile(name, rows):
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with (B / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in rows:
            w.writerow({k: "미확인" if r.get(k) is None else json.dumps(r[k], ensure_ascii=False) if isinstance(r[k], (list, dict)) else r[k] for k in keys})
def truth(x):
    if x is True: return "correct"
    if x is False: return "wrong"
    return x

out = []
def add(case, condition, correct, **kw):
    row = dict(record_id=f"O{len(out)+1:03}", case_id=case, stratum=case[0],
               condition=condition, advice_truth=truth(correct), row_type="outcome",
               allocation_unit=None, analysis_set="primary" if case[0] in "AB" else "diagnostic",
               dataset=None, planned_people=None, analyzed_people=None, people_basis=None,
               planned_D=None, observed_D=None, accept_n=None, accept_D=None,
               final_correct_n=None, final_correct_D=None, third_wrong_n=None,
               missing_final_n=None, original_assigned_missing=None,
               skipped=None, withdrawn=None, exclusions_people=None,
               advice_provided=True, actual_reading="미확인", pre_advice=None,
               status="unidentified", grade="JU", source_ids=[], source_file=None,
               source_row=None, locator=None, next_input=None, limits=None,
               model_acceptance_percent=None, model_accuracy_percent=None)
    row.update(kw);out.append(row)

for i, r in enumerate(load("streams/software/outcomes.json"), 1):
    case = r["case_id"]
    add(case, r.get("condition"), r["recommendation_correctness"],
        allocation_unit=r.get("allocation_unit"), planned_people=r.get("planned_assignment_n"),
        analyzed_people=r.get("reported_completed_person_n"), people_basis="author-reported completers; not allocation roster",
        observed_D=r.get("judgable_recommendation_trials"), accept_n=r.get("accepted_recommendation_n"),
        accept_D=r.get("accepted_recommendation_denominator"), final_correct_n=r.get("final_correct_n"),
        final_correct_D=r.get("final_correct_denominator"), original_assigned_missing=r.get("missing_or_unlinked_trials"),
        pre_advice=r.get("pre_advice_answer"), status=r["count_status"],
        advice_provided=None if case in ("A03", "A04") else True,
        grade="JU/J3" if case in ("A01", "A02") else "unfilled_slot",
        source_ids=sorted(set(([r["response_source"]] if r.get("response_source") else []) + r.get("truth_source", []))),
        source_file="streams/software/outcomes.json", source_row=i,
        next_input=r.get("next_minimum_input", "앞선 방법 미확인 원문을 확보하고 고정 모집 순서 재검토"),
        limits=r.get("skip_withdrawal", r.get("reason")), details=r)

for i, r in enumerate(load("streams/adjacent/outcomes.json"), 1):
    zero = r["case_id"] == "B01" and r["advice_truth"] == "wrong"
    add(r["case_id"], r["condition"], r["advice_truth"], allocation_unit=r["assignment_unit"],
        planned_people=r.get("condition_people_planned", r.get("cohort_people_recruited")),
        analyzed_people=r.get("cohort_people_analyzed", r.get("cohort_people_included")),
        people_basis="author study summary; group allocation rows not recovered",
        planned_D=r.get("planned_trials_after_author_person_exclusions", r.get("planned_trials")),
        observed_D=r.get("adjudicable_trials_observed"), accept_n=r.get("acceptance_numerator"),
        accept_D=None if zero else r.get("acceptance_denominator"),
        final_correct_n=r.get("final_correct_numerator"), final_correct_D=r.get("final_correct_denominator"),
        missing_final_n=r.get("missing_responses"), skipped=r.get("skips"), withdrawn=r.get("withdrawals"),
        exclusions_people=r.get("exclusions_people", r.get("excluded_people")), pre_advice=r.get("pre_advice"),
        status="not_applicable_design_zero" if zero else "unidentified", grade=r["evidence_grade"],
        source_ids=r["source_ids"], source_file="streams/adjacent/outcomes.json", source_row=i, locator=r.get("locator"),
        next_input=r.get("next_input"), limits=r.get("no_endpoint_reason", r.get("denominator_problem", r.get("missingness_limit"))),
        model_acceptance_percent=r.get("author_model_predicted_acceptance_percent"),
        model_accuracy_percent=r.get("author_model_predicted_accuracy_percent"), details=r)

# B02 is owned and independently read by root. Products below are planned counts.
for cond, people in (("Control", 100), ("Feature", 99)):
    for correct in ("correct", "wrong"):
        add("B02", cond, correct, allocation_unit="person randomized between conditions;16 repeated judgments",
            analyzed_people=people, people_basis="Table2/3 retained people, total200 recruited minus1",
            planned_D=people * 8, exclusions_people=0 if cond == "Control" else 1,
            pre_advice="initial answer collected; RAIR/RSR restrict to initial disagreement",
            grade="J3", source_ids=["RT-SCH-P", "RT-OTT11-P", "RT-OTT13-P"],
            source_file="streams/root/schemmer-ott-notes.md", source_row="Table3 audit",
            locator="§3.2 equations1–3;§5;Table2/3, PDFpp6–7/10–14",
            next_input="person/item/condition initial/final response and AI/truth joint counts; corrected VoR and inclusion rule",
            limits="800/792 are retainedN×8 design products, not observed joint rows. RAIR/RSR group means are not all-trial A/D. §6.3 no-missing-data statement refers to SEM preprocessing, not a verified final-response allocation census.",
            details={"SEM_missing_author_statement":0,"retained_missing_raw_audit":None,
                     "RAIR_percent":29.59 if cond=="Control" else 38.87,
                     "RSR_percent":71.87 if cond=="Control" else 69.45})

for i, r in enumerate(load("streams/diagnostics/outcomes.json"), 1):
    offered = r["condition"] != "Human"
    add(r["study_id"], r["condition"], r["advice_correct"],
        allocation_unit="person condition; repeated response records (not iid people)", analysis_set=r["analysis_set"], dataset=r["dataset"],
        analyzed_people=r["unique_anonymous_person_keys"], people_basis="distinct anonymous keys; not recruitment/allocation census",
        observed_D=r["denominator"], accept_n=r["accept_count"], accept_D=r["denominator"] if offered else None,
        final_correct_n=r["correct_count"], final_correct_D=r["denominator"],
        third_wrong_n=r["other_wrong_count"] if r["advice_correct"] is False and offered else None,
        missing_final_n=r["missing_final_in_this_file"], original_assigned_missing=r["original_assigned_missing"],
        advice_provided=offered, pre_advice=r["preanswer_switch"], status="observed_records" if offered else "no_advice_reference_model_stratum",
        grade="J1", source_ids=[r["source_id"]], source_file="streams/diagnostics/outcomes.json", source_row=i,
        locator="same-row truth, prediction, final response; pinned-input hashes in input-receipt.json",
        next_input="full allocation/dropout roster; actual reading and pre-advice answers were not recovered",
        limits="Human condition has hidden model reference only, so advice acceptance is not applicable. Filtered/ambiguous-excluded sets are separate, never pooled.", details=r)

for fn in ("unrecovered-outcomes.json", "dejong-outcomes.json"):
    for i, r in enumerate(load("streams/diagnostics/" + fn), 1):
        add(r["study_id"], r["condition"], r["advice_correct"], allocation_unit=r.get("unit", "see original methods"),
            dataset=r.get("experiment"), analyzed_people=r.get("analyzed_people_author_statement"),
            planned_D=r.get("planned_trial_D_from_author_design"), observed_D=r.get("observed_response_D", r.get("judgeable_denominator")),
            accept_n=r.get("accept_count"), final_correct_n=r.get("final_correct_count"),
            status=r.get("status", "unidentified"), grade=r["grade"], source_ids=[r["source_id"]],
            source_file="streams/diagnostics/"+fn, source_row=i, limits=r["reason"], details=r)

for cond in ("Prediction", "Highlight"):
    for correct in ("correct", "wrong"):
        add("D06", cond, correct, dataset="Study1 hard only", analyzed_people=85,
            allocation_unit="person; reused in Studies2/3", people_basis="author design statement",
            planned_D=85*(12 if correct=="correct" else 3), grade="J3/JU",
            source_ids=["RT-VAS-P", "RT-VAS-REG2"], source_file="streams/root/vasconcelos-notes.md", source_row="Study1 hard",
            limits="Design product only; Table1 logistic model contrast is not a count or percentage-point difference. Other tasks/conditions not pooled.",
            next_input="public final-response integer cross-table plus exclusions and item-condition assignment")

# Distinct missingness rows retain original allocation uncertainty, including observed zero core gaps.
keys = set()
for r in list(out):
    key=(r["case_id"],r["condition"],r["analysis_set"],r["dataset"])
    if key in keys: continue
    keys.add(key)
    z=dict(r);z.update(record_id=f"O{len(out)+1:03}",row_type="missingness",advice_truth="unallocated_to_correctness",
                     accept_n=None,accept_D=None,final_correct_n=None,final_correct_D=None,third_wrong_n=None,
                     planned_D=None,observed_D=None,model_acceptance_percent=None,model_accuracy_percent=None)
    z["limits"]="결측은 정오층에 임의 배분하지 않음. " + str(r["limits"] or "원배정·철회·건너뜀 명단 미확인")
    out.append(z)

contrasts=[]
def ca(case, intervention, control, correct, **kw):
    r=dict(contrast_id=f"C{len(contrasts)+1:03}",case_id=case,stratum=case[0],intervention=intervention,control=control,
           advice_truth=truth(correct),dataset=None,analysis_set="primary" if case[0] in "AB" else "diagnostic",
           intervention_accept_n=None,intervention_D=None,control_accept_n=None,control_D=None,
           delta_accept_pp_observed=None,delta_final_correct_pp_observed=None,
           delta_accept_pp_model=None,data_informed_bounds=None,grade="JU",unit="original assignment unit retained",
           source_ids=[],source_file=None,source_row=None,limits=None)
    r.update(kw);contrasts.append(r)
for stream in ("software","adjacent"):
    for i,r in enumerate(load(f"streams/{stream}/contrasts.json"),1):
        # Keep WOA and quality-selected model contrasts in their own estimand fields.
        ca(r["case_id"],r["intervention"],r["control"],r.get("correctness",r.get("advice_truth")),
           delta_accept_pp_observed=r.get("acceptance_delta_pp_observed"),
           delta_accept_pp_model=r.get("acceptance_delta_pp_model_descriptive"),
           grade=r.get("evidence_grade",r.get("directness")),source_ids=r.get("source_ids",[]),
           source_file=f"streams/{stream}/contrasts.json",source_row=i,
           limits=r.get("reason",r.get("limitations")),details=r,
           subgroup=r.get("subgroup"),alternate_metric=r.get("reported_metric"))
for correct in ("correct","wrong"):
    ca("B01","Dr.XAI","Dr.AI",correct,grade="J3/J4",source_ids=["AD-M12"],
       limits="WOA median difference does not identify strict final acceptance; wrong-advice denominator absent by design.")
    ca("B02","Feature","Control",correct,grade="J3",source_ids=["RT-SCH-P"],
       limits="RAIR/RSR have different, initial-disagreement denominators; overall accuracy cannot identify all correct/wrong advice acceptance.")
for i,r in enumerate(load("streams/diagnostics/contrasts.json"),1):
    ca(r["study_id"],r["intervention"],r["control"],r["advice_correct"],dataset=r["dataset"],analysis_set=r["analysis_set"],
       intervention_accept_n=r["intervention_accept"],intervention_D=r["intervention_D"],
       control_accept_n=r["control_accept"],control_D=r["control_D"],
       delta_accept_pp_observed=r["delta_accept_percentage_points"],
       delta_final_correct_pp_observed=r["delta_final_accuracy_percentage_points"],grade="J1",unit=r["unit"],
       source_ids=[r["source_id"]],source_file="streams/diagnostics/contrasts.json",source_row=i,
       limits="Descriptive published-response ratios; no population pooling or iid trial inference.")

for r in out:
    if r["row_type"]=="outcome" and r["accept_n"] is not None:
        assert isinstance(r["accept_n"],int) and isinstance(r["accept_D"],int)
        assert 0 <= r["accept_n"] <= r["accept_D"]
    if r["final_correct_n"] is not None:
        assert 0 <= r["final_correct_n"] <= r["final_correct_D"]
for r in contrasts:
    if r["delta_accept_pp_observed"] is not None:
        expected=100*(r["intervention_accept_n"]/r["intervention_D"]-r["control_accept_n"]/r["control_D"])
        assert abs(expected-r["delta_accept_pp_observed"])<1e-9
(B/"evidence/outcome-ledger.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
(B/"evidence/contrast-ledger.json").write_text(json.dumps(contrasts,ensure_ascii=False,indent=2)+"\n")
csvfile("outcomes.csv",out);csvfile("contrasts.csv",contrasts)
print(json.dumps({"outcome_rows":len(out),"contrast_rows":len(contrasts),
 "primary_integer_acceptance_cells":sum(r["stratum"] in "AB" and r["row_type"]=="outcome" and r["accept_n"] is not None for r in out),
 "diagnostic_integer_acceptance_cells":sum(r["stratum"]=="D" and r["row_type"]=="outcome" and r["accept_n"] is not None for r in out)}))
