#!/usr/bin/env python3
"""Audit the committed research denominators; never rerun A/B searches or conversions."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PREFIX = ROOT.relative_to(REPO).as_posix()
SEAL1 = "498feab24f0671273a0a91a8868e5c318e8093a3"
SEAL2 = "a04fbb20ca1a415235f69a1018a93e07e7adc926"


def csv_rows(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def jsonl_rows(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines()]


def normalized(data):
    return data.replace(b"\r\n", b"\n")


def main():
    frame = csv_rows("frame.csv")
    candidates = csv_rows("candidates.csv")
    outcomes = csv_rows("outcomes.csv")
    events = jsonl_rows("searches.jsonl")
    sources = jsonl_rows("sources.jsonl")
    expected_ids = [78264525, 78265746, 78304807, 78273711, 78311072, 78358965]
    assert [int(row["question_id"]) for row in frame] == expected_ids
    assert len(frame) == len(outcomes) == 6
    assert len(candidates) == 12
    assert len({(row["case_id"], row["route"]) for row in candidates}) == 12
    assert len({row["source_id"] for row in sources}) == len(sources)

    frozen_checks = {}
    for name, seal in [("frame.csv", SEAL1), ("search_plan.json", SEAL1),
                       ("candidates.csv", SEAL2), ("searches.jsonl", SEAL2)]:
        old = subprocess.check_output(["git", "show", f"{seal}:{PREFIX}/{name}"], cwd=REPO)
        now = (ROOT / name).read_bytes()
        assert normalized(old) == normalized(now), f"Frozen artifact changed: {name}"
        frozen_checks[name] = {"seal": seal, "git_blob_sha256": hashlib.sha256(old).hexdigest()}

    route_metrics = []
    for candidate in candidates:
        case, route = candidate["case_id"], candidate["route"]
        own = [event for event in events if event.get("case_id") == case and event.get("route") == route]
        searches = [event for event in own if event["event"] == "search"]
        opened = [event for event in own if event["event"] == "open"]
        failures = [event for event in own if event["event"] == "open_failure"]
        close = [event for event in own if event["event"] == "close"]
        assert len(searches) == 2 and len(close) == 1
        assert {event["query_number"] for event in searches} == {1, 2}
        distinct = {(event["repository"], event["path"]) for event in opened}
        assert len(distinct) == int(candidate["source_opens"]) <= 4
        assert len(opened) == len(distinct), "Source reopens must be identified before counting"
        assert close[0]["sources_opened"] == len(distinct)
        assert int(candidate["unused_source_opens"]) == 4 - len(distinct)
        assert len([candidate[key] for key in ["return_link_1", "return_link_2"] if candidate[key]]) <= 2
        search_failures = sum(event.get("status") == "failed_before_exposure" for event in searches)
        partial_corpus = sum(bool(event.get("failures")) and event.get("status") != "failed_before_exposure" for event in searches)
        primary = "jq" if case.startswith("J") else "pandoc"
        adjacent_exposed = sum(hit["repository"] != primary for event in searches for hit in event.get("exposed", []))
        route_metrics.append({
            "case_id": case, "route": route, "searches_charged": len(searches),
            "searches_with_output": len(searches) - search_failures,
            "searches_with_partial_corpus": partial_corpus,
            "successful_source_reads": len(distinct), "failed_source_attempts": len(failures),
            "distinct_source_attempts": len(distinct) + len(failures),
            "navigation_events": sum(event["event"] == "navigation" for event in own),
            "adjacent_search_hits_exposed": adjacent_exposed,
            "adjacent_sources_read": sum(repo != primary for repo, path in distinct),
            "unused_searches": 2 - len(searches), "unused_source_reads": 4 - len(distinct),
            "frozen_judgment": candidate["judgment"],
        })

    required = ["source_id", "work_event_id", "lineage_id", "url", "published_utc", "read_utc",
                "version_commit_file_section", "questions_cases", "observation", "excerpt",
                "fingerprint_or_discriminator", "support_or_refute", "limitations", "reopen_path"]
    for source in sources:
        assert all(key in source for key in required), source["source_id"]
        assert source.get("independent_work_event_group"), source["source_id"]
    # Concrete reconciliation gate: these rereads add neither route evidence nor sources.
    source_by_id = {source["source_id"]: source for source in sources}
    for source in sources:
        if not source["source_id"].startswith("RESUME-"):
            continue
        assert source["reopens_source_id"] in source_by_id, source["source_id"]
        for flag in ("count_minimum", "counted_direct", "counted_minimum", "counted_unique_source"):
            assert not source.get(flag, False), (source["source_id"], flag)
        if "directly_opened" in source:
            assert source["directly_opened"] == source["direct_read"], source["source_id"]
        if source["direct_read"]:
            assert source.get("evidence_kind") != "failed_access", source["source_id"]
            original = source_by_id[source["reopens_source_id"]]
            assert source["lineage_id"] == original["lineage_id"], source["source_id"]
    counted = [source for source in sources if source.get("count_minimum")]
    category = Counter(source["category"] for source in counted)
    audio = sum(count for name, count in category.items() if name.startswith("audio_"))
    ebook = sum(count for name, count in category.items() if name.startswith("cross_domain_ebook"))
    assert category["new_r0"] == 6
    assert category["manual_code"] >= 8
    assert category["upstream_behavior"] >= 6
    assert audio >= 3 and ebook >= 3 and len(counted) >= 26
    assert not any(source.get("count_minimum") for source in sources if source["source_id"].startswith("CAL-"))

    first_answers = json.loads((ROOT / "evidence/outcomes/answer-first-receipts.json").read_text())
    comments = json.loads((ROOT / "evidence/outcomes/comment-receipts.json").read_text())
    assert len({row["answer_id"] for row in first_answers}) == 7
    assert sum(int(row["answer_count"]) for row in outcomes) == 7
    assert sum(bool(row["accepted_answer_id_now"]) for row in outcomes) == 5
    assert all(row["within_30_days"] for row in first_answers + comments)
    assert all(row["asker_exact_version_and_output_verified"] == "False" for row in outcomes)

    pairs = []
    for row in frame:
        case = row["case_id"]
        pair = {candidate["route"]: candidate for candidate in candidates if candidate["case_id"] == case}
        outcome = next(item for item in outcomes if item["case_id"] == case)
        complete_a, complete_b = [pair[route]["judgment"] == "완결" for route in ["A", "B"]]
        category_name = "양쪽" if complete_a and complete_b else "A만" if complete_a else "B만" if complete_b else "어느 쪽도 아님"
        strict = "비교불가" if case == "P2" else category_name
        costs = {item["route"]: item for item in route_metrics if item["case_id"] == case}
        pairs.append({
            "case_id": case, "question_id": row["question_id"], "r0_url": row["r0_url"],
            "route_order": row["route_order"], "frozen_A": pair["A"]["judgment"],
            "frozen_B": pair["B"]["judgment"], "frozen_pair_classification": category_name,
            "strict_comparison_classification": strict,
            "retrieval_fault": case == "P2", "strict_attempt_budget_violation": case == "P2",
            "post_document_fit_A": outcome["post_document_fit_A"],
            "post_document_fit_B": outcome["post_document_fit_B"],
            "source_read_delta_B_minus_A": costs["B"]["successful_source_reads"] - costs["A"]["successful_source_reads"],
            "attempt_delta_B_minus_A": costs["B"]["distinct_source_attempts"] - costs["A"]["distinct_source_attempts"],
            "asker_exact_execution_verified": False,
            "limitation": "P2 B has partial-corpus query1, failed query2 and 5 attempts; original Quarto chain incomplete" if case == "P2" else "same researcher crossover; documentary fit is not asker execution",
        })
    with (ROOT / "pairs.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(pairs[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pairs)

    metrics = {
        "scope": "AF-RES-092; all post-verification remains outside frozen A/B route evidence",
        "recruited_questions": 6, "executed_routes": 12, "planned_primary_pairs": 6,
        "strictly_comparable_pairs": 5, "incomparable_pairs": ["P2"],
        "frozen_pair_counts": dict(Counter(row["frozen_pair_classification"] for row in pairs)),
        "strict_pair_counts": {name: sum(row["strict_comparison_classification"] == name for row in pairs)
                               for name in ["A만", "B만", "양쪽", "어느 쪽도 아님", "비교불가"]},
        "B_only_complete_strict": {"numerator": 0, "denominator": 5},
        "discordant_strict_pairs": 0,
        "winner_fraction_among_discordant": "산출 불가 (분모 0)",
        "post_conservative_both_complete": 2,
        "search_budget": 24, "searches_charged": sum(row["searches_charged"] for row in route_metrics),
        "searches_with_output": sum(row["searches_with_output"] for row in route_metrics),
        "partial_corpus_searches": sum(row["searches_with_partial_corpus"] for row in route_metrics),
        "source_read_budget": 48, "successful_route_reads": sum(row["successful_source_reads"] for row in route_metrics),
        "distinct_route_attempts": sum(row["distinct_source_attempts"] for row in route_metrics),
        "navigation_events": sum(row["navigation_events"] for row in route_metrics),
        "adjacent_search_hits_exposed": sum(row["adjacent_search_hits_exposed"] for row in route_metrics),
        "adjacent_sources_read": sum(row["adjacent_sources_read"] for row in route_metrics),
        "route_metrics": route_metrics,
        "source_counts": {"ledger_rows": len(sources), "eligible_distinct_materials": len(counted),
                          "independent_work_event_groups": len({row["independent_work_event_group"] for row in counted}),
                          "lineages": len({row["lineage_id"] for row in counted}),
                          "new_r0": category["new_r0"], "pinned_manual_code": category["manual_code"],
                          "upstream_behavior": category["upstream_behavior"], "audio": audio, "ebook": ebook,
                          "counted_ids": [row["source_id"] for row in counted]},
        "calibration_cases": ["JN2", "PN1", "PE1"], "calibration_contribution_to_main_pairs": 0,
        "blank_second_constraint_cases": [row["case_id"] for row in frame if not row["C2"]],
        "public_outcomes": {"answers": len(first_answers), "accepted_questions_now": 5,
                            "answers_within_30_days": len(first_answers), "answers_after_30_days": 0,
                            "comments_within_30_days": len(comments), "comments_after_30_days": 0,
                            "asker_reported_fixed_cases": ["P3"], "asker_reported_auxiliary_failure_cases": ["J1"],
                            "exact_version_input_command_output_verified": 0,
                            "execution_success_rate": "산출 불가 (완비 실행 분모 0)"},
        "frozen_checks": frozen_checks,
    }
    (ROOT / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"audit": "PASS", "pairs": metrics["strict_pair_counts"],
                      "route_reads": metrics["successful_route_reads"], "source_counts": metrics["source_counts"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
