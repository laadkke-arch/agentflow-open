"""Cross-check frame membership, planned-cell coverage, provenance and actual runs."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from score import CELLS, SEATS, index, read_jsonl, run_scoring_cases, verify_sources


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def check(root):
    match = read_csv(root / "matches.csv")
    frames = read_csv(root / "frames.csv")
    req = index(read_jsonl(root / "requests.jsonl"), "seat_id")
    gold = index(read_jsonl(root / "gold.jsonl"), "seat_id")
    assert sorted(req) == sorted(gold) == sorted(SEATS)
    assert len(match) == len(SEATS) * len(CELLS)
    assert {(x["seat_id"], x["cell"]) for x in match} == {(s, c) for s in SEATS for c in CELLS}
    assert all(row["acquired_status"] == "unknown" for row in match if not row["version"])
    assert all(row["status"] == "unknown" for row in match if row["recruitment"] != "selected")
    assert all(req[row["seat_id"]]["repo"] == row["repo"] for row in match)
    for layer, size in (("natural", 60), ("calibration", 100)):
        for upstream in ("pallets/click", "python-attrs/attrs"):
            observed = [row for row in frames if (row["stratum"],row["repo"]) == (layer,upstream)
                        and row["issue_number"]]
            assert [int(row["ordinal"]) for row in observed] == list(range(1, size + 1))
            times = [(row["created_utc"], int(row["issue_number"])) for row in observed]
            assert times == sorted(set(times)), (layer, upstream)
            assert all("2022-01-01" <= utc < "2025-01-01" for utc, _ in times)
            assert len({number for _, number in times}) == size
    with_issue = [row for row in req.values() if row.get("issue_number")]
    assert len({(x["repo"], x["issue_number"]) for x in with_issue}) == len(with_issue)
    for x in with_issue:
        assert re.fullmatch(r"[0-9a-f]{64}", x["original_sha256"])
        selected = [row for row in frames if row["slot"] == x["seat_id"]]
        assert len(selected) == 1
        frame = selected[0]
        assert (int(frame["issue_number"]), int(frame["ordinal"]), frame["body_sha256"]) == (
            x["issue_number"], x["ordinal"], x["original_sha256"])
    runplan = root / "fixtures/execution-plan.json"
    runfixture = root / "fixtures/probe.py"
    runs = index(read_jsonl(root / "runs.jsonl"), "id")
    first = index(read_jsonl(root / "evidence/runs-first-pass.jsonl"), "id")
    choices = ("CC01","CC02","AC01","AC02")
    assert set(runs) == set(first) == {f"{s}-{e}-{m}" for s in choices
                                     for e in ("reference", "exact") for m in ("positive", "boundary")}
    for row in runs.values():
        assert row["plan_sha256"] == digest(runplan) and row["fixture_sha256"] == digest(runfixture)
        if row["axis"] == "exact" and not row["version"]:
            assert row["status"] == "not-run" and row["returncode"] is None and row["actual"] is None
        if row["status"] == "ran":
            assert row["returncode"] == 0 and row["different_from_expectation"] == {}, row["id"]
    original_failure = first["AC02-reference-positive"]
    assert original_failure["returncode"] == 1 and "NameError" in original_failure["stderr"]
    counts = verify_sources(root / "sources.jsonl")
    assert counts["independent_originals"] >= 20
    assert counts["cross_domain_originals"] == 2
    return {"frames": len(frames), "planned_cells": len(match), "strict_joint": Counter(r["status"] for r in match),
            **counts, "scoring_cases": len(run_scoring_cases(root / "fixtures/scoring-cases.json")),
            "run_statuses": Counter(row["status"] for row in runs.values()), "first_probe_exit": 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
