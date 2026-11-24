"""Read and measure signed PCM16 WAV files. The analyzer only reads samples."""

import argparse
import hashlib
import json
import math
import struct
import wave
from functools import lru_cache
from pathlib import Path


RATE = 44_100
TONES = (440, 880)
WINDOW_OFFSET = RATE // 4
WINDOW_SIZE = RATE // 2
ABSENT_LSB = 8
PRESENT_LSB = 2000
SILENT_PEAK_LSB = 2
ONSET_LSB = 100
MATCH_MAX_ERROR_LSB = 3


def read_pcm(path):
    with wave.open(str(path), "rb") as reader:
        channels = reader.getnchannels()
        frames = reader.getnframes()
        rate = reader.getframerate()
        if reader.getsampwidth() != 2 or reader.getcomptype() != "NONE":
            raise ValueError(f"{path} is not uncompressed PCM16")
        if rate != RATE:
            raise ValueError(f"{path} has sample rate {rate}; expected {RATE}")
        pcm = reader.readframes(frames)
    if len(pcm) != frames * channels * 2:
        raise ValueError(f"{path} has an incomplete sample payload")
    return frames, channels, pcm


@lru_cache
def kernels(frequency):
    phase = [math.tau * frequency * index / RATE for index in range(WINDOW_SIZE)]
    return tuple(map(math.cos, phase)), tuple(map(math.sin, phase))


def component(samples, frequency):
    cosine, sine = kernels(frequency)
    real = math.fsum(sample * basis for sample, basis in zip(samples, cosine, strict=True))
    imag = math.fsum(sample * basis for sample, basis in zip(samples, sine, strict=True))
    return 2 * math.hypot(real, imag) / WINDOW_SIZE


def tone_status(amplitude):
    if amplitude <= ABSENT_LSB:
        return "absent"
    if amplitude >= PRESENT_LSB:
        return "present"
    return "inconclusive"


def windows(samples):
    observed = []
    for start in range(WINDOW_OFFSET, len(samples) - WINDOW_SIZE + 1, RATE):
        end = start + WINDOW_SIZE
        on_window = samples[start:end]
        amplitudes = {str(tone): component(on_window, tone) for tone in TONES}
        a_440 = amplitudes["440"]
        a_880 = amplitudes["880"]
        observed.append(
            {
                "local_frames": [start, end],
                "peak_lsb": max(map(abs, on_window)),
                "rms_lsb": math.sqrt(math.fsum(x * x for x in on_window) / WINDOW_SIZE),
                "amplitude_lsb": amplitudes,
                "tone": {key: tone_status(value) for key, value in amplitudes.items()},
                "ratio_880_to_440": a_880 / a_440 if a_440 > ABSENT_LSB else None,
            }
        )
    return observed


def reference_matches(samples, reference_dir):
    matches = []
    for name in ("A", "B", "AB-calibration", "Silence"):
        frames, channels, raw = read_pcm(reference_dir / f"{name}.wav")
        if channels != 1:
            raise ValueError(f"Reference {name} is not mono")
        reference = struct.unpack(f"<{frames}h", raw)
        for start in range(0, frames - len(samples) + 1, RATE):
            cut = reference[start : start + len(samples)]
            error = max((abs(a - b) for a, b in zip(samples, cut, strict=True)), default=0)
            matches.append(
                {
                    "reference": name,
                    "source_frames": [start, start + len(samples)],
                    "max_abs_error_lsb": error,
                    "match": error <= MATCH_MAX_ERROR_LSB,
                }
            )
    return matches


def measure(path, reference_dir=None):
    frames, channels, raw = read_pcm(path)
    samples = struct.unpack(f"<{frames * channels}h", raw)
    readings = []
    for channel in range(channels):
        values = samples[channel::channels]
        peak = max(map(abs, values), default=0)
        readings.append(
            {
                "channel": channel,
                "first_samples": values[:8],
                "first_above_100_lsb": next(
                    (index for index, value in enumerate(values) if abs(value) > ONSET_LSB), None
                ),
                "peak_lsb": peak,
                "near_full_scale_samples": sum(value in (-32768, 32767) for value in values),
                "silence_by_peak": peak <= SILENT_PEAK_LSB,
                "windows": windows(values),
            }
        )
    row = {
        "file": path.name,
        "format": "pcm_s16le",
        "rate_hz": RATE,
        "frames": frames,
        "channels": channels,
        "wav_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "pcm_sha256": hashlib.sha256(raw).hexdigest(),
        "measurements": readings,
    }
    if reference_dir is not None and channels == 1:
        row["reference_matches"] = reference_matches(samples, reference_dir)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-dir", type=Path)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps([measure(path, args.reference_dir) for path in args.files], indent=2))


if __name__ == "__main__":
    main()
