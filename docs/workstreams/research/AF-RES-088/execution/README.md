# AF-RES-088 실행 보완 패킷

## 현재 실시 범위와 버전

**고정 참조판 변환 실행 0건.** 로컬 `/usr/bin/jq`는 `jq-1.7`, `/usr/bin/pandoc`은 `pandoc 3.1.11.1`이다. 고정 참조판 `jq-1.7.1` 및 `pandoc 3.1.11`과 모두 달라 버전 검사만 실시했다. 설치·네트워크 다운로드를 하지 않았다. `support/execution_preflight.json`에 실제 검사 UTC, 실행한 `--version` 명령, stdout/stderr, 바이너리 SHA-256, 각 종료값과 전체 gate 종료값 **2**를 보존했다. 아래 변환 명령은 후속 실행 절차이며 이번 연구의 실행 관측값이 아니다. 기존 판정은 변경하지 않는다. 시도2의 JE1 사후 답 두 식은 별도 jq1.7로 보조 실행했고 첫 식 `[1,1]`, 둘째 `[1,2]`를 얻었다. 이 실행은 고정 참조판이나 원 질문자 실행에 포함하지 않는다(`../support/resume/outcomes_audit/JE1_answer_variant_run.json`).

| 구분 | 고정 참조 | 이번 로컬 관측 | 원 질문의 사용자 환경 |
|---|---|---|---|
| jq | `jq-1.7.1`, `71c2ab509a8628dbbad4bc7b3f98a64aa90d3297` | `jq-1.7`; 정확판 아님 | 선택 jq 질문에서 실제 설치판·실행 로그 미확인 |
| Pandoc | `3.1.11`, `c3038dcd54152c4e18e49db31676b79ee7cc29b2` | `pandoc 3.1.11.1`, `+lua`; 정확판 아님 | **PN1만** 질문 본문에서 `pandoc 2.9.2.1`, pandoc-types 1.20, texmath 0.12.0.2, skylighting 0.8.5를 보고함. 연구자가 직접 측정한 설치판 아님 |

Pandoc의 세 판을 서로 대체하지 않는다. 향후 3.1.11 실행이 성공해도 PN1의 2.9.2.1 실행이나 당시 PDF 결과를 확인한 것이 아니다. 버전 문자열 gate는 오실행 방지 장치이며 바이너리가 참조 커밋에서 빌드됐다는 공급 이력까지 보증하지 않는다. 실제 실행 때 빌드 출처·PDF 엔진·폰트·의존 라이브러리도 함께 남겨야 한다.

## 입력 출처와 추출 검산

입력은 `evidence/r0/`와 `evidence/r1/`의 **선택 8사례 × 2판 = 16 HTML 파일**에서만 가져왔다. 답변, 댓글, 현재 질문 페이지, 답 이후 코드를 입력으로 사용하지 않았다. `candidates.csv`의 SHA-256은 사전점검 파일에 기록했다.

`inputs/index.json`은 추출물 **37개**마다 다음을 제공한다.

- 사례·질문 ID·R0/R1, frozen HTML 경로와 전체 SHA-256.
- 원문 HTML 줄 범위, 0부터 시작하는 문자 구간, 그 구간의 SHA-256, 코드 블록 순번.
- 추출물 경로·SHA-256·바이트 수·역할, HTML entity를 한 번만 해제했는지 여부.
- 혼합 코드에서 JSON 부분을 고른 경우 디코딩된 부모와 정확한 부분 구간.

HTML entity 해제 후 코드의 공백·줄바꿈은 유지했다. JSON의 생략기호를 지우거나 값·외곽 구조를 보충하지 않았다. **PE2 R0는 별도 `<p>`로 보이는 코드 행을 LF로 연결한 복원물**이다. 이 둘은 최초 Markdown 바이트가 아니며, 원래 빈 줄은 알 수 없다. 나머지 추출물도 저장된 HTML에서 추출한 텍스트이지 즉시 게시 바이트 증거는 아니다.

저장소 루트에서 다음으로 추출물을 재검산한다. 파일 내용이나 인덱스가 다르면 종료값 1을 반환한다.

