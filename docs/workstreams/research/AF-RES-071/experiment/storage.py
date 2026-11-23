"""Three isolated storage projections and a single test address resolver."""
from collections import Counter
from contextlib import closing
import json
import os
import sqlite3

from model import (BASIS, BUDGET_BYTES, BUDGET_REQUESTS, IncompleteEvidence, TRANSFORM,
                   canonical, digest, link_key, run_package, solve, text_digest)

VIEWS = ("A0", "A1", "A2")
REGIMES = ("retained", "lost")
PROBES = {
    "declared": ("body", "context", "registered", "unlisted"),
    "opened": ("body", "context", "registered", "unlisted"),
    "read": ("body", "context", "registered", "ignored_note"),
    "parsed": ("body", "context", "registered", "ignored_note"),
    "selected": ("body", "context", "registered", "ignored_note"),
    "value_contributor": ("body", "context", "registered", "ignored_note"),
}


def manifest(edition):
    return {role: {"path": edition.paths[role], "sha256": digest(raw)}
            for role, raw in edition.files.items()}


def project(view, spec, edition, run):
    record = {"address": edition.address,
              "reason": {"condition": BASIS[spec["domain"]], "held": run["value"]["reason_holds"]}}
    fragments = []
    if view != "A0":
        record.update(tag=edition.tag, manifest=manifest(edition), snapshot=run["value"],
                      output_sha256=text_digest(run["value"]))
    if view == "A2":
        fragments = [row for role in run["order"] for row in run["parsed"][role]]
        receipt_trace = [{key: val for key, val in event.items() if key != "returned_hex"}
                         for event in run["trace"]]
        record["receipt"] = {"run": run["id"], "transform": run["transform"],
                             "order": run["order"], "policy": run["policy"],
                             "trace": receipt_trace, "discarded": run["discarded"], "guards": run["guards"], "cells": run["cells"],
                             "fragment_count": len(fragments), "fragments_sha256": text_digest(fragments)}
    return record, fragments


SCHEMA = """
CREATE TABLE IF NOT EXISTS operations (
    op TEXT PRIMARY KEY, fingerprint TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS answers (
    run TEXT PRIMARY KEY, op TEXT NOT NULL UNIQUE REFERENCES operations(op),
    object TEXT NOT NULL, edition TEXT NOT NULL, record BLOB NOT NULL);
CREATE INDEX IF NOT EXISTS answers_object ON answers(object);
CREATE TABLE IF NOT EXISTS current_answer (
    object TEXT PRIMARY KEY, run TEXT NOT NULL REFERENCES answers(run));
CREATE TABLE IF NOT EXISTS fragments (
    run TEXT NOT NULL REFERENCES answers(run), ordinal INTEGER NOT NULL,
    data BLOB NOT NULL, PRIMARY KEY(run, ordinal));
"""


def open_db(file):
    db = sqlite3.connect(file, isolation_level=None)
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA journal_mode=DELETE")
    db.execute("PRAGMA synchronous=FULL")
    db.executescript(SCHEMA)
    return db


class InjectedFailure(RuntimeError):
    pass


class OperationConflict(ValueError):
    pass


def save(db, op, edition, run, record, fragments, fault=None):
    encoded = canonical(record).encode()
    pieces = [canonical(fragment).encode() for fragment in fragments]
    fingerprint = text_digest([edition.id, edition.tag, edition.address, manifest(edition),
                               run["value"], run["policy"], run["order"]])
    if fault == "crash":
        db.execute("PRAGMA cache_size=1")
    db.execute("BEGIN IMMEDIATE")
    try:
        prior = db.execute("SELECT fingerprint FROM operations WHERE op=?", (op,)).fetchone()
        if prior:
            if prior[0] != fingerprint:
                raise OperationConflict("operation key reused with different arguments")
            db.rollback()
            return "duplicate", len(encoded) + sum(map(len, pieces))
        db.execute("INSERT INTO operations VALUES(?, ?)", (op, fingerprint))
        db.execute("INSERT INTO answers VALUES(?, ?, ?, ?, ?)",
                   (run["id"], op, edition.object_id, edition.id, encoded))
        db.executemany("INSERT INTO fragments VALUES(?, ?, ?)",
                       ((run["id"], index, blob) for index, blob in enumerate(pieces)))
        db.execute("INSERT INTO current_answer VALUES(?, ?) ON CONFLICT(object) DO UPDATE SET run=excluded.run",
                   (edition.object_id, run["id"]))
        if fault == "exception":
            raise InjectedFailure("after history, fragments and current pointer, before commit")
        if fault == "crash":
            print(canonical({"phase": "before_commit", "in_transaction": db.in_transaction,
                             "run": run["id"], "pending_fragments": len(pieces)}), flush=True)
            os._exit(73)
        db.commit()
    except BaseException:
        db.rollback()
        raise
    return "inserted", len(encoded) + sum(map(len, pieces))


