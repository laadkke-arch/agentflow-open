"""Replay three display policies on fixed investigation candidates."""
import argparse
import copy
import csv
import json
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path

from capture import (
    FEATURE_FIELDS, QUERY_FIELDS, capture, digest, encode, jsonl, padding,
    predecessor_blob, predecessor_module, ranking_rows, scoped_view, write_jsonl,
)


ROOT = Path(__file__).resolve().parent
POLICIES = ("A", "B", "C")
CLASSES = ("direct", "partial", "conflict", "unknown")
SCENARIOS = ("base", "fixed_role", "fixed_alias", "upstream_role", "upstream_alias")
OUTPUTS = ("slots.csv", "table1.csv", "table3.csv", "perturbations.csv", "policy-scans.csv")


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def measure(payload):
    text = encode(payload)
    return len(text), len(text.encode("utf-8"))


def partition_view(rows):
    fields = {
        "feature": set(FEATURE_FIELDS),
        "request": set(QUERY_FIELDS),
        "order": {"query_id", "language", "candidates"},
    }
    for row in rows:
        if row.keys() != fields[row["kind"]] | {"kind"}:
            raise ValueError(f"unexpected field in {row['kind']} policy input")
    for row in rows:
        if row["kind"] in {"feature", "request"}:
            for role in row["roles"]:
                if role.keys() != {"source_id", "url", "location", "role", "concept"}:
                    raise ValueError("unexpected role field")
    cards = {r["feature_id"]: r for r in rows if r["kind"] == "feature"}
    requests = {r["query_id"]: r for r in rows if r["kind"] == "request"}
    orders = [r for r in rows if r["kind"] == "order"]
    for order in orders:
        ids = order["candidates"]
        if len(ids) > 12 or len(ids) != len(set(ids)) or not set(ids) <= cards.keys():
            raise ValueError("invalid investigation set")
    return cards, requests, orders


def classify(card, requirements, clauses):
    active = {}
    missing_roles = []
    for clause in clauses:
        if clause["span"] not in card[clause["field"]]:
            raise ValueError(f"claim span absent on {card['feature_id']}")
        if clause["evidence"] not in card["evidence_en"]:
            raise ValueError(f"claim source absent on {card['feature_id']}")
        role = clause["role"]
        if role and not any([r["concept"], r["role"]] == role for r in card["roles"]):
            missing_roles.append(clause["atom"])
        else:
            active[clause["atom"]] = clause["evidence"]

    counters = [key for key in requirements["counter_atoms"] if key in active]
    operations = requirements["operation_atoms"]
    missing_acts = [key for key in operations if key not in active]
    support = [key for key in operations if key in active]
    preservation = requirements["preservation_checks"]
    missing_checks = [prompt for key, prompt in preservation.items() if key not in active]
    preservation_support = [key for key in preservation if key in active]
    if counters:
        state, refs = "conflict", counters
    elif missing_acts:
        state, refs = "unsupported", support
    else:
        state, refs = ("conditional" if missing_checks else "direct"), support + preservation_support
    return {
        "state": state, "operation_supported": support, "operation_missing": missing_acts,
        "checks": missing_checks, "missing_roles": missing_roles,
        "counters": counters, "references": [active[key] for key in dict.fromkeys(refs)],
    }


def select(view_path, clause_path, output):
    """The selection process receives two files and operates on the allowlist."""
    clausebook = read_json(clause_path)
    if clausebook["policy_view_sha256"] != digest(view_path.read_bytes()):
        raise ValueError("selection view digest changed")
    cards, requests, orders = partition_view(jsonl(view_path))
    clauses_by_card = {fid: [] for fid in cards}
    for clause in clausebook["clauses"]:
        clauses_by_card[clause["feature_id"]].append(clause)
    result = []
    for order in orders:
        qid, language = order["query_id"], order["language"]
        request = requests[qid]
        requirements = clausebook["definitions"].get(qid)
        for policy in POLICIES:
            selected, decisions = [], []
            cost = Counter(chars=0, bytes=0, clause_rows=0, candidates_scanned=0, source_fetches=0)
            if request[language] and policy in {"B", "C"} and order["candidates"]:
                chars, size = measure({
                    **{field: request[field] for field in
                       (language, "operation", "preserve", "roles", "source_location")},
                    "requirements": requirements,
                })
                cost.update(chars=chars, bytes=size)
            for fid in order["candidates"]:
                if len(selected) == 3:
                    break
                card = cards[fid]
                if policy == "A":
                    selected.append({"id": fid, "label": "unqualified", "proof": None})
                    continue
                clauses = clauses_by_card[fid]
                chars, size = measure({"card": card, "clauses": clauses})
                cost.update(chars=chars, bytes=size, clause_rows=len(clauses), candidates_scanned=1)
                decision = classify(card, requirements, clauses)
                decisions.append({"id": fid, **decision})
                if decision["state"] == "conflict":
                    continue
                if policy == "B":
                    selected.append({"id": fid, "label": "unqualified", "proof": decision})
                elif decision["state"] in {"direct", "conditional"}:
                    selected.append({"id": fid, "label": decision["state"], "proof": decision})
            result.append({
                "query_id": qid, "language": language, "policy": policy,
                "selected": padding(selected, 3), "decisions": decisions, "cost": dict(cost),
            })
    write_jsonl(output, result)


