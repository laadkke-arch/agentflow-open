"""Score separately captured answers against the sealed source reader and controlled contracts."""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from events import ROOT, encoded

SCOPED = {"A", "B", "C"}
CONTROLS = {
    "S-BASE": (",", "decimal"), "S-T3": "temporary", "S-T4": "temporary",
    "S-T5": (".", "decimal"), "S-T6": (".", "decimal"),
    "S-FIRST3": "temporary", "S-FIRST4": "temporary", "S-FIRST5": (".", "decimal"),
    "S-FIRST6": (".", "decimal"), "S-ABS1": "key_absent", "S-ABS2": "key_absent",
    "S-OTHER": (",", "decimal"), "S-UNSET": (",", "decimal"),
    "S-INPUT": (",", "decimal"), "S-ALT-A": (",", "decimal"), "S-ALT-B": (",", "group"),
    "S-ENTRY-V1": (".", "decimal"), "S-NEXT": (".", "decimal"), "S-NEW-OBS": (".", "decimal"),
    "S-LATE-OLD": (",", "decimal"), "S-LATE-NOW": (".", "decimal"),
    "S-LATE-P2": (".", "decimal"), "S-ENTRY-V2": "entry_unavailable",
    "S-SAME-A": (",", "decimal"), "S-SAME-B": (",", "decimal"),
    "S-MIRROR": (".", "decimal"), "S-OUT-NOW": "access_lost",
}
EVIDENCE_EVENTS = {
    "S-UNOBS", "S-LINK", "S-REG", "S-BASE", "S-T3", "S-T4", "S-T5", "S-T6",
    "S-FIRST5", "S-FIRST6", "S-ABS1", "S-OTHER", "S-ABS2", "S-UNSET", "S-INPUT",
    "S-ALT-A", "S-ALT-B", "S-DUP1", "S-DUP2", "S-KNOWN-BEFORE", "S-KNOWN-AFTER",
    "S-RECON", "S-NEXT", "S-NEW-OBS", "S-ARRIVE-f1", "S-ARRIVE-f2", "S-KNOWN-LATE",
    "S-LATE-OLD", "S-LATE-NOW", "S-LATE-P2", "S-ENTRY-V2", "S-SAME-B", "S-MIRROR",
    "S-H-BASE", "S-H-TEMP", "S-H-NEXT", "S-H-DUP-PROOF", "S-OUT-NOW",
    "D-tzdb-2023b-TZ-A-P1", "D-tzdb-2023c-TZ-A-OLD-P2", "D-cldr-44-CL-U1-P1",
    "D-cldr-43.1-CL-A-P1", "D-cldr-44-CL-A-OLD-P2",
}


def cell_value(req, fact):
    """Reference implementation of the stated input contract, independent of SQLite."""
    if req["mode"] == "unknown":
        return "hold", "preference_unknown", None
    if isinstance(fact, str):
        return "hold", fact, None
    role = req["role"]
    if role and role != fact["role"]:
        return "reject", "role_mismatch", fact
    if req["mode"] == "literal":
        token = fact["symbol"] if role else fact["abbreviation"]
        if token == req["literal"]:
            return "approve", "literal_preserved", {"role": role or "abbreviation", "literal": token}
        return "reject", "literal_changed", {"role": role or "abbreviation", "literal": token}
    if role:
        is_fraction = role == "decimal"
        digits = "125" if is_fraction else "1234"
        native = [req["digits"][int(d)] for d in digits]
        at = 2 if is_fraction else 1
        rendered = "".join(native[:at]) + fact["symbol"] + "".join(native[at:])
        return "approve", "number_preserved", {"display": rendered, "role": role,
                                                "number": "12.5" if is_fraction else "1234"}
    utc = datetime.fromisoformat(req["utc"])
    offset = fact["offset_seconds"]
    local = datetime.fromtimestamp(utc.timestamp() + offset, tz=timezone.utc)
    return "approve", "instant_preserved", {"offset_seconds": offset,
                                            "local": local.strftime("%Y-%m-%dT%H:%M:%S"),
                                            "utc": req["utc"]}


def synthetic_location(edition, e):
    return f'replay/fixture_source.json#/{edition}/{e["key"]}/{e["scope"] or "general"}'


