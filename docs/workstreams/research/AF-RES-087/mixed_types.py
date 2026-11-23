"""Exploratory WKB/native pair for Point and MultiPoint in one column."""
import argparse
import io
import json
import sys
from pathlib import Path

from generate import checked_geopandas, crs_summary, digest, dump, utc, writer_kwargs
from observe import geometry_record

def input_frame(gpd):
    from shapely.geometry import MultiPoint, Point

    return gpd.GeoDataFrame(
        {"feature_id": ["single", "multi"]},
        geometry=[Point(117, 23), MultiPoint([(2, 7), (3, 8)])],
        crs="EPSG:4326",
    )


def writer(source, output):
    gpd, writer = checked_geopandas("N", source)
    frame = input_frame(gpd)
    output.mkdir(parents=True, exist_ok=True)
    outs = {}
    for name, encoding in (("G-WKB", "WKB"), ("G-native", "geoarrow")):
        path = output / f"{name}.parquet"
        kwargs = writer_kwargs("N", "1.1.0", encoding)
        frame.to_parquet(path, **kwargs)
        outs[name] = {"kwargs": kwargs, "sha256": digest(path.read_bytes())}
    dump({"observed_utc": utc(), "command": [sys.executable, *sys.argv], "writer": writer,
          "inputs": [geometry_record(x) for x in frame.geometry], "files": outs})


def reader(role, source, file, sha256):
    import pyarrow.parquet as pq

    gpd, identity = checked_geopandas(role, source)
    expected = input_frame(gpd)
    payload = file.read_bytes()
    assert digest(payload) == sha256
    footer = json.loads(pq.ParquetFile(io.BytesIO(payload)).metadata.metadata[b"geo"])
    record = {"observed_utc": utc(), "command": [sys.executable, *sys.argv],
              "source_bytes_sha256": digest(payload), "reader": identity, "geo": footer,
              "expected": [geometry_record(x) for x in expected.geometry]}
    try:
        actual = gpd.read_parquet(io.BytesIO(payload))
    except ValueError as exc:
        dump(record | {"exception": {"type": type(exc).__name__, "message": str(exc)}})
        return 20
    dump(record | {
        "observed": [geometry_record(x) for x in actual.geometry],
        "ids": list(actual["feature_id"]),
        "crs": crs_summary(actual.crs),
        "topology_equal": [x.equals(y) for x, y in zip(actual.geometry, expected.geometry)],
        "types_equal": list(actual.geom_type) == list(expected.geom_type),
    })
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    write = commands.add_parser("write")
    write.add_argument("source", type=Path)
    write.add_argument("output", type=Path)
    read = commands.add_parser("read")
    read.add_argument("role", choices=("O", "N"))
    read.add_argument("source", type=Path)
    read.add_argument("file", type=Path)
    read.add_argument("sha256")
    args = parser.parse_args()
    if args.action == "write":
        writer(args.source, args.output)
        return 0
    return reader(args.role, args.source, args.file, args.sha256)


if __name__ == "__main__":
    sys.exit(main())
