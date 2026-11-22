#!/usr/bin/env python3
"""Recalculate selected independent-arm contrasts from published rounded summaries.
No participant data are invented; no pooled meta-analysis or equivalence test.
"""
import json, math, hashlib
from pathlib import Path
from scipy.stats import t
BASE=Path(__file__).resolve().parent
inputs=json.loads((BASE/"effect-inputs.json").read_text())
def metric(x, ni, nc):
    mi,mc=x["mean_intervention"],x["mean_control"]
    out={**x,"difference_intervention_minus_control":mi-mc}
    if x["unit"]=="min":
        out.update(ratio_intervention_over_control=mi/mc,relative_change_percent=100*(mi-mc)/mc)
    if ni is None or nc is None:
        out.update(ci95=None,ci_missing_reason="Methods/Table group n conflict; unresolved arm n, no arbitrary denominator selection")
        return out
    vi=x["sd_intervention"]**2/ni
    vc=x["sd_control"]**2/nc
    se=math.sqrt(vi+vc)
    df=(vi+vc)**2/(vi**2/(ni-1)+vc**2/(nc-1))
    half=t.ppf(.975,df)*se
    out.update(se=se,welch_df=df,ci95=[mi-mc-half,mi-mc+half],ci_method="two-sided nominal95% Welch; independent people; rounded published inputs; no multiplicity adjustment")
    return out
out=[]
for r in inputs["independent_group_comparisons"]:
    ni,nc=r["n_intervention"],r["n_control"]
    row={**r,"calculation":"summary_data_recalculation_not_human_trial","time_result":metric(r["time"],ni,nc),"quality_results":[metric(q,ni,nc) for q in r["quality"]],"equations":{"difference":"M_I-M_C","ratio":"M_I/M_C","relative_time_change_percent":"100*(M_I-M_C)/M_C","SE":"sqrt(SD_I^2/n_I+SD_C^2/n_C)","Welch_df":"(v_I+v_C)^2/(v_I^2/(n_I-1)+v_C^2/(n_C-1))","CI95":"difference +/- t(.975,Welch_df)*SE"},"post_adoption_rework_effect":None,"quality_equivalence":"not tested; nonsignificance does not establish equality"}
    out.append(row)
out.extend(inputs["non_time_or_uncomputable"])
(BASE/"effects.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in out))
sha=hashlib.sha256((BASE/"effect-inputs.json").read_bytes()).hexdigest()
report={"input_sha256":sha,"numeric_comparisons":len(inputs["independent_group_comparisons"]),"other_comparisons":len(inputs["non_time_or_uncomputable"]),"computed_rows":len(out),"ci_missing_due_to_n_conflict":[r["comparison_id"] for r in out if "time_result" in r and r["time_result"]["ci95"] is None],"scope":"17 independent-arm contrasts; 6 non-time/uncomputable contrasts; no experimental rerun"}
(BASE/"calculation-receipt.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(report,ensure_ascii=False))
for r in out:
    if r["comparison_id"] in {"XL-SCHWONKE2009-E1-WE_vs_TPS","XL-SCHWONKE2009-E2-WE_vs_TPS","XL-MCLAREN2016-E1-WE_vs_PS","XL-MCLAREN2016-E2-WE_vs_PS","XL-REISSLEIN2006-EP_vs_PE-overall"}:
        print(json.dumps({"id":r["comparison_id"],"time":r["time_result"],"quality":r["quality_results"]},ensure_ascii=False))

