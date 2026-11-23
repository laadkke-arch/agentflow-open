"""Small reusable link catalog. SQLite + Python only, no fetching or fact grading."""

from contextlib import contextmanager
import hashlib
import ipaddress
import json
import re
from urllib.parse import unquote, urlsplit, urlunsplit


SCHEMA = (
    """CREATE TABLE IF NOT EXISTS catalog_link (
       id TEXT PRIMARY KEY NOT NULL, canonical_url TEXT NOT NULL UNIQUE,
       title TEXT, form TEXT, note TEXT, provenance TEXT)""",
    """CREATE TABLE IF NOT EXISTS catalog_alias (
       original_url TEXT PRIMARY KEY NOT NULL, item_id TEXT NOT NULL REFERENCES catalog_link(id))""",
    """CREATE TABLE IF NOT EXISTS catalog_relation (
       id TEXT PRIMARY KEY NOT NULL, item_id TEXT NOT NULL REFERENCES catalog_link(id),
       operation TEXT NOT NULL, operation_key TEXT NOT NULL, invariant TEXT NOT NULL, breaks_at TEXT NOT NULL,
       locator TEXT NOT NULL, provenance TEXT NOT NULL)""",
    """CREATE INDEX IF NOT EXISTS catalog_op ON catalog_relation(operation_key,item_id)""",
    """CREATE TABLE IF NOT EXISTS catalog_term (
       term TEXT NOT NULL, item_id TEXT NOT NULL REFERENCES catalog_link(id), PRIMARY KEY(term,item_id))""",
    """CREATE INDEX IF NOT EXISTS catalog_item_terms ON catalog_term(item_id)""",
    """CREATE INDEX IF NOT EXISTS catalog_item_relations ON catalog_relation(item_id)""",
    """CREATE INDEX IF NOT EXISTS catalog_item_aliases ON catalog_alias(item_id)""",
)
FORMS = {"oss", "website", "service", "feature", "mechanism", "other"}
URL_STOP = {"https", "http", "www", "com", "org", "net", "io", "github", "blob", "tree", "html", "md"}
UNKNOWN = "현재 요청의 설정에서 작동·보존 여부는 미확인입니다."


def _id(prefix, parts):
    data = json.dumps(parts, ensure_ascii=False, separators=(",", ":")).encode()
    return prefix + hashlib.sha256(data).hexdigest()[:24]


def canonical_url(value):
    """Only normalize scheme, host case and default ports. Keep path, query, fragment and their case."""
    if not isinstance(value, str) or not value or value.strip() != value or any(
        char.isspace() or ord(char)<32 or ord(char)==127 for char in value
    ) or "\\" in value:
        raise ValueError("expected an absolute HTTP(S) URL without whitespace")
    p = urlsplit(value)
    host = p.hostname
    if p.scheme not in ("http","https") or not host or p.username is not None or p.password is not None:
        raise ValueError("expected a public HTTP(S) URL without embedded credentials")
    if host.rstrip(".") == "localhost" or host.rstrip(".").endswith((".localhost",".local")):
        raise ValueError("local host")
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        addr = None
    if addr is not None and not addr.is_global:
        raise ValueError("non-public IP address")
    # Abort on invalid/out-of-range port through SplitResult.port.
    port = p.port
    host = f"[{host}]" if ":" in host else host
    if port is not None and port != {"http":80,"https":443}[p.scheme]:
        host += f":{port}"
    # urlunsplit elides explicit empty query/fragment markers. Preserve their
    # presence as well; aliases must not silently change opaque resource keys.
    result = urlunsplit((p.scheme,host,p.path,p.query,p.fragment))
    if "?" in value.split("#",1)[0] and not p.query:
        before, sep, after = result.partition("#")
        result = before + "?" + sep + after
    if "#" in value and not p.fragment:
        result += "#"
    return result


def words(value):
    return set(re.findall(r"[^\W_]+", value.casefold()))


def _op(value):
    return " ".join(value.casefold().split())


def _text(value, name):
    if not isinstance(value,str) or not value.strip():
        raise ValueError(f"nonempty {name} required")
    return value.strip()


def _dicts(cursor):
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns,row)) for row in cursor]


@contextmanager
def _atomic(conn):
    nested = conn.in_transaction
    conn.execute("SAVEPOINT catalog_change" if nested else "BEGIN IMMEDIATE")
    try:
        yield
        if not nested:
            conn.commit()
    except BaseException:
        if nested:
            conn.execute("ROLLBACK TO catalog_change")
        else:
            conn.rollback()
        raise
    finally:
        if nested:
            conn.execute("RELEASE catalog_change")


