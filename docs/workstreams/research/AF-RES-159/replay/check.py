#!/usr/bin/env python3
"""Check pre/post joins and compare a new checkout's output to the sealed measurements."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from run import PO_HASHES, sha
from score import read_csv, read_jsonl
from seal import ROOT, VIEWS, encoded


def keyed_runs(rows, repeat):
    selected = [r for r in rows if r.get("repeat") == repeat and r["row_type"] == "lookup"]
    result = {}
    for item in selected:
        key = item["catalog"], item["call_id"], item["language"], item["mode"]
        assert key not in result, key
        assert item["exit"] == item["glib"]["exit"] == 0, key
        assert item["stdout_sha256"] == sha(item["stdout"].encode()) == item["glib"]["stdout_sha256"], key
        assert bytes.fromhex(item["stdout_hex"]) == item["stdout"].encode(), key
        assert item["po_sha256"] == PO_HASHES[item["product"], item["language"]], key
        result[key] = tuple(item[k] for k in (
            "input_sha256", "mo_sha256", "stdout_sha256", "mo_has_key", "po_state", "po_key_line",
        ))
    return result


def compare_repeats(path, expected_len):
    result = read_jsonl(path)
    first, second = (keyed_runs(result, repeat) for repeat in ("W1", "W2"))
    assert first == second and len(first) == expected_len
    for item in result:
        kind = item["row_type"]
        if kind == "compile":
            assert item["exit"] == item["validation"]["exit"] == 0
            assert item["po_sha256"] == PO_HASHES[item["product"], item["language"]]
        if kind == "probe_build":
            assert item["exit"] == 0
    return result, first


def check_frame(frame, sources):
    for product in ("G", "I"):
        for desired, layer in ((12, "natural_candidate"), (2, "single_control")):
            portion = [row for row in frame if row["id"].startswith(product) and row["layer"] == layer]
            assert [int(r["rank"]) for r in portion] == list(range(1, desired + 1))
            assert [r["utf8_hex"] for r in portion] == sorted(r["utf8_hex"] for r in portion)
            for row in portion:
                assert row["msgid"] and row["msgid"].encode().hex() == row["utf8_hex"]
                options = json.loads(row["explicit_contexts"])
                choice = json.loads(row["chosen"])
                assert [x.encode() for x in options] == sorted(x.encode() for x in options)
                assert len(options) >= (1 if layer == "single_control" else 2)
                assert (choice == options[:2]) == (row["status"] == "sealed")
    for call in read_csv(ROOT / "calls.csv"):
        code = call["id"][0]
        row = next(item for item in frame if item["id"] == call["group"])
        assert row["msgid"] == call["msgid"] and call["context"] in json.loads(row["chosen"])
        actual_reference = [tuple(loc) for key in json.loads(row["all_refs"])
                            for loc in key["references"] if call["context"] == key["context"]]
        assert tuple(json.loads(call["anchor"])) == actual_reference[0]
        for key in ("b", "c"):
            proof = json.loads(call[key])
            position = proof["line"] - 1
            full = (sources[code] / proof["path"]).read_bytes().split(b"\n")[position]
            assert sha(full) == proof["line_sha256"]
            assert full[proof["utf8_start"]:proof["utf8_end_exclusive"]].decode() == proof["text"]


def check_packets():
    calls = {r["id"]: r for r in read_csv(ROOT / "calls.csv")}
    packets = read_jsonl(ROOT / "packets.jsonl")
    predicates = read_csv(ROOT / "predictions.csv")
    assert len(packets) == len(predicates) == 280
    assert len({r["packet_id"] for r in packets}) == len(packets)
    assert all(r["sealed_utc"] for r in predicates)
    for packet, before in zip(packets, predicates, strict=True):
        k = packet["call_id"]
        payload = packet["payload"]
        view = packet["view"]
        assert packet["packet_id"] == before["packet_id"] and view == before["view"]
        assert sha(encoded(payload)) == packet["payload_sha256"] == before["payload_sha256"]
        assert len(encoded(payload)) == packet["payload_bytes"]
        assert payload["selection"] == calls[k]["msgid"]
        assert packet["selection_bytes"] == len(calls[k]["msgid"].encode())
        assert len(json.loads(before["candidate_urls"])) >= 1
        if view in ("B", "C"):
            source = packet["source_span"]
            assert payload["reference"] == source["text"]
            assert len(source["text"].encode()) == packet["reference_bytes"]
    index = {(p["call_id"], p["payload"]["language"], p["view"]): p for p in packets}
    groups = {r["group"] for r in calls.values() if r["group"][1] != "C"}
    for group in groups:
        for lang in ("ko", "de"):
            assert index[group+"a",lang,"A"]["payload"] == index[group+"b",lang,"A"]["payload"]
    for k in calls:
        for lang in ("ko", "de"):
            assert index[k,lang,"C"]["reference_bytes"] <= index[k,lang,"B"]["reference_bytes"]
    return calls, predicates


def check_sources(roots, calls):
    readings = read_jsonl(ROOT / "sources.jsonl")
    assert len({i["source_id"] for i in readings}) == len(readings)
    eligible = [i for i in readings if i["counts_toward_floor"]]
    assert len({i["work_id"] for i in eligible}) == len(eligible) >= 20
    floors = dict(ui_change=6, contract=4, release_compat=6, geographic_record=2, cultural_record=2)
    levels = Counter(i["material_type"] for i in eligible)
    assert all(levels[category] >= lower for category, lower in floors.items()), levels
    assert all(i["result"] == "opened" for i in eligible)
    needed = ("work_id", "lineage", "questions", "claim_ids", "material_type", "publisher",
              "source_url", "fixed_url", "verified_utc", "read_locus", "confirmed",
              "limitation_or_alternate", "result", "floor_reason")
    assert all(all(row[f] for f in needed) for row in readings)
    code = [r for r in readings if r["material_type"] == "release_code"]
    observed_calls = set()
    po_calls = set()
    for row in readings:
        if row["material_type"] == "catalog":
            po_calls.update(row["claim_ids"])
    for row in code:
        observed_calls.update(row["claim_ids"])
        project = "G" if row["version"] == "3.0.6" else "I"
        file = row["read_locus"].split(" · ", 1)[0]
        assert sha((roots[project] / file).read_bytes()) == row["sha256"], file
    assert set(calls) <= observed_calls and set(calls) <= po_calls
    print(f"sources {len(readings)} rows, {len(eligible)} independent: {dict(levels)}, "
          f"{sum(r['result'] == 'failed' for r in readings)} failed accesses")


def check_markdown(path):
    lines = path.read_text(encoding="utf-8").rstrip().splitlines()
    footer = "| 불일치·약점 | 영향을 받는 결론 | 다음 조사·자료 | 결론을 바꿀 관측 |"
    assert lines[-5] == footer and all(l.startswith("|") for l in lines[-5:])
    for row in lines[-3:]:
        assert len(re.findall(r"(?<!\\)\|", row)) == 5
    if path.name == "RESULT.md":
        assert lines[0].startswith("# ") and lines[2].startswith("| 제품·판·자연 그룹")
        order = [next(i for i, l in enumerate(lines) if l.startswith("| "+col)) for col in (
            "제품·판·자연 그룹", "그룹·언어", "유일하게 정해지는 조건"
        )]
        q = next(i for i,l in enumerate(lines) if l.startswith("## Q1"))
        assert order == sorted(order) and max(order) < q


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gimp", type=Path, required=True)
    parser.add_argument("--inkscape", type=Path, required=True)
    parser.add_argument("--compare-main", type=Path)
    parser.add_argument("--compare-supplement", type=Path)
    args = parser.parse_args()
    roots = {"G": args.gimp, "I": args.inkscape}
    check_frame(read_csv(ROOT / "frame.csv"), roots)
    calls, predicts = check_packets()
    runs, main = compare_repeats(ROOT / "runs.jsonl", 328)
    _, supplement = compare_repeats(ROOT / "evidence/supplement-runs.jsonl", 12)
    if args.compare_main:
        assert keyed_runs(read_jsonl(args.compare_main), "verify") == main
    if args.compare_supplement:
        assert keyed_runs(read_jsonl(args.compare_supplement), "verify") == supplement
    earliest = min(r["utc"] for r in runs if r["row_type"] == "compile")
    assert all(r["sealed_utc"].replace("Z","+00:00") < earliest for r in predicts)
    actual = [r for r in runs if r["row_type"] == "lookup" and r["repeat"] == "W1"]
    results = [r for r in actual if r["catalog"] == "compiled" and r["mode"] == "context"]
    assert Counter(r["po_state"] for r in results) == {"translated": 54, "fuzzy": 2}
    for row in actual:
        if row["catalog"] == "published":
            local = main[("compiled", row["call_id"], row["language"], row["mode"])]
            assert local[:3] == (row["input_sha256"], row["mo_sha256"], row["stdout_sha256"])
    scores = read_csv(ROOT / "evidence/scores.csv")
    expected = [8, 54, 56, 8, 50]
    assert [sum(r["view"] == v and r["function_result"] == "유일_일치" for r in scores)
            for v in VIEWS] == expected
    assert len(scores) == len(predicts)
    assert len(read_csv(ROOT / "evidence/neighbor-sensitivity.csv")) == 48
    check_sources(roots, calls)
    check_markdown(ROOT / "RESULT.md")
    if (ROOT / "HANDOFF.md").is_file():
        check_markdown(ROOT / "HANDOFF.md")
    print("frame 28, calls 28, packets/predictions 280, main 328×2, supplements 12×2")
    print("fresh process comparisons use only pinned input, MO and output hashes")


if __name__ == "__main__":
    main()
