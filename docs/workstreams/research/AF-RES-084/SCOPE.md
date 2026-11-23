# AF-RES-084 범위와 판단 규칙

계획 기준 `e7a777f2c13b626532b5828591d6388743688b34`. GitHub에 작업 ref가 없는 것을 확인하고 최신 통합판 `f736bd557fa4c40aecb6833165823196cfa42af2`에서 `work/research-af-res-084`를 만들었다. 통합판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 진행표의 자기 행을 읽었다. 진행표의 유일한 의존 작업은 AF-RES-080이다. [배정판](https://github.com/laadkke-arch/agentflow-open/blob/f736bd557fa4c40aecb6833165823196cfa42af2/docs/automation/dot-control.json#L1946) · [080 인계](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/HANDOFF.md) · [세션 계약](manifest.json)

| ID | 층 | 원 이슈 | 저장소 ID | 이슈 ID | 생성 UTC |
| --- | --- | --- | ---: | ---: | --- |
| CN01 | 자연 | [Click #2172](https://github.com/pallets/click/issues/2172) | 19103692 | 1097298383 | 2022-01-09 20:42:23Z |
| AN01 | 자연 | [attrs #911](https://github.com/python-attrs/attrs/issues/911) | 29918975 | 1111868357 | 2022-01-23 13:15:53Z |
| CC01 | 교정 | [Click #2250](https://github.com/pallets/click/issues/2250) | 19103692 | 1195991112 | 2022-04-07 12:41:17Z |
| AC01 | 교정 | [attrs #971](https://github.com/python-attrs/attrs/issues/971) | 29918975 | 1273548531 | 2022-06-16 13:13:09Z |
| EDIT1060 | 편집 대조 | [attrs #1060](https://github.com/python-attrs/attrs/issues/1060) | 29918975 | 1465633178 | 2022-11-28 00:29:53Z |

고정 네 건은 층별·프로젝트별 첫 배정 자리다. EDIT1060은 대조 전용이다. 080의 모집 120 자연과 200 교정, 48셀, 기존 목록 6개의 분모를 참조한다. 모집·기존 카탈로그·참조판 8개 프로세스는 재실행하지 않는다.

## 최초 본문 증거

1. 공개 이슈의 저장소·이슈 불변 ID, 번호, 개설 시각을 기준으로 삼는다. UTC 해당 시간 파일을 기본으로 하고 인접 파일을 추가 조회하면 경계·수집 지연과 함께 표시한다. GH Archive는 GitHub Events API에서 수집하는 미러다. 같은 이벤트 ID·내용과 여러 경로는 하나의 사건이다. [이벤트 형식](https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#issuesevent) · [보관 방식](https://www.gharchive.org/)
2. `IssuesEvent / opened`에서 repo ID, issue ID, 번호, issue.created_at이 맞고 본문 문자열이 있어야 한다. 이벤트 자체의 ID·UTC·개설자도 검증한다. 여러 원본이 상충하거나 열린 행이 본문을 잃었으면 미확인이다. 기본 해시는 UTF-8 SHA-256이며 별도 해시는 CRLF/CR만 LF로 옮긴다. 끝공백·여백·유니코드는 그대로 둔다.
3. 시간 자료가 열리지 않으면 공식 수정 이력의 **생성 리비전** 또는 당일 작성자의 고정 첨부에서 이슈·시각·전체 본문 연결을 요구한다. 열린 시각, 최신 body/checksum, rendered HTML, 편집 표시, 답변자 댓글, 빈 패널은 각각 독립적으로 미확인이다. 공개 수정 이력에는 삭제·보존 한도가 있다. [공식 이력 정책](https://docs.github.com/en/communities/moderating-comments-and-conversations/tracking-changes-in-a-comment#editing-history-limits)
4. `verify_events.py --self-test`의 가상 자료에는 양성, 서로 다른 문자열이나 줄끝, 다른 이슈/저장소 ID, 다른 동작, 상충 또는 누락한 본문, 현재와 같은 해시, 타인 댓글, 생성 시각만 있는 자리, 같은 이벤트의 중복을 넣는다. 가상 증거는 실자료 원장에 세지 않는다.

## 입력판과 소비판

Q3의 판독 화면에는 080 최초 확보본의 요청 부분과 증거가 확보된 개설 본문만 둔다. C1, C2, 금지조건, 명시한 판, 이미 제시한 해법을 비교한다. 버전·요구·해법이 같으면 의미 동일이며, 바이트 동일·줄끝만 차이·기타 바이트 차이를 별도로 기록한다. 두 판 중 하나가 없으면 차이는 미확인이다. 같은 작업자가 요구를 판독하고 후속 판단을 하므로 파일과 읽기 순서만 가린다. 배정문에 있던 사례·프로브 정보와 사전 지식을 가리는 실험은 아니다. 고정 요구표를 커밋한 뒤 후속 본문과 080 정답·판정에 접근한다.

각 사례는 좁음/넓음 × 참조/정확의 네 자리다. 080 최초 확보본과 새 최초 본문 결과는 같은 자리의 쌍이다. 목록 등재, 같은 구성의 C1·C2 동시 충족, 반박, 미확인, 범위 밖을 별도 기록한다. 입력 대비는 같은 범위·소비판만, 소비판 대비는 같은 입력·범위만 고정하여 계산한다. 같은 기능 ID, 별칭, 절/배포 지문을 확인하며 후보 합집합으로 두 조건을 채우지 않는다.

자연의 정확판은 작성자의 원 질문 환경이다. 교정의 정확판은 작성자 또는 원 수행자의 **후속 성공 실행**에서 연결된 환경이다. 질문판, 성공판, 참조판 및 작성자·타인·이번 재현 실행을 별도로 쓴다. 당시 최신 버전, 닫힘, 버전 없는 성공 진술은 정확판을 채우지 않는다. 필요한 소비판을 확보한 때에만 같은 목록 규칙을 추가 적용하며, 버전이 같은지는 목록 판본의 일치와 별개로 Python/배포/실행 맥락을 확인한다.

## 작업 이력

① ID·복원 규칙·음성 시험 → ② 이벤트·가린 요구 봉인 → ③ 소비판 증거·예상 봉인 → ④ 16셀과 실행·검산 → ⑤ 인계 단독. 추적 변경과 공개 결과는 이 소유 경로에 둔다. 원 이슈 전문·시간 덤프는 임시 파일로만 다루고 커밋에는 링크·대상 식별자·지문·요구 요약을 보존한다.
