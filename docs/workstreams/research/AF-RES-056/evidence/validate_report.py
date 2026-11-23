"""Validate AF-RES-056 report/ledger joins without network or file mutation.

Run from any directory. This is publication validation, not a software
conformance suite or a substitute for the required workbench session check.
"""
from pathlib import Path
from collections import Counter
import csv
import datetime
import hashlib
import json
import re
import subprocess
import sys

P = Path(__file__).resolve().parents[1]
REPO = P.parents[3]
PREFIX = "docs/workstreams/research/AF-RES-056/"
STAGE1 = "1f63f0129207904a91ae9e01bb3e48c86415a644"
STAGE2 = "b765a189aa2a1f5982a4994fc0476273abbf7127"
BASE = "573a8f1a7cafa90b87bcbb4267e73fee12385bda"
checks = []


def check(name, condition, detail=None):
    checks.append({"check": name, "passed": bool(condition), "detail": detail})


def read_json(path):
    return json.loads((P / path).read_text())


def read_csv(path):
    with (P / path).open(newline="") as f:
        return list(csv.DictReader(f))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


frame = read_csv("frame.csv")
matches = read_csv("matches.csv")
slots = read_csv("slots.csv")
windows = read_csv("windows.csv")
judgments = read_csv("judgments.csv")
catalog = read_csv("catalog.csv")
vocabulary = read_csv("vocabulary.csv")
sources = [json.loads(s) for s in (P / "sources.jsonl").read_text().splitlines()]
counts = read_json("evidence/source-counts.json")
acceptance = read_json("evidence/acceptance-evidence.json")
cases = [f"{domain}-{n}" for domain in ["JS", "LD"] for n in range(1, 5)]
comparison_ids = [f"{case}-{method}" for case in cases for method in ["L", "V"]]

check("frame_80", len(frame) == 80)
check("selected_8_unique_cases", sorted(r["case_id"] for r in frame if r["case_id"]) == sorted(cases))
for domain, rows in [(d, [r for r in frame if r["domain"] == d]) for d in {r["domain"] for r in frame}]:
    check("frame_first40_" + domain, len(rows) == 40 and [int(r["screen_rank"]) for r in rows] == list(range(1, 41)))
    check("frame_creation_id_order_" + domain, rows == sorted(rows, key=lambda r: (r["created_utc"], int(r["question_id"]))))
check("earliest_revision_one_80", all(r["revision"] == "1" for r in frame))
check("catalog_rows_62", len(catalog) == 62)
check("vocabulary_20_literal_7_allowed_10_withheld", Counter(r["method"] for r in vocabulary) == {"L,V": 20, "V": 7, "withhold": 10})
check("comparisons_complete_order", [r["comparison_id"] for r in matches] == comparison_ids)
check("slot_states", len(slots) == 48 and Counter(r["status"] for r in slots) == {"observed_no_match": 45, "matched_pool_exhausted": 2, "filled": 1})
nonempty = [r for r in matches if int(r["total_matches"])]
check("only_JS4V_SC032", len(nonempty) == 1 and nonempty[0]["comparison_id"] == "JS-4-V" and json.loads(nonempty[0]["top3_ids_json"]) == ["SC-032"] and json.loads(nonempty[0]["top3_original_ranks_json"]) == [32])

report_lines = (P / "RESULT.md").read_text().splitlines()
first_blocks = []
current = []
for line in report_lines:
    if line.startswith("|"):
        current.append(line)
    elif current:
        first_blocks.append(current)
        current = []
        if len(first_blocks) == 2:
            break
check("report_starts_table1", report_lines[0].startswith("| 요구 ID·원문 주소 |"))
check("first_two_tables_16_8", len(first_blocks) == 2 and [len(b) - 2 for b in first_blocks] == [16, 8])
for row, ledger in zip(first_blocks[0][2:], matches):
    cells = [v.strip() for v in row.strip("|").split("|")]
    check("table1_join_" + ledger["comparison_id"], len(cells) == 7 and ("[" + ledger["case_id"] + "]") in cells[0] and cells[2].startswith(ledger["method"] + " ·") and cells[4].startswith(ledger["total_matches"] + " ·"))
    if ledger["total_matches"] == "1":
        check("table1_SC032_unknown_not_complete", "SC-032(원32)" in cells[4] and "모두 미확인" in cells[5] and "미확인 후보1" in cells[6])
check("table2_case_order", [r.split("|")[1].strip() for r in first_blocks[1][2:]] == cases)
check("cards_8", re.findall(r"^## ((?:JS|LD)-\d)$", (P / "cards.md").read_text(), re.M) == cases)
check("Q1_to_Q7_sections", all(any(line.startswith(f"## {n}. Q{n}") for line in report_lines) for n in range(1, 8)))
check("no_known_stale_report_wording", not any(x in "\n".join(report_lines) for x in ["§see evidence/", "Python4.26", "JS9.0.0 실행판"]))
check("final_three_weakness_rows", report_lines[-1].startswith("| 본표 구현") and len([x for x in report_lines[report_lines.index("## 10. 가장 중요한 불일치·약점 3건") + 1:] if x.startswith("|")]) == 5)

