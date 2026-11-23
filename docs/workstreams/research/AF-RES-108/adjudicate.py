#!/usr/bin/env python3
"""Validate paired receipts, score frozen readings, and render the ledgers."""
from argparse import ArgumentParser
from collections import Counter
from csv import DictWriter
import gzip
from io import StringIO
import json
from pathlib import Path

from select_passages import ROOT, digest, read_jsonl, serialized

LABELS = {
    "S": "근거 있고 맞음",
    "V": "값 맞음·근거 부족",
    "W": "오답",
    "U": "유보",
    "X": "측정 불가",
}

# A citation must carry the decisive rule for this input. The task-provided key,
# declared box geometry, and arithmetic are available to both versions.
SUPPORT = {
    ("S3", "normal", "K"): "첫 정렬식부터 정렬한다는 인용과 주어진 a 오름차순 계약",
    ("S3", "edge", "K"): "같은 정렬식 값의 순서 미정 인용과 입력의 같은 a",
    ("F1", "edge", "K"): "양수 여유의 두 auto margin 균등 배분",
    ("F1", "edge", "E"): "양수 여유의 두 auto margin 균등 배분",
    ("F2", "normal", "E"): "확정 cross-size의 한 줄과 위쪽 10px 입력",
    ("F4", "normal", "K"): "column의 block 축과 주어진 단일 in-flow 항목의 동일 높이",
}

RETURN = {
    ("S1", "normal"): ("§7 CASE에서 첫 true와 ELSE. NULL인 b도 ELSE인지 §2 확인", "b가 NULL인 행만 따로 비교"),
    ("S1", "edge"): ("§2의 NULL 피연산자와 §7의 ELSE를 함께 읽기", "비교가 true인 행 또는 99가 나오는지"),
    ("S2", "normal"): ("§3 SUM에서 정수 결과 조건을 원 시험과 함께 보기", "입력 하나가 REAL이면 typeof 확인"),
    ("S2", "edge"): ("§3 NULL 제외 및 빈 집합 SUM/TOTAL 차이", "남은 비NULL 값이 0개인 추가 입력"),
    ("S3", "normal"): ("§4 ORDER BY 정수 위치와 기본 ASC", "ORDER BY 1이 출력 열 a를 가리키는지"),
    ("S3", "edge"): ("§4 동점 순서와 covering index 진단", "키 b를 추가해 두 계획이 같은 결과인지"),
    ("S4", "normal"): ("§2.2.2 RANGE 수치 band와 비수치 IS 경계", "값 a=5와 문자열 a를 분리해 관측"),
    ("S4", "edge"): ("§2.2.2 0 PRECEDING/CURRENT ROW와 비수치 분기", "0 PRECEDING 위치와 실제 타입"),
    ("F1", "normal"): ("§8.1과 §8.2, 초기 주축 정렬과 margin:0", "default justify-content가 바뀐 경우"),
    ("F1", "edge"): ("§8.1/§9.5 양수 공간 배분과 Ahem 폭", "글꼴 로드 완료 또는 여유 공간 ≤0"),
    ("F2", "normal"): ("§6·§9.4 확정 높이의 한 줄 cross-size", "네 번째 요소의 y와 height 80을 구분"),
    ("F2", "edge"): ("§6·§9.3 줄 수집부터 §9.4/§9.6의 cross-size", "첫 세 개 외곽 높이와 두 번째 줄 offset"),
    ("F3", "normal"): ("§4.1 및 CSS Align §6.2 auto의 static position", "border 1px을 포함한 rect와 offsetTop 대응"),
    ("F3", "edge"): ("§4.1과 CSS Align §6.2, 부모 center 전달 조건", "자식 inset 하나를 고정하면 static position 영향이 남는지"),
    ("F4", "normal"): ("§5.1 column의 block 방향과 §4.1 out-of-flow", "in-flow 자식 높이를 80px로 줄인 별도 시험"),
    ("F4", "edge"): ("§5.1 column-reverse와 주축 여유 0의 기하", "80px 자식의 y가 20px 이동하는지"),
}


