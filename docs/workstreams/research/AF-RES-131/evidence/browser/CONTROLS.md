# 대조와 래퍼 없는 경계 재생

| 입력 | 예정·실행·비교 가능 | down의 구별과 정착 |
| --- | --- | --- |
| 같은 좌표의 양성 ① | 8·8·8, 본행 참조 | 모든 판에서 hit `parcel-01/owned`, filter와 layers 각각 down 2·전체 4회 true, geometry (+72,−40). |
| 배경 드래그 | 8·8·8 | 초기 raw hit ∅, filter 0·layers 3회, center (−64,+36). 레이어 조회만으로 피처 hit가 있었다고 판단할 수 없다. |
| 피처 무이동 클릭 | 8·8·8 | hit 유지, Translate down 수락, filter와 layers 각각 down 2회, pointerdrag 0회와 두 값 유지. 정착 후 Select의 singleclick이 목록을 채웠다. |
| 피처 문턱 이내 이동 | 4·4·4 | 경계 각 판 ×2, 가장 먼 축 차 3px. down 수락과 callback 각 2회, pointerdrag 0회. geometry·center 유지. |
| Translate 미등록 | 4·4·4 | 경계 각 판 ×2, 동일 hit·포인터 이동과 설정값에서 Translate 수신 없음, 사용자 callback 0회, center만. |
| 목록 단독·5px tolerance | 4·4·4 | 경계 각 판 ×2. 두 predicate를 생략했으며 선택된 점이 두 판에서 geometry만 이동. #12638의 6.6.1 앱에서 보였다는 현상은 이 fixture에서 재현되지 않았다. |
| ④·⑤ 래퍼 없는 정착 | 8·8·8 | 경계 각 판 각 셀 ×2. 거부/허용 기능은 그대로이고 live observer와 predicate 로깅이 없다. 각 반복의 geometry·center·해상도·회전·선택이 본행과 정확히 같다. |

R1과 R2는 새 BrowserContext다. 별도 대조 16, 보충 12, 정착 전용 8을 본 48에 더해 예정·실행·비교 가능 각각 84다. ①의 8회는 두 분모에 넣지 않았다. 76개는 브라우저 포인터·콜백까지 비교하고 8개는 정착만 비교한다. 6.0.0에는 Translate condition API가 없지만 filter·layers는 있다. filter 자체가 없던 6.0.0-beta.9는 소스로만 봤다. [원장](../../runs.jsonl) · [대조 stdout](controls.stdout.log) · [보충 stdout](supplement.stdout.log) · [래퍼 없는 stdout](bare.stdout.log)

동일 6.6.1 hit에서 ①→②·③은 공급한 한 predicate의 반전이다. ②의 filter false와 ③의 layers false는 서로 다른 단계에서 Translate를 통과시킨다. 구형 ④도 filter false, ⑤도 layers false를 관측했다. 6.7.0에서 ②·③의 동일 predicate는 효력이 남고, 목록을 넣은 ④·⑤에서만 호출되지 않은 채 geometry가 움직인다. 새 ⑥은 같은 0회에서도 빈 Collection의 포함 검사로 geometry를 유지했다. 적용 가능성 판정에는 raw hit, 양성·거부 조건 반전, 옵션 지원, 실제 receiver, drag 이벤트, 움직인 값이 모두 쓰인다. [구형 ④](main/main-6.6.1-04-r1.json) · [신형 ④](main/main-6.7.0-04-r1.json) · [신형 ⑥](main/main-6.7.0-06-r1.json) · [미등록](supplement/supplement-6.7.0-disabled-r1.json) · [래퍼 없는 ④](bare/bare-6.7.0-04-r1.json)

down에서 사용자 layers 호출이 3회였던 거부·빈 hit 행은 세계 좌표 wrap 후보 세 개를 통과하는 코드와 일치한다. 한 lookup에서 실제 Feature 후보는 0 또는 한 건이다. 성공 down은 현재 hit와 cursor 갱신을 위해 두 lookup을 보이며 각각 첫 layer→filter에서 끝났다. 횟수의 차이는 “조건 무시”의 증거에서 제외하고 콜백 단계·반환·관측한 geometry/center를 함께 사용한다. [Map renderer의 wrap offsets와 layerFilter](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/renderer/Map.js#L120-L164) · [Translate down](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Translate.js#L232-L259)
