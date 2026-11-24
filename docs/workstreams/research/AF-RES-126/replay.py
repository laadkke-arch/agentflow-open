"""Replay four pinned Korean matching policies without reading relevance labels."""

import argparse
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

from capture import HERE, POLICIES, PREVIOUS, VIEWS, aliases_by_phrase, find_aliases, load_previous, sparse_runs


VIEW_INPUTS = ("evidence/forum-inputs.jsonl", "evidence/controls-inputs.jsonl")
AUDIT_INPUTS = ("evidence/forum-audit.jsonl", "evidence/controls-audit.jsonl")
PREVIOUS_INPUTS = (
    "prepare.py", "replay.py", "catalog.csv", "aliases.csv", "ranks.csv",
    "evidence/query-inputs.jsonl", "evidence/controls-query-inputs.jsonl", "evidence/controls.jsonl",
)


def checked_views(data, prepare, legacy):
    views = {}
    for name in VIEW_INPUTS:
        for row in prepare.read_jsonl(data / name):
            key = (row["request_id"], row["view"])
            basic = {field: row[field] for field in legacy.VIEW_FIELDS}
            extra = {field: row[field] for field in ("korean_retained_runs", "korean_words")}
            if key in views or prepare.sha(prepare.packed(basic)) != row["projection_sha256"]:
                raise ValueError(f"{key}: duplicate or predecessor projection mismatch")
            if prepare.sha(prepare.packed(extra)) != row["extended_projection_sha256"]:
                raise ValueError(f"{key}: extended projection mismatch")
            views[key] = row
    ids = {request for request, _ in views}
    if set(views) != {(request, view) for request in ids for view in VIEWS}:
        raise ValueError("every replayed request needs exactly one raw and masked input")
    return views


def check_baseline(data, prior, prepare, legacy, features, aliases, views, previous_views, alias_sha):
    openings = prepare.read_jsonl(data / "openings.jsonl")
    old_ids = {row["request_id"] for row in openings if row["status"] == "hash_identical"}
    old_ids |= {request for request, _ in previous_views if request.startswith("C")}
    previous_ranks = {
        (row["request_id"], row["condition"], row["feature_id"]): row
        for row in prepare.read_csv(prior / "ranks.csv")
    }
    checked = 0
    for request in sorted(old_ids):
        for view in VIEWS:
            current = views[request, view]
            previous = previous_views[request, view]
            if {key: current[key] for key in previous} != previous:
                raise ValueError(f"{request}/{view}: A/B projection differs from the predecessor")
            for enabled in (False, True):
                condition = f"{view}-{'on' if enabled else 'off'}"
                rows = legacy.rank_rows(request, condition, current, enabled, features, aliases, alias_sha)[0]
                for row in rows:
                    old = previous_ranks[request, condition, row["feature_id"]]
                    if {field: str(value) for field, value in row.items()} != old:
                        raise ValueError(f"{request}/{condition}/{row['feature_id']}: A/B score or rank differs")
                    checked += 1
    return {"request_ids": sorted(old_ids), "view_count": len(old_ids) * len(VIEWS), "rank_rows": checked}


def eligible_hits(matches, policy):
    return [hit for hit in matches if hit["first_policy"] <= policy]


def ranking(request, view_name, view, policy, hits, features, aliases, legacy, alias_sha):
    scoring_view = view
    if policy in ("C", "D"):
        # The fixed scorer accepts sets of canonical phrases as separate runs.
        # Copying one accepted phrase into one run preserves the fixed weights.
        scoring_view = {
            **view,
            "korean_sequences": [
                [[hit["start"], word] for word in hit["phrase"].split()] for hit in hits
            ],
        }
    rows, positive, cost = legacy.rank_rows(
        request, f"{view_name}-{policy}", scoring_view, policy != "A", features, aliases, alias_sha
    )
    by_feature = defaultdict(list)
    for hit in hits:
        by_feature[hit["feature_id"]].append(hit)
    for row in rows:
        feature_hits = by_feature[row["feature_id"]]
        if set(row["alias_hits"].split("|")) - {""} != {hit["alias_id"] for hit in feature_hits}:
            raise ValueError(f"{request}/{view_name}/{policy}: scorer and matcher disagree")
        row["alias_positions"] = "|".join(
            f"{hit['alias_id']}@{hit['start']}:{hit['end']}({hit['first_policy']})"
            for hit in feature_hits
        )
        row["english_positions"] = "|".join(
            f"{word}@{','.join(map(str, view['english_positions'][word]))}"
            for word in row["english_overlap"].split("|") if word
        )
        row["extended_projection_sha256"] = view["extended_projection_sha256"]
    return rows, positive, cost


