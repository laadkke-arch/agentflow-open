"""Freeze the published AF-RES-114 input and reconcile the two archived runs."""
import argparse
import csv
import hashlib
import io
import json
import sqlite3
import subprocess
from pathlib import Path
from types import ModuleType


PREDECESSOR = "4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450"
HANDOFF = "9695479c8e9e3c36488f3d0376f197733e05ef3e"
PRECEDENT_PATH = "docs/workstreams/research/AF-RES-114/"
PROFILE = "publisher_partial"
LANGUAGES = ("en", "ko")
FEATURE_FIELDS = (
    "feature_id", "project", "edition", "title", "symbol", "url",
    "memo_en", "note", "roles", "evidence_en", "source_url", "source_id",
)
QUERY_FIELDS = (
    "query_id", "layer", "project", "en", "ko", "operation", "preserve",
    "roles", "url", "source_location", "source_edition",
)
RANK_FIELDS = ("feature_id", "retrieval_rank", "score", "sweep_rank")


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(payload):
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_jsonl(path, rows):
    path.write_text("".join(encode(row) + "\n" for row in rows), encoding="utf-8")


def project(row, fields):
    return {field: row[field] for field in fields}


def predecessor_blob(repo, name, sha=PREDECESSOR):
    return subprocess.run(
        ["git", "show", f"{sha}:{PRECEDENT_PATH}{name}"],
        cwd=repo, stdout=subprocess.PIPE, check=True,
    ).stdout


def predecessor_module(raw):
    module = ModuleType("published_af_res_114_replay")
    module.__file__ = PRECEDENT_PATH + "tools/replay.py"
    exec(compile(raw, module.__file__, "exec"), module.__dict__)
    return module


def archived_projection(row):
    """Read raw ranks, scores and observed display IDs without any score labels."""
    retrieved = json.loads(row["retrieved_json"])
    sweep = sorted(retrieved, key=lambda item: (item["conflicts"], item["rank"]))
    cards = [
        {"feature_id": item["id"], "retrieval_rank": item["rank"],
         "score": item["score"], "sweep_rank": index}
        for index, item in enumerate(sweep, 1)
    ]
    if [x["id"] for x in retrieved] != [
        row[f"r{i:02}"] for i in range(1, 13) if row[f"r{i:02}"]
    ]:
        raise ValueError("archive wide and JSON investigation columns disagree")
    top = [row[f"d{i:02}"] or None for i in range(1, 4)]
    displayed = [x["id"] for x in json.loads(row["display_json"])]
    if displayed != [x for x in top if x is not None] or displayed != [
        card["feature_id"] for card in cards[:3]
    ]:
        raise ValueError("archive display order disagrees with sweep order")
    return {"candidates": cards, "top3": top, "sql_statements": int(row["sql_statements"])}


def padding(values, length):
    return values + [None] * (length - len(values))


def ranking_rows(module, cards, queries, database):
    with sqlite3.connect(database) as connection:
        index_cost = module.create_catalog(connection, cards, PROFILE)
        rows = [
            {
                "kind": "rank",
                "query_id": q["query_id"],
                "language": language,
                "execution": "executed" if q[language] else "vacant_request",
                **archived_projection(module.query_row(connection, q, language, PROFILE, 1, 1, 1)),
            }
            for q in queries
            for language in LANGUAGES
        ]
    for row in rows:
        candidates = row["candidates"]
        retrieval = sorted(candidates, key=lambda c: c["retrieval_rank"])
        row["raw_top12"] = padding([c["feature_id"] for c in retrieval], 12)
        row["investigation_sha256"] = digest(encode(candidates))
    return rows, index_cost


def scoped_view(cards, queries, ranks):
    return (
        [{"kind": "feature", **project(card, FEATURE_FIELDS)} for card in cards]
        + [{"kind": "request", **project(query, QUERY_FIELDS)} for query in queries]
        + [
            {
                "kind": "order", "query_id": row["query_id"], "language": row["language"],
                "candidates": [card["feature_id"] for card in row["candidates"]],
            }
            for row in ranks
        ]
    )