def ordered(case, form):
    return case == "S3" and form == "normal"


def canonical_rows(items, case, form):
    tuples = [serialized(row) for row in items]
    return tuples if ordered(case, form) else sorted(tuples)


def types_for(rows):
    return [["null" if v is None else "integer" if isinstance(v, int)
             else "real" if isinstance(v, float) else "text" for v in row] for row in rows]


def observed(run, expected):
    if "px" in expected:
        return {"px": run["probe"]["relativePx"]}
    return {"rows":run["rows"],"types":run["types"]}


def matches(value, expected, cid, form):
    if "px" in expected:
        return "px" in value and abs(value["px"] - expected["px"]) <= 0.5
    expected_types = expected.get("types", types_for(expected["rows"]))
    if "rows" not in value or len(value["rows"]) != len(value["types"]):
        return False
    if expected.get("either_order") and not value.get("either_order"):
        return False
    return canonical_rows(zip(value["rows"],value["types"]),cid,form) == canonical_rows(
        zip(expected["rows"],expected_types),cid,form)


def native_ok(cid, r, native_source):
    if cid.startswith("S"):
        width=len(r["rows"][0])
        flat=native_source["suffix"].split()
        oracle=[flat[i:i+width] for i in range(0,len(flat),width)]
        from_run=[[str(x) for x in row] for row in r["rows"]]
        return canonical_rows(from_run,cid,r["input"])==canonical_rows(oracle,cid,r["input"])
    if not r["original"]:
        return True
    a = r["native_assertions"]
    if cid == "F1":
        return a["pixel_match"]["equal"] and a["original_script_margins"]["report"].count("PASS") == 2
    if cid == "F4":
        return a["pixel_match"]["equal"]
    if cid == "F2":
        return a["upstream_height"]["pass"] and len(r["harness"]["tests"])==6 and all(x["status"]==0 for x in r["harness"]["tests"])
    return a["upstream_offset_y"]["pass"] and len(r["harness"]["tests"])==24 and all(x["status"]==0 for x in r["harness"]["tests"])


