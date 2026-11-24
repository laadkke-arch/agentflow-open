"""Cross-check the reviewed Translate constructor and hit branches in the census."""

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from functools import cache
from pathlib import Path

from release_artifacts import SOURCE

CHANGE = "207fc99295cc6a126425dd5fcb3aaec1865bd424"
ANCHORS = ("6.0.0", "10.11.0")
RULES = ("filter_with_features", "layers_with_features")
UNKNOWN = "unreadable"
FIELDS = [
    *RULES, "translate_condition", "source_rules_match", "behavior_change_ancestor",
    "release_line", "package_reissue_evidence",
]


def inspect(code):
    text = code.decode("utf-8").replace("_this.", "this.")
    # Fail closed on a new shape. These patterns index the manually read branches.
    shape = {
        "collection": r"this\.features_\s*=\s*options\.features\s*!==\s*undefined",
        "lookup": r"map\.forEachFeatureAtPixel\(",
        "feature_check": r"this\.filter_\(feature,\s*layer\)",
        "membership": r"(?:includes\(this\.features_\.getArray\(\),\s*feature\)|"
                      r"this\.features_\.getArray\(\)\.includes\(feature\))",
        "layer_forward": r"layerFilter:\s*this\.layerFilter_",
        "layer_default": r"layerFilter\s*=\s*TRUE\s*;",
        "class_gate": r"feature instanceof Feature",
    }
    lines = {name: text.count("\n", 0, found.start()) + 1 if (found := re.search(pattern, text)) else None
             for name, pattern in shape.items()}
    collection_gate = all(lines[key] for key in ("collection", "lookup", "membership"))

    def rule(option, form, connected):
        access = re.search(r"\boptions\." + option + r"\b", text)
        if not access:
            return "option-absent", None
        found = re.search(form, text)
        if not found or not connected:
            return UNKNOWN, None
        return ("collection-first" if found[1] else "both-applied",
                text.count("\n", 0, found.start()) + 1)

    filter_rule, lines["filter_constructor"] = rule(
        "filter", r"this\.filter_\s*=\s*options\.filter(\s*&&\s*!this\.features_)?\s*\?\s*options\.filter\s*:\s*TRUE",
        collection_gate and lines["feature_check"],
    )
    layer_rule, lines["layer_constructor"] = rule(
        "layers", r"if\s*\(options\.layers(\s*&&\s*!this\.features_)?\)",
        collection_gate and lines["layer_default"] and lines["layer_forward"],
    )
    return {
        RULES[0]: filter_rule, RULES[1]: layer_rule,
        "translate_condition": "present" if "options.condition" in text else "absent",
        "lines": lines,
    }


def transitions(rows, key):
    return [(before["version"], after["version"]) for before, after in zip(rows, rows[1:])
            if before[key] != after[key]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    with args.artifacts.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        columns = reader.fieldnames

    @cache
    def source(blob):
        return inspect(subprocess.check_output(["git", "-C", str(args.upstream), "cat-file", "blob", blob]))

    module_groups = {}
    source_groups = {}
    for row in rows:
        version = row["version"]
        sha = row["translate_sha256"]
        artifact = {"lines": {}, **dict.fromkeys(RULES, UNKNOWN), "translate_condition": UNKNOWN}
        if sha:
            data = (args.cache / f"Translate-{version}.js").read_bytes()
            assert hashlib.sha256(data).hexdigest() == sha, version
            artifact = inspect(data)
            group = module_groups.setdefault(sha, {**artifact, "versions": []})
            group["versions"].append(version)
        row.update({key: artifact[key] for key in (*RULES, "translate_condition")})
        tag, head = row["tag_commit"], row["npm_git_head"]
        ref = tag or head
        blob = row["tag_source_blob"] or row["githead_source_blob"]
        verdict = "unavailable"
        if blob:
            upstream = source(blob)
            verdict = "yes" if all(row[key] == upstream[key] for key in (*RULES, "translate_condition")) else "no"
            upstream_group = source_groups.setdefault(blob, {**upstream, "sample_commit": ref, "versions": []})
            upstream_group["versions"].append(version)
        result = subprocess.run(["git", "-C", str(args.upstream), "merge-base", "--is-ancestor", CHANGE, ref],
                                capture_output=True)
        row.update({
            "source_rules_match": verdict,
            "behavior_change_ancestor": {0: "yes", 1: "no"}.get(result.returncode, "unknown"),
            "release_line": {
                "10.7.1": "npm-only-version-from-main-before-10.8",
                "10.7.2": "npm-only-older-10.7-artifact-reissue",
            }.get(version, ".".join(version.split(".")[:2])),
            "package_reissue_evidence": {
                "10.7.1": "separate-untagged-gitHead-check-changelog",
                "10.7.2": "10.7.0-gitHead-check-full-archive-file-diff",
            }.get(version, "none-observed"),
        })
    publish = sorted(rows, key=lambda row: int(row["publish_rank"]))
    semver_edges = {rule: transitions(rows, rule) for rule in RULES}
    publish_edges = {rule: transitions(publish, rule) for rule in RULES}
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, [*columns, *FIELDS], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    args.receipt.write_text(json.dumps({
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "stable_count": len(rows), "tarballs_verified": sum(row["tarball_status"] == "verified" for row in rows),
        "contract_counts": {rule: dict(Counter(row[rule] for row in rows)) for rule in RULES},
        "tag_match": dict(Counter(row["tag_source_status"] for row in rows)),
        "githead_match": dict(Counter(row["githead_source_status"] for row in rows)),
        "source_rule_match": dict(Counter(row["source_rules_match"] for row in rows)),
        "semver_edges": semver_edges,
        "publish_edges": publish_edges,
        "publish_rank_differs": [row["version"] for row in rows if row["semver_rank"] != row["publish_rank"]],
        "browser_versions": [row["version"] for row in rows if row["version"] in
                             set(ANCHORS) | {version for edges in semver_edges.values()
                                             for pair in edges[:2] for version in pair}],
        "distribution_groups": module_groups,
        "upstream_groups": source_groups,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
