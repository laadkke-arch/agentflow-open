# AF-RES-086 HANDOFF

## 연구 판정: PARTIAL

핵심 질문의 역사 공석을 남긴 채 조사·대조·자가검산·원격 재열람을 완료했다. **P3의 주 관측창 두 경로 공동 제공은 0/1 확인·1 미확인이고, R1은 남은 inactive 상태를 읽었으나 그 전의 성공/실패 순서와 당시 root·leaf 응답을 복원하지 못했다.** 자료 최소량이나 검사 통과를 REVIEW_READY로 바꾸지 않는다.

- 직접 원문 원장201행, 적격 URL·판126쌍. 동일 바이트3쌍을 더 세지 않은 최소123자료, 같은 저작·사건을 묶은25계보. 정책4계보를 빼도21실례계보로 최소량을 충족한다.
- 원 약속 두 조건의 분모는 **1/6** 유지, 이번 고정4자리는1/4. 기본9경로의 주창 판 식별0/9·미확인9, 현재HTTP2008/9·목표판4/9다. P1/R1/R2 공동 조건은0/0 산출 불가다.
- 원 로그까지 분석한 선택 RTD 생성4/4성공과 독립 게시 거래0/4미확인, Pages success 직접관측0/2미확인을 구별한다. 현재 inactive2/2를 성공 또는 실패2건으로 세지 않는다.
- 동일 목적의 사전·사후 링크 후보는4/4비교 가능, 변경1/4(R1 유보→생성 HTML 원문), 유지3/4. R2의 현재 바이트2/2일치는 확인했으나 당시 제공은 여전히 미확인이다.
- 최초 사건은 네 저장소별 생성순 첫3개를 합친 층화12개다. 강한 사슬0/12, 추가4개0/4. 전역 최초12나 전체 사건 부재를 주장하지 않는다. 타 분야는2기관·3저작쌍·6판 기록이다.

## 고정 기준과 산출물

