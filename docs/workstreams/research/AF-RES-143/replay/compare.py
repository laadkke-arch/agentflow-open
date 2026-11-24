"""Adjudicate values and inputs using the frozen roster; never reads signal data."""
import argparse
from collections import Counter
from pathlib import Path

from cases import cases_for, observation
from common import ROOT, json_in, read_jsonl, sha, utc, write_csv, write_json


def cells(run):
    if run is None or run["status"] != "ok":
        return {}
    found = {c["id"]: c for c in run["cases"]}
    if len(found) != len(run["cases"]):
        raise ValueError("duplicate result cells")
    return found


def adjudicate(first, second, out):
    rosters = json_in(ROOT / "evidence/roster.json")["cohorts"]
    sets = [{(row["package"], row["version"]): row for row in runs} for runs in (first, second)]
    rows, functions, boundaries, release_rows = [], [], [], []
    for cohort in rosters:
        package = cohort["package"]
        versions = [r["version"] for r in cohort["selected"]]
        expected = list(cases_for(package))
        verified = {}
        for version in versions:
            key = package, version
            a, b = [runs.get(key) for runs in sets]
            aa, bb = cells(a), cells(b)
            identity_keys = ("package", "version", "runtime", "loader", "entry", "entry_sha256", "lock_sha256",
                             "inputs_sha256", "probe_sha256", "manifest_sha256", "direct")
            same_identity = bool(a and b and all(a.get(field) == b.get(field) for field in identity_keys))
            shared, errors = {}, Counter()
            for item in expected:
                left, right = aa.get(item["id"]), bb.get(item["id"])
                if not left or not right:
                    errors["missing_observation"] += 1
                    continue
                if not same_identity or (left["input_sha256"] != item["input_sha256"] or
                                         right["input_sha256"] != item["input_sha256"]):
                    errors["identity_or_input_mismatch"] += 1
                    continue
                if observation(left) != observation(right) or left["accessor_trace"] != right["accessor_trace"]:
                    errors["path_disagreement"] += 1
                    continue
                if left["result"]["type"] == "timeout":
                    errors["reproduced_case_timeout"] += 1
                    continue
                shared[item["id"]] = left
            verified[version] = shared
            release_rows.append({"package": package, "version": version, "status_a": a["status"] if a else None,
                                 "status_b": b["status"] if b else None, "same_identity": same_identity,
                                 "expected": len(expected), "agreed": len(shared), "missing_or_disagreed": dict(errors),
                                 "agreed_types": dict(Counter(c["result"]["type"] for c in shared.values())),
                                 "error_a": a.get("error", {}).get("code") if a else None,
                                 "error_b": b.get("error", {}).get("code") if b else None})
        for before, after in zip(versions, versions[1:]):
            group = []
            for definition in expected:
                ident = definition["id"]
                left, right = verified[before].get(ident), verified[after].get(ident)
                target = {
                    "package": package, "previous": before, "version": after, "function": definition["function"],
                    "layer": definition["layer"], "cell": ident, "input_sha256": definition["input_sha256"],
                    "before_type": left["result"]["type"] if left else "",
                    "after_type": right["result"]["type"] if right else "",
                }
                if not left or not right:
                    state = "unconfirmed"
                    why = "no two-path value at " + "/".join(v for v, data in ((before, left), (after, right)) if not data)
                elif "api_absent" in (target["before_type"], target["after_type"]):
                    state = "api_absent_both" if target["before_type"] == target["after_type"] else "availability"
                    why = "public API availability"
                else:
                    state = "unchanged" if observation(left) == observation(right) else "changed"
                    why = "return/exception and original/argument/p before-after"
                target.update(state=state, reason=why, trace_changed=bool(left and right and
                              left["accessor_trace"] != right["accessor_trace"]))
                group.append(target)
            rows.extend(group)
            boundaries.append(edge_row(package, before, after, "ALL", group))
            for name in sorted({row["function"] for row in group}):
                functions.append(edge_row(package, before, after, name, [row for row in group if row["function"] == name]))
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "output-cells.csv", rows)
    write_csv(out / "output-pairs.csv", boundaries + functions)
    write_json(out / "output-read.json", {"completed_utc": utc(), "release_checks": release_rows,
                                          "counts": dict(Counter(r["state"] for r in rows)),
                                          "paths": [[r["label"] for r in data[:1]] for data in (first, second)]})


def edge_row(package, before, after, fn, rows):
    counts = Counter(r["state"] for r in rows)
    state = ("changed" if counts["changed"] else "availability" if counts["availability"] else
             "unconfirmed" if counts["unconfirmed"] else "all-absent" if counts["api_absent_both"] == len(rows) else "unchanged")
    return {"package": package, "previous": before, "version": after, "function": fn, "state": state,
            "cells": len(rows), **{k: counts[k] for k in ("changed", "unchanged", "unconfirmed", "availability", "api_absent_both")},
            "trace_changes": sum(r["trace_changed"] for r in rows)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=Path, required=True)
    parser.add_argument("--second", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    adjudicate(read_jsonl(args.first), read_jsonl(args.second), args.out)
    result = json_in(args.out / "output-read.json")
    result["inputs"] = [{"path": str(path), "sha256": sha(path.read_bytes())} for path in (args.first, args.second)]
    write_json(args.out / "output-read.json", result)


if __name__ == "__main__":
    main()
