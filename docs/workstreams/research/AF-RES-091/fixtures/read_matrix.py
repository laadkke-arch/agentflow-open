"""Fill all read positions, preserving the distinction between a read and a writer block."""

import argparse
import csv
import io
import json
import os
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely

from build import ARROW_SHA256, GPD_SHA, crs_record, dump, get_git, utc
from model import digest, geometry_record, read_spec, score_value, selections

QUERIES = ("T", "P")
ROW_AXES = {
    "exact_type": "type",
    "exact_xy": "xy",
    "dimension": "dimension",
    "z_coordinates": "z",
    "has_z": "has_z",
    "missing": "is_missing",
    "empty": "is_empty",
    "validity": "is_valid",
    "wkb_iso": "wkb_iso_hex",
    "attribute_value": "score",
}
FRAME_AXES = ("columns", "dtypes", "index", "active_geometry")


def compare_selection(expected, actual):
    origin = {row["id"]: row["score"] for row in expected}
    read = {row["id"]: row["score"] for row in actual}
    return {
        "expected": expected, "actual": actual, "matches": expected == actual,
        "missing_ids": sorted(origin.keys() - read.keys()),
        "unexpected_ids": sorted(read.keys() - origin.keys()),
        "different_score_ids": sorted(row_id for row_id in origin.keys() & read.keys() if origin[row_id] != read[row_id]),
    }


def observe_frame(frame, original, rectangle):
    expected_by_id = {rec["id"]: rec for rec in original["rows"]}
    restored = []
    checks = {}
    for row_id, score, geometry in frame[["id", "score", "geometry"]].itertuples(index=False):
        record = {"id": row_id, "score": score_value(score), **geometry_record(geometry)}
        restored.append(record)
        expected = expected_by_id.get(row_id)
        if expected is None:
            checks[row_id] = None
            continue
        row_checks = {axis: expected[key] == record[key] for axis, key in ROW_AXES.items()}
        row_checks["topology_xy"] = None
        if not (expected["is_missing"] or record["is_missing"]):
            wanted = shapely.from_wkb(bytes.fromhex(expected["wkb_iso_hex"]))
            row_checks["topology_xy"] = bool(shapely.equals(wanted, geometry))
        checks[row_id] = row_checks

    actual_order = [row["id"] for row in restored]
    expected_order = list(expected_by_id)
    observation = {
        "rows": restored, "crs": crs_record(frame.crs),
        "columns": list(frame.columns),
        "dtypes": {col: str(dtype) for col, dtype in frame.dtypes.items()},
        "index": list(frame.index), "active_geometry": frame.geometry.name,
        "id_order": actual_order,
        "duplicate_ids": sorted(row_id for row_id, count in Counter(actual_order).items() if count > 1),
        "missing_ids": sorted(expected_by_id.keys() - set(actual_order)),
        "unexpected_ids": sorted(set(actual_order) - expected_by_id.keys()),
    }
    selected = selections(frame, rectangle)
    observed_queries = {q: compare_selection(original["selections"][q], selected[q]) for q in QUERIES}
    comparison = {
        "by_id": checks,
        "frame": {
            **{axis: original[axis] == observation[axis] for axis in FRAME_AXES},
            "crs": observation["crs"] == original["crs"],
            "id_order": expected_order == actual_order,
        },
        "queries": observed_queries,
    }
    return observation, comparison


def reader_identity(source):
    source = source.resolve()
    head = get_git(source, "rev-parse", "HEAD")
    arrow_path = Path(gpd.io.arrow.__file__).resolve()
    arrow_sha = digest(arrow_path.read_bytes())
    if (head != GPD_SHA or arrow_sha != ARROW_SHA256 or gpd.__version__ != "1.0.0"
            or Path(gpd.__file__).resolve() != source / "geopandas" / "__init__.py"
            or get_git(source, "status", "--porcelain", "--untracked-files=no")):
        raise ValueError(f"Unexpected GeoPandas reader {head}, {arrow_sha}, {gpd.__file__}")
    return {
        "head": head, "version": gpd.__version__, "pandas": pd.__version__,
        "shapely": shapely.__version__, "geos": shapely.geos_version_string,
        "import_path": gpd.__file__, "arrow_path": str(arrow_path), "arrow_sha256": arrow_sha,
    }


def one_read(args):
    record = {
        "started_utc": utc(),
        "pid": os.getpid(),
        "command": [sys.executable, *sys.orig_argv[1:]],
        "repetition": args.repetition,
        "file_id": args.file.stem,
        "read_success": None,
    }
    status = 0
    try:
        record["reader"] = reader_identity(args.source)
        payload = args.file.read_bytes()
        original_bytes = args.original.read_bytes()
        record["input_sha256"] = digest(payload)
        record["original_sha256"] = digest(original_bytes)
        if record["input_sha256"] != args.sha256 or record["original_sha256"] != args.original_sha256:
            raise ValueError("Reader received bytes different from the sealed file or originals")
        original = json.loads(original_bytes)
        rectangle = read_spec()["rectangle"]
        record["read_success"] = False
        frame = gpd.read_parquet(io.BytesIO(payload))
        record["read_success"] = True
        record["observed"], record["comparison"] = observe_frame(frame, original, rectangle)
    except Exception as exc:
        record["exception"] = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
        status = {None: 19, False: 20, True: 21}[record["read_success"]]
    record["completed_utc"] = utc()
    record["exit"] = status
    print(json.dumps(record, ensure_ascii=False, allow_nan=False))
    return status


