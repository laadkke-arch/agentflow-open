"""Check the sealed ledgers independently of the view evaluator."""
import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def table(path, key=None):
    with path.open(encoding="utf-8", newline="") as handle:
        data = list(csv.reader(handle))
    headers, body = data[0], data[1:]
    assert len(headers) == len(set(headers))
    assert all(len(row) == len(headers) for row in body), path.name
    records = [dict(zip(headers, row, strict=True)) for row in body]
    if key:
        assert len({row[key] for row in records}) == len(records), path.name
    return records, {"rows": len(records), "columns": len(headers)}


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def audit(result):
    sources = lines(ROOT / "sources.jsonl")
    frame, frame_size = table(ROOT / "frame.csv", "frame_id")
    selected = [r for r in frame if r["result"] == "selected"]
    assert Counter(r["layer"] for r in selected) == {"A": 4, "B": 4}
    assert len({r["native_id"] for r in frame}) == len(frame) == 19
    by_source = {r["id"]: r for r in sources}
    assert len(by_source) == len(sources)
    counted = [s for s in sources if s["counted"]]
    assert len({s["lineage_id"] for s in counted}) == len(counted) >= 20
    assert all(by_source[row["source_id"]]["counted"] for row in selected)
    for s in counted:
        for field in ("lineage_id", "source_url", "author", "edition", "confirmed_utc", "location",
                      "claim", "limits", "counterexample_or_unknown", "access"):
            assert s[field], (s["id"], field)
        assert s["confirmed_utc"].endswith("Z")
    captures = json.loads((ROOT / "inputs" / "sha256.json").read_text())
    for name, expected in captures["source_extracts"].items():
        raw = (ROOT / "inputs" / name).read_bytes()
        assert sha256(raw).hexdigest() == expected["sha256"] and len(raw) == expected["bytes"]

    pairs, pair_size = table(ROOT / "pairs.csv", "pair_id")
    by_pair = {r["pair_id"]: r for r in pairs}
    object_set = {r["object_id"] for r in selected}
    assert {r["object_id"] for r in pairs} == object_set
    targets = defaultdict(set)
    for row in pairs:
        if row["primary"] == "1":
            targets[row["layer"], row["type"]].add(row["object_id"])
        assert len(row["before_payload_sha256"]) == len(row["after_payload_sha256"]) == 64
    assert len(targets) == 10 and min(map(len, targets.values())) >= 2
    assert Counter(r["primary"] for r in pairs) == {"1": 22, "0": 4}
    assert all(r["treatment"] == "advance" for r in pairs if r["primary"] == "0")
    primary_ids = {r["pair_id"] for r in pairs if r["primary"] == "1"}

    runs = lines(result / "runs.jsonl")
    by_run = {r["id"]: r for r in runs}
    assert len(runs) == len(by_run)
    assert Counter(r["event"] for r in runs) == {
        "instrumented": 52, "paired_oracle_check": 26, "view_evaluation": 156,
        "transaction_trial": 14, "fragment_loss_control": 1,
    }
    for pair in pairs:
        pid = pair["pair_id"]
        for label in ("before", "after"):
            run = by_run[pid + ":" + label]
            assert (run["version"], run["object_id"], run["edge"]) == (
                pair[label + "_version"], pair["object_id"], label)
        change = by_run["DIFF:" + pid]
        assert change["observed_changes"] == change["expected_changes"]
        assert list(map(int, change["observed_changes"])) == [int(pair[key]) for key in (
            "expected_answer_change", "expected_reason_change", "expected_link_change", "expected_load_order_change")]
    for holdout in ("A4", "B4"):
        first = next(i for i, r in enumerate(runs) if r.get("object_id") == holdout)
        assert not any(r.get("object_id") and not r["object_id"].endswith("4") for r in runs[first:])

    judged, judgment_size = table(result / "judgments.csv", "id")
    groups = defaultdict(list)
    primary_judgments = 0
    for row in judged:
        pair = by_pair[row["pair_id"]]
        assert all(row[k] == pair[k] for k in ("layer", "type", "primary"))
        assert row["old_run"] == pair["pair_id"] + ":before" and row["new_run"] == pair["pair_id"] + ":after"
        assert row["old_run"] in by_run and row["new_run"] in by_run
        expected = "defer" if row["actual"] == "defer" else "correct" if row["expected"] == row["actual"] else "wrong"
        assert row["status"] == expected
        if row["pair_id"] in primary_ids:
            groups[tuple(row[k] for k in ("layer", "type", "regime", "view", "probe"))].append(row)
            primary_judgments += 1
    assert len(judged) == 26 * 2 * 3 * 30 and primary_judgments == 22 * 2 * 3 * 30

    scores, score_size = table(result / "scores.csv")
    assert len(scores) == len(groups)
    for score in scores:
        k = tuple(score[name] for name in ("layer", "type", "regime", "view", "probe"))
        group = groups.pop(k)
        s = Counter(r["status"] for r in group)
        for label in ("correct", "wrong", "defer"):
            assert int(score[label]) == s[label]
        assert int(score["n"]) == len(group) == sum(s.values())
        decided = Counter((r["expected"], r["actual"]) for r in group)
        if any(r["expected"] in ("yes", "no") for r in group):
            yes = sum(r["expected"] == "yes" for r in group)
            no = len(group) - yes
            assert (int(score["true_n"]), int(score["false_n"])) == (yes, no)
            assert int(score["false_negative"]) == decided["yes", "no"]
            assert int(score["false_positive"]) == decided["no", "yes"]
            assert int(score["held_true"]) == decided["yes", "defer"]
            assert int(score["held_false"]) == decided["no", "defer"]
        else:
            assert not any(score[k] for k in ("true_n", "false_n", "false_negative", "false_positive"))
    assert not groups

    costs, cost_size = table(result / "costs.csv", "id")
    cost_sets = defaultdict(list)
    for row in costs:
        assert row["object_id"] in object_set and row["pair_id"] in primary_ids
        assert row["editorial_http_calls"] == "0"
        assert 1 <= int(row["resolver_calls"]) <= 2 and row["elapsed_ns"].isdigit()
        assert int(row["sqlite_bytes"]) - int(row["sqlite_before_bytes"]) == int(row["sqlite_increment_bytes"])
        key = tuple(row[k] for k in ("object_id", "regime", "view", "cache"))
        cost_sets[key].append(row)
    for (_, _, _, state), entry in cost_sets.items():
        assert sorted(r["trial"] for r in entry) == ["1", "2", "3"]
        assert all((int(r["cache_start_bytes"]) == 0) == (state == "cold") for r in entry)
    assert len(costs) == 8 * 2 * 3 * 2 * 3
    cost_summary, summary_size = table(result / "cost-summary.csv")
    for row in cost_summary:
        key = tuple(row[k] for k in ("object_id", "regime", "view", "cache"))
        if key[0] == "all":
            subset = [r for k, entries in cost_sets.items() if k[1:] == key[1:] for r in entries]
        else:
            subset = cost_sets[key]
        values = sorted(int(r[row["metric"]]) for r in subset)
        middle = len(values) // 2
        mid = values[middle] if len(values) % 2 else (values[middle - 1] + values[middle]) / 2
        assert int(row["n"]) == len(values)
        assert (int(row["min"]), float(row["median"]), int(row["max"]), int(row["sum"])) == (
            values[0], mid, values[-1], sum(values))

    tx = json.loads((result / "evidence" / "transactions.json").read_text())
    assert tx["duplicate_rows"] == tx["old_answers_modified"] == tx["residual_rows_after_rollback"] == 0
    assert tx["replayed_after_reopen"] and len(tx["trials"]) == 14
    assert by_run["LOSS01"]["old_recompute"] == "defer"
    return {"frame": frame_size, "pairs": pair_size, "judgments": judgment_size, "scores": score_size,
            "costs": cost_size, "cost-summary": summary_size, "runs": len(runs),
            "sources": len(sources), "counted": len(counted),
            "direct_web_open_count": sum(s["access"] == "web_open_publisher" for s in counted),
            "publisher_body_indexed_count": sum(s["access"] == "publisher_body_indexed_text" for s in counted),
            "primary_judgments": primary_judgments, "transaction_trials": len(tx["trials"]),
            "unique_pair_object_cells_and_denominators": "passed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT)
    print(json.dumps(audit(parser.parse_args().out), ensure_ascii=False, indent=2))
