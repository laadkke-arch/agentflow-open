#!/usr/bin/env python3
"""Independently trace the 12 displaced exposure slots without new body reads.

Inputs are the fixed protocol, exposure/access/judgment records, corpus metadata,
and existing source notes. Cached bodies are read only to validate recorded hashes.
The experiment/seal scripts and public outcome bodies are not read or imported.
"""

from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
import pathlib
import subprocess


HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parent.parent
REPO = BASE.parents[3]
SEAL2 = "d03ca37daf0c43688c68bc39417d84a9b84803e9"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_json(path):
    return json.loads(path.read_text())


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


# Analyst interpretation is deliberately separated from mechanically derived facts.
# These notes refer only to the already recorded section summaries and judgments.
NOTES = {
    ("J2", "JQ-0080"): {
        "core_content": "누락 필드/범위 밖 접근의 null 및 변수 바인딩을 보여 주는 상류 기대출력.",
        "assessment": "A는 C3의 입력 누락 진단에 이 시험을 반환했다. B도 유지된 JQ-0001:408-435로 같은 null 진단을 했다. 시험이라는 별도 근거 형식은 없어졌지만 누락 offset의 출처나 필수조건 완결은 어느 경로도 확보하지 못했다.",
        "lost_detail": "누락값 진단의 독립된 원시험 예시가 B 반환에서 빠짐.",
        "qualitative_loss_type": "corroboration",
    },
    ("J2", "JQ-0072"): {
        "core_content": "객체 pair 문법을 컴파일하는 parser 구현.",
        "assessment": "A가 읽은 3971-4002는 객체 문법 확인이며 최종 조건 근거로 쓰지 않았다. C1은 유지된 매뉴얼로 지지되고 C2 매핑/C3 offset 누락은 그대로다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("J3", "JQ-0004"): {
        "core_content": "range/3의 증가 조건을 구현한 jq 내장 함수.",
        "assessment": "A는 147-165를 확인했지만 사용하지 않았다. A/B 모두 유지된 manual의 range·인덱스·병합 절과 JQ-0080의 기대출력으로 C1/C2를 지지했다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("J3", "JQ-0002"): {
        "core_content": "plus가 문자열·배열·객체에 따라 동작을 나누는 구현.",
        "assessment": "A는 92-114를 확인했지만 사용하지 않았다. 같은 타입별 의미가 두 경로의 manual/원시험 반환에 남아 있어 기록된 조건 지지는 감소하지 않았다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("J4", "JQ-0002"): {
        "core_content": "match의 문자열 입력·global flag, Oniguruma 컴파일, Oniguruma 없는 build에서의 실패 분기.",
        "assessment": "A는 C1에 이 파일을 사용·반환했다. B는 유지된 manual의 match/foreach 계약으로 같은 조건을 지지하지만, A의 구체적인 Oniguruma 부재 경고는 B 반환에 없다. 이것은 설명의 반대조건 손실이며 사전 문서상 완결 또는 실제 runtime 성공의 관찰 손실과 같지 않다.",
        "lost_detail": "Oniguruma 없는 jq build에서 match 계열을 사용할 수 없다는 구체적 반대조건.",
        "qualitative_loss_type": "build_failure_caveat",
    },
    ("J4", "JQ-0055"): {
        "core_content": "JSON 파서의 유효 literal 요구.",
        "assessment": "A는 506-544를 확인했지만 사용하지 않았다. raw-input으로 로그를 문자열로 다루어야 한다는 조건은 유지된 manual:124-148이 직접 설명한다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P1", "PD-0007"): {
        "core_content": "FAQ의 형식 변환·참조 스타일 설명.",
        "assessment": "A가 읽은 139-230은 최종 조건 근거가 아니며 simpara role→custom-style 복구를 닫지 못했다. 두 경로의 반박은 유지된 DocBook reader 및 manual로 설명된다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P1", "PD-0016"): {
        "core_content": "server API의 reference-doc 옵션 및 filter/외부 HTTP 제한.",
        "assessment": "이 server API는 원 사용자의 CLI와 다르며 A의 최종 조건 근거가 아니다. 읽은 절에는 DocBook role 복구가 없다는 원 메모가 남아 있다. 이를 제거한 것이 CLI 복구의 실패 원인이라는 관찰은 없다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P3", "PD-1324"): {
        "core_content": "빈 metadata와 MediaWiki RawInline/RawBlock 예제가 있는 native 기대출력 fixture.",
        "assessment": "원 요청은 YAML signature/template이다. 다른 reader이고 metadata가 비어 있어 A도 이 파일을 조건 근거로 사용하지 않았다. A/B의 최종 구성은 유지된 manual 하나에 근거한다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P3", "PD-0022"): {
        "core_content": "-V 문자열 변수와 metadata/template 변수 옵션을 구분하는 CLI parser.",
        "assessment": "초기 -V 후보를 이해하는 데는 쓰였지만 R chunk 값의 전달 시점은 입증하지 못했다. 사전 최종 판정은 원 생산 경로를 유지하는 raw HTML scalar 구성으로 바뀌었고 이 파일을 사용·반환하지 않았다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P4", "PD-0007"): {
        "core_content": "FAQ의 일반 변환 설명.",
        "assessment": "A가 읽은 95-121은 원 TikZ 그림의 AST→PDF→SVG 접합을 닫는 최종 근거가 아니다. 두 경로의 최종 반환은 유지된 Lua-filter 예제와 manual이다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
    ("P4", "PD-0008"): {
        "core_content": "reader→AST→filter→writer의 일반 구조와 필터 예시.",
        "assessment": "일반 필터 구조는 확인했으나 정확한 TikZ preamble/그림 보존을 독립 지지하지 않는다. 원 기록은 반환한 PD-0012/PD-0001에 전체 문서상 구성을 귀속하며 이 파일을 사용하지 않는다.",
        "lost_detail": None,
        "qualitative_loss_type": None,
    },
}


def audit():
    started = utc()
    errors = []
    input_checks = []
    section_checks = []

    def require(test, check, detail):
        if not test:
            errors.append({"check": check, "detail": detail})

    def sealed_input(path):
        data = path.read_bytes()
        relative = path.relative_to(REPO).as_posix()
        result = subprocess.run(["git", "show", f"{SEAL2}:{relative}"], cwd=REPO,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        equal = result.returncode == 0 and data == result.stdout
        require(equal, "seal2_exact_input", relative)
        input_checks.append({"path": relative, "sha256": sha(data),
                             "seal2_sha256": sha(result.stdout) if result.returncode == 0 else None,
                             "exact_bytes_equal": equal})
        return data

    protocol_path = BASE / "protocol.json"
    sealed_input(protocol_path)
    protocol = read_json(protocol_path)
    cases = [c for c in protocol["cases"] if c["stratum"] == "boundary"]
    require(len(cases) == 6, "boundary_count", len(cases))
    corpus = {r["file_id"]: r for r in read_rows(BASE / "corpus-files.jsonl")}
    notes = {}
    for path in [BASE / "evidence/jq/sources-note.jsonl", BASE / "evidence/pandoc/sources-note.jsonl"]:
        for row in read_rows(path):
            notes[row.get("file_id", row["source_id"])] = row

    output_rows, case_rows = [], []
    for case in cases:
        cid = case["case_id"]
        routes = {}
        for arm in ["A", "B"]:
            route_dir = BASE / "evidence/routes" / f"{cid}-{arm}"
            for name in ["exposure.json", "access.jsonl", "judgment.json"]:
                sealed_input(route_dir / name)
            routes[arm] = {
                "exposure": read_json(route_dir / "exposure.json"),
                "access": read_rows(route_dir / "access.jsonl"),
                "judgment": read_json(route_dir / "judgment.json"),
            }
        a, b = routes["A"], routes["B"]
        a_slots, b_slots = a["exposure"]["slots"], b["exposure"]["slots"]
        a_j, b_j = a["judgment"], b["judgment"]
        a_top2 = [s["file_id"] for s in a_slots[:2]]
        b_top2 = [s["file_id"] for s in b_slots[:2]]
        require(a_top2 == b_top2, "retained_main_top2", cid)
        require(all(s["role"] == "adjacent" for s in b_slots[2:]), "replacement_is_adjacent", cid)
        b_ids = {s["file_id"] for s in b_slots if not s["empty"]}
        b_conditions = {c["condition_id"]: c for c in b_j["condition_evidence"]}
        a_conditions = {c["condition_id"]: c for c in a_j["condition_evidence"]}
        condition_comparison = [{"condition_id": c["id"], "requirement": c["requirement"],
                                 "a_status": a_conditions[c["id"]]["status"],
                                 "b_status": b_conditions[c["id"]]["status"],
                                 "same_status": a_conditions[c["id"]]["status"] == b_conditions[c["id"]]["status"]}
                                for c in case["conditions"]]
        b_rank_path = BASE / b["exposure"]["full_merged_ranking"]
        sealed_input(b_rank_path)
        b_ranks = {r["file_id"]: index for index, r in enumerate(read_rows(b_rank_path), 1)}
        case_rows.append({"case_id": cid, "a_judgment": a_j["judgment"], "b_judgment": b_j["judgment"],
                          "a_only_complete": a_j["judgment"] == "완결" and b_j["judgment"] != "완결",
                          "retained_main_top2": a_top2,
                          "condition_comparison": condition_comparison,
                          "a_judgment_url": f"https://github.com/laadkke-arch/agentflow-open/blob/{SEAL2}/docs/workstreams/research/AF-RES-096/evidence/routes/{cid}-A/judgment.json",
                          "b_judgment_url": f"https://github.com/laadkke-arch/agentflow-open/blob/{SEAL2}/docs/workstreams/research/AF-RES-096/evidence/routes/{cid}-B/judgment.json"})

        for slot in a_slots[2:]:
            fid = slot["file_id"]
            require(fid not in b_ids, "displaced_not_exposed_B", [cid, fid])
            opens = [x for x in a["access"] if x["event"] == "body_attempt" and x["file_id"] == fid]
            successful = [x for x in opens if x["status"] == "success"]
            require(len(opens) == len(successful) == 1, "one_successful_A_open", [cid, fid, len(opens)])
            require(not any(x["event"] == "body_attempt" and x["file_id"] == fid for x in b["access"]),
                    "no_hidden_B_open", [cid, fid])
            sections = [x for x in a["access"] if x["event"] == "section_navigation" and x["file_id"] == fid]
            require(bool(sections), "recorded_section_exists", [cid, fid])
            body = (BASE / successful[0]["opened_body"]).read_bytes()
            require(sha(body) == corpus[fid]["sha256"] == successful[0]["body_sha256"],
                    "displaced_body_hash", [cid, fid])
            body_lines = body.decode().splitlines()
            row_section_checks = []
            for sec in sections:
                selected = "\n".join(body_lines[sec["start_line"] - 1:sec["end_line"]]).encode()
                correct = sha(selected) == sec["section_sha256"]
                require(correct, "recorded_section_hash", [cid, fid, sec["start_line"], sec["end_line"]])
                check = {"case_id": cid, "file_id": fid, "start": sec["start_line"], "end": sec["end_line"],
                         "section_sha256": sec["section_sha256"], "hash_matches": correct}
                section_checks.append(check)
                row_section_checks.append(check)
            references = [c for c in a_j["condition_evidence"] if fid in c["evidence_file_ids"]]
            sole = [c["condition_id"] for c in references if c["evidence_file_ids"] == [fid]]
            return_item = next((x for x in a_j["returned_sources"] if x["file_id"] == fid), None)
            source_note = notes.get(fid, {})
            note_fields = {k: source_note[k] for k in ["directly_verified", "directly_observed", "limitations_unknown", "limitations_unverified"] if k in source_note}
            original_nonuse = [x for x in a_j.get("examined_but_not_used", []) if x["file_id"] == fid]
            require((cid, fid) in NOTES, "analyst_note_exists", [cid, fid])
            output_rows.append({
                "case_id": cid, "a_slot": slot["slot"], "a_global_rank": slot["merged_global_rank"],
                "a_main_rank": slot["within_role_rank"], "b_full_global_rank_unexposed": b_ranks[fid],
                "file_id": fid, "repo": slot["repo"], "path": slot["path"], "url": slot["url"],
                "body_sha256": sha(body), "replacing_b_slot": b_slots[slot["slot"]-1]["file_id"],
                "opened_A": len(successful) == 1, "exposed_B": fid in b_ids, "opened_B": False,
                "used_A": fid in a_j["used_file_ids"], "returned_A": return_item is not None,
                "returned_sections_A": return_item["sections"] if return_item else [],
                "recorded_A_sections": row_section_checks,
                "condition_references_A": references,
                "sole_evidence_file_for_A_condition_ids": sole,
                "same_conditions_B": [b_conditions[c["condition_id"]] for c in references],
                "original_nonuse_record": original_nonuse,
                "source_note_summary": note_fields,
                "a_judgment": a_j["judgment"], "b_judgment": b_j["judgment"],
                "a_only_complete_observed": a_j["judgment"] == "완결" and b_j["judgment"] != "완결",
                "attribution": "기계집계: 봉인 노출/접근/판정. 내용: 기존 연구자 원 메모. 손실 해석: 사후 독립 감사자의 추론.",
                "analyst_note": NOTES[(cid, fid)],
            })

    require(len(output_rows) == 12, "displaced_slot_count", len(output_rows))
    conditions = [r for case in case_rows for r in case["condition_comparison"]]
    result = {
        "audit": "independent-displacement-v1", "started_utc": started, "finished_utc": utc(),
        "pre_outcome_result_sha": SEAL2, "postseal_secondary_analysis": True,
        "primary_judgments_modified": False, "new_external_body_opens": 0,
        "public_answer_or_comment_bodies_read": False,
        "auditor_exposure_note": "봉인 이후 조건·원판정·이미 기록된 절 요약을 읽었다. J2 노출 구조 탐색 중 기존 exposure 발췌도 표시되었으며 이를 별도 원문 열람이나 승패 근거로 쓰지 않았다. 본문 캐시는 hash 검사만 수행했다.",
        "boundary_pairs": len(cases), "displaced_slot_denominator": len(cases)*2,
        "displaced_slots_reviewed": len(output_rows),
        "unique_displaced_files": len({r["file_id"] for r in output_rows}),
        "opened_A_displaced_slots": sum(r["opened_A"] for r in output_rows),
        "used_A_displaced_slots": sum(r["used_A"] for r in output_rows),
        "returned_A_displaced_slots": sum(r["returned_A"] for r in output_rows),
        "A_only_complete_boundary_pairs": sum(r["a_only_complete"] for r in case_rows),
        "displaced_slots_in_A_only_complete_pairs": sum(r["a_only_complete_observed"] for r in output_rows),
        "sole_evidence_condition_displaced_slot_pairs": sum(len(r["sole_evidence_file_for_A_condition_ids"]) for r in output_rows),
        "explicit_conditions_compared": len(conditions),
        "explicit_condition_status_differences": sum(not c["same_status"] for c in conditions),
        "qualitative_loss_observations": [
            {"case_id": r["case_id"], "file_id": r["file_id"], "kind": r["analyst_note"]["qualitative_loss_type"],
             "detail": r["analyst_note"]["lost_detail"]}
            for r in output_rows if r["analyst_note"]["lost_detail"]
        ],
        "exact_seal2_inputs_checked": len(input_checks),
        "recorded_section_hashes_checked": len(section_checks),
        "seal2_input_checks": input_checks, "section_checks": section_checks,
        "cases": case_rows, "slots": output_rows,
        "limits": [
            "관찰0은 봉인된 여섯 경계쌍의 문서상 완결 손실 0이다. 범위 확장의 실제 안전성이나 모든 가능한 요청에서 손실 없음이라는 명제가 아니다.",
            "조건이 한 파일만 인용하는지와 파일 제거의 인과적 필요성은 다르다. 본 감사는 재실험 없이 기록된 조건·반환·판정의 관계를 추적했다.",
            "새 원문 절을 열지 않아 기록되지 않은 절에 필수조건의 유일한 해법이 있는지는 미확인이다. 원 메모와 hash의 일치가 모든 해석의 참을 입증하지 않는다.",
            "동일 연구자의 양 경로 기억 노출과 큰 manual이 상위 두 자리에 유지되는 구조가 손실 관찰을 줄일 수 있다. 독립 평가자/파일 분할은 새 실험이어야 한다.",
            "실행 성공이나 사용자판 실패를 관찰한 분석이 아니다. 특히 J4 build 반대조건의 누락을 완결 패배로 사후 재분류하지 않았다.",
        ],
        "next_minimal_observation": "새 질문에서 필수 조건을 해결하는 주 도구 절이 실제 3/4위 파일에만 있고 1/2위에는 없다는 사전 판별을 봉인한 뒤, 독립 평가자가 두 노출 집합으로 같은 입력을 처리하도록 한다. 결과를 아는 현 8질문은 재모집하지 않는다.",
        "error_count": len(errors), "errors": errors, "status": "PASS" if not errors else "FAIL",
    }
    (HERE / "displacement-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    md = ["# AF-RES-096 밀려난 주 도구 12자리 독립 감사", "",
          f"**{result['status']} · 오류 {len(errors)}건. 탐색 {len(output_rows)}/12, A만 완결 관찰 {result['A_only_complete_boundary_pairs']}/6쌍.**", "",
          f"분석 기준은 사전 봉인 `{SEAL2}`다. 노출·접근·최종 판정은 수정하지 않았다. 여섯 경계 요청의 A 3·4위를 전수 추적했으며, 사후 답/댓글과 새 외부 본문은 열지 않았다. 공식 원문의 내용은 기존 절 메모·조건 판정에 귀속하고, 캐시 본문은 기록된 hash만 기계 검산했다.", "",
          "|요청·A순위|밀려난 파일·기존 절|기록된 핵심 내용|A 사용/반환|필수조건 손실 검토|",
          "|---|---|---|---|---|"]
    for row in output_rows:
        ranges = ", ".join(f"{s['start']}-{s['end']}" for s in row["recorded_A_sections"])
        note = row["analyst_note"]
        md.append(f"|{row['case_id']} · {row['a_main_rank']}|[{row['file_id']}]({row['url']}) `{row['path']}` · {ranges}|{note['core_content']}|{'예' if row['used_A'] else '아니오'}/{'예' if row['returned_A'] else '아니오'}|{note['assessment']}|")
    md += ["", "## 분자와 분모", "",
           f"- 경계쌍 {len(cases)}건 × 주 도구 두 자리 = **{len(output_rows)}자리**, 서로 다른 파일 **{result['unique_displaced_files']}개**. 반복 파일을 새 자료로 늘리지 않았다.",
           f"- A 실제 열람 **{result['opened_A_displaced_slots']}/12**, A 최종 판정 사용 **{result['used_A_displaced_slots']}/12**, A 반환 **{result['returned_A_displaced_slots']}/12**. B 노출·열람은 0/12다.",
           f"- 명시 조건 **{len(conditions)}개**의 A/B 상태를 비교했고 차이는 **{result['explicit_condition_status_differences']}개**다. 밀려난 파일만을 단독 근거로 적은 전체 조건은 **{result['sole_evidence_condition_displaced_slot_pairs']}개**다. 단독 인용 여부는 인과적 필요성과 같지 않다.",
           f"- A만 문서상 완결 **{result['A_only_complete_boundary_pairs']}/6쌍**. A만 완결 사례에서 밀려난 자리 **{result['displaced_slots_in_A_only_complete_pairs']}/12**. 알려진 사례를 넣거나 사후 원문으로 이 분자를 채우지 않았다.",
           f"- ②봉인과 **{len(input_checks)}개 입력**의 bytes가 정확히 일치하고, 밀려난 파일의 기존 **{len(section_checks)}개 절** hash를 재계산했다. 새 body 접근은 **0회**다.", "",
           "## 완결 손실과 설명 손실을 구별", "",
           "관찰된 필수조건 완결 손실은 없었다. 그러나 모든 설명이 같아진 것은 아니다. J2-B의 반환은 J2-A가 붙인 누락키/null 상류 fixture의 별도 확인을 잃었다. J4-B는 J4-A가 반환한 Oniguruma 없는 build의 구체적인 실패 경고를 잃었다. 두 차이는 원 판정에 기록된 사실이며, 이 감사는 이를 반례 설명의 손실로 남긴다. 실제 사용자 build 실패나 문서상 완결 패배로 사후 승격하지 않는다.", "",
           "## 사실·추론·설계 제안", "",
           "**사실:** 노출 ID·원 순위·열람 절·사용/반환 ID와 A/B 판정은 고정 원장에서 재계산했다. 원문 내용 요약은 처음 읽은 연구자의 메모에 귀속한다.", "",
           "**추론:** 현재 표본에서는 필요한 큰 manual/원시험이 상위 두 자리에 남아, 3·4위를 바꾸어도 최종 요구 충족 상태가 달라지지 않았다. 이것이 모든 요청에서 성립하거나 같은 연구자의 기억 영향을 배제한다는 결론은 아니다.", "",
           f"**설계 제안 / 다음 최소 확인:** {result['next_minimal_observation']}", "",
           "## 적용 한계", ""]
    md += [f"- {item}" for item in result["limits"]]
    md += ["", "## 감사 입력과 재실행", "",
           "각 고정 judgment 링크·해시·원 절·전체 조건 비교는 displacement-audit.json에 있다. 루트 experiment.py/seal_routes.py나 사후 승패 요약을 호출하지 않았다.", "",
           "```bash", "python -B docs/workstreams/research/AF-RES-096/evidence/audit/audit_displacement.py", "```", "",
           "## 오류", ""]
    md += [json.dumps(e, ensure_ascii=False) for e in errors] or ["없음."]
    (HERE / "displacement-audit.md").write_text("\n".join(md)+"\n")
    keys = ["status", "error_count", "boundary_pairs", "displaced_slots_reviewed", "unique_displaced_files",
            "opened_A_displaced_slots", "used_A_displaced_slots", "returned_A_displaced_slots",
            "A_only_complete_boundary_pairs", "explicit_conditions_compared", "explicit_condition_status_differences",
            "exact_seal2_inputs_checked", "recorded_section_hashes_checked"]
    print(json.dumps({k: result[k] for k in keys}, ensure_ascii=False, indent=2))
    if errors:
        print(json.dumps(errors, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(audit())
