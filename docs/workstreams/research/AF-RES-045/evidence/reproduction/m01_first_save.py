"""UNEXECUTED probe plan: M01, Matplotlib3.0.2 and Cartopy0.17.0.

Input: https://github.com/matplotlib/matplotlib/issues/13430
Implementation is independently written; only case-defining API inputs retained.
"""
import argparse
from pathlib import Path
from probe_common import (axis_snapshot, call_step, difference, file_record,
                          load_matplotlib, prepare_output, utc, write_json)


def uniform_scale_png(source, target, scale, axes_bbox):
    # This is an external raster operation, after export. It never changes
    # Matplotlib artists or reflows axes. Affine coordinates enforce the same
    # scalar in x and y without rounding independent resized dimensions.
    from PIL import Image
    import PIL
    with Image.open(str(source)) as opened:
        image = opened.convert("RGBA")
        width, height = image.size
    dx, dy = (1.0 - scale) * width / 2.0, (1.0 - scale) * height / 2.0
    moved = image.transform(
        image.size, Image.AFFINE,
        (1.0 / scale, 0.0, -dx / scale,
         0.0, 1.0 / scale, -dy / scale),
        resample=Image.BICUBIC)
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    Image.alpha_composite(background, moved).save(str(target), dpi=(100, 100))
    x, y, w, h = axes_bbox
    return {
        "operation": "uniform affine scale of whole first PNG, centered on same canvas",
        "pillow": PIL.__version__, "scale": scale, "translation_pixels": [dx, dy],
        "canvas_pixels": [width, height], "resampling": "bicubic",
        "axis_bbox_after_raster_transform_MODEL_pixels":
            [scale*x+dx, scale*y+dy, scale*w, scale*h],
        "model_warning": "Transformed metadata, not independently detected PNG geometry.",
        "source": file_record(source), "result": file_record(target),
        "parameter_status": "scalar and centering are post-seal operationalization",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--scale", type=float, required=True,
                        help="Explicit post-seal B scalar, strictly between0 and1.")
    args = parser.parse_args()
    if not 0.0 < args.scale < 1.0:
        parser.error("--scale must be nonidentity and strictly between0 and1")
    out = prepare_output(args.out)
    mpl, plt, np, environment = load_matplotlib(out, "3.0.2", "0.17.0")
    import cartopy.crs as ccrs
    result = {
        "case": "M01", "environment": environment,
        "original_backend": "Qt on Ubuntu16.04; this probe uses Agg",
        "input_control": "6.4x4.8in,100dpi,empty axes; researcher-fixed historical defaults",
        "normal": "Cartesian", "boundary": "PlateCarree",
        "choice_A": "exactly one explicit canvas.draw before first save",
        "choice_B": "no explicit pre-draw; export first PNG then uniform external scale",
        "reference": "untreated original first and second saves",
        "runs": [],
    }
    for domain in ("cartesian", "platecarree"):
        for choice in ("reference", "A", "B"):
            kwargs = {} if domain == "cartesian" else {"projection": ccrs.PlateCarree()}
            fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=100,
                                   constrained_layout=True, subplot_kw=kwargs)
            label = domain + "-" + choice
            run = {"domain": domain, "choice": choice, "steps": [], "draw_events": []}
            stage = ["created"]
            def on_draw(event):
                run["draw_events"].append({
                    "stage": stage[0], "utc": utc(),
                    "snapshot": axis_snapshot(fig, ax)
                })
            fig.canvas.mpl_connect("draw_event", on_draw)
            if choice == "A":
                stage[0] = "explicit_pre_draw"
                intervention = call_step("explicit_pre_draw", fig.canvas.draw)
                run["steps"].append(intervention)
                if not intervention["ok"]:
                    run["export_status"] = "not attempted: explicit A pre-draw failed"
                    result["runs"].append(run)
                    plt.close(fig)
                    write_json(out / "observations.json", result)
                    continue
            first = out / (label + "-first.png")
            second = out / (label + "-second.png")
            for ordinal, target in (("first", first), ("second", second)):
                stage[0] = ordinal + "_save"
                saved = call_step(stage[0], lambda p=target: fig.savefig(str(p)))
                run["steps"].append(saved)
                if saved["ok"]:
                    run[ordinal] = axis_snapshot(fig, ax)
                    run[ordinal + "_file"] = file_record(target)
                if ordinal == "first" and choice == "B" and saved["ok"]:
                    holder = {}
                    def scale_export():
                        holder.update(uniform_scale_png(
                            first, out / (label + "-first-scaled.png"),
                            args.scale, run["first"]["axes_bbox_pixels"]))
                    run["steps"].append(call_step("external_uniform_scale", scale_export))
                    run["B_raster_step"] = holder
            if "first" in run and "second" in run:
                run["first_minus_second_axis_bbox_pixels"] = difference(
                    run["first"]["axes_bbox_pixels"], run["second"]["axes_bbox_pixels"])
            result["runs"].append(run)
            plt.close(fig)
            write_json(out / "observations.json", result)
    for domain in ("cartesian", "platecarree"):
        group = {r["choice"]: r for r in result["runs"] if r["domain"] == domain}
        reference = group["reference"].get("second")
        if reference and "first" in group["A"]:
            group["A"]["first_minus_reference_second_bbox_pixels"] = difference(
                group["A"]["first"]["axes_bbox_pixels"], reference["axes_bbox_pixels"])
        model = group["B"].get("B_raster_step", {}).get(
            "axis_bbox_after_raster_transform_MODEL_pixels")
        if reference and model:
            group["B"]["raster_MODEL_minus_reference_second_bbox_pixels"] = difference(
                model, reference["axes_bbox_pixels"])
    result["completed_utc"] = utc()
    result["inference_limit"] = (
        "No automatic support/rejection verdict. A success does not test B. "
        "B changes PNG pixels, not internal layout. Compare geometry, not PNG hash equality.")
    write_json(out / "observations.json", result)


if __name__ == "__main__":
    main()

