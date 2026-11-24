"""Integrate independently reviewed evidence without editing sealed forecasts."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
SEAL = "8054c2221d4023ba03c904d96f13928219d36c3d"
REL = "docs/workstreams/research/AF-RES-106/"


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def array(value):
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def first(row, *names, default="미확인"):
    for name in names:
        value = row.get(name)
        if value is not None and value != "":
            return value
    return default


def csv_write(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (ROOT / name).open("w", encoding="utf-8", newline="") as stream:
        out = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({k: json.dumps(v, ensure_ascii=False, separators=(",", ":")) if isinstance(v, (dict, list)) else v for k, v in r.items()})


def normalize_source(row, origin, canonical):
    sid = str(first(row, "id", "source_id"))
    counted = sid in canonical
    work = first(row, "work_lineage", "lineage")
    chosen = canonical.get(sid, {})
    category = first(row, "category")
    cc = chosen.get("category", "excluded")
    if cc in {"body", "example_body"}:
        cc = "example_body"
    elif cc in {"figure_or_source", "independent_source_or_payload"}:
        cc = "independent_payload_source"
    elif cc in {"official_record", "publication_record", "official_change_record"}:
        cc = "official_change"
    elif counted and (sid.startswith("CD106-I") or "IIIF" in str(work)):
        cc = "iiif"
    elif counted and sid.startswith("CD106-J"):
        cc = "jats"
    status = str(first(row, "status", "novelty", default="미확인"))
    status = {"new": "신규", "inherited": "계승", "duplicate": "중복", "failure": "실패", "failed": "실패"}.get(status, status)
    if counted:
        status = "신규"
    old_count = row.get("countable", False)
    reason = first(row, "count_reason", default="미확인")
    if old_count and not counted:
        reason = "최종38저작 보수 대사에서 산입0. 동일 계보의 대표 자료 또는 허용 증명집합 밖 옛판만의 추가 열람. 원 산입 판단은 previous_countable로 보존. " + str(reason)
    fp = first(row, "fingerprints", "fingerprint", default={})
    if not fp and row.get("sha256"):
        fp = {"sha256": row["sha256"]}
    return dict(id=sid, questions=array(first(row, "questions", "question", default=[])),
                cases=array(first(row, "cases", "case", default=[])),
                original_url=first(row, "original_url", "url"),
                immutable_url=first(row, "immutable_url", "fixed_url"),
                preserved_location=first(row, "preserved_location", "preserved_path", "preservation"),
                accessed_utc=first(row, "accessed_utc", "opened_utc", "requested_utc"),
                publisher=first(row, "publisher"), work_lineage=chosen.get("canonical_work", work),
                edition=first(row, "edition", "version"), location=first(row, "location"),
                fingerprints=fp, observed=first(row, "observed", "observation"),
                supports=first(row, "supports", "supports_or_refutes", "claims_supported", default=[]),
                refutes=first(row, "refutes", "claims_refuted", default=[]),
                limits=first(row, "limits", "limitations"), status=status,
                category=category, count_category=cc, countable=counted,
                direct_read=True if counted else row.get("direct_read", False),
                count_reason=reason, previous_countable=old_count,
                receipt=row.get("receipt", "미확인"), origin_ledger=origin,
                canonical_count_review="evidence/crossdomain/source-count-review.json")


def main():
    canonical = {r["source_id"]: r for r in read("evidence/crossdomain/source-count-review.json")["canonical_works"]}
    sealed = subprocess.check_output(["git", "show", SEAL + ":" + REL + "sources.jsonl"], cwd=REPO, text=True)
    ledgers = [("sealed@" + SEAL + ":sources.jsonl", [json.loads(s) for s in sealed.splitlines() if s.strip()])]
    for path in ["evidence/ggplot2/sources-stage3.jsonl", "evidence/matplotlib/sources-stage3.jsonl",
                 "evidence/crossdomain/sources-crossdomain.jsonl", "evidence/crossdomain/sources-review.jsonl"]:
        ledgers.append((path, [json.loads(s) for s in (ROOT / path).read_text().splitlines() if s.strip()]))
    sources, ids = [], set()
    for origin, records in ledgers:
        for record in records:
            n = normalize_source(record, origin, canonical)
            if n["id"] in ids:
                raise ValueError("Duplicate source record id: " + n["id"])
            ids.add(n["id"])
            sources.append(n)
    assert set(canonical) <= ids, set(canonical) - ids
    assert sum(r["countable"] for r in sources) == 38
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in sources))
    write("evidence/source-reconciliation.json", {
        "basis": "Immutable stage2 sources plus three final project ledgers and separate Q7 reread. Preserved earlier counts are not forecasts.",
        "canonical_allowlist": "evidence/crossdomain/source-count-review.json", "rows": len(sources),
        "counted_works": 38, "reclassified_records": [{"id": r["id"], "prior": r["previous_countable"], "final": r["countable"], "reason": r["count_reason"]} for r in sources if bool(r["previous_countable"]) != r["countable"]],
        "no_prediction_change": hashlib.sha256((ROOT / "predictions.csv").read_bytes()).hexdigest() == "b963763c165faae527e3d214dcd44bb471f390778c49787c7744d696909e7d91"})

    lineages = read("evidence/ggplot2/lineage-final.json") + read("evidence/matplotlib/lineage-final.json")
    for r in lineages:
        r["method_specific"] = first(r, "method_specific", "method_inherited")
        r["method_core_api"] = first(r, "method_core_api", "method_inherited")
        r["method_original_exact"] = first(r, "method_original_exact", "method_inherited")
        r["evidence_files"] = array(first(r, "evidence_files", "evidence_file", default=[]))
    csv_write("lineage.csv", lineages)
    returns = read("evidence/ggplot2/returns-final.json") + read("evidence/matplotlib/returns-final.json")
    for r in returns:
        r["additional_content_http_reads"] = first(r, "additional_content_http_reads", "http_receipt_count", default=0)
        r["logical_document_visits"] = first(r, "logical_work_reads", "extra_logical_documents", default=0)
        r["old_payload_url"] = first(r, "old_payload_url", "old_payload")
        r["new_payload_url"] = first(r, "new_payload_url", "new_payload")
        r["support_urls"] = array(first(r, "support_urls", default=[]))
    csv_write("returns.csv", returns)

    gg = read("evidence/ggplot2/counts-stage3.json")["supplemental"]
    mp = read("evidence/matplotlib/counts-stage3.json")["supplemental"]
    write("evidence/supplemental-summary.json", {"ggplot2": gg, "Matplotlib": mp,
        "no_pooling": "Supplementary events/representatives and main samples have separate denominators; merges and main-overlapping examples are not independent extra outcomes.",
        "ggplot2_results": "evidence/ggplot2/lineage-extra.json", "matplotlib_results": "evidence/matplotlib/supplemental-final.json"})
    print(json.dumps({"source_records": len(sources), "counted_primary_works": 38, "lineage_rows": len(lineages), "returns": len(returns)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
