# 병렬 작업공간의 판정 보존과 불일치 감사

이 부록은 **같은 원 실행에 대한 상관된 내부 판정의 민감도 기록**이다. 새 기준선 실행, 사람 검토, 다른 모델의 검증 또는 합의 판정이 아니다. 기존 주보고서와 인수 조건은 변경하지 않는다. 원격 주결과 `eb569f07a3a34ffacf114384ae9b06ad062f5396`을 유지하고, 이 작업공간의 미게시 결과를 별도 보존한다.

현재 전체 인수 상태는 주결과의 **BLOCKED**를 유지한다. 사용자 요청의 사이트당 최대 3개를 사례 최소수에도 문자적으로 적용하면 GitHub 계열 고정판 31개 가운데 산입 가능한 것은 **3개/요구 30개**다. 최초 SAMPLING의 비사례 한정 해석이나 이 부록은 사용자 승인된 예외가 아니다. 이 부록의 추가로 차단이 해소되었다고 주장하지 않는다.

## 1. 무엇을 보존했는가

- 실행 위치: `/workspace/scratch/71d498d6556a/agentflow-open`.
- 모델 표기: **GPT-6 Astra Pro**. 검토자 구분은 **내부 별도 검토**다.
- 병렬 작업의 기준 커밋: `caa2a814727dd485ed0eb9bb8530d6b16fab9584`.
- 발견한 원격 주결과: `eb569f07a3a34ffacf114384ae9b06ad062f5396`.
- ref에 연결되지 않은 준비 판정 커밋: `0cc0fc15c650f8d3ec551202ffe4dbdcef335898`.
- [SNAPSHOT.json](SNAPSHOT.json)은 기준 커밋과 달랐던 **230개 파일, 4,752,466바이트**의 경로·크기·SHA-256을 기록한다. `snapshot/`의 복사본은 원 작업공간의 해당 파일과 바이트 단위로 같으며, 대표 검토 때 230개 hash를 다시 확인했다.

이는 전체 저장소 복사본이 아니라 **기준 커밋에 대한 owned_path 내부의 차이**다. 변경되지 않은 접두부와 A/B 원 응답은 기준 커밋에서 읽는다. 그 기준 커밋은 원격 주결과의 선조다. 원 실행을 다시 수행하거나 다른 응답으로 교체하지 않았다.

`snapshot/JUDGMENTS.json`은 342개 후보의 필수 판정값을 담고, 각 `details`는 62개 실행별 상세 파일로 연결한다. 약 1 MB의 단일 상세 판정 파일을 대신해 공통 값과 상세 이유를 나눈 보존 형식이며, 제약별 이유·전이 대응·추가 확인은 상세 파일에 남아 있다. 이 구조를 생략된 판정이나 새 검색 색인으로 읽으면 안 된다.

### 상대경로를 읽는 방법

**snapshot 내부의 모든 상대경로는 `snapshot/`과 기준 커밋의 owned_path를 겹친 논리적 연구 루트를 기준으로 한다.** 먼저 `snapshot/<경로>`를 읽고, 그 파일이 없으면 다음과 같이 기준 커밋의 원본을 읽는다.

```bash
git show caa2a814727dd485ed0eb9bb8530d6b16fab9584:docs/workstreams/research/AF-RES-013/runs/B/C27.json
```

예를 들어 snapshot 판정의 `evidence/judgments/expanded/B-C27.json#/judgments/0`은 snapshot 아래의 상세 파일을 가리킨다. 같은 판정의 `runs/B/C27.json`은 변경되지 않은 기준 커밋 파일을 가리킨다. 현재 주결과 파일을 누락된 snapshot 입력에 임의로 대신 넣으면 두 판정 계열이 섞인다. snapshot 내부 문서의 링크가 웹 디렉터리에서 곧바로 열리지 않는 경우도 이 논리적 경로 기준으로 해석해야 한다.

## 2. 원격 상태 확인의 시점 정정

snapshot의 PROGRESS 등에 남은 “원격이 caa…”라는 서술은 **최종 fresh 원격 ref 확인 전 이 작업공간이 유지하던 관측**이다. 원격에는 이미 eb569f0… 주결과가 게시되어 있었고, 그 커밋의 시각은 **2026-11-20 15:47:26 UTC**다. Git의 원 표기는 `2026-11-21T00:47:26+09:00`다. 준비 판정의 게시 과정에서 API의 `expected_sha` 부모 조건이 맞지 않아 ref 갱신이 실패한 뒤 최신 원격을 확인했다.

