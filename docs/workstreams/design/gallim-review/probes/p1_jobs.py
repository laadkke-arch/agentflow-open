import sys, json
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import example_scope, ingest_scope
with Ledger(":memory:") as db:
    rt.seed_catalog(db)
    rev = ingest_scope(db, example_scope())
    a1 = rt.publish_answer(db, rev, "first")
    print("jobs after first:", db.pending_jobs())
    rt.retract_annotation(db)
    print("jobs after retraction:", db.pending_jobs())
    a2 = rt.publish_answer(db, rev, "after-synthetic-review")
    print("jobs after second publish:", db.pending_jobs())
    print("freshness(first):", rt.answer_freshness(db, "first"))
    print("freshness(second):", rt.answer_freshness(db, "after-synthetic-review"))
    # replay old answer
    old = rt.read_answer(db, "first")
    print("old answer statuses:", [(x["title"], x["status"]) for x in old["answers"]])
    print("uninspected first:", old["uninspected"])
    print("shortlist first:", [(s["title"], s["matched_terms"], s["matched_operations"]) for s in old["catalog_shortlist"]])
    print("next_check first:", old["next_check"], [ (x["context_id"], x["title"]) for x in old["answers"]])
    # retry same key
    again = rt.publish_answer(db, rev, "first")
    print("retry same key equal:", again == old)
