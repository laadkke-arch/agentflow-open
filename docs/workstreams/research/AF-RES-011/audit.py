#!/usr/bin/env python3
"""AF-RES-011의 저장된 관측값을 검증하고 기술통계를 재생성한다. 네트워크 호출 없음."""
import argparse, collections, datetime as dt, hashlib, json, pathlib, re
from urllib.parse import urlsplit, urlunsplit

BASE = pathlib.Path(__file__).resolve().parent
PLATFORM_MIN = {"softwarerecs":25,"hackernews":10,"reddit":10,"github":5,"other":5}
INFO_VALUES = {"present","absent","captured","explicit_unknown","undecided","not_applicable","unknown"}
FORMS = {"link_only","link_explanation","experience","comparison_table","text_only"}
ROLES = {"product","component","principle","mixed"}
REASONS = {"L","E","H","T","M","C","P","LIC","TRUST","UX","EXP","OTHER"}
STATUSES = {"accessible","redirected","archived","failed","blocked","not_linked"}
SOURCE_FIELDS = {"id","url","accessed_at_utc","source_type","title","version_or_date","sections_read","confirmed","limits","level","used_in"}

def read(name):
    return json.loads((BASE/name).read_text())
def norm_url(url):
    if not url: return None
    p=urlsplit(url)
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),p.path,p.query,""))
def counts(values):
    return dict(sorted(collections.Counter(values).items()))
def answer_id(case, i, answer):
    return answer.get("analysis_id", f"{case['id']}.A{i+1:03d}")
def get_text(value):
    if isinstance(value,str): return value
    return json.dumps(value,ensure_ascii=False)
def flatten_answers(cases):
    return [(c,i,a) for c in cases for i,a in enumerate(c["answers"])]
