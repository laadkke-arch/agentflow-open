"""Run the blinded reader, then launch the exhaustive reference and join ledgers."""
import argparse
import copy
import itertools
import json
import os
import subprocess
import sys
from pathlib import Path
from time import perf_counter_ns

from projector import coverage, logical_records, project
from registry import (CLAIMS, ENTRYPOINTS, ROOT, STATES, VIEWS, encode, sha, summarize,
                      write_csv, write_json, write_jsonl)

SCRIPTS = Path(__file__).resolve().parent
MAX_ASSET_BYTES = 131072
RULES = json.loads((ROOT / "inputs/rules.json").read_bytes())
EXEC_READER = "import runpy,sys; sys.path.insert(0,sys.argv[1]); runpy.run_module('reader',run_name='__main__')"


class Broker:
    """Serve one current lookup and up to two phased historical lookups."""

    def __init__(self, out, case, state):
        self.root = out / "broker-assets"
        self.old = case["before"]
        self.current = case["after"]
        self.domain = case["domain"]
        self.retained = state == "retained"
        self.events = []
        self.seen = set()

    def response(self, request):
        slot, phase = request.get("slot"), request.get("phase")
        key = slot, phase
        asset = self.old if slot == "historical" else self.current
        entrypoint = ENTRYPOINTS[self.domain]
        accepted = (
            set(request) == {"entrypoint", "slot", "phase", "revision"}
            and request["entrypoint"] == entrypoint
            and key not in self.seen
            and (key == ("current", "initial") and request["revision"] is None
                 or slot == "historical" and request["revision"] == asset["edition"]
                 and (phase == "initial" or phase == "post_defer"
                      and ("historical", "initial") in self.seen))
        )
        source_read_bytes = 0
        local_file_reads = 0
        result = {"status": "route_rejected"}
        if accepted:
            self.seen.add(key)
            if slot == "historical" and not self.retained:
                result = {"status": "historical_unavailable"}
            else:
                location = self.root / asset["sha256"]
                if location.stat().st_size <= MAX_ASSET_BYTES:
                    raw = location.read_bytes()
                    local_file_reads = 1
                    source_read_bytes = len(raw)
                    result = {
                        "status": "available", "edition": asset["edition"], "raw": raw.decode(),
                        "sha256": asset["sha256"], "rows": asset["row_count"], "rule": RULES[self.domain],
                    }
                else:
                    result = {"status": "file_budget_exceeded"}
        self.events.append({
            "sequence": len(self.events) + 1, "slot": slot, "phase": phase,
            "entrypoint": request.get("entrypoint"), "requested_edition": request.get("revision"),
            "status": result["status"], "source_read_bytes": source_read_bytes,
            "local_file_reads": local_file_reads, "asset_sha256": result.get("sha256"),
            "source_url": asset["url"] if source_read_bytes else None,
            "raw_budget_bytes": MAX_ASSET_BYTES,
        })
        return result


