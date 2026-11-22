"""Verify exact requested report structure and ledger joins; no receiver execution."""
import pathlib,json,csv,hashlib,datetime,subprocess,re,ast,argparse
P=pathlib.Path(__file__).resolve().parents[1]
REPO=P.parents[3]
parser=argparse.ArgumentParser();parser.add_argument("--handoff",action="store_true");parser.add_argument("--output",type=pathlib.Path,required=True);args=parser.parse_args()
checks=[]
def ck(name,ok,observed=None):checks.append({"check":name,"passed":bool(ok),"observed":observed})
def tables(t):
 lines=t.splitlines();out=[];start=None
 for i,line in enumerate(lines+[""]):
  if line.startswith("|"):
   if start is None:start=i
  elif start is not None:
   block=lines[start:i];out.append({"start_line":start+1,"end_line":i,"header":[c.strip() for c in block[0].strip("|").split("|")],"rows":block[2:],"raw":block});start=None
 return out
headers=[
["요구 ID·최초판","두 선택과 판별 입력","제공 분야·원리","근거 자료 주소·절","봉인한 정상·경계 예측","후속 근거 주소·판","지지·충돌·판별불가·미확인","깨지는 조건"],
["요구 ID","두 예측이 갈렸는가","어느 출력에서 갈렸는가","관측된 출력·근거 위치","지지 후보","결말 사전 노출","추천 가능한 용도","미확인"]]
weak=["불일치 또는 약점","영향받는 결론","근거 주소·위치","다음 최소 조사","판정이 바뀌는 조건"]
result=(P/"RESULT.md").read_text();tt=tables(result)
ck("result_first_table_header",tt[0]["header"]==headers[0],tt[0]["header"])
ck("result_second_table_header",tt[1]["header"]==headers[1],tt[1]["header"])
ck("result_first_table_rows",len(tt[0]["rows"])==12,len(tt[0]["rows"]))
ck("result_second_table_rows",len(tt[1]["rows"])==6,len(tt[1]["rows"]))
ck("result_analysis_after_two_tables","## 판정과 분야별 해석" in result and result.index("## 판정과 분야별 해석")>result.index(tt[1]["raw"][-1]))
ck("result_ends_exact_three_weakness_rows",tt[-1]["header"]==weak and len(tt[-1]["rows"])==3 and result.rstrip().endswith(tt[-1]["rows"][-1]))
for i,tab in enumerate(tt[:2]):
 ck("result_table_"+str(i+1)+"_row_urls",all("https://" in row for row in tab["rows"]))
source=[json.loads(x) for x in (P/"sources.jsonl").read_text().splitlines()];ids={r["source_id"] for r in source};works={r["work_id"] for r in source if r["work_id"]}
fields=["source_id","work_id","edition_id","url","final_url","publisher","kind","publication_date","changed_date","checked_utc","exact_locator","confirmed","limitations","case_ids","questions","duplicate_of","minimum_count","allocation"]
missing={r["source_id"]:[f for f in fields if f not in r] for r in source if any(f not in r for f in fields)}
ck("source_fields_present",not missing,missing)
ck("source_ids_unique",len(ids)==len(source),len(source))
baddup=[r["source_id"] for r in source if r.get("duplicate_of") and r["duplicate_of"] not in ids|works]
ck("source_duplicate_links_resolve",not baddup,baddup)
counted=[r for r in source if r["minimum_count"]]
ck("source_counted_work_ids_unique",len({r["work_id"] for r in counted})==len(counted),len(counted))
ck("source_counted_not_duplicate",all(not r.get("duplicate_of") for r in counted))
ck("source_counted_urls",all(str(r["url"]).startswith("https://") and str(r["final_url"]).startswith("https://") for r in counted))
ck("source_record_count_in_result",str(len(source))+"열람/탐색/재방문 기록" in result,len(source))
accept=json.loads((P/"evidence/acceptance-evidence.json").read_text())
ck("acceptance_counts_match",accept["counts"]["source_records"]==len(source) and accept["counts"]["unique_counted_works"]==len(counted))
ck("acceptance_items_complete",all(all(k in r for k in ["status","numerator","denominator","unit","evidence","unmet_reason","minimum_next_check"]) for r in accept["acceptance"]),len(accept["acceptance"]))
ck("acceptance_partial_status",accept["status"]=="partial_handoff")
rows=list(csv.DictReader((P/"outcomes.csv").open()))
policies={}
for key in ["strict_pair_denominator_member","original_wording_lenient_case_member","operator_only_case_member"]:
 policies[key]=sorted({r["request_id"] for r in rows if r.get(key)=="true"})
