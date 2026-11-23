"""Validate the reported units, references, table contract, and owned paths.

This checks deliverable consistency. It cannot certify missing original data,
study eligibility, or a causal effect; research acceptance remains partial.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import collections
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PREFIX = ROOT.relative_to(REPO).as_posix() + "/"


def read_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    required = ["manifest.json", "SCOPE.md", "sources.jsonl", "RESULT.md", "SELF_CHECK.md",
                "frame.csv", "endpoints.csv", "joins.csv", "bounds.csv", "reproduce.md",
                "evidence/acceptance-evidence.json"]
    assert all((ROOT / f).exists() for f in required)
    rows = [json.loads(s) for s in (ROOT / "sources.jsonl").read_text().splitlines()]
    fields = {"source_id", "work_id", "자료종류", "원본_URL", "최종_URL", "발행자", "확인_UTC",
              "판_또는_SHA", "쪽_절_행_셀", "관련_Q와_사례_ID", "확인한_내용", "확인범위와_한계",
              "지지_또는_반증", "직접열람_상태", "중복_계보"}
    assert all(fields <= set(r) for r in rows)
    ids = {r["source_id"] for r in rows}
    assert len(ids) == len(rows)
    stream_ids = [json.loads(line)["source_id"]
                  for file in (ROOT / "streams").glob("*/sources.jsonl")
                  for line in file.read_text().splitlines() if line.strip()]
    assert len(stream_ids) == len(set(stream_ids)) and set(stream_ids) == ids
    counted = {r["work_id"] for r in rows if r.get("count_toward_minimum")}
    counts = json.loads((ROOT / "evidence/source-counts.json").read_text())
    assert len(counted) == counts["unique_counted_primary_works"] and len(counted) >= 22
    assert len(rows) == counts["all_read_attempt_rows"] and len(rows) >= 151
    tables = {n: read_csv(n + ".csv") for n in ["frame", "endpoints", "joins", "bounds"]}
    slots = [r["slot"] for r in tables["frame"] if r["record_type"] == "required_slot"]
    assert set(slots) == {"B01", "B02", "S01", "S02", "S03", "S04", "E01", "D01"} and len(slots) == 8
    for n, key in [("endpoints", "endpoint_id"), ("joins", "join_id"), ("bounds", "bound_id")]:
        assert len({r[key] for r in tables[n]}) == len(tables[n])
        for r in tables[n]:
            assert set(json.loads(r["source_ids"])) <= ids
    endpoints = {r["endpoint_id"]: r for r in tables["endpoints"]}
    joins = {r["join_id"]: r for r in tables["joins"]}
    bounds = {r["bound_id"]: r for r in tables["bounds"]}
    assert endpoints["E01-final"]["deadline_seconds"] == "미확인"
    assert endpoints["S03-primary"]["deadline_seconds"] == "미확인"
    assert endpoints["S03-primary"]["nominal_or_approximate_duration_seconds"] == "2400"
    assert endpoints["E01-final"]["nominal_or_approximate_duration_seconds"] == "2100"
    assert "분석231행" in endpoints["E01-final"]["missing_or_withdrawal"]
    assert "approximately70min" in endpoints["S01-primary"]["training"]
    assert joins["S01-roster-artifacts"]["event_rows"] == "588"
    assert joins["S03-fragments"]["joined_rows"] == "122"
    assert joins["CD-J02"]["joined_rows"] == "112"
    assert bounds["B02-task3"]["unit"] == "rate difference"
    for arm, value in [("Newton", "6"), ("Control", "4")]:
        r = bounds[f"S01-{arm}-author-completion"]
        assert r["observed_joint_x"] == "미확인" and r["observed_secondary_count"] == value
    assert bounds["B02-eXoa"]["observed_joint_x"] == "3"
    assert bounds["B02-JavaDocs"]["observed_joint_x"] == "1"
    assert Fraction(bounds["B02-difference"]["lower"]) == Fraction(1, 6)
    assert all(r["target_join_performed"] == "false" for r in tables["joins"])

    result = (ROOT / "RESULT.md").read_text()
    acceptance = json.loads((ROOT / "evidence/acceptance-evidence.json").read_text())
    assert acceptance["counts"]["read_attempt_rows"] == len(rows)
    assert acceptance["counts"]["unique_primary_works"] == len(counted)
    for requirement in acceptance["requirements"]:
        for source in requirement.get("source_rows", []):
            assert rows[source["line"] - 1]["source_id"] == source["source_id"]
        for evidence in requirement.get("evidence", []):
            if evidence.get("file") == "RESULT.md" and evidence.get("heading"):
                assert result.splitlines()[evidence["line"] - 1] == evidence["heading"]
    headers = re.findall(r"^## .+$", result, flags=re.M)
    assert headers[0].startswith("## 표 1") and headers[1].startswith("## 표 2")
    first = result.split("## 표 2", 1)[0]
    first_rows = [l for l in first.splitlines() if l.startswith("|")]
    assert len(first_rows) == 10
    second = result.split("## 표 2", 1)[1].split("## 1. Q1", 1)[0]
    second_rows = [l for l in second.splitlines() if l.startswith("|")]
    assert all(len(l.split("|")) == 10 for l in first_rows + second_rows)
    assert all(f"Q{i}" in result for i in range(1, 8))
    assert "약한 조건부 외피" in result and "t≥11/10" in result
    assert "[+16⅔,+16⅔]%p" in result
    assert "부분 충족" in result
    final = result.split("## 가장 중요한 불일치·약점 3건", 1)[1]
    weakness_rows = [l for l in final.splitlines() if l.startswith("|")]
    assert len(weakness_rows) == 5 and result.rstrip().endswith(weakness_rows[-1])
    self_check = (ROOT / "SELF_CHECK.md").read_text()
    assert len(re.findall(r"^\| \*\*Q[1-7] ", self_check, flags=re.M)) == 7
    assert not re.search("[\u3040-\u30ff]", result + self_check)
    missing_links = []
    for file in ["RESULT.md", "SELF_CHECK.md", "reproduce.md"]:
        text = (ROOT / file).read_text()
        for destination in re.findall(r"\]\(([^)]+)\)", text):
            if "://" in destination or destination.startswith("#"):
                continue
            destination = destination.split("#", 1)[0]
            if not (ROOT / destination).is_file():
                missing_links.append([file, destination])
    assert not missing_links, missing_links
    changed = subprocess.check_output(["git", "diff", "--name-only", "573a8f1a7cafa90b87bcbb4267e73fee12385bda"], cwd=REPO, text=True).splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=REPO, text=True).splitlines()
    outside = [p for p in changed + untracked if not p.startswith(PREFIX)]
    assert not outside, outside
    calc = json.loads((ROOT / "evidence/calculation-check.json").read_text())
    assert calc["exact_frechet_cases_verified"] == 6200
    sensitivity = calc["B02_author_joint"]["partial_submission_same_clock_sensitivity"]
    assert sensitivity["treatment_lower_t_table"] == {"both": 3, "quality_only": 0, "time_only": 8, "neither": 1}
    assert sensitivity["control_lower_t_table"] == {"both": 1, "quality_only": 0, "time_only": 9, "neither": 2}
    out = {"checked_utc": datetime.now(timezone.utc).isoformat(), "status": "passed",
           "check_kind": "internal deliverable consistency and observed units; research acceptance remains partial",
           "source_rows": len(rows), "unique_primary_works": len(counted), "source_fields": len(fields),
           "csv_rows": {n: len(rs) for n, rs in tables.items()}, "first_required_table_study_rows": 8,
           "second_required_table_rows": len(second_rows)-2, "self_check_questions": 7,
           "last_weakness_rows": 3, "missing_local_links": missing_links, "outside_owned_paths": outside,
           "research_acceptance": "부분 충족", "future_remote_session_check": "not certified by this local check",
           "checked_file_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in required}}
    (ROOT / "evidence/deliverable-check.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "checked_file_sha256"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
