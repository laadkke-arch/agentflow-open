# AF-RES-161 — 사전 범위·선정·판정 (①)
- 계획 통합판 ded3420249a3d60ebbb578a8432cf262d3ffa7d7 → 실제 시작 d32c697b4345442a4c91f62b8fb0bbed19e58034. GitHub compare: ahead 4, behind 0, 변경 파일은 docs/automation/dot-control.json 하나. 작업 브랜치가 없음을 확인하고 실제 시작 SHA에서 생성.
- AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md 읽음. dot-control.json 일반 파일/원문 조회는 빈 본문/크기 실패, 동일 blob 5f3dc0c9c7fcefdfabecc46d4f405fdf69eab596 직접 조회로 AF-RES-161 RUNNING 및 depends_on AF-RES-150 DONE, result_commit ff2c1fc8786ba70a1432f1089f8f81288e43a61d 확인. 선행 HANDOFF, RESULT, cases/sources 원장(관련 N08)과 제품 브리프 ded3420, REVIEW-39 a61743ae 참조. 150의 구성 재생 반복 금지.
- 소유 경로만 작성, 공통 파일·통합 브랜치·외부 편집 원장 변경 금지. 실행/대량판 비교는 Codex 인계. UTC 확인일은 이 세션 기준 2026-11-24 (일자 정밀도; KST 11-25).
## 모집 사전 규칙
교정 C1 = #6371의 작품 OL14863262W; C2 = 거래 42049802. 두 ID를 명시한 거래 구성원/판의 편집 요약 및 시간순이 맞을 때만 동일 사건 지지. 불일치 키가 확인되면 반박, 하나라도 결측이면 미확인. 보고자 서술은 원판 직접 관측과 분리.
자연 OL: GitHub issue search repo:internetarchive/openlibrary is:issue created:2020-01-01..2025-12-31 merge undo 및 merge revert 두 검색(본문/제목 기본 검색, 동일 보고 ID 중복 제거). created 오름차순, 동률 numeric issue ID. 검색 결과 전체(가능한 모든 페이지)를 합친 뒤 앞 8자리; 시간순/필터 확인 불가시 원순위 미확인. 목록 검색 자체는 원전 산입하지 않음.
자연 WD: Wikimedia Phabricator 공개 검색(project Wikidata, 문구 merge undo / merge revert, 생성일 2020-01-01..2025-12-31), 생성일 오름차순, 동률 numeric T ID. 기본 검색이 생성일 정렬/범위를 못 제공하면 원 목록 복원 실패로 기록하고 Wikidata 공개 요청/보관 페이지를 대체 진입점으로 시도; 페이지 생성일을 개별 보고일로 대체하지 않음. 두 서비스 모두 첫 8에서 연속 판 열람 가능한 사건 2 미만일 때만 다음 8, 총 16까지. 순위 복원되지 않은 후보는 보충이며 빈 자리 대체 금지. 관측 없이 비율 금지.
## 관측 기준
각 사건의 병합 전/병합/중간 독립 편집/복구판을 객체 ID·revision·행위 역할·UTC로 구별. 독립 편집은 별도 편집 근거가 있어야 하며 중간판 없음과 접근 실패를 구별. 대상/무관/안정 필드의 실제 값 원문 위치 없이 보존·손실 판정 금지. 전체 복원·선택 취소·사후 수동 재작성·미확인 각각 구별. Q5는 고정 서지/연결된 작품과 실제 이전 ID의 대상/판/절. 단순 URL 200/redirect는 동치 아님. Q7의 선택적 복원/원문+정정판은 제안일 수 있으며 실제 동작과 섞지 않음.
원전 목표 22 = 거래/이력 8, 보고/인용 6, 지침/변경결정 4, 전거 2, 지리명 2. 동일 저작 중복 금지; 검색 요약/차단/메타데이터/내부 선행 0산입. 분모는 16 자연 최초 자리 (+조건부 16 확장), 교정 사건 후보 2, 필드별 실제 판독 및 결측. 결측률 외 대표 빈도 금지. 반례는 전부 되돌려도 손실 없는 경우 및 부분 복구 후 오류가 남는 경우 각각 검색해 별도 층으로 보존.
