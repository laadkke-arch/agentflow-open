#!/usr/bin/env python3
"""Join donor-only field records, validate hashes, and prepare the corpus seal.

This script never reads recipient artifacts and does not calculate rankings.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(name: str, rows: list[dict]) -> None:
    (BASE / name).write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8", newline="\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_cache_path(value: str) -> Path:
    supplied = Path(value)
    if supplied.is_absolute():
        resolved = supplied.resolve()
    elif value.startswith("cache/"):
        resolved = (BASE / supplied).resolve()
    else:
        resolved = (REPO / supplied).resolve()
    assert resolved.is_relative_to((BASE / "cache").resolve()), resolved
    return resolved


def main() -> None:
    rows = read_jsonl(BASE / "library_statistics_corpus_draft.jsonl") + read_jsonl(BASE / "transit_corpus_draft.jsonl")
    expected = {f"{prefix}{number:02d}" for prefix in "LTS" for number in range(1, 7)}
    assert len(rows) == 18 and {row["candidate_id"] for row in rows} == expected
    order = {"L": 0, "T": 1, "S": 2}
    rows.sort(key=lambda row: (order[row["candidate_id"][0]], row["candidate_id"]))
    validations = []
    for row in rows:
        path = resolve_cache_path(row["cache_text_path"])
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        assert raw and b"\r" not in raw and "\ufffd" not in text, row["candidate_id"]
        actual = hashlib.sha256(raw).hexdigest()
        declared = row.get("body_sha256") or row.get("text_sha256") or row.get("selected_body_sha256")
        assert actual == declared, row["candidate_id"]
        row["cache_text_path"] = str(path.relative_to(REPO))
        row["body_sha256"] = actual
        row["text_sha256"] = actual
        row["body_lines"] = len(text.splitlines())
        row["body_bytes"] = len(raw)
        row["body_whitespace_words"] = len(text.split())
        row["source_id"] = row.get("source_id", row["candidate_id"])
        row["counted_minimum"] = True
        row["substantive_read"] = True
        if row["candidate_id"].startswith("T"):
            row["field"] = "transport"
        if row.get("cache_raw_path"):
            source = resolve_cache_path(row["cache_raw_path"])
            if row.get("raw_sha256"):
                assert digest(source) == row["raw_sha256"], row["candidate_id"]
            row["cache_raw_path"] = str(source.relative_to(REPO))
        validations.append({"candidate_id": row["candidate_id"], "body_sha256": actual, "utf8_lf": True, "body_lines": row["body_lines"], "body_whitespace_words": row["body_whitespace_words"], "raw_hash_verified_when_declared": True})
    assert len({row["url"] for row in rows}) == 18
    assert Counter(row["field"] for row in rows) == Counter({"library": 6, "transport": 6, "statistics": 6})
    write_jsonl("corpus_draft.jsonl", rows)

    source_inputs = read_jsonl(BASE / "library_statistics_sources.jsonl") + read_jsonl(BASE / "transit_sources.jsonl")
    selected_by_id = {row["source_id"]: row for row in rows}
    excluded = []
    for source in source_inputs:
        if source.get("source_id") in selected_by_id:
            continue
        assert not source.get("counted_minimum", False), source.get("source_id")
        excluded.append(source)
    assert len({row["source_id"] for row in rows + excluded}) == len(rows + excluded)
    write_jsonl("donor_sources.jsonl", rows + excluded)

    attempts = read_jsonl(BASE / "donor_attempts.jsonl")
    transit_attempts = read_jsonl(BASE / "transit_attempts.jsonl")
    existing = {json.dumps(row, ensure_ascii=False, sort_keys=True) for row in attempts}
    attempts.extend(row for row in transit_attempts if json.dumps(row, ensure_ascii=False, sort_keys=True) not in existing)
    write_jsonl("donor_attempts.jsonl", attempts)

    frame_path = BASE / "donor_frame.csv"
    frame = list(csv.DictReader(frame_path.open(encoding="utf-8", newline="")))
    by_issuer = {row["issuer"]: row for row in rows}
    for entry in frame:
        match = by_issuer.get(entry["issuer"])
        if match:
            entry.update(status="selected", selected_candidate_id=match["candidate_id"], selected_url=match["url"])
        else:
            entry.setdefault("selected_candidate_id", "")
            entry.setdefault("selected_url", "")
    columns = list(frame[0])
    with frame_path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(frame)

    report = {
        "status": "pass",
        "scope": "Donor-only source identity, unique counts, selected-body hashes, UTF-8/LF encoding, and declared raw hashes; no recipient material accessed.",
        "selected_count": len(rows),
        "selected_by_field": dict(Counter(row["field"] for row in rows)),
        "substantively_read_excluded_source_record_count": sum(bool(row.get("substantive_read") or row.get("read_notes")) for row in excluded),
        "attempt_record_count": len(attempts),
        "corpus_metadata_sha256": digest(BASE / "corpus_draft.jsonl"),
        "source_metadata_sha256": digest(BASE / "donor_sources.jsonl"),
        "selected_body_set_sha256": hashlib.sha256(json.dumps({row["candidate_id"]: row["body_sha256"] for row in rows}, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
        "selected_body_set_hash_recipe": "SHA256 of UTF-8 compact JSON mapping candidate_id to selected-body SHA256, keys sorted ascending, separators comma/colon, no final newline",
        "selected_bodies": validations,
    }
    (BASE / "capture_validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
