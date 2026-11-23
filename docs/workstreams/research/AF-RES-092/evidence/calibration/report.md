# Q6 · 결과를 알고 시작한 별도 교정 3건

이 세 건은 AF-RES-088의 알려진 채택 주해법을 받은 뒤 판독했다. 신규 여섯 질문, 12개 경로, 6대응쌍, 동일 예산 승률에 **포함하지 않는다**. 이 파일의 원자료도 최소 26건을 보충하지 않는다. 신규 사전판정 원격 봉인 `a04fbb20ca1a415235f69a1018a93e07e7adc926` 이후 수행했다.

선행 `e173b53f071aabfa749d33ab7da7ce970d5641b5`의 RESULT와 인수 SCOPE/candidates/frame/pairs/metrics/evidence_corrections를 읽었다. 전후 64판정을 다시 만들거나 채점하지 않았다. 개설시각 바이트, PE1 이미지, 고정 바이너리 변환 시험은 조사·실행하지 않았다. 원 답 최초판은 해당 커밋의 짧은 보존 HTML을 읽었고, 직접 revision 웹 재열람은 DisabledError라 새 공개답 확인으로 세지 않았다.

## 교정 표

| 사례·알고 시작한 결과 | 주 도구 전체 매뉴얼에서 발견 가능한가 | 실제 인접 단계 관계 | 반환 정책 | 반례·한계 |
| --- | --- | --- | --- | --- |
| **JN2** — [R0 78262117](https://stackoverflow.com/revisions/78262117/1)의 Helm YAML에서 version 추출. 알려진 [채택 답 78266023](https://stackoverflow.com/revisions/78266023/1)은 **mikefarah/yq**로 명령을 교체한다. | jq 1.7.1은 기본 JSON 입력, `-R` 문자열 입력, 필드 조회와 `capture`를 문서화한다. 정규식으로 보이는 특정 행을 뽑는 것은 가능 후보지만, **일반 YAML 파서나 yq 해법이 매뉴얼 안에 있다고 확인되지는 않는다**. YAML을 문자열로 받는 것과 YAML 구조를 파싱하는 것은 다르다. [고정 jq 매뉴얼 L50–54,124–129,408–413,2635–2645](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml#L50-L54) | `Helm → YAML → 파싱/조회` 경계는 원 입력이 지지한다. yq는 앞단 YAML→JSON 어댑터로도 쓸 수 있지만 채택 답은 **jq의 자리를 대체**한다. yq 한 프로그램이 파싱과 필드 조회를 함께 하므로 반드시 둘을 조립할 필요는 없다. [고정 yq README](https://github.com/mikefarah/yq/blob/c35ec752e38ea0c096d3c44e13cfc0797ac394d8/README.md#quick-usage-guide) | JSON 전체를 다음 단계에 넘겨야 하는지, version 값 하나만 필요한지 한 가지를 묻는다. 값 하나면 yq 필드조회 한 링크. 기존 jq 처리가 이어져야 하면 yq JSON 출력 + jq 필드조회 두 링크와 중간 JSON 계약을 제시한다. | 채택 답의 `yq .`은 필드 선택을 하지 않는다. 고정 yq 문서의 기본 출력은 YAML이므로 그 명령만으로 JSON 출력까지 입증했다고 쓰면 틀린다. 사용자 yq판·설치·실제 출력은 미확인. 단순한 한 행 입력만 보장되면 jq raw/정규식 경로가 충분할 반례도 남는다. |
| **PN1** — [R0 78258237](https://stackoverflow.com/revisions/78258237/1), 연속 중간선과 헤더선과 같은 굵기/색. 알려진 [채택 답 78260959](https://stackoverflow.com/revisions/78260959/1)은 grid-table footer이며 Pandoc 3 이상을 요구한다. | **주된 구조 기능은 발견 가능하다.** Pandoc 3.1.11의 `grid_tables` 절이 footer를 `=` 구분선으로 둘러싸는 방법을 직접 설명한다. 네 옵션 후보 밖이라는 사실이 Pandoc 전체 문서 밖이라는 뜻은 아니다. [고정 매뉴얼 L4465–4540](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt#L4465-L4540) | pipe table→grid table은 **주 도구 reader가 받는 입력 문법 선택**이다. 별도 인접 도구를 발견한 사례가 아니다. LaTeX/PDF 출력에서는 writer·엔진이 뒤따르지만, grid_tables라는 해법 자체는 주 도구 안이다. | 우선 매뉴얼 한 링크와 “실제 판이 3 이상인가, 2.9.2.1에 머무는가”를 묻는다. 원 사용판을 유지하면 해당 새 기능을 완결 답으로 반환하지 않는다. | 질문자의 자기보고판은 2.9.2.1, 연구판은 3.1.11이다. footer 구조 지원은 문서로 확인했지만 원 입력에서 요구한 모든 선의 굵기·색을 측정한 새 출력은 없다. 채택 뒤 댓글은 다음 작업에 사용할 계획이며 즉시 성공 실행으로 승격하지 않는다. |
| **PE1** — [R0 78300525](https://stackoverflow.com/revisions/78300525/1)의 코드 줄 번호 여백. 알려진 [채택 답 78302381](https://stackoverflow.com/revisions/78302381/1)은 raw LaTeX로 `Highlighting` 환경의 `xleftmargin`을 설정한다. | **raw LaTeX 전달 경로는 발견 가능**, 정확한 여백 해법 완성은 미확인이다. 매뉴얼 `raw_tex`/`raw_attribute`가 원문 통과와 목표 출력 형식 일치를 설명하고 fancyvrb도 PDF 의존 패키지로 연결한다. 그러나 같은 MANUAL.txt 전체에서 `xleftmargin`은 찾지 못했다. [L5139–5208](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt#L5139-L5208) | raw 삽입은 **Pandoc 자체 기능**이고, 그 바이트를 해석하는 LaTeX/fancyvrb는 실제 뒤 소비자다. 두 층을 분리해야 한다. 새 변환기를 도입했다는 사례로 볼 수 없고, 이미 사용하는 소비자의 설정을 바꾸는 경로다. | raw 전달 매뉴얼 한 링크만으로 수치 여백 성공을 보증하지 않는다. LaTeX 기반 PDF인가를 먼저 묻고, 맞으면 raw 문법과 fancyvrb 문서를 연결하되 정확판·환경·설정의 효력을 미확인으로 표시한다. [공식 fancyvrb 진입점](https://ctan.org/pkg/fancyvrb)은 선행 답/매뉴얼에 있는 연결이며 이번 교정에서 본문을 새로 열지 않았다. | HTML 기반 PDF나 다른 writer에는 같은 raw 바이트가 맞지 않는다. 18pt라는 값은 채택 답의 조정 예시이지 모든 문서의 정답이 아니다. 실제 엔진·환경 및 성공 출력은 미확인이고 PE1 이미지 결손도 그대로다. |

## 판 고정과 직접 확인 범위

- jq: `jq-1.7.1` → `71c2ab509a8628dbbad4bc7b3f98a64aa90d3297`; `docs/content/manual/v1.7/manual.yml` 원 파일을 열었다.
- Pandoc: `3.1.11` → `c3038dcd54152c4e18e49db31676b79ee7cc29b2`; `MANUAL.txt`와 `data/templates/default.latex`를 열었다. 템플릿 L249–251의 highlighting-macros 및 L397–399의 header-includes 삽입을 확인했다. 이는 LaTeX 환경 재정의의 실제 성공을 측정한 것이 아니다. 선행의 MAN-06/HTML5 잘못된 대응 대신 **MAN-10/default.latex**라는 정정도 인수했다.
- yq: [v4.43.1](https://github.com/mikefarah/yq/releases/tag/v4.43.1), 공개 `2024-03-24T00:17:31Z`, 커밋 `c35ec752e38ea0c096d3c44e13cfc0797ac394d8`. JN2 R0 이전 공개 안정판을 교정 참조판으로 사용했다. 원 질문자가 이 판을 썼다는 뜻은 아니다. README L6–19와 L366–369는 각각 YAML 처리·필드조회와 출력 형식/기본값을 명시한다.

문서에서 구성한 조건부 예는 `helm show chart CHART | yq -o=json '.' | jq -r '.version'`이다. 앞 단계는 YAML을 JSON으로 내보내고 뒤는 JSON 객체의 version을 읽는다. 이는 **이번에 실행한 명령이 아니다**. 실제 목적이 값 하나라면 yq에서 직접 `.version`을 조회할 수 있어 jq 결합을 추가할 필요가 없을 수 있다. 반대로 고정 원문 모양에 대한 jq `-R`+정규식 해결은 quoting, comments, nested keys, YAML aliases 같은 입력 변화에 안전한 일반 파싱을 입증하지 않는다.

## 이 교정으로 바꿀 해석

“풀 밖 채택 = 인접 단계 확장의 승리”는 세 건을 설명하지 못한다. PN1은 주 도구 문서의 후보 범위를 넓히는 것만으로 구조 기능이 나온다. PE1은 주 도구의 전달 기능과 소비자의 배치 의미를 연결해야 한다. JN2는 형식 경계를 바로잡지만 단일 대체 도구가 두 일을 수행하므로 두 링크 조립이 항상 더 낫지 않다.

그렇다고 “전체 매뉴얼이면 언제나 충분하다”도 지지되지 않는다. PN1의 사용자 판 차이, PE1의 미제공 여백 파라미터, JN2의 YAML 해석과 JSON/값 출력 목적은 링크를 찾은 뒤에도 남는다. 다음 최소 관측은 각각 **허용되는 출력 형식**, **실제 Pandoc판**, **PDF engine/Highlighting 구성**이다. 이 세 교정의 승률은 산출하지 않는다.

## 원장·실패 경로

`sources.jsonl`의 모든 행은 `counted_minimum=false`다. `receipts.json`에는 실제 열람 UTC, 고정 원문 해시, 검색한 절과 API 판 확인값이 있다. SO revision 3개와 GitHub 웹 화면 2개의 웹 도구 재열람은 DisabledError였고 jq/Pandoc은 공식 raw URL로 직접 확인했다. yq의 추정 `doc/usage/convert.md` 경로는 404여서 근거로 쓰지 않았으며 README의 공식 출력 옵션을 사용했다. 선행 보존 답을 현재 공개답으로 재확인했다고 표시하지 않았다.
