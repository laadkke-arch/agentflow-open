# AF-RES-134 인계 · PARTIAL

GitHub 원저자 질문 **6건·6저자**의 정책 재생과 검산을 완료했다. 완전 어절 B와 한 조사 허용 C는 활성 별칭 적중이 없어 같은 순위였다. C→Gate는 G2의 표시 충돌 1쌍을 해소하면서, 단일 프로세스 허용 조건에서 직접인 D01 1쌍도 보류했다. GitHub 관측 표시 18자리 중 C의 9공석이 Gate의 18공석으로 늘었다. 조사 상위 8은 유지됐고 Gate에서 검토할 원절은 28개였다. [결과](RESULT.md) · [짝 비교](evidence/transitions.csv)

| 층 또는 검증 | 상태와 분모 |
| --- | --- |
| 포럼 A | **PARTIAL** · 64 JSON의 프록시 CONNECT 403, 정상 HTML #1 열람 1건·홍보 제외, 나머지 63 ID 미확인 |
| 포럼 B | **PARTIAL** · 사이트 자체 네 검색 응답 0/4, 예정 32슬롯과 당시 배열 미확인 |
| GitHub G1 | **DONE** · 공식 반환 22개 첫 본문 열람 및 관측 적격 2건 재생. 조작 대상 판독이 남은 이미지 의존 2건 |
| GitHub G2 | **DONE** · 어떻게 24개와 싶습니다 22개 첫 본문 열람, 중복 슬롯 5개, 적격 4건·4저자 재생 |
| 전체 효능 | **PARTIAL** · 외부 고유 38편/최소 24편, 자연 질문 6/목표 8저자. 96쌍의 표시 봉인·기준 봉인과 288 정책 행을 확보했고, 적격 원문에서 B→C 회복/밀림 사례는 관측되지 않았다. |
| 다른 분야 및 검산 | **DONE** · 공식 철도 7편과 서지·전거 6편으로 식별자·역할을 비교했다. 두 번의 고정 재생 결과 일치, 원격 계약 검사 종료 0. 독립 세션 판독과 PyTorch Windows 런타임은 미실시. |

## 입력판과 실제 변경

