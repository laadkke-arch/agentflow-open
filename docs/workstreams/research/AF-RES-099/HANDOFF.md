# AF-RES-099 · 최종 인계

**연구 COMPLETE · REVIEW_READY.** 원 TeX 1개로 A/B/C를 각각 2회 실행했다. A는 그림 0/2이고 본문 2/2였다. B는 두 HTML에서 4/4 상태, 8/8 방향 전이·라벨, 검색 가능한 문장 2/2를 보존했다. C 두 SVG는 같은 그림과 페이지 글자 모양을 보존했다. C+로 열면 그림은 보이나 본문 DOM 0/2였고, 외부 SVG가 없는 HTML은 404였다. 의미 판정 반복 3/3쌍, 주 산출물 바이트 일치 3/3쌍이다. [결과판의 세 표](RESULT.md) · [요소 대조](evidence/ELEMENTS.md) · [원장](runs.jsonl)

## 브랜치와 저장판

- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-099`, 허용 경로 `docs/workstreams/research/AF-RES-099/`.
- 시작 기준 `01177554d0fbd33a914ea9c982c348d442d1358d`. 계획 기준 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`와의 변경은 중앙 진행표다. 시작·검사 시 두 의존 브랜치의 원격 헤드는 지정 095 `b7f6db6f3e0dbbaa27ea3fbfb70cd6a629e23455`와 096 `fce8d0ded93fe1f13f2c4978ed273c1ceef32934`에 일치했다. 실제 연구 입력은 각 결과판 `55eb703075163a84b38fdc7eb577f66207e9980e`, `1d399f630930d2763459e16509c5224b0cded9a0`에서 읽었고 인계판과 사용 blob이 동일했다. [입력·고정 파일](inputs.json) · [시작 계약](manifest.json)

