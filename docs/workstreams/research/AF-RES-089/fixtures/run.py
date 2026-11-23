#!/usr/bin/env python3
"""Exercise a fixed twelve-slot matrix on one Xvfb display with fresh app profiles."""
import argparse
import csv
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from visibility import active, document, index, object_key, score_names, selected, visible_changes


def read_driver(packet):
    spec = importlib.util.spec_from_file_location("af085_replay", packet / "fixtures/replay.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver


def session_type(driver, display):
    class SharedDisplay(driver.Session):
        def init_display(self):
            self.out.mkdir()
            self.input = self.out / self.fixture.name
            shutil.copyfile(self.fixture, self.input)
            self.env = {
                **os.environ, "DISPLAY": display, "QT_QPA_PLATFORM": "xcb",
                "LC_ALL": "C.UTF-8", "QT_STYLE_OVERRIDE": "Fusion", "AF085_TRACE": "1",
                "XDG_RUNTIME_DIR": str(self.out / "runtime"),
                "XDG_CONFIG_HOME": str(self.out / "config"),
                "XDG_DATA_HOME": str(self.out / "data"),
                "XDG_CACHE_HOME": str(self.out / "cache"),
                "TMPDIR": str(self.out / "tmp"),
                "AF085_SNAPSHOT_REQUEST": str(self.out / "snapshot-request"),
            }
            for name in ("XDG_RUNTIME_DIR", "TMPDIR"):
                Path(self.env[name]).mkdir(mode=0o700)
            self.write("display_shared", display=display, screen="1280x900x24", dpi=96)

        def x11_focus(self):
            return subprocess.check_output(["xdotool", "getwindowfocus"], env=self.env, text=True).strip()

    return SharedDisplay


def prepare_selection(app, case):
    app.score_object("Note", 0, 60)
    app.snapshot("source_selected")
    app.score_object("Rest", 4, modifier="Shift_L")
    state = app.snapshot("manual_range")
    selection = selected(state)
    bounds = (selection["mode"], selection["staff_start"], selection["staff_end"],
              selection.get("tick_start"), selection.get("tick_end"))
    if bounds != ("RANGE", 0, 2, 0, 1920):
        raise ValueError(f"Unexpected starting range {selection}")
    if case in ("X1", "X2"):
        app.click_widget("menu", "Tools")
        app.snapshot("tools_open")
        app.screen("01-menu", move_pointer=False)
        app.click_widget("action", action="explode")
        app.snapshot("menu_ended")
    elif case == "N":
        app.key("Escape", "Clear the same manual range before the negative control")


def save_copy(app, label):
    app.key("ctrl+s", f"Save {label} to the isolated working file")
    state = app.snapshot(f"saved_{label}")
    copy = app.out / f"{label}.mscx"
    shutil.copyfile(app.input, copy)
    app.write("save_evidence", label=label, file=copy.name, probe_seq=state["seq"])
    return copy, state


def reopen(session_factory, app, saved, name, capture_screen):
    reader = session_factory(app.binary, saved, app.out / name)
    try:
        reader.init_display()
        state = reader.launch()
        if capture_screen:
            reader.screen("reopened", move_pointer=False)
        reader.quit()
        reader.results["run_exit"] = 0
        return state
    except Exception:
        reader.results["run_exit"] = 1
        raise
    finally:
        reader.close()
        app.results["reopens"][saved.stem] = {
            **reader.results, "path": name, "snapshot_seq": reader.state.get("seq")
        }


def exercise(app, row, driver, session_factory, prepare=prepare_selection):
    case = row["case"]
    app.init_display()
    opened = app.launch()
    app.results["start_undo_index"] = index(opened)
    prepare(app, case)
    before = app.snapshot("before_v")
    app.screen("02-before-v", move_pointer=False)
    focus_before = app.x11_focus()
    app.write("edit_focus", stage="before_v", x11=focus_before, qt=before["focus_class"])
    app.key("v", "One Toggle Visibility shortcut with no post-menu score click")
    after = app.snapshot("after_v")
    focus_after = app.x11_focus()
    app.write("edit_focus", stage="after_v", x11=focus_after, qt=after["focus_class"])
    app.screen("03-after-v", move_pointer=False)

    trace = driver.entries(app.trace)
    in_window = [event for event in trace if before["seq"] < event["seq"] < after["seq"]]
    result = app.results
    result["focus"] = {"before": before["focus_class"], "after": after["focus_class"],
                       "x11_before": focus_before, "x11_after": focus_after}
    result["menu"] = {
        "gui_explode": [event["seq"] for event in trace if event["event"] == "gui_action"
                        and event.get("action") == "explode"],
        "cloneVoice": [event for event in trace if event["event"] == "cloneVoice_call"],
        "pasteStaff": [event for event in trace if event["event"] == "pasteStaff_call"],
    }
    result["v_dispatch"] = {
        "gui": [event["seq"] for event in in_window if event["event"] == "gui_action"
                and event.get("action") == "toggle-visible"],
        "model": [event["seq"] for event in in_window if event["event"] == "toggle_visible_enter"],
        "end": [event["seq"] for event in in_window if event["event"] == "score_action_ended"
                and event.get("action") == "toggle-visible"],
    }
    result["visited"] = [
        {"key": object_key(event["target"], score_names(before)), "id": event["target"]["id"],
         "seq": event["seq"], "visible": [event["visible_before"], event["target"]["visible"]]}
        for event in in_window if event["event"] == "visibility_target"
    ]
    result["selection"] = {"before": selected(before), "after": selected(after), "undo": None}
    result["undo_index"] = {"before": index(before), "after": index(after), "undo": None}
    result["trace_seq"] = {"before": before["seq"], "after": after["seq"], "undo": None}
    result["changed"] = changed = visible_changes(before, after)
    result["restored"] = None
    result["undo"] = "skipped_no_visible_delta"
    result["document_edited"] = document(before) != document(after)
    result["saved"] = {}
    result["reopens"] = {}
    edited, saved_edit = save_copy(app, "after-v")
    result["saved"]["after-v"] = {"sha256": driver.sha256(edited), "seq": saved_edit["seq"]}
    recovered = saved_undo = None
    if changed:
        # An undo is safe only if the latest new macro was the single delivered V.
        is_v = all(len(result["v_dispatch"][name]) == 1 for name in ("gui", "model", "end"))
        if is_v and index(after) == index(before) + 1 and index(saved_edit) == index(after):
            app.key("ctrl+z", "Undo the V macro only")
            recovered = app.snapshot("after_undo")
            app.screen("04-after-undo", move_pointer=False)
            result["undo"] = "sent_one_ctrl_z"
            result["selection"]["undo"] = selected(recovered)
            result["undo_index"]["undo"] = index(recovered)
            result["trace_seq"]["undo"] = recovered["seq"]
            result["restored"] = visible_changes(after, recovered)
            result["restore_document"] = document(recovered) == document(before)
            saved_undo, undo_save_state = save_copy(app, "after-undo")
            result["saved"]["after-undo"] = {"sha256": driver.sha256(saved_undo), "seq": undo_save_state["seq"]}
        else:
            result["undo"] = "skipped_unattributed_macro"
    app.quit()

    for copy, path, expected in [(edited, "read-e", after), (saved_undo, "read-u", recovered)]:
        if copy:
            read = reopen(session_factory, app, copy, path, capture_screen=True)
            result["reopens"][copy.stem]["document_matches"] = document(read) == document(expected)
            result["reopens"][copy.stem]["undo_index_fresh"] = index(read)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--af085", required=True, type=Path)
    parser.add_argument("--bin", required=True, type=Path, dest="bins")
    parser.add_argument("--display", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--phase", required=True, choices=("controls", "main"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    packet = Path(__file__).resolve().parents[1]
    driver = read_driver(args.af085.resolve())
    factory = session_type(driver, args.display)
    with (packet / "cases.csv").open(newline="") as file:
        rows = {row["run_id"]: row for row in csv.DictReader(file)}

    order = ("P-G-1", "P-L-1", "N-L-1", "N-G-1") if args.phase == "controls" else (
        "X1-G-1", "X1-L-1", "X2-L-1", "X2-G-1", "X1-L-2", "X1-G-2", "X2-G-2", "X2-L-2",
    )
    failures = 0
    for ident in order:
        row = rows[ident]
        binary = args.bins.resolve() / f"mscore-{row['build']}"
        app = factory(binary, packet / row["fixture"], args.out.resolve() / ident)
        if app.out.exists():
            raise FileExistsError(f"Preserve the existing attempt at {app.out}")
        app.results.update(run_id=ident, case=row["case"], build=row["build"], repeat=int(row["repeat"]),
                           runner_argv=[sys.executable, "-B", *sys.argv])
        if app.results["input_sha256"] != row["input_sha256"]:
            raise ValueError(f"Input bytes differ from the frozen slot {ident}")
        try:
            exercise(app, row, driver, factory)
            app.results["run_exit"] = 0
            print(ident, app.results["changed"], app.results["undo_index"], flush=True)
        except (OSError, RuntimeError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as error:
            app.results.update(error=f"{type(error).__name__}: {error}", run_exit=1)
            failures += 1
            if app.out.exists():
                app.write("failed", error=app.results["error"])
            if app.app and app.app.poll() is None:
                try:
                    app.screen("failure", move_pointer=False)
                except (OSError, subprocess.SubprocessError):
                    pass
            print(ident, app.results["error"], flush=True)
        finally:
            app.close()
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(main())
