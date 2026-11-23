"""Join sealed readings and expectations, and generate the three result tables."""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit

from display import display_rows
from judge import grade
from search import ARMS, MODES, read_jsonl, terms_request, tokens, write_csv

LABEL = {"direct": "직접", "partial": "부분", "transfer": "전이"}
OUTCOME = {"correct": "맞음", "false_adoption": "오채택", "refuted": "반박", "hold": "보류",
           "unread": "미판독", "no_display": "표시 없음", "rejection_conflict": "반박 불일치"}
ACTION = {"adopt": "직접 채택", "hold": "보류", "reject": "반박", "": "없음"}
CONDITION = {"yes": "확인", "no": "불일치", "conditional": "조건부", "unknown": "미확인", "": "—"}
STRATUM = {"natural": "자연", "calibration": "교정"}
NOTE = {
    "NP01": "원 폰트·같은 문자열·빌드별 RAQM/FreeType 미확인",
    "NP02": "T-07에서 고정 Linux 합성을 확인. 원 Windows 11·JP2 재현 미확인",
    "NP03": "원 TIFF의 EXIF 길이·파생 JPEG 태그 미확인",
    "ND01": "최초 master SHA·INSERT 검증 환경 미확인",
    "ND02": "T-08은 고정판 로컬 읽기. httpfs·CLI/Wasm 조건 미확인",
    "ND03": "원 R API·빌드에서 SQL NULLS LAST 연동 미확인",
    "CP01": "시험으로 두 조건 확인. 본 표시창의 API 호출 구간 누락",
    "CP02": "시험은 튜플 확인. 본 표시창에 호출·정확한 반환 형태 누락",
    "CP03": "T-03에서 잘린 결과 확인. 원본 보유 렌더러는 범위 밖",
    "CD01": "T-04에서 raw CAST 확인. 두 직접 후보의 본 표시창은 부분 근거",
    "CD02": "T-05에서 원표 재조회. 본 표시창이 EXCLUDE 예 직전에서 끝남",
    "CD03": "T-06에서 파일 재열기 확인. WHERE만 사용하면 두 행이 남음",
}


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def pair_key(row):
    return row["request_id"], row["candidate_id"]


def make_slots(root):
    qrels = {pair_key(r): r for r in read_csv(root / "qrels.csv")}
    case_strata = {r["id"]: r["stratum"] for r in read_jsonl(root / "requests.jsonl")}
    readings = {r["slot_id"]: r for r in read_jsonl(root / "evidence/individual-readings.jsonl")}
    slots = []
    for visible in display_rows(root):
        request, candidate = pair_key(visible)
        expectation = qrels[(request, candidate)]
        reading = readings.get(visible["slot_id"], {})
        if reading:
            assert reading["display_sha256"] == visible["display_sha256"]
        view = visible["view"]
        url = visible["url"]
        span = f"L{view['start']}-L{view['end']}" if view else ""
        slots.append({
            "slot_id": visible["slot_id"], "request_id": request, "stratum": case_strata[request],
            "arm": visible["arm"], "slot": visible["slot"], "candidate_id": candidate,
            "edition": visible["edition"], "rank_id": visible["rank_id"], "fetch_id": visible["fetch_id"],
            "opening_step": visible["opening_step"], "exposure": visible["exposure"],
            "display_sha256": visible["display_sha256"], "shown_url": url + ("#" + span if span else ""),
            "actual_arrival_url": visible["source_http_url"], "source_span": span,
            "source_lines": " ".join(str(n) for n in view["source_lines"]) if view else "",
            "card_shown": bool(visible["card_text"]), "c1": reading.get("c1", ""), "c2": reading.get("c2", ""),
            "environment": reading.get("environment", ""), "reading_id": reading.get("reading_id", ""),
            "observation_id": reading.get("observation_id", ""), "reader": reading.get("reader", ""),
            "read_utc": reading.get("read_utc", ""),
            "status": "read" if reading else "unread" if visible["exposure"] != "none" else "no_display",
            "qrel_id": expectation["pair_id"], "full_candidate_judgment": expectation["judgment"],
            "expected_output": expectation["output_expectation"],
            "observed_output": reading.get("action", ""), "observed_finding": reading.get("window_finding", ""),
            "grade": grade(visible["exposure"], reading, expectation["judgment"]),
        })
    return slots


