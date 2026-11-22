#!/usr/bin/env python3
"""Render the four opening tables from the fixed question, key and score files."""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUDGETS = (1, 2, 4)
LABELS = {"official": "공식 판", "history": "실제 답"}
REQUIRED = {"required", "forbidden"}
CASE_LOCATORS = {
    "Q01": ("원 시도 3건 실패. 후속 참여자의 선택은 별도",
            "#issuecomment-684909900", ("E02", 688), "원 요청자의 최종 해결"),
    "Q02": ("글 #2·7 설치 조언, #4에서 FetchContent도 피하려 함",
            "", ("E04", 351), "설치 채택과 수정 이력"),
    "Q03": ("글 #3 작성자가 SYSTEM을 시험해 성공 보고",
            "", ("E07", 30), "실제 툴체인과 수정 이력"),
    "Q04": ("공유 동기 Client 답 수락, 요청자 감사",
            "#discussioncomment-717752", ("E11", 529), "0.18.1 스레드 보장과 적용"),
    "Q05": ("AsyncHTTPTransport 답 수락",
            "#discussioncomment-3525531", ("E13", 259), "수락 후 같은 GET 시험"),
    "Q06": ("글 #2 대상 속성 제안, #3 성공 보고",
            "", ("E15", 100), "성공 댓글의 실제 빌드와 수정 이력"),
    "Q07": ("현재 subtests 사용. #4382569 개별 연결 거절",
            "#discussioncomment-4382569", ("E19", 123), "동시 연결의 사전 명시 범위"),
    "Q08": ("단순 주입 반대, 자원 fixture 답 수락",
            "#discussioncomment-6150250", ("E20", 107), "실제 비용과 팀 동작"),
    "Q09": ("글 #2 설치 먼저, #3 Find 모듈. 선택 미관측",
            "", ("E22", 277), "동일 alias의 실행과 수정 이력"),
    "Q10": ("연결 닫기 수락, 유지관리자가 범용성 이견",
            "#discussioncomment-7693010", ("E25", 57), "두 루프의 보장과 원 HTTPX 판"),
    "Q11": ("직접 x/y 동작 수락, 지원 문서 유보",
            "#discussioncomment-8022883", ("E30", 506), "범용 공개 지원 계약"),
    "Q12": ("0.27.2 고정 수락. 다른 Colab 사례는 실패",
            "#discussioncomment-11415123", ("E32", 24), "wrapper별 설정과 후속 이행"),
}
CASE_COUNTERS = {
    "Q01": ("필요한 절에 도달해도 스코프 오독", "Q01d", "E02", 688),
    "Q02": ("공식 기능과 후속 선호 불일치", "Q02c", "E05", 33),
    "Q03": ("두 분절을 읽은 2절에서 동률", "Q03a", "E07", 33),
    "Q04": ("동기 사용 회수와 비동기 오승인이 동시 증가", "Q04b/c", "E11", 1213),
    "Q05": ("생성자와 비동기 훅에 도달해도 보류", "Q05b", "E13", 321),
    "Q06": ("표준 하한과 대상의 지역 상한을 구별해야 함", "Q06a/b", "E15", 100),
    "Q07": ("실제 subtests 우회는 4절 역사만 개선", "Q07c/d", "E19", 123),
    "Q08": ("4절 M 추가 회수는 자원용 fixture 한 행", "Q08d", "E20", 1243),
    "Q09": ("정상 M은 2절 회수, 잘못 연결한 M은 4절 P보다 실패", "Q09b", "E22", 277),
    "Q10": ("수락된 header는 공식 보류, 1절 M 판정은 지지", "Q10b", "E26", 1295),
    "Q11": ("직접 방식과 indirect의 보장 경계가 다름", "Q11a/c", "E29", 291),
    "Q12": ("제거 근거 첫 절 충돌 3/3. 고정 회수는 2절 M", "Q12a/b", "E32", 24),
}


def read_jsonl(name):
    return [json.loads(s) for s in (ROOT / name).read_text(encoding="utf-8").splitlines() if s]


def table(headers, rows):
    def line(values):
        return "| " + " | ".join(str(v).replace("|", "&#124;") for v in values) + " |"
    return "\n".join([line(headers), line(["---"] * len(headers)), *(line(r) for r in rows)])


