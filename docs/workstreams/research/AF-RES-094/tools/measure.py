"""Code the preserved observations, derive the A/B pairs, and verify saved tables."""
from collections import Counter
import csv
from datetime import datetime
from io import StringIO
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((root / name).read_text(encoding="utf-8"))


def jsonl(name):
    return [json.loads(line) for line in (root / name).read_text(encoding="utf-8").splitlines()]


def dump(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def confirmed(doc):
    return bool(doc and doc["status"] and 200 <= doc["status"] < 300
                and doc["analysis"] and doc["analysis"]["kind"] != "error_document")


def timestamp_bin(iso):
    minute = int(iso[14:16]) // 10 * 10
    return iso[:14] + f"{minute:02}:00Z"


targets = {row["purpose_id"]: row for row in load("freeze.json")["targets"]}
comparisons = load("evidence/payload-audit.json")["wrappers"]
matches = {r["receipt_id"]: r for r in comparisons if r["equal_after_removing_final_lfs_from_raw"]}
original = load("evidence/main/routes-observed.json")
sources = jsonl("sources.jsonl")


def assess(row):
    first, *rest = row["docs"]
    next_doc = rest[0] if rest else None
    purpose = row["purpose_id"]
    target = targets[purpose]
    analysis = first["analysis"] or {}
    reached = confirmed(first)
    body = "미확인" if reached else "접근 실패"
    summary = "입구에서 지정 본문 회수 미실시 (프록시 연결 실패)"
    if reached and purpose == "P1-next":
        has_body = (first["id"] in matches and analysis["minmal_settings"].get("master") == target["add_url"]
                    and analysis["commit"] == "7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74"
                    and (row["planned_method"] == "http" or first["dom"]["code_uri_visible"]))
        if has_body:
            body, summary = "확인", "고정 7.0.1 Minmal의 master 문자열 및 INI"
    elif reached and purpose == "R1-next":
        has_body = (first["id"] in matches and analysis["archive_version_marker"] == "1.1.12"
                    and analysis["usage_has_archive_read"] and analysis["examples_has_system_file"]
                    and (row["planned_method"] == "http" or first["dom"]["code_uri_visible"]))
        if has_body:
            body, summary = "확인", "고정 1.1.12 source의 Usage·Examples와 system.file 원URI"

    needed = target["requires_followup"]
    payload = "해당 없음" if not needed else "미확인"
    observed_relation = "지정판 미확인" if not needed else "후속판 관계 미확인"
    next_summary = ""
    historical = "해당 없음"
    if next_doc and not confirmed(next_doc):
        payload, next_summary = "접근 실패", "지정 후속 주소의 payload 미회수"
    elif next_doc and purpose == "P1-next" and "Python Package Index" in next_doc["analysis"]["service_markers"]:
        payload, next_summary = "확인", "현재 PyPI 홈페이지 본문"
        observed_relation = "현재 외부 서비스 확인"
        historical = "미확인 · 7.0.1 당시 서비스 귀속"
    elif needed and not next_doc:
        next_summary = "후속 요청 없음 · 첫 실패와 봉인 주소 유무 적용"
    if purpose == "R1-next":
        observed_relation = "미확인 · archive 문서를 생성한 R판"
    if purpose == "R2-next":
        observed_relation = "미확인 · 2.3.1 예제와 실제 payload 연결"
    if purpose == "P3-next":
        observed_relation = "미확인 · 1.x 루트 판독 실패"
    result = "접근 실패" if "접근 실패" in (body, payload) else "미확인"
    if body == "확인" and payload == "확인" and observed_relation == "현재 외부 서비스 확인":
        result = "엄격 충족"
    return dict(body=body, body_detail=summary, payload=payload, payload_detail=next_summary,
                required_relation=target["relation"], observed_relation=observed_relation, strict_outcome=result,
                strict_historical_service=historical)


def enrich(row):
    route = row["route_id"]
    assert not row.get("instrumentation_error"), route
    docs = []
    for ordinal, doc in enumerate(row["docs"], 1):
        path = "evidence/main/" + doc["id"] + ".json"
        assert load(path) == doc, path
        if doc["method"] == "browser":
            assert doc["screenshot"] and (root / "evidence/main" / doc["screenshot"]).is_file(), route
        docs.append({**doc, "document_number": ordinal, "view_cost": 1,
                     "access_failure": not confirmed(doc), "receipt": path,
                     "screenshot": "evidence/main/" + doc["screenshot"] if doc.get("screenshot") else None})
    assert 1 <= len(docs) <= 2 and docs[0]["asked_url"] == targets[row["purpose_id"]]["first_url"], route
    assert all(doc["method"] == row["planned_method"] for doc in docs)
    return {**row, "docs": docs, "document_views": len(docs), "start_10min_bin": timestamp_bin(docs[0]["started_utc"]),
            "provenance": "실측 · Chromium/GET 2026-11-23", "verdict": assess(row)}


traversals = [enrich(row) for row in original]
assert len(traversals) == 24 and len({r["route_id"] for r in traversals}) == 24
pairs = []
for purpose, target in targets.items():
    group = [r for r in traversals if r["purpose_id"] == purpose]
    same_window = len({r["start_10min_bin"] for r in group}) == 1
    expected = target["card_order"]
    for method in ("browser", "http"):
        selected = [row for row in group if row["planned_method"] == method]
        assert [row["card"] for row in selected] == expected, (purpose, method)
        assert sorted(row["docs"][0]["started_utc"] for row in selected) == [row["docs"][0]["started_utc"] for row in selected]
        a, b = sorted(selected, key=lambda row: row["card"])
        a2 = a["docs"][1]["asked_url"] if len(a["docs"]) == 2 else ""
        b2 = b["docs"][1]["asked_url"] if len(b["docs"]) == 2 else ""
        actual = "different" if a2 and b2 and a2 != b2 else "same" if a2 and b2 else "one_side" if a2 or b2 else "none"
        va, vb = a["verdict"], b["verdict"]
        success_a = va["strict_outcome"] == "엄격 충족"
        success_b = vb["strict_outcome"] == "엄격 충족"
        label = "비교불가" if not same_window else {
            (True, True): "양쪽", (True, False): "A만", (False, True): "B만", (False, False): "둘 다 실패",
        }[success_a, success_b]
        if b["card_added_url"]:
            assert b2 == b["card_added_url"]
        pairs.append(dict(purpose_id=purpose, access_method=method, first_url=target["first_url"],
                          comparable_time=same_window, card_added_url=b["card_added_url"] or "",
                          card_add_status=target["add_status"], A_route=a["route_id"], B_route=b["route_id"],
                          A_second_url=a2, B_second_url=b2, actual_second_url_comparison=actual,
                          A_body=va["body"], B_body=vb["body"], A_payload=va["payload"], B_payload=vb["payload"],
                          A_relation=va["observed_relation"], B_relation=vb["observed_relation"],
                          A_outcome=va["strict_outcome"], B_outcome=vb["strict_outcome"],
                          A_7_0_1_service_attribution=va["strict_historical_service"],
                          B_7_0_1_service_attribution=vb["strict_historical_service"],
                          A_views=a["document_views"], B_views=b["document_views"], pair_outcome=label))


def summary(rows, comparisons):
    docs = [doc for row in rows for doc in row["docs"]]
    required = [row for row in rows if targets[row["purpose_id"]]["requires_followup"]]
    verdicts = [row["verdict"] for row in rows]
    successes = sum(v["strict_outcome"] == "엄격 충족" for v in verdicts)
    failures = sum(v["strict_outcome"] == "접근 실패" for v in verdicts)
    unknown = sum(v["strict_outcome"] == "미확인" for v in verdicts)
    assert successes + failures + unknown == len(rows)
    result = {
        "routes": len(rows), "pairs": len(comparisons), "body_readable": sum(v["body"] == "확인" for v in verdicts),
        "followup_required": len(required), "followup_readable": sum(row["verdict"]["payload"] == "확인" for row in required),
        "followup_access_failed": sum(row["verdict"]["payload"] == "접근 실패" for row in required),
        "followup_unconfirmed": sum(row["verdict"]["payload"] == "미확인" for row in required),
        "relation_confirmed": successes, "strict_success": successes, "access_failure": failures, "unknown": unknown,
        "document_views": len(docs), "failed_views": sum(doc["access_failure"] for doc in docs),
        "first_origins_responded": sum(row["docs"][0]["status"] is not None for row in rows),
        "second_document_attempts": sum(row["document_views"] == 2 for row in rows),
        "automatic_redirects": sum(doc["redirect_count"] for doc in docs),
        "menu_opens": sum(row.get("menu_opens", 0) for row in rows),
        "browser_subrequests_captured": sum(doc.get("browser_event_count", {}).get("other_requests_observed_by_capture", 0) for doc in docs),
        "A_views": sum(pair["A_views"] for pair in comparisons), "B_views": sum(pair["B_views"] for pair in comparisons),
        "card_added_url_pairs": sum(bool(pair["card_added_url"]) for pair in comparisons),
        "no_added_url_pairs": sum(not pair["card_added_url"] for pair in comparisons),
        "actual_second_urls": dict(Counter(pair["actual_second_url_comparison"] for pair in comparisons)),
        "pair_outcomes": {label: sum(pair["pair_outcome"] == label for pair in comparisons)
                          for label in ("B만", "A만", "양쪽", "둘 다 실패", "비교불가")},
        "only_cards_with_added_url": dict(Counter(pair["pair_outcome"] for pair in comparisons if pair["card_added_url"])),
        "start_utc_min": min(row["docs"][0]["started_utc"] for row in rows),
        "start_utc_max": max(row["docs"][0]["started_utc"] for row in rows),
        "p1_historical_success": 0, "p1_historical_unconfirmed": sum(v["strict_historical_service"].startswith("미확인") for v in verdicts),
    }
    assert result["followup_required"] == result["followup_readable"] + result["followup_access_failed"] + result["followup_unconfirmed"]
    return result


primary = {
    "all": summary(traversals, pairs),
    **{method: summary([r for r in traversals if r["planned_method"] == method],
                      [p for p in pairs if p["access_method"] == method]) for method in ("browser", "http")},
}
minimum = [s for s in sources if s["minimum_eligible"]]
assert len({s["source_id"] for s in sources}) == len(sources)
assert len({s["original_url"] for s in minimum}) == len(minimum)
buckets = Counter(s["minimum_bucket"] for s in minimum)
assert all(buckets[k] >= n for k, n in {"publisher":8, "asset":8, "rules":4, "iiif":2, "epub":2}.items())
primary["source_minimum"] = {
    "number_of_ledger_rows": len(sources), "eligible_unique_sources": len(minimum),
    "eligible_by_group": dict(buckets), "eligible_lineages": len({s["lineage_id"] for s in minimum}),
    "independent_observed_publication_or_service_case_lineages": [
        "cibuildwheel", "bandersnatch", "archive", "asciicast", "PyPI", "IIIF Cookbook 0009", "Internet Archive 사건 60", "IDPF Moby-Dick"],
    "independent_incident_reports": ["Internet Archive IIIF #60"],
}

ACT = {
    "card_first_click": "카드 첫 클릭", "card_first_get": "첫 GET",
    "card_additional_click": "추가 링크 클릭", "card_additional_get": "추가 URL GET",
    "verbatim_visible_uri_navigation": "보인 문자 URI 탐색", "verbatim_literal_uri_get": "원문 문자 URI GET",
}


def doc_brief(doc):
    utc = doc["started_utc"][11:23] + "Z"
    status = str(doc["status"]) if doc["status"] is not None else (
        "CONNECT 403" if doc["proxy_connect_status"] == 403 else "터널 실패") if doc["method"] == "http" else "터널 실패"
    return f"[{doc['document_number']}]({doc['asked_url']}) {utc} {ACT[doc['action']]} · {status}"


def table_2():
    lines = [
        "| 목적·카드·접근 수단 | 실제 요청·UTC·비용 | 도착 본문·후속 payload | 판 근거·응답 지문 주소 | 엄격 충족·접근 실패·미확인 |",
        "|---|---|---|---|---|",
    ]
    for row in sorted(traversals, key=lambda v: (list(targets).index(v["purpose_id"]), v["card"], v["planned_method"])):
        docs, v = row["docs"], row["verdict"]
        who = "Chromium" if row["planned_method"] == "browser" else "HTTP GET"
        requests = "<br>".join(doc_brief(d) for d in docs) + f"<br>**{len(docs)}회**"
        content = v["body_detail"] + ("<br>" + v["payload_detail"] if v["payload_detail"] else "")
        fingerprints = " · ".join(f"[{i} {'SHA ' + d['decoded_body_sha256'][:9] if d['decoded_body_sha256'] else '실패'}]({d['receipt']})"
                                  for i, d in enumerate(docs, 1))
        fingerprints += "<br>" + v["observed_relation"]
        history = "<br>옛판 엄격 미확인" if v["strict_historical_service"].startswith("미확인") else ""
        lines.append(f"| {row['purpose_id']} {row['card']} · {who} | {requests} | {content} | {fingerprints} | **{v['strict_outcome']}**{history} |")
    return "\n".join(lines)


payloads = {
    "traversals.jsonl": "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in traversals),
    "evidence/counts.json": dump(primary),
}
with StringIO(newline="") as pair_file:
    writer = csv.DictWriter(pair_file, fieldnames=pairs[0], lineterminator="\n")
    writer.writeheader()
    writer.writerows(pairs)
    payloads["pairs.csv"] = pair_file.getvalue()

if __name__ == "__main__":
    if "--verify" in sys.argv[1:]:
        for name, expected in payloads.items():
            assert (root / name).read_text(encoding="utf-8") == expected, name
        assert table_2() in (root / "RESULT.md").read_text(encoding="utf-8")
        print("24 원장행, 12 대응쌍, 표 2, 분모, 파일 지문 주소 및 외부 자료 하한 일치")
    else:
        for name, value in payloads.items():
            (root / name).write_text(value, encoding="utf-8")
        print(table_2())
