"""Materialize the manual C1/C2 destination judgments recorded in this study.

This is not a classifier: index sets refer to the fixed arrival audit, whose
opening definitions, relevant input/plot contexts, and special scopes were read.
"""
from pathlib import Path
from urllib.parse import urldefrag, urlsplit
import datetime
import hashlib
import json
import copy

P = Path(__file__).resolve().parent
rows = json.loads((P / "control-second-hop-reading.tmp.json").read_text())
manual = {r["url"]: r for r in json.loads((P / "control-second-hop-manual-scopes.json").read_text())}
frozen_judgments = json.loads((P / "control-second-hop-manual-judgments.json").read_text())
c2 = json.loads((P / "control-C2.json").read_text())
pool_c2 = set(c2["conservative_complete_alternative_ids"])


def evidence(aid, first, second, fact, subfacts=None):
    return {"alternative_id": aid, "atom_verdicts": [
        {"atom_suffix": "A1", "verdict": first, "counts_as_proven": first == "예"},
        {"atom_suffix": "A2", "verdict": second, "counts_as_proven": second == "예"}],
        "verified_fact": fact, "subcondition_facts": subfacts or []}


def code(i, r):
    u = r["url"]
    # URL-keyed frozen manual judgments are authoritative after the initial pass.
    # Fresh content drift needs a fresh review, never index-based reassignment.
    if u in frozen_judgments:
        old = frozen_judgments[u]
        if r["window_text_sha256"] == old["expected_window_text_sha256"]:
            return copy.deepcopy(old["support"]), old["verified_fact"], old["semantic_review_status"]
        return [], "허용 창 내용 해시가 바뀌어 고정 판정을 재사용하지 않음. 원문 재판독 필요.", "미확인: window content drift"
    if frozen_judgments:
        return [], "고정 수동 판정에 없는 새 목적지. 원문 재판독 필요.", "미확인: new destination"
    case = r["source_occurrences"][0]["case_id"]
    support = []
    fact = "연결 또는 실제 도착 범위가 확인되지 않아 기능 근거를 확정하지 않음."
    if not r["destination_section_confirmed"]:
        if "requests.readthedocs.io" in u:
            fragment = urldefrag(u)[1]
            second = "예" if fragment in ("prepared-requests", "requests.Session", "requests.PreparedRequest") else "조건부"
            if fragment == "requests.Response": second = "미확인"
            fact = {"prepared-requests": "Prepared Requests 절의 Request 구성, prepare 및 Session.send 예제를 웹 도구로 확인.",
                    "requests.Session": "Session 클래스의 Python import와 s.get 호출, request/send 메서드 설명을 웹 원문에서 확인.",
                    "requests.PreparedRequest": "PreparedRequest 클래스 예제는 Request 구성, prepare 및 Session.send를 연결함.",
                    "requests.Response": "Response 정의는 HTTP 응답 객체를 설명하며 그 정의만으로 요청 구성·전송을 증명하지 않음.",
                    "requests.Request.prepare": "prepare는 전송용 PreparedRequest를 구성하나 이 메서드 자체는 전송 호출이 아님.",
                    "requests.Session.prepare_request": "Session 설정을 반영한 PreparedRequest 구성을 설명하나 이 메서드 자체는 전송하지 않음."}[fragment]
            support = [evidence("http-client:requests", "예", second, fact)]
            return support, fact, "web semantic supplement; raw HTTP403 preserved"
        return [], fact, "unavailable or fragment missing"

    if case == "C1":
        if i in [58,59,66,67,68]:
            fact = "유지보수자의 원질문에 HTTPX Client 및 get 코드와 요청 전송/리다이렉트 설명이 있음. Requests 이름 언급을 Requests 구성·전송 증거로 바꾸지 않음."
            support = [evidence("http-client:httpx", "예", "예", fact)]
        elif i in [225,227,228,229]:
            fact = "공식 HTTPX 예제가 Client.get 또는 Request 생성 후 client.send, 또는 python -c import httpx/get을 명시함."
            support = [evidence("http-client:httpx", "예", "예", fact)]
        elif i == 226:
            fact = "Routing 절은 URL 패턴별 전송 경로 선택을 명시함. 이 작은 절에는 Request 구성이나 get/send 호출 예제가 없음."
            support = [evidence("http-client:httpx", "예", "조건부", fact,
                                ["generic outgoing routing supported", "explicit construction/send invocation absent in this destination section"])]
        elif i == 71:
            fact = "유지보수자 프로필의 고정 저장소 설명은 HTTPX를 Python HTTP client로 식별하지만 구성·전송 사용법은 없음."
            support = [evidence("http-client:httpx", "예", "미확인", fact)]
        elif i in [61,62,63,64]:
            fact = "실제 댓글 subtree는 리다이렉트 기본값 또는 인자 명칭 의견만 담음. 다른 댓글이나 본문 코드까지 이 도착 절의 근거로 합치지 않음."
        else:
            fact = "프로필·토론 목록·단순 동의 등 실제 읽은 범위에서 HTTP client의 구성·전송 계약을 확인하지 못함."
        return support, fact, "opening and exact relevant context read"

    # C2: affirmative rows below were read for both identity and data visualization.
    if i in set(range(3,30)) - {10,27} or i == 31:
        fact = "Altair 공식 Python 예제/데이터 가이드는 표의 필드·열 또는 DataFrame을 Chart에 연결하여 시각화함."
        support = [evidence("C2-altair", "예", "예", fact)]
    elif i in [2,10,27,30]:
        fact = "Altair 이름과 Python 또는 차트 구성은 확인되지만 이 도착 창에서 해당 tabular 입력 조건의 직접 지지가 부족함. 지도 geometry만 보인 예제를 표 입력 증거로 확대하지 않음."
        support = [evidence("C2-altair", "예", "미확인", fact)]
    elif i in [32,35,37,38,39,40,41,42,43,44,45,54,55]:
        fact = "Bokeh 설치·공동체·모듈/갤러리 목록 또는 일반 시각화 소개를 읽음. 이 범위의 링크 제목만으로 표 입력 동작까지 확인했다고 세지 않음."
        support = [evidence("C2-bokeh", "예", "미확인", fact)]
    elif i == 36:
        fact = "Bokeh 홈페이지는 Python 시각화 라이브러리를 식별하나 표/DataFrame 입력을 명시하지 않음."
        support = [evidence("C2-bokeh", "예", "미확인", fact)]
    elif i == 51:
        fact = "허용된 첫 h1 이후 창은 Pandas-Bokeh를 Pandas/GeoPandas plotting backend로 설명함. Python 언어/호출 지지는 첫 카드의 문맥과 분리함."
        support = [evidence("C2-pandas-bokeh", "미확인", "예", fact)]
    elif i == 56:
        fact = "qtpandas 저장소는 Python 요구, pip 설치 및 Python CSVImportDialog 예제를 명시함. DataFrame 시각화 진술은 첫 카드의 ecosystem 절에 있음."
        support = [evidence("C2-qtpandas", "예", "조건부", fact)]
    elif i == 70:
        fact = "plotnine 저장소는 Python 문법 기반 그림과 dataframe 변수를 시각 속성에 매핑하는 기능을 명시함."
        support = [evidence("C2-plotnine", "예", "예", fact)]
    elif i == 72:
        fact = "Lux 저장소 첫 창의 import lux/import pandas, read_csv와 DataFrame 시각화 추천 예제를 확인."
        support = [evidence("C2-lux", "예", "예", fact)]
    elif i == 73:
        fact = "D-Tale 공식 저장소의 Python 주제 식별과 pandas 자료구조 visualizer 설명을 확인."
        support = [evidence("C2-dtale", "예", "예", fact)]
    elif i == 75:
        fact = "ipyvega 저장소는 Python Package Index, pip 및 pandas 의존성, Vega notebook 시각화를 명시함. 표 입력 지원의 문맥은 첫 ecosystem 카드와 결합할 때만 사용함."
        support = [evidence("C2-ipyvega", "예", "조건부", fact)]
    elif i == 77:
        fact = "HoloViews 홈페이지는 Python 시각화 라이브러리라고 명시하지만 이 창의 표 입력 계약은 확인하지 못함."
        support = [evidence("C2-holoviews", "예", "미확인", fact)]
    elif i == 78:
        fact = "hvPlot 홈페이지 창의 import hvplot.pandas 및 DataFrame scatter/bar 예제와 명시적 Pandas DataFrames 지원을 확인. 렌더러를 별도 frontend로 중복 산입하지 않음."
        support = [evidence("C2-hvplot", "예", "예", fact)]
    elif i in [33,50]:
        fact = "실제 패키지는 R용 Radviz 또는 ggplot2이며 Python 라이브러리 조건의 근접 오답."
        support = [evidence("C2-Radviz" if i == 33 else "C2-ggplot2", "아니오", "예", fact)]
    elif i in [1,76,220]:
        fact = "Vega/Vega-Lite의 JSON 시각화 grammar 또는 HTML5/SVG 출력 설명이다. 이를 Python frontend 자체로 간주하지 않음."
        support = [evidence("C2-vega" if i == 76 else "C2-vega-lite", "미확인", "예", fact)]
    elif i in [81,84,99]:
        fact = "Matplotlib의 Python 시각화 정체성 또는 colormap 설정을 확인. 이 도착 창만으로 독립적인 표 입력 시각화 경로는 확정하지 않음."
        support = [evidence("C2-matplotlib", "예", "미확인", fact)]
    elif i == 82 or 85 <= i <= 97:
        fact = "Matplotlib 함수/예제는 column/2D arrays, x/y 값 쌍, 표 셀 또는 record-array 필드를 받아 plot을 생성함. Parameters와 실제 관련 예제만 읽었으며 모든 옵션의 계약을 검사한 것은 아님."
        support = [evidence("C2-matplotlib", "예", "예", fact)]
    elif i == 101 or i == 102 or i == 115 or 118 <= i <= 141 or i == 143 or 144 <= i <= 152 or 154 <= i <= 172 or 174 <= i <= 182 or 184 <= i <= 207:
        fact = "pandas의 DataFrame/Series plotting 또는 Styler 표 표시 기능을 실제 정의·입력 설명·예제에서 확인. 연결된 외부 렌더러를 별도 구현의 직접사용 근거로 자동 확대하지 않음."
        support = [evidence("C2-pandas", "예", "예", fact)]
        if i in [158,187]:
            fact = "허용된 Chart visualization h1 전체 중 기본 pandas plotting 및 후반 Plotting directly with Matplotlib의 직접 Series/DataFrame 전달 설명과 plt.plot 예제를 확인."
            support = [evidence("C2-pandas", "예", "예", fact), evidence("C2-matplotlib", "예", "예", fact)]
    elif i in [116,117,142,153,183]:
        fact = "pandas/Matplotlib의 데이터 정리, converter 또는 스타일 설정만 확인. 이 절만으로 전체 표 시각화 기능을 입증하지 않음."
        support = [evidence("C2-matplotlib" if i in [153,183] else "C2-pandas", "예", "조건부", fact)]
    elif i == 173:
        fact = "Plotting directly with Matplotlib 절은 Series/DataFrame 직접 전달과 plt.plot/plt.fill_between 호출을 명시함."
        support = [evidence("C2-matplotlib", "예", "예", fact)]
    elif i in [106,114]:
        fact = "원 ecosystem Visualization 전체 절 재도착; 봉인된 10개 이름층 대안을 같은 원문 범위에서 확인."
        support = [evidence(aid,"예","예",fact) for aid in c2["slots"][0]["complete_alternative_ids"]]
    elif i in [103,104,105,107,109,110,111,113]:
        names = {103:["altair"],104:["bokeh","pandas-bokeh"],105:["dtale"],107:["hvplot"],109:["lux"],110:["plotly"],111:["plotnine"],113:["seaborn"]}[i]
        fact = "ecosytem의 해당 실제 하위 절에서 이름과 기능을 확인. 첫 카드의 같은 저자 문맥보다 더 강한 판/호환성 보장은 부여하지 않음."
        support = [evidence("C2-"+name,"예","예",fact) for name in names]
    elif i == 108:
        fact = "IPython Vega의 notebook plotting은 말하지만 이 짧은 하위 절에서 Python과 표 입력을 직접 확인할 수 없음."
        support = [evidence("C2-ipyvega","미확인","조건부",fact)]
    elif i == 112:
        fact = "qtpandas의 DataFrame 시각화는 명시되나 이 짧은 절의 Python 언어 명시는 미확인."
        support = [evidence("C2-qtpandas","미확인","예",fact)]
    elif i in [208,211,212]:
        fact = "Plotly Python 그래프/앱 소개를 확인했지만 이 도착 창에서 DataFrame/표 입력 직접 지지는 확인하지 못함."
        support = [evidence("C2-plotly","예","미확인",fact)]
    elif i == 217:
        fact = "Seaborn을 Python 통계 시각화 라이브러리로 소개하나 홈페이지의 이 창에는 pandas/표 입력이 명시되지 않음."
        support = [evidence("C2-seaborn","예","미확인",fact)]
    elif i in [209,213,214]:
        fact = "HTML redirect 안내만 도착했다. JavaScript/meta 이동이나 추가 클릭을 자동 성공으로 바꾸지 않음."
    elif i in [0,46,79,210]:
        fact = "demo shell, 문자열 포맷, notebook 환경 또는 상업 문의 소개다. 이 도착 범위는 독립 라이브러리의 표 시각화 두 조건을 모두 증명하지 않음."
    else:
        fact = "열람한 도착 범위에서 고정 요구의 두 조건을 모두 확인하지 못함. 미검사 부분을 부정으로 단정하지 않음."
    return support, fact, "opening/definition and exact relevant input-function contexts read"


