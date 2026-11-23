# AF-RES-104 인계

상태 **COMPLETE** · 문서 근거 비교. 검사한 결과 SHA는 `f38c0af427c66876bf411bfd0a728cfcd60013eb`다. [고정 결과와 세 필수 표](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/RESULT.md)

## 핵심 결과

- 동일 파일의 W1/W2는 각각 64과금·74,400 원문자·0이동이다. 기존 S 실재 슬롯 62/62와 코드포인트·UTF-8·SHA가 일치했다. 32패킷·128자리를 생성해 두 실행이 바이트 단위로 일치했다. [패킷](packets.jsonl) · [비용과 반복](evidence/packet-replay.json)
- W 비교 15쌍에서 W2 전용 2, 모두 미완결 13. 두 자리 모두 같은 J1에서 나온다. A/B는 14쌍에서 양쪽 완결 1, 모두 미완결 13. P3-B 때문에 W 쌍 1개와 A/B 쌍 2개를 제외했다. 예전 F→S 손실 9자리 중 2자리가 돌아왔다. [대응](pairs.csv) · [집계](metrics.json)
- 60개 최초 조건 판정, 가시 인용 77개, 선행 인용 115개를 저장했다. 과거 F 인용 81개 중 W1 통째 회수 7, W2 0이다. W2의 J1 대체 증명은 더 좁은 구현과 새 시험에 있다. W1 전용 제약 6자리와 W2 전용 시험 3자리를 별도로 표시했다. [판정](judgments.jsonl) · [인용 감사](evidence/prior-citations-audit.jsonl) · [제약 비교](evidence/feature-visibility.jsonl)
- 고유 1차 자료 46개는 최초 질문 8, 주 도구 21, 인접 10, 보조 7이다. 인수 사례의 새 주 표본은 0이다. SQLite 재귀 CTE에서는 높은 키워드 점수와 FIFO 경고 손실이 함께 발생했고 CSS Grid에서는 적용 절의 도입과 예외 위치가 떨어졌다. 일부 짧은 fixture는 W1로 충분했다. [출처](sources.jsonl) · [보조 사례](evidence/crossdomain.md)

## 계약·봉인

계획판 `ace1a06a13ea435f5cb6a3e340ad24f03f68ecae`, 기동 관측판 `cb25303b783cbd3bf82294857a7191c45a69305e`, 최신 계약 기동판 `ac7abc85e12b3a5b5f87b694d00e9511332fe272`의 관련 차이는 중앙 진행표였다. 선행 등록 인계 `80e2d746d0aa0ad7c009043e1cea3ae2e3be1311`은 별개다. 선행 관측 끝 `ab89ae6704471aaea96d175103839bc6356d389a`에서 계약 끝 `4ade4912e73723aadd08b3e0ebe90c9f862bbcf4` 사이 변경 파일은 선행 HANDOFF.md 한 개이고 사용 원장의 blob은 동일했다. 고정 실험 입력은 `b3f3694b54bb7a85dc7a21e2731841679fc6753c`다. [계약](manifest.json) · [입력 차이와 지문](evidence/prior-readback.json)

