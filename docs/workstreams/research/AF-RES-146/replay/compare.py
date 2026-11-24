"""Verify independent replay directories and join the sealed gate with the separate truth judgment."""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

from inputs import ROOT, digest, read_csv, read_jsonl
from run import COST_FIELDS, put_csv, put_json

GRADE = ("direct", "partial", "conflict", "unconfirmed")
METRICS = (
    "compared","actual_file_opens","source_text_opens","reading_note_opens","bytes_read","source_text_bytes",
    "reading_note_bytes","cache_hits","process_cpu_ns","wall_ns","direct","partial","conflict_reviewed",
    "unconfirmed_reviewed","conflict_displayed","vacancies",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    a,b = args.first,args.second
    output = args.output
    output.mkdir(parents=True,exist_ok=True)
    ma,mb = (json.loads((folder/"run-receipt.json").read_text()) for folder in (a,b))
    assert ma["input_fingerprints"] == mb["input_fingerprints"]
    assert ma["input_sha256"] == mb["input_sha256"]
    reference = ROOT/"evidence/prototype.json"
    for name, sha in ma["result_sha256"].items():
        assert sha == mb["result_sha256"][name] == digest((a/name).read_bytes()) == digest((b/name).read_bytes())
    assert reference.read_bytes() == (a/"prototype.json").read_bytes()
    assert ma["legacy_alternative"] == mb["legacy_alternative"]

    truth_raw = (ROOT/"truth.csv").read_bytes()
    independent = json.loads((ROOT/"evidence/independent.json").read_text())
    assert digest(truth_raw) == independent["truth_sha256"]
    truth = read_csv(truth_raw)
    truth_pair = {(r["event_id"],r["card_id"]):r for r in truth}
    cards = read_jsonl((ROOT/"inventory.jsonl").read_bytes())
    requests = read_jsonl((ROOT/"requests.jsonl").read_bytes())
    assert len(truth) == len(truth_pair) == 48
    assert set(truth_pair) == {(e["event_id"],c["card_id"]) for e in requests for c in cards}
    assert {r["grade"] for r in truth} <= set(GRADE)
    gate = [r for r in read_csv((ROOT/"replay/gate-new.csv").read_bytes()) if r["experiment"]=="primary"]
    assert len(gate) == 25
    against = Counter((g["grade"],truth_pair[g["event_id"],g["card_id"]]["grade"]) for g in gate)
    diff = []
    for g in gate:
        t = truth_pair[g["event_id"],g["card_id"]]
        if t["grade"] != g["grade"]:
            diff.append(dict(event_id=g["event_id"],card_id=g["card_id"],sealed_gate=g["grade"],independent=t["grade"],
                             gate_reason=g["reason"],independent_reason=t["reason"],independent_condition=t["condition"],
                             independent_alternative=t["alternative_grade"],source_url=g["source_url"]))

    result = read_csv((a/"stages.csv").read_bytes())
    displays_against_truth = {}
    for policy in ("cap3","cap8","sequential8","zero_fill8"):
        drawn = [r for r in result if (r["cohort"],r["policy"],r["stage"],r["state"]) ==
                 ("new",policy,"display_slot","displayed")]
        grades = Counter(truth_pair[r["event_id"],r["card_id"]]["grade"] for r in drawn)
        displays_against_truth[policy] = dict(n_shown=len(drawn),**{grade:grades[grade] for grade in GRADE})
    census = defaultdict(Counter)
    for row in truth:
        census[row["event_id"]][row["grade"]] += 1

    cost_raw = [r for d in (a,b) for r in read_csv((d/"costs.csv").read_bytes())]
    totals = defaultdict(Counter)
    stops = defaultdict(Counter)
    for row in cost_raw:
        if row["pass_kind"] not in {"cache_empty_at_policy_start","same_order_repeat"}:
            continue
        key = "|".join(row[f] for f in ("run","cohort","policy_group","policy","pass_kind"))
        totals[key].update({f:int(row[f]) for f in METRICS})
        stops[key][row["stop_reason"]] += 1
    only_counts = set(METRICS) - {"process_cpu_ns","wall_ns"}
    for key, measures in totals.items():
        folder,tail = key.split("|",1)
        if folder == a.name:
            replay = totals[b.name+"|"+tail]
            assert all(measures[f]==replay[f] for f in only_counts)
    standalone = dict(run="independent_reader",cohort="new",policy_group="census",event_id="all",policy="4x12",
                      pass_kind="reader_wall",stop_reason="48_pairs_sealed",compared=48,
                      wall_ns=round(independent["costs"]["elapsed_wall_seconds"]*1e9),
                      basis="Independent elapsed session only; 4 first bodies, 6 unique manual ranges and 4 distinct institutional works; source bytes in evidence/independent.json")
    put_csv(output/"costs.csv",COST_FIELDS,[*cost_raw,standalone])
    put_json(output/"analysis-join.json",{
        "counts":{grade:sum(c[grade] for c in census.values()) for grade in GRADE},
        "per_request":{e:{grade:c[grade] for grade in GRADE} for e,c in census.items()},
        "sealed_review_cells":len(gate),"cohort_pair_count":48,
        "agreement":len(gate)-len(diff),"disagreements":diff,
        "cross_tab":[{"sealed_gate":g,"independent":j,"n":n} for (g,j),n in sorted(against.items())],
        "display_join":displays_against_truth,
        "meaning":"The independent table was not available to the display operator before sealing and supplies no runtime decision."
    })
    put_json(output/"receipts.json",{
        "original_prototype_commit":"fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c",
        "original_observation_file":"evidence/prototype.json",
        "original_observation_sha256":digest(reference.read_bytes()),
        "replays":[{"folder":a.name,**ma},{"folder":b.name,**mb}],
        "source_capture":{
            path.name:json.loads((path/"source-capture.json").read_text())
            for path in (a,b)
        },
        "deterministic_diff":{"inputs":[],"stages":[],"transition":[],"prototype":[],"measured_counts":[]},
        "timing_diff":"Retained as independently observed numbers, excluded from equality. See costs.csv.",
        "cost_totals":totals,"stop_reasons":stops,"independent_receipt":"evidence/independent.json",
        "legacy_request_verification":"evidence/legacy-request-checks.json",
    })
    print(json.dumps({"direct":sum(c["direct"] for c in census.values()), "new_grade_agree":len(gate)-len(diff),
                      "new_grade_disagree":len(diff),"display_truth_join":displays_against_truth},ensure_ascii=False))


if __name__=="__main__":
    main()
