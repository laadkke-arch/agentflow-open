"""Recount ledger, match, budget and packet evidence for AF-RES-039."""
import argparse
import csv
import io
import json
import tarfile
import tempfile
import unittest.mock
from collections import Counter
from datetime import datetime
from pathlib import Path

import replay
from batch import read_manifest
from measure import checks, load_lines, measure, physicals, write_csv
from prepare import ROOT, sha, storage
from score import BUDGETS, METRICS, pair_state, parser_class, reference_tables

MAIN_COMMIT = "64589b5c9786f7a94d01fe1a37de77bff0e1a35c"
SOURCE_KEYS = {
    "source_id", "original_url", "pinned_url_or_version", "publisher", "published_or_event_date",
    "checked_utc", "locator", "source_kind", "verified_fact", "limitation", "question_ids",
    "case_ids", "duplicate_group", "counted",
}


def csv_rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def sum_request(entries):
    requests = [entry["request"] for entry in entries]
    exchanges = [exchange for request in requests for exchange in request["exchanges"]]
    return {
        "logical_gets": len(requests), "http_exchanges": sum(item["http_exchange"] for item in exchanges),
        "proxy_connects": sum(item["proxy_connect_attempted"] for item in exchanges),
        "received_body_bytes": sum(item["received_body_bytes"] for item in exchanges),
        "error_count": sum(bool(item["error"]) for item in requests),
        "request_seconds_sum": round(sum(item["elapsed_seconds"] for item in requests), 6),
    }


def storage_summary():
    table = storage()
    fixed_historical_url_counts = Counter(
        unit["url"] for (_, cfg), (record, _) in table.items() if cfg == "C2"
        for unit in record["historical_retrieval_units"]
    )
    c1 = sum(len(data) for (_, cfg), (_, data) in table.items() if cfg == "C1")
    c2 = sum(len(data) for (_, cfg), (_, data) in table.items() if cfg == "C2")
    return {
        "rows": len(table),
        "identical_B_pairs": sum(table[(ref, "C1")][0]["B"].encode() == record["B"].encode()
                                 for (ref, cfg), (record, _) in table.items() if cfg == "C2"),
        "C1_serialized_bytes": c1, "C2_serialized_bytes": c2, "increment_bytes": c2 - c1,
        "B_unique_text_bytes": sum(len(row["B"].encode()) for (_, cfg), (row, _) in table.items() if cfg == "C1"),
        "H_card_text_bytes": sum(len(row.get("H", "").encode()) for row, _ in table.values()),
        "H_artifact_url_occurrences": sum(fixed_historical_url_counts.values()),
        "H_artifact_distinct_URLs": len(fixed_historical_url_counts),
        "reused_H_artifact_URLs": {url: n for url, n in fixed_historical_url_counts.items() if n > 1},
    }


def derived_receipts(raw, grades, pairs, sources):
    assert len(raw) == len(grades) == 48 and len(pairs) == 24
    by_run = {row["run_id"]: row for row in raw}
    assert len(by_run) == 48
    observed = [row for row in sources if row["counted"]]
    assert all(SOURCE_KEYS <= row.keys() for row in sources)
    assert len({row["source_id"] for row in sources}) == len(sources)
    assert len({row["duplicate_group"] for row in observed}) == len(observed)
    assert len({(row["ref_id"], row["task"]) for row in pairs}) == 24
    for pair in pairs:
        c1, c2 = (by_run[pair[f"{cfg}_run"]] for cfg in ("C1", "C2"))
        assert c1["ref_id"] == c2["ref_id"] == pair["ref_id"]
        assert c1["task"] == c2["task"] == pair["task"]
        for budget in BUDGETS:
            for score in ("success", "equivalent_success"):
                col = f"{budget}_pair_state" if score == "success" else f"{budget}_equivalent_pair_state"
                assert pair[col] == pair_state(c1[f"{budget}_{score}"] == "True", c2[f"{budget}_{score}"] == "True")
        for metric in METRICS:
            delta = float(c2[metric]) - float(c1[metric])
            assert abs(float(pair[f"C2_minus_C1_{metric}"]) - delta) <= 0.000001
    for row in grades:
        actual = by_run[row["run_id"]]
        for budget, score in row["budgets"].items():
            assert (actual[f"{budget}_success"] == "True") == score["success"]
            assert actual[f"{budget}_state"] == score["state"]
        logical, strict = (row["budgets"][b] for b in BUDGETS)
        assert not strict["success"] or logical["success"]
        if row["task"] == "restore":
            assert logical["success"] == (logical["N"] == logical["H"] == "exact")
            assert strict["success"] == (strict["N"] == strict["H"] == "exact")
    return {
        "runs": len(raw), "pairs": len(pairs), "grades": len(grades), "bidirectional_cost_pairs": len(pairs),
        "source_ledger_rows": len(sources), "unique_counted": len(observed),
        "count_categories": dict(Counter(row["count_category"] for row in observed)),
        "consumer_exact_members": sum(row.get("exact_fixed_member", False) for row in observed),
    }


