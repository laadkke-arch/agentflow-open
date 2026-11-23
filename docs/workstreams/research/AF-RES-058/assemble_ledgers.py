"""Normalize the separately read evidence ledgers; never merge participant records.

All inputs and outputs remain in this workstream. Raw author inputs stay ignored.
The resulting counts are bibliographic counts, not independent participant counts.
"""
from __future__ import annotations
import csv
import json
import re
from collections import defaultdict, Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent

def read_json(path):
    return json.loads(path.read_text())

def cell(value):
    if value is None:
        return "미확인"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value

def write_csv(name, rows, fields=None):
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    with (BASE / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: cell(row.get(k)) for k in fields})

frames = []
for stream in ("software", "adjacent"):
    for row in read_json(BASE / "streams" / stream / "frame.json"):
        rank = row.get("review_order", row.get("recruit_rank"))
        fid = row.get("frame_id", f"AD-F{rank:02}")
        sid = row.get("source_id", f"SW-S{rank:02}")
        frames.append({
            "frame_id": fid,
            "stratum": "A" if stream == "software" else "B",
            "recruit_rank": rank,
            "doi": row["doi"],
            "title": row["title"],
            "publication_sort_date": row.get("publication_sort_date", row.get("sort_date")),
            "date_precision": row.get("date_precision", "see frozen recruitment snapshot"),
            "method_decision": row.get("method_status", row.get("method_decision")),
            "reason": row.get("method_reason_ko", row.get("reason")),
            "slot": row.get("slot_id", row.get("slot")),
            "cohort_id": row.get("cohort_id"),
            "source_id": sid,
            "method_location": row.get("method_location", row.get("method_locator")),
            "method_access_limit": row.get("method_access_limit", row.get("method_status") == "methods_unresolved"),
            "raw_discovery": row.get("discovery", "evidence/recruitment-B-snapshot.json.gz"),
            "metadata_freeze_commit": "02dbcaa1cd8dad27b113e9a225ab1fc95b913a9a",
            "selection_freeze_commit": "1ff924dc53dee8ff4b07fa1f1c25e7f601d72d95",
        })
write_csv("frame.csv", frames)
selected_dois = {r["doi"].lower(): r["slot"] for r in frames if r["slot"]}
source_slot = {r["source_id"]: r["slot"] for r in frames if r["slot"]}

raw_sources = []
for stream in ("software", "adjacent", "diagnostics", "root"):
    path = BASE / "streams" / stream / "sources.jsonl"
    if path.exists():
        raw_sources.extend((stream, json.loads(line)) for line in path.read_text().splitlines() if line)

known = {
    "W-D01-Bansal2021": "doi:10.1145/3411764.3445717",
    "W-D02-Bucinca2021": "doi:10.1145/3449287",
    "W-D03-Poursabzi2021": "doi:10.1145/3411764.3445315",
    "W-D04-Lai2019": "doi:10.1145/3287560.3287590",
    "W-D05-Zhang2020": "doi:10.1145/3351095.3372852",
    "W-D07-deJong2025": "doi:10.1145/3710946",
    "W-D03-Poursabzi2017-Preregister": "protocol:aspredicted-5247",
}

def canonical(row):
    wid = row["work_id"]
    if wid in known:
        return known[wid]
    kind = row.get("kind", row.get("kind_lineage", {}).get("kind", ""))
    if "access" in kind or "fail" in kind:
        return wid
    urls = " ".join(str(row.get(k, "")) for k in ("original_url", "fixed_version_url", "pinned_url"))
    if any(s in kind for s in ("package", "repository", "code", "dataset")) or "Package" in wid:
        hit = re.search(r"github\.com/([^/\s]+)/([^/\s]+)", urls)
        if hit:
            return "repo:" + "/".join(hit.groups()).rstrip(".,)").lower()
    if wid.startswith(("doi:", "acl:", "repo:", "dataset:", "osf:")):
        return wid.lower()
    lineage = row.get("lineage", {})
    if isinstance(lineage, dict) and lineage.get("doi"):
        key = "doi:" + lineage["doi"].lower()
        known.setdefault(wid, key)
        return known[wid]
    hit = re.search(r"doi\.org/(10\.[^\s?]+)", row.get("original_url", ""))
    if hit:
        key = "doi:" + hit.group(1).lower().rstrip(".,)")
        known.setdefault(wid, key)
        return known[wid]
    return wid

