# 고정판 재생

AF-RES-045의 [재현 설명](https://github.com/laadkke-arch/agentflow-open/blob/29c5da579b7a29118f31541092e6a51f3d77219d/docs/workstreams/research/AF-RES-045/evidence/reproduction/REPRODUCE.md)과 코드의 검토 사본은 [upstream-045/](upstream-045/)에 있다. `probe_common.py`의 출력 루트만 [diff](045-output-path.diff)대로 이 작업 경로에 대응한다. 새 runner는 M02의 `build`와 M03의 `snapshot`을 사용한다. M03의 fixture는 이전 `main`의 재료와 같은 순서이며, 지정된 G1에서만 혼합 transform 및 xlim 개입을 사용한다. 원본의 일괄 코드에는 부가 입력 M02 20개와 M03 factor .1이 있다. 이 작업은 봉인된 예정 행을 CSV에서 읽는다.

Linux x86_64/glibc, Python 3.12 이상인 호스트에서 저장소 루트로 시작한다. [distributions.json](distributions.json)의 URL과 SHA256을 사용해 각 prefix를 새로 구성한다. 부트스트랩은 프로젝트 의존판 설치에 필요한 Conda 배포의 Python/runtime과 PyPI 휠만 내려받는다. Matplotlib의 wheel metadata와 fixture의 imports에서 Cartopy 요구가 없으며, 045 환경의 Cartopy는 M01에만 필요했다. Matplotlib는 자체 Agg 및 wheel의 DejaVu Sans를 사용한다. 호스트 OS와 시스템 공유 라이브러리 차이는 실제 환경 영수증으로 확인한다.

```sh
AF049_OWNED="$PWD/docs/workstreams/research/AF-RES-049"
AF049_SOFTWARE="$(mktemp -d /tmp/af049-software-XXXXXX)"
python -B "$AF049_OWNED/reproduce/bootstrap.py" --version 3.0.2 --prefix "$AF049_SOFTWARE/R1"
python -B "$AF049_OWNED/reproduce/bootstrap.py" --version 3.0.2 --prefix "$AF049_SOFTWARE/R2"
python -B "$AF049_OWNED/reproduce/bootstrap.py" --version 2.2.2 --prefix "$AF049_SOFTWARE/V1"
AF049_OUTPUT="$(mktemp -d "$AF049_OWNED/evidence/replay-XXXXXX")"
"$AF049_SOFTWARE/R1/bin/python3.6" -B -s "$AF049_OWNED/reproduce/replay.py" --repeat R1 --out "$AF049_OUTPUT"
"$AF049_SOFTWARE/R2/bin/python3.6" -B -s "$AF049_OWNED/reproduce/replay.py" --repeat R2 --out "$AF049_OUTPUT"
"$AF049_SOFTWARE/V1/bin/python3.6" -B -s "$AF049_OWNED/reproduce/replay.py" --repeat V1 --out "$AF049_OUTPUT"
"$AF049_SOFTWARE/R1/bin/python3.6" -B -s "$AF049_OWNED/reproduce/replay.py" --repeat G1 --out "$AF049_OUTPUT"
```

정상 그림은 각 실행 ID의 `figure.png`다. `ink-mask.png`는 그 저장 뒤 같은 figure에서 라벨 alpha만 0으로 바꿔 얻은 RGB 차분이며, 관측 JSON에 원본·비교 RGB 해시와 축 동일성 검사가 있다. 구성·계측 문제는 프로세스 비정상종료나 `instrumentation_error`로, 각 layout/save의 측정된 예외는 그림별 단계와 종료 분류로 남는다. 두 반복은 별도 설치와 빈 MPLCONFIGDIR이다. R2의 runner는 예정 행을 읽고 자기 ID로만 저장한다. R1/R2를 비교하는 단계는 이후에 수행한다.
