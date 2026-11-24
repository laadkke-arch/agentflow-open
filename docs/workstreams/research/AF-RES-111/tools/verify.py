"""Recompute the comparison from the sealed gold, evidence edges, and two replays."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("original", "synonym", "order", "polarity", "scope", "omission")
CONDITIONS = ("operation", "preserve")
RUN_FILES = ("runs.jsonl", "links.csv", "lifecycle.csv", "calibration.jsonl", "controls.jsonl")


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def csv_rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def goal_status(states):
    if "refuted" in states.values():
        return "excluded"
    if all(x == "supported" for x in states.values()):
        return "verified"
    return "pending"


def read_gold(path):
    return {
        g["request_id"]: {
            "raw": g,
            "states": {k: g[f"{k}_state"] for k in CONDITIONS},
            "proof": {k: set(filter(None, g[f"{k}_evidence"].split("|"))) for k in CONDITIONS},
        } for g in csv_rows(path)
    }


def inputs_and_runs(root):
    requests = {r["id"]: r for r in jsonl(root / "requests.jsonl")}
    cases = {c["case_id"]: c for c in jsonl(root / "facts.jsonl")}
    aliases = {r["read_id"]: r["request_id"] for r in jsonl(root / "evidence" / "blind-map.jsonl")}
    blind = {v["id"]: v for v in jsonl(root / "inputs.jsonl")}
    gold = read_gold(root / "gold.csv")
    runs = {(aliases[r["id"]], r["method"]): r for r in jsonl(root / "runs.jsonl")}
    return requests, cases, aliases, blind, gold, runs


def score(requests, gold, runs):
    report = {}
    for variant in KINDS:
        keys = [rid for rid, q in requests.items() if q["variant"] == variant]
        outcome = {}
        for method in ("A", "B"):
            counts = Counter({
                "condition_denominator": 0, "condition_exact": 0, "condition_false_support": 0,
                "condition_justified_hold": 0, "condition_gold_unknown": 0, "condition_gold_known": 0,
                "condition_missed": 0, "request_denominator": len(keys), "request_exact": 0,
                "request_bad_inheritance": 0, "request_missed": 0, "request_status_exact": 0,
                "request_false_support": 0, "request_justified_hold": 0, "request_gold_pending": 0,
                "request_verified": 0, "request_false_verified": 0, "partial_support_promoted": 0,
                "partial_support_denominator": 0, "raw_same_candidate_and_evidence": 0,
                "shared_gold_link_denominator": 0, "same_gold_link": 0,
            })
            mismatch = {}
            for rid in keys:
                reference = gold[rid]
                measured = runs[rid, method]
                original_id = requests[rid]["case_id"] + "-original"
                original = runs[original_id, method]
                orig_gold = gold[original_id]
                expected_status = goal_status(reference["states"])
                counts["request_status_exact"] += measured["status"] == expected_status
                counts["request_gold_pending"] += expected_status == "pending"
                counts["request_justified_hold"] += expected_status == measured["status"] == "pending"
                counts["request_verified"] += measured["status"] == "verified"
                counts["request_false_verified"] += measured["status"] == "verified" and expected_status != "verified"
                if list(measured["states"].values()).count("supported") == 1:
                    counts["partial_support_denominator"] += 1
                    counts["partial_support_promoted"] += measured["status"] == "verified"
                counts["raw_same_candidate_and_evidence"] += (
                    original["candidate"] == measured["candidate"] and original["evidence"] == measured["evidence"]
                )
                common = {
                    k: reference["proof"][k] & orig_gold["proof"][k]
                    for k in CONDITIONS if reference["states"][k] == orig_gold["states"][k]
                }
                if any(common.values()):
                    counts["shared_gold_link_denominator"] += 1
                    exact_reuse = measured["candidate"] == original["candidate"] and all(
                        common[k] <= set(measured["evidence"][k]) & set(original["evidence"][k]) and
                        reference["states"][k] == measured["states"][k] == original["states"][k]
                        for k in common if common[k]
                    )
                    counts["same_gold_link"] += exact_reuse

                tags = {"wrong_inheritance": [], "false_support": [], "missed": [], "justified_hold": []}
                aligned = []
                for criterion in CONDITIONS:
                    state = measured["states"][criterion]
                    g_state = reference["states"][criterion]
                    used = set(measured["evidence"][criterion])
                    g_ids = reference["proof"][criterion]
                    old_ids = set(original["evidence"][criterion])
                    counts["condition_denominator"] += 1
                    counts["condition_gold_unknown"] += g_state == "unknown"
                    counts["condition_gold_known"] += g_state != "unknown"
                    wrong_carry = bool(used & old_ids) and (state != g_state or bool((used & old_ids) - g_ids))
                    if wrong_carry and variant in {"polarity", "scope", "omission"}:
                        tags["wrong_inheritance"].append(criterion)
                    if state == "supported" and g_state != "supported":
                        counts["condition_false_support"] += 1
                        tags["false_support"].append(criterion)
                    if state == g_state == "unknown" and not used:
                        counts["condition_justified_hold"] += 1
                        tags["justified_hold"].append(criterion)
                    if g_state != "unknown" and (state != g_state or not used & g_ids):
                        counts["condition_missed"] += 1
                        tags["missed"].append(criterion)
                    condition_matches = state == g_state and (
                        bool(used) and used <= g_ids if g_state != "unknown" else not used
                    )
                    counts["condition_exact"] += condition_matches
                    aligned.append(condition_matches)
                exact = all(aligned)
                counts["request_exact"] += exact
                counts["request_bad_inheritance"] += bool(tags["wrong_inheritance"])
                counts["request_false_support"] += bool(tags["false_support"])
                counts["request_missed"] += bool(tags["missed"])
                outcome[rid, method] = exact
                mismatch[rid] = {k: v for k, v in tags.items() if v}
            report.setdefault(variant, {})[method] = {"counts": dict(counts), "by_request": mismatch}
        distribution = Counter()
        for rid in keys:
            distribution[{(True, False): "A_only", (False, True): "B_only",
                          (True, True): "both", (False, False): "neither"}[outcome[rid, "A"], outcome[rid, "B"]]] += 1
        report[variant]["distribution"] = {k: distribution[k] for k in ("A_only", "B_only", "both", "neither")}
    return report


def verify(root, replays):
    requests, cases, aliases, blind, gold, runs = inputs_and_runs(root)
    sources = {s["source_id"]: s for s in jsonl(root / "sources.jsonl")}
    assert Counter(s["allocation"] for s in sources.values() if s["counted"]) == {
        "request": 6, "official": 8, "counter": 6, "cross": 4
    }
    frame = csv_rows(root / "frame.csv")
    assert len(cases) == 6 and len(requests) == 36 and len(gold) == 36 and len(runs) == 72
    assert sha(root / "gold.csv") == json.loads((root / "evidence" / "gold-seal.json").read_text())["committed_gold_sha256"]
    freeze = json.loads((root / "evidence" / "pre-gold-implementation.json").read_text())
    for filename in ("tools/adapters.py", "tools/run.py", "rules.json"):
        assert sha(root / filename) == freeze[filename]
    assert sha(root / "inputs.jsonl") == json.loads((root / "evidence" / "blind-inputs.json").read_text())["requests.jsonl"]
    assert set(r["case_id"] for r in frame if r["disposition"] == "selected") == cases.keys()
    evidence = {f["evidence_id"]: f for c in cases.values() for f in c["evidence"]}
    for f in evidence.values():
        s = f["source"]
        assert s["origin_end"] - s["origin_start"] == len(s["quote"])
        assert hashlib.sha256(s["quote"].encode()).hexdigest() == s["excerpt_sha256"]
        assert s["origin_sha256"] == sources[s["source_id"]]["body_sha256"]

    for read_id, rid in aliases.items():
        packet = blind[read_id]
        question = requests[rid]
        assert set(packet) == {"id", "case_id", "text", "parts"}
        assert packet["text"] == question["text"] and packet["case_id"] == question["case_id"]
        assert gold[rid]["raw"]["read_id"] == read_id
        assert gold[rid]["raw"]["edition"] == cases[question["case_id"]]["candidate"]["version"]
        for name, span in packet["parts"].items():
            assert (packet["text"][slice(*span)] if span else None) == question["parts"][name]
            assert gold[rid]["raw"][name + "_span"] == (":".join(map(str, span)) if span else "")
            expected = gold[rid]["states"][name]
            assert expected in ("supported", "refuted", "unknown")
            assert bool(gold[rid]["proof"][name]) == (expected != "unknown")
            for proof in gold[rid]["proof"][name]:
                # The gold reader can cite a passage across the adapter's
                # assigned criterion. That recall limitation must stay visible.
                assert evidence[proof] in cases[question["case_id"]]["evidence"]
                assert evidence[proof]["version"] == cases[question["case_id"]]["candidate"]["version"]
        if question["natural"]:
            parts = cases[question["case_id"]]["raw_event"]["source_segments"]
            assert question["text"] == "\n".join(r["quote"] for r in parts)
            assert all(r["end"] - r["start"] == len(r["quote"]) for r in parts)
        a, b = runs[rid, "A"], runs[rid, "B"]
        assert a["input_sha256"] == b["input_sha256"]
        assert a["candidate"] == b["candidate"] and a["version"] == b["version"]
        assert a["parts"] == b["parts"] == packet["parts"]

    edges = csv_rows(root / "links.csv")
    edge_counts = Counter()
    for edge in edges:
        f = evidence[edge["evidence_id"]]
        s = f["source"]
        assert edge["source_url"] == s["url"] and edge["selector"] == s["selector"]
        assert int(edge["original_start"]) == s["origin_start"] and int(edge["original_end"]) == s["origin_end"]
        assert edge["excerpt_sha256"] == s["excerpt_sha256"]
        print_id = aliases[edge["id"]]
        run = runs[print_id, edge["method"]]
        assert int(edge["run_id"]) == run["run_id"] and edge["input_sha256"] == run["input_sha256"]
        rid = edge["evidence_id"]
        used = edge["used"] == "True"
        assert used == (rid in run["evidence"][edge["criterion"]])
        if used:
            assert edge["claim_id"] in run["used_claims"]
            assert f["version"] == run["version"]
        request = blind[edge["id"]]
        for item in json.loads(edge["surface_spans"]):
            assert request["text"][slice(*item["span"])] == item["quote"]
        if edge["slots"]:
            for items in json.loads(edge["slots"]).values():
                if isinstance(items, list):
                    for item in items:
                        assert request["text"][slice(*item["span"])] == item["quote"]
        edge_counts[(print_id, edge["method"], edge["criterion"])] += 1
    assert all(0 < count <= 4 for count in edge_counts.values())
    assert len(edge_counts) == 144

    history = csv_rows(root / "lifecycle.csv")
    assert len(history) == 10
    assert len({x["past_sha256"] for x in history}) == len({x["past_source_sha256"] for x in history}) == 1
    for event in history:
        if event["error"] or event["event"] in {"same_scope_same_key", "retry_historical_after_successor"}:
            assert json.loads(event["before"]) == json.loads(event["after"])

    for path in replays:
        b = json.loads((path / "receipt.json").read_text())
        assert b["observed_workstream_input_opens"] == ["inputs.jsonl", "facts.jsonl", "rules.json"]
        for name, fingerprint in b["input_files"].items():
            assert sha(root / name) == fingerprint
        for name in RUN_FILES:
            reference = root / name if name in ("runs.jsonl", "links.csv", "lifecycle.csv") else root / "evidence" / name
            assert sha(path / name) == sha(reference) == b["results_sha256"][name]
        for method in ("A", "B"):
            db = sqlite3.connect(f"file:{path / (method + '.sqlite')}?mode=ro", uri=True)
            try:
                assert db.execute("SELECT count(*) FROM decision_run").fetchone() == (36,)
                assert db.execute("SELECT count(*) FROM decision_item").fetchone() == (72,)
                assert db.execute("SELECT count(*) FROM run_claim").fetchone() == (
                    sum(edge["method"] == method and edge["used"] == "True" for edge in edges),
                )
                assert db.execute("PRAGMA integrity_check").fetchone() == ("ok",)
                assert not db.execute("PRAGMA foreign_key_check").fetchall()
            finally:
                db.close()

    return {
        "main": len(runs), "scheduled": 72, "missing": 0, "edges": len(edges), "lifecycle_events": len(history),
        "evidence_fragments": len(evidence), "replays_checked": len(replays),
        "origin": {"request_cases": 6, "natural_excerpts": 6, "authored_variants": 30,
                   "counted_primary_sources": 24, "source_register_total": len(sources)},
        "metrics": score(requests, gold, runs),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="append", type=Path, default=[])
    parser.add_argument("--summary", type=Path)
    options = parser.parse_args()
    result = verify(ROOT, options.replay)
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if options.summary:
        options.summary.write_text(rendered, encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "metrics"}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