def perturbed(cards, scenario):
    cards = copy.deepcopy(cards)
    box, = [card for card in cards if card["feature_id"] == "B-M03"]
    if scenario.endswith("role"):
        original = len(box["roles"])
        box["roles"] = [r for r in box["roles"] if (r["concept"], r["role"]) != ("mask", "output")]
        if original - len(box["roles"]) != 1:
            raise ValueError("role perturbation must remove one row")
    elif scenario.endswith("alias"):
        original = len(box["alias_publisher"])
        box["alias_publisher"] = [
            r for r in box["alias_publisher"] if (r["en"], r["ko"]) != ("Box Mask", "박스 마스크")
        ]
        if original - len(box["alias_publisher"]) != 1:
            raise ValueError("alias perturbation must remove one row")
    return cards


def make_variant(study, repo, run, scenario, card_rows, request_rows, base_ranks, clausebook):
    home = run / scenario
    home.mkdir()
    cards = perturbed(card_rows, scenario)
    ranks = base_ranks
    if scenario.startswith("upstream"):
        source = predecessor_module(predecessor_blob(repo, "tools/replay.py"))
        ranks, _ = ranking_rows(source, cards, request_rows, home / "rank.sqlite")
    view = scoped_view(cards, request_rows, ranks)
    view_path = home / "policy-view.jsonl"
    write_jsonl(view_path, view)
    view_sha = digest(view_path.read_bytes())
    clause_path = home / "policy-clauses.json"
    write_json(clause_path, {**clausebook, "policy_view_sha256": view_sha})
    subprocess.run(
        [sys.executable, "-B", str(study / "replay.py"), "select",
         "--view", view_path.name, "--clauses", clause_path.name, "--output", "selection.jsonl"],
        cwd=home, check=True,
    )
    selection_path = home / "selection.jsonl"
    return ranks, jsonl(selection_path), {
        "policy_view_sha256": view_sha, "selection_sha256": digest(selection_path.read_bytes()),
        "retrieval_sha256": digest(encode(ranks)), "clause_payload_sha256": digest(clause_path.read_bytes()),
    }


def reference_table(study):
    rows = read_csv(study / "judgments.csv")
    mapping = {(r["query_id"], r["feature_id"]): r for r in rows}
    if len(mapping) != len(rows) or any(r["strict_class"] not in CLASSES for r in rows):
        raise ValueError("invalid references")
    return mapping


def ids_for(selected):
    return [r["id"] if r else None for r in selected]