def prepare_expectations(events, oracle, phase):
    latest = {}
    expectations = {}
    for e in events:
        action = e["action"]
        if action == "publish":
            latest[e["url"]] = e["edition"]
            continue
        if action in {"ingest", "register"}:
            continue
        edition = key = proof = location = source_ids = url = ""
        requested = e.get("selector", "")
        project = e.get("project", "")
        if action == "catalog":
            verdict, reason, value = (("hold", "unobserved", e["url"]) if phase == "first"
                                      else ("link", "tracked_link", e["url"]))
        elif action == "bookmark":
            verdict, reason, value = "link", "address", e["url"]
        elif action in {"history", "reconstruct"}:
            expectations[e["id"]] = dict(expectations[e["target"]])
            continue
        elif action == "asof":
            query = e["id"]
            known = query == "S-KNOWN-AFTER" or (query == "S-KNOWN-LATE" and
                                                  e["sequence"] == "reversed")
            verdict, reason = (("known", "observed_before_cutoff") if known else
                               ("unknown", "no_qualified_observation"))
            value = {"role": "decimal", "symbol": ","} if known else None
            edition, key = e["edition"], e["key"]
            if known:
                proof, location, url = edition, synthetic_location(edition, e), "replay/fixture_source.json"
        elif action == "current":
            edition = latest[e["url"]] if requested == "latest" else requested
            key = e["key"]
            if e["cohort"] == "public":
                original = oracle[e["family"], edition, key]
                fact = (json.loads(original["effective_value"]) if original["availability"] == "available"
                        else "key_absent" if original["availability"] == "absent" else "path_unresolved")
                location, url, source_ids = (original["source_location"], original["fixed_url"],
                                             original["source_ids"])
            else:
                assigned = CONTROLS[e["id"]]
                fact = ({"symbol": assigned[0], "role": assigned[1]} if isinstance(assigned, tuple)
                        else assigned)
                location, url = synthetic_location(edition, e), "replay/fixture_source.json"
            proof = edition
            verdict, reason, value = cell_value(e["input"], fact)
        else:
            raise ValueError(action)
        expectations[e["id"]] = {"verdict": verdict, "reason": reason, "value": value,
                                 "requested": requested, "edition": edition, "proof": proof,
                                 "key": key, "location": location, "project": project,
                                 "fixed_url": url, "source_ids": source_ids}
    return expectations


def same_result(a, b):
    return all(a[key] == b[key] for key in ("outcome", "reason", "value"))


