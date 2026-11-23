"""Run the instrumented comparisons, view judgments, costs, and fault probes."""
import argparse
from collections import Counter, defaultdict
from contextlib import closing
import csv
from datetime import datetime, timezone
import json
import platform
from pathlib import Path
import sqlite3
from statistics import median
import tempfile
from time import perf_counter_ns

from model import ROOT, canonical, design, load_json, run_local, text_digest
from oracle import effects, verify_observation
from prepare import pair_row, write_csv
from storage import (AddressResolver, PROBES, REGIMES, VIEWS, evaluate, load_view, open_db,
                     project, reconstruct_fragment, save)
from transactions import exercise

JUDGMENT_COLUMNS = ("id", "pair_id", "layer", "type", "primary", "regime", "view", "probe", "expected",
                    "actual", "status", "old_run", "new_run")
COST_COLUMNS = ("id", "object_id", "pair_id", "regime", "view", "cache", "trial", "elapsed_ns",
                "sqlite_before_bytes", "sqlite_bytes", "sqlite_increment_bytes", "stored_payload_bytes",
                "cache_start_bytes", "cache_end_bytes", "resolver_calls", "origin_requests", "origin_misses",
                "origin_response_bytes", "origin_file_reads", "origin_file_read_bytes", "cache_reads",
                "cache_read_bytes", "sqlite_rows_read", "sqlite_payload_read_bytes", "editorial_http_calls")
SCORE_COLUMNS = ("layer", "type", "regime", "view", "probe", "n", "correct", "wrong", "defer",
                 "true_n", "false_n", "false_negative", "false_positive", "held_true", "held_false")
COST_METRICS = ("elapsed_ns", "sqlite_before_bytes", "sqlite_bytes", "sqlite_increment_bytes",
                "stored_payload_bytes", "cache_start_bytes", "cache_end_bytes", "resolver_calls",
                "origin_requests", "origin_misses", "origin_response_bytes", "origin_file_reads",
                "origin_file_read_bytes", "cache_reads", "cache_read_bytes", "sqlite_rows_read",
                "sqlite_payload_read_bytes", "editorial_http_calls")


def write_jsonl(file, rows):
    with file.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(canonical(row) + "\n")


def write_json(file, document):
    file.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def public_request(spec):
    keys = ["domain", "anchor" if spec["domain"] == "A" else "window"]
    return {key: spec[key] for key in keys}


def probe_truth(domain, predicate, role):
    allowed = {
        "declared": {"body", "context", "registered"},
        "opened": {"body", "context"},
        "read": {"body", "context", "ignored_note"},
        "parsed": {"body", "context"},
        "selected": {"body", "context"},
        "value_contributor": {"body", "context"} if domain == "B" else {"body"},
    }
    return role in allowed[predicate]


def recorded(value):
    if value is None:
        return "defer"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return "result@" + text_digest(value)


def compare(pair, before, after, gold, directories, work):
    request = public_request(pair.spec)
    old_value, new_value = gold[0][0], gold[1][0]
    expected = {"redisplay": old_value, "old_recompute": old_value, "current": new_value,
                "recheck_answer": pair.expected[0], "recheck_reason": pair.expected[1],
                "recheck_link": pair.expected[2]}
    for predicate, roles in PROBES.items():
        expected.update({f"{predicate}:{role}": probe_truth(pair.spec["domain"], predicate, role)
                         for role in roles})
    for view in VIEWS:
        file = work / f"{pair.id}-{view}.sqlite"
        with closing(open_db(file)) as db:
            record, fragments = project(view, pair.spec, pair.before, before)
            if view == "A0":
                assert set(record) == {"address", "reason"} and not fragments
            if view == "A1":
                assert set(record) == {"address", "reason", "tag", "manifest", "snapshot", "output_sha256"}
                assert not fragments
            save(db, "comparison:" + pair.id, pair.before, before, record, fragments)
            for regime in REGIMES:
                resolver = AddressResolver(pair, regime, directories)
                saved, pieces = load_view(db, before["id"], resolver.metrics)
                actual, rationale = evaluate(request, view, saved, pieces, pair.after.address, resolver)
                assert 1 <= resolver.metrics["resolver_calls"] <= 2
                assert (regime != "lost" or view == "A2" or actual["old_recompute"] is None)
                ident = f"{pair.id}/{regime}/{view}"
                trace = {"id": "VIEW:" + ident, "event": "view_evaluation", "pair_id": pair.id,
                         "view": view, "regime": regime, "old_run": before["id"], "current_run": after["id"],
                         "redisplay": recorded(actual["redisplay"]), "old_recompute": recorded(actual["old_recompute"]),
                         "current": recorded(actual["current"]), "recompute_rationale": rationale,
                         "metrics": dict(resolver.metrics)}
                rows = []
                for probe, truth in expected.items():
                    claim = actual[probe]
                    verdict = "defer" if claim is None else ("correct" if claim == truth else "wrong")
                    rows.append((ident + "/" + probe, pair.id, pair.spec["domain"], pair.type, int(pair.main),
                                 regime, view, probe, recorded(truth), recorded(claim), verdict, before["id"],
                                 after["id"]))
                yield trace, rows


