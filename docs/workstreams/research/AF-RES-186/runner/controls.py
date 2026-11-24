"""Executed scoring controls and synthetic grouping checks. Main run denominator: zero."""

import json

from scoring import equal_json, grade


def test(source, control_id, input_values, actual, expected):
    return {
        "id": control_id,
        "source_ids": source,
        "inputs": input_values,
        "observed": actual,
        "expected": expected,
        "pass": actual == expected,
    }


def comparison(control_id, left, right, expected):
    return test(["W01"], control_id, {"left": left, "right": right}, equal_json(left, right), expected)


def scorer_controls():
    expected_error = {"kind": "error", "code": "invalid typed value"}
    wrong_error = {"kind": "jsonld_error", "code": "invalid type value", "message": "invalid typed value"}
    matching_error = {"kind": "jsonld_error", "code": "invalid typed value", "message": "different prose"}
    list_context = {"term": {"@id": "https://example.org/term", "@container": "@list"}}
    left = {"@context": list_context, "term": ["a", "b"]}
    right = {"@context": list_context, "term": ["b", "a"]}
    expanded = {
        "expected": {"kind": "json", "value": [{"https://example.org/term": [{"@list": [
            {"@value": "a"}, {"@value": "b"}
        ]}]}]},
        "actual": {"kind": "json", "value": [{"https://example.org/term": [{"@list": [
            {"@value": "b"}, {"@value": "a"}
        ]}]}]},
    }
    actual = {"kind": "json", "value": right}
    expected = {"kind": "json", "value": left}

    return [
        comparison("C01", {"a": 1, "b": "x"}, {"b": "x", "a": 1}, True),
        comparison("C02", [{"@id": "a"}, {"@id": "b"}], [{"@id": "b"}, {"@id": "a"}], True),
        comparison("C03", {"@list": ["a", "b"]}, {"@list": ["b", "a"]}, False),
        comparison("C04", {"@value": 1}, {"@value": True}, False),
        comparison("C05", {"@value": 1}, {"@value": "1"}, False),
        test(["W01"], "C06", {"actual": wrong_error, "expected": expected_error},
             list(grade(wrong_error, expected_error)), ["fail", "wrong_error_code"]),
        test(["W01"], "C07", {"actual": matching_error, "expected": expected_error},
             list(grade(matching_error, expected_error)), ["pass", "exact_error_code"]),
        comparison("C08", ["a", "a", "b"], ["a", "b", "b"], False),
        comparison("C09", {"@language": "EN-us"}, {"@language": "en-US"}, True),
        test(["W01"], "C10", {"actual": actual, "expected": expected, "post_expansion_fixture": expanded},
             {"direct_comparison": equal_json(left, right), "full_grade": list(grade(actual, expected, True, expanded))},
             {"direct_comparison": True, "full_grade": ["fail", "reexpanded_json_mismatch"]}),
    ]


def grouping_controls():
    # S27 describes grouped results. These lab and result IDs are synthetic.
    common_sample = ("NIST-IR8447r1", "Figure8-2/Table8-4", "SRM3233", "table measurand")
    readings = (
        common_sample + ("example-lab-A", "AOAC", "example-result-A"),
        common_sample + ("example-lab-B", "other", "example-result-B"),
    )
    proficiency = {
        "common_protocol_sample_keys": len({row[:len(common_sample)] for row in readings}),
        "measurement_keys": len(set(readings)),
    }
    # S29/S30 document the feed relation. This is a hypothetical matched observation.
    observation = ("USGS", "example-site", "example-activity", "2024-01-01T00:00:00Z",
                   "example-analyte", "example-method", "mg/L", "example-qualifier")
    publications = (("NWIS", observation, 3.0), ("WQP/WQX2.2", observation, 3.0))
    changed_unit = observation[:-2] + ("ug/L", observation[-1])
    water_quality = {
        "publication_keys": len({(portal, key) for portal, key, _ in publications}),
        "observation_keys": len({key for _, key, _ in publications}),
        "observation_keys_after_unit_mutation": len({observation, changed_unit}),
        "value_equality_when_unit_differs": publications[0][2] == publications[1][2],
    }
    return [
        test(["P27"], "K01", {"common_key": common_sample, "synthetic_readings": readings}, proficiency,
             {"common_protocol_sample_keys": 1, "measurement_keys": 2}),
        test(["P29", "P30"], "K02",
             {"synthetic_publications": publications, "mutated_observation_key": changed_unit},
             water_quality, {"publication_keys": 2, "observation_keys": 1,
                             "observation_keys_after_unit_mutation": 2, "value_equality_when_unit_differs": True}),
    ]


if __name__ == "__main__":
    scorer = scorer_controls()
    grouping = grouping_controls()
    print(json.dumps({"main_denominator": 0, "scorer": scorer, "grouping": grouping}, indent=2))
    raise SystemExit(0 if all(item["pass"] for item in scorer + grouping) else 1)
