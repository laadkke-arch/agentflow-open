#!/usr/bin/env python3
"""AF-RES-009 documentation integrity gate. No network, no product execution."""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OWNED = Path("docs/workstreams/research/AF-RES-009")
SOURCE = "50ebddbc28a756a4c886184d0f56a0f648e19145"
SOURCE_FIELDS = {"id", "url", "accessed_at_utc", "source_type", "title",
                 "version_or_date", "sections_read", "confirmed", "limits",
                 "level", "used_in"}
SYSTEM_FIELDS = {"id", "name", "category", "status", "input", "corpus_scope",
                 "collection_method", "data_license", "representation",
                 "retrieval", "explanation_of_results", "maintenance",
                 "business_or_funding", "part_or_crossdomain_capability",
                 "evidence", "unknowns"}
DIMENSIONS = {"structure_part_input", "component_link", "crossdomain_principle",
              "link_explanation", "evidence_maintenance"}
VERDICTS = {"이미 충족", "부분 충족", "비어 있음"}

def git(*args):
    return subprocess.check_output(["git", *args], text=True).rstrip("\n")

def utc(value):
    dt = datetime.fromisoformat(value.replace(" UTC", "+00:00").replace("Z", "+00:00"))
    assert dt.utcoffset() is not None and dt.utcoffset().total_seconds() == 0, value
    return dt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["pre-handoff", "final"], required=True)
    parser.add_argument("--write-report")
    args = parser.parse_args()
    root = Path(git("rev-parse", "--show-toplevel"))
    folder = root / OWNED
    def read(name):
        return json.loads((folder / name).read_text(encoding="utf-8"))
    checks = []
    def check(name, condition, detail=None):
        checks.append({"check": name, "pass": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(name + ": " + str(detail))
    required = ["SCOPE.md", "sources.json", "SYSTEMS.json", "LANDSCAPE.md",
                "FAILURES.md", "GAP.md", "SEARCH_LOG.json", "SELF_CHECK.md",
                "SELF_CHECK.json", "REVIEW.md"]
    if args.stage == "final":
        required += ["HANDOFF.md", "VERIFICATION.json"]
    check("required_files", all((folder / f).is_file() for f in required), required)
    sd, yd, ld, sc = read("sources.json"), read("SYSTEMS.json"), read("SEARCH_LOG.json"), read("SELF_CHECK.json")
    check("source_commit_fixed", all(d["source_commit"] == SOURCE for d in [sd, yd, ld, sc]))
    sources, systems, queries = sd["sources"], yd["systems"], ld["queries"]
    sid = {s["id"]: s for s in sources}
    qid = {q["id"]: q for q in queries}
    check("source_ids_unique", len(sid) == len(sources), len(sources))
    check("system_ids_unique", len({s["id"] for s in systems}) == len(systems))
    check("query_ids_unique", len(qid) == len(queries), len(queries))
    check("source_urls_unique", len({s["url"] for s in sources}) == len(sources))
    for s in sources:
        check("source_fields:" + s["id"], SOURCE_FIELDS <= set(s) and all(s[k] for k in SOURCE_FIELDS))
        check("source_level:" + s["id"], s["level"] in {"D1", "D2", "D3"})
        check("source_url:" + s["id"], s["url"].startswith("https://"))
        utc(s["accessed_at_utc"])
    external = [s for s in sources if s.get("primary")]
    counted = [s for s in external if s.get("counted")]
    groups = Counter(s["counting_group"] for s in counted)
    check("source_minimum", len(counted) >= 30, len(counted))
    check("per_system_source_cap", max(groups.values()) <= 3, dict(groups))
    official = [s for s in counted if "official_doc" in s.get("tags", [])]
    check("official_minimum", len(official) >= 15, len(official))
    check("strict_engineering_minimum", len(sc["strict_engineering_sources"]) >= 6)
    for key in ["strict_engineering_sources", "strict_failure_sources", "evaluation_sources"]:
        check("distinct:" + key, len(sc[key]) == len(set(sc[key])))
        for source_id in sc[key]:
            check(key + ":" + source_id, source_id in sid and sid[source_id].get("primary") and sid[source_id].get("counted"))
    check("strict_failure_minimum", len(sc["strict_failure_sources"]) >= 6)
    check("evaluation_minimum", len(sc["evaluation_sources"]) >= 3)
    for source_id in sc["evaluation_sources"]:
        check("evaluation_type:" + source_id, sid[source_id]["source_type"] in {"peer_reviewed_evaluation", "original_institutional_evaluation"})
    categories = Counter(s["category"] for s in systems)
    check("system_minimum", len(systems) >= 25, len(systems))
    check("seven_categories", set(categories) == set("abcdefg") and min(categories.values()) >= 3, dict(categories))
    gap = (folder / "GAP.md").read_text(encoding="utf-8")
    for s in systems:
        check("system_fields:" + s["id"], SYSTEM_FIELDS <= set(s) and all(s[k] for k in SYSTEM_FIELDS))
        check("status:" + s["id"], s["status"]["value"] in {"운영", "종료", "쇠퇴", "불명"} and bool(s["status"]["basis"]))
        check("system_evidence:" + s["id"], set(s["evidence"]) <= set(sid) and any(sid[x].get("primary") for x in s["evidence"]))
        check("assessment:" + s["id"], set(s["value_assessment"]) == DIMENSIONS and set(s["value_assessment"].values()) <= VERDICTS)
        check("assessment_evidence:" + s["id"], bool(s["assessment_evidence"]) and set(s["assessment_evidence"]) <= set(sid))
        display_name = s["name"].replace(" 및 기여 규칙", "")
        check("gap_row:" + s["id"], ("| " + display_name + " |") in gap)
    check("d1_boundary", all(s["level"] == "D1" for s in external))
    check("no_fabricated_public_queries", ld["public_system_queries"] == [])
    for q in queries:
        check("query_fields:" + q["id"], all(q.get(k) for k in ["query", "at_utc", "tool", "observed_results"]))
        utc(q["at_utc"])
        check("query_links:" + q["id"], set(q["opened_source_ids"]) <= set(sid))
    cases = sd["failure_cases"]
    core = [f for f in cases if f["count_toward_minimum"]]
    check("core_failure_minimum", len(core) >= 6 and len({f["system"] for f in core}) >= 6, len(core))
    for f in cases:
        check("failure_primary:" + f["id"], set(f["source_ids"]) <= set(sid) and any(sid[x].get("primary") for x in f["source_ids"]))
        check("failure_reason_H:" + f["id"], bool(f["official_reason"]) and f["hypothesis_H"].startswith("H:"))
        check("failure_quote_limit:" + f["id"], f["quote_words"] <= 25)
    check("questions_complete", {q["id"] for q in sc["questions"]} == {"Q" + str(i) for i in range(1, 9)})
    for q in sc["questions"]:
        check("question_types:" + q["id"], len(q["kinds"]) >= 2, list(q["kinds"]))
        linked = set(x for values in q["kinds"].values() for x in values)
        check("question_primary:" + q["id"], linked <= set(sid) and all(sid[x].get("primary") for x in linked))
        check("question_used_in:" + q["id"], all(q["id"] in sid[x]["used_in"] for x in linked))
        check("question_counter:" + q["id"], bool(q["counterqueries"]) and set(q["counterqueries"]) <= set(qid) and bool(q["counter_result"]))
        check("question_counter_sources:" + q["id"], bool(q["counter_sources"]) and set(q["counter_sources"]) <= set(sid))
        check("question_uncertainty:" + q["id"], bool(q["uncertainty"]) and bool(q["minimum_next_check"]))
    for path in folder.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        cited = set(re.findall(r"\[((?:S-[A-Z]+\d+)|(?:I-[A-Z]+))\]", text))
        check("markdown_refs:" + path.name, cited <= set(sid), sorted(cited - set(sid)))
        definitions = dict(re.findall(r"^\[((?:S-[A-Z]+\d+)|(?:I-[A-Z]+))\]: (https://\S+)$", text, flags=re.M))
        check("markdown_urls:" + path.name, all(sid[k]["url"] == v for k, v in definitions.items()))
    check("excluded_not_counted", not any(x.get("counted", False) for x in sd["excluded"]), len(sd["excluded"]))
    counts = {
        "external_read": len(external), "counted_external": len(counted),
        "official_docs": len(official),
        "engineering_or_research": sum(any(t in {"engineering", "research"} for t in s.get("tags", [])) for s in counted),
        "failure_primary_sources": sum("failure" in s.get("tags", []) for s in counted),
        "evaluation_studies": len(sc["evaluation_sources"]), "systems": len(systems),
        "categories": dict(sorted(categories.items())), "searches": len(queries),
        "excluded": len(sd["excluded"]), "core_failures": len(core),
        "strict_engineering_articles_or_papers": len(sc["strict_engineering_sources"]),
        "strict_failure_sources": len(sc["strict_failure_sources"])
    }
    check("reported_counts_match", sd["counts"] == counts, counts)
    changed = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    check("committed_owned_path", bool(changed) and all(p.startswith(str(OWNED) + "/") for p in changed), changed)
    check("control_unchanged", git("rev-parse", SOURCE + ":docs/automation/dot-control.json") == git("rev-parse", "HEAD:docs/automation/dot-control.json"))
    work = git("status", "--porcelain").splitlines()
    check("working_changes_owned", all(line[3:].startswith(str(OWNED) + "/") for line in work), work)
    if args.stage == "final":
        check("worktree_clean", not work, work)
        last_paths = git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD").splitlines()
        check("handoff_only_final_commit", last_paths == [str(OWNED / "HANDOFF.md")], last_paths)
        check("local_remote_equal", git("rev-parse", "HEAD") == git("rev-parse", "origin/work/research-af-res-009"))
    stable = ["SCOPE.md", "sources.json", "SYSTEMS.json", "SEARCH_LOG.json", "FAILURES.md", "LANDSCAPE.md", "GAP.md"]
    hashes = {name: hashlib.sha256((folder / name).read_bytes()).hexdigest() for name in stable}
    if args.stage == "final":
        check("pre_handoff_evidence_unchanged", read("VERIFICATION.json")["sha256"] == hashes)
    report = {
        "task_id": "AF-RES-009", "stage": args.stage, "result": "PASS",
        "checked_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_commit": SOURCE, "head_at_check": git("rev-parse", "HEAD"),
        "counts": counts, "check_count": len(checks),
        "checks": checks,
        "sha256": hashes,
        "limits": "Metadata and commit-boundary verification only; not D3 product execution or D4 utility validation."
    }
    if args.write_report:
        dest = (root / args.write_report).resolve()
        check("report_owned_path", dest.is_relative_to(folder.resolve()), str(dest))
        report["check_count"] = len(checks)
        dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["stage", "result", "checked_at_utc", "head_at_check", "counts", "check_count"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