destinations = []
source_rows = []
for i, r in enumerate(rows):
    support, fact, review = code(i, r)
    case = r["source_occurrences"][0]["case_id"]
    for a in support:
        for atom in a["atom_verdicts"]:
            atom["atom_id"] = case + "." + atom.pop("atom_suffix")
    complete = [a["alternative_id"] for a in support if all(x["counts_as_proven"] for x in a["atom_verdicts"])]
    record = {k:v for k,v in r.items() if k not in ["text","links"]}
    record.update(source_id="C-H2-%03d"%(i+1), source_cases=sorted({o["case_id"] for o in r["source_occurrences"]}),
                  source_candidate_ids=sorted({o["candidate_id"] for o in r["source_occurrences"]}),
                  semantic_review_status=review, verified_fact=fact,
                  per_case=[{"case_id":case,"alternative_atom_support":support,"complete_alternative_ids":complete}],
                  semantic_complete_alternative_ids=complete,
                  reachable_complete_alternative_ids=complete if r["destination_section_confirmed"] else [],
                  pool_membership_changed=False,
                  reading_method="Declared window opening/definition and relevant input/function contexts; not exhaustive reading of every option or unrelated paragraph.",
                  limitation="Documented capability, not code execution or measured human behavior. Identity atoms are implementation-specific; never transfer an atom between libraries.")
    if r["url"] in manual:
        mr=manual[r["url"]]
        record["helper_scope_not_used_for_semantic_judgment"]=r["scope_locator"]
        record["semantic_scope_override"]={k:v for k,v in mr.items() if k!="text"}
    if "requests.readthedocs.io" in r["url"]:
        record["web_semantic_evidence"]={"refs":["turn286228775view0","turn571292173view0","turn571292173view2"],
            "manual_locators":"Prepared Requests lines72–132; API Session238–257, prepare_request422–433, Request.prepare578–581, Response587–590, PreparedRequest715–731",
            "fragment_http_confirmation":"미확인; raw403. Parent browser confirms only original Prepared Requests source arrival separately."}
    destinations.append(record)
    source_rows.append({"source_id":record["source_id"],"original_url":r["url"],
                        "pinned_url_or_version":r.get("document_sha256") or "raw bytes 미확인; web Requests2.34.2 when recorded",
                        "publisher":urlsplit(r["url"]).netloc,"event_or_publication_date":"미확인",
                        "checked_utc":r["checked_utc"],"locator":manual[r["url"]]["manual_scope"]+"; target "+urldefrag(r["url"])[1] if r["url"] in manual else r["scope_locator"],
                        "source_kind":"second-hop primary-document/metadata/access audit","verified_fact":fact,
                        "limitation":record["limitation"]+" Not used to inflate the minimum independent-source reading count.",
                        "question_ids":["Q4","Q5","Q6"],"case_ids":record["source_cases"],
                        "duplicate_group":urldefrag(r["url"])[0].split('?')[0],"counted":False,
                        "connectivity_success":r["connectivity_success"],"semantic_review_status":review,
                        "first_resume_source":r["url"]})

