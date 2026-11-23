"""Record the locked environment and input, then fill the eight writer slots."""

import argparse
import csv
import importlib.metadata as metadata
import io
import json
import os
import platform
import subprocess
import sys
import traceback
import warnings
from datetime import datetime, timezone
from pathlib import Path

import fiona
import geopandas as gpd
import geopandas.io.arrow as geo_io
import geopandas.io._geoarrow as native_io
import pyarrow
import pyogrio
import pyproj
import shapely

from model import INPUT_SHA256, digest, geometry_record, make_frame, read_spec, score_value, selections

GPD_SHA = "d8e14e1be3ecbef6f75a1142f85561ff652ed3d1"
ARROW_SHA256 = "b50fba2f51a0ec5237f57dd30ad7cd290ad1d80b082af28ea1aaf17e5ae15584"
FILES = [
    "file_id", "input", "manual_input_sha256", "input_record_sha256",
    "input_record", "writer_commit", "requested_encoding", "status", "geo_version",
    "encoding", "geometry_types", "geo_footer_sha256", "output_sha256",
    "bytes", "artifact", "writer_receipt", "footer_receipt", "reader_ready", "exception",
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def dump(path, data):
    with path.open("x", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, allow_nan=False, indent=2)
        out.write("\n")


def get_git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args], text=True).strip()


def verify_environment(source, wheels, previous_installation, previous_environment):
    source = source.resolve()
    head = get_git(source, "rev-parse", "HEAD")
    tracked_clean = not get_git(source, "status", "--porcelain", "--untracked-files=no")
    import_path = Path(gpd.__file__).resolve()
    arrow_sha = digest(Path(geo_io.__file__).read_bytes())
    if (
        head != GPD_SHA
        or not tracked_clean
        or import_path != source / "geopandas" / "__init__.py"
        or arrow_sha != ARROW_SHA256
        or gpd.__version__ != "1.0.0"
    ):
        raise ValueError(f"Wrong GeoPandas source identity: {head} {import_path} {arrow_sha}")
    original = json.loads(previous_installation.read_text(encoding="utf-8"))
    expected_wheels = {wheel["name"]: wheel["sha256"] for wheel in original["wheels"]}
    actual_wheels = {path.name: digest(path.read_bytes()) for path in sorted(wheels.glob("*.whl"))}
    if not actual_wheels or actual_wheels != expected_wheels:
        raise ValueError("Wheel names or bytes differ from AF-RES-087")
    previous = json.loads(previous_environment.read_text(encoding="utf-8"))["N"]
    expected_installed = dict(previous["installed"])
    installed = {item.metadata["Name"]: item.version for item in metadata.distributions()}
    if installed != expected_installed:
        raise ValueError(f"Distribution lock differs from AF-RES-087: {installed}")
    resolved = {
        "python": sys.version,
        "pandas": installed["pandas"],
        "numpy": installed["numpy"],
        "pyarrow": pyarrow.__version__,
        "arrow_cpp": pyarrow.cpp_version,
        "shapely": shapely.__version__,
        "GEOS": shapely.geos_version_string,
        "pyproj": pyproj.__version__,
        "PROJ": pyproj.proj_version_str,
        "PROJ_network_enabled": pyproj.network.is_network_enabled(),
        "fiona": fiona.__version__,
        "fiona_GDAL": fiona.__gdal_version__,
        "pyogrio": pyogrio.__version__,
        "pyogrio_GDAL": pyogrio.__gdal_version_string__,
        "geopandas_options": {"io_engine": gpd.options.io_engine, "use_pygeos": gpd.options.use_pygeos},
    }
    equal_to_previous = {key: value == previous[key] for key, value in resolved.items()}
    if not all(equal_to_previous.values()):
        raise ValueError(f"Runtime differs from AF-RES-087: {equal_to_previous}")
    pip = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True, check=True)
    return {
        "observed_utc": utc(),
        "command": [sys.executable, *sys.orig_argv[1:]],
        "pid": os.getpid(),
        "writer_reader": {"commit": head, "version": gpd.__version__, "tracked_source_clean": tracked_clean},
        "checkout": str(source),
        "import_path": str(import_path),
        "arrow_import_path": geo_io.__file__,
        "arrow_source_sha256": arrow_sha,
        "native_source_sha256": digest(Path(native_io.__file__).read_bytes()),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "libc": platform.libc_ver(),
        "PROJ_data": pyproj.datadir.get_data_dir(),
        **resolved,
        "same_as_087_N": equal_to_previous,
        "installed": dict(sorted(installed.items())),
        "wheels": actual_wheels,
        "predecessor_wheel_receipt_sha256": digest(previous_installation.read_bytes()),
        "predecessor_environment_sha256": digest(previous_environment.read_bytes()),
        "pip_check": {"exit": pip.returncode, "stdout": pip.stdout, "stderr": pip.stderr},
    }


def crs_record(crs):
    if crs is None:
        return None
    return {
        "authority": list(crs.to_authority()) if crs.to_authority() else None,
        "axes": [
            {"name": axis.name, "direction": axis.direction, "unit": axis.unit_name}
            for axis in crs.axis_info
        ],
        "wkt": crs.to_wkt(),
    }


