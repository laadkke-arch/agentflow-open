# 반례와 사전판 수정

| 사전 해석·가능성 | 이후의 직접 관측 | 수정한 판정 |
|---|---|---|
| 하한을 충족하면 공개 바이너리 후보가 있을 수 있다 | M3/M6은 3.13이 릴리스 하한을 만족한다. 전체 버전 JSON과 Simple에서 태그 일치 0개. M6에는 별도 sdist가 있고 그 `PKG-INFO`에도 `>=3.10`이 있다. | 바이너리만 원하는 일반 GIL Linux x86_64 사용자는 두 셀에서 현재 직접 wheel 후보 0개. 소스 빌드 전망과 당시 파일 존재는 미확인. |
| 모델이 출력한 태그 항목 수를 wheel 수로 셀 수 있다 | M1/M2/M5/M8/M9 각각 filename 끝에 플랫폼 태그가 두 개, ZIP WHEEL에도 두 `Tag`가 있다. 두 독립 판독이 각 셀에서 같은 하나의 파일을 고른다. | 파일 단위 5, 부합 태그 단위 10. glibc 2.16 모형은 9셀 모두 0. 2.17+에서 태그가 부합한 실제 실행은 M9 2.41 한 번. |
| Python 3.13 또는 cp313 문자열이 같으면 함께 연결할 수 있다 | 표본 3판 free-threaded 후보 0/3. 대조한 1.15.0 `cp313-cp313t` x86_64 wheel은 ZIP WHEEL에도 t가 있고, 자유 스레딩 태그에 1, GIL에는 0이다. | 후속판은 별도 비교. 1.14.1 GIL 링크의 적용 범위를 넓히지 않는다. |
| 배포판 및 Python/ABI만 같으면 파일 링크를 고를 수 있다 | 1.14.0 CPython 3.10의 macOS arm64 14.0 wheel은 Linux wheel과 같은 `>=3.10` 및 `cp310-cp310`을 가진다. ZIP 태그는 macOS이고 두 Linux 파서 모두 0. | 파일명에서 OS·아키텍처·libc를 각각 확인. 태그상 Linux 후보 1개만 유지. |
| 3.13 classifier가 없으면 해당 버전 wheel이 없다 | 1.14.1 `info.classifiers`, 동판 `pyproject.toml`, M9의 METADATA에 3.13 classifier 부재. 반면 릴리스 공지, 3.13 job 정의, 검산한 M9, 오늘의 로컬 GIL import/solve가 양성. | classifier와 파일 호환·배포·시험은 별도 관측. |
| 날짜가 같으면 발표 전후를 가를 수 없거나 공개 파일 모두가 발표 전에 올라왔을 것이다 | 9셀 양성 5/5와 전체 82/83 파일의 PyPI 업로드 기록은 GitHub 공지 표시값보다 먼저다. 1.14.1 CPython 3.12 macOS x86_64 파일 하나만 `04:08:04.150472Z`로 공지 `00:10:50Z` 후다. GitHub 자산 시각 `04:06:56Z`, 발행 README에 checksum 행이 없다. 두 호스트에서 받은 바이트는 같은 39,128,781 B 및 SHA-256이다. | 같은 판·같은 날에도 서로 다른 게시 순서와 채널 시각이 있다. 1.14.1의 README 목록은 오늘도 32개 wheel 중 31개를 포함한다. 과거 삭제·교체 및 첫 공개는 당시 스냅샷/작업 기록을 기다린다. |
| 태그의 CI 파일이나 현재 아티팩트 일치가 있으면 당시 시험까지 주장할 수 있다 | 1.14.1은 빌드/시험/업로드 정의가 있고 M9 발행 해시도 일치한다. 다만 공개 체크 조회는 job 행 부재, PyPI provenance 5건 404. 확인한 실제 오류는 PR #21409의 aarch64 개발 로그 발췌이며 exact tag x86_64 시험과 연결되지 않는다. | GitHub 발행 digest와 당시 job이 소비한 digest를 구분한다. M9 새 로컬 시험만 시행 범위로 남긴다. |

기계 판정은 [두 파서 반례 출력](receipts/computed/counterexamples.json)과 [파일별 시각/해시](files.csv)에서 재생된다. 근거는 [1.14.1 공지와 Assets](https://github.com/scipy/scipy/releases/tag/v1.14.1), [발행 체크섬 README](https://github.com/scipy/scipy/releases/download/v1.14.1/README.txt), [개발 Issue #20992](https://github.com/scipy/scipy/issues/20992), [Cirrus PR #21409](https://github.com/scipy/scipy/pull/21409), [1.15.0 free-threaded 발표](https://docs.scipy.org/doc/scipy-1.15.0/release/1.15.0-notes.html#preliminary-support-for-free-threaded-cpython-3-13)에서 읽었다.

## Nikon 정규화한 두 행

| 설치 대상 | 현재 C 범위 → 목표 | 설치 파일 | 다운로드 컴퓨터·링크 호스트 | 같은 호스트라는 잘못된 판정 |
|---|---|---|---|---|
| D850 | 1.00–1.30 → 1.31, 발행일 2024-04-25 | `D850_0131.bin` | Windows 또는 Mac OS 선택. 페이지에 두 `crossgate.nikonimglib.com` 링크 | 올바른 다운로드 OS여도 Z 6II에는 대상 불일치. 이미 D850 C 1.31이면 업데이트 불필요. [D850 원행](https://downloadcenter.nikonimglib.com/en/download/fw/529.html) |
| Z 6II | 1.00–1.62 → 1.70, 발행일 2025-06-03 | `Z6_2_0170.bin` | Windows 또는 Mac OS 선택. 페이지에 두 `crossgate.nikonimglib.com` 링크 | 올바른 다운로드 OS여도 D850에는 대상 불일치. 이미 Z 6II C 1.70이면 업데이트 불필요. [Z 6II 원행](https://downloadcenter.nikonimglib.com/en/download/fw/560.html) |

날짜는 제조사 제품 목록의 일 단위 값이다. 호스트 링크의 실제 리다이렉트, 바이트 동일성, 펌웨어 적용은 미실행이다. [D850 목록](https://downloadcenter.nikonimglib.com/en/products/359/D850.html), [Z 6II 목록](https://downloadcenter.nikonimglib.com/en/products/556/Z_6II.html).