# Every recorded outgoing occurrence is a separate logical trial with its own
# starting card. Document-response reuse is explicit and is not human clicking.
base={}
for s in c2["slots"]:
    cid="C2-"+str(s["slot"]);base[cid]={aid:{"C2.A1","C2.A2"} for aid in s["complete_alternative_ids"]}
base["C2-1"]["C2-qtpandas"]={"C2.A2"}
base["C2-1"]["C2-ipyvega"]={"C2.A2"}
base["C2-4"]={"C2-altair":{"C2.A1"}}
base["C2-6"]={"C2-bokeh":{"C2.A1"}}
for n in [1,2,3,5]:base["C1-"+str(n)]={"http-client:httpx":{"C1.A1","C1.A2"}}
base["C1-4"]={"http-client:requests":{"C1.A1","C1.A2"}}
base["C1-6"]={}
trials=[]
for d in destinations:
    for occ in d["source_occurrences"]:
        case=occ["case_id"];cid=occ["candidate_id"]
        state={aid:set(atoms) for aid,atoms in base.get(cid,{}).items()}
        if d["destination_section_confirmed"]:
            for a in d["per_case"][0]["alternative_atom_support"]:
                state.setdefault(a["alternative_id"],set()).update(x["atom_id"] for x in a["atom_verdicts"] if x["counts_as_proven"])
        complete=sorted(a for a,ats in state.items() if {case+".A1",case+".A2"}<=ats)
        trials.append({"trial_id":"C-H2-TRIAL-%04d"%(len(trials)+1),"case_id":case,"start_candidate_id":cid,
                       "fresh_logical_start":True,"human_clicks_observed":False,
                       "first_step":"open candidate direct URL (1)","second_step":"open the recorded real href (1)",
                       "navigation_cost":2,"source_url":occ["source_url"],"raw_href":occ["raw_href"],"source_dom_index":occ["dom_index"],
                       "first_step_success_is_a_precondition":True,
                       "independent_network_trial_receipt":"parent root execution ledger, not this semantic map",
                       "destination_url":d["url"],"destination_source_id":d["source_id"],
                       "second_step_connectivity_success":d["connectivity_success"],
                       "second_step_section_confirmed":d["destination_section_confirmed"],
                       "complete_ids_after_trial":complete,
                       "complete_ids_in_original_pool":sorted(set(complete)&pool_c2) if case=="C2" else complete,
                       "additional_ids_outside_original_pool":sorted(set(complete)-pool_c2) if case=="C2" else [],
                       "document_fetch_reused":True,"actual_user_response":"미확인",
                       "limitation":"No union across trials. A failed second step does not erase evidence already obtained at first step. Parent selects only displayed starts for each grouping."})

