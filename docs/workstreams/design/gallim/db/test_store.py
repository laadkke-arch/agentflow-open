"""Local, persisted-data tests. No project code or external services are invoked."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import hashlib
import sqlite3
import unittest

from store import Ledger

# The published package places the evaluator beside store.py.
from demo import evaluate


TEXT = "원래 위치 유지. 내용 색인."
CRITERIA = [
    dict(id="keep", label="원래 위치 유지", required=True, start_char=0, end_char=8),
    dict(id="index", label="내용 색인", required=False, start_char=10, end_char=15),
]


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "ledger.db"
        self.db = Ledger(self.path)
        self.addCleanup(self.db.conn.close)
        db = self.db
        db.add_request("r", "r1", TEXT, CRITERIA)
        db.add_resource("device", "문서 처리기", "fixture")
        db.add_edition("e", "device", "1")
        db.add_context("direct", "r1", "e", "single file", "input=only copy")
        db.add_context("staged", "r1", "e", "single file", "input=separate copy")
        db.add_document("d", "cases.json", "Fixture, synthetic observations")
        db.add_source("d", "v1", "원본 삭제. 색인 성공.", "complete synthetic observation")
        db.add_fragment("delete", "d", "v1", 0, 5, "cases.json#/records/delete")
        db.add_claim("refute", "direct", "direct", "keep", "direct", "refute", "delete", "원본 삭제")

    def publish(self, context="direct", key="p", **options):
        return self.db.publish_decision(context, key, evaluate, "1", **options)

    def test_spans_hashes_and_immutable_requests(self):
        row = self.db.conn.execute("SELECT * FROM source_fragment").fetchone()
        self.assertEqual(row["sha256"], hashlib.sha256("원본 삭제".encode()).hexdigest())
        self.db.add_request("r", "r1", TEXT, list(reversed(CRITERIA)))
        with self.assertRaises(ValueError):
            self.db.add_request("r", "r1", TEXT, CRITERIA[:1])
        self.db.add_request("r", "r2", TEXT, CRITERIA[:1], previous_id="r1")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.conn.execute("UPDATE request_revision SET original_text='new' WHERE id='r1'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add_request("new", "self", TEXT, CRITERIA, "self")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add_source("d", "self", "self-loop", "fixture", "self")
        with self.assertRaises(ValueError):
            self.db.add_fragment("bad", "d", "v1", 0, 100, "cases.json#/records/oob")
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.add_document("doc", None, "no URL")

    def test_reused_display_name_does_not_cross_resource_scope(self):
        db = self.db
        db.add_resource("other", "문서 처리기", "another product")
        db.add_edition("other-e", "other", "1")
        db.add_context("other-c", "r1", "other-e", "single file", "input=separate copy")
        db.add_claim("wrong", "staged", "other-c", "keep", "direct", "support", "delete", "other subject")
        run = db.get_decision(self.publish("staged", "s"))
        self.assertEqual(run["status"], "pending")
        self.assertIn("subject", run["output"]["criteria"]["keep"]["ignored"]["wrong"])

    def test_snapshot_idempotency_and_known_cross_scope(self):
        db = self.db
        db.add_claim("wrong-path", "staged", "direct", "keep", "direct", "refute", "delete", "different input")
        db.add_claim("proposal", "staged", "staged", "keep", "proposal", "support", "delete", "copy idea")
        old = self.publish()
        self.assertEqual(self.publish(), old)
        with self.assertRaises(ValueError):
            self.publish("staged", "p")
        self.assertEqual(db.get_decision(old)["status"], "excluded")
        staged = db.get_decision(self.publish("staged", "staged-run"))
        self.assertEqual(staged["request_revision_id"], "r1")
        self.assertEqual(staged["status"], "pending")
        self.assertEqual(set(staged["output"]["criteria"]["keep"]["ignored"]), {"wrong-path","proposal"})
        with self.assertRaises(sqlite3.IntegrityError):
            db.conn.execute("DELETE FROM decision_run WHERE id=?", (old,))

    def test_source_cascade_and_explicit_recheck(self):
        db = self.db
        old = self.publish()
        child = self.publish("staged", "derived", parents=[old])
        grandchild = self.publish("staged", "derived-twice", parents=[child])
        unaffected = self.publish("staged", "standalone")
        db.add_source("d", "v2", "새 자료, 아직 판독 전.", "fixture v2", "v1")
        db.add_source("d", "v2", "새 자료, 아직 판독 전.", "fixture v2", "v1")
        self.assertEqual({j["run_id"] for j in db.pending_jobs()}, {old,child,grandchild})
        self.assertFalse(db.pending_jobs(unaffected))
        self.assertEqual(db.get_decision(old)["status"], "excluded")
        self.assertEqual(db.get_decision(old)["input"]["claims"][0]["source_revision"], "v1")
        job = db.pending_jobs(old)[0]["id"]
        replacement = self.publish("direct", "recheck", resolve_jobs=[job])
        self.assertEqual(self.publish("direct", "recheck", resolve_jobs=[job]), replacement)
        self.assertEqual(db.get_decision(replacement)["status"], "pending")
        self.assertEqual(db.get_decision(replacement)["input"]["claims"], [])
        self.assertFalse(db.pending_jobs(old))
        child_job = db.pending_jobs(child)[0]["id"]
        with self.assertRaisesRegex(ValueError, "retain each parent"):
            self.publish("staged", "missing-parent", resolve_jobs=[child_job])
        recomputed_child = self.publish("staged", "new-child", parents=[replacement], resolve_jobs=[child_job])
        self.assertFalse(db.pending_jobs(child))
        self.assertTrue(db.pending_jobs(grandchild))
        self.assertGreater(recomputed_child, child)
        with self.assertRaises(ValueError):
            self.publish("staged", "stale-parent", parents=[old])
        eligibility = db.conn.execute("SELECT eligibility FROM run_claim WHERE run_id=?",(replacement,)).fetchone()[0]
        self.assertEqual(eligibility, "superseded")
        db.add_fragment("new", "d", "v2", 0, 4, "cases.json#/records/new")
        db.add_claim("explicit-new", "direct", "direct", "keep", "direct", "support", "new", "synthetic support")
        final = self.publish("direct", "with-new-claim")
        self.assertEqual(db.get_decision(final)["status"], "verified")
        self.assertEqual(db.get_decision(replacement)["status"], "pending")

    def test_invalid_publish_rolls_back_all_tables(self):
        def broken(**inputs):
            result = evaluate(**inputs)
            result["criteria"]["index"]["used"] = ["invented"]
            return result
        with self.assertRaises(ValueError):
            self.db.publish_decision("direct", "retry", broken, "v")
        for table in ("decision_run", "decision_item", "run_claim", "recheck_resolution"):
            self.assertEqual(self.db.conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0], 0)
        self.db.publish_decision("direct", "retry", evaluate, "v")

    def test_grouped_ingestion_rolls_back_and_checks_fks(self):
        db = self.db
        with self.assertRaises(KeyError):
            with db.transaction():
                db.add_document("partial", "cases.json", "partial ingest")
                db.add_fragment("unavailable", "partial", "missing", 0, 2, "cases.json#/records/none")
        self.assertIsNone(db.conn.execute("SELECT id FROM source_document WHERE id='partial'").fetchone())
        db.add_request("q", "q1", TEXT, CRITERIA)
        db.add_context("q-c", "q1", "e", "single file", "input=separate copy")
        with self.assertRaises(sqlite3.IntegrityError):
            db.add_claim("mixed", "direct", "q-c", "keep", "direct", "support", "delete", "wrong request")

    def test_concurrent_publish_and_fork(self):
        gate = Barrier(2)
        def publish_once(i):
            with Ledger(self.path) as conn:
                gate.wait(timeout=8)
                return conn.publish_decision("direct", "same", evaluate, "1")
        with ThreadPoolExecutor(2) as pool:
            ids = list(pool.map(publish_once, range(2)))
        self.assertEqual(ids[0], ids[1])
        gate = Barrier(2)
        def competing_revision(i):
            with Ledger(self.path) as conn:
                gate.wait(timeout=8)
                try:
                    conn.add_source("d", f"v2-{i}", str(i), "fixture", "v1")
                    return True
                except sqlite3.IntegrityError:
                    return False
        with ThreadPoolExecutor(2) as pool:
            result = list(pool.map(competing_revision, range(2)))
        self.assertEqual(sorted(result), [False,True])
        self.assertEqual(len(self.db.pending_jobs()), 1)


if __name__ == "__main__":
    unittest.main()
