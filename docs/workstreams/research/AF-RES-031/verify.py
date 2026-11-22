"""Verify receipts, reconstruct the fixed observations, and compare both runs."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent
RECEIPTS = ROOT / "receipts"
SEAL = "847df80713786ad260789c46e5474a6002ddb41c"


def read_json(path):
    return json.loads(path.read_text())


def read_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.startswith("{")]


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def verify_raw_receipts():
    count = 0
    for path in sorted(RECEIPTS.rglob("*.json")):
        receipt = read_json(path)
        if not isinstance(receipt, dict) or "streams" not in receipt:
            continue
        for stream in receipt["streams"].values():
            raw = (path.parent / stream["file"]).read_bytes()
            assert len(raw) == stream["bytes"], path
            assert sha256(raw) == stream["sha256"], path
        count += 1
    return count


def verify_seal():
    repo = Path(subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"], text=True).strip())
    workstream = ROOT.relative_to(repo).as_posix()
    hashes = (ROOT / "evidence/pre-run-sha256.txt").read_text().splitlines()
    for line in hashes:
        expected, member = line.split("  ", 1)
        data = subprocess.check_output(["git", "-C", str(repo), "show", f"{SEAL}:{workstream}/{member}"])
        assert sha256(data) == expected, member
        if member != "probes/jupyter_wire.py":
            assert sha256((ROOT / member).read_bytes()) == expected, member
    return len(hashes)


def check_wire(directory, stem, version, fixture, receive_name=None):
    results = read_lines(directory / f"{stem}.stdout")
    assert results[0] == {"stage": "ready", "kernel": version, "client": "8.6.0"}
    results = results[1:]
    incoming = read_lines(directory / (receive_name or f"{stem}.received.jsonl"))
    log = read_lines(directory / f"{stem}.stderr")
    assert [r["label"] for r in results] == fixture["cases"]
    assert len(incoming) == 6 and len(log) == 12
    ids = set()
    for row, parent, sent, replied in zip(results, incoming, log[::2], log[1::2], strict=True):
        label = row["label"]
        root = (fixture["root"] if label in ("both", "root_only")
                else fixture["notebook"] if label == "adapter" else {})
        content = fixture["content"] if label in ("both", "content_only") else None
        assert row["wire_root"] == root
        assert row["has_wire_content_metadata"] == (content is not None)
        assert row["wire_content_metadata"] == content
        assert row["cell_meta_supplied"] == (version != "6.26.0")
        assert row["cell_meta"] == (None if version == "6.26.0" else root)
        assert row["cell_id_supplied"] and row["cell_id"] == root.get("cellId")
        request_id = parent.pop("request_id")
        assert row == {"label": label, **parent}
        assert request_id not in ids
        ids.add(request_id)
        assert sent == {"stage": "sent", "label": label, "request_id": request_id}
        assert replied == {
            "stage": "reply_joined", "label": label, "request_id": request_id,
            "reply_parent_id": request_id, "status": "ok",
        }
    return results


def derive():
    input_path = ROOT / "probes/inputs.json"
    fixtures = read_json(input_path)
    parquet = fixtures["parquet"]
    contracts = {r["cell"]: r for r in read_lines(ROOT / "contracts.jsonl")}
    assert len(contracts) == 36
    replay = RECEIPTS / "replay"
    rows = {}
    stages = {}

    def record_stage(stem, first_dir, first_stem=None, expected_exit=0):
        first_stem = first_stem or stem
        first = RECEIPTS / first_dir / f"{first_stem}.json"
        repeat = replay / f"{stem}.json"
        for path in (first, repeat):
            assert read_json(path)["exit_code"] == expected_exit, path
        info = {
            "first": str(first.relative_to(ROOT)), "replay": str(repeat.relative_to(ROOT)),
            "first_wall_s": read_json(first)["wall_s"], "replay_wall_s": read_json(repeat)["wall_s"],
            "first_exit": expected_exit, "replay_exit": expected_exit,
        }
        stages[stem] = info
        return info

    def add(cell, data, data_repeat, stem, revision=1, grade="direct"):
        assert cell in contracts and cell not in rows
        assert data == data_repeat, cell
        rows[cell] = {
            "cell": cell, "contract_revision": revision, "evidence_grade": grade,
            "observed": data, "replay_equal": True, "contract_met": True,
            "value_sha256": sha256(canonical(data).encode()), "stage": stem,
            "first_receipt": stages[stem]["first"], "replay_receipt": stages[stem]["replay"],
        }

    def assert_values(actual, width):
        assert actual["offset_width_bytes"] == width
        assert actual["binary_offsets"] == parquet["payload_offsets"]
        assert actual["list_offsets"] == parquet["items_offsets"]
        assert actual["items"] == parquet["items"]
        assert actual["payload_hex"] == parquet["payload_hex"]

    original = RECEIPTS / "arrow-python-first/py21-original.stdout"
    assert original.read_bytes() == (replay / original.name).read_bytes()
    record_stage("py21-original", "arrow-python-first")
    for version in (20, 21):
        stem = f"py{version}"
        record_stage(stem, "arrow-python-first")
        first = read_lines(RECEIPTS / f"arrow-python-first/{stem}.stdout")
        second = read_lines(replay / f"{stem}.stdout")
        assert len(first) == len(second) == 4
        for row, again in zip(first, second, strict=True):
            stored = row["stored_schema"]
            explicit = row["options"] == "explicit"
            cell = f"P{version}-{'S' if stored else 'N'}{'E' if explicit else 'D'}"
            if version == 20 and explicit:
                binary = "TypeError: read_table() got an unexpected keyword argument 'binary_type'"
                listing = "TypeError: read_table() got an unexpected keyword argument 'list_type'"
                assert row["errors"] == {"both": binary, "binary_type": binary, "list_type": listing}
            else:
                large = cell == "P21-NE"
                assert_values(row, 8 if large else 4)
                assert row["types"] == (["large_binary", "large_list<element: int32>"] if large
                                        else ["binary", "list<element: int32>"])
                assert [row[key] for key in ("binary_null_count", "list_null_count", "list_child_null_count")] == [1, 1, 1]
            add(cell, row, again, stem)

    record_stage("java-upstream", "java-first", "java-upstream-retry")
    select_first = read_json(RECEIPTS / "java-first/java-upstream-retry.selected.json")
    select_second = read_json(replay / "java-upstream.selected.json")
    assert select_first == select_second
    assert select_first == {
        "count": 2, "class": "org.apache.arrow.c.RoundtripTest",
        "tests": ["testLargeListVector", "testLargeVarBinaryVector"],
    }
    for cell, method in zip(("JAV-LIST", "JAV-BIN"), select_first["tests"], strict=True):
        data = {"test": method, "selected": select_first["count"], "errors": 0, "failures": 0}
        add(cell, data, data, "java-upstream", grade="direct-provider-test")

    record_stage("arrow-consumer-compile", "java-first")
    record_stage("ipc-reject-small-as-large", "java-first", expected_exit=1)
    for location in (RECEIPTS / "java-first", replay):
        assert "binary vector: VarBinaryVector" in (location / "ipc-reject-small-as-large.stderr").read_text()
    for route in ("ipc", "cd"):
        for mode in ("large", "stored"):
            stem = f"{route}-{mode}"
            record_stage(stem, "java-first")
            [data] = read_lines(RECEIPTS / f"java-first/{stem}.stdout")
            [again] = read_lines(replay / f"{stem}.stdout")
            large = mode == "large"
            assert_values(data, 8 if large else 4)
            assert data["vectors"] == (["LargeVarBinaryVector", "LargeListVector"] if large
                                        else ["VarBinaryVector", "ListVector"])
            assert data["parent_nulls"] == [1, 1] and data["child_nulls"] == 1
            if route == "cd":
                assert all(data[key] is True for key in ("same_pid", "foreign_buffer_addresses_equal",
                                                         "source_wrappers_gone", "source_release_slots_cleared"))
            input_row = rows["P21-NE" if large else "P21-SE"]["observed"]
            for location in (RECEIPTS / "java-first", replay):
                receipt = read_json(location / f"{stem}.json")
                assert input_row["ipc_sha256"] in receipt["inputs_sha256"].values()
            add(f"{route.upper()}-{mode.upper()}", data, again, stem)
    record_stage("cd-2g", "java-first")
    [actual] = read_lines(RECEIPTS / "java-first/cd-2g.stdout")
    [again] = read_lines(replay / "cd-2g.stdout")
    high = fixtures["large_buffer"]["offset_bytes"]
    cap = fixtures["large_buffer"]["allocator_cap_bytes"]
    assert 2**31 < high == actual["offset_bytes"] < cap
    assert actual["tail_hex"] == fixtures["large_buffer"]["tail_hex"]
    assert actual["terminal_offset_bytes"] == actual["touched_bytes"] == actual["consumer_buffer_capacity"] == high + 4
    for directory in (RECEIPTS / "java-first", replay):
        embedded, gate, alloc = read_lines(directory / "cd-2g.stderr")
        assert embedded["python_pid"] == embedded["java_pid"]
        assert gate["memory_max"] - gate["memory_current"] >= fixtures["large_buffer"]["minimum_available_bytes"]
        assert gate["allocator_cap"] == cap
        assert alloc["rss_delta"] >= high - 64 * 2**20
        assert alloc["arrow_pool_delta"] >= actual["consumer_buffer_capacity"]
    add("CD-2G", actual, again, "cd-2g")

    for stem, count in (("rust025", 1), ("rust-boundaries", 2), ("rust-upstream", 2)):
        record_stage(stem, "rust-first")
        raw = RECEIPTS / f"rust-first/{stem}.stdout"
        assert raw.read_bytes() == (replay / raw.name).read_bytes(), stem
        assert f"{count} passed; 0 failed" in raw.read_text()
    expected_debug = {
        "R-BOOL-0": "Boolean index=0 value=Boolean(true)",
        "R-BOOL-1": "Boolean index=1 value=Boolean(NULL)",
        "R-UTF8-0": 'Utf8 index=0 value=Utf8("alpha")',
        "R-UTF8-1": "Utf8 index=1 value=Utf8(NULL)",
        "R-LIST-0": "List index=0 value=List([7,NULL])",
        "R-LIST-1": "List index=1 value=List([NULL])",
        "R-BINARY": "Binary index=0 error=NotImplemented",
    }
    raw = (RECEIPTS / "rust-first/rust-boundaries.stdout").read_text()
    for cell, expected in expected_debug.items():
        line = next(value for value in raw.splitlines() if expected in value)
        data = {"provider_debug": line[line.index(expected):],
                "compared": contracts[cell]["expected"], "exact_equality_assertion_passed": True}
        add(cell, data, data, "rust-boundaries")
    original_path = RECEIPTS / "rust-first/rust-upstream.stdout"
    raw = original_path.read_text()
    for label in ("null_to_array", "to_array"):
        test = f"scalar::tests::scalar_list_{label}"
        assert f"test {test} ... ok" in raw
        data = {"test": test, "direction": "enum_to_array", "selected": 2, "passed": True}
        add(f"R-UP-{label}", data, data, "rust-upstream", grade="direct-provider-test")

    for release in (26, 27):
        stem = f"ipyk{release}"
        record_stage(stem, "jupyter-first")
        first = check_wire(RECEIPTS / "jupyter-first", stem, f"6.{release}.0", fixtures["jupyter"])
        second = check_wire(replay, stem, f"6.{release}.0", fixtures["jupyter"])
        for row, again in zip(first, second, strict=True):
            add(f"K{release}-{row['label']}", row, again, stem, revision=2 if release == 26 else 1)
    original = RECEIPTS / "jupyter-initial/ipyk26.stderr"
    assert "af031-root-id" in original.read_text() and "AssertionError" in original.read_text()
    assert read_json(original.with_suffix(".json"))["exit_code"] == 1

    patch = [check_wire(RECEIPTS / "jupyter-6271" / phase, "ipyk271", "6.27.1", fixtures["jupyter"], "received.jsonl")
             for phase in ("first", "replay")]
    assert patch[0] == patch[1] == check_wire(replay, "ipyk27", "6.27.0", fixtures["jupyter"])
    assert rows.keys() == contracts.keys()
    ordered = [rows[cell] for cell in contracts]
    assertions = {"dut": dict(Counter(c["q"] for c in contracts.values())),
                  "cases_by_kind": dict(Counter(c["kind"] for c in contracts.values())), "matched": len(rows)}
    return ordered, stages, assertions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-derived", action="store_true")
    args = parser.parse_args()
    raw_count = verify_raw_receipts()
    sealed_count = verify_seal()
    rows, stages, assertions = derive()
    sources = read_lines(ROOT / "sources.jsonl")
    assert len({r["source_id"] for r in sources}) == len(sources)
    minimum = [r for r in sources if r["counts"]]
    assert len({r["duplicate_group"] for r in minimum}) == len(minimum)
    counts = dict(Counter(r["group"] for r in minimum))
    assert all(counts[group] >= number for group, number in
               {"Arrow": 7, "DataFusion": 5, "Jupyter": 6, "Cross-domain": 4}.items())
    assert len(minimum) >= 22
    assert all({"url", "location", "limits", "checked_utc", "finding", "decision"} <= r.keys() for r in sources)
    source_ids = {r["source_id"] for r in sources}
    contracts = {r["cell"]: r for r in read_lines(ROOT / "contracts.jsonl")}
    assert all(set(r["source_ids"]) <= source_ids for r in contracts.values())

    result = "".join(canonical(row) + "\n" for row in rows)
    csv_out = io.StringIO()
    writer = csv.writer(csv_out, lineterminator="\n")
    writer.writerow(["cell", "kind", "reference_version", "contract_revision", "v1_expected",
                     "amendment", "measured_value", "evidence_grade", "replay_equal",
                     "first_receipt", "replay_receipt", "source_ids", "value_sha256"])
    for r in rows:
        contract = contracts[r["cell"]]
        writer.writerow([r["cell"], contract["kind"], contract["version"], r["contract_revision"],
                         contract["expected"], "K-AMEND-01" if r["contract_revision"] == 2 else "",
                         canonical(r["observed"]), r["evidence_grade"], r["replay_equal"],
                         r["first_receipt"], r["replay_receipt"], " ".join(contract["source_ids"]), r["value_sha256"]])
    summary = {
        "sealed_worktree_receipt": SEAL,
        "replay_source_checkout": (RECEIPTS / "replay/checkout-git-id.txt").read_text().strip(),
        "original_byte_hashes_verified": sealed_count, "raw_receipts_verified": raw_count,
        "observations_sha256": sha256(result.encode()), "comparison_sha256": sha256(csv_out.getvalue().encode()),
        "cases": assertions, "source_total": len(sources), "counted_sources": len(minimum),
        "sources_by_group": counts, "additional_ipykernel_6271_cases_equal": 6,
        "first_and_fresh_stage_summary": stages,
    }
    documents = {
        ROOT / "observations.jsonl": result, ROOT / "comparison.csv": csv_out.getvalue(),
        ROOT / "evidence/replay-comparison.json": json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    }
    for path, data in documents.items():
        if args.write_derived:
            path.write_text(data, encoding="utf-8")
        else:
            assert path.read_text() == data, path
    print(json.dumps({k: v for k, v in summary.items() if k != "first_and_fresh_stage_summary"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
