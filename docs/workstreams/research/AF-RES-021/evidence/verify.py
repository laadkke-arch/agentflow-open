#!/usr/bin/env python3
"""Check AF-RES-021 input separation, coverage, exact replay and report tables."""

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMATS = "APM"
BUDGETS = (1, 2, 4)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def sentence_payload(packet):
    return {k: v for k, v in packet.items() if k not in ("format", "positions", "links", "tokens")}


def checked_command(*args):
    return subprocess.run([sys.executable, "-I", *map(str, args)], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True,
                        help="output of replay.py index and build, storing no answer keys")
    parser.add_argument("--scratch", type=Path, required=True,
                        help="temporary output directory for independently generated logs and tables")
    args = parser.parse_args()
    stage, scratch = args.stage, args.scratch
    scratch.mkdir(parents=True, exist_ok=True)
    assert not (stage / "keys.jsonl").exists()
    case_rows = lines(ROOT / "cases.jsonl")
    assert len(case_rows) == len({x["id"] for x in case_rows}) == 12
    assert Counter(q["project"] for q in case_rows) == {"pytest": 4, "CMake": 4, "HTTPX": 4}
    assert Counter(q["scope"] for q in case_rows) == {"전체": 6, "부분": 6}
    assert all(len(q["candidates"]) >= 3 for q in case_rows)
    cases = {r["id"]: q["id"] for q in case_rows for r in q["candidates"]}
    packets = {(x["id"], x["format"]): x for x in lines(ROOT / "packets.jsonl")}
    runs_file = ROOT / "runs.jsonl"
    runs = {(x["row"], x["format"]): x for x in lines(runs_file)}
    expected = {(row, fmt) for row in cases for fmt in FORMATS}
    assert set(packets) == set(runs) == expected
    assert len(cases) == 45 and len(lines(runs_file)) == len(expected) == len(lines(ROOT / "packets.jsonl"))
    key_rows = lines(ROOT / "keys.jsonl")
    assert {x["row"] for x in key_rows} == set(cases) and len(key_rows) == len(cases)
    assert sum(x["natural_near"] for x in key_rows) == 14
    assert sum(x["official"]["verdict"] == "support" for x in key_rows) == 23

    index = {s["id"]: s for s in read(stage / "index.json")}
    allowed_verdicts = {"support", "conflict", "hold"}
    for row, qid in cases.items():
        a, p, m = (packets[row, fmt] for fmt in FORMATS)
        assert sentence_payload(a) == sentence_payload(p) == sentence_payload(m)
        assert p["positions"] == m["positions"] and a["positions"] == []
        assert not a["links"] and not p["links"] and all(x["to"] in p["positions"] for x in m["links"])
        assert all(x["tokens"] <= 256 and x["question"] == qid for x in (a, p, m))
        for fmt in FORMATS:
            log = runs[row, fmt]
            assert log["q"] == qid and log["reader"] == "python-rule"
            assert len(log["opened"]) <= 4 and set(log["at"]) == {"1", "2", "4"}
            opened = log["opened"]
            for position, event in enumerate(opened, 1):
                section = index[event["id"]]
                assert position == event["order"] and section["doc"] == packets[row, fmt]["source"]
                assert event["sha256"] == section["sha256"] and "error" not in event
            for b in BUDGETS:
                verdict = log["at"][str(b)]
                assert verdict["verdict"] in allowed_verdicts
                assert set(verdict["cited"]) <= {e["id"] for e in opened[:b]}

    for row in key_rows:
        for lens in ("official", "history"):
            ref = row[lens]
            assert ref["verdict"] in allowed_verdicts
            assert all(group and set(group) <= set(index) for group in ref["allowed"])
        for loc in row["official"]["checked_sources"]:
            s = index[loc["section"]]
            assert s["first"] <= loc["line"] <= s["last"] and loc["url"].startswith(s["url"] + "#L")

    with (ROOT / "metrics.csv").open(encoding="utf-8", newline="") as file:
        metrics = list(csv.DictReader(file))
    assert len(metrics) == 1560
    for r in metrics:
        if r["format"] not in FORMATS:
            continue
        a = {k: int(v) for k, v in r.items() if v.isdecimal()}
        assert a["rows"] == a["pred_hold"] + a["pred_support"] + a["pred_conflict"]
        assert a["rows"] == a["ref_hold"] + a["ref_positive"] + a["ref_conflict"]
        assert a["mapped"] == a["reached"] + a["unreached"]
        assert a["pos_recovered"] <= a["pos_reached"] <= a["ref_positive"]
        assert a["near_approved"] <= a["near"] and a["read_errors"] == 0

    sources = read(ROOT / "sources.json")
    counted = [x for x in sources if x["counted"]]
    assert len({s["id"] for s in sources}) == len(sources)
    assert len({s["url"] for s in counted}) == len(counted)
    assert Counter(s["category"] for s in counted) == {
        "original_public": 12, "supplier_versioned": 26, "other_field": 8
    }

    study_receipt = read(ROOT / "evidence/score-receipt.json")
    assert all(digest((ROOT / name).read_bytes()) == expected_hash
               for name, expected_hash in study_receipt["inputs_sha256"].items())
    assert digest((ROOT / "metrics.csv").read_bytes()) == study_receipt["metrics_sha256"]
    assert digest((stage / "index.json").read_bytes()) == study_receipt["cold_cache_verification"]["index_sha256"]
    assert (stage / "packets.jsonl").read_bytes() == (ROOT / "packets.jsonl").read_bytes()

    diagnostics = read(ROOT / "evidence/diagnostics.json")["controls"]
    replays = []
    for mode in ("main", "permuted", "no-links", "mislinked"):
        outfile = scratch / f"runs-{mode}.jsonl"
        checked_command(ROOT / "replay.py", "read", "--stage", stage, "--out", outfile,
                        "--receipt", scratch / f"read-{mode}.json", "--mode", mode)
        replays.append(outfile)
        if mode == "main":
            assert outfile.read_bytes() == runs_file.read_bytes()
        else:
            assert digest(outfile.read_bytes()) == diagnostics[mode]["run_sha256"]
    new_metrics = scratch / "metrics.csv"
    checked_command(ROOT / "replay.py", "score", "--runs", *replays, "--keys", ROOT / "keys.jsonl",
                    "--out", new_metrics)
    assert new_metrics.read_bytes() == (ROOT / "metrics.csv").read_bytes()

    checked_command(ROOT / "evidence/render-tables.py", "--check")
    end = (ROOT / "RESULT.md").read_text(encoding="utf-8").strip().split("## 중요한 불일치와 다음 조사")[-1]
    final_rows = [line for line in end.splitlines() if line.startswith("|")]
    assert len(final_rows) == 5 and end.rstrip().endswith("|")
    print(f"Verified {len(case_rows)} questions, {len(cases)} rows, {len(expected)} treatments, "
          f"{len(index)} sections, {len(metrics)} CSV rows and {len(counted)} counted sources.")
    print("All four run hashes and the score CSV match. Opening tables and three closing rows match.")


if __name__ == "__main__":
    main()
