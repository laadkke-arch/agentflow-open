"""Read one fixed payload and compare two contracts in a fresh reader process."""
import argparse
import io
import math
import os
import sys
import traceback
import warnings
from pathlib import Path

from generate import VERSIONS, checked_geopandas, crs_summary, digest, dump, make_frame, parquet_record
from generate import utc


def scalar(value):
    import pandas as pd

    if value is None or value is pd.NA:
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


def geometry_record(geometry):
    import shapely

    if geometry is None:
        return {"missing": True}
    return {
        "missing": False,
        "empty": bool(geometry.is_empty),
        "type": geometry.geom_type,
        "dimension": int(shapely.get_coordinate_dimension(geometry)),
        "wkt": shapely.to_wkt(geometry, rounding_precision=-1),
        "xy": shapely.get_coordinates(geometry).tolist(),
    }


def crs_comparison(candidate, expected, probes):
    from pyproj import CRS, Transformer

    expected = CRS.from_user_input(expected)
    report = {"observed": crs_summary(candidate), "expected": crs_summary(expected)}
    if candidate is None:
        return report | {"equals": False, "equals_ignore_axis": False, "same_xy": False}
    candidate = CRS.from_user_input(candidate)
    reference = Transformer.from_crs(expected, "EPSG:3857", always_xy=True)
    observed = Transformer.from_crs(candidate, "EPSG:3857", always_xy=True)
    transformed = [{"xy": p, "expected": reference.transform(*p), "observed": observed.transform(*p)}
                   for p in probes]
    same_xy = all(math.isclose(left, right, rel_tol=0, abs_tol=1e-7)
                  for p in transformed for left, right in zip(p["expected"], p["observed"]))
    transformed_safe = [{key: [scalar(item) for item in value] for key, value in p.items()}
                        for p in transformed]
    return report | {
        "equals": candidate.equals(expected),
        "equals_ignore_axis": candidate.equals(expected, ignore_axis_order=True),
        "same_xy": same_xy,
        "always_xy_to_epsg3857": transformed_safe,
    }


def attribute_check(actual, spec, footer):
    import pandas as pd

    fields = {field["name"]: field for field in footer["arrow_fields"]}
    leaves = {col["path"]: col for col in footer["parquet_columns"]}
    observed = {}
    for name in actual.columns[actual.dtypes != "geometry"]:
        series = actual[name]
        dtype = repr(series.dtype) if isinstance(series.dtype, pd.StringDtype) else str(series.dtype)
        observed[name] = {
            "values": [scalar(x) for x in series],
            "pandas": dtype,
            "arrow": fields.get(name, {}).get("type"),
            "parquet_physical": leaves.get(name, {}).get("physical"),
            "parquet_logical": leaves.get(name, {}).get("logical"),
        }
    checks = {}
    for name, expected in spec["attributes"].items():
        current = observed.get(name, {})
        checks[name] = {
            "values": current.get("values") == [row[name] for row in spec["rows"]],
            "pandas": current.get("pandas") == expected["pandas"],
            "arrow": current.get("arrow") == expected["arrow"],
            "parquet_physical": current.get("parquet_physical") == expected["parquet_physical"],
            "parquet_logical": (current.get("parquet_logical") or "").startswith(
                expected["parquet_logical_prefix"]
            ),
        }
    return observed, checks


