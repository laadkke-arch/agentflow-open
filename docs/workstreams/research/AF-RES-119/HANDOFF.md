# AF-RES-119 최종 인계

**PARTIAL.** 두 공개 트래커에서 각각 40개 opening 사양과 41번째 경계를 고정했고 본 자연 입력 6/6을 확보했다. 최초 게시 리비전은 6건 모두 미확인이다. 독립 가림 판독은 0/18이었다. 정확한 저자 전체 환경의 유효 SVG는 0/36이다. 명시 core CLI 6회는 원 JSON 파싱에서 실패했고, 대체판은 30회 중 26회 유효해 원형·두 수정안을 모두 판정한 사건이 4/5였다. 구성 반례 18/18과 별도 M3994 대조 6/6을 판독했다. 출처 후보 293개 중 실제 본문·구간 283개, 산입한 고유 1차 저작 54개다. [고정 결과](RESULT.md) · [자가 점검](SELF_CHECK.md) · [독립 계산](evidence/verification.json)

V8627의 자식 하나 정렬 변경은 공유 도메인 경고와 원 SVG를 그대로 돌려줬다. 공통 정렬은 막대와 주석을 함께 재배치했다. V8628에서는 공유 brush 이동 설정과 로컬 fallback 색의 영향이 다르다. #3982의 공유 CSS는 alt·opt 둘 다 숨겼다. #3987의 showData는 범례만 바꾸고 101%를 유지했다. AA1·AB3 동명, 같은 AA1의 두 사용, mark 기본값과 로컬 point 덮어쓰기의 결과를 구성 입력으로 남겼다. 자동 A/B/C 정확은 0/6·3/6·3/6이고 matched B/C는 같았다. 작성자가 원 요청에서 답을 이미 적은 #3981과 추가 자료가 있어도 대안을 고르지 못하는 경우를 분리했다. [봉인 기준](truth.csv) · [판독](choices.jsonl) · [수정 원값과 출력](runs.jsonl)

## 식별과 기반

작업 ID AF-RES-119, 시도 1, 실행 위치 Codex Cloud. 저장소 laadkke-arch/agentflow-open, 브랜치 work/research-af-res-119, 시작판 `ba55c71bf1382dc7b83cf46b2439f590866fc50f`다. 계획판 `101426a5e76154bb89b642dd9bd3c52fc1229c30` 이후 통합판 dot-control 배정 추가를 확인했다. 허용 변경은 `docs/workstreams/research/AF-RES-119/` 한 곳이다. 최종 검사에서 통합판 `5e072663b2c1610339e925676bb1f4449b36d0c5`의 계약은 버전 2 그대로였다. AF-RES-115의 `7f853bd85c57ad3657a7bed4962a3c8eaeed8433`와 검사판 `0da8f40d4aff86a85c559d2851e5e38acff4f380`을 읽었고 의존은 전자의 인계 하나다. [계약·초기 관측](SCOPE.md) · [manifest](manifest.json) · [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/7f853bd85c57ad3657a7bed4962a3c8eaeed8433/docs/workstreams/research/AF-RES-115/HANDOFF.md)

모집과 보기 재생은 기존 workbench 계약 및 AF-RES-115의 입력만 전송하는 비교 원칙을 사용했다. 새 수집기는 본문에 들어 있는 JSON 및 Mermaid 문법과 UTF-8 범위를 다룬다. 렌더는 기존 제품 코드를 변경하지 않고 고정 배포 CLI와 격리 실행에서 수행했다. 첫 렌더에서 관리 Chromium이 공식 mmdc 9.3.0의 로컬 HTML 요청을 거부했다. 그 시도 36회는 도표 파싱 전 실패다. 같은 패키지의 공개 Mermaid 9.3.0을 메모리 문서에서 로드해 렌더를 진행했다. M3994는 원 HTML label을 보존하고 Chromium DOM 직렬화로 검산했다. [재현](reproduce.md) · [CLI 실패 영수증](evidence/initial-mmdc-failures.jsonl)

