"""Recount the committed source, trace and recommendation ledgers."""

import argparse
from collections import Counter, defaultdict
import csv
import io
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit

from analyze import ROOT, read, sha256, summarize

DECISION_LINKS = {
    "geometry만": ("OL05", "interaction/Translate.js#L45-L63"),
    "center만": ("OL06", "interaction/DragPan.js#L20-L33"),
    "둘 다": ("OL01", "Map.js#L1310-L1326"),
    "둘 다 유지": ("OL02", "MapBrowserEventHandler.js#L349-L421"),
}


def from_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def source_stats(sources):
    required = {
        "source_id", "work_id", "category", "type", "publisher", "url", "version_location",
        "checked_utc", "questions", "claim_ids", "evidence_kind", "finding",
        "limit_or_counter", "access", "countable",
    }
    assert len({r["source_id"] for r in sources}) == len(sources)
    counted = defaultdict(set)
    for row in sources:
        assert required <= row.keys(), row["source_id"]
        assert urlsplit(row["url"]).scheme == "https", row["source_id"]
        if row["access"] == "read" and row["countable"]:
            counted[row["category"]].add(row["work_id"])
        if row["access"] == "failed":
            assert not row["countable"] and row["fallback_url"], row["source_id"]
    all_works = set().union(*counted.values())
    assert len(all_works) == sum(map(len, counted.values()))
    minima = {"map-api-source": 7, "map-example-test": 5, "map-issue-pr": 4, "chart": 3, "audio": 3}
    assert all(len(counted[key]) >= value for key, value in minima.items())
    assert len(all_works) >= 22
    return {
        "ledger_rows": len(sources),
        "candidate_urls": len({r["url"] for r in sources}),
        "directly_read_urls": len({r["url"] for r in sources if r["access"] == "read"}),
        "failed_attempts": sum(r["access"] == "failed" for r in sources),
        "countable_distinct": len(all_works),
        "categories": {key: len(value) for key, value in sorted(counted.items())},
    }


def prediction_inputs():
    current_text = (ROOT / "predictions.csv").read_text(encoding="utf-8")
    predictions = list(csv.DictReader(io.StringIO(current_text)))
    b_sha = {row["B_lock"] for row in predictions}.pop()
    locked_b_fields = ("B_assumptions", "B_prediction", "B_conditional", "B_section")
    repository = Path(subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=ROOT, text=True,
    ).strip())
    csv_path = (ROOT / "predictions.csv").relative_to(repository).as_posix()

    def historical(commit):
        return subprocess.check_output(
            ["git", "show", f"{commit}:{csv_path}"], cwd=ROOT, text=True,
        )

    locked_b = {row["cell_id"]: row for row in csv.DictReader(io.StringIO(historical(b_sha)))}
    assert set(locked_b) == {row["cell_id"] for row in predictions}
    for row in predictions:
        assert row["B_lock"] == b_sha
        assert all(row[key] == locked_b[row["cell_id"]][key] for key in locked_b_fields)
    ac_sha = read(ROOT / "evidence/main/environment.json")["codeCommit"]
    assert historical(ac_sha) == current_text, "A/C ledger changed after first run"
    return {row["cell_id"]: row for row in predictions}, {"A": ac_sha, "B": b_sha, "C": ac_sha}


