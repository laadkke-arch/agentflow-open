"""Evaluate intact, extracted, and explicitly reconstructed JS-3 in jschon."""

import copy
import json
import platform
from pathlib import Path
import traceback

from jschon import JSON, JSONSchema, __version__, create_catalog

fixture = json.loads(Path(__file__).with_name("js3.json").read_bytes())


def reconstruction(src, dialect):
    if isinstance(src, dict):
        out = {("$defs" if k == "definitions" else k): reconstruction(v, dialect) for k, v in src.items()}
        if "$schema" in out:
            out["$schema"] = dialect
        return out
    if isinstance(src, list):
        return [reconstruction(item, dialect) for item in src]
    if isinstance(src, str) and src.startswith("#/definitions/"):
        return src.replace("#/definitions/", "#/$defs/", 1)
    return src


def run(arm, group, missing):
    person = dict(group["person"])
    if missing:
        del person[missing]
    if arm == "literal_extracted":
        types = fixture["types"]["properties"]
        schema = fixture["definitions"]["definitions"]["person"]
        instance = person
    elif arm == "literal_whole":
        types = fixture["types"]
        schema = fixture["definitions"]
        instance = {"person": person}
    else:
        dialect = fixture["diagnostic_dialect"]
        types = reconstruction(fixture["types"], dialect)
        schema = reconstruction(fixture["definitions"], dialect)
        instance = {"person": person}
    before = copy.deepcopy(instance)
    out = {
        "arm": arm, "group": group["id"], "dropped_required": missing, "input": before,
        "expected_valid": group["expected_valid"], "python": platform.python_version(), "jschon": __version__,
        "catalog_versions": ["2020-12"], "remote_registry": "none; two documents constructed in one Catalog",
        "format_assertion": "disabled; email guard not validated",
    }
    phase = "register_types"
    try:
        catalog = create_catalog("2020-12", name=arm + group["id"] + (missing or ""))
        JSONSchema(types, catalog=catalog)
        phase = "compile_person"
        loaded = JSONSchema(schema, catalog=catalog)
        phase = "evaluate"
        result = loaded.evaluate(JSON(instance))
        out.update(actual_valid=result.valid, evaluation=result.output("basic"),
                   outcome_matches=result.valid == group["expected_valid"])
    except Exception as error:
        out.update(actual_valid=None, error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
    out.update(last_phase=phase, unchanged=instance == before, input_after=instance)
    return out


if __name__ == "__main__":
    for arm in fixture["arms"]:
        for group in fixture["groups"]:
            for missing in group.get("drop_each", [None]):
                print(json.dumps(run(arm, group, missing), ensure_ascii=False))
