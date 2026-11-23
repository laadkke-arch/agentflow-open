"""Replay the four AF-RES-084 case matrices against the pinned AF-RES-080 inputs."""

from collections import Counter
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
PRIOR_SHA = "152f5261ab9a35ab675ab003931ac4dc89966b55"
PRIOR = f"{PRIOR_SHA}:docs/workstreams/research/AF-RES-080"
CASES = ("CN01", "AN01", "CC01", "AC01")
POSITIONS = ("NR", "BR", "NE", "BE")
KNOWN = {"positive", "refuted", "absent-in-scope"}

FEATURES = {
    "CN01": ("click.Option.prompt", "click.Option.multiple"),
    "AN01": ("attrs.field.default + attrs.field.init",),
    "CC01": ("click.version_option",),
    "AC01": ("attrs.hook.__attrs_init_subclass__",),
}
AUTHOR_SPELLINGS = {"CC01": "click.version_option", "AC01": "attr.define.slots"}
CONSUMER_MISSING = {
    "AN01": "원 질문의 attrs·Python 배포 묶음",
    "CC01": "원 작성자의 성공 -V stdout·종료와 같은 실행의 Click·Python",
    "AC01": "원 수행자의 성공 두 키·최종 클래스와 같은 실행의 attrs·Python",
}
CHANGED_SCOPE = {
    "CN01": "상위 링크에서 프롬프트·다중값의 결합 거부를 보이는 절까지 확대",
    "AN01": "필드 메뉴에서 init=False와 default가 동시 적용되는 절까지 확대",
    "CC01": "일반 메뉴에서 버전 데코레이터의 -V·alpha 바인딩까지 확대",
    "AC01": "상위 초기화 메뉴에서 완성 이후 전용 상속 훅까지 확대",
}


def jsonl(contents):
    return [json.loads(line) for line in contents.splitlines() if line.strip()]


def here(name):
    return (ROOT / name).read_text(encoding="utf-8")


def prior(name):
    return subprocess.check_output(["git", "show", f"{PRIOR}/{name}"], cwd=ROOT)


def index(items, key):
    rows = {}
    for item in items:
        identity = key(item)
        assert identity not in rows, f"Duplicate input key: {identity}"
        rows[identity] = item
    return rows


def find_feature(features, name):
    for feature in features.values():
        if name == feature["id"] or name in feature["names"]:
            return feature
    parent, _, setting = name.rpartition(".")
    for feature in features.values():
        if parent in feature["names"]:
            canonical = features.get(f"{feature['id']}.{setting}")
            if canonical:
                return canonical
    return None


def match_feature(features, name):
    feature = find_feature(features, name)
    if feature is None:
        return {"query": name, "canonical": None, "aliases": []}
    aliases = sorted(set([name, *feature["names"]]))
    return {"query": name, "canonical": feature["id"], "aliases": aliases}


