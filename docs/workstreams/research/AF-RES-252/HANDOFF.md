# AF-RES-252 인계 · PARTIAL

## 상태와 고정점

- 배정 AF-RES-252 #1, Codex Cloud, `laadkke-arch/agentflow-open`, `work/research-af-res-252`. 착수 통합 `d1353701530ffd4c68587276c15d988d2cc92972`. 의존 AF-RES-231 `e55fd8c9df7fdd45259346aeb8884a7d3586594b`, 중앙 DONE/자체 PARTIAL. 231의 예정 4사건·8경로와 이전 질의가 비어 있었다. 이번 제목식 비교는 새 조건이다. [착수 범위](SCOPE.md) · [231 인계](https://github.com/laadkke-arch/agentflow-open/blob/e55fd8c9df7fdd45259346aeb8884a7d3586594b/docs/workstreams/research/AF-RES-231/HANDOFF.md)
- **고정 결과 SHA `51fc0ee7663a7b22245372e4c31f74c51aa00dc6`.** 이 인계 파일은 검사한 결과판 뒤의 단독 커밋이다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/51fc0ee7663a7b22245372e4c31f74c51aa00dc6/docs/workstreams/research/AF-RES-252/RESULT.md)
- **실제 장애는 Cloud HTTP CONNECT 403이다.** 두 API 호스트가 현재 Cloud의 제한된 HTTP 허용 목록에 없다. 정규 수집 GET 4건에서 curl exit 56, 원제공자 HTTP 000, 본문 미수신을 기록했다. Stack Exchange 필터, AND 모집 첫 페이지 및 Crossref 두 cursor 응답의 수집이 막혔다. 웹 열람 도구의 정확한 API URL도 본문을 받지 못했다. [live 실행 기록](receipts/live-execution.json) · [F01](receipts/filter-frame.1.meta.json) · [F02](receipts/frame-default-diagnostic.1.meta.json) · [F03](receipts/crossref-shannon-p1.1.meta.json) · [F04](receipts/crossref-kuhn-1900-p1.1.meta.json)
- 실제 모집·기계 후보·정상 공석 수 미확인. 첫 120자리를 정규화할 frame, 12 한도 후보 질의 봉인, 두 도착 배열 및 선택 답, 실제 판독 파일을 만들 수 없었다. 254 목표 4사건 미배정·8경로 미실시. 보정 #138641의 현재 HTML 1건, 별도 DBA 보조 10건을 열었다. Crossref 0/2 관측·2 결측. 자료 원장은 75행, 산입 원자료 41건, 계보 20개다. [결과](RESULT.md) · [원장](sources.jsonl) · [자체 점검](SELF_CHECK.md)

## 검증한 범위

