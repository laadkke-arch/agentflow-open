# AF-RES-184 SCOPE — 사전 등록

- 계획판 `128f673685ec804c526a38e3f89d4d8a43fcd299` → 시작 통합판 `6fa67328360b02bc7e7270d4ad3300bfe0f286bd` (2026-11-24T19:16:14Z, +3/−0, compare: dot-control.json +208행만 변경). AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW 및 RESEARCH_BRIEF 읽음. 진행표는 1.4MB라 contents file 응답이 비었으나 GitHub API contents URL로 원문을 확보하여 184 RUNNING, depends_on 176, owned_path와 brief 일치 확인. 176 중앙 DONE / 고정 HANDOFF a347a373cdd46910f2cd2cf53419849ba48ee03a 자체 PARTIAL: 55/55 EARL-표시 합치, 과거 엄격 독립 실행 확인 없음. 새 JSON-LD 실행·검산 제외.
- INDEX.md(2026-11-19)는 환경 설정 색인뿐, 184/176 또는 재현빌드 항목 없음. 관련 중복은 직접 의존 176의 '표시 ≠ 실행' 원칙이며 EARL 표본은 재사용하지 않음. 색인은 편집하지 않음.
- 새 작업 브랜치를 위 시작판에서 생성. 본 작업 경로 외 변경 금지. 제품 DB/수집기/검색 형식 미선택. 공개 문서 판독만, 새 빌드 없음.

## 모집
예정 고정 기준시각 **2026-11-24T00:00:00Z** (UTC, 작업 전 날짜; 결과를 보기 전 정한 요청 컷오프). snapshot.debian.org 문서에 따르면 정확 시각이 없으면 그 이전 최근 import로 해석되므로 실제 resolved import timestamp와 Release/Packages/Sources digest가 확인돼야 고정 완료. 아직 미확인. `main` trixie, amd64/arm64 각 hello, sed, grep, gzip 순서, 8자리. 각 소스의 동명 기본 바이너리만 주표본; 동일 source의 debug/doc/다른 binary는 비교 밖. 없는 항목은 공석, 조회 실패는 미확인. 소스 버전과 바이너리 버전(+bN 포함) 분리, epoch 포함 원문 보존; Architecture: all은 단일 산출 키이며 두 arch에 노출되어도 두 빌드로 세지 않음. 명부에서 원래 버전/바이너리 먼저 확인, 이후 rebuild 레코드 조인. 라이브 패키지 페이지는 fallback 후보이지 snapshot 고정 증거 아님.
- 조회 순서: snapshot import/Release/Packages/Sources → archive binary hash/buildinfo/buildd → 해당 rebuilder API/raw log/attestation → 대시보드/통계/코드 → 인접 실패/재시도 최대 4개(동일 명부 확인 후) → Arch 표시 구조(별개) → 관측소·숙련도 원보고.
- 자료 최소 22: 배포 6, 별도 rebuild 실행 6, API/화면 규칙 4, 반례 2, 분야 비교 4. 하나의 실행 ID의 웹/JSON/log 미러는 한 실행 자료; 원전 불가/미리보기 제외. 자료 수, 사건 수, 독립 관측 수 별도.
- 초기 진입점 trixie overview/amd64/arm64, snapshot root, buildinfos root, Debian wiki, Arch wiki/dashboard 열람 시도: trixie arch 페이지는 JS Loading stats만, snapshot monthly URL 접근 실패, buildinfos disabled, Debian wiki 403, Arch wiki 접근차단. 결과값 아직 채택하지 않음. 실패는 원장으로 보존.

## 판정
키 K=(archive/suite/resolved import, source name/version, binary name/version, artifact arch, file SHA256). 원 빌드는 buildinfo 서명/날짜/환경/산출물 및 archive hash 교차 확인; .deb 존재만으로 실행 로그 확인 아님. 재빌드 사건 R=(운영 조직, instance namespace, job/attempt ID, 실제 시간, worker, 입력·산출 지문); 동일 작업 ID 다른 화면은 동일 관측, 시도 ID가 다른 경우 별도 실행 후보, worker 차이는 조직 독립성 아님. 입력·산출물 동일성 확인 전에 hash 불일치 판정 금지. SUCCESS 상태와 직접 두 해시 일치 분리; BAD/FAILED/queued/expired/unknown 분리. 미확인은 실패 아님. 적어도 2개 패키지에 실제 원·재빌드 해시 연결 필요; 미달 PARTIAL. 미상 상한을 URL 수로 추정하지 않음. 독립 성공률 계산 금지. 연구 주체별 claim 최소 증거 및 반례 기록. 본 세션은 GitHub API 편집, 실제 checkout/workbench 실행은 별도 인계.
