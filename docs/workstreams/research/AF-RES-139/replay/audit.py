"""Recount the committed evidence with independent equations and a fresh optional run."""
import argparse
import csv
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGNAL_SEAL = "38ac75a5a8196575216e6c0d6644e3c5c0769902"
OUTPUT_SEAL = "0e0185ecb9500fc84f9eb995999b5ad7e0036412"
POLICIES = "A C D E F N E_absence".split()


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def jsonlines(path):
    with path.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source]


def csvrows(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def command(*args):
    return subprocess.check_output(args, cwd=ROOT)


def snapshot(run):
    return {
        case["cell"]: (
            tuple(sorted((k, json.dumps(v)) for k, v in case["result"].items() if k != "stack")),
            json.dumps([case[name] for name in ("argument_before", "argument_after", "original_before", "original_after")]),
            case["argument_mutated"], case["original_mutated"],
        )
        for case in run["cases"]
    }


def audit_runtime(fresh):
    roster = read_json("evidence/roster.json")
    specs = read_json("replay/inputs.json")
    included = [r for r in csvrows("releases.csv") if r["status"] == "included"]
    versions = [r["version"] for r in included]
    assert len(versions) == 30
    assert sorted(versions, key=lambda v: tuple(map(int, v.split(".")))) == roster["semver_order"]
    assert [r["version"] for r in sorted(included, key=lambda r: r["publish_utc"])] == roster["published_order"]
    assert all(r["verified_sha1"] == r["verified_sha512"] == "True" and r["direct"] == "{}" for r in included)
    by_release = {r["version"]: r for r in included}
    assert Counter(r["tag_status"] for r in included) == {"match": 29, "different_from_gitHead": 1}
    ids = {
        f"{function}/{label}/{p}/{mode}"
        for function, label, mode in itertools.product(specs["functions"], specs["arrays"], specs["modes"])
        for p in (specs["quantile_p"] if function == "quantile" else ["-"])
    }
    input_sha = hashlib.sha256((ROOT / "replay/inputs.json").read_bytes()).hexdigest()
    runs = jsonlines(ROOT / "runs.jsonl")
    groups = {(run["cohort"], run["intended_version"]): run for run in runs}
    assert len(groups) == len(runs) == 60
    for run in runs:
        reference = by_release[run["intended_version"]]
        assert (run["status"], run["mode"], run["entry_relative"]) == ("ok", "require", "dist/simple-statistics.js")
        assert run["version"] == run["intended_version"] and run["runtime"] == specs["node"]
        assert run["entry_sha256"] == reference["entry_sha256"]
        assert run["lock_sha256"] == run["lock_before"] == run["lock_after_install"] == reference["lock_sha256"]
        assert run["archive_sha256"] == reference["archive_sha256"] and run["inputs_sha256"] == input_sha
        assert run["direct"] == {}
        assert len(run["cases"]) == len(ids) == 126 and {case["cell"] for case in run["cases"]} == ids
        for case in run["cases"]:
            expected = [{"type": "number", "value": x} for x in specs["arrays"][case["input_id"]]]
            ordered = sorted(expected, key=lambda t: (t["value"] == "NaN", t["value"] if t["value"] != "NaN" else 0))
            assert case["original_before"] == case["original_after"] == expected
            assert case["argument_before"] == case["argument_after"] == (ordered if case["mode"] == "sorted_copy" else expected)
            assert not case["argument_mutated"] and not case["original_mutated"]
    reference = {v: snapshot(groups["A", v]) for v in versions}
    assert all(reference[v] == snapshot(groups["B", v]) for v in versions)
    fresh_count = 0
    if fresh is not None:
        reruns = jsonlines(fresh)
        assert sorted(r["intended_version"] for r in reruns) == sorted(reference)
        for run in reruns:
            assert run["status"] == "ok" and run["launch_path"] not in {r["launch_path"] for r in runs}
            assert run["inputs_sha256"] == input_sha and run["lock_sha256"] == by_release[run["version"]]["lock_sha256"]
            assert snapshot(run) == reference[run["version"]]
            fresh_count += len(run["cases"])
    assert len({run["npm_cache"] for run in runs}) == 2 and len({run["launch_path"] for run in runs}) == 60
    output = {(r["order"], r["before"], r["after"], r["cell"]): r for r in csvrows("evidence/output-comparison.csv")}
    expected_output = {}
    for label, key in (("publish", "published_order"), ("semver", "semver_order")):
        for a, b in itertools.pairwise(roster[key]):
            for case_id in ids:
                expected_output[label, a, b, case_id] = int(reference[a][case_id] != reference[b][case_id])
    assert set(output) == set(expected_output)
    assert all(output[key]["state"] == ("changed" if changed else "same") for key, changed in expected_output.items())
    modes = Counter()
    raw_types = Counter()
    for v in versions:
        cases = {c["cell"]: c for c in groups["A", v]["cases"]}
        raw_types.update(c["result"]["type"] for c in cases.values())
        for cell in cases.values():
            if cell["mode"] == "direct":
                modes["total"] += 1
                paired = cases[cell["cell"].replace("/direct", "/sorted_copy")]
                modes["different"] += reference[v][cell["cell"]][0] != reference[v][paired["cell"]][0]
        for label, mode in itertools.product(specs["arrays"], specs["modes"]):
            assert reference[v][f"median/{label}/-/{mode}"] == reference[v][f"quantile/{label}/0.5/{mode}"]
    assert modes == {"total": 1890, "different": 120}
    pair_truth = csvrows("evidence/output-pairs.csv")
    assert len(pair_truth) == 58 and all(row["state"] == "same" and row["same_cells"] == "126" for row in pair_truth)
    assert len(output) == 7308 and sum(expected_output.values()) == 0
    contrasts = csvrows("evidence/matched-direct.csv")
    assert len(contrasts) == 58 and all(row["status"] == "no_direct_dependencies_in_either_release" for row in contrasts)
    return reference, roster, {"releases": len(versions), "primary_raw_runs": len(runs), "pair_cell_rows": len(output),
                              "paired_runtime_agreement": len(ids) * len(versions), "outcome_types_A": dict(raw_types),
                              "within_version_modes": dict(modes), "fresh_cells": fresh_count}


def audit_signals():
    signals = {(r["order"], r["version"], r["function"]): r for r in csvrows("signals.csv")}
    rows = csvrows("evidence/cell-scores.csv")
    primary = {}
    for r in rows:
        policy, function = r["policy"], r["cell"].split("/")[0]
        level = "any" if r["execution_scope"] == "package" else function
        series = [v for (order, _, fn), v in signals.items() if (order, fn) == (r["order"], level) and v["previous"]]
        forced = [v["current_only_absence"] == "True" if level != "any" else
                  signals[r["order"], v["version"], "median"]["current_only_absence"] == "True" for v in series]
        actions = [("force" if missing else v["E"]) if policy == "E_absence" else v[policy] for v, missing in zip(series, forced)]
        fp = sum(act != "skip" for act in actions)
        tn = len(actions) - fp
        assert all(int(r[name]) == 0 for name in ("TP", "FN", "unknown", "forced_notice_time"))
        assert int(r["FP"]) == fp and int(r["TN"]) == tn and int(r["forced"]) == actions.count("force")
        assert len(series) == int(r["eligible"]) == 29 and not r["sensitivity"]
        for scenario in ("unknown_all_changed", "unknown_all_same"):
            assert [r[scenario + "_" + key] for key in ("TP", "FP", "FN", "TN")] == [r[key] for key in ("TP", "FP", "FN", "TN")]
        if r["order"] == "publish" and r["cell"] == "any" and r["execution_scope"] == "package":
            primary[policy] = {"FP": fp, "TN": tn, "forced": actions.count("force")}
    assert len(rows) == 3612 and len(csvrows("decisions.csv")) == 7482
    assert {policy: item["FP"] for policy, item in primary.items()} == {"A": 29, "C": 0, "D": 23, "E": 2, "F": 2, "N": 1, "E_absence": 5}
    return primary


def audit_costs(reference, roster, primary):
    costs = csvrows("costs.csv")
    summaries = csvrows("evidence/cost-summary.csv")
    versions = roster["published_order"]
    expected = {"pinned": [versions[0]], "each_publish": versions, "dual": [versions[0], versions[-1]] * 3}
    columns = ("correct", "wrong_carry", "held", "document_body_bytes", "archive_body_bytes", "hash_files",
               "hash_read_bytes", "executions", "answer_cache_hits", "forced_executions", "notice_time_forced_edges_read")
    assert len(costs) == 518 and len(summaries) == 42
    for group in summaries:
        scenario, policy, mode = [group[key] for key in ("scenario", "policy", "mode")]
        matching = [r for r in costs if (r["scenario"], r["policy"], r["mode"]) == (scenario, policy, mode)]
        assert [r["requested_release"] for r in matching] == expected[scenario]
        execs = 1 + primary[policy]["FP"] if mode == "batch" or scenario == "each_publish" else (
            2 if scenario == "dual" and primary[policy]["FP"] else 1)
        assert sum(int(r["executions"]) for r in matching) == execs
        assert sum(int(r["answer_cache_hits"]) for r in matching) == (4 if scenario == "dual" else 0)
        for r in matching:
            carrier = r["last_measured_release"]
            target = r["requested_release"]
            assert carrier in reference and r["returned_release"] == target and r["disposition"] == "correct"
            assert sum(reference[carrier][c] != val for c, val in reference[target].items()) == int(r["cells_different"])
        for field in columns:
            assert all(int(r[field]) >= 0 for r in matching)
            assert int(group["first_" + field]) == int(matching[0][field])
            assert int(group["repeat_" + field]) == sum(int(r[field]) for r in matching[1:])
    return {"query_rows": len(costs), "summary_rows": len(summaries),
            "dispositions": dict(Counter(r["disposition"] for r in costs))}


def audit_sources():
    rows = jsonlines(ROOT / "sources.jsonl")
    source_ids = {x["source_id"]: x for x in rows}
    counted = [r for r in rows if r["counted_unique"]]
    assert len(source_ids) == len(rows)
    assert all(row["access_status"] == "opened" and row["locator"] and row["opened_utc"] for row in counted)
    assert len({r["work_id"] for r in counted}) == len(counted)
    stats = Counter(r["category"] for r in counted)
    assert all(stats[category] >= minimum for category, minimum in
               {"package": 6, "change": 6, "distribution": 4, "statistics": 3, "transit": 3}.items())
    for row in csvrows("domain-cells.csv"):
        assert all(source_ids[row[key]]["access_status"] == "opened" for key in ("before_source", "after_source", "notice_source"))
        assert (row["before_value"] != row["after_value"]) == (row["state"] == "changed")
    assert not any(r["counted_unique"] for r in rows if r["access_status"] == "failed")
    return {"ledger_rows": len(rows), "unique_counted": len(counted), "categories": dict(stats),
            "domain_cells": len(csvrows("domain-cells.csv")), "ONS_exact_workbook_opened": 0}


def seal():
    prefix = ROOT.relative_to(Path(command("git", "rev-parse", "--show-toplevel").decode().strip())).as_posix()
    for name, commit in {"signals.csv": SIGNAL_SEAL, "evidence/output-comparison.csv": OUTPUT_SEAL}.items():
        assert command("git", "show", f"{commit}:{prefix}/{name}") == (ROOT / name).read_bytes()
    scope = read_json("manifest.json")["base_commit"]
    paths = command("git", "diff", "--name-only", scope, "HEAD").decode().splitlines()
    assert all(path.startswith(prefix + "/") for path in paths)
    assert all(not path.endswith("dot-control.json") for path in paths)
    sealed_at = datetime.fromtimestamp(int(command("git", "show", "-s", "--format=%ct", SIGNAL_SEAL)), tz=datetime.now().astimezone().tzinfo)
    earliest_run = min(datetime.fromisoformat(r["started_utc"]) for r in jsonlines(ROOT / "runs.jsonl"))
    assert sealed_at < earliest_run
    return {"sealed_signal_sha": SIGNAL_SEAL, "sealed_output_sha": OUTPUT_SEAL,
            "checked_sha": command("git", "rev-parse", "HEAD").decode().strip(),
            "paths_inside_ownership": len(paths), "signal_seal_before_runtime": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fresh-run", type=Path)
    args = parser.parse_args()
    reference, roster, runtime = audit_runtime(args.fresh_run)
    policies = audit_signals()
    costs = audit_costs(reference, roster, policies)
    sources = audit_sources()
    result = (ROOT / "RESULT.md").read_text(encoding="utf-8")
    assert "## 표 1" in result.splitlines()[0]
    tail = result.strip().splitlines()[-5:]
    assert tail[0].startswith("| 중요한 불일치·약점") and all(line.startswith("|") for line in tail)
    print(json.dumps({"git": seal(), "runtime": runtime, "public_pair_counts": policies, "costs": costs, "sources": sources},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
