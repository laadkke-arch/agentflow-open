"""Re-read committed bytes, verify predictions and compare a clean replay."""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from fixturegen import CELLS, OWNED, digest, fixtures, read_lines, utc
from oracle import csv_middle, image_conditions, image_expectation, png_info, source_table, table_final, zip_members
from report import aggregate, compare_all, cost, run_hashes, tables_one, tables_three, tables_two

GIT_ROOT = OWNED.parents[3]
PREFIX = OWNED.relative_to(GIT_ROOT).as_posix()


def git(*args, required=True):
    result = subprocess.run(["git", *args], cwd=GIT_ROOT, capture_output=True, timeout=10)
    if required:
        result.check_returncode()
    return result


def version_json(name):
    return json.loads((OWNED / name).read_text(encoding="utf-8"))


class Checks:
    def __init__(self):
        self.tests = Counter()

    def need(self, group, truth, description):
        if not truth:
            raise AssertionError(f"{group}: {description}")
        self.tests[group] += 1


def read_csv(path, width, tests):
    name = path.relative_to(OWNED).as_posix()
    with path.open(newline="", encoding="utf-8") as file:
        header, *rows = list(csv.reader(file, strict=True))
    tests.need("csv_shape", len(set(header)) == len(header) == width, name)
    for row in rows:
        tests.need("csv_shape", len(row) == width, name + " rectangular")
    return [dict(zip(header, row)) for row in rows]


def key_check(tests, rows, columns, size, name):
    keys = {tuple(r[k] for k in columns) for r in rows}
    tests.need("unique_keys", len(keys) == len(rows) == size, name)
    return keys


def blob_map(rows, tests):
    result = {}
    for row in rows:
        content = base64.b64decode(row["base64"], validate=True)
        key = row["sha256"]
        tests.need("artifact_digest", key not in result and len(content) == row["bytes"] and digest(content) == key, key)
        result[key] = content
    return result


def artifact(proof, blobs, tests):
    data = blobs[proof["sha256"]]
    tests.need("artifact_reference", len(data) == proof["bytes"], proof)
    return data


def snapshot_read(snapshot, path, blobs, tests):
    if path in snapshot and "sha256" in snapshot[path]:
        return artifact(snapshot[path], blobs, tests)
    return None


def assert_record_structure(run, blobs, tests):
    for event in run["events"]:
        tests.need("event_receipt", event["process_started"] and bool(event["argv"]) and
                   event["start_utc"] <= event["end_utc"], run["run"])
        for attr in ("stdin", "stdout", "stderr"):
            if event[attr] is not None:
                body = artifact(event[attr], blobs, tests)
                if attr == "stderr":
                    tests.need("event_receipt", event["stderr_text"] == body.decode("utf-8", "replace"), run["run"])
        gate = event.get("gate", {})
        if "pipe_payload" in gate:
            artifact(gate["pipe_payload"], blobs, tests)
    for snapshot in run["snapshots"].values():
        for path, proof in snapshot.items():
            tests.need("snapshot_path", not path.startswith("/") and ".." not in Path(path).parts, path)
            if "sha256" in proof:
                artifact(proof, blobs, tests)


