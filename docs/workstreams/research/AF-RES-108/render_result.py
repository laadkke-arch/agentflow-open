#!/usr/bin/env python3
"""Render the required tables from the scored records."""
from argparse import ArgumentParser
import json
import re

from adjudicate import LABELS, RETURN, compact, counts, score
from select_passages import ROOT

ORACLES = {
    "S1":"Tcl 59","S2":"Tcl 823","S3":"Tcl 365","S4":"Tcl 881",
    "F1":"원 스크립트·픽셀","F2":"원 height 150와 §9.4","F3":"원 offsetTop + border","F4":"원 픽셀·주축 크기",
}
DIFF = {
    "S1":"b<>0 → b<>NULL","S2":"첫 INSERT 1 → NULL","S3":"첫 a 1 → 2","S4":"1 PRECEDING → 0 PRECEDING",
    "F1":"#ok margin 0 → auto", "F2":"셋째 가로 컨테이너 nowrap → wrap",
    "F3":"align-items flex-start → center","F4":"flex-direction column → column-reverse",
}
DOC_PIN = {
    "SQLite":"3.51.1 실행. 문서 당시판 미확인.",
    "Flexbox":"2025-10-14 CRD. HTML 좌표 미확인.",
}
APPENDIX = """## 판독 및 실행 해석

- **확정 답 8/16, 오답 0/8으로 양쪽이 같다.** E는 F2 정상의 유보를 근거 있는 정답으로 바꿨다. E는 F4 정상에서 K가 보여 준 column의 block 축 문장을 접근성 경고로 바꿔 정답을 유보로 바꿨다. S3 정상·경계에서는 값이 맞았고 정렬 근거가 두 자리 모두 사라졌다. 사전 오답→유보 0건, 사전 오답→정답 0건이었다. [대응 원장](pairs.csv) · [집계](metrics.json)
- **표지와 적용 조건은 따로 검사해야 한다.** S1의 E는 비교 결과의 일반 유형을 언급한 예외를 남겼다. 경계의 NULL 피연산자와 ELSE를 함께 설명하는 근거는 보이지 않았다. S4의 E는 최종 결과 순서에 관한 주석을 남겼고, RANGE의 비수치 분기는 두 방식에서 빠졌다. F1의 동일 구간은 양수 여유 배분의 근거를 같이 보였다. [표시 좌표](packets.jsonl) · [SQLite 표현식](https://sqlite.org/lang_expr.html) · [SQLite RANGE](https://sqlite.org/windowfunctions.html#frame_boundaries)
- **경계 조건이 바뀐 실행은 7/8쌍이다.** S3은 행 값과 허용 순열이 바뀌었다. F4는 같은 y=0을 유지했다. 같은 동점 입력에 covering index만 추가한 보조 시험은 실제 출력 순서를 뒤집었다. F2·F3 편집판은 원 assertion을 각각 1·2건 실패했다. 새 기대값의 rect는 두 실행에서 맞았다. F1·F4 원본은 참조와 픽셀이 일치했다. [실행](runs.jsonl) · [원 기대](evidence/upstream-oracles.json) · [보조 실행](evidence/calibration.json)
- **보조 교정에서는 다른 패턴이 관측됐다.** POSIX 재게시에서 E는 선두 점과 FNM_PATHNAME의 연결을 남겼다. 그 조건 없이 기본 매치를 경계에 적용하면 glibc의 FNM_NOMATCH(1)와 충돌했다. SVG에서는 둘 다 nonzero 규칙을 보였고 evenodd의 짝홀 판정과 표의 초기값이 빠졌다. 두 보조 실측은 주 분모와 별개다. [교정 좌표와 실행](evidence/calibration.json) · [POSIX 재게시](https://man7.org/linux/man-pages/man3/fnmatch.3p.html) · [SVG 원 규격](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty)
- **문자 예산은 동일했고 내용과 바이트가 달랐다.** 두 방식 모두 16번에 19,200 코드포인트, 구간 경계 32개, 추가 이동 0회를 썼다. K는 19,376B, E는 19,342B였다. 입력별 후보 집합과 메타데이터 SHA는 16/16 일치했다. F1의 두 입력에서는 실제 두 구간도 일치했다. 전처리의 공동 벽시계, 후보 수와 문장 검사는 따로 기록했다. [전처리와 비용](evidence/preprocess-cost.json) · [패킷](packets.jsonl)
- **눈가림 범위가 제한된다.** 하나의 작업자가 각 8자리씩 네 화면으로 판독했다. F1은 선정 중 원 본문의 가운데 정렬을 봤다. S3의 문항은 허용 순서를 드러낸다. 같은 문서·입력의 이전 노출과 문장 표지로 방법을 추측할 가능성이 있다. 독립 판독 0회다. 원 기대에서 직접 고정된 8원 시험 입력만 보아도 유지된 답의 범위는 K 5/8, E 4/8이다. [가림과 공유 노출](evidence/exposure.json)
- **완료 상태는 PARTIAL이다.** 36개 고유 1차 자료를 직접 열었다. 필수 층별 하한에서는 18/24를 충족했다. SQLite canonical 시험 네 원문과 POSIX 두 원문의 직접 열람이 6개 결원이다. SQLite의 시험은 정식판 manifest와 일치하는 공식 mirror 바이트를 사용했다. 공개 게시자 문서 네 쪽을 판독했으나 3.51.1 당시 docsrc 등가성은 미확인이다. 두 영역의 원시 HTML 좌표도 미확인이다. [출처 원장](sources.jsonl) · [취득 실패](evidence/access-notes.md)

## 제품에서 반환할 링크

정확한 값이 필요한 사용자는 표 2의 관측값과 원 시험을 먼저 연다. 유지보수자는 표 3에서 해당 입력의 규칙과 바뀔 조건을 함께 확인한다. 편집자는 정답 근거가 두 구간에 들어오는 F1과 한 절을 통째로 열어야 하는 S4·F3을 구분한다. 근거 있게 맞은 F2 정상과 F4 정상의 위치를 함께 보존한다. SQlite 도구 문서의 정렬 문장과 Flexbox의 위치·여백 알고리즘은 링크 하나를 어느 단위로 반환할지 보여 주며, POSIX와 SVG는 같은 선택 방식의 다른 분야 대조다. [제품 연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/product/RESEARCH_BRIEF.md)

정상 근거와 예외를 모두 담을 수 있을 때 짧은 설명과 정확 절을 한 링크에 묶을 수 있다. 한쪽 근거가 가려지면 정확 절과 확인할 입력을 제시하는 방식이 후보가 된다. 두 방식의 우선순위를 바꿔 볼 조건은 아래 표로 인계한다. [재현과 계산](reproduce.md) · [자가검산](SELF_CHECK.md)
"""
END = """| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| 사전 오답 0/8씩이다. E의 F2 정상 정답 1개와 F4 정상 유보 1개가 상쇄됐다. | 같은 비용과 더 많은 고정 경계 조건으로 독립 판독한다. `wrap`의 두 줄 높이와 `column-reverse`의 80px 단일 항목부터 실행한다. | 사전 오답이 실제로 E→유보·정답으로 이동하고 정상 손실보다 꾸준히 크면 E 우선의 범위를 넓힌다. |
| SQLite 당시 문서·Fossil 원 시험 직접 열람과 원시 HTML 좌표가 비어 있다. | [3.51.1 문서 ZIP](https://sqlite.org/2025/sqlite-doc-3510100.zip)과 [CSS 2025 CRD](https://www.w3.org/TR/2025/CRD-css-flexbox-1-20251014/) 원시 HTML을 받아 새 회차에서 다시 선택한다. | 고정판과 텍스트 추출이 달라도 S3의 근거 손실과 F2/F4의 전환이 재현되면 결과의 판 의존성을 낮춘다. |
| 표지어는 S4 비수치 경계와 SVG parity를 놓쳤다. POSIX 원본 도메인은 미확인이다. | [Open Group fnmatch](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fnmatch.html) 및 [SVG fill-rule](https://www.w3.org/TR/2018/CR-SVG2-20181004/painting.html#FillRuleProperty)을 열고 조건절·표 행을 포함한 대안을 같은 비용에서 대조한다. | false-positive 표지에 밀린 정상 근거와 놓친 조건이 동시에 회복되면 표지 위주의 선별을 바꾼다. |
"""


