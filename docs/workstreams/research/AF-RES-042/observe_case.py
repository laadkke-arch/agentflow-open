"""Read the sealed AF-RES-042 literals through independent API calls."""
import argparse
import ast
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import sys
import traceback
import unittest
from unittest.mock import patch
import warnings

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NA = "해당 없음"
UNKNOWN = "미확인"


def kind(value):
    return f"{type(value).__module__}.{type(value).__qualname__}"


def exception(exc):
    frames = traceback.extract_tb(exc.__traceback__)
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "frames": [
            {"file": frame.filename, "line": frame.lineno, "symbol": frame.name}
            for frame in frames
        ],
        "cause": (
            {"type": type(exc.__cause__).__name__, "message": str(exc.__cause__)}
            if exc.__cause__ is not None else NA
        ),
    }


def dates(values):
    return {
        "values": [item.isoformat() for item in values],
        "container_type": type(values).__name__,
        "element_types": [type(item).__name__ for item in values],
        "qualified_element_types": [kind(item) for item in values],
        "dtype": str(values.dtype) if hasattr(values, "dtype") else NA,
    }


def date_probe(row, values, obs):
    from pandas._libs.tslibs.parsing import guess_datetime_format

    name = row["implementation"]
    fmt = row["requested_format"]
    obs["initial"] = list(values)
    obs["format"] = fmt
    try:
        if name == "legacy_infer":
            # The public return value doesn't expose which fallback branch ran.
            candidate = guess_datetime_format(values[0], dayfirst=False)
            obs.update(format=UNKNOWN, calculated_first_candidate=candidate)
            result = pd.to_datetime(values, infer_datetime_format=True, errors="raise")
        else:
            if row["declaration"] == "first_nonmissing":
                first_i, first = next((i, v) for i, v in enumerate(values) if not pd.isna(v))
                fmt = guess_datetime_format(first, dayfirst=row["dayfirst"])
                obs.update(first_nonmissing_index=first_i, first_nonmissing=first)
                if fmt is None:
                    raise ValueError("No matching format found by the first-value helper")
            obs["format"] = fmt
            if name == "stdlib_dmy":
                result = []
                for i, value in enumerate(values):
                    obs["error_index"] = i
                    result.append(datetime.strptime(value, fmt))
                obs.pop("error_index")
            else:
                result = pd.to_datetime(values, format=fmt, exact=True, errors="raise")
    except ValueError as exc:
        obs.update(outcome="exception", exception=exception(exc))
        if "error_index" not in obs and fmt is not None and name != "legacy_infer":
            # The vector API raises for the batch. Reparse each singleton with
            # that same format to locate the invalid literal independently.
            by_item = []
            with warnings.catch_warnings(record=True):
                for i, value in enumerate(values):
                    try:
                        item = pd.to_datetime([value], format=fmt, exact=True, errors="raise")[0]
                    except ValueError as single_error:
                        by_item.append({"index": i, "error": str(single_error)})
                    else:
                        by_item.append({"index": i, "value": item.isoformat(), "type": kind(item)})
            obs["positional_diagnostic"] = by_item
            obs["error_index"] = next((x["index"] for x in by_item if "error" in x), UNKNOWN)
    else:
        obs.update(outcome="returned", **dates(result))
    finally:
        obs["final_input"] = values
        obs["input_unchanged"] = obs["initial"] == values


def snapshot(container):
    values = container.tolist()
    get = container.iloc if isinstance(container, pd.Series) else container
    return {
        "values": [item.item() if isinstance(item, np.generic) else item for item in values],
        "scalar_types": [kind(get[i]) for i in range(len(container))],
        "tolist_element_types": [kind(item) for item in values],
        "container_type": kind(container),
        "dtype": str(container.dtype),
    }


