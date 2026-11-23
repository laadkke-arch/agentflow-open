#!/usr/bin/env python3
"""Build readable tables and denominators from immutable route rows.

Post-outcome interpretation is intentionally separate from pairs.csv.  This
script never writes protocol, exposure, route judgment, or frozen pair files.
"""
from __future__ import annotations
import collections
import csv
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAIR_LABELS = ["A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"]

def read_json(path):
    return json.loads((ROOT / path).read_text())

def read_jsonl(path):
    return [json.loads(s) for s in (ROOT / path).read_text().splitlines() if s.strip()]

def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("<", "&lt;").replace(">", "&gt;").replace("|", "&#124;").replace("\n", " ").replace("\r", "")

def table(headers, rows):
    return "| " + " | ".join(headers) + " |\n| " + " | ".join("---" for _ in headers) + " |\n" + "".join("| " + " | ".join(cell(v) for v in row) + " |\n" for row in rows) + "\n"

def link(label, url):
    return f"[{label}]({url})"

NOTES = {
    "J1": {
        "quote": "“startTime, one, two”; “three lines of output”",
        "post": "현재 채택 첫답은 배열을 더한 뒤 join. 30일 내 질문자 후속 없음. 원 JSON 조각 exit5, 닫힘만 수리한 입력에서는 봉인 filter 3행 일치.",
        "maintainer": "부모 binding을 보존한 채 자식 하나를 현재 입력으로 둔다. 소수점 자릿수 보존은 이번에 새 요구로 추가하지 않았다.",
        "editor": "한 매뉴얼이 입력·반복·출력을 모두 설명한다. 두 번째 링크를 쓸 때는 짧은 공개 join 대안임을 표시한다.",
        "asker": "부모 값과 각 자식의 대응을 같은 filter에서 유지한다. 잘린 입력을 그대로 실행한 성공은 주장하지 않는다.",
    },
    "J2": {
        "quote": "“cat sample.json”; “two top-level properties”; 기대 start=3645, end=3820",
        "post": "현재 채택 답에 질문자의 긍정 댓글이 있음. 비채택 INDEX 답의 실제 제시 출력은 offset=null. 원 숫자·title/artist 대응의 완결은 여전히 미확인.",
        "maintainer": "배열 전체를 유지해 title과 tracks를 같은 객체에서 만든다. 없는 offset의 null과 입력 title/artist 대응을 분리해서 확인한다.",
        "editor": "cat의 전달 계약은 맞지만 누락 입력을 채우지 못한다. 반환 우선순위는 jq의 객체·스코프 설명과 짧은 공개 해법이다.",
        "asker": "두 최상위 필드를 묶는 구조는 제공할 수 있다. 주어진 숫자까지 맞는 완결 예제로 제시하려면 실제 offset 입력이 필요하다.",
    },
    "J3": {
        "quote": "“limitations of OverpassQL”; “in just jq”; [a,b,c,d]→[ab,cd]",
        "post": "현재 채택 첫답은 undocumented _nwise(2)+add. 질문자는 더 복잡한 실제 사례에도 접근이 작동한다고 후속. 원 Overpass 입력·판은 없음.",
        "maintainer": "공개 API인 range/인덱싱/더하기로 같은 쌍 묶기를 구성할 수 있다. _nwise는 공개 답이 undocumented라고 명시한다.",
        "editor": "Overpass 쪽 질의를 바꾸면 'jq만' 조건을 깨뜨릴 수 있다. 생산자 이름 등장 자체를 외부 해법의 필요성으로 읽지 않는다.",
        "asker": "연속 두 항목을 위치로 묶는다. 실제 JSON envelope와 홀수 개 입력 정책은 원 질문에서 확정되지 않았다.",
    },
    "J4": {
        "quote": "“adb logcat”; “grep my.app”; “specificword=[]”",
        "post": "비채택 첫답은 recursive PCRE grep 명령+입출력. 질문자 성공 후속 없음. 봉인 jq filter 범위내8/8 일치; JSON quoting 확장반례는 조기절단.",
        "maintainer": "로그는 raw input으로 받아 문자별 대괄호 깊이를 센다. jq regex 기능에는 Oniguruma가 필요하고 grep 대안에는 -P 지원이 필요하다.",
        "editor": "짧은 grep 답은 사후 대안으로 추가할 수 있다. B가 밀어낸 jq 구현의 'Oniguruma 없는 build' 경고는 완결점수 밖 설명 손실이다.",
        "asker": "한 줄의 literal balanced brackets, 빈 값과 반복 발생을 처리한다. 문자열 안의 ]를 escape/quote 문법으로 해석하는 요구까지 확장하면 봉인 filter는 실패한다.",
    },
    "P1": {
        "quote": "“custom style gets lost during the second step”; simpara role=custom",
        "post": "질문자 self-answer는 Strong→Span(custom-style=test) 우회 성공. 원 DocBook 문단 role 보존과 다른 입력·목표이며 생성 DOCX는 없음.",
        "maintainer": "Asciidoctor 원 시험은 role 방출을 지지하고 Pandoc reader의 simpara 분기는 role을 custom-style로 보존하지 않는다. 소실 위치와 우회 성공을 구분한다.",
        "editor": "공식 custom-style 계약과 실제 후속 코드를 연결하되 '모든 굵은 요소를 test 문자 스타일로'라는 조건을 함께 보여 준다.",
        "asker": "자동 role 전달이 끊긴다는 진단을 준다. 공개 우회 코드는 원 문단별 custom role을 자동으로 복원한 해법이 아니다.",
    },
    "P2": {
        "quote": "“added a second style”; VE 스타일 재사용",
        "post": "공개 답 없음. 질문자가 30일 내 styles.xml의 style name/id를 조사했으나 실제 reference.docx 및 해결 결과는 없음.",
        "maintainer": "custom-style의 Div/Span과 DOCX paragraph/character style 유형을 확인한다. 같은 표시 이름만으로 같은 styleId/type을 보장하지 않는다.",
        "editor": "인접 도구를 발명하지 않는 A=B 대조다. 공식 스타일 계약 한 링크로 시작하고 실제 참조 파일을 받아야 진단을 좁힐 수 있다.",
        "asker": "기존 VE와 새 스타일이 왜 다르게 취급되는지 판단하려면 정의와 최소 입력이 필요하다. 현재 자료만으로 재사용 성공을 보장하지 않는다.",
    },
    "P3": {
        "quote": "“adding line break tags”; “Is there an option in Pandoc”; 사용자2.11.2→3.1.11",
        "post": "현재 채택 답은 주 도구 markdown_in_html_blocks 비활성화. 답변자 화면은 R4.4.2/rmarkdown2.29/Pandoc3.1.11.1. 연구자3.6 중간입력: br38→0, R 전체 미실행. 원문은 옵션을 묻지만 사전 C1은 출력 목표로 고정; 옵션만 허용하는 사후 민감도는 양쪽 부분. 원문에 이전 주 질문의 repost라는 자술도 있음.",
        "maintainer": "YAML scalar의 Markdown 파싱과 RawInline HTML 경계를 구별한다. 사전 raw wrapper와 사후 reader 확장 비활성화는 서로 다른 주 도구 내부 해법이다.",
        "editor": "기본 링크는 원문 매뉴얼, 두 번째는 Rmarkdown YAML까지 연결한 채택 답으로 제시한다. 사후 발견을 B의 사전 승리로 올리지 않는다.",
        "asker": "이 카드의 사후 옵션은 Rmarkdown의 pandoc_args로 markdown_in_html_blocks를 비활성화하는 예다. 원 문자열에 raw 표지를 더한 사전안과 적용 위치가 다르다. 두 방식은 고정3.6 중간 입력에서 같은 표를 냈지만 R 전체와 원 사용자판은 미검증이다.",
    },
    "P4": {
        "quote": "“picture is missing”; LaTeX TikZ→HTML",
        "post": "공개 답은 PDF→MuPDF SVG와 출력 이미지, 질문자 후속 없음. 원 TeX는 RawBlock2개/TikZ1개로 읽힘. 봉인 filter 전체 실행은 exit83, pdflatex.fmt 부재.",
        "maintainer": "diagram filter는 CodeBlock을 처리하지만 원 LaTeX는 RawBlock이다. 공식 RawBlock Lua 예제에 원 TikZ preamble을 공급하고 SVG를 HTML에 포함하는 경로를 문서로 연결했다.",
        "editor": "공식 RawBlock 변환과 SVG 포함 문서를 한 쌍으로 반환한다. TeX·pdf2svg가 없는 환경에서는 문서 완결과 실행 가능을 같은 표지로 표시하지 않는다.",
        "asker": "원 그림의 preamble과 명령을 보존한 재현안은 있으나 이 환경에서 그림 생성은 실패했다. 단순히 HTML 파일이 생기는 것은 목표 그림을 보존했다는 증거가 아니다.",
    },
}

