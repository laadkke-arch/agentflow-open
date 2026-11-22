"""Read-only ledger checks; writes only the local validation report."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json

BASE = Path(__file__).resolve().parent
sources = json.loads((BASE / "sources.json").read_text())
decisions = [json.loads(line) for line in (BASE / "decisions.jsonl").read_text().splitlines() if line.strip()]
with (BASE / "sampling.csv").open(newline="") as handle:
    sampling = list(csv.DictReader(handle))
with (BASE / "costs.csv").open(newline="") as handle:
    costs = list(csv.DictReader(handle))
searches = json.loads((BASE / "search-log.json").read_text())
required_source = {"source_id", "case_ids", "questions", "url", "published_or_version", "checked_utc",
                   "location", "observed", "limitation", "evidence_kind", "lineage",
                   "count_category", "count_in_minimum", "access"}
required_decision = {"id", "sample", "record_family", "project", "title", "screening_order",
                     "original_url", "need", "first_public_implementation", "alternatives",
                     "awareness", "decision", "implementation", "initial_choice", "final_choice",
                     "outcome", "competing_explanations", "unknowns", "minimum_next_record",
                     "followup_search_scope", "source_ids", "linked_A_id", "duplicate_017",
                     "connected_chain", "strict_discovery_change", "causal_statement_url",
                     "later_available", "awareness_unknown", "cost_ids"}
checks = []
def check(name, met, note=""):
    checks.append({"condition": name, "met": bool(met), "note": note})

source_ids = {source["source_id"] for source in sources}
case_ids = {decision["id"] for decision in decisions}
cost_ids = {cost["cost_id"] for cost in costs}
check("unique source IDs", len(source_ids) == len(sources))
check("unique B choices", len(case_ids) == len(decisions) == 9)
check("required source fields", all(required_source <= set(source) for source in sources))
check("required decision fields", all(required_decision <= set(decision) for decision in decisions))
check("all cited sources exist", all(set(decision["source_ids"]) <= source_ids for decision in decisions))
check("nested source references exist", all(set(record.get("source_ids", [])) <= source_ids
      for decision in decisions for field in ("alternatives", "awareness") for record in decision[field]))
check("all cost references exist", all(set(decision["cost_ids"]) <= cost_ids for decision in decisions))
check("all costs belong to a B choice", all(cost["case_id"] in case_ids for cost in costs))
check("one included sampling row per choice",
      Counter(row["case_id"] for row in sampling if row["included"].lower() == "true") == Counter(case_ids))
check("no counted blocked/search-only sources", all(source["access"] == "direct_full_or_selected_section"
      for source in sources if source["count_in_minimum"]))
counted = [source for source in sources if source["count_in_minimum"]]
check("counted URLs unique", len({source["url"] for source in counted}) == len(counted))
check("strict change is subset of connected chain", all(not decision["strict_discovery_change"]
      or decision["connected_chain"] for decision in decisions))
b09 = next(decision for decision in decisions if decision["id"] == "B09")
check("B09 dated example does not imply operational implementation",
      b09["dated_example_chain"] is True and b09["connected_chain"] is False and
      b09["date_fixed_connected_chain"] is False and b09["implementation"]["date"] == "2023-02-09T03:11:41Z")
check("original public choice window", all("2018" <= decision["need"]["date"][:4] <= "2024" for decision in decisions))
check("per-project cap 2", max(Counter(decision["project"] for decision in decisions).values()) <= 2)
grid_routes = searches["counterexample_query_grid"]["route_keys"]
grid_groups = [group for group in searches["search_groups"] if group["route"] in grid_routes]
check("negative query grid is six groups of three", len(grid_groups) == 6 and
      all(len(group["queries"]) == 3 for group in grid_groups))
check("all actor statements retain uncertainty fields", all(decision["unknowns"] and
      decision["minimum_next_record"] for decision in decisions))
check("no A or 017 choices reused", all(decision["linked_A_id"] is None and
      decision["duplicate_017"] is False for decision in decisions),
      "Manual case/topic comparison also performed; common SQLAlchemy ecosystem is not a shared team-choice.")

stats = {
    "B_unique": len(decisions),
    "B_record_families": dict(Counter(decision["record_family"] for decision in decisions)),
    "source_ledger_rows": len(sources),
    "counted_external_originals": len(counted),
    "count_categories": dict(Counter(source["count_category"] for source in counted)),
    "excluded_from_source_minimum": len(sources) - len(counted),
    "sampling_search_candidate_urls": len(sampling),
    "sampling_included": sum(row["included"].lower() == "true" for row in sampling),
    "sampling_direct_read_excluded": sum(row["included"].lower() != "true" and
          row["access"] == "direct_full_or_selected_section" for row in sampling),
    "sampling_blocked_candidates": sum(row["access"] == "blocked" for row in sampling),
    "sampling_prior_017_duplicates": sum(row["duplicate_id"].startswith("AF-RES-017/") for row in sampling),
    "sampling_search_only_not_selected": sum(row["access"] == "search_only" for row in sampling),
    "connected_chain_ids": [decision["id"] for decision in decisions if decision["connected_chain"]],
    "date_fixed_connected_chain_ids": [decision["id"] for decision in decisions if decision["date_fixed_connected_chain"]],
    "dated_example_chain_ids": [decision["id"] for decision in decisions if decision.get("dated_example_chain", False)],
    "strict_discovery_change_ids": [decision["id"] for decision in decisions if decision["strict_discovery_change"]],
    "outcome_counts": dict(Counter(decision["outcome"] for decision in decisions)),
    "later_available_ids": [decision["id"] for decision in decisions if decision["later_available"]],
    "cost_rows": len(costs),
    "cost_kind_counts": dict(Counter(cost["cost_kind"] for cost in costs)),
    "measured_causal_saving_cases": 0,
    "cost_total": None,
    "cost_total_note": "Units/scopes differ and causal attribution is absent; no total calculated."
}
files = ["sources.json", "decisions.jsonl", "sampling.csv", "costs.csv", "analysis.md",
         "search-log.json", "recruitment-plan.json", "prior-duplicate-exclusions.json", "b09-git-audit.json", "verify.py"]
report = {
    "checked_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "command": "python docs/workstreams/research/AF-RES-022/streams/b/verify.py",
    "all_metadata_checks_passed": all(item["met"] for item in checks),
    "checks": checks, "statistics": stats,
    "sha256": {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in files},
    "limits": [
        "These checks validate the local ledger, not every historical claim or external URL's future availability.",
        "No external project code, database, vehicle, browser polyfill, or uploaded example was executed.",
        "B09 revision date is fixed by public Git; only educational artifact retention is established, not operational implementation.",
        "Six strict connected cases and three strict production late-retention cases were not forced into the data."
    ]
}
(BASE / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"all_metadata_checks_passed": report["all_metadata_checks_passed"], "statistics": stats}, ensure_ascii=False))
if not report["all_metadata_checks_passed"]:
    raise SystemExit(1)