def load_view(db, run_id, metrics):
    encoded, = db.execute("SELECT record FROM answers WHERE run=?", (run_id,)).fetchone()
    metrics["sqlite_rows_read"] += 1
    metrics["sqlite_payload_read_bytes"] += len(encoded)
    record = json.loads(encoded)
    pieces = []
    if "receipt" in record:
        for blob, in db.execute("SELECT data FROM fragments WHERE run=? ORDER BY ordinal", (run_id,)):
            pieces.append(json.loads(blob))
            metrics["sqlite_rows_read"] += 1
            metrics["sqlite_payload_read_bytes"] += len(blob)
    return record, pieces


class AddressResolver:
    """A scoped simulation. Only public GET routes are passed to a view."""

    def __init__(self, pair, regime, directories, cache=None):
        self.old = pair.before
        self.new = pair.after
        self.regime = regime
        self.directories = directories
        self.public_recipe = pair.old_recipe_public
        self.cache = cache
        self.metrics = Counter()

    def resolve(self, mode, address, ref=None):
        counts = self.metrics
        if counts["resolver_calls"] >= BUDGET_REQUESTS:
            return None
        counts["resolver_calls"] += 1
        old = mode == "historical"
        edition = self.old if old else self.new
        reachable = address == edition.address
        if old:
            reachable = reachable and self.regime == "retained" and (
                ref == edition.tag or (ref is None and address != self.new.address))
        recipe = not old or self.public_recipe
        cache_key = text_digest([mode, address, ref, edition.id, self.regime, reachable, recipe])
        path = self.cache / cache_key if self.cache else None
        if path and path.exists():
            wire = path.read_bytes()
            counts["cache_reads"] += 1
            counts["cache_read_bytes"] += len(wire)
        else:
            counts["origin_requests"] += 1
            if not reachable:
                counts["origin_misses"] += 1
                return None
            files = {}
            for role, asset in edition.paths.items():
                raw = (self.directories[edition.id] / asset).read_bytes()
                counts["origin_file_reads"] += 1
                counts["origin_file_read_bytes"] += len(raw)
                files[role] = raw.decode()
            package = {"address": edition.address, "tag": edition.tag, "files": files,
                       "paths": edition.paths, "immutable_history": old,
                       "order": edition.order if recipe else None,
                       "policy": edition.policy if recipe else None,
                       "config_changed_notice": (self.old.order != self.new.order
                                                 or self.old.policy != self.new.policy)}
            wire = canonical(package).encode()
            counts["origin_response_bytes"] += len(wire)
            if path:
                path.write_bytes(wire)
                counts["cache_written_bytes"] += len(wire)
        if counts["returned_bytes"] + len(wire) > BUDGET_BYTES:
            counts["budget_rejections"] += 1
            return None
        counts["returned_bytes"] += len(wire)
        return json.loads(wire)


def reconstruct_fragment(request, record, pieces):
    receipt = record["receipt"]
    if (receipt["transform"] != TRANSFORM or len(pieces) != receipt["fragment_count"]
            or text_digest(pieces) != receipt["fragments_sha256"]):
        return None, "incomplete or unrecognized fragment recipe"
    parsed = {role: [row for row in pieces if row["role"] == role] for role in receipt["order"]}
    try:
        rebuilt, _, _ = solve(request, parsed, receipt["policy"])
    except IncompleteEvidence as error:
        return None, str(error)
    return rebuilt, "stored same-run fragment replay"