class Evidence:
    def __init__(self):
        self.cases = read_jsonl("cases.jsonl")
        self.sources = {r["id"]: r for r in json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))}
        self.keys = {r["row"]: r for r in read_jsonl("keys.jsonl")}
        with (ROOT / "metrics.csv").open(encoding="utf-8", newline="") as file:
            self.scores = {(r["mode"], r["q"], r["basis"], int(r["budget"]), r["format"]): r
                           for r in csv.DictReader(file)}
        self.cost = json.loads((ROOT / "evidence/preparation.json").read_text(encoding="utf-8"))
        self.diagnostics = json.loads((ROOT / "evidence/diagnostics.json").read_text(encoding="utf-8"))

    def src(self, ident, line=None):
        href = self.sources[ident]["url"]
        label = ident
        if line:
            href += f"#L{line}"
            label += f" L{line}"
        return f"[{label}]({href})"

    def score(self, qid, basis, budget, fmt, mode="main"):
        return self.scores[mode, qid, basis, budget, fmt]


def question_table(e):
    rows = []
    for q in e.cases:
        ident = q["id"]
        chosen, anchor, (doc, line), missing = CASE_LOCATORS[ident]
        rows.append([ident, f'[{q["project"]} 원문]({q["url"]}) · {q["published_utc"][:10]}',
                     q["scope"], "<br>".join(req["text"] for req in q["requirements"] if req["kind"] in REQUIRED),
                     "<br>".join(f'{c["id"]} · {c["label"]} — {c["use"]}' for c in q["candidates"]),
                     ", ".join(dict.fromkeys(c["release"] for c in q["candidates"])),
                     f'[{chosen}]({q["url"]}{anchor})', e.src(doc, line), "미확인 · "+missing])
    return table(["질문 ID", "원 질문 주소·판", "전체·부분", "필수 조건", "후보·제안한 사용", "당시 판",
                  "실제 선택 근거", "공식 조건 근거", "미확인"], rows)


def metric_table(e):
    rows = []
    for budget in BUDGETS:
        for basis, name in LABELS.items():
            for fmt in ("A", "P", "M"):
                s = e.score("ALL", basis, budget, fmt)
                per = (f'{float(s["opened_per_success"]):.2f} ({s["opened"]}/{s["pos_recovered"]})'
                       if s["opened_per_success"] else f'미정의 ({s["opened"]}/0)')
                cost = e.cost["presentation_counts"]
                rows.append([f"{fmt} · {budget}", name, f'{s["questions"]}질문 · {s["rows"]}행',
                             f'{s["pos_recovered"]}/{s["ref_positive"]}', f'{s["near_approved"]}/{s["near"]}',
                             f'{s["pos_rejected"]}/{s["ref_positive"]}',
                             f'{s["pred_hold"]}/{s["rows"]} · {s["unreached"]}/{s["mapped"]}', per,
                             f'{e.cost["card_unique_source_pages"]}쪽 · 위치 {cost[fmt+"_locations"]} · 대응 {cost[fmt+"_links"]}'])
    return table(["형식·절 예산", "평가 기준", "질문·후보 분모", "지지 근거 회수", "근접 오답 승인",
                  "적합 탈락", "보류·미도달", "성공당 열람 절", "준비 비용"], rows)


def by_question_table(e):
    rows = []
    for q in e.cases:
        ident = q["id"]
        group_out = []
        mismatch = []
        for gap in ("P-A", "M-P"):
            vals = {basis: [int(e.score(ident, basis, b, gap)["pos_recovered"]) for b in BUDGETS]
                    for basis in LABELS}
            for i, b in enumerate(BUDGETS):
                if vals["official"][i] != vals["history"][i]:
                    mismatch.append(f"{gap}/{b}절")
            show = lambda t: "/".join(f"{v:+d}" if v else "0" for v in t)
            group_out.append(f'공식 {show(vals["official"])}<br>실제 {show(vals["history"])}')
        ref_pos = sum(e.keys[c["id"]]["history"]["verdict"] == "support" for c in q["candidates"])
        note, row, doc, line = CASE_COUNTERS[ident]
        rows.append([f'{ident} · {q["scope"]}', *group_out,
                     ("방향 차이 " + ", ".join(mismatch)) if mismatch else "동일 방향",
                     note, f'{e.src(doc,line)} · [실행](runs.jsonl) `{row}`',
                     "실제 지지 키 0건" if ref_pos == 0 else f'실제 지지 키 {ref_pos}건. 나머지 상태는 keys 참조'])
    return table(["질문·층", "P−A", "M−P", "판정원별 방향", "역전 또는 동률 사례", "근거 절·실행 행", "미확인"], rows)


