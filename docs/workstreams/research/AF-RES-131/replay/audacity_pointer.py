"""Generate a tone and compare real X11 drags in a disposable Audacity 3 project."""

import argparse
import hashlib
import json
import math
import os
import struct
import subprocess
import time
import wave
from ctypes import CDLL, c_int, c_uint, c_ulong, c_void_p
from pathlib import Path

RATE = 44100
TONE_SECONDS = 4
EPSILON_SECONDS = 0.001


def generate_tone(path):
    with wave.open(str(path), "wb") as stream:
        stream.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        stream.writeframes(b"".join(struct.pack("<h", round(5000 * math.sin(2 * math.pi * 440 * i / RATE)))
                                    for i in range(TONE_SECONDS * RATE)))
    print(json.dumps({"wav": path.name, "seconds": TONE_SECONDS, "frequency_hz": 440,
                      "sample_rate_hz": RATE, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))


class Pipe:
    def __enter__(self):
        to = Path(f"/tmp/audacity_script_pipe.to.{os.getuid()}")
        incoming = Path(f"/tmp/audacity_script_pipe.from.{os.getuid()}")
        assert to.is_fifo() and incoming.is_fifo()
        self.out = to.open("w", encoding="utf-8")
        self.incoming = incoming.open(encoding="utf-8")
        return self

    def __exit__(self, *_):
        self.out.close()
        self.incoming.close()

    def run(self, command, result=False):
        self.out.write(command + "\n")
        self.out.flush()
        parts = []
        while True:
            line = self.incoming.readline()
            if not line:
                raise RuntimeError("Audacity closed the response pipe")
            if line.startswith("BatchCommand finished:"):
                if line.strip() != "BatchCommand finished: OK":
                    raise RuntimeError(f"{command}: {''.join(parts)}{line.strip()}")
                return json.loads("".join(parts)) if result else None
            parts.append(line)


def drag(x, end_x, y):
    lib = CDLL("libX11.so.6")
    mouse = CDLL("libXtst.so.6")
    lib.XOpenDisplay.restype = c_void_p
    lib.XFlush.argtypes = [c_void_p]
    lib.XCloseDisplay.argtypes = [c_void_p]
    mouse.XTestFakeMotionEvent.argtypes = [c_void_p, c_int, c_int, c_int, c_ulong]
    mouse.XTestFakeButtonEvent.argtypes = [c_void_p, c_uint, c_int, c_ulong]
    display = lib.XOpenDisplay(None)
    assert display, "start a dedicated local X11 display"
    try:
        def move(point):
            assert mouse.XTestFakeMotionEvent(display, -1, point, y, 0)
            lib.XFlush(display)
            time.sleep(0.045)

        move(x)
        assert mouse.XTestFakeButtonEvent(display, 1, 1, 0)
        lib.XFlush(display)
        time.sleep(0.09)
        for fraction in range(1, 9):
            move(round(x + (end_x - x) * fraction / 8))
        assert mouse.XTestFakeButtonEvent(display, 1, 0, 0)
        lib.XFlush(display)
        time.sleep(0.25)
    finally:
        lib.XCloseDisplay(display)


def snapshot(pipe):
    clips = pipe.run("GetInfo: Type=Clips", result=True)
    tracks = pipe.run("GetInfo: Type=Tracks", result=True)
    assert len(clips) == len(tracks) == 1
    return {"clip": clips[0], "track": tracks[0]}


def capture(path):
    time.sleep(0.55)  # Allow the Audacity script status window and pending track paint to settle.
    subprocess.run(["import", "-window", "root", str(path)], check=True)
    return {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def settings(pipe):
    pipe.run("SetProject: X=10 Y=86 Width=1180 Height=694")
    pipe.run("FitInWindow:")
    time.sleep(0.15)


def measure(args):
    args.output.mkdir(parents=True, exist_ok=True)
    cases = [("selected-waveform", args.waveform_y, True, False),
             ("selected-clip-handle", args.handle_y, True, True),
             ("unselected-clip-handle", args.handle_y, False, True)]
    with Pipe() as pipe:
        settings(pipe)
        for name, y, selected, should_move in cases:
            pipe.run("Select: Track=0 TrackCount=1 Start=0.3 End=1.2" if selected
                     else "Select: Track=0 TrackCount=1 Start=0 End=0")
            if not selected:
                pipe.run("SelectNone:")
            before = snapshot(pipe)
            assert bool(before["track"]["selected"]) == selected, before
            assert abs(before["clip"]["start"]) <= EPSILON_SECONDS
            pre = capture(args.output / f"{name}-before.png")
            drag(args.x, args.end_x, y)
            after = snapshot(pipe)
            post = capture(args.output / f"{name}-after.png")
            clip_shift = after["clip"]["start"] - before["clip"]["start"]
            duration_before = before["clip"]["end"] - before["clip"]["start"]
            duration_after = after["clip"]["end"] - after["clip"]["start"]
            print(json.dumps({"id": name, "before": before, "after": after,
                              "pointer_root_start": [args.x, y], "pointer_root_end": [args.end_x, y],
                              "clip_shift_s": clip_shift, "clip_duration_before_s": duration_before,
                              "clip_duration_after_s": duration_after, "comparison_epsilon_s": EPSILON_SECONDS,
                              "before_image": pre, "after_image": post}), flush=True)
            assert (clip_shift > EPSILON_SECONDS) == should_move
            assert abs(duration_after - duration_before) <= EPSILON_SECONDS
            if should_move:
                pipe.run("Undo:")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tone", type=Path)
    parser.add_argument("--calibrate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--x", type=int)
    parser.add_argument("--end-x", type=int)
    parser.add_argument("--handle-y", type=int)
    parser.add_argument("--waveform-y", type=int)
    args = parser.parse_args()
    if args.tone:
        generate_tone(args.tone)
    if args.calibrate:
        with Pipe() as pipe:
            settings(pipe)
            pipe.run("Select: Track=0 TrackCount=1 Start=0.3 End=1.2")
            print(json.dumps(snapshot(pipe)))
            print(json.dumps(capture(args.calibrate)))
    if args.output:
        measure(args)


if __name__ == "__main__":
    main()
