"""Independently inspect the two interchange formats and the required meaning."""

from __future__ import annotations

from collections import Counter
from io import BytesIO
import json
from pathlib import Path
import re
import sqlite3
import struct
from zipfile import BadZipFile, ZipFile
import zlib

from fixturegen import CASES_I, CASES_T, PNG_HEADER, digest

CSV_FIELD = re.compile(rb'(?:"((?:[^"]|"")*)"|([^",\r\n]*))(,|\r\n|\r|\n|\Z)')
DISPLAY = {
    None: (0, 1, 2, 3),
    1: (0, 1, 2, 3), 2: (1, 0, 3, 2), 3: (3, 2, 1, 0), 4: (2, 3, 0, 1),
    5: (0, 2, 1, 3), 6: (2, 0, 3, 1), 7: (3, 1, 2, 0), 8: (1, 3, 0, 2),
}


def source_table(path, fixture):
    with sqlite3.connect(path.as_uri() + "?mode=ro", uri=True) as db:
        returnable = list(db.execute("SELECT row_key, cell, typeof(cell) FROM work ORDER BY row_key"))
    authored = sorted((r["key"], r["value"], r["type"]) for r in fixture["rows"])
    if returnable != authored:
        raise ValueError(f"Source DB does not match the fixture: {fixture['id']}")
    return [{"key": k, "value": v, "sql_type": t} for k, v, t in returnable]


def csv_records(data):
    """Expose the producer's lexical quote bit without using CPython csv."""
    offset = 0
    results = []
    row = []
    while offset < len(data):
        match = CSV_FIELD.match(data, offset)
        if match is None or match.end() == offset:
            raise ValueError(f"Unexpected CSV field at byte {offset}")
        quoted, raw, delimiter = match.groups()
        text = raw if quoted is None else quoted.replace(b'""', b'"')
        row.append({"text": text.decode("utf-8"), "quoted": quoted is not None})
        offset = match.end()
        if delimiter != b",":
            results.append(row)
            row = []
    if row:
        results.append(row + [{"text": "", "quoted": False}])
    return results


def csv_middle(data, fixture, typed=False):
    try:
        records = csv_records(data)
    except (UnicodeDecodeError, ValueError) as err:
        return {"error": str(err), "conditions": {c: False for c in CASES_T}}
    header = [f["text"] for f in records[0]] if records else []
    body = records[1:] if header == ["row_key", "cell"] else []
    cells = []
    for row in body:
        if len(row) != 2:
            continue
        field = row[1]
        value = field["text"]
        if typed:
            if value == "N":
                value = None
            elif value.startswith("T"):
                value = bytes.fromhex(value[1:]).decode("utf-8")
        elif value == "" and not field["quoted"]:
            value = None
        cells.append({"key": row[0]["text"], "value": value})
    # Under the fixed experiment protocol only the unquoted-empty spelling
    # carries a NULL bit. A plain NULL token is indistinguishable from TEXT.
    return {"header": header, "fields": records, "conditions": table_conditions(cells, fixture),
            "schema_valid": bool(header) and len(body) == len(cells)}


def table_conditions(rows, fixture):
    if rows is None:
        return {c: False for c in CASES_T}
    expected = fixture["rows"]
    keys = Counter(row["key"] for row in rows)
    values = {row["key"]: row["value"] for row in rows}
    checks = {"keys": keys == Counter(row["key"] for row in expected), "rows": len(rows) == len(expected)}
    for category in CASES_T[2:]:
        candidates = [row for row in expected if row["role"] == category]
        checks[category] = all(
            keys[r["key"]] == 1
            and type(values[r["key"]]) is type(r["value"])
            and values[r["key"]] == r["value"]
            for r in candidates
        )
    return checks


def table_final(data, fixture):
    if data is None:
        return {"rows": None, "conditions": table_conditions(None, fixture)}
    try:
        rows = [json.loads(line) for line in data.decode("utf-8").split("\n") if line]
        for row in rows:
            if set(row) != {"key", "value"} or not isinstance(row["key"], str):
                raise ValueError("Unexpected serialized row schema")
    except (UnicodeError, ValueError) as err:
        return {"rows": None, "error": str(err), "conditions": table_conditions(None, fixture)}
    return {"rows": rows, "conditions": table_conditions(rows, fixture)}


def exif_orientation(data):
    if not data:
        return None
    try:
        endian = {b"II": "<", b"MM": ">"}[data[:2]]
        magic, start = struct.unpack_from(endian + "HI", data, 2)
        if magic != 42:
            raise ValueError("Unexpected TIFF EXIF type")
        count = struct.unpack_from(endian + "H", data, start)[0]
        for index in range(count):
            pos = start + 2 + index * 12
            tag, encoding, number, value = struct.unpack_from(endian + "HHIH", data, pos)
            if tag == 0x0112:
                if encoding != 3 or number != 1:
                    raise ValueError("Expected single SHORT EXIF Orientation")
                return value
    except (KeyError, struct.error) as exc:
        raise ValueError("Invalid test EXIF profile") from exc
    return None


def paeth(left, above, diag):
    ideal = left + above - diag
    return min((left, above, diag), key=lambda v: abs(ideal - v))