```bash
cd docs/workstreams/research/AF-RES-088
python execution/extract_inputs.py --check
```

이번 결과는 `verified`, 인덱스를 포함한 38파일, **종료값 0**이다. `--check` 없이 실행하면 frozen 파일에서 동일 추출물을 다시 만든다. 원문이나 `candidates.csv`는 수정하지 않는다.

| 사례 | R0/R1 입력 파일 | 즉시 재현할 수 있는 범위와 결손 |
|---|---|---|
| JN1 / 78253195 | `inputs/JN1/R0-input_fragment01.txt`, `R0-input_fragment02.txt`; `R1-weather.json` | R0는 외곽 `DailyForecasts`와 나머지 5일 자료가 빠진 생략본이다. R1의 완전한 JSON에는 5개 예보가 있다. 두 질의는 `attempted_query01/02.txt`에 별도 보존했다. |
| JN2 / 78262117 | `inputs/JN2/R0-helm_chart.yaml`, `R1-helm_chart.yaml` | 보인 YAML 자체는 추출 가능. 원래 Helm URL을 호출할 필요 없이 이 입력으로 jq의 JSON 파서 전제를 검사한다. 원래 명령과 오류는 `attempt_and_error.txt`에 분리했다. |
| JE1 / 78296361 | `inputs/JE1/R0-web_data.json`, `R1-web_data.json` | 혼합 예시의 `json_data =` 다음 JSON 배열을 정확히 잘라냈다. 두 객체를 파싱할 수 있으나, `JSONLoader`의 설치판·메타데이터 바인딩·실제 `/content/` 파일은 없다. 혼합 예시는 실행 가능한 Python 파일이 아니다. |
| JE2 / 78305924 | `inputs/JE2/R0-input_with_ellipsis.json.txt`, `R1-input_with_ellipsis.json.txt` | `....`를 보존한 불완전 JSON. `_count:566`이 적혀 있지만 566개 실제 레코드는 제공되지 않았다. 원하는 JSONL 및 시도 명령은 별도 파일이다. |
| PN1 / 78258237 | `inputs/PN1/R0-table.md`, `R1-table.md` | Markdown 표·캡션·EM DASH를 보존했다. 두 판의 스니펫 바이트는 같다. 실제 사용한 명령·PDF 엔진·문서 설정은 없으며 2.9.2.1 보고만 있다. |
| PN2 / 78267487 | `inputs/PN2/R0-formula.html`, `R1-formula.html` | MathEquation/MathRoot/MathScript 중첩 HTML과 `aria-label`을 보존했다. `reported_output.adoc`는 질문자가 보고한 실패 출력이며 기대 정답이 아니다. |
| PE1 / 78300525 | `inputs/PE1/R0-code_attribute.txt`, `R1-code_attribute.txt` | `{.lang .numberLines}`만 있다. 코드 본문·전체 Markdown·Pandoc 명령·PDF 엔진·마진 수치가 없다. 이미지 주소만으로 실행 입력을 만들지 않았다. |
| PE2 / 78461996 | `inputs/PE2/R0-python_chunk.qmd`, `R0-r_chunk.qmd`; `R1-python_chunk.qmd`, `R1-r_chunk.qmd` | Quarto의 `code-fold` Python 예시와 `sessionInfo()` R 예시다. 전체 `.qmd`, Quarto판, 실행된 출력, Pandoc에 전달된 AST는 없다. Pandoc 단독은 이 코드를 실행해 출력 청크를 만들지 않는다. |

## 정확판 gate와 JN1 두 경로

후속 담당자가 이미 확보한 정확판 바이너리의 절대 경로를 넣는다. 이 패킷은 도구를 설치하지 않는다. 기본값은 PATH의 `jq`와 `pandoc`이다.

```bash
export AF088_JQ_BIN=/absolute/path/to/jq-1.7.1
export AF088_PANDOC_BIN=/absolute/path/to/pandoc-3.1.11
python execution/reproduce.py --preflight
```

