# AF-RES-045 Matplotlib 재현 절차

## 상태와 범위

**이 스크립트와 환경 명세는 실행하지 않았다.** 작성 시점은 2026-11-22이며, 예측 봉인 커밋 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1` 뒤에 작성한 후속 검사 도구다. 예측·요구 원장을 수정하지 않았다. 작성 중 실시하는 검사는 Python 문법의 정적 분석이며 Matplotlib/Cartopy import, 그림 생성, 시험 통과를 뜻하지 않는다.

입력은 [M01 #13430](https://github.com/matplotlib/matplotlib/issues/13430), [M02 #13522](https://github.com/matplotlib/matplotlib/issues/13522), [M03 #13600](https://github.com/matplotlib/matplotlib/issues/13600)과 봉인한 `requests.csv`·`predictions.csv`다. 독립적으로 구현한 계측 코드이며 원래 이슈 본문이나 원래 프로그램 전문을 재배포하지 않는다.

출력은 실행자가 지정한 **AF-RES-045 소유 경로 안의 새로운 디렉터리**에만 쓴다. 이미 존재하는 실행 디렉터리에는 덮어쓰지 않고 종료한다. Matplotlib 설정·글꼴 캐시도 해당 실행 디렉터리의 `_mplconfig`에 둔다. `python -B`로 bytecode 생성을 막는다.

## 역사적 환경

| 환경 | 고정 핵심 판 | 용도 |
| --- | --- | --- |
| `af-res045-mpl302` | Matplotlib3.0.2, Cartopy0.17.0, Python3.6.8, NumPy1.16.6, Pillow6.2.2 | M01·M02·M03 기본 조사 |
| `af-res045-mpl222` | Matplotlib2.2.2, Python3.6.8, NumPy1.16.6, Pillow6.2.2 | M03 판 민감도 |

환경 파일은 **해결·설치·검증한 lockfile이 아니다**. 오래된 빌드와 전이 의존성을 현재 저장소에서 해결할 수 있는지 확인하지 않았다. Cartopy의 GEOS/PROJ 및 글꼴·FreeType 판은 결과에 영향을 줄 수 있다. 설치 성공 뒤 반드시 실제 의존성 목록을 내보내고, 스크립트의 `environment.json`과 함께 보존한다. 주요 판이 다르면 스크립트는 거절한다. 의존성 해결 실패를 피하려고 Matplotlib나 Cartopy를 최신판으로 대체하지 않는다.

이 환경은 원작성자의 기계 복제가 아니다. M01은 원래 Ubuntu16.04/Python3.6/Qt, M02·M03은 Windows10/Python3.7/TkAgg였다. 여기서는 비대화형 **Agg**를 명시한다. 이 변경 때문에 성공/실패가 원래 플랫폼의 재시험과 같다고 보장할 수 없다. Agg는 후속 수신 실행을 분리해 검사하는 선택이며 역사적 관측을 대체하지 않는다.

다음은 필요할 때 실행할 환경 준비 명령이다. **본 작업에서 실행하지 않았다.** 환경 생성은 운영자가 마련한 Conda 실행기에서 수행한다. 저장소 소유 경로 밖의 환경/패키지 설치는 이 연구 산출물 편집과 별개의 실행 환경 준비 작업이다.

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
conda env create --file "$AF_RES045_OWNED/evidence/reproduction/environment-mpl302.yml"
conda env create --file "$AF_RES045_OWNED/evidence/reproduction/environment-mpl222.yml"
```

위 명령은 **저장소 루트**에서 시작한다. Conda가 없거나 solver가 실패하면 첫 행동은 해당 실행기와 실패 로그·해결 불가 패키지를 기록하는 것이다. 환경이 준비되기 전에는 관측 없음 상태를 유지한다. `environment-*.yml`은 설치가 될 것이라는 주장이 아니다.

## 정확한 실행 명령

아래 명령은 모두 **아직 실행하지 않았다**. 각 명령은 독립적이며 앞 명령이 실패했다고 그 실패를 무시한 실행으로 간주하지 않는다. 다시 실행할 때는 마지막 디렉터리 이름을 새 이름으로 바꿔 이전 결과를 보존한다.

