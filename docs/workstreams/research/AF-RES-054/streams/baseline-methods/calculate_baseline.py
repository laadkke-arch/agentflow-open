"""Aggregate-only checks for AF-RES-054 B01/B02. No participant data.

Run from any directory: python -B path/to/calculate_baseline.py
The examples are mathematical witnesses, never reconstructed observed records.
"""
from fractions import Fraction
from pathlib import Path
import json


def table(n, q, t, x):
    cells = [x, q - x, t - x, n - q - t + x]
    assert all(isinstance(v, int) and v >= 0 for v in cells)
    assert sum(cells) == n
    assert cells[0] + cells[1] == q
    assert cells[0] + cells[2] == t
    return cells


def bounds(n, q, t):
    lo, hi = max(0, q + t - n), min(q, t)
    return {"N": n, "q": q, "t": t, "L": lo, "U": hi,
            "lower_table": table(n, q, t, lo),
            "upper_table": table(n, q, t, hi)}


def patterns(d, margins, all_pass):
    assert sum(d.values()) == 12
    observed_margins = [sum(n for pattern, n in d.items() if pattern[i] == "1")
                        for i in range(4)]
    assert observed_margins == margins
    assert d.get("1111", 0) == all_pass
    return {"N": 12, "patterns": d, "task_margins": margins,
            "all_four_pass": all_pass, "status": "constructed_witness_not_observed"}


def main():
    exoa = [11, 11, 3, 3]
    jdoc = [10, 8, 4, 1]
    # Same publication margins. Author's explicit all-task result is an extra constraint.
    witnesses = {
        "exoa_compatible_upper_task12_overlap": patterns(
            {"1111": 3, "1100": 8, "0000": 1}, exoa, 3),
        "exoa_compatible_lower_task12_overlap": patterns(
            {"1111": 3, "1100": 7, "1000": 1, "0100": 1}, exoa, 3),
        "jdoc_compatible_upper_task12_overlap": patterns(
            {"1111": 1, "1110": 3, "1100": 4, "1000": 2, "0000": 2}, jdoc, 1),
        "jdoc_compatible_lower_task12_overlap": patterns(
            {"1111": 1, "1110": 3, "1100": 2, "1000": 4, "0100": 2}, jdoc, 1),
        "exoa_margins_only_rejected_by_author_intersection": patterns(
            {"1110": 3, "1101": 3, "1100": 4, "1000": 1, "0100": 1}, exoa, 0),
        "jdoc_margins_only_rejected_by_author_intersection": patterns(
            {"1110": 4, "1100": 4, "1001": 1, "1000": 1, "0000": 2}, jdoc, 0),
    }
    for key in list(witnesses):
        witnesses[key]["publication_compatible"] = "rejected" not in key

    fourway = {
        "exoa": {"L": max(0, sum(exoa) - 3 * 12), "U": min(exoa)},
        "jdoc": {"L": max(0, sum(jdoc) - 3 * 12), "U": min(jdoc)},
    }
    assert fourway == {"exoa": {"L": 0, "U": 3}, "jdoc": {"L": 0, "U": 1}}
    # Unknown t: these are two admissible values of the unknown timing margin,
    # not lower and upper x at one observed t. x is fixed by author aggregate.
    exoa_t_extremes = [table(12, 3, 3, 3), table(12, 3, 12, 3)]
    jdoc_t_extremes = [table(12, 1, 1, 1), table(12, 1, 12, 1)]
    contrast = Fraction(3, 12) - Fraction(1, 12)
    task3_contrast = Fraction(3, 12) - Fraction(4, 12)
    assert contrast == Fraction(1, 6)
    assert task3_contrast == Fraction(-1, 12)
    # Generic hand-calculation example, not attributed to any empirical study.
    generic = bounds(12, 7, 8)
    assert generic["L"] == 3 and generic["U"] == 7
    # Illustrates a change in the composition of observed finishers, not a
    # statement about what happened in Blueprint.
    survivor_counterexample = {
        "N_each": 10,
        "treatment": {"completed": 1, "mean_among_completers_seconds": 100,
                      "deadline_seconds": 600, "cap_composite_mean_seconds": 550},
        "control": {"completed": 10, "mean_among_completers_seconds": 200,
                    "deadline_seconds": 600, "cap_composite_mean_seconds": 200},
        "meaning": "Illustration only: finishers look faster while completion rate and explicitly cap-penalized composite are worse. Cap is not a completion time.",
    }
    assert (100 + 9 * 600) / 10 == 550
    output = {
        "cell_order": ["both", "quality_only", "time_only", "neither"],
        "four_task_pattern_order": ["T1", "T2", "T3", "T4"],
        "witnesses": witnesses,
        "ignoring_author_intersection_is_not_the_final_analysis": {
            "marginal_only_fourway_bounds": fourway,
            "difference": [str(Fraction(-1, 12)), str(Fraction(3, 12))],
            "negative_sign_witness": ["exoa_margins_only_rejected_by_author_intersection", "jdoc_compatible_upper_task12_overlap"],
            "positive_sign_witness": ["exoa_compatible_upper_task12_overlap", "jdoc_margins_only_rejected_by_author_intersection"],
        },
        "author_intersection": {
            "exoa": {"N": 12, "x": 3, "L": 3, "U": 3,
                     "t_not_observed_range": [3, 12], "t_extreme_tables": exoa_t_extremes},
            "jdoc": {"N": 12, "x": 1, "L": 1, "U": 1,
                     "t_not_observed_range": [1, 12], "t_extreme_tables": jdoc_t_extremes},
            "risk_difference": str(contrast), "risk_difference_pp": float(contrast * 100),
            "task3_risk_difference": str(task3_contrast),
        },
        "blueprint": {
            "original_binary_quality_predicate": None,
            "primary_endpoint_bound": None,
            "reason": "Original final quality is ordinal; no original pass cutoff. A hypothetical binary predicate's logical envelope is not the specified original endpoint.",
            "completion_only": {"blueprint": [9, 10], "control": [8, 10], "difference": "1/10"},
        },
        "generic_frechet_hand_example_not_a_study": generic,
        "generic_survivor_counterexample_not_a_study": survivor_counterexample,
        "checks": {"integer_nonnegative_cells": "pass", "margins_and_total": "pass",
                   "all_task_intersection": "pass", "contrast_exact_fractions": "pass",
                   "no_inferred_q_for_blueprint": "pass"},
    }
    target = Path(__file__).with_name("calculation-output.json")
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(target), "checks": output["checks"],
                      "author_bundle_difference": str(contrast),
                      "task3_difference": str(task3_contrast)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
