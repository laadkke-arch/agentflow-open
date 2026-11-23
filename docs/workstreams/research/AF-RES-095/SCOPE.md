# AF-RES-095 · 사전 범위

- 연구 질문 Q1–Q7은 원 요구와 입력, 고정 실행 판, writer·템플릿·TeX 연결, 두 선과 셀, 검출 교정과 반례, 독자별 반환, CSS·Calc 대조다. 제품 목적은 사용자의 구조와 목적에 도움이 되는 부품이나 원리를 근거 링크로 찾는 것이다.
- 계획 기준은 `e2a80afec762b10ee7979136c6332473c70905bb`다. 배정 직후 GitHub에서 확인한 통합 브랜치와 실제 작업 브랜치 시작점은 `f72073277e6be643302a33f204d70baeb2c749a4`다. 작업 경로는 `docs/workstreams/research/AF-RES-095/`다. [시작 커밋](https://github.com/laadkke-arch/agentflow-open/commit/f72073277e6be643302a33f204d70baeb2c749a4)
- 통합판의 AGENTS·STATE·Dot 규칙·연구 규칙·AF-RES-095 배정 항목을 읽었다. 지정 [AF-RES-092 인계](https://github.com/laadkke-arch/agentflow-open/blob/e0d7ecda64bab2bd5d5779a9fb2a18d39a83bcdf/docs/workstreams/research/AF-RES-092/HANDOFF.md)와 [결과](https://github.com/laadkke-arch/agentflow-open/blob/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/RESULT.md)에서 P2를 고정했다. 현행 의존 브랜치와 계약 오류는 [인수 기록](evidence/intake/contract.md)에 있다.
- 비교 표본은 [원 질문](https://stackoverflow.com/revisions/78311072/1)의 추출 파일, 092 사전 무인수 재정의본, [최초 공개 답](https://stackoverflow.com/revisions/78314393/1)의 두 필수 인수 재정의본이다. 각 파일의 원 표 하나 조건에 더해, 고유 제목과 실제 헤더를 가진 동일한 두 번째 Markdown 표를 붙인다. 부착한 표에는 로컬 재정의가 없다. 두 독립 작업 디렉터리씩 총 12자리다. [입력 및 사전 판정](fixtures/plan.json)
- 원 요구는 위·아래 수평선 제거다. 셀의 내용·순서와 문서 안의 다른 표의 상태는 연구 판정 조건으로 둔다. 두 번째 표의 헤더 구분선은 내부 선 양성 대조이며 사전 예상 보존 대상이다. 텍스트는 문자열·행·열 순으로, 지오메트리는 페이지 좌측 위 기준 pt 좌표로 대조한다. 바이트 등가와 실측 등가를 따로 검사한다.
- 사전 기전 가설은 booktabs 정의를 본문 앞에서 재정의하면 뒤에 오는 표에도 적용되고, 원 writer가 규칙명 뒤에 토큰을 썼으면 무인수의 후속 토큰 처리와 두 인수의 소모가 다를 수 있다는 것이다. 두 매크로가 현재 입력에서 같은 PDF를 만들 가능성, 규칙 뒤 토큰 형식이 다른 TeX 표에서 정상 내용 소실·엔진 실패·간격 변경이 생길 가능성, 실제 헤더·두 번째 표에서만 드러나는 차이를 각각 본다. 한 표 격리는 별도 반례로 시험한다.
- Quarto 공식 Linux amd64 v1.4.553과 그 Pandoc을 쓴다. 092의 독립 Pandoc 3.1.11은 비교용 소스 판이다. 입력의 article을 유지하고 모든 렌더에 같은 keep-tex와 설치 차단 옵션을 준다. 동일한 고정 OS·TeX·PDF 판독기를 쓴다.
- 원본 양성 및 교정의 벡터·래스터 두 판독이 안정적으로 일치해야 성공률을 낸다. 0분모는 산출 불가로 적는다. 엔진 실패, 경고, PDF 미생성, 판독 불능, 셀 손실을 독립 기록한다. PDF가 있어도 엔진 오류가 있으면 성공으로 세지 않는다.
- 외부 1차 직접 열람 24건 이상을 분야별로 대조한다. 질문/답은 두 자료·같은 사건이며 같은 저작 원문 미러·반복 접근, 검색 요약, 092 기록 및 연구 입력·출력은 최소량에서 제외한다. 사례·교정·다른 버전은 12자리 분모 밖이다. 092의 탐색 쌍이나 과거 질문자 성공률은 재채점 대상에서 제외한다.
- 원 질문자의 프로그램 판·명령·해법 적용 후 PDF는 미확인이다. 스크린샷은 [원 주소](https://i.sstatic.net/V5Tdz.png)를 시도했으나 셸 CONNECT 403, 웹 열람기에서 시각 자료를 확인하지 못했다. 실제 PNG를 받아 위·아래 선·기준 픽셀을 읽으면 원래 출력에 대한 판정을 보강할 수 있다. 원문의 한 표/모든 표 의도는 당시 질문에 나오지 않는다.