def predictions_and_returns(rows, predictions, locks, ol_url):
    pairs = defaultdict(list)
    for row in rows:
        if row["mode"] == "main":
            pairs[row["scenario"]["cell"]].append(row)
    assert set(pairs) == set(predictions)
    scores = {}
    outputs = []
    for cell, same_cell in pairs.items():
        assert sorted(row["scenario"]["repeat"] for row in same_cell) == [1, 2]
        outcomes = {item["outcome"] for item in same_cell if item["comparable"]}
        assert len(outcomes) == 1 and len(same_cell) == sum(row["comparable"] for row in same_cell), cell
        outcome = next(iter(outcomes))
        guesses = predictions[cell]
        scores[cell] = {method: guesses[method + "_prediction"] for method in ("A", "B", "C")} | {"observed": outcome}
        source_id, section = DECISION_LINKS[outcome]
        primary = ol_url + section
        b_section = ol_url + DECISION_LINKS["center만"][1] if guesses["B_prediction"] == "center만" else guesses["B_section"]
        for row in same_cell:
            feature_intent = row["scenario"]["position"] == "feature"
            actual_hit = row["dom_down"]["hits"]["atConfiguredTolerance"]
            matches_intent = outcome == ("geometry만" if feature_intent else "center만")
            if outcome == "둘 다":
                decision = "단독 기능 보류 · 전파 및 시퀀스 확인"
                action_url = ol_url + "interaction/Pointer.js#L125-L179"
                additional = "OL04;OL06"
                condition = "선택 피처를 받는 T를 먼저 호출하거나 두 조건을 분리하고 한 상태만 바뀌는지 대조"
            elif feature_intent and outcome == "center만":
                decision = "원인 채택 · 편집 목적에는 선택/필터 조합"
                action_url = ol_url + "interaction/Select.js#L291-L298"
                additional = "OL05;OL07;OI02"
                condition = "사전 선택 그룹이면 적격 목록. 첫 press 편집이면 판을 맞추고 features 없이 Translate filter"
            elif outcome == "geometry만":
                decision = "채택 · 적격 피처 이동"
                action_url = ol_url + "interaction/Translate.js#L235-L263"
                additional = "OL04;OL05"
                condition = "실제 hit가 목록에 있고 T가 down을 먼저 받아 P에는 넘기지 않음"
            else:
                decision = "채택 · 배경 pan"
                action_url = primary
                additional = "OL05;OL06"
                condition = "적격 피처 hit 없고 활성 P의 마우스 조건과 이동 문턱 충족"
            outputs.append({
                "id": row["id"], "cell_id": cell, "intended_operation": guesses["intent"],
                "A_prediction": guesses["A_prediction"], "A_section": guesses["A_section"], "A_lock": locks["A"],
                "B_prediction": guesses["B_prediction"], "B_section": b_section, "B_lock": locks["B"],
                "C_prediction": guesses["C_prediction"], "C_section": guesses["C_section"], "C_lock": locks["C"],
                "actual_down": "/".join(f'{hit["featureId"]}@{hit["layerId"]}' for hit in actual_hit) or "∅",
                "actual_down_handled": ">".join(row["down_accepted"]) or "∅",
                "outcome": outcome, "intent_matched": matches_intent,
                "geometry_delta_epsg3857": json.dumps(row["delta_geometry"]),
                "center_delta_epsg3857": json.dumps(row["delta_center"]),
                "feature_id_preserved": row["state_initial"]["featureId"] == row["state_final"]["featureId"],
                "post_primary_section": primary, "post_action_section": action_url,
                "source_ids": source_id + ";" + additional, "decision": decision, "use_if": condition,
                "raw_path": row["raw_path"], "raw_sha256": row["raw_sha256"],
            })
    scoring = {"cell_count": len(scores), "row_count": len(outputs), "tiers": {}, "cells": scores}
    for key in ("A", "B", "C"):
        scoring["tiers"][key] = {
            "correct": [c for c, s in scores.items() if s[key] == s["observed"]],
            "wrong": [c for c, s in scores.items() if s[key] not in ("보류", s["observed"])],
            "held": [c for c, s in scores.items() if s[key] == "보류"],
            "changed_priority_rows_after_observation": sum(row[key + "_section"] != row["post_primary_section"] for row in outputs),
        }
    for low, high in (("A", "B"), ("B", "C"), ("A", "C"), ("C", "B")):
        low_correct = set(scoring["tiers"][low]["correct"])
        high_correct = set(scoring["tiers"][high]["correct"])
        scoring[low + "_to_" + high] = {"new": sorted(high_correct - low_correct), "lost": sorted(low_correct - high_correct)}
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(outputs[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(outputs)
    return stream.getvalue(), scoring


def check_tables_and_links(sources, runs):
    source_ids = {row["source_id"] for row in sources}
    result_path = ROOT / "RESULT.md"
    result = result_path.read_text(encoding="utf-8")
    table_groups = re.findall(r"(?:^\|.*\|\n)+", result, re.MULTILINE)
    headers = (
        "목적·사건", "셀·반복", "증거 A·B·C", "불일치·약점",
    )
    for block, label in zip([*table_groups[:3], table_groups[-1]], headers, strict=True):
        assert block.startswith(f"| {label} |"), label
    counts = [len(block.splitlines()) - 2 for block in table_groups]
    assert counts[:3] == [3, 8, 3] and counts[-1] == 3
    assert result.endswith(table_groups[-1])
    raw_paths = {row["raw_path"] for row in runs if row["mode"] == "main"}
    assert all(f"({path})" in table_groups[1] for path in raw_paths)
    documents = [ROOT / "RESULT.md", ROOT / "SELF_CHECK.md", ROOT / "reproduce.md", ROOT / "SCOPE.md"]
    recorded_sources = {
        urlsplit(address)._replace(fragment="").geturl().rstrip("/")
        for row in sources
        for address in (row["url"], row.get("fallback_url"))
        if address
    }
    links = 0
    for doc in documents:
        for href in re.findall(r"\]\(([^\s)]+)\)", doc.read_text(encoding="utf-8")):
            target = urlsplit(href)
            if target.scheme:
                assert target.scheme == "https", href
                owned_repo = target.netloc == "github.com" and target.path.startswith("/laadkke-arch/agentflow-open/")
                assert owned_repo or target._replace(fragment="").geturl().rstrip("/") in recorded_sources, href
            elif target.path:
                assert (doc.parent / target.path).exists(), (doc.name, href)
            links += 1
    mentioned_ids = set(re.findall(r"\b(?:OI|OL|OE|OM|AU|VE|AX)\d\d[A-Z\d]*\b",
                                  result + (ROOT / "SELF_CHECK.md").read_text(encoding="utf-8")))
    assert mentioned_ids <= source_ids, mentioned_ids - source_ids
    return {"first_three_data_rows": counts[:3], "last_table_data_rows": counts[-1],
            "main_links": len(raw_paths), "source_ids_in_result_and_self_check": sorted(mentioned_ids),
            "document_links_checked": links}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-returns", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    plan = read(ROOT / "plan.json")
    assert plan["sealed"]
    evidence = ROOT / "evidence"
    modes = ("main", "controls", "supplement")
    runs = [summarize(plan, scenario, mode, evidence) for mode in modes for scenario in plan["cases"][mode]]
    assert runs == from_jsonl(ROOT / "runs.jsonl"), "committed trial ledger differs from raw replay"
    assert all(row["comparable"] for row in runs)
    for row in runs:
        for surface in row["surfaces"].values():
            assert sha256(evidence / surface["path"]) == surface["sha256"], row["id"]
    by_id = {r["id"]: r for r in runs}
    repeats = defaultdict(list)
    for row in runs:
        repeats[row["mode"], row["scenario"]["cell"]].append(row)
    for key, pair in repeats.items():
        assert len(pair) == 2
        assert all(pair[0][field] == pair[1][field] for field in (
            "state_initial", "state_final", "feature_pixel_final", "outcome", "surfaces",
        )), key
    for repeat in (1, 2):
        zero = by_id[f"C-edge-zero-r{repeat}"]
        six = by_id[f"C-edge-six-r{repeat}"]
        assert zero["dom_down"]["client"] == six["dom_down"]["client"]
        assert not zero["dom_down"]["hits"]["atConfiguredTolerance"]
        assert six["dom_down"]["hits"]["atConfiguredTolerance"] and zero["outcome"] != six["outcome"]
        paired = by_id[f"M-in-feature-translate-pan-r{repeat}"]
        no_observer = by_id[f"S-observers-off-simultaneous-r{repeat}"]
        assert all(no_observer[key] == paired[key] for key in ("state_final", "feature_pixel_final", "surfaces"))
        assert no_observer["comparison_scope"] == "settled-only" and no_observer["dom_down"] is None
        assert by_id[f"S-features-and-filter-deny-r{repeat}"]["filter_evaluations"] == []
        rejected = by_id[f"S-filter-alone-deny-r{repeat}"]["filter_evaluations"]
        allowed = by_id[f"S-filter-alone-accept-no-selection-r{repeat}"]["filter_evaluations"]
        assert rejected and not any(rejected)
        assert allowed and all(allowed)
    main_rows = [r for r in runs if r["mode"] == "main"]
    assert len({r["surfaces"]["initial"]["sha256"] for r in main_rows}) == 1
    assert {r["dom_down"]["target"] for r in main_rows} == {"CANVAS"}
    assert {len(r["dom_down"]["hits"]["atConfiguredTolerance"]) for r in main_rows} == {0, 1}
    probes = [read(ROOT / r["raw_path"])["initial"]["probes"] for r in main_rows]
    assert all(item == probes[0] for item in probes)

    sources = from_jsonl(ROOT / "sources.jsonl")
    positions = source_stats(sources)
    predictions, locks = prediction_inputs()
    pin = read(ROOT / "fixture/fingerprints.json")["source_commit"]
    ol_url = f"https://github.com/openlayers/openlayers/blob/{pin}/src/ol/"
    returns, scores = predictions_and_returns(runs, predictions, locks, ol_url)
    returns_path = ROOT / "returns.csv"
    if args.write_returns:
        returns_path.write_text(returns, encoding="utf-8")
    else:
        assert returns_path.read_text(encoding="utf-8") == returns
    summary = {
        "result_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "locks": locks,
        "sources": positions,
        "trials": {
            mode: {
                "planned": len(plan["cases"][mode]),
                "executed": sum(r["mode"] == mode and r["execution"] == "실행" for r in runs),
                "comparable": dict(Counter(r["comparison_scope"] for r in runs if r["mode"] == mode and r["comparable"])),
                "outcomes": dict(Counter(r["outcome"] for r in runs if r["mode"] == mode)),
                "records": sum(r["event_count"] for r in runs if r["mode"] == mode),
            }
            for mode in modes
        },
        "scores": scores,
        "matching_repeat_pairs": dict(Counter(mode for mode, _ in repeats)),
    }
    if not args.write_returns:
        summary["tables"] = check_tables_and_links(sources, runs)
    if args.report:
        args.report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