def boundary_checks(prepare, legacy, glossary, features, aliases, alias_sha):
    cases = (
        ("축\t순서를", "A11", "C"),
        ("축\n순서에", "A11", "C"),
        ("축, 순서를", "A11", ""),
        ("앞축 순서를", "A11", ""),
        ("축 뒤순서는", "A11", "D"),
        ("축 순서로는", "A11", "D"),
        ("축 순서에서", "A11", "C"),
        ("뷰어", "A04", "D"),
        ("복사본에", "A05", "C"),
        (unicodedata.normalize("NFD", "복사본을"), "A05", "C"),
    )
    for body, alias_id, expected in cases:
        body = unicodedata.normalize("NFC", body)
        runs, _ = sparse_runs(prepare, body, glossary)
        found = [hit["first_policy"] for hit in find_aliases(runs, glossary)[0] if hit["alias_id"] == alias_id]
        if found != ([expected] if expected else []):
            raise ValueError(f"boundary check for {body!r}: {found} != {expected!r}")

    body = "축 순서를 기록하고 축 순서를 유지한다."
    runs, _ = sparse_runs(prepare, body, glossary)
    hits = eligible_hits(find_aliases(runs, glossary)[0], "C")
    view = {
        "exact_ids": [], "english_positions": {}, "view_sha256": "",
        "projection_sha256": "", "extended_projection_sha256": "",
    }
    rows = ranking("boundary", "raw", view, "C", hits, features, aliases, legacy, alias_sha)[0]
    target = next(row for row in rows if row["feature_id"] == "T03")
    if len(hits) != 2 or target["alias_points"] != 4:
        raise ValueError("two occurrences of one alias must score exactly once")

    body = "축 torch.transpose 순서를"
    names, tensor = prepare.names_for(prepare.read_csv(legacy.HERE / "catalog.csv"))
    spans = list(prepare.find_spans(body, names, tensor))
    masked = list(body)
    for span in spans:
        masked[span["start"]:span["end"]] = span["after"]
    for text, expected in ((body, []), ("".join(masked), ["A11"])):
        run, _ = sparse_runs(prepare, text, glossary)
        observed = [hit["alias_id"] for hit in find_aliases(run, glossary)[0]]
        if observed != expected:
            raise ValueError("mask-created whitespace boundary check disagrees")
    return len(cases) + 2


def change_rows(request, view_name, before, after, left, right, limits):
    left_ranks = {feature: rank for rank, feature in enumerate(left, 1)}
    right_ranks = {feature: rank for rank, feature in enumerate(right, 1)}
    for stage, cap in limits.items():
        old, new = left[:cap], right[:cap]
        yield {
            "request_id": request, "view": view_name, "before": before, "after": after, "stage": stage,
            "before_ids": "|".join(old), "after_ids": "|".join(new),
            "added": "|".join(f"{fid}:{left_ranks.get(fid, '0')}>{right_ranks[fid]}" for fid in new if fid not in old),
            "lost": "|".join(f"{fid}:{left_ranks[fid]}>{right_ranks.get(fid, '0')}" for fid in old if fid not in new),
            "moved": "|".join(
                f"{fid}:{left_ranks[fid]}>{right_ranks[fid]}"
                for fid in new if fid in old and left_ranks[fid] != right_ranks[fid]
            ),
        }


def domain_replay(data, prepare):
    rows = []
    for case in prepare.read_jsonl(data / "evidence/domain-inputs.jsonl"):
        phrase = tuple(case["alias"].split())
        glossary = {case["case_id"]: (case["alias_entity"], phrase)}
        runs, _ = sparse_runs(prepare, unicodedata.normalize("NFC", case["body"]), glossary)
        found = find_aliases(runs, glossary)[0]
        policies = "".join(policy for policy in POLICIES if eligible_hits(found, policy))
        if policies != case["expect"]:
            raise ValueError(f"{case['case_id']}: domain contrast differs from its frozen expectation")
        rows.append({
            "case_id": case["case_id"], "alias": case["alias"], "body": case["body"],
            "input_kind": case["input_kind"], "matching_policies": policies,
            "alias_entity": case["alias_entity"], "body_entity": case["body_entity"],
            "same_entity": case["alias_entity"] == case["body_entity"],
            "source_ids": "|".join(case["evidence"]), "role": case["role"],
        })
    return rows