def collect():
    protocol = read_json("protocol.json")
    cases = protocol["cases"]
    pairs = list(csv.DictReader((ROOT / "pairs.csv").open()))
    outcomes = read_json("evidence/post-jq/outcomes.json") + read_json("evidence/post-pandoc/outcomes.json")
    by_case = {x["case_id"]: x for x in outcomes}
    routes = {}
    for case in cases:
        for route in ["A", "B"]:
            base = f"evidence/routes/{case['case_id']}-{route}"
            routes[case["case_id"], route] = {
                "judgment": read_json(base + "/judgment.json"),
                "exposure": read_json(base + "/exposure.json"),
                "access": read_jsonl(base + "/access.jsonl"),
            }
    return protocol, cases, pairs, by_case, routes

def calculate(cases, pairs, outcomes, routes):
    counts = {}
    for stratum in ["all", "boundary", "control"]:
        selected = [x for x in pairs if stratum == "all" or x["stratum"] == stratum]
        count = {label: 0 for label in PAIR_LABELS}
        for row in selected:
            count[row["strict_pair"]] += 1
        counts[stratum] = {**count, "planned_pairs": len(selected),
                           "comparable_pairs": sum(x["strict_comparable"].lower() == "true" for x in selected)}
    attempts, failed, searches, extra, unexposed = 0, 0, 0, 0, 0
    for key, route in routes.items():
        access = [x for x in route["access"] if x.get("event") == "body_attempt"]
        attempts += len(access)
        failed += sum(x.get("status") != "success" for x in access)
        extra += max(0, len(access) - 4)
        exposed = {x["file_id"] for x in route["exposure"]["slots"] if not x["empty"]}
        unexposed += len(set(route["judgment"]["used_file_ids"]) - exposed)
    searches = sum(x.get("event") == "search" for x in read_jsonl("evidence/search-events.jsonl"))
    boundary = [x for x in pairs if x["stratum"] == "boundary"]
    public = read_json("evidence/outcomes/public-records.json")
    def flag(x):
        return str(x).lower() == "true"
    out = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "basis": "pairs.csv plus immutable route access/exposure/judgment; post outcomes never change frozen labels",
        "cases": len(cases), "routes": len(routes), "explicit_conditions": sum(len(x["conditions"]) for x in cases),
        "counts": counts, "searches": searches, "body_attempts": attempts,
        "failed_body_attempts": failed, "excess_body_attempts": extra, "unexposed_used_file_occurrences": unexposed,
        "B_boundary_adjacent_exposed": sum(flag(x["B_adjacent_exposed"]) for x in boundary),
        "B_boundary_adjacent_opened": sum(flag(x["B_adjacent_opened"]) for x in boundary),
        "B_boundary_adjacent_returned": sum(flag(x["B_adjacent_returned"]) for x in boundary),
        "B_boundary_completeness_changed": sum(flag(x["B_completeness_differs_from_A"]) for x in boundary),
        "discordant_pairs": counts["all"]["A만"] + counts["all"]["B만"],
        "B_win_fraction_among_discordant": "산출 불가 (분모 0)" if not counts["all"]["A만"] + counts["all"]["B만"] else counts["all"]["B만"] / (counts["all"]["A만"] + counts["all"]["B만"]),
        "public_answer_count": sum(len(x["answers"]) for x in public),
        "public_comment_count": sum(len(x["comments"]) for x in public),
        "current_accepted_questions": sum(x["current_accepted_answer_id"] is not None for x in public),
        "questions_with_no_answer": sum(not x["answers"] for x in public),
        "questions_with_asker_action_in_30d": sum(bool(x.get("asker_actions_30d")) for x in outcomes.values()),
        "exact_asker_execution_verified": sum(x.get("exact_asker_execution_verified", False) for x in outcomes.values()),
        "source_counts": read_json("evidence/source-counts.json"),
    }
    prior = read_json("evidence/pre-outcome-metrics.json")
    for key in ["counts", "searches", "body_attempts", "failed_body_attempts", "B_boundary_adjacent_exposed", "B_boundary_adjacent_opened", "B_boundary_adjacent_returned", "discordant_pairs"]:
        assert out[key] == prior[key], (key, out[key], prior[key])
    assert len(pairs) == len(cases) == len(outcomes) == 8
    assert extra == unexposed == 0
    sensitivity = json.loads(json.dumps(counts))
    assert next(x for x in pairs if x["case_id"] == "P3")["strict_pair"] == "양쪽"
    for group in ["all", "boundary"]:
        sensitivity[group]["양쪽"] -= 1
        sensitivity[group]["어느 쪽도 아님"] += 1
    out["posthoc_option_only_sensitivity"] = {
        "after_unblinding": True, "affected_case": "P3", "frozen_pair_file_changed": False,
        "counts": sensitivity, "discordant_pairs": 0,
        "B_win_fraction_among_discordant": "산출 불가 (분모 0)",
        "source": "evidence/post-evaluation-sensitivity.json",
    }
    return out

