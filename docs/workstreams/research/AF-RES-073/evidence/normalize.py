"""Normalize recorded AF-RES-073 ledgers; never fetch or infer unread evidence."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter, defaultdict
from urllib.parse import urlsplit, urlunsplit

P = Path(__file__).resolve().parent.parent


def read_jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def pick(row, *keys, default=""):
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return default


def truth(value):
    return value is True or str(value).lower() in {"true", "yes", "1"}


def joined(value):
    return "; ".join(map(str, value)) if isinstance(value, list) else str(value)


def listed(value):
    if value in (None, ""):
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [part.strip() for part in str(value).split(";") if part.strip()]


def source_classification(row, sid):
    """Classify observed content, independently of minimum-count eligibility.

    An API transport can return an original body/patch or merely a commit list.
    Conversely, an original document may be excluded from the minimum because
    it is a repeated version or an incidental recruitment-control read.
    """
    status = pick(row, "access_status", "status")
    url = pick(row, "landed_url", "actual_url", "original_url", "url")
    if status.startswith("access_failed"):
        return False, False, "access_failure", "No original body was returned."
    if status == "redirect_notice_only":
        return False, False, "redirect_notice", "Only a redirect notice was read; destination unread."
    if status == "rewritten_summary_only":
        return False, False, "rewritten_summary", "Returned rewrite is not direct reading of the original body."
    if status == "metadata_empty":
        return False, True, "metadata_only", "An issuer metadata request returned no substantive body."
    if status == "read_secondary_or_mirror":
        return True, False, "secondary_or_mirror", "Body read, but original publisher/instrument not directly verified."
    if sid == "P3-B-O6":
        return True, False, "fictional_examples_and_secondary_technical_explanation", "Raw limitations identify fictional teaching cases and secondary technical explanations; no primary operational/technical proof."
    if status == "direct_read_api" and urlsplit(url).path.endswith("/commits"):
        return False, True, "metadata_only", "Commit collection was read for chronology; original blob/patch is recorded separately."
    body_read = status in {"direct_read", "read", "read_original", "direct_read_api"}
    if "direct_read" in row:
        body_read = truth(row["direct_read"])
    primary = truth(row["primary_source"]) if "primary_source" in row else body_read
    kind = "original_api_body_or_patch" if status == "direct_read_api" else "original_body_or_record"
    return body_read, primary, kind, "Publisher body/record read; minimum-count exclusion and repeated-version status are separate."


def canonical_work(value):
    # Deliberately conservative cross-worker family merges. They never create
    # a qualifying candidate, and reported IDs stay in the normalized record.
    if value in {"ONES-HANDOFF-GUIDANCE-2026", "ONES-approval-workflow-guidance"}:
        return "ONES-workflow-guidance"
    if value in {"Scientific-Python-project-governance", "SPEC-Steering-Committee-governance", "Scientific-Python-code-of-conduct"}:
        return "Scientific-Python-governance-and-conduct"
    if value in {"SPEC9-governance", "SPEC-0009", "SPEC-9"}:
        return "SPEC-9"
    if value == "nbformat-relax-add-props-343":
        return "jupyter-nbformat-reference-implementation"
    return value


def norm_url(url):
    if not url:
        return ""
    u = urlsplit(url)
    return urlunsplit((u.scheme.lower(), u.netloc.lower(), u.path.rstrip("/"), u.query, ""))


queries = {r["query_id"]: r for r in read_jsonl(P / "queries.jsonl")}
sources = []
source_paths = [P / "recruitment/jep/sources.jsonl", P / "recruitment/spec/sources.jsonl", P / "recruitment/mep/source.jsonl"]
run_paths = []
for arm in "ABC":
    source_paths += [P / f"experiment/P1/arm-{arm}-sources.jsonl", P / f"experiment/P2/{arm}-sources.jsonl", P / f"experiment/P3/{arm}/sources.jsonl"]
    run_paths += [P / f"experiment/P1/arm-{arm}-runs.jsonl", P / f"experiment/P2/{arm}-runs.jsonl", P / f"experiment/P3/{arm}/runs.jsonl"]
source_paths += sorted((P / "postseal").glob("*/sources.jsonl")) if (P / "postseal").exists() else []
for path in source_paths:
    for r in read_jsonl(path):
        sid = pick(r, "source_id", "id")
        assert sid, str(path)
        raw_work = pick(r, "independent_work_id", "work_id", default=sid)
        allow = pick(r, "count_eligible", "count_independent", "count_toward_minimum", "counts_toward_minimum", default=path.parent.name == "jep")
        phase = pick(r, "phase", default="postseal" if "postseal" in path.parts else "recruitment")
        if phase in {"experiment", "original_experiment"}:
            phase = "original_experiment"
        body_read, primary, source_kind, classification_basis = source_classification(r, sid)
        operation_ids = listed(pick(r, "operation_ids", "operation_id", "open_id", default=[]))
        read_sections = joined(pick(r, "read_sections", "sections"))
        if not read_sections and not body_read:
            read_sections = "No original sections read; " + pick(r, "access_status", "status")
        s = {
            "source_id": sid, "independent_work_id": canonical_work(raw_work), "reported_work_id": raw_work,
            "phase": phase, "proposal_id": pick(r, "proposal_id"), "arm": pick(r, "arm"),
            "original_url": pick(r, "original_url", "url"), "landed_url": pick(r, "landed_url", "actual_url", "original_url", "url"),
            "author_publisher": pick(r, "author_publisher", "publisher", "author"),
            "version_time": pick(r, "version_time", "version"),
            "checked_utc": pick(r, "checked_utc", "verified_utc", "accessed_utc"),
            "read_sections": read_sections,
            "concrete_findings": joined(pick(r, "concrete_findings", "verified_content", "findings")),
            "supports": pick(r, "supports", "question_claims", "claims", default=[]),
            "limitations_counterevidence": joined(pick(r, "limitations_counterevidence", "limits_counterevidence", "limitations", "limits")),
            "access_status": pick(r, "access_status", "status"),
            "count_eligible": truth(allow),
            "count_reason": pick(r, "count_reason", "minimum_count_reason"),
            "evidence_ref": joined(pick(r, "evidence_ref", "response_ref", "source_ref")),
            "origin_rank_ids": pick(r, "origin_rank_ids", default=[r["rank_id"]] if "rank_id" in r else []),
            "operation_id": joined(operation_ids), "operation_ids": operation_ids,
            "independent_event_id": pick(r, "independent_event_id", "event_id"),
            "direct_body_read": body_read, "primary_source": primary,
            "direct_original_read": body_read and primary,
            "source_kind": source_kind, "classification_basis": classification_basis,
            "reported_direct_read": r.get("direct_read"), "reported_primary_source": r.get("primary_source"),
            "original_url_status": r.get("original_url_status", ""),
            "publication_date": r.get("publication_date", ""),
            "author_prior_awareness": r.get("author_prior_awareness", ""),
            "existed_at_decision": r.get("existed_at_decision", ""),
            "commit_sha": r.get("commit_sha", ""), "blob_sha": r.get("blob_sha", ""),
            "merge_commit_sha": r.get("merge_commit_sha", ""), "patch_head_sha": r.get("patch_head_sha", ""),
            "condition_assessment": r.get("condition_assessment", {}),
            "record_file": str(path.relative_to(P)),
            "reader": "root" if "cross-domain" in path.parts else "same-model delegate; see record_file",
        }
        sources.append(s)
assert len({s["source_id"] for s in sources}) == len(sources), "duplicate source ID"
src = {s["source_id"]: s for s in sources}
counted_works = {s["independent_work_id"] for s in sources if s["count_eligible"]}
minimum_representatives = {}
for s in sources:
    if s["count_eligible"]:
        assert s["direct_original_read"], (s["source_id"], "minimum count requires a directly read primary body")
        minimum_representatives.setdefault(s["independent_work_id"], s["source_id"])
for s in sources:
    representative = minimum_representatives.get(s["independent_work_id"], "")
    s["minimum_count_source_id"] = representative
    s["minimum_count_representative"] = s["source_id"] == representative
    s["counting_adjustment"] = "Patch/release event retained separately; no additional independent work beyond nbformat implementation." if s["reported_work_id"] == "nbformat-relax-add-props-343" else ""

runs = []
for path in run_paths:
    for r in read_jsonl(path):
        kind = pick(r, "kind", "event", "type")
        eid = pick(r, "event_id", "id")
        assert eid and kind
        qid = pick(r, "query_id", default=eid if kind == "search" else "")
        if not qid and kind == "rank":
            qid = eid.rsplit("-R", 1)[0]
        rankid = eid if kind == "rank" else pick(r, "rank_id")
        sourceid = pick(r, "source_id")
        if kind in {"open", "find", "screenshot"} and not sourceid:
            choices = [s for s in sources if s["phase"] == "original_experiment" and (eid in s["operation_ids"] or s["source_id"] == eid or rankid in s["origin_rank_ids"])]
            if len(choices) == 1:
                sourceid = choices[0]["source_id"]
        event = {
            "event_id": eid, "phase": "original_experiment", "kind": kind,
            "proposal_id": r["proposal_id"], "arm": r["arm"], "query_id": qid, "rank_id": rankid,
            "query": pick(r, "query", default=queries.get(qid, {}).get("query", "")),
            "rank": pick(r, "rank", "returned_position", default=None) if kind == "rank" else None,
            "title": pick(r, "title"), "url": pick(r, "url", "requested_url"),
            "landed_url": pick(r, "landed_url", "url", "requested_url"),
            "tool_ref": pick(r, "ref", "ref_id", "evidence_ref", "response_ref", "source_ref"),
            "source_id": sourceid, "status": pick(r, "status", "access_status"),
            "started_utc": pick(r, "started_utc", "checked_utc"), "ended_utc": pick(r, "ended_utc", "completed_utc"),
            "cost": 1 if kind in {"search", "open", "find", "screenshot"} else 0,
            "cumulative_cost": pick(r, "cumulative_cost", default=None),
            "record_file": str(path.relative_to(P)),
        }
        runs.append(event)
assert len({r["event_id"] for r in runs}) == len(runs), "duplicate event ID"
search_by_query = {r["query_id"]: r for r in runs if r["kind"] == "search"}
for r in runs:
    if r["kind"] == "rank":
        # P1 raw rank receipts use query_cost rather than cumulative_cost.
        # Use the matching actual search event, never a document operation.
        r["cumulative_cost"] = search_by_query[r["query_id"]]["cumulative_cost"]
    if r["kind"] in {"open", "find", "screenshot"} and r["source_id"]:
        s = src[r["source_id"]]
        if r["event_id"] not in s["operation_ids"]:
            s["operation_ids"].append(r["event_id"])
        s["operation_id"] = joined(s["operation_ids"])

operation_records = {r["event_id"]: r["record_file"] for r in runs if r["cost"]}
for path in sorted((P / "postseal").glob("*/operations.jsonl")):
    for operation in read_jsonl(path):
        oid = pick(operation, "operation_id", "event_id", "id")
        assert oid and oid not in operation_records, (str(path), oid)
        operation_records[oid] = str(path.relative_to(P))
for s in sources:
    s["operation_records"] = [{"operation_id": oid, "record_file": operation_records[oid]} for oid in s["operation_ids"]]
rank_rows = {r["event_id"]: r for r in runs if r["kind"] == "rank"}
open_by_source = {r["source_id"]: r for r in runs if r["kind"] in {"open", "find", "screenshot"} and r["source_id"]}
assert len(open_by_source) == sum(r["kind"] in {"open", "find", "screenshot"} and bool(r["source_id"]) for r in runs), "multiple original operations for one source require explicit earliest-read handling"
totals = {(p, a): sum(r["cost"] for r in runs if r["proposal_id"] == p and r["arm"] == a) for p in ["P1", "P2", "P3"] for a in "ABC"}
common = {p: min(totals[p, a] for a in "ABC") for p in ["P1", "P2", "P3"]}

judgments = []
p1_maps = json.loads((P / "experiment/P1/candidate-map.json").read_text())
p1_by_rank = {rid: m for m in p1_maps for rid in m["ranks"]}
for pr in ["P1", "P2", "P3"]:
    path = P / f"experiment/{pr}/judgments.csv"
    with path.open(newline="") as f:
        raw = list(csv.DictReader(f))
    for r in raw:
        rid = pick(r, "rank_id", "id")
        rr = rank_rows[rid]
        sid = pick(r, "source_id")
        s = src.get(sid, {})
        op = open_by_source.get(sid, {})
        # Null means there was no document operation linked to this rank.
        # Search-return time and end-of-arm cost never masquerade as read cost.
        readcost = op.get("cumulative_cost")
        status = pick(r, "read_status", "access_status")
        primary = bool(s.get("direct_original_read"))
        j = {
            "rank_id": rid, "proposal_id": pr, "arm": r["arm"], "query_id": rr["query_id"],
            "raw_rank": rr["rank"], "actual_query": queries[rr["query_id"]]["query"],
            "title": rr["title"], "original_url": rr["url"], "landed_url": s.get("landed_url", rr["url"]),
            "read_status": status, "source_id": sid, "operation_id": op.get("event_id", ""),
            "search_cumulative_cost": rr["cumulative_cost"], "reading_cumulative_cost": readcost,
            "arm_total_cost": totals[pr, r["arm"]], "common_prefix": common[pr],
            "within_common_prefix": bool(readcost is not None and int(readcost) <= common[pr]),
            "direct_original_read": primary,
            "direct_body_read": bool(s.get("direct_body_read")), "primary_source": bool(s.get("primary_source")),
            "source_kind": s.get("source_kind", "unread"),
            "target_id": pick(r, "target_id"), "mechanism_ids": pick(r, "mechanism_ids", "principle_ids", "mechanism"),
            "candidate_role": pick(r, "candidate_role", "role"),
            "donor_to_recipient_choice": pick(r, "donor_to_recipient_choice", "mapping", "potential_design_hypothesis"),
            "C1": r.get("C1", "unknown"), "C2": r.get("C2", "unknown"),
            "qualified_design": truth(pick(r, "qualified_design", "conditional_design_eligible", "conditional_eligible", default=False)),
            "application_status": "not_run", "read_sections": s.get("read_sections", ""),
            "minimal_falsifier": pick(r, "minimal_falsifier", "separating_input", "counter_input"),
            "control_input": pick(r, "control_input"),
            "novelty_assessment": pick(r, "novelty_assessment", "novelty"),
            "next_design_action": pick(r, "next_design_action"),
            "remaining_unknowns": pick(r, "remaining_unknowns", "limits", "limit"),
            "record_file": str(path.relative_to(P)),
        }
        if pr == "P1" and rid in p1_by_rank:
            m = p1_by_rank[rid]
            j["mechanism_ids"] = m["candidate_id"]
            j["donor_to_recipient_choice"] = m["canonical_target"] + ": " + m["canonical_mechanism"] + "; 적용 한계: " + m["reason"]
            j["minimal_falsifier"] = j["minimal_falsifier"] or m["separating_input"]
            j["control_input"] = j["control_input"] or m["control_input"]
        judgments.append(j)
assert len(judgments) == 90 and len({j["rank_id"] for j in judgments}) == 90
assert set(rank_rows) == {j["rank_id"] for j in judgments}
for j in judgments:
    rr = rank_rows[j["rank_id"]]
    rr["source_id"] = j["source_id"]
    rr["status"] = j["read_status"]
    rr["document_operation_ids"] = [j["operation_id"]] if j["operation_id"] else []
    rr["reading_cumulative_cost"] = j["reading_cumulative_cost"]
judgments.sort(key=lambda r: r["rank_id"])
sources.sort(key=lambda r: r["source_id"])
runs.sort(key=lambda r: (r["proposal_id"], r["arm"], int(r["cumulative_cost"] or 0), {"search":0,"rank":1,"open":2}.get(r["kind"],3), r["event_id"]))
for name, rows in [("runs.jsonl", runs), ("sources.jsonl", sources)]:
    (P / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
with (P / "judgments.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(judgments[0]))
    writer.writeheader(); writer.writerows(judgments)

semantic = []
for pr in ["P1", "P2", "P3"]:
    groups = defaultdict(list)
    for j in judgments:
        if j["proposal_id"] != pr or not j["source_id"]:
            continue
        for mechanism in j["mechanism_ids"].replace("|", ";").split(";"):
            mechanism = mechanism.strip()
            if mechanism and mechanism not in {"unknown", "unverified", "none_confirmed"}:
                groups[mechanism].append(j)
    for mechanism, js in sorted(groups.items()):
        semantic.append({"proposal_id":pr, "mechanism_class":mechanism, "arms":"/".join(sorted({j["arm"] for j in js})), "rank_ids":";".join(j["rank_id"] for j in js), "distinct_donor_target_ids":";".join(sorted({j["target_id"] for j in js})), "source_ids":";".join(sorted({j["source_id"] for j in js})), "all_direct_original":all(j["direct_original_read"] for j in js), "qualified_in_any_arm":any(j["qualified_design"] for j in js), "same_mechanism_is_not_same_implementation":True, "boundary":"Partial behavior-level alignment only; two fixed conditions are separately judged in judgments.csv"})
with (P / "evidence/semantic-overlap.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(semantic[0])); writer.writeheader(); writer.writerows(semantic)

summary = {
    "queries": len(queries), "rank_slots": len(judgments), "original_events": len(runs),
    "original_search_operations": sum(r["kind"] == "search" for r in runs),
    "original_document_operations": sum(r["kind"] in {"open", "find", "screenshot"} for r in runs),
    "original_total_operations": sum(r["cost"] for r in runs),
    "distinct_exact_returned_urls": len({r["url"] for r in rank_rows.values() if r["url"]}),
    "distinct_normalized_returned_urls": len({norm_url(r["url"]) for r in rank_rows.values() if r["url"]}),
    "source_rows": len(sources), "independent_original_works": len(counted_works),
    "minimum_count_representatives": sum(s["minimum_count_representative"] for s in sources),
    "source_direct_body_read_rows": sum(s["direct_body_read"] for s in sources),
    "source_direct_primary_body_rows": sum(s["direct_original_read"] for s in sources),
    "source_classification_definitions": {
        "direct_body_read": "A substantive body was read, including secondary/mirror bodies; metadata-only listings and failed/redirect/rewrite responses are false.",
        "primary_source": "Issuer-original evidence for the recorded research claims; independent of whether this work is eligible for the minimum.",
        "direct_original_read": "direct_body_read AND primary_source; not derived from another row's count eligibility.",
        "count_eligible": "Reported source eligibility for the minimum; canonical work deduplication still applies.",
        "minimum_count_representative": "One actual eligible source row per canonical work; these rows sum to the independent-work total."
    },
    "original_direct_read_work_ids": sorted({s["independent_work_id"] for s in sources if s["phase"] == "original_experiment" and s["direct_original_read"]}),
    "counted_work_ids": sorted(counted_works),
    "direct_original_rank_slots": sum(j["direct_original_read"] for j in judgments),
    "qualified_design_slots": sum(j["qualified_design"] for j in judgments),
    "target_application_trials": 0, "target_application_success_rate": None,
    "arms": {},
    "normalization_notes": ["Two ONES families merged into one", "Scientific Python generic governance/conduct/committee docs conservatively merged", "nbformat PR343/release correction retains its event ID but is counted in the same implementation family", "Direct body access, primary provenance and minimum-count eligibility are separate", "API bodies/patches are primary reads; commit-list metadata is not a body read", "Source operation_ids arrays and operation-record paths are preserved", "Rank search costs are linked to their actual search events; read costs only to actual document operations", "Original raw byte seals stay immutable; derived files normalize aliases and interpret labels"]
}
for pr in ["P1", "P2", "P3"]:
    summary["arms"][pr] = {}
    for arm in "ABC":
        js = [j for j in judgments if j["proposal_id"] == pr and j["arm"] == arm]
        rs = [r for r in runs if r["proposal_id"] == pr and r["arm"] == arm]
        qualified = [j for j in js if j["qualified_design"]]
        primary_ops = [r for r in rs if r["kind"] in {"open","find","screenshot"} and src.get(r["source_id"],{}).get("direct_original_read")]
        summary["arms"][pr][arm] = {"search":sum(r["kind"] == "search" for r in rs), "document_operations":sum(r["kind"] in {"open","find","screenshot"} for r in rs), "cost":totals[pr,arm], "common_prefix":common[pr], "direct_original_document_operations":len(primary_ops), "direct_original_document_operations_at_prefix":sum(int(r["cumulative_cost"]) <= common[pr] for r in primary_ops), "direct_original_slots":sum(j["direct_original_read"] for j in js), "direct_original_slots_at_prefix":sum(j["direct_original_read"] and j["within_common_prefix"] for j in js), "qualified":len(qualified), "first_qualified_cost":min((j["reading_cumulative_cost"] for j in qualified),default=None), "read_statuses":dict(Counter(j["read_status"] for j in js))}
(P / "evidence/normalized-counts.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ["queries","rank_slots","original_total_operations","source_rows","independent_original_works","direct_original_rank_slots","qualified_design_slots"]}, ensure_ascii=False))
