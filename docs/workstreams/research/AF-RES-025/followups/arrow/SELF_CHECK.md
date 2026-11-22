# Arrow 후속 단계 자체 점검

검사 시각: 2026-11-22T06:17:35.433341+00:00. 관측 파일·분모·참조·회수 해시 점검 355개가 모두 통과했다. 소프트웨어 runtime 테스트는 0회다. 결과는 `validation.json`에 있고, 재집계 명령은 아래와 같다. 이 자기 점검은 사람의 독립 검증이 아니다.

```sh
python docs/workstreams/research/AF-RES-025/followups/arrow/build_followups.py
python docs/workstreams/research/AF-RES-025/followups/arrow/validate_followups.py
```

첫 명령은 이미 기록한 관측·판정을 다시 JSON/JSONL로 직렬화한다. 두 번째 명령은 원 반환 19개와 history19개 일치, Q01–Q04 각 결정1개, 자료 스키마·ID·봉인 후 UTC, 실제 성공 응답90개의 sha256, 실패3개 최소수 제외, 비용과 미실시 검증의 구분을 확인한다. 원문 cache가 없는 새 환경에서는 위 해시 비교를 위해 별도 복구 디렉터리에서 원 URL을 다시 받아야 한다. 살아 있는 API 응답 전체 해시는 변경될 수 있으므로 고정 commit/blob과 최초 영수증을 함께 보존한다.

| 상위 연구 질문 | 이번 후속 단계의 주장·반증 시도 | 직접 근거·결과 | 남은 한계 |
| --- | --- | --- | --- |
| Q1 | 최초 원장 문서와 후속 구현을 섞지 않는다. Arrow2의 최초 branch head를 현재 Git 이력으로 역산할 수 있는지 확인했다. | AR-F019, AR-H040; author/committer 날짜와 첫 공개는 다르며 branch head 복구 실패를 유지한다. | Force-push와 당시 공개 head 스냅샷 미확인. |
| Q2 | 새 답을 후속에서 찾더라도 원 검색 결과를 보강하지 않는다. | 주 판정 봉인 d1f506b1dde91e706360846f4c2eac5baabe492e 뒤의 요청 UTC; `frozen_returns_changed=false`; 새 ScalarValue/Java 테스트는 후속층. | 동일 모델 에이전트가 원 Arrow 검색과 후속 판독을 수행했다. |
| Q3 | 실패·재시도·당대판 단서를 별도 비용으로 남긴다. | HTTP93회=성공90+실패3, 별도 웹 검색4회; `cost-summary.json`; 잘못 추정한 Java 시험 경로 실패를 보존했다. | 검색 제공 순위의 재현성은 원 discovery로그 범위이며 이 후속 검색에 과거 ranking을 주장하지 않는다. |
| Q4 | 현재 필수 근거와 당시 구현을 구분한다. | AR-H006, AR-H021, AR-H022, AR-H050, AR-H064; 옵션은2025, Java 버퍼는2020 일부지원, C Data 공식 현재 테스트는 postseal추가. | 신선한 Java 테스트 원문이 원 반환의 빠진 인용을 구제하지 않는다. Runtime0회. |
| Q5 | 관계가 당대에 있어도 target adapter가 없으면 완전해지지 않는다. | AR-H031; Bevy0.4의 공통 List.get→dyn Reflect가 실제 존재. | Arrow adapter·null/소유권 경계와 도입 노력 미확인. 라이브러리/제조 보조는 이 에이전트가 열지 않았다. |
| Q6 | 표현된 선택·실제 변경·미확인을 나눈다. 동명/후대/버전 반례를 찾는다. | AR-F007, AR-F022, AR-F026, AR-F017, AR-H030; Q02표현된수용만, Q03통합코드, Q04이행보류/별도개발,2018quiver는현재API와다름. | 당사자 미인지로 추론하지 않는다. Q01채택, Q02후속호출부 diff 미확인. |
| Q7 | 현재 유효성과 당시 유효성을 구분해 분모를 유지한다. | `candidate-history.jsonl`19개=not_available10+unknown9+supported0. 원 반환 슬롯/순위/판정 불변. | 부분존재는 supported로 올리지 않는다. 이 분포는 신규 검색 성공률이나 인시 절감률이 아니다. |

## 실제로 반박된 간단한 결론

1. “현재 Arrow 문서에서 찾았으니 2021년에도 그 설정을 쓸 수 있었다”: PyArrow20/21 태그와 2025 PR diff가 반박한다(AR-H003, AR-H004, AR-H006, AR-H021). Java1.0에 큰 버퍼 일부가 있었다는 것은 별도 조건이다.
2. “등록된 제품 이름이 오래됐으니 현재 부품도 오래됐다”: quiver0.0.1의 원 패키지 파일과2026의 새 저장소가 반박한다(AR-H030, AR-H029). DataFusion의 host 이름 hit도 ScalarValue 동작 hit를 뜻하지 않는다.
3. “형 구조가 맞으므로 이행할 수 있다”: Arrow2 작성자의 Parquet 검증 공백·보류 결정과 Feb8 slice 코드 판독이 반례다(AR-F017, AR-F027). 메모리 안전성 취약점이나 실행 실패를 관측했다고 확대하지 않는다.

## 파일과 비용 점검

- 고유 원반환 후보19개 전체에 판별 근거·미확인·다음 최소 확인이 있다.
- 자료 레코드93개 가운데 로컬 신규 원문 산입 표시는32개다. 이전 discovery의 역사판·동일 원천·API/검색 메타데이터는 보수적으로 제외했다. 전체 저장소의 최종 중복 제거는 root 자료 원장이 우선한다.
- 직접 읽은 후속 메일11개와 실제 PR 논의/구현 변경이 있으며 네 원질문 각각 후속 원문2개 이상이 있다. 새 URL 개수를 독립 사건수로 쓰지 않는다.
- 요청별 HTTP 벽시간 합은 621902ms, 웹 검색 합은 4098ms다. 병렬화되었으므로 합계는 실제 경과 시간이 아니다. 첫~마지막 요청 간격은 1311.387초이며 모델 판독 전체시간이나 인시와 같지 않다.
- 실행 환경 준비·의존성 설치·JavaJNI/4GiB 테스트·Rust 컴파일을 하지 않았다. README의 명령은 다음 실행 입력이며 성공 영수증이 아니다.

## 남은 중요한 약점 3건과 각 후속 조사

1. Q01의 실제 Python→Java C Data 경계와 큰 버퍼 한계: README의 PyArrow21 입력과 Java 고정 RoundtripTest를 먼저 실행한 뒤 같은 프로세스 embedding fixture로 두 경계를 연결한다. 작은 C Data 형 확인과 >2GiB 확인을 따로 남긴다.
2. Q02의 표현된 수용과 실제 코드 변경 차이: 작성자 gist 또는 실제 Table 저장소의 수용 이후 diff 한 건을 확보해 StringArray downcast 호출부가 ScalarValue로 대체됐는지 확인한다.
3. Q04 최초 공개 head와 포맷별 검증 공백: 최초 메일 시각의 branch/ref 아카이브 및 Parquet golden fixture 결과를 찾아 정확한 당시 지원 범위를 한정한다. 현재 arrow2나2022 ScalarBuffer를 처음부터 있던 답으로 돌리지 않는다.
