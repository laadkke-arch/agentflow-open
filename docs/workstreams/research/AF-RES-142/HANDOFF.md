# AF-RES-142 HANDOFF

## 판정: PARTIAL

계획 기준 d950356cdfae3edf799870cdeb90b93b5bd4ffd3; 실제 통합 시작 c088f5af075c3b010102d002e66c84d9263fe5de. 유일한 선행 AF-RES-138 중앙 DONE, 고정 인계 PARTIAL 198e74358fe2d124c31e16f8bbb93dbbf7ee561d, 고정 결과 5313f08e5aa2b45ff3477a963697d1f059059f05. 모두 원격 커밋/파일 재열람. 작업 경로 docs/workstreams/research/AF-RES-142/만 변경; dot-control.json 및 통합 브랜치 변경하지 않음.

## 관측과 판독

- 모집 84 슬롯(중립 64, 목적 20). 반환 중립 34, 고유 32, 138 기노출 3, 신규 중립 6 잠정 채택. 목적 반환 0/20, 적격 0. 검색 커넥터가 total_count 및 완전성을 제공하지 않아 실제 모집단 0 주장 금지. N1-06/07은 query가 template에 나타나고 실제 작성 feature는 별도; 좁은 조작 요청 기준 4명 이하 가능. 긴 본문 일부 발췌 및 선행 노출 해시 미검증. 선택 순서 불확실. 최초 모집 원장 보존.
- 후보 K16/K22 고정 후 L/R 4정책. 표시 봉인 전수 신규 판정 전 별도 커밋. 11×22=242 unique pairs (direct 2, partial 6, conflict 3, unconfirmed 231), 836 rank rows, 484 slot rows. 132 표시자리 중 1 표시/131 공석. 원격 JS로 재집계; 실제 PyTorch 실행 없음, 동일 판독자의 재판독이지 독립 판독 아님.
- 신규 중립 6건: K16/L, K22/L, K16/R, K22/R 모두 direct 표시 0/18, 직접 기회 1(좁은 dataset 가져오기 해석 N1-07/D01); R 조사 0, L 조사 16→17. 교정 5건: K16/L 0/15, K22/L 1/15, K16/R 0/15, K22/R 0/15; 직접 기회 K16 0, K22 1. C-P1-07/S04(준비된 입력→classifier 반환) 추가로 회복, 목표 구절만 보면 0점. 교정 후속 답 기노출이므로 신규 개선 아님. raw review→label 전체 요청 해석에서는 partial. N1-07/D01도 runner class 전체 해석에서는 partial. 실제 direct 밀림 관측 없음; N2-08에서 D01 조사8 밖 밀림, C-P1-07에서 T01 밀림(둘 다 direct 아님). 적합 후보 0인 층의 회복률 N/A.
- 구분: 목록 밖 공식 하위 조작 후보(cosine similarity, classifier C-logit/target range, token multinomial)와 이미 목록 안 0점, 전제 부족으로 표시 보류, 실제 자료 파일 부재는 별도 문제. N2-08 logits C와 label 범위 조건은 공식 계약으로 확인했으나 실제 모델 head 미확인. C-N1-03 키 불일치에는 strict=False가 해결책이라는 주장 금지; 호환 mapping 여부를 질문할 조건. 연구자 추론이지 사용자 응답/실행 관측 아님.
- 원장 82행(미열람·실패 포함), 보수적 산입 23: 잠정 신규 issue 6, 공급자 파일 8, 시험/공식 사용 4, 음악 4, 교통 공식 문서 1. 교통 개별 운영 레코드 0. 추가 K16 재열람/목록 밖 원절을 보수적 하한에 포함하지 않았다. 24 하한 및 교통 분야 최소 3 불충족; 실제 분모 23, 엄격 적격을 적용하면 더 낮을 수 있음. MusicBrainz work/recording/release ID 및 아티스트 공식 트랙 확인; duration 2:07 vs 2:03 차이 미해결. MBTA Harvard의 parent/boarding schema 직접 확인했으나 공식 API/웹 차단으로 70067/70068 방향·운행 ID 미확인. 개별 물리 열람 시간과 정확한 UTC 미계측; 논리적 절 대조 횟수만 기록. K16 각 카드 독립 시험/과거 버전, pad_sequence 별도 회귀 미검증.

## 커밋 및 원격 확인

| 묶음 | commit | 다시 읽은 대표 파일 | blob | 변경 경로 확인 |
|---|---|---|---|---|
| ① scope/cards | 1bc62377390e69f5175586b00818bd1ae1d8a152 | SCOPE.md | 892a8bcfd58f7bfc6585637fc3b375e02821775a | owned only |
| ② 모집 | d1c5576728c3e8149aa1576a8dce4f8a8a86b3cb | frame.csv | f1e1a35c0500f85c2f67ee4b1f9f65d0a54f758c | owned only |
| ③a 점수/구절 | 54fe5f5ce891e787a8ee4e87dfc9bfc8fe6c9809 | role_spans.jsonl | 3877a299953faea5189c5d5a686f4d1481fd3213 | owned only |
| ③b 표시 봉인 | 0a41578997e807f398c40c5e0fd762efcc095bb8 | gate-seal.md | 19a2a8cddc8878768132b0798d5812f862335211 | owned only |
| ④ 전수 | bc1d4367c39ea02fc5885eb54567b37c1b40caaf | judgments.csv | 72677e1bbbb757b6cd1009d61de79aec6537b437 | owned only |
| ⑤ 비교/출처/결과 | 6c379fe049e8e8416c4a42df8dcb9f76de36b684 | RESULT.md | 403150659255def9c660ad127fcaf7737449952b | owned only |