def matrix(args):
    root = args.input.resolve()
    out = args.out.resolve()
    (out / "evidence/read").mkdir(parents=True, exist_ok=True)
    files = list(csv.DictReader((root / "files.csv").open(encoding="utf-8")))
    runs = []
    for file in files:
        original_path = root / file["input_record"]
        original = json.loads(original_path.read_text(encoding="utf-8"))
        for repetition in read_spec()["repetitions"]:
            row = {
                "slot": f"{file['file_id']}-r{repetition}", "input": file["input"],
                "encoding": file["requested_encoding"], "repetition": repetition,
                "file_id": file["file_id"], "input_path": file["artifact"],
                "expected_file_sha256": file["output_sha256"] or None,
                "original_path": file["input_record"],
                "original": original,
                "reader_plan": {"head": GPD_SHA, "executable": sys.executable},
                "writer_status": file["status"],
            }
            if file["reader_ready"] != "True":
                writer_path = root / file["writer_receipt"]
                row.update(
                    run_status="blocked_by_writer", read_success=None, actual_input_sha256=None,
                    pid=None, exit=None, reader=None, command=None, observed=None, comparison=None,
                    raw_path=file["writer_receipt"], raw_sha256=digest(writer_path.read_bytes()),
                    exception=json.loads(writer_path.read_bytes())["exception"],
                )
                runs.append(row)
                continue

            raw_path = f"evidence/read/{row['slot']}.json"
            command = [
                sys.executable, "-B", str(Path(__file__)), "read", str(args.source.resolve()),
                str(root / file["artifact"]), file["output_sha256"], str(original_path),
                file["input_record_sha256"], str(repetition),
            ]
            completed = subprocess.run(command, capture_output=True, text=True, check=False)
            stdout = json.loads(completed.stdout) if completed.stdout.strip() else {}
            dump(out / raw_path, {
                "command": command, "exit": completed.returncode, "stdout": stdout,
                "stderr": completed.stderr,
            })
            row.update(
                run_status="observed" if completed.returncode == 0 else "process_error",
                read_success=stdout.get("read_success"), actual_input_sha256=stdout.get("input_sha256"),
                pid=stdout.get("pid"), exit=completed.returncode, reader=stdout.get("reader"),
                command=command, observed=stdout.get("observed"), comparison=stdout.get("comparison"),
                exception=stdout.get("exception"), raw_path=raw_path, raw_sha256=digest((out / raw_path).read_bytes()),
            )
            runs.append(row)
    with (out / "runs.jsonl").open("x", encoding="utf-8") as stream:
        for run in runs:
            stream.write(json.dumps(run, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n")
    dump(out / "evidence/read/summary.json", summary(runs))
    for run in runs:
        print(run["slot"], run["run_status"], run["pid"], run["exit"])


def summary(runs):
    indexed = {(row["input"], row["encoding"], row["repetition"]): row for row in runs}
    spec = read_spec()
    pairs = []
    repeated = []
    for input_id in spec["inputs"]:
        for rep in spec["repetitions"]:
            wkb = indexed[input_id, "WKB", rep]
            native = indexed[input_id, "geoarrow", rep]
            both = wkb["comparison"] is not None and native["comparison"] is not None
            pairs.append({
                "input": input_id, "repetition": rep, "slots": [wkb["slot"], native["slot"]],
                "status": "compared" if both else "unobservable_pair",
                "unobserved_slots": [run["slot"] for run in (wkb, native) if run["comparison"] is None],
                "observed_queries_equal": {
                    name: wkb["comparison"]["queries"][name]["actual"] == native["comparison"]["queries"][name]["actual"]
                    for name in QUERIES
                } if both else None,
                "observed_rows_equal": wkb["observed"]["rows"] == native["observed"]["rows"] if both else None,
            })
        for encoding in spec["encodings"]:
            r1, r2 = (indexed[input_id, encoding, rep] for rep in spec["repetitions"])
            available = r1["comparison"] is not None and r2["comparison"] is not None
            repeated.append({
                "file_id": r1["file_id"],
                "available": available,
                "same_sha": r1["actual_input_sha256"] == r2["actual_input_sha256"] if available else None,
                "different_pid": r1["pid"] != r2["pid"] if available else None,
                "stable_rows_frame_queries": (
                    r1["observed"] == r2["observed"] and r1["comparison"] == r2["comparison"]
                ) if available else None,
            })
    observed = [run for run in runs if run["comparison"] is not None]
    queries = {}
    for query in QUERIES:
        cells = [(run, run["comparison"]["queries"][query]) for run in observed]
        queries[query] = {
            "observed": len(cells), "matching": sum(result["matches"] for _, result in cells),
            "missing_ids_by_slot": {run["slot"]: cell["missing_ids"] for run, cell in cells if cell["missing_ids"]},
            "unexpected_ids_by_slot": {run["slot"]: cell["unexpected_ids"] for run, cell in cells if cell["unexpected_ids"]},
            "different_score_ids_by_slot": {
                run["slot"]: cell["different_score_ids"] for run, cell in cells if cell["different_score_ids"]
            },
            "expected_ids_unobserved_by_slot": {
                run["slot"]: [row["id"] for row in run["original"]["selections"][query]]
                for run in runs if run["comparison"] is None
            },
        }
    return {
        "planned_slots": len(runs), "statuses": dict(Counter(run["run_status"] for run in runs)),
        "writer_reader_pairs": pairs, "repetitions": repeated, "queries": queries,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    trial = subparsers.add_parser("matrix")
    trial.add_argument("input", type=Path)
    trial.add_argument("out", type=Path)
    trial.add_argument("source", type=Path)
    read = subparsers.add_parser("read")
    read.add_argument("source", type=Path)
    read.add_argument("file", type=Path)
    read.add_argument("sha256")
    read.add_argument("original", type=Path)
    read.add_argument("original_sha256")
    read.add_argument("repetition", type=int)
    args = parser.parse_args()
    if args.action == "read":
        return one_read(args)
    matrix(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
