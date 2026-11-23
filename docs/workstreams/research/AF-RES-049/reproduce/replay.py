"""Replay one predeclared panel and record layout, export and PNG ink."""
import argparse
import csv
import hashlib
import io
from pathlib import Path
import platform
import struct
import sys
import tempfile
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parent / "upstream-045"))
from m02_legend import build as build_m02
from m03_colorbar import snapshot as m03_snapshot
from probe_common import (OWNED_ROOT, axis_snapshot, call_step, file_record,
                          floats, load_matplotlib, prepare_output, utc, write_json)

PIXEL_TOLERANCE = 0.25
INK_TOLERANCE = 4.0


def np_rgb(source):
    import numpy as np
    from PIL import Image
    with Image.open(source) as png:
        return np.asarray(png.convert("RGB"))


def rgb_sha(rgb):
    return hashlib.sha256(rgb.tobytes()).hexdigest()


def png_probe(fig, labels, target, axes):
    """Use saved pixels and a label-alpha-zero export at the same geometry."""
    import numpy as np
    from PIL import Image

    original = np_rgb(target)
    record = {
        "size_px_wh": list(original.shape[1::-1]),
        "file": file_record(target),
        "decoded_rgb_sha256": rgb_sha(original),
    }
    if not labels:
        return record, None
    before = [axis_snapshot(fig, ax) for ax in axes]
    old_alpha = [label.get_alpha() for label in labels]
    with io.BytesIO() as buffer:
        try:
            for label in labels:
                label.set_alpha(0)
            fig.savefig(buffer, format="png")
            buffer.seek(0)
            hidden = np_rgb(buffer)
        finally:
            for label, alpha in zip(labels, old_alpha):
                label.set_alpha(alpha)
    after = [axis_snapshot(fig, ax) for ax in axes]
    if original.shape != hidden.shape:
        raise ValueError("PNG probe changed canvas dimensions")
    changed = np.any(original != hidden, axis=2)
    mask = target.with_name("ink-mask.png")
    Image.fromarray(changed.astype("uint8") * 255, mode="L").save(str(mask))
    record.update(
        alpha_zero_decoded_rgb_sha256=rgb_sha(hidden),
        axes_unchanged_for_alpha_zero=(before == after),
        changed_pixels=int(changed.sum()),
        ink_mask=file_record(mask),
    )
    return record, changed


def ink_box(mask, x0=0, y0=0):
    """Return a half-open top-left-origin bbox and an exact pixel count."""
    yy, xx = mask.nonzero()
    if not len(xx):
        return None, 0
    return [int(xx.min()+x0), int(yy.min()+y0),
            int(xx.max()+x0+1), int(yy.max()+y0+1)], int(len(xx))


def outside(box, width, height, tolerance=PIXEL_TOLERANCE):
    x0, y0, dx, dy = box
    return min(x0, y0) < -tolerance or x0+dx > width+tolerance or y0+dy > height+tolerance


def label_ink(box, mask):
    import math
    height, width = mask.shape
    x0, y0, dx, dy = box
    left = max(0, math.floor(x0)-2)
    right = min(width, math.ceil(x0+dx)+2)
    top = max(0, math.floor(height-y0-dy)-2)
    bottom = min(height, math.ceil(height-y0)+2)
    if left >= right or top >= bottom:
        return None, 0
    return ink_box(mask[top:bottom, left:right], left, top)


def m03_state(fig, ax, cb, label, renderer=None):
    state = m03_snapshot(fig, ax, cb, label, renderer)
    p = state["text_anchor_display_pixels"]
    box = state["colorbar_axes"]["figure_bbox_pixels"]
    state["anchor_inside_figure"] = bool(fig.bbox.contains(*p))
    state["axes_data_coordinates_at_anchor"] = floats(cb.ax.transData.inverted().transform(p))
    if renderer:
        state["text_bbox_outside_figure"] = outside(state["text_bbox_display_pixels"], box[2], box[3])
    return state


def make_m03(plt, np, plan):
    from matplotlib.transforms import blended_transform_factory
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    factor = float(plan["input"])
    matrix = factor * np.arange(100).reshape((10, 10))
    fig, ax = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
    fig.suptitle("my title")
    im = ax.imshow(matrix)
    cax = make_axes_locatable(ax).append_axes("right", "5%", pad="10%")
    cb = fig.colorbar(im, cax=cax)
    if plan["condition"] == "xlim=-1..3":
        cb.ax.set_xlim(-1, 3)
    transform = {}
    if plan["choice"] == "A":
        transform = {"transform": cb.ax.transAxes}
    if plan["choice"] == "M":
        transform = {"transform": blended_transform_factory(cb.ax.transAxes, cb.ax.transData)}
    label = cb.ax.text(0.5, 0.5, "my colorbar", ha="center",
                       va="center", rotation=90, **transform)
    return fig, ax, cb, label, matrix


