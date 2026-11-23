"""Freeze distinct A/B and future-input C predictions before result exposure."""

import argparse
import csv
import hashlib
import subprocess

from fixturegen import CASES_I, CASES_T, CELLS, OWNED, json_text, read_lines, utc

FIELDS = ("view", "domain", "cell", "scenario", "condition", "prediction", "reason", "basis")
PATHS = {"names", "one_each", "extract"}


def table_predictions(view, cell, scenario):
    basis_a = f"T{cell[1]}x.solo-writer.0; Tx{cell[2]}.solo-reader.0"
    predictions = {c: ("support", "Separate syntax and typed-field exemplars round-trip on the supported subset", basis_a)
                   for c in CASES_T}
    if cell.endswith("0"):
        predictions["null"] = ("reject", "The singleton manual NULL field returns a string using the default reader", basis_a)
    if view == "A" and scenario == "retry":
        return {c: p if p[0] == "reject" else ("hold", "Standalone runs provide no resubmission evidence", basis_a)
                for c, p in predictions.items()}
    if view == "B":
        basis_b = basis_a + "; T02/T04/T05; SCOPE checkpoint rule"
        if cell[1] == "1":
            predictions["null"] = ("reject", "Raw NULL spelling can equal the literal. Both readers return the spelling as str", basis_b)
        elif cell.endswith("1"):
            predictions["null"] = ("support", "Empty unquoted field maps to None at the fixed reader version", basis_b)
        if scenario == "edge":
            predictions["text"] = ("hold", "The seeded family can include NUL. The realized input has not been inspected", basis_b + "; T10")
        if scenario == "retry":
            predictions = {c: (vote, reason + "; publication overwrites a fresh .part", basis_b)
                           for c, (vote, reason, _) in predictions.items()}
    return predictions


def image_predictions(view, cell, scenario):
    basis_a = f"I{cell[1]}x.solo-converter.0; Ix{cell[2]}.solo-zip.0"
    predictions = {c: ("support", "Singleton capabilities support this property in the separate examples", basis_a)
                   for c in CASES_I}
    if cell != "I00":
        for c in PATHS:
            predictions[c] = ("reject", "At least one standalone setting removes the originally required directory component", basis_a)
    if view == "A" and scenario == "retry":
        return {c: p if p[0] == "reject" else ("hold", "Standalone runs did not edit an existing completed artifact", basis_a)
                for c, p in predictions.items()}
    if view == "B":
        basis_b = basis_a + "; I01/I08/I13/I14; existing archive publication rule"
        if cell == "I01":
            predictions = {c: ("reject", "Two equal basenames will be sent to native ZIP duplicate detection; no current product", basis_b)
                           for c in CASES_I}
        elif cell in {"I10", "I11"}:
            predictions = {c: ("reject", "First staging loses one source identity and the required directory names", basis_b)
                           for c in CASES_I}
        elif scenario == "retry":
            for c in ("names", "members"):
                predictions[c] = ("reject", "Default add replaces the matching old entry and retains the unrelated old entry", basis_b)
        elif scenario == "edge":
            for c in PATHS:
                predictions[c] = ("hold", "Non-ASCII path success depends on actual archive name bits, extras, and reader version", basis_b)
    return predictions


def future_predictions(domain, cell, rows):
    main_rows = [row for row in rows if row["cell"] == cell and row["scenario"] == "normal"]
    if len(main_rows) != 2:
        raise ValueError(f"Missing normal pair for {cell}")
    basis = "; ".join(row["run"] for row in main_rows)
    result = {}
    for c in CASES_T if domain == "T" else CASES_I:
        votes = {row["phase_status"] == "complete" and row["final"]["conditions"][c] for row in main_rows}
        outcome = "support" if votes == {True} else "reject" if votes == {False} else "hold"
        reason = "Observed pair agrees; the held fixture is assumed comparable for this property"
        if domain == "T" and c == "text":
            outcome, reason = "hold", "The observed text did not include an embedded NUL; the new generator can include one"
        if cell == "I00" and c in PATHS:
            outcome, reason = "hold", "The normal pair only demonstrates ASCII paths. The new name repertoire is outside that evidence"
        result[c] = outcome, reason, basis
    return result


def predictions(view, rows=()):
    for domain, cells in CELLS.items():
        for cell in cells:
            for scenario in (("edge",) if view == "C" else ("normal", "edge", "retry")):
                if view == "C":
                    values = future_predictions(domain, cell, rows)
                else:
                    function = table_predictions if domain == "T" else image_predictions
                    values = function(view, cell, scenario)
                all_outcomes = {v[0] for v in values.values()}
                result = "reject" if "reject" in all_outcomes else "hold" if "hold" in all_outcomes else "support"
                values["all"] = (result, "Conjunction of the mandatory conditions", "This cell and scenario")
                for condition, (outcome, reason, basis) in values.items():
                    yield (view, domain, cell, scenario, condition, outcome, reason, basis)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("view", choices=("AB", "C"))
    args = parser.parse_args()
    edge_realized = any(r["id"].endswith("-edge") for r in read_lines(OWNED / "fixtures.jsonl"))
    if edge_realized:
        raise ValueError("The edge fixture was already materialized")
    runs = OWNED / "runs.jsonl"
    if args.view == "AB" and runs.exists():
        raise ValueError("The composed run ledger already exists")
    rows = read_lines(runs) if args.view == "C" else []
    if any(r["scenario"] == "edge" for r in rows):
        raise ValueError("The edge run is already visible")
    path = OWNED / ("evidence/c-heldout-predictions.csv" if args.view == "C" else "predictions.csv")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(FIELDS)
        for view in args.view:
            writer.writerows(predictions(view, rows))
    details = {
        "view": args.view, "prepared_utc": utc(), "actor": "AF-RES-078 Codex Cloud",
        "precommit_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "predictions_sha256": sha(path), "fixture_file_sha256": sha(OWNED / "fixtures.jsonl"),
        "inputs": {"normal_and_retry_run_sha256": sha(runs)} if rows else {
            "solo_sha256": sha(OWNED / "evidence/solo.jsonl"), "contracts_sha256": sha(OWNED / "contracts.csv")},
        "held_seed_or_output_exposed": False,
        "visible": "Known fixture generator, official behavior and version limits, source incidents.",
    }
    proof = OWNED / ("evidence/c-heldout-freeze.json" if args.view == "C" else "evidence/ab-freeze.json")
    proof.write_text(json_text(details) + "\n", encoding="utf-8")
    print(path.name, sha(path))


if __name__ == "__main__":
    main()