def grade(run, event, out, expected, previous, last_seen, prior_outputs):
    act = out["answer"]
    if act is None:
        return None
    eid, action = event["id"], event["action"]
    actual = act["outcome"]
    ok = actual == expected["verdict"] and act["value"] == expected["value"]
    reason_correct = act["reason"] == expected["reason"]
    verdict = expected["verdict"]
    is_history = action == "history"
    basis = act["basis"] or {}
    real_basis = last_seen.get(event["url"], {}) if out["transition"] == "last-url-hit" else basis
    proof = expected["proof"]
    matched = ""
    if proof:
        if not all(basis.get(key) is not None for key in ("edition", "key", "location", "at")):
            matched = "missing"
        elif ((proof, expected["key"], expected["location"]) ==
              (basis["edition"], basis["key"], basis["location"])):
            matched = "matched"
        else:
            matched = "mismatch"
    fidelity = ""
    if action in {"history", "reconstruct"}:
        fidelity = ("faithful" if act["mode"] == "recorded"
                    and same_result(act, prior_outputs[event["target"]]) else
                    "reconstructed" if act["mode"] == "reconstructed" and ok else "unproven")
    if is_history and act["mode"] == "not_recorded":
        status = "wrong_hold"
    elif action == "asof":
        status = "asof_correct" if ok else ("false_knowledge" if actual == "known" else "knowledge_unproven")
    elif actual == "hold":
        status = "warranted_hold" if verdict == "hold" else "wrong_hold"
    elif actual == "approve" and not ok:
        status = "false_approval"
    elif actual == "reject" and not ok:
        status = "wrong_rejection"
    else:
        status = "correct" if ok else "wrong_response"
    stale = bool(action == "current" and actual == "approve" and real_basis.get("edition") and
                 real_basis["edition"] != expected["edition"])
    wrong_key = bool(action == "current" and real_basis.get("key") and real_basis["key"] != expected["key"])
    wrong_scope = bool(action == "current" and event.get("scope") and real_basis.get("scope") and
                       event["scope"] != real_basis["scope"])
    externally_false_hold = (eid in {"S-T5", "S-T6", "S-FIRST5", "S-FIRST6"} and
                             actual == "hold" and act["reason"] == "temporary")
    unnecessary = bool(action == "current" and event["retry"] and out["acquire_calls"] and
                       previous and all(expected[k] == previous[k] for k in
                                        ("verdict", "reason", "value", "edition", "key", "location")))
    return {
        "sequence": run["sequence"], "cohort": event["cohort"], "design": run["design"],
        "cache": run["policy"], "phase": run["phase"], "masked": run["mask"] or "",
        "id": eid, "action": action, "historical_target": event.get("target", ""), "at": event["at"],
        "cutoff": event.get("cutoff", ""), "family": event["family"], "url": event["url"],
        "key": expected["key"], "project": expected["project"], "request_selector": expected["requested"],
        "request_edition": expected["edition"], "actual_observed_edition": basis.get("edition", ""),
        "actual_observed_key": basis.get("key", ""), "actual_observed_at": basis.get("at", ""),
        "actual_location": basis.get("location", ""), "observation_id": basis.get("id", ""),
        "observed_kind": basis.get("kind", ""), "evaluable_proof_edition": real_basis.get("edition", ""),
        "evaluable_proof_key": real_basis.get("key", ""),
        "expected_location": expected["location"], "expected_fixed_url": expected["fixed_url"],
        "source_ids": expected["source_ids"], "expected_outcome": verdict,
        "expected_value": encoded(expected["value"]), "expected_reason": expected["reason"],
        "actual_outcome": actual, "actual_value": encoded(act["value"]), "actual_reason": act["reason"],
        "mode": act["mode"], "grade": status, "reason_matches": int(reason_correct),
        "proof": matched, "delivery_fidelity": fidelity,
        "stale_success": int(stale), "cross_key_or_scope": int(wrong_key or wrong_scope),
        "recovery_held": int(externally_false_hold),
        "unnecessary_retry": int(unnecessary),
        "acquire_calls": out["acquire_calls"], "local_file_reads": len(out["reads"]),
        "local_body_bytes": sum(item[1] for item in out["reads"]), "transition": out["transition"],
    }


def assess(run, events, oracle, first):
    exp = prepare_expectations(events, oracle, run["phase"])
    earlier_outputs, earlier_acquisitions = first or ({}, {})
    previous = {}
    answers = []
    state = earlier_acquisitions.copy()
    matrix = []
    for event, out in zip(events, run["trace"], strict=True):
        if event["id"] != out["id"]:
            raise ValueError(f'unaligned event: {event["id"]} / {out["id"]}')
        before = state.get(event["url"])
        if out["fetched"]:
            state[event["url"]] = out["fetched"]
        feedback = grade(run, event, out, exp[event["id"]], exp.get(event.get("prior")),
                         state, earlier_outputs or previous) if event["id"] in exp else None
        if feedback:
            answers.append(feedback)
            previous[event["id"]] = out["answer"]
        if event["id"] in EVIDENCE_EVENTS:
            after = state.get(event["url"])
            matrix.append({"sequence": run["sequence"], "design": run["design"], "cache": run["policy"],
                           "event_id": event["id"], "phase": run["phase"], "masked": run["mask"],
                           "idempotence": out["transition"], "written_rows": out["sqlite_changes"],
                           "diagnostic_last_fetch_before": before, "diagnostic_last_fetch_after": after,
                           "returned": out["answer"]})
    return answers, (previous, state), matrix


def duration_ns(items):
    return round(sum(e["wall_ns"] for e in items) / 1_000_000, 3)


