# AF-RES-050 · HANDOFF

**판정: partial(부분 인계).** 공개성에 무관하게 고정 소프트웨어6군과 분야 대조2군을 유지했다. Q1~Q7 모두 직접 근거 또는 구체적인 미확인·재개 조건을 붙였지만, 자료 배당과 참가자 원자료 연결은 완전 충족하지 못했다. 이 인계서는 아래 최종 결과판의 원격 재열람과 실제 session check가 끝난 뒤에 작성했다.

## 고정 결과·시작판·커밋

- 브랜치: `work/research-af-res-050`
- **최종 결과 SHA: `5797f9a9f1a1f0281d54c1922c6698a53093b67a`**
- 계획 통합판: `d8c8d029bfb6107520ae74d2a172b2b18840e764`
- 배정/시작 당시 실제 통합판: `522ea9092d4d56ef6db0bd4f707bfc90032e179e`
- 최종 check가 확인한 원격 통합판: `2875c1af816d6f376c061fffef20b739fd0af005`; 계약 hash는 유지되었고 check는 passed였다.
- 읽은 의존 HANDOFF: AF-RES-034 `f6dc9b8873b049f1eb4f8977ce3408ed057df1f7`, AF-RES-046 `40030229bfa87f92f9875cdf5937fe382af8cb57`
- 별도 고정 labor.csv 판: `d8a2c696046e28adb68cdfb75d4104454e48dd52`
- 모든 편집·제출 경로: `docs/workstreams/research/AF-RES-050/`. `dot-control.json` 변경은 없다.

| 묶음 | 원격 커밋 | 보존한 내용 |
| --- | --- | --- |
| ① | f3c8de473b52a64c92c862cc64927ce787525c1a | 외부 새 관측 전 표본·선정·종점·분모 규칙, manifest/start |
| ② | 35576f16914c9f62b5c4d91bf015092b2e93aa34 | 고정 입력·출처·기준선 |
| ③ | 9cb61b4f5952c3b3b8b32f6be27239d06d55f404 | 실제 필드·기수·연결 계약·반례·원장 |
| ④ | 5a86c940a28ab4d06c45acba20c652e49e8f941b | RESULT·SELF_CHECK·수용 원장·독립 검토 |
| 검증 | 5797f9a9f1a1f0281d54c1922c6698a53093b67a | 고정판 원격 재열람·session 실제 출력·종료코드 |
| 최종 인계 | 이 HANDOFF.md만 추가하는 후속 단독 커밋 | 결과판5797f9a9의 재확인 뒤 작성; 자체 SHA는 git 이력에서 확인 |

수용 원장의 `GATE-HANDOFF`는 결과판 시점에는 pending이다. 마지막 커밋을 HANDOFF 단독으로 남겨야 하므로 그 파일을 미리 성공으로 바꾸지 않았다. 이 문서가 추가된 최종 커밋의 변경 경로가 HANDOFF.md 한 개라는 git 이력이 마지막 게이트의 증거다.

## 두 표와 제출물 위치

| 산출물 | 위치·용도 |
| --- | --- |
| 필수 표1 | [RESULT.md](RESULT.md) 1–10줄;8군의 개입·배정·시간·품질·키·연결 범위 |
| 필수 표2 | RESULT.md 12–39줄;26종점 행, 공개행 기술통계/저자 집계/식별 불가 구별 |
| 말미 약점3건 | RESULT.md 166–170줄;이 인계서 마지막에도 같은 표 보존 |
| 질문별 점검 | [SELF_CHECK.md](SELF_CHECK.md);Q1~Q7의 근거행·반대증거·결손·재개 행동 |
| 수용 원장 | [evidence/acceptance-evidence.json](evidence/acceptance-evidence.json);27조건과7질문 dossier |
| 사전 규칙·표본 | [SCOPE.md](SCOPE.md), [studies.csv](studies.csv);고정8군과 보강 선정0군 |
| 연결·종점 | [joins.csv](joins.csv)16행, [outcomes.csv](outcomes.csv)26행, [analysis-procedure.md](analysis-procedure.md) |
| 출처·줄 위치 | [sources.jsonl](sources.jsonl), [evidence/line-index.json](evidence/line-index.json) |
| 반례·정정 | [counterexamples.md](counterexamples.md), [CORRECTIONS.md](CORRECTIONS.md), [evidence/review-result.json](evidence/review-result.json) |
| 시작·판 정보 | [manifest.json](manifest.json), [evidence/session-start.json](evidence/session-start.json), [PROGRESS.md](PROGRESS.md) |

