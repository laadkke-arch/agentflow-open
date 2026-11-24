"""Read only the raw executions and the fixed population to compare outputs."""
import argparse
import json
from collections import Counter
from pathlib import Path

from common import ROOT, json_in, sha, write_csv, write_json, write_jsonl


def read_runs(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def semantic_outcome(case):
    return {key: value for key, value in case["result"].items() if key != "stack"}


def array_state(case):
    return {key: case[key] for key in ("argument_before", "argument_after", "original_before",
                                      "original_after", "argument_mutated", "original_mutated")}


def cell_fingerprint(case):
    return semantic_outcome(case), array_state(case)


def expected_cases(inputs):
    return [
        ("/".join((fn, name, "-" if p is None else str(p), mode)), fn, name, p, mode)
        for fn in inputs["functions"] for name in inputs["arrays"]
        for p in (inputs["quantile_p"] if fn == "quantile" else [None]) for mode in inputs["modes"]
    ]


def index_cohort(rows):
    return {row["intended_version"]: (row, {case["cell"]: case for case in row.get("cases", [])}) for row in rows}


def verified_case(cohorts, version, cell):
    a, b = [cohort.get(version, ({}, {})) for cohort in cohorts]
    if a[0].get("status") != "ok" or b[0].get("status") != "ok":
        return None
    left, right = a[1].get(cell), b[1].get(cell)
    if not left or not right or cell_fingerprint(left) != cell_fingerprint(right):
        return None
    return left


def reduce_state(states):
    if "changed" in states:
        return "changed"
    if "unknown" in states:
        return "unknown"
    return "same"


def compare(before, after, design, indexes):
    for cell, function, array, p, mode in design:
        a = verified_case(indexes, before, cell)
        b = verified_case(indexes, after, cell)
        outcomes = (semantic_outcome(a) if a else None, semantic_outcome(b) if b else None)
        observed = a is not None and b is not None
        value_delta = outcomes[0] != outcomes[1] if observed else None
        array_delta = array_state(a) != array_state(b) if observed else None
        yield {
            "cell": cell, "function": function, "array": array, "p": p, "mode": mode,
            "state": ("changed" if value_delta or array_delta else "same") if observed else "unknown",
            "outcome_before": json.dumps(outcomes[0], ensure_ascii=False, separators=(",", ":")),
            "outcome_after": json.dumps(outcomes[1], ensure_ascii=False, separators=(",", ":")),
            "array_before_mutated": a["original_mutated"] if a else None,
            "array_after_mutated": b["original_mutated"] if b else None,
            "argument_before_mutated": a["argument_mutated"] if a else None,
            "argument_after_mutated": b["argument_mutated"] if b else None,
            "outcome_delta": value_delta, "array_state_delta": array_delta,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT)
    args = parser.parse_args()
    first, second = [read_runs(path) for path in (args.first, args.second)]
    cohorts = [index_cohort(rows) for rows in (first, second)]
    roster = json_in(ROOT / "evidence/roster.json")
    inputs = json_in(ROOT / "replay/inputs.json")
    design = expected_cases(inputs)
    order_keys = {"publish": "published_order", "semver": "semver_order"}
    publish = roster["published_order"]
    evidence = args.out / "evidence"
    evidence.mkdir(exist_ok=True, parents=True)
    write_jsonl(args.out / "runs.jsonl", first + second)
    results, pairs, matching = [], [], []
    for order, key in order_keys.items():
        versions = roster[key]
        for before, after in zip(versions, versions[1:]):
            common = {"order": order, "before": before, "after": after,
                      "raw_run_ids": " ".join(f"{code}-{v}" for v in (before, after) for code in ("A", "B"))}
            rows = list(compare(before, after, design, cohorts))
            results.extend(common | row for row in rows)
            counts = Counter(row["state"] for row in rows)
            pairs.append(common | {"state": reduce_state(counts), "changed_cells": counts["changed"],
                                   "same_cells": counts["same"], "unknown_cells": counts["unknown"],
                                   **{f"{fn}_state": reduce_state({row["state"] for row in rows if row["function"] == fn})
                                      for fn in inputs["functions"]}})
            left = cohorts[0][before][0].get("direct")
            right = cohorts[0][after][0].get("direct")
            shared = sorted(set(left or {}) & set(right or {}))
            matching.append(common | {"left_declared_and_loaded": json.dumps(left), "right_declared_and_loaded": json.dumps(right),
                                       "shared": " ".join(shared), "matched_extra_runs": 0,
                                       "status": "no_direct_dependencies_in_either_release" if left == right == {} else
                                       "shared_alignment_unconfirmed" if shared else "no_shared_or_unconfirmed"})
    write_csv(evidence / "output-comparison.csv", results)
    write_csv(evidence / "output-pairs.csv", pairs)
    write_csv(evidence / "matched-direct.csv", matching)
    agreed = {
        version: sum(verified_case(cohorts, version, c[0]) is not None for c in design) for version in publish
    }
    write_json(evidence / "replay.json", {
        "inputs_sha256": sha((ROOT / "replay/inputs.json").read_bytes()),
        "case_cells_per_release": len(design), "expected_releases": publish,
        "cohorts": [
            {"id": rows[0]["cohort"], "release_rows": len(rows), "probe_statuses": dict(Counter(row["status"] for row in rows)),
             "clean_root": str(Path(rows[0]["launch_path"]).parent), "npm_cache": rows[0]["npm_cache"]}
            for rows in (first, second)
        ],
        "identical_semantic_cells_by_version": agreed,
        "agreement": sum(agreed.values()), "agreement_denominator": len(design) * len(publish),
        "entry_and_integrity_conditions": "Both clean paths separately run npm ci against the same SRI-locked tar URI. Path and stack differ by install root.",
        "expected_different_metadata": "time, install/cache path, wall/cpu, stack absolute path",
        "supported_versions": [version for version in publish if agreed[version] == len(design) and
                               all(cohort[version][0]["supported"] for cohort in cohorts)],
        "published_pairs": dict(Counter(row["state"] for row in pairs if row["order"] == "publish")),
        "raw_only": ["runs from both paths", "roster.json", "inputs.json"],
    })
    print(f"{sum(agreed.values())}/{len(design) * len(publish)} repeated cells agree; {len(results)} output-only pair cells in two orders")


if __name__ == "__main__":
    main()
