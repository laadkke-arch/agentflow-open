"""Exercise the fixed Gallim round trip using two projects and immutable answer history."""
import json
import sqlite3

from prototype import SOURCE_CLAUSE, SYNONYM_CLAUSE, brief, request_scope


def table_counts(db):
    tables = [
        row[0] for row in db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    return {t: db.conn.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in tables}


def checked(db):
    assert [row[0] for row in db.conn.execute("PRAGMA integrity_check")] == ["ok"]
    assert not list(db.conn.execute("PRAGMA foreign_key_check"))


def lifecycle(path):
    from roundtrip import answer_freshness, publish_answer, read_answer, retract_annotation, seed_catalog
    from scope_input import example_scope, ingest_scope
    from store import Ledger, canonical, digest

    rows = []
    with Ledger(path) as db:
        seed_catalog(db)
        rev = ingest_scope(db, request_scope(example_scope, SOURCE_CLAUSE))
        first = publish_answer(db, rev, "first")
        original = brief(db, first)

        def record(event, before, answer=None, error=None, extra=None, baseline=original):
            persisted = brief(db, read_answer(db, "first"))
            assert persisted["answer_sha256"] == original["answer_sha256"]
            assert persisted["sources"] == original["sources"]
            checked(db)
            after = table_counts(db)
            receipt = {
                "event": event, "error": error, "before": before, "after": after,
                "past_sha256": persisted["answer_sha256"],
                "past_source_sha256": digest(canonical(persisted["sources"])),
                "reference_sha256": baseline["answer_sha256"],
                "new_sha256": answer["answer_sha256"] if answer else None,
                "new_source_sha256": digest(canonical(answer["sources"])) if answer else None,
                "new_candidates": [
                    [c["catalog_id"], c["candidate_context_id"], c["status"], c["used_citation_count"],
                     c["decision_output_sha256"]] for c in answer["candidates"]
                ] if answer else [],
                "changes": answer_freshness(db, "first"),
                "extra": extra,
            }
            rows.append(receipt)
            return receipt

        record("first_publication", {}, original)
        before = table_counts(db)
        replay_scope = ingest_scope(db, request_scope(example_scope, SOURCE_CLAUSE))
        replay = brief(db, publish_answer(db, replay_scope, "first"))
        assert record("same_scope_same_key", before, replay)["after"] == before
        assert replay == original

        new = request_scope(example_scope, SYNONYM_CLAUSE, revision="scope-r2", previous=rev)
        new_revision = ingest_scope(db, new)
        before = table_counts(db)
        try:
            publish_answer(db, new_revision, "first")
        except ValueError as exc:
            assert "operation key reused" in str(exc)
            assert record("different_revision_same_key", before, error=str(exc))["after"] == before
        else:
            raise AssertionError("reused key accepted")

        invalid = request_scope(example_scope, SOURCE_CLAUSE, revision="invalid", project="invalid")
        invalid["requirements"][0]["end_char"] += 1
        before = table_counts(db)
        try:
            ingest_scope(db, invalid)
        except ValueError as exc:
            assert "exact half-open Unicode span" in str(exc)
            assert record("invalid_coordinate", before, error=str(exc))["after"] == before
        else:
            raise AssertionError("invalid request span accepted")

        before = table_counts(db)
        revised = brief(db, publish_answer(db, new_revision, "changed-request"))
        record("new_request_revision", before, revised)
        actual = [{c["catalog_id"] for c in b["candidates"]} for b in (original, revised)]
        assert actual[0] == actual[1]

        before = table_counts(db)
        project_scope = request_scope(example_scope, SOURCE_CLAUSE, revision="p2-r1", project="p2")
        p2 = ingest_scope(db, project_scope)
        other = brief(db, publish_answer(db, p2, "project-two"))
        old_paper, new_paper = original["candidates"][0], other["candidates"][0]
        assert old_paper["catalog_id"] == new_paper["catalog_id"]
        assert old_paper["candidate_context_id"] != new_paper["candidate_context_id"]
        assert original["sources"] == other["sources"]
        record("different_project_same_candidate", before, other,
               extra={"catalog_id": new_paper["catalog_id"], "source_fragments": sorted(other["sources"]),
                      "context_ids": [old_paper["candidate_context_id"], new_paper["candidate_context_id"]]})

        before = table_counts(db)
        try:
            db.add_claim("cross-context-attempt", new_paper["candidate_context_id"], old_paper["candidate_context_id"],
                         "keep_source", "direct", "refute", "flow-initial", "synthetic cross-request relation")
        except sqlite3.IntegrityError as exc:
            assert record("invalid_cross_project_claim", before, error=str(exc))["after"] == before
        else:
            raise AssertionError("cross-request provenance accepted")

        before = table_counts(db)
        retract_annotation(db)
        new_source = brief(db, publish_answer(db, rev, "after-source-review"))
        assert "flow-correction" in new_source["sources"]
        assert "flow-initial" not in new_source["sources"]
        jobs = db.pending_jobs()
        assert jobs and all(job["revision_key"] == "annotation.2" for job in jobs)
        record("source_annotation_successor", before, new_source, extra={"pending_recheck_jobs": jobs})

        before = table_counts(db)
        old_after = brief(db, publish_answer(db, rev, "first"))
        assert old_after == original
        assert record("retry_historical_after_successor", before, old_after)["after"] == before

        before = table_counts(db)
        try:
            db.conn.execute("UPDATE flow_answer SET answer_json = ? WHERE operation_key = 'first'", ("{}",))
        except sqlite3.IntegrityError as exc:
            assert record("immutable_answer_trigger", before, error=str(exc))["after"] == before
        else:
            raise AssertionError("historical answer update accepted")
    return rows
