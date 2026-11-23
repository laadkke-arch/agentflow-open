# AF-RES-100 최종 인계

상태: **요청된 제한 공개자료 비교·원장·자가검산 완료. 원 사용자 실행과 사람의 독립 발견률은 미확인.** 작업 브랜치는 `work/research-af-res-100`, 쓰기 범위는 `docs/workstreams/research/AF-RES-100/`다. 이 인계는 최종 결과판을 원격에서 다시 열고 그 SHA의 검사를 마친 뒤 작성한 **HANDOFF.md 한 파일의 마지막 커밋**이다. 결과판 이후에는 사전 판단·자료·표를 바꾸지 않는다. 이 파일 자체를 포함한 커밋 SHA는 자기참조할 수 없으므로 Git 이력과 최종 응답에서 확인한다.

- 최종 결과판: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/RESULT.md), **`ab89ae6704471aaea96d175103839bc6356d389a`**.
- 전체 재현 절차: [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/REPRODUCE.md). Q1~Q7 답·근거·반례·남은 확인은 [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/SELF_CHECK.md).
- 사전 원장: [protocol.json](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/protocol.json), [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/frame.csv), [packets.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/packets.jsonl), [judgments.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/judgments.jsonl), [pairs.csv](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/pairs.csv).
- 사후·출처 원장: [displacement.csv](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/displacement.csv), [outcomes.csv](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/outcomes.csv), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/sources.jsonl).

## 1. 결과와 해석 범위

| 읽기 단위·층 | 배정 A/B 쌍 | 비교 가능 | A만 | B만 | 양쪽 완결 | 모두 미완결 | 비교 불가 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F 전체 | 8 | 7 | 0 | 1 | 4 | 2 | 1 |
| F 경계 | 6 | 5 | 0 | 1 | 2 | 2 | 1 |
| F 대조 | 2 | 2 | 0 | 0 | 2 | 0 | 0 |
| S 전체 | 8 | 7 | 0 | 0 | 0 | 7 | 1 |
| S 경계 | 6 | 5 | 0 | 0 | 0 | 5 | 1 |
| S 대조 | 2 | 2 | 0 | 0 | 0 | 2 | 0 |

8요청×2정책×2단위=**32자리**, 8×2=**16개 A/B 비교 위치**를 재구성했다. P3의 인접 도구 최신 안정판을 질문 이전 시점에 확정하지 못해 F/S 각 한 쌍을 비교 불가로 남겼다. 비교 가능 분모는 **14/16쌍**, 파일 접근 위치는 **128개 중 비공석124·공석4**다. P3 B의 3·4번 공석은 F/S 모두 과금했고 주 도구 파일로 보충하지 않았다.

F에서 A4/7·B5/7, 경계 A2/5·B3/5가 문서 근거상 완결이다. S는 비교 가능한 A/B 각 0/7, 경계 각 0/5다. F→S로 **비교 가능한 정책 경로14개 중 완결9개가 미완결로 바뀌고 새 완결0개**, 질문7개 중 J1·J2·J4·P1·P4의 5개 행이 바뀐다. 불일치 쌍의 B 비율은 F1/1이며 S는 분모0으로 **산출 불가**다. 표본이 작고 유일 이득에 의도 민감도가 있어 일반적 동등성·우월성으로 확대하지 않는다.

유일한 B 완결은 P1의 **helper 호출 변경을 허용하는 사전 주 해석**에서다. knitr의 실제 경로 선택 구현이 필요한 근거를 보탰다. 내장 옵션만 허용하는 사전 민감도에서는 그 이득이0이다. P1은 현재 Pandoc 태그의 모집 프레임에 들어왔지만 최초 본문·최초 태그에는 Pandoc이 없다. P1을 사후 제외하는 별도 민감도에서는 F 비교가능6쌍의 양쪽4·모두미완결2·B만0이다. 기본 원장을 사후에 고치지 않았다.

J1은 디버깅 절차의 근거, J2는 최초 본문 스키마의 조건부 변환, J4는 원 입력에서 없는 Iops를 null로 남기는 변환, P4는 YAML parse 수정까지만 완결이다. 완전한 원 입력의 JOIN 성공, 뒤늦은 J2 UserData 사건, 값이 없는 Iops의 수치 추정, 전체 P4 PDF 렌더링을 뜻하지 않는다. P4는 렌더링하지 않았다.

각 단위의 첫 접근은64회다. F의 절 이동102회, 실제 표시 구간 문자270,609자(패킷별 중복 제거 합245,384자), S의 절 이동0회·표시74,400자다. F의 전체 접근 가능 문자6,509,235자를 실제 읽은 양으로 세지 않았다. 시간·사람의 독해량을 동일하게 놓지 않는다. 115개 인용 모두 해당 패킷의 문자/UTF-8 바이트 경계·원 파일 지문·사전 표시 구간과 대조했다. 4개 별도 기계 읽기 문맥은 같은 질문의 다른 조건을 보지 않았지만, 24/32자리에는 다른 질문에서 같은 파일을 읽은 이력이 있다. 따라서 주 지표는 **제시된 근거의 충분성**이며 사람의 독립 발견률은 미확인이다. 최초 판정→사후 답 공개 전 가용성 감사의 완결·조건 상태 변경은0이다.

