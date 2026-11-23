# AF-RES-088 재개: 고정 후보·미확인 입력 감사

확인: 2026-11-23 15:35–15:37 UTC. 담당: `resume_gaps`. 이 검토는 같은 연구팀의 재개 검토이며 독립 맹검 의미 판독이 아니다. 모집, R0/R1의 64판정, 32쌍을 수정하지 않았다. 기존 결과 커밋은 `f048885abfbfcca1ffd8840899bf2911cd35da60`이다.

## 결론

두 태그 SHA와 여덟 후보의 고정 원문 절은 재확인했다. 자료 링크나 태그가 없어서 생긴 결손은 아니다. 남은 핵심 결손은 **PE1의 옛 이미지 내용**과 **여섯 Pandoc 후보의 구체적인 코드·입력·출력 조건**이다. 이 검토에서 해결 성공이나 공개판의 완전한 시각 동등성을 추가로 확인하지 못했다. 문서상 26확정+6미확인이라는 기존 구분과 PARTIAL을 유지하는 데 반대 근거를 찾지 못했다. 이 판단은 다른 Q의 완료 여부를 대신 검사한 결과가 아니다.

## 1. 원문·태그 재열람

일반 공개 raw URL로 네 원문을 직접 가져와 아래 절을 읽었다. 재열람이므로 원자료와 독립 사건 최소량에 **0개**를 더한다. `sources.jsonl`에는 기존 MAN ID와 같은 사건 ID를 사용하고 `count_primary=false`를 넣었다. 전송 시작 시각, 응답 상태, 전체 파일 SHA-256은 `fetch_receipts.jsonl`에 있다. 장문 복제는 남기지 않고 읽은 범위·요약과 고정 원문 위치를 보존한다.

