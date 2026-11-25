# 저장 응답에서 재생하기

Git, tar, sha256sum, Python 3.12+가 있는 Linux에서 실행한다. PyPA `packaging` 26.3 wheel은 [도구 영수증](receipts/tools/)에 있다. PyPI 원 파일 SHA-256으로 먼저 검사하며 소스 `tags.py`와 `_manylinux.py`가 해당 wheel member와 같은 것도 [확인했다](receipts/tools/source-match.json). 인덱스·네트워크 패키지 설치·SciPy 설치를 호출하지 않는 재계산이다.

```bash
# GitHub에서 받은 agentflow-open 체크아웃 루트로 이동한다.
owned=docs/workstreams/research/AF-RES-266
result=HANDOFF에_기재한_고정_결과_SHA
bash "$owned/receipts/verify-replay.sh" "$PWD" "$result"
```

스크립트는 새 빈 임시 폴더에 해당 결과 트리만 `git archive`로 추출한다. 저장 입력 SHA-256을 확인하고 다른 빈 출력 폴더에 83행 파일 조인·9셀·릴리스 순서·인벤토리·두 파서 출력·반례 6개 파일을 다시 계산한다. 여섯 파일은 원 결과와 바이트 단위로 비교한다. 원응답과 본문 지문/헤더는 [index](receipts/index/)에서, 파일별 사전 원근거는 [248 원표 사본](receipts/af-res-248.matrix.csv)에서 가져온다. Simple 및 메타데이터 gzip은 해제 후 전송 본문과 비교한다. Github 시각 비교에는 [저장한 원필드 값](receipts/ci/public-github.json)을 사용한다. GitHub의 세션 헤더와 서명된 일회성 CDN 쿼리는 공개 영수증에서 가렸다. 원 헤더의 SHA-256과 공개본 SHA-256을 분리했다. PyPI 세 버전과 Simple의 저장 헤더는 원바이트다.

## 원파일 재검산

보존된 [files.csv](files.csv)의 `url`에서 정확한 파일명을 받아, `sha256` 및 `size_bytes`와 대조한다. 전체 SciPy 바이너리는 크기 때문에 Git에 복제하지 않았다. 온라인에서 내려받았을 때 [archive 검사](receipts/inspect_artifact.py)는 고정 영수증의 바이트 길이/해시 및 ZIP의 WHEEL, METADATA, RECORD를 재검산한다. 아래는 M9 하나를 검사하는 예다. 새로운 출력은 원 영수증 복사본에 쓴다.

```bash
owned=docs/workstreams/research/AF-RES-266
audit=$(mktemp -d)
cp "$owned"/receipts/artifacts/M9.* "$audit/"
file=scipy-1.14.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
url=https://files.pythonhosted.org/packages/56/46/2449e6e51e0d7c3575f289f6acb7f828938eaab8874dbccfeb0cd2b71a27/$file
curl --fail --location --proto '=https' "$url" --output "$audit/$file"
python "$owned/receipts/inspect_artifact.py" "$audit/$file" "$audit/M9"
```

저장 응답 전용 재생에서는 payload 다운로드 영수증과 ZIP 추출의 지문·필드가 연결되는지 확인한다. 전체 payload를 다시 해시하려면 위처럼 원바이트가 필요하다. [최초 추출·HTTP 지문](receipts/artifacts/).

## M9 실행 다시 하기

[잠금파일](receipts/local/requirements.txt)의 두 파일을 빈 `wheel_folder`에 다운로드한다. SciPy는 위 URL, NumPy는 [고정 원 URL과 지문](receipts/local/numpy-wheel.transport.json)을 사용한다. Python은 일반 GIL CPython 3.13, x86_64 Linux glibc 2.17+ 기준이며 본 관측 환경은 3.13.5와 2.41이다. 시험은 설치 import와 BLAS 선형 풀이 한 건이다.

```bash
receipts="$PWD/docs/workstreams/research/AF-RES-266/receipts"
env_dir=$(mktemp -d)
uv --no-config --no-cache venv --offline --python /usr/bin/python3.13 "$env_dir"
cd "$wheel_folder"
cp "$receipts/local/requirements.txt" .
uv --no-config --no-cache pip install --offline --no-index --no-deps \
  --require-hashes --python "$env_dir/bin/python" -r requirements.txt
"$env_dir/bin/python" -I "$receipts/local/smoke.py" \
  ./scipy-1.14.1-cp313-cp313-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

기대값은 `[2.0, 3.0]`, 오차 ≤ 1e-12 및 로드한 네이티브 member의 원 archive SHA-256 일치다. `*.run.json`의 명령·입력 지문·stdout/stderr 지문·종료 코드가 설치와 실행을 고정한다. [실행 영수증](receipts/local/).
