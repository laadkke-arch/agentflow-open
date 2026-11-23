# AF-RES-100 — 봉인② 이후 독립 의미 검토

**결론: 봉인된 주 해석에서 32자리의 완결 판정을 바꿀 근거는 확인하지 못했다.** F의 B만 1·양쪽 4·모두미완결 2·비교불가 1, S의 모두미완결 7·비교불가 1을 유지한다. 다만 유일한 B 이득인 P1은 **helper 허용**과 **현재 Pandoc 태그로 모집한 요청**이라는 조건에 의존한다. 내장 option 또는 기존 namespace-qualified 호출 불변만 허용하면 그 이득은 사라진다. 이는 사전 등록된 해석의 민감도이며, 사후 답을 보고 추가한 새 요구가 아니다.

## 검토의 지위와 범위

- 대상: `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`의 protocol, packets, judgments, pairs 및 사전 근거 가용성 감사.
- 검토자: `/root/dependency_audit`, 별도 모델 문맥. 사람이 실제 검토한 것으로 쓰지 않는다.
- 봉인② 이후 정책·판정을 먼저 읽은 의미 검토다. 독립 맹검 발견이나 최초 독자의 결과가 아니다.
- 이 문맥에서는 신규 여덟 질문의 최초 revision만 읽었으며 답·댓글·채택·후속을 열지 않았다. 다른 문맥의 후속 노출 여부를 대신 보증하지 않는다.
- 모든 S 패킷의 실제 노출 구간, F 완결 9자리의 핵심 근거, J3의 Bash 경계 및 P1의 A 대안을 직접 읽었다. 원 질문 여덟 개의 캐시 해시는 봉인 값과 일치한다.
- 검토 중 실제 시계 관측: `2026-11-23T20:31:20+00:00`. 보고서 기록시각: `2026-11-23T20:34:37.519254+00:00`. 최초 열람의 정확한 시작시각은 별도 기록하지 않았으므로 만들어 넣지 않았다.
- 봉인 judgments/access/packets를 수정하지 않았고, 실행 성공을 추가하지 않았다. 원 문서 구간과 원장 해시·바이트 검산은 `semantic-review.json`에 있다.

## 사례별 판단

| 사례 | F 판단 유지 이유 | S에서 빠진 것 / 의미 한계 |
| --- | --- | --- |
| J1 | debug(msgs)의 값 보존, input 경계, INDEX/JOIN 정의가 구체적인 다음 진단 행동을 지지한다. 두 제안 모두 원 INDEX 내부 쉼표를 유지한다. | S에 실제 debug 및 INDEX/JOIN 정의가 없다. F 완결은 유일 원인·최종 JOIN 결과를 뜻하지 않는다. |
| J2 | map·동일 원소의 Name/content·from_entries·update-assignment·결손키 null이 변환을 지지한다. 원문이 `.Event[]`를 직접 지명한다. | 출력 예시의 루트와 전체 envelope가 일치하는지는 미확인이다. 두 답 모두 경계별 대안을 조건부로 적었다. 원 파이프라인의 무조건 실행 가능성을 주장하면 과장이다. S는 부분 인덱싱/null까지만 보인다. |
| J3 | C1은 지지되나 Bash 변수확장과 `.new` 리다이렉션 경계의 근거가 없어 C2 부분, 양쪽 미완결 유지. | jq의 `--argjson` 소비 의미와 shell이 실제 argv를 만드는 규칙은 다르다. Terminal 문서의 bash 명명만으로 결손을 채우지 않는다. |
| J4 | 같은 volume 문맥의 sibling과 괄호 안 Tags 선택을 결합하며, 없는 Iops는 null로 남긴다. | S는 출력 형식/무관 C 구간 및 AWS 예시를 보일 뿐 jq의 전체 변환을 지지하지 않는다. 예시 AWS Iops를 원 입력으로 복사하지 않는다. |
| P1 | B의 R 함수 구현은 전역 선호 확장자→존재하는 대체 경로→실제 include_graphics 인수를 연결한다. A는 downstream Image.src 가능성까지만 제공한다. | B-S는 generated plot용 dev2ext만 노출한다. helper 호출명 변경이 필요하며 기존 `knitr::include_graphics`를 자동 가로채지 않는다. |
| P2 | 실제 CeTZ import를 유지하면서 같은 Markdown을 만드는 해결 경로가 확보되지 않았다. | Typst compile 성공·일반 변환 소개·다른 CeTZ 판은 원 Pandoc import 해결이 아니다. |
| P3 | 컨테이너 script/entrypoint/의존 설치 경계가 비어 있다. | B의 두 공석과 안정판 미고정으로 비교불가를 유지한다. 실패 두 건으로 분모에 넣지 않는다. |
| P4 | 매뉴얼이 colon을 포함한 title을 인용부호로 감싸는 정확한 예를 제공하며, filter는 parsing 이후다. | S에는 해당 YAML 규칙이 없다. F는 입력 parse 수정이며 전체 PDF 또는 원 Pandoc 2.18 실행을 입증하지 않는다. |

