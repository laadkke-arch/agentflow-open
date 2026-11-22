# AF-RES-034 · 원장 단위와 재현 방법

이 묶음의 통합 파일은 `streams/`의 판독 원장을 정규화한 것이다. 원문에서 보고한 값, 이 작업의 산술 재계산, 제품 적용 추론, 미시행 시험의 가정을 서로 바꾸지 않는다. 원문 PDF·다운로드한 전체 코드·notebook은 커밋하지 않았다. 출처 URL·판·직접 읽은 위치·해시·발견/열람/확인의 구별을 원장에 남겼다.

## 단위와 식별자

| 파일·필드 | 단위·규칙 | 오독하면 안 되는 것 |
| --- | --- | --- |
| `sources.jsonl` / `source_id` | 고유 외부 문서 또는 독립 내용의 원산출물 1행. 부분 열람·발견만 된 후보도 상태와 함께 보존 | 원장48행이 전문48편을 뜻하지 않음 |
| `count_minimum` | 봉인한 핵심 분류와 직접 확인 조건을 충족한 행만 true | false가 무효효과 또는 연구 가치 없음이라는 뜻은 아님 |
| `count_category` | software_primary/design_primary/learning_primary/artifact가 최소수에 해당. 인접·동반·발견·접근미완료는 별도 | artifact8은 실험8개도, 사람 시간 raw8개도 아님 |
| `study_family` / `duplicate_group` | 같은 모집·표본·과제/논문군의 중복을 묶는 ID | 같은 가족의 두 실험을 한 코호트로 합치지 않음 |
| `studies.csv` / `study_id` | 독립 실험 또는 코호트 | 핵심26실험과 인접1실험, 총27 ID. 핵심 연구군은22 |
| `study_row_id` | 실험 안의 배정군/조건 행 | 74행을74사람·74실험으로 세지 않음 |
| `people_*`, `arm_people_reported`, `arm_n_*` | 보고·등록·배정·분석·완료를 구별. 교차의 같은 사람은 두 조건에 반복될 수 있음 | 모든 군행의 사람 수를 단순 합산하지 않음 |
| `trials_reported`, `arm_trials` | 보고된 과제 시행·기회. 원 정의는 detail_json을 확인 | eXoaDocs/REST의 배정 과제기회와 실제 시도수는 다름. 누락된 군 시행수를 역산해 실제 관측처럼 채우지 않음 |
| `comparison_grade` | R=무작위 또는 균형 교차, Q=비무작위, U=배정 불명, O=대조 부재 | R도 학습·탈락·품질의 모든 편향을 제거하지 않음 |
| `product_directness` | L=링크/목적·근거만 바뀜, B=소프트웨어 도구/자료 묶음, X=다른 분야 | 이번 핵심 가족의 L은0. B/X의 효과를 링크만의 효과로 환산하지 않음 |
| `effects.csv` / `comparison_id` | 동일 실험의 특정 비교·결과 또는 계산 불가 관측 | 53효과 행은53독립 실험이 아님. 같은 참가자의 여러 대비를 합치지 않음 |
| `original_values` / `recalculation_inputs` | 원보고 값과 계산에 실제 사용한 입력. 단위·표/쪽·분모를 보존 | reported d/p 또는 원문 그래프를 임의로 원평균으로 복원하지 않음 |
| `recalculated_result` / `formula` | 개입−대조, 비율, 가능한 집계자료 구간. 계산 불가는 이유를 가진 객체 | Welch CI는 반올림 입력의 양측 명목95% 탐색구간. 동일 품질 입증·원자료 재분석이 아님 |
| `denominator` / `noncompletion` | 원 입력의 표본 수와 실험 수준 분모·완료자 선택·누락 상태 | 보고되지 않은 시간 평균 n을 전체 배정 n이나 테스트 통과 n으로 바꾸지 않음 |
| `study_link_basis` | 원 효과의 ID / 검토한 명시맵 / 가족 안 유일한 canonical 실험 | NCQ/Unakite의 두 실험은 명시맵으로 분리 |
| `claim_link_basis` | 효과 자체 주장 연결 또는 source_level_join | 출처 수준 연결이 모든 주장에 대한 그 효과행의 직접 입증을 뜻하지 않음 |
| `claims.jsonl` | 기존 주장 ID→원문·위치·효과의 탐색용 인덱스 | 새 효과나 새 독립 증거가 아님. limitations를 함께 읽음 |
| `screening.csv` | 질의 반환 후보와 전문 심사/접근 상태. 같은 URL이 여러 질의에서 반복됨 | 검색1066행·고유URL901을 논문수로 부르지 않음 |
| `attempts.jsonl` | 검색·열람·실패·대체 접근·중요 실행의 기록 | 후기 복원 로그의 logged_utc는 원 실행 UTC가 아님 |
| `strand_record`, `detail_json`, `strand_details` | 원 분담 파일·행과 원값 전체를 보존 | 통합 열에 편의상 요약한 문장을 원문 인용으로 보지 않음 |