def labeled_results(selected, rank, labels, requests, cards):
    """Join the sealed benchmark after all policy outputs exist."""
    base = {
        (r["query_id"], r["language"]): r["selected"] for r in selected if r["policy"] == "A"
    }
    rows = []
    for policy_result in selected:
        qid, lang = policy_result["query_id"], policy_result["language"]
        policy = policy_result["policy"]
        order = rank[qid, lang]
        source_ranks = {r["feature_id"]: r for r in order["candidates"]}
        a_ids = ids_for(base[qid, lang])
        actual_ids = ids_for(policy_result["selected"])
        removed = [fid for fid in a_ids if fid and fid not in actual_ids]
        introduced = [fid for fid in actual_ids if fid and fid not in a_ids]
        fills = dict(zip(introduced, removed))
        if not set(i for i in actual_ids if i) <= source_ranks.keys():
            raise ValueError("displayed candidate outside investigation")
        if policy == "A" and a_ids != order["top3"]:
            raise ValueError("A did not reproduce the prescribed top three")
        request = requests[qid]
        state_counts = Counter(row["state"] for row in policy_result["decisions"])
        for slot, (item, old) in enumerate(zip(policy_result["selected"], a_ids, strict=True), 1):
            fid = item["id"] if item else None
            pos = source_ranks[fid] if fid else {}
            card = cards[fid] if fid else {}
            ref = labels.get((qid, fid), {})
            old_ref = labels.get((qid, old), {})
            removed_id = fills.get(fid)
            removed_ref = labels.get((qid, removed_id), {})
            proof = item["proof"] if item else None
            why = "A 순서대로 표시"
            if item and policy == "B":
                why = "카드에서 명시 충돌이 확인되지 않아 표시"
            elif item and policy == "C":
                why = "조작·대상과 보존 확인" if item["label"] == "direct" else "조작·대상 확인, 보존 확인 항목 있음"
            elif not item:
                if not request[lang]:
                    why = "요구 미모집"
                elif not source_ranks:
                    why = "조사 후보 없음"
                elif policy == "A":
                    why = "조사 후보가 3개 미만"
                elif policy == "B":
                    why = "비충돌 후보가 3개 미만"
                else:
                    why = "조작·대상 근거 후보가 3개 미만"
            rows.append({
                "query_id": qid, "layer": request["layer"], "language": lang, "policy": policy,
                "slot": slot, "investigation_id": order["investigation_sha256"],
                "retrieval_rank": pos.get("retrieval_rank"), "scan_rank": pos.get("sweep_rank"),
                "lexical_score": pos.get("score"), "feature_id": fid, "title": card.get("title"),
                "evidence_url": (proof["references"][0]["url"] if proof and proof["references"]
                                 else card.get("source_url")),
                "evidence_location": (proof["references"][0]["lines"] if proof and proof["references"]
                                      else (card["evidence_en"][0]["lines"] if item else "")),
                "policy_evidence": proof["state"] if proof else ("unexamined" if item else "vacant"),
                "display": item["label"] if item else "vacant", "display_reason": why,
                "unverified_condition": " | ".join(proof["checks"]) if item and item["label"] == "conditional" else "",
                "filtered_conflicts": state_counts["conflict"], "seen_unsupported": state_counts["unsupported"],
                "reference_class": ref.get("strict_class", "vacant"),
                "predecessor_class": ref.get("af114_verdict"),
                "reference_basis": ref.get("reference_basis"),
                "reference_sources": ref.get("reference_sources"),
                "reference_url": ref.get("reference_url"), "reference_location": ref.get("reference_location"),
                "a_at_slot": old, "a_replaced": (old or "") if old != fid else "",
                "a_lost_entirely": (old or "") if old not in actual_ids else "",
                "a_slot_reference_class": old_ref.get("strict_class", "vacant"),
                "a_slot_predecessor_class": old_ref.get("af114_verdict", ""),
                "new_visible_vs_A": fid in introduced,
                "fills_removed_a": removed_id,
                "removed_a_reference_class": removed_ref.get("strict_class"),
                "removed_a_predecessor_class": removed_ref.get("af114_verdict"),
            })
    return rows


def request_table(ranks, requests, labels):
    result = []
    for rank in ranks:
        qid, language = rank["query_id"], rank["language"]
        request = requests[qid]
        candidates = rank["candidates"]
        assessed = [ref for (q, _), ref in labels.items() if q == qid]
        counts = Counter(ref["strict_class"] for ref in assessed)
        direct = [ref["feature_id"] for ref in assessed if ref["strict_class"] == "direct"]
        pool = {r["feature_id"] for r in candidates}
        by_score = {}
        for candidate in candidates:
            by_score.setdefault(candidate["score"], []).append(candidate["feature_id"])
        result.append({
            "query_id": qid, "layer": request["layer"], "language": language,
            "source_url": request["url"], "source_location": request["source_location"],
            "operation_target": request["operation"], "preserve": request["preserve"],
            "catalog_direct": counts["direct"] if assessed else None,
            "catalog_partial": counts["partial"] if assessed else None,
            "catalog_conflict": counts["conflict"] if assessed else None,
            "catalog_unknown": counts["unknown"] if assessed else None,
            "investigation_id": rank["investigation_sha256"],
            "investigation_size": len(candidates), "investigation_vacancies": 12 - len(candidates),
            "retrieval_sql": rank["sql_statements"],
            "ties_retained": encode({score: group for score, group in by_score.items() if len(group) > 1}),
            "direct_outside_investigation": " ".join(i for i in direct if i not in pool),
            "direct_in_investigation": " ".join(i for i in direct if i in pool),
            "ordinal_source": "AF-RES-114 11/held-out same search" if assessed else "요구 미모집",
            "raw_top12": encode(rank["raw_top12"]), "a_top3": encode(rank["top3"]),
        })
    return result