def metric_rows(root, slots, ranks, qrels, requests):
    by_req = {r["id"]: r["stratum"] for r in requests}
    score = {}
    kinds = list(LABEL)
    for stratum in STRATUM:
        score[stratum] = {}
        available = Counter(r["judgment"] for r in qrels if r["stratum"] == stratum)
        for arm in ARMS:
            relevant = [s for s in slots if s["arm"] == arm and s["stratum"] == stratum]
            found = Counter(s["full_candidate_judgment"] for s in relevant)
            score[stratum][arm] = {
                "pool": {key: available[key] for key in kinds},
                "top3": {key: found[key] for key in kinds},
                "requests_with_candidate": {
                    key: len({s["request_id"] for s in relevant if s["full_candidate_judgment"] == key})
                    for key in kinds
                },
                "slots": len(relevant), "outcomes": dict(Counter(s["grade"] for s in relevant)),
            }
    attempts = [e for e in read_jsonl(root / "fetches.jsonl") if e["cache"] == "cold"]
    changed = {str(n): sum(e["step"] == n and e["before_top3"] != e["after_top3"] for e in attempts)
               for n in (1, 2, 3)}
    first_changed = {str(n): sum(e["step"] == n and e["before_top3"][0] != e["after_top3"][0]
                                 for e in attempts) for n in (1, 2, 3)}
    first_l = {r["request_id"]: [r["candidate_id"], int(r["initial_score"]), int(r["initial_tie_n"])]
               for r in ranks if (r["cache"], r["arm"], r["initial_rank"]) == ("cold", "L", "1")}
    changed_by_stratum = {}
    for stratum in STRATUM:
        changed_by_stratum[stratum] = {str(stage): sum(
            e["step"] == stage and e["before_top3"] != e["after_top3"] and by_req[e["request"]] == stratum
            for e in attempts) for stage in (1, 2, 3)}
    return {
        "qrel_total": len(qrels), "qrel_breakdown": {
            stratum: dict(Counter(r["judgment"] for r in qrels if r["stratum"] == stratum)) for stratum in STRATUM},
        "rank_total": len(ranks), "main_slot_total": len(slots),
        "slot_grades": dict(Counter(r["grade"] for r in slots)),
        "original_windows": sum(s["exposure"] == "original" for s in slots),
        "individual_readings": sum(bool(s["reading_id"]) for s in slots),
        "distinct_observations": len({x["observation_id"] for x in slots if x["observation_id"]}),
        "by_stratum_and_arm": score,
        "top3_order_changes_by_open": changed, "first_slot_changes_by_open": first_changed,
        "order_changes_by_stratum": changed_by_stratum, "first_L": first_l,
        "smallest_live_response_b": min(e["received_body_b"] for e in attempts),
        "largest_live_response_b": max(e["received_body_b"] for e in attempts),
    }


def lexical_notes(root, ranks):
    requests = {r["id"]: r for r in read_jsonl(root / "requests.jsonl")}
    docs = {x["candidate_id"]: x["url"] for x in read_jsonl(root / "corpus.jsonl")}
    cards = {c["candidate_id"]: c for c in read_jsonl(root / "cards.jsonl")}
    examples = [("NP03", "X03"), ("CD01", "D01"), ("CD01", "D03"), ("CP02", "P04"),
                ("CP03", "X01"), ("ND02", "D01")]
    out = []
    for rid, cid in examples:
        query = terms_request(requests[rid])
        path = tokens(urlsplit(docs[cid]).path.split("/", 5)[-1])
        card = cards[cid]
        title = tokens(card["name"])
        s_first = tokens(card["s"])
        e_text = tokens(card["e"])
        out.append({"request_id": rid, "candidate_id": cid, "url_matches": sorted(query & path),
                    "new_title_matches": sorted(query & (title - path)),
                    "new_first_sentence_matches": sorted(query & (s_first - (path | title))),
                    "new_edited_text_matches": sorted(query & (e_text - (path | title))),
                    "rows": [{k: r[k] for k in ("rank_id", "initial_score", "initial_rank", "initial_tie_n", "final_slot")}
                             for r in ranks if r["cache"] == "cold" and pair_key(r) == (rid, cid)]})
    return out


def clean(s):
    return str(s).replace("|", "\\|").replace("\n", " ").replace(";", " · ")


def table(headings, rows):
    all_rows = [headings, ["---"] * len(headings), *rows]
    assert all(len(row) == len(headings) for row in all_rows)
    return "\n".join("| " + " | ".join(clean(s) for s in row) + " |" for row in all_rows)


