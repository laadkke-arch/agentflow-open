"""Offline round-trip using a frozen partial-map request and a curated, bounded index."""
import json

from catalog import Catalog
from demo import evaluate, next_check
from retrieval import PRESERVE, Relation, SearchEntry, infer_mechanisms, rebuild_index, search
from scope_input import example_scope, ingest_scope, read_scope
from store import Ledger, canonical, digest


VERSION = "roundtrip.1"
POLICY = "document-criteria.1"
COMMIT = "4973be8499bc61dc4f791a609d0d31e9ac9ccd41"
MANUAL = f"https://github.com/paperless-ngx/paperless-ngx/blob/{COMMIT}/docs/usage.md"
LOCATOR = MANUAL + "#L147-L183"
# This is an authored annotation of the public section; its digest covers our words only.
ANNOTATION = "파일 수집: 소비 폴더에 둔 파일은 처리 후 그 폴더에 남지 않는다."
CORRECTION = "합성 철회 연습: 이전 해석을 철회한다. 새 직접 근거는 아직 판독하지 않았다."
ARCHIVES = "https://www.archives.gov/preservation/products/definitions/preservation-copy"
MASTER_NOTE = "보존용 마스터를 장기간 유지하며 복제·배포용 사본을 만든다."
TRANSFER = "보존용 마스터에서 사본을 만드는 원리를 빌려, 최초 폴더를 읽기 전용으로 두고 별도 작업본을 수집하는 설계를 제안한다."
ANNOTATION_DOC = "fixture-paperless-annotation"
MASTER_DOC = "fixture-nara-annotation"
UNUSED = "https://example.org/reference-to-classify"