| 진입점 | 실행 범위와 결과 |
|---|---|
| `workbench.session start ... --fetch` | exit 0, 계약 v2, 허용 경로 1개 및 231 의존 SHA를 고정. `session.json`에 stdout과 시작 핀을 보존 |
| `python -B collect.py frame / probe-frame / crossref / audit` | 각 exit 2 / 2 / 2 / 0. 로그는 2026-11-25 UTC와 Python·curl·Git 정보, 환경 지문 및 실제 실행 수집기 지문을 포함한다. 해당 수집기는 커밋 `cd8cb848b4f74053faf2ad0c308e51fbeb245881`에서 다시 얻을 수 있다 |
| 별도 폴더 `collect.py audit / replay / replay-crossref` 및 `test_replay.py` | 각 exit 0 / 2 / 2 / 0. 실패 영수증 네 개를 다시 읽었고 두 replay의 예상 중단이 재현됐다. 합성 검사 12개 통과. 실제 공개 정렬·서지 결과는 미확인 |
| `python -m workbench.session check docs/workstreams/research/AF-RES-252/session.json --fetch` | 고정 결과 SHA에서 exit 0, remote_checked. 2026-11-25 00:18:36 UTC의 통합 SHA `78b64ce8b84ef1d37c2a7100dc376c65dd97e74a`, 계약 SHA-256 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`, 의존 변경·범위 이탈·미해결 병합 0 |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 고정 결과 SHA의 clean checkout, Python 3.12.14, 00:18:36–00:18:44 UTC, exit 0. doctor·acceptance(공통 55, lab 7·9, demo·export·Git 복원)·reference-audit discovery·original smoke 실행. 공통 check-all은 `no_active_sessions`. 사용자 소유 경로의 manifest는 위 개별 검사에서 검증 |
| 고정 결과판 실제 재조회 | GitHub로 16개 전부 다시 열고 checkout 원바이트를 파싱했다. 결과 표 열 6·5·4 및 행 1(결측 표시)·4·3, Q1–Q7과 원근거 링크, 원장 75행, 영수증, manifest를 대조했다. 실제 판독 파일 3개는 모두 부재, 수·SHA null |

별도 폴더 실행의 실제 입력 해시와 stdout/stderr는 [replay-execution.json](receipts/replay-execution.json)에 있다. 고정 결과 SHA의 개별 계약 stdout SHA-256은 `27bd8c099328de2e8b4dc4774bcda09cc0baaa117543e74d0d6b36c60c36fb02`, 공통 stdout SHA-256은 `a5dab5d87a57d432ca928d8cbc11873264818ea2509d7fc234114b84d01a7a34`다. 두 stderr는 0바이트였다. 공통 검사보다 별도로 12개 합성 시험을 고정 SHA에서 재실행했다. 자체 점검 시행, 별도 독립 검토 미실시다.

## 재개 첫 행동과 254 입력

두 공개 호스트에 연결할 수 있는 승인된 실행 환경에서 지정 브랜치의 결과를 읽은 뒤 첫 단계로 필터·프레임을 요청한다. 새 계정 또는 API 키 없이 현재 익명 제한으로 재개한다. 필터 성공 영수증과 실제 included_fields를 먼저 확인한다.

```bash
git clone --single-branch --branch work/research-af-res-252 https://github.com/laadkke-arch/agentflow-open.git agentflow-af252-restart
cd agentflow-af252-restart
git rev-parse HEAD
P=docs/workstreams/research/AF-RES-252
python -B "$P/collect.py" frame --retry-failed
```

정상 입력은 v2.3 `/filters/create`의 base=none, 명시 필드와 `/questions`의 site=dba, tagged=`postgresql;greatest-n-per-group`, epoch 1325376000–1735689599, creation asc, pagesize=100이다. F01 영수증 이후 정상 frame이 확보되면 `origins --retry-failed`로 원문을 모아 frame·queries·영수증을 커밋한다. 그 SHA로 `routes --seal`을 실행한다. Crossref의 두 서지·일자·cursor 및 재실행 명령, #138641의 별도 봉인·실행은 [replay.md](replay.md)에 있다.

**254는 [packet-manifest.json](packet-manifest.json)이 ready가 된 판에서만 개방한다.** manifest → `reader/origins.jsonl`에서 최초 적격 4건과 요구를 고정 → `reader/destinations.jsonl`의 익명 질문·답 판독 → `mapping.json`으로 대응 확인 순서다. 현재 manifest 상태는 blocked이고 자체 SHA-256은 `d41899ceaebd7c49a6f7ad3de42d05d57b8411eb6c9e6a7839f5024ea52cb6d2`다. 실제 모집, 원응답, A/B 적합도 입력은 대기 상태다.

## 커밋과 색인 제안

- ① `980ab5c` 사전 범위·예측·session, ② `cd8cb84` 원자료·영수증·수집기, ③ `5e41a1b` 두 필수 표·실측과 차단, ④ `3df4bb9` 반례·재생 및 `4889e83` 정상 생략 분류 정정, ⑤ `a9d16c6` RESULT와 `51fc0ee` SELF_CHECK, ⑥ 이 HANDOFF 단독.
- 색인 제안은 **AF-RES-252 PARTIAL · result `51fc0ee7663a7b22245372e4c31f74c51aa00dc6` · 원응답 4시도 미수신 · 합성 검산 12 통과 · 254 blocked · 다음은 승인된 환경의 frame 재수집**이다. 진행표 갱신은 통합 담당이 맡는다.
