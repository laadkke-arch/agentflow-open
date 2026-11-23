"""Reconstruct publisher order from frozen listing source; no destination fetches."""
import csv, json, pathlib, re, subprocess, hashlib
import yaml

P=pathlib.Path(__file__).resolve().parent
S=P/"snapshots"
JS_SHA="1a415f9d36c34fe0eae271c05f86a459746ed00b"
LD_SHA="f9e9288d7c41db5643386effff1ff2a3fe820237"
fields=["catalog_id","family","catalog_edition","listing_url","posted_rank","group_rank","group_heading","membership_type","title","explicit_aliases","function_field","language","supported_specification","license","destination_url","destination_display_status","first_action","source_path","source_lines","data_order","upstream_declared","role_at_listing","search_fields_json","nonsearchable_hidden_description","notes"]
def write(name, rows):
    with (P/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
js_text=(S/"js-data.yaml").read_text()
js=yaml.safe_load(js_text)
js_nodes=yaml.compose(js_text).value
for i,(v,node) in enumerate(zip(js,js_nodes),1):
    v["_data_order"]=i;v["_source_lines"]=f"{node.start_mark.line+1}-{node.end_mark.line}"
# Node uses publisher's ECMAScript lowercase.localeCompare comparator.
sortjs="let s='';process.stdin.on('data',x=>s+=x).on('end',()=>{let a=JSON.parse(s);a=a.filter(x=>x.status!=='obsolete');a.sort((a,b)=>a.name.toLowerCase().localeCompare(b.name.toLowerCase()));process.stdout.write(JSON.stringify({locale:Intl.DateTimeFormat().resolvedOptions().locale,rows:a}));});"
proc=subprocess.run(["node","-e",sortjs],input=json.dumps(js),text=True,capture_output=True,check=True)
parsed=json.loads(proc.stdout);ordered=parsed["rows"]
group_match=re.search(r"const toolingTypesOrder = \[(.*?)\];",(S/"js-transform.tsx").read_text(),re.S)
group_order=re.findall(r"'([^']+)'",group_match.group(1))
draft_match=re.search(r"DRAFT_ORDER = \[(.*?)\]",(S/"js-config.ts").read_text(),re.S)
draft_order=re.findall(r"'([^']+)'",draft_match.group(1))
groups={g:[t for t in ordered if g in t.get("toolingTypes",[])] for g in group_order}
extra=sorted(set(g for t in ordered for g in t.get("toolingTypes",[]))-set(group_order))
if extra: raise RuntimeError("Unordered new groups require publisher comparator replication: "+str(extra))
visible=[]
for group,ts in groups.items():
    title=" ".join(x[:1].upper()+x[1:] for x in group.split("-"))
    for gi,t in enumerate(ts,1):
        rank=len(visible)+1
        langs=t.get("languages",[])
        ds=list(map(str,t.get("supportedDialects",{}).get("draft",[])))
        ds.sort(key=lambda d: -draft_order.index(d) if d in draft_order else 1)
        # Field presentation order is checked against public page text separately.
        search=[t["name"],title]
        visible.append(dict(zip(fields,[
          f"SC-{rank:03d}","JSON Schema",JS_SHA,"https://json-schema.org/tools",rank,gi,title,"tooling category; not detailed feature guarantee",
          t["name"],"[]",title," | ".join(langs)," | ".join(ds),t.get("license",""),
          t.get("source",t.get("homepage","")),"catalog modal Source-first destination; resolved before provider actions","open Source-first provider URL (catalog already visible abstraction)",
          "data/tooling-data.yaml",t["_source_lines"],t["_data_order"],json.dumps(t.get("dependsOnValidators",[]),ensure_ascii=False),
          "published tool; category only; runtime identity unconfirmed",json.dumps(search,ensure_ascii=False),
          t.get("description",""),f"description/upstream/compliance excluded from matching; exact Source URL; initially_visible={gi<=5}; catalog_load_more_needed={gi>5}"
        ])))
write("catalog-schema-expanded40.csv",visible[:40])
write("catalog-schema-expanded-all.csv",visible)
write("catalog-schema-initial-viewport.csv",[r for r in visible if r["group_rank"]<=5])
ld_text=(S/"ld-data.yaml").read_text()
ld=yaml.safe_load(ld_text)["implementations"]
ld_root=yaml.compose(ld_text)
ld_nodes=next(v for k,v in ld_root.value if k.value=="implementations").value
for i,(v,node) in enumerate(zip(ld,ld_nodes),1):
    v["_data_order"]=i;v["_source_lines"]=f"{node.start_mark.line+1}-{node.end_mark.line}"
ld_groups=re.findall(r"implementation-card' (language|applicationCategory): '([^']+)'",(S/"ld-index.liquid").read_text())
lrows=[]
for typ,g in ld_groups:
    ts=[]
    for t in ld:
        lang=t.get("language",[]);lang=[lang] if isinstance(lang,str) else lang
        match=t.get("applicationCategory")=="CLI" if typ=="applicationCategory" else t.get("applicationCategory")!="CLI" and any(x in lang for x in g.split(","))
        if match:ts.append(t)
    heading=g.replace(","," / ")
    for gi,t in enumerate(ts,1):
        rank=len(lrows)+1; version=f'{t["jsonldVersion"]:.1f}';state=" (WIP (Work In Progress))" if t.get("state")=="InProgress" else ""
        lang=t.get("language",[]);lang=[lang] if isinstance(lang,str) else lang
        search=[t["name"]]
        lrows.append(dict(zip(fields,[
          f"LD-{rank:03d}","JSON-LD",LD_SHA,"https://json-ld.org/#developers",rank,gi,heading,"language/environment membership",
          t["name"],"[]",""," | ".join(lang),version,"",t["repo"],"direct href in initial list","open implementation repository",
          "index.yaml",t["_source_lines"],t["_data_order"],"[]","publisher lists implementation; complete processor vs plugin vs wrapper not asserted",
          json.dumps(search,ensure_ascii=False),"","No expand/compact/flatten/validation functionality field. Header conformance claim is not per-feature evidence."
        ])))
write("catalog-ld22.csv",lrows[:40])
meta={"schema":{"commit":JS_SHA,"raw_tools":len(js),"active_tools":len(ordered),"expanded_posted_rows":len(visible),"initial_viewport_rows":len([r for r in visible if r["group_rank"]<=5]),"selected_rows":len(visible[:40]),"selected_exact_source_urls":len({x["destination_url"] for x in visible[:40]}),"first40_rule":"expand every Load More; groups publisher order; lowercased name localeCompare; desktop/mobile duplicate render once; take first40","matching_fields":"title, explicit alias (none), displayed tooling category only; other metadata retained for environment restrictions","extra_catalog_load_actions_for_selected40":len({x["group_heading"] for x in visible[:40] if x["group_rank"]>5}),"locale":parsed["locale"],"fallback":False,"test_report_read":False},"json_ld":{"commit":LD_SHA,"raw_implementations":len(ld),"default_visible_posted_rows":len(lrows),"selected_rows":len(lrows[:40]),"selected_exact_source_urls":len({x["destination_url"] for x in lrows[:40]}),"first40_rule":"publisher group order, raw entry order inside group; CLI excluded from language groups","matching_fields":"title only; no explicit alias or function field; language/CLI heading is membership","fallback":False,"test_report_read":False},"boundary":"Source-based expanded catalog abstraction; catalog modal and Load More preparation excluded from provider actions. Not a browser click experiment. No provider destination fetched."}
(P/"reconstruction-receipt.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(meta,ensure_ascii=False,indent=2))

