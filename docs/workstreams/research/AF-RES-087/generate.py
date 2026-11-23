"""Generate the fixed files and inspect their byte and footer fingerprints."""
import argparse
import hashlib
import importlib.metadata
import inspect
import io
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "manifest.json").read_bytes())["research"]
INPUT = HERE / "fixtures/input.json"
VERSIONS = {"O": "0.14.4", "N": "1.0.0"}


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False))


def checked_geopandas(role, source):
    import geopandas as gpd
    import geopandas.io.arrow as arrow

    source = Path(source).resolve()
    rev = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    tracked_changes = subprocess.check_output(
        ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    )
    if rev != PLAN["geopandas_commits"][role] or tracked_changes:
        raise RuntimeError(f"{role} source checkout differs from the pin: {rev}")
    if not Path(gpd.__file__).resolve().is_relative_to(source):
        raise RuntimeError(f"{role} imported another GeoPandas: {gpd.__file__}")
    if not Path(arrow.__file__).resolve().is_relative_to(source):
        raise RuntimeError(f"{role} imported another Arrow implementation: {arrow.__file__}")
    if gpd.__version__ != VERSIONS[role]:
        raise RuntimeError(f"{role} imported an unexpected version: {gpd.__version__}")
    return gpd, {
        "role": role,
        "checkout": str(source),
        "commit": rev,
        "tracked_source_clean": True,
        "geopandas_version": gpd.__version__,
        "distribution_version": importlib.metadata.version("geopandas"),
        "import_path": str(Path(gpd.__file__).resolve()),
        "arrow_import_path": str(Path(arrow.__file__).resolve()),
        "arrow_source_sha256": digest(Path(arrow.__file__).read_bytes()),
    }


def resolved_environment(role, source):
    import fiona
    import numpy
    import pandas
    import pyarrow
    import pyogrio
    import pyproj
    import shapely

    gpd, fingerprint = checked_geopandas(role, source)
    return fingerprint | {
        "observed_utc": utc(),
        "environment_kind": "reconstructed; no historical resolved publisher lock",
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "libc": platform.libc_ver(),
        "pandas": pandas.__version__,
        "numpy": numpy.__version__,
        "pyarrow": pyarrow.__version__,
        "arrow_cpp": pyarrow.cpp_version,
        "shapely": shapely.__version__,
        "GEOS": shapely.geos_version_string,
        "pyproj": pyproj.__version__,
        "PROJ": pyproj.proj_version_str,
        "PROJ_data": pyproj.datadir.get_data_dir(),
        "PROJ_network_enabled": pyproj.network.is_network_enabled(),
        "fiona": fiona.__version__,
        "fiona_GDAL": fiona.__gdal_version__,
        "pyogrio": pyogrio.__version__,
        "pyogrio_GDAL": pyogrio.__gdal_version_string__,
        "geopandas_options": {
            "io_engine": gpd.options.io_engine,
            "use_pygeos": gpd.options.use_pygeos,
        },
        "installed": sorted(
            (d.metadata["Name"], d.version) for d in importlib.metadata.distributions()
        ),
    }


def make_frame(gpd):
    import pandas as pd
    from shapely.geometry import Point, box

    raw = INPUT.read_bytes()
    if digest(raw) != PLAN["common_input_sha256"]:
        raise RuntimeError("Common input bytes differ from the sealed plan")
    spec = json.loads(raw)
    data = {
        col: pd.Series([row[col] for row in spec["rows"]], dtype=desc["pandas"])
        for col, desc in spec["attributes"].items()
    }
    for col, shape in (("geometry", box), ("probe", Point)):
        data[col] = gpd.GeoSeries(
            [shape(*row[col]) for row in spec["rows"]], crs=spec["crs"]
        )
    frame = gpd.GeoDataFrame(data, geometry=spec["active_geometry"])[spec["columns"]]
    return spec, frame


def crs_summary(value):
    from pyproj import CRS

    if value is None:
        return None
    crs = CRS.from_user_input(value)
    return {
        "authority": crs.to_authority(),
        "name": crs.name,
        "axes": [
            {"name": axis.name, "direction": axis.direction, "unit": axis.unit_name}
            for axis in crs.axis_info
        ],
    }


