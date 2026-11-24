#!/usr/bin/env python3
"""Open the saved raw logs and recompute the scores and joins."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from prepare import INPUTS, hash_file
from run import build_comparisons, compact_json, decode_case, run_row


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_value(value):
    return "" if value is None else str(value)


def check_report_bytes(plan, suite):
    for manifest in plan["manifests"]:
        assert hash_file(suite / manifest["path"]) == manifest["sha256"], manifest["path"]
        entries = json.loads((suite / manifest["path"]).read_bytes())["sequence"]
        assert len(entries) == manifest["total_definitions"]
        for case in plan["cases"]:
            if case["algorithm"] != manifest["algorithm"]:
                continue
            entry = entries[case["manifest_ordinal"] - 1]
            assert entry["@id"] == "#" + case["short_id"]
            assert entry["@type"] == case["manifest_kind"]
            assert entry.get("option", {}) == case["manifest_options"]
            for fixture in (case["input"], case["context"], case["expected"].get("file")):
                if fixture:
                    assert hash_file(suite / fixture["path"]) == fixture["sha256"], fixture["path"]
            if case["expected"]["kind"] == "error":
                assert entry["expectErrorCode"] == case["expected"]["code"]
    for report in plan["earl_reports"]:
        path = suite / report["path"]
        assert hash_file(path) == report["sha256"], report["path"]
        lines = path.read_text(encoding="utf-8").splitlines()
        for row in plan["historical"]:
            if row["engine"] == report["engine"]:
                first, last = row["lines"]
                block = "\n".join(lines[first - 1:last])
                for field in ("subject", "test_iri", "assertor", "mode", "assertion_date_lexical", "outcome_iri"):
                    assert row[field] in block, (report["path"], first, field)


def audit(out, plan):
    expected_keys = {(engine, case["event_id"], rep)
                     for engine in plan["run_contract"]["engines"] for case in plan["cases"]
                     for rep in range(1, plan["run_contract"]["repetitions"] + 1)}
    cases = {case["event_id"]: case for case in plan["cases"]}
    rows = read_csv(out / "runs.csv")
    records = {}
    raw_count = 0
    active_pids = set()
    nonces = set()
    strict_positive = Counter()
    loads = Counter()
    for row in rows:
        key = (row["engine"], row["event_id"], int(row["repetition"]))
        assert key in expected_keys and key not in records, key
        receipt = json.loads((out / row["receipt"]).read_bytes())
        assert receipt["run_id"] == row["run_id"]
        case = cases[row["event_id"]]
        assert receipt["test_iri"] == case["test_iri"]
        assert receipt["engine"] == key[0] and receipt["event_id"] == key[1] and receipt["repetition"] == key[2]
        assert receipt["options"] == case["options"]
        assert (receipt["input"], receipt["context"], receipt["expected"]) == (case["input"], case["context"], case["expected"])
        records[key] = receipt
        assert receipt["nonce"] not in nonces, key
        nonces.add(receipt["nonce"])
        folder = (out / row["receipt"]).parent
        for name, expected in receipt["files"].items():
            path = folder / name
            assert path.stat().st_size == expected["bytes"] and hash_file(path) == expected["sha256"], path
            path.read_bytes()
        if not receipt["spawned"]:
            assert receipt["verdict"] == "not_run" and receipt["not_run_reason"], key
            continue
        assert receipt["engine_commit"] == plan["upstream"][key[0]]["commit"]
        assert receipt["process_id"] and receipt["started_utc"] <= receipt["ended_utc"]
        active_pids.add(receipt["process_id"])
        request = json.loads((folder / "request.json").read_bytes())
        assert request["nonce"] == receipt["nonce"]
        assert request["algorithm"] == case["algorithm"]
        assert request["base"] == case["options"]["base"]
        assert request["processing_mode"] == case["options"]["processingMode"]
        assert request["reexpand"] == (case["algorithm"] == "compact" and case["expected"]["kind"] == "json")
        assert (request["input"], request["context"]) == (case["input"], case["context"])
        if case["expected"]["kind"] == "json":
            assert request["expected"] == case["expected"]["value"]
        status = receipt["verdict"]
        if status not in ("pass", "fail"):
            assert status == "incomparable", key
            continue
        assert receipt["exit_code"] == 0
        raw = json.loads((folder / "stdout.log").read_bytes())
        assert raw == receipt["observation"]
        runtime = receipt["runtime"].split()[2] if key[0] == "gold" else receipt["runtime"]
        assert decode_case(raw, case, request, receipt["process_id"], runtime) == (status, receipt["rule"])
        raw_count += 1
        loads.update(item["mechanism"] for item in raw["loads"])
        if case["expected"]["kind"] == "json":
            actual = raw["actual"]
            # A stricter cross-check that preserves every array's order. None of the sampled
            # positive fixtures has a language-case difference, a list alias, or number precision stress.
            strict_positive["match" if actual.get("value") == case["expected"]["value"] else "different"] += 1
    assert records.keys() == expected_keys
    joined = build_comparisons(plan, records)
    assert [{key: csv_value(value) for key, value in row.items()} for row in joined] == read_csv(out / "comparison.csv")
    repeat = {row["left_id"]: row["comparison"] for row in joined if row["layer"] == "within_engine_repetition"}
    for row in rows:
        key = (row["engine"], row["event_id"], int(row["repetition"]))
        left_id = records[key]["run_id"].replace("-r2", "-r1")
        assert row == {name: csv_value(value) for name, value in run_row(records[key], repeat[left_id]).items()}
    by_layer = {}
    for row in joined:
        by_layer.setdefault(row["layer"], Counter()).update([row["comparison"]])
    started = [row["started_utc"] for row in rows if row["pid"]]
    ended = [row["ended_utc"] for row in rows if row["pid"]]
    return {
        "planned": len(expected_keys),
        "spawned": sum(row["spawned"] for row in records.values()),
        "distinct_process_ids": len(active_pids),
        "unique_nonces": len(nonces),
        "raw_and_grade_rechecked": raw_count,
        "all_log_hashes_rechecked": True,
        "utc_first": min(started, default=None),
        "utc_last": max(ended, default=None),
        "observed_read_roles": dict(loads),
        "strict_positive_crosscheck": dict(strict_positive),
        "by_engine": {engine: dict(Counter(row["verdict"] for row in records.values() if row["engine"] == engine))
                      for engine in plan["run_contract"]["engines"]},
        "by_comparison_layer": {layer: dict(count) for layer, count in by_layer.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="directory of runs.csv, comparison.csv and receipts")
    parser.add_argument("--suite", type=Path, help="optional pinned checkout for original-file recheck")
    args = parser.parse_args()
    plan = json.loads(INPUTS.read_bytes())
    if args.suite:
        check_report_bytes(plan, args.suite)
    summary = audit(args.out, plan)
    print(compact_json(summary))
    return 0 if summary["raw_and_grade_rechecked"] == summary["planned"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