def observed(pair, directories):
    receipts, truths = [], []
    for edge, edition in (("before", pair.before), ("after", pair.after)):
        run = run_local(pair.spec, edition, directories[edition.id], pair.id + ":" + edge)
        truths.append(verify_observation(pair.spec, edition, run))
        run.update(event="instrumented", pair_id=pair.id, edge=edge, object_id=edition.object_id,
                   layer=pair.spec["domain"], version=edition.id, declared=edition.paths,
                   synthetic=edition.synthetic, value_sha256=text_digest(run["value"]),
                   observed_utc=datetime.now(timezone.utc).isoformat())
        receipts.append(run)
    before, after = receipts
    changes = effects(pair.before, pair.after, *truths, before, after)
    assert changes == pair.expected, (pair.id, changes, pair.expected)
    observation = {"id": "DIFF:" + pair.id, "event": "paired_oracle_check", "pair_id": pair.id,
                   "before": before["id"], "after": after["id"], "primary": pair.main, "old_grade": "D3",
                   "new_grade": "D3", "observed_changes": list(changes), "expected_changes": list(pair.expected)}
    return before, after, observation, truths


def missing_fragment(pair, run, directory):
    record, pieces = project("A2", pair.spec, pair.before, run)
    file = directory / "loss.sqlite"
    with closing(open_db(file)) as db:
        save(db, "loss-probe", pair.before, run, record, pieces)
        db.execute("DELETE FROM fragments WHERE run=? AND ordinal=0", (run["id"],))
    with closing(open_db(file)) as db:
        saved, partial = load_view(db, run["id"], Counter())
    rebuilt, rationale = reconstruct_fragment(public_request(pair.spec), saved, partial)
    assert rebuilt is None and saved["snapshot"] == run["value"]
    return {"id": "LOSS01", "event": "fragment_loss_control", "pair_id": pair.id, "old_run": run["id"],
            "retention": "lost", "loss": "one stored fragment deleted from isolated database",
            "fragments_before": len(pieces), "fragments_after": len(partial), "snapshot_preserved": True,
            "old_recompute": "defer", "rationale": rationale}


def total_files(directory):
    return sum(path.stat().st_size for path in directory.iterdir() if path.is_file())


def cost_trial(pair, before, directories, root, regime, view, cache_condition, trial):
    request = public_request(pair.spec)
    key = f"C-{pair.spec['id']}-{regime}-{view}-{cache_condition}-{trial}"
    work = root / key
    work.mkdir()
    assert not list(work.iterdir())
    cache = work / "cache"
    cache.mkdir()
    record, pieces = project(view, pair.spec, pair.before, before)
    if cache_condition == "warm":
        warm = AddressResolver(pair, regime, directories, cache)
        evaluate(request, view, record, pieces, pair.after.address, warm)
        assert list(cache.iterdir())
    cached_before = total_files(cache)
    file = work / "trial.sqlite"
    started = perf_counter_ns()
    resolver = AddressResolver(pair, regime, directories, cache)
    with closing(open_db(file)) as db:
        sqlite_before = file.stat().st_size
        _, stored_bytes = save(db, "cost:" + key, pair.before, before, record, pieces)
        saved, parts = load_view(db, before["id"], resolver.metrics)
        result, _ = evaluate(request, view, saved, parts, pair.after.address, resolver)
        assert result["current"] is not None
    elapsed = perf_counter_ns() - started
    sqlite_bytes = file.stat().st_size
    m = resolver.metrics
    return (key, pair.spec["id"], pair.id, regime, view, cache_condition, trial, elapsed,
            sqlite_before, sqlite_bytes, sqlite_bytes - sqlite_before, stored_bytes, cached_before,
            total_files(cache), m["resolver_calls"], m["origin_requests"], m["origin_misses"],
            m["origin_response_bytes"], m["origin_file_reads"], m["origin_file_read_bytes"],
            m["cache_reads"], m["cache_read_bytes"], m["sqlite_rows_read"], m["sqlite_payload_read_bytes"], 0)


