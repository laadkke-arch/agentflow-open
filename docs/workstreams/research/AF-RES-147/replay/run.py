"""Run isolated SQLite stores against materialized sources; produce ungraded observations."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import time

from events import ROOT, all_events, encoded
from provider import Provider
from store import MASKS, Store


def run(prepared, database, events, design, policy, mask, phase):
    provider = Provider(prepared)
    start = time.perf_counter_ns()
    store = Store(database, design, policy, provider, mask)
    setup_ns = time.perf_counter_ns() - start
    trace = []
    registration = None
    start = time.perf_counter_ns()
    try:
        for e in events:
            before = (store.sql_lookups, len(provider.calls), len(provider.reads), store.db.total_changes)
            then = time.perf_counter_ns()
            with store.db:
                answer = store.step(e)
            lapse = time.perf_counter_ns() - then
            if e["action"] == "register" and registration is None:
                registration = {**store.summary(), "file_bytes": database.stat().st_size}
            sql, calls, reads, written = before
            trace.append({
                "id": e["id"], "answer": answer, "transition": store.transition,
                "fetched": store.last_fetch, "sql_lookups": store.sql_lookups - sql,
                "acquire_calls": len(provider.calls) - calls, "reads": provider.reads[reads:],
                "sqlite_changes": store.db.total_changes - written, "wall_ns": lapse,
            })
        wall_ns = time.perf_counter_ns() - start
        db = store.summary()
        for table in store.tables:
            if (store.db.execute("PRAGMA foreign_key_check(" + table + ")").fetchone()):
                raise ValueError(f"foreign key integrity failed: {table}")
        db["integrity"] = store.db.execute("PRAGMA integrity_check").fetchone()[0]
        if db["integrity"] != "ok":
            raise ValueError(db["integrity"])
    finally:
        store.db.close()
    file_bytes = database.stat().st_size
    return {
        "sequence": events[0]["sequence"], "design": design, "policy": policy,
        "mask": mask, "phase": phase, "setup_ns": setup_ns, "wall_ns": wall_ns,
        "db": {**db, "file_bytes": file_bytes}, "first_registration": registration,
        "lookups": store.sql_lookups, "observations_inserted": store.inserts, "trace": trace,
    }


def plan():
    for design in ("A", "B", "C"):
        for policy in ("off", "retry", "ttl"):
            yield design, policy, None
    yield "A-url", "retry", None
    for mask in MASKS:
        yield "C", "ttl", mask


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--prepared", type=Path, required=True)
    cli.add_argument("--scratch", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--sequence", choices=["dense", "sparse", "control", "reversed"], action="append")
    args = cli.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=False)
    frozen = (ROOT / "events.jsonl").read_bytes()
    regenerated = "".join(encoded(e) + "\n" for e in all_events()).encode()
    if frozen != regenerated:
        raise ValueError("events JSONL differs from committed generator and inputs")
    selected = args.sequence or ["dense", "sparse", "control", "reversed"]
    groups = defaultdict(list)
    for raw_line in frozen.splitlines():
        event = json.loads(raw_line)
        if event["sequence"] in selected:
            groups[event["sequence"]].append(event)

    runs = []
    for sequence, events in groups.items():
        for design, policy, mask in plan():
            database = args.scratch / f'{sequence}-{design}-{policy}-{mask or "full"}.sqlite'
            for phase in ("first", "retained"):
                runs.append(run(args.prepared, database, events, design, policy, mask, phase))
    receipt = {
        "events_sha256": hashlib.sha256(frozen).hexdigest(),
        "env": {"python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version,
                "sqlite_journal": "DELETE", "sqlite_synchronous": "FULL"},
        "runs": runs,
    }
    args.output.write_text(encoded(receipt) + "\n", encoding="utf-8")
    print(f'{len(runs)} batch runs and {sum(len(r["trace"]) for r in runs)} events')


if __name__ == "__main__":
    main()