## 결과의 SHA와 검사

고정 결과는 `038ac865c8d2cada84e32989bdd5eb174f4bb7d8`이다. 2026-11-24 07:26 UTC에 GitHub에서 새로 clone해 작업판과 389개 변경의 소유 경로를 확인했다. 대표 원 이슈 6건과 두 프로젝트 40/41 주소를 개별 API로 다시 읽어 opening SHA와 생성 UTC 10/10을 대조했다. 필수 표 행 수는 7·18·22이며 Q별 표는 7행이다. 원출력·로그 지문 310개를 별도 계산 코드로 확인했다. [고정 결과판](https://github.com/laadkke-arch/agentflow-open/tree/038ac865c8d2cada84e32989bdd5eb174f4bb7d8/docs/workstreams/research/AF-RES-119) · [검사 영수증](evidence/acceptance-evidence.json)

`verify.py`, manifest `workbench.session check --fetch`, `cloud_check.py --environment codex-cloud --fetch-contract --require-clean`, `scripts/check.py --require-git`가 고정 결과에서 종료 0이었다. 공통 55, 기존 lab 7·9 검사도 통과했다. 공통 검사의 자동 검색은 no_active_sessions였고 이 과제 manifest는 별도 명령에서 검증했다. 동일 작업자의 독립 재계산과 원격 재열람을 수행했다. 다른 판독자·Windows CI·원 포인터 이벤트의 검증은 미실시다. 수용 증거와 이 인계는 고정 결과 SHA의 검사 대상 이후에 커밋한다. [명령·출력·종료값](evidence/acceptance-evidence.json)

| 묶음 | 커밋 | GitHub에서 다시 읽은 근거 |
| --- | --- | --- |
| ① 모집·판정 계약 | [5e06d3f031b083edfc0f76b8cd70c88ca3a5349b](https://github.com/laadkke-arch/agentflow-open/commit/5e06d3f031b083edfc0f76b8cd70c88ca3a5349b) | SCOPE의 생성순 모집·예산, manifest를 결과판에서 확인 |
| ② 원글·사양·보기 | [cedff0c33905964278641b708e83a82e0a5eabf6](https://github.com/laadkke-arch/agentflow-open/commit/cedff0c33905964278641b708e83a82e0a5eabf6) | cases, views, #3987 사양, opening-history |
| ② 바이트 수정 | [0138d609869ede5ea49b4f1d5d2f3df27367a294](https://github.com/laadkke-arch/agentflow-open/commit/0138d609869ede5ea49b4f1d5d2f3df27367a294) | 첫 저장판 LF 정규화 확인, CRLF 원 지문 복원 |
| ③ 기준 봉인·구성 반례 | [70a45b75588e21595dc1be10be9959a8ae36031d](https://github.com/laadkke-arch/agentflow-open/commit/70a45b75588e21595dc1be10be9959a8ae36031d) | truth, operations, sources 뒤 실제 렌더 |
| ④ 보기별 선택·두 반복 | [ea48206f14320a5472bbc8af734bd5743f114d85](https://github.com/laadkke-arch/agentflow-open/commit/ea48206f14320a5472bbc8af734bd5743f114d85) | choices, render-matrix, #3987 browser observations, brush tuple |
| ⑤ 독립 계산·결과표·자가 점검 | [038ac865c8d2cada84e32989bdd5eb174f4bb7d8](https://github.com/laadkke-arch/agentflow-open/commit/038ac865c8d2cada84e32989bdd5eb174f4bb7d8) | RESULT 첫 세 표, SELF_CHECK, frame, sources 및 새 checkout |
| ⑤ 결과 수용 영수증 | [4b966979a8625a899ca331788a4d45731922da8c](https://github.com/laadkke-arch/agentflow-open/commit/4b966979a8625a899ca331788a4d45731922da8c) | 고정 결과 SHA와 검사 시작 시각 확인 |
| 최종 인계 | 이 파일을 추가하는 단독 커밋 | 결과·수용 증거를 원격에서 다시 읽은 뒤 작성 |

## 첫 재개 행동

먼저 [cases.jsonl](cases.jsonl)의 V8625와 [원 오류](evidence/render/r1/V8625-base/svg.stderr.txt), [쉼표 제거 후 함수 오류](evidence/render/r1/V8625P-base/svg.stderr.txt)를 연다. [원 CodePen](https://codepen.io/danielmalaton/pen/rNrLzaj)에서 원 JS와 등록된 함수, 당시 브라우저 설정을 확보한다. 여기서는 웹 원 주소가 열리지 않았고 셸에서 원 URL·JS·embed가 터널 403이었다. 같은 제한 환경의 공식 mmdc는 재시도하지 않았다. 렌더 차이는 명시 core·원 함수·원 호스트를 대조한 뒤에만 판정할 수 있다.

공개 CodePen 접근이 가능한 실행 환경에서는 아래 방식으로 원 함수 입력을 따로 받고 SHA를 기록한다. [동일 판 설치 및 재생](reproduce.md)의 lockfile을 사용한다. 원 사양 파일은 그대로 보존한다.

```sh
af119_original_dir=$(mktemp -d /tmp/af119-author.XXXXXX)
curl -fLsS --max-time 30 \
    'https://codepen.io/danielmalaton/pen/rNrLzaj.js' \
    -o "$af119_original_dir/v8625-author.js"
sha256sum "$af119_original_dir/v8625-author.js"
python -B docs/workstreams/research/AF-RES-119/replay.py \
    --id V8625 --id V8625P --engines /tmp/af119/npm \
    --out "$af119_original_dir/replay"
```

재현 명령의 V8625P는 원 업체 코드 실행과 별개인 진단이다. 원 함수 등록이 확보되면 당시 Vega-Embed 환경의 원 날짜와 epoch 조건을 둘 다 실행한다. V8628은 원 앱판·데이터와 DOM drag start/end 및 hit target을 먼저 받는다. A/B/C 효과 확인은 다음 판독자에게 `views.jsonl`의 input만 분배하고 `truth.csv`는 판독 후 대조에 사용한다.

색인 제안 — AF-RES-119 · 공개 도표 사양의 발생·공유 설정과 기능 링크의 보존 범위 · PARTIAL · [결과](RESULT.md) · AF-RES-115 고정 인계 의존.

| 가장 중요한 불일치·약점 | 다음 조사와 직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 최초 리비전 0/6, 저자 전체 환경에서 유효 SVG 0/36 | [원 CodePen](https://codepen.io/danielmalaton/pen/rNrLzaj)와 [원문 이력](evidence/opening-history.json)에서 함수 등록과 정확 판을 읽는다. | 당시 원문 바이트와 호스트가 확인되고 원형·두 변경안의 저장과 출력이 맞는다. |
| 자연 입력의 독립 가림 판독 0/18이고 같은 길이 B/C의 기술 진단 정확은 3건씩이었다. | [보기 입력](views.jsonl)을 가려 제공하고 이후 [허용 판독](truth.csv)과 대조한다. | C만 정확히 가른 자연 사건이 늘면서 불필요한 확정이 증가하지 않는다. |
| 파이 합 100과 동률 보존이 충돌한다. brush 주입은 pointer 현상을 검증하지 않는다. | [저자 후속](https://github.com/mermaid-js/mermaid/issues/3987#issuecomment-1656810998)과 [원 brush 요청](https://github.com/vega/vega-lite/issues/8628)을 먼저 연다. | 파이 반환에 쓸 동률·합의 정책 또는 당시 정확한 hit target에서 일어나는 점프가 확인된다. |
