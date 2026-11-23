"""Build and replay counterexamples without changing the primary matrix."""
import argparse
import csv
import io
import json
import os
import subprocess
import sys
from pathlib import Path

from generate import HERE, checked_geopandas, crs_summary, digest, dump, make_frame, utc, writer_kwargs
from observe import crs_comparison, geometry_record, scalar
from read_matrix import read_one

POINT_CASES = HERE / "fixtures/point-cases.json"
POINT_FILES = {"C-WKB": "WKB", "C-native": "geoarrow"}
MAIN_CONTROLS = ("B-cell", "D-missing-crs", "D-null-crs", "E-added", "F-no-pandas-meta")


def point_frame(gpd):
    import shapely

    spec = json.loads(POINT_CASES.read_bytes())
    geoms = [shapely.from_wkt(row["geometry"]) if row["geometry"] is not None else None
             for row in spec["rows"]]
    return gpd.GeoDataFrame(
        {"feature_id": [row["feature_id"] for row in spec["rows"]]},
        geometry=geoms, crs=spec["crs"],
    )


def rewrite(source, target, mode):
    import pyarrow.parquet as pq

    payload = source.read_bytes()
    table = pq.read_table(io.BytesIO(payload), use_threads=False)
    metadata = dict(table.schema.metadata)
    if mode == "F-no-pandas-meta":
        del metadata[b"pandas"]
    else:
        geo = json.loads(metadata[b"geo"])
        for column in geo["columns"].values():
            if mode == "D-missing-crs":
                del column["crs"]
            else:
                column["crs"] = None
        metadata[b"geo"] = json.dumps(geo).encode()
    pq.write_table(table.replace_schema_metadata(metadata), target, compression="snappy", version="2.6")
    return digest(payload)


def build(source, fixtures, output):
    import pandas as pd

    gpd, writer = checked_geopandas("N", source)
    _, changed = make_frame(gpd)
    changed.loc[0, "score"] = 8
    _, added = make_frame(gpd)
    added["new_flag"] = pd.Series([True, False], dtype="boolean")
    point = point_frame(gpd)
    records = {}
    for name, frame, encoding in (
        ("B-cell", changed, "WKB"), ("E-added", added, "WKB"),
        *((name, point, encoding) for name, encoding in POINT_FILES.items()),
    ):
        kwargs = writer_kwargs("N", "1.1.0", encoding)
        target = output / f"{name}.parquet"
        frame.to_parquet(target, **kwargs)
        records[name] = {
            "utc": utc(), "sha256": digest(target.read_bytes()), "writer": writer,
            "method": "GeoDataFrame.to_parquet", "kwargs": kwargs,
        }

    for name in ("D-missing-crs", "D-null-crs", "F-no-pandas-meta"):
        source_id = "F3" if name == "F-no-pandas-meta" else "F1"
        target = output / f"{name}.parquet"
        input_hash = rewrite(fixtures / f"{source_id}.parquet", target, name)
        records[name] = {
            "utc": utc(), "sha256": digest(target.read_bytes()), "input_sha256": input_hash,
            "method": "pyarrow.parquet.write_table", "source_file": source_id, "metadata_edit": name,
        }
    dump(records)


def pyarrow_read(file, expected_hash):
    import pyarrow.parquet as pq

    payload = file.read_bytes()
    assert digest(payload) == expected_hash
    table = pq.read_table(io.BytesIO(payload), use_threads=False)
    frame = table.to_pandas()
    geom_encoding = json.loads(table.schema.metadata[b"geo"])["columns"]
    dump({
        "utc": utc(), "source_bytes_sha256": digest(payload),
        "table_type": type(table).__qualname__, "frame_type": type(frame).__qualname__,
        "active_geometry": getattr(frame, "_geometry_column_name", None),
        "rows": table.num_rows, "names": table.column_names,
        "geometry_pandas_dtype": str(frame["geometry"].dtype),
        "metadata_keys": sorted(k.decode() for k in table.schema.metadata),
        "geometry_storage_type": str(table["geometry"].type),
        "geometry_storage_values": table["geometry"].to_pylist(),
        "probe_storage_type": str(table["probe"].type),
        "probe_storage_values": table["probe"].to_pylist(),
        "geo_metadata_encodings": {name: col["encoding"] for name, col in geom_encoding.items()},
        "semantic_spatial": False,
    })


