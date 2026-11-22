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

def opening_recoveries():
    output = []
    extra_path = ROOT / "evidence/opening-head-metadata.json"
    extra = read_json(extra_path) if extra_path.exists() else {}
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / "initial-public-head-recovery.json"
        if not path.exists():
            continue
        data = read_json(path)
        for r in data.get("recoveries", data.get("recovered", [])):
            sid = r.get("slot_id", "")
            if not sid.startswith(("N-", "L-")):
                continue
            isp = stream == "pandas"
            meta = r.get("head_commit_metadata", {})
            if sid in extra:
                m = extra[sid]
                meta = {"author_login": m["author"], "git_author_date": m["author_date"], "git_committer_date": m["committer_date"], "parents": [m["parent"]]}
            output.append({
                "slot_id": sid, "pr_number": r["pr"], "repository": data["repository"],
                "opening_head_sha": r.get("opening_head_sha", r.get("head_sha")),
                "opening_base_sha": r.get("opening_base_sha", r.get("base_sha")),
                "opening_event_utc": r.get("opening_event_created_at_utc", r.get("opening_event_utc")),
                "pr_created_utc": r.get("created_at_current_API", r.get("pr_created_at_rest")),
                "payload_updated_utc": r.get("opening_payload_updated_at_utc", r.get("pr_payload_updated_at_in_open_event_utc")),
                "opening_actor": r.get("opening_actor", r.get("actor")),
                "opening_head_author": meta.get("author_login", "see original commit metadata"),
                "opening_head_git_author_date": meta.get("git_author_date", ""),
                "opening_head_git_committer_date": meta.get("git_committer_date", ""),
                "head_parents": r.get("head_parent_sha") or ";".join(meta.get("parents", [])),
                "pr_diff_merge_base": r.get("original_diff_merge_base_sha", r.get("compare_merge_base")),
                "opening_title": r.get("opening_title", r.get("initial_title")),
                "body_equals_current": r.get("opening_body_exact_equals_current", r.get("current_body_matches")),
                "opening_changed_files": r["opening_changed_files"],
                "opening_commits": r.get("opening_commit_count", r.get("opening_commits")),
                "previous_candidate_sha": r.get("initial_candidate_sha_before_recovery", r.get("existing_baseline_sha")),
                "diff_url": r.get("original_diff_source_url", r.get("compare_url")),
                "diff_directly_read": r.get("original_diff_directly_read", r.get("initial_diff_file_count_matches_event", False)),
                "source_query_url": r.get("mirror_query_url", data.get("query_url")),
                "source_query_checked_utc": r.get("mirror_checked_utc", data.get("query_checked_utc")),
                "source_id": r["source_id"],
                "head_metadata_source_id": "RR-OPEN-P2" if sid in extra else "",
                "finding": r.get("opening_body_summary", r.get("finding")),
                "prior_knowledge_correction": r.get("prior_knowledge_correction", r.get("finding")),
                "raw_event_independent_corroboration": False,
                "verification_basis": "documented public normalized mirror of opened event plus exact GitHub SHA diff; raw compressed archive403 and original event ID unavailable",
                "stream_file": str(path.relative_to(ROOT)),
            })
    output.sort(key=lambda r: (not r["slot_id"].startswith("N-"), r["slot_id"]))
    write_csv("initial-public-heads.csv", output)
    return {r["slot_id"]: r for r in output}

