# 도너 원전 조사 — 사례 배정 전

작성자: 동일 모델의 `/root/donor_sources` 보조 에이전트. 조사 범위는 인쇄·지도 원전과 발행 이력이며 Vega-Lite/libass 후보 이슈·해답·후속 PR·시험을 읽지 않았다. root가 사례별 D를 고르기 전의 원전 탐색 보조 자료다. 독립 채점 또는 도너 효과 실험이 아니다.

## 원전과 판

| 저작 ID | 직접 읽은 저작·판 | 고정 위치 | 역할과 중단 조건 |
| --- | --- | --- | --- |
| D-P01 | W3C CSS Paged Media Level 3, 2013-03-14 Working Draft | [§6.3.2.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/#variable-auto-sizing), §6.3.2.4, [§6.4 도판 4·6](https://www.w3.org/TR/2013/WD-css3-page-20130314/#margin-box-ex) | 가운데·여백·넘침의 우선순위를 설명하는 원전. Working Draft이고 수신 엔진 규격이 아니다. |
| D-P02 | W3C XSL 1.1, 2006-12-05 Recommendation | [§7.16.13 wrap-option](https://www.w3.org/TR/2006/REC-xsl11-20061205/#wrap-option), [§4.5 Line-areas](https://www.w3.org/TR/2006/REC-xsl11-20061205/#area-line) | 줄바꿈과 줄 높이의 서로 다른 경계를 설명한다. 텍스트의 발화 시각·자막 충돌·도표 값 대응은 보장하지 않는다. |
| D-M01 | QGIS 2.18 User Guide/Manual, 관련 파일 마지막 2020년 이전 변경 2018-07-16 | [원 사이트 Rendering](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html#rendering-tab), [9e1c449… 원본 RST](https://github.com/qgis/QGIS-Documentation/blob/9e1c449188baa5c258f30aac57ec6d0dd52b4d46/source/docs/user_manual/working_with_vector/vector_properties.rst#L1199) | 충돌 시 일부 표기를 감추는 선택과 강제 표시를 나눈다. 이름 전부 보존이 목표면 자동 생략을 성공으로 세지 않는다. |
| D-M02 | QGIS 2.18 Training Manual, 해당 절 마지막 2020년 이전 변경 2017-02-15 | [§4.2.5 Labeling Lines](https://docs.qgis.org/2.18/en/docs/training_manual/vector_classification/label_tool.html#follow-along-labeling-lines), [305f0bb… RST L171–235](https://github.com/qgis/QGIS-Documentation/blob/305f0bb402d3331430ee8490c34f5e2f9d7172fb/source/docs/training_manual/vector_classification/label_tool.rst#L171) | 실제 지도에서 배치와 표기 손실을 함께 보여 준다. 도판은 QGIS 2.0.1 화면이므로 2.18 실행 증거로 부르지 않는다. |
| D-M03 | Ordnance Survey GeoDataViz Toolkit, Cartographic Design Principles, 2019-11-18 SHA 424bccc… | [Legibility L71–81](https://github.com/OrdnanceSurvey/GeoDataViz-Toolkit/blob/424bccc4f95f15d354a74c716e62c8592c4b10d3/Cartographic%20Design%20Principles/README.md#L71) | 지도 판독 조건을 독립 발행자가 서술한 자료. 픽셀 임계값·특정 엔진·개별 조작 승패를 제공하지 않는다. |

고유 저작은 통상 저작 단위로 인쇄 2·지도 3=5개다. 두 QGIS 매뉴얼은 서로 다른 제목·목차·용도의 저작이지만 발행자와 설명 계보가 겹친다. QGIS 전체를 하나로 합치는 보수적 계산도 인쇄 2·지도 2=4개다. 같은 저작의 웹·RST·이미지·다른 SHA는 추가 저작이 아니다. 검색 결과와 실패 요청을 고유 저작 수에서 제외한다.

## 1. 인쇄 원전에서 실제로 읽은 범위

**D-P01.** §6.3.2.2는 가운데 박스의 중앙 정렬, 넘침·겹침 최소화, 내용량에 비례한 공간 배분의 순서를 명시한다. §6.3.2.4는 좌·중·우 박스의 배치 기준을 정한다. §6.4 도판 4에서는 가운데 박스가 페이지 중앙을 차지하고 왼쪽 짧은 박스가 남은 쪽에 놓인다. 도판 6에서는 가운데 내용이 없어 긴 왼쪽 문구가 중앙선을 넘을 수 있다. 같은 레이아웃 이름이라도 보존 목표의 우선순위와 점유 상태가 다르다. 이 규칙을 축 눈금에 적용해 위치를 이동하면 값-좌표 대응을 해칠 수 있으며, 표기를 삭제해도 좋다는 규칙은 아니다. 제작자 목표는 유한한 페이지 여백 안에서 주어진 머리말·꼬리말의 배치를 정하는 것이다.

**D-P02.** §7.16.13은 자동 줄바꿈을 하지 않는 경우와 가용 폭을 넘을 때 줄바꿈하는 경우를 구분하며, no-wrap의 넘침은 별도 overflow 설정으로 넘긴다. §4.5는 요청한 줄 사각형과 실제 inline 영역까지 감싸는 최대 줄 사각형을 구분한다. 원 도판에는 큰 라틴 글자와 다른 모양의 glyph가 요청 높이 밖으로 확장되는 모습이 있다. 그러므로 고정 줄 높이 자체는 실제 잉크의 비겹침 보장이 아니다. 이 문서는 자막 이벤트 시간·동시 발화 우선순위·ASS 태그 기본값을 정하지 않는다. 제작자 목표는 콘텐츠를 일관된 영역·줄·글리프 배치로 조판하는 것이다.

## 2. 지도 원전에서 실제로 읽은 범위

**D-M01.** Formatting은 지정 문자에서의 줄바꿈과 상대 위치를 따르는 정렬을 나눈다. Placement는 지물 유형별 후보 위치와 충돌 우선순위를 다루며, Rendering은 읽기 어려운 겹침에서 일부 라벨을 숨기거나 모든 라벨을 표시해 수동 수정하게 할 수 있다고 한다. 곡선·평행·수평의 원 도판을 직접 확인했다. 같은 문자열과 선에서도 지물 방향을 따르는 정도가 달라진다. 지도 작성자의 선택은 지물과 이름의 대응 및 읽기 쉬움을 함께 다룬다. 도표의 모든 범주명을 요구하거나 자막의 모든 발화를 요구할 때 이 생략 정책을 그대로 쓰면 목표를 바꾼다.

**D-M02.** Labeling Lines 실습은 도로 이름의 중복 병합·짧은 지물 억제·곡선 배치를 순차 적용한다. 두 실제 지도 그림을 열었다. 앞 그림에는 하단 Station Street의 반복 표기가 보이고 마지막 그림에는 표기가 줄어 있다. 문서는 곡선을 따라가면서 읽기 쉬움을 지키기 어려운 라벨이 사라진다고 설명한다. 다만 그림 사이에는 여러 설정 변화가 있어 한 조작의 인과 효과나 정확한 누락 수를 도판만으로 계산하지 않는다. 화면 제목은 `QGIS 2.0.1-Dufour`, 축척 표시는 `1:4917`이다. 설명의 2.18 판과 그림의 실행판을 분리한다.

**D-M03.** Legibility 절은 글꼴·대비·크기·간격·마스크와 주변 표기의 근접성을 함께 다룬다. 지도 용도와 축척에 맞게 일반화할 필요가 있으며 가능한 곳에서 겹침을 피하도록 한다. 수치 한계나 완전 라벨 수를 보장하지 않는다. 제목·색인을 통한 추가 원전 후보로 보관하며, 사례별 첫 적격 절이 QGIS에 있으면 이를 후순위의 더 유리한 결과로 교체하지 않는다.

## 3. ≤200단어 카드에 사용할 수 있는 절 후보와 절단 규칙

아래는 후보 창의 주소·시작/끝만 고정한 목록이다. 각 사례의 입력·A/B를 보기 전이므로 **D 카드 선택·예측은 아직 미실시**다. 긴 원문을 이 파일에 복제하지 않는다. 실제 보여 주는 카드의 본문·단어 수·그림 한 점은 root의 cards.csv에 따로 기록해야 한다.

| 후보 | 제목·색인 검색 순서 | 최초 관련 절·창 | 그림 후보 | 정보 예산 주의 |
| --- | --- | --- | --- | --- |
| DP-01 | CSS 목차→margin boxes→variable dimension | §6.3.2.2 첫 설명 문단부터 순서대로 최대 200 whitespace 단어; 첫 200단어로 완결 안 되는 마지막 문장 제외 | §6.4 도판 4 하나 | 위치 규칙은 다른 절이다. 둘을 합쳐 한 절처럼 표시하지 않는다. |
| DP-02 | CSS 목차→margin boxes→positioning | §6.3.2.4 전체 세 위치 항목 | §6.4 도판 4 하나 | 짧은 절은 200단어를 채우지 않는다. I/D 실제 길이 차이를 기록한다. |
| DP-03 | CSS 목차에 wrap-option 없음→XSL 속성 색인 wrap-option | §7.16.13 전체(설명·값·기본값·조건) | 없음 | 해당 절의 wrap과 no-wrap 양쪽을 읽으며 overflow의 구체값을 외부 지식에서 채워 넣지 않는다. |
| DP-04 | XSL 목차→Area Model→Line-areas | §4.5 도입부터 최대 200단어, 마지막 완결 문장까지 | Nominal and Maximum Line Rectangles 한 점 | 이 창에서 최대 rectangle 정의까지 실제 보이는지 확인. 잘리면 그 정의를 봤다고 쓰지 않는다. |
| DM-01 | QGIS2.18 목차→Labels→Formatting | Formatting tab의 첫 문단(원본 RST L970–978) | 없음 | 지정 문자 wrap과 align 설명. 자동 폭 기반 줄바꿈으로 바꾸어 읽지 않는다. |
| DM-02 | QGIS2.18 목차→Labels→Rendering | Rendering tab에서 collision 키워드가 있는 문단 RST L1224–1231; 앞의 z-index 문단은 창 밖 | 없음 | 원 절의 한 문단을 택했다는 사실, z-index·우선순위가 창에 없다는 사실을 기록한다. |
| DM-03 | QGIS Training 목차→Labeling Lines | §4.2.5 곡선 선택 직전 문단부터 절 끝(RST L222–235) | final_street_labels 하나 | 앞 단계의 merge/suppress를 창 밖 지식으로 구분한다. 그림은 2.0.1 화면이다. |
| DM-04 | OS 목차→Legibility | 2019 SHA README의 Legibility 전체 L71–81 | 없음 | 일반론뿐이면 두 구체 조작을 가르는 카드로 쓰지 않는다. |

## 4. 도판 판독과 접근 한계

원 도판 URL·다운로드 SHA256·직접 판독 범위는 `figure-observations.json`에 있다. W3C PNG/GIF와 QGIS 공식 저장소의 도판을 `view_image`로 실제 보았다. QGIS 원 웹 이미지 URL은 web 도구에서 이미지 참조를 반환했지만 픽셀을 도구 응답으로 제공하지 않았으므로 그것을 판독 성공으로 세지 않았다. 직접 HTTP 요청은 403이었다. 같은 발행자의 공개 GitHub 원본으로 재열람했으며 미러를 새 저작으로 계수하지 않았다.

QGIS2.18 문서의 두 RST는 2020년 이전 마지막 변경 SHA의 바이트와 현재 release_2.18 사본이 동일하다. 마지막 지도 도판도 2014년 파일과 동일하다. 이는 문헌 선행성의 증거이며 소프트웨어 동작의 별도 재실행이 아니다. 이력 조회의 공개 REST 경로는 403을 반환했으나 기존 연결의 GitHub 도구로 같은 공개 이력을 읽었다. 실패와 성공을 모두 영수증에 남겼다.

## 5. 노출

2026-11-23 약 01:31 UTC에 보조 에이전트가 root에 CSS 우선순위·XSL wrap·QGIS 숨김 정책의 짧은 요약을 전송했다. root가 A/B 봉인 전 노출로 기록하도록 요청했다. 이후에는 상세 원리·문구를 메시지로 보내지 않았고 파일 준비 상태만 보고한다. 원전 후보를 찾은 이 과정은 블라인드 조작 선택의 증거가 아니다.
