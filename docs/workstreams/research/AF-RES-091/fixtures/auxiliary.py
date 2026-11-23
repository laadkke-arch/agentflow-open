"""Diagnose Point EMPTY offsets and dimension padding outside the sealed grid."""

import argparse
import io
import json
import os
import subprocess
import sys
import traceback
import warnings
from pathlib import Path

import geopandas as gpd
import shapely
from shapely.geometry import MultiPoint

from build import crs_record, dump, utc
from model import INPUT_SHA256, digest, geometry_record, json_value, make_frame, read_spec, score_value, selections
from read_matrix import observe_frame, reader_identity

CASES = {
    "S1-drop-E": ("S1", "drop_E"),
    "S1-drop-N": ("S1", "drop_N"),
    "S1-empty-MultiPoint": ("S1", "replace_E"),
    "S2-drop-E": ("S2", "drop_E"),
    "S3-drop-E": ("S3", "drop_E"),
}


def ragged(frame):
    geometry = frame.geometry.to_numpy()
    parts, part_ids = shapely.get_parts(geometry, return_index=True)
    _, coord_ids = shapely.get_coordinates(geometry, return_index=True)
    geom_type, xy_or_xyz, offsets = shapely.to_ragged_array(geometry)
    return {
        "row_ids": list(frame["id"]),
        "missing_mask": shapely.is_missing(geometry).tolist(),
        "parts": [part.wkt for part in parts],
        "part_indices": part_ids.tolist(),
        "coordinate_row_indices": coord_ids.tolist(),
        "array_type": geom_type.name,
        "coords": [[json_value(value) for value in row] for row in xy_or_xyz.tolist()],
        "offsets": [array.tolist() for array in offsets],
        "dimension": xy_or_xyz.shape[1],
        "offsets_reach_coordinates": not offsets or int(offsets[-1][-1]) == len(xy_or_xyz),
    }


def input_for(spec, input_id, edit):
    frame = make_frame(spec, input_id)
    if edit == "replace_E":
        frame.loc[frame["id"].eq("E"), "geometry"] = MultiPoint([])
        return frame
    return frame.loc[frame["id"].ne(edit[-1])].reset_index(drop=True)


def altered_record(frame, input_id, rect):
    return {
        "input": input_id, "manual_input_sha256": INPUT_SHA256,
        "rows": [
            {"id": row_id, "score": score_value(score), **geometry_record(geometry)}
            for row_id, score, geometry in frame[["id", "score", "geometry"]].itertuples(index=False)
        ],
        "selections": selections(frame, rect), "crs": crs_record(frame.crs),
        "dtypes": {col: str(dtype) for col, dtype in frame.dtypes.items()},
        "columns": list(frame.columns), "index": list(frame.index),
        "active_geometry": frame.geometry.name,
    }


def contrast(out, spec, name, input_id, edit):
    rect = spec["rectangle"]
    frame = input_for(spec, input_id, edit)
    buffer = io.BytesIO()
    options = {**spec["writer_options"], "geometry_encoding": "geoarrow"}
    result = {
        "case": name, "base_input": input_id, "edit": edit, "writer_options": options,
        "original": altered_record(frame, input_id, rect), "ragged": ragged(frame),
    }
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            frame.to_parquet(buffer, **options)
        except Exception as exc:
            return result | {
                "write_status": "writer_exception", "buffer_bytes": len(buffer.getvalue()),
                "exception": {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()},
                "warnings": [str(item.message) for item in caught],
            }
    payload = buffer.getvalue()
    sha256 = digest(payload)
    artifact = f"{name}.parquet"
    with (out / artifact).open("xb") as stream:
        stream.write(payload)
    inspect_script = Path(__file__).with_name("inspect_parquet.py")
    command = [sys.executable, "-B", str(inspect_script), str(out / artifact), sha256]
    proc = subprocess.run(command, capture_output=True, text=True, check=True)
    restored = gpd.read_parquet(io.BytesIO(payload))
    observed, comparison = observe_frame(restored, result["original"], rect)
    return result | {
        "write_status": "written", "buffer_bytes": len(payload), "sha256": sha256,
        "bytes_path": artifact, "warnings": [str(item.message) for item in caught],
        "footer": {"exit": proc.returncode, "stdout": json.loads(proc.stdout), "stderr": proc.stderr},
        "read": {"observed": observed, "comparison": comparison},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    spec = read_spec()
    identity = reader_identity(args.source)
    dump(out / "original-ragged.json", {
        "observed_utc": utc(), "command": [sys.executable, *sys.orig_argv[1:]], "pid": os.getpid(),
        "runtime": identity, "original_inputs": {key: ragged(make_frame(spec, key)) for key in spec["inputs"]},
    })
    for name, (input_id, edit) in CASES.items():
        result = contrast(out, spec, name, input_id, edit)
        dump(out / f"{name}.json", {
            "observed_utc": utc(), "command": [sys.executable, *sys.orig_argv[1:]], "pid": os.getpid(),
            "runtime": identity, **result,
        })
        print(name, result["write_status"], result.get("sha256", ""), result["ragged"]["offsets"])


if __name__ == "__main__":
    main()
