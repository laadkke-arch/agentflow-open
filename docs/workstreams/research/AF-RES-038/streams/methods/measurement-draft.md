# AF-RES-038 · 원자료·결측 판정 초안

이 파일은 사람 시험 전 수집 양식이다. AF-RES-034 고정판의 assignment/activity/submission/rework를 세 군에 확장한다. 예시 사건은 AI가 작성한 논리 점검용 자료이고 실제 참가자·시간·처치 효과가 아니다. 시간값은 모두 null로 남긴다. 구체 과제의 요구 ID는 최종 rubric과 조인한다.

## 실행 전에 잠글 단위

사람을 개별 배정하는 시험이면 사람 한 명을 한 과제의 A/B/C 중 한 군에 배정한다. 배정 비율 1:1:1, 과제·사전 지식 층 안에서 배정한다. 팀이 함께 풀거나 자료를 공유하면 팀을 배정·분석 단위로 바꾸며 팀원을 독립 배정자처럼 세지 않는다. 여러 과제를 한 사람이 풀게 바꾸면 같은 군을 유지하고 사람 안 반복을 표시한다. 같은 사람에게 동일 사건의 다른 군을 뒤이어 보여 주지 않는다.

모집 전에 `run-config`의 공통 훈련, t0/t1 예산, 추적 간격, 허용 도구·검색·지원, 사전 인지 질문, 배정 concealment, 미완료/장애 처리, 품질 경계, 실질 노동 차이, 분석·중단 규칙을 고정한다. 현재 90/60분·7일·비열등성 수치는 미합의이며 이 파일에서 승인된 값으로 사용하지 않는다. 예산이 비어 있는 자료는 내용 준비본이지 즉시 사람 시험 착수판이 아니다.

## 데이터 사전

| 원표 | 필수 열 | 기록·해석 규칙 |
| --- | --- | --- |
| run-config | run_id, packet_hash, rubric_hash, allocation_unit, allocation_ratio, training_policy, t0_budget, t1_budget, followup_gap, tool_policy, search_policy, support_policy, quality_margin, labor_target, missing_plan, stopped_rule, locked_utc | 값이 미정이면 null. 실행 후 수정은 새 version과 이유를 기록 |
| assignment | run_id, unit_id, participant_id, team_id, case_id, arm, allocation_seed_hash, assigned_utc, stratum, prior_domain_score, prior_solution_known, prior_source_seen, enrollment_status, preassignment_exclusion_reason | 전체 배정자 분모. 배정 후 포기·실패·미출석도 삭제하지 않음 |
| exposure | unit_id, case_id, source_id, source_version, source_hash, shown_utc, opened_utc, cited_utc, adopted_decision_id, prior_seen, access_route, future_relative_to_task, cross_arm_shared | 화면 표시·열람·인용·채택을 별개 사건으로 기록. 클릭만으로 읽음/이해를 판정하지 않음 |
| activity | unit_id, person_id, case_id, phase, interval_id, start_utc, end_utc, activity_code, active_seconds, attention_required, interruption_reason, log_available, provenance | search/read/design/code/test_inspect/discuss/active_wait/idle. 동일 사람의 겹치는 구간은 중복 합산 금지. 실행 CPU·wall time과 분리 |
| submission | unit_id, case_id, declaration_id, declared_adopted, first_acceptance_utc, first_submission_hash, first_test_pass_utc, final_submission_hash, t0_end_reason, t1_attended, t1_end_reason, output_available, output_missing_reason | t0 첫 선언+제출판 고정. 첫 테스트 통과나 마지막 저장을 첫 채택으로 바꾸지 않음 |
| decision | unit_id, decision_id, t0_submission_hash, requirement_ids, selected_behavior, rationale, rejected_alternative, invested_work_evidence | 이름이 아니라 행동·조건으로 최초 채택 추적 |
| quality | unit_id, submission_hash, phase, blind_rater_id, requirement_id, grade, critical_violation, evidence_locator, test_result, rater_condition_guess, adjudication_id | grade pass/partial/fail/unverified. 중대 오류 별도. 첫 판독·불일치·조정 판정 모두 보존 |
| rework | unit_id, event_id, old_decision_id, old_submission_hash, new_submission_hash, original_requirement_ids, trigger_code, changed_decision, discarded_work_evidence, repair_interval_ids, subsequent_quality, assessable, exclusion_reason | t0 후 기존 채택을 되돌린 사건만 원요구 재작업 후보. 새 요구/추가 기능/형식 정리/장애는 분리 |
| provider-cost | bundle_id, person_role, cost_event_id, cost_type, start_utc, end_utc, active_seconds, measured, consumers_observed, allocation_rule | 탐색·선별·작성·검수·정정·유지 비용. 실험 운영/채점 연구비와 제품 제공비를 별도 cost_type으로 분리 |
| adjudication | adjudication_id, requirement_id, rater1_grade, rater2_grade, rater1_basis, rater2_basis, disagreement_type, third_rater_grade, final_grade, changed_rubric, resolution_authority | 정답본을 읽은 저자 자기점검, 별도 AI 판독, 외부 사람 2명 합의는 각기 표시 |

