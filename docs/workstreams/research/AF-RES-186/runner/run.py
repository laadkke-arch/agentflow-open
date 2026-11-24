#!/usr/bin/env python3
"""Run and grade the 40 fixed cells. Each cell starts one child process."""

import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess
import time
from uuid import uuid4

from prepare import INPUTS, hash_file, written_json
from scoring import equal_observation, grade


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def compact_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def file_meta(path):
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": hash_file(path)}


def verify_installation(role, state):
    if not state["ready"]:
        return state["reason"]
    base = state["checkout"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=base, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=base)
    if head != state["commit"] or dirty:
        return f"{role} checkout changed after preparation"
    if role == "gold" and hash_file(Path(state["argv"][0])) != state["binary_sha256"]:
        return "Gold binary changed after preparation"
    if role == "js":
        if hash_file(Path(state["argv"][0])) != state["runtime_sha256"]:
            return "Node executable changed after preparation"
        if hash_file(Path(state["argv"][1])) != state["adapter_sha256"]:
            return "JS adapter changed after preparation"
    return ""


def request_for(case, suite_path, nonce):
    expected = case["expected"]
    request = {
        "nonce": nonce,
        "algorithm": case["algorithm"],
        "suite_root": suite_path,
        "base": case["options"]["base"],
        "processing_mode": case["options"]["processingMode"],
        "input": case["input"],
        "context": case["context"],
        "reexpand": case["algorithm"] == "compact" and expected["kind"] == "json",
    }
    if expected["kind"] == "json":
        evidence = expected["file"]
        path = Path(suite_path) / evidence["path"]
        if hash_file(path) != evidence["sha256"]:
            raise ValueError(f"Expected JSON SHA-256 changed: {path}")
        request["expected"] = json.loads(path.read_bytes())
        if request["expected"] != expected["value"]:
            raise ValueError(f"Expected JSON disagrees with input contract: {path}")
    return request


def clean_fixture_reads(case, loads):
    expected_reads = [(case["input"], "processor_loader")]
    if case["context"]:
        expected_reads.insert(0, (case["context"], "local_context_argument"))
    return loads == [{
        "document_iri": fixture["document_iri"], "path": fixture["path"],
        "sha256": fixture["sha256"], "mechanism": mechanism, "status": "read",
    } for fixture, mechanism in expected_reads]


def decode_case(observation, case, request, process_id, runtime):
    if (observation["protocol"], observation["nonce"], observation["pid"], observation["runtime"]) != (
        1, request["nonce"], process_id, runtime
    ):
        raise ValueError("Adapter protocol, nonce, process ID, or runtime mismatch")
    if not clean_fixture_reads(case, observation["loads"]):
        return "incomparable", "loader_trace_mismatch"
    return grade(observation["actual"], case["expected"], request["reexpand"], observation["post_expansion"])