def claim_table(e):
    s = lambda f: e.score("ALL", "official", 2, f)
    notes = [
        ("Q1", "공개 질문과 선정 범위", f'{e.src("S-Q01")} · {e.src("S-Q07")} · {e.src("S-Q09")}',
         "12질문 · pytest, CMake, HTTPX 각 4. 전체 6, 부분 6.",
         "OUT-C6454의 초기 글과 후속 헤더 위치 조건을 대조해 제외.",
         "CMake 네 건 원 수정 이력, GitHub Discussions 7건은 공개 수정 표시만 확인."),
        ("Q2", "공식 지지·충돌과 실제 사용의 차이", f'{e.src("E03", 112)} · {e.src("E20",107)} · {e.src("H-Q08")}',
         f'공식 지지 {s("A")["ref_positive"]}/45, 충돌 {s("A")["ref_conflict"]}/45, 보류 {s("A")["ref_hold"]}/45. 자연 근접 {s("A")["near"]}/45.',
         "Q08b는 문서가 허용해도 요청자가 선호하지 않음. Q10b는 답 수락, 공식 범위 약함.",
         "후보별 배포 조건과 정답원의 독립 코딩."),
        ("Q3", "조건 연결의 추가 효과를 분리하는 카드", "[카드·해시](packets.jsonl) · [작성 영수증](evidence/prepare-b3.json)",
         f'공통 내용 45/45 일치. 지점 {e.cost["presentation_counts"]["P_locations"]}개, M 간선 {e.cost["presentation_counts"]["M_links"]}개.',
         "직전 해시로 정렬, no-links와 permuted 대조.",
         "동일 편집자가 실제 적용을 알고 작성한 영향."),
        ("Q4", "예산 안에 실제로 연 근거", "[실행](runs.jsonl) · [입력 b1](evidence/input-b1.json)",
         f'2절 공식 지지 도달 A {s("A")["pos_reached"]}/23, P {s("P")["pos_reached"]}/23, M {s("M")["pos_reached"]}/23.',
         "Q05b는 비동기 클래스·재시도 근거에 도달해도 지지 판정 보류.",
         "사람의 탐색 순서, 한 문서 밖 근거에 도달할 운영 경로."),
        ("Q5", "공식 근거 회수와 잘못 승인한 근접 행 비교",
         f'{e.src("E11",1213)} · {e.src("E18",502)} · [집계](metrics.csv)',
         f'2절 P/M 회수 {s("P")["pos_recovered"]}/23 → {s("M")["pos_recovered"]}/23, 오승인 {s("P")["near_approved"]}/14 → {s("M")["near_approved"]}/14.',
         "같은 오승인 총수 안에서 Q04c 오승인 추가, Q07d 오승인 제거.",
         "오승인 비용의 현장 비대칭과 자연 오답의 더 엄격한 분류."),
        ("Q6", "위치·간선 민감도", f'{e.src("E22",277)} · {e.src("E32",24)} · [진단](evidence/diagnostics.json)',
         f'공식 2절 P−A +{int(s("P")["pos_recovered"])-int(s("A")["pos_recovered"])}행, M−P +{int(s("M")["pos_recovered"])-int(s("P")["pos_recovered"])}행.',
         "Q09b 잘못 연결하면 P4보다 악화. Q12a는 세 형식 첫 절 동률.",
         "공식/실제 합의가 낮은 층과 편집 오류 발생률."),
        ("Q7", "편집 부담, 반복 판독, 다른 분야의 적용 범위",
         f'{e.src("X01")} · {e.src("X02")} · {e.src("X04")} · {e.src("X05")} · {e.src("X08")}',
         "소스 판본 38쪽 실제 수집. 2절 공식 P 88/9, M 88/14 열린 절/회수. 의학 3개, 법령 5개.",
         "환자군·기간이 바뀌면 정밀한 통증행도 부족. 시행일 시작 확인은 짧은 s.4로 충분.",
         "독립 편집자, 사람 판독 시간, 유지 비용의 손익분기."),
    ]
    return table(["Q 번호", "주장·판정 범위", "근거 자료 주소·정확한 위치", "확인한 내용·분자와 분모",
                  "반례를 찾은 경로·결과", "미확인·결정을 바꿀 자료"], notes)


def opening():
    data = Evidence()
    return "# AF-RES-021 고정 후보에서 근거 위치와 사용 조건 대응의 효과\n\n" + "\n\n".join(
        f"## 표 {number} {title}\n\n{body}" for number, title, body in (
            (1, "질문과 후보", question_table(data)),
            (2, "형식별 판독", metric_table(data)),
            (3, "질문별 차이", by_question_table(data)),
            (4, "세부 질문의 근거와 반례", claim_table(data)),
        )
    ) + "\n"


def main():
    cmd = argparse.ArgumentParser(description=__doc__)
    cmd.add_argument("--check", action="store_true")
    args = cmd.parse_args()
    text = opening()
    if args.check:
        if not (ROOT / "RESULT.md").read_text(encoding="utf-8").startswith(text):
            raise SystemExit("RESULT.md opening tables differ from current evidence")
        print("Opening tables match cases, keys, and metrics.")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
