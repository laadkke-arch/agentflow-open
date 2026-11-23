"""Assemble already frozen fragments; never fetch issue follow-ups."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def read_jsonl(path):
    return [json.loads(s) for s in path.read_text().splitlines() if s.strip()]


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows))


def main():
    fragments = [
        ROOT / "evidence/inkscape/records_A.jsonl",
        ROOT / "evidence/inkscape/records_B.jsonl",
        ROOT / "evidence/pillow/records-a.jsonl",
        ROOT / "evidence/pillow/records-b.jsonl",
    ]
    records = []
    for path in fragments:
        for row in read_jsonl(path):
            # Keep original record payload and original byte count unchanged.
            row = dict(row)
            row["request_id"] = row.get("request_id", row.get("case_id"))
            row["mode"] = row.get("mode", row.get("method"))
            row["fragment"] = path.relative_to(ROOT).as_posix()
            records.append(row)
    records.sort(key=lambda r: (r["request_id"], r["mode"]))
    assert len(records) == 12
    assert {(r["request_id"], r["mode"]) for r in records} == {
        (case, mode) for case in ("I1", "I2", "I3", "P1", "P2", "P3") for mode in ("A", "B")
    }
    write_jsonl(ROOT / "records.jsonl", records)

    frame_rows = []
    for project in ("inkscape", "pillow"):
        path = ROOT / "evidence" / project / "frame.csv"
        with path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                rank = row.get("unique_event_rank") or row.get("canonical_rank")
                selected = row.get("selected") == "true" or row.get("selection") == "selected"
                frame_rows.append({
                    "project_key": project,
                    "source_fragment": path.relative_to(ROOT).as_posix(),
                    "event_rank": rank,
                    "is_first30": str(bool(rank) and int(rank) <= 30).lower(),
                    "selected_for_study": str(selected).lower(),
                    **row,
                })
    fields = list(dict.fromkeys(k for r in frame_rows for k in r))
    with (ROOT / "frame.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(frame_rows)

    judgment_rows = []
    for row in records:
        candidates = row["record"]["candidates"]
        judgment_rows.append({
            "request_id": row["request_id"], "method": row["mode"],
            "pre_judgment": row["judgment"], "pre_reason": row["reason"],
            "record_bytes": row["utf8_bytes"],
            "candidate_count": sum(c is not None for c in candidates),
            "contaminated": str(row.get("contaminated", False)).lower(),
            "truth": "", "scorable": "false", "truth_attribution": "미공개",
            "post_source_ids": "", "post_urls": "", "expected": "",
            "error_class": "미채점", "unconfirmed": "사전 봉인 단계: 후속 원자료 아직 공개하지 않음",
        })
    with (ROOT / "judgments.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(judgment_rows[0]))
        writer.writeheader()
        writer.writerows(judgment_rows)

    original_sources = read_jsonl(ROOT / "sources.jsonl")
    sources = [r for r in original_sources if r["source_id"].startswith("CAL-")]
    for path in [ROOT / "evidence/root-sources.jsonl", ROOT / "evidence/inkscape/sources.jsonl", ROOT / "evidence/pillow/sources.jsonl"]:
        sources.extend(read_jsonl(path))
    assert len({r["source_id"] for r in sources}) == len(sources)
    write_jsonl(ROOT / "sources.jsonl", sources)

    summary = {
        "assembled_utc": datetime.now(timezone.utc).isoformat(),
        "scope_remote_commit": "b9f878064bcf27b627a16977c9fa4580268aed3c",
        "fragments": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in fragments},
        "record_count": len(records), "request_count": 6,
        "candidate2_missing": sorted({r["request_id"] for r in records if r["record"]["candidates"][1] is None}),
        "posthoc_open_permission": False,
        "blindness_limits": ["same coder A then B", "I3 edited-body follow-up sentence exposed before seal", "earliest original revision not fully recovered"],
    }
    (ROOT / "evidence/preseal-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