class Catalog:
    def __init__(self, conn):
        self.conn = conn
        with _atomic(conn):
            for statement in SCHEMA:
                conn.execute(statement)

    def add(self, url, *, title=None, form=None, note=None, provenance=None):
        """An original URL alone is sufficient. Optional enrichment fills in unknown fields."""
        normalized = canonical_url(url)
        item = _id("link-",[normalized])
        if form is not None and form not in FORMS:
            raise ValueError(f"unsupported form: {form}")
        values = dict(title=title,form=form,note=note,provenance=provenance)
        for key,value in values.items():
            if value is not None:
                values[key] = _text(value,key)
        if note is not None and provenance is None:
            raise ValueError("attach a provenance label when adding a curator note")
        with _atomic(self.conn):
            self.conn.execute("""INSERT INTO catalog_link(id,canonical_url) VALUES(?,?)
                                ON CONFLICT(canonical_url) DO NOTHING""", (item,normalized))
            present = _dicts(self.conn.execute("SELECT * FROM catalog_link WHERE id=?",(item,)))[0]
            for field,value in values.items():
                if value is not None and present[field] is not None and value != present[field]:
                    raise ValueError(f"existing {field} differs; preserve the original record")
            self.conn.execute(
                """UPDATE catalog_link SET title=coalesce(title,?),form=coalesce(form,?),
                          note=coalesce(note,?),provenance=coalesce(provenance,?) WHERE id=?""",
                (values["title"],form,values["note"],values["provenance"],item))
            self.conn.execute("""INSERT INTO catalog_alias VALUES(?,?) ON CONFLICT(original_url) DO NOTHING""",
                              (url,item))
            terms = words(unquote(normalized)) - URL_STOP
            terms.update(words(values["title"] or present["title"] or ""))
            self.conn.executemany("INSERT OR IGNORE INTO catalog_term VALUES(?,?)",
                                  [(term,item) for term in sorted(terms)])
        return item

    def add_relation(self, item_id, operation, invariant, breaks_at, locator, provenance):
        """A curated mechanism requires a source pointer, invariant and explicit boundary."""
        operation,invariant,breaks_at,locator,provenance = [
            _text(v,n) for n,v in zip(("operation","invariant","breaks_at","locator","provenance"),
                                      (operation,invariant,breaks_at,locator,provenance))]
        canonical_url(locator)
        key = _op(operation)
        identity = _id("rel-",[item_id,key,invariant,breaks_at,locator,provenance])
        with _atomic(self.conn):
            if not self.conn.execute("SELECT 1 FROM catalog_link WHERE id=?",(item_id,)).fetchone():
                raise KeyError(item_id)
            self.conn.execute("""INSERT INTO catalog_relation VALUES(?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO NOTHING""",
                (identity,item_id,operation,key,invariant,breaks_at,locator,provenance))
        return identity

    def get(self, item_id):
        records = _dicts(self.conn.execute("SELECT * FROM catalog_link WHERE id=?",(item_id,)))
        if not records:
            raise KeyError(item_id)
        result = records[0]
        result["item_id"] = result.pop("id")
        result["aliases"] = [r[0] for r in self.conn.execute(
            "SELECT original_url FROM catalog_alias WHERE item_id=? ORDER BY rowid",(item_id,))]
        result["url"] = result["aliases"][0]
        result["form"] = result["form"] or "unknown"
        result["relations"] = _dicts(self.conn.execute("""
          SELECT operation,invariant,breaks_at,locator,provenance FROM catalog_relation
          WHERE item_id=? ORDER BY operation_key,id""", (item_id,)))
        return result

    def discover(self, query, *, operations=(), limit=12):
        """Return reusable entry IDs even for a request that has never been ingested."""
        if not isinstance(query,str) or type(limit) is not int or not 1<=limit<=100:
            raise ValueError("text query and limit from 1 to 100 required")
        if isinstance(operations,str):
            raise TypeError("pass operation labels as an iterable, not a string")
        terms = sorted(words(query))
        operations = sorted({_op(_text(v,"operation")) for v in operations})
        # The temp-free JSON table parameters avoid variable-count limits.
        rows = _dicts(self.conn.execute("""
          WITH evidence AS (
            SELECT t.item_id AS id,'term' AS reason,t.term AS matched_value FROM catalog_term t
            JOIN json_each(?) q ON t.term=q.value
            UNION
            SELECT r.item_id,'operation',r.operation_key FROM catalog_relation r
            JOIN json_each(?) q ON r.operation_key=q.value
          )
          SELECT id, sum(reason='operation') AS op_count, sum(reason='term') AS word_count,
                 json_group_array(json_array(reason,matched_value)) AS matches
          FROM evidence GROUP BY id ORDER BY op_count DESC, word_count DESC, id LIMIT ?""",
          (json.dumps(terms),json.dumps(operations),limit)))
        output=[]
        for hit in rows:
            matches=json.loads(hit["matches"])
            result=self.get(hit["id"])
            terms_hit=sorted(v for kind,v in matches if kind=="term")
            op_hit=sorted(v for kind,v in matches if kind=="operation")
            tags=(["terms"] if terms_hit else [])+(["operation"] if op_hit else [])
            reasons=[]
            if terms_hit:
                reasons.append("주소·제목에서 일치한 말 " + ", ".join(terms_hit))
            if op_hit:
                reasons.append("출처가 연결된 작동 원리 " + ", ".join(op_hit))
            result.update(matched=tags,matched_terms=terms_hit,matched_operations=op_hit,
                          why=" / ".join(reasons),unknown=UNKNOWN)
            output.append(result)
        return output

    def shortlist(self, ledger, request_revision_id, item_id, *, version, scope, configuration):
        """Materialize only a selected context; listing/discovery never writes a request."""
        if ledger.conn is not self.conn:
            raise ValueError("catalog and ledger must share this connection for an atomic shortlist")
        version,scope,configuration = [_text(v,n) for v,n in
            ((version,"version"),(scope,"scope"),(configuration,"configuration"))]
        with ledger.transaction():
            item = self.get(item_id)
            resource_id = "catalog:"+item_id
            edition_id = _id("ed-",[item_id,version])
            context_id = _id("ctx-",[request_revision_id,edition_id,scope,configuration])
            # Global identities do not change when a bare bookmark is enriched.
            ledger.add_resource(resource_id,item["canonical_url"],"catalog-link")
            ledger.add_edition(edition_id,resource_id,version)
            ledger.add_context(context_id,request_revision_id,edition_id,scope,configuration)
            self.conn.execute("""CREATE TABLE IF NOT EXISTS catalog_shortlist (
                context_id TEXT PRIMARY KEY REFERENCES candidate_context(id),
                item_id TEXT NOT NULL REFERENCES catalog_link(id))""")
            self.conn.execute("""INSERT INTO catalog_shortlist VALUES(?,?)
                                ON CONFLICT(context_id) DO NOTHING""", (context_id,item_id))
        return context_id