def summarize(run, answers, events, replica):
    lookup = {e["id"]: e for e in events}
    traces = run["trace"]
    path_reads = [path for e in traces for path, _ in e["reads"]]
    grade_counts = Counter(a["grade"] for a in answers)
    started = [e for e in traces if lookup[e["id"]]["action"] == "register"]
    catalogue = [e for e in traces if lookup[e["id"]]["action"] == "catalog"]
    basis_counts = Counter(a["proof"] for a in answers)
    action_counts = Counter(a["action"] for a in answers)
    tables = run["db"]["tables"]
    return {
        "replica": replica, "sequence": run["sequence"], "design": run["design"],
        "cache": run["policy"], "masked": run["mask"] or "", "phase": run["phase"],
        "queries": len(answers), "current_queries": action_counts["current"],
        "history_queries": action_counts["history"], "asof_queries": action_counts["asof"],
        "sql_lookups": run["lookups"], "acquire_calls": sum(t["acquire_calls"] for t in traces),
        "local_file_reads": len(path_reads), "local_unique_files": len(set(path_reads)),
        "local_body_bytes": sum(byte_count for e in traces for _, byte_count in e["reads"]),
        "sqlite_changes": sum(t["sqlite_changes"] for t in traces),
        "stored_logical_bytes": sum(t["bytes"] for t in tables.values()),
        "links_bytes": tables["links"]["bytes"],
        "observation_bytes": sum(t["bytes"] for name, t in tables.items()
                                 if name in {"observations", "last_observation"}),
        "decision_bytes": tables.get("decisions", {}).get("bytes", 0),
        "sqlite_pages": run["db"]["pages"], "sqlite_page_size": run["db"]["page_size"],
        "sqlite_file_bytes": run["db"]["file_bytes"], "integrity": run["db"]["integrity"],
        "wall_ms": round(run["wall_ns"] / 1_000_000, 3),
        "setup_ms": round(run["setup_ns"] / 1_000_000, 3), "registration_wall_ms": duration_ns(started),
        "catalog_wall_ms": duration_ns(catalogue), "catalog_acquires": sum(e["acquire_calls"] for e in catalogue),
        "after_first_register_logical_bytes": sum(t["bytes"] for t in run["first_registration"]["tables"].values()),
        "after_first_register_pages": run["first_registration"]["pages"],
        "after_first_register_file_bytes": run["first_registration"]["file_bytes"],
        "observation_inserts": run["observations_inserted"],
        "reuse_observation": sum(t["transition"] == "observation-hit" for t in traces),
        "reuse_decision": sum(t["transition"] == "decision-hit" for t in traces),
        "reuse_last_url": sum(t["transition"] == "last-url-hit" for t in traces),
        "retry_acquires": sum(a["acquire_calls"] for a in answers if lookup[a["id"]].get("retry")),
        "unnecessary_retries": sum(a["unnecessary_retry"] for a in answers),
        "same_delivery_writes": sum(t["sqlite_changes"] for t in traces if t["id"] == "S-DUP2"),
        "stale_success": sum(a["stale_success"] for a in answers),
        "cross_key_or_scope": sum(a["cross_key_or_scope"] for a in answers),
        "recovery_held": sum(a["recovery_held"] for a in answers),
        "terminal_recovery_held": sum(a["recovery_held"] for a in answers
                                      if a["id"] in {"S-T6", "S-FIRST6"}),
        "false_approval": grade_counts["false_approval"], "wrong_hold": grade_counts["wrong_hold"],
        "wrong_rejection": grade_counts["wrong_rejection"], "warranted_hold": grade_counts["warranted_hold"],
        "false_knowledge": grade_counts["false_knowledge"],
        "knowledge_unproven": grade_counts["knowledge_unproven"],
        "hold_reason_mismatch": sum(a["grade"] == "warranted_hold" and not a["reason_matches"]
                                    for a in answers),
        "proof_missing": basis_counts["missing"], "proof_mismatch": basis_counts["mismatch"],
        "history_faithful": sum(a["action"] == "history" and a["delivery_fidelity"] == "faithful"
                                for a in answers),
        "history_reconstructed": sum(a["delivery_fidelity"] == "reconstructed" for a in answers),
        "runtime_http_body_bytes": "unmeasured (offline source provider)", "human_time": "unmeasured",
    }