CSV의 목록·객체는 JSON 문자열이다. 빈칸/null은 원문 미보고·미확인 또는 해당 없음이며 0이 아니다. 계산에 필요한 대표 열은 명시적 누락 이유로 채웠다. 배정군 수 등 원문 자체에 없는 값은 빈칸을 유지한다. `normalization_notes`는 통합에서 한 의미 보존 수정을 기록한다. Chan의 본문153/표151, McLaren 열람판 군 n, Strata recall 모순은 수정한 정답이 아니라 미해결 원문 충돌이다.

## 카운트와 인과 범위

최소수30=소프트웨어15+디자인3+학습4+독립 원산출물8이다. 핵심22가족은 가장 강한 가족 내 설계를 기준으로 직접16/간접4/대조 부재2이며, 독립 실험26개는 R19/Q3/U2/O2다. 이 설계 분류와 제품의 링크 단독 인과 비교0을 따로 보고한다. 설계·품질·시간 경계가 다른 효과를 메타분석으로 합치지 않았다.

산출물8개 중 실험 전용 지시·자료만 요구하며 NCQ 일반 명령 지시문을 제외하면7개다. 이 민감도는 최소수 충족 판단의 한계이며 숨기지 않는다. 원산출물8개 중 사람별 시작·종료·중단 시간 자료는0개다. 각 논문의 집계 시간은 존재하므로 ‘시간 증거가 전혀 없다’는 뜻은 아니다.

## 재현 명령

저장소 루트에서 다음 순서로 실행한다. Python 표준 라이브러리와 SciPy가 필요하다. 첫 두 명령은 통합 파일을 같은 원장으로 재생성하고, 세 번째는 자체 산술·조인을 확인해 영수증을 쓴다. 외부 저자 프로그램이나 사람 시험은 실행하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-034/tools/aggregate.py
python -B docs/workstreams/research/AF-RES-034/tools/build_result.py
python -B docs/workstreams/research/AF-RES-034/tools/verify.py --phase result --output evidence/validation.json
python -B -m workbench.session check docs/workstreams/research/AF-RES-034/manifest.json --fetch
```

`result-analysis.md.inc`는 RESULT의 세 필수 표 뒤에 붙는 작성 원본이다. `build_result.py`는 첫 세 표를 만들고 이 분석을 연결한다. `verify.py`는 source/study/effect/claim/attempt ID, 중복·카운트, 집계 수치·Welch 구간, 필수 표 순서·마지막3행, 소유 경로를 검사한다. 통과는 내부 일관성의 확인이며 원문 모순 해소나 색인 검색 포괄성 증명이 아니다.

고정 결과의 원격 재독과 session check 영수증은 최종 HANDOFF 묶음에 있다. 파일을 재생성하면 시간·해시 영수증이 달라질 수 있으므로 원격 고정 SHA의 판과 재실행판을 구별한다.