def save(fig, target, record):
    outcome = call_step("save_png", lambda: fig.savefig(str(target)))
    record["steps"].append(outcome)
    record["status"] = "saved" if outcome["ok"] else "save_failed"
    return outcome["ok"]


def run_m03(plt, np, plan, target, record):
    fig, ax, cb, label, matrix = make_m03(plt, np, plan)
    try:
        record["input"] = {
            "factor": float(plan["input"]),
            "matrix_min_max": [float(matrix.min()), float(matrix.max())],
            "matrix_sha256": hashlib.sha256(matrix.tobytes()).hexdigest(),
            "text": label.get_text(),
            "text_align": [label.get_horizontalalignment(), label.get_verticalalignment()],
        }
        record["before_layout"] = m03_state(fig, ax, cb, label)
        layout = call_step("tight_layout_rect", lambda: fig.tight_layout(rect=[0, 0, 1, .95]))
        record["steps"].append(layout)
        record["after_layout_attempt"] = m03_state(fig, ax, cb, label)
        if not layout["ok"]:
            record["status"] = "layout_failed"
            return
        if not save(fig, target, record):
            return
        state = m03_state(fig, ax, cb, label, fig.canvas.get_renderer())
        record["after_save"] = state
        record["rendered_font"] = font_record(label.get_fontproperties())
        probe, mask = png_probe(fig, [label], target, [ax, cb.ax])
        box, pixels = ink_box(mask)
        probe["label_bbox_top_left_px"] = box
        probe["label_ink_pixels"] = pixels
        if box:
            height = probe["size_px_wh"][1]
            center = [(box[0]+box[2])/2, height-(box[1]+box[3])/2]
            delta = [a-b for a, b in zip(center, state["text_anchor_display_pixels"])]
            probe.update(
                label_center_display_px=center,
                label_center_minus_anchor_px=delta,
                agrees_with_transform=probe["axes_unchanged_for_alpha_zero"] and
                max(map(abs, delta)) <= INK_TOLERANCE and state["anchor_inside_figure"],
            )
        else:
            probe["agrees_with_transform"] = (
                probe["axes_unchanged_for_alpha_zero"] and not state["anchor_inside_figure"])
        record["png"] = probe
    finally:
        plt.close(fig)


def run_m02(plt, np, plan, target, record):
    count = int(plan["input"])
    choice = "no_artist_reference" if plan["choice"] == "C" else plan["choice"]
    fig, axes, legend, inputs = build_m02(plt, np, count, choice, 45045)
    try:
        record["input"] = inputs
        record["before_layout"] = [axis_snapshot(fig, ax) for ax in axes]
        layout = call_step("tight_layout", fig.tight_layout)
        record["steps"].append(layout)
        record["after_layout_attempt"] = [axis_snapshot(fig, ax) for ax in axes]
        if not layout["ok"]:
            record["status"] = "layout_failed"
            return
        if not save(fig, target, record):
            return
        record["after_save"] = [axis_snapshot(fig, ax) for ax in axes]
        labels = legend.get_texts() if legend is not None else []
        probe, mask = png_probe(fig, labels, target, axes)
        record["png"] = probe
        record["legend"] = None
        if legend is not None:
            width, height = probe["size_px_wh"]
            renderer = fig.canvas.get_renderer()
            bbox = floats(legend.get_window_extent(renderer).bounds)
            entries = []
            for index, label in enumerate(labels, 1):
                entry_box = floats(label.get_window_extent(renderer).bounds)
                ink, pixels = label_ink(entry_box, mask)
                entries.append({
                    "id": "%02d-%s" % (index, label.get_text()),
                    "caption": label.get_text(),
                    "bbox_display_px": entry_box,
                    "bbox_outside": outside(entry_box, width, height),
                    "ink_bbox_top_left_px": ink,
                    "ink_pixels": pixels,
                })
            record["rendered_font"] = font_record(labels[0].get_fontproperties())
            record["legend"] = {
                "in_layout": legend.get_in_layout(),
                "bbox_display_px": bbox,
                "bbox_outside": outside(bbox, width, height),
                "count": len(labels),
                "font_size_pt": [float(label.get_fontsize()) for label in labels],
                "entries": entries,
            }
    finally:
        plt.close(fig)


