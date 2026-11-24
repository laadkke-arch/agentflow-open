"""Compare replay evidence from clean checkouts and preserve measured clocks."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from summarize import ROOT, json_file

TIME_FIELDS = {"clockMs", "eventTimeMs", "timeOriginMs"}
ENV_FIELDS = ("browser", "executableSha256", "browserEngineSha256", "node", "arch", "kernel",
              "playwright", "esbuild", "gpu", "fileHashes", "browserVersions")


def normalize(value):
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items() if key not in TIME_FIELDS}
    return value


def observation(raw):
    return normalize({key: value for key, value in raw.items() if key != "notices"})


def content_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def environment(root, mode):
    combined = root / "environment-all.json"
    return json_file(combined if combined.exists() else root / f"environment-{mode}.json")


def observed_duration(raw):
    steps = {item["phase"]: item.get("clockMs") for item in raw["steps"]}
    return steps["settled"] - steps["down"] if "down" in steps else None


def compare(reference, candidate, expected_candidate, expected_reference):
    cases = json_file(ROOT / "fixture" / "cases.json")
    groups = {}
    for mode in ("main", "controls", "supplement", "bare"):
        first_env, second_env = environment(reference, mode), environment(candidate, mode)
        differences = [field for field in ENV_FIELDS if first_env[field] != second_env[field]]
        for label, evidence, expected in (("reference", first_env, expected_reference),
                                          ("candidate", second_env, expected_candidate)):
            if expected and evidence["codeCommit"] != expected:
                differences.append(f"{label} checkout commit")
        ids = [case["id"] for case in cases if case["mode"] == mode]
        extras = {}
        for label, root in (("reference", reference), ("candidate", candidate)):
            extras[label] = sorted(path.stem for path in (root / mode).glob("*.json") if path.stem not in ids)
        rows = []
        for run_id in ids:
            old_path, new_path = [root / mode / (run_id + ".json") for root in (reference, candidate)]
            row = {"id": run_id}
            if not old_path.is_file() or not new_path.is_file():
                rows.append({**row, "changed": ["raw log missing"]})
                continue
            old_raw, new_raw = json_file(old_path), json_file(new_path)
            old, new = observation(old_raw), observation(new_raw)
            if old_raw["status"] != "observed" or new_raw["status"] != "observed":
                rows.append({**row, "changed": ["invalid raw status"]})
                continue
            rows.append({
                **row,
                "changed": [key for key in sorted(old.keys() | new.keys()) if old.get(key) != new.get(key)],
                "normalized_sha256": [content_hash(old), content_hash(new)],
                "reference_down_to_settled_ms": observed_duration(old_raw),
                "candidate_down_to_settled_ms": observed_duration(new_raw),
                "notice_counts": [dict(Counter(n["type"] for n in raw["notices"])) for raw in (old_raw, new_raw)],
            })
        groups[mode] = {
            "cases": len(ids), "matches": sum(not row["changed"] for row in rows),
            "environment_differences": differences, "unexpected_raw_ids": extras,
            "reference": {key: first_env[key] for key in ("codeCommit", "startedUtc", "finishedUtc")},
            "candidate": {key: second_env[key] for key in ("codeCommit", "startedUtc", "finishedUtc")},
            "notice_count_differences": sum(a != b for row in rows if "notice_counts" in row
                                            for a, b in [row["notice_counts"]]),
            "rows": rows,
        }
    return {
        "clock_fields_excluded_from_trace_equality": sorted(TIME_FIELDS),
        "browser_notices_counted_separately": True,
        "groups": groups,
        "ok": all(group["cases"] == group["matches"] and not group["environment_differences"]
                  and not any(group["unexpected_raw_ids"].values()) for group in groups.values()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--commit")
    parser.add_argument("--reference-commit")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = compare(args.reference, args.candidate, args.commit, args.reference_commit)
    args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for mode, group in result["groups"].items():
        print(mode, f'{group["matches"]}/{group["cases"]}', "environment differences",
              group["environment_differences"], "notice count differences", group["notice_count_differences"])
    return int(not result["ok"])


if __name__ == "__main__":
    raise SystemExit(main())