def replay(data, prior, output):
    prepare, legacy = load_previous(prior)
    features, aliases, previous_views, _ = legacy.read_inputs(prior)
    glossary = aliases_by_phrase(prepare, prior / "aliases.csv")
    if len(glossary) != 12:
        raise ValueError("the pinned matcher requires exactly 12 active alias rows")

    views = checked_views(data, prepare, legacy)
    alias_sha = legacy.file_sha(prior / "aliases.csv")
    baseline = check_baseline(data, prior, prepare, legacy, features, aliases, views, previous_views, alias_sha)
    smoke = boundary_checks(prepare, legacy, glossary, features, aliases, alias_sha)
    tiers = {
        row["request_id"]: row["status"] for row in prepare.read_jsonl(data / "openings.jsonl")
    }
    tiers.update((row["request_id"], "existing_control") for row in prepare.read_jsonl(prior / "evidence/controls.jsonl"))
    tiers.update((row["request_id"], "new_control") for row in prepare.read_jsonl(data / "controls.jsonl"))
    audits = {
        row["request_id"]: row for name in AUDIT_INPUTS for row in prepare.read_jsonl(data / name)
    }
    if set(audits) != {request for request, _ in views}:
        raise ValueError("each scored request needs a mask audit")

    ranks, slots, changes, costs = [], [], [], []
    current_orders = {}
    for (request, view_name), view in sorted(views.items()):
        sha_field = "raw_nfc_sha256" if view_name == "raw" else "masked_nfc_sha256"
        if audits[request][sha_field] != view["view_sha256"]:
            raise ValueError(f"{request}/{view_name}: mask audit SHA differs from the view")
        mask_spans = audits[request]["mask"] if view_name == "raw" else []
        matches, inspections = find_aliases(view["korean_retained_runs"], glossary)
        orders = {}
        for policy in POLICIES:
            hits = eligible_hits(matches, policy)
            batch, order, cost = ranking(request, view_name, view, policy, hits, features, aliases, legacy, alias_sha)
            orders[policy] = order
            for row in batch:
                spans = [f"{span['start']}:{span['end']}" for span in mask_spans if span["feature_id"] == row["feature_id"]]
                ranks.append({
                    "tier": tiers[request], "view": view_name, "policy": policy,
                    **row, "symbol_positions": "|".join(spans),
                })
            slots.extend(
                {"view": view_name, "policy": policy, **row}
                for row in legacy.slot_rows(request, f"{view_name}-{policy}", order)
            )
            costs.append({
                "request_id": request, "tier": tiers[request], "view": view_name, "policy": policy, **cost,
                "opening_korean_words": view["korean_words"],
                "candidate_windows_shared_bcd": inspections.get("windows", 0),
                "final_tokens_shared_bcd": inspections.get("final_tokens", 0),
                "accepted_spans": len(hits),
                "retained_runs": len(view["korean_retained_runs"]),
            })
        current_orders[request, view_name] = orders
        for before, after in zip(POLICIES, POLICIES[1:]):
            changes.extend(change_rows(request, view_name, before, after, orders[before], orders[after], legacy.LIMITS))

    for request in sorted({request for request, _ in views}):
        for policy in POLICIES:
            left = current_orders[request, "raw"][policy]
            right = current_orders[request, "masked"][policy]
            changes.extend(change_rows(request, "raw→masked", f"raw-{policy}", f"masked-{policy}", left, right, legacy.LIMITS))

    output.mkdir(parents=True, exist_ok=True)
    files = {
        "ranks.csv": ranks, "slots.csv": slots, "transitions.csv": changes,
        "replay-costs.csv": costs, "domain-cases.csv": domain_replay(data, prepare),
    }
    for name, rows in files.items():
        legacy.write_csv(output / name, rows)
    data_files = VIEW_INPUTS + AUDIT_INPUTS + ("openings.jsonl", "controls.jsonl", "evidence/domain-inputs.jsonl", "capture.py", "replay.py")
    return {
        "predecessor_commit": PREVIOUS,
        "pin_input_sha256": {name: legacy.file_sha(prior / name) for name in PREVIOUS_INPUTS},
        "input_sha256": {name: legacy.file_sha(data / name) for name in data_files},
        "output_sha256": {name: legacy.file_sha(output / name) for name in files},
        "output_rows": {name: len(rows) for name, rows in files.items()},
        "baseline_ab": baseline,
        "boundary_assertions": smoke,
        "request_count": len({request for request, _ in views}),
        "query_count": len(costs),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prior", required=True, type=Path)
    parser.add_argument("--data", type=Path, default=HERE)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    receipt = replay(args.data, args.prior, args.out)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
