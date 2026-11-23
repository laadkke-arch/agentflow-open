"""Shared recording helpers. No rendering occurs on module import."""
import hashlib
import json
import math
import os
import platform
import sys
import traceback
import warnings
from datetime import datetime, timezone
from pathlib import Path

OWNED_ROOT = Path(__file__).resolve().parents[6] / "docs/workstreams/research/AF-RES-049"
SEAL = "0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1"


def utc():
    return datetime.now(timezone.utc).isoformat()


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    return value


def write_json(path, value):
    Path(path).write_text(json.dumps(clean(value), indent=2,
                                   ensure_ascii=False, allow_nan=False) + "\n")


def prepare_output(path):
    out = Path(path).resolve()
    try:
        out.relative_to(OWNED_ROOT)
    except ValueError:
        raise SystemExit("Output must remain under " + str(OWNED_ROOT))
    if out == OWNED_ROOT:
        raise SystemExit("Use a new run subdirectory, not the owned root.")
    out.mkdir(parents=True, exist_ok=False)
    # Keep Matplotlib font/config cache inside the owned path as well.
    config = out / "_mplconfig"
    config.mkdir()
    os.environ["MPLCONFIGDIR"] = str(config)
    os.environ["MPLBACKEND"] = "Agg"
    sys.dont_write_bytecode = True
    return out


def load_matplotlib(out, expected, cartopy_expected=None):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib import ft2font
        record = {
            "started_utc": utc(), "prediction_seal": SEAL,
            "python": sys.version, "platform": platform.platform(),
            "matplotlib": matplotlib.__version__, "numpy": np.__version__,
            "backend": matplotlib.get_backend(),
            "freetype": getattr(ft2font, "__freetype_version__", None),
            "expected_matplotlib": expected,
            "historical_original_platform_reproduced": False,
            "researcher_control": "Agg, rcdefaults, explicit 10-point DejaVu Sans",
            "status": "probe_started_not_yet_completed",
        }
        if cartopy_expected is not None:
            import cartopy
            import cartopy.crs as cartopy_crs
            record["cartopy"] = cartopy.__version__
            record["expected_cartopy"] = cartopy_expected
            record["proj"] = getattr(cartopy_crs, "PROJ4_VERSION", None)
        write_json(out / "environment.json", record)
        if matplotlib.__version__ != expected:
            raise RuntimeError("Required Matplotlib " + expected +
                               "; found " + matplotlib.__version__)
        if cartopy_expected and record["cartopy"] != cartopy_expected:
            raise RuntimeError("Required Cartopy " + cartopy_expected +
                               "; found " + record["cartopy"])
        matplotlib.rcdefaults()
        matplotlib.rcParams["font.size"] = 10.0
        matplotlib.rcParams["font.family"] = ["DejaVu Sans"]
        matplotlib.rcParams["figure.dpi"] = 100.0
        matplotlib.rcParams["savefig.dpi"] = 100.0
        matplotlib.rcParams["savefig.bbox"] = None
        return matplotlib, plt, np, record
    except Exception as exc:
        write_json(out / "environment-error.json", {
            "utc": utc(), "error_type": type(exc).__name__,
            "error": str(exc), "traceback": traceback.format_exc(),
            "plot_execution_completed": False,
        })
        raise


def floats(values):
    return [float(v) for v in values]


def axis_snapshot(fig, ax):
    # Deliberately avoid Axes.get_position(): in 3.0.2 it calls
    # apply_aspect(), so a measurement could alter the first-save state.
    # Private fields are passive diagnostics, never assigned by these probes.
    box = floats(ax.bbox.bounds)
    return {
        "active_position_figure_fraction": floats(ax._position.bounds),
        "original_position_figure_fraction": floats(ax._originalPosition.bounds),
        "axes_bbox_pixels": box,
        "axes_bbox_width_over_height": box[2] / box[3] if box[3] else None,
        "figure_bbox_pixels": floats(fig.bbox.bounds),
        "figure_size_inches": floats(fig.get_size_inches()),
        "dpi": float(fig.dpi),
        "xlim": floats(ax.get_xlim()), "ylim": floats(ax.get_ylim()),
        "xscale": ax.get_xscale(), "yscale": ax.get_yscale(),
        "aspect": ax.get_aspect(),
    }


def call_step(label, function):
    record = {"step": label, "started_utc": utc()}
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always")
        try:
            function()
            record["ok"] = True
        except Exception as exc:
            record.update(ok=False, error_type=type(exc).__name__,
                          error=str(exc), traceback=traceback.format_exc())
        record["warnings"] = [{
            "category": item.category.__name__, "message": str(item.message),
            "filename": item.filename, "lineno": item.lineno
        } for item in observed]
    record["finished_utc"] = utc()
    return record


def file_record(path):
    path = Path(path)
    return {"filename": path.name, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def difference(a, b):
    return [float(x) - float(y) for x, y in zip(a, b)]

