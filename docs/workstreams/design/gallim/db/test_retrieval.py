import sqlite3
import unittest

from retrieval import DEDUP, PRESERVE, RETAIN, Relation, SearchEntry, demo_fixture, infer_mechanisms, rebuild_index, search


class RetrievalTest(unittest.TestCase):
    def setUp(self):
        self.conn, self.entries = demo_fixture()
        self.addCleanup(self.conn.close)

    def test_plain_language_finds_distant_candidate_and_conflicting_near_miss(self):
        query = "Scan PDF, do not delete the original folder file; prevent duplicate entries."
        result = search(self.conn, query, budget=2, request_revision_id="scan")
        self.assertEqual(result["query"], query)
        self.assertIn("not", result["query_terms"])
        self.assertEqual(result["mechanisms"], [PRESERVE, DEDUP])
        inbox, archive = result["hits"]
        self.assertEqual(inbox["context_id"], "box")
        edges = {r["mechanism"]: r["relation"] for r in inbox["routes"] if r["route"] == "mechanism"}
        self.assertEqual(edges, {DEDUP: "implements", PRESERVE: "violates"})
        self.assertEqual(archive["context_id"], "museum")
        self.assertEqual([r["route"] for r in archive["routes"]], ["mechanism"])
        self.assertTrue(all(h["verification"] == "unverified" for h in result["hits"]))

    def test_distinct_failures_and_control_are_reported_honestly(self):
        result = search(self.conn, "keep batch success after later failure", budget=3, request_revision_id="batch")
        hits = {h["context_id"]: h for h in result["hits"]}
        self.assertEqual(result["mechanisms"], [RETAIN])
        self.assertEqual(hits["ledger"]["routes"][0]["relation"], "transfer_hypothesis")
        self.assertEqual(hits["rollback"]["routes"][-1]["relation"], "violates")
        self.assertEqual([r["route"] for r in hits["dashboard"]["routes"]], ["lexical"])
        self.assertEqual(search(self.conn, "잘못된 요구", budget=0)["hits"], [])

    def test_no_positive_route_from_explicit_negative_or_unrelated_request(self):
        self.assertEqual(infer_mechanisms("Delete the original file"), [])
        self.assertEqual(infer_mechanisms("Do not preserve the original folder"), [])
        self.assertEqual(infer_mechanisms("원본 파일 경로를 그대로 유지하고 중복 등록을 막아줘"), [PRESERVE, DEDUP])
        self.assertEqual(infer_mechanisms("파일이 실패해도 성공 결과는 남겨줘"), [RETAIN])
        self.assertEqual(search(self.conn, "avocado", mechanism="unknown")["hits"], [])
        self.assertEqual(search(self.conn, '!" OR NOT *', mechanism=[], request_revision_id="absent")["hits"], [])

    def test_scope_example_preserves_both_constraints_without_turning_deletion_into_preservation(self):
        text = "파일을 수집하면서 최초 폴더의 파일을 삭제하거나 옮기지 않고, 재시도해도 중복 항목을 만들지 않는다."
        result = search(self.conn, text, budget=2, request_revision_id="scan")
        self.assertEqual(result["query"], text)
        self.assertEqual(result["mechanisms"], [PRESERVE, DEDUP])
        self.assertCountEqual([h["context_id"] for h in result["hits"]], ["box", "museum"])
        for control in ("최초 폴더의 파일은 보존하지 않고 삭제한다. 재시도해도 중복 항목을 만들지 않는다.",
                        "최초 폴더의 파일을 삭제하고 중복을 만들지 않는다."):
            self.assertEqual(infer_mechanisms(control), [DEDUP])

    def test_bounded_query_work_and_normalized_unicode(self):
        from retrieval import MAX_QUERY_CHARS, MAX_QUERY_TERMS
        with self.assertRaisesRegex(ValueError, "Unicode characters"):
            search(self.conn, "가" * (MAX_QUERY_CHARS + 1))
        with self.assertRaisesRegex(ValueError, "distinct lexical terms"):
            search(self.conn, " ".join(str(n) for n in range(MAX_QUERY_TERMS+1)))
        text = "ｋｅｅｐ original folder"
        result = search(self.conn, text, budget=0)
        self.assertEqual(result["query"], text)
        self.assertIn("keep", result["query_terms"])
        self.assertIn(PRESERVE, result["mechanisms"])

    def test_multiple_evidence_does_not_manufacture_multiple_candidates(self):
        self.conn.execute("INSERT INTO source_fragment VALUES('box-second')")
        body = self.entries[0].text
        extra = SearchEntry("box", body, ("box-second",), (Relation(PRESERVE, "violates", "box-second"),))
        rebuild_index(self.conn, [*self.entries, self.entries[0], extra])
        result = search(self.conn, "scan PDF", PRESERVE, 9, "scan")
        self.assertEqual([h["context_id"] for h in result["hits"]].count("box"), 1)
        box = next(h for h in result["hits"] if h["context_id"] == "box")
        self.assertCountEqual(box["source_ids"], ["box-fragment", "box-second"])
        self.assertEqual(self.conn.execute("SELECT count(*) FROM retrieval_text WHERE context_id='box'").fetchone()[0], 1)

    def test_refresh_isolated_from_other_work_and_existing_index_on_failure(self):
        self.conn.commit()
        self.conn.execute("INSERT INTO source_fragment VALUES('uncommitted')")
        before = search(self.conn, "scan PDF", PRESERVE)
        for entry in (SearchEntry("no-context", "body", ("box-fragment",)),
                      SearchEntry("box", "body", ("nonexistent-fragment",)),
                      SearchEntry("box", "body", ("box-fragment",), (Relation(PRESERVE, "invented", "box-fragment"),))):
            with self.assertRaises(ValueError):
                rebuild_index(self.conn, [entry])
            self.assertEqual(search(self.conn, "scan PDF", PRESERVE), before)
        self.assertTrue(self.conn.in_transaction)
        self.conn.rollback()
        self.assertFalse(self.conn.execute("SELECT 1 FROM source_fragment WHERE id='uncommitted'").fetchone())

    def test_revision_rebuild_preserves_other_project_and_rolls_back_atomically(self):
        def observed(req):
            return search(self.conn, "scan PDF batch failure", [PRESERVE, RETAIN], 9, req)
        original_scan, original_batch = observed("scan"), observed("batch")
        with self.assertRaises(ValueError):
            rebuild_index(self.conn, self.entries, request_revision_id="scan")
        self.assertEqual(observed("scan"), original_scan)
        self.assertEqual(observed("batch"), original_batch)
        self.conn.commit()
        self.conn.execute("BEGIN")
        rebuild_index(self.conn, [self.entries[1]], request_revision_id="scan")
        self.assertEqual([h["context_id"] for h in observed("scan")["hits"]], ["museum"])
        self.assertEqual(observed("batch"), original_batch)
        self.conn.rollback()
        self.assertEqual(observed("scan"), original_scan)

        # A failed insert after the delete must roll back BOTH search indices.
        self.conn.execute("""CREATE TRIGGER reject_edge BEFORE INSERT ON retrieval_edge
                           BEGIN SELECT RAISE(ABORT, 'failure after projection delete'); END""")
        with self.assertRaises(sqlite3.IntegrityError):
            rebuild_index(self.conn, [self.entries[1]], request_revision_id="scan")
        self.assertEqual(observed("scan"), original_scan)
        self.assertEqual(observed("batch"), original_batch)

    def test_rebuild_against_canonical_schema_and_rollback_after_replacement(self):
        from pathlib import Path
        bundled = Path(__file__).with_name("schema.sql")
        if not bundled.exists():  # Before packaging, the canonical store is in a sister directory.
            bundled = Path(__file__).resolve().parents[1] / "storage_lab" / "schema.sql"
        conn = sqlite3.connect(":memory:")
        self.addCleanup(conn.close)
        conn.executescript(bundled.read_text())
        conn.execute("INSERT INTO request_revision VALUES('r','r',NULL,'read')")
        conn.execute("INSERT INTO resource VALUES('s','Name','product')")
        conn.execute("INSERT INTO edition VALUES('e','s','1')")
        conn.execute("INSERT INTO candidate_context VALUES('c','r','e','scope','config')")
        conn.execute("INSERT INTO source_document VALUES('d','fixture:test','test')")
        conn.execute("INSERT INTO source_revision VALUES('d','v',NULL,'source','text',?)", ("a"*64,))
        conn.execute("INSERT INTO source_fragment VALUES('f','d','v',0,4,?,'fixture:fragment')", ("a"*64,))
        rebuild_index(conn, [SearchEntry("c", "text", ("f",))])
        conn.commit()
        conn.execute("BEGIN")
        rebuild_index(conn, [])
        self.assertFalse(search(conn, "text")["hits"])
        conn.rollback()
        self.assertEqual(search(conn, "text")["hits"][0]["context_id"], "c")


if __name__ == "__main__":
    unittest.main()
