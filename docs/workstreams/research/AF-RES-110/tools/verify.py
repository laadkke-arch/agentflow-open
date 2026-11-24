"""Audit the frozen cohort, lexical arithmetic, replay and RESULT tables."""
import argparse
from collections import Counter
import json
from pathlib import Path
from urllib.parse import unquote

from policy import assess, fields
from prototype import catalog_module, roundtrip_module
from replay import DISPLAY, INVESTIGATE, file_hash, signature_rows
from summarize import ROOT, LANGUAGES, METHODS, compute, csv_rows, json_rows

TALLY_MINIMUM = {"feature": 8, "requirement": 6, "change": 6, "crossdomain": 4}


def check_seals():
    evidence = ROOT / "evidence"
    for file, mapping in (
        ("cards-seal.json", {"catalog_sha256": "catalog.jsonl", "policy_sha256": "tools/policy.py"}),
        ("queries-seal.json", {"query_sha256": "queries.jsonl", "frame_sha256": "issue-frame.csv"}),
        ("truth-seal.json", {"truth_sha256": "truth.csv", "queries_sha256": "queries.jsonl"}),
    ):
        values = json.loads((evidence / file).read_text())
        assert all(values[key] == file_hash(ROOT / relpath) for key, relpath in mapping.items()), file


def check_input():
    frames = csv_rows(ROOT / "frame.csv")
    issues = csv_rows(ROOT / "issue-frame.csv")
    queries = json_rows(ROOT / "queries.jsonl")
    cards = json_rows(ROOT / "catalog.jsonl")
    truth = csv_rows(ROOT / "truth.csv")
    sources = json_rows(ROOT / "sources.jsonl")
    counts = Counter(r["category"] for r in sources if r["counted"])
    assert all(counts[k] >= v for k, v in TALLY_MINIMUM.items())
    assert len({r["work_key"] for r in sources if r["counted"]}) == sum(counts.values())
    assert all(s["access"] == "direct" for s in sources if s["counted"])
    source_ids = {s["source_id"] for s in sources}
    assert len(source_ids) == len(sources)
    assert len(frames) == 24 and len(queries) == 6 and len(truth) == 6 * 24
    features = {r["slot_id"] for r in frames}
    assert len(features) == 24
    qids = {q["query_id"] for q in queries}
    assert {(r["query_id"], r["feature_id"]) for r in truth} == {(q, f) for q in qids for f in features}
    assert len(cards) == 48 and len({c["url"] for c in cards}) == 48
    assert {(r["feature_id"], r["tier"]) for r in cards} == {(f, t) for f in features for t in ("old", "current")}
    assert {c["language"] for c in cards} == {"en"}
    assert all(ref["source_id"] in source_ids for c in cards for ref in c["evidence"])
    assert all(all(id in source_ids for id in r[key].split("|"))
               for r in truth for key in ("old_reference_ids", "current_reference_ids"))
    assert all(r["rank_access"] == "withheld" for r in truth)
    for q in queries:
        cohort = [r for r in issues if r["project"] == q["project"]]
        assert len(cohort) == 40
        assert [int(r["ordinal"]) for r in cohort] == list(range(1, 41))
        keys = [(r["created_utc"], int(r["issue_number"])) for r in cohort]
        assert keys == sorted(set(keys)) and keys[29][0] != keys[30][0]
        first = next(r for r in cohort[:30] if r["select_status"] == "first_qualifying_published_starter")
        assert first["issue_url"] == q["issue_url"] and first["body_sha256"] == q["starter_sha256"]
        assert q["source_id"] in source_ids
    return queries, cards


def numeric_rows(rows):
    string_fields = {"run_id", "query_id", "language", "method", "query_area", "card_id", "catalog_id",
                     "feature_id", "feature_area", "tier", "edition", "base_terms", "note_only", "note_shared",
                     "operations", "conflicts", "edition_compatibility", "return_location", "url", "page_url"}
    return [
        {k: (v == "True" if k == "occupied" else (v if k in string_fields or v == "" else int(v)))
         for k, v in row.items()}
        for row in rows
    ]