이후 진행 담당은 원격 주결과를 이 작업공간의 결과로 덮어쓰지 않았다. 준비 커밋과 로컬 기록을 보존하고, 주결과의 상태를 기준으로 이 부록을 분리했다. 과거 관측을 현재 원격 상태로 읽거나, 준비 커밋이 브랜치의 최종 판정이었다고 읽으면 안 된다.

## 3. 같은 실행, 다른 판정 수치

관측 창은 두 계열 모두 **31사례, A 31회·204후보, B 31회·138후보**다. 본문 gold는 176항목이다. 아래 동일·결정 전 수치는 각각 서로 다른 `(사례, gold 항목)` 쌍의 수다. A+B는 사후 합집합이며 통합 검색 실행 결과가 아니다.

| 지표 | 유지되는 원격 주결과 eb569f0… | 병렬 snapshot |
| --- | --- | --- |
| A 동일 / 결정 전 적중 | 23/176 · 16/176 | 22/176 · 16/176 |
| B 동일 / 결정 전 적중 | 14/176 · 5/176 | 8/176 · 2/176 |
| A+B 동일 / 결정 전 합집합 | 29/176 · 17/176 | 24/176 · 16/176 |
| 근접 오답 A / B | 0/204 · 0/138 | 9/204 · 3/138 |
| 정답 밖 유용 후보 A | 170/178행 | 146/178행 |
| 정답 밖 유용 후보 B | 109/120행 | 105/126행 |
| 외부 실체 / 내부 구조 gold 분모 | 30 / 146 | 34 / 142 |
| 최소수 산입 비사례 / 사이트 그룹 | 25 / 13 | 26 / 14 |

주결과의 외부 실체 **34→30**, 내부 구조 **142→146** 정정은 후보 판정 불일치와 별개다. 병렬 snapshot은 정정 전 분모를 보존한 것이며, 이 부록은 주결과의 그 정정을 되돌리지 않는다. 두 계열의 근거는 [현재 주결과 집계](../AGGREGATES.json)와 [snapshot 집계](snapshot/evidence/AGGREGATES.json)에 있다.

비사례 산입 집합에서 snapshot에만 있는 것은 **M25·M27**, 주결과에만 있는 것은 **PS-R-S21-LENS**다. M25는 수락 공고, M27은 추가 Rust 토론이며, 주결과는 실제 Swift lens 토론을 포함한 5개 리뷰를 센다. 이 선택 차이를 새 자료 수에 합산하거나 두 연구의 독립된 근거 수로 더하지 않는다. 주결과의 25개/13사이트와 사이트 상한의 인수 차단을 유지한다. [주결과 산입 원장](../SOURCE_COUNT.json), [snapshot 산입 원장](snapshot/evidence/SOURCE_COUNT.json).

### 기계적 비교

[COMPARISON.json](COMPARISON.json)은 342개 후보를 `(baseline, case_id, rank)`로 짝지었다. **129행**에서 적어도 하나의 비교 필드가 다르다. 필드별 행 수는 서로 겹치므로 더해서 전체 변경 행 수로 삼지 않는다.

| 비교 필드 | 다른 행 수 / 342 |
| --- | ---: |
| H | 96 |
| label | 58 |
| nongold_useful | 64 |
| T | 26 |
| near_miss | 12 |
| nongold_historical_useful | 20 |
| gold_ids | 23 |
| historical_ids | 11 |
| date_status | 7 |
| E | 3 |

snapshot에서 근접 오답으로 센 12행은 주결과에서 INSUFFICIENT 4행, CONDITIONAL_TRANSFER 8행으로 바뀐다. 주결과의 `exclusion`은 `null` 또는 `{excluded:false,...}`이고 snapshot은 boolean을 사용한다. 객체 전체의 truthiness를 제외 여부로 쓰면 집계가 틀린다. 이러한 schema 차이를 맞춘 뒤 수치를 비교했다.

## 4. 대표 5행의 내부 별도 검토

