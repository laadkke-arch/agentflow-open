"""Join the frozen adjudication and ranks to reconstruct the three report tables."""

import argparse
import collections
import csv
import json
from pathlib import Path

from replay import ROOT, read_jsonl

FILES = {
    ("verified", "natural"): "ranks.csv",
    ("verified", "exploratory"): "evidence/ranks-exploratory.csv",
    ("verified", "control"): "evidence/ranks-controls.csv",
    ("publisher_partial", "exploratory"): "evidence/ranks-exploratory-publisher.csv",
    ("publisher_partial", "control"): "evidence/ranks-controls-publisher.csv",
}
TRUTH = {
    "natural": "truth.csv",
    "exploratory": "evidence/truth-exploratory.csv",
    "control": "evidence/truth-controls.csv",
}
CONDITIONS = ("00", "10", "01", "11")


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"missing rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def condition(row):
    return row["alias"] + row["role"]


def ids(row, prefix, width):
    return {row[f"{prefix}{i:02}"] for i in range(1, width + 1)} - {""}


def classify_pass(query, direct, raw, display):
    if query["status"] != "ready":
        return "request_frame"
    if not direct:
        return "no_confirmed_direct_in_sample"
    if not direct & raw:
        return "retrieval"
    if not direct & display:
        return "display"
    if direct - display:
        return "partial_retrieval_or_display"
    return "displayed"


def table1(queries, judgments):
    result = []
    for query in queries:
        key = query["query_id"]
        truth = [pair for (qid, _), pair in judgments.items() if qid == key]
        by = collections.Counter(pair["verdict"] for pair in truth)
        direct = sum(pair["verdict"] == "direct" for pair in truth)
        pool = sum(val for status, val in by.items() if status != "vacant_request")
        result.append({
            "query_id": key, "layer": query["layer"], "languages": "en/ko",
            "source_url": query["url"], "source_edition": query["source_edition"], "source_location": query["source_location"],
            "original_excerpt": query["original_excerpt"], "en": query["en"], "ko": query["ko"],
            "operation": query["operation"], "preservation": query["preserve"],
            "direct_features": direct if pool else "", "evaluated_pairs": pool,
            "direct_ids": " ".join(fid for (qid, fid), row in judgments.items() if qid == key and row["verdict"] == "direct"),
            "partial_rows": by["partial"], "unconfirmed_rows": by["unverified"], "vacant_rows": by["vacant_request"],
            "source_revision": query["source_revision"], "limitation": query["limitation"],
        })
    return result


def table2_row(rank, feature, card, item, query, judge, stage, retrieval, display):
    comparisons = item.get("comparisons", {})
    aliases = ", ".join(x["ko"] for x in card["alias_publisher"])
    return {
        "profile": rank["profile"], "query_id": query["query_id"], "layer": query["layer"],
        "language": rank["language"], "alias": rank["alias"], "role": rank["role"],
        "investigation_rank": retrieval, "display_rank": display, "feature_id": feature,
        "title_en": card["title"], "label_ko_html": card["evidence_ko"]["label"],
        "publisher_label_ko": aliases, "verdict": judge["verdict"],
        "evidence_url": judge["candidate_evidence_url"], "evidence_location": judge["candidate_evidence_location"],
        "alternate_evidence_url": judge["alternate_evidence"], "query_evidence_url": query["url"],
        "query_evidence_location": query["source_location"], "occurrence_stage": stage,
        "matches": ", ".join(item.get("matched", [])),
        "role_conflicts": sum(c["state"] == "conflicting_role" for c in comparisons),
        "role_evidence": json.dumps(comparisons, ensure_ascii=False, sort_keys=True),
    }