두 첫 버전 행이 정확히 일치해야 종료값 0이다. 한쪽만 검사하려면 `--require jq` 또는 `--require pandoc`을 쓴다. 아래 명령은 정확 jq gate를 먼저 통과한 경우에만 JN1 **R1** 입력에 두 `map` 식을 실행한다. 입력과 frozen HTML 해시도 먼저 검사한다.

```bash
python execution/reproduce.py --run-jn1
```

| 경로 | 고정 계약 안의 식 | R1 JSON에서 읽어 계산한 기대값 | 확인할 관측 |
|---|---|---|---|
| 강수확률 | `.DailyForecasts \| map(.Day.RainProbability)` | `[2, 1, 7, 6, 9]` | 종료 0, 배열 한 개, 원소 수 5, 값과 순서 일치 |
| AirAndPollen의 인덱스 1 | `.DailyForecasts \| map(.AirAndPollen[1].Value)` | `[12, 12, 13, 29, 69]` | 종료 0, 배열 한 개, 원소 수 5, 값과 순서 일치; 해당 입력에서는 인덱스 1의 Name이 다섯 번 모두 Grass임 |

기대값은 Python으로 frozen JSON의 두 경로를 읽은 값이며 **jq 실행 결과로 보고하지 않는다**. `reproduce.py`는 이후 실제 stdout/stderr·종료값·비교값을 JSON으로 반환한다. R0에 R1의 전체 JSON을 소급해 넣지 않는다. R0를 별도로 실행하려면 R0와 동시대의 완전한 입력과 해시가 필요하다. `map` 외 후보를 붙여 성공 기여를 부풀리지 않는다.

## 나머지 jq 사례의 다음 최소 검사

다음 명령 역시 이번에 실행하지 않았다. 정확판 gate 성공 후에만 수행한다.

```bash
python execution/reproduce.py --require jq || exit "$?"
"$AF088_JQ_BIN" '.' execution/inputs/JN2/R0-helm_chart.yaml
```

JN2에서 예상하는 것은 JSON 파싱 단계의 오류와 비영 종료값이다. 진단 문구의 정확한 위치·값은 실행 후 기록한다. `select`, `map`, `sort_by`, `group_by`는 이 파서보다 뒤에서 동작하므로 성공적인 YAML→JSON 변환을 제공하지 않는다. `-R`로 문자열을 얻는 검사도 YAML 구조 파싱 성공으로 세지 않는다. 근거는 같은 jq 매뉴얼의 Invoking jq L78–89, `--raw-input` L124–129와 `candidates.csv`의 네 절이다. 원래 Helm 저장소에 접속하거나 새 출력을 가져오면 frozen 입력과 달라진다.

JE1에서 JSON 객체를 재구성하는 실행이 성공해도 LangChain Document의 `metadata`에 값이 들어갔다고 판정할 수 없다. 다음 확인에는 질문자가 실제 사용한 `langchain_community`, Python `jq`, JSONLoader 구성과 두 Document 결과가 필요하다. 이 추가 API/사용자 코드는 고정 jq 후보 단독 범위 밖이므로 이 패킷은 연결 구현을 만들지 않는다.

JE2는 완전한 `response.json`이 필요하다. 생략본을 jq에 넣어 생기는 오류는 생략 입력의 오류이며, 실제 566레코드 파일에 관한 기능 반증이 아니다. 완전한 입력을 받은 뒤 각 레코드가 별도 JSON 줄이고 내부 `_rid`가 보존되는지 확인해야 한다. 배열을 내는 `map`/`group_by`와 레코드 스트림의 차이를 기록하고, 기본 `.Documents[]`가 이미 완료한 핵심 변환을 불필요하게 붙인 후보의 공로로 세지 않는다.

## 미확인 6후보: 필요한 입력과 관측

아래 여섯 행은 `PN1/Lua`, `PN2/Lua`, `PE1/metadata`, `PE1/template`, `PE1/Lua`, `PE2/Lua`이다. **프로그램이나 LaTeX 설정을 새로 만들지 않았고, 여섯 판정을 모두 그대로 둔다.** `execution/supplied/`로 표시한 경로는 아직 없는 후속 입력의 명세다. 파일이 없으면 실행을 진행하지 않는다. 코드는 답변에서 가져와 frozen 질문의 요구로 소급하지 않는다.