def score(root, cache=None):
    cases=json.loads((root/"inputs"/"selection.json").read_text())
    docs=json.loads((root/"evidence"/"documents.json").read_text())
    expected=json.loads((root/"evidence"/"expected.json").read_text())
    originals=json.loads((root/"evidence"/"upstream-oracles.json").read_text())["records"]
    original_by_case={x["case"]:x for x in originals}
    packs={r["packet_id"]:(i,r) for i,r in enumerate(read_jsonl(root/"packets.jsonl"),1)}
    pred={r["packet_id"]:(i,r) for i,r in enumerate(read_jsonl(root/"predictions.jsonl"),1)}
    run_map={(r["case"],r["input"],r["repeat"]):(i,r) for i,r in enumerate(read_jsonl(root/"runs.jsonl"),1)}
    seal=json.loads((root/"evidence"/"prediction-seal.json").read_text())
    assert len(cases)==8 and len(packs)==len(pred)==len(run_map)==32
    assert list(packs)==list(pred)==sorted(packs)
    assert digest((root/"predictions.jsonl").read_bytes())==seal["sealed_predictions_sha256"]
    assert digest((root/"packets.jsonl").read_bytes())==seal["packets_sha256"]
    assert all(r["reader_order"]==i for i,r in pred.values())
    raw_map=json.loads(gzip.decompress((root/"evidence"/"document-map.json.gz").read_bytes()))
    assert set(raw_map)==set(docs)
    for key,mapping in raw_map.items():
        assert digest(serialized(mapping))==docs[key]["position_map_sha256"]
    pairs=[]
    for case in cases:
        cid=case["case"]
        for item in case["inputs"]:
            form=item["form"]
            pair={}
            data=(root/item["path"]).read_bytes()
            assert digest(data)==item["sha256"]
            results=[run_map[(cid,form,i)] for i in (1,2)]
            exp=expected[cid][form]
            ran=all(r["exit"]==0 and not r["timed_out"] for _,r in results)
            eligible=ran
            for _,r in results:
                if not ran:
                    break
                result=observed(r,exp)
                if exp.get("either_order"):
                    result["either_order"]=True
                eligible &= matches(result,exp,cid,form)
                if form==case["original_form"]:
                    eligible &= native_ok(cid,r,original_by_case[cid])
                if cid.startswith("S"):
                    assert canonical_rows(r["values_in_type_probe"],cid,form)==canonical_rows(r["rows"],cid,form)
                else:
                    assert r["document_sha256"]==item["render_sha256"] and r["probe"]["viewport"]==[800,600,1]
                    assert not r["page_errors"] and not r["failed_requests"]
                    if r["screenshot"]:
                        assert digest((root/r["screenshot"]).read_bytes())==r["screenshot_sha256"]
            if eligible:
                a,b=(observed(r,exp) for _,r in results)
                a["either_order"]=bool(exp.get("either_order"))
                eligible &= matches(a,b,cid,form)
            for pid,(i,p) in packs.items():
                if p["case"]!=cid or p["input"]!=form:
                    continue
                index,reading=pred[pid]
                assert p["cp"]==p["union_cp"]==min(1200,docs[p["doc"]]["codepoints"])
                assert p["utf8"]==p["union_utf8"]==sum(s["bytes"] for s in p["segments"])
                assert p["cp"]==sum(s["chars"] for s in p["segments"])
                s1,s2=p["segments"]
                assert s1["codepoints"][1] <= s2["codepoints"][0]
                assert p["boundaries"]==2 and p["incremental_moves"]==0
                assert p["input_sha256"]==item["sha256"]
                for citation in reading["support"]+reading["against"]:
                    a,b=citation["span"]
                    assert any(u<=a<b<=v for u,v in [seg["codepoints"] for seg in p["segments"]])
                if cache is not None:
                    screen=json.loads((cache/"reader"/(pid+".json")).read_text())
                    source=(cache/(p["doc"]+".txt")).read_text()
                    assert digest(source)==docs[p["doc"]]["normalized_sha256"]
                    assert digest(serialized(screen))==p["screen_sha256"]
                    for s in p["segments"]:
                        a,b=s["codepoints"]
                        assert digest(source[a:b])==s["sha256"]
                    for quote in reading["support"]+reading["against"]:
                        assert digest(source[slice(*quote["span"])])==quote["sha256"]
                v=reading["predicted"]
                support=SUPPORT.get((cid,form,p["arm"]))
                label=("X" if not eligible else "U" if v is None else "W"
                       if not matches(v,exp,cid,form) else "S" if support else "V")
                assert not support or reading["support"]
                pair[p["arm"]]={"packet":p,"answer":reading,"grade":label,
                                "packet_line":i,"prediction_line":index,"basis":support}
            assert set(pair)=={"K","E"}
            k,e=(pair[x]["packet"] for x in ("K","E"))
            for field in ("doc","cp","candidate_profile","input_sha256","metadata_sha256","boundaries","incremental_moves"):
                assert k[field]==e[field],(cid,form,field)
            ordered_marker=e["mode_fallback"] or e["included_marked_sentences"]
            assert ordered_marker
            pairs.append({"case":case,"form":form,"results":results,"expected":exp,"eligible":bool(eligible),"methods":pair})
    return pairs


def counts(pairs):
    summary={}
    for area in ("SQLite","Flexbox","전체"):
        these=[p for p in pairs if area=="전체" or p["case"]["domain"]==area]
        methods={}
        for arm in ("K","E"):
            c=Counter(p["methods"][arm]["grade"] for p in these)
            n=c["S"]+c["V"]+c["W"]
            methods[arm]=dict(wrong=c["W"],definite=n,eligible=len(these)-c["X"],supported=c["S"],
                  insufficient=c["V"],abstain=c["U"],unmeasured=c["X"])
        summary[area]=methods
    return summary


