# 공간·인쇄 제공 원리 — 결말 열람 전 조사

작성자는 수신 이슈·댓글·PR·릴리스를 열지 않았다. 아래 M01–M03 요구는 root가 전달한 최초 본문 요약에만 의존한다. 제공 원리와 수신측 예측의 구체화는 연구자의 해석이며, 역사적 영감 또는 실제 채택의 증거가 아니다.

기록 완료: 2026-11-22T22:05:59Z. 원장 `spatial-donor-sources.jsonl`은 직접 열람, 실패, 리다이렉트와 동일 저작의 추가 절을 모두 구분한다. 최소 배당은 제공 공간 원문 4저작(SD01/02/04/06), 독립 비교 2저작(SD03/SC01)다. Esri 여러 문서와 Adobe 여러 쪽은 각각 한 매뉴얼로 센다. OS의 다른 지침 SD05는 보수적으로 추가 산입하지 않았다.

## 원문에 있는 조작과 한계

| ID | 정확한 위치 | 조작·보존 조건·예외 | 판·시간의 한계 |
| --- | --- | --- | --- |
| SD01 | [Esri10.3 Maplex](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm), Labeling toolbar L66·L98–111, placement L125–145; [fixed-position shifting](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/shifting-labels-from-a-fixed-position.htm) L36–81 | 지도 제작자는 크기/위치를 잠그거나, fitting 전략·우선순위를 선택한다. 라벨의 작은 이동은 충돌을 줄이지만 방향별 offset 제약을 유지한다. [Never remove](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/forcing-the-placement-of-all-labels-in-a-label-class.htm) L36–49는 모든 라벨을 남기는 대신 겹침을 허용한다. | 10.3 보존판·footer2016. 정확한 최초 게시일과 동일 본문 당시 가용성은 별도 미확인. |
| SD02 | [CSS Paged Media2013](https://www.w3.org/TR/2013/WD-css3-page-20130314/) §8.2 L819–828, §6 Table1 L436–461, §4.2 L176–189 | 인쇄 포매터는 넘치는 페이지에 더 큰 용지→회전→비례 축소→분할→잘라냄 순으로 대응한다. 머리말/꼬리말은 페이지 영역의 경계를 기준으로 배치한다. 페이지 밖 모든 객체의 처리는 규정되지 않는다. | 2013-03-14 명시판. Working Draft이며 최종 권고가 아니다. 인쇄 포매터는 수신 시각화와 가까운 소프트웨어 분야이기도 하므로 순수 비소프트웨어 전이로 부르지 않는다. |
| SD04 | [Adobe CS6 공식PDF](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf), PDF35–36/인쇄30–31, PDF226/인쇄221, PDF300–301/인쇄295–296, PDF657–658/인쇄652–653 | 페이지 기준 anchor와 텍스트 line 기준 anchor를 구분한다. 전자는 텍스트 재흐름 중 페이지의 자리를 유지한다. Layout Adjustment는 새 guide/margin 관계를 따르지만 열 안내선을 드래그하는 것 자체는 발동 조건이 아니다. Preflight는 출력 전 지정 오류를 찾는다. | 710쪽. 생성2012·수정2017 PDF metadata. 최초 공개 시점은 metadata만으로 증명하지 않는다. 텍스트만 추출했으며 전체 조판의 시각 검사는 하지 않았다. |
| SD06 | [USGS Topographic Mapping](https://www.usgs.gov/educational-resources/topographic-mapping), L24–26, L144–147, L186–199 | 지도 인쇄는 색 분판과 글자를 최종 교정쇄로 합친 뒤 정확도·가독성 등을 편집하고 승인 후 인쇄한다. 위치 정확도는 실제 지형점에 관한 기준이다. | 발행자가 historical reference로 표시한 온라인 책자다. 이 판의 게시일은 보이지 않으므로 날짜 미상 제공판이다. |

## 최초 요구에 적용하기 전의 경쟁 가설

| 요구 | 그럴듯한 후보 1 | 그럴듯한 후보 2·근접 오답 | 봉인 시 주의 |
| --- | --- | --- | --- |
| M01 / #13430 첫 저장의 배치 | SD06의 합성 교정쇄→확정→인쇄, SD04의 출력 전 preflight. 모든 변환이 반영된 기하를 확인한 뒤 첫 결과를 내보낸다는 운영 원리. | SD02의 이미 정해진 페이지 전체를 비례 축소하여 용지에 맞추기. 출력 영역이 문제라는 표면상 진단에는 맞는다. | 어떤 원문도 `draw` 2회나 Cartopy의 기하 갱신 순서를 말하지 않는다. 정상 입력에서 둘 다 같은 결과를 낼 수 있다. 경계 입력의 내부 축 비율이 뒤늦게 바뀐다면 최종 이미지 전체 scaling은 그 상대 배치를 고치지 못한다는 것은 **연구자의 구조적 추론**이다. 정확한 수신 API 검증이 없으면 예측 판별 불가를 남긴다. |
| M02 / #13522 큰 범례 | 지도상의 충돌 해결처럼 중요 본체·고정 영역을 보존하고 배치 불가능한 장식을 제외하거나 미배치로 표시하는 후보. SC01의 명시적 collision-hide는 별도 비교근거다. | SD01의 글꼴 축소·약어 또는 SD02의 전체 비례 축소를 적용하면 더 많은 내용을 넣을 수 있다는 후보. 모든 내용을 보존하려는 목표는 비슷하다. | 요구자가 font·figure를 고정했다면 축소·새 용지·분할은 조건 위반이다. 후보가 이 조건을 충족한다고 쓰지 않는다. `ignore in layout`과 `omit from drawing`은 다른 조작이므로 연구자가 대체해서는 안 된다. 지도는 라벨을 누락시켜도 다른 위치 참조가 있지만 범례 누락은 데이터 해독을 불가능하게 할 수 있다. |
| M03 / #13600 색막대 .5,.5 | SD04의 page-edge/page-margin anchor 또는 SD02 page-margin center: 텍스트 내용이 바뀌어도 컨테이너 비율 위치를 보존한다. | SD01의 feature-relative anchor: 의미상 동일 데이터 위치를 보존한다. 같은 숫자 `.5`가 글자 위치와 데이터값을 모두 뜻하는 것처럼 보이는 근접 오답. | page/axes fraction과 데이터 단위는 별개의 좌표계다. 값 범위를 바꿀 때 무엇을 불변으로 할지 먼저 정해야 한다. 단위를 반대로 바꾸면 정상 입력에서 우연히 겹쳐도 경계 입력에서는 갈린다. 분모의 영역을 명시하지 않은 50%는 예측이 아니다. |

## 독립 비교와 반증

SC01 [QGIS2.18](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html), L324–326은 겹친 점의 기호를 원 위로 옮겨 모두 보이게 하는 실제 기능이다. 따라서 ‘잘 보인다’가 ‘원래 좌표에 그린다’를 보장하지 않는다. L553–558의 라벨 숨김/전체 표시 전환은 자동 가독성과 완전성의 긴장을 보여준다. 이는 원시 데이터 변경이 아니라 **표시 기호 변위**다. 지도와 과학 데이터 시각화가 인접 분야라는 분류는 유지한다.

SD03 [OS Text on maps](https://docs.os.uk/more-than-maps/geographic-data-visualisation/guide-to-cartography/text-on-maps), L55–67은 이동한 라벨이 강이나 경계를 잘못 건너 의미를 바꾸는 것을 경계한다. 바닷가 이름을 물 위에 두는 예외도 있어 ‘모든 글자를 대상 좌표 위에 고정’하는 규칙으로 일반화할 수 없다. 이 현재판을 2019년 당시 원리로 소급하지 않는다.

비용 제약을 제거하면 M02의 큰 용지/축소/분할 선택은 다시 가능한 후보가 된다. 하지만 모두가 불변으로 정한 font·figure를 유지한 원 실험과 섞지 않는다. M03에서 요구를 ‘색막대의 중앙 설명’에서 ‘데이터값 .5의 주석’으로 바꾸면 권장 좌표계가 뒤집힌다. 이것은 원 요구의 개선이 아니라 목적 변경이다.

## 탐색 실패·재개

- USGS FS171-99는 발행자 서지/초록만 읽었고 공식 PDF는 웹과 셸 모두403이었다. 그 원문을 산입하지 않았다. 성공한 별도 Topographic Mapping 책자의 명시 조항만 사용한다.
- Adobe 현행 PDF 주소는2026 Desktop Help로 이동했다. 공식 CS6 archive URL을 별도로 열어11,543,420바이트·SHA256 `1fd595284749b6da5822af8c1b411b755f38fcd510bd4fe904724db4d26e72e5`를 확인했다. 전문은 재배포하지 않는다.
- Esri background-labels 직접 열기는 두 번 timeout이었다. 검색 요약의 ‘낮은 우선순위 미배치’ 문구를 직접 열람처럼 쓰지 않는다. QGIS의 직접 열린 collision-hide 절을 비교자료로 사용한다.
- OS Design Principles 경로의 최초 Git 커밋은2019-09-24, 수정은2019-11-18이다. February/March2019 요구에 앞선 공개판의 증거가 없다. 현재 Text on maps의 첫 공개일 역시 미확인이다.
- 수신 프로젝트가 이 제공 자료를 이미 인용했는지는 결과 열람 금지 때문에 조사하지 않았다. 결말 봉인 이후 프로젝트 문서/토론의 명시 인용을 확인해야 하며, 무검색·무인용을 ‘모르고 있었다’로 읽지 않는다.

이 문서는 제공 원전 작성자의 규칙과 연구자의 전이 가설을 구분하는 자체 조사다. 수신 프로젝트 후속 결말을 본 독립 판정이 아니다.