| 사례·후보 | 필요한 Lua/LaTeX/AST 및 환경 입력 | 첫 검사와 성공/반증 관측 |
|---|---|---|
| PN1 / `PD-lua-filter` | frozen `table.md`; 3.1.11의 Table AST; 실제 구분행을 식별해 한 줄 규칙을 만드는 `supplied/PN1-rule.lua`; PDF 엔진·표 스타일. 특정 LaTeX 방식을 쓸 경우 raw LaTeX와 Table/Row 타입 반환이 유효한지 별도 검사 | 원문 EM DASH 행을 일반 셀 텍스트로 읽는지 먼저 확인. 필터 적용 후 마지막 값 행·캡션·열 수가 보존되고, 경계선이 표 전체에 끊김 없이 이어지며 머리행 아래 선과 두께·색이 같은 PDF인지 확인. AST 변경 또는 PDF 시각 확인 없이 충족으로 올리지 않는다. |
| PN2 / `PD-lua-filter` | frozen `formula.html`; HTML reader의 실제 AST; MathScript/MathRow/VBox 및 속성의 보존 여부; 구조를 Math로 변환하는 `supplied/PN2-math.lua`; 정확한 원하는 수식 표기 | AST에서 아래첨자 관계를 복원할 근거가 남는지 먼저 확인. AsciiDoc 결과가 유효 STEM 블록이며 왼쪽·오른쪽 아래첨자와 `=`가 원래 수식과 같은지 비교. reader 단계에서 관계가 소실됐다면 필터가 추측해 만든 성공으로 세지 않는다. 임의 수식 일반화는 추가 입력 없으면 미확인이다. |
| PE1 / `PD-metadata` | 판과 연결된 전체 `supplied/PE1-R0-code.md`, `PE1-R1-code.md`; 적용할 LaTeX 매크로 텍스트 `supplied/PE1-header-includes.txt`; 현재 highlighting 환경과 PDF 엔진/마진 | `--metadata` 값이 MetaInlines/MetaBlocks 등 어느 타입으로 읽히는지, header-includes 위치에 원문 LaTeX로 전달되는지 확인. 번호가 마진 안으로 들어오고 코드 내용·번호가 보존되는 PDF가 있어야 한다. 값만 넣었는데 escaping되거나 스타일 변화가 없으면 성공 아님. 원문에 없는 매크로는 필요한 추가 입력으로 남긴다. |
| PE1 / `PD-template` | 위 전체 Markdown; 고정 기본 LaTeX 템플릿의 `$highlighting-macros$`, `header-includes` 위치; 수정할 `supplied/PE1-template.latex`; 실제 highlighting 매크로·PDF 엔진 | 템플릿이 생성 매크로의 배치/정의를 어떻게 바꾸는지 diff를 남기고 동일 PDF 입력으로 마진·줄번호·코드 보존을 비교. 템플릿 옵션이 standalone을 암묵적으로 켜는 것은 후보 고유 동작이다. 별도 metadata/Lua 후보를 추가한 성공은 이 행의 단독 성공이 아니다. |
| PE1 / `PD-lua-filter` | 위 전체 Markdown; reader가 만든 CodeBlock 속성; `supplied/PE1-margin.lua`; 출력에서 사용하는 LaTeX 환경과 마진·폰트 설정 | AST에서 `numberLines`와 언어 클래스가 보이는지 먼저 확인. 사용자 Lua가 CodeBlock/문서 메타데이터를 어떻게 바꾸는지 기록하고 실제 번호의 페이지 내 위치를 확인. numberLines 클래스가 보인다는 사실만으로 마진 수정 성공은 아니다. |
| PE2 / `PD-lua-filter` | 전체 Quarto 보고서와 해당 판·엔진의 실제 청크 출력; Pandoc에 전달된 `supplied/PE2-R0-input.ast.json`, `PE2-R1-input.ast.json`; 출력 블록 선택 규칙과 `supplied/PE2-output-fold.lua`; 목표 writer | 생성된 AST에 코드 입력과 출력이 구분되는지 확인한다. 필터 후 기본 상태에서 출력이 접히고 열면 전체 텍스트가 보이며 기존 코드 접기·다른 문서 블록이 보존되는지 확인한다. frozen `.qmd` 조각을 Pandoc으로 읽은 것만으로 실행 출력의 접힘을 검증할 수 없다. 목표가 HTML인지도 명시해야 한다. |

