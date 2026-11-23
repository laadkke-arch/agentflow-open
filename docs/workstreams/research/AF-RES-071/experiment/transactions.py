"""Execute transaction faults and verify history by reopening in fresh processes."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import subprocess
import sys

from model import ROOT, baseline, canonical, design, load_json, run_local
from storage import InjectedFailure, OperationConflict, open_db, project, reopen_snapshot, save

OBJECT = "A3"


def editions():
    spec = next(row for row in load_json(ROOT / "inputs" / "objects.json") if row["id"] == OBJECT)
    base = baseline(spec)
    restored = next(pair for pair in design([spec]) if pair.change == "restore")
    return spec, {"base": base, "edit": restored.before, "restore": restored.after}


def worker(work, action, op, fault):
    db_file = work / "history.sqlite"
    if action == "lookup":
        print(canonical(reopen_snapshot(db_file, OBJECT)))
        return 0
    spec, choices = editions()
    edition = choices[action]
    run = run_local(spec, edition, edition.materialize(work / "origin"), "TX-" + edition.id)
    record, pieces = project("A2", spec, edition, run)
    with closing(open_db(db_file)) as db:
        try:
            result, _ = save(db, op, edition, run, record, pieces, fault)
        except InjectedFailure as error:
            print(canonical({"event": "exception", "message": str(error)}))
            return 72
        except OperationConflict as error:
            print(canonical({"event": "collision", "message": str(error)}))
            return 74
    print(canonical({"event": result, "op": op, "run": run["id"]}))
    return 0


def exercise(work):
    work.mkdir()
    trials = []
    def invoke(case, action, expected, op="none", fault="none"):
        command = [sys.executable, "-B", __file__, "worker", str(work), action, op, fault]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=10)
        record = {"id": case, "action": action, "op": op, "fault": fault,
                  "exit": completed.returncode, "expected_exit": expected, "stderr": completed.stderr,
                  "stdout": json.loads(completed.stdout) if completed.stdout else None,
                  "journal_exists_before_reopen": (work / "history.sqlite-journal").exists()}
        trials.append(record)
        assert completed.returncode == expected, record
        return record["stdout"]

    invoke("TX01", "base", 0, "initial")
    first = invoke("TX02", "lookup", 0)
    invoke("TX03", "edit", 72, "edit", "exception")
    after_exception = invoke("TX04", "lookup", 0)
    invoke("TX05", "edit", 73, "edit", "crash")
    after_crash = invoke("TX06", "lookup", 0)
    assert first == after_exception == after_crash, trials
    invoke("TX07", "edit", 0, "edit")
    changed = invoke("TX08", "lookup", 0)
    duplicate = invoke("TX09", "edit", 0, "edit")
    after_duplicate = invoke("TX10", "lookup", 0)
    assert duplicate["event"] == "duplicate" and changed == after_duplicate, trials
    invoke("TX11", "restore", 74, "edit")
    after_collision = invoke("TX12", "lookup", 0)
    assert changed == after_collision, trials
    invoke("TX13", "restore", 0, "restore")
    last = invoke("TX14", "lookup", 0)
    values = [row["snapshot"] for row in last["old_answers"]]
    assert len(values) == 3 and values[0] == values[2] and values[1] != values[0], last
    assert last["active"] == last["old_answers"][2]["run"], last
    assert last["old_answers"][:2] == changed["old_answers"], last
    for row in (first, after_exception, after_crash, changed, after_duplicate, after_collision, last):
        assert row["counts"]["operations"] == row["counts"]["answers"] == len(row["old_answers"])
        assert row["counts"]["current_answer"] == 1
        assert row["integrity"] == "ok" and row["orphan_fragments"] == 0 and not row["foreign_key_errors"]
    residual = sum(abs(first["counts"][table] - row["counts"][table])
                   for row in (after_exception, after_crash) for table in first["counts"])
    return {"trials": trials, "duplicate_rows": after_duplicate["counts"]["answers"] - changed["counts"]["answers"],
            "old_answers_modified": sum(a != b for a, b in zip(last["old_answers"][:2],
                                                             changed["old_answers"], strict=True)),
            "residual_rows_after_rollback": residual, "replayed_after_reopen": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["worker", "check"])
    parser.add_argument("work", type=Path)
    parser.add_argument("action", nargs="?", choices=["base", "edit", "restore", "lookup"])
    parser.add_argument("op", nargs="?", default="none")
    parser.add_argument("fault", nargs="?", default="none")
    options = parser.parse_args()
    if options.command == "worker":
        raise SystemExit(worker(options.work, options.action, options.op, options.fault))
    print(canonical(exercise(options.work)))
