"""JSON-LD Test Suite README comparison for the fixed expansion/compaction sample."""

from decimal import Decimal


def canonical(value, key=None):
    if isinstance(value, dict):
        return ("object", tuple((name, canonical(item, name)) for name, item in sorted(value.items())))
    if isinstance(value, list):
        items = tuple(canonical(item) for item in value)
        return ("array", items if key == "@list" else tuple(sorted(items)))
    if value is None:
        return ("null",)
    if isinstance(value, bool):
        return ("boolean", value)
    if isinstance(value, (int, float, Decimal)):
        return ("number", Decimal(str(value)))
    if isinstance(value, str):
        return ("string", value.lower() if key == "@language" else value)
    raise TypeError(f"Not a JSON value: {type(value).__name__}")


def equal_json(left, right):
    return canonical(left) == canonical(right)


def equal_observation(left, right):
    if left["kind"] != right["kind"]:
        return False
    if left["kind"] == "json":
        return equal_json(left["value"], right["value"])
    if left["kind"] == "jsonld_error":
        return left["code"] == right["code"]
    raise ValueError("Infrastructure errors cannot be compared as JSON-LD observations")


def grade(actual, expected, post_required=False, post=None):
    """Return a verdict and the rule that produced it."""
    if actual["kind"] == "infrastructure_error":
        return "incomparable", "infrastructure_error"
    if expected["kind"] == "error":
        if actual["kind"] != "jsonld_error":
            return "fail", "returned_json_instead_of_error"
        if actual["code"] != expected["code"]:
            return "fail", "wrong_error_code"
        return "pass", "exact_error_code"
    if actual["kind"] != "json":
        return "fail", "unexpected_jsonld_error"
    if not equal_json(actual["value"], expected["value"]):
        return "fail", "json_mismatch"
    if post_required:
        reexpanded = post or {}
        if any(reexpanded.get(side, {}).get("kind") != "json" for side in ("actual", "expected")):
            return "incomparable", "reexpansion_unavailable"
        if not equal_observation(reexpanded["actual"], reexpanded["expected"]):
            return "fail", "reexpanded_json_mismatch"
        return "pass", "json_and_reexpansion_match"
    return "pass", "json_match"
