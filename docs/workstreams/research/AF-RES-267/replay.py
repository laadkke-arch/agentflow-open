"""Run the preserved AF-RES-249 grader and a separate reference on synthetic inputs."""
import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

import reference

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "receipts" / "original"
UPSTREAM = ("https://github.com/laadkke-arch/agentflow-open/blob/"
            "a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/")
ORIGINAL_SHA = {
    "verify_vectors.py": "e0f1afe777b4e224f704946f223f52c83f96bcf466e0724d8d7f6f92f47f9f2f",
    "trace-artifacts.jsonl": "f4a4edd32db787349e8d2339515432169a29b04fb02f2607a986d9d062deef8b",
    "worked-traces.csv": "7cbb4177b980150a88290db2b8d1ecedc3b27d90484c2bd4fe18cf5cc82b3e5a",
    "worked-events.jsonl": "ffdc96b383c6553182087516e2b6c6eb25f2fbc59e024bc7d9d4d335e17c5929",
    "stimuli.md": "93fca257b05c68aa2f1925776501dae200f03a82a80cebe4b3f648da6fc46458",
}
TASKS = {"K": "A", "N": "B", "R": "A", "F": "B"}
PHASES = ("t0", "t12minus", "t24")
FUNCTION = {"A": "runs", "B": "insertion_index"}
CONTROLS = {
    "left_ties": ("B", "N-t12minus"),
    "global_groups": ("A", "R-t0"),
    "bool_indices": ("B", "N-t0"),
    "restore_input": ("B", "N-t0"),
    "raise_on_tie_vector": ("B", "N-t0"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def json_file(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def csv_file(path, rows):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def json_lines(path):
    return [json.loads(line) for line in path.read_bytes().splitlines()]


def source_inputs():
    for name, expected in ORIGINAL_SHA.items():
        require(sha((SOURCE / name).read_bytes()) == expected, f"changed original: {name}")
    with (SOURCE / "worked-traces.csv").open(encoding="utf-8", newline="") as file:
        cases = {row["case_id"]: (line, row) for line, row in enumerate(csv.DictReader(file), 2)}
    checkpoints = {}
    for line, event in enumerate(json_lines(SOURCE / "worked-events.jsonl"), 1):
        if event["event_type"] not in {"seal", "freeze"}:
            continue
        phase = "t0" if event["phase"] == "baseline" else event["phase"]
        key = (event["case_id"], phase)
        require(key not in checkpoints, f"duplicate checkpoint: {key}")
        checkpoints[key] = line, event

    expected_order = [(case, phase) for case in TASKS for phase in PHASES]
    raw_snapshots = json_lines(SOURCE / "trace-artifacts.jsonl")
    require([(r["case_id"], r["phase"]) for r in raw_snapshots] == expected_order,
            "unexpected snapshot order or membership")
    require(set(checkpoints) == set(expected_order) and set(cases) == set(TASKS),
            "case or checkpoint coverage mismatch")
    parent = {}
    groups = {}
    snapshots = []
    for line, row in enumerate(raw_snapshots, 1):
        case, phase = row["case_id"], row["phase"]
        case_line, trace = cases[case]
        event_line, event = checkpoints[case, phase]
        task = TASKS[case]
        data = row["source_utf8"].encode("utf-8")
        digest = sha(data)
        slot = case + "-" + phase
        functions = {n.name for n in ast.parse(data).body if isinstance(n, ast.FunctionDef)}
        require(functions == {FUNCTION[task]}, f"{slot}: wrong task function")
        require(row["synthetic"] is True and trace["synthetic"] == "true"
                and event["synthetic"] is True and event["not_observation"] is True,
                f"{slot}: expected explicitly synthetic sources")
        require(task == trace["task"] == event["task_id"]
                and trace["condition"] == event["condition"], f"{slot}: task or condition mismatch")
        for key in ("participant_id", "assignment_id", "session_id", "artifact_id"):
            require(row[key] == trace[key] == event[key], f"{slot}: {key} mismatch")
        require(row["actor_id"] == trace["participant_id"] == event["actor_id"]
                and event["actor_role"] == "author", f"{slot}: actor mismatch")
        require(digest == row["sha256"] == trace[phase + "_hash"] == event["artifact_hash"],
                f"{slot}: bytes or linked hash mismatch")
        require(row["parent_hash"] == parent.get(case) == event.get("parent_hash"),
                f"{slot}: parent mismatch")
        parent[case] = digest
        group = groups.setdefault(digest, f"G{len(groups) + 1}")
        snapshots.append(({
            "slot": slot, "case_id": case, "phase": phase, "task": task,
            "condition": trace["condition"], "actor_id": row["actor_id"],
            "participant_id": row["participant_id"], "assignment_id": row["assignment_id"],
            "session_id": row["session_id"], "artifact_id": row["artifact_id"],
            "declared_sha256": row["sha256"], "actual_sha256": digest,
            "worked_trace_sha256": trace[phase + "_hash"], "checkpoint_sha256": event["artifact_hash"],
            "parent_hash": row["parent_hash"] or "null", "parent_scope": "root" if phase == "t0" else "previous_case_phase",
            "code_group": group, "code_bytes_utf8": len(data), "function": FUNCTION[task],
            "fixture_jsonl_line": line, "case_csv_line": case_line,
            "checkpoint_event_id": event["event_id"], "checkpoint_jsonl_line": event_line,
            "source_url": UPSTREAM + f"trace-artifacts.jsonl#L{line}",
            "case_url": UPSTREAM + f"worked-traces.csv#L{case_line}",
            "checkpoint_url": UPSTREAM + f"worked-events.jsonl#L{event_line}",
        }, data))
    return snapshots


def run_process(argv, work):
    started_at = now()
    started = time.monotonic()
    env = {"LC_ALL": "C.UTF-8", "TZ": "UTC"}
    try:
        process = subprocess.run(argv, cwd=work, env=env, capture_output=True, timeout=10)
    except subprocess.TimeoutExpired as exc:
        status, code = "timeout", None
        stdout, stderr, failure = exc.stdout or b"", exc.stderr or b"", str(exc)
    except OSError as exc:
        status, code = "not_started", None
        stdout, stderr, failure = b"", b"", str(exc)
    else:
        status, code = "exited", process.returncode
        stdout, stderr, failure = process.stdout, process.stderr, None
    return stdout, stderr, {
        "command": argv, "cwd": str(work), "child_environment": env, "timeout_seconds": 10,
        "started_utc": started_at, "ended_utc": now(),
        "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
        "process_status": status, "exit_code": code, "failure": failure,
    }


def process_rows(root, work, slot, engine, exe, binary_sha, task, data, source,
                 source_url, observe_lines=False):
    folder = work / slot / engine
    folder.mkdir(parents=True)
    initial = list(folder.iterdir())
    require(not initial, f"nonempty process directory: {folder}")
    script = folder / source.name
    fixture = folder / "submission.py"
    script.write_bytes(source.read_bytes())
    fixture.write_bytes(data)
    argv = [str(exe), "-I", "-B", "-X", "utf8", script.name, task, fixture.name]
    if observe_lines:
        argv.append("--observe-lines")
    stdout, stderr, meta = run_process(argv, folder)
    receipt = root / "runs" / slot / engine
    receipt.mkdir(parents=True)
    (receipt / "stdout.jsonl").write_bytes(stdout)
    (receipt / "stderr.txt").write_bytes(stderr)
    rows = {}
    errors = []
    for line, raw in enumerate(stdout.splitlines(), 1):
        try:
            row = json.loads(raw)
            vector = row["id"]
            if vector in rows:
                raise ValueError(f"duplicate vector {vector}")
            rows[vector] = (line, row)
        except (ValueError, TypeError, KeyError) as exc:
            errors.append({"line": line, "error": str(exc)})
    meta.update({
        "slot": slot, "engine": engine, "task": task, "initial_cwd_entries": [],
        "fixture_source": source_url, "fixture_sha256": sha(data),
        "fixture_after_sha256": sha(fixture.read_bytes()) if fixture.is_file() else None,
        "script_sha256": sha(script.read_bytes()), "python_executable_sha256": binary_sha,
        "stdout_sha256": sha(stdout), "stderr_sha256": sha(stderr),
        "stdout_bytes": len(stdout), "stderr_bytes": len(stderr), "vector_ids": list(rows),
        "parse_errors": errors,
    })
    relative = (receipt / "stdout.jsonl").relative_to(root).as_posix()
    json_file(receipt / "receipt.json", meta)
    return rows, meta, relative


def state(row, process_status):
    if row is None:
        return "not_started" if process_status == "not_started" else "no_vector_row"
    if "exception" in row:
        return "vector_exception"
    if row.get("type_ok") is False:
        return "type_error"
    if row.get("unchanged") is False:
        return "input_changed_at_return"
    if row.get("pass") is False:
        return "wrong_value"
    return "pass" if row.get("pass") is True else "invalid_row"


def compare_vector(grader, ref):
    if grader is None or ref is None:
        return False
    if any(grader[k] != ref[k] for k in ("input", "x", "expected")):
        return False
    if "exception" in grader:
        return (grader["pass"] is False and "exception" in ref
                and grader["exception"].splitlines()[-1] == ref["exception"]
                and not any(k in grader for k in ("got", "type_ok", "unchanged")))
    return ("exception" not in ref
            and all(grader[k] == ref[k] for k in ("got", "type_ok", "unchanged"))
            and grader["pass"] == ref["endpoint_pass"])


def evaluate_slot(root, work, slot, exe, binary_sha, task, data, source_url):
    graded, gmeta, gpath = process_rows(root, work, slot, "grader", exe, binary_sha,
                                        task, data, SOURCE / "verify_vectors.py", source_url)
    checked, rmeta, rpath = process_rows(root, work, slot, "reference", exe, binary_sha,
                                         task, data, ROOT / "reference.py", source_url,
                                         observe_lines=slot == "restore_input")
    expected_ids = [v[0] for v in reference.vectors(task)]
    entries = []
    for vector in expected_ids:
        gline, grader = graded.get(vector, (None, None))
        rline, ref = checked.get(vector, (None, None))
        g, r = grader or {}, ref or {}
        changes = r.get("line_observations")
        endpoint_agreement = compare_vector(grader, ref)
        entries.append({
            "vector_id": vector, "input_repr": g.get("input", r.get("input")),
            "x": g.get("x", r.get("x")), "expected_repr": g.get("expected"),
            "manual_repr": r.get("manual_expected"), "expected_type": r.get("expected_type"),
            "got_repr": g.get("got"), "reference_observed_type": r.get("got_type"),
            "reference_value_equal": r.get("value_equal"), "type_ok": g.get("type_ok"),
            "unchanged_at_return": g.get("unchanged"), "grader_pass": g.get("pass"),
            "grader_state": state(grader, gmeta["process_status"]), "grader_exit": gmeta["exit_code"],
            "grader_exception": g.get("exception"), "reference_exit": rmeta["exit_code"],
            "reference_endpoint_pass": r.get("endpoint_pass"),
            "reference_unchanged_at_return": r.get("unchanged"),
            "endpoint_agreement": endpoint_agreement,
            "reference_mid_changes": len(changes) if changes is not None else None,
            "strict_pass_if_observed": False if changes else None,
            "grader_stdout": f"{gpath}#L{gline}" if gline else None,
            "reference_stdout": f"{rpath}#L{rline}" if rline else None,
        })
    complete = (list(graded) == expected_ids == list(checked)
                and not gmeta["parse_errors"] and not rmeta["parse_errors"]
                and gmeta["process_status"] == rmeta["process_status"] == "exited"
                and gmeta["exit_code"] == int(any(g["grader_pass"] is False for g in entries))
                and rmeta["exit_code"] == 0
                and gmeta["fixture_after_sha256"] == rmeta["fixture_after_sha256"] == sha(data)
                and gmeta["script_sha256"] == ORIGINAL_SHA["verify_vectors.py"])
    return entries, complete


def runtime(exe, binary_sha):
    import _bisect
    import bisect
    import copy
    import itertools
    version = {}
    for option in ("--version", "-VV"):
        command = [str(exe), option]
        result = subprocess.run(command, capture_output=True, check=True, timeout=10)
        version[option] = {"command": command, "exit_code": result.returncode,
                           "stdout": result.stdout.decode("utf-8"),
                           "stderr": result.stderr.decode("utf-8")}
    return {
        "platform": platform.platform(), "machine": platform.machine(),
        "sys_version": sys.version, "sys_version_info": list(sys.version_info),
        "sys_implementation": sys.implementation.name, "sys_git": list(sys._git),
        "executable": str(exe), "executable_sha256": binary_sha,
        "version_probes": version,
        "bisect_right_uses_c": bisect.bisect_right is _bisect.bisect_right,
        "groupby_module": itertools.groupby.__module__,
        "module_sha256": {m.__name__: sha(Path(m.__file__).read_bytes())
                          for m in (_bisect, bisect, copy)},
        "original_sha256": ORIGINAL_SHA,
    }


def compare_runs(current, earlier):
    checks = []
    for slot in (f"{case}-{phase}" for case in TASKS for phase in PHASES):
        for engine in ("grader", "reference"):
            relative = Path("runs") / slot / engine
            a, b = current / relative, earlier / relative
            names = ("stdout.jsonl", "stderr.txt")
            matching = {name: a.joinpath(name).read_bytes() == b.joinpath(name).read_bytes()
                        for name in names}
            a_meta = json.loads(a.joinpath("receipt.json").read_bytes())
            b_meta = json.loads(b.joinpath("receipt.json").read_bytes())
            keys = ("exit_code", "fixture_sha256", "script_sha256", "process_status")
            matching.update({k: a_meta[k] == b_meta[k] for k in keys})
            checks.append({"slot": slot, "engine": engine, "matching": matching})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("snapshots", "controls"))
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--expected-python-sha256")
    parser.add_argument("--compare-to", type=Path)
    args = parser.parse_args()
    require(sys.implementation.name == "cpython" and tuple(sys.version_info) == (3, 12, 0, "final", 0),
            f"exact CPython 3.12.0 final required, got {sys.version}")
    require(args.mode == "snapshots" or args.compare_to is None, "comparison expects snapshots")
    exe = Path(sys.executable).resolve()
    binary_sha = sha(exe.read_bytes())
    require(not args.expected_python_sha256 or binary_sha == args.expected_python_sha256,
            "executable fingerprint differs from requested SHA256")
    out, work = args.out.resolve(), args.work.resolve()
    require(out != work and out not in work.parents and work not in out.parents,
            "output and process directories must be separate")
    for directory in (out, work):
        directory.mkdir(parents=True, exist_ok=True)
        require(not any(directory.iterdir()), f"directory must start empty: {directory}")
    snapshots = source_inputs()
    run_plan = []
    if args.mode == "snapshots":
        for row, data in snapshots:
            run_plan.append((row["slot"], row["task"], data, row["source_url"], row))
        csv_file(out / "snapshots.csv", [row for row, _ in snapshots])
    else:
        for slot, (task, baseline) in CONTROLS.items():
            path = ROOT / "controls" / (slot + ".py")
            run_plan.append((slot, task, path.read_bytes(), path.relative_to(ROOT).as_posix(),
                             {"matched_baseline_slot": baseline}))

    json_file(out / "environment.json", runtime(exe, binary_sha))
    rows = []
    incomplete = []
    for slot, task, data, url, provenance in run_plan:
        values, complete = evaluate_slot(out, work, slot, exe, binary_sha, task, data, url)
        if not complete:
            incomplete.append(slot)
        prefix = {"slot": slot, "task": task, "source_sha256": sha(data),
                  **{k: provenance[k] for k in
                     ("case_id", "phase", "actor_id", "matched_baseline_slot") if k in provenance}}
        rows.extend(prefix | row for row in values)
    csv_file(out / "vectors.csv", rows)
    checks = compare_runs(out, args.compare_to.resolve()) if args.compare_to else []
    if checks:
        json_file(out / "replay-comparison.json", checks)
    summary = {
        "mode": args.mode, "finished_utc": now(), "work": str(work),
        "argv": sys.argv, "python_executable_sha256": binary_sha,
        "grader_process_receipts": len(run_plan), "reference_process_receipts": len(run_plan),
        "vector_slots": len(rows), "grader_pass": sum(r["grader_pass"] is True for r in rows),
        "grader_fail": sum(r["grader_pass"] is False for r in rows),
        "endpoint_disagreements": sum(not r["endpoint_agreement"] for r in rows),
        "observed_mid_change_vectors": sum(bool(r["reference_mid_changes"]) for r in rows),
        "incomplete": incomplete, "comparison_pairs": len(checks),
        "comparison_mismatches": [c for c in checks if not all(c["matching"].values())],
    }
    json_file(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 2 if incomplete or summary["comparison_mismatches"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
