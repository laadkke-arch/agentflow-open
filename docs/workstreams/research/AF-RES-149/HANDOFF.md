# AF-RES-149#1 HANDOFF

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
