"""Independent source-count, source-identity, and seal chronology audit.

Only ledger fields, source hashes, and HTTP receipts are inspected. Original
source bodies are never printed. Postseal answer bodies/outcome interpretations
are never read, and are excluded from every minimum-source calculation.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
REPO = BASE.parents[3]
SEAL2 = "d03ca37daf0c43688c68bc39417d84a9b84803e9"
INPUTS = [
    "evidence/jq/sources.jsonl", "evidence/pandoc/sources.jsonl",
    "evidence/jq/sources-note.jsonl", "evidence/pandoc/sources-note.jsonl",
    "evidence/crossdomain/sources.jsonl",
]


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def h(blob):
    return hashlib.sha256(blob).hexdigest()


def j(path):
    return json.loads(path.read_bytes())


def jl(path):
    return [json.loads(row) for row in path.read_bytes().splitlines() if row]


def when(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def first(row, *keys):
    return next((row[key] for key in keys if key in row and row[key] not in (None, "", [], {})), None)


def nonempty(value):
    return value is not None and (bool(value.strip()) if isinstance(value, str) else bool(value))


def github_identity(url):
    parsed = urllib.parse.urlsplit(url)
    parts = [urllib.parse.unquote(p) for p in parsed.path.split("/") if p]
    if parsed.netloc.casefold() == "github.com" and len(parts) >= 5 and parts[2] == "blob":
        return "/".join(parts[:2]).casefold(), parts[3], "/".join(parts[4:])
    if parsed.netloc.casefold() == "raw.githubusercontent.com" and len(parts) >= 4:
        return "/".join(parts[:2]).casefold(), parts[2], "/".join(parts[3:])
    return None


def normalized_url(url):
    parsed = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parsed.scheme.casefold(), parsed.netloc.casefold(), parsed.path, parsed.query, ""))


def audit():
    started = utc()
    errors = []
    warnings = []

    def require(condition, code, source=None, detail=None):
        if not condition:
            errors.append({"check": code, "source_id": source, "detail": detail})

    protocol = j(BASE / "protocol.json")
    cases = {case["source_id"]: case for case in protocol["cases"]}
    catalog = {entry["file_id"]: entry for entry in jl(BASE / "corpus-files.jsonl")}
    accesses = []
    for path in (BASE / "evidence/routes").glob("*/access.jsonl"):
        accesses.extend(e for e in jl(path) if e["event"] == "body_attempt")
    success_by_id = collections.defaultdict(list)
    for event in accesses:
        if event["status"] == "success":
            success_by_id[event["file_id"]].append(event)

    jq_bodies = {x["question_id"]: x for x in j(BASE / "evidence/jq/_cache/r0-bodies.json")}
    jq_r0 = {x["question_id"]: x for x in j(BASE / "evidence/jq/r0-index.json")}
    pd_r0 = {x["question_id"]: x for x in j(BASE / "evidence/pandoc/r0-metadata.json")}
    cross_receipts = jl(BASE / "evidence/crossdomain/receipts.jsonl")
    normalized = []
    input_summaries = []
    source_rows = []
    field_audit = []

    for name in INPUTS:
        data = jl(BASE / name)
        input_summaries.append({"path": name, "sha256": h((BASE / name).read_bytes()), "rows": len(data)})
        for line, row in enumerate(data, 1):
            eligible = bool(first(row, "minimum_count_eligible", "minimum_counted", "eligible"))
            # False is a meaningful eligibility value, so determine it without
            # allowing some other truthy field to reinterpret the decision.
            for key in ("minimum_count_eligible", "minimum_counted", "eligible"):
                if key in row:
                    eligible = row[key] is True
                    break
            sid = row["source_id"]
            original = first(row, "original_url", "original_source_url", "url")
            reread = first(row, "reread_url", "reopen_url", "read_url", "reread_url") or original
            category = first(row, "minimum_category", "count_category")
            finding = first(row, "directly_verified", "verified", "directly_observed", "finding")
            limitation = first(row, "limitations", "limitations_unknown", "limitations_unverified")
            supports = first(row, "supports_questions", "supports_or_refutes_questions", "supports_or_refutes", "supports")
            lineage = first(row, "authorship_lineage", "authorship_event_lineage", "work_lineage", "lineage")
            event_lineage = first(row, "independent_work_event", "event_lineage", "event_id", "authorship_event_lineage")
            published = first(row, "published_utc", "published")
            checked = first(row, "checked_utc", "reviewed_utc")
            location = first(row, "file_section_lines", "read_sections", "sections_read", "section", "lines")
            source_hash = first(row, "body_sha256", "sha256")
            version = row.get("version")
            values = {"original_url": original, "reread_url": reread, "published": published,
                      "checked_utc": checked, "version": version, "location": location,
                      "confirmed_finding": finding, "supports_or_refutes": supports,
                      "limitations": limitation, "authorship_lineage": lineage,
                      "event_lineage": event_lineage, "sha256": source_hash}
            missing = [key for key, value in values.items() if not nonempty(value)]
            if eligible:
                require(not missing, "counted_source_required_field_nonempty", sid, missing)
            field_audit.append({"source_id": sid, "input": name, "eligible": eligible,
                                "missing_fields": missing,
                                "finding_nonempty": nonempty(finding), "limitation_nonempty": nonempty(limitation)})
            entry = {"source_id": sid, "ledger_path": name, "ledger_line": line,
                     "eligible": eligible, "original_category": category,
                     "original_url": original, "reread_url": reread,
                     "source_sha256": source_hash, "missing_fields": missing}
            if not eligible:
                entry.update(count_bucket="excluded", exclusion_category=category,
                             canonical_source_key=None, project=None, user_event_id=None,
                             recorded_finding_nonempty=nonempty(finding), recorded_limit_nonempty=nonempty(limitation))
                normalized.append(entry)
                continue

            if category == "new_r0":
                require(sid in cases, "R0_matches_selected_protocol_case", sid)
                case = cases[sid]
                qid = case["question_id"]
                guid = case["r0_guid"].casefold()
                meta = jq_r0[qid] if case["tag"] == "jq" else pd_r0[qid]
                require(meta["body_sha256"] == source_hash, "R0_metadata_body_hash", sid)
                if case["tag"] == "jq":
                    body = jq_bodies[qid]["body"].encode()
                    require(jq_bodies[qid]["revision_guid"].casefold() == guid, "R0_jq_revision_GUID", sid)
                    local = "evidence/jq/_cache/r0-bodies.json#" + str(qid)
                else:
                    local = "evidence/pandoc/_cache/" + str(qid) + ".html"
                    body = (BASE / local).read_bytes()
                    require(meta["earliest_body_revision"]["revision_guid"].casefold() == guid, "R0_pandoc_revision_GUID", sid)
                require(h(body) == source_hash, "R0_cached_body_sha256", sid)
                entry.update(count_bucket="new_r0", canonical_source_key=f"stackoverflow/question/{qid}@revision/{guid}",
                             project=None, user_event_id=f"stackoverflow-question-{qid}",
                             material_role="original_request", local_source=local,
                             local_hash_verified=h(body) == source_hash,
                             first_direct_open_utc=checked)
            elif name.endswith("sources-note.jsonl"):
                fid = row.get("file_id", sid)
                require(fid in catalog, "official_source_in_frozen_catalog", sid, fid)
                item = catalog[fid]
                version_identity = item["commit"] or "version:" + item["version"]
                identity = item["repo"].casefold() + "@" + version_identity + ":" + item["path"]
                require(source_hash == item["sha256"], "source_note_catalog_sha256", sid)
                raw = (BASE / item["cached_body"]).read_bytes()
                require(h(raw) == source_hash, "official_source_cached_sha256", sid)
                require(normalized_url(original) == normalized_url(item["url"]), "official_source_original_URL", sid)
                opens = success_by_id[fid]
                require(bool(opens), "counted_official_file_actually_opened", sid)
                actual_routes = sorted({f'{e["case_id"]}-{e["route"]}' for e in opens})
                if "read_routes" in row:
                    require(sorted(row["read_routes"]) == actual_routes, "source_note_read_routes_match_access", sid)
                if "route_body_opens" in row:
                    note_reads = sorted((e["case_route"], e["utc"], e["status"]) for e in row["route_body_opens"])
                    real_reads = sorted((f'{e["case_id"]}-{e["route"]}', e["started_utc"], e["status"]) for e in opens)
                    require(note_reads == real_reads, "source_note_open_receipts_match_access", sid)
                if category == "upstream_original_test":
                    bucket = "upstream_original_test"
                elif category.startswith("main_"):
                    bucket = "main_official_manual_implementation"
                elif category.startswith("adjacent_"):
                    bucket = "adjacent_official_manual_implementation"
                else:
                    bucket = "unmapped"
                    require(False, "counted_official_category_mapped", sid, category)
                entry.update(count_bucket=bucket, canonical_source_key=identity,
                             project=item["repo"].casefold(), user_event_id=None,
                             material_role="original_upstream_test" if bucket == "upstream_original_test" else "official_manual_or_implementation",
                             file_id=fid, repo=item["repo"], commit=item["commit"], version=item["version"], path=item["path"],
                             local_source=item["cached_body"], local_hash_verified=h(raw) == source_hash,
                             actual_route_open_count=len(opens), actual_read_routes=actual_routes,
                             first_direct_open_utc=min(e["started_utc"] for e in opens))
            elif name == "evidence/crossdomain/sources.jsonl":
                identity = github_identity(original)
                require(identity is not None, "Q7_pinned_GitHub_identity", sid)
                project, commit, source_path = identity
                require(github_identity(reread) == identity, "Q7_raw_and_blob_same_material", sid)
                require(commit == row["commit"] and source_path == row["path"], "Q7_version_file_identity", sid)
                raw = (BASE / row["local_copy"]).read_bytes()
                require(h(raw) == source_hash, "Q7_local_source_sha256", sid)
                matching = [r for r in cross_receipts if r["url"] == reread and r.get("sha256") == source_hash and r.get("success")]
                require(bool(matching), "Q7_direct_fetch_receipt", sid)
                entry.update(count_bucket=category, canonical_source_key=f"{project}@{commit}:{source_path}",
                             project=project, user_event_id=None, material_role=row.get("primary_kind"),
                             local_source=row["local_copy"], local_hash_verified=h(raw) == source_hash,
                             calibration_cluster=row["event_id"],
                             first_direct_open_utc=min(r["finished_utc"] for r in matching))
            else:
                require(False, "counted_input_type_recognized", sid)
            normalized.append(entry)
            source_rows.append(entry)

    by_source = collections.defaultdict(list)
    by_url = collections.defaultdict(list)
    by_hash = collections.defaultdict(list)
    for entry in source_rows:
        by_source[entry["canonical_source_key"]].append(entry["source_id"])
        by_url[normalized_url(entry["original_url"])].append(entry["source_id"])
        by_hash[entry["source_sha256"]].append(entry["source_id"])
    duplicate_keys = {key: ids for key, ids in by_source.items() if len(ids) > 1}
    duplicate_urls = {key: ids for key, ids in by_url.items() if len(ids) > 1}
    duplicate_hashes = {key: ids for key, ids in by_hash.items() if len(ids) > 1}
    require(not duplicate_keys, "no_double_count_same_repo_commit_path_or_R0_revision", detail=duplicate_keys)
    require(not duplicate_urls, "no_double_count_same_canonical_URL", detail=duplicate_urls)
    if duplicate_hashes:
        warnings.append({"check": "same_bytes_multiple_source_identities", "detail": duplicate_hashes,
                         "interpretation": "Must inspect whether a true mirror; different implementation/test paths can legitimately share bytes."})
    unique = list({entry["canonical_source_key"]: entry for entry in source_rows}.values())
    counts = collections.Counter(entry["count_bucket"] for entry in unique)
    minimums = {"new_r0": 8, "main_official_manual_implementation": 4,
                "adjacent_official_manual_implementation": 4, "upstream_original_test": 4,
                "crossdomain_sphinx": 2, "crossdomain_gdal": 2}
    for bucket, minimum in minimums.items():
        require(counts[bucket] >= minimum, "allocated_source_minimum", bucket,
                {"observed": counts[bucket], "minimum": minimum})
    require(len(unique) >= 24, "overall_unique_primary_minimum_24", detail=len(unique))
    question_events = sorted({entry["user_event_id"] for entry in unique if entry["user_event_id"]})
    require(len(question_events) == 8, "eight_distinct_selected_public_request_events")
    require({e["source_id"] for e in unique if e["count_bucket"] == "new_r0"} == set(cases), "all_eight_selected_R0_slots")
    projects = sorted({e["project"] for e in unique if e["project"]})
    tests = [e for e in unique if e["count_bucket"] == "upstream_original_test"]
    test_projects = collections.defaultdict(list)
    for entry in tests:
        test_projects[entry["project"]].append(entry["source_id"])
    primary_corpus_ids = {e["file_id"] for e in unique if e.get("file_id")}
    corpus_open_count = sum(len(success_by_id[fid]) for fid in primary_corpus_ids)
    unique_opened_corpus_files = len(success_by_id)
    route_reopen_count = len(accesses) - unique_opened_corpus_files

    # Seal2: compare every declared file to immutable Git object, preserving
    # .gitattributes CRLF/LF representation differences separately.
    seal_receipt = j(BASE / "evidence/seal2-receipt.json")
    seal_manifest = j(BASE / "evidence/seal2-files.json")
    require(seal_receipt["remote_sha"] == SEAL2 and seal_receipt["confirmed_remote"] is True, "seal2_remote_receipt_identity")
    verified = when(seal_receipt["verified_utc"])
    seal_checks = []
    for record in seal_manifest["files"]:
        path = REPO / record["path"]
        raw = path.read_bytes()
        require(h(raw) == record["sha256"], "seal2_current_raw_manifest_sha256", record["path"])
        require(len(raw) == record["bytes"], "seal2_current_raw_manifest_bytes", record["path"])
        sealed = subprocess.run(["git", "show", f'{SEAL2}:{record["path"]}'], cwd=REPO,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        require(sealed.returncode == 0, "seal2_commit_blob_available", record["path"])
        exact = raw == sealed.stdout
        normalized_only = False
        if not exact and path.suffix == ".csv":
            attrs = subprocess.run(["git", "check-attr", "-z", "text", "eol", "--", record["path"]], cwd=REPO,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            parts = attrs.stdout.decode().split("\0")
            settings = {parts[i+1]: parts[i+2] for i in range(0, len(parts)-2, 3)}
            normalized_only = settings.get("eol") == "lf" and settings.get("text") in {"auto", "set"} and raw.replace(b"\r\n", b"\n") == sealed.stdout
        require(exact or normalized_only, "seal2_frozen_content_unchanged", record["path"])
        seal_checks.append({"path": record["path"], "worktree_sha256": h(raw),
                            "commit_sha256": h(sealed.stdout), "exact_bytes_equal": exact,
                            "configured_csv_eol_only": normalized_only})

    first_open = j(BASE / "evidence/outcomes/first-open.json")
    require(first_open["seal2_remote_sha"] == SEAL2, "postseal_first_open_pinned_SHA")
    require(when(first_open["first_open_utc"]) > verified, "first_open_marker_after_remote_confirmation")
    post_receipts = jl(BASE / "evidence/outcomes/receipts.jsonl")
    require(bool(post_receipts), "actual_post_open_receipt_present")
    first_actual = min(post_receipts, key=lambda r: when(r["started_utc"]))
    require(when(first_actual["started_utc"]) >= when(first_open["first_open_utc"]), "actual_first_request_after_first_open_marker")
    for receipt in post_receipts:
        require(when(receipt["started_utc"]) > verified, "every_post_request_after_seal2", receipt.get("label"))
    post_chronology = {
        "seal2_remote_confirmed_utc": seal_receipt["verified_utc"],
        "first_open_marker_utc": first_open["first_open_utc"],
        "first_actual_request_started_utc": first_actual["started_utc"],
        "first_actual_request_finished_utc": first_actual["finished_utc"],
        "first_actual_request_url": first_actual["url"],
        "seconds_between_remote_confirmation_and_first_actual_request": (when(first_actual["started_utc"]) - verified).total_seconds(),
        "post_receipts_checked": len(post_receipts),
        "post_outcome_bodies_read_by_auditor": False,
        "post_outcome_contribution_to_minimum": 0,
    }

    # Independent public Git metadata confirmation; no diff or source contents.
    remote_url = f"https://api.github.com/repos/laadkke-arch/agentflow-open/git/commits/{SEAL2}"
    remote_record = {"url": remote_url, "started_utc": utc(), "counts_toward_minimum": False}
    try:
        with urllib.request.urlopen(remote_url, timeout=30) as response:
            raw = response.read()
            metadata = json.loads(raw)
            remote_record.update(http_status=response.status, response_sha256=h(raw), sha=metadata["sha"],
                                 tree_sha=metadata["tree"]["sha"], committer_date=metadata["committer"]["date"], success=True)
            require(metadata["sha"] == SEAL2, "independent_GitHub_commit_identity")
    except Exception as exc:
        remote_record.update(success=False, error=f"{type(exc).__name__}: {exc}")
        warnings.append({"check": "independent_remote_metadata_fetch_unavailable", "detail": remote_record["error"],
                         "interpretation": "Local immutable Git objects and root's exact-SHA remote receipt still inspected; this fresh network check is unconfirmed."})
    remote_record["finished_utc"] = utc()
    (HERE / "source-audit-remote-seal2.json").write_text(json.dumps(remote_record, ensure_ascii=False, indent=2) + "\n")

    result = {
        "audit": "independent-source-count-and-seal-chronology-v1", "started_utc": started, "finished_utc": utc(),
        "input_ledgers": input_summaries, "input_rows": len(normalized),
        "eligible_rows_before_dedup": len(source_rows), "unique_primary_materials": len(unique),
        "excluded_rows": len(normalized)-len(source_rows), "allocated_counts": dict(sorted(counts.items())),
        "allocated_minimums": minimums, "unique_public_request_events": len(question_events),
        "public_request_event_ids": question_events, "unique_human_requester_count": "미확인; blinded recruitment does not establish distinct persons",
        "project_authorship_lineage_count": len(projects), "project_authorship_lineages": projects,
        "upstream_minimum_test_files": len(tests), "upstream_minimum_test_project_lineages": dict(test_projects),
        "independent_observed_upstream_execution_events": "산출 불가; file/spec counts do not establish independent execution incidents",
        "calibration_user_event_contribution": 0, "post_outcome_minimum_contribution": 0,
        "canonical_key_duplicate_groups": duplicate_keys, "canonical_URL_duplicate_groups": duplicate_urls,
        "identical_body_hash_groups": duplicate_hashes,
        "route_body_attempts": len(accesses), "unique_route_opened_corpus_files": unique_opened_corpus_files,
        "repeated_route_body_reads_not_new_sources": route_reopen_count,
        "eligible_corpus_unique_files": len(primary_corpus_ids), "eligible_corpus_route_open_events": corpus_open_count,
        "required_field_checks": field_audit,
        "counted_source_missing_required_field_rows": sum(e["eligible"] and bool(e["missing_fields"]) for e in normalized),
        "counted_cached_hash_checks": sum(e.get("local_hash_verified", False) for e in unique),
        "source_identity_limit": "Exact URL, pinned repo/ref:path, and byte hashes tested; semantic mirror equivalence beyond these identities was not inferred without inspecting meaning.",
        "seal2_remote_sha": SEAL2, "seal2_manifest_files_checked": len(seal_checks),
        "seal2_exact_bytes_equal": sum(e["exact_bytes_equal"] for e in seal_checks),
        "seal2_configured_csv_eol_only": sum(e["configured_csv_eol_only"] for e in seal_checks),
        "seal2_files": seal_checks, "post_chronology": post_chronology,
        "independent_remote_metadata_receipt": remote_record,
        "source_claim_truth_validated": False, "source_text_displayed_to_model": False,
        "errors": errors, "error_count": len(errors), "warnings": warnings,
        "status": "PASS" if not errors else "FAIL",
    }
    (HERE / "source-count-normalized.json").write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n")
    (HERE / "source-count-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    report = ["# AF-RES-096 독립 자료수·봉인 순서 감사", "",
              f"**{result['status']} · 오류 {len(errors)}건** · `{result['finished_utc']}`.", "",
              "루트의 통합 sources.jsonl·metrics·결과 수치를 입력으로 쓰지 않았다. jq/pandoc 모집 원장2개, 실제 공식원문 메모2개, Q7원장1개에서 독립 집계하고 corpus/실제접근/취득 영수증·고정 R0와 해시를 대조했다. 본문은 프로그램 hash 검사만 했으며 모델에 출력하지 않았다. 사후 답 본문은 읽지 않았고 최소량에도 넣지 않았다.", "",
              "|하한 할당|중복 제거 후 고유 원자료|하한|", "|---|---:|---:|"]
    report += [f"|{bucket}|{counts[bucket]}|{minimum}|" for bucket, minimum in minimums.items()]
    report += [f"|전체|{len(unique)}|24|", "",
               f"원장 {len(normalized)}행 중 산입 {len(source_rows)}행·제외 {len(normalized)-len(source_rows)}행이며, URL/repo@고정판:path/R0리비전 중복 제거 뒤 {len(unique)}개다. 같은 내용 hash가 다른 산입 자료로 겹친 그룹 {len(duplicate_hashes)}개, 같은 파일 정체성이 겹친 그룹 {len(duplicate_keys)}개다. 산입자료의 확인내용·한계 등 필수필드 공백 {result['counted_source_missing_required_field_rows']}행, 원문 해시 대조 {result['counted_cached_hash_checks']}개다. 필드가 채워졌다는 것은 주장의 참을 독립 입증했다는 뜻이 아니다.", "",
               "## 자료·사건·저작 계보를 따로 셈", "",
               f"- 원 요청 사건은 Stack Overflow 질문 ID가 다른 **{len(question_events)}건**이다. 요청자 개인이8명인지 또는 통계적으로 독립인지까지 확인하지 않았다.",
               f"- 공식자료의 프로젝트 저작 계보는 **{len(projects)}개**다: {', '.join(projects)}. 파일 수와 프로젝트 수를 합치지 않는다.",
               f"- 최소량의 상류 원 시험은 **{len(tests)}파일**, 프로젝트 계보는 **{len(test_projects)}개**다. jq의 두 시험 파일과 Asciidoctor의 두 시험 파일을 별개 원자료로 세되, 네 독립 사용자 성공 사건이나 네 독립 실행으로 세지 않는다. 같은 변환 문제를 여러 파일이 뒷받침할 때 근거 정밀도는 늘 수 있지만 사건 분모는 늘지 않는다.",
               f"- 경로의 본문 시도 **{len(accesses)}회**는 고유 corpus파일 **{unique_opened_corpus_files}개**에 대한 것이다. 반복 접근 **{route_reopen_count}회**는 신규자료가 아니다. 그중 하한에 산입하는 corpus파일은 **{len(primary_corpus_ids)}개**, 대응하는 실제 접근은 **{corpus_open_count}회**다.",
               "- Q7 교정 자료는 해당 계열 할당에만 한 번씩 센다. 새 요청·사용자 행동·주 실험 성공 분자는 늘리지 않는다. 사후 답·댓글·현재 채택·실행 보고의 하한 기여는0이다.", "",
               "## ②봉인 불변과 사후 최초 접근", "",
               f"고정 SHA `{SEAL2}`의 manifest **{len(seal_checks)}파일**을 현재 bytes·manifest hash·Git 객체와 비교했다. 원격 바이트와 정확히 같은 파일 **{result['seal2_exact_bytes_equal']}개**, CSV의 설정된 CRLF→LF만 다른 파일 **{result['seal2_configured_csv_eol_only']}개**다. 기존 파일이나 원 봉인 manifest를 고치지 않았다.", "",
               f"원격 확인 `{seal_receipt['verified_utc']}` → 최초 열람 표식 `{first_open['first_open_utc']}` → 실제 첫 HTTP요청 `{first_actual['started_utc']}` 순서다. 실제 첫 요청은 확인 뒤 **{post_chronology['seconds_between_remote_confirmation_and_first_actual_request']:.6f}초**이며, 이 감사에서 확보된 사후 취득 영수증 **{len(post_receipts)}개** 모두 원격 확인 뒤 시작했다. marker만 비교하지 않고 실제 request 시작 시각을 사용했다. 사후 수집이 더 진행되면 같은 코드로 다시 검사한다.", "",
               f"별도 GitHub Git-commit API 재조회 성공 여부: **{remote_record['success']}**. 응답 hash·SHA·tree·시각은 source-audit-remote-seal2.json에 있다. 이 메타데이터는 외부1차자료 하한에 산입하지 않는다.", "",
               "## 한계", "",
               "공식자료/원시험이라는 원장 분류와 확인내용·한계의 존재를 검사했으며 각 문장의 참·조건 완결을 재판정하지 않았다. 바이트나 경로가 다른 의미상 미러를 완전히 판별하지는 못한다. 동일 파일의 여러 절은 한 정체성으로 셌고, GitHub blob/raw 주소를 별개 자료로 더하지 않았다. 사후 공개 자료는 별도 사건 추적을 위한 것이며 이 최소량을 보충하는 데 쓰지 않았다.", "",
               "## 오류", ""]
    report += ([f"- `{e['check']}` · `{e['source_id']}` · {json.dumps(e['detail'], ensure_ascii=False)}" for e in errors] or ["없음."])
    report += ["", "## 경고", ""]
    report += ([f"- {json.dumps(w, ensure_ascii=False)}" for w in warnings] or ["없음."])
    report.append("")
    (HERE / "source-count-audit.md").write_text("\n".join(report))
    print(json.dumps({key: result[key] for key in ["status", "error_count", "input_rows", "eligible_rows_before_dedup", "unique_primary_materials", "allocated_counts", "unique_public_request_events", "project_authorship_lineage_count", "counted_source_missing_required_field_rows", "counted_cached_hash_checks", "seal2_manifest_files_checked", "seal2_exact_bytes_equal", "seal2_configured_csv_eol_only", "post_chronology"]}, ensure_ascii=False, indent=2))
    print(json.dumps({"errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(audit())
