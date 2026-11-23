# AF-RES-052 · 부분 인계

## 상태와 고정 결과

**상태: 부분 인계.** 직접 자료 배당·8자리/24행 보고·A/B/C 배열과 같은 예산의 경로 비교·반례·감도·원격 재열람·session check를 마쳤다. 다만 자연4풀이 제목 매칭에서 비었고, 보강은1개 메타데이터 풀만 확보했으며 그 풀에 사전 사용자 목적을 연결하지 못했다. 주표본에서 요구를 완결하는 독립 구현의 증감을 일반화할 수 없다. 양성0 자체를 미완료 이유로 삼은 것은 아니다.

- 작업 브랜치: `work/research-af-res-052`.
- 소유 경로: `docs/workstreams/research/AF-RES-052/`.
- **결과 SHA: `3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9`.** RESULT 본문은 최초 결과 커밋 `95b5ee40522a190e67b9b7bd8aff6fe3ea1bec20`와 동일하며, 수용 원장의 실제 출판검증 상태만 후속 커밋에서 완료했다.
- 최종 검증 영수증 커밋: `d7eef8b8054fc875c417090163973bf51bb9eae4`.
- 필수 표1: [고정 RESULT L1–10](https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/RESULT.md#L1-L10), 자연4자리+보강4자리.
- 필수 표2: [고정 RESULT L12–37](https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/RESULT.md#L12-L37), 같은8자리×A/B/C24행.
- [고정 수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9/docs/workstreams/research/AF-RES-052/evidence/acceptance-evidence.json): `overall_status=partial_handoff`, AC15 실제 검증 충족.

이 인계서는 위 두 문서를 고정 결과 SHA에서 원격으로 읽고 실제 검사를 끝낸 뒤 작성했다. 마지막 커밋은 HANDOFF.md 한 파일만 포함한다. 커밋되지 않은 캐시 전문은 제출 증거로 요구하지 않는다.

## 배정·읽은 입력·커밋 순서

| 구분 | SHA·확인 |
| --- | --- |
| 계획 기준 통합 | `d8c8d029bfb6107520ae74d2a172b2b18840e764` |
| 실제 배정·시작 통합 | `522ea9092d4d56ef6db0bd4f707bfc90032e179e`; AF-RES-052 RUNNING/attempt1/web-pro 확인 |
| 읽은033 의존 | `03ff2eb1264b85016266de1f36ddebe45f5fface`; HANDOFF와 returned-window-audit |
| 읽은048 의존 | `132e0108e652bdd2413edb71dfd6531507ea63e8`; HANDOFF. 표시규칙/changes는 보조판 `a690049db3a0e22ae20e0573a67925b8800efb34` |
|① 규칙·요구 | `842b7099bba6869000abad23f0316d34556bd080`, `817ebda103ee5926c308ad563a5879c2cf66fc32` |
|② 잠정 목록·정정 봉인 | `cd940aa340a5396611d028002ffc7150981f853a`, `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e` |
|③ 관측·경로·반례 | `37a82ee278c9db48b67c41e1c906eab6e976501b` |
|④ 결과·수용·검증 | `95b5ee40522a190e67b9b7bd8aff6fe3ea1bec20`, `3da61ff8a9d2e3ecfff1e5327bd26395babe3ae9`; 영수증 `d7eef8b8054fc875c417090163973bf51bb9eae4` |
| 최종check가 확인한 당시 통합 | `2875c1af816d6f376c061fffef20b739fd0af005`; 시작판을 이 판으로 소급하지 않음. 계약 hash 일치로 passed |

실제 환경은 ChatGPT의 클라우드 Linux 셸·GitHub 연결·공개 원문 읽기다. 별도 모델 선택 UI를 확인한 것으로 쓰지 않았다. 지정 모델/작업자와 실제 관측 환경의 범위는 SCOPE 및 manifest에 있다. AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md와 배정 항목을 읽고 시작했다. dot-control.json과 소유 경로 밖 파일을 편집하지 않았다.

## 확인한 결과와 부분 충족

| 단위·원장 | 확인한 결과 | 결론 경계 |
| --- | --- | --- |
| 자연4자리 | Python #564/#574, remark #941/#955. 고정 기능명사→발행 제목/공식별칭 매치 모두 관측0 | 반환 ID 관측0이지 생태계 해결책 부재가 아니다. 네 생성판은 미복원. |
| 보강4자리 | P-S1 bandersnatch5URL만 확보; P-S2/M-S1/M-S2 미충원 | 목적 연결0/확보1. 목적 연결된 완결 양성 비율은 분모0이므로 해당 없음. |
| P-S1 A/B/C | A=C 원1,2,3; B 원1,5·형제2,3,4 | 원5 S3 URL 승격은 확인. 미러의 보완 저장 서비스·목적 미연결이라 독립 완결 대안 증감은 미확인. |
| D-M1 진단 | A/C1,2,3; B1,6.50경로 A18/B14/C18. B-P08만 C1 노출 | 원6 mdast는 명세. 모든 방식의 현재 직접/두동작 완결·한 시행 최대는 관측0. 자연/보강 자리를 대체하지 않음. |
| D2 현재 계보 | `IM-M1-current-configured`: remark-stringify11.0.0 + utility2.0.0, fences=true·backtick·덮어쓰기 없음 | 코드·시험으로 가능한 호환 조합을 판독. 실제 설치·실행·literal react-stringify10.0.2 역사판과 다름. |
| 추가 슬롯 | D-M1의4슬롯은 A/C에 원4 C1을 직접 노출; P-S1은 원4 PyPI만 추가 | 완결 결론은 변하지 않음. P-S1 AWS 원5를 A/C에 직접 올리려면5슬롯 필요. |
| 반례 |12건: 명세/보완서비스, 부분조건만 증가, 보완경로 지연, 뒤쪽병합, 한문서 여러역할, 옵션반례·릴리스충돌·snapshot차이·녹음·서체 | 각 최소 반증/재개 조건은 counterexamples.csv. 다른 분야를 software적중에 합산하지 않음. |

기능 절과 소속 범주를 혼동한 잠정판을 목록 노출 뒤, 새 목적지 열람 전에 정정했다. 이전 배열과 영향은 CORRECTIONS.md 및 두 원격 커밋에 보존했다. remark README는 목록 라우팅과 D-M1 첫 목적지의 같은 저작이라 먼저 노출된 예외다. 전 목적지 비노출을 주장하지 않았다.

## 자료 수와 실제 실행

직접 열람의 필수 배당은 **중복 없는24저작**: 사용자 요구4, 공식 목록/작성규칙4, 공급자 문서/기능명세8, 별도 릴리스/시험4, 녹음/서체 개별 기록4다. 같은 매뉴얼 장·README 재게시·녹음 HTML/XML·fragment를 중복 산입하지 않았다. 추가 자료는 배경으로 유지했다.

`sources.jsonl`은151행, 모집·맥락까지 포함한 직접 확인 고유 work_id132개, 원문 실패/정확fragment 미확인13행이다. 이는 후보132개나 실행132회라는 뜻이 아니다. 같은 저작의 최종 재열람 시도는 별도 `final-source-rechecks.jsonl`, 도구별 실패 뒤 같은 정확HTTP 주소가 회복된 시도는 Markdown observation-failures에 연결했다.

| 실행·검사 | 실제 상태·결과 | 증거 |
| --- | --- | --- |
| 지정 session start --fetch | 실행, exit0 | evidence/start-receipt.json; manifest.json |
| 표집/배열·경로 계산 및 원장 통합 | 실행 | prepare_inputs.py, assemble_sources.py, assemble_results.py와 각 출력 |
| 자체 원장 검사 |50개 체크 passed, exit0 | evidence/local-validation.json; verify_research.py |
| 재현 계획 JavaScript 구문 검사 | `node --check` exit0; import/설치/fixture 동작은 실행하지 않음 | local-validation.json의 replay_plan_syntax |
| 초기 결과95b5ee 원격재열람·session check | RESULT/수용 원장 blob 일치; passed, exit0 | evidence/verification-initial.json |
| **최종 결과3da61ff 원격재열람·session check** | **2파일 byte/blob 동일, passed, exit0**, outside_paths=[], unmerged_paths=[], errors=[] | **evidence/final-verification.json**의 실제명령·UTC·stdout·stderr·checked_out_commit |
| 공급자 행동시험·패키지설치·실제 UI/사용자 시행 | 미실행 | D2와 사용자 창을 분리. 행동시험 결과나 실제 채택을 주장하지 않음. |
| 녹음 재생·서체 fvar/브라우저 검사 | 미실행 | 개별 레코드·발행자 판별 문서까지만 확인 |

실제 실행한 최종 지정 명령은 다음과 같다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-052/manifest.json --fetch
```

검사는 Git 계약·소유 경계를 확인하며 새 AI 대화나 제품 검증을 뜻하지 않는다는 원출력의 boundary도 그대로 보존했다. 전체 stdout을 요약으로 대체하지 않았다. 자료 결손을 파일 존재/검사 통과로 덮지 않는다.

## 남은 실행의 명령·입력과 다음 첫 행동

**다음 첫 행동:** 이번 모집을 덮어쓰지 않는 새 차수의 사전 등록 초안을 만들고, 목록과 독립적인 적격 목적·두 필수조건을 먼저 고정한다. 그다음 기존 출발점이 안내하는 [remark의 플러그인 안내 고정판](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/doc/plugins.md) 등에서 발행자가 직접 구성한 기능 절의 존재를 확인한다. 제목/공식별칭이 맞는 절·4–6위 별개 구현·C의 알려진5필드 충돌을 새 봉인으로 확보해야 현재의 요구별 효과 미확인을 해소할 수 있다. 관측 결과로 기능명사를 추가하거나 이번 빈 자리에 다른 절을 끼우지 않는다.

역사 재현은 [원941 첨부](https://codesandbox.io/s/beautiful-water-1j3fe?file=/src/App.js:0-1695)의 package.json/lockfile와 파이프라인을 먼저 확보해야 한다. literal react-stringify를 remark-stringify로 자동 교정하지 않는다. 원955는 별도 첨부의 unified10.1.1/rehype-stringify9.0.3/remark-parse10.0.1/remark-rehype10.1.0와 두 raw HTML 문맥을 입력으로 쓴다.

현재 조합만 검사하는 미실행 계획은 [evidence/markdown/REPLAY_PLAN.md](evidence/markdown/REPLAY_PLAN.md)에 완전한 명령·입력을 남겼다. 설치 폴더는 소유 경로의 `evidence/markdown/cache/replay-current/`다. 계획 package.json은 remark-stringify11.0.0, mdast-util-to-markdown2.0.0, unified11.0.0과 utility override를 고정한다. unified11.0.0은 허용 범위 안의 계획 pin이며 registry 확인·실제lock는 미확인이다.

```bash
npm install --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org
npm ls --all --json
node replay.mjs
```

위 명령은 REPLAY_PLAN의 package.json/replay.mjs를 만든 지정 cache 폴더에서 실행한다. 입력은 원941 body42–63의 root 아래 두 code 노드, lang=javascript/null, meta=null, 같은 전체 value이며 `export` 뒤 공백2개와 value 말미 newline 없음까지 보존했다. 네 시행은 configured backtick/default/fences=false/tilde이고 기대 C1/C2는 각각 true/true, true/true, false/true, false/true다. 이 명령은 이번에 실행하지 않았다. 구문 검사만 통과했다. 원문 fence 줄바꿈 모호성 때문에 전체 예상 문자열을 임의 byte oracle로 만들지 않았다.

Python의 PyPI 초기 동일 snapshot·-h 정확fragment·Compose 원주소·build inventory를 다시 읽는 명령과 정확 URL 입력은 [REPRODUCE.md](REPRODUCE.md)에 있다. 새로운 응답은 새 시행으로 보존하고 초기7.0.0과 후기8.2.0을 합치지 않는다. 목적이 연결되기 전 S3 네트워크 배포를 실행해도 현재의 완결 미확인은 해결되지 않는다.

## 파일 색인과 통합 제안

| 파일 | 역할 |
| --- | --- |
| SCOPE.md / CORRECTIONS.md / manifest.json / frame.csv | 사전 규칙·노출·정정·실제시작/의존판·모집/탈락/빈자리 |
| pools.csv / groups.csv / slots.csv | 원순위·표시5필드·결측·대표/형제; 진단은 evidence/diagnostic-* 별도 |
| evidence.csv / paths.csv / changes.csv | 조건별 근거·실제도착/예산·요구별증감/null;177행 중21빈상태·156경로행 |
| sources.jsonl / evidence/source-counts.json | 출처·배당·확인UTC·판/행·한계·중복/실패 |
| cards.md / sensitivity.csv / counterexamples.csv | 반환카드·추가슬롯/판미상감도·12반례 |
| RESULT.md / SELF_CHECK.md / evidence/acceptance-evidence.json | 필수표·Q1–Q7·반대증거·부분충족/미확인 |
| REPRODUCE.md / evidence/markdown/REPLAY_PLAN.md | 실제/미실행 구분과 후속 명령·정확입력 |
| evidence/final-verification.json / evidence/local-validation.json | 실제 원격·Git 계약·원장 검사 결과; 공급자 D3 결과 아님 |

색인 제안 한 줄: **AF-RES-052 — 부분 인계; 자연4풀 무매치·보강1/4 목적 미연결, 별도 진단에서 B의 C1 접근 증가와 명세 URL 승격을 확인했으나 독립 완결 구현 증감은 주표본에서 미확인.**

## 영향이 큰 약점과 다음 최소 조사

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 1. 기능 절 정의를 목록 노출 뒤 정정했고, 자연4풀은 빈 매치·보강3자리는 미충원·P-S1은 목적 미연결이다. | 주표본에서 독립 구현의 요구별 승격·손실을 추정하거나 B를 기본 형식으로 채택할 수 없다. | [PY 목록 L18–35](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L18-L35), [Markdown 범주 L34–98](https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md#L34-L98); CORRECTIONS C01, slots.csv2–9, groups.csv2–25 | 새 차수에서 발행자가 기능별로 구성한 공식 목록과 독립 사용자 목적을 먼저 고정하고 같은 정원·순서 규칙으로 다시 모집한다. 현재 빈 자리는 유지한다. | 같은 사전 규칙으로 매치된 요구·목록 절에 실제4–6위의 별개 구현이 있고 두 필수조건의 동일판 근거가 확보될 때. |
| 2. 제품판·문서 역할 등의 표시 결측으로 엄격 C의 실제 충돌을 확보하지 못했다. | C=A는 C의 유효성·안전성 검증이 아니다. 판 미상만 완화해도 다른 결측·부품 차이가 남는다. | [PY 목록 L21–24](https://github.com/pypa/packaging.python.org/blob/5ecbc0db967843e64d55da165b72e773888860c5/source/key_projects.rst#L21-L24), [Official L36–41](https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md#L36-L41); pools.csv2–6, sensitivity.csv30–41 | 목적지를 보기 전에 다섯 필드가 모두 명시된 충돌 쌍과 뒤의 별개 URL을 확보한다. 모르는 역할을 목적지 내용으로 채우지 않는다. | 알려진5필드 충돌로 앞3 대표가 달라지고 같은 목적의 독립 완결 ID 또는 필요한 보완 절의 접근성이 변할 때. |
| 3. 생성 당시 이슈·첨부, 일부 정확 도착과 같은 snapshot, 실제 설치·화면 시행이 미확인이다. 라우팅 README는 먼저 노출됐다. | 역사판 완결, 모든 목적지의 비노출, 실제 UI 두 동작 효과를 주장할 수 없다. D-M1은 현재 소스 창의 C1만 양성이다. | [#941 본문8–10·첨부](https://github.com/remarkjs/remark/issues/941), [옵션 L160–167](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167), [PyPI 초기 주소](https://pypi.org/project/bandersnatch); PY-A04/07/10/17, ME-HISTORY, sources.jsonl111–112·151 | 원 package.json/lockfile와 첨부를 확보하고, 정확 URL·fragment의 고정 응답을 보존한 새 시행에서 같은 입력을 실행한다. REPRODUCE.md와 Markdown REPLAY_PLAN.md의 입력·명령을 사용한다. | 역사 패키지 식별과 판이 확정되고, 한 시행의 실제 도착 창 또는 실행에서 C1/C2가 함께 확인되거나 현재의 부분 양성이 반증될 때. |