def main():
    """A request ledger is unnecessary for bookmarking or browsing the catalog."""
    import argparse
    from pathlib import Path
    import sqlite3

    parser = argparse.ArgumentParser(description="공개 링크와 적용 가능한 원리를 로컬 SQLite에 보관·검색합니다.")
    parser.add_argument("database", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="URL만 등록하거나 짧은 메타데이터를 보충")
    add.add_argument("url")
    add.add_argument("--title")
    add.add_argument("--form", choices=sorted(FORMS))
    add.add_argument("--note")
    add.add_argument("--provenance")
    relation = commands.add_parser("relate", help="작동 원리·불변조건·적용 한계와 출처 기록")
    relation.add_argument("item_id")
    for field in ("operation","invariant","breaks-at","locator","provenance"):
        relation.add_argument("--"+field, required=True)
    find = commands.add_parser("find", help="주소·제목 용어와 등록된 작동 원리로 발견")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--operation", action="append", default=[])
    find.add_argument("--limit", type=int, default=12)
    show = commands.add_parser("show", help="원주소·별칭·근거 위치와 적용 한계 조회")
    show.add_argument("item_id")
    args = parser.parse_args()
    if args.command not in ("add",) and not args.database.is_file():
        parser.error("database does not exist")
    conn = sqlite3.connect(args.database, isolation_level=None, timeout=15)
    try:
        conn.execute("PRAGMA foreign_keys=ON")
        catalog = Catalog(conn)
        if args.command == "add":
            item = catalog.add(args.url, title=args.title, form=args.form,
                               note=args.note, provenance=args.provenance)
            result = catalog.get(item)
        elif args.command == "relate":
            catalog.add_relation(args.item_id, args.operation, args.invariant, args.breaks_at,
                                 args.locator,args.provenance)
            result = catalog.get(args.item_id)
        elif args.command == "find":
            result = catalog.discover(args.query, operations=args.operation, limit=args.limit)
        else:
            result = catalog.get(args.item_id)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
