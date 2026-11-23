#!/usr/bin/env python3
"""Validate AF-RES-053 ledgers; passing does not mean missing research is complete."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
REL = ROOT.relative_to(REPO).as_posix()
SEAL = "9b13473a76a381fe27d775524aa65416ec28f591"
SLOTS = ["V01", "V02", "V03", "L01", "L02", "L03"]
IDS = {f"{slot}-{view}" for slot in SLOTS for view in "NID"}
FIELDS = ["source_id", "work_id", "자료종류", "원본_URL", "최종_URL", "발행자",
          "확인_UTC", "판_또는_SHA", "쪽_절_행_셀", "관련_Q와_사례_ID", "확인한_내용",
          "확인범위와_한계", "지지_또는_반증", "직접열람_상태", "중복_계보"]


def read_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["outcomes", "final"], default="final")
    parser.add_argument("--output", default="evidence/validation.json")
    args = parser.parse_args()
    checks = []

    def check(name, passed, observed):
        checks.append({"check": name, "pass": bool(passed), "observed": observed})

    cards, predictions, frame = (read_csv(n) for n in ["cards.csv", "predictions.csv", "frame.csv"])
    outcomes = read_csv("outcomes.csv")
    for name, rows, key in [("cards", cards, "card_id"), ("predictions", predictions, "prediction_id"),
                            ("outcomes", outcomes, "outcome_id")]:
        values = [r[key] for r in rows]
        check(name + "_18_ids", len(values) == 18 and set(values) == IDS, values)
    candidates = [r for r in frame if r["issue_number"]]
    check("frame_58_available_candidates", len(candidates) == 58,
          {repo: sum(r["repository"] == repo for r in candidates) for repo in ["vega/vega-lite", "libass/libass"]})
    selected = [r for r in candidates if r["selected_slot"]]
    check("five_filled_one_empty", len(selected) == 5 and {r["selected_slot"] for r in selected} == set(SLOTS[:-1]),
          [r["selected_slot"] for r in selected])
    by_card = {r["card_id"]: r for r in cards}
    budgets = {}
    for slot in SLOTS[:-1]:
        i, d = by_card[slot + "-I"], by_card[slot + "-D"]
        pair = [(int(r["addition_words"]), int(r["addition_figures"])) for r in [i, d]]
        budgets[slot] = pair
        check(slot + "_matched_addition_budget", pair[0] == pair[1] and pair[0][0] <= 200 and pair[0][1] <= 1, pair)
        check(slot + "_common_N", all(by_card[slot + "-" + v]["common_N_window_sha256"] == i["common_N_window_sha256"] for v in "NID"), i["common_N_window_sha256"])
    frozen = json.loads((ROOT / "evidence/pre-outcome-freeze.json").read_text())
    for name in frozen["files_sha256"]:
        remote = subprocess.check_output(["git", "show", f"{SEAL}:{REL}/{name}"], cwd=REPO)
        current = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        check("seal_unchanged:" + name, current == remote, hashlib.sha256(remote).hexdigest())
    source_rows = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text().splitlines() if line.strip()]
    source_ids = [r["source_id"] for r in source_rows]
    check("unique_source_ids", len(source_ids) == len(set(source_ids)), len(source_ids))
    missing = [{"source_id": r.get("source_id"), "missing": [k for k in FIELDS if k not in r]} for r in source_rows if any(k not in r for k in FIELDS)]
    check("source_fields", not missing, missing)
    counts = json.loads((ROOT / "evidence/source-counts.json").read_text())
    check("source_count_rows", counts["total_read_rows"] == len(source_rows), len(source_rows))
    registry = counts["works"]
    check("source_count_registry", set(r["work_id"] for r in source_rows) == {w["work_id"] for w in registry}, len(registry))
    assignments = counts["allocation"]
    assigned = [w for bucket in assignments.values() for w in bucket["work_ids"]]
    check("allocation_disjoint", len(assigned) == len(set(assigned)), assigned)
    if args.phase == "final":
        text = (ROOT / "RESULT.md").read_text()
        lines = text.splitlines()
        h1 = "| 요구 ID | 목적·제품판 | 보기 N·I·D | 읽은 원문 주소·절 | 두 조작 | 정상·경계 사전 예측 | 후속 실제 출력·주소 | 일치·충돌·미확인 |"
        h2 = "| 요구 ID | API만으로 판정한 내용 | 같은 분야 예제가 더한 내용 | 타 분야 원전이 더한 내용 | 같은 예산에서 뒤집힌 조작 | 적용이 깨지는 조건 | 설계자에게 줄 링크·용도 | 미확인 |"
        check("RESULT_starts_table1", bool(lines) and lines[0] == h1, lines[:1])
        for header, expected in [(h1, 18), (h2, 6)]:
            if header not in lines:
                check("required_table", False, header)
                continue
            start = lines.index(header) + 2
            body = []
            for line in lines[start:]:
                if not line.startswith("|"):
                    break
                body.append(line)
            check("table_rows_" + str(expected), len(body) == expected, {"line": start + 1, "rows": len(body)})
        for q in range(1, 8):
            check("RESULT_Q" + str(q), f"## Q{q}." in text, f"Q{q}")
        review = (ROOT / "SELF_CHECK.md").read_text()
        for q in range(1, 8):
            check("SELF_CHECK_Q" + str(q), f"| Q{q} |" in review, f"Q{q}")
        weakness_header = "| 불일치·약점 | 영향받는 주장 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀔 조건 |"
        tail = text.strip().split(weakness_header)[-1].strip().splitlines()
        check("three_weaknesses_at_end", weakness_header in text and len(tail) == 4 and all(x.startswith("|") for x in tail), len(tail))
        acceptance = json.loads((ROOT / "evidence/acceptance-evidence.json").read_text())
        check("honest_partial_status", acceptance["overall_status"] == "부분 인계" and acceptance["fully_satisfied"] is False, acceptance["overall_status"])
    report = {"checked_UTC": datetime.now(timezone.utc).isoformat(), "phase": args.phase,
              "prediction_seal": SEAL, "checks": checks, "passed": all(c["pass"] for c in checks),
              "research_complete": False,
              "meaning": "원장·봉인·형식 일관성 검사. 표본/역사판/후속원전 결손을 충족으로 바꾸지 않는다."}
    target = ROOT / args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": report["passed"], "checks": len(checks), "failed": [c for c in checks if not c["pass"]], "research_complete": False, "report": str(target)}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