## 2. 모집·출처·사후 귀속

모집은 2025-07-01~12-31 UTC 생성순/동률 숫자 ID순으로 태그별 상한 안에서 했다. 39개 metadata ID, 최초 본문22개를 직접 읽어 8개를 선택했고 이전68 ID와 겹침0이다. 결원이 없어 2026년 추가 모집은 하지 않았다. 제목 metadata가 처음 수집에 노출된 절차 이탈, 현재 태그와 최초 태그 차이, 재게시·동일 원 입력의 독립성 미확인을 원장에 남겼다. 옛 질문을 새 적중으로 세지 않았다.

최종 `sources.jsonl`은 **337개 기록 행**, 하한에 산입한 **고유 직접 열람 1차 자료46개**다. 구성은 최초 질문8·고정 주 도구 공식16·인접 공식10·상류 원 시험5·다른 분야 공식 문서5·fixture2다. 반복 접근·답/댓글·실패 응답·원 시험 실행 준비용31개 기록은 이46개에 보태지 않는다. 원 흐름의 보수적32개와 재개 흐름의46개는 교집합28, 원 흐름만4, 재개만18이다. 두 집합을 합산하거나 32가 46의 부분집합이라고 쓰지 않는다. 외부 전문 대신 재열람 주소·필요한 짧은 근거·정확 구간·지문을 남겼고 보관 스냅샷의 긴 인용27개도 제거했다.

사전 판정 봉인은 `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673`다. 원 흐름의 원격 봉인20:22:57→첫 후속20:25:18 UTC, 별도 재개 흐름의 봉인 확인20:29:13→첫 후속20:32:07 UTC를 구분한다. 재개 중 중복으로 생긴 접근 로그9개와 부분 판정4행/2파일은 `evidence/resume2/duplicate-reading/`에 격리했으며 주32자리·발견률·비용에 합치지 않았다.

사후 보이는 답은5개/4질문, 현재 채택은3/8이다. 직접 다시 연 timeline의 채택 시점은 J2 `2025-07-14T21:04:27Z`, J4 `2025-08-06T11:30:01Z`, P4 `2025-07-25T13:35:19Z`로 모두30일 안이다. 이 event의 post owner를 채택 행위자로 오인하지 않았다. 30일 내 질문자의 토론/자기답5/8, 질문 수정3/8, 합집합7/8이지만 J4/P4 수정은 답보다 먼저라서7/8을 답의 실제 채택·성공으로 바꾸지 않는다. **같은 판·완전한 원 입력·필수 출력이 실행으로 함께 확인된 건0/8이며 8건의 실패라는 뜻이 아니다.** P1 helper 제안은 새 사용으로 확인되지 않았고 P3 작동 Dockerfile 자기보고의 실제 파일·digest·PDF는 취득한 스레드에 없다. 확인 근거는 `outcomes.csv`, `evidence/outcomes/acceptance-verification.json`이다.

밀린/추가 파일24위치(12+12, 추가 중 공석2), 고유 비공석21파일의 절을 대조했다. J3의 빠진 jq argv 구현과 부족한 Bash 규칙, J4 AWS 예시의 부분적 입력 구조와 EMR 어휘 중복, P1의 밀린 PowerPoint SVG/EMF writer 근거, P2의 실제 CeTZ 의존을 분리했다. A만 완결 및 승패는 같지만 필수 실패 조건이 제거된 사례는 확인하지 못했다.

과학 데이터·문서 빌드 반례는 고정 GDAL3.10.0/PROJ9.5.1, Sphinx8.1.3와 Graphviz 공식 문서에서 읽었다. 주 문서만으로 수직 변환 적용 조건·상속도 입력 규칙이 충분한 경우와 PROJ grid 검색 경로·Graphviz renderer 가용성까지 필요한 경우가 갈린다. GDAL135s는 `{empty_grid_gtx}`가 보간되지 않는 원 시험이고 일반 예외 assertion이 원 grid 값 실패의 원인을 입증하지 않는다. Sphinx membership 검사는 전체 집합·개수 동일성 검사가 아니다. AWS 고정 describe-volumes Example1의 빠진 따옴표는 실제 JSON parse 검사로 확인했으나 AWS API 응답 실패나 사용자의 jq 실패로 귀속하지 않았다.

## 3. 운영 계약과 커밋 이력

