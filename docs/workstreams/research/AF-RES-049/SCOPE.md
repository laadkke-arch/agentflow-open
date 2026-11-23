# AF-RES-049 표본과 사전 판정

Matrix 값이 달라져도 색 막대 중앙에 글자를 두려는 M03과, 범례가 커져도 두 데이터 축을 유지하려는 M02를 재생한다. 각 요구의 입력·판·목적을 고정해 원리에서 옮긴 조작이 실제로 만드는 차이를 확인한다.

## 시작판과 사전 노출

계획 통합판은 `d8c8d029bfb6107520ae74d2a172b2b18840e764`이며 실제 시작판은 `522ea9092d4d56ef6db0bd4f707bfc90032e179e`다. 시작 검사와 의존판은 [manifest.json](manifest.json)과 [시작 영수증](evidence/session-start.json)에 있다. AF-RES-045 인계 `7649739855299e7c054286d5d5126a76c701fd01`와 결과·계측 코드 `29c5da579b7a29118f31541092e6a51f3d77219d`를 고정했다.

봉인 시점에 이미 045의 예측과 부분 인계, 두 이슈의 공개 본문·수락 댓글, #13603·#18100의 패치가 알려졌다. #13600에서 작성자는 factor .01과 .1의 그림, .001의 경고와 None 예외를 보고했다. #13522에서 작성자는 10개 정상, 20개 축 축소, 30개 배치 실패를 보고했다. 이번에 생성할 Agg 그림과 영수증은 열람 전이다. 범위에서 제외한 것은 다른 네 요구, pdfTeX·악보 역사, 새 유사 제품 목록 및 채택 인과·노동시간 추정이다. [045 결과 L9–12](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/RESULT.md#L9) · [#13600](https://github.com/matplotlib/matplotlib/issues/13600) · [#13522](https://github.com/matplotlib/matplotlib/issues/13522)

## 고정 조건

- 주패널은 Linux x86_64의 Matplotlib 3.0.2/Agg에서 10조건씩 두 번이다. 045의 목표와 맞춰 Python 3.6.8, NumPy 1.16.6, Pillow 6.2.2, 100 DPI, DejaVu Sans 10pt 및 rcdefaults를 쓴다. 휠에 실린 FreeType과 실제 폰트 파일은 판별 입력으로 기록한다. 원 작성자는 Windows/TkAgg, M03 Python 3.7.2와 M02 32비트 Python 3.7이었다.
- R1과 R2는 별도 설치 경로와 새 프로세스, 빈 Matplotlib 설정/폰트 캐시로 시작한다. 같은 배포본 해시를 허용하며 두 번째 실행은 첫 출력에 접근하지 않는다. 이후 읽기 전용 비교를 수행한다. 같은 실행자·호스트라는 범위도 기록한다.
- M03은 5×4인치 figure, 10×10 배열 `factor * arange(100).reshape(10, 10)`, 우측 폭 5%·간격 10% colorbar, 수직 가운데 정렬 텍스트 `(0.5, 0.5)`, `tight_layout(rect=[0,0,1,.95])`를 유지한다. A만 `cb.ax.transAxes`를 지정한다. 별도 crash guard나 자동 클리핑을 덧붙이지 않는다.
- M02는 10×3인치 figure, 세 subplot의 폭 비 5:1:5, 계열 10/30개, 난수 seed 45045, 원 palette·caption 순서를 쓴다. 같은 항목 수의 A/B/C 데이터와 텍스트를 맞춘다. A는 범례를 layout에 포함한다. B는 `legend.set_in_layout(False)`를 쓰고 그린다. C는 중앙 축과 모든 데이터를 유지하고 범례 artist만 생략한다. 모든 figure에 `tight_layout()`을 적용하며 원래 캔버스 크기로 PNG를 저장한다.
- 판 감도 V1은 Matplotlib 2.2.2에서 M03 A/B와 두 factor 네 자리다. 별도 목적 감도 G1은 3.0.2에서 x축 비율 .5와 y데이터값 .5를 섞은 두 factor, 그리고 factor .01에서 xlim을 `[-1,3]`으로 바꾼 B와 혼합 좌표 두 자리다. 마지막 둘은 색 띠 자체가 아니라 축 프레임의 가로 중앙을 시험한다. 주표본 밖의 4자리는 [expected.csv](expected.csv)에 별도 기록한다.

