"""Deletion test: replace the second-stage FTS/edge index with 'display shortlist as-is'."""
import sys, json, importlib
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import example_scope, ingest_scope
sys.path.insert(0, sys.argv[2]); import p2_other  # reuse scopes (prints its own output)
def run(sc, stage2=True, retract=False):
    importlib.reload(rt)
    if not stage2:
        rt.rebuild_index = lambda *a, **k: None
        def passthrough(conn, query, budget=2, request_revision_id=None):
            if not conn.execute("SELECT 1 FROM sqlite_master WHERE name='catalog_shortlist'").fetchone():
                return {"query":query,"trace":{"stage2":"deleted"},"hits":[]}
            rows = conn.execute("SELECT context_id FROM catalog_shortlist s JOIN candidate_context c ON c.id=s.context_id WHERE c.request_revision_id=? ORDER BY s.rowid", (request_revision_id,)).fetchall()
            hits=[{"context_id":r[0],"title":None,"routes":[],"source_ids":[]} for r in rows][:budget]
            return {"query":query,"trace":{"stage2":"deleted"},"hits":hits}
        rt.search = passthrough
    with Ledger(":memory:") as db:
        rt.seed_catalog(db); rev = ingest_scope(db, sc)
        a = rt.publish_answer(db, rev, "k")
        out=[(x["title"], x["status"], tuple(sorted((c["requirement_id"],c["state"]) for c in x["conditions"]))) for x in a["answers"]]
        if retract:
            rt.retract_annotation(db); b = rt.publish_answer(db, rev, "k2")
            out.append(("after", tuple((x["title"], x["status"]) for x in b["answers"])))
        return sorted(out, key=str), a["next_check"] is not None
cases = {"example": example_scope(), **p2_other.cases}
for name, sc in cases.items():
    for retract in ((False, True) if name=="example" else (False,)):
        with_s2, without = run(sc, True, retract), run(sc, False, retract)
        print(f"{name:15s} retract={retract!s:5s} same={with_s2==without}  stage2={with_s2[0]}")