def output_csv(cases, outcomes):
    fields = ["case_id", "question_id", "question_creation_utc", "deadline_30d_utc", "answer_ids", "first_answers_and_revisions", "current_accepted_answer_id", "acceptance_time", "asker_actions_30d", "first_answer_summary", "execution_input", "execution_command", "execution_version", "execution_output", "execution_attribution", "exact_asker_execution_verified", "agreement_with_frozen", "post_links", "keep_or_change_reason", "ask_one", "limitations", "frozen_verdict_changed", "detail_file"]
    with (ROOT / "outcomes.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n")
        w.writeheader()
        for case in cases:
            o = outcomes[case["case_id"]]
            e = o["execution_fields"]
            window = o.get("observation_window", o)
            row = {
                "case_id": case["case_id"], "question_id": case["question_id"],
                "question_creation_utc": window.get("question_creation_utc", case["creation_utc"]),
                "deadline_30d_utc": window.get("deadline_30d_utc"), "answer_ids": o["answer_ids"],
                "first_answers_and_revisions": o.get("answer_dates", o.get("answer_versions")),
                "current_accepted_answer_id": o["accepted_now"],
                "acceptance_time": "미확인: 현재 표지와 30일 내 채택 시각은 다름",
                "asker_actions_30d": o["asker_actions_30d"], "first_answer_summary": o["first_answer_summary"],
                "execution_input": e.get("input"), "execution_command": e.get("command"),
                "execution_version": e.get("version"), "execution_output": e.get("output"),
                "execution_attribution": e.get("attribution", "공개 후속 발화자·입력 동일성은 detail_file의 execution_fields 참조"),
                "exact_asker_execution_verified": o["exact_asker_execution_verified"],
                "agreement_with_frozen": o["agreement_with_frozen"], "post_links": o["post_links"],
                "keep_or_change_reason": o["keep_or_change_reason"], "ask_one": o["ask_one"],
                "limitations": o["limitations"], "frozen_verdict_changed": False,
                "detail_file": f"evidence/post-{'jq' if case['tag']=='jq' else 'pandoc'}/outcomes.json",
            }
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()})