def integer_probe(row, value, obs):
    name = row["implementation"]
    index = row["typed_input"]["index"]
    if name == "numpy_scalar_set":
        container = np.array(row["initial_values"], dtype=row["initial_dtype"])
    else:
        container = pd.Series(row["initial_values"], dtype=row["initial_dtype"])
    before = snapshot(container)
    calls = []
    try:
        if name == "numpy_scalar_set":
            calls.append("ndarray[index]")
            container[index] = value
        else:
            if name == "native_guard":
                from pandas.core.dtypes.cast import LossySetitemError, np_can_hold_element

                calls.append("np_can_hold_element")
                try:
                    value = np_can_hold_element(container.dtype, value)
                except LossySetitemError as exc:
                    raise TypeError("Incompatible scalar for declared integer dtype") from exc
            elif name == "python_int_then_set":
                calls.append("int")
                value = int(value)
            obs["setter_input"] = {"literal": repr(value), "type": kind(value)}
            calls.append("Series.iloc[index]")
            container.iloc[index] = value
    except (TypeError, ValueError) as exc:
        obs.update(outcome="exception", exception=exception(exc))
    else:
        obs.update(outcome="returned", return_type="builtins.NoneType")
    finally:
        after = snapshot(container)
        obs.update(
            initial=before,
            final=after,
            applied_calls=calls,
            value_changed_indices=[
                i for i, (old, new) in enumerate(zip(before["values"], after["values"])) if old != new
            ],
            scalar_type_changed_indices=[
                i for i, (old, new) in enumerate(zip(before["scalar_types"], after["scalar_types"]))
                if old != new
            ],
        )


def different_fields(row, obs, expectation, check_representation):
    actual = obs if row["case"] == "P04" else {**obs, **obs["final"]}
    mismatch = []
    for field, wanted in expectation.items():
        if field == "error_type":
            detected = obs.get("exception", {}).get("type")
            if wanted == "explicit_incompatibility_error":
                if detected not in ("TypeError", "ValueError"):
                    mismatch.append(field)
                continue
        elif field == "post_state":
            detected = "unchanged_input_no_batch_result" if obs["input_unchanged"] else UNKNOWN
        else:
            if not check_representation and row["case"] == "P04" and (
                field in ("container_type", "dtype", "element_types")
                or field == "format" and row["implementation"] == "legacy_infer"
            ):
                continue
            detected = actual.get(field)
        if json.dumps(detected) != json.dumps(wanted):
            mismatch.append(field)
    return mismatch


def run_probe(row):
    typed = row["typed_input"]
    value = ast.literal_eval(typed["literal"])
    if row["case"] == "P04":
        assert type(value) is list and all(type(item) is str for item in value)
        operation = date_probe
        actual_type = "list[str]"
    else:
        assert type(value).__name__ == typed["type"]
        operation = integer_probe
        actual_type = type(value).__name__
    obs = {
        "probe_id": row["probe_id"], "implementation": row["implementation"],
        "typed_input": {**typed, "observed_type": actual_type},
    }
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        operation(row, value, obs)
    obs["warnings"] = [
        {"type": item.category.__name__, "message": str(item.message)} for item in caught
    ]
    obs["prediction_mismatch_fields"] = different_fields(row, obs, row["predicted_behavior"], True)
    obs["contract_mismatch_fields"] = different_fields(row, obs, row["source_expectation"], False)
    return obs


class BrokenArray:
    """Stand-in for the NumPy setter in the synthetic testing-only fault."""
    def __init__(self, values, dtype):
        self.array = np.array(values, dtype=dtype)
        self.dtype = self.array.dtype

    def tolist(self):
        return self.array.tolist()

    def __setitem__(self, index, value):
        raise RuntimeError("AF-RES-042 injected NumPy setitem error")


