"""Independently reconcile roster, output, policy, measured events and source quotas."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
from statistics import median
import subprocess

from common import ROOT, json_in, read_csv, read_jsonl, sha, write_json

EVIDENCE = ROOT / "evidence"


def visible(cell):
    fields = ("argument_before", "argument_after", "original_before", "original_after", "p_before", "p_after")
    outcome = dict(cell["result"])
    outcome.pop("stack", None)
    return outcome, tuple(cell[field] for field in fields)


def clean_values(run):
    if run["status"] != "ok":
        return {}
    return {c["id"]: (visible(c), c["accessor_trace"], c["input_sha256"]) for c in run["cases"]
            if c["result"]["type"] != "timeout"}


def check_roster_and_order(data, releases, runs):
    contexts = {(x["package"],x["version"]): x for x in releases}
    expected = {}
    for p in data["cohorts"]:
        pkg = p["package"]
        seq = [r["version"] for r in p["selected"]]
        assert len(seq) == (8 if pkg == "simple-statistics" else 16)
        assert [contexts[(pkg,v)]["publish_rank"] for v in seq] == list(range(1,len(seq)+1))
        assert {v: contexts[(pkg,v)]["semver_rank"] for v in seq} == {v: i for i,v in enumerate(seq,1)}
        expected[pkg] = seq
    assert len(runs) == 48
    lock = json_in(ROOT / "replay/locks.json")
    raw = Counter()
    for row in runs:
        key = (row["package"],row["version"])
        ref = contexts[key]
        locked = lock["/".join(key)]["lock"]
        locked_hash = sha((json.dumps(locked, ensure_ascii=False, indent=2)+"\n").encode())
        assert locked_hash == row["lock_sha256"] == ref["lock_sha256"]
        if row["status"] == "ok":
            assert row["entry"] == ref["entry"] and row["entry_sha256"] == ref["entry_sha256"]
            assert row["loader"] == ref["loader"] and row["direct"] == ref["direct"]
        raw[row["status"]] += 1
    assert raw == {"ok":46,"load_error":2}, raw
    remotes = read_jsonl(EVIDENCE / "remote-reads.jsonl")
    prediction = next(x for x in remotes if x["path"].endswith("/predictions.csv"))
    output = next(x for x in remotes if x["path"].endswith("/output-pairs.csv"))
    assert prediction["matches"] and output["matches"]
    assert datetime.fromisoformat(prediction["read_utc"]) < min(datetime.fromisoformat(r["opened_utc"]) for r in runs)
    subprocess.run(["git","merge-base","--is-ancestor",prediction["commit"],output["commit"]],check=True)
    return expected, dict(raw)


def check_outputs(expected, runs, output_rows, fresh):
    a = {(r["package"],r["version"]): r for r in runs if r["label"] == "A"}
    b = {(r["package"],r["version"]): r for r in runs if r["label"] == "B"}
    consensus = {}
    for key in a:
        left, right = clean_values(a[key]), clean_values(b[key])
        assert left == right
        consensus[key] = left
    seen = Counter()
    for row in output_rows:
        p, older, newer, fn = (row[k] for k in ("package","previous","version","function"))
        assert expected[p].index(newer) == expected[p].index(older)+1
        cell = row["cell"]
        assert cell.split("/")[0] == fn
        left, right = consensus[(p,older)].get(cell), consensus[(p,newer)].get(cell)
        status = "unconfirmed" if left is None or right is None else "changed" if left[0] != right[0] else "unchanged"
        assert status == row["state"]
        if left is not None and right is not None:
            assert left[-1] == right[-1] == row["input_sha256"]
            assert (left[1] != right[1]) == (row["trace_changed"] == "True")
        seen[status] += 1
    assert sum(seen.values()) == sum((len(versions)-1)*a[(pkg,versions[0])]["case_count"] for pkg, versions in expected.items())
    for path in fresh:
        for row in read_jsonl(path):
            same = a[(row["package"],row["version"])]
            assert row["status"] == same["status"]
            if row["status"] == "ok":
                assert clean_values(row) == clean_values(same)
                assert row["inputs_sha256"] == same["inputs_sha256"] and row["lock_sha256"] == same["lock_sha256"]
                assert row["entry_sha256"] == same["entry_sha256"]
            else:
                assert row["error"]["code"] == same["error"]["code"]
    return dict(seen)


def check_scores(outputs, predictions):
    policies = ("A","C","D","E","E2")
    sealed = {(r["package"],r["previous"],r["version"],r["function"]):r for r in predictions if r["previous"]}
    tally = defaultdict(Counter)
    for side in outputs:
        p, old, v, f, layer = (side[k] for k in ("package","previous","version","function","layer"))
        pred = sealed[p,old,v,f]
        for policy in policies:
            for scope in (layer,"ALL_CELLS"):
                counts = tally[p,f,scope,policy]
                counts["forced"] += int(pred[policy] == "forced")
                if side["state"] == "unconfirmed":
                    counts["unconfirmed"] += 1
                elif side["state"] == "changed":
                    counts["fn" if pred[policy]=="skip" else "tp"] += 1
                elif side["state"] == "unchanged":
                    counts["tn" if pred[policy]=="skip" else "fp"] += 1
    actual = read_csv(EVIDENCE / "policy-cells.csv")
    assert len(actual) == len(tally)
    for row in actual:
        count = tally[tuple(row[k] for k in ("package","function","layer","policy"))]
        for k in ("forced","unconfirmed","tp","fp","fn","tn"):
            assert int(row[k]) == count[k]
        assert int(row["total"]) == sum(count[k] for k in ("unconfirmed","tp","fp","fn","tn"))
    return len(tally)


def check_costs(releases):
    groups = defaultdict(list)
    costs = read_csv(ROOT / "costs.csv")
    events = {r["event_id"]:r["events"] for r in read_jsonl(EVIDENCE / "cost-events.jsonl")}
    answers = {r["event_id"]:r for r in read_jsonl(EVIDENCE / "cost-answers.jsonl")}
    phases = read_jsonl(EVIDENCE / "cost-phases.jsonl")
    states = ("correct","wrong_carry","held","unknown","direct_disagreement")
    for row in costs:
        ident = row["event_id"]
        assert row["requested"] == answers[ident]["requested"]
        ev = events[ident]
        network = [e for e in ev if e["kind"]=="http" and e["cache"]=="miss"]
        assert int(row["actual_body_bytes"]) == sum(e["bytes"] or 0 for e in network)
        assert int(row["http_calls"]) == len(network)
        assert int(row["logical_hash_bytes"]) == sum(e["bytes"] for e in ev if e["kind"]=="logical_hash")
        assert int(row["node_probes"]) == sum(e["kind"]=="node_probe" for e in ev)
        assert int(row["installs"]) == sum(e["kind"]=="npm_ci" for e in ev)
        account, cell_ids = Counter(), set()
        for item in answers[ident]["outcomes"]:
            basis = item["basis"]
            if basis != "-":
                assert basis in releases[row["package"]]
                assert releases[row["package"]].index(basis) <= releases[row["package"]].index(row["requested"])
            assert not cell_ids.intersection(item["cells"])
            cell_ids.update(item["cells"])
            account[item["state"]] += len(item["cells"])
        assert [int(row[k]) for k in states] == [account[k] for k in states]
        assert len(cell_ids) == int(row["responses"])
        groups[tuple(str(row[k]) for k in ("package","sequence","policy","rep","cache"))].append(row)
    assert len(costs) == len(events) == len(answers) == 1080 and len(groups) == len(phases) == 120
    for phase in phases:
        key = tuple(str(phase[k]) for k in ("package","sequence","policy","rep","cache"))
        bucket = groups[key]
        expect = releases[phase["package"]]
        if phase["sequence"] == "ends":
            expect = [expect[0],expect[-1]]*3
        assert [r["requested"] for r in bucket] == expect
        for k in (*states,"responses","actual_body_bytes","logical_hash_bytes","installs","node_probes",
                  "http_non_200","body_unmeasured"):
            assert phase[k] == sum(int(r[k]) for r in bucket)
        assert phase["phase_wall_ms"] >= sum(float(r["wall_ms"]) for r in bucket) - 0.02
    for row in read_csv(EVIDENCE / "cost-summary.csv"):
        keys = ("package","sequence","policy","cache")
        matching = [r for r in phases if all(r[k]==row[k] for k in keys)]
        assert len(matching) == 3
        assert float(row["phase_wall_ms_median"]) == median(r["phase_wall_ms"] for r in matching)
    return {"queries":len(costs),"phases":len(phases),"answers":sum(int(row["responses"]) for row in costs)}


def source_counts():
    sources = read_jsonl(ROOT / "sources.jsonl")
    assert len({r["source_id"] for r in sources}) == len(sources)
    included = [r for r in sources if r["counted"]]
    counts = Counter(r["category"] for r in included)
    assert len({r["work_id"] for r in included}) == len(included)
    assert all(counts[k] >= n for k,n in {"package":6,"fixture":6,"distribution":6,"transit":3,"statistics":3}.items()), counts
    return {"opened_rows":len(sources),"unique_counted":len(included),"by_category":dict(counts)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rebuilt", type=Path)
    p.add_argument("--fresh-run", type=Path, action="append", default=[])
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    runs = read_jsonl(ROOT / "runs.jsonl")
    releases, receipts = check_roster_and_order(json_in(EVIDENCE / "roster.json"),
                                               json_in(EVIDENCE / "release-data.json"), runs)
    cells = read_csv(EVIDENCE / "output-cells.csv")
    if args.rebuilt:
        for f in ("output-cells.csv","output-pairs.csv"):
            assert (EVIDENCE/f).read_bytes() == (args.rebuilt/f).read_bytes(), f
    result = {"release_statuses":receipts, "cells":check_outputs(releases, runs, cells, args.fresh_run),
              "policy_groups":check_scores(cells, read_csv(ROOT / "predictions.csv")),
              "costs":check_costs(releases), "sources":source_counts(),
              "fresh_runs":{str(path):sha(path.read_bytes()) for path in args.fresh_run}}
    if args.out:
        write_json(args.out,result)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
