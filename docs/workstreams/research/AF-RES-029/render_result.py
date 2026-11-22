"""Render required result tables from joined ledgers and the reviewed prose."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
def rows(n):return [json.loads(x) for x in (P/n).read_text().splitlines() if x.strip()]
def cell(s):
    if isinstance(s,(dict,list)):s=json.dumps(s,ensure_ascii=False)
    return str("—" if s is None or s=="" else s).replace("|","\\|").replace("\n","<br>")
def table(headers,rs):
    return "| "+" | ".join(headers)+" |\n| "+" | ".join(["---"]*len(headers))+" |\n"+"".join("| "+" | ".join(cell(x) for x in r)+" |\n" for r in rs)+"\n"
def link(label,url):return f"[{label}]({url})"
def clip(s,n=210):
    if isinstance(s,(list,dict)):s=json.dumps(s,ensure_ascii=False)
    s=str(s or "미확인");return s if len(s)<=n else s[:n]+"…"
def main():
    qs=rows("questions.jsonl");pairs=list(csv.DictReader((P/"pairs.csv").open()))
    pm={x["question_id"]:x for x in pairs};facts=json.loads((P/"evidence/report-facts.json").read_text())
    notes=json.loads((P/"evidence/report-notes.json").read_text())
    decisions=rows("evidence/candidate-decisions.jsonl")
    dmap={(q["id"],r):[x for x in decisions if x["question_id"]==q["id"] and x["route"]==r] for q in qs for r in "CAB"}
    obs={(r["question_id"],r["route"]):r for r in rows("evidence/observation-decisions.jsonl")}
    traces={(r["question_id"],r["route"]):r for r in rows("evidence/failure-trace.jsonl")}
    stage_kr={"supported":"지지","empty_route":"빈 경로","not_appeared":"미등장","name_only":"이름만 등장","exact_component_unread":"정확한 부품/절 미열람","version_environment_conflict":"판·환경·동작 충돌","citation_omission":"인용 누락","novelty_unverified":"신규성 미확인","evidence_unverified":"근거 미확인"}
    kr={"supported":"지지","unverified":"미확인","conflict":"충돌","empty":"빈 반환"}
    def cits(cs,rt):
        return "<br>".join(link(f"{rt}{c['original_rank']}.{i}",z["url"])+" "+z["section"] for c in cs for i,z in enumerate(c["citations"],1)) or "∅ (빈 반환)"
    t1=[]
    for q in qs:
        qid=q["id"];p=pm[qid];n=notes[qid];st=json.loads((P/f"common/{qid}/start.json").read_text())
        cps=st.get("opened",st.get("provider_pages",[]))
        common="<br>".join(link(f"C{i}",z.get("url",z.get("requested_url")))+(" — 접근 실패" if z.get("body_status",z.get("status"))=="fetch_failed" else " — 메타데이터만" if z.get("body_status",z.get("status"))=="metadata_only" else "") for i,z in enumerate(cps,1)) or "∅ (적격 출발점 없음)"
        novelty=[]
        for rt in "AB":
            cc=dmap[(qid,rt)]
            novelty.append(rt+": "+", ".join(f"{c['original_rank']} {dict(new_target='새 대상',new_component_in_named_family='명시 제품군의 새 부품',same_named_use='이미 적힌 같은 용도',unverified='신규성 미확인')[c['novelty']]}" for c in cc) if cc else rt+": 해당 없음")
        t1.append([qid+" · "+("전체" if q["scope"]=="whole" else "부분")+"<br>"+link(n["name"],q["initial_url"]),
            n["goal"]+"<br>"+", ".join(x["id"] for x in q["partial_must"]),common,cits(dmap[(qid,"A")],"A"),cits(dmap[(qid,"B")],"B"),
            kr[p["A_partial_returned_status"]]+" / "+kr[p["B_partial_returned_status"]],
            kr[p["A_whole_returned_status"]]+" / "+kr[p["B_whole_returned_status"]],
            "<br>".join(novelty+[n["unknown"],"실제 저자 사전지식 미확인"])])
    out="# AF-RES-029 · 첫 결과 다음의 새 검색과 제공자 내부 탐색\n\n"
    out+=table(["질문 ID·전체/부분","고정 부분 목적·필수조건","공통 출발 URL","A 반환 URL·절","B 반환 URL·절","부분 지지 A/B","전체 지지 A/B","신규성·미확인"],t1)
    out+="## 2. 실제 반환과 실패\n\n";t2=[]
    for q in qs:
        qid=q["id"]
        for rt in "CAB":
            cc=dmap[(qid,rt)]
            if not cc:
                rr=obs[(qid,rt)];why=clip(rr.get("empty_reason") or "반환 후보 없음. 검색/열람 실패는 원 영수증에서 확인.",300)
                t2.append([f"{qid}·{rt}·∅","후보 없음",link("필수 술어","questions.jsonl")+"; "+link("검색·열람 추적",f"{'common' if rt=='C' else 'routes/'+rt}/{qid}/"),
                    link("실제 전달 범위","visits.jsonl"),"∅",why,"부분/전체 미지지; 빈 경로. 부품 부재를 뜻하지 않음."])
            for c in cc:
                did=f"D-{qid}-{rt}-{c['original_rank']:02d}";evs=[]
                for pd in c["predicates"]:
                    if pd["scope"]!="partial":continue
                    for e in pd.get("opened_evidence",[]):
                        v=e.get("section","")+(f" ({e.get('evidence_id')})" if e.get("evidence_id") else "")
                        if v and v not in evs:evs.append(v)
                opened="<br>".join(evs[:4])
                if len(evs)>4:opened+=f"<br>외 {len(evs)-4}개 위치: "+link(did,"evidence/candidate-decisions.jsonl")
                if not opened:opened="부분 필수조건 본문 근거 미확인; "+link(did,"evidence/candidate-decisions.jsonl")
                pr=c["partial_verdict_returned"];po=c["partial_verdict_opened"];wh=c["whole_verdict_returned"]
                diag=next(x for x in traces[(qid,rt)]["returned_candidates"] if x["candidate_token"]==c["candidate_token"])["diagnostic_stage_by_scope"]
                stage="부분: "+stage_kr[diag["partial"]]+"; 전체: "+stage_kr[diag["whole"]]
                missing=[f"{pd['predicate_id']}: {clip(pd.get('missing_or_conflict'),105)}" for pd in c["predicates"] if pd["scope"]=="partial" and pd["returned_status"]!="supported"]
                needed=", ".join(pd["predicate_id"] for pd in c["predicates"] if pd["scope"]=="partial")+"<br>"+"<br>".join(link(f"근거 {i}",u) for i,u in enumerate(c["original_document_urls"],1))
                t2.append([f"{qid}·{rt}·{c['original_rank']}<br>"+link(did,"evidence/candidate-decisions.jsonl"),c["name"]+"<br>"+clip(c.get("proposed_use",notes[qid]["goal"]),225),
                    needed,opened,cits([c],rt),clip(c.get("remaining_adapter"),235)+("<br>"+"<br>".join(missing) if missing else ""),
                    f"부분 열람 {kr[po]} / 반환 {kr[pr]}; 전체 반환 {kr[wh]}<br>{stage}; "+link("술어별 행","judgments.csv")+" · "+link("실패 추적","evidence/failure-trace.jsonl")])
    out+=table(["질문·경로·순위","후보와 제안한 사용","필요한 근거·원문 URL","열린 절","반환 인용 절","남는 접합·충돌","판정·실패 단계"],t2)
    out+="## 3. 짝 결과와 비용\n\n"
    labels=json.loads((P/"evidence/stratum-labels.json").read_text());t3=[]
    for a in facts["strata"]:
        n=a["n"];succ="해당 없음 (분모 0)" if not n else "; ".join(f"{rt} {a['successes'][rt]}/{n}" for rt in "CAB")
        cost="; ".join(f"{rt} {a['costs'][rt]['navigation']}/{a['costs'][rt]['body_opens']}/{a['costs'][rt]['failed_body_open_attempts']}/{a['costs'][rt]['document_url_count']}" for rt in "CAB")
        exp="미확인도 분모 유지; 모델 판독"
        if a["label"] in ("strict_status_followup_excluded","fully_fresh_pair_only"):exp="효과율 산출 불가; 0%로 쓰지 않음"
        if a["label"]=="top_first_URL_initial_reader_interpretation":exp="Q11-P03 singleton 해석 차이; 원 판독 보존"
        t3.append([labels[a["label"]]+"<br>독립 단위: 설계 사건","C 탐색1/본문2; A 탐색2/본문4; B 탐색2/본문4; 반환 후보≤3·URL≤3"+("; 첫 URL만" if "top_first" in a["label"] else ""),
            succ,f"공통 {a['both_success']} · 양쪽 미지지 {a['both_no_success']} · A승 {a['A_win']} · B승 {a['B_win']}",cost,exp+f"; 빈 반환 C/A/B {a['empty']['C']}/{a['empty']['A']}/{a['empty']['B']}"])
    out+=table(["질문군·관측 단위","경로·상한","표본·성공 분자/분모","공통 성공·양쪽 실패·A승·B승","탐색·열람·실패·URL 수","노출·미확인"],t3)
    body=(P/"report-sections/interpretation.md").read_text()
    costs=facts["strata"][0]["costs"]
    bodycost=table(["경로","실제 요청","탐색 차감","본문 시도","실질 원문 응답","실패 본문 시도","메타데이터/미사용 응답","URL 사용 합계","도구 경과 합계(ms)"],
       [[rt,costs[rt]["web_operations"],costs[rt]["navigation"],costs[rt]["body_opens"],costs[rt]["substantive_original_body_responses"],costs[rt]["failed_body_open_attempts"],costs[rt]["metadata_or_unusable_body_responses"],costs[rt]["document_url_count"],costs[rt]["tool_elapsed_ms_sum"]] for rt in "CAB"])
    out+=body.replace("{{BODY_COST_TABLE}}",bodycost)
    out+="\n## 사건별 첫판·판정 근거와 다음 자료\n\n"
    for q in qs:
        qid=q["id"];rp=q["initial_text_file"].split("AF-RES-029/",1)[-1];n=notes[qid]
        out+=f"### {qid} · {n['name']}\n\n첫 목적: {n['goal']}. 최초 기록 {q['initial_date']}; 원장/구간 {q['ledger']} / {q['period']}; 요청 경계 {'전체' if q['scope']=='whole' else '부분'}. [최초 전문]({rp}) · [고정 원 출처]({q['initial_url']}) · [술어/반증 입력](questions.jsonl) {qid}.\n\n"
        out+=n["analysis"]+"\n\n"
        out+=f"근거 연결: [원 반환](returns.jsonl) {qid}-C/A/B, [실제 열람](visits.jsonl), [술어 판정](judgments.csv) {qid}-*, [검색부터 실패까지](evidence/failure-trace.jsonl) {qid}-C/A/B. 동일 사건의 여러 문서·후보·절은 사건 수를 늘리지 않는다.\n\n"
    out+=(P/"report-sections/counterexamples-and-next.md").read_text()+"\n"+(P/"report-sections/weaknesses.md").read_text()
    (P/"RESULT.md").write_text(out)
    (P/"evidence/result-table-shape.json").write_text(json.dumps({"table1_rows":len(t1),"table2_rows":len(t2),"table2_candidate_rows":len(decisions),"table2_empty_rows":len(t2)-len(decisions),"table3_rows":len(t3),"independent_events":12,"warning":"Table rows are not independent event denominators."},ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"table_rows":[len(t1),len(t2),len(t3)],"utf8_bytes":len(out.encode())}))
if __name__=="__main__":main()