### Pandoc 공통 gate와 baseline AST

아래에서는 `AF088_PANDOC_BIN`을 앞에서 정확판 경로로 설정했다고 가정한다. 첫 gate가 실패하면 다음 줄을 실행하지 않는다. R0/R1을 각각 보존하되 동일 바이트라고 독립 실행 사건으로 세지 않는다.

```bash
python execution/reproduce.py --require pandoc || exit "$?"
mkdir -p execution/results
for AF088_REV in R0 R1; do
  "$AF088_PANDOC_BIN" -f markdown -t json "execution/inputs/PN1/${AF088_REV}-table.md" -o "execution/results/PN1-${AF088_REV}.ast.json"
  "$AF088_PANDOC_BIN" -f markdown -t latex "execution/inputs/PN1/${AF088_REV}-table.md" -o "execution/results/PN1-${AF088_REV}.latex-fragment.tex"
  "$AF088_PANDOC_BIN" -f html -t json "execution/inputs/PN2/${AF088_REV}-formula.html" -o "execution/results/PN2-${AF088_REV}.ast.json"
  "$AF088_PANDOC_BIN" -f html -t asciidoc "execution/inputs/PN2/${AF088_REV}-formula.html" -o "execution/results/PN2-${AF088_REV}.baseline.adoc"
done
```

이는 AST와 기본 writer의 관측을 위한 명령이다. LaTeX fragment만으로 PDF의 마진·색·두께를 검증하지 않는다. PDF 출력에는 Pandoc이 standalone 처리를 자동으로 적용한다. 다른 고정 후보를 명시적으로 덧붙여 후보 하나의 성공으로 세지 않는다.

### 제공된 Lua 및 template 파일을 시험하는 명령

다음 파일들은 아직 없다. 담당자는 파일 내용을 리뷰하고 SHA-256과 작성 근거를 남긴 뒤 정확판 gate를 통과한 동일 셸에서 실행한다. PDF 엔진 이름과 버전을 확인한 뒤 AF088_PDF_ENGINE을 export한 환경변수로 설정한다(원 질문자 엔진 미확인 상태에서 임의 기본값을 고정하지 않는다). 예시의 `R0`를 `R1`로 바꾸어 각 판을 검사할 수 있지만, PE1/PE2에는 판과 연결된 실제 입력이 먼저 필요하다.

```bash
: "${AF088_PDF_ENGINE:?Set the confirmed PDF engine after checking its version}"
mkdir -p execution/results
test -f execution/supplied/PN1-rule.lua || exit 3
"$AF088_PANDOC_BIN" -f markdown --pdf-engine "$AF088_PDF_ENGINE" --lua-filter execution/supplied/PN1-rule.lua execution/inputs/PN1/R0-table.md -o execution/results/PN1-R0-filtered.pdf

test -f execution/supplied/PN2-math.lua || exit 3
"$AF088_PANDOC_BIN" -f html -t asciidoc --lua-filter execution/supplied/PN2-math.lua execution/inputs/PN2/R0-formula.html -o execution/results/PN2-R0-filtered.adoc

test -f execution/supplied/PE1-R0-code.md || exit 3
test -f execution/supplied/PE1-template.latex || exit 3
"$AF088_PANDOC_BIN" -f markdown --pdf-engine "$AF088_PDF_ENGINE" --template execution/supplied/PE1-template.latex execution/supplied/PE1-R0-code.md -o execution/results/PE1-R0-template.pdf

test -f execution/supplied/PE1-margin.lua || exit 3
"$AF088_PANDOC_BIN" -f markdown --pdf-engine "$AF088_PDF_ENGINE" --lua-filter execution/supplied/PE1-margin.lua execution/supplied/PE1-R0-code.md -o execution/results/PE1-R0-lua.pdf

test -f execution/supplied/PE2-R0-input.ast.json || exit 3
test -f execution/supplied/PE2-output-fold.lua || exit 3
"$AF088_PANDOC_BIN" -f json -t html --lua-filter execution/supplied/PE2-output-fold.lua execution/supplied/PE2-R0-input.ast.json -o execution/results/PE2-R0-output-fragment.html
```

