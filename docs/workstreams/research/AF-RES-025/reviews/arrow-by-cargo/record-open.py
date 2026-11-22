import sys,json,hashlib,re
from pathlib import Path
x=json.loads(sys.argv[1])
r=x.pop("result")
raw=json.dumps(r,ensure_ascii=False,separators=(",",":"))
texts="\n".join(v.get("text","") for v in r.get("content",[]) if v.get("type")=="text")
x["raw_response_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
x["raw_response_hash_serialization"]="JSON UTF-8 ensure_ascii=False separators=(',',':'), received tool object"
x["ref_ids"]=re.findall(r"【(turn[^】]+)】",texts)
x["response_headers"]=texts.splitlines()[:2]
x["status"]="access_failed" if "not accessible via this tool" in texts else "body_returned"
x["provided_line_numbers"]=[int(n) for n in re.findall(r"^L(\d+)(?:@P\d+)?:",texts,re.M)]
x["cost_category"]="audit_open_not_discovery"
x["not_added_to_original_returned_citations"]=True
x["tokens"]=None
x["human_hours"]=None
p=Path(__file__).parent/"receipts";p.mkdir(exist_ok=True)
(p/(x["id"]+".json")).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
print(x["id"],x["status"],x["raw_response_sha256"])

