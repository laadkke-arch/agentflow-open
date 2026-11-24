#!/usr/bin/env python3
"""Recover selected-quad connections from complete public contour receipts."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from run import ENGINE_NAMES, INPUTS, ROOT, canonical, control_jobs, fingerprint, job_for, sha256

EPS = 1e-12
SIDES = ("N", "E", "S", "W")
SHORTHAND = {
    frozenset(("N–W", "E–S")): "A",
    frozenset(("N–E", "S–W")): "B",
    frozenset(("E–W",)): "C",
}


def same_point(a, b):
    return all(abs(x - y) <= EPS for x, y in zip(a, b))


def side_labels(point):
    u, v = point
    boundaries = (v, u - 1, v - 1, u)
    return tuple(side for side, distance in zip(SIDES, boundaries) if abs(distance) <= EPS)


def snap(value):
    if abs(value) <= EPS:
        return 0.0
    if abs(value - 1) <= EPS:
        return 1.0
    return value


def clip_segment(a, b):
    """Intersect the segment's parameter interval with both coordinate slabs."""
    lower, upper = 0.0, 1.0
    delta = tuple(end - start for start, end in zip(a, b))
    for origin, change in zip(a, delta):
        if abs(change) <= EPS:
            if origin < -EPS or origin > 1 + EPS:
                return None
            continue
        entry, leave = sorted((-origin / change, (1 - origin) / change))
        lower, upper = max(lower, entry), min(upper, leave)
        if lower > upper + EPS:
            return None
    return tuple(tuple(snap(origin + t * change) for origin, change in zip(a, delta))
                 for t in (lower, upper))


def polyline_parts(vertices, line_index):
    """Only join consecutive pieces across an interior vertex of this polyline."""
    inside, boundary, touches = [], [], []
    current = None
    for segment_index, (a, b) in enumerate(zip(vertices, vertices[1:])):
        clipped = clip_segment(a, b)
        if clipped is None:
            current = None
            continue
        start, end = clipped
        shared_sides = set(side_labels(start)).intersection(side_labels(end))
        if same_point(start, end):
            touches.append({"line": line_index, "segments": [segment_index], "uv": [start]})
            if side_labels(start):
                current = None
            continue
        if shared_sides:
            boundary.append({"line": line_index, "segments": [segment_index], "uv": [start, end]})
            current = None
            continue
        if current and not side_labels(start) and same_point(current["uv"][-1], start):
            current["segments"].append(segment_index)
            current["uv"].append(end)
        else:
            current = {"line": line_index, "segments": [segment_index], "uv": [start, end]}
            inside.append(current)
    if len(inside) >= 2 and same_point(vertices[0], vertices[-1]):
        first, last = inside[0], inside[-1]
        if (first["segments"][0] == 0 and last["segments"][-1] == len(vertices) - 2
                and not side_labels(first["uv"][0]) and same_point(first["uv"][0], last["uv"][-1])):
            last["segments"].extend(first["segments"])
            last["uv"].extend(first["uv"][1:])
            inside.pop(0)
    return inside, boundary, touches


def unique_parts(parts):
    """Aggregate repeated/reversed copies of a path, preserving every source index."""
    unique = {}
    for part in parts:
        vertices = tuple(tuple(round(x, 12) for x in p) for p in part["uv"])
        key = min(vertices, vertices[::-1])
        if key in unique:
            unique[key]["duplicate_sources"].append({
                "line": part["line"], "segments": part["segments"], "uv": part["uv"],
            })
        else:
            unique[key] = {**part, "duplicate_sources": []}
    return list(unique.values())


