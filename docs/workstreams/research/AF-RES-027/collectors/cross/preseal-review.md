# A 봉인 전 conda 참조 적격성 판독

- 판독자: `/root/cross_domain`, 같은 표시 모델의 별도 내부 판독. 외부 독립 검토·맹검·사용자 실험이 아니다.
- 입력: `SCOPE.md`, `collectors/conda/historical.json` 및 그 원장에 있는 **정확한 과거 커밋**의 원문만. 미래 소비자 이력·상류 변경 원문은 열지 않았다.
- 직접 재열람: 2026-11-22 05:01–05:04 UTC. 여섯 행의 역사 파일과 같은 판의 목적/호출 파일 총 19 URL을 raw.githubusercontent.com에서 읽었다. 수집자가 이미 센 원문을 재열람한 것이므로 고유 최소수에 추가하지 않는다.
- 판독 범위: 입력 파일 연결과 선언된 당시 목적의 적격성. 실제 설치·테스트 실행·패키지 해석 결과·배포판을 검증한 것은 아니다.

## 여섯 행 판독

| 참조 | 같은 고정판에서 재확인한 연결 | 판독과 한계 |
| --- | --- | --- |
| A-C01 · Dask · Python | 환경 파일:2–7의 conda-forge 첫 채널과 python=3.6.*; appveyor.yml:13–16의 Python 3.6/환경 경로; setup_conda_environment.cmd:16의 `-f %ENV_FILE%`; run_tests.cmd:5–8의 pytest 호출 | CI 목적·명시 판 제약·환경 입력 연결 충족. 실행 성공 및 실제 선택 채널은 미확인. |
| A-C02 · JupyterLab · Sphinx | docs/environment.yml:2–6의 채널/버전; readthedocs.yml:1–2의 해당 환경 파일; docs/Makefile:6,20의 Sphinx 문서 빌드 | 문서 빌드 도구 목적 충족. Read the Docs의 실제 실행·게시판은 미확인. |
| A-C03 · napari · setuptools | .cirrus.yml:51,68,116의 `-c conda-forge setuptools`; :76,124의 개발 설치; setup.py:40,78의 setuptools 호출 | 빌드 도구/라이브러리 목적 충족. CI 내 다른 설치가 최종 산출물을 바꿀 수 있으므로 설치 명령만으로 최종 선택 바이너리를 확정하지 않는다. |
| A-C04 · pandas · NumPy | environment.yml:2–6의 채널/NumPy; contributing.rst:203–232의 해당 파일에서 환경 생성과 소스 빌드; __init__.py:5–17의 필수 의존성 검사 | 개발·실행 라이브러리 목적은 명확. 독립 CLI 도구라는 판정은 하지 않는다. |
| A-C05 · scikit-image · SciPy | requirements/default.txt:4; INSTALL.rst:263–291의 conda 개발 절, 특히 :278의 정확한 `--file` 입력; filters.py:10,82,139–141의 SciPy Gaussian filter 호출 | requirements 파일을 pip 설치용이라고만 보고 배제할 수 없다. 이 판은 같은 파일을 conda-forge 명시 명령에 직접 넣는다. 수치 라이브러리 목적 충족; solver 성공·배포는 미확인. |
| A-C06 · Spyder · applaunchservices | requirements/conda.txt:5; CONTRIBUTING.md:58–66의 conda-forge 설치와 :79–86의 clone 실행; dependencies.py:94–98의 macOS 기능 설명 | 파일/채널/선언 목적 연결 충족. 기능 설명은 실제 런타임 호출이나 성공한 macOS 실행의 증명이 아니다. Binder 사본은 같은 소비자 계보이며 두 번째 독립 참조로 세지 않는다. |

## A-C05·A-C06 직접 확인 위치