summary={"strict_outgoing_occurrences":len(trials),"unique_destination_urls":len(destinations),
         "unique_document_requests":len(json.loads((P/"control-second-hop-access.json").read_text())),
         "raw_http_success_urls":sum(d["connectivity_success"] for d in destinations),
         "confirmed_raw_destination_sections":sum(d["destination_section_confirmed"] for d in destinations),
         "missing_fragments":sum(d["fragment_exists"] is False for d in destinations),
         "raw_access_failure_urls":sum(not d["connectivity_success"] for d in destinations),
         "non_html_success_urls":sum(d["connectivity_success"] and not d["destination_section_confirmed"] and d["fragment_exists"]=="not applicable" for d in destinations),
         "C2_original_pool_complete_ids":sorted(pool_c2),
         "C2_additional_confirmed_ids_outside_pool":sorted(set(a for t in trials for a in t["additional_ids_outside_original_pool"])),
         "actual_user_response":"미확인","groups_calculated":False,
         "first_step_assumption":"C1 baseline generic capability remains parent adjudication; C1-3 direct execution absence documented in W audit, not silently treated as a runtime test.",
         "requests_note":"Seven original outgoing href occurrences were recovered from parent's fresh rendered-DOM observation. Six raw second-hop URLs remain403; web semantic proofs and original single browser arrival are separate."}
for name,value in [("coding.json",{"protocol":"strict original windows; manual relevant-context reading; no A/B/C computation","destinations":destinations}),
                   ("trials.json",trials),("summary.json",summary)]:
    (P/("control-second-hop-"+name)).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
(P/"control-second-hop-sources.jsonl").write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in source_rows))
print(json.dumps(summary,ensure_ascii=False))