## P1의 유일 B 이득을 반증하려고 확인한 내용

[최초 요청](https://stackoverflow.com/revisions/32603E8D-E453-4BCB-895B-83AFBE3FB468/view-source)의 HTML payload 문자·바이트 `[0,364)`는 기본 외부 그래픽 선택을, `[569,864)`는 Rmd setup와 namespace-qualified 호출을 담는다. 봉인 protocol의 주 해석은 전역 설정 또는 한 번 정의한 helper를 허용하고, native option만 허용하는 읽기는 민감도로 분리했다.

[B의 knitr plot.R](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R) 문자=바이트 `[13900,18600)`는 path 벡터 인수, R chunk에서의 사용, PDF-only 자동 대체, 존재 검사, output별 마크업을 위한 반환 클래스를 직접 보인다. helper가 고른 경로를 `knitr::include_graphics(path, auto_pdf=FALSE)`로 전달하는 연결은 이 근거로 지지된다. [hooks-latex.R](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/hooks-latex.R) `[7662,8178)`는 sub/sprintf 파일명 조합의 구현 맥락을 제공한다. helper는 연구자의 파생 구성이고 내장 SVG/EMF option이라는 주장이 아니다.

검토한 핵심 반례는 **helper를 정의만 하고 기존 호출을 그대로 두는 경우**다. 그때 동작하지 않는다. 봉인 답은 이 문제를 이미 명시하고 실제 호출을 `include_preferred_graphics("external_figure.jpg")`로 바꾼다. 호출마다 파일 확장자를 수동으로 고치는 방식과는 다르지만 기존 코드에 호출명 변경이 필요하다는 비용을 반환표에 남겨야 한다. 대체 SVG/EMF 실물 파일은 없고, 미존재 시 원 경로 유지까지 명시되므로 선택 가능성의 문서 근거를 실제 파일 선택·PowerPoint 렌더링 성공으로 쓰면 안 된다.

A의 [Lua 문서](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md)는 등록 `[2630,3145)`, FORMAT 문자 `[8857,9115)`/바이트 `[8858,9116)`, Image.src 문자 `[40888,41164)`/바이트 `[40911,41187)`를 제공한다. [PowerPoint writer](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Writers/Powerpoint/Output.hs) `[37330,37731)`는 SVG/EMF 타입 인식을 보인다. 그러나 이 사실만으로 Rmd에 필터를 연결하거나 원 include_graphics 인수를 바꾸었다고 할 수 없다. 네 A 파일의 knitr/include_graphics/rmarkdown 명명 검색에서도 그 연결을 찾지 못했다. 이 검색 실패를 모든 가능한 A 해법의 부재 증명으로 표현하지 않는다.

B-S의 plot.R `[0,1200)`는 dev2ext이고 실제 include_graphics 구간은 밖에 있다. F에서 읽은 함수 지식을 S의 지원 근거로 빌려 쓰지 않았다.

## J2의 원 envelope와 다른 완결들의 한계

[원 J2](https://stackoverflow.com/revisions/77962A23-F898-4295-99B6-0CD81D12DEAF/view-source)는 HTML `[263,511)`에 `.Events` 출력 파이프라인, `[601,2345)`에 부분 event 객체, `[2346,3065)`에 `.Event[].EventData.Data[]` 경로를 쓴다. 따라서 경로는 전적으로 연구자가 만든 것이 아니지만 전체 루트를 확정할 자료도 없다. [jq manual](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/docs/content/manual/v1.7/manual.yml)의 `[16161,17386)` missing-key null, `[26075,28280)` 객체 필드 결합, `[37458,39500)` map, `[43318,45400)` from_entries, 문자 `[129714,131902)`/바이트 `[129716,131904)` update-assignment가 **명시한 구조에서의 변환**을 지지한다. 전역 원 입력을 연구자 예제로 메운 것은 아니므로 주 판정은 유지하되, 단일 무조건 명령이나 전체 원 파이프라인 실행까지는 지원되지 않는다.

J1의 같은 manual 문자 `[123208,125480)`/바이트 `[123210,125482)`, [builtin.jq](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.jq) `[10173,10903)`, [builtin.c](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/builtin.c) `[38482,39160)`는 diagnostic lead를 지지한다. 원 두 파일 없이 정확 오류 원인이나 올바른 결과가 입증되지는 않는다.

J3의 manual `[3325,4597)`는 jq 프로그램의 shell quoting, `[9370,10420)`는 arg/argjson/slurpfile 의미이며, [main.c](https://github.com/jqlang/jq/blob/71c2ab509a8628dbbad4bc7b3f98a64aa90d3297/src/main.c) `[17844,18754)`는 argv 한 원소를 JSON으로 읽는다. 이 내용으로 Bash의 JSON 변수 word splitting·인용·변수 출력경로가 모두 입증되었다고 확대하지 않았다.

P4의 [Pandoc manual](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt) 문자 `[188838,193650)`/바이트 `[188847,193659)`는 정확한 YAML title 규칙을 담는다. 전체 PDF 실행 의존을 배제한 봉인된 parse 요구에서는 완결 유지가 타당하다.

## 32자리 검토 결과

| 사례 | 정책 | 읽기 | 패킷 | 봉인 완결 | 검토 |
| --- | --- | --- | --- | --- | --- |
| J1 | A | F | `cc86f215a28e` | 예 | 유지 |
| J1 | A | S | `28483f232965` | 아니오 | 유지 |
| J1 | B | F | `2f20d4696820` | 예 | 유지 |
| J1 | B | S | `90c5d90f8abc` | 아니오 | 유지 |
| J2 | A | F | `b6aad97ea044` | 예 | 유지 |
| J2 | A | S | `3ea1130ebcab` | 아니오 | 유지 |
| J2 | B | F | `14f044b30814` | 예 | 유지 |
| J2 | B | S | `2d1378170a3d` | 아니오 | 유지 |
| J3 | A | F | `a13997d37fef` | 아니오 | 유지 |
| J3 | A | S | `8591724781d4` | 아니오 | 유지 |
| J3 | B | F | `0be2a4830a4c` | 아니오 | 유지 |
| J3 | B | S | `a76ec0d77f82` | 아니오 | 유지 |
| J4 | A | F | `a0007d0fb17a` | 예 | 유지 |
| J4 | A | S | `d018c8051020` | 아니오 | 유지 |
| J4 | B | F | `837da1ed6706` | 예 | 유지 |
| J4 | B | S | `a032f9aa185e` | 아니오 | 유지 |
| P1 | A | F | `523094dc11e7` | 아니오 | 유지 |
| P1 | A | S | `932ed36d42d8` | 아니오 | 유지 |
| P1 | B | F | `2c39a224e483` | 예 | 유지 |
| P1 | B | S | `edb07d55ddaf` | 아니오 | 유지 |
| P2 | A | F | `169dbf5f4342` | 아니오 | 유지 |
| P2 | A | S | `2f55c804a8f3` | 아니오 | 유지 |
| P2 | B | F | `7e9b0eaaaf03` | 아니오 | 유지 |
| P2 | B | S | `342eea14f081` | 아니오 | 유지 |
| P3 | A | F | `c0b7629f5619` | 아니오 | 유지 |
| P3 | A | S | `78178fae9374` | 아니오 | 유지 |
| P3 | B | F | `5480c02357ef` | 아니오 | 유지 |
| P3 | B | S | `09c26140214f` | 아니오 | 유지 |
| P4 | A | F | `ac9beb264939` | 예 | 유지 |
| P4 | A | S | `4b6da2f3c82a` | 아니오 | 유지 |
| P4 | B | F | `529295ca2f71` | 예 | 유지 |
| P4 | B | S | `3092b6d907de` | 아니오 | 유지 |

## 민감도와 판정 변경 조건

| 읽기 | F A만 / B만 / 양쪽 / 모두미완결 / 비교불가 | 의미 |
| --- | --- | --- |
| 봉인된 주 해석 | 0 / 1 / 4 / 2 / 1 | 비교가능 7쌍, 경계 5쌍. |
| P1 native option 또는 기존 namespace-qualified 호출 불변만 허용 | 0 / 0 / 4 / 3 / 1 | 유일한 단독완결 이득이 사라짐. 주 판정을 덮어쓰지 않는다. |
| Pandoc이 R0에 없는 P1을 분석에서 제외 | 0 / 0 / 4 / 2 / 1 | 비교가능 6쌍. 이것은 모집 범위의 민감도다. |

S는 위 조건에서도 성공으로 승격되는 패킷이 없으며, 각 정책의 성공 0을 일반 정책 동등성으로 해석하지 않는다. S가 다른 anchoring을 사용했다면 결과가 달라질 수 있지만 이번 고정 구간을 사후 바꾸지 않는다.

전체 원장 인용 115건을 원 파일의 문자·UTF-8 바이트·패킷 범위에 대조한 오류는 0건이다. 이는 위치 검산이며 문서 해석의 참, 독자의 이해, 원 사용자 실행을 자동 보증하지 않는다. 이 의미 검토가 권고하는 주 판정 변경은 0건이다.
