"""Load the specified Gallim revision without changing it and run its actual entry point."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory

PIN = "fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c"
PREFIX = "docs/workstreams/design/gallim/db"
READINGS = ("scope_input.py", "roundtrip.py", "store.py", "schema.sql")
IMPORTS = ("catalog.py", "demo.py", "retrieval.py")
SOURCE_CLAUSE = "최초 폴더의 파일을 삭제하거나 옮기지 않고"
SYNONYM_CLAUSE = "원래 폴더에서 파일을 지우거나 이동하지 않고"


def load_frozen(folder):
    """Calls are resolved by Python from a private copy of the exact Git blobs."""
    receipts = {}
    for name in (*READINGS, *IMPORTS):
        content = subprocess.check_output(["git", "show", f"{PIN}:{PREFIX}/{name}"])
        (folder / name).write_bytes(content)
        receipts[name] = {
            "sha256": hashlib.sha256(content).hexdigest(),
            "role": "reading" if name in READINGS else "runtime_import",
        }
    sys.path.insert(0, str(folder))
    return receipts


def request_scope(example, clause, revision=None, previous=None, project=None):
    scope = example()
    scope["goal"] = scope["goal"].replace(SOURCE_CLAUSE, clause)
    if revision:
        scope["revision_id"] = revision
    if previous:
        scope["previous_id"] = previous
    if project:
        scope["project_token"] = project
        scope["request_id"] = project + "/scope-request"
    for condition in scope["requirements"]:
        if condition["id"] == "keep_source":
            condition["quote"] = clause
        start = scope["goal"].index(condition["quote"])
        condition["start_char"] = start
        condition["end_char"] = start + len(condition["quote"])
        assert scope["goal"][start:condition["end_char"]] == condition["quote"]
    return scope


def brief(db, answer):
    from store import canonical, digest

    evidence = answer["sources"]
    for fragment in evidence.values():
        assert digest(fragment["quote"]) == fragment["fragment_sha256"]
        assert fragment["end_char"] - fragment["start_char"] == len(fragment["quote"])
    candidates = []
    for item in answer["answers"]:
        run = db.get_decision(item["run_id"])
        candidates.append({
            "catalog_id": item["catalog_item"],
            "candidate_context_id": item["context_id"],
            "candidate_edition": item["context"],
            "status": item["status"],
            "url": item["url"],
            "decision_run_id": item["run_id"],
            "decision_operation_key": run["operation_key"],
            "decision_input_sha256": digest(canonical(run["input"])),
            "decision_output_sha256": digest(canonical(run["output"])),
            "used_citation_count": sum(len(c["citations"]) for c in item["conditions"]),
            "conditions": item["conditions"],
            "discovery_fragment_ids": item["discovery_sources"],
        })
    return {
        "answer_sha256": digest(canonical(answer)),
        "request_revision_id": answer["request_revision_id"],
        "operation_key": answer["operation_key"],
        "goal": answer["original_goal"],
        "request_spans": answer["requirements"],
        "candidates": candidates,
        "sources": evidence,
        "catalog_shortlist": answer["catalog_shortlist"],
        "search_trace": answer["search_trace"],
        "uninspected": answer["uninspected"],
    }


def calibration(folder):
    from roundtrip import publish_answer, read_answer, seed_catalog
    from scope_input import example_scope, ingest_scope
    from store import Ledger

    rows = []
    for label, quote in (("exact", SOURCE_CLAUSE), ("synonym", SYNONYM_CLAUSE)):
        with Ledger(folder / f"calibration-{label}.sqlite") as db:
            seed_catalog(db)
            revision = ingest_scope(db, request_scope(example_scope, quote))
            published = publish_answer(db, revision, "calibration")
            saved = read_answer(db, "calibration")
            assert published == saved
            rows.append({"label": label, **brief(db, saved)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    with TemporaryDirectory(prefix="af111-calibration-") as temp:
        folder = Path(temp)
        pins = load_frozen(folder)
        output = {
            "git_pin": PIN,
            "input_blobs": pins,
            "sqlite": sqlite3.sqlite_version,
            "rows": calibration(folder),
        }
    options.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