def table2(ranks, queries, cards, judgments, supply):
    out = []
    for rank in ranks:
        qid = rank["query_id"]
        query = queries[qid]
        acceptable = supply[qid]
        raw = json.loads(rank["retrieved_json"])
        shown = {x["id"]: x["slot"] for x in json.loads(rank["display_json"])}
        for item in raw:
            fid = item["id"]
            decision = judgments[qid, fid]
            out.append(table2_row(rank, fid, cards[fid], item, query, decision,
                "displayed" if fid in shown else "display_cut", item["rank"], shown.get(fid, "")))
        for fid in sorted(acceptable - {item["id"] for item in raw}):
            out.append(table2_row(rank, fid, cards[fid], {}, query, judgments[qid, fid], "retrieval_miss", "", ""))
        blank_positions = (("investigation_vacancy", range(len(raw) + 1, 13)),
                           ("display_vacancy", range(len(shown) + 1, 4)))
        for name, positions in blank_positions:
            for pos in positions:
                blank_card = {"title": "", "evidence_ko": {"label": ""}, "alias_publisher": []}
                blank_judge = dict(verdict="", candidate_evidence_url="", candidate_evidence_location="", alternate_evidence="")
                stage = ("request_frame" if query["status"] != "ready" else
                         "no_confirmed_direct_in_sample" if not acceptable else name)
                out.append(table2_row(rank, "", blank_card, {}, query, blank_judge, stage,
                    pos if name == "investigation_vacancy" else "", pos if name == "display_vacancy" else ""))
    return out


