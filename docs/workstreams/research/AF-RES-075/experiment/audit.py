"""Check ledger joins, evidence, dimensions and stable replay fingerprints."""
import argparse
import collections
import itertools
import json
from pathlib import Path

from registry import CLAIMS, ENTRYPOINTS, ROOT, STATES, VIEWS, encode, sha, write_json

EVIDENCE = ("sealed.json", "truth.jsonl", "projections.jsonl", "input-boundary.json",
            "losses.jsonl", "swap.jsonl")
STABLE = ("pairs.csv", "runs.jsonl", "scores.csv", "costs.csv", *EVIDENCE)
GRADE = ("correct", "wrong", "defer")


def json_lines(path):
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def csv_rows(path):
    import csv

    with path.open(encoding="utf8", newline="") as data:
        reader = csv.DictReader(data)
        rows = list(reader)
        assert len(reader.fieldnames) == len(set(reader.fieldnames))
        assert all(None not in row and None not in row.values() for row in rows), path
    return rows, len(reader.fieldnames)


def index(rows, fields):
    located = {tuple(row[field] for field in fields): row for row in rows}
    assert len(located) == len(rows), fields
    return located


def workfile(root, name, committed):
    return root / "evidence" / name if committed and name in EVIDENCE else root / name


def replay_compare(root, replay):
    checked = {}
    for name in STABLE:
        committed = workfile(root, name, True)
        replica = workfile(replay, name, False)
        assert committed.read_bytes() == replica.read_bytes(), name
        checked[name] = sha(replica.read_bytes())
    views = [path.relative_to(replay) for path in (replay / "views").glob("*.json")]
    committed = {path.name for path in (root / "evidence/views").glob("*.json")}
    assert committed == {view.name for view in views}
    for view in views:
        other = root / "evidence" / view
        assert (replay / view).read_bytes() == other.read_bytes(), view
        assert sha(other.read_bytes()) == view.stem
    return {"stable_sha256": checked, "projection_blobs_identical": len(views),
            "timings_compared": False}


def aggregate(scores, costs):
    grouped = []
    by_id = index(costs, ("run_id",))
    for claim, view, state in itertools.product(CLAIMS, VIEWS, STATES):
        group = [row for row in scores if (row["claim"], row["view"], row["state"]) == (claim, view, state)]
        cases = {row["pair_id"] for row in group}
        assert len(cases) == len(group) == 16
        selected_costs = [by_id[(row["run_id"],)] for row in group]
        measures = {key: sum(int(row[key]) for row in selected_costs)
                    for key in (
                        "build_bytes", "logical_records", "stored_read_bytes", "origin_local_requests",
                        "historical_initial_requests", "historical_post_defer_requests", "current_requests",
                        "local_file_reads", "local_read_bytes", "historical_read_bytes", "current_read_bytes",
                        "post_defer_read_bytes",
                    )}
        outcomes = {stage: {status: sum(row[stage] == status for row in group) for status in GRADE}
                    for stage in ("display", "historical", "current")}
        assert all(sum(statuses.values()) == 16 for statuses in outcomes.values())
        grouped.append({"claim": claim, "view": view, "state": state, "denominator": len(cases),
                        **outcomes, "measures": measures})
    return grouped


def check_grade(label, expected, actual):
    if actual["status"] == "deferred":
        assert actual["value"] is None and actual["notes"] and label == "defer"
    else:
        assert actual["status"] == "resolved"
        assert label == ("correct" if expected == actual["value"] else "wrong")


