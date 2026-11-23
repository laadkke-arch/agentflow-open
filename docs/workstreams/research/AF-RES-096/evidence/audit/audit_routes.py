"""Independent route-accounting audit; does not read root seal_routes.py.

Input: sealed protocol/frame manifest, raw search/exposure/access/judgment logs.
Source bytes are used only for hashes and line-bound checks and never printed.
All writes, including judgment observation snapshots, stay in evidence/audit/.
No answers, comments, acceptance metadata, or outcome files are opened.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
REPO = BASE.parents[3]
SEAL1 = "abf2bc2ac9303cb96e6109eba107684e5f858a42"


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def read_json(path):
    return json.loads(path.read_bytes())


def read_jsonl(path):
    return [json.loads(line) for line in path.read_bytes().splitlines() if line]


def instant(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def run():
    started = utc()
    problems = []
    warnings = []
    unlogged_ranges = []

    def check(value, code, row=None, detail=None):
        if not value:
            problems.append({"check": code, "row": row, "detail": detail})

    def warn(code, row=None, detail=None):
        warnings.append({"check": code, "row": row, "detail": detail})

    protocol = read_json(BASE / "protocol.json")
    manifest = read_json(BASE / "evidence/seal1-files.json")
    receipt = read_json(BASE / "evidence/seal1-receipt.json")
    check(receipt["remote_sha"] == SEAL1, "seal1_receipt_identity")
    seal_verified = instant(receipt["verified_utc"])
    seal1_results = []
    for record in manifest:
        rel = record["path"]
        path = REPO / rel
        raw = path.read_bytes()
        historical = subprocess.run(
            ["git", "show", f"{SEAL1}:{rel}"], cwd=REPO,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        matches_current = digest(raw) == record["sha256"]
        matches_commit = historical.returncode == 0 and historical.stdout == raw
        normalization = None
        content_matches_commit = matches_commit
        if historical.returncode == 0 and not matches_commit and path.suffix == ".csv":
            attributes = subprocess.run(
                ["git", "check-attr", "-z", "text", "eol", "--", rel],
                cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            parts = attributes.stdout.decode().split("\0")
            settings = {parts[i + 1]: parts[i + 2] for i in range(0, len(parts) - 2, 3)}
            eol_equivalent = raw.replace(b"\r\n", b"\n") == historical.stdout
            if settings.get("eol") == "lf" and settings.get("text") in {"auto", "set"} and eol_equivalent:
                content_matches_commit = True
                normalization = {
                    "conversion": "CRLF worktree to LF git blob",
                    "git_attributes": settings,
                    "worktree_crlf_count": raw.count(b"\r\n"),
                    "commit_crlf_count": historical.stdout.count(b"\r\n"),
                    "worktree_sha256": digest(raw),
                    "commit_sha256": digest(historical.stdout),
                    "equivalent_only_after_configured_eol_normalization": True,
                }
                warn("seal1_csv_git_eol_normalization", rel, normalization)
        check(matches_current, "seal1_manifest_current_hash", rel)
        check(len(raw) == record["bytes"], "seal1_manifest_current_bytes", rel)
        check(content_matches_commit, "seal1_commit_content_unchanged", rel)
        if "blob_sha" in record:
            actual_blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            check(actual_blob == record["blob_sha"], "seal1_git_blob_hash", rel)
        seal1_results.append({"path": rel, "sha256": digest(raw),
                              "commit_sha256": digest(historical.stdout) if historical.returncode == 0 else None,
                              "manifest_matches": matches_current,
                              "commit_exact_bytes_match": matches_commit,
                              "commit_content_unchanged": content_matches_commit,
                              "git_eol_normalization": normalization})

    amendments = read_json(BASE / "evidence/preseal-amendments.json")
    for index, change in enumerate(amendments, 1):
        check(all(k in change for k in ("old", "new", "utc", "reason")), "amendment_old_new_reason", index)
        check(instant(change["utc"]) < seal_verified, "amendment_before_seal1", index)

    events = read_jsonl(BASE / "evidence/search-events.jsonl")
    searches = [x for x in events if x["event"] == "search"]
    check(len(searches) == 32, "global_searches_32")
    for event in searches:
        check(instant(event["started_utc"]) >= seal_verified, "search_after_remote_seal1", f'{event["case_id"]}-{event["route"]}-q{event["query_number"]}')

    catalog = {entry["file_id"]: entry for entry in read_jsonl(BASE / "corpus-files.jsonl")}
    observation_path = HERE / "judgment-observations.jsonl"
    old_observations = read_jsonl(observation_path) if observation_path.exists() else []
    previous_by_route = {r["route_key"]: r for r in old_observations}
    observations = []
    fingerprints = []
    judgment_changes = []
    snapshots_dir = HERE / "judgment-snapshots"
    snapshots_dir.mkdir(exist_ok=True)
    route_results = []
    judgments = {}
    exposures = {}
    first_times = {}
    route_finish_times = {}
    status_counter = collections.Counter()

    for case in protocol["cases"]:
        case_id = case["case_id"]
        required_conditions = [c["id"] for c in case["conditions"]]
        check(len(set(required_conditions)) == len(required_conditions), "protocol_unique_conditions", case_id)
        for route in case["route_order"]:
            key = f"{case_id}-{route}"
            folder = BASE / "evidence/routes" / key
            exposure = read_json(folder / "exposure.json")
            accesses = read_jsonl(folder / "access.jsonl")
            exposure_ids = [s["file_id"] for s in exposure["slots"] if not s["empty"]]
            slot_by_id = {s["file_id"]: s for s in exposure["slots"] if not s["empty"]}
            exposures[key] = exposure
            attempts = [e for e in accesses if e["event"] == "body_attempt"]
            navigations = [e for e in accesses if e["event"] == "section_navigation"]
            route_searches = [s for s in searches if (s["case_id"], s["route"]) == (case_id, route)]
            check(len(route_searches) == 2, "two_search_events", key)
            check(sorted(s["query_number"] for s in route_searches) == [1, 2], "two_distinct_queries", key)
            check(sum(s["charged_searches"] for s in route_searches) == 2, "two_search_charges", key)
            check(len(exposure["slots"]) == 4, "four_exposure_slots", key)
            check(len(attempts) <= 4, "at_most_four_body_attempt_events", key, len(attempts))
            check(sum(e["charged_attempts"] for e in attempts) <= 4,
                  "at_most_four_body_attempt_charges", key,
                  sum(e["charged_attempts"] for e in attempts))
            check(sum(e["charged_attempts"] for e in accesses) <= 4,
                  "all_access_charge_budget", key,
                  sum(e["charged_attempts"] for e in accesses))
            check({e["event"] for e in accesses} <= {"body_attempt", "section_navigation"}, "known_access_event_types", key)
            check([e["file_id"] for e in attempts] == exposure_ids,
                  "open_all_nonempty_slots_in_exact_order", key,
                  {"attempt_ids": [e["file_id"] for e in attempts], "exposed_ids": exposure_ids})
            check([e["attempt_number"] for e in attempts] == list(range(1, len(attempts) + 1)), "attempt_number_sequence", key)
            body_lines = {}
            opened = set()
            open_time = {}
            nav_ranges = collections.defaultdict(list)
            for index, event in enumerate(accesses):
                check(event["case_id"] == case_id and event["route"] == route, "access_route_identity", key)
                fid = event["file_id"]
                check(fid in slot_by_id, "access_file_exposed_in_this_route", key, fid)
                if event["event"] == "body_attempt":
                    check(event["charged_attempts"] == 1, "each_attempt_including_failure_charged", key, fid)
                    check(event["slot"] == slot_by_id.get(fid, {}).get("slot"), "attempt_slot_order", key, fid)
                    check(event["url"] == catalog.get(fid, {}).get("url"), "attempt_original_url", key, fid)
                    check(instant(event["started_utc"]) >= instant(exposure["created_utc"]), "attempt_after_exposure", key, fid)
                    check(instant(event["finished_utc"]) >= instant(event["started_utc"]), "attempt_finish_after_start", key, fid)
                    status_counter[event["status"]] += 1
                    if event["status"] == "success":
                        cache_path = BASE / event["opened_body"]
                        raw = cache_path.read_bytes()
                        check(digest(raw) == event["body_sha256"] == catalog[fid]["sha256"], "opened_corpus_body_hash", key, fid)
                        check(len(raw) == event["bytes"], "opened_body_bytes", key, fid)
                        lines = raw.decode("utf-8").splitlines()
                        check(len(lines) == event["line_count"], "opened_body_line_count", key, fid)
                        body_lines[fid] = lines
                        opened.add(fid)
                        open_time[fid] = instant(event["finished_utc"])
                elif event["event"] == "section_navigation":
                    check(event["charged_attempts"] == 0, "same_open_file_navigation_charge", key, fid)
                    check(fid in opened and event["already_opened_file"] is True, "navigation_after_route_open", key, fid)
                    if fid not in body_lines:
                        continue
                    check(instant(event["utc"]) >= open_time[fid], "navigation_timestamp_after_open", key, fid)
                    lo, hi = event["start_line"], event["end_line"]
                    check(1 <= lo <= hi <= len(body_lines[fid]), "navigation_line_bounds", key, {"file_id": fid, "start": lo, "end": hi})
                    section = "\n".join(body_lines[fid][lo - 1:hi])
                    check(digest(section.encode()) == event["section_sha256"], "navigation_section_hash", key, {"file_id": fid, "start": lo, "end": hi})
                    nav_ranges[fid].append((lo, hi))

            judgment_path = folder / "judgment.json"
            stat_before = judgment_path.stat()
            judgment_raw = judgment_path.read_bytes()
            stat_after = judgment_path.stat()
            check(stat_before.st_mtime_ns == stat_after.st_mtime_ns and stat_before.st_size == stat_after.st_size,
                  "stable_judgment_read", key)
            judgment = json.loads(judgment_raw)
            judgments[key] = judgment
            judgment_hash = digest(judgment_raw)
            snapshot_name = f"{key}-{judgment_hash}.json"
            snapshot = snapshots_dir / snapshot_name
            if not snapshot.exists():
                snapshot.write_bytes(judgment_raw)
            else:
                check(snapshot.read_bytes() == judgment_raw, "judgment_snapshot_immutable", key)
            previous = previous_by_route.get(key)
            observed = {
                "route_key": key, "observed_utc": utc(),
                "judgment_sha256": judgment_hash,
                "filesystem_mtime_utc": dt.datetime.fromtimestamp(stat_after.st_mtime, dt.timezone.utc).isoformat(),
                "filesystem_mtime_ns": stat_after.st_mtime_ns,
                "declared_read_completed_utc": judgment.get("read_completed_utc"),
                "declared_judgment_finalized_utc": judgment.get("judgment_finalized_utc"),
                "snapshot_path": str(snapshot.relative_to(BASE)),
                "judgment": judgment.get("judgment"),
                "previous_observed_sha256": previous["judgment_sha256"] if previous else None,
                "changed_since_prior_audit": previous is not None and previous["judgment_sha256"] != judgment_hash,
            }
            observations.append(observed)
            fingerprints.append(observed)
            if observed["changed_since_prior_audit"]:
                judgment_changes.append(observed)
                check((BASE / previous["snapshot_path"]).exists(), "prior_judgment_snapshot_retained", key)
            check(judgment["case_id"] == case_id and judgment["route"] == route, "judgment_route_identity", key)
            check(bool(judgment.get("memory_exposure")), "memory_exposure_declared", key)
            check(bool(judgment.get("stop_reason")), "stop_reason_recorded", key)
            check(bool(judgment.get("limitations")), "limitations_recorded", key)
            last_access = max(instant(e.get("finished_utc") or e.get("utc")) for e in accesses)
            completed = instant(judgment["read_completed_utc"])
            finalized = instant(judgment.get("judgment_finalized_utc") or judgment["read_completed_utc"])
            check(finalized >= last_access, "judgment_finalization_after_accesses", key,
                  {"read_completed_utc": judgment["read_completed_utc"],
                   "judgment_finalized_utc": judgment.get("judgment_finalized_utc"),
                   "last_access": last_access.isoformat()})
            if completed < last_access and judgment.get("judgment_finalized_utc"):
                warn("documented_same_file_review_after_initial_read_completion", key,
                     {"initial_read_completed_utc": judgment["read_completed_utc"],
                      "last_access_utc": last_access.isoformat(),
                      "judgment_finalized_utc": judgment["judgment_finalized_utc"],
                      "classification": "Initial completion preserved; later in-route same-file review accounted separately. No extra body source or answer access is inferred."})
            first_times[key] = instant(attempts[0]["started_utc"])
            route_finish_times[key] = completed
            condition_rows = judgment["condition_evidence"]
            condition_ids = [c["condition_id"] for c in condition_rows]
            check(len(condition_ids) == len(set(condition_ids)), "unique_condition_rows", key)
            check(set(condition_ids) == set(required_conditions), "all_and_only_explicit_conditions", key,
                  {"expected": required_conditions, "observed": condition_ids})
            used = set(judgment.get("used_file_ids", []))
            condition_used = {fid for c in condition_rows for fid in c["evidence_file_ids"]}
            check(used <= opened, "used_files_opened_in_this_route", key, sorted(used - opened))
            check(used <= set(exposure_ids), "used_files_exposed_in_this_route", key, sorted(used - set(exposure_ids)))
            check(condition_used <= opened, "condition_files_opened_in_this_route", key, sorted(condition_used - opened))
            check(condition_used <= used, "condition_ids_declared_as_used", key, sorted(condition_used - used))
            returned = judgment["returned_sources"]
            returned_ids = {r["file_id"] for r in returned}
            returned_urls = {r["url"] for r in returned}
            check(len(returned) <= 2 and len(returned_urls) <= 2, "maximum_two_returned_links", key, len(returned))
            check(len(returned_ids) == len(returned), "unique_returned_source_files", key)
            check(returned_ids <= opened, "returned_files_opened_in_this_route", key, sorted(returned_ids - opened))
            check(returned_ids <= used, "returned_files_declared_as_used", key, sorted(returned_ids - used))
            if "opened_file_ids" in judgment:
                check(set(judgment["opened_file_ids"]) == opened, "declared_opened_files_match_accesses", key)
            complete = judgment["judgment"] == "완결"
            if complete:
                check(used <= returned_ids, "complete_uses_only_returned_sources", key, sorted(used - returned_ids))
                check(all(c["status"].startswith("supported") for c in condition_rows), "complete_has_supported_condition_labels", key)
            elif used - returned_ids:
                warn("noncomplete_diagnostic_sources_beyond_returned_two", key,
                     {"extra_used_ids": sorted(used - returned_ids),
                      "classification": "All extra sources are route-opened diagnostic evidence, not a returned-link overflow; semantic sufficiency remains reviewer judgment."})

            def inspect_range(fid, lo, hi, context):
                if fid not in body_lines:
                    check(False, "cited_range_source_opened", key, fid)
                    return
                check(1 <= lo <= hi <= len(body_lines[fid]), "cited_range_within_source", key,
                      {"file_id": fid, "start": lo, "end": hi, "context": context})
                covered = set()
                for left, right in nav_ranges[fid]:
                    covered.update(range(max(lo, left), min(hi, right) + 1))
                if len(covered) < hi - lo + 1:
                    unlogged_ranges.append({"route_key": key, "file_id": fid,
                                            "start": lo, "end": hi, "context": context,
                                            "missing_navigation_lines": hi - lo + 1 - len(covered),
                                            "body_opened": True})

            for source in returned:
                fid = source["file_id"]
                check(source["url"] == catalog[fid]["url"], "returned_url_matches_file", key, fid)
                for section in source["sections"]:
                    inspect_range(fid, section["start"], section["end"], "returned_source")
            for condition in condition_rows:
                for section_range in condition.get("section_ranges", []):
                    match = re.fullmatch(r"(?:(?P<fid>[A-Z]+-\d+):)?(?P<lo>\d+)-(?P<hi>\d+)", section_range)
                    if not match:
                        warn("unparsed_condition_section_range", key,
                             {"condition_id": condition["condition_id"], "range": section_range})
                        continue
                    fid = match["fid"]
                    if not fid and len(condition["evidence_file_ids"]) == 1:
                        fid = condition["evidence_file_ids"][0]
                    if not fid:
                        warn("ambiguous_unqualified_condition_range", key,
                             {"condition_id": condition["condition_id"], "range": section_range})
                        continue
                    check(fid in condition["evidence_file_ids"], "range_file_in_condition_evidence", key, fid)
                    inspect_range(fid, int(match["lo"]), int(match["hi"]), condition["condition_id"])
            route_results.append({
                "case_id": case_id, "route": route, "stratum": case["stratum"],
                "searches": len(route_searches), "search_charges": sum(s["charged_searches"] for s in route_searches),
                "attempt_events": len(attempts), "attempt_charges": sum(a["charged_attempts"] for a in attempts),
                "failed_attempts": sum(a["status"] != "success" for a in attempts),
                "section_navigations": len(navigations), "remaining_attempt_budget": 4 - sum(a["charged_attempts"] for a in attempts),
                "opened_file_ids": sorted(opened), "used_file_ids": sorted(used),
                "returned_file_ids": sorted(returned_ids), "returned_links": len(returned),
                "condition_ids": condition_ids, "judgment_observed": judgment["judgment"],
                "judgment_sha256": judgment_hash,
                "first_attempt_utc": first_times[key].isoformat(),
                "read_completed_utc": judgment["read_completed_utc"],
                "judgment_finalized_utc": judgment.get("judgment_finalized_utc"),
            })

    # Request/route order alternates within each tag; tags can run concurrently.
    order_results = []
    for tag in ("jq", "pandoc"):
        tagged = [c for c in protocol["cases"] if c["tag"] == tag]
        planned = [f'{c["case_id"]}-{r}' for c in tagged for r in c["route_order"]]
        actual = sorted(planned, key=lambda key: first_times[key])
        check(actual == planned, "actual_route_order_within_tag", tag,
              {"planned": planned, "actual": actual})
        for left, right in zip(planned, planned[1:]):
            if route_finish_times[left] > first_times[right]:
                warn("declared_completion_interleaves_next_route", tag,
                     {"prior": left, "next": right,
                      "classification": "Initial body-open order is checked separately; late same-file review requires explicit memory/order disclosure, not automatic budget failure."})
        order_results.append({"tag": tag, "planned": planned, "actual": actual,
                              "matches": actual == planned})

    control_results = []
    for case_id in protocol["evaluation"]["equal_scope_controls"]:
        left, right = judgments[case_id + "-A"], judgments[case_id + "-B"]
        exposure_same = exposures[case_id + "-A"]["slots"] == exposures[case_id + "-B"]["slots"]
        check(exposure_same, "same_scope_control_exposure_equality", case_id)
        signature = lambda j: {
            "judgment": j["judgment"],
            "returned": sorted((r["file_id"], r["url"]) for r in j["returned_sources"]),
            "conditions": sorted((c["condition_id"], c["status"], tuple(sorted(c["evidence_file_ids"]))) for c in j["condition_evidence"]),
            "used": sorted(j["used_file_ids"]),
        }
        meaningful_same = signature(left) == signature(right)
        if not meaningful_same:
            warn("same_scope_control_judgment_signature_difference", case_id,
                 {"A": signature(left), "B": signature(right)})
        sections_same = left["returned_sources"] == right["returned_sources"]
        if not sections_same:
            warn("same_scope_control_returned_section_ranges_or_prose_differ", case_id,
                 {"judgment_ids_urls_condition_statuses_match": meaningful_same,
                  "classification": "Not a scope/exposure discrepancy; inspect differing cited ranges or prose separately."})
        control_results.append({"case_id": case_id, "exposure_all_fields_equal": exposure_same,
                                "judgment_ids_urls_condition_statuses_equal": meaningful_same,
                                "returned_sources_all_fields_equal": sections_same})

    if unlogged_ranges:
        warn("cited_ranges_without_full_section_navigation_coverage", detail={
            "count": len(unlogged_ranges),
            "classification": "All affected source bodies were opened in-route. Open event does not record which portions were displayed; absence of a section-navigation log is a traceability warning, not proof of hidden file access.",
        })
    with observation_path.open("a") as stream:
        for item in observations:
            stream.write(json.dumps(item, ensure_ascii=False) + "\n")

    finished = utc()
    report = {
        "audit": "independent-route-accounting-v1", "started_utc": started,
        "finished_utc": finished, "seal1_remote_sha": SEAL1,
        "implementation_independence": "No root seal_routes.py/experiment.py read, import, or call. Computed from raw logs and sealed manifest.",
        "corpus_text_model_exposure": False, "answers_comments_accessed": False,
        "semantic_verdicts_validated": False,
        "judgment_freeze_status": "Current pre-seal2 observations; judgments may still be corrected. Fingerprints and exact prior snapshots are preserved on every audit run.",
        "routes": route_results, "route_count": len(route_results),
        "search_count": sum(r["searches"] for r in route_results),
        "search_charges": sum(r["search_charges"] for r in route_results),
        "body_attempt_events": sum(r["attempt_events"] for r in route_results),
        "body_attempt_charges": sum(r["attempt_charges"] for r in route_results),
        "body_status_counts": dict(status_counter),
        "section_navigations": sum(r["section_navigations"] for r in route_results),
        "returned_link_count": sum(r["returned_links"] for r in route_results),
        "maximum_route_returned_links": max(r["returned_links"] for r in route_results),
        "seal1_files_checked": len(seal1_results), "seal1_files": seal1_results,
        "seal1_exact_byte_matches": sum(r["commit_exact_bytes_match"] for r in seal1_results),
        "seal1_configured_eol_matches": sum(r["git_eol_normalization"] is not None for r in seal1_results),
        "preseal1_amendments_checked": len(amendments),
        "actual_order": order_results, "same_scope_controls": control_results,
        "judgment_fingerprints": fingerprints, "judgment_changes_since_prior_audit": judgment_changes,
        "cited_ranges_not_fully_navigation_covered": unlogged_ranges,
        "violations": problems, "violation_count": len(problems),
        "warnings": warnings, "warning_count": len(warnings),
        "status": "PASS" if not problems else "FAIL",
        "limits": [
            "Recorded same-researcher crossover memory cannot be mechanically removed.",
            "No semantic correctness or useful-link completeness finding is inferred from bookkeeping conformance.",
            "Judgment mtime is a filesystem observation, not the exact instant reasoning was changed.",
            "Changes before the first audit observation cannot be reconstructed by this audit unless another original snapshot exists.",
            "Remote seal2 and first postseal answer access have not yet been audited.",
        ],
    }
    safe_time = finished.replace(":", "").replace("+", "_")
    archive = HERE / "route-audit-runs"
    archive.mkdir(exist_ok=True)
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    (archive / (safe_time + ".json")).write_text(serialized)
    (HERE / "route-audit.json").write_text(serialized)
    text = ["# AF-RES-096 독립 경로 회계 감사", "",
            f"**{report['status']} · 위반 {len(problems)}건 / 경고 {len(warnings)}건** · UTC `{finished}`.", "",
            "루트의 seal_routes.py·experiment.py를 읽거나 호출하지 않고, 원 search/exposure/access/judgment와①봉인 파일 원장에서 재계산했다. 원문 내용은 프로그램의 hash·행범위 대조에만 쓰고 모델에 노출하지 않았다. 답·댓글·채택·outcomes는 열지 않았다. 판정 의미와 완결 분자의 적정성은 검토하지 않았다.", "",
            "|항목|재계산|", "|---|---|",
            f"|경로|{len(route_results)}|",
            f"|검색 이벤트 / 과금|{report['search_count']} / {report['search_charges']}|",
            f"|본문 시도 이벤트 / 과금|{report['body_attempt_events']} / {report['body_attempt_charges']}|",
            f"|본문 결과|{json.dumps(report['body_status_counts'], ensure_ascii=False)}|",
            f"|동일 열린 파일 안의 절 이동|{report['section_navigations']}|",
            f"|반환 링크 합계 / 경로 최대|{report['returned_link_count']} / {report['maximum_route_returned_links']}|",
            f"|①봉인 파일 대조|{len(seal1_results)}파일: 원격 bytes exact {report['seal1_exact_byte_matches']}, Git설정 EOL정규화 동일 {report['seal1_configured_eol_matches']}|",
            f"|①이전 원값·새값·시각·이유 보존 수정|{len(amendments)}건|",
            f"|첫 관측 이후 판정 해시 변경|{len(judgment_changes)}건|", "",
            "## 범위와 기준", "",
            "실패·재시도도 본문 시도로 계산하며 각 경로의2검색·4시도·2반환 한도, 네 노출 자리의 실제 열람 순서, 해당 경로에서 노출하고 연 파일만 근거로 쓰는지, 명시 조건별 행의 누락·추가, 완결 경로의 used IDs가 반환 IDs 안에 포함되는지를 검사했다. 비완결 경로의 추가 진단 자료는 숨은 파일 접근이나 반환수 초과와 구별해 경고로 남겼다.", "",
            "동일범위 대조는 전체 노출 slot과 판정·반환 파일ID/URL·조건 상태/근거ID를 대조했다. 절 범위나 설명문 표현 차이는 의미 판정 없이 경고로 분리했다. jq/pandoc 각 태그 안의 실제 첫 접근과 직전 읽기 완료 시각으로 번갈아 시행한 순서를 검증했으며 태그 사이 병렬 수행은 위반으로 보지 않는다.", "",
            "## 판정 원본과 변경 시각", "",
            "각 judgment.json의 정확한 bytes를 파일 SHA별 judgment-snapshots/에 보존하고, 관측 UTC·파일시스템 mtime·원 read_completed_utc·별도 judgment_finalized_utc·이전 hash·변경 여부를 judgment-observations.jsonl에 append한다. 매 감사 결과도 route-audit-runs/에 별도 남긴다. 최초 감사 관측 이전의 수정은 이 자료만으로 복원하지 못한다. 파일 mtime은 실제 추론 변경 시각의 증거가 아니다. 현 단계는②사전봉인 전이며 이후 변경된 판정으로 재실행해야 한다.", "",
            "첫 감사에서 CSV3개는 커밋 전 manifest hash와 작업파일이 일치하지만 원격 Git bytes와는 달랐다. 차이는 정확히 CRLF→LF이고, 저장소의 text:auto/eol:lf 설정과 일치한다. 이 표현차이를 원문 내용 수정으로 분류하지 않되, 두 hash와 줄끝 수를 별도 경고·원장에 보존한다. 기존 봉인·manifest·CSV는 수정하지 않았다. 원격42파일 모두 exact라고 주장하지 않는다.", "",
            "## 위반", ""]
    text += ([f"- `{r['check']}` · `{r['row']}` · {json.dumps(r['detail'], ensure_ascii=False)}" for r in problems] or ["없음."])
    text += ["", "## 경고", ""]
    text += ([f"- `{r['check']}` · `{r['row']}` · {json.dumps(r['detail'], ensure_ascii=False)}" for r in warnings] or ["없음."])
    text += ["", "## 남은 확인", "",
             "조건·절의 실질적 지지와 반박 여부, 연구자의 기억 영향, 정확판 실행 성공은 감사하지 않았다. source body를 열었지만 별도 절 이동 로그가 덮지 않는 범위는 JSON에 남겼다. 전체 body open에서 실제 모델에 표시된 범위가 기록되지 않았다면 이 경고만으로 미열람 또는 다른 경로에서만 본 절이라고 단정할 수 없다.②원격 봉인 SHA와 사후 최초 답 열람 시각은 이후 별도 대조한다.", ""]
    markdown = "\n".join(text)
    (HERE / "route-audit.md").write_text(markdown)
    (archive / (safe_time + ".md")).write_text(markdown)
    print(json.dumps({k: report[k] for k in ["status", "violation_count", "warning_count", "route_count", "search_count", "body_attempt_events", "body_attempt_charges", "body_status_counts", "section_navigations", "maximum_route_returned_links", "seal1_files_checked"]}, ensure_ascii=False, indent=2))
    print(json.dumps({"violations": problems, "warnings": warnings,
                      "judgment_hash_changes": len(judgment_changes)}, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(run())
