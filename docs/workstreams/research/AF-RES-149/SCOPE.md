# AF-RES-149#1 — 범위와 비교 동결 (PARTIAL 가능)

## 시작 / 관측 전
- 시작: 2026-11-24 UTC / 25 KST, 세션 시작 시각 제공값 15:44 UTC. 분 단위 실제 열람별 시각은 미계측. 계획 SHA ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19; 최신 통합 브랜치 실제 시작 SHA f140af3179b7d9271710778104ccee5b4812e2ef. 작업 브랜치 신규 생성. 이 SHA의 AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, docs/product/RESEARCH_BRIEF.md를 읽음. dot-control.json은 contents API에서 빈 본문이 반환되어 blob ab648c6fe5720410e04b9ea43228e8b1226f51f0으로 직접 읽음: RUNNING, attempt 1, worker_kind web-pro, 소유 경로 일치, source_commit/result_commit null, depends_on 002/146.
- 선행 인계 002@62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1, 146@9bf267b71a0000aae5f098e82eab3f84c0dd7714 직접 열람. 002는 목적/부품/전이 탐색의 후단, 146은 고정 후보 12장×4 요구 직접 0/48. 이번에는 후보 모집 입구와 발견/재발견만. 선행 표본은 산입하지 않는다. 영구 동일성, 보존 등급, 장기 재방문, 제품 구현 제외.
- 실제 도구: 웹 원문 조회, GitHub 연결. shell git 명령 시도는 TransportError; checkout/session manifest 실행 및 공통 CLI 검사는 아직 미실시. 지정 경로 밖 변경 금지.

## 탐색 단계 (동결 전에 읽은 출처; 비교 분모 제외)
1. 직접 저자 발표: https://news.ycombinator.com/showhn.html (직접 만든 시험 가능 작품, shownew와 점수 통과 show 구별, 작은 개선 제외); https://news.hada.io/topic?id=4828 (2021-08-17, 한국어, Show HN 참고 명시; 직접 만든 것/초기 작품, 다중 채널 전파의 점수 조건). 반대 가설: 다른 언어라도 같은 진입 규칙이라 동일한 공급자를 반복한다.
2. 편집 제보: https://forest.watch.impress.co.jp/info/sakusya/sakusya3.html (일본어, 무료 시험 가능 정식 공개판, 이메일 자천→편집 기사→별도 허가 후 라이브러리; 미선정 개별 회신 없음). https://forest.watch.impress.co.jp/info/about/about.html (라이브러리와 기사, 월별 재심). 반대: 편집자가 이미 유명한 것만 반복한다.
3. 배포 편입: https://f-droid.org/en/docs/Inclusion_Policy/ 및 https://f-droid.org/en/docs/Submitting_to_F-Droid_Quick_Start_Guide/ (공개 소스·FOSS 도구/의존·빌드 검증·저자 의사·메타데이터 MR). 반대: 이 관문이 설계 적격성과 무관하여 폐쇄형 웹기능을 체계적으로 배제.
4. 커뮤니티/전문 분야 제보: https://linuxfr.org/aide (프랑스어, journaux 사후/depêches 사전 중재), https://this-week-in-rust.org/blog/2025/10/01/this-week-in-rust-619/ (영어, 태그/PR 제보, Project/Tooling Updates 및 별도 crate self-suggestion). 반대: 전문 분야 색인이 언어/도메인 필터를 추가할 뿐.
5. 타 분야 원리: https://lsa.umich.edu/herbarium/collections/contributing-specimens-to-the-collections.html (범위/표본 상태/라벨/허가라는 문턱); https://guides.loc.gov/zines/donate (기증·웹 후보 지명). 물리적 표본과 소프트웨어 링크의 독립 복제성은 다름. 배포 편입을 '입수와 점검을 별개 사건으로 보존'하는 모형의 시험으로 선택. 새 제안: 의존성 소비자/플러그인 통합 측의 호환성 실패 이슈에서 역으로 작은 기능의 제작자 원문을 따라가는 경로; 이번 비교에는 넣지 않음.
- 이미 보인 자료(비교 외): Impress 2025-11 월간 업데이트 목록, F-Droid 뉴스 페이지의 해당 주 제목, 2026-04-03 F-Droid 신규 목록 일부, GN Show와 LinuxFr 최신 목록, TWIR 619(10/01). 비교할 섹션의 첫 여섯은 아직 읽지 않음. 요구를 찾는 과정에서 본 검색 반환 후보 Dynos, FeedStash 등은 비교에서 별도 검색하지 않음.
- HN Algolia 날짜 API 시험(2026-01-01) 접근 실패; HN front(2025-10-02) 429, Product Hunt 일간(2025-10-02) 접근 실패, Codeberg 탐색 robots 차단. 날짜 고정 목록이 확인된 대안으로 바꿈. 접근 실패와 결과 없음 구별. 원래 희망한 직접 발표 경로의 날짜 원장 미확보라는 모집 편향은 본 비교에 남음. 한국/프랑스어는 탐색/반례 층; 본 비교 언어는 일본어·영어. 영어 편중을 개선한 것으로 주장하지 않음.

