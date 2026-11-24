# AF-RES-253 범위와 사전 판정

## 착수와 입력

2026-11-24 UTC, Codex Cloud 셸. 저장소 `laadkke-arch/agentflow-open`, 작업 브랜치 `work/research-af-res-253`, 소유 경로 `docs/workstreams/research/AF-RES-253/`. GitHub 통합 head를 재조회하고 `d1353701530ffd4c68587276c15d988d2cc92972`에서 브랜치를 만들었다. 이 배정의 계획판 `7369707441e2eb70e84004ca6cb3bfeefc8b4061`에는 AF-RES-253 행이 없었다. 첫 조회 `80b4df0af9ae814e2f5d70fa24ffdeeb64f9308a`에서 착수판까지 이동했으며 두 판의 이 과제와 직계 의존 과제 행은 같다. 첫 조회의 Contents 응답 본문이 비어 Git으로 받은 blob `7a0b6490b055704cd2572c9d3a37a6f81b11def6`을 직접 읽었다. 착수판의 진행표 blob은 `41cefbc22f8d86795d0aff7204c9cbefb69577fa`다. AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, CLOUD_WORKFLOW, START_HERE, 제품 브리프·프로토콜·로드맵, 협업 규칙·인계 양식을 확인했다.

직계 의존은 AF-RES-235 하나다. 중앙 DONE 및 인계 자체 PARTIAL의 근거 SHA `5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126`에서 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/HANDOFF.md), [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/RESULT.md), [citations.csv](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/citations.csv), [timeline.csv](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/timeline.csv), [consumer.csv](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/consumer.csv)를 읽었다. 235의 당시 본문·소비자 설정은 사전 해석이고 런타임 분모는 0이다. 238–242의 입력·출력과 241의 교육 서비스 UI, 실제 사용자의 감사 증거, 보조기술 발화, 개별 사이트 적합성 전체, 235에서 열어 둔 정오표의 최초 적용일은 이번 표본 밖이다.

`python -m workbench.session start af-res-253 --allow docs/workstreams/research/AF-RES-253/ --dependency work/research-af-res-235=5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126 --output docs/workstreams/research/AF-RES-253/session.json --fetch`를 실행했다. [session.json](session.json)과 [종료 코드](receipts/session/start.exit), [stdout](receipts/session/start.stdout), [stderr](receipts/session/start.stderr)를 보존했다.

## 표집과 확인 단위

- 날짜판 3개 × 각 두 fragment = 6행. [inputs.json](inputs.json)의 URL 그대로 요청한다. 2.0/2.1 Parsing 원 요구, 2.2 Parsing 제거 표지, 세 판의 1.1.1 존속을 비교한다. 원 요청과 최종 응답/형식/바이트를 기록하고, HTML 파서의 `id` 및 `name` 일치 집합과 Chromium `:target`, 화면 위치, 가까운 제목·절을 각각 확인한다.
- axe 두 판 × [235와 같은 네 fixture](fixtures/) × 세 옵션 = 24개 주호출. 같은 Chromium에서 매 호출에 새 문서를 쓰고 `axe.run(document, options)`의 원결과 네 배열을 보관한다. 대상 네 ID의 분류·태그·노드 target과 그 밖의 규칙을 구분한다. payload에서 빠진 규칙, `inapplicable`, 배열 내 노드 0개, 실패로 미관측을 별개로 기록한다. axe의 기본 `resultTypes`를 변경하지 않는다.
- 추가 판별은 ARIA 원문, 두 span 순서만 반전, 첫 span의 ID만 유일하게 변경의 세 경우다. DOM 첫 매치, 가능한 경우 Chromium CDP의 AX 이름·참조, axe 네 배열을 대조한다. 주표 분모에 넣지 않는다.
- RFC 2119·8174의 RFC Editor 공식 HTML에서 각각 §1, §2 fragment 후보를 같은 파서로 확인한다. RFC 원문 헤더의 Updates와 별도 원발행 관계(BCP 14 인덱스 등), 각 절의 명제를 구분한다.
- 대표 재생은 독립 임시 폴더와 새 프로필에서 6개 앵커, 8개 기본 모드 호출을 다시 실행한다. 원 dump의 지문/원 차이 및 환경·시간에 종속하는 필드를 명시한 정규화를 비교한다. 브라우저 이름 계산은 해당 엔진 관측으로 범위를 제한한다.
- 자료 하한은 W3C 날짜판 3개, 정오·원결정 3개, 두 axe 판 규칙·별도 시험/릴리스 결정 8개, 브라우저/AX 명세 및 axe API 3개, RFC 본문과 원발행 관계 3개. 한 저작의 번역·미러·링크 별칭·실패는 산입하지 않는다. 확인 시각, 근거 위치와 한계, 고유 저작·계보·사건을 원장에서 구분한다.

## 사전 예측과 반증 조건

| 질문 | AF-RES-235를 바탕으로 고정한 예측 | 반증 조건 |
|---|---|---|
| Q1–Q2 | 3 HTTP 본문과 6 fragment에 대응하는 절을 볼 수 있다. 판마다 유일한 요소이며 2.0은 레거시 `a[name]`일 가능성도 있다. 2.2의 Parsing에는 제거 표지만 남는다. | 404/챌린지/비HTML, 일치 0/복수, 제목이 다른 절, 파서와 브라우저가 다른 선택, 요구 본문 재등장 |
| Q3–Q4 | 4.7.2의 plain `duplicate-id`, active `duplicate-id-active`, aria `duplicate-id-aria`가 해당 fixture에서 violation이다. 4.8.0 generic/active는 default·wcag2a에서 미보고, explicit enabled 시 해당 fixture에서 violation이다. 4.8.0 ARIA는 incomplete와 `wcag412`를 예상한다. 235가 지정하지 않은 부수 규칙·노드는 열린 값이다. | 모드별 결과 누락/이동·교차 규칙, `reviewOnFail`인데 violation, SHA/패키지 provenance 또는 런타임 판 불일치 |
| Q4 대조 | 두 image-alt 노드 중 alt 생략 이미지가 violation, 텍스트 alt 입력이 개별 check를 통과할 수 있다. 원 rule-level 버킷에 pass 노드까지 배열로 나타나는지 별도 검증한다. 두 판 모두 `wcag111`. | 생략 속성인데 통과·다른 결과, mixed 결과 집계 또는 rule tag가 예상과 다름 |
| Q5 | 두 span 순서에 따라 IDREF 대상과 AX 이름이 바뀔 수 있고 충돌 보고는 두 순서에서 같다. 첫 span ID만 변경한 통제는 Intended title을 참조하며 ARIA 중복 보고가 사라진다. | 실제 이름 선택 불변, AX 소스와 DOM 첫 매치 불일치, 순서만으로 분류 변경, 유일해도 충돌 보고 |
| Q6 | RFC 둘의 section fragment가 각각 도착해도 동일 요구의 증거는 아니다. 8174의 Updates 및 대문자 적용 범위를 원문으로 따로 찾는다. | 한 문서에 섹션 앵커 없음, 실제 Updates 관계가 반대이거나 원문 의미가 예상과 다름 |
| Q7 | 고정 입력의 정규화 주결과와 별도 폴더 재생이 일치할 것으로 예상한다. 원 dump에서 반복 시 변하는 값은 차이로 기록한다. | 바이트·도착 절·결과·selector·모드/노드의 실질 차이 또는 재생 누락 |

노출 순서: 배정·운영 규칙·235 고정 입력 → 이 문서·fixture·session 커밋 → 직접 원자료·원장 → 주관측 → 별도 반전·재생 → 최종 자체 점검과 인계.