def verify_oracle(run, blobs, registry, tests):
    rid = run["run"]
    fixture = registry[run["fixture"]]
    before, middle, after = (run["snapshots"][key] for key in ("before_front", "after_front", "after_back"))
    with TemporaryDirectory(prefix="af078-verify-") as area:
        root = Path(area)
        if run["domain"] == "T":
            db = root / "source.db"
            db.write_bytes(snapshot_read(before, "source.db", blobs, tests))
            actual_mid = snapshot_read(middle, "exchange.csv", blobs, tests)
            current = snapshot_read(after, "final.jsonl", blobs, tests)
            tests.need("independent_oracle", source_table(db, fixture) == run["expected"], rid+" DB")
            tests.need("independent_oracle", csv_middle(actual_mid, fixture) == run["middle"], rid+" CSV")
            tests.need("independent_oracle", table_final(current, fixture) == run["final"], rid+" JSON")
            input_paths = ["source.db"]
        else:
            input_paths = [image["path"] for image in fixture["images"]]
            for path in input_paths:
                source = root / path
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(snapshot_read(before, "source/" + path, blobs, tests))
            expected = image_expectation(root, fixture)
            tests.need("independent_oracle", expected == run["expected"], rid+" input PNG")
            input_paths = ["source/" + name for name in input_paths]
            for member in run["middle"]["members"]:
                payload = snapshot_read(middle, "stage/" + member["name"], blobs, tests)
                tests.need("independent_oracle", png_info(payload) == member["image"], rid+" saved PNG")
            tests.need("independent_oracle", image_conditions(run["middle"]["members"], expected) ==
                       run["middle"]["conditions"], rid+" stage offer")
            current = snapshot_read(after, "artifact.zip", blobs, tests)
            recovered = zip_members(current, extract=sorted(expected))
            recovered["conditions"] = image_conditions(recovered["members"], expected, recovered["accessed_by_name"])
            for k, v in recovered.items():
                tests.need("independent_oracle", run["final"][k] == v, f"{rid} archive {k}")
            unzip = [e for e in run["events"] if e["stage"] == "oracle_unzip"]
            if current is not None:
                tests.need("independent_oracle", len(unzip) == 1 and unzip[0]["exit"] == 0, rid+" UnZip")
                names = artifact(unzip[0]["stdout"], blobs, tests).decode("utf-8", "backslashreplace").splitlines()
                tests.need("independent_oracle", names == run["final"]["unzip_cli"]["names"], rid+" UnZip names")
                tests.need("independent_oracle", names == [m["name"] for m in recovered["members"]], rid+" readers agree")
    for name in input_paths:
        tests.need("original_integrity", before[name]["sha256"] == after[name]["sha256"], rid)
    tests.need("original_integrity", run["originals_unchanged"], rid)
    conjunction = run["phase_status"] == "complete" and all(run["final"]["conditions"].values())
    tests.need("score_integrity", run["adoption"] == conjunction, rid)
    for condition, passed in run["final"]["conditions"].items():
        if not passed:
            step = "front" if run["middle"]["conditions"].get(condition) is False else "back/publication"
            tests.need("score_integrity", run["first_loss"][condition] == step, rid+" "+condition)
        else:
            tests.need("score_integrity", condition not in run["first_loss"], rid+" "+condition)


def compare_attempts(runs, tests):
    by_group = defaultdict(list)
    for r in runs:
        by_group[(r["cell"], r["scenario"])].append(r)
    equal_content = 0
    for (cell, scenario), pair in by_group.items():
        tests.need("matrix", len(pair) == 2, (cell, scenario))
        a, b = sorted(pair, key=lambda x: str(x["attempt"]))
        if scenario == "retry":
            if a["attempt"] == "resume":
                a, b = b, a
            tests.need("retry", [a["attempt"], b["attempt"]] == ["stop", "resume"] and a["fixture"] == b["fixture"], cell)
            tests.need("retry", run_hashes(a)[0:2] == run_hashes(b)[0:2], cell + " identical source and staging")
            pub = "final.jsonl" if cell.startswith("T") else "artifact.zip"
            expected_old = a["snapshots"]["before_front"][pub]["sha256"]
            tests.need("retry", a["snapshots"]["after_back"][pub]["sha256"] == expected_old, cell + " old safe")
            tests.need("retry", b["snapshots"]["before_front"][pub]["sha256"] == expected_old, cell + " old in next input")
            back = next(e for e in a["events"] if e["stage"] == "back")
            retry_back = next(e for e in b["events"] if e["stage"] == "back")
            tests.need("retry", back["cwd"] == retry_back["cwd"], cell + " stop and resume share operation directory")
            tests.need("retry", back["gate"]["kind"] == "actual SIGTERM", cell + " actual stop")
            tests.need("retry", back["exit"] == (-15 if cell.startswith("T") else 9), cell + " native stop exit")
            if cell.startswith("T"):
                tests.need("retry", "final.part" in a["snapshots"]["after_back"] and
                           "final.part" not in b["snapshots"]["after_back"], cell + " table partial lifecycle")
            else:
                tests.need("retry", "pipe" in back["gate"]["wchan"], cell + " verified Zip gate")
                tests.need("retry", not any(k.startswith("zip-temp/") for k in a["snapshots"]["after_back"]), cell + " early temp not started")
            continue
        tests.need("matrix", [a["attempt"], b["attempt"]] == [1, 2], cell + scenario)
        cwd_a, cwd_b = [next(e for e in r["events"] if e["stage"] == "front")["cwd"] for r in (a, b)]
        tests.need("matrix", cwd_a != cwd_b, cell + scenario + " clean independent roots")
        tests.need("matrix", a["final"]["conditions"] == b["final"]["conditions"], cell + scenario + " semantic repeat")
        tests.need("matrix", run_hashes(a)[:2] == run_hashes(b)[:2], cell + scenario + " input artifacts")
        if run_hashes(a)[2] == run_hashes(b)[2]:
            equal_content += 1
    return equal_content


