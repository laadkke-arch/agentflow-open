"""AF-RES-097 input inspection and independent Pillow process runner."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inspect_png", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect_png(args.inspect_png.read_bytes()), indent=2))


if __name__ == "__main__":
    main()
