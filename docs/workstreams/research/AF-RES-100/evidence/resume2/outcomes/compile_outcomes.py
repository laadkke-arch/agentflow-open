#!/usr/bin/env python3
"""Compile post-seal attribution tables from fetched metadata and manual coding.

No primary judgment is changed. No third-party body is copied into deliverables.
Run after fetch_public_outcomes.py fetch; assessment.json is the explicit coding.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
CACHE = ROOT / "evidence/_cache/resume2-outcomes"
SEALED = "5d81bcbeb5f1248fc1dd2ce2d825cf6467353673"


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def clean_meta(value):
    return {k.lstrip("_"): v for k, v in value.items()}


def main():
    raw = json.loads((CACHE / "bundle.json").read_text())
    index = json.loads((OUT / "retrieval-index.json").read_text())
    coding = json.loads((OUT / "assessment.json").read_text())
    protocol = json.loads((ROOT / "protocol.json").read_text())
    primary_bytes = (ROOT / "judgments.jsonl").read_bytes()
    primary = [json.loads(line) for line in primary_bytes.splitlines()]
    manifest = [json.loads(line) for line in (OUT / "sources.jsonl").read_text().splitlines()]
    receipts = [x for x in manifest if x.get("kind") == "api_response"]
    qmap = {c["question_id"]: c["case_id"] for c in raw["cases"]}
    post_to_question = {qid: qid for qid in qmap}
    for c in raw["cases"]:
        for a in c["answers"]:
            post_to_question[a["answer_id"]] = c["question_id"]
    receipt_by_id = {r["source_id"]: r for r in receipts}
    checked = max(r["finished_utc"] for r in receipts)
    all_sources = []
    for receipt in receipts:
        path = urlparse(receipt["url"]).path.split("/")
        numeric = [int(x) for part in path for x in part.split(";") if x.isdigit()]
        qids = sorted({post_to_question[p] for p in numeric if p in post_to_question})
        caseids = [qmap[q] for q in qids]
        row = dict(receipt)
        row.update(q_numbers=["Q7"], question_ids=qids,
                   case_id=caseids[0] if len(caseids) == 1 else caseids,
                   direct_url=receipt["url"], fixed_url=None, checked_utc=receipt["finished_utc"],
                   author_publisher="Stack Exchange API / Stack Overflow public posts",
                   lineage="stackoverflow:api_snapshot:" + digest(receipt["url"]),
                   version="API 2.3; retrieved snapshot " + receipt["finished_utc"],
                   exact_section_payload="Exact HTTP JSON response bytes in the ignored cache; items and pagination metadata.",
                   body_sha256=receipt.get("sha256"), confirmed=receipt.get("status") == "success",
                   supports="Public current-post, revision, comment, or 30-day timeline inventory; route is recorded in direct_url.",
                   limits=["Snapshot is not an immutable historical website state.", "Deleted/private posts or comments may be unavailable.", "Acceptance and author prose do not establish same-version/input/output execution."],
                   count_minimum=False, count_group="post_outcome_attribution",
                   duplicate_reason="Post-seal attribution response; excluded from primary minimum source count. Revision filters can overlap while supplying separate body/editor metadata.",
                   research_phase="post_seal2")
        all_sources.append(row)

    cases = []
    for meta in index["cases"]:
        cid, qid = meta["case_id"], meta["question_id"]
        c = next(c for c in raw["cases"] if c["case_id"] == cid)
        assessment = coding[cid]
        p = next(p for p in protocol["cases"] if p["case_id"] == cid)
        observations = []
        for number, entry in enumerate(assessment["observations"], 1):
            kind, ident = entry["kind"], entry["id"]
            if kind == "comment":
                m = next(x for x in meta["comments"] if x["comment_id"] == ident)
                url = m["comment_url"]
            elif kind == "revision":
                m = next(x for x in meta["revisions"] if x["revision_guid"] == ident)
                url = m["revision_url"]
            elif kind == "answer":
                m = next(x for x in meta["answers"] if x["answer_id"] == ident)
                url = f"https://stackoverflow.com/a/{ident}"
            elif kind == "acceptance":
                m = next(x for x in meta["timeline"] if x.get("timeline_type") == "accepted_answer" and x.get("post_id") == ident)
                url = f"https://stackoverflow.com/posts/{qid}/timeline"
            else:
                raise ValueError(kind)
            obs = {"evidence_id": f"{cid}-E{number:02d}", **entry,
                   "url": url, "metadata": clean_meta(m)}
            if kind == "acceptance":
                obs["actor_limit"] = "Timeline owner denotes the answer owner; no accepting-actor identity or execution is inferred from this field."
            observations.append(obs)

        answer_history = []
        for a in meta["answers"]:
            aid = a["answer_id"]
            revs = sorted([r for r in meta["revisions"] if r.get("post_id") == aid],
                          key=lambda r: (r.get("creation_date", 0), r.get("revision_number", 0)))
            bodies = [r for r in revs if "body_sha256" in r]
            answer_history.append({"answer_id": aid, "current": clean_meta(a),
                                   "earliest_body_revision": clean_meta(bodies[0]) if bodies else None,
                                   "latest_body_revision": clean_meta(bodies[-1]) if bodies else None,
                                   "current_matches_latest_body": bool(bodies) and a.get("body_sha256") == bodies[-1].get("body_sha256"),
                                   "earliest_revision_equals_answer_creation": bool(bodies) and bodies[0].get("creation_date") == a.get("creation_date") and bodies[0].get("revision_number") == 1,
                                   "all_revisions": [clean_meta(r) for r in revs]})
        acceptances = [clean_meta(t) for t in meta["timeline"] if t.get("timeline_type") in {"accepted_answer", "unaccepted_answer"}]
        followup_roles = sorted({m["author_role"] for m in meta["comments"] + meta["answers"] +
                                [r for r in meta["revisions"] if r.get("revision_number", 0) > 1]})
        related_receipts = [r["source_id"] for r in all_sources if qid in r["question_ids"]]
        sealed = [{"packet_id": r["packet_id"], "reader_id": r["reader_id"], "complete": r["complete"],
                   "conditions": [{"id": x.get("id", x.get("condition_id")), "status": x["status"]} for x in r["conditions"]]}
                  for r in primary if r["case_id"] == cid]
        record = {"case_id": cid, "question_id": qid, "q_numbers": ["Q7"],
                  "question_url": f"https://stackoverflow.com/questions/{qid}",
                  "window_start_utc": meta["window_start_utc"], "window_end_utc": meta["window_end_utc"],
                  "original_question_url": p["r0_url"], "original_body_sha256": meta.get("original_body_sha256"),
                  "current_question": clean_meta(meta["question"]),
                  "current_equals_original_body": meta["current_equals_original_body"],
                  "current_accepted_answer_id": meta["question"].get("accepted_answer_id"),
                  "acceptance_events_within_window": acceptances,
                  "answers_current_count": len(meta["answers"]),
                  "answers_within_window_count": sum(a["within_30_days"] for a in meta["answers"]),
                  "comments_within_window_count": len(meta["comments"]),
                  "followup_author_roles": followup_roles or ["none_observed"],
                  "answer_history": answer_history,
                  "question_revision_history": [clean_meta(r) for r in sorted(meta["revisions"], key=lambda r: (r.get("creation_date", 0), r.get("revision_number", 0))) if r.get("post_id") == qid],
                  "comments_metadata": [clean_meta(x) for x in meta["comments"]],
                  "timeline_metadata": [clean_meta(x) for x in meta["timeline"]],
                  "observations": observations, "related_api_source_ids": related_receipts,
                  "assessment": {k: v for k, v in assessment.items() if k != "observations"},
                  "same_version_verified": False, "same_input_verified": False,
                  "same_output_verified": False, "same_version_input_output_execution_verified": False,
                  "verification_false_means": "Not established by the retrieved public record; it does not assert that the user used a different version or input.",
                  "sealed_comparison_read_only": sealed,
                  "comparison_status": "incomparable_adjacent_source_vacancy" if cid == "P3" else "primary_unchanged"}
        cases.append(record)

        # Record every current post, revision and comment, plus acceptance events,
        # as attributable source metadata without embedding the external text.
        entities = [("question", meta["question"])] + [("answer", a) for a in meta["answers"]] + [("revision", r) for r in meta["revisions"]] + [("comment", x) for x in meta["comments"]] + [("acceptance", t) for t in meta["timeline"] if t.get("timeline_type") in {"accepted_answer", "unaccepted_answer"}]
        for kind, m in entities:
            ident = m.get("revision_guid", m.get("comment_id", m.get("answer_id", m.get("post_id", qid))))
            if kind == "revision":
                direct = fixed = m["revision_url"]
            elif kind == "comment":
                direct, fixed = m["comment_url"], None
            elif kind == "answer":
                direct = f"https://stackoverflow.com/a/{m['answer_id']}"
                ah = next(x for x in answer_history if x["answer_id"] == m["answer_id"])
                fixed = (ah["latest_body_revision"] or {}).get("revision_url")
            elif kind == "question":
                direct = record["question_url"]
                bodyrevs = [r for r in record["question_revision_history"] if r.get("body_sha256")]
                fixed = bodyrevs[-1]["revision_url"] if bodyrevs else None
            else:
                direct, fixed = f"https://stackoverflow.com/posts/{qid}/timeline", None
            evidence = [o for o in observations if o["kind"] == kind and o["id"] == ident]
            supports = " ".join(o["paraphrase"] for o in evidence) or "Public post/revision/comment inventory and authorship metadata for this selected case."
            created = m.get("creation_utc")
            source_receipt = receipt_by_id[m["_source_id"]]
            metadata_receipt = receipt_by_id.get(m.get("_metadata_source_id"))
            entity = {"source_id": f"SO-PUB-{cid}-{kind.upper()}-{ident}", "kind": "public_attribution_entity",
                      "q_numbers": ["Q7"], "question_ids": [qid], "case_id": cid,
                      "direct_url": direct, "fixed_url": fixed,
                      "checked_utc": (metadata_receipt or source_receipt)["finished_utc"],
                      "author_publisher": {"publisher": "Stack Overflow / Stack Exchange API", "user_id": m.get("author_user_id"), "role": m.get("author_role")},
                      "lineage": f"stackoverflow:question:{qid}:{kind}:{ident}",
                      "version": {"revision_guid": m.get("revision_guid"), "revision_number": m.get("revision_number"), "created_utc": created, "retrieved_snapshot": source_receipt["finished_utc"]},
                      "exact_section_payload": {"entity_kind": kind, "post_id": m.get("post_id", m.get("answer_id", qid)), "comment_id": m.get("comment_id"), "revision_guid": m.get("revision_guid"), "api_response_source_id": m["_source_id"], "api_url": m["_api_url"], "editor_metadata_source_id": m.get("_metadata_source_id"), "body_format": "API body HTML" if m.get("body_sha256") else "metadata-only event"},
                      "body_sha256": m.get("body_sha256"), "confirmed": True,
                      "supports": supports,
                      "limits": ["Observed public statement or metadata; not independent verification of its technical claim.", "No same-version/input/output original execution is established.", "Comment/current-post links are mutable; cached response hashes preserve the retrieved snapshot."],
                      "count_minimum": False, "count_group": "post_outcome_attribution",
                      "duplicate_reason": "Post-seal evidence only; excluded from the primary evidence count. Current bodies and revision bodies may represent the same post content.",
                      "research_phase": "post_seal2", "metadata": clean_meta(m)}
            all_sources.append(entity)

    details = {"schema": "af-res-100-postseal-outcome-attribution-v1", "post_seal_commit": SEALED,
               "research_phase": "post_seal2", "q_numbers": ["Q7"], "checked_utc": checked,
               "compiled_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "primary_judgments_sha256_read_only": digest(primary_bytes),
               "method": {"window_days": 30, "window_boundaries": "Inclusive original creation through creation plus 30*86400 seconds; current answers and all API-returned revisions separately inventoried.",
                          "api_requests": len(receipts), "api_failures": sum(r["status"] != "success" for r in receipts),
                          "source_limits": "Public API only; no deleted/private material or comment revision histories. No external linked docs, demos, or older questions were opened.",
                          "reader_context": "Post-seal attribution in a reused machine-reader context following an interrupted duplicate packet-reading attempt; not independent human validation.",
                          "runtime": "No jq/Pandoc/R/Typst/Docker code was executed; no P4 render for AF-RES-096 or AF-RES-100.",
                          "primary_policy": "No sealed judgment, primary denominator, ranking, packet, or source selection is changed."},
               "cases": cases}
    (OUT / "evidence-details.json").write_text(json.dumps(details, ensure_ascii=False, indent=2) + "\n")
    with (OUT / "sources.jsonl").open("w", encoding="utf-8") as f:
        for source in all_sources:
            f.write(json.dumps(source, ensure_ascii=False) + "\n")

    fields = ["case_id", "question_id", "q_numbers", "question_url", "original_revision_url",
              "window_start_utc", "window_end_utc", "answers_current_count", "answers_within_30_days", "comments_within_30_days",
              "current_accepted_answer_id", "accepted_answer_url", "accepted_within_30_days", "accepted_utc",
              "followup_author_roles", "outcome_category", "thanks_or_acknowledgement", "questioner_execution_report",
              "same_version_verified", "same_version_detail", "same_input_verified", "same_input_detail",
              "same_output_verified", "same_output_detail", "same_version_input_output_execution_verified",
              "route_or_goal_difference", "question_edit_summary", "answer_change_summary", "original_requirement_status",
              "principal_followup_url", "evidence_details_file", "source_ids", "primary_comparison_status", "research_phase"]
    with (OUT / "outcomes.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for c in cases:
            accepted = [x for x in c["acceptance_events_within_window"] if x["timeline_type"] == "accepted_answer"]
            aid = c["current_accepted_answer_id"]
            a = c["assessment"]
            row = {k: c.get(k, "") for k in fields}
            row.update(q_numbers="Q7", original_revision_url=c["original_question_url"],
                       answers_within_30_days=c["answers_within_window_count"], comments_within_30_days=c["comments_within_window_count"],
                       accepted_answer_url=f"https://stackoverflow.com/a/{aid}" if aid else "",
                       accepted_within_30_days=bool(accepted), accepted_utc=";".join(x["creation_utc"] for x in accepted),
                       followup_author_roles=";".join(c["followup_author_roles"]),
                       principal_followup_url=(f"https://stackoverflow.com/a/{aid}" if aid else c["observations"][-1]["url"] if c["observations"] else c["question_url"]),
                       evidence_details_file="evidence-details.json", source_ids=";".join(c["related_api_source_ids"]),
                       primary_comparison_status=c["comparison_status"], research_phase="post_seal2")
            for k in fields:
                if k in a:
                    row[k] = a[k]
            writer.writerow(row)

    lines = ["# AF-RES-100: public followup attribution after seal2", "",
             "This report covers all eight preregistered cases. It is separate attribution evidence after commit `" + SEALED + "`; it does not change the sealed packet judgments, source rankings, or comparison denominators.", "",
             "## What the public record establishes", "",
             "The API returned eight questions, five answers across four questions, 29 revision records, and 18 comments in the specified 30-day windows. Three answers were accepted within those windows. No case supplies a verified execution tying the same original tool versions, complete inputs, and required outputs together. Author reports of failure, partial diagnostics, existing helper use, and a working alternative are recorded separately below.", "",
             "| Case | Current accepted answer | Questioner followup category | Same version/input/output execution |",
             "| --- | --- | --- | --- |"]
    for c in cases:
        aid = c["current_accepted_answer_id"]
        link = f"[{aid}](https://stackoverflow.com/a/{aid})" if aid else "None"
        lines.append(f"| [{c['case_id']}]({c['question_url']}) | {link} | {c['assessment']['questioner_execution_report']} | Not established |")
    lines += ["", "Acceptance is a platform event. Thanks or an assertion that a workaround works is a user report. An answerer's example output is not a questioner's execution. The false verification fields in the CSV mean evidence was not established, rather than proving different versions or inputs were used.", "",
              "## Retrieval and attribution", "",
              "The window is inclusive from each original question's creation timestamp through exactly 30 days later. Current posts and all returned answer/question revisions are also retained as metadata, with explicit window flags. The earliest body-bearing answer revisions are compared with later revisions and current answers. The source ledger preserves exact API URLs, UTC retrieval times, response hashes, revision IDs, public user roles, and fixed revision URLs where available. The initial blinded revision filter omitted editors; a separate ordinary revision request supplies editor metadata after the seal.", "",
              f"There were {len(receipts)} API requests, {sum(r['status'] != 'success' for r in receipts)} recorded failures, and no returned backoff instructions. Pagination completed for every response. No questioners were contacted; no linked old questions, external demos, or documentation pages were followed. No subject runtime was executed, including no P4 render. Deleted/private posts and deleted comments are outside the API-visible record, and comments have no retrieved edit history.", "",
              "This was a reused machine-reader context following an interrupted duplicate reading attempt. It is not independent human confirmation. Original full bodies are held only in the ignored cache; the committed deliverables contain metadata, hashes, links, and short paraphrases.", ""]
    for c in cases:
        a = c["assessment"]
        lines += [f"## {c['case_id']} — [{c['question_id']}]({c['question_url']})", "",
                  f"Window: {c['window_start_utc']} through {c['window_end_utc']}. Current answers: {c['answers_current_count']}; comments in window: {c['comments_within_window_count']}.", "",
                  a["public_answer_summary"], "", a["question_edit_summary"], "", a["answer_change_summary"], "",
                  "**Attribution and execution.** " + a["thanks_or_acknowledgement"] + " " + a["execution_detail"], "",
                  "**Goal and route.** " + a["route_or_goal_difference"], "",
                  "**Verification limits.** " + a["same_version_detail"] + " " + a["same_input_detail"] + " " + a["same_output_detail"], "",
                  "**Relation to seal2.** " + a["seal2_comparison"], ""]
        accepted = [x for x in c["acceptance_events_within_window"] if x["timeline_type"] == "accepted_answer"]
        if accepted:
            lines += ["Acceptance timestamp: " + "; ".join(x["creation_utc"] for x in accepted) + ". The timeline owner field refers to the answer owner, not an independently verified accepting actor.", ""]
        if c["observations"]:
            lines += ["Evidence:", ""]
            for o in c["observations"]:
                m = o["metadata"]
                lines.append(f"- [{o['evidence_id']}]({o['url']}) — {m.get('creation_utc', 'timestamp unknown')}; {m.get('author_role', 'role unknown')}. {o['paraphrase']}")
            lines.append("")
        else:
            lines += ["No followup statement was returned. The current-post, answer-list, comment-list and timeline API receipt IDs in the CSV and evidence details document this empty public result; absence is not coded as a technical failure.", ""]
    lines += ["## Files and reproduction", "",
              "- [outcomes.csv](outcomes.csv): one stable row for each of the eight cases, with links, windows, roles, acceptance and verification fields.",
              "- [evidence-details.json](evidence-details.json): per-case observations, exact body hashes, revision histories, author roles, and read-only sealed comparisons.",
              "- [sources.jsonl](sources.jsonl): unified source-ledger fields plus exact API receipt details. All rows use Q7, post_seal2, count_minimum=false and count_group=post_outcome_attribution.",
              "- [retrieval-index.json](retrieval-index.json): sanitized automatic metadata inventory.",
              "- [assessment.json](assessment.json): explicit manual coding and paraphrases.",
              "- [fetch_public_outcomes.py](fetch_public_outcomes.py) and [compile_outcomes.py](compile_outcomes.py): reproducible fetching, inspection, and compilation.", "",
              "Run the fetch script with `fetch`, inspect a case with `read --case J2 --part answers` (or questions/comments/timeline), then run the compilation script. Existing cached successful URLs are reused. API backoff and Retry-After are respected; failures are logged. New fetching does not run submitted code or mutate primary judgments.", ""]
    (OUT / "report.md").write_text("\n".join(lines), encoding="utf-8")
    assert (ROOT / "judgments.jsonl").read_bytes() == primary_bytes
    required = "source_id q_numbers case_id direct_url fixed_url checked_utc author_publisher lineage version exact_section_payload body_sha256 confirmed supports limits count_minimum count_group duplicate_reason research_phase".split()
    assert len(cases) == 8 and len({c["case_id"] for c in cases}) == 8
    assert all(set(required) <= set(s) for s in all_sources)
    assert all(s["q_numbers"] == ["Q7"] and s["count_minimum"] is False and s["count_group"] == "post_outcome_attribution" for s in all_sources)
    assert all(digest((ROOT / r["cache_path"]).read_bytes()) == r["sha256"] for r in receipts)
    assert all(a["current_matches_latest_body"] and a["earliest_revision_equals_answer_creation"] for c in cases for a in c["answer_history"])
    assert all(m["within_30_days"] for c in cases for m in c["comments_metadata"])
    validation = {"checked_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                  "cases": len(cases), "api_receipts": len(receipts), "source_rows": len(all_sources),
                  "accepted_cases": sum(c["current_accepted_answer_id"] is not None for c in cases),
                  "verified_original_executions": sum(c["same_version_input_output_execution_verified"] for c in cases),
                  "all_response_hashes_match": True, "all_common_source_fields_present": True,
                  "all_comment_records_in_window": True, "all_five_answer_revision_chains_match_current": True,
                  "primary_judgments_unchanged": True, "primary_judgments_sha256": digest(primary_bytes),
                  "artifact_sha256": {name: digest((OUT / name).read_bytes()) for name in ("outcomes.csv", "evidence-details.json", "sources.jsonl", "report.md")}}
    (OUT / "validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
