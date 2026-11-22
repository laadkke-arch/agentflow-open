"""Build the masked second reading from review notes and the sealed authorized packet only."""
import json, hashlib, datetime, re
from pathlib import Path
from collections import Counter
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REPO=ROOT.parents[3]
packet_path=ROOT/"blind/arrow.jsonl"
packet_bytes=packet_path.read_bytes()
packets=[json.loads(x) for x in packet_bytes.decode().splitlines()]
notes=json.loads((HERE/"assessment-notes.json").read_text())
sources=json.loads((HERE/"source-notes.json").read_text())
receipts=[json.loads(p.read_text()) for p in sorted((HERE/"receipts").glob("*.json"))]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
url_audits={s["source_url"]:s for s in sources}
for s in sources:
 rr=[r for r in receipts if re.sub("[a-z]$","",r["id"])==s["source_id"]]
 s["checked_utc"]=[r["started"] for r in rr]
 s["receipt_ids"]=[r["id"] for r in rr]
 s["count_in_minimum"]=False
 s["count_reason"]="감사 재열람은 기존 후보 원문과 같은 계보이므로 연구 최소 고유 원문 수에 중복 추가하지 않는다." if s["direct_original_read"] else "접근 실패 또는 rewritten-summary 표시: 직접 원문 최소수 제외."
 s["audit_only"]=True
 s["new_evidence_added_to_original_citations"]=False
(HERE/"sources.json").write_text(json.dumps(sources,ensure_ascii=False,indent=2)+"\n")
reviews=[]
inputs={}
def refkey(x):
 return (x.get("source_id"),x.get("url"),x.get("section"))
for row in packets:
 n=notes[row["blind_key"]]
 predicates=row["question"]["mandatory_predicates"]
 assert len(predicates)==len(n["statuses"])==len(n["reasons"])==len(n["required"])
 q=row["question"]; ip=REPO/q["input_path"]
 actual=hashlib.sha256(ip.read_bytes()).hexdigest()
 assert actual==q["input_sha256"],(str(ip),actual,q["input_sha256"])
 inputs[row["question_id"]]={"input_path":q["input_path"],"input_sha256":actual,"initial_url":q["initial_url"],"full_input_read":True}
 pkgs=[]
 for p in row["citation_packages"]:
  opened={refkey(x) for x in p["opened_evidence"]}
  cited={refkey(x) for x in p["returned_citations"]}
  ps=[]
  for i,pred in enumerate(predicates):
   cid=pred["id"]
   required=p["required_bundle"].get(cid,[])
   validrefs=[e for e in required if e.get("url")]
   if not validrefs:
    validrefs=p["opened_evidence"]
   required_set={refkey(e) for e in validrefs}
   covers_o=bool(required_set) and required_set.issubset(opened)
   covers_c=bool(required_set) and required_set.issubset(cited)
   state=n["statuses"][i]
   so=(state=="supported" and covers_o)
   sc=(state=="supported" and covers_c)
   fresh=[url_audits[u] for u in sorted({e["url"] for e in validrefs}) if u in url_audits]
   mode="direct_current_source_and_packet" if any(s["direct_original_read"] for s in fresh) else ("rewritten_summary_and_packet" if any(s["source_id"]=="RVA-011" for s in fresh) else ("failed_reopen_and_packet" if fresh else "packet_only"))
   pr={"condition_id":cid,"status":state,
       "source_ids":list(dict.fromkeys(e.get("source_id") for e in validrefs)),
       "urls":list(dict.fromkeys(e["url"] for e in validrefs)),
       "sections":list(dict.fromkeys(e.get("section") for e in validrefs)),
       "reason":n["reasons"][i],
       "support_in_original_opened":so,"support_in_original_citations":sc,
       "required_bundle_source_coverage_opened":covers_o,
       "required_bundle_source_coverage_cited":covers_c,
       "original_evidence":[{k:e[k] for k in ("source_id","url","section") if k in e} for e in validrefs],
       "reading_mode":mode,
       "audit_source_ids":[s["source_id"] for s in fresh],
       "audit_evidence_not_added_to_original":True}
   ps.append(pr)
  oc=all(x["support_in_original_opened"] for x in ps)
  cc=all(x["support_in_original_citations"] for x in ps)
  stat="supported" if cc else ("conflict" if any(x["status"]=="conflict" for x in ps) else "hold")
  missing=[x["condition_id"] for x in ps if not x["support_in_original_citations"]]
  aud=[s for s in sources if s["source_url"] in {e["url"] for e in p["opened_evidence"]}]
  original_versions=[]
  for e in p["opened_evidence"]:
   exact=[s for s in row["sources"] if s.get("source_id")==e.get("source_id") and s.get("source_url")==e["url"]]
   original_versions.append({"source_id":e["source_id"],"url":e["url"],"version":exact[0].get("version") if exact else "unresolved: packet source metadata uses a different URL for this source_id"})
  pkgs.append({"package_key":p["package_key"],"predicate_reviews":ps,
     "opened_complete":oc,"cited_complete":cc,
     "original_opened_complete":oc,"original_cited_complete":cc,
     "current_audit_opened_complete":oc and bool(aud) and all(s["direct_original_read"] for s in aud) and len({s["source_url"] for s in aud})==len({e["url"] for e in p["opened_evidence"]}),
     "status":stat,"required_evidence":p["required_bundle"],
     "reviewer_required_evidence":[{"condition_id":x["id"],"needed":n["required"][i]} for i,x in enumerate(predicates)],
     "missing_conditions":missing,
     "has_original_returned_citations":bool(p["returned_citations"]),
     "returned_citations_unchanged":p["returned_citations"],
     "original_opened_evidence_unchanged":p["opened_evidence"],
     "original_version_observations":original_versions,
     "current_audit_version_observations":[{"source_id":s["source_id"],"url":s["source_url"],"version":s["version"],"direct_original_read":s["direct_original_read"]} for s in aud],
     "now_vs_original":"Current reopens are separately described; live URL or cached snapshot does not establish identical version. No current evidence is added to the original citation package."})
 reviews.append({"blind_key":row["blind_key"],"question_id":row["question_id"],"reviewer":"cargo_agent_same_model",
  "package_reviews":pkgs,"novelty_category":n["novelty"],"new_target":n["novelty"]=="new_target",
  "proposed_boundary":row["proposed_uses"],"provider_facts":n["provider"],
  "researcher_proposed_use":row["proposed_uses"],
  "questioner_choice":"이 단계에서는 후속 결정 원문을 읽지 않아 미확인",
  "counterexample":{"description":n["counter"],"execution_status":"not_executed; documented constraint or reasoned input case, as reading_mode indicates"},
  "notes":n["notes"],"reviewed_utc":now,
  "prior_explicit_route_exposure":row["blind_key"] in ["B-a1fa7bb168d2","B-ac7b5f5909e2","B-e9f810131568"]})