ck("denominator_policies_explicit_0_1_2",[len(v) for v in policies.values()]==[0,1,2],policies)
ck("zero_unique_support_all_policies",all(r["unique_support"]=="false" and r["lenient_unique_support"]=="false" for r in rows))
ck("post_reveal_strengthening_disclosed","사후에 강화한 운용 기준" in result and "최종 방법 반론" in (P/"amendments.md").read_text())
seal=json.loads((P/"evidence/prediction-seal.json").read_text())
hashes={}
for n in ["SCOPE.md","frame.csv","requests.csv","predictions.csv"]:
 raw=(P/n).read_bytes();record=seal["files"][n];expected=record["sha256"] if isinstance(record,dict) else record
 blob=subprocess.check_output(["git","show","0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1:docs/workstreams/research/AF-RES-045/"+n],cwd=REPO)
 hashes[n]={"local":hashlib.sha256(raw).hexdigest(),"sealed_git_blob":hashlib.sha256(blob).hexdigest(),"recorded":expected}
 ck("sealed_git_and_local_hash:"+n,len(set(hashes[n].values()))==1,hashes[n])
scope="docs/workstreams/research/AF-RES-045/"
paths=set(subprocess.check_output(["git","diff","--name-only","4492dd8e9978087b32897ec2685110d24f510473"],cwd=REPO,text=True).splitlines())
paths.update(subprocess.check_output(["git","ls-files","--others","--exclude-standard"],cwd=REPO,text=True).splitlines())
ck("all_changed_paths_owned",all(x.startswith(scope) for x in paths),sorted(paths))
syntax=[]
for script in (P/"evidence").rglob("*.py"):
 try:ast.parse(script.read_text());syntax.append(str(script.relative_to(P)))
 except SyntaxError as e:ck("syntax:"+str(script.relative_to(P)),False,str(e))
ck("python_static_syntax_only",not any(c["check"].startswith("syntax:") and not c["passed"] for c in checks),len(syntax))
ck("self_check_questions",all("## Q"+str(i)+" " in (P/"SELF_CHECK.md").read_text() for i in range(1,8)))
ck("reproduction_and_limits_present",all((P/n).exists() for n in ["evidence/reproduction/REPRODUCE.md","evidence/reproduction/AUDACITY-REPRODUCE.md","evidence/environment-execution-status.json"]))
if args.handoff:
 h=(P/"HANDOFF.md").read_text();ht=tables(h)
 ck("handoff_ends_exact_three_weakness_rows",ht[-1]["header"]==weak and len(ht[-1]["rows"])==3 and h.rstrip().endswith(ht[-1]["rows"][-1]))
 ck("handoff_fixed_result_and_resume","고정 결과 SHA" in h and "재개 첫 행동" in h and "색인 제안" in h)
 ck("final_remote_and_session_receipts",all((P/n).exists() for n in ["evidence/result-verification.json","evidence/session-check.json"]))
data={"generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"checks":checks,"summary":{"passed":sum(x["passed"] for x in checks),"total":len(checks),"failures":[x["check"] for x in checks if not x["passed"]]},"result_tables":[{"start_line":x["start_line"],"end_line":x["end_line"],"rows":len(x["rows"]),"header":x["header"]} for x in tt[:2]],"ending_weakness_rows":3,"sources":{"records":len(source),"counted":len(counted)},"denominator_policies":policies,"protected_hashes":hashes,"input_sha256":{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ["RESULT.md","SELF_CHECK.md","outcomes.csv","sources.jsonl","evidence/acceptance-evidence.json"]},"limit":"Verifies structure, joins and recorded classifications; does not prove donor causality or receiver behavior."}
output=args.output.resolve();output.relative_to(P);output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"output":str(output),"summary":data["summary"]},ensure_ascii=False));raise SystemExit(0 if not data["summary"]["failures"] else 1)