PE2 마지막 명령의 HTML은 **후속 실험에서 목표 writer를 HTML로 확인한 경우**의 명령이다. 원문에 출력 형식이 명시되지 않았으므로 원래 계약에 소급해 HTML을 확정하지 않는다. 전체 보고서에서의 동작은 별도 렌더링과 열기/닫기 관측이 필요하다. Quarto의 사전 실행 AST 없이 새로 만든 AST는 사용자 실행을 대신하지 않는다.

### PE1 metadata 값의 전달 명령

다중행 LaTeX 값을 셸 재해석 없이 인수 하나로 전달한다. 해당 매크로 파일이 아직 없으므로 이번에 실행하지 않았다. `-t json`은 metadata가 어떻게 읽혔는지를 점검하고, PDF는 실제 시각 결과를 점검한다. 이 명령은 LaTeX 수정을 제공하지 않는다.

```bash
python execution/reproduce.py --require pandoc || exit "$?"
python - <<'PY'
import os
from pathlib import Path
import subprocess

binary = os.environ['AF088_PANDOC_BIN']
assert os.environ.get('AF088_PDF_ENGINE'), 'Confirmed PDF engine required'
Path('execution/results').mkdir(parents=True, exist_ok=True)
source = Path('execution/supplied/PE1-R0-code.md')
header = Path('execution/supplied/PE1-header-includes.txt')
if not source.is_file() or not header.is_file():
    raise SystemExit('Missing original Markdown or supplied LaTeX header; no run performed.')
metadata_argument = 'header-includes=' + header.read_text()
common = [binary, '-f', 'markdown', '--metadata', metadata_argument, str(source)]
subprocess.run(common + ['-t', 'json', '-o', 'execution/results/PE1-R0-metadata.ast.json'], check=True)
subprocess.run(common + ['--pdf-engine', os.environ['AF088_PDF_ENGINE'], '-o', 'execution/results/PE1-R0-metadata.pdf'], check=True)
PY
```

### 반드시 남길 실행행

실행시각 UTC, 바이너리 버전·SHA·빌드 출처, 입력·추가 코드·매크로·템플릿 SHA, 명령의 argv, stdout/stderr, 종료값, 생성 AST/문서의 SHA를 보존한다. PDF 검사는 실제 엔진판·폰트·페이지 크기·마진, 확인한 페이지와 번호 영역도 연결한다. `--version` 관측, JSON 파싱, AST 관측, PDF/HTML 시각 관측, 질문자의 실제 실행은 서로 다른 증거 수준이다.

## 근거 연결과 판단을 바꿀 다음 입력

후보 동작·허용 코드의 출발점은 `../candidates.csv`의 동일 태그 절이다. jq input 전제는 [고정 jq 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L78-L129), Pandoc 네 옵션은 [고정 MANUAL](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt)에 있다. PE1의 생성 경로는 [default.latex L249–251 및 L397–399](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/data/templates/default.latex#L249-L251), [LaTeX writer L221–227](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Writers/LaTeX.hs#L221-L227), [Highlighting L81–100](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/src/Text/Pandoc/Highlighting.hs#L81-L100)로 거슬러 갈 수 있다. 이 연결은 매크로가 생성·삽입되는 위치의 근거이며 수정 성공 코드의 근거는 아니다.

가장 작은 다음 실행은 정확판 jq 바이너리를 확보한 후 `--run-jn1`로 R1의 두 배열을 확인하는 것이다. 이는 문서상 충족의 실행 보강이며 R0 최초 게시 입력이나 실제 사용판의 결손을 메우지 않는다. 여섯 미확인은 표의 코드·입력·AST·writer 관측이 모두 연결될 때만 재판정한다. 특히 PE1의 전체 Markdown과 PE2의 실행 후 AST가 없으면 옵션의 표현력만으로 완료를 선언할 수 없다.
