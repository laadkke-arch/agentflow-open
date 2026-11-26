"""Sealed case EVAL-X1 T0 and T3 requests through the pinned gallim code (baseline only)."""
import sys, json, subprocess
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import ingest_scope
from catalog import Catalog
from retrieval import infer_mechanisms
REPO, PIN, STUDY = sys.argv[2], "cb602858378db90adb1f085953016267f9afbd6d", "docs/workstreams/research/AF-RES-012"
case = json.loads((Path(__file__).resolve().parent.parent / "sealed-case.json").read_text())
show = lambda p: subprocess.check_output(["git", "-C", REPO, "show", f"{PIN}:{STUDY}/{p}"]).decode()
entries = [json.loads(l) for l in show("corpus/entries.jsonl").splitlines()]
req = case["request"]
goal = " ".join([req["goal"]] + [r["text"] for r in req["requirements"]])
def scope(rid, goal, quotes, comp):
    reqs = []
    for i, q in quotes:
        s = goal.index(q); reqs.append(dict(id=i, label=i, required=True, quote=q, start_char=s, end_char=s + len(q), component_ids=[comp["id"]]))
    return dict(request_id=rid, revision_id=rid + "-r1", mode="partial", goal=goal, components=[comp], selected_ids=[comp["id"]],
                excluded_ids=[], edges=[], requirements=reqs)
t0 = scope("evalx1", goal, [(r["id"], r["text"]) for r in req["requirements"]], {"id": "saved", "label": "저장 목록"})
t3_text = case["checkpoints"][4]["request"]
t3 = scope("evalx1-t3", t3_text, [("keep", "서비스가 문을 닫아도 북마크가 우리 서버에 남아야 한다")], {"id": "bm", "label": "참고문헌 북마크"})
for name, sc in (("T0", t0), ("T3", t3)):
    for mode in ("seed-only", "url+title(ko)"):
        with Ledger(":memory:") as db:
            rt.seed_catalog(db)
            if mode != "seed-only":
                c = Catalog(db.conn)
                for e in entries: c.add(e["url"], title=e["D-a"]["ko"])
            rev = ingest_scope(db, sc)
            q = rt._query(sc)
            top = Catalog(db.conn).discover(q, operations=infer_mechanisms(q), limit=5)
            a = rt.publish_answer(db, rev, name, budget=3)
            print(f"== {name} {mode}: mechanisms={infer_mechanisms(q)}")
            for h in top: print("   top:", h["title"] or h["url"], "| why:", h["why"])
            print("   answers:", [(x["title"], x["status"]) for x in a["answers"]], "| uninspected:", len(a["uninspected"]), "| abstention:", a["abstention"])
