"""Merge existing source/access ledgers; count original works once, never access rows.

Run from repository root with:
  python -B docs/workstreams/research/AF-RES-070/tools/merge_sources.py
The script reads all four streams afresh and writes only SOURCES.jsonl and
evidence/source-audit.json under the AF-RES-070 owned path.
"""
import collections
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[1]
REPOSITORIES = {
    "rclone": "rclone/rclone",
    "ripgrep": "BurntSushi/ripgrep",
    "pandoc": "jgm/pandoc",
    "jq": "jqlang/jq",
}
DIRECTIONS = {
    "rclone": "backup_transfer",
    "ripgrep": "file_search",
    "pandoc": "document_conversion",
    "jq": "json_query",
}
FIELDS = [
    "source_id", "lineage_id", "repository_direction", "author", "original_url",
    "pinned_url", "version_date", "section_lines", "accessed_utc",
    "selection_reason", "direct_read", "verified_claim", "cannot_determine",
    "contrary_or_unknown", "count_toward_minimum", "access_status", "origin_ledger",
]
MISSING = "미기록"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canon_repo(repo):
    if repo.lower() in {"stedolan/jq", "jqlang/jq"}:
        return "jqlang/jq"
    for target in REPOSITORIES.values():
        if repo.lower() == target.lower():
            return target
    return repo


def url_identity(url):
    """Identity of original work, ignoring comments, revisions, and mirror URLs."""
    if not url:
        return None
    parsed = urlsplit(str(url))
    parts = parsed.path.strip("/").split("/")
    if parsed.hostname == "api.github.com" and len(parts) >= 5 and parts[0] == "repos":
        repo = canon_repo("/".join(parts[1:3]))
        if parts[3] == "issues" and parts[4].isdigit():
            return f"github:{repo}:issue:{parts[4]}"
    if parsed.hostname == "github.com" and len(parts) >= 4:
        repo = canon_repo("/".join(parts[:2]))
        if parts[2] == "issues" and parts[3].isdigit():
            return f"github:{repo}:issue:{parts[3]}"
        if parts[2] in {"blob", "raw"} and len(parts) >= 5:
            file_path = "/".join(parts[4:])
            if repo == "jqlang/jq" and file_path.endswith("manual.yml"):
                file_path = "docs/content/MANUAL_LOGICAL_WORK"
            return f"github:{repo}:file:{file_path}"
    if parsed.hostname == "raw.githubusercontent.com" and len(parts) >= 4:
        repo = canon_repo("/".join(parts[:2]))
        file_path = "/".join(parts[3:])
        if repo == "jqlang/jq" and file_path.endswith("manual.yml"):
            file_path = "docs/content/MANUAL_LOGICAL_WORK"
        return f"github:{repo}:file:{file_path}"
    return None


def version_url(url):
    """Fixed file revision identity used only for documented reading-cost counts."""
    parsed = urlsplit(str(url or ""))
    return parsed._replace(fragment="", query="").geturl()


def timestamp(raw):
    return raw.get("accessed_utc") or raw.get("started_utc") or raw.get("completed_utc") or raw.get("ended_utc")


