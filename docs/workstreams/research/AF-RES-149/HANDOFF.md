# AF-RES-149#1 HANDOFF — 최종 보완 재시도 #2 (S2)

- task_id: AF-RES-149 / 원 attempt 1 이어서, 보완 재시도 #2
- status: PARTIAL (신규 비교·역사 사건 확인·검산 수행; 원 엄격 완료 기준 미충족)
- branch: work/research-af-res-149
- owned_path: docs/workstreams/research/AF-RES-149/
- resumed_from: f06a999fc72112bd7d8a9ae9e12c4d61cab6d175
- S2 protocol_commit: b8b5d8e8a3ce8b762c6b33ed8f555b2276674a6f
- S2 result_commit: ebfd3c4c7d81774ac7d5ff322b4ba683f0e1d062
- S2 self_check_commit / pre_handoff: 2ae91fc86466e05f621f2b0ff569f5cd5292b4d3
- handoff_commit: 마지막 단독 HANDOFF 커밋(브랜치 HEAD로 확인)
- 원 결과·S1 및 모든 기존 원장 동결; 통합 브랜치/중앙 진행표/소유 경로 밖 변경 없음.

## 이번 실행 결과

[RESULT](supplement2/RESULT.md)와 [SELF_CHECK](supplement2/SELF_CHECK.md) 먼저 읽는다.

