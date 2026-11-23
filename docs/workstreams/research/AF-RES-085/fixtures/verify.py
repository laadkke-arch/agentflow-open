#!/usr/bin/env python3
"""Recompute the paired GUI claims from committed trace, XML and screen evidence."""
import argparse
import csv
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
from xml.etree import ElementTree


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def digest(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def one(candidates, description):
    values = list(candidates)
    assert len(values) == 1, (description, len(values))
    return values[0]


def events(trace, name):
    return [row for row in trace if row["event"] == name]


def phase(trace, name):
    return one((row for row in events(trace, "ui_snapshot") if row["label"].endswith("-" + name)), name)


def get_score(state, title=None):
    return one((score for score in state["scores"]
                if (score["master"] if title is None else score["title"] == title)), title or "master")


def get_element(score, kind, track, pitch, tick=0):
    return one((row for row in score["objects"] if (row["type"], row["track"], row.get("pitch"), row.get("tick"))
                == (kind, track, pitch, tick)), (score["title"], kind, track, pitch, tick))


def bits(obj):
    return [int(obj["flag"]), int(obj["member"]), int(obj["mark"]) if "mark" in obj else None]


def checked_files(root, files):
    for entry in files.values():
        archive = root / entry["path"]
        assert archive.stat().st_size == entry["bytes"], archive
        assert digest(archive) == entry["sha256"], archive


def musical_state(snapshot, include_rests=False):
    """Compare saved values with stable identities across subprocesses."""
    kind = ("Note", "Fingering", "Rest") if include_rests else ("Note", "Fingering")
    equivalents, occurrences, objects = {}, Counter(), {}
    for score in snapshot["scores"]:
        title = "master" if score["master"] else score["title"]
        occurrences[title] += 1
        for item in score["objects"]:
            if item["type"] in kind:
                key = (title, occurrences[title], item["type"], item["tick"], item["track"], item.get("pitch"), item.get("text"))
                assert key not in objects, key
                assert item["member"] == (item["id"] in score["selection"]["list"]), key
                objects[key] = item
                equivalents[item["id"]] = key

    resolved = {}
    for key, item in objects.items():
        peers = tuple(sorted(equivalents[peer["id"]] for peer in item["peers"]))
        for peer in peers:
            assert item["id"] in [other["id"] for other in objects[peer]["peers"]], (key, peer)
        if item["type"] == "Fingering":
            parent_key = equivalents[item["parent_id"]]
            assert parent_key[2] == "Note" and key[3:6] == parent_key[3:6], key
        resolved[key] = (item["duration_ticks"], item["tag"], item["visible"], peers)
    return resolved


def preserved_sentinel(before, after, case):
    layer_case = case in ("X3", "X4")
    track = 4 if layer_case else 8
    title = "Oboe" if layer_case else "Violin"
    original = next(score for score in before["scores"] if score["title"] == title)
    old_part = one((score for score in after["scores"] if score["id"] == original["id"]), "old sentinel score")
    old_note = get_element(original, "Note", 0, 67)
    part_note = get_element(old_part, "Note", 0, 67)
    assert {key: value for key, value in old_note.items() if key != "peers"} == {
        key: value for key, value in part_note.items() if key != "peers"}
    assert {peer["id"] for peer in old_note["peers"]} <= {peer["id"] for peer in part_note["peers"]}
    sentinel = get_element(get_score(after), "Note", track, 67)
    original_peer = get_element(old_part, "Note", 0, 67)
    assert sentinel["duration_ticks"] == 1920 and not sentinel["flag"] and not sentinel["member"]
    assert {peer["id"] for peer in sentinel["peers"]} >= {original_peer["id"]}
    return len(sentinel["peers"])


def from_screen(path, snapshot, obj):
    widget = one((item for item in snapshot["objects_on_screen"] if item["id"] == obj["id"]), "screen rectangle")
    left, top, width, height = widget["rect"]
    assert width > 0 and height > 0, widget
    crop = f"{width}x{height}+{left}+{top}"
    rgb = subprocess.check_output(["convert", str(path), "-crop", crop, "+repage", "-depth", "8", "rgb:-"])
    assert len(rgb) == width * height * 3, path
    pixels = zip(rgb[::3], rgb[1::3], rgb[2::3])
    blue = ink = 0
    for red, green, blue_channel in pixels:
        blue += blue_channel > red + 55 and blue_channel > green + 28
        ink += min(red, green, blue_channel) < 180
    return {"rect": widget["rect"], "blue": blue, "ink": ink, "probe_seq": snapshot["seq"]}


def verify_native_xml(path, case):
    score = ElementTree.parse(path).getroot().find("Score")
    assert not any(node.tag in ("selected", "mark") for node in score.iter()), path
    if case in ("X1", "X2"):
        pitches = ["60", "64", "67"] if case == "X1" else ["64", "60", "67"]
        for index, (staff, pitch) in enumerate(zip(score.findall("Staff"), pitches, strict=True), 1):
            assert staff.get("id") == str(index)
            measures = staff.findall("Measure")
            assert len(measures) == 1
            chords_and_rests = [event for event in measures[0].findall("voice/*") if event.tag in ("Chord", "Rest")]
            only = one(chords_and_rests, "one chord and no overlapping rest")
            assert only.tag == "Chord" and only.findtext("durationType") == "whole"
            assert [note.findtext("pitch") for note in only.findall("Note")] == [pitch]
    else:
        flutes = [part for part in score.findall("Score") if part.findtext("name") == "Flute"]
        part = one(flutes, "one new Flute")
        child = part.find("Staff/Measure/voice/Chord/Note/Fingering")
        assert child.findtext("tag") == "study-child" and child.findtext("text") == "1"
        assert child.findtext("visible", "1") == "1"
        assert len([p for p in score.findall("Score") if p.findtext("name") == "Oboe"]) == 2


def gui(root, row, case_pin):
    case, variant = row["case"], row["build"]
    is_explode = case in ("X1", "X2")
    focus_title = None if is_explode else "Flute"
    kind = "Note" if is_explode else "Fingering"
    target_track = 4 if is_explode else 0
    pitch = 64 if case == "X1" else 60
    checks = row["checks"]
    assert all(checks.values()) or set(key for key, result in checks.items() if not result) == {"primary_undo_executed"}, row["run_id"]
    assert row["run_exit"] == 0 and [proc["exit_code"] for proc in row["processes"]] == [0, 0]
    assert digest(root / row["input"]) == case_pin["sha256"] == row["input_sha256"]
    files = row["files"]
    directory = (root / files["app.jsonl"]["path"]).parent
    app, reopen, steps = map(lines, [directory / "app.jsonl", directory / "reopen.jsonl", directory / "steps.jsonl"])
    for trace in (app, reopen):
        assert [entry["seq"] for entry in trace] == list(range(1, len(trace) + 1))
    saved = directory / "saved.mscx"
    assert digest(saved) == row["saved_sha256"] != row["input_sha256"]
    verify_native_xml(saved, case)

    before = phase(app, "before_menu")
    ended = phase(app, "menu_ended")
    edit_before = phase(app, "next_edit_before")
    edit_after = phase(app, "next_edit_after")
    undo_boundary = phase(app, "primary_undo_boundary")
    primary_saved = phase(app, "primary_saved")
    reselect_before = phase(app, "reselected_edit_before")
    reselect_after = phase(app, "reselected_edit_after")
    reselect_undo = phase(app, "reselected_undo_after")
    repro = phase(reopen, "reopened" if is_explode else "reopened_flute")

    def find(state):
        return get_element(get_score(state, focus_title), kind, target_track, pitch)

    music = musical_state(edit_before, include_rests=True)
    assert music == musical_state(edit_after, include_rests=True) == musical_state(undo_boundary, include_rests=True)
    assert music == musical_state(primary_saved, include_rests=True) == musical_state(reselect_before, include_rests=True)
    assert music == musical_state(reselect_undo, include_rests=True) == musical_state(repro, include_rests=True)
    assert get_score(edit_before, focus_title)["undo_index"] == get_score(edit_after, focus_title)["undo_index"] == 1
    assert get_score(reselect_after, focus_title)["undo_index"] == 2
    assert get_score(reselect_undo, focus_title)["undo_index"] == 1
    delta = {key: value for key, value in musical_state(reselect_after).items()
             if musical_state(reselect_before).get(key) != value}
    changed_key, changed_value = one(delta.items(), "one changed note or child")
    assert changed_key[2:6] == (kind, 0, target_track, pitch)
    assert changed_value[0] == (960 if is_explode else 1920)
    assert changed_value[2] == is_explode
    assert bits(find(reselect_before)) == ([1, 1, 0] if is_explode else [1, 1, None])
    assert find(edit_before)["duration_ticks"] == 1920 and find(reselect_undo)["duration_ticks"] == 1920
    assert bits(find(repro)) == ([0, 0, 0] if is_explode else [0, 0, None])
    assert get_score(repro, focus_title)["selection"]["mode"] == "NONE"
    assert len(get_score(repro, focus_title)["selection"]["list"]) == 0

    focus_edit = [obj for obj in events(app, "score_action") if edit_before["seq"] < obj["seq"] < edit_after["seq"]]
    assert [obj["action"] for obj in focus_edit] == ["pad-note-2" if is_explode else "toggle-visible"]
    assert any(step["kind"] == "mouse_x11" and step["intent"] == "action:explode" for step in steps) == is_explode
    assert sum(step["kind"] == "mouse_x11" and step["intent"] == "button:New All" for step in steps) == (0 if is_explode else 1)
    links_after_menu = preserved_sentinel(before, ended, case)
    assert links_after_menu == (1 if is_explode else 2)

    if is_explode:
        assert len(events(app, "explode_enter")) == 1
        source = get_element(get_score(before), "Note", 1 if case == "X1" else 0, pitch)
        if case == "X1":
            path = one(events(app, "cloneVoice_call"), "one cloneVoice")
            properties = [path[field] for field in ("source_track", "destination_track", "start_tick", "end_tick", "link", "spanner")]
            assert properties == [1, 4, 0, 1920, False, True]
            assert not events(app, "pasteStaff_call")
            inserted = one(events(app, "cloneVoice_insert"), "one clone insertion")
            immediate = one((obj for obj in inserted["destination"] if obj["type"] == "Note"), "new bottom E4")
            assert bits(immediate) == [int(variant != "G"), 0, 0] and immediate["track"] == 4
        else:
            path = one(events(app, "pasteStaff_call"), "one pasteStaff")
            assert (path["staff"], path["tick"], path["paste_mode"]) == (1, 0, True)
            assert not events(app, "cloneVoice_call")
            inserted = one(events(app, "pasteStaff_insert"), "one paste insertion")
            immediate = find(inserted)
            assert bits(immediate) == bits(get_element(get_score(inserted), "Note", 4, 64)) == [0, 0, 0]
            assert inserted["seq"] < one(events(app, "pasteStaff_range_planned"), "planned paste range")["seq"]
        reselected = one(events(app, "explode_reselected"), "range reselected")
        assert inserted["seq"] < reselected["seq"] < ended["seq"]
        assert bits(find(reselected)) == bits(find(ended)) == [1, 1, 0]
        assert find(ended)["id"] == immediate["id"] != source["id"] and not find(ended)["peers"]
        assert get_score(ended)["selection"]["mode"] == "RANGE"
        assert len(get_score(ended)["selection"]["list"]) == 2
        scan = None
        hidden_metrics = None
    else:
        assert len(events(app, "excerpt_enter")) == len(events(app, "excerpt_return")) == 2
        assert len(events(app, "excerpts_dialog_create_return")) == 2
        assert not events(app, "cloneVoice_call") and not events(app, "pasteStaff_call")
        source = get_element(get_score(before), kind, 0, pitch)
        assert source["tag"] == 2 and source["tag_valid"] == (case == "X4")
        assert bits(source) == [1, 1, None]
        inserted = events(app, "excerpt_cloned")[0]
        immediate = find(inserted)
        assert immediate["id"] != source["id"] and immediate["parent_id"] != source["parent_id"]
        assert immediate["tag"] == 2 and immediate["tag_valid"] == (case == "X4")
        assert bits(immediate) == [int(variant != "G"), 0, None]
        assert [p["id"] for p in immediate["peers"]] == [source["id"]]
        scans = events(app, "note_child_scan")
        if variant == "L":
            scan = one(scans, "only the L reset scan")
            assert scan["stage"] == "after_final_layout" and scan["all"] and scan["flag_before"]
            assert scan["tag_pass"] == (case == "X4") and scan["child"]["flag"] == (case == "X3")
            assert scan["child"]["id"] == immediate["id"]
        else:
            assert not scans
            scan = None
        return_event = events(app, "excerpt_return")[0]
        assert inserted["seq"] < return_event["seq"] < ended["seq"]
        flag_at_end = int(variant == "U" or (variant == "L" and case == "X3"))
        assert bits(find(return_event)) == bits(find(ended)) == [flag_at_end, 0, None]
        assert bits(find(phase(app, "focus_flute_tab"))) == bits(find(primary_saved)) == [flag_at_end, 0, None]
        assert find(edit_before)["tag_valid"] and find(edit_before)["id"] == immediate["id"]
        assert get_element(get_score(edit_after), kind, 0, pitch)["visible"]
        hidden_metrics = None
        if case == "X3":
            hidden_view = phase(app, "flute_first_view")
            hidden_metrics = from_screen(directory / "03-menu-ended.png", hidden_view, find(hidden_view))
            assert hidden_metrics["ink"] == 0 and hidden_metrics["blue"] == 0, hidden_metrics

    image = "03-menu-ended.png" if is_explode else "04-shown.png"
    image_state = ended if is_explode else phase(app, "layer_shown")
    pixels = from_screen(directory / image, image_state, find(image_state))
    assert pixels["ink"] > 0, (row["run_id"], pixels)
    assert bool(pixels["blue"]) == bool(find(image_state)["flag"]), (row["run_id"], pixels)
    reread = from_screen(directory / "07-reopened.png", repro, find(repro))
    assert reread["blue"] == 0 and reread["ink"] > 0, (row["run_id"], reread)
    return {"run_id": row["run_id"], "case": case, "build": variant, "repeat": row["repeat"],
            "input_sha256": row["input_sha256"], "saved_sha256": row["saved_sha256"],
            "immediate": bits(immediate), "menu_end": bits(find(ended)), "before_key": bits(find(edit_before)),
            "after_key": bits(find(edit_after)), "after_save": bits(find(primary_saved)), "reopen": bits(find(repro)),
            "same_document_after_key": True, "clicked_edit": [kind, target_track, pitch, changed_value[0], changed_value[2]],
            "undo_reverted": True, "before_key_selection": get_score(edit_before, focus_title)["selection"]["mode"],
            "before_key_list_size": len(get_score(edit_before, focus_title)["selection"]["list"]),
            "source_id": source["id"], "source_parent_id": source["parent_id"], "destination_id": immediate["id"],
            "destination_parent_id": immediate["parent_id"],
            "destination_scan": None if scan is None else {"passed": scan["tag_pass"], "probe": scan["seq"]},
            "other_peer_count": links_after_menu,
            "rest_replacement_warning": "there is already a Rest at track 4 tick 0" in (directory / "app.stderr").read_text(),
            "screen": {"image": image, **pixels}, "hidden_screen": hidden_metrics, "reopen_screen": reread,
            "probes": {"before": before["seq"], "immediate": inserted["seq"], "menu_end": ended["seq"],
                       "edit_before": edit_before["seq"], "edit_after": edit_after["seq"], "primary_saved": primary_saved["seq"],
                       "reselected_after": reselect_after["seq"], "undo_after": reselect_undo["seq"], "reopen": repro["seq"]}}


def auxiliary(root, row):
    trace = {entry["stage"]: entry for entry in lines(root / row["files"]["stdout.jsonl"]["path"])}
    case = row["case"]
    assert row["run_exit"] == 0
    key = "C1" if case == "E05" else "P1"
    expected = [int(row["build"] != "G"), 0, 0] if case == "E05" else [0, 0, 1]
    clone = trace["immediate"]["objects"][key]
    assert bits(clone) == expected and bits(trace["reopened"]["objects"][key]) == [0, 0, 0]
    assert (clone["cur_color"] == clone["selection_color"]) == bool(expected[0] or expected[2])
    assert bits(trace["after_command"]["objects"][key]) == expected
    return {"run_id": row["run_id"], "immediate": expected, "reopened": [0, 0, 0]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    with (root / "cases.csv").open(encoding="utf-8") as input_file:
        cases = {row["case_id"]: row for row in csv.DictReader(input_file)}
    builds = load(root / "evidence/build/build-info.json")
    runs = lines(root / "runs.jsonl")
    prior = lines(root / "evidence/gui-attempts.jsonl")
    sources = lines(root / "sources.jsonl")
    keys = [(r["case"], r["build"], r["repeat"]) for r in runs if r["entry_mode"] == "gui_x11_native_menu"]
    assert sorted(keys) == sorted(itertools.product(cases, "UGL", (1, 2)))
    assert len({entry["run_id"] for entry in runs}) == len(runs)
    checked_paths = 0
    for row in runs + prior:
        checked_files(root, row["files"])
        checked_paths += len(row["files"])
    records, controls = {}, []
    for row in runs:
        if row["entry_mode"] == "gui_x11_native_menu":
            assert row["binary_sha256"] == builds["variants"][row["build"]]["binary_sha256"]
            try:
                records[row["run_id"]] = gui(root, row, cases[row["case"]])
            except AssertionError as error:
                raise AssertionError(f"{row['run_id']}: {error}") from error
        else:
            assert row["entry_mode"] == "auxiliary_direct_call"
            controls.append(auxiliary(root, row))

    # IDs and individual X11 rectangles live in the process or screen coordinate space.
    # Stable semantic signatures are compared across profiles.
    signature = ("immediate", "menu_end", "before_key", "after_key", "after_save", "reopen",
                 "same_document_after_key", "clicked_edit", "undo_reverted", "before_key_selection",
                 "before_key_list_size", "other_peer_count", "rest_replacement_warning", "saved_sha256")
    for case, build in itertools.product(cases, "UGL"):
        left, right = (records[f"{case}-{build}-{rep}"] for rep in (1, 2))
        assert all(left[key] == right[key] for key in signature), (case, build)
    pairs = {}
    for case, rep in itertools.product(cases, (1, 2)):
        base, glob, local = (records[f"{case}-{build}-{rep}"] for build in "UGL")
        assert base["input_sha256"] == glob["input_sha256"] == local["input_sha256"]
        assert base["saved_sha256"] == glob["saved_sha256"] == local["saved_sha256"]
        assert base["clicked_edit"] == glob["clicked_edit"] == local["clicked_edit"]
        assert base["same_document_after_key"] == glob["same_document_after_key"] == local["same_document_after_key"]
        pairs[f"{case}-{rep}"] = {key: glob[key] == local[key] for key in signature}
        pairs[f"{case}-{rep}"]["rendered_blue"] = bool(glob["screen"]["blue"]) == bool(local["screen"]["blue"])
    categories = {}
    for entry in sources:
        for item in entry["local_evidence"]:
            assert (root / item).exists(), item
        group = entry["count_group"]
        if group:
            categories.setdefault(group, set()).add(entry["lineage_id"])
    all_lineages = set().union(*categories.values())
    assert len(all_lineages) == sum(map(len, categories.values())) >= 22
    for group, bound in {"musescore_history": 8, "notation_outcomes": 4, "vector3d": 3,
                         "text_multiview": 3, "persistence_undo": 4}.items():
        assert len(categories[group]) >= bound
    report = {
        "planned_gui": 24, "verified_gui": len(records), "failed_gui_slots": 0, "valid_repeat_pairs": 12,
        "matched_GL_repeats": len(pairs), "compared_U_baseline_repeats": len(pairs),
        "pairs_immediate_flag_diff": sum(not p["immediate"] for p in pairs.values()),
        "pairs_visible_flag_diff": sum(not p["before_key"] for p in pairs.values()),
        "pairs_render_diff": sum(not p["rendered_blue"] for p in pairs.values()),
        "pairs_next_edit_diff": sum(not p["clicked_edit"] or not p["same_document_after_key"] for p in pairs.values()),
        "primary_next_edits_changed_value": sum(not r["same_document_after_key"] for r in records.values()),
        "separate_reselection_edits_and_undo": sum(r["undo_reverted"] for r in records.values()),
        "rehearsal_attempts": len(prior), "rehearsal_incomplete": sum(not a["observed_primary"] for a in prior),
        "rest_replacement_warnings": sum(r["rest_replacement_warning"] for r in records.values()),
        "file_fingerprints_checked": checked_paths, "source_rows": len(sources), "independent_sources": len(all_lineages),
        "source_groups": {group: len(ids) for group, ids in categories.items()},
        "gui": list(records.values()), "auxiliary": controls, "GL_pairs": pairs,
    }
    result = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.write_text(result, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("gui", "auxiliary", "GL_pairs")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
