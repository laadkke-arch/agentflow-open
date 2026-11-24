"""Trace the frozen gallim prototype through its unchanged public entry points."""
import json
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

PIN = "fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c"
PROTOTYPE = "docs/workstreams/design/gallim/db/"


def digest(data):
    return sha256(data).hexdigest()


def materialize(output):
    target = output / "prototype-src"
    target.mkdir()
    files = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", PIN, PROTOTYPE], text=True)
    hashes = {}
    for file in files.splitlines():
        name = Path(file).name
        if Path(name).suffix not in {".py", ".sql", ".json"}:
            continue
        body = subprocess.check_output(["git", "show", f"{PIN}:{file}"])
        (target / name).write_bytes(body)
        hashes[name] = digest(body)
    sys.path.insert(0, str(target))
    return hashes


def run(output):
    hashes = materialize(output)
    import roundtrip as rt   # Frozen upstream; loaded from the local Git objects above.

    cases = []
    for synthetic in (False, True):
        for budget in (2, 3):
            name = f"{'synthetic' if synthetic else 'plain'}-{budget}"
            trace = []
            original_discover = rt.Catalog.discover
            original_inspect = rt._inspect_public_fixture
            original_search = rt.search
            original_decision = rt.Ledger.publish_decision

            def discover(catalog, query, *, operations, limit):
                result = original_discover(catalog, query, operations=operations, limit=limit)
                trace.append({"stage": "first_search", "limit": limit, "ids": [r["item_id"] for r in result]})
                return result

            def inspect(db, catalog, item, scope):
                result = original_inspect(db, catalog, item, scope)
                trace.append({"stage": "fixture_inspection", "id": item["item_id"], "url": item["url"],
                              "context": None if result is None else result.context_id,
                              "fragments": [] if result is None else list(result.source_ids)})
                return result

            def search(*args, **kwargs):
                result = original_search(*args, **kwargs)
                trace.append({"stage": "second_search", "limit": kwargs["budget"],
                              "contexts": [r["context_id"] for r in result["hits"]]})
                return result

            def decision(db, context, *args, **kwargs):
                result = original_decision(db, context, *args, **kwargs)
                trace.append({"stage": "decision", "context": context, "decision_id": result})
                return result

            db_path = output / f"{name}.sqlite"
            with rt.Ledger(db_path) as db:
                paperless, nara = rt.seed_catalog(db)
                catalog = rt.Catalog(db.conn)
                scope = rt.example_scope()
                revision = rt.ingest_scope(db, scope)
                query = rt._query(rt.read_scope(db, revision))
                if synthetic:
                    with db.transaction():
                        synthetic_id = catalog.add(rt.UNUSED, title="합성 교정 " + query, form="feature")
                        catalog.add_relation(synthetic_id, rt.PRESERVE, "합성 순위 교정", "원문 미판독",
                                             rt.UNUSED, "synthetic calibration only")
                else:
                    synthetic_id = None
                registered = db.conn.execute("SELECT id FROM catalog_link ORDER BY id").fetchall()
                all_matches = original_discover(catalog, query, operations=rt.infer_mechanisms(query), limit=100)
                trace.extend([{"stage": "registered", "ids": [r[0] for r in registered]},
                              {"stage": "scope_ingested", "revision": revision},
                              {"stage": "publish_call", "operation": name, "budget": budget}])
                if synthetic:
                    assert all_matches[0]["item_id"] == synthetic_id
                assert set(r["item_id"] for r in all_matches) == (
                    {paperless, nara, synthetic_id} if synthetic else {paperless, nara}
                )
                with patch.object(rt.Catalog, "discover", discover), patch.object(rt, "_inspect_public_fixture", inspect), \
                     patch.object(rt, "search", search), patch.object(rt.Ledger, "publish_decision", decision):
                    answer = rt.publish_answer(db, revision, name, budget)
                assert len(answer["catalog_shortlist"]) == min(budget, len(all_matches))
            with rt.Ledger(db_path) as reopened:
                persisted = rt.read_answer(reopened, name)
                assert persisted == answer
                saved_hash = reopened.conn.execute(
                    "SELECT answer_sha256 FROM flow_answer WHERE operation_key=?", (name,)
                ).fetchone()[0]
                source_bytes = reopened.conn.execute(
                    "SELECT COALESCE(SUM(LENGTH(CAST(content AS BLOB))),0) FROM source_revision"
                ).fetchone()[0]
            trace.append({"stage": "answer_saved_and_reopened", "ids": [r["catalog_item"] for r in persisted["answers"]],
                          "answer_sha256": saved_hash})
            cases.append({"case": name, "display_budget": budget, "synthetic_only": synthetic,
                          "synthetic_id": synthetic_id, "paperless_id": paperless, "nara_id": nara,
                          "matching_catalog": all_matches, "trace": trace, "persisted_source_note_bytes": source_bytes,
                          "prototype_source_kind": "offline curated notes; upstream network opens = 0",
                          "answer": answer})
    return {"commit": PIN, "source_file_sha256": hashes, "cases": cases}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py EMPTY_OUTPUT_DIRECTORY")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True)
    payload = run(output)
    (output / "prototype.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    for row in payload["cases"]:
        answer = row["answer"]
        print(row["case"], [r["item_id"] for r in answer["catalog_shortlist"]],
              [(r["catalog_item"], r["status"]) for r in answer["answers"]],
              [r["item_id"] for r in answer["uninspected"]])


if __name__ == "__main__":
    main()