def req_pair(values, key):
    pairs = [(r["query_id"], r["feature_id"]) for r in values if key(r)]
    return {"requests": len({q for q, _ in pairs}), "pairs": len(set(pairs))}


def coverage_summary(slots, table1, selected):
    group_rows = []
    baseline_summary = [r for r in slots if r["policy"] == "A"]
    selected_by = {(s["query_id"], s["language"], s["policy"]): s for s in selected}
    detail = {}
    for layer in sorted({r["layer"] for r in table1}):
        for lang in ("en", "ko"):
            observations = [r for r in table1 if r["layer"] == layer and r["language"] == lang]
            query_ids = {r["query_id"] for r in observations}
            active = [r for r in observations if r["catalog_direct"] is not None]
            counts = {
                "requests": len(active), "reserved": len(observations) - len(active),
                "eligible_requests": sum(r["catalog_direct"] > 0 for r in active),
                "eligible_pairs": sum(r["catalog_direct"] for r in active),
                "pool_eligible_requests": sum(bool(r["direct_in_investigation"]) for r in active),
                "pool_eligible_pairs": sum(len(r["direct_in_investigation"].split()) for r in active),
                "no_investigation_requests": sum(r["investigation_size"] == 0 for r in active),
            }
            for policy in POLICIES:
                group = [r for r in slots if r["query_id"] in query_ids and r["language"] == lang and r["policy"] == policy]
                baseline = [r for r in baseline_summary if r["query_id"] in query_ids and r["language"] == lang]
                base_direct = {(r["query_id"], r["feature_id"]) for r in baseline if r["reference_class"] == "direct"}
                group_direct = {(r["query_id"], r["feature_id"]) for r in group if r["reference_class"] == "direct"}
                lost = base_direct - group_direct
                gained = group_direct - base_direct
                previous_partial = {(r["query_id"], r["feature_id"]) for r in baseline if r["reference_class"] == "partial"}
                remaining_partial = {(r["query_id"], r["feature_id"]) for r in group if r["reference_class"] == "partial"}
                lost_partial = previous_partial - remaining_partial
                visible = [r for r in group if r["feature_id"]]
                status = Counter(r["display"] for r in group)
                sources = [r for r in group if r["reference_class"] != "vacant"]
                partitioned = {
                    key: req_pair(sources, lambda row, k=key: row["reference_class"] == k)
                    for key in CLASSES
                }
                gate_empty = {r["query_id"] for r in active if r["investigation_size"] > 0} - {r["query_id"] for r in visible}
                all_empty = {r["query_id"] for r in active} - {r["query_id"] for r in visible}
                cost = Counter(chars=0, bytes=0, clause_rows=0, candidates_scanned=0, source_fetches=0)
                for q in query_ids:
                    cost.update(selected_by[q, lang, policy]["cost"])
                lookup = sum(r["retrieval_sql"] for r in active)
                denominator = counts["eligible_pairs"]
                row = {
                    "layer": layer, "language": lang, "policy": policy, **counts,
                    "direct_requests": partitioned["direct"]["requests"], "direct_pairs": len(group_direct),
                    "direct_lost_requests_vs_A": len({q for q, _ in lost}), "direct_lost_pairs_vs_A": len(lost),
                    "direct_gained_requests_vs_A": len({q for q, _ in gained}), "direct_gained_pairs_vs_A": len(gained),
                    "partial_lost_requests_vs_A": len({q for q, _ in lost_partial}), "partial_lost_pairs_vs_A": len(lost_partial),
                    "direct_missing_from_pool_display": counts["pool_eligible_pairs"] - len(group_direct),
                    "direct_recall": len(group_direct) / denominator if denominator else None,
                    "conflict_requests": partitioned["conflict"]["requests"], "conflict_pairs": partitioned["conflict"]["pairs"],
                    "partial_requests": partitioned["partial"]["requests"], "partial_pairs": partitioned["partial"]["pairs"],
                    "unknown_requests": partitioned["unknown"]["requests"], "unknown_pairs": partitioned["unknown"]["pairs"],
                    "displayed": len(visible), "unqualified": status["unqualified"], "direct_label": status["direct"],
                    "conditional": status["conditional"], "vacancies": status["vacant"],
                    "all_withheld_requests": len(all_empty), "gate_emptied_requests": len(gate_empty),
                    "scan_lookups": cost["candidates_scanned"], "read_chars": cost["chars"],
                    "read_utf8_bytes": cost["bytes"], "clauses_read": cost["clause_rows"],
                    "online_lookups": cost["source_fetches"], "shared_retrieval_queries": len(active), "shared_retrieval_sql": lookup,
                }
                group_rows.append(row)

                reading = {}
                for width in (1, 3):
                    for interpretation in ("treat_all_as_recommended", "distinguish_conditional"):
                        offers = [r for r in visible if r["slot"] <= width]
                        recs = [r for r in offers if interpretation == "treat_all_as_recommended" or r["display"] != "conditional"]
                        conditions = [r for r in offers if r["display"] == "conditional"]
                        reading[f"{width}/{interpretation}"] = {
                            "recommendations": len(recs),
                            "confirmed": {k: req_pair(recs, lambda r, key=k: r["reference_class"] == key) for k in CLASSES},
                            "conditional_offers": {k: req_pair(conditions, lambda r, key=k: r["reference_class"] == key) for k in CLASSES},
                            "no_recommendation_requests": counts["requests"] - len({r["query_id"] for r in recs}),
                        }
                prior_bad = [r for r in group if r["predecessor_class"] == "conflict"]
                swaps = [r for r in group if r["fills_removed_a"]]
                detail[f"{layer}/{lang}/{policy}"] = {
                    "observations": row, "readers": reading,
                    "prior_conflict_label": req_pair(prior_bad, lambda r: True),
                    "explicit_conflict_to_unknown": req_pair(swaps, lambda r: r["removed_a_reference_class"] == "conflict" and r["reference_class"] == "unknown"),
                    "prior_conflict_to_prior_conflict": req_pair(swaps, lambda r: r["removed_a_predecessor_class"] == "conflict" and r["predecessor_class"] == "conflict"),
                    "lost_direct_ids": sorted(lost), "gained_direct_ids": sorted(gained),
                    "lost_partial_ids": sorted(lost_partial),
                    "requests_without_catalog_direct": counts["requests"] - counts["eligible_requests"],
                    "requests_without_catalog_direct_but_visible": len(
                        {r["query_id"] for r in active if r["catalog_direct"] == 0}
                        & {r["query_id"] for r in visible}
                    ),
                    "unqualified_false_certainty": {
                        k: req_pair(visible, lambda r, key=k: r["display"] in {"unqualified", "direct"} and r["reference_class"] == key)
                        for k in ("partial", "conflict", "unknown")
                    },
                }
    return group_rows, detail


