# 지도 밖에서 같은 위치의 의미가 달라지는 조건

| 분야·원문 | 시작 조건과 보존할 값 | 지도에 옮길 수 있는 질문과 경계 |
| --- | --- | --- |
| Audacity Selecting Audio · AU01 | Selection Tool에서 파형을 끌어 시간 범위를 만든다. 기존 경계에 충분히 가까워진 곳에서는 경계 커서가 바뀌고 한쪽 시간을 조절한다. 트랙 멤버십과 포커스는 시간 양끝과 분리해 조작할 수 있다. [경계](https://manual.audacityteam.org/man/audacity_selection.html#Extending_or_contracting_an_existing_selection) · [포커스](https://manual.audacityteam.org/man/audacity_selection.html#Focus_versus_selection) | 같은 시간 x라도 파형, 범위 경계, 트랙 조절부가 받는 동작이 다르다. 지도에서도 x 또는 Canvas 태그 뒤에 실제 지도 객체와 보존할 좌표를 요청할 수 있다. |
| Audacity Moving Clips · AU02 | 파형 위 Clip-handle을 끌면 클립을 옮긴다. 선택 범위 안의 handle이면 선택 영역과 여러 클립이 함께 움직이고 밖이면 한 클립만 움직이며 기존 시간 영역이 남는다. 윗모서리의 trim 및 Alt 늘이기는 또 다른 동작이다. [클립 이동·경계](https://manual.audacityteam.org/man/audacity_tracks_and_clips.html#Moving_Clips) | '선택 있음' 하나로 부족하다. 어느 객체의 어느 부분이 hit였고 시간 영역 안이었는지 가른다. 범위와 클립이 함께 이동해도 오디오에서는 매뉴얼에 맞는 동작일 수 있다. |
| Audacity 작성자 사례 · AU03–04 | #12487의 Ctrl/Cmd+클릭은 범위 시간의 경계를 조정하려는 의도에서 트랙 멤버십을 바꿨다고 보고됐다. 후속 댓글의 두 트랙 범위 합치기는 다른 확인 조건이다. #8331은 Shift로 고른 여러 클립에서 한 handle만 이동한 보고다. [트랙 선택](https://github.com/audacity/audacity/issues/12487) · [후속](https://github.com/audacity/audacity/issues/12487#issuecomment-6525546367) · [클립 선택 방식](https://github.com/audacity/audacity/issues/8331) | AU3·AU4 조작을 섞지 않는다. 입력에 modifier와 시간 영역 선택·클립 객체 선택의 종류가 있어야 해당 절을 적용한다. 실제 오디오 앱, 영상 및 패치 버전 재생은 미실행이다. |
| Vega 원 사양 · VE01–02 | `@overview:pointerdown`는 새 양끝을 x에 놓고 `@brush:pointerdown`는 기존 양끝과 x를 기억한다. 이어지는 move에서 brush 경로는 두 끝에 같은 델타를 더해 구간을 옮기고 detail 축 domain을 갱신한다. 면 mark는 interactive:false다. [발행 예제의 원 사양](https://vega.github.io/vega/examples/overview-plus-detail/) · [이벤트 대상을 고르는 문법](https://vega.github.io/vega/docs/event-streams/#event-stream-objects) | 새 선택을 만들 때와 이동 폭을 유지할 때의 실제 receiver와 보존값을 다르게 질문할 수 있다. 이 예제는 v6 스키마이고 지도에는 별도의 복수 수신 규칙이 있다. |
| Vega-Lite 선택과 원 보고 · VE03–04 | 고정 선택 문서의 translate는 brush 이동 옵션을 연결한다. 현재 발행판에서 기본 내부 드래그, false, modifier를 비교한다. #8628 opening의 막대와 빈 plot은 화면에서 유사한 드래그의 서로 다른 선택 결과를 보고한다. [고정 선택](https://github.com/vega/vega-lite/blob/1ff500a596b51f579d622c2559a4e7ca3f5d8cdd/site/docs/parameter/select.md#L177-L192) · [현재 선택](https://vega.github.io/vega-lite/docs/selection.html#translate) · [원 사례](https://github.com/vega/vega-lite/issues/8628) | 입력의 기존 brush와 실제 item을 알아야 구간 이동 절을 돌려준다. 선택 폭·원 데이터의 보존을 구분한다. #8628 첨부·저자 런타임과 chart 재현은 이번 조사에서 미실행이다. |

| 읽는 사람 | 먼저 받을 최소 단서 하나 | 보존값과 활용 |
| --- | --- | --- |
| 지도 조작자 | 문제 순간에 어느 쪽이 남아야 했는지 한 문장 | 피처를 편집하면 피처 ID와 view center, 화면을 탐색하면 geometry와 피처 ID. 피처를 바꾸는 목적이면 사전 선택 필요 여부를 이어서 확인한다. |
| 라이브러리 저자 | trusted down 한 번의 순서가 있는 `handleDownEvent`·`stopDown` 반환 기록 | 피처 ID, world geometry, view center, 해상도와 회전의 변경을 분리한다. 같은 hit가 두 시퀀스를 시작했는지 판독할 수 있다. |
| 접근성 검토자 | 같은 목표에 이르는 드래그 없는 클릭·탭 경로 한 건 | 목적에 따라 원 피처 또는 view 상태가 보존되는지 확인한다. 키보드 이용은 별도 판정이다. 지도 출처에는 focus된 화살표 pan 예가 있고 W3C는 드래그 없는 단일 포인터 대안을 설명한다. [지도 키보드 예](https://openlayers.org/en/latest/examples/accessible.html) · [WCAG 2.2 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) |

오디오·차트와 접근성 행은 원전에서 확인한 계약·문제 보고의 비교다. 마우스 본행은 Canvas 지도 한 판, 한 DPR에서 실행했다. 키보드 조작, 터치 조작, WebGL 및 다른 렌더러에서의 동등한 결과는 미실행이다.
