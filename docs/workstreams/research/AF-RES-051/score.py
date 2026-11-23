"""Build evidence packets and score the frozen rules against separately checked truth."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

TASK = Path(__file__).resolve().parent
FACTS = {"A": "path_open", "K": "key_read", "R": "reported_effect", "I": "publisher_identity"}
TRI = {"yes": "확인", "no": "반증", None: "미확인"}
OUTCOMES = {"match": "일치", "fp": "거짓 양성", "fn": "거짓 음성", "hold": "보류", "no_truth": "정답 미확인"}


def jsonline(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def csv_write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_runs(path):
    return {row["run_id"]: row for row in (json.loads(line) for line in path.read_text().splitlines())}


def proposed_edit(target, baseline, domain, condition):
    prediction = baseline["paired_selected_expected"][f"{domain}{condition}"]
    return {"path": target["path"], "line": target["line"], "key": target["key"],
            "field": target["field"], "from": prediction["before"], "to": prediction["after"]}


def build_packets(run, chosen):
    purpose = (f"Sum selected confirmed case counts for Bronx+Brooklyn on {chosen['date']}"
               if run["domain"] == "S" else
               f"Count distinct trip IDs on route {chosen['route']} on {chosen['date']} in direction {chosen['direction']}")
    basic = {"address": run["publisher_url"], "purpose": purpose}
    pinned = basic | {"edition": run["edition"], "distribution_sha256": run["distribution_sha256"],
                      "publisher_file_sha256": run["publisher_file_sha256"],
                      "candidate_sha256": run["visible"][run["target"]["path"]]["sha256"]}
    receipt = run["receipt"]
    measured = pinned | {
        "run_id": run["run_id"], "coverage": run["coverage"],
        "visible_paths": sorted(run["visible"]), "opens": receipt["opens"],
        "key_reads": receipt["key_reads"], "transform": receipt["transform"], "output": receipt["output"]
    }
    return {"P0": basic, "P1": pinned, "P2": measured}


def field_at(entries, target):
    named = [entry["fields"][target["field"]] for entry in entries
             if entry["path"] == target["path"] and entry["line"] == target["line"]
             and target["field"] in entry["fields"]]
    if len(named) > 1:
        raise ValueError(f"Duplicate field record for {target}")
    return named[0] if named else None


def published_id(packet):
    fields = ("edition", "distribution_sha256", "publisher_file_sha256", "candidate_sha256")
    if all(packet.get(field) for field in fields):
        return "yes" if packet["publisher_file_sha256"] == packet["candidate_sha256"] else "no"
    return None


def report_effect(packet, edit, opened, looked_up):
    if opened == "no" or looked_up == "no":
        return "no"
    output, transform = packet["output"], packet["transform"]
    relevant = [entry for entry in output["contributors"]
                if entry["path"] == edit["path"] and entry["line"] == edit["line"]
                and edit["field"] in entry["fields"]]
    if transform["kind"] == "sum-round" and len(relevant) == 1:
        before = int(edit["from"])
        if relevant[0]["fields"][edit["field"]] != before:
            return None
        raw = output["raw"] - before + int(edit["to"])
        quantum = transform["increment"]
        after = (raw + quantum // 2) // quantum * quantum
    elif transform["kind"] == "active-direction-distinct" and edit["field"] == "direction_id" and len(relevant) == 1:
        ids = {entry["key"] for entry in output["contributors"] if entry != relevant[0]}
        if edit["to"] == transform["direction"]:
            ids.add(relevant[0]["key"])
        after = len(ids)
    elif transform["kind"] == "active-direction-distinct" and edit["field"] == "trip_id":
        rejected = [entry for entry in transform["rejected_direction"] if entry["line"] == edit["line"]]
        if len(rejected) != 1 or rejected[0]["trip_id"] != edit["from"]:
            return None
        # The substituted identifier cannot change the route/date/direction gate.
        after = output["report"]
    else:
        return None
    return "yes" if after != output["report"] else "no"


def decide(mode, packet, edit):
    answers = dict.fromkeys(FACTS)
    if mode in {"P1", "P2"}:
        answers["I"] = published_id(packet)
    if mode == "P2" and packet.get("coverage") == "complete-for-staged-regular-files-and-explicit-lookup":
        if edit["path"] in packet.get("visible_paths", []):
            if "opens" in packet:
                answers["A"] = "yes" if any(opened["path"] == edit["path"] for opened in packet["opens"]) else "no"
            if "key_reads" in packet:
                answers["K"] = "yes" if field_at(packet["key_reads"], edit) is not None else "no"
            if (answers["A"] is not None and answers["K"] is not None
                    and "output" in packet and "transform" in packet):
                answers["R"] = report_effect(packet, edit, answers["A"], answers["K"])
    return answers


def outcome(predicted, truth):
    if truth is None:
        return "no_truth"
    if predicted is None:
        return "hold"
    if predicted == truth:
        return "match"
    return "fp" if predicted == "yes" else "fn"


def yes(value):
    return "yes" if value else "no"


def independent_truth(main, selected, unselected, sealed, chosen):
    target = main["target"]
    actual = main["independent"]
    path = target["path"]
    expected_identity = main["visible"][path]["sha256"] == main["publisher_file_sha256"]
    sanctioned = not any(item["path"] == path and item["kind"] == "header-only modified control"
                         for item in main["preparation"])
    if expected_identity != sanctioned:
        raise AssertionError(f"Publisher hash and independently specified fixture differ: {main['run_id']}")
    baseline_path = "statistics.csv" if main["domain"] == "S" else "trips.txt"
    base_included = (target["field"] in actual.get("field_values", {})
                     and actual["field_values"][target["field"]] not in {"", "NA", ":"}
                     if main["domain"] == "S" else target["line"] in actual["lines"])
    findings = {
        "path_open": yes(path in main["os"]["by_path"]),
        "key_read": yes(actual["field_trap"]["exit_code"] == 19),
        "reported_effect": yes(selected["independent"]["report"] != actual["report"]),
        "publisher_identity": yes(sanctioned),
        "formula_member": yes(path == baseline_path and base_included),
        "same_content_used": yes(expected_identity and base_included),
    }
    for field in ("raw", "report"):
        for probe, label in [(selected, "selected"), (unselected, "unselected")]:
            relation = "same" if probe["independent"][field] == actual[field] else "changed"
            findings[f"{label}_{field}_relation"] = relation
    for field, value in findings.items():
        if sealed[field] != value:
            raise AssertionError((chosen["output_id"], sealed["truth_id"], field, sealed[field], value))
    return findings


def record_sensitivity(run, inputs, baseline):
    """Test the fixed rule's reliance on an independently justified coverage claim."""
    packet = build_packets(run, inputs["selection"]["T"])["P2"]
    edit = proposed_edit(run["target"], baseline, "T", run["condition"])
    target = edit["path"]
    missing = packet | {
        "opens": [entry for entry in packet["opens"] if entry["path"] != target],
        "key_reads": [entry for entry in packet["key_reads"] if entry["path"] != target],
    }
    variants = [
        ("unaltered", packet),
        ("lists removed explicitly", {key: value for key, value in packet.items()
                                      if key not in {"opens", "key_reads"}}),
        ("entries removed and coverage flagged", missing | {"coverage": "incomplete"}),
        ("entries removed but coverage incorrectly complete", missing),
    ]
    return {"run_id": run["run_id"], "target": edit, "status": "exploratory deletion outside the main score",
            "results": [{"variant": label, "decisions": {axis: TRI[value] for axis, value in decide("P2", variant, edit).items()}}
                        for label, variant in variants]}


