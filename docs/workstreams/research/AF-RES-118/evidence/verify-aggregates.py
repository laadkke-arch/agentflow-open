"""Check committed slot arithmetic and old display IDs without the selector."""
import csv
import hashlib
import io
import json
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIN = "4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450"
OLD = "docs/workstreams/research/AF-RES-114/evidence/"


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def verify():
    ranks = {}
    for line in (ROOT / "inputs.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["kind"] == "rank":
            ranks[row["query_id"], row["language"]] = row
    assert len(ranks) == 44
    slots = defaultdict(list)
    for row in csv_rows(ROOT / "slots.csv"):
        key = row["query_id"], row["language"], row["policy"]
        slots[key].append(row)
    assert len(slots) == 44 * 3

    comparisons = 0
    for name in ("ranks-exploratory-publisher.csv", "ranks-controls-publisher.csv"):
        archived = subprocess.check_output(["git", "show", f"{PIN}:{OLD}{name}"]).decode()
        for row in csv.DictReader(io.StringIO(archived)):
            if row["alias"] != "1" or row["role"] != "1":
                continue
            qid, language = row["query_id"], row["language"]
            assert ranks[qid, language]["raw_top12"] == [row[f"r{i:02}"] or None for i in range(1, 13)]
            assert [s["feature_id"] for s in slots[qid, language, "A"]] == [row[f"d{i:02}"] for i in range(1, 4)]
            comparisons += 1
    assert comparisons == 40

    for (qid, language, _), rows in slots.items():
        rank = ranks[qid, language]
        raw = [item for item in rank["raw_top12"] if item]
        assert [int(row["slot"]) for row in rows] == [1, 2, 3]
        assert {row["feature_id"] for row in rows if row["feature_id"]} <= set(raw)
        assert raw == [r["feature_id"] for r in sorted(rank["candidates"], key=lambda x: (-x["score"], x["feature_id"]))]

    metrics = json.loads((ROOT / "metrics.json").read_text(encoding="utf-8"))
    repeats = metrics["repeat"]["runs"]
    assert {record["observation_sha256"] for record in repeats} == {repeats[0]["observation_sha256"]}
    paths = {"slots.csv": ROOT / "slots.csv"}
    paths.update({name: ROOT / "evidence" / name for name in ("table1.csv", "table3.csv", "perturbations.csv", "policy-scans.csv")})
    for file, path in paths.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == repeats[0]["output_sha256"][file]
    table3 = csv_rows(ROOT / "evidence/table3.csv")
    assert len(table3) == 24
    flat = [row for group in slots.values() for row in group]
    for row in table3:
        group = [s for s in flat if tuple(s[k] for k in ("layer", "language", "policy")) ==
                 tuple(row[k] for k in ("layer", "language", "policy"))]
        for label in ("direct", "partial", "conflict", "unknown"):
            found = [s for s in group if s["reference_class"] == label]
            assert len(found) == int(row[label + "_pairs"])
            assert len({s["query_id"] for s in found}) == int(row[label + "_requests"])
        assert sum(s["display"] == "vacant" for s in group) == int(row["vacancies"])
        if row["eligible_pairs"] == "0":
            assert row["direct_recall"] == ""
    sources = [json.loads(row) for row in (ROOT / "sources.jsonl").read_text(encoding="utf-8").splitlines()]
    counted = [r for r in sources if r["count_unique"]]
    assert len(counted) == len({r["origin_or_event_id"] for r in counted}) == 35
    assert all(r["status"] in {"body", "binary_body"} for r in counted)
    labels = csv_rows(ROOT / "judgments.csv")
    assert len(labels) == 384
    assert {sid for r in labels for sid in r["reference_sources"].split()} <= {r["source_id"] for r in sources}
    print(f"archived_11={comparisons} slots={len(flat)} table3_groups={len(table3)} "
          f"reference_pairs={len(labels)} primary_works={len(counted)}")


if __name__ == "__main__":
    verify()