def verify_git_freezes(tests):
    evidence = {
        "seed": "evidence/seed-seal.json", "correction": "evidence/oracle-correction-seal.json",
        "solo": "evidence/solo.jsonl", "ab": "predictions.csv", "main": "runs.jsonl",
        "c": "evidence/c-heldout-predictions.csv", "reveal": "evidence/seed-reveal.json",
    }
    heads = {}
    for label, name in evidence.items():
        heads[label] = git("log", "--format=%H", "--diff-filter=A", "--", f"{PREFIX}/{name}").stdout.decode().strip()
        tests.need("git_seal", len(heads[label]) == 40, label)
    chain = ("seed", "correction", "ab", "main", "c", "reveal")
    for left, right in zip(chain, chain[1:]):
        tests.need("git_seal", heads[left] != heads[right] and
                   git("merge-base", "--is-ancestor", heads[left], heads[right], required=False).returncode == 0,
                   (left, right))
    for label in ("ab", "c"):
        file = evidence[label]
        actual = git("show", f"{heads[label]}:{PREFIX}/{file}").stdout
        tests.need("git_seal", actual == (OWNED / file).read_bytes(), label + " exact committed predictions")
        tests.need("git_seal", git("cat-file", "-e", f"{heads[label]}:{PREFIX}/{evidence['reveal']}", required=False).returncode != 0,
                   label + " not exposed")
    tests.need("git_seal", git("cat-file", "-e", f"{heads['ab']}:{PREFIX}/runs.jsonl", required=False).returncode != 0, "AB before composition")
    main = git("show", f"{heads['main']}:{PREFIX}/runs.jsonl").stdout
    at_c = git("show", f"{heads['c']}:{PREFIX}/runs.jsonl").stdout
    tests.need("git_seal", main == at_c and all(json.loads(l)["scenario"] != "edge" for l in main.splitlines()), "C has only primary volume")
    c_seal, ab_seal = (version_json("evidence/" + name) for name in ("c-heldout-freeze.json", "ab-freeze.json"))
    tests.need("git_seal", digest(main) == c_seal["inputs"]["normal_and_retry_run_sha256"], "C declared primary input")
    tests.need("git_seal", digest((OWNED / "evidence/solo.jsonl").read_bytes()) == ab_seal["inputs"]["solo_sha256"], "A/B declared solo input")
    tests.need("git_seal", digest((OWNED / evidence["ab"]).read_bytes()) == ab_seal["predictions_sha256"], "AB declared hash")
    tests.need("git_seal", digest((OWNED / evidence["c"]).read_bytes()) == c_seal["predictions_sha256"], "C declared hash")
    return heads


