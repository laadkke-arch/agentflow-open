"""Read-only audit of the aggregate source ledger; writes only this review folder."""
from __future__ import annotations
import ast
from collections import Counter, defaultdict
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import re

REVIEW = Path(__file__).resolve().parent
P = REVIEW.parent.parent
errors = []
checks = []
raw_files = {}


def read(path):
    data = (P / path).read_bytes()
    raw_files[path] = data
    return data.decode("utf-8")


def check(name, condition, detail=None):
    result = {"check": name, "passed": bool(condition)}
    if detail is not None:
        result["detail"] = detail
    checks.append(result)
    if not condition:
        errors.append(result)


def canonical(work):
    work = re.sub(r"^(?:stackoverflow|so)-question-", "so-question-", work)
    if work in {"SCH-SUITE", "JSON-SCHEMA-TEST-SUITE"}:
        return "JSON-SCHEMA-TEST-SUITE"
    if work.startswith("jsonldjs-"):
        return "SUP-JSONLDJS"
    if work.startswith("pyld-"):
        return "SUP-PYLD"
    if work.startswith("SUP-SC032"):
        return "SUP-SC032"
    return work


def independently_classify(r):
    state = str(r["직접열람_상태"]).lower()
    kind = r["자료종류"]
    sid = r["source_id"]
    work = canonical(r["work_id"])
    if "실패" in state or "fail" in state or "접근 실패" in kind:
        return "failed"
    if sid.startswith(("INPUT-", "DEP052-", "EXEC-")) or work.lower().startswith("af-res-056") or "실제 실행" in kind or "자체 실행" in kind:
        return "internal_or_execution"
    if sid in {"AUTH-LOC-PDF", "WIN-07"}:
        return "mirror_republication"
    if sid == "AUTH-GETTY-SOURCEREC" or "synonyms" in work or "ALIASES" in sid or "metadata" in kind.lower() or "메타데이터" in kind or "재사용 허가" in kind or "라이선스" in kind or "license" in kind.lower():
        return "metadata_or_license"
    if r.get("primary_external") is False:
        return "internal_or_execution"
    return "direct_primary"


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    script = read("aggregate_sources.py")
    constants = {}
    for node in ast.parse(script).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {"LEDGERS", "REQUIRED", "ALLOCATIONS"}:
                    constants[target.id] = ast.literal_eval(node.value)
    expected_requirements = {"questions": 8, "catalogs_editorial": 4, "standards_tests": 4, "suppliers": 4, "authority_records": 4}
    check("assignment allocations have exactly 8+4+4+4+4", {k: len(v) for k, v in constants["ALLOCATIONS"].items()} == expected_requirements)
    expected = []
    subledger_counts = {}
    for path in constants["LEDGERS"]:
        lines = read(path).splitlines()
        subledger_counts[path] = len(lines)
        for line_no, line in enumerate(lines, 1):
            row = json.loads(line)
            check("required fields " + row["source_id"], all(k in row for k in constants["REQUIRED"]))
            row["origin_ledger"] = path
            row["origin_line"] = line_no
            old = row["work_id"]
            row["work_id"] = canonical(old)
            if old != row["work_id"]:
                row["original_work_id"] = old
            row["counting_class"] = independently_classify(row)
            row["required_allocation"] = next((k for k, values in constants["ALLOCATIONS"].items() if row["source_id"] in values), "")
            expected.append(row)
    actual = [json.loads(line) for line in read("sources.jsonl").splitlines()]
    check("aggregate exactly equals subledgers plus declared normalization", actual == expected)
    check("source IDs unique", len({r["source_id"] for r in actual}) == len(actual))
    counts = json.loads(read("evidence/source-counts.json"))
    by_id = {r["source_id"]: (i, r) for i, r in enumerate(actual, 1)}
    works = defaultdict(list)
    for line, row in enumerate(actual, 1):
        if row["counting_class"] == "direct_primary":
            works[row["work_id"]].append((line, row))
    row_classes = dict(Counter(r["counting_class"] for r in actual))
    check("observation total", counts["observation_rows"] == len(actual))
    check("row classes", counts["row_classes"] == row_classes)
    check("unique primary total", counts["unique_direct_primary_works"] == len(works))
    allocations = []
    for bucket, ids in constants["ALLOCATIONS"].items():
        observed = counts["allocations"][bucket]
        check("quota cardinality " + bucket, observed["required"] == expected_requirements[bucket] == observed["obtained"])
        for sid, reported in zip(ids, observed["works"]):
            line, row = by_id[sid]
            check("allocation source pointer " + sid, reported == {"source_id": sid, "work_id": row["work_id"], "sources_line": line, "url": row["원본_URL"], "location": row["쪽_절_행_셀"]})
            check("allocation is opened external primary " + sid, row["counting_class"] == "direct_primary")
            allocations.append(row["work_id"])
    check("24 different allocated work IDs", len(allocations) == len(set(allocations)) == 24)
    check("allocated count receipt", counts["allocated_unique_primary_works"] == len(set(allocations)))
    inventory = list(csv.DictReader(io.StringIO(read("evidence/primary-works.csv"))))
    check("primary inventory covers exactly grouped works", {r["work_id"] for r in inventory} == set(works) and len(inventory) == len(works))
    for entry in inventory:
        grouped = works[entry["work_id"]]
        check("inventory links " + entry["work_id"], entry["sources_lines"] == ";".join(str(n) for n, r in grouped) and entry["source_ids"] == ";".join(r["source_id"] for n, r in grouped))
        check("inventory representative " + entry["work_id"], entry["representative_source_id"] == grouped[0][1]["source_id"] and entry["representative_url"] == grouped[0][1]["원본_URL"])
    own_exec = [r for r in actual if "자체 실행" in r["자료종류"] or "실제 실행" in r["자료종류"] or r["source_id"].startswith("EXEC-")]
    check("all own execution records excluded", all(r["counting_class"] == "internal_or_execution" for r in own_exec), [r["source_id"] for r in own_exec])
    check("known mirror rows excluded", all(by_id[sid][1]["counting_class"] == "mirror_republication" for sid in ("AUTH-LOC-PDF", "WIN-07")))
    check("schema draft variants merged", {by_id[sid][1]["work_id"] for sid in ("SCH-STD-VALID07", "SCH-STD-VALID20", "SCH-STD-VALID20-RECHECK")} == {"json-schema-validation"})
    check("W3C suite version copies merged", {r["work_id"] for r in actual if r["source_id"].startswith("LD-TEST-") or r["source_id"].startswith("LD-SUP-PY-SUITE-")} == {"w3c-jsonld-api-conformance-suite"})
    question_rows = [r for r in actual if r["counting_class"] == "direct_primary" and r["work_id"].startswith("so-question-")]
    check("80 distinct author question works", len(question_rows) == len({r["work_id"] for r in question_rows}) == 80)
    schema_raw = json.loads(read("evidence/schema-pre/revisions-p1.json"))
    schema_first = {r["post_id"]: r for r in schema_raw["items"] if r.get("revision_number") == 1 and "body" in r}
    schema_hash_n = 0
    ld_meta = {r["question_id"]: r for r in json.loads(read("evidence/ld-pre/revision-audit.json"))["records"]}
    ld_meta_n = 0
    for row in question_rows:
        qid = int(row["work_id"].split("-")[-1])
        check("question original URL identity " + str(qid), f"/questions/{qid}/" in row["원본_URL"])
        if row["source_id"].startswith("SCH-Q"):
            first = schema_first[qid]
            digest = hashlib.sha256(first["body"].encode()).hexdigest()
            check("schema first-body hash " + str(qid), digest in row["판_또는_SHA"] and first["revision_guid"] in row["판_또는_SHA"])
            schema_hash_n += 1
        else:
            meta = ld_meta[qid]
            check("LD revision metadata link " + str(qid), meta["original_body_sha256"] in row["판_또는_SHA"] and meta["original_revision_guid"] in row["판_또는_SHA"])
            ld_meta_n += 1
    check("files stable during audit", all((P / path).read_bytes() == data for path, data in raw_files.items()))
    result = {
        "reviewer": "/root/catalogs; same ChatGPT collaboration, author of catalog-pre and schema-diagnostics subledgers",
        "independence": "independent recomputation of root aggregation; not external or blind independent review",
        "utc_started": started,
        "utc_finished": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "read_only_root": True,
        "root_aggregation_executed": False,
        "input_sha256": {path: hashlib.sha256(data).hexdigest() for path, data in raw_files.items()},
        "subledger_rows": subledger_counts,
        "observation_rows": len(actual),
        "row_classes": row_classes,
        "unique_primary_work_ids": len(works),
        "allocated_unique_work_ids": len(set(allocations)),
        "allocation_counts": expected_requirements,
        "schema_question_body_hashes_recomputed": schema_hash_n,
        "ld_question_revision_metadata_links_checked": ld_meta_n,
        "ld_question_body_hashes_recomputed": 0,
        "limitation": "LD raw first bodies are not saved in this snapshot; metadata/hash joins checked but original body hashes not independently regenerated. Factual source spot checks and catalog-boundary sensitivity are in source-audit.md.",
        "catalog_same_system_sensitivity": {"catalog_editorial_works": 2, "allocated_works": 22, "overall_unique_work_ids": len(works) - 2, "interpretation": "optional stricter boundary, not the declared main counting rule"},
        "semantic_notes": ["LD-SUP-PY-CHECKOUT mixes external fixed-source reading with local import observation; shares existing SUP-PYLD and changes no unique/allocated count", "PyLD is ported from JavaScript; two implementation source works do not imply independent algorithm ancestry", "catalog data contract and submission form are separate authored artifacts with overlapping fields; not independent editorial publishers", "extra broad 109-work inventory is not a substitute for the explicit 24-source allocation"],
        "checks": checks,
        "errors": errors,
        "status": "pass_with_scope_qualifications" if not errors else "failed",
        "exit_code": 0 if not errors else 1,
    }
    (REVIEW / "source-audit-receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("utc_finished", "observation_rows", "row_classes", "unique_primary_work_ids", "allocated_unique_work_ids", "schema_question_body_hashes_recomputed", "ld_question_revision_metadata_links_checked", "status", "exit_code")}, ensure_ascii=False))
    return result["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
