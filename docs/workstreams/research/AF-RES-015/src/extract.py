"""Build the reason ledger from reviewed annotations and the pinned AF-RES-011 tree."""

import csv
import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = "478c301b693896e2c6d777f46ac441f071bfdfe8"
UPSTREAM = f"{SHA}:docs/workstreams/research/AF-RES-011/"
TYPES = {
    "F": "기능 지원", "C": "가격", "L": "라이선스", "P": "플랫폼",
    "H": "호스팅 방식", "M": "관리 상태", "S": "성능", "O": "기타 검증 가능",
    "N": "이유 없음",
}


def upstream(path):
    return json.loads(subprocess.check_output(["git", "show", UPSTREAM + path]))


def jsonl(path, records):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records))


def normalize(text):
    return re.sub(r"[^\w]", "", text.casefold())


def aliases(candidate, case):
    match = normalize(candidate)
    return [x for x in case["link_status_now"]
            if normalize(str(x.get("candidate") or "")) == match]


def supplied_links(answer):
    single = answer.get("candidate_url") or answer.get("recommendation_url")
    return [x for x in ([single] if single else answer.get("links", []))
            if isinstance(x, str) and x.startswith(("https://", "http://"))]


def read_annotations():
    for path in sorted((ROOT / "data").glob("extract-*.txt")):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line or line.startswith("#"):
                continue
            ref, candidate, type_code, key, issued, locator, target, *urls = line.split("|")
            if issued:
                date.fromisoformat(issued)
            if not ref or not candidate or not key or not locator or not target or len(urls) > 1:
                raise ValueError(f"{path.name}:{lineno}: missing annotation field")
            yield ref, candidate, TYPES[type_code], key, issued, locator, target, urls


def main():
    cases = upstream("CASES.json")["cases"]
    inventory = {a["analysis_id"]: (c, a) for c in cases for a in c["answers"]}
    records, extracted = [], set()

    for ref, candidate, reason_type, key, issued, locator, target, urls in read_annotations():
        case, answer = inventory[ref]
        links = [link["url"] for link in aliases(candidate, case) if link.get("url")]
        posted = supplied_links(answer)
        original = links[0] if len(set(links)) == 1 else None
        # A product in a multi-candidate answer does not automatically inherit the first link.
        if original is None and len(posted) == 1 and (
            not answer.get("candidate") or normalize(str(answer["candidate"])) == normalize(candidate)
        ):
            original = posted[0]
        url = urls[0] if urls and urls[0] else original
        basis = "원문" if locator.startswith(("L", "본문", "댓글")) else "고정 입력 답별 요약"
        source_locator = str(answer.get("id_or_permalink") or answer.get("id") or "")
        original_post = case["url"]
        if case["platform"] == "hackernews" and source_locator.isdigit():
            original_post = f"https://news.ycombinator.com/item?id={source_locator}"
        if source_locator.startswith(("https://", "http://")):
            original_post = source_locator
        evidence = {
            "basis": basis, "position": locator,
            "source_url": case["url"] if basis == "원문" and locator.startswith("L") else original_post,
            "upstream_case_position": f"CASES.json cases[id={case['id']}].answers[analysis_id={ref}]",
        }
        if source_locator and not source_locator.startswith(("https://", "http://")):
            evidence["fixed_post_id"] = source_locator
        row = {
            "reason_id": f"{ref}/{key}", "answer_ref": ref, "candidate": candidate,
            "url": url, "url_origin": ("원문 지정" if urls and urls[0] else "011 연결" if url else None),
            "answer_date": issued or None, "reason_type": reason_type,
            "reason_target": target, "evidence_locator": evidence, "predicate": key,
            "now_verdict": None, "now_evidence_url": None, "now_checked_at_utc": None,
            "then_verdict": None, "then_evidence": None, "break_interval": None, "signals": {},
        }
        extracted.add(ref)
        records.append(row)

    with (ROOT / "results" / "answer-coverage.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("answer_ref", "thread_url", "thread_platform", "upstream_form", "status"))
        for ref, (case, answer) in inventory.items():
            if ref in extracted:
                status = "코딩됨"
            elif answer.get("minimal_answer_kind") in {"name_only", "url_only"}:
                status = "011 최소 후보(이유 행 추가 확인 필요)"
            elif not (answer.get("candidate") or supplied_links(answer)):
                status = "후보 링크 없음 또는 요약 검토 필요"
            else:
                status = "추출 미확인(이유 귀속 검토 필요)"
            writer.writerow((ref, case["url"], case["platform"], answer["form"], status))

    if len({r["reason_id"] for r in records}) != len(records):
        raise ValueError("duplicate reason_id")
    jsonl(ROOT / "REASONS.jsonl", sorted(records, key=lambda r: r["reason_id"]))


if __name__ == "__main__":
    main()
