# 실행자가 복사할 비어 있는 판정 양식 (v1; 실제 자료 없음)

연구자가 승인·동의 후 별도 보안 저장소에 생성. 공개 GitHub에는 개인 로그/실험 결과 원본 업로드 금지; 비식별 파생표는 별도 검토. event-dictionary.csv 정의 우선, revisions.md 수정 규칙 우선. 각 ID는 무작위 가명, 누락 코드를 명시; 전후 원파일과 해시, 테스트 영수증, 채점자의 원행을 연결. 아래 헤더는 빈 양식이며 0이나 공석을 채운 관측 행이 아님.

## 배정 원장(모든 배정, 후보 아님)
```csv
participant_id,assignment_id,session_id,task,period,sequence,condition,assigned_utc,baseline_seal_at,t0_hash,t12minus_hash,t24_hash,terminal_hash,termination_status,last_observed_at,off_protocol,missing_code
```
한 사람×과제당 1개. 무작위 배정 후 시작 전 탈락/기술 오류/포기 기록. 배정 전 자리 VACANT. 실제 배정된 사람만 ITT N. t12− 고정 checkpoint는 지연군 첫 카드 전에 seal.

## 사건/후보 판정 원장(코더 각자)
```csv
assignment_id,participant_id,session_id,candidate_id,artifact_id,coder_id,rule_version,prior_free_recall_id,prior_family_state,prior_name_state,prior_condition_state,prior_application_state,prior_evidence_ids,first_content_visible_id,offer_event_id,source_channel,source_url,resolved_url,source_snapshot_hash,open_event_id,understanding_evidence_id,attempt_event_id,edit_actor_receipt,from_hash,to_hash,function_diff_id,change_class,replacement,retained_t12minus,retained_t24,retained_terminal,other_path_evidence_id,post_reason_id,attribution,missing_code,rival,reverse_observation,allowed_claim
```
판독 규칙 순서: actor/task/lineage/시간 검증 → 사전 4차원 각각 → exposure별 제공/보임/열람/이해/시도 → 기능 diff, 실제 교체, 되돌림 → 원인 경쟁 설명 → 가림 품질·인수와 결합. K/N_CONSISTENT/U가 섞일 수 있다. 기존 코드 없으면 planning change 또는 first implementation만 기록. 코드 없는 동일 사용자 후기 의견도 교체 아님. 판독자 독립 원행 보존. 조정자가 어떤 gate에 이견인지 기록, 원판정 덮어쓰지 않는다.

## blind 채점 / 운영 인수 양식
```csv
blind_alias,artifact_hash,task,rubric_hash,interpreter_version,runner_id,test_receipt_id,per_vector_expected,per_vector_got,no_mutation,type_ok,test_verdict,reviewer_id,review_id,independent,blind_inference,review_verdict,review_reason,review_seconds
```
별도 인수:
```csv
assignment_id,artifact_hash,acceptor_id,acceptance_id,rubric_hash,review_id,decision_utc,verdict,reason,active_seconds,missing_code
```
요구 적합+벡터 통과+코드/비용 상의 미해결 요구 없음+별도 수락이 모두 관측되어야 accepted. 미제출/거절/보류 따로. 같은 산출물 수정을 검수자가 했다면 author provenance와 reviewer 노동을 별도로 기록.

## 사람시간(사건 원장과 join)
```csv
activity_id,assignment_id,actor_id,actor_role,activity_type,start_utc,end_utc,start_mono_ns,end_mono_ns,active_seconds,elapsed_seconds,phase,review_id,from_hash,to_hash,missing_code
```
정상 공석 VACANT, 관측된 없음 OBS_NO, 관측된 0 OBS_ZERO, 미측정 U_UNOBSERVED, 자료 충돌 U_CONFLICT, join 실패 U_JOIN, 비적용 NA. active interval 합집합 사람별, actor 간 더함. wall elapsed 더하지 않음. idle/wait/연구자 coding overhead 별도.

## 집계용 빈 두 표
| task×period×Z | 배정 N | 미시작/포기/기술오류 | 카드 제공/보임/열람 | known / novelty-consistent / unknown | 교체 Y/N/U | 독립 품질 pass/fail/U | 인수 accepted/rejected/pending/not submitted/U | 오염/기록 손실 | 비용 관측 N/U |
|---|---:|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |

| task×period×Z | 분석 분모 | author pre/search/impl/test/rework min | reviewer/acceptor min | wait elapsed | total person-min / missing | accepted | 비용/accepted | 성공자 조건부 평균(별도) |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

각 phase의 실제 수는 비어 있음. all-assigned main table과 accepted-only table 분리; successful-only은 선택편향 가능. 4 synthetic fixture는 별도 namespace. 연구 실행/개인 자료/결과는 미생성. 
