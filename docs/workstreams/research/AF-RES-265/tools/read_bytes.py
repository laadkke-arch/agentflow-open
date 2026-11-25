"""Read pinned GLB/glTF bytes with the Python standard library."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct

from prepare import MODELS

FORMATS = {5120: "b", 5121: "B", 5122: "h", 5123: "H", 5125: "I", 5126: "f"}
WIDTHS = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def glb(data):
    magic, version, size = struct.unpack_from("<4sII", data)
    assert (magic, version, size) == (b"glTF", 2, len(data))
    chunks = []
    cursor = 12
    binary = None
    while cursor < size:
        length, kind_bytes = struct.unpack_from("<I4s", data, cursor)
        start = cursor + 8
        end = start + length
        assert end <= size and length % 4 == 0
        kind = kind_bytes.decode("ascii")
        payload = data[start:end]
        pad = None
        if not chunks:
            assert kind == "JSON"
            decoded = payload.decode("utf-8")
            doc, used = json.JSONDecoder().raw_decode(decoded)
            padding = decoded[used:].encode()
            assert all(x == 0x20 for x in padding)
            pad = padding.hex()
        elif kind == "BIN\0":
            assert len(chunks) == 1
            logical = doc["buffers"][0]["byteLength"]
            binary = payload[:logical]
            padding = payload[logical:]
            assert 0 <= length - logical <= 3 and all(x == 0 for x in padding)
            pad = padding.hex()
        chunks.append({"kind": kind, "header": cursor, "start": start, "end": end,
                       "length": length, "padHex": pad, "sha256": digest(payload)})
        cursor = end
    assert cursor == size and chunks
    return doc, binary, {"magic": magic.decode(), "version": version, "length": size,
                         "headerHex": data[:12].hex(), "chunks": chunks}


def attribute(doc, bufs, index):
    acc = doc["accessors"][index]
    view_index = acc["bufferView"]
    view = doc["bufferViews"][view_index]
    count = acc["count"]
    token = "<" + FORMATS[acc["componentType"]] * WIDTHS[acc["type"]]
    size = struct.calcsize(token)
    stride = view.get("byteStride", size)
    view_offset = view.get("byteOffset", 0)
    acc_offset = acc.get("byteOffset", 0)
    offset = view_offset + acc_offset
    end = offset + (count - 1) * stride + size
    buf = bufs[view["buffer"]]
    assert offset >= view_offset and end <= view_offset + view["byteLength"] <= len(buf)
    elements = [buf[at:at + size] for at in range(offset, end, stride)]
    values = [struct.unpack(token, item) for item in elements]
    columns = list(zip(*values))
    return {"accessor": index, "view": view_index, "buffer": view["buffer"],
            "componentType": acc["componentType"], "type": acc["type"], "count": count,
            "viewOffset": view_offset, "viewLength": view["byteLength"], "accessorOffset": acc_offset,
            "stride": stride, "start": offset, "end": end, "first": values[0], "last": values[-1],
            "min": [min(c) for c in columns], "max": [max(c) for c in columns],
            "declaredMin": acc.get("min"), "declaredMax": acc.get("max"),
            "logicalBytes": count * size, "sha256": digest(b"".join(elements))}


def fmt_image(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        length, name, width, height, depth, color = struct.unpack_from(">I4sIIBB", data, 8)
        assert length == 13 and name == b"IHDR"
        return {"format": "PNG", "size": [width, height], "bitDepth": depth, "colorType": color}
    if data[:12] == b"\xabKTX 20\xbb\r\n\x1a\n":
        vk_format, type_size, width, height, _depth, _layers, _faces, levels, supercomp = struct.unpack_from(
            "<9I", data, 12)
        dfd_start, dfd_len = struct.unpack_from("<2I", data, 48)
        assert dfd_len >= 16 and dfd_start + dfd_len <= len(data)
        model, primaries, transfer, flags = struct.unpack_from("<4B", data, dfd_start + 12)
        return {"format": "KTX2", "size": [width, height], "vkFormat": vk_format, "typeSize": type_size,
                "levelCount": levels, "supercompressionScheme": supercomp,
                "dfd": {"offset": dfd_start, "bytes": dfd_len, "colorModel": model,
                        "primaries": primaries, "transferFunction": transfer, "flags": flags}}
    return {"format": "unknown", "prefix": data[:16].hex()}


def all_uris(value, pointer=""):
    if isinstance(value, dict):
        for key, item in value.items():
            name = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
            if key == "uri":
                yield {"pointer": name, "uri": item}
            yield from all_uris(item, name)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from all_uris(item, f"{pointer}/{i}")


def texture_uses(doc):
    def walk(value, path):
        if isinstance(value, dict):
            for k, v in value.items():
                where = path + "/" + k
                if k.lower().endswith("texture") and isinstance(v, dict) and "index" in v:
                    index = v["index"]
                    texture = doc["textures"][index]
                    yield {"pointer": where, "texture": index, "texCoord": v.get("texCoord", 0),
                           "coreImage": texture.get("source"),
                           "basisImage": texture.get("extensions", {}).get("KHR_texture_basisu", {}).get("source")}
                else:
                    yield from walk(v, where)
    for mat_index, material in enumerate(doc.get("materials", [])):
        yield from walk(material, f"/materials/{mat_index}")


def read_entry(path, manifest):
    data = path.read_bytes()
    assert len(data) == manifest["bytes"] and digest(data) == manifest["sha256"]
    if path.suffix == ".glb":
        doc, binary, header = glb(data)
    else:
        doc, binary, header = json.loads(data), None, None
    bufs = []
    geometry = []
    images = []
    for b in doc["buffers"]:
        payload = (path.parent / b["uri"]).read_bytes() if "uri" in b else binary
        assert payload is not None and len(payload) >= b["byteLength"]
        bufs.append(payload[:b["byteLength"]])
    for mi, mesh in enumerate(doc["meshes"]):
        for pi, p in enumerate(mesh["primitives"]):
            geometry.append({"mesh": mi, "primitive": pi, "material": p.get("material"),
                             "mode": p.get("mode", 4),
                             "POSITION": attribute(doc, bufs, p["attributes"]["POSITION"]),
                             "indices": attribute(doc, bufs, p["indices"])})
    for i, image in enumerate(doc.get("images", [])):
        view_id = image.get("bufferView")
        if view_id is not None:
            view = doc["bufferViews"][view_id]
            start = view.get("byteOffset", 0)
            end = start + view["byteLength"]
            assert end <= len(bufs[view["buffer"]])
            payload = bufs[view["buffer"]][start:end]
            location = {"bufferView": view_id, "buffer": view["buffer"], "start": start, "end": end,
                        "fileStart": header["chunks"][1]["start"] + start, "fileEnd": header["chunks"][1]["start"] + end}
        else:
            payload = (path.parent / image["uri"]).read_bytes()
            location = {"uri": image["uri"]}
        images.append({"image": i, **location, "mimeType": image.get("mimeType"),
                       "bytes": len(payload), "sha256": digest(payload), **fmt_image(payload)})
    buffer_details = []
    for index, buf in enumerate(bufs):
        furthest = max((v.get("byteOffset", 0) + v["byteLength"] for v in doc["bufferViews"]
                        if v["buffer"] == index), default=0)
        assert furthest <= len(buf)
        tail = buf[furthest:]
        buffer_details.append({"bytes": len(buf), "sha256": digest(buf),
                               "maximumViewEnd": furthest, "unreferencedTailBytes": len(tail),
                               "unreferencedTailPrefixHex": tail[:16].hex()})
    return {"path": manifest["path"], "edition": manifest["commit"], "url": manifest["url"],
            "bytes": len(data), "gitBlob": manifest["git_blob"], "sha256": digest(data), "glb": header,
            "buffers": buffer_details, "bufferViews": doc["bufferViews"],
            "extensionsUsed": doc.get("extensionsUsed", []), "extensionsRequired": doc.get("extensionsRequired", []),
            "uris": list(all_uris(doc)), "textureUses": list(texture_uses(doc)), "images": images,
            "geometry": geometry}


def inputs(root):
    manifest = json.loads((root / "input-manifest.json").read_text())
    return [r for r in manifest["files"] if r["group"] == "assets" and r["path"].endswith((".glb", ".gltf"))]


def csv_rows(entries):
    for entry in entries:
        _models, model, variant, _file = entry["path"].split("/")
        assert model in MODELS
        header = entry["glb"] or {}
        chunks = header.get("chunks", [])
        for primitive in entry["geometry"]:
            yield {
                "model": model, "variant": variant, "edition": entry["edition"], "source_url": entry["url"],
                "bytes": entry["bytes"], "git_blob": entry["gitBlob"], "sha256": entry["sha256"],
                "magic": header.get("magic"), "version": header.get("version"),
                "declared_length": header.get("length"), "json_chunk": chunks[0] if chunks else None,
                "bin_chunk": chunks[1] if len(chunks) > 1 else None,
                "buffers": entry["buffers"], "uris": entry["uris"],
                "extensions_required": entry["extensionsRequired"], "texture_uses": entry["textureUses"],
                "images": entry["images"], "mesh": primitive["mesh"], "primitive": primitive["primitive"],
                "material": primitive["material"], "mode": primitive["mode"],
                "position": primitive["POSITION"], "indices": primitive["indices"],
            }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root", type=Path)
    args = cli.parse_args()
    entries = [read_entry(args.root / row["group"] / row["path"], row) for row in inputs(args.root)]
    output = {"parser": "Python struct/JSONDecoder", "finished_utc": datetime.now(timezone.utc).isoformat(),
              "entries": entries}
    (args.root / "python-static.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    rows = list(csv_rows(entries))
    with (args.root / "chunks.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False, separators=(",", ":")) if isinstance(v, (dict, list)) else v
                             for k, v in row.items()})
    print(f"read {len(entries)} serializations, {len(rows)} mesh primitives")


if __name__ == "__main__":
    main()