시작 최신 통합 SHA는 **`01177554d0fbd33a914ea9c982c348d442d1358d`**다. 계획 통합판 `fcde6becc49120c5be91adf43fb5b4aa42e71d48`에서 시작판까지 변경은 중앙 `dot-control.json`뿐이었다. 시작에 읽은 AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW와 배정 항목을 따랐고 중앙표는 수정하지 않았다. 096의 연구 결과 입력은 **`1d399f630930d2763459e16509c5224b0cded9a0`**, 의존 HANDOFF와 운영 원격 SHA는 모두 **`fce8d0ded93fe1f13f2c4978ed273c1ceef32934`**여서 의존 drift가 없었다. 실제 사용 파일 blob은 `evidence/start-receipt.json`, `evidence/dependency-audit.md`에 있다.

실제 시작 명령(종료값0):

```sh
python -B -m workbench.session start af-res-100 --allow docs/workstreams/research/AF-RES-100/ --dependency work/research-af-res-096=fce8d0ded93fe1f13f2c4978ed273c1ceef32934 --output docs/workstreams/research/AF-RES-100/manifest.json --fetch
```

| 묶음·통합 | 원격 보존 SHA | 변경 파일 근거 |
|---|---|---|
| ① 모집·원 요구·판·순위·예산 봉인 | `e0cb8eaec3cbd9a7e5d40291a5a883f33473ec2f` | 154파일; `evidence/seal1-receipt.json` |
| ② 32패킷·사전 판단·근거 봉인 | `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673` | 56파일; `evidence/seal2-receipt.json` |
| 별도 재개 흐름 | `747359a546daf5300d82afa0904cbbf71e211202` | `evidence/resume2/bundle-history.json` |
| ③ 재개 흐름 후속·타분야 | `866ee7a68eec0f5c7077fec364685d6039d5ca75` | `evidence/resume2/seal3-receipt.json` |
| ③ 원 흐름 후속·타분야 | `b3d7af5a3a55eba78adc6c3bd31db7eaf9de49b1` | 54파일; `evidence/seal3-integration-receipt.json` |
| 두 ③ 흐름 보존 병합 | `82e21d89eb592769f6f44ed75c9937400a565641` | 첫 부모 대비60파일; 위 영수증 및 `evidence/concurrent-integration.json` |
| ④ 재개 흐름 재계산·결론·검산 | `b3f3694b54bb7a85dc7a21e2731841679fc6753c` | 28파일; `evidence/resume2/bundle-history.json` |
| 기존 인계 보존 | `80e2d746d0aa0ad7c009043e1cea3ae2e3be1311` | 당시 HANDOFF 한 파일; 원문은 `evidence/resume2/handoff-80e2d74.md`에도 보존 |
| ④ 추가 감사·반례·정확 실행 계획 | `3ac381dd723c5f089b139ca270132d8be1caa5de` | 29파일; 다음 보존 병합의 둘째 부모 |
| 실질 최종 결과 통합 | `8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9` | 첫 부모 대비30파일; `evidence/seal4-integration-receipt.json` |
| 실제 결과 SHA 검사 영수증·보고 | `ab89ae6704471aaea96d175103839bc6356d389a` | `PROGRESS.md`, `RESULT.md`, `evidence/result-checks.json`, `evidence/seal4-integration-receipt.json`의4파일 |
| 최종 인계 | 이 파일의 커밋 | 부모 `ab89ae6704471aaea96d175103839bc6356d389a`; 변경 허용 파일은 `HANDOFF.md` 하나 |

처음 shell `git push -u origin HEAD:refs/heads/work/research-af-res-100`는 HTTPS 자격증명 부재로 종료128, 원격 변경 없음이었다. 연결된 GitHub의 Git data API로 blob/tree/commit을 만들고 예상 부모 SHA를 지정해 브랜치를 갱신했다. 동시 재개 작업 때문에 두 번 갱신이 거절/UNKNOWN이 되었을 때 현재 원격을 먼저 읽고 양쪽 커밋을 부모로 보존 병합했다. 강제 푸시하지 않았고 다른 흐름의 파일·인계를 삭제하지 않았다. 로컬은 fetch 후 working files를 보존하는 mixed/no-refresh로 원격 커밋에 맞췄다. 각 SHA와 변경 경로·blob 목록은 위 영수증과 Git 이력에 남아 있다.

## 4. 실제 검사 대상·종료값·범위

`8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9`의 두 검사 원문과 stdout/stderr는 결과판의 `evidence/result-checks.json`에 커밋돼 있다. 이어서 최종 결과판 **`ab89ae6704471aaea96d175103839bc6356d389a` 자체**를 별도 깨끗한 detached worktree에서 아래 두 명령으로 검사했다. 원 checker를 수정하지 않았으며 검사 산출물/임시 경로도 owned_path 아래에 두었다.

