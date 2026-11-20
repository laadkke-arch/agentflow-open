"""Index existing query logs and append documented recovery reads, without recounting them."""
from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SOURCE_FIELDS = {"id", "url", "accessed_at_utc", "source_type", "title", "version_or_date", "sections_read", "confirmed", "limits", "level", "used_in"}


def read(path):
    return json.loads(path.read_text())


def query_rows(value, pointer=""):
    if isinstance(value, dict):
        for key in ("q", "query", "query_string"):
            if isinstance(value.get(key), str):
                yield {"json_pointer": pointer or "/", "string_field": key, "query_string": value[key], "original_record": value}
                return
        for key, child in value.items():
            yield from query_rows(child, pointer + "/" + key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from query_rows(child, pointer + "/" + str(index))


def main():
    registry_path = ROOT / "sources.json"
    registry = read(registry_path)
    extra_files = [ROOT / "evidence/recovery/READINGS.json", *sorted(ROOT.glob("evidence/judging-recovery/*/sources.json"))]
    additions = []
    new_excluded = []
    for path in extra_files:
        if not path.exists():
            continue
        data = read(path)
        rows = data if isinstance(data, list) else data.get("sources", [])
        for source in rows:
            missing = REQUIRED_SOURCE_FIELDS - source.keys()
            assert not missing, (str(path), source.get("id"), sorted(missing))
            source = dict(source)
            source["recorded_in"] = str(path.relative_to(ROOT))
            source["minimum_counted_noncase"] = False
            source["counting_note"] = "판정 추가 검증 또는 기존 출처 재열람; 최소 비사례25개에 추가 산입하지 않음."
            additions.append(source)
        for excluded in data.get("excluded", []) if isinstance(data, dict) else []:
            new_excluded.append({**excluded, "recorded_in": str(path.relative_to(ROOT)), "counted": False})
    by_id = {s["id"]: s for s in registry["sources"]}
    assert len(by_id) == len(registry["sources"])
    assert len({s["id"] for s in additions}) == len(additions), "Recovery IDs collide"
    for source in additions:
        by_id[source["id"]] = source
    registry["sources"] = list(by_id.values())
    fingerprints = {json.dumps(x, ensure_ascii=False, sort_keys=True) for x in registry["excluded"]}
    for row in new_excluded:
        fingerprint = json.dumps(row, ensure_ascii=False, sort_keys=True)
        if fingerprint not in fingerprints:
            registry["excluded"].append(row)
            fingerprints.add(fingerprint)
    registry["counting"]["all_source_records_including_support"] = len(registry["sources"])
    registry["counting"]["excluded_attempts"] = len(registry["excluded"])
    registry["counting"]["recovery_read_records_not_added_to_minimum"] = len(additions)
    registry["counting"]["case_host_site_groups"] = {"github.com": 31}
    registry["counting"]["literal_case_count_after_site_cap"] = 3
    registry["counting"]["strict_case_minimum_after_site_cap_satisfied"] = False
    registry["counting"]["site_cap_interpretation_status"] = "최초 SAMPLING의 비사례 한정 해석은 연구자가 사전 명시했으나 사용자 승인된 예외가 아니다. 사례에도 사이트당3개를 문자적으로 적용하면 최소30개 인수 조건은 미충족이다."
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "evidence/SOURCE_COUNT.json").write_text(json.dumps(registry["counting"], ensure_ascii=False, indent=2) + "\n")

    original_logs = []
    indexed_queries = []
    for path in sorted(ROOT.glob("evidence/**/*SEARCH_LOG.json")):
        data = read(path)
        rel = str(path.relative_to(ROOT))
        original_logs.append({"path": rel, "content": data})
        for row in query_rows(data):
            indexed_queries.append({"original_path": rel, **row})
    baseline_queries = []
    for path in sorted(ROOT.glob("runs/*/C*.json")):
        data = read(path)
        baseline_queries.append({"path": str(path.relative_to(ROOT)), "case_id": data["case_id"], "baseline": data["baseline"], "queries": data["queries"]})
    output = {
        "schema_version": 1,
        "purpose": "사례 선정·역사 판 복구·방법론·반례 탐색·재개 검증의 실제 문자열 및 기존 기준선 질의 통합 색인",
        "notes": ["원 기록의 오타·대소문자·질의 순서를 보존한다. URL 직접 탐색을 검색엔진 질의라고 부르지 않는다.", "같은 문자열 반복 실행을 삭제하지 않는다. 단순 목록·메타데이터·실패 기록은 D1 출처 수에 포함하지 않는다.", "원 기록에 묶음 시각만 있으면 그 정밀도를 유지하며 개별 요청 시각을 만들어 채우지 않는다.", "A/B 원 응답·열람 문서·노출은 runs의 원 파일이 기준이다. 이 색인은 재실행이 아니다."],
        "counts": {"nonbaseline_original_log_files": len(original_logs), "indexed_nonbaseline_query_or_url_records": len(indexed_queries), "baseline_query_records": dict(Counter(r["baseline"] for group in baseline_queries for r in [{"baseline": group["baseline"]}] for _ in group["queries"]))},
        "nonbaseline_query_index": indexed_queries,
        "nonbaseline_original_logs": original_logs,
        "baseline_queries": baseline_queries,
        "source_open_index": [{"id": s["id"], "url": s["url"], "accessed_at_utc": s["accessed_at_utc"], "level": s["level"], "recorded_in": s.get("recorded_in")} for s in registry["sources"]],
        "failed_open_index": registry["excluded"],
    }
    (ROOT / "SEARCH_LOG.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"sources": len(registry["sources"]), "excluded": len(registry["excluded"]), "minimum_noncase": registry["counting"]["noncase_counted"], **output["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