def font_record(props):
    from matplotlib import font_manager
    return file_record(font_manager.findfont(props))


def attest_environment(mpl, np, details, cache):
    import ctypes
    import ssl
    import zlib
    from matplotlib import font_manager, ft2font
    from PIL import Image, __version__ as pillow_version
    prop = font_manager.FontProperties(family="DejaVu Sans", size=10.0)
    font = Path(font_manager.findfont(prop)).resolve()
    bundled = Path(mpl.get_data_path()).resolve() / "fonts" / "ttf" / "DejaVuSans.ttf"
    if font != bundled:
        raise ValueError("DejaVu Sans was resolved outside the wheel: " + str(font))
    if sys.version_info[:3] != (3, 6, 8) or np.__version__ != "1.16.6" or pillow_version != "6.2.2":
        raise ValueError("Legacy interpreter, NumPy or Pillow pin mismatch")

    from numpy.core import _multiarray_umath
    modules = {key: dict(file_record(value.__file__), path=value.__file__) for key, value in
               (("matplotlib", mpl), ("ft2font", ft2font), ("numpy", np),
                ("numpy_native", _multiarray_umath), ("pillow", Image), ("ctypes", ctypes))}
    details.update(
        os_release=Path("/etc/os-release").read_text(),
        glibc=platform.libc_ver(),
        executable=str(Path(sys.executable).resolve()),
        pointer_bits=8*struct.calcsize("P"),
        backend=mpl.get_backend(),
        pillow=pillow_version,
        openssl=ssl.OPENSSL_VERSION,
        zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,
        freetype_build_type=getattr(ft2font, "__freetype_build_type__", None),
        font=dict(file_record(font), path=str(font), font_properties="DejaVu Sans 10 pt"),
        modules=modules,
        dpi={"figure": mpl.rcParams["figure.dpi"], "savefig": mpl.rcParams["savefig.dpi"]},
        config_dir=str(cache / "_mplconfig"),
        cache_entries_after_import=sorted(x.name for x in (cache / "_mplconfig").iterdir()),
        rerender_bbox_inches=mpl.rcParams["savefig.bbox"],
        rc_tight_layout_auto=mpl.rcParams["figure.autolayout"],
        cartopy_used=False,
    )
    return details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeat", choices=["R1", "R2", "V1", "G1"], required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    try:
        out.relative_to(OWNED_ROOT / "evidence")
    except ValueError:
        parser.error("Write this replay below the owned evidence directory.")

    with (OWNED_ROOT / "expected.csv").open(encoding="utf-8", newline="") as stream:
        plans = [row for row in csv.DictReader(stream) if row["repeat"] == args.repeat]
    if not plans or len({plan["version"] for plan in plans}) != 1:
        raise ValueError("Expected exactly one pinned version per repeat.")
    version = plans[0]["version"]
    out.mkdir(exist_ok=True, parents=True)
    for target in [out / plan["run_id"] for plan in plans] + [out / (args.repeat+".environment.json")]:
        if target.exists():
            raise FileExistsError(str(target))

    errors = 0
    with tempfile.TemporaryDirectory(dir=str(out), prefix=".mpl-replay-") as tmp:
        cache = prepare_output(Path(tmp) / "runtime")
        if list((cache / "_mplconfig").iterdir()):
            raise ValueError("Expected empty Matplotlib config directory at start.")
        mpl, plt, np, identity = load_matplotlib(cache, version)
        environment = attest_environment(mpl, np, identity, cache)
        environment.update(repeat=args.repeat, mpl_config_entries_before_import=[], argv=sys.argv)
        write_json(out / (args.repeat+".environment.json"), environment)
        for plan in plans:
            run_dir = out / plan["run_id"]
            run_dir.mkdir()
            record = {"plan": plan, "started_utc": utc(), "steps": []}
            probe = run_m03 if plan["case"] == "M03" else run_m02
            try:
                probe(plt, np, plan, run_dir / "figure.png", record)
            except Exception:
                errors += 1
                record["instrumentation_error"] = traceback.format_exc()
                record.setdefault("status", "instrumentation_failed")
            record["finished_utc"] = utc()
            write_json(run_dir / "observations.json", record)
            print(plan["run_id"], record["status"])
    return int(errors > 0)


if __name__ == "__main__":
    sys.exit(main())