| 실제 대상 SHA | 명령 | UTC 시작→끝 | 종료값·범위 |
|---|---|---|---|
| `8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9` | `python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch` | 21:30:37→21:30:45 | 0; AF-RES-100 계약·범위·원격 최신성 |
| `8b22a47f9daaf8f6bfaaec06f441edb7c78a9ff9` | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 21:30:45→21:31:32 | 0; 공통 workbench 검사. 개별 session은 아래 skip |
| `ab89ae6704471aaea96d175103839bc6356d389a` | `python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch` | 21:34:00→21:34:07 | 0; `outside_paths=[]`, `unmerged_paths=[]`, `errors=[]` |
| `ab89ae6704471aaea96d175103839bc6356d389a` | `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | 21:34:07→21:34:28 | 0; doctor·acceptance·research-case·original-smoke·sessions 프로세스 각0 |

날짜는 모두 **2026-11-23 UTC**다. 마지막 fetch가 확인한 통합판은 `ace1a06a13ea435f5cb6a3e340ad24f03f68ecae`, 계약 SHA-256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`다. 공통 검사 안의 session 검증은 두 결과판 모두 **`status=not-executed`, `reason=no_active_sessions`, `count=0`, `freshness=not_checked`**여서 AF-RES-100 개별 계약을 실행하지 않았다. 별도 직접 `check --fetch`의 종료0이 이 manifest 검사 근거다. 공통 sessions 프로세스가0이라는 이유로 개별 검사가 실행됐다고 보고하지 않는다. 두 검사 모두 해당 SHA에서 clean 시작/끝, HEAD 불변이었다. 이 검사는 저장소 계약·workbench용이며 원8질문 실행이나 상류 프로그램의 정확성을 인증하지 않는다.

최종 결과판 검사 캐시만으로는 커밋된 기록이 되지 않으므로, 실제 명령·시점·대상·출력 지문·범위·gate·skip을 이 인계에 다시 보존한다. 아래는 원 영수증에서 긴 changed_paths 목록과 stdout 전문만 뺀 요약이며, 원 영수증 지문도 포함한다.

```json
{
  "started_utc": "2026-11-23T21:34:00.928841+00:00",
  "target_sha": "ab89ae6704471aaea96d175103839bc6356d389a",
  "verification_checkout": "/workspace/scratch/70ebadc29f31/agentflow-open/docs/workstreams/research/AF-RES-100/evidence/_cache/verification-ab89ae670447",
  "checkout_mode": "detached committed result; unmodified common checker; all generated logs under owned_path",
  "scope": "Actual repository ownership/contract and common workbench gates; not original user requests or upstream jq/Pandoc/R suites.",
  "completed_utc": "2026-11-23T21:34:28.430910+00:00",
  "all_exit_zero": true,
  "ending_head": "ab89ae6704471aaea96d175103839bc6356d389a",
  "ending_clean": true,
  "original_receipt_sha256": "1065f2ec4a77ed1e35741a03cef3a504c074deda720791d3545b2839dee7a0d5",
  "commands": [
    {
      "label": "workstream check --fetch",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "-B",
        "-m",
        "workbench.session",
        "check",
        "docs/workstreams/research/AF-RES-100/manifest.json",
        "--fetch"
      ],
      "cwd": "/workspace/scratch/70ebadc29f31/agentflow-open/docs/workstreams/research/AF-RES-100/evidence/_cache/verification-ab89ae670447",
      "target_sha": "ab89ae6704471aaea96d175103839bc6356d389a",
      "started_utc": "2026-11-23T21:34:00.928917+00:00",
      "completed_utc": "2026-11-23T21:34:07.326517+00:00",
      "exit_code": 0,
      "stdout_sha256": "03a3cb5ac3c6317d8e4adcfad25a27906bf787601d36e4155aafee94c2673839",
      "stderr_chars": 0,
      "result": {
        "status": "passed",
        "task_id": "af-res-100",
        "freshness": "remote_checked",
        "checked_at": "2026-11-23T21:34:07.315074+00:00",
        "checked_out_commit": "ab89ae6704471aaea96d175103839bc6356d389a",
        "task_base_commit": "01177554d0fbd33a914ea9c982c348d442d1358d",
        "integration_commit": "ace1a06a13ea435f5cb6a3e340ad24f03f68ecae",
        "scope_base_commit": "01177554d0fbd33a914ea9c982c348d442d1358d",
        "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
        "outside_paths": [],
        "unmerged_paths": [],
        "errors": [],
        "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
      },
      "changed_paths_count": 366
    },
    {
      "label": "common cloud_check",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "-B",
        "scripts/cloud_check.py",
        "--environment",
        "codex-cloud",
        "--fetch-contract",
        "--require-clean"
      ],
      "cwd": "/workspace/scratch/70ebadc29f31/agentflow-open/docs/workstreams/research/AF-RES-100/evidence/_cache/verification-ab89ae670447",
      "target_sha": "ab89ae6704471aaea96d175103839bc6356d389a",
      "started_utc": "2026-11-23T21:34:07.327130+00:00",
      "completed_utc": "2026-11-23T21:34:28.430440+00:00",
      "exit_code": 0,
      "stdout_sha256": "c98b329a7ac1e32872d4e50e1fde258e16c08f8a1aeac4053e9abe83ae975c53",
      "stderr_chars": 0,
      "common_receipt": {
        "schema": 1,
        "scope": "workbench checks, not product or browser integration",
        "environment": "codex-cloud",
        "environment_is_caller_label": true,
        "platform": "Linux-6.18.57-x86_64-with-glibc2.41",
        "python": "3.12.14",
        "started_at": "2026-11-23T21:34:07+00:00",
        "completed_at": "2026-11-23T21:34:28+00:00",
        "status": "passed",
        "exit_code": 0,
        "source_start": {
          "commit": "ab89ae6704471aaea96d175103839bc6356d389a",
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
          "checked_out_sha": "ab89ae6704471aaea96d175103839bc6356d389a"
        },
        "contract_fetch_requested": true,
        "require_clean": true,
        "session_validation": {
          "status": "not-executed",
          "reason": "no_active_sessions",
          "count": 0,
          "freshness": "not_checked",
          "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
        },
        "source_end": {
          "commit": "ab89ae6704471aaea96d175103839bc6356d389a",
          "dirty": false,
          "clean": true
        },
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
            "started_at": "2026-11-23T21:34:07+00:00",
            "status": "passed",
            "exit_code": 0,
            "completed_at": "2026-11-23T21:34:07+00:00"
          },
          {
            "name": "acceptance",
            "command": [
              "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
              "scripts/check.py",
              "--require-git"
            ],
            "timeout_seconds": 420,
            "started_at": "2026-11-23T21:34:07+00:00",
            "status": "passed",
            "exit_code": 0,
            "completed_at": "2026-11-23T21:34:28+00:00"
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
            "started_at": "2026-11-23T21:34:28+00:00",
            "status": "passed",
            "exit_code": 0,
            "completed_at": "2026-11-23T21:34:28+00:00"
          },
          {
            "name": "original-smoke",
            "command": [
              "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
              "workbench/verify.py"
            ],
            "timeout_seconds": 30,
            "started_at": "2026-11-23T21:34:28+00:00",
            "status": "passed",
            "exit_code": 0,
            "completed_at": "2026-11-23T21:34:28+00:00"
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
            "started_at": "2026-11-23T21:34:28+00:00",
            "status": "passed",
            "exit_code": 0,
            "completed_at": "2026-11-23T21:34:28+00:00"
          }
        ]
      }
    }
  ]
}
```

