"""Public-synthetic input proposal; no project API, network or filesystem imports.

The caller supplies an explicitly shared, finite graph. "Whole" means every
component in that supplied graph; an upstream inventory is never inferred.
Neighbors provide context only. The caller supplies the accepted requirements.
"""

import json
from hashlib import sha256


def _fields(row, required, optional=()):
    if not isinstance(row, dict) or set(required) - row.keys() or row.keys() - set(required) - set(optional):
        raise ValueError(f"Expected fields {sorted(required)}; optional fields {sorted(optional)}")


def _text(value):
    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        raise ValueError("Expected nonempty text without NUL")
    return value


def _list(value):
    if not isinstance(value, list):
        raise ValueError("Expected a JSON array")
    return value


def _ids(values):
    values = _list(values)
    ids = {_text(value) for value in values}
    if len(ids) != len(values):
        raise ValueError("Duplicate IDs")
    return ids


def _validate(s):
    _fields(s, ("request_id", "revision_id", "mode", "goal", "components",
                "selected_ids", "excluded_ids", "edges", "requirements"),
            ("previous_id", "project_token", "plan_token"))
    for key in ("request_id", "revision_id", "goal", "previous_id", "project_token", "plan_token"):
        if key in s:
            _text(s[key])
    if s.get("previous_id") == s["revision_id"]:
        raise ValueError("A revision cannot be its own predecessor")

    for component in _list(s["components"]):
        _fields(component, ("id", "label"))
        _text(component["label"])
    components = _ids([c["id"] for c in s["components"]])
    selected, excluded = _ids(s["selected_ids"]), _ids(s["excluded_ids"])
    if not selected or not selected <= components or not excluded <= components or selected & excluded:
        raise ValueError("Select known components explicitly, disjoint from excluded IDs")
    if s["mode"] not in ("partial", "whole"):
        raise ValueError("Specify partial or whole explicitly")
    if s["mode"] == "whole" and selected != components:
        raise ValueError("Whole scope requires explicit selection of all supplied components")

    connected = set()
    for edge in _list(s["edges"]):
        _fields(edge, ("id", "source", "target", "kind", "payload"))
        endpoints = {_text(edge["source"]), _text(edge["target"])}
        if not endpoints <= components or not endpoints & selected or endpoints & excluded:
            raise ValueError("Edges must touch the selection and reference visible, known endpoints")
        if edge["kind"] not in ("data", "control", "ref"):
            raise ValueError("Unknown edge kind")
        _text(edge["payload"])
        connected.update(endpoints)
    _ids([e["id"] for e in s["edges"]])
    if components - selected - excluded - connected:
        raise ValueError("Each contextual neighbor needs an explicit edge to the selection")

    for req in _list(s["requirements"]):
        _fields(req, ("id", "label", "required", "start_char", "end_char", "quote", "component_ids"))
        _text(req["label"])
        if type(req["required"]) is not bool:
            raise ValueError("Specify required as true or false")
        applies = _ids(req["component_ids"])
        if not applies or not applies <= selected:
            raise ValueError("A requirement can apply only to explicitly selected components")
        start, end = req["start_char"], req["end_char"]
        if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(s["goal"])
                or s["goal"][start:end] != _text(req["quote"])):
            raise ValueError("Requirement quote must match its exact half-open Unicode span")
    if not _ids([r["id"] for r in s["requirements"]]):
        raise ValueError("Supply an accepted requirement")


def _schema(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS scope_snapshot (
        revision_id TEXT PRIMARY KEY NOT NULL REFERENCES request_revision(id),
        snapshot_json TEXT NOT NULL, sha256 TEXT NOT NULL CHECK(length(sha256)=64)
    )""")
    for operation in ("UPDATE", "DELETE"):
        conn.execute(f"""CREATE TRIGGER IF NOT EXISTS scope_snapshot_deny_{operation}
            BEFORE {operation} ON scope_snapshot
            BEGIN SELECT RAISE(ABORT,'immutable scope_snapshot'); END""")


def ingest_scope(db, snapshot):
    """Atomically create a request, requirements and frozen input. Keyed by revision ID."""
    raw = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    frozen = json.loads(raw)
    _validate(frozen)
    key = frozen["revision_id"]
    checksum = sha256(raw.encode()).hexdigest()
    with db.transaction():
        _schema(db.conn)
        old = db.conn.execute("SELECT snapshot_json FROM scope_snapshot WHERE revision_id=?", (key,)).fetchone()
        if old:
            if old[0] != raw:
                raise ValueError("Different scope content requires a new revision")
            return key
        if db.conn.execute("SELECT 1 FROM request_revision WHERE id=?", (key,)).fetchone():
            raise ValueError("Existing standalone request has no frozen scope; use a new revision")
        db.add_request(frozen["request_id"], key, frozen["goal"], frozen["requirements"],
                       previous_id=frozen.get("previous_id"))
        db.conn.execute("INSERT INTO scope_snapshot VALUES(?,?,?)", (key, raw, checksum))
    return key


def read_scope(db, revision_id):
    """Return the frozen content for this exact revision without following live relationships."""
    if db.conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='scope_snapshot'").fetchone():
        row = db.conn.execute("SELECT snapshot_json,sha256 FROM scope_snapshot WHERE revision_id=?",
                              (revision_id,)).fetchone()
        if row:
            if sha256(row[0].encode()).hexdigest() != row[1]:
                raise ValueError("Scope snapshot digest mismatch")
            return json.loads(row[0])
    raise KeyError(revision_id)


def example_scope():
    """New public-synthetic example, with no identifiers or messages from a real project."""
    goal = "파일을 수집하면서 최초 폴더의 파일을 삭제하거나 옮기지 않고, 재시도해도 중복 항목을 만들지 않는다."
    clauses = [
        ("keep_source", "최초 경로 유지", "최초 폴더의 파일을 삭제하거나 옮기지 않고"),
        ("no_duplicates", "재시도 중복 방지", "재시도해도 중복 항목을 만들지 않는다"),
    ]
    requirements = []
    for key, label, quote in clauses:
        start = goal.index(quote)
        requirements.append(dict(id=key, label=label, required=True, quote=quote,
                                 start_char=start, end_char=start + len(quote),
                                 component_ids=["intake"]))
    return dict(request_id="scope-request", revision_id="scope-r1", mode="partial", goal=goal,
                components=[{"id":"intake","label":"파일 수집"}, {"id":"folder","label":"최초 폴더"},
                            {"id":"ocr","label":"문자 인식"}],
                selected_ids=["intake"], excluded_ids=["ocr"],
                edges=[dict(id="input-file", source="folder", target="intake",
                            kind="data", payload="사용자가 넣은 PDF의 경로와 내용")],
                requirements=requirements)