def validate(root):
    pairs, pair_cols = csv_rows(root / "pairs.csv")
    scores, score_cols = csv_rows(root / "scores.csv")
    costs, cost_cols = csv_rows(root / "costs.csv")
    primary = {row["pair_id"] for row in pairs if row["kind"] != "supplemental"}
    assert len(pairs) == 17 and len(primary) == 16 and len(index(pairs, ("pair_id",))) == 17
    assert collections.Counter((row["domain"], row["kind"]) for row in pairs
                               if row["pair_id"] in primary) == {
                                   ("PG", "natural"): 4, ("PG", "injected"): 4,
                                   ("TZ", "natural"): 4, ("TZ", "injected"): 4,
                               }
    cases = index(pairs, ("pair_id",))
    truth = index(json_lines(root / "evidence/truth.jsonl"), ("pair_id", "phase"))
    assert set(truth) == set(itertools.product((row["pair_id"] for row in pairs), ("before", "after")))
    for (pair, phase), row in truth.items():
        fixture = root / cases[(pair,)][f"{phase}_path"]
        raw = fixture.read_bytes()
        assert sha(raw) == row["asset_sha256"] == cases[(pair,)][f"{phase}_sha256"]
        lines = raw.decode().splitlines()
        assert row["exists"] == (len(row["eligible"]) > 0)
        assert row["unique"] == (len(row["eligible"]) == 1)
        point = max((score for _, score in row["eligible"]), default=None)
        assert row["top"] == sorted(row_id for row_id, score in row["eligible"] if score == point)
        assert [r["id"] for r in row["citations"]] == [row_id for row_id, _ in row["eligible"]]
        for cite in row["citations"]:
            assert cite["clause_sha256"] == sha(lines[cite["line"] - 1].encode())

    runs = json_lines(root / "runs.jsonl")
    assert len(runs) == len(scores) == len(costs) == 288
    run_keys = {(row["pair_id"], row["input"]["claim"], row["input"]["view"], row["state"]) for row in runs}
    assert run_keys == set(itertools.product(primary, CLAIMS, VIEWS, STATES))
    keyed_runs = index(runs, ("run_id",))
    score_by_id = index(scores, ("run_id",))
    cost_by_id = index(costs, ("run_id",))
    assert keyed_runs.keys() == score_by_id.keys() == cost_by_id.keys()
    for key, run in keyed_runs.items():
        row = score_by_id[key]
        cost = cost_by_id[key]
        logged = run["input"]
        claim, view, state = logged["claim"], logged["view"], run["state"]
        assert not run["exit"] and not run["error"] and not run["stderr"]
        assert (row["pair_id"], row["claim"], row["view"], row["state"], row["pair_weight"]) == (
            run["pair_id"], claim, view, state, "1")
        assert (cost["pair_id"], cost["claim"], cost["view"], cost["state"]) == (
            run["pair_id"], claim, view, state)
        assert logged["entrypoint"] == ENTRYPOINTS[logged["domain"]]
        projection = (root / "evidence" / logged["projection_path"]).read_bytes()
        assert len(projection) == int(cost["build_bytes"]) == int(cost["stored_read_bytes"])
        assert sha(projection) == logged["projection_sha256"] == cost["projection_sha256"]
        record = json.loads(projection)
        request = {key: logged[key] for key in ("domain", "query", "claim", "view", "entrypoint")}
        wire = encode(request | {"record": record})
        assert len(wire) == logged["wire_bytes"] and sha(wire) == logged["wire_sha256"]
        for event in run["reads"]:
            assert event["entrypoint"] == logged["entrypoint"]
            if event["status"] == "available":
                phase = "before" if event["slot"] == "historical" else "after"
                assert event["asset_sha256"] == truth[(run["pair_id"], phase)]["asset_sha256"]
                file = root / cases[(run["pair_id"],)][f"{phase}_path"]
                assert event["source_read_bytes"] == file.stat().st_size <= event["raw_budget_bytes"]
            else:
                assert event["status"] == "historical_unavailable" and state == "lost"
                assert event["source_read_bytes"] == 0 and event["local_file_reads"] == 0
        assert [event["sequence"] for event in run["reads"]] == list(range(1, len(run["reads"]) + 1))
        assert sum(event["slot"] == "current" for event in run["reads"]) == int(cost["current_requests"]) == 1
        assert len(run["reads"]) == int(cost["origin_local_requests"])
        assert sum(event["source_read_bytes"] for event in run["reads"]) == int(cost["local_read_bytes"])
        assert sum(event["local_file_reads"] for event in run["reads"]) == int(cost["local_file_reads"])
        outcome = run["decision"]
        assert row["display"] == "correct" and outcome["display"] == record["display"][claim]
        for stage, phase in (("historical", "before"), ("current", "after")):
            oracle_val = truth[(run["pair_id"], phase)][claim]
            assert json.loads(row[f"oracle_{phase}_json"]) == oracle_val
            check_grade(row[stage], oracle_val, outcome[stage])

    boundary = json.loads((root / "evidence/input-boundary.json").read_bytes())
    assert len(boundary["top_level_canaries"]) == 5
    assert all(row["exit"] == 2 and row["route_reads"] == 0
               and row["result"] == "unexpected request field" for row in boundary["top_level_canaries"])
    assert boundary["display_before"] != boundary["display_after"]
    assert boundary["historical_unchanged"] and boundary["current_unchanged"]
    assert boundary["forbidden_route"] == "route_rejected" and boundary["forbidden_route_reads"] == 0
    assert boundary["oracle_input_path_is_separate"] and boundary["reader_cwd_empty"]

    loss = json_lines(root / "evidence/losses.jsonl")
    swap = json_lines(root / "evidence/swap.jsonl")
    assert len(index(loss, ("run_id",))) == 16 and len(index(swap, ("run_id",))) == 18
    for row in loss:
        expected = truth[("TZ-C01", "after")][row["input"]["claim"]]
        assert not row["error"] and row["exit"] == 0 and expected == row["oracle_historical"]
        outcome = "correct" if row["state"] == "retained" else (
            "wrong" if row["pair_id"] == "LOSS03" else "defer"
        )
        assert row["historical_grade"] == outcome
        check_grade(outcome, expected, row["decision"]["historical"])
        if row["pair_id"] == "LOSS01":
            assert row["unsafe_subset_value"] != expected
    swapped = [truth[("SWAP01", phase)] for phase in ("before", "after")]
    assert swapped[0]["scanned"] == swapped[1]["scanned"]
    assert len(swapped[0]["eligible"]) == len(swapped[1]["eligible"])
    first_before, first_after = (row["citations"][0] for row in swapped)
    assert first_before["id"] == first_after["id"]
    assert first_before["clause_sha256"] == first_after["clause_sha256"]
    assert swapped[0]["top"] != swapped[1]["top"]

    changes = {}
    for pair in sorted(primary):
        before, after = (truth[(pair, phase)] for phase in ("before", "after"))
        changes[pair] = [claim for claim in CLAIMS if before[claim] != after[claim]]
    return {
        "primary_pairs": len(primary), "claims": len(CLAIMS), "views": len(VIEWS), "states": len(STATES),
        "primary_judgments": len(runs), "independent_reads": len(truth), "swap_judgments": len(swap),
        "loss_judgments": len(loss), "leak_canaries_rejected": len(boundary["top_level_canaries"]),
        "csv_shapes": {"pairs_with_swap": [len(pairs), pair_cols], "scores": [len(scores), score_cols],
                       "costs": [len(costs), cost_cols]},
        "changes": changes, "aggregates": aggregate(scores, costs),
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--root", type=Path, default=ROOT)
    cli.add_argument("--replay", type=Path, action="append", default=[])
    cli.add_argument("--receipt", type=Path)
    args = cli.parse_args()
    report = validate(args.root)
    report["replay_comparisons"] = [replay_compare(args.root, replay) for replay in args.replay]
    if args.receipt:
        write_json(args.receipt, report)
    print(f"Audited {report['primary_judgments']} main, {report['swap_judgments']} swap, "
          f"{report['loss_judgments']} loss rows; {len(args.replay)} stable replay comparisons")
