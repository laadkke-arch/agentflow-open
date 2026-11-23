# ProseMirror 재생과 판 경계

예측 봉인 `74dc9f887bc47bc0a92b9a75ea327ffa30aca70b`(2026-11-23T03:32:00Z) 뒤에만 실행했다. 실제 첫 후속 열람은 `2026-11-23T03:32:31.973Z`다. 실행 위치는 ChatGPT 클라우드 checkout, Node `v24.22.3`, npm `11.19.1`이다. 사람·원작성자·공개 CI의 실행으로 부르지 않는다.

## 1. 고정한 연구 변형

`run.cjs`는 PN1·PN2·PT1 각각 정상/경계 × opA/opB의 **12개 고정 변형**을 실행한다. 파일 맨 뒤에는 사후 공개 회귀 fixture를 history1.0.3/1.0.4에 넣는 **별도 2개 감도 실행**이 붙어 있다. 이 2개는 `variant=posthoc-public-regression`이며 예측 적중 분모에서 제외한다. 따라서 첫 실행 JSON에는 14레코드가 있지만 예측 변형은 12개다.

아래 명령은 checkout 루트에서 실행한다. 캐시는 추적되지 않으므로 커밋한 lock을 복원한 뒤 설치한다. 경로 밖 파일을 수정하지 않는다.

```bash
mkdir -p docs/workstreams/research/AF-RES-057/.cache/prosemirror/replay
cp docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/package.json docs/workstreams/research/AF-RES-057/.cache/prosemirror/replay/package.json
cp docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/package-lock.json docs/workstreams/research/AF-RES-057/.cache/prosemirror/replay/package-lock.json
npm ci --ignore-scripts --no-audit --no-fund --prefix docs/workstreams/research/AF-RES-057/.cache/prosemirror/replay
node docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run.cjs docs/workstreams/research/AF-RES-057/.cache/prosemirror/replay docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/results.json
```

실제 최초 설치는 `npm install --ignore-scripts --no-audit --no-fund`였고 종료0이다. lock 복원용 `npm ci`는 후속 담당자를 위한 명령이며 이 세션에서 별도 실행했다고 주장하지 않는다. 실제 node 명령·cwd·UTC·exit·스크립트/lock/출력 해시는 `run-receipt.json`에 있다. 하네스 종료0은 각 제품 호출이 모두 성공했다는 뜻이 아니다. 회귀 감도1.0.3의 `RangeError`를 JSON에 유지한다.

별칭 `history103/104/130/150`은 각각 npm `prosemirror-history`1.0.3/1.0.4/1.3.0/1.5.0이다. `prosemirror-inputrules`1.2.0. package provenance의5개 npm `gitHead`가 대응 GitHub 고정판과 모두 같고, 설치된5개 source file을 직접 취득한 GitHub source bytes와 비교해 모두 일치했다. 실행한 compiled dist 파일 해시는 `source-runtime-check.json`에 있다. npm의 source와 gitHead 일치가 해당 빌드 도구의 재현성까지 증명하는 것은 아니다.

공통 core는 명시적으로 state1.4.3, transform1.8.0, model1.22.3, view1.33.11, rope-sequence1.3.4로 고정했다. 이 묶음은 사건 당시 원작성자 환경이 아니다. 최소 doc/paragraph/text schema, 함수형 view wrapper, 고정 시각은 연구자가 보충한 입력이다. 실제 브라우저·IME·통신 왕복을 재현하지 않는다.

## 2. 사후 역사 의존판 확인 — 위 12변형과 별도

공개 원작성자 재현 저장소 `johanneswilm/pm-collab-test@50aca6003eac6890a36fd7b21a2e90a99b8bf7c6`의 `package-lock.json`에서 historical core를 읽었다. 이때의 model1.7.0/state1.2.2/transform1.1.3/collab1.1.1/schema-basic1.0.0/schema-list1.0.2/rope-sequence1.2.2/orderedmap1.0.0을 따로 설치했다. 다음은 **사후 4개 실행**을 재생하는 별도 명령이다.

```bash
mkdir -p docs/workstreams/research/AF-RES-057/.cache/prosemirror/historical-replay
cp docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/package.json docs/workstreams/research/AF-RES-057/.cache/prosemirror/historical-replay/package.json
cp docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/package-lock.json docs/workstreams/research/AF-RES-057/.cache/prosemirror/historical-replay/package-lock.json
npm ci --ignore-scripts --no-audit --no-fund --prefix docs/workstreams/research/AF-RES-057/.cache/prosemirror/historical-replay
node docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/run-historical.cjs docs/workstreams/research/AF-RES-057/.cache/prosemirror/historical-replay docs/workstreams/research/AF-RES-057/streams/prosemirror/replay/historical/results.json
```

원작성자 JSON 사건열과 초기 HTML 텍스트를 보존하되 EditorView/DOM/exampleSetup UI 플러그인을 history+collab의 headless state로 치환했다. 따라서 역사적 브라우저 실행과 같다고 하지 않는다. 원작성자 축약 사례의 local selection은6..13이며 모집 본문의25..30과도 다르다.

| 사후 입력 | history1.0.3 | history1.0.4 |
| --- | --- | --- |
| 원작성자 JSON 사건열, 원 초기123456789 | `RangeError: Position 22 out of range` | 텍스트123456789ABCED, selection6..15 |
| 유지보수자9bdb377 회귀 입력, 초기123456789ABCD | `RangeError: Position 21 out of range` | 텍스트123456789ABCDE, selection6..13 |

두 입력을 같은 출력으로 합치지 않는다. 후자의 원시험은 예외 없이 undo가 끝나는지를 시험하며 최종텍스트 assertion은 추가하지 않았다. 위 문자열은 연구 재생에서 관측한 것이고 원시험이 선언한 기대값으로 바꿔 쓰지 않는다. 각4실행의 receipt와 stdout/stderr는 `historical/` 아래에 있다.

## 3. 확인된 경계

- PN1의 역순 대조는 opA/opB 후 텍스트가 같아도 남은 undoDepth가0/1로 다름을 확인한다. 문자열 동등만으로 이력 소유·순서 동등을 판정할 수 없다.
- PN2에서 `undoInputRule`은 즉시 호출하면 `...`를 복원하지만 뒤의 `history.redo`는 false/dispatch0이다. `x`를 추가한 경계에서는 `undoInputRule` 자체가 false이고 `…x`를 유지한다. 원장의 정정을 편집기 redo 가능성으로 옮길 수 없다.
- PT1은 default group undo의 빈 문단 기대가 E의 다른 시험에서 봉인 전 의미상 노출됐다. 선언 assertion과 연구 재생이 일치해도 신규 사전 적중으로 세지 않는다.
- 공개 Actions/check-runs/commit-status를 정확4SHA에서 조회했지만 기록은 각각0건이었다. aggregate status `pending`을 실패나 실행 중으로 해석하지 않는다. 이 연구의 local replay가 공개 CI 결손을 채우지 않는다.
