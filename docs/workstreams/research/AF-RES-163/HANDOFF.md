# HANDOFF — AF-RES-163 — PARTIAL

## 인계 상태와 고정판
- 상태: PARTIAL. 자연 모집창·기준일 상태·30일 연속 판독 미달. 보충/반례/분야 비교 및 세 필수 표·원장·자기검산을 원격에 저장. 과제의 의미 있는 부분은 발신/인지/행동을 분리하고 역할·회차를 혼동하지 않는 판정. 자연층 결측은 채우지 않음.
- 저장소 laadkke-arch/agentflow-open; branch work/research-af-res-163; owned path docs/workstreams/research/AF-RES-163/. 시작 d32c697b4345442a4c91f62b8fb0bbed19e58034; 계획 ded3420249a3d60ebbb578a8432cf262d3ffa7d7에서 4커밋 앞, 통합 변경은 dot-control.json(+190/-6)뿐. 고정 선행 53450ff704bb33a95090093f81c5762d4483d127; 158 HANDOFF PARTIAL, 상태/trace 각각 28행, 별도 통지 수신 입증 없음. 중앙 DONE 여부는 지시문과 최신 배정 diff에 따른다. dot-control 전체 JSON 대용량 조회 실패(raw 400 포함), 최신 커밋의 AF-RES-163 배정 diff 확인.
- **결과판 SHA(인계 이전 최종 결과/자기검산): 48fc58551204344983d34ab54648765f47c9ce57**. 이 HANDOFF를 포함한 마지막 커밋 SHA는 GitHub 브랜치 head 및 이 파일의 원격 고정 링크에서 확인(자기 SHA를 본문에 순환 기록할 수 없음).
- 단계별 원격 확인 커밋:
  1. 96925efa9c5903e95a38b5b0f0d5c43c458ee4f7 — SCOPE
  2. 1edcdb55de0dbebd120a9c928f1d11d2af4f6418 — 모집/기초 원전
  3. 0686ec89928189285ad69afc5894baf6fb7471ae — 주 관측
  4. 51206dc31cd8946e72154c43a0ffcd54c19c387f — 반례/조인/안내
  5. a5d83672e4a5a0c6ce2b5e9a1310e4b9bccc21d2 — 결과표/자기검산
  6. 48fc58551204344983d34ab54648765f47c9ce57 — ⑤ 열명 기준 재검산 보정, 분모 불변.
- 원격 compare 시작판→결과판: ahead 6, 파일 12개, owned path 밖 변경 0. 중앙 진행표·공통 파일 변경 없음. 대표 파일 원격 exact read 완료.

