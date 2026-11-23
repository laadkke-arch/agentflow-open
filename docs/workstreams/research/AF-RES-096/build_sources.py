#!/usr/bin/env python3
"""Normalize directly read source notes; never change sealed route evidence."""
from __future__ import annotations
import collections
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUTS = [
    "evidence/jq/sources.jsonl", "evidence/pandoc/sources.jsonl",
    "evidence/jq/sources-note.jsonl", "evidence/pandoc/sources-note.jsonl",
    "evidence/crossdomain/sources.jsonl",
    "evidence/post-jq/source-note.jsonl", "evidence/post-pandoc/sources-note.jsonl",
    "evidence/intake/sources-note.jsonl",
]

def choose(row, *keys, default=None):
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return default

def normalize(row, source_file, ordinal):
    category = choose(row, "minimum_category", "count_category", default="auxiliary")
    category = {"main_manual": "main_manual_implementation",
                "main_implementation": "main_manual_implementation",
                "adjacent_manual": "adjacent_manual_implementation",
                "adjacent_implementation": "adjacent_manual_implementation"}.get(category, category)
    eligible = bool(choose(row, "minimum_count_eligible", "minimum_counted", "eligible", default=False))
    if "post-" in source_file:
        eligible = False
        category = "post_outcome_or_validation"
    original = choose(row, "original_source_url", "original_url", "url", default="미확인")
    reread = choose(row, "reread_url", "reopen_url", "read_url", "api_url", default=original)
    source_id = row.get("source_id", f"AUX-{source_file}-{ordinal}")
    key = choose(row, "independent_source_key", default=original)
    return {
        "source_id": source_id,
        "original_url": original,
        "reread_url": reread,
        "published_utc": choose(row, "published_utc", "published", default="미확인"),
        "publication_basis": choose(row, "publication_precision", "publication_time_meaning", "published_basis", default="원 기록의 creation/revision 시각; 게시 첫 바이트와 동일함까지 보장하지 않음"),
        "checked_utc": choose(row, "reviewed_utc", "checked_utc", "read_utc", "fetched_utc", default="미확인"),
        "first_body_open_utc": choose(row, "first_body_open_utc", "checked_utc", "fetched_utc", default="미확인"),
        "version": choose(row, "version", "version_revision", default="미확인"),
        "commit": row.get("commit"),
        "file_id": row.get("file_id", source_id if source_id[:2] in {"CU", "GR", "JQ", "OP"} else None),
        "file": choose(row, "file", "path", default="question/answer body"),
        "sections_lines": choose(row, "sections_read", "read_sections", "file_section_lines", "section", "lines", default="원 기록 참조"),
        "directly_verified": choose(row, "directly_verified", "directly_observed", "verified", "finding", default="원 기록 참조"),
        "short_excerpt": choose(row, "short_excerpt", "quote"),
        "supports_or_refutes": choose(row, "supports_or_refutes_questions", "supports_questions", "supports_or_refutes", "supports", default=["Q6"] if "post-" in source_file else []),
        "limitations_unverified": choose(row, "limitations_unknown", "limitations_unverified", "limitations", default="원 기록 참조; 원 사용자 실행은 별도 관측"),
        "authorship_lineage": choose(row, "authorship_lineage", "work_lineage", "lineage", "authorship_event_lineage", default="원 출처 저자"),
        "event_lineage": choose(row, "event_lineage", "independent_work_event", "event_id", "independent_event_note", "authorship_event_lineage", default="개별 사용자 사건 수와 합산하지 않음"),
        "minimum_count_eligible": eligible,
        "minimum_category": category,
        "independent_source_key": key,
        "body_sha256": choose(row, "body_sha256", "sha256"),
        "route_evidence": row.get("route_evidence", "sources-note.jsonl" in source_file and "post-" not in source_file),
        "read_routes": choose(row, "read_routes", "route_body_opens", default=[]),
        "attribution": choose(row, "attribution", "researcher_inference", default="직접 원문의 사실 요약. 적용·해법 합성·분류는 연구자 추론이며 실행 관측과 분리."),
        "original_note_file": source_file,
        "original_note_line": ordinal,
        "original_note": row,
    }

def main():
    rows = []
    for relative in INPUTS:
        path = ROOT / relative
        if not path.exists():
            continue
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if line.strip():
                rows.append(normalize(json.loads(line), relative, i))
    seen_ids, eligible_keys, eligible_hashes = set(), {}, {}
    for row in rows:
        if row["source_id"] in seen_ids:
            raise ValueError("duplicate source ID: " + row["source_id"])
        seen_ids.add(row["source_id"])
        if row["minimum_count_eligible"]:
            key, sha = row["independent_source_key"], row["body_sha256"]
            duplicate = eligible_keys.get(key) or (eligible_hashes.get(sha) if sha else None)
            if duplicate:
                row["minimum_count_eligible"] = False
                row["duplicate_of"] = duplicate
                row["minimum_exclusion_reason"] = "same source key or exact body hash; repeat/mirror excluded"
            else:
                eligible_keys[key] = row["source_id"]
                if sha:
                    eligible_hashes[sha] = row["source_id"]
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    eligible = [x for x in rows if x["minimum_count_eligible"]]
    counts = dict(sorted(collections.Counter(x["minimum_category"] for x in eligible).items()))
    minima = {"new_r0": 8, "main_manual_implementation": 4, "adjacent_manual_implementation": 4,
              "upstream_original_test": 4, "crossdomain_sphinx": 2, "crossdomain_gdal": 2}
    summary = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "rows_in_ledger": len(rows), "eligible_unique_primary_sources": len(eligible),
        "eligible_by_category": counts, "required_by_category": minima,
        "minima_satisfied": len(eligible) >= 24 and all(counts.get(k, 0) >= v for k, v in minima.items()),
        "selected_independent_public_request_events": 8,
        "request_event_note": "8 question IDs; answers/comments/revisions are follow-ups to those same events, not new independent requests.",
        "crossdomain_note": "14 primary files, 3 project lineages and 5 specification/test calibration goals; no newly recruited requests or A/B wins.",
        "counting_note": "Distinct versioned files/bodies, not independent authors or statistically independent observations. Search previews, prior handoffs, metadata, licenses, duplicate reads and own outputs excluded.",
        "eligible_ids": [x["source_id"] for x in eligible],
    }
    (ROOT / "evidence/source-counts.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "eligible_ids"}, ensure_ascii=False))

if __name__ == "__main__":
    main()
