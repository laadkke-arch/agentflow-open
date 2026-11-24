"""Build fresh SQLite search inputs and replay the same four search conditions."""

import argparse
import collections
import csv
import hashlib
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {"verified": "alias_verified", "publisher_partial": "alias_publisher"}
MODES = [(0, 0), (1, 0), (0, 1), (1, 1)]
LANGUAGES = ("en", "ko")
WIDTHS = (12, 3)
WORDS = re.compile(r"[^\W_]+", re.UNICODE)
HANGUL = re.compile(r"[가-힣ㄱ-ㅎㅏ-ㅣ]")
STOP = frozenset("a an and as at be by for from in is it of on or the to with www https html".split())
WEIGHTS = {"title": 3, "memo_en": 2, "url": 1}
ROLE_NAMES = {"input", "output", "edit", "display"}
SLOTS = [f"r{i:02}" for i in range(1, 13)] + [f"d{i:02}" for i in range(1, 4)]
ROW_FIELDS = (
    "profile", "replay", "layer", "query_id", "language", "alias", "role", "execution",
    "sql_statements", "terms", *SLOTS, "retrieved_json", "display_json",
)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def tokens(value):
    return sorted(set(WORDS.findall(unicodedata.normalize("NFKC", value).casefold())) - STOP)


def checked_roles(entries):
    for entry in entries:
        if entry["role"] not in ROLE_NAMES or not entry["concept"] or not entry["url"]:
            raise ValueError("invalid role evidence")
    return entries


def create_catalog(connection, cards, profile):
    connection.execute("PRAGMA page_size=4096")
    connection.executescript(
        """
        CREATE TABLE postings (
            term TEXT NOT NULL,
            feature_id TEXT NOT NULL,
            field TEXT NOT NULL,
            weight INTEGER NOT NULL,
            PRIMARY KEY (term, feature_id, field)
        ) WITHOUT ROWID;
        """
    )
    base_rows = [
        (term, card["feature_id"], field, weight)
        for card in cards
        for field, weight in WEIGHTS.items()
        for term in tokens(card[field])
    ]
    connection.executemany("INSERT INTO postings VALUES (?, ?, ?, ?)", base_rows)
    connection.commit()
    base_pages = connection.execute("PRAGMA page_count").fetchone()[0]

    pairs = {
        (term, card["feature_id"])
        for card in cards
        for label in card[PROFILES[profile]]
        for term in tokens(label["ko"])
        if HANGUL.search(term)
    }
    connection.execute(
        """CREATE TABLE aliases (
               term TEXT NOT NULL, feature_id TEXT NOT NULL,
               PRIMARY KEY (term, feature_id)
           ) WITHOUT ROWID"""
    )
    connection.executemany("INSERT INTO aliases VALUES (?, ?)", sorted(pairs))
    connection.commit()
    alias_pages = connection.execute("PRAGMA page_count").fetchone()[0]

    role_rows = [
        (card["feature_id"], json_text(checked_roles(card["roles"])))
        for card in cards
        if card["roles"]
    ]
    connection.execute("CREATE TABLE roles (feature_id TEXT PRIMARY KEY, payload TEXT NOT NULL) WITHOUT ROWID")
    connection.executemany("INSERT INTO roles VALUES (?, ?)", role_rows)
    connection.commit()
    role_pages = connection.execute("PRAGMA page_count").fetchone()[0]

    alias_fields = [card[PROFILES[profile]] for card in cards if card[PROFILES[profile]]]
    return {
        "base_rows": len(base_rows),
        "alias_rows": len(pairs),
        "alias_label_rows": sum(map(len, alias_fields)),
        "alias_feature_count": len(alias_fields),
        "role_features": len(role_rows),
        "role_statements": sum(len(c["roles"]) for c in cards),
        "base_data_bytes": sum(len(c[f].encode("utf-8")) for c in cards for f in WEIGHTS),
        "alias_evidence_bytes": sum(len(json_text(labels).encode("utf-8")) for labels in alias_fields),
        "role_evidence_bytes": sum(len(payload.encode("utf-8")) for _, payload in role_rows),
        "page_size": 4096,
        "base_database_bytes": base_pages * 4096,
        "alias_extra_database_bytes": (alias_pages - base_pages) * 4096,
        "role_extra_database_bytes": (role_pages - alias_pages) * 4096,
    }


def retrieve(connection, words, alias):
    if not words:
        return [], 0
    token_params = ", ".join("(?)" for _ in words)
    alias_sql = """
        UNION ALL
        SELECT aliases.feature_id, aliases.term, 'alias', 3
        FROM aliases JOIN tokens USING (term)
    """ if alias else ""
    sql = f"""
        WITH tokens(term) AS (VALUES {token_params}), matched AS (
            SELECT postings.feature_id, postings.term, postings.field, postings.weight
            FROM postings JOIN tokens USING (term)
            {alias_sql}
        )
        SELECT feature_id, SUM(weight), GROUP_CONCAT(field || ':' || term)
        FROM matched
        GROUP BY feature_id
        ORDER BY SUM(weight) DESC, feature_id
        LIMIT 12
    """
    return [
        {"rank": rank, "id": feature, "score": score, "matched": sorted(matches.split(","))}
        for rank, (feature, score, matches) in enumerate(connection.execute(sql, words), 1)
    ], 1