`active_seconds`를 생성하지 않은 자료는 계산 가능한 시간 원자료가 아니다. 입력 양식은 JSON null을 사용하고 설명에는 미확인이라고 쓴다. 해당 없음과 누락은 구별한다.

## 판정 순서와 분모

1. 각 군의 전체 배정수 N을 먼저 표시한다. 최종 원요구 통과/중대 오류/부분/결측/채택 전 포기 수를 나란히 둔다. 알려진 미제출은 성공 없음 endpoint로 남기되 미관측 요구별 점수를 0으로 날조하지 않는다.
2. 품질 미확인 u가 있으면 알려진 pass p에 대한 전체 통과율 범위 `[p/N, (p+u)/N]`를 제시할 수 있다. 이 범위는 관측되지 않은 사람의 결과를 추정하거나 대입한 값이 아니다. N=0이면 해당 없음이다.
3. 전체 배정자의 관측 소비 노동을 보고하되 로그 범위·누락자를 함께 보고한다. 일부 구간만 있으면 총노동은 미확인이며 관측된 부분만 합친다. 실패의 적은 노동을 절감 성공으로 해석하지 않는다.
4. t0 채택자 n_adopt를 분모로 한 원요구 재작업 사건률·수정노동은 이차 기술량이다. 서로 다른 군의 채택자는 처치 후 선택되어 비교의 인과 해석이 제한된다. t0 미채택은 재작업 해당 없음, t1 미관측은 미확인, 검증된 무수정은 사건수 0이다. 사건 0이 재검·확인 노동 0을 뜻하지 않는다.
5. 완료자 시간의 분모 n_complete를 따로 쓰며 N과 병기한다. 중단·확정실패·철회·장애를 모두 단순 우측검열로 취급하지 않는다. 성공시간에 임의 0/상한을 넣지 않는다.
6. t0 전 폐기 노동은 초기 활동에 이미 포함된다. 수정노동에 더할 때 버린 초기 작업의 시간을 다시 더하지 않는다. 제공자 노동을 포함한 전체 자원량은 `observed provider labor + sum(observed consumer labor)`이며 실험 운영비는 별도다. 반복 사용자 수와 유지 비용이 미확인이면 1회당 비용·손익분기를 계산하지 않는다.

## 예시 사건의 논리 검사