def observations(case, position, runs):
    if position.startswith("N"):
        return {"c1": "scope-absent", "c2": "scope-absent", "counterexample": "", "runs": []}
    match case:
        case "CN01":
            role = "new-reference" if position == "BR" else "stated-question-match"
            boundary = f"CN01-{role}-boundary"
            positive = f"CN01-{role}-positive"
            result = runs[boundary]["observed"]
            if result["prompt_seen"] and result["iterable_error"] and not result["names"] and result["cli_exit"] == 1:
                return {"c1": "yes", "c2": "refuted", "counterexample": "입력 한 줄이 iterable 검사에서 거부됨",
                        "runs": [boundary, positive]}
        case "AN01":
            run = "AN01-new-reference-positive"
            control = "AN01-new-reference-boundary"
            result = runs[run]["observed"]
            boundary = runs[control]["observed"]
            if (result["parameters"] == ["a", "b"] and result["field_present"] and result["sum"] is None
                    and boundary["parameters"] == ["a", "b", "sum"]):
                return {"c1": "yes", "c2": "yes", "counterexample": "init=True이면 sum 인자가 노출됨",
                        "runs": [run, control]}
        case "CC01":
            run = "CC01-reference-positive"
            control = "CC01-reference-boundary"
            result = runs[run]["observed"]
            boundary = runs[control]["observed"]
            if (result["selected_flag"]["exit_code"] == 0 and result["selected_flag"]["output"] == "probe, version alpha\n"
                    and result["default_flag"]["exit_code"] == 2 and boundary["error"]["type"] == "TypeError"):
                return {"c1": "yes", "c2": "yes", "counterexample": "param_decls 키워드는 등록 실패",
                        "runs": [run, control, "CC01-question-only-positive", "CC01-question-only-boundary"]}
        case "AC01":
            run = "AC01-reference-positive"
            control = "AC01-reference-boundary"
            result = runs[run]["observed"]["documented_attrs_hook"]
            other = runs[run]["observed"]["reported_unslotted"]
            if (result["call_count"] == 2
                    and result["int_lookup"]["class"] == "Int" and result["int_lookup"]["is_final_class"]
                    and result["range_lookup"]["class"] == "IntRange" and result["range_lookup"]["is_final_class"]
                    and other["range_lookup"]["exception"] == "KeyError"):
                return {"c1": "yes", "c2": "yes", "counterexample": "원 slots=False 방법의 둘째 키는 KeyError",
                        "runs": [run, control, "AC01-historical-control-positive", "AC01-historical-control-boundary"]}
    return {"c1": "unknown", "c2": "unknown", "counterexample": "", "runs": []}


def score(listed, c1, c2):
    if listed == "no" and c1 == c2 == "scope-absent":
        return "absent-in-scope"
    if listed != "yes":
        return "unknown"
    if "refuted" in (c1, c2):
        return "refuted"
    if c1 == c2 == "yes":
        return "positive"
    return "unknown"


def opened_score(event, original, acquired, old, edition_available):
    if event["opened_status"] != "verified":
        assert original["availability"] == "unrestored"
        return "unknown"
    assert event["event_id"] and event["opened_url"]
    assert original["body_raw_sha256"] == event["raw_sha256"]
    assert original["body_lf_sha256"] == event["lf_sha256"]
    if not edition_available or original["availability"] != "available-reviewed":
        return "unknown"
    if original["compared_to_acquired"] == "same-bytes":
        assert original["body_raw_sha256"] == acquired["body_raw_sha256"]
    elif original["compared_to_acquired"] == "lf-only":
        assert original["body_raw_sha256"] != acquired["body_raw_sha256"]
        assert original["body_lf_sha256"] == acquired["body_lf_sha256"]
    elif original["compared_to_acquired"] != "semantic-same":
        # A semantic change requires a new paired judgment for this cell.
        return "unknown"
    fields = ("C1", "C2", "prohibited", "stated_environment", "already_named_method")
    assert all(original[key] == acquired[key] for key in fields)
    return old