저작 단계의 `packet_builder.py --verify`, `validate_ledger.py --initial`, `validate_ledger.py`, `assemble_preseal.py --check`, `assemble_supplement.py --check`, `recompute.py --check` 및 보호된 사전 원장 비교는 모두 종료0이다. `evidence/final-authoring-validation.json`을 참조한다. 캐시 복원 offline 검사도 종료0: 등록 원문3,488개/21,845,551바이트와 archive7개/74,551,535바이트 지문 일치, 네트워크0·쓰기0·메모리 안전성 검사28건이다. 새 환경에서 모든 온라인 설치를 한 통합 실행은 하지 않았다.

별도 기계 읽기·가용성 감사, 115개 인용 경계/노출 순서 검토, 사후60개 공통 entity·24개 displacement·3개 채택 event 검토, 마지막 집계/링크 검토의 역할을 각각 `evidence/audit/`에 보존했다. 마지막 별도 리뷰는 실질 결과판의 본문 SHA-256 `5a32e5398c5525ac988816a8d92b751c682aa0d271e0557fe5c0858959f339a0`를 확인했고, 이후 검사 보고4파일 추가와 최종 GitHub readback은 주 작업자가 수행했다. 자기검토와 다른 기계 문맥 검토를 구분하며 **사람의 리뷰를 받았다는 주장은 없다**. 인계 초안도 별도 기계 문맥이 읽기 전용으로 대조했다. 최종 검사 요약의130개 scalar 값·원 영수증 지문·원격8개 blob·고정 링크21개·337/46개 집계·마지막3행이 일치했다. 이 검토가 찾은 인계 첫 표 S대조 행의 여분0 한 칸을 제거하고 모든 인계 표의 열수를 다시 확인했다. 이 수정은 결과판·원장·판정을 바꾸지 않는다.

## 5. GitHub 최종 결과판 재열람

2026-11-23T21:33:42~43Z에 GitHub의 **`ab89ae6704471aaea96d175103839bc6356d389a`**에서 아래8파일의 **전체 내용**을 다시 취득했다. 각 Git blob이 로컬 기대 지문과 같았다. RESULT 첫 세 표는8/32/8행, 마지막 약점 표3행, 실제 결과 SHA 검사·skip 사유를 확인했다. 원장32패킷/32판정, P1 BF `2c39a224e483`의 두 supported 조건·완결과4파일, sources337행/하한46개, 재현 명령 및 원 시험 실행 계획 링크를 다시 확인했다. 오류0이다. 이 검증은 사후 편집 결과 확인이며 새로운 사전 발견으로 세지 않는다.

