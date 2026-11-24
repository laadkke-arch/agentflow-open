# AF-RES-122 인계

**PARTIAL.** PyTorch v2.5.1의 후보 16개와 출전 있는 활성 별칭 12개를 고정했다. 공개 첫 게시물 13건을 직접 읽고 10건을 진단층으로 재생했으며, 공식 시험 기반 구성 9건까지 304쌍의 판독과 76회 조회를 남겼다. 고유 1차 저작은 55개다. 정규 2025·2024 모집의 생성 UTC 경계를 검증할 수 없어 두 군의 8자리가 공석이다. [검사한 결과](https://github.com/laadkke-arch/agentflow-open/blob/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc/docs/workstreams/research/AF-RES-122/RESULT.md) · [모집 원장](frame.csv) · [출처](sources.jsonl)

포럼 진단의 모든 전체 요구에서 직접 적격은 0이었다. O5952의 영어 심벌 세 개는 원문에서 하위 기능 링크 세 개를 표시했다. 가림 뒤 둘은 조사 목록에만 남고 하나는 조사 밖이다. 별칭은 이 층의 표시를 바꾸지 않았다. 구성 C09의 전치는 가린 T04를 되찾았다. C01의 데이터로더 별칭은 D01을 올려 조사에서 찾아낸 D07을 표시 밖으로 밀었다. 화면 사용자의 클릭·이해와 실제 언어 효과는 미측정이다. [표와 조건별 손실](evidence/table3.csv) · [효과 원장](evidence/effects.csv)

## 식별과 변경 구조

- 작업은 Codex Cloud의 AF-RES-122 시도 1이다. 브랜치는 work/research-af-res-122, 시작은 chore/workspace-foundation의 3215fdb429e307175b2f277a9a167d2d07361883이다. 계획 기준 13be736df17a4c697880f57029d16de38db061dd 이후의 배정·진행 변경을 읽었다. 의존성은 AF-RES-118 인계 077258def07e3d7d103ecbd3183d60a2e35f9d48이다. 기존 workbench session 계약을 재사용했다. [범위](SCOPE.md) · [manifest](manifest.json)
- 카탈로그, 별칭, 모집 결정과 한국어 opening의 인용 위치, 원문/가림 해시·diff를 저장했다. prepare.py는 인용 범위에서 일치 위치만을 투영한다. replay.py는 카탈로그·별칭·두 투영을 읽고 순위 원장과 공석을 쓴다. summarize.py는 그 뒤 판독을 연결한다. probe_torch.py는 고정 CPU 판의 배열·인덱스·값을 확인한다. 35개의 결과 파일은 모두 소유 경로 아래에 있다. [재현과 입력 경계](reproduce.md) · [자가 점검](SELF_CHECK.md)

## 결과판 검증

검사한 결과 SHA는 **e69a3f837d400ba8a4820edb5bcd91223dc5f9cc**다. 그 SHA를 원격에서 확인하고 깨끗한 detached checkout으로 다시 가져왔다. GitHub에서 열린 표·집계·결과·검토 파일 4개의 blob을 대조했고, 발행 원문 4개의 커밋 주소와 태그 읽기 SHA-256도 일치했다. 표 3개와 비용·효과·누락 등 7개 파일을 재집계해 커밋과 바이트 대조했다. 두 새 경로에서 순위·표시·차이·비용 원장 4개가 일치했다. 포럼 투영 재생은 조사 중 확보한 웹 발췌를 다시 사용했다. [실제 명령·환경·입력·stdout·stderr·종료값](https://github.com/laadkke-arch/agentflow-open/blob/7efbd4ba68e12ca05d9acfd48a7ce3be0541f64f/docs/workstreams/research/AF-RES-122/evidence/acceptance-evidence.json)

2.5.1+cpu의 torch.version.git_version은 a8d6afb511a69687bbb2b7e88a3cf67917e1697e였고 실행 출력은 커밋과 일치했다. workbench.session check --fetch는 종료 0, remote_checked 및 범위 위반 0이었다. 검사 당시 통합 head는 3c428c04ac0d5bdce25046a78e27cb4afd49772c였다. cloud_check.py도 종료 0이며 내부 공통 55개와 lab 7·9개가 통과했다. 공통 자동 발견은 no_active_sessions였고 AF-RES-122 계약은 별도 명령으로 확인했다. 검산·CPU 호출·문서 판독의 주체는 모두 같은 Codex Cloud 작업자다. 별도 독자, Core ML·CUDA·DDP 실기기, 저자 판의 실동작은 미실시다. [CPU 관측](evidence/torch-probe.stdout.json) · [검사 영수증](evidence/acceptance-evidence.json)

## 묶음별 원격 고정판

| 묶음 | 커밋 | GitHub에서 다시 연 파일 |
| --- | --- | --- |
| ① 후보·별칭·규칙 | [dc9df1b1e7595bfe802152c82554276e92d54de7](https://github.com/laadkke-arch/agentflow-open/commit/dc9df1b1e7595bfe802152c82554276e92d54de7) | SCOPE, catalog, aliases |
| ② 공개 opening과 가림 | [92b06817e369b9cfa6c7672574741afc646c48bb](https://github.com/laadkke-arch/agentflow-open/commit/92b06817e369b9cfa6c7672574741afc646c48bb) | frame, requests |
| ③ 전수 기준·공식 반례 | [a92ab372d128a9576559c84630b584b8f21d7f4e](https://github.com/laadkke-arch/agentflow-open/commit/a92ab372d128a9576559c84630b584b8f21d7f4e) | truth, CPU probe |
| ④ 네 조회·두 재생 | [99f48d55f437e67ed71ebf8a460d04bfbde927cc](https://github.com/laadkke-arch/agentflow-open/commit/99f48d55f437e67ed71ebf8a460d04bfbde927cc) | ranks, comparisons, replay receipt |
| ⑤ 비용·필수표·자가 검산 | [e69a3f837d400ba8a4820edb5bcd91223dc5f9cc](https://github.com/laadkke-arch/agentflow-open/commit/e69a3f837d400ba8a4820edb5bcd91223dc5f9cc) | RESULT, SELF_CHECK, table3, metrics |
| 검사 영수증 | [7efbd4ba68e12ca05d9acfd48a7ce3be0541f64f](https://github.com/laadkke-arch/agentflow-open/commit/7efbd4ba68e12ca05d9acfd48a7ce3be0541f64f) | acceptance-evidence |
| ⑥ 인계 | [작업 브랜치 head](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-122/docs/workstreams/research/AF-RES-122) | HANDOFF |

색인 제안 한 줄은 **AF-RES-122 · PyTorch 16기능의 영문 심벌×한국어 별칭 네 조회 · 10개 공개 진단·9개 구성 · 정규 8자리 공석으로 PARTIAL · docs/workstreams/research/AF-RES-122/RESULT.md**다.

## 다음 첫 행동

discuss.pytorch.kr에 정상 접속 가능한 실행 위치에서 아래의 두 GET으로 카테고리와 생성 UTC 정렬을 먼저 확인한다. 익명 카테고리 API는 이번 셸에서 CONNECT 403, Chromium에서 터널 연결 실패였다. 활동 페이지는 서로 다른 수집 시점과 4페이지 결손이 있다. 이 결손을 해소한 뒤 topic_list.more_topic_url을 따라 두 UTC 경계를 기록한다. 2025년 첫 240건 안에서 opening 1을 시간순으로 판독한다. 부족한 군만 2024년 같은 방식으로 이어 간다. [접근 시도 및 경계](frame.csv) · [확인·재생에 쓴 명령](reproduce.md)

```bash
curl -fLsS 'https://discuss.pytorch.kr/categories.json?include_subcategories=true' -o /tmp/af122-categories.json
curl -fLsS 'https://discuss.pytorch.kr/c/qna/5/l/latest.json?order=created&ascending=true' -o /tmp/af122-category-page0.json
python -B -m workbench.session check docs/workstreams/research/AF-RES-122/manifest.json --fetch
```

| 가장 중요한 불일치·약점 | 다음에 열 자료·할 조사 | 무엇을 보면 판정이 바뀌나 |
| --- | --- | --- |
| 정규 UTC 시간순 8자리 미확보 | qna/5 생성 시각, 하위 카테고리, 두 기간 경계와 각 opening #1을 확인한다 | 정규 모집을 검증하고 직접 적격이 있는 질문을 확보하면 언어별 회수를 정규 분모에서 비교할 수 있다 |
| 별칭은 지칭을 회수해도 보존 조건과 거절 역할을 판단하지 못했다 | C01·C06의 역할과 원절을 독립 독자에게 보여 주고 새 공개 질문을 대조한다 | 유효 부품을 유지하면서 확인 충돌과 표시 밖 직접 손실이 줄어드는지 확인한다 |
| O5952는 2.2.2·Core ML 차이가 남았고 무명 질문의 회수는 구성 중심이다 | 2.2.2 체크포인트·변환기·가중치 stride와 원문에 영어 이름이 없는 정규 질문을 확보한다 | 변환 뒤 추론과 메모리·좌표를 함께 관측하면 일부 기능을 채택할 조건 또는 다른 판의 제약이 달라질 수 있다 |
