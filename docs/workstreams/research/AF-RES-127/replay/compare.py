"""Compare pinned browser inputs and the observable event sequence across checkouts."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from analyze import MODES, ROOT, read, sha256, summarize

TIME_FIELDS = {"clockMs", "eventTimeMs", "timeOriginMs"}
INPUT_FIELDS = (
    "browserBundleSha256", "browserBundleBytes", "versions", "fileHashes",
    "loadedSources", "releaseFiles", "npmIntegrity", "sourceCommit",
    "browser", "executableSha256", "node", "arch", "kernel", "userAgent",
)


def normalize(value):
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items() if key not in TIME_FIELDS}
    return value


def observation(raw):
    return normalize({key: value for key, value in raw.items() if key != "notices"})


def content_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def compare(plan, reference, candidate, expected_commit):
    groups = {}
    for mode in MODES:
        old_env = read(reference / mode / "environment.json")
        new_env = read(candidate / mode / "environment.json")
        inputs = [field for field in INPUT_FIELDS if old_env[field] != new_env[field]]
        if expected_commit and new_env["codeCommit"] != expected_commit:
            inputs.append("expected candidate checkout SHA")
        paths = []
        for row in plan["cases"][mode]:
            name = row["id"] + ".json"
            old_path = reference / mode / name
            new_path = candidate / mode / name
            old_raw, new_raw = read(old_path), read(new_path)
            old, new = observation(old_raw), observation(new_raw)
            differences = [key for key in sorted(old.keys() | new.keys()) if old.get(key) != new.get(key)]
            checked = summarize(plan, row, mode, candidate)
            for surface in new["surfaces"].values():
                if sha256(candidate / surface["path"]) != surface["sha256"]:
                    differences.append("PNG bytes " + surface["path"])
            paths.append({
                "id": row["id"], "outcome": checked["outcome"], "scope": checked["comparison_scope"],
                "trace_events": len(new_raw["records"]),
                "reference_raw_sha256": sha256(old_path), "candidate_raw_sha256": sha256(new_path),
                "reference_behavior_sha256": content_hash(old), "candidate_behavior_sha256": content_hash(new),
                "reference_notices": dict(Counter(n["text"] for n in old_raw["notices"])),
                "candidate_notices": dict(Counter(n["text"] for n in new_raw["notices"])),
                "changed_fields": differences,
                "candidate_quality_errors": checked["reasons"],
            })
        groups[mode] = {
            "reference_code_sha": old_env["codeCommit"], "candidate_code_sha": new_env["codeCommit"],
            "input_differences": inputs, "candidate_bundle_sha256": new_env["browserBundleSha256"],
            "run_count": len(paths), "matches": sum(not (r["changed_fields"] or r["candidate_quality_errors"]) for r in paths),
            "notice_count_differences": sum(r["reference_notices"] != r["candidate_notices"] for r in paths),
            "rows": paths,
        }
    return {
        "time_fields_removed": sorted(TIME_FIELDS),
        "browser_notices_checked_separately": True,
        "reference": str(reference), "candidate": str(candidate), "groups": groups,
        "ok": all(not group["input_differences"] and group["matches"] == group["run_count"] for group in groups.values()),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--commit")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = compare(read(ROOT / "plan.json"), args.reference, args.candidate, args.commit)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for mode, group in result["groups"].items():
        print(mode, f'{group["matches"]}/{group["run_count"]}', "input differences", group["input_differences"],
              "notice count differences", group["notice_count_differences"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
