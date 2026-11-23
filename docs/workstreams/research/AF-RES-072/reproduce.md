# AF-RES-072 재생·대조

저장소 루트에서 실행한다. 관측 환경은 Codex Cloud, Python 3.12.14와 lxml 6.1.1이다. `-B`로 유도한 실행은 저장소에 바이트코드를 쓰지 않는다. 임시 입력 디렉터리를 매번 새로 만들고 결과 파일은 그 아래에 쓴다.

## 입력과 고정 SHA

| 구분 | GitHub SHA 또는 SHA-256 |
| --- | --- |
| 모집 및 작업계약 | `9c0306072f8a9fb0fa3bfea7040c750092a86c54` |
| 20원본·카드 | `17898b7748bb1909ecb0c54beba553d6168ec126` |
| 가림 qrels | `41b73e199f9529bc5ce3165532b87d88eb4d62d0` · [파일 지문](evidence/qrel-seal.json) |
| 보류 순위 | `b74de450e7f0f0ffff150b8662cb840388a17aea` · [입력·출력 지문](evidence/rank-seal.json) |
| 라이브·반복·번역·실패 | `168d8da351873873fa121932a6dc514386d524cb` · [원장 지문](evidence/replay-comparison.json) |
| 20본문·압축 | [파일별 SHA-256와 바이트](frozen/manifest.jsonl) |
| 재생 원순위 | `c2b7aad3fce53dd0c336c2b52538e4483802dd282b43242ac581dd95f4962710` |
| 재생 원표시 및 영수증 | `311ef22d6a80d7386608d9a78bb6a12301a500df87d935c4fa163bd6853e7f58` |
| 정리된 표·수용 원장·계약의 검증판 | [최종 인계](HANDOFF.md) |

`fetches.jsonl`은 여러 실행의 합본이다. 여기에 관측층 ID와 고정판 지문 비교 필드를 붙였다. 지문 표의 단일 재생 원영수증과는 서로 다른 파일이다. 프로그램 실행시간, 라이브 시각 및 HTTP 응답 헤더는 결정성 판정에서 제외한다. `ranks.csv`와 오프라인 원영수증은 두 프로세스에서 실제 바이트가 같았다. R과 F의 ID는 각 층에서 반복되므로 그 층을 포함해 결합한다. [실행 지문](evidence/replay-comparison.json)

## 원 자료집의 두 번 재생

```sh
p=docs/workstreams/research/AF-RES-072
af072_tmp=$(mktemp -d)
mkdir -p "$af072_tmp/input/frozen"
cp "$p"/search.py "$p"/passages.py "$p"/source_io.py "$p"/capture.py "$af072_tmp/input/"
cp "$p"/urls.jsonl "$p"/requests.jsonl "$p"/cards.jsonl "$p"/purpose.jsonl "$p"/translated.jsonl "$af072_tmp/input/"
cp -R "$p"/frozen/body "$af072_tmp/input/frozen/body"
python -B "$af072_tmp/input/search.py" "$af072_tmp/a"
python -B "$af072_tmp/input/search.py" "$af072_tmp/b"
cmp "$af072_tmp/a/ranks.csv" "$af072_tmp/b/ranks.csv"
cmp "$af072_tmp/a/fetches.jsonl" "$af072_tmp/b/fetches.jsonl"
sha256sum "$af072_tmp/a/ranks.csv" "$af072_tmp/a/fetches.jsonl"
python -B "$p/audit.py" --replay-a "$af072_tmp/a" --replay-b "$af072_tmp/b"
python -B "$p/report.py" "$af072_tmp/tables.md" "$af072_tmp/metrics.json"
```

입력 폴더에는 판정표·순위·원출처 연구 노트가 없다. L은 링크와 요청 및 선택한 원문만 열었다. I는 링크·요청·카드만 열었다. 실제 시스템 호출을 추가 확인하려면 같은 임시 입력에서 두 방식을 한 개씩 실행한다. [실제 경로 관측](evidence/input-access.json)

```sh
strace -f -e trace=openat -o "$af072_tmp/L-openat.log" \
  python -B "$af072_tmp/input/search.py" "$af072_tmp/L" --arms L
strace -f -e trace=openat -o "$af072_tmp/I-openat.log" \
  python -B "$af072_tmp/input/search.py" "$af072_tmp/I" --arms I
python -B "$p/blind.py" "$af072_tmp/blinded"
```

가림 입력은 원본문·조건·섞인 alias만 판독용으로 사용한다. `mapping.jsonl`은 채점 후 alias를 합칠 때 쓰는 파일이다. 과거 연구자의 판단을 새 독립 판정으로 간주하지 않는다. 모든 요청의 쌍 판독과 위치는 `qrels.csv`에 이미 동결되어 있다. [별도 판정 해시](evidence/qrel-seal.json)

## 공개 원문·라이브·사후 감도

```sh
python -B "$af072_tmp/input/capture.py" "$af072_tmp/refetch"
python -B "$af072_tmp/input/search.py" "$af072_tmp/pilot" --split pilot
python -B "$af072_tmp/input/search.py" "$af072_tmp/live" --mode live
python -B "$af072_tmp/input/search.py" "$af072_tmp/ko" --mode translated
python -B "$af072_tmp/input/search.py" "$af072_tmp/missing" --mode failure --drop O02 A07
cp -R "$af072_tmp/input" "$af072_tmp/control-input"
cp "$p/evidence/counterexample-control.jsonl" "$af072_tmp/control-input/requests.jsonl"
python -B "$af072_tmp/control-input/search.py" "$af072_tmp/control"
```

라이브는 같은 공개 주소를 받고 응용 캐시를 경로·요구 단위로 투입한다. 한 HTTP 오류 또는 한도 거절이 생겨도 동결판의 오프라인 실행은 별도다. 반복은 직전 그 경로의 성공한 본문만 메모리에 둔다. 공개 목록·GitHub 이슈 최초 공개판과 서비스 응답은 시각에 따라 바뀔 수 있다. 본문 전체에서 읽을 조각을 고른 계산량과 표시 단어는 각각 영수증에 있다.

## 작업 계약

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-072/manifest.json --fetch
git diff --check
```

최종 인계의 결과판을 원격에서 직접 다시 받으면 릴리스 핀과 연구 결과의 저장 상태를 별도로 확인할 수 있다. 실물 터치·제품 당시 런타임은 이 연구의 실행에 포함되지 않는다. 그 재검증은 [Zotero #3555](https://github.com/zotero/zotero/issues/3555) 작성자와 동일한 앱 판 및 실제 터치 장치를 확보한 후, 라이브러리 탭과 PDF 뷰어에서 같은 길게 누르기를 각각 입력하여 출력 메뉴를 기록한다.
