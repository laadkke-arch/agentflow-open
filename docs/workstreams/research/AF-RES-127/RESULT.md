# AF-RES-127 · 같은 화면 위치의 드래그와 보존할 값

| 목적·사건 | 저자 근거 URL·판 | 대체 지도 입력·버전 SHA | 바꿀 값·보존값 | 실제 확인·미확인 |
| --- | --- | --- | --- | --- |
| 편집 · #9625의 플래그로 한 번에 피처 드래그 | 2019-05-31 opening과 06-03 작성자 후속 OI01–02. 당시 npm 공개 5.3.3과 6.0.0-beta.9에서 Translate의 피처 filter 부재 확인. [opening](https://github.com/openlayers/openlayers/issues/9625) · [작성자 후속](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656) | 로컬 Point parcel-01과 명시 배열. ol 10.11.0 · `88fc44564552176b761dbb9531f9977386d041c0` · [plan](plan.json) · [npm·파일 SHA](fixture/fingerprints.json) | geometry를 바꾸고 피처 ID와 view center·해상도·회전을 보존 | 선택 목록과 호출 순서를 바꾼 본행에서 geometry만 2/16과 두 값 동시 변화 2/16. 빈 선택과 filter 단독 통과에서 geometry만 2/2. 저자의 설치판·앱 좌표·배열·채택은 미확인. |
| 탐색 · 화면의 지도 pan | DragPan 계약 OL06A와 지도 등록 역순 OL01. [DragPan API](https://openlayers.org/en/latest/apidoc/module-ol_interaction_DragPan-DragPan.html) · [등록 역순](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/Map.js#L665-L674) | CSS 720×460, DPR 1, EPSG:3857, 해상도 2, CanvasVectorLayerRenderer. Chromium 156.0.8078.79의 실제 inline bundle `285f0b061c10ab7067482208ef49a8e8efe4fcb42a5a48807443b77386734f07`. [실행 환경](evidence/main/environment.json) | view center를 바꾸고 피처 geometry·ID, 해상도·회전을 보존 | 배경 8/8과 미선택 피처 4/4는 center만. 저자 앱의 DragPan 설정과 동일 동작 여부 미확인. |
| 판 이동 · filter와 선택 목록을 같이 쓰기 | v6.0.0은 filter 통과와 목록 포함을 같이 요구한다. 현행 10.11.0에서 features는 filter·layers를 우회한다. [PR #9638](https://github.com/openlayers/openlayers/pull/9638/files) · [6.0.0 구현](https://github.com/openlayers/openlayers/blob/55adb4ee33f6cd08b2b91511b5c9d2bdcc6f62e4/src/ol/interaction/Translate.js#L287-L299) · [10.11.0 구현](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Translate.js#L172-L215) | 같은 마우스 경로, 목록 유무와 Translate filter의 통과/거부를 보충 입력에 명시. [보충 입력](evidence/supplement/RECEIPT.md) | 필터 거부가 유지할 geometry, 편집 적격 hit에 보존할 view center | 10.11.0에서 기능 조합 확인. 과거판의 실제 마우스 재생, layers 조합의 브라우저 대조와 최초 변경판 미확인. |

| 셀·반복 | 시작 선택·위치·등록 순서 | 실제 hit·처리 순서 | geometry 전후 | view 중심 전후 | 결과·원 로그 ID |
| --- | --- | --- | --- | --- | --- |
| 1 · R1/R2 | 포함 · 피처 · P,T | parcel-01/owned · T0 → drag T | (-128,80) → (-56,40) | (0,0) → (0,0) | geometry만 · [M-in-feature-pan-translate-r1](evidence/main/M-in-feature-pan-translate-r1.json) · [M-in-feature-pan-translate-r2](evidence/main/M-in-feature-pan-translate-r2.json) |
| 2 · R1/R2 | 포함 · 피처 · T,P | parcel-01/owned · P1,T0 → drag P,T | (-128,80) → (-96,62) | (0,0) → (-64,36) | 둘 다 · [M-in-feature-translate-pan-r1](evidence/main/M-in-feature-translate-pan-r1.json) · [M-in-feature-translate-pan-r2](evidence/main/M-in-feature-translate-pan-r2.json) |
| 3 · R1/R2 | 포함 · 배경 · P,T | ∅ · T1,P1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-in-background-pan-translate-r1](evidence/main/M-in-background-pan-translate-r1.json) · [M-in-background-pan-translate-r2](evidence/main/M-in-background-pan-translate-r2.json) |
| 4 · R1/R2 | 포함 · 배경 · T,P | ∅ · P1,T1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-in-background-translate-pan-r1](evidence/main/M-in-background-translate-pan-r1.json) · [M-in-background-translate-pan-r2](evidence/main/M-in-background-translate-pan-r2.json) |
| 5 · R1/R2 | 밖 · 피처 · P,T | parcel-01/owned · T1,P1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-out-feature-pan-translate-r1](evidence/main/M-out-feature-pan-translate-r1.json) · [M-out-feature-pan-translate-r2](evidence/main/M-out-feature-pan-translate-r2.json) |
| 6 · R1/R2 | 밖 · 피처 · T,P | parcel-01/owned · P1,T1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-out-feature-translate-pan-r1](evidence/main/M-out-feature-translate-pan-r1.json) · [M-out-feature-translate-pan-r2](evidence/main/M-out-feature-translate-pan-r2.json) |
| 7 · R1/R2 | 밖 · 배경 · P,T | ∅ · T1,P1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-out-background-pan-translate-r1](evidence/main/M-out-background-pan-translate-r1.json) · [M-out-background-pan-translate-r2](evidence/main/M-out-background-pan-translate-r2.json) |
| 8 · R1/R2 | 밖 · 배경 · T,P | ∅ · P1,T1,S1 → drag P | (-128,80) → (-128,80) | (0,0) → (-64,36) | center만 · [M-out-background-translate-pan-r1](evidence/main/M-out-background-translate-pan-r1.json) · [M-out-background-translate-pan-r2](evidence/main/M-out-background-translate-pan-r2.json) |