### M01 — 원래 두 저장, A pre-draw, B 외부 raster 축소

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
conda run --no-capture-output -n af-res045-mpl302 python -B "$AF_RES045_OWNED/evidence/reproduction/m01_first_save.py" --scale 0.90 --out "$AF_RES045_OWNED/evidence/reproduction/runs/m01-mpl302-scale090"
```

일반 Cartesian 정상 입력과 PlateCarree 경계 입력에 각각 다음 세 조작을 적용한다. 각 조작마다 새 figure를 만든다.

- `reference`: 명시적 pre-draw 없이 최초·둘째 `savefig`를 기록한다.
- `A`: `canvas.draw()`를 한 번 명시적으로 수행하고 최초·둘째 저장을 기록한다. pre-draw가 예외를 내면 성공한 A로 취급하지 않고 export를 중지한다.
- `B`: pre-draw 없이 최초 PNG를 저장한 뒤 **Pillow로 전체 raster를 실제로 비례 축소**하고, 같은 크기의 흰 캔버스 중앙에 놓는다. 그 뒤 같은 figure의 둘째 저장도 보존한다. B는 아무것도 하지 않는 대조로 바뀌지 않는다.

`--scale 0.90`과 중앙 배치는 봉인 때 정해지지 않았던 **사후 계측 매개변수**다. 결과에 맞춰 고른 최적 축척이 아니다. 스크립트는 0보다 크고1보다 작은 명시적 축척을 요구한다. 기본 PNG는 이미 캔버스 크기이므로 “canvas fit”만으로 유일한 비항등 축척이 결정되지 않는다는 약점도 남는다. 다른 축척을 검사할 때도 새 실행 경로에 기록한다.

`B-first-scaled.png`는 실제 변환 산출물이다. `axis_bbox_after_raster_transform_MODEL_pixels`는 저장 직후 얻은 bbox에 동일 affine 변환을 적용한 **기하 모형값**이며 PNG에서 독립적으로 검출한 bbox가 아니다. 축소는 내부 상대 geometry를 다시 layout하지 않는다. 캔버스상 bbox가 우연히 가까워졌다고 내부 배치 문제를 해결했다고 판정하지 않는다.

계측 중 `Axes.get_position()`을 호출하지 않는다. [Matplotlib3.0.2 소스 L827–849](https://github.com/matplotlib/matplotlib/blob/v3.0.2/lib/matplotlib/axes/_base.py#L827-L849)에서 이 함수는 `apply_aspect()`를 호출하기 때문이다. 최초 저장 전에 계측용 `draw`, `get_tightbbox`, `get_position`을 호출하면 검사 대상 상태를 바꿀 수 있다. 스크립트는 수동 bbox 필드를 읽고 저장·draw event 뒤의 상태를 기록한다. private 필드를 읽기만 하며 수정하지 않는다. 내부 draw event 수는 실제 기록값이고, 명시적 pre-draw 횟수와 혼동하지 않는다.

### M02 — 범례10·20·30개와 범례 없는 대조

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
conda run --no-capture-output -n af-res045-mpl302 python -B "$AF_RES045_OWNED/evidence/reproduction/m02_legend.py" --seed 45045 --counts 10 20 30 --out "$AF_RES045_OWNED/evidence/reproduction/runs/m02-mpl302-seed45045"
```

10개와30개는 봉인한 정상·경계 입력이고20개는 원문에 포함된 추가 민감도다. figure10×3inch, subplot 폭 비5:1:5, 동일 글꼴과10point 크기를 고정한다. 원문은 난수 seed를 고정하지 않았으므로 **seed45045는 재현성을 위한 사후 조작**이다. 실행 JSON에 실제 생성된 좌표와 series 데이터를 남긴다. 각 항목 수에서 A/B/대조는 동일 데이터를 쓴다.

A는 범례를 layout에 포함하는 기본값을 유지한다. **B에서만** `legend.set_in_layout(False)`를 호출한다. 대조는 같은 데이터와 중앙 axes를 두고 **범례 artist만 추가하지 않는다**. 대조는 B가 아니며 series를 줄이지 않는다. 모든 경우에 `tight_layout`을 호출하고 `bbox_inches='tight'`를 사용하지 않아 캔버스를 확대하지 않는다. layout 예외가 나면 export를 하지 않고 예외·경고를 남긴다.

