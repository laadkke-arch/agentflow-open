# AF-RES-044 Q7 보조 비교: 소장품과 노선

이 폴더는 자연 8요구·보강 4요구 밖의 보조 원장이다. 실제 공식 원문 8개를 직접 읽었다. 세 소장품 레코드는 같은 판화 제목을 갖지만 서로 다른 대상의 기관 기록이다. 한 원문의 여러 쪽·fragment·재열람은 추가 산입하지 않았다. 사람의 클릭·채택, 실물 감정, 당일 운행은 관측하지 않았다.

## 1. 확인 범위

| 출처 ID | 직접 읽은 범위 | 근거 주소 |
| --- | --- | --- |
| CF-M01 | Met 36491, Artwork Details의 치수·취득·Object Number | https://www.metmuseum.org/art/collection/search/36491 |
| CF-M02 | Met 56353, 같은 필드 | https://www.metmuseum.org/art/collection/search/56353 |
| CF-M03 | Met 45434, 같은 필드 | https://www.metmuseum.org/art/collection/search/45434 |
| CF-M04 | API Object 응답의 objectID·accessionNumber·title·portfolio 정의 | https://metmuseum.github.io/ |
| CF-T01 | A 시간표 p1 설명, p2 Manhattan 방향, p8 Queens 방향의 첫 두 행·열 | https://www.mta.info/schedules/subway/a-train |
| CF-T02 | 지선 설명과 Lefferts/Far Rockaway/Rockaway Park 역 목록 | https://www.mta.info/maps/subway-line-maps/a-line |
| CF-T03 | Aqueduct Racetrack 표지·출입구 방향 표시 | https://www.mta.info/document/1091 |
| CF-T04 | Get the right train / Go the right way | https://www.mta.info/guides/riding-the-subway |

원문별 정확한 위치·확인 시각·한계는 [sources.jsonl](sources.jsonl), 직접 취득한 바이트의 해시는 [access-log.jsonl](access-log.jsonl)에 있다. HTML/PDF 전체를 재배포하지 않는다. PDF는 내려받아 PyMuPDF로 렌더하고 view_image로 열 배치와 표지를 확인한 다음 임시 원문과 이미지를 제거했다. 이 시각 확인은 PDF 스킬의 절차를 적용했다.

## 2. 같은 작품명과 다른 소장품

| 소장품 레코드 | Object Number | 기관이 기재한 크기 | 기관이 기재한 취득 경로 |
| --- | --- | --- | --- |
| CF-M01 / 36491 | JP10 | 24.4 × 35.7 cm | Rogers Fund, 1914 |
| CF-M02 / 56353 | JP2972 | 25.1 × 37.8 cm | Henry L. Phillips 유증, 1939 |
| CF-M03 / 45434 | JP1847 | 25.7 × 37.9 cm | H. O. Havemeyer 유증, 1929 |

**직접 관측:** 세 기관 기록은 작가와 Great Wave 제목을 공유하지만 소장품 번호·치수·이력이 다르다. 같은 인쇄 순서나 상태라고 감정한 것은 아니다. CF-M01 HTML에는 다른 소장품으로 가는 실제 관련 링크도 있다([museum-hrefs.json](museum-hrefs.json)).

**연구자 해석:** `CF-M-NAME`처럼 작품명과 작가만 확인한다면 대표 한 개로 충분하다. `CF-M-OBJECT`처럼 JP2972의 크기를 확인한다면 JP10 대표의 크기를 전용할 수 없다. 관련 멤버 목록은 대상이 남아 있다는 사실만 제공하며, 특정 소장품 필드는 그 기록을 열어야 확인된다.

**관리자 관점:** 표시용 제목 묶음과 소장품 원자료 병합은 다르다. Met API는 objectID를 고유 키, accessionNumber를 항상 고유하지는 않은 식별자로 설명한다. 따라서 원 ID와 소장품별 필드 출처를 보존해야 재분리의 입력을 남길 수 있다. 이는 문서에 기초한 관리 제안이며 실제 merge/split 시험 결과가 아니다.

## 3. 같은 A 노선명과 서로 다른 목적지·방향

**발행자 진술:** CF-T01 첫 쪽은 여러 Queens 종착과 혼잡 방향 운행을 설명하고, 표가 모든 역을 담지 않는다고 명시한다. CF-T02의 104 St는 Lefferts 지선에, Howard Beach-JFK Airport는 Far Rockaway 지선에 있다. CF-T04는 문자/번호뿐 아니라 정차 표지와 차량 목적지를 확인하도록 안내한다.