def scan_table(rows):
    return [
        {"query_id": entry["query_id"], "language": entry["language"], "policy": entry["policy"],
         "feature_id": item["id"], "classification": item["state"],
         "operation_supported": encode(item["operation_supported"]),
         "operation_missing": encode(item["operation_missing"]),
         "preservation_to_check": encode(item["checks"]), "role_missing": encode(item["missing_roles"]),
         "counter_atoms": encode(item["counters"]), "references": encode(item["references"])}
        for entry in rows for item in entry["decisions"]
    ]


def compare_scenarios(scenarios):
    base_ranks, base_selected, _ = scenarios["base"]
    old = {(r["query_id"], r["language"]): r for r in base_ranks}
    old_selected = {(s["query_id"], s["language"], s["policy"]): s for s in base_selected}
    result = []
    for variant in SCENARIOS[1:]:
        ranks, selected, _ = scenarios[variant]
        choices = {(s["query_id"], s["language"], s["policy"]): s for s in selected}
        for rank in ranks:
            qid, language = pair = rank["query_id"], rank["language"]
            before = old[pair]
            original_ids = [r["feature_id"] for r in before["candidates"]]
            variant_ids = [r["feature_id"] for r in rank["candidates"]]
            row = {
                "variant": variant, "query_id": qid, "language": language,
                "pool_added": " ".join(c for c in variant_ids if c not in original_ids),
                "pool_removed": " ".join(c for c in original_ids if c not in variant_ids),
                "raw_order_changed": rank["raw_top12"] != before["raw_top12"],
                "sweep_order_changed": original_ids != variant_ids,
                "raw_top12_before": encode(before["raw_top12"]), "raw_top12_after": encode(rank["raw_top12"]),
                "sweep_before": encode(original_ids), "sweep_after": encode(variant_ids),
                "slots_before_and_after": encode({
                    policy: {
                        "before": [{"id": x["id"],"label": x["label"]} if x else None for x in old_selected[qid, language, policy]["selected"]],
                        "after": [{"id": x["id"],"label": x["label"]} if x else None for x in choices[qid, language, policy]["selected"]],
                    }
                    for policy in POLICIES
                }),
            }
            for policy in POLICIES:
                first = old_selected[qid, language, policy]
                second = choices[qid, language, policy]
                row[policy + "_ids_changed"] = ids_for(first["selected"]) != ids_for(second["selected"])
                row[policy + "_decision_changed"] = first["selected"] != second["selected"]
                row[policy + "_scan_bytes_before"] = first["cost"]["bytes"]
                row[policy + "_scan_bytes_after"] = second["cost"]["bytes"]
            result.append(row)
    return result