def png_info(data):
    """Decode the test subset: 8-bit RGB/RGBA, noninterlaced, all five filters."""
    if not data.startswith(PNG_HEADER):
        raise ValueError("Non-PNG member")
    width, height, stride = 0, 0, 0
    chunks = bytearray()
    exif = None
    offset = len(PNG_HEADER)
    while offset < len(data):
        size, code = struct.unpack_from(">I4s", data, offset)
        payload = data[offset + 8:offset + 8 + size]
        crc = struct.unpack_from(">I", data, offset + size + 8)[0]
        if zlib.crc32(code + payload) != crc:
            raise ValueError("PNG chunk CRC mismatch")
        if code == b"IHDR":
            width, height, depth, color, compress, filt, interlace = struct.unpack(">IIBBBBB", payload)
            if depth != 8 or color not in (2, 6) or compress or filt or interlace:
                raise ValueError("Outside the oracle's PNG subset")
            stride = 3 if color == 2 else 4
        elif code == b"IDAT":
            chunks.extend(payload)
        elif code == b"eXIf":
            exif = payload
        elif code == b"IEND":
            break
        offset += size + 12
    raster = zlib.decompress(chunks)
    pitch = width * stride
    if not width or not height or len(raster) != height * (pitch + 1):
        raise ValueError("Unexpected test raster size")
    previous = bytes(pitch)
    all_rows = []
    for y in range(height):
        start = y * (pitch + 1)
        filter_id = raster[start]
        current = bytearray(raster[start + 1:start + 1 + pitch])
        for index in range(pitch):
            left = current[index - stride] if index >= stride else 0
            diag = previous[index - stride] if index >= stride else 0
            above = previous[index]
            predictors = (0, left, above, (left + above) // 2, paeth(left, above, diag))
            current[index] = (current[index] + predictors[filter_id]) & 255
        all_rows.append(bytes(current))
        previous = current
    corners = [
        list(all_rows[y][x * stride:x * stride + 3])
        for y in (0, height - 1)
        for x in (0, width - 1)
    ]
    return {"size": [width, height], "corners": corners, "tag": exif_orientation(exif),
            "mode": "RGB" if stride == 3 else "RGBA", "raster_sha256": digest(b"".join(all_rows))}


def image_expectation(source, fixture):
    expected = {}
    for row in fixture["images"]:
        raw = png_info((source / row["path"]).read_bytes())
        if [raw[k] for k in ("size", "corners", "tag")] != [row[k] for k in ("size", "corners", "tag")]:
            raise ValueError(f"Source PNG does not match the fixture: {row['path']}")
        width, height = raw["size"]
        order = DISPLAY[raw["tag"]]
        expected[row["path"]] = {
            "source": raw, "size": [height, width] if raw["tag"] in (5, 6, 7, 8) else raw["size"],
            "corners": [raw["corners"][i] for i in order],
        }
    return expected


def png_record(name, payload):
    return {"name": name, "image": png_info(payload), "sha256": digest(payload), "bytes": len(payload)}


def stage_images(root):
    return [png_record(file.relative_to(root).as_posix(), file.read_bytes())
            for file in sorted(root.rglob("*.png")) if file.is_file()]


def zip_unicode_name(info):
    """Recover a valid optional Info-ZIP Unicode Path extra field (0x7075)."""
    raw = info.orig_filename.encode("utf-8" if info.flag_bits & 0x800 else "cp437")
    offset = 0
    while offset + 4 <= len(info.extra):
        tag, size = struct.unpack_from("<HH", info.extra, offset)
        data = info.extra[offset + 4:offset + 4 + size]
        offset += 4 + size
        if tag == 0x7075 and len(data) >= 5 and data[0] == 1:
            if int.from_bytes(data[1:5], "little") == zlib.crc32(raw):
                return raw.hex(), data[5:].decode("utf-8")
    return raw.hex(), info.orig_filename


def zip_members(data, metadata_encoding=None, extract=()):
    if data is None:
        return {"members": [], "accessed_by_name": [], "readable": False}
    try:
        with ZipFile(BytesIO(data), metadata_encoding=metadata_encoding) as z:
            result = []
            for entry in z.infolist():
                with z.open(entry) as opened:
                    body = opened.read()
                record = png_record(entry.filename, body)
                record["legacy_decoded_name"] = entry.orig_filename
                if metadata_encoding is None:
                    record["raw_name_hex"], record["appnote_name"] = zip_unicode_name(entry)
                record.update(flag_bits=entry.flag_bits, crc32=f"{entry.CRC:08x}", zip_time=list(entry.date_time))
                result.append(record)
            access = []
            for name in extract:
                try:
                    access.append({"name": name, "sha256": digest(z.read(name))})
                except KeyError:
                    continue
            return {"members": result, "accessed_by_name": access, "readable": True}
    except (BadZipFile, ValueError, UnicodeError, struct.error, zlib.error) as error:
        return {"members": [], "accessed_by_name": [], "readable": False, "error": str(error)}


def image_conditions(members, expected, accessed=None, name_key="name"):
    names = Counter(row[name_key] for row in members)
    results = {"names": set(names) == set(expected),
               "one_each": all(names[name] == 1 for name in expected),
               "members": len(members) == len(expected), "size": True, "orientation": True}
    identity_to_payloads = {}
    for row in members:
        key = tuple(sorted(map(tuple, row["image"]["corners"])))
        identity_to_payloads.setdefault(key, []).append(row)
    extracted = {record["name"]: record["sha256"] for record in accessed or []}
    results["extract"] = True
    for name, proof in expected.items():
        key = tuple(sorted(map(tuple, proof["corners"])))
        matches = identity_to_payloads.get(key, [])
        if len(matches) != 1:
            for condition in ("size", "orientation", "extract"):
                results[condition] = False
            continue
        match = matches[0]
        results["size"] &= match["image"]["size"] == proof["size"]
        results["orientation"] &= match["image"]["corners"] == proof["corners"]
        if accessed is None:
            results["extract"] &= match[name_key] == name
        else:
            results["extract"] &= extracted.get(name) == match["sha256"]
    return results
