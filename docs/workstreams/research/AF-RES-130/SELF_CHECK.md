# AF-RES-130 자기검사 — PARTIAL

| 답한 주장 | 고정 근거 URL·위치 | 반대로 될 수 있는 조건 | 실제 찾아본 반증과 결과 | 미확인과 다음 한 번의 확인 |
| --- | --- | --- | --- | --- |
| Q1: 64개 ID 접근 시도, 1건 제외, 63건 미확인. B 응답 없음 | [frame 고정판](https://github.com/laadkke-arch/agentflow-open/blob/57e73d1ffd86dfad1277c35549aaf2b21c5e7d1f/docs/workstreams/research/AF-RES-130/frame.csv) 96행; [6027 #1](https://discuss.pytorch.kr/t/topic/6027) L5–36 | 실제 canonical slug/JSON이 열릴 수 있음 | 6001의 다른 URL 3개 실패; 6027 성공이 호스트 전체 접근 불가의 반례. 외부 검색 조각은 답글과 126 중복 혼입 | 63건 존재·원문 및 B 반환 순위; 공개 사이트 접속 가능한 환경에서 동일 창 재조회 |
| Q2: 적격 원문 역할 판독 미실시 | frame 및 SCOPE 판독 규칙 | 본문 확보하면 이름 유무와 의도 구분 가능 | 홍보 게시물은 질문으로 오인하지 않음; 코드/인용 판독 사례 미확보 | 원문 #1 범위·판·NFC 오프셋·해시 |
| Q3: 타입 조건 일부 읽음, 질문별 기준 미봉인 | [sources 고정판](https://github.com/laadkke-arch/agentflow-open/blob/e12a08f377bd59890593334a267dd53ccfdae74b/docs/workstreams/research/AF-RES-130/sources.jsonl) PT1–PT7 | 출력이 입력형·stride에 따라 달라짐 | sampler의 index와 loader의 sample 구별, reshape의 nonview 회귀 반례 직접 읽음. 실행 아님 | 원문 확보 후 승격 선행 봉인 및 16 전수 기준 |
| Q4: B/C 순위 미실시 | SCOPE, [126 SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/abcdda426e2a2d19f0732752c221ea4d494458c4/docs/workstreams/research/AF-RES-126/SCOPE.md), 122 고정판 prepare/replay | 어절 적중은 순위를 바꾸지 않거나 충돌을 올릴 수 있음 | 126 선행의 양방향 변화는 재사용 맥락; 신규 순위 미개봉 | 동일 고정 원문에서 두 번 점수 재생 |
| Q5: 승격 규칙만 저장, 판독 미봉인 | [SCOPE 사전 커밋](https://github.com/laadkke-arch/agentflow-open/blob/35b356843845f292718b06560725d3fe2995a0ab/docs/workstreams/research/AF-RES-130/SCOPE.md) | 원절 불충분으로 직접 후보 보류 가능 | T01/T02의 공유 조건 차이는 확인했지만 실제 승격 결과 없음 | 각 요청×16 역할 및 호환 출력 판독 별도 커밋 |
| Q6: 이득·비용 실측 없음 | RESULT 표 3; sources PT1–PT7 | 직접 적격 자체가 드문 층, 중복 작성자 등 | 관측 0과 결측 분리, 검색 응답 0을 실제 결과 공석으로 쓰지 않음 | 각 층별 직접 쌍/요청, 추가 원절 확인 및 유입·탈락 |
| Q7: 미실시 | SCOPE Q7 | 이름·ID 및 역할 혼동이 다른 분야에도 있을 수 있음 | 신규 역·서지 미열람; 반증 미실시 | 새 운영 역 ID·방향 및 도서관 전거/서지 각 3건 이상 |

## 실제 원격 자기검산

- 시작 SHA adafe971a088300e3a5319f95c5341db4c27e334; 중앙 진행표의 blob 4a212969cb235d2644514022beb9516c694316fa를 fetch_blob으로 복구했다(UTF-8 문자열 1,046,959자). JSON에서 AF-RES-130 RUNNING, branch/path 일치, depends_on=[AF-RES-126], AF-RES-126 DONE/result_commit d2bfe8cc4b3d7f28f4b9498770554878eaf6b118 확인. 최초 SCOPE의 진행표 읽기 실패는 이 후속 확인으로 해소됐다. 중앙 파일 변경 없음.
- ① 사전 규칙 35b356843845f292718b06560725d3fe2995a0ab: SCOPE.md 재열람 blob c387bb7adeb83dcedb671303b6787b697dedecb4.
- ② 모집 57e73d1ffd86dfad1277c35549aaf2b21c5e7d1f: frame.csv 재열람 blob 40a10eab0c71bf47c3c87481b00f0d283b0d0d12. JS 집계: 96행=A 64+B 32, A ID unique 64, A opened 1, A inaccessible 63, B unresolved 32.
- 원전 접근 기록 e12a08f377bd59890593334a267dd53ccfdae74b: sources.jsonl 재열람 blob 7c41369814e2cdd5411b8cc2104f426da7422ecf. JSON parse 76행; failed 67, success 8, snippet_only 1; 산입 work_id 7/고유 7.
- ③ 승격 및 전수 기준, ④ 순위는 차례를 어기지 않기 위해 미실시. ⑤ 부분 결과 fe2d50ff6548d9d339f5cc8a50b32000d1f28962, RESULT.md. 같은 작업자의 원격 파일 재독·행 재집계이며 독립 판독·순위 실행 검사 아님. 최소 24건 미충족, 신규 질문 0/8, API·회귀 파일 7/6, 문법·용례 0/4, 철도 0/3, 도서관 0/3.
- 현재 컨테이너 DNS에서 discuss.pytorch.kr, raw.githubusercontent.com 해석 실패(HTTP 000); 실제 checkout 없음. workbench.session start/check, 순위 재산출 및 CPU 미실시. 선행 126의 기존 실행을 신규 실행으로 세지 않는다.

## 재개 순서

기존 작업 브랜치와 소유 경로를 유지한다. 공개 사이트 접속 가능한 checkout에서:
```sh
git fetch origin chore/workspace-foundation work/research-af-res-126 work/research-af-res-130
git switch work/research-af-res-130
git merge-base --is-ancestor abcdda426e2a2d19f0732752c221ea4d494458c4 d2bfe8cc4b3d7f28f4b9498770554878eaf6b118
# 기존 manifest 없을 때에만:
python -B -m workbench.session start af-res-130 --allow docs/workstreams/research/AF-RES-130/ --dependency work/research-af-res-126=d2bfe8cc4b3d7f28f4b9498770554878eaf6b118 --output docs/workstreams/research/AF-RES-130/manifest.json --fetch
curl -fsSL --max-time 30 'https://discuss.pytorch.kr/t/6001.json'
curl -fsSL --max-time 30 --get --data-urlencode 'q=가중치' 'https://discuss.pytorch.kr/search.json'
```
200 응답 여부, 반환 실제 ID, post_number==1의 원작성자와 본문·편집 버전 확인. 접근 제한은 우회하지 않고 기록. A 6001–6064 전체와 B 네 질의 최초 8개를 고정하고 원문을 가려 판독, 현재 frame의 미확인 행은 근거가 있을 때만 교체. 전체 본문을 임시 입력으로 두고 공개 저장소에는 필요한 구절/지문/출처와 투영만 남긴다. display-review를 기준·순위 없이 커밋한 뒤 truth 별도 커밋, 그 후 ranks와 재생, Q7, 결과·검사를 작성한다.
```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-130/manifest.json --fetch
```
실행 SHA, 입력 지문, stdout/stderr/종료값을 evidence/에 기록. 이 명령들은 이 세션에서 실행하지 않았음.