## 핵심 결과와 부분 충족

**배정×시간×최종품질 공동 원자료로 새 비교를 계산할 수 있는 연구군은 관측0/8, 주표본0/6이다.** 효과0이라는 추정이 아니다. 실제 조인을 못 한 표의 입력·미연결 수는 미확인으로 남겼다. 새 노동 절감시간·동등품질 시간쌍·추적 재작업 절감 숫자는 산출하지 않았다.

확보한 부분 참가자행은 NCQ1군이다. NCQ의142/156 snippet행을 각각20 P×T그룹으로 확인했지만 T조건 코드북·시각·최종검사 파일이 없다. CodeMend361행/360고유키는 검색 질의 평가표이므로 사람 대장에 포함하지 않는다. Blueprint20그림 위치는 paste/완료상태만 연결되고3미완료가 남는다. Strata6/6은 조건×과제 평균의 제작 계보이며 참가자행이 아니다. 최소 두 군에서 익명행 대장을 찾기 위한 구체적 탐색은 수행했으나 두 군의 참가자 대장 확보 요건은 보수적으로 부분 충족1/2로 판정했다. [J-NA-01/02; BC-J02/04; J-US-AGG; AC-08]

**반례:** NCQ의 선택 중앙값380→57초와 총849→847초를 서로 다른 종점으로 유지했다. eXoaDocs는 전체40분 내 all-pass3/12 대1/12지만 Task3통과는3/12 대4/12로 반대 방향이고 시간 포함자와 pass자 키가 없다. Blueprint 완료자 평균에는1/2미완료가 빠진다. Strata precision90.1%/91.0%와 recall 관계 불일치, Chan153명/표151명을 임의 정정하지 않았다. 도구·후보·훈련 묶음을 동일 링크 설명 한 요소의 효과로 귀속하지 않았다. [RESULT Q1~Q6; counterexamples.md]

| 자료 수 | 실제 값 | 해석 |
| --- | --- | --- |
| 출처 기록 | 143 | 직접열람 표시97,실패/미열람46;고유 저작 수와 다름 |
| 실질적으로 직접 읽은 고유1차저작 | 25 | 검색·실패·판복제·동일 패키지 구성파일 제외 |
| 배당 적격 저작 | 19 | 원논문8,저자 별도 연구자료2,독립 과제/구현3,방법/추가6 |
| 지정 배당 충족 슬롯 | 17/24 | 8/8·2/6·3/6·6/4;초과 방법2개를 다른 층에 전용하지 않음 |
| 부족 | 저자자료4·과제/구현3 | 총7슬롯. 추가 특허·선별 탈락 논문으로 채우지 않음 |
| 보강 | 선정0군 | 사전 질의 반환34기록은 고유연구34가 아님;전수조사 주장 없음 |

자료 배당 미달, 두 번째 익명 참가자 대장 미확보, 공동키 부재 때문에 **완전 완료로 인계하지 않는다**. 저자 연락·새 참가자 모집·미공개 데이터베이스 접근 없이 공개 자료에서 확인 가능한 범위까지 수행했다. 실패 URL과 최소 추가 파일은 각 source 실패행·studies/joins에 남겼다.

## 실제 실행·미실행