`data_axes_bbox_minus_no_artist_pixels`가 좌우 axes와 범례 없는 대조의 차이를 제공한다. `bbox_outside_canvas`는 legend bbox와 캔버스의 경계 계산이며, 실제 어느 문자열이 보이는지는 PNG와 함께 검토한다. bbox 초과만으로 series key의 의미 손실을 측정했다고 주장하지 않는다. 두 후보의 추천이 같았다는 봉인 사실은 실행 결과와 관계없이 유지한다.

### M03 — 실제 colorbar 범위·anchor와 판 민감도

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
conda run --no-capture-output -n af-res045-mpl302 python -B "$AF_RES045_OWNED/evidence/reproduction/m03_colorbar.py" --expected-mpl 3.0.2 --out "$AF_RES045_OWNED/evidence/reproduction/runs/m03-mpl302"
conda run --no-capture-output -n af-res045-mpl222 python -B "$AF_RES045_OWNED/evidence/reproduction/m03_colorbar.py" --expected-mpl 2.2.2 --out "$AF_RES045_OWNED/evidence/reproduction/runs/m03-mpl222"
```

각 판에서 factor0.01,0.001,0.1과 A/B를 별도 figure로 실행한다. 0.01은 정상,0.001은 경계,0.1은 봉인한 부가 민감도다. 모두 `factor * arange(100).reshape((10,10))`,5×4inch,100dpi,우측5% colorbar,10% pad,수직 중앙 text,rect[0,0,1,0.95]를 유지한다.

A만 `transform=cb.ax.transAxes`를 지정하고, B는 원문의 기본 data transform을 유지한다. label 위치를 자동으로 고치거나 crash guard를 패치하지 않는다. 다음을 별도 시점으로 기록한다.

- `before_layout`
- `after_layout_attempt`
- 성공했을 때만 `after_save`

각 시점에 실제 colorbar x/y limits, scale, text anchor의 display 좌표와 colorbar axes 비율 좌표를 저장한다. `data_value_point5_fraction_from_ACTUAL_ylim`은 실행에서 읽은 실제 y limits에 근거한 계산이다. 데이터 배열의 min/max를 실제 colorbar limits로 대체하지 않는다. layout에서 예외가 나면 이후 저장을 중지하며, 저장 성공과 text 중심 성공을 다른 관측으로 유지한다.

### 현재 Python의 순수 산술 — 수신 소프트웨어 실행과 분리

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
python -B "$AF_RES045_OWNED/evidence/reproduction/model_arithmetic.py" --out "$AF_RES045_OWNED/evidence/reproduction/runs/conditional-arithmetic"
```

이 명령도 아직 실행하지 않았다. 표준 라이브러리만 사용하며 Matplotlib/Cartopy를 import하지 않는다. “linear·noninverted이며 실제 축 범위가 정확히[0,99×factor]”라는 가정 아래의 분수 계산만 남긴다. 생성 파일은 `conditional-model-only.json`이며 `software_execution_evidence:false`로 표시한다. 이 수치를 소프트웨어 시험 통과나 과거 기대 출력으로 전환하지 않는다.

## 실행 뒤 보존할 환경과 판정

환경이 실제로 준비된 다음, 다음 명령으로 환경 명세를 파일에 남긴다. 이 명령 역시 아직 실행하지 않았다.

```bash
AF_RES045_OWNED="$PWD/docs/workstreams/research/AF-RES-045"
conda list -n af-res045-mpl302 --explicit > "$AF_RES045_OWNED/evidence/reproduction/mpl302-resolved-explicit.txt"
conda list -n af-res045-mpl222 --explicit > "$AF_RES045_OWNED/evidence/reproduction/mpl222-resolved-explicit.txt"
```

스크립트 실행이 끝나면 `environment.json`, `observations.json`, PNG와 실제 실행 로그를 함께 검토한다. JSON의 예외·경고, font/FreeType·Cartopy·PROJ 판, seed와 B 축척, 원래 조건과 다른 backend를 먼저 확인한다. 아직 없던 값을 예상 수치로 채우지 않는다. 수용 판단을 자동으로 출력하는 코드는 넣지 않았다.

실행 후 결과를 연구 원장에 추가할 때는 **봉인 뒤 수행한 새로운 연구자 실행**으로 표시한다. 원래 유지보수자의 시험이나 원작성자 재시험으로 소급해서 부르지 않는다. 봉인된 CSV를 수정하는 대신 새로운 관측 파일과 판정 변경 이유·영향받은 행을 별도로 남긴다.

