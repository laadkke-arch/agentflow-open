#!/usr/bin/env python3
"""Join adjudicated evidence without changing the frozen frame or predictions."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text())


def write_json(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    predictions = list(csv.DictReader((ROOT / "predictions.csv").open()))
    by_case = {r["case_id"]: r for r in predictions}
    common = "case_id project stratum edition version vacant body_url section_url section_locator literal_reference base_uri payload_url payload_mime payload_bytes payload_sha256 P U G legacy_path_P source_url publication_url evidence receipt limitation".split()
    rows, extras = [], []
    for group in ("ggplot2", "matplotlib"):
        for row in csv.DictReader((ROOT / f"evidence/{group}/lineage.csv").open()):
            row["stratum"] = by_case[row["case_id"]]["stratum"]
            for key in row:
                if key not in common and key not in extras:
                    extras.append(key)
            rows.append(row)
    rank = {r["case_id"]: i for i, r in enumerate(predictions)}
    rows.sort(key=lambda r: (rank[r["case_id"]], r["edition"] != "old"))
    assert len(rows) == 24
    assert len({(r["case_id"], r["edition"]) for r in rows}) == 24
    with (ROOT / "lineage.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=common + extras)
        writer.writeheader()
        writer.writerows(rows)

    sources = []
    input_ledgers = []
    for group in ("ggplot2", "matplotlib", "cross-domain"):
        path = ROOT / f"evidence/{group}/sources.jsonl"
        members = [json.loads(line) for line in path.read_text().splitlines()]
        input_ledgers.append({"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "rows": len(members), "countable": sum(r["countable"] for r in members)})
        for row in members:
            row["ledger_origin"] = str(path.relative_to(ROOT))
        sources.extend(members)

    mirror_specs = [
        ("evidence/return-url-checks.json", "example_body", "HTML"),
        ("evidence/live-payload-checks.json", "image_payload", "PNG"),
    ]
    for file, category, label in mirror_specs:
        for i, r in enumerate(read_json(file)["records"], 1):
            sources.append({
                "source_id": f"ROOT-LIVE-{label}-{i:02}",
                "questions": ["Q4", "Q7"], "cases": [r["case_id"]],
                "original_url": r["original_url"],
                "fixed_url": r.get("fixed_url", r.get("fixed_source_url")),
                "accessed_utc": r["finished_utc"],
                "publisher": "Matplotlib maintainers", "lineage": "Matplotlib selected 3.7.0 publication reader mirror",
                "category": category, "version": "3.7.0", "location": r.get("fragment", "payload bytes"),
                "sha256": r["sha256"],
                "observation": ({"http_status": r["status"], "bytes": r["bytes"], "mime": r["mime"], "whole_HTML_matches_pinned": r["matches_pinned_body_bytes"], "exact_fragment_present": r["fragment_present"], "first_reference_matches": r["first_reference_matches"], "scope_comparison": "evidence/return-url-scope-comparison.json"} if label == "HTML" else {"http_status": r["status"], "bytes": r["bytes"], "mime": r["mime"], "PNG_signature": r["png_signature"], "exact_bytes_match_pinned": r["exact_bytes_match"]}),
                "claims_supported": ["Observed availability of reader URL at this UTC; scoped references and linked payloads checked separately"],
                "claims_refuted": ["Version directory implies immutable complete HTML bytes"] if label == "HTML" else [],
                "limitations": "A current mirror observation is neither browser execution nor proof of fresh generation by the historical build.",
                "countable": False, "duplicate_reason": r["duplicate_reason"], "receipt": file,
                "ledger_origin": "root reader-link follow-up",
            })
    assert len({r["source_id"] for r in sources}) == len(sources)
    # Cross-ledger byte deduplication is conservative; same-work edition deduplication
    # was performed by each reader and remains explicitly documented per row.
    seen = {}
    reconciled = []
    for row in sources:
        if row["countable"] and row.get("sha256"):
            h = row["sha256"]
            if h in seen:
                row["countable_before_root_reconciliation"] = True
                row["countable"] = False
                row["duplicate_reason"] = f"Root cross-ledger same-byte merge with {seen[h]}"
                reconciled.append({"removed": row["source_id"], "retained": seen[h], "sha256": h})
            else:
                seen[h] = row["source_id"]
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in sources))
    categories = collections.Counter(r["category"] for r in sources if r["countable"])
    publication_categories = {"release_record", "publication_record", "deployment_listing", "distribution_record", "distribution_bundle", "change_record", "build_rule"}
    minima = {
        "example_bodies": {"required": 8, "observed": categories["example_body"]},
        "resources_or_example_sources": {"required": 8, "observed": categories["image_payload"]},
        "publication_release_change_build": {"required": 8, "observed": sum(categories[c] for c in publication_categories)},
        "epub_spec_and_new_package": {"required": 2, "observed": sum(r["countable"] for r in sources if "epub" in r["category"])},
        "wheel_specs_and_new_package": {"required": 2, "observed": sum(r["countable"] for r in sources if "wheel" in r["category"] or "packaging" in r["category"])},
    }
    write_json("evidence/source-reconciliation.json", {
        "input_ledgers": input_ledgers, "root_mirror_rows": 12, "rows": len(sources),
        "countable": sum(r["countable"] for r in sources), "categories": dict(categories),
        "cross_ledger_same_byte_merges": reconciled, "minima": minima,
        "policy": "Same work across editions, same-byte payloads, mirrors, inherited 098 work, uninspected automatic scans, failed requests and empty job queries are not new primary materials. Publication/source events remain marked with their common lineage; counts are not independent experiments.",
    })
    write_json("evidence/failure-index.json", {
        "scope": "Failed fetches and failed comparisons remain distinct from missing historical execution evidence.",
        "files": [str(x.relative_to(ROOT)) for x in sorted((ROOT / "evidence").rglob("*fail*")) if x.is_file() and "cache" not in x.parts and x.name != "failure-index.json"],
        "other_failure_receipts": ["evidence/prepublication-checks.json", "evidence/publish-path.json", "evidence/return-url-checks.json"],
        "reader_HTML_comparison": "check_returns.py returned 1: whole HTML bytes differed in all 4 pages. Subsequent exact section comparison and 8 payload SHA checks were separate successful narrower observations, not a rewrite of this result.",
    })
    print(json.dumps({"lineage_rows": len(rows), "source_rows": len(sources), "countable": sum(r["countable"] for r in sources), "minima": minima, "cross_ledger_merges": reconciled}, ensure_ascii=False))


if __name__ == "__main__":
    main()
