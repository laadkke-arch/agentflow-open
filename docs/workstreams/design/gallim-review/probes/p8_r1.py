"""Common request R1 = AF-RES-012 P03.w (ko) through the pinned gallim code."""
import sys, json, subprocess
sys.path.insert(0, sys.argv[1])
import roundtrip as rt
from store import Ledger
from scope_input import ingest_scope
from catalog import Catalog
from retrieval import infer_mechanisms
REPO, PIN, STUDY = sys.argv[2], "cb602858378db90adb1f085953016267f9afbd6d", "docs/workstreams/research/AF-RES-012"
show = lambda p: subprocess.check_output(["git","-C",REPO,"show",f"{PIN}:{STUDY}/{p}"]).decode()
entries = [json.loads(l) for l in show("corpus/entries.jsonl").splitlines()]
Q = {q["id"]: q for q in map(json.loads, show("queries/queries.jsonl").splitlines())}
rel = {"asyncio-queue":"2","asyncio-semaphore":"1","reactive-streams":"1","toyota-jit":"1","npm-p-limit":"1","npm-p-queue":"1","pypi-janus":"1","token-bucket":"N"}
goal = Q["P03.w"]["ko"]
def req(i, quote):
    s = goal.index(quote); return dict(id=i, label=i, required=True, quote=quote, start_char=s, end_char=s+len(quote), component_ids=["admission"])
scope = dict(request_id="r1", revision_id="r1-ko", mode="partial", goal=goal,
  components=[{"id":"admission","label":"작업 투입·완료 신호"},{"id":"convert","label":"이미지 변환"},{"id":"store","label":"최종 저장"}],
  selected_ids=["admission"], excluded_ids=[],
  edges=[dict(id="e1",source="admission",target="convert",kind="data",payload="lazy iterator 항목"),
         dict(id="e2",source="store",target="admission",kind="control",payload="완료 신호")],
  requirements=[req("H1","대기 큐 안의 항목 수는 최대 8개이고 처리 중 작업은 최대 4개여야 한다"),
                req("H2","sink가 느려지면 producer가 기다려야 하며, 모든 입력에 대해 task를 미리 만들거나 다른 무제한 buffer로 옮기면 안 된다"),
                req("H3","처리 완료/용량 회복을 투입 재개의 근거로 삼고, 단순 시간 경과만으로 처리 중 상한을 넘겨서는 안 된다")])
def load(db, mode, lang="ko"):
    c = Catalog(db.conn)
    for e in entries:
        if mode == "seed-only": break
        title = e["D-a"][lang] if mode in ("url+title","url+title+note") else None
        note = e["D-b"][lang] if mode == "url+title+note" else None
        c.add(e["url"], title=title, note=note, provenance="AF-RES-012 corpus" if note else None)
for mode in ("seed-only","url","url+title","url+title+note"):
    with Ledger(":memory:") as db:
        rt.seed_catalog(db); load(db, mode)
        rev = ingest_scope(db, scope)
        q = rt._query(scope)
        top = Catalog(db.conn).discover(q, operations=infer_mechanisms(q), limit=10)
        by_url = {e["url"]: e["id"] for e in entries}
        ids = [by_url.get(h["url"], h["title"] or h["url"]) for h in top]
        print(f"== {mode}: mechanisms={infer_mechanisms(q)} top10:")
        for i,(h,eid) in enumerate(zip(top,ids),1):
            print(f"   {i:2d} {eid:28s} grade={rel.get(eid,'-'):2s} why={h['why']}")
        a = rt.publish_answer(db, rev, "r1", budget=3)
        print("   answers:", [(x["title"],x["status"]) for x in a["answers"]], "| uninspected:", len(a["uninspected"]), "| abstention:", a["abstention"])
        print("   remembered rows: flow_answer", db.conn.execute("select count(*) from flow_answer").fetchone()[0],
              "candidate_context", db.conn.execute("select count(*) from candidate_context").fetchone()[0],
              "decision_run", db.conn.execute("select count(*) from decision_run").fetchone()[0],
              "catalog_link", db.conn.execute("select count(*) from catalog_link").fetchone()[0])
