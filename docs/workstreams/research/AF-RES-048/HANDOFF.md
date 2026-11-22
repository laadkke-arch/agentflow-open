# AF-RES-048 · HANDOFF

**부분 인계.** 공식 Matplotlib 3.11.2 게시 바이트를 확보한 2/9개 후보 풀에서 고유 경로 40개를 저장 재생했다. 고유 1차 원문 33개를 직접 판독했다. 수용 항목 38개 중 28개 충족·10개 미충족이다. 자연 5풀과 PyPA 2풀의 원응답 결측, 원 게시 주소의 직접 도착 및 MTA 정규 GTFS 확인이 남았다.

## 고정 결과

| 항목 | SHA·주소·위치 |
| --- | --- |
| 작업 브랜치 및 소유 경로 | `work/research-af-res-048` · `docs/workstreams/research/AF-RES-048/` |
| 계획 / 실제 시작 통합 SHA | `1f722bfb7360ff9c8d221284d7b1b6484c6fa692` / `4492dd8e9978087b32897ec2685110d24f510473` |
| 고정 결과 SHA | `a690049db3a0e22ae20e0573a67925b8800efb34` |
| 필수 표 위치 | [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/RESULT.md) 첫 표 5–13행, 둘째 표 17–43행, 마지막 약점 표 89–91행 |
| 수용 원장·자체 점검 | [acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/evidence/acceptance-evidence.json) · [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/a690049db3a0e22ae20e0573a67925b8800efb34/docs/workstreams/research/AF-RES-048/SELF_CHECK.md) Q1–Q7 |
| 고정 재열람과 최종 검사 | [final-verification.json](https://github.com/laadkke-arch/agentflow-open/blob/835ca552a54ddfa34a4c9e6d7add21f34055bbdd/docs/workstreams/research/AF-RES-048/evidence/final-verification.json) · `835ca552a54ddfa34a4c9e6d7add21f34055bbdd` |
| 의존 결과 | [AF-RES-044 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/6c8c025284215c7749921619cb09c89643886276/docs/workstreams/research/AF-RES-044/HANDOFF.md) · `6c8c025284215c7749921619cb09c89643886276` |
| 실행 환경 | 관리형 Linux 셸, Python 3.12.14, GitHub 연결. 내부 확인 표기는 Codex/GPT-6, 배정은 codex-cloud. 정확 모델 변형·추론 강도와 계정 UI 값은 미확인. |

두 관측 풀에서 C가 각각 서로 다른 두 URL을 병합했고, 두 풀 모두 대표 배열이 바뀌었다. 각 풀에는 원후보가 세 개였고 새로운 대표 URL은 나오지 않았다. M1의 원풀 완결 ID 하나는 A/B/C 모두 직접과 두 동작 내에 남았다. A만 M1-2의 짧은 경로 T011에서 원풀 밖 TightLayoutEngine의 생성·겹침 계약까지 함께 읽었다. B/C에서 동일 href를 여는 경로는 세 번째 동작이거나 첫 두 href 예산 밖이다. M2는 원풀 완결 분모가 0이고, standalone의 표시 방법은 C의 대표에서 형제 목록으로 이동했다. 관측되지 않은 7풀은 효과 미확인이다. [변화 원장](changes.csv) · [T011](trials.csv#L12)

같은 공식 문서 목차의 후속 탐색에서는 앞 세 자리가 같고 뒤쪽 그룹만 줄어든 실제 HTML 절을 찾았다. 다른 상류의 완결 구현이 새 대표로 회복된 관측은 없었다. 국립국회도서관의 두 발행 레코드와 MTA의 양방향 시간표를 확인했다. MTA 정규 ZIP의 동일성은 공개 사본과 시간표 대조에서 확인되지 않았다. [RESULT.md 후속 탐색·다른 분야](RESULT.md)

## 원격 커밋 순서

| 순서 | 원격 SHA | 파일 |
| --- | --- | --- |
| 묶음 1 | `8cd74ab245d4c300c2cd10ddee1cfcdc86e03c0f` | `manifest.json`, `SCOPE.md`, `frame.csv` |
| 묶음 2 | `e8c494a52858ba3ce2dee9c45c71b98cdf377928` | `captures.jsonl`, `pool.csv`, `groups.jsonl`, `sources.jsonl`, 최초 20 범위와 정정 전 스캔 |
| 묶음 3 | `cc156a53923e895f402e8d78b168d83b5b788278` | `replay.py`, `trials.csv`, `gold.csv`, `changes.csv`, 직접 판독 및 경로 입력 |
| 묶음 3 재판독 | `2f0d8b2b7d904a03f57f6587e54e506577b7146d` | 같은 절의 E16–E19와 집계 정정, [이전 값](evidence/gold-recheck.json) |
| 묶음 4 | `a690049db3a0e22ae20e0573a67925b8800efb34` | `RESULT.md`, `SELF_CHECK.md`, `evidence/acceptance-evidence.json`, 청정 재생·민감도 |
| 고정 검증 | `835ca552a54ddfa34a4c9e6d7add21f34055bbdd` | `evidence/final-verification.json` |
| 인계 | 이전 행을 부모로 하는 마지막 단독 커밋 | `HANDOFF.md` |

두 고정 파일을 GitHub의 결과 SHA에서 다시 열어 본문 blob과 표 행 수를 대조했다. 고정 결과 SHA에서 2026-11-22T22:47:14Z에 `workbench.session check --fetch`가 종료코드 0, `passed`, `remote_checked`를 반환했다. `outside_paths`, `unmerged_paths`, `errors`는 각각 빈 목록이다. 깨끗한 두 저장 재생의 출력이 동일하고, 그 후 고정 결과 SHA에서도 재생했다. 원격 작업 커밋의 변경은 소유 경로 안에 있다. [최종 영수증](evidence/final-verification.json)

## 재개 첫 행동

원 게시 HTML을 얻을 수 있는 승인된 실행환경에서 **Pandoc MANUAL의 HTTP 원응답 바이트 확보**부터 시작한다. 아래 새 디렉터리는 Pandoc·Vega-Lite·Matplotlib stable·PyPA 시작 응답과 MTA 정규 ZIP을 별개 새 획득으로 보존한다. 기존 P/V/Y 결측은 그대로 둔다. Pandoc은 `frame.csv` P1R–P4R을, Vega-Lite는 V3R의 `word cloud`와 fallback을 입력으로 사용한다. PyPA는 첫 20개의 공식 HTML 문서와 명시판을 확인한 뒤 순서대로 적격 풀을 고른다. [SCOPE.md 자연·보강 절](SCOPE.md) · [획득 원장](captures.jsonl)

```bash
python -B docs/workstreams/research/AF-RES-048/evidence/acquire.py /tmp/af-res-048-new-publications --publisher
python -I -B docs/workstreams/research/AF-RES-048/replay.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-048/manifest.json --fetch
```

남은 실제 HTTP 검사의 최소 대표는 M1의 T011이다. 두 URL은 [trial-plan.jsonl T011](evidence/trial-plan.jsonl#L11)에 있고 각각의 예상 SHA256·정확 fragment·절은 [windows.jsonl](evidence/windows.jsonl)에 있다. 새 HTTP 세션에서 첫 응답이 같은 바이트인지 확인하고, 같은 바이트이면 열린 압축 절의 첫 href로 두 번째 요청을 한다. 아래 명령은 원 URL의 응답 두 건을 순서대로 해시 비교한다. 실패하거나 바이트가 달라지면 그 시행은 새 판 미확인으로 남는다. 전체 다시 실행에는 같은 두 입력의 모든 계획 행을 사용한다.

```bash
python -B - \
  docs/workstreams/research/AF-RES-048/evidence/trial-plan.jsonl \
  docs/workstreams/research/AF-RES-048/evidence/windows.jsonl <<'PY'
import hashlib, json, sys, urllib.request
from pathlib import Path
from urllib.parse import urldefrag
plans = [json.loads(s) for s in Path(sys.argv[1]).read_text().splitlines()]
windows = {r["url"]: r for r in map(json.loads, Path(sys.argv[2]).read_text().splitlines())}
for step in next(row for row in plans if row["id"] == "T011")["steps"]:
    url = step["url"]
    with urllib.request.urlopen(urldefrag(url).url, timeout=30) as response:
        digest = hashlib.sha256(response.read()).hexdigest()
        print(response.status, response.geturl(), url, digest, windows[url]["section"])
        if digest != windows[url]["sha256"]:
            raise SystemExit("New response: retain separately and verify the fragment before continuing")
PY
```

MTA 원 ZIP이 확보되면 `unzip -p /tmp/af-res-048-new-publications/new-mta-static.raw stops.txt`에서 `120`, `120N`, `120S`를 찾는다. `stop_times.txt`를 `trips.txt`의 `trip_id`로 연결해 1번 노선 방향과 시간표 2026-05-17 적용판의 p2·p7을 대조한다. 승강장 식별과 발행일·서비스일을 함께 기록한다. [MTA 발행 안내](https://www.mta.info/developers#static-gtfs-data)

색인 제안은 **표시 키 → 원 URL 및 절 → 시행별 도달 → 구현·판의 필요조건**을 연결하고 원풀 밖 도달을 별도 필드로 유지하는 것이다.

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 공식 시작 HTML 세 계열 결측 | 자연 5풀과 PyPA 2풀의 후보 순서·분모 | [captures P48/V48/Y48](captures.jsonl) · [frame.csv](frame.csv) | Pandoc MANUAL 바이트·판과 해시부터 새 획득으로 보존 | 원응답에서 절과 URL들이 고정되면 후보 적격·손실을 다시 판단한다. |
| 공식 게시 주소 live GET 두 건 거절 | 실제 네트워크의 같은 두 동작과 최종 절 | [T001/T021 live](evidence/live-trials.jsonl) · [T011 계획](evidence/trial-plan.jsonl#L11) | 권한 있는 환경에서 T011의 순서·최종 URL·응답 해시를 검증 | 바이트 또는 도착 절이 바뀌면 저장 경로가 보여 준 계약의 적용 범위가 바뀐다. |
| 앞자리가 충분한 두 주표본과 MTA 정규 ZIP 미확인 | 독립 구현의 새 대표 회복 및 승강장별 외적 적용 | [후속 40문서](evidence/post-seal-matplotlib-screen-40.json) · [MTA regular ZIP](https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip) | 네 후보 이상 실제 풀과 MTA 정규 stop/trip 행을 확보 | C에서 새 완결 구현을 읽거나 정규 feed가 사본과 달라지면 해당 판단이 바뀐다. |
