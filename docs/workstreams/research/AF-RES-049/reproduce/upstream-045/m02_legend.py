"""UNEXECUTED probe plan: M02, Matplotlib3.0.2.

Input: https://github.com/matplotlib/matplotlib/issues/13522
Independently implemented original plot inputs with seeded randomness.
"""
import argparse
import itertools
import random
from probe_common import (axis_snapshot, call_step, difference, file_record,
                          floats, load_matplotlib, prepare_output, utc, write_json)

COLORS = [
    "#418CF0FF", "#FCB441FF", "#E0400AFF", "#056492FF", "#BFBFBFFF",
    "#1A3B69FF", "#FFE382FF", "#129CDDFF", "#CA6B4BFF", "#005CDBFF",
    "#F3D288FF", "#506381FF", "#F1B9A8FF", "#E0830AFF", "#7893BEFF",
]
CAPTIONS = "abcdefghijklmnopsdjkfhsdkjfsdkfggudyguyu"


def build(plt, np, count, choice, seed):
    import matplotlib.lines as line_module
    rng = random.Random(seed)
    x = [rng.randint(-7, 7) for _ in range(10)]
    y = [rng.randint(1, 9) for _ in range(10)]
    series = [[rng.randint(1, 10) for _ in range(10)] for _ in range(count)]
    colors = itertools.cycle(COLORS)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3), dpi=100,
                             gridspec_kw={"width_ratios": [5, 1, 5]})
    left, middle, right = axes
    left.set_xlabel("X Axis")
    left.set_ylabel("Y AXis")
    right.set_ylabel("Y Axis")
    left.set_xlim(-8, 8)
    left.set_ylim(0, 10)
    right.set_ylim(0, 10)
    for xx, yy in zip(x, y):
        left.scatter(xx, yy, marker="o", facecolors=next(colors),
                     edgecolors="black", zorder=3)
    handles = []
    for values in series:
        color = next(colors)
        right.plot(np.linspace(0, len(values)-1, len(values)), values, color=color)
        handles.append(line_module.Line2D(
            [0, 0], [0, 0], color=color, marker="o",
            markeredgecolor=color, markerfacecolor=color))
    legend = None
    if choice != "no_artist_reference":
        legend = middle.legend(handles, CAPTIONS[:count], loc=0,
                               frameon=False, title="My Chart")
        if choice == "B":
            # Only B changes this flag; A retains default layout inclusion.
            legend.set_in_layout(False)
    for spine in middle.spines.values():
        spine.set_visible(False)
    middle.set_xticks([])
    middle.set_yticks([])
    inputs = {"seed": seed, "legend_count": count,
              "balance_x": x, "balance_y": y, "series": series}
    return fig, axes, legend, inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=45045)
    parser.add_argument("--counts", type=int, nargs="+", default=[10, 20, 30])
    args = parser.parse_args()
    if not {10, 30}.issubset(set(args.counts)):
        parser.error("Retain both sealed inputs10 and30;20 is optional sensitivity.")
    if any(n < 1 or n > len(CAPTIONS) for n in args.counts):
        parser.error("Counts must fit the original captions sequence.")
    out = prepare_output(args.out)
    mpl, plt, np, environment = load_matplotlib(out, "3.0.2")
    result = {
        "case": "M02", "environment": environment,
        "original_backend": "TkAgg/Windows10; probe uses Agg",
        "postseal_controls": "seed45045(default),Agg,explicit fixed10-pointfont",
        "fixed_figure_inches": [10, 3], "width_ratios": [5, 1, 5], "runs": [],
        "no_artist_reference": "Same plotted data and middle axes; legend artist never added.",
    }
    for count in args.counts:
        for choice in ("A", "B", "no_artist_reference"):
            fig, axes, legend, inputs = build(plt, np, count, choice, args.seed)
            run = {"count": count, "choice": choice, "inputs": inputs, "steps": []}
            layout = call_step("tight_layout", fig.tight_layout)
            run["steps"].append(layout)
            run["after_layout"] = [axis_snapshot(fig, ax) for ax in axes]
            if not layout["ok"]:
                run["export_status"] = "not attempted: original layout raised"
                result["runs"].append(run)
                plt.close(fig)
                write_json(out / "observations.json", result)
                continue
            target = out / ("legend-%s-%s.png" % (count, choice))
            saved = call_step("save_without_bbox_tight", lambda: fig.savefig(str(target)))
            run["steps"].append(saved)
            if saved["ok"]:
                run["after_save"] = [axis_snapshot(fig, ax) for ax in axes]
                run["file"] = file_record(target)
                if legend is not None:
                    renderer = fig.canvas.get_renderer()  # after saving, no extra draw
                    box = legend.get_window_extent(renderer)
                    frame = fig.bbox
                    run["legend"] = {
                        "in_layout": legend.get_in_layout(),
                        "bbox_pixels": floats(box.bounds),
                        "artist_text_count": len(legend.get_texts()),
                        "font_sizes_points": [float(t.get_fontsize()) for t in legend.get_texts()],
                        "bbox_outside_canvas": bool(
                            box.x0 < frame.x0 or box.y0 < frame.y0 or
                            box.x1 > frame.x1 or box.y1 > frame.y1),
                        "clipping_caveat": "bbox overflow; inspect PNG for actual visible clipping",
                    }
            result["runs"].append(run)
            plt.close(fig)
            write_json(out / "observations.json", result)
    for count in args.counts:
        group = {r["choice"]: r for r in result["runs"] if r["count"] == count}
        reference = group["no_artist_reference"].get("after_save")
        if reference:
            for choice in ("A", "B"):
                current = group[choice].get("after_save")
                if current:
                    group[choice]["data_axes_bbox_minus_no_artist_pixels"] = {
                        str(i): difference(current[i]["axes_bbox_pixels"],
                                           reference[i]["axes_bbox_pixels"])
                        for i in (0, 2)
                    }
    result["completed_utc"] = utc()
    result["verdict"] = "No automatic donor discrimination; both sealed rules recommend B."
    write_json(out / "observations.json", result)


if __name__ == "__main__":
    main()