1. 전문 색인 독립 창 사전등록 2025-10-06~12 / 10-13~19. TWIR #620 8행, #621 11행 용량 확인 후 원순서 첫6씩 모집하여 **B 12/12**. A 12/12. C 10/09 1행뿐, 10/16 목록 접근 불가. 실제25/36; 열림17(제작자13/중간4), 실패8, 공백11(구조5/목록 접근 실패6). 금요일 10/17 첫6의 3 중간/3 실패/0 적격은 감도층만; 동결 창 대체 안 함. 새 엄격 직접/조건부 0/75쌍, 일반 DB 질의까지 허용한 감도층 Seaography R3 1. 원 전문 우위 재현 안 됨. 누적 원32+S1 31+S2 25=88/108, 열림68(44/24), 실패20, 공백20, 73 work_id 라벨/88자리. 엄격 적격3/5쌍(264 실제 요구쌍), 직접0. 원 부족을 새 관측으로 지우지 않음. S2 산입18, 누적76레코드/72 work_id.
2. 한국어 [공개 등재 이력](supplement2/show_history.jsonl): 3개 2025 과거 날짜 페이지 첫20씩, 명시 Show GN 5/60, 원문5/5(JSilicon, Linux tuning, Chatter, unegg, Ad Astra). Show-only 고정판/전수 분모와 당시 순위·점수 미확인. [시도/출처](supplement2/show_attempts.md). 기존 네 언어 날짜쌍 유지.
3. 역사 [노출 시도](supplement2/exposure_attempts.jsonl)16행. [ciphernotes #4](https://github.com/rapnuss/cipher-notes/issues/4) 2025-11-23 18:56:26 UTC의 제3자 요청 1건 이상(편입 전); [LWN](https://lwn.net/SubscriberLink/1039374/664ea18bb8a3c1a8/) 2025-10-15 17:00 UTC 공개 댓글 1건 이상(등재일 종료 기준). 종류/기간/모수 다름. Telegram 2015 이미지 요청 제외. 집중 후보6의 정확 누적 audience0/6; 전체 비교 원장0/88(전수 개별 조회 아님), GN0/5. GH Archive WatchEvent 5 repo 쿼리 DNS/웹 실패 0/5 결과; 0노출로 바꾸지 않음. 현재 별/점수·날짜 null 댓글 미산입.
4. [계약](supplement2/contract_attempts.md) 재시도: DNS·checkout 부재 exit128, workbench 모듈 없음 exit1, cloud_check/check.py 없음 exit2. 공통 본체 통과 미확인. 보조 검산: 원+S1 구조 비용 480 필드, S2 696 필드 불일치0, frame/path 및 source 참조 불일치0. 실제 연구 호출 web26배치126하위 요청/GitHub8개별/shell5행, [호출](supplement2/calls.csv). 웹 그룹 시간만 일부 확보, 개별 대기 미계측. 기록 읽기/쓰기 비용 비교에서 제외.
5. 주요 원장: [PROTOCOL](supplement2/PROTOCOL.md), [frame](supplement2/frame.csv), [paths](supplement2/paths.jsonl), [sources](supplement2/sources.jsonl), [judgments](supplement2/judgments.csv), [cost](supplement2/cost.csv), [recalculation](supplement2/recalculation.json), [금요일 감도](supplement2/friday_sensitivity.jsonl), [추가 용량점검](supplement2/capacity_screen.md).

## 남은 미충족 및 다음 행동

- A/B/C 모두 6 이상인 독립 두 창을 목록만 먼저 확인한 뒤 별도 사전등록(기존 실험과 S2 수정 금지). 이번 추가 7주 점검 B/C 동시≥6 1, A/B/C 모두 확인0; 신규 비교 시작하지 않음. 개별 대기 및 실제 동일 시간 예산 기록.
- 한국어 Show 전용 고정 과거 전수 자료, 당시 제작자/제보 및 편입 기록·정확 historical audience, 정확 당시판 실행/독립 가린 판정 미확인. 날짜 고정 이벤트만 산입. 이전 4~6 역사 진단의 제품 판정은 바꾸지 않음.
- 실제 네트워크·exact checkout 및 manifest로 공통 계약 CLI 실행/exit/output 확인. connector 검산은 대체가 아님.

원 엄격 COMPLETE로 바꾸지 않는다. 아래는 이전 인계 그대로 보존하며 최신 다음 행동은 위 섹션을 따른다.

---

# AF-RES-149#1 HANDOFF — 보충 조사 S1 갱신

- task_id: AF-RES-149 / attempt 1, same owned branch
- status: PARTIAL (보충 조사 실행·비교·저장·검산 완료, 원 엄격 조건 일부 미충족)
- branch: work/research-af-res-149
- owned_path: docs/workstreams/research/AF-RES-149/
- original_start: f140af3179b7d9271710778104ccee5b4812e2ef
- frozen_baseline / resumed_from: fbd9a00b105da2666af5a158ee2678740572cf38
- original_result: 978c3ed46eaf44008901b2bb287e36977b4b461b
- supplement_protocol_commit: f9438d8c45d0c02b3cde985c06897c534b552407
- supplement_result_commit: d8bf7d96dc4c6d158fc37d707357889a08057799
- supplement_self_check_commit / last verified pre-handoff: b827365a8b9712b252b79e4af2a8690183f1b36a
- handoff_commit: 이 파일만 갱신하는 마지막 커밋; 브랜치 HEAD로 확인
- 통합·중앙 진행표 미변경. 원래 결과/자체검사/원장 그대로 보존. 기존 다른 작업 데이터/검토자 사용 없음.

## 재개 후 실제 수행 결과 (이전 인계의 다음 행동을 대체)

[보충 RESULT](supplement/RESULT.md), [보충 SELF_CHECK](supplement/SELF_CHECK.md)부터 읽는다.

- 사전등록 별도 창 2025-11-03~09 / 11-24~30, A/B/C 최대 6자리씩. B 새 7자리 확보로 원 부족4 누적 초과 보완. 보충 실제31/36, 첫 링크21성공(제작자14/중간7), 10실패, 5구조적 없음. 원32/36과 합63/72, 첫 링크51성공(31/20), 12실패, 9공백. 원 B-W2 실제2행은 수정하지 않음. 각 셀 실제6 충족 아님.
- 원 첫 링크 적격 3(5/96쌍), 보충 첫 링크 적격0(0/93쌍), 직접0. 보충 2차 추가8회/7성공→39시도/28열림, 엄격0, 현재 중간 설명 완화1. 역사 진단(비균등 추가 조사): 원 날짜 후보2→4, 새2, 합6/11쌍; Telegram의 topic export JSON 형식 추론 및 ciphernotes 당시 배포판/재연결 미확인에 따라 4~6. 기제 신규0. H01 channels-console 당시 고정 README와 H21 Calisthenics v1.3 JSON backup·H04 11/19 빌드 기록 확보. H12/H13 ciphernotes pre-listing 소스, H09/H10 Telegram pinned 코드, H11 공식 이전 형식 설명. 원 판정 변경 아님. Notesnook 현재 직접 R1 증거는 비교 밖, 2025 판 미확인.
- ja/en/ko/fr 최신·과거 날짜 목록 4/4 직접 확인. ko는 Show-only 2025 접근 불가로 같은 발행처 전체 날짜 목록; LinuxFr 과거 실패 뒤 FR Framablog 최신/월별 과거 및 과거 큐레이션 본문. 언어 목록 4개 확보와 동일 좁은 모집틀 완전 재현 구분. 실제 2026-11-24 한국어 orca 4점/CRAMA 3점(비교 밖), 2025 정확 노출 0/63. archive 5 실패, 존재하지 않는다고 추론하지 않음.
- 호출 연구 원장: web148 subrequests/20 invocations, GitHub39, shell3. web 배치 전후 UTC 상한, 개별 내부 대기 미계측. 이전 실험 시간 소급 금지. 원 비용 576 필드 및 보충 모집/열람 비용 240 필드 독립 재계산 불일치0. GitHub 재개봉으로 원본10/10 동일(이 HANDOFF 갱신 직전까지). git ls-remote DNS 오류 exit128 재현, 공통 계약 CLI 실행 불가.
- 산출물: [PROTOCOL](supplement/PROTOCOL.md), [frame](supplement/frame.csv), [paths](supplement/paths.jsonl), [sources](supplement/sources.jsonl), [judgments](supplement/judgments.csv), [cost](supplement/cost.csv), [secondary](supplement/secondary.jsonl), [history](supplement/history.jsonl), [history addendum](supplement/history_addendum.jsonl), [historical judgments](supplement/historical_judgments.csv), [languages](supplement/languages.jsonl), [live](supplement/live_observations.jsonl), [exposure](supplement/exposure.csv), [calls](supplement/calls.csv), [final attempts](supplement/final_attempts.jsonl), [recalculation](supplement/recalculation.json). 보충 산입17, 원41, 합58 기록/56 work_id. 진단 자료 중복 산입 금지.

## 남은 정확한 결손과 다음 첫 행동

1. 독립 사전등록 새 B 창에서 전문 목록 실제6개 확보 여부를 먼저 확인하고, 같은 창 A/C와 비교. 기존 원/S1 결번9 삭제 또는 다른 날짜 삽입 금지. 한국어 Show 전용 고정 과거 목록 필요; 네 언어 날짜쌍 자체는 확보했음.
2. 2025 시점 정확 audience 자료 0/63, 당시 개별 제보 및 편입 MR·배포 SHA 일부 미확인. 당시 snapshot/metric API 접근 가능한 환경에서 후보별 고정 원문·실행 검증 및 독립 가린 판정. Telegram topic JSON 직접 검증과 ciphernotes Android 오프라인/자동 재연결 필요. Calisthenics v1.3 JSON은 근거 확인, 실제 APK 시험 아님.
3. GitHub DNS 접근 가능한 환경에서 exact checkout과 계약 CLI를 실행하고 개별 요청 대기/시간을 계측. 새 비교에서 동일 실제 시간예산을 증명할 자료. 원 시간은 복구 불가.

원 과제 엄격 COMPLETE로 바꾸지 않음. 누적 수량 보완을 원 각 셀 완성으로 바꾸지 않는다. 다음 작업자는 새 결과와 검산을 이어받고 원 원장과 S1 원장을 덮어쓰지 않는다.

---

## 이전 동결 인계 (기록 보존, 다음 행동은 위 최신 섹션으로 대체)

- task_id: AF-RES-149
- attempt: 1 (중단 후 같은 브랜치에서 이어서 작업)
- status: PARTIAL
- branch: work/research-af-res-149
- owned_path: docs/workstreams/research/AF-RES-149/
- source_commit: f140af3179b7d9271710778104ccee5b4812e2ef (최초 작업 시작 통합판)
- protocol_commit: 1eda0cc3d22457e8980a21ee0c944f473e644414
- resumed_from: c560f49b577c802a3b2befa75eb5e9b6fc55d79b
- result_commit: 978c3ed46eaf44008901b2bb287e36977b4b461b
- self_check_commit: 936d41c8a0371249f6a050b120dd55223239f6ad
- handoff_commit: 이 HANDOFF.md만 추가한 마지막 커밋 (자기 SHA는 본문에 넣을 수 없으므로 브랜치 HEAD로 확인)
- inputs: AF-RES-002 @62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1; AF-RES-146 @9bf267b71a0000aae5f098e82eab3f84c0dd7714; 재개 시 통합 HEAD 35ca756d1b18af5d89c3eb53659365c09f1f88e3
- 통합/중앙 진행표 미변경. 소유 폴더 밖 수정 없음.

## 결론 (최종 설계 확정 아님)
A 지역 편집, B 전문 제보, C 배포 편입을 같은 날짜 창/최대 6자리 및 1회 원문 링크 시도 기준으로 비교. 이전에 누락된 A W1 6행을 월간 아카이브에서 복구. 실제 32/36; 30 링크 성공(제작자 17/중간 13), 접근 실패 2, 구조적 공백 4. 직접 0, 조건부 3 대상/32(요구×실제 자리 5/96), A 대비 B 추가 2 대상·1 기제. 날짜 고정 2, 현재 배포 설명 완화 4. A1 B2 C0 → 날짜 고정 A1 B1 C0, 완화 A1 B2 C1. 주 비교 바깥 GN/FR/PL 및 기증/입수 사례는 보조 증거. 전세계 발견률/작은 프로젝트 인과 효과 미확인.

## 산출물
- [SCOPE.md](SCOPE.md) 비교 기준·3 실사용 요구 동결.
- [frame.csv](frame.csv), [paths.jsonl](paths.jsonl) 36 계획 자리, 원순서·링크 실패·중복·미관측 보존.
- [sources.jsonl](sources.jsonl) 83 기록(71 성공), 산입 41(14 intake/14 maker/9 operation/4 outside), 5 원문 언어, 발행자 표기 29.
- [judgments.csv](judgments.csv) 108행, 현재 원문/날짜 엄격/중간 설명 완화, URL·조건·한계.
- [cost.csv](cost.csv) 24행, 절반/전량, A 대비 추가·단독·기제/100, 분모와 결측.
- [OPTIONS.md](OPTIONS.md) 발견 경로 대안/선택·교체 조건, 새 역추적 가설 및 타 분야 전이.
- [RESULT.md](RESULT.md) 첫 3 표, Q1–Q7, 반대 가설 및 마지막 약점 3개.
- [SELF_CHECK.md](SELF_CHECK.md) 원격 CSV/JSON 대조·비용 576 필드 재계산 모두 일치; 검사 한계.

## 미충족 및 다음 첫 행동
1. 실제 모집 4자리 부족(B W2 원 목록에 2행뿐). 동결 원장 변경/대체일 삽입 금지. 별도 보충 실험을 먼저 사전등록하고 6행 이상 확인 가능한 B의 독립 창과 FR/KO의 날짜 고정 목록 접근성을 확인한다.
2. 당시 노출 지표 정확한 값 0/32, 당시 제작자 고정판 및 개별 제보/편입 MR 미확인, C 12/12 중간 본문. 호출/대기시간 미계측, 독립 블라인드 아님. 후속은 별도 두 단계 예산, 고정 판·원문·노출 당시 값 수집, 실제 호출/대기 기록, 지표 가린 독립 평가.
3. 네 언어의 최신 및 과거 동일 종류 목록 완전쌍 부족(FR 과거 접근 실패, KO 과거 혼합, 현재 캐시 최신성 불명). 5언어 원문 수는 충족하되 이 비교와 동치 아님. 네 외부 입수 원전도 컬렉션 단위라 낱권 정확 접수 시각 불명.
4. GitHub 연결 검산만 성공. 셸 DNS 실패로 로컬 checkout 및 공통 계약 CLI 미실시; 다음 실행 환경에서 검사 보완. 진행표 완료 처리 근거로 쓰지 말 것.

재개 시 RESULT/SELF_CHECK 먼저 읽고 위 첫 행동을 수행. 이 인계 이후 원래 비교 원장을 덮어쓰지 않는다. PARTIAL을 COMPLETE로 바꾸지 않는다.
