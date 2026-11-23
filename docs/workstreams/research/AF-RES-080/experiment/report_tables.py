"""Render the three leading result tables from the result ledgers."""
import argparse
import csv
import json
from pathlib import Path

from score import SEATS, index, read_jsonl

ANSWER_LABELS = {
    "proposal-only": "제안",
    "author-changed-context": "작성자 입력 변경",
    "different-participant": "다른 참여자의 우회",
    "redirect-only": "질문 경로 안내",
    "author-partial": "작성자 부분 실행",
    "author-reported": "작성자 조작 성공 보고",
    "author-alternative": "작성자 대체 사용",
    "author-tentative": "작성자 잠정 보고",
    "author-input-changed": "작성자 변경 입력 성공",
    "vacant": "공석",
}
CELL_LABELS = {"NR": "좁음·참조", "BR": "넓음·참조", "NE": "좁음·정확", "BE": "넓음·정확"}


def escape(value):
    return str(value or "—").replace("|", "\\|").replace("\n", " ").strip()


def table(headers, rows):
    all_rows = [headers, ["---"] * len(headers), *rows]
    assert all(len(row) == len(headers) for row in all_rows)
    return "".join("| " + " | ".join(map(escape, row)) + " |\n" for row in all_rows)


def recruitment(requests, gold):
    for seat in SEATS:
        r, answer = requests[seat], gold[seat]
        if r["recruitment"] == "vacant":
            yield [seat, "교정 · 상한 100", "잠정 자리 공석", "—", "—", "—", "—"]
            continue
        family = "자연" if r["stratum"] == "natural" else "교정"
        frame = f"{family} · {r['ordinal']}/{60 if family == '자연' else 100}"
        opening = f"[#{r['issue_number']}]({r['issue_url']}) · `{r['original_sha256'][:10]}` · 첫판 미복원"
        if r.get("original_clue"):
            opening += " · 원 글 단서"
        editions = f"{r.get('question_version') or '미확인'} / {answer.get('author_success_exact_version') or answer.get('success_exact_version') or '미확인'}"
        outcome = f"[{ANSWER_LABELS[answer['status']]}]({answer['answer_url']})"
        yield [seat, frame, opening, r["C1"], r["C2"], editions, outcome]


def judgments(rows):
    for r in rows:
        edition = r["version"] or "미확인"
        if r["commit"]:
            edition += f" · [`{r['commit'][:8]}`](https://github.com/{r['repo']}/tree/{r['commit']})"
        feature = r["candidate_ids"].replace("|", ", ")
        if r["related_menu_ids"]:
            related = r["related_menu_ids"].replace("|", ", ")
            feature += (" · " if feature else "") + "메뉴 " + related
        gold = r["acquired_gold_join"]
        if r["gold_function_ids"]:
            gold += " · " + r["gold_function_ids"].replace("|", ", ")
        evidence = [f"[{n}]({url})" for n, url in enumerate(r["evidence"].split(" | "), 1) if url]
        missing = r["missing"] + (" · " if r["missing"] and evidence else "") + " ".join(evidence)
        cell = f"{r['cell']} {CELL_LABELS[r['cell']]} · {r['catalog_id'] or '목록 결손'}"
        yield [r["seat_id"], cell, edition, feature, r["listed"], f"{r['status']} / {r['acquired_status']}",
               gold, r["scope_outside"], missing]


def summary_rows(stats):
    for label, key in (("엄격", "tables"), ("최초 확보본", "acquired_sensitivity")):
        for stratum, r in stats[key].items():
            planned, complete = r["planned_seats"], r["complete"]
            op = r["recovery_opportunity"]
            by_range = r["pairs"]["NR->BR"]
            span = f"참조 범위 확대 {by_range['recovered']}/{by_range['recovery_opportunity_denom']}"
            order = ["scope-only", "edition-only", "joint-only", "either-axis", "all-positive",
                     "no-recovery", "nonmonotone", "unjudged"]
            changes = ", ".join(str(r["patterns"][key]) for key in order)
            stratum_name = "자연" if stratum == "natural" else "교정"
            yield [f"{stratum_name} {label}", f"완전 {complete}/{planned} · 기회 {op}/{planned}",
                   span, f"짝 변화 {changes}", "동일판 예 없음", "최초판 및 정확판 증거 확보"]


