# AF-RES-253 HANDOFF

**PARTIAL**. axe 공식 두 배포판을 검증해 주호출 **24/24**, ARIA 통제 **24/24**, 별도 폴더의 기본 모드 재생 **8/8**을 확보했다. 원자료는 **37개 고유 저작, 10개 계보, 날짜가 확인된 사건 16건**이다. WCAG 날짜판 본문 6절과 RFC 본문 2편은 직접 읽었다. Cloud의 HTTPS 네트워크 제한 때문에 WCAG 원 게시 HTML/Chromium target **0/6**, RFC **0/2**는 미확인이다.

## 1. 식별과 결과판

- AF-RES-253 시도 1, Codex Cloud Linux 셸. 세부 실제 모델 설정은 미확인이다.
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-253`, 소유 경로 `docs/workstreams/research/AF-RES-253/`.
- 통합 착수 SHA `d1353701530ffd4c68587276c15d988d2cc92972`. 직접 의존 AF-RES-235의 중앙 DONE 및 자체 PARTIAL을 `5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126`에 고정했다. [선행 인계](https://github.com/laadkke-arch/agentflow-open/blob/5dce1f8cd7ceafbf8a3c587a8f859bf1114eb126/docs/workstreams/research/AF-RES-235/HANDOFF.md)
- **원격 결과 SHA `a543a726012f20cdf91e74feec82583b9915614a`**. 결과판을 GitHub에서 다시 받아 자체 점검과 저장소 검사를 끝냈다. 가장 최근 저장소 검사는 2026-11-25 00:14:49 UTC에 끝났다. 이 인계는 다음 단독 커밋이며 최신 브랜치에서 구별할 수 있다. 최종 인계 작성 UTC `2026-11-25T00:17:42Z`.
- 보관 이력은 ① `5e3e727c4e0b31fadd77d76da0864141dffd1587` 사전 봉인, ② `1b2501ef7ac438a503974e05d1f9f2bdda84604b` 원장/HTTP 영수증, ③ `e8e29011c0270d09cc2c67508e3bb52e677703d4` 주호출/필수 표, ④ `7eb6820c6be02e91a7f6e5fecfe6dc109522cc4f` 반례/재생, ⑤ 위 결과 SHA의 RESULT·SELF_CHECK다.
- 238–242의 작업별 입력·정답과 241의 교육 서비스 동작은 이 실험 범위 밖이다. PR 미생성, 독립 검토 미실시.

## 2. 결과와 대표 파일

| 파일 | 확인한 내용 |
| --- | --- |
| [RESULT.md](RESULT.md) · [SELF_CHECK.md](SELF_CHECK.md) | 6행·24행 필수 표와 Q1–Q7, 약점 3행. 근거와 반증, 미확인 분모 |
| [SCOPE.md](SCOPE.md) · [session.json](session.json) · [sources.jsonl](sources.jsonl) | 사전 판정, 계약/의존 SHA, 원자료 51 접근행 중 37 고유 |
| [anchors.csv](anchors.csv) · [페이지 영수증](receipts/pages/) | 날짜판 6행의 실패 단계와 본문 관측. W3C 작성 HTML 두 파일과 합성 5개의 파서·브라우저 관측은 별도 |
| [rules.csv](rules.csv) · [axe 원결과](receipts/runs/) | 24회의 네 배열, 96 호출×rule 셀, 실행 옵션/지문·DOM·출력. ARIA CDP 통제도 포함 |
| [replay.md](replay.md) · [비교 JSON](receipts/replay/comparison.json) | 공개 입력·환경·실행 명령, 기본 모드 8쌍의 raw/정규화 비교, RFC 및 앵커 검사 |

4.8.0의 일반·활성 중복 ID 규칙은 기본/`wcag2a` 모드의 원배열에 없고 explicit에 다시 나타났다. ARIA는 4.7.2 violation에서 4.8.0 incomplete로 이동했다. 순서 반전은 같은 분류에서 이름만 바꿨고, 한 유일화 통제에서는 passes와 의도와 다른 이름이 공존했다. 별도 프로필 재생 8쌍의 차이 필드는 `timestamp` 하나였다. axe 판정·AX 이름과 실제 AT 발화는 별 관측이며 AT 및 실제 사용자 감사를 관측하지 못했다. 이번 fixture에서의 범위는 [RESULT](RESULT.md)와 [비용·약점](RESULT.md#비용대안추가-분석)에 있다.

## 3. 고정 결과판 검증

GitHub에서 결과 SHA를 별도 clone으로 열고 220개 소유 경로 blob의 Git 지문을 다시 확인했다. 두 주요 표 6×6과 24×6, 끝 표 3×4, Q1–Q7, CSV 행수 6/96, 원장 JSONL 형식·ID, 24호출과 24 통제의 raw 연결, 8 재생과 7 앵커 통제 재생을 대조했다. 문서 링크 183개의 형식과 저장소 내 대상 경로·절을 확인했다. 결과 diff의 소유 경로 밖 파일 0, 진행표 blob `41cefbc22f8d86795d0aff7204c9cbefb69577fa`. 독립 검토는 별도 미실시다.

| 실행 | 결과 SHA에서 읽은 출력과 범위 |
| --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-253/session.json --fetch` | 종료 0, `passed`, `remote_checked`, integration `78b64ce8b84ef1d37c2a7100dc376c65dd97e74a`, 계약 SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`, 의존 SHA 유지. check의 changed_paths는 자기 manifest를 제외한 219개, outside/unmerged/errors는 모두 공석. |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 종료 0, 시작과 종료 checkout SHA·clean 일치. doctor·acceptance·research-case·original-smoke·sessions 명령이 각각 종료 0. acceptance는 공통 55개와 lab 7·9개, 각 lab test/demo, 독립 export, 결과판 Git bundle 복원을 검사했다. discovery는 기존 랩 출처 연결 검사다. |
| 공통 `check-all`의 실제 적용 범위 | `no_active_sessions`, count 0. manifest가 소유 경로에 있으므로 직접 지정한 `session check --fetch`가 본 과제 계약 검사다. 저장소 공통 검사의 scope는 workbench이며 대상 페이지 HTML/axe를 재실행하는 항목은 별도 실험 영수증으로 확인했다. |

Linux x64 6.18.57, Python 3.12.14에서 위 두 검사 stderr는 0 B. 개별 session stdout 19,831 B의 SHA-256은 `b2bdd3570904950a5773700e4f330690416d2d49cbc8260eb8c920cc4a3a45fd`, 공통 stdout 14,892 B의 SHA-256은 `0cb22fdb14f433dd0bc0c25b20d5494fc1c9fe142d61f333ef073512c6a6a8b4`였다. 위 검사는 고정 결과 SHA 및 실행 당시 통합 계약에 대한 범위다. GitHub Actions/Windows 검사는 미실시다.

## 4. 막힌 이유와 재개 첫 행동

**차단된 작업**은 [inputs.json](inputs.json)에서 고정한 `www.w3.org` 3 문서 및 `www.rfc-editor.org` 2 문서의 원바이트 GET와 해당 WCAG 6·RFC 2 fragment의 Chromium 원격 탐색이다. 셸의 요청은 프록시 CONNECT 403에서 거절됐고 브라우저도 터널 연결 실패였다. origin 응답·바이트·DOM은 미확인이다. Cloud 환경의 시행 중인 제한 정책에서 두 호스트가 빠져 있었다. Cloud 환경 스킬의 네트워크 변경 절차는 소유자 승인을 요구한다. 두 호스트의 네트워크 변경 요청은 미실시이고, 최초 실패와 재생 준비에서 확인한 정책을 커밋했다. [실패 영수증](receipts/pages/network.json) · [재생 시 상태](receipts/replay/network.json)

**첫 행동**은 두 공식 호스트를 읽을 수 있는 승인된 실행 환경에서 `a543a72`의 고정 inputs를 다시 받는 것이다. 의존성 설치는 [replay.md](replay.md#공개-원자료에서-재생)의 lock과 `npm ci`를 사용한다. 소유 경로와 의존판 확인 뒤 다음 명령을 실행하고 종료 코드, 표준출력과 오류, 원바이트와 파서·브라우저 결과를 보관한다.

```bash
o=docs/workstreams/research/AF-RES-253
scratch=$(mktemp -d)
mkdir -p "$scratch/deps"
cp "$o/deps/package.json" "$o/deps/package-lock.json" "$scratch/deps/"
npm ci --prefix "$scratch/deps" --cache "$scratch/npm-cache" --ignore-scripts --no-audit --no-fund
node "$o/fetch-pages.mjs" "$scratch/page-bytes" "$scratch/http"
AF253_DEPS="$scratch/deps" node "$o/run.mjs" anchors "$scratch/browser" "$scratch/page-bytes" "$scratch/http"
```

발행일·Content-Type·SHA-256을 대조한 뒤 6+2 앵커의 정확 ID/name, 상위 절/제목, Chromium :target·위치·본문을 판독한다. 동일 SHA의 새 checkout과 별도 캐시에서 재생하고 0·복수·다른 절이면 해당 행의 판정과 인용을 수정한다. 2.0 정오표 #13의 정확 최초일, AT 발화, 사용자의 역사적 감사 원결과는 별도 미결이다.

## 5. 색인 제안

`AF-RES-253 · PARTIAL — WCAG 날짜판 fragment 및 axe 4.7.2/4.8.0 소비 결과 검산`. 진입점은 [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/a543a726012f20cdf91e74feec82583b9915614a/docs/workstreams/research/AF-RES-253/RESULT.md), 의존은 AF-RES-235. 별도 브라우저 도착과 원바이트 추후 보강, 주호출/반전/재생 확보를 표시한다.