def fault_audit(case, output):
    spec = importlib.util.spec_from_file_location(
        "af038_frozen_replay", HERE / "upstream" / "replay_api_contracts.py"
    )
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    gate_path = output.with_suffix(".blocked-import.json")
    with patch.dict(sys.modules, {"pandas": None}), patch.object(
        sys, "argv", [str(spec.origin), "--case", case, "--expected-numpy",
                      "1.23.5", "--report", str(gate_path)]
    ):
        gate_exit = driver.main()
    gate = json.loads(gate_path.read_text())

    driver.PD, driver.NP = pd, np
    if case == "P04":
        klass = driver.P04Contracts
        pairs = [(
            "legacy_infer", "test_legacy_infer_characterization",
            "test_xfail_legacy_infer_should_reject_a_switch",
            patch.object(pd, "to_datetime", side_effect=RuntimeError("AF-RES-042 injected date error")),
        )]
    else:
        klass = driver.P06Contracts
        real_setter = driver.direct_scalar_set

        def broken_setter(target):
            def assign(series, index, value):
                if type(value) is type(target) and value == target:
                    raise RuntimeError("AF-RES-042 injected Series setitem error")
                real_setter(series, index, value)
            return assign

        pairs = [
            (
                "plain_fractional", "test_legacy_plain_series_upcast_characterization",
                "test_xfail_plain_series_should_reject_fractional",
                patch.object(driver, "direct_scalar_set", side_effect=broken_setter(1.5)),
            ),
            (
                "plain_text", "test_legacy_plain_series_upcast_characterization",
                "test_xfail_plain_series_should_reject_text",
                patch.object(driver, "direct_scalar_set", side_effect=broken_setter("potage")),
            ),
            (
                "numpy_fractional", "test_numpy_truncation_characterization",
                "test_xfail_numpy_should_reject_fractional_not_truncate",
                patch.object(driver, "NP", type("FaultNumpy", (), {"array": BrokenArray, "generic": np.generic})),
            ),
        ]
    diagnoses = []
    for label, ordinary, expected_failure, fault in pairs:
        with fault:
            result = unittest.TextTestRunner(stream=io.StringIO()).run(
                unittest.TestSuite([klass(ordinary), klass(expected_failure)])
            )
        observed = {
            "control": label, "ordinary_test": ordinary, "xfail_test": expected_failure,
            "tests_run": result.testsRun, "ordinary_errors": len(result.errors),
            "expected_failures": len(result.expectedFailures),
            "unexpected_successes": len(result.unexpectedSuccesses),
            "unexpected_trace_contains_injection": all(
                "RuntimeError: AF-RES-042 injected" in trace
                for _, trace in result.errors + result.expectedFailures
            ),
        }
        observed["matched"] = (
            observed["tests_run"] == 2
            and observed["ordinary_errors"] == observed["expected_failures"] == 1
            and observed["unexpected_successes"] == 0
            and observed["unexpected_trace_contains_injection"]
        )
        diagnoses.append(observed)
    import_gate = {
        "exit_code": gate_exit, "tests_executed": gate["tests_executed"],
        "test_methods_run": gate.get("test_methods_run", 0),
        "expected_failures": gate.get("expected_failure_count_observed", 0),
        "status": gate["status"], "error": gate["error"],
    }
    import_gate["matched"] = (
        gate_exit == 2 and import_gate["status"] == "blocked_import_or_environment"
        and not import_gate["tests_executed"] and import_gate["expected_failures"] == 0
        and import_gate["error"]["type"] == "ModuleNotFoundError"
    )
    return {"injected_import_gate": import_gate, "injected_operation_errors": diagnoses}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("P04", "P06"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.with_suffix(".blocked-import.json").exists():
        parser.error("choose a new output path")
    inputs = [json.loads(line) for line in (HERE / "inputs.jsonl").read_text().splitlines()]
    rows = [row for row in inputs if row["case"] == args.case]
    results = [run_probe(row) for row in rows]
    audit = fault_audit(args.case, args.output)
    expected_rows = {"P04": 18, "P06": 25}
    matches = [
        not obs["prediction_mismatch_fields"]
        and bool(obs["contract_mismatch_fields"]) == row["discriminator"]
        for row, obs in zip(rows, results)
    ]
    report = {
        "case": args.case, "ordinary_probes": len(results), "probes_matched": sum(matches),
        "probes": results, "fault_audit": audit,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("case", "ordinary_probes", "probes_matched")}))
    return int(not (
        len(results) == expected_rows[args.case] and all(matches)
        and audit["injected_import_gate"]["matched"]
        and all(x["matched"] for x in audit["injected_operation_errors"])
    ))


if __name__ == "__main__":
    raise SystemExit(main())