def read_points(role, source, file, expected_hash):
    import pyarrow.parquet as pq

    gpd, reader = checked_geopandas(role, source)
    baseline = point_frame(gpd)
    payload = file.read_bytes()
    assert digest(payload) == expected_hash
    column = pq.read_table(io.BytesIO(payload), use_threads=False)["geometry"]
    storage = []
    for arrow_value in column.to_pylist():
        if isinstance(arrow_value, dict):
            storage.append({k: scalar(v) for k, v in arrow_value.items()})
        else:
            storage.append(arrow_value.hex() if isinstance(arrow_value, bytes) else arrow_value)
    record = {
        "utc": utc(), "pid": os.getpid(), "source_bytes_sha256": digest(payload), "reader": reader,
        "storage_type": str(column.type), "storage": storage,
        "arrow_validity": column.is_valid().to_pylist(),
        "expected": [geometry_record(x) for x in baseline.geometry],
    }
    try:
        frame = gpd.read_parquet(io.BytesIO(payload))
    except ValueError as exc:
        dump(record | {"exception": {"type": type(exc).__name__, "message": str(exc)}})
        return 20
    rows = [geometry_record(x) for x in frame.geometry]
    dump(record | {
        "ids": list(frame["feature_id"]), "observed": rows, "CRS": crs_summary(frame.crs),
        "state_and_coordinates_equal": rows == record["expected"],
    })
    return 0


def axes():
    from pyproj import Transformer

    xy = (117, 23)
    dump({
        "utc": utc(),
        "comparison": crs_comparison("OGC:CRS84", "EPSG:4326", [xy]),
        "authority_order_4326": [scalar(v) for v in Transformer.from_crs(
            "EPSG:4326", "EPSG:3857", always_xy=False
        ).transform(*xy)],
        "authority_order_CRS84": [scalar(v) for v in Transformer.from_crs(
            "OGC:CRS84", "EPSG:3857", always_xy=False
        ).transform(*xy)],
    })


def invoke(lab, role, *args):
    command = [str(lab / f"venv-{role}/bin/python"), "-B", str(Path(__file__).resolve()),
               *map(str, args)]
    result = subprocess.run(command, text=True, capture_output=True)
    output = json.loads(result.stdout) if result.stdout.strip() else None
    return {"command": command, "exit": result.returncode, "stdout": output,
            "stderr": result.stderr}


def replay(lab, work, output):
    log = output / "evidence/auxiliary"
    fixtures = output / "fixtures/auxiliary"
    log.mkdir(parents=True, exist_ok=True)
    fixtures.mkdir(parents=True, exist_ok=True)
    with (work / "files.csv").open() as stream:
        rows = {row["file_id"]: row for row in csv.DictReader(stream)}
    f4 = work / rows["F4"]["file"]
    build_log = invoke(lab, "N", "build", lab / "src-N", work / "fixtures", fixtures)
    if build_log["exit"]:
        dump(build_log)
        return 1
    built = build_log["stdout"]
    results = {"build": build_log, "A-pyarrow": invoke(lab, "N", "arrow", f4, rows["F4"]["file_sha256"])}
    for file_name in MAIN_CONTROLS:
        results[file_name] = [
            read_one(lab, file_name, fixtures / f"{file_name}.parquet",
                     built[file_name]["sha256"], role, 1, log)
            for role in ("O", "N")
        ]
    for file_name in POINT_FILES:
        results[file_name] = [
            invoke(lab, role, "points", role, lab / f"src-{role}",
                   fixtures / f"{file_name}.parquet", built[file_name]["sha256"])
            for role in ("O", "N")
        ]
    results["D-axis-comparison"] = invoke(lab, "N", "axes")
    for name, record in results.items():
        (log / f"{name}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        )
    dump(list(results))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    run = actions.add_parser("run")
    run.add_argument("lab", type=Path)
    run.add_argument("work", type=Path)
    run.add_argument("output", type=Path)
    writer = actions.add_parser("build")
    writer.add_argument("source", type=Path)
    writer.add_argument("fixtures", type=Path)
    writer.add_argument("output", type=Path)
    plain = actions.add_parser("arrow")
    plain.add_argument("file", type=Path)
    plain.add_argument("sha256")
    reader = actions.add_parser("points")
    reader.add_argument("role", choices=("O", "N"))
    reader.add_argument("source", type=Path)
    reader.add_argument("file", type=Path)
    reader.add_argument("sha256")
    actions.add_parser("axes")
    args = parser.parse_args()
    if args.action == "run":
        return replay(args.lab.resolve(), args.work.resolve(), args.output.resolve())
    if args.action == "build":
        build(args.source, args.fixtures, args.output)
    elif args.action == "arrow":
        pyarrow_read(args.file, args.sha256)
    elif args.action == "points":
        return read_points(args.role, args.source, args.file, args.sha256)
    else:
        axes()
    return 0


if __name__ == "__main__":
    sys.exit(main())
