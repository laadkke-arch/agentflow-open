"""Summarize observed loader receipts and compute pairwise frame deltas."""
import argparse
import csv
import json
from pathlib import Path

from PIL import Image

from read_bytes import all_uris, glb, texture_uses

DELTA_PAIRS = [
    ("Box-R", "Box-O"), ("BoxTextured-R", "BoxTextured-O"), ("Lamp-R", "Lamp-O"),
    ("Box-O", "BoxTextured-O"), ("Lamp-R", "ktx-on"), ("ktx-on", "fallback-on"),
    ("Lamp-R", "fallback-off"), ("Lamp-R", "ktx-wasm-absent"), ("Lamp-R", "fallback-ktx-absent"),
    ("Lamp-R", "aniso-off"), ("BoxTextured-R", "unused-present"),
    ("unused-present", "unused-absent"), ("unused-absent", "referenced-absent"),
    ("Box-O", "external-present"),
]
GEOMETRY_FIELDS = ("count", "first", "last", "min", "max", "logicalBytes", "sha256")


def write_rows(file, rows):
    with file.open("w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False, separators=(",", ":")) if isinstance(v, (dict,list)) else v
                             for k, v in row.items()})


def frame_diff(first, second):
    a = Image.open(first).convert("RGB").tobytes()
    b = Image.open(second).convert("RGB").tobytes()
    assert len(a) == len(b) == 384 * 384 * 3
    errors = [abs(x - y) for x, y in zip(a, b, strict=True)]
    return {"changed_pixels_ge1": sum(max(errors[i:i + 3]) >= 1 for i in range(0, len(errors), 3)),
            "changed_pixels_ge3": sum(max(errors[i:i + 3]) >= 3 for i in range(0, len(errors), 3)),
            "rgb_mae": sum(errors) / len(errors), "max_channel_delta": max(errors)}


def consistent(expected, meshes):
    if len(expected) != len(meshes):
        return False
    by_key = {(x["mesh"], x["primitive"]): x for x in expected}
    for m in meshes:
        ref = by_key[(m["mesh"], m["primitive"])]
        for attr in ("POSITION", "indices"):
            if any(ref[attr][f] != m[attr][f] for f in GEOMETRY_FIELDS):
                return False
    return True


def summarize(root):
    cases = json.loads((root / "cases.json").read_text())
    static = json.loads((root / "python-static.json").read_text())["entries"]
    by_model = {entry["path"].split("/")[1]: entry["geometry"] for entry in static if entry["glb"]}
    rows = []
    for round_id in (1, 2):
        for case in cases:
            run = json.loads((root / f"round-{round_id}" / f"{case['id']}.json").read_text())
            entry = root / case["paths"][case["entry"]]
            data = entry.read_bytes()
            doc = glb(data)[0] if entry.suffix == ".glb" else json.loads(data)
            outcome = run.get("outcome", {})
            load = outcome.get("load", "미확인")
            draw = outcome.get("draw")
            frame = outcome.get("frame")
            decoded = outcome.get("decode", [])
            model_http = [x for x in run["serverHttp"] if x["category"] == "model"]
            decoder_http = [x for x in run["serverHttp"] if x["category"] == "decoder-runtime"]
            mesh_match = consistent(by_model[case["model"]], outcome["geometry"]) if load=="resolved" else None
            errors = [x for x in [run.get("executionError"), outcome.get("harnessError"), outcome.get("error"),
                                  *run["pageErrors"], *(d.get("error") for d in decoded)] if x]
            degraded = load=="resolved" and any(d.get("error") for d in decoded)
            status = ("정상관측" if load=="resolved" and not degraded else
                      "저하관측" if degraded else "실패관측" if load=="rejected" else "미확인")
            rows.append({
                "case": case["id"], "round": round_id, "model": case["model"], "purpose": case["purpose"],
                "synthetic": case["synthetic"], "change": case["change"], "entry_path": case["paths"][case["entry"]],
                "entry_bytes": case["bytes"], "entry_sha256": case["sha256"], "provided_model_paths": sorted(case["paths"]),
                "declared_uri_count": len(list(all_uris(doc))), "declared_image_count": len(doc.get("images", [])),
                "texture_info_count": len(list(texture_uses(doc))), "extensions_required": doc.get("extensionsRequired", []),
                "ktx2_registered": case["decoder"], "model_http": [{"url": e["url"], "status": e["status"]} for e in model_http],
                "additional_model_requests": sum(e["url"]!=f"/asset/{case['entry']}" for e in model_http),
                "decoder_http": [{"url": e["url"], "status": e["status"]} for e in decoder_http],
                "external_blocked": run["blocked"], "load": load, "callbacks": outcome.get("callbacks", []),
                "geometry_match_glb": mesh_match, "geometry_primitives": len(outcome.get("geometry", [])),
                "decoded_images": len({d["index"] for d in decoded if d.get("decoded")}),
                "attached_textures": len({d["texture"] for d in outcome.get("textureSelections", []) if d.get("bound")}),
                "draw_calls": draw["calls"] if draw else None, "renderer_triangles": draw["triangles"] if draw else None,
                "gl_error": draw["glError"] if draw else None, "foreground": frame["foreground"] if frame else None,
                "mean_rgb": frame["meanRGB"] if frame else None, "rgba256": frame["pixelsSha256"] if frame else None,
                "frame_png_sha256": frame["png"]["sha256"] if frame else None, "errors": errors,
                "console": run["console"], "observation": status, "receipt": f"receipts/round-{round_id}/{case['id']}.json",
            })
    write_rows(root / "runs.csv", rows)

    deltas = []
    for n in (1, 2):
        frame = root / f"round-{n}" / "frames"
        for a, b in DELTA_PAIRS:
            deltas.append({"round": n, "left": a, "right": b, **frame_diff(frame / (a + ".png"), frame / (b + ".png"))})
    write_rows(root / "frame-diffs.csv", deltas)
    print(f"{len(rows)} observations; {len(deltas)} frame contrasts")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("root", type=Path)
    summarize(cli.parse_args().root)


if __name__ == "__main__":
    main()