| 명령/작업 | 입력 | 실제 상태·출력 |
| --- | --- | --- |
| 지정 session start --fetch | manifest의 실제 통합판·의존2SHA·허용경로 | exit0;evidence/session-start.json |
| `python -B docs/workstreams/research/AF-RES-050/streams/ncq-exoa/audit_ncq.py` | 고정 ce14f193… CSV1/2 | exit0;ncq-row-audit.json |
| `"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/audit_public_release.py` | 고정445d5d8… 공개 release파일 | exit0;execution.json/artifact-inspection.json |
| `python -B docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py strata` | arXiv2102.06231v2 source tar | exit0;reproduced-strata.json |
| 같은 스크립트 `unakite` 모드 | 공식 source map | exit0;reproduced-unakite.json |
| `python -B docs/workstreams/research/AF-RES-050/build_ledgers.py` | 커밋된 분담 JSON/JSONL | exit0;8studies/16joins/26outcomes/143sources |
| `python -B docs/workstreams/research/AF-RES-050/verify_ledgers.py --documents` | 최종 문서·원장 | exit0;364검사 통과,evidence/validation-documents.json |
| 지정 session check --fetch | 결과판5a86c940의 manifest | exit0,passed;전체 stdout/stderr는 evidence/session-check.json |
| 같은 check 최종 재실행 | 최종 결과판5797f9a9의 manifest | exit0,passed;아래 실제 전체 stdout과 stderr 보존 |
| 사람별 시간–품질/실패 포함 재추정 | 배정·시각·최종검사 공동행 필요 | 미실시:필수 파일·코드북 미확보 |
| 저자 분석/도구·참가자 코드 실행 | 논문 실험판·entry point·입력파일 필요 | 미실시:실험 원자료/판/실행 입력 미확인;정적 파일 감사만 수행 |

최종 문서와 원장 검사는 효과 재현 검사가 아니다. 읽기 전용 분석 절차는 analysis-procedure.md의 입력 계약과 join 순서를 따른다. 저자 분석의 실행명령·입력 파일이 공개판에서 확인되지 않은 경우 존재하지 않는 명령을 만들어 쓰지 않았다. 다음 공개 파일을 얻기 전에는 사람 조인이나 효과 계산을 재개할 수 없다.

## 막힌 이유·다음 첫 행동

**첫 행동:** NCQ의 공개 `(experiment,P,T)→condition,problem,period` 코드북과 시행별 시작/선택/제출/최종검사 export가 있는지 고정 프로젝트·논문 연결 경로에서 확인한다. 최소 입력은 각 실험20대상시행의 배정·시각·최종score·중단사유, 실험2예약14명의 흐름/철회단계다. 확보 전 T1/T2를 조건으로 해석하지 않는다.

그다음 Strata `CSCW 2020 Participants Tracking.xlsx`의 공개 비식별판과 이유별score/gold·계산식, Schwonke 후보dataset77/78의 실제 코호트 crosswalk와 공개 transaction/posttest export를 확인한다. Blueprint/CodeMend는 person×task×condition×period×time×completion×grade와 실제 과제판이 필요하다. eXoaDocs는24명 배정·문서-event·검사 결과의 공유키와 시간표 포함자 지시자가 필요하다. Unakite는 실험별40/32시행의 배정·영상코딩·설명 채점 export가 필요하다.

새 공개자료를 받을 때 첫 실행 검사는 배정 자연키 유일성→event/채점의1:N→배정 left join→실제 전후 행수/미연결/탈락 분모다. 기존 감사 재현은 위 명령과 입력 SHA 그대로 가능하다. 완성한 새 원장은 `python -B docs/workstreams/research/AF-RES-050/build_ledgers.py`와 `python -B docs/workstreams/research/AF-RES-050/verify_ledgers.py --documents`로 일관성을 다시 검사한다. 독립군에 가짜 짝을 만들거나 cap을 실제 완료시간으로 대입하지 않는다.

**색인 제안:** AF-RES-050 | 공개 실험의 배정·시간·품질 연결 감사 | 고정8군·공동 원자료 비교0군·자료배당17/24 | partial | RESULT.md / HANDOFF.md.

## 최종 원격 재열람 영수증

두 필수 표와 수용원장을 정확한 결과 SHA에서 GitHub로 다시 읽고 게시 payload와 모든 문자를 비교했다. 아래는 실제 최종 재열람 기록이다.

