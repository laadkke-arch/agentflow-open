"""Freeze recipient-only conditions; consumes no corpus or outcome material."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    output = HERE / "recipient_targets.jsonl"
    if output.exists():
        raise SystemExit("Refusing to overwrite frozen targets")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    attempts = read_jsonl(HERE / "recipient_attempts.jsonl")
    restores = {(r["repository"], r["pr_number"]): r for r in attempts
                if r["stage"] in {"restore_snapshot", "restore_archived_snapshot"}}
    packets = read_jsonl(HERE / "condition_packets_rust_draft.jsonl")
    packets += read_jsonl(HERE / "condition_packets_kep_draft.jsonl")
    assert len(packets) == 8
    packets.sort(key=lambda r: r["recipient_id"])
    for packet in packets:
        packet["target_scope"] = {
            "whole": "whole_design", "partial": "partial_design"
        }.get(packet["target_scope"], packet["target_scope"])
        if packet["recipient_id"] == "R03":
            # Source-only refinement before any query is authored: separate the
            # selected value-transfer rule from tied/discarded-output support.
            packet["mandatory_conditions"].extend([
                {"id": "R03-M12", "predicate": "After execution, copy each non-discarded declared output register into its output place expression, including a late output.", "source_line_spans": [[340, 346]], "basis": "explicit"},
                {"id": "R03-M13", "predicate": "Initialize each declared input register with its input expression value at the start of the assembly code.", "source_line_spans": [[336, 338]], "basis": "explicit"},
            ])
            packet["frozen_partial_target"]["mandatory_predicate_ids"] = [
                "R03-M13", "R03-M04", "R03-M05", "R03-M12"
            ]
        mandatory = {c["id"]: c for c in packet["mandatory_conditions"]}
        target = packet["frozen_partial_target"]
        target["mandatory_predicates"] = [mandatory[c] for c in target["mandatory_predicate_ids"]]
        target["require_all_mandatory_predicates"] = True
        target["matching_rule"] = "All listed mandatory predicates must be satisfied together; a shared topic or one matching predicate is insufficient."
        target["frozen_at_utc"] = now
        target["frozen_before_provider_evidence"] = True
        restore = restores[(packet["repository"], packet["pr_number"])]
        raw = (ROOT / packet["snapshot_path"]).read_bytes()
        canonical = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert digest(raw) == restore["snapshot_raw_sha256"]
        assert digest(canonical) == restore["snapshot_canonical_lf_sha256"]
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == restore["initial_blob_sha"]
        packet["original_source"] = {
            "original_url": restore["original_url"],
            "immutable_url": restore["fixed_url"],
            "immutable_raw_url": restore["raw_fixed_url"],
            "snapshot_commit_sha": restore["snapshot_commit_sha"],
            "repository_path": restore["initial_path"],
            "git_blob_sha": restore["initial_blob_sha"],
            "raw_sha256": digest(raw),
            "canonical_lf_sha256": digest(canonical),
            "line_count": len(raw.splitlines()),
            "bytes": len(raw),
        }
        for field in ["mandatory_conditions", "preferred_conditions", "unnecessary_conditions", "named_prior_solutions", "initial_document_uncertainties"]:
            for condition in packet[field]:
                for first, last in condition.get("source_line_spans", []):
                    assert 1 <= first <= last <= len(raw.splitlines()), (packet["recipient_id"], condition)
        ids = [c["id"] for field in ["mandatory_conditions", "preferred_conditions", "unnecessary_conditions"] for c in packet[field]]
        assert len(ids) == len(set(ids))
        if packet.get("initial_image"):
            image = packet["initial_image"]
            image_raw = (ROOT / image["image_path"]).read_bytes()
            assert digest(image_raw) == image["raw_sha256"]
            assert hashlib.sha1(b"blob " + str(len(image_raw)).encode() + b"\0" + image_raw).hexdigest() == image["git_blob_sha"]
            image["immutable_raw_url"] = f"https://raw.githubusercontent.com/{packet['repository']}/{image['opening_commit_sha']}/{image['repository_path']}"
    output.write_text("".join(json.dumps(p, ensure_ascii=False, separators=(",", ":")) + "\n" for p in packets))
    print(json.dumps({"path": str(output.relative_to(ROOT)), "sha256": digest(output.read_bytes()), "rows": len(packets), "frozen_at_utc": now,
                      "sources": [{"id": p["recipient_id"], "snapshot_path": p["snapshot_path"], "sha256": p["original_source"]["raw_sha256"], "scope": p["target_scope"]} for p in packets]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