1. A-C05 고정판 `0e35d8040d0b0bb409de41f3c0f024f941e09d8a`:
   - [INSTALL.rst](https://github.com/scikit-image/scikit-image/blob/0e35d8040d0b0bb409de41f3c0f024f941e09d8a/INSTALL.rst#L263-L291): conda 개발 환경을 만든 뒤 `conda install -c conda-forge --file requirements/default.txt`를 실행하라는 지시와 소스 빌드/시험 명령이 이어진다.
   - [requirements/default.txt](https://github.com/scikit-image/scikit-image/blob/0e35d8040d0b0bb409de41f3c0f024f941e09d8a/requirements/default.txt#L1-L10): NumPy 다음에 scipy>=1.8. 파일 생성원은 pyproject.toml이라고 쓰여 있으나 여기서 실제 입력 파일과 명령 연결을 직접 확인했다.
   - [filters.py](https://github.com/scikit-image/scikit-image/blob/0e35d8040d0b0bb409de41f3c0f024f941e09d8a/skimage/_shared/filters.py#L129-L141): ndimage.gaussian_filter를 반환하는 실제 호출. INSTALL의 최신 의존성 권고는 **이 판 당시의 문맥**이며 영구적인 최신판 의도로 확장하지 않는다.
2. A-C06 고정판 `569b4cf8d93969163412cfc2b3f36b02bfaff0d5`:
   - [CONTRIBUTING.md](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/CONTRIBUTING.md#L58-L86): `conda install -c conda-forge --file requirements/conda.txt` 뒤 개발 clone 실행법. macOS에서 추가로 요구하는 python.app는 이 행의 참조 대상과 다르다.
   - [requirements/conda.txt](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/requirements/conda.txt#L1-L6): 첫 패키지는 applaunchservices >=0.1.7.
   - [dependencies.py](https://github.com/spyder-ide/spyder/blob/569b4cf8d93969163412cfc2b3f36b02bfaff0d5/spyder/dependencies.py#L87-L98): Python 파일 열기 지원을 macOS에 알리는 용도로 설명하고 macOS에만 표시한다. 이것을 실제 기능 실행 결과로 올려 읽지 않았다.

## “일반 도구” 범위에 대한 유보

여섯 행은 **과거 공개 개발·실행 환경의 패키지 참조**로 적격이다. 역할을 보면 Python은 런타임, Sphinx는 문서 도구, setuptools는 빌드 도구/라이브러리이고, 나머지 세 행은 라이브러리다. NumPy·SciPy는 여러 용도의 수치 연산을 위한 라이브러리지만, applaunchservices는 플랫폼 통합 기능으로 범위가 좁다. 사용자 표현인 “일반 도구”를 독립 실행 도구로 한정하면 여섯 건 모두를 동일하게 적격이라고 확정할 수 없다. 특히 A-C06을 범용 CLI 사례처럼 서술하면 안 된다.

권고: 봉인 전에 이 역할 차이와 라이브러리를 포함한 해석을 명시하고, 원장·집계에서 도구/런타임과 라이브러리를 구별한다. “일반 도구만 6건”이라고 쓰는 엄격한 수용 조건은 별도로 판단해야 한다. 이 판독은 SCOPE를 수정하거나 행을 성공 가능성으로 교체하지 않는다. 목적의 분명함은 설치·호출·기능 설명 수준에서 충족하지만 “모든 소프트웨어 소비자”로 일반화할 근거는 없다.

## 남은 검증과 반증 시도

- 두 requirements 파일에 채널이 없다는 반대 설명을 같은 판 설치 명령으로 대조했고, 정확한 `--file` 연결을 확인했다. 반대로 A-C06에는 직접 기능 호출 근거가 없다는 한계가 남는다.
- requirements/Binder 사본을 두 소비자로 세거나, 사본의 conda-forge 채널만으로 주 설치 경로를 보충하는 방식은 배제했다. A-C06은 CONTRIBUTING 명령 자체에 채널이 있다.
- SHA 고정 원문은 모두 읽혔다. 커밋 날짜의 별도 API 재확인은 여섯 정확한 `/repos/{repo}/commits/{sha}` 요청이 HTTP 403이어서 성공하지 않았다. 날짜는 historical.json 수집자의 메타데이터에 의존하며 독립 재검증했다고 쓰지 않는다. 이는 원문 파일 접근 실패와 구별한다. 필요한 재개 입력은 각 행의 정확한 SHA에 대한 GitHub connector commit metadata이다.
- 2019/2021 후보 탈락과 본문 순서 선정의 전체 원장을 재판독하지 않았다. 따라서 이번 판독은 6개 최종 참조의 적격성 검토이며 모집틀 준수의 전체 독립 감사가 아니다.
