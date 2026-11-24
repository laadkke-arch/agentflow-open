#!/usr/bin/env python3
"""Verify frozen fixtures, direct C3/C4 endpoint readings, and clean replays."""

import argparse
from collections import Counter
import csv
from fractions import Fraction
import json
from pathlib import Path

from analyze import (array_values, coordinate_arrays, geometry, primary_rows, control_rows,
                     read_receipt)
from run import ENGINE_NAMES, INPUTS, ROOT, fingerprint, job_for, published_jobs


def rows(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def original_fixtures():
    expected = rows(ROOT / "baseline/inputs.csv")
    assert len(expected) == 7
    for row in expected:
        fixture = INPUTS["primary"][row["id"]]
        spec = fixture["spec"]
        if row["id"] == "R1":
            original_grid = [[int(not ((r == 1 and 1 <= c < 7) or (c == 1 and 1 <= r < 7)))
                              for c in range(8)] for r in range(8)]
        else:
            original_grid = json.loads(row["input_grid"])
        assert spec["z"] == original_grid, row["id"]
        assert spec["level"] == float(row["level"]) and spec["quad_rc"] == [0, 0]
        assert spec["dtype"] == ("float32" if row["id"] == "R1" else "float64")
        assert [original_grid[0][0], original_grid[0][1], original_grid[1][1], original_grid[1][0]] == [
            int(row[side]) for side in ("NW", "NE", "SE", "SW")
        ]
        assert fingerprint(spec) == fixture["sha256"]
    return [row["id"] for row in expected]


def manual_unit_cell():
    # Direct endpoint identification using hand-interpolated fractions, with no clipping.
    expected_points = {
        "C3": {"N": (Fraction(2, 3), 0), "E": (1, Fraction(4, 5)),
               "S": (Fraction(3, 4), 1), "W": (0, Fraction(8, 11))},
        "C4": {"N": (Fraction(1, 2), 0), "E": (1, Fraction(1, 2)),
               "S": (Fraction(1, 2), 1), "W": (0, Fraction(1, 2))},
    }
    checks = []
    for case, edges in expected_points.items():
        for engine in ENGINE_NAMES:
            for repeat in (1, 2):
                job = job_for(case, engine, repeat)
                _, payload = read_receipt(ROOT / "receipts/primary" / f"{job['id']}.json", job)
                raw_lines = payload["return"]["items"]
                found, max_residual = [], 0.0
                for line in raw_lines:
                    assert line["shape"] == [2, 2]
                    labels = []
                    for vertex in line["values"]["items"]:
                        p, q = vertex["items"]
                        # The hand calculations use (u,v); scikit-image raw is (v,u).
                        u, v = (q, p) if engine == "skimage" else (p, q)
                        matches = []
                        for side, (u_expected, v_expected) in edges.items():
                            residual = max(abs(u - u_expected), abs(v - v_expected))
                            if residual <= 3e-16:
                                matches.append((side, residual))
                        (side, residual), = matches
                        labels.append(side)
                        max_residual = max(max_residual, residual)
                    found.append("→".join(labels))
                expected = ["N→E", "S→W"] if case == "C3" and engine == "contourpy" else ["N→W", "S→E"]
                assert found == expected, (job["id"], found, expected)
                assert len(raw_lines) == 2
                checks.append({"run_id": job["id"], "directed_endpoint_labels": found,
                               "max_coordinate_residual": max_residual})
    return checks


def check_observed_csv(filename, generated):
    expected = list(generated)
    actual = rows(ROOT / filename)
    assert len(expected) == len(actual)
    for row, observed in zip(expected, actual):
        assert {key: str(value) for key, value in row.items()} == observed, observed["run_id"]
    return len(actual)


def compare_published():
    published = {}
    for job in published_jobs():
        _, payload = read_receipt(ROOT / "receipts/published" / f"{job['id']}.json", job)
        published[job["id"]] = payload
    _, r1_default = read_receipt(ROOT / "receipts/primary/R1-skimage-1.json")
    r1_high = published["R1-original-high"]
    default_points, = [array_values(a["values"]) for a in coordinate_arrays(r1_default)]
    high_points, = [array_values(a["values"]) for a in coordinate_arrays(r1_high)]
    assert default_points == high_points[::-1]
    assert len(default_points) == 25 and default_points[16:18] == [[0.5, 1], [1, 0.5]]
    _, r2_default = read_receipt(ROOT / "receipts/primary/R2-contourpy-1.json")
    r2_separate = published["R2-original-Separate"]
    r2_code = published["R2-original-SeparateCode-to-Offset"]
    assert r2_separate["return"] == r2_default["return"] == r2_code["return"]["items"][0]
    assert r2_code["relative_comparison"]["equal_recursive"]
    return {"r1_default_vs_original_reverse_exact": True,
            "r1_points_including_closure": len(default_points), "r1_selected_raw_default": default_points[16:18],
            "r2_Separate_and_SeparateCode_and_default_point_arrays_identical": True,
            "r2_relative_same_generator_Offset_comparison": True}


def other_r2_quads():
    outputs = {}
    for engine in ENGINE_NAMES:
        _, payload = read_receipt(ROOT / "receipts/primary" / f"R2-{engine}-1.json")
        lines = [array_values(array["values"]) for array in coordinate_arrays(payload)]
        outputs[engine] = lines, payload["raw_coordinate_order"]
    z = INPUTS["primary"]["R2"]["spec"]["z"]
    differences = []
    for row in range(len(z) - 1):
        for col in range(len(z[0]) - 1):
            selected = {key: geometry(*value, (row, col)) for key, value in outputs.items()}
            if selected["skimage"]["edge_pairs"] != selected["contourpy"]["edge_pairs"]:
                differences.append({"quad_rc": [row, col], "z": [line[col:col+2] for line in z[row:row+2]],
                                    **selected})
    assert [item["quad_rc"] for item in differences] == [[1, 1]]
    assert (differences[0]["skimage"]["pair_code"], differences[0]["contourpy"]["pair_code"]) == ("B", "A")
    return differences


def clipping_examples():
    cases = [
        ("clip-through-interior-vertex", [[[-1, 0.5], [0.5, 0.5], [2, 0.5]]], "C", [1, 0, 0]),
        ("duplicate-through-reversed", [[[0, 0.5], [1, 0.5]], [[1, 0.5], [0, 0.5]]], "C", [1, 0, 0]),
        ("duplicate-on-one-edge", [[[0, 0], [1, 0]], [[1, 0], [0, 0]]], "경계만", [0, 1, 0]),
        ("tangent-point-only", [[[-0.5, 0.5], [0.5, -0.5]]], "한 점", [0, 0, 1]),
        ("corner-incidence-no-unique-edge", [[[0, 0], [0.5, 1]]], "N/W→S", [1, 0, 0]),
        ("outside", [[[-1, -0.5], [2, -0.5]]], "범위 밖", [0, 0, 0]),
    ]
    verified = []
    for name, lines, label, counts in cases:
        actual = geometry(lines, ["x", "y"], (0, 0))
        assert actual["pair_code"] == label
        assert [len(actual[key]) for key in ("through", "boundary_only", "point_contacts")] == counts
        if name == "duplicate-on-one-edge":
            assert len(actual["boundary_only"][0]["duplicate_sources"]) == 1 and not actual["edge_pairs"]
        elif name == "duplicate-through-reversed":
            assert len(actual["through"][0]["duplicate_sources"]) == 1
        verified.append({"name": name, "input_xy": lines, "observed": actual})
    return verified


def component_counts():
    outcomes = {}
    for case in ("C4", "C5"):
        read = ROOT / "receipts/domain" / f"{case}-scipy-label4and8.json"
        _, payload = read_receipt(read)
        outcomes[case] = [item["items"][1] for item in payload["return"]["items"]]
    assert outcomes == {"C4": [2, 1], "C5": [1, 1]}
    return outcomes


def ledger_counts():
    entries = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text().splitlines()]
    success = [x for x in entries if x["access_result"] == "직접 열람 성공"]
    included = [x for x in entries if x["counted"]]
    assert len({x["source_id"] for x in entries}) == len(entries)
    assert len({x["work_id"] for x in included}) == len(included) >= 22
    counts = Counter(row["group"] for row in included)
    for key, minimum in {"221": 3, "scikit-image": 5, "ContourPy": 5, "안장점 원연구": 4,
                         "지형·영상·다른 분야": 5}.items():
        assert counts[key] >= minimum
    return {"entries": len(entries), "success_rows": len(success),
            "opened_distinct_works": len({x["work_id"] for x in success}), "counted_unique_works": len(included),
            "counted_lineages": len({x["lineage_id"] for x in included}), "group_counts": counts}