| 원격에서 직접 연 파일 | 확인 blob SHA | UTC | 로컬 기대값 대조 |
|---|---|---|---|
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/RESULT.md) | `778e2a48ee5055269f336cb6fcb9dccbd733d185` | 2026-11-23T21:33:42.616Z | 일치 |
| [judgments.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/judgments.jsonl) | `9d410a328432918b3f27f6b2f45488a0f4b04476` | 2026-11-23T21:33:42.667Z | 일치 |
| [pairs.csv](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/pairs.csv) | `f24e9d8b8473a85be0d632bb2f6bd01a577c4e9a` | 2026-11-23T21:33:42.714Z | 일치 |
| [packets.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/packets.jsonl) | `a5ab902fd86f7f61d7e532572a05ce4c30632f2f` | 2026-11-23T21:33:42.899Z | 일치 |
| [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/SELF_CHECK.md) | `922bf41e7252ef1d80bd03e3b032e4f4d659bb63` | 2026-11-23T21:33:42.996Z | 일치 |
| [REPRODUCE.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/REPRODUCE.md) | `76f05343e6d633357b0b36e244ae06a1f68cd33a` | 2026-11-23T21:33:43.025Z | 일치 |
| [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/sources.jsonl) | `b8a0b1aa40d8544f0faf30b75d5194a0457b505c` | 2026-11-23T21:33:43.123Z | 일치 |
| [evidence/result-checks.json](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/result-checks.json) | `d77a0b6a4cf6f0ec4cc00a5fabb59d844e49ea72` | 2026-11-23T21:33:43.441Z | 일치 |

## 6. 재현과 미실시 실행의 명령·입력

