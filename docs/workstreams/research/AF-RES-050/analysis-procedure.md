# 읽기 전용 분석·연결 절차

## 실행 범위와 원장

이 작업은 공개 파일의 구조·기수·출판 집계 계보를 계산했다. 참가자 프로그램, 원저자의 서비스/모델, 자동 채점기나 사람 실험을 실행하지 않았다. 원 참가자 가명·코드 행을 재게시하지 않고, 자체 예시ID와 원 URL·논리행/물리줄을 안내한다. 분석 결과의 사실 단위는 `sources.jsonl → studies.csv → joins.csv/outcomes.csv → RESULT.md`이다. CSV의 `details_json`과 `evidence_pointer`는 요약 열에서 생략된 기수·제외 분모·파일판을 보존한다.

실제로 실행한 재현 명령과 출력:

| 명령 | 입력 | 실제 결과·증거 |
| --- | --- | --- |
| `python -B docs/workstreams/research/AF-RES-050/streams/ncq-exoa/audit_ncq.py` | ce14f193…의 codesnippets1/2.csv | exit0;142/156행과 각20 P×T 그룹; ncq-row-audit.json |
| `"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/audit_public_release.py` | 445d5d8…의 CSV·XLS·SQLite·소스 | exit0;361 IR행/360고유 full-row; execution.json,artifact-inspection.json |
| `python -B docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py strata` | arXiv2102.06231v2 source tar | exit0;집계6/6계보,외부 workbook 누락; reproduced-strata.json |
| `python -B docs/workstreams/research/AF-RES-050/streams/unakite-strata/inspect_public_artifacts.py unakite` | 공식 main.bb8e5ba3.js.map | exit0;공개 정적 스키마; reproduced-unakite.json |
| `python -B docs/workstreams/research/AF-RES-050/build_ledgers.py` | 커밋된 분담 JSON/JSONL | exit0;8연구군·16join·26outcome 및 source 수량 생성 |

첫 두 파일의 blob/바이트 hash와 파싱 방법은 각 감사 파일에 있다. NCQ CSV의 인코딩은 파일에 맞추어 명시했고, multiline quoted snippet 때문에 논리행과 물리줄을 분리했다. 공개 코드의 작업 수·추천점수·SQL example 테이블을 참가자 시간/품질 파일로 이름만 바꾸지 않는다.

## 원자료가 추가될 때의 입력 계약

필요한 표는 다음과 같다. 파일 이름은 저자가 공개한 실제 이름을 유지하고 아래 구조를 코드북으로 대응시킨다.

| 표 | 최소 열 | 기수와 위험 |
| --- | --- | --- |
| 배정 | study/cohort, 익명 person, task, period/order, assigned condition, strata/site, scheduled/started/withdrawn | 사람1:N시행; 단계별 탈락과 예약·배정을 분리 |
| 시각 사건 | 동일 시행키, event type, timestamp, timezone/unit, start/selection/submit/timeout/wait | 시행1:Nevent; 중복 사건 제거 규칙을 먼저 확인 |
| 제출·검사 | 시행키, submission/artifact ID, rubric/test version, criterion, score/pass, missing/timeout | 시행1:Ncriterion/grader; 원 평가자와 합의 점수를 구별 |
| 노출·채택 | 후보/문서 URL·판, feature flags, displayed/opened/saved/pasted/applied, 연결 이유 | 후보 노출과 실제 사용이 다름; 검색 결과에 없던 후보를 같은 처치로 합치지 않음 |
| 활동·추적 | active/idle/wait intervals, 교육·작성·검사 구간, 초기 산출물과 후속 revision, 관찰 종료일 | 활동시간은 측정 규칙이 있을 때만; 단순 사건 간격은 대체물 |

고정표본에서는 이 전체 계약을 만족하는 공개 person–task 행의 비교 사례를 **관측0/8군** 찾았다. 이는 효과가0이라는 뜻이 아니다. 미획득 표의 행수와 unmatched 수는 `미확인`으로 남겼다.