```json
{
  "result_commit": "5797f9a9f1a1f0281d54c1922c6698a53093b67a",
  "checked_at_utc": "2026-11-23 00:53:27 UTC",
  "status": "pass",
  "required_sections_verified": 3,
  "required_sections": 3,
  "items": [
    {
      "file": "RESULT.md",
      "git_blob_sha": "d3d1b9ec5d8d10df40f14bc14e054811ccf279ef",
      "exact_content_match": true,
      "characters": 24632,
      "display_url": "https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/RESULT.md"
    },
    {
      "file": "evidence/acceptance-evidence.json",
      "git_blob_sha": "bdbb93d15212087d41b64119afb8c5bee53a5157",
      "exact_content_match": true,
      "characters": 66722,
      "display_url": "https://github.com/laadkke-arch/agentflow-open/blob/5797f9a9f1a1f0281d54c1922c6698a53093b67a/docs/workstreams/research/AF-RES-050/evidence/acceptance-evidence.json"
    }
  ],
  "table_locations": {
    "table1": "RESULT.md:1-10",
    "table2": "RESULT.md:12-39",
    "final3weaknesses": "RESULT.md:166-170"
  }
}
```

## 최종 session check 실제 출력

명령: `python -B -m workbench.session check docs/workstreams/research/AF-RES-050/manifest.json --fetch`

시작 UTC: `2026-11-23T00:53:33.740987+00:00`; 종료 UTC: `2026-11-23T00:53:41.732534+00:00`; **exit_code: 0**. stderr: 빈 문자열. stdout 전문:

