# 외부 반례의 실행 범위와 남은 입력

## 실행한 것

```sh
python -B docs/workstreams/research/AF-RES-113/evidence/verification/external/counterexample_arithmetic.py
```

입력은 코드와 transfer-tests.json에 고정되어 있다. 마지막 실행은 arithmetic-checks.json의 UTC에 기록했다. 일곱 산술 assertion이 통과했다. 파이썬 표준 라이브러리로 배열 접힘·삼각함수·좌표·시간 간격만 계산했다. 이 명령을 다시 실행하면 산술 결과와 새 확인 시각으로 같은 파일을 갱신한다. 깨끗한 결과 SHA를 검사할 때는 먼저 별도 checkout에서 실행하거나 저장 결과와 시각 필드를 제외하고 대조한다.

## 실행하지 않은 것

원 논문의 음향 장비 실험, librosa/skimage의 공개 API, GDAL의 파일 해석은 이 묶음에서 실행하지 않았다. 그림의 모양과 논문에 보고된 수치는 원전 관측이며 재측정치가 아니다.

EXT-T4를 실제 파일로 검사하려면 의도한 첫 표본의 물리적 위치와 생산기 버전을 아는 `legacy-point.tif`가 필요하다. 모의 태그만 만든 새 파일로 과거 사용자의 의도를 증명할 수 없다. GDAL이 있는 환경에서 다음과 같이 버전과 양쪽 결과를 기록한다.

```sh
gdalinfo --version
gdalinfo --config GTIFF_POINT_GEO_IGNORE TRUE legacy-point.tif
gdalinfo --config GTIFF_POINT_GEO_IGNORE FALSE legacy-point.tif
```

필수 입력: 파일의 byte SHA256, RasterType=PixelIsPoint, 실제 tiepoint와 spacing, 생산기·버전, 알려진 첫 표본 좌표. 구성 예의 tiepoint=(100,200), spacing=(10,-10)에서는 두 해석의 corner 예상이(100,200)/(95,205)다. 이 값은 원본 파일의 실제 결과가 아니다.

Farina2007의 §3.4를 재현하려면 저자가 기록한 재생 sweep·녹음 응답·원 역필터 또는 동일한 clock-rate 차이를 가진 측정 입력이 필요하다. 첫 행동은 저자 원 PDF의 §3.4 그림32–34와 원시 신호 제공 경로를 확인하는 것이다. 원시 입력 없이 약8.5ms나12.45dB를 재현했다고 주장하지 않는다. EXT-T2의 비균일 시간축 시험은 알려진 timestamp를 가진 세 점 구성 입력으로 이미 산술만 확인했으며, 물리적 장비 측정의 대체가 아니다.