def probe_rows(runs):
    positive = {seat: runs[f"{seat}-reference-positive"]["actual"] for seat in ("CC01","CC02","AC01","AC02")}
    boundary = {seat: runs[f"{seat}-reference-boundary"]["actual"] for seat in positive}
    cc1, cc2, ac1, ac2 = (positive[key] for key in positive)
    cb1, cb2, ab1, ab2 = (boundary[key] for key in boundary)
    evidence = {
        "CC01": (f"`-V` → `{cc1['selected_flag']['output'].strip()}` · {cc1['selected_flag']['exit_code']}",
                 f"이름 인수 등록 → {cb1['error']['type']} · 기본 플래그 exit {cc1['default_flag']['exit_code']}",
                 "성공 실행의 Click 버전과 -V의 stdout 확인"),
        "CC02": (f"사용자 콜백 → `{cc2['version_flag']['output'].strip()}` · {cc2['version_flag']['exit_code']}",
                 f"데코레이터를 params에 전달 → {cb2['version_flag']['error']['type']} · {cb2['version_flag']['exit_code']}",
                 "작성자 성공판과 전달한 실제 Parameter 유형 확인"),
        "AC01": (f"전용 훅 {ac1['documented_attrs_hook']['call_count']}회, Int/IntRange · slots=False의 둘째 키 {ac1['reported_unslotted']['range_lookup']['exception']}",
                 f"일반 slotted 훅 {ab1['original_slotted']['call_count']}회 · int 키는 {ab1['original_slotted']['int_lookup']['class']}",
                 "성공판, 두 키의 값, 원 클래스 조립 순서 확인"),
        "AC02": (f"주석 전용 type 동일 {ac2['reports_original_type']} · 원 객체 {ac2['original_after']}",
                 f"명시 대입 시 type은 {ab2['reported_type_kind']} · 원 객체 {ab2['original_after']}",
                 "정확 attrs와 Python 판에서 field.type 객체 동일성 확인"),
    }
    for seat, facts in evidence.items():
        ref = runs[f"{seat}-reference-positive"]["version"]
        attained, edge, next_check = facts
        yield [seat, f"참조 {ref} · CPython 3.12.14", attained, edge, "정확판 양성·경계 모두 미실행", next_check]


def render(root):
    requests = index(read_jsonl(root / "requests.jsonl"), "seat_id")
    gold = index(read_jsonl(root / "gold.jsonl"), "seat_id")
    with (root / "matches.csv").open(newline="", encoding="utf-8") as stream:
        matches = list(csv.DictReader(stream))
    stats = json.loads((root / "evidence/metrics.json").read_text(encoding="utf-8"))
    runs = index(read_jsonl(root / "runs.jsonl"), "id")
    lines1 = list(recruitment(requests, gold))
    lines2 = list(judgments(matches))
    lines3 = [*summary_rows(stats), *probe_rows(runs)]
    assert (len(lines1), len(lines2), len(lines3)) == (12, 48, 8)
    return (
        "# AF-RES-080 · 알려진 해결이 후보 목록에 들어 있는가\n\n"
        "## 표 1. 모집·봉인·성공 사슬\n\n"
        + table(["자리", "층·순번", "원 글·봉인", "C1", "C2", "질문판 / 성공판", "공개 답"], lines1)
        + "\n## 표 2. 범위×판 네 목록\n\n"
        + table(["자리", "셀·목록", "배포·commit", "기능 ID·메뉴", "등재", "공동 엄격 / 최초 확보", "공개 답 ID 조인", "범위 밖", "결손·근거"], lines2)
        + "\n## 표 3. 짝 변화와 실행 대조\n\n"
        + table(["층·실행 자리", "분모·실행판", "범위 변화·양성", "짝 변화·경계", "판별 차이", "다음 최소 확인"], lines3)
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = render(args.root)
    if args.check:
        path = args.root / "RESULT.md"
        saved = path.read_text(encoding="utf-8").split("## Q1.", 1)[0]
        assert result == saved, "First three tables do not match the result ledgers"
        print("RESULT tables match 12 recruitment rows, 48 cells, and 8 comparison/run rows")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
