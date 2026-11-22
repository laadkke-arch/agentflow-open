"""Merge independently saved reading ranges without multiplying duplicate works."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = "source_id original_url pinned_url_or_version publisher event_or_publication_date checked_utc locator source_kind verified_fact limitation question_ids case_ids duplicate_group counted".split()
CATEGORIES = {
    "independent_counter": "counter",
    "independent_publication_record": "bibliography",
    "institution": "bibliography",
}
rows = []
for source_file in sorted((ROOT / "streams").glob("*/sources.jsonl")):
    for line_number, line in enumerate(source_file.read_text().splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        missing = [key for key in FIELDS if key not in row]
        if missing:
            raise ValueError((source_file.name, line_number, missing))
        row["stream_quota_category"] = row.get("quota_category", "excluded")
        row["quota_category"] = CATEGORIES.get(row["stream_quota_category"], row["stream_quota_category"])
        row["reading_record"] = str(source_file.relative_to(ROOT)) + ":" + str(line_number)
        rows.append(row)
rows.sort(key=lambda row: row["source_id"])
ids = [row["source_id"] for row in rows]
assert len(ids) == len(set(ids)), "duplicate source_id"
counted = [row for row in rows if row["counted"]]
groups = [row["duplicate_group"] for row in counted]
assert len(groups) == len(set(groups)), "same work counted more than once"
(ROOT / "sources.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
report = {
    "reading_ranges": len(rows),
    "unique_counted_works": len(counted),
    "categories": dict(collections.Counter(row["quota_category"] for row in counted)),
    "missing_required_fields": 0,
    "duplicate_counted_groups": 0,
    "note": "Reading ranges, failed attempts and repeated readings remain separate; only representative counted=true rows enter quotas. This is a format/count check, not historical verification.",
}
(ROOT / "evidence" / "source-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False))
