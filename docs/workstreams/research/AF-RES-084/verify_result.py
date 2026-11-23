"""Verify the Markdown tables and evidence counts against the research data."""

import csv
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def read_jsonl(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines()]


def read_csv(path):
    with (ROOT / path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def table_body(text, name):
    section = text.split(f"\n## {name}", 1)[1].split("\n## ", 1)[0]
    return [line for line in section.splitlines() if line.startswith("| ")][2:]


def main():
    report = (ROOT / "RESULT.md").read_text()
    sources = read_jsonl("sources.jsonl")
    attempts = read_jsonl("attempts.jsonl")
    versions = read_jsonl("versions.jsonl")
    events = read_jsonl("events.jsonl")
    runs = read_jsonl("runs.jsonl")
    cells = read_csv("cells.csv")
    metrics = json.loads((ROOT / "metrics.json").read_text())
    sources_by_id = {row["source_id"]: row for row in sources}
    assert len(sources_by_id) == len(sources)
    source_fields = {"source_id", "lineage_id", "kind", "url", "locator", "read_utc",
                     "q_cases", "observed", "limitations", "claim"}
    assert all(source_fields <= row.keys() and all(row[x] for x in source_fields) for row in sources)
    external = {row["lineage_id"] for row in sources if not row["lineage_id"].startswith("study:")}
    assert len(external) >= 20
    assert len({row["attempt_id"] for row in attempts}) == len(attempts)
    assert {row["case"] for row in versions} == {row["case"] for row in cells}
    assert all(row["non_opening_control"]["excluded_from_opening"] for row in events)

    for row in events:
        assert all(source_id in sources_by_id for source_id in row["source_ids"])
        if row["opened_status"] != "verified":
            assert all(row[field] is None for field in ("event_id", "opened_url", "raw_sha256", "lf_sha256"))
            for cell in cells:
                if row["case"] == cell["case"]:
                    assert cell["recalculated_opened"] == "unknown"
                    assert cell["listed_opened"] == "unknown"
                    assert cell["joint_opened"] == cell["refuted_opened"] == "unknown"
    assert metrics["denominators"]["suspect_opened_promotions"] == 0

    assert len({x["id"] for x in runs}) == len(runs)
    for row in runs:
        kind = row["record_source"]
        if kind == "new":
            assert row["actor"] == "AF-RES-084" and row["expectation_matches"]
        if kind == "inherited":
            assert row["actor"] == "AF-RES-080" and row["status"] == "ran-in-080"
        if kind == "planned":
            assert row["role"] == "exact" and row["observed"] is None and row["version"] is None
        if kind == "author":
            assert row["source_id"] in sources_by_id
        if row["role"] == "author-followup":
            assert row["observed"] is None and row["version"] is None and row["process_exit"] is None

    cases = [line.split()[1] for line in table_body(report, "표 1.")]
    assert cases == [row["case"] for row in versions]
    status_terms = {"absent-in-scope": "부재", "refuted": "반박", "positive": "양성", "unknown": "미확인"}
    table = table_body(report, "표 2.")
    assert len(table) == 16 == len(cells)
    for printed, row in zip(table, cells, strict=True):
        assert printed.startswith(f"| {row['case']} {row['cell']} |")
        a = status_terms[row["old_acquired"]]
        b = status_terms[row["recalculated_acquired"]]
        o = status_terms[row["recalculated_opened"]]
        assert f"확보 {a}→{b} · 개설 {o}" in printed, printed
    exec_table = table_body(report, "표 3.")
    assert len(exec_table) == 8
    assert [line.split()[1] for line in exec_table[::2]] == [row["case"] for row in versions]
    for line in exec_table:
        refs = re.findall(r"\(runs\.jsonl#L(\d+)\)", line)
        assert refs and all(runs[int(i) - 1]["case"] == line.split()[1] for i in refs)
    final = report.split("\n## 판단을 바꿀 세 가지", 1)[1]
    assert len(re.findall(r"(?m)^\d+\. ", final)) == 3
    print(f"3 tables checked; 16 cells; {len(sources)} source rows; {len(external)} external lineages")


if __name__ == "__main__":
    main()