def score(directory, output):
    inputs = json.loads((TASK / "evidence" / "inputs.json").read_text())
    baseline = json.loads((TASK / "evidence" / "baseline.json").read_text())
    runs = load_runs(directory / "runs.jsonl")
    with (TASK / "truth.csv").open(newline="") as stream:
        truths = list(csv.DictReader(stream))
    packets, decisions, pairs, checked = [], [], [], []
    for sealed in truths:
        run_id = sealed["run_id"]
        main = runs[run_id]
        chosen = inputs["selection"][main["domain"]]
        tag_selected, tag_unselected = [runs[f"{run_id}-{suffix}"] for suffix in ("SEL", "NON")]
        facts = independent_truth(main, tag_selected, tag_unselected, sealed, chosen)
        checked.append({"id": sealed["truth_id"], "run_id": run_id,
                        "baseline_id": baseline["primary"][main["domain"]]["id"],
                        "target": main["target"], "facts": facts,
                        "path_evidence": "runs.jsonl os.by_path (strace)",
                        "key_evidence": "runs.jsonl independent.field_trap",
                        "reported_effect_evidence": [run_id, tag_selected["run_id"]],
                        "identity_evidence": "inputs.json whole publisher pin and runs visible candidate digest",
                        "raw": main["independent"]["raw"], "report": main["independent"]["report"]})
        for variant in [tag_selected, tag_unselected]:
            changed_paths = [path for path, identity in main["visible"].items() if variant["visible"][path] != identity]
            edit = variant["preparation"][-1]
            if changed_paths != [edit["path"]]:
                raise AssertionError(f"Variant changes more than one file: {variant['run_id']}")
            pairs.append({"comparison_id": "PAIR-" + variant["run_id"], "parent_run_id": run_id, "variant_run_id": variant["run_id"],
                          "kind": edit["kind"], "path": edit["path"], "line": edit["line"], "field": edit["field"],
                          "old": edit["old"], "new": edit["new"], "parent_raw": main["independent"]["raw"],
                          "variant_raw": variant["independent"]["raw"], "parent_report": main["independent"]["report"],
                          "variant_report": variant["independent"]["report"], "matched_preregistered": "yes"})
        edit = proposed_edit(main["target"], baseline, main["domain"], main["condition"])
        previous_fields, previous_bytes = 0, 0
        for mode, packet in build_packets(main, chosen).items():
            encoded = jsonline(packet)
            byte_count = len(encoded.encode("utf-8"))
            packet_id = f"PK-{run_id}-{mode}"
            packets.append({"packet_id": packet_id, "run_id": run_id, "mode": mode, "field_count": len(packet),
                            "added_field_count": len(packet) - previous_fields, "bytes": byte_count,
                            "added_bytes": byte_count - previous_bytes, "fields_json": encoded})
            answers = decide(mode, packet, edit)
            shortcut = {"P0": "yes", "P1": answers["I"]}.get(mode)
            for axis, truth_name in FACTS.items():
                primary = answers[axis]
                alternative = primary if mode == "P2" else shortcut
                verified = facts[truth_name]
                decisions.append({"decision_id": f"D-{run_id}-{mode}-{axis}", "packet_id": packet_id,
                                  "truth_id": sealed["truth_id"], "run_id": run_id, "mode": mode, "fact": axis,
                                  "target_json": jsonline(edit), "primary_rule": f"{mode}-{axis} (SCOPE.md)",
                                  "primary_verdict": TRI[primary], "verified_truth": TRI[verified],
                                  "primary_outcome": OUTCOMES[outcome(primary, verified)],
                                  "shortcut_verdict": TRI[alternative],
                                  "shortcut_outcome": OUTCOMES[outcome(alternative, verified)],
                                  "measured_truth_denominator": int(verified is not None), "bytes": byte_count,
                                  "added_field_count": len(packet) - previous_fields, "added_bytes": byte_count - previous_bytes,
                                  "evidence": f"{sealed['truth_id']}; {packet_id}; {run_id} / {tag_selected['run_id']}"})
            previous_fields, previous_bytes = len(packet), byte_count
    if len(packets) != 48 or len(decisions) != 192 or len(pairs) != 32:
        raise AssertionError("Panel shape did not match the sealed design")
    output.mkdir(parents=True, exist_ok=True)
    csv_write(output / "packets.csv", packets)
    csv_write(output / "decisions.csv", decisions)
    csv_write(output / "pairs.csv", pairs)
    (output / "truth-verification.jsonl").write_text("".join(jsonline(row) + "\n" for row in checked), encoding="utf-8")
    (output / "receipt-sensitivity.json").write_text(
        json.dumps(record_sensitivity(runs["T1-1"], inputs, baseline), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    counts = {
        mode: {column: dict(Counter(row[column] for row in decisions if row["mode"] == mode))
               for column in ["primary_outcome", "shortcut_outcome"]}
        for mode in ["P0", "P1", "P2"]
    }
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    score(args.runs_dir, args.output)