- 계획 통합판 `42260ca230e028e1303667be943b861a1d5953e4`, 작업 시작·manifest 기준 `67eb3c65404bf70de554bee6eb4c126344a3cd4a`. 중앙표는 AF-RES-130의 등록 결과를 DONE으로 기록하지만, 그 결과 SHA의 인계는 포럼 원문 회수 PARTIAL이다. 이 차이를 이번 분모와 접근 기록에 반영했다. [범위와 입력판](SCOPE.md) · [계약](manifest.json) · [AF-RES-130 등록 인계](https://github.com/laadkke-arch/agentflow-open/blob/56e82eff157e558db4db01acb321d2fcc83574a0/docs/workstreams/research/AF-RES-130/HANDOFF.md)
- 선행 내용판 AF-RES-130 `2c901ef834f23603f849b6a2e740321c7b8bc56f`, 카드·별칭·점수 AF-RES-122 `e69a3f837d400ba8a4820edb5bcd91223dc5f9cc`, 한국어 어절 AF-RES-126 `abcdda426e2a2d19f0732752c221ea4d494458c4`, PyTorch `a8d6afb511a69687bbb2b7e88a3cf67917e1697e`. PyTorch는 선행 7편을 다시 읽고 6편을 추가했다. [출처 원장](sources.jsonl)
- 소유 경로에 번호·시각 고정 및 첫 본문 추출, NFC 구절과 본문 지문, 전수 표시·기준 원장, 두 정책 점수와 Gate 및 짝 집계를 추가했다. 재생 코드는 선행의 투영·점수·경계·동점 처리를 직접 호출한다. 여기서는 자료 획득·투영 검증·Gate 표시 및 재집계만 구현했다. 작업 경로와 의존을 `workbench.session`으로 검사했다. [재현](replay/README.md) · [계약 검사](evidence/session-check.json)

## 원격 묶음과 검사 SHA

| 묶음 | GitHub 커밋 | 그 SHA에서 재열람한 파일 |
| --- | --- | --- |
| 모집·판정 | [5279d689656e4bdc2d29f88943dcd0bb39ae13ef](https://github.com/laadkke-arch/agentflow-open/commit/5279d689656e4bdc2d29f88943dcd0bb39ae13ef) | SCOPE.md |
| 공개 창·요청 투영 | [94a6269a48c7724cadeab912322b15759e4b6a88](https://github.com/laadkke-arch/agentflow-open/commit/94a6269a48c7724cadeab912322b15759e4b6a88) | frame.csv, requests.jsonl |
| 선행 표시 판독 | [2a4af7b6365e0f6c771ea5fc9b7aff81039d99f4](https://github.com/laadkke-arch/agentflow-open/commit/2a4af7b6365e0f6c771ea5fc9b7aff81039d99f4) | display-review.csv |
| 별도 전수 기준 | [656825eff895d8878b94e5e67cf93a449566ffe2](https://github.com/laadkke-arch/agentflow-open/commit/656825eff895d8878b94e5e67cf93a449566ffe2) | truth.csv |
| 첫 점수 재생·반례 | [d12a81d3eab3d07d8a99800a950e4fb850631397](https://github.com/laadkke-arch/agentflow-open/commit/d12a81d3eab3d07d8a99800a950e4fb850631397) | ranks.csv |
| 필수 표·자기검산·두 재생 | [6a17cf5265e6f13155407c3785906b048982a12f](https://github.com/laadkke-arch/agentflow-open/commit/6a17cf5265e6f13155407c3785906b048982a12f) | RESULT.md, evidence/replay-validation.json |
| 원격 계약 검사 영수증 | [0467581b07747e343796ea1ac5b71c81c8aa666a](https://github.com/laadkke-arch/agentflow-open/commit/0467581b07747e343796ea1ac5b71c81c8aa666a) | evidence/session-check.json |
| 최종 인계 | 작업 브랜치에서 이 파일을 추가한 마지막 커밋 | HANDOFF.md |

재생 대상 SHA는 `d12a81d3eab3d07d8a99800a950e4fb850631397`이다. 같은 연구자가 두 새 프로세스를 사용했고, 각각 원저자 첫 본문 6개를 다시 읽어 본문·구절·투영과 6개 출력 CSV가 고정판과 일치했다. 계약 대상 SHA는 결과판 `6a17cf5265e6f13155407c3785906b048982a12f`이며 원격 통합판 `34ce88996e63786adfc24d1b6cd5306d0efd1bd9`를 받아 확인했다. `python -B -m workbench.session check docs/workstreams/research/AF-RES-134/manifest.json --fetch`는 `remote_checked`, 종료 0, 소유 경로 외 변경 0을 반환했다. [재집계](evidence/recount.json) · [자가검사](SELF_CHECK.md)

## 첫 재개 행동

공개 Discourse에 접속할 수 있는 환경에서 같은 두 URL의 배달 상태 및 배열부터 확인한다.

```sh
af134_next=$(mktemp -d)
curl -sS -D - --max-time 30 'https://discuss.pytorch.kr/t/6001.json' \
  -o "$af134_next/topic-6001.json"
curl -sS -D - --max-time 30 --get --data-urlencode 'q=가중치' \
  'https://discuss.pytorch.kr/search.json' -o "$af134_next/search-weights.json"
```

topic과 첫 게시물 번호, 검색 배열이 확인되면 A 6001–6064와 B 네 질의 첫 8 슬롯을 같은 순서에서 회수한다. 공개 HTML로 확인한 topic과 `post_number=1`을 맞추고 새 관측을 추가한다. G1 #30/#43의 첨부가 열리면 자연 질문 판정부터 다시 확인한다. 신규 요청 또는 바뀐 본문은 표시→기준→순위 순서로 재봉인한다. HDF5 배치 재시도는 입력과 Windows worker 요구를 먼저 확인하고, 공개 회귀의 CPU 재현은 기존 프로브 명령을 사용한다. [모집과 재생 명령](replay/README.md) · [CPU 확인 명령](SELF_CHECK.md#실행과-대조)

색인 제안 · **AF-RES-134 · 한국어 조사 결합과 표시 조건 · PARTIAL · 포럼 A/B 미복구, GitHub 6건 순위 판독, Gate 직접 1·충돌 1 동시 보류 · docs/workstreams/research/AF-RES-134/RESULT.md**

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
| --- | --- | --- |
| 포럼 JSON 실패로 A 63개 ID와 B 4개 검색이 미확인이고 적격 자연 질문이 6/8저자다. | 두 정상 JSON probe와 같은 #1을 먼저 복구하고 G1 #30/#43의 공개 그림을 연다. | 원저자 입력/출력을 특정할 새 원문과 최초 적격 채택 순서가 확인된다. |
| 현재 B/C 순위 동률은 활성 별칭 없는 6건에 한정된다. | 자연스러운 조사 결합, 실제 저자 거절 및 보존 조건이 있는 원문에서 짝 비교한다. | 직접 후보 회수, 표시 3위 밖 이동, 또는 역할이 다른 후보 진입이 같은 쌍에서 드러난다. |
| Gate는 표시 충돌을 하나 막고 조건부 직접 D01도 하나 잃었다. | HDF5 단일/다중 작업자 두 해석을 분리해 같은 배치 계약과 출력 원절을 독립 판독한다. | 단일 프로세스 금지나 명시 허용이 확인되거나, 호환 출력을 확보해 충돌만 보류하고 직접 링크를 유지할 수 있다. |
