"""Recalculate AF-RES-106 denominators from the sealed and adjudicated ledgers.

No network, example execution, or historical-build claim. Read-only by default.
--write writes only the task's counts.json. All rates stay within project/stratum.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEALED_PREDICTIONS_SHA256 = "b963763c165faae527e3d214dcd44bb471f390778c49787c7744d696909e7d91"
SEALED_FRAME_SHA256 = "5e2010d546b64841c915bc42628d52a1c5bb534886adbeee579eda6997e5147e"
MINIMUM = {"example_body": 8, "independent_payload_source": 6,
           "official_change": 6, "iiif": 2, "jats": 2}


def read_csv(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def truth(value):
    return value is True or str(value).lower() in {"true", "yes", "1"}


def confusion(predictions, new_rows, field):
    result = []
    for project in ["ggplot2", "Matplotlib"]:
        for stratum in ["A", "M", "G"]:
            selected = [p for p in predictions if p["project"] == project and p["stratum"] == stratum]
            c = dict(project=project, stratum=stratum, axis=field, slots=len(selected),
                     TP=0, FP=0, FN=0, TN=0, prediction_abstentions=0,
                     observed_unknown=0, vacancies=0, actual_positive=0, actual_negative=0)
            for p in selected:
                if p["vacant"] == "YES":
                    c["vacancies"] += 1
                    continue
                outcome = new_rows[p["case_id"]].get(field, "미확인")
                pred = p["prediction_U"]
                if outcome == "YES":
                    c["actual_positive"] += 1
                elif outcome == "NO":
                    c["actual_negative"] += 1
                else:
                    c["observed_unknown"] += 1
                if pred not in {"YES", "NO"}:
                    c["prediction_abstentions"] += 1
                elif outcome in {"YES", "NO"}:
                    c[{("YES", "YES"): "TP", ("YES", "NO"): "FP",
                       ("NO", "YES"): "FN", ("NO", "NO"): "TN"}[(pred, outcome)]] += 1
            positive, negative = c["actual_positive"], c["actual_negative"]
            c["FPR"] = {"numerator": c["FP"], "denominator": negative,
                        "value": c["FP"] / negative if negative else "산출 불가"}
            c["FNR"] = {"numerator": c["FN"], "denominator": positive,
                        "value": c["FN"] / positive if positive else "산출 불가"}
            c["specificity"] = {"numerator": c["TN"], "denominator": negative,
                                "value": c["TN"] / negative if negative else "산출 불가"}
            result.append(c)
    return result


def calculate():
    frame, predictions, lineage, returns = [read_csv(x) for x in
                                            ["frame.csv", "predictions.csv", "lineage.csv", "returns.csv"]]
    sources = [json.loads(s) for s in (ROOT / "sources.jsonl").read_text().splitlines() if s.strip()]
    checks = []

    def require(name, condition, detail=None):
        checks.append({"check": name, "passed": bool(condition), "detail": detail})

    for name, digest in [("frame.csv", SEALED_FRAME_SHA256), ("predictions.csv", SEALED_PREDICTIONS_SHA256)]:
        require("sealed bytes " + name, hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest)
    require("12 unique pair slots", len(predictions) == 12 and len({r["case_id"] for r in predictions}) == 12)
    require("24 unique edition slots", len(lineage) == 24 and len({(r["case_id"], r["edition"]) for r in lineage}) == 24)
    require("12 unique returns", len(returns) == 12 and {r["case_id"] for r in returns} == {r["case_id"] for r in predictions})
    require("803 distinct project/page frame rows", len(frame) == 803 and len({(r["project"].lower(), r["page_path"]) for r in frame}) == 803)

    population = {}
    for project, expected in [("ggplot2", 68), ("Matplotlib", 479)]:
        project_rows = [r for r in frame if r["project"].lower() == project.lower()]
        eligible = [r for r in project_rows if r["eligible"] == "YES"]
        require(project + " eligible denominator", len(eligible) == expected)
        strata = collections.Counter(r.get("signal_stratum") or r.get("stratum") for r in eligible)
        population[project] = {"all_page_rows": len(project_rows), "eligible": len(eligible),
                               "excluded": len(project_rows) - len(eligible),
                               "strata": {s: strata[s] for s in ["A", "M", "G"]},
                               "asset_kinds": dict(collections.Counter(r["asset_kind"] for r in eligible)),
                               "exclusions": dict(collections.Counter(r["exclusion"] for r in project_rows if r["eligible"] != "YES"))}
        computed_hashes = {r["old_section_path"]: hashlib.sha256(("AF106|" + project + "|" + r["old_section_path"]).encode("utf-8")).hexdigest() for r in eligible}
        require(project + " all path hashes", all(r["hash_sha256"] == computed_hashes[r["old_section_path"]] for r in eligible))
        require(project + " mutually exclusive strata", sum(strata.values()) == expected and not set(strata) - {"A", "M", "G"})
        for stratum in ["A", "M", "G"]:
            candidate = sorted([r for r in eligible if (r.get("signal_stratum") or r.get("stratum")) == stratum],
                               key=lambda r: (computed_hashes[r["old_section_path"]], r["old_section_path"]))[:2]
            selected = [r for r in predictions if r["project"] == project and r["stratum"] == stratum]
            actual = sorted(r["old_section_path"] for r in selected if r["vacant"] == "NO")
            require(project + " " + stratum + " selection/vacancy", len(selected) == 2 and actual == sorted(r["old_section_path"] for r in candidate)
                    and sum(r["vacant"] == "YES" for r in selected) == 2 - len(candidate))
    new_rows = {r["case_id"]: r for r in lineage if r["edition"] == "new"}
    for p in predictions:
        editions = [r for r in lineage if r["case_id"] == p["case_id"]]
        require(p["case_id"] + " editions/vacancy", {r["edition"] for r in editions} == {"old", "new"}
                and all(r["vacant"] == p["vacant"] for r in editions))
    actual_rows = [r for r in lineage if r["vacant"] == "NO"]
    require("16 observed edition slots", len(actual_rows) == 16)
    require("G remains unverified", all(r["G"] == "미확인" for r in actual_rows))
    require("four valid return decisions", all(r["decision"] in {"옛판 고정 인용", "새 절로 교체", "두 판 병기", "유보"} for r in returns))

    counted = [s for s in sources if truth(s.get("countable"))]
    count_by_category = collections.Counter(s["count_category"] for s in counted)
    require("unique counted work lineages", len({s["work_lineage"] for s in counted}) == len(counted))
    require("unique source IDs", len({s["id"] for s in sources}) == len(sources))
    require("all counted sources directly read and new", all(truth(s.get("direct_read")) and s["status"] == "신규" for s in counted))
    require("all source URLs and times", all(s.get("original_url") and s.get("accessed_utc") for s in sources))
    minimum = {k: {"required": n, "observed": count_by_category[k], "shortfall": max(0, n - count_by_category[k])} for k, n in MINIMUM.items()}
    require("source category minimum", all(x["shortfall"] == 0 for x in minimum.values()), minimum)
    require("at least24 distinct primary works", len(counted) >= 24)
    required = {"id", "questions", "cases", "original_url", "immutable_url", "preserved_location", "accessed_utc", "publisher", "work_lineage", "edition", "location", "fingerprints", "observed", "supports", "refutes", "limits", "status", "category", "countable", "count_reason"}
    require("source schema", all(required <= set(s) for s in sources))
    for filename in ["RESULT.md", "SELF_CHECK.md", "reproduce.md", "SCOPE.md", "manifest.json", "INDEX_PROPOSAL.md"]:
        require("required file " + filename, (ROOT / filename).exists())
    for filename in ["RESULT.md", "SELF_CHECK.md"]:
        if (ROOT / filename).exists():
            content = (ROOT / filename).read_text()
            require(filename + " explicitly preserves unknown", "미확인" in content)

    supplemental = json.loads((ROOT / "evidence/supplemental-summary.json").read_text())
    result = {"schema": 1, "prediction_seal": "8054c2221d4023ba03c904d96f13928219d36c3d",
              "frame": population, "pair_slots": 12, "filled_pairs": 8, "vacant_pairs": 4,
              "edition_slots": 24, "observed_editions": len(actual_rows), "vacant_editions": 24 - len(actual_rows),
              "main_original_purpose": confusion(predictions, new_rows, "U_original_purpose"),
              "main_visual_role": confusion(predictions, new_rows, "U_visual_role"),
              "main_specific_method": confusion(predictions, new_rows, "method_specific"),
              "sources": {"ledger_rows": len(sources), "unique_primary_works": len(counted),
                          "count_by_category": dict(count_by_category), "minimum": minimum,
                          "excluded_rows": len(sources) - len(counted),
                          "counted_ids": [s["id"] for s in counted]},
              "supplemental": supplemental,
              "scope_note": "No aggregate performance rate across projects/strata or auxiliary samples. Negative-zero groups have FPR/specificity 산출 불가. G/GUI/runtime are not inferred from source/tree/hash.",
              "checks": checks, "passed": all(c["passed"] for c in checks)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = calculate()
    if args.write:
        (ROOT / "counts.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    else:
        saved = json.loads((ROOT / "counts.json").read_text())
        result["saved_counts_match"] = result == saved
        result["passed"] = result["passed"] and result["saved_counts_match"]
    print(json.dumps({"passed": result["passed"], "checks": len(result["checks"]),
                      "failed": [c for c in result["checks"] if not c["passed"]],
                      "saved_counts_match": result.get("saved_counts_match"),
                      "pairs": result["filled_pairs"], "vacancies": result["vacant_pairs"],
                      "sources": result["sources"]}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
