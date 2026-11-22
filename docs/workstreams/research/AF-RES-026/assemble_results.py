"""Assemble family evidence; preserve all case records and source limitations.

No network. This is a mechanical merge, not an independent reading or scorer.
It does not modify the sealed T0 files. Final strategy scores are curated in
adjudication.jsonl and computed separately by summarize.py.
"""
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent
FAMILIES = ("sqlite", "postgres", "curl")
STRICT_EXCLUSIONS = {
    "S-D07": "보수적 최소수에서는 구현 안 설계 주석을 독립 매뉴얼/테스트와 구분하여 제외; 판정 근거로는 유지.",
    "S-D08": "보수적 최소수에서는 구현 안 헤더 지침을 독립 매뉴얼/테스트와 구분하여 제외; 판정 근거로는 유지.",
    "C-D09": "구현 소스 읽기는 확인했으나 문서·테스트·정정 8건의 보수적 최소수에서는 제외.",
    "C-D13": "구현 소스 읽기는 확인했으나 문서·테스트·정정 8건의 보수적 최소수에서는 제외.",
    "C-IM01": "T0 뒤 개발된 별도 구현을 직접 읽었지만 최소수의 '당시 제공자 문서/테스트' 범주에는 소급 산입하지 않음.",
}


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_csv(name):
    rows, fields = [], []
    for family in FAMILIES:
        with (ROOT / "streams" / family / name).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            fields.extend(field for field in reader.fieldnames if field not in fields)
            rows.extend(reader)
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def merge_jsonl(name):
    rows = [row for family in FAMILIES for row in read_jsonl(ROOT / "streams" / family / name)]
    assert len(rows) == 24 and len({r["case_id"] for r in rows}) == 24, name
    (ROOT / name).write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    return rows


def work_key(source):
    """Deduplicate versions/mirrors of one Git file, not unrelated pages."""
    url = urlsplit(source["url"])
    parts = unquote(url.path).strip("/").split("/")
    if url.netloc in ("sqlite.org", "www.sqlite.org") and len(parts) >= 3 and parts[:1] == ["forum"] and parts[1] in ("artifact", "forumpost", "raw"):
        return "sqlite_forum:" + parts[2]
    if url.netloc in ("github.com", "raw.githubusercontent.com"):
        if len(parts) >= 5 and parts[2] == "blob":
            return "git:" + "/".join(parts[:2] + parts[4:])
        if url.netloc == "raw.githubusercontent.com" and len(parts) >= 4:
            return "git:" + "/".join(parts[:2] + parts[3:])
    return url.netloc.lower() + unquote(url.path)


