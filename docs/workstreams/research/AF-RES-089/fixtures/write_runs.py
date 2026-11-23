#!/usr/bin/env python3
"""Build the twelve-row run ledger from the raw observations and fixed allocation."""
import argparse
import csv
import json
from pathlib import Path

from visibility import objects


def load(path):
    return json.loads(path.read_text())


def trace(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def ledger_row(packet, case):
    relative = Path("evidence/gui") / case["run_id"]
    evidence = packet / relative
    result = load(evidence / "result.json")
    events = {event["seq"]: event for event in trace(evidence / "app.jsonl")}
    transitions = {}
    for kind, first, last in (("changed", "before", "after"), ("restored", "after", "undo")):
        if result[kind] is None:
            transitions[kind] = None
            continue
        before = objects(events[result["trace_seq"][first]])
        after = objects(events[result["trace_seq"][last]])
        transitions[kind] = {key: {"visible": delta, "id_before": before[key]["id"], "id_after": after[key]["id"]}
                             for key, delta in result[kind].items()}

    return {
        "run_id": case["run_id"], "case": case["case"], "build": case["build"], "repeat": int(case["repeat"]),
        "start_utc": result["started_utc"], "end_utc": result["end_utc"],
        "runner_argv": result["runner_argv"], "app_argv": result["processes"][0]["argv"],
        "binary_sha256": result["binary_sha256"], "case_fixture": case["fixture"], "input_sha256": result["input_sha256"],
        "display": result["processes"][0]["display"],
        "runner_exit": result["run_exit"], "app_exit": result["processes"][0]["exit_code"],
        "menu": result["menu"], "v_dispatch": result["v_dispatch"], "visited": result["visited"],
        "focus": result["focus"], "selection": result["selection"],
        "undo": result["undo"], "undo_index": result["undo_index"], "trace_seq": result["trace_seq"],
        "document_edited": result["document_edited"], "restore_document": result.get("restore_document"),
        **transitions,
        "app_log": str(relative / "app.jsonl"), "ui_steps": str(relative / "steps.jsonl"),
        "stderr": str(relative / "app.stderr"), "result": str(relative / "result.json"),
        "saved": {name: {**row, "path": str(relative / f"{name}.mscx")} for name, row in result["saved"].items()},
        "reopen": {
            label: {
                "argv": value["processes"][0]["argv"], "exit": value["processes"][0]["exit_code"],
                "runner_exit": value["run_exit"], "fresh_undo_index": value["undo_index_fresh"],
                "document_matches": value["document_matches"], "snapshot_seq": value["snapshot_seq"],
                "log": str(relative / value["path"] / "app.jsonl"),
                "ui_steps": str(relative / value["path"] / "steps.jsonl"),
            }
            for label, value in result["reopens"].items()
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parents[1]
    with (packet / "cases.csv").open(newline="") as file, args.out.open("w", encoding="utf-8") as out:
        for case in csv.DictReader(file):
            out.write(json.dumps(ledger_row(packet, case), ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