def capture(repo, heldout, out):
    required = [
        "catalog.jsonl", "queries.jsonl", "evidence/ranks-exploratory-publisher.csv",
        "evidence/ranks-controls-publisher.csv", "evidence/table3.csv", "tools/replay.py", "RESULT.md",
    ]
    pinned = {name: predecessor_blob(repo, name) for name in required}
    pinned["HANDOFF.md"] = predecessor_blob(repo, "HANDOFF.md", HANDOFF)

    module = predecessor_module(pinned["tools/replay.py"])
    decode = lambda name: [json.loads(line) for line in pinned[name].decode().splitlines()]
    cards = decode("catalog.jsonl")
    queries = [
        query for query in decode("queries.jsonl")
        if query["layer"] in {"natural", "exploratory", "control"}
    ] + heldout
    if len(cards) != 24 or len({card["feature_id"] for card in cards}) != 24:
        raise ValueError("catalog must have exactly 24 distinct cards")

    out.mkdir(parents=True, exist_ok=False)
    ranks, costs = ranking_rows(module, cards, queries, out / "rank.sqlite")
    by_key = {(r["query_id"], r["language"]): r for r in ranks}
    archive_comparison = []
    for file in required[2:4]:
        reader = csv.DictReader(io.StringIO(pinned[file].decode()))
        for row in reader:
            if (row["profile"], row["alias"], row["role"]) != (PROFILE, "1", "1"):
                continue
            observed = by_key[row["query_id"], row["language"]]
            match = observed["raw_top12"] == [
                row[f"r{i:02}"] or None for i in range(1, 13)
            ] and all(observed[k] == v for k, v in archived_projection(row).items())
            archive_comparison.append({
                "query_id": row["query_id"], "language": row["language"],
                "predecessor_replay": int(row["replay"]), "file": file, "agrees": match,
            })
    if len(archive_comparison) != 40 or not all(entry["agrees"] for entry in archive_comparison):
        raise ValueError(f"archives disagree: {archive_comparison}")

    view = scoped_view(cards, queries, ranks)
    write_jsonl(out / "policy-view.jsonl", view)
    inputs = [
        {
            "kind": "meta", "schema": 1, "predecessor_result": PREDECESSOR,
            "predecessor_handoff": HANDOFF, "profile": PROFILE, "alias": 1, "role": 1,
            "original_blob_sha256": {k: digest(v) for k, v in pinned.items()},
            "policy_view_sha256": digest((out / "policy-view.jsonl").read_bytes()),
            "policy_feature_fields": FEATURE_FIELDS, "policy_query_fields": QUERY_FIELDS,
            "policy_order_fields": ("query_id", "language", "candidates"),
        },
        *[{"kind": "feature", **project(card, FEATURE_FIELDS),
           "alias_publisher": card["alias_publisher"], "evidence_ko": card["evidence_ko"]}
          for card in cards],
        *[{"kind": "request", **project(query, QUERY_FIELDS)} for query in queries],
        *ranks,
    ]
    write_jsonl(out / "inputs.jsonl", inputs)
    receipt = {
        "archived_11_comparisons": archive_comparison,
        "archived_11_query_languages": len({(r["query_id"], r["language"]) for r in archive_comparison}),
        "investigation_and_top3_agree": all(entry["agrees"] for entry in archive_comparison),
        "index_cost": costs, "python_sqlite": sqlite3.sqlite_version,
        "input_sha256": digest((out / "inputs.jsonl").read_bytes()),
        "policy_view_sha256": inputs[0]["policy_view_sha256"],
        "reserved_natural_query_languages": sum(r["execution"] == "vacant_request" for r in ranks),
    }
    (out / "reconciliation.json").write_text(encode(receipt) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--heldout-requests", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = capture(args.repo, jsonl(args.heldout_requests) if args.heldout_requests else [], args.out)
    print(encode({k: v for k, v in result.items() if k != "archived_11_comparisons"}))
