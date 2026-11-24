#!/usr/bin/env python3
"""Reconcile supplemental evidence without inspecting natural experiment artifacts."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

p = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--write-evidence", action="store_true")
args = parser.parse_args()
def jsonl(name):
    return [json.loads(line) for line in (p / name).read_text().splitlines() if line.strip()]
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
sources = jsonl("sources-analogies.jsonl")
queries = jsonl("discovery-queries.jsonl")
metrics = json.loads((p / "metrics-analogies.json").read_text())
with (p / "claims.csv").open(newline="") as stream:
    claims = list(csv.DictReader(stream))
ids = {r["source_id"] for r in sources}
assert len(ids) == len(sources) == metrics["opened_action_count"] == 67
assert len({r["original_url"] for r in sources}) == metrics["distinct_original_urls"] == 37
unique = [r for r in sources if r["unique_counted"]]
assert len(unique) == len({r["work_id"] for r in unique}) == metrics["unique_primary_work_count"] == 13
assert {r["work_id"] for r in unique} == set(metrics["unique_work_ids"])
for claim in claims:
    assert all(x in ids for x in claim["source_rows"].split(";")), claim["claim_id"]
claim_ids = {r["claim_id"] for r in claims}
for source in sources:
    assert all(x in claim_ids for x in source["ledger_rows"]), source["source_id"]
assert len(claims) == 9
assert len(queries) == metrics["search_query_count"] == 24
methods = Counter(r["read_method"] for r in sources)
assert methods["urllib.request.urlopen"] == metrics["direct_http_gets"] == 7
assert methods["local_pdf_render_view"] == metrics["local_image_view_attempts"] == 6
assert len(sources) - methods["urllib.request.urlopen"] - methods["local_pdf_render_view"] == metrics["web_document_operations"] == 54
for name in ["natural_cases_read", "natural_packets_read", "gold_read", "reader_trials_conducted"]:
    assert metrics[name] == 0
receipts = jsonl("eisenhower/download-receipts.jsonl")
for receipt in receipts:
    name = receipt["original_url"].rsplit("/", 1)[-1]
    if name == "farewell-address-january-17-1961.pdf":
        name = "subject-guide.pdf"
    path = p / "eisenhower" / name
    assert path.stat().st_size == receipt["bytes"]
    assert sha(path) == receipt["sha256"]
assert sum(r["bytes"] for r in receipts) == metrics["retained_pdf_download_bytes"]
visuals = jsonl("eisenhower/visual-readings.jsonl")
assert len(visuals) == 4
for visual in visuals:
    assert sha(p / visual["render_path"]) == visual["render_sha256"]
    assert visual["source_id"] in ids
facsimiles = [r for r in sources if r["observation_status"] == "read_original_facsimile"]
assert len({r["original_url"] for r in facsimiles}) == metrics["original_manuscript_facsimile_read_count"] == 2
assert len({(r["original_url"], r["pdf_page"]) for r in facsimiles}) == metrics["original_facsimile_unique_pages_read"] == 3
for report in ["ANALOGIES.md", "eisenhower/READING_NOTES.md"]:
    tail = (p / report).read_text().split("| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |")[-1]
    lines = [x for x in tail.splitlines() if x.strip()]
    assert len(lines) == 4, (report, len(lines))
artifacts = {}
for path in sorted(p.rglob("*")):
    if path.is_file() and path.name != "ledger-check.json" and "__pycache__" not in path.parts:
        artifacts[str(path.relative_to(p))] = sha(path)
result = {
    "check": "cross-domain ledger reconciliation",
    "actor": "/root/cross_domain AI worker",
    "checked_utc": datetime.now(timezone.utc).isoformat(),
    "command": "python -B docs/workstreams/research/AF-RES-116/analogies/verify_analogies.py --write-evidence",
    "result": "PASS",
    "checks": [
        "67 operation rows and unique source IDs; 54 web + 7 HTTP + 6 local image requests",
        "All 9 claims resolve to existing source rows; all source claim references resolve",
        "13 uniquely counted works, one counted row each; 37 distinct original URLs",
        "24 discovery-only queries; zero natural/gold/packet exposure and reader trials",
        "Downloaded PDF bytes and SHA-256 match receipts; rendered image hashes match visual reading rows",
        "2 original record versions / 1 speech work / 3 visually read original pages",
        "Both substantive reports end in exactly 3 weakness/next-source/change-observation rows"
    ],
    "limitations": [
        "Same worker support review, not independent reading or causal experiment",
        "Yale original remains unread; Eisenhower supplies a separate directly read original example",
        "FDR institutional statement read, underlying Senate/House originals not independently examined",
        "Two prior image outputs not retained after context compaction are attempts only; confirmed reopens provide evidence",
        "No claim of reader effects or human time saving"
    ],
    "artifact_sha256": artifacts,
}
if args.write_evidence:
    (p / "ledger-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "artifact_sha256"}, ensure_ascii=False, indent=2))