def build_tables(cases, pairs, outcomes, routes):
    repos = {x["label"]: x for x in read_json("corpus-plan.json")["repositories"]}
    first, second, third = [], [], []
    pairmap = {x["case_id"]: x for x in pairs}
    for c in cases:
        cid = c["case_id"]
        def version(label):
            if not label:
                return "없음(A=B)"
            r = repos[label]
            return r["repo"] + "@" + r["version"] + " / " + str(r.get("commit") or "release archive")[:12]
        conditions = "; ".join(x["id"] + ": " + x["requirement"] for x in c["conditions"])
        if c["second_condition_blank"]:
            conditions += "; C2=공석(별개 명시조건 없음)"
        userv = c["user_versions"]
        if isinstance(userv, dict):
            userv = "; ".join(k + "=" + str(v) for k, v in userv.items())
        first.append([
            f"{cid} / {c['question_id']} / " + link("R0", c["r0_url"]) + f" / GUID {c['r0_guid']}",
            c["input_summary"] + " → " + c["desired_output"] + " 원문: " + NOTES[cid]["quote"],
            conditions,
            "비교 주=" + version(c["main_label"]) + "; 인접=" + version(c["adjacent_label"]) + "; 사용자=" + userv,
            f"{c['tag']} 원순번 {c['original_rank']}; {c['stratum']}; " + c["adjacency_evidence"] + "; 이전 ID 중복0, 알려진 답0. 원래 생성 바이트 동일성은 grace-period 때문에 미확인.",
        ])
        for route_name in ["A", "B"]:
            route = routes[cid, route_name]
            j, e = route["judgment"], route["exposure"]
            accesses = [a for a in route["access"] if a.get("event") == "body_attempt"]
            ranks = "; ".join(f"slot{s['slot']} {s['file_id']} {s['role']}#{s['within_role_rank']}/전체#{s['merged_global_rank']}" if not s["empty"] else f"slot{s['slot']} 공석" for s in e["slots"])
            sources = []
            for source in j["returned_sources"]:
                sections = "; ".join(f"L{s['start']}-{s['end']}: {s.get('claim','')}" for s in source["sections"])
                sources.append(link(source["file_id"], source["url"]) + " " + sections)
            evidence = "; ".join(f"{x['condition_id']}={x['status']} [{','.join(x['evidence_file_ids'])}]: {x.get('interface','')}; 반대/미확인={x.get('contradictory_or_missing','')}" for x in j["condition_evidence"])
            first_time = min(a.get("started_utc", a.get("utc", "")) for a in accesses)
            last_time = max(a.get("finished_utc", a.get("utc", "")) for a in accesses)
            second.append([
                cid + "-" + route_name + "; 순서 " + "→".join(c["route_order"]), ranks,
                f"검색2; 시도{len(accesses)}/4; 실패{sum(a.get('status')!='success' for a in accesses)}; 잔여{4-len(accesses)}; {first_time}~{last_time}; 중단={j['stop_reason']}",
                " / ".join(sources), evidence,
                j["judgment"] + "; " + " / ".join(j["limitations"]),
            ])
        p, o = pairmap[cid], outcomes[cid]
        comparison = "절차상 가능; 동일 태그 연구자의 교차 기억 있음"
        if cid in ["P3", "P4"]:
            comparison += "; 양 경로 열람 뒤 공통 기준 재검토"
        b = routes[cid, "B"]
        adjacent_ids = {s["file_id"] for s in b["exposure"]["slots"] if not s["empty"] and s["role"] == "adjacent"}
        opened_adjacent = {a["file_id"] for a in b["access"] if a.get("event") == "body_attempt" and a.get("status") == "success"} & adjacent_ids
        returned_adjacent = {s["file_id"] for s in b["judgment"]["returned_sources"]} & adjacent_ids
        third.append([
            cid + ": " + comparison, p["strict_pair"],
            f"B 인접 파일 노출{len(adjacent_ids)}/열람{len(opened_adjacent)}/반환{len(returned_adjacent)}; 완결변화={p['B_completeness_differs_from_A']}",
            NOTES[cid]["post"] + " " + " / ".join(link(str(a), f"https://stackoverflow.com/a/{a}") for a in o["answer_ids"]),
            o["keep_or_change_reason"] + " " + " / ".join(link(item.get("purpose", item.get("reason", "사후 반환")), item["url"]) for item in o["post_links"]), " / ".join(o["limitations"]),
        ])
    return (
        "## 표 1. 최초 요청과 고정 조건\n\n" + table(["요청 ID·최초 보존 URL", "원 입력·원하는 출력", "명시 조건·빈칸", "주·인접 도구와 판", "선정·제외 근거"], first)
        + "## 표 2. 사전 노출·실제 열람·조건별 판정\n\n" + table(["요청·경로", "노출 파일 ID와 순위", "실제 시도·실패·잔여 예산", "반환 URL·볼 절", "조건별 근거와 접합 여부", "판정·미확인"], second)
        + "## 표 3. 쌍별 비교와 사후 공개 근거\n\n" + table(["요청·비교 가능성", "A만·B만·양쪽·어느 쪽도 아님", "인접 노출·열람·반환", "사후 공개 근거·사용자 행동", "유지·바꿀 링크와 이유", "한계"], third)
    )

