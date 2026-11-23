# AF-RES-100 인계

## 상태와 결과판

**완료 — 제한된 공개 자료 묶음에서의 근거 가용성·교체 손실 연구.** 신규 8요청 × A/B × F/S =32자리, 16개 A/B 비교를 원장에서 재구성했다. 비교가능은 14쌍이며 P3의 F/S 2쌍은 고정 인접판 공석으로 비교불가다. 사용자 실제 실행 성공률이나 일반적인 링크 정책의 동등성을 입증한 연구가 아니다.

- 작업 브랜치: `work/research-af-res-100`.
- 쓰기 범위: `docs/workstreams/research/AF-RES-100/`만 사용. 중앙 진행표·이전 연구 결과·이전 인계는 수정하지 않았다.
- 검사한 결과판: `b3f3694b54bb7a85dc7a21e2731841679fc6753c`.
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/RESULT.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/SELF_CHECK.md), [원장 재계산기](https://github.com/laadkke-arch/agentflow-open/blob/b3f3694b54bb7a85dc7a21e2731841679fc6753c/docs/workstreams/research/AF-RES-100/recompute.py).
- 이 파일은 결과판 검사와 GitHub 재열람 뒤 작성하는 마지막 단독 파일 커밋이다. 아래 검사는 이 인계의 부모 결과 SHA를 대상으로 했다. 인계 커밋 자체에 같은 검사 실행을 소급 주장하지 않는다.

## 핵심 수치와 해석

| 예산·층 | 배정쌍 / 비교가능 | A만 완결 | B만 완결 | 양쪽 완결 | 모두 미완결 | 비교불가 |
|---|---:|---:|---:|---:|---:|---:|
| F 전체 | 8 / 7 | 0 | 1 | 4 | 2 | 1 |
| F 경계 | 6 / 5 | 0 | 1 | 2 | 2 | 1 |
| F 대조 | 2 / 2 | 0 | 0 | 2 | 0 | 0 |
| S 전체 | 8 / 7 | 0 | 0 | 0 | 7 | 1 |
| S 경계 | 6 / 5 | 0 | 0 | 0 | 5 | 1 |
| S 대조 | 2 / 2 | 0 | 0 | 0 | 2 | 0 |

F의 완결은 9/16배정자리, 비교가능 사례의 정책자리만 분모로 삼으면 9/14이다(A 4/7, B 5/7). S는 0/16배정자리, 0/14비교가능자리다. F→S에서 완결을 잃은 정책자리는 9개(J1·J2·J4·P4의 A/B, P1의 B), 질문은 5개다. 승패가 갈린 F쌍은 1개여서 B 1/1은 이 한 사례의 기술통계이고 일반적 우월성을 뜻하지 않는다. S는 승패 분모0이므로 승률 산출 불가다.

유일한 B 이득은 P1에서 `knitr::include_graphics` 주변 helper로 입력 파일 선택을 바꾸는 해석을 허용할 때 나온다. 기존 호출·내장 옵션만 허용하면 B만 완결은0이 된다. P1은 현재 Pandoc 태그로 모집됐지만 최초 본문·태그에는 Pandoc이 없었다. 이를 제외해도 B만 완결은0이다. J1의 최종 JOIN 생성, J2의 사후 이질적 UserData를 포함한 전체 원 파이프라인, P4의 전체 PDF 빌드를 필수로 해석하는 민감도도 각각 보존했다. P4는 렌더링하지 않았다.

`evidence/derived/metrics.json`·`pairs.csv`·`displacement.csv`에 분모·16비교·24교체자리를, `judgments.jsonl`·`packets.jsonl`에 32판정·파일과 Unicode/UTF-8 구간을 기록했다. 인용115개는 등록 파일 해시와 해당 패킷 경계 안에 있고 최초 판정 전 노출로 덮이는지 재검사했다. 처음 판정→사전 감사 변경0, 사후 자료를 근거로 한 주판정 수정0이다.

F와 S는 각각64번의 파일 접근을 과금했다. 총128자리 중124성공·4공석이며 빈자리도 과금했다. F는 전체6,509,235자를 접근 가능하게 두고 실제 표시270,609자(패킷 안 중복 제외245,384자), 절 이동102회다. S는74,400자, 절 이동0회다. 같은 시간·독해량의 비교가 아니다. 네 모델 문맥의 교차 배정은 같은 질문의 다른 경로 선행 노출0으로 기록됐으나 24/32자리에 다른 질문의 공유파일 선행 노출이 있고 URL은 정책을 드러낼 수 있다. 사람의 독립 발견률과 사전 학습 지식의 영향은 미확인이다.

## 모집·자료·공개 후속

- `frame.csv`: 모집틀39건(jq24, Pandoc15), 최초 본문 직접 확인22건, 신규 선정8건, 이전68 ID와 중복0. 2026년 추가창은 불필요했다. 현재 jq 제목24건이 R0 읽기 전에 노출된 모집 절차 이탈을 기록했다. 원 사건 독립성은 확인 가능한 범위만 주장한다.
- `sources.jsonl`:303행, 최소자료 산입46고유자료. 신규 질문8, 주 공식16, 인접 공식10, 상류 원 시험5, 다른 분야 공식문서5·fixture2. 최소26개와 각 범주 하한을 충족한다. 원 답·댓글·실패 응답·다운로드만 한 파일은 이 하한에 넣지 않았다.
- 원래 흐름143행과 재개 흐름160행을 모두 보존했다. 원래 흐름의143행은 `ORIGINAL-P3-` ID와 `count_minimum=false`이며 이전 산입 표시를 별도 보존했다. 이전 보수적32자료와 현재46자료를 합산하지 않는다. 중복 연구를 새32자리로 늘리지 않았다.
- 원 질문 후속:8질문,5답(4질문),29revision,30일 내18댓글,현재채택3건. 원 사용자판·완전입력·필수출력을 함께 확인한 실행은0/8이다. 이는 실행 실패8건이라는 뜻이 아니다.
- 사후 첫 요청은2026-11-23T20:32:07Z이며② 원격 존재 확인20:29:13Z 뒤다. 채택은 J2·J4·P4이며 `evidence/resume2/outcomes/`의 공식 timeline payload로 시점을 확인했다. 원래 흐름에서 채택시각을 미확인으로 두었던 기록은 지우지 않았고 추가 회수와 구분했다.
- Q1~Q7 답·실제 근거·반례 탐색·한계는 `SELF_CHECK.md`, 질문별 최대 두 반환 링크·절·실패조건과 관점별 설명은 `case-notes.json` 및 RESULT 세 번째 표에 있다.

## 타 분야와 실제 실행의 범위

GDAL 3.10.0의 vertical-warp 문서·원 fixture와 PROJ 9.5.1의 grid 검색·optional grid 의미를 읽었다. 주 설명은 단일 band·`-novshift` 조건을 설명하고, 인접 자료는 grid 위치와 `@` 누락 의미를 좁힌다. 로컬 보조 실행은 GDAL3.10.3/PROJ9.6.0, 네트워크OFF이며 고정 상류판과 동일하다고 주장하지 않는다. 단일 band+20 grid는100→120, 두 band·novshift·optional missing은100유지, required missing은오류였다. 이 연구자 변형은 신규 모집이나 주 승패에 넣지 않았다.

Sphinx8.1.3의 inheritance-diagram 문서·PNG/SVG fixture와 Graphviz CLI 원문을 읽었다. 로컬 `dot`2.42.4의 단일 SVG 실행은 종료0이며 missing binary 대조는 FileNotFoundError다. Sphinx/docutils/pytest가 없어 고정 Sphinx fixture 자체는 실행하지 않았다. 이를 HTML·링크·caption 성공으로 확대하지 않는다. 096에서 쓴 공통 Sphinx 시험 gate는 재사용 표시하고 새 자료 수에서 제외했다. 새 사례의 문서·fixture는 096의 예제와 구분했다. 상세 `evidence/resume2/crossdomain/{report.md,fixtures.json,gdal-runtime.json,graphviz-runtime.json}`.

## 작업 계약·고정 입력·중간 원격 SHA

계획 통합판 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`, 최초 시작 통합판 `01177554d0fbd33a914ea9c982c348d442d1358d`, 재개 때 최신 통합판 `daf01339d0a81a3a8f19fad43b497480aa62515f`를 구분했다. 시작/재개 차이는 중앙 진행표였으며 수정하지 않았다. 마지막 작업별 check가 실제 fetch한 통합판은 `7e76659e81ba9c6c9a933c8164cb4b8a60abd4ed`다. 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`로 검사했다.

운영 의존 원격 및 이전 인계는 `work/research-af-res-096=fce8d0ded93fe1f13f2c4978ed273c1ceef32934`, 연구 결과 입력은 `1d399f630930d2763459e16509c5224b0cded9a0`다. 필요한 096 파일의 blob/바이트 지문은 `evidence/start-receipt.json`에 있고 연구 입력 drift는 없었다. 최신 다른 신규 배정의 결과를 기다리지 않았다.

시작 명령은 아래와 같으며 실제 종료0이었다. 재개에서 기존 manifest를 덮어쓰지 않았다.

```sh
python -B -m workbench.session start af-res-100 --allow docs/workstreams/research/AF-RES-100/ --dependency work/research-af-res-096=fce8d0ded93fe1f13f2c4978ed273c1ceef32934 --output docs/workstreams/research/AF-RES-100/manifest.json --fetch
```

| 묶음 | 원격 SHA | 내용·변경 파일 기록 |
|---|---|---|
| ① | `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f` | 모집·원 요구·판·순위·두 예산·32패킷,154파일. `evidence/resume2/bundle-history.json` |
| ② | `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673` | 32초기판정·별도 사전 감사·16쌍,56파일. 동일 history |
| 재개 | `747359a546daf5300d82afa0904cbbf71e211202` | 캐시 복구·동시 진행·중복 독자 격리,19파일. 동일 history |
| ③ 재개 | `866ee7a68eec0f5c7077fec364685d6039d5ca75` | 공개 후속·밀림·교차 분야·의미 감사,46파일. `evidence/resume2/seal3-receipt.json` |
| ③ 원래 흐름 | `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1` | 원래 조사 흐름의 후속·교차 분야 기록 보존 |
| 합류 | `82e21d89eb592769f6f44ed75c9937400a565641` | 두③ 부모 보존. `evidence/resume2/concurrency-stage4.json` |
| ④ 결과 | `b3f3694b54bb7a85dc7a21e2731841679fc6753c` | 필수표·분모·불리한 해석·반환·자가검산·303행 정합,28파일. 아래 전체 경로 |

②가 원격에 이미 존재하는 것을 발견해 재개에서의 중복 읽기를 중단·격리했다. lease가 거부한 orphan `54ab626e9a558f0e442d74dad9697b787dec539b`는 branch에 연결하지 않았다. 후속 원격 합류도 fast-forward로 보존했다. shell `git push`의 credential 실패(exit128) 후 GitHub connector의 create-tree/commit와 expected-SHA lease update를 사용했다. CSV CRLF 정규화 때문에 로컬 fast-forward가 한 번 거부되어 보호 stash에 남기고 원격판을 인수했다. reset·force push·기존 history 덮어쓰기는 하지 않았다. 실패/복구 기록은 `evidence/resume2/concurrency*.json`, `evidence/resume.json`, `evidence/git-write-route.json`에 있다.

④ 변경28파일(owned_path 상대):

```text
PROGRESS.md
REPORT_NOTES.md
RESULT.md
SELF_CHECK.md
assemble_supplement.py
case-notes.json
displacement.csv
evidence/derived/metrics.json
evidence/derived/required-tables.md
evidence/resume2/bundle-history.json
evidence/resume2/concurrency-stage4.json
evidence/resume2/concurrent-original-sources.jsonl
evidence/resume2/crossdomain/assemble_evidence.py
evidence/resume2/crossdomain/audit-stage4.json
evidence/resume2/crossdomain/report.md
evidence/resume2/crossdomain/reproduce_sources.py
evidence/resume2/crossdomain/sources.jsonl
evidence/resume2/crossdomain/validation.json
evidence/resume2/final-independent-review.json
evidence/resume2/final-independent-review.md
evidence/resume2/seal3-receipt.json
evidence/resume2/stage4-corrections.json
evidence/resume2/stage4-integration-validation.json
evidence/resume2/stage4-validation.json
evidence/resume2/supplement_annotations.json
outcomes.csv
recompute.py
sources.jsonl
```

## 결과 SHA의 검사와 GitHub 재열람

| 검사 | 실제 대상 SHA | 실행 UTC | 종료·범위 |
|---|---|---|---|
| 작업별 `check manifest --fetch` | `b3f3694b54bb7a85dc7a21e2731841679fc6753c` |21:17:56–21:18:06|0, remote_checked. 변경344경로, 범위 밖0, 미해결병합0, 오류0. Git 계약·소유범위 검사 |
| 공통 `cloud_check --fetch-contract --require-clean` | 같은 결과 SHA |21:21:42–21:22:10|0, 시작/끝 clean. doctor·acceptance·research-case·original-smoke·sessions 명령 전부 종료0 |
| 공통 검사 속 개별 session | 같은 결과 SHA |21:22:10|**not-executed / no_active_sessions / count0 / freshness not_checked**. 위 개별 AF-RES-100 check가 별도로 수행됨 |
| `assemble_supplement.py --check` | 같은 결과 SHA |21:22:28–21:22:29|0,303행·46산입·24교체자리 |
| `recompute.py --check` | 같은 결과 SHA |21:22:29|0,32자리·16쌍·14비교가능·115인용·9손실·주 변경0 |
| GitHub 결과 재열람 | 같은 결과 SHA |21:22:29까지 대조 완료|RESULT·재계산기·SELF_CHECK 전체 및 원장 명시 구간이 로컬 결과와 동일 |

날짜는 모두2026-11-23 UTC다. 공통 검사는 owned_path의 ignored 임시 detached checkout에서 실행하여 쓰기를 이 범위 안에 두었다. `chatgpt-cloud`는 호출자가 정한 환경 이름이며 GitHub Actions나 새 사람/AI 세션을 입증하지 않는다. 공통 검사는 workbench 구조·예제·계약 검사이며 제품, 검색 품질, 사용자 원 실행을 검증하지 않는다. 원래 stdout과 receipt의 핵심 값·하위 검사 출력은 아래 JSON에 이 인계의 일부로 커밋한다. 임시 checkout 로그 경로는 영구 산출물 링크로 제시하지 않는다.

별도 문맥 `dependency_audit`가 ④ 초안의 계산·바이트 경계·원장 지문을 검토했고, 결과 SHA에서도 추가143행 전부 비산입·46고유자료·주5파일 불변을 읽기 전용으로 재확인했다. 사람 검토나 맹검 발견 실험은 아니다. 자기 검산은 원장 생성기와 `SELF_CHECK.md`, 다른 모델의 실제 검토는 `evidence/resume2/final-independent-review.*` 및 아래 추가 검토 영수증으로 구분한다.

GitHub에서 RESULT blob `88895e7438795df58f5211b1c3c53d501864b2de` 전체를 다시 열어 첫 필수3표(8/32/8행), 마지막3약점 표와 본문을 대조했다. `recompute.py`, `SELF_CHECK.md` 전체도 동일했다. `packets.jsonl`1–4행, `judgments.jsonl`17–20행(P1 네 조건), `sources.jsonl`1–2행을 각각 원격에서 열어 정확한 범위 텍스트를 대조했다. 범위 조회를 원장 전체 재열람이라고 주장하지 않는다. 등록된 모든115인용의 전수 대조는 로컬 결과 SHA 재계산 검사가 맡았다.

## 재현·미실시와 재개 첫 행동

완료 묶음은 반복하지 않는다. **재개 첫 행동은 원격 branch의 최신 SHA와 이 인계부터 읽고, 현재 결과의 원장 지문이 유지되는지 `recompute.py --check`로 확인하는 것이다.** 문서 가용성 결과를 유지한 채 마지막 세 행의 원 입력이 실제 공개되는 경우에만 별도 실행·독립 독해 실험을 새로 배정한다.

원장 재현(저장소 루트, 먼저 hydrate/restore를 통해 고정 해시를 복구; 전체 corpus 다운로드 자체는 독해/자료 수가 아님):

```sh
python -B docs/workstreams/research/AF-RES-100/hydrate_ledgers.py
python -B docs/workstreams/research/AF-RES-100/restore_cache.py --all
python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify
python -B docs/workstreams/research/AF-RES-100/assemble_preseal.py --check
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch
python -B scripts/cloud_check.py --environment chatgpt-cloud --fetch-contract --require-clean
```

마지막 공통 명령은 깨끗한 checkout에 쓰기 가능한 `.workbench`를 요구한다. 본 작업의 쓰기 제약을 유지하려면 이때와 같이 owned_path 내부 별도 checkout을 준비한다. 이전 `assemble_evidence.py`는 원래③ 집계 재현용이다. 현재 최종303행·46산입·RESULT는 위 `assemble_supplement.py`와 `recompute.py`를 사용한다.

미실시: 자연 요청8건의 전체 원 실행, jq/sed/knitr/CeTZ 고정 상류시험, 고정 GDAL 상류 suite, Sphinx fixture. 원 입력·사용자판·실행 의존이 없거나 문서 근거 조사 범위 밖이었으며 연구자 예제로 원 질문을 채우지 않았다. 실행 확인0/8의 입력 결손은 `outcomes.csv`·`case-notes.json`, 상류 실행의 정확한 source pin·fixture·node는 `evidence/resume2/crossdomain/fixtures.json`에 있다. 준비된 각 고정 소스 tree에서 다음 명령을 실행할 수 있다. 이 인계에서는 미실시다.

```sh
# GDAL 3.10.0, 35a44cc570cdf4dbd55611e4bd61da76e56bc221, 필요한 test 의존 준비
python -m pytest autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135 autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135j autotest/utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135k
# Sphinx 8.1.3, a1510de4777eaa2e569435f95b05f6f3293d7035, Sphinx/docutils/pytest 및 dot 준비
python -m pytest tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_png_html tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_svg_html
```

색인 제안 한 줄: **부분 설계의 필수 조건별로 고정 URL·볼 절·입력/판·실패조건을 함께 반환하고, 인접 슬롯 대체와 첫 일치 발췌가 잃는 근거를 별도 표시한다.**

## 기계 판독 검사·재열람 영수증

```json
{
  "scope": "Actual final result-SHA checks and remote readback; this HANDOFF-only commit itself is not the tested code/result SHA.",
  "task_check": {
    "command": [
      "python",
      "-B",
      "-m",
      "workbench.session",
      "check",
      "docs/workstreams/research/AF-RES-100/manifest.json",
      "--fetch"
    ],
    "target_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "started_utc": "2026-11-23T21:17:56.919149+00:00",
    "finished_utc": "2026-11-23T21:18:06.006802+00:00",
    "exit_code": 0,
    "stdout_sha256": "1a6d2e6ed78581f78f7cb2cea24d6a53c83c8cff71a9433658fb49c7f6850736"
  },
  "task_check_output": {
    "status": "passed",
    "task_id": "af-res-100",
    "freshness": "remote_checked",
    "checked_at": "2026-11-23T21:18:05.997184+00:00",
    "checked_out_commit": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "task_base_commit": "01177554d0fbd33a914ea9c982c348d442d1358d",
    "integration_commit": "7e76659e81ba9c6c9a933c8164cb4b8a60abd4ed",
    "scope_base_commit": "01177554d0fbd33a914ea9c982c348d442d1358d",
    "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
    "outside_paths": [],
    "unmerged_paths": [],
    "errors": [],
    "boundary": "Git contract and ownership checks; not a new AI chat or product verification",
    "changed_paths_count": 344
  },
  "task_check_stderr": "",
  "cloud_check": {
    "command": [
      "python",
      "-B",
      "scripts/cloud_check.py",
      "--environment",
      "chatgpt-cloud",
      "--fetch-contract",
      "--require-clean"
    ],
    "target_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "checkout_under_owned_path": true,
    "started_utc": "2026-11-23T21:21:42.338221+00:00",
    "finished_utc": "2026-11-23T21:22:10.366067+00:00",
    "exit_code": 0,
    "stdout_sha256": "2499b1eee895ff12506363e02b4a0d0939fe6f87983727bfe48f534c89003ea8",
    "receipt": {
      "schema": 1,
      "scope": "workbench checks, not product or browser integration",
      "environment": "chatgpt-cloud",
      "environment_is_caller_label": true,
      "platform": "Linux-6.18.57-x86_64-with-glibc2.41",
      "python": "3.12.14",
      "started_at": "2026-11-23T21:21:42+00:00",
      "completed_at": "2026-11-23T21:22:10+00:00",
      "status": "passed",
      "exit_code": 0,
      "source_start": {
        "commit": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
        "dirty": false,
        "clean": true
      },
      "github": {
        "event_name": null,
        "event_sha": null,
        "run_id": null,
        "run_attempt": null,
        "pr_head_sha": null,
        "pr_base_sha": null,
        "checked_out_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c"
      },
      "contract_fetch_requested": true,
      "require_clean": true,
      "checks": [
        {
          "name": "doctor",
          "command": [
            "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
            "-m",
            "workbench",
            "doctor"
          ],
          "timeout_seconds": 30,
          "started_at": "2026-11-23T21:21:42+00:00",
          "status": "passed",
          "exit_code": 0,
          "completed_at": "2026-11-23T21:21:42+00:00",
          "stdout_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/doctor.stdout.log",
          "stderr_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/doctor.stderr.log",
          "stdout_sha256": "c6c51f978e9fcc69a102eb5431743ddf2c7aa721881a0ad354a274a1286ef866",
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "name": "acceptance",
          "command": [
            "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
            "scripts/check.py",
            "--require-git"
          ],
          "timeout_seconds": 420,
          "started_at": "2026-11-23T21:21:42+00:00",
          "status": "passed",
          "exit_code": 0,
          "completed_at": "2026-11-23T21:22:10+00:00",
          "stdout_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/acceptance.stdout.log",
          "stderr_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/acceptance.stderr.log",
          "stdout_sha256": "e6035419d0abc80666c41dde8bbd5949c3fc10e965c02b8ace1b7efe5fd7c41d",
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "name": "research-case",
          "command": [
            "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
            "-m",
            "workbench",
            "run",
            "reference-audit",
            "discovery"
          ],
          "timeout_seconds": 60,
          "started_at": "2026-11-23T21:22:10+00:00",
          "status": "passed",
          "exit_code": 0,
          "completed_at": "2026-11-23T21:22:10+00:00",
          "stdout_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/research-case.stdout.log",
          "stderr_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/research-case.stderr.log",
          "stdout_sha256": "bf594c197c2aa89793ea78ff2e323d88f99c52d5291262eb2ad7514357eb6656",
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "name": "original-smoke",
          "command": [
            "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
            "workbench/verify.py"
          ],
          "timeout_seconds": 30,
          "started_at": "2026-11-23T21:22:10+00:00",
          "status": "passed",
          "exit_code": 0,
          "completed_at": "2026-11-23T21:22:10+00:00",
          "stdout_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/original-smoke.stdout.log",
          "stderr_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/original-smoke.stderr.log",
          "stdout_sha256": "aae65a8ac9c8fced75b674fc9f9939c093de1e8cc749ed029f7f9ae396fbdc35",
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        },
        {
          "name": "sessions",
          "command": [
            "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
            "-m",
            "workbench.session",
            "check-all",
            "--fetch"
          ],
          "timeout_seconds": 60,
          "started_at": "2026-11-23T21:22:10+00:00",
          "status": "passed",
          "exit_code": 0,
          "completed_at": "2026-11-23T21:22:10+00:00",
          "stdout_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/sessions.stdout.log",
          "stderr_log": ".workbench/cloud-check-logs/9179dda348ce4da3b545b36ba053b83f/sessions.stderr.log",
          "stdout_sha256": "5dbd686bb3343f33497be6af8c6937c799634169e798e01675f30d9ec067d2ef",
          "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ],
      "session_validation": {
        "status": "not-executed",
        "reason": "no_active_sessions",
        "count": 0,
        "freshness": "not_checked",
        "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
      },
      "source_end": {
        "commit": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
        "dirty": false,
        "clean": true
      }
    },
    "receipt_sha256": "433475aaf7ea15c9a44ca2c140b51a54ba665c8b36c5393f9f814708250454af"
  },
  "cloud_subcheck_output": {
    "doctor": {
      "stdout": "{\n  \"python\": \"3.12.14\",\n  \"supported\": true,\n  \"projects\": [\n    \"repo-intake\",\n    \"reference-audit\"\n  ],\n  \"git\": {\n    \"commit\": \"b3f3694b54bb7a85dc7a21e2731841679fc6753c\",\n    \"dirty\": false\n  },\n  \"network_required\": false,\n  \"agent_daemon\": false\n}\n",
      "stderr": ""
    },
    "acceptance": {
      "stdout": "test_registered_third_project_is_not_implicitly_executed (test_acceptance_scope.AcceptanceScopeTests.test_registered_third_project_is_not_implicitly_executed) ... ok\ntest_clean_gate_rejects_tracked_child_mutation_and_dirty_restart (test_cloud_check.CloudCheckEvidenceTests.test_clean_gate_rejects_tracked_child_mutation_and_dirty_restart) ... ok\ntest_github_context_keeps_shas_without_copying_secrets (test_cloud_check.CloudCheckEvidenceTests.test_github_context_keeps_shas_without_copying_secrets) ... ok\ntest_no_active_sessions_is_preserved_as_not_executed (test_cloud_check.CloudCheckEvidenceTests.test_no_active_sessions_is_preserved_as_not_executed) ... ok\ntest_nonzero_retains_output_and_stops_later_checks (test_cloud_check.CloudCheckEvidenceTests.test_nonzero_retains_output_and_stops_later_checks) ... ok\ntest_timeout_is_nonzero_and_has_a_completed_receipt (test_cloud_check.CloudCheckEvidenceTests.test_timeout_is_nonzero_and_has_a_completed_receipt) ... ok\ntest_workspace_alias_uses_one_canonical_root (test_path_alias.WorkspaceAliasTests.test_workspace_alias_uses_one_canonical_root) ... ok\ntest_bad_source_shapes_rejected (test_runtime.RuntimeTests.test_bad_source_shapes_rejected) ... ok\ntest_big_context_rejected (test_runtime.RuntimeTests.test_big_context_rejected) ... ok\ntest_budget_and_omissions_explicit (test_runtime.RuntimeTests.test_budget_and_omissions_explicit) ... ok\ntest_context_contains_own_not_other_project (test_runtime.RuntimeTests.test_context_contains_own_not_other_project) ... ok\ntest_context_search_finds_decision (test_runtime.RuntimeTests.test_context_search_finds_decision) ... ok\ntest_deleted_input_still_leaves_failure_receipt (test_runtime.RuntimeTests.test_deleted_input_still_leaves_failure_receipt) ... ok\ntest_duplicate_source_id_rejected (test_runtime.RuntimeTests.test_duplicate_source_id_rejected) ... ok\ntest_export_excludes_other_project_and_secrets (test_runtime.RuntimeTests.test_export_excludes_other_project_and_secrets) ... ok\ntest_export_rejects_workspace_child (test_runtime.RuntimeTests.test_export_rejects_workspace_child) ... ok\ntest_export_runs_without_original_pythonpath (test_runtime.RuntimeTests.test_export_runs_without_original_pythonpath) ... ok\ntest_export_will_not_overwrite (test_runtime.RuntimeTests.test_export_will_not_overwrite) ... ok\ntest_impossible_budget_is_not_silent (test_runtime.RuntimeTests.test_impossible_budget_is_not_silent) ... ok\ntest_manifest_context_cannot_escape (test_runtime.RuntimeTests.test_manifest_context_cannot_escape) ... ok\ntest_manifest_rejects_arbitrary_shell (test_runtime.RuntimeTests.test_manifest_rejects_arbitrary_shell) ... ok\ntest_manifest_rejects_unbounded_timeout (test_runtime.RuntimeTests.test_manifest_rejects_unbounded_timeout) ... ok\ntest_missing_context_file (test_runtime.RuntimeTests.test_missing_context_file) ... ok\ntest_nonzero_exit_is_not_passed (test_runtime.RuntimeTests.test_nonzero_exit_is_not_passed) ... ok\ntest_project_identity_mismatch (test_runtime.RuntimeTests.test_project_identity_mismatch) ... ok\ntest_project_registry (test_runtime.RuntimeTests.test_project_registry) ... ok\ntest_receipt_altered_log_detected (test_runtime.RuntimeTests.test_receipt_altered_log_detected) ... ok\ntest_receipt_other_project_rejected (test_runtime.RuntimeTests.test_receipt_other_project_rejected) ... ok\ntest_receipt_stale_after_source_edit (test_runtime.RuntimeTests.test_receipt_stale_after_source_edit) ... ok\ntest_receipt_success_and_verify (test_runtime.RuntimeTests.test_receipt_success_and_verify) ... ok\ntest_reject_parent_and_absolute_paths (test_runtime.RuntimeTests.test_reject_parent_and_absolute_paths) ... ok\ntest_reject_symlink_escape (test_runtime.RuntimeTests.test_reject_symlink_escape) ... ok\ntest_source_empty_credentials_rejected (test_runtime.RuntimeTests.test_source_empty_credentials_rejected) ... ok\ntest_sources_validate (test_runtime.RuntimeTests.test_sources_validate) ... ok\ntest_task_cannot_mutate_inputs_and_claim_pass (test_runtime.RuntimeTests.test_task_cannot_mutate_inputs_and_claim_pass) ... ok\ntest_timeout_is_not_retried (test_runtime.RuntimeTests.test_timeout_is_not_retried) ... ok\ntest_unknown_project (test_runtime.RuntimeTests.test_unknown_project) ... ok\ntest_unknown_search_keeps_required_handover (test_runtime.RuntimeTests.test_unknown_search_keeps_required_handover) ... ok\ntest_unknown_task (test_runtime.RuntimeTests.test_unknown_task) ... ok\ntest_changed_task_cannot_use_itself_as_the_baseline (test_session.SessionTests.test_changed_task_cannot_use_itself_as_the_baseline) ... ok\ntest_cli_creates_a_manifest_once_without_overwriting_it (test_session.SessionTests.test_cli_creates_a_manifest_once_without_overwriting_it) ... ok\ntest_committed_and_untracked_out_of_scope_changes_fail (test_session.SessionTests.test_committed_and_untracked_out_of_scope_changes_fail) ... ok\ntest_conflicting_worktree_merge_fails_and_can_be_aborted (test_session.SessionTests.test_conflicting_worktree_merge_fails_and_can_be_aborted) ... ok\ntest_empty_queue_is_not_a_collaboration_pass (test_session.SessionTests.test_empty_queue_is_not_a_collaboration_pass) ... ok\ntest_exact_dependency_pin_detects_a_new_remote_result (test_session.SessionTests.test_exact_dependency_pin_detects_a_new_remote_result) ... ok\ntest_ignored_run_outputs_do_not_become_task_changes (test_session.SessionTests.test_ignored_run_outputs_do_not_become_task_changes) ... ok\ntest_independent_worktrees_merge_without_borrowing_ownership (test_session.SessionTests.test_independent_worktrees_merge_without_borrowing_ownership) ... ok\ntest_remote_contract_drift_without_version_bump_is_detected (test_session.SessionTests.test_remote_contract_drift_without_version_bump_is_detected) ... ok\ntest_reusing_an_integrated_task_for_new_changes_requires_a_new_pin (test_session.SessionTests.test_reusing_an_integrated_task_for_new_changes_requires_a_new_pin) ... ok\ntest_duplicate (test_verify.SourceValidationTests.test_duplicate) ... ok\ntest_empty (test_verify.SourceValidationTests.test_empty) ... ok\ntest_invalid_date (test_verify.SourceValidationTests.test_invalid_date) ... ok\ntest_invalid_evidence (test_verify.SourceValidationTests.test_invalid_evidence) ... ok\ntest_invalid_urls (test_verify.SourceValidationTests.test_invalid_urls) ... ok\ntest_valid (test_verify.SourceValidationTests.test_valid) ... ok\n\n----------------------------------------------------------------------\nRan 55 tests in 25.277s\n\nOK\n\n=== repo-intake/test stdout ===\n\n=== repo-intake/test stderr ===\ntest_bad_input_container (test_task.RepositoryIdentityTests.test_bad_input_container) ... ok\ntest_clone_aliases (test_task.RepositoryIdentityTests.test_clone_aliases) ... ok\ntest_collect_preserves_indices (test_task.RepositoryIdentityTests.test_collect_preserves_indices) ... ok\ntest_distinct_owner_not_merged (test_task.RepositoryIdentityTests.test_distinct_owner_not_merged) ... ok\ntest_idempotent_canonical_identity (test_task.RepositoryIdentityTests.test_idempotent_canonical_identity) ... ok\ntest_reject_ambiguous_or_deceptive (test_task.RepositoryIdentityTests.test_reject_ambiguous_or_deceptive) ... ok\ntest_rejected_credentials_not_echoed (test_task.RepositoryIdentityTests.test_rejected_credentials_not_echoed) ... ok\n\n----------------------------------------------------------------------\nRan 7 tests in 0.002s\n\nOK\n\n=== repo-intake/demo stdout ===\n{\n  \"repositories\": [\n    {\n      \"key\": \"github.com/other-owner/cpython\",\n      \"input_indices\": [\n        7\n      ]\n    },\n    {\n      \"key\": \"github.com/psf/requests\",\n      \"input_indices\": [\n        5\n      ]\n    },\n    {\n      \"key\": \"github.com/python/cpython\",\n      \"input_indices\": [\n        0,\n        1,\n        2\n      ]\n    }\n  ],\n  \"rejected\": [\n    {\n      \"index\": 3,\n      \"reason\": \"expected exactly /owner/repository, not a subpage\"\n    },\n    {\n      \"index\": 4,\n      \"reason\": \"only GitHub repository roots are supported\"\n    },\n    {\n      \"index\": 6,\n      \"reason\": \"queries, fragments and encoded paths need manual review\"\n    }\n  ],\n  \"input_count\": 8,\n  \"existence_checked\": false\n}\n\n=== repo-intake/demo stderr ===\n\n=== reference-audit/test stdout ===\n\n=== reference-audit/test stderr ===\ntest_does_not_collapse_subpages (test_task.ReferenceTests.test_does_not_collapse_subpages) ... ok\ntest_duplicate_id (test_task.ReferenceTests.test_duplicate_id) ... ok\ntest_invalid_id (test_task.ReferenceTests.test_invalid_id) ... ok\ntest_invalid_input (test_task.ReferenceTests.test_invalid_input) ... ok\ntest_missing_source (test_task.ReferenceTests.test_missing_source) ... ok\ntest_repeated_marker (test_task.ReferenceTests.test_repeated_marker) ... ok\ntest_reuses_root_identity (test_task.ReferenceTests.test_reuses_root_identity) ... ok\ntest_unused (test_task.ReferenceTests.test_unused) ... ok\ntest_valid_reference (test_task.ReferenceTests.test_valid_reference) ... ok\n\n----------------------------------------------------------------------\nRan 9 tests in 0.001s\n\nOK\n\n=== reference-audit/demo stdout ===\n{\n  \"ok\": true,\n  \"errors\": [],\n  \"used\": [\n    \"api-doc\",\n    \"upstream\"\n  ],\n  \"unused\": [\n    \"alternate-clone\"\n  ],\n  \"duplicate_repository_sources\": {\n    \"github.com/python/cpython\": [\n      \"upstream\",\n      \"alternate-clone\"\n    ]\n  },\n  \"claim_truth_checked\": false,\n  \"network_accessed\": false\n}\n\n=== reference-audit/demo stderr ===\n\nWORKBENCH_ACCEPTANCE={\"backup\": {\"commit\": \"b3f3694b54bb7a85dc7a21e2731841679fc6753c\", \"scope\": \"Git objects and refs only; not issues, secrets, DB, LFS or untracked files\", \"sha256\": \"b9665e2b2c940c35812c4dc9fd31b984120a778938807749752f9f3b5ec19dc7\", \"status\": \"passed\"}, \"exports\": {\"reference-audit\": {\"other_project_absent\": true, \"shared_helper_sha256\": \"5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a\", \"status\": \"passed\"}, \"repo-intake\": {\"other_project_absent\": true, \"shared_helper_sha256\": \"5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a\", \"status\": \"passed\"}}, \"new_model_session_tested\": false, \"projects\": {\"reference-audit\": {\"context_files\": [\"lab/reference-audit/STATE.md\", \"lab/reference-audit/BRIEF.md\", \"lab/reference-audit/RESEARCH.md\", \"lab/reference-audit/DECISIONS.md\", \"lab/reference-audit/sources.json\"], \"context_process\": \"fresh process, not a fresh AI session\", \"runs\": [{\"id\": \"20261123T212208Z-46f956e54840\", \"receipt\": \".workbench/runs/reference-audit/20261123T212208Z-46f956e54840/receipt.json\", \"status\": \"passed\", \"task\": \"test\"}, {\"id\": \"20261123T212208Z-70dac50f0b24\", \"receipt\": \".workbench/runs/reference-audit/20261123T212208Z-70dac50f0b24/receipt.json\", \"status\": \"passed\", \"task\": \"demo\"}], \"source_records\": 4}, \"repo-intake\": {\"context_files\": [\"lab/repo-intake/STATE.md\", \"lab/repo-intake/BRIEF.md\", \"lab/repo-intake/RESEARCH.md\", \"lab/repo-intake/DECISIONS.md\", \"lab/repo-intake/sources.json\"], \"context_process\": \"fresh process, not a fresh AI session\", \"runs\": [{\"id\": \"20261123T212208Z-141ca9b822ee\", \"receipt\": \".workbench/runs/repo-intake/20261123T212208Z-141ca9b822ee/receipt.json\", \"status\": \"passed\", \"task\": \"test\"}, {\"id\": \"20261123T212208Z-924974a30921\", \"receipt\": \".workbench/runs/repo-intake/20261123T212208Z-924974a30921/receipt.json\", \"status\": \"passed\", \"task\": \"demo\"}], \"source_records\": 4}}, \"python\": \"3.12.14\", \"schema\": 1, \"scope\": \"workbench acceptance, not discovery product\", \"source\": {\"commit\": \"b3f3694b54bb7a85dc7a21e2731841679fc6753c\", \"dirty\": false}, \"status\": \"passed\"}\n\n",
      "stderr": ""
    },
    "research-case": {
      "stdout": "{\n  \"schema\": 1,\n  \"id\": \"20261123T212210Z-1d9869d40cde\",\n  \"project\": \"reference-audit\",\n  \"task\": \"discovery\",\n  \"status\": \"passed\",\n  \"returncode\": 0,\n  \"attempts\": 1,\n  \"tracking_error\": null,\n  \"duration_seconds\": 0.041,\n  \"inputs\": {\n    \"lab/reference-audit/fixtures/discovery.json\": \"52f87db095173ee92dad09d034dbc3b3176274988a87f80787127ccdd36a3c90\",\n    \"lab/reference-audit/fixtures/input.json\": \"e6e6f211dde2a9184a41a0078c6bb8b8f9ce1afae08017af42ea0511710ec8c4\",\n    \"lab/reference-audit/project.json\": \"f8f6667a31347e33472677280e218d44780ff58c1669dc0a0f2d145ac50400e8\",\n    \"lab/reference-audit/sources.json\": \"06c9b569f2237370cab87c948a655bd8c7079705ad29639acb56006c079afec4\",\n    \"lab/reference-audit/task.py\": \"aa01a78fb057d55dbcd48a87f346fbc6dae2c4a6607312986bc927d4b66faf5d\",\n    \"lab/reference-audit/test_task.py\": \"2155a3ed4260dcb8084f81c69387dbc947bf37c2aeb5685044cd07d38c03d5b7\",\n    \"workbench/__init__.py\": \"c89288e0f257f46b5cfe1a8fb3f78cfe49f899cc82427bc9597aab3128ce4e20\",\n    \"workbench/__main__.py\": \"935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d\",\n    \"workbench/cli.py\": \"02087f34d697ef8de35473410ea684b73e5b2bc3179a3f8ca88f369ad3784ced\",\n    \"workbench/urls.py\": \"5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a\"\n  },\n  \"source\": {\n    \"commit\": \"b3f3694b54bb7a85dc7a21e2731841679fc6753c\",\n    \"dirty\": false\n  },\n  \"python\": \"3.12.14\",\n  \"workflow_run\": null,\n  \"stdout_sha256\": \"dc664ddf420fc08386ae3d4cefd2ef42ee59ebaf5bdafcbd44430c10f4ff7a8c\",\n  \"stderr_sha256\": \"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\n  \"boundary\": \"trusted repository tasks, not a sandbox or factual certification\",\n  \"receipt\": \".workbench/runs/reference-audit/20261123T212210Z-1d9869d40cde/receipt.json\"\n}\n",
      "stderr": ""
    },
    "original-smoke": {
      "stdout": "WORKBENCH_RECEIPT={\"challenge\": \"agentflow-workbench-roundtrip-001\", \"checked_files\": [\"AGENTS.md\", \"STATE.md\", \"docs/WORKBENCH.md\", \"workbench/sources.json\"], \"commit\": \"b3f3694b54bb7a85dc7a21e2731841679fc6753c\", \"limitation\": \"Structure checked; source truth, product and deployment NOT tested.\", \"run_id\": null, \"scope\": \"environment-only\", \"source_count\": 6, \"sources_sha256\": \"143d19ff6c09afbbc00f713486e4cedefc4225f064be8416c0b4859a6e9184bc\", \"status\": \"passed\"}\n",
      "stderr": ""
    },
    "sessions": {
      "stdout": "{\n  \"status\": \"not-executed\",\n  \"reason\": \"no_active_sessions\",\n  \"count\": 0,\n  \"freshness\": \"not_checked\",\n  \"contract_sha256\": \"19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc\"\n}\n",
      "stderr": ""
    }
  },
  "result_recomputation": {
    "target_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "commands": [
      {
        "command": [
          "python",
          "-B",
          "docs/workstreams/research/AF-RES-100/assemble_supplement.py",
          "--check"
        ],
        "started_utc": "2026-11-23T21:22:28.910409+00:00",
        "finished_utc": "2026-11-23T21:22:29.092448+00:00",
        "exit_code": 0,
        "stdout": "{\"sources\": 303, \"counted\": 46, \"displacement_positions\": 24, \"check\": true}\n",
        "stderr": ""
      },
      {
        "command": [
          "python",
          "-B",
          "docs/workstreams/research/AF-RES-100/recompute.py",
          "--check"
        ],
        "started_utc": "2026-11-23T21:22:29.092520+00:00",
        "finished_utc": "2026-11-23T21:22:29.291673+00:00",
        "exit_code": 0,
        "stdout": "{\"check\": true, \"packets\": 32, \"pairs\": 16, \"comparable\": 14, \"sources_counted\": 46, \"citations_checked\": 115, \"F_to_S_losses\": 9, \"primary_changes\": []}\n",
        "stderr": ""
      }
    ]
  },
  "github_readback": {
    "checked_utc": "2026-11-23T21:22:29.580Z",
    "target_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "result": {
      "path": "RESULT.md",
      "blob": "88895e7438795df58f5211b1c3c53d501864b2de",
      "full_text_equal": true
    },
    "entries": [
      {
        "path": "recompute.py",
        "blob": "820745375f9c42aff737088c9083b8f5d03f6c2d",
        "chars": 16033,
        "full_text_equal": true
      },
      {
        "path": "SELF_CHECK.md",
        "blob": "128135dacae18276f7d105299fa2896c2061635b",
        "chars": 5594,
        "full_text_equal": true
      },
      {
        "path": "packets.jsonl",
        "start_line": 1,
        "end_line": 4,
        "blob": "a5ab902fd86f7f61d7e532572a05ce4c30632f2f",
        "chars": 21727,
        "range_text_equal": true
      },
      {
        "path": "judgments.jsonl",
        "start_line": 17,
        "end_line": 20,
        "blob": "9d410a328432918b3f27f6b2f45488a0f4b04476",
        "chars": 18697,
        "range_text_equal": true
      },
      {
        "path": "sources.jsonl",
        "start_line": 1,
        "end_line": 2,
        "blob": "cd7f5592e63f03a18571bf79509bcb3a9a2097db",
        "chars": 3278,
        "range_text_equal": true
      }
    ]
  },
  "final_merge_review": {
    "target_sha": "b3f3694b54bb7a85dc7a21e2731841679fc6753c",
    "reviewer": "dependency_audit, separate model context",
    "recorded_utc": "2026-11-23T21:24:53.868885+00:00",
    "new_external_reads": 0,
    "new_runtime_experiments": 0,
    "human_review": false,
    "blind_discovery_review": false,
    "source_rows": 303,
    "unique_source_ids": 303,
    "concurrent_added_noncounted_rows": 143,
    "counted_unique_sources": 46,
    "primary5_byte_identical_to_seal2": true,
    "unresolved_findings": [],
    "scope": "Read-only final merge/source count and sealed-ledger consistency check. Earlier full draft review is evidence/resume2/final-independent-review.json."
  }
}
```

## 가장 중요한 남은 불일치·약점

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 유일한 B 이득 P1은 helper 호출 변경 허용과 현재 Pandoc 태그 모집에 의존한다. 최초 본문·태그에는 Pandoc이 없고 실제 SVG/EMF·helper·PPT가 없다. | 원 helper 구현, 실제 JPEG/SVG/EMF 파일과 같은 R Markdown 호출·knitr/rmarkdown/Pandoc 판을 고정한 입력. 기존 호출 불변 조건과 helper 조건을 나누어 실행한다. | 기존 호출을 바꾸지 않고 내장 옵션만으로 같은 선택이 되거나, helper 조건에서도 원 출력이 실패하면 P1의 해석 및 유일 이득의 범위를 바꾼다. |
| F/S는 같은 네 파일 접근이지만 표시량·절 이동·시간이 다르며 24/32자리에 선행 공유파일 노출이 있다. S의 첫 일치 규칙과 사람의 독립 발견률은 분리되지 않았다. | 동일 원 질문·고정 파일에서 절 선택 방식과 표시량/시간을 별도 배정한 새 맹검 문맥. 현재 원장은 `recompute.py --check`로 먼저 보존 확인한다. | 같은 표시 예산·독립 문맥에서도 P1의 이득이나 9자리 손실이 유지/반전되는 관측이 나오면 전달 단위에 관한 해석을 좁히거나 바꾼다. |
| 같은 판·완전한 원 입력·필수 출력 실행 검증은 0/8이고 P3는 고정 연구판 공석이다. J2 사후 UserData 사건도 원 조건부 변환 밖에 있다. | P3의 공개되지 않은 작동 Dockerfile·image digest·custom template·두 filter·원 Markdown, J2의 원 Security.json/evtx와 전체 envelope. 고정 GDAL/Sphinx node는 fixtures.json 명령대로 준비한다. | 원 자료로 최신 안정 소스와 실행이 연결되면 P3 비교 가능성을 재연구한다. 같은 입력의 성공·실패가 주 조건과 어긋나면 문서 충분성과 원 실행의 관계를 수정한다. |
