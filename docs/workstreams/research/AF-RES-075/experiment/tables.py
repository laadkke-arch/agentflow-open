"""Build the three RESULT tables from their committed ledgers."""
import argparse
from pathlib import Path

from audit import aggregate, csv_rows, json_lines
from registry import ROOT

CLAIM_LABEL = {"exists": "E", "unique": "U", "top": "R"}
STATE_LABEL = {"retained": "보존", "lost": "소실"}
GRADE_LABEL = {"correct": "정답", "wrong": "오답", "defer": "보류"}
METHOD_LABEL = {
    "one_verified_clause": "원절", "historical_archive": "옛 원본", "inventory_keys": "B 키",
    "local_full_registry": "C 전체", "current_route": "현재 원본",
}


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        assert len(row) == len(headers) and all("|" not in cell and "\n" not in cell for cell in row)
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def value_str(value, truncate=False):
    if type(value) is bool:
        return "참" if value else "거짓"
    if not value:
        return "∅"
    if truncate and len(value) > 5:
        return f"{len(value)}개"
    return ", ".join(value)


def citation(pair, phase, row):
    path = pair[f"{phase}_url"]
    if pair["kind"] == "injected" and phase == "after":
        path = pair[f"{phase}_path"]
    if row is not None:
        return f"[{row['id']} L{row['line']}]({path}#L{row['line']})"
    return f"[전체 표]({path})"


def pairs_table(pairs, truth):
    headers = ("쌍 ID·자연/주입", "목록 범위·전후 판 URL", "요청·주장 유형",
               "전후 적격 수·공동 1위", "바뀐 근거 절", "독립 정답", "미확인")
    rows = []
    for number, pair in enumerate(pairs, 2):
        if pair["kind"] == "supplemental":
            continue
        key = pair["pair_id"]
        old_pos, old = truth[(key, "before")]
        new_pos, new = truth[(key, "after")]
        legacy = {row["id"]: row for row in old["citations"]}
        current = {row["id"]: row for row in new["citations"]}
        representative_old = legacy.get(old["top"][0]) if old["top"] else None
        representative_new = current.get(new["top"][0]) if new["top"] else None
        removed, added = sorted(legacy.keys() - current.keys()), sorted(current.keys() - legacy.keys())
        changed = sorted(row_id for row_id in legacy.keys() & current.keys()
                         if legacy[row_id]["clause_sha256"] != current[row_id]["clause_sha256"])
        moved = sorted(row_id for row_id in legacy.keys() & current.keys()
                       if legacy[row_id]["line"] != current[row_id]["line"])
        delta = []
        for named, ids, phase, citations in (("추가", added, "after", current),
                                             ("제거", removed, "before", legacy),
                                             ("원절 변경", changed, "after", current)):
            if ids:
                delta.append(named + " " + ", ".join(citation(pair, phase, citations[id_]) for id_ in ids))
        if moved:
            delta.append(f"공통 적격 중 줄 위치 변경 {len(moved)}")
        if not delta:
            delta.append("적격 원절 유지")
        if pair["mutation"] == "irrelevant_edit":
            delta.append("질의 밖 행 수정")
        tag = "자연" if pair["kind"] == "natural" else "주입"
        rank = value_str(old["top"])
        if old["top"] != new["top"]:
            rank += " → " + value_str(new["top"])
        else:
            rank += " · 양판"
        after_link = pair["after_url"] if tag == "자연" else pair["after_path"]
        summary = " · ".join(
            f"{CLAIM_LABEL[claim]} {value_str(old[claim])}→{value_str(new[claim])}"
            for claim in ("exists", "unique")
        )
        rows.append((
            f"[{key}](pairs.csv#L{number}) · {tag}",
            f"{pair['domain']} [{pair['before_edition']}]({pair['before_url']}) → "
            f"[{pair['after_edition'] if tag == '자연' else '합성'}]({after_link})",
            f"`{pair['query']}` · E/U/R", f"{len(legacy)}→{len(current)} · {rank}",
            " · ".join(delta) + " · 대표 " + citation(pair, "before", representative_old)
            + " → " + citation(pair, "after", representative_new),
            f"{summary} · R [전](evidence/truth.jsonl#L{old_pos})/[후](evidence/truth.jsonl#L{new_pos})",
            "실사용 분류" if pair["domain"] == "PG" else "실제 위치·오프셋",
        ))
    return table(headers, rows)


def one_outcome(result):
    if result["status"] == "deferred":
        return "보류"
    return value_str(result["value"], truncate=True) + " · " + METHOD_LABEL[result["method"]]


