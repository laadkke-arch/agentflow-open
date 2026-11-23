"""UNEXECUTED probe plan: M03; require explicit3.0.2 or2.2.2.

Input: https://github.com/matplotlib/matplotlib/issues/13600
No crash guard is patched; failures and transformed anchors remain separate.
"""
import argparse
from probe_common import (axis_snapshot, call_step, file_record, floats,
                          load_matplotlib, prepare_output, utc, write_json)


def snapshot(fig, ax, cb, text, renderer=None):
    display = text.get_transform().transform(text.get_position())
    fraction = cb.ax.transAxes.inverted().transform(display)
    result = {
        "data_axes": axis_snapshot(fig, ax),
        "colorbar_axes": axis_snapshot(fig, cb.ax),
        "text_input_position": floats(text.get_position()),
        "text_anchor_display_pixels": floats(display),
        "text_anchor_colorbar_axes_fraction": floats(fraction),
        "text_font_points": float(text.get_fontsize()),
        "text_rotation": float(text.get_rotation()),
        "transform_is_colorbar_data": text.get_transform() is cb.ax.transData,
        "transform_is_colorbar_axes": text.get_transform() is cb.ax.transAxes,
    }
    low, high = cb.ax.get_ylim()
    if cb.ax.get_yscale() == "linear" and high != low:
        result["data_value_point5_fraction_from_ACTUAL_ylim"] = float(
            (0.5-low) / (high-low))
    if renderer is not None:
        result["text_bbox_display_pixels"] = floats(text.get_window_extent(renderer).bounds)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--expected-mpl", required=True, choices=["3.0.2", "2.2.2"])
    args = parser.parse_args()
    out = prepare_output(args.out)
    mpl, plt, np, environment = load_matplotlib(out, args.expected_mpl)
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    result = {
        "case": "M03", "environment": environment,
        "original_backend": "TkAgg/Windows10; probe uses Agg",
        "version_role": "primary" if args.expected_mpl == "3.0.2" else "version sensitivity",
        "postseal_controls": "Agg and explicit fixed10-pointfont; instrumented actual limits",
        "normal_factor": 0.01, "boundary_factor": 0.001, "sensitivity_factor": 0.1,
        "runs": [],
    }
    for factor in (0.01, 0.001, 0.1):
        for choice in ("A", "B"):
            matrix = factor * np.arange(100).reshape((10, 10))
            fig, ax = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
            fig.suptitle("my title")
            im = ax.imshow(matrix)
            cax = make_axes_locatable(ax).append_axes("right", "5%", pad="10%")
            cb = fig.colorbar(im, cax=cax)
            extra = {"transform": cb.ax.transAxes} if choice == "A" else {}
            text = cb.ax.text(0.5, 0.5, "my colorbar", ha="center",
                              va="center", rotation=90, **extra)
            run = {
                "factor": factor, "choice": choice,
                "input": {"formula": "factor * arange(100).reshape((10,10))",
                          "minimum": float(matrix.min()), "maximum": float(matrix.max())},
                "before_layout": snapshot(fig, ax, cb, text),
                "steps": [],
            }
            layout = call_step("tight_layout_rect",
                               lambda: fig.tight_layout(rect=[0, 0, 1, 0.95]))
            run["steps"].append(layout)
            run["after_layout_attempt"] = snapshot(fig, ax, cb, text)
            if layout["ok"]:
                target = out / ("factor-%s-%s.png" % (factor, choice))
                saved = call_step("save_png", lambda: fig.savefig(str(target)))
                run["steps"].append(saved)
                if saved["ok"]:
                    run["after_save"] = snapshot(fig, ax, cb, text,
                                                 fig.canvas.get_renderer())
                    run["file"] = file_record(target)
            else:
                run["export_status"] = "not attempted: original layout raised; no silent repair"
            result["runs"].append(run)
            plt.close(fig)
            write_json(out / "observations.json", result)
    result["completed_utc"] = utc()
    result["inference_limit"] = (
        "Actual transformed anchor and actual ylim are recorded. "
        "Do not substitute data extrema for colorbar axis limits. "
        "A fixed crash alone does not establish a centered anchor.")
    write_json(out / "observations.json", result)


if __name__ == "__main__":
    main()

