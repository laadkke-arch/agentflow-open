# Adapted from AF-RES-012 cb602858378db90adb1f085953016267f9afbd6d (src/metrics.py).
"""Metrics over eligible documents and sparse, graded relevance judgments."""
from math import log2
from statistics import mean


ROLES = ("product", "component", "principle")
METRICS = ("recall_at10", "ndcg_at10", "mrr", "near_misses_at10",
           "recall_grade2_at10", *(f"{role}_recall_at10" for role in ROLES))


def dcg(grades):
    return sum((2 ** grade - 1) / log2(rank + 1) for rank, grade in enumerate(grades, 1))


def evaluate(ranking, labels, roles, k=10):
    """Missing labels get gain zero; missing denominators stay undefined."""
    relevant = {entry: int(grade) for entry, grade in labels.items()
                if grade in {"1", "2"} and entry in roles}
    top = ranking[:k]
    hits = relevant.keys() & set(top)
    ideal = dcg(sorted(relevant.values(), reverse=True)[:k])
    first = next((rank for rank, entry in enumerate(ranking, 1) if entry in relevant), None)
    strong = {entry for entry, grade in relevant.items() if grade == 2}
    row = {
        "recall_at10": len(hits) / len(relevant) if relevant else None,
        "ndcg_at10": dcg([relevant.get(entry, 0) for entry in top]) / ideal if ideal else None,
        "mrr": 1.0 / first if first else 0.0,
        "near_misses_at10": sum(labels.get(entry) == "N" for entry in top),
        "recall_grade2_at10": len(strong & hits) / len(strong) if strong else None,
        "first_relevant_rank": first,
        "relevant_in_corpus": len(relevant),
        "grade2_in_corpus": len(strong),
        "judged_at10": sum(entry in labels for entry in top),
    }
    for role in ROLES:
        wanted = {entry for entry in relevant if roles[entry] == role}
        row[f"{role}_recall_at10"] = len(wanted & hits) / len(wanted) if wanted else None
    return row


def summarize(rows):
    summary = {}
    for field in METRICS:
        values = [row[field] for row in rows if row[field] is not None]
        summary[field] = mean(values) if values else None
        summary[f"{field}_n"] = len(values)
    summary["queries"] = len(rows)
    summary["queries_without_relevant"] = sum(row["relevant_in_corpus"] == 0 for row in rows)
    summary["queries_without_signal"] = sum(not row["has_signal"] for row in rows)
    summary["mean_judged_at10"] = mean(row["judged_at10"] for row in rows)
    return summary
