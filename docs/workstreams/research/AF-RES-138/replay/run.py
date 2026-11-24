"""Replay AF-RES-134 at the same budgets and fill at most one Gate vacancy."""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
POLICIES = ("B", "C", "Gate", "Conditional")
ALIAS_FIELDS = ("request_id", "alias_id", "feature_id", "first_policy", "phrase", "start", "end",
                "last_start", "token_start", "token_end", "last_token", "prefix", "suffix", "particle",
                "counts_in_replay")


def conditional_choice(gate_rows, review, request_id, display_cap):
    occupied = sum(row["display_rank"] is not None for row in gate_rows)
    considered = []
    if occupied == display_cap:
        return None, considered
    for row in gate_rows:
        feature = row["feature_id"]
        if row["investigation_rank"] is None or row["display_rank"] is not None:
            continue
        decision = review[request_id, feature]
        considered.append(feature)
        if decision["conditional_eligible"] == "yes":
            required = (decision["conditional_text"], decision["unresolved_conditions"], decision["request_spans"],
                        decision["card_clause_url"], decision["condition_true_action"], decision["condition_false_action"])
            if (not all(required) or decision["conditional_reject_reason"]
                    or decision["gate"] != "hold"
                    or decision["condition_true_action"] != "recommend"
                    or decision["condition_false_action"] != "hold"
                    or len(decision["unresolved_conditions"].split("|")) != 1):
                raise ValueError("conditional display requires one verified condition and two outcomes")
            return feature, considered
    return None, considered


def extend_gate(rid, gate_rows, gate_slots, review, inherited):
    cap = inherited.STAGES["display"]
    feature, examined = conditional_choice(gate_rows, review, rid, cap)
    vacancy = next((row["position"] for row in gate_slots if row["stage"] == "display" and row["vacancy"]), None)
    args = []
    for previous in gate_rows:
        fid = previous["feature_id"]
        row = dict(previous, policy="Conditional", investigation_change="same" if previous["investigation_rank"] else "outside",
                   previous_investigation_rank=previous["investigation_rank"], previous_display_rank=previous["display_rank"],
                   conditional_checked=fid in examined)
        if fid == feature:
            row.update(display_rank=vacancy, display_change="entered", reason="conditional_display")
        elif row["display_rank"] is not None:
            row.update(display_change="same")
        else:
            row.update(display_change="outside")
            if row["reason"] == "gate_hold" and fid in examined:
                row["reason"] = "conditional_hold"
        row["condition_text"] = review[rid, fid]["conditional_text"] if fid == feature else ""
        args.append(row)

    slot_rows = []
    for previous in gate_slots:
        row = dict(previous, policy="Conditional")
        if row["stage"] == "display" and row["position"] == vacancy and feature is not None:
            row.update(feature_id=feature, grade="", vacancy=False, reason="conditional_display")
        slot_rows.append(row)
    return args, slot_rows, examined


def moves(rows, truth, inherited):
    positions = {(r["request_id"], r["feature_id"], r["policy"]): r for r in rows}
    for before, after in zip(POLICIES[:-1], POLICIES[1:], strict=True):
        for row in rows:
            if row["policy"] != after:
                continue
            rid, fid = row["request_id"], row["feature_id"]
            earlier = positions[rid, fid, before]
            verdict = truth[rid, fid]
            for stage in inherited.STAGES:
                pos_field = stage + "_rank"
                old, new = earlier[pos_field], row[pos_field]
                yield {
                    "request_id": rid, "layer": row["layer"], "from": before, "to": after, "stage": stage,
                    "feature_id": fid, "grade": verdict["grade"],
                    "alternative_grade": verdict["alternative_grade"] or verdict["grade"],
                    "change": inherited.location_change(old, new), "old_position": old, "new_position": new,
                    "old_visibility": earlier["visibility"] if stage == "display" else "",
                    "new_visibility": row["visibility"] if stage == "display" else "",
                    "old_reason": earlier["reason"], "new_reason": row["reason"],
                    "confirmed_direct_before": bool(old and earlier["visibility"] != "conditional" and verdict["grade"] == "direct"),
                    "confirmed_direct_after": bool(new and row["visibility"] != "conditional" and verdict["grade"] == "direct"),
                    "conditional_if_true": "direct" if stage == "display" and row["visibility"] == "conditional" else "",
                    "conditional_if_false": "hold" if stage == "display" and row["visibility"] == "conditional" else "",
                }


def slot_visibility(row):
    if row["vacancy"]:
        return "vacant"
    if row["stage"] == "investigation":
        return "candidate"
    return "conditional" if row["reason"] == "conditional_display" else "unconditional"


def annotate(ranks, slots):
    counts = Counter((r["request_id"], r["policy"], r["stage"]) for r in slots if r["vacancy"])
    for row in ranks:
        row.setdefault("conditional_checked", False)
        row.setdefault("condition_text", "")
        row["visibility"] = ("conditional" if row["reason"] == "conditional_display" else "unconditional"
                             if row["display_rank"] is not None else "absent")
        row["investigation_vacancies"] = counts[row["request_id"], row["policy"], "investigation"]
        row["display_vacancies"] = counts[row["request_id"], row["policy"], "display"]
        if row["visibility"] == "conditional":
            row["condition_true_grade"] = "direct"
            row["condition_false_grade"] = "hold"
        else:
            row["condition_true_grade"] = ""
            row["condition_false_grade"] = ""
    for row in slots:
        row["visibility"] = slot_visibility(row)


