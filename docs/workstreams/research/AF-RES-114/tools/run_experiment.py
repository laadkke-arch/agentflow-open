"""Produce frozen replay ledgers, SQLite receipts, and one-feature contrasts."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from replay import ROOT, digest, read_jsonl

HERE = Path(__file__).resolve().parent
PUBLISH = {
    "verified": {
        "natural": "ranks.csv",
        "exploratory": "evidence/ranks-exploratory.csv",
        "control": "evidence/ranks-controls.csv",
        "variant": "evidence/ranks-variants.csv",
    },
    "publisher_partial": {
        "exploratory": "evidence/ranks-exploratory-publisher.csv",
        "control": "evidence/ranks-controls-publisher.csv",
        "variant": "evidence/ranks-variants-publisher.csv",
    },
}


def run(tool, *args):
    subprocess.run([sys.executable, "-B", str(HERE / tool), *map(str, args)], check=True)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def copy_outputs(src, dst, mapping):
    for layer, name in mapping.items():
        shutil.copyfile(src / f"{layer}.csv", dst / name)


def preparation():
    catalog = read_jsonl(ROOT / "catalog.jsonl")
    queries = read_jsonl(ROOT / "queries.jsonl")
    sources = {s["source_id"]: s for s in read_jsonl(ROOT / "sources.jsonl")}
    base = {sources[c["source_id"]]["lineage"] for c in catalog}
    alias = {item["source_id"] for c in catalog for item in c["alias_publisher"]}
    roles = {sources[e["source_id"]]["lineage"] for c in catalog for e in c["roles"]}
    query_roles = {q["source_id"] for q in queries if q["roles"] and q["layer"] == "exploratory"}
    return {
        "base_feature_source_lineages": sorted(base),
        "base_feature_document_count": len(base),
        "additional_publisher_alias_source_ids": sorted(alias),
        "additional_publisher_alias_document_count": len(alias),
        "candidate_role_source_lineages": sorted(roles),
        "candidate_role_document_count": len(roles),
        "additional_role_document_count_over_base": len(roles - base),
        "exploratory_query_role_documents": sorted(query_roles),
        "exploratory_query_role_document_count": len(query_roles),
        "human_editing_time": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    dst = args.out.resolve()
    (dst / "evidence").mkdir(parents=True, exist_ok=False)
    builds = dst / "scratch"
    catalog = ROOT / "catalog.jsonl"
    main_receipts = {}
    contrast_receipts = {}
    for profile, mapping in PUBLISH.items():
        target = builds / profile
        run("replay.py", "--profile", profile, "--layers", *mapping, "--out", target)
        main_receipts[profile] = load_json(target / "replay.json")
        copy_outputs(target, dst, mapping)
    for case in load_json(ROOT / "evidence/scenarios.json"):
        changed_catalog = builds / (case["name"] + ".jsonl")
        selector = ["--drop-alias", case["drop_alias"]] if "drop_alias" in case else ["--omit-role", *case["omit_role"]]
        run("perturb.py", "--input", catalog, "--output", changed_catalog, "--feature", case["feature"], *selector)
        target = builds / case["name"]
        run("replay.py", "--profile", case["profile"], "--catalog", changed_catalog, "--layers", "control", "--out", target)
        name = f"evidence/ranks-{case['name']}.csv"
        copy_outputs(target, dst, {"control": name})
        contrast_receipts[case["name"]] = {
            "changed_from_base": changed_catalog.read_bytes() != catalog.read_bytes(),
            "intervention": case,
            "receipt": load_json(target / "replay.json"),
        }
    fingerprints = {}
    for file in sorted(dst.rglob("*.csv")):
        if "scratch" not in file.relative_to(dst).parts:
            fingerprints[str(file.relative_to(dst))] = digest(file.read_bytes())
    cost = {
        "preparation": preparation(),
        "profiles": main_receipts,
        "contrasts": contrast_receipts,
        "rank_file_sha256": fingerprints,
        "accounting": "Build 1 and 2 are distinct files. A search is one SQL statement for nonempty tokens. R1 reads role evidence using a second SQL statement if the pool is nonempty. A vacant query executes neither.",
    }
    (dst / "costs.json").write_text(json.dumps(cost, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