def t(title, headings):
    return [f"## {title}", "", "| " + " | ".join(headings) + " |",
            "| " + " | ".join("---" for _ in headings) + " |"]


def row(xs):
    return "| " + " | ".join(map(str,xs)) + " |"


def text_citations(records):
    return ", ".join("–".join(map(str,r["span"])) for r in records) or "—"


def source(c,anchor=False):
    link=c["doc_url"]+(c["anchor"] if anchor else "")
    return f'[{"절" if anchor else "공통 문서"}]({link})'


def results_table(pairs):
    oracles=json.loads((ROOT/"evidence"/"upstream-oracles.json").read_text())["records"]
    mirror={r["case"]:r["mirror_url"] for r in oracles if "mirror_url" in r}
    out=t("1. 시험·예산 표",["문제 ID·영역","상류 입력 URL·고정판","정상 → 경계","정답의 단위·허용 범위",
                           "양쪽 문서 URL·구간 길이·비용","선정 결원·사전 노출·미확인"])
    for p in pairs[::2]:
        c=p["case"]
        cid=c["case"]
        k,e=(p["methods"][arm]["packet"] for arm in ("K","E"))
        stamp="3.51.1" if c["domain"]=="SQLite" else "f1edffe"
        amount=(f'{source(c)} · K/E {k["cp"]}자(600+600) · {k["utf8"]}/{e["utf8"]}B'
                f' · 공통 메타 {k["metadata_utf8"]}B · 0이동')
        out.append(row([f'{cid} {c["domain"]}',f'[{c["test_id"]} · {stamp}]({c["source"]})'+
                       (f' · [검증 바이트]({mirror[cid]})' if cid in mirror else ""),
                        f"`{DIFF[cid]}`",c["unit"],amount,f'결원 0 · {c["pre_exposure"]} {DOC_PIN[c["domain"]]}']))
    out.extend(["",*t("2. 사전 답·실측 표",["쌍·입력·K/E","패킷 지문·구간 좌표","봉인 답 또는 유보",
                "인용 원문 URL·위치·반대 근거","원 기대·두 실행과 출력 주소","판정","미확인"])])
    for p in pairs:
        c=p["case"]
        cid=c["case"]
        form="정상" if p["form"]=="normal" else "경계"
        l1,l2=(l for l,_ in p["results"])
        expected=compact(p["expected"],cid)
        oracle=(f'[{ORACLES[cid]}]({mirror.get(cid,c["source"])})' if p["form"]==c["original_form"]
                else "[변이 기대](evidence/expected.json)")
        for arm in ("K","E"):
            m=p["methods"][arm]
            a=m["answer"]
            pk=m["packet"]
            coordinates="·".join("–".join(map(str,s["codepoints"])) for s in pk["segments"])
            digest_link=f'[{pk["screen_sha256"][:10]}](packets.jsonl#L{m["packet_line"]})'
            source_link=(f'{source(c,True)} · 지지 {text_citations(a["support"])}'
                         f' · 반대 {text_citations(a["against"])}')
            out.append(row([f"{cid} {form} {arm}",digest_link+" · "+coordinates,
                 f'[{compact(a["predicted"],cid)}](predictions.jsonl#L{m["prediction_line"]})',
                 source_link,f'{oracle} · [2회 {expected}](runs.jsonl#L{l1}-L{l2})',
                 LABELS[m["grade"]],"미확인 · "+(a["needed"] or "독립 판독")]))
    out.extend(["",*t("3. 대응·반환 표",["사례·정상/경계","K → E 판정","막은 오답·잃은 정상 근거",
                  "분자·분모·유보·미실행","권할 절·필요한 예외나 추가 열람","출처 URL·판정을 바꿀 관측"])])
    for p in pairs:
        c=p["case"]
        cid=c["case"]
        k,e=(p["methods"][arm]["grade"] for arm in ("K","E"))
        a,b=RETURN[(cid,p["form"])]
        change={
            ("F2","normal"):"한 줄 cross-size 회복",
            ("F4","normal"):"column block 방향 손실",
            ("S3","normal"):"정렬 근거 손실",
            ("S3","edge"):"동점 근거 손실",
        }.get((cid,p["form"]),"사전 오답 전환 0")
        vals=[]
        for arm,g in (("K",k),("E",e)):
            vals.append(arm+" "+("산출 불가 · 확정 0/1 · 유보 1" if g=="U" else
                "산출 불가 · 확정 산출 불가 · 미실행 1" if g=="X" else f'{int(g=="W")}/1·1/1 · 유보 0'))
        out.append(row([cid+(" 정상" if p["form"]=="normal" else " 경계"),LABELS[k]+" → "+LABELS[e],
             change,"<br>".join(vals)+" · 미실행 "+str(int(k=="X"))+"/"+str(int(e=="X")),
             f'{source(c,True)} · {a}',f'[원 시험]({mirror.get(cid,c["source"])}) · 미확인 {b}']))
    for area,v in counts(pairs).items():
        amounts="<br>".join(
            arm+f' {x["wrong"]}/{x["definite"]}·{x["definite"]}/{x["eligible"]} · 유보 {x["abstain"]} · 미실행 {x["unmeasured"]}'
            for arm,x in v.items())
        label=f'근거 있는 정답 {v["K"]["supported"]} → {v["E"]["supported"]}'
        out.append(row([area+" 합계",label,"오답 전환 0",amounts,
                    "오답/확정 · 확정/적격","[대응 원장](pairs.csv) · 독립 판독 미확인"]))
    return "\n".join(out)


def main():
    p=ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--chat-base")
    args=p.parse_args()
    output=results_table(score(ROOT))+"\n\n"+APPENDIX.replace("SQlite","SQLite")+"\n"+END
    if args.chat_base:
        print(re.sub(r'\]\((?!https?://)([^)]+)\)',lambda m:"]("+args.chat_base.rstrip("/")+"/"+m[1]+")",output),end="")
    elif args.check:
        assert (ROOT/"RESULT.md").read_text()==output
        print("RESULT tables and section ordering verified.")
    else:
        (ROOT/"RESULT.md").write_text(output)


if __name__=="__main__":
    main()
