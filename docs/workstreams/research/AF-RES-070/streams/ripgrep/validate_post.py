"""Validate ripgrep's sealed packets and post-seal ledger joins without git mutation."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SEAL = "a6e2f47e6cfa52e249f4d648016cf9d324eccae9"
checks = []


def check(name, condition, detail=None):
    checks.append({"check": name, "passed": bool(condition), "detail": detail})
    if not condition:
        raise AssertionError(name)


def read(name):
    return json.loads((BASE / name).read_text())


def jsonl(name):
    return [json.loads(line) for line in (BASE / name).read_text().splitlines() if line]


def utc(value):
    return datetime.fromisoformat(value.replace(" UTC", "+00:00").replace("Z", "+00:00"))


def index(rows, key):
    out = {row[key]: row for row in rows}
    check("unique " + key, len(out) == len(rows), len(rows))
    return out


pre = index(read("pre.json"), "issue_id")
post = index(read("post.json"), "issue_id")
outcomes = index(read("outcomes.json"), "issue_id")
events = index(read("events.json"), "event_id")
pins = index(read("pins-post.json"), "issue_id")
check("view and outcome issue joins", set(pre) == set(post) == set(outcomes) == set(pins))
check("sealed row count", len(pre) == 6)
check("event count", len(events) == 15)
for key, a in pre.items():
    b = post[key]
    o = outcomes[key]
    check(key + " fixed candidate identities", a["candidates"] == b["candidates"])
    check(key + " fixed version", a["version_sha"] == b["version_sha"])
    a_sections = a.get("packet_doc_sections_by_candidate", [c["evidence"] for c in a["candidates"]])
    b_sections = b.get("packet_doc_sections_by_candidate", [c["evidence"] for c in b["candidates"]])
    check(key + " fixed sections", a_sections == b_sections)
    check(key + " fixed field", a["selected_field"] == b["selected_field"])
    check(key + " A precedes comment reading", utc(a["cutoff_A_utc"]) < utc(b["first_comment_read_utc"]))
    check(key + " actual seal reference", b["A_seal_sha"] == o["A_seal_sha"] == pins[key]["A_seal_sha"] == SEAL)
    check(key + " at most one added value", o["B_added_field_count"] <= 1)
    if b["B_source_event_id"]:
        event = events[b["B_source_event_id"]]
        check(key + " B event join", event["issue_id"] == key)
        check(key + " B same numeric author", event["same_numeric_author"])
    check(key + " no circular success proof", o["B_statement_reused_as_success_proof"] is False)
    if b["B_source_event_id"] is None:
        check(key + " missing B not strict accuracy denominator", not o["strict_change_denominator"])

source_pre = jsonl("sources-pre.jsonl")
source_post = jsonl("sources-post.jsonl")
check("post sources do not double count issues", all(s["count_toward_minimum"] is False for s in source_post))
counted = [s for s in source_pre if s["count_toward_minimum"]]
check("unique counted lineages", len({s["lineage_id"] for s in counted}) == len(counted))
pages = [s["pagination"] for s in source_post if "pagination" in s]
check("six comment endpoints complete", len(pages) == 6 and all(p["all_pages_complete"] and p["returned"] < p["per_page"] for p in pages))
check("pagination event total", sum(p["returned"] for p in pages) == len(events))

remote_blobs = {"pre.json": "9bfda117bc112330417076ed3543cda676c45f21", "A.md": "ed5807bf004a469f1684ababe468585411b267ff"}
blob_receipts = []
for name, remote_sha in remote_blobs.items():
    data = (BASE / name).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    check(name + " matches GitHub A-seal blob", blob == remote_sha)
    blob_receipts.append({"path": str((BASE / name).relative_to(BASE.parents[1])), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "local_git_blob": blob, "remote_git_blob": remote_sha, "same": blob == remote_sha})

cross = read("cross-review.json")
check("cross review not extra sources", cross["new_source_count"] == 0 and not cross["count_toward_minimum"])
check("cross review row IDs", {r["review_id"] for r in cross["reviews"]} == {"CR-RCL4911", "CR-JQ2349"})
with (BASE / "q-check.csv").open(newline="") as handle:
    rows = list(csv.reader(handle))
check("q-check column widths", bool(rows) and all(len(r) == len(rows[0]) for r in rows))
check("Q1 to Q8 rows", len(rows) == 9)

counts = {
    "main_slots": sum(o["main_slot_denominator"] for o in outcomes.values()),
    "diagnostic_rows": sum(not o["main_slot_denominator"] for o in outcomes.values()),
    "new_B_values": sum(o["actual_B_denominator"] for o in outcomes.values()),
    "strict_accuracy_denominator": sum(o["strict_change_denominator"] for o in outcomes.values()),
    "question_false_positive_denominator": sum(o["question_false_positive_denominator"] for o in outcomes.values()),
    "question_false_positive_numerator": sum(o["question_false_positive"] is True for o in outcomes.values()),
    "observed_pairs": sum(o["is_observed_pair"] for o in outcomes.values()),
    "source_lineages_counted": len(counted),
    "direct_issue_works": sum(s["kind"] == "original_issue" for s in counted),
    "direct_official_works": sum(s["kind"].startswith("official_versioned_") for s in counted),
}
check("denominator sums", counts["main_slots"] == 3 and counts["diagnostic_rows"] == 3 and counts["new_B_values"] == 1 and counts["strict_accuracy_denominator"] == 0 and counts["question_false_positive_denominator"] == 1 and counts["question_false_positive_numerator"] == 0)

receipt = {
    "validated_utc": datetime.now(timezone.utc).isoformat(),
    "cwd": str(BASE.parents[5]),
    "target_sha": SEAL,
    "command": "python -B docs/workstreams/research/AF-RES-070/streams/ripgrep/validate_post.py",
    "exit_code": 0,
    "scope": "ripgrep stream local joins, A seal blob identity, counts; no original OSS binaries executed",
    "checks": checks,
    "counts": counts,
    "remote_read": {
        "tool": "mcp__codex_apps__github_fetch_file",
        "arguments_common": {"link_id": "link_6afeba07d38881919e7e632c521ab112", "repository_full_name": "laadkke-arch/agentflow-open", "ref": SEAL},
        "path_prefix": "docs/workstreams/research/AF-RES-070/streams/ripgrep/",
        "files": ["pre.json", "A.md"],
        "tool_error": False,
        "comparison": "Remote returned blob SHA compared to Git blob hash of actual local UTF-8 bytes.",
        "receipts": blob_receipts
    },
    "abandoned_command": {
        "command": "git diff --exit-code a6e2f47e6cfa52e249f4d648016cf9d324eccae9 -- docs/workstreams/research/AF-RES-070/streams/ripgrep/pre.json docs/workstreams/research/AF-RES-070/streams/ripgrep/A.md",
        "cwd": "/workspace/scratch/f1ffe17c302f/agentflow-open",
        "exit_code": 130,
        "reason": "No output while git command stayed running; explicitly interrupted. It is not evidence of a content mismatch. Replaced by direct GitHub blob comparison above."
    },
    "prior_validation_attempt": {
        "command": "python -B docs/workstreams/research/AF-RES-070/streams/ripgrep/validate_post.py",
        "exit_code": 1,
        "reason": "Validator initially assumed optional packet_doc_sections_by_candidate existed on every row. Diagnostic rows store their sections inside candidate evidence. Validator was corrected to compare the existing sealed structure; no sealed packet was changed."
    },
    "not_performed": ["ripgrep actual execution at historical commits", "original creation-body recovery for edited comment 791894916 (archive access returned HTTP 403)", "primary recommendation accuracy experiment", "global integration RESULT table and final result SHA review (ROOT responsibility)"]
}
(BASE / "validation-post.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"exit_code": 0, "checks_passed": len(checks), "counts": counts}, ensure_ascii=False))