| 단계 | 원격 커밋 | 봉인 UTC | 변경 파일 |
| --- | --- | --- | --- |
| ① 선택·예산·경계 봉인 | [`0e9c2e2f2e27`](https://github.com/laadkke-arch/agentflow-open/commit/0e9c2e2f2e275411ac449dea9267cf1de409e1c4) | 2026-11-23T21:58:01Z | `SCOPE.md`, `evidence/restore-receipts.json`, `evidence/selector-unit.txt`, `manifest.json`, `protocol.json`, `reproduce.md`, `select_passages.py`, `stage_archives.py`, `test_select_passages.py` |
| ② 32패킷·반복 봉인 | [`b514e43fee90`](https://github.com/laadkke-arch/agentflow-open/commit/b514e43fee90390f1b2d599b7cbe00af28266eae) | 2026-11-23T21:59:40Z | `evidence/packet-costs.json`, `evidence/packet-replay.json`, `packets.jsonl`, `reader_input.py` |
| ③ 최초 판독만 봉인 | [`e7374c3b06a8`](https://github.com/laadkke-arch/agentflow-open/commit/e7374c3b06a8a92c63a7b255882af066103ca8d9) | 2026-11-23T22:02:32Z | `evidence/initial-read-lock.json`, `judgments.jsonl` |
| ④ 원 F 감사·매칭·반례·자가검산 | [`d3579a7f46c6`](https://github.com/laadkke-arch/agentflow-open/commit/d3579a7f46c6134dc12b48c8f2a2040590f26e5d) | 2026-11-23T22:24:39Z | `RESULT.md`, `SELF_CHECK.md`, `audit.py`, `crossdomain.py`, `evidence/access-failures.jsonl`, `evidence/audit-decisions.json`, `evidence/crossdomain-windows.json`, `evidence/crossdomain.md`, `evidence/direct-file-reads.jsonl`, `evidence/exposure.json`, `evidence/feature-visibility.jsonl`, `evidence/j1-synthetic.json`, `evidence/prior-citations-audit.jsonl`, `evidence/prior-readback.json`, `evidence/question-open-receipt.json`, `evidence/raw-display-audit.json`, `evidence/result-aware-upper-bound.json`, `evidence/sqlite-runtime.json`, `evidence/wpt-runtime.json`, `judgments.jsonl`, `metrics.json`, `pairs.csv`, `reader_input.py`, `render_tables.py`, `reproduce.md`, `sources.jsonl`, `wpt_probe.py` |
| ④의 판정·좌표 검증 보강 | [`f38c0af427c6`](https://github.com/laadkke-arch/agentflow-open/commit/f38c0af427c66876bf411bfd0a728cfcd60013eb) | 2026-11-23T22:25:25Z | `SELF_CHECK.md`, `audit.py` |

## 결과 SHA 검사 영수증

검사는 clean checkout에서 시작하고 종료했다. 정확한 명령과 UTC의 종료값은 아래와 같다.

| 명령 | 시작 → 종료 UTC | 종료 | 범위 |
| --- | --- | ---: | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-104/manifest.json --fetch` | 22:25:46.773442 → 22:25:47.129512 | 0 | 원격 계약·허용 경로·의존 SHA, outside/unmerged 0, 명시 세션 1 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 22:25:47.129600 → 22:25:55.678960 | 0 | doctor, acceptance, research-case, original-smoke 성공. check-all은 no_active_sessions, 자동 0개 |
| `python -B audit.py --cache <고정 AF-RES-100 복원 경로> --check` | 22:25:55.679020 → 22:25:55.790350 | 0 | 32패킷, 128자리, 두 축 16쌍씩, 77개 새 인용과 115개 이전 인용, 그룹별 출처 최소값 |
| `python -B render_tables.py --check` | 22:25:55.790411 → 22:25:55.835015 | 0 | 세 필수 표 16·32·32행 원장 일치 |
| `python -B -m unittest discover -s docs/workstreams/research/AF-RES-104 -p test_*.py -v` | 22:25:55.835068 → 22:25:56.239891 | 0 | 선택·경계 7개 시험 |
| `python -B crossdomain.py <보조 원문 캐시>` | 22:25:56.240160 → 22:26:07.274513 | 0 | SQLite·CSS Grid 구간 영수증과 바이트 일치 |

실행일은 2026-11-23 UTC다. `check-all`은 중앙 `docs/tasks`의 활성 manifest를 찾는다. 이 작업의 manifest는 허용 경로 아래에 있으므로 명시 검사와 자동 세션 수를 구별했다. 계약을 보존하기 위해 중앙 경로에 중복 manifest를 추가하지 않았다. 정확한 명령의 작업 위치와 인수는 [재현 절차](reproduce.md)에 있다.

GitHub 재열람 UTC는 22:26:04–22:26:29다. 고정 SHA의 Connector 범위 15개에서 Git blob이 맞았다. RESULT의 필수 표, 패킷, 최초 판정과 감사, pairs, sources, 보조 구간, SELF_CHECK, 재현 절차를 포함한 확인이다. raw GitHub에서도 RESULT, reproduce, packets, judgments, pairs, sources, crossdomain-windows 및 SELF_CHECK 8파일의 전체 바이트가 로컬 Git과 일치했다. [RESULT blob](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/RESULT.md) · [원장](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/judgments.jsonl) · [재현 명령](https://github.com/laadkke-arch/agentflow-open/blob/f38c0af427c66876bf411bfd0a728cfcd60013eb/docs/workstreams/research/AF-RES-104/reproduce.md)

## 미확인과 재개

- 사용자 원 실행 0/8, 독립 판독 미실시, 눈가림이 제한된 단일 작업자다. 같은 질문 구간을 함께 봤고 이전 사례와 원 파일이 겹친 자리 24/32가 있다. 화면 콘솔의 CR 표기가 원시 코드포인트 계량과 달랐으며 두 CR 차이 쌍을 빼도 J1 두 자리만 완결이었다. [노출](evidence/exposure.json) · [원문과 콘솔](evidence/raw-display-audit.json)
- WPT Chromium은 로컬 launch 오류와 timeout으로 assertion을 읽지 못했다. `python -B docs/workstreams/research/AF-RES-104/wpt_probe.py /tmp/af104-wpt`를 Chromium이 구동되는 환경에서 실행한다. 스크립트가 고정 WPT fixture 및 harness를 받아 네 축 기대를 검사한다. SQLite는 3.53.1 합성 5개 실행, 고정 Tcl 원 suite는 미실시다. [WPT 영수증](evidence/wpt-runtime.json) · [SQLite 영수증](evidence/sqlite-runtime.json)
- 재개 첫 행동은 결과 SHA에서 [재현 절차](reproduce.md)에 따라 AF-RES-100 고정 cache를 복구하고, `audit.py --check`로 인용 원장을 검증하는 것이다. 독립 판독자에게 `reader_input.py --case` 출력과 첫 질문만 주고 J1·J2부터 비교한다.

색인 제안 — AF-RES-104 · 동일 파일/코드포인트의 W1/W2에서 문서 완결은 W2 전용 2/15(고유 J1 1건), W1 전용 0. 예외·실행 제약이 잘리는 사례와 원문 지문은 RESULT와 source ledger를 참조.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| W2 완결 두 자리가 J1 한 건의 중복 대조이며 판독자가 공통 원장을 알고 있었다. | 동결된 32개 구간에서 방법 정보 없이 독립 판독을 배정하고 J1을 사례 단위로 합산한다. | 해당 판독에서 J1의 두 조건 증명이 재현되지 않거나 다른 요청에서 W1 전용 완결이 나오면 이득 해석을 수정한다. |
| 문자 예산은 같지만 W2에서 원 제약, 예외 및 넓은 인용이 많이 빠졌다. | SQLite 음수·FIFO와 Grid §6.6의 전체 문장, P4 title 절을 포함한 제한 보존 비교를 되풀이한다. | 더 높은 토큰 적중에서 예외 보존율도 유지되며 W1 독점 제약이 사라지면 두 구간의 적용 범위를 넓힌다. |
| P3-B Docker 고정판 공석 및 실제 작성자 실행 0/8이고 WPT 실행도 완료되지 않았다. | 완전한 P3 Dockerfile·image digest·두 필터·template·Markdown을 고정한다. 준비된 Chromium에서 `wpt_probe.py`로 네 rect assertion을 실행한다. | 같은 판·입력의 P3 PDF 실행과 CSS의 네 치수가 직접 확인되면 문서 근거를 실행 근거와 연결해 범위를 갱신한다. |
