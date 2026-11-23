#!/usr/bin/env python3
"""Drive the historical application with X11 input and request read-only snapshots."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def entries(path):
    if not path.exists():
        return []
    lines = path.read_bytes().splitlines(keepends=True)
    return [json.loads(line) for line in lines if line.endswith(b"\n")]


def active_score(state):
    return next(score for score in state["scores"] if score["id"] == state["active_score_id"])


def find_object(score, kind, track=None, pitch=None, tick=0):
    matches = [
        item for item in score["objects"]
        if item["type"] == kind and item.get("tick") == tick
        and (track is None or item["track"] == track)
        and (pitch is None or item.get("pitch") == pitch)
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one {kind} with track={track}, pitch={pitch}, tick={tick}, found {len(matches)}")
    return matches[0]


def matches_widget(row, kind, text=None, action=None):
    return (row["kind"] == kind
            and (text is None or row["text"].replace("&", "") == text)
            and (action is None or row.get("action") == action))


class Session:
    def __init__(self, binary, fixture, out, experimental=False):
        self.binary = binary
        self.fixture = fixture
        self.out = out
        self.experimental = experimental
        self.side_log = out / "steps.jsonl"
        self.results = {"started_utc": utc(), "entry": "xdotool_real_x11",
                        "input_sha256": sha256(fixture), "binary_sha256": sha256(binary), "processes": []}
        self.xvfb = self.app = None
        self.state = {}
        self.seq = 0
        self.launch_number = 0

    def write(self, kind, **fields):
        event = {"utc": utc(), "kind": kind, **fields}
        with self.side_log.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def init_display(self):
        self.out.mkdir()
        self.input = self.out / self.fixture.name
        shutil.copyfile(self.fixture, self.input)
        env = dict(os.environ)
        env.update(QT_QPA_PLATFORM="xcb", LC_ALL="C.UTF-8", QT_STYLE_OVERRIDE="Fusion", AF085_TRACE="1",
                   XDG_RUNTIME_DIR=str(self.out / "runtime"), XDG_CONFIG_HOME=str(self.out / "config"),
                   XDG_DATA_HOME=str(self.out / "data"), XDG_CACHE_HOME=str(self.out / "cache"),
                   TMPDIR=str(self.out / "tmp"), AF085_SNAPSHOT_REQUEST=str(self.out / "snapshot-request"))
        Path(env["XDG_RUNTIME_DIR"]).mkdir(mode=0o700)
        Path(env["TMPDIR"]).mkdir(mode=0o700)
        with (self.out / "display.txt").open("wb") as display, (self.out / "xvfb.log").open("wb") as error:
            args = ["Xvfb", "-displayfd", str(display.fileno()), "-screen", "0", "1280x900x24", "-dpi", "96",
                    "-ac", "-nolisten", "tcp"]
            self.xvfb = subprocess.Popen(args, stdout=error, stderr=error, pass_fds=(display.fileno(),), cwd=self.out)
            self.write("display_start", argv=args)
        display_path = self.out / "display.txt"
        deadline = time.monotonic() + 7
        while not display_path.stat().st_size:
            if self.xvfb.poll() is not None or time.monotonic() >= deadline:
                raise RuntimeError("Xvfb failed to allocate an isolated display")
            time.sleep(0.05)
        env["DISPLAY"] = f":{display_path.read_text().strip()}"
        self.env = env

    def launch(self):
        self.launch_number += 1
        label = "app" if self.launch_number == 1 else "reopen"
        self.trace = self.out / f"{label}.jsonl"
        self.stderr = self.out / f"{label}.stderr"
        args = [str(self.binary), "--no-synthesizer", "--no-midi", "-D", "96", "-x", "1"]
        if self.experimental:
            args.append("-e")
        args.append(str(self.input))
        (self.out / "snapshot-request").unlink(missing_ok=True)
        with self.trace.open("wb") as stdout, self.stderr.open("wb") as stderr:
            self.app = subprocess.Popen(args, cwd=self.out, env=self.env, stdout=stdout, stderr=stderr)
        self.results["processes"].append({"label": label, "argv": args, "trace": self.trace.name,
                                         "stderr": self.stderr.name, "display": self.env["DISPLAY"]})
        self.write("app_start", argv=args, subprocess=label)
        return self.wait_ready(label)

    def snapshot(self, label, delay=0.12):
        time.sleep(delay)
        self.seq += 1
        requested = f"{self.seq:03d}-{label}"
        temporary = self.out / "snapshot-request-next"
        temporary.write_text(requested, encoding="utf-8")
        temporary.replace(self.out / "snapshot-request")
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            for row in reversed(entries(self.trace)):
                if row.get("label") == requested:
                    self.state = row
                    self.write("snapshot", label=label, probe_seq=row["seq"], subprocess=self.launch_number)
                    return row
            if self.app.poll() is not None:
                raise RuntimeError(f"app exited {self.app.returncode} while waiting for {label}")
            time.sleep(0.04)
        raise RuntimeError(f"timeout waiting for {label}")

    def shell(self, args):
        subprocess.run(args, env=self.env, cwd=self.out, check=True, timeout=10)

    def key(self, key, intent):
        self.write("keyboard_x11", key=key, intent=intent)
        self.shell(["xdotool", "key", "--clearmodifiers", key])

    def click(self, target, intent, modifier=None):
        left, top, width, height = target["rect"]
        x, y = left + width // 2, top + height // 2
        if width <= 0 or height <= 0 or not 0 <= x < 1280 or not 0 <= y < 900:
            raise ValueError(f"off-screen or empty target for {intent}: {target}")
        if not target["enabled"]:
            raise ValueError(f"disabled target for {intent}: {target}")
        self.write("mouse_x11", x=x, y=y, rect=target["rect"], modifier=modifier, intent=intent,
                   text=target.get("text"), probe_seq=self.state.get("seq"))
        if modifier:
            self.shell(["xdotool", "mousemove", str(x), str(y), "keydown", modifier, "click", "1", "keyup", modifier])
        else:
            self.shell(["xdotool", "mousemove", str(x), str(y), "click", "1"])

    def widget(self, kind, text=None, action=None):
        found = [row for row in self.state["widgets"] if matches_widget(row, kind, text, action)]
        if len(found) != 1:
            raise ValueError(f"expected one widget for {kind}/{text}/{action}, found {len(found)}")
        return found[0]

    def click_widget(self, kind, text=None, action=None):
        self.click(self.widget(kind, text, action), f"{kind}:{text or action}")

    def score_object(self, kind, track, pitch=None, modifier=None):
        item = find_object(active_score(self.state), kind, track, pitch)
        geometry = next(row for row in self.state["objects_on_screen"] if row["id"] == item["id"])
        self.click(geometry, f"{item['type']} track={track} pitch={pitch}", modifier)

    def screen(self, label, move_pointer=True):
        if move_pointer:
            self.shell(["xdotool", "mousemove", "1150", "830"])
        time.sleep(0.08)
        output = self.out / f"{label}.png"
        self.shell(["import", "-window", "root", str(output)])
        self.write("screenshot", label=label, file=output.name, sha256=sha256(output),
                   probe_seq=self.state.get("seq"))

    def wait_ready(self, label):
        for _ in range(16):
            state = self.snapshot(f"{label}_startup")
            dialogs = [row["text"] for row in state["widgets"] if row["kind"] == "dialog"]
            if dialogs == ["Startup Wizard"]:
                self.click_widget("button", "Cancel")
            elif dialogs == ["Tour"]:
                choice = self.widget("button", "Continue showing tours")
                self.click({**choice, "rect": [choice["rect"][0], choice["rect"][1], 16, choice["rect"][3]]},
                           "disable welcome tours via its checkbox")
                self.click_widget("button", "Close")
            elif state["active_score_id"] and not dialogs:
                windows = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^MuseScore 3"],
                                         env=self.env, cwd=self.out, text=True, check=True, capture_output=True).stdout.split()
                if len(windows) != 1:
                    raise ValueError(f"expected one MuseScore main window, found {windows}")
                self.shell(["xdotool", "windowfocus", "--sync", windows[0]])
                self.write("x11_focus", window=windows[0])
                return self.snapshot("reopened" if self.launch_number > 1 else "ready")
            else:
                time.sleep(0.25)
        raise RuntimeError(f"startup blocked by {dialogs!r}")

    def switch_layer(self, name):
        self.click_widget("layer_combo")
        self.snapshot(f"layer_{name}_popup")
        self.widget("layer_choice", name)
        if name == "hidden":
            self.key("End", "Navigate to the hidden layer in the open native combo")
        else:
            self.key("Home", "Navigate to the first layer in the open native combo")
            self.key("Down", "Navigate to the shown layer")
        self.key("Return", f"Activate layer {name}")
        state = self.snapshot(f"layer_{name}")
        if (name == "shown" and active_score(state)["layer_mask"] != 3
                or name == "hidden" and active_score(state)["layer_mask"] != 1):
            raise ValueError(f"{name} layer selection did not apply")
        return state

    def wait_quit(self):
        self.app.wait(timeout=8)
        process = self.results["processes"][-1]
        process["exit_code"] = self.app.returncode
        self.write("app_exit", exit=self.app.returncode)
        if self.app.returncode:
            raise RuntimeError(f"app exited {self.app.returncode}")

    def quit(self):
        self.key("ctrl+q", "Quit after smoke or save")
        self.wait_quit()

    def close(self):
        if self.app and self.app.poll() is None:
            self.app.terminate()
            try:
                self.app.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.app.kill()
                self.app.wait(timeout=2)
        if self.app and self.results["processes"] and "exit_code" not in self.results["processes"][-1]:
            self.results["processes"][-1]["exit_code"] = self.app.returncode
        if self.xvfb and self.xvfb.poll() is None:
            self.xvfb.terminate()
            self.xvfb.wait(timeout=4)
        self.results["end_utc"] = utc()
        if self.out.exists():
            (self.out / "result.json").write_text(json.dumps(self.results, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8")


def action_count(session, name):
    return sum(row.get("event") == "score_action" and row.get("action") == name for row in entries(session.trace))


def check(session, key, value):
    session.results.setdefault("checks", {})[key] = value


def explode(session, case):
    session.score_object("Note", 0, 60)
    session.snapshot("source_selected")
    session.score_object("Rest", 4, modifier="Shift_L")
    state = session.snapshot("before_menu")
    selection = active_score(state)["selection"]
    valid = (selection["mode"], selection["staff_start"], selection["staff_end"],
             selection.get("tick_start"), selection.get("tick_end")) == ("RANGE", 0, 2, 0, 1920)
    check(session, "requested_range", valid)
    if not valid:
        raise ValueError(f"unexpected input range {selection}")
    session.screen("01-before-menu")
    session.click_widget("menu", "Tools")
    session.snapshot("tools_open")
    session.screen("02-menu", move_pointer=False)
    session.click_widget("action", action="explode")
    state = session.snapshot("menu_ended")
    session.screen("03-menu-ended")
    check(session, "entered_expected_menu", action_count(session, "explode") == 1)
    moved_pitch = 64 if case == "X1" else 60
    find_object(active_score(state), "Note", 4, moved_pitch)
    return "6", "pad-note-2", "Note", moved_pitch, 4


def create_part(session, case):
    session.score_object("Fingering", 0, 60)
    state = session.snapshot("source_selected")
    source_child = find_object(active_score(state), "Fingering", 0, 60)
    check(session, "source_selected", source_child["flag"] and source_child["member"] and source_child["tag_valid"])
    if case == "X3":
        state = session.switch_layer("hidden")
    state = session.snapshot("before_menu")
    source = find_object(active_score(state), "Fingering", 0, 60)
    check(session, "requested_tag_state", source["tag"] == 2 and source["flag"] and source["member"]
          and source["tag_valid"] == (case == "X4"))
    session.screen("01-before-menu")
    session.click_widget("menu", "File")
    session.snapshot("file_open")
    session.click_widget("action", text="Parts…")
    session.snapshot("parts_open", delay=0.3)
    session.screen("02-menu", move_pointer=False)
    session.click_widget("button", "New All")
    session.snapshot("parts_prepared")
    session.click_widget("button", "OK")
    session.snapshot("menu_ended", delay=0.35)
    session.click_widget("tab", "Flute")
    state = session.snapshot("flute_first_view")
    check(session, "entered_expected_menu", any(row["event"] == "excerpt_enter" for row in entries(session.trace)))
    session.screen("03-menu-ended")
    if case == "X3":
        state = session.switch_layer("shown")
    else:
        state = session.snapshot("layer_shown")
    check(session, "flute_tab", active_score(state)["title"] == "Flute")
    session.screen("04-shown")
    # Both conditions use the same tab-only focus transfer. A combo popup leaves key focus on itself.
    before_focus = find_object(active_score(state), "Fingering", 0, 60)
    master_name = next(score["title"] for score in state["scores"] if score["master"])
    master_tabs = [widget for widget in state["widgets"] if widget["kind"] == "tab"
                   and widget["text"].replace("&", "").rstrip("*") == master_name]
    part_bar_y = session.widget("tab", "Flute")["rect"][1]
    master_tab = next(widget for widget in master_tabs if widget["rect"][1] == part_bar_y)
    session.click(master_tab, "Return focus through the master tab without selecting a score element")
    session.snapshot("focus_master_tab")
    session.click_widget("tab", "Flute")
    state = session.snapshot("focus_flute_tab")
    focus_target = find_object(active_score(state), "Fingering", 0, 60)
    check(session, "document_focused", state["focus_class"] == "Ms::ScoreView")
    check(session, "focus_transfer_preserved", focus_target == before_focus)
    return "v", "toggle-visible", "Fingering", 60, 0


def next_edit(session, case, edit, command, kind, pitch, track):
    before = session.snapshot("next_edit_before")
    previous_count = action_count(session, command)
    session.key(edit, f"Primary {case} action with no new score click")
    after = session.snapshot("next_edit_after")
    check(session, "primary_edit_dispatched", action_count(session, command) == previous_count + 1)
    session.screen("05-after-next-edit")
    change = active_score(after)["undo_index"] > active_score(before)["undo_index"]
    check(session, "primary_undo_executed", change)
    if change:
        session.key("ctrl+z", "Undo primary edit")
    session.snapshot("primary_undo_boundary")
    session.key("ctrl+s", "Save the primary path before any reselection")
    session.snapshot("primary_saved")
    session.results["saved_sha256"] = sha256(session.input)
    if session.results["saved_sha256"] == session.results["input_sha256"]:
        raise ValueError("the primary save produced unchanged input bytes")

    # This coordinate is an explicit new selection and starts a distinct condition.
    session.score_object(kind, track, pitch)
    before = session.snapshot("reselected_edit_before")
    child = find_object(active_score(before), kind, track, pitch)
    check(session, "reselected_target", child["member"] and child["flag"])
    previous_count = action_count(session, command)
    session.key(edit, f"Separate {case}-R action after explicit target click")
    after = session.snapshot("reselected_edit_after")
    check(session, "reselected_edit_dispatched", action_count(session, command) == previous_count + 1)
    if active_score(after)["undo_index"] > active_score(before)["undo_index"]:
        session.key("ctrl+z", "Undo the separate reselected edit")
    session.snapshot("reselected_undo_after")
    session.screen("06-after-undo")


def roundtrip(session):
    if sha256(session.input) != session.results["saved_sha256"]:
        raise ValueError("the separate control modified the saved primary input")
    session.quit()
    session.launch()
    if session.experimental:
        session.click_widget("tab", "Flute")
        session.snapshot("reopened_flute")
    session.screen("07-reopened")
    session.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--case", required=True, choices=["smoke", "X1", "X2", "X3", "X4"])
    args = parser.parse_args()
    session = Session(args.binary.resolve(), args.fixture.resolve(), args.out.resolve(), args.case in ("X3", "X4"))
    session.results["case"] = args.case
    try:
        session.init_display()
        session.launch()
        if args.case == "smoke":
            session.screen("smoke-ready")
            session.quit()
        else:
            targets = explode(session, args.case) if args.case in ("X1", "X2") else create_part(session, args.case)
            next_edit(session, args.case, *targets)
            roundtrip(session)
        session.results["run_exit"] = 0
        return 0
    except (OSError, RuntimeError, ValueError, StopIteration, subprocess.SubprocessError) as error:
        session.results["error"] = f"{type(error).__name__}: {error}"
        session.results["run_exit"] = 1
        session.write("failed", error=session.results["error"])
        if session.app and session.app.poll() is None:
            try:
                session.screen("failure", move_pointer=False)
            except (OSError, subprocess.SubprocessError):
                pass
        print(session.results["error"])
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