def geometry(raw_lines, coordinate_order, quad_rc):
    r0, c0 = quad_rc
    inside, boundary, touches = [], [], []
    for i, line in enumerate(raw_lines):
        if coordinate_order == ["row", "column"]:
            vertices = [(c - c0, r - r0) for r, c in line]
        elif coordinate_order == ["x", "y"]:
            vertices = [(x - c0, y - r0) for x, y in line]
        else:
            raise ValueError(f"Unsupported coordinate order {coordinate_order}")
        parts, edges, points = polyline_parts(vertices, i)
        inside.extend(parts)
        boundary.extend(edges)
        touches.extend(points)
    pairs, path_labels = set(), []
    inside = unique_parts(inside)
    for part in inside:
        start, end = [side_labels(point) for point in (part["uv"][0], part["uv"][-1])]
        path_labels.append(f"{'/'.join(start) or '내부'}→{'/'.join(end) or '내부'}")
        if len(start) == len(end) == 1 and start != end:
            pairs.add("–".join(sorted((start[0], end[0]), key=SIDES.index)))
        part["side_endpoints"] = [start, end]
    for part in boundary:
        start, end = map(side_labels, part["uv"])
        part["shared_sides"] = sorted(set(start).intersection(end), key=SIDES.index)
    boundary, touches = unique_parts(boundary), unique_parts(touches)
    incomplete_paths = len(inside) - sum(
        len(a) == len(b) == 1 and a != b for a, b in (part["side_endpoints"] for part in inside)
    )
    if inside and incomplete_paths:
        label = " / ".join(path_labels)
    elif pairs:
        label = SHORTHAND.get(frozenset(pairs), " + ".join(sorted(pairs)))
    elif boundary:
        label = "경계만"
    elif touches:
        label = "한 점"
    else:
        label = "범위 밖" if raw_lines else "0"
    return {"pair_code": label, "edge_pairs": sorted(pairs), "directed_paths": path_labels,
            "through": inside, "boundary_only": boundary, "point_contacts": touches}


def read_receipt(path, expected_job=None):
    record = json.loads(path.read_text())
    assert sha256(record["stdout"].encode("utf-8")) == record["stdout_sha256"], path
    assert sha256(record["stderr"].encode("utf-8")) == record["stderr_sha256"], path
    assert record["exit_code"] == 0 and not record["timeout"], path
    payload = json.loads(record["stdout"])
    assert record["job"] == payload["job"] and record["pid"] == payload["pid"], path
    if expected_job is not None:
        assert record["job"] == expected_job, path
    assert fingerprint(record["job"]["spec"]) == record["job"]["input_sha256"], path
    return record, payload


def coordinate_arrays(payload):
    raw_return = payload["return"]
    if payload["effective_options"].get("line_type") == "SeparateCode":
        raw_return = raw_return["items"][0]
    assert raw_return["type"] == "list"
    arrays = raw_return["items"]
    for array in arrays:
        assert array["dtype"] == "float64" and array["shape"][1] == 2
    return arrays


def array_values(encoded):
    if isinstance(encoded, dict):
        if encoded["type"] != "list":
            raise ValueError(f"Unexpected ndarray value container {encoded['type']}")
        return [array_values(item) for item in encoded["items"]]
    return encoded


def result_row(path, record, payload, root=ROOT):
    job = record["job"]
    arrays = coordinate_arrays(payload)
    raw_lines = [array_values(array["values"]) for array in arrays]
    normalized = geometry(raw_lines, payload["raw_coordinate_order"], job["spec"]["quad_rc"])
    return {
        "run_id": job["id"], "case": job["case"], "engine": job["engine"],
        "repeat": job["repeat"], "version": payload["engine_version"],
        "input_sha256": job["input_sha256"], "api_input_sha256": job["api_input_sha256"],
        "input_c_order_sha256": payload["input_c_order_sha256"],
        "shape_rc": canonical(payload["input_shape"]), "dtype": payload["input_dtype"],
        "level": job["spec"]["level"], "quad_rc": canonical(job["spec"]["quad_rc"]),
        "kwargs_passed": canonical(job["kwargs_passed"]),
        "effective_options": canonical(payload["effective_options"]),
        "raw_order": "/".join(payload["raw_coordinate_order"]),
        "return_shapes": canonical([array["shape"] for array in arrays]),
        "raw_polylines": canonical(raw_lines),
        "raw_geometry": normalized["pair_code"],
        "edge_pairs": " + ".join(normalized["edge_pairs"]),
        "directed_paths": " + ".join(normalized["directed_paths"]),
        "through_uv": canonical(normalized["through"]),
        "boundary_only_uv": canonical(normalized["boundary_only"]),
        "point_contacts_uv": canonical(normalized["point_contacts"]),
        "raw_polylines_count": len(arrays),
        "coordinate_vertices_count": sum(array["shape"][0] for array in arrays),
        "exit_code": record["exit_code"], "pid": record["pid"],
        "receipt": path.relative_to(root).as_posix(), "stdout_sha256": record["stdout_sha256"],
    }