actions = [r for r in windows if r["trial_id"]]
trials = Counter(r["trial_id"] for r in actions)
check("window_rows_and_paths", len(windows) == 52 and trials == {"JS-4-V-P1": 1, "JS-4-V-P2": 2, "JS-4-V-P3": 2})
check("no_cross_trial_conjunction", all(r["C1"] == "미확인" and r["C2"] == "미확인" for r in actions))
main = [r for r in judgments if r["trial_id"] in trials]
check("main_three_unknown", len(main) == 3 and all(r["classification"] == "미확인" for r in main))
check("judgment_rows_19", len(judgments) == 19)
source_ids = {r["source_id"] for r in sources}
check("window_source_ids_resolve", all(r["source_id"] in source_ids for r in actions))

required = ["source_id", "work_id", "자료종류", "원본_URL", "최종_URL", "발행자", "확인_UTC", "판_또는_SHA", "쪽_절_행_셀", "관련_Q와_사례_ID", "확인한_내용", "확인범위와_한계", "지지_또는_반증", "직접열람_상태", "중복_계보"]
check("source_rows_and_unique_ids", len(sources) == len(source_ids) == 269)
check("source_15_required_fields", all(all(k in r for k in required) for r in sources))
check("source_row_classes", dict(Counter(r["counting_class"] for r in sources)) == counts["row_classes"])
primary = {r["work_id"] for r in sources if r["counting_class"] == "direct_primary"}
check("unique_primary_109", len(primary) == counts["unique_direct_primary_works"] == 109)
allocations = [w for a in counts["allocations"].values() for w in a["works"]]
check("24_distinct_allocated_works", len(allocations) == len({w["work_id"] for w in allocations}) == 24)
check("allocation_source_line_identity", all(sources[w["sources_line"] - 1]["source_id"] == w["source_id"] for w in allocations))

check("acceptance_partial_not_full", acceptance["overall"]["status"] == "partial_handoff" and acceptance["overall"]["full_acceptance"] is False)
check("no_imputed_precision_or_false_positive_rate", acceptance["outcomes"]["precision"] is None and acceptance["outcomes"]["false_positive_rate"] is None)
for criterion in acceptance["criteria"]:
    check("criterion_fields_" + criterion["criterion_id"], all(k in criterion for k in ["status", "numerator", "denominator", "unit", "evidence", "gap_reason"]))
    for index, ref in enumerate(criterion["evidence"]):
        file = P / ref["file"]
        n = len(file.read_text().splitlines()) if file.is_file() else 0
        check(f"evidence_location_{criterion['criterion_id']}_{index}", 1 <= ref["line_start"] <= ref["line_end"] <= n, ref)

for filename in ["frame.csv", "requirements.json", "vocabulary.csv"]:
    a = git("show", STAGE1 + ":" + PREFIX + filename)
    b = git("show", STAGE2 + ":" + PREFIX + filename)
    current = (P / filename).read_bytes().replace(b"\r\n", b"\n")
    check("frozen_before_rank_" + filename, a == b == current)
for filename in ["catalog.csv", "matches.csv", "slots.csv", "evidence/path-plan.json"]:
    fixed = git("show", STAGE2 + ":" + PREFIX + filename)
    check("frozen_before_destination_" + filename, fixed == (P / filename).read_bytes().replace(b"\r\n", b"\n"))
changed = git("diff", "--name-only", BASE, "HEAD").decode().splitlines()
check("committed_ownership_only", all(x.startswith(PREFIX) for x in changed))
check("source_audit_exit0", read_json("evidence/review/source-audit-receipt.json")["exit_code"] == 0)
check("PyLD_unexpected_failure_preserved", read_json("evidence/ld-suppliers/execution-attempts/offline-frame-attempt.json")["exit_code"] == 1)

failed = [r for r in checks if not r["passed"]]
result = {
    "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "checker": "root report/ledger publication validation; not independent execution or product conformance",
    "git_head": git("rev-parse", "HEAD").decode().strip(),
    "input_sha256": {f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in ["RESULT.md", "cards.md", "SELF_CHECK.md", "evidence/acceptance-evidence.json", "sources.jsonl", "windows.csv", "judgments.csv"]},
    "checks": checks,
    "check_count": len(checks),
    "failed_count": len(failed),
    "status": "passed" if not failed else "failed",
    "exit_code": 1 if failed else 0,
}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(result["exit_code"])