def aggregate(ranks, queries, judgments, supply, costs):
    index = {(r["profile"], r["layer"], r["query_id"], r["language"], condition(r)): r for r in ranks}
    groups = collections.defaultdict(list)
    for r in ranks:
        groups[r["profile"], r["layer"], r["language"], condition(r)].append(r)
    rows = []
    trace = []
    for (profile, layer, language, method), group in groups.items():
        expected = [r for r in group if supply[r["query_id"]]]
        missing = sum(queries[r["query_id"]]["status"] != "ready" for r in group)
        counts = collections.Counter()
        for r in group:
            qid = r["query_id"]
            direct = supply[qid]
            raw = ids(r, "r", 12)
            show = ids(r, "d", 3)
            reference = index[profile, layer, qid, language, "00"]
            reference_shown = ids(reference, "d", 3)
            reference_raw = ids(reference, "r", 12)
            grade = {fid: judgments[qid, fid]["verdict"] for fid in show}
            counts.update(grade.values())
            counts["raw_direct"] += len(raw & direct)
            counts["added_direct_pool"] += len((raw - reference_raw) & direct)
            counts["lost_direct_pool"] += len((reference_raw - raw) & direct)
            counts["added_display_direct"] += len((show - reference_shown) & direct)
            counts["removed_display_direct"] += len((reference_shown - show) & direct)
            counts["new_confirmed_wrong"] += sum(grade[fid] == "conflict" for fid in show - reference_shown)
            counts["investigation_vacancies"] += 12 - len(raw)
            counts["display_vacancies"] += 3 - len(show)
            counts["stats_query_calls"] += int(r["execution"] == "executed")
            counts["sql"] += int(r["sql_statements"])
            trace.append({
                "profile": profile, "layer": layer, "query_id": qid, "language": language, "condition": method,
                "corpus_direct": sorted(direct) if r["execution"] == "executed" else None,
                "in_top12": sorted(raw & direct), "in_top3": sorted(show & direct),
                "lost_in_retrieval": sorted(direct - raw), "lost_in_display": sorted((direct & raw) - show),
                "role_and_search_rows": [x["id"] for x in json.loads(r["retrieved_json"])],
                "stage": classify_pass(queries[qid], direct, raw, show),
            })
        denominator = sum(len(supply[r["query_id"]]) for r in expected)
        receipt = costs["profiles"][profile]
        build = receipt["builds"][0]["index"]
        prepared = costs["preparation"]
        rows.append({
            "profile": profile, "layer": layer, "language": language, "method": method,
            "available_requests": len(group) - missing, "reserved_requests": len(group),
            "requests_with_direct": len(expected), "direct_pair_denominator": denominator,
            "in_top12_direct": counts["raw_direct"], "top3_direct": counts["direct"],
            "recall": counts["direct"] / denominator if denominator else "",
            "new_pool_direct": counts["added_direct_pool"], "lost_pool_direct": counts["lost_direct_pool"],
            "new_display_direct": counts["added_display_direct"], "lost_display_direct": counts["removed_display_direct"],
            "new_confirmed_wrong": counts["new_confirmed_wrong"], "confirmed_wrong": counts["conflict"],
            "partial": counts["partial"], "unconfirmed_display": counts["unverified"],
            "investigation_vacancies": counts["investigation_vacancies"], "display_vacancies": counts["display_vacancies"],
            "query_calls": counts["stats_query_calls"], "query_sql": counts["sql"],
            "base_source_documents": prepared["base_feature_document_count"], "base_token_rows": build["base_rows"],
            "alias_extra_documents": prepared["additional_publisher_alias_document_count"] if method[0] == "1" and profile == "publisher_partial" else 0,
            "alias_extra_token_rows": build["alias_rows"] if method[0] == "1" else 0,
            "alias_extra_evidence_bytes": build["alias_evidence_bytes"] if method[0] == "1" else 0,
            "role_extra_documents_over_base": prepared["additional_role_document_count_over_base"] if method[1] == "1" else 0,
            "role_data_bytes": build["role_evidence_bytes"] if method[1] == "1" else 0,
            "replay_agrees": receipt["repeat_agrees"], "unknown_or_missing_request": missing,
        })
    return rows, trace


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    root = args.root
    queries = {q["query_id"]: q for q in read_jsonl(root / "queries.jsonl") if q["layer"] != "variant"}
    cards = {c["feature_id"]: c for c in read_jsonl(root / "catalog.jsonl")}
    entries = [r for f in TRUTH.values() for r in csv_rows(root / f)]
    judgments = {(r["query_id"], r["feature_id"]): r for r in entries}
    supply = {q: {f for f in cards if judgments[q, f]["verdict"] == "direct"} for q in queries}
    costs = json.loads((root / "costs.json").read_text(encoding="utf-8"))
    ranks = [row for filename in FILES.values() for row in csv_rows(root / filename) if row["replay"] == "1"]
    frame = csv_rows(root / "frame.csv")
    sources = read_jsonl(root / "sources.jsonl")
    source_counts = collections.Counter(s["allocation"] for s in sources if s["unique_count"])
    corpus = {layer: {q: sorted(fids) for q, fids in supply.items() if queries[q]["layer"] == layer
                      and queries[q]["status"] == "ready"} for layer in TRUTH}
    t3, trace = aggregate(ranks, queries, judgments, supply, costs)
    cohort = {
        "paired_supplied_query_ids": {layer: sorted(q for q, fids in d.items() if fids) for layer, d in corpus.items()},
        "paired_results": [t for t in trace if t["corpus_direct"]],
    }
    args.out.mkdir(parents=True, exist_ok=False)
    write_csv(args.out / "table1.csv", table1(queries.values(), judgments))
    write_csv(args.out / "table2.csv", table2(ranks, queries, cards, judgments, supply))
    write_csv(args.out / "table3.csv", t3)
    summary = {
        "source_accounting": {
            "attempt_rows": len(sources),
            "distinct_source_urls": len({s["source_url"] for s in sources}),
            "distinct_landed_urls": len({s["landed_url"] for s in sources if s["landed_url"]}),
            "unique_count_by_allocation": dict(source_counts),
            "unique_lineages": len({s["lineage"] for s in sources if s["unique_count"]}),
            "unique_author_request_or_change_events": len({s["lineage"] for s in sources if s["unique_count"]
                                                            and s["allocation"] in {"request", "change"}}),
            "status": dict(collections.Counter(s["status"] for s in sources)),
        },
        "frame": {"counts": dict(collections.Counter(f["kind"] + "/" + f["status"] for f in frame))},
        "corpus_direct_by_query": corpus,
        "truth_designations": dict(collections.Counter(r["layer"] + "/" + r["verdict"] for r in entries)),
        "summary_rows": t3, "positive_bilingual_cohort": cohort, "query_traces": trace,
    }
    (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