def predictions():
    with (ROOT / "baseline/predictions.csv").open(newline="") as file:
        stages = {(row["id"], row["stage"]): row for row in csv.DictReader(file)}
    with (ROOT / "baseline/I_FREEZE.csv").open(newline="") as file:
        frozen_i = {row["case_id"]: row for row in csv.DictReader(file)}
    return stages, frozen_i


def primary_rows():
    stages, frozen_i = predictions()
    pids = set()
    repeat_returns = {}
    for case, case_record in INPUTS["primary"].items():
        for engine in ENGINE_NAMES:
            for repeat in (1, 2):
                job = job_for(case, engine, repeat)
                path = ROOT / "receipts/primary" / f"{job['id']}.json"
                record, payload = read_receipt(path, job)
                assert record["pid"] not in pids, path
                pids.add(record["pid"])
                assert payload["job"]["input_sha256"] == case_record["sha256"]
                previous = repeat_returns.setdefault((case, engine), payload["return"])
                assert previous == payload["return"], path
                row = result_row(path, record, payload)
                row.update({stage: stages[case, stage][f"{engine}_pair"] for stage in ("M", "P", "I", "E")})
                row["I_frozen_pre_test"] = frozen_i[case][f"{engine}_pairs"]
                row["exposure"] = stages[case, "I"]["exposure"]
                row["P_bilinear"] = stages[case, "P"]["bilinear_pair"]
                row["E_evidence"] = stages[case, "E"]["source"]
                row["product_match"] = "M/P/I 일치" if all(row[stage] == row["raw_geometry"]
                                                       for stage in ("M", "P", "I")) else "불일치"
                if row["E"] != "미확인":
                    row["E_match"] = "선택 quad 일치" if row["E"] == row["raw_geometry"] else "불일치"
                else:
                    row["E_match"] = "상대 비교" if (case, engine) == ("R2", "contourpy") else "미확인"
                yield row


CONTROL_NOTES = {
    "C4-nw-minus": "m=-2^-22, Q=-2^-19; bilinear A",
    "C4-nw-plus": "m=+2^-22, Q=+2^-19; bilinear B",
    "C3-transpose": "u/v 교환; N↔W, E↔S; A/B 라벨 보존",
    "C3-flip-lr": "E↔W; A↔B",
    "C3-flip-ud": "N↔S; A↔B",
    "C3-negate": "동일 bilinear zero set A; CP center-기반 기하 B 보존 예상; ski low쪽 변경",
    "C3-mask-nw": "유효 삼각형 NE–SE–SW의 E=4/5, S=3/4; N/W 격자변 보간 제외",
    "C5-mask-nw": "유효 삼각형에서 E=(1,2/3)와 diagonal=(1/3,2/3)",
    "C3-mask-nw-no-corner": "전체 quad 제외",
    "C5-mask-nw-no-corner": "전체 quad 제외",
    "C3-high-connected": "양의 대각 연결 B; bilinear A",
    "corner-exact": "NW=(0,0)은 N/W 공동, S=(.5,1)",
    "side-exact": "y=0 경계만, 구간 길이 1",
}


def control_rows():
    controls = {entry["id"]: entry for entry in INPUTS["register_controls"]}
    for job in control_jobs():
        path = ROOT / "receipts/controls" / f"{job['id']}.json"
        record, payload = read_receipt(path, job)
        key = job["id"].removesuffix(f"-{job['engine']}")
        row = result_row(path, record, payload)
        row.update(control_id=key, change=controls[key]["change"], hand_check=CONTROL_NOTES[key])
        yield row


def write_rows(path, rows):
    rows = list(rows)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{path.name}: {len(rows)} rows")
    print(Counter((row["engine"], row["raw_geometry"]) for row in rows))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("group", choices=("primary", "controls"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    write_rows(args.out, primary_rows() if args.group == "primary" else control_rows())


if __name__ == "__main__":
    main()