def run_once(study, repo, run):
    heldout = jsonl(study / "evidence/heldout-requests.jsonl")
    receipt = capture(repo, heldout, run / "reconciled")
    for file in ("inputs.jsonl", "policy-view.jsonl"):
        if (run / "reconciled" / file).read_bytes() != (study / file).read_bytes():
            raise ValueError(f"published {file} differs from fresh capture")
    records = jsonl(study / "inputs.jsonl")
    cards = [r for r in records if r["kind"] == "feature"]
    requests = [r for r in records if r["kind"] == "request"]
    ranks = [r for r in records if r["kind"] == "rank"]
    book = read_json(study / "policy-clauses.json")
    if book["policy_view_sha256"] != receipt["policy_view_sha256"]:
        raise ValueError("claim annotations are not pinned to the policy view")

    scenarios = {name: make_variant(study, repo, run, name, cards, requests, ranks, book)
                 for name in SCENARIOS}
    if scenarios["base"][2]["policy_view_sha256"] != receipt["policy_view_sha256"]:
        raise ValueError("baseline selection used a changed view")
    if scenarios["fixed_alias"][2]["policy_view_sha256"] != receipt["policy_view_sha256"]:
        raise ValueError("alias leaked into the fixed-pool policy input")
    for fixed in ("fixed_role", "fixed_alias"):
        if scenarios[fixed][0] != ranks:
            raise ValueError(f"{fixed} changed investigation order")
    if any(a["raw_top12"] != b["raw_top12"]
           for a, b in zip(ranks, scenarios["upstream_role"][0], strict=True)):
        raise ValueError("role-only perturbation changed raw retrieval")

    # No benchmark file is loaded before the subprocess outputs for all variants.
    labels = reference_table(study)
    card_map = {r["feature_id"]: r for r in cards}
    request_map = {r["query_id"]: r for r in requests}
    expected_labels = {(q, c) for q, item in request_map.items() if item["en"] for c in card_map}
    if labels.keys() != expected_labels:
        raise ValueError("the reference does not cover the active catalog pairs")
    summary_by_scenario = {}
    for name, (rank_rows, selected, provenance) in scenarios.items():
        rank_map = {(r["query_id"], r["language"]): r for r in rank_rows}
        slots = labeled_results(selected, rank_map, labels, request_map, card_map)
        requests_table = request_table(rank_rows, request_map, labels)
        summary_table, metrics = coverage_summary(slots, requests_table, selected)
        if name == "base":
            summary_by_scenario[name] = {"fingerprints": provenance, "groups": metrics}
            write_csv(run / "slots.csv", slots)
            write_csv(run / "table1.csv", requests_table)
            write_csv(run / "table3.csv", summary_table)
            write_csv(run / "policy-scans.csv", scan_table(selected))
        else:
            baseline_groups = summary_by_scenario["base"]["groups"]
            differences = {}
            for group, detail in metrics.items():
                before = baseline_groups[group]["observations"]
                after = detail["observations"]
                changes = {key: {"before": before[key], "after": value}
                           for key, value in after.items() if before[key] != value}
                if changes:
                    differences[group] = changes
            summary_by_scenario[name] = {"fingerprints": provenance, "observation_changes": differences}
    perturbations = compare_scenarios(scenarios)
    write_csv(run / "perturbations.csv", perturbations)
    return {
        "inputs_sha256": receipt["input_sha256"],
        "judgments_sha256": digest((study / "judgments.csv").read_bytes()),
        "sources_sha256": digest((study / "sources.jsonl").read_bytes()),
        "clauses_sha256": digest((study / "policy-clauses.json").read_bytes()),
        "af114_query_languages_reconciled": receipt["archived_11_query_languages"],
        "af114_archived_runs_reconciled": len(receipt["archived_11_comparisons"]),
        "all_displays_in_investigation": True,
        "source_index_preparation": receipt["index_cost"],
        "clause_rows_prepared": len(book["clauses"]), "request_definitions_prepared": len(book["definitions"]),
        "scenarios": summary_by_scenario,
        "perturbations": {
            name: {field: sum(bool(row[field]) for row in perturbations if row["variant"] == name)
                   for field in ("pool_added", "pool_removed", "raw_order_changed", "sweep_order_changed",
                                 "A_ids_changed", "B_ids_changed", "C_ids_changed")}
            for name in SCENARIOS[1:]
        },
    }


