"""Check the committed AF-RES-091 grid, source ledger, and report references."""

import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAMILY = ("S0", "S1", "S2", "S3")
ENCODINGS = ("WKB", "geoarrow")
QUERIES = ("T", "P")
AXES = (
    "exact_type", "exact_xy", "dimension", "z_coordinates", "has_z", "missing",
    "empty", "validity", "wkb_iso", "attribute_value",
)
SOURCE_MINIMA = dict(standard=5, library=7, downstream=8, tabular=2, palette=2)


def sha(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def read_jsonl(relative):
    return [json.loads(line) for line in (ROOT / relative).read_text(encoding="utf-8").splitlines()]


def read_csv(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def check_files():
    files = read_csv("files.csv")
    assert [(row["input"], row["requested_encoding"]) for row in files] == [
        (input_id, encoding) for input_id in FAMILY for encoding in ENCODINGS
    ]
    input_sha = sha("fixtures/inputs.json")
    assert input_sha == "d9303498152bcb6567843204633c33ce5691c0a106578f3de8204576280f5aa8"
    assert len(read_json("environments.json")["wheels"]) == 23
    assert all(read_json("environments.json")["same_as_087_N"].values())
    by_id = {}
    for row in files:
        ident = row["file_id"]
        by_id[ident] = row
        assert row["manual_input_sha256"] == input_sha
        assert sha(row["input_record"]) == row["input_record_sha256"]
        writer = read_json(row["writer_receipt"])
        assert writer["file_id"] == ident and writer["writer_head"] == row["writer_commit"]
        assert writer["requested"]["geometry_encoding"] == row["requested_encoding"]
        assert writer["input_record_sha256"] == row["input_record_sha256"]
        if row["status"] == "written":
            assert row["reader_ready"] == "True"
            assert sha(row["artifact"]) == row["output_sha256"] == writer["output_sha256"]
            assert (ROOT / row["artifact"]).stat().st_size == int(row["bytes"])
            footer = read_json(row["footer_receipt"])
            assert footer["exit"] == 0 and not footer["stdout"]["geopandas_loaded"]
            assert footer["stdout"]["sha256"] == row["output_sha256"]
            geo = footer["stdout"]["geo"]
            assert geo["version"] == row["geo_version"] == "1.1.0"
            col = geo["columns"][geo["primary_column"]]
            assert col["encoding"] == row["encoding"]
            assert col["geometry_types"] == json.loads(row["geometry_types"])
            assert col["crs"]["id"] == {"authority": "EPSG", "code": 4326}
            assert footer["stdout"]["root_geometry"]["valid"] == [True, True, False, True]
            assert footer["stdout"]["scores"] == [101, None, -3, 0]
            assert footer["stdout"]["geo_footer_sha256"] == row["geo_footer_sha256"]
        else:
            assert row["reader_ready"] == "False"
            assert row["status"] == "writer_exception" and not row["output_sha256"]
            assert writer["output_buffer_bytes"] == 0 and writer["exception"]["type"] == "ArrowInvalid"
            assert "list offsets (3) larger than values array (length 2)" in writer["exception"]["message"]
            fixture = read_json(f"fixtures/{ident}.refusal.json")
            assert fixture["writer_receipt"]["sha256"] == sha(row["writer_receipt"])
            assert not (ROOT / f"fixtures/{ident}.parquet").exists()
    assert Counter(row["status"] for row in files) == {"written": 5, "writer_exception": 3}
    return by_id


def check_reads(files):
    runs = read_jsonl("runs.jsonl")
    expected_slots = [f"{name}-r{rep}" for name in files for rep in (1, 2)]
    assert [run["slot"] for run in runs] == expected_slots
    counts = Counter()
    spec = read_json("fixtures/inputs.json")
    for run in runs:
        row = files[run["file_id"]]
        assert run["original"] == read_json(row["input_record"])
        assert run["original"]["selections"] == {query: spec["inputs"][run["input"]][query] for query in QUERIES}
        assert run["raw_sha256"] == sha(run["raw_path"])
        raw = read_json(run["raw_path"])
        if run["run_status"] == "blocked_by_writer":
            assert run["read_success"] is None and run["pid"] is None and run["exit"] is None
            assert run["comparison"] is None and run["observed"] is None
            assert run["exception"] == raw["exception"] and run["actual_input_sha256"] is None
            counts["writer_blocks"] += 1
            continue
        assert run["run_status"] == "observed" and run["exit"] == raw["exit"] == 0
        assert run["read_success"] and run["actual_input_sha256"] == row["output_sha256"]
        assert run["reader"]["head"] == row["writer_commit"]
        for key in ("command", "pid", "comparison", "observed", "read_success"):
            assert run[key] == raw["stdout"][key]
        compare = run["comparison"]
        assert all(compare["frame"].values())
        for geom in run["observed"]["rows"]:
            row_id = geom["id"]
            observed = compare["by_id"][row_id]
            assert all(observed[axis] for axis in AXES)
            assert observed["topology_xy"] is (None if row_id == "N" else True)
            if row_id in ("A", "B"):
                counts["nonempty_xy"] += 1
                counts["finite_z"] += sum(isinstance(value, (int, float)) and math.isfinite(value) for value in geom["z"])
        for query in QUERIES:
            observed = compare["queries"][query]
            assert observed["matches"] and observed["expected"] == observed["actual"]
            assert not any(observed[key] for key in ("missing_ids", "unexpected_ids", "different_score_ids"))
            counts[f"{query}_rows"] += len(observed["actual"])
        counts["reads"] += 1
    assert counts == {"reads": 10, "writer_blocks": 6, "nonempty_xy": 20, "finite_z": 6, "T_rows": 14, "P_rows": 10}
    assert len({r["pid"] for r in runs if r["pid"]}) == 10
    summary = read_json("evidence/read/summary.json")
    assert [(p["input"], p["repetition"]) for p in summary["writer_reader_pairs"]] == [
        (ident, repeat) for ident in FAMILY for repeat in (1, 2)
    ]
    assert Counter(p["status"] for p in summary["writer_reader_pairs"]) == {"compared": 2, "unobservable_pair": 6}
    for p in summary["writer_reader_pairs"]:
        if p["status"] == "compared":
            assert p["observed_rows_equal"] and p["observed_queries_equal"] == dict.fromkeys(QUERIES, True)
    assert sum(rep["stable_rows_frame_queries"] is True for rep in summary["repetitions"]) == 5
    for rep in summary["repetitions"]:
        if rep["available"]:
            assert rep["same_sha"] and rep["different_pid"]
    for result in summary["queries"].values():
        assert result["observed"] == result["matching"] == 10
        assert not any(result[key] for key in ("missing_ids_by_slot","unexpected_ids_by_slot","different_score_ids_by_slot"))
        assert list(result["expected_ids_unobserved_by_slot"].values()) == [["A"]] * 6
    return runs, counts


def check_contrasts():
    auxiliary = "evidence/auxiliary/"
    diagnostic = read_json(auxiliary+"original-ragged.json")["original_inputs"]
    for ident in FAMILY[1:]:
        assert diagnostic[ident]["offsets"] == [[0, 1, 2, 2, 3]]
        assert len(diagnostic[ident]["coords"]) == 2
    blocked = read_json(auxiliary+"S1-drop-N.json")
    assert blocked["write_status"] == "writer_exception" and blocked["ragged"]["offsets"] == [[0, 1, 2, 3]]
    for variant in ("S1-drop-E", "S1-empty-MultiPoint", "S2-drop-E", "S3-drop-E"):
        result = read_json(auxiliary+variant+".json")
        assert result["sha256"] == sha(auxiliary+result["bytes_path"])
        query = result["read"]["comparison"]["queries"]
        assert query["P"]["matches"] and query["T"]["missing_ids"] == ["A"]
        assert query["T"]["actual"] == []
    xyz = read_json(auxiliary+"S2-drop-E.json")["read"]["observed"]["rows"]
    assert [r["z"] for r in xyz] == [[135.25], [-42.5], []]
    mixed = read_json(auxiliary+"S3-drop-E.json")
    assert mixed["footer"]["stdout"]["root_geometry"]["values"]["fields"]["z"]["values"] == [135.25, "nan"]
    assert mixed["read"]["observed"]["rows"][1]["dimension"] == 2
    alias = read_json(auxiliary+"type-alias.json")
    assert alias["same_bytes"] and alias["alternate"]["sha256"] == alias["baseline"]["sha256"] == sha(auxiliary+"S1-drop-E.parquet")
    assert alias["baseline"]["original"]["selections"]["T"] == [{"id":"A","score":101}]
    assert alias["alternate"]["original"]["selections"]["T"] == [{"id":"B","score":None}]
    assert alias["alternate"]["observed"] == alias["baseline"]["observed"]
    ext = read_json("evidence/external/consumer-controls.json")["results"]
    assert len(ext) == 3 and all(cell["Dask_cx"] == [{"id":"A","score":101}] for cell in ext.values())
    assert all(cell["notebook_unmodified"]["error"] == "AttributeError" for cell in ext.values())
    tests = read_json("evidence/external/upstream-tests.json")["records"]
    assert [record["exit"] for record in tests] == [0, 0, 0]
    representation = read_json("evidence/external/representation-controls.json")
    small = representation["small_integers"]
    assert small["plain"]["normalized_numeric_values"] == small["input"]["normalized_numeric_values"]
    assert small["plain"]["integer_columns"] == [] and small["mapped"]["integer_columns"] == ["score"]
    assert representation["consecutive_large_ids"]["plain"]["duplicated_value_row_ids"] == ["A","B"]
    for page in ("small_integers","consecutive_large_ids"):
        assert representation[page]["mapped_roundtrip_equal"] and representation[page]["metadata_roundtrip_equal"]
    pal = representation["palette"]
    assert pal["swap_rgba_equal"] and not pal["swap_index_selection_equal"]
    assert pal["identity_rgba_equal"] and pal["identity_index_selection_equal"]


def check_sources_and_report(runs):
    rows = read_jsonl("sources.jsonl")
    source_receipts = read_jsonl("evidence/source-reads.jsonl")
    assert len(rows) == len(source_receipts)
    assert len({row["source_id"] for row in rows}) == len(rows)
    for source, receipt in zip(rows, source_receipts, strict=True):
        assert source["source_id"] == receipt["source_id"] and source["status"] == receipt["status"]
        if source["commit"]:
            assert source["fingerprint"]["sha256"] == receipt["full_sha256"]
        assert source["origin_url"].startswith("https://") and source["limit"] and source["checked"]
    included = [r for r in rows if r["counted"]]
    categories = Counter(r["category"] for r in included)
    assert len({r["reopen_url"] for r in included}) == len(included) == 52
    assert len({r["lineage_id"] for r in included}) == 38
    assert all(categories[k] >= minimum for k, minimum in SOURCE_MINIMA.items())
    assert {row["id"] for row in read_csv("consumers.csv")} >= {"CT", "CP", "EX-P", "EX-T"}
    for filename in ("RESULT.md","SELF_CHECK.md","reproduce.md","SCOPE.md"):
        content = (ROOT / filename).read_text(encoding="utf-8")
        for path in re.findall(r"\]\(([^)\s]+)\)", content):
            if not path.startswith(("https://", "#")):
                assert (ROOT / path.split("#", 1)[0]).exists(), (filename, path)
    report = (ROOT / "RESULT.md").read_text(encoding="utf-8")
    h1, h2, h3, denominators = [report.index(part) for part in ("## 표 1", "## 표 2", "## 표 3", "### 분모")]
    assert 0 < h1 < h2 < h3 < denominators
    assert len(re.findall(r"^\| S[0-3]", report[h1:h2], flags=re.M)) == 8
    assert len(re.findall(r"^\| S[0-3]", report[h2:h3], flags=re.M)) == 16
    for file in read_csv("files.csv"):
        assert f"({file['artifact']})" in report[h1:h2]
    for run in runs:
        assert f"({run['raw_path']})" in report[h2:h3]
    assert len(re.findall(r"^[1-3]\. ", report.split("## 핵심 약점",1)[1], flags=re.M)) == 3
    return {"counted_sources":len(included), "source_lineages":38, "ledger_rows":len(rows), "by_category":categories}


def main():
    files = check_files()
    runs, counts = check_reads(files)
    check_contrasts()
    sources = check_sources_and_report(runs)
    print(json.dumps({"status":"passed", "writer_slots":len(files), "reader_slots":len(runs), "read_counts":counts, **sources},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
