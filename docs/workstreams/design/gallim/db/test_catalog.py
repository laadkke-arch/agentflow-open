"""Offline synthetic fixtures; their mechanisms are test data, not external research."""
import sqlite3
import unittest

from catalog import Catalog, canonical_url
from store import Ledger


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.db=Ledger(":memory:")
        self.addCleanup(self.db.conn.close)
        self.cat=Catalog(self.db.conn)

    def test_just_a_url_preserves_bounded_identity_and_aliases(self):
        c=self.cat
        first="https://EXAMPLE.ORG:443/tool?ref=v1#consume"
        key=c.add(first)
        self.assertEqual(c.add("https://example.org/tool?ref=v1#consume"),key)
        self.assertEqual(c.get(key)["url"],first)
        self.assertEqual(len(c.get(key)["aliases"]),2)
        self.assertEqual(c.get(key)["relations"],[])
        self.assertIsNone(c.get(key)["note"])
        for other in ("https://example.org/tool?ref=v2#consume",
                      "https://example.org/tool?ref=v1#export",
                      "https://example.org/Tool?ref=v1#consume",
                      "https://example.org/tool?ref=v1"):
            self.assertNotEqual(c.add(other),key)
        self.assertNotEqual(canonical_url("https://example.org/x?#"),
                            canonical_url("https://example.org/x#"))
        self.assertEqual(canonical_url("https://example.org/x?#"),"https://example.org/x?#")
        self.assertEqual(canonical_url("https://example.org/x?z=9&k=2"),"https://example.org/x?z=9&k=2")
        self.assertEqual(c.get(key)["form"],"unknown")
        self.assertEqual(self.db.conn.execute("SELECT count(*) FROM decision_run").fetchone()[0],0)

    def test_incremental_enrichment_and_retrieval(self):
        url="https://example.org/study#part"
        item=self.cat.add(url)
        self.assertEqual(self.cat.add(url,title="마스터 보관",form="website"),item)
        self.assertEqual(self.cat.discover("마스터")[0]["matched"],["terms"])
        self.assertEqual(self.cat.add(url),item)
        self.assertEqual(self.cat.get(item)["title"],"마스터 보관")
        with self.assertRaises(ValueError):
            self.cat.add(url,title="다른 제목")
        self.assertEqual(self.cat.discover("다른"),[])
        self.assertEqual(self.cat.discover("마스터")[0]["item_id"],item)

    def test_far_mechanism_and_near_lexical_are_separable(self):
        c=self.cat
        direct=c.add("https://example.org/input#stage",title="문서 보존",form="feature")
        near=c.add("https://example.org/notebooks",title="문서 보존 노트의 서체",form="service")
        far=c.add("https://example.org/museum#replicas",title="전시품과 복제품",form="mechanism")
        miss=c.add("https://example.org/salt",title="소금",form="other")
        for item in (direct,far):
            c.add_relation(item,"권위본 분리","권위본을 유지하고 작업용 사본만 다룬다.",
                           "원래 위치나 복제의 완전성은 별도 확인한다.",c.get(item)["url"],"test:curator")
        hits=c.discover("문서 보존",operations=["권위본 분리"])
        self.assertEqual([h["item_id"] for h in hits],[direct,far,near])
        self.assertNotIn(miss,[h["item_id"] for h in hits])
        self.assertEqual(hits[1]["matched"],["operation"])
        self.assertEqual(hits[2]["matched"],["terms"])
        self.assertIn("미확인",hits[0]["unknown"])
        self.assertTrue(all(h["relations"][0]["breaks_at"] for h in hits[:2]))
        self.assertEqual(self.db.conn.execute("SELECT count(*) FROM candidate_context").fetchone()[0],0)

    def test_unseen_request_reuses_global_data_and_only_selected_items_materialize(self):
        c=self.cat
        first=c.add("https://example.org/repository/doc#piece",title="원본 처리",form="feature")
        c.add("https://example.org/another",title="원본 복구",form="oss")
        req=[dict(id="keep",label="보관",required=True,start_char=0,end_char=2)]
        for rq in ("r1","r2"):
            self.db.add_request(rq,rq+"@1","보관",req)
            hits=c.discover("원본")
            self.assertEqual(len(hits),2)
            key=c.shortlist(self.db,rq+"@1",first,version="fixed",scope="one inlet",configuration="direct")
            self.assertEqual(c.shortlist(self.db,rq+"@1",first,version="fixed",scope="one inlet",configuration="direct"),key)
        conn=self.db.conn
        for table,count in (("catalog_link",2),("resource",1),("edition",1),("candidate_context",2),
                            ("catalog_shortlist",2),("claim",0),("source_document",0),("decision_run",0)):
            self.assertEqual(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0],count)
        key2=c.shortlist(self.db,"r1@1",first,version="next",scope="one inlet",configuration="direct")
        self.assertNotEqual(key,key2)
        with self.assertRaises(sqlite3.IntegrityError):
            c.shortlist(self.db,"missing",first,version="missing-version",scope="test",configuration="test")
        self.assertEqual(conn.execute("SELECT count(*) FROM edition WHERE version='missing-version'").fetchone()[0],0)

    def test_needs_no_ledger_and_outer_rollback(self):
        connection=sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        cat=Catalog(connection)
        item=cat.add("https://example.org/item")
        self.assertEqual(cat.discover("item")[0]["item_id"],item)
        with self.assertRaises(RuntimeError):
            with self.db.transaction():
                cat=Catalog(self.db.conn)
                cat.add("https://example.org/rollback")
                raise RuntimeError("cancel publication")
        self.assertEqual(self.cat.discover("rollback"),[])
        for url in ("file://private/path","https://user:pass@example.org/x","http://127.0.0.1/x"):
            with self.assertRaises(ValueError):
                self.cat.add(url)


if __name__=="__main__":
    unittest.main()