def compare_roles(request_roles, evidence):
    available = collections.defaultdict(list)
    for statement in evidence:
        available[statement["concept"]].append(statement)
    comparisons = []
    for request in request_roles:
        candidate = available[request["concept"]]
        if not candidate:
            state = "unresolved"
        elif any(entry["role"] == request["role"] for entry in candidate):
            state = "supported_role"
        else:
            state = "conflicting_role"
        comparisons.append({"state": state, "request": request, "candidate": candidate})
    return comparisons


def display(connection, pool, request_roles, role_mode):
    if not role_mode or not pool:
        return [{**item, "slot": i, "conflicts": None, "comparisons": []}
                for i, item in enumerate(pool[:3], 1)], [], 0
    marks = ", ".join("?" for _ in pool)
    get_roles = f"SELECT feature_id, payload FROM roles WHERE feature_id IN ({marks})"
    payloads = {
        feature: json.loads(payload)
        for feature, payload in connection.execute(get_roles, [item["id"] for item in pool])
    }
    annotated = []
    for item in pool:
        comparisons = compare_roles(request_roles, payloads.get(item["id"], []))
        conflicts = sum(x["state"] == "conflicting_role" for x in comparisons)
        annotated.append({**item, "conflicts": conflicts, "comparisons": comparisons})
    ordered = sorted(annotated, key=lambda item: (item["conflicts"], item["rank"]))
    return [{**item, "slot": i} for i, item in enumerate(ordered[:3], 1)], annotated, 1


def query_row(connection, query, language, profile, iteration, alias, role_mode):
    value = query[language]
    words = tokens(value) if value else []
    raw, search_calls = retrieve(connection, words, alias)
    selected, annotations, role_calls = display(connection, raw, checked_roles(query["roles"]), role_mode)
    rids = [item["id"] for item in raw]
    dids = [item["id"] for item in selected]
    values = rids + [""] * (12 - len(rids)) + dids + [""] * (3 - len(dids))
    return {
        "profile": profile,
        "replay": iteration,
        "layer": query["layer"],
        "query_id": query["query_id"],
        "language": language,
        "alias": alias,
        "role": role_mode,
        "execution": "executed" if value else "vacant_request",
        "sql_statements": search_calls + role_calls,
        "terms": json_text(words),
        **dict(zip(SLOTS, values, strict=True)),
        "retrieved_json": json_text(annotations if role_mode else raw),
        "display_json": json_text(selected),
    }


def replay_layer(connection, queries, profile, iteration):
    result = []
    for query in queries:
        languages = ("ko",) if query["layer"] == "variant" else LANGUAGES
        for language in languages:
            for alias, role_mode in MODES:
                result.append(query_row(connection, query, language, profile, iteration, alias, role_mode))
    return result


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ROW_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def observation(rows):
    key = {k for k in ROW_FIELDS if k != "replay"}
    payload = [{k: row[k] for k in key} for row in rows]
    return {
        "fingerprint": digest(json_text(payload).encode("utf-8")),
        "rows": len(rows),
        "actual_queries": sum(row["execution"] == "executed" for row in rows),
        "empty_requests": sum(row["execution"] == "vacant_request" for row in rows),
        "sql_statements": sum(row["sql_statements"] for row in rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.jsonl")
    parser.add_argument("--queries", type=Path, default=ROOT / "queries.jsonl")
    parser.add_argument("--profile", choices=tuple(PROFILES), required=True)
    parser.add_argument("--layers", nargs="+", choices=("natural", "exploratory", "control", "variant"),
                        default=("natural", "exploratory", "control", "variant"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    cards = read_jsonl(args.catalog)
    queries = read_jsonl(args.queries)
    if len(cards) != 24 or len({c["feature_id"] for c in cards}) != 24:
        raise ValueError("the replay requires 24 fixed distinct cards")
    if len({q["query_id"] for q in queries}) != len(queries):
        raise ValueError("duplicate query identifiers")
    args.out.mkdir(parents=True, exist_ok=False)
    by_layer = {layer: [] for layer in args.layers}
    receipt = {
        "profile": args.profile,
        "python": ".".join(map(str, sys.version_info[:3])),
        "sqlite": sqlite3.sqlite_version,
        "input_sha256": {"catalog": digest(args.catalog.read_bytes()), "queries": digest(args.queries.read_bytes())},
        "builds": [],
    }
    for iteration in (1, 2):
        path = args.out / f"build{iteration}.sqlite"
        connection = sqlite3.connect(path)
        try:
            cost = create_catalog(connection, cards, args.profile)
            measured = {}
            for layer in by_layer:
                rows = replay_layer(connection, [q for q in queries if q["layer"] == layer], args.profile, iteration)
                by_layer[layer].extend(rows)
                measured[layer] = observation(rows)
        finally:
            connection.close()
        receipt["builds"].append({"replay": iteration, "database_bytes": path.stat().st_size,
                                  "index": cost, "layers": measured})
    receipt["repeat_agrees"] = receipt["builds"][0]["layers"] == receipt["builds"][1]["layers"]
    if not receipt["repeat_agrees"]:
        raise RuntimeError("independent databases disagreed")
    for layer, rows in by_layer.items():
        write_csv(args.out / f"{layer}.csv", rows)
    (args.out / "replay.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