def parse_utc(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace(" UTC", "+00:00").replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def status(raw, access=False):
    if raw.get("access_status"):
        return raw["access_status"]
    http = raw.get("http_status") or raw.get("status")
    text = " ".join(str(raw.get(k, "")) for k in ("kind", "status", "error", "verified_claim"))
    error = re.search(r"\b(40[0-9]|50[0-9])\b", text)
    if isinstance(http, int) and http >= 400:
        return f"failed_http_{http}"
    if error and ("fail" in text.lower() or "error" in text.lower() or "HTTP" in text):
        return "failed_http_" + error.group(1)
    if any(term in text.lower() for term in ("not_found", "no_file_at_path", "access_failed", "access_failure")):
        return "failed_unresolved"
    if http == 200 or http in {"success", "original_recovered"} or raw.get("found") is True:
        return "access_success" if access else "opened"
    if access and "comment_count" in raw and raw.get("sha256"):
        return "access_success_comment_receipt"
    if not access and raw.get("direct_read") is True:
        return "opened"
    return str(raw.get("status") or "not_recorded")


input_receipts = []
source_inputs = []
access_inputs = []
for stream in REPOSITORIES:
    folder = BASE / "streams" / stream
    for path in sorted(folder.glob("*.jsonl")):
        if "source" not in path.name and not path.name.startswith("access"):
            continue
        data = path.read_bytes()
        origin = str(path.relative_to(BASE))
        rows = [json.loads(line) for line in data.decode().splitlines() if line.strip()]
        input_receipts.append({"path": origin, "sha256": digest(data), "rows": len(rows)})
        for row_number, raw in enumerate(rows, 1):
            entry = {"stream": stream, "origin": origin, "row_number": row_number, "raw": raw}
            (source_inputs if "source" in path.name else access_inputs).append(entry)

alias_to_canonical = {}
source_url_to_lineages = collections.defaultdict(set)
for entry in source_inputs:
    raw = entry["raw"]
    identity = url_identity(raw.get("original_url")) or url_identity(raw.get("pinned_url")) or raw.get("lineage_id")
    entry["lineage"] = identity
    if raw.get("lineage_id"):
        alias_to_canonical[raw["lineage_id"]] = identity
    for field in ("original_url", "pinned_url"):
        if raw.get(field):
            source_url_to_lineages[(entry["stream"], version_url(raw[field]))].add(identity)


def access_lineage(entry):
    raw = entry["raw"]
    identity = url_identity(raw.get("url"))
    if identity:
        return identity
    if raw.get("lineage_id") in alias_to_canonical:
        return alias_to_canonical[raw["lineage_id"]]
    number = raw.get("number") or raw.get("issue")
    if number is None:
        match = re.search(r"(?:REST-|ARCHIVE-?|HTML-?|EDITS?-?|DIAG-)(\d+)", raw.get("access_id", ""))
        if match:
            number = match.group(1)
    if number is not None and str(number).isdigit():
        return f"github:{REPOSITORIES[entry['stream']]}:issue:{number}"
    related = source_url_to_lineages.get((entry["stream"], version_url(raw.get("url"))), set())
    if len(related) == 1:
        return next(iter(related))
    return "access-url:" + version_url(raw.get("url"))


rows = []
source_missing = []
access_missing = []
scope_warnings = []
duplicate_count_suppressed = []
for entry in source_inputs:
    raw = entry["raw"]
    row = dict(raw)
    row.update({
        "source_id": raw.get("source_id"),
        "lineage_id": entry["lineage"],
        "repository_direction": DIRECTIONS[entry["stream"]],
        "author": raw.get("author") or MISSING,
        "original_url": raw.get("original_url") or MISSING,
        "pinned_url": raw.get("pinned_url") or raw.get("original_url") or MISSING,
        "version_date": raw.get("version_date") or MISSING,
        "section_lines": raw.get("section_lines") or MISSING,
        "accessed_utc": timestamp(raw),
        "selection_reason": raw.get("selection_reason") or MISSING,
        "direct_read": raw.get("direct_read") is True,
        "verified_claim": raw.get("verified_claim") or MISSING,
        "cannot_determine": raw.get("cannot_determine") or MISSING,
        "contrary_or_unknown": raw.get("contrary_or_unknown") or MISSING,
        "count_toward_minimum": raw.get("count_toward_minimum") is True and raw.get("direct_read") is True,
        "access_status": status(raw),
        "origin_ledger": entry["origin"],
        "origin_row": entry["row_number"],
        "origin_lineage_id": raw.get("lineage_id"),
        "origin_repository_direction": raw.get("repository_direction"),
        "origin_count_toward_minimum": raw.get("count_toward_minimum"),
        "record_class": "source_claim",
    })
    missing = [key for key in FIELDS if key not in {"origin_ledger", "access_status"} and (raw.get(key) is None or raw.get(key) == "")]
    if missing:
        source_missing.append({"source_id": row["source_id"], "origin_ledger": entry["origin"], "fields": missing})
    if row["kind"] != "original_issue" and not row["kind"].startswith("official_"):
        row["count_toward_minimum"] = False
    if str(row["access_status"]).startswith("failed"):
        row["direct_read"] = False
        row["count_toward_minimum"] = False
    issue_match = re.search(r":issue:(\d+)$", row["lineage_id"] or "")
    if issue_match:
        own = issue_match.group(1)
        for field in ("verified_claim", "cannot_determine", "contrary_or_unknown", "section_lines"):
            other = sorted(set(re.findall(r"#(\d+)", str(row[field]))) - {own})
            if other:
                scope_warnings.append({"source_id": row["source_id"], "field": field, "other_issue_numbers": other, "status": "cross_issue_text_not_independent_evidence_for_this_source", "action": "해당 원작의 판별 주장으로 확대하지 않음. 봉인 원장은 보존하며 이 경고를 적용."})
    rows.append(row)

existing_source_ids = {row["source_id"] for row in rows}
for entry in access_inputs:
    raw = entry["raw"]
    identity = access_lineage(entry)
    sid = raw.get("source_id") or "ACCESS-" + (raw.get("access_id") or f"{entry['stream']}-{Path(entry['origin']).stem}-{entry['row_number']:04d}")
    state = status(raw, access=True)
    failure = state.startswith("failed")
    original = raw.get("url") or MISSING
    if ":issue:" in identity:
        repo, issue = identity.removeprefix("github:").split(":issue:", 1)
        original = f"https://github.com/{repo}/issues/{issue}"
    access_time = timestamp(raw)
    raw_missing = []
    if not raw.get("url"):
        raw_missing.append("url")
    if access_time is None:
        raw_missing.append("accessed_utc")
    if raw_missing:
        access_missing.append({"source_id": sid, "origin_ledger": entry["origin"], "origin_row": entry["row_number"], "fields": raw_missing})
    row = {
        "source_id": sid,
        "lineage_id": identity,
        "repository_direction": DIRECTIONS[entry["stream"]],
        "author": "접근 원장에는 원저자 미기록; 같은 계보의 source_claim 행을 참조",
        "original_url": original,
        "pinned_url": raw.get("url") or MISSING,
        "version_date": raw.get("event_created_at") or raw.get("issue_created_at") or MISSING,
        "section_lines": raw.get("content_read") or raw.get("purpose") or raw.get("type") or "접근 응답·메타데이터만; 원문 판독 절은 source_claim 행 참조",
        "accessed_utc": access_time,
        "selection_reason": raw.get("purpose") or raw.get("type") or raw.get("stage") or raw.get("phase") or "원자료 접근과 최초판 확인의 실행 이력",
        "direct_read": False,
        "verified_claim": ("이 접근의 실패 상태만 확인: " if failure else "이 접근의 응답·메타데이터만 기록: ") + state,
        "cannot_determine": "접근 성공만으로 원문의 실질 판독·주장 참·작성자 성공을 추론하지 않는다. 실제 읽은 내용은 같은 계보의 source_claim을 참조.",
        "contrary_or_unknown": raw.get("error") or raw.get("note") or raw.get("disclosure") or ("본문 복구·수정이력 확인 불가" if failure else "추가 원저작으로 재산입하지 않음"),
        "count_toward_minimum": False,
        "access_status": state,
        "origin_ledger": entry["origin"],
        "origin_row": entry["row_number"],
        "record_class": "access_receipt",
        "kind": "access_failure" if failure else "access_record",
        "access_id": raw.get("access_id"),
        "access_metadata": raw,
        "direct_read_basis": "접근 이력 행에서는 원문의 실질 판독 여부를 새로 추론하지 않음; source_claim과 별개 필드",
    }
    rows.append(row)

# Prefer the chronologically earliest eligible original-work record. Source IDs
# are never renamed. Manual/code revisions and issue archive/comment mirrors
# share the canonical lineage and therefore cannot increase the work count.
eligible = sorted((r for r in rows if r["count_toward_minimum"]), key=lambda r: (parse_utc(r["accessed_utc"]) or float("inf"), r["origin_ledger"], r["origin_row"]))
counted_by_lineage = {}
for row in eligible:
    identity = row["lineage_id"]
    if identity in counted_by_lineage:
        row["count_toward_minimum"] = False
        row["counting_exclusion"] = "same_original_work_already_counted"
        row["counted_source_id"] = counted_by_lineage[identity]
        duplicate_count_suppressed.append({"source_id": row["source_id"], "lineage_id": identity, "counted_source_id": counted_by_lineage[identity]})
    else:
        counted_by_lineage[identity] = row["source_id"]
for row in rows:
    if row["lineage_id"] in counted_by_lineage:
        row.setdefault("counted_source_id", counted_by_lineage[row["lineage_id"]])

ids = [row["source_id"] for row in rows]
duplicate_ids = sorted(s for s, n in collections.Counter(ids).items() if n > 1)
if duplicate_ids:
    raise ValueError("Source IDs are not unique; fix origin ledgers, do not silently rename: " + repr(duplicate_ids))
if any(set(FIELDS) - set(row) for row in rows):
    raise AssertionError("Normalized field missing")

direction_stats = {}
cost_sections = {}
for stream, direction in DIRECTIONS.items():
    subset = [r for r in rows if r["repository_direction"] == direction]
    claims = [r for r in subset if r["record_class"] == "source_claim"]
    counted = [r for r in subset if r["count_toward_minimum"]]
    issues = [r for r in claims if r.get("kind") == "original_issue"]
    official = [r for r in claims if r.get("kind", "").startswith("official_") and r["direct_read"]]
    intervals = set()
    unparsed = []
    section_detail = []
    for row in official:
        ranges = re.findall(r"L(\d+)\s*[-–—]\s*L?(\d+)", row["section_lines"])
        if not ranges:
            unparsed.append(row["source_id"])
        for start, end in ranges:
            key = (row["lineage_id"], version_url(row["pinned_url"]), int(start), int(end))
            intervals.add(key)
        section_detail.append({"source_id": row["source_id"], "lineage_id": row["lineage_id"], "version_url": version_url(row["pinned_url"]), "recorded_sections": row["section_lines"], "explicit_intervals": [[int(a), int(b)] for a, b in ranges]})
    direction_stats[direction] = {
        "repository": REPOSITORIES[stream],
        "source_claim_rows": len(claims),
        "access_receipt_rows": sum(r["record_class"] == "access_receipt" for r in subset),
        "counted_original_works": len(counted),
        "counted_original_issues": sum(r["kind"] == "original_issue" for r in counted),
        "counted_official_works": sum(r["kind"].startswith("official_") for r in counted),
        "original_issues_accessed": len({r["lineage_id"] for r in issues}),
        "original_issue_partial_or_not_substantively_read": [r["source_id"] for r in issues if not r["direct_read"]],
        "failed_access_or_recovery_record_rows": sum(str(r["access_status"]).startswith("failed") for r in subset),
        "reading_cost": {
            "cost_coverage": "declared-section lower bound; navigation/overshoot not exhaustively quantified",
            "official_document_lineages_directly_read": len({r["lineage_id"] for r in official}),
            "official_document_versions_directly_read": len({(r["lineage_id"], version_url(r["pinned_url"])) for r in official}),
            "explicit_section_intervals_in_source_ledgers": len(intervals),
            "official_source_rows_without_parseable_line_interval": unparsed,
            "issue_body_documents_substantively_read": sum(r["direct_read"] for r in issues),
            "navigation_only_access_document_rows": sum("navigation" in str(r.get("access_metadata", {})).lower() for r in subset if r["record_class"] == "access_receipt"),
        },
    }
    cost_sections[direction] = section_detail

counted = [r for r in rows if r["count_toward_minimum"]]
totals = {
    "normalized_rows": len(rows),
    "source_claim_rows": len(source_inputs),
    "access_receipt_rows": len(access_inputs),
    "counted_original_works": len(counted),
    "counted_original_issues": sum(r["kind"] == "original_issue" for r in counted),
    "counted_official_works": sum(r["kind"].startswith("official_") for r in counted),
    "original_issues_accessed": sum(s["original_issues_accessed"] for s in direction_stats.values()),
    "source_row_missing_field_records": len(source_missing),
    "access_row_missing_execution_metadata_records": len(access_missing),
    "failed_access_or_recovery_record_rows": sum(str(r["access_status"]).startswith("failed") for r in rows),
}
groups = collections.defaultdict(list)
for row in rows:
    groups[row["lineage_id"]].append(row["source_id"])
alias_groups = [{"lineage_id": key, "source_ids": value, "counted_source_id": counted_by_lineage.get(key)} for key, value in sorted(groups.items()) if len(value) > 1]
changed = [r["path"] for r in input_receipts if digest((BASE / r["path"]).read_bytes()) != r["sha256"]]
audit = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "command": "python -B docs/workstreams/research/AF-RES-070/tools/merge_sources.py",
    "cwd": str(BASE.parents[3]),
    "exit_code": 0,
    "input_files": input_receipts,
    "input_files_changed_during_merge": changed,
    "required_fields": FIELDS,
    "totals": totals,
    "minimum_checks": {"at_least_20_original_works": len(counted) >= 20, "at_least_12_original_issues": totals["counted_original_issues"] >= 12, "at_least_8_official_works": totals["counted_official_works"] >= 8, "all_four_directions": all(s["counted_original_works"] > 0 for s in direction_stats.values())},
    "by_direction": direction_stats,
    "count_rules": [
        "원저작은 원 이슈 또는 실질 판독한 독립 공식 문서/코드 파일이다. source_claim의 direct_read=true이고 원장이 산입한 경우만 후보로 삼는다.",
        "같은 이슈의 본문/댓글/아카이브는 한 계보이며, 같은 공식 파일의 다른 판과 여러 절도 한 계보이다. jq 매뉴얼 경로 변경과 stedolan→jqlang 저장소 이름 변경을 정규화한다.",
        "탐색용 re-export/메타데이터·제목만·접근 실패·검색 응답·부분 로그로 실질 판독을 주장하지 않는 행은 산입하지 않는다. jq2329는 접근한 이슈에 포함하되 실질 판독 최소량에서 제외한다.",
        "접근 성공 행의 direct_read=false는 그 접근 이력 자체가 내용 판독을 증명하지 않음을 뜻한다. 같은 계보 source_claim의 실제 판독 기록을 부정하지 않는다.",
        "같은 계보에서 산입 후보가 여럿이면 기록된 접근 시각이 가장 이른 한 행만 true로 남기고 나머지의 원래 값과 제외 사유를 보존한다. 기존 source_id는 변경하지 않는다."
    ],
    "reading_cost_rules": [
        "비용 표는 시간·토큰·금전 대신 문서와 절을 센다. 이슈 본문 문서, 공식 문서 계보, 공식 문서 판을 분리한다.",
        "공식 절 수는 source 원장에 실제 기록된 고정 문서판+명시적 L시작-L끝 구간의 고유 조합이다. 같은 판의 동일 구간 재사용은 한 번, 다른 판은 별도 판독 구간이다. 같은 줄 구간 안의 논리적 소절 수를 임의로 늘리지 않는다.",
        "이 절 수는 기록된 구간 비용이며 모든 네트워크 요청이나 눈으로 지나친 줄의 완전한 비용이 아니다. 같은 원작 여러 절을 원저작 수로 늘리지 않는다.",
        "A/B 후보별 2문서×문서당1절 준수 여부는 봉인 pre/pins의 별도 기준이다. 본 표의 저장소 전체 판독 구간 수가 개별 후보 예산을 대신하지 않는다.",
        "공식 source_claim에 없는 navigation-only 접근은 별도 문서 행으로 표시하되 지정 절을 복원할 수 없으면 절 수를 만들지 않는다. 검색 결과 페이지는 원저작/공식 절 수에서 제외한다."
    ],
    "duplicates": {"duplicate_source_ids": duplicate_ids, "suppressed_true_count_rows": duplicate_count_suppressed, "lineage_groups_with_multiple_records": alias_groups},
    "field_audit": {"source_row_missing_fields_before_normalization": source_missing, "access_row_missing_execution_metadata": access_missing, "normalized_key_presence_complete": True, "unknown_values_not_fabricated": True, "pandoc_missing_time_addendum": "streams/pandoc/access-time-addendum.json; 두 실패 접근의 정확 UTC 복원 불가를 명시"},
    "claim_scope_audit": {
        "claim_limit_or_counterevidence_missing": [r["source_id"] for r in rows if r["record_class"] == "source_claim" and any(r[k] == MISSING for k in ("verified_claim", "cannot_determine", "contrary_or_unknown"))],
        "cross_issue_scope_warnings": scope_warnings,
        "reviewed_boundaries": [
            {"source_ids": ["RCL-D1", "RCL-I4911"], "finding": "사용 종료 버퍼 계약과 모든 전송 완료 필드는 동일하지 않음. 특정 메모리 관측 시점을 A가 이미 답했다고 확정하지 않음.", "review": "streams/ripgrep/cross-review.json#CR-RCL4911"},
            {"source_ids": ["SRC-JQ-I2349", "SRC-JQ-AUX16"], "finding": "특정 무키 항목 보존 목적과 여러 무키 항목에 대한 일반 병합정책을 구분. 코드가 작성자 목적이나 실사용 성공을 대신 증명하지 않음.", "review": "streams/ripgrep/cross-review.json#CR-JQ2349"},
            {"source_ids": ["RCL-D4"], "finding": "한 함수에 직접 검사문이 없다는 독해는 하위 호출 전체 보호 부재를 입증하지 않음; source의 cannot_determine에 한계가 명시됨."},
            {"source_ids": ["PAN-D08"], "finding": "re-export navigation 파일은 직접 열었어도 독립 행동 판별 원저작 최소량에서는 false."},
            {"source_ids": ["RG-I1808-COMMENTS", "PAN-I7113-COMMENTS"], "finding": "수정된 현재 댓글과 다른 필드의 후속 반례를 최초 생성시점의 선택 B 또는 독립 성공으로 재사용하지 않음."}
        ],
        "limit": "원장 병합과 주장 범위 감사이며 모든 공식 코드를 새로 실행하거나 모든 출처를 독립 재현한 검사가 아니다. 직접 판독 여부는 각 stream의 실행 이력·해시와 함께 읽는다."
    },
    "jq_access_addendum_present": any(e["stream"] == "jq" for e in access_inputs) or any(r["repository_direction"] == "json_query" and str(r["access_status"]).startswith("failed") for r in rows),
    "pending": (["ROOT가 별도 보완할 jq 역사 저장소명 아카이브 실패·빈 잘못된 문서 경로 접근 기록은 해당 access*.jsonl 저장 후 이 스크립트를 재실행하여 반영"] if not (any(e["stream"] == "jq" for e in access_inputs) or any(r["repository_direction"] == "json_query" and str(r["access_status"]).startswith("failed") for r in rows)) else []) + ["최종 결과 SHA의 GitHub 재열람 대조는 ROOT 최종 검증에서 수행"],
}
output = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
(BASE / "SOURCES.jsonl").write_text(output)
audit["output_sources_sha256"] = digest(output.encode())
(BASE / "evidence").mkdir(exist_ok=True)
(BASE / "evidence/source-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"exit_code": 0, "totals": totals, "minimum_checks": audit["minimum_checks"], "input_files_changed": changed}, ensure_ascii=False))
