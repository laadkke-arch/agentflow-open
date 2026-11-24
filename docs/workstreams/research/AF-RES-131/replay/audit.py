"""Recount release, source, experiment, and report rows at the saved commit."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from summarize import ROOT, json_file, summarize

MINIMUM = {"implementation-api": 6, "test-example": 4, "change-report": 4,
           "release-environment": 4, "qgis": 3, "audacity": 3}


def json_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def distinct(rows, key):
    values = {row[key] for row in rows}
    assert len(values) == len(rows), f"duplicate {key}"
    return values


def markdown_tables(path):
    sections = []
    block = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| "):
            block.append(line)
        elif block:
            sections.append(block)
            block = []
    if block:
        sections.append(block)
    return sections


def verify_ending(path):
    grid = markdown_tables(path)[-1]
    assert grid[0] == "| 중요한 불일치·약점 | 다음에 열 자료 또는 수행할 검사 | 판단을 바꿀 관측 |"
    assert len(grid) == 5
    assert all(len(line.split("|")) == 5 for line in grid)
    assert path.read_text(encoding="utf-8").strip().endswith(grid[-1])


def sources_audit():
    rows = json_lines(ROOT / "sources.jsonl")
    distinct(rows, "source_id")
    distinct(rows, "url")
    groups = defaultdict(set)
    access = Counter(row["access"] for row in rows)
    for row in rows:
        assert row["url"].startswith(("https://", "http://"))
        assert datetime.fromisoformat(row["checked_utc"]).utcoffset() is not None
        assert all(row[key] for key in ("source_id", "work_id", "kind", "publisher",
                                       "version_commit_section", "questions", "claim_ids", "observed", "limits"))
        assert row["eligible"] == (row["access"] == "read")
        if row["eligible"]:
            groups[row["kind"]].add(row["work_id"])
    by_kind = {kind: len(ids) for kind, ids in groups.items()}
    assert all(by_kind[kind] >= count for kind, count in MINIMUM.items()), by_kind
    unique = set.union(*groups.values())
    assert len(unique) == sum(by_kind.values())
    return {"candidates": len(rows), "access": dict(access), "eligible_by_kind": by_kind,
            "unique_qualifying_primary_works": len(unique)}


def releases_audit():
    rows = csv_rows(ROOT / "releases.csv")
    prereleases = csv_rows(ROOT / "evidence" / "prereleases.csv")
    distinct(rows, "version")
    distinct(prereleases, "version")
    expected = json_file(ROOT / "evidence" / "roster.json")
    assert len(rows) == expected["stable"]
    assert len(prereleases) == expected["prerelease_core_in_range"]
    assert [int(row["semver_rank"]) for row in rows] == list(range(1, len(rows) + 1))
    versions = [tuple(map(int, row["version"].split("."))) for row in rows]
    assert versions == sorted(versions) and (versions[0], versions[-1]) == ((6, 0, 0), (10, 11, 0))
    by_publish = sorted(rows, key=lambda row: datetime.fromisoformat(row["publish_utc"]))
    assert [int(row["publish_rank"]) for row in by_publish] == list(range(1, len(rows) + 1))
    assert all(row["tarball_status"] == "verified" and row["source_rules_match"] == "yes" for row in rows)
    fields = ("filter_with_features", "layers_with_features")
    counts = {field: dict(Counter(row[field] for row in rows)) for field in fields}
    expected_edge = [("6.6.1", "6.7.0")]
    for field in fields:
        for ordered in (rows, by_publish):
            edges = [(left["version"], right["version"]) for left, right in zip(ordered, ordered[1:])
                     if left[field] != right[field]]
            assert edges == expected_edge, (field, edges)
    groups = {row["translate_sha256"] for row in rows}
    assert groups == set(json_file(ROOT / "evidence" / "release-rules.json")["distribution_groups"])
    return {"stable": len(rows), "prerelease": len(prereleases), "artifact_groups": len(groups),
            "counts_per_option": counts, "edge": expected_edge,
            "publish_position_differs": [row["version"] for row in rows
                                         if row["semver_rank"] != row["publish_rank"]]}


def runs_audit():
    plan = json_file(ROOT / "fixture" / "input.json")
    cases = json_file(ROOT / "fixture" / "cases.json")
    forecasts = {row["run_id"]: row for row in csv_rows(ROOT / "predictions.csv")}
    rows = json_lines(ROOT / "runs.jsonl")
    ids = distinct(rows, "id")
    assert ids == distinct(cases, "id") == set(forecasts)
    counted = Counter(row["mode"] for row in rows)
    assert counted == Counter(main=48, controls=16, supplement=12, bare=8)
    assert len(list((ROOT / "evidence" / "browser").glob("*/*.json"))) == len(rows)
    raw_by_id = {row["id"]: row for row in rows}
    for case in cases:
        row = raw_by_id[case["id"]]
        assert summarize(case, forecasts[row["id"]], plan, ROOT / row["raw_log"], row["raw_log"]) == row
        assert row["attempt"] == "observed" and row["comparable"] and row["prediction_matches"], row["id"]
        if row["mode"] == "bare":
            comparable = raw_by_id[row["id"].replace("bare-", "main-", 1)]
            assert row["callback_counts"] is None and row["settled"] == comparable["settled"]
        if row["mode"] == "main":
            assert row["raw_down_hit"] == [{"featureId": "parcel-01", "layerId": "owned"}]
            assert row["pointerdrag_count"] == 4
    return rows, {"counts": dict(counted), "categories": dict(Counter(row["category"] for row in rows)),
                  "full_comparisons": sum(row["comparison_scope"] == "full" for row in rows),
                  "settled_comparisons": counted["bare"], "predictions_matching": len(rows)}


def reports_audit(runs):
    tables = markdown_tables(ROOT / "RESULT.md")
    assert [len(table) - 2 for table in tables] == [2, 24, 9, 3]
    verify_ending(ROOT / "RESULT.md")
    q_table, = markdown_tables(ROOT / "SELF_CHECK.md")
    assert [line.split("|")[1].strip() for line in q_table[2:]] == [f"Q{i}" for i in range(1, 8)]
    by_id = {row["id"]: row for row in runs}
    for row in runs:
        if row["mode"] == "main":
            assert sum(row["raw_log"] in text for text in tables[1]) == 1, row["id"]
    returns = csv_rows(ROOT / "returns.csv")
    distinct(returns, "case_id")
    for row in returns:
        ids = row["supporting_run_ids"].split()
        assert len(set(ids)) == int(row["supporting_reused_run_count"])
        assert all(by_id[run_id]["comparable"] for run_id in ids)
        assert row["actual_user_adoption"] == "미확인"
        assert any(f"| {row['case_id']} ·" in text and row["primary_section_url"] in text for text in tables[2])
    return {"result_table_body_counts": [len(table) - 2 for table in tables], "self_check_questions": 7,
            "return_strategies": len(returns), "user_adoptions_observed": 0}


def cross_domain_audit():
    root = ROOT / "evidence" / "cross-domain"
    qgis = json_lines(root / "qgis.stdout.log")
    audio = json_lines(root / "audacity.stdout.log")
    assert (root / "qgis.exit").read_text().strip() == (root / "audacity.exit").read_text().strip() == "0"
    assert len(qgis) == 4 and len(audio) == 3
    for row in audio:
        for field in ("before_image", "after_image"):
            image = row[field]
            assert hashlib.sha256((root / "audacity" / image["file"]).read_bytes()).hexdigest() == image["sha256"]
    return {"qgis": len(qgis), "audacity": len(audio),
            "audacity_pngs_verified": sum(2 for _ in audio)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    runs, metrics = runs_audit()
    report = {"sources": sources_audit(), "releases": releases_audit(), "runs": metrics,
              "reports": reports_audit(runs), "cross_domain": cross_domain_audit(),
              "review_type": "same-worker self-check"}
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
