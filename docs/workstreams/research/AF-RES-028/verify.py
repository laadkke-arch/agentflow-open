#!/usr/bin/env python3
"""Check stage locks, source minimums, replay hashes and reported sample denominators."""
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path
import re

from run import load

HERE = Path(__file__).resolve().parent


def json_file(name):
    return json.loads((HERE / name).read_text())


def sha(name):
    return sha256((HERE / name).read_bytes()).hexdigest()


def main():
    scope = json_file("scope-lock.json")
    blind = json_file("observation-seal.json")
    repeat = json_file("receipts/clean-replay/seal.json")
    assert sha("packets.jsonl") == scope["packets_sha256"]
    assert len(scope["answer_sha256"]) == 64
    for part, files in (("executed", "receipts/first/"), ("blinded", ""), ("design", "")):
        for name, lock in blind[part].items():
            assert sha(files + name) == lock, (name, part)
    for name, lock in repeat["executed"].items():
        assert sha("receipts/clean-replay/" + name) == lock, name
    for name in ("canonical_judgment_sha256", "input_sha256"):
        assert blind[name] == repeat[name], name
    assert sha("receipts/first/observations.jsonl") == sha("receipts/clean-replay/observations.jsonl")

    cases = load(HERE / "observations.jsonl")
    contracts = load(HERE / "contracts.jsonl")
    packets = load(HERE / "packets.jsonl")
    ids = [f"A028-{i:02d}" for i in range(1, 43)]
    assert [r["cell_id"] for r in cases] == [r["cell_id"] for r in packets] == ids
    assert len(contracts) == 33 and sorted(cid for r in contracts for cid in r["cells"]) == ids
    assert all("expect_positive" in r and "expect_boundary" in r and r["t0_lines"] for r in contracts)
    assert all(r["direct_pair"] for r in cases)
    for phase in ("first", "clean-replay"):
        receipts = load(HERE / f"receipts/{phase}/raw.jsonl")
        assert len(receipts) == 75 and len(set(r["id"] for r in receipts)) == 75
        for row in receipts:
            assert row["grade"] == "direct" and row["rc"] == 0
            for stream in ("stdout", "stderr"):
                assert sha256(row[stream].encode()).hexdigest() == row[stream + "_sha256"], row["id"]
        assert "driver_rc=0" in (HERE / f"receipts/{phase}/time.txt").read_text()

    with (HERE / "artifacts.csv").open() as f:
        artifacts = list(csv.DictReader(f))
    versions = load(HERE / "receipts/first/versions.jsonl")
    assert len(artifacts) == len(versions) == 24 and all(r["valid"] for r in versions)
    binaries = {(a["ecosystem"], a["tag"]): a["binary_sha256"] for a in artifacts}
    assert binaries == {(r["ecosystem"], r["tag"]): r["sha256"] for r in versions}
    assert all(r["status"] == "ready" and r["tag_verified"] == "True" and len(r["sha256"]) == 64 for r in artifacts)
    assert Counter(r["ecosystem"] for r in artifacts) == {"python": 13, "node": 11}

    with (HERE / "comparison.csv").open() as f:
        comparison = list(csv.DictReader(f))
    tab = json_file("tabulations.json")
    assert [r["cell_id"] for r in comparison] == ids
    prior = Counter(r["prior_state"] for r in comparison)
    assert prior == {"supported": 32, "invalid": 8, "initial_error": 1, "unknown": 1}
    kept = [r for r in comparison if r["prior_state"] == "supported"]
    assert Counter(r["ecosystem"] for r in kept) == {"python": 16, "node": 16}
    assert all(r["runtime_state"] == "supported" for r in kept)
    assert tab["reveal"]["supported_untested"] == 865
    assert tab["reveal"]["primary_hidden_invalid"] == tab["reveal"]["primary_unconfirmed"] == 0
    assert tab["supported"]["policy"]["D"]["manual_read"] == 6
    assert tab["supported"]["policy"]["S"]["manual_read"] == 4
    assert tab["all"]["policy"]["D"]["paired_new"] == {"TP": 5, "FP": 1, "FN": 1, "TN": 32, "censored": 0}
    assert tab["all"]["policy"]["S"]["paired_new"] == {"TP": 3, "FP": 0, "FN": 3, "TN": 33, "censored": 0}

    source_list = json_file("sources.json")
    counted = [r for r in source_list if r["minimum_counted"]]
    assert len({r["id"] for r in source_list}) == len(source_list)
    assert len(counted) == len({r["lineage"] for r in counted}) == 71
    by_type = Counter(r["kind"] for r in counted)
    assert by_type["t0_manual"] >= 8 and by_type["official_implementation"] >= 8 and by_type["release"] >= 4
    assert by_type["metrology"] >= 2 and by_type["preservation"] >= 2
    for row in source_list:
        assert all(row[k] for k in ("url", "checked_utc", "location", "observed", "limits", "producer", "lineage", "count_reason"))
    draw_verification = json_file("evidence/verification.json")
    for name, record in draw_verification["repeat_comparison"].items():
        assert record["byte_equal"] and record["committed_sha256"] == record["replay_sha256"]
        if name != "raw_decision_observations":
            assert record["committed_sha256"] == sha(name), name

    report = (HERE / "RESULT.md").read_text()
    groups = re.findall(r"(?:^\|.*\n)+", report, flags=re.MULTILINE)
    assert len(groups) >= 5
    assert [group.splitlines()[0].split("|")[1].strip() for group in groups[:4]] == [
        "익명 셀 ID·생태계", "표집층·생태계", "정책·표본층", "Q 번호·주장·적용 범위"]
    assert groups[-1].startswith("| 중요한 불일치·약점") and len(groups[-1].splitlines()) == 5
    costs = json_file("costs-summary.json")
    assert costs["official_raw_file"]["ok_or_direct"] == 105
    assert costs["official_raw_file"]["measured_bytes"] == 3669760
    assert costs["probe_first"]["ok_or_direct"] == costs["probe_clean-replay"]["ok_or_direct"] == 75
    assert costs["probe_python-first"]["failed_or_unavailable"] == 8
    print(json.dumps({"cells": 42, "main": 32, "controls": 10, "direct_pairs": 42,
                      "source_count": len(counted), "source_strata": by_type, "version_count": 24,
                      "canonical_judgment_sha256": blind["canonical_judgment_sha256"],
                      "report_tables_and_last_three": True}, sort_keys=True))


if __name__ == "__main__":
    main()
