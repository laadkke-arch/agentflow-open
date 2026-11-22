import sys,json,hashlib,re
from pathlib import Path
x=json.loads(sys.argv[1]);r=x.pop("result")
raw=json.dumps(r,ensure_ascii=False,separators=(",",":"))
x["raw_response_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
x["hash_serialization"]="JSON UTF-8 ensure_ascii=False compact separators of received object"
txt="\n".join(c.get("text","") for c in r.get("content",[]) if c.get("type")=="text")
sc=r.get("structuredContent",{})
x["is_error"]=bool(r.get("isError")) or any(t in txt for t in ["Failed to fetch","not accessible via this tool","requires a non-empty"])
x["ref_ids"]=re.findall(r"【(turn[^】]+)】",txt)
x["response_headers"]=txt.splitlines()[:3]
x["response_payload_chars"]=len(sc.get("content","")) if isinstance(sc.get("content"),str) else len(txt)
x["source_role"]="historical_provider" if x["id"].startswith("CG-H") else "followup_decision"
x["phase"]="post_primary_seal";x["discovery_hit"]=False
x["tokens"]=None;x["human_hours"]=None
p=Path(__file__).parent/"receipts";p.mkdir(parents=True,exist_ok=True)
(p/(x["id"]+".json")).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
print(x["id"],"error" if x["is_error"] else "ok")

