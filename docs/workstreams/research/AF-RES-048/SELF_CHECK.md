# AF-RES-048 · 자체 점검

동일 연구자가 고정 자료와 원문 절을 다시 열어 판단을 검산했다. 외부 독립 판독은 미실시다. 두 깨끗한 워크트리에서 같은 입력을 재생하고, 별도 HTTP 실행에서 고정 게시 자산 27개를 다시 받아 SHA256을 대조했다. 판독 때 쓰는 정보와 대조 범위는 [SCOPE.md](SCOPE.md)에 해당한다. [청정 재생](evidence/clean-replay.json) · [고정 자산 재요청](evidence/pinned-refetch.jsonl)

| 질문 | 검산한 답 | 다시 연 주소·정확한 위치 | 반대 관측 또는 반증 탐색 | 판정을 뒤집을 최소 자료 |
| --- | --- | --- | --- | --- |
| Q1 · 응답·계보 | 원요구 본문 해시 5/5 일치. P48·V48·Y48 발행 HTML 결측. M은 3.11.2 공식 Git 게시물의 원 바이트를 사용. | [044 requirements.csv](https://github.com/laadkke-arch/agentflow-open/blob/6c8c025284215c7749921619cb09c89643886276/docs/workstreams/research/AF-RES-044/requirements.csv) P1–P4/V3 · [Pandoc MANUAL](https://pandoc.org/MANUAL.html) L738–745 · [Vega Overview](https://vega.github.io/vega-lite/docs/) L7–25 · [Matplotlib stable symlink](https://github.com/matplotlib/matplotlib.github.com/blob/13eef99be6bc70f601507bda8ccce2c23bad2b59/stable) | Pandoc release tar의 man pages와 Vega Markdown/Actions 산출물 목록·PyPA htmlzip을 확인했다. 웹 문서는 읽혔으나 현재 발행 HTML 해시를 검증할 입력은 얻지 못했다. | 공인 호스트 또는 공식 고정 HTML의 원응답 바이트, final URL, 판·UTC. 예전 044 바이트와 다르면 새 ID로 저장한다. |
| Q2 · 여섯 자리 | 54자리에 6개 href·6소진·42결측. V3R은 word cloud만 고정했다. P2의 원자와 reader 방향을 이관했다. | [M1 Figure options](https://matplotlib.org/3.11.2/users/explain/figure/figure_intro.html#figure-options) L769–771 · [M2 Backends 진단](https://matplotlib.org/3.11.2/users/explain/figure/backends.html#debugging-the-figure-windows-not-showing) L861–862 및 Get help가 들어 있는 최종 단락 · [044 V3 최초 요청](https://github.com/vega/vega-lite/issues/6135) 첫 문장 · [pool.csv](pool.csv) | Quick start의 목차 DOM 538–539가 본문 범위를 벗어나 있음을 찾아 원규칙대로 제외했다. 3.13.5 HTMLParser의 기록 302곳을 주 추출의 원 href·행과 대조했다. | 대상 범주와 raw href를 확인할 원응답. HEAD·프록시·DOM 차이가 있으면 후보 순서와 범주 소진을 다시 계산한다. |
| Q3 · 답안 전 표집 | Matplotlib 첫 20문서의 원순서에서 두 C 일치를 골랐다. PyPA 두 슬롯은 미확인. | [공식 고정 시작 목차](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/13eef99be6bc70f601507bda8ccce2c23bad2b59/3.11.2/users/index.html) Using Matplotlib · [목적·조건](evidence/cases.json) M1/M2 · [PyPA setup.py 안내](https://packaging.python.org/en/latest/discussions/setup-py-deprecated/) L87–110 | Quick start의 오선정과 수정 전 구조 집계를 보존했다. PyPA 원 안내의 목적을 따로 읽되 표집 정원을 채우지 않았다. | PyPA의 고정 발행 시작 HTML과 첫 20 공인 문서, URL·목차·발행판 위치. 조건에 맞는 최초 두 절에서만 빈자리를 채운다. |
| Q4 · 그룹과 세 대표 | 주표본 C는 A 대비 서로 다른 URL 2쌍을 병합했고 2/2 대표 배열이 달라졌다. 새 A 밖 대표는 0/2. | [groups.jsonl](groups.jsonl) M1/M2의 6행 · [순번 21 Constrained guide](https://matplotlib.org/3.11.2/users/explain/axes/constrainedlayout_guide.html#constrained-layout-guide) L583–590 · [40문서 구조 대조](evidence/post-seal-matplotlib-screen-40.json) | 순번 21에서 다섯째·여섯째만 병합되어 그룹 6→5, 처음 세 주소·순번 유지. 주표본에 합성 스모크 통계를 넣지 않았다. | 원풀에 동질 키가 아닌 네 번째 기능 문서가 있고 앞 두 주소가 같은 C 키여야 C가 새 대표를 노출할 수 있다. |
| Q5 · 같은 시행의 두 동작 | 고유 저장 경로 40, 방식 적용 70, 모든 동작 수 ≤2, 37완료/3부분. 원 게시 URL live는 두 시도 모두 CONNECT 단계 실패. | [T011 기록](trials.csv#L12) M1-2 origin L770, compressed href L1004, Figure anchor L613 · [두 live 시도](evidence/live-trials.jsonl) T001/T021 · [044 §5](https://github.com/laadkke-arch/agentflow-open/blob/6c8c025284215c7749921619cb09c89643886276/docs/workstreams/research/AF-RES-044/SCOPE.md#5-판독과-실제-2동작-q5) | `#id11`·`#id12`는 figure intro의 실제 TOC 앵커로 확인했다. PNG 도착도 별도로 검증했다. 두 자료에는 필수조건 코딩을 부여하지 않았다. GitHub issues GET 200도 고정 창을 입증하지 못했다. | 원 게시 URL에서 같은 최종 응답·fragment를 확인할 GET 또는 브라우저 영수증. live 시행으로 새 실행 ID에 남긴다. |
| Q6 · 살린 것과 가린 것 | 관측 M1의 원풀 ID 하나를 모두 회수했고 M2는 완결 분모 0. T011에서 A만 원풀 밖 TightLayoutEngine에 도달한다. | [Figure API](https://matplotlib.org/3.11.2/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure) layout 파라미터 · [gold.csv](gold.csv) E01–E19 · [v3.11.2 Figure 구현](https://github.com/matplotlib/matplotlib/blob/v3.11.2/lib/matplotlib/figure.py#L2727-L2734) · [P2 writer diff L1077–1089](https://github.com/jgm/pandoc/commit/28e01fac74c88a777dc69c693f1296e46e1d738c) | 생성자에서 constrained도 입증하는 것을 재판독해 T011의 ID 수를 정정했다. 다른 NDL/교통 사례를 원풀에 추가하지 않았다. 372절 후속 탐색에서 새 대표 여섯을 확인했으나 다른 상류 회복 근거는 없었다. | 원풀 안의 Tight 안내에 생성자 인자까지 있으면 분모가 늘어난다. M2 조건을 충족할 정확한 backend 조회·최소 재현 절이 풀에 있으면 분모와 A/C 비교가 달라진다. |
| Q7 · 사용·발행·표시 조건 | 같은 책 이름·저자 권위에는 한 서지가 충분. 판·번역·삽화에는 개별 서지. 시간표 한 PDF는 두 방향을 담지만 방향·승강장 계약에는 실제 행이 필요하다. | [NDL 1990, 紙 L537–672](https://ndlsearch.ndl.go.jp/books/R100000002-I000002031480) · [NDL 1987, 紙 L480–606](https://ndlsearch.ndl.go.jp/books/R100000002-I000001868920) · [MTA p2/p7](https://www.mta.info/schedules/subway/1-train) · [GTFS stops.txt 사본 53–55행](https://github.com/itsashishupadhyay/NYC_MTA_Timetable/blob/f11ef56ff9438eacef0ff301f35a2aa0dcb15de3/info/stops.txt#L53-L55) | 도서관 두 원 레코드를 직접 재열람했다. MTA 정규 ZIP의 동일 여부는 미확인이다. 숫자 판을 URL에서 읽지 못한다고 가정하면 C는 안전하게 개별 슬롯으로 돌아간다. | MTA 정규 ZIP의 발행판과 stop_times/trips 조인, 혹은 실제 한 화면에서 사람의 과업별 열기·확신을 관측할 사용자 연구가 필요하다. |

재판독은 2026-11-22 22:37:45–46 UTC의 웹 원문 재열람과, 추가로 고정 Matplotlib 바이트의 절 재판독·SHA 검증을 사용했다. 원래 섹션의 키·후보·실행 계획에 영향을 주지 않는 의미 코딩 정정은 [재판독 정정 기록](evidence/gold-recheck.json)에 있다. 공개 자료 33건 배당과 동일 저작 중복 제외를 [sources.jsonl](sources.jsonl)의 실제 행에서 다시 셌다.

두 오프라인 실행의 stdout 해시와 원순서·대표·경로·집계 해시가 일치한다. 하나의 깨끗한 실행에서 확보한 27개 고정 자산의 바이트 해시도 대조했다. 전체 문서 사이트의 이용자 행동, AF-RES-044의 1,927시행, 과거 040 비교는 이 검산 범위 밖이다. [두 청정 환경 출력](evidence/clean-replay.json) · [파서 대조 영수증](evidence/parser-sensitivity.json)

## 재현

저장소 루트에서 원장 기반 재생은 파일을 변경하지 않는다. 신규 요청 또는 해시 확인은 새 외부 작업 폴더에 기록한다.

```bash
python -I -B docs/workstreams/research/AF-RES-048/replay.py
python -I -B docs/workstreams/research/AF-RES-048/replay.py --smoke
python -B docs/workstreams/research/AF-RES-048/evidence/acquire.py /tmp/af-res-048-verified-input
python -I -B docs/workstreams/research/AF-RES-048/replay.py --raw-dir /tmp/af-res-048-verified-input
python -I -B docs/workstreams/research/AF-RES-048/evidence/check_anchors.py /tmp/af-res-048-verified-input
python -B -m workbench.session check docs/workstreams/research/AF-RES-048/manifest.json --fetch
```
