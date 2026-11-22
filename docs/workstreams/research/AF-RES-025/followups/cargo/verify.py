#!/usr/bin/env python3
"""Recompute Cargo followup coverage from frozen returns and local audit files."""
import collections
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
OWNED = HERE.parents[1]

def jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

decisions = jsonl(HERE / "decisions.jsonl")
histories = jsonl(HERE / "candidate-history.jsonl")
sources = json.loads((HERE / "sources.json").read_text())
receipts = [json.loads(p.read_text()) for p in sorted((HERE / "receipts").glob("*.json"))]
returns = jsonl(OWNED / "streams/cargo/returns.jsonl")
wanted = {(r["question_id"], r["candidate_id"]) for r in returns if r.get("candidate_id")}
actual = {(r["question_id"], r["candidate_id"]) for r in histories}
assert wanted == actual, (wanted - actual, actual - wanted)
assert len(histories) == len(actual) == 24
assert len(decisions) == 4
assert {r["question_id"] for r in decisions} == {"Q05", "Q06", "Q07", "Q08"}
assert all(len(d["candidate_stage_annotations"]) == 6 for d in decisions)
source_ids = {s["source_id"] for s in sources}
assert len(source_ids) == len(sources)
required = {"source_id", "title", "source_url", "version", "published_or_revised",
            "checked_utc", "sections_read", "verified_content", "limitations",
            "producer", "lineage_id", "count_in_minimum", "count_reason",
            "related_questions", "source_role"}
assert all(required <= set(s) for s in sources)
assert all(isinstance(s["count_in_minimum"], bool) for s in sources)
assert all(set(r["source_ids"]) <= source_ids for r in histories + decisions)
assert all(r["historical_availability"] in {"supported", "not_available", "unknown"} for r in histories)
assert all(r["reason"] and r["next_minimum_check"] and r["actual_probe_receipt_ids"] for r in histories)
receipt_ids = {r["id"] for r in receipts}
assert all(set(s["receipt_ids"]) <= receipt_ids for s in sources)
assert all(set(r["actual_probe_receipt_ids"]) <= receipt_ids for r in histories)
assert all(r["phase"] == "post_primary_seal" and r["discovery_hit"] is False for r in receipts)
assert all(re.fullmatch(r"[0-9a-f]{64}", r["raw_response_sha256"]) for r in receipts)
assert all(isinstance(r["elapsed_ms"], int) and r["elapsed_ms"] >= 0 for r in receipts)
assert all((HERE / "diffs" / (q + ".diff")).is_file() for q in ("Q05", "Q06", "Q07", "Q08"))
assert all((HERE / "final-inputs" / (q + ".md")).is_file() for q in ("Q05", "Q06", "Q07", "Q08"))
public = "\n".join(p.read_text() for p in HERE.rglob("*") if p.is_file() and p.suffix in {".json", ".jsonl", ".md", ".py", ".diff"})
assert not re.search(r"link_[0-9a-f]{32}", public), "Private connector identifier found"
used = {rid for s in sources for rid in s["receipt_ids"]}
explored = {r["record_id"] for r in jsonl(HERE / "exploration.jsonl")}
assert used | explored == receipt_ids
assert used.isdisjoint(explored)
summary = {
    "checks_passed": True,
    "questions": len(decisions),
    "unique_originally_returned_candidates": len(actual),
    "history_status_counts": dict(collections.Counter(r["historical_availability"] for r in histories)),
    "history_status_by_question": {
        q: dict(collections.Counter(r["historical_availability"] for r in histories if r["question_id"] == q))
        for q in sorted({r["question_id"] for r in histories})
    },
    "source_rows": len(sources),
    "new_distinct_original_rows_before_global_lineage_audit": sum(s["count_in_minimum"] for s in sources),
    "new_followup_decision_threads": sum(s["count_in_minimum"] and s["source_role"] == "followup_decision" for s in sources),
    "receipts": len(receipts),
    "search_requests": sum(bool(r["request"].get("system1_search_query")) for r in receipts),
    "read_navigation_api_requests": sum(not bool(r["request"].get("system1_search_query")) for r in receipts),
    "receipt_failures": sum(r["is_error"] for r in receipts),
    "unreceipted_schema_failures_disclosed_separately": 1,
    "tool_elapsed_ms_sum_not_work_time": sum(r["elapsed_ms"] for r in receipts),
    "issue_comments_in_inspected_corpus": sum(d["searched_scope"]["issue_comments_returned"] for d in decisions),
    "inline_comments_not_read": sum(d["searched_scope"]["inline_review_comments_not_read"] for d in decisions),
    "file_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                    for name in ("decisions.jsonl", "candidate-history.jsonl", "sources.json", "cost-summary.json")}
}
print(json.dumps(summary, ensure_ascii=False, indent=2))
