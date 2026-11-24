# 표 1
행 단위: 고정 사례 자리 × 기관 × 확인판(역사 교육 예시와 현행판 분리); GNIS 후보는 별도 대조. URL과 원장 ID는 sources.jsonl 참조. “표시 없음”은 해당 역사 예시 화면에서의 관측이지 현재 필드 부재가 아니다.

| 지명 자리·기관·판 | 010/URI·원필드 | 선호명/이형명/관계 | 저작 근거·주소 | 동일·별개·보류 | 미확인 |
|---|---|---|---|---|---|
| A 역사 LC 2004 전사(2008 교재) | 010 $a n 79090096; 005 20040623033151.0; 100/400/670; $z·500 표시 없음 | Tennessee Williams 1911–1983; Thomas Lanier Williams 같은 날짜; 두 번역 전사 | [E04 Appendix B L9615–9665](https://www.loc.gov/catworkshop/courses/nametitleauth/pdf/Name-Title_Trnee_Manual.pdf) 670 Glass menagerie 1945 등 | 역사 레코드 내 동일 | 실제 현대판 및 정확 전사 철자 |
| A 현행 LC | [n79090096](https://id.loc.gov/authorities/names/n79090096) 접근 실패 F01–F05 | 미확인 | A05 NDL 자체 출처는 별도 | 보류 | 010 $a/$z,005,100,400,500,670 전체 |
| B 1951 자리 LC/기타 | 010/URI 미확인 | 교육 Davis, Kate, 1951- | E04 L3629–3632 Rough road c2000; Secretary of the Interior 2003 | 보류 | 원전거 및 서지 연결 |
| B 1959 자리 LC/기타 | 010/URI 미확인 | 교육 Davis, Kate, 1959- | E04 L3634–3638 Raptors of the Rockies 2002; E02 정답 | 보류 | 원전거 및 서지 연결 |
| C père LC | [n79042162](https://id.loc.gov/authorities/names/n79042162) NDL 연결 후보 A03 | LC 원필드 미확인 | A03 NDL citation | LC 보류 | 010/005/100/400/500/670 |
| C fils LC | [n81120314](https://id.loc.gov/authorities/names/n81120314) NDL 연결 후보 A04 | LC 원필드 미확인 | A04 NDL citation | LC 보류 | 동일 |
| C père BnF 2024-08-30 | [cb119010630](https://catalogue.bnf.fr/ark:/12148/cb119010630.public) A01 L68–83 | Dumas Alexandre 1802–1870; père/Aramis; fils 관련 | [W03](https://catalogue.bnf.fr/ark:/12148/cb35752325z), [W04](https://catalogue.bnf.fr/ark:/12148/cb35215558h) Monte-Cristo 저자 | fils와 별개 | raw MARC와 표제면 영상 |
| C fils BnF 2024-03-30 | [cb11901062n](https://catalogue.bnf.fr/ark:/12148/cb11901062n) A02 L66–82 | Dumas Alexandre 1824–1895; fils; père/Jalin 관련 | [W02](https://catalogue.bnf.fr/ark:/12148/cb38665336s) La dame aux camélias 저자 | père와 별개 | raw MARC와 표제면 영상 |
| C père NDL 2025-11-18 | [00438367](https://id.ndl.go.jp/auth/ndlna/00438367) A03 L14–45 | Dumas Alexandre 1802–1870; Père, 일본어; LC exactMatch | Monte-Cristo 일본어판 출처 | fils와 별개 | LC 원값 및 별도 실제 서지 역방향 |
| C fils NDL 2025-11-10 | [00438368](https://id.ndl.go.jp/auth/ndlna/00438368) A04 L14–42 | Dumas Alexandre 1824–1895; Fils, 일본어; LC exactMatch | 椿姫 일본어판 출처 | père와 별개 | LC 원값 및 별도 실제 서지 역방향 |
| A 대조 NDL 2024-01-30 | [00461042](https://id.ndl.go.jp/auth/ndlna/00461042) A05 L14–43 | Tennessee Williams; 일본어 variant; LC exactMatch | 欲望といふ名の電車 | NDL 내 동일, LC 현행 보류 | Thomas Lanier 현행 LC |
| C 대조 BnF 2023-06-06 | [cb10746501c](https://catalogue.bnf.fr/ark:/12148/cb10746501c) A06 L53,67–78 | Jalin, Alphonse de; 공동 필명, fils 등 관계 | Le filleul de Pompignac 1869 | 별개 전거·관계 | 작품별 공동 필명 귀속 |
| GNIS MO/ID/CO 후보 | 735864/400107/203868 F18–F20, F24 | Springfield; MO의 North Springfield 일부 variant 후보 | [USGS 데이터 설명 G03](https://www.usgs.gov/us-board-on-geographic-names/download-gnis-data), [G05](https://cartowfs.nationalmap.gov/arcgis/rest/services/geonames/FeatureServer) | 후보만, 보류 | 실제 ID/좌표/variant 행 조회 실패 |

# 표 2
행 단위: 요청 목적 × 입력의 실제/교육 예 × 반환 규칙. 반환은 설계 제안이며 실행 결과가 아니다.

| 요청 목적 | 검색어·원표기 | 돌려줄 실체·역할 | 합칠 조건 | 분리·보류 반례 |
|---|---|---|---|---|
| 옛 인용 보존 | A Thomas Lanier Williams / Tennessee Williams | 원문 literal과 역사 전거판; 현행 연결은 별도 | 같은 역사 010/005 내 400 연결; 원표기는 덮어쓰지 않음 | 현행 005·철자·필드 미확인 |
| 현행 별칭 탐색 | A Thomas Lanier Williams | 역사 결과 및 NDL 후보, LC 현재 결과는 보류 | 같은 현재 전거 400 실제 관측 또는 검증된 redirect | 2004 전사만으로 현행 alias 확정 금지 |
| 동명 후보 선택 | B Kate Davis | 1951,1959 교육 후보 두 개 + 미확인 표시 | 실제 기관+ID 및 해당 저작 670/서지 연결 일치 | 1951의 두 저작과 1959 Raptors는 이름만 같음; B 0/2 |
| 옛 인용 보존 | C ifjabb Dumas Sándor / Dumas père | 판별된 서지별 원표기 + 해당 저작 역할 | W02와 A02 또는 W03/04와 A01의 서지 링크 확인 | 두 전거의 이름을 같은 정규화 문자열로 축약하면 혼동 |
| 현행 별칭 탐색 | C Dumas fils / Aramis | 해당 BnF 전거 후보 및 역할 근거; LC 링크 후보 별도 | 기관 자체 variant → 동일 전거 | 공동 필명 Jalin은 A06 별도 관계, 500 식 자동 동치 금지 |
| 동명 후보 선택 | C Alexandre Dumas | père/fils 두 후보 + 연대·작품·역할 | 특정 작품/판의 연결을 근거로 해당 후보 선택 | W01은 두 Dumas 모두 등장, W05는 저자와 대상 다름 |
| 전거 갱신 | 취소 LCCN, 400, 500 | 400 검색 안내, 500 관련 탐색, 010 z 이력/검증된 재지정 | 기관의 실제 이전→현행 방향 및 유효 ID 확인 | R01 예시만으로 현재 redirect 생성 금지; A06 공동 필명 |
| 지도 선택 | Springfield / variant | 여러 지형 후보 ID, class, state/county, 위치 | 동일 현행 GNIS Feature ID에 variant 행 확인 | G04 Mount Rainier 검색 네 후보; Springfield 원행 미확인 |
