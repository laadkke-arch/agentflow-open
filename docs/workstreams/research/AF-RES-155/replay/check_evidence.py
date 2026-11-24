#!/usr/bin/env python3
"""Verify the sealed inputs, recorded outputs and repeatability of this bundle."""

import argparse
import base64
import csv
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from run import WORK, fingerprint, open_fixture, read_inputs


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def sha(data):
    return fingerprint(data)["sha256"]


def exact_bytes(blob):
    if "utf8" in blob:
        return blob["utf8"].encode("utf-8")
    return base64.b64decode(blob["base64"], validate=True)


def check_region(body, region, expected=None):
    start, finish = region["utf8_0_based_half_open"]
    raw = body[start:finish]
    first, last = region["codepoints_0_based_half_open"]
    assert body.decode("utf-8")[first:last].encode("utf-8") == raw
    assert len(raw) == region["bytes"] and sha(raw) == region["sha256"]
    if expected is not None:
        assert raw == expected.encode("utf-8")


def snapshot_bodies():
    snapshots = read_jsonl(WORK / "evidence/issue-snapshots.jsonl")
    bodies = {}
    for item in snapshots:
        path = item["body_ref"]
        if item["body_ref_row"]:
            upstream = subprocess.check_output(["git", "-C", WORK, "show", path])
            by_eid = {json.loads(line)["eid"]: json.loads(line)["body"] for line in upstream.splitlines()}
            data = by_eid[item["body_ref_row"]].encode("utf-8")
        else:
            data = (WORK / path).read_bytes()
        assert len(data) == item["utf8_bytes"] and sha(data) == item["body_sha256"]
        assert data.count(b"\r\n") == item["crlf_count"]
        bodies[item["id"]] = data
    return bodies


def validate_packets(snapshots):
    inputs = read_inputs()
    for key, item in inputs.items():
        open_fixture(inputs, key)
        if "source_region" in item:
            check_region(snapshots[item["case"]], item["source_region"])
        for key in ("presented_actual", "presented_expected"):
            if key in item:
                check_region(snapshots[item["case"]], item[key]["region"])
    packets = read_jsonl(WORK / "packets.jsonl")
    assert len(packets) == len({row["packet_id"] for row in packets}) == 12
    for row in packets:
        source = snapshots[row["case"]]
        payload = row["payload"]
        assert sha(source) == row["source_body_sha256"]
        check_region(source, row["selection_region"], payload["selected_raw"] if payload else None)
        if payload is None:
            assert row["missing_reason"] and row["payload_sha256"] is None
            continue
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        assert len(encoded) == row["payload_utf8_bytes"] and sha(encoded) == row["payload_sha256"]
        if row["extra_region"] is not None:
            check_region(source, row["extra_region"], payload["extra_raw"])
            check_region(source, row["original_extra_region"])
            assert len(payload["extra_raw"]) == row["extra_chars"]
            assert len(payload["extra_raw"].encode("utf-8")) == row["extra_utf8_bytes"]
            assert row["original_extra_region"]["chars"] - row["extra_chars"] == row["cut_codepoints_from_end"]
    preds = read_csv(WORK / "predictions.csv")
    assert len(preds) == 12 and {x["packet_id"] for x in preds} == {x["packet_id"] for x in packets}
    return packets


def stable_results(row):
    return (row["status"], row["summary"],
            [(s["stage"], s["exit_code"], s["stdin"], s["stdout"], s["stderr"]) for s in row["stages"]])