def replay():
    seal = json.loads(prior("evidence/first-seal.json"))
    for name, held in seal["input_sha256"].items():
        raw = prior(name)
        actual = hashlib.sha256(raw).hexdigest()
        if name == "frames.csv" and actual != held:
            # The producer sealed the CSV writer's CRLF before Git stored LF.
            assert b"\r" not in raw
            actual = hashlib.sha256(raw.replace(b"\n", b"\r\n")).hexdigest()
        assert actual == held, name
    prior_rows = list(csv.DictReader(io.StringIO(prior("matches.csv").decode())))
    old_cells = index(prior_rows, lambda row: (row["seat_id"], row["cell"]))
    old_requests = index(jsonl(prior("requests.jsonl").decode()), lambda row: row["seat_id"])
    gold = jsonl(prior("gold.jsonl").decode())
    old_gold = index((row for row in gold if row.get("seat_id") in CASES), lambda row: row["seat_id"])
    catalogs = index(jsonl(prior("catalogs.jsonl").decode()), lambda row: row["id"])
    frames = list(csv.DictReader(io.StringIO(prior("frames.csv").decode())))
    inputs = index(csv.DictReader(io.StringIO(here("inputs.csv"))), lambda row: (row["case"], row["edition"]))
    events = index(jsonl(here("events.jsonl")), lambda row: row["case"])
    versions = index(jsonl(here("versions.jsonl")), lambda row: row["case"])
    runs = index(jsonl(here("runs.jsonl")), lambda row: row["id"])
    clauses = index(jsonl(here("fixtures/clauses.jsonl")), lambda row: row["url"])

    rows = []
    for case in CASES:
        event, version = events[case], versions[case]
        acquired = inputs[case, "first-acquired"]
        original = inputs[case, "opened"]
        assert acquired["body_raw_sha256"] == old_requests[case]["original_sha256"]
        original_reporter = old_gold[case].get("reporter_login") or old_gold[case]["author_login"]
        assert version["question"]["actor"] == original_reporter == event["author"]
        if case in AUTHOR_SPELLINGS:
            assert old_gold[case]["author_success_exact_version"] == version["success"]["version"]
            assert AUTHOR_SPELLINGS[case] in old_gold[case]["feature_ids"]
        assert acquired["body_raw_sha256"] == event["first_acquired"]["raw_sha256"]
        for position in POSITIONS:
            previous = old_cells[case, position]
            catalog = catalogs.get(previous["catalog_id"])
            scope = "narrow" if position.startswith("N") else "broad"
            axis = "reference" if position.endswith("R") else "exact"
            expected_version = version[axis]["version"]
            verified_clauses = []
            menu, joined = [], []
            author_join = None
            if catalog:
                assert catalog["scan_complete"]
                assert catalog["scope"] == scope and catalog["version"] == expected_version
                assert catalog["commit"] == previous["commit"]
                by_file = index(catalog["files"], lambda row: row["path"])
                for url in previous["evidence"].split(" | "):
                    if "github.com/" in url:
                        clause = clauses[url]
                        assert clause["commit"] == catalog["commit"]
                        assert f"{case}-{position}" in clause["cells"]
                        assert by_file[clause["path"]]["sha256"] == clause["file_sha256"]
                        assert len(clause["clause_sha256"]) == 64
                        verified_clauses.append(clause["id"])
                features = index(catalog["features"], lambda row: row["id"])
                joined = [match_feature(features, name) for name in FEATURES[case]]
                menu = [name for name in previous["related_menu_ids"].split("|") if name]
                assert all(find_feature(features, name) for name in menu)
                if case in AUTHOR_SPELLINGS:
                    author_join = match_feature(features, AUTHOR_SPELLINGS[case])
                listed = "yes" if all(item["canonical"] for item in joined) else "no"
                observation = observations(case, position, runs)
            else:
                assert expected_version is None, f"Add same-rules catalog for {case} {axis}"
                listed = "unknown"
                observation = {"c1": "unknown", "c2": "unknown", "counterexample": "", "runs": []}

            acquired_judge = score(listed, observation["c1"], observation["c2"])
            original_judge = opened_score(event, original, acquired, acquired_judge, catalog is not None)
            missing = []
            if event["opened_status"] != "verified":
                missing.append(f"{case}의 ID 일치 opened 본문 및 가린 요구 판독")
            if not catalog:
                missing.append(CONSUMER_MISSING[case])
            rows.append({
                "case": case, "cell": position, "scope": scope, "consumer_axis": axis,
                "catalog_id": previous["catalog_id"], "package_version": expected_version or "",
                "catalog_commit": previous["commit"], "acquired_input_state": acquired["availability"],
                "opened_input_state": original["availability"],
                "features": "|".join(FEATURES[case]), "menu_ids": "|".join(menu),
                "feature_join": json.dumps(joined, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "author_feature_join": json.dumps(author_join, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                "clause_ids": "|".join(verified_clauses), "listed_acquired": listed,
                "listed_opened": listed if original_judge != "unknown" else "unknown",
                "c1_acquired": observation["c1"], "c2_acquired": observation["c2"],
                "joint_acquired": "yes" if acquired_judge == "positive" else "unknown" if acquired_judge == "unknown" else "no",
                "refuted_acquired": "yes" if acquired_judge == "refuted" else "unknown" if acquired_judge == "unknown" else "no",
                "joint_opened": "yes" if original_judge == "positive" else "unknown" if original_judge == "unknown" else "no",
                "refuted_opened": "yes" if original_judge == "refuted" else "unknown" if original_judge == "unknown" else "no",
                "old_acquired": previous["acquired_status"], "recalculated_acquired": acquired_judge,
                "old_strict": previous["status"], "recalculated_opened": original_judge,
                "scope_outside": previous["scope_outside"], "counterexample": observation["counterexample"],
                "run_ids": "|".join(observation["runs"]),
                "scope_delta_basis": CHANGED_SCOPE[case], "minimal_missing": " | ".join(missing),
            })

    assert len(index(rows, lambda row: (row["case"], row["cell"]))) == 16
    pairs = compare_pairs(rows)
    return rows, pairs, summarize(rows, pairs, events, runs, frames, old_cells)


def compare_pairs(rows):
    by_key = index(rows, lambda row: (row["case"], row["cell"]))
    pair_rows = []

    def add(case, axis, layer, left, right, first, second, reason):
        comparable = first in KNOWN and second in KNOWN
        pair_rows.append({
            "case": case, "axis": axis, "input_layer": layer, "from": left, "to": right,
            "from_status": first, "to_status": second,
            "comparable": str(comparable).lower(),
            "verdict_changed": str(first != second).lower() if comparable else "unknown",
            "positive_recovery": str(first != "positive" and second == "positive").lower() if comparable else "unknown",
            "basis": reason,
        })

    for case in CASES:
        for pos in POSITIONS:
            row = by_key[case, pos]
            add(case, "input", "paired", pos + "/first-acquired", pos + "/opened",
                row["recalculated_acquired"], row["recalculated_opened"], row["minimal_missing"])
        plans = (("scope", "NR", "BR"), ("scope", "NE", "BE"),
                 ("consumer", "NR", "NE"), ("consumer", "BR", "BE"))
        for axis, left, right in plans:
            a, b = by_key[case, left], by_key[case, right]
            for layer in ("acquired", "opened"):
                score_col = "recalculated_" + layer
                reason = CHANGED_SCOPE[case] if axis == "scope" and b[score_col] in KNOWN else b["minimal_missing"]
                if axis == "consumer" and a[score_col] in KNOWN and b[score_col] in KNOWN:
                    reason = f"{a['package_version']} → {b['package_version']}; 같은 범위와 최초 확보 입력"
                add(case, axis, layer, left, right, a[score_col], b[score_col], reason)

    return pair_rows


def summarize(cells, pairs, events, runs, frames, old_cells):
    old_plans = Counter(row["stratum"] for row in frames if row["issue_number"])
    cells_by_first = Counter(row["recalculated_acquired"] for row in cells)
    cells_by_opened = Counter(row["recalculated_opened"] for row in cells)
    pair_summary = {}
    for axis in ("input", "scope", "consumer"):
        for layer in ("paired", "acquired", "opened"):
            selected = [row for row in pairs if row["axis"] == axis and row["input_layer"] == layer]
            if not selected:
                continue
            by_axis = {
                "planned": len(selected),
                "comparable": sum(row["comparable"] == "true" for row in selected),
                "changes": sum(row["verdict_changed"] == "true" for row in selected),
                "recoveries": sum(row["positive_recovery"] == "true" for row in selected),
            }
            for left, right in sorted({(r["from"], r["to"]) for r in selected if axis != "input"}):
                subset = [r for r in selected if (r["from"], r["to"]) == (left, right)]
                by_axis[f"{left}-{right}"] = {
                    "scoped_cases": len(subset),
                    "comparable": sum(r["comparable"] == "true" for r in subset),
                    "changes": sum(r["verdict_changed"] == "true" for r in subset),
                    "recoveries": sum(r["positive_recovery"] == "true" for r in subset),
                }
            pair_summary[f"{axis}/{layer}"] = by_axis
    fresh = [row for row in runs.values() if row["record_source"] == "new"]
    prior_ref = [row for row in runs.values() if row["record_source"] == "inherited"]
    raw_verified = sum(events[case]["opened_status"] == "verified" for case in CASES)
    return {
        "denominators": {
            "planned_cases": len(CASES), "planned_cells": len(cells), "original_frame": dict(old_plans),
            "original_strict_cells": len(old_cells), "edit_control_excluded": "EDIT1060",
            "opened_bodies": raw_verified,
            "acquired_same_raw_latest": sum(events[case]["latest"]["raw_sha256"] ==
                                          events[case]["first_acquired"]["raw_sha256"] for case in CASES),
            "suspect_opened_promotions": sum(row["recalculated_opened"] != "unknown" for row in cells
                                            if events[row["case"]]["opened_status"] != "verified"),
        },
        "cells": {"acquired": dict(cells_by_first), "opened": dict(cells_by_opened),
                  "acquired_changes_from_080": sum(row["recalculated_acquired"] != row["old_acquired"] for row in cells),
                  "comparable_acquired": sum(cells_by_first[k] for k in KNOWN),
                  "comparable_opened": sum(cells_by_opened[k] for k in KNOWN)},
        "pairs": pair_summary,
        "runs": {
            "record_types": dict(Counter(row["record_source"] for row in runs.values())),
            "new_by_role": dict(Counter(row["role"] for row in fresh)),
            "new_expectations_met": sum(row["expectation_matches"] for row in fresh),
            "reference_observations_this_matrix": len(prior_ref) + sum(row["role"] == "new-reference" for row in fresh),
            "reused_080_without_execution": len(prior_ref),
            "exact_author_success_with_versions": sum(row["role"] == "author-followup" and row["version"] is not None
                                                      and row["python"] is not None and row["observed"] is not None for row in runs.values()),
            "author_success_reports_without_confirmed_versions": sum(row["role"] == "author-followup" and not row["version"]
                                                                      for row in runs.values()),
        },
    }


def csv_text(rows):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--upstream", type=Path, help="directory with click-git and attrs-git repositories")
    args = parser.parse_args()

    cells, pairs, metrics = replay()
    if args.upstream:
        for clause in jsonl(here("fixtures/clauses.jsonl")):
            repo = args.upstream / f"{clause['repo'].split('/')[-1]}-git"
            raw = subprocess.check_output(
                ["git", "-C", str(repo), "show", f"{clause['commit']}:{clause['path']}"])
            lines = raw.splitlines(keepends=True)
            text = b"".join(lines[clause["line_start"] - 1:clause["line_end"]])
            assert hashlib.sha256(raw).hexdigest() == clause["file_sha256"], clause["url"]
            assert hashlib.sha256(text).hexdigest() == clause["clause_sha256"], clause["url"]
    bundle = {
        "cells.csv": csv_text(cells),
        "pairs.csv": csv_text(pairs),
        "metrics.json": json.dumps(metrics, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    }
    for file, value in bundle.items():
        path = args.out / file
        if args.check:
            assert path.read_bytes() == value.encode(), f"{file} differs from replay"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value.encode())
    print(f"Replayed {len(cells)} cells and {len(pairs)} pairs against {PRIOR_SHA}")


if __name__ == "__main__":
    main()
