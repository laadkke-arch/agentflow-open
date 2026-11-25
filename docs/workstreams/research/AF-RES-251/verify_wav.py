"""Cross-check the sealed WAV measurements with ffprobe and FFmpeg."""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

import measure


ROOT = Path(__file__).resolve().parent


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_with_ffmpeg(path, channels):
    argv = ["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-f", "s16le", "-"]
    result = subprocess.run(argv, check=False, capture_output=True, timeout=20)
    frame_bytes = 2 * channels
    frames, leftover = divmod(len(result.stdout), frame_bytes)
    return {
        "argv": argv,
        "exit": result.returncode,
        "stderr": result.stderr.decode("utf-8", errors="replace"),
        "stdout_pcm_bytes": len(result.stdout),
        "stdout_pcm_sha256": hashlib.sha256(result.stdout).hexdigest(),
        "decoded_frames": frames,
        "leftover_bytes": leftover,
    }


def probe(path):
    argv = ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_streams", "-of", "json", str(path)]
    result = subprocess.run(argv, check=False, capture_output=True, text=True, timeout=20)
    data = {"argv": argv, "exit": result.returncode, "stderr": result.stderr, "stdout": result.stdout}
    if result.returncode == 0:
        (stream,) = json.loads(result.stdout)["streams"]
        rate = int(stream["sample_rate"])
        frames = int(stream["duration_ts"]) * Fraction(stream["time_base"]) * rate
        data.update(stream=stream, frames_from_duration_ts=frames.numerator if frames.denominator == 1 else str(frames))
    return data


def crosscheck(path, references):
    result = measure.measure(path, references)
    ffprobe = probe(path)
    ffmpeg = decode_with_ffmpeg(path, result["channels"])
    stream = ffprobe.get("stream", {})
    result["ffprobe"] = ffprobe
    result["ffmpeg"] = ffmpeg
    result["decoders_agree"] = (
        ffprobe["exit"] == ffmpeg["exit"] == 0
        and stream.get("codec_name") == result["format"]
        and stream.get("channels") == result["channels"]
        and stream.get("sample_rate") == str(result["rate_hz"])
        and stream.get("bits_per_sample") == 16
        and ffprobe.get("frames_from_duration_ts") == ffmpeg["decoded_frames"] == result["frames"]
        and ffmpeg["leftover_bytes"] == 0
        and ffmpeg["stdout_pcm_sha256"] == result["pcm_sha256"]
    )
    return result


def tools_version(executable):
    return subprocess.check_output([executable, "-version"], text=True, timeout=12).splitlines()[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav_dir", type=Path)
    parser.add_argument("--reference-dir", type=Path, default=ROOT / "fixtures")
    args = parser.parse_args()
    inputs = sorted(args.wav_dir.glob("*.wav"))
    if not inputs:
        parser.error(f"No WAV files under {args.wav_dir}")

    rows = [crosscheck(path, args.reference_dir) for path in inputs]
    verify_exit = int(not all(row["decoders_agree"] for row in rows))
    receipt = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "ffprobe": tools_version("ffprobe"),
        "ffmpeg": tools_version("ffmpeg"),
        "analysis_sha256": {name: fingerprint(ROOT / name) for name in ("measure.py", "verify_wav.py")},
        "reference_sha256": {path.name: fingerprint(path) for path in sorted(args.reference_dir.glob("*.wav"))},
        "verifier_exit": verify_exit,
        "files": rows,
    }
    print(json.dumps(receipt, indent=2))
    return verify_exit


if __name__ == "__main__":
    sys.exit(main())
