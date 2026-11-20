"""Recompute descriptive counts from preserved runs and explicit judgments.

No search, candidate generation, automatic relevance judgment, or new scoring rule.
All output stays in this workstream. Run from any directory with Python 3.
"""
from collections import Counter, defaultdict
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ROLES = ["같은 목적 완성품", "재사용 부품", "같은 분야의 다른 설계", "다른 언어·생태계", "다른 분야 원리", "표준·논문"]
LABELS = {"DIRECT_DOCUMENTED", "CONDITIONAL_TRANSFER", "SURFACE_OR_CONSTRAINT_MISMATCH", "INSUFFICIENT"}


def read(name):
    return json.loads((ROOT / name).read_text())


def excluded(row):
    value = row.get("exclusion", False)
    return value.get("excluded", False) if isinstance(value, dict) else bool(value)


def gold_ids(row):
    return {x["gold_id"] for x in row["gold_matches"]}


def percent(n, d):
    return f"{n}/{d} ({100*n/d:.1f}%)" if d else "0/0 (해당 정답 없음)"


def main():
    cases = read("cases/CASES.json")["cases"]
    data = read("JUDGMENTS.json")
    judgments = data["judgments"]
    cdict = {c["id"]: c for c in cases}
    gold = {(c["id"], g["id"]): g for c in cases for g in c["gold_items"]}
    runs = {(c["id"], b): read(f"runs/{b}/{c['id']}.json") for c in cases for b in "AB"}
    by_run = defaultdict(list)
    expected = {(cid, b, i + 1) for (cid, b), r in runs.items() for i in range(len(r["candidates"]))}
    keys = [(j["case_id"], j["baseline"], j["rank"]) for j in judgments]
    assert len(keys) == len(set(keys)), "Duplicate judgment"
    assert set(keys) == expected, "Missing/extra candidate judgment"
    for j in judgments:
        cid, b = j["case_id"], j["baseline"]
        original = runs[cid, b]["candidates"][j["rank"] - 1]
        assert j["candidate_url"] == original["url"], (cid, b, j["rank"], "changed candidate URL")
        assert j["label"] in LABELS
        assert j["L"] in {"ok", "broken", "missing"}
        assert j["E"] in {"supported", "contradicted", "unknown"}
        assert j["T"] in {"not_needed", "mapped", "analogy_only", "unknown"}
        assert j["runtime_observation"] == "not_performed"
        assert {x["constraint_id"] for x in j["H"]} == {x["id"] for x in cdict[cid]["mandatory_constraints"]}
        assert all(x["value"] in {"pass", "fail", "unknown", "not_in_scope"} for x in j["H"])
        assert all((cid, gid) in gold for gid in gold_ids(j))
        assert not (j["nongold_useful"] and gold_ids(j)), "Gold hit counted as nongold"
        if j["nongold_useful"]:
            assert j["L"] == "ok" and j["E"] == "supported"
            assert j["label"] in {"DIRECT_DOCUMENTED", "CONDITIONAL_TRANSFER"}
            assert all(h["value"] not in {"fail", "unknown"} for h in j["H"])
            assert not excluded(j)
        if j["nongold_historical_useful"]:
            assert j["nongold_useful"] and j["date_status"] == "pre_decision"
        for field, status in [("strict_historical_gold_ids", "pre_decision"), ("post_decision_gold_ids", "post_decision"), ("date_unknown_gold_ids", "unknown")]:
            assert set(j[field]).issubset(gold_ids(j))
            if j[field]:
                assert j["date_status"] == status and not excluded(j), (cid, b, j["rank"], field)
        by_run[cid, b].append(j)

    def summarize(rows, ids):
        available_gold = {(cid, g["id"]) for cid in ids for g in cdict[cid]["gold_items"]}
        result = {"cases": len(ids), "candidates": len(rows), "gold_denominator": len(available_gold)}
        for field, key in [("gold_matches", "all_matches"), ("strict_historical_gold_ids", "strict_historical"), ("post_decision_gold_ids", "post_decision"), ("date_unknown_gold_ids", "date_unknown")]:
            pairs = {(r["case_id"], gid) for r in rows if not excluded(r) for gid in (gold_ids(r) if field == "gold_matches" else r[field])}
            result[key + "_gold_pairs"] = [list(x) for x in sorted(pairs)]
            result[key + "_hits"] = len(pairs)
            result[key + "_recall"] = len(pairs) / len(available_gold) if available_gold else None
        result["labels"] = dict(Counter(r["label"] for r in rows))
        result["H_values"] = dict(Counter(h["value"] for r in rows for h in r["H"]))
        result["candidates_with_scoped_out_constraints"] = sum(any(h["value"] == "not_in_scope" for h in r["H"]) for r in rows)
        result["all_constraints_scoped_out"] = sum(all(h["value"] == "not_in_scope" for h in r["H"]) for r in rows)
        result["date_status_candidates"] = dict(Counter(r["date_status"] for r in rows))
        result["nongold_candidate_denominator"] = sum(not gold_ids(r) and not excluded(r) for r in rows)
        for key in ["nongold_useful", "nongold_historical_useful", "near_miss", "broken_or_fake"]:
            result[key] = sum(bool(r[key]) for r in rows)
            result[key + "_cases"] = sorted({r["case_id"] for r in rows if r[key]})
        result["insufficient_candidates"] = sum(r["label"] == "INSUFFICIENT" for r in rows)
        result["excluded_candidates"] = sum(excluded(r) for r in rows)
        result["link_status"] = dict(Counter(r["link_status"] for r in rows))
        result["all_matches_gold_types"] = dict(Counter(gold[tuple(x)]["match_kind"] for x in result["all_matches_gold_pairs"]))
        result["strict_historical_gold_types"] = dict(Counter(gold[tuple(x)]["match_kind"] for x in result["strict_historical_gold_pairs"]))
        return result

    totals = {}
    case_results = []
    for c in cases:
        cid = c["id"]
        row = {"id": cid, "canonical_id": c["canonical_id"], "family": c["family"], "url": c["url"], "decision_date": c["decision_date"], "gold_denominator": len(c["gold_items"]), "gold_roles": dict(Counter(g["role"] for g in c["gold_items"]))}
        for b in "AB":
            row[b] = summarize(by_run[cid, b], {cid})
            row[b]["recorded_exposure_entries"] = len(runs[cid, b].get("exposures", []))
            found = {g for _, g in row[b]["strict_historical_gold_pairs"]}
            row[b]["missed_strict_gold_ids"] = [g["id"] for g in c["gold_items"] if g["id"] not in found]
        row["union_strict_gold_ids"] = sorted({g for b in "AB" for _, g in row[b]["strict_historical_gold_pairs"]})
        row["union_all_match_gold_ids"] = sorted({g for b in "AB" for _, g in row[b]["all_matches_gold_pairs"]})
        case_results.append(row)
    for b in "AB":
        rows = [r for r in judgments if r["baseline"] == b]
        totals[b] = summarize(rows, set(cdict))
        clean = {cid for cid in cdict if not runs[cid, b].get("exposures")}
        totals[b]["no_recorded_exposure_subset"] = summarize([r for r in rows if r["case_id"] in clean], clean)
        totals[b]["no_recorded_exposure_subset"]["case_ids"] = sorted(clean)
        totals[b]["recorded_exposure_runs"] = len(cdict) - len(clean)

    roles = []
    for role in ROLES:
        population = {key for key, g in gold.items() if g["role"] == role}
        row = {"role": role, "gold_denominator": len(population)}
        for b in "AB":
            row[b] = {}
            for kind in ["strict_historical", "all_matches", "post_decision", "date_unknown"]:
                matched = {tuple(x) for x in totals[b][kind + "_gold_pairs"]} & population
                row[b][kind] = len(matched)
            row[b]["missed_case_ids"] = sorted({cid for cid, gid in population - {tuple(x) for x in totals[b]["strict_historical_gold_pairs"]}})
        roles.append(row)
    family_results = []
    for family in sorted({c["family"] for c in cases}):
        ids = {c["id"] for c in cases if c["family"] == family}
        gs = [g for (cid, _), g in gold.items() if cid in ids]
        row = {"family": family, "case_ids": sorted(ids), "cases": len(ids), "gold_denominator": len(gs), "role_counts": dict(Counter(g["role"] for g in gs)), "crossfield_structural_items": [g["id"] for g in gs if g["role"] == "다른 분야 원리"]}
        for b in "AB":
            row[b] = summarize([r for r in judgments if r["baseline"] == b and r["case_id"] in ids], ids)
        family_results.append(row)
    gold_types = []
    for kind in sorted({g["match_kind"] for g in gold.values()}):
        population = {key for key, g in gold.items() if g["match_kind"] == kind}
        gold_types.append({"kind": kind, "gold_denominator": len(population), **{b: {k: len({tuple(x) for x in totals[b][k + "_gold_pairs"]} & population) for k in ["strict_historical", "all_matches"]} for b in "AB"}})
    union = {tuple(x) for b in "AB" for x in totals[b]["strict_historical_gold_pairs"]}
    union_all = {tuple(x) for b in "AB" for x in totals[b]["all_matches_gold_pairs"]}
    review_rows = [{"case_id": r["case_id"], "baseline": r["baseline"], "rank": r["rank"], "review_matches": r["review_matches"], "date_status": r["date_status"]} for r in judgments if r["review_matches"]]
    result = {
        "schema_version": 1,
        "unit": "case × baseline × returned candidate; recall unit is distinct (case,gold_id)",
        "interpretation": "One preserved run per case/baseline, no significance test or global-recall claim. Temporal buckets can overlap when different candidates match one gold item. No runtime or user-effect test.",
        "input_hashes": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ["cases/CASES.json", "JUDGMENTS.json"]},
        "corpus": {"cases": len(cases), "families": dict(Counter(c["family"] for c in cases)), "gold": len(gold), "roles": dict(Counter(g["role"] for g in gold.values())), "match_kinds": dict(Counter(g["match_kind"] for g in gold.values())), "stances": dict(Counter(g["stance"] for g in gold.values())), "added_in_review": dict(Counter(str(g.get("added_in_review")) for g in gold.values())), "decision_window": [min(c["decision_date"] for c in cases), max(c["decision_date"] for c in cases)]},
        "baseline_totals": totals,
        "union_strict_hits": len(union),
        "union_all_matches": len(union_all),
        "roles": roles,
        "families": family_results,
        "gold_types": gold_types,
        "cases": case_results,
        "review_matches": review_rows,
    }
    (ROOT / "evidence/AGGREGATES.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"judgments": len(judgments), "gold": len(gold), "A_strict": totals["A"]["strict_historical_hits"], "B_strict": totals["B"]["strict_historical_hits"], "A_all": totals["A"]["all_matches_hits"], "B_all": totals["B"]["all_matches_hits"], "union_strict": len(union), "union_all": len(union_all), "roles": result["corpus"]["roles"], "gold_types": gold_types, "useful": {b: [totals[b]["nongold_useful"], totals[b]["nongold_candidate_denominator"], totals[b]["nongold_historical_useful"]] for b in "AB"}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
