# Adapted from AF-RES-012 cb602858378db90adb1f085953016267f9afbd6d (src/run.py).
"""Rank the fixed AF-RES-014 corpus and score locked and pooled answer labels."""
import argparse
from collections import defaultdict
import csv
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import random
import subprocess
from time import perf_counter
from urllib.parse import urlsplit

from threadpoolctl import threadpool_limits

from queries.generate import load_inputs
from .constraints import conflicts, postprocess, query_concepts
from .language import augment
from .metrics import evaluate, summarize
from .search import (
    E5Index, LexicalIndex, LsaIndex, has_signal, ranking, reciprocal_rank_fusion,
    stable_order,
)

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTIONS = {"a": "D-a", "b": "D-b", "c": "D-c", "filter": "D-b", "penalty": "D-b"}
SAMPLE_SEED = 14014


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def judgments(path, queries, entries, *, optional=False):
    if optional and not path.exists():
        return {}
    result = defaultdict(dict)
    seen = set()
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file, delimiter="\t"):
            query, entry, grade = row["query_id"], row["doc_id"], row["grade"]
            if query not in queries or entry not in entries or grade not in {"0", "1", "2", "N", "U"}:
                raise ValueError(f"Unknown query, entry or grade: {query}/{entry}/{grade}")
            if (query, entry) in seen:
                raise ValueError(f"Duplicate judgment: {query}/{entry}")
            seen.add((query, entry))
            if grade != "U":
                result[query][entry] = grade
    return result


def atomic_write(path, content):
    pending = path.with_suffix(path.suffix + ".tmp")
    pending.write_text(content, encoding="utf-8")
    pending.replace(path)


