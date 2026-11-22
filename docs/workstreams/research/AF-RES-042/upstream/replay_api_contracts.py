#!/usr/bin/env python3
"""AF-RES-038 P04/P06 API replay driver; prepared but NOT EXECUTED here.

Uses stdlib unittest as the driver. The systems under test are the explicitly
installed pandas/NumPy versions. This is API replay, not proof of the complete
historical environment. No human time or human outcome is generated.

Expected-failure controls intentionally assert the desired contract against
known old behavior. A matching control is expectedFailure; an unexpectedSuccess
is a failed replay expectation, never silently reclassified as success.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys
import unittest
import warnings

PD = None
NP = None
GUARD = None
LOSSY_ERROR = None
GUESS_FORMAT = None
EVENTS = []

DMY = "%d-%m-%Y %H:%M:%S"
MDY = "%m-%d-%Y %H:%M:%S"
P04_INPUTS = {
    "t0": ["01-01-2000 00:00:00", "02-01-2000 00:00:00"],
    "t1_batch1": ["12-01-2000 00:00:00", "13-01-2000 00:00:00"],
    "t1_batch2": ["12-01-2000 00:00:00", "01-13-2000 00:00:00"],
}
# Python literals deliberately preserve int versus float; do not round-trip
# these through a JSON system that normalizes 2.0 to 2.
P06_T0 = [(0, 4), (1, 2.0)]
P06_T1 = [(1, 3.0), (1, 1.5), (1, "potage")]
EXPECTED_VERSIONS = {
    "P04": {"python": "3.10.6", "pandas": "1.4.4"},
    "P06": {"python": "3.10.6", "pandas": "1.5.2"},
}
EXPECTED_FAILURE_COUNTS = {"P04": 1, "P06": 3}

SOURCE_PINS = {
    "P04": [
        "https://github.com/pandas-dev/pandas/blob/e59b6ffd4881ecebb1d3739080d16e162660ae83/web/pandas/pdeps/0004-consistent-to-datetime-parsing.md",
        "https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py",
        "https://github.com/python/cpython/blob/9c7b4bd1646f2170247f88cf59936740d9c4c004/Doc/library/datetime.rst",
    ],
    "P06": [
        "https://github.com/pandas-dev/pandas/blob/1fb0adb5a7b1ba909fb34a19b1d27c7eccdf4119/web/pandas/pdeps/0006-ban-upcasting.md",
        "https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/dtypes/cast.py",
        "https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py",
        "https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/tests/arrays/masked/test_indexing.py",
    ],
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def typed(value):
    return {"value_literal": repr(value), "value_type": type(value).__name__}


def json_value(value):
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, dict):
        return {str(k): json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(v) for v in value]
    if NP is not None and isinstance(value, NP.generic):
        return json_value(value.item())
    return repr(value)


def snapshot(container):
    return {
        "values": json_value(container.tolist()),
        "dtype": str(container.dtype),
    }


def observe(label, operation, inputs, post_state=None):
    """Record actual software observations only when this driver is run."""
    event = {"label": label, "inputs": json_value(inputs)}
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        try:
            result = operation()
        except Exception as exc:
            event["outcome"] = "exception"
            event["exception"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
            raise
        else:
            event["outcome"] = "returned"
            event["output"] = json_value(result)
            return result
        finally:
            if post_state is not None:
                event["post_state"] = json_value(post_state())
            event["warnings"] = [
                {"category": type(w.message).__name__, "message": str(w.message)}
                for w in captured
            ]
            EVENTS.append(event)


def iso_dates(values):
    return [value.isoformat() for value in values]


def vector_explicit(values, fmt):
    return iso_dates(PD.to_datetime(values, format=fmt, exact=True, errors="raise"))


def loop_explicit(values, fmt):
    return [datetime.strptime(value, fmt).isoformat() for value in values]


def strict_infer_once(values, dayfirst=False):
    """Author-composed wrapper, NOT pandas 1.4.4's default inference behavior.

    The pinned private helper chooses one format from the first non-missing
    value; the public API then receives that explicit format. Missing-value
    output behavior, locale and general inference accuracy are outside this
    fixture scope. Each batch is independent, as in the participant packet.
    """
    first = next(value for value in values if not PD.isna(value))
    fmt = GUESS_FORMAT(first, dayfirst=dayfirst)
    EVENTS.append({
        "label": "P04.inference_once",
        "first_non_missing": first,
        "dayfirst": dayfirst,
        "format_used": fmt,
        "wrapper_status": "author_composition_using_pinned_private_helper",
    })
    if fmt is None:
        raise ValueError("No format inferred; no fallback is permitted.")
    return {"format_used": fmt, "values": vector_explicit(values, fmt)}


def native_prevalidated_set(series, index, value):
    """Author-composed consumer boundary around the official private guard."""
    try:
        checked = GUARD(series.dtype, value)
    except LOSSY_ERROR as exc:
        raise TypeError("Incompatible scalar for declared integer dtype") from exc
    # No catch-and-upcast fallback. Mutation occurs only after validation.
    series.iloc[index] = checked


def direct_scalar_set(series, index, value):
    series.iloc[index] = value


class P04Contracts(unittest.TestCase):
    def test_explicit_dmy_vector_and_loop(self):
        expectations = {
            "t0": ["2000-01-01T00:00:00", "2000-01-02T00:00:00"],
            "t1_batch1": ["2000-01-12T00:00:00", "2000-01-13T00:00:00"],
        }
        for name, expected in expectations.items():
            for implementation in (vector_explicit, loop_explicit):
                with self.subTest(batch=name, implementation=implementation.__name__):
                    actual = observe(
                        "P04.explicit." + implementation.__name__,
                        lambda: implementation(P04_INPUTS[name], DMY),
                        {"batch": P04_INPUTS[name], "format": DMY, "errors": "raise"},
                    )
                    self.assertEqual(actual, expected)

    def test_explicit_dmy_vector_and_loop_reject_mismatch(self):
        for implementation in (vector_explicit, loop_explicit):
            with self.subTest(implementation=implementation.__name__):
                with self.assertRaises(ValueError):
                    observe(
                        "P04.explicit_mismatch." + implementation.__name__,
                        lambda: implementation(P04_INPUTS["t1_batch2"], DMY),
                        {"batch": P04_INPUTS["t1_batch2"], "format": DMY},
                    )

    def test_strict_infer_once_dmy(self):
        expected = {
            "t0": ["2000-01-01T00:00:00", "2000-01-02T00:00:00"],
            "t1_batch1": ["2000-01-12T00:00:00", "2000-01-13T00:00:00"],
        }
        for name, values in expected.items():
            actual = observe(
                "P04.strict_infer_dmy",
                lambda: strict_infer_once(P04_INPUTS[name], dayfirst=True),
                {"batch": P04_INPUTS[name], "dayfirst": True},
            )
            self.assertEqual(actual["format_used"], DMY)
            self.assertEqual(actual["values"], values)
        with self.assertRaises(ValueError):
            observe(
                "P04.strict_infer_dmy_mismatch",
                lambda: strict_infer_once(P04_INPUTS["t1_batch2"], dayfirst=True),
                {"batch": P04_INPUTS["t1_batch2"], "dayfirst": True},
            )

    def test_strict_infer_once_mdy_is_an_allowed_alternative(self):
        expected = {
            "t0": ["2000-01-01T00:00:00", "2000-02-01T00:00:00"],
            "t1_batch2": ["2000-12-01T00:00:00", "2000-01-13T00:00:00"],
        }
        for name, values in expected.items():
            actual = observe(
                "P04.strict_infer_mdy",
                lambda: strict_infer_once(P04_INPUTS[name], dayfirst=False),
                {"batch": P04_INPUTS[name], "dayfirst": False},
            )
            self.assertEqual(actual["format_used"], MDY)
            self.assertEqual(actual["values"], values)
        # An error here is correct under the declared MDY mode, not an
        # inferior or incomplete DMY solution.
        with self.assertRaises(ValueError):
            observe(
                "P04.strict_infer_mdy_correct_rejection",
                lambda: strict_infer_once(P04_INPUTS["t1_batch1"], dayfirst=False),
                {"batch": P04_INPUTS["t1_batch1"], "dayfirst": False},
            )

    def test_legacy_infer_characterization(self):
        actual = observe(
            "P04.legacy_infer.characterization",
            lambda: iso_dates(PD.to_datetime(
                P04_INPUTS["t1_batch1"],
                infer_datetime_format=True,
                errors="raise",
            )),
            {"batch": P04_INPUTS["t1_batch1"], "infer_datetime_format": True},
        )
        self.assertEqual(actual, ["2000-12-01T00:00:00", "2000-01-13T00:00:00"])

    @unittest.expectedFailure
    def test_xfail_legacy_infer_should_reject_a_switch(self):
        # This desired-contract assertion should fail on the known old
        # behavior. The preceding ordinary characterization test also checks
        # the exact observed behavior so an arbitrary runtime error cannot
        # by itself establish a successfully reproduced defect.
        with self.assertRaises(ValueError):
            observe(
                "P04.legacy_infer.expected_contract_failure",
                lambda: iso_dates(PD.to_datetime(
                    P04_INPUTS["t1_batch1"],
                    infer_datetime_format=True,
                    errors="raise",
                )),
                {"batch": P04_INPUTS["t1_batch1"], "infer_datetime_format": True},
            )


class P06Contracts(unittest.TestCase):
    def test_typed_fixture_literals_are_preserved(self):
        self.assertIs(type(P06_T0[0][1]), int)
        self.assertIs(type(P06_T0[1][1]), float)
        self.assertIs(type(P06_T1[0][1]), float)
        self.assertIs(type(P06_T1[1][1]), float)
        self.assertIs(type(P06_T1[2][1]), str)

    def test_native_and_nullable_accept_compatible_scalars(self):
        for dtype, setter in (("int64", native_prevalidated_set), ("Int64", direct_scalar_set)):
            with self.subTest(dtype=dtype):
                series = PD.Series([1, 2, 3], dtype=dtype)
                for index, value in P06_T0:
                    observe(
                        "P06.t0." + dtype,
                        lambda: setter(series, index, value),
                        {"index": index, "value": typed(value), "before": snapshot(series)},
                        lambda: snapshot(series),
                    )
                    self.assertEqual(str(series.dtype), dtype)
                self.assertEqual(series.tolist(), [4, 2, 3])

                # t1 is a fresh independent state, not the t0 mutated series.
                series = PD.Series([1, 2, 3], dtype=dtype)
                index, value = P06_T1[0]
                observe(
                    "P06.t1_compatible." + dtype,
                    lambda: setter(series, index, value),
                    {"index": index, "value": typed(value), "before": snapshot(series)},
                    lambda: snapshot(series),
                )
                self.assertEqual(series.tolist(), [1, 3, 3])
                self.assertEqual(str(series.dtype), dtype)

    def test_native_and_nullable_reject_without_mutation(self):
        for dtype, setter in (("int64", native_prevalidated_set), ("Int64", direct_scalar_set)):
            for index, value in P06_T1[1:]:
                with self.subTest(dtype=dtype, value=repr(value)):
                    series = PD.Series([1, 2, 3], dtype=dtype)
                    before = snapshot(series)
                    with self.assertRaises(TypeError):
                        observe(
                            "P06.t1_incompatible." + dtype,
                            lambda: setter(series, index, value),
                            {"index": index, "value": typed(value), "before": before},
                            lambda: snapshot(series),
                        )
                    self.assertEqual(snapshot(series), before)

    def test_legacy_plain_series_upcast_characterization(self):
        for value, dtype, expected in (
            (1.5, "float64", [1.0, 1.5, 3.0]),
            ("potage", "object", [1, "potage", 3]),
        ):
            series = PD.Series([1, 2, 3], dtype="int64")
            observe(
                "P06.legacy_plain_series.characterization",
                lambda: direct_scalar_set(series, 1, value),
                {"index": 1, "value": typed(value), "before": snapshot(series)},
                lambda: snapshot(series),
            )
            self.assertEqual(str(series.dtype), dtype)
            self.assertEqual(series.tolist(), expected)

    def test_numpy_truncation_characterization(self):
        array = NP.array([1, 2, 3], dtype="int64")
        observe(
            "P06.numpy_truncation.characterization",
            lambda: array.__setitem__(1, 1.5),
            {"index": 1, "value": typed(1.5), "before": snapshot(array)},
            lambda: snapshot(array),
        )
        self.assertEqual(array.tolist(), [1, 1, 3])
        self.assertEqual(str(array.dtype), "int64")

    @unittest.expectedFailure
    def test_xfail_plain_series_should_reject_fractional(self):
        series = PD.Series([1, 2, 3], dtype="int64")
        with self.assertRaises(TypeError):
            observe(
                "P06.legacy_fractional.expected_contract_failure",
                lambda: direct_scalar_set(series, 1, 1.5),
                {"value": typed(1.5), "before": snapshot(series)},
                lambda: snapshot(series),
            )

    @unittest.expectedFailure
    def test_xfail_plain_series_should_reject_text(self):
        series = PD.Series([1, 2, 3], dtype="int64")
        with self.assertRaises(TypeError):
            observe(
                "P06.legacy_text.expected_contract_failure",
                lambda: direct_scalar_set(series, 1, "potage"),
                {"value": typed("potage"), "before": snapshot(series)},
                lambda: snapshot(series),
            )

    @unittest.expectedFailure
    def test_xfail_numpy_should_reject_fractional_not_truncate(self):
        array = NP.array([1, 2, 3], dtype="int64")
        with self.assertRaises((TypeError, ValueError)):
            observe(
                "P06.numpy_fractional.expected_contract_failure",
                lambda: array.__setitem__(1, 1.5),
                {"value": typed(1.5), "before": snapshot(array)},
                lambda: snapshot(array),
            )


def write_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    global PD, NP, GUARD, LOSSY_ERROR, GUESS_FORMAT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, choices=("P04", "P06"))
    parser.add_argument("--expected-numpy", required=True)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.report.exists():
        parser.error("Report already exists; choose a new evidence path to preserve the previous run.")

    report = {
        "case_id": args.case,
        "software_replay_started_utc": utc_now(),
        "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "purpose": "API replay with explicit dependency selection",
        "historical_environment_equivalence": "미확인",
        "historical_dependency_lock": "미확인; selected replay dependencies are not recovered original dependencies",
        "human_trial": "not_performed",
        "human_time": None,
        "source_pins": SOURCE_PINS[args.case],
        "expected_versions": dict(EXPECTED_VERSIONS[args.case], numpy=args.expected_numpy),
        "environment": {
            "python": platform.python_version(),
            "python_full": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "uname": dict(platform.uname()._asdict()),
        },
        "inputs": (
            P04_INPUTS if args.case == "P04"
            else {
                "initial": [1, 2, 3],
                "t0": [{"index": i, **typed(v)} for i, v in P06_T0],
                "t1_independent": [{"index": i, **typed(v)} for i, v in P06_T1],
            }
        ),
        "excluded_scope": ["human performance", "NA", "overflow", "timezone", "locale", "general API compatibility", "historical environment identity"],
    }
    try:
        import numpy as numpy_module
        import pandas as pandas_module
        NP, PD = numpy_module, pandas_module
        report["environment"].update({"pandas": PD.__version__, "numpy": NP.__version__})
        report["installed_distributions"] = sorted(
            [{"name": dist.metadata.get("Name", "unknown"), "version": dist.version}
             for dist in importlib.metadata.distributions()],
            key=lambda item: item["name"].lower(),
        )
        expected = report["expected_versions"]
        mismatches = {
            key: {"expected": value, "actual": report["environment"].get(key)}
            for key, value in expected.items()
            if report["environment"].get(key) != value
        }
        if mismatches:
            report.update({"status": "blocked_version_mismatch", "mismatches": mismatches, "tests_executed": False})
            write_report(args.report, report)
            return 2
        if args.case == "P04":
            from pandas._libs.tslibs.parsing import guess_datetime_format
            GUESS_FORMAT = guess_datetime_format
        else:
            from pandas.core.dtypes.cast import LossySetitemError, np_can_hold_element
            GUARD, LOSSY_ERROR = np_can_hold_element, LossySetitemError
    except Exception as exc:
        report.update({
            "status": "blocked_import_or_environment",
            "tests_executed": False,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        })
        write_report(args.report, report)
        return 2

    test_class = P04Contracts if args.case == "P04" else P06Contracts
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
    )
    expected_failure_count_ok = len(result.expectedFailures) == EXPECTED_FAILURE_COUNTS[args.case]
    success = result.wasSuccessful() and expected_failure_count_ok
    report.update({
        "status": "api_replay_matched_expectations" if success else "api_replay_mismatch",
        "tests_executed": True,
        "test_methods_run": result.testsRun,
        "expected_failure_count_required": EXPECTED_FAILURE_COUNTS[args.case],
        "expected_failure_count_observed": len(result.expectedFailures),
        "expected_failure_count_matches": expected_failure_count_ok,
        "failures": [{"test_id": test.id(), "traceback": trace} for test, trace in result.failures],
        "errors": [{"test_id": test.id(), "traceback": trace} for test, trace in result.errors],
        "expected_contract_failures": [{"test_id": test.id(), "traceback": trace} for test, trace in result.expectedFailures],
        "unexpected_successes": [test.id() for test in result.unexpectedSuccesses],
        "skipped": [{"test_id": test.id(), "reason": reason} for test, reason in result.skipped],
        "observations": EVENTS,
        "software_replay_finished_utc": utc_now(),
        "interpretation": "Expected failures reproduce defects in historical API choices; they are not passing alternatives or human observations.",
    })
    write_report(args.report, report)
    print(json.dumps({"case_id": args.case, "status": report["status"], "report": str(args.report)}, ensure_ascii=False))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())

