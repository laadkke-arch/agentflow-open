"""Construct the sealed inputs and apply the two row-selection controls."""

import hashlib
import json
import math
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import MultiPoint, Point, box

INPUT = Path(__file__).with_name("inputs.json")
INPUT_SHA256 = "d9303498152bcb6567843204633c33ce5691c0a106578f3de8204576280f5aa8"


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def read_spec():
    payload = INPUT.read_bytes()
    if digest(payload) != INPUT_SHA256:
        raise ValueError("Logical input differs from the sealed fixture")
    return json.loads(payload)


def make_frame(spec, input_id):
    rows = spec["row_order"]
    geometries = spec["inputs"][input_id]["geometry"]
    return gpd.GeoDataFrame(
        {
            "id": pd.Series(rows, dtype=spec["id_dtype"]),
            "score": pd.Series([spec["score_by_id"][row] for row in rows], dtype=spec["score_dtype"]),
            spec["geometry_column"]: [make_geometry(geometries[row]) for row in rows],
        },
        geometry=spec["geometry_column"],
        crs=spec["crs"],
    )


def make_geometry(row):
    coordinates = row["coordinates"]
    if row["type"] is None:
        return None
    if row["type"] == "MultiPoint":
        return MultiPoint(coordinates)
    if row["type"] == "Point":
        return Point(coordinates[0]) if coordinates else Point()
    raise ValueError(f"Unknown fixture geometry type: {row['type']}")


def selections(frame, rectangle):
    geometry = frame.geometry
    eligible = geometry.notna() & geometry.is_valid & ~geometry.is_empty
    masks = {
        "T": eligible & geometry.geom_type.eq("Point"),
        "P": eligible & geometry.intersects(box(*rectangle)),
    }
    return {
        name: [
            {"id": row_id, "score": score_value(score)}
            for row_id, score in frame.loc[mask, ["id", "score"]].sort_values("id").itertuples(index=False)
        ]
        for name, mask in masks.items()
    }


def score_value(score):
    if pd.isna(score):
        return None
    return score.item() if hasattr(score, "item") else score


def json_value(value):
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


def geometry_record(geometry):
    missing = bool(shapely.is_missing(geometry))
    dimension = None if missing else int(shapely.get_coordinate_dimension(geometry))
    coordinates = []
    if not missing:
        parts = geometry.geoms if geometry.geom_type == "MultiPoint" else [geometry]
        for part in parts:
            coordinates.extend(
                [[json_value(value) for value in coordinate] for coordinate in part.coords]
            )
    return {
        "type": None if missing else geometry.geom_type,
        "dimension": dimension,
        "has_z": bool(shapely.has_z(geometry)),
        "coordinates": coordinates,
        "xy": [coordinate[:2] for coordinate in coordinates],
        "z": [coordinate[2] if len(coordinate) == 3 else None for coordinate in coordinates],
        "is_empty": bool(shapely.is_empty(geometry)),
        "is_missing": missing,
        "is_valid": bool(shapely.is_valid(geometry)),
        "wkt": shapely.to_wkt(geometry, rounding_precision=-1),
        "wkb_iso_hex": shapely.to_wkb(geometry, hex=True, byte_order=1, flavor="iso"),
    }
