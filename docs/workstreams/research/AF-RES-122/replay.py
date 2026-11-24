"""Replay the two query views against the same 16 features and alias table."""

import argparse
import csv
import hashlib
from pathlib import Path

from prepare import ENGLISH, HERE, KOREAN_WORD, packed, read_csv, read_jsonl, sha


CONDITIONS = ("raw-off", "raw-on", "masked-off", "masked-on")
LIMITS = {"investigation": 8, "display": 3}
INPUT_FILES = (
    "catalog.csv",
    "aliases.csv",
    "evidence/query-inputs.jsonl",
    "evidence/controls-query-inputs.jsonl",
)
VIEW_FIELDS = {"english_positions", "korean_sequences", "exact_ids"}
COMPARISONS = (
    ("raw-alias", "raw-off", "raw-on"),
    ("masked-alias", "masked-off", "masked-on"),
    ("off-symbol", "masked-off", "raw-off"),
    ("on-symbol", "masked-on", "raw-on"),
)


def read_inputs(root):
    cards = read_csv(root / INPUT_FILES[0])
    features = {
        card["feature_id"]: {word.lower() for word in ENGLISH.findall(card["english_terms"])}
        for card in cards
    }
    expected = {f"{family}{index:02}" for family in ("D", "T") for index in range(1, 9)}
    if set(features) != expected or len(cards) != 16:
        raise ValueError("expected the 16 pinned feature slots exactly once")

    aliases = {feature: [] for feature in features}
    for row in read_csv(root / INPUT_FILES[1]):
        if row["status"] == "active":
            aliases[row["feature_id"]].append((row["alias_id"], tuple(KOREAN_WORD.findall(row["surface"]))))

    views = {}
    for path in INPUT_FILES[2:]:
        for row in read_jsonl(root / path):
            key = (row["request_id"], row["view"])
            payload = {field: row[field] for field in VIEW_FIELDS}
            if set(row) != VIEW_FIELDS | {"request_id", "view", "view_sha256", "projection_sha256"}:
                raise ValueError(f"{key}: unexpected input fields")
            if key in views or sha(packed(payload)) != row["projection_sha256"]:
                raise ValueError(f"{key}: duplicate or projection SHA mismatch")
            if not set(row["exact_ids"]) <= expected:
                raise ValueError(f"{key}: unexpected candidate ID")
            views[key] = row
    questions = sorted({request for request, _ in views})
    if set(views) != {(request, view) for request in questions for view in ("raw", "masked")}:
        raise ValueError("each question needs exactly the raw and masked views")
    return features, aliases, views, questions


def alias_match(sequences, phrase):
    for sequence in sequences:
        for start in range(len(sequence) - len(phrase) + 1):
            if sequence[start:start + len(phrase)] == phrase:
                return True
    return False


def score_query(view, enabled, features, aliases):
    sequences = [
        tuple(item[1] if item else None for item in items)
        for items in view["korean_sequences"]
    ] if enabled else []
    exact_ids = set(view["exact_ids"])
    english = set(view["english_positions"])
    scores = []
    cost = {
        "candidate_comparisons": len(features),
        "symbol_checks": len(features),
        "english_token_checks": sum(len(words) for words in features.values()),
        "alias_checks": sum(len(variants) for variants in aliases.values()) if enabled else 0,
    }
    for feature, vocabulary in features.items():
        overlap = sorted(word for word in vocabulary if word in english)
        hits = [
            (alias_id, phrase) for alias_id, phrase in aliases[feature]
            if enabled and alias_match(sequences, phrase)
        ]
        exact = feature in exact_ids
        alias_points = 4 * len({phrase for _, phrase in hits})
        scores.append({
            "feature_id": feature,
            "score": 12 * exact + len(overlap) + alias_points,
            "symbol_points": 12 * exact,
            "english_points": len(overlap),
            "english_overlap": "|".join(overlap),
            "alias_points": alias_points,
            "alias_hits": "|".join(alias_id for alias_id, _ in hits),
        })
    return sorted(scores, key=lambda item: (-item["score"], item["feature_id"])), cost


def rank_rows(request, condition, view, enabled, features, aliases, alias_hash):
    scores, cost = score_query(view, enabled, features, aliases)
    ranked = []
    positive = [row["feature_id"] for row in scores if row["score"] > 0]
    for position, score in enumerate(scores, 1):
        shown = position <= LIMITS["display"] and score["score"] > 0
        in_scope = position <= LIMITS["investigation"] and score["score"] > 0
        if not score["score"]:
            reason = "0점"
        elif shown:
            reason = "표시"
        elif in_scope:
            reason = "표시 상한"
        else:
            reason = "조사 상한"
        ranked.append({
            "request_id": request,
            "condition": condition,
            **score,
            "positive_rank": position if score["score"] else "",
            "investigation_rank": position if in_scope else "",
            "display_rank": position if shown else "",
            "reason": reason,
            "view_sha256": view["view_sha256"],
            "projection_sha256": view["projection_sha256"],
            "alias_sha256": alias_hash,
        })
    cost.update(positive_candidates=len(positive), display_links=min(len(positive), LIMITS["display"]))
    return ranked, positive, cost


def slot_rows(request, condition, positive):
    for stage, width in LIMITS.items():
        for slot in range(1, width + 1):
            feature = positive[slot - 1] if len(positive) >= slot else ""
            yield {
                "request_id": request,
                "condition": condition,
                "stage": stage,
                "slot": slot,
                "feature_id": feature,
                "reason": "양점 순위" if feature else (
                    "양점 후보 없음" if not positive else "양점 후보 수 부족"
                ),
            }


def comparison_rows(request, order):
    for name, before, after in COMPARISONS:
        for stage, width in LIMITS.items():
            left = order[before][:width]
            right = order[after][:width]
            yield {
                "request_id": request,
                "comparison": name,
                "stage": stage,
                "before": before,
                "after": after,
                "before_ids": "|".join(left),
                "after_ids": "|".join(right),
                "added": "|".join(fid for fid in right if fid not in left),
                "lost": "|".join(fid for fid in left if fid not in right),
                "moved": "|".join(
                    f"{fid}:{left.index(fid) + 1}>{index}"
                    for index, fid in enumerate(right, 1)
                    if fid in left and left.index(fid) + 1 != index
                ),
            }


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(data, output):
    features, aliases, views, questions = read_inputs(data)
    input_hashes = {name: file_sha(data / name) for name in INPUT_FILES}
    ranks, slots, comparisons, costs = [], [], [], []
    for request in questions:
        order = {}
        for condition in CONDITIONS:
            view, flag = condition.split("-")
            rows, positive, cost = rank_rows(
                request, condition, views[request, view], flag == "on", features,
                aliases, input_hashes["aliases.csv"]
            )
            order[condition] = positive
            ranks.extend(rows)
            slots.extend(slot_rows(request, condition, positive))
            costs.append({"request_id": request, "condition": condition, **cost})
        comparisons.extend(comparison_rows(request, order))

    output.mkdir(parents=True, exist_ok=True)
    files = {
        "ranks.csv": ranks,
        "slots.csv": slots,
        "comparisons.csv": comparisons,
        "replay-costs.csv": costs,
    }
    for name, rows in files.items():
        write_csv(output / name, rows)
    return {
        "query_count": len(questions) * len(CONDITIONS),
        "input_sha256": input_hashes,
        "output_sha256": {name: file_sha(output / name) for name in files},
        "output_rows": {name: len(rows) for name, rows in files.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=HERE, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    print(packed(replay(args.data, args.out)))


if __name__ == "__main__":
    main()
