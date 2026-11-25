"""Check the saved corpus, receipt joins, report shape and fixed replay."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

root, fresh = (Path(x) for x in sys.argv[1:])
original = root / "receipts/original"
sha = lambda data: hashlib.sha256(data).hexdigest()


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def jsonl(path):
    return [json.loads(line) for line in path.read_bytes().splitlines()]


for row in (original / "SHA256SUMS").read_text().splitlines():
    digest, filename = row.split()
    assert sha((original / filename).read_bytes()) == digest

snapshots = csv_rows(root / "snapshots.csv")
source = jsonl(original / "trace-artifacts.jsonl")
cases = {r["case_id"]: r for r in csv_rows(original / "worked-traces.csv")}
assert len(snapshots) == len(source) == len({row["slot"] for row in snapshots}) == 12
assert Counter(r["code_group"] for r in snapshots) == {"G1": 3, "G2": 3, "G3": 2, "G4": 3, "G5": 1}
parents = {}
for view, raw in zip(snapshots, source):
    key, phase = raw["case_id"], raw["phase"]
    digest = sha(raw["source_utf8"].encode("utf-8"))
    assert (view["case_id"], view["phase"]) == (key, phase)
    assert digest == raw["sha256"] == view["actual_sha256"] == cases[key][phase + "_hash"]
    assert raw["parent_hash"] == parents.get(key)
    assert view["actor_id"] == raw["actor_id"] == cases[key]["participant_id"]
    parents[key] = digest

expected_cases = {"r1": 12, "r2": 12, "controls": 5, "fixed": 12}
assert len({json.loads((path / "summary.json").read_bytes())["work"]
            for path in [root / "receipts/r1", root / "receipts/r2", root / "receipts/controls", fresh]}) == 4
expected_binaries = set()
for name, count in expected_cases.items():
    path = fresh if name == "fixed" else root / "receipts" / name
    assert (path/"launcher.exit").read_text().strip() == "0"
    environment = json.loads((path/"environment.json").read_bytes())
    assert environment["sys_version_info"] == [3, 12, 0, "final", 0]
    assert environment["sys_implementation"] == "cpython"
    expected_binaries.add(environment["executable_sha256"])
    meta = list((path/"runs").glob("*/*/receipt.json"))
    assert len(meta) == 2 * count
    for m in meta:
        r = json.loads(m.read_bytes())
        assert r["initial_cwd_entries"] == [] and r["process_status"] == "exited"
        assert r["fixture_sha256"] == r["fixture_after_sha256"]
        assert r["python_executable_sha256"] == environment["executable_sha256"]
        for stream, filename in (("stdout", "stdout.jsonl"), ("stderr", "stderr.txt")):
            data = m.with_name(filename).read_bytes()
            assert len(data) == r[stream + "_bytes"] and sha(data) == r[stream + "_sha256"]
        assert [row["id"] for row in jsonl(m.with_name("stdout.jsonl"))] == r["vector_ids"]
        if r["engine"] == "grader":
            assert r["script_sha256"] == sha((original/"verify_vectors.py").read_bytes())
    if name in {"r2", "fixed"}:
        pairs = json.loads((path/"replay-comparison.json").read_bytes())
        assert len(pairs) == 24 and all(all(p["matching"].values()) for p in pairs)
assert len(expected_binaries) == 1

records = csv_rows(root/"vectors.csv")
assert len(records) == 90 and all(r["endpoint_agreement"] == "True" for r in records)
assert Counter(r["grader_state"] for r in records) == {"pass": 86, "wrong_value": 4}
assert {(r["slot"],r["vector_id"],r["got_repr"],r["expected_repr"]) for r in records
        if r["grader_state"] != "pass"} == {
    ("F-t24","B2","1","3"), ("F-t24","B3","0","3"), ("F-t24","B6","2","4"), ("F-t24","B7","1","3"),
}
for row in records:
    for column in ("r1_grader_stdout","r2_grader_stdout","r1_reference_stdout","r2_reference_stdout"):
        path, anchor = row[column].split("#L")
        raw = jsonl(root/path)[int(anchor)-1]
        assert (raw["id"], raw["got"], raw["expected"]) == (row["vector_id"], row["got_repr"], row["expected_repr"])

controls = csv_rows(root/"receipts/controls/vectors.csv")
assert len(controls) == 39 and all(r["endpoint_agreement"] == "True" for r in controls)
expected_fail = {
    "left_ties": {"B2","B3","B6","B7"}, "global_groups": {"A2","A4","A5"},
    "bool_indices": {"B0","B1","B4","B5"}, "restore_input": set(),
    "raise_on_tie_vector": {"B2"},
}
for slot, expected in expected_fail.items():
    matching = [r for r in controls if r["slot"] == slot]
    assert len(matching) == (7 if slot == "global_groups" else 8)
    assert {r["vector_id"] for r in matching if r["grader_pass"] == "False"} == expected
    if slot == "restore_input":
        assert all(r["reference_mid_changes"] == "2" and r["strict_pass_if_observed"] == "False"
                   and r["unchanged_at_return"] == "True" for r in matching)
    if slot == "bool_indices":
        assert all(r["reference_value_equal"] == "True" and r["grader_state"] == "type_error"
                   for r in matching if r["vector_id"] in expected)
exception = jsonl(root/"receipts/controls/runs/raise_on_tie_vector/grader/stdout.jsonl")[2]
assert exception["id"] == "B2" and "ValueError" in exception["exception"]
assert all(k not in exception for k in ("got","type_ok","unchanged"))

ledger = jsonl(root/"sources.jsonl")
keys = {"source_id","work_id","lineage_id","group","questions","cases","url","publisher","version",
        "publication_date","checked_utc","location","finding","unit","evidence_kind",
        "limitation","access","counted","count_reason"}
assert len(ledger) == len({r["source_id"] for r in ledger}) == 54
assert all(set(r) == keys and r["url"].startswith("https://") for r in ledger)
counted = [r for r in ledger if r["counted"]]
assert len({r["work_id"] for r in counted}) == len(counted) == 28
assert len({r["lineage_id"] for r in counted}) == 3
assert all(r["access"] == "success" for r in counted)
assert Counter(r["group"] for r in counted) == {"AF-RES-249": 8, "CPython": 8, "language": 5, "nbgrader": 7}
assert Counter(r["access"] for r in ledger) == {"success": 50, "failed": 4}

report = (root/"RESULT.md").read_text(encoding="utf-8")
tables = re.findall(r"(?:^\|[^\n]*\n)+", report, re.MULTILINE)
assert report.startswith("| 합성 사건·시점·코드 지문 |")
for table, fields, count in ((tables[0],6,90),(tables[1],5,8),(tables[-1],4,3)):
    lines = table.splitlines()
    assert len(lines) == count + 2 and all(line.count("|") == fields + 1 for line in lines)
    if table is tables[-1]:
        assert report.endswith(table)
assert re.findall(r"^## (Q[1-7])\b", report, re.MULTILINE) == [f"Q{i}" for i in range(1,8)]
self_check = (root/"SELF_CHECK.md").read_text(encoding="utf-8")
assert re.findall(r"^\| (Q[1-7]) \|", self_check, re.MULTILINE) == [f"Q{i}" for i in range(1,8)]
assert (fresh/"vectors.csv").read_bytes() == (root/"receipts/r2/vectors.csv").read_bytes()
assert (fresh/"snapshots.csv").read_bytes() == (root/"snapshots.csv").read_bytes()
print("PASS: 5 original files, 12 slots / 5 code groups, 41 grader + 41 reference receipts with stream hashes; 90 joined rows, 39 control rows, 28 counted sources, both opening tables and final three weaknesses, Q1–Q7, exact-version fixed replay")