def main():
    frame = read_csv(ROOT / "frame.csv")
    selected = {r["slot_id"]: r for r in frame if r.get("slot_id")}
    baseline = {r["slot_id"]: r for r in read_csv(ROOT / "baselines.csv")}
    pmeta = read_json(ROOT / "streams/pandas/observation-metadata.json")
    openings = opening_recoveries()
    cases = []
    evidence = {
        "L-P1": {"same_public": None, "any_public": "2023-03-23T18:46:25Z", "any_sha": "540db96b8179c2ed83e427b9d501b04d68ee1804", "any_change_ref": "L-P1-3;L-P1-4", "same_prestarted": False, "any_prestarted": True},
        "L-P2": {"same_public": "2023-03-20T17:17:26Z", "any_public": "2023-03-20T17:17:26Z", "any_sha": "19e864062c0d253db1b10469876b553391dad0db", "any_change_ref": "L-P2-7", "same_prestarted": True, "any_prestarted": True},
        "L-S1": {"same_public": None, "any_public": "2023-02-14T09:22:47Z", "any_sha": "feaabb7e6f2ccecced7a6847a267ad54b026f8a3", "any_change_ref": "S-C08", "same_prestarted": False, "any_prestarted": False},
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
    for c in cases:
        opening = openings.get(c["slot_id"])
        if opening:
            c["candidate_sha_before_opened_recovery"] = c["baseline_sha"]
            c["baseline_sha"] = opening["opening_head_sha"]
            c["opening_base_sha"] = opening["opening_base_sha"]
            c["opening_event_utc"] = opening["opening_event_utc"]
            c["exact_first_public_head_verified"] = True
            c["first_public_head_verification_basis"] = opening["verification_basis"]
            c["raw_event_independent_corroboration"] = False
            c["opening_body_equals_current"] = opening["body_equals_current"]
            c["opening_body_correction"] = opening["prior_knowledge_correction"]
            c["first_public_head_limitation"] = "Opened snapshot recovered from documented normalized mirror and immutable GitHub diff; raw event ID/hourly archive not independently recovered; intermediate/later push histories remain incomplete."
            c["source_ids"].append(opening["source_id"])
            if opening["head_metadata_source_id"]:
                c["source_ids"].append(opening["head_metadata_source_id"])
            c["missing_before_opened_recovery"] = c["missing"]
            c["missing"] = {
                "N-P1": "실패 CI 원 job 로그, 실제 사람 작업 시작/중지; raw opened event 독립 확인은 공통 한계",
                "N-P2": "PR/patch 계정의 동일인 증명, 실제 작업시간; raw opened event 독립 확인은 공통 한계",
                "N-P3": "사람 검토/수정시간; raw opened event 독립 확인은 공통 한계",
                "N-P4": "CoW 시험 보정의 명시 원인, 38일의 작업/대기 구분",
                "N-S1": "표본 작성자의 실제 사람 시간과 동등 품질 반사실",
                "N-S2": "원 PR 종결 전 후속 patch/push 순서 미복구, 사람 시간",
                "N-S3": "원 commit 계정 귀속과 사람 작업시간",
                "N-S4": "주창 표본 작성자 노동 및 동등 품질 시간쌍; 소비자 many hours는 주창 밖",
                "L-P1": "정확한 링크 직전 public head, 사라진/사적 원작성자 patch, 실제 열람시각/최초인지/사람 시간",
                "L-P2": "첫 링크의 기존 재설계에 대한 추가 기여, 실제 작업 시작/중지",
                "L-S1": "원 작성자의 링크 뒤 branch/push 복구, 명시 자료 연결, 당시 시험 완료, 사람 시간",
                "L-S2": "당시 HackMD 판, 첫 링크와 변경의 명시 연결, 대응 CI/시험 로그, 실제 사람 시간/동등 품질 비교",
            }[c["slot_id"]]
            if c["slot_id"] in ("L-P1", "L-P2"):
                c["strict_reason_before_opened_recovery"] = c["strict_reason"]
                c["strict_reason"] = "원 작성자 response patch와 첫 링크 변경 이유 연결 미확인; 타인 대안은 먼저 착수" if c["slot_id"] == "L-P1" else "같은 작성자 후속 patch는 있지만 같은 재설계가 첫 링크 전에 이미 공개; 첫 링크의 명시 기여 연결 없음"
        if c["slot_id"] == "L-P2":
            c["same_author_change_before_publication_recheck"] = c["same_author_same_purpose_change"]
            c["same_author_change_after_R03"] = None
            c["same_author_same_purpose_change"] = True
            c["same_author_change_status"] = "confirmed R04: same-author post-link merge integration19e8640 changes relevant mask handling relative to first parent; logic had been authored before the link in52043"
            c["any_author_same_purpose_change"] = True
            c["any_author_change_status"] = "confirmed by19e8640 integration, not by unknown in-window f95152e publication"
            c["change_type"] = "integration_of_previously_authored_same_purpose_logic"
            c["integration_dependency_created_at"] = "2023-03-17T19:48:49Z"
            c["integration_public_by"] = "2023-03-20T17:17:26Z"
            c["integration_source"] = "streams/pandas/final-risk-review.json"
            c["post_closure_same_author_same_purpose_change_confirmed"] = True
            c["post_closure_patch_public_by"] = "2023-03-20T20:36:41Z"
            c["publication_recheck_source"] = "https://github.com/pandas-dev/pandas/pull/52089#pullrequestreview-1349354160"
            c["source_ids"].append("RR-LP2-FIRST-PUBLIC")
            c["missing"] = "정확 f95152e가 원PR종결17:38:10Z까지 공개됐다는 head/review 기록; 이후20:36:41Z리뷰에서는확인. 첫링크의기여와사람노동도미확인"
            c["strict_reason"] = "19e8640의 주창 내 실제 사후통합은 확인하나 로직은 링크 전에 이미 작성됨. 첫 링크가 이 변경의 이유였다는 연결은 미확인; 별도 f95152e의 주창 공개도 여전히 미확인"
            c["source_ids"].extend(json.loads(line)["source_id"] for line in (ROOT/"streams/pandas/sources-supplement-final-risk.jsonl").read_text().splitlines() if line.strip())
        if c["slot_id"] == "N-S4":
            c["source_ids"].append("S-ARCH-COST-25261")
        if c["slot_id"] == "L-S1":
            c["source_ids"].append("S-ARCH-SUCCESSOR-25605")
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
            r["final_historical_implementation_status"] = "opening head/base/body recovered from documented public mirror; exact GitHub diff read" if c["exact_first_public_head_verified"] else "recovered; first public upload identity unverified"
            r["postfreeze_recovery"] = c.get("selection_recovery") or "none"
            r["final_baseline_sha"] = c["baseline_sha"]
            if r["slot_id"] in openings:
                r["opening_source_id"] = openings[r["slot_id"]]["source_id"]
                r["opening_event_utc"] = openings[r["slot_id"]]["opening_event_utc"]
        elif r["repository"] == "scikit-learn/scikit-learn" and r["pr_number"] == "25272":
            r["postfreeze_recovery"] = "S-ARCH-OPEN-25272/S-ARCH-COMPARE-25272: opening33ee1f59 exact diff confirms test-only exclusion; frozen uncertainty retained"
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
        actor_sens.append({"rule": name, "excluded_slots": sorted(excluded), "denominator_first_link_slots": len(cs), "same_author_change_confirmed": sum(c["same_author_same_purpose_change"] is True for c in cs), "same_author_change_unknown": sum(c["same_author_same_purpose_change"] is None for c in cs), "any_author_change_confirmed": sum(c["any_author_same_purpose_change"] is True for c in cs), "any_author_change_unknown": sum(c["any_author_same_purpose_change"] is None for c in cs), "strict_confirmed": 0})
    write_json("evidence/statistics.json", {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "frame_rows": len(frame), "frame_groups": dict(Counter(r["repository"] + "/" + r["stratum"] for r in frame)),
        "slots": len(cases), "strata": {s: sum(c["stratum"] == s for c in cases) for s in ("natural", "link_priority")},
        "historical_implementations_recovered": 12, "exact_first_public_heads_verified": len(openings),
        "first_public_head_verification_basis": "documented public normalized opened-event mirror plus immutable GitHub exact diff; raw event independent corroborations0",
        "main_window": groups[-2:], "time_boundary_sensitivity": groups, "actor_and_prework_sensitivity": actor_sens,
        "explicit_reading_confirmed": 0, "specific_target_content_engagement_confirmed": 2,
        "first_review_acknowledgement_confirmed": 3, "explicit_first_discovery_confirmed": 0,
        "specific_target_prior_authorship": 1, "same_author_change_unobserved": ["L-P1"], "same_author_change_unknown": ["L-S1"],
        "publication_boundary_correction": "R03: earlier same-author2/4 and any-author4/4 become1/4 and3/4; L-P2 exact patch first recovered public anchor20:36:41 is after17:38:10 closure, despite successor PR opening45 seconds before closure. Actual later change remains confirmed.",
        "integration_recheck_R04": "Final same-author2/4 and any-author4/4 use independent19e8640 first-parent diff and post-link GitHub-created parent1f7a7f2 plus in-window review1349064316. R03 correction for f95152e remains valid. Pre-link authorship of imported logic prevents causal/discovery upgrade.",
        "change_type_sensitivity": {"include_same_purpose_integration": {"same_author_confirmed":2,"denominator":4},"exclude_integration_of_previously_authored_logic": {"same_author_confirmed":1,"denominator":4,"excluded_positive":"L-P2; descriptive recoding, not PR exclusion"}},
        "human_time": {"active_logs": 0, "in_window_author_duration_selfreports": 0, "out_of_window_other_person_qualitative_selfreport": 1, "quality_matched_time_pairs": 0, "saved_seconds": None},
        "interpretation": "Counts are observations within fixed small strata. Missing labor is not zero labor; conditional denominator zero means not applicable. Any-author sensitivity includes continuation of an already-started alternative in L-P1. Same-author2 includes L-P2 integration of logic authored before the link; excluding that change type leaves1/4.",
        "change_denominator_notes": "All change counts in main_window and sensitivity mean after the first qualifying reviewer URL. Natural strata have zero such URLs: the conditional change ratio is not applicable, not a claim that no revision occurred. N-P1 is an observed no-link functional revision counterexample.",
        "inputs_sha256": {**{f"streams/{s}/cases.json": hashlib.sha256((ROOT / "streams" / s / "cases.json").read_bytes()).hexdigest() for s in ("pandas", "sklearn")}, "streams/pandas/final-risk-review.json":hashlib.sha256((ROOT/"streams/pandas/final-risk-review.json").read_bytes()).hexdigest()},
    })
    print(json.dumps({"cases": len(cases), "sensitivity_rows": len(sensitivity), "stratum_counts": groups[-2:], "actor_sensitivity": actor_sens}, ensure_ascii=False))

if __name__ == "__main__":
    main()
