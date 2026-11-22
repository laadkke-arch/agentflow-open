#!/usr/bin/env python3
"""Reopen a scoped set of Q1–Q8 primary locations; record failures honestly.

Does not recalculate case evidence or add documents to the literature minimum.
Only hashes, locations, and short original summaries are persisted.
"""
import hashlib
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1]
TARGETS = [
    {"questions": ["Q1"], "source_id": "ADR-I01", "url": "https://raw.githubusercontent.com/backstage/backstage/ffe93e7aa7ebcc429ed98bfd02810314a6f27c73/docs/architecture-decisions/index.md",
     "location": "Creating an ADR; Superseding an ADR; actual file inventory is separately pinned in streams/adr/frame_inventory.json", "markers": ["Creating an ADR", "architecture-decisions"], "finding": "같은 고정판의 ADR 저장/기여 절차. index 자체가14개 목록을 열거하는 것은 아님."},
    {"questions": ["Q2"], "source_id": "RUST-I2285", "url": "https://github.com/rust-lang/rust/pull/47046",
     "location": "PR body and merge timeline", "markers": ["1946", "CommonMark", "2018-01-23"], "finding": "원 RFC 구현 PR와 CommonMark 제약 논의 및 병합 시점이 있는 공개 기록을 다시 읽음."},
    {"questions": ["Q3"], "source_id": "B-022", "url": "https://raw.githubusercontent.com/google/go-cloud/38a09e97496915ea40567701513208c505685202/blob/azureblob/azureblob.go",
     "location": "Package azureblob; Open URLs; Authentication", "markers": ["Package azureblob", "Open URLs", "azblob"], "finding": "원 기능 추가 commit의 Azure Blob 공급 범위와 URL 조건을 확인. 공개 push/팀승인일로 바꾸지 않음."},
    {"questions": ["Q4"], "source_id": "RUST-F04", "url": "https://github.com/rust-lang/rfcs/pull/2287",
     "location": "issuecomment-356850346 and issuecomment-356850830; provider comment not required in this partial HTML recheck", "markers": ["356850830", "Criterion"], "finding": "Criterion 소개와 제안자의 선행 검토 댓글 위치를 재확인. 공급자댓글357104198은 이번HTML에없으며 기존 전체 원문 열람과 구별."},
    {"questions": ["Q5", "Q8"], "source_id": "B-030", "url": "https://www.frank-mitchell.com/projects/duplicate-files/2023-03-07-py/",
     "location": "numbered code L12–15,158,173–178; Summary of Changes", "markers": ["simplejson", "PathEncoder", "2023-03-07"], "finding": "선택적 simplejson import와 PathEncoder 출력 경계, YAML/CLI 후속 추가. 실제 실행 환경은 여전히 불명."},
    {"questions": ["Q6"], "source_id": "AP-J31", "url": "https://issues.apache.org/jira/browse/FLINK-10653",
     "location": "Time Tracking; parent/subtask status; child external shuffle services", "markers": ["13h", "50m", "FLINK-13247"], "finding": "13h50m 집계와 열린 외부 서비스 하위 이슈를 확인. 이름/시점별 worklog는 불명."},
    {"questions": ["Q7"], "source_id": "CF-P1", "url": "https://www.epo.org/boards-of-appeal/decisions/pdf/t132074eu1.pdf",
     "location": "FactsI–IV and reasons3.3–3.9,4.3–4.6; root web re-open turn684795807view0", "markers": [], "finding": "EPO 공식 심판 PDF를 재개방. 원 심사 dossier의403은 별도 갭으로 유지."},
    {"questions": ["Q7"], "source_id": "CF-E1", "url": "https://joelchan.github.io/files/2014-cogsci-analogy.pdf",
     "location": "Methods and Tables10–12; root web re-open turn684795807view1", "markers": [], "finding": "저자 호스팅 원 연구 PDF를 재개방. 동일 팀 자료의 재분석을 독립 연구로 세지 않음."},
    {"questions": ["Q8"], "source_id": "RUST-V01", "url": "https://spec.commonmark.org/0.27/#link-destination",
     "location": "6.5 Links: link destination; examples460–461", "markers": ["2016-11-18", "link-destination", "ASCII space"], "finding": "당시 공개 명세의 link destination 제약을 확인. 링크의 존재와 팀의 최초 인지는 별개."},
]


def read(target):
    result = {k: v for k, v in target.items() if k != "markers"}
    result["checked_utc"] = datetime.now(timezone.utc).isoformat()
    try:
        request = Request(target["url"], headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=35) as response:
            body = response.read()
            result.update({"http_status": response.status, "final_url": response.url,
                           "content_type": response.headers.get("Content-Type")})
        result["bytes"] = len(body)
        result["sha256"] = hashlib.sha256(body).hexdigest()
        text = body.decode("utf-8", "replace")
        result["markers_found"] = {needle: needle.lower() in text.lower() for needle in target["markers"]}
        result["met"] = result["http_status"] == 200 and all(result["markers_found"].values())
        result["limitation"] = "Re-access/marker check only; not independent corroboration or historical runtime verification."
    except Exception as error:
        result.update({"met": False, "error": str(error), "next_action": "retry the exact public original or documented provider connector; never replace with search snippet"})
    return result


parser = argparse.ArgumentParser()
parser.add_argument("--source", action="append", help="Recheck only this source ID, retaining earlier results for other IDs")
args = parser.parse_args()
targets = [target for target in TARGETS if not args.source or target["source_id"] in args.source]
with ThreadPoolExecutor(max_workers=5) as pool:
    current_rows = list(pool.map(read, targets))
if args.source and (BASE / "evidence/link-check.json").exists():
    old = json.loads((BASE / "evidence/link-check.json").read_text())
    merged = {row["source_id"]: row for row in old["rows"]}
    merged.update({row["source_id"]: row for row in current_rows})
    rows = [merged[target["source_id"]] for target in TARGETS]
else:
    rows = current_rows
report = {"scope": "one or more real primary locations for each Q; no new literature counting",
          "rows": rows,
          "web_open_failures": [
              {"source_id": sid, "error": "DisabledError in web open; ordinary public HTTP GET retried separately"}
              for sid in ("ADR-I01", "RUST-I2285", "B-022", "RUST-F04")],
          "covered_questions_with_success": sorted({q for row in rows if row["met"] for q in row["questions"]})}
(BASE / "evidence/link-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"passed": sum(row["met"] for row in rows), "total": len(rows),
                  "covered_questions": report["covered_questions_with_success"],
                  "failed": [{"source_id": r["source_id"], "error": r.get("error"), "markers": r.get("markers_found")} for r in rows if not r["met"]]}, ensure_ascii=False))
