"""Report type-level outcomes using an answer once in each reason type."""

import json
from collections import Counter, defaultdict
from datetime import date
from statistics import median

from collect import ROOT, rows
from extract import TYPES
from simulate import AS_OF

PRIORITY = {"성립": 0, "판단 불가": 1, "약화": 2, "무너짐": 3}
REPRESENTATIVES = {
    "기능 지원": "T001.A004 Mattermost / T051.A001 TanStack Table",
    "가격": "T013.A001 Microsoft 365 / T021.A001 Syncfusion",
    "라이선스": "T009.A001 Directus / T017.A003 CXXGraph",
    "플랫폼": "T020.A001 Dcoder / T015.A002 ScreenToGif",
    "호스팅 방식": "T003.A002 Bitwarden / T058.A021 Soft Serve",
    "관리 상태": "T004.A001 BiblioteQ / T024.A001 Args",
    "성능": "T043.A013 Mozilla STT/TTS / T060.A001 CLOVA Speech",
    "기타 검증 가능": "T031.A009 LessWrong / T032.A009 Lobsters",
}


def type_totals(reasons):
    groups = defaultdict(lambda: defaultdict(list))
    for row in reasons:
        if row["reason_type"] != "이유 없음":
            groups[row["reason_type"]][row["answer_ref"]].append(row)
    result = []
    for key in TYPES.values():
        if key == "이유 없음":
            continue
        groups_by_answer = groups[key]
        flattened = [r for group in groups_by_answer.values() for r in group]
        worst = Counter(max((r["now_verdict"] for r in group), key=PRIORITY.__getitem__)
                        for group in groups_by_answer.values())
        anchors = [min(r["answer_date"] for r in group if r["answer_date"])
                   for group in groups_by_answer.values() if any(r["answer_date"] for r in group)]
        age = median((AS_OF - date.fromisoformat(d)).days / 365.2425 for d in anchors) if anchors else None
        result.append({"reason_type": key, "answers": len(groups_by_answer),
                       "now": {name: worst[name] for name in PRIORITY},
                       "initially_false": sum(any(x["then_verdict"] == "처음부터 틀림" for x in group)
                                              for group in groups_by_answer.values()),
                       "dated_answers": len(anchors), "median_elapsed_years": age,
                       "atomic_reasons": len(flattened),
                       "atomic_verdicts": dict(Counter(r["now_verdict"] for r in flattened)),
                       "representative": REPRESENTATIVES[key]})
    return result


def print_markdown(table):
    print("| 이유 유형 | 답 수(분모) | 지금 성립 | 약화 | 무너짐 | 판단 불가 | 처음부터 틀림 | 중앙 경과 연수 | 대표 사례(스레드 ID·후보) | 미확인 |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |")
    for row in table:
        n, dt = row["answers"], row["dated_answers"]
        age = row["median_elapsed_years"]
        age_text = "미확인(원 답 시각 필요)" if age is None else f"{age:.2f}년 (n={dt})"
        cells = (row["reason_type"], n, *(row["now"][k] for k in ("성립", "약화", "무너짐", "판단 불가")),
                 row["initially_false"], age_text, row["representative"],
                 f"미확인(현재 답 {row['now']['판단 불가']}개 공식 대조, 날짜 없는 답 {n - dt}개 원문 시각)")
        print("| " + " | ".join(map(str, cells)) + " |")


def main():
    table = type_totals(rows(ROOT / "REASONS.jsonl"))
    (ROOT / "results" / "reason-types.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n")
    print_markdown(table)


if __name__ == "__main__":
    main()
