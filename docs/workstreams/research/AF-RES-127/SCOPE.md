# AF-RES-127 · 같은 지도 위치에서 피처 이동과 뷰 이동

탐색기는 부분 설계와 목적을 받아 적용 조건이 있는 기능 절을 반환한다. 편집 목적은 소유 피처 `parcel-01`의 지도 좌표를 바꾸면서 피처 ID와 뷰 중심을 보존하는 것이다. 탐색 목적은 화면의 지도를 옮기면서 피처 좌표와 ID를 보존하는 것이다. 두 목적 모두 해상도와 회전을 보존한다. 조작의 결과와 사용자의 목적 일치 여부를 따로 판정한다.

## 시작판과 원래 사건

| 입력 | 고정판과 확인 범위 |
| --- | --- |
| 계획과 시작판 | 계획 `4a92e22c5356dc7ea2b715f671077e8ab63b2835`, GitHub에서 받은 통합판 `5c0eca97d41e084a76bddd7cb0e976e5e9f792e8`. 그 사이 변경은 진행표의 과제 등록·배정이다. 자기 행의 의존은 AF-RES-123 한 건이다. [시작판](https://github.com/laadkke-arch/agentflow-open/tree/5c0eca97d41e084a76bddd7cb0e976e5e9f792e8) · [세션 manifest](manifest.json) |
| 선행 AF-RES-123 | 등록 인계 `7554304d725082275661cdd011ad4f4472a00438`, 검산 결과 `0a4acb5368e2f064e9b3eb21b52d219de262440f`. 선행 차트 대체판의 down hit·선택 오버레이와 보존값의 구분을 질문으로 옮긴다. 지도 요약에는 공식 예제, 선택 목록 적격성, 역순 전달과 DragPan의 예측이 이미 노출되어 있다. 이 노출은 B를 순수한 지도 비노출 시험으로 해석할 수 없게 한다. [인계](https://github.com/laadkke-arch/agentflow-open/blob/7554304d725082275661cdd011ad4f4472a00438/docs/workstreams/research/AF-RES-123/HANDOFF.md) · [검산](https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/RESULT.md) · [분야 대조](https://github.com/laadkke-arch/agentflow-open/blob/0a4acb5368e2f064e9b3eb21b52d219de262440f/docs/workstreams/research/AF-RES-123/evidence/cross-domain.md#openlayers-10110) |
| 저자 사건 | agpixdev가 Translate에도 Select와 같은 피처 판별 함수가 있으면 좋겠다고 요청했다. opening에는 제품 판, 사용 코드, 실제 선택 컬렉션, 포인터, 이동 전후 수치가 없다. [#9625 작성자 본문](https://github.com/openlayers/openlayers/issues/9625) |
| 실험과 접근 | Codex Cloud의 별도 GitHub checkout에서 OpenLayers npm `ol@10.11.0`과 선행이 지정한 소스 후보 `88fc44564552176b761dbb9531f9977386d041c0`를 대조할 계획이다. 외부 타일 없이 마우스 입력을 사용한다. 키보드, 터치, 실제 저자 앱 흐름, 차트 재생과 제품 구현은 이 실험에서 미실행이다. |

## 지도 전달 소스 열람 전 예측

본행의 공개 시험 사양은 단일 벡터 레이어의 원형 Point, 배경, 선택 시 스타일 교체 없음, `Translate({features: select.getFeatures()})`, 활성 DragPan, 같은 기본 버튼·modifier 조건이다. 매 행의 선택 목록은 빈 목록 또는 `parcel-01` 하나다. 중심과 같은 x의 배경을 각각 범위 안쪽과 충분히 떨어진 점으로 설계한다. 본행 hitTolerance는 0이다. 두 interaction의 배열 순서는 두 가지이나 실제 호출 우선순위는 B가 사용하는 전제에 넣지 않는다. CSS 위치·이동 궤적·비교 허용오차는 pilot 이후 본행 전에 고정한다. 시딩은 컬렉션 입력이고 측정 드래그는 브라우저 이벤트다.

- A는 겉보기 피처와 배경, 편집·탐색 의도만 입력받는다. 추후 A 기준열에 실제 상태를 가리기 전 예상 상태를 적는다.
- B는 시작 선택, 어느 적격 대상이 실제로 down을 받을 수 있는지, 바꿀 값과 보존값을 묻는다. 빈 컬렉션 또는 단일 마커에서 충분히 떨어진 배경이면, 기본 마우스 드래그를 받을 적격 피처가 없으므로 활성 pan이 조건을 만족한다는 공개 사양에서 center 이동을 예상한다. 선택된 마커의 중앙에서는 점 hit 자체가 가능해도 두 처리 중 어느 쪽이 시퀀스를 점유하는지 입력에 없다. Translate 점유 시 geometry, pan 점유 시 center, 둘이 처리하면 둘 다, 아무 처리도 안 하면 둘 다 유지로 두고 단일 판정을 보류한다. 이 보류를 실측 이후 맞힘으로 바꾸지 않는다.
- C는 같은 공개 지도 사양과 지도 원전을 받아, 등록 순서에 따른 차이를 예측한다. B가 커밋된 뒤에만 공식 Translate Features 예제, #9625의 응답과 현재·당시 API, 상호작용의 고정 소스를 읽는다.

본 규칙의 B 추가 입력은 시작 선택·목록, down 후보와 불확실성, 보존값의 세 묶음이다. 클릭, 임계 미만, 높은 허용오차, 전달을 바꾼 구현은 본행의 확정 전제를 깨뜨릴 수 있다. 같은 작업자가 A/B/C를 기록한다. 이 비교는 입력을 제한한 규칙 비교이고 사람의 독립 판독이나 클릭 선호 시험은 미실행이다. 차트의 101 CSS px와 월 범주를 지도 수치에 쓰지 않는다. [셀별 봉인](predictions.csv)

## 본행 실행 전 고정한 입력과 반환 후보

`predictions.csv`의 여덟 행에 A와 C를 추가했다. A의 판정은 보이는 피처의 편집과 빈 화면의 탐색이 각각 성공한다는 추측이다. C는 역순 전달, `handleDownEvent`가 여는 시퀀스와 `stopDown`이 막는 전달을 구별한다. T를 먼저 호출하면 선택된 hit에서 T만 down을 처리한다. P를 먼저 호출하면 P가 true를 돌려 시퀀스를 열면서도 down을 전달하므로 해당 hit에서 T도 등록된다. 보통 드래그 입력의 최종 상태 범주만 예측하고 두 처리기가 동시에 열린 경우의 좌표량은 로그로 확인한다. [지도 원전](evidence/map-sources.md) · [봉인 행렬](plan.json)

- 같은 CSS viewport 720×460, 지도 rect (24,20,640,400), DPR 1과 EPSG:3857, 해상도 2 투영 단위/CSS px, 회전 0 rad, view center (0,0)을 쓴다. 피처의 초기 지도 좌표는 (-128,80), 표시 반지름은 16 CSS px다. 중앙과 배경의 map pixel은 (256,160)과 (256,260)이다.
- 경계 대조의 map pixel (274,160)은 중심에서 18px 떨어진다. 0과 6 CSS px는 같은 좌표에서 비교한다. 드래그는 map pixel에서 (+36,+20)으로 끝난다. 1px 첫 이동 뒤 최대 축 차이가 3px를 넘어가는 (+4,+2)에서 첫 pointerdrag를 예상한다. 픽셀은 화면 오른쪽/아래가 양수, 투영 좌표는 동쪽/북쪽이 양수다. 좌표와 pixel의 비교 여유는 각각 1e-6, 해상도·회전 1e-9다.
- Select는 기본 singleClick, `style: null`이다. 컬렉션을 직접 seed한 사실을 실제 사용자 선택이나 필터 적용으로 세지 않는다. Translate와 DragPan은 동일한 주 버튼·modifier 조건을 쓴다. 기본 interaction과 kinetic을 넣지 않고 초기 애니메이션도 없다. View의 제약 정착 가능성을 실제 로그에서 확인한다. CSS 조작 후 브라우저 렌더 두 프레임을 기다린다. [fixture](fixture/map.js) · [재생](replay/drive.mjs)
- 우선 절의 기준은 A의 피처/탐색에 Translate/DragPan, B의 center 확정에 DragPan과 보존 조건, B 보류에 #9625와 수신자 확인이다. C와 후속 판독에서는 geometry만이면 Translate, center만이면 DragPan, 둘 다면 Map의 전달 절, 둘 다 유지면 이동 문턱·활성 조건을 먼저 돌려준다. 편집 의도인데 피처가 미적격이면 Select·Translate filter를 조합 후보로 붙인다. 선택/층/필터의 판이 갈리면 해당 버전의 옵션 절과 조건을 함께 반환한다.