def write_json(path, value):
    atomic_write(path, json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_rows(path, rows, delimiter=",", fields=None):
    pending = path.with_suffix(path.suffix + ".tmp")
    with pending.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fields or rows[0].keys(), delimiter=delimiter,
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    pending.replace(path)


def validate_inputs(entries, queries, sources):
    if len({e["id"] for e in entries}) != len(entries):
        raise ValueError("Duplicate document ID")
    if len({q["id"] for q in queries}) != len(queries):
        raise ValueError("Duplicate query ID")
    source_ids = {source["id"] for source in sources}
    evidence_urls = {source["url"] for source in sources}
    for item in entries:
        if item["role"] not in {None, "product", "component", "principle", "mixed", "other"}:
            raise ValueError(f"Unknown role: {item['id']}")
        if not item["source_ids"] or set(item["source_ids"]) - source_ids:
            raise ValueError(f"Missing provenance: {item['id']}")
        if any(not item[field].strip() for field in ("D-a", "D-b", "D-c")):
            raise ValueError(f"Empty field: {item['id']}")
        if item["D-c"] != item["D-b"] and not item["D-c"].startswith(item["D-b"] + " "):
            raise ValueError(f"D-c did not retain D-b: {item['id']}")
        if urlsplit(item["url"]).scheme not in {"http", "https"}:
            raise ValueError(f"Nonpublic URL schema: {item['id']}")
        for row in item["exclusions"]:
            if row["evidence_url"] not in evidence_urls or row["polarity"] not in {"required", "unsupported"}:
                raise ValueError(f"Invalid exclusion: {item['id']}/{row['target']}")


def matches_by_query(queries, entries):
    result = {}
    mapping = {}
    for query in queries:
        qid = query["id"]
        needs, bans, mapped = query_concepts(query["must"])
        mapping[qid] = {"must_count": len(query["must"]), "must_mapped": mapped}
        result[qid] = {}
        for number, item in enumerate(entries):
            contradicted = conflicts(item["exclusions"], needs, bans)
            if contradicted:
                result[qid][number] = sorted(contradicted)
    return result, mapping


def induction(backend, descriptions, questions, raw_docs, raw_queries):
    lexical = LexicalIndex(descriptions).scores(questions)
    if backend == "lsa":
        semantic = LsaIndex(descriptions).scores(questions)
    else:
        semantic = E5Index(raw_docs).scores(raw_queries)
    return {"BM25": lexical, "LSA" if backend == "lsa" else "E5": semantic,
            "RRF": reciprocal_rank_fusion(lexical, semantic)}


def compute_runs(entries, queries, raw_queries, backend, output, answer):
    ids = [item["id"] for item in entries]
    tie_map = {entry: i for i, entry in enumerate(stable_order(ids))}
    tie = [tie_map[entry] for entry in ids]
    matches, mapping = matches_by_query(queries, entries)
    pool = set()
    bundles = {}
    for bridge, conditions in [("terms", tuple(DESCRIPTIONS)), ("raw", ("b", "c"))]:
        questions = [augment(x) for x in raw_queries] if bridge == "terms" else raw_queries
        matrices = {}
        for condition in conditions:
            field = DESCRIPTIONS[condition]
            if field not in matrices:
                raw_docs = [item[field] for item in entries]
                documents = [augment(x) for x in raw_docs] if bridge == "terms" else raw_docs
                matrices[field] = induction(backend, documents, questions, raw_docs, raw_queries)
            for method, scores in matrices[field].items():
                run_rows = {}
                for query, row in zip(queries, scores, strict=True):
                    qid = query["id"]
                    base = ranking(row, tie)
                    match = matches[qid] if condition in {"filter", "penalty"} else {}
                    order = postprocess(base, match, condition)
                    pool.update((qid, ids[i]) for i in order[:10] if ids[i] not in answer.get(qid, {}))
                    run_rows[qid] = {
                        "order": order, "has_signal": has_signal(row),
                        "conflicts": sorted(match), "base_top10": base[:10],
                    }
                identity = f"{bridge}-{method}-{condition}"
                bundle = {"backend": backend, "bridge": bridge, "method": method,
                          "condition": condition, "description": field, "queries": run_rows}
                write_json(output / "runs" / f"{identity}.json", bundle)
                bundles[identity] = bundle
    write_json(output / "doc_order.json", ids)
    write_json(output / "constraint_coverage.json", {
        qid: {**values, "matches": [
            {"doc_id": ids[number], "concepts": concepts} for number, concepts in matches[qid].items()
        ]} for qid, values in mapping.items()
    })
    pool_rows = [{"query_id": qid, "doc_id": doc} for qid, doc in sorted(pool)]
    write_rows(output / "pool_candidates.tsv", pool_rows, "\t", ["query_id", "doc_id"])
    return bundles


def measure(bundles, queries, roles, ids, label_sets, reviewed):
    output = []
    for bundle in bundles.values():
        fixed = {key: val for key, val in bundle.items() if key != "queries"}
        for qid, row in bundle["queries"].items():
            q = queries[qid]
            ranking_ids = [ids[idx] for idx in row["order"]]
            base_top = {ids[idx] for idx in row["base_top10"]}
            conflict_ids = {ids[idx] for idx in row["conflicts"]}
            for pass_name, judgments_by_query in label_sets.items():
                if pass_name.startswith("review_") and qid not in reviewed:
                    continue
                labels = judgments_by_query.get(qid, {})
                relevant = {doc for doc, grade in labels.items() if grade in {"1", "2"}}
                removed = conflict_ids if fixed["condition"] == "filter" else set()
                output.append({
                    **fixed, "judgments": pass_name, "query_id": qid, "source": q["source"],
                    "scope": q["whole_or_part"], "i5": q["I5"], "has_signal": row["has_signal"],
                    "slots_at10": len(ranking_ids[:10]), "conflicts": len(conflict_ids),
                    "removed_relevant": len(relevant & removed),
                    "removed_top10_relevant": len(relevant & removed & base_top),
                    "displaced_top10_relevant": len((relevant & base_top) - set(ranking_ids[:10]))
                    if fixed["condition"] == "penalty" else 0,
                    **evaluate(ranking_ids, labels, roles),
                })
    return output


def aggregates(details):
    groups = defaultdict(list)
    for row in details:
        base = tuple(row[key] for key in ["backend", "bridge", "method", "condition", "description", "judgments"])
        scopes = ["all", row["scope"], row["source"]]
        if row["scope"] == "part":
            scopes.append("part_i5" if row["i5"] == "present" else "part_no_i5")
        for scope in scopes:
            groups[(*base, scope)].append(row)
    keys = ["backend", "bridge", "method", "condition", "description", "judgments", "scope"]
    result = []
    for key, rows in sorted(groups.items()):
        slots = sum(x["slots_at10"] for x in rows)
        counts = {
            "original": sum(row["source"] == "original" for row in rows),
            "summary": sum(row["source"] == "summary" for row in rows),
            "slots_at10": slots,
            "near_miss_count": sum(row["near_misses_at10"] for row in rows),
        }
        for field in ["conflicts", "removed_relevant", "removed_top10_relevant", "displaced_top10_relevant"]:
            counts[field] = sum(row[field] for row in rows)
        result.append({
            **dict(zip(keys, key, strict=True)), **summarize(rows), **counts,
            "n_per_slot": counts["near_miss_count"] / slots if slots else None,
        })
    return result


def merge_labels(main, extra, query_ids):
    return {qid: main.get(qid, {}) | extra.get(qid, {}) for qid in sorted(query_ids)}


def compute_metrics(entries, queries, answer, bundles, output, stage):
    roles = {item["id"]: item["role"] for item in entries}
    qids = {row["id"]: row for row in queries}
    reviewed = sorted(random.Random(SAMPLE_SEED).sample(sorted(qids), 10))
    write_json(output / "review_sample.json", {"seed": SAMPLE_SEED, "query_ids": reviewed})
    labels = {"answers": answer}
    if stage != "initial":
        pool = judgments(ROOT / "qrels/pooled.tsv", qids, roles, optional=True)
        independent = judgments(ROOT / "qrels/independent.tsv", qids, roles, optional=True)
        labels.update(
            pooled=merge_labels(answer, pool, qids),
            review_answers=answer,
            review_pool=merge_labels(answer, pool, qids),
            review_independent=merge_labels(answer, independent, qids),
        )
    details = measure(bundles, qids, roles, list(roles), labels, reviewed)
    summary = aggregates(details)
    write_rows(output / "metrics.csv", summary)
    write_rows(output / "per_query.csv", details)
    return len(summary), len(details)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def run_all(output, backend, stage):
    start = perf_counter()
    output.mkdir(parents=True, exist_ok=True)
    (output / "runs").mkdir(exist_ok=True)
    entries = sorted(jsonl(ROOT / "corpus/entries.jsonl"), key=lambda entry: entry["id"])
    queries, texts = map(list, zip(*load_inputs(), strict=True))
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))["sources"]
    validate_inputs(entries, queries, sources)
    answer = judgments(ROOT / "qrels/answers.tsv", {q["id"] for q in queries}, {e["id"] for e in entries})
    if stage == "evaluate":
        bundles = {path.stem: json.loads(path.read_text()) for path in sorted((output / "runs").glob("*.json"))}
        ids = json.loads((output / "doc_order.json").read_text())
        if ids != [entry["id"] for entry in entries] or not bundles:
            raise ValueError("Run inputs do not match the existing document order or no runs exist")
        if set(x["backend"] for x in bundles.values()) != {backend}:
            raise ValueError("Evaluation backend differs from the existing runs")
    else:
        # Use the same ordering as the evaluate-only path to keep CSVs reproducible.
        bundles = dict(sorted(compute_runs(entries, queries, texts, backend, output, answer).items()))
    metrics, query_rows = compute_metrics(entries, queries, answer, bundles, output, stage)
    recorded = {
        "begin_input_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(), "platform": platform.platform(),
        "stage": stage, "backend": backend, "rank_files": len(bundles),
        "metric_rows": metrics, "per_query_rows": query_rows, "queries": len(queries),
        "corpus_entries": len(entries), "seconds": round(perf_counter() - start, 3),
        "input_sha256": {str(path.relative_to(ROOT)): file_hash(path) for path in
                         [ROOT / "corpus/entries.jsonl", ROOT / "queries/metadata.json",
                          ROOT / "qrels/answers.tsv", ROOT / "src/concepts.tsv",
                          ROOT / "qrels/EXCLUSIONS.md"]},
        "output_sha256": {str(path.relative_to(output)): file_hash(path) for path in
                          sorted((output / "runs").glob("*.json"))},
    }
    for filename in ("pooled.tsv", "independent.tsv"):
        path = ROOT / "qrels" / filename
        if stage != "initial" and path.exists():
            recorded["input_sha256"][f"qrels/{filename}"] = file_hash(path)
    write_json(output / ("initial-receipt.json" if stage == "initial" else "evaluation-receipt.json"), recorded)
    print(json.dumps({key: recorded[key] for key in ("queries", "corpus_entries", "rank_files", "metric_rows", "seconds")}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("lsa", "e5"), default="lsa")
    parser.add_argument("--stage", choices=("initial", "all", "evaluate"), default="initial")
    parser.add_argument("--output", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    with threadpool_limits(limits=1):
        run_all(args.output, args.backend, args.stage)


if __name__ == "__main__":
    main()