def digest(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def deterministic(payload):
    return {**payload, "runs": [
        {k: ([{ek: ev for ek, ev in e.items() if ek != "wall_ns"} for e in v] if k == "trace" else v)
         for k, v in run.items() if k not in {"wall_ns", "setup_ns"}}
        for run in payload["runs"]
    ]}


def writecsv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def changes(oracle):
    tracks = defaultdict(list)
    for cell in oracle.values():
        tracks[cell["family"], cell["layer"], cell["key"]].append(cell)
    result = {}
    for (family, layer, key), cells in tracks.items():
        totals = result.setdefault(f"{family}:{layer}", Counter())
        for older, newer in zip(cells, cells[1:]):
            totals["pairs"] += 1
            if older["availability"] != "available" or newer["availability"] != "available":
                totals["unconfirmed"] += 1
                continue
            changed = older["effective_value"] != newer["effective_value"]
            totals["changed" if changed else "same"] += 1
            if older["source_location"] != newer["source_location"] and not changed:
                totals["same_value_new_origin"] += 1
    return {k: dict(v) for k, v in result.items()}


def check(answers, costs, source, event_groups):
    by = {(r["sequence"],r["design"],r["cache"],r["phase"],r["id"]): r for r in answers}
    for design in SCOPED:
        for policy in {"off", "retry", "ttl"}:
            current = [r for r in answers if r["cohort"] == "public" and r["design"] == design
                       and r["cache"] == policy and r["phase"] == "first" and r["action"] == "current"]
            if len(current) != 144 or any(r["grade"] != "correct" or r["proof"] != "matched" for r in current):
                raise ValueError(f"main scoped source equivalence failed for {design}/{policy}")
    natural = [r for r in answers if r["sequence"] == "dense" and r["design"] == "C"
               and r["cache"] == "retry" and r["phase"] == "first" and r["action"] == "history"]
    data = {(r["family"],r["request_edition"],r["key"],r["project"]) for r in natural}
    if len(data) != 64 or len(natural) != 112 or any(r["delivery_fidelity"] != "faithful"
                                                  or r["proof"] != "matched" for r in natural):
        raise ValueError("C did not replay both projects across all 32 cells")
    for policy in {"off", "retry", "ttl"}:
        original = ("control", "C", policy, "first")
        reversed_run = ("reversed", "C", policy, "first")
        for eid in ("S-LATE-OLD","S-LATE-NOW","S-LATE-P2","S-H-BASE","S-H-NEXT","S-H-DUP-PROOF"):
            before, after = (by[(*run, eid)] for run in (original, reversed_run))
            for field in ("actual_outcome","actual_value","delivery_fidelity","actual_observed_edition"):
                if before[field] != after[field]:
                    raise ValueError(f"arrival order changed a scoped result: {policy} {eid} {field}")
        assert by[(*original, "S-KNOWN-LATE")]["actual_outcome"] == "unknown"
        assert by[(*reversed_run, "S-KNOWN-LATE")]["actual_outcome"] == "known"
    assert by[("control","B","retry","first","S-RECON")]["delivery_fidelity"] == "reconstructed"
    assert by[("control","C","retry","first","S-RECON")]["delivery_fidelity"] == "faithful"
    for row in costs:
        assert row["catalog_acquires"] == 0
        if row["phase"] == "first":
            assert row["after_first_register_logical_bytes"] > 0
        assert row["after_first_register_pages"]*row["sqlite_page_size"] == row["after_first_register_file_bytes"]
        assert row["sqlite_pages"]*row["sqlite_page_size"] == row["sqlite_file_bytes"]
        assert row["observation_bytes"]+row["decision_bytes"]+row["links_bytes"] == row["stored_logical_bytes"]
        if row["design"] in {"B","C"} and row["sequence"] in {"control","reversed"}:
            assert row["same_delivery_writes"] == 0
    source_ids = {x["source_id"] for x in source}
    assert len(source_ids) == len(source)
    assert all(s in source_ids for r in answers for s in r["source_ids"].split(";") if s)
    known_events = {e["id"] for seq in event_groups.values() for e in seq}
    unknown = {ref for s in source for ref in s["event_ids"] if ref not in known_events}
    if unknown:
        raise ValueError(f"source ledger references unknown events: {sorted(unknown)}")
    counted = [r for r in source if r["counts_toward_minimum"]]
    assert all(r["access"] == "read" and r["checked_at_utc"] for r in counted)
    count = Counter(r["category"] for r in counted)
    assert len({r["work_id"] for r in counted}) == len(counted)
    minimum = {"tzdb":6,"cldr":6,"impl-tzdb":2,"impl-cldr":2,
               "identity-cache":4,"transport":2,"statistics-standards":2}
    assert all(count[cat] >= n for cat,n in minimum.items())
    return count


def inputs_sha():
    paths = [ROOT / item for item in ("editions.csv","oracle.csv","events.jsonl","schemas.sql",
                                     "sources.jsonl","evidence/artifacts.json","evidence/calibration.json",
                                     "evidence/origin-comparisons.json")]
    paths.extend(sorted((ROOT / "replay").glob("*.py")))
    paths.extend(sorted((ROOT / "replay").glob("*.json")))
    return {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--first", type=Path, required=True)
    cli.add_argument("--second", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    A, B = (json.loads(p.read_text(encoding="utf-8")) for p in (args.first, args.second))
    da, db = deterministic(A), deterministic(B)
    if da != db:
        difference = [(i,a["sequence"],a["design"],a["policy"],a["mask"],a["phase"])
                      for i,(a,b) in enumerate(zip(da["runs"],db["runs"],strict=True)) if a != b]
        raise ValueError(f"Two from-empty runs differ: {difference}")
    events = defaultdict(list)
    for line in (ROOT / "events.jsonl").read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        events[e["sequence"]].append(e)
    with (ROOT / "oracle.csv").open(newline="",encoding="utf-8") as stream:
        oracle = {(o["family"],o["edition"],o["key"]): o for o in csv.DictReader(stream)}
    source = [json.loads(line) for line in (ROOT / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
    baseline, ablations, cost, evidence = [], [], [], []
    for name, payload in (("A", A), ("B", B)):
        first_by_config = {}
        for run in payload["runs"]:
            group = events[run["sequence"]]
            cfg = tuple(run[k] for k in ("sequence", "design", "policy", "mask"))
            rows, delivery, transitions = assess(run, group, oracle, first_by_config.get(cfg))
            if run["phase"] == "first":
                first_by_config[cfg] = delivery
            cost.append(summarize(run, rows, group, name))
            if name == "A":
                (ablations if run["mask"] else baseline).extend(rows)
                if run["phase"] == "first" and (not run["mask"] or run["sequence"] == "control"):
                    evidence.extend(transitions)
    wc = check(baseline, cost, source, events)
    output = args.output
    (output / "evidence").mkdir(parents=True, exist_ok=True)
    writecsv(output / "answers.csv", baseline)
    writecsv(output / "ablation.csv", ablations)
    writecsv(output / "costs.csv", cost)
    (output / "evidence/transitions.jsonl").write_text(
        "".join(encoded(x) + "\n" for x in evidence), encoding="utf-8")
    source_n = len(source)
    receipt = {
        "input_sha256": inputs_sha(),
        "oracle_cells": {"planned":32,"read":len(oracle),
                         "availability":dict(Counter(r["availability"] for r in oracle.values()))},
        "public_edition_adjacent_changes": changes(oracle),
        "source_ledger_rows": source_n,
        "unique_qualifying_works": dict(wc),
        "expected_scope": {k: len(v) for k,v in events.items()},
        "from_empty_replays": {"A": digest(da), "B": digest(db), "equal": True,
                               "batches_per_pass": len(A["runs"]),
                               "events_per_pass":sum(len(r["trace"]) for r in A["runs"]),
                               "engine": A["env"], "deterministic_without_nanoseconds": True},
        "result_rows": {"answers":len(baseline), "ablation":len(ablations), "costs":len(cost),
                        "transitions":len(evidence)},
        "checks": {"scoped_current": "match both independently read value and proof",
                   "dense_two_project_history": 64, "history_reads_dense_c_retry":112,
                   "normal_and_reverse_current_answers_match":True, "as_of_at_late_arrival_changes":True,
                   "idempotent_delivery_b_c":True, "no_file_fetch_for_initial_catalogue": True},
        "failures": [
            {"stage":"official archive HEAD", "result":"tunnel 403", "retry":"upstream exact-commit tree"},
            {"stage":"public script smoke", "result":"SQLite INSERT binding arity error", "status":"fixed; control smoke then all replayed"},
            {"stage":"older workflow calibration", "result":"7.8.6 require MODULE_NOT_FOUND", "separate_cohort": True},
        ],
        "variable": ["wall and setup times", "file pages on different SQLite/runtime environment",
                     "archive/preparation transfer and time"],
        "isolated_evaluation": "run.py never imports this scorer or opens oracle.csv",
    }
    (output / "evidence/receipts.json").write_text(
        json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:receipt[k] for k in ("oracle_cells","unique_qualifying_works","result_rows")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
