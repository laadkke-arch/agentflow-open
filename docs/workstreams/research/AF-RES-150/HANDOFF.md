# AF-RES-150#1 인계

**REVIEW_READY.** 자연 사건 12, 안정 대조 4, 산입 원전 49로 수량 기준을 충족했다. 초기·사후 네 조회와 오류 복구를 별도의 로컬 저장소에서 실행했다. 직접 열지 못한 원문과 그로 인해 답하지 못한 역사 질문은 아래와 [자체 점검](SELF_CHECK.md)에 남겼다.

## 인계 대상

| 항목 | 값과 근거 |
| --- | --- |
| 저장소 / 작업 브랜치 / 변경 경로 | `laadkke-arch/agentflow-open` / `work/research-af-res-150` / `docs/workstreams/research/AF-RES-150/` |
| 실제 시작 통합 SHA와 계획판 | 최신에서 새 브랜치 `35ca756d1b18af5d89c3eb53659365c09f1f88e3`. 계획 기준은 `ecdf28ee7a4f2004aeeffc8b9c17fff5bc8a0e19`. [초기 입력과 확인 경로](SCOPE.md) |
| 고정 선행 인계 | [003 / b13db393](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/HANDOFF.md) · [023 / a9178ca](https://github.com/laadkke-arch/agentflow-open/blob/a9178ca95979564fd8801559d90d15db4ddac91b/docs/workstreams/research/AF-RES-023/HANDOFF.md) |
| 결과와 검사 SHA | **`e4086f5b8f58b1b8494ed6474547e34cd7bff567`**에서 결과, 자체 점검과 고정 입력을 읽었다. [RESULT 고정판](https://github.com/laadkke-arch/agentflow-open/blob/e4086f5b8f58b1b8494ed6474547e34cd7bff567/docs/workstreams/research/AF-RES-150/RESULT.md) · [SELF_CHECK 고정판](https://github.com/laadkke-arch/agentflow-open/blob/e4086f5b8f58b1b8494ed6474547e34cd7bff567/docs/workstreams/research/AF-RES-150/SELF_CHECK.md) |
| 마지막 단독 인계 SHA | 이 파일의 마지막 커밋이다. 아래 `git log`로 정확한 값을 확인한다. |
| 환경 | GitHub에서 입력과 커밋을 직접 읽었다. 웹 원문은 페이지 본문과 고정판을 확인했다. 로컬 재생은 Linux, Python 3.12.14, SQLite 3.53.1, Git 2.56.1에서 실행했다. [REPLAY](REPLAY.md) |

| 묶음 | 근거 커밋 | 같은 SHA에서 다시 읽은 대표 파일 |
| --- | --- | --- |
| ① 탐색·비교 기준 | `35c6e07f9acae6883990ec231fae7bd311ef468b` | SCOPE.md |
| ② 모집·직접 원자료·기대 답 | `b08e46d11fddc578fc6f3a20336cc2014302188c` | cases.jsonl, sources.jsonl |
| ② 보강 조회 사전 기록 | `9ef9304634c9e250d56cb2f7cce47e4764c2dcd8` | SCOPE.md |
| ③ 주 관측 | `856360036cd0ac0307c61660c29b80a442cd6a67` | replay.py, answers.csv |
| ④ 반례·검산 | `656b0a9e42aaf7ac1c55d54f2a5a1e613afd67af` | REPLAY.md |
| ⑤ 결과표와 자체 점검 | `e4086f5b8f58b1b8494ed6474547e34cd7bff567` | RESULT.md, SELF_CHECK.md |

## 넘길 판단과 분모

- **안정된 고정 절에는 주소 한 개가 충분한 경우가 있었다.** 4개 대조의 두 시점·네 조회 32/32를 보존했다. 별칭 근거 조회 4/4는 소실됐다. 같은 주소와 같은 목적의 새 인용을 처리하는 데 필요한 최소량과 두 기록의 동일성을 증명할 최소량이 달랐다.
- **키의 범위가 답의 범위를 따라야 한다.** 같은 repo ID와 PR을 증명한 React 두 주소는 중복이다. 공통 작품 키를 쓴 B는 다른 Frankenstein·Darwin 판을 포함해 6/16쌍을 오병합했다. 주소별 A는 실제 동치 6쌍을 오분리했다. 방향과 범위를 쓴 C는 15/16쌍의 값과 근거를 맞췄고, Atom/Pulsar의 공식 보관 근거 하나를 쌍의 답에 돌려주지 못했다. [결과 표 1–3](RESULT.md).
- **정정 부분을 특정하면 다른 인용을 유지할 수 있다.** C의 두 구성 오류에서 L/P 4/4가 취소 뒤 원결과로 돌아왔다. 공개일을 없앤 C는 N01의 과거 조회 2개에 사후 발표를 섞었다. 중복·역순·실패는 별도 시나리오다. 정상 A/B/C의 성공 쓰기는 38/52/60회, 논리 바이트는 10,156/13,987/16,652다. [답 원장](answers.csv) · [비용 원장](costs.csv).

원장은 75행이며 직접 확인 71행, 고유 원전 49저작이다. 하한 기준별 산입은 **당사자 변경 12, 고정판 18+독립 소비자·편집자 인용 5, 다른 분야 사건 9, 운영 규약/구현 5**다. 보수적 발행 주체는 23곳이다. 자연 12건은 소프트웨어 7와 비소프트웨어 5이며, 안정 대조 4와 겹치지 않는다. [sources.jsonl](sources.jsonl) · [cases.jsonl](cases.jsonl).

시간순 원자료의 변화를 관찰했고 관계 범위와 기대 답은 작업자가 판독했다. 오류 주입과 중단은 구성했고 결과 행 수·바이트·재생은 실측했다. 본 비교는 384개 주 조회와 P 48쌍 판정이다. 별도 감사, 입력 중복, 순서, 재실행과 제거 대조를 포함한 전체 답은 5,336행이다. N11의 역사 근거가 빈 방식당 6개는 주 조회의 미확인으로 유지했다.

## 재개 첫 행동

**Open Library 42049802와 OL14863262W 24/26 원 revision을 확보해 동일 거래인지 먼저 확인한다.** S08a/b의 직접 읽은 편집자 보고는 작품 필드 손실과 일반 undo 동작을 설명한다. 두 원장 URL은 웹 열람과 대체 경로에서 본문을 얻지 못했다. 목표 입력은 두 revision의 author, 제목, 표지, 설명, 주제, 때와 편집자다. 원장이 연결되면 N08에서 보류한 L/A와 관계만 취소할 수 있는 최소 필드를 다시 판정한다. [공개 보고](https://github.com/internetarchive/openlibrary/issues/6371) · [출처 S08c/d](sources.jsonl).

공개 원장에 접근되는 작업공간에서 다음 정확한 URL을 읽는다. 현 세션에서 이 두 HTML을 수신하지 못했고 아래 파일 저장 명령의 성공도 미확인이다. 서버 응답과 본문을 모두 확인하고, 프로젝트 밖에는 원본을 옮기지 않는다.

```sh
AF150_REVISIONS=$(mktemp -d /tmp/af150-ol-revisions-XXXXXX)
curl --fail --location --max-time 20 -o "$AF150_REVISIONS/merge-42049802.html" \
  'https://openlibrary.org/recentchanges/2010/11/26/merge-authors/42049802?page=1'
curl --fail --location --max-time 20 -o "$AF150_REVISIONS/work-24-26.html" \
  'https://openlibrary.org/works/OL14863262W/Tales_of_Soldiers_and_Civilians_18_stories?_compare=Compare&b=26&a=24&m=diff'
```

다음 직접 확인 후보는 [Ostrom 1970 S11c](https://www.science.org/doi/10.1126/science.170.3957.537)와 [NEJM notice S12c](https://www.nejm.org/doi/pdf/10.1056/NEJMc1806491)다. 각각 웹 발행처가 접근을 거부했다. 현재 결과는 후대의 물건 재동정과 원 초록·정정 서지 및 재출판의 내용까지를 다룬다. 독립 판독, 덮어쓰기 경쟁, 실제 구형 runtime과 배포 호환, 생산 서비스 부하 시험은 미실시다. Compose의 재개용 입력과 명령은 [REPLAY](REPLAY.md#좁은-기능-대조)에 있다.

## 검사와 인계 재확인

- 결과 SHA의 소유 경로를 `git archive`로 빈 폴더에 추출해 다시 재생했다. 종료 0, 저장된 두 CSV와 `cmp` 일치, 원전과 사례·반증 행 정합 점검 종료 0이다. 입력 및 출력의 SHA-256은 [REPLAY](REPLAY.md#입력과-출력-지문)에 있다.
- `python -m workbench.session check docs/workstreams/research/AF-RES-150/manifest.json --fetch`를 결과 SHA에서 실행했고 `passed / remote_checked / exit 0`이었다. 그때의 통합판은 `ff5a037d4926e5c3ce6032bfa22c75b62f3c6aa8`이다. 이 통합판은 계약 확인에 쓰였고 시험 입력은 앞선 시작판과 원장 고정에 맞췄다.
- `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean`는 분리한 Git 작업트리의 phase 4 `656b0a9e42aaf7ac1c55d54f2a5a1e613afd67af`에서 종료 0이었다. 공통 합격 기록의 전체 세션 일괄 조회는 `no_active_sessions`였으며 이 작업의 manifest에는 위 개별 검사 결과를 쓴다. 공통 검사는 로컬 재생을 대신하지 않는다.

후속 담당은 지정 브랜치를 checkout하고 저장소 루트에서 확인한다.

```sh
git fetch origin refs/heads/work/research-af-res-150:refs/remotes/origin/work/research-af-res-150
git log -1 --format=%H refs/remotes/origin/work/research-af-res-150 -- docs/workstreams/research/AF-RES-150/HANDOFF.md
git diff-tree --no-commit-id --name-only -r refs/remotes/origin/work/research-af-res-150
git diff --check 35ca756d1b18af5d89c3eb53659365c09f1f88e3 refs/remotes/origin/work/research-af-res-150
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-150/manifest.json --fetch
```

색인에 반영한다면 제목은 **AF-RES-150 · 주소·판·부분 계보의 시간순 복구**다. 주 결과는 [RESULT](RESULT.md), 재생은 [REPLAY](REPLAY.md)이며 고정 선행은 003/023이다. 연구 결과의 채택 조건은 조회 목적, 원 근거의 역할, 관계 범위와 비용이다.
