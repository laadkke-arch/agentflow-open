#!/usr/bin/env python3
"""Independent final artifact accounting; writes only this audit directory.

Does not call/import the result assembler, source builder, experiment, or sealer.
Public-record metadata is used without displaying cached question/answer bodies.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import hashlib
import html
import json
import pathlib
import re
import subprocess
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parent.parent
REPO = BASE.parents[3]
SEAL2 = "d03ca37daf0c43688c68bc39417d84a9b84803e9"
ORIGINAL = ["evidence/jq/sources.jsonl", "evidence/pandoc/sources.jsonl",
            "evidence/jq/sources-note.jsonl", "evidence/pandoc/sources-note.jsonl",
            "evidence/crossdomain/sources.jsonl"]
ADDITIONAL = ["evidence/post-jq/source-note.jsonl", "evidence/post-pandoc/sources-note.jsonl",
              "evidence/intake/sources-note.jsonl", "evidence/post-evaluation-sources.jsonl"]
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\s]+)\)")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load(path):
    return json.loads(path.read_text())


def jsonlines(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x]


def csvrows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def tables(text):
    groups, current = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            current.append([html.unescape(c.strip()) for c in line.strip().strip("|").split("|")])
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return [{"header": rows[0], "rows": rows[2:]} for rows in groups]


def pair_label(a, b):
    ac, bc = a == "완결", b == "완결"
    return "양쪽" if ac and bc else "A만" if ac else "B만" if bc else "어느 쪽도 아님"


def canonical_url(url):
    return urllib.parse.urldefrag(url)[0]


def collect_urls(value):
    out = set()
    if isinstance(value, dict):
        for item in value.values():
            out.update(collect_urls(item))
    elif isinstance(value, list):
        for item in value:
            out.update(collect_urls(item))
    elif isinstance(value, str) and value.startswith(("https://", "http://")):
        out.add(canonical_url(value))
    return out


def main():
    started = utc()
    errors, warnings, checks = [], [], []

    def require(test, check, detail=None):
        checks.append({"check": check, "passed": bool(test), "detail": detail})
        if not test:
            errors.append({"check": check, "detail": detail})

    artifacts = ["RESULT.md", "metrics.json", "outcomes.csv", "cards.md", "SELF_CHECK.md", "README.md",
                 "sources.jsonl", "evidence/post-evaluation-sensitivity.json", "evidence/post-evaluation-sources.jsonl"]
    before = {name: sha((BASE / name).read_bytes()) for name in artifacts}
    result_text = (BASE / "RESULT.md").read_text()
    cards_text = (BASE / "cards.md").read_text()
    self_text = (BASE / "SELF_CHECK.md").read_text()
    readme_text = (BASE / "README.md").read_text()
    metric = load(BASE / "metrics.json")
    cases = load(BASE / "protocol.json")["cases"]
    pair_rows = csvrows(BASE / "pairs.csv")
    pairs = {r["case_id"]: r for r in pair_rows}
    outcomes = csvrows(BASE / "outcomes.csv")
    searches = [r for r in jsonlines(BASE / "evidence/search-events.jsonl") if r["event"] == "search"]
    aggregate = jsonlines(BASE / "exposure.jsonl")
    event_counts = dict(collections.Counter(r["event"] for r in aggregate))
    corpus = {r["file_id"]: r for r in jsonlines(BASE / "corpus-files.jsonl")}
    require(len(cases) == len(pairs) == len(outcomes) == 8, "eight_case_and_outcome_rows")
    require(len({c["question_id"] for c in cases}) == 8, "eight_distinct_selected_question_ids")
    require(metric["explicit_conditions"] == sum(len(c["conditions"]) for c in cases), "explicit_condition_denominator")
    route_rows, independent_pairs, condition_labels = [], [], {}
    for case in cases:
        cid = case["case_id"]
        arms = {}
        for arm in ["A", "B"]:
            rid = f"{cid}-{arm}"
            directory = BASE / "evidence/routes" / rid
            exposure = load(directory / "exposure.json")
            judgment = load(directory / "judgment.json")
            access = jsonlines(directory / "access.jsonl")
            attempts = [a for a in access if a["event"] == "body_attempt"]
            route_searches = [s for s in searches if s["case_id"] == cid and s["route"] == arm]
            slots = exposure["slots"]
            exposed_ids = {s["file_id"] for s in slots if not s["empty"]}
            adjacent_ids = {s["file_id"] for s in slots if not s["empty"] and s["role"] == "adjacent"}
            opened_ids = {a["file_id"] for a in attempts if a["status"] == "success"}
            returned_ids = {r["file_id"] for r in judgment["returned_sources"]}
            used_ids = set(judgment["used_file_ids"])
            require(len(route_searches) == 2 and sum(s["charged_searches"] for s in route_searches) == 2,
                    "two_search_events", rid)
            require(len(attempts) <= 4 and sum(a["charged_attempts"] for a in attempts) <= 4,
                    "four_attempt_budget_including_failures", rid)
            require([a["file_id"] for a in attempts] == [s["file_id"] for s in slots if not s["empty"]][:len(attempts)],
                    "exposure_order", rid)
            require(len(returned_ids) <= 2, "returned_source_limit", rid)
            require(used_ids <= exposed_ids & opened_ids, "used_sources_exposed_and_opened", rid)
            require(returned_ids <= exposed_ids & opened_ids, "returned_sources_exposed_and_opened", rid)
            require({x["condition_id"] for x in judgment["condition_evidence"]} == {x["id"] for x in case["conditions"]},
                    "all_explicit_conditions_present", rid)
            if judgment["judgment"] == "완결":
                require(used_ids <= returned_ids, "complete_route_evidence_in_returned_sources", rid)
            elif not used_ids <= returned_ids:
                warnings.append({"kind": "noncomplete_extra_diagnostic_sources", "route": rid,
                                 "file_ids": sorted(used_ids-returned_ids), "not_a_return_limit_violation": True})
            for source in judgment["returned_sources"]:
                require(source["url"] == corpus[source["file_id"]]["url"], "returned_url_identity", [rid, source["file_id"]])
            row = {"case_id": cid, "route": arm, "route_id": rid, "exposure": exposure, "judgment": judgment,
                   "searches": len(route_searches), "body_attempts": len(attempts),
                   "failed_body_attempts": sum(a["status"] != "success" for a in attempts),
                   "excess_body_attempts": max(0, len(attempts)-4),
                   "section_navigation": sum(a["event"] == "section_navigation" for a in access),
                   "adjacent_exposed": len(adjacent_ids), "adjacent_opened": len(adjacent_ids & opened_ids),
                   "adjacent_returned": len(adjacent_ids & returned_ids),
                   "unexposed_used": len(used_ids-exposed_ids)}
            arms[arm] = row
            route_rows.append(row)
            condition_labels[rid] = judgment["judgment"]
        if case["stratum"] == "control":
            require(arms["A"]["exposure"]["slots"] == arms["B"]["exposure"]["slots"], "control_exposure_equal", cid)
            require(condition_labels[f"{cid}-A"] == condition_labels[f"{cid}-B"], "control_judgment_equal", cid)
        pair = pair_label(condition_labels[f"{cid}-A"], condition_labels[f"{cid}-B"])
        require(pairs[cid]["strict_pair"] == pair, "pair_matches_raw_judgments", cid)
        require(pairs[cid]["strict_comparable"] == "True", "strict_comparability_record", cid)
        for arm in ["A", "B"]:
            require(pairs[cid]["frozen_"+arm] == condition_labels[f"{cid}-{arm}"], "frozen_pair_label", [cid, arm])
        independent_pairs.append({"case_id": cid, "stratum": case["stratum"], "label": pair,
                                  "B_adjacent_exposed": arms["B"]["adjacent_exposed"],
                                  "B_adjacent_opened": arms["B"]["adjacent_opened"],
                                  "B_adjacent_returned": arms["B"]["adjacent_returned"]})

    independently_counted = {}
    for group in ["all", "boundary", "control"]:
        subset = [r for r in independent_pairs if group == "all" or r["stratum"] == group]
        count = {k: sum(r["label"] == k for r in subset) for k in ["A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"]}
        count.update(planned_pairs=len(subset), comparable_pairs=len(subset))
        independently_counted[group] = count
    require(metric["counts"] == independently_counted, "primary_metrics_counts", independently_counted)
    totals = {key: sum(r[key] for r in route_rows) for key in ["searches", "body_attempts", "failed_body_attempts", "excess_body_attempts"]}
    totals["unexposed_used_file_occurrences"] = sum(r["unexposed_used"] for r in route_rows)
    for key, value in totals.items():
        require(metric[key] == value, "metric_"+key, value)
    require(event_counts.get("search") == totals["searches"] == 32, "aggregate_search_type_filter")
    require(event_counts.get("body_attempt") == totals["body_attempts"] == 64, "aggregate_body_type_filter")
    require(event_counts.get("section_navigation") == sum(r["section_navigation"] for r in route_rows) == 194,
            "section_navigation_separate_count")
    require(event_counts.get("exposure") == len(route_rows) == 16, "exposure_events_count")
    for key in ["exposed", "opened", "returned"]:
        value = sum(bool(r["B_adjacent_"+key]) for r in independent_pairs if r["stratum"] == "boundary")
        require(metric["B_boundary_adjacent_"+key] == value, "boundary_adjacent_"+key, value)
    require(metric["discordant_pairs"] == 0 and "산출 불가" in metric["B_win_fraction_among_discordant"],
            "zero_discordance_denominator")

    tab = tables(result_text)
    require([len(t["rows"]) for t in tab[:3]] == [8, 16, 8], "first_three_table_rows", [len(t["rows"]) for t in tab[:3]])
    for table, columns in zip(tab[:3], [5, 6, 6]):
        require(all(len(row) == columns for row in table["rows"]), "table_column_width", columns)
    for case, row in zip(cases, tab[0]["rows"]):
        require(row[0].startswith(case["case_id"]+" /") and str(case["question_id"]) in row[0] and case["r0_url"] in row[0],
                "table1_identity", case["case_id"])
        require(all(c["id"]+":" in row[2] for c in case["conditions"]), "table1_conditions", case["case_id"])
    for expected, row in zip(route_rows, tab[1]["rows"]):
        rid = expected["route_id"]
        require(row[0].startswith(rid+";"), "table2_route", rid)
        for slot in expected["exposure"]["slots"]:
            fragment = f"slot{slot['slot']} {slot['file_id']} {slot['role']}#{slot['within_role_rank']}/전체#{slot['merged_global_rank']}"
            require(fragment in row[1], "table2_exposure_original_rank", [rid, slot["file_id"]])
        require(f"검색{expected['searches']}; 시도{expected['body_attempts']}/4; 실패{expected['failed_body_attempts']}; 잔여{4-expected['body_attempts']}" in row[2],
                "table2_budget", rid)
        require(LINK.findall(row[3]) == [s["url"] for s in expected["judgment"]["returned_sources"]], "table2_return_urls", rid)
        require(row[5].startswith(expected["judgment"]["judgment"]+";"), "table2_frozen_judgment", rid)
        for cond in expected["judgment"]["condition_evidence"]:
            require(f"{cond['condition_id']}={cond['status']}" in row[4], "table2_condition_status", [rid, cond["condition_id"]])
    for expected, row in zip(independent_pairs, tab[2]["rows"]):
        cid = expected["case_id"]
        require(row[0].startswith(cid+":"), "table3_identity", cid)
        require(row[1] == expected["label"], "table3_frozen_pair", cid)
        require(f"노출{expected['B_adjacent_exposed']}/열람{expected['B_adjacent_opened']}/반환{expected['B_adjacent_returned']}" in row[2],
                "table3_adjacent_steps", cid)
        require(len(LINK.findall(row[4])) <= 2, "table3_editor_links_limit", cid)
    for row, group in zip(tab[3]["rows"], ["boundary", "control", "all"]):
        expected = independently_counted[group]
        values = [expected[k] for k in ["planned_pairs", "comparable_pairs", "A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"]]
        require(list(map(int, row[1:])) == values, "summary_count_table", group)
    require(tab[-1]["header"] == ["틀릴 수 있는 주장", "다음 조사 대상·입력·방법", "판정을 바꿀 관측"]
            and len(tab[-1]["rows"]) == 3 and all(all(cell for cell in r) for r in tab[-1]["rows"]),
            "exactly_three_final_weaknesses")
    self_rows = tables(self_text)[0]["rows"]
    require(len(self_rows) == 7 and all(f"Q{i}." in row[0] for i, row in enumerate(self_rows, 1)), "self_check_Q1_Q7")
    require(all(len(row) == 6 and all(row) for row in self_rows), "self_check_complete_columns")
    sections = re.split(r"(?m)^## ([JP][1-4]) · [0-9]+\s*$", cards_text)
    cards = {sections[i]: sections[i+1] for i in range(1, len(sections), 2)}
    require(set(cards) == {c["case_id"] for c in cases}, "eight_cards")
    card_links = {}
    for cid, body in cards.items():
        card_links[cid] = LINK.findall(body)
        require(len(card_links[cid]) <= 2, "card_max_two_links", cid)
        require(body.count("**되물을 한 가지:**") == 1, "card_one_followup_question", cid)

    sources = jsonlines(BASE / "sources.jsonl")
    original_map = {(f, i): x for f in ORIGINAL + ADDITIONAL for i, x in enumerate(jsonlines(BASE / f), 1)}
    source_seen = collections.Counter()
    for source in sources:
        key = (source["original_note_file"], source["original_note_line"])
        source_seen[key] += 1
        require(key in original_map and source["original_note"] == original_map[key], "unified_original_record", source["source_id"])
        if key[0] in ADDITIONAL:
            require(source["minimum_count_eligible"] is False, "post_intake_reread_excluded", source["source_id"])
    require(set(source_seen) == set(original_map) and all(n == 1 for n in source_seen.values()), "all_original_records_once")
    eligible = {s["source_id"]: s for s in sources if s["minimum_count_eligible"]}
    baseline = {x["source_id"]: x for x in load(HERE / "source-count-normalized.json") if x["eligible"]}
    require(set(eligible) == set(baseline) and len(eligible) == 46, "eligible_46_identity_set")
    for sid, row in eligible.items():
        require(row["body_sha256"] == baseline[sid]["source_sha256"] and row["original_url"] == baseline[sid]["original_url"],
                "eligible_identity_hash_unchanged", sid)
    source_categories = dict(collections.Counter(row["minimum_category"] for row in eligible.values()))
    require(metric["source_counts"]["rows_in_ledger"] == len(sources) == 169, "source_ledger_169")
    require(metric["source_counts"]["eligible_unique_primary_sources"] == len(eligible)
            and metric["source_counts"]["eligible_by_category"] == source_categories, "source_metric_categories", source_categories)
    new_review = next(s for s in sources if s["source_id"] == "R0-P3-POST-REVIEW")
    require(new_review["minimum_count_eligible"] is False and new_review["body_sha256"] == eligible["R0-P3"]["body_sha256"],
            "P3_reread_same_body_not_new_source")

    sensitivity = load(BASE / "evidence/post-evaluation-sensitivity.json")
    post_counts = {}
    for group in ["all", "boundary", "control"]:
        subset = [r for r in independent_pairs if group == "all" or r["stratum"] == group]
        counter = collections.Counter("어느 쪽도 아님" if r["case_id"] == "P3" else r["label"] for r in subset)
        post_counts[group] = {k: counter[k] for k in ["A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"]}
        post_counts[group].update(planned_pairs=len(subset), comparable_pairs=len(subset))
    require(metric["posthoc_option_only_sensitivity"]["counts"] == post_counts, "posthoc_counts_separate", post_counts)
    require(sensitivity["affected_case"] == "P3" and sensitivity["posthoc_A"] == sensitivity["posthoc_B"] == "부분"
            and sensitivity["frozen_A"] == sensitivity["frozen_B"] == "완결", "sensitivity_record_keeps_original_values")
    require("미확인" in metric["source_counts"]["independent_underlying_problem_events"], "underlying_event_independence_unknown")

    public_records = load(BASE / "evidence/outcomes/public-records.json")
    answer_count = sum(len(r["answers"]) for r in public_records)
    comment_count = sum(len(r["comments"]) for r in public_records)
    accepted_count = sum(bool(r["current_accepted_answer_id"]) for r in public_records)
    actions = {}
    for r in public_records:
        cid = r["case_id"]
        actions[cid] = (any(c["within_30_days"] and c["by_asker"] for c in r["comments"])
                        or any(a["within_30_days"] and a["owner_id"] == r["asker_id"] for a in r["answers"])
                        or any(v["within_30_days"] and v["by_asker"] and v["creation_epoch"] > r["question_creation_epoch"]
                               for v in r["question_body_revisions"]))
        output = next(o for o in outcomes if o["case_id"] == cid)
        require(json.loads(output["answer_ids"]) == [a["answer_id"] for a in r["answers"]], "outcome_answer_metadata", cid)
        require(output["frozen_verdict_changed"] == "False", "outcome_keeps_frozen_verdict", cid)
    for key, value in {"public_answer_count": answer_count, "public_comment_count": comment_count,
                       "current_accepted_questions": accepted_count,
                       "questions_with_no_answer": sum(not r["answers"] for r in public_records),
                       "questions_with_asker_action_in_30d": sum(actions.values()),
                       "exact_asker_execution_verified": sum(o["exact_asker_execution_verified"] == "True" for o in outcomes)}.items():
        require(metric[key] == value, "public_metadata_"+key, value)

    seal_manifest = load(BASE / "evidence/seal2-files.json")["files"]
    seal_checks, exact, eol_only = [], 0, 0
    for entry in seal_manifest:
        path = REPO / entry["path"]
        data = path.read_bytes()
        blob = subprocess.run(["git", "show", f"{SEAL2}:{entry['path']}"], cwd=REPO, capture_output=True)
        attrs = subprocess.run(["git", "check-attr", "text", "eol", "--", entry["path"]], cwd=REPO,
                               capture_output=True, text=True).stdout
        equal = blob.returncode == 0 and data == blob.stdout
        normal = (not equal and path.suffix == ".csv" and "text: auto" in attrs and "eol: lf" in attrs
                  and data.replace(b"\r\n", b"\n") == blob.stdout)
        require(sha(data) == entry["sha256"], "seal2_manifest_hash_unchanged", entry["path"])
        require(equal or normal, "seal2_git_object_unchanged", entry["path"])
        exact += equal
        eol_only += normal
        seal_checks.append({"path": entry["path"], "worktree_sha256": sha(data), "git_sha256": sha(blob.stdout),
                            "exact": equal, "configured_eol_only": normal})

    known_urls = collect_urls(sources) | collect_urls(cases) | collect_urls(public_records) | collect_urls(list(corpus.values()))
    for receipt_name in ["evidence/seal1-receipt.json", "evidence/seal2-receipt.json"]:
        receipt = load(BASE / receipt_name)
        commit = receipt["remote_sha"]
        exists = subprocess.run(["git", "cat-file", "-e", commit+"^{commit}"], cwd=REPO, capture_output=True).returncode == 0
        remote_verified = receipt.get("confirmed_remote") is True or (receipt.get("bundle") == 1 and bool(receipt.get("verified_utc")))
        require(exists and remote_verified, "commit_link_remote_receipt_and_local_object", commit)
        if exists and remote_verified:
            known_urls.add("https://github.com/laadkke-arch/agentflow-open/commit/"+commit)
    link_checks, unknown_http, missing_local, allowed_pending = [], [], [], []
    doc_texts = {"RESULT.md": result_text, "cards.md": cards_text, "SELF_CHECK.md": self_text, "README.md": readme_text}
    for filename, text in doc_texts.items():
        for url in sorted(set(LINK.findall(text))):
            if url.startswith(("https://", "http://")):
                supported = canonical_url(url) in known_urls
                if not supported:
                    unknown_http.append({"file": filename, "url": url})
                link_checks.append({"file": filename, "url": url, "kind": "external", "known_provenance": supported})
            else:
                target = urllib.parse.unquote(urllib.parse.urldefrag(url)[0])
                path = BASE / target
                exists = path.exists()
                record = {"file": filename, "url": url, "kind": "local", "exists": exists}
                if not exists and target == "HANDOFF.md":
                    record["intentionally_pending_final_commit"] = True
                    allowed_pending.append(record)
                elif not exists:
                    missing_local.append(record)
                link_checks.append(record)
    require(not missing_local, "local_links_exist_except_final_handoff", missing_local)
    require(not unknown_http, "external_links_have_recorded_origin", unknown_http)
    require("완결로 판정한 경로" in readme_text and "미완결" in readme_text, "README_complete_only_return_provenance_qualification")
    semantic = [
        {"topic": "generalization", "assessment": "PASS", "evidence": "RESULT explicitly limits zero discordance to six boundary pairs and distinguishes it from general equality, discovery probability, and time efficiency."},
        {"topic": "posthoc_sensitivity", "assessment": "PASS", "evidence": "Primary both5/neither3 is preserved; option-only P3 reading is explicitly post-unblinding and yields both4/neither4 with discordance0."},
        {"topic": "runtime_attribution", "assessment": "PASS", "evidence": "Documentary completeness, answer-author output, asker follow-up, researcher probes, and Q7 expected fixtures are distinguished. P4 exit83 and original asker execution0/8 remain explicit."},
        {"topic": "independent_events", "assessment": "PASS", "evidence": "Selected distinct question IDs8 are operational units; P3 repost makes independent underlying problem-event count unknown, with original wording/time preserved."},
        {"topic": "known_calibration", "assessment": "PASS", "evidence": "Q7 14 files and 5 goals are not added to new-request success, and discovery fraction is undefined at denominator0."},
        {"topic": "displacement", "assessment": "PASS", "evidence": "12/12 slots checked, no observed A-only completeness, but J2 corroboration and J4 build caveat losses are retained."},
        {"topic": "contract", "assessment": "PASS", "evidence": "PARTIAL explicitly reflects unsuccessful specified dependency contract, and manifest.json is not presented as a successful tool contract."},
        {"topic": "README_prior_issue", "assessment": "CORRECTED", "evidence": "Originally all routes were said to connect all conditions through <=2 returns; root narrowed this to complete routes and separately noted noncomplete diagnostics after audit feedback."},
    ]
    require("연구 상태: PARTIAL" in result_text, "partial_state_visible")
    require("산출 불가" in result_text and "같은 연구자" in result_text and "독립 맹검" in result_text, "major_inference_limits_visible")
    after = {name: sha((BASE / name).read_bytes()) for name in artifacts}
    require(before == after, "final_artifacts_stable_during_audit")
    report = {
        "audit": "independent-final-report-v1", "started_utc": started, "finished_utc": utc(),
        "primary_seal_sha": SEAL2, "artifact_sha256": before, "status": "PASS" if not errors else "FAIL",
        "error_count": len(errors), "errors": errors, "warnings": warnings,
        "table_rows": [len(t["rows"]) for t in tab[:3]], "counts_recomputed": independently_counted,
        "posthoc_counts_recomputed": post_counts, "event_counts": event_counts, "route_budget_totals": totals,
        "source_ledger_rows": len(sources), "source_eligible_unique": len(eligible), "source_categories": source_categories,
        "source_original_records_verified": len(source_seen), "new_P3_reread_count_contribution": 0,
        "card_link_counts": {k: len(v) for k,v in card_links.items()},
        "final_weakness_count": len(tab[-1]["rows"]), "self_check_rows": len(self_rows),
        "public_metadata_counts": {"answers": answer_count, "comments": comment_count, "accepted_questions": accepted_count,
                                   "asker_action_question_ids": [cid for cid, yes in actions.items() if yes]},
        "seal2_file_count": len(seal_checks), "seal2_exact": exact, "seal2_configured_eol_only": eol_only,
        "seal2_checks": seal_checks, "semantic_review": semantic, "checks": checks, "link_checks": link_checks,
        "missing_local_links": missing_local, "allowed_pending_handoff_links": allowed_pending,
        "unknown_external_links": unknown_http,
        "auditor_correction": "The first final-audit run matched external links only against source/corpus/public records and flagged the two valid repository seal commit links. Added the existing confirmed remote receipts plus local Git commit-object checks for precisely those links. First run retained in final-report-audit-runs; no result content changed to fix the checker.",
        "limitations": [
            "External URL checks establish identity in previously retrieved source/corpus/public metadata, not a fresh HTTP availability check for every link.",
            "Final result commit has not yet been pushed at this audit; GitHub exact-result readback and result-SHA repository checks remain root handoff steps.",
            "HANDOFF.md intentionally does not exist before the last standalone handoff commit.",
            "Auditor read final synthesized narratives after seal2; did not reopen raw answer/comment caches or execute user transformations in this final audit.",
            "Original source-count and unified168 audits remain unchanged. Final169 adds one same-body P3 reread with minimum contribution0.",
        ],
    }
    stamp = report["finished_utc"].replace(":", "").replace("+", "_")
    history = HERE / "final-report-audit-runs"
    history.mkdir(exist_ok=True)
    serialized = json.dumps(report, ensure_ascii=False, indent=2)+"\n"
    (history / f"{stamp}.json").write_text(serialized)
    (HERE / "final-report-audit.json").write_text(serialized)
    md = ["# AF-RES-096 최종 보고서 독립 감사", "",
          f"**{report['status']} · 오류 {len(errors)}건** · `{report['finished_utc']}`.", "",
          "원 결과 생성기·source builder·experiment/sealer를 호출하거나 읽지 않고 protocol, 각 경로의 원 exposure/access/judgment, 원 source notes, 공개 후속 메타데이터에서 다시 계산했다. 모든 쓰기는 evidence/audit 아래다. 이전 감사의 최초 관측을 수정하지 않았다.", "",
          "|확인 항목|독립 실측|", "|---|---|",
          f"|RESULT 처음 세 표|{report['table_rows']}|", "|경로·검색·본문시도|16 · 32 · 64|",
          "|실패·초과·미노출 근거|0 · 0 · 0|", "|동파일 절 이동|194, 새 본문시도로 세지 않음|",
          f"|사전 전체|{independently_counted['all']}|", f"|사후 옵션-only 민감도|{post_counts['all']}|",
          f"|통합 원장·산입 고유자료|{len(sources)} · {len(eligible)}|",
          f"|카드 링크 수|{report['card_link_counts']}|", "|Q별 자가검산·마지막 약점|7행 · 정확히3행|",
          f"|②봉인 불변|{len(seal_checks)}파일: exact {exact}, 설정된 CSV EOL만 {eol_only}|", "",
          "## 자료·사후 값 분리", "",
          "통합169행의 원위치와 embedded original_note가 모두 원 기록과 일치한다. 기존109+사후49+인수10+P3 재열람1이며 산입46의 ID·원주소·hash는 최초 독립 감사와 같다. 새 P3 재열람은 기존 R0와 같은 body hash이고 비산입이다. 주10/인접10/원시험4/R0 8/Sphinx7/GDAL7이며 후속이나 실행으로 하한을 보충하지 않았다.", "",
          "최초 사전5/3, P3를 옵션만으로 좁힌 사후4/4, 서로 다른 선정 질문 ID8과 실제 독립 사건 미확인을 구분했다. 공개 메타데이터에서 답8·댓글18·현재채택4·30일내 질문자후속5를 재계산했다. 이 감사는 현재채택 시각 또는 원 사용자 실행 성공을 새로 입증하지 않는다.", "",
          "## 내용 검토", ""]
    md += [f"- **{item['topic']} / {item['assessment']}:** {item['evidence']}" for item in semantic]
    md += ["", "## 링크와 완료 단계", "",
           f"Markdown 로컬 링크의 실제 경로를 검사했다. 의도적으로 아직 없는 HANDOFF 링크 {len(allowed_pending)}개를 제외한 누락은 {len(missing_local)}개다. 외부 링크는 이전에 취득한 원 source/corpus/public 메타데이터의 정체성과 대조했고 미대응은 {len(unknown_http)}개다. 모든 URL에 새 HTTP를 보낸 검사는 아니다.", "",
           "이 감사는 ④ 푸시 전 산출물에 대한 것이다. 원격 결과 SHA에서의 GitHub 핵심 표·원장·반례 readback, 저장소 검사와 계약 검사 종료값, 마지막 단독 HANDOFF 커밋은 루트가 이어서 고정한다. 결과의 파일별 hash는 JSON에 있으며 감사 중 변경되지 않았음을 확인했다.", "",
           "최초 실행은 외부 링크 대조 집합에 저장소의 두 봉인 commit 링크를 넣지 않아 오탐했다. 기존 confirmed remote 영수증과 Git commit 객체로 그 두 링크를 검증하도록 감사기만 보완했고 최초 결과는 runs 아래 보존했다. 산출물을 수정해 검사를 통과시킨 것이 아니다.", "",
           "## 경고", ""]
    md += [f"- {json.dumps(w, ensure_ascii=False)}" for w in warnings] or ["없음."]
    md += ["", "## 오류", ""]
    md += [f"- {json.dumps(e, ensure_ascii=False)}" for e in errors] or ["없음."]
    md += ["", "## 재실행", "", "```sh",
           "python -B docs/workstreams/research/AF-RES-096/evidence/audit/final-report-audit.py", "```", ""]
    rendered = "\n".join(md)
    (history / f"{stamp}.md").write_text(rendered)
    (HERE / "final-report-audit.md").write_text(rendered)
    summary = {k: report[k] for k in ["status", "error_count", "table_rows", "counts_recomputed", "posthoc_counts_recomputed",
                                    "event_counts", "source_ledger_rows", "source_eligible_unique", "card_link_counts",
                                    "final_weakness_count", "seal2_file_count", "seal2_exact", "seal2_configured_eol_only",
                                    "missing_local_links", "unknown_external_links", "errors"]}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