def run(study, repo, out):
    out.mkdir(parents=True, exist_ok=False)
    attempts = []
    for name in ("run-1", "run-2"):
        work = out / name
        result = run_once(study, repo, work)
        hashes = {f: digest((work / f).read_bytes()) for f in OUTPUTS}
        attempts.append({"path_label": name, "output_sha256": hashes, "observation_sha256": digest(encode(result))})
    compact = [{k: v for k, v in item.items() if k != "path_label"} for item in attempts]
    if compact[0] != compact[1]:
        raise ValueError("new-path replays differ")

    sources = jsonl(study / "sources.jsonl")
    body_reads = [row for row in sources if row["status"] in {"body", "binary_body"}]
    candidate_urls = {u for r in sources for u in [r["original_url"], *r["official_alternatives"]] if u}
    result["source_reading"] = {
        "ledger_rows": len(sources), "candidate_urls": len(candidate_urls),
        "opened_rows_including_pointers": len(body_reads) + sum(r["status"] == "pointer_only" for r in sources),
        "direct_body_rows": len(body_reads), "counted_unique_works": sum(r["count_unique"] for r in sources),
        "direct_text_characters": sum(r["read_characters"] or 0 for r in body_reads),
        "direct_utf8_text_bytes": sum(r["read_utf8_bytes"] or 0 for r in body_reads if r["status"] == "body"),
        "direct_binary_fixture_bytes": sum(r["read_utf8_bytes"] or 0 for r in body_reads if r["status"] == "binary_body"),
        "counted_by_allocation": dict(Counter(r["allocation"] for r in sources if r["count_unique"])),
        "preceding_request_addresses": sum(r["allocation"] == "request" for r in sources),
        "preceding_direct_request_documents": sum(r["allocation"] == "request" for r in body_reads),
    }
    result["repeat"] = {"agree": True, "runs": attempts, "sqlite": sqlite3.sqlite_version,
                        "python": ".".join(map(str, sys.version_info[:3]))}
    for filename in OUTPUTS:
        (out / filename).write_bytes((out / "run-1" / filename).read_bytes())
    write_json(out / "metrics.json", result)
    print(encode({
        "agreement": True, "baseline_rows": len(read_csv(out / "slots.csv")),
        "af114_query_languages": result["af114_query_languages_reconciled"],
        "reference_pairs": len(read_csv(study / "judgments.csv")),
        "observation_sha256": attempts[0]["observation_sha256"],
        "source_reading": result["source_reading"], "perturbations": result["perturbations"],
    }))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choices = parser.add_subparsers(dest="action", required=True)
    replay = choices.add_parser("run")
    replay.add_argument("--repo", type=Path, default=Path.cwd())
    replay.add_argument("--out", type=Path, required=True)
    selection = choices.add_parser("select")
    selection.add_argument("--view", type=Path, required=True)
    selection.add_argument("--clauses", type=Path, required=True)
    selection.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.action == "select":
        select(args.view, args.clauses, args.output)
    else:
        run(ROOT, args.repo.resolve(), args.out.resolve())


if __name__ == "__main__":
    main()