def reconstruct_archive(request, record, resolver):
    package = resolver.resolve("historical", record["address"], record.get("tag"))
    if package is None or not package["immutable_history"]:
        return None, "historical address or publisher tag unavailable"
    if "manifest" in record:
        files = {role: {"path": package["paths"][role], "sha256": digest(s.encode())}
                 for role, s in package["files"].items()}
        if files != record["manifest"]:
            return None, "archive fingerprint mismatch"
    if package["policy"] is None:
        return None, "historical transform settings unavailable"
    return run_package(request, package)["value"], "independent resolver replay"


def usage(record, pieces, predicate, role):
    if predicate == "declared":
        return role in record["manifest"] if "manifest" in record else None
    if "receipt" not in record:
        return None
    receipt = record["receipt"]
    if predicate == "opened":
        return any(event["event"] == "open" and event["role"] == role for event in receipt["trace"])
    if predicate == "read":
        if role == "ignored_note":
            return any(row["kind"] == role for row in receipt["discarded"])
        return any(event["event"] == "read" and event["role"] == role and event["end"] > event["start"]
                   for event in receipt["trace"])
    if predicate == "parsed":
        return any(row["role"] == role for row in pieces)
    contributors = [cell["input"] for cell in receipt["cells"]]
    if predicate == "selected":
        contributors += list(receipt["guards"].values())
    return any(row["role"] == role for row in contributors)


def evaluate(request, view, record, pieces, current_address, resolver):
    shown = record.get("snapshot")
    if view == "A2":
        historical, rationale = reconstruct_fragment(request, record, pieces)
    else:
        historical, rationale = reconstruct_archive(request, record, resolver)
    package = resolver.resolve("current", current_address)
    now = run_package(request, package) if package else None
    recheck_answer = None
    recheck_link = None
    recheck_reason = None
    if now:
        recheck_reason = record["reason"]["held"] != now["value"]["reason_holds"]
        if view == "A0":
            recheck_answer = recheck_reason
            recheck_link = record["address"] != current_address
        else:
            recheck_answer = shown != now["value"]
            if view == "A1":
                manifest_now = {role: {"path": package["paths"][role], "sha256": digest(raw.encode())}
                                for role, raw in package["files"].items()}
                recheck_link = (record["address"] != current_address or record["manifest"] != manifest_now
                                or package["config_changed_notice"])
            else:
                recheck_link = link_key(record["address"], record["receipt"]["cells"]) != link_key(
                    current_address, now["cells"])
    decisions = {"redisplay": shown, "old_recompute": historical, "current": now["value"] if now else None,
                 "recheck_answer": recheck_answer, "recheck_reason": recheck_reason, "recheck_link": recheck_link}
    for predicate, roles in PROBES.items():
        decisions.update({f"{predicate}:{role}": usage(record, pieces, predicate, role) for role in roles})
    return decisions, rationale


def reopen_snapshot(file, object_id):
    with closing(open_db(file)) as db:
        rows = db.execute("SELECT run, edition, record FROM answers WHERE object=? ORDER BY rowid",
                          (object_id,)).fetchall()
        active = db.execute("SELECT run FROM current_answer WHERE object=?", (object_id,)).fetchone()
        return {"old_answers": [{"run": run, "edition": edition, "snapshot": json.loads(record)["snapshot"]}
                                for run, edition, record in rows],
                "active": active[0] if active else None,
                "counts": {table: db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                           for table in ("operations", "answers", "current_answer", "fragments")},
                "integrity": db.execute("PRAGMA integrity_check").fetchone()[0],
                "foreign_key_errors": db.execute("PRAGMA foreign_key_check").fetchall(),
                "orphan_fragments": db.execute(
                    "SELECT count(*) FROM fragments f LEFT JOIN answers a USING(run) WHERE a.run IS NULL"
                ).fetchone()[0]}
