# 동명 원레코드 네 사례와 반환에 쓸 범위

| 사례·실제로 연 두 편 이상 | 이름 외에 선택을 바꾸는 한 값 | 남는 다의성과 주소 반례 |
|---|---|---|
| Lake Louise. Alberta의 정착지 IACFT와 호수 IAFIG. 같은 NTS 082N08, 이름과 1952-04-03 결정일도 같다. [정착지](https://geonames.nrcan.gc.ca/search-place-names/unique?id=IACFT) [호수](https://geonames.nrcan.gc.ca/search-place-names/unique?id=IAFIG&wbdisable=true) | 두 후보 사이에서 목적이 인구 정착지라면 Generic Term Hamlet, 물 표면이라면 Lake를 쓰면 갈린다. 시·도와 이름만인 경우 둘 다 남는다. | 정착지의 고정 URL에 이미 IACFT가 있다면 기존 주소 하나가 타입·좌표까지 읽는 출발점이다. GNBC HTML과 JSON은 같은 레코드다. |
| Green Lake. Saskatchewan의 Northern Village HAAVF, 남쪽 호수 HADOP, 다른 호수 HAYJL. [마을](https://geonames.nrcan.gc.ca/search-place-names/unique?id=HAAVF) [남쪽 호수](https://geonames.nrcan.gc.ca/search-place-names/unique?id=HADOP&wbdisable=true) [다른 호수](https://geonames.nrcan.gc.ca/search-place-names/unique?id=HAYJL) | Northern Village는 마을 레코드를 고른다. 목적이 호수라면 NTS 073J04로 HADOP를 고를 수 있다. | 유형과 주를 함께 줘도 두 호수가 유효하다. 064M09나 공식 키를 요청하는 것이 다른 속성 여러 개를 붙이는 것보다 작다. 지도 축척과 결정일은 렌더된 경계나 접근 가능성을 보증하지 않는다. |
| Water Lilies. Monet과 유화라는 조건이 같다. MoMA의 1914–26 3패널 666.1959.a-c와 Met의 1919 단일 캔버스 1998.325.2. [MoMA](https://www.moma.org/collection/works/80220) [Met](https://www.metmuseum.org/art/collection/search/438008) | 이 둘 사이에서 소장 단위나 소장처가 갈라준다. 시대 범위를 1919와 겹쳐 찾으면 두 결과가 남을 수 있다. | 이미 MoMA 80220 링크가 있으면 그 기관의 한 레코드와 패널 표기를 바로 건넬 수 있다. 그 주소를 전체 연작의 식별자로 확대할 근거는 없다. |
| The Kiss. Musée Rodin의 대리석 S.1002/Lux.132와 Philadelphia의 Brancusi 1916 조각 웹 레코드 51306. [Musée Rodin](https://www.musee-rodin.fr/en/musee/collections/oeuvres/kiss) [Philadelphia](https://www.philamuseum.org/objects/51306) | 두 객체 사이에서는 제작자만으로 갈린다. 제작자+제목만 주면 동일 주제의 Brancusi 여러 판 중 네 번째라는 판단에는 소장 레코드가 필요하다. | 같은 장르·제목을 순위 하나로 압축하면 한 작품이 빠진다. Rodin 기록은 구상 무렵과 대리석 작업 연도를 나누므로 날짜 필드 의미도 확인한다. |

[출처 원장](../sources.jsonl) GE01–05 및 AR01–04가 위 개별 레코드다. 주소에 식별자가 있을 때의 기술적 역참조와, 그 주소를 사람이 갖고 있거나 그 필드를 알아볼 가능성은 별개다. 위 자료가 편집기의 번역 또는 사람의 질문 횟수를 측정하지는 않는다.
