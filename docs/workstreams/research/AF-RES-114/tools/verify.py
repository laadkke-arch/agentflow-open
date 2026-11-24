"""Independently check frozen inputs, rank arithmetic, evidence, and repeat output."""

import argparse
import collections
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOP = set("a an and as at be by for from in is it of on or the to with www https html".split())
COLUMNS = tuple(f"r{i:02}" for i in range(1, 13))
DISPLAY = tuple(f"d{i:02}" for i in range(1, 4))
MODES = {"00", "10", "01", "11"}
PROFILES = {"verified": "alias_verified", "publisher_partial": "alias_publisher"}


def jsonl(path):
    with path.open(encoding="utf-8") as f:
        return list(map(json.loads, f))


def csvs(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def words(s):
    if not s:
        return set()
    s = unicodedata.normalize("NFKC", s).casefold()
    parts = "".join(character if character.isalnum() else " " for character in s).split()
    return set(parts) - STOP


def hangul_terms(labels):
    terms = set()
    for label in labels:
        terms.update(word for word in words(label["ko"]) if re.search("[가-힣ㄱ-ㅎㅏ-ㅣ]", word))
    return terms


def brute_rank(cards, profile, question, alias):
    scores = {}
    for fid, card in cards.items():
        matches = {}
        for field, weight in (("title", 3), ("memo_en", 2), ("url", 1)):
            matches.update({field + ":" + term: weight for term in words(card[field]) & question})
        if alias:
            matches.update({"alias:" + term: 3 for term in hangul_terms(card[PROFILES[profile]]) & question})
        if matches:
            scores[fid] = (sum(matches.values()), sorted(matches))
    return [(fid, *scores[fid]) for fid in sorted(scores, key=lambda candidate: (-scores[candidate][0], candidate))[:12]]


def role_count(candidate, request):
    candidate_mapping = collections.defaultdict(set)
    for item in candidate:
        candidate_mapping[item["concept"]].add(item["role"])
    return sum(
        len(candidate_mapping[item["concept"]]) > 0 and item["role"] not in candidate_mapping[item["concept"]]
        for item in request
    )


def check_sources(cards, queries, sources):
    assert all(s["status"] == "direct" for s in sources.values() if s["unique_count"])
    counted = [s["lineage"] for s in sources.values() if s["unique_count"]]
    assert len(counted) == len(set(counted))
    for card in cards.values():
        assert card["source_id"] in sources
        for field in PROFILES.values():
            for alias in card[field]:
                assert sources[alias["source_id"]]["status"] == "direct"
                assert alias["ko"] and alias["en"]
                if field == "alias_verified":
                    assert card["manual_key"]["ko_msgid_verified"]
        for role in card["roles"]:
            assert role["source_id"] == card["source_id"]
            assert any(role["url"] == e["url"] for e in card["evidence_en"]) or role["url"] == card["source_url"]
            assert role["url"] != card["evidence_ko"]["url"]
    for query in queries.values():
        if query["source_id"]:
            assert sources[query["source_id"]]["status"] == "direct"
        for role in query["roles"]:
            assert role["url"] == query["url"] and role["source_id"] == query["source_id"]
    return len(counted)


def check_rank_file(path, cards, queries):
    rows = csvs(path)
    matches = collections.defaultdict(list)
    grouped = collections.defaultdict(dict)
    sql_queries = 0
    for row in rows:
        qid = row["query_id"]
        query = queries[qid]
        assert query["layer"] == row["layer"]
        text = query[row["language"]]
        terms = words(text)
        assert sorted(terms) == json.loads(row["terms"])
        alias = row["alias"] == "1"
        role = row["role"] == "1"
        expected = brute_rank(cards, row["profile"], terms, alias)
        observed = json.loads(row["retrieved_json"])
        assert [(x["id"], x["score"], x["matched"]) for x in observed] == expected
        assert [x["rank"] for x in observed] == list(range(1, len(expected) + 1))
        raw = [a[0] for a in expected]
        explanation_count = {fid: role_count(cards[fid]["roles"], query["roles"]) for fid in raw}
        if role:
            target = sorted(raw, key=explanation_count.get)[:3]
            for record in observed:
                assert record["conflicts"] == explanation_count[record["id"]]
                assert [c["request"] for c in record["comparisons"]] == query["roles"]
                for cmp in record["comparisons"]:
                    published_roles = cards[record["id"]]["roles"]
                    assert cmp["candidate"] == [e for e in published_roles if e["concept"] == cmp["request"]["concept"]]
                    assert all(e["url"] for e in cmp["candidate"])
        else:
            target = raw[:3]
        result = json.loads(row["display_json"])
        assert [x["id"] for x in result] == target
        assert [x["slot"] for x in result] == list(range(1, len(target) + 1))
        assert [row[c] for c in COLUMNS] == raw + [""] * (12 - len(raw))
        assert [row[c] for c in DISPLAY] == target + [""] * (3 - len(target))
        assert row["execution"] == ("executed" if text else "vacant_request")
        assert int(row["sql_statements"]) == int(bool(terms)) + int(bool(raw) and role)
        sql_queries += int(row["sql_statements"])
        mode = row["alias"] + row["role"]
        measure = (row["profile"], qid, row["language"])
        matches[(*measure, mode)].append({key: val for key, val in row.items() if key != "replay"})
        grouped[(*measure, row["replay"])][mode] = raw
    assert all(len(repeats) == 2 and repeats[0] == repeats[1] for repeats in matches.values())
    for arms in grouped.values():
        assert set(arms) == MODES and arms["00"] == arms["01"] and arms["10"] == arms["11"]
    return len(rows), sql_queries


def check_truth(cards, queries):
    adjudication = {
        "natural": "truth.csv",
        "exploratory": "evidence/truth-exploratory.csv",
        "control": "evidence/truth-controls.csv",
    }
    counts = {}
    for layer, file in adjudication.items():
        rows = csvs(ROOT / file)
        wanted = {(q["query_id"], c) for q in queries.values() if q["layer"] == layer for c in cards}
        assert len(rows) == len(wanted)
        assert {(r["query_id"], r["feature_id"]) for r in rows} == wanted
        assert all(r["rank_access"] == "withheld" and r["candidate_evidence_url"] for r in rows)
        assert all(r["operation"] and r["preservation"] and r["rationale"] for r in rows)
        assert all((r["verdict"] == "vacant_request") == (queries[r["query_id"]]["status"] != "ready") for r in rows)
        assert all((r["verdict"] == "direct") == (r["operation"] == r["preservation"] == "supported") for r in rows)
        assert all(r["query_evidence_url"] for r in rows if r["verdict"] != "vacant_request")
        counts[layer] = dict(collections.Counter(r["verdict"] for r in rows))
    return counts


def one_row(path, qid, language, mode):
    row, = [r for r in csvs(path) if r["replay"] == "1" and r["query_id"] == qid
            and r["language"] == language and r["alias"] + r["role"] == mode]
    return row


def verify_control_effects(out):
    baseline = out / "evidence/ranks-controls-publisher.csv"
    missing = out / "evidence/ranks-filter_missing.csv"
    broken_role = out / "evidence/ranks-box_role_omitted.csv"
    assert one_row(baseline, "C-N2", "ko", "10")["r01"] == "K-L04"
    assert one_row(missing, "C-N2", "ko", "10")["r01"] == ""
    for lang in ("en", "ko"):
        good = one_row(baseline, "C-P2", lang, "11")
        lost = one_row(broken_role, "C-P2", lang, "11")
        assert good["d01"] == "B-M03" and lost["r01"] == "B-M03"
        assert "B-M03" not in [lost[c] for c in DISPLAY]
    original_clone = one_row(out / "evidence/ranks-controls.csv", "C-P1", "ko", "00")
    assert original_clone["d01"] == "K-L01"
    assert (out / "evidence/ranks-controls.csv").read_bytes() == (out / "evidence/ranks-clone_missing.csv").read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay-output", required=True, type=Path)
    parser.add_argument("--table-output", required=True, type=Path)
    args = parser.parse_args()
    out = args.replay_output
    costs = json.loads((ROOT / "costs.json").read_text(encoding="utf-8"))
    cards = {c["feature_id"]: c for c in jsonl(ROOT / "catalog.jsonl")}
    queries = {q["query_id"]: q for q in jsonl(ROOT / "queries.jsonl")}
    sources = {s["source_id"]: s for s in jsonl(ROOT / "sources.jsonl")}
    assert len(cards) == 24
    assert len(sources) == len(jsonl(ROOT / "sources.jsonl"))
    requests = [q for q in queries.values() if q["layer"] == "natural"]
    assert len(requests) == 6
    tracker = [f for f in csvs(ROOT / "frame.csv") if f["kind"] == "tracker"]
    assert len(tracker) == 80
    assert check_sources(cards, queries, sources) >= 24
    adjudication = check_truth(cards, queries)
    assert "truth" not in (ROOT / "tools/replay.py").read_text(encoding="utf-8").casefold()
    expected_pairs = list(costs["rank_file_sha256"])
    measurements = {}
    for name in expected_pairs:
        regenerated = out / name
        assert regenerated.read_bytes() == (ROOT / name).read_bytes()
        assert hashlib.sha256(regenerated.read_bytes()).hexdigest() == costs["rank_file_sha256"][name]
        profile_case = next((name for name in costs["contrasts"] if regenerated.stem == "ranks-" + name), "")
        effective_cards = cards
        if profile_case:
            effective_cards = {c["feature_id"]: c for c in jsonl(out / "scratch" / f"{profile_case}.jsonl")}
            assert sum(cards[k] != effective_cards[k] for k in cards) == int(costs["contrasts"][profile_case]["changed_from_base"])
        measurements[name] = check_rank_file(regenerated, effective_cards, queries)
    assert measurements["ranks.csv"] == (96, 0)
    assert (out / "costs.json").read_bytes() == (ROOT / "costs.json").read_bytes()
    for name in ("table1.csv", "table2.csv", "table3.csv", "summary.json"):
        assert (args.table_output / name).read_bytes() == (ROOT / "evidence" / name).read_bytes()
    verify_control_effects(out)
    print(json.dumps({
        "rank_file_count": len(measurements),
        "rank_rows": sum(x[0] for x in measurements.values()),
        "sql_statements": sum(x[1] for x in measurements.values()),
        "natural_rows_reserved": measurements["ranks.csv"][0],
        "natural_queries_executed": measurements["ranks.csv"][1],
        "truth": adjudication,
        "source_ids": len(sources),
        "table_files": 4,
        "control_interventions": 3,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