def capture_input(frame, spec, input_id):
    expected = spec["inputs"][input_id]
    rows = [
        {"id": row_id, "score": score_value(score), **geometry_record(geometry)}
        for row_id, score, geometry in frame[["id", "score", "geometry"]].itertuples(index=False)
    ]
    for row in rows:
        row_id = row["id"]
        for key, value in expected["geometry"][row_id].items():
            if row[key] != value:
                raise ValueError(f"Original {input_id}/{row_id} {key} differs from the manual truth")
        if (row["is_missing"], row["is_empty"], row["is_valid"]) != (row_id == "N", row_id == "E", row_id != "N"):
            raise ValueError(f"Original mask differs for {input_id}/{row_id}")
        if row["score"] != spec["score_by_id"][row_id]:
            raise ValueError(f"Original score differs for {input_id}/{row_id}")
    queries = selections(frame, spec["rectangle"])
    if queries != {name: expected[name] for name in ("T", "P")}:
        raise ValueError(f"Original selections differ from manual truth: {input_id} {queries}")
    return {
        "input": input_id, "manual_input_sha256": INPUT_SHA256, "rows": rows,
        "selections": queries, "crs": crs_record(frame.crs),
        "dtypes": {col: str(dtype) for col, dtype in frame.dtypes.items()},
        "columns": list(frame.columns), "index": list(frame.index),
        "active_geometry": frame.geometry.name,
    }


def write_slot(out, input_id, encoding, frame, entry, options):
    use_native = encoding == "geoarrow"
    file_id = f"{input_id}-{'native' if use_native else 'WKB'}"
    artifact = f"fixtures/{file_id}.parquet"
    writer_receipt = f"evidence/build/{file_id}-writer.json"
    options = {**options, "geometry_encoding": encoding}
    timing = utc()
    target = io.BytesIO()
    failure = None
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            frame.to_parquet(target, **options)
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()}
    writer = {
        "observed_utc": timing,
        "command": [sys.executable, *sys.orig_argv[1:]],
        "pid": os.getpid(),
        "writer_head": GPD_SHA,
        "file_id": file_id,
        "requested": options,
        "input_record_sha256": entry["input_record_sha256"],
        "output_buffer_bytes": len(target.getvalue()),
        "warnings": [{"category": w.category.__name__, "message": str(w.message)} for w in caught],
        "exception": failure,
    }
    if failure:
        dump(out / writer_receipt, {**writer, "status": "writer_exception", "output_sha256": None})
        return {
            **entry, "file_id": file_id, "requested_encoding": encoding, "status": "writer_exception",
            "artifact": writer_receipt, "writer_receipt": writer_receipt, "reader_ready": False,
            "exception": f"{failure['type']}: {failure['message']}",
        }

    payload = target.getvalue()
    sha256 = digest(payload)
    with (out / artifact).open("xb") as stream:
        stream.write(payload)
    dump(out / writer_receipt, {**writer, "status": "written", "output_sha256": sha256, "artifact": artifact})
    cmd = [sys.executable, "-B", str(Path(__file__).with_name("inspect_parquet.py")), str(out / artifact), sha256]
    observed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    footer_receipt = f"evidence/build/{file_id}-footer.json"
    dump(out / footer_receipt, {
        "command": cmd, "exit": observed.returncode, "stderr": observed.stderr,
        "stdout": json.loads(observed.stdout) if observed.returncode == 0 else observed.stdout,
    })
    written = {
        **entry, "file_id": file_id, "requested_encoding": encoding, "status": "written",
        "output_sha256": sha256, "bytes": len(payload), "artifact": artifact,
        "writer_receipt": writer_receipt, "footer_receipt": footer_receipt, "reader_ready": True,
    }
    if observed.returncode:
        return {**written, "status": "written_footer_failed", "exception": observed.stderr.strip()}
    footer = json.loads(observed.stdout)
    geo = footer["geo"]
    column = geo["columns"][geo["primary_column"]]
    return {
        **written, "geo_version": geo["version"], "encoding": column["encoding"],
        "geometry_types": json.dumps(column["geometry_types"]),
        "geo_footer_sha256": footer["geo_footer_sha256"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("wheels", type=Path)
    parser.add_argument("previous_installation", type=Path)
    parser.add_argument("previous_environment", type=Path)
    args = parser.parse_args()

    out = args.out.resolve()
    (out / "evidence/build").mkdir(parents=True, exist_ok=True)
    (out / "fixtures").mkdir(parents=True, exist_ok=True)
    env = verify_environment(args.source, args.wheels, args.previous_installation, args.previous_environment)
    dump(out / "environments.json", env)
    spec = read_spec()
    records = []
    for input_id in spec["inputs"]:
        frame = make_frame(spec, input_id)
        relative = f"fixtures/{input_id}-original.json"
        dump(out / relative, capture_input(frame, spec, input_id))
        entry = {
            "input": input_id, "manual_input_sha256": INPUT_SHA256, "input_record": relative,
            "input_record_sha256": digest((out / relative).read_bytes()), "writer_commit": GPD_SHA,
        }
        for encoding in spec["encodings"]:
            records.append(write_slot(out, input_id, encoding, frame, entry, spec["writer_options"]))

    with (out / "files.csv").open("x", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FILES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    for record in records:
        print(record["file_id"], record["status"], record.get("encoding", ""), record.get("output_sha256", ""),
              record.get("exception", ""))


if __name__ == "__main__":
    main()