sources = []
for stream, row in raw_sources:
    sid = row["source_id"]
    wid = canonical(row)
    kind = row.get("kind", row.get("kind_lineage", {}).get("kind", ""))
    fixed = row.get("fixed_version", {})
    eligible = row.get("countable_primary_work", row.get("count_as_external_primary_work", row.get("external_primary_eligible", row.get("counts_for_20", False))))
    status = row.get("read_status", row.get("access_status"))
    cases = list(row.get("cases", row.get("case_ids", [])))
    if sid in source_slot and source_slot[sid] not in cases:
        cases.append(source_slot[sid])
    if row.get("study_id") and row["study_id"] not in cases:
        cases.append(row["study_id"])
    paper_doi = wid.removeprefix("doi:")
    category = "screened_method_source"
    if eligible:
        if sid.startswith(("AD-BIOS-P", "AD-MIMIC-P")) and not sid.endswith("PKG"):
            category = "ground_truth_support"
        elif sid in ("AD-DRXAI-PKG", "AD-BIOS-PKG", "AD-MIMIC-PKG"):
            category = "source_or_model_tool_support"
        elif "protocol" in kind or "preregister" in kind:
            category = "separate_protocol"
        elif "ground_truth" in kind:
            category = "ground_truth_support"
        elif any(t in kind for t in ("package", "repository", "code", "dataset")):
            category = "author_package"
        elif paper_doi in selected_dois:
            category = "selected_author_poster" if kind == "author_poster" else "selected_human_paper"
        elif any(str(c).startswith("D0") for c in cases) and "correction" not in kind:
            category = "diagnostic_human_paper"
        elif "ground" in kind or sid.startswith(("RT-OTT", "AD-BIOS", "AD-MIMIC")):
            category = "ground_truth_support"
    else:
        category = "not_counted"
    # Method-only exclusions are real reads, but are not used to meet the deep minimum.
    counts_for_20 = bool(eligible and category not in ("screened_method_source", "not_counted"))
    source = {
        "source_id": sid, "work_id": wid, "original_work_id": row["work_id"],
        "kind": kind, "lineage": row.get("lineage", row.get("kind_lineage", {})),
        "questions": row.get("questions", []), "cases": cases,
        "original_url": row.get("original_url"),
        "fixed_version_url": row.get("fixed_version_url", row.get("pinned_url", fixed.get("url", row.get("original_url")))),
        "version_date_or_hash": row.get("version_or_hash", row.get("version_date_or_hash", fixed or {"version": row.get("version"), "sha256": row.get("sha256")})),
        "read_utc": row.get("read_utc", row.get("accessed_utc", row.get("read_utc_interval", row.get("opened_utc")))),
        "acquired_utc": row.get("opened_utc", row.get("accessed_utc")),
        "locations": row.get("locator", row.get("locations", row.get("location"))),
        "verified": row.get("verified_content", row.get("verified", row.get("checked_ko"))),
        "scope_and_limits": row.get("scope_and_limitations", row.get("scope_and_limits", row.get("scope_and_limit", row.get("limits_ko")))),
        "evidence_mode": row.get("evidence_mode", row.get("epistemic_status", row.get("claim_type", row.get("epistemic")))),
        "counterevidence_ids": row.get("contrary_source_ids", row.get("counterevidence_ids", row.get("opposing_source_ids", []))),
        "read_status": status,
        "external_primary_eligible": bool(eligible), "counts_for_deep_20": counts_for_20,
        "category": category, "formal_paper_read": row.get("formal_paper_read", kind != "author_poster"),
        "reader": row.get("reader", "/root/" + stream),
        "stream_record": f"streams/{stream}/sources.jsonl",
    }
    if sid == "RT-VAS-P":
        source["counterevidence_ids"] = sorted(set(source["counterevidence_ids"] + ["DI-DEJ-P", "DI-LAI-P", "RT-VAS-REG-QA"]))
    sources.append(source)
assert len({s["source_id"] for s in sources}) == len(sources), "duplicate source IDs"
with (BASE / "sources.jsonl").open("w") as f:
    for row in sources:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

works = defaultdict(list)
for row in sources:
    works[row["work_id"]].append(row)