def aggregate(judgments, costs):
    verdicts = defaultdict(Counter)
    for row in map(lambda fields: dict(zip(JUDGMENT_COLUMNS, fields, strict=True)), judgments):
        if not row["primary"]:
            continue
        key = tuple(row[field] for field in ("layer", "type", "regime", "view", "probe"))
        counts = verdicts[key]
        counts["n"] += 1
        counts[row["status"]] += 1
        yes = row["expected"] == "yes"
        no = row["expected"] == "no"
        counts["true_n"] += yes
        counts["false_n"] += no
        counts["false_negative"] += yes and row["actual"] == "no"
        counts["false_positive"] += no and row["actual"] == "yes"
        counts["held_true"] += yes and row["actual"] == "defer"
        counts["held_false"] += no and row["actual"] == "defer"
    scores = []
    for key, groups in sorted(verdicts.items()):
        numeric = [groups[field] for field in SCORE_COLUMNS[5:9]]
        boolean = [groups[field] for field in SCORE_COLUMNS[9:]] if groups["true_n"] or groups["false_n"] else [""] * 6
        scores.append((*key, *numeric, *boolean))

    measured = defaultdict(list)
    for row in map(lambda fields: dict(zip(COST_COLUMNS, fields, strict=True)), costs):
        for identity in (row["object_id"], "all"):
            for metric in COST_METRICS:
                key = (identity, row["regime"], row["view"], row["cache"], metric)
                measured[key].append(row[metric])
    cost_summary = [(*key, len(values), min(values), median(values), max(values), sum(values))
                    for key, values in sorted(measured.items())]
    return scores, cost_summary


def run_all(out, work):
    specs = load_json(ROOT / "inputs" / "objects.json")
    cases = list(design(specs))
    with (ROOT / "pairs.csv").open(newline="", encoding="utf-8") as stream:
        sealed = list(csv.reader(stream))[1:]
    assert sealed == [[str(item) for item in pair_row(pair)] for pair in cases]
    versions = {e.id: e for pair in cases for e in (pair.before, pair.after)}
    directories = {eid: edition.materialize(work / "origin") for eid, edition in versions.items()}
    work_views = work / "views"
    work_views.mkdir()
    history, judgments, costs = [], [], []
    reference = {}
    for pair in sorted(cases, key=lambda p: (p.spec["id"].endswith("4"), p.id)):
        old, new, checked, gold = observed(pair, directories)
        history.extend((old, new, checked))
        for trace, rows in compare(pair, old, new, gold, directories, work_views):
            history.append(trace)
            judgments.extend(rows)
        if pair.main and pair.spec["id"] not in reference:
            reference[pair.spec["id"]] = pair, old

    selected, run = reference["A1"]
    history.append(missing_fragment(selected, run, work))
    tx = exercise(work / "transactions")
    history.extend({"event": "transaction_trial", **trial} for trial in tx["trials"])

    cost_root = work / "costs"
    cost_root.mkdir()
    for object_id, (pair, before) in sorted(reference.items()):
        for regime in REGIMES:
            for view in VIEWS:
                for trial in range(1, 4):
                    order = ("cold", "warm") if trial % 2 else ("warm", "cold")
                    costs.extend(cost_trial(pair, before, directories, cost_root, regime, view, state, trial)
                                 for state in order)

    scores, cost_summary = aggregate(judgments, costs)
    write_jsonl(out / "runs.jsonl", history)
    write_csv(out / "judgments.csv", JUDGMENT_COLUMNS, judgments)
    write_csv(out / "costs.csv", COST_COLUMNS, costs)
    write_csv(out / "scores.csv", SCORE_COLUMNS, scores)
    write_csv(out / "cost-summary.csv", ("object_id", "regime", "view", "cache", "metric", "n", "min",
                                        "median", "max", "sum"), cost_summary)
    write_json(out / "evidence" / "transactions.json", tx)
    write_json(out / "evidence" / "run-environment.json",
               {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version,
                "machine": platform.machine(), "system": platform.system(), "kernel": platform.release(),
                "timing": "perf_counter_ns, app-cold and resolver-cache-warm; OS cache not flushed",
                "external_origin": "local simulation only; no network calls by experiment",
                "primary_pairs": sum(pair.main for pair in cases), "secondary_pairs": sum(not pair.main for pair in cases),
                "cost_samples": len(costs), "judgment_rows": len(judgments), "run_rows": len(history),
                "holdout_first_run": {key: next(row["id"] for row in history if row.get("object_id") == key)
                                      for key in ("A4", "B4")}})
    print(f"{len(cases)} paired changes, {len(history)} run events, "
          f"{len(judgments)} judgments, {len(costs)} cost trials, {len(tx['trials'])} transaction trials")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    options = parser.parse_args()
    options.out.mkdir(parents=True, exist_ok=True)
    (options.out / "evidence").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="af071-run-") as temporary:
        run_all(options.out.resolve(), Path(temporary))