산출물: SCOPE.md, cards.csv, frame.csv, requests.jsonl, role_spans.jsonl, rank_scores.csv, slots.csv, gate-seal.md, judgments.csv, paired.csv, sources.jsonl, RESULT.md(표1~3, Q1–7 및 한계), SELF_CHECK.md, evidence/recount.json. 새 별칭의 동결 위치 SCOPE.md. 선행 K16 별칭은 AF-RES-122 고정 원장을 재사용. 별칭 수·점수는 사후 추가하지 않음. 현재 체크아웃 없음; Git 원격 연결은 DNS 실패. 로컬 workbench.session start/check --fetch 미실행. 위 커밋 변경 경로/대표 blob 확인은 GitHub API 원격 검산이지 로컬 검사 통과 아님.

## 첫 재개 입력 및 검사 명령 (미실행)

첫 행동: 아래 고정 API 질의를 실제 HTTP 응답 total_count, incomplete_results, 정렬, 페이지 및 원문 수정 이력과 함께 접근 원장에 추가. 84 원본 슬롯은 수정하지 말고 재생 결과 별도 파일로 보존. 6 엄격 적격 부족 시 등록 N1–N4의 17~32만 한 번 추가; 이미 판독·표시한 표본/결과와 새 표본을 분리. API 제한을 우회하지 않는다.

```sh
git ls-remote https://github.com/laadkke-arch/agentflow-open.git refs/heads/chore/workspace-foundation
git fetch origin chore/workspace-foundation work/research-af-res-142 work/research-af-res-138
# 깨끗한 baseline checkout을 준비할 수 있을 때만 시작 manifest를 기록.
git switch --detach c088f5af075c3b010102d002e66c84d9263fe5de
python -m workbench.session start af-res-142 --allow docs/workstreams/research/AF-RES-142/ --output /tmp/af-res-142-manifest.json --dependency work/research-af-res-138=198e74358fe2d124c31e16f8bbb93dbbf7ee561d --fetch
git switch work/research-af-res-142
python -m workbench.session check /tmp/af-res-142-manifest.json --fetch
# 시작 manifest를 사후에 생성하는 것은 원래 작업의 시작 당시 검사로 간주하지 않는다.
git diff --name-only c088f5af075c3b010102d002e66c84d9263fe5de..HEAD
git log --format='%H %s' c088f5af075c3b010102d002e66c84d9263fe5de..HEAD
```

공개 검색 API 입력: https://api.github.com/search/issues , sort=created, order=asc, per_page=100, page=1, q='is:issue is:public in:body created:2020-01-01..2025-12-31 "pytorch" "어떻게"' 및 나머지 SCOPE.md N2,N3,N4,P1,P2의 동일 조건. curl --get --data-urlencode 사용; 반환 첫 16/10 및 등록 확장 17~32만 소비. 원문 issue API에서 author, body, created_at, updated_at을 확인; updated_at은 수정 이력과 동일하지 않음.

교통 재개: https://api-v3.mbta.com/stops/place-harsq , /stops/70067, /stops/70068, /routes/Red, /schedules?filter[stop]=70067&filter[route]=Red 및 70068. 또는 MBTA GTFS 공개 archive의 같은 feed version stops.txt/routes.txt/trips.txt/stop_times.txt를 다운로드하여 stop_id, parent_station, route_id, trip_id, direction_id, stop_sequence 교차 확인. 원문 API가 열리지 않았던 실패 경로는 sources.jsonl A-TR1–9. 실제 방향 및 운행 ID 확인 전 미확인 유지. 이 단계가 24/유형 하한의 결정적 재개점. 이어 고정 판의 pad_sequence test 경로 재검색 및 K16 별 계약/시험, 역사판 존재/호환; 셀별 시간과 실제 opens 계측, 별도 독립 판독. 원본 표시·전수 표 사후 수정 대신 새 revision으로 기록.

색인 한 줄 제안: AF-RES-142 PARTIAL — K16/K22×L/R 신규 6 잠정 direct 표시 0, 교정 1 회복·R 1 소실; 242쌍, 보수적 원전 23/24, 목적 0·Harvard 공식 운행 원문 미확인.

## 가장 중요한 불일치·약점

| 가장 중요한 불일치·약점 | 현재 판정에 미치는 영향 | 다음 조사·찾을 자료 | 판정을 바꿀 관측 |
|---|---|---|---|
| 목적층 0/20·중립 6 중 2 템플릿·긴 원문 일부 미열람 | 자연 신규 표본 적격/순서 및 분모 미확정 | 동일 고정 질의 API total_count/created 정렬과 첫 원문 재검토; 부족 시 등록 17–32 한 번 | 6 엄격 적격 신규 저자, 목적층 각 10 반환 상태 명시 |
| 좁은 direct와 전체 산출물 partial의 경계; 교정 후속 노출 및 동일 판독자 | 교정 1 회복을 신규 개선으로 볼 수 없고 direct 기회가 해석에 민감 | 표시 숨긴 독립 판독과 동결한 목표/보존 기준; 역할 재분류 | 새 독립 직접 회복 또는 직접 소실 반례 |
| MBTA 원기관 API 차단·시간/판/시험 미검증 | 24 및 분야별 하한과 실제 열람 비용 미달; 운행 방향/ID 확정 불가 | Harvard GTFS stops/routes/stop_times/trips 원 레코드, pad_sequence 회귀 시험, 역사 버전, 실제 셀별 계측 | 하한 충족 및 실제 ID 방향 연결, workbench 재검산 |