def fixtures():
    doc = replay.html_document(b'<html><h1 id="present">Title 2024</h1><p>POSIX edition</p></html>')
    case = {"Presealed minimum purpose (collector paraphrase)": "2018 POSIX",
            "Original href": "https://example.org/spec"}
    wrong_anchor, _ = replay.classify_document(doc, "https://example.org/spec#absent", case, "")
    wrong_edition, _ = replay.classify_document(doc, "https://example.org/spec#present", case, "")
    assert wrong_anchor["reason"] == "WRONG_OR_MISSING_ANCHOR"
    assert wrong_edition["reason"] == "EDITION_UNCONFIRMED"
    with tempfile.TemporaryDirectory(prefix="af039-audit-") as base:
        archive = Path(base) / "docs.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            data = b"unrelated member"
            info = tarfile.TarInfo("project/other.txt")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
        receipt, text = replay.receipt_for_member(
            archive, {"member": "project/missing.txt", "url": "https://example.org/docs.tar.gz"}
        )
        assert receipt["error"] == "ARCHIVE_MEMBER_MISSING" and text is None
    with unittest.mock.patch("replay.subprocess.run") as client:
        client.side_effect = replay.subprocess.TimeoutExpired("curl", 0.1, output=b"", stderr=b"")
        receipt, _ = replay.exchange("https://example.org/example", Path("/tmp/af039-no-output"), 0.1)
        assert receipt["error"] == "TIMEOUT" and receipt["status"] is None
    return {"synthetic_offline_passed": ["missing anchor", "wrong edition", "archive member missing",
                                         "curl timeout return"], "live_network": False}


def replication(main, replica):
    ref = {row["run_id"]: row for row in main}
    rows = []
    for event in replica:
        a = measure(ref[event["run_id"]])
        b = measure(event)
        assert a["input_sha256"] == b["input_sha256"]
        assert a["tool_exit_code"] == b["tool_exit_code"] == 0
        assert not event["file_access"]["unexpected_workspace_or_tmp_open_paths"]
        comparable = ("provisional_action", "logical_gets", "http_exchanges", "total_body_bytes",
                      "displayed_local_H_bytes", "failures", "final_urls", "response_sha256s")
        rows.append({
            "run_id": event["run_id"], "input_sha256": a["input_sha256"], "started_utc": b["started_utc"],
            "all_route_action_body_hashes_equal": all(a[key] == b[key] for key in comparable),
            "changed_fields": ";".join(key for key in comparable if a[key] != b[key]),
            **{key: b[key] for key in ("logical_gets", "http_exchanges", "total_body_bytes",
                  "displayed_local_H_bytes", "request_seconds_sum", "worker_wall_seconds", "tool_wall_seconds", "failures")},
        })
    assert len(rows) == 8
    return rows


def duplicate_response_cost(main):
    success = [shot for row in main for shot in physicals(row) if shot["status"] == 200 and not shot["error"]]
    by_url, by_hash = {}, {}
    for item in success:
        by_url.setdefault(item["requested_url"], item["received_body_bytes"])
        by_hash.setdefault(item["body_sha256"], item["received_body_bytes"])
    return {
        "successful_body_downloads": len(success),
        "successful_body_bytes": sum(item["received_body_bytes"] for item in success),
        "same_URL_shared_cache_hypothesis": {"objects": len(by_url), "first_received_bytes": sum(by_url.values())},
        "digest_distinct_body_count": len(by_hash),
        "unique_digest_bytes": sum(by_hash.values()),
        "scope": "Only successful 200 document payloads. Hypothesis pools all tasks/configurations. "
                 "Redirections, errors, validation and future cache freshness excluded.",
    }



