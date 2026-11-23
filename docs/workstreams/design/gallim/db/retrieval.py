"""Offline candidate discovery. Ranks propose items for inspection; the store owns judgments."""
import argparse
import json
import re
import sqlite3
import unicodedata
from collections import defaultdict
from dataclasses import dataclass

PRESERVE = "preserve-source-at-original-path"
RETAIN = "preserve-success-after-later-failure"
DEDUP = "prevent-duplicate-entry"
MAX_QUERY_CHARS = 65536
MAX_QUERY_TERMS = 512
EDGE_KINDS = {"implements", "violates", "transfer_hypothesis", "control"}


@dataclass(frozen=True)
class Relation:
    mechanism: str
    kind: str
    source_id: str


@dataclass(frozen=True)
class SearchEntry:
    context_id: str
    text: str
    source_ids: tuple
    relations: tuple = ()


CONTEXTS = """SELECT c.id, r.id, r.subject, r.kind, c.request_revision_id
              FROM candidate_context c JOIN edition e ON c.edition_id=e.id
              JOIN resource r ON r.id=e.resource_id"""


def rebuild_index(conn, entries, *, request_revision_id=None):
    """Replace the whole derivative index, or only contexts belonging to one revision."""
    conn.execute("SAVEPOINT retrieval_rebuild")
    try:
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS retrieval_text USING fts5("
                     "context_id UNINDEXED, title, body, source_ids UNINDEXED, tokenize='unicode61')")
        conn.execute("""CREATE TABLE IF NOT EXISTS retrieval_edge(
            context_id TEXT NOT NULL REFERENCES candidate_context(id), mechanism TEXT NOT NULL,
            kind TEXT NOT NULL, source_id TEXT NOT NULL REFERENCES source_fragment(id),
            PRIMARY KEY(context_id,mechanism,kind,source_id))""")
        conn.execute("CREATE INDEX IF NOT EXISTS retrieval_edge_type ON retrieval_edge(mechanism,kind)")
        if request_revision_id is None:
            context_rows = conn.execute(CONTEXTS)
        else:
            context_rows = conn.execute(CONTEXTS + " WHERE c.request_revision_id=?", (request_revision_id,))
        contexts = {row[0]: row[2] for row in context_rows}
        fragments = {row[0] for row in conn.execute("SELECT id FROM source_fragment")}
        docs = defaultdict(set)
        edges = set()
        for entry in entries:
            if entry.context_id not in contexts:
                raise ValueError("unknown canonical context: " + entry.context_id)
            ids = set(entry.source_ids)
            if not entry.text.strip() or not ids or ids - fragments:
                raise ValueError("index text needs known source fragment IDs: " + entry.context_id)
            docs[entry.context_id, entry.text].update(ids)
            for edge in entry.relations:
                if edge.kind not in EDGE_KINDS or not edge.mechanism or edge.source_id not in ids:
                    raise ValueError("invalid typed relation or fragment outside entry")
                edges.add((entry.context_id, edge.mechanism, edge.kind, edge.source_id))
        if request_revision_id is None:
            conn.execute("DELETE FROM retrieval_text")
            conn.execute("DELETE FROM retrieval_edge")
        else:
            in_revision = " WHERE context_id IN (SELECT id FROM candidate_context WHERE request_revision_id=?)"
            conn.execute("DELETE FROM retrieval_text" + in_revision, (request_revision_id,))
            conn.execute("DELETE FROM retrieval_edge" + in_revision, (request_revision_id,))
        conn.executemany("INSERT INTO retrieval_text VALUES(?,?,?,?)", (
            (context_id, contexts[context_id], body, json.dumps(sorted(ids), ensure_ascii=False))
            for (context_id, body), ids in sorted(docs.items())))
        conn.executemany("INSERT INTO retrieval_edge VALUES(?,?,?,?)", sorted(edges))
    except BaseException:
        conn.execute("ROLLBACK TO retrieval_rebuild")
        raise
    finally:
        conn.execute("RELEASE retrieval_rebuild")


