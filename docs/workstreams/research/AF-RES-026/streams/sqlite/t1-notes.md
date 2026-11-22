# SQLite T1 대조·반증·인계 메모

## 봉인과 열람 순서

전체 24건 봉인 SHA는 `68fc97fadceb46f9945a71fcc53730e29f6c62bf`다. root가 exact-SHA 재독 검증을 알린 뒤 최초 후속 본문을 `2026-11-22T05:08:30.223622Z`에 열었다. 영수증은 `t1-receipt.json`이다. T0 `initial.jsonl`, `frozen-responses.jsonl`, `frame.csv`, `sources.json`의 해시는 봉인 전 `t0-receipt.json`과 같다. 초기 파일을 수정하지 않았다. `field-locations.jsonl`은 그때 쓴 값의 명시/해석/미상과 원문 위치만 분리한 감사 자료다.

원 thread 8개를 모두 시간순·편집 포함 보기로 열었다. 첫 묶음의 출력 일부가 잘려 S02–S08은 작은 묶음으로 재열람했고, 중요한 작성자 메시지는 raw artifact를 행 번호와 함께 다시 읽었다. 원글·편집·답 53개 모두 raw SHA3-256이 artifact ID와 일치했다. 원글 이후/원글 편집 45개 버전을 `followups.csv`에 두되, 서로 다른 댓글이나 편집을 독립 원문 수에 더하지 않는다. 한 삭제 개정(S02)은 W=0이며 이전 원문과 재게시 답은 회수할 수 있었다. 일시적 503 두 건은 같은 공개 raw 주소 재시도로 회수했고 이력은 메타데이터에 남겼다.

S01은 T0 검색 결과에서 답 한 문장을 보았던 노출 사례다. 원판 확인은 성공했으나 엄격 미노출 비교에서는 제외한다. 따라서 원판 확정은 8/8, 엄격 미노출은 7/8이다. 이 파일 작성자는 T0와 같은 `/root/sqlite`이며 독립 판독자가 아니다.

## 사례별 핵심 대조

