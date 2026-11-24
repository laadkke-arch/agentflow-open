# AF-RES-115 연구 범위와 사전 규칙

이 묶음은 자연 요청의 대상 하나를 설명하는 링크를 부분 도면·악보에 붙일 때 발생하는 범위 오류를 비교한다. 독립 표본은 Excalidraw와 MuseScore 각 세 사건이다. 실측 편집과 저장 관계 판독을 별도로 다룬다.

## 시작점과 읽기 순서

- 계획판은 `670ecde1dab07aede6760618a7d907f0cdff185a`다. 2026-11-24 03:50 UTC 첫 조회에서 통합 브랜치는 `3839d730271a9a7f2f909be9cca5526299a4d929`였다. 첫 checkout과 작업 브랜치 부재 재조회에서 본 head `581b863dfb9f90106c2a07fb749d0cada51b0a25`로 분기했다. 계획판 뒤 3커밋은 진행표에 92행을 추가했다. 시작판의 AF-RES-115 행은 `codex-cloud`, 자체 경로, 운영 선행 AF-RES-111을 지정한다.
- 먼저 GitHub에서 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_BRIEF, RESEARCH_WORKFLOW, 진행표의 해당 행을 읽었다. 시작 checkout에서 진행표와 변경을 다시 읽고 START_HERE, CLOUD_WORKFLOW, RESEARCH_PROTOCOL, 인계 양식도 열었다. [시작판](https://github.com/laadkke-arch/agentflow-open/tree/581b863dfb9f90106c2a07fb749d0cada51b0a25)
- AF-RES-111의 운영 결과 `c49eb343ca0f74006cd3f748a1ec48b67615cedf`에서 인계를, 고정 검사판 `cf01f72e7b9837661efc3a70bb29ef924a52ad29`에서 RESULT, 36행 gold, 192행 links, verification의 72판정 및 변형층을 읽었다. 어순 대조에서 양쪽 후보·근거 유지 6/6, 동의어 완전 정합 0/6, 반대·범위·누락에서 잘못된 승계 7→5와 오지지 2→4가 이 시험의 출발점이다. [운영 인계](https://github.com/laadkke-arch/agentflow-open/blob/c49eb343ca0f74006cd3f748a1ec48b67615cedf/docs/workstreams/research/AF-RES-111/HANDOFF.md) · [검사판](https://github.com/laadkke-arch/agentflow-open/tree/cf01f72e7b9837661efc3a70bb29ef924a52ad29/docs/workstreams/research/AF-RES-111)
- `manifest.json`은 원격을 가져와 생성했다. 공통 계약은 버전 2다.

## 모집과 첨부 판정

1. GitHub의 프로젝트별 전체 issue 목록에서 `is:issue created:2022-01-01..2025-12-31 sort:created-asc`로 생성일 오름차순을 읽는다. 검색으로 단어를 거르기 전에 첫 페이지부터 순차로 열고, 각 원 이슈의 작성자 opening Markdown을 직접 읽는다. 생성 초의 동률은 GitHub issue의 전역 정수 `databaseId`로 정렬한다. 본문 확인 실패가 60위 이전에 있으면 순위 검증 결손으로 기록한다.
2. 제목과 댓글을 제외한 Markdown에서 ASCII 영숫자 경계의 `excalidraw|json|drawing` 또는 `musicxml|mxl|mscx|mscz`를 대소문자 구분 없이 검사한다. 파일명, 코드, 본문에 직접 쓴 주소도 문자열에 포함된다. 목록은 60번째 일치 초의 동률 묶음까지 확인한다. 공개 페이지에 제공되는 최종 opening body 판을 사용하고 작성 당시 미편집 원문은 별도 관측으로 둔다.
3. 해당 60건에서 변화 대상, 유지할 주변 조건, 원글 작성자가 원글에 제공한 읽을 수 있는 파일 또는 실제 직렬화 조각이 있는 첫 세 건을 취한다. 조건을 원문의 기대·대조·재현 단계에서 각각 가리킨다. 전체 파일에서도 대상이 복수일 수 있다. 후속 파일, 재게시, 화면 캡처, 소스 코드 예제, 빈 파일, 만료 링크는 상태를 나눠 적는다. 기본 적격 조건을 바꾸면 원 규칙·변화 이유·새 판을 함께 남긴다.
4. 외부 파일은 공식 공개 원경로에서 바이트와 SHA-256을 확인한다. ZIP과 내부 파일은 한 저작이다. 이슈와 파일의 사건 계보를 연결한다. 증거에는 필요한 record excerpt와 위치만 저장하고 원본 전체는 일시 캐시에 둔다.

## 보기와 판정

- A는 opening request의 필요한 실제 글과 글에 나타난 기호다. B/C는 같은 A, 같은 실제 시작 후보 집합, 같은 후보 절을 받는다. 시작점은 원문에 나타나는 표현의 범위에서 공개하며 여러 후보를 유지한다.
- B는 직렬화 거리, C는 저장 스키마의 직접 참조 또는 역참조를 사용한다. 네 레코드 상한, Unicode 코드포인트 1,600자 상한, 시작 후보 우선과 직렬화 순번으로 동률을 해소하는 정책을 양측에 적용한다. 레코드가 중간에 잘리면 슬라이스 좌표를 남기고 잘린 레코드에서 새 주장을 판독할 수 없다. 짧은 쪽 실제 길이로 양쪽을 다시 구성한다. 레코드가 같을 수 있다.
- 후보 절은 사건당 최대 3개다. 후보마다 공식 근거가 말하는 조작, 적용 범위, 보존 조건, 판과 근거 위치를 부호화한다. 판정기는 제공된 모습에서 확인한 식별자와 방향만 매칭한다. 불완전한 보존, 버전 판정 미결, 다중 대상, 근거 충돌은 보류를 야기한다.
- origin은 `author-explicit`, `author-description`, `serialized`, `parser-derived`, `research-inference`로 구별한다. `unknown`, `[]`, `predicted`, `observed`는 다른 값이다. 예상 영향을 기록할 경우 저장 관계와 구분하고, 같은 판 실제 조작 후 저장 비교가 있을 때에만 observed로 표시한다.
- gold 판독 입력에는 전체 원파일·원 요청·공식 규칙을 넣고 기준을 먼저 GitHub에 봉인한다. 비교기는 별도 프로세스에서 보기와 후보 절만 제공받는다. 같은 입력을 새 경로에서 두 번 재생하고 gold 비교는 후처리에서 실행한다.
- 합성 두 자리는 각 자연 사건의 동명 독립 요소 하나와 시작점을 유지하는 합법적 직접 참조 한 곳의 변경이다. 정의된 변형을 만들 수 없는 자리는 빈 상태와 이유를 보존한다.
