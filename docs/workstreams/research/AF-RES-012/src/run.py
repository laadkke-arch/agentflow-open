"""Run and score all fixed description, method, language and corpus conditions."""
import argparse
import csv
from collections import defaultdict
import json
from pathlib import Path
import random
from time import perf_counter

from threadpoolctl import threadpool_limits

from .metrics import evaluate, summarize
from .search import (
    E5Index, LexicalIndex, LsaIndex, SEED, has_signal, ranking, reciprocal_rank_fusion,
    stable_order,
)


ROOT = Path(__file__).resolve().parents[1]
DESCRIPTIONS = ("D-a", "D-b", "D-c")
LANGUAGES = (("ko", "ko"), ("en", "en"), ("ko", "en"))
METHODS = ("M1", "M2", "M3")
REVIEWED = frozenset({
    "K01.w", "K02.w", "K03.w", "K04.w", "K05.w", "K06.w", "P1.w", "P2.w",
    "P01.w", "P02.w", "P03.w", "P04.w", "P01.1", "P02.2", "P03.2",
})


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def judgments(path, queries, entries):
    result = defaultdict(dict)
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file, delimiter="\t"):
            q, entry, grade = row["query_id"], row["entry_id"], row["grade"]
            if q not in queries or entry not in entries or grade not in {"0", "1", "2", "N"}:
                raise ValueError(f"Unknown query, entry or grade: {row}")
            if entry in result[q] or not row["reason"].strip():
                raise ValueError(f"Duplicate judgment or missing rationale: {row}")
            result[q][entry] = grade
    return result


def atomic_write(path, content):
    pending = path.with_suffix(path.suffix + ".tmp")
    pending.write_text(content, encoding="utf-8")
    pending.replace(path)


def write_rows(path, rows, delimiter=","):
    pending = path.with_suffix(path.suffix + ".tmp")
    with pending.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, rows[0].keys(), delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    pending.replace(path)


def validate_inputs(entries, queries, sources):
    ids = {entry["id"] for entry in entries}
    urls = {entry["url"] for entry in entries}
    if len(ids) != len(entries) or len(urls) != len(entries) or len(entries) < 150:
        raise ValueError("The complete corpus must include at least 150 unique entries and URLs.")
    source_ids = {source["id"] for source in sources}
    for item in entries:
        if item["role"] not in {"product", "component", "principle", "other"}:
            raise ValueError(f"Unknown role: {item['id']}")
        if not item["ledger_ref"] or not item["url"].startswith("https://"):
            raise ValueError(f"Missing provenance: {item['id']}")
        if not item["da_status"].endswith("_only") and item["da_source_id"] not in source_ids:
            raise ValueError(f"Missing primary description source: {item['id']}")
        for language in ("ko", "en"):
            gloss = [item[d][language] for d in DESCRIPTIONS]
            if not all(text.strip() and len(text.split()) <= 40 for text in gloss):
                raise ValueError(f"Description length error: {item['id']}/{language}")
            if not gloss[2].startswith(gloss[1] + " "):
                raise ValueError(f"D-c did not retain D-b: {item['id']}/{language}")
    ids_by_query = {query["id"] for query in queries}
    by_problem = defaultdict(list)
    for query in queries:
        by_problem[query["problem_id"]].append(query["whole_or_part"])
        if not query["ko"].strip() or not query["en"].strip() or len(query["origin_sha"]) != 40:
            raise ValueError(f"Missing original or translation: {query['id']}")
    if len(ids_by_query) != len(queries) or len(by_problem) != 12 or any(
        scopes.count("whole") != 1 or scopes.count("part") < 2 for scopes in by_problem.values()
    ):
        raise ValueError("Expected 12 problems, each with one whole and at least two partial queries.")


def measure(ordered, query, roles, heard, label_sets, details, fixed):
    qid = query["id"]
    for condition, labels in label_sets.items():
        if condition in {"review_seed", "review_pool", "review_independent"} and qid not in REVIEWED:
            continue
        details.append({
            **fixed, "judgments": condition, "query_id": qid, "problem_id": query["problem_id"],
            "scope": query["whole_or_part"], "has_signal": heard,
            **evaluate(ordered, labels.get(qid, {}), roles),
        })


