"""Check AF-RES-073 evidence integrity, not external truth or task completion.

Only reads files and Git state; emits a JSON receipt on stdout. No network.
Run from any working directory. Exit 0 means the stored evidence is internally
consistent; the independently reported completion status remains PARTIAL.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
import re
import subprocess
import sys

P = Path(__file__).resolve().parent.parent
ROOT = P.parents[3]
PREFIX = P.relative_to(ROOT).as_posix() + "/"
checks = []


def check(name, condition, detail=None):
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


def jl(name):
    return [json.loads(s) for s in (P / name).read_text().splitlines() if s.strip()]


def csv_rows(name):
    with (P / name).open(newline="") as f:
        values = list(csv.reader(f))
    check("CSV rectangular: " + name, len(values) > 1 and all(len(v) == len(values[0]) for v in values), {"rows": len(values) - 1, "columns": len(values[0])})
    return [dict(zip(values[0], row)) for row in values[1:]]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def utc(s):
    if s.endswith(" UTC"):
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def table_rows(section):
    lines = [x for x in section.splitlines() if x.startswith("| ")]
    return lines[2:] if len(lines) >= 2 else []


manifest = json.loads((P / "manifest.json").read_text())
counts = json.loads((P / "evidence/normalized-counts.json").read_text())
acceptance = json.loads((P / "evidence/acceptance-evidence.json").read_text())
seal = json.loads((P / "evidence/original-seal.json").read_text())
queries = jl("queries.jsonl")
proposals = jl("proposals.jsonl")
runs = jl("runs.jsonl")
sources = jl("sources.jsonl")
judgments = csv_rows("judgments.csv")
decisions = csv_rows("decisions.csv")
frame = csv_rows("frame.csv")
mapping = csv_rows("evidence/query-mapping.csv")
semantic = csv_rows("evidence/semantic-overlap.csv")
src = {s["source_id"]: s for s in sources}
query = {q["query_id"]: q for q in queries}
events = {r["event_id"]: r for r in runs}
rank = {r["event_id"]: r for r in runs if r["kind"] == "rank"}
judgment = {j["rank_id"]: j for j in judgments}
searches = [r for r in runs if r["kind"] == "search"]
documents = [r for r in runs if r["kind"] in {"open", "find", "screenshot"}]

for name, rows, key in [("sources", sources, "source_id"), ("runs", runs, "event_id"), ("queries", queries, "query_id"), ("judgments", judgments, "rank_id"), ("decisions", decisions, "decision_id")]:
    check("Unique nonempty keys: " + name, len({r[key] for r in rows}) == len(rows) and all(r[key] for r in rows), len(rows))
check("3 actual sealed proposal inputs, 2 repositories", len(proposals) == 3 and len({p["project"] for p in proposals}) == 2)
check("Recruitment frame 17 rows; MEP vacancy explicit", len(frame) == 17 and Counter(r["repository"] for r in frame) == {"matplotlib/matplotlib": 1, "jupyter/enhancement-proposals": 8, "scientific-python/specs": 8}, dict(Counter(r["repository"] for r in frame)))
check("18 queries and 18 complete query mappings", len(query) == 18 and {m["query_id"] for m in mapping} == set(query))
check("90 slots and judgments have exact same keys", len(rank) == 90 and set(rank) == set(judgment))
check("18 original searches, 52 document operations, 70 charged operations", len(searches) == 18 and len(documents) == 52 and sum(r["cost"] for r in runs) == 70)
check("166 original events retain zero-cost skips/stops", len(runs) == 166 and Counter(r["kind"] for r in runs) == {"search": 18, "rank": 90, "open": 52, "skip": 5, "stop": 1})
check("Only original experiment in normalized runs", all(r["phase"] == "original_experiment" for r in runs))
check("5 original ranks per query", all(sorted(int(r["rank"]) for r in rank.values() if r["query_id"] == q) == [1, 2, 3, 4, 5] for q in query))
check("Executed queries exactly match preregistration", all(r["query"] == query[r["query_id"]]["query"] for r in searches))
check("All search calls after published query seal", all(utc(r["started_utc"]) > utc(seal["query_seal_commit_utc"]) for r in searches))
check("Fixed tool/language/recency/domain settings", all(q["tool"] == "system1_search_query" and q["language"] == "English" and q["domains"] is None and q["recency"] is None and q["response_length"] == "long" for q in queries))

arms = {}
for p in ("P1", "P2", "P3"):
    for a in "ABC":
        rr = [r for r in runs if r["proposal_id"] == p and r["arm"] == a]
        ops = [r for r in rr if r["cost"]]
        arms[p + a] = sum(r["cost"] for r in ops)
        check("Budget and continuous cumulative cost " + p + a, sum(r["kind"] == "search" for r in rr) == 2 and sum(r["kind"] == "open" for r in rr) <= 6 and sorted(r["cumulative_cost"] for r in ops) == list(range(1, len(ops) + 1)), {"cost": arms[p + a]})
        check("Two searches precede document operations " + p + a, all(r["cumulative_cost"] in {1, 2} for r in rr if r["kind"] == "search") and all(r["cumulative_cost"] >= 3 for r in rr if r["kind"] == "open"))
    ordered = sorted("ABC", key=lambda a: min(utc(r["started_utc"]) for r in searches if r["proposal_id"] == p and r["arm"] == a))
    check("Rotating arm order " + p, "".join(ordered) == {"P1": "ABC", "P2": "BCA", "P3": "CAB"}[p], "".join(ordered))
check("Actual arm totals", arms == {"P1A": 7, "P1B": 8, "P1C": 8, "P2A": 7, "P2B": 8, "P2C": 8, "P3A": 8, "P3B": 8, "P3C": 8}, arms)

check("All 52 document operations link original sources", all(r["source_id"] in src and src[r["source_id"]]["phase"] == "original_experiment" for r in documents))
opmap = {r["event_id"]: r for r in documents}
for j in judgments:
    if j["source_id"]:
        check("Rank source and read-cost join " + j["rank_id"], j["source_id"] in src and j["operation_id"] in opmap and opmap[j["operation_id"]]["source_id"] == j["source_id"] and str(opmap[j["operation_id"]]["cumulative_cost"]) == j["reading_cumulative_cost"])
    else:
        check("No invented read cost " + j["rank_id"], j["reading_cumulative_cost"] == "" and j["direct_original_read"].lower() == "false")
    check("Rank query and prefix join " + j["rank_id"], j["actual_query"] == query[j["query_id"]]["query"] and int(j["common_prefix"]) == min(arms[j["proposal_id"] + a] for a in "ABC") and int(j["search_cumulative_cost"]) in {1, 2})

required = ["source_id", "independent_work_id", "original_url", "landed_url", "author_publisher", "version_time", "checked_utc", "read_sections", "concrete_findings", "supports", "limitations_counterevidence", "access_status", "count_reason"]
missing = [(s["source_id"], k) for s in sources for k in required if not s.get(k)]
check("Every source has mandatory provenance/findings/limits fields", not missing, missing)
check("Every source URL uses a real web address", all(s["original_url"].startswith(("https://", "http://")) and s["landed_url"].startswith(("https://", "http://")) for s in sources))
representatives = [s for s in sources if s["minimum_count_representative"]]
works = {s["independent_work_id"] for s in sources if s["count_eligible"]}
check("Minimum count only directly read originals", all(s["direct_original_read"] for s in representatives) and len(representatives) == len(works) == counts["independent_original_works"] == 43, {"works": len(works), "representatives": len(representatives)})
check("At least22 independent original works", len(works) >= 22)
check("108 source rows", len(sources) == counts["source_rows"] == 108)
check("43 original primary document operations", sum(src[r["source_id"]]["direct_original_read"] for r in documents) == 43)
check("46 primary-linked ranks, including3 reuses", sum(j["direct_original_read"].lower() == "true" for j in judgments) == counts["direct_original_rank_slots"] == 46)
check("22 budget-unread slots", sum("unread_budget" in j["read_status"] for j in judgments) == 22)
check("0 qualified is observed, application success undefined", not any(j["qualified_design"].lower() == "true" for j in judgments) and counts["qualified_design_slots"] == 0 and counts["target_application_trials"] == 0 and counts["target_application_success_rate"] is None)
check("First qualified cost is null in every arm", all(r["first_qualified_cost"] is None for a in counts["arms"].values() for r in a.values()))
check("23 postseal decisions; no retroactive score change", len(decisions) == 23 and all(d["phase"] == "postseal" and d["original_score_changed"].lower() == "false" for d in decisions))
post = json.loads((P / "evidence/postseal-costs.json").read_text())
check("62 postseal operations separate from original70", post["totals"]["operation_rows"] == post["totals"]["operation_cost"] == 62 and sum(post["totals"]["category_costs"].values()) == 62 and post["phase"] == "postseal_only")

raw_mismatch = [x["path"] for x in seal["raw_files"] if hashlib.sha256((P / x["path"]).read_bytes()).hexdigest() != x["sha256"]]
check("All27 original raw seals intact", len(seal["raw_files"]) == 27 and not raw_mismatch, raw_mismatch)
seal_diff = git("diff", seal["query_seal"], "--", PREFIX + "queries.jsonl", PREFIX + "proposals.jsonl")
check("Sealed queries and proposal inputs unchanged", seal_diff == "")

result = (P / "RESULT.md").read_text()
sections = re.split(r"(?m)^## ", result)
check("First three content sections are required tables", [s.splitlines()[0] for s in sections[1:4]] == ["표 1. 모집과 실제 고정 입력", "표 2. 모든 반환 자리와 판독·판정·비용", "표 3. 동일 누적 연산에서의 적격과 다음 행동"])
check("Required table data rows3/90/3", [len(table_rows(s)) for s in sections[1:4]] == [3, 90, 3])
table2 = "\n".join(table_rows(sections[2]))
check("Every rank/source address/query appears in table2", all(j["rank_id"] in table2 and j["actual_query"].replace("|", "&#124;") in table2 and (j["landed_url"] or j["original_url"]) in table2 for j in judgments))
check("Q1 through Q8 answered in RESULT and SELF_CHECK", all("## Q" + str(i) + "." in result and "Q" + str(i) in (P / "SELF_CHECK.md").read_text() for i in range(1, 9)))
last_section = sections[-1]
check("Last table has exactly3 weaknesses", last_section.startswith("가장 중요한 불일치·약점") and len(table_rows(last_section)) == 3 and all("| W" + str(i) + " |" in last_section for i in (1, 2, 3)))
check("PARTIAL status preserves failed origin criterion", acceptance["status"] == "PARTIAL" and acceptance["completion_criteria"]["three_eligible_foundational_versions"]["met"] is False and "PARTIAL" in result)

changed = [s for s in git("diff", "--name-only", manifest["base_commit"]).splitlines() if s]
untracked = [s for s in git("ls-files", "--others", "--exclude-standard").splitlines() if s]
outside = [s for s in changed + untracked if not s.startswith(PREFIX)]
check("All changes and untracked deliverables are within owned path", not outside, outside)
check("Central dot-control and base rules unchanged", not git("diff", manifest["base_commit"], "--", "docs/automation/dot-control.json", "AGENTS.md", "STATE.md", "docs/DOT_AUTOMATION.md", "docs/RESEARCH_WORKFLOW.md"))
check("Manifest fixes only assigned dependency", manifest["allowed_paths"] == [PREFIX] and manifest["dependencies"] == [{"branch": "work/research-af-res-069", "commit": "616a1dab1b7d3ff8ff14210316c251cd5e5727b7"}])

input_files = ["manifest.json", "frame.csv", "proposals.jsonl", "queries.jsonl", "runs.jsonl", "sources.jsonl", "judgments.csv", "decisions.csv", "RESULT.md", "SELF_CHECK.md", "evidence/acceptance-evidence.json", "evidence/normalized-counts.json", "evidence/original-seal.json", "evidence/postseal-costs.json", "evidence/normalize.py", "evidence/build-report.py", "evidence/verify.py"]
failed = [c for c in checks if not c["passed"]]
receipt = {"task_id": "AF-RES-073", "checker": "local Python standard-library evidence checker; no external truth test", "actor": "root research agent in actual checkout", "checked_utc": datetime.now(timezone.utc).isoformat(), "checked_head": git("rev-parse", "HEAD"), "branch": git("branch", "--show-current"), "working_tree_clean": not git("status", "--porcelain"), "status": "passed" if not failed else "failed", "exit_code": 0 if not failed else 1, "completion_status": "PARTIAL", "check_count": len(checks), "failed_checks": failed, "input_sha256": {f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in input_files}, "checks": checks}
print(json.dumps(receipt, ensure_ascii=False, indent=2))
sys.exit(receipt["exit_code"])
