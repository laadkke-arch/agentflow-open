# 공간 예측 봉인 전 재판독

검토 기록 시각: 2026-11-22T22:15:49Z. 대상은 당시 `requests.csv` M01–M03, `predictions.csv` M01-P1–M03-P2 및 `sources.jsonl`의 연결된 원문 레코드다. 수신 이슈의 댓글·PR·릴리스·종료 상태는 열지 않았다. 제공 원문을 조사한 동일 모델의 별도 문맥 재판독이며 외부 독립 평가가 아니다.

## 봉인 전 수정 필요

| 행 | 문제 | 최소 수정 | 판정 영향 |
| --- | --- | --- | --- |
| M03 요청·P2 | `.5/.99`, `.5/.099`는 실제 colorbar data limits가 각각 `[0,.99]`, `[0,.099]`이고 선형·정방향이라는 가정에서만 성립한다. matrix min/max가 colorbar axes limits와 동일하다고 아직 실행 확인하지 않았다. | 일반식 `(0.5-ymin)/(ymax-ymin)` 및 선형·정방향 가정을 먼저 명시하고, 구체적 숫자는 limits가 min/max와 같을 때의 연구자 계산으로 한정한다. | 좌표계가 달라진다는 예측은 유지된다. 정확한 수치를 관측값·당대 명세로 승격하는 것을 막는다. |
| M02-P2 | CSS §8.2에서 font·figure 고정만으로 ‘clip만 남음’이 논리적으로 보장되지 않는다. 회전과 여러 sheet로 분할도 원래 fallback에 있다. | 단일 장·orientation 보존까지 연구자가 고정한 경우에 한해 clipping을 남은 fallback으로 적고, 원요구자가 말한 것과 연구자 조건을 구분한다. CSS는 legend만 layout에서 제외하는 API를 명세하지 않는다. | 두 후보가 같은 조건부 결과를 낸다는 가설은 가능하지만 직접 CSS 결정으로 세지 않는다. |
| M02 요청·P1/P2 | ‘데이터 axes 크기 보존’의 비교 기준이 모호하다. 성공한10-entry 그림과 legend없는 같은 figure는 bbox가 다를 수 있다. | 같은 figure에서 legend가 layout에 참여하지 않는 명시적 대조 또는10-entry 대조 중 하나를 정하고, 정확히 그 기준을 기입한다. | 후속 자료가 다른 기준으로 확인했을 때 같은 입력·출력 지지로 묶지 않는다. |

## 원문과의 대응 확인

**M01:** SD06 [USGS L186–199](https://www.usgs.gov/educational-resources/topographic-mapping)의 합성 교정쇄→확인·승인→인쇄 및 SD04 [Adobe CS6 PDF657–658](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf)의 preflight는 출력 전 확인 순서를 뒷받침한다. 요청·예측이 `한 번 pre-draw`를 연구자 가설로 명시한 것은 적절하다. 제공 원전이 한 번/두 번 draw나 Cartopy 호출 순서를 정한다는 주장으로 바꾸지 않는다. `different_conditional`은 무조건적인 설계 판별 성공이 아니다.

**M02:** `choice_b`는 실제 그리기를 유지하고 layout bbox에서만 제외한다고 명시하여 omission과 clipping을 구분했다. SD01의 지도 배치 정책, SC01 [QGIS Rendering L553–558](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html)은 해당 API의 성공을 보장하지 않는다. 현재 `exact bbox API not entailed` 및 `same_conditional` 표기를 유지해야 한다. 원작성자가 clipping과 font/figure 고정을 이미 요구했으므로, 이 후보의 후속 일치를 새로운 해결책 발견으로 세지 않는다.

**M03:** SD04 [Adobe CS6 PDF300–301/인쇄295–296](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf)의 페이지 기준 anchor와 line 기준 anchor 구분은 실제 규칙이다. SD02 [CSS2013 §6 Table1](https://www.w3.org/TR/2013/WD-css3-page-20130314/)은 컨테이너 경계 중심이라는 참조 프레임을 제공한다. 수신 `transAxes`는 당시 API와 연구자가 연결한 구체 조작이지 원전의 명령이 아니다. M03-P2는 동일 data value를 보존하지만 최초 요청의 ‘값 범위와 무관한 중앙’을 이미 어긴다. 따라서 후속 지지가 생기더라도 **원요구에 대한 좌표계 해석의 확인**이며 두 미지의 유효 설계 중 새로운 승자를 발굴했다는 결과가 아니다.

## 산입·분야·판의 확인

공간 원문 배당은 SD01/SD02/SD04/SD06 4저작, 별도 비교 SD03/SC01 2저작이다. 후보가 SC01을 참조하더라도 한 저작을 donor와 comparison 두 배당에 더하지 않는다. Esri·QGIS는 수신과 인접한 시각화 소프트웨어이며 CSS는 인쇄 포매터 소프트웨어다. 세 분야를 완전히 먼 분야라고 부르지 않는 현재 문구가 적절하다. USGS의 물리적 분판·교정쇄는 별도 인쇄 생산 작업이다.

원문 날짜 미확인 및 당시 가용성의 한계는 sources에 남아 있다. Adobe PDF metadata와 Esri10.3 edition 표지만으로 정확한 최초 웹 공개일을 단정하지 않는다. 이번 검토는 성공 사례를 늘리는 목적으로 후보나 입력을 바꾸지 않았으며, 공유 CSV는 직접 편집하지 않았다. root가 위 수정 여부와 적용 행을 별도로 기록한 뒤 봉인해야 한다.