def compute_runs(entries, queries, backend, output, outcome, baseline):
    semantic_class = LsaIndex if backend == "lsa" else E5Index
    ids = [item["id"] for item in entries]
    role_by_id = {item["id"]: item["role"] for item in entries}
    tie_map = {entry: i for i, entry in enumerate(stable_order(ids))}
    tie = [tie_map[entry] for entry in ids]
    pool = set()
    bundles = []
    cost = []
    for representation in DESCRIPTIONS:
        for corpus_language in ("ko", "en"):
            documents = [item[representation][corpus_language] for item in entries]
            started = perf_counter()
            m1 = LexicalIndex(documents)
            bm25_seconds = perf_counter() - started
            started = perf_counter()
            m2 = semantic_class(documents)
            semantic_seconds = perf_counter() - started
            for query_language, lang in LANGUAGES:
                if lang != corpus_language:
                    continue
                query_text = [query[query_language] for query in queries]
                started = perf_counter()
                lexical = m1.scores(query_text)
                after_lexical = perf_counter()
                semantic = m2.scores(query_text)
                after_semantic = perf_counter()
                fused = reciprocal_rank_fusion(lexical, semantic)
                after_fused = perf_counter()
                measurements = (
                    (m1.size_bytes, bm25_seconds, after_lexical - started),
                    (m2.size_bytes, semantic_seconds, after_semantic - after_lexical),
                    (m1.size_bytes + m2.size_bytes, bm25_seconds + semantic_seconds,
                     after_fused - started),
                )
                for method, matrix, (size, build, score_time) in zip(
                    METHODS, (lexical, semantic, fused), measurements, strict=True
                ):
                    run_name = f"{method}_{representation}_{query_language}-{corpus_language}"
                    fixed = dict(
                        m2_backend=backend, corpus=outcome, method=method,
                        representation=representation, query_language=query_language,
                        corpus_language=corpus_language,
                    )
                    score_started = perf_counter()
                    runs = []
                    for query, scores in zip(queries, matrix, strict=True):
                        indexes = ranking(scores, tie)
                        ordered = [ids[index] for index in indexes]
                        heard = has_signal(scores)
                        if outcome == "full":
                            qid = query["id"]
                            pool.update((qid, e) for e in ordered[:10] if e not in baseline.get(qid, {}))
                            runs.append({
                                "query_id": qid, "has_signal": heard,
                                "top20": [{"id": ids[index], "score": round(float(scores[index]), 12)}
                                          for index in indexes[:20]],
                            })
                        bundles.append((fixed, query, ordered, heard, role_by_id))
                    cost.append({
                        **fixed, "entries": len(entries), "logical_index_bytes": size,
                        "build_seconds": round(build, 6),
                        "search_seconds": round(score_time + perf_counter() - score_started, 6),
                    })
                    if outcome == "full":
                        atomic_write(output / "runs" / f"{run_name}.json",
                                     json.dumps({**fixed, "queries": runs}, indent=2) + "\n")
    return bundles, cost, pool


def run_all(root, backend):
    entries = sorted(jsonl(root / "corpus/entries.jsonl"), key=lambda entry: entry["id"])
    queries = jsonl(root / "queries/queries.jsonl")
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))["sources"]
    validate_inputs(entries, queries, sources)
    query_ids = {query["id"] for query in queries}
    entry_ids = {item["id"] for item in entries}
    baseline = judgments(root / "qrels/qrels.tsv", query_ids, entry_ids)
    if set(baseline) != query_ids:
        raise ValueError("Initial judgments must cover every query.")
    output = root / "results"
    (output / "runs").mkdir(parents=True, exist_ok=True)
    half_ids = set(random.Random(SEED).sample(sorted(entry_ids), len(entries) // 2))
    subsets = {
        "full": entries,
        "nodistractors": [entry for entry in entries if not entry["distractor"]],
        "half": [entry for entry in entries if entry["id"] in half_ids],
    }
    details = []
    costs = []
    label_sets = {"seed": baseline}
    pooled_path = output / "pooled_judgments.tsv"
    independent_path = root / "qrels/independent.tsv"
    with threadpool_limits(limits=1):
        for subset, selected in subsets.items():
            bundles, cost, pool = compute_runs(selected, queries, backend, output, subset, baseline)
            costs.extend(cost)
            if subset == "full":
                write_rows(output / "pool_candidates.tsv",
                           [{"query_id": q, "entry_id": e} for q, e in sorted(pool)], delimiter="\t")
                print(f"Pool contains {len(pool)} previously unjudged query-entry pairs.")
                if pooled_path.is_file():
                    added = judgments(pooled_path, query_ids, entry_ids)
                    if {(q, e) for q in added for e in added[q]} != pool:
                        raise ValueError("Post-run labels must cover exactly the selected pool.")
                    label_sets["pooled"] = {q: baseline[q] | added[q] for q in query_ids}
                if independent_path.is_file():
                    independent = judgments(independent_path, query_ids, entry_ids)
                    if set(independent) != REVIEWED:
                        raise ValueError("Independent review does not match the fixed 15 query IDs.")
                    label_sets["review_seed"] = baseline
                    if "pooled" in label_sets:
                        label_sets["review_pool"] = label_sets["pooled"]
                    label_sets["review_independent"] = independent
            for fixed, query, ordered, heard, role_by_id in bundles:
                measure(ordered, query, role_by_id, heard, label_sets, details, fixed)
    grouped = defaultdict(list)
    keys = ("m2_backend", "corpus", "method", "representation", "query_language",
            "corpus_language", "judgments")
    for row in details:
        key = tuple(row[field] for field in keys)
        grouped[(*key, "all")].append(row)
        grouped[(*key, row["scope"])].append(row)
    summary = [{**dict(zip((*keys, "scope"), key, strict=True)), **summarize(rows)}
               for key, rows in sorted(grouped.items())]
    write_rows(output / "per_query.csv", details)
    write_rows(output / "metrics.csv", summary)
    write_rows(output / "index_cost.csv", costs)
    print(f"{len(entries)} entries, {len(queries)} queries, 27 full-corpus runs.")
    print(f"{len(details)} per-query evaluations; label sets: {', '.join(label_sets)}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", required=True, help="run the full matrix")
    parser.add_argument("--m2", choices=("lsa", "e5"), default="lsa", help="semantic backend")
    parser.add_argument("--root", type=Path, default=ROOT, help="experiment directory")
    args = parser.parse_args()
    random.seed(SEED)
    run_all(args.root.resolve(), args.m2)


if __name__ == "__main__":
    main()
