# 실행 환경 준비와 복구

Debian GNU/Linux 13.6, Linux 6.18.57 x86_64, GCC 14.2.0, uv 0.13.6. CPython의 GitHub 태그 archives와 PyPI csvkit 의존 고정을 사용했다. csvkit 1.0.7 및 1.0.5의 표시상 판과 Python 패치판이 저자 보고와 일치한다. Fedora RPM의 패치·빌드 플래그·정확한 의존 조합과 C4 저자의 OS는 별도 미확인이다. 1.1.0은 Python 3.8.16과 1.0.5의 동일 cutoff에 두었다.

| 단계 | 실제 입력 또는 명령 | 종료·관측 |
| --- | --- | --- |
| uv 사전 빌드 | `UV_CACHE_DIR=<scratch>/uv-cache uv python install --install-dir <scratch>/uv-pythons 3.11.2 3.8.16` | 3.11.2 Linux x86_64 다운로드 레코드 없음. 소스 빌드로 전환 |
| CPython 소스 최초 | `./configure --prefix=<scratch>/python-<version> --with-ensurepip=no`, `make -j 6` | 두 빌드 0, `-VV` 성공. csvkit 명령 1, `ModuleNotFoundError: No module named '_bz2'` |
| OS 패키지 | `apt-get download libbz2-dev liblzma-dev libsqlite3-dev libffi-dev` | 100, apt metadata에서 패키지 찾지 못함. 시스템은 그대로 두고 scratch에 헤더 제공 |
| bz2 복구 | `CPPFLAGS=-I<scratch>/support/include LDFLAGS=-L<scratch>/support/lib ./configure …`, `make -j 5` | 두 빌드의 bz2 왕복 0, 1.0.7 csvformat 명령 1, `ModuleNotFoundError: No module named '_lzma'` |
| bz2 및 xz 복구 | 같은 configure/make에 xz의 고정 헤더와 공유 객체 symlink 추가 | CPython 3.11.2 / 3.8.16 bz2·lzma 왕복 모두 0, 각 csvformat·csvstat·in2csv의 `--version` 0 |
| 빌드 지원 데이터 | [bzip2 1.0.8 bzlib.h](https://github.com/libarchive/bzip2/blob/bzip2-1.0.8/bzlib.h) SHA-256 `6ac62e811669598ee30c9e1c379b9e627f6ff17a5a3dc1e0b4fa8b8ea75e580d`, [xz a522a22 헤더](https://github.com/tukaani-project/xz/tree/a522a226545730551f7e7c2685fab27cf567746c/src/liblzma/api) | 시스템 `libbz2.so.1.0` (Debian 1.0.8-6), `liblzma.so.5` (5.8.1-1+deb13u2)를 링크 |
| 로케일 대조 | CPython에서 `locale.setlocale(LC_ALL, name)`, `C`, `C.UTF-8`, `en_US.utf8`, `en_GB.UTF-8`, `en_GB.utf8` | 첫 셋 성공, en_GB 별칭 둘은 환경이 거절. 이 상태에서 csvstat 1.1.0은 import에서 1, 1.0.5는 실행. 두 버전이 지원되는 `C.UTF-8` / `en_US.utf8` 비교도 실행 |

실제 공개 패키지와 입력 지문은 [versions.json](../replay/versions.json), [fixtures.jsonl](../fixtures.jsonl)에서 확인한다. 실패 stdout/stderr와 중간 CSV는 [runs.jsonl](../runs.jsonl)에 저장했다.
