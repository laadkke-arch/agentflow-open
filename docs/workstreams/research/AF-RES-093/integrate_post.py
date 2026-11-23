"""Attach post-seal evidence to immutable predictions, preserving attribution."""
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
SEAL = "3c50d0bd1d8f3659d86f8cf45fe233595c3d2592"
PREFIX = "docs/workstreams/research/AF-RES-093/"


def jl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def original(path):
    return subprocess.check_output(["git", "show", f"{SEAL}:{PREFIX}{path}"], cwd=REPO, text=True)


def canonical_event(value):
    value = value.lower()
    match = re.fullmatch(r"pillow-(?:issue-)?(\d+)", value)
    if match:
        return "pillow-issue-" + match.group(1)
    match = re.fullmatch(r"(?:inkscape|ink)-(?:issue-)?(\d+)", value)
    if match:
        return "inkscape-issue-" + match.group(1)
    return value


def main():
    sources = [json.loads(x) for x in original("sources.jsonl").splitlines() if x.strip()]
    files = [
        ("cross_domain_researcher", "evidence/cross-domain/sources.jsonl"),
        ("inkscape_researcher", "evidence/inkscape/post/sources.jsonl"),
        ("pillow_researcher", "evidence/pillow/post/sources.jsonl"),
        ("independent_adjudicator", "evidence/adjudication/source-open-log.jsonl"),
        ("root", "evidence/root-post-sources.jsonl"),
    ]
    for reader, relative in files:
        for row in jl(ROOT / relative):
            row["reader"] = reader
            row["ledger_fragment"] = relative
            sources.append(row)
    for row in sources:
        row.setdefault("reopen_url", row["url"])
        row.setdefault("published_at", None)
        row.setdefault("version", "미확인: 원장 locator/관찰 범위 참조")
        row.setdefault("locator", row.get("section", "원 자료 및 관찰 설명"))
        row.setdefault("questions", ["Q5"] if row["source_id"].startswith("ADJ-") else [])
        row.setdefault("work_id", row.get("work", row["url"].split("#")[0]))
        row.setdefault("event_id", row.get("event", row["work_id"]))
        row.setdefault("category", "independent_recheck")
        row["reported_event_id"] = row["event_id"]
        row["event_id"] = canonical_event(row["event_id"])
        url = row["url"]
        # A later authored discussion is a distinct primary text from the
        # request body, but all comments in one issue remain one source/event.
        if row["category"] == "posthoc_evidence" and "/issues/" in url and "/blob/" not in url:
            row["document_id"] = url.split("#")[0].split("/discussions")[0] + ":followup-thread"
        else:
            row.setdefault("document_id", url.split("#")[0])
        if "reader" not in row:
            row["reader"] = "inkscape_researcher" if row["source_id"].startswith("I-") else "pillow_researcher" if row["source_id"].startswith("PIL-") else "root"
    assert len({r["source_id"] for r in sources}) == len(sources)
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in sources))

    independent = {r["case_id"]: r for r in jl(ROOT / "evidence/adjudication/pair-adjudication.jsonl")}
    inkscape = {r["case_id"]: r for r in json.loads((ROOT / "evidence/inkscape/post/truth.json").read_text())["cases"]}
    pillow = {r["request_id"]: r for r in json.loads((ROOT / "evidence/pillow/post/truth.json").read_text())["cases"]}
    rows = list(csv.DictReader(io.StringIO(original("judgments.csv"))))
    decisions = []
    for case in ("I1", "I2", "I3", "P1", "P2", "P3"):
        review = independent[case]
        author = inkscape.get(case, pillow.get(case))
        author_scorable = author.get("scorable", author.get("strict_scorable"))
        assert author_scorable == review["scorable"], case
        if review["scorable"]:
            assert author.get("label", author.get("gold")) == review["true_pair_label"], case
        source_ids = author.get("sources", author.get("source_ids", []))
        source_ids += [x for c in review["candidates"] for x in c.get("post_source_ids", [])]
        source_ids = list(dict.fromkeys(source_ids))
        urls = list(dict.fromkeys(u for c in review["candidates"] for u in c.get("post_urls", [])))
        expected = review["scope"]["expected"]
        observed = " / ".join(c.get("observed", "후보 결원") for c in review["candidates"])
        for row in rows:
            if row["request_id"] != case:
                continue
            row["truth"] = review["true_pair_label"] if review["scorable"] else ""
            row["scorable"] = str(review["scorable"]).lower()
            row["truth_attribution"] = review["independent_evidence_assessment"]
            row["post_source_ids"] = ";".join(source_ids)
            row["post_urls"] = ";".join(urls)
            row["expected"] = expected
            row["observed_posthoc"] = observed
            row["scope"] = json.dumps(review["scope"], ensure_ascii=False, separators=(",", ":"))
            row["unconfirmed"] = review["minimum_additional_observation"] if not review["scorable"] else "; ".join(review["limitations"])
            if not review["scorable"]:
                row["error_class"] = "미채점: 정답 결손"
            elif row["pre_judgment"] == "유보":
                row["error_class"] = "유보: 정답 있는 행"
            elif row["pre_judgment"] == row["truth"]:
                row["error_class"] = "일치"
            elif row["pre_judgment"] == "묶음":
                row["error_class"] = "오병합"
            else:
                row["error_class"] = "불필요한 분리"
        decisions.append({
            "case_id": case, "scorable": review["scorable"],
            "label": review["true_pair_label"] if review["scorable"] else None,
            "scope": review["scope"], "source_ids": source_ids, "urls": urls,
            "expectation": expected, "observed": observed,
            "minimal_observation": review["minimum_additional_observation"],
            "advisory_label": author.get("advisory_label", author.get("reported_gold")),
            "root_decision": "수집자와 A/B 미노출 검토자의 제한범위 판정이 일치함을 채택. 후보·사전판정은 수정하지 않음.",
        })
    with (ROOT / "judgments.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "integrated_utc": datetime.now(timezone.utc).isoformat(), "seal_sha": SEAL,
        "status": "PARTIAL", "strict_scorable_cases": 1, "planned_cases": 6,
        "primary_policy": "원 요청에 명시된 판·입력·관찰 목표. 정량 픽셀 artifact를 새 의무로 추가하지 않음. 양후보·판·요구의 비교 가능성에 따라 판정.",
        "case_decisions": decisions,
        "sensitivity": [
            "P1 작성자 질적 해결보고를 충분한 gold로 허용하면 분리 gold 1건 추가. A/B는 모두 유보여서 확정판정 오류 분모는 변화 없음.",
            "I1과 P2의 원 코드 및 유지관리자 설명을 gold로 허용하면 분리 예측을 지지하나 후보 설명과 독립된 원판 양결과 대조로 세지 않음.",
            "P3에서 모든 설치판/8.2 호환까지 필수로 바꾸면 기존 8.3 gold는 적용되지 않음. 모집 후 목표를 확장해 기존 정답을 바꾸지 않음.",
            "contaminated I3를 별도 제외해도 채점 가능한 사건수 1은 그대로이며 전체 요청분모는 사전 계약대로 6 유지.",
        ],
        "independence": "별도 검토 에이전트가 A/B 예측을 읽지 않고 원자료로 채점가능성을 검토했다. 외부 독립 실행 또는 사람 평가가 아니다. 유일한 gold는 유지관리자의 게시된 비교이며 후보 구현과 프로젝트 저작군이 겹친다.",
    }
    (ROOT / "evidence/posthoc-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"sources": len(sources), "scorable_cases": 1, "method_slots": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
