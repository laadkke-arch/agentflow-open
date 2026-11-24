"""Build the locked PCM input and calibration fixtures. This never writes DAW exports."""

import hashlib
import json
import math
import struct
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RATE = 44_100
TONES = {
    "A": (440, [6000, 7200, 8400, 9600, 10800]),
    "B": (880, [4000, 4800, 5600, 6400, 7200]),
}
LABELS = {
    "L": [["L13", 1, 3], ["L35", 3, 5]],
    "K": [["K24", 2, 4]],
}
CONDITIONS = {
    "base": {"order": ["A", "L", "B", "K"], "muted": []},
    "move-b": {"order": ["A", "B", "L", "K"], "muted": []},
    "mute-b": {"order": ["A", "L", "B", "K"], "muted": ["B"]},
    "swap-labels": {"order": ["A", "K", "B", "L"], "muted": []},
}


def tone(frequency, amplitudes):
    cycle = [math.sin(math.tau * frequency * index / RATE) for index in range(RATE)]
    return [round(amplitude * value) for amplitude in amplitudes for value in cycle]


def write_pcm(name, samples):
    path = ROOT / f"{name}.wav"
    pcm = struct.pack(f"<{len(samples)}h", *samples)
    with wave.open(str(path), "wb") as target:
        target.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        target.writeframes(pcm)
    return {
        "path": f"fixtures/{path.name}",
        "frames": len(samples),
        "wav_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "pcm_sha256": hashlib.sha256(pcm).hexdigest(),
    }


def main():
    a = tone(*TONES["A"])
    b = tone(*TONES["B"])
    waves = {
        "A": a,
        "B": b,
        "AB-calibration": [left + right for left, right in zip(a, b, strict=True)],
        "Silence": [0] * len(a),
    }
    manifest = {
        "rate_hz": RATE,
        "channels": 1,
        "sample_width_bytes": 2,
        "project_span_seconds": [0, 5],
        "project_rate_hz": RATE,
        "tone_frequencies_hz": {name: value[0] for name, value in TONES.items()},
        "peak_lsb_by_project_second": {name: value[1] for name, value in TONES.items()},
        "gain_db": 0,
        "pan": "center",
        "effect_chain": [],
        "solo": [],
        "labels": {},
        "conditions": CONDITIONS,
        "versions": {
            "3.4.2": "9dd60f25c6cd271879756ea57fd67e582fe17d91",
            "3.5.0": "54275321175a6d796953e4bb47bfb6775535d276",
        },
        "waves": {name: write_pcm(name, samples) for name, samples in waves.items()},
    }
    for name, labels in LABELS.items():
        path = ROOT / f"{name}.txt"
        path.write_text(
            "".join(f"{start:.6f}\t{end:.6f}\t{label}\n" for label, start, end in labels),
            encoding="utf-8",
        )
        manifest["labels"][name] = {
            "regions": labels,
            "path": f"fixtures/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    (ROOT.parent / "inputs.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