def replay(directory):
    env = json.loads((directory / "environment.json").read_text())
    initial = json.loads((ROOT / "environment.json").read_text())
    assert env["runtime_fingerprint_sha256"] == initial["runtime_fingerprint_sha256"]
    assert not env["system_site_packages_enabled"] and env["prefix"] != initial["prefix"]
    results = []
    for case in ("C3", "C4", "R1", "R2"):
        for engine in ENGINE_NAMES:
            job = job_for(case, engine, 1)
            path = directory / f"{job['id']}.json"
            receipt, actual = read_receipt(path, job)
            _, expected = read_receipt(ROOT / "receipts/primary" / path.name, job)
            for key in ("return", "effective_options", "input_c_order_sha256", "raw_coordinate_order"):
                assert actual[key] == expected[key], (path, key)
            results.append({"run_id": job["id"], "pid": receipt["pid"], "exit_code": receipt["exit_code"],
                            "ordered_typed_return_sha256": fingerprint(actual["return"])})
    assert len({result["pid"] for result in results}) == 8
    return {"environment_sha256": env["runtime_fingerprint_sha256"], "matching_runs": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-dir", type=Path)
    args = parser.parse_args()
    result = {
        "frozen_fixtures": original_fixtures(),
        "primary_rows_verified": check_observed_csv("observed.csv", primary_rows()),
        "control_rows_verified": check_observed_csv("controls.csv", control_rows()),
        "manual_C3_C4": manual_unit_cell(),
        "published_comparison": compare_published(),
        "r2_all_36_quads_differences": other_r2_quads(),
        "normalizer_cases": clipping_examples(),
        "scipy_4_and_8_neighbor_components": component_counts(),
        "ledger": ledger_counts(),
    }
    if args.replay_dir:
        result["clean_replay"] = replay(args.replay_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
