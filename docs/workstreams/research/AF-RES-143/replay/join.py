"""Join the separately sealed outputs and predictions without editing either ledger."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path

from common import ROOT, json_in, read_csv, write_csv, write_json

POLICIES = ("A", "C", "D", "E", "E2")
CONTRACT = {"scalar-contract", "vector-contract", "empty", "accessor-contract"}


def edge(cell, scope):
    return (cell["package"], cell["previous"], cell["version"], scope)


def score(counter, state, action):
    counter["total"] += 1
    counter["forced"] += action == "forced"
    if state not in {"changed", "unchanged"}:
        counter[state] += 1
        if action != "skip":
            counter["unconfirmed_or_availability_checked"] += 1
        return
    counter["comparable"] += 1
    counter["positive"] += state == "changed"
    if state == "changed":
        counter["tp" if action != "skip" else "fn"] += 1
    else:
        counter["fp" if action != "skip" else "tn"] += 1


def result(group):
    states = {r["state"] for r in group}
    for state in ("changed", "availability", "unconfirmed"):
        if state in states:
            return state
    return "unchanged" if "unchanged" in states else "api_absent_both"


def predicted(rows, policy):
    actions = {r[policy] for r in rows}
    return "forced" if "forced" in actions else "alert" if "alert" in actions else "skip"


def join(predictions, outputs, all_releases, out):
    static = {edge(r,r["function"]): r for r in predictions if r["previous"]}
    evaluated = []
    layers, contracts, availability = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    buckets = defaultdict(list)
    for row in outputs:
        pred = static[edge(row,row["function"])]
        merged = row | {name: pred[name] for name in POLICIES}
        evaluated.append(merged)
        for policy in POLICIES:
            for scope in (row["layer"], "ALL_CELLS"):
                score(layers[(row["package"], row["function"], scope, policy)], row["state"], pred[policy])
        if row["layer"] in CONTRACT:
            for scope in (row["function"], "ALL"):
                buckets[edge(row,scope)].append(merged)
    edge_rows = []
    for (package, before, after, scope), group in buckets.items():
        state = result(group)
        fns = sorted({r["function"] for r in group})
        p_rows = [static[(package, before, after, fn)] for fn in fns]
        record = dict(package=package, previous=before, version=after, function=scope,
                      cells=len(group), state=state)
        for policy in POLICIES:
            action = predicted(p_rows, policy)
            record[policy] = action
            score(contracts[(package,scope,policy)], state, action)
        edge_rows.append(record)
    availability_rows = []
    healthy = {(r["package"],r["version"]): r for r in all_releases}
    for (package, before, after, scope), group in buckets.items():
        if scope != "ALL":
            continue
        sides = [healthy[(package,v)] for v in (before,after)]
        load_states = [r["status_a"] if r["status_a"] == r["status_b"] else "unconfirmed" for r in sides]
        if "load_error" not in load_states:
            continue
        row = dict(package=package, previous=before, version=after,
                   scope="public entry loadability", prior_state=load_states[0], next_state=load_states[1],
                   prior_error=sides[0]["error_a"], next_error=sides[1]["error_a"])
        fns = sorted({r["function"] for r in group})
        p_rows = [static[(package, before, after, fn)] for fn in fns]
        for policy in POLICIES:
            action = predicted(p_rows, policy)
            row[policy] = action
            availability[(package, policy)]["caught" if action != "skip" else "missed"] += 1
        availability_rows.append(row)
    metrics = ["total","comparable","positive","tp","fp","fn","tn","forced","unconfirmed",
               "availability","api_absent_both","unconfirmed_or_availability_checked"]
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "policy-cells.csv", [
        dict(package=p,function=f,layer=layer,policy=pol) | {key: counter[key] for key in metrics}
        for (p,f,layer,pol),counter in sorted(layers.items())
    ])
    write_csv(out / "policy-contract-edges.csv", edge_rows)
    write_csv(out / "policy-summary.csv", [
        dict(package=p,function=f,policy=pol) | {key: counter[key] for key in metrics} |
        {"availability_caught": availability[(p,pol)]["caught"] if f=="ALL" else "",
         "availability_missed": availability[(p,pol)]["missed"] if f=="ALL" else "",
         "recall": "undefined" if not counter["positive"] else counter["tp"]/counter["positive"]}
        for (p,f,pol),counter in sorted(contracts.items())
    ])
    write_csv(out / "entry-loadability.csv", availability_rows)
    write_json(out / "counterexamples.json", select(static, buckets, availability_rows))


def select(static, groups, availability):
    output = {"entry_loadability": availability, "deeper_only": [], "bundle_only": [], "document_only": []}
    for (package, before, after, fn), pred in static.items():
        if (package,before,after,fn) not in groups:
            continue
        group = groups[(package,before,after,fn)]
        proof = dict(package=package, previous=before, version=after, function=fn,
                     C=pred["C"], D=pred["D"], E=pred["E"], E2=pred["E2"],
                     reason_E2=pred["E2_reason"], scope="pre-frozen contract families", state=result(group),
                     cells=len(group), notice=pred["notice_state"], doc_url=pred["doc_url"], tarball=pred["archive_url"])
        if pred["E"] == "skip" and pred["E2"] == "alert":
            output["deeper_only"].append(proof)
        if pred["D"] == "alert" and all(pred[p] == "skip" for p in ("C","E","E2")):
            output["bundle_only"].append(proof)
        if pred["C"] == "alert" and pred["E"] == "skip":
            output["document_only"].append(proof)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    join(read_csv(ROOT / "predictions.csv"), read_csv(ROOT / "evidence/output-cells.csv"),
         json_in(ROOT / "evidence/output-read.json")["release_checks"], args.out)


if __name__ == "__main__":
    main()
