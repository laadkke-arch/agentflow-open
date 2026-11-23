"""Grade literal window readings against independently stored candidate expectations."""
import argparse
import json
from pathlib import Path


def grade(exposure, reading, expected):
    if exposure == "none":
        return "no_display"
    if not reading or not reading.get("reading_id"):
        return "unread"
    checks = [reading[key] for key in ("c1", "c2", "environment")]
    action = reading["action"]
    if action == "adopt":
        if exposure == "original" and checks == ["yes"] * 3 and expected == "direct":
            return "correct"
        return "false_adoption"
    if action == "reject" and "no" in checks:
        return "rejection_conflict" if expected == "direct" else "refuted"
    if action not in {"hold", "reject"}:
        raise ValueError(f"Unknown action {action}")
    return "hold"


def run_fixtures(path):
    results = []
    for line in path.read_text().splitlines():
        fixture = json.loads(line)
        actual = grade(fixture["exposure"], fixture["reading"], fixture["candidate_expectation"])
        assert actual == fixture["expected_outcome"], (fixture["id"], actual)
        results.append({
            "id": fixture["id"], "expected": fixture["expected_outcome"], "observed": actual,
        })
    return {"fixtures": results, "passed": len(results)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_fixtures(args.fixtures), ensure_ascii=False, indent=2))
