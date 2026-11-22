#!/usr/bin/env python3
"""Validate AF-RES-022 ledgers and report structure; no network or mutations.

Run from repository root:
  PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-022/tools/validate.py
This checks research invariants, not the truth of an author's retrospective.
"""
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[3]
OWNED = BASE.relative_to(REPO).as_posix() + "/"
FOUNDATION = "435a5099a0abb0bb4b3c08d40401d0e304e82153"
checks = []


def check(condition, met, detail):
    checks.append({"condition": condition, "met": bool(met), "detail": detail})


def read_jsonl(name):
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line.strip()]


def read_csv(name):
    with (BASE / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


sources = json.loads((BASE / "sources.json").read_text())
decisions = read_jsonl("decisions.jsonl")
sampling = read_csv("sampling.csv")
costs = read_csv("costs.csv")
stats = json.loads((BASE / "evidence/statistics.json").read_text())
result = (BASE / "RESULT.md").read_text()
source_ids = [s["source_id"] for s in sources]
case_ids = [d["id"] for d in decisions]
cost_ids = [c["cost_id"] for c in costs]
check("unique_source_ids", len(source_ids) == len(set(source_ids)), len(source_ids))
check("unique_case_ids", len(case_ids) == len(set(case_ids)), case_ids)
check("unique_cost_ids", len(cost_ids) == len(set(cost_ids)), len(cost_ids))
required_source_fields = {
    "source_id", "case_ids", "questions", "url", "published_or_version", "checked_utc",
    "location", "observed", "limitation", "evidence_kind", "lineage", "count_category",
    "count_in_minimum", "access",
}
missing = {s["source_id"]: sorted(required_source_fields - s.keys())
           for s in sources if required_source_fields - s.keys()}
check("source_provenance_complete", not missing, missing)
counted = [s for s in sources if s["count_in_minimum"]]
bad_access = [s["source_id"] for s in counted if s["access"] != "direct_full_or_selected_section"]
check("count_only_direct_originals", not bad_access, bad_access)
url_counts = Counter(s["url"] for s in counted)
check("no_identical_counted_source_url", all(n == 1 for n in url_counts.values()),
      {u: n for u, n in url_counts.items() if n > 1})
counts = Counter(s["count_category"] for s in counted)
check("minimum_unique_originals_36", len(counted) >= 36, len(counted))
for category, minimum in {"decision": 16, "followup": 10, "version": 6,
                          "crossfield_patent": 2, "crossfield_engineering": 2}.items():
    check("minimum_" + category, counts[category] >= minimum, counts[category])

A = [d for d in decisions if d["sample"] == "A"]
B = [d for d in decisions if d["sample"] == "B"]
check("A_24_consecutive_choices", len(A) == 24 and {d["id"] for d in A} ==
      {f"A{i:02}" for i in range(1, 25)}, len(A))
check("B_at_least_8_unique_additions", len(B) >= 8 and all(not d.get("linked_A_id") for d in B), len(B))
check("A_eight_per_frozen_family", Counter(d["record_family"] for d in A) == {"F1": 8, "F2": 8, "F3": 8},
      dict(Counter(d["record_family"] for d in A)))
check("no_recount_017", all(d.get("duplicate_017") is False for d in decisions),
      [d["id"] for d in decisions if d.get("duplicate_017") is not False])
bad_refs = {}
for decision in decisions:
    refs = set(decision["source_ids"])
    for item in decision.get("alternatives", []) + decision.get("awareness", []):
        refs.update(item.get("source_ids", []))
    absent = sorted(refs - set(source_ids))
    if absent:
        bad_refs[decision["id"]] = absent
check("case_source_references_resolve", not bad_refs, bad_refs)
missing_cases = [d["id"] for d in A if not d.get("original_url") or
                 not d.get("followup_search_scope") or not d.get("minimum_next_record")]
check("all_A_have_original_followup_and_next_record", not missing_cases, missing_cases)
bad_dates = []
for d in decisions:
    for kind in ("need", "first_public_implementation", "decision", "implementation"):
        entry = d.get(kind, {})
        if "date" not in entry or not entry.get("precision"):
            bad_dates.append([d["id"], kind])
check("date_types_and_precision_separated", not bad_dates, bad_dates)
strict_bad = []
for d in decisions:
    if not d.get("strict_discovery_change"):
        continue
    unaware = any(a.get("kind") == "explicit_unaware" and a.get("role") in
                  ("decision_maker", "proposer") for a in d.get("awareness", []))
    usable = any(a.get("available_at_decision") == "yes" for a in d.get("alternatives", []))
    implemented = d.get("implementation", {}).get("status") not in (
        None, "unconfirmed", "not_implemented", "change_unconfirmed")
    if not (unaware and usable and implemented and d.get("causal_statement_url") and d.get("connected_chain")):
        strict_bad.append(d["id"])
check("strict_positive_has_required_chain", not strict_bad, strict_bad)
check("statistics_match_A_B", stats["A"]["n"] == len(A) and stats["B"]["n"] == len(B),
      {"A": len(A), "B": len(B)})
check("statistics_strict_A_matches", stats["A"]["strict_discovery_change"] ==
      sum(bool(d.get("strict_discovery_change")) for d in A), stats["A"]["strict_discovery_change"])
check("statistics_strict_B_matches", stats["B"]["strict_discovery_change"] ==
      sum(bool(d.get("strict_discovery_change")) for d in B), stats["B"]["strict_discovery_change"])
check("statistics_source_counts_match", stats["sources"]["categories"] == dict(counts) and
      stats["sources"]["counted_unique_originals"] == len(counted), dict(counts))
check("all_A_public_proposals_preserved", all(d.get("proposal", {}).get("date") and d["proposal"].get("url") for d in A),
      [d["id"] for d in A if not d.get("proposal", {}).get("date")])
known = sum(d["initial_awareness_audit"]["baseline_known"] is True for d in A)
unknown_ids = [d["id"] for d in A if d["initial_focal_awareness_unknown"]]
candidate_ids = [d["id"] for d in A if d["available_awareness_completion_candidate"]]
check("awareness_audit_counts_match", known == stats["A"]["initial_focal_known"] and
      unknown_ids == stats["A"]["initial_focal_unknown_ids"] and candidate_ids == stats["A"]["available_awareness_completion_candidates"],
      {"known": known, "unknown": unknown_ids, "conditional_candidates": candidate_ids})
check("cost_scope_and_units", all(c.get("unit") and c.get("scope") and c.get("limitation") for c in costs), len(costs))
check("cost_references_resolve", all(cid in cost_ids for d in decisions for cid in d.get("cost_ids", [])), len(costs))
check("cost_missingness_covers_every_choice", {c["case_id"] for c in costs} == set(case_ids) and
      stats["costs"]["rows"] == len(costs), len({c["case_id"] for c in costs}))
link_check = json.loads((BASE / "evidence/link-check.json").read_text())
check("all_Q_primary_locations_reopened", link_check["covered_questions_with_success"] == [f"Q{i}" for i in range(1, 9)],
      link_check["covered_questions_with_success"])

table_headers = [
    "| 표본 A/B·사건 ID | 원 결정·목적·날짜 정밀도 |",
    "| 표본·기록 계열 | 검토·탈락·채택 수 |",
    "| 사건 ID | 관측한 비용·단위 |",
    "| Q 번호 | 주장·판정 범위 |",
]
positions = [result.find(h) for h in table_headers]
check("four_required_tables_in_order", all(p >= 0 for p in positions) and positions == sorted(positions), positions)
first_lines = [line for line in result.splitlines()[1:] if line.strip()]
check("tables_before_method_prose", first_lines and
      (first_lines[0].startswith("## 표 1") or first_lines[0].startswith("| 표본 A/B")), first_lines[:2])
tail = []
for line in reversed(result.rstrip().splitlines()):
    if line.startswith("|"):
        tail.append(line)
    else:
        break
tail.reverse()
check("final_table_exactly_three_data_rows", len(tail) == 5 and
      tail[0].startswith("| 중요한 불일치·약점 | 근거 ID·주소 |"), len(tail))
check("all_Q_answer_sections", all(re.search(r"^## Q" + str(i) + r"\b", result, re.M)
                                  for i in range(1, 9)), "Q1–Q8")
changed = subprocess.check_output(["git", "diff", "--name-only", FOUNDATION], cwd=REPO, text=True).splitlines()
untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=REPO, text=True).splitlines()
outside = [name for name in changed + untracked if not name.startswith(OWNED)]
check("owned_path_only", not outside, outside)
check("dot_control_unchanged", not subprocess.check_output([
    "git", "diff", FOUNDATION, "--", "docs/automation/dot-control.json"], cwd=REPO, text=True), "foundation comparison")

output = {"checks": checks, "passed": sum(c["met"] for c in checks), "total": len(checks),
          "source_counts": dict(counts), "counted_originals": len(counted),
          "limitations": "Structural/data checks only. Unknown chronology, causality, historical deployment, and missing primary records stay unknown."}
print(json.dumps(output, ensure_ascii=False, indent=2))
sys.exit(0 if all(c["met"] for c in checks) else 1)
