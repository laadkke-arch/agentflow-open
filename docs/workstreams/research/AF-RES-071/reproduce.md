# AF-RES-071 · 재현

실측 입력과 코드 기준은 [계측 코드 1f3499d](https://github.com/laadkke-arch/agentflow-open/tree/1f3499d47eac6f4cfa7b76b0e8fe5cacadbb4575/docs/workstreams/research/AF-RES-071)이며, [실측 원장](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/runs.jsonl)과 검산 코드가 든 커밋은 `abfa72b4c9482955ce8af049ff80831284d6eab8`다. 아래 실험은 표준 라이브러리, Python 3.12, SQLite만 필요하다. 저장소 루트에서 실행한다. 임시 출력 디렉터리를 사용하면 원장이 보존된다.

```sh
af071_path=docs/workstreams/research/AF-RES-071
af071_out=$(mktemp -d /tmp/af071-reproduce-XXXXXX)
python -B "$af071_path/experiment/prepare.py" "$af071_out"
cmp "$af071_path/pairs.csv" "$af071_out/pairs.csv"
cmp "$af071_path/inputs/sha256.json" "$af071_out/inputs/sha256.json"
python -B "$af071_path/experiment/run.py" --out "$af071_out"
python -B "$af071_path/experiment/audit.py" --out "$af071_out"
cmp "$af071_path/judgments.csv" "$af071_out/judgments.csv"
cmp "$af071_path/scores.csv" "$af071_out/scores.csv"
python -B "$af071_path/experiment/decisions.py" --output "$af071_out/evidence/design-decisions.jsonl"
cmp "$af071_path/evidence/design-decisions.jsonl" "$af071_out/evidence/design-decisions.jsonl"
python -B -m workbench.session check "$af071_path/manifest.json" --fetch
```

`run.py`는 공개판에서 파생한 `C0`와 합성판을 임시 디렉터리에 만들고 실제 Python 바이너리 읽기를 실행한다. 역할별 파일 SHA, 판 태그와 사건 ID는 기록이 다른 속성이다. `prepare.py`는 입력 및 기대를 계산하고, `oracle.py`는 원문 발췌를 별도 코드 경로로 다시 읽어 값을 확인한다. `storage.py`는 보기별 저장 투영을 SQLite에서 꺼내어 동일 질의를 처리한다. 회수된 자료는 보기당 2번, 누적 65,536B까지 허용된다. A2 조각은 로컬 SQLite BLOB으로 저장된다. 시간과 실행 UTC는 실측치이며 재실행마다 바뀐다. 원장 구조, 진릿값, 출력 지문, 두 표의 분모를 재현한다.

트랜잭션만 따로 재현하려면 `python -B "$af071_path/experiment/transactions.py" check "$af071_out/transaction-only"`를 실행한다. 하위 프로세스 종료코드 72·73·74는 시험이 유도하는 예외·강제 종료·연산키 충돌이다. 상위 검사 종료코드가 0이어야 한다. DB 파일과 SQLite 롤백 저널을 같은 디렉터리에 둔다. 시험은 처음 만든 임시 원장에 한한다.

## 발행사 확인 및 입력 취득

- `frame.csv`의 두 발행사 목록과 19개 위치 행을 확인한다. 전사는 NARA 렌더링에서 Transcript를 열고 `sources.jsonl` A14–A17이 위치시킨 해당 구간을 원문 철자·구두점 그대로 읽는다. A1의 조항 제목, A2의 제목과 섹션 이름, A4의 법 제목은 인접한 본문 문장과 구분한다. A3의 대시 뒤 종속 연결은 한 번의 원문 문장으로 판독했다. 각 텍스트 파일은 왼쪽에 그 브라우즈 위치의 행 번호를 붙인 발췌다. [A 원목록](https://www.archives.gov/milestone-documents/list)
- B는 지역검색의 원 ID를 먼저 가져온다. 상세 페이지의 `Composite Station Metadata`와 `Composite Station Threads`에서 두 원소의 개별 ID/이름/시작/끝/단위를 읽는다. 8300300의 강수 원소는 강수일 표의 스레드에서 확인했다. `inputs/B*.txt`에는 열 이름과 필요 행을 남겼다. 날짜를 ISO 형식으로, 두 원소의 단위를 °C와 mm로 옮긴 파일이 `inputs/objects.json`이다. [PE 8개 목록](https://climate.weather.gc.ca/climate_normals/station_select_1991_2020_e.html?climate_id=8300418&lstProvince=PE&searchType=stnProv&txtCentralLatMin=0&txtCentralLatSec=0&txtCentralLongMin=0&txtCentralLongSec=0)
- Codex Cloud의 공개 기관 HTTPS 쉘 요청은 403이었다. B의 정규 상세 페이지 open/click도 시간 초과했다. `search-log.jsonl`에 쓴 색인 검색에서 공개 발행사의 해당 본문을 읽어 발췌를 만들어 사용했다. 릴리스 기간 및 원 ID를 유지했고 쿼리 파라미터의 검색어와 실제 응답 원 ID를 구분했다. SHA는 크롤러의 전송 바이트나 원 PDF의 SHA가 아니라 보존한 UTF-8 발췌 및 파생 입력의 지문이다. 이 발췌로 실험을 로컬에서 다시 실행할 수 있다. [획득 위치·계보·한계](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/sources.jsonl) · [접근 실패 로그](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/search-log.jsonl) · [입력 지문](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/inputs/sha256.json)

발행사 응답 직접 대조는 공개 출처 접근이 지원되는 별도 클라우드 셸에서 작성한 임시 디렉터리로 다운로드한다.

```sh
af071_public=$(mktemp -d /tmp/af071-origin-XXXXXX)
python -B - "$af071_path/inputs/objects.json" <<'PY' > "$af071_public/urls.tsv"
import json
import sys
for row in json.load(open(sys.argv[1], encoding="utf-8")):
    print(row["id"], row["url"], sep="\t")
PY
while IFS="$(printf '\t')" read -r af071_id af071_url; do
  curl --fail --location --max-time 60 --output "$af071_public/$af071_id.html" "$af071_url"
  printf '%s exit=%s\n' "$af071_id" "$?"
done < "$af071_public/urls.tsv"
```

다운로드된 원본에서 섹션/행/단위 및 발췌를 비교하고 원 SHA를 따로 남긴다. 위 경로에 원본이 없는 경우 검색 실패와 내용 차이의 판정을 구분한다. `manifest.json`은 시작 계약을 보존한다. `session start`는 출발판에서만 새 기록을 만들며 위 재실행은 기존 계약을 `check --fetch`로 확인한다.