## 비교 동결 (이 커밋 이후의 표본 열람만 주 비교)
공개 설계 요구, 각각 issue 본문: 
- R1 전체: https://github.com/blinkospace/blinko/issues/898 (2025-09-22): 모바일에서 인터넷 없이 단순 메모 조회/작성, 연결 시 동기화. 직접=세 동작 모두 제작자 문서에 명시. 부분=오프라인 읽기/쓰기/동기 중 하나 이상 구체적.
- R2 부품: https://github.com/plankanban/planka/issues/670 (2024-04-04): 목록, 가능하면 보드의 JSON/CSV 내보내기. 직접=보드/목록 구조화 내보내기 동작 확인; 부분=다른 종류의 기록/리스트를 구조화 내보내기하는 구체적 기제.
- R3 타 분야 전이: https://github.com/tallbl0nde/NX-Activity-Log/issues/21 (2020-02-19): 게임 활동 로그 전체를 CSV/XML/JSON 파일이나 로컬 HTTP 서버로 꺼내 외부 플러그인이 쓸 수 있도록. 직접=해당 활동 로그의 외부 이용 구조, 부분/전이=다른 분야에서 데이터/활동 기록을 외부 기계 판독 소비자에게 전달하는 동작과 깨지는 전제를 확인. 단순 파일 저장·네트워크 접속은 불충분.
- 시간창 W1 2025-11-10~16, W2 2025-11-17~23 (각 출처 표시 현지 발행일, 시차 미확인). 동일 두 창, 앵커 수요일 Rust 12/19, 목요일 Japan/F-Droid 13/20. A=일본 窓の杜 해당 목요일 다이제스트 뉴스 첫 6개의 소프트웨어 행(광고/중복/무링크 포함; 쉬운 공개 목록 기준). B=This Week in Rust 해당 수요일 Project/Tooling Updates 첫 6개(커뮤니티 전문 제보; PR인지 개별 확인). C=F-Droid 해당 목요일 TWIF Newly Added Apps 첫 6개(편입 기반, 타 분야 원리). 새 앱 부족은 빈 예정 자리로 표시, 실제 모집 자리로 세지 않음. 주소 찾기 위해 날짜/목록 제목만 검색 가능, 결과 대체 금지. 특정 섹션이 없으면 missing; 대체일 금지.
- 각 셀 6자리, 각 자리 원문 후보 1개 열람 시도 최대(36회 전체), 무링크/차단/중복 그대로. 모집 목록 1개 접근 + 필요 링크 확인은 별도 호출. 중간 링크가 저자 본문이 아니면 실제 후보 검증 실패로 남기고 주 비교에서 추가 개봉하지 않음. 추가 추적은 별도 탐색/반례로 기록. 배치 호출의 대기/개별 벽시계 미계측이면 미확인. 표시 순서와 원게시 시점 분리. 현재 점수/별은 당시 값으로 사용하지 않음.
- 원문 본문에서 확인된 동작으로만 적격(직접/조건부 부분/전이 별도), 제목·설명 요약/도달 실패=미판정, 분모에 남김. 구체적 모순=부적격. 명시가 없으면 미확인이지 없다는 증거 아님. 같은 대상의 원문 URL·명시적 교차 링크만 하한에서 합치고 불확실 중복 상한 분리. 추가 적격 기준 A의 관측 집합, B/C 각각 A 차집합 및 전경로 단독 기여 별도. 반예산 첫 3자리, 전량 첫 6자리; 실제 성공 열람 수와 시도 수 구별. 적격 고유 대상/자리, 추가 적격/자리, 새 기제/100 성공 열람 (0이면 산출 불가). 본문 판정에 노출 지표 쓰지 않음; 정식 독립 블라인드가 아니라 같은 작업자의 지표 제외 판정. 언어/출처 제거는 같은 관측 집합에서 재계산. 전세계 분모·재현율 미확인.
- 운영 규칙과 실측은 분리. 관측 실패도 성공 증거로 올리지 않는다.
