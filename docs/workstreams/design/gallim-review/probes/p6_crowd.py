import sys
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import example_scope, ingest_scope
from catalog import Catalog
with Ledger(":memory:") as db:
    rt.seed_catalog(db)
    c = Catalog(db.conn)
    # a bookmark whose title shares many request words (no relation, never inspected)
    c.add("https://example.org/file-intake-folder-retry", title="파일 수집 폴더 재시도 중복 항목")
    c.add("https://example.org/another", title="최초 폴더의 파일을 삭제하거나 옮기지 않고")
    rev = ingest_scope(db, example_scope())
    a = rt.publish_answer(db, rev, "k")
    print("shortlist:", [(s["title"], len(s["matched_terms"]), s["matched_operations"]) for s in a["catalog_shortlist"]])
    print("answers:", [(x["title"], x["status"]) for x in a["answers"]])
    print("uninspected:", [(u["url"], u["reason"][:60]) for u in a["uninspected"]])
    a3 = rt.publish_answer(db, rev, "k3", budget=3)
    print("budget3 answers:", [(x["title"], x["status"]) for x in a3["answers"]], "| uninspected:", [u["url"] for u in a3["uninspected"]])