| 원문 | 확인 범위 | 재확인한 내용·한계 |
| --- | --- | --- |
| [jq-1.7.1 매뉴얼](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml) | L78–89, L989–1049, L1182–1198, L1510–1571 | 입력 JSON 파싱이 필터보다 앞선다. map은 결과 배열을 만들고 출력 길이가 달라질 수 있다. select는 통과시킨 값을 유지한다. sort_by와 group_by는 배열을 재배열·묶는다. 이는 질문자의 실행판이나 완전한 R0 입력 증거가 아니다. |
| [Pandoc 3.1.11 MANUAL](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/MANUAL.txt) | L623–658, L744–762, L2131–2167 | Lua는 변환 함수를 담은 스크립트를 요구한다. metadata 값은 파싱 및 템플릿 삽입 시 escaping을 거친다. template은 standalone을 암묵적으로 켜며 PDF에는 standalone이 자동이다. docx/pptx에는 template이 없다. 옵션 설명만으로 사례의 성공 구현을 확정할 수 없다. |
| [같은 판 Lua guide](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/doc/lua-filters.md) | L1–180, 특히 L11–18, L38–63, L112–128 | AST의 파싱 이후·쓰기 이전에 작동한다. 명시한 Strong→SmallCaps 코드는 구체적인 변환의 예다. handler는 inline/block의 반환 타입 제약을 지켜야 한다. 다른 요구에 같은 옵션만 붙인 성공을 뜻하지 않는다. |
| [같은 판 default.latex](https://github.com/jgm/pandoc/blob/c3038dcd54152c4e18e49db31676b79ee7cc29b2/data/templates/default.latex) | L241–256, L390–403 | L249–251에 highlighting 매크로, L397–399에 header-includes가 삽입된다. 삽입 위치 자체는 줄번호를 옮기는 코드·raw metadata 전달·PDF 결과의 증거가 아니다. |

`git ls-remote`도 두 태그와 peel ref를 다시 조회했다. 종료값은 각각 0이며 반환 SHA는 계약과 같다. 응답 원문은 `tag_jq.json`, `tag_pandoc.json`이다.

- jq-1.7.1: `71c2ab509a8628dbbad4bc7b3f98a64aa90d3297`
- Pandoc 3.1.11: `c3038dcd54152c4e18e49db31676b79ee7cc29b2`

GitHub 웹 본문은 이번에도 DisabledError였으나 일반 raw 원문 요청은 HTTP 200이었다. 실패를 성공 자료 수에 넣지 않았다.

## 2. PE1 이미지 결손

`revisions.jsonl`을 읽어 PE1이 **78300525**임을 먼저 확인했다. R0 GUID는 `DAD692BA-D95F-4262-8B83-C762CF15C4A9`, R1 GUID는 `06E686FC-FB2D-4E3B-836C-7CA2CF31DB4E`다. 이력에 있는 이미지 URL만 사용했다.

| 공개 원주소 | 이번 결과 | 비교에 남는 결손 |
| --- | --- | --- |
| https://i.sstatic.net/A0Wtm.png | 웹 접근불가, 셸 HTTP 403/1010 | R0 이미지 바이트·번호 위치·추가 단서 미확인 |
| https://i.stack.imgur.com/A0Wtm.png | 셸 HTTP 403/1010 | 알려진 과거 호스트로도 R0 원이미지 미확보 |
| https://i.sstatic.net/yQDJv.jpg | 웹 접근불가, 셸 HTTP 403/1010 | 작성자가 바꾼 중간판의 시각 내용 미확인 |
| https://i.sstatic.net/avk9k.png | 웹은 이미지 표시 항목을 반환, 셸 HTTP 403/1010 | 이번 감사자는 원 바이트를 얻거나 독립 pixel 비교를 하지 못했다. 기존 root의 R1 관측을 새로운 독립 관측으로 세지 않는다. |

차단 우회나 추측 URL 대량 탐색은 하지 않았다. 실제 원이미지를 확보하지 못했으므로 빈 이미지 파일이나 합성 이미지도 만들지 않았다. `text_requirement_change=false`와 `full_input_information_change=unknown`을 구분한 기존 후속 정정은 타당하다. 옛 이미지의 문서 폭·번호 자릿수·추가 예제가 달랐다면 같은 텍스트에서도 반환할 조건이 바뀔 수 있다. 다음 최소 입력은 이 세 URL과 공개판 시각에 연결되는 보존 이미지 바이트와 해시다.

## 3. 여섯 미확인의 성격

| 후보쌍 | 공식 절에서 확인한 범위 | 아직 필요한 최소 관측 |
| --- | --- | --- |
| PN1 / lua-filter | Table/블록 처리 경로와 유효한 handler 반환 타입 | 원 표 AST, 규칙을 만드는 실제 handler, 선택한 PDF 엔진, 원문의 선 위치·연속성·굵기·색을 비교한 출력 |
| PN2 / lua-filter | 파싱 뒤 AST 변환 경로 | 같은 HTML reader AST에 수식 관계가 남는지, Math handler, 원 수식과 같은 AsciiDoc STEM 결과 |
| PE1 / metadata | metadata와 default.latex의 삽입점 | 실제 LaTeX 값의 파싱·escaping 결과, 전체 Markdown, highlighting 환경·엔진, 줄번호/코드 보존 출력 |
| PE1 / template | 사용자 template와 암묵적 standalone | 구체적 template 변경, 생성 매크로의 작동 순서, 같은 전체 입력·엔진에서의 번호 위치 |
| PE1 / lua-filter | CodeBlock 또는 문서 AST 변환 경로 | 번호·언어 속성, 구체적 handler, 전체 문서와 PDF 결과 |
| PE2 / lua-filter | AST를 감싸거나 변경하는 handler 경로 | 목표 writer, 실제 Quarto 실행 뒤 코드·출력을 구분한 AST, handler, 기본 접힘·펼침 관측 |

여기서 `조건부`는 필요한 자료를 붙여 검토할 **경로**다. 조건을 만족하면 반드시 성공한다고 입증된 정답이 아니다. 원문만으로 실패를 명시 반박한 상태도 아니며, 임의 코드를 새로 만들어 성공한 뒤 질문자의 당시 환경에서 성공했다고 쓸 수 없다. 특히 PE1은 코드 속성만 있고 전체 Markdown이 없고, PE2의 .qmd 조각은 실행 뒤 Pandoc AST가 아니다.

## 4. 실행 인계 검토

`execution/reproduce.py`와 `execution/extract_inputs.py`를 읽은 뒤 변환 없는 검사만 실시했다.

| 검사 | 종료값·관측 | 한계 |
| --- | --- | --- |
| `python execution/extract_inputs.py --check` | 0, 인덱스 포함 38파일 일치 | 저장 HTML에서의 추출 일치다. 최초 게시 Markdown 바이트나 변환 성공을 확인하지 않는다. |
| `python execution/reproduce.py --preflight` | 2, jq 1.7 / Pandoc 3.1.11.1 | 두 판 모두 계약의 1.7.1 / 3.1.11과 다르다. 변환 실행 0회이며 설치·바이너리 다운로드도 하지 않았다. |

명령은 저장소 루트에서 전체 상대경로로 실행했고 stdout·종료값은 `extraction_check.json`, `preflight.json`에 남겼다. 실제 jq 두 배열 실행이나 Pandoc AST/PDF 변환을 한 것으로 세지 않는다. 테스트 스크립트의 정확판 gate는 변환 전 중단하므로 계약 보존에 적합하다.

인계 명령에는 작은 보완을 권고한다. PDF 결과를 비교할 때는 먼저 실제 엔진 이름·버전이 입력으로 제공되어야 한다. `execution/README.md`의 설명에는 이 조건이 있지만 예시 명령은 기본 엔진을 선택한다. 후속 담당자는 `AF088_PDF_ENGINE`을 확인된 이름으로 설정하고 `--pdf-engine "$AF088_PDF_ENGINE"`를 추가하여 선택을 명시하면 재현 입력이 분명해진다. 이는 고정 후보를 추가하는 것이 아니라 이미 요구된 실행환경을 고정하는 것이다. 별도 명령 블록만 실행할 때는 `mkdir -p execution/results`도 먼저 해야 한다. 원 요구에 엔진이 없는 상황을 임의 기본값으로 채우고 검증 완료로 삼아서는 안 된다.

## 5. 출처 ID 정정 제안

PE1의 세 미확인 행은 `manual_additional_urls`에 올바른 default.latex 고정 주소를 포함한다. 다만 `manual_source_ids`가 주로 `MAN-02;MAN-06` 등을 가리키며 MAN-06은 HTML5 template이다. default.latex의 직접 대응 ID는 **MAN-10**, 생성 경로 보강은 **MAN-11/12**다. URL 근거는 이미 있으므로 판정이나 수치의 오류는 아니다. 후속 설명에서 이 대응을 명시하되 R0 판정이 처음부터 다른 출처 ID를 가졌던 것처럼 소급해서 쓰지 않는 것이 좋다.

## 권고 상태와 다음 첫 행동

이 감사에서 고정 문서 근거는 재확인됐지만 PE1 시각 결손과 여섯 구체적 구현 결손은 남았다. 연구 PARTIAL, 원래 8자리·32쌍·64행, 확정 비교 26쌍의 범위를 유지한다. 첫 행동은 PE1의 보존 이미지·전체 Markdown을 회수할 수 있는 공개 증거를 확보하는 것이다. 확보되지 않으면 시각 비교는 unknown으로 유지한다. 정확판 바이너리만 확보해 JN1 R1을 실행하는 일은 문서 적합성의 보강이지만 PE1 결손이나 원 질문자의 실사용판 확인을 대신하지 않는다.
