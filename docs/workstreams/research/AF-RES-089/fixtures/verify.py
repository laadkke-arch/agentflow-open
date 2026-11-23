#!/usr/bin/env python3
"""Recompute the formal matrix and saved values from the committed raw evidence."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from visibility import active, document, index, object_key, objects, score_names, selected, visible_changes
from write_runs import ledger_row, load, trace

PACKET = Path(__file__).resolve().parents[1]


def require(condition, label):
    if not condition:
        raise ValueError(label)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def event(rows, name, label=None, action=None):
    matches = [row for row in rows if (row.get("event") == name
               and (label is None or row.get("label", "").endswith("-" + label))
               and (action is None or row.get("action") == action))]
    require(len(matches) == 1, f"{name}/{label}/{action}: found {len(matches)}")
    return matches[0]


def xml_values(path):
    """The frozen fixtures have one measure per staff and one chord/rest per voice."""
    top = ET.parse(path).getroot().find("Score")
    values = {}
    for name, score in [("M", top), *((s.findtext("name"), s) for s in top.findall("Score"))]:
        for staff, entry in enumerate(score.findall("Staff")):
            measures = entry.findall("Measure")
            require(len(measures) == 1, f"{path}: unexpected measure count")
            for voice, slice_ in enumerate(measures[0].findall("voice")):
                for cr in (n for n in slice_ if n.tag in {"Rest", "Chord"}):
                    for item in [cr, *cr.findall("Note")]:
                        key = f"{name}:{4 * staff + voice}:0:{item.tag}:{item.findtext('pitch', '-')}"
                        require(key not in values, f"{path}: duplicate XML identity {key}")
                        values[key] = item.findtext("visible", "1") != "0"
    return values


def peers_ok(doc):
    for kind, pitch in (("Chord", "-"), ("Note", 67)):
        master = f"M:8:0:{kind}:{pitch}"
        part = f"Violin:0:0:{kind}:{pitch}"
        if doc[master]["peers"] != [part] or doc[part]["peers"] != [master]:
            return False
        if not (doc[master]["visible"] and doc[part]["visible"]):
            return False
    return True


def check_recorded_images(folder):
    count = 0
    for step in trace(folder / "steps.jsonl"):
        if step["kind"] == "screenshot":
            require(sha(folder / step["file"]) == step["sha256"], f"Screenshot checksum {folder}")
            count += 1
    return count


def state_fields(state):
    return {key: {k: item[k] for k in ("id", "parent_id", "score_id", "flag", "member", "visible", "peers", "cur_color")}
            for key, item in sorted(objects(state).items())}


def check_run(case, run, build):
    ident = run["run_id"]
    expected = case["expected_change_keys"].split()
    require(run == ledger_row(PACKET, case), f"{ident}: ledger differs from observed run")
    require(run["app_exit"] == run["runner_exit"] == 0, f"{ident}: failed process")
    require(sha(PACKET / case["fixture"]) == run["input_sha256"] == case["input_sha256"], f"{ident}: input")
    variant = build["variants"][case["build"]]
    require(run["binary_sha256"] == variant["binary_sha256"]
            and run["app_argv"][:-1] == variant["app_argv_prefix"], f"{ident}: binary or argv")

    log_path = PACKET / run["app_log"]
    rows = trace(log_path)
    steps = trace(PACKET / run["ui_steps"])
    before = event(rows, "ui_snapshot", "before_v")
    after = event(rows, "ui_snapshot", "after_v")
    manual = event(rows, "ui_snapshot", "manual_range")
    require([row["seq"] for row in rows] == list(range(1, len(rows) + 1)), f"{ident}: trace sequence")
    x11 = [i for i, row in enumerate(steps) if row.get("kind") == "keyboard_x11" and row.get("key") == "v"]
    require(len(x11) == 1, f"{ident}: expected one V in X11 steps")
    focus = [row for row in steps if row.get("kind") == "edit_focus"]
    require(len(focus) == 2 and focus[0]["x11"] == focus[1]["x11"]
            and before["focus_class"] == after["focus_class"] == "Ms::ScoreView", f"{ident}: focus")
    gui = event(rows, "gui_action", action="toggle-visible")
    cmd = event(rows, "toggle_visible_enter")
    end = event(rows, "score_action_ended", action="toggle-visible")
    require(before["seq"] < gui["seq"] < cmd["seq"] < end["seq"] < after["seq"], f"{ident}: V route")
    require(selected(before) == selected(cmd) and selected(before)["list"] == expected, f"{ident}: membership")
    require(selected(before)["mode"] == ("RANGE" if expected else "NONE"), f"{ident}: selection mode")
    visited = [row for row in rows if row["event"] == "visibility_target"]
    require([object_key(row["target"], score_names(before)) for row in visited] == expected, f"{ident}: V traversal")
    require([row["target"]["id"] for row in visited] == active(before)["selection"]["list"], f"{ident}: visited addresses")
    require(all(row["visible_before"] and row["target"]["visible"] is False for row in visited),
            f"{ident}: visited property values")
    require(visible_changes(before, after) == {key: [True, False] for key in expected}, f"{ident}: V delta")
    previous = document(before)
    altered = document(after)
    require(previous.keys() == altered.keys() and all(
        {**previous[key], "visible": altered[key]["visible"]} == altered[key]
        for key in previous), f"{ident}: structural change after V")
    require(all(peers_ok(stage) for stage in (document(manual), previous, altered)), f"{ident}: linked guards")
    require(selected(after) == selected(before), f"{ident}: selection changed after V")
    require(index(after) == index(before) + bool(expected), f"{ident}: V index delta")
    require(all(objects(before)[key]["id"] == objects(after)[key]["id"] for key in previous), f"{ident}: V identity")

    notes = []
    if case["case"] in ("X1", "X2"):
        expect_clone = case["case"] == "X1"
        menu = event(rows, "explode_reselected")
        menu_ui = event(rows, "ui_snapshot", "menu_ended")
        require(selected(menu) == selected(menu_ui) == selected(before) and index(menu_ui) == 1, f"{ident}: menu exit")
        clicks = [i for i, row in enumerate(steps) if row.get("intent") == "action:explode"]
        require(len(clicks) == 1 and all(row.get("kind") != "mouse_x11" for row in steps[clicks[0]+1:x11[0]]),
                f"{ident}: a click followed the menu action")
        if expect_clone:
            clone = event(rows, "cloneVoice_call")
            require((clone["source_track"], clone["destination_track"], clone["start_tick"],
                     clone["end_tick"], clone["link"], clone["spanner"]) == (1, 4, 0, 1920, False, True)
                    and not run["menu"]["pasteStaff"], f"{ident}: clone branch or arguments")
            pair = event(rows, "cloneVoice_insert")
            source = next(note for note in pair["source"] if note["type"] == "Note")
            notes = [note for note in pair["destination"] if note["type"] == "Note"]
            require(source["id"] == objects(manual)["M:1:0:Note:64"]["id"] and source["flag"] and source["member"]
                    and notes[0]["id"] != source["id"] and notes[0]["flag"] == (case["build"] == "L")
                    and not notes[0]["member"] and notes[0]["id"] == objects(before)["M:4:0:Note:64"]["id"],
                    f"{ident}: X1 source/destination continuity")
        else:
            paste = event(rows, "pasteStaff_call")
            require((paste["staff"], paste["tick"], paste["paste_mode"]) == (1, 0, True)
                    and not run["menu"]["cloneVoice"], f"{ident}: paste branch or arguments")
            insertion = event(rows, "pasteStaff_insert")
            notes = [objects(insertion)[f"M:4:0:Note:{pitch}"] for pitch in (60, 64)]
            require(not any(n["flag"] or n["member"] for n in notes)
                    and notes[0]["id"] == objects(before)["M:4:0:Note:60"]["id"]
                    and "M:4:0:Note:64" not in previous, f"{ident}: X2 after paste and trim")
    else:
        require(not any(run["menu"].values()) and index(before) == 0, f"{ident}: control ran Explode")

    restored = None
    if expected:
        restored = event(rows, "ui_snapshot", "after_undo")
        require(document(restored) == previous and selected(restored)["mode"] == "NONE"
                and index(restored) == index(before), f"{ident}: Undo values, selection or index")
        require(all(objects(before)[key]["id"] == objects(restored)[key]["id"] for key in previous),
                f"{ident}: Undo did not preserve Explode identities")
        require(index(event(rows, "undo_enter")) == index(after)
                and index(event(rows, "undo_exit")) == index(before), f"{ident}: independent V macro")
        require(sum(row.get("key") == "ctrl+z" for row in steps) == 1, f"{ident}: one Ctrl+Z")
    else:
        require(not any(row.get("key") == "ctrl+z" for row in steps) and run["restored"] is None,
                f"{ident}: Undo would target a different action")

    images = check_recorded_images(log_path.parent)
    stages = {"after-v": after}
    if restored:
        stages["after-undo"] = restored
    require(set(stages) == set(run["saved"]) == set(run["reopen"]), f"{ident}: save count")
    for name, baseline in stages.items():
        saved, read = run["saved"][name], run["reopen"][name]
        file, log = PACKET / saved["path"], PACKET / read["log"]
        again = event(trace(log), "ui_snapshot", "ready")
        require(read["exit"] == read["runner_exit"] == index(again) == 0 and
                document(again) == document(baseline) and peers_ok(document(again)), f"{ident}: reopened model")
        require(sha(file) == saved["sha256"] == sha(log.parent / file.name), f"{ident}: read-back bytes")
        require(xml_values(file) == {key: value["visible"] for key, value in document(again).items()},
                f"{ident}: XML differs from reopened visibility")
        images += check_recorded_images(log.parent)

    return {
        "images_verified": images, "changed_keys": expected, "indexes": run["undo_index"],
        "start_range": selected(manual), "source_objects": state_fields(manual),
        "menu_or_control_objects": state_fields(before), "edit_objects": state_fields(after),
        "restored_objects": state_fields(restored) if restored else None,
        "immediate_insertion_notes": notes, "readbacks_verified": len(stages),
        "semantic_edit": altered, "semantic_undo": document(restored) if restored else None,
    }


def check_auxiliary():
    checks = {}
    for case in ("F-P", "F-X", "PEER", "VV"):
        for build in "GL":
            ident = f"{case}-{build}"
            folder = PACKET / "evidence" / "aux" / ident
            record = load(folder / "result.json")
            rows = trace(folder / "app.jsonl")
            require(record["run_exit"] == 0 and record["processes"][0]["exit_code"] == 0, ident)
            before = event(rows, "ui_snapshot", "before_v")
            after = event(rows, "ui_snapshot", "after_v")
            inside = [row for row in rows if before["seq"] < row["seq"] < after["seq"]]
            event(inside, "toggle_visible_enter")
            require(record["focus"]["before"] == record["focus"]["after"] == "Ms::ScoreView"
                    and record["focus"]["x11_before"] == record["focus"]["x11_after"], f"{ident} focus")
            delta = visible_changes(before, after)
            entry = {"visible_delta": delta, "mode": selected(before)["mode"],
                     "list": selected(before)["list"], "indexes": record["undo_index"],
                     "capture_count": check_recorded_images(folder)}
            if case == "F-P":
                require(delta == {"M:1:0:Note:64": [True, False]}, ident)
            elif case == "F-X":
                inserted = event(rows, "cloneVoice_insert")
                copied = next(obj for obj in inserted["destination"] if obj["type"] == "Note")
                e4 = objects(before)["M:4:0:Note:64"]
                require(not delta and selected(before)["mode"] == "NONE" and not selected(before)["list"]
                        and index(before) == index(after) == 1 and record["restored"] is None, ident)
                require(copied["id"] == e4["id"] and copied["flag"] == e4["flag"] == (build == "L")
                        and not e4["member"], f"{ident} stale highlight")
                entry["oboe_e4"] = {k: e4[k] for k in ("id", "flag", "member", "cur_color")}
            elif case == "PEER":
                master, part = "M:8:0:Note:67", "Violin:0:0:Note:67"
                verify_doc = document(after)
                require(delta == {master: [True, False]} and verify_doc[part]["visible"]
                        and verify_doc[part]["peers"] == [master] and verify_doc[master]["peers"] == [part], ident)
                entry["part_delta"] = [document(before)[part]["visible"], verify_doc[part]["visible"]]
            else:
                baseline = event(rows, "ui_snapshot", "equal_value_reference")
                require(document(after) == document(baseline) and selected(after) == selected(baseline)
                        and index(baseline) == 0 and index(after) == 2, f"{ident}: equal values, different macro index")
                require(len([r for r in rows if r["event"] == "toggle_visible_enter"]) == 2, f"{ident}: two V")
                entry["equal_value_reference_index"] = index(baseline)
            if delta:
                undone = event(rows, "ui_snapshot", "after_undo")
                require(index(undone) == index(before) and document(undone) == document(before), f"{ident} undo")
            for label, meta in record["reopens"].items():
                read_dir = folder / meta["path"]
                saved = folder / f"{label}.mscx"
                snap = event(trace(read_dir / "app.jsonl"), "ui_snapshot", "ready")
                expect = after if label == "after-v" else event(rows, "ui_snapshot", "after_undo")
                require(meta["processes"][0]["exit_code"] == 0 and document(snap) == document(expect)
                        and sha(saved) == sha(read_dir / saved.name) == record["saved"][label]["sha256"],
                        f"{ident} {label} reopened")
                entry["capture_count"] += check_recorded_images(read_dir)
            checks[ident] = entry
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    with (PACKET / "cases.csv").open(newline="") as handle:
        cases = {row["run_id"]: row for row in csv.DictReader(handle)}
    runs = {row["run_id"]: row for row in trace(PACKET / "runs.jsonl")}
    require(len(cases) == len(runs) == 12 and cases.keys() == runs.keys(), "Formal slot mismatch")
    require(len(trace(PACKET / "runs.jsonl")) == 12 and len({r["display"] for r in runs.values()}) == 1,
            "Duplicate runs or divergent displays")
    build = load(PACKET / "evidence/build/build-info.json")
    for variant in ("G", "L"):
        expected = build["variants"][variant]
        require(expected["build_exit"] == 0 and sha(PACKET / f"evidence/build/build-{variant}.log")
                == expected["build_stdout_sha256"], f"{variant}: build log")
        require(sha(PACKET / f"evidence/build/source-{variant}.diff") == expected["source_diff_sha256"],
                f"{variant}: source diff")
    data = {ident: check_run(case, runs[ident], build) for ident, case in cases.items()}
    pairs = {}
    for case, repeats in (("X1", [1, 2]), ("X2", [1, 2]), ("P", [1]), ("N", [1])):
        for repeat in repeats:
            g, l = f"{case}-G-{repeat}", f"{case}-L-{repeat}"
            k = f"{case}-{repeat}"
            pairs[k] = {
                "changed_keys": data[g]["changed_keys"],
                "same_change_keys": data[g]["changed_keys"] == data[l]["changed_keys"],
                "same_post_v_model": data[g]["semantic_edit"] == data[l]["semantic_edit"],
                "same_undo_model": data[g]["semantic_undo"] == data[l]["semantic_undo"],
                "same_undo_indexes": data[g]["indexes"] == data[l]["indexes"],
                "same_saved_bytes": {key: record["sha256"] == runs[l]["saved"][key]["sha256"]
                                     for key, record in runs[g]["saved"].items()},
            }
            require(all(pairs[k][key] for key in ("same_change_keys", "same_post_v_model",
                                                 "same_undo_model", "same_undo_indexes")), f"{k}: pair differs")
    for case in ("X1", "X2"):
        require(all(data[f"{case}-{v}-1"]["semantic_edit"] == data[f"{case}-{v}-2"]["semantic_edit"]
                    for v in "GL"), f"{case}: repeats differ")

    sources = trace(PACKET / "sources.jsonl")
    counted = [row for row in sources if row["counted"]]
    required = {"history": 6, "implementation": 6, "score_case": 6, "inkscape": 3, "calc": 3}
    require(len(set(row["id"] for row in sources)) == len(sources), "Duplicate source IDs")
    counts = Counter(row["category"] for row in counted)
    lineages = {row["lineage_id"] for row in counted}
    require(len(counted) >= 24 and len(lineages) >= 24 and all(counts[k] >= v for k, v in required.items()),
            "Source minimum not met")
    report = {
        "auxiliary": check_auxiliary(),
        "formal": {"slots": len(runs), "menu_runs": 8, "controls": 4, "menu_pairs": 4,
                   "values_changed_main": 8, "matched_target_pairs": 4, "undo_restored_main": 8,
                   "readbacks": sum(r["readbacks_verified"] for r in data.values()),
                   "images_verified": sum(r["images_verified"] for r in data.values())},
        "sources": {"rows": len(sources), "direct_rows_with_duplicates": sum(r["access_status"] in {"direct", "same_lineage"} for r in sources),
                    "unique_primary": len(counted), "independent_lineages": len(lineages),
                    "categories": counts},
        "pairs": pairs, "runs": data,
    }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