| 묶음 | 푸시 뒤 확인한 SHA | 변경 파일과 목적 |
| --- | --- | --- |
| ① | [cfdf8d325d4e3c847485c7e31dfefe0f149a68f6](https://github.com/laadkke-arch/agentflow-open/commit/cfdf8d325d4e3c847485c7e31dfefe0f149a68f6) | 4개. 채점표·입력 해시·계약·원 질문 봉인 |
| ② | [0cae89305ea1d7d3bbcdfadf0f368293029211eb](https://github.com/laadkke-arch/agentflow-open/commit/0cae89305ea1d7d3bbcdfadf0f368293029211eb) | 48개. 환경·포맷·첫 실패·양성 음성 교정·실행기 |
| ③ | [7a7c0a3b8cf39cf543e70b6f3da59a3bbd5e1fb3](https://github.com/laadkke-arch/agentflow-open/commit/7a7c0a3b8cf39cf543e70b6f3da59a3bbd5e1fb3) | 99개. 6자리 AST, PDF, HTML/SVG, 화면·대조 |
| **④ 결과** | [01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7](https://github.com/laadkke-arch/agentflow-open/commit/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7) | 41개. 필수 표·출처·검산·재현·교차 분야와 반례 |
| 마지막 인계 | 이 파일의 단독 커밋 | ④ 검사와 GitHub 원본 읽기 뒤 작성 |

[①–③ 전체 변경 파일·SHA](evidence/commit-files.json)와 ④ GitHub 커밋의 파일 목록을 기준으로 비교할 수 있다. 작업 브랜치의 결과 변경 189개가 모두 소유 경로에 있다.

## 실제 검증과 GitHub 재열람

대상은 깨끗한 checkout의 결과 `01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7`이다. 2026-11-23 20:02:53–20:03:02 UTC에 실행했고 종료 시에도 동일 SHA 및 clean이었다.

| 검사 | 종료값 및 범위 | 실행 stdout SHA-256 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-099/manifest.json --fetch` | **0**, remote_checked. 검사기의 자체 manifest 제외 변경 188개, 범위 밖 0, 오류 0. 통합 원격 SHA는 검사 때 `1edec76ded75209eb35a10046239ad7c9f72b30f`였다. 시작판 이후 변경 파일은 중앙 진행표 하나, 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`로 일치 | `0cb68abc252a5c845e960a7b7e34daf1e8e5273e1ca313c5ac6aa7489140aa61` |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | **0**, doctor·acceptance·research-case·original-smoke 각 0. 내부 check-all은 0이나 `not-executed/no_active_sessions`, count 0, freshness not_checked. 이 작업의 개별 검사는 위 행에서 실행 | `cc788620c2bbb72d2d67f836afe1ccb35dd2e465a9054120d6756fbd66de7b09` |
| `python -B docs/workstreams/research/AF-RES-099/audit.py` | **0**, 행렬 6자리·보조 원장 전체 20행, 보존된 지문 126개, 39/60 자료 산입, 디코딩·반복 지문·PDF 상대 좌표 검산 | `c8f70b6b96a1cd106bf76a7621bbf98cfaf3d5c3ec386f0973ce4fdeb1cdfd43` |

GitHub의 ④ raw 주소에서 20:02:57 UTC에 30개 파일을 받아 **30/30 바이트 일치**를 확인했다. RESULT 표의 3/6/4행과 마지막 3행, RUNS 주 6자리, A AST·HTML 및 B HTML payload·디코딩 SVG 지문, C PDF·SVG, 확대 판독 이미지, 재현·자가검토·출처 원장을 다시 열었다. Git blob은 RESULT `861c97c36c776a5df10f82b1126983f6b7a2bc2a`, runs `2f22f2d1940e7ebcd4249ddfae5be031e286fd9d`, reproduce `fc905a117deda820d2662add5a73fad386922e2a`다. [GitHub 결과판](https://github.com/laadkke-arch/agentflow-open/tree/01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7/docs/workstreams/research/AF-RES-099)

## 실행 한계와 재개 첫 행동

최초 B에서 pdflatex 0 다음 pdf2svg 실행 파일 부재로 Pandoc 83이 발생했다. 교정 후 두 번 모두 통과했고, 빈 format의 독립 대조는 pdflatex 1/Pandoc 83이었다. B는 전역 색 파생 입력에서 실패했다. Chromium file URL 첫 시도는 관리 정책으로 차단됐고 최종 판독은 새 오프라인 Chromium 컨텍스트·로컬 파일 라우팅에서 수행했다. 질문자 당시 환경·답변자 PDF·답 첨부 화면의 이번 직접 접근·타인 독립 검토는 미확인 또는 미실시다. Graphviz 전용 하네스·WPT 하네스는 미실시였고 nbconvert 상류 선택 시험 3건은 통과했다. [교정](evidence/calibration/README.md) · [다른 분야](evidence/cross-domain/README.md) · [검토](SELF_CHECK.md)

재개 시 첫 행동은 결과 SHA의 [요소별 대조](evidence/ELEMENTS.md)와 [B1 HTML](evidence/matrix/B1/example.html)을 함께 열어 사용자가 필요한 것이 검색 가능한 HTML인지 페이지 외관인지 결정하는 것이다. 같은 원문을 재실행하려면 [고정 입력 준비와 명령](reproduce.md)의 세 단계로 TeX·봉인 Lua·Pandoc을 준비하고 `run.py matrix`를 새 경로로 실행한다. 다음 입력이 전역 정의를 쓸 때는 먼저 `run.py counterexample`로 비교 기준을 재현한다.

**색인 제안** — AF-RES-099 · COMPLETE · Pandoc 3.6 동일 TeX 6/6 실행, A 그림 0/2, B HTML 2/2·문장 2/2, C SVG 2/2·C+ 본문 0/2 · 1차 자료 39 · 결과 01c7d0a40a20a35f98c11eb12c2ad28423cbdbd7 · [RESULT](RESULT.md)

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| A의 연구 SHA와 질문자의 당시 main·환경 사이에 간격이 있다 | 질문 당시 diagram SHA·Pandoc 버전·원 생성 HTML을 확보해 같은 TeX와 원 명령 실행 | 당시 판의 실제 콜백이 TikZ를 받고 읽히는 원 그림 4/4·8/8을 표시 |
| B 성공은 봉인 preamble의 원 단일 그림에 한정된다 | `B-CUSTOM-PREAMBLE` 입력과 다중 그림·서로 다른 전역 스타일을 가진 TeX를 같은 B로 실행 | 봉인 필터 본문과 입력 문맥 전달 방식을 유지한 채 사용자 스타일·방향·라벨 모두 표시 |
| C의 SVG→HTML 그림 표시와 검색 가능한 본문 사이에 간격이 있다 | 답변자가 실제로 사용한 통합 HTML 또는 C+ 두 방식에 별도 본문 태그를 붙인 입력에서 DOM·자원 시험 | 한 파일에서 원 그림과 검색 가능한 두 문장이 함께 보이며 네트워크 없이 로드 |
