# 통합 스크립트 매핑 수정 인계

수정 대상은 root가 단독 편집권을 넘긴 `docs/workstreams/research/AF-RES-034/tools/aggregate.py`다. 이 문서 외 다른 파일은 이번 수정에서 편집하지 않았다. 원장과 통합 산출물은 읽기 전용으로 확인했다. **aggregate.py를 import하거나 실행하지 않았다.** 통합 CSV/JSON 재생성은 root가 수행한다.

## 변경 맵

| 대상 | 변경 | 보존하거나 남긴 한계 |
| --- | --- | --- |
| B 효과 SWB-E13~E16 | `original_report`의 원보고 값을 대표 `original_values`에 병합 | REST의 정확한 평균시간을 추정해 채우지 않음. Strathcona의7/1/8/2는 원보고 건수 그대로. |
| SWB-E15/E16 | `coefficient`/`standard_error`를 `recalculation_inputs`, 기존 `recalculated_interval`을 `recalculated_result`로 복사 | 새 구간 계산은 하지 않음. 원장의 근사95%Wald·반올림 입력·비보정·원보고 CI 아님 문구 유지. |
| SWB-E04 | 원 분자/분모 `original_counts`를 원값과 재계산 입력에 추가 | 원 수준값1/12·3/12와 비율은 그대로. |
| B 군별 시행 | arm의 `trial_n` 또는 `n_trials`를 `arm_trials`에 매핑 | Acar52/52/56/56, Prompter12/12, NCQ 각실험10/10. 단일군 Strathcona는 원 연구 전체8시행을 그 군으로 연결. |
| eXoaDocs/REST 군별 시행 | 실제 시행 수를 추정해 채우지 않음 | 48/48·80/50은 배정 과제기회이며 실제 완료/시도수가 아님. 이 네 군행의 빈 `arm_trials`는 의도적이다. |
| NCQ 시간 | arm의 `median_total_seconds`와 `median_final_package_seconds`를 `time_result`로 이동 | 대표 `quality_result`에서는 시간 키만 제거하고 완료 건수는 유지. 원 arm 전체는 `detail_json`에 보존. |
| SWB-E08/E09 | 원 수준값 `unit=percent`, 차이 단위 `absolute_difference_unit=percentage_points`, 비율 `dimensionless`, 상대변화 `percent`로 분리 | 값70/46,68/40,차이24/28,상대비율 자체는 그대로. phase3 raw `detail_json`의 원 단위 표현도 보존하므로 정규화 이유는 BREV-03과 이 파일에 기록. |
| SWB-E08 분모 | `12 people observed in each condition;24 task executions;12 paired participants` | 24쌍이 아니라12사람의24시행임을 명확히 함. |
| 전 효과 study ID | 기존 효과의 `study_id`/`experiment_id` 우선, 다음 명시 검토맵, 그 외에는 **전체 core+adjacent canonical studies에서 해당 family의 실험 ID가 하나일 때만** 연결 | 새로운 효과용 추측 ID를 만들지 않음. family 내 복수 실험이 남으면 assertion으로 중단. 연결 ID의 family/source도 대조. |
| 전 효과 claim ID | `claim_id`→`claim_ids`→`claims` 순으로 기존 효과 필드 우선; 없을 때만 해당 source의 기존 claim IDs를 연결 | `claim_link_basis=source_level_join`이면 출처수준 연결이며 효과 단위 직접 지지로 승격하지 않음. 새 claim ID 없음. |
| 연결 근거 열 | `study_link_basis`, `claim_link_basis`를 effects.csv에 추가 | 기존/명시맵/family유일/출처수준 fallback을 구별. |
| source 전체 수 | counts 키 `all_directly_reviewed_source_records`를 `source_records_including_partial_and_discovery`로 변경하고 범위 note 추가 | `len(sources)` 수식 유지. 현재 입력48행에는 부분 열람·발견만 한 행도 있어48개 적격 전문이라는 오독을 막음. 최소수·분류·다른 count 수식은 변경하지 않음. |