def infer_mechanisms(query):
    """Small disclosed dictionary for these fixtures. Unmatched wording retains lexical recall."""
    q = unicodedata.normalize("NFKC", query).casefold()
    inferred = []
    rejects_preservation = re.search(r"(?:do not|don't|never) (?:keep|preserve|retain)|"
                                     r"(?:보존|유지)하지 (?:말|않)|보존할 필요.{0,3}없", q)
    if not rejects_preservation and re.search(r'original|source file|원본|원래|(?:최초|처음).{0,16}(?:폴더|경로|위치)', q) and re.search(
            r'preserv|retain|keep|do not (?:move|delete)|without (?:moving|deleting)|'
            r'보존|유지|그대로|(?:삭제하|제거하|이동하|옮기)지\s*(?:않|말)|'
            r'(?:삭제|제거|이동|옮기기)(?:를)?\s*금지', q):
        inferred.append(PRESERVE)
    if not rejects_preservation and re.search(r'success|completed|성공|완료', q) and re.search(r'fail|error|실패|오류', q) and re.search(
            r'keep|preserv|retain|do not roll back|유지|보존|남기|남겨|취소하지', q):
        inferred.append(RETAIN)
    if re.search(r'중복.{0,22}(?:방지|막|제외|금지|않|없|한 번|하나)|deduplicat|'
                 r'(?:prevent|avoid|without|no) duplicate|only once', q):
        inferred.append(DEDUP)
    return inferred


def search(conn, raw_query, mechanism=None, budget=3, request_revision_id=None):
    """Search a published derivative index. Budget caps displayed contexts, not database work."""
    if not isinstance(raw_query, str) or isinstance(budget, bool) or not isinstance(budget, int) or budget < 0:
        raise ValueError("query must be text and budget a nonnegative integer")
    if len(raw_query) > MAX_QUERY_CHARS:
        raise ValueError(f"query exceeds {MAX_QUERY_CHARS} Unicode characters; select a smaller search scope")
    mechanisms = ([mechanism] if isinstance(mechanism, str) else list(mechanism)
                  if mechanism is not None else infer_mechanisms(raw_query))
    mechanisms = list(dict.fromkeys(mechanisms))
    q = unicodedata.normalize("NFKC", raw_query).casefold()
    terms = list(dict.fromkeys(re.findall(r'[^\W_]+', q, flags=re.UNICODE)))
    if len(terms) > MAX_QUERY_TERMS:
        raise ValueError(f"query exceeds {MAX_QUERY_TERMS} distinct lexical terms; select a smaller search scope")
    ctx_rows = conn.execute(CONTEXTS + (" WHERE c.request_revision_id=?" if request_revision_id is not None else ""),
                            (request_revision_id,) if request_revision_id is not None else ())
    contexts = {row[0]: row for row in ctx_rows}
    lexical, typed = {}, defaultdict(list)
    if terms:
        # Tokens are quoted individually. Query text, including negation, never becomes FTS syntax.
        expression = " OR ".join('"' + term + '"' for term in terms)
        matches = conn.execute("""SELECT context_id,source_ids FROM retrieval_text
                                  WHERE retrieval_text MATCH ?
                                  ORDER BY bm25(retrieval_text,0,2,1,0),context_id,rowid""", (expression,))
        for cid, sources in matches:
            if cid in contexts:
                lexical.setdefault(cid, set()).update(json.loads(sources))
    # Controls get no positive graph route. They can still be retrieved and inspected lexically.
    for m in mechanisms:
        for cid, kind, sid in conn.execute("""SELECT context_id,kind,source_id FROM retrieval_edge
            WHERE mechanism=? AND kind<>'control' ORDER BY context_id,kind,source_id""", (m,)):
            if cid in contexts:
                typed[cid].append({"route": "mechanism", "mechanism": m, "relation": kind, "source_id": sid})
    candidates = list(dict.fromkeys([*lexical, *typed]))
    analogy = {cid for cid, routes in typed.items() if any(r["relation"] == "transfer_hypothesis" for r in routes)}
    direct = [cid for cid in candidates if cid not in analogy]
    # A typed contradiction is as eligible for inspection as a typed positive relation.
    direct.sort(key=lambda cid: cid not in typed)
    chosen = direct[:1] if budget else []
    seen_resources = {contexts[cid][1] for cid in chosen}
    hypotheses = [cid for cid in candidates if cid in analogy]
    if hypotheses and len(chosen) < budget:
        preferred = next((cid for cid in hypotheses if contexts[cid][1] not in seen_resources), hypotheses[0])
        chosen.append(preferred)
        seen_resources.add(contexts[preferred][1])
    for enforce_diversity in (True, False):
        for cid in candidates:
            if len(chosen) >= budget:
                break
            rid = contexts[cid][1]
            if cid not in chosen and (not enforce_diversity or rid not in seen_resources):
                chosen.append(cid)
                seen_resources.add(rid)
    hits = []
    for cid in chosen:
        _, rid, title, kind, revision = contexts[cid]
        routes = []
        if cid in lexical:
            routes.append({"route": "lexical", "source_ids": sorted(lexical[cid])})
        routes.extend(typed.get(cid, []))
        sources = set(lexical.get(cid, [])) | {r["source_id"] for r in typed.get(cid, [])}
        hits.append({"context_id": cid, "resource_id": rid, "title": title, "kind": kind,
                     "request_revision_id": revision, "routes": routes, "source_ids": sorted(sources),
                     "verification": "unverified"})
    return {"query": raw_query, "query_terms": terms, "mechanisms": mechanisms,
            "mechanism_origin": "supplied" if mechanism is not None else "fixture_dictionary",
            "budget": budget, "hits": hits, "trace": {"lexical_contexts": len(lexical),
            "typed_contexts": len(typed), "distinct_contexts": len(candidates),
            "displayed": len(hits), "budget_unit": "displayed_contexts"}}