def compared(actual, gpd, spec, expected, footer):
    import pandas as pd

    columns = list(actual.columns)
    ids = [scalar(x) for x in actual["feature_id"]] if "feature_id" in columns else []
    expected_ids = [row["feature_id"] for row in spec["rows"]]
    same_ids = sorted(ids, key=str) == sorted(expected_ids)
    is_geodataframe = isinstance(actual, gpd.GeoDataFrame)
    active = getattr(actual, "_geometry_column_name", None)
    positions = {value: i for i, value in enumerate(ids)}
    geometry_names = list(actual.columns[actual.dtypes == "geometry"])
    probes = [row["probe"] for row in spec["rows"]]
    geometric = {}
    for name in ("geometry", "probe"):
        if name not in geometry_names:
            geometric[name] = {"present": False, "pass": False}
            continue
        series = actual[name]
        rows = []
        for row_i, key in enumerate(expected_ids):
            baseline = expected[name].iat[row_i]
            seen = series.iat[positions[key]] if key in positions else None
            observed = geometry_record(seen)
            baseline_record = geometry_record(baseline)
            same_coordinates = (
                seen is not None and baseline.normalize().equals_exact(seen.normalize(), 0)
            )
            rows.append({
                "feature_id": key,
                "observed": observed,
                "expected_xy": baseline_record["xy"],
                "same_type_dimension": (
                    observed.get("type"), observed.get("dimension")
                ) == (baseline_record["type"], baseline_record["dimension"]),
                "topologically_equal": seen is not None and baseline.equals(seen),
                "same_normalized_xy": bool(same_coordinates),
            })
        crs = crs_comparison(series.crs, spec["crs"], probes)
        geometric[name] = {
            "present": True, "rows": rows, "crs": crs,
            "pass": crs["equals_ignore_axis"] and crs["same_xy"] and all(
                row["same_type_dimension"] and row["topologically_equal"] and row["same_normalized_xy"]
                for row in rows
            ),
        }
    attrs, attr_checks = attribute_check(actual, spec, footer)
    range_index = isinstance(actual.index, pd.RangeIndex) and actual.index.equals(expected.index)
    schema_checks = {
        "row_count": len(actual) == len(expected),
        "ids_in_order": ids == expected_ids,
        "range_index": range_index,
        "columns_in_order": columns == spec["columns"],
        "existing_columns_in_order": [name for name in columns if name in spec["columns"]] == spec["columns"],
        "attributes_exact": all(all(check.values()) for check in attr_checks.values()),
    }
    strict = all(schema_checks.values())
    added = [name for name in columns if name not in spec["columns"]]
    relaxed = (
        schema_checks["row_count"] and schema_checks["ids_in_order"] and range_index
        and schema_checks["existing_columns_in_order"] and schema_checks["attributes_exact"]
        and all(name in attrs for name in added)
    )
    semantic = (
        is_geodataframe and active == spec["active_geometry"] and same_ids
        and all(obs["pass"] for obs in geometric.values())
    )
    return {
        "frame_type": type(actual).__qualname__,
        "rows": len(actual),
        "feature_ids": ids,
        "index_type": type(actual.index).__name__,
        "index": [scalar(v) for v in actual.index],
        "columns": columns,
        "active_geometry": active,
        "geometry_columns": geometry_names,
        "geometry": geometric,
        "attributes": attrs,
        "attribute_checks": attr_checks,
        "schema_checks": schema_checks,
        "semantic_spatial": semantic,
        "strict_attribute_schema": strict,
        "strict_except_additional_attributes": relaxed,
        "additional_attributes": added,
        "both_contracts": semantic and strict,
    }


def observe(args):
    import numpy
    import pandas
    import pyarrow
    import pyproj
    import shapely

    gpd, reader = checked_geopandas(args.role, args.source)
    spec, baseline = make_frame(gpd)
    payload = args.file.read_bytes()
    input_hash = digest(payload)
    if input_hash != args.sha256:
        raise RuntimeError(f"Input bytes differ from expected SHA-256: {input_hash}")
    footer = parquet_record(payload)
    record = {
        "file_id": args.file_id,
        "role": args.role,
        "repeat": args.repeat,
        "read_utc": utc(),
        "pid": os.getpid(),
        "command": [sys.executable, *sys.argv],
        "source_bytes_sha256": input_hash,
        "expected_file_sha256": args.sha256,
        "reader_argument": "BytesIO of the same hashed payload",
        "input_size_bytes": len(payload),
        "input_geo_version": footer["geo"]["version"],
        "input_encodings": {c: v["encoding"] for c, v in footer["geo"]["columns"].items()},
        "input_physical_schema": footer["parquet_columns"],
        "reader": reader | {
            "python_executable": sys.executable, "python": sys.version.split()[0],
            "pandas": pandas.__version__, "numpy": numpy.__version__,
            "pyarrow": pyarrow.__version__, "shapely": shapely.__version__,
            "GEOS": shapely.geos_version_string, "PROJ": pyproj.proj_version_str,
            "pyproj": pyproj.__version__,
        },
    }
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        try:
            actual = gpd.read_parquet(io.BytesIO(payload))
        except Exception as exc:
            traceback.print_exc()
            explicit_wkb_rejection = (
                args.role == "O" and type(exc) is ValueError
                and str(exc) == "Only WKB geometry encoding is supported"
                and any(v != "WKB" for v in record["input_encodings"].values())
            )
            dump(record | {
                "outcome": "explicit_rejection" if explicit_wkb_rejection else "reader_error",
                "exception": {"type": type(exc).__name__, "message": str(exc)},
                "warnings": [str(w.message) for w in captured],
                "rows": None,
                "semantic_spatial": None,
                "strict_attribute_schema": None,
            })
            return 20 if explicit_wkb_rejection else 21

        result = compared(actual, gpd, spec, baseline, footer)
        dump(record | result | {
            "outcome": "preserved" if result["both_contracts"] else "silent_loss",
            "exception": None,
            "warnings": [str(w.message) for w in captured],
        })
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=VERSIONS)
    parser.add_argument("source", type=Path)
    parser.add_argument("file_id")
    parser.add_argument("file", type=Path)
    parser.add_argument("sha256")
    parser.add_argument("repeat", type=int)
    return observe(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
