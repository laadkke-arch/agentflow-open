#!/usr/bin/env python3
"""Assemble AF-RES-086's already-read evidence; performs no network access."""
from pathlib import Path
import csv
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
STREAMS = ("python", "r", "incidents", "preservation")

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def save_jsonl(path, values):
    path.write_text("".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values))

sources = []
counts = {}
for stream in STREAMS:
    rows = read_jsonl(ROOT / "streams" / stream / "sources.jsonl")
    for old in rows:
        row = dict(old)
        row["id"] = old.get("id", old.get("source_id"))
        row["stream"] = stream
        row["Q"] = old.get("Q", old.get("questions", []))
        row["version"] = old.get("version", old.get("version_or_section", ""))
        row["section"] = old.get("section", old.get("version_or_section", ""))
        row["direct_read"] = True
        row["countable_original"] = old.get("countable_original", old.get("primary_count_eligible", old.get("counts_original", False)))
        receipt = json.loads((ROOT / old["receipt_path"]).read_text())
        if not isinstance(receipt, dict):
            receipt = {}
        row["http_status"] = old.get("http_status", old.get("access_status")) or receipt.get("status") or receipt.get("http_status")
        row["request_started_utc"] = receipt.get("requested_at_utc", receipt.get("requested_utc", receipt.get("read_utc")))
        row["response_received_utc"] = receipt.get("finished_at_utc", receipt.get("completed_utc"))
        row["read_utc_basis"] = "Original stream retrieval timestamp retained. Use request_started_utc/response_received_utc for the measured retrieval interval; archived capture UTC and publisher event UTC are separate. Semantic reading was performed in this session, not timed independently."
        row["direct_sha256"] = old.get("direct_sha256", old.get("download_sha256"))
        row["publisher_hash"] = old.get("publisher_hash")
        row["transport_body_bytes"] = old.get("bytes", old.get("response_bytes"))
        row["minimum_count_note"] = "Same work/event grouped by lineage_id; discovery, failures, empty history and duplicate mirrors excluded."
        if stream == "r":
            candidates = [f"streams/r/evidence/{row['id']}.extract.{suffix}" for suffix in ("json", "txt")]
            row["excerpt_path"] = next(path for path in candidates if (ROOT / path).exists())
        sources.append(row)
    eligible = [r for r in sources if r["stream"] == stream and r["countable_original"]]
    counts[stream] = {"rows": len(rows), "eligible_original_rows": len(eligible), "eligible_lineages": sorted({r["lineage_id"] for r in eligible})}

assert len({r["id"] for r in sources}) == len(sources)
save_jsonl(ROOT / "sources.jsonl", sources)
by_id = {r["id"]: r for r in sources}

claims = []
fields = ["claim_id", "case_id", "claim_type", "owner_or_observer", "reader", "claim", "status", "source_ids", "url", "section", "retention_duration", "limitations"]
for stream in ("python", "r"):
    with (ROOT / "streams" / stream / "claims.csv").open() as file:
        for old in csv.DictReader(file):
            ids = old.get("source_id", "")
            first = ids.split(";")[0]
            source = by_id.get(first, {})
            typ = old.get("claim_type", old.get("owner_or_assumption", ""))
            claims.append({
                "claim_id": old["claim_id"], "case_id": old["case_id"], "claim_type": typ,
                "owner_or_observer": old.get("owner", "project publisher" if typ == "owner_promise" else "AF-RES-086 researcher"),
                "reader": old.get("reader", "documentation reader"), "claim": old["claim"],
                "status": old.get("status", "research-assumption" if typ == "research_assumption" else "confirmed-limited"),
                "source_ids": ids, "url": old.get("url", source.get("url", "")),
                "section": old.get("section", old.get("locator", "")),
                "retention_duration": old.get("retention_duration", "미기재; 연구 관측창은 보존 약속이 아님"),
                "limitations": old.get("limitations", old.get("limitation", "")),
            })

claim_sources = defaultdict(list)
for source in sources:
    for claim in source.get("claim_ids", []):
        claim_sources[claim].append(source)