P는 DragPan, T는 Translate, S는 Select다. 등록 배열 앞에는 언제나 S가 있다. 실제 down 열의 1/0은 각 interaction의 외부 `handleEvent` 반환 true/false이고, drag 뒤에는 실제 내부 drag 호출 순서를 적었다. 히트의 ∅는 빈 map query다. 본 16/16 전부 실행·비교 가능, 비교 불가와 미실행은 각각 0이다. 8/8 짝에서 상태 범주와 전후 좌표가 같았다. [실행 원장](runs.jsonl) · [본행 영수증](evidence/main/RECEIPT.md)

| 증거 A·B·C | 예측·보류·실측 가능 분모 | 맞힘·틀린 확정·추가 맞힘·소실 | 우선 기능 절 URL | 비용·반례·저자 적용 한계 |
| --- | --- | --- | --- | --- |
| A · 겉보기와 편집/탐색 의도 | geometry만 4셀, center만 4셀, 보류 0. 실측 8셀/16행 | 5 맞힘·3 틀린 확정. 기준선. 실측 뒤 우선 절 변경 3셀/6행. | [Translate 옵션](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Translate.js#L45-L63) · [DragPan 옵션](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/DragPan.js#L20-L33) | 겉보기와 의도 두 입력. 본행의 동일 PNG에서 선택·전파가 달라진다. 저자의 플래그나 사전 선택 요구는 화면 입력만으로 미확인. |
| B · 차트에서 가져온 선택·실제 down·보존 질문과 공개 설정 | center만 6셀, 보류 2셀. 실측 8셀/16행 | 6 맞힘·0 틀린 확정. A에서 2 추가, 1 소실. C 밖에 추가 맞힘 0. 실측 뒤 우선 절 변경 2셀/4행. | [DragPan 옵션](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/DragPan.js#L20-L33) · [보류의 필터 단서](https://github.com/openlayers/openlayers/issues/9625) | 시작 목록, down 후보, 보존값을 더 확인한다. B 전에 새 외부 열람은 이슈 opening 한 건이며, 선행의 지도 요약이 이미 노출됐다. 두 수신이 가능한 선택 피처에서는 결론을 보류했다. |
| C · 동일 설정과 지도 고유 계약·전달 | geometry만 1셀, center만 6셀, 둘 다 1셀, 보류 0. 실측 8셀/16행 | 8 맞힘·0 틀린 확정. B에서 2 추가, 소실 0. A 대비 3 추가, 소실 0. 실측 뒤 우선 절 변경 0. | [Map에서 전파](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/Map.js#L1310-L1326) · [Pointer에서 시퀀스](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Pointer.js#L125-L179) · [컬렉션·필터](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Translate.js#L172-L215) | Map·Pointer·Select·Translate·DragPan 다섯 고유 소스의 규칙과 등록 배열을 읽었다. 설정을 알 때의 상태 범주 정확도다. 처리 시점·픽셀 위치 변화량·저자 실제 배열은 별도 증거가 필요하다. |

## Q1 · 저자와 대체 지도의 목적

`#9625`에서 저자가 찾은 기능은 피처별 editable/draggable 플래그를 이용해 한 번의 press에서 피처를 끌 수 있는 판별이다. fredj의 Select filter 답변은 국가 이름을 검사한 뒤 선택 컬렉션을 이동하는 조합이다. 저자의 후속은 선택 클릭을 생략하고 싶다는 의도 및 자기 구현의 보고다. 저자 앱의 실제 down, geometry와 center 전후 값은 공개 미확인이다. 대체 지도에서 고른 geometry/center 보존 계약은 위 첫 표의 연구 입력이다. [원문 OI01](https://github.com/openlayers/openlayers/issues/9625) · [응답 OI02](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498230742) · [자료 대조](evidence/map-sources.md)

## Q2 · 사전 판정과 실행판

B의 원 조건과 보류는 `11c78d102bdee10b9de4f3c87475e5cd8136d11a`에 저장했다. 선행의 OpenLayers 예제·역순 전달 요약은 선노출로 표시했고 B 결정식에는 구현 세부를 넣지 않았다. A/C와 입력은 `ed2d7895451b3653d72fc7665a27281f2e20e1ee`에서 본행 전에 고정했다. A/B/C는 같은 작업자가 다른 입력 제약으로 작성했다. B의 조건부 경로는 관측이 들어와도 사전 정답으로 세지 않았다. [B 봉인](https://github.com/laadkke-arch/agentflow-open/blob/11c78d102bdee10b9de4f3c87475e5cd8136d11a/docs/workstreams/research/AF-RES-127/predictions.csv) · [A/C 봉인](https://github.com/laadkke-arch/agentflow-open/blob/ed2d7895451b3653d72fc7665a27281f2e20e1ee/docs/workstreams/research/AF-RES-127/predictions.csv)

npm gitHead와 annotated tag의 대상 SHA가 같다. 고정 소스·npm tarball·설치 12개 모듈을 byte 비교했다. tarball SHA-256은 `9e8377871c10e1299a8a302be847de3b8f1060a6d31063b90e84363c7e060477`이다. 브라우저에서 읽은 inline script SHA를 bundle과 대조했고, source 목록과 SHA는 build metadata에 보존했다. 2019 HTML API는 접근 실패여서 고정 5.3.3·beta.9·6.0.0 JSDoc과 구현에서 계약을 읽었다. 공개 발표와 어느 판을 실제 로드했는지는 분리한다. [지문](fixture/fingerprints.json) · [환경](evidence/main/environment.json) · [역사판 대조](evidence/map-sources.md)

## Q3 · 입력과 표면

선택 포함은 fixture가 `Select.getFeatures().push(parcel-01)`로 seed했다. 선택 밖의 컬렉션은 비어 있다. 클릭은 default singleClick이고 `style: null`을 제공한다. 16행의 화면 PNG와 중앙·배경·경계 지도 hit probe가 seed와 무관하게 같았다. 본행에서는 DOM down이 모두 CANVAS이며 중앙 hit는 parcel-01/owned 8/8, 배경의 공집합은 8/8이다. 두 처리기는 같은 primary·no modifier 조건으로 만들었고 명시 controls/interaction 배열에 기본 kinetic·zoom·rotate를 넣지 않았다. 고정 투영·해상도·DPR·스타일에서만 이 hit를 비교했다. [파일럿](evidence/pilot/RECEIPT.md) · [초기 표면](evidence/surfaces/51b9806235305c705fef7a4da697e19e31e4830120bd42571fa59b726b7bf062.png) · [Select 스타일 OL07](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Select.js#L45-L91)

## Q4 · 첫 이동과 정착

동시 처리 R1의 DOM down `seq 10`은 CSS (280,180), map (256,160), EPSG:3857 (-128,80), 463.0ms다. 첫 1px 이동 `seq 27`에서 map (257,160), 투영 (-126,80), 497.2ms를 기록했다. geometry·center 변화는 없었다. 문턱을 넘은 다음 이동의 DOM `seq 35`와 map `seq 43`은 (260,162), (-120,76), 546.4ms다. 이때 P는 centroid를 잡고 T가 geometry를 (-120,76)으로 옮겼다. 처음 center를 바꾼 P의 `seq 67`은 그 다음 drag이고, T `seq 73`은 이벤트의 기존 frame 좌표를 읽었다. `up seq 122` 748.3ms의 포인터 세계 좌표 (-120,76)는 정착 geometry (-96,62)와 달랐다. 실제 이동량은 `translating`과 geometry 값을 함께 봐야 한다. [원 로그](evidence/main/M-in-feature-translate-pan-r1.json) · [좌표 getter OL03](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/MapBrowserEvent.js#L69-L98) · [pan centroid OL06](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/DragPan.js#L93-L126)

입력 궤적의 최종 CSS Δ는 (+36,+20)이다. 해상도 2, 회전 0에서 T만 처리하면 지도 geometry Δ가 (+72,-40), 피처 화면 Δ가 (+36,+20)이다. P만 처리하면 두 번째 좌표 이후의 pan으로 center Δ가 (-64,+36), 피처 화면 Δ가 (+32,+18)이다. 둘이 처리하면 geometry Δ가 (+32,-18), center Δ가 (-64,+36), 피처 화면 Δ가 (+48,+27)이다. 단계마다 자연 rAF 두 번을 기다렸고 view의 up/settled 값은 모두 같았다. 좌표 델타의 부호는 EPSG:3857의 동/북과 화면의 오른쪽/아래를 분리해 계산했다. 본행 해상도·회전·피처 ID·선택이 전 단계에서 보존됐다. [실행 원장](runs.jsonl) · [geometry만의 표면](evidence/surfaces/346f90728d56edff4c13046947df756682a4c16495d57595cbcef9c9091f9759.png) · [둘 다의 표면](evidence/surfaces/d6b4e3f74e93982d383c5a6448431564b4ab9fe8ad64fdfa2a89d05ec2195efe.png)

## Q5 · 순서·문턱·필터의 반례

| 대조 조건 | 실행·비교 가능 | 실제 결과와 반례 |
| --- | --- | --- |
| 적격 피처, T만 | 2/2 | geometry만. [R1](evidence/controls/C-translate-only-r1.json) · [R2](evidence/controls/C-translate-only-r2.json) |
| 같은 피처, P만 | 2/2 | center만. [R1](evidence/controls/C-pan-only-r1.json) · [R2](evidence/controls/C-pan-only-r2.json) |
| 같은 피처, T/P 모두 끔 | 2/2 | pointerdrag와 동일 hit를 받고 geometry·center가 보존됐다. [R1](evidence/controls/C-both-off-r1.json) · [R2](evidence/controls/C-both-off-r2.json) |
| 동일 피처의 click | 2/2 | T가 down을 받아도 drag가 없어 두 값 유지. [R1](evidence/controls/C-click-r1.json) · [R2](evidence/controls/C-click-r2.json) |
| 경계 바깥, tolerance 0 | 2/2 | 빈 hit와 center만. [R1](evidence/controls/C-edge-zero-r1.json) · [R2](evidence/controls/C-edge-zero-r2.json) |
| 같은 경계 점, tolerance 6 | 2/2 | 6px에서 parcel-01/owned가 hit하고 geometry만. [R1](evidence/controls/C-edge-six-r1.json) · [R2](evidence/controls/C-edge-six-r2.json) |

6개 설정의 12/12를 실행했고 미실행·비교 불가 각 0이다. 동시 변화는 대조 0/12, 본행 2/16이다. 두 값 유지 결과는 대조 4/12, 본행 0/16이다. 보충 10/10 중 8은 입력부터 전파까지, 2는 live 옵저버 없이 정착만 비교했다. 문턱 이내 마우스 이동의 2/2는 down 수락 뒤 두 값 유지다. 선택 목록을 공급한 거부 filter는 0회 호출되고 geometry만 2/2였다. 같은 피처에 filter만 두면 거부 2/2는 center만, 허용 2/2는 빈 선택으로도 geometry만 움직였다. 해당 조합은 원 PR 및 6.0.0 당시 filter→목록 검사와 갈린다. 레이어 필터 결합, 여러 선택 피처, focus가 요구된 map, 실제 WebGL·키보드·터치는 미실행이다. [대조 영수증](evidence/controls/RECEIPT.md) · [보충 영수증](evidence/supplement/RECEIPT.md) · [역사 PR OI03](https://github.com/openlayers/openlayers/pull/9638) · [focus 반례 OI04](https://github.com/openlayers/openlayers/issues/11102) · [WebGL 보고 OI07](https://github.com/openlayers/openlayers/issues/14154)

## Q6 · 조건부로 반환할 기능 절

- **채택 · 적격 피처 이동.** 피처 ID와 view를 남겨야 하는 그룹 편집은 실제 hit와 선택 목록을 맞춘 뒤 Translate 수락이 pan보다 앞서는 조합에서 성립했다. 이때 피처 이동 절과 사용 중인 Select 컬렉션을 연결한다. 선행 클릭을 피하려는 편집은 version과 features 유무를 먼저 받아 Translate filter 단독의 절을 돌려줄 수 있다. [Translate 옵션 OL05A](https://openlayers.org/en/latest/apidoc/module-ol_interaction_Translate-Translate.html) · [컬렉션 OL07](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Select.js#L291-L298)
- **채택 · 중심 이동과 피처 보존.** 적격 피처가 없는 곳의 일반 드래그에는 DragPan을 우선 반환한다. 이미 보이는 피처를 움직이려는 요청에서 같은 결과가 확인되면 pan 원인에 선택/적격 조건을 붙인다. 모서리 바깥을 눌렀다면 0/양수 hitTolerance에 따라 먼저 읽을 절이 갈린다. [DragPan OL06A](https://openlayers.org/en/latest/apidoc/module-ol_interaction_DragPan-DragPan.html) · [hitTolerance 예 OE03](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/examples/hit-tolerance.js#L46-L92)
- **보류 · 피처 하나가 hit됐을 때 단일 승자.** 두 처리에서 요구한 보존값을 주고 down의 실제 수락·전파를 요청한다. pan이 먼저 true로 시작해도 stopDown=false라 두 시퀀스가 열렸다. 위치를 안다는 설명으로 이 동시 처리를 생략하면 B의 보류 두 셀에서 적용 조건을 잃는다. 클릭과 작은 이동은 수락된 down과 값 변화도 구분해야 한다. [Map OL01](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/Map.js#L1310-L1326) · [Pointer OL04](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/interaction/Pointer.js#L125-L179) · [이동 문턱 OL02](https://github.com/openlayers/openlayers/blob/88fc44564552176b761dbb9531f9977386d041c0/src/ol/MapBrowserEventHandler.js#L349-L421)

A→B의 새 맞힘은 미선택 피처 두 셀이다. A가 맞힌 선택·Translate 선행 한 셀은 B에서 보류됐다. C는 그 셀과 선택·Pan 선행의 동시 결과를 맞혔다. C가 이미 맞힌 범위 밖에 B의 추가 맞힘은 0/8이다. B의 가치는 정보가 적은 요청에서 빠진 단서를 묻고 확정 오류를 줄이는 선택지라는 해석이다. C의 설명을 그대로 돌려주면 판과 등록 설정의 읽기 비용이 든다. 16행의 보존값, 관측 뒤 우선 절과 목적에 맞는 후속 절을 남겼다. 현장 클릭, 실제 채택 및 시간 절감은 미측정이다. [봉인 예측](predictions.csv) · [16행 기능 절](returns.csv) · [검산 영수증](evidence/acceptance/RECEIPT.md)

## Q7 · 다른 분야와 최소 질문

지도 조작자에게 먼저 바꾸려는 값과 한 번의 누르기에서 꼭 남아야 하는 상태를 받는다. 라이브러리 저자에게는 trusted down 하나의 전달 결과를 받고, 접근성 검토자에게는 같은 상태를 만드는 드래그 없는 클릭·탭 경로를 받는다. Audacity에서는 파형 범위·경계·clip handle과 트랙 선택이 다른 결과를 내며, 시간 영역과 Shift로 고른 클립 집합을 구분해야 한다. Vega 예는 overview와 brush의 down을 따로 받아 새 구간을 그리거나 기존 양끝을 같은 양만큼 이동한다. 시간 축·클립 ID나 범위 폭을 보존할 목표로 각각 적는다. 지도에서 확인한 mouse 결과의 키보드·터치 또는 다른 renderer 이식은 미실행이다. [문서와 사례 및 역할별 단서](evidence/cross-domain.md)

원장 70행은 후보 URL 67개, 본문을 읽은 URL 50개, 접근 실패 시도 20개다. 현재 API 3개는 웹에서 본문 열람에 성공했고 별도 셸 경로에서 접근 실패했다. URL 중복 및 계보를 합치면 고유 외부 1차 저작 37개다. 지도 API/전달 13, 예제/회귀 7, 이슈/PR 6, 차트 4, 오디오 4, 접근성 1, 릴리스 2다. 메타데이터를 빼고도 35개다. 실패는 원장에 원인과 대체 경로를 저장했다. [출처 원장](sources.jsonl) · [질문별 자기검산](SELF_CHECK.md)

| 불일치·약점 | 다음 조사 자료·행동 | 판정을 바꿀 관측 |
| --- | --- | --- |
| 저자의 실제 앱의 판·옵션·down 및 좌표가 미확인이다. 과거판과 현재판의 filter 조합도 갈린다. | [#9625 작성자 후속](https://github.com/openlayers/openlayers/issues/9625#issuecomment-498282656)과 [판 대조](evidence/map-sources.md)에서 시작해 앱의 판과 features/filter/layers, down→첫 drag의 값을 한 건 확인한다. | 앱에서 제공한 판·필터의 적격 hit와 실제 center 또는 geometry 변화가 밝혀지면 반환할 옵션과 보존값을 앱에 맞춰 바꾼다. |
| 동시 처리의 이동량은 단일 Chromium·Canvas·DPR과 프레임 간격에서 얻었다. | [동시 처리 원 로그](evidence/main/M-in-feature-translate-pan-r1.json)의 입력을 연속 pointermove 간격, 다른 DPR/renderer 및 입력 장치에서 각각 대조한다. | 같은 hit와 down 수락에서도 첫 drag의 frame 변환 또는 정착 범주가 달라지면 이동량이나 범주 설명의 적용 범위를 좁힌다. |
| 같은 작성자의 A/B/C와 B의 지도 선노출이다. 링크 클릭·채택·절감은 미측정이다. | [예측 봉인](predictions.csv)과 [기능 절](returns.csv)을 가린 채 판·설정이 다른 사례에 독립 판독을 붙이고 실제 링크 선택·읽기 시간을 기록한다. | 지도 원문만으로 판단한 기준에 차트 질문을 더했을 때 새 맞힘·오류·열람비가 다른 표본에서도 달라지는지 본다. |