```json
{
  "status": "passed",
  "task_id": "af-res-050",
  "freshness": "remote_checked",
  "checked_at": "2026-11-23T00:53:41.722081+00:00",
  "checked_out_commit": "5797f9a9f1a1f0281d54c1922c6698a53093b67a",
  "task_base_commit": "522ea9092d4d56ef6db0bd4f707bfc90032e179e",
  "integration_commit": "2875c1af816d6f376c061fffef20b739fd0af005",
  "scope_base_commit": "522ea9092d4d56ef6db0bd4f707bfc90032e179e",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-050/CORRECTIONS.md",
    "docs/workstreams/research/AF-RES-050/PROGRESS.md",
    "docs/workstreams/research/AF-RES-050/RESULT.md",
    "docs/workstreams/research/AF-RES-050/SCOPE.md",
    "docs/workstreams/research/AF-RES-050/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-050/analysis-procedure.md",
    "docs/workstreams/research/AF-RES-050/build_ledgers.py",
    "docs/workstreams/research/AF-RES-050/counterexamples.md",
    "docs/workstreams/research/AF-RES-050/evidence/acceptance-evidence.json",
    "docs/workstreams/research/AF-RES-050/evidence/fixed-input-map.json",
    "docs/workstreams/research/AF-RES-050/evidence/line-index.json",
    "docs/workstreams/research/AF-RES-050/evidence/remote-reread.json",
    "docs/workstreams/research/AF-RES-050/evidence/review-ledgers.json",
    "docs/workstreams/research/AF-RES-050/evidence/review-result.json",
    "docs/workstreams/research/AF-RES-050/evidence/session-check.json",
    "docs/workstreams/research/AF-RES-050/evidence/session-start.json",
    "docs/workstreams/research/AF-RES-050/evidence/source-counts.json",
    "docs/workstreams/research/AF-RES-050/evidence/supplement-search-frame.json",
    "docs/workstreams/research/AF-RES-050/evidence/validation-documents.json",
    "docs/workstreams/research/AF-RES-050/evidence/validation-ledgers.json",
    "docs/workstreams/research/AF-RES-050/joins.csv",
    "docs/workstreams/research/AF-RES-050/outcomes.csv",
    "docs/workstreams/research/AF-RES-050/sources.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/REVIEW_CORRECTION.md",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/artifact-inspection.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/audit_public_release.py",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/baseline.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/baseline.md",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/codemend-tree.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/counterexamples.md",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/discovery.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/execution-output.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/execution.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/figure-observations.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/findings.md",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/joins.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/outcomes.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/source-counts.json",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/sources-extension.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/sources.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/studies.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/REVISIONS.md",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/audit_ncq.py",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/baseline.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/capture_retrievals.py",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/counterexamples.md",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/exoa-archive-attempt.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/exoa-archive-final.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/exoa-archive-followup.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/findings.md",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/joins.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/ncq-evaltree-retry.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/ncq-row-audit.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/outcomes.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/source-retrievals-addendum.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/source-retrievals.json",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/sources-addendum.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/sources.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/ncq-exoa/stream-validation.json",
    "docs/workstreams/research/AF-RES-050/streams/root/baseline.json",
    "docs/workstreams/research/AF-RES-050/streams/root/counterexamples.md",
    "docs/workstreams/research/AF-RES-050/streams/root/datashop-catalog-audit.json",
    "docs/workstreams/research/AF-RES-050/streams/root/datashop-discovery.json",
    "docs/workstreams/research/AF-RES-050/streams/root/datashop-metadata-fields.json",
    "docs/workstreams/research/AF-RES-050/streams/root/datashop-target-attempts.json",
    "docs/workstreams/research/AF-RES-050/streams/root/fetch-audit-01.json",
    "docs/workstreams/research/AF-RES-050/streams/root/findings.md",
    "docs/workstreams/research/AF-RES-050/streams/root/joins.json",
    "docs/workstreams/research/AF-RES-050/streams/root/outcomes.json",
    "docs/workstreams/research/AF-RES-050/streams/root/root-data-discovery-exact.json",
    "docs/workstreams/research/AF-RES-050/streams/root/root-data-discovery.json",
    "docs/workstreams/research/AF-RES-050/streams/root/sources-addendum.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/root/sources-metadata.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/root/sources-stimuli-failures.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/root/sources.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/aggregate-join-audit.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/audit-arxiv-source.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/baseline.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/counterexamples.md",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/findings.md",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/joins.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/outcomes.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/reproduced-strata.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/reproduced-unakite.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/search-paths.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/source-counts.json",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/sources.jsonl",
    "docs/workstreams/research/AF-RES-050/streams/unakite-strata/studies.json",
    "docs/workstreams/research/AF-RES-050/studies.csv",
    "docs/workstreams/research/AF-RES-050/verify_ledgers.py"
  ],
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 1. 배정×시간×최종품질·실패 원행 미연결; Strata 품질/Chan 사람분모도 불일치 | 동등 품질 총시간,실패 포함 효과,정확한 불확실성 | [NCQ CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) P/T와논리17행; [Strata 제작자료](https://arxiv.org/src/2102.06231v2) main.tex802/848/850; [Chan Table1](https://joelchan.github.io/files/2011-jmd-distancecommonness.pdf); J-NA-01/02,J-US-03/AGG,J-RT-01 | NCQ코드북·timestamp·최종검사와 철회 ledger;Strata workbook/이유별score;Chan배정표 | 자연키·관측분모·제외 규칙이 연결되고 출판 불일치가 같은 원행으로 해소될 때 |
| 2. 도구·후보·훈련 묶음과 부분 종점; 추적 노동/재작업 계측 미확인 | 동일 링크 설명만의 효과 및 설계자의 전체 재작업 절감 | [Blueprint p518/Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); [Unakite pp8–10](https://lxieyang.github.io/assets/files/pubs/unakite-uist-2019/unakite-uist-2019.pdf); O-NA-01/02,BC-O01~07,O-US-01~03 | 같은 후보 설명 배정과 교육·열람·구현·검사·후속수정 event 계약 | 개입이 분리되고 같은 품질 기준의 전체 활동/추적 시간이 배정 단위에 연결될 때 |
| 3. 직접 자료 배당17/24; 별도 연구자료4·과제/구현3 부족 | 요구된 조사 완결성·공개성 탐색 범위의 확신 | [sources.jsonl](sources.jsonl), [source-counts](evidence/source-counts.json), [검색틀](evidence/supplement-search-frame.json); eXoa실패·DataShop후보행 | 부족한 두 층의 독립 공개 packet/루브릭/복제자료를 정확명·DOI·artifact경로에서 확인 | 중복·검색·실패를 빼고8/6/6/4 각 층을 채우거나 접근불가 범위를 명시한 부분 인계로 수용될 때 |

