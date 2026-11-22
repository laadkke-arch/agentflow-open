#!/usr/bin/env python3
"""Mechanical audit only; run with python -B. Never edits frozen discovery."""
import json
import hashlib
import copy
import re
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parent
OWN = ROOT.parents[1]
def lines(path):
    return [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]
def check(ok, label):
    checks.append({"check":label,"met":bool(ok)})
checks=[]
dec=lines(ROOT/"decisions.jsonl")
hist=lines(ROOT/"candidate-history.jsonl")
src=json.loads((ROOT/"sources.json").read_text())
original=lines(OWN/"streams/jupyter/returns.jsonl")
orig={x["candidate_id"]:x for x in original if x.get("candidate_id")}
oldsrc=json.loads((OWN/"streams/jupyter/sources-candidates.json").read_text())
allids={s["source_id"] for s in src+oldsrc}
check(len(dec)==4 and {x["question_id"] for x in dec}=={"Q09","Q10","Q11","Q12"}, "exactly four question decisions")
check(len(hist)==23 and {x["candidate_id"] for x in hist}==set(orig), "every unique original returned candidate once:23")
check(len({s["source_id"] for s in src})==len(src), "new source IDs unique")
for x in dec:
    for k in ["decision_status","actual_choice","choice_scope","source_ids","source_urls","exact_sections","changes_from_first","candidate_stage_annotations","searched_scope","limitations"]:
        check(bool(x.get(k)),x["question_id"]+":"+k)
    expected={r["candidate_id"] for r in original if r["question_id"]==x["question_id"]}
    check({a["candidate_id"] for a in x["candidate_stage_annotations"]}==expected,x["question_id"]+":stage annotation denominator")
    check(all(s in allids for s in x["source_ids"]),x["question_id"]+":source references resolve")
for x in hist:
    key=x["candidate_id"]
    check(x["historical_availability"] in {"supported","not_available","unknown"},key+":three-state availability")
    check({p["condition_id"] for p in x["feature_evidence"]}==set(orig[key]["mandatory_predicates"]),key+":all mandatory conditions represented")
    check(all(s in allids for s in x["source_ids"]),key+":source references resolve")
    check(bool(x["inspected_scope"]) and bool(x["next_minimum_check"]),key+":real scope and next minimum check")
    if x["historical_availability"]=="supported":
        check(all(p["status"]=="supported" for p in x["feature_evidence"]),key+":supported covers all declared predicates")
    if x.get("partial_supported") and any(p["status"]!="supported" for p in x["feature_evidence"]):
        check(x["historical_availability"]!="supported",key+":partial feature cannot rescue missing full predicates")
    if x["historical_availability"]=="not_available":
        check(any(p["status"]=="not_available" for p in x["feature_evidence"]),key+":unavailability has feature-level evidence")
for s in src:
    for k in ["source_id","related_questions","title","source_url","published_or_revised","version","checked_utc","sections_read","verified_content","limitations","producer","lineage_id","count_reason","role","receipt_ids"]:
        check(bool(s.get(k)),s["source_id"]+":"+k)
    check(isinstance(s.get("count_in_minimum"),bool),s["source_id"]+":count boolean")
    check(all((ROOT/"receipts"/(r+".json")).exists() for r in s["receipt_ids"]),s["source_id"]+":receipts exist")
receipts=[json.loads(p.read_text()) for p in sorted((ROOT/"receipts").glob("*.json"))]
check(len(receipts)==53,"53 actual external tool calls")
check(all(r.get("request") and r.get("raw_response_sha256") and r.get("started_utc") and r.get("finished_utc") for r in receipts),"every receipt has request/hash/timing")
amendment_path=ROOT/"amendments/JP-AMEND-002.json"
if amendment_path.exists():
    amendment=json.loads(amendment_path.read_text())
    digest=lambda value:hashlib.sha256(value).hexdigest()
    canonical=lambda value:digest(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
    changes=amendment["receipt_changes"]
    check(len(changes)==32 and len({x["file"] for x in changes})==32,"32 distinct receipt selectors redacted")
    check(digest((ROOT/amendment["previous_seal_snapshot"]).read_bytes())==amendment["previous_seal_sha256"],"previous seal preserved byte for byte before receipt redaction")
    for item in changes:
        receipt_path=ROOT/item["file"]
        record=json.loads(receipt_path.read_text())
        check(record["request"].get("link_id")=="[connection selector redacted]",item["file"]+":selector redacted")
        check(digest(receipt_path.read_bytes())==item["after_sha256"],item["file"]+":redacted receipt hash")
        invariant=copy.deepcopy(record)
        invariant["request"].pop("link_id",None)
        check(canonical(invariant)==item["all_other_fields_sha256"],item["file"]+":all non-selector fields unchanged")
    def string_values(value):
        if isinstance(value,str):
            yield value
        elif isinstance(value,dict):
            for child in value.values():
                yield from string_values(child)
        elif isinstance(value,list):
            for child in value:
                yield from string_values(child)
    check(not any(re.search(r"\blink_[A-Za-z0-9_-]+",value) for r in receipts for value in string_values(r.get("request",{}))),"no unredacted internal selector value remains in receipt requests")
    check(all(digest((ROOT/name).read_bytes())==value for name,value in amendment["protected_evidence_sha256"].items()),"source observations and history evidence unchanged by receipt redaction")
check(len(json.loads((ROOT/"diff-observations.json").read_text()))==4,"four fixed proposal diffs")
check({s["related_questions"][-1] for s in src if s["role"]=="followup_decision" and s["count_in_minimum"]}=={"Q09","Q10","Q11","Q12"},"four distinct followup cases counted")
out={"status":"PASS" if all(c["met"] for c in checks) else "FAIL","checks":len(checks),"failed":[c for c in checks if not c["met"]],"denominators":{"questions":len(dec),"original_slots":len(original),"unique_original_candidates":len(orig),"candidate_history_rows":len(hist),"sources":len(src),"counted_sources":sum(s["count_in_minimum"] for s in src),"receipts":len(receipts)},"historical_availability_counts":{state:sum(x["historical_availability"]==state for x in hist) for state in ["supported","not_available","unknown"]},"limitations":"Mechanical audit of own records only; not independent factual validation or runtime testing."}
(ROOT/"validation.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out["status"]=="PASS" else 1)