고정 [AF-RES-004 PROTOCOL](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md)과 동일한 SCOPE를 적용했다. 아래의 “더 지지됨”은 **이 검토자의 근거 판단**이다. 공동 합의나 주결과의 정정이 아니며 모든 행을 `unresolved_no_consensus`로 보존한다. 판단과 양쪽 값, 근거 위치는 [REPRESENTATIVE_REVIEW.json](REPRESENTATIVE_REVIEW.json)에 있다.

| 후보 행 | 핵심 차이 | 이 검토의 판단과 남은 경계 |
| --- | --- | --- |
| B-C27-r1 Elixir capture | snapshot H2 fail·근접 오답, 주결과 H2/T unknown·불충분 | **주결과의 보류가 더 지지된다.** 원 응답은 arity를 labels로 옮기는 것을 추론이라고 처음부터 한정하고 resolution을 남겼다. 전체 해법의 알려진 실패보다 미완성 전이 조건의 unknown에 가깝다. |
| A-C31-r1 StrictVersion/LooseVersion | snapshot 순서 fail, 주결과 모든 H pass | **양쪽을 그대로 확정하기 어렵다.** 원 응답은 오류를 회귀 예제로 쓰므로 snapshot의 실패 판정은 과도할 수 있다. 주결과 H2 pass에는 OS 패키징 환경과의 관계에 대한 구체 근거가 부족하다. 두 gold 실체 적중에는 이견이 없다. |
| B-C09-r3 Cython lowering | snapshot range 미적중, 주결과 range 적중 | **고정 주점수에는 snapshot 미적중이 더 지지된다.** 선택된 사용 방식은 compiler의 lowering 조건이다. 검증 문서에 등장한 range 호출을 제시된 재사용 부품으로 소급하는 것은 더 넓은 회수 단위다. |
| B-C24-r2 Immutables | snapshot 공개 경계의 거절 구조 적중, 주결과 미적중 | **structural_match 경로에서는 snapshot 적중이 더 지지된다.** 원 응답 자체가 비공개 속성의 공개 생성 입력 노출을 경고한다. builder와 initializer의 차이가 핵심 조건인지에 대한 이견과 날짜 unknown을 유지한다. |
| B-C22-r1 Qt 명명 | Threadsafe는 공통 적중, ConcurrentlySharable 추가 적중 여부가 다름 | **고정 명칭 규칙에는 snapshot이 더 지지된다.** 원 응답의 ConcurrentShareable과 gold ConcurrentlySharable은 공식 alias로 확인되지 않았다. 의미 수준의 유사성은 별도 경계이며 주점수 정규화를 소급 확장하지 않는다. |

대표 5개 실행 파일은 기준 커밋과 주결과 사이에 바이트 단위로 동일했다. 이 5행에서 비교한 gold 항목도 양쪽에서 동일하다. 따라서 이 차이를 새 검색 결과나 gold 원문의 변경 효과로 해석할 수 없다.

## 5. 검증 상태와 미실시

snapshot의 `SELF_CHECK.md`와 `evidence/FINAL_VALIDATION.json`은 **예비 자료**다. 검증 JSON은 `mode=data`, 기준 HEAD caa…, **19개 자료 gate 통과**를 기록한다. 이것은 최종 인수 검증이 아니며, snapshot SELF_CHECK의 완료처럼 보이는 문구를 원격의 BLOCKED 인수를 대체하는 승인으로 사용할 수 없다.

이 부록에서 확인한 것은 230개 보존 파일의 크기·hash, 342개 기계적 쌍 비교, 대표 5행의 원 응답·판정·고정 규칙이다. **H 불일치 96행과 gold 불일치 23행 전체의 실질 재심은 하지 않았다.** 대표행은 차이를 본 뒤 의도적으로 골랐으므로 모집단 오류율이나 판정 신뢰도 추정에 쓰지 않는다. 새 외부 자료 열람, 후보 통합 실행, 설계자 효과 관측도 하지 않았다.

다음 판정 작업은 처음부터 제안한 참고 범위, 출처에 등장한 객체와 후보가 선택한 대상, 명명 정규화의 경계를 동일한 규칙으로 분리해 불일치 행을 재심하는 것이다. 그 전까지 두 판정 계열과 원 응답을 함께 보존한다. **주보고서의 수치와 전체 인수 조건은 그대로 유지한다.**
