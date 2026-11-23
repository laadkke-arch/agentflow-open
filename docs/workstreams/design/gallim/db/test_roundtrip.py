import sqlite3
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

from catalog import Catalog
from roundtrip import (ANNOTATION, ANNOTATION_DOC, ARCHIVES, MANUAL, UNUSED, answer_freshness,
                       answers_for_revision, publish_answer, read_answer, retract_annotation, seed_catalog)
from scope_input import example_scope, ingest_scope, read_scope
from store import Ledger


class RoundtripTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "data.db"
        self.db = Ledger(self.path)
        self.addCleanup(self.db.conn.close)
        self.links = seed_catalog(self.db)
        self.scope = example_scope()
        self.revision = ingest_scope(self.db, self.scope)

    def count(self, table):
        return self.db.conn.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]

    def publish(self, op="first", budget=2):
        return publish_answer(self.db, self.revision, op, budget)

    def test_global_catalog_to_anchored_answer(self):
        self.assertEqual(self.count("source_revision"), 0)
        self.assertEqual(self.count("candidate_context"), 0)
        # A goal may mention the context in the person's own words. Only explicit selection
        # enriches it: use sentinels in the otherwise unselected labels and edge payload.
        rev = deepcopy(self.scope)
        rev.update(revision_id="s2", previous_id=self.revision)
        rev["components"][1]["label"] = "contextual-neighbor-label"
        rev["components"][2]["label"] = "out-of-scope-ocr"
        rev["edges"][0]["payload"] = "context-only-payload"
        current = ingest_scope(self.db, rev)
        ans = publish_answer(self.db, current, "focused")
        self.assertEqual(read_scope(self.db, current), rev)
        self.assertEqual((ans["original_goal"], ans["included"], ans["excluded"]), (rev["goal"], ["intake"], ["ocr"]))
        for forbidden in ("contextual-neighbor-label", "out-of-scope-ocr", "context-only-payload"):
            self.assertNotIn(forbidden, ans["query"])
        direct, transfer = ans["answers"]
        self.assertEqual([item["url"] for item in (direct,transfer)], [MANUAL, ARCHIVES])
        self.assertEqual((direct["status"], transfer["status"]), ("excluded", "pending"))
        self.assertEqual([c["state"] for c in direct["conditions"]], ["refuted","unknown"])
        self.assertEqual([c["state"] for c in transfer["conditions"]], ["unknown","unknown"])
        self.assertEqual(direct["conditions"][1]["citations"], [])
        self.assertTrue(direct["conditions"][1]["abstention"])
        analogy = transfer["conditions"][0]
        self.assertTrue(analogy["ignored"])
        self.assertEqual(analogy["citations"], [])
        self.assertTrue(transfer["proposal"])
        for c in direct["conditions"]:
            self.assertEqual(c["component_ids"], ["intake"])
            self.assertEqual(ans["original_goal"][c["start_char"]:c["end_char"]], c["request_quote"])
        receipt = ans["sources"][direct["conditions"][0]["citations"][0]["fragment_id"]]
        self.assertEqual(receipt["capture_sha256"], sha256(ANNOTATION.encode()).hexdigest())
        self.assertIn("paraphrase",receipt["capture_scope"])
        self.assertEqual((receipt["source_url"], receipt["quote"]), (MANUAL, ANNOTATION))
        self.assertEqual(ans["next_check"]["criterion"], "keep_source")

    def test_second_project_and_zero_budget(self):
        ans = self.publish()
        initial_resources = self.count("resource")
        other = deepcopy(self.scope)
        other.update(mode="whole", request_id="independent-request", revision_id="independent-r1",
                     selected_ids=["intake"], excluded_ids=[], edges=[], components=self.scope["components"][:1])
        second = ingest_scope(self.db, other)
        none = publish_answer(self.db, second, "zero", 0)
        self.assertFalse(none["answers"])
        self.assertTrue(none["abstention"])
        res = publish_answer(self.db, second, "whole", 2)
        self.assertEqual(self.count("resource"), initial_resources)
        self.assertEqual(self.count("source_revision"), 2)
        self.assertEqual({h["catalog_item"] for h in ans["answers"]}, {h["catalog_item"] for h in res["answers"]})
        a, b = [{h["context_id"] for h in r["answers"]} for r in (ans, res)]
        self.assertTrue(a.isdisjoint(b))
        indexed = {row[0] for row in self.db.conn.execute("SELECT context_id FROM retrieval_text")}
        self.assertEqual(indexed, a | b)
        for h in res["answers"]:
            self.assertEqual(self.db.get_decision(h["run_id"])["request_revision_id"], second)
        self.assertEqual(answers_for_revision(self.db, self.revision),["first"])

    def test_bounded_acquisition_and_uninspected_link(self):
        one = self.publish("small",1)
        self.assertEqual(len(one["catalog_shortlist"]),1)
        self.assertEqual(self.count("source_revision"),1)
        self.assertEqual(self.count("candidate_context"),1)
        third = Catalog(self.db.conn)
        third.add(UNUSED, title="외환시세")
        s = deepcopy(self.scope)
        s.update(goal="외환시세", revision_id="market-r1", request_id="market", mode="whole",
                 components=[{"id":"fx","label":"외환시세"}], selected_ids=["fx"], excluded_ids=[], edges=[],
                 requirements=[dict(id="keep_source",label="외환시세",quote="외환시세",start_char=0,end_char=4,
                                    component_ids=["fx"],required=True)])
        rid = ingest_scope(self.db,s)
        ans = publish_answer(self.db,rid,"market")
        self.assertEqual([x["url"] for x in ans["uninspected"]],[UNUSED])
        self.assertFalse(ans["answers"])
        self.assertTrue(ans["abstention"])
        self.assertEqual(self.count("source_revision"),1)

    def test_history_survives_source_and_request_revision(self):
        old = self.publish()
        self.assertEqual(answer_freshness(self.db,"first")["state"],"no_recorded_successor")
        retract_annotation(self.db)
        self.assertEqual(self.publish(), old)
        self.assertEqual(self.count("decision_run"),2)
        self.assertEqual(answer_freshness(self.db,"first")["changes"][0]["id"], ANNOTATION_DOC)
        fresh = self.publish("after")
        self.assertEqual([x["status"] for x in fresh["answers"]], ["pending","pending"])
        self.assertEqual(answer_freshness(self.db,"after")["state"],"no_recorded_successor")
        self.assertEqual(read_answer(self.db,"first"),old)
        s = dict(self.scope, revision_id="s2", previous_id=self.revision)
        ingest_scope(self.db,s)
        self.assertEqual({r["kind"] for r in answer_freshness(self.db,"first")["changes"]},{"source","request"})
        self.assertEqual(read_answer(self.db,"first"),old)
        self.assertEqual(answers_for_revision(self.db, self.revision),["first","after"])
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.conn.execute("UPDATE flow_answer SET answer_json='{}' WHERE operation_key='first'")

    def test_same_condition_id_different_meaning_abstains(self):
        s = deepcopy(self.scope)
        s.update(revision_id="s2", previous_id=self.revision)
        req = s["requirements"][0]
        req["quote"] = "파일을 수집하면서"
        req["start_char"],req["end_char"] = 0,len(req["quote"])
        ans = publish_answer(self.db,ingest_scope(self.db,s),"new-meaning")
        for h in ans["answers"]:
            self.assertEqual(h["conditions"][0]["state"], "unknown")

    def test_failure_rolls_back_decisions_and_shortlist(self):
        publish = self.db.publish_decision
        seen = []
        def fail_second(*args):
            seen.append(args[0])
            if len(seen) == 2:
                raise RuntimeError("artificial interruption before answer commit")
            return publish(*args)
        with patch.object(self.db,"publish_decision",side_effect=fail_second), self.assertRaises(RuntimeError):
            self.publish()
        self.assertEqual(len(seen),2)
        for table in ("decision_run","candidate_context","source_revision"):
            self.assertEqual(self.count(table),0)
        self.assertEqual(answers_for_revision(self.db,self.revision),[])
        self.assertEqual(len(self.publish()["answers"]),2)

    def test_concurrent_retry_and_key_collision(self):
        def run(_):
            with Ledger(self.path) as handle:
                return publish_answer(handle,self.revision,"raced",2)
        with ThreadPoolExecutor(max_workers=2) as pool:
            first, second = pool.map(run, range(2))
        self.assertEqual(first,second)
        self.assertEqual(self.count("decision_run"),2)
        with self.assertRaises(ValueError):
            self.publish("raced",1)
        # A caller can reopen SQLite read-only to recover an earlier published answer.
        conn = sqlite3.connect(self.path.resolve().as_uri() + "?mode=ro",uri=True)
        self.addCleanup(conn.close)
        handle = type("ReadOnly", (), {"conn":conn})()
        self.assertEqual(read_answer(handle,"raced"),first)


if __name__ == "__main__":
    unittest.main()
