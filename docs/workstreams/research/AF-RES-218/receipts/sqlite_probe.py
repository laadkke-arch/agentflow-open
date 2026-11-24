"""Exercise the official SQLite visibility examples on two temporary databases."""

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3


def pixel(connection):
    return connection.execute("SELECT value FROM pixels WHERE id=1").fetchone()[0]


def attempt(operation):
    try:
        operation()
    except sqlite3.OperationalError as exc:
        return dict(returned=False, error_code=exc.sqlite_errorcode,
                    error_name=exc.sqlite_errorname, message=str(exc))
    return dict(returned=True)


def case(path, journal):
    with closing(sqlite3.connect(path, timeout=0, isolation_level=None)) as writer:
        mode = writer.execute(f"PRAGMA journal_mode={journal}").fetchone()[0]
        if mode != journal.lower():
            raise RuntimeError(f"journal mode was {mode}, expected {journal}")
        writer.execute("PRAGMA synchronous=FULL")
        sync = writer.execute("PRAGMA synchronous").fetchone()[0]
        writer.executescript("CREATE TABLE pixels(id INTEGER PRIMARY KEY, value REAL); "
                             "INSERT INTO pixels VALUES(1,0.0);")
        seen = dict(case_id=f"SQL-{journal}", database=str(path), sqlite=sqlite3.sqlite_version,
                    journal=mode, synchronous=sync)
        with closing(sqlite3.connect(path, timeout=0, isolation_level=None)) as existing:
            existing.execute("BEGIN")
            seen["existing_before_update"] = pixel(existing)
            writer.execute("BEGIN IMMEDIATE")
            writer.execute("UPDATE pixels SET value=99.0 WHERE id=1")
            seen["writer_after_update"] = pixel(writer)
            seen["existing_after_update_before_commit"] = pixel(existing)
            seen["first_commit_ack"] = attempt(writer.commit)
            seen["writer_transaction_after_first_commit"] = writer.in_transaction
            seen["existing_after_first_commit"] = pixel(existing)
            if journal == "WAL":
                seen["existing_upgrade"] = attempt(
                    lambda: existing.execute("UPDATE pixels SET value=50.0 WHERE id=1")
                )
                with closing(sqlite3.connect(path, timeout=0)) as fresh:
                    seen["fresh_connection_while_old_snapshot_open"] = pixel(fresh)
            existing.rollback()
            if journal == "DELETE":
                seen["retry_commit_ack"] = attempt(writer.commit)
            existing.execute("BEGIN")
            seen["existing_after_restart"] = pixel(existing)
            existing.rollback()
    with closing(sqlite3.connect(path, timeout=0)) as fresh:
        seen["new_connection_after_writer_close"] = pixel(fresh)
    return seen


def main(work):
    work = work.resolve()
    work.mkdir()
    results = [case(work / f"{mode.lower()}.db", mode) for mode in ("WAL", "DELETE")]
    print(json.dumps(results, indent=2))
    wal, rollback = results
    wal_pass = (wal["first_commit_ack"]["returned"]
                and wal["existing_after_first_commit"] == 0.0
                and wal["existing_upgrade"].get("error_name") == "SQLITE_BUSY_SNAPSHOT"
                and wal["fresh_connection_while_old_snapshot_open"] == 99.0)
    rollback_pass = (rollback["first_commit_ack"].get("error_name") == "SQLITE_BUSY"
                     and rollback["writer_transaction_after_first_commit"]
                     and rollback["retry_commit_ack"]["returned"])
    fresh_pass = all(row["existing_after_restart"] == row["new_connection_after_writer_close"] == 99.0
                     for row in results)
    return int(not (wal_pass and rollback_pass and fresh_pass))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    raise SystemExit(main(parser.parse_args().work))
