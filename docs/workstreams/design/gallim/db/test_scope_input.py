import copy
import sqlite3
import tempfile
import unittest
from pathlib import Path

from scope_input import example_scope, ingest_scope, read_scope
from store import Ledger


class ScopeInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "scope.sqlite"
        self.db = Ledger(self.path)
        self.addCleanup(self.db.conn.close)

    def test_partial_scope_round_trip_and_canonical_requirements(self):
        s = example_scope()
        s.update(project_token="synthetic-project", plan_token="synthetic-plan")
        revision = ingest_scope(self.db, s)
        self.assertEqual(ingest_scope(self.db, dict(reversed(s.items()))), revision)
        with Ledger(self.path) as reopened:
            saved = read_scope(reopened, revision)
            self.assertEqual(saved, s)
            self.assertEqual(saved["selected_ids"], ["intake"])
            self.assertEqual(saved["excluded_ids"], ["ocr"])
            self.assertEqual(saved["edges"][0]["source"], "folder")
            canonical = reopened.conn.execute(
                "SELECT id,label,required,start_char,end_char FROM requirement WHERE request_revision_id=?",
                (revision,)).fetchall()
            expected = {r["id"]:r for r in s["requirements"]}
            self.assertEqual({r["id"] for r in canonical}, expected.keys())
            for row in canonical:
                self.assertEqual(saved["goal"][row["start_char"]:row["end_char"]], expected[row["id"]]["quote"])
                self.assertEqual(dict(row), {k:expected[row["id"]][k] for k in row.keys()})
        changed = copy.deepcopy(s)
        changed["edges"][0]["payload"] = "다른 내용"
        with self.assertRaises(ValueError):
            ingest_scope(self.db, changed)
        self.assertEqual(read_scope(self.db, revision), s)
        second = dict(changed, revision_id="scope-r2", previous_id=revision)
        self.assertEqual(ingest_scope(self.db, second), "scope-r2")
        self.assertEqual(read_scope(self.db, "scope-r2"), second)

    def test_explicit_whole_and_multiple_components(self):
        whole = example_scope()
        whole.update(mode="whole", selected_ids=["intake", "folder", "ocr"], excluded_ids=[])
        whole["requirements"][0]["component_ids"] = ["intake", "folder"]
        self.assertEqual(read_scope(self.db, ingest_scope(self.db, whole)), whole)

    def test_no_inferred_expansion_or_unscoped_material(self):
        def missing_selection(s): del s["selected_ids"]
        def empty_selection(s): s["selected_ids"] = []
        def inferred_whole(s): s["mode"] = "whole"
        def selected_excluded(s): s["excluded_ids"] += ["intake"]
        def dangling_edge(s): s["edges"][0]["source"] = "missing"
        def excluded_edge(s): s["edges"][0]["source"] = "ocr"
        def detached_node(s): s["components"].append({"id":"extra","label":"Extra"})
        def duplicate_node(s): s["components"].append(s["components"][0])
        def unknown_kind(s): s["edges"][0]["kind"] = "guess"
        def neighbor_claim(s): s["requirements"][0]["component_ids"] = ["folder"]
        def bad_anchor(s): s["requirements"][0]["start_char"] += 1
        def extra_scope(s): s["history"] = "unsolicited"
        for change in (missing_selection, empty_selection, inferred_whole, selected_excluded,
                       dangling_edge, excluded_edge, detached_node, duplicate_node, unknown_kind,
                       neighbor_claim, bad_anchor, extra_scope):
            with self.subTest(change=change.__name__):
                s = example_scope()
                change(s)
                with self.assertRaises(ValueError):
                    ingest_scope(self.db, s)
                self.assertEqual(self.db.conn.execute("SELECT count(*) FROM request_revision").fetchone()[0], 0)

    def test_cannot_mutate_or_attach_to_an_old_standalone_request(self):
        s = example_scope()
        ingest_scope(self.db, s)
        for query in ("UPDATE scope_snapshot SET sha256=sha256", "DELETE FROM scope_snapshot"):
            with self.assertRaises(sqlite3.IntegrityError):
                self.db.conn.execute(query)
        self.db.add_request("old", "old-r1", s["goal"], s["requirements"])
        with self.assertRaises(ValueError):
            ingest_scope(self.db, dict(s, request_id="old", revision_id="old-r1"))
        with self.assertRaises(KeyError):
            read_scope(self.db, "old-r1")

    def test_scope_write_failure_rolls_back_canonical_request_and_requirements(self):
        s = example_scope()
        ingest_scope(self.db, s)
        self.db.conn.execute("""CREATE TRIGGER simulated_fault BEFORE INSERT ON scope_snapshot
                BEGIN SELECT RAISE(ABORT,'storage failure'); END""")
        with self.assertRaises(sqlite3.IntegrityError):
            ingest_scope(self.db, dict(s, revision_id="scope-r2", previous_id=s["revision_id"]))
        for table in ("scope_snapshot", "request_revision", "requirement"):
            count = self.db.conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
            self.assertEqual(count, 2 if table == "requirement" else 1)


if __name__ == "__main__":
    unittest.main()