def _answer_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS flow_answer(
        operation_key TEXT PRIMARY KEY NOT NULL,
        request_revision_id TEXT NOT NULL REFERENCES request_revision(id),
        command_sha256 TEXT NOT NULL, answer_json TEXT NOT NULL, answer_sha256 TEXT NOT NULL)""")
    for op in ("UPDATE", "DELETE"):
        conn.execute(f"""CREATE TRIGGER IF NOT EXISTS flow_answer_no_{op} BEFORE {op}
            ON flow_answer BEGIN SELECT RAISE(ABORT,'immutable answer'); END""")


def read_answer(db, operation_key):
    """Read the exact persisted response, without making a new decision or rebuilding an index."""
    if db.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='flow_answer'").fetchone():
        row = db.conn.execute("SELECT answer_json,answer_sha256 FROM flow_answer WHERE operation_key=?",
                              (operation_key,)).fetchone()
        if row:
            if digest(row[0]) != row[1]:
                raise ValueError("answer integrity check failed")
            return json.loads(row[0])
    raise KeyError(operation_key)


def _citation(conn, fragment_id):
    row = conn.execute("""SELECT f.id AS fragment_id,f.document_id,f.revision_key,
            f.locator,f.start_char,f.end_char,f.sha256 AS fragment_sha256,
            r.sha256 AS capture_sha256,r.capture_scope,r.content,d.url AS source_url
            FROM source_fragment f JOIN source_revision r USING(document_id,revision_key)
            JOIN source_document d ON d.id=f.document_id WHERE f.id=?""", (fragment_id,)).fetchone()
    if not row:
        raise ValueError("missing source fragment")
    out = dict(row)
    capture = out.pop("content")
    out["quote"] = capture[row["start_char"]:row["end_char"]]
    if digest(capture) != out["capture_sha256"] or digest(out["quote"]) != out["fragment_sha256"]:
        raise ValueError("captured source integrity check failed")
    return out


def _successor(conn, document_id, revision_key):
    return conn.execute("""SELECT revision_key FROM source_revision WHERE document_id=?
                           AND previous_key=?""", (document_id, revision_key)).fetchone()


def answer_freshness(db, operation_key):
    """Check current request/source lineage, keeping the historical response immutable."""
    answer = read_answer(db, operation_key)
    # One SELECT observes all lineages at one SQLite snapshot.
    rows = db.conn.execute("""SELECT 'source', s.document_id, s.previous_key, s.revision_key
        FROM source_revision s JOIN json_each(?) j
        ON s.document_id=json_extract(j.value,'$.document_id')
        AND s.previous_key=json_extract(j.value,'$.revision_key')
        UNION SELECT 'request', request_id, previous_id, id FROM request_revision WHERE previous_id=?
        ORDER BY 1,2,3,4""", (canonical(list(answer["sources"].values())), answer["request_revision_id"]))
    changes = [dict(kind=r[0], id=r[1], old=r[2], successor=r[3]) for r in rows]
    return {"state": "stale" if changes else "no_recorded_successor", "changes": changes}


def _query(scope):
    included = set(scope["selected_ids"])
    labels = [c["label"] for c in scope["components"] if c["id"] in included]
    # The immutable human goal stays verbatim. Neighbor labels, edges, excluded nodes and UI
    # state do not expand the query. Requirements already have validated, selected-only anchors.
    return "\n".join([scope["goal"], *labels, *(r["label"] + " " + r["quote"] for r in scope["requirements"])])


def publish_answer(db, revision_id, operation_key, budget=2):
    """Publish selected results and their decision runs atomically; replay keys recover the old answer."""
    if not isinstance(operation_key, str) or not operation_key.strip():
        raise ValueError("operation_key required")
    if type(budget) is not int or not 0 <= budget <= 3:
        raise ValueError("display budget must be 0..3")
    cmd = digest(canonical([VERSION, POLICY, revision_id, budget]))
    with db.transaction():
        _answer_tables(db.conn)
        prior = db.conn.execute("SELECT command_sha256 FROM flow_answer WHERE operation_key=?",
                                (operation_key,)).fetchone()
        if prior:
            if cmd != prior[0]:
                raise ValueError("operation key reused for another answer command")
            return read_answer(db, operation_key)
        scope = read_scope(db, revision_id)
        catalog = Catalog(db.conn)
        query = _query(scope)
        shortlist = catalog.discover(query, operations=infer_mechanisms(query), limit=budget) if budget else []
        entries, unresolved, origins = [], [], {}
        for link in shortlist:
            entry = _inspect_public_fixture(db, catalog, link, scope)
            if entry is None:
                unresolved.append({"item_id": link["item_id"], "url": link["url"],
                                   "reason": "No curated document inspection available in this offline demo."})
            else:
                entries.append(entry)
                origins[entry.context_id] = link
        rebuild_index(db.conn, entries, request_revision_id=revision_id)
        found = search(db.conn, query, budget=budget, request_revision_id=revision_id)
        answers, outcomes, sources = [], {}, {}

        def capture(fragment_id):
            if fragment_id not in sources:
                record = _citation(db.conn, fragment_id)
                if _successor(db.conn, record["document_id"], record["revision_key"]):
                    raise ValueError("source superseded; refresh index before publishing")
                sources[fragment_id] = record
            return fragment_id

        for hit in found["hits"]:
            ctx = hit["context_id"]
            route_sources = [capture(sid) for sid in hit["source_ids"]]
            run = db.publish_decision(ctx, "flow/" + digest(canonical([operation_key, ctx])), evaluate, POLICY)
            decision = db.get_decision(run)
            judgement = decision["output"]
            outcomes[ctx] = judgement
            claims = {c["id"]: c for c in decision["input"]["claims"]}
            conditions = []
            for req in scope["requirements"]:
                outcome = judgement["criteria"][req["id"]]
                evidence = [dict(claim_id=key, fragment_id=capture(claims[key]["fragment_id"]))
                            for key in outcome["used"]]
                rejected = [dict(claim_id=key, fragment_id=capture(claims[key]["fragment_id"]), reason=why)
                            for key, why in outcome["ignored"].items()]
                conditions.append(dict(requirement_id=req["id"], component_ids=req["component_ids"],
                                       request_quote=req["quote"], start_char=req["start_char"], end_char=req["end_char"],
                                       state=outcome["state"], citations=evidence, ignored=rejected,
                                       abstention=outcome["explanation"] if not evidence else None))
            answers.append(dict(context_id=ctx, title=origins[ctx]["title"] or hit["title"], context=decision["input"]["candidate"]["context"],
                                run_id=run, status=judgement["status"], conditions=conditions,
                                discovery_routes=hit["routes"], discovery_sources=route_sources,
                                catalog_item=origins[ctx]["item_id"], url=origins[ctx]["url"],
                                proposal=TRANSFER if origins[ctx]["canonical_url"] == ARCHIVES else None))
        inspected = {hit["context_id"] for hit in found["hits"]}
        for ctx, link in origins.items():
            if ctx not in inspected:
                unresolved.append({"item_id": link["item_id"], "url": link["url"],
                                   "reason": "Global match did not pass the second retrieval stage."})
        answer = dict(schema=VERSION, request_revision_id=revision_id, operation_key=operation_key,
                      original_goal=scope["goal"], included=scope["selected_ids"], excluded=scope["excluded_ids"],
                      requirements=scope["requirements"], query=found["query"], search_trace=found["trace"],
                      catalog_shortlist=shortlist, uninspected=unresolved, answers=answers, sources=sources, next_check=next_check(scope["requirements"], outcomes),
                      abstention=None if answers else "No candidates returned within the requested display budget.")
        raw = canonical(answer)
        db.conn.execute("INSERT INTO flow_answer VALUES(?,?,?,?,?)", (operation_key, revision_id, cmd, raw, digest(raw)))
        return json.loads(raw)


def _inspect_public_fixture(db, catalog, link, scope):
    """Two disclosed manual readings. Other catalog links remain discoverable and explicitly uninspected."""
    url = link["canonical_url"]
    if url not in (MANUAL, ARCHIVES):
        return None
    revision_id = scope["revision_id"]
    eligible_components = {c["id"] for c in scope["components"] if c["label"] == "파일 수집"}
    # This offline bridge only knows the reviewed meaning of this particular anchored condition.
    # ID equality across projects never grants a matching claim to a different requirement.
    eligible_req = [r for r in scope["requirements"]
                    if r["quote"] == "최초 폴더의 파일을 삭제하거나 옮기지 않고"
                    and set(r["component_ids"]) <= eligible_components]
    if url == MANUAL:
        version, config = COMMIT, "최초 폴더 직접 소비"
    else:
        version, config = "NARA page reviewed 2023-10-26; proposal.1", "보존 마스터 방식에서 제안한 작업본"
    ctx = catalog.shortlist(db, revision_id, link["item_id"], version=version,
                            scope=canonical(sorted(scope["selected_ids"])), configuration=config)
    if url == MANUAL:
        db.add_document(ANNOTATION_DOC, MANUAL, "Public pinned manual; locally curated annotation")
        db.add_source(ANNOTATION_DOC, "annotation.1", ANNOTATION, "curated paraphrase of fixed public manual; not upstream bytes")
        db.add_fragment("flow-initial", ANNOTATION_DOC, "annotation.1", 0, len(ANNOTATION), LOCATOR)
        successor = _successor(db.conn, ANNOTATION_DOC, "annotation.1")
        if successor:
            if successor[0] != "annotation.2":
                return None
            return SearchEntry(ctx, "파일 수집 " + CORRECTION, ("flow-correction",))
        fragment, kind, direction, text = "flow-initial", "direct", "refute", ANNOTATION
        edge = Relation(PRESERVE, "violates", fragment)
    else:
        db.add_document(MASTER_DOC, ARCHIVES, "National Archives, Preservation Master, main paragraphs 3–5")
        db.add_source(MASTER_DOC, "reading.1", MASTER_NOTE,
                      "curated paraphrase of Preservation Master, main paragraphs 3–5; not upstream bytes")
        # The locator is a public URL and a human-readable section, with no fabricated HTML fragment.
        db.add_fragment("flow-master", MASTER_DOC, "reading.1", 0, len(MASTER_NOTE), ARCHIVES + " · main paragraphs 3–5")
        fragment, kind, direction, text = "flow-master", "analogy", "support", TRANSFER
        edge = Relation(PRESERVE, "transfer_hypothesis", fragment)
    for req in eligible_req:
        claim_id = "flow-claim/" + digest(canonical([ctx, req["id"], fragment]))
        db.add_claim(claim_id, ctx, ctx, req["id"], kind, direction, fragment, text)
    return SearchEntry(ctx, text, (fragment,), (edge,))


def seed_catalog(db):
    """Register thin public metadata shared by every request, without allocating contexts or fetching bodies."""
    with db.transaction():
        catalog = Catalog(db.conn)
        direct = catalog.add(MANUAL, title="Paperless-ngx 파일 수집", form="feature")
        catalog.add_relation(direct, PRESERVE, "파일 수집 위치와 영구 보관 위치가 다르다",
                             "최초 폴더를 직접 소비하면 그 경로에 남지 않는다", LOCATOR, "curated manual annotation")
        master = catalog.add(ARCHIVES, title="NARA 보존 마스터", form="mechanism")
        catalog.add_relation(master, PRESERVE, "보존용 마스터에서 작업용 사본을 만든다",
                             "원래 파일 경로 및 중복 처리에는 별도 설계·검사가 필요하다",
                             ARCHIVES, "curated reading, main paragraphs 3–5; transfer remains a proposal")
        catalog.add(UNUSED)
        return direct, master


def retract_annotation(db):
    """Synthetic change to the reviewer's own annotation, never a change to the pinned upstream manual."""
    with db.transaction():
        db.add_source(ANNOTATION_DOC, "annotation.2", CORRECTION,
                      "synthetic review event; upstream commit unchanged", previous_key="annotation.1")
        db.add_fragment("flow-correction", ANNOTATION_DOC, "annotation.2", 0, len(CORRECTION), "fixture:flow-correction")


def answers_for_revision(db, revision_id):
    """List historical publications for the exact frozen request; performs no writes."""
    if not db.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='flow_answer'").fetchone():
        return []
    return [r[0] for r in db.conn.execute("SELECT operation_key FROM flow_answer WHERE request_revision_id=? ORDER BY rowid",
                                          (revision_id,))]


def main():
    with Ledger(":memory:") as db:
        seed_catalog(db)
        revision = ingest_scope(db, example_scope())
        initial = publish_answer(db, revision, "first")
        retract_annotation(db)
        updated = publish_answer(db, revision, "after-synthetic-review")
        def brief(answer):
            return {"request_revision": answer["request_revision_id"], "included": answer["included"],
                    "excluded": answer["excluded"], "candidates": [
                        {"context": item["title"], "url": item["url"], "proposal": item["proposal"],
                         "run": item["run_id"], "status": item["status"],
                         "conditions": {c["requirement_id"]:c["state"] for c in item["conditions"]}}
                        for item in answer["answers"]], "next_check": answer["next_check"]}
        print(json.dumps({"fixture":"offline; public-document paraphrase plus synthetic proposal and review",
                          "original":brief(initial),"original_today":answer_freshness(db,"first"),
                          "after_review":brief(updated)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
