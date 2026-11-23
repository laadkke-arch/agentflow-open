"""Check the fixed research ledgers, display budgets and output links."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from replay import HERE, boundary_tests, measure, sha256


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def json_obj(path):
    return json.loads(path.read_bytes())


def compare_replay(root):
    baseline = {row["id"]: row for row in jsonl(HERE / "windows.jsonl")}
    trial = {row["id"]: row for row in jsonl(root / "windows.jsonl")}
    assert baseline.keys() == trial.keys()
    for key, window in baseline.items():
        expected = {**window, "source": dict(window["source"])}
        actual = {**trial[key], "source": dict(trial[key]["source"])}
        for data in (expected, actual):
            data["source"].pop("attempts")
        assert expected == actual, key
    assert (HERE / "routes.csv").read_bytes() == (root / "routes.csv").read_bytes()
    assert jsonl(HERE / "evidence/route-actions.jsonl") == jsonl(root / "evidence/route-actions.jsonl")
    return {"matching_display_windows": len(trial), "matching_routes": 33}


def markdown_rows(lines, heading):
    start = next(i for i, line in enumerate(lines) if line.startswith(heading))
    table = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("| "):
            table.append(line)
        elif table:
            break
    return table[2:]


def audit_report_links(cases, pairs, routes, windows):
    result = HERE / "RESULT.md"
    lines = result.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "## 표 1. 고정 12요구와 상위 슬롯"
    main_tables = [markdown_rows(lines, heading) for heading in ("## 표 1.", "## 표 2.", "## 남은 약점")]
    counts = list(map(len, main_tables))
    assert counts == [12, 11, 3]
    assert [line.split()[1] for line in main_tables[0]] == cases
    assert [line.split("<br>", 1)[0].removeprefix("| ") for line in main_tables[1]] == pairs
    for i, line in enumerate(main_tables[0]):
        assert all(f"slots.csv?plain=1#L{2 + 3 * i + slot})" in line for slot in range(3))
    for route, line in zip(routes, main_tables[1], strict=True):
        for view in ("A1", "A2", "B1", "B2"):
            if wid := route[view + "_window"]:
                window = windows[wid]
                assert f"{wid} {window['words']}단어/{window['bytes']}B" in line
                assert f"({route[view + '_url']})" in line
    assert lines[-1].startswith("| 원 Ajv/Drupal판")
    docs = [result, HERE / "SELF_CHECK.md", HERE / "reproduce.md", HERE / "SCOPE.md", HERE / "evidence/library.md"]
    if (HERE / "HANDOFF.md").exists():
        docs.append(HERE / "HANDOFF.md")
    local_links = 0
    external_links = 0
    for doc in docs:
        for url in re.findall(r"\]\(([^\s)]+)\)", doc.read_text(encoding="utf-8")):
            parsed = urlsplit(url)
            if parsed.scheme:
                external_links += 1
                assert parsed.scheme == "https" and parsed.netloc, (doc, parsed)
                continue
            target = (doc.parent / unquote(parsed.path)).resolve()
            assert target.is_relative_to(HERE) and target.exists(), (doc, target)
            local_links += 1
            if match := re.fullmatch(r"L(\d+)(?:-L(\d+))?", parsed.fragment):
                assert 1 <= int(match[1]) <= int(match[2] or match[1]) <= len(target.read_bytes().splitlines()), (doc, url)
    return {"required_table_rows": counts, "local_link_occurrences": local_links,
            "external_url_occurrences": external_links}


def verify():
    freeze = json_obj(HERE / "evidence/doc-seal.json")
    for path, digest in freeze["files_sha256"].items():
        assert sha256((HERE / path).read_bytes()) == digest, path

    slots = csv_rows(HERE / "slots.csv")
    cases = list(dict.fromkeys(row["case_id"] for row in slots))
    assert len(cases) == 12 and len(slots) == 36
    assert [(r["case_id"], int(r["slot"])) for r in slots] == [(case, index) for case in cases for index in (1, 2, 3)]
    chosen = [row for row in slots if row["catalog_id"]]
    pairs = [f"{row['case_id']}/{row['catalog_id']}" for row in chosen]
    assert len(pairs) == len(set(pairs)) == 11
    assert Counter(row["empty_reason"] for row in slots) == {"": 11, "observed_no_match": 18, "matched_pool_exhausted": 7}

    windows = {row["id"]: row for row in jsonl(HERE / "windows.jsonl")}
    assert json_obj(HERE / "evidence/boundary-check.json") == boundary_tests()
    for window in windows.values():
        assert all(window[key] == value for key, value in measure(window["text"]).items())
        assert window["words"] <= 500 and window["source"]["raw_bytes"] > 0
        for seg in window["source_segments"]:
            assert 1 <= seg["start"] <= seg["end"]
            assert 0 <= seg["from"] <= seg["to"] <= len(window["text"])

    routes = csv_rows(HERE / "routes.csv")
    assert [row["pair_id"] for row in routes] == pairs
    assert sum(row["A1_url"] != row["B1_url"] for row in routes) == 6
    actions = jsonl(HERE / "evidence/route-actions.jsonl")
    exposures = json_obj(HERE / "evidence/actual-exposure.json")
    costs = json_obj(HERE / "evidence/costs.json")
    assert [(row["pair_id"], row["view"]) for row in actions] == [(pair, view) for pair in pairs for view in ("A", "B", "P")]
    for view in ("A", "B", "P", "AB", "ABP"):
        paths = [route for route in actions if route["view"] in view]
        shown = [windows[action["window"]] for route in paths for action in route["actions"]]
        for route in paths:
            assert 1 <= len(route["actions"]) <= 2
            assert route["strict_budget"]
            assert route["logical_raw_bytes"] == sum(windows[a["window"]]["source"]["raw_bytes"] for a in route["actions"])
        assert costs[view]["planned_routes"] == len(paths)
        assert costs[view]["actions"] == len(shown)
        assert costs[view]["logical_shown_words"] == sum(w["words"] for w in shown)
        assert costs[view]["logical_shown_bytes"] == sum(w["bytes"] for w in shown)
        assert costs[view]["actual_read_strict_routes"] == sum(r["pair_id"] != exposures["affected_pair"] for r in paths)

    judgments = csv_rows(HERE / "judgments.csv")
    assert [(row["pair_id"], row["view"]) for row in judgments] == [(row["pair_id"], row["view"]) for row in actions]
    verdict_fields = ("C1_rename", "C2_rename", "C1_literal", "C2_literal", "judgment_rename", "judgment_literal")
    for judgment, route in zip(judgments, actions, strict=True):
        ids = [action["window"] for action in route["actions"]]
        assert ids == judgment["windows"].split(",")
        assert all(judgment[field] == "미확인" for field in verdict_fields)
        assert set(re.findall(r"W\d{2}/", judgment["C1_C2_citations"] + judgment["environment_citations"])) <= {f"{w}/" for w in ids}
        assert judgment["C1_C2_direct_refutation"] == "관측 0"

    corpus = jsonl(HERE / "sources.jsonl")
    distinct = [entry for entry in corpus if entry["counts_minimum"]]
    assert len({entry["id"] for entry in corpus}) == len(corpus)
    assert len({entry.get("edition_scan_id") or entry["lineage_id"] for entry in distinct}) == len(distinct)
    types = Counter(entry["kind"] for entry in distinct)
    assert len(distinct) >= 20 and types["implementation"] >= 8
    assert types["requirement"] + types["independent_criteria"] >= 5
    assert types["release_anchor_build"] >= 3 and types["library_primary"] >= 2
    for source in corpus:
        for key in ("original_url", "pinned_url", "read_utc", "read_loci", "scope_and_limit", "questions_and_cases"):
            assert source[key], (source["id"], key)

    runs = jsonl(HERE / "runs.jsonl")
    groups = Counter((entry["pair_id"], entry["arm"]) for entry in runs)
    assert len({(entry["pair_id"], entry["group"]) for entry in runs}) == 12
    assert len(runs) == 32 and set(groups.values()) == {4}
    trial_count = 0
    for run in runs:
        for name in ("stdout", "stderr", "input"):
            path = HERE / run["input_file" if name == "input" else name]
            assert sha256(path.read_bytes()) == run[name + "_sha256"]
        assert run["unchanged"] and run["exit_code"] == 0
        actual = (HERE / run["stdout"]).read_text(encoding="utf-8")
        if run["pair_id"] == "JS-6/SC-005":
            index = int(re.fullmatch(r"\$\.result\[(\d+)\]", run["output_location"])[1])
            assert json.loads(actual)["result"][index]["id"] == run["group"]
            trial_count += 1
        else:
            lines = actual.splitlines()
            for line in run["output_location"]:
                record = json.loads(lines[line - 1])
                assert (record["group"], record["arm"]) == (run["group"], run["arm"])
                trial_count += 1
    accept = json_obj(HERE / "evidence/acceptance-evidence.json")
    assert len({entry["id"] for entry in accept["criteria"]}) == len(accept["criteria"])
    assert {f"Q{i}" for i in range(1, 8)} <= {entry["question"] for entry in accept["criteria"]}
    actual = {entry["id"]: entry["actual"]["numerator"] for entry in accept["criteria"]}
    assert actual["routes-read-strict"] == costs["AB"]["actual_read_strict_routes"]
    assert actual["source-minimum"] == len(distinct)
    assert actual["input-groups"] == len({(entry["pair_id"], entry["group"]) for entry in runs})

    return {
        "slots": len(slots), "filled_pairs": len(chosen), "cases": len(cases), "route_actions": sum(len(r["actions"]) for r in actions),
        "A_B_routes": costs["AB"]["planned_routes"], "A_B_strict_final": costs["AB"]["final_replay_strict_routes"],
        "A_B_strict_actual": costs["AB"]["actual_read_strict_routes"], "unique_windows": len(windows),
        "source_records": len(corpus), "counted_sources": len(distinct), "counted_lineages": len({e["lineage_id"] for e in distinct}),
        "groups_per_runtime_and_arm": {f"{pair}/{arm}": size for (pair, arm), size in groups.items()},
        "output_observations": trial_count, "sources_by_kind": types, "acceptance_criteria": len(accept["criteria"]),
        **audit_report_links(cases, pairs, routes, windows),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replayed", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.replayed:
        result["replay"] = compare_replay(args.replayed)
    print(json.dumps(result, ensure_ascii=False, indent=2))