existing = {c["claim_id"] for c in claims}
for claim, rows in sorted(claim_sources.items()):
    if claim in existing:
        continue
    # These are observation group labels, never new owner promises.
    observations = list(dict.fromkeys(r["observed"] for r in rows))
    claims.append({
        "claim_id": claim, "case_id": ";".join(sorted({c for r in rows for c in r.get("cases", [])})),
        "claim_type": "research_observation_group", "owner_or_observer": "AF-RES-086 researcher; primary observer stated per source",
        "reader": "research reviewer", "claim": " / ".join(observations),
        "status": "scope-limited; see each source support_refute and limitations",
        "source_ids": ";".join(r["id"] for r in rows), "url": rows[0]["url"],
        "section": "sources.jsonl linked rows; not an independent source", "retention_duration": "not applicable",
        "limitations": "Grouped observations retain failures and unknowns. No additional owner promise or independent lineage is inferred.",
    })
with (ROOT / "claims.csv").open("w", newline="") as file:
    writer = csv.DictWriter(file, fields)
    writer.writeheader()
    writer.writerows(claims)

routes = []
for stream in ("python", "r"):
    for row in read_jsonl(ROOT / "streams" / stream / "routes.jsonl"):
        row["stream"] = stream
        row["retrieval_intervals"] = [{"source_id": sid, "request_started_utc": by_id[sid].get("request_started_utc"), "response_received_utc": by_id[sid].get("response_received_utc")} for sid in row.get("source_ids", [])]
        routes.append(row)
assert len({r["route_id"] for r in routes}) == len(routes)
save_jsonl(ROOT / "routes.jsonl", routes)
(ROOT / "incidents.csv").write_bytes((ROOT / "streams/incidents/incidents.csv").read_bytes())

eligible = [r for r in sources if r["countable_original"]]
lineages = sorted({r["lineage_id"] for r in eligible})
unique_url_version = {(r["url"], r["version"]) for r in eligible}
payload_groups = defaultdict(list)
for row in eligible:
    digest = row.get("direct_sha256") or row.get("snapshot_sha256") or "no-comparable-payload:" + row["id"]
    payload_groups[digest].append(row["id"])
save_json(ROOT / "evidence/source-audit.json", {
    "source_rows": len(sources), "eligible_original_rows": len(eligible),
    "unique_eligible_url_version_pairs": len(unique_url_version), "conservative_lineage_count": len(lineages),
    "minimum_originals_after_equal_payload_dedup": len(payload_groups),
    "equal_payload_groups_excluded_from_extra_minimum_count": [ids for ids in payload_groups.values() if len(ids) > 1],
    "lineages": lineages, "by_stream": counts, "minimum_originals": 24, "minimum_lineages": 20,
    "passes_quantity_gate": len(payload_groups) >= 24 and len(lineages) >= 20,
    "lineage_rule": "A project's fixed README/release, all builds, artifacts and responses stay one consumer lineage. An incident and its linked logs/comments stay one incident lineage. Multiple versions of one archived work stay one lineage. Platform policies are separately grouped, not split by help page.",
})

py = json.loads((ROOT / "streams/python/costs.json").read_text())
r = json.loads((ROOT / "streams/r/summary.json").read_text())
inc = json.loads((ROOT / "streams/incidents/COSTS.json").read_text())
pr = json.loads((ROOT / "streams/preservation/costs.json").read_text())
costs = {
    "instrumented_logical_http_gets": py["logical_gets"] + r["requests_with_receipts"] + inc["direct_http_logical_get_calls"] + pr["instrumented_logical_gets"],
    "instrumented_response_body_bytes": py["response_body_bytes"] + r["download_bytes"] + inc["direct_http_body_bytes"] + pr["instrumented_response_body_bytes"],
    "incident_github_connector_calls_separate": inc["github_connector_calls"],
    "preservation_preinstrument_exploratory_gets_separate": 3,
    "preservation_archive_download_bytes_subset": pr["downloaded_archive_bytes"],
    "python": py, "r": r, "incidents": inc, "preservation": pr,
    "not_measured": ["connector wire bytes", "search-tool response bytes", "headers/TLS", "automatic redirect exchanges", "publisher internal operations", "human reading minutes", "money"],
    "boundary": "Research collection costs, not a benchmark or per-user requirement. Re-reads of local snapshots transfer zero network bytes. Search calls and remote repository commits are separate from source retrieval; unknown quantities are null, not zero.",
}
save_json(ROOT / "costs.json", costs)

