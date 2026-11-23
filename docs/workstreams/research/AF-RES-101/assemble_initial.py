"""Normalize already coded initial records; no network, no outcome access."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent


def cell(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")) if isinstance(value, (list, dict)) else value


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=fields)
        out.writeheader()
        out.writerows({key: cell(value) for key, value in row.items()} for row in rows)


def normalize_source(s):
    cases = s.get("case_ids", s.get("case_id", []))
    if isinstance(cases, str):
        cases = [cases]
    return {
        "source_id": s.get("source_id", s.get("id")),
        "q": s.get("q", s.get("questions", [])),
        "case_ids": cases,
        "category": s.get("category", s.get("count_category", "method")),
        "original_url": s.get("original_url"),
        "direct_open_url": s.get("direct_open_url", s.get("directly_opened_url", s.get("original_url"))),
        "fixed_url": s.get("fixed_url", s.get("pinned_url")),
        "checked_at_utc": s.get("checked_at_utc", s.get("checked_utc", s.get("confirmation_utc"))),
        "author_publisher": s.get("author_publisher", str(s.get("author", "")) + " / " + str(s.get("publisher", ""))),
        "lineage": s.get("lineage"),
        "version_section_locator": s.get("version_section_locator", s.get("version_section", str(s.get("version", "")) + "; " + str(s.get("location", "")))),
        "fingerprint": s.get("fingerprint", {"sha256": s.get("sha256")}),
        "observed": s.get("observed", s.get("confirmed")),
        "claim_relation": s.get("claim_relation", s.get("supports_or_refutes")),
        "limits_unknown": s.get("limits_unknown", s.get("limitations")),
        "counted": s.get("counted", False),
        "duplicate_reason": s.get("duplicate_reason"),
    }


def main():
    initial = []
    frame = []
    for tag in ("imagemagick", "typst"):
        base = ROOT / "evidence" / tag
        for r in json.loads((base / "initial-part.json").read_text()):
            im = tag == "imagemagick"
            row = {
                "case_id": r["case_id"], "question_id": r["question_id"], "tag": tag,
                "stratum": r["stratum"] if im else {"specific_attempt": "attempt", "no_specific_attempt": "unspecified"}[r["stratum"]],
                "frame_rank": r["selection_rank"] if im else r["frame_rank"],
                "stratum_rank": r["within_stratum_rank"] if im else r["selection_rank"],
                "created_utc": r.get("created_at", r.get("created_utc")),
                "initial_revision_url": r["initial_revision_url"],
                "initial_revision_guid": r["initial_revision_guid"],
                "initial_body_sha256": r["initial_body_sha256"],
                "question_url": r["question_url"],
                "input_state": r["input_state"],
                "purpose": r.get("purpose", r.get("goal")),
                "required_output": r.get("required_output", r.get("mandatory_outputs")),
                "tool_version": r["tool_version"],
                "actual_used_products": r.get("actual_used_products", r.get("actual_products")),
                "operation_attempted": r.get("operation_attempted", r.get("actual_calls")),
                "arguments": r.get("arguments", r.get("known_values")),
                "reported_output_error": r.get("reported_output_error", r.get("observed_output_or_error")),
                "allowed_changes": r["allowed_changes"],
                "known_values": r["known_values"],
                "unknown": r.get("unknown", r.get("unknowns")),
                "history": r.get("history", {"attempt_status": r.get("attempt_status"), "mention_only": r.get("mention_only"), "third_party_suggestion": r.get("other_person_suggestion_at_baseline")}),
                "source_id": r.get("source_id", "SO-T-" + str(r["question_id"])),
                "source_record": "evidence/" + tag + "/initial-part.json",
                "original_location": r.get("location", "evidence char[start,end) and 1-based HTML lines in source_record"),
                "title_changed": r.get("title_changed", r.get("current_vs_initial_title_different")),
                "tags_changed": r.get("tags_changed", r.get("current_vs_initial_tags_different")),
                "judged_at_utc": r.get("sealed_at", r.get("coded_utc")),
            }
            initial.append(row)
        for r in csv.DictReader((base / "frame-part.csv").open()):
            frame.append({
                "tag": tag, "window": r["window"], "frame_rank": r["frame_rank"], "question_id": r["question_id"],
                "created_utc": r.get("created_at", r.get("created_utc")),
                "initial_revision_url": r.get("initial_revision_url", r.get("initial_url")),
                "initial_revision_guid": r["initial_revision_guid"], "initial_body_sha256": r["initial_body_sha256"],
                "initial_available": r.get("initial_available", r.get("first_revision_found")),
                "initial_title": r["initial_title"], "current_title": r["current_title"],
                "initial_tags": r["initial_tags"], "current_tags": r["current_tags"],
                "title_changed": r["title_changed"], "tags_changed": r["tags_changed"],
                "stratum": {"specific_attempt":"attempt", "no_specific_attempt":"unspecified"}.get(r["stratum"], r["stratum"]),
                "eligible": r["eligible"], "selected_slot": r.get("selected_slot", r.get("selected_case", "")),
                "disposition": r["disposition"], "reason": r.get("review_reason", r.get("reason")),
                "duplicate_or_cross_tag": r.get("duplicate_or_cross_tag", "cross_tag=" + r.get("cross_tag_imagemagick", "False")),
                "source_record": "evidence/" + tag + "/frame-part.csv",
            })
    order = {s: i for i, s in enumerate(["IM-A1", "IM-A2", "IM-U1", "IM-U2", "TY-A1", "TY-A2", "TY-U1", "TY-U2"])}
    initial.sort(key=lambda r: order[r["case_id"]])
    assert len(initial) == 8 and len({r["question_id"] for r in initial}) == 8
    assert len(frame) == 87 and sum(bool(r["selected_slot"]) for r in frame) == 8
    write_csv(ROOT / "initial.csv", initial)
    write_csv(ROOT / "frame.csv", frame)
    sources = []
    for p in [ROOT / "evidence/start/sources-method.jsonl", ROOT / "evidence/imagemagick/sources-part.jsonl", ROOT / "evidence/typst/sources-part.jsonl"]:
        sources.extend(normalize_source(json.loads(line)) for line in p.read_text().splitlines() if line)
    (ROOT / "sources.jsonl").write_text("".join(json.dumps(s, ensure_ascii=False) + "\n" for s in sources))
    print(json.dumps({"initial_slots": len(initial), "frame_rows": len(frame), "counted_initial_sources": sum(s["counted"] for s in sources), "selected_ids": [r["question_id"] for r in initial]}))


if __name__ == "__main__":
    main()