def build_cards(cases, outcomes):
    out = ["# AF-RES-096 · 조건부 반환 카드\n\n각 요청의 링크는 최대 두 개다. 사후 링크를 포함한 편집안이며 봉인된 A/B 반환·승패를 변경하지 않는다. '완결'은 고정판의 문서 적합을 뜻하고 원 사용자의 실행 성공과 다르다.\n"]
    for c in cases:
        cid, o = c["case_id"], outcomes[c["case_id"]]
        links = o["post_links"]
        assert len(links) <= 2
        out.append(f"\n## {cid} · {c['question_id']}\n\n")
        for n, item in enumerate(links, 1):
            out.append(f"{n}. {link(item.get('purpose', item.get('reason', '근거')), item['url'])}\n")
        out.append("\n**질문자에게:** " + NOTES[cid]["asker"] + "\n\n")
        out.append("**유지관리자에게:** " + NOTES[cid]["maintainer"] + "\n\n")
        out.append("**검색 결과 편집자에게:** " + NOTES[cid]["editor"] + "\n\n")
        out.append("**되물을 한 가지:** " + o["ask_one"] + "\n\n")
        out.append("**귀속·한계:** " + NOTES[cid]["post"] + " 위 처리 설명과 추천은 연구자의 적용 추론이며, 원문 사실과 사후 실행의 자세한 귀속은 outcomes.csv 및 각 sources 원장에 있다.\n")
    (ROOT / "cards.md").write_text("".join(out))

