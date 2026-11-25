"""Drive Audacity's native form with xdotool on the fixed 1360x1020 X11 display."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
CONDITIONS = ("base", "move-b", "mute-b", "swap-labels")


def now():
    return datetime.now(timezone.utc).isoformat()


class Desktop:
    def __init__(self, xdotool, version):
        self.xdotool = xdotool
        self.version = version
        self.commands = []

    def invoke(self, *args):
        args = [str(arg) for arg in args]
        result = subprocess.run(args, capture_output=True, text=True, check=False, timeout=12)
        self.commands.append(
            {
                "utc": now(),
                "argv": args,
                "exit": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        )
        if result.returncode:
            raise RuntimeError(f"{args!r} returned {result.returncode}: {result.stderr.strip()}")
        return result.stdout.strip()

    def x(self, *args):
        return self.invoke(self.xdotool, *args)

    def key(self, *keys):
        self.x("key", "--clearmodifiers", *keys)

    def click(self, x, y):
        self.x("mousemove", x, y, "click", 1)

    def type(self, value):
        self.x("type", "--clearmodifiers", "--delay", 1, value)

    def title(self):
        return self.x("getactivewindow", "getwindowname")

    def window_geometry(self, window):
        geometry = self.invoke("xwininfo", "-id", window)
        fields = re.findall(r"^\s*(?:Absolute upper-left [XY]|Width|Height):\s+(-?\d+)", geometry, re.M)
        if len(fields) != 4:
            raise RuntimeError(f"No window geometry in xwininfo result: {geometry}")
        return tuple(int(value) for value in fields)

    def wait_title(self, expected, timeout=7):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            title = self.title()
            if expected(title):
                return title
            time.sleep(0.12)
        raise RuntimeError(f"Unexpected active window: {title!r}")

    def shot(self, path):
        self.invoke("import", "-window", "root", "-strip", path)

    def picker(self, path, *, label=False):
        if label:
            self.key("alt+f", "i", "l")
            self.wait_title(lambda title: title.startswith("Select") and "label" in title.lower())
        else:
            self.key("ctrl+shift+i")
            self.wait_title(lambda title: title == "Select one or more files")
        self.key("ctrl+l", "ctrl+a")
        self.type(path)
        self.key("Return")
        title = self.wait_title(lambda title: title in ("A", "Music Import"))
        if title == "A" and self.version == "3.5.0" and path == FIXTURES / "A.wav":
            # The project title can change before Audacity finishes tempo detection.
            deadline = time.monotonic() + 1.5
            while title == "A" and time.monotonic() < deadline:
                time.sleep(0.12)
                title = self.title()
        if title == "Music Import":
            left, top, _, _ = self.window_geometry(self.x("getactivewindow"))
            self.click(left + 284, top + 91)  # No: keep the project in seconds.
            self.wait_title(lambda title: title == "A")
        elif title != "A":
            raise RuntimeError(f"Unexpected post-import window: {title!r}")
        time.sleep(0.18)

    def move_up(self, y):
        self.click(93, y)
        self.key("u")
        time.sleep(0.15)


def run(desktop, version, condition, run_dir):
    run_dir.mkdir(parents=True, exist_ok=False)
    outputs = run_dir / "wav"
    outputs.mkdir()
    b_input = FIXTURES / "B.wav"
    if condition == "silent-b":
        b_input = run_dir / "B.wav"
        b_input.write_bytes((FIXTURES / "Silence.wav").read_bytes())
    paths = (FIXTURES / "A.wav", FIXTURES / "L.txt", b_input, FIXTURES / "K.txt")
    record = {
        "version": version,
        "condition": condition,
        "start_utc": now(),
        "display": os.environ.get("DISPLAY"),
        "inputs": [
            {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths
        ],
    }
    desktop.commands = []
    try:
        desktop.wait_title(lambda title: title == "Audacity")
        for path in paths:
            desktop.picker(path, label=path.suffix == ".txt")
        if condition == "move-b":
            desktop.move_up(403)
        elif condition == "mute-b":
            desktop.click(28, 421)
        elif condition == "swap-labels":
            desktop.move_up(578)
            desktop.move_up(403)
            desktop.move_up(475)

        desktop.key("alt+e", "l", "Return")
        desktop.wait_title(lambda title: title == "Edit Labels")
        desktop.shot(run_dir / "labels.png")
        desktop.key("Escape")
        desktop.wait_title(lambda title: title == "A")
        desktop.click(167, 209)
        desktop.key("Home")
        desktop.x("mousemove", 1030, 875)
        desktop.shot(run_dir / "project.png")

        desktop.key("ctrl+shift+e")
        if version == "3.5.0":
            route = desktop.wait_title(lambda title: title in ("Audacity", "Export Audio"))
            if route == "Audacity":
                chooser = desktop.x("getactivewindow")
                left, top, _, _ = desktop.window_geometry(chooser)
                desktop.shot(run_dir / "local-export-choice.png")
                desktop.click(left + 500, top + 427)
        desktop.wait_title(lambda title: title == "Export Audio")
        settings_window = desktop.x("getactivewindow")
        left, top, _, _ = desktop.window_geometry(settings_window)
        desktop.click(left + 235, top + 63)
        desktop.key("ctrl+a")
        desktop.type(outputs)
        desktop.click(left + 170, top + 336)
        deadline = time.monotonic() + 7
        while True:
            left, top, _, height = desktop.window_geometry(settings_window)
            if height >= 650:
                break
            if time.monotonic() >= deadline:
                raise RuntimeError("Multiple Files did not expand the export dialog")
            time.sleep(0.12)
        desktop.click(left + 16, top + 499)
        desktop.x("mousemove", 1020, 875)
        desktop.shot(run_dir / "export.png")
        desktop.click(left + 490, top + 638)
        title = desktop.wait_title(
            lambda title: title == "Export Audio" and desktop.x("getactivewindow") != settings_window
        )
        record["completion_window"] = title
        desktop.shot(run_dir / "completion.png")
        record["files"] = sorted(path.name for path in outputs.iterdir())
        record["export_completed"] = bool(record["files"])
        if not record["export_completed"]:
            raise RuntimeError(f"Export completion needs inspection: {title!r}, {record['files']!r}")
        desktop.key("Return")
        desktop.wait_title(lambda title: title == "A")
        desktop.key("ctrl+w")
        desktop.wait_title(lambda title: title.startswith("Save changes to "))
        desktop.click(600, 587)
        desktop.wait_title(lambda title: title == "Audacity")
        record["driver_exit"] = 0
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        record["driver_exit"] = 1
        record["error"] = str(error)
        desktop.shot(run_dir / "failure.png")
        raise
    finally:
        record["end_utc"] = now()
        record["commands"] = desktop.commands
        (run_dir / "gui.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", choices=("3.4.2", "3.5.0"))
    parser.add_argument("output_root", type=Path)
    parser.add_argument("run_ids", nargs="+", help="e.g. base-r1, move-b-r2, silent-b-r1")
    parser.add_argument("--xdotool", default="xdotool")
    args = parser.parse_args()
    desktop = Desktop(args.xdotool, args.version)
    for run_id in args.run_ids:
        condition, repetition = run_id.rsplit("-r", 1)
        if condition not in (*CONDITIONS, "silent-b") or not repetition.isdecimal():
            parser.error(f"Unknown run ID {run_id!r}")
        run(desktop, args.version, condition, args.output_root.resolve() / run_id)
        print(now(), args.version, run_id, "complete", flush=True)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        sys.exit(str(error))
