# 출력 관측과 목적·판 감도

## M03

R1과 R2에서 A의 colorbar 기준 anchor는 세 시점 모두 (.5,.5)였다. 캔버스의 물리 픽셀은 바뀌었다. .01의 A는 저장 뒤 (420.9653, 200.1111), .001의 A는 (416.5903, 200.1111)이다. 글자 RGB 차분을 왼쪽 아래 픽셀로 바꾼 중심은 각각 (420.5,199.5), (416.5,199.5)였다. 두 좌표계 의미를 구분할 수 있다. [R1 .01 A](runs/R1-M03-01-A/observations.json) · [R1 .001 A](runs/R1-M03-001-A/observations.json)

.01 B의 실제 x/y limits는 둘 다 [0,.99]다. 저장 뒤 (421.0468,201.7413)과 (.505051,.505051), 잉크 중심 (420.5,201.5)였다. A와 PNG의 라벨 영역 시작 행이 2px 다르며 두 그림에 글자가 보인다. .001 B의 실제 limits는 둘 다 [0,.099]다. 시작 표시 좌표 (2019.5707,1599.5556)에서 layout 시도 뒤 (495.7278,1599.5556)로 바뀌었지만 axes 비율은 (5.050505,5.050505)로 같았다. 시도 직후 y가 400px 높이를 벗어났다. 배치 경고와 TypeError 뒤 정상 저장을 시도하지 않아 실제 라벨 픽셀은 미확인이다. [R1 .01 B](runs/R1-M03-01-B/observations.json) · [R1 .001 B](runs/R1-M03-001-B/observations.json)

2.2.2에서는 x/y limits가 모두 [0,1]이고 두 조작의 (.5,.5)가 각각 같은 픽셀에 그려졌다. 같은 factor의 A/B PNG는 바이트 동일하다. 각 행의 DeprecationWarning은 NumPy 1.16의 `np.asscalar`이며 figure가 저장됐다. 3.0.2 B의 숫자 .5가 뜻하는 데이터값과 2.2.2 B의 정규화 좌표 .5는 해석이 다르다. [V1 정상 B](runs/V1-M03-01-B/observations.json) · [V1 경계 B](runs/V1-M03-001-B/observations.json)

3.0.2에서 설명 대신 실제 y=.5의 주석을 요구하면 .01 B의 y=.5가 맞고 .01 A의 y=.495가 목적을 놓친다. 혼합 변환 M의 x=.5 axes, y=.5 data도 저장됐다. 이 입력에선 B/M PNG 바이트가 같았다. .001 M은 x가 중앙이어도 y=5.050505 axes fraction으로 범위를 벗어나 같은 경고·예외를 냈다. xlim=[−1,3] 분리 시험에서는 B의 가로 비율 .375, M의 .5가 각각 PNG에서 확인됐다. xlim 개입은 색 띠를 축보다 좁게 만든다. 이 시험의 가운데는 축 프레임의 가운데다. [G1 정상 혼합](runs/G1-M03-01-M/observations.json) · [G1 경계 혼합](runs/G1-M03-001-M/observations.json) · [G1 xlim B](runs/G1-M03-x01-B/figure.png) · [G1 xlim 혼합](runs/G1-M03-x01-M/figure.png)

## M02

10개에서 A/B/C의 데이터 축 bbox는 동일하고 A/B는 a–j를 모두 읽을 수 있다. 30개 A는 경고를 내고 기본 축 크기에서 저장했다. 30개 C에 비해 좌우 폭이 각 47.713px 작고 높이는 9.778px 크다. A의 초기 배치가 줄어들었다고 해석할 수 있는 관측은 없었다. 하단은 X Axis 제목 일부도 잘렸다. B는 동수 C에 대해 좌우 x0/y0/폭/높이 차 모두 관측 0이다. [R1 10개](runs/R1-M02-10-A/observations.json) · [R1 30개 A](runs/R1-M02-30-A/observations.json) · [R1 30개 B](runs/R1-M02-30-B/observations.json) · [R1 30개 C](runs/R1-M02-30-C/observations.json)

30개 A의 19개(12-l부터), B의 18개(13-m부터)가 프레임을 넘었다. 라벨 RGB 차분과 PNG 판독에서 각각 그 목록의 글자 픽셀을 찾지 못했다. A의 12-l text bbox는 약 0.167px만 캔버스 안에 걸쳤고 잉크는 관측 0이었다. B의 마지막 12-l은 22 ink pixels 및 선 키가 보였다. 부분적으로 남은 범례 글자는 관측 0이다. 원본 15색이 30계열에서 두 번 순환하므로 읽힌 12개 이름을 고유하게 선에 연결할 수 있는지 별도 독자 검증이 필요하다. [PNG 판독 행](png-readback.csv) · [R1 30개 A 그림](runs/R1-M02-30-A/figure.png) · [R1 30개 B 그림](runs/R1-M02-30-B/figure.png)

## 반복과 결측

R1/R2의 성공 PNG 9쌍은 파일 바이트와 RGB가 같았다. 나머지 1쌍은 M03 B .001의 같은 경고/예외이고 PNG 비교는 해당 없음이다. 대응 geometry의 최대 차는 모든 쌍에서 0이었다. 두 소프트웨어 prefix와 Matplotlib 캐시는 별도로 만들었고 호스트와 판독자는 공유했다. 저장된 M03 13행의 텍스트 RGB 중심과 수치 anchor는 모두 4px 이내였다. 이는 색상이나 텍스트 대비에 대한 사람 시험이 아니다. [짝 비교](replay-pairs.json) · [환경](environment.json)
