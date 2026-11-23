"""Check ledger links, measured denominators, execution bytes, and replay outputs."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def csv_rows(file):
    with (ROOT / file).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def json_lines(file):
    return [json.loads(line) for line in (ROOT / file).read_text(encoding="utf-8").splitlines()]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode()


def supporting(row, allow_transfer=False):
    allowed = {"D", "T"} if allow_transfer else {"D"}
    return {field for field in ("C1", "C2", "environment") if row[field] in allowed}


def intervention_pair(cases, routes, judgments, left, right, *, protocol=False, changed=False,
                      exact=False, allow_transfer=False):
    out = {"pairs": 0, "same_address": 0, "gains": {x: 0 for x in ("C1", "C2", "environment")},
           "losses": {x: 0 for x in ("C1", "C2", "environment")}, "joint_gain": 0, "joint_loss": 0}
    for case in cases:
        x, y = (f"{case}/{name}" for name in (left, right))
        first, second = judgments[x], judgments[y]
        same = routes[x]["first_url"] == routes[y]["first_url"]
        if changed and same:
            continue
        if exact and (first["exact_selection"] != "True" or second["exact_selection"] != "True"):
            continue
        if protocol and (first["protocol_strict"] != "True" or second["protocol_strict"] != "True"):
            continue
        out["pairs"] += 1
        out["same_address"] += same
        a, b = supporting(first, allow_transfer), supporting(second, allow_transfer)
        for field in b - a:
            out["gains"][field] += 1
        for field in a - b:
            out["losses"][field] += 1
        out["joint_gain"] += len(b) == 3 and len(a) != 3
        out["joint_loss"] += len(a) == 3 and len(b) != 3
    return out


def audit(replay_dirs=(), report=False):
    frame = csv_rows("frame.csv")
    selected = [r for r in frame if r["case_id"]]
    ids = [r["case_id"] for r in selected]
    assert len(frame) == 120 and len(ids) == 12
    assert list(Counter(r["repo"] for r in frame).values()) == [60, 60]
    assert len({r["url"] for r in frame}) == 120 and len({r["body_sha256"] for r in selected}) == 12
    for repo in set(r["repo"] for r in frame):
        rows = [r for r in frame if r["repo"] == repo]
        assert rows == sorted(rows, key=lambda r: (r["created_utc"], int(r["number"])))
        assert list(map(int, (r["rank"] for r in rows))) == list(range(1, 61))

    paths = csv_rows("routes.csv")
    route = {r["route_key"]: r for r in paths}
    assert len(route) == len(paths) == 36
    assert list(route) == [f"{case}/{tag}" for case in ids for tag in "ABC"]
    window_rows = json_lines("windows.jsonl")
    wins = {w["window"]: w for w in window_rows}
    assert len(wins) == len(window_rows) and 0 < len(wins) <= 72
    assert all(0 < w["tokens"] <= 500 for w in wins.values())
    action_rows = json_lines("evidence/route-actions.jsonl")
    action_count = Counter(x["route_key"] for x in action_rows)
    use_count = Counter(x["window"] for x in action_rows if x["window"])
    for r in paths:
        assert action_count[r["route_key"]] == int(r["actions"]) <= 2
        assert (r["first_state"] == "READ") == bool(r["first_window"])
        if r["first_window"]:
            w = wins[r["first_window"]]
            assert (w["pin"], w["path"], w["start"]) == (r["pin"], r["path"], int(r["display_line"] or r["line"]))
            assert r["first_range"] == f'{w["line_first"]}–{w["line_last"]}'
            assert r["same_first_as_A"] == str(r["first_url"] == route[r["case_id"] + "/A"]["first_url"])
    assert all(w["route_actions_using"] == use_count[w["window"]] for w in wins.values())
    assert len(action_rows) == sum(int(r["actions"]) for r in paths)

    raw_codes = csv_rows("judgments.csv")
    codes = {r["route_key"]: r for r in raw_codes}
    assert list(codes) == list(route)
    for key, r in codes.items():
        assert r["first_window"] == route[key]["first_window"]
        shown = {wins[id]["source_url"] for id in (r["first_window"], r["second_window"]) if id}
        for name in ("C1", "C2", "environment"):
            flag = r[name]
            assert flag in {"D", "R", "T", "U"}
            if flag != "U":
                assert r[name + "_origin"] in shown
    blind = json_lines("evidence/blind-readings.jsonl")
    assert set(wins) == {r["window"] for r in blind}
    assert [r["order"] for r in blind] == list(range(1, len(wins) + 1))

    sources = json_lines("sources.jsonl")
    assert len({s["id"] for s in sources}) == len(sources)
    counted = [s for s in sources if s["counts_for_minimum"]]
    assert len({s["lineage"] for s in counted}) == len(counted) >= 20
    assert {r["url"] for r in selected} <= {s["url"] for s in counted}
    assert all(s["open_location"] and s["observed"] and s["limitation"] for s in sources)

    runs = json_lines("runs.jsonl")
    by_run = {(r["case"], r["group"]): r for r in runs}
    execution_cases = [r["case_id"] for r in selected if r["execution"] == "yes"]
    assert list(by_run) == [(c, f"G{g}") for c in execution_cases for g in range(1, 5)]
    for c in execution_cases:
        fixture = json.loads((ROOT / "fixtures" / f"{c}.json").read_text())
        for opt in fixture["groups"]:
            r = by_run[c, opt["group"]]
            digest = sha256(json.dumps(opt["input"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
            assert r["input_sha256"] == digest and r["expectation"] == opt["expectation"]
            assert r["fixture_sha256"] == sha256((ROOT / r["input_location"]).read_bytes())
            for att in r["attempts"]:
                assert att["input_sha256"] == r["input_sha256"] and att["pin"] == r["pin"]
                if att.get("output_location") and att["stdout"]:
                    assert (ROOT / att["output_location"]).read_text() == att["stdout"]
                if att.get("error_location") and att["stderr"]:
                    assert (ROOT / att["error_location"]).read_text() == att["stderr"]
                if "observed" in att:
                    obs = att["observed"]
                    assert obs == json.loads(att["stdout"])
                    assert obs["output_sha256"] == sha256(json_bytes(obs["observed"]))
                    assert obs["case"] == c and obs["group"] == opt["group"]
                    assert obs["version"] == fixture["version"]

    for directory in replay_dirs:
        for source, regenerated in [
            ("routes.csv", "routes.csv"), ("windows.jsonl", "windows.jsonl"),
            ("evidence/route-actions.jsonl", "actions.jsonl"),
        ]:
            assert (ROOT / source).read_bytes() == (directory / regenerated).read_bytes(), source

    layers = {
        "all": ids,
        "timestamp_equal": [r["case_id"] for r in selected if r["initial_body_status"] == "timestamp_equal"],
        "author_exact": [r["case_id"] for r in selected if r["release_layer"] == "author_exact"],
        "named_range_floor": [r["case_id"] for r in selected if r["release_layer"] == "named_range_floor"],
        "comparison_before_post": [r["case_id"] for r in selected if r["release_layer"] == "comparison_before_post"],
    }
    counts = {
        "screened": len(frame), "cases": len(ids), "distinct_selected_authors": len({r["author"] for r in selected}),
        "routes": len(route), "routes_first_read": sum(r["first_state"] == "READ" for r in paths),
        "route_exact_by_arm": dict(Counter(r["route"] for r in codes.values() if r["exact_selection"] == "True")),
        "route_budget_strict": sum(r["budget_strict"] == "True" for r in codes.values()),
        "route_protocol_strict": sum(r["protocol_strict"] == "True" for r in codes.values()),
        "second_actions": sum(x["action"] == 2 for x in action_rows),
        "window_identities": len(wins), "window_display_hashes": len({w["sha256"] for w in wins.values()}),
        "joint_cases": sum(any(len(supporting(codes[f"{c}/{arm}"])) == 3 for arm in "ABC") for c in ids),
        "joint_routes": sum(len(supporting(r)) == 3 for r in codes.values()),
        "joint_windows": len({r["first_window"] for r in codes.values() if len(supporting(r)) == 3}),
        "conditions_direct": sum(r[f] == "D" for r in codes.values() for f in ("C1", "C2")),
        "conditions_refuted": sum(r[f] == "R" for r in codes.values() for f in ("C1", "C2")),
        "environment_direct": sum(r["environment"] == "D" for r in codes.values()),
        "environment_transfer": sum(r["environment"] == "T" for r in codes.values()),
        "source_records": len(sources), "source_urls": len({r["url"] for r in sources}),
        "source_lineages_all": len({r["lineage"] for r in sources}), "source_lineages_counted": len(counted),
        "groups": len(runs), "attempts": sum(len(r["attempts"]) for r in runs),
        "actual_release_groups": sum(r["case"] in layers["author_exact"] for r in runs),
        "expectation_matches": sum(r.get("meets_expected", False) for r in runs),
        "behavior_groups": sum(r.get("observed", {}).get("observed", {}).get("phase") in ("validate", "convert") for r in runs),
        "compiler_observations": sum(r.get("observed", {}).get("observed", {}).get("phase") ==
                                     "caught_compile_or_validate" for r in runs),
        "initial_process_failures": sum(r["attempts"][0]["status"] == "process_failed" for r in runs),
    }
    metrics = {"counts": counts, "layer_cases": layers, "pairs": {}}
    for layer, cases in layers.items():
        metrics["pairs"][layer] = {
            kind: {a + b: intervention_pair(cases, route, codes, a, b, **kwargs)
                   for a, b in (("A","B"), ("B","C"), ("A","C"))}
            for kind, kwargs in {
                "all_budget": {}, "protocol": {"protocol": True},
                "changed": {"changed": True}, "changed_protocol": {"changed": True, "protocol": True},
                "exact_and_changed": {"exact": True, "changed": True},
                "names_transfer": {"allow_transfer": True},
            }.items()
        }
    if report:
        stored = json.loads((ROOT / "evidence/metrics.json").read_text())
        assert stored == metrics
        result = (ROOT / "RESULT.md").read_text()
        assert result.startswith("## 표 1. ")
        table_one, table_two_and_more = result.split("\n## 표 2. ", 1)
        table_two = table_two_and_more.split("\n## ", 1)[0]
        assert sum(x.startswith("| [") for x in table_one.splitlines()) == 12
        assert sum(x.startswith("| **") for x in table_two.splitlines()) == 16
        for r in paths:
            assert r["first_url"] in result
        for r in runs:
            assert r["output_location"] in table_two
        acceptance = json.loads((ROOT / "evidence/acceptance-evidence.json").read_text())
        for item in acceptance["checks"]:
            if metric := item.get("audit_count_key"):
                assert item["numerator"] == counts[metric]
        assert len(re.findall(r"(?m)^\| W[1-3] ·", result)) == 3
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replayed", action="append", type=Path, default=[])
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--metrics", type=Path)
    args = parser.parse_args()
    result = audit(args.replayed, args.report)
    if args.metrics:
        args.metrics.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
