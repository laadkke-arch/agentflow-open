import sys, json
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import ingest_scope
from retrieval import infer_mechanisms
from catalog import Catalog

def scope(rid, goal, clauses, comps, selected, edges=None, excluded=()):
    reqs=[]
    for key,label,quote in clauses:
        s=goal.index(quote); reqs.append(dict(id=key,label=label,required=True,quote=quote,start_char=s,end_char=s+len(quote),component_ids=[selected[0]]))
    return dict(request_id=rid, revision_id=rid+"-r1", mode="partial", goal=goal, components=comps,
                selected_ids=list(selected), excluded_ids=list(excluded), edges=edges or [], requirements=reqs)

cases = {
 # Months later: other domain, other words, same relation
 "ml-augment-ko": scope("ml", "학습 데이터 원본은 그대로 두고 증강본만 만들어 학습에 쓴다.",
     [("keep","원본 유지","학습 데이터 원본은 그대로 두고")],
     [{"id":"aug","label":"데이터 증강"}], ["aug"]),
 # Same relation, no trigger vocabulary
 "inbox-en": scope("en", "Files dropped into the inbox must stay where the user put them, and re-uploading must not create a second record.",
     [("stay","stay","Files dropped into the inbox must stay where the user put them"),("once","once","re-uploading must not create a second record")],
     [{"id":"in","label":"inbox import"}], ["in"]),
 # Same project wording but paraphrased requirement
 "paraphrase-ko": scope("pk", "스캔본을 가져올 때 처음 폴더에 있던 원본 파일은 그대로 남겨 두고, 같은 파일을 다시 넣어도 한 건만 생겨야 한다.",
     [("keep","원본 유지","처음 폴더에 있던 원본 파일은 그대로 남겨 두고"),("one","한 건","같은 파일을 다시 넣어도 한 건만 생겨야 한다")],
     [{"id":"intake","label":"파일 수집"}], ["intake"]),
}
for name, sc in cases.items():
    with Ledger(":memory:") as db:
        rt.seed_catalog(db)
        rev = ingest_scope(db, sc)
        q = rt._query(sc)
        print("==", name, "| mechanisms:", infer_mechanisms(q))
        a = rt.publish_answer(db, rev, "k")
        for s in a["catalog_shortlist"]:
            print("  shortlist:", s["title"], "terms", s["matched_terms"], "ops", s["matched_operations"])
        for x in a["answers"]:
            print("  answer:", x["title"], x["status"], {c["requirement_id"]:c["state"] for c in x["conditions"]}, "| proposal:", x["proposal"])
        print("  uninspected:", a["uninspected"], "| abstention:", a["abstention"], "| next:", a["next_check"])
