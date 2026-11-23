# 선택적 보조 재생 — 결과 열람 전 고정

이 재생은 공개 후속 기록을 대신하지 않는다. 원 작성자의 실제 patch가 미확인이므로 역사적 같은 판 분모에 합치지 않는다. N/I/D의 원문 창에 renderer 출력이나 재생 코드를 넣지 않는다. 실행은 단계 ② 원격 커밋을 확인한 뒤에만 시작한다.

## 입력·조작

- V02 경계: #7422 최초 가용 본문의 JSON fenced block 그대로. penguin 3행, repeat 4×4, schema 원문 그대로. A는 `fieldTitle`만 공급하고 accessor를 그대로 둔다. callback은 operation-refinements.json의 문자열에서 정한 escape 제거 함수다. B는 repeat.row/repeat.column 및 color.field의 access escape만 제거하며 formatter는 쓰지 않는다. 다른 data/scale/width/height/mark는 바꾸지 않는다.
- V02 정상 보조 입력: 경계와 같은 세 record를 사용하되 literal key의 점·대괄호를 없애고 참조도 그 일반 이름으로 바꾼 복사본. 이는 변수 하나를 보는 연구자 입력이며 원 저자의 외부 정상 예제 재현이 아니다. 정상 A/B가 같고 경계에서 달라지는지 보조적으로만 확인한다.
- V03: #7507 최초 가용 본문의 10행 inline spec. A는 axis labelColor.condition.test를 `datum.value === '4. Hygiene & Cleaning'`으로 바꾸고, B는 `datum.resilience === 0` 그대로. 9개 비zero/1개 numeric zero는 한 출력의 두 부분집합이다. 다른 zero-category를 만들거나 threshold를 바꾸지 않는다.
- 기준 compiler는 Vega-Lite 5.1.0. Vega runtime과 다른 renderer 의존성은 해당 release의 공개 package/lock 요구를 먼저 확인해 한 판으로 고정하고 실제 import 판·패키지 무결성·명령을 기록한다. 임의 최신 compiler로 대체하지 않는다. 의존성 확보 실패면 실패 로그와 정확 재개 명령을 남긴다.

## 출력 전 예상과 측정

- V02 정상: A/B 모두 동일한 일반 이름의 값 접근과 title을 유지한다는 범주 예측. 경계 A: 특수 이름의 값 접근 유지와 표시 title의 access escape 제거를 동시에 예측한다. 경계 B: 특수 이름의 값 접근 손실을 예측한다. 표시되는 각 title은 대응 field와 함께 확인한다. 고정 title 하나의 반복 복사는 성공이 아니다. 정확 point/axis label 수는 사전 문서 근거가 부족하므로 숫자 정답을 만들지 않는다.
- V03 A: 정확한 원문 표에서 red axis label 1개, black axis label 9개. B: red 0개, black 10개. CSS 색 표기는 대소문자·hex/RGB 동치만 정규화한다. label identity도 확인하며 legend text를 axis label 수에 합치지 않는다.
- compile 출력, 실제 SVG, stdout/stderr/exit와 입력 hash를 별도로 보존한다. 가능하면 SVG의 axis label text/fill과 scenegraph의 datum을 서로 대조한다. raster pixel·독자 가독성·원 작성자 수락은 이 재생의 측정이 아니다.
- 실패·경고·schema/runtime 불일치와 정상/경계 입력의 연구자 구성 부분을 숨기지 않는다. 출력 뒤 옵션·예측을 바꾸면 별도 감도로 기록하고 원 봉인을 덮어쓰지 않는다.
