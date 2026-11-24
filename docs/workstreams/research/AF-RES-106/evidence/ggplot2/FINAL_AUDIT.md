# AF-RES-106 ggplot2 사후 판독·재개 검토

봉인판: `8054c2221d4023ba03c904d96f13928219d36c3d`. 재개에서 봉인된 모집단·목적·층·예측을 수정하지 않았다. 이전 미커밋 수신물의 원 HTML·Rd·R·PNG·공식 diff를 직접 다시 읽고 `raw/`에 보존했으며 수신 SHA-256, Git blob, 발행 트리의 blob과 대사했다. 이 문서와 final 원장은 사후 판독이다.

## 1. 주 표본 결과

| 자리 | 예제·고정 본문 | 새판 경로/절 도착 | 원 목적·일반 시각 역할·공개 API | P/G | 판단 근거와 한계 |
|---|---|---|---|---|---|
| GG-A1 | 결원 | 후보 0 | 미확인 | 미확인 | 완전 새 트리에서 옛 대표 외부 경로 부재 후보가 없었다. 음성/유보로 합치지 않는다. |
| GG-A2 | 결원 | 후보 0 | 미확인 | 미확인 | 완전 새 트리에서 옛 대표 외부 경로 부재 후보가 없었다. 음성/유보로 합치지 않는다. |
| GG-M1 | [옛판](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape.html#ref-examples) · [새판](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_shape.html#ref-examples) | 옛 정규화 경로 및 `#ref-examples` 정적 id YES | YES / YES / YES | 참조 자원 P=YES, G=미확인 | 양판 첫 예제는 seed596의 diamonds100행, carat/price, shape=cut 및 순서형 shape 경고를 유지한다. 정확한 R/scale-shape.r→R/scale-shape.R 이동을 Upkeep diff와 현재 @examples로 연결했다. 새 PNG가 해당 절의 첫 img로 직접 참조된다. 양판 대표 PNG sha256은 다르다. 첫 코드 문자열 일치와 직접 이미지 판독은 의미 계승을 보조하지만 당시 생성 실행을 입증하지 않는다. 실제 browser scroll·R 실행 미확인. |
| GG-M2 | [옛판](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_segment.html#ref-examples) · [새판](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/geom_segment.html#ref-examples) | 옛 정규화 경로 및 `#ref-examples` 정적 id YES | YES / YES / YES | 참조 자원 P=YES, G=미확인 | 양판 mtcars wt/mpg 산점도에 같은 한 행 df(2.62,21.0→3.57,15.0)를 사용한 geom_curve와 geom_segment가 있다. R/geom-segment.r→.R은 R100, geom-curve는 include 경로 교정과 함께 제거/추가되어 diff와 rdname/호출로 후계를 확인했다. 양판 대표 PNG sha256은 다르다. 첫 코드 문자열 일치와 직접 이미지 판독은 의미 계승을 보조하지만 당시 생성 실행을 입증하지 않는다. 실제 browser scroll·R 실행 미확인. |
| GG-G1 | [옛판](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/position_jitterdodge.html#ref-examples) · [새판](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/position_jitterdodge.html#ref-examples) | 옛 정규화 경로 및 `#ref-examples` 정적 id YES | YES / YES / YES | 참조 자원 P=YES, G=미확인 | 양판 seed596의 diamonds1000행, cut/carat/clarity, geom_boxplot(outlier.size=0), geom_point(pch=21,position_jitterdodge())가 같다. 새 이미지의 그룹별 상자와 점을 직접 확인했다. 내부 ndodge 계산 변경은 같은 공개 방법의 소멸이 아니다. 양판 대표 PNG sha256은 다르다. 첫 코드 문자열 일치와 직접 이미지 판독은 의미 계승을 보조하지만 당시 생성 실행을 입증하지 않는다. 실제 browser scroll·R 실행 미확인. |
| GG-G2 | [옛판](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_linewidth.html#ref-examples) · [새판](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_linewidth.html#ref-examples) | 옛 정규화 경로 및 `#ref-examples` 정적 id YES | YES / YES / YES | 참조 자원 P=YES, G=미확인 | 양판 economics date/unemploy, linewidth=uempmed, geom_line(lineend="round") 첫 예제가 같다. 시간축 실업자수와 중앙 실업기간의 선 두께를 PNG에서 확인했다. 양판 대표 PNG sha256은 다르다. 첫 코드 문자열 일치와 직접 이미지 판독은 의미 계승을 보조하지만 당시 생성 실행을 입증하지 않는다. 실제 browser scroll·R 실행 미확인. |

주 M층과 G층은 각각 후보 57/11, 주 선택 2/2, TP=2·FP=0·FN=0·TN=0이다. 원 구체 목적·일반 시각 역할·공개 API 세 축 모두 같다. 실제 양성은 층별 2, 음성은 0이므로 **거짓양성률과 특이도는 산출 불가**다. A층은 후보0·자리2 결원이다. 이를 전체 목적 성능4/4나 전수68개 성공률로 일반화하지 않는다.

네 PNG의 경로는 생존하지만 양판 SHA-256은 네 쌍 모두 달랐다. 실제 그림의 축·범례·주요 표식과 첫 코드 및 저자 원 예제를 함께 읽어 계승을 판정했다. 새판에 파일이 있다는 P, 그 절에서 실제 참조된다는 관계, 원 목적 U, 특정 호출 방법, 역사적 빌드 G가 별개라는 원칙이 유지된다. 옛 빌드 조회는 반복하지 않았으며 G는 전부 문자 그대로 미확인이다.

## 2. 정확한 판별 위치·지문

| 사례·판 | HTML Examples 줄·fragment | 실제 대표 PNG 지문 | 예제 소스·지문 |
|---|---|---|---|
| GG-M1 old | [192–224](https://github.com/tidyverse/ggplot2/blob/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape.html#L192) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape-1.png) · `672a89564a27f017105e9a86d7c43e4e36d510da9211c53ca83d6d244966830a` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/63125db184b6e7d5516007574b5d15acbfd8f470/man/scale_shape.Rd) · `dbf49f530f960172f9ae90cd56edab3fdcd36776d5ac3dce8a88aebd0f5face8` |
| GG-M1 new | [205–237](https://github.com/tidyverse/ggplot2/blob/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_shape.html#L205) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_shape-1.png) · `532e6e2bff6baf564c5726ecb71fce0efcc2508e7fe81257db5f680e32d57b9d` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/man/scale_shape.Rd) · `2c74786aea826f4b5a69036a421e2aaab053f05ec39addff1233716953a07417` |
| GG-M2 old | [260–316](https://github.com/tidyverse/ggplot2/blob/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_segment.html#L260) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_segment-1.png) · `e64d7eb79e6426dc205df57736c5c80c94de953bc7d264bc00ce6d4ec8d97aee` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/63125db184b6e7d5516007574b5d15acbfd8f470/man/geom_segment.Rd) · `84d16ed78ba9ac4f4066b86efde0e1c485116a31153d33eea7c04c84fccade37` |
| GG-M2 new | [263–319](https://github.com/tidyverse/ggplot2/blob/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/geom_segment.html#L263) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/geom_segment-1.png) · `0a32844fe54cc8dceb4ad86eacaf229da64a825bdf5c956afb496eae24e4c28b` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/man/geom_segment.Rd) · `91461c07f2e70ab1a481ee8d377f94318fc01d2ae9293ca4b908829804c09551` |
| GG-G1 old | [141–149](https://github.com/tidyverse/ggplot2/blob/57852124c86f770dd443fcf5064d30ea320a4731/reference/position_jitterdodge.html#L141) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/position_jitterdodge-1.png) · `a8d74eab4a46746faafb97d07a02c00db5e532cf6f5a2d15b96cb4d16fe45c4c` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/63125db184b6e7d5516007574b5d15acbfd8f470/man/position_jitterdodge.Rd) · `f8d26a810fdebe05d58432c9444d4310fefd4b64f474f522d22a9671d8ba4135` |
| GG-G1 new | [145–153](https://github.com/tidyverse/ggplot2/blob/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/position_jitterdodge.html#L145) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/position_jitterdodge-1.png) · `b399ae0d3c0011793859ae9ccf38ddf19a60e0342aed8c4383be6e87b05a7edd` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/man/position_jitterdodge.Rd) · `f8d26a810fdebe05d58432c9444d4310fefd4b64f474f522d22a9671d8ba4135` |
| GG-G2 old | [206–221](https://github.com/tidyverse/ggplot2/blob/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_linewidth.html#L206) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_linewidth-1.png) · `6b91070d4d6c0f1cf33dee5a88e86cd555cfa37d87a3bd58d234b82a60b4f78c` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/63125db184b6e7d5516007574b5d15acbfd8f470/man/scale_linewidth.Rd) · `04b3b90a144da6598c04e4e2c98be918549242b34324400027d97a562b14b0b3` |
| GG-G2 new | [222–237](https://github.com/tidyverse/ggplot2/blob/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_linewidth.html#L222) · `#ref-examples` | [PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_linewidth-1.png) · `be04677d1f70ad1c36707acefe09bdac4b00f5dd9385d343e84153099e35bdef` | [Rd](https://raw.githubusercontent.com/tidyverse/ggplot2/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/man/scale_linewidth.Rd) · `07ec948d769e03228b48284d9d5d4399003dc52feab591a1775c5c95c06d8b6b` |

본문·Rd·R·PNG의 전체 지문/URL/수신 영수증은 `lineage-final.json`과 `audit-extraction.json`에 있다. 각 `raw/` 파일을 `resume-static-validation.json`의 수신 SHA-256 및 Git blob으로 다시 확인할 수 있다. base 없음, 선택 첫 img의 srcset 없음, picture 없음, 선택 절 SVG/data URI 없음도 원 HTML에서 확인했다. 1x/2x 별칭을 합쳐 생존으로 바꾼 경우는 없다.

## 3. 보조 사건과 자료 대조

| 사전 사건·대표 | 확인한 공식 변경 | 실제 새 목적·방법 | 범위·반례 탐색 한계 |
|---|---|---|---|
| [04a5ef274e…](https://github.com/tidyverse/ggplot2/commit/04a5ef274e912bee76180154b25d8bca0206feb1) · register_theme_elements | .r→.R Upkeep, theme-elements R100 | 사용자 정의 panel annotation과 등록·ggproto/render_fg 방법 YES | 사건은 전수 포착되었지만 연결57페이지의 의미를 모두 판독한 것이 아니다. 대표 한 예제와 주 M2개를 상세 판독했다. |
| [b9f43f2a7d…](https://github.com/tidyverse/ggplot2/commit/b9f43f2a7d93548b0794bc527b0f18ff0f028681) · guide_axis | guides-axis.R 제거, guide-axis.R 추가, GuideAxis ggproto rewrite | n.dodge=2 축 텍스트 배치와 공개 호출 YES | 같은 guide_axis는 앞 사건에도 연결돼 사건수2를 서로 독립인 원 예제57+1로 합치지 않는다. 내부 구현 메커니즘은 달라졌지만 사전 특정 API 목적은 유지한다. |

동일 source DAG에서 R/man 이동·삭제 metadata 사건은4개였다. 위2개가 적격 예제와 연결된다. 나머지 `5074f11…`의 range.r 제거는 scales Range 사용으로의 내부 전환이고, `202029b…`의 utilities-table.R 제거는 내부 grob helper 정리다. 두 원 diff를 직접 읽었지만 독자가 받은 논리 예제의 삭제 사례에 넣지 않았다. `4daadf7…`의 PositionJitterdodge 내부 vec_unique_count 교체는 추가 공식 설명 근거이며 보조 D/R 표본 사건으로 넣지 않았다.

보조 상세 대표 2개는 원 시각 목적·공개 방법 모두 YES, 실제 음성0이다. **보조 대표 결과를 주 혼동표에 넣지 않았다.** `lineage-extra.json`에는 두 대표와 별도 자료 대조3개의 양판10행이 있다.

## 4. 직접 자료수와 중복 대사

`sources-stage3.jsonl`의83개 기록 중 신규 고유 자료는14저작으로 보수 산정했다. 본문6(주4+사전 보조2), 본문과 계보가 다른 그림/예제소스3(stat_unique·labs·ggtheme), 공식 변화5사건이다. 각 논리예제의 old/new HTML·Rd·R·PNG는 한 저작이며 한 범주에만 배정한다. 102의 고정 `sources.jsonl`을 다시 읽어 이미 센 계보와 URL을 확인했고, 새9예제 및 새5변경사건은 거기에 없다. 발행 트리·릴리스 정보의 재수신은 계승0이다.

**원 stage1/root 원장의 stat_unique 본문 산입은 최종 집계에서 제외하고 이 자료의 독립 그림/소스 범주 한 건으로만 배정한다.** 원 기록은 삭제하지 않으며 최종 source 집계 담당자가 이 재분류를 대사해야 한다. labs와 ggtheme도 HTML과 PNG를 동시에 세지 않는다. guide_axis의 source와 body도 별도 두 건으로 세지 않는다. 74개 원 파일 검증이나 18개 PNG 직접 열람은14개의 신규 저작 분모와 다르다.

stat_unique의 첫 그림은 `geom_point(alpha=0.1)` 기준 그림이며 `stat="unique"`는 다음 그림이다. labs 저자 파일의 첫 `@examples`는 update_labels이므로 labs에 해당하는 두 번째 블록(새 R/labels.R 50행 이후)을 연결했다. 이런 경계 오류를 피하기 위해 단순 첫 @examples 또는 페이지 제목으로 예제를 결정하지 않았다.

편의 웹 리더의 raw HTML4회가 DisabledError를 돌려줬다. 이4실패는 산입0이며 삭제의 근거로 삼지 않았다. 동일 불변 원 URL의 보존 원문을 수신 영수증과 검증했고, 재개 때 scale_shape 새 HTML을 urllib로 독립 재수신하여 HTTP200·동일 SHA-256을 확인했다(`resume-network-check.json`). 선택 HTML은 원래도 text/plain으로 전달된다.

## 5. 반환 선택·확인 비용

| 사례 | 권고 | 정확한 본문·payload | 예측 후 원자료 추가 요청 수 | 바뀔 조건 |
|---|---|---|---|
| GG-A1 | 유보(결원) | 미확인 | 0 | 누락된 적격 A 후보가 확인되면 모집단 교정 검토 |
| GG-A2 | 유보(결원) | 미확인 | 0 | 누락된 적격 A 후보가 확인되면 모집단 교정 검토 |
| GG-M1 | 두 판 병기 | [옛](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape.html#ref-examples) / [새](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_shape.html#ref-examples) · [옛 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape-1.png) / [새 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_shape-1.png) | 8 | 새 정확 절의 목적/호출 부재 또는 fragment가 다른 예제로 도착한다는 실제 관측 |
| GG-M2 | 두 판 병기 | [옛](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_segment.html#ref-examples) / [새](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/geom_segment.html#ref-examples) · [옛 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_segment-1.png) / [새 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/geom_segment-1.png) | 10 | 새 정확 절의 목적/호출 부재 또는 fragment가 다른 예제로 도착한다는 실제 관측 |
| GG-G1 | 두 판 병기 | [옛](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/position_jitterdodge.html#ref-examples) / [새](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/position_jitterdodge.html#ref-examples) · [옛 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/position_jitterdodge-1.png) / [새 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/position_jitterdodge-1.png) | 8 | 새 정확 절의 목적/호출 부재 또는 fragment가 다른 예제로 도착한다는 실제 관측 |
| GG-G2 | 두 판 병기 | [옛](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_linewidth.html#ref-examples) / [새](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_linewidth.html#ref-examples) · [옛 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_linewidth-1.png) / [새 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/scale_linewidth-1.png) | 8 | 새 정확 절의 목적/호출 부재 또는 fragment가 다른 예제로 도착한다는 실제 관측 |

추가 요청 수는 봉인예측 UTC 뒤 성공한 개별 원 HTML·PNG·Rd·R·해당 공식 변경의 수신 영수증 수다. 공유 변경사건이 여러 사례에 기여할 수 있으므로 단순 합이 전체 고유 자료수가 아니다. 원문을 다시 연 재개 조회/로컬 image viewing은 별도다. 운영자에게는 정확한 절 확인 비용, 역사 저자에게는 옛판과 옛 PNG의 불변 지문, 비교판 독자에게는 새판의 정확한 예제 위치가 각각 필요하다.

raw HTML의 `#ref-examples`는 보존한 HTML DOM id를 정확히 지정한다. 원 URL이 text/plain이라 브라우저에서 HTML로 렌더·스크롤된다는 약속은 하지 않는다. `returns-final.json`에 고정 GitHub `#L` 코드 보기 URL도 함께 둔다. 실제 렌더 화면/fragment scroll은 미확인이므로, 해당 제품이 한 번 클릭해 바로 보이는 화면만을 요구하면 반환을 유보하고 별도 표시 경로를 확인해야 한다. 조사판은3.4.0→3.5.0이며2026년 최신 안내라고 쓰지 않는다.

## 6. 반례 탐색의 경계·재현

옛195개 reference HTML과 잔여 적격68개 대표 자원의 새 경로 존재 여부는 전수 판독했다. 새 의미·절 사용은 주4개, 자료 대조3개, 보조 대표2개에 국한한다. 이9개에서는 옛 대표 경로 잔류·새 절 미사용이 없었고, A 후보 자체도0이었다. 따라서 **ggplot2에서 양방향 오류가 없다고 일반화할 수 없다.** 아직 읽지 않은59개 새 본문의 의미적 미사용 여부는 미확인이다. 이동·삭제 source사건4개를 모두 열었다는 사실이57개 연결 예제의 목적을 모두 재확인했다는 뜻도 아니다.

원 SCOPE의 보조 최대10건 규칙에서 실제 eligible 사건2개를 모두 열었고, 사전 대표2개를 사용했다. ggplot2만의 후속 최소 조사라면 같은 고정68잔여 모집단의 나머지59개 정확 Examples 관계를 전수 판독하여 잔류 참조가 빠진 후보를 찾는 것이다. 이번 주 표본과 합산하지 않고 별도 보조 분모로 남겨야 한다.

재계산 명령:

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/ggplot2/finalize_stage3.py
```

입력은 기존 audit-extraction/details/receipts, 봉인 predictions/supplemental-selection, 원 raw 파일 및092f4c5의102자료 원장이다. `.cache`가 없어도 커밋될 raw/에서 원문을 읽는다. 스크립트는 선택·예측을 변경하지 않으며 source bytes/트리/first code 보존을 검사한 뒤 명시적 판독값을 표로 만든다. 새로 만든 UTC만 달라질 수 있다. 실제 R 렌더/역사 빌드 검사는 하지 않는다. 전체 저장소 계약 검사는 부모가 결과 SHA를 커밋한 뒤 수행한다.

별도 AI 역할이 재개하여 원문·그림을 다시 판독한 범위는 위9예제와5변경사건이다. 작성 자료를 함께 읽었으므로 정답을 모르는 독립 맹검/사람 검토라고 부르지 않는다.

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
|---|---|---|
| A층 후보0·원 목적 음성0이라 이 프로젝트에서 FPR 또는 부재 후계 찾기 성능을 측정할 수 없다. | 고정 frame의 남은59새 Examples를 별도 표본으로 판독; 원 tree/반환 코드 위치 보존. | 잔류 경로가 해당 목적 절에서 참조되지 않거나 다른 목적에만 쓰인 정확 본문이 발견되면 미사용 반례를 추가한다. |
| 소스57경로의 정확 대소문자 이동은 실제 의미 삭제가 아니었다. source-set 규칙 보완도 새 경로 노출 후였다. | man-only 민감도 원장과 명시적 저자 파일 연결을 함께 검토한다. | @examples/Rd 연결이 없거나 공개 예제 방법이 실제 제거된 문서가 나오면 M선정 해석/방법 판정을 바꾼다. |
| 고정 raw HTML의 DOM과 PNG 직접 열람은 렌더된 화면/fragment 이동·역사적 생성G를 입증하지 않는다. | 같은 고정 원문을 허용된 렌더 경로에서 표시하고 해당 fragment 이동을 관측; G는 실제 build manifest가 있을 때만 조사한다. | 표시가 다른 예제에 도착하면 반환을 유보하고, input→run→output 지문이 연결되면 G의 미확인을 갱신한다. |
