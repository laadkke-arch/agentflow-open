# AF-RES-109 모집 사전 판독 교정

## 판독 범위와 실제 노출

- 기록 시각: 2026-11-24 01:47:57 UTC에 시계를 직접 확인했다. 최초 판독 메시지의 별도 UTC 타임스탬프는 추출하지 않았다.
- 판독 주체: 주작업자와 분리된 협업 에이전트 `protocol_review`.
- 열람 입력: 자기 작업의 `.cache/initial-0.json`, `.cache/initial-1.json` 두 파일에 담긴 현재 opening post의 제목·본문·작성시각·URL·작성자 필드.
- 주작업자의 잠정 포함/제외 의견은 판독 전에 제공되었다. 따라서 이 기록은 그 의견을 모르는 독립 이중 코딩이나 맹검 판독이 아니다.
- 본 검토자는 검색질의 실행, 검색결과 열람, issue 댓글·후속·해결표시 열람, 연결된 이미지·영상·외부 링크 개봉을 하지 않았다. 다른 PLAN#27 작업의 산출물도 읽지 않았다.
- 주작업자는 모든 A/B 검색 전에 이 교정을 수용하고 모집을 고정한다고 확인했다. 본 검토자가 직접 관측한 범위는 검색결과를 받지 않은 사전 판독과 교정 전달이며, 다른 세션의 전체 실행 이력을 독립 감사하지는 않았다.
- 허용된 쓰기는 이 기록 파일 하나다. 본 검토자는 다른 파일을 수정하거나 커밋하지 않는다.

## 입력 식별

| 파일 | 포함 issue | 바이트 | SHA-256 |
| --- | --- | ---: | --- |
| `.cache/initial-0.json` | node-red/node-red 4505, 4507, 4508, 4509 | 6312 | `1a5f2b286f554fb2d083da634e798c2f23b3b81e3b3eb2e9dda3ca108a11673a` |
| `.cache/initial-1.json` | xyflow/xyflow 3757, 3758, 3759, 3765 | 4048 | `58b75d4335a9c149d2811e4ea8905d4f27504bf01fac3f7706e40735cb079b54` |

이 검토는 두 파일의 첫 네 행씩에 대한 의미 판독이다. 저장소별 최초 80개 모집틀 전체의 누락·정렬·PR 제외 여부를 별도로 검사한 기록은 아니다. 최초 요청판을 새로 확보하지 않았으므로 현재 opening-post 탐색층이라는 제한이 유지된다.

## 검색 전 교정과 최종 첫 세 자리

| 층·원순위 | 현재 opening post | 대상·목적 | 원문에서 읽는 조건 1 | 원문에서 읽는 조건 2 | 판독 |
| --- | --- | --- | --- | --- | --- |
| Node-RED 1 | [4505](https://github.com/node-red/node-red/issues/4505), 제목·Current Behavior·Expected Behavior·본문 마지막 문장 | flow 메뉴에서 실제 편집 기능을 찾을 수 있게 함 | 메뉴 명칭을 열린 편집 대화상자의 기능과 맞게 변경 | 번역된 메뉴에도 수정 반영 | 포함. 사례가 단순하다는 이유로 제외하지 않는다. |
| Node-RED 2 | [4507](https://github.com/node-red/node-red/issues/4507), Current Behavior·Expected Behavior·Steps To Reproduce | flow 속성 pane을 통해 이름 변경 | flow 이중클릭 경로에서 속성 pane 표시 | 표시된 pane을 통해 flow 이름 변경 가능 | 포함하되 두 조건의 독립성이 약하다고 표시한다. |
| Node-RED 3 | [4508](https://github.com/node-red/node-red/issues/4508), Current Behavior·Expected Behavior·Steps To Reproduce | global credential 값 보존 | 기존 credential 값을 inject를 통해 정상 조회 | 새 plaintext global 변수 추가·조회 경로 갱신 후에도 기존 credential 값 유지 | 포함. 기존값·추가 경로·관측된 실패값이 본문에 있다. |
| xyflow 1 | [3757](https://github.com/xyflow/xyflow/issues/3757), feature 본문 두 문단 | 겹치는 node의 선택 영역 제어 | 일부 영역에서 다른 node로 click-through | 해당 node를 선택하여 삭제할 가능성 유지 | 포함. selectable과 drag handle은 이미 제시된 시도로 기록한다. |
| xyflow 2 | [3758](https://github.com/xyflow/xyflow/issues/3758), 제목·본문 마지막 문장 | 다중 edge 배치를 위한 예시·참고 확보 | 같은 node에 여러 edge 연결 | edge 사이 간격 자동 조정 | 포함. 제목은 원문 일부다. 이미지 미열람으로 이 두 명시 조건까지 삭제하지 않는다. |
| xyflow 3 | [3759](https://github.com/xyflow/xyflow/issues/3759), Describe the Bug·Steps·Expected behavior·Additional context | Windows viewport의 pinch zoom 복구 | Windows pinch 동작이 viewport 확대·축소 수행 | panOnScroll=true인 설정에서 동작 | 포함. zoomOnPinch=true 시도는 이미 알려진 안이다. |

## 교정 이유와 유지할 결손

1. **NR4507:** 주작업자의 잠정 의견은 pane 표시와 이름 변경을 한 목적의 반복으로 보고 제외하는 것이었다. 그러나 pane 자체가 나타나지 않는 실패와 pane은 나타나지만 이름을 바꿀 수 없는 실패는 구분할 수 있다. 두 조건이 서로 관련된다는 사실을 이유로 앞선 자연 요청을 빼고 더 풍부한 후순위 사례로 교체하면 선택편향이 생길 수 있다. 다만 이 둘을 강하게 독립적인 설계 제약이라고 주장하지 않는다. 이후 후보 적합성 판독에서 해당 약점을 유지한다.
2. **XY3758:** 주작업자의 잠정 의견은 그림 조건을 확인하지 못했다는 이유로 제외하는 것이었다. 제목에는 같은 node의 다중 edge와 자동 간격이 직접 적혀 있으므로, 그림이 없어도 이 두 조건은 읽을 수 있다. 그림의 간격 수치·균등성·방향·곡선 형식·정확한 시각 배치는 여전히 미확인이다. 그런 추가 조건을 연구자가 합성하지 않는다.
3. **원순위 유지:** 따라서 Node-RED는 4505/4507/4508, xyflow는 3757/3758/3759를 첫 세 자리로 고정한다. 4509와 3765는 후순위이며 검색 성과를 본 뒤 승격한 대체 사례가 아니다. 이 교정은 검색 결과를 얻기 전에 이루어졌다.
4. **최초판 결손 지속:** 현재 opening post의 판독 가능성과 생성 시점 최초판의 검증은 별개다. 이 검토로 최초판·편집 이력 결손이 해소되지 않는다. 특히 4509에는 Edit 표기가 직접 있으나, 다른 행에 Edit 표기가 없다는 사실도 원판 증명으로 사용하지 않는다. 검증되지 않은 최초판에 근거한 엄격 역사 비교의 분모를 늘리지 않는다.

## 수용 범위

주작업자가 이 교정을 수용했다. 수용한 것은 현재 opening-post 탐색층에서의 원순위 첫 세 행 모집과 결손 표시다. 최초판 확보, 전체 80개 모집틀 검사, 후보 검색 성공, 두 방법의 우열, 실제 개발자의 후속 선택을 확인했다는 뜻은 아니다.
