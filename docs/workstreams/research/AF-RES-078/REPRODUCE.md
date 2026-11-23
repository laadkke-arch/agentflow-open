# AF-RES-078 재현

## 시작 입력

본 연구의 [fixtures.jsonl](fixtures.jsonl)에 시험 입력의 역할과 기대값이 있다. [inputs/](inputs/)에는 원본 PNG 및 표 값이 있다. SQL DB는 격리된 작업 디렉터리 안에 매번 만들고 읽기 전용으로 사용한다. 공개된 시드는 같은 경계 자료를 다시 만드는 데 사용한다. 독립적인 새 입력을 검증하려면 새 시드와 예측 봉인부터 시작한다.

실행에는 Linux `/proc`의 실행 프로그램과 wait channel 확인, SIGTERM/SIGKILL 및 FIFO가 필요하다. 외부 네트워크는 패키지·저장소 취득에만 사용했다. 연구 재생 단계에는 원격 호출이 없다. 사용 판은 [런타임](evidence/runtime-versions.json), ZIP 패키지·DB 바인딩 및 Debian SQLite 취득 정보는 [취득 영수증](evidence/runtime-acquisition.json)에 있다.

| 역할 | 직접 실행한 판 |
| --- | --- |
| SQLite CLI 및 연결 라이브러리 | Debian x86_64 3.46.1-7+deb13u2 |
| 표의 reader | CPython 3.13.5, Debian 3.13.5-2+deb13u5 |
| Pillow 및 검사 프로세스 | Pillow 13.0.0 + CPython 3.12.14 |
| zip 및 이름 교차 검사 | Info-ZIP Zip 3.0, Debian 3.0-15+deb13u1 + UnZip 6.00, Debian 6.0-29+deb13u1 |

## 버전과 실행 경로

Codex Cloud 기계에서는 Python/Pillow 및 zip/unzip이 있었다. sqlite3 시스템 패키지를 설치하는 대신 다음 Debian 파일 둘을 전용 임시 위치에 풀어 사용했다. 해시를 대조해 같은 입력을 고정한다.

```bash
AF078_RUNTIME=$(mktemp -d /tmp/af078-runtime-XXXXXX)
AF078_DEBIAN=https://deb.debian.org/debian/pool/main/s/sqlite3
curl -fSs "$AF078_DEBIAN/sqlite3_3.46.1-7+deb13u2_amd64.deb" -o "$AF078_RUNTIME/sqlite3.deb"
curl -fSs "$AF078_DEBIAN/libsqlite3-0_3.46.1-7+deb13u2_amd64.deb" -o "$AF078_RUNTIME/libsqlite3.deb"
(
  cd "$AF078_RUNTIME"
  sha256sum -c <<'SUM'
877b00bd5ab6a3792fdffebd4aeebe0b8178df3c21f0e06f6a3c5186f7a799d9  sqlite3.deb
0a459adaffd901109f7811ab65f58e7a957b4907d05539cf3d1184efdcde0468  libsqlite3.deb
SUM
)
dpkg-deb -x "$AF078_RUNTIME/sqlite3.deb" "$AF078_RUNTIME"
dpkg-deb -x "$AF078_RUNTIME/libsqlite3.deb" "$AF078_RUNTIME"
export AF078_SQLITE="$AF078_RUNTIME/usr/bin/sqlite3"
export AF078_SQLITE_LIB="$AF078_RUNTIME/usr/lib/x86_64-linux-gnu"
export AF078_PY_CSV=/usr/bin/python3.13
export AF078_PY_IMAGE="$(command -v python)"
```

아래는 저장소 루트에서 실행한다. `verify.py`는 커밋 관계를 읽으므로 완전한 작업 브랜치 이력이 필요하다.

```bash
AF078_DIR=docs/workstreams/research/AF-RES-078
AF078_REPLAY=$(mktemp -d /tmp/af078-replay-XXXXXX)
python -B -m workbench.session check "$AF078_DIR/manifest.json" --fetch
bash "$AF078_DIR/tools/replay.sh" "$AF078_REPLAY"
```

동일한 설치에서 재생한다면 기존 연구 바이트를 덮어쓰지 않는다. 원본 48시도의 입력·교환·끝 지문과 판정/종료, 진단 18개 행의 요건·종료, 단독 8개 행과 판 정보가 대조 대상이다. 절대 실행물 경로가 다른 설치에서 `versions`의 argv 차이가 생길 수 있다. 이 경우 동일 시험판의 바이너리 해시와 파일 판정을 별도로 확인한다. 특정 호스트의 `/proc`이 child wait channel을 공개하지 않으면 명시한 중단 위치는 재현 불가로 처리한다.

공개 시험 입력과 출력 영수증을 재판독만 하려면 `python -B "$AF078_DIR/tools/verify.py"`로 실행한다. 개별 입력·로그·이전/임시/완료품 바이트는 [artifact 원장](evidence/artifacts.jsonl)의 SHA-256으로 복원할 수 있다.