## join 순서

1. 실험/cohort를 가장 바깥 키로 유지한다. NCQ 두 파일에 같은 P값이 있어도 같은 사람으로 연결하지 않는다. T1/T2는 조건명으로 번역하지 않는다.
2. 배정의 기대 자연키가 유일한지 검사한다. event·snippet·채점차원은 정상적인1:N이다. 이를 먼저 목적 단위로 요약하지 않고 서로 붙이면 N:M로 행과 표본수가 부풀 수 있다.
3. 시간표와 채점표를 **배정표에 left join**한다. 원 배정 수, 시작 수, 제출 수, 검사 수, 포함 수와 제외 이유를 각각 보존한다. 기준선/처치의 성공자만 inner join한 표를 전체 효과로 쓰지 않는다.
4. 실제 입력 행수, 고유/결측 키, 중복군, join 후 행수, 양쪽 unmatched를 기록한다. 현재 NCQ는 snippet 열만 있고 CodeMend IR자료는 관측 단위부터 다르므로 join을 실행하지 않았다.
5. 각 연구의 시간 원점·종점·상한을 적용한다. Blueprint first paste와 완료, CodeMend subtask와 전체, eXoaDocs 문서 전환과 최종제출, Unakite interaction fraction과 total seconds는 별개다.

## 허용 식과 빠진 항

독립 배정군의 시간 차이는 `mean(T|E)−mean(T|C)`이다. 각 군의 n과 분산, repeated task의 사람 군집이 필요하다. eXoaDocs의 전체40분 내 전과제 통과 집계에서는 `3/12`와 `1/12`, 기술적 차이 `(3−1)/12`를 읽을 수 있지만 층별 배정·개인 시간 연결을 복원하지 못한다. 이전034의 표를 재산출하는 일을 새 성과로 세지 않는다.

교차설계에서는 실제 `person×task×period×condition` 배정대로 차이와 불확실성을 구한다. 동일인이 다른 문제를 풀었으면 과제/순서를 보존한다. marginal SD만으로 paired covariance를 만들지 않는다. NCQ의 baseline-first에서는 condition과 순서가 완전히 얽혀 있으므로 원자료가 생겨도 학습·순서 효과가 저절로 분리되지 않는다. `median(E)−median(C)`는 `median(E−C)`가 아니다(RT-M02).

제한시간 내 올바른 완료는 `sum(I[original correctness threshold met and time≤cap])/N_assigned`이다. cap·정답 기준·미완료 지시자가 없는 연구에 새 성공 기준을 만들지 않는다. Strata의 “끝냈다”와 모든 이유가 정확함은 다르다. CodeMend의 조건당60은 예정 subtask기회이며14/19개 잔여가 실제 실패인지 미도달인지는 모른다.

동등 품질은 사전 정한 허용 차이와 해당 CI가 필요하다. p가 크거나 평균 점수가 비슷하다는 이유로 동등성을 선언하지 않는다(RT-M03). 현재 자료로 새 동등품질 시간쌍은 산출하지 않았다. 수치 없는 칸을0·상한·성공자 평균으로 채우지 않는다.

## 감도와 후속 원장

최소 감도 축은 전원/성공자, 부분/전체 시간, 초보/숙련, 교육 포함/제외, 같은 링크/다른 후보, 정답/미제출/timeout/미도달이다. 각 축의 현재 판정은 `counterexamples.md`와 Q6에 있다. 없어진 비교 행은 조용히 삭제하지 않고 필요한 최소 파일을 남긴다.

재작업을 계산하려면 초기 채택·검사와 후속 수정의 동일 산출물ID, 관찰 기간 및 활동시간이 필요하다. 여기서는 모든 고정군에서 미확인이다. 교육시간을 임의로 더하거나 PR시각 차이를 노동으로 쓰지 않는다. 후속 파일을 받으면 첫 행동은 NCQ codebook과 시각/최종검사 파일의 자연키·판을 검사하는 것이다.

