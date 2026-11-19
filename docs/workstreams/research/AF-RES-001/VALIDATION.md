# AF-RES-001 — 수행한 검증과 재현 입력

확인: **2026-11-20 KST / 2026-11-19 15:32:46 UTC**. 이 문서는 연구 묶음 커밋 `40f53bec864da98ace69bbfa31c0493c6783dad7`까지의 검사 기록이다. 이후 검증 기록 자체와 마지막 HANDOFF 커밋을 이전 검사에 포함했다고 주장하지 않는다.

## 1. 실제 결과와 범위

| 검사 | 실제 입력/방법 | 결과와 한계 |
| --- | --- | --- |
| JSON/원문·참조 구조 | Python 3.12.14; 아래 §2 코드를 로컬 연구 파일에 실제 실행 | 종료 코드 **0**. 출처 28, 사례 6, 원문 문장 36, 표현 18, 합성 반례 18, 조건부 질문 12. 참조와 원문 일치 검사이며 의미 정확도 자동 판정 아님 |
| 공개 자료 열람 | evidence 3개 기록과 대응 source JSON | 자료별 실제 본문 열람 범위·URL·확인일·버전·한계 기록. 서로 다른 자료 28개; 같은 문서의 버전·절·재열람은 중복 집계하지 않음 |
| 독립 검토 | [REVIEW.md](REVIEW.md)의 원문 6개 주장 묶음·합성 6사례 | 발견 8건의 수정 확인. 내부 별도 에이전트 검토이며 사용자 시험·다른 모델 블라인드 평가 아님 |
| 원격 재열람 | 고정 연구 커밋의 파일 11개 본문을 GitHub에서 다시 fetch; 로컬 Git blob SHA와 반환 blob SHA 대조 | 보정 뒤 **11/11 일치**. [VALIDATION.json](VALIDATION.json)에 파일별 기록 |
| 쓰기 범위 | 기준 `11137686f238b7a7f66e7fdeb72f5f6c49565486` → 연구 `40f53bec864da98ace69bbfa31c0493c6783dad7` GitHub compare | 추가 파일 11개 전부 `docs/workstreams/research/AF-RES-001/` 아래. 공통 파일 변경 없음 |
| 통합 브랜치 변동 | 끝에서 재조회한 foundation `46c874671c6d066292750401d75af50136ef95d6`와 시작 기준 비교 | 다른 과제 AF-RES-002 배정으로 dot-control.json만 3줄 추가/3줄 삭제. AF-RES-001 항목의 JSON 값은 동일. 고정 기준을 바꾸지 않음 |
| 자동 협업 계약 검사 | [Actions run 44555557113](https://github.com/laadkke-arch/agentflow-open/actions/runs/44555557113), 연구 SHA `40f53bec864da98ace69bbfa31c0493c6783dad7` | run·sessions job·검사 step의 completed/success를 읽음. workflow의 실제 명령은 `python -m workbench.session check-all --fetch`. stdout/receipt/숫자 종료 코드는 읽지 않았으며 연구 의미 검증이나 전체 검사 성공으로 확대하지 않음 |

이번 연구는 실행 가능한 제품 과제가 아니므로 신규 workbench manifest를 만들지 않았다. `INPUT_LOCK.json`은 연구 입력 고정 기록이며 workbench 실행 계약으로 위장하지 않는다. 로컬에는 전체 저장소를 checkout하지 않았고 제품 실행·공통 전체 검사·새 모델/API 실행·검색 품질/사용자 실험은 수행하지 않았다.

### 발견한 검사 오류와 조치

1. 첫 로컬 구조 검사에서 종료 코드 1이 발생했다: `File "<stdin>", line 43, AssertionError`. 검사 코드가 `interpretation`과 `proposal_unconfirmed`만 허용해 K05.P3의 `proposal_requires_constraint_change`를 놓쳤다. 해당 문장은 원래부터 조건 변경을 전제하는 미확인 제안이므로 세 번째 상태를 명시적으로 포함했다. 데이터를 통과시키려고 사용자 확인 여부나 참조 검사를 제거하지 않았고 `user_confirmed=false` 등 기존 검사는 유지했다. 보정 후 종료 코드 0을 확인했다.
2. 첫 원격 바이트 대조에서 INPUT_LOCK만 불일치했다. 로컬 끝의 줄바꿈 1개가 더 있었으며 JSON 객체 내용은 같았다. 원격의 이미 커밋된 파일을 기준으로 로컬 줄바꿈을 맞췄고 모든 11개 blob이 일치했다. 고정한 입력 내용·원격 파일은 바꾸지 않았다.
3. 첫 구조 검사 시점에는 마지막 작성 파일인 HANDOFF.md가 아직 없었다. 아래 코드는 이를 `pending_final_file`로 명시해 반환하며, 다른 끊긴 상대 링크는 실패로 처리한다. 최종 인계 작성 시 이 목록이 비었는지 따로 확인한다.

## 2. 재현한 로컬 구조 검사 명령

저장소 루트에서 실행한다. 입력은 고정 연구 커밋의 `CASES.json`, `evidence/*-sources.json`, 연구 디렉터리의 Markdown 파일이다. 다음 코드를 그대로 실행했으며 stdout은 [VALIDATION.json](VALIDATION.json)의 `local_structure`에 보존했다. 문장별 의미 손실 값의 **존재**만 검사한다. 그 내용이 옳다는 판단은 [REVIEW.md](REVIEW.md)의 실제 문장 대조 범위에 한정한다.

```sh
python - <<'PY'
from pathlib import Path
import json, hashlib, re, sys
root = Path("docs/workstreams/research/AF-RES-001")
data = json.loads((root / "CASES.json").read_text())
sources = []
for rel in data["evidence_registry"]:
    registry = json.loads((root / rel).read_text())
    sources.extend(registry["sources"])
ids = [s["id"] for s in sources]
assert len(ids) == len(set(ids)) == 28
assert len({s["url"] for s in sources}) == 28
for s in sources:
    assert s["url"].startswith("https://")
    assert s.get("directly_opened") is True or s.get("read_status", "").startswith("directly_opened")
    assert s.get("read_scope")
    assert s.get("observed") or s.get("confirmed")
    assert s.get("limitations") or s.get("limitation")
    assert s.get("version") or s.get("version_or_locator")
cases = data["cases"]
assert len(cases) == 6
assert len({c["id"] for c in cases}) == 6
counts = {"sources": len(sources), "cases": len(cases), "statements": 0,
          "formulations": 0, "negative_examples": 0, "conditional_questions": 0}
for case in cases:
    assert "synthetic" in case["origin"]
    assert set(case["public_fact_refs"]) <= set(ids)
    orig = case["original"]
    spans = {s["id"]: s["text"] for s in orig["statements"]}
    assert len(spans) == len(orig["statements"]) == 6
    assert orig["full_text"] == "\n".join(s["text"] for s in orig["statements"])
    forms = case["formulations"]
    assert set(forms) == {"A_free_text", "B_light_structure", "C_ai_decomposition_proposal"}
    a,b,c = [forms[k] for k in ("A_free_text", "B_light_structure", "C_ai_decomposition_proposal")]
    assert a["text"] == orig["full_text"]
    assert b["original_ref"] == c["original_ref"] == orig["id"]
    fields = {f["id"]:f for f in b["fields"]}
    proposals = {p["id"]:p for p in c["proposals"]}
    assert len(fields) == 6 and len(proposals) == 3
    assert c["input_read_back"] == b["fields"]
    assert c["preserved_input_fields"] == list(fields)
    for prop in proposals.values():
        assert prop["user_confirmed"] is False
        assert prop["status"] in {"interpretation","proposal_unconfirmed","proposal_requires_constraint_change"}
        assert set(prop["external_basis"]) <= set(ids)
    def check_spans(obj):
        if isinstance(obj,dict):
            for key,value in obj.items():
                if key == "source_spans":
                    assert value and set(value) <= set(spans)
                else:
                    check_spans(value)
        elif isinstance(obj,list):
            for item in obj: check_spans(item)
    check_spans(case)
    mapping = case["original_to_candidate_map"]
    assert len(mapping) == 6 and {m["source_span"] for m in mapping} == set(spans)
    for m in mapping:
        span = m["source_span"]
        expected_fields = [fid for fid,f in fields.items() if span in f["source_spans"]]
        expected_props = [pid for pid,p in proposals.items() if span in p["source_spans"]]
        assert m["B_fields"] == m["C_preserved_fields"] == expected_fields
        assert m["C_proposals"] == expected_props
        assert m["no_proposal_references_span"] == (len(expected_props)==0)
        assert isinstance(m["proposal_only_semantic_loss"], str) and m["proposal_only_semantic_loss"].strip()
    assert len(case["counterexamples"]) == 3
    for neg in case["counterexamples"]:
        assert "researcher_constructed" in neg["origin"]
        assert neg["bad_transformation"] and neg["why_wrong"]
    assert len(case["additional_questions"]) == 2
    for q in case["additional_questions"]:
        assert q["asked_to_user"] is False
        for key in ("only_when","decision_changed_by_answer","if_unanswered"): assert q[key]
    assert case["allowed_without_answer"] and case["stop_inference_at"]
    counts["statements"] += len(spans)
    counts["formulations"] += len(forms)
    counts["negative_examples"] += len(case["counterexamples"])
    counts["conditional_questions"] += len(case["additional_questions"])
pending = set()
for path in sorted(root.rglob("*.md")):
    text = path.read_text()
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in target or target.startswith("#"): continue
        destination = (path.parent / target.split("#")[0]).resolve()
        assert destination.is_relative_to(root.resolve()), (path,target)
        if not destination.exists():
            assert destination == (root / "HANDOFF.md").resolve(), (path,target)
            pending.add("HANDOFF.md")
hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(root.rglob("*")) if p.is_file()}
result = {"status":"PASS", "scope":"syntax, identifiers, reference consistency and file hashes only",
          "counts":counts, "pending_final_file":sorted(pending), "sha256":hashes,
          "python":sys.version.split()[0]}
print(json.dumps(result,ensure_ascii=False,indent=2))
PY
```

## 3. 검사한 11개 파일의 SHA-256

검사한 Git 커밋: `40f53bec864da98ace69bbfa31c0493c6783dad7`.

| 상대 경로 | SHA-256 |
| --- | --- |
| CASES.json | `b0f95a2bf55d061adb052e098ce0dbfc6bb9a071b7f7771694d4450da9710922` |
| INPUT_LOCK.json | `a5c07cd6f5b18a00650ced085cae1ea8a0493ec28a5ec05277ca52512e7551c3` |
| RESEARCH.md | `ee0a115ac7cd70bb29208e7d12a5ad9a9884b9ab93b4db5eedaf7f962a859e0b` |
| REVIEW.md | `d03c50f3325aa7d041ceeddacba615319d14069c5ee9f3bade3995a6fb000e9f` |
| SCOPE.md | `7898240bc9960bf350d33c47246cd6e4de5808d9ebc63e4c82c21aa19dc000bd` |
| evidence/architecture-sources.json | `fd9e963809ea69466526352b4f5b25434719875f02bee9676fe4199516b659b1` |
| evidence/architecture.md | `483954273e1fc95ccc9d5c34a892fcf29b31eb3e12f4dc7fc1ba1cb0ccca771a` |
| evidence/clarification-sources.json | `3ae3f0155dcefd14961ac12b8b5a7a7de94180ac0e04cc960447735cdebce591` |
| evidence/clarification.md | `90f0359b3ce82f63ecec674cf7ee28c05447fbf6b3ed72615cb28d278c5f224d` |
| evidence/software-sources.json | `6f549f4bd9c0ff2e0d57377dba65edd51d9a8f6ef46df421b84230e2b31c6908` |
| evidence/software.md | `164e5c2a4634c0ae134f0b71169be1816057b376f19aca224d00e58aa4e24281` |

이 해시는 로컬 파일의 정확한 바이트를 식별한다. 원격과 비교한 Git blob SHA-1은 파일 길이와 `blob` 헤더를 포함하므로 이 SHA-256과 값이 다르다. 구체 값과 GitHub compare 결과는 VALIDATION.json에 있다.

## 4. 다른 실행 환경에서 필요할 때의 확인

원격 파일을 확인하는 첫 입력은 `work/research-af-res-001`의 최신 SHA와 마지막 HANDOFF다. 이번 연구의 내용 검사는 위 고정 SHA로 재현한다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-001
git show 40f53bec864da98ace69bbfa31c0493c6783dad7:docs/workstreams/research/AF-RES-001/RESEARCH.md
git diff --name-only 11137686f238b7a7f66e7fdeb72f5f6c49565486 40f53bec864da98ace69bbfa31c0493c6783dad7
```

통합 담당이 별도의 전체 환경 검사를 요구하는 경우, 전체 저장소 checkout과 Python 3.12 이상·Git·원격 fetch가 가능한 해당 검사 환경에서 아래 명령을 실행하고 실제 SHA·종료 코드·`.workbench/cloud-check.json` 및 실패 로그를 읽어야 한다. 이 명령은 여기서 실행하지 않았으며 연구 완료의 수행 증거에 포함하지 않는다.

```sh
python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

자료를 더 읽거나 재현 명령을 작성한 일은 실제 제품 실행과 같지 않다. 다음 작업자가 실제로 새 대화를 시작해 이 자료를 이어 받는 시험도 아직 하지 않았다.