def render(root, slots, ranks, qrels, requests, metrics):
    by_request = defaultdict(list)
    for row in qrels:
        by_request[row["request_id"]].append(row)
    by_route = defaultdict(list)
    for row in slots:
        by_route[(row["request_id"], row["arm"])].append(row)
    first_table = []
    for req in requests:
        rid = req["id"]
        pool = by_request[rid]
        by_candidate = {s["candidate_id"]: s for s in pool}
        counts = Counter(r["judgment"] for r in pool)
        lines = []
        for arm in ARMS:
            shown = by_route[(rid, arm)]
            first = {key: next((s["slot"] for s in shown if s["full_candidate_judgment"] == key), "—")
                     for key in LABEL}
            first_text = "/".join(str(first[key]) for key in LABEL)
            lines.append(f"{arm} " + " › ".join(s["candidate_id"] for s in shown) + f" · {first_text}")
        input_link = f"[{req['source_id']}]({req['source_url']})"
        chosen = [r for r in pool if r["judgment"] in LABEL]
        chosen.sort(key=lambda row: list(LABEL).index(row["judgment"]))
        paths = " · ".join(f"[{r['candidate_id']} {r['source_lines'].split(';')[0]}]({r['original_anchors'].split()[0]})"
                           for r in chosen[:3])
        first_table.append([
            f"{STRATUM[req['stratum']]} · {rid}",
            f"{req['part']} · {req['purpose']}<br>C1 {req['c1']}<br>C2 {req['c2']}<br>환경 {req['environment']}",
            "/".join(str(counts[key]) for key in LABEL),
            "<br>".join(lines), f"{input_link} · {paths}" if paths else input_link, NOTE[rid],
        ])

    second_table = []
    for number, s in enumerate(slots, 2):
        checks = "/".join(CONDITION[s[k]] for k in ("c1", "c2", "environment"))
        source_link = f"[{s['source_span'] or '주소'}]({s['shown_url']})"
        reading_link = f"[{s['reading_id']}](slots.csv#L{number})" if s["reading_id"] else "—"
        state = "원문 판독" if s["status"] == "read" else OUTCOME[s["grade"]]
        first = f"{s['request_id']} · {s['arm']} · {s['slot']}"
        candidate = f"{s['candidate_id']} · {s['edition']}"
        output = f"{ACTION[s['expected_output']]} / {ACTION[s['observed_output']]}"
        second_table.append([first, candidate, source_link, checks, f"{reading_link} · {state}",
                             output, OUTCOME[s["grade"]]])

    cost_summary = [r for r in read_csv(root / "costs.csv") if r["phase"] == "summary_sum"]
    third_table = []
    for r in cost_summary:
        arm, layer, mode, n = r["arm"], r["stratum"], r["cache"], int(r["unique_requests"])
        stat = metrics["by_stratum_and_arm"][layer][arm]
        denom = stat["pool"]["direct"]
        recovered = f"{stat['top3']['direct']}/{denom}" if denom else "분모 0 · 산출 불가"
        joint = stat["outcomes"].get("correct", 0)
        storage = f"{int(r['representation_file_b']):,} · 원문 최대 {int(r['max_raw_cache_b']):,}"
        cost = (f"HTTP {int(r['http_calls'])/n:g} · 논리 {int(r['attempts'])/n:g}"
                f"<br>{int(r['network_body_b'])/n:,.1f} B · {int(r['display_words'])/n:,.1f}단어"
                f" · 표시 {int(r['display_b'])/n:,.1f} B")
        state = "빈 캐시" if mode == "cold" else "즉시 반복"
        caveat = "요청마다 빈 원문 캐시" if mode == "cold" else "같은 요청과 원문 캐시 재사용"
        third_table.append([f"{arm} · {state} · {STRATUM[layer]}", n,
                            f"{r['build_calls']} · {int(r['build_http_b']):,} B", cost, storage,
                            f"{recovered} · 공동 {joint}/{stat['slots']}", caveat])
    return "# AF-RES-076 결과\n\n" + "\n\n".join([
        "## 표 1. 요구별 적격과 반환 후보\n\n" + table(
            ["층·요구 ID", "부분·목적·조건·환경", "직접/부분/전이 적격 분모", "L/S/E 상위 3과 첫 적격",
             "확인한 원문 주소·절", "미확인"], first_table),
        "## 표 2. 반환 슬롯의 표시 근거\n\n" + table(
            ["요구·방식·슬롯", "후보·판", "실제 표시창 주소/행", "C1·C2·환경", "개별 판독 ID·상태",
             "기대 출력/관찰 출력", "맞음·오채택·보류·미판독"], second_table),
        "## 표 3. 구축과 요청 비용\n\n" + table(
            ["방식·캐시·모집층", "고유 요청 수", "구축 원문 수·바이트", "요청당 호출·전송 B·읽힌 단어",
             "실제 저장 B", "직접 적격 회수와 공동 확인", "손익 가정·미확인"], third_table),
    ]) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    root, out = args.root, args.output
    out.mkdir(parents=True, exist_ok=True)
    qrels = read_csv(root / "qrels.csv")
    ranks = read_csv(root / "ranks.csv")
    requests = read_jsonl(root / "requests.jsonl")
    slots = make_slots(root)
    metrics = metric_rows(root, slots, ranks, qrels, requests)
    write_csv(out / "slots.csv", slots)
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n")
    (out / "lexical-explanations.json").write_text(
        json.dumps(lexical_notes(root, ranks), ensure_ascii=False, indent=2) + "\n"
    )
    (out / "tables.md").write_text(render(root, slots, ranks, qrels, requests, metrics))


if __name__ == "__main__":
    main()
