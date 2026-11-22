"""Cross-check the staged cohort, publication-time visits, and saved result totals."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def jsonl(path):
    with path.open(encoding="utf-8") as source:
        return [json.loads(line) for line in source]


def validate(root):
    for line in (root / "cohort.sha256").read_text().splitlines():
        expected, path = line.split()
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == expected, path
    cohort = [r for r in rows(root / "cohort.csv") if r["selected"] == "1"]
    assert Counter(r["ecosystem"] for r in cohort) == {"python": 32, "node": 32}
    assert len({(r["ecosystem"],r["group"]) for r in cohort}) == len(cohort)
    assert len({r["t0_url"] for r in cohort}) == 64
    assert all(r["group_frame_n"] and r["prob_within"] != "0" for r in cohort)
    releases = rows(root / "releases.csv")
    assert len(releases) == 34
    assert all(r["public_date"] <= r["cutoff"] < r["next_higher_date"] for r in releases)
    snapshots = {}
    for family in ("cold","reuse1","reuse2"):
        seen = []
        for run in jsonl(root / "evidence" / "runs" / f"{family}.jsonl"):
            q = run["quarter"]
            seen.append(q)
            records = jsonl(root / "evidence" / "receipts" / family / f"{q}.jsonl")
            snap = jsonl(root / "snapshots" / f"{q}.jsonl")
            assert len(records) == len(snap) == 72, q
            for key in ("http_attempts","http_body_bytes","git_pack_bytes","new_objects",
                        "local_reads","local_bytes","retries"):
                assert sum(r[key] for r in records) == run[key], (q,family,key)
            for record in snap:
                key = q,record["ecosystem"],record["kind"],record["path"]
                snapshots[key] = record
            for receipt in records:
                key = receipt["quarter"],receipt["ecosystem"],receipt["kind"],receipt["path"]
                assert receipt["status"] == snapshots[key]["status"]
                assert receipt["body_sha256"] == snapshots[key]["sha256"]
                if family != "cold":
                    assert receipt["http_attempts"] == receipt["http_body_bytes"] == receipt["new_objects"] == 0
        assert len(seen) == len(set(seen)) == 17
    findings = rows(root / "observed-findings.csv")
    for r in findings:
        snap = snapshots[r["quarter"],r["ecosystem"],r["kind"],r["path"]]
        assert snap["status"] == "ok"
        assert r["url"].split("#")[0] == snap["url"]
        if r["kind"] == "release_notes":
            assert any(s["quarter"] == r["quarter"] and s["ecosystem"] == r["ecosystem"] and
                       s.get("release_path") == r["path"] for s in snapshots.values())
    timeline = jsonl(root / "timeline.jsonl")
    truth = {(r["quarter"],r["id"]):r["adjudication"]["state"] for r in timeline}
    assert len(truth) == len(timeline) == 64 * 17
    assert Counter(truth[q,r] for q,r in truth if q != "T0") == {
        "invalid":95,"supported":897,"initial_error":16,"unknown":16,
    }
    basis = json.loads((root / "truth.json").read_text())
    by_reason = {r: e for e in basis["events"] for r in e["reason_ids"]}
    assert len(basis["events"]) == 10 and len(by_reason) == 11
    sources = {r["id"]:r for r in json.loads((root / "sources.json").read_text())}
    for e in basis["events"]:
        assert e["notice_source"] in sources and e["release_source"] in sources
        assert e["implementation_sources"]
        assert all(s in sources for s in e["implementation_sources"])
        assert all(sources[s]["url"] != sources[e["release_source"]]["url"] for s in
                   e["implementation_sources"])
    count = Counter(r["category"] for r in sources.values() if r["counts_toward_minimum"])
    assert count["t0_reference"] >= 12 and count["official_comparison"] >= 12
    assert count["crossfield_crawler"] >= 2 and count["crossfield_scholar"] >= 2
    assert sum(count.values()) >= 28
    assert len({r["url"].split("#")[0] for r in sources.values() if
                r["counts_toward_minimum"]}) == sum(count.values())
    visits = rows(root / "visits.csv")
    observed = {(r["quarter"],r["id"],r["url"]) for r in findings if r["status"] == "invalid"}
    doc_visits = {(v["scenario"],v["quarter"],v["url"]) for v in visits
                  if v["entry_type"] == "document_attempt" and v["opened_original"] == "True"}
    attempts = defaultdict(Counter)
    decisions = defaultdict(Counter)
    positive = defaultdict(set)
    for v in visits:
        sc, q, id = v["scenario"],v["quarter"],v["id"]
        is_oracle = sc == "O-known-address"
        if v["entry_type"] == "document_attempt":
            if not is_oracle:
                assert v["kind"] != "given_event_url"
                attempts[sc,q]["network"] += int(v["http_attempts"] or 0)
                attempts[sc,q]["documents"] += int(v["review_units"] or 0)
            continue
        state = truth[q,id]
        pred = v["predicted_invalid"] == "True"
        if state in {"initial_error","unknown"}:
            decisions[sc][state] += 1
        else:
            label = ("TP" if pred else "FN") if state == "invalid" else ("FP" if pred else "TN")
            decisions[sc][label] += 1
        if v["outcome"].endswith("_invalid"):
            if not is_oracle:
                assert (q,id,v["proof"]) in observed
                assert (sc,q,v["proof"].split("#")[0]) in doc_visits
            if state == "invalid":
                positive[sc].add(id)
    for (sc,q),counts in attempts.items():
        budget = int(sc.split("-")[1])
        assert max(counts.values(),default=0) <= budget, (sc,q,counts)
    main = {}
    for m in rows(root / "metrics.csv"):
        if not m["stratum"] == m["ecosystem"] == "all":
            continue
        sc = m["scenario"]
        for key in ("TP","FP","FN","TN","unknown","initial_error"):
            assert int(m[key]) == decisions[sc][key], (sc,key)
        assert int(m["reasons_seen"]) == len(positive[sc])
        if sc.endswith("20-t2-cold-charged-once-both") or sc == "O-known-address":
            main[sc] = m["reasons_seen"]
    assert sorted(main.values()) == ["0","11","11","8"]
    result = (root / "RESULT.md").read_text().strip().splitlines()
    assert result[2].startswith("## 표 1")
    assert [l[:6] for l in result if l.startswith("## 표")] == ["## 표 1","## 표 2","## 표 3","## 표 4"]
    assert result[-5].startswith("| 중요한 불일치") and all(l.startswith("| ") for l in result[-5:])
    return dict(release_rows=len(releases),reasons=len(cohort),observed_snapshots=len(snapshots),
                truth_rows=len(truth),visit_rows=len(visits),main=main,source_counts=dict(count))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--inputs",type=Path,default=HERE)
    args = cli.parse_args()
    print(json.dumps(validate(args.inputs),ensure_ascii=False,sort_keys=True))