def run(root, af122, af126, af134, out):
    if any(out.iterdir()):
        raise ValueError("replay output directory must be empty")
    sys.path.insert(0, str(af134.resolve()))
    import project as projection
    inherited = projection.read_module("af134_run", af134 / "run.py")

    prepare, legacy, capture = projection.load_predecessors(af122, af126)
    sys.modules["capture"] = capture
    scorer = projection.read_module("af126_replay", af126 / "replay.py")
    cards, aliases, _, _ = legacy.read_inputs(af122)
    glossary = capture.aliases_by_phrase(prepare, af122 / "aliases.csv")
    if len(cards) != 16 or len(glossary) != 12:
        raise ValueError("the fixed card pool and active alias count must be preserved")
    source_sha = legacy.file_sha(af122 / "aliases.csv")
    assertions = scorer.boundary_checks(prepare, legacy, glossary, cards, aliases, source_sha)
    requests = projection.read_jsonl(root / "requests.jsonl")
    replay_inputs = projection.read_jsonl(root / "replay/inputs.jsonl")
    ids = {r["request_id"] for r in requests}
    views = {view["request_id"]: view for view in replay_inputs}
    frame = prepare.read_csv(root / "frame.csv")
    selected = {row["selected_request_id"] for row in frame if row["selection"] == "selected"}
    if ids != set(views) or ids != selected or len(ids) != len(requests) or len(ids) != len(replay_inputs):
        raise ValueError("selection, requests and replay projections disagree")

    display = inherited.coverage(prepare.read_csv(root / "display.csv"), ids, cards, "display")
    truth = inherited.coverage(prepare.read_csv(root / "truth.csv"), ids, cards, "truth")
    ranks, slots, inspections, audit = [], [], [], []
    for request in requests:
        rid = request["request_id"]
        view = views[rid]
        inherited.check_projection(view, request, prepare, legacy)
        checks = {span["span_id"] for span in request["spans"]}
        for fid in cards:
            row = display[rid, fid]
            if not set(row["request_spans"].split("|")) <= checks or row["gate"] not in ("hold", "pass"):
                raise ValueError("display decision has an unknown span or Gate state")
            if row["conditional_eligible"] not in ("yes", "no") or truth[rid, fid]["grade"] not in inherited.GRADES:
                raise ValueError("invalid sealed decision")

        base, base_slots, _, base_cost, hits = inherited.make_ranks(
            request, view, scorer, legacy, cards, aliases, glossary, source_sha, display, truth
        )
        gate_rows = [row for row in base if row["policy"] == "Gate"]
        gate_slots = [row for row in base_slots if row["policy"] == "Gate"]
        fourth, fourth_slots, examined = extend_gate(rid, gate_rows, gate_slots, display, inherited)
        gate_examined = [row["feature_id"] for row in gate_rows if row["gate_scanned"]]
        condition_exam = list(dict.fromkeys(gate_examined + examined))
        fourth_cost = inherited.costs(rid, "Conditional", condition_exam, display)
        extra = fourth_cost["extra_clauses"] - base_cost[-1]["extra_clauses"]
        for row in base_cost:
            row.update(conditional_checks=0, additional_over_gate_clauses="")
        fourth_cost.update(conditional_checks=len(examined), additional_over_gate_clauses=extra)
        ranks.extend(base + fourth)
        slots.extend(base_slots + fourth_slots)
        inspections.extend(base_cost + [fourth_cost])
        audit.extend(hits)

    annotate(ranks, slots)
    transitions = list(moves(ranks, truth, inherited))
    outputs = {"ranks.csv": ranks, "slots.csv": slots, "transitions.csv": transitions,
               "editor-cost.csv": inspections, "alias-audit.csv": audit}
    for name, rows in outputs.items():
        fields = ALIAS_FIELDS if name == "alias-audit.csv" else None
        inherited.save_csv(out / name, rows, fields)
    own = ("requests.jsonl", "replay/inputs.jsonl", "frame.csv", "display.csv", "truth.csv", "replay/run.py")
    return {"boundary_assertions": assertions, "budget": inherited.STAGES, "requests": len(ids), "policies": POLICIES,
            "inputs": {name: legacy.file_sha(root / name) for name in own},
            "predecessors": {
                tag: {name: legacy.file_sha(folder / name) for name in names}
                for tag, folder, names in (("af122", af122, inherited.PINS["af122"]), ("af126", af126, inherited.PINS["af126"]),
                                            ("af134", af134, ("project.py", "run.py")))
            },
            "output_sha256": {name: legacy.file_sha(out / name) for name in outputs},
            "output_rows": {name: len(rows) for name, rows in outputs.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT)
    for pin in ("af122", "af126", "af134"):
        parser.add_argument("--" + pin, type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    print(json.dumps(run(args.data, args.af122, args.af126, args.af134, args.out), sort_keys=True))


if __name__ == "__main__":
    main()
