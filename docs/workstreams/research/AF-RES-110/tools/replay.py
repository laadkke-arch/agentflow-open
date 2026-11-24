"""Replay Gallim lexical discovery on AF-RES-110's frozen inputs."""
import argparse
from collections import Counter
from contextlib import closing
import csv
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
from urllib.parse import unquote, urldefrag

from policy import assess, fields
from prototype import catalog_module, roundtrip_module

ROOT = Path(__file__).resolve().parents[1]
INVESTIGATE = 12
DISPLAY = 3
METHODS = ("A", "B", "C")
LANGUAGES = ("en", "ko")
PRAGMAS = {"page_size": 4096, "cache_size": -2048, "journal_mode": "delete",
           "synchronous": 2, "temp_store": 2, "auto_vacuum": 0}


def serialize(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def signature(value):
    return hashlib.sha256(serialize(value).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def jsonl(name):
    return [json.loads(line) for line in (ROOT / name).read_text().splitlines()]


def write_json(output, name, value):
    (output / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_jsonl(output, name, rows):
    (output / name).write_text("".join(serialize(row) + "\n" for row in rows))


def write_csv(output, name, rows):
    with (output / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def tagged(token_list):
    return "|".join(token_list)


class CatalogRun:
    def __init__(self, catalog, database, cards, *, notes=False):
        self.module = catalog
        self.connection = sqlite3.connect(database, isolation_level=None)
        for key, value in PRAGMAS.items():
            self.connection.execute(f"PRAGMA {key}={value}")
        self.connection.execute("PRAGMA foreign_keys=ON")
        start = time.perf_counter_ns()
        self.catalog = catalog.Catalog(self.connection)
        self.card_by_item = {}
        self.meta_words = {}
        self.note_words = {}
        with catalog._atomic(self.connection):
            for card in cards:
                item = self.catalog.add(card["url"], title=card["title"], form="feature",
                                        note=card["note"], provenance=card["evidence"][0]["source_id"])
                self.card_by_item[item] = card
                meta = (catalog.words(unquote(catalog.canonical_url(card["url"]))) - catalog.URL_STOP)
                self.meta_words[item] = meta | catalog.words(card["title"])
                self.note_words[item] = catalog.words(card["note"])
                for relation in card["relations"]:
                    self.catalog.add_relation(item, **relation)
                if notes:
                    self.connection.executemany("INSERT OR IGNORE INTO catalog_term VALUES (?,?)",
                                                ((term, item) for term in sorted(self.note_words[item])))
        elapsed = time.perf_counter_ns() - start
        assert len(self.card_by_item) == len(cards)
        stored_pragmas = {key: self.connection.execute(f"PRAGMA {key}").fetchone()[0] for key in PRAGMAS}
        assert stored_pragmas == PRAGMAS
        # These three b-trees serve the original term lookup and its indexes.
        term_names = ("catalog_term", "catalog_item_terms", "sqlite_autoindex_catalog_term_1")
        term_bytes = self.connection.execute(
            "SELECT total(pgsize) FROM dbstat WHERE name IN (?,?,?)", term_names
        ).fetchone()[0]
        self.stats = {
            "pragmas": stored_pragmas,
            "init_and_build_ns": elapsed,
            "database_bytes": database.stat().st_size,
            "database_sha256": file_hash(database),
            "term_table_and_indexes_bytes": int(term_bytes),
            "term_rows": self.connection.execute("SELECT count(*) FROM catalog_term").fetchone()[0],
            "link_rows": len(self.card_by_item),
            "relation_rows": self.connection.execute("SELECT count(*) FROM catalog_relation").fetchone()[0],
        }

    def lookup(self, query, operations, *, limit=INVESTIGATE):
        statements = 0

        def count(_statement):
            nonlocal statements
            statements += 1

        self.connection.set_trace_callback(count)
        start = time.perf_counter_ns()
        try:
            hits = self.catalog.discover(query, operations=operations, limit=limit)
            elapsed = time.perf_counter_ns() - start
        finally:
            self.connection.set_trace_callback(None)
        return hits, elapsed, statements

    def close(self):
        self.connection.close()


def score(hit):
    return len(hit["matched_operations"]), len(hit["matched_terms"])


def flags(database, hits, requested):
    return {row["item_id"]: assess(database.card_by_item[row["item_id"]]["applicability"], requested)
            for row in hits}


def rerank(hits, applicability):
    # Stable order across clean/unknown candidates and across conflicting candidates.
    return sorted(hits, key=lambda row: bool(applicability[row["item_id"]]["conflicts"]))


def signature_rows(rows):
    return signature([{k: v for k, v in row.items() if k not in ("build", "run_id")} for row in rows])


def ranked_rows(build, query, language, method, db, hits, applicability, lexical_order):
    hit_counts = Counter(map(score, lexical_order))
    positions = {row["item_id"]: index for index, row in enumerate(lexical_order, 1)}
    for rank in range(1, INVESTIGATE + 1):
        hit = hits[rank - 1] if rank <= len(hits) else None
        item = hit["item_id"] if hit else ""
        card = db.card_by_item[item] if hit else {}
        matched = set(hit["matched_terms"]) if hit else set()
        lexical = db.meta_words[item] if hit else set()
        note = db.note_words[item] if hit else set()
        status = applicability.get(item, {})
        yield {
            "run_id": f"{build}/{query['query_id']}/{language}/{method}",
            "build": build, "query_id": query["query_id"], "language": language, "method": method,
            "query_area": query["area"], "candidate_rank": rank,
            "display_slot": rank if rank <= DISPLAY else "",
            "occupied": bool(hit),
            "card_id": card.get("card_id", ""), "catalog_id": item,
            "feature_id": card.get("feature_id", ""), "feature_area": card.get("area", ""),
            "tier": card.get("tier", ""), "edition": card.get("edition", ""),
            "op_score": score(hit)[0] if hit else "", "word_score": score(hit)[1] if hit else "",
            "same_score_in_primary_pool": hit_counts[score(hit)] if hit else "",
            "lexical_rank": positions.get(item, ""),
            "base_terms": tagged(sorted(matched & lexical)),
            "note_only": tagged(sorted(matched - lexical)),
            "note_shared": tagged(sorted(matched & note & lexical)),
            "operations": tagged(hit["matched_operations"]) if hit else "",
            "conflicts": tagged(status.get("conflicts", [])),
            "edition_compatibility": status.get("edition_status", "not_evaluated") if hit else "",
            "return_location": card.get("location", ""), "url": hit["url"] if hit else "",
            "page_url": urldefrag(hit["url"]).url if hit else "",
        }


def sensitivity(database, text, ops, expected, request, method):
    hits, elapsed, sql_count = database.lookup(text, ops, limit=len(database.card_by_item))
    original = hits[:INVESTIGATE]
    assert [h["item_id"] for h in original] == [h["item_id"] for h in expected]
    # Keep score keys and change only the deterministic ID tie breaker.
    reversed_id = sorted(hits, key=lambda h: h["item_id"], reverse=True)
    alternate = sorted(reversed_id, key=score, reverse=True)[:INVESTIGATE]

    def visible(options):
        return [database.card_by_item[h["item_id"]]["card_id"] for h in options[:DISPLAY]]

    methods = {method: {"display_original": visible(original), "display_reverse_id": visible(alternate)}}
    if method == "B":
        methods["C"] = {
            "display_original": visible(rerank(original, flags(database, original, request))),
            "display_reverse_id": visible(rerank(alternate, flags(database, alternate, request))),
        }
    return {
        "lookup_ns": elapsed, "sql_statements": sql_count, "matched_count": len(hits),
        "score_group_sizes": [[*key, count] for key, count in Counter(map(score, hits)).items()],
        "tie_across_3": len(hits) > DISPLAY and score(hits[DISPLAY - 1]) == score(hits[DISPLAY]),
        "tie_across_12": len(hits) > INVESTIGATE and score(hits[INVESTIGATE - 1]) == score(hits[INVESTIGATE]),
        "methods": methods,
    }


def play(build, version_db, queries, infer):
    runs = []
    ranks = []
    aux = []
    fingerprints = {}
    shortlist = set()
    # The measured mode order is constant. All sensitivity queries follow the main pass.
    for language in LANGUAGES:
        for query in queries:
            text = query[language]
            ops = infer(text)
            request = fields(text)
            hits_a, ns_a, sql_a = version_db["A"].lookup(text, ops)
            hits_b, ns_b, sql_b = version_db["B"].lookup(text, ops)
            start = time.perf_counter_ns()
            applicability = flags(version_db["B"], hits_b, request)
            hits_c = rerank(hits_b, applicability)
            ns_c = time.perf_counter_ns() - start
            for method, database, hits, lexical, ns, sql_count in (
                ("A", version_db["A"], hits_a, hits_a, ns_a, sql_a),
                ("B", version_db["B"], hits_b, hits_b, ns_b, sql_b),
                ("C", version_db["B"], hits_c, hits_b, ns_c, 0),
            ):
                part = list(ranked_rows(build, query, language, method, database, hits,
                                        applicability if method == "C" else {}, lexical))
                run_id = part[0]["run_id"]
                fingerprints[f"{query['query_id']}/{language}/{method}"] = signature_rows(part)
                ranks.extend(part)
                shortlist.update(row["card_id"] for row in part if row["occupied"])
                runs.append({
                    "run_id": run_id, "build": build, "query_id": query["query_id"],
                    "language": language, "method": method, "query_area": query["area"],
                    "query_sha256": signature(text), "operation_keys": ops,
                    "automatic_fields": request if method == "C" else None,
                    "catalog_calls": int(method != "C"), "sql_statements": sql_count,
                    "elapsed_ns": ns, "end_to_end_ns": ns + (ns_b if method == "C" else 0),
                    "inherited_catalog": f"{build}/{query['query_id']}/{language}/B" if method == "C" else None,
                    "investigation_slots": INVESTIGATE, "display_slots": DISPLAY,
                    "investigation_vacant": INVESTIGATE - len(hits),
                    "display_vacant": DISPLAY - min(DISPLAY, len(hits)),
                    "fingerprint": fingerprints[f"{query['query_id']}/{language}/{method}"],
                })
            aux.append((language, query, text, ops, request, hits_a, hits_b))
    ties = {}
    for lang, query, text, ops, request, hits_a, hits_b in aux:
        key = f"{query['query_id']}/{lang}"
        ties[key] = {method: sensitivity(version_db[method], text, ops, hits, request, method)
                     for method, hits in (("A", hits_a), ("B", hits_b))}
    return runs, ranks, ties, signature(fingerprints), sorted(shortlist)


def fixed_replacement(directory, catalog, infer, cards):
    recipe = json.loads((ROOT / "evidence" / "replacement-input.json").read_text())
    states = {}
    archived_citations = {}
    target = recipe["feature_id"]
    for state, tier in (("before", "old"), ("after", "current"), ("replay_before", "old")):
        subset = [card for card in cards
                  if card["tier"] == (tier if card["feature_id"] == target else "current")]
        pointer = next(card for card in subset if card["feature_id"] == target)
        archived_citations[state] = {"card_id": pointer["card_id"], "url": pointer["url"],
                                     "text": recipe["citation"][tier], "location": pointer["location"],
                                     "source_sha256": recipe["source_sha256"][tier]}
        with closing(CatalogRun(catalog, directory / f"change-{state}-A.db", subset)) as a, closing(
            CatalogRun(catalog, directory / f"change-{state}-B.db", subset, notes=True)
        ) as b:
            comparisons = {}
            for query in recipe["queries"]:
                text = query["en"]
                ops = infer(text)
                requested = fields(text)
                a_hits, _, _ = a.lookup(text, ops)
                b_hits, _, _ = b.lookup(text, ops)
                cue = flags(b, b_hits, requested)
                c_hits = rerank(b_hits, cue)
                rows = {}
                for method, db, hits, lexical in (("A", a, a_hits, a_hits), ("B", b, b_hits, b_hits),
                                                  ("C", b, c_hits, b_hits)):
                    ranked = list(ranked_rows("replacement", query, "en", method, db, hits,
                                              cue if method == "C" else {}, lexical))
                    rows[method] = {
                        "fingerprint": signature_rows(ranked),
                        "display": [r["card_id"] or None for r in ranked[:DISPLAY]],
                        "target_candidate": next((r for r in ranked if r["feature_id"] == target), None),
                    }
                comparisons[query["query_id"]] = {"query_sha256": signature(text),
                                                    "automatic_fields": requested, "runs": rows}
            states[state] = {"state_sha256": signature([card["card_id"] for card in subset]),
                             "input_count": len(subset), "comparisons": comparisons}
    assert states["before"] == states["replay_before"]
    assert archived_citations["before"] == archived_citations["replay_before"]
    assert archived_citations["before"]["url"] != archived_citations["after"]["url"]
    return {
        "scope": "Controlled single-card replacement; all other 23 cards use the current edition.",
        "six_natural_queries_excluded": True,
        "catalog_lookups": len(states) * len(recipe["queries"]) * 2,
        "states": states, "citations": archived_citations,
        "previous_answer_and_citation_reproduced": True,
    }


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    cards = jsonl("catalog.jsonl")
    queries = jsonl("queries.jsonl")
    archive = jsonl("sources.jsonl")
    catalog = catalog_module()
    stats = {"python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version,
             "pragmas": PRAGMAS, "natural_sort_order": "build A/B, for en then ko query order A/B/C, then ties"}
    card_reads = [r for r in archive if r["source_id"].startswith("DOC-")]
    # Same body can appear as multiple cited spans or arrive as a second version.
    distinct_bytes = {r["source_sha256"]: r["source_bytes"] for r in card_reads}
    readings = {(r["arrival_url"], r["read_utc"]): r["source_bytes"] for r in card_reads}
    stats["preparation"] = {
        "card_read_response_count": len(readings), "card_read_response_bytes": sum(readings.values()),
        "unique_card_source_contents": len(distinct_bytes),
        "deduplicated_card_source_bytes": sum(distinct_bytes.values()),
        "catalog_serialized_bytes": (ROOT / "catalog.jsonl").stat().st_size,
        "application_fields_bytes": sum(len(serialize(card["applicability"]).encode()) for card in cards),
        "notes_count": len(cards), "unique_note_texts": len({c["note"] for c in cards}),
        "note_unicode_chars": sum(len(c["note"]) for c in cards),
        "note_utf8_bytes": sum(len(c["note"].encode()) for c in cards),
        "relation_records": sum(len(c["relations"]) for c in cards),
        "language_counts": dict(Counter(c["language"] for c in cards)),
        "manual_author_hours": None, "hosting_cost": None,
    }
    runs = []
    ranks = []
    groups = []
    with tempfile.TemporaryDirectory(prefix="af110-replay-") as folder, roundtrip_module() as original:
        directory = Path(folder)
        for build in (1, 2):
            with closing(CatalogRun(catalog, directory / f"{build}-A.db", cards)) as a, closing(
                CatalogRun(catalog, directory / f"{build}-B.db", cards, notes=True)
            ) as b:
                events, observations, ties, fingerprint, shortlist = play(
                    build, {"A": a, "B": b}, queries, original.infer_mechanisms)
                runs.extend(events)
                ranks.extend(observations)
                groups.append({"build": build, "fingerprint": fingerprint, "A": a.stats, "B": b.stats,
                               "tie_runs": ties, "shortlist_card_ids": shortlist})
        replacement = fixed_replacement(directory, catalog, original.infer_mechanisms, cards)
    stats["builds"] = groups
    stats["replay_identical"] = groups[0]["fingerprint"] == groups[1]["fingerprint"]
    assert stats["replay_identical"]
    for method in ("A", "B"):
        assert groups[0][method]["database_sha256"] == groups[1][method]["database_sha256"]
    write_jsonl(output, "runs.jsonl", runs)
    write_csv(output, "ranks.csv", ranks)
    write_json(output, "replay.json", stats)
    write_json(output, "replacement.json", replacement)
    print(serialize({"main_runs": len(runs), "rank_slots": len(ranks), "sqlite": stats["sqlite"],
                     "fingerprint": groups[0]["fingerprint"], "catalog_lookups": sum(r["catalog_calls"] for r in runs)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    main(parser.parse_args().output)
