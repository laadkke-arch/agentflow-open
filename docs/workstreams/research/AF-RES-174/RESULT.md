# AF-RES-174 — 비지도 차트 레이블과 지도 배치 원전 (PARTIAL)

| 요청·레이블 ID | 입력만 본 출처 | 가까운 규칙의 예측 | 지도 원리의 예측·출처 | 노출·미확인 |
|---|---|---|---|---|
| V1: 그룹 막대, B 첫 막대 등 | [#3376](https://github.com/vega/vega/issues/3376) 최초 본문에는 결과도 포함 | 그룹 local bounds를 global 크기와 일치시킨 후 padding/anchor 검사, ID 미정 | [WaPo](https://www.mapbox.com/blog/washington-post-s-electoral-maps-how-we-built-it): 변환된 도형에 붙는 포인터; 막대 귀속 검사, ID 미정 | 노출; 압축 spec 미복원, 폰트·viewport 미정 |
| V2: L1(2,9), L2(2,8), L3(4,5), L4(9,.2), L5(1,.5) | [#3558](https://github.com/vega/vega/issues/3558) 300×300, font16, offset20, 8 anchors, circle size200 | [LabelLayout](https://github.com/vega/vega/blob/v5.16.0/packages/vega-label/src/LabelLayout.js): L1/L2 경쟁, L4 좌/위·L5 우/위 조건부. 정확한 ID·방향 미정 | [Imhof](https://giscience-research.github.io/geog281a/readings/wk5/Imhof-1975.pdf), [CMS](https://www.eecs.harvard.edu/~shieber/Biblio/Papers/tog-final.pdf): 다른 점으로 읽힐 후보를 거절하거나 leader 검증. L1/L2 소속 시험 추가 | 노출; 실제 폰트 metrics·우선권 없음 |
| V3: 영화 Title 집합 | [#3746](https://github.com/vega/vega/issues/3746) 800×600, 외부 movies.json | mark 충돌·sort·anchor. 정확한 이름 미정 | [Esri weight](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/text/prevent-labels-from-overlapping-certain-features.html): 보호할 지물의 의미가 있는 경우만 가중치; transform 실패에는 무효 | 노출; 버전·데이터 동결 안 됨 |
| G1: mtcars 행 wt 2.75–3.45 | [#95](https://github.com/slowkow/ggrepel/issues/95) seed42, hjust -0.5/1.5, vjust1.5 angle90 | [0.7.0 R](https://github.com/slowkow/ggrepel/blob/0.7.0/R/geom-text-repel.R) grob와 device 경계, 정확 ID 미정 | [PSU](https://courses.ems.psu.edu/geog486/node/557): 소속이 바뀌는 배치 회피, 방향 미정 | 노출; 실제 크기·버전 불명 |
| G2: tSNE group IDs | [#101](https://github.com/slowkow/ggrepel/issues/101), sLF 미제공 | group별 집계 후 한 레이블, ID 미정 | [Imhof](https://giscience-research.github.io/geog281a/readings/wk5/Imhof-1975.pdf): 면의 대표점은 면이 의미를 가질 때만; 겹치는 tSNE에는 면 이름 강제 금지 | 노출; 원 데이터 없음 |
| G3: 50개 중 test>75, a/b | [#125](https://github.com/slowkow/ggrepel/issues/125) seed1, jitterdodge | [ggrepel examples 0.9.6](https://github.com/slowkow/ggrepel/blob/0.9.6/vignettes/examples.Rmd): 같은 전체 행·position, 비대상 빈 문자열. ID는 조건식 | [WaPo](https://www.mapbox.com/blog/washington-post-s-electoral-maps-how-we-built-it): 동일 실제 렌더 좌표·ID 연결 점검. 선택은 N과 동일 | 노출; 화면 좌표 미고정 |
| RV1/RV2: 회전/정렬, ID 불명 | [#3974](https://github.com/vega/vega/issues/3974), [#3975](https://github.com/vega/vega/issues/3975) | 각도 bbox, align overwrite 확인 | [CMS](https://www.eecs.harvard.edu/~shieber/Biblio/Papers/tog-final.pdf) 대체 위치; 구현 결함에는 무효 | 둘 다 노출, 차트 종류 미확정 |
| RG1: 1–20; 특히 7,8,9,11,17 | [#139](https://github.com/slowkow/ggrepel/issues/139) seed1234, dotplot center stack, direction y | 표시된 stack 좌표와 원 ID 결합; 1–20 후보 | [WaPo](https://www.mapbox.com/blog/washington-post-s-electoral-maps-how-we-built-it) 실제 변환 좌표 포인터; N과 동일하면 추가 없음 | 노출; 실제 ID 매핑 미확인 |
| RG2: A–J red/blue | [#153](https://github.com/slowkow/ggrepel/issues/153) 두 레이어 | 공통 충돌 패스 필요; ID/순서 불명 | [Esri weight](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/text/prevent-labels-from-overlapping-certain-features.html) 보호 대상 공유; 우선권 입력 없음 | 노출; 레이어 독립성 |
| C1: label 하나 (30,30), 점(0,0) | [#3336](https://github.com/vega/vega/issues/3336) 100×100 | 원 anchor를 보존; hover 색 변경으로 위치 이동 금지 | [Imhof](https://giscience-research.github.io/geog281a/readings/wk5/Imhof-1975.pdf) 소속 유지, N과 동일 | 노출; 실제 고정판 없음 |
| C2: ggrepel 단일 레이블 | [#173](https://github.com/slowkow/ggrepel/issues/173) 후보는 선 차트 제외 | 결측 | 결측 | 미모집 |

주의: 표1의 WaPo/PSU 등 지도 제작 사례 링크 일부는 봉인 뒤 읽은 보강 출처이며, 봉인 당시 M의 근거는 predictions.csv에 적힌 M-IMHOF/M-CMS/M-ESWEIGHT뿐이다. 표1의 근접·원거리 링크는 당시 예측을 재작성한 것이 아니라 봉인 조건을 사후 설명하는 연결이다. 사전 선택을 주장하는 경우 반드시 봉인 CSV 원문을 사용한다.

단위: 사건-레이블 ID; 예측 파일 12 슬롯×4=48행(S 모두 표시/일괄 숨김, N 근접, M N+귀속 보호 한 조건, U N+무관한 파일명 일관성). 모집 예정 자연 6+대조 2; 임시 자연 6·예비 4·대조 노출1/결측1, 자연순위 확정 0. frame 원 검색 180행(79 Vega, 62+39 ggrepel), 20 중복, 160 고유 후보; C2 결측 행 별도. 최초 body 이미 출력 보고 11, 미노출 확정 0, 날짜·제목 스크리닝 불완전. 정확한 방향/선택 ID를 추측해 채우지 않았다. 지도 원전은 brief가 알려 줬으므로 발견 성과 0.

| 예측 커밋·대조군 | 실제 출력 또는 기대 그림 주소 | 관측값 | 예측이 갈린 이유 | 판독 한계 |
|---|---|---|---|---|
| d250d3667857 S/N/M/U V1 | [#3376](https://github.com/vega/vega/issues/3376) | 최초 보고: 우측 막대 이름만 표시, padding20 | local/global 경계 오류; M으로 해결 안 됨 | 그림 열리지 않음, 후속 댓글 0; 무효 |
| 같은 SHA V2 | [그림1](https://user-images.githubusercontent.com/37225856/185753246-3059fc8a-368f-437e-a491-38c8539301b0.png), [그림2](https://user-images.githubusercontent.com/37225856/185753261-7036c26c-4d70-45ad-89b2-6c7c6842f33c.png), [수정 보고](https://github.com/vega/vega/issues/3558#issuecomment-1236399384) | 실제 보고 화면 Vega5.22.1/editor7063a88: L1/L2 우측 겹침, L3 위/점 겹침, L4 좌/위 아래축 침범, L5 보이지 않음. Hover L1 왼쪽 잘림/x,y NaN, L2 먼 우측, L4 위 이동. 수정 보고 drift 없어짐, multiline 겹침 잔존 | N reactive geometry + 측정 결함, M 소속 보호 시험 추가 | 그림 2장은 한 사건; 수정 이후 실제 ID 미측정; 노출 무효 |
| 같은 SHA V3 | [그림](https://user-images.githubusercontent.com/26147504/235805671-d9eda3ce-8d03-4efc-b0a5-2b1ac0020b47.png), [후속](https://github.com/vega/vega/issues/3746#issuecomment-1535210256) | 실제 캡처 좌상단 텍스트 덩어리; 작성자 local 5.24·5.25 정상 보고 | editor 환경, M 추가 선택 무관 | 이름 판독 불가; 버전/환경 혼입 |
| 같은 SHA G1 | [#95](https://github.com/slowkow/ggrepel/issues/95) | 당사자 작은 크기/범위 외 hjust에서 overlap | device 의존, 지도 원리 추가 없어도 설명 | 이미지 실패, 후속 없음; 무효 |
| 같은 SHA G2 | [별도 합성 예제 댓글](https://github.com/slowkow/ggrepel/issues/101#issuecomment-369690540) | G1 mean(1.55,.822), G2(1.84,1.64) 출력 값, 집계 코드 | N 이미 one-per-group, M 면 가정은 별도 | 실제 sLF 아님; 기대/제안, 무효 |
| 같은 SHA G3 | [수정 사양](https://github.com/slowkow/ggrepel/issues/125#issuecomment-454591393), [채택](https://github.com/slowkow/ggrepel/issues/125#issuecomment-454597995) | 전체 50행, 빈 문자열로 선택; 작성자 채택 | N과 M 같은 선택. 좌표 정체성 우선 | 그림 실패; 채택 보고≠실제 픽셀 |
| 같은 SHA RV1/RV2 | [#3974](https://github.com/vega/vega/issues/3974), [#3975](https://github.com/vega/vega/issues/3975) | 회전 겹침, 정렬 변경 최초 보고 | 측정/출력 문제 | 별도 결과 미확인 |
| 같은 SHA RG1 | [중간 출력](https://github.com/slowkow/ggrepel/issues/139#issuecomment-512803467), [추가 동률 문제](https://github.com/slowkow/ggrepel/issues/139#issuecomment-521144029) | y=-.9442121 세 점 stackpos=-1,0,1; 다른 geom 제안, 나중에 순서 뒤섞임 보고 | 동일 y 정렬은 stable ID가 아니다; N/M 귀속 제약 | 원 그림 실패, 정확 ID 불명 |
| 같은 SHA RG2 | [원 그림](https://user-images.githubusercontent.com/6883382/80376553-e4e3ef00-8891-11ea-8c75-e8065120f29a.png), [유지자](https://github.com/slowkow/ggrepel/issues/153#issuecomment-620001266) | A–J red/blue 겹침, C/G 등 이중 글자. 레이어 간 의존 불가 보고 | 공통 충돌 정보가 없으면 어떤 우선순위도 무효 | 수정 출력 없음 |
| 같은 SHA C1/C2 | [#3336 수정 제안](https://github.com/vega/vega/issues/3336#issuecomment-985897427); C2 없음 | 한 label의 reactive geometry 교정 제안 / 결측 | N/M 같음; 부작용 여부를 볼 대조였음 | C1 노출, C2 결측 |

단위: 12개 슬롯; 실제 이미지 직접 판독 4개(3 사건 V2/V3/RG2), 이미지 실패 6회; 그림 판독 가능 자체가 독립 관측은 아니다. 별도 후속 댓글을 실제 실행/기대 fixture/희망으로 혼합하지 않음. 정확한 ID-level 후속 비교 가능한 쌍 0, 유효 분모 0; 일치 0/반대 0/유효 미판독 0(분모 자체 없음), 제외 12(노출11·결측1). 조건부 같은 선택 G3/C1 등은 설명이지 적중이 아니다. V1/G1/RV1/RV2 등 비교용 후속 출력 없음; 원 이슈 내 실제 화면 및 보고와 후속 출력의 구분은 outcomes.csv에 유지. 외부 원리 예측력 미확인.

| 권할 근접·원거리 링크 | 새 선택·반례·추가 조건 | 해당 마크·전제 | 무효가 되는 경우 | 미확인 |
|---|---|---|---|---|
| N [Vega label](https://vega.github.io/vega/docs/transforms/label/) / M [PSU point association](https://courses.ems.psu.edu/geog486/node/557) | V2: 두 점에 동일 거리/잘못 귀속 후보 reject 시험; 근접 위치와 독해 구별 | point·텍스트, leader 없는 경우 | 범례가 귀속을 이미 완전히 표시, 또는 구현 drift | 독자 실제 오독률 |
| N [ggrepel examples](https://github.com/slowkow/ggrepel/blob/0.9.6/vignettes/examples.Rmd) / M [Esri weights](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/text/prevent-labels-from-overlapping-certain-features.html) | G3/G199: 라벨 없는 장애물도 유지; 경계/내부 가중치 구분 후보 | 점 또는 막대의 보호 부분을 명시 | 동일 빈 문자열 장애물로 충분, 막대 내부 글씨가 가치를 명료화 | 사용자가 보호할 mark/값 |
| N [G139](https://github.com/slowkow/ggrepel/issues/139#issuecomment-512803467) / M [WaPo](https://www.mapbox.com/blog/washington-post-s-electoral-maps-how-we-built-it) | RG1: 변환 후 좌표로 leader 끝 연결; 동일 y 정렬 오류 시험, 축값을 인위 이동하지 않음 | 점마다 stable ID가 있는 경우 | ID 없는 집계 bin은 개별 귀속 불가능 | original row→stackpos mapping |
| N [G101](https://github.com/slowkow/ggrepel/issues/101#issuecomment-369690540) / M [Imhof](https://giscience-research.github.io/geog281a/readings/wk5/Imhof-1975.pdf) | G2: cluster 대표점 또는 경계 내 label. 군집 겹침·다중 모드에서 centroid 오해 시험 | 명시적 그룹/영역이 있을 때 | 비연속/중첩 군집에 실제 면 이름처럼 배치하면 오해 | sLF, 의미적 그룹 경계 |
| N [Vega Label.js](https://github.com/vega/vega/blob/v5.16.0/packages/vega-label/src/Label.js) / M [People Map](https://medium.com/mapbox/how-the-pudding-team-uses-mapbox-4b5b8577001f) | V3/G201: 생략된 레이블에도 mark 표시, 중요도/상태를 독자에게 노출, zoom 시 재표시 | 의미 있는 사용자 순위 명시 | Wikipedia 인기도나 큰 값이 chart 목적과 무관; legend/색 중복 | 우선순위 미제공 |
| N [G153](https://github.com/slowkow/ggrepel/issues/153#issuecomment-620001266) / M [Mapbox optimize](https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/) | RG2: cross-layer compositing, C1: 줌 이전 위치 우선; anchor/sort는 기존 중복 | 공유 충돌 공간·상태별 invariant | 레이어별 독립 API, hover에서 지리적 zoom 비유 부적절 | 공통 geometry/스케줄러 |
| N [ggrepel NEWS](https://ggrepel.slowkow.com/news/) / M [Kern–Brewer](https://cartographicperspectives.org/index.php/journal/article/download/cp60-kern-brewer/pdf/1397) | G1/G95: 생략률·겹침·선호 위치·연결 정확성 별개 측정; 수동 수정으로 선호 방향 악화 가능 | 최종 화면과 원본 ID 확보 | label count 하나만 최적화하면 정보 훼손 | 차트 효과 크기 |
| N [V3746](https://github.com/vega/vega/issues/3746#issuecomment-1535210256) / M [CMS](https://www.eecs.harvard.edu/~shieber/Biblio/Papers/tog-final.pdf) | 외부 링크 추가 선택 없음: Editor vs local 환경을 먼저 고정 | V3 모든 영화 텍스트 | runtime 결함이 지배할 때 지도 원리 무효 | 정확 editor 버전/재현 |

단위: 적용 후보 8행, 사전 성과 0. 원거리 링크는 설계 선택·시험 후보와 반례 설명일 뿐 검증된 성능 상승이 아니다.

## Q1–Q7
**Q1 — 대상과 목적.** V2에서 5개 label과 점/축, V1에서 막대 그룹, G3에서 원 행과 선별 대상, G139에서 bin 이후 점 위치를 분리했다. G101은 tSNE 데이터 없는 채로 group 이름이 중요하다고 보았으나 그룹 순위는 미제공. V3는 제목 전체가 대상이며 우선순위는 없음. G1의 device 크기가 조건이다. 입력과 출력 노출은 전수 inputs.csv로 표시. C2·정확 자연순번은 미확인.

**Q2 — 가까운 구현.** D-VLABEL v5.16.0 default anchor 순서는 top-left,left,bottom-left,top,bottom,top-right,right,bottom-right, offset 1, padding 0; sort 옵션과 avoidMarks, opacity가 있다. D-VLAYOUT comparator→공유 bitmap→place; 각 data opacity0에서 시작한다. 이는 그 버전 소스 값이지 2022–24 이슈 실행값이 아니다. D-G070은 0.7.0의 force 및 direction, D-G096은 0.9.6의 device-dependent grob, seed, max.overlaps 10(0.9.0에 도입; D-GNEWS2), 빈 label도 point obstacle 유지(0.6.0부터). 모든 표시와 전부 숨김은 각각 밀집에서 겹침/정보 전부 소실 위험을 드러내는 단순 기준이다. 이미 제공되는 sort/anchor/repel은 외부 발명 아님.

**Q3 — 원거리 원리.** Imhof p130은 축척에 따라 같은 지물이 점/면이 됨을 보여 준다. CMS Fig1 p2는 8개 이산 후보와 위치 페널티를 두되 항상 최적 위치는 아님. Esri weight는 지물 0–1000, 1000 회피; polygon 내부/경계 가중치 분리, 독립 priority는 표기의 순서다. PSU의 East Gate 위치 대안은 소속 명확성, Shawnee Nieman Center 간격/다른 label 이동은 공간의 상호작용. WaPo는 좌표계에 맞춘 leader, The Pudding은 명시된 popularity 계층과 숨은 이름 표시, Kern–Brewer는 하수도 map-book에서 Maplex가 거의 7% 더 표시·둘 다 약 93% 무겹침, 수동 수정에서 모든 겹침 제거하지만 선호 위치 지표 9% 하락(원논문 abstract/screenshot p22). Darwin tutorial은 Point Farewell 가운데 정렬/West Alligator River 단순 곡선과 annotation용 강제 표시. Nova Scotia 제작자는 검은 물의 의미를 유지할 조건에 레이블을 포함했다. 반대로 그래프의 범례는 공간 지명 아님, 막대 내부에 값 표기를 허용하면 map barrier 금지를 그대로 쓰면 안 됨, 군집은 실제 지리 영역이 아닐 수 있음.

**Q4 — 예측.** 동결 SHA d250d3667857506f1c4d2be470e51759a530259c, S/N/M/U 48행. 결과 보기 이전이라는 절차는 후속 댓글·첨부를 기준으로만 충족, 최초 본문 노출로 모든 비교가 오염. U는 N+파일명 일관성으로 기하학 무관. M은 귀속 보호 한 조건만 추가하고 순위가 없으면 ID를 발명하지 않음. 위치 후보와 판독 불가를 같은 형식으로 기록했다. 방향·개별 ID가 동결되지 않은 경우에는 효과 판정 불가.

**Q5 — 출력.** 표2 및 O-/IMG- 원장. V2와 V3, RG2 실제 작성자 이미지 4장; V2 수정은 작성자 보고, G3 수정 코드/채택, G2는 합성 예제 출력 숫자, RG1은 빌드 중간값/다른 geom 제안. 실제 fixture는 확보하지 못했고, 동일 버전·폰트·viewport로 N/M 재실행하지 않았다. 다음 첫 행동은 아래 약점 표 참조.

**Q6 — 반증.** 근접 도구만으로 설명되는 G3: 전체 행 유지(공식 예제 및 0.6.0 NEWS), V2: reactive geometry로 hover drift 해소 보고, V3: Editor bug, RG2: 레이어 의존 없음. 지도 추가 조건이 나을 후보는 V2의 잘못 귀속과 RG1 실제 stackpos 연결, 그러나 근접 geometry를 올바르게 사용하면 중복된다. 지도 방법을 잘못 옮기면 G101에서 겹치는 tSNE 군집을 지역으로 해석, V1에서 막대 사이 읽기 순서/높이 값 의미 훼손, G201 순위 부여 시 작은 값의 중요도 삭제 가능. Mapbox anchor/sort/충돌은 이미 N과 겹친다. Mapbox의 줌에서 이전 anchor 우선은 상태 변경 후 의도가 바뀌면 반례. Darwin처럼 자동 배치 단계의 강제 표시가 최종 수동 정리에 유효할 수 있어 all-hidden 기준을 보편 규칙으로 삼지 않는다. 독립 사용자 평가 없음.

**Q7 — 탐색기 권장 조건.** 직접 링크에는 버전, mark type, geometry space, 보호 대상, 읽기/연결 실패와 대체 후보, 증거 종류를 붙인다. 가까운 구현 링크 먼저. 지도 원문은 우선순위/label association/보호 지물 구분/생략 상태 표시 중 근접 문서가 하지 않은 시험을 만들 때만 추가. V3처럼 실행 환경 문제에는 외부 링크가 아무것도 더하지 못한다고 남긴다. 데이터가 충분하면 ID-방향-이유를 비교하고 그렇지 않으면 질문/조건 링크를 제공.

## 조건부 대안
우선 질문(실제 사용자에게 지금 질문하는 것이 아니라 미래 탐색기의 분기): **어떤 레이블을 반드시 보존하고, 어떤 점·선·막대 부분을 가리지 않아야 하는가?** 답이 중요한 레이블 목록이면 [Vega sort/avoidMarks](https://vega.github.io/vega/docs/transforms/label/)와 [The Pudding의 의미 기반 우선순위/누락 표식](https://medium.com/mapbox/how-the-pudding-team-uses-mapbox-4b5b8577001f)을 함께 권한다. 답이 점 귀속/실제 위치라면 [ggrepel jitter/빈 문자열](https://github.com/slowkow/ggrepel/blob/0.9.6/vignettes/examples.Rmd)와 [WaPo projected leader](https://www.mapbox.com/blog/washington-post-s-electoral-maps-how-we-built-it)를 권한다. 순위가 없는 경우 기본 N, 동일 표시 후보만 비교. 부정확한 point association을 막는 것이 실제 요구가 아니면 외부 원전 추가 없음.

## 추가 분석·분모
자료 원장 73행; 산입된 원자료/보충 고유 work 42, 명시적 계보 ID 36(독립성의 보수적 대용이지 독립 관측 실증 아님). 지정 유형의 입력6, 구현4(버전별 work; 동일 Vega 계보 2), 지도 원전/규칙4(Esri 두 문서는 같은 계보), 지도 결정4(노바스코샤는 label 의미 보호 결정이며 위치 이동 직접 수치는 없음), 보충24, 별도 출판·고정 비교 결과0. 즉 유형 하한은 최대 18/22, 엄격한 위치 이동 사례만 보면 17/22. 42건 총량으로 미충족 유형을 상쇄하지 않는다. 접근 실패9(이미지6), 같은 사건 댓글/그림은 분리 출처 행이되 중복 work 산입 금지. 그림 확인 4; 댓글의 수정 사례 다수는 동일 issue 계보. 원목록 전체 body 및 모든 재시도/읽기의 행별 로그 완전성 미확보; frame에는 제목/노출/미확인 구분. 중앙 제어 상태와 자체 PARTIAL 구분. 제품 선택·DB/검색/Studio 수정 없음.

후속 Codex 입력 최소 조건: V2의 정확 issue body spec 원문과 comment-1236399384 수정 spec, Vega5.22.1/editor7063a88, 300×300 + padding5, 실제 sans-serif 폰트 파일명·버전 및 renderer, L1–L5 stable IDs와 출전 캡처; ggrepel G3 exact reprex + R/ggplot2/ggrepel version·font·device 및 50개 행/seed. 재렌더 2회 및 별도 기대 fixture·기록의 차이 검사; 해당 실행은 이 작업에서 하지 않음. 이 사건은 retrospective regression만 가능; 새 미노출 자연 사례의 사전 검정과 분리한다.

| 불일치·약점 | 영향을 받는 판단 | 다음 조사·원자료 | 결론이 바뀌는 관측 |
|---|---|---|---|
| 자연순위 0 확정, 11 노출/1 결측, 유효쌍 0 | 외부 예측력, 적중률 | frame.csv 원 검색(2017–25) created/number 정렬·pagination, 최초 edit 이력/분리된 input-only fixture, C2 확보 | N≠M인 미노출 사례가 동일 고정 결과에서 ID별로 판독 |
| 결과 출판 유형 0/4, 이미지 6 실패, 버전·font 누락 | 화면에서 선택된 실제 ID, 각도·생략 비교 | #3558 두 수정 사양/원 그림, #125 reprex 결과 원본, #139 stable row ID; 별도 PR·릴리스·fixture 4 work | 별도 고정 결과의 ID·방향과 출력 조건 확인 |
| 원거리 조건이 N과 중복 또는 읽기 의도 왜곡 | 링크 추천의 추가 가치 | [CMS](https://www.eecs.harvard.edu/~shieber/Biblio/Papers/tog-final.pdf), [Kern–Brewer](https://cartographicperspectives.org/index.php/journal/article/download/cp60-kern-brewer/pdf/1397), [Mapbox](https://docs.mapbox.com/help/dive-deeper/optimize-map-label-placement/); mark association blind reader test | 같은 near 기하·우선권에서 M만 새로 막은 오귀속 또는 M이 오독을 증가시키는 사례 |
