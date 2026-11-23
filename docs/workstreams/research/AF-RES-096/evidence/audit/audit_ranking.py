"""Independent mechanical Q3 audit. Never prints corpus text or answer data.

This is a second implementation of protocol.json, not an import, invocation,
or copy of experiment.py. It writes only under evidence/audit/. Pinned
protocol/corpus metadata and cached source bytes are read, never modified.
"""
from __future__ import annotations

import collections
import datetime as dt
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
REPO = BASE.parents[3]
SEAL1 = "abf2bc2ac9303cb96e6109eba107684e5f858a42"
TOKEN = re.compile(r"[a-z0-9_]+")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def utc() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def rows(path: Path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def norm_tokens(text: str):
    return set(TOKEN.findall(unicodedata.normalize("NFKC", text).casefold()))


def audit():
    started = utc()
    discrepancies = []
    observations = []

    def check(condition, code, row=None, detail=None):
        if not condition:
            discrepancies.append({"check": code, "row": row, "detail": detail})

    sealed = {}
    seal_checks = []
    for name in ("protocol.json", "corpus-plan.json", "corpus-files.jsonl"):
        current = (BASE / name).read_bytes()
        repository_path = str((BASE / name).relative_to(REPO))
        past = subprocess.run(
            ["git", "show", f"{SEAL1}:{repository_path}"], cwd=REPO,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        check(past.returncode == 0, "seal1_blob_available", name,
              {"exit_code": past.returncode})
        if past.returncode:
            raise RuntimeError("Sealed protocol is unavailable; cannot audit.")
        check(past.stdout == current, "seal1_unchanged", name)
        sealed[name] = past.stdout
        seal_checks.append({"file": name, "sealed_sha256": sha(past.stdout),
                            "current_sha256": sha(current),
                            "equal": past.stdout == current})

    protocol = json.loads(sealed["protocol.json"])
    plan = json.loads(sealed["corpus-plan.json"])
    catalog = [json.loads(line) for line in sealed["corpus-files.jsonl"].splitlines() if line]
    by_id = {x["file_id"]: x for x in catalog}
    plan_by_label = {x["label"]: x for x in plan["repositories"]}
    check(len(by_id) == len(catalog), "unique_file_ids")
    check(len({(x["repo"], x["path"]) for x in catalog}) == len(catalog), "one_repo_path_one_file")
    tokens = {}
    hashes = {}
    decoded_lengths = {}
    label_counts = collections.Counter()
    for entry in catalog:
        file_id = entry["file_id"]
        label_counts[entry["label"]] += 1
        cfg = plan_by_label[entry["label"]]
        permitted = any(fnmatch.fnmatchcase(entry["path"], pattern) for pattern in cfg["include"])
        excluded = any(fnmatch.fnmatchcase(entry["path"], pattern) for pattern in cfg["exclude"])
        check(permitted and not excluded, "file_scope", file_id)
        check(entry["repo"] == cfg["repo"], "repository_identity", file_id)
        check(entry["version"] == cfg["version"], "version_identity", file_id)
        check(entry["commit"] == cfg["commit"], "commit_identity", file_id)
        expected_url = cfg["file_url_template"].format(path=entry["path"])
        check(entry["url"] == expected_url, "source_url_identity", file_id)
        path = BASE / entry["cached_body"]
        check(path.is_file(), "cached_source_exists", file_id)
        if not path.is_file():
            tokens[file_id] = set()
            continue
        body_bytes = path.read_bytes()
        hashes[file_id] = sha(body_bytes)
        check(hashes[file_id] == entry["sha256"], "body_sha256", file_id)
        check(len(body_bytes) == entry["bytes"], "body_bytes", file_id)
        check(len(body_bytes) <= plan["max_file_bytes"], "maximum_file_size", file_id)
        try:
            text = body_bytes.decode("utf-8")
        except UnicodeDecodeError:
            check(False, "utf8_text", file_id)
            text = ""
        tokens[file_id] = norm_tokens(text)
        decoded_lengths[file_id] = len(text)
        # No text, excerpts, or token list is printed or added to the audit report.

    def expected_rank(allowed, query_words):
        query_set = norm_tokens(" ".join(query_words))
        scored = []
        for item in catalog:
            if item["label"] not in allowed:
                continue
            hits = sorted(tokens[item["file_id"]] & query_set)
            scored.append((item, hits))
        scored.sort(key=lambda pair: (-len(pair[1]), pair[0]["repo"] + "/" + pair[0]["path"]))
        return [{"rank": n, "file_id": item["file_id"],
                 "score": len(hits), "matched_tokens": hits}
                for n, (item, hits) in enumerate(scored, 1)]

    def validate_rank(path, expected, key):
        got = rows(path)
        check(len(got) == len(expected), "ranking_row_count", key,
              {"observed": len(got), "expected": len(expected)})
        if got != expected:
            for n in range(max(len(got), len(expected))):
                observed = got[n] if n < len(got) else None
                predicted = expected[n] if n < len(expected) else None
                if observed != predicted:
                    # Ranking metadata is safe, but no corpus text is reported.
                    check(False, "ranking_row_disagreement", f"{key}:{n+1}",
                          {"observed": observed, "expected": predicted})
        return {"file": str(path.relative_to(BASE)), "rows": len(got),
                "sha256": sha(path.read_bytes()), "agrees": got == expected,
                "positive": sum(x["score"] > 0 for x in expected),
                "zero_score": sum(x["score"] == 0 for x in expected)}

    events = rows(BASE / "evidence/search-events.jsonl")
    searches = [x for x in events if x["event"] == "search"]
    exposure_events = [x for x in events if x["event"] == "exposure"]
    search_index = {(x["case_id"], x["route"], x["query_number"]): x for x in searches}
    exposure_index = {(x["case_id"], x["route"]): x for x in exposure_events}
    check(len(searches) == 32, "32_searches", detail=len(searches))
    check(len(search_index) == 32, "unique_search_events")
    check(len(exposure_events) == 16, "16_exposure_events", detail=len(exposure_events))
    check(len(exposure_index) == 16, "unique_exposure_events")
    check(len(list((BASE / "evidence/ranking").glob("*.jsonl"))) == 48,
          "48_full_ranking_files")
    check(len(list((BASE / "evidence/routes").glob("*/exposure.json"))) == 16,
          "16_route_exposure_files")

    rank_results = []
    route_results = []
    fallback_rows = []
    padding_rows = []
    scored_zero_rows = 0
    ties_checked = 0
    merged_duplicate_tokens = []
    slot_total = 0
    exposure_snapshots = {}
    expected_route_sequence = []
    for case in protocol["cases"]:
        query1, query2 = case["queries"]
        overlap = norm_tokens(" ".join(query1)) & norm_tokens(" ".join(query2))
        if overlap:
            merged_duplicate_tokens.append({"case_id": case["case_id"],
                                             "duplicate_query_token_count": len(overlap)})
        for route in case["route_order"]:
            case_id = case["case_id"]
            key = f"{case_id}-{route}"
            expected_route_sequence.append(key)
            labels = [case["main_label"]]
            if route == "B" and case["stratum"] == "boundary":
                labels.append(case["adjacent_label"])
            for query_number, words in enumerate(case["queries"], 1):
                expected = expected_rank(labels, words)
                rankpath = BASE / f"evidence/ranking/{key}-q{query_number}.jsonl"
                rank_results.append(validate_rank(rankpath, expected, f"{key}-q{query_number}"))
                scored_zero_rows += sum(r["score"] == 0 for r in expected)
                ties_checked += sum(a["score"] == b["score"] for a, b in zip(expected, expected[1:]))
                event = search_index.get((case_id, route, query_number))
                check(event is not None, "query_event_present", f"{key}-q{query_number}")
                if event:
                    check(event["query_tokens"] == sorted(norm_tokens(" ".join(words))), "normalized_query_tokens", f"{key}-q{query_number}")
                    check(event["allowed_labels"] == labels, "query_allowed_repositories", f"{key}-q{query_number}")
                    check(event["charged_searches"] == 1, "search_charge", f"{key}-q{query_number}")
                    check(event["ranked_files"] == len(expected), "search_full_denominator", f"{key}-q{query_number}")
                    check(event["positive_files"] == sum(r["score"] > 0 for r in expected), "search_positive_denominator", f"{key}-q{query_number}")
                    check(event["full_ranking_sha256"] == sha(rankpath.read_bytes()), "query_event_hash", f"{key}-q{query_number}")
                    check(event["full_ranking_file"] == str(rankpath.relative_to(BASE)), "query_event_path", f"{key}-q{query_number}")
                    check(event["started_utc"] <= event["finished_utc"], "search_timestamp_order", f"{key}-q{query_number}")

            merged = expected_rank(labels, query1 + query2)
            rankpath = BASE / f"evidence/ranking/{key}-merged.jsonl"
            rank_results.append(validate_rank(rankpath, merged, f"{key}-merged"))
            scored_zero_rows += sum(r["score"] == 0 for r in merged)
            ties_checked += sum(a["score"] == b["score"] for a, b in zip(merged, merged[1:]))
            positives_by_role = {
                "main": [r for r in merged if r["score"] > 0 and by_id[r["file_id"]]["label"] == case["main_label"]],
                "adjacent": [r for r in merged if r["score"] > 0 and by_id[r["file_id"]]["label"] != case["main_label"]],
            }
            allocations = [("main", 0), ("main", 1), ("main", 2), ("main", 3)]
            if route == "B" and case["stratum"] == "boundary":
                allocations = [("main", 0), ("main", 1), ("adjacent", 0), ("adjacent", 1)]
            exposurepath = BASE / f"evidence/routes/{key}/exposure.json"
            exp = json.loads(exposurepath.read_text())
            exposure_snapshots[(case_id, route)] = exp
            check(exp == exposure_index.get((case_id, route)), "exposure_event_same_as_file", key)
            check(exp["seal1_remote_sha"] == SEAL1, "exposure_references_seal1", key)
            check(exp["full_merged_ranking"] == str(rankpath.relative_to(BASE)), "merged_ranking_path", key)
            check(exp["full_merged_sha256"] == sha(rankpath.read_bytes()), "merged_ranking_hash", key)
            check(exp["route_order"] == case["route_order"], "route_order_declared", key)
            check(len(exp["slots"]) == 4, "four_slots", key)
            slot_total += len(exp["slots"])
            nonempty_ids = [slot["file_id"] for slot in exp["slots"] if not slot["empty"]]
            check(len(nonempty_ids) == len(set(nonempty_ids)), "one_file_one_exposed_result", key)
            before = len(discrepancies)
            for slot_number, ((role, role_index), slot) in enumerate(zip(allocations, exp["slots"]), 1):
                slot_key = f"{key}:{slot_number}"
                check(slot["slot"] == slot_number, "slot_index", slot_key)
                available = positives_by_role[role]
                expected_row = available[role_index] if role_index < len(available) else None
                if expected_row is None:
                    check(slot["empty"] and slot["file_id"] is None, "explicit_empty_slot_not_refilled", slot_key)
                    continue
                fid = expected_row["file_id"]
                entry = by_id[fid]
                check(slot["file_id"] == fid and not slot["empty"], "exposed_file_identity", slot_key)
                check(slot["role"] == role, "slot_role", slot_key)
                for prop in ("repo", "path", "url"):
                    check(slot[prop] == entry[prop], "exposed_" + prop, slot_key)
                check(slot["merged_global_rank"] == expected_row["rank"], "exposed_global_rank", slot_key)
                check(slot["within_role_rank"] == role_index + 1, "exposed_role_rank", slot_key)
                check(slot["score"] == expected_row["score"], "exposed_score", slot_key)
                check(slot["matched_tokens"] == expected_row["matched_tokens"], "exposed_distinct_tokens", slot_key)
                check(slot["score"] > 0, "zero_score_not_exposed", slot_key)
                check(slot["body_sha256"] == hashes[fid], "exposed_body_hash", slot_key)
                raw = (BASE / entry["cached_body"]).read_text(encoding="utf-8")
                # Protocol: first original-text case-insensitive token boundary,
                # 100 original characters before it, then exactly 600 with padding.
                pattern = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in expected_row["matched_tokens"]) + r")\b", re.I)
                hit = pattern.search(raw)
                fallback = hit is None
                offset = max(0, hit.start() - 100) if hit else 0
                excerpt_raw = raw[offset:offset + protocol["ranking"]["excerpt_chars"]]
                excerpt = excerpt_raw.ljust(protocol["ranking"]["excerpt_chars"])
                check(slot["excerpt_offset"] == offset, "excerpt_anchor_offset", slot_key,
                      {"expected": offset, "observed": slot["excerpt_offset"]})
                check(slot["anchor_fallback"] == fallback, "excerpt_fallback_flag", slot_key)
                check(slot["excerpt"] == excerpt, "excerpt_bytes", slot_key,
                      {"expected_sha256": sha(excerpt.encode()), "observed_sha256": sha(slot["excerpt"].encode())})
                check(slot["excerpt_sha256"] == sha(excerpt.encode()), "excerpt_recorded_hash", slot_key)
                check(slot["excerpt_source_chars"] == len(excerpt_raw), "excerpt_source_length", slot_key)
                check(len(slot["excerpt"]) == 600, "excerpt_equal_600_chars", slot_key)
                if fallback:
                    fallback_rows.append({"slot": slot_key, "file_id": fid, "normalized_score": expected_row["score"], "offset": offset})
                if len(excerpt_raw) < 600:
                    padding_rows.append({"slot": slot_key, "file_id": fid, "source_characters": len(excerpt_raw), "padded_characters": 600 - len(excerpt_raw)})
            route_results.append({"case_id": case_id, "route": route,
                                  "stratum": case["stratum"], "ranked_files": len(merged),
                                  "slots": len(exp["slots"]), "nonempty_slots": len(nonempty_ids),
                                  "main_exposed": sum(not s["empty"] and s.get("role") == "main" for s in exp["slots"]),
                                  "adjacent_exposed": sum(not s["empty"] and s.get("role") == "adjacent" for s in exp["slots"]),
                                  "slot_disagreements": len(discrepancies) - before})

    check(slot_total == 64, "64_slots", detail=slot_total)
    for case_id in protocol["evaluation"]["equal_scope_controls"]:
        a = exposure_snapshots[(case_id, "A")]
        b = exposure_snapshots[(case_id, "B")]
        check(a["slots"] == b["slots"], "control_A_equals_B_all_slot_fields", case_id)

    actual_search_order = [f'{e["case_id"]}-{e["route"]}' for e in searches if e["query_number"] == 1]
    check(actual_search_order == expected_route_sequence, "planned_route_search_order")
    for tag in ("jq", "pandoc"):
        tagged = [c for c in protocol["cases"] if c["tag"] == tag]
        expected_first = ["A", "B", "A", "B"]
        check([c["route_order"][0] for c in tagged] == expected_first,
              "within_tag_order_alternation", tag)

    # Only the canonical v1.7 jq manual is in the sealed scope. Other kinds of
    # distinct files may legitimately share content; content identity alone
    # is not enough to label an implementation/test file a manual mirror.
    jq_manual = [r["file_id"] for r in catalog if r["label"] == "JQ" and "manual" in r["path"].lower()]
    check(len(jq_manual) == 1, "canonical_jq_manual_only")
    manual_hashes = collections.defaultdict(list)
    for entry in catalog:
        source_path = entry["path"]
        # A tests/manual path is a manual-run test, not a reader's manual.
        # Preserve the initial broad-name false positive in the audit history.
        documented_extension = Path(source_path).suffix.lower() in {
            ".md", ".txt", ".texi", ".rst", ".rd", ".yml", ".1"
        }
        documentation_path = source_path.startswith(("doc/", "docs/", "man/"))
        canonical_named_manual = Path(source_path).name.upper().startswith("MANUAL")
        if (documentation_path and documented_extension) or canonical_named_manual:
            manual_hashes[entry["sha256"]].append(entry["file_id"])
    same_manual_bytes = [ids for ids in manual_hashes.values() if len(ids) > 1]
    check(not same_manual_bytes, "manual_byte_identical_duplicate_files", detail=same_manual_bytes)

    summary = {
        "audit": "independent-Q3-token-ranking-exposure", "started_utc": started,
        "finished_utc": utc(), "seal1_remote_sha": SEAL1,
        "implementation_independence": "No experiment.py import, call, or source read; protocol algorithm recreated separately.",
        "corpus_text_model_exposure": False, "answers_comments_accessed": False,
        "source_reads_count_as_experimental_attempts": False,
        "scope": "Mechanical protocol conformance; no semantic correctness, answer usefulness, or external source minimum judgment.",
        "catalog_files": len(catalog), "repository_file_counts": dict(sorted(label_counts.items())),
        "searches": len(searches), "search_charges": sum(x["charged_searches"] for x in searches),
        "exposure_events": len(exposure_events), "full_ranking_files": len(rank_results),
        "full_ranking_rows": sum(r["rows"] for r in rank_results),
        "zero_score_rows_retained": scored_zero_rows, "tied_neighbor_pairs_checked": ties_checked,
        "slots": slot_total, "nonempty_slots": sum(r["nonempty_slots"] for r in route_results),
        "empty_slots": slot_total - sum(r["nonempty_slots"] for r in route_results),
        "adjacent_slots": sum(r["adjacent_exposed"] for r in route_results),
        "boundary_B_routes_with_adjacent_exposure": sum(r["route"] == "B" and r["stratum"] == "boundary" and r["adjacent_exposed"] > 0 for r in route_results),
        "control_pairs": protocol["evaluation"]["equal_scope_controls"],
        "merged_query_overlap_cases": merged_duplicate_tokens,
        "excerpt_fallback_rows": fallback_rows, "short_file_padded_rows": padding_rows,
        "manual_mirror_limit": "Exact documentation content duplication and canonical jq manual checked; semantic mirror equivalence is not mechanically established. tests/manual is not treated as user documentation.",
        "auditor_correction": {
            "initial_report": "evidence/audit/ranking-audit-initial.json",
            "initial_extra_check_failures": 1,
            "initial_ranking_exposure_disagreements": 0,
            "affected_file_ids": ["RM-0135", "RM-0139"],
            "reason": "A substring 'manual' heuristic wrongly classified two identical tests/manual/*.Rmd inputs as manual mirrors. No source body was shown to the model. Path classification corrected in the auditor only.",
            "P3_B_merged_ranks": [277, 278],
            "affected_exposed_slots": 0,
            "experimental_files_changed": False,
        },
        "seal1_files": seal_checks, "rankings": rank_results, "routes": route_results,
        "disagreements": discrepancies, "disagreement_count": len(discrepancies),
        "status": "PASS" if not discrepancies else "FAIL",
    }
    (HERE / "ranking-audit.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    report = ["# AF-RES-096 독립 Q3 기계 감사", "",
              f"상태 **{summary['status']}** · 불일치 **{len(discrepancies)}건** · 확인 UTC `{summary['finished_utc']}`.", "",
              "`experiment.py`를 읽거나 호출·import하지 않고, 원격①봉인의 protocol을 별도 코드로 구현했다. corpus 본문은 프로그램 내부에서만 토큰화·해시·발췌 대조했고 모델 출력이나 이 보고서에 표시하지 않았다. 신규 요청의 답·댓글·채택은 열지 않았다. 이 감사는 의미 판정이나 원자료 최소량의 감사가 아니다.", "",
              "|항목|원행 재계산|", "|---|---|",
              f"|고정 corpus 파일|{len(catalog)}|",
              f"|검색 이벤트/과금|{len(searches)} / {summary['search_charges']}|",
              f"|노출 이벤트/route exposure 파일|{len(exposure_events)} / {len(exposure_snapshots)}|",
              f"|전체 순위 파일/행|{len(rank_results)} / {summary['full_ranking_rows']}|",
              f"|동점 인접행 대조|{ties_checked}|",
              f"|full rank에 남긴 score0행|{scored_zero_rows}|",
              f"|전체 자리/본문있는 자리/공석|{slot_total} / {summary['nonempty_slots']} / {summary['empty_slots']}|",
              f"|인접 파일 노출자리/해당 B경계경로|{summary['adjacent_slots']} / {summary['boundary_B_routes_with_adjacent_exposure']}|",
              f"|원문 anchor fallback/짧은 파일 padding|{len(fallback_rows)} / {len(padding_rows)}|",
              f"|일치하지 않은 검사|{len(discrepancies)}|", "",
              "## 점검한 계약", "",
              "NFKC→casefold→ASCII token 정규화, 쿼리 내·두 쿼리 간 중복 제거, 파일 본문의 서로 다른 일치 토큰 수, repo/path 대소문자 구분 사전순 tie를 재계산했다. score0 파일은 전체 순위에 포함시키되 노출하지 않았다. A의 주 도구4자리, B의 주 도구2+인접2자리, 공석 비충원, 대조 J1/P2의 전체 slot 필드 일치, 파일별 결과 하나, 600문자 발췌와 source offset/hash/padding/fallback를 대조했다.", "",
              "원문 발췌 anchor는 정규화된 토큰이 원문에서 대소문자 무시 단어 경계로 처음 나타나는 위치다. 원문 검색이 실패해도 정규화 score가 양수이면 offset0/fallback 표시라는 사전 규칙을 적용한다. 이 경로는 재순위화나 추가 근거 열람이 아니다. fallback 개별 행은 JSON에 내용 없이 파일 ID와 자리만 기록했다.", "",
              f"①봉인 `{SEAL1}`의 protocol/corpus-plan/corpus-files 세 파일 바이트를 현재 작업 사본과 비교했다. 결과는 ranking-audit.json의 seal1_files에 각각 SHA-256으로 남겼다. 본문3560개도 각 corpus metadata hash·bytes와 대조했다.", "",
              "## 한계와 다음 감사", "",
              "원문 의미상 같은 매뉴얼의 미러 여부는 해시만으로 모두 판별되지 않는다. 고정된 jq canonical manual 하나와 문서 경로의 동일 바이트 중복만 기계 확인했다. 본문 파일 내용과 ID의 적합성, 조건별 완결, 답의 독창성은 이 감사 대상이 아니다. 현재 접근·판정 작성이 진행 중이므로 실제4회 예산·미노출 근거 이용·최대2 반환 링크·②사전봉인/사후시각은 후속 감사에서 검사한다.", "",
              "## 감사기 자체의 수정 이력", "",
              "첫 실행도 순위·노출 불일치는0이었지만, 추가 mirror 검사에서 경로에 manual이라는 문자열이 있다는 이유로 `tests/manual/bslib-forced-mode/test.Rmd`(RM-0135)와 `tests/manual/test.Rmd`(RM-0139)를 독자용 매뉴얼 미러로 잘못 분류하여 실패1을 냈다. 두 파일은 수동 실행 시험의 입력이며, P3-B의 합친 순위277/278이고 노출자리는0이다. 원문 본문을 모델에 표시하지 않고 path만 확인하여 감사기의 문서 경로 판별을 고쳤다. 최초 결과는 ranking-audit-initial.json/md에 남겼다. 실험·corpus·봉인·노출 파일은 수정하지 않았다.", ""]
    if discrepancies:
        report += ["## 불일치 행", ""]
        for item in discrepancies:
            report.append(f"- `{item['check']}` · `{item['row']}` · {json.dumps(item['detail'], ensure_ascii=False)}")
    else:
        report += ["모든 순위·노출의 독립 재계산이 저장 원장과 일치했다. 의미상 좋은 검색이라는 결론은 이 일치에서 나오지 않는다.", ""]
    (HERE / "ranking-audit.md").write_text("\n".join(report))
    # Safe stdout: counts, row IDs, flags, hashes only; never source text.
    print(json.dumps({k: summary[k] for k in ["status", "disagreement_count", "catalog_files", "searches", "exposure_events", "full_ranking_files", "full_ranking_rows", "slots", "nonempty_slots", "empty_slots", "adjacent_slots", "excerpt_fallback_rows", "short_file_padded_rows"]}, ensure_ascii=False, indent=2))
    return 0 if not discrepancies else 1


if __name__ == "__main__":
    raise SystemExit(audit())
