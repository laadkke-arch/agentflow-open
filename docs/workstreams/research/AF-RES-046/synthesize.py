#!/usr/bin/env python3
"""Join frozen slots to observed case records; never infer human work from dates."""
from __future__ import annotations
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FREEZE = "994e21aaea7c5da0c4322db9d1ce2c4f52fa6a2f"

def dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def iso(d):
    return d.isoformat().replace("+00:00", "Z")

def read_json(path):
    return json.loads(path.read_text())

def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))

def write_json(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def write_csv(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def main():
    frame = read_csv(ROOT / "frame.csv")
    selected = {r["slot_id"]: r for r in frame if r.get("slot_id")}
    baseline = {r["slot_id"]: r for r in read_csv(ROOT / "baselines.csv")}
    pmeta = read_json(ROOT / "streams/pandas/observation-metadata.json")
    cases = []
    evidence = {
        "L-P1": {"same_public": None, "any_public": "2023-03-23T18:46:25Z", "any_sha": "540db96b8179c2ed83e427b9d501b04d68ee1804", "any_change_ref": "L-P1-3;L-P1-4", "same_prestarted": False, "any_prestarted": True},
        "L-P2": {"same_public": "2023-03-20T17:37:25Z", "any_public": "2023-03-20T17:37:25Z", "any_sha": "f95152e78c8baa2b1f4e07ecebb31496b3956c65", "any_change_ref": "L-P2-6", "same_prestarted": True, "any_prestarted": True},
        "L-S1": {"same_public": None, "any_public": "2023-02-14T09:22:46Z", "any_sha": "feaabb7e6f2ccecced7a6847a267ad54b026f8a3", "any_change_ref": "S-C08", "same_prestarted": False, "any_prestarted": False},
        "L-S2": {"same_public": "2023-02-06T07:57:51Z", "any_public": "2023-02-06T07:57:51Z", "any_sha": "eb6a658b0ada3464e0fa79da716f57af053141fe", "any_change_ref": "S-C09", "same_prestarted": False, "any_prestarted": False},
    }
    for stream in ("pandas", "sklearn"):
        for number, raw in enumerate(read_json(ROOT / "streams" / stream / "cases.json"), 1):
            sid = raw["slot_id"]
            row = selected[sid]
            is_p = stream == "pandas"
            has_link = raw["link"]["exists"] if is_p else raw["link"]
            link = raw["link"] if is_p else raw.get("first_link") or {}
            same = raw["same_author_change"]["after_first_link_across_PR"] if is_p else raw["post_first_link_same_author_same_purpose_change"]
            ev = evidence.get(sid, {})
            cases.append({
                "slot_id": sid, "stratum": "natural" if sid.startswith("N-") else "link_priority",
                "repository": raw["repo"], "pr_number": raw["pr"], "pr_url": raw["url"],
                "proposal_author": raw.get("author") or raw["proposal_author"], "selection_rank": int(row["rank"]),
                "selection_freeze_sha": FREEZE,
                "selection_provisional_at_freeze": sid == "N-S2",
                "selection_recovery": raw.get("selection_postfreeze_recovery"),
                "outcome_first_full_read_utc": pmeta["outcome_first_semantic_read_utc"] if is_p else raw["outcome_first_full_read_utc"],
                "window_start": raw["window_start"], "window_end": raw["window_end"],
                "window_end_rule": "created_plus_90_days" if dt(raw["window_end"]) == dt(raw["window_start"]) + timedelta(days=90) else "first_terminal_event",
                "historical_concrete_implementation_recovered": True,
                "exact_first_public_head_verified": False,
                "first_public_head_limitation": "Retained pre-opening git object or original review head, not independently archived first upload; current editable body is not proved identical to original body.",
                "baseline_sha": raw["baseline"]["initial_candidate_sha"] if is_p else raw["baseline_sha"],
                "pre_link_review_sha": baseline[sid]["pre_link_review_sha"],
                "first_qualifying_link_observed": has_link,
                "first_link_url": link.get("first_url") if is_p else link.get("url"),
                "first_link_co_url": None if is_p else link.get("co_link_url"),
                "first_link_source": link.get("source_url") if is_p else link.get("comment_url"),
                "first_link_at": link.get("at"), "first_link_location": link.get("location"),
                "first_link_class": link.get("class") if is_p else link.get("type"),
                "explicit_reading_observed": False,
                "reading_status": "미확인" if has_link else "해당 없음: 적격 링크 0",
                "target_content_engagement_confirmed": sid in ("L-P1", "L-P2"),
                "review_acknowledgement_confirmed": sid in ("L-P1", "L-P2", "L-S2"),
                "explicit_first_discovery_observed": False,
                "first_discovery_status": "미확인" if has_link else "해당 없음: 적격 링크 0",
                "specific_target_prior_authorship": sid == "L-P2",
                "linked_project_previously_named": sid == "L-S1",
                "same_author_same_purpose_change": same,
                "same_author_change_status": ("confirmed" if same is True else "not_observed_in_recovered_record" if same is False else "미확인" if has_link else "해당 없음: 적격 링크 0"),
                "same_author_change_public_by": ev.get("same_public"),
                "any_author_same_purpose_change": True if has_link else None,
                "any_author_change_public_by": ev.get("any_public"),
                "change_sha": ev.get("any_sha"), "change_evidence_rows": ev.get("any_change_ref"),
                "prelink_same_author_redesign_confirmed": ev.get("same_prestarted", False),
                "prelink_any_author_same_purpose_implementation_confirmed": ev.get("any_prestarted", False),
                "prelink_specific_correction_note": "P1 other author; P2 same author. S1/S2 broad prior work/failure is not proof that this exact corrective patch predated the URL." if has_link else "해당 없음",
                "strict_first_link_chain_confirmed": False,
                "strict_reason": raw["strict"]["reason"] if is_p else raw["strict_missing"],
                "active_work_log_observed": False, "active_human_work_seconds": None,
                "in_window_author_duration_selfreport_observed": False,
                "quality_matched_human_time_pair_observed": False, "saved_human_seconds": None,
                "savings_status": "미확인", "conditional_savings_rate": "해당 없음: 비교 가능한 시간 쌍 0",
                "competing_explanations": raw["competing_explanations"] if is_p else raw["evidence"]["competing"],
                "missing": raw["unknowns"] if is_p else raw["evidence"]["missing"],
                "source_ids": raw["source_ids"] if is_p else raw["evidence"]["source_ids"],
                "stream": stream, "stream_file": f"streams/{stream}/cases.json", "stream_record": number,
            })
    cases.sort(key=lambda c: (not c["slot_id"].startswith("N-"), c["slot_id"]))
    write_json("cases.json", cases)
    by_slot = {c["slot_id"]: c for c in cases}
    for r in frame:
        r.setdefault("frozen_status", r["status"])
        r.setdefault("frozen_eligibility", r["eligibility"])
        r.setdefault("frozen_baseline_candidate_sha", r["baseline_candidate_sha"])
        r["freeze_commit"] = FREEZE
        r["normalized_status"] = "selected" if r.get("slot_id") else "not_screened_after_quota" if "quota" in (r["status"] + r["reason"]).lower() else "excluded_or_not_selected"
        r["first_exposure_kind"] = "query metadata; detailed body/patch receipt in sources.jsonl"
        if r["repository"] == "pandas-dev/pandas" and r["pr_number"] == "51109":
            r["amendment_affected"] = "true"
        if r.get("slot_id"):
            c = by_slot[r["slot_id"]]
            r["outcome_first_read_utc"] = c["outcome_first_full_read_utc"]
            r["window_start"] = c["window_start"]
            r["window_end"] = c["window_end"]
            r["window_reason"] = c["window_end_rule"]
            r["final_historical_implementation_status"] = "recovered; first public upload identity unverified"
            r["postfreeze_recovery"] = c.get("selection_recovery") or "none"
            r["final_baseline_sha"] = c["baseline_sha"]
    write_csv("frame.csv", frame)
    sensitivity = []
    for days in (30, 60, 90):
        for c in cases:
            end = min(dt(c["window_end"]), dt(c["window_start"]) + timedelta(days=days))
            linked = c["first_qualifying_link_observed"] and dt(c["first_link_at"]) <= end
            sensitivity.append({
                "slot_id": c["slot_id"], "stratum": c["stratum"], "days": days, "window_start": c["window_start"], "window_end": iso(end),
                "link_in_window": linked,
                "same_author_change_confirmed": bool(linked and c["same_author_change_public_by"] and dt(c["same_author_change_public_by"]) <= end),
                "any_author_change_confirmed": bool(linked and c["any_author_change_public_by"] and dt(c["any_author_change_public_by"]) <= end),
                "strict_confirmed": False, "active_labor_measured": False,
                "source": c["first_link_source"] or c["pr_url"],
                "change_source": f"https://github.com/{c['repository']}/commit/{c['change_sha']}" if c["change_sha"] else "해당 없음",
            })
    write_csv("sensitivity.csv", sensitivity)
    groups = []
    for days in (30, 60, 90):
        for stratum in ("natural", "link_priority"):
            rs = [r for r in sensitivity if r["days"] == days and r["stratum"] == stratum]
            groups.append({"days": days, "stratum": stratum, "slots": len(rs), "links": sum(r["link_in_window"] for r in rs), "same_author_changes": sum(r["same_author_change_confirmed"] for r in rs), "any_author_changes": sum(r["any_author_change_confirmed"] for r in rs), "strict": 0, "direct_labor": 0, "paired_quality_time": 0})
    actor_sens = []
    for name, excluded in (("all_first_link_slots", set()), ("exclude_prelink_same_author_redesign", {"L-P2"}), ("exclude_prelink_any_author_same_purpose_implementation", {"L-P1", "L-P2"})):
        cs = [c for c in cases if c["first_qualifying_link_observed"] and c["slot_id"] not in excluded]
        actor_sens.append({"rule": name, "excluded_slots": sorted(excluded), "denominator_first_link_slots": len(cs), "same_author_change_confirmed": sum(c["same_author_same_purpose_change"] is True for c in cs), "same_author_change_unknown": sum(c["same_author_same_purpose_change"] is None for c in cs), "any_author_change_confirmed": sum(c["any_author_same_purpose_change"] is True for c in cs), "strict_confirmed": 0})
    write_json("evidence/statistics.json", {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "frame_rows": len(frame), "frame_groups": dict(Counter(r["repository"] + "/" + r["stratum"] for r in frame)),
        "slots": len(cases), "strata": {s: sum(c["stratum"] == s for c in cases) for s in ("natural", "link_priority")},
        "historical_implementations_recovered": 12, "exact_first_public_heads_verified": 0,
        "main_window": groups[-2:], "time_boundary_sensitivity": groups, "actor_and_prework_sensitivity": actor_sens,
        "explicit_reading_confirmed": 0, "specific_target_content_engagement_confirmed": 2,
        "first_review_acknowledgement_confirmed": 3, "explicit_first_discovery_confirmed": 0,
        "specific_target_prior_authorship": 1, "same_author_change_unobserved": ["L-P1"], "same_author_change_unknown": ["L-S1"],
        "human_time": {"active_logs": 0, "in_window_author_duration_selfreports": 0, "out_of_window_other_person_qualitative_selfreport": 1, "quality_matched_time_pairs": 0, "saved_seconds": None},
        "interpretation": "Counts are observations within fixed small strata. Missing labor is not zero labor; conditional denominator zero means not applicable. Any-author sensitivity includes continuation of an already-started alternative in L-P1.",
        "change_denominator_notes": "All change counts in main_window and sensitivity mean after the first qualifying reviewer URL. Natural strata have zero such URLs: the conditional change ratio is not applicable, not a claim that no revision occurred. N-P1 is an observed no-link functional revision counterexample.",
        "inputs_sha256": {f"streams/{s}/cases.json": hashlib.sha256((ROOT / "streams" / s / "cases.json").read_bytes()).hexdigest() for s in ("pandas", "sklearn")},
    })
    print(json.dumps({"cases": len(cases), "sensitivity_rows": len(sensitivity), "stratum_counts": groups[-2:], "actor_sensitivity": actor_sens}, ensure_ascii=False))

if __name__ == "__main__":
    main()