현재 최종판의 계산 생성기는 `assemble_supplement.py`와 `recompute.py`다. `assemble_evidence.py` 등 원 흐름의 과거 생성기를 최종 통합 원장 위에 실행하지 않는다. 아래 검사는 원 프로그램 실행을 대신하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-100/restore_corpus.py --offline
python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py --initial
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py
python -B docs/workstreams/research/AF-RES-100/assemble_preseal.py --check
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
```

새 checkout은 `REPRODUCE.md` 순서로 고정 corpus를 `restore_corpus.py --restore`로 확보하고 archive/hash를 먼저 대조한다. 현재 환경의 jq1.7/Pandoc3.1.11.1은 연구판 jq1.7.1/Pandoc3.6과 다르고 Rscript/cabal은 없다. 원8건 실행·아래4개 고정 상류 suite·고정 GDAL/Sphinx node는 **미실시(종료값 없음)**다. 사용자 자료를 예제로 메우거나 최신판을 같은 판이라고 간주하지 않았다.

| 원 요청 | 다음 실행할 명령/봉인된 프로그램 | 필요한 실제 입력·판·관측 |
|---|---|---|
| J1 | `jq`의 `debug`를 원 JOIN 전후에 넣은 `judgments.jsonl` 패킷 `cc86f215a28e`의 전체 명령. stdout `joined.json`, stderr `trace.log`를 분리한다. | 원 `file1.json`, `file2.json`, 실제 jq판. 파일·행·INDEX/stream/pair별 마지막 probe를 확인한다. 진단 절차가 곧 JOIN 성공은 아니다. |
| J2 | 개별 event 입력이면 `jq '.EventData.Data \|= (map({key: .Name, value: .content}) \| from_entries)'`. `.Events/.Event[]` envelope 경로는 패킷 `b6aad97ea044`의 조건부 프로그램 중 실제 구조에 맞는 것을 고른다. | 원 `Security.json`/EVTX, 변환 전후 전체 envelope, GNU sed/yq/jq판. missing content는 null로 두며 뒤늦은 UserData는 별도 조건으로 실행한다. |
| J3 | jq 변환 `.schemes += [$content]`, `--argjson content`에 단일 argv JSON 값을 전달하는 패킷 `a13997d37fef`의 제안. 완전한 Bash 명령은 사전 패킷 근거가 부족하여 완결 명령으로 제시하지 않는다. | 원 settings/Grape JSON, 실제 `json_content`/`json_file` 값과 파일명 여부, Bash판, 확장 후 argv·`.new` 경로. 파일명 인수 대안을 원 JSON 내용 변수 명령과 혼동하지 않는다. |
| J4 | `jq '[.Volumes[] \| {VolumeId, VolumeType, Size, Iops, VolName: ([.Tags[]? \| select(.Key == "VolName") \| .Value][0])}]' described.json` | 전체 원 describe-volumes 응답, jq/AWS판. 동일 volume의 VolName/Size/Iops를 비교하고 없는 값은 null, 중복 tag는 첫값이라는 조건을 유지한다. |
| P1 | 패킷 `2c39a224e483`의 `include_preferred_graphics()` 정의와 실제 `include_preferred_graphics("external_figure.jpg")` 호출. `ext="svg"`/`"emf"` 및 원 `knitr::include_graphics` 호출 불변 조건을 각각 실행한다. | 실제 Rmd/JPEG/SVG/EMF, R/knitr/rmarkdown/Pandoc판, 원 PPTX 출력. helper를 정의만 하고 namespace-qualified 원 호출은 바꾸지 않는 경우도 따로 확인한다. |
| P2 | 최초 revision `245AC802-E2BD-486D-9214-F598A55EDD93`의 원 Pandoc 명령과 `test1.typ`, `relimport.typ`, `test2.typ`. | 실제 CeTZ0.3.4 전체/hash, Typst0.13.1/Pandoc3.1.3, 별도 연구3.6. `a=123`과 실제 import를 유지한 동일 Markdown을 비교한다. import 삭제·빈 dummy 금지. |
| P3 | 최초 revision `8AA85F98-D6E0-4E96-8BE7-3175E15F8B24`의 원 `build.sh`를 실제 image의 entrypoint/작업 경로/mount 조건에서 실행한다. 먼저 당시 최신 안정 image 발행·digest→source를 확정한다. | 작동 Dockerfile,6개 Markdown, `TEST-includes.txt`, custom `TEST-eisvogel.tex`, `pandoc-latex-environment`/`pandoc-latex-unlisted` 판, pdflatex, image digest. 그전에는 runnable Docker recipe나 B 공석 대체를 만들지 않는다. |
| P4 | 원 title을 `'Heading1: Heading2'`로 인용한 `text.md`에 `pandoc text.md -f markdown -t native`로 parse/metadata를 비교한다. | Pandoc2.18과 같은 원 Markdown. 원 title 값을 보존하고 parse 종료값·AST를 확인한다. 전체 PDF 렌더링은 이 과제에서 하지 않는다. |

원 시험을 실행할 때는 registered text 일부가 아니라 전체 고정 source tree와 보조 fixture가 필요하다. [정확 실행 계획](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/audit/upstream-execution-plan.md)에 명령의 상류 근거31자료·행·archive SHA·의존성/장치 gate를 남겼다.

| 고정 원 시험 | 준비·명령(각 고정 source root에서 실행) | 필수 입력·미실시 이유 |
|---|---|---|
| jq1.7.1 `71c2ab509a8628dbbad4bc7b3f98a64aa90d3297` | 고정 checkout, `git submodule update --init`; `autoreconf -i`; `./configure --with-oniguruma=builtin`; `make -j2`; `NO_VALGRIND=1 JQ="$PWD/jq" sh ./tests/jqtest` | `tests/jq.test`, jqtest/setup/modules, 고정 Oniguruma submodule와 빌드 산출물. archive만으로 submodule가 채워지지 않는다. 고정 빌드 미실시. |
| GNU sed4.9 | 전체 공식 release를 압축해제해 `./configure`; `make -j2`; `make check-TESTS TESTS=testsuite/bsd-wrapper.sh` | bsd-wrapper.sh/bsd.sh/bsd.good/init.sh, 생성 configuration·check_PROGRAMS. `bsd.sh` 단독 실행을 원 oracle 검사로 간주하지 않는다. 빌드 미실시. |
| knitr1.50 `01bf7eff974903d1498e76e92a3e4b3bf9273cf5` | 전체 package root에서 `make travis`; 상류 runner는 `tests/run-all.R`의 `library(testit); test_pkg("knitr")` | 전체 package/testit/plot/vignette 입력, R≥3.6과 Imports/Suggests·장치 gate. 검증된 단일 test-plot 파일 선택 명령은 없다. Rscript 부재. |
| Pandoc3.6 `8a72b8449ddccd84fcdffc1a09ae18c4baaca32a` | `cabal build test-pandoc`; `cabal test test-pandoc --test-options='-p yaml-metadata-blocks.md'` | 전체 cabal project·runner·원 golden5개·`test/command/yaml-metadata.yaml`. `--accept` 금지. P4의 정확 title case 자체는 상류5개에 없다. cabal 부재. |

다른 분야 원 시험은 [unrun.md](https://github.com/laadkke-arch/agentflow-open/blob/ab89ae6704471aaea96d175103839bc6356d389a/docs/workstreams/research/AF-RES-100/evidence/crossdomain/unrun.md)의 전체 준비조건을 따른다. GDAL `35a44cc570cdf4dbd55611e4bd61da76e56bc221`의 `autotest/`에서 다음 명령을 실행할 수 있도록 GDAL3.10.0/Python binding, PROJ/proj.db, MEM/GTX/VRT/GTiff와 pytest/pymod를 갖춘다.

```sh
python -m pytest -q utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135 utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135b utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135d utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135f
PROJ_DEBUG=3 python -m pytest -q -s utilities/test_gdalwarp_lib.py::test_gdalwarp_lib_135s
```

원 fixture는 값100의 1×1 MEM과3×3 GTX의20/5 값, 원 geotransform/CRS를 생성하며 첫 네 원 기대값은120/80/115/100이다. 이는 고정 원 시험에서 이번에 측정한 값이 아니다. 135s는 먼저 원문 그대로 실제 시도 파일명과 예외 trace를 보존한다. 실세계 grid/DEM이 없다고 이 상수를 실제 사용자 값으로 대신하지 않는다.

Sphinx `a1510de4777eaa2e569435f95b05f6f3293d7035` root와 전체 tests/roots, pytest/Sphinx fixture·Graphviz 실행기를 준비한 후:

```sh
python -m pytest -q tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram
python -m pytest -q tests/test_extensions/test_ext_inheritance_diagram.py::test_inheritance_diagram_svg_html
dot -Tsvg:
```

`test-inheritance`의 A/B/C/D/E/F 클래스·두 RST와 `ext-inheritance_diagram`의 conf/module/RST/inventory를 원문 그대로 써야 한다. `class_info` 전체 목록·renderer·skip·출력 파일을 기록한다. `dot -Tsvg:`는 renderer 조회 문법이며 비영 종료값만으로 build 실패라 하지 않는다.

이미 보존된 보조 실행은 별도 재개 흐름의 **GDAL3.10.3/PROJ9.6.0 파생5조건**, **Graphviz2.42.4 파생 DOT→SVG**다. 각 `evidence/resume2/crossdomain/*runtime.json`에 실제판과 출력이 있다. 고정 상류 suite와 Sphinx 빌드 성공이 아니다. GDAL runner의 프로세스0만으로 기대값 일치를 보장하지 않으므로 JSON의 개별 기대값을 함께 확인했다. 원8요청 실행 성공으로 세지 않는다.

## 7. 색인 제안·재개 첫 행동

색인 제안 한 줄: **네 파일을 고정해도 첫1,200자 발췌에서는 필요한 절이 사라질 수 있으므로, 사용자에게 반환할 도구 링크와 필수 조건의 정확한 절·원 입력 결손을 함께 보존하고 인접 링크의 도움은 호출 변경 허용 여부와 구분한다.**

재개 첫 행동: P3의 질문 이전 최신 안정 image 발행 기록과 digest→source 연결을 먼저 확인하고, 취득한 스레드에 없는 실제 작동 Dockerfile·custom template·두 filter·6개 Markdown을 확보할 수 있는지 판별한다. 확보 전에는 B 공석·비교불가를 유지한다. 모든 재실행은 이 결과판 원장을 보존하고 별도 시점·판·입력 지문으로 기록한다.

## 가장 중요한 남은 불일치·약점

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 유일한 B 이득 P1은 helper 호출 변경 허용과 현재 Pandoc 태그 모집에 의존한다. 최초 본문·태그에는 Pandoc이 없고 실제 SVG/EMF·helper·PPT가 없다. | 원 helper 구현, 실제 JPEG/SVG/EMF 파일과 같은 R Markdown 호출·knitr/rmarkdown/Pandoc 판을 고정한 입력. 기존 호출 불변 조건과 helper 조건을 나누어 실행한다. | 기존 호출을 바꾸지 않고 내장 옵션만으로 같은 선택이 되거나, helper 조건에서도 원 출력이 실패하면 P1의 해석 및 유일 이득의 범위를 바꾼다. |
| F/S는 같은 네 파일 접근이지만 표시량·절 이동·시간이 다르며 24/32자리에 선행 공유파일 노출이 있다. S의 첫 일치 규칙과 사람의 독립 발견률은 분리되지 않았다. | 동일 원 질문·고정 파일에서 절 선택 방식과 표시량/시간을 별도 배정한 새 맹검 문맥. 현재 원장은 `recompute.py --check`로 먼저 보존 확인한다. | 같은 표시 예산·독립 문맥에서도 P1의 이득이나 9자리 손실이 유지/반전되는 관측이 나오면 전달 단위에 관한 해석을 좁히거나 바꾼다. |
| 같은 판·완전한 원 입력·필수 출력 실행 검증은 0/8이고 P3는 고정 연구판 공석이다. J2 사후 UserData 사건도 원 조건부 변환 밖에 있다. | P3의 취득한 스레드에 없는 작동 Dockerfile·image digest·custom template·두 filter·원 Markdown, J2의 원 Security.json/evtx와 전체 envelope. 고정 GDAL/Sphinx node는 fixtures.json 명령대로 준비한다. | 원 자료로 최신 안정 소스와 실행이 연결되면 P3 비교 가능성을 재연구한다. 같은 입력의 성공·실패가 주 조건과 어긋나면 문서 충분성과 원 실행의 관계를 수정한다. |
