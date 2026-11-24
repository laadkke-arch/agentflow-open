# 같은 위치가 다른 동작을 가리키는 사례

## OpenLayers 10.11.0

공식 Translate Features 예제는 미국 주 피처가 있는 vector layer, Select와 `features: select.getFeatures()`를 설정한 Translate를 지도 기본 interactions 뒤에 붙인다. 콜백은 역순으로 검사한다. 현재 좌표에서 관리 목록의 선택된 피처를 찾으면 Translate가 down을 잡고 지도 좌표의 변화를 geometry에 적용한다. 같은 지도 픽셀에서도 선택 목록 밖이면 Translate가 넘기고 기본 조건을 충족한 DragPan이 view 중심을 이동시킬 수 있다. feature의 지도 좌표와 카메라 view 중심이 서로 다른 보존 대상이다. 이 동작 순서는 공식 예제와 소스에서 도출했다. [실행 예제](https://openlayers.org/en/latest/examples/translate-features.html) · [Translate 히트 조건](https://openlayers.org/en/latest/apidoc/module-ol_interaction_Translate-Translate.html) · [Map 역순 전달](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/Map.js#L1311-L1325) · [DragPan](https://openlayers.org/en/latest/apidoc/module-ol_interaction_DragPan-DragPan.html)

사용자가 올린 #9625는 Select에 있는 필터를 Translate에도 적용하고 싶었던 사례다. 해당 기능은 이번에 읽은 판에서 inspection 가능한 `filter`다. 배경으로 보이는 같은 픽셀도 hitTolerance와 레이어 필터, 조건, 선택 컬렉션이 바뀌면 피처로 들어갈 수 있다. 위 예제의 판단을 특정 지도나 모바일 장치로 옮길 때 이 설정이 추가 입력이다. [사용자 사례](https://github.com/openlayers/openlayers/issues/9625) · [고정 후보 필터](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Translate.js#L375-L391)

## Audacity 시간 선택

Selection Tool로 파형에서 좌·우 drag를 하면 시간 범위를 그린다. 기존 선택의 경계 가까이에서 커서가 바뀌면 경계를 한쪽만 움직일 수 있다. Shift-click으로 경계를 잡는 조작과 시간 단위 및 물리적 clip 경계 snap을 문서가 별도로 설명한다. 동일한 화면 x에서도 파형의 선택 경계와 clip 상단 handle은 다른 동작을 건다. 선택 영역 내부의 clip handle을 끌면 선택된 여러 clip과 영역 위치가 함께 움직이며, 외부 handle을 끌면 그 clip이 이동하고 선택 영역의 시간은 유지된다. [선택 경계](https://manual.audacityteam.org/man/audacity_selection.html#Extending_or_contracting_an_existing_selection) · [Moving Clips](https://manual.audacityteam.org/man/audacity_tracks_and_clips.html#Moving_Clips)

AU4/Future #12487의 작성자는 단일 트랙의 시간 선택에서 바깥쪽 canvas를 Ctrl/Cmd-click했더니 그 트랙이 선택 대상에서 빠졌다고 보고했다. 기대 동작은 시간 경계의 확장·축소이고 트랙의 선택 여부는 헤더에서 조작하길 원했다. 지원하는 modifier와 구현의 의미를 매뉴얼의 Shift 조작과 혼용하면 잘못된 기능 절을 돌려준다. 옵션과 판을 확인한 뒤 범위의 시간과 트랙 ID를 따로 본다. [저자 입력·상태](https://github.com/audacity/audacity/issues/12487) · [선택 길이·시각](https://manual.audacityteam.org/man/selection_toolbar.html)

## 인계할 최소 단서

| 읽는 사람 | 가장 먼저 받을 단서 | 보존·판정 단서 |
| --- | --- | --- |
| 조작자 | 누르기 직전 기존 선택이 어디에 있었고 무엇을 누르는 의도였는지 한 문장 | 끝점 하나의 조정, 범위 전체의 이동, 새 범위 생성 중 원하는 결과와 유지할 상태 |
| 차트 작성자 | 선택의 x 채널, 조건 색의 param과 fallback, `translate` 및 `on`의 판별 설정 | 축·데이터와 선택 외부 색을 유지할 목적에 따라 projection, 이동, 표시를 조합 |
| 렌더러 구현자 | 브라우저 viewport·DPR와 첫 trusted down/move의 CSS 좌표, Vega item/parents, active tool | plot 및 unit origin, brush 픽셀과 투영 변화. 지도라면 feature ID·filter·view 중심도 함께 기록 |
| 접근성 검토자 | 포커스와 조작 장치, 동일 목표를 이루는 키보드·탭/클릭 경로 | 마우스 결론의 적용 범위를 제한. Audacity의 시간 입력·키보드 목록과 W3C의 두 모서리 클릭 예에서 별도 계약을 비교 |

이 도메인 대조는 각 원문에서 읽은 입력과 계약이다. 지도·오디오의 실제 실행과 키보드·터치의 성공률은 미측정이다. [키보드와 선택](https://manual.audacityteam.org/man/audacity_selection.html#Selecting_using_the_keyboard) · [드래그 대안](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)
