"""Complete the read-source ledger from the already sealed 60-row frame."""
import csv
import datetime
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "evidence/imagemagick/stage3"
FRAME = BASE / "evidence/imagemagick/frame-part.csv"
receipts = json.loads((BASE / "evidence/imagemagick/acquisition-h1.json").read_text())
revisions = {}
for page, receipt in enumerate(receipts, 1):
    raw = json.loads((BASE / f".cache/imagemagick/revisions-h1-{page}.json").read_text())
    for rev in raw["items"]:
        if rev.get("revision_number") == 1 and "body" in rev:
            revisions[rev["post_id"]] = (rev, receipt)
rows = []
for row in csv.DictReader(FRAME.open()):
    if row["selected_slot"]:
        continue
    qid = int(row["question_id"])
    rev, receipt = revisions[qid]
    rows.append({
        "id": f"SO-IM-SCREEN-{qid}", "questions": ["Q1", "Q2"], "case_id": None,
        "original_url": f"https://stackoverflow.com/questions/{qid}",
        "directly_opened_url": receipt["url"], "pinned_url": row["initial_revision_url"],
        "confirmation_utc": receipt["utc"],
        "ledger_completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "author_publisher": rev.get("user", {}).get("display_name", "unknown") + " / Stack Overflow (Stack Exchange API)",
        "lineage": f"Stack Overflow question {qid}",
        "version_section": "public revision1; GUID=" + row["initial_revision_guid"] + "; original body reviewed during Stage1; source locator: entire initial body; row-specific observation is the sealed frame review_reason",
        "fingerprint": {"body_html_sha256": row["initial_body_sha256"], "response_sha256": receipt["sha256"]},
        "observed": row["review_reason"],
        "claim_relation": "Validates chronological recruitment and eligibility boundary; frame_rank=" + row["frame_rank"] + "; eligible=" + row["eligible"] + "; specific_attempt=" + row["specific_attempt"] + "; disposition=" + row["disposition"],
        "limitations": "Not selected because ineligible or because its stratum was already filled. No answers, comments or outcomes used for selection. Current-tag recruitment may differ from initial tags; see frame row.",
        "counted": False, "count_category": "screening_only",
        "duplicate_reason": "Conservative exclusion of all nonselected screening requests from the minimum; not one of the8 selected events.",
        "frame_evidence": {"path": "evidence/imagemagick/frame-part.csv", "frame_rank": int(row["frame_rank"]), "question_id": qid},
    })
assert len(rows) == 56
(OUT / "sources-screening.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
print(json.dumps({"screening_sources": len(rows), "counted": 0}))
