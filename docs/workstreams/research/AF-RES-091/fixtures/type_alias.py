"""Test whether changing which row is Point can yield identical native bytes."""

import argparse
import io
import sys
from pathlib import Path

import geopandas as gpd
from shapely.geometry import MultiPoint, Point

from auxiliary import altered_record, input_for
from build import dump, utc
from model import digest, read_spec
from read_matrix import observe_frame, reader_identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_file", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    identity = reader_identity(args.source)
    spec = read_spec()
    rect = spec["rectangle"]
    original = input_for(spec, "S1", "drop_E")
    alternate = original.copy()
    alternate.loc[alternate["id"].eq("A"), "geometry"] = MultiPoint([(117, 23)])
    alternate.loc[alternate["id"].eq("B"), "geometry"] = Point(2, 7)
    original_record = altered_record(original, "S1-drop-E", rect)
    alternate_record = altered_record(alternate, "S1-drop-E-swap-type", rect)

    options = {**spec["writer_options"], "geometry_encoding": "geoarrow"}
    target = io.BytesIO()
    alternate.to_parquet(target, **options)
    payload = target.getvalue()
    saved = args.baseline_file.read_bytes()
    observations = {}
    for label, bytes_in, record in (
        ("baseline", saved, original_record),
        ("alternate", payload, alternate_record),
    ):
        restored = gpd.read_parquet(io.BytesIO(bytes_in))
        observed, comparison = observe_frame(restored, record, rect)
        observations[label] = {
            "sha256": digest(bytes_in), "original": record,
            "observed": observed, "comparison": comparison,
        }
    out_dir = args.out.parent
    dump(args.out, {
        "observed_utc": utc(), "command": [sys.executable, *sys.orig_argv[1:]],
        "runtime": identity,
        "baseline_path": str(args.baseline_file), "writer_options": options,
        "alternate_edit": {"A": "Point to MultiPoint", "B": "MultiPoint to Point"},
        "same_bytes": payload == saved, **observations,
    })
    if payload != saved:
        with (out_dir / "S1-drop-E-swap-type.parquet").open("xb") as stream:
            stream.write(payload)
    print("Native byte equality:", saved == payload, digest(payload))


if __name__ == "__main__":
    main()
