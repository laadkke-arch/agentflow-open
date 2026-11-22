"""Integrate the independently authored queries without changing either string."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9]+")


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    output = HERE / "inputs_draft.jsonl"
    if output.exists():
        raise SystemExit("Refusing to overwrite frozen query inputs")
    selection = json.loads((HERE / "recipient_selection.json").read_text())
    assert selection["primary_prefix"]["surviving_history_excluded_heads_with_initiality_uncertainty"] == 0, "Prefix archive verification is incomplete"
    packets = records(HERE / "recipient_targets.jsonl")
    sources = {row["recipient_id"]: row for row in records(HERE / "recipient_sources.jsonl") if row["selected"]}
    query_path = HERE / "queries_sealed.jsonl"
    query_file_raw = query_path.read_bytes()
    queries = {row["recipient_id"]: row for row in records(query_path)}
    checks_path = HERE / "query_author_checks.json"
    checks = json.loads(checks_path.read_text())
    assert checks["query_file"]["sha256"] == sha(query_file_raw)
    assert checks["source_packet_actual_sha256"] == sha((HERE / "recipient_targets.jsonl").read_bytes())
    assert all(value is True for value in checks["reading_attestation"].values())
    assert all(value is True for value in checks["manual_scope_review"].values())
    assert checks["authorized_input_count"] == 10
    assert len(packets) == len(sources) == len(queries) == 8
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    inputs, verified = [], []
    for packet in packets:
        recipient_id = packet["recipient_id"]
        source, query = sources[recipient_id], queries[recipient_id]
        raw = (ROOT / packet["snapshot_path"]).read_bytes()
        assert sha(raw) == packet["original_source"]["raw_sha256"] == source["raw_sha256"] == query["source_raw_sha256"]
        original_tokens = set(TOKEN.findall(raw.decode().lower()))
        for label in ["S", "R"]:
            value = query[label]
            assert isinstance(value, str) and value.strip() == value and value == value.lower()
            tokens = TOKEN.findall(value.lower())
            assert 1 <= len(tokens) <= 80
            assert len(tokens) == query[label + "_token_count"]
            assert sha(value.encode()) == query[label + "_sha256"]
            assert sha(" ".join(tokens).encode()) == query[label + "_tokens_sha256"]
            if label == "S":
                assert set(tokens) <= original_tokens, sorted(set(tokens) - original_tokens)
            for first, last in query["source_line_spans_supporting_" + label]:
                assert 1 <= first <= last <= source["line_count"]
        assert packet["target_scope"] in {"whole_design", "partial_design"}
        row = {
            **packet,
            "created_at": source["created_at"],
            "initial_source_id": source["source_id"],
            "immutable_source_url": source["immutable_url"],
            "immutable_source_raw_url": source["immutable_raw_url"],
            "initiality_status": source["initiality_status"],
            "opening_head_certainty": source["opening_head_certainty"],
            "first_authored_draft_certainty": False,
            "provenance": {
                "archive_binding": source["archive_binding"],
                "source_ledger": str((HERE / "recipient_sources.jsonl").relative_to(ROOT)),
                "retrieved_at_utc": source["retrieved_at_utc"],
                "read_line_range": source["read_line_range"],
                "read_at_utc": source["read_at_utc"],
                "read_time_interval_utc": source["read_time_interval_utc"],
                "earliest_retained_proposal_addition_commit_sha": source["earliest_retained_proposal_addition_commit_sha"],
                "first_comparison_commit_sha": source["first_comparison_commit_sha"],
                "first_comparison_commit_limit": source["first_comparison_commit_limit"],
            },
            "limitations": source["limitations"],
            "query_s": query["S"], "query_r": query["R"],
            "query_s_sha256": query["S_sha256"], "query_r_sha256": query["R_sha256"],
            "query_s_token_count": query["S_token_count"], "query_r_token_count": query["R_token_count"],
            "query_s_tokens_sha256": query["S_tokens_sha256"], "query_r_tokens_sha256": query["R_tokens_sha256"],
            "query_author_record": query,
            "query_author_file_sha256": sha(query_file_raw),
            "query_author_checks_sha256": sha(checks_path.read_bytes()),
            "query_language": "English", "query_token_rule": "lowercase regex [a-z0-9]+; maximum80 per query",
            "integrated_at_utc": now,
            "query_strings_changed_by_integrator": False,
            "counted_minimum": True,
        }
        inputs.append(row)
        verified.append({"recipient_id": recipient_id, "S_tokens": query["S_token_count"], "R_tokens": query["R_token_count"],
                         "S_all_tokens_in_original": True, "query_strings_and_hashes_preserved": True})
    output.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in inputs))
    assert query_path.read_bytes() == query_file_raw
    verification = {
        "verified_at_utc": now,
        "inputs_sha256": sha(output.read_bytes()), "query_author_file_sha256": sha(query_file_raw),
        "target_packet_sha256": sha((HERE / "recipient_targets.jsonl").read_bytes()),
        "rows": verified, "query_strings_changed_by_integrator": False,
        "hold": "Ready for root's remote input seal; no outcomes or rankings consumed by recipient collector or query author.",
    }
    (HERE / "recipient_input_checks.json").write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(verification))


if __name__ == "__main__":
    main()