def run_cell(out, case, engine, repetition, suite_path, state, reason):
    run_id = f"{engine}-{case['event_id']}-r{repetition}"
    folder = out / "receipts" / run_id
    folder.mkdir(parents=True)
    nonce = str(uuid4())
    argv = state.get("argv", [])
    runtime = state.get("runtime")
    overrides = {"TZ": "UTC", "LC_ALL": "C.UTF-8", **state.get("environment_overrides", {})}
    receipt = {
        "run_id": run_id, "engine": engine, "engine_commit": state.get("commit"), "runtime": runtime,
        "event_id": case["event_id"], "test_iri": case["test_iri"], "algorithm": case["algorithm"],
        "repetition": repetition, "nonce": nonce, "argv": argv, "cwd": state.get("checkout"),
        "environment_overrides": overrides, "options": case["options"], "input": case["input"],
        "context": case["context"], "expected": case["expected"],
        "spawned": False, "process_id": None, "started_utc": None, "ended_utc": None,
        "elapsed_ms": None, "exit_code": None, "files": {}, "observation": None,
        "verdict": "not_run", "rule": "prerequisite_unavailable", "not_run_reason": reason,
    }
    if not reason:
        try:
            request = request_for(case, suite_path, nonce)
        except (OSError, ValueError) as exc:
            receipt["not_run_reason"] = str(exc)
        else:
            payload = (compact_json(request) + "\n").encode()
            (folder / "request.json").write_bytes(payload)
            env = dict(os.environ)
            for key in ("NODE_OPTIONS", "NODE_PATH", "GODEBUG", "GOMAXPROCS", "GOTRACEBACK"):
                env.pop(key, None)
            env.update(overrides)
            receipt["started_utc"] = now()
            start = time.monotonic()
            try:
                child = subprocess.Popen(argv, cwd=state["checkout"], env=env, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError as exc:
                stdout, stderr = b"", b""
                receipt["not_run_reason"] = f"process failed to start: {exc}"
            else:
                receipt.update(spawned=True, process_id=child.pid)
                timeout = False
                try:
                    stdout, stderr = child.communicate(payload, timeout=30)
                except subprocess.TimeoutExpired:
                    child.kill()
                    stdout, stderr = child.communicate()
                    timeout = True
                receipt["exit_code"] = child.returncode
                if child.returncode or timeout:
                    receipt.update(verdict="incomparable", rule="timeout" if timeout else "abnormal_process_exit")
                else:
                    try:
                        observed = json.loads(stdout)
                        receipt["observation"] = observed
                        expected_runtime = runtime.split()[2] if engine == "gold" else runtime
                        receipt["verdict"], receipt["rule"] = decode_case(
                            observed, case, request, child.pid, expected_runtime
                        )
                    except (ValueError, TypeError, KeyError) as exc:
                        receipt.update(verdict="incomparable", rule="adapter_protocol_failure", diagnostic=str(exc))
            receipt["ended_utc"] = now()
            receipt["elapsed_ms"] = round((time.monotonic() - start) * 1000, 3)
            (folder / "stdout.log").write_bytes(stdout)
            (folder / "stderr.log").write_bytes(stderr)
            receipt["files"] = {name: file_meta(folder / name) for name in ("request.json", "stdout.log", "stderr.log")}
    written_json(folder / "receipt.json", receipt)
    return receipt


def outcome(receipt):
    if receipt["verdict"] not in ("pass", "fail"):
        return None
    return receipt["observation"]["actual"]


def short_outcome(record):
    actual = outcome(record)
    if actual is None:
        return ""
    if actual["kind"] == "json":
        return compact_json(actual["value"])
    return actual["code"]


def compared(left, right):
    a, b = outcome(left), outcome(right)
    if a is None or b is None:
        return "unavailable"
    if not equal_observation(a, b) or left["verdict"] != right["verdict"]:
        return "different"
    post_a, post_b = (r["observation"]["post_expansion"] for r in (left, right))
    if post_a or post_b:
        if not post_a or not post_b:
            return "different"
        if not equal_observation(post_a["actual"], post_b["actual"]):
            return "different"
    return "same"


def build_comparisons(plan, by_key):
    historical = {(r["engine"], r["algorithm"], r["test_iri"]): r for r in plan["historical"]}
    reports = {r["engine"]: r for r in plan["earl_reports"]}
    result = []
    for case in plan["cases"]:
        event, algorithm, iri = case["event_id"], case["algorithm"], case["test_iri"]
        repeated = {}
        for engine in plan["run_contract"]["engines"]:
            a, b = by_key[engine, event, 1], by_key[engine, event, 2]
            repeated[engine] = compared(a, b)
            result.append({
                "comparison_id": f"R-{engine}-{event}", "layer": "within_engine_repetition",
                "event_id": event, "algorithm": algorithm, "test_iri": iri,
                "left_id": a["run_id"], "right_id": b["run_id"], "left_actual": short_outcome(a),
                "right_actual": short_outcome(b), "left_verdict": a["verdict"], "right_verdict": b["verdict"],
                "comparison": repeated[engine], "new_run_utc": f"{a['started_utc']} / {b['started_utc']}",
                "historical_date_lexical": "", "historical_repo_date": "",
                "historical_source_url": "", "unknown_historical_conditions": "",
            })
        gold, js = by_key["gold", event, 1], by_key["js", event, 1]
        result.append({
            "comparison_id": f"X-{event}", "layer": "between_engines",
            "event_id": event, "algorithm": algorithm, "test_iri": iri,
            "left_id": gold["run_id"], "right_id": js["run_id"], "left_actual": short_outcome(gold),
            "right_actual": short_outcome(js), "left_verdict": gold["verdict"], "right_verdict": js["verdict"],
            "comparison": compared(gold, js) if set(repeated.values()) == {"same"} else "unavailable",
            "new_run_utc": f"{gold['started_utc']} / {js['started_utc']}",
            "historical_date_lexical": "", "historical_repo_date": "",
            "historical_source_url": "", "unknown_historical_conditions": "",
        })
        for engine in plan["run_contract"]["engines"]:
            current = by_key[engine, event, 1]
            old = historical[engine, algorithm, iri]
            relation = "unavailable"
            if repeated[engine] == "same":
                relation = "same_verdict" if (current["verdict"], old["outcome"]) in (
                    ("pass", "passed"), ("fail", "failed")
                ) else "different_verdict"
            result.append({
                "comparison_id": f"H-{engine}-{event}", "layer": "current_vs_reported_earl",
                "event_id": event, "algorithm": algorithm, "test_iri": iri,
                "left_id": f"{engine}-{event}-r1 / r2", "right_id": old["assertion_id"],
                "left_actual": short_outcome(current), "right_actual": "",
                "left_verdict": current["verdict"], "right_verdict": old["outcome"],
                "comparison": relation, "new_run_utc": current["started_utc"],
                "historical_date_lexical": old["assertion_date_lexical"],
                "historical_repo_date": reports[engine]["repository_receipt"]["committer_date"],
                "historical_source_url": old["source_url"],
                "unknown_historical_conditions": "suite SHA, options, raw log, historical runtime",
            })
    return result


def csv_rows(path, rows):
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_row(receipt, repeat_comparison):
    run_id = receipt["run_id"]
    folder = f"receipts/{run_id}"
    actual = receipt["observation"]["actual"] if receipt["observation"] else {}
    return {
        "run_id": run_id, "event_id": receipt["event_id"], "algorithm": receipt["algorithm"],
        "test_iri": receipt["test_iri"], "engine": receipt["engine"], "engine_commit": receipt["engine_commit"],
        "runtime": receipt["runtime"], "repetition": receipt["repetition"],
        "pid": receipt["process_id"], "nonce": receipt["nonce"], "started_utc": receipt["started_utc"],
        "ended_utc": receipt["ended_utc"], "elapsed_ms": receipt["elapsed_ms"],
        "command": shlex.join(receipt["argv"]) + " < " + folder + "/request.json" if receipt["argv"] else "",
        "receipt": folder + "/receipt.json", "exit_code": receipt["exit_code"],
        "actual_kind": actual.get("kind", ""), "actual_json": compact_json(actual["value"]) if "value" in actual else "",
        "error_code": actual.get("code", ""), "verdict": receipt["verdict"], "rule": receipt["rule"],
        "repeat_comparison": repeat_comparison, "not_run_reason": receipt["not_run_reason"],
        "stdout_path": folder + "/stdout.log" if receipt["files"] else "",
        "stdout_sha256": receipt["files"].get("stdout.log", {}).get("sha256", ""),
        "stderr_path": folder + "/stderr.log" if receipt["files"] else "",
        "stderr_sha256": receipt["files"].get("stderr.log", {}).get("sha256", ""),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, type=Path, help="runtime.json written by prepare.py")
    parser.add_argument("--out", required=True, type=Path, help="new or empty output directory")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if any(args.out.iterdir()):
        parser.error("--out must be empty")
    plan = json.loads(INPUTS.read_bytes())
    setup = json.loads(args.runtime.read_bytes())
    blockers = {}
    for role, item in setup.items():
        try:
            blockers[role] = verify_installation(role, item)
        except (OSError, subprocess.CalledProcessError) as exc:
            blockers[role] = f"prepared installation verification failed: {exc}"
    runs = {}
    for rep in range(1, plan["run_contract"]["repetitions"] + 1):
        for engine in plan["run_contract"]["engines"]:
            for case in plan["cases"]:
                receipt = run_cell(args.out, case, engine, rep, setup["suite"].get("checkout"), setup[engine],
                                   blockers["suite"] or blockers[engine])
                runs[engine, case["event_id"], rep] = receipt
    comparisons = build_comparisons(plan, runs)
    repeat = {row["left_id"]: row["comparison"] for row in comparisons if row["layer"] == "within_engine_repetition"}
    csv_rows(args.out / "runs.csv", [run_row(row, repeat[row["run_id"].replace("-r2", "-r1")]) for row in runs.values()])
    csv_rows(args.out / "comparison.csv", comparisons)
    print(compact_json({
        "planned": len(runs), "spawned": sum(record["spawned"] for record in runs.values()),
        "verdicts": {kind: sum(record["verdict"] == kind for record in runs.values())
                     for kind in ("pass", "fail", "incomparable", "not_run")},
    }))
    return 0 if all(outcome(record) is not None for record in runs.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
