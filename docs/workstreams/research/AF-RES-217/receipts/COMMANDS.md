# 재현 명령과 영수증

명령은 저장소 루트에서 실행한다. Linux amd64, Python 3.12 이상, Git, curl, dpkg-deb, strace가 필요하다. 이번 실행은 Debian 13 x86_64에서 Bookworm의 지정 바이너리와 공유 라이브러리를 임시 디렉터리에 풀고 동적 로더 경로를 고정했다. 시스템에는 패키지를 설치하지 않았다. 다른 호스트에서는 시스템 라이브러리·SIMD 차이를 별도로 기록한다.

## 기록된 실행의 입력 및 도구

- [inputs.json](../inputs.json)에서 고정 URL, Git blob, SHA-256, 크기, 원본/합성 구분과 입력 비트 수를 읽는다. 프로그램은 상대 경로로 모델·패키지 바이트를 찾고 SHA-256 불일치를 검사한다.
- [package-chain.json](package-chain.json)의 InRelease 서명, index, .deb 반환값과 fingerprint를 연결했다. apt의 서명 검증 도구 sqv를 사용했다. 현재 미러 InRelease와 index는 갱신될 수 있다. 아래 fetch 명령은 본 실험이 서명 원장에서 확인한 고정 .deb SHA-256과 크기를 사용한다.
- [toolchain.json](toolchain.json)에 Tesseract·도구 ·Hunspell 버전, 도움말, ldd 대상과 stdout/stderr/exit, 플랫폼, 실행 파일·해석된 공유 객체 지문이 있다. shell의 PATH 기본 5.5.0은 실행 표본에 포함하지 않았다.
- 두 PNG는 [make_page.py](make_page.py)로 생성했다. 재실행 기록은 커밋된 fixtures 바이트를 쓴다. 그림 생성기를 다시 돌리려면 Pillow/libraqm/FreeType 및 DejaVu Sans 지문을 inputs.json과 비교한다.

## 빈 임시 경로 재현

~~~sh
set -eu
task=docs/workstreams/research/AF-RES-217
scratch=$(mktemp -d /tmp/af-res-217-repro.XXXXXX)
mkdir "$scratch/receipts"
python -B "$task/inspect.py" fetch "$scratch"
export LD_LIBRARY_PATH="$scratch/root/usr/lib/x86_64-linux-gnu"
"$scratch/root/usr/bin/tesseract" --version
"$scratch/root/usr/bin/tesseract" --help-oem
"$scratch/root/usr/bin/combine_tessdata" --version
"$scratch/root/usr/bin/hunspell" --version
unset LD_LIBRARY_PATH
python -B "$task/inspect.py" record "$scratch" "$scratch/receipts/components.jsonl"
python -B "$task/inspect.py" headers "$scratch" "$scratch/receipts/headers.jsonl"
python -B "$task/run.py" record main "$scratch" "$scratch/receipts"
python -B "$task/run.py" record controls "$scratch" "$scratch/receipts"
python -B "$task/inspect.py" replay "$scratch/receipts/components.jsonl" "$scratch/components.csv" \
  --headers "$scratch/receipts/headers.jsonl"
python -B "$task/run.py" replay "$scratch/receipts" "$scratch/runs.csv"
~~~

초기 원본 GitHub/공개 Debian 저장소에서 확보한 /tmp 입력을 사용했다. 본 실행과 대조의 실제 명령은 main.jsonl 및 controls.jsonl의 argv와 program_argv에 있다. 예컨대 R1에는 strace -f -qq -s 96 -yy, 지정 open/read syscall과 tesseract INPUT stdout --tessdata-dir DIR -l LANG --oem N --psm 6 --dpi 300이 기록된다. API 대조는 별도 Python 프로세스이고 Hunspell은 고정 표준입력을 쓴다. 반복 경로, PID, 타임스탬프와 라이브러리 매핑 주소는 새 실행에서 달라진다.

## 커밋된 기록에서 오프라인 재집계

~~~sh
set -eu
task=docs/workstreams/research/AF-RES-217
replay=$(mktemp -d /tmp/af-res-217-replay.XXXXXX)
python -B "$task/inspect.py" replay "$task/receipts/components.jsonl" "$replay/components.csv" \
  --headers "$task/receipts/headers.jsonl"
python -B "$task/run.py" replay "$task/receipts" "$replay/runs.csv"
cmp "$replay/components.csv" "$task/components.csv"
cmp "$replay/runs.csv" "$task/runs.csv"
python -B "$task/receipts/recheck.py"
~~~

각 JSONL 행의 ID가 표의 영수증과 대응한다. stdout/stderr 문자열은 JSON 이스케이프를 풀면 원바이트를 복원할 수 있다. 각 .txt는 필터 범위의 strace 원문이다. read 바이트 합에는 여러 번 읽은 영역이 포함될 수 있다. 결정 시에는 read 발생과 지문의 연결을 쓴다. main에서 별도 디렉터리당 모델 사본 한 개를 시작 전후로 검증했다.

~~~sh
python -m workbench.session check docs/workstreams/research/AF-RES-217/session.json --fetch
~~~