def demo_fixture():
    """Isolated synthetic source fragments and canonical IDs, never historical product judgments."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""CREATE TABLE resource(id TEXT PRIMARY KEY,subject TEXT,kind TEXT);
        CREATE TABLE edition(id TEXT PRIMARY KEY,resource_id TEXT,version TEXT);
        CREATE TABLE candidate_context(id TEXT PRIMARY KEY,request_revision_id TEXT,edition_id TEXT);
        CREATE TABLE source_fragment(id TEXT PRIMARY KEY);""")
    cases = [
        ("scan", "box", "Synthetic inbox", "implementation", "Scan PDF for search. A duplicate digest prevents another entry. Consumption removes the original folder input.",
         [(PRESERVE, "violates"), (DEDUP, "implements")]),
        ("scan", "museum", "Collection handling", "principle", "A master remains accessioned while surrogates circulate.",
         [(PRESERVE, "transfer_hypothesis")]),
        ("scan", "same", "Search catalogue", "control", "scan PDF, search, original, duplicate",
         [(PRESERVE, "control")]),
        ("batch", "rollback", "Transaction wrapper", "implementation", "batch success failure, keep results, roll back group",
         [(RETAIN, "violates")]),
        ("batch", "ledger", "Parcel receipts", "principle", "Individual consignments close irrevocably.",
         [(RETAIN, "transfer_hypothesis")]),
        ("batch", "dashboard", "Statistics display", "control", "success failure batch",
         [(RETAIN, "control")]),
    ]
    entries = []
    for req, cid, title, kind, body, rels in cases:
        conn.execute("INSERT INTO resource VALUES(?,?,?)", (cid, title, kind))
        conn.execute("INSERT INTO edition VALUES(?,?,?)", (cid, cid, "fixture"))
        conn.execute("INSERT INTO candidate_context VALUES(?,?,?)", (cid, req, cid))
        sid = cid + "-fragment"
        conn.execute("INSERT INTO source_fragment VALUES(?)", (sid,))
        entries.append(SearchEntry(cid, body, (sid,), tuple(Relation(m,k,sid) for m,k in rels)))
    rebuild_index(conn, entries)
    return conn, entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true")
    mode.add_argument("--db")
    parser.add_argument("--query")
    parser.add_argument("--mechanism", action="append")
    parser.add_argument("--revision")
    parser.add_argument("--budget", type=int, default=3)
    args = parser.parse_args()
    if args.demo:
        conn, _ = demo_fixture()
        examples = [("scan", "scan PDF search and keep original folder; prevent duplicate entry"),
                    ("batch", "keep batch success after later failure")]
        output = {"fixture": "synthetic retrieval cases; no verified product outcomes",
                  "cases": [search(conn, q, budget=args.budget, request_revision_id=r) for r,q in examples]}
    else:
        if args.query is None:
            parser.error("--db requires --query and a previously rebuilt index")
        from pathlib import Path
        conn = sqlite3.connect(Path(args.db).resolve().as_uri() + "?mode=ro", uri=True)
        output = search(conn, args.query, args.mechanism, args.budget, args.revision)
    conn.close()
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