def compact(x,cid=None):
    if x is None:
        return "유보"
    if "px" in x:
        return f'{x["px"]:g}px'
    rows=x["rows"]
    if cid=="S1":
        c=Counter(r[0] for r in rows)
        return " + ".join(f"{key}×{count}" for key,count in sorted(c.items()))
    if cid=="S2":
        return f"{rows[0][0]} 정수"
    if cid=="S3":
        s=", ".join("("+",".join(str(v) for v in row)+")" for row in rows)
        return s+(" / 역순 허용" if x.get("either_order") else "")
    return ", ".join(f"{a}→{b}" for a,b in rows)


def csv_text(pairs):
    stream=StringIO()
    fields=["case","input","eligible","K","E","transition","run_lines","K_prediction_line","E_prediction_line",
            "expected","release_document_verified","route","change_observation","source"]
    writer=DictWriter(stream,fields,lineterminator="\n")
    writer.writeheader()
    for p in pairs:
        c=p["case"]
        key=c["case"],p["form"]
        k,e=(p["methods"][arm] for arm in ("K","E"))
        r,change=RETURN[key]
        writer.writerow(dict(case=key[0],input=key[1],eligible=p["eligible"],K=k["grade"],E=e["grade"],
                             transition=k["grade"]+"→"+e["grade"],run_lines=",".join(str(i) for i,_ in p["results"]),
                             K_prediction_line=k["prediction_line"],E_prediction_line=e["prediction_line"],
                             expected=compact(p["expected"],key[0]),release_document_verified=c["domain"]=="Flexbox",
                             route=r,change_observation=change,source=c["source"]))
    return stream.getvalue()


def audit_metrics(pairs):
    flat=[(p["case"]["case"]+"/"+p["form"],p["methods"]["K"]["grade"],p["methods"]["E"]["grade"]) for p in pairs]
    ratios=counts(pairs)
    return {
       "main_cases":len(pairs)//2,"inputs":len(pairs),"packets":2*len(pairs),"local_runs":2*len(pairs),
       "native_fixture_inputs":8,"synthetic_mutations":8,
       "matched_stats":ratios,
       "errors_to_abstentions":[i for i,k,e in flat if k=="W" and e=="U"],
       "errors_to_correct":[i for i,k,e in flat if k=="W" and e in "SV"],
       "correct_normal_to_abstain_or_error":[i for i,k,e in flat if i.endswith("/normal") and k in "SV" and e in "UW"],
       "new_correct_from_abstain":[i for i,k,e in flat if k=="U" and e in "SV"],
       "lost_support_same_correct_value":[i for i,k,e in flat if k=="S" and e=="V"],
       "transitions":dict(Counter(k+"→"+e for _,k,e in flat)),
       "cost":{arm:{
          "codepoints":sum(p["methods"][arm]["packet"]["cp"] for p in pairs),
          "utf8":sum(p["methods"][arm]["packet"]["utf8"] for p in pairs),
          "boundaries":sum(p["methods"][arm]["packet"]["boundaries"] for p in pairs),
          "moves":sum(p["methods"][arm]["packet"]["incremental_moves"] for p in pairs),
          } for arm in ("K","E")},
       "dated_sqlite_docs_verified":0,"raw_html_maps_verified":0,
       "identical_windows_by_input":sum([s["codepoints"] for s in p["methods"]["K"]["packet"]["segments"]]
                   ==[s["codepoints"] for s in p["methods"]["E"]["packet"]["segments"]] for p in pairs),
    }


def main():
    parser=ArgumentParser()
    parser.add_argument("--cache",type=Path)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    pairs=score(ROOT,args.cache)
    holders={
       ROOT/"pairs.csv":csv_text(pairs),
       ROOT/"metrics.json":json.dumps(audit_metrics(pairs),ensure_ascii=False,indent=2)+"\n",
    }
    for path,data in holders.items():
        if args.check:
            assert path.read_text()==data, path
        else:
            path.write_text(data)
    print("Verified 8 pairs, 16 inputs, 32 predictions with in-window citations, and 32 executions.")


if __name__=="__main__":
    main()