def exchange(out, case, state, wire):
    broker = Broker(out, case, state)
    command = [sys.executable, "-B", "-I", "-c", EXEC_READER, str(SCRIPTS)]
    started = perf_counter_ns()
    with subprocess.Popen(command, cwd=out / "blind-cwd", env={},
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as proc:
        proc.stdin.write(wire + b"\n")
        proc.stdin.flush()
        decision = None
        error = None
        for message in proc.stdout:
            event = json.loads(message)
            if "read" in event:
                proc.stdin.write(encode(broker.response(event["read"])) + b"\n")
                proc.stdin.flush()
            elif "decision" in event:
                decision = event["decision"]
            else:
                error = event.get("error", "invalid reader message")
        status = proc.wait()
        stderr = proc.stderr.read().decode()
    if status and not error:
        error = "reader subprocess failed"
    return {"decision": decision, "error": error, "exit": status,
            "stderr": stderr, "reads": broker.events}, perf_counter_ns() - started


def put_projection(out, case, view, record, projections, role):
    raw = encode(record)
    digest = sha(raw)
    relative = f"views/{digest}.json"
    path = out / relative
    if not path.exists():
        path.write_bytes(raw)
    size = path.stat().st_size
    info = {
        "pair_id": case["pair_id"], "role": role, "view": view, "path": relative,
        "sha256": digest, "build_bytes": size, "logical_records": logical_records(view, record),
        "historical_asset_sha256": case["before"]["sha256"],
    }
    projections.append(info)
    return info


def identify(case, claim, view, state):
    return ".".join((case["pair_id"], claim, view, state))


def read_case(out, case, claim, view, state, projection, expected_record=None):
    data = (out / projection["path"]).read_bytes()
    if sha(data) != projection["sha256"]:
        raise ValueError("Projection changed between write and read")
    object_data = json.loads(data)
    if expected_record is not None and expected_record != object_data:
        raise ValueError("Unexpected projection value")
    request = {"domain": case["domain"], "query": case["query"], "claim": claim,
               "view": view, "record": object_data, "entrypoint": ENTRYPOINTS[case["domain"]]}
    wire = encode(request)
    output, elapsed = exchange(out, case, state, wire)
    input_log = {key: value for key, value in request.items() if key != "record"} | {
        "projection_path": projection["path"], "projection_sha256": projection["sha256"],
        "wire_sha256": sha(wire), "wire_bytes": len(wire),
    }
    run_id = identify(case, claim, view, state)
    return (
        {"run_id": run_id, "pair_id": case["pair_id"], "state": state, "input": input_log, **output},
        {"run_id": run_id, "reader_wall_ns": elapsed},
    )


def read_all(out, cases):
    measurements, timings, projections = [], [], []
    for case in cases:
        domain = case["domain"]
        asset = case["before"]
        raw = (out / "broker-assets" / asset["sha256"]).read_bytes()
        projections_start = perf_counter_ns()
        source_views = project(domain, case["query"], asset, raw, RULES[domain])
        packed = {view: put_projection(out, case, view, value, projections, case["kind"])
                  for view, value in source_views.items()}
        timings.append({"capture": case["pair_id"], "capture_all_views_wall_ns":
                        perf_counter_ns() - projections_start})
        for claim, view, state in itertools.product(CLAIMS, VIEWS, STATES):
            run, time = read_case(out, case, claim, view, state, packed[view])
            cost = measure(run, packed[view])
            measurements.append((run, cost))
            timings.append(time)
    return measurements, timings, projections


def measure(run, projection):
    reads = run["reads"]
    archive = [event for event in reads if event["slot"] == "historical"]
    current = [event for event in reads if event["slot"] == "current"]
    after_defer = [event for event in archive if event["phase"] == "post_defer"]
    return {
        "run_id": run["run_id"], "pair_id": run["pair_id"], "claim": run["input"]["claim"],
        "view": run["input"]["view"], "state": run["state"],
        "projection_sha256": projection["sha256"], "build_bytes": projection["build_bytes"],
        "logical_records": projection["logical_records"], "stored_read_bytes": projection["build_bytes"],
        "origin_local_requests": len(reads), "historical_initial_requests": len(archive) - len(after_defer),
        "historical_post_defer_requests": len(after_defer), "current_requests": len(current),
        "local_file_reads": sum(event["local_file_reads"] for event in reads),
        "local_read_bytes": sum(event["source_read_bytes"] for event in reads),
        "historical_read_bytes": sum(event["source_read_bytes"] for event in archive),
        "current_read_bytes": sum(event["source_read_bytes"] for event in current),
        "post_defer_read_bytes": sum(event["source_read_bytes"] for event in after_defer),
    }


def losses(out, cases, projections, timings):
    donor = next(case for case in cases if case["pair_id"] == "TZ-C01")
    asset = donor["after"]
    raw = (out / "broker-assets" / asset["sha256"]).read_bytes()
    domain, query = donor["domain"], donor["query"]
    views = project(domain, query, asset, raw, RULES[domain])
    remove = next(row_id for row_id, key in views["B"]["keys"]
                  if key == ["AD"] and row_id != views["B"]["witness"]["id"])
    dropped = copy.deepcopy(views["B"])
    dropped["keys"] = [row for row in dropped["keys"] if row[0] != remove]
    forged = copy.deepcopy(views["B"])
    forged["keys"] = [[row_id, ["AQ"] if row_id == remove else key]
                      for row_id, key in forged["keys"]]
    recomputed = summarize(domain, query, forged["keys"], forged["rule"])
    forged["coverage"] = coverage(forged["keys"], recomputed, asset, domain, query, forged["rule"])
    partial = copy.deepcopy(views["C"])
    partial["source_raw"] = "".join(
        line for line in partial["source_raw"].splitlines(keepends=True)
        if len(line.split("\t")) < 3 or line.split("\t")[2] != remove
    )
    assert len(partial["source_raw"]) < len(views["C"]["source_raw"])
    no_rule = {view: {k: v for k, v in views[view].items() if k != "rule"} for view in ("B", "C")}
    naive = summarize(domain, query, dropped["keys"], dropped["rule"])
    probes = [
        ("LOSS01", "B", dropped, STATES),
        ("LOSS02", "B", no_rule["B"], STATES),
        ("LOSS02", "C", no_rule["C"], STATES),
        ("LOSS03", "B", forged, ("lost",)),
        ("LOSS04", "C", partial, ("lost",)),
    ]
    outcomes = []
    for probe, view, record, states in probes:
        case = donor | {"pair_id": probe, "before": asset}
        info = put_projection(out, case, view, record, projections, "loss_probe")
        for claim, state in itertools.product(("unique", "top"), states):
            run, elapsed = read_case(out, case, claim, view, state, info, record)
            timings.append(elapsed)
            run["unsafe_subset_value"] = naive[claim] if probe == "LOSS01" else None
            run["modified_peer_id"] = remove if probe != "LOSS02" else None
            run["reference"] = {"pair_id": "TZ-C01", "phase": "after"}
            outcomes.append(run)
    return outcomes


def full_reference(out, cases):
    results = []
    for case in cases:
        for phase in ("before", "after"):
            asset = case[phase]
            path = (out / "oracle-assets" / asset["sha256"]).resolve()
            if sha(path.read_bytes()) != asset["sha256"]:
                raise ValueError("Oracle source failed its sealed digest")
            command = [sys.executable, "-B", "-I", str(SCRIPTS / "oracle.py"), case["domain"],
                       case["query"], str(path)]
            run = subprocess.run(command, env={}, cwd=out / "oracle-cwd", capture_output=True,
                                 check=True)
            result = json.loads(run.stdout)
            if result["scanned"] != asset["row_count"]:
                raise ValueError("Independent oracle did not traverse the pinned population")
            results.append({
                "pair_id": case["pair_id"], "phase": phase, "domain": case["domain"],
                "query": case["query"], "scope_url": asset["url"], "asset_sha256": asset["sha256"],
                **result,
            })
    return results


def grade(expected, value):
    if value["status"] == "deferred":
        return "defer"
    return "correct" if expected == value["value"] else "wrong"


def claim_text(claim, value):
    # independent text template for checking the original output, not used in solving.
    if claim == "top":
        return "공동 1위 " + (", ".join(value) if value else "없음")
    return {"exists": "적격 후보 있음", "unique": "적격 후보 정확히 하나"}[claim] + (
        " · 참" if value else " · 거짓"
    )


def score(run, lookup):
    claim = run["input"]["claim"]
    pair_id = run["pair_id"]
    before, after = (lookup[(pair_id, phase)][claim] for phase in ("before", "after"))
    if run["exit"] or run["decision"] is None:
        raise ValueError(f"Reader failed: {run['run_id']}, {run['error']}, {run['stderr']}")
    outcome = run["decision"]
    return {
        "run_id": run["run_id"], "pair_id": pair_id, "claim": claim,
        "view": run["input"]["view"], "state": run["state"], "pair_weight": 1,
        "display": "correct" if outcome["display"] == claim_text(claim, before) else "wrong",
        "historical": grade(before, outcome["historical"]), "current": grade(after, outcome["current"]),
        "oracle_before_json": encode(before).decode(), "oracle_after_json": encode(after).decode(),
    }


def leakage(out, cases, projections):
    case = next(row for row in cases if row["pair_id"] == "TZ-C01")
    projection = next(row for row in projections if row["pair_id"] == case["pair_id"]
                      and row["view"] == "B")
    record = json.loads((out / projection["path"]).read_bytes())
    request = {"domain": "TZ", "query": case["query"], "claim": "top",
               "entrypoint": ENTRYPOINTS["TZ"], "view": "B", "record": record}
    clean, _ = exchange(out, case, "lost", encode(request))
    attempts = []
    for field in ("oracle_answer", "pair_id", "mutation", "expected", "hidden_candidate_id"):
        poisoned, _ = exchange(out, case, "lost", encode(request | {field: "input-canary"}))
        attempts.append({"field": field, "result": poisoned["error"], "exit": poisoned["exit"],
                         "route_reads": len(poisoned["reads"])})
    tampered = copy.deepcopy(request)
    tampered["record"]["display"]["top"] = "untrusted-text-canary"
    altered, _ = exchange(out, case, "lost", encode(tampered))
    forbidden = Broker(out, case, "lost")
    bad = forbidden.response({"entrypoint": "file:///oracle-assets", "slot": "current",
                              "phase": "initial", "revision": None})
    return {
        "top_level_canaries": attempts, "display_before": clean["decision"]["display"],
        "display_after": altered["decision"]["display"],
        "historical_unchanged": clean["decision"]["historical"] == altered["decision"]["historical"],
        "current_unchanged": clean["decision"]["current"] == altered["decision"]["current"],
        "forbidden_route": bad["status"], "forbidden_route_reads": forbidden.events[0]["local_file_reads"],
        "reader_cwd_empty": not any((out / "blind-cwd").iterdir()),
        "oracle_input_path_is_separate": not os.path.samefile(out / "oracle-assets", out / "broker-assets"),
    }


def run(out):
    if (out / "runs.jsonl").exists():
        raise ValueError("Already run. Prepare a new directory.")
    cases = json.loads((out / "sealed.json").read_bytes())
    (out / "views").mkdir()
    measurements, timings, projections = read_all(out, cases)
    probes = losses(out, cases, projections, timings)
    boundary = leakage(out, cases, projections)
    # All blinded processes have exited before starting the full-input oracle.
    truth = full_reference(out, cases)
    lookup = {(row["pair_id"], row["phase"]): row for row in truth}
    primary, secondary = [], []
    for run_row, cost in measurements:
        if run_row["pair_id"] == "SWAP01":
            secondary.append(run_row)
        else:
            primary.append((run_row, cost))
    raw_runs, costs = map(list, zip(*primary, strict=True))
    grades = [score(row, lookup) for row in raw_runs]
    for row in secondary:
        row["grades"] = score(row, lookup)
    for row in probes:
        truth_key = (row["reference"]["pair_id"], row["reference"]["phase"])
        expected = lookup[truth_key][row["input"]["claim"]]
        row["oracle_historical"] = expected
        row["historical_grade"] = grade(expected, row["decision"]["historical"])
    for name, rows in (
        ("runs", raw_runs), ("truth", truth), ("losses", probes), ("swap", secondary),
        ("projections", projections), ("timings", timings),
    ):
        write_jsonl(out / f"{name}.jsonl", rows)
    write_json(out / "input-boundary.json", boundary)
    write_csv(out / "scores.csv", list(grades[0]), grades)
    write_csv(out / "costs.csv", list(costs[0]), costs)
    print(f"{len(raw_runs)} primary judgments; {len(secondary)} swap judgments; "
          f"{len(probes)} loss judgments; {len(truth)} independent edition reads")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--out", type=Path, required=True)
    args = cli.parse_args()
    run(args.out.resolve())