def verify_replay(tests, source, saved, diagnostics):
    replay = read_lines(source / "runs.jsonl")
    key_check(tests, replay, ("run",), 48, "replayed primary/held outputs")
    different_codes = Counter()
    for row in replay:
        frozen = saved[row["run"]]
        for field in ("adoption", "first_loss", "expected", "phase_status"):
            tests.need("replay", row[field] == frozen[field], row["run"] + " " + field)
        tests.need("replay", row["final"]["conditions"] == frozen["final"]["conditions"], row["run"] + " required outcomes")
        tests.need("replay", run_hashes(row) == run_hashes(frozen), row["run"] + " input/interchange/output bytes")
        current, old = [[(n["stage"], n["exit"]) for n in p["events"]] for p in (row, frozen)]
        if current != old:
            different_codes[row["run"]] += 1
    tests.need("replay", not different_codes, different_codes)
    rerun_diag = read_lines(source / "evidence/diagnostics.jsonl")
    key_check(tests, rerun_diag, ("run",), 18, "replayed diagnostics")
    prior_diag = {r["run"]:r for r in diagnostics}
    for row in rerun_diag:
        tests.need("replay", row["final"]["conditions"] == prior_diag[row["run"]]["final"]["conditions"], row["run"])
        tests.need("replay", [e["exit"] for e in row["events"]] == [e["exit"] for e in prior_diag[row["run"]]["events"]], row["run"])
    rerun_solo = read_lines(source / "evidence/solo.jsonl")
    tests.need("replay", len(rerun_solo) == 8 and all(row["status"] == 0 for row in rerun_solo), "solo run status")
    versions = json.loads((source / "evidence/runtime-versions.json").read_text(encoding="utf-8"))
    originals = version_json("evidence/runtime-versions.json")
    tests.need("replay", versions == originals, "runtime probes")
    return {"core_rows": len(replay), "core_processes": sum(len(r["events"]) for r in replay),
            "diagnostic_rows": len(rerun_diag), "diagnostic_processes": sum(len(r["events"]) for r in rerun_diag),
            "solo_processes": len(rerun_solo), "version_probes": len(versions)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-dir", type=Path)
    args = parser.parse_args()
    tests = Checks()
    registry = {r["id"]: r for r in read_lines(OWNED / "fixtures.jsonl")}
    tests.need("matrix", set(registry) == {"t-normal", "i-normal", "t-edge", "i-edge", "t-old", "i-old", "t-nul", "t-empty"}, "eight authored fixtures")
    original_seal = version_json("evidence/seed-seal.json")
    correction = version_json("evidence/oracle-correction-seal.json")
    tests.need("seed", correction["initial_seal_sha256"] == digest((OWNED / "evidence/seed-seal.json").read_bytes()), "original seed commitment unchanged")
    for name, key in (("fixturegen.py", "generator_sha256"), ("oracle.py", "oracle_sha256")):
        tests.need("seed", digest((OWNED / "tools" / name).read_bytes()) == correction[key], name)
    seeds = version_json("evidence/seed-reveal.json")["hex"]
    for domain, encoded in seeds.items():
        tests.need("seed", len(encoded) == 32 and digest(encoded.encode("ascii")) == original_seal["commitments"][domain], domain)
    tests.need("seed", all(registry[f["id"]] == f for f in fixtures("edge", {k:int(v,16) for k,v in seeds.items()})), "seeded fixtures")
    heads = verify_git_freezes(tests)
    sources = read_lines(OWNED / "sources.jsonl")
    orig = [r for r in sources if r["counted"]]
    tests.need("source_minimum", len({r["lineage"] for r in orig}) == len(orig) >= 20, "unique sources")
    domain_counts = Counter(r["domain"] for r in orig)
    incidents = sum(r["counted_original_event"] for r in orig)
    tests.need("source_minimum", min(domain_counts[d] for d in "TI") >= 8 and incidents >= 4, (domain_counts, incidents))
    for src in sources:
        tests.need("source_minimum", all(src[k] for k in ("original_url", "accessed_url", "author", "version", "direct_read_utc", "section", "observation", "limits", "questions", "minimum_reason")), src["id"])
    search_log = read_lines(OWNED / "search-log.jsonl")
    tests.need("source_minimum", len(search_log) >= 1 and all(r["result"] and r["next_or_exclusion"] for r in search_log), "failed access")
    ab = read_csv(OWNED / "predictions.csv", 8, tests)
    cp = read_csv(OWNED / "evidence/c-heldout-predictions.csv", 8, tests)
    comparisons = read_csv(OWNED / "comparisons.csv", 12, tests)
    summary = read_csv(OWNED / "evidence/counts.csv", 12, tests)
    costs = read_csv(OWNED / "evidence/costs.csv", 13, tests)
    key_check(tests, read_csv(OWNED / "contracts.csv", 10, tests), ("domain", "stage"), 4, "contracts")
    for name, group, keys, n in (
        ("A/B", ab, ("view", "cell", "scenario", "condition"), 408),
        ("C", cp, ("view", "cell", "scenario", "condition"), 68),
        ("comparisons", comparisons, ("view", "cell", "scenario", "condition"), 612),
        ("summary", summary, ("view", "layer", "domain", "condition"), 126),
        ("cost", costs, ("run",), 48),
    ):
        key_check(tests, group, keys, n, name)
    runs = read_lines(OWNED / "runs.jsonl")
    solo = read_lines(OWNED / "evidence/solo.jsonl")
    diagnostics = read_lines(OWNED / "evidence/diagnostics.jsonl")
    key_check(tests, runs, ("run",), 48, "original run ledger")
    key_check(tests, solo, ("run",), 8, "standalone experiment")
    key_check(tests, diagnostics, ("run",), 18, "diagnostics")
    for domain, labels in CELLS.items():
        shape = {(r["cell"], r["scenario"]) for r in runs if r["domain"] == domain}
        tests.need("matrix", shape == {(cell,s) for cell in labels for s in ("normal", "edge", "retry")}, domain)
    blobs = blob_map(read_lines(OWNED / "evidence/artifacts.jsonl"), tests)
    for row in runs + solo + diagnostics:
        assert_record_structure(row, blobs, tests)
    for row in runs:
        verify_oracle(row, blobs, registry, tests)
    repeats = compare_attempts(runs, tests)
    tests.need("repeat", repeats == 16, "all clean pairs produce equal bytes or shared absence")
    compare_work = list(compare_all(runs))
    tests.need("score_integrity", compare_work == comparisons, "all joined comparison rows recompute")
    cost_work = [cost(r) for r in runs]
    tests.need("cost", [{k:"" if v is None else str(v) for k,v in row.items()} for row in cost_work] == costs, "cost lines recompute")
    agg_work = aggregate(compare_work)
    tests.need("score_integrity", [{k:str(v) for k,v in row.items()} for row in agg_work] == summary, "all numerator/denominator groups recompute")
    for row in agg_work:
        n = row["true_support"] + row["true_reject"] + row["false_accept"] + row["false_reject"] + row["hold"]
        tests.need("score_integrity", n == row["eligible"] and n + row["ineligible"] == row["total"], row)
    expected_markdown = "# AF-RES-078 조합 검증 결과\n\n" + tables_one() + tables_two(runs) + tables_three(agg_work, cost_work, solo)
    rendered = (OWNED / "RESULT.md").read_text(encoding="utf-8")
    tests.need("markdown", rendered.startswith(expected_markdown), "three projected tables")
    tests.need("markdown", rendered.split("## 불일치와 약점 세 가지", 1)[-1].count("\n| ") == 5, "exactly three weakness rows")
    diag = {r["scenario"]:r for r in diagnostics}
    for name in ("typed_adapter","fresh_adapter","sync_adapter","zero_framed"):
        tests.need("counterexamples", diag[name]["adoption"], name + " successful candidate")
    for name in ("reader_version312","raw_orientation_tag","nul_text","zero_default","zero_failed_query"):
        tests.need("counterexamples", diag[name]["adoption"] is False, name + " negative candidate")
    tests.need("counterexamples", diag["native_write_sigterm"]["final"]["conditions"] ==
               {"old_kept":True,"temporary_removed":True}, "native SIGTERM cleans temp")
    tests.need("counterexamples", diag["native_write_sigkill"]["final"]["conditions"] ==
               {"old_kept":True,"temporary_removed":False}, "native SIGKILL retains temp")
    tests.need("counterexamples", diag["zero_framed"]["bytes"]["final"] == 0 and
               diag["zero_default"]["bytes"]["final"] is None and diag["zero_failed_query"]["bytes"]["final"] is None,
               "genuine empty and absent")
    tests.need("counterexamples", diag["zip_empty"]["final"]["conditions"] ==
               {"empty_created_by_zip":False,"legal_empty_zip":True}, "valid empty ZIP")
    run_index = {r["run"]: r for r in runs}
    tests.need("counterexamples", run_hashes(diag["same_meaning_different_dates"])[2] != run_hashes(run_index["I00.normal.1"])[2]
               and diag["same_meaning_different_dates"]["final"]["conditions"] == run_index["I00.normal.1"]["final"]["conditions"],
               "different ZIP headers, same requested meaning")
    for first, last, stage in (("T00", "T01", 1), ("T10", "T11", 2), ("I10", "I11", 2)):
        for scenario in ("normal", "edge"):
            a, b = [run_index[f"{label}.{scenario}.1"] for label in (first, last)]
            tests.need("paired_setting", run_hashes(a)[stage] == run_hashes(b)[stage], first + last + scenario)
    old_run, next_run = (run_index[f"I00.retry.{step}"] for step in ("stop", "resume"))
    old_files, next_files = [{m["name"]: m["sha256"] for m in row["final"]["members"]} for row in (old_run, next_run)]
    tests.need("retry", tuple(sorted(next_files)) == ("a/photo.png", "b/photo.png", "old/previous.png") and
               old_files["a/photo.png"] != next_files["a/photo.png"] and
               old_files["old/previous.png"] == next_files["old/previous.png"], "native add behavior")
    for d in "TI":
        tests.need("matrix", sum(r["adoption"] for r in runs if r["domain"] == d) == (5 if d == "T" else 4), d)
    replay = verify_replay(tests, args.replay_dir, run_index, diagnostics) if args.replay_dir else None
    result = {
        "actor": "AF-RES-078 작업자 / codex-cloud", "utc": utc(), "status": "pass",
        "checked_commit": git("rev-parse", "HEAD").stdout.decode().strip(),
        "checks": dict(tests.tests), "assertions_passed": sum(tests.tests.values()),
        "sources": {"whole_ledger": len(sources), "distinct_credited": len(orig), "domains": dict(domain_counts), "events": incidents},
        "scope": {"attempts": len(runs), "cell_scenarios": 24, "comparison_rows": len(comparisons),
                  "clean_pair_equivalent": repeats, "study_processes": sum(c["processes"] for c in cost_work)},
        "commit_order": heads, "replay": replay,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
