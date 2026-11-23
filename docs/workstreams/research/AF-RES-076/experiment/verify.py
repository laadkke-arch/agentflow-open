"""Verify the solved experiment's keys, source bindings, budgets and both replays."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from analyze import make_slots, metric_rows, read_csv, render
from judge import run_fixtures
from search import ARMS, MODES, PACKET, read_jsonl, sha, words

ARTIFACTS = {
    "ranks.csv": "ranks.csv", "fetches.jsonl": "fetches.jsonl", "route-costs.csv": "evidence/route-costs.csv",
    "costs.csv": "costs.csv", "slots.csv": "slots.csv", "metrics.json": "evidence/metrics.json",
    "lexical-explanations.json": "evidence/lexical-explanations.json",
}


def keyed(rows, key):
    result = {key(row): row for row in rows}
    assert len(result) == len(rows), "Duplicate key"
    return result


def file_digest(path):
    return sha(path.read_bytes())


def compare_replays(root, dirs, expected_tables):
    results = []
    for directory in dirs:
        assert (directory / "tables.md").read_text() == expected_tables, directory
        files = {}
        for replay, original in ARTIFACTS.items():
            left, right = (directory / replay).read_bytes(), (root / original).read_bytes()
            assert left == right, (directory, replay, original)
            files[replay] = {"sha256": sha(left), "bytes": len(left)}
        results.append({"run": directory.parent.name + "/" + directory.name, "equal_outputs": files,
                        "tables_md_sha256": file_digest(directory / "tables.md")})
    assert len(results) == 2 and results[0]["equal_outputs"] == results[1]["equal_outputs"]
    return results


def check(root, replay_dirs):
    corpus = keyed(read_jsonl(root / "corpus.jsonl"), lambda d: d["candidate_id"])
    requests = keyed(read_jsonl(root / "requests.jsonl"), lambda d: d["id"])
    frames = [r for r in read_csv(root / "frames.csv") if r["status"] == "selected"]
    assert set(corpus) == {r["candidate_id"] for r in frames}
    assert Counter(k[0] for k in corpus) == {"P": 8, "D": 8, "X": 4}
    assert Counter((r["stratum"], r["domain"]) for r in requests.values()) == {
        ("natural", "Pillow"): 3, ("natural", "DuckDB"): 3,
        ("calibration", "Pillow"): 3, ("calibration", "DuckDB"): 3,
    }
    screen = read_jsonl(root / "evidence/natural-screen.jsonl")
    assert len(screen) == 13 and sum(bool(r["request_id"]) for r in screen) == 6
    for group in "PD":
        frame = [r for r in screen if r["frame"] == group]
        assert [r["ordinal"] for r in frame] == list(range(1, len(frame) + 1))
        assert [(r["date"], r["number"]) for r in frame] == sorted((r["date"], r["number"]) for r in frame)

    sources = keyed(read_jsonl(root / "sources.jsonl"), lambda r: r["source_id"])
    countable = [r for r in sources.values() if r["minimum_count"]]
    assert len({r["work_id"] for r in countable}) == len(countable) >= 22
    assert all(r["access"] == "direct" and r["original_url"] and r["arrival_url"] and r["section"] for r in countable)
    assert [r for r in sources.values() if r["access"] == "failed"]
    for request in requests.values():
        assert request["source_id"] in sources and request["source_url"].startswith("https://")

    qrels = read_csv(root / "qrels.csv")
    keyed(qrels, lambda r: r["pair_id"])
    pairs = keyed(qrels, lambda r: (r["request_id"], r["candidate_id"]))
    assert set(pairs) == {(r, c) for r in requests for c in corpus}
    for (rid, cid), row in pairs.items():
        request, document = requests[rid], corpus[cid]
        assert row["source_id"] == document["source_id"] and row["source_id"] in sources
        assert row["candidate_edition"] == document["edition"]
        assert row["c1_expected"] == request["c1"] and row["c2_expected"] == request["c2"]
        assert row["environment_expected"] == request["environment"]
        assert all(anchor.startswith(document["url"] + "#L") for anchor in row["original_anchors"].split())
        assert all(row[field] for field in ("donor", "recipient", "operation", "break_condition")) == (
            row["judgment"] == "transfer")
        assert row["pair_id"] == f"Q-{rid}-{cid}"
        if row["judgment"] == "direct":
            assert [row[k] for k in ("c1_verdict", "c2_verdict", "environment_verdict")] == ["yes"] * 3

    cards = keyed(read_jsonl(root / "cards.jsonl"), lambda r: r["candidate_id"])
    assert set(cards) == set(corpus)
    assert all(words(r["name"] + " " + r[arm]) <= 40 for r in cards.values() for arm in "se")
    build = keyed(read_jsonl(root / "evidence/build-fetches.jsonl"), lambda r: r["candidate_id"])
    assert set(build) == set(corpus)
    for cid, rec in build.items():
        assert (rec["status"], rec["http_status"], rec["sha256"], rec["bytes"]) == (
            "ok", 200, corpus[cid]["document_sha256"], corpus[cid]["raw_bytes"])
    for seal_name, item in [("card-seal", "sha256"), ("qrel-seal", "sha256"), ("rank-seal", "outputs_sha256")]:
        sealed = json.loads((root / "evidence" / (seal_name + ".json")).read_text())[item]
        for name, digest in sealed.items():
            assert digest == file_digest(root / name), (seal_name, name)
    rank_seal = json.loads((root / "evidence/rank-seal.json").read_text())
    assert rank_seal["ranker_read_qrels_before_seal"] is False
    assert set(rank_seal["packet_files"]) == {"input/" + name for name in PACKET}
    for name, digest in rank_seal["packet_files"].items():
        assert digest == file_digest(root / "experiment/inputs" / Path(name).name)
    assert rank_seal["isolated_script_sha256"] == file_digest(root / "experiment/search.py")

    fetched = read_jsonl(root / "fetches.jsonl")
    keyed(fetched, lambda r: r["fetch_id"])
    traces = defaultdict(list)
    for event in fetched:
        traces[(event["request"], event["arm"], event["cache"])].append(event)
        document = corpus[event["candidate"]]
        view = event["view"]
        if view:
            assert view["start"] == min(view["source_lines"]) and view["end"] == max(view["source_lines"])
        if event["status"] == "ok":
            assert event["body_sha256"] == document["document_sha256"]
            assert event["kind"] == "original"
        if event["storage"] == "cache":
            assert event["received_body_b"] == 0
        if event["storage"] == "http" and event["status"] == "ok":
            assert event["http_status"] == 200
            assert event["received_body_b"] == document["raw_bytes"]
        text = "\n".join([event["candidate_url"], event["edition"]] +
                         ([event["card"]] if event["card"] else []) +
                         ([view["text"]] if view else []))
        assert event["display_b"] == len(text.encode())
        assert event["display_words"] == words(text)
        assert event["display_sha256"] == sha(text.encode())
        assert event["received_body_b"] <= 1024 * 1024

    ranks = read_csv(root / "ranks.csv")
    keyed(ranks, lambda r: r["rank_id"])
    by_route = defaultdict(list)
    for r in ranks:
        by_route[(r["request_id"], r["arm"], r["cache"])].append(r)
    keys = {(r, a, mode) for r in requests for a in ARMS for mode in MODES}
    assert set(traces) == set(by_route) == keys
    cost_rows = keyed([r for r in read_csv(root / "costs.csv") if r["phase"] == "request"],
                      lambda r: (r["request_id"], r["arm"], r["cache"]))
    assert set(cost_rows) == keys
    max_bytes, max_words = 0, 0
    for key, r in by_route.items():
        assert set(corpus) == {row["candidate_id"] for row in r}
        current = [row["candidate_id"] for row in sorted(r, key=lambda row: int(row["initial_rank"]))][:3]
        entries = traces[key]
        assert len(entries) == 3 and len({e["candidate"] for e in entries}) == 3
        for step, entry in enumerate(entries, 1):
            assert entry["step"] == step and entry["before_top3"] == current
            current = [row["candidate_id"] for row in sorted(r, key=lambda row: int(row[f"rank_after_{step}"]))][:3]
            assert entry["after_top3"] == current
        assert current == [row["candidate_id"] for row in sorted([row for row in r if row["final_slot"]],
                                                                key=lambda row: int(row["final_slot"]))]
        cost = cost_rows[key]
        nbytes = sum(e["received_body_b"] for e in entries)
        nwords = sum(e["display_words"] for e in entries)
        assert nbytes == int(cost["network_body_b"]) <= 1024 * 1024
        assert nwords <= int(cost["display_words"]) <= 750
        assert int(cost["machine_scan_words"]) == sum(e["scanned_words"] for e in entries)
        assert int(cost["http_calls"]) == sum(e["storage"] == "http" for e in entries)
        assert int(cost["cache_reads"]) == sum(e["storage"] == "cache" for e in entries)
        max_bytes, max_words = max(max_bytes, nbytes), max(max_words, nwords)
    for request in requests:
        for arm in ARMS:
            cold, warm = (traces[(request, arm, mode)] for mode in MODES)
            assert [f["display_sha256"] for f in cold] == [f["display_sha256"] for f in warm]
            assert all(f["storage"] == "cache" for f in warm)

    slots = make_slots(root)
    actual = read_csv(root / "slots.csv")
    keyed(actual, lambda r: r["slot_id"])
    assert len(actual) == 108
    assert {(s["request_id"], s["arm"], int(s["slot"])) for s in actual} == {
        (rid, arm, place) for rid in requests for arm in ARMS for place in (1, 2, 3)
    }
    obs = keyed(read_jsonl(root / "evidence/window-observations.jsonl"), lambda r: r["observation_id"])
    individual = keyed(read_jsonl(root / "evidence/individual-readings.jsonl"), lambda r: r["slot_id"])
    assert all(r["observation_id"] in obs for r in individual.values())
    assert set(individual) <= {r["slot_id"] for r in actual}
    assert all((r["grade"] == "unread") == (r["exposure"] != "none" and not r["reading_id"]) for r in actual)

    fixtures = run_fixtures(root / "experiment/grader-fixtures.jsonl")
    assert fixtures == json.loads((root / "evidence/grader-pretest.json").read_text())
    control = json.loads((root / "evidence/controls.json").read_text())
    kinds = Counter(r["kind"] for r in control["results"])
    assert kinds == {"positive": 4, "scope_counterexample": 2, "context_only": 2}
    assert all(r["expected"] == r["observed"] for r in control["results"])
    assert all((r["c1"], r["c2"]) == (True, r["kind"] != "scope_counterexample") for r in control["results"])
    metrics = metric_rows(root, slots, ranks, qrels, list(requests.values()))
    assert metrics == json.loads((root / "evidence/metrics.json").read_text())
    tables = render(root, slots, ranks, qrels, list(requests.values()), metrics)
    result = (root / "RESULT.md").read_text()
    assert result.startswith(tables)
    table_chunks = re.findall(r"(?:^\|.*\|$\n?)+", result, re.MULTILINE)
    sizes = []
    for chunk in table_chunks:
        rows = chunk.splitlines()
        sizes.append({"rows": len(rows) - 2, "columns": len(re.split(r"(?<!\\)\|", rows[0])) - 2})
    assert sizes[:3] == [{"rows": 12, "columns": 6}, {"rows": 108, "columns": 7}, {"rows": 12, "columns": 7}]
    assert sizes[-1] == {"rows": 3, "columns": 3}
    return {
        "status": "passed", "independent_originals": len(countable), "sources_rows": len(sources),
        "candidate_pairs": len(qrels), "ranks": len(ranks), "fetch_attempts": len(fetched),
        "slots": len(actual), "individual_readings": len(individual), "window_observations": len(obs),
        "max_network_body_b": max_bytes, "max_display_words": max_words, "tabulated": sizes,
        "fixed_controls": dict(kinds), "grader_fixtures": fixtures["passed"],
        "replays": compare_replays(root, replay_dirs, tables),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("replay_a", type=Path)
    parser.add_argument("replay_b", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.root, [args.replay_a, args.replay_b]), ensure_ascii=False, indent=2))
