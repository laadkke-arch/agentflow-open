"""Generate scoped controls and a per-case model-resource allowlist."""
import argparse
import json
from pathlib import Path
import struct

from prepare import MODELS
from read_bytes import digest, glb


def glb_bytes(doc, binary):
    js = json.dumps(doc, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    data = binary + b"\0" * (-len(binary) % 4)
    return (struct.pack("<4sII", b"glTF", 2, 28 + len(js) + len(data)) +
            struct.pack("<I4s", len(js), b"JSON") + js +
            struct.pack("<I4s", len(data), b"BIN\0") + data)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root", type=Path)
    root = cli.parse_args().root
    cases = []

    def source(model, variant):
        return root / "assets" / "Models" / model / variant

    def children(folder):
        return sorted(f for f in folder.iterdir() if f.is_file())

    def case(case_id, model, purpose, entry, files, *, render=True, decoder=False,
             omit_wasm=False, synthetic=False, change="official unchanged bytes"):
        if any(f.name == entry.name and f != entry for f in files):
            raise ValueError("ambiguous entry filename")
        paths = {f.name: str(f.relative_to(root)) for f in [entry, *files]}
        cases.append({"id": case_id, "model": model, "purpose": purpose, "entry": entry.name,
                      "paths": paths, "sha256": digest(entry.read_bytes()), "bytes": entry.stat().st_size,
                      "render": render, "decoder": decoder, "omitWasm": omit_wasm,
                      "synthetic": synthetic, "change": change})

    def synth(folder, name, data):
        target = root / "variants" / folder / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return target

    def json_variant(folder, original, doc):
        return synth(folder, original.name, (json.dumps(doc, indent=2) + "\n").encode())

    for model in MODELS:
        alias = "Lamp" if model == "AnisotropyBarnLamp" else model
        original_glb = source(model, "glTF-Binary") / (model + ".glb")
        split = source(model, "glTF")
        entry = split / (model + ".gltf")
        case(f"{alias}-G", model, "geometry", original_glb, [], render=False)
        case(f"{alias}-R", model, "material", entry, children(split))
        case(f"{alias}-O", model, "offline", original_glb, [])

        geometry_only = json.loads(entry.read_bytes())
        for mesh in geometry_only["meshes"]:
            for primitive in mesh["primitives"]:
                primitive.pop("material", None)
        for field in ("materials", "textures", "images", "samplers", "extensionsUsed", "extensionsRequired"):
            geometry_only.pop(field, None)
        geometry_entry = json_variant(f"geometry-{alias}", entry, geometry_only)
        bin_file = split / geometry_only["buffers"][0]["uri"]
        case(f"{alias}-minimum", model, "control", geometry_entry, [bin_file], render=False, synthetic=True,
             change="geometry-only view of official external glTF, material links removed")

    model = "BoxTextured"
    split = source(model, "glTF")
    entry = split / (model + ".gltf")
    doc = json.loads(entry.read_bytes())
    png = split / doc["images"][0]["uri"]
    buf = split / doc["buffers"][0]["uri"]
    del doc["materials"][0]["pbrMetallicRoughness"]["baseColorTexture"]
    unused = json_variant("texture-declared-unused", entry, doc)
    case("unused-present", model, "control", unused, [buf, png], synthetic=True,
         change="baseColorTexture edge removed, declared image served")
    case("unused-absent", model, "control", unused, [buf], synthetic=True,
         change="same unused JSON, declared image unserved")
    case("referenced-absent", model, "control", entry, [buf],
         change="official BoxTextured split, referenced image unserved")

    model = "Box"
    entry = source(model, "glTF-Binary") / (model + ".glb")
    doc, bin_data, _ = glb(entry.read_bytes())
    prim = doc["meshes"][0]["primitives"][0]
    view = doc["bufferViews"][doc["accessors"][prim["attributes"]["POSITION"]]["bufferView"]]
    # This sample shares the vertex bufferView between POSITION and NORMAL.
    # Move that complete view, leaving indices in the original GLB's BIN chunk.
    start, length = view.get("byteOffset", 0), view["byteLength"]
    external = synth("external-glb", "external.bin", bin_data[start:start + length])
    doc["buffers"].append({"byteLength": length, "uri": external.name})
    view["buffer"] = 1
    view["byteOffset"] = 0
    outside = synth("external-glb", entry.name, glb_bytes(doc, bin_data))
    case("external-present", model, "control", outside, [external], synthetic=True,
         change="GLB first buffer embedded, vertex view moved to relative external.bin")
    case("external-absent", model, "control", outside, [], synthetic=True,
         change="same legal external-URI GLB, external.bin unserved")

    model = "AnisotropyBarnLamp"
    ktx = source(model, "glTF-KTX-BasisU")
    png_files = source(model, "glTF")
    ktx_entry = ktx / (model + ".gltf")
    png_entry = png_files / ktx_entry.name
    case("ktx-on", model, "control", ktx_entry, children(ktx), decoder=True,
         change="official required BasisU, KTX2Loader and JS/WASM available")
    case("ktx-off", model, "control", ktx_entry, children(ktx),
         change="same required BasisU, KTX2Loader unregistered")
    case("ktx-wasm-absent", model, "control", ktx_entry, children(ktx), decoder=True, omit_wasm=True,
         change="same required BasisU with KTX2Loader, decoder WASM unserved")

    doc = json.loads(ktx_entry.read_bytes())
    png_doc = json.loads(png_entry.read_bytes())
    first_png = len(doc["images"])
    png_images = png_doc["images"]
    for texture in doc["textures"]:
        basis_img = doc["images"][texture["extensions"]["KHR_texture_basisu"]["source"]]
        png_index = next(i for i, img in enumerate(png_images)
                         if Path(img["uri"]).stem == Path(basis_img["uri"]).stem)
        texture["source"] = first_png + png_index
    doc["images"].extend(png_images)
    doc["extensionsRequired"].remove("KHR_texture_basisu")
    if not doc["extensionsRequired"]:
        del doc["extensionsRequired"]
    fallback = json_variant("optional-fallback", ktx_entry, doc)
    images = [png_files / image["uri"] for image in png_images]
    bundled = [f for f in children(ktx) if f != ktx_entry] + images
    case("fallback-on", model, "control", fallback, bundled, decoder=True, synthetic=True,
         change="optional BasisU and core PNG source, decoder on")
    case("fallback-off", model, "control", fallback, bundled, synthetic=True,
         change="same optional BasisU/core source, decoder off")
    case("fallback-ktx-absent", model, "control", fallback,
         [f for f in bundled if f.suffix != ".ktx2"], decoder=True, synthetic=True,
         change="same both-source JSON, decoder on but KTX2 model images unserved")

    doc = json.loads(png_entry.read_bytes())
    del doc["materials"][0]["extensions"]["KHR_materials_anisotropy"]
    no_aniso = json_variant("anisotropy-removed", png_entry, doc)
    case("aniso-off", model, "control", no_aniso, [f for f in children(png_files) if f != png_entry], synthetic=True,
         change="only material0 anisotropy extension object removed")
    assert len({c["id"] for c in cases}) == len(cases)
    (root / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
    print(f"{sum(c['purpose']!='control' for c in cases)} primary cases, "
          f"{sum(c['purpose']=='control' for c in cases)} controls")


if __name__ == "__main__":
    main()
