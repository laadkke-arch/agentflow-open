"""Conditional model arithmetic only; imports no plotting library.

These numbers are not Matplotlib observations and do not establish its axis limits.
"""
import argparse
from fractions import Fraction
from probe_common import prepare_output, utc, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = prepare_output(args.out)
    rows = []
    for string in ("0.01", "0.001", "0.1"):
        factor = Fraction(string)
        assumed_low = Fraction(0)
        assumed_high = factor * 99
        b = (Fraction(1, 2) - assumed_low) / (assumed_high - assumed_low)
        rows.append({
            "factor": string,
            "assumption": "linear,noninverted axis limits exactly[0,99*factor]",
            "assumed_ylim": [str(assumed_low), str(assumed_high)],
            "A_axes_fraction": "1/2", "B_conditional_fraction": str(b),
            "B_conditional_decimal": float(b),
            "observed_colorbar_ylim": None, "software_execution_evidence": False,
        })
    write_json(out / "conditional-model-only.json", {
        "created_utc": utc(), "kind": "arithmetic_only_not_plot_execution",
        "rows": rows,
        "limitation": "Use m03_colorbar.py output for real transforms/limits; "
                      "this file never supplies missing historical expected outputs.",
    })


if __name__ == "__main__":
    main()