| ID | 봉인 Q의 값 | 후속에서 확인한 내용 | 판정·행동의 구분 |
| --- | --- | --- | --- |
| S01 | 새 파일 생성 의도는 T0에 이미 있음 | [post14](https://sqlite.org/forum/artifact/76963f0026b6b12a2ccec60eff052ad870a1fe4e597334cf19d287ffcc2f18cb) L3·16–18·35–59: CREATE 유무를 비교하고 자신의 테스트 앱도 해결됐다고 보고 | A 선택 유지와 실제 성공 보고는 함께 관측. Q를 실제 발송해 얻은 결과가 아님. 노출 때문에 엄격 비교 제외 |
| S02 | `-o mysql`은 T0 로그에 있음 | [post2](https://sqlite.org/forum/artifact/43935bc7fb97f1bc76f7df8ae6a7fbc2a08c8f6f648cd6c13b3d50e835217c05) L1–3은 명령을 다시 물었고 [post4](https://sqlite.org/forum/artifact/051f0e1b6e6509c48ad90353610c671e4caeba4352fbcdd43fbdbc2586c9aeb2) L1–5는 곧바로 올바른 실행파일을 안내 | 작성자 후속 없음. 실행 오류를 고칠 조언과 전체 데이터 조회의 완료는 다름 |
| S03 | legacy OFF 유지가 필수인지는 끝까지 미상 | [post2](https://sqlite.org/forum/artifact/ae4fbb89dfc9269e3034795980430af62324b153fa4848ec1b58c1e13549bea8) L1–9는 view 순서 변경과 legacy 대안을 함께 설명 | Q를 모르더라도 안전한 1차 제안 A는 유지. 조건부 실제 답은 있으나 작성자 성공 보고 없음 |
| S04 | 성공 COMMIT 반환은 확정할 수 없음 | [post6](https://sqlite.org/forum/artifact/2070eae6fd0fa53a44a8ac87b946dd31facab9d181d29f4a304c74c5846246a4) L1–2의 committed 주장과 [post8.1](https://sqlite.org/forum/artifact/8a24d27a64786c26fcee69222d94ce3e0d88c58126bec7aedcd22bff513139d6) L7–23·28–35의 COMMIT 없는 코드/실패 로그가 충돌 | 주장까지 세는 민감도에서만 부분 값 1건. 정확한 Q 값 회수는 0. 실제 I는 보류했으므로 오승인으로 세지 않음 |
| S05 | 실제 serialized mode 값 없음 | [post2](https://sqlite.org/forum/artifact/ad1beab8b38eeef8c10c8d0c27ae7c75549dafd1e0c71c804b89bc87fe66da0c) L1–3은 제3자의 조건부 답뿐 | 실제 mode·실행·속도 보고 없음. mode 한 값이 알고리즘 전체의 안전성을 충분히 결정하지 않음 |
| S06 | amalgamation/split source 값 없음 | [post3](https://sqlite.org/forum/artifact/38da9f6c568f8cae81a1c49c5d94f1c44fd9da3dc5e87d76bdd9b6ce8608cd83) L1은 가능할 수도 있다는 반응과 문서 수정 희망 | 관심·가능성 표현이며 실행 성공 아님. 과거 링크의 다른 사용자가 성공한 사실을 이 작성자에게 이전하지 않음 |
| S07 | PG autovacuum daemon은 T0에 명시 | [post4](https://sqlite.org/forum/artifact/ac6dc2f57f77f12603e296d7b73ba4befeac52c4a145403efda17b57a807e0e8) L1은 문서가 더 자세하다는 읽기 보고. post5·9는 UPDATE/DELETE·in-place에 대한 추가 질문 | 읽기/원 질문 해결/구현을 분리. 추가 범위를 최초 필수 조건으로 소급하지 않음 |
| S08 | JS `req.body.duration`은 T0 코드에 있음 | [post3](https://sqlite.org/forum/artifact/b3d355a004483fafdd6745085c55063f79ce2183130144114731cb4c1c2ede6f) L1: 실제 조언을 따른 뒤에도 같은 오류, 두 열로 축소한 스키마 보고 | 실제 조언 실패는 관측되지만 그 조언은 봉인 I/C와 다름. I/C는 미전송 |

## 첫 결론을 반박한 자료

### 답을 받으면 빈칸이 채워진다는 가정 — S04

작성자는 실제 질문에 답했다. 그러나 첫 질문은 행마다 별도 트랜잭션인지에 관한 것이었고, 봉인 Q가 물은 **손실 행의 COMMIT 성공 반환**과 같지 않다. 작성자의 소실 주장에는 성공 반환값이 없다. 후속 재현 코드에는 BEGIN 이후 INSERT·reset·finalize·close만 있고 COMMIT가 없으며, 로그에는 commit 실패도 있다. 앞서 [post5](https://sqlite.org/forum/artifact/05f8cce9f61c2c27c6ae5ff9afb57b41fb8994ad7125e38e594f99c7569995e2) L1–10에서 설명한 FMDB 원앱과 이 직접 C API 코드가 동일한 완전 실행인지도 미확인이다.

그러므로 “작성자가 거짓말했다” 또는 “실제로 COMMIT하지 않았다”로 확정하지 않는다. `author_assertion_conflicted`로 두고, 완전한 코드 계보와 성공 반환 로그를 다음 최소 자료로 지정한다. 반대로 그 말을 성공 반환으로 대체하면 rollback 가능성을 부당하게 제외하고 장치/sync 문제를 확정하는 오류가 생길 수 있다. 이것은 `counterfactual-audit.csv`의 보조 반례이며 관측된 봉인 I/C의 오승인이 아니다.

### 한 mode만 알면 안전 여부가 정해진다는 가정 — S05

동일한 당시 [3.37.1 API 문서](https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/src/sqlite.h.in) L1761–1789는 multi-thread와 serialized의 mutex 계약을 구별한다. 그러나 L4904–4914는 유효한 ROW 뒤 reset/finalize가 없어야 column 결과를 읽을 수 있다고 제한하고, L5050–5054는 반환 pointer의 수명을 reset/step/finalize까지로 제한한다. L5117–5141은 reset의 상태 되돌림을 설명한다.

따라서 `step(ROW) → 다른 thread의 reset → 원 thread의 column 조회`라는 순서를 API 호출 단위로 직렬화해도 결과 수명의 문제는 남는다. 이 trace는 문서에서 도출한 연구자의 반례이며 실제 작성자의 수행이나 이번 세션의 실행 결과가 아니다. 새 mode 답을 받는다고 전체 원래 목표가 충분해지지는 않는다. 성능 선호도 mutex 안전성으로 충족됐다고 보지 않는다. `judgments.csv`의 `R1-multicall-order`와 `R2-speed`는 원래 R1/R2의 한계를 드러내는 별도 조건으로 남겼다.

### 감사·링크·단어 수정이면 진전이라는 가정 — S06·S07·S08

S06은 가능성 표현만 있어 실제 사용으로 세지 않았다. 실제 답이 연결한 [2021년 대화](https://sqlite.org/forum/forumpost/9f431ed4c1f6e82e7a32ad103cb57229df98b83c26f6420e115f3a2dea9989f5?t=r)는 다른 사건이며 마지막 anonymous의 동일성도 확정할 수 없다.

S07은 문서를 비교해 읽었다는 말이 있어 원문 조회의 하한 1건은 관측되지만, 원 질문 해결이나 구현은 보고하지 않았다. 제3자의 “이해가 맞다”는 승인도 PG 일반 VACUUM의 끝 페이지 반환 예외를 입증하지 않는다. 이 예외는 봉인 후보인 S-D11 PG14.1 공식 문서 L156–194에서 독립 확인했다.

S08은 실제 실패를 직접 보고했다. 실제 첫 답은 작은따옴표와 NOT NULL을 지적했지만 바인딩을 고치지는 않았다. 당시 [parser](https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/src/parse.y) L306–309·971–977·1006–1016은 INSERT 열 이름 위치에서 STRING을 허용하므로, 단일 인용 열 이름은 전혀 사용할 수 없다는 절대 명제도 이 SQLite 판에는 맞지 않는다. 반면 `VALUES(duration)`의 bare 식별자와 JS parameter 바인딩 문제는 따로 남는다. [공식 NOT NULL 테스트](https://github.com/sqlite/sqlite/blob/57acbb1380e3b51476aa8c71d1a881821f8ad5ff/test/notnull.test) 1.0–1.2b는 default 없는 필수 열 생략의 오류를 확인해 주며, 1.6은 default가 있을 때의 반례다. 이 테스트는 T1에서 추가로 연 사후 검증 자료이고 봉인 메시지의 입력에 있었던 자료로 소급하지 않는다.

## 분모와 비용

| 항목 | 8건 전체/원판 확정 | 미노출 7건 | 뜻 |
| --- | --- | --- | --- |
| I의 좁은 다음 행동 근거 / 보류 | 5 / 3 | 4 / 3 | 보류의 설명이 정확하다는 이유로 승인으로 세지 않음 |
| C의 좁은 다음 행동 근거 / 보류 | 5 / 3 | 4 / 3 | 조건부 기술 문장이 맞아도 실제 후보 선택은 보류 가능 |
| I가 원 목적 전체에 필요한 조건까지 다룸 | 3 | 2 | S02 조회 SQL 미제공, S07은 비교 일부 정정 |
| C가 원 목적 전체에 필요한 조건까지 다룸 | 3 | 2 | S08 C는 NOT NULL 조건이 빠져 binding 설명만 성립 |
| Q 값이 처음부터 있음 | 4 | 3 | S01·S02·S07·S08 |
| 신규 Q 값의 직접·유효 작성자 회수 | 0 | 0 | 같은 변수 직접 답만인 분모는 0건이므로 0/0은 해당 없음 |
| 상충 주장까지 포함한 값 회수 민감도 | 1 | 1 | S04, 성공 반환 확정으로 쓰지 않음 |
| 신규 Q 값 때문에 후보 선택 변경 | 0 | 0 | 결과가 0이라는 이유로 표본 교체 안 함 |
| 작성자 직접 성공 보고 | 1 | 0 | S01 자체 앱·플래그 비교. 전략 인과효과 아님 |
| 다른 실제 조언/상황의 실패 보고 | 2 | 2 | S04·S08. 봉인 I/C 실패로 귀속하지 않음 |

S01에서 3쌍, S04에서 3쌍의 실제 추가 정보 요청→작성자 답을 확인했다. 한 응답에 질문이 여러 개 있어도 왕복은 한 번이며 편집이나 감사는 새 왕복이 아니다. 메시지 쌍과 각각의 달력 시간은 `case-analysis.jsonl`에 있다. 요청→응답 구간이 겹칠 수 있으므로 합계를 인과적 지연이나 시간 절약으로 제시하지 않는다. S02·S04·S07에는 이 정의의 미답 실제 요청이 각각 한 번 남는다.

S01의 root→자가 성공 보고는 약 9.445시간이다. 이것을 I를 썼다면 줄었을 시간으로 바꾸지 않는다. S02·S03·S05의 작성자 후속 부재는 30일 창의 검열이며 거절이나 실패가 아니다. 8개 thread 모두 31–90일의 추가 발화가 없다. 90일 안의 자가 구현/재현 보고는 S01·S04·S08의 30일 안 발화와 중복되므로 별도 필드만 두고 독립 사건으로 더하지 않는다. 연결되지 않은 별도 구현·diff의 존재는 미확인이다.

가상 I/C는 추가 응답 없이 읽을 수 있다는 하한 0왕복, Q는 답이 온다는 조건에서 최소 1왕복으로 기록했다. 이 값은 관측 결과가 아니다. Q의 예상 달력 대기는 미확인이다. I/C가 보류하면 0왕복이어도 해결된 것이 아니다.

같은 8건에서 조건부 실제 답만으로 해결됐다고 작성자가 확인한 예는 0건이다. S03·S05의 실제 조건부 답과 S06의 가능성 반응까지 살폈으나 성공 확인으로 이어지지 않았다. 원래 목적을 대체한 새 요구가 시간 지연 때문에 발생했다고 확정할 사례도 0건이다. S07은 질문 범위 추가, S01은 발생 시점 불명의 늦은 선호다. S01의 권한 확인과 S04의 언어/wrapper 정보는 제한된 봉인 후보 둘의 판정을 각각 그대로 유지시켰다. 이것은 그 정보가 모든 다른 원인 가설에 무관하다는 뜻은 아니다.

## 원문 집계와 재현

T0는 대화 8개와 공급자 문서/테스트/설계 설명 8개를 최소수에 넣었다. T1에서 별도 공식 NOT NULL 테스트 S-TD02 하나를 추가하여 고유 최소수 산입 원문은 **17개 = 대화 8 + 공급자 9**다. 공급자 중 코드 속 설계 설명 S-D07·S-D08을 제외하는 엄격 문서/테스트 민감도는 7개다. API 문서 판이 다른 S-D06, 구현 소스, 같은 thread 댓글, 과거 링크 대화, 같은 원문의 재독을 증식시키지 않는다.

`t1-sources.json`의 S-S01…S-S08, S-D01, S-D12는 기존 ID를 재사용한 **추가 관측**이다. 원문을 새로 세지 않도록 `count_in_minimum=false`를 썼으며, 통합 시 기존 T0 행의 true를 false로 덮는 뜻이 아니다. ID별 원문을 합치고 관측 위치·한계만 추가해야 한다.

재현 명령은 소유 경로에서 다음과 같다. 원문 본문을 파일에 저장하지 않는다.

```sh
python docs/workstreams/research/AF-RES-026/streams/sqlite/collect_t1_metadata.py
python docs/workstreams/research/AF-RES-026/streams/sqlite/build_t1.py
python docs/workstreams/research/AF-RES-026/streams/sqlite/build_field_locations.py
```

첫 명령은 같은 원 thread의 고정 artifact 목록을 다시 읽는 메타데이터 수집이다. 네트워크 실패가 나면 `followup-metadata.json`의 error를 확인하고 동일 raw 주소만 재시도한다. 뒤 두 명령은 이미 저장한 메타데이터와 연구자 코딩을 바탕으로 표를 다시 만든다. 원래 연구의 판독 순서를 재연하는 실험은 아니다. `build_t0.py`는 봉인 파일을 다시 쓰므로 이 재현 절차에서 실행하지 않는다.

## 남은 중요한 약점과 다음 한 조사

| 약점 | 영향을 받는 판단 | 다음 최소 조사 |
| --- | --- | --- |
| S04의 원앱/재현 계보와 COMMIT 성공 반환이 연결되지 않음 | Q 값을 받았다는 이유만으로 원인 분기를 승인할 수 있는가 | FMDB 원앱과 재현 코드의 동일 실행을 증명하는 완전 트랜잭션/성공 반환 로그 한 묶음을 찾기 |
| S05의 mode만으로는 statement 순서·성능까지 판정할 수 없음 | 한 변수 질문이면 충분한가 | 실제 statement ID·소유 thread·reset/step/column 순서가 드러나는 당시 trace 한 건 확보 |
| 유일한 자가 성공 S01은 봉인 전 한 문장 노출, 다른 사례는 성공 보고 부족 | I/C/Q의 사실 충분성과 실제 진전을 같은 효과로 해석할 위험 | 이미 고른 S02·S03·S05·S06 중 한 원 thread에 명시적으로 연결된 작성자의 90일 내 적용 기록을 찾되 새 성공 사례로 표본을 교체하지 않기 |