저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-086`, 유일 쓰기 범위 `docs/workstreams/research/AF-RES-086/`.

| 구분 | 고정 SHA·기록 |
|---|---|
| 계획 기준 | `184137d2f257f5d1a7ef584e0f3a6b35f3d280cd` |
| 실제 시작 통합판 | `9dcae48a47b05d7ba2a1320444be28f5d0fcd739` |
| 유일 선행 | `work/research-af-res-082@1f8bf039ad4f9a38b99764a11f72b515facef39c` |
| 묶음1: 범위·manifest | `ed38f7622cacbf329467617296c2a435a7961afe` |
| 묶음2: 현재 정보 사전 권고 | `586b33488f6338ee8309a671d270656d837df636` |
| 묶음3: 역사·사건·보존 원장 | `a8852cc15640429f9faf5ee487f83c0fd0d8dfdc` |
| 묶음4a: 고정 결과·카드·비교·자가검산 | **`6b7cb06061742f9ecd42efac3788b4ce6ac6cc7b`** |
| 묶음4b: 고정 결과 검사·원격 재열람 영수증 | **`e6a79c3ac05b84ea1c7db313233df1717cade756`** |
| 묶음5 | 이 HANDOFF만 마지막 단독 커밋. 부모는 묶음4b. |

계획 SHA의 dot-control에는 자기 행이 없었고 시작판에는 RUNNING·의존082·본 과제 brief가 있었다. 두 판의 원문·blob 영수증을 `evidence/startup-contract.json`에 보존했다. 선행 HANDOFF, requirements.csv, deployments.jsonl, cards.md와 Python/R 관련 행을 고정 선행 SHA에서 읽었다. 다른 같은 회차 결과는 사용하지 않았다. `dot-control.json`, 중앙 색인, main은 변경하지 않았다.

주요 결과 파일은 [RESULT.md](RESULT.md), [cards.md](cards.md), [comparison.json](comparison.json), [SELF_CHECK.md](SELF_CHECK.md)다. 계약·사전 기준은 [manifest.json](manifest.json)·[SCOPE.md](SCOPE.md), 약속과 가정은 [claims.csv](claims.csv), 출판 단계는 [routes.jsonl](routes.jsonl), 사건 표본은 [incidents.csv](incidents.csv), 원자료와 한계는 [sources.jsonl](sources.jsonl)에 있다. 조회 영수증·짧은 추출·원 상태 배열·파일 manifest는 각 `streams/*/evidence/`에 있으며, 네 독립 감사는 `streams/review/`에 있다.

## 지금 반환할 네 답

| 자리 | 반환 링크·볼 절 | 주장 가능한 범위와 유보 |
|---|---|---|
| P3 | [v3.3.0 enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable), [1.x의 Python 표](https://cibuildwheel.pypa.io/en/1.x/) | 현재 내용 확인. 보조 stable/options2025-11-14T02:26:28Z와1.x11:28:00Z는 개별 확인이다. 주창 공동 제공·run별 파일 귀속은 유보. |
| P1 | 7.0.1 문서 링크는 유보. [빌드30720077](https://readthedocs.org/api/v3/projects/bandersnatch/builds/30720077/)은 생성 근거로만 반환. | 현재latest8.2.0·named404. 같은 SHA의 latest HTML 생성 성공은 확인하지만7.0.1 당시 응답은 없음. |
| R1 | [고정 archive_read HTML 원문](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html), Usage·Arguments·Examples | 1.1.12 생성물 원문/다운로드이며 렌더링된 옛 사이트가 아니다. 현재root1.1.14. 당시 게시·제공은 유보. |
| R2 | [현재2.3.1 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html), init_knitr_engine·Caching·Using SVG files | 현재 두 HTML은 선택 생성물과 바이트 동일. 2024년 제공·무중단 유지·전체assets실행은 유보. 고정 인용에는 cards의 생성 HTML 원문 링크를 함께 제공. |

## 실제 검사와 고정 원격 재열람

| 검사 | 대상 SHA | 실시·종료값·범위 |
|---|---|---|
| 연구 원장·직접 보유 raw 재검산 | `6b7cb060…` | 실시, exit0, 14 PASS. optional raw142개와 원문 스냅샷/추출을 재해시. 전체 body 미보존 항목은 명시적으로 제외. `evidence/fixed-result-validation.json`. |
| 커밋된 파일만 둔 별도 checkout | `6b7cb060…` | 실시, exit0, 14 PASS. Git의 정규화된 실제 커밋 bytes를 검사. 미커밋 raw cache를 읽었다고 주장하지 않음. `evidence/committed-checkout-validation.json`. |
| 공통 `python -B scripts/check.py --require-git` | `6b7cb060…` | 최종 exit0. 55단위 검사와 두 lab test/demo/export·Git bundle/restore 통과. `evidence/common-check-final.json`. |
| 최초 두 공통 검사 | 같은 `6b7cb060…` | 각각 exit1도 보존. 1차는 공유 clone의220개 Git 객체 누락; 공개 객체 재수신 뒤0개. 2차는 TMPDIR가 검사 workspace 안이어서 export guard에 막힘; 사용자 owned_path 안의 형제 임시폴더로 옮김. 검사 코드는 수정하지 않음. |
| manifest `check --fetch` | `6b7cb060…` | exit0, remote_checked, outside_paths/errors없음. `evidence/session-check-result.json`. |
| 핵심9파일 전체 원격 재열람 | `6b7cb060…` | GitHub fetch_file 전체UTF-8본문과 public-fetched Git blob이9/9일치. RESULT·cards·SELF_CHECK·manifest·sources·routes·incidents·claims·comparison. `evidence/remote-reread.json`. |
| 검사 영수증 재열람 | `e6a79c3a…` | acceptance.json·COMMIT_LOG 전체본문/공개Gitblob2/2일치. 위 핵심9파일이6b7cb060부터 불변임도 확인. |
| 인계 직전 manifest `check --fetch` | **`e6a79c3ac05b84ea1c7db313233df1717cade756`** | **exit0, passed, remote_checked**. 아래 최종 영수증 요약. |

실행 명령:

```bash
python -B docs/workstreams/research/AF-RES-086/tools/validate_research.py --require-final-docs
python -B -m workbench.session check docs/workstreams/research/AF-RES-086/manifest.json --fetch
python -B scripts/check.py --require-git
```

공통 검사는 동일 결과 SHA의 별도 checkout에서 실행했다. 그 checkout과 TMPDIR 모두 사용자 owned_path 안이다. `scripts/check.py`를 주 작업트리에서 실행해 허용 밖 .workbench/lab에 쓰지 않았다. 공통 검사와 원장 검사는 역사적 공개 응답을 생성하는 검사가 아니다. 원 stdout/stderr는 공백까지 보존한 JSON 문자열과 SHA256으로 커밋했다.

인계 직전 최종 검사 요약:

```json
{
  "target_sha": "e6a79c3ac05b84ea1c7db313233df1717cade756",
  "started_utc": "2026-11-23T15:40:32.968807+00:00",
  "completed_utc": "2026-11-23T15:40:39.737100+00:00",
  "exit_code": 0,
  "command": "python -B -m workbench.session check docs/workstreams/research/AF-RES-086/manifest.json --fetch",
  "status": "passed",
  "freshness": "remote_checked",
  "integration_commit": "4eaab7a4ba954026026d2fce59982114f61acbf9",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_path_count": 504,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "stdout_sha256": "2e14e8291300aa0e18980f25bb74e103f56f79fcc83ff9b216c3b4fe75e74cdc",
  "stderr": "",
  "core_result_files_unchanged_from": "6b7cb06061742f9ecd42efac3788b4ce6ac6cc7b",
  "clean_before_handoff": true
}
```

위 검사는 HANDOFF의 부모까지다. 이 마지막 문서 커밋을 앞선 코드·원장 검사에 포함됐다고 주장하지 않는다. 마지막 커밋은 HANDOFF 하나만 추가하고 원격에서 다시 읽어 범위를 확인한다.

## 막힌 이유와 첫 다음 행동

막힌 것은 실행 권한이나 자료 최소량이 아니라 **고정 관측창의 공개 역사 기록 공석**이다. R1의 statuses는 지금 읽히지만 이전 상태가 없고 run/job은404다. P3의 두 내용을 읽은 보관 응답은 모두 주창 다음 날이며 시간도 다르다. 부가 공개자료·재게시 대조·보존기관·반례 탐색을 끝내도 이 간격을 메울 수 없었다.

**첫 다음 행동:** R1의 deployment2328795124 / run14035386117 / job39292155301을 지목하는 발행자의 당시 공개 정적 로그 또는 보관 응답을 확보해 입력45e0d9eb…와 연결한다. 발견할 공개 원문의 URL이 아직 없으므로 특정 파일을 이미 존재한다고 가정하지 않는다. 상태 API를 다시 읽어도 inactive 한 행이면 같은 공석을 유지한다. 판정을 바꾸려면 당시 status의UTC·state·environment_url과 실제root/leaf의판·지문이 함께 필요하다.

다음 조사자가 재조회할 정확한 공개 입력은 다음과 같다. 인증·신규 배포가 필요 없는 읽기만이며 이번 실행 결과는 이미 각 source 영수증에 있다. 미래 재실행은 새 UTC와 별도 후속 원장행으로 기록해야 한다.

```bash
TASK_RESEARCH_DIR=docs/workstreams/research/AF-RES-086
mkdir -p "$TASK_RESEARCH_DIR/evidence/followup"
curl --silent --show-error --location --max-time 45 \
  --dump-header "$TASK_RESEARCH_DIR/evidence/followup/r1-status.headers.txt" \
  --output "$TASK_RESEARCH_DIR/evidence/followup/r1-status.json" \
  'https://api.github.com/repos/r-lib/archive/deployments/2328795124/statuses'
curl --silent --show-error --location --max-time 45 \
  --output "$TASK_RESEARCH_DIR/evidence/followup/r1-run.json" \
  'https://api.github.com/repos/r-lib/archive/actions/runs/14035386117'
curl --silent --show-error --location --max-time 45 \
  --output "$TASK_RESEARCH_DIR/evidence/followup/r1-job.json" \
  'https://api.github.com/repos/r-lib/archive/actions/jobs/39292155301'
curl --silent --show-error --get --max-time 45 \
  --data-urlencode 'url=cibuildwheel.pypa.io/en/stable/*' \
  --data-urlencode 'matchType=prefix' --data-urlencode 'from=20251111' \
  --data-urlencode 'to=20251113' --data-urlencode 'output=json' \
  --output "$TASK_RESEARCH_DIR/evidence/followup/p3-stable-cdx.json" \
  'https://web.archive.org/cdx/search/cdx'
curl --silent --show-error --get --max-time 45 \
  --data-urlencode 'url=cibuildwheel.pypa.io/en/1.x/*' \
  --data-urlencode 'matchType=prefix' --data-urlencode 'from=20251111' \
  --data-urlencode 'to=20251113' --data-urlencode 'output=json' \
  --output "$TASK_RESEARCH_DIR/evidence/followup/p3-legacy-cdx.json" \
  'https://web.archive.org/cdx/search/cdx'
```

CDX에 status200 필터를 넣지 않는다. revisit도 실제 payload를 읽어야 하며 빈 결과는 사이트 실패가 아니다. RTD run별 artifact manifest는 공개 위치를 확보하지 못했으므로 문서에 없는 관리자 endpoint를 만들어 요청하지 않는다. 생성 파일 자체의 재확인은 `streams/python/history1-inputs.json`·`streams/python/archive-inputs.json`, `streams/r/phase2-inputs.json` 및 각 sources의 원 URL·고정 SHA를 사용한다. 실행하지 않은 것은 신규 서비스 빌드/배포, 비공개 API, 브라우저 상호작용·전체asset검사, A/B 효과와 새 모델 세션 인계 시험이다.

## 중앙 색인에 반영할 한 줄

`AF-RES-086 | PARTIAL | docs/workstreams/research/AF-RES-086/RESULT.md | 고정4자리: P3 보조두판 개별확인·주창공동0/1미확인, R1 inactive와생성파일보존은확인하나당시게시미확인; 원자료123·25계보, 사전후보변경1/4 | result 6b7cb06061742f9ecd42efac3788b4ce6ac6cc7b | depends AF-RES-082@1f8bf039ad4f9a38b99764a11f72b515facef39c`

## 마지막으로 유지할 핵심 약점 — 정확히 3건

1. **P3:** 주창 공동 제공·run별 파일 귀속 공석. 다음 대상은30298914/16/15의파일manifest와2025-11-11~13 stable/options·1.x응답이다. 파일지문→run과두경로같은시점/게시구간교집합 또는직접오판응답이 나와야 판단을 바꾼다.
2. **R1:** 남은inactive는전체역사상태가아니다. 다음 입력은2328795124·14035386117·39292155301·45e0d9eb…이며,당시state/UTC/env URL과root·leaf1.1.12응답지문을 잇는 공개 기록이 필요하다.
3. **사건·보존 대조:** typst의회복직후지문과Gitorious옛경로의직접소실시점은없다. 다음대상은같은source의회복dispatch catalog/artifact와종료당시HTTP보관본이다. 회복판·내용보존을경로시점과연결하기전에는strong0/12·0/4와해당한계를유지한다.