## 결과와 남은 수
- 자연층 예정 20: Debian 종료8/열림2, GNU 종료8/열림2. 순위 및 2025-12-31 상태 배정 0, 결측 20. 원 모집목록·대체 목록 접근 실패. 확장 각 다음 종료8은 최초 모집창 복원 전 판단 보류. 양성 0 관측이 아니라 분모 0. 대표 빈도 없음.
- 자료 원장 74행(열람 기록47, 실패27), 고유 열람 work28, 진입점·배경 4 제외 실질 24. 동일 티켓·답장·미러·PDF 재열람은 중복 산입하지 않음. 엄격 필수 범주: 자연 0/10 최소, 규약 6/4, 별도 반례4/4, EGU 2/2(ED 통지 인지 불명), 시민 1/2 원 제출자 내용 연결+1 부분 대조. 즉 자연 최소10·시민 완전1 남음; 전체 20자리 및 확장 판단 별도. 자연층 완결 관찰창 0. 실제 열람 단위 일부 묶음·확인 UTC 날짜 정밀도는 원장 한계.
- 보충 9티켓 중 8티켓 발신 로그, 1(D1035733) 종료 로그 미판독. 8 원 제출자 표적 +8 closer ack. 원 제출자 인지/행동 승인 0, 미확인 8. 원 제출자 후속 행동 2건은 notice 내용 조인 없음. 반례/후속 5티켓의 추가 통지·확인 19행(11 원 제출자,8 closer). 전체 선택 36행(발신/생성 35, 표적 미확인1), 원 제출자 발신 19, 같은 통지 내용 인지1/대응1(보강 D1020248 첫 통지에 #97 및 reopen), 나머지18 미확인; 수신함 도착 전건 미확인. 16 closer 행 중 명시 closer 내용 2를 원 제출자 인지로 계수하지 않음. 전체 창/반복 통지 전수 아님.
- D1034732 다른 참여자가 자동 종료 뒤 재개; D1095935와 D990667 closer 반응은 원 제출자 반응 아님. D1020248의 두 번째 closure에 첫 답을 결합하면 시간 역전. EGU 두 AR PDF 본문은 reviewer 내용 인지에 직접 증거, ED 이메일 경로는 없음. Medway C3 의회 응답과 원 청원 대표의 검토 요청; North Herts C2는 포털 게시됐으나 email 미발송 및 다른 수신 역할. 1개 시민 적합 사례 추가 필요.
- SELF_CHECK: 동일 작업자 JS 구조 검사. source_id 중복 0, 헤더 기반 참조 누락0, CSV 열수 불일치0. 처음 위치 열을 source_id로 검사한 오류는 ⑤ 보정 커밋으로 수정, 판정/분모 불변. 독립 검토 및 checkout/실행/빌드/CI는 미실시. 공개 아카이브 전수 검증과 동치 아님.

## 공개 재개 입력 및 첫 행동
1. 이 결과판의 SCOPE.md, frame.csv 자연 20자리, RECRUITMENT.md 실패 위치부터 읽는다. 원 Debian 목록 https://bugs.debian.org/debian-policy 와 GNU https://debbugs.gnu.org/ 를 직접 다시 열고, 발행자 공개 CGI 패키지 목록/아카이브를 사용해 생성일·티켓 번호 순으로 전체 반환 및 누락을 기록한다. 후보 URL(직접 확인 필요) Debian https://bugs.debian.org/cgi-bin/pkgreport.cgi?pkg=debian-policy;archive=both , GNU https://debbugs.gnu.org/cgi/pkgreport.cgi?pkg=emacs;archive=both . 막히면 발행자 월별 공개 보관본 및 Debian UDD https://udd.debian.org/ 에서 원 순위 재현 가능성 확인. 검색 엔진 순위는 자연 모집에 쓰지 않는다.
2. 최초 본문 필터와 2025-12-31 당시 상태 복원 후 서비스별 종료 8/열림 2를 배정. 종료 ±30d, 열림 생성 +30d. 원 제출자가 인용한 통지 2건 미만일 때에만 다음 종료8까지 확장. 원본 mbox 및 public message permalink의 역할·통지 ID·시각·인용 위치 확인. 다른 회차/다른 수신자·침묵을 거절. 원 모집 원장 빈자리는 보충층으로 채우지 않는다.
3. 시민 두 번째 원 청원자 보완·회신/의회 통보 문서를 같은 사건으로 직접 확인. 학술 E1/E2에서 정확히 ED 통지에 대한 저자의 인용/수신 진술이 있는지 별도 조사. 실제 사용자나 메일 발송은 불필요.
4. 별도 실행 검사가 필요한 경우 Codex 또는 독립 검사자에게 넘길 입력(미실행): 고정 repo/branch/commit 48fc58551204344983d34ab54648765f47c9ce57, owned path 원장. 공개 URL 요청은 `curl -L --fail --max-time 60 'https://bugs.debian.org/cgi-bin/pkgreport.cgi?pkg=debian-policy;archive=both'`와 `curl -L --fail --max-time 60 'https://debbugs.gnu.org/cgi/pkgreport.cgi?pkg=emacs;archive=both'`를 각각 1회부터 시험; HTTP 상태, 실제 반환, content type, UTC, 판독 범위 기록, 접근 제한을 우회하지 않음. 출력이 정상 원목록이면 날짜 필터/정렬/기준일 상태를 별도 원장으로 재현; 오류이면 실패 원장. 기존 작업자 권한/공통 계약 확인 후 `git diff --name-only d32c697b4345442a4c91f62b8fb0bbed19e58034 48fc58551204344983d34ab54648765f47c9ce57`, `git diff --check d32c697b4345442a4c91f62b8fb0bbed19e58034 48fc58551204344983d34ab54648765f47c9ce57`, Python csv/json parser로 sources/notifications/joins/advice/tickets ID 연결 및 A/R 역할 필터 재집계. 기대: owned path 밖 0, 참조누락0, A/R 승인1(보강), 원래 자연 20 결측 유지. 실제 환경에서 필요 시 `python scripts/check.py --require-git`, `python scripts/cloud_check.py --environment codex-cloud --fetch-contract` (환경 일치 시) 및 exit code/영수증. 웹 조사에서 manifest start/check나 CI 실행 확인하지 않았으므로 검사가 통과했다고 기록하지 않는다.
5. 새로운 자료로 결론이 바뀌면 기존판 유지하고 보정 커밋에 분모/판정 이유를 기록. 이번 단계는 제품 구현을 권하지 않는다.

색인 제안: **상태 통지의 발신과 원 제출자 인지·대응 분리 — Debian BTS·EGU·시민 절차 — 역할/회차 반례, 자연 모집 미복원(PARTIAL).**

| 불일치·약점 | 영향을 받는 판단 | 다음 조사와 자료 | 결론을 뒤집을 관측 |
|---|---|---|---|
| 두 모집 목록 접근 실패; Debian 일부 검색 후보만, GNU 자연 원전 0 | 두 서비스의 대표 발송·인지·행동 빈도와 독립 운영 비교 보류 | 발행자 전체 티켓 목록/공개 mbox, 상태 이력, 기준일 정렬 및 8+2 자리 복원 | 생성 순위와 기준일 상태가 원장으로 재현되고 각 30일 창을 판독 |
| 공개 발신·답장과 수신함 도달이 다름; 반복 종료·다른 수신인·무응답의 경쟁 설명 | 원 제출자에게 전달/읽힘/행동했다는 일반화 금지; D1020248 내용 인지만 승인 | 원 통지 식별자·표적 역할·동일 원 제출자 직접 인용 또는 수신 진술, 반복 통지별 대조 | 동일 통지의 당사자 인용/확인 또는 명시 수신 증거; 이전 통지 인용이면 재귀속 |
| 시민 North Herts는 다른 수신인, EGU AR은 리뷰 내용 중심; 자료 원장 접근별 기록 일부 묶음 | 분야 이전의 통지 경로·수신 보장, 시민 2개 완결 사례와 엄격 범주 하한 보류 | 두 번째 시의회 원 청원자 보완/회신 원문, EGU ED 연결, 원장 접근 재기록 | 같은 통지와 원 제출자의 구체 응답을 두 번째 시민 사건에서 독립 판독 |
