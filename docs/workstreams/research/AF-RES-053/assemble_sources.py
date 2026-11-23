#!/usr/bin/env python3
"""Assemble direct-read logs and conservative, disjoint source allocations."""
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
PARTS = [
    "evidence/governance-sources.jsonl",
    "streams/vega/sources.jsonl", "streams/libass/sources.jsonl",
    "streams/vega/receiver-sources.jsonl", "streams/libass/receiver-sources.jsonl",
    "streams/donors/sources.jsonl", "evidence/root-card-sources.jsonl",
    "streams/vega/outcome-sources.jsonl", "streams/libass/outcome-sources.jsonl",
    "replay/sources-new.jsonl",
]
ALIASES = {
    "vl-implementation": "vl-official-manual",
    "D-M02": "D-M01",
}
REQUESTS = ["vega-lite-issue-7278", "vega-lite-issue-7422", "vega-lite-issue-7507", "libass-issue-588", "libass-issue-685"]
RECEIVERS = ["vl-official-manual", "vl-example-aggregate-nested", "vl-example-conditional-axis", "libass-public-api", "aegisub-manual-3.2"]
COUNTERS = ["libass-issue-598", "libass-issue-600"]
DONORS = ["D-P01", "D-P02", "D-M01", "D-M03"]


def eligible(row):
    status = row["직접열람_상태"].lower()
    kind = row["자료종류"]
    work = row["work_id"]
    if work == "vega-lite-issue-7372":
        return False, "사후 교차 검토: 본문은 열지 않은 PR을 가리키는 한 문장뿐. pointer-only 저작을 보수적으로 최소수에서 제외"
    if row.get("substantive_work") is False or row.get("count_primary") is False or row.get("고유저작_산입") is False:
        return False, "명시적 비산입 또는 body:null"
    if "failed" in status or "실패" in status:
        return False, "접근 실패; 최소수 제외"
    if "metadata" in status or "메타데이터" in status or "내부 입력" in kind:
        return False, "내부 입력 또는 발행/검색 metadata; 최소수 제외"
    if work in {"AF-RES-049", "agentflow-open-governance", "lz-string-1.4.4"}:
        return False, "선행 내부 결과 또는 복원 도구; 새 연구 원전 최소수 제외"
    if row.get("count_for_primary_minimum") is False:
        return False, "재생 의존성/도구의 별도 기록; 연구 원전 최소수 제외"
    return True, "내용과 위치를 직접 확인한 1차 자료; 동일 저작의 재열람은 중복 제거"


def main():
    rows = []
    for name in PARTS:
        path = ROOT / name
        if not path.exists():
            raise FileNotFoundError(name)
        rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    ids = [r["source_id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source_id")
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    groups = defaultdict(list)
    for line, row in enumerate(rows, 1):
        groups[row["work_id"]].append((line, row))
    works = []
    for work, items in sorted(groups.items()):
        included = [(line, row) for line, row in items if eligible(row)[0]]
        works.append({"work_id": work, "canonical_work_id": ALIASES.get(work, work),
                      "primary_eligible": bool(included), "read_rows": len(items),
                      "source_ids": [row["source_id"] for _, row in items],
                      "sources_jsonl_lines": [line for line, _ in items],
                      "eligible_read_lines": [line for line, _ in included],
                      "notes": sorted({eligible(row)[1] for _, row in items})})
    eligible_works = {w["canonical_work_id"] for w in works if w["primary_eligible"]}
    allocation = {
        "requester_originals": {"required": 6, "work_ids": REQUESTS, "reason": "선정5요구만; L03 미충원. 제외 이슈를 요청자6번째로 대체하지 않음."},
        "receiver_contemporary_docs_examples": {"required": 4, "work_ids": RECEIVERS, "reason": "Vega 문서와 구현은 보수적으로 병합; 독립 공식 예제2와 libass API·Aegisub 설명. 판/사례 대응은 receiver-review."},
        "printing_mapping_originals": {"required": 4, "work_ids": DONORS, "printing": 2, "mapping": 2, "reason": "QGIS User/Training Manuals를 보수적으로1저작으로 묶음. CSS/XSL2+QGIS/OS2."},
        "new_independent_public_followup_outputs": {"required": 6, "work_ids": [], "reason": "선정5issue 댓글/그림은 요청자원문과 동일저작; 연결된 별도 PR·기대시험을 확보하지 못함. 2020 PR384/385는 L01 이전 배경. 자체 재생은 공개 후속저작에 산입하지 않음."},
        "independent_boundary_counterexamples": {"required": 2, "work_ids": COUNTERS, "reason": "#598 좌표/overscan·#600 세로조판; 주표본과 다른 저작."},
    }
    for values in allocation.values():
        missing = set(values["work_ids"]) - eligible_works
        if missing:
            raise ValueError(f"Allocation work not eligible: {missing}")
        values["observed"] = len(values["work_ids"])
        values["status"] = "충족" if values["observed"] >= values["required"] else "미충족"
    all_assigned = [work for value in allocation.values() for work in value["work_ids"]]
    if len(all_assigned) != len(set(all_assigned)):
        raise ValueError("Allocation must be disjoint")
    failed = [r for r in rows if "failed" in r["직접열람_상태"].lower() or "실패" in r["직접열람_상태"]]
    report = {"generated_UTC": datetime.now(timezone.utc).isoformat(), "parts": PARTS,
              "total_read_rows": len(rows), "failed_access_rows": len(failed),
              "primary_count_eligible_rows": sum(eligible(r)[0] for r in rows),
              "eligible_rows_note": "중복·재생도구 비산입 flag를 반영한 행 수이며, 성공한 모든 직접 열람 횟수와 같지 않다.",
              "unique_primary_works_before_conservative_merge": sum(w["primary_eligible"] for w in works),
              "unique_primary_works_conservative": len(eligible_works), "minimum_required": 22,
              "unique_minimum_met": len(eligible_works) >= 22,
              "required_allocation_met": all(v["status"] == "충족" for v in allocation.values()),
              "assigned_unique_works": len(all_assigned), "canonical_aliases": ALIASES,
              "allocation": allocation, "works": works,
              "interpretation": "큰 고유저작 수의 다수는 모집 제외 이슈다. 최소 총수 충족이 필수 배당 충족이나 사전예측 검증을 뜻하지 않는다. 전체 열람행에는 실패/metadata/내부읽기도 포함한다."}
    (ROOT / "evidence/source-counts.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["total_read_rows", "primary_count_eligible_rows", "unique_primary_works_conservative", "required_allocation_met"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