**직접 관측:** CF-T01 p8의 열 배치를 확인했다. 평일 Queens 방향 첫 행은 Inwood 06:58 → Far Rockaway 08:33, 다음 행은 Inwood 07:05 → Lefferts 08:20이다. `CF-T-BRANCH`의 종착 확인에는 행·지선이 필요하다. 이 판독은 유효일 2025-11-02의 출판 일정에 한정한다.

`CF-T-DIRECTION`에서는 지도 CF-T03의 Aqueduct Racetrack 표지에 North only, 두 출입구에 Brooklyn/Manhattan 방면만이라는 표시가 실제로 있다. CF-T02의 같은 역 이름과 한쪽 플랫폼 기재만으로 남행 정차를 보증할 수 없다. CF-T03의 개정일은 **미확인**이므로 현재 운행 증명으로 승격하지 않는다.

## 4. 단일 대표가 충분한 반례와 한 요소 민감도

같은 A PDF 한 개에 양방향·지선 시간이 함께 들어 있다. 한 대표 URL이 여러 의미를 담는다는 이유만으로 근거 손실이 발생하지 않는다. `CF-T-NAME`의 노선·지선 이름 확인은 p1 한 곳으로 가능하다.

`CF-T-SCOPE`는 **판독 범위만** 바꾸는 보조 진단이다. 원문 URL·해시·대표·요구·그룹 멤버를 고정한다. 도착한 p2(Manhattan 방향)만 읽게 하면 평일 07:05 Inwood→Lefferts 행은 **미확인**이다. 동일 PDF의 다른 쪽을 허용하면 p8에서 확인되어 판정이 `예`로 바뀐다. 따라서 문서 수준 대표의 손실과 도착 절/쪽 제한의 손실을 구분해야 한다. 이 진단은 사후 설계한 보조 민감도이고, 자연 8요구의 사전 등록 결과나 실제 사람 두 클릭 시험으로 집계하지 않는다.

강한 반증 시도도 남긴다. A 시간표에 104 St가 없다는 것만으로 무정차라고 결론내리려던 가능성은 p1의 timepoint 한정과 CF-T02의 역 목록이 반박한다. 반대로 Aqueduct의 명시적 방향 표지는 단순한 공백과 다르다. 같은 A 색상·노선명만으로 목적지·정차를 합치면 이 차이를 잃는다.

## 5. 재현·한계와 다음 최소 확인

- [comparisons.csv](comparisons.csv)의 6행은 위 요구 범위와 근거를 연결한다. [observations.json](observations.json)은 판독한 행·민감도 고정 요인을 보존한다.
- 자연/보강 표본의 클릭 횟수·회수율에 이 6행을 더하지 않는다. 고유 원문 최소수의 박물관·교통 항목으로만 사용할 수 있다.
- 검색 결과의 A 시간표 요약은 2025-06-08 판을 가리켰지만 실제 열린 PDF는 2025-11-02 판이었다. 결과에는 실제 PDF의 날짜와 SHA256만 적용했다. 검색 스니펫은 원문 최소수에서 제외했다.
- 관리자에게 필요한 다음 최소 확인은 Met 원 ID별 필드를 두 묶음으로 합쳤다가 같은 ID·값·출처로 되돌리는 작은 재구성 시험이다. 실제로 시험하지 않았다.
- 운행 판단의 다음 첫 자료는 위 A 시간표·라인맵의 현재판과 해당 날짜의 공식 서비스 변경 기록이다. 관측한 PDF를 현재 실시간 운행으로 대체하지 않는다.

| 중요한 불일치·약점 | 영향받는 판단과 근거 | 다음 최소 조사 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| 작품명 동일성은 소장품/인쇄 상태 동일성이 아니다. | CF-M-OBJECT; CF-M01–03 Object Information | 해당 Met objectID의 curatorial 상태·인상 판정 기록 | 기관이 동일 실물의 중복 레코드라고 정정하면 원자료 합침 판단이 달라진다. |
| 시간표는 주요 시점 역만 담고 지도 개정일 일부는 미확인이다. | CF-T-BRANCH/CF-T-DIRECTION; CF-T01 p1, CF-T03 표지 | 날짜가 맞는 공식 운행/정차 자료를 추가 대조 | 해당 날짜·방향의 정차 변경이 확인되면 운행 결론이 달라진다. |
| 판독 범위 민감도는 연구자 진단이고 실제 이용자 시험이 아니다. | CF-T-SCOPE; CF-T01 p2/p8 | 같은 대표로 사람의 실제 탐색 경로·시간 관찰 | 사용자가 같은 문서 다른 쪽을 찾지 못하면 문서상 접근 가능성과 실제 도달은 달라진다. |
