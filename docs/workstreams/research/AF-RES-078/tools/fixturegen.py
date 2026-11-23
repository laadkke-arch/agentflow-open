"""Construct controlled fixtures without either conversion pipeline."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import secrets
import sqlite3
import struct
import zlib

OWNED = Path(__file__).resolve().parents[1]
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
CASES_T = ("keys", "rows", "null", "empty", "literal", "comma", "quote", "newline", "text")
CASES_I = ("names", "one_each", "members", "extract", "size", "orientation")
CELLS = {domain: tuple(domain + pair for pair in ("00", "01", "10", "11")) for domain in "TI"}


def json_text(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def json_lines(rows):
    return "".join(json_text(row) + "\n" for row in rows)


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def csv_fixture(name, edge=None):
    """Represent SQL values as JSON values, with type checks made separately."""
    rows = [
        ("null", None), ("empty", ""), ("literal", "NULL"), ("comma", "a,b"),
        ("quote", 'a "quote"'), ("newline", "first\r\nsecond\nlast"),
        ("text", "한글 café"), ("text", " Other "),
    ]
    keys = [f"r{i:02d}" for i in range(1, 9)]
    if edge is not None:
        rng = random.Random(edge)
        keys = [f"e{i:02d}-{rng.randrange(1000, 9999)}" for i in range(1, 9)]
        punctuation = ["x, y", '""inside""', "next\rbare\nlast"]
        rows[3:6] = list(zip(("comma", "quote", "newline"), punctuation))
        suffix = str(rng.randrange(1000, 9999))
        examples = ["Ω" + suffix, "行" + ("\0" if rng.randrange(3) else ":") + suffix]
        rows[6:] = [("text", value) for value in examples]
        rng.shuffle(keys)
    return {"id": name, "domain": "T", "rows": [
        {"key": key, "role": role, "type": "null" if content is None else "text", "value": content}
        for key, (role, content) in zip(keys, rows)
    ]}


def image_fixture(name, edge=None):
    rng = random.Random(edge if edge is not None else 7800)
    folders = ["a", "b"]
    flags = [1, 6]
    if edge is not None:
        stem = rng.choice(("한글", "café", "e\u0301", "スカイ"))
        folders = [f"a/{stem} {rng.randrange(100, 1000)}", f"b/{rng.randrange(100, 1000)}"]
        flags = [rng.choice((2, 5, 7)), rng.choice((3, 4, 8))]
    images = []
    colors = rng.sample(range(24, 238), 8)
    for index, (folder, flag) in enumerate(zip(folders, flags)):
        corners = [[value, (value * 3) % 251, (value * 7) % 253] for value in colors[index * 4:index * 4 + 4]]
        images.append({"path": folder + "/photo.png", "size": [7 + index * 2, 5 + index],
                       "corners": corners, "tag": flag, "background": [12 + index, 43, 75]})
    return {"id": name, "domain": "I", "images": images}


def fixtures(phase, seeds=None):
    if phase == "edge":
        return [csv_fixture("t-edge", seeds["T"]), image_fixture("i-edge", seeds["I"])]
    t, i = csv_fixture("t-normal"), image_fixture("i-normal")
    old_t = {"id": "t-old", "domain": "T", "rows": [
        {"key": "old-cert", "role": "text", "type": "text", "value": "previous release"}
    ]}
    old_i = image_fixture("i-old", 1940)
    for path, image in zip(("a/photo.png", "old/previous.png"), old_i["images"]):
        image["path"] = path
    empty_t = {"id": "t-empty", "domain": "T", "rows": []}
    has_nul = csv_fixture("t-nul")
    has_nul["rows"][-1]["value"] = "prefix\0suffix"
    return [t, i, old_t, old_i, empty_t, has_nul]


def make_database(path, fixture):
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE work(row_key TEXT PRIMARY KEY NOT NULL, cell TEXT)")
        db.executemany("INSERT INTO work VALUES (?, ?)", [(r["key"], r["value"]) for r in fixture["rows"]])


def png_chunk(name, payload):
    return struct.pack(">I", len(payload)) + name + payload + struct.pack(">I", zlib.crc32(name + payload))


def make_png(image, rgb=False):
    width, height = image["size"]
    channels = 3 if rgb else 4
    data = bytearray()
    for y in range(height):
        data.append(0)
        for x in range(width):
            pixel = image["background"]
            if x in (0, width - 1) and y in (0, height - 1):
                pixel = image["corners"][2 * (y > 0) + (x > 0)]
            data.extend(pixel + ([255] if channels == 4 else []))
    header = struct.pack(">IIBBBBB", width, height, 8, 2 if rgb else 6, 0, 0, 0)
    tag = image["tag"]
    metadata = b""
    if tag is not None:
        tiff = struct.pack("<2sHIH", b"II", 42, 8, 1)
        # An IFD entry has a SHORT type, count of one and inline SHORT value.
        tiff += struct.pack("<HHIHHI", 0x0112, 3, 1, tag, 0, 0)
        metadata = png_chunk(b"eXIf", tiff)
    return PNG_HEADER + png_chunk(b"IHDR", header) + metadata + png_chunk(b"IDAT", zlib.compress(data)) + png_chunk(b"IEND", b"")


def write_originals(directory, fixture):
    directory.mkdir(parents=True, exist_ok=True)
    for image in fixture["images"]:
        path = directory / image["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(make_png(image))


def seal(vault):
    vault.mkdir(mode=0o700)
    commits = {}
    for domain in "TI":
        content = secrets.token_hex(16)
        (vault / domain).write_text(content, encoding="ascii")
        commits[domain] = digest(content.encode("ascii"))
    artifact = {
        "sealed_utc": utc(), "actor": "AF-RES-078 / codex-cloud",
        "encoding": "SHA-256 of lowercase seed hex ASCII without a newline, 128 bits per field",
        "commitments": commits,
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "oracle_sha256": digest((OWNED / "tools/oracle.py").read_bytes()),
        "prior_exposure": "Writer knows generator, scoring rules, input classes, upstream docs and failed cases. No resolved held-out seed, concrete fixture, or resulting file was shown before C freeze.",
    }
    (OWNED / "evidence/seed-seal.json").write_text(json_text(artifact) + "\n", encoding="utf-8")


def reveal(vault):
    seal_doc = json.loads((OWNED / "evidence/seed-seal.json").read_text(encoding="utf-8"))
    hexes = {domain: (vault / domain).read_text(encoding="ascii") for domain in "TI"}
    correction = OWNED / "evidence/oracle-correction-seal.json"
    effective = json.loads(correction.read_text(encoding="utf-8")) if correction.exists() else seal_doc
    for domain, value in hexes.items():
        if digest(value.encode("ascii")) != seal_doc["commitments"][domain]:
            raise ValueError(f"Seed commitment mismatch: {domain}")
    if digest(Path(__file__).read_bytes()) != effective["generator_sha256"]:
        raise ValueError("Fixture code changed after commitment")
    if digest((OWNED / "tools/oracle.py").read_bytes()) != effective["oracle_sha256"]:
        raise ValueError("Oracle code changed after commitment")
    (OWNED / "evidence/seed-reveal.json").write_text(json_text({"revealed_utc": utc(), "hex": hexes}) + "\n", encoding="utf-8")
    return {domain: int(value, 16) for domain, value in hexes.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["seal", "main", "reveal"])
    parser.add_argument("--vault", type=Path)
    args = parser.parse_args()
    if args.action == "seal":
        seal(args.vault)
        return
    rows = fixtures("main")
    if args.action == "reveal":
        rows += fixtures("edge", reveal(args.vault))
    (OWNED / "fixtures.jsonl").write_text(json_lines(rows), encoding="utf-8")
    for row in rows:
        if row["domain"] == "I":
            write_originals(OWNED / "inputs" / row["id"], row)
        else:
            (OWNED / "inputs" / (row["id"] + ".json")).write_text(json_text(row) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
