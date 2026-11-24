# AF-RES-189 HANDOFF

- work_id: AF-RES-189
- self_status: PARTIAL
- status: PARTIAL
- independent_review: NOT_RUN
- branch: work/research-af-res-189
- owned_path: docs/workstreams/research/AF-RES-189/
- result_commit: 328d1c6988ccaf89e7beddf34017bd7f80f68cff (⑤ 결과·자체점검 고정판; 이 HANDOFF 자체 SHA는 branch tip으로 확인)
- plan_commit: 0f6765df46ad2128c7fdfa92c3bf917bbfe0c5e6
- starting_integration_commit: 72cf39aea54e2de2ba78a245593aefdc40205a16
- dependency: AF-RES-180 central DONE / worker PARTIAL, 6b1afbba225dac3f051ea4a8c7bb8a6585071aea, fixed HANDOFF directly read.
- representative_files: RESULT.md, SELF_CHECK.md, SCOPE.md, frame.csv, sources.jsonl, requests.csv, states.csv, questions.csv; INITIAL_READ.md (body-only record).

## 판정 범위 및 핵심 발견
고유 원자료 44개(요구 22, 부족 0), 원장 51행(7 제외/비산입), 15 계보, 자연 자리 6/6, 후행 비교 5자리(그중 successor 1), 독립 원보고 사건 뿌리 8건(자연 4+사후 4, PR 별도); 코드/타입/시험 파일 11; MUI/APG 패턴 7; 별도 변경/소비자 문서 10; 타분야 10. requests 13, states 23, questions 11. 모든 종류 최소치 초과. 원작성자 직접 의미 확인 B/C/E, 사후 K; A는 본문에 명시된 S와 동일 작성자 PR의 접근까지, 재현 확인 아님.
- #36085 [S01](https://github.com/mui/material-ui/issues/36085) 검색어 표시 보존, #18784 [S02](https://github.com/mui/material-ui/issues/18784) 원격 검색 추가 발행 억제. B [동일 작성자 답](https://github.com/mui/material-ui/issues/18784#issuecomment-564681486)이 user-input only origin을 원함을 확인. 입력 보존과 요청 억제는 동일 정책 아님.
- 표의 한 질문: "선택 확정 뒤 입력창의 검색어가 그대로 남아야 하나요, 아니면 선택 라벨로 바뀌어도 이전 검색 결과가 유지되고 추가 검색만 없으면 되나요?" S면 [controlled states](https://v5.mui.com/material-ui/react-autocomplete/#controlled-states), R이면 [reason PR](https://github.com/mui/material-ui/pull/18796)과 [판별 migration](https://mui.com/material-ui/migration/upgrade-to-v6/#autocomplete). ID 또는 자유 문자열이면 [option structure](https://mui.com/material-ui/react-autocomplete/) / [validation case](https://github.com/mui/material-ui/issues/18656). H/P는 [APG](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). A/B 원질문처럼 이미 목적 명시되면 질문 불필요. 질문 효용 실험 0; 배정문 및 원문 노출 표기, 가상 답 분리.
- v5 reset이 select/blur/external prop을 포괄, v6 세분화. 제3자 #36085가 selection 갱신 허용/external 갱신 억제 요구(반대). J [Ant #58733](https://github.com/ant-design/ant-design/issues/58733)는 q 유지 또는 q와 필터 같이 초기화 둘 다 허용. K [react-select #5863](https://github.com/JedWatson/react-select/issues/5863)는 q 보존해도 결과 목록이 초기화된 사건. N [Carbon #2154](https://github.com/carbon-design-system/carbon-ai-chat/issues/2154)는 즉시 전송 시 clear, 삽입 전용은 보존 요구. O [SO #77461227](https://stackoverflow.com/questions/77461227/mui-autocomplete-resulting-in-an-infinite-loop-of-requests) 반복 요청과 input 유지 시도 보고, 실제 T 유지와 두 요청 동시 관측은 아님.
- MARC 전사/전거/ID·취소 규칙과 Ticketmaster/Seats.io 강조·선택·hold·book/expiry 차이 비교. 같은 이름과 동일 entity를 구분, ID scope, 취소 이후 final commit 여부 분리. 실제 거래/authority pair 검증 없음. DB/API/수집기/검색 순위 미결정.

## validation
⑤ fixed SHA에서 9개 파일 다시 fetch: SCOPE 14 lines, INITIAL_READ 5, frame 16, sources 51, requests 14, states 24, questions 12, RESULT 100, SELF_CHECK 30. 전부 nonempty. 형식검사: 44 unique count URLs, 51 source IDs unique, 15 lineages, required fields missing 0; frame 15×10, requests 13×14, states 23×13, questions 11×11 row-length mismatch 0; RESULT 요구 4 headers, Q1–7 7 headings, last table exactly 3 rows. Starting integration 대비 result ahead19 behind0, changed 9 paths all under owned_path, outside 0; dot-control.json unchanged. Small format verification only; independent review and runtime execution not performed.

| 묶음 | 대표 커밋 | 내용 |
|---|---|---|
| ① | c11c6c6e2a577bb9ebc3d0ef00bd0efa9ffb7d8d | scope/preflight and recruitment |
| ② | cf308378c28ea44f4051da07c3a51ee64126a759 / 676db795b37a19c8b9d45af75c4044f34629cf3c / c5eb5d1397ec10d9aa12504d07bc7c00f4802034 | body-only before comments, frame, ledger |
| ③ | 366babd9f7aac550b55c3cf3a4116c735f833367 / 966fb74101d1d27d32ea0937d1a25957f0e41146 | requests and state operations |
| ④ | 52519ced8efd9fafe8830462ab324a80ea1a8687 / 9fcabf0d365b557955eb4bab68f2856a266db946 / b5534b6379a823db922a7832b6e154e0047fa867 / ca6c73ba99d01479abf60c9f382c97701c773e2d | comparative counterexamples, routing, scope revisions |
| ⑤ | fcb63d05bb5b05d44dc862f7f39d5b02073fb33d / dd04deda71bc108b57302b20767e98178883b204 / 328d1c6988ccaf89e7beddf34017bd7f80f68cff | result, late near miss, self-check |
| ⑥ | this HANDOFF commit | final handoff |

## blockers / 미확인
- 원 최초 body edit revision 2/2 미확인, exact reporter-installed version 2/2 미확인. GitHub current body, public activity(title casing/edited comments), exact pinned source/PR SHA read. A literal input/mode/fixture and actual result after patch not verified. #37013 actual revert commit not located; v5.11.10 test target section only first line read and excluded.
- B extra request and K retained input→result reset and O attempted keep→repeated requests separately reported, **actual continuously preserved visible query plus exactly two search calls after select** combined case missing 1. No fabricated joining. Actual same-name 2 distinct authority ID records not individually fetched; rules and worked examples read (MUI duplicate label fixture read). This strict counterexample/provenance gap → PARTIAL even though core question routing and minimum counts met.
- v6.0.0 freeSolo createOption reason static propagation vs type union mismatch unresolved; callback tests not run, no request tracing or browser/ARIA tests. Question friction qualitative; no blind/independent reviewer. Exact observed author semantic response at least one satisfied, not claim user success on rebuilt versions.

## next_action / first resume
Read the fixed result and ledger, recover issue original revisions and reporter dependency manifests if accessible, then Codex Cloud synthetic callback fixture for the missing joint event and v6 reason. No new paid API, no account change, no central control edit. Only use authorized environment for dependency installation; if no lockfile/runner compatible, report blocker rather than change versions. 
```sh
git fetch origin work/research-af-res-189
git show 328d1c6988ccaf89e7beddf34017bd7f80f68cff:docs/workstreams/research/AF-RES-189/RESULT.md
git show 328d1c6988ccaf89e7beddf34017bd7f80f68cff:docs/workstreams/research/AF-RES-189/SELF_CHECK.md
git diff --name-only 72cf39aea54e2de2ba78a245593aefdc40205a16 origin/work/research-af-res-189
gh api --paginate 'repos/mui/material-ui/issues/36085/timeline?per_page=100'
gh api --paginate 'repos/mui/material-ui/issues/18784/timeline?per_page=100'
git clone https://github.com/mui/material-ui.git /tmp/mui-af-res-189
cd /tmp/mui-af-res-189
git checkout --detach ae4f62643704e7fb6721a37b4af1dcc417bf882d
git rev-parse HEAD; node --version; git status --short
# after lockfile/CI setup and approved dependencies:
yarn cross-env NODE_ENV=test mocha packages/material-ui-lab/src/Autocomplete/Autocomplete.test.js --grep onInputChange
# clean separate checkout for v5 source, then v6 tag:
git checkout --detach 684cd85544eff977f284e6bd5f9513483a85dd54
yarn cross-env NODE_ENV=test mocha packages/mui-material/src/Autocomplete/Autocomplete.test.js --grep onInputChange
git checkout --detach v6.0.0
git rev-parse HEAD
pnpm exec cross-env NODE_ENV=test mocha packages/mui-material/src/Autocomplete/Autocomplete.test.js --grep onInputChange
```
Commands derived from root package manifests X05–X07, not run/guaranteed runner setup. Repro inputs and observables in RESULT: synthetic q=sa, duplicate label same IDs 1/2, foo 3, freeSolo wat; selection, blur, Escape, external value replacement, select with controlled input unchanged; record T/H/V/P, reason/args/order/callback count and **mock fetch count/query/results**, distinguish two request sequences from two callbacks. On v6 multiple freeSolo, specifically record createOption input callback or absence and compare union. Record exact package/Node/lockfile/commit and output, not same reporter fixture unless verified. For authority example first locate two public name authority records with same unqualified label but different control IDs and their publication literal transcriptions; do not assume missing identifiers from name alone.

## index suggestion
AF-RES-189 | autocomplete 의미 판별: 입력·검색결과·강조·선택ID·자유문자 확정 분리, 한 질문으로 링크 분기/명시 목적에는 생략 | PARTIAL; result_commit 328d1c6988ccaf89e7beddf34017bd7f80f68cff | 44 원자료/6 자연자리/15계보, strict preserved-T+2 requests 미확인.
