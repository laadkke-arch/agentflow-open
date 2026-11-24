# AF-RES-115 재현

## 고정 자료에서 보기와 판정 생성

GitHub에서 작업 브랜치를 가져온 checkout의 루트에서 실행한다. Python 3.12와 Git, 대조 XSD를 위한 lxml이 필요하다. 결과는 새 임시 디렉터리에 쓴다.

```sh
bundle=docs/workstreams/research/AF-RES-115
scratch=$(mktemp -d /tmp/af-res-115-replay.XXXXXX)

python -B "$bundle/tools/materialize.py" "$scratch/blobs" "$scratch/expanded.jsonl" --fetch
python -B "$bundle/tools/structure.py" "$scratch/expanded.jsonl" "$scratch/blobs" "$scratch/views.jsonl"
cmp "$bundle/views.jsonl" "$scratch/views.jsonl"

python -B "$bundle/tools/replay.py" "$scratch/replays" --views "$scratch/views.jsonl"
cmp "$bundle/runs.jsonl" "$scratch/replays/runs.jsonl"
cmp "$bundle/evidence/replays.json" "$scratch/replays/replays.json"

python -B "$bundle/tools/verify.py" --runs "$scratch/replays/runs.jsonl" \
  --tables "$scratch/tables.md" --evidence "$scratch/verification.json"
cmp "$bundle/evidence/verification.json" "$scratch/verification.json"
sed '/^## 결론$/,$d' "$bundle/RESULT.md" > "$scratch/result-tables.md"
cmp "$scratch/result-tables.md" "$scratch/tables.md"

git clone --quiet --depth 1 --branch v4.0 https://github.com/w3c-cg/musicxml.git "$scratch/musicxml"
git -C "$scratch/musicxml" rev-parse HEAD
python -B "$bundle/tools/provenance.py" "$scratch/blobs" "$scratch/external" \
  "$scratch/expanded.jsonl" "$scratch/musicxml/schema" "$scratch/provenance.json"
cmp "$bundle/evidence/provenance.json" "$scratch/provenance.json"
```

schema commit은 `799e2defb2ece0ae7bafe08dcbcac25b2c631d53`이다. lxml 판이 달라지면 출력에서 validator 필드만 달라질 수 있다. E05는 GitHub opening의 CRLF 문자를 유지한 SHA가 맞을 때 정확한 inline JSON을 가져온다. M60 선행 파일과 작성자 패치 뒤 파일은 각각 pinned URL에서 가져온다. 공개 주소가 바뀌면 임의로 새 데이터로 바꾸기 전에 원장에 불일치와 SHA를 남긴다. 생성 시 M60-d와 두 합성 대조의 각 변형은 별도 SHA 파일이다. 비교기의 두 런은 그 경로를 보지 않는다. [실제 입력](inputs.jsonl) · [봉인](evidence/gold-seal.json)

## 생성순과 링크 상태 재확인

기록한 검색 시점 이후 이슈의 opening이 편집·이동되면 현재 결과가 달라질 수 있다. 생성순 순위와 원본문 SHA를 각각 비교한다. 1차 조회의 긴 날짜 폭은 1,000건 상한을 재현하며, 2차는 쿼리 문구를 유지하고 시간 구간만 나눈다. 직접 열어 둔 본문 캐시를 두 조회에서 공유한다.

```sh
frame_pin=94688a38659879cc5020aae93b532d58ebc50126
scan=$(mktemp -d /tmp/af-res-115-frame.XXXXXX)
git show "$frame_pin:$bundle/tools/frame.py" > "$scan/frame-initial.py"
python -B "$scan/frame-initial.py" "$scan"
cp "$scan/scan.csv" "$scan/scan-original.csv"
cp "$scan/E-lists.json" "$scan/E-lists-original.json"
cp "$scan/M-lists.json" "$scan/M-lists-original.json"
python -B "$bundle/tools/frame.py" "$scan"
python -B "$bundle/tools/frame_review.py" "$scan" "$scan/review"
```

`review`에는 자동 opening 판독만 재생성된다. 수작업 판독·타 분야·원 코드 근거는 이 브랜치의 `sources.jsonl`에 있다. `frame_notes`의 접근 실패를 재개할 때는 각 원글의 주소에서 원 파일을 받고, GitHub 원 ZIP이 이동하면 그 공개 도착 호스트를 확인한다. 각 아카이브에서 안전한 파일명 목록, 포맷 시작부, 안쪽 구조 바이트 SHA와 선택 표시를 기록한다. 403은 이 실행 경로의 접근 실패다. [모집 기록](frame-notes.md) · [원 시도 URL](evidence/attachment-attempts.jsonl)

## 원래 앱 동작을 확인할 입력과 명령

- **Excalidraw E05.** 필요한 입력은 `inputs.jsonl`의 clipboard JSON, 폰트 크기 `18.092888001469653`, 재현할 텍스트와 당시 localhost checkout이다. 정확한 checkout과 실제 입력 텍스트를 알 수 없다. v0.11.0 같은 판 대조는 원 사건 재실행과 별도로 해당 checkout에서 `yarn install --frozen-lockfile` 뒤 `CI=true yarn test:app --watchAll=false --runInBand src/tests/binding.test.tsx`를 실행한다. 그 판의 `package.json`에서 test:app 진입점을 확인했다. 직접 입력은 `yarn start`로 열린 앱에서 clipboard를 붙이고 사각형과 text, container 및 화살표의 JSON 앞뒤를 기록한다.
- **MuseScore M60.** 필요한 입력은 `inputs.jsonl`의 raw 두 파일과 보관판 `ee7506f7a877b79f905fc15b3f0051e468d397de`다. 해당 보관판의 `src/engraving/tests/CMakeLists.txt`에서 `tst_repeat.cpp`가 fail 주석과 함께 제외돼 있다. 현재 빌드 정보만으로 그 테스트 실행을 주장할 수 없다. 임시 MuseScore 워크트리에서 해당 판의 Qt/engraving 의존성과 동작하는 repeat test 진입점을 마련한 뒤 아래 명령으로 타깃을 확인한다. 그 타깃이 실제로 `repeat14`를 등록한 경우 두 artifact를 같은 `src/engraving/tests/repeat_data/repeat14.mscx` 경로에 한 번씩 놓고 나머지 입력을 고정한다. C++ 비교용 reference와 화면 주석, RepeatList를 별도로 수집한다. [대상 테스트 구성](https://github.com/musescore/MuseScore/blob/ee7506f7a877b79f905fc15b3f0051e468d397de/src/engraving/tests/CMakeLists.txt#L21-L45)

```sh
cmake -S . -B /tmp/af115-muse-build -DBUILD_UNIT_TESTS=ON
cmake --build /tmp/af115-muse-build --target engraving_tests
ctest --test-dir /tmp/af115-muse-build -R '^engraving_tests$' -V --output-on-failure
```

현행 타깃을 그대로 실행하면 `repeat14` 등록이 입증되지 않으므로 위 실행이 곧 해당 원 케이스 검사임을 뜻하지 않는다. 등록을 확인할 때까지 M60의 기계 관측은 원본 앞뒤의 바이트 차이로 제한한다. [바이트 대조](evidence/provenance.json)

## 저장소 계약

```sh
python -B -m workbench.session check "$bundle/manifest.json" --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

검사 결과 SHA와 명령을 인수 영수증에 남긴다.