def normalized_arrow_field(field):
    return {
        "name": field.name,
        "type": str(field.type),
        "nullable": field.nullable,
        "metadata": {
            k.decode(): v.decode() for k, v in (field.metadata or {}).items()
        },
    }


def parquet_record(payload):
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(io.BytesIO(payload))
    file_metadata = pf.metadata.metadata
    geo_bytes = file_metadata[b"geo"]
    geo_metadata = json.loads(geo_bytes)
    footer_size = int.from_bytes(payload[-8:-4], "little")
    return {
        "file_sha256": digest(payload),
        "file_bytes": len(payload),
        "footer_sha256": digest(payload[-8-footer_size:-8]),
        "footer_bytes": footer_size,
        "format_version": pf.metadata.format_version,
        "created_by": pf.metadata.created_by,
        "rows": pf.metadata.num_rows,
        "row_groups": pf.metadata.num_row_groups,
        "geo_json": geo_bytes.decode(),
        "geo": geo_metadata,
        "crs": {
            col: crs_summary(desc.get("crs", "OGC:CRS84"))
            for col, desc in geo_metadata["columns"].items()
        },
        "schema_metadata_sha256": {
            k.decode(): digest(v) for k, v in file_metadata.items()
        },
        "pandas_metadata": json.loads(file_metadata[b"pandas"]) if b"pandas" in file_metadata else None,
        "arrow_fields": [normalized_arrow_field(field) for field in pf.schema_arrow],
        "parquet_columns": [
            {
                "path": column.path,
                "physical": column.physical_type,
                "logical": str(column.logical_type),
                "converted": column.converted_type,
                "definition_level": column.max_definition_level,
                "repetition_level": column.max_repetition_level,
            }
            for column in (pf.schema.column(i) for i in range(len(pf.schema)))
        ],
    }


def writer_kwargs(role, schema_version, encoding):
    kwargs = {
        "index": False,
        "compression": "snappy",
        "version": "2.6",
        "schema_version": schema_version,
    }
    if role == "N":
        kwargs.update(geometry_encoding=encoding, write_covering_bbox=False)
    return kwargs


def generate_file(file_id, source, output):
    config = PLAN["files"][file_id]
    gpd, fingerprint = checked_geopandas(config["writer"], source)
    _, frame = make_frame(gpd)
    kwargs = writer_kwargs(config["writer"], config["schema_version"], config["encoding"])
    record = {
        "file_id": file_id,
        "utc": utc(),
        "command": [sys.executable, *sys.argv],
        "writer": fingerprint,
        "writer_signature": str(inspect.signature(frame.to_parquet)),
        "actual_kwargs": kwargs,
        "input_sha256": PLAN["common_input_sha256"],
        "path": str(output),
    }
    if output.exists():
        raise FileExistsError(f"Generation output already exists: {output}")
    try:
        frame.to_parquet(output, **kwargs)
    except Exception as exc:
        dump(record | {
            "status": "generation_failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "partial_output_exists": output.exists(),
        })
        raise
    payload = output.read_bytes()
    dump(record | {"status": "generated", "file_sha256": digest(payload), "bytes": len(payload)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    env = actions.add_parser("env")
    env.add_argument("role", choices=VERSIONS)
    env.add_argument("source", type=Path)
    write = actions.add_parser("write")
    write.add_argument("file_id", choices=PLAN["files"])
    write.add_argument("source", type=Path)
    write.add_argument("output", type=Path)
    footer = actions.add_parser("footer")
    footer.add_argument("file", type=Path)
    args = parser.parse_args()
    if args.action == "env":
        dump(resolved_environment(args.role, args.source))
    elif args.action == "write":
        generate_file(args.file_id, args.source, args.output)
    else:
        dump({"utc": utc(), "command": [sys.executable, *sys.argv]} |
             parquet_record(args.file.read_bytes()))


if __name__ == "__main__":
    main()
