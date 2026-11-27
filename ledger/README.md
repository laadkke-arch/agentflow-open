# ledger · 확인 장부 코어 (첫 구현 단위)

설계서 [docs/design/final](../docs/design/final/README.md)의 첫 구현 단위(06 3절, "확인 장부 코어로 R1 한 요청을 실제 원문에서 끝까지")다.
Python 3.11 이상, 표준 라이브러리와 SQLite FTS5만 쓴다. 클라우드 DB와 배포는 없다.
구현하면서 드러난 설계 수정점은 [08-implementation.md](../docs/design/final/08-implementation.md)에 있다.

```sh
python3 -I ledger/tests/run.py            # 시험 78개. 네트워크 없이 기록 재생
python3 -I ledger/run_r1.py               # R1을 기록 재생으로 돌려 결과를 출력
python3 -I ledger/run_r1.py --live        # 실제 검색·원문·실행으로 돌리고 기록, out/r1_live.json을 쓴다
python3 -I ledger/run_unit2.py             # 둘째 단위: EVAL-X1 기록 재생(위상 12개)
python3 -I ledger/measure.py [--live]     # A4·B1·R-4·R-6·정규화 회귀·F01 잡음·위치 대응 측정, out/measure_*.json
```

`--live`는 `api.github.com`(코드 검색, 환경의 `GITHUB_TOKEN`)과 `raw.githubusercontent.com`(원문), 로컬 `python3.13`·`python3.12`를 쓴다.

## 파일

| 경로 | 내용 |
| --- | --- |
| `afledger/ledger.py` | 엔진. 설계 예제 `docs/design/final/db/ledger.py`에서 옮기고 정규화 키·앵커·D6c를 더했다 |
| `afledger/config.py` | 설정 상수와 규칙 판(한 곳). 값을 바꾸면 판을 올린다 |
| `afledger/sql/` | 공용 장부(`commons.sql`)와 프로젝트 장부(`project.sql`) |
| `afledger/normalize.py`, `afledger/vendor/` | 주소 정규화(R-1 임시안). opensource `tools/rcore/normalize.py` n1을 바이트 그대로 |
| `afledger/locate.py` | 위치 앵커와 판 사이 위치 대응(R-1 임시안 m1) |
| `afledger/budget.py` | 요청 시계 예산(D1·D11, b1) |
| `afledger/privacy.py` | 공개 꼬리표 사생활 검사(p1·p2) |
| `afledger/tokenize.py` | 서랍 토큰화(R-5 결정 t2: 영어 + 한국어 어절 줄기·음절 2-gram) |
| `afledger/studio.py`, `afledger/intake.py` | Studio 입력 모형과 접수(칸별 필요 문장 규칙 i1) |
| `afledger/adapters/http.py` | HTTP 기록·재생 |
| `afledger/adapters/reader_github.py` | 판독 어댑터: GitHub 고정판 줄 범위 |
| `afledger/adapters/runner.py` | 실행 영수증 러너(D6c) |
| `afledger/adapters/search_github.py` | 새 검색 직접 갈래(GitHub 코드 검색), 서랍 기호 풀기 |
| `programs/r1_queue.py` | R1 실행 영수증 프로그램(요청 수치는 표준 입력) |
| `run_r1.py`, `drawer_load.py` | R1 끝까지(완료 기준 2~5) |
| `measure.py` | 첫 측정과 P0 이른 신호 |
| `afledger/worker.py`, `afledger/clock.py`, `afledger/adapters/channel_raw.py` | 둘째 구현 단위: 재확인 작업자, 폴링 시계, 조건부 요청 채널 |
| `run_unit2.py` | EVAL-X1 기록 재생(단위 2 완료 기준), `out/unit2_x1.json` |
| `fixtures/` | 기록 재생 자료(`http/`, `exec/`), R1 입력과 사람이 쓴 판독·판정 계획(`r1/`), 012 자료집, opensource link-index 모음 |
| `out/` | 실제 실행 결과(`r1_live.json`)와 측정 결과 |
| `tests/` | 옮긴 설계 시험 33개, P0·어댑터·D6c·완료 기준·측정 시험 |
| `tools/snapshot_link_index.py` | opensource link-index를 읽기만 해서 모은다 |
