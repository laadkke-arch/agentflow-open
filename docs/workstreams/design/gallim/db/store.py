"""SQLite evidence ledger. All public writes are serialized, transactional, and retryable.

Offsets use Python Unicode character indices and half-open intervals. A source
capture can be a whole document or a named excerpt. Revision labels identify
captures within one document; SHA-256 hashes apply to their exact UTF-8 text.
"""

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


CONTEXT_QUERY = """
 SELECT c.id, c.request_revision_id, r.id AS subject, e.version, c.scope, c.configuration
 FROM candidate_context c JOIN edition e ON e.id=c.edition_id
 JOIN resource r ON r.id=e.resource_id WHERE c.id=?
"""
CONTEXT_FIELDS = ("subject", "version", "scope", "configuration")


class Ledger:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, isolation_level=None, timeout=15)
        self.conn.row_factory = sqlite3.Row
        try:
            self.conn.execute("PRAGMA foreign_keys=ON")
            self.conn.execute("PRAGMA recursive_triggers=ON")
            schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
            self.conn.executescript("BEGIN IMMEDIATE;\n" + schema + "\nCOMMIT;")
        except BaseException:
            self.conn.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.conn.close()

    @contextmanager
    def transaction(self):
        """Group public writes or a multi-step ingestion into one commit."""
        if self.conn.in_transaction:
            self.conn.execute("SAVEPOINT ledger_nested")
            try:
                yield
            except BaseException:
                self.conn.execute("ROLLBACK TO ledger_nested")
                raise
            finally:
                self.conn.execute("RELEASE ledger_nested")
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.conn.commit()
        except BaseException:
            self.conn.rollback()
            raise

    def _insert(self, table, key_columns, values):
        # Table/column names come only from the fixed call sites below.
        where = " AND ".join(f"{key}=?" for key in key_columns)
        cols = list(values)
        existing = self.conn.execute(
            f"SELECT {','.join(cols)} FROM {table} WHERE {where}",
            [values[k] for k in key_columns],
        ).fetchone()
        if existing:
            if dict(existing) != values:
                raise ValueError(f"{table}: identity already names different content")
            return False
        markers = ",".join("?" for _ in cols)
        self.conn.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({markers})", list(values.values()))
        return True

    def _one(self, sql, params):
        row = self.conn.execute(sql, params).fetchone()
        if row is None:
            raise KeyError(f"identity not found: {params!r}")
        return row

    def add_request(self, request_id, revision_id, original_text, requirements, previous_id=None):
        criteria = []
        for req in requirements:
            if not isinstance(req["required"], bool):
                raise ValueError("required must be boolean")
            start, end = req["start_char"], req["end_char"]
            if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(original_text):
                raise ValueError("invalid requirement anchor")
            criteria.append(dict(request_revision_id=revision_id, id=req["id"], label=req["label"],
                                 required=int(req["required"]), start_char=start, end_char=end))
        if not criteria or len({r["id"] for r in criteria}) != len(criteria):
            raise ValueError("at least one requirement and unique requirement IDs required")
        with self.transaction():
            created = self._insert("request_revision", ["id"], dict(id=revision_id, request_id=request_id,
                                   previous_id=previous_id, original_text=original_text))
            if not created:
                old = self.conn.execute("SELECT * FROM requirement WHERE request_revision_id=?", (revision_id,))
                if sorted(map(canonical, map(dict, old))) != sorted(map(canonical, criteria)):
                    raise ValueError("different requirements require a new request revision")
            for req in criteria:
                self._insert("requirement", ["request_revision_id", "id"], req)
        return revision_id

    def add_resource(self, id, subject, kind):
        with self.transaction():
            self._insert("resource", ["id"], dict(id=id, subject=subject, kind=kind))
        return id

    def add_edition(self, id, resource_id, version):
        with self.transaction():
            self._insert("edition", ["id"], dict(id=id, resource_id=resource_id, version=version))
        return id

    def add_context(self, id, request_revision_id, edition_id, scope, configuration):
        with self.transaction():
            self._insert("candidate_context", ["id"], dict(id=id, request_revision_id=request_revision_id,
                         edition_id=edition_id, scope=scope, configuration=configuration))
        return id

    def add_document(self, id, url, title):
        with self.transaction():
            self._insert("source_document", ["id"], dict(id=id, url=url, title=title))
        return id

    def add_source(self, document_id, revision_key, content, capture_scope, previous_key=None):
        """Publish one revision. An existing sibling rejects this write, never forks the lineage."""
        with self.transaction():
            added = self._insert("source_revision", ["document_id", "revision_key"],
                                 dict(document_id=document_id, revision_key=revision_key, content=content,
                                      sha256=digest(content), capture_scope=capture_scope, previous_key=previous_key))
            if added and previous_key is not None:
                self.conn.execute("""
                 WITH RECURSIVE affected(id) AS (
                   SELECT DISTINCT rc.run_id FROM run_claim rc
                   JOIN claim c ON c.id=rc.claim_id JOIN source_fragment f ON f.id=c.fragment_id
                   WHERE rc.eligibility='active' AND f.document_id=? AND f.revision_key=?
                   UNION
                   SELECT dp.run_id FROM decision_parent dp JOIN affected a ON dp.parent_id=a.id
                 )
                 INSERT INTO recheck_job(run_id,document_id,revision_key)
                 SELECT id,?,? FROM affected""", (document_id, previous_key, document_id, revision_key))
        return revision_key

    def add_fragment(self, id, document_id, revision_key, start_char, end_char, locator):
        with self.transaction():
            content = self._one("SELECT content FROM source_revision WHERE document_id=? AND revision_key=?",
                                (document_id, revision_key))["content"]
            if type(start_char) is not int or type(end_char) is not int or not 0 <= start_char < end_char <= len(content):
                raise ValueError("fragment outside captured source")
            self._insert("source_fragment", ["id"], dict(id=id, document_id=document_id, revision_key=revision_key,
                         start_char=start_char, end_char=end_char, sha256=digest(content[start_char:end_char]), locator=locator))
        return id

    def add_claim(self, id, context_id, evidence_context_id, requirement_id, kind, direction, fragment_id, assertion):
        with self.transaction():
            revision = self._one(CONTEXT_QUERY, (context_id,))["request_revision_id"]
            self._insert("claim", ["id"], dict(id=id, context_id=context_id, evidence_context_id=evidence_context_id,
                         request_revision_id=revision, requirement_id=requirement_id, kind=kind,
                         direction=direction, fragment_id=fragment_id, assertion=assertion))
        return id

    def _inputs(self, context_id):
        target = self._one(CONTEXT_QUERY, (context_id,))
        candidate = dict(id=context_id, context={field: target[field] for field in CONTEXT_FIELDS})
        criteria = []
        for row in self.conn.execute(
            "SELECT id,label,required,start_char,end_char FROM requirement WHERE request_revision_id=? ORDER BY start_char,id",
            (target["request_revision_id"],)
        ):
            criteria.append(dict(dict(row), required=bool(row["required"])))
        claims, eligibility = [], []
        rows = self.conn.execute("""
          SELECT c.*, r.id AS subject, e.version, ctx.scope, ctx.configuration,
                 f.document_id, f.revision_key, f.locator, f.sha256,
                 NOT EXISTS(SELECT 1 FROM source_revision newer WHERE newer.document_id=f.document_id
                            AND newer.previous_key=f.revision_key) AS active
          FROM claim c JOIN candidate_context ctx ON ctx.id=c.evidence_context_id
          JOIN edition e ON e.id=ctx.edition_id JOIN resource r ON r.id=e.resource_id
          JOIN source_fragment f ON f.id=c.fragment_id WHERE c.context_id=? ORDER BY c.id
        """, (context_id,))
        for row in rows:
            eligibility.append((row["id"], "active" if row["active"] else "superseded"))
            if row["active"]:
                claims.append(dict(id=row["id"], candidate=row["context_id"], criterion=row["requirement_id"],
                                   context={k: row[k] for k in CONTEXT_FIELDS}, kind=row["kind"],
                                   direction=row["direction"], locator=row["locator"], assertion=row["assertion"],
                                   fragment_id=row["fragment_id"], document_id=row["document_id"],
                                   source_revision=row["revision_key"], fragment_sha256=row["sha256"]))
        return dict(candidate=candidate, criteria=criteria, claims=claims), eligibility

    def publish_decision(self, context_id, operation_key, evaluator, evaluator_version, parents=(), resolve_jobs=()):
        """Retry a key to recover its original result. Use a fresh key for a changed evidence set.

        Parents express declared provenance for invalidation. They are not extra supporting claims.
        An evaluator must be deterministic and must not perform I/O or mutate the supplied maps.
        """
        if not operation_key or not evaluator_version:
            raise ValueError("operation key and evaluator version required")
        parents, jobs = sorted(set(parents)), sorted(set(resolve_jobs))
        command_hash = digest(canonical([context_id, evaluator_version, parents, jobs]))
        with self.transaction():
            prior = self.conn.execute("SELECT id,command_hash FROM decision_run WHERE operation_key=?",
                                      (operation_key,)).fetchone()
            if prior:
                if prior["command_hash"] != command_hash:
                    raise ValueError("operation_key already used for another command")
                return prior["id"]
            for parent in parents:
                self._one("SELECT id FROM decision_run WHERE id=?", (parent,))
                if self.conn.execute("SELECT 1 FROM recheck_job WHERE run_id=? LIMIT 1", (parent,)).fetchone():
                    raise ValueError("superseded parent: use its reevaluated replacement")
            for job in jobs:
                target = self._one("""
                  SELECT d.context_id FROM recheck_job j JOIN decision_run d ON d.id=j.run_id
                  WHERE j.id=? AND NOT EXISTS (SELECT 1 FROM recheck_resolution z WHERE z.job_id=j.id)""", (job,))
                if target["context_id"] != context_id:
                    raise ValueError("recheck job belongs to a different context")
                for old in self.conn.execute("""
                    SELECT p.parent_id FROM recheck_job j JOIN decision_parent p ON p.run_id=j.run_id
                    WHERE j.id=?""", (job,)):
                    # Keep valid parents, or require their explicitly recomputed descendants.
                    replacements = self.conn.execute("""
                      WITH RECURSIVE valid(id) AS (
                        SELECT ? UNION SELECT z.replacement_run_id FROM valid v
                        JOIN recheck_job j ON j.run_id=v.id JOIN recheck_resolution z ON z.job_id=j.id
                      ) SELECT id FROM valid""", (old["parent_id"],))
                    if not set(parents).intersection(r["id"] for r in replacements):
                        raise ValueError("recheck must retain each parent or its reevaluated replacement")
            inputs, eligibility = self._inputs(context_id)
            snapshot = canonical(inputs)
            outcome = evaluator(**inputs)
            if set(outcome["criteria"]) != {row["id"] for row in inputs["criteria"]}:
                raise ValueError("evaluator must return exactly the request requirements")
            run_id = self.conn.execute("""
                INSERT INTO decision_run(operation_key,command_hash,context_id,evaluator_version,input_json,output_json,status)
                VALUES(?,?,?,?,?,?,?)""", (operation_key, command_hash, context_id, evaluator_version,
                                           snapshot, canonical(outcome), outcome["status"])).lastrowid
            for criterion, detail in outcome["criteria"].items():
                allowed_claims = {row["id"] for row in inputs["claims"] if row["criterion"] == criterion}
                if not set(detail["used"]) <= allowed_claims:
                    raise ValueError("used claim absent from the active input for this criterion")
                self.conn.execute("INSERT INTO decision_item VALUES (?,?,?,?)",
                                  (run_id, criterion, detail["state"], canonical(detail)))
            self.conn.executemany("INSERT INTO run_claim VALUES (?,?,?)", [(run_id,*row) for row in eligibility])
            self.conn.executemany("INSERT INTO decision_parent VALUES (?,?)", [(run_id,p) for p in parents])
            self.conn.executemany("INSERT INTO recheck_resolution VALUES (?,?)", [(j,run_id) for j in jobs])
            return run_id

    def get_decision(self, run_id):
        row = dict(self._one("""SELECT d.*,c.request_revision_id FROM decision_run d
                            JOIN candidate_context c ON c.id=d.context_id WHERE d.id=?""", (run_id,)))
        row["input"], row["output"] = json.loads(row.pop("input_json")), json.loads(row.pop("output_json"))
        return row

    def pending_jobs(self, run_id=None):
        rows = self.conn.execute("""
          SELECT j.* FROM recheck_job j LEFT JOIN recheck_resolution z ON z.job_id=j.id
          WHERE z.job_id IS NULL AND (? IS NULL OR j.run_id=?) ORDER BY j.id""", (run_id,run_id))
        return list(map(dict,rows))


def main():
    parser = argparse.ArgumentParser(description="Inspect an offline SQLite evidence ledger (UTF-8 JSON).")
    parser.add_argument("database", type=Path)
    interface = parser.add_subparsers(dest="command", required=True)
    interface.add_parser("init")
    interface.add_parser("jobs")
    decision = interface.add_parser("decision")
    decision.add_argument("run_id", type=int)
    args = parser.parse_args()
    if args.command != "init" and not args.database.is_file():
        parser.error("database does not exist")
    with Ledger(args.database) as db:
        if args.command == "init":
            result = {"database": str(args.database), "initialized": True}
        elif args.command == "jobs":
            result = db.pending_jobs()
        else:
            result = db.get_decision(args.run_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