def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(doc, sources):
    cs=doc["cases"];errors=[];warnings=[]
    def check(ok, text):
        if not ok:errors.append(text)
    check(len(cs)>=60,"스레드 최소60")
    check(len(cs)==len({c["id"] for c in cs}),"사례 ID 고유")
    check(len(cs)==len({norm_url(c["url"]) for c in cs}),"사례 URL 고유")
    for p,n in PLATFORM_MIN.items():check(sum(c["platform"]==p for c in cs)>=n,f"플랫폼 {p}>={n}")
    for scope in ["whole","part"]:check(sum(c["whole_or_part"]==scope for c in cs)>=20,f"{scope}>=20")
    check(doc["source_commit"]=="020c8d002cf782079053441368ed3e4a95b3289f","foundation SHA")
    fields={"id","url","platform","date","accessed_at_utc","whole_or_part","question_summary","info_codes","clarifications","answers","link_status_now","notes"}
    for c in cs:
        check(fields <= c.keys(),f"{c['id']}:필수필드")
        try:d=dt.date.fromisoformat(c["date"][:10]);check(dt.date(2014,1,1)<=d<=dt.date(2026,11,20),c["id"]+":기간")
        except (ValueError,TypeError):errors.append(c["id"]+":날짜 형식")
        check(len(c["answers"])>=2,c["id"]+":실질답2개")
        for k in range(1,9):check(c["info_codes"].get("I"+str(k))in INFO_VALUES,c["id"]+":I"+str(k))
        for cl in c["clarifications"]:
            check(cl.get("changed_answer")in {"yes","no","unknown"},c["id"]+":changed_answer")
            check(bool(cl.get("evidence")),c["id"]+":되묻기근거")
            if cl.get("changed_answer")=="yes":check(cl.get("respondent")=="original_asker",c["id"]+":yes는원질문자응답필요")
        obs={norm_url(r.get("url")) for r in c["link_status_now"]}
        for i,a in enumerate(c["answers"]):
            tag=answer_id(c,i,a)
            check(a.get("form")in FORMS,tag+":form")
            check(a.get("role")in ROLES,tag+":role")
            check(set(a.get("rejection_codes",[]))<=REASONS,tag+":reason")
            check(a["outcome"].get("accepted") in (None,True,False),tag+":accepted")
            check(a["outcome"].get("asker_response")in {"adopt","reject","try","thanks","none","unknown"},tag+":asker_response")
            if "OTHER"in a.get("rejection_codes",[]):
                check(bool(a.get("other_reason") or a.get("rejection_evidence") or a["outcome"].get("observed_reason") or a.get("summary")),tag+":OTHER사유")
            url=a.get("recommendation_url",a.get("candidate_url"))
            if url and norm_url(url)not in obs:warnings.append(tag+":대표URL과상태URL문자열대조필요:"+url)
        for r in c["link_status_now"]:
            check(r.get("status")in STATUSES,c["id"]+":링크상태")
            check(bool(r.get("observed_at_utc")),c["id"]+":링크시각")
            check(r.get("level")==("D1" if r.get("status")=="not_linked" else "D3"),c["id"]+":링크근거수준")
    accepted_path=BASE/"evidence/accepted-metadata-attempt.json"
    if accepted_path.exists():
        meta=read("evidence/accepted-metadata-attempt.json")
        if meta.get("result")=="metadata_read":
            qm={x["question_id"]:x for x in meta["items"]}
            for c in cs:
                if c["platform"]!="softwarerecs":continue
                qid=int(c["url"].split("/questions/")[1].split("/")[0]);q=qm[qid]
                formal=[a for a in c["answers"] if a.get("is_formal_answer")]
                check(len(formal)==q["answer_count"],c["id"]+":공식API정식답수")
                got=[a for a in formal if a["outcome"]["accepted"]is True]
                check(len(got)==int(q.get("accepted_answer_id")is not None),c["id"]+":공식API채택수")
                if got:check(got[0].get("platform_answer_id")==q["accepted_answer_id"],c["id"]+":공식API채택ID")
    ss=sources["sources"]
    check(len(ss)>=20,"비 스레드 자료20")
    check(len(ss)==len({s["id"] for s in ss})==len({s["url"] for s in ss}),"자료 ID/URL고유")
    for s in ss:
        check(SOURCE_FIELDS<=s.keys(),s["id"]+":출처필드")
        check(s["level"]in {"D1","D2","D3"},s["id"]+":D0제외")
    check(sum(s["source_type"].startswith("platform_") for s in ss)>=6,"규칙메타6")
    check(sum(s.get("counted_as")=="crossfield_literature" for s in ss)>=6,"다른분야문헌6")
    check(sum(s["source_type"]=="community_empirical" for s in ss)>=3,"커뮤니티실증3")
    chosen=read("evidence/reliability-selection.json")
    import random
    check(sorted(random.Random(1101).sample(sorted(c["id"] for c in cs),15))==chosen["sampled_ids"],"재코딩무작위표본")
    for file in ["evidence/reliability-original.json","evidence/reliability-blind.json"]:
        ids=sorted(c["id"] for c in read(file)["cases"]);check(ids==chosen["sampled_ids"],file+":15고정")
    nm=BASE/"evidence/near-misses.json"
    if nm.exists():
        rows=read("evidence/near-misses.json")["pairs"]
        eligible=[r for r in rows if r["count_as_near_miss"]]
        check(len(eligible)>=10,"근접오답10후보조건쌍")
        check(len({r["case_id"] for r in eligible})>=10,"근접오답10서로다른스레드(보완포함)")
    # 저장 금지 필드는 사용자 식별자 원본 필드다. 출처 URL의 저장소 소유자 부분은 제외하지 않는다.
    forbidden={"username","user_name","author_name","profile_url","email","user_id"}
    def keys(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in forbidden:errors.append("개인식별필드:"+k)
                keys(x)
        elif isinstance(v,list):
            for x in v:keys(x)
    keys(cs)
    return {"passed":not errors,"errors":errors,"warnings":warnings}

def summarize(cs):
    aa=flatten_answers(cs)
    cl=[(c,x) for c in cs for x in c["clarifications"]]
    q=[(c,x) for c,x in cl if x.get("target","question")=="question"]
    link=[(c,r) for c in cs for r in c["link_status_now"] if r["status"]!="not_linked"]
    unique_urls={norm_url(r["url"]) for c,r in link if r.get("url")}
    def threads_with(predicate):return [c["id"] for c in cs if predicate(c)]
    reasons={}
    for code in sorted(REASONS):
        selected=[(c,i,a) for c,i,a in aa if code in a.get("rejection_codes",[])]
        reasons[code]={"answer_units":len(selected),"threads":len({c["id"] for c,i,a in selected}),"case_ids":sorted({c["id"] for c,i,a in selected})}
    statuses={}
    for status in sorted(STATUSES-{"not_linked"}):
        rows=[(c,r) for c,r in link if r["status"]==status]
        statuses[status]={"observations":len(rows),"unique_urls":len({norm_url(r["url"]) for c,r in rows}),"threads":len({c["id"] for c,r in rows}),"case_ids":sorted({c["id"] for c,r in rows})}
    strict404=[(c,r) for c,r in link if r["status"]=="failed" and re.search(r"(?<![0-9])(404|410)(?![0-9])",get_text(r.get("evidence","")))]
    outside=[(c,i,a) for c,i,a in aa if a.get("rejection_codes") and not(set(a["rejection_codes"])&{"L","E","H","T"})]
    forms=counts(a["form"] for c,i,a in aa);roles=counts(a["role"] for c,i,a in aa)
    return {
      "n":len(cs),"platform":counts(c["platform"] for c in cs),"scope":counts(c["whole_or_part"] for c in cs),
      "info":{f"I{k}":counts(c["info_codes"][f"I{k}"] for c in cs) for k in range(1,9)},
      "answer_units":len(aa),"forms":forms,"roles":roles,
      "form_thread_presence":{f:sum(any(a["form"]==f for a in c["answers"]) for c in cs) for f in FORMS},
      "role_thread_presence":{f:sum(any(a["role"]==f for a in c["answers"]) for c in cs) for f in ROLES},
      "fit_answers":sum("FIT"in a["codes"] for c,i,a in aa),
      "fit_threads":threads_with(lambda c:any("FIT"in a["codes"] for a in c["answers"])),
      "cross_domain_answers":[{"case_id":c["id"],"answer_id":answer_id(c,i,a),"summary":a.get("candidate",a.get("summary")),"response":a["outcome"]["asker_response"]} for c,i,a in aa if "CROSS_DOMAIN"in a["codes"]],
      "minimal_url_answers":sum(a["form"]=="link_only" and a.get("minimal_answer_kind")=="url_present" for c,i,a in aa),
      "minimal_name_answers":sum(a["form"]=="link_only" and a.get("minimal_answer_kind")=="name_only" for c,i,a in aa),
      "minimal_kind_unknown":sum(a["form"]=="link_only" and not a.get("minimal_answer_kind") for c,i,a in aa),
      "clarifications_all":{"events":len(cl),"threads":len({c["id"] for c,x in cl}),"targets":counts(x.get("target","question") for c,x in cl),"codes":counts(x["code"] for c,x in cl)},
      "clarifications_question":{"events":len(q),"threads":len({c["id"] for c,x in q}),"codes":counts(x["code"] for c,x in q),"outcomes":counts(x["changed_answer"] for c,x in q),"changed_cases":sorted({c["id"] for c,x in q if x["changed_answer"]=="yes"}),"bot_events":sum(x.get("actor")=="bot" for c,x in q)},
      "clarification_explanation_change":sum(x.get("changed_explanation")=="yes" for c,x in cl),
      "asker_response":counts(a["outcome"]["asker_response"] for c,i,a in aa),
      "adopt_threads":threads_with(lambda c:any(a["outcome"]["asker_response"]=="adopt" for a in c["answers"])),
      "try_threads":threads_with(lambda c:any(a["outcome"]["asker_response"]=="try" for a in c["answers"])),
      "reject_threads":threads_with(lambda c:any(a["outcome"]["asker_response"]=="reject" for a in c["answers"])),
      "top_voted_observed_answers":sum(a["outcome"]["top_voted"]is True for c,i,a in aa),
      "top_voted_known_threads":threads_with(lambda c:any(a["outcome"]["top_voted"]is not None for a in c["answers"])),
      "accepted_true":sum(a["outcome"]["accepted"]is True for c,i,a in aa),
      "accepted_known_answers":sum(a["outcome"]["accepted"]is not None for c,i,a in aa),
      "rejection_codes":reasons,
      "any_criticism_answers":sum(bool(a.get("rejection_codes")) for c,i,a in aa),
      "outside_LEHT_only":{"answer_units":len(outside),"threads":len({c["id"] for c,i,a in outside}),"case_ids":sorted({c["id"] for c,i,a in outside})},
      "link_observations":len(link),"link_unique_urls":len(unique_urls),"link_status":statuses,
      "not_linked_records":sum(r["status"]=="not_linked" for c in cs for r in c["link_status_now"]),
      "explicit_404_410":{"observations":len(strict404),"threads":len({c["id"] for c,r in strict404}),"urls":[{"case_id":c["id"],"url":r["url"]} for c,r in strict404]},
      "partial_questions":{"n":sum(c["whole_or_part"]=="part" for c in cs),"adopt_case_ids":threads_with(lambda c:c["whole_or_part"]=="part" and any(a["outcome"]["asker_response"]=="adopt" for a in c["answers"])),"try_case_ids":threads_with(lambda c:c["whole_or_part"]=="part" and any(a["outcome"]["asker_response"]=="try" for a in c["answers"]))},
      "top_long_threads":sorted([{"id":c["id"],"answers":len(c["answers"])} for c in cs],key=lambda x:x["answers"],reverse=True)[:5]
    }

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--write",action="store_true");args=parser.parse_args()
    doc=read("CASES.json");src=read("sources.json");validation=validate(doc,src)
    result={"study_id":"AF-RES-011","generated_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"data_sha256":sha256(BASE/"CASES.json"),"sources_sha256":sha256(BASE/"sources.json"),"validation":validation,"main":summarize(doc["cases"]),"by_platform":{p:summarize([c for c in doc["cases"] if c["platform"]==p]) for p in PLATFORM_MIN},"source_counts":src["count_summary"]}
    exclusions={"without_header_count_gaps":{"T045","T049","T050"},"without_T061":{"T061"},"without_boundary_T057":{"T057"},"without_all_documented_boundaries":{"T045","T049","T050","T057","T061"}}
    result["sensitivity"]={k:summarize([c for c in doc["cases"] if c["id"]not in ids]) for k,ids in exclusions.items()}
    blind=read("evidence/reliability-blind.json")["cases"];repl={c["id"]:c for c in blind}
    result["sensitivity"]["blind_answer_role_substitution_15"]={"definition":"본표본의15개 답 역할·형식만 블라인드 원응답 단위로 치환. 원문 단위 차이도 포함하며 모집단추정 아님.","answer_units":sum(len(repl[c["id"]]["answers"]) if c["id"]in repl else len(c["answers"]) for c in doc["cases"]),"roles":counts(a["role"] for c in doc["cases"] for a in (repl[c["id"]]["answers"] if c["id"]in repl else c["answers"])),"forms":counts(a["form"] for c in doc["cases"] for a in (repl[c["id"]]["answers"] if c["id"]in repl else c["answers"]))}
    if args.write:(BASE/"evidence/metrics.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"validation":validation,"n":result["main"]["n"],"answer_units":result["main"]["answer_units"],"forms":result["main"]["forms"],"roles":result["main"]["roles"],"sources":len(src["sources"])},ensure_ascii=False,indent=2))
    raise SystemExit(0 if validation["passed"] else 1)
if __name__=="__main__":main()

