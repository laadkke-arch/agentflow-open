"""Read only: compare the R1 and R2 receipts and decoded PNGs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

PHASES = ("before_layout", "after_layout_attempt", "after_save")
PX_KEYS = ("axes_bbox_pixels", "figure_bbox_pixels")
UNIT_KEYS = ("xlim", "ylim", "active_position_figure_fraction",
             "original_position_figure_fraction")
UNITS_TOL = 1e-6
PIXELS_TOL = 0.25


def differences(a, b):
    if len(a) != len(b):
        raise ValueError("Geometry fields have different shapes.")
    return [abs(x-y) for x, y in zip(a, b)]


def get_geometry(run, case):
    pixels = []
    limits = []
    for phase in PHASES:
        if phase not in run:
            continue
        state = run[phase]
        if case == "M03":
            pixels.extend(state["text_anchor_display_pixels"])
            limits.extend(state["text_anchor_colorbar_axes_fraction"])
            limits.extend(state["axes_data_coordinates_at_anchor"])
            state = [state["data_axes"], state["colorbar_axes"]]
        for ax in state:
            for key in PX_KEYS:
                pixels.extend(ax[key])
            for key in UNIT_KEYS:
                limits.extend(ax[key])
    if run.get("legend"):
        pixels.extend(run["legend"]["bbox_display_px"])
        for item in run["legend"]["entries"]:
            pixels.extend(item["bbox_display_px"])
    return pixels, limits


def steps(run):
    return [(step["step"], step["ok"], step.get("error_type"), step.get("error"),
             [(warning["category"], warning["message"].strip()) for warning in step["warnings"]])
            for step in run["steps"]]


def label_signature(run):
    legend = run.get("legend")
    if legend:
        return [legend["in_layout"], legend["bbox_outside"],
                [(e["id"], e["bbox_outside"], e["ink_pixels"], e["ink_bbox_top_left_px"])
                 for e in legend["entries"]]]
    png = run.get("png", {})
    return [png.get("agrees_with_transform"), png.get("label_ink_pixels"),
            png.get("label_bbox_top_left_px")]


def read_png(path, receipt):
    payload = path.read_bytes()
    with Image.open(path) as img:
        rgb = np.asarray(img.convert("RGB"))
    return rgb, {
        "file_sha256": hashlib.sha256(payload).hexdigest(),
        "rgb_sha256": hashlib.sha256(rgb.tobytes()).hexdigest(),
        "size_px_wh": list(rgb.shape[1::-1]),
        "matches_receipt": (
            hashlib.sha256(payload).hexdigest() == receipt["file"]["sha256"] and
            hashlib.sha256(rgb.tobytes()).hexdigest() == receipt["decoded_rgb_sha256"]),
    }


def compare(root, left_id, right_id, case):
    ids = [left_id, right_id]
    rows = [json.loads((root / run_id / "observations.json").read_text()) for run_id in ids]
    a, b = rows
    pxa, fa = get_geometry(a, case)
    pxb, fb = get_geometry(b, case)
    same_stage_shape = (len(pxa), len(fa)) == (len(pxb), len(fb))
    px = max(differences(pxa, pxb), default=0.0) if same_stage_shape else None
    frac = max(differences(fa, fb), default=0.0) if same_stage_shape else None
    status_a, status_b = a["status"], b["status"]
    result = {
        "pair_id": left_id[3:],
        "run_ids": ids,
        "status": [status_a, status_b],
        "same_inputs": a.get("input") == b.get("input"),
        "same_stage_geometry_shape": same_stage_shape,
        "max_px_delta": px,
        "max_limits_or_fraction_delta": frac,
        "same_step_types_messages_and_warnings": steps(a) == steps(b),
        "same_label_signature": label_signature(a) == label_signature(b),
        "png": None,
    }
    if status_a == status_b == "saved" and "png" in a and "png" in b:
        (data_a, image_a), (data_b, image_b) = [
            read_png(root / name / "figure.png", row["png"])
            for name, row in zip(ids, rows)]
        count = None if data_a.shape != data_b.shape else int(np.any(data_a != data_b, axis=2).sum())
        result["png"] = {
            "byte_equal": image_a["file_sha256"] == image_b["file_sha256"],
            "rgb_equal": image_a["rgb_sha256"] == image_b["rgb_sha256"],
            "different_pixel_count": count,
            "dimensions_match": image_a["size_px_wh"] == image_b["size_px_wh"],
            "receipts_verified": image_a["matches_receipt"] and image_b["matches_receipt"],
        }
    common = (
        status_a == status_b
        and result["same_inputs"]
        and result["same_step_types_messages_and_warnings"]
        and result["same_label_signature"]
        and same_stage_shape
        and px <= PIXELS_TOL and frac <= UNITS_TOL
        and not any("instrumentation_error" in row for row in rows)
    )
    png = result["png"]
    if common and png and png["receipts_verified"] and png["dimensions_match"]:
        pixel_class = "rgb_identical" if png["rgb_equal"] else "raster_difference"
    elif common and status_a in ("layout_failed", "save_failed"):
        pixel_class = "matching_failure"
    else:
        pixel_class = "unverified_or_difference"
    result["comparison"] = pixel_class
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True)
    args = parser.parse_args()
    with (Path(__file__).resolve().parents[1] / "expected.csv").open(newline="") as stream:
        plans = [row for row in csv.DictReader(stream) if row["repeat"] == "R1"]
    evidence = [compare(args.runs, r["run_id"], "R2"+r["run_id"][2:], r["case"])
                for r in plans]
    print(json.dumps({"pixel_tolerance": PIXELS_TOL,
                      "unit_tolerance": UNITS_TOL, "pairs": evidence}, indent=2))


if __name__ == "__main__":
    main()