work_rows = []
priority = ["selected_human_paper", "selected_author_poster", "diagnostic_human_paper", "separate_protocol", "author_package", "ground_truth_support", "source_or_model_tool_support", "screened_method_source", "not_counted"]
for wid, rows in sorted(works.items()):
    category = min((r["category"] for r in rows), key=priority.index)
    work_rows.append({"work_id": wid, "category": category,
                      "counts_for_deep_20": any(r["counts_for_deep_20"] for r in rows),
                      "external_primary_read": any(r["external_primary_eligible"] for r in rows),
                      "source_ids": [r["source_id"] for r in rows],
                      "cases": sorted({c for r in rows for c in r["cases"]}),
                      "count": 1 if any(r["counts_for_deep_20"] for r in rows) else 0})
write_csv("evidence/works.csv", work_rows)
counts = {"source_records": len(sources),
          "unique_read_primary_works": sum(r["external_primary_read"] for r in work_rows),
          "unique_deep_primary_works": sum(r["counts_for_deep_20"] for r in work_rows),
          "deep_categories": dict(Counter(r["category"] for r in work_rows if r["counts_for_deep_20"])),
          "primary_frame_reviewed": len(frames), "primary_slots_filled": len(selected_dois),
          "unfilled_primary_slots": ["A03", "A04"],
          "rule": "A work is counted once across mirrors, figures, appendices, code and repeated reads. Method-only exclusions are excluded from deep20. Three Vasconcelos registrations conservatively count as one protocol lineage. Author poster is not a read formal paper."}
(BASE / "evidence/source-counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=2) + "\n")

stimuli = []
for stream in ("software", "adjacent", "diagnostics", "root"):
    path = BASE / "streams" / stream / "stimuli.json"
    if not path.exists():
        continue
    payload = read_json(path)
    rows = payload.get("rows", []) if isinstance(payload, dict) else payload
    for n, row in enumerate(rows, 1):
        case = row.get("case_id", row.get("study_id"))
        pair = row.get("stimulus_pair", {})
        explanation = row.get("explanation", {})
        sid = row.get("stimulus_id", f"{stream.upper()}-ST{n:02}")
        stimuli.append({
            "stimulus_id": sid, "case_id": case,
            "conditions": row.get("conditions", row.get("contrast")),
            "allocation_unit": row.get("allocation_unit", row.get("assignment_unit")),
            "candidate_item_mapping": row.get("candidate_id", row.get("same_item", row.get("same_candidate_evidence"))),
            "candidate_equality_grade": row.get("candidate_equality_grade", row.get("same_item_grade")),
            "candidates_and_rank": row.get("rank_equality", row.get("candidates_rank")),
            "advice_value_equality": row.get("recommendation_value", row.get("same_recommendation")),
            "model": row.get("model"), "confidence": row.get("confidence", row.get("probability_or_confidence")),
            "time_limit": row.get("time_limit", row.get("time")),
            "explanation_elements": explanation or row.get("explanation_elements", row.get("explanation_forms")),
            "original_source_link": row.get("original_text_or_link", row.get("external_source_link", explanation.get("source_link"))),
            "delivery_and_reading": row.get("mandatory_or_optional", row.get("reading", explanation.get("delivery"))),
            "other_interventions": row.get("cointerventions", row.get("other_interventions")),
            "truth_source": row.get("truth_source", row.get("truth")),
            "actual_screen_pair": pair.get("actual_scope", row.get("item_pair_observed", row.get("paired_example"))),
            "source_ids": row.get("source_ids", []),
            "source_urls": row.get("stimulus_urls", pair.get("url")),
            "locator": row.get("locator", row.get("visual_locator", pair.get("locator"))),
            "limits": row.get("limit", row.get("interpretation")),
            "details_json": row,
        })
for case in ("A03", "A04"):
    stimuli.append({"stimulus_id": case + "-UNFILLED", "case_id": case,
                    "candidate_equality_grade": "미확인: 원연구 미선정",
                    "limits": "같은 층의 방법확인 부족. 다른 분야로 대체하지 않았다.",
                    "source_ids": [], "details_json": {"state": "unfilled_slot", "observed_zero_participants": False}})
write_csv("stimuli.csv", stimuli)
print(json.dumps(counts, ensure_ascii=False))
