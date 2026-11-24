"""Reduce browser traces to the row ledger without changing the observation files."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODES = ("pilot", "main", "controls", "supplement")
RESULTS = {
    (True, False): "geometry만",
    (False, True): "center만",
    (True, True): "둘 다",
    (False, False): "둘 다 유지",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subtract(end, start):
    return [x - y for x, y in zip(end, start, strict=True)]


def close(left, right, epsilon):
    return all(abs(delta) <= epsilon for delta in subtract(left, right))


def collect(raw, kind, **fields):
    return [
        row
        for row in raw["records"]
        if row["kind"] == kind and all(row.get(key) == value for key, value in fields.items())
    ]


def summarize(plan, scenario, mode, folder):
    identifier = scenario["id"]
    path = folder / mode / f"{identifier}.json"
    entry = {"id": identifier, "mode": mode, "scenario": scenario}
    if not path.is_file():
        return entry | {"execution": "미실행", "comparable": False, "reason": "원 로그 파일 공석"}

    raw = read(path)
    start = raw["initial"]["afterSeed"]
    by_phase = {step["phase"]: step for step in raw["steps"]}
    last = by_phase["settled"]["state"]
    left, top = plan["mapRectCssPx"][:2]
    pixels = plan["positions"][scenario["position"]]
    client = [pixels[0] + left, pixels[1] + top]
    moves = [[client[0] + dx, client[1] + dy] for dx, dy in plan["moves"][scenario["gesture"]]]
    end = moves[-1] if moves else client
    epsilon = plan["epsilon"]
    geometry_changed = not close(last["geometry"], start["geometry"], epsilon["worldCoordinate"])
    center_changed = not close(last["center"], start["center"], epsilon["worldCoordinate"])
    expected_drag_index = next(
        (k for k, point in enumerate(moves, start=1) if max(map(abs, subtract(point, client))) > plan["moveToleranceCssPx"]),
        None,
    )
    reasons = []
    if raw["scenario"] != scenario or raw["commanded"] != {"start": client, "moves": moves, "end": end}:
        reasons.append("봉인 입력과 실행 명령 불일치")
    initial = raw["initial"]
    if (
        start["selectedIds"] != plan["seed"][scenario["selection"]]
        or start["featureId"] != plan["feature"]["id"]
        or start["geometry"] != plan["feature"]["coordinate"]
        or start["center"] != plan["view"]["center"]
        or initial["rect"] != plan["mapRectCssPx"]
        or initial["dpr"] != plan["dpr"]
        or initial["projection"] != plan["view"]["projection"]
        or initial["radiusCssPx"] != plan["feature"]["radiusCssPx"]
        or initial["featureStyleDefined"]
        or initial["selectStyle"] is not None
    ):
        reasons.append("초기 피처·선택·스타일·뷰 또는 화면 입력 불일치")
    states = [start, *(item["state"] for item in raw["steps"])]
    if any(
        state["featureId"] != start["featureId"]
        or state["geometryType"] != start["geometryType"]
        or abs(state["resolution"] - plan["view"]["resolution"]) > epsilon["resolution"]
        or abs(state["rotation"] - plan["view"]["rotation"]) > epsilon["rotationRadians"]
        or state["animating"]
        or (mode == "main" and state["selectedIds"] != start["selectedIds"])
        for state in states
    ):
        reasons.append("피처 ID·geometry 유형·뷰 불변량·선택·animating 조건 불일치")
    if last["interacting"]:
        reasons.append("정착 후 view가 상호작용 중")
    if any(
        note["type"] != "warning" or not note["text"].startswith("Canvas2D: Multiple readback")
        for note in raw["notices"]
    ):
        reasons.append("예상 범위 밖의 브라우저 경고·오류·요청")
    if by_phase["up"]["state"] != last:
        reasons.append("up과 정착 상태 불일치")

    dom_down = collect(raw, "dom", originalType="pointerdown")
    dom_first = collect(raw, "dom", originalType="pointermove", phase="move-1")
    dom_up = collect(raw, "dom", originalType="pointerup")
    map_down = collect(raw, "map-event", type="pointerdown")
    map_drag = collect(raw, "map-event", type="pointerdrag")
    map_up = collect(raw, "map-event", type="pointerup")

    def handlers(event, method, kind="handler-return"):
        if not event:
            return []
        return collect(raw, kind, mapId=event[0]["mapId"], method=method)

    if scenario["observers"]:
        pointer_dom = collect(raw, "dom")
        expected_typing = ["pointermove", "pointerdown"] + ["pointermove"] * len(moves) + ["pointerup"]
        if (
            [event["originalType"] for event in pointer_dom] != expected_typing
            or [event["client"] for event in pointer_dom] != [client, client, *moves, end]
            or any(not event["trusted"] or event["pointerType"] != "mouse" for event in pointer_dom)
            or len(map_down) != 1
            or len(map_up) != 1
        ):
            reasons.append("trusted DOM 포인터 경로 불일치")
        if not dom_down or not close(dom_down[0]["mapPixel"], pixels, epsilon["mapPixel"]):
            reasons.append("down의 map pixel 불일치")
        expected_phase = f"move-{expected_drag_index}" if expected_drag_index is not None else None
        actual_phase = map_drag[0]["phase"] if map_drag else None
        if expected_phase != actual_phase:
            reasons.append("첫 pointerdrag 문턱 불일치")
        map_ids_by_native = {e["nativeId"]: e for e in pointer_dom}
        if any(
            event["nativeId"] not in map_ids_by_native
            or event["eventTimeMs"] != map_ids_by_native[event["nativeId"]]["eventTimeMs"]
            for event in [*map_down, *map_drag, *map_up]
        ):
            reasons.append("DOM–map 이벤트 시간 연결 불일치")

    def changes(event):
        return [
            {"name": row["name"], "method": row["method"], "value": row["value"], "seq": row["seq"]}
            for row in collect(raw, "state-change", mapId=event["mapId"])
        ]

    down_id = map_down[0]["mapId"] if map_down else None
    actual_handler_hits = [
        {key: row[key] for key in ("seq", "name", "method", "hits", "tolerance", "returnFeatureId")}
        for row in collect(raw, "handler-hit", mapId=down_id, method="handleDownEvent")
    ]
    down_chain = [
        {"name": row["name"], "continues": row["returned"], "seq": row["seq"],
         "explicitStop": row["propagationStopped"]}
        for row in handlers(map_down, "handleEvent")
    ]
    relevant_snapshots = {phase: by_phase[phase] for phase in ("down", "move-1", "up", "settled") if phase in by_phase}
    return entry | {
        "execution": "실행",
        "comparable": not reasons,
        "comparison_scope": "full-pointer-trace" if scenario["observers"] else "settled-only",
        "reasons": reasons,
        "raw_path": f"evidence/{mode}/{path.name}",
        "raw_sha256": sha256(path),
        "event_count": len(raw["records"]),
        "dom_down": dom_down[0] if dom_down else None,
        "first_dom_move": dom_first[0] if dom_first else None,
        "first_map_drag": map_drag[0] if map_drag else None,
        "dom_up": dom_up[0] if dom_up else None,
        "down_interaction_hits": actual_handler_hits,
        "down_chain": down_chain,
        "down_accepted": [row["name"] for row in handlers(map_down, "handleDownEvent") if row["returned"]],
        "first_drag_handlers": [row["name"] for row in handlers(map_drag, "handleDragEvent")],
        "up_handlers": [row["name"] for row in handlers(map_up, "handleUpEvent")],
        "drag_state_changes": [{"phase": event["phase"], "changes": changes(event)} for event in map_drag],
        "translate_events": [row["type"] for row in collect(raw, "translate-event")],
        "filter_evaluations": [row["accepted"] for row in collect(raw, "configured-filter")],
        "snapshots": relevant_snapshots,
        "state_initial": start,
        "state_final": last,
        "delta_geometry": subtract(last["geometry"], start["geometry"]),
        "delta_center": subtract(last["center"], start["center"]),
        "feature_pixel_initial": by_phase["hover"]["featurePixel"],
        "feature_pixel_final": by_phase["settled"]["featurePixel"],
        "surfaces": raw["surfaces"],
        "outcome": RESULTS[geometry_changed, center_changed] if not reasons else "미확인",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence")
    parser.add_argument("--modes", nargs="+", choices=MODES, default=["main", "controls", "supplement"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = read(ROOT / "plan.json")
    rows = [
        summarize(plan, scenario, mode, args.evidence)
        for mode in args.modes
        for scenario in plan["cases"][mode]
    ]
    args.output.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    for mode in args.modes:
        group = [row for row in rows if row["mode"] == mode]
        print(mode, "executed", sum(row["execution"] == "실행" for row in group), "/", len(group),
              "comparable", sum(row["comparable"] for row in group))
        for row in group:
            if not row["comparable"]:
                print(row["id"], row.get("reasons", row.get("reason")))
    return 0 if all(row["comparable"] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
