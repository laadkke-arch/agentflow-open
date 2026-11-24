"""Recompute selection, hit and preservation from AF-RES-123 browser receipts."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FALLBACK = {"original": "lightgray", "local": "steelblue", "shared": "lightgray"}
OBSERVED_FIELDS = {"visual", "projected", "dataExtent", "tupleStore", "fills", "unit", "brush"}
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
HIT_NAMES = {"marks": "mark", "root": "plot", "drag_brush_brush": "brush",
             "drag_brush_brush_bg": "brush-back"}


def read(path: Path):
    return json.loads(path.read_bytes())


def encode(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def month_labels(values):
    if values is None:
        return None
    return [MONTHS[datetime.fromtimestamp(value / 1000, timezone.utc).month - 1] for value in values]


def project(visual, bands):
    if visual is None or len(visual) != 2 or visual[0] == visual[1]:
        return None
    lo, hi = sorted(visual)
    return [band["value"] for band in bands
            if lo <= band["end"] + 1e-10 and band["start"] <= hi] or None


def mask_expected(state, scale, fallback):
    selected = None if state["projected"] is None else set(state["projected"])
    expected = {}
    for key in state["fills"]:
        month, weather = key.split(":", 1)
        expected[key] = scale["colors"][weather] if selected is None or int(month) in selected else fallback
    return expected


def expected_extent(mode, seed, start, x, width):
    if mode == "new":
        return [start, max(0, min(width, x))]
    offset = max(-min(seed), min(width - max(seed), x - start))
    return [edge + offset for edge in seed]


def residual(observed, expected):
    if observed is None or expected is None or len(observed) != len(expected):
        return None
    return max(abs(a - b) for a, b in zip(observed, expected, strict=True))


def event_hit(event):
    if event is None:
        return None
    item = event["item"]
    if item is None:
        return "none"
    mark = item["mark"]
    return HIT_NAMES.get(mark["name"], mark["name"] or mark["role"])


def close_step(raw, phase, label):
    return next((snap for snap in raw["snapshots"] if snap["phase"] == phase and snap["step"] == label), None)


def state_at(raw, phase, label):
    snap = close_step(raw, phase, label)
    return snap["first"] if snap else None


def native_sequence(raw, phase):
    return [event for event in raw["events"] if event["phase"] == phase and event["channel"] == "dom"
            and event["type"] in {"mousedown", "mousemove", "mouseup"}
            and event["step"] not in {"reset", "hover"}]


def evidence_status(raw, scenario, gesture, native):
    if raw["status"] != "executed":
        return raw["status"]
    if not scenario["observers"]:
        return "executed_without_observers"
    expected = ["mousedown"] + ["mousemove"] * len(gesture["moves"]) + ["mouseup"]
    if [event["type"] for event in native] != expected:
        return "input_trace_mismatch"
    if any(not event["trusted"] or event["button"] != 0 for event in native
           if event["type"] in {"mousedown", "mouseup"}):
        return "input_trace_mismatch"
    if not all(event["trusted"] and event["buttons"] == 1 for event in native[:-1]):
        return "input_trace_mismatch"
    return "observed"


def observed_step(state, expected, covariates, fallback):
    projected_from_visual = project(state["visual"], covariates["scales"]["bands"])
    projected_from_input = project(expected, covariates["scales"]["bands"])
    colors = Counter(state["fills"].values())
    return {
        "visual": state["visual"], "projected": month_labels(state["projected"]),
        "projected_ms": state["projected"], "projected_from_input": month_labels(projected_from_input),
        "projection_matches_visual": state["projected"] == state["dataExtent"] == projected_from_visual,
        "projection_matches_input": state["projected"] == projected_from_input,
        "expected_visual": expected, "residual_css_px": residual(state["visual"], expected),
        "unit_offset": state["unit"]["offset"], "color_counts": dict(sorted(colors.items())),
        "colors_match_predicate": state["fills"] == mask_expected(state, covariates["scales"], fallback),
        "nonselected_count": colors[fallback],
        "invariants_sha256": state["invariantsSha256"]
    }


def derive(raw, scenario, plan, kind, sha):
    gesture = plan["gestures"][scenario["gesture"]]
    local_positions = [gesture["start"], *gesture["moves"]]
    initial = plan["seed"]["extent"] if scenario["state"] == "active" else []
    inside = bool(initial and min(initial) < gesture["start"][0] < max(initial))
    target = "brush" if inside else scenario["position"]
    forced_mode = "translate" if inside and scenario["variant"] != "shared" else "new"
    record = {
        **scenario, "kind": kind, "status": raw["status"] if raw else "not_run",
        "planned_hit": target, "hit": None, "plan_matches_hit": None,
        "planned_starts_inside_brush": inside, "planned_plot_trajectory": local_positions,
        "raw_path": f"evidence/{kind}/{scenario['id']}.json" if raw else None, "raw_sha256": sha
    }
    if not raw or raw["status"] != "executed":
        return record

    native = native_sequence(raw, "test")
    record["status"] = evidence_status(raw, scenario, gesture, native)
    received = [ev for ev in raw["events"] if ev["phase"] == "test" and ev["channel"] == "vega"
                and ev["step"] == "down" and ev["vegaType"] == "mousedown"]
    down = received[0] if len(received) == 1 else None
    hit = event_hit(down)
    record.update(hit=hit, plan_matches_hit=hit == target if hit is not None else None,
                  hit_item=down["item"] if down is not None else None,
                  screen_target=down["target"] if down is not None else None,
                  down_event_sequence=down["sequence"] if down is not None else None)
    before = state_at(raw, "test", "hover")
    record["start_visual"] = before["visual"]
    record["start_projected"] = month_labels(before["projected"])
    record["start_projected_ms"] = before["projected"]
    record["seed_valid"] = (before["visual"] == initial and before["projected"] ==
                            (plan["seed"]["months"] if initial else None))
    record["browser_trace"] = [[e["step"], e["client"], e["plot"], e["button"], e["buttons"]]
                               for e in native] if scenario["observers"] else None
    if record["status"] == "observed" and (hit is None or not record["seed_valid"]):
        record["status"] = "hit_unavailable" if hit is None else "initialization_failed"

    # If hit and plan disagree, preserve the distinct gating implied by the real target.
    mode = forced_mode if hit is None else ("translate" if hit == "brush" and scenario["variant"] != "shared" else "new")
    record["mode_from_hit"] = mode if hit is not None else None
    start = gesture["start"][0]
    width = plan["chartSystem"]["plotSize"][0]
    steps = {}
    relevant = ["down", "first", "move-2", "move-3", "up"]
    plot_by_stage = dict(zip(relevant[:-1], local_positions))
    plot_by_stage["up"] = local_positions[-1]
    for label in relevant:
        snap = close_step(raw, "test", label)
        if not snap:
            continue
        state = snap["first"]
        plot_target = plot_by_stage[label]
        expected = expected_extent(mode, initial, start, plot_target[0], width)
        covariates = raw["invariants"][state["invariantsSha256"]]
        measured = observed_step(state, expected, covariates, FALLBACK[scenario["variant"]])
        measured["planned_pointer_band"] = month_labels(project([plot_target[0], plot_target[0] + 1e-8],
                                                                  covariates["scales"]["bands"]))
        measured["late_frame_fields"] = sorted(set(snap["nextChanges"]) & OBSERVED_FIELDS)
        steps[label] = measured

    record["steps"] = steps
    observed_residual = steps.get("first", {}).get("residual_css_px")
    record["first_jump_sensitivity"] = {str(t): None if observed_residual is None else observed_residual > t
                                        for t in plan["toleranceCssPx"]}
    record["comparable"] = (record["status"] == "observed" and record["plan_matches_hit"] is True
                            and record["seed_valid"] and not any(s["late_frame_fields"] for s in steps.values()))
    record["normal_no_change"] = (steps["up"]["visual"] == before["visual"]
                                  and steps["up"]["projected_ms"] == before["projected"]
                                  and observed_residual in (0, None))
    record["projection_matches_observed_visual_all_steps"] = all(s["projection_matches_visual"] for s in steps.values())
    record["colors_match_observed_selection_all_steps"] = all(s["colors_match_predicate"] for s in steps.values())
    record["axes_data_geometry_preserved"] = all(s["invariants_sha256"] == before["invariantsSha256"]
                                                   for s in steps.values())
    record["static_paint_sha256"] = raw["chart"]["staticPaintSha256"]
    record["final_paint_sha256"] = raw["finalPaintSha256"]
    return record


def event_rows(raw, record):
    snapshots = {(s["phase"], s["step"]): s for s in raw.get("snapshots", [])}
    for ev in raw.get("events", []):
        snap = snapshots.get((ev["phase"], ev["step"]))
        state = snap["first"] if snap else None
        yield {
            "run_id": record["id"], "kind": record["kind"], **ev,
            "state_after_step": {
                "raf": snap["raf"], "visual": state["visual"], "projected_ms": state["projected"],
                "brush_foreground": state["brush"].get("drag_brush_brush", {}).get("rect"),
                "color_counts": dict(sorted(Counter(state["fills"].values()).items())),
                "geometry_axes_aggregate_sha256": state["invariantsSha256"]
            } if state else None,
            "raw_path": record["raw_path"], "raw_sha256": record["raw_sha256"]
        }


def load_mode(plan, directory: Path, mode, with_events):
    kind = {"matrix": "main", "controls": "controls"}[mode]
    runs, events = [], []
    for scenario in plan["cases"][mode]:
        path = directory / (scenario["id"] + ".json")
        data = path.read_bytes() if path.exists() else None
        raw = json.loads(data) if data else None
        if raw and raw["scenario"] != scenario:
            raise ValueError(f"scenario mismatch: {path}")
        record = derive(raw, scenario, plan, kind, digest(data) if data else None)
        runs.append(record)
        if raw and with_events:
            events.extend(event_rows(raw, record))
    return runs, events


def same_signature(a, b, include_color=False):
    def stages(r):
        fields = ["visual", "projected_ms", "unit_offset"]
        if include_color:
            fields.append("color_counts")
        return [tuple(stage[k] for k in fields) for stage in r["steps"].values()]
    return a["hit"] == b["hit"] and stages(a) == stages(b)


def match_pairs(runs, by, contrast, left, right, hit_can_differ=False, colors=False):
    duplicates = {}
    for row in runs:
        if row[contrast] in (left, right):
            key = tuple(row[k] for k in by)
            duplicates.setdefault(key, {})[row[contrast]] = row
    pairs = []
    for key, pair in duplicates.items():
        if left not in pair or right not in pair:
            continue
        a, b = pair[left], pair[right]
        comparable = (a.get("comparable") and b.get("comparable") and a["start_visual"] == b["start_visual"]
                      and a["start_projected_ms"] == b["start_projected_ms"]
                      and (hit_can_differ or a["hit"] == b["hit"]))
        pairs.append({"left": a["id"], "right": b["id"], "comparable": bool(comparable),
                      "matching_trajectory": same_signature(a, b, colors) if comparable else None,
                      "matching_first_selection_pixels": a["steps"]["first"]["visual"] ==
                      b["steps"]["first"]["visual"] if comparable else None,
                      "matching_up_selection": a["steps"]["up"]["projected_ms"] ==
                      b["steps"]["up"]["projected_ms"] if comparable else None,
                      "matching_up_colors": a["steps"]["up"]["color_counts"] ==
                      b["steps"]["up"]["color_counts"] if comparable else None})
    return pairs


def contrasts(runs):
    return {
        "repeat": match_pairs(runs, ("variant", "renderer", "state", "position"), "repeat", 1, 2, colors=True),
        "renderer": match_pairs(runs, ("variant", "state", "position", "repeat"), "renderer", "svg", "canvas",
                                colors=True),
        "original_local": match_pairs(runs, ("renderer", "state", "position", "repeat"), "variant",
                                      "original", "local"),
        "original_shared": match_pairs(runs, ("renderer", "state", "position", "repeat"), "variant",
                                       "original", "shared"),
        "mark_plot": match_pairs(runs, ("variant", "renderer", "state", "repeat"), "position", "mark", "plot",
                                 hit_can_differ=True)
    }


def summarize(main_runs, controls, plan):
    rows = [row for row in main_runs if row.get("comparable")]
    return {
        "main_expected": len(main_runs), "main_outcomes": Counter(row["status"] for row in main_runs),
        "main_comparable": len(rows),
        "main_hit": Counter(f"{row['state']}:{row['position']}:{row['hit']}" for row in rows),
        "main_threshold_counts": {
            str(t): sum(row["first_jump_sensitivity"][str(t)] is True for row in rows)
            for t in plan["toleranceCssPx"]
        },
        "main_initial_down_largest_error_css_px": max(
            (row["steps"]["down"]["residual_css_px"] for row in rows), default=None),
        "main_errors_above_threshold_ids": [
            row["id"] for row in rows if row["first_jump_sensitivity"][str(plan["primaryThresholdCssPx"])] is True
        ],
        "main_projection_matches_observed_visual": sum(row["projection_matches_observed_visual_all_steps"] for row in rows),
        "main_color_contract": sum(row["colors_match_observed_selection_all_steps"] for row in rows),
        "main_invariants_preserved": sum(row["axes_data_geometry_preserved"] for row in rows),
        "main_normal_no_change": sum(row["normal_no_change"] for row in rows),
        "control_outcomes": Counter(row["status"] for row in controls),
        "control_comparable": sum(row.get("comparable", False) for row in controls),
        "contrasts": contrasts(main_runs)
    }


def write_jsonl(path, rows):
    with path.open("w", encoding="utf-8", newline="\n") as out:
        for row in rows:
            out.write(encode(row) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", type=Path, required=True)
    parser.add_argument("--controls", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="new output directory")
    parser.add_argument("--skip-event-ledger", action="store_true", help="recompute runs without writing duplicate event rows")
    args = parser.parse_args()
    plan = read(ROOT / "plan.json")
    need_events = not args.skip_event_ledger
    main_runs, main_events = load_mode(plan, args.main, "matrix", need_events)
    controls, control_events = load_mode(plan, args.controls, "controls", need_events) if args.controls else ([], [])
    args.out.mkdir()
    write_jsonl(args.out / "runs.jsonl", main_runs + controls)
    if need_events:
        write_jsonl(args.out / "events.jsonl", main_events + control_events)
    summary = summarize(main_runs, controls, plan)
    (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                         encoding="utf-8")
    print(encode({k: v for k, v in summary.items() if k not in {"contrasts", "main_errors_above_threshold_ids"}}))


if __name__ == "__main__":
    main()