## 관측 순서와 허용오차

| 관측 | 측정과 판정 |
| --- | --- |
| M03 위치 | layout 직전, layout 시도 직후, 저장 성공 직후에 실제 x/y limits·scale, figure/axes bbox, 텍스트 anchor의 표시 픽셀과 axes fraction을 얻는다. A의 (.5,.5)는 좌표마다 절대차 ≤1e-6을 일치로 본다. 실제 y축이 정방향·선형이고 limits가 [0,99×factor]에 절대차 ≤1e-12로 맞는 경우만 B에 조건부 산술 50/99 또는 500/99를 적용한다. 예측 구간과 실제 limits가 다른 사례는 전제 불성립으로 적는다. |
| M03 독립 PNG | 원 PNG와, 성공 직후 동일 figure에서 텍스트 alpha만 0으로 바꾼 PNG를 디코딩해 달라진 RGB 픽셀의 bbox를 얻는다. 축 geometry 유지 여부를 함께 검사한다. PNG 원점은 왼쪽 위로, 화면 픽셀 원점은 왼쪽 아래로 기록한다. anchor와 살아 있는 글자 영역 중심의 차이는 축별 ≤4 px를 일치로 본다. 글자가 모두 밖이어서 픽셀 관측 0인 경우에는 canvas 밖 여부를 대조한다. 저장 실패는 PNG 위치 미확인이다. |
| M02 geometry | 저장 뒤 좌우 데이터 axes의 x0/y0/폭/높이를 픽셀과 figure fraction으로 적고 동수 C와 비교한다. 좌표별 차이가 ≤0.25 px면 보존이다. A30은 C와의 bbox 변화가 0.25 px를 넘거나 배치 거부 경고·예외를 내야 부담 예측과 일치한다. 반환·경고·예외를 구별한다. |
| M02 판독 | 범례 전체·개별 라벨 text bbox가 캔버스 경계를 0.25 px 넘는 항목 수와 ID를 센다. RGB 차분으로 라벨별 잉크를 찾아 원본 PNG를 눈으로 재판독한다. ID는 위에서부터 1기반 순서와 caption을 결합한다. 읽힘, 일부 잘림, 전부 밖, 불명확을 구분하며 같은 글자의 중복 ID를 병합하지 않는다. C의 범례 없음은 의도된 기준이다. 서체나 색의 중복으로 계열 대응 정보를 잃는 문제는 별도로 기록한다. |
| 반복 일치 | 입력 배열·조건·판·DPI·픽셀 크기·상태·경고/예외 종류 및 메시지·라벨 손실 분류가 같아야 한다. 대응 geometry는 좌표별 ≤0.25 px, axes 비율과 limits는 ≤1e-6을 사용한다. 성공 PNG는 바이트 SHA, 디코딩 RGB SHA, 달라진 픽셀 수를 각각 비교한다. 수치가 같아도 RGB가 다르면 래스터 차이로 따로 기록한다. 양쪽 저장 실패는 실패 재현으로 분류한다. 미실행은 짝 일치로 세지 않는다. |

예외가 나면 해당 시점 상태와 추적을 저장하고 다음 조건의 새 figure로 진행한다. 실패한 레이아웃에서 강제로 저장하지 않는다. 정상·경계는 입력의 이름이다. 두 목적을 비교할 때 먼저 사용자 목표를 고정한다. 같은 입력·목적에 관측 가능한 경쟁 예측이 갈라지는 경우에만 조작 판별을 검토한다. M02는 양쪽 도너가 조건부 B를 내므로 동률 대조다. 도너의 독점적인 설명 효과에는 별도 비교군이 필요하다. API 문서만 따라가도 같은 조작을 얻을 가능성을 Q7의 반례로 다룬다. [045 봉인 예측 L4–7](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/predictions.csv#L4)
