# AF-RES-092 · 다음 첫 행동과 실행 대기 명령

## 지금 완료한 범위와 실행하지 않은 이유

6질문·12경로를 봉인하고 공개 후속/교정/타 분야 자료를 대조했다. 원자료·분모 감사는 `audit.py`로 수행했다. 원 질문자 성공을 재현하는 변환은 하지 않았다. 현재 설치판은 jq1.7, Pandoc3.1.11.1, TeX Live2025/dev이며 참조판 jq1.7.1/Pandoc3.1.11과 다르다. Quarto는 없다. 이는 이미 수행한 AF088의 고정 바이너리 변환을 다시 실행할 이유도 아니며, 현재판 실행을 정확판으로 바꾸어 적을 이유도 아니다.

원 질문자 환경은 더 크게 비어 있다. P1의 실제 문자와 fontfile, P3의 전체 Markdown/bib/CSL/명령, 모든 질문자의 정확판이 없다. 아래 명령은 **새 후속 관측**으로만 실행하고 기존12경로의 비용·후보·승패는 바꾸지 않는다. 필요 입력은 evidence/next-inputs/에 준비했다.

## 다음 첫 행동: P2 연결 근거 확보

소유 경로 안의 별도 실행 출력 디렉터리에 원 Qmd 및 두 파생 Qmd를 복사하고, Quarto1.4.553이 준비된 환경에서 실행한다. 정확판을 먼저 확인한다. 이 버전의 공식 release는 https://github.com/quarto-dev/quarto-cli/releases/tag/v1.4.553 이다. 판을 설치/검증한 영수증을 새 조사에 남긴다.

```bash
quarto --version
mkdir -p docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs
cp docs/workstreams/research/AF-RES-092/evidence/next-inputs/P2-*.qmd docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-original.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-sealed-macros.qmd --to pdf -M keep-tex:true
quarto render docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-answer-macros.qmd --to pdf -M keep-tex:true
rg -n 'booktabs|toprule|bottomrule|noalign|renewcommand' docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P2-*.tex
```

이 명령들은 실행 대기이며 이 환경에서 Quarto CLI를 검증한 기록은 없다. 각 render의 stdout/stderr/종료코드, Quarto가 쓴 Pandoc판과 TeX판, 입력 SHA-256, .tex/PDF를 보존한다. 판이1.4.553이 아니면 그 사실을 별도 조건으로 보고한다. 원 template가 booktabs를 먼저 로드하고 rule 재정의를 뒤에서 덮지 않는지 확인한 뒤, 원 출력 대비 두 수평선과 표 내용이 어떻게 바뀌었는지 검사한다. [2]{}와 {}는 서로 다른 후보이므로 같다고 합치지 않는다. 실패 출력도 보존한다. 사용자 원판을 알게 되면 그 판과 연구판의 결과를 분리한다.

## P3: reader 원인과 CSL 원인을 가르는 최소 관측

아래 입력은 전체 원문이 아닌 합성 최소형이다. 원본 Markdown/bib/CSL가 확보되면 같은 비교를 원본에도 별도로 수행한다. `$AF092_PANDOC_BIN`은 **검증한 Pandoc3.1.11 실행파일의 절대경로**로 지정한다.

```bash
"$AF092_PANDOC_BIN" --version
mkdir -p docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs
"$AF092_PANDOC_BIN" --from=markdown --to=native docs/workstreams/research/AF-RES-092/evidence/next-inputs/P3-reader-minimal.md > docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P3-default.native
"$AF092_PANDOC_BIN" --from=markdown-example_lists --to=native docs/workstreams/research/AF-RES-092/evidence/next-inputs/P3-reader-minimal.md > docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P3-no-examples.native
rg -n 'OrderedList|Example|Cite|citationId|achelis1897' docs/workstreams/research/AF-RES-092/evidence/_cache/next-runs/P3-*.native
```

기대하는 판별은 example-list/숫자 참조 구조가 의도한 Cite로 바뀌는가다. 이것은 아직 관측한 실제 출력이 아니다. 이 단계에는 citeproc/bibliography를 넣지 않아 reader와 citation 렌더링을 구별한다. 실제 bib/CSL와 원 writer가 확보된 뒤에만 전체 문서·서지 보존의 성공을 판정한다.

## J1/J3: 정확판에서만 별도 검산할 입력

`$AF092_JQ_BIN`은 검증한 jq1.7.1 실행파일 경로다. 사용자 실행이 아니라 연구자가 제공한 예를 확인하는 새 관측이며 외부 원자료 수를 늘리지 않는다.

```bash
"$AF092_JQ_BIN" --version
"$AF092_JQ_BIN" 'walk(if type == "object" and has("food") and (.food | type == "object") then .food.extra_cheese = true else . end)' docs/workstreams/research/AF-RES-092/evidence/next-inputs/J1-reference.json
"$AF092_JQ_BIN" --arg key b '.[$key] += 40' docs/workstreams/research/AF-RES-092/evidence/next-inputs/J3-reference.json
```

J1은 food 객체4개에 추가되고 나머지 값·배열이 보존되는지, J3은 b=42/a=1/c=3인지 본다. J1의 null/배열 food, J3의 점을 포함한 리터럴 키·중첩 경로는 별도 반례 입력이다. J2는 완전한 JSON과 새 값·대상 선택이 없으므로 실행 가능한 원문을 꾸며 만들지 않는다.

## P1에 먼저 필요한 입력

실제 실패 코드포인트, 선택한 Noto fontfile의 지문/coverage, 전체 Rmd, rmarkdown/Pandoc/TeX/fontspec판, PDF와HTML 각각의 출력/로그가 필요하다. 폰트 이름만으로 NotoSans와NotoColorEmoji의 coverage를 동일시하지 않는다. 공개답의 LuaLaTeX fallback은 이 자료가 확보되기 전까지 조건부 후보다. 없는 글리프·설치파일을 임의로 대체해 원 질문 해결로 세지 않는다.

## 탐색 공평성의 다음 실험

원12경로 로그는 다시 쓰지 않는다. P2-B의 실패한 질의를 고쳐 실행할 수는 있으나 이미 사후 답을 본 같은 연구자의 재실행은 원 탐색의 맹검 대체가 아니다. 별도 실험에서 실패 요청 과금, 파일당 노출 중복 제거, 소스별 노출 할당과 탐색 경로명을 먼저 봉인한다. 원 R0·각 고정 SHA·두 질의는 search_plan.json에 있고 검색코드는research.py에 있다. 새 로그 파일/새 실험ID를 먼저 정해야 한다. 기존 script의 중복 실행 방지 assertion을 제거하지 않는다.

## 이미 완료한 산출물의 재검사

최종 HANDOFF의 결과 SHA를 checkout한 상태에서 수행한다. `audit.py`는 고정 원기록을 바꾸지 않고 파생 pairs/metrics를 동일하게 생성한다.

```bash
python -B docs/workstreams/research/AF-RES-092/audit.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-092/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract
```

결과 SHA와 종료코드를 함께 남긴다. 마지막 HANDOFF 문서 커밋을 이전 결과 검사에 포함된 것처럼 쓰지 않는다. 공통 검사가 실패하면 공통 파일/검사기를 바꾸지 말고 원 로그·원인·다음 첫 행동을 인계한다.