## 기존 canonical ID의 명시 맵

| 효과 | 이미 존재하는 실험 ID |
| --- | --- |
| SWB-E01~E04 | SWB-EXO-1 |
| SWB-E05~E07, SWB-E15~E16 | SWB-ACAR-1 |
| SWB-E08~E09 | SWB-PROMPT-2 |
| SWB-E10 | SWB-NCQ-1 |
| SWB-E11~E12 | SWB-NCQ-2 |
| SWB-E13 | SWB-REST-1 |
| SWB-E14 | SWB-STRATH-1 |
| Er-01 | UNAKITE2 |
| Er-02 | UNAKITE1 |
| Er-03 | CODEMEND-LAB |
| Er-04 | STRATA-LAB |

SWA 단일 실험 ID는 기존 통합 `studies.csv`에 있던 family별 canonical ID에 연결한다. 기존 studies 정규화의 family+`-E1` 규칙을 바꾸지 않았으며, 효과를 위해 별개 ID를 새로 구성하지 않는다. cross numeric17행은 이미 있는 `study_id`를 그대로 사용한다.

## 실제 정적 검증 영수증

확인 UTC: **2026-11-22T16:26:31.120644+00:00**, 종료코드 **0**.

| 확인 | 실제 결과 |
| --- | --- |
| Python 구문 | `ast.parse(source)` 및 `compile(source, path, 'exec')` 통과. 코드 객체를 실행하지 않음. |
| 명시 맵 | AST에서 두 상수 dict를 `ast.literal_eval`로 읽어 기존 원장과 대조. |
| canonical ID | 원장으로 읽은27개 canonical 실험 ID 집합이 기존 통합 studies.csv의27개와 일치. core26에 adjacent1 포함. |
| 전 효과 조인 | 53/53: 효과 명시 ID17, 검토 명시맵20(B16+root4), family유일16(SWA10+cross 비시간6). 모두 기존 canonical ID·family·source 조인 일치. |
| 기존 claim 연결 | 53/53: effect.claim_id14, source_level_join39. 각 ID가 해당 source의 기존 claim 집합에 있음. |
| 실행 범위 | aggregate import/실행 없음, 통합 CSV/JSON 쓰기 없음, 다운로드 코드 실행 없음. |
| 수정 스크립트 SHA256 | `acfaf0bd5aa5bae8098a3523253e56ab963c2a7d03288eb1b3ef5741f5067d77` |

구문 검사는 다음 형태로 재현 가능하다. 이는 집계 실행 명령이 아니다.

```sh
python -B - <<'PY'
import ast
from pathlib import Path
p = Path('docs/workstreams/research/AF-RES-034/tools/aggregate.py')
s = p.read_text()
ast.parse(s, filename=str(p))
compile(s, str(p), 'exec')
print('syntax ok; aggregate not executed')
PY
```

## root 실행 전 확인과 다음 명령

1. 다른 원장 작성이 끝난 판에서 실행한다. 추가 효과나 family가 들어오면 고유 실험 조인의 전제가 달라지므로 ambiguous assertion을 임의 우회하지 않는다.
2. counts의 이름이 바뀌므로 `all_directly_reviewed_source_records`를 직접 읽는 검증/설명 소비자가 있으면 새 키로 연결한다. 숫자48은 원장 전체 수이며 전문 적격 최소수30과 다르다.
3. 다음 명령은 통합 sources/studies/effects/attempts/screening과 counts를 재생성한다. 이번 인계에서는 아직 실행하지 않았다.

```sh
python -B docs/workstreams/research/AF-RES-034/tools/aggregate.py
```

실행 뒤 root의 통합 검증에서53개 효과의 canonical study/claim 조인, `claim_link_basis`의39개 source 수준 표시, E15/E16 구간·입력, NCQ 대표 시간4행을 확인하면 된다. 검토 내용의 텍스트 수정(BREV-05/06/07: Acar 참여 표현, 원산출물 종류, 미시행 검열 규칙)은 이 스크립트 변경과 별개다.
