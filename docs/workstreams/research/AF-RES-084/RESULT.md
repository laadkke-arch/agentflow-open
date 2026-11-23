# AF-RES-084 · 개설 본문과 당시 소비판은 후보 판정을 바꾸는가

**PARTIAL.** 개설 본문 대비는 0/16셀에서 가능했다. 최초 확보본으로 판정 가능한 10셀은 080의 결과와 모두 일치했다. 최초판을 복원하면 적합 판정이 변하는지는 미확인이다.

## 표 1. 사례, 개설 증거, 두 조건과 소비판

| 사례ID·층 | 생성 이벤트·최초 원문 URL·지문 | 최초 확보본과의 의미 차이 | 당시 C1·C2 | 질문판·성공판·실행자 근거 | 미확인 |
| --- | --- | --- | --- | --- | --- |
| CN01 · 자연 | 2022-01-09 20:42:23Z, ID 1097298383. [개설 시간](https://data.gharchive.org/2022-01-09-20.json.gz), 이벤트·개설 지문 미확인. [최초 확보본 자리](https://github.com/pallets/click/issues/2172) `a0badd47…/c66f636f…` | 복원 실패. 080과 이번 공개본의 raw 지문은 일치 | 확보본 C1 옵션 없이 Names 입력, C2 한 줄의 두 이름을 별개 값으로 전달 | skieffer 질문 Click 8.0.3·Python 3.8.12. 오류 코드 고정 SHA가 8.0.3과 일치. 제3자 우회 제안과 작성자 질문. [질문 코드](https://github.com/pallets/click/blob/41f5b7a7967bb65910e8837bd4e8542a18feec6c/src/click/core.py#L2243-L2259) · [작성자 후속](https://github.com/pallets/click/issues/2172#issuecomment-1011573184) | 개설 본문, OS/TTY, 작성자 성공 실행 |
| AN01 · 자연 | 2022-01-23 13:15:53Z, ID 1111868357. [개설 시간](https://data.gharchive.org/2022-01-23-13.json.gz), 이벤트·개설 지문 미확인. [최초 확보본 자리](https://github.com/python-attrs/attrs/issues/911) `c3335039…/884a794a…` | 복원 실패. 080과 이번 공개본의 raw 지문은 일치 | 확보본 C1 생성자 인자는 a,b만, C2 초기 sum은 None | UGuntupalli가 `field(default=None, init=False)` 대입을 제안했다. 유지보수자는 필드 줄에 동의하며 `int`에 None이 맞지 않는다고 지적했다. [작성자 제안](https://github.com/python-attrs/attrs/issues/911#issuecomment-1019502089) · [유지보수자](https://github.com/python-attrs/attrs/issues/911#issuecomment-1019509912) | 개설 본문, 원 질문의 attrs·Python, 생성한 객체·출력 |
| CC01 · 교정 | 2022-04-07 12:41:17Z, ID 1195991112. [개설 시간](https://data.gharchive.org/2022-04-07-12.json.gz), 이벤트·개설 지문 미확인. [최초 확보본 자리](https://github.com/pallets/click/issues/2250) `c7e9dc1c…/cea0a191…` | 복원 실패. 080과 이번 공개본의 raw 지문은 일치 | 확보본 C1 -V 등록, C2 -V가 명시 alpha 출력 | chr7 질문 Click 8.1.2·Python 3.10.3에서 오류. 같은 날 위치 인수로 바꿔 작동했다고 보고. [단계별 댓글](versions.jsonl) · [성공 진술](https://github.com/pallets/click/issues/2250#issuecomment-1091807779) | 개설 본문, 저자 후속의 실제 -V stdout·종료 및 설치판 |
| AC01 · 교정 | 2022-06-16 13:13:09Z, ID 1273548531. [개설 시간](https://data.gharchive.org/2022-06-16-13.json.gz), 이벤트·개설 지문 미확인. [최초 확보본 자리](https://github.com/python-attrs/attrs/issues/971) `cd5ccfc5…/363211ba…` | 복원 실패. 080과 이번 공개본의 raw 지문은 일치 | 확보본 C1 완성 클래스의 이름 기본값으로 한 번 등록, C2 int→Int 및 int-range→IntRange | sscherfke가 일반 훅과 `attr.define(slots=False)`에서 작동했다고 보고. 작동 예제는 int만 조회. 참조 전용 훅은 후대 추가. [저자 보고](https://github.com/python-attrs/attrs/issues/971#issuecomment-1159394251) · [릴리스 이력](https://github.com/python-attrs/attrs/blob/7bfc49e9b22d5ba25b6e429524c3d49fee27cb36/CHANGELOG.md#L217) | 개설 본문, 질문판, 성공판 및 두 키의 최종 클래스 출력 |

지문은 **최초 확보 raw / 줄끝만 LF로 정규화** 순서다. 전체 지문, 저장소/이슈 불변 ID, 실제로 본 닫힘 이벤트는 원장에 있다. 각 행의 개설 날짜는 이슈 메타데이터로 확인했다. [이벤트 원장](events.jsonl) · [가린 요구표](inputs.csv)

## 표 2. 네 사례의 16셀

| 사례·셀 | 입력판·목록 범위·소비판 | 기능·원문 절 | 옛 판정→재판정 | 바뀐 단일 축·이유 | 두 조건 충족·반례·미확인 |
| --- | --- | --- | --- | --- | --- |
| CN01 NR | 확보/개설 · 좁음 · 8.5.1 | 옵션·프롬프트 메뉴 CL01–02 | 확보 부재→부재 · 개설 미확인 | 기준 셀. 입력판을 바꿀 개설 증거 없음 | 조합 미등재 |
| CN01 BR | 확보/개설 · 넓음 · 8.5.1 | `click.Option.prompt`, `multiple` CL03–07 | 확보 반박→반박 · 개설 미확인 | 범위 ↑. 두 설정의 실제 변환 경로 노출 | C1만. 문자열 거부, 명령 내 분해는 별도 구성 |
| CN01 NE | 확보/개설 · 좁음 · 8.0.3 | 옵션·프롬프트 메뉴 CL08–09 | 확보 부재→부재 · 개설 미확인 | 소비판만 8.5.1→8.0.3. 결과 동일 | 조합 미등재 |
| CN01 BE | 확보/개설 · 넓음 · 8.0.3 | `click.Option.prompt`, `multiple` CL10–14 | 확보 반박→반박 · 개설 미확인 | 넓은 범위에서 소비판만 변경. 결과 동일 | C1만. 독립 프로세스에서 iterable 오류 |
| AN01 NR | 확보/개설 · 좁음 · 26.1.0 | `attrs.field`·초기화 메뉴 CL15–16 | 확보 부재→부재 · 개설 미확인 | 기준 셀. 입력판 가림 유지 | 같은 설정 미등재 |
| AN01 BR | 확보/개설 · 넓음 · 26.1.0 | `attrs.field.default + attrs.field.init` CL17–19 | 확보 양성→양성 · 개설 미확인 | 범위 ↑. 같은 필드의 두 옵션 | C1·C2. init=True이면 C1 실패 |
| AN01 NE | 확보/개설 · 좁음 · 정확판 미확인 | `attrs.field` 하위 설정 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 소비판 대비 대기 | 원 질문의 Python·attrs |
| AN01 BE | 확보/개설 · 넓음 · 정확판 미확인 | `attrs.field.default + attrs.field.init` 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 소비판 대비 대기 | 원 질문의 Python·attrs 및 동판 구문 |
| CC01 NR | 확보/개설 · 좁음 · 8.5.1 | 옵션·데코레이터 메뉴 CL01–02 | 확보 부재→부재 · 개설 미확인 | 기준 셀. 해당 기능의 하위 절은 범위 밖 | 사용자 -V 조합 미등재 |
| CC01 BR | 확보/개설 · 넓음 · 8.5.1 | `click.version_option` CL20–23 | 확보 양성→양성 · 개설 미확인 | 범위 ↑. 버전 값과 플래그의 위치 바인딩이 보임 | C1·C2. `param_decls` 키워드에서는 TypeError |
| CC01 NE | 확보/개설 · 좁음 · 성공판 미확인 | `click.version_option`의 목록 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 성공 소비판 대비 대기 | 성공판과 -V 실행 영수증 |
| CC01 BE | 확보/개설 · 넓음 · 성공판 미확인 | `click.version_option`의 절 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 성공 소비판 대비 대기 | 8.1.2 질문판 실행은 보조 |
| AC01 NR | 확보/개설 · 좁음 · 26.1.0 | 초기화 훅 메뉴 CL16, CL24 | 확보 부재→부재 · 개설 미확인 | 기준 셀. 대체 훅 존재는 설명에 언급 | 전용 이름·두 키 구성 미등재 |
| AC01 BR | 확보/개설 · 넓음 · 26.1.0 | `attrs.hook.__attrs_init_subclass__` CL25–29 | 확보 양성→양성 · 개설 미확인 | 범위 ↑. 클래스 준비 후 전용 훅 확보 | C1·C2는 전용 훅. 별칭으로 조인한 저자 `slots` 방법은 별도이며 둘째 키 실패 |
| AC01 NE | 확보/개설 · 좁음 · 성공판 미확인 | `attr.define.slots` 목록 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 성공 소비판 대비 대기 | 성공판·키별 결과 |
| AC01 BE | 확보/개설 · 넓음 · 성공판 미확인 | `attr.define.slots` 동작 근거 조회 대기 | 확보 미확인→미확인 · 개설 미확인 | 성공 소비판 대비 대기 | 21.4.0 대조만 관측, 당시 채택 미확인 |

등재 부재는 해당 범위에서 개별 기능·조합의 직접 등재 부재를 뜻한다. 최상위 메뉴 다음에 연결 문서를 열면 넓은 범위가 된다. 열마다 080 판정과 이번 재판정, 기능 ID의 별칭, 소스 파일과 절의 SHA-256을 조인했다. 입력판 대비와 소비판 대비의 분모는 별도로 계산했다. [16셀 원장](cells.csv) · [쌍 원장](pairs.csv) · [절 지문](fixtures/clauses.jsonl)

## 표 3. 양성과 경계 실행

| 사례·양성 또는 경계 | 실제 실행판·입력 | 기대·관측·종료 | 근거 주소 또는 로그 | 답변 상태·다음 확인 |
| --- | --- | --- | --- | --- |
| CN01 양성 | Click 8.0.3/Py3.8.12 및 8.5.1/Py3.12.14. 명령 내 prompt와 분해, stdin `foo bar\n` | 두 이름·CLI 0 기대, 두 배포에서 일치. 명시적 사용자 코드 | [새 실행](runs.jsonl#L17) | 원문의 해당 절 제공. 사용자 코드가 허용될 때만 이 실행 예를 첨부 |
| CN01 경계 | 같은 두 환경과 입력, 기본 `multiple=True, prompt='Names'` | 프롬프트 표시·iterable 오류·이름 없음·CLI 1 기대, 두 배포에서 일치 | [새 실행](runs.jsonl#L18) · [8.0.3 문서](https://github.com/pallets/click/blob/41f5b7a7967bb65910e8837bd4e8542a18feec6c/docs/options.rst#L394-L440) | 원문의 해당 절 제공. 사용자 요구가 재구성 허용 여부를 정함 |
| AN01 양성 | attrs 26.1.0/Py3.12.14. a,b=11,23, sum에 None 기본값·init=False | 인자 a,b와 sum=None 기대, 일치 · 프로세스 0 | [새 실행](runs.jsonl#L21) | 이 판 또는 같은 동작이면 조건부 제공 |
| AN01 경계 | 같은 판·a,b·기본값, init=True | sum이 인자로 추가되고 초기값은 None 기대, 일치 · 0 | [새 실행](runs.jsonl#L22) | 원 질문에서 사용한 attrs·Python 필요 |
| CC01 양성 | 질문판 Click 8.1.2/Py3.10.3 새 실행, 참조 8.5.1/Py3.12.14는 080 영수증. 두 위치 인수로 등록 | 두 판에서 -V 등록·`probe, version alpha`·CLI 0, 기본 --version CLI 2 | [질문판 보조](runs.jsonl#L23) · [참조 재사용](runs.jsonl#L1) | 이 판 또는 같은 서명이면 조건부 제공 |
| CC01 경계 | 같은 두 판, `param_decls`를 키워드로 등록 | TypeError로 등록에서 멈춤. 관측 프로세스 0, CLI 미호출 | [질문판 보조](runs.jsonl#L24) · [참조 재사용](runs.jsonl#L2) | 성공판 채택 판단에는 작성자 -V 출력과 버전 행 필요 |
| AC01 양성 대비 | attrs 26.1.0/Py3.12.14 전용 훅은 080 영수증. 21.4.0/Py3.10.3의 저자형 slots=False는 새 역사 대조. 두 키 조회 | 전용 훅 2회, Int/IntRange 최종 클래스. 대조의 일반 훅은 2회지만 int→IntRange, int-range KeyError. 프로세스 모두 0 | [과거판 대조](runs.jsonl#L25) · [참조 재사용](runs.jsonl#L3) | 실제 성공판 채택은 보류. 저자 실행의 attrs·Python, 두 키 정체성 필요 |
| AC01 경계 | 같은 역사 대조와 참조판, 기본 slots의 일반 훅 | 두 판 모두 훅 4회, int가 교체 전 IntRange, int-range는 최종 IntRange. 프로세스 0 | [과거판 대조](runs.jsonl#L26) · [참조 재사용](runs.jsonl#L4) | 같은 두 키와 클래스 조립 순서를 성공 환경에서 비교 |

## 분모

| 단위 | 관측 / 계획 | 해석 |
| --- | --- | --- |
| 영향을 본 고정 요청과 셀 | 4/4 요청, 16/16 셀 생성 | 두 입력판은 셀 안의 쌍이다. 모집 120 자연·200 교정과 원 엄격 48셀은 보존했다 |
| 개설 원본문과 엄격 셀 | 개설 0/4, 편집 대조 0/1, 엄격 판정 가능 0/16 | 원문 비교 가능 0/16, 변화율 산출 불가 |
| 최초 확보본 판정 | 판정 가능 10/16, 양성 3, 반박 2, 범위 내 미등재 5, 미확인 6 | 080과 다른 판정 0/10. 이번 공개본과 080 raw 지문 동일 4/4 |
| 두 범위의 비교가 가능한 요청 | 확보본 참조 4/4, 확보본 정확 1/4, 엄격 참조 0/4 및 정확 0/4 | 참조 범위를 넓혀 양성 3/4. CN01은 부재→반박. 정확판에서는 0/1 양성 |
| 두 소비판의 비교가 가능한 요청 | 확보본 좁음 1/4 및 넓음 1/4, 엄격 양쪽 0/4 | 확보본 소비판 짝 2/8 판정 가능, 변화 0/2. 네 셀이 모두 알려진 요청 1/4 |
| 실사용자 성공 소비판 | 교정 0/2, 원 교정 0/5. 정확 환경을 명시한 질문은 1/2 자연 | 교정의 저자 성공 진술은 2건. 같은 실행 로그와 판 번호가 모두 잡힌 성공 0건 |
| 실행한 입력 | 새 프로세스 10/10 예상 일치, 네 사례의 참조 입력 8/8 관측 | 참조 4개 새 실행·4개 재사용. 지정 버전 일치 CN01 2/8 정확판 입력, 나머지 6/8 미실행. 엄격 개설 출처와 연결된 역사 재연 0/8 |
| 추가 대조 입력 | CC01 질문판 2/2, AC01 역사판 2/2 | 두 종류는 새 10개에 포함. 080의 참조 8개 프로세스를 반복하지 않음 |
| 자료와 대조 | 91 판독 행 · 31 계보(외부 30), 독립 비교 대조 6개 이상, 타 분야 2개 | 행/판/미러와 원 사건을 동일 분모로 쓰지 않는다. 접근 실패는 시도 원장에 있다 |

**0/0은 산출 불가다.** 16개 중 10개에서 판정을 재생한 것은 16개 엄격 셀을 확인했다는 의미로 환산할 수 없다. 기본값과 입력 채널이 달라지면 같은 기능도 답이 달라지므로, 이 목적 표본으로 모집 전체 대표성이나 재작업 감소를 추정하지 않는다. [자동 검산](metrics.json) · [자료 원장](sources.jsonl) · [시도 원장](attempts.jsonl)

## 개설 증거와 가림

GH Archive 발행자가 설명하는 원천은 GitHub 공개 Events API다. 2022년 사건마다 해당 UTC 시간과 다음 파일을 요청했지만 Cloud 프록시에서 모두 403이었고 응답 본문을 받지 못했다. 웹 도구에서 원 시간 파일과 ClickHouse의 공개 원파일 미러도 열리지 않았다. 공개 GitHub HTML에서는 대상 ID, 현재 Description, 닫힘 타임라인을 읽었다. 인증 GraphQL 조회는 403이었고 익명 화면의 수정 필드는 비었다. Wayback 캡처와 당시 전체 본문 첨부도 확인되지 않았다. 중복 미러 경로들을 독립 목격으로 세지 않았다. [이벤트 스키마](https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#issuesevent) · [시간별 자료 정책](https://www.gharchive.org/) · [미러 수집 설명](https://ghe.clickhouse.tech/) · [실제 경로와 UTC](attempts.jsonl)

#1060은 작성자가 후속 댓글에서 BUG 설명 추가를 인정했고 최신 본문에 후속 `evolve` 구간이 있다. 개설 이벤트는 읽지 못했으므로 처음에 어떤 문자열이 있었는지는 복구하지 못했다. 검증된 수정 사례인 github-page #1에서도 익명 `lastEditedAt`가 null이지만 공개된 인증 조회에서 내용이 다른 리비전 세 개를 읽을 수 있었다. 생성 시각과 최신 본문을 함께 담은 dear-github #129의 작성자 REST 예도 개설 본문 증거가 되지 않았다. [#1060 작성자](https://github.com/python-attrs/attrs/issues/1060#issuecomment-1329862116) · [별도 리비전 예](https://github.com/orgs/community/discussions/33551) · [#129 REST 대조](https://github.com/dear-github/dear-github/issues/129)

네 건의 C1·C2·금지조건·버전·선행 해법은 Description만 들어 있는 투영으로 판독해 ②에서 봉인했다. 이후 080의 정답과 판정, 해당 네 사례의 후속 답을 읽었다. 같은 작업자가 판독과 재판정을 했다. 배정문이 공개한 클래스·플래그·입력의 기대와 당시 배포 여부는 독립적으로 가리지 못했다. Q3의 개설 대비에서 raw 동일, 줄끝만 변경, 기타 바이트 변경, 의미 변경은 각각 확인 0건이고 복원 실패 4건이다. 이번 공개본과 080 확보본 사이의 raw 동일 4건은 별도 관측이다. [봉인 커밋](https://github.com/laadkke-arch/agentflow-open/commit/d3ff13eee67c7f81ddd39302d1f35576ef2b4423) · [판독 규칙](SCOPE.md)

## 채택률이 부풀려지는 경우

- **해시 차이만으로 검색 답이 바뀌지 않는다.** 080 모집 원장의 Git LF 바이트와 봉인의 CRLF 바이트를 둘 다 대조했다. 줄끝 변환 하나로 봉인의 SHA-256과 일치했고 같은 320개 순번과 16셀을 재생했다. 이슈 원본 변화의 근거는 별도로 필요하다. [바이트 검산](evidence/fixture-correction.md)
- **본문 지문이 같아도 사용판은 남지 않을 수 있다.** CC01의 확보본과 이번 공개본은 같고 작성자는 같은 날 성공했다는 줄을 남겼다. 같은 교환의 앞선 8.1.2 버전 줄을 성공에 붙일 증거는 없다. 그와 달리 Click #2276 작성자는 8.0.2에서 8.1.3으로 바꾸고 해결했다고 판을 직접 연결했다. #2276의 Bash 감지는 이번 고정 표본 밖이다. [CC01 저자](https://github.com/pallets/click/issues/2250#issuecomment-1091807779) · [#2276 저자](https://github.com/pallets/click/issues/2276#issuecomment-1117371871)
- **기능 이름과 공식 성공 구성의 ID가 다를 수 있다.** AC01의 글에서 보고한 방식은 `attr.define.slots`로 조인된다. 넓은 참조판에서 두 키를 지킨 것은 24.1.0부터 등장한 `__attrs_init_subclass__`다. 일반 훅으로도 `__qualname__`을 키로 쓰는 상류 예는 성공한다. 같은 키가 최종 클래스로 덮이는 그 예를 필드 기본값 키에 적용하면 비교 입력이 바뀐다. [공식 절](https://github.com/python-attrs/attrs/blob/7bfc49e9b22d5ba25b6e429524c3d49fee27cb36/docs/init.md#L555-L588) · [다른 키의 시험](https://github.com/python-attrs/attrs/blob/7bfc49e9b22d5ba25b6e429524c3d49fee27cb36/tests/test_init_subclass.py#L46-L66)
- **같은 메뉴의 기능을 한 구성으로 묶기 어려울 수 있다.** CN01은 프롬프트 동작과 반복 플래그가 각각 목록에 있지만, 한 줄을 입력하면 두 판에서 변환 오류가 난다. #218은 예전 코드가 프롬프트에서 문자를 일일이 나누었고 argv와 환경변수에서는 단어를 나눴다는 별도 관측이다. #2356에서는 같은 8.1.3의 상류 시험이 프롬프트에서 선택값을 숨겼지만 실제 보고의 입력은 `--help`였다. [#218 관측](https://github.com/pallets/click/issues/218) · [#2356 실제 출력](https://github.com/pallets/click/issues/2356) · [동판 상류 입력](https://github.com/pallets/click/blob/9c6f4c8e1bb8670ce827c98559f57f6ee5935cd0/tests/test_termui.py#L198-L220)
- **수집자, 배포자, 실행자의 시계가 다르다.** GH Archive의 시간 파일은 공개 피드에서 확인 가능한 것을 보존한다. 2025년 자료 이용자들은 시간별 관측 급감을 기록했다. 이는 2022년 대상 행의 실제 누락을 확정하지 않는다. PyPI의 wheel SHA와 배포일은 설치 파일을 고정할 수 있어도 개인 실행과 연결되지 않는다. 우리가 실행한 로그는 명시된 로컬 입력과 받은 pinned wheel을 연결한다. [수집 대조](https://github.com/igrigorik/gharchive.org/issues/310) · [배포 원장](fixtures/wheels.json) · [실행 원장](runs.jsonl)

### 타 분야의 실제 발행과 인용

- **학술 공개판.** Micheli 등의 2010.03813v1은 2020-10-08, 오타 수정으로 표기된 v2는 2020-10-09다. 읽은 표 3·결론의 100MB 관측은 두 판이 같았다. 2022년 6월 BERTrade가 소규모 코퍼스 학습의 선례로 이용한 인용은 2020년 11월 EMNLP 논문이다. 그 참고문헌에서 실제로 열어 본 프리프린트의 판까지는 알 수 없다. [v1 원문](https://arxiv.org/html/2010.03813v1#S8) · [v2 정정 기록](https://arxiv.org/abs/2010.03813v2) · [v2 결론](https://arxiv.org/html/2010.03813v2#S8) · [2022 실제 인용](https://aclanthology.org/2022.lrec-1.119.pdf)
- **표준 정오표.** RFC 2978의 2000년 10월 원문은 charset 규칙에 작은따옴표와 중괄호를 포함한다. EID 1912는 작은따옴표를 제거했고 EID 5433은 중괄호도 제거했다. 2010년 2월 IETF 초안이 1912를, 2022년 6월 RFC 9110 §8.3.2가 둘을 실제로 인용했다. 예를 들어 UTF-8은 수정과 무관하게 허용된다. 인용은 수정이 존재했던 상한을 주며 개별 구현의 적용 시각은 남기지 않는다. [2000 원문](https://www.rfc-editor.org/rfc/rfc2978.html#section-2.3) · [검증된 정오표](https://www.rfc-editor.org/rfc/inline-errata/rfc2978.html) · [2010 인용](https://datatracker.ietf.org/doc/html/draft-reschke-rfc2231-in-http-09) · [2022 인용](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3.2)

## 답변에 붙일 조건

CN01은 8.0.3의 프롬프트 절과 실제 오류까지만 반환할 수 있다. AN01은 `@define`과 `field(default=None, init=False)`의 같은 구성에 한해 반환할 수 있다. CC01은 위치 인수 서명을 확인한 Click 판에서 `version_option('alpha', '-V')`를 조건부로 제공할 수 있다. AC01은 저자의 실제 성공 환경에서 두 키가 최종 클래스에 연결됐는지 보류한다. 현대판이 허용되는 별도 요청에서는 전용 훅과 참조판의 두 키 실행을 제시할 수 있다. [범위·판·동작 연결](cells.csv) · [실행 증거와 입력](runs.jsonl)

## 판단을 바꿀 세 가지 약점과 다음 확인

1. **개설 본문이 비어 있다.** 읽기 가능한 환경에서 먼저 #1060의 2022-11-28 00·01 UTC 파일과 불변 이슈 ID 1465633178을 넣어 유일한 `IssuesEvent/opened`를 찾는다. raw·LF 해시와 `evolve` 추가 전후를 확인한 뒤 네 고정 건에도 같은 입력 투영을 다시 봉인한다.
2. **교정의 성공 환경이 빠져 있다.** CC01은 위치 인수 호출의 같은 로그에 `-V` stdout·종료·패키지/Python 행을, AC01은 같은 실행에서 두 키 및 클래스 동일성과 패키지/Python 행을 연결한다. AN01은 질문 시점의 Python·attrs를 확인한다. 이 입력이 생기면 고정된 범위 규칙으로 해당 정확판만 추가할 수 있다.
3. **AC01의 정상 호출 수와 정답 객체가 갈라졌다.** 성공 환경에서 동일 상속 구조, 같은 두 키로 저자 slots=False, 공식 전용 훅 및 일반 slotted 경계를 실행한다. 각 키의 객체 정체성, 훅 시점과 네임스페이스를 각각 기록해 문서의 대안이 당시 요구에도 맞는지 판정한다.
