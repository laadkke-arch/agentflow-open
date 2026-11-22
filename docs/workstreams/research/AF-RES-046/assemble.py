#!/usr/bin/env python3
"""Normalize already-read stream ledgers; no network calls or upstream code execution."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STREAMS = ("pandas", "sklearn", "crossdomain", "root")
ALIASES = {
    "pr_original": "pr_origin", "pr_origin": "pr_origin",
    "review_decision": "review_decision",
    "commit_test": "commit_test", "commit_or_test": "commit_test",
    "link_target": "linked_original", "linked_original": "linked_original",
    "cross_domain_music_operating_rule": "music_rule",
    "cross_domain_music_edit_ledger": "music_ledger",
    "cross_domain_map_edit_ledger": "map_ledger",
    "cross_domain_map_object_versions": "map_versions",
}

def first(row, *keys, default=""):
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return default

def scalar(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if value is None:
        return ""
    return str(value).replace("\r\n", " / ").replace("\n", " / ").replace("\r", " / ")

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(name, rows):
    keys = list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: scalar(value) for key, value in row.items()})

def canonical_work(row):
    url = first(row, "url", "source_url")
    match = re.search(r"github\.com/([^/]+/[^/]+)/(pull|issues)/(\d+)(?:#pullrequestreview-(\d+))?", url)
    if match:
        repo, kind, number, review = match.groups()
        return f"github:{repo}:review:{review}" if review else f"github:{repo}:{'pr' if kind == 'pull' else 'issue'}:{number}"
    match = re.search(r"github\.com/([^/]+/[^/]+)/(?:commit|blob)/([0-9a-f]{40})(?:[/#]|$)", url)
    if match:
        return "git:" + match.group(1) + ":" + match.group(2)
    return row["work_id"]

def sources():
    output, used, source_ids, inputs = [], {}, set(), {}
    for stream in STREAMS:
        folder = ROOT / "streams" / stream
        files = [folder / "sources.jsonl"]
        files += sorted(folder.glob("sources-supplement*.jsonl"))
        files += [folder / "additional-sources.jsonl", folder / "screening-attempts.jsonl", folder / "attempts.jsonl"]
        for path in files:
            if not path.exists():
                continue
            inputs[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if not line.strip():
                    continue
                raw = json.loads(line)
                sid = raw.get("source_id") or "ATT-" + raw["attempt_id"]
                raw.setdefault("work_id", f"attempt:{stream}:{sid}")
                if path.name == "attempts.jsonl":
                    raw.setdefault("checked_utc", raw.get("first_query_utc") or raw.get("start_utc"))
                    raw.setdefault("checked_utc_precision", raw.get("utc_precision", "recorded attempt; first retrieval time may be unavailable"))
                    raw.setdefault("location", "search query or HTTP retrieval attempt; no independent authored work")
                    raw.setdefault("finding", raw.get("result") or raw.get("error") or raw.get("status"))
                    raw.setdefault("limitation", "Attempt or discovery record only; no additional minimum-count source")
                if sid in source_ids:
                    raise ValueError("duplicate source_id " + sid)
                source_ids.add(sid)
                proposed = bool(first(raw, "count_in_minimum", "minimum_count", default=False))
                work = canonical_work(raw)
                is_git_object = work.startswith("git:")
                allocation = first(raw, "allocation", "minimum_allocation", default="supplementary")
                count = proposed and work not in used
                duplicate = used.get(work) if proposed and not count else raw.get("duplicate_of")
                if count:
                    used[work] = sid
                output.append({
                    "source_id": sid, "work_id": work, "original_work_id": raw["work_id"],
                    "edition_id": raw.get("edition_id"), "url": first(raw, "url", "source_url"),
                    "final_url": raw.get("final_url"), "publisher": raw.get("publisher"),
                    "kind": raw.get("kind"),
                    "published_at": None if is_git_object else first(raw, "published_at", "publication_date", default=None),
                    "modified_at": None if is_git_object else first(raw, "modified_at", "modified_date", default=None),
                    "git_author_date_from_stream": first(raw, "published_at", "publication_date", default=None) if is_git_object else None,
                    "git_committer_date_from_stream": first(raw, "modified_at", "modified_date", default=None) if is_git_object else None,
                    "date_semantics": "Git object date fields are not publication or work-time observations; see events for public anchors" if is_git_object else "platform/source metadata; editable body edition is separately qualified",
                    "checked_utc": raw.get("checked_utc"), "checked_utc_precision": raw.get("checked_utc_precision", "as recorded by stream"),
                    "location": raw.get("location"), "finding": raw.get("finding"),
                    "limitation": first(raw, "limitation", "limitations"),
                    "questions": first(raw, "questions", "question_ids", default=["Q1"] if "screening" in path.name else []), "case_ids": raw.get("case_ids", []),
                    "duplicate_of": duplicate, "count_in_minimum": count,
                    "allocation": ALIASES.get(allocation, allocation),
                    "raw_count_in_minimum": proposed, "raw_allocation": allocation,
                    "read_status": first(raw, "access_status", "read_status", "reading_method", default="stream semantic reading receipt"),
                    "query": raw.get("query"), "attempt_recorded_utc": raw.get("recorded_utc"),
                    "later_interpretation_correction": "R03: PR52089 creation17:37:25 does not establish exact f95152e public head. First recovered SHA-specific review1349354160 at20:36:41 follows original closure17:38:10; this patch's primary-window publication unknown. R04 confirms an independent19e integration; it does not restore this inference." if sid in ("P-PR-52089", "P-C-f95152e78c8b") else "R04: PR52053 creation16:00:14 does not establish exact fa750 opening head. Its ancestor presence is fixed by final19e review2023-03-20T17:17:26Z; the independent post-link19e integration is described in final-risk-review.json." if sid in ("P-PR-52053", "P-C-fa750f5fdaaf") else None,
                    "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
                })
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    return output, inputs

def baselines():
    frame = {row["slot_id"]: row for row in read_csv(ROOT / "frame.csv") if row.get("slot_id")}
    output = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / "baselines.csv"
        for number, row in enumerate(read_csv(path), 1):
            slot = row["slot_id"]
            meta = frame[slot]
            output.append({
                "slot_id": slot, "stratum": meta["stratum"], "repository": row["repository"],
                "pr_number": first(row, "pr_number", "pr"), "pr_url": first(row, "pr_url", "proposal_url"),
                "author": first(row, "author_login", "proposal_author"), "requirement": row["requirement"],
                "pre_link_choice": first(row, "prechoice", "implementation"),
                "initial_candidate_sha": first(row, "initial_candidate_sha", "pre_link_sha"),
                "pre_link_review_sha": first(row, "prelink_review_sha", "pre_link_sha"),
                "parent_sha": first(row, "initial_parent_sha", "base_parent"),
                "original_review_base": row.get("original_review_base", "미확인; commit parent is not asserted to be review base"),
                "git_author_date": first(row, "initial_candidate_author_date", "commit_author_date"),
                "git_committer_date": first(row, "initial_candidate_committer_date", "commit_committer_date"),
                "public_anchor": first(row, "prelink_public_anchor_at", "platform_public_observation_bound"),
                "public_anchor_url": row.get("prelink_public_anchor_url", ""),
                "first_public_head_verified": first(row, "first_public_head_verified", "first_public_upload_exact"),
                "first_public_head_limitation": first(row, "first_public_head_reason", "limitation"),
                "tests": first(row, "tests", "regression_test_contract"), "known_alternatives": row["known_alternatives"],
                "first_qualifying_link": first(row, "first_qualifying_link", default=meta.get("first_link_url", "")),
                "first_link_at": first(row, "first_qualifying_link_at", default=meta.get("first_link_at", "")),
                "first_link_location": row.get("first_qualifying_link_location", "see events.csv and frame.csv"),
                "window_start": first(row, "created_at", default=meta["created_at"]),
                "window_end": first(row, "window_end_90d", default=meta.get("window_end", "")),
                "window_end_source": row.get("closure_source", "see case-level outcomes when completed"),
                "source_ids": row["source_ids"], "limitation": first(row, "limitation", "current_base_head_warning"),
                "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
            })
    output.sort(key=lambda x: (0 if x["slot_id"].startswith("N-") else 1, x["slot_id"]))
    opening_path = ROOT / "initial-public-heads.csv"
    if opening_path.exists():
        opening = {r["slot_id"]: r for r in read_csv(opening_path)}
        for row in output:
            o = opening.get(row["slot_id"])
            if not o:
                continue
            row["initial_candidate_sha_before_archive"] = row["initial_candidate_sha"]
            row["candidate_parent_before_archive"] = row["parent_sha"]
            row["first_public_head_status_before_archive"] = row["first_public_head_verified"]
            row["first_public_head_limitation_before_archive"] = row["first_public_head_limitation"]
            row["initial_candidate_sha"] = o["opening_head_sha"]
            row["opening_head_sha"] = o["opening_head_sha"]
            row["opening_base_sha"] = o["opening_base_sha"]
            row["opening_diff_merge_base"] = o["pr_diff_merge_base"]
            row["opening_event_utc"] = o["opening_event_utc"]
            row["opening_payload_updated_utc"] = o["payload_updated_utc"]
            row["opening_diff_url"] = o["diff_url"]
            row["opening_body_equals_current"] = o["body_equals_current"]
            row["opening_body_finding"] = o["finding"]
            row["opening_head_author"] = o["opening_head_author"]
            row["first_public_head_verified"] = "true: documented opened-event mirror plus exact immutable GitHub diff"
            row["first_public_head_limitation"] = o["verification_basis"]
            if o["head_parents"]:
                row["parent_sha"] = o["head_parents"]
            elif row["initial_candidate_sha_before_archive"] != o["opening_head_sha"]:
                row["parent_sha"] = "미확인: new opened head parent not supplied"
            if o["opening_head_git_author_date"]:
                row["git_author_date"] = o["opening_head_git_author_date"]
                row["git_committer_date"] = o["opening_head_git_committer_date"]
            row["known_alternatives_before_archive"] = row["known_alternatives"]
            if row["slot_id"] in ("N-P1", "L-S1", "L-S2"):
                row["known_alternatives"] = o["prior_knowledge_correction"]
            row["source_ids"] += ";" + o["source_id"]
            row["head_metadata_source_id"] = o.get("head_metadata_source_id", "")
            if row["head_metadata_source_id"]:
                row["source_ids"] += ";" + row["head_metadata_source_id"]
    write_csv("baselines.csv", output)
    return output

def events():
    output = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / "events.csv"
        for number, row in enumerate(read_csv(path), 1):
            output.append({
                "event_id": row["event_id"], "slot_id": row["slot_id"], "pr_number": first(row, "pr_number", "pr"),
                "event_type": first(row, "event_type", "type"), "actor": first(row, "actor", "speaker"),
                "actor_role": row["actor_role"], "public_at": first(row, "public_at", "platform_at"),
                "comment_created_at": first(row, "comment_created_at", "authored_at"),
                "review_submitted_at": row.get("review_submitted_at", ""),
                "author_date": row.get("author_date", ""), "committer_date": row.get("committer_date", ""),
                "sha": row.get("sha", ""), "original_commit_id": row.get("original_commit_id", ""),
                "review_id": row.get("review_id", ""), "url": row["url"], "location": row["location"],
                "observed": first(row, "summary", "observed"), "target_url": row.get("target_url", ""),
                "link_class": row.get("link_class", ""), "within_primary_window": first(row, "within_primary_window", "in_main_window"),
                "public_time_limitation": first(row, "public_time_limit", "publication_note"),
                "source_ids": first(row, "source_ids", "source_id"),
                "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number,
            })
    opening_path = ROOT / "initial-public-heads.csv"
    if opening_path.exists():
        for number, o in enumerate(read_csv(opening_path), 1):
            output.append({
                "event_id": "ARCH-" + o["slot_id"], "slot_id": o["slot_id"], "pr_number": o["pr_number"],
                "event_type": "opened_snapshot_recovered_after_freeze", "actor": o["opening_actor"],
                "actor_role": "PR opener; not necessarily author of all shared branch code", "public_at": o["opening_event_utc"],
                "comment_created_at": "", "review_submitted_at": "", "author_date": o["opening_head_git_author_date"],
                "committer_date": o["opening_head_git_committer_date"], "sha": o["opening_head_sha"],
                "original_commit_id": o["opening_head_sha"], "review_id": "", "url": o["source_query_url"],
                "location": "PullRequestEvent/action=opened; repo+number+event.created_at; head/base/body", "observed": o["finding"],
                "target_url": o["diff_url"], "link_class": "not a reviewer precedent", "within_primary_window": "true",
                "public_time_limitation": "0–1 second after REST PR created_at; original event ID/raw archive not independently recovered",
                "source_ids": o["source_id"], "stream": "archive supplement", "stream_file": "initial-public-heads.csv", "stream_record": number,
            })
    for row in output:
        if row["event_id"] == "followup-pr-52053":
            row["sha_association_before_publication_recheck"] = row["sha"]
            row["sha"] = ""
            row["observed_before_publication_recheck"] = row["observed"]
            row["observed"] = "후속 PR52053가 링크 전에 개설됨; 당시 exact fa750 head는 미복구. 원작성자의 후속 통합19e는 별도 리뷰/부모 근거로 링크 뒤·원PR종결 전을 고정"
            row["public_time_limitation"] = "PR creation is distinct from exact patch publication; fa750 ancestor confirmed only by later19e review"
        if row["event_id"] == "followup-pr-52089":
            row["sha_association_before_publication_recheck"] = row["sha"]
            row["sha"] = ""
            row["observed_before_publication_recheck"] = row["observed"]
            row["observed"] = "후속 PR52089가 원PR종결45초전에 개설됨. 당시 head 미복구; current/surviving f95152e를 이 개설시각에 소급 고정하지 않음"
            row["public_time_limitation"] = "R03: exact f95152e first recovered SHA-specific review20:36:41Z after17:38:10Z closure; PR creation alone does not publish that exact revision"
    extra_events = [
        {"event_id":"PUB-LP2-1349354160","slot_id":"L-P2","pr_number":"51116","event_type":"post_closure_sha_specific_review","actor":"mroeschke","actor_role":"reviewer on successor52089","public_at":"2023-03-20T20:36:41Z","review_submitted_at":"2023-03-20T20:36:41Z","sha":"f95152e78c8baa2b1f4e07ecebb31496b3956c65","original_commit_id":"f95152e78c8baa2b1f4e07ecebb31496b3956c65","review_id":"1349354160","url":"https://github.com/pandas-dev/pandas/pull/52089#pullrequestreview-1349354160","location":"review.submitted_at/commit_id/state","observed":"Actual same-author successor patch fixed by approval, but after original PR first closure. Primary-window exact publication remains unknown.","within_primary_window":"false","source_ids":"RR-LP2-FIRST-PUBLIC","public_time_limitation":"First recovered exact SHA public anchor, not claimed actual first publication."},
        {"event_id":"PUB-COST-25261","slot_id":"N-S4","pr_number":"25274","event_type":"prehistory_consumer_qualitative_selfreport","actor":"gerardkr","actor_role":"consumer, not sampled PR author","public_at":"2022-12-30T18:33:16Z","sha":"","url":"https://github.com/scikit-learn/scikit-learn/issues/25261","location":"IssuesEvent opened body/Describe the bug/second paragraph","observed":"many hours cost sentence present in original opening body; numeric active time unknown, outside PR window and another person.","within_primary_window":"false","source_ids":"S-ARCH-COST-25261","public_time_limitation":"Documented normalized public event mirror; original raw event ID not independently recovered."},
        {"event_id":"PUB-S1-25605","slot_id":"L-S1","pr_number":"25535","event_type":"successor_opened_exact_head","actor":"fcharras","actor_role":"other author","public_at":"2023-02-14T09:22:47Z","sha":"feaabb7e6f2ccecced7a6847a267ad54b026f8a3","url":"https://github.com/scikit-learn/scikit-learn/pull/25605","location":"PullRequestEvent opened head/base;1commit2files","observed":"Opened headfeaabb7e/basea897a34 verifies recovered two-file other-author patch in primary window.","within_primary_window":"true","source_ids":"S-ARCH-SUCCESSOR-25605","public_time_limitation":"REST creation09:22:46; opened event09:22:47 is distinct exact-head public observation."},
    ]
    for row in extra_events:
        row.update({"stream":"publication recheck","stream_file":"streams/root/sources-supplement-boundary.jsonl" if row["slot_id"]=="L-P2" else "streams/sklearn/successor-publication-recovery.json","stream_record":"specified source_id"})
        output.append(row)
    integration = json.loads((ROOT/"streams/pandas/final-risk-review.json").read_text())
    for row in [
        {"event_id":"PUB-LP2-PARENT-1f7a","public_at":"2023-03-17T19:48:49Z","event_type":"upstream_merge_generates_parent_of_later_integration","actor":"phofl","actor_role":"merger of same-author prior logic; not the19e integration author","sha":integration["parent_provenance"]["sha"],"url":"https://github.com/pandas-dev/pandas/pull/52043","location":"merged_at/merge_commit_sha plus signed GitHub parent committer metadata","observed":"1f7a parent generated after firstlink; using its provenance to infer19e integration cannot precede this time. Logic itself had been authored before link.","source_ids":"P-FR-PARENT-1f7a7f20b1a3;P-FR-PR-52043-MERGE","public_time_limitation":"Inferred lower boundary for descendant integration, not its exact push time."},
        {"event_id":"PUB-LP2-1349064316","public_at":"2023-03-20T17:17:26Z","review_submitted_at":"2023-03-20T17:17:26Z","review_id":"1349064316","event_type":"in_window_review_fixes_postlink_integration","actor":"mroeschke","actor_role":"reviewer of same-author successor52053","sha":"19e864062c0d253db1b10469876b553391dad0db","url":"https://github.com/pandas-dev/pandas/pull/52053#pullrequestreview-1349064316","location":"review.submitted_at/commit_id/state; exact19e first-parent diff","observed":"Review fixes actual two-file nullable result-mask integration before original closure. Same author's integration is confirmed; first-link causation is not.","source_ids":"P-SUCC-REVIEW-1349064316;P-FR-C-19e864062c0d;P-FR-COMPARE-3ce5-19e8","public_time_limitation":"Direct public upper bound for exact19e; actual push time unknown."},
    ]:
        row.update({"slot_id":"L-P2","pr_number":"51116","within_primary_window":"true","stream":"R04 integration recheck","stream_file":"streams/pandas/final-risk-review.json","stream_record":"time_boundaries/parent_provenance"})
        output.append(row)
    write_csv("events.csv", output)
    return output

def optional_csv(name):
    rows = []
    for stream in ("pandas", "sklearn"):
        path = ROOT / "streams" / stream / name
        if not path.exists():
            raise FileNotFoundError(path)
        for number, raw in enumerate(read_csv(path), 1):
            if name == "changes.csv" and raw.get("change_id") == "L-P2-4":
                raw["public_anchor_before_publication_recheck"] = raw["public_anchor_at"]
                raw["causality_before_publication_recheck"] = raw["causality"]
                raw["public_anchor_at"] = "2023-03-20T17:17:26Z"
                raw["public_anchor_kind"] = "fa750 ancestor present by final19e review1349064316; exact opening head at PR creation unknown"
                raw["causality"] = "PR creation and git dates predate firstlink; exact fa750 opening publication unknown. Later ancestor presence alone does not show postlink modification. R04 separate19e first-parent integration is the positive."
                raw["source_ids"] = raw["source_id"] + ";P-SUCC-REVIEW-1349064316;P-FR-C-fa750f5fdaaf"
            if name == "changes.csv" and raw.get("change_id") == "L-P2-6":
                raw["phase_before_publication_recheck"] = raw["phase"]
                raw["public_anchor_before_publication_recheck"] = raw["public_anchor_at"]
                raw["phase"] = "post_closure_first_verified_SHA_publication; primary_window_publication_unknown"
                raw["public_anchor_at"] = "2023-03-20T20:36:41Z"
                raw["public_anchor_kind"] = "review1349354160 fixes f95152e; after sampled PR closure17:38:10"
                raw["within_primary_window"] = "미확인 for exact patch; first recovered public anchor is outside"
                raw["source_ids"] = raw["source_id"] + ";RR-LP2-FIRST-PUBLIC"
                raw["causality"] = "Same-author same-purpose actual successor code confirmed, but exact patch not established public within primary window; prior redesign and first-link contribution unresolved"
            if name == "changes.csv" and raw.get("change_id") == "S-C08":
                raw["platform_public_bound_before_recheck"] = raw["platform_public_bound"]
                raw["platform_public_bound"] = "2023-02-14T09:22:47Z exact opened head; REST PR creation09:22:46 is separate"
                raw["source_ids"] += ";S-ARCH-SUCCESSOR-25605"
            if name == "labor.csv" and raw["slot_id"] == "L-P2":
                raw["successor_patch_primary_window_publication"] = "f95152e only: 미확인; PR opened45sec before closure but exact SHA first recovered after closure. Independent19e integration confirmed in window by R04."
                raw["successor_patch_public_by"] = "2023-03-20T20:36:41Z; post_closure"
                raw["integration19e_public_by"] = "2023-03-20T17:17:26Z; primary_window"
                raw["integration19e_git_date"] = "2023-03-17T20:07:51Z; not active work duration or publication time"
                raw["integration_labor"] = "미확인; same-author integration of previously authored logic, not measured design creation effort"
                raw["source_ids"] += ";RR-LP2-FIRST-PUBLIC;P-FR-C-19e864062c0d;P-SUCC-REVIEW-1349064316"
            if name == "labor.csv" and raw["slot_id"] == "N-S4":
                raw["source_ids"] += ";S-ARCH-COST-25261"
            if name == "labor.csv" and raw["slot_id"] == "L-S1":
                raw["source_ids"] += ";S-ARCH-SUCCESSOR-25605"
            rows.append({**raw, "stream": stream, "stream_file": str(path.relative_to(ROOT)), "stream_record": number})
    if name == "changes.csv":
        d = json.loads((ROOT/"streams/pandas/final-risk-review.json").read_text())
        raw = dict(d["recommended_changes_row"])
        raw.update({"change_id":"L-P2-7","pre_sha":d["explicit_first_parent_comparison"]["base_sha"],"post_sha":raw["sha"],"change":d["same_purpose"]["actual_diff"],"hunks":";".join(f["filename"]+":"+" / ".join(f["hunks"]) for f in d["explicit_first_parent_comparison"]["files"]),"test_execution":"existing exact-tree tests read; not executed; no new tests in19e","within_primary_window":"true","integration_lower_bound_inferred":"2023-03-17T19:48:49Z","stream":"R04 integration recheck","stream_file":"streams/pandas/final-risk-review.json","stream_record":"recommended_changes_row/first-parent comparison/related_existing_tests","revert_status":"No new all-history revert search; existing sampled timeline scope remains"})
        raw["source_ids"] = ";".join(raw["source_ids"])
        rows.append(raw)
    write_csv(name, rows)
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("evidence", "all"), default="evidence")
    args = parser.parse_args()
    src, inputs = sources()
    baseline = baselines()
    ev = events()
    counts = {"sources_receipts": len(src), "counted_unique_works": sum(x["count_in_minimum"] for x in src),
              "allocation": dict(Counter(x["allocation"] for x in src if x["count_in_minimum"])),
              "baseline_rows": len(baseline), "event_rows": len(ev)}
    if args.stage == "all":
        for name in ("changes.csv", "labor.csv"):
            counts[name] = len(optional_csv(name))
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(), "stage": args.stage, "counts": counts,
               "source_input_sha256": inputs, "boundary": "Field normalization and work deduplication of directly-read evidence; not upstream test execution or causal validation."}
    (ROOT / "evidence" / "assembly.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False))

if __name__ == "__main__":
    main()