def verify_saved_documents():
    import subprocess

    result = (ROOT / "RESULT.md").read_text().splitlines()
    blocks = []
    previous = ""
    for line in result:
        if line.startswith("| "):
            if not blocks or not previous.startswith("| "):
                blocks.append([])
            blocks[-1].append(line)
        previous = line
    assert result[0].startswith("# AF-RES-039") and not result[1] and result[2].startswith("| 참조 ID")
    assert len(blocks[0]) - 2 == 48 and len(blocks[1]) - 2 == 4 and len(blocks[-1]) - 2 == 3
    assert result[-1] == blocks[-1][-1]
    all_attempts = load_lines(ROOT / "attempts.jsonl")
    main = [row for row in all_attempts if row["phase"] == "main"]
    plans = read_manifest()
    assert [r["run_id"] for r in main] == [r["run_id"] for r in plans]
    assert all(r["logical_gets"] <= 2 and all(q["elapsed_seconds"] <= 30 for q in r["requests"]) for r in main)
    assert [(r["ref_id"], r["task"]) for r in main[::2]] == [(r["ref_id"], r["task"]) for r in main[1::2]]
    sources = load_lines(ROOT / "sources.jsonl")
    recount = derived_receipts(csv_rows("runs.csv"), load_lines(ROOT / "evidence/span-matches.jsonl"),
                               csv_rows("pairs.csv"), sources)
    data = json.loads((ROOT / "evidence/acceptance-evidence.json").read_bytes())
    criteria = data["conditions"]
    assert data["summary"] == {"total": len(criteria), "met": sum(row["met"] for row in criteria),
                               "unmet": [row["id"] for row in criteria if not row["met"]]}
    for row in criteria:
        for item in row["evidence"]:
            name, _, span = item.partition(":")
            path = ROOT / name
            assert path.is_file(), item
            if span:
                assert max(map(int, span.split("-"))) <= len(path.read_bytes().splitlines()), item
    receipt = json.loads((ROOT / "evidence/receipts.json").read_bytes())
    assert recount == receipt["derived_recount"]
    for name, digest in receipt["hashes"].items():
        assert sha((ROOT / name).read_bytes()) == digest, name
    original = (ROOT / "attempts.jsonl").read_bytes().splitlines(keepends=True)[:48]
    raw = json.loads((ROOT / "evidence/raw-observations.json").read_bytes())
    assert sha(b"".join(original)) == raw["attempts_prefix_sha256"]
    plan = json.loads((ROOT / "manifest.json").read_bytes())
    for name, pin in {"SCOPE.md": "scope_sha256", "prepare.py": "generator_sha256",
                      "inputs.jsonl": "inputs_sha256"}.items():
        assert sha((ROOT / name).read_bytes()) == plan["experiment_pins"][pin]
    assert sha((ROOT / "replay.py").read_bytes()) == receipt["runner_sha256"]
    edited = subprocess.check_output(
        ["git", "diff", "--name-only", plan["base_commit"]], text=True, cwd=ROOT).splitlines()
    assert all(any(path.startswith(p) for p in plan["allowed_paths"]) for path in edited)
    return {"exit_code": 0, "tables": [48, 4, 3], "acceptance": data["summary"], "recount": recount,
            "checked_with_original_bodies": False, "changed_paths_inside_contract": len(edited)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main_capture", type=Path, nargs="?")
    parser.add_argument("diagnostic_capture", type=Path, nargs="?")
    parser.add_argument("--documents-only", action="store_true")
    args = parser.parse_args()
    if args.documents_only:
        print(json.dumps(verify_saved_documents(), ensure_ascii=False, indent=2))
        return
    if args.main_capture is None or args.diagnostic_capture is None:
        parser.error("Both body capture directories are required for full audit.")
    all_attempts = load_lines(ROOT / "attempts.jsonl")
    main_events = [row for row in all_attempts if row["phase"] == "main"]
    grades = load_lines(ROOT / "evidence/span-matches.jsonl")
    runs, pairs = csv_rows("runs.csv"), csv_rows("pairs.csv")
    sources = load_lines(ROOT / "sources.jsonl")
    repl = replication(main_events, [row for row in all_attempts if row["phase"] == "replication"])
    write_csv(ROOT / "evidence/replication.csv", repl)
    report = derived_receipts(runs, grades, pairs, sources)
    criteria = load_lines(ROOT / "evidence/current-criteria.jsonl")
    source_ids = {row["source_id"] for row in sources}
    assert all(set(row["source_ids"]) <= source_ids for row in criteria)
    plans = read_manifest()
    assert len(plans) == 48 and len({row["input_sha256"] for row in plans}) == 24
    pinned = load_lines(ROOT / "evidence/packet-boundaries.jsonl")
    assert len(pinned) == 4 and all(row["network_attempts"] == 0 for row in pinned)
    original = json.loads((ROOT / "evidence/raw-observations.json").read_bytes())
    text = (ROOT / "attempts.jsonl").read_bytes().splitlines(keepends=True)
    assert sha(b"".join(text[:48])) == original["attempts_prefix_sha256"]
    components, _, _ = reference_tables()
    g02_note = args.diagnostic_capture / "DG-G02-release" / "1-1.body"
    g02_note_sha = sha(g02_note.read_bytes())
    g02_expected = components["G02"][0]["H"]["spans"][1]
    g02_normalizer = parser_class("collectors/gnu/parse_html.py", "Document")()
    g02_normalizer.feed(g02_note.read_text(errors="replace"))
    g02_notes_exact = g02_expected["text"] in g02_normalizer.text
    windows = [datetime.fromisoformat(row["checked_utc"]) for row in sources if row["source_id"] in
               {sid for c in criteria if c["same_window_action"] for sid in c["source_ids"]}]
    observations = {
        "checked_utc": replay.utc(),
        "runner": "Python -I -B, curl 8.14.1, strace, fresh temporary folders; managed Code Cloud",
        "seed": 39036, "algorithm_version": "1.0",
        "remote_commits_before_result": {
            "scope": "52048b3d238966da17c9739639f4619ef2890bd7",
            "runner_pins": "2982044f4fb1cb7de4b7f239c193f7f95bcf7d40",
            "raw": MAIN_COMMIT,
        },
        "runner_sha256": sha((ROOT / "replay.py").read_bytes()),
        "raw_envelope_and_meter_audit": checks(main_events, args.main_capture),
        "derived_recount": report, "storage": storage_summary(),
        "criterion_count": sum(bool(row["same_window_action"]) for row in criteria),
        "criterion_linked_observations": [min(windows).isoformat(), max(windows).isoformat()],
        "replication": {"same_routes_status_body_hashes": sum(row["all_route_action_body_hashes_equal"] for row in repl),
                         "rows": len(repl), **{key: round(sum(row[key] for row in repl), 6) for key in (
                             "logical_gets", "http_exchanges", "total_body_bytes", "request_seconds_sum",
                             "worker_wall_seconds", "tool_wall_seconds")}},
        "source_attempts": dict(Counter(row["phase"] for row in all_attempts)),
        "post_seal_costs": {
            phase: sum_request([row for row in all_attempts if row["phase"] == phase])
            for phase in ("diagnostic", "source_http")
        },
        "pooled_200_body_arithmetic": duplicate_response_cost(main_events),
        "G02_post_seal_release_notes": {
            "body_sha256": g02_note_sha, "whole_body_matches_036": g02_note_sha == g02_expected["source_sha256"],
            "excerpt_matches_036": g02_notes_exact, "excerpt_sha256": g02_expected["text_sha256"],
            "normalized_offset": g02_normalizer.text.find(g02_expected["text"]),
        },
        "fixtures": fixtures(),
        "commands_and_exit_codes": [
            ["python -B batch.py boundary --capture-dir /tmp/af039-boundary-52048 --journal evidence/packet-boundaries.jsonl", 0],
            ["python -B batch.py main --capture-dir /tmp/af039-main-2982044 --journal attempts.jsonl", 0],
            ["python -B measure.py /tmp/af039-main-2982044", 0],
            ["python -B batch.py replication --capture-dir /tmp/af039-replication-64589 --journal /tmp/af039-replication-64589.jsonl", 0],
            ["python -B score.py /tmp/af039-main-2982044", 0],
            ["python -B audit.py /tmp/af039-main-2982044 /tmp/af039-diag-capture", 0],
        ],
        "hashes": {name: sha((ROOT / name).read_bytes()) for name in
                   ("attempts.jsonl", "inputs.jsonl", "runs.csv", "pairs.csv", "sources.jsonl",
                    "evidence/current-criteria.jsonl", "evidence/span-matches.jsonl", "evidence/replication.csv")},
    }
    (ROOT / "evidence/receipts.json").write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: observations[key] for key in ("derived_recount", "storage", "replication",
                     "post_seal_costs", "pooled_200_body_arithmetic", "G02_post_seal_release_notes")}, indent=2))


if __name__ == "__main__":
    main()
