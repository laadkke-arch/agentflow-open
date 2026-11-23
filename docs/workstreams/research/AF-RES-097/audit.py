"""Recompute AF-RES-097 from the sealed input, raw receipts and run records."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from run import CALLS, HERE, VERSIONS


MINIMUM_SOURCES = {"issue": 2, "release_change": 5, "implementation": 7,
                   "png": 4, "arrow": 2, "gdal": 2}


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def check_receipts(rows, directory, environment):
    assert len({row["id"] for row in rows}) == len(rows)
    processes = [tuple(row["process"][key] for key in ("pid", "started_utc"))
                 for row in rows if row["process"]]
    assert len(processes) == len(set(processes))
    for row in rows:
        if "stdout_name" not in row:
            assert row["stage"] in {"not_run_environment", "not_run_input", "process_launch_failed"}
            continue
        for stream in ("stdout", "stderr"):
            data = (directory / row[f"{stream}_name"]).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row[f"{stream}_sha256"], row["id"]
            assert len(data) == row[f"{stream}_bytes"], row["id"]
        if row["stage"] in {"observed", "unsupported_call"}:
            actual = json.loads((directory / row["stdout_name"]).read_bytes())
            for key in ("id", "stage", "process", "runtime"):
                assert actual[key] == row[key], (row["id"], key)
            assert actual.get("observation") == row["observation"], row["id"]
            assert actual.get("error") == row.get("error"), row["id"]
            assert row["runtime"] == environment["versions"][row["version"]]["loaded"], row["id"]


def fit(row, inputs):
    if row["stage"] != "observed" or row["exit_code"] != 0:
        return None
    value = row["observation"]
    if row["case"] == "5595":
        return value["before_save"]["palette_prefix"] == inputs["5595"]["literal"]["palette"]
    out = value["output"]
    if out["mode"] != "RGBA" or out["channel_count"] != 4:
        return False
    alpha = inputs["5593"]["png"]["alpha_by_index"]
    return all(entry["rgba_or_rgb"][3] == alpha[int(index)]
               for index, group in out["output_by_input_index"].items() for entry in group)


def outcome(values):
    if None in values:
        return "unverified"
    return {0: "neither_fits", 1: "one_fits", 2: "both_fit"}[sum(values)]


def summarize(rows, calibration, inputs, sources):
    main = [r for r in rows if r["kind"] == "main"]
    assert {r["id"] for r in main} == {
        f"{case}-{version}-{call}-{repeat}"
        for case, calls in CALLS.items() for version in VERSIONS for call in calls for repeat in (1, 2)
    }
    assert len(main) == 24
    expected_origin = {"5593": inputs["5593"]["png"]["sha256"], "5595": inputs["5595"]["sha256"]}
    groups = defaultdict(list)
    for row in main:
        case = row["case"]
        assert row["input_sha256"] == expected_origin[case]
        if row["stage"] == "observed":
            obs = row["observation"]
            if case == "5593":
                assert obs["input_label_counts"] == inputs[case]["png"]["counts_by_index"]
                assert obs["source_indices_unchanged"]
                assert obs["input_before_load"]["transparency"] == 0
                groups_out = obs["output"]["output_by_input_index"]
                assert {index: sum(g["count"] for g in group) for index, group in groups_out.items()} == obs["input_label_counts"]
                for name, xy in inputs[case]["probe_xy"].items():
                    assert obs["output"]["points"][name]["xy"] == xy
            else:
                assert obs["before_attach_index_0_0"] == 1
                assert obs["input_palette_after_attach"] == inputs[case]["literal"]["palette"]
        groups[(case, row["version"], row["call"])].append(row)

    repeat = {}
    fits = {}
    for group, entries in groups.items():
        observed = all(r["stage"] == "observed" and r["exit_code"] == 0 for r in entries)
        repeat[group] = observed and entries[0]["observation"] == entries[1]["observation"]
        fits[group] = fit(entries[0], inputs) if repeat[group] else None
    decisions = {}
    for case, calls in CALLS.items():
        decisions[case] = {}
        for version in VERSIONS:
            values = {call: fits[(case, version, call)] for call in calls}
            decisions[case][version] = {"fit": values, "outcome": outcome(list(values.values()))}

    sources_counted = [row for row in sources if row["counted"]]
    assert len({s["id"] for s in sources}) == len(sources)
    assert len({s["fixed_url"] for s in sources_counted}) == len(sources_counted)
    byte_digests = [s["sha256"] for s in sources_counted if "sha256" in s]
    assert len(byte_digests) == len(set(byte_digests))
    category_counts = Counter(row["category"] for row in sources_counted)
    assert all(category_counts[key] >= minimum for key, minimum in MINIMUM_SOURCES.items())

    pairs = Counter(decision["outcome"] for case in decisions.values() for decision in case.values())
    experimental_stages = Counter((r["kind"], r["stage"]) for r in rows)
    return {
        "main": {"planned": len(main), "observed": experimental_stages[("main", "observed")],
                 "missing_or_failed": len(main) - experimental_stages[("main", "observed")],
                 "per_case": dict(Counter(row["case"] for row in main if row["stage"] == "observed"))},
        "repetitions": {"groups": len(repeat), "matching": sum(repeat.values()),
                        "mismatching_or_unobserved": len(repeat) - sum(repeat.values())},
        "comparisons": {"pairs": len(VERSIONS) * len(CALLS), **dict(sorted(pairs.items())),
                        "neither_fits": pairs["neither_fits"], "unverified": pairs["unverified"],
                        "by_case_and_version": decisions},
        "auxiliary": {"planned": len(rows) - len(main),
                      "by_kind_and_stage": {f"{kind}/{stage}": n for (kind, stage), n
                                            in sorted(experimental_stages.items()) if kind != "main"}},
        "calibration": dict(Counter(r["stage"] for r in calibration)),
        "sources": {"rows": len(sources), "counted": len(sources_counted), "excluded": len(sources) - len(sources_counted),
                    "counted_by_category": dict(sorted(category_counts.items()))},
    }


def compare_replay(original, replay):
    right = {r["id"]: r for r in replay}
    assert {r["id"] for r in original} == set(right)
    differences = []
    for row in original:
        other = right[row["id"]]
        if any(row.get(key) != other.get(key) for key in ("stage", "exit_code", "input_sha256", "observation", "error")):
            differences.append(row["id"])
    assert not differences, differences
    return len(right)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument("--replay-dir", type=Path)
    args = parser.parse_args()
    rows = read_rows(HERE / "runs.jsonl")
    calibration_dir = HERE / "evidence/calibration"
    calibration = read_rows(calibration_dir / "ledger.jsonl")
    sources = read_rows(HERE / "sources.jsonl")
    inputs = json.loads((HERE / "inputs.json").read_bytes())
    environment = json.loads((HERE / "environment.json").read_bytes())
    check_receipts(rows, HERE / "evidence/experiment", environment)
    check_receipts(calibration, calibration_dir, environment)
    summary = summarize(rows, calibration, inputs, sources)
    destination = HERE / "evidence/reconciliation.json"
    if args.write_summary:
        destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        assert summary == json.loads(destination.read_bytes())
    if args.replay_dir is not None:
        summary["fresh_replay_matching_rows"] = {
            "experiment": compare_replay(rows, read_rows(args.replay_dir / "experiment/ledger.jsonl")),
            "calibration": compare_replay(calibration, read_rows(args.replay_dir / "calibration/ledger.jsonl")),
        }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
