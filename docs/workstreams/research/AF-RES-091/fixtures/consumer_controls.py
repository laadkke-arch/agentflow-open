"""Reapply the two public call patterns to selected synthetic GeoParquet bytes."""

import argparse
import importlib.metadata
import io
import json
from pathlib import Path

import dask_geopandas as dg
import dask_geopandas.expr as expr
import geopandas as gpd

from build import dump, utc
from model import digest, read_spec, score_value


def row_values(frame):
    return [
        {"id": row_id, "score": score_value(score)}
        for row_id, score in frame[["id", "score"]].sort_values("id").itertuples(index=False)
    ]


def exact_type_notebook(frame):
    return row_values(frame[frame["geometry"].apply(lambda value: value.geom_type == "Point")])


def reproduce(frame, rect):
    xmin, ymin, xmax, ymax = rect
    distributed = dg.from_geopandas(frame, npartitions=2)
    distributed.calculate_spatial_partitions()
    try:
        raw_types = {"output": exact_type_notebook(frame)}
    except AttributeError as exc:
        raw_types = {"error": type(exc).__name__, "message": str(exc)}
    have_geometry = frame.geometry.notna()
    return {
        "Dask_cx": row_values(distributed.cx[xmin:xmax, ymin:ymax].compute(scheduler="synchronous")),
        "spatial_partitions": [geometry.wkt for geometry in distributed.spatial_partitions],
        "notebook_unmodified": raw_types,
        "notebook_missing_removed": exact_type_notebook(frame[have_geometry]),
        "notebook_study_guard": exact_type_notebook(
            frame[have_geometry & frame.geometry.is_valid & ~frame.geometry.is_empty]
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("dask_source", type=Path)
    args = parser.parse_args()
    package_expr = Path(expr.__file__).read_bytes()
    pinned_expr = (args.dask_source / "dask_geopandas/expr.py").read_bytes()
    if package_expr != pinned_expr or dg.__version__ != "0.5.0":
        raise ValueError("Dask-GeoPandas expr.py differs from the audited v0.5.0 source")

    files = {
        "fixtures/S0-WKB.parquet": "7dd2a078997039bb5cc97066446f93e21819d73d3f73191d8bee2ae055b7e30f",
        "fixtures/S0-native.parquet": "9dcc45e8fe3313265336484882ad64e5762eedbd267cfb7a86d69a177fc39911",
        "evidence/auxiliary/S1-drop-E.parquet": "8174134afb03872bd4495a9fb4507c2ae3c92b1f52cd673c9e9298db31669aaa",
    }
    results = {}
    for name, sha256 in files.items():
        payload = (args.root / name).read_bytes()
        if digest(payload) != sha256:
            raise ValueError(f"File SHA does not match: {name}")
        results[name] = {
            "sha256": sha256,
            **reproduce(gpd.read_parquet(io.BytesIO(payload)), read_spec()["rectangle"]),
        }

    dump(args.out, {
        "observed_utc": utc(), "scope": "downstream call patterns on AF-RES-091 fixtures",
        "dask_geopandas_commit": "90c0734199e1c678318d66b2e7ee69a5edb4895c",
        "dask_geopandas_expr_sha256": digest(package_expr),
        "original_notebook_commit": "dd68ad89f88d28bee301e235a4af3bb95fe225ad",
        "versions": {name: importlib.metadata.version(name) for name in (
            "dask", "dask-geopandas", "geopandas", "pandas", "shapely", "pyarrow",
            "cloudpickle", "fsspec", "partd", "pyyaml", "toolz", "locket",
        )},
        "results": results,
    })
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