def validate_runs(fresh):
    rows = read_jsonl(WORK / "runs.jsonl")
    groups = defaultdict(list)
    counted = Counter()
    for row in rows:
        groups[row["path_id"]].append(row)
        assert row["checkout_clean_at_start"] is True
        counted["paths"] += 1
        counted[row["status"]] += 1
        for stage in row["stages"]:
            counted["stages"] += 1
            counted[f"stage_exit_{stage['exit_code']}"] += 1
            for name in ("stdout", "stderr"):
                blob = stage[name]
                assert fingerprint(exact_bytes(blob)) == {k: blob[k] for k in ("bytes","sha256")}
    assert len(groups) == 20 and all(len(g) == 2 for g in groups.values())
    for group in groups.values():
        first, second = group
        assert first["checkout_root"] != second["checkout_root"] and first["repeat"] != second["repeat"]
        assert first["pandoc_executable"] == second["pandoc_executable"]
        assert first["lockfile"] == second["lockfile"]
        assert stable_results(first) == stable_results(second), first["path_id"]
    assert counted == Counter(paths=40, attempted=38, blocked_before_execution=2, stages=132, stage_exit_0=132)

    if fresh:
        actual = read_jsonl(fresh)
        assert len(actual) == len(groups) and {x["path_id"] for x in actual} == groups.keys()
        for row in actual:
            baseline = groups[row["path_id"]][0]
            assert stable_results(row) == stable_results(baseline), row["path_id"]
            assert row["checkout_clean_at_start"] and row["versions"] == baseline["versions"]
            assert row["pandoc_executable"] == baseline["pandoc_executable"]
            assert row["lockfile"] == baseline["lockfile"]

    observed = {k: v[0]["summary"] for k, v in groups.items()}
    assert observed["E2-default"]["plain_lines"] == ["first column"]
    assert observed["E2-drop-pre"]["plain_lines"] == ["first column", "second column"]
    assert observed["E2-default-lf"] == observed["E2-default"]
    assert observed["E2-html-reader"]["top_level"] == ["Table"]
    assert observed["E3-default"]["top_level"] == ["Para"]
    assert observed["E3-commonmark"]["plain_lines"] == observed["E3-braced"]["plain_lines"]
    assert observed["E3-commonmark"]["code_blocks"] != observed["E3-braced"]["code_blocks"]
    assert observed["X05-static-boundary"]["original"]["html"] == observed["X05-static-boundary"]["formatted"]["html"]
    assert "&#x60;" in observed["X05-nested-boundary"]["formatted"]["blocks"][0]["literal"]
    assert [b["type"] for b in observed["X05-raw-nested-boundary"]["formatted"]["blocks"]] == [
        "code_block", "paragraph", "code_block", "paragraph",
    ]
    assert observed["X05-raw-format-expanded"]["original"] == observed["X05-raw-format-expanded"]["formatted"]
    return counted


def validate_sources():
    rows = read_jsonl(WORK / "sources.jsonl")
    codes = {row["source_id"] for row in rows}
    assert len(rows) == len(codes)
    counted = [row for row in rows if row["counts_toward_category_minimum"]]
    assert len({x["work_id"] for x in counted}) == len(counted)
    assert all(x["access"] == "opened" for x in counted)
    assert {q for row in rows for q in row["questions"]} >= {f"Q{i}" for i in range(1,9)}
    for row in read_csv(WORK / "distinctions.csv"):
        assert set(row["source_ids"].split()) <= codes
        assert row["natural_valid_pair"] == "no"
    passed = read_jsonl(WORK / "evidence/public-tests.jsonl")
    assert len(passed) == 6 and all(row["matched"] and row["source_id"] in codes for row in passed)
    return {"all_rows": len(rows), "unique_work_ids": len({r["work_id"] for r in rows}),
            "access": Counter(r["access"] for r in rows),
            "credited_by_category": Counter(r["category"] for r in counted),
            "credited_assets": len(counted),
            "credited_publication_lineages": len({r["publication_lineage"] for r in counted})}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-replay", type=Path)
    args = parser.parse_args()
    bodies = snapshot_bodies()
    packets = validate_packets(bodies)
    runs = validate_runs(args.compare_replay)
    sources = validate_sources()
    print(json.dumps({
        "body_snapshots": len(bodies),
        "packets_planned": len(packets),
        "packets_materialized": sum(x["payload"] is not None for x in packets),
        "runs": runs,
        "sources": sources,
        "final_checkout_replay_paths": 20 if args.compare_replay else None,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