def decisions_table(pairs, runs, grades):
    headers = ("쌍·주장·보관안", "원본 보존/소실", "옛 문구 표시", "옛 주장 재계산",
               "현재 주장 재판정", "사용한 증거 주소/행", "정답·오답·보류")
    rows = []
    for number, record in enumerate(runs, 1):
        key = record["pair_id"]
        packet, decision = record["input"], record["decision"]
        grade = grades[record["run_id"]]
        shown = decision["display"]
        if len(shown) > 105:
            shown = f"[저장한 전체 문구](runs.jsonl#L{number})"
        addresses = []
        for phase, stage in (("before", "historical"), ("after", "current")):
            evidence = decision[stage]["evidence"]
            if evidence:
                addresses.append(citation(pairs[key], phase, evidence["witness"]))
        if decision["historical"]["method"] in ("inventory_keys", "local_full_registry"):
            addresses.append(f"[저장](evidence/{packet['projection_path']})")
        if decision["historical"]["status"] == "deferred":
            addresses.insert(0, f"[옛 접근 영수증](runs.jsonl#L{number})")
        rows.append((
            f"[{key}·{CLAIM_LABEL[packet['claim']]}·{packet['view']}](runs.jsonl#L{number})",
            STATE_LABEL[record["state"]], shown, one_outcome(decision["historical"]),
            one_outcome(decision["current"]), " · ".join(addresses),
            "/".join(GRADE_LABEL[grade[stage]] for stage in ("display", "historical", "current")),
        ))
    return table(headers, rows)


def sufficiency(row):
    if row["view"] == "B":
        return "같은 판의 전체 판별 키·범위 영수증·규칙"
    if row["view"] == "C":
        return "같은 판의 전체 바이트·규칙"
    if row["state"] == "retained":
        return "검증된 원절 또는 보존 목록·당시 규칙" if row["claim"] == "exists" else "보존 목록·당시 규칙"
    return "원절은 긍정 증인" if row["claim"] == "exists" else "모집·판별 규칙 필요"


def summary_table(scores, costs):
    headers = ("주장 유형·보관안·조건", "고유 쌍 분모", "맞음·틀림·보류",
               "구축 B·재취득 수·읽은 B", "충분한 조건", "미확인")
    rows = []
    for item in aggregate(scores, costs):
        m = item["measures"]
        counts = " · ".join(
            label + " " + "/".join(str(item[stage][status]) for status in ("correct", "wrong", "defer"))
            for label, stage in (("옛", "historical"), ("현", "current"), ("표시", "display"))
        )
        rows.append((
            f"{CLAIM_LABEL[item['claim']]}·{item['view']}·{STATE_LABEL[item['state']]}",
            str(item["denominator"]), counts,
            f"{m['build_bytes']:,}B · 옛 {m['historical_initial_requests']}+{m['historical_post_defer_requests']}"
            f"/현 {m['current_requests']}회 · 원본 {m['local_read_bytes']:,}B",
            sufficiency(item), "운영 HTTP·캐시",
        ))
    return table(headers, rows)


INTRO = """# AF-RES-075 · 단일 증인과 전체 후보에 대한 주장

단위는 **고유 전후쌍 16**이다. PG·TZ 각 8쌍은 자연 4·주입 4다. E는 적격 후보 존재, U는 정확히 하나, R은 명시 점수의 공동 1위 집합이다. 표 1은 쌍 16개, 표 2는 같은 쌍의 **16×3×3×2 = 288자리**, 표 3은 각 비교의 고유 쌍 16개다. SWAP01·손실·네이티브와 외부 사례는 주 분모 밖의 대조다. 표 2의 등급 순서는 표시·옛·현이고 표 3의 각 세 수는 정답·오답·보류다. 보관안 A는 대표 원절, B는 전체 판별 키, C는 전체 목록을 보존한다. 각 보기에는 같은 당시 표시 문자열도 들어 있다. 표 3의 재취득은 옛 초기+기권 뒤 진단/현재 요청이며 읽은 B는 로컬 서비스 원본의 본문 바이트다. [사전 범위](SCOPE.md) · [실행](runs.jsonl) · [판정](scores.csv) · [비용](costs.csv)
"""


def render(root):
    pairs, _ = csv_rows(root / "pairs.csv")
    runs = json_lines(root / "runs.jsonl")
    scores, _ = csv_rows(root / "scores.csv")
    costs, _ = csv_rows(root / "costs.csv")
    truth = {(row["pair_id"], row["phase"]): (index, row) for index, row in
             enumerate(json_lines(root / "evidence/truth.jsonl"), 1)}
    return "\n\n".join((
        INTRO.strip(), "## 표 1 · 전후 후보와 인용", pairs_table(pairs, truth),
        "## 표 2 · 보기별 단일 판독",
        decisions_table({row["pair_id"]: row for row in pairs}, runs,
                        {row["run_id"]: row for row in scores}),
        "## 표 3 · 정오·보류와 비용", summary_table(scores, costs),
    )) + "\n"


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--root", type=Path, default=ROOT)
    args = cli.parse_args()
    print(render(args.root), end="")
