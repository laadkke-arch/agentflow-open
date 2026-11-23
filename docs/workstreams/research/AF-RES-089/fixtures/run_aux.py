#!/usr/bin/env python3
"""Run the Q6 cases on the same display after fixing the primary results."""
import argparse
from pathlib import Path
import subprocess
import sys

from run import exercise, prepare_selection, read_driver, session_type
from visibility import index, selected, visible_changes


def prepare_aux(app, case, voice1):
    if case == "VV":
        prepare_selection(app, "P")
        initial = app.snapshot("equal_value_reference")
        app.key("v", "First V of the two-edit value/undo contrast")
        first = app.snapshot("after_first_v")
        if not visible_changes(initial, first) or index(first) != index(initial) + 1:
            raise ValueError("First V of the contrast produced no distinct edit")
        return
    if case == "PEER":
        app.score_object("Note", 8, 67)
        app.snapshot("peer_single", delay=0.5)
        app.score_object("Note", 8, 67, modifier="Shift_L")
        state = app.snapshot("peer_range")
        selection = selected(state)
        if selection["mode"] != "RANGE" or selection["list"] != ["M:8:0:Note:67"]:
            raise ValueError(f"Unexpected peer range: {selection}")
        return
    app.key("F6", "Open Selection Filter")
    app.snapshot("filter_open")
    app.screen("00-filter-before", move_pointer=False)
    x, y = voice1
    app.click({"rect": [x, y, 1, 1], "enabled": True, "text": "Voice 1 checkbox"},
              "Uncheck only Voice 1")
    app.snapshot("filter_changed")
    app.screen("00-filter-voice-1-off", move_pointer=False)
    prepare_selection(app, "X1" if case == "F-X" else "P")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--af085", type=Path, required=True)
    parser.add_argument("--bin", type=Path, required=True, dest="bins")
    parser.add_argument("--display", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--voice1", type=int, nargs=2, required=True, metavar=("X", "Y"))
    parser.add_argument("--only", choices=("F-P", "F-X", "PEER", "VV"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    driver = read_driver(args.af085.resolve())
    factory = session_type(driver, args.display)
    here = Path(__file__).resolve().parent
    failures = 0
    cases = (args.only,) if args.only else ("F-P", "F-X", "PEER", "VV")
    for case in cases:
        fixture = here / ("x2.mscx" if case in {"PEER", "VV"} else "x1.mscx")
        for build in "GL":
            ident = f"{case}-{build}"
            app = factory(args.bins.resolve() / f"mscore-{build}", fixture, args.out.resolve() / ident)
            if app.out.exists():
                raise FileExistsError(f"Preserve the existing attempt at {app.out}")
            app.results.update(run_id=ident, case=case, build=build, repeat=1,
                               runner_argv=[sys.executable, "-B", *sys.argv])
            try:
                exercise(app, {"case": case}, driver, factory,
                         prepare=lambda session, kind: prepare_aux(session, kind, args.voice1))
                app.results["run_exit"] = 0
                print(ident, app.results["selection"]["before"]["mode"], app.results["changed"],
                      app.results["undo_index"], flush=True)
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