def main():
    for name in ("followups.csv", "judgments.csv"):
        merge_csv(name)
    for name in ("case-analysis.jsonl", "field-locations.jsonl"):
        merge_jsonl(name)

    sources, by_id = [], {}
    for family in (*FAMILIES, "cross"):
        folder = ROOT / "streams" / family
        names = ["sources.json", "t1-sources.json", "sources-t1.json", "followup-sources.json"]
        for name in names:
            path = folder / name
            if not path.exists():
                continue
            for source in json.loads(path.read_text(encoding="utf-8")):
                if source["id"] in by_id:
                    # P's T1 file deliberately reuses IDs for the same work.
                    # Preserve the exact T0 entry and attach the later reading.
                    old = by_id[source["id"]]
                    if work_key(old) != work_key(source):
                        raise ValueError("Source ID reused for a different work: " + source["id"])
                    old.setdefault("postseal_observations", []).append({
                        **source, "source_record_file": str(path.relative_to(ROOT))})
                    continue
                source = dict(source)
                source["source_record_file"] = str(path.relative_to(ROOT))
                source["family_minimum_decision"] = source["count_in_minimum"]
                if source["id"] in STRICT_EXCLUSIONS:
                    source["count_in_minimum"] = False
                    source["count_reason"] = STRICT_EXCLUSIONS[source["id"]]
                source["unique_work_key"] = work_key(source)
                sources.append(source)
                by_id[source["id"]] = source
    counted_keys = {}
    for source in sources:
        if not source["count_in_minimum"]:
            continue
        key = source["unique_work_key"]
        if key in counted_keys:
            source["count_in_minimum"] = False
            source["count_reason"] = "동일 외부 저작의 판/미러 중복. 최소수는 " + counted_keys[key] + "에 한 번 산입."
        else:
            counted_keys[key] = source["id"]
    write_json(ROOT / "sources.json", sources)

    # Preserve family fields and add one explicit record/window interpretation.
    # Censoring dates are observation endpoints, not fabricated author messages.
    initials = {row["case_id"]: row for row in read_jsonl(ROOT / "initial.jsonl")}
    with (ROOT / "followups.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields, followups = list(reader.fieldnames), list(reader)
    additions = ["normalized_record_type", "within30_from_initial_declared_time", "window_origin_audit"]
    fields.extend(field for field in additions if field not in fields)
    differences = []
    for row in followups:
        if row.get("record_type") == "censoring" or row.get("lineage_status") == "bounded_negative_observation":
            kind = "censoring_summary_not_author_message"
        elif row.get("is_edit_of"):
            kind = "revision"
        elif row.get("classification") == "unavailable" and row["case_id"].startswith("S"):
            kind = "unavailable_revision_metadata"
        elif row.get("section") == "adjacent_unlinked_90d":
            kind = "adjacent_unlinked_record_excluded_from_primary"
        else:
            kind = "public_message"
        row["normalized_record_type"] = kind
        root_time = datetime.fromisoformat(initials[row["case_id"]]["submitted_utc"].replace("Z", "+00:00"))
        try:
            occurred = datetime.fromisoformat(row["occurred_utc"].replace("Z", "+00:00"))
            row["within30_from_initial_declared_time"] = root_time <= occurred <= root_time + timedelta(days=30)
        except ValueError:
            row["within30_from_initial_declared_time"] = "미확인"
        row["window_origin_audit"] = "원 family 판정 유지; 이 열은 initial의 제출시각으로 재검. C는 원래 서버 수신시각 창도 보존."
        previous = str(row["within_30_days"]).lower()
        current = str(row["within30_from_initial_declared_time"]).lower()
        if previous in ("true", "false") and current in ("true", "false") and previous != current:
            differences.append({"case_id": row["case_id"], "url": row["url"], "record_type": kind,
                                "family_within30": previous, "declared_time_within30": current})
    with (ROOT / "followups.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(followups)
    write_json(ROOT / "evidence" / "window-audit.json", {"record_count": len(followups),
        "record_types": dict(Counter(row["normalized_record_type"] for row in followups)),
        "clock_origin_boundary_differences": differences,
        "meaning": "비교 가능한 시각 경계를 점검. 검열 요약을 새 작성자 발화로 세지 않고, 인접 미연결 대화를 원 사례에 소급하지 않음."})

    with (ROOT / "frame.csv").open(encoding="utf-8", newline="") as stream:
        frame = list(csv.DictReader(stream))
    stats = {
        "frame_rows": len(frame),
        "frame_decisions": dict(Counter(row["decision"] for row in frame)),
        "source_rows": len(sources),
        "unique_external_works_counted": sum(bool(row["count_in_minimum"]) for row in sources),
        "counted_source_ids": [row["id"] for row in sources if row["count_in_minimum"]],
        "counted_by_kind": dict(Counter(row["kind"] for row in sources if row["count_in_minimum"])),
        "conservative_count_exclusions": STRICT_EXCLUSIONS,
        "unknown_date_sensitivity_excluded": ["X-S1"],
        "definition": "Separate source works, not independent people, projects, or adoptions. A conversation's replies/revisions/crossposts are not new sampled events.",
    }
    write_json(ROOT / "evidence" / "source-counts.json", stats)
    print(json.dumps({k: stats[k] for k in ("frame_rows", "source_rows", "unique_external_works_counted")}, indent=2))


if __name__ == "__main__":
    main()