def check_ranks(queries, cards):
    original = catalog_module()
    card_by_id = {row["card_id"]: row for row in cards}
    runs = json_rows(ROOT / "runs.jsonl")
    ranks = numeric_rows(csv_rows(ROOT / "ranks.csv"))
    assert len(runs) == 72 and len(ranks) == 72 * 12
    keyed_runs = {row["run_id"]: row for row in runs}
    keyed_ranks = {id: [r for r in ranks if r["run_id"] == id] for id in keyed_runs}
    assert len(keyed_runs) == 72 and all(len(r) == 12 for r in keyed_ranks.values())
    assert sum(r["catalog_calls"] for r in runs) == 48
    assert sum(r["method"] == "C" and r["sql_statements"] != 0 for r in runs) == 0
    expected = {}
    with roundtrip_module() as fixed:
        for q in queries:
            for lang in LANGUAGES:
                text = q[lang]
                words = original.words(text)
                ops = set(fixed.infer_mechanisms(text))
                rows = {m: [] for m in METHODS}
                for card in cards:
                    url = original.canonical_url(card["url"])
                    item = original._id("link-", [url])
                    terms = (original.words(unquote(url)) - original.URL_STOP) | original.words(card["title"])
                    keys = {original._op(r["operation"]) for r in card["relations"]} & ops
                    for m in ("A", "B"):
                        indexed = terms if m == "A" else terms | original.words(card["note"])
                        overlap = words & indexed
                        if overlap or keys:
                            rows[m].append((-len(keys), -len(overlap), item, card["card_id"],
                                            "|".join(sorted(overlap - terms))))
                for m in ("A", "B"):
                    rows[m] = sorted(rows[m])[:INVESTIGATE]
                request = fields(text)
                verdict = {
                    c_id: assess(card_by_id[c_id]["applicability"], request) for _, _, _, c_id, _ in rows["B"]
                }
                rows["C"] = sorted(rows["B"], key=lambda item: bool(verdict[item[3]]["conflicts"]))
                for method in METHODS:
                    for build in (1, 2):
                        key = f"{build}/{q['query_id']}/{lang}/{method}"
                        material = keyed_ranks[key]
                        receipt = keyed_runs[key]
                        shown = [r for r in material if r["occupied"]]
                        assert len(material) - len(shown) == receipt["investigation_vacant"]
                        assert DISPLAY - min(DISPLAY, len(shown)) == receipt["display_vacant"]
                        assert [r["display_slot"] for r in material[:DISPLAY]] == [1, 2, 3]
                        assert all(r["display_slot"] == "" for r in material[DISPLAY:])
                        assert [(r["op_score"], r["word_score"], r["catalog_id"], r["card_id"], r["note_only"])
                                for r in shown] == [(-x, -y, item, id, terms) for x, y, item, id, terms in rows[method]]
                        assert all(r["url"] == card_by_id[r["card_id"]]["url"] for r in shown)
                        if method == "C":
                            assert receipt["automatic_fields"] == request
                            assert all(r["conflicts"] == "|".join(verdict[r["card_id"]]["conflicts"]) for r in shown)
                            assert all(r["edition_compatibility"] == verdict[r["card_id"]]["edition_status"] for r in shown)
                        assert signature_rows(material) == receipt["fingerprint"]
                        variant = key.split("/", 1)[1]
                        if build == 1:
                            expected[variant] = receipt["fingerprint"]
                        else:
                            assert expected[variant] == receipt["fingerprint"]
    return len(keyed_runs)


def attempt_fresh_comparison(output):
    old = json.loads((ROOT / "evidence/replay.json").read_text())
    new = json.loads((output / "replay.json").read_text())
    assert [s["fingerprint"] for s in new["builds"]] == [s["fingerprint"] for s in old["builds"]]
    for index in (0, 1):
        for m in ("A", "B"):
            assert new["builds"][index][m]["database_sha256"] == old["builds"][index][m]["database_sha256"]
    assert (output / "ranks.csv").read_bytes() == (ROOT / "ranks.csv").read_bytes()
    assert (output / "replacement.json").read_bytes() == (ROOT / "evidence/replacement.json").read_bytes()


def main(fresh):
    check_seals()
    queries, cards = check_input()
    run_count = check_ranks(queries, cards)
    tally, tables = compute(ROOT, ROOT / "evidence")
    assert tally == json.loads((ROOT / "evidence/summary.json").read_text())
    assert (ROOT / "RESULT.md").read_text().startswith(tables)
    replacement = json.loads((ROOT / "evidence/replacement.json").read_text())
    before = replacement["states"]["before"]
    after = replacement["states"]["after"]
    assert before == replacement["states"]["replay_before"]
    assert replacement["citations"]["before"] == replacement["citations"]["replay_before"]
    changed = after["comparisons"]["S-REPLACE-CUE"]["runs"]["C"]["target_candidate"]
    control = after["comparisons"]["S-REPLACE"]["runs"]["C"]["target_candidate"]
    assert changed["conflicts"] == "python:3.12" and changed["candidate_rank"] > DISPLAY
    assert control["conflicts"] == "" and control["candidate_rank"] <= DISPLAY
    if fresh:
        attempt_fresh_comparison(fresh)
    print(json.dumps({"runner_records": run_count, "frames": tally["frame_slots"], "queries": len(queries),
                      "truth_rows": tally["truth_rows"], "primary_source_counts": tally["direct_first_party_work_counts"],
                      "fingerprint": tally["main_replay_fingerprint"], "fresh_bitwise_rank_comparison": bool(fresh),
                      "required_tables": 3, "verified_creation_revisions": tally["first_query_original_verified"]}))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--fresh", type=Path, help="directory produced by replay.py --output")
    main(cli.parse_args().fresh)
