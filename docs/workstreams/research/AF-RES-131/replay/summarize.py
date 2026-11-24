"""Recount trusted input, first state changes, and predicate calls from raw rows."""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = ("geometry", "center", "resolution", "rotation", "selectedIds", "featureId")


def json_file(path):
    return json.loads(path.read_text(encoding="utf-8"))


def delta(first, last):
    return [after - before for before, after in zip(first, last, strict=True)]


def exceeds(values, tolerance):
    return any(abs(value) > tolerance for value in values)


def category(before, after, tolerance):
    geometry = exceeds(delta(before["geometry"], after["geometry"]), tolerance)
    center = exceeds(delta(before["center"], after["center"]), tolerance)
    return {(False, False): "stable-both", (True, False): "geometry-only",
            (False, True): "center-only", (True, True): "both-changed"}[geometry, center]


def state_fields(state):
    return {key: state[key] for key in STATES}


def minimum_met(actual, forecast):
    if forecast == "unobserved":
        return actual is None
    if forecast == ">=1":
        return actual >= 1
    return actual == int(forecast)


def summarize(case, forecast, plan, source, reference):
    outcome = {
        **case, "raw_log": reference, "predicted_category": forecast["category"],
        "predicted_filter": forecast["filter_down_min"], "predicted_layers": forecast["layers_down_min"],
    }
    if not source.is_file():
        return {**outcome, "attempt": "not-run", "comparable": False, "category": "unknown",
                "errors": ["raw log absent"]}
    raw = json_file(source)
    if raw["status"] != "observed":
        return {**outcome, "attempt": "error", "comparable": False, "category": "unknown",
                "errors": [raw.get("error", str(raw.get("notices", [])))]}
    assert raw["scenario"] == case, case["id"]
    initial, records, steps = raw["initial"], raw["records"], raw["steps"]
    before, final = initial["afterSeed"], steps[-1]["state"]
    observed = case["observers"]
    eps = plan["epsilon"]
    final_category = category(before, final, eps["worldCoordinate"])
    callbacks = [event for event in records if event["kind"] == "configured-callback"]
    downs = [event for event in callbacks if event["phase"] == "down"]
    counts = ({option: {"down": sum(event["option"] == option for event in downs),
                       "total": sum(event["option"] == option for event in callbacks)}
               for option in ("filter", "layers")} if observed else {})
    order = [{"phase": event["phase"], "option": event["option"], "mapId": event["mapId"],
              "featureId": event["featureId"], "layerId": event["layerId"],
              "accepted": event["accepted"]} for event in callbacks]
    first_changes = {}
    for event in records:
        if event["kind"] == "state-change" and event["value"] not in first_changes:
            field = event["value"]
            if exceeds(delta(before[field], event["state"][field]), eps["worldCoordinate"]):
                first_changes[field] = {"seq": event["seq"], "phase": event["phase"],
                                        "mapId": event["mapId"], "value": event["state"][field]}
    dom = [event for event in records if event["kind"] == "dom"]
    down = next((event for event in dom if event["originalType"] == "pointerdown"), None)
    first_move = next((event for event in dom if event["phase"] == "move-1"
                       and event["originalType"] == "pointermove"), None)
    up = next((event for event in dom if event["originalType"] == "pointerup"), None)
    hit = down["hits"]["atConfiguredTolerance"] if down else None
    hit_text = (" ".join(f"{item['featureId']}/{item['layerId']}" for item in hit) or "none"
                if hit is not None else "unobserved")
    handler_downs = [{"name": event["name"], "accepted": event["returned"]}
                     for event in records if event["kind"] == "handler-return"
                     and event["phase"] == "down" and event["method"] == "handleDownEvent"]
    translate_accepted = next((event["accepted"] for event in handler_downs if event["name"] == "translate"), False)
    expected_phases = ["hover", "down", *[f"move-{i}" for i in range(1, len(raw["commanded"]["moves"]) + 1)],
                       "up", "settled"] if observed else ["settled"]
    errors = []
    if [step["phase"] for step in steps] != expected_phases:
        errors.append("missing or out-of-order snapshots")
    if observed:
        predictable_client = [raw["commanded"]["start"], raw["commanded"]["start"],
                              *raw["commanded"]["moves"], raw["commanded"]["end"]]
        expected_types = ["pointermove", "pointerdown", *["pointermove"] * len(raw["commanded"]["moves"]),
                          "pointerup"]
        if ([event["client"] for event in dom] != predictable_client
                or [event["originalType"] for event in dom] != expected_types):
            errors.append("native input did not follow commanded trajectory")
        if not all(event["trusted"] and event["primary"] and event["pointerType"] == "mouse"
                   and not any(event["modifiers"]) for event in dom):
            errors.append("non-primary, untrusted or modified pointer")
        if not down or down["button"] != 0 or down["buttons"] != 1 or not up or up["buttons"] != 0:
            errors.append("missing left down/up")
        if not any(event["kind"] == "map-event" and event["type"] == "pointerdown" for event in records):
            errors.append("map did not observe the down")
        if not all(event["layerId"] == plan["feature"]["layerId"] and event["layerIsSeed"]
                   and (event["featureId"] is None if event["option"] == "layers"
                        else event["featureId"] == plan["feature"]["id"] and event["featureIsSeed"])
                   and event["argCount"] == (1 if event["option"] == "layers" else 2)
                   and event["accepted"] == (case[event["option"]] == "allow")
                   for event in callbacks):
            errors.append("callback arguments or returns failed the fixture contract")
        if not all(field in first_changes for field in ("geometry", "center")
                   if exceeds(delta(before[field], final[field]), eps["worldCoordinate"])):
            errors.append("unexplained change without a raw state-change event")
    elif records:
        errors.append("unexpected observer records in bare replay")

    if any(step["state"]["featureId"] != before["featureId"]
           or abs(step["state"]["resolution"] - before["resolution"]) > eps["resolution"]
           or abs(step["state"]["rotation"] - before["rotation"]) > eps["rotationRadians"] for step in steps):
        errors.append("feature ID, resolution or rotation changed")
    matches = final_category == forecast["category"]
    if observed:
        matches = (matches and hit_text == forecast["predicted_hit"]
                   and translate_accepted == (forecast["predicted_translate_accept"] == "True")
                   and all(minimum_met(counts[option][window], forecast[f"{option}_{window}_min"])
                           for option in counts for window in ("down", "total")))
    return {
        **outcome, "attempt": "observed", "comparable": not errors,
        "comparison_scope": "full" if observed else "settled-only", "errors": errors,
        "category": final_category if not errors else "unknown",
        "prediction_matches": matches and not errors,
        "raw_down_hit": hit, "down_target": down.get("target") if down else None,
        "down_target_class": down.get("targetClass") if down else None,
        "down_id": down.get("seq") if down else None,
        "first_move_id": first_move.get("seq") if first_move else None,
        "up_id": up.get("seq") if up else None,
        "down_handler_order": handler_downs if observed else None,
        "callback_counts": counts if observed else None,
        "callback_order": order if observed else None,
        "pointerdrag_count": sum(event["kind"] == "map-event" and event["type"] == "pointerdrag"
                                 for event in records) if observed else None,
        "first_changes": first_changes if observed else None,
        "before": state_fields(before), "settled": state_fields(final),
        "geometry_delta": delta(before["geometry"], final["geometry"]),
        "center_delta": delta(before["center"], final["center"]),
        "renderer": initial["renderer"], "surface_sha256": raw["surfaceSha256"],
        "bundle_sha256": raw["loadedBundleSha256"],
        "configured_options": initial["translateOptions"],
        "selection_style": initial["selectStylePath"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["main", "controls", "supplement", "bare", "all"], default="all")
    args = parser.parse_args()
    plan = json_file(ROOT / "fixture" / "input.json")
    cases = json_file(ROOT / "fixture" / "cases.json")
    with (ROOT / "predictions.csv").open(encoding="utf-8") as stream:
        forecasts = {row["run_id"]: row for row in csv.DictReader(stream)}
    rows = []
    for case in cases:
        mode, run_id = case["mode"], case["id"]
        if args.mode not in ("all", mode):
            continue
        reference = Path(mode) / (run_id + ".json")
        rows.append(summarize(case, forecasts[run_id], plan, args.evidence / reference,
                              str(Path("evidence/browser") / reference)))
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    print(f"planned={len(rows)} observed={sum(row['attempt'] == 'observed' for row in rows)} "
          f"comparable={sum(row['comparable'] for row in rows)} "
          f"predictions_matching={sum(row.get('prediction_matches', False) for row in rows)}")
    return int(not all(row["comparable"] for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