def main():
    protocol, cases, pairs, outcomes, routes = collect()
    metrics = calculate(cases, pairs, outcomes, routes)
    (ROOT / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n")
    output_csv(cases, outcomes)
    build_cards(cases, outcomes)
    counts = []
    for name, group in [("경계 요청", "boundary"), ("같은 범위 대조", "control"), ("전체", "all")]:
        x = metrics["counts"][group]
        counts.append([name, x["planned_pairs"], x["comparable_pairs"], *[x[k] for k in PAIR_LABELS]])
    header = "# AF-RES-096 · 앞뒤 단계 원문 노출 정책의 8쌍 비교\n\n"
    body = build_tables(cases, pairs, outcomes, routes)
    body += "## 분자·분모와 연구 상태\n\n"
    body += table(["구분", "예정 쌍", "절차상 비교가능", "A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"], counts)
    body += """**연구 상태: PARTIAL.** 신규 8쌍·16경로, 자료 하한, 사전/사후 분리, 원행 재계산은 수행했다. 지정 고정 의존의 계약 생성은 원격 브랜치가 이미 다른 SHA로 이동하여 거부되었다. 성공한 도구 생성 manifest는 없다. 원 사용자 전체 환경의 실행 성공을 확인한 요청은 0/8이므로, 문서 완결 5/8을 원 사용자의 실제 성공률로 제시하지 않는다. 계약·공통 검사 실제 결과와 대상 SHA는 마지막 HANDOFF에 고정한다.

| 단계 | 분자 / 분모 | 의미 |
| --- | --- | --- |
| 모집 | jq45/최대60, pandoc31/최대60 | 2025 H1 현재 가시 태그·생성순 목록. 각 API has_more=false; H2 확장0 |
| 최초 보존 revision 확보 | 76/76 | revision1 시각=생성 시각. grace-period 내 원 바이트 동일성은 미확인 |
| 연구자가 최초 본문 직접 읽음 | jq45/45, pandoc10/31; 전체55/76 | 후순위는 첫3+1 선정 결과를 대체하지 않음. 기계 취득을 직접 읽은 자료 수에 더하지 않음 |
| 선정 | 경계6/6 자리, 대조2/2 자리 | jq 원순번1·3·4·5, pandoc1·2·3·4. 기존60 ID와 중복0, 양 태그 중복0, 알고 있던 답0 |
| 고정 파일 corpus | 3,560개 / 8 프로젝트 | 최초 논리 archive 다운로드8회, 22,951,621 bytes. 메타데이터 범위 수정 후 같은 archive로 재구축1회 |
| 검색 | 32/32 예정 회 | 각16경로에 동일한 질의2개; 한 파일 결과1개 |
| 노출 | 64/64 자리, 공석0 | 파일당 같은600자. 양 대조의 A/B 네 자리 동일 |
| 본문 접근 | 64/64 한도, 성공64, 실패0 | 경로당4회, 초과0, 재시도0, 미노출 근거 이용0. 같은 열린 파일 절 탐색194회는 별도 기록 |
| B 인접 원문 실제 노출 | 경계6/6쌍, 12/12 인접 자리 | AF-RES-092의 노출0과 구별되는 정책 실행 관측 |
| B 인접 원문 실제 열람 | 경계6/6쌍, 12/12 인접 자리 | 후보 존재와 연구자 열람을 따로 셈 |
| B 인접 원문 최종 반환 | 경계3/6쌍 | J2·J4·P1; 그로 인해 완결 여부가 바뀐 쌍0/6 |
| 문서 완결 | A5/8, B5/8; 경계각4/6, 대조각1/2 | J1·J3·J4·P3·P4. J2/P2 부분, P1 반박 |
| 단독 완결 불일치 | 0/8쌍 | 그 안의 B 승률은 **산출 불가(분모0)**. 비율0%로 쓰지 않음 |
| 사후 답·댓글 | 답8개/질문8개, 댓글18개 | P2 답0. 현재 채택표지4/8; 채택 시각·30일 내 채택 여부는 미확인 |
| 질문자 30일 내 공개 후속 | 5/8질문 | J2·J3·J4 댓글/수정, P1 self-answer, P2 진단 댓글. J1·P3·P4에서는 관측되지 않음 |
| 동일 원입력·사용판·출력으로 검증한 질문자 실행 | 0/8 | 답변자 출력, 연구자 재현 및 현재 채택 표지와 분리 |
| 직접 연 고유 1차 자료 | 46/최소24 | 신규 R0 8, 주 도구10, 인접10, 상류 원시험4, Sphinx7, GDAL/PROJ7 |

46은 서로 다른 고정 원문 수다. 분석 단위는 **서로 다른 선정 질문 ID 8개**이며, 질문 ID를 기준으로 한 사건 수는8이다. 실제 문제 사건이나 저자/사용자의 독립성은 미확인이다. 특히 P3는 이전 주 질문의 repost라고 자술하므로 ID8을 독립 실제 사건8로 단정하지 않는다. 이전 ID는 본문에 없고 이번에 추적하지 않았다. 공식 프로젝트 저작 계보는 **11**이다. 상류 원 시험4파일은 jq·Asciidoctor 두 계보이고 네 독립 실행 성공 사건이 아니다. Q7의14파일은3프로젝트·5교정 목표, 새 요청·사전 경로 기여0이다. 사후 답·댓글·이미지·재현 출력, 선행 인계, 검색 미리보기, 메타데이터·라이선스·같은 원문 재열람은 최소량에 더하지 않는다. ③의 독립 사건 표현을 좁힌 이유·시각·원값은 [사후 민감도 기록](evidence/post-evaluation-sensitivity.json)에 남겼다. [원장](sources.jsonl), [하한 재계산](evidence/source-counts.json), [독립 감사](evidence/audit/source-count-audit.md)를 함께 본다.

"""
    body += (ROOT / "result-analysis.md").read_text()
    (ROOT / "RESULT.md").write_text(header + body)
    print(json.dumps({k: metrics[k] for k in ["cases", "routes", "counts", "searches", "body_attempts", "discordant_pairs", "questions_with_asker_action_in_30d"]}, ensure_ascii=False))

if __name__ == "__main__":
    main()
