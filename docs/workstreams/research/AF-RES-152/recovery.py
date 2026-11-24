"""Replay quota, Retry-After, a missing page and durable alias history."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
SCHEMA = """
CREATE TABLE IF NOT EXISTS inbox (seq INTEGER PRIMARY KEY, payload TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS applied (seq INTEGER PRIMARY KEY, item TEXT, url TEXT, version TEXT, state TEXT);
CREATE TABLE IF NOT EXISTS cursor (
    id INTEGER PRIMARY KEY CHECK (id = 1), high INTEGER, next_read INTEGER, epoch INTEGER, calls INTEGER
);
INSERT OR IGNORE INTO cursor VALUES (1, 0, 0, -1, 0);
"""


class Interrupted(Exception):
    """The constructed worker terminates before committing a transaction."""


def encode(row):
    return json.dumps(row, sort_keys=True, separators=(",", ":"))


def send(rows, now, at, high, held):
    if now == 4:
        return 429, []
    if 4 < now < at:
        return 503, []
    if high == 2 and not held:
        return 200, [rows[4]]
    if high == 2:
        return 200, [rows[n] for n in (3, 4, 4)]
    if high == 4:
        return 200, [rows[n] for n in (4, 5, 6) if rows[n]["known"] <= now]
    if high >= 6:
        return 200, [rows[n] for n in (3, 4, 5, 6)]
    return 200, [row for seq, row in rows.items() if seq > high and row["known"] <= now]


def write_records(db, received, cursor):
    inserted, applied = 0, 0
    for row in received:
        payload = encode(row)
        prior = db.execute("SELECT payload FROM inbox WHERE seq=?", (row["seq"],)).fetchone()
        if prior is None:
            db.execute("INSERT INTO inbox VALUES (?, ?)", (row["seq"], payload))
            inserted += 1
        elif prior[0] != payload:
            raise ValueError(f"Conflicting sequence {row['seq']}")
    while item := db.execute("SELECT payload FROM inbox WHERE seq=?", (cursor+1,)).fetchone():
        row = json.loads(item[0])
        db.execute("INSERT INTO applied VALUES (:seq, :item, :url, :version, :state)", row)
        applied += 1
        cursor += 1
    return cursor, inserted, applied


def paths(db):
    records = list(db.execute("SELECT seq, item, url, version, state FROM applied ORDER BY seq"))
    latest = {}
    for seq, item, url, version, state in records:
        if state == "replacement":
            for prior in latest.values():
                if prior["item"] == item and prior["url"] != url:
                    prior.update(state="moved", to=url)
        latest[url] = dict(seq=seq, item=item, url=url, version=version, state=state)
    return latest


def simulate(path, fixture, recovery_hour, interrupt):
    rows = {r["seq"]: r for r in fixture["records"]}
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    journey = []
    interrupted_at = None
    for now in range(fixture["end_hour"]):
        high, next_read, last_epoch, calls = db.execute(
            "SELECT high, next_read, epoch, calls FROM cursor").fetchone()
        epoch = now // fixture["quota_window_hours"]
        if epoch != last_epoch:
            calls = 0
        if now < next_read:
            journey.append(dict(hour=now, response="wait", high=high))
            continue
        if calls >= fixture["quota_calls"]:
            journey.append(dict(hour=now, response="quota", high=high))
            continue
        held = db.execute("SELECT 1 FROM inbox WHERE seq=4").fetchone()
        status, received = send(rows, now, recovery_hour, high, held)
        resume_at = now + fixture["retry_after_hours"] if status in (429, 503) else now + 1
        try:
            with db:
                cursor, inserted, applied = write_records(db, received, high)
                db.execute("UPDATE cursor SET high=?, next_read=?, epoch=?, calls=?",
                           (cursor, resume_at, epoch, calls+1))
                should_stop = interrupt and interrupted_at is None and high == 2 and cursor > 2
                if should_stop:
                    raise Interrupted()
        except Interrupted:
            db.close()
            db = sqlite3.connect(path)
            restored = db.execute("SELECT high, calls FROM cursor").fetchone()
            assert restored == (high, calls)
            interrupted_at = now
            # Replay the exact buffered response after losing the uncommitted writes.
            with db:
                cursor, inserted, applied = write_records(db, received, high)
                db.execute("UPDATE cursor SET high=?, next_read=?, epoch=?, calls=?",
                           (cursor, resume_at, epoch, calls+1))
        journey.append(dict(hour=now, response=status, high=cursor, inputs=[r["seq"] for r in received],
                            document_writes=applied, inbox_writes=inserted, paths=paths(db)))
    final = dict(cursor=db.execute("SELECT high, next_read, epoch, calls FROM cursor").fetchone(),
                 rows=list(db.execute("SELECT * FROM applied ORDER BY seq")), links=paths(db))
    db.close()
    return dict(history=journey, final=final, interrupted_at=interrupted_at)


def run(fixture, out):
    with TemporaryDirectory(prefix="af152-recovery-") as tmp:
        records = []
        for recovery_hour in fixture["recovery_hours"]:
            once = simulate(Path(tmp)/f"{recovery_hour}-once.sqlite", fixture, recovery_hour, False)
            resumed = simulate(Path(tmp)/f"{recovery_hour}-resume.sqlite", fixture, recovery_hour, True)
            assert once["history"] == resumed["history"] and once["final"] == resumed["final"]
            assert resumed["final"]["cursor"][0] == len(fixture["records"])
            assert resumed["interrupted_at"] is not None
            accepted = [h for h in once["history"] if h["response"] == 200]
            duplicates = [h for h in accepted if h["high"] == 6 and h["document_writes"] == 0]
            assert duplicates and all(h["inbox_writes"] == 0 for h in duplicates)
            old = fixture["records"][0]["url"]
            assert any(h["paths"].get(old, {}).get("state") == "moved" for h in accepted)
            assert any(h["paths"].get(old, {}).get("to") == fixture["records"][3]["url"] for h in accepted)
            assert once["final"]["links"][old]["state"] == "archived"
            assert once["final"]["links"][old]["version"] == "v1"
            by_status = Counter(str(s["response"]) for s in once["history"])
            records.append(dict(recovery_hour=recovery_hour,
                                gap_filled_hour=next(h["hour"] for h in accepted if h["high"] >= 4),
                                first_contiguous_recovery_hour=next(h["hour"] for h in accepted if h["high"] == 6),
                                response_counts=by_status, duplicate_rounds=len(duplicates),
                                productive_writes=sum(h["document_writes"] for h in accepted),
                                interrupted_at=resumed["interrupted_at"], final_equal=True, result=once))
    out.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "control-input.json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run(json.loads(args.input.read_text()), args.out)


if __name__ == "__main__":
    main()
