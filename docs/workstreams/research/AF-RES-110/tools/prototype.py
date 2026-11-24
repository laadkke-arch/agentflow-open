"""Load the read-only Gallim prototype from the fixed Git object."""
from contextlib import contextmanager
import hashlib
import importlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

PROTOTYPE = "fc68f0d1227cab2bf5a7a4b8eef1d9d6f3affc5c"
DIRECTORY = "docs/workstreams/design/gallim/db"
REPO = Path(__file__).resolve().parents[5]


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def catalog_module():
    filename = f"{DIRECTORY}/catalog.py"
    source = git("show", f"{PROTOTYPE}:{filename}")
    from types import ModuleType
    catalog = ModuleType("fixed_gallim_catalog")
    exec(compile(source, f"{PROTOTYPE}:{filename}", "exec"), catalog.__dict__)
    return catalog


@contextmanager
def roundtrip_module():
    # The fixed round trip imports its own sibling modules. Keep its code and
    # fixture in a temporary directory and leave this task's catalogue separate.
    with tempfile.TemporaryDirectory(prefix="af110-prototype-") as directory:
        for file in git("ls-tree", "--name-only", f"{PROTOTYPE}:{DIRECTORY}").decode().splitlines():
            if file.endswith((".py", ".sql")):
                Path(directory, file).write_bytes(git("show", f"{PROTOTYPE}:{DIRECTORY}/{file}"))
        sys.path.insert(0, directory)
        try:
            yield importlib.import_module("roundtrip")
        finally:
            sys.path.remove(directory)
            for file in Path(directory).glob("*.py"):
                sys.modules.pop(file.stem, None)


def calibration():
    module = catalog_module()
    token = "quartzleaf"
    with sqlite3.connect(":memory:", isolation_level=None) as connection:
        app = module.Catalog(connection)
        item = app.add("https://example.org/reference", note=token, provenance="synthetic calibration")
        saved_note = app.get(item)["note"]
        note_only = app.discover(token)
        app.add("https://example.org/reference", title=f"{token} title")
        title = app.discover(token)
        assert saved_note == token and note_only == [] and title[0]["item_id"] == item
    calls = []
    with roundtrip_module() as original:
        discover = original.Catalog.discover

        def observe(self, query, *, operations=(), limit=12):
            output = discover(self, query, operations=operations, limit=limit)
            calls.append({"limit": limit, "operations": list(operations), "returned": len(output)})
            return output

        original.Catalog.discover = observe
        try:
            with original.Ledger(":memory:") as db:
                original.seed_catalog(db)
                revision = original.ingest_scope(db, original.example_scope())
                published = [
                    {
                        "budget": budget,
                        "shortlist": len(answer["catalog_shortlist"]),
                        "displayed": len(answer["answers"]),
                    }
                    for budget in (0, 1, 2, 3)
                    for answer in (original.publish_answer(db, revision, f"af110/{budget}", budget),)
                ]
        finally:
            original.Catalog.discover = discover
    assert [call["limit"] for call in calls] == [1, 2, 3]
    return {
        "prototype_sha": PROTOTYPE, "sqlite": sqlite3.sqlite_version,
        "catalog_sha256": hashlib.sha256(git("show", f"{PROTOTYPE}:{DIRECTORY}/catalog.py")).hexdigest(),
        "note_only": {"saved": saved_note, "ids": [x["item_id"] for x in note_only]},
        "title_and_note": {"ids": [x["item_id"] for x in title], "matched_terms": title[0]["matched_terms"]},
        "publish_answer": published, "actual_discover_calls": calls,
        "scope": "one synthetic note token and the original two-inspection synthetic fixture",
    }


if __name__ == "__main__":
    print(json.dumps(calibration(), indent=2, ensure_ascii=False))
