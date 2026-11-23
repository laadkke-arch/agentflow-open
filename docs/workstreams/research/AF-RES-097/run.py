"""AF-RES-097 input inspection and independent Pillow process runner."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from io import BytesIO
from itertools import zip_longest
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import traceback
import zlib


HERE = Path(__file__).resolve().parent
VERSIONS = ("8.2.0", "8.3.0", "8.3.1")
CALLS = {"5593": ("default", "rgba"), "5595": ("object", "raw")}
PALETTE_INPUT = {"mode": "P", "size": [100, 100], "index": 1,
                 "palette": [0, 0, 0, 255, 0, 0, 0, 255, 0]}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def paeth(left, above, upper_left):
    estimate = left + above - upper_left
    return min((left, above, upper_left), key=lambda value: abs(estimate - value))


def inspect_png(data):
    """Read indexed, noninterlaced PNG bytes without loading Pillow."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("missing PNG signature")
    chunks, content, offset = [], {}, len(PNG_SIGNATURE)
    while offset < len(data):
        length, kind = struct.unpack_from(">I4s", data, offset)
        end = offset + length + 12
        payload = data[offset + 8:end - 4]
        crc, = struct.unpack_from(">I", data, end - 4)
        if zlib.crc32(kind + payload) != crc:
            raise ValueError(f"CRC mismatch: {kind!r}")
        name = kind.decode("ascii")
        chunks.append({"name": name, "offset": offset, "payload_bytes": length,
                       "crc32": f"{crc:08x}"})
        content.setdefault(name, []).append(payload)
        offset = end
    if chunks[-1]["name"] != "IEND":
        raise ValueError("missing final IEND")
    width, height, depth, color, compression, method, interlace = struct.unpack(
        ">IIBBBBB", content["IHDR"][0]
    )
    if (color, compression, method, interlace) != (3, 0, 0, 0) or depth not in (1, 2, 4, 8):
        raise ValueError("input is outside indexed noninterlaced PNG scope")
    palette = list(content["PLTE"][0])
    transparency = next(iter(content.get("tRNS", [])), None)
    alpha = list(transparency or b"")
    alpha += [255] * (len(palette) // 3 - len(alpha))
    row_bytes = (width * depth + 7) // 8
    raw = zlib.decompress(b"".join(content["IDAT"]))
    if len(raw) != height * (row_bytes + 1):
        raise ValueError("unexpected decompressed size")
    counts = Counter()
    first = {}
    filters = Counter()
    previous = bytearray(row_bytes)
    for y in range(height):
        start = y * (row_bytes + 1)
        predictor = raw[start]
        filters[predictor] += 1
        current = bytearray(raw[start + 1:start + row_bytes + 1])
        for i, byte in enumerate(current):
            left = current[i - 1] if i else 0
            above = previous[i]
            upper_left = previous[i - 1] if i else 0
            estimates = (0, left, above, (left + above) // 2, paeth(left, above, upper_left))
            current[i] = (byte + estimates[predictor]) & 255
        previous = current
        for x in range(width):
            bit = x * depth
            index = (current[bit // 8] >> (8 - depth - bit % 8)) & ((1 << depth) - 1)
            counts[index] += 1
            first.setdefault(index, [x, y])
    return {
        "sha256": digest(data),
        "bytes": len(data),
        "ihdr": {"width": width, "height": height, "depth": depth, "color_type": color,
                 "compression": compression, "filter_method": method, "interlace": interlace},
        "chunks": chunks,
        "plte": [palette[i:i + 3] for i in range(0, len(palette), 3)],
        "trns": None if transparency is None else list(transparency),
        "alpha_by_index": alpha,
        "counts_by_index": dict(sorted(counts.items())),
        "first_xy_by_index": dict(sorted(first.items())),
        "scanline_filters": dict(sorted(filters.items())),
    }



POST_FIX = "8.4.0"
REJECTED_INPUT = {**PALETTE_INPUT, "mode": "RGB", "index": None, "fill_rgb": [0, 0, 0]}
CALIBRATION_PALETTE = [21, 22, 23, 80, 90, 100, 155, 65, 35]
CALIBRATION_INDICES = [0, 1, 2, 1]
DUPLICATE_PALETTE = [0, 0, 0, 70, 80, 90, 70, 80, 90, 200, 210, 220]
CONTROLS = {
    "no-trns": (CALIBRATION_PALETTE, CALIBRATION_INDICES, None),
    "unused-trns": (CALIBRATION_PALETTE, [1, 2, 1, 2], [0]),
    "used-trns": (CALIBRATION_PALETTE, CALIBRATION_INDICES, [0]),
    "duplicate-a": (DUPLICATE_PALETTE, [1, 2, 3, 1, 2, 3], None),
    "duplicate-b": (DUPLICATE_PALETTE, [2, 1, 3, 2, 1, 3], None),
}
HOPPER_SHA256 = "4c5f7cecc9d468eb37c886840d8f7e7824267e7e315d08751318efddb09a5efb"


def now():
    return datetime.now(timezone.utc).isoformat()


def make_indexed_png(palette, indices, transparency):
    """Build a 1-row, 2-bit PNG independent of the tested writer."""
    packed = bytearray((len(indices) + 3) // 4)
    for x, index in enumerate(indices):
        packed[x // 4] |= index << (6 - 2 * (x % 4))
    parts = [(b"IHDR", struct.pack(">IIBBBBB", len(indices), 1, 2, 3, 0, 0, 0)),
             (b"PLTE", bytes(palette))]
    if transparency is not None:
        parts.append((b"tRNS", bytes(transparency)))
    parts.extend([(b"IDAT", zlib.compress(b"\x00" + packed)), (b"IEND", b"")])
    return PNG_SIGNATURE + b"".join(
        struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))
        for kind, payload in parts
    )


def file_identity(path):
    path = Path(path)
    return {"path": str(path), "realpath": str(path.resolve()), "sha256": digest(path.read_bytes())}


def runtime(PIL, Image, ImagePalette, core, version):
    files = {name: file_identity(module.__file__) for name, module in (
        ("PIL", PIL), ("Image", Image), ("ImagePalette", ImagePalette), ("_imaging", core),
    )}
    if PIL.__version__ != version or core.PILLOW_VERSION != version:
        raise RuntimeError(f"expected {version}; loaded {PIL.__version__}/{core.PILLOW_VERSION}")
    if not all(Path(value["path"]).is_relative_to(sys.prefix) for value in files.values()):
        raise RuntimeError(f"Pillow outside runtime prefix {sys.prefix}")
    return {"pillow": PIL.__version__, "core": core.PILLOW_VERSION, "python": sys.version,
            "executable": sys.executable, "prefix": sys.prefix, "base_prefix": sys.base_prefix,
            "platform": sys.platform, "files": files}


def metadata(image):
    trns = image.info.get("transparency")
    return {"mode": image.mode, "size": image.size,
            "palette_mode": getattr(image.palette, "mode", None),
            "palette_rawmode": getattr(image.palette, "rawmode", None),
            "transparency_kind": type(trns).__name__ if trns is not None else None,
            "transparency": list(trns) if isinstance(trns, bytes) else trns}


def calibrate(Image, transparent, state):
    state["stage"] = "image_write"
    with Image.new("P", (4, 1)) as image:
        image.putpalette(CALIBRATION_PALETTE, rawmode="RGB")
        image.putdata(CALIBRATION_INDICES)
        options = {"transparency": 0} if transparent else {}
        stream = BytesIO()
        image.save(stream, format="PNG", bits=2, **options)
        data = stream.getvalue()
    png = inspect_png(data)
    state["stage"] = "image_open"
    with Image.open(BytesIO(data)) as reopened:
        before = metadata(reopened)
        state["stage"] = "image_load"
        indices = list(reopened.getdata())
        prefix = reopened.getpalette()[:len(CALIBRATION_PALETTE)]
        after = metadata(reopened)
    state["stage"] = "calibration_compare"
    expected_trns = 0 if transparent else None
    if (indices != CALIBRATION_INDICES or prefix != CALIBRATION_PALETTE or before["mode"] != "P"
            or before["transparency"] != expected_trns or png["trns"] != ([0] if transparent else None)):
        raise AssertionError({"indices": indices, "palette_prefix": prefix, "header": before, "png": png})
    return {"png": png, "input_indices": CALIBRATION_INDICES, "reopened_indices": indices,
            "palette_prefix": prefix, "before_load": before, "after_load": after}


def pixels(image, labels, coordinates, indices):
    alpha_channel = "A" in image.getbands()
    points = {}
    for name, xy in coordinates.items():
        color = image.getpixel(tuple(xy))
        points[name] = {"xy": xy, "input_index": indices[name], "rgb": color[:3],
                        "alpha": color[3] if alpha_channel else None}
    data = list(image.getdata())
    if len(data) != len(labels):
        raise ValueError("conversion changed pixel count")
    groups = {}
    for index, value in zip(labels, data):
        groups.setdefault(index, Counter())[value] += 1
    return {**metadata(image), "bands": image.getbands(), "channel_count": len(image.getbands()),
            "points": points, "pixel_bytes_sha256": digest(image.tobytes()),
            "rgb_bytes_sha256": digest(bytes(channel for color in data for channel in color[:3])),
            "alpha_counts": dict(sorted(Counter(color[3] for color in data).items())) if alpha_channel else None,
            "output_by_input_index": {
                index: [{"rgba_or_rgb": pixel, "count": count} for pixel, count in sorted(counts.items())]
                for index, counts in sorted(groups.items())
            }}


def run_convert(Image, data, coordinates, call, state, promote=False):
    state["stage"] = "image_open"
    with Image.open(BytesIO(data)) as target, Image.open(BytesIO(data)) as witness:
        header = metadata(target)
        state["stage"] = "image_load"
        labels = list(witness.getdata())
        indices = {name: witness.getpixel(tuple(xy)) for name, xy in coordinates.items()}
        loaded = metadata(witness)
        state["stage"] = "call"
        converted = target.convert() if call == "default" else target.convert("RGBA")
        with converted:
            state["stage"] = "observe"
            output = pixels(converted, labels, coordinates, indices)
            source_after = {**metadata(target), "indices": {
                name: target.getpixel(tuple(xy)) for name, xy in coordinates.items()
            }, "index_bytes_sha256": digest(target.tobytes())}
            same_indices = source_after["index_bytes_sha256"] == digest(bytes(labels))
            observation = {"input_before_load": header, "same_bytes_witness_after_load": loaded,
                           "input_label_counts": dict(sorted(Counter(labels).items())),
                           "input_label_bytes_sha256": digest(bytes(labels)),
                           "source_after_call": source_after, "source_indices_unchanged": same_indices,
                           "output": output}
            if len(labels) <= 100:
                observation["input_index_selection"] = {
                    index: [x for x, value in enumerate(labels) if value == index]
                    for index in sorted(set(labels))
                }
            if promote:
                with converted.convert("RGBA") as promoted:
                    observation["after_explicit_promotion"] = pixels(promoted, labels, coordinates, indices)
    return observation


def first_difference(actual, expected):
    return next(({"offset_zero_based": offset, "seen": a, "expected": e}
                 for offset, (a, e) in enumerate(zip_longest(actual, expected)) if a != e), None)


def attach_palette(ImagePalette, image, values, call):
    if call == "object":
        palette = ImagePalette.ImagePalette(mode="RGB", palette=values, size=len(values))
        image.putpalette(palette)
    else:
        image.putpalette(values, rawmode="RGB")


def palette_snapshot(image, length):
    palette = image.getpalette()
    with image.convert("RGB") as rgb:
        rgb_pixel = rgb.getpixel((0, 0))
    return {**metadata(image), "palette_prefix": palette[:length], "palette_read_length": len(palette),
            "index_0_0": image.getpixel((0, 0)), "rgb_0_0": rgb_pixel,
            "index_histogram": dict(sorted(Counter(image.getdata()).items()))}


def run_palette(Image, ImagePalette, call, version, state, options):
    values = list(PALETTE_INPUT["palette"])
    history = [0, 255, 0, 0, 0, 255, 0, 0, 0] if version == "8.2.0" and call == "object" else values
    mode = "RGB" if options["reject"] else PALETTE_INPUT["mode"]
    color = (0, 0, 0) if options["reject"] else PALETTE_INPUT["index"]
    with Image.new(mode, tuple(PALETTE_INPUT["size"]), color) as image:
        state["stage"] = "call"
        origin_index = image.getpixel((0, 0))
        try:
            attach_palette(ImagePalette, image, values, call)
        except ValueError as exc:
            if "illegal image mode" in str(exc):
                state["stage"] = "unsupported_call"
            raise
        state["stage"] = "observe"
        before = palette_snapshot(image, len(values))
        result = {"input_palette_after_attach": values, "before_attach_index_0_0": origin_index,
                  "before_save": before,
                  "first_diff_from_goal": first_difference(before["palette_prefix"], PALETTE_INPUT["palette"]),
                  "first_diff_from_reported_trace": first_difference(before["palette_prefix"], history)}
        if options["save"]:
            state["stage"] = "image_write"
            stream = BytesIO()
            image.save(stream, format="PNG")
            data = stream.getvalue()
            png = inspect_png(data)
            state["stage"] = "image_open"
            with Image.open(BytesIO(data)) as reopened:
                state["stage"] = "image_load"
                result["after_png_reopen"] = palette_snapshot(reopened, len(values))
            result["saved_png"] = {"sha256": png["sha256"], "bytes": png["bytes"], "ihdr": png["ihdr"],
                                   "plte_count": len(png["plte"]), "plte_first_three": png["plte"][:3],
                                   "trns": png["trns"]}
            result["first_reopen_palette_difference"] = first_difference(
                result["after_png_reopen"]["palette_prefix"], before["palette_prefix"]
            )
    return result


def sequential(Image, ImagePalette, state):
    state["stage"] = "call"
    p = list(PALETTE_INPUT["palette"])
    with Image.new("P", (100, 100), 1) as image:
        attach_palette(ImagePalette, image, p, "object")
        object_read = image.getpalette()[:len(p)]
        image.putpalette(p)  # The posted call omitted rawmode.
        raw_read = image.getpalette()[:len(p)]
        image.load()
        image.palette.dirty = 1
        dirty_read = image.getpalette()[:len(p)]
        color_queries = []
        for color in ((0, 0, 0), (255, 255, 255)):
            try:
                answer = {"index": image.palette.getcolor(color)}
            except IndexError as exc:
                answer = {"error": type(exc).__name__, "message": str(exc)}
            color_queries.append({"query": color, **answer})
        return {"order": "object → raw(default rawmode) → dirty/load", "object_palette": object_read,
                "raw_palette": raw_read, "dirty_palette": dirty_read,
                "color_queries_after_dirty": color_queries}


def hopper_regression(Image, data, state):
    state["stage"] = "image_open"
    with Image.open(BytesIO(data)) as ppm, ppm.convert("P") as generated, generated.copy() as image:
        state["stage"] = "call"
        labels = list(image.getdata())
        observations = []
        for _ in range(2):
            with image.convert() as converted:
                observations.append({"mode": converted.mode, "size": converted.size})
        image.info["transparency"] = 0
        with image.convert() as converted:
            observations.append({"mode": converted.mode, "size": converted.size,
                                 "alpha_counts": converted.getchannel("A").getcolors() if "A" in converted.getbands() else None})
        return {"input_index_0_count": labels.count(0),
                "conversions": observations,
                "matches_upstream_mode_assertions": [a["mode"] for a in observations] == ["RGB", "RGB", "RGBA"]}


def worker(job):
    state = {"id": job["id"], "stage": "runtime", "process": {"pid": os.getpid(), "started_utc": now()}}
    status = 0
    try:
        import PIL
        from PIL import Image, ImagePalette, _imaging

        state["runtime"] = runtime(PIL, Image, ImagePalette, _imaging, job["version"])
        kind, call = job["kind"], job["call"]
        if kind == "calibration":
            value = calibrate(Image, call == "positive", state)
        elif kind == "hopper":
            state["stage"] = "input_identity"
            data = Path(job["input_path"]).read_bytes()
            if digest(data) != job["input_sha256"]:
                raise ValueError("hopper fixture digest differs")
            value = hopper_regression(Image, data, state)
        elif kind == "sequential":
            value = sequential(Image, ImagePalette, state)
        elif job["case"] == "5595":
            value = run_palette(Image, ImagePalette, call, job["version"], state,
                                {"save": kind == "roundtrip", "reject": kind == "rejected"})
        else:
            state["stage"] = "input_identity"
            data = (make_indexed_png(*CONTROLS[job["fixture"]]) if kind == "control"
                    else Path(job["input_path"]).read_bytes())
            if digest(data) != job["input_sha256"]:
                raise ValueError("input PNG digest differs")
            value = run_convert(Image, data, job["coordinates"], call, state, promote=kind == "promotion")
        state.update(observation=value, stage="observed")
    except Exception as exc:
        state["error"] = {"class": type(exc).__name__, "message": str(exc)}
        traceback.print_exc()
        status = 2
    state["process"]["finished_utc"] = now()
    print(json.dumps(state, ensure_ascii=False, sort_keys=True))
    return status


def make_job(kind, case, version, call, repeat=1, **input_data):
    name = f"{case}-{version}-{call}-{repeat}"
    if kind != "main":
        name = f"{kind}-{input_data.get('fixture', case)}-{version}-{call}-{repeat}"
    return {"id": name, "kind": kind, "case": case, "version": version, "call": call,
            "repeat": repeat, **input_data}


def schedule(suite, input_path, hopper_path):
    if suite == "calibration":
        return [make_job("calibration", "P-PNG", version, call)
                for version in (*VERSIONS, POST_FIX) for call in ("positive", "negative")]
    specs = json.loads((HERE / "inputs.json").read_text())
    original = {"input_path": str(input_path) if input_path else None,
                "input_sha256": specs["5593"]["png"]["sha256"], "coordinates": specs["5593"]["probe_xy"]}
    literal = {"input_sha256": specs["5595"]["sha256"]}
    jobs = [make_job("main", case, version, call, repeat, **(original if case == "5593" else literal))
            for case, calls in CALLS.items() for version in VERSIONS for call in calls for repeat in (1, 2)]
    jobs.extend(make_job("roundtrip", "5595", version, call, **literal)
                for version in VERSIONS for call in CALLS["5595"])
    jobs.extend(make_job("rejected", "5595", version, call,
                         input_sha256=digest(canonical(REJECTED_INPUT)))
                for version in VERSIONS for call in CALLS["5595"])
    jobs.extend(make_job("sequential", "5595", version, "object-then-raw", **literal) for version in VERSIONS[:2])
    jobs.extend(make_job("promotion", "5593", version, "default", **original) for version in VERSIONS)
    jobs.extend(make_job("postfix", "5593", POST_FIX, call, **original) for call in CALLS["5593"])
    for version in (*VERSIONS, POST_FIX):
        jobs.append(make_job("hopper", "5593", version, "upstream-sequence",
                             input_path=str(hopper_path) if hopper_path else None, input_sha256=HOPPER_SHA256))
    for name, inputs in CONTROLS.items():
        png = inspect_png(make_indexed_png(*inputs))
        coordinates = {f"index_{index}": xy for index, xy in png["first_xy_by_index"].items()}
        jobs.extend(make_job("control", "5593", version, call, fixture=name,
                             coordinates=coordinates, input_sha256=png["sha256"])
                    for version in VERSIONS for call in CALLS["5593"])
    return jobs


def launch(job, env_dir, destination):
    python = env_dir / job["version"] / "bin" / "python"
    command = [str(python), "-I", "-B", str(HERE / "run.py"), "worker", json.dumps(job, sort_keys=True)]
    row = {**job, "command": command, "exit_code": None, "process": None, "observation": None}
    if not python.is_file():
        return {**row, "stage": "not_run_environment", "reason": f"missing {python}"}
    if "input_path" in job and (not job["input_path"] or not Path(job["input_path"]).is_file()):
        return {**row, "stage": "not_run_input", "reason": "required fixed fixture is unavailable"}
    if job["case"] == "5595":
        definition = REJECTED_INPUT if job["kind"] == "rejected" else PALETTE_INPUT
        if digest(canonical(definition)) != job["input_sha256"]:
            return {**row, "stage": "not_run_input", "reason": "canonical literal differs from sealed input"}
    try:
        child = subprocess.run(command, capture_output=True, timeout=60, check=False)
    except subprocess.TimeoutExpired as exc:
        save_streams(row, destination, exc.stdout or b"", exc.stderr or b"")
        return {**row, "stage": "process_timeout", "reason": "child exceeded 60 seconds"}
    except OSError as exc:
        return {**row, "stage": "process_launch_failed", "reason": str(exc)}
    row["exit_code"] = child.returncode
    save_streams(row, destination, child.stdout, child.stderr)
    try:
        payload = json.loads(child.stdout)
    except ValueError:
        return {**row, "stage": "unobservable_output", "reason": "stdout is not one JSON object"}
    if payload["id"] != job["id"]:
        return {**row, "stage": "unobservable_output", "reason": "worker returned a different slot id"}
    return {**row, **payload}


def save_streams(row, destination, stdout, stderr):
    empty = destination / "empty.stderr.txt"
    empty.touch(exist_ok=True)
    for stream, data, suffix in (("stdout", stdout, "stdout.json"), ("stderr", stderr, "stderr.txt")):
        name = f"{row['id']}.{suffix}" if stream == "stdout" or data else empty.name
        (destination / name).write_bytes(data)
        row[f"{stream}_name"] = name
        row[f"{stream}_sha256"] = digest(data)
        row[f"{stream}_bytes"] = len(data)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("png", type=Path)
    child = sub.add_parser("worker")
    child.add_argument("job")
    execute = sub.add_parser("execute")
    execute.add_argument("suite", choices=("calibration", "experiment"))
    execute.add_argument("--env-dir", type=Path, required=True)
    execute.add_argument("--output", type=Path, required=True)
    execute.add_argument("--input", type=Path)
    execute.add_argument("--hopper", type=Path)
    args = parser.parse_args()
    if args.action == "worker":
        return worker(json.loads(args.job))
    if args.action == "inspect":
        print(json.dumps(inspect_png(args.png.read_bytes()), indent=2))
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
    records = schedule(args.suite, args.input, args.hopper)
    with (args.output / "ledger.jsonl").open("w", encoding="utf-8") as ledger:
        for job in records:
            row = launch(job, args.env_dir.resolve(), args.output)
            ledger.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            print(row["id"], row["stage"], row["exit_code"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
