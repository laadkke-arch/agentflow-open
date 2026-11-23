"""Verify transcriptions and design arithmetic, never reconstruct raw integer cells."""
import json
from datetime import datetime, timezone
from pathlib import Path
from fractions import Fraction

base = Path(__file__).resolve().parent
out = json.loads((base / "outcomes.json").read_text())
contr = json.loads((base / "contrasts.json").read_text())
sources = [json.loads(x) for x in (base / "sources.jsonl").read_text().splitlines()]
rows = out["rows"]
checks = []
def check(name, ok, detail):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
check("B01 author person accounting", 31-1-2 == 28 and 5+20+1+1+1 == 28,
      "AD-M12 section4.1:31 recruited,1 attention,2 I=A excluded;28 retained")
correct_items, wrong_items = 3+3+1+1, 3+3
check("B03 Table1 item accounting", correct_items == 8 and wrong_items == 6 and correct_items+wrong_items == 14,
      "AD-M26 Table1; this does not establish figure denominators")
expected_correct_share = float(Fraction(8,14)*100)
printed_correct_sums = [34.5+15.5, 34.0+16.0, 32.2+17.8]
check("B03 denominator discrepancy retained", all(abs(expected_correct_share-v)>0.1 for v in printed_correct_sums),
      {"expected_if14": expected_correct_share, "printed": printed_correct_sums, "max_rounding_sum_error_pp":0.1, "inferred_actual_denominator":None})
check("B04 design arithmetic only", 85*20*4 == 6800 and 1190+510 == 1700,
      "planned85x20;70/30% =>1190/510 eachcondition;notobservedrows")
expected = {"None":(73.8,52.7),"SM":(71.4,53.1),"NLE":(74.5,46.4),"Combined":(72.3,53.7)}
for c,(right,wrong) in expected.items():
    rr = [r for r in rows if r["case_id"]=="B04" and r["condition"]==c]
    check("B04 Fig6 actual bar mapping "+c,
          next(r for r in rr if r["advice_truth"]=="correct")["author_model_predicted_accuracy_percent"]==right
          and next(r for r in rr if r["advice_truth"]=="wrong")["author_model_predicted_accuracy_percent"]==wrong,
          {"correct_model_accuracy":right,"wrong_model_accuracy":wrong,"source":"AD-M30 Fig6 rendered p18906"})
for r in contr["rows"]:
    if r["case_id"]=="B04" and r.get("subgroup") is None:
        expected_delta=round(r["intervention_acceptance_percent_model"]-r["control_acceptance_percent_model"],1)
        check("descriptive model subtraction "+r["contrast_id"], r["acceptance_delta_pp_model_descriptive"]==expected_delta,
              "rounded model contrast only; no empirical integer cells/significance computed")
check("No rounded-percent integer reconstruction",
      len(rows)==18 and all(r["acceptance_numerator"] is None and r["final_correct_numerator"] is None and r["adjudicable_trials_observed"] is None for r in rows),
      "null is unknown; structural zero wrong opportunities in B01 retained separately")
check("Distinct substantive source works",
      len({s["work_id"] for s in sources if s.get("counts_for_20")}) == 8,
      "3 selected papers+1 auxiliary tool+2 auxiliary papers+2 auxiliary reconstruction packages; B02 root excluded here")
result={"executed_utc":datetime.now(timezone.utc).isoformat(),"executor":"adjacent assistant local Python standard library","command":"python -B docs/workstreams/research/AF-RES-058/streams/adjacent/audit_checks.py","scope":"published aggregates/design arithmetic and file transcription; NOT original participant analysis","checks":checks,"pass":all(c["pass"] for c in checks)}
(base/"arithmetic-check.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"pass":result["pass"],"checks":len(checks),"artifact":str(base/"arithmetic-check.json")}))
raise SystemExit(0 if result["pass"] else 1)

