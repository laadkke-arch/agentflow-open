# Vega-Lite 엄격한 두 번째 링크 목적지 조사

## 분모와 접근 결과

`windows-V.json`의 `strict_outgoing_hrefs`만 사용했다. 17개 비빈 후보창에서 href 발생246개, 고유 목적지 URL89개, fragment 제거 문서43개다. 같은 URL이 여러 후보/요구에서 나타나도 `second-hop-targets.json`의 source occurrence를 지우지 않았다. 원풀·원요구·metadata·그룹 key는 변경하지 않았다.

독립 문서43개 중 HTTP200은36개, HTTP403은7개다. URL 수준에서는 HTTP200이82개지만 실제 목표 fragment/범위를 확인한 목적지는65개다. 17개는 문서는 열리지만 literal id/name이 없고, 7개는 HTTP403이다. 네 요구의 완전 필수 atom 또는 새 완전 대안은 **확인0**이다. 실패·도착절 미확인을 해결 불가능 또는 의미적 부적격으로 바꾸지 않는다.

| 구분 | 실제 관측 | 판단 경계 |
| --- | --- | --- |
| V1에서 출발한 두 번째 링크 | view background와 size | subtitle config 문서로 넘어가는 href가 아니며 원 v4 수정 근거가 없다. |
| V2에서 출발한 두 번째 링크 | 지도 좌표·projection·GeoJSON·지도 예제·d3 투영 파라미터 | identity 일반 기능과 원 graticule-label 결합 성공을 구별한다. |
| V3에서 출발한 두 번째 링크 | text/mark/encoding/config/property types | text 문자열과 시각 속성은 wordcloud layout 지원을 입증하지 않는다. |
| V4에서 출발한 두 번째 링크 | 일반 transforms·집계·field/data/type 계약 | 각 문서의 명시된 기능은 tree/dendrogram layout의 지원 근거가 아니다. |

V2의 identity/reflectY는 원풀에서 확인된 하위사실을 다시 제공할 수 있다. 봉인된 V2.A1은 graticule 결합까지 포함하므로 이 하위사실을 완전 atom으로 세지 않았다. Vega Projections의 identity 설명 역시 원 Vega-Lite 결합 성공 또는 해당 오류 수정의 증거가 아니다. `second-hop-coding.json`에는 source URL별로 관련 요구의 동일 atom·판·방향 판정을 남겼다.

## 실제 도착 실패와 범위

- Wikipedia5개와 원문 href의 `http://bl.ocks.org` 2개는 이 HTTP 환경에서403이었다. 프로토콜·호스트·scheme을 바꿔 접근 성공으로 대체하지 않았다. 재개자는 동일 URL의 실제 접근과 목적지 범위를 먼저 확인한다.
- 현행 d3-geo README는 짧은 모듈 소개와 Documentation/Examples/Release 링크로 바뀌어, 원문이 가리키는 개별 `geoAlbers` 등 fragment15개가 없다. HTTP200과 원문 절 도달 성공을 별도로 둔다. 새로운 d3js 문서로 가는 세 번째 클릭을 암묵적으로 추가하지 않았다.
- Vega-Lite의 `encoding.html#field-transform`, `projection.html#properties`도 해당 literal id/name이 없다. 비슷한 새 제목의 절을 찾아 같은 도착으로 치환하지 않았다.
- GitHub에서는 실제 `user-content-` id/name 접두사도 검사했다. 접두사를 붙여 추측한 URL을 후보로 만든 것은 아니며, 원래 href를 받은 GitHub의 게시 DOM 앵커 확인이다.

도착 fragment가 heading이 아니면 실제 요소를 포함하는 문단/블록부터 다음 동급 이상 heading 전까지 범위를 잡았다. no-fragment는 해당 article/main/body의 h1 뒤800 공백 token이다. 각 목적지의 해시·범위·단어 수는 `second-hop-arrivals.json`에 있다. 실제 읽은 것은 이 창의 기능 정의·시작 범위와 필수 조건에 해당하는 문맥이며, 무관한 장문의 모든 단어를 정독했다고 주장하지 않는다. 키워드 검색에서 `tree`가 나타난 mark 문서는 **ARIA accessibility tree** 문맥이었다. 이를 계층 자료의 tree layout으로 세지 않았다.

## 오류 보존과 자료 수

첫 추출기의 HTML comment-node 처리 오류는 일곱 문서를 접속실패처럼 반환했다. 실제 HTTP실패와 구별해 `second-hop-access-v1.json`과 `second-hop-arrivals-v1.json`을 보존하고, comment 노드를 제외해 실제 게시 HTML을 다시 취득·판독했다. 최종 접근 결과에서는 이 일곱 건 모두 HTTP200이다. 첫 GitHub 비heading 앵커의 문단만 추출하던 좁은 범위도 사전 규칙의 다음 heading 경계까지 바로잡았다. 원 요구·풀·그룹키는 불변이며 정정 전후 기록을 함께 보존했다.

`second-hop-sources.jsonl`은89행이다. 이 V 경로에서 기존 counted 원문과 중복을 제거하면 신규 직접 일차 원문31개가 있다. 이미 읽은5개의 후보 HTML과 같은 fragment는 추가로 세지 않았다. 최종 전체 출처 수는 부모가 다른 경로와의 중복도 제거해 재계산해야 한다.

통제된 독립 시행의 출발 카드·첫 동작·두 번째 동작·합산된 조건은 부모의 clicks 원장이 기록한다. 이 파일의 서로 다른 목적지에서 읽은 내용을 한 시행의 사용자 기억으로 합치면 안 된다. 실제 사람의 클릭·채택은 **미확인**이다.