assert set(notes)=={r["blind_key"] for r in packets}
assert len(reviews)==25
assert len({r["blind_key"] for r in reviews})==25
(HERE/"reviews.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in reviews))
(HERE/"input-receipt.json").write_text(json.dumps({"blind_packet_path":str(packet_path.relative_to(REPO)),"blind_packet_sha256":hashlib.sha256(packet_bytes).hexdigest(),"packet_commit":"64f2db1004d5e40842a6f347a835964bcb8503ef","inputs":inputs,"reviewed_utc":now},ensure_ascii=False,indent=2)+"\n")
packages=[p for r in reviews for p in r["package_reviews"]]
preds=[p for pkg in packages for p in pkg["predicate_reviews"]]
summary={"candidates":len(reviews),"citation_packages":len(packages),"mandatory_predicate_reviews":len(preds),
 "questions":dict(Counter(r["question_id"] for r in reviews)),
 "package_statuses":dict(Counter(p["status"] for p in packages)),
 "original_opened_complete_packages":sum(p["opened_complete"] for p in packages),
 "original_cited_complete_packages":sum(p["cited_complete"] for p in packages),
 "predicate_original_opened_support":sum(p["support_in_original_opened"] for p in preds),
 "predicate_original_cited_support":sum(p["support_in_original_citations"] for p in preds),
 "predicate_support_citation_gaps":[{"blind_key":r["blind_key"],"package_key":p["package_key"],"condition_id":pr["condition_id"]} for r in reviews for p in r["package_reviews"] for pr in p["predicate_reviews"] if pr["support_in_original_opened"] and not pr["support_in_original_citations"]],
 "new_target_candidates":sum(r["new_target"] for r in reviews),
 "new_target_with_cited_complete":sum(r["new_target"] and any(p["cited_complete"] for p in r["package_reviews"]) for r in reviews),
 "audit_open_calls":len(receipts),"audit_unique_urls":len({r["url"] for r in receipts}),
 "audit_body_return_calls":sum(r["status"]=="body_returned" for r in receipts),
 "audit_access_failed_calls":sum(r["status"]=="access_failed" for r in receipts),
 "audit_successful_unique_urls":len({r["url"] for r in receipts if r["status"]=="body_returned"}),
 "audit_direct_original_read_unique_sources":sum(s["direct_original_read"] for s in sources),
 "audit_sum_call_wall_ms":sum(r["elapsed_ms"] for r in receipts),
 "audit_first_request_utc":min(r["started"] for r in receipts),
 "audit_last_response_utc":max(r["finished"] for r in receipts),
 "audit_query_calls":0,"tokens":None,"human_hours":None,
 "explicit_route_exposed_candidates":3,"new_candidate_discovery":0,
 "independence":"same-model separate reviewer; not human independent validation"}
(HERE/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(summary,ensure_ascii=False,indent=2))