slots = [
    ("P3-STABLE", "P3", "https://cibuildwheel.pypa.io/en/stable/options/#enable", "PY-P3-STABLE-NOW", False),
    ("P3-LEGACY", "P3", "https://cibuildwheel.pypa.io/en/1.x/", "PY-P3-LEGACY-NOW", True),
    ("P3-TAG", "P3", "https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable", "PY-P3-TAG-NOW", True),
    ("P1-LATEST", "P1", "https://bandersnatch.readthedocs.io/en/latest/", "PY-P1-LATEST-NOW", False),
    ("P1-NAMED", "P1", "https://bandersnatch.readthedocs.io/en/7.0.1/", "PY-P1-NAMED-NOW", False),
    ("R1-ROOT", "R1", "https://archive.r-lib.org/", "R1-CURRENT-ROOT", False),
    ("R1-LEAF", "R1", "https://archive.r-lib.org/reference/archive_read.html", "R1-CURRENT-LEAF", False),
    ("R2-ROOT", "R2", "https://asciicast.r-lib.org/", "R2-CURRENT-ROOT", True),
    ("R2-LEAF", "R2", "https://asciicast.r-lib.org/articles/asciicast-demo.html", "R2-CURRENT-LEAF", True),
]
slot_rows = []
for slot, case, url, sid, current_target in slots:
    source = by_id[sid]
    receipt = json.loads((ROOT / source["receipt_path"]).read_text())
    status = source.get("http_status") or receipt.get("status") or receipt.get("status_code") or receipt.get("http_status")
    slot_rows.append({"slot_id": slot, "case_id": case, "url": url, "current_source_id": sid,
                      "current_http_status": status, "current_target_version_identified": current_target,
                      "main_historical_target_identified": False, "main_historical_status": "unconfirmed", "historical_failure_proved": False})
save_json(ROOT / "evidence/route-denominators.json", {
    "slots": slot_rows, "fixed_route_denominator": 9,
    "current_200": sum(r["current_http_status"] == 200 for r in slot_rows),
    "current_target_version_identified": sum(r["current_target_version_identified"] for r in slot_rows),
    "main_historical_target_identified": 0, "main_historical_unknown": 9,
    "owner_two_condition_projects_original": {"numerator": 1, "denominator": 6, "source": "AF-RES-082 fixed predecessor"},
    "owner_two_condition_projects_selected": {"numerator": 1, "denominator": 4},
    "joint_historical_confirmation": {"numerator": 0, "denominator": 1, "unknown": 1, "refuted": 0},
    "other_cases_joint_confirmation": {"numerator": 0, "denominator": 0, "meaning": "산출 불가: 두 번째 원 약속이 확인되지 않음"},
    "rtd_generation_success": {"numerator": 4, "denominator": 4, "run_ids": [30298914, 30298916, 30298915, 30720077], "scope": "Selected four runs with raw generator logs analyzed. Additional same-source latest30298913 appears in metadata query and is not silently added to this denominator."},
    "rtd_separately_identified_publish_transaction": {"numerator": 0, "denominator": 4, "unknown": 4},
    "pages_provider_reported_success_directly_read": {"numerator": 0, "denominator": 2, "unknown_prior_sequence": 2, "deployment_ids": [2328795124, 1283145596]},
    "do_not_combine": "RTD build and Pages deployment denominators have different units. Neither current 200 nor an inactive status is an independent historical publish-success report.",
})
print(json.dumps({"sources": len(sources), "eligible_originals": len(eligible), "lineages": len(lineages), "claims": len(claims), "routes": len(routes), "GETs": costs["instrumented_logical_http_gets"], "body_bytes": costs["instrumented_response_body_bytes"]}))