| fixture | 상태 | 원요구 품질·분모 | 재작업 판정 | 시간값 |
| --- | --- | --- | --- | --- |
| FX01 | 배정 뒤 t0 채택 전 포기, 제출 없음 | N에는 포함, qualifying submission 없음; 요구별 실측 점수는 미확인 | 해당 없음·아직 채택 안 됨 | null |
| FX02 | t0 채택·제출은 있으나 t1 불참 | N 포함, t0 품질 보존; 최종 품질 미확인 | 미확인; 0으로 대체 금지 | null |
| FX03 | t0 빠른 종료 뒤 원 필수조건 위반, t1에도 수정 안 함 | N 포함, 최종 fail·중대 여부 rubric대로 | 실제 변경 사건 0; 결함 잔존이므로 이득 아님 | null |
| FX04 | t0와 t1 모두 pass, 같은 대안·같은 요구 | N 포함, 최종 pass | 수정 불필요·원요구 되돌림 0; 확인 노동은 별도 | null |
| FX05 | t0/t1 원요구 pass, 후속에만 추가된 기능 구현 | N 포함, 원요구 최종 pass | new_requirement_excluded; 예방가능 원요구 재작업에서 제외 | null |
| FX06 | t0 오판 뒤 같은 원요구를 다시 읽고 결정 변경 | N 포함, t0 fail·t1 pass | old_decision_id와 원요구가 연결되면 원요구 재작업 | null |
| FX07 | C 카드의 근거 연결이 틀렸고 참가자가 그대로 채택 | N 포함, 최종 품질은 공통 rubric; card_error 별도 | 원요구 되돌림이 있으면 후보; 제공자 정정 노동 별도 | null |
| FX08 | 두 허용 대안 모두 t0/t1 통과하며 바뀌지 않음 | N 포함, 두 대안 모두 pass | 수정노동 차이 판별 정보 없음; 검증된 0사건 | null |
| FX09 | 활동 로그 일부 손실, 최종 산출물은 pass | 품질은 관측 pass, 시간 기록 완결은 실패 | 되돌림 증거가 있으면 사건은 판정 가능하나 노동 미확인 | null |
| FX10 | 원요구 위반과 새 기능을 한 commit에서 함께 고침 | 요구별 품질은 분리; 제출 하나를 사람 2명으로 세지 않음 | 원요구 repair와 새 기능의 구간이 분리 안 되면 비용 분해 미확인 | null |

## 세 대비가 지지하거나 기각할 수 있는 것

| 대비·가설 | 지지할 관측 패턴 | 반대/판별 불충분 패턴 | 분리 못 하는 요소 |
| --- | --- | --- | --- |
| A↔B 선별 링크 제공 묶음 | 사전 품질 기준 유지 + 전원 노동 이득 + 결측 민감도에서 결론 유지 | 빨리 멈춘 실패/품질열화, 준비비 포함 시 반전, 넓은 불확실성 | 선별 정확성·추천 신호·순서·접근 편의 |
| B↔C 설명 추가 | URL/판/순서 동일 상태에서 품질·전원 노동 공동기준 충족 | 설명 오연결 고착, 읽기 부담으로 총노동 증가, 전문가 층에서 반대 | 설명 내용과 추가 길이/읽기 부담 |
| A↔C 전체 제공 | 전체 패키지 공동기준 충족 | 검색단계 이득만 있고 총노동/품질 이득 없음 | 링크·설명 각각의 순효과 |
| 채택 뒤 원요구 수정 | 원요구 위반·old decision·실제 repair 노동·후속 품질이 연결됨 | 모두 무수정, 미채택 분모 불균형, t1 결측, 새 요구만 변경 | 채택자 조건부 선택; 단기 과제와 장기 제품 설계 |

유의차 없음은 품질 동등성이나 효과 0의 증거로 쓰지 않는다. 품질 경계·최소 노동 차이가 사전 확정되지 않으면 성공/실패 사업 판정을 보류한다. 예시 파일의 논리 통과는 사람 시험 효과의 지지/기각이 아니다.

## 가림과 노출 통제

참가자는 t0·배정 arm·t1만 받는다. 채점자는 arm·제품/정책 이름을 지운 행동/출력/근거 위치와 공통 요구를 받는다. 이름 삭제로 정당화 근거까지 없어지면 evidence map을 별도 보조자가 만들어 제공하고 의미 손실을 검사한다. 채점자의 조건 추정도 기록하여 실제 가림 유지 여부를 확인한다. 공개 repo 전체를 전달하면 정답이 노출될 수 있으므로 배포 manifest를 사용한다.

A도 같은 공개 원문을 검색할 수 있다. 현재 웹에는 과제 원시점 이후 자료가 있으므로 엄격 역사적 정보집합이 아니다. 미래 문서를 발견한 사람을 사후 제외하지 않고 exposure에 기록하며, 원시점 정보집합만 시험하려면 모든 군에 같은 고정 corpus·검색기를 제공하는 별도 설계를 만들어야 한다. B/C의 원문 pin만으로 A의 자연 검색을 당시로 되돌릴 수 없다.

외부 사람 두 채점자의 독립 판독과 제3자 조정은 후속 계획이다. 이번 저자·AI 판독을 사람 간 합의로 기록하지 않는다.
