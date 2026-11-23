"""Unexecuted next-step probe for AF-RES-073 P3; no network resolution.

Run only in a recorded historical environment. It measures that environment;
it does not establish every old reader's behavior or schema-URI immutability.
"""
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform

import jsonschema
import nbformat

HERE = Path(__file__).resolve().parent


def installed_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def error_record(error):
    return {"type": type(error).__name__, "message": str(error)}


def main():
    if nbformat.__version__ != "5.7.3":
        raise SystemExit("Require nbformat.__version__ == 5.7.3; no probe executed.")
    schema_path = Path(nbformat.__file__).resolve().parent / "v4" / "nbformat.v4.5.schema.json"
    schema_bytes = schema_path.read_bytes()
    validator = jsonschema.Draft4Validator(json.loads(schema_bytes))
    fixture = json.loads((HERE / "fixtures.json").read_text(encoding="utf-8"))
    observations = []
    for case in fixture["cases"]:
        notebook = case["notebook"]
        row = {"case_id": case["case_id"]}
        try:
            errors = list(validator.iter_errors(copy.deepcopy(notebook)))
            row["direct_v4_5_schema"] = {
                "accepted": not errors,
                "errors": [error_record(error) for error in errors],
            }
        except Exception as error:
            row["direct_v4_5_schema"] = {"operation_error": error_record(error)}
        try:
            nbformat.validate(copy.deepcopy(notebook))
            row["nbformat_validate"] = {"accepted": True}
        except Exception as error:
            row["nbformat_validate"] = {"accepted": False, "error": error_record(error)}
        captured = {}
        try:
            result = nbformat.reads(
                json.dumps(notebook),
                as_version=nbformat.NO_CONVERT,
                capture_validation_error=captured,
            )
            row["nbformat_reads"] = {
                "returned": True,
                "result": result,
                "captured_errors": {key: error_record(value) for key, value in captured.items()},
            }
        except Exception as error:
            row["nbformat_reads"] = {"returned": False, "error": error_record(error)}
        observations.append(row)
    print(json.dumps({
        "probe": "AF-RES-073-P3",
        "python": platform.python_version(),
        "nbformat_source": str(Path(nbformat.__file__).resolve()),
        "package_versions": {name: installed_version(name) for name in [
            "nbformat", "jsonschema", "fastjsonschema", "traitlets", "jupyter_core",
        ]},
        "validator_environment": os.environ.get("NBFORMAT_VALIDATOR"),
        "raw_schema_path": str(schema_path),
        "raw_schema_sha256": hashlib.sha256(schema_bytes).hexdigest(),
        "uri_network_resolution_performed": False,
        "C2_immutability_verified": False,
        "observations": observations,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

