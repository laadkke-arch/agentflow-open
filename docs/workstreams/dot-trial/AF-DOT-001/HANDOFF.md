# AF-DOT-001 — 다음 세션 인수인계

## 1. 식별

- 작업 ID / 시도 / 상태: `AF-DOT-001 / 1 / REVIEW_READY`.
- 작업 종류: `web-pro`. 세션이 제공받은 모델 표기: `GPT-6 Astra Pro`. 실제 수행 위치: ChatGPT 제공 클라우드 작업공간(Linux, Python 3.12.14)과 GitHub 연결.
- 관측 경계: Dot의 세션 생성 과정·모델 선택 UI·구독 등급은 여기서 별도로 관측하지 않았다. 진행 담당이 자신의 배정 기록에서 확인해야 한다.
- 공개 조회 참조: `AF-DOT-001#1`, 저장소·브랜치. 비공개 대화 URL·서비스 작업 ID는 저장하지 않았다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/dot-trial-af-dot-001`.
- 시작 SHA: `9c06a7a998a7040a708d9336545fbf3c9cdfd205`. 생성 직전 재확인한 통합 브랜치 head다.
- `depends_on`: 없음. 선행 HANDOFF 없음. 이번 작업 PR은 생성하지 않았다.
- 작성 직전 원격 내용까지 확인한 커밋: `766a0a59c54ff6a6e95f448079c2d81301d937d3`.
- 마지막 실제 검사 시각(UTC): `2026-11-19T13:24:58.870099+00:00`.
- **최종 결과는 이 HANDOFF를 추가한 커밋이다.** Dot은 저장 후 작업 브랜치 head와 이 파일을 읽어 정확한 SHA를 `result_commit`에 고정한다. 위 직전 커밋을 최종 결과로 오인하지 않는다.

## 2. 사용자 요구 / 작업 범위

기존 조사 표본의 후보 네 개를 검토하고, 새 세션이 이전 채팅 없이 출처 연결 검사를 수행할 수 있게 인계한다. 미래 제품 전체 설계·구현은 이번 범위가 아니다.

시작 SHA에서 지정된 다섯 문서·AF-DOT-001 항목을 직접 읽었다. 추가로 자료 색인, 조사 표본, 인계 양식, 협업 계약, 연구 브리프·프로토콜, 클라우드 절차와 관련 검사 코드를 확인했다. 주요 원본의 blob SHA·SHA-256은 [VERIFICATION.json](VERIFICATION.json)에 보존했다.

허용 쓰기 경로는 `docs/workstreams/dot-trial/AF-DOT-001/` 하나다. `dot-control.json`, 공통 색인·계약, 검사기·fixture·제품 코드는 수정하지 않았다. main·기존 AgentFlow Studio·운영 환경·비밀값·유료 자원에 접근하거나 변경하지 않았다.

## 3. 실제 변경과 저장 커밋

| 파일 | 변경 / 확인 |
| --- | --- |
| [manifest.json](manifest.json) | `session start --fetch`로 시작 SHA·계약 v2 해시·허용 경로·의존성 없음을 고정. |
| [REVIEW.md](REVIEW.md) | 네 후보의 역할·미확인·반례·조합 조건과 검사 경계. 별도 읽기 전용 검토자가 기존 고정 원문 다섯 파일을 재열람했고 주 작성자가 표본·fixture·검사 코드와 대조. |
| [VERIFICATION.json](VERIFICATION.json) | 검토 커밋의 실제 명령·결과·입력 해시·정적 대조·미실시 항목. |
| `HANDOFF.md` | 이번 변경과 다음 작업의 정확한 입력·명령·판정 범위. 마지막 커밋으로 전달. |

1. `d825179a47acb05b1f7c0fcf73ba0f5010ddefa0` — 검토와 manifest.
2. `fb3c499d51df36fcadbca709b3291c9fb30dea02` — 검사 증거.
3. `766a0a59c54ff6a6e95f448079c2d81301d937d3` — REVIEW·VERIFICATION 파일 끝의 여분 빈 줄만 제거.
4. 이 파일 추가 커밋 — 최종 인계.

manifest는 사용자의 명시적 쓰기 범위를 우선해 이 폴더에 생성했다. 기본 `check-all`은 `docs/tasks/*.json`만 찾으므로 이 작업은 아래 **개별 check**로 검사한다.

## 4. 실제 검증 결과

| 실행 | 대상 / 결과 |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench context reference-audit --query discovery` | 시작 SHA에서 exit 0; BRIEF·STATE·fixture 읽음, 출력 omitted 없음. discovery 실행은 아니다. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session start af-dot-001 --allow docs/workstreams/dot-trial/AF-DOT-001/ --output docs/workstreams/dot-trial/AF-DOT-001/manifest.json --fetch` | 시작 SHA에서 exit 0, `remote_checked`. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/dot-trial/AF-DOT-001/manifest.json --fetch` | 검토·증거 커밋에서 각각 exit 0. 인계 직전 아래 값으로 다시 통과. |
| Python 표준 라이브러리로 원본·fixture 정적 대조 | 검토 커밋에서 exit 0. 4후보·11주장·13출처; 13출처의 `id/url/checked_at_utc/level/revision` 일치, 모든 ID 표식 존재. `audit()`·discovery 미호출. |
| `git diff --check 9c06a7a998a7040a708d9336545fbf3c9cdfd205 HEAD` | 증거 커밋에서 파일 끝 빈 줄 두 곳으로 exit 2. 3번 커밋으로 수정 후 exit 0. |

인계 직전 계약 검사 기록:

```json
{
  "returncode": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "checked_at": "2026-11-19T13:24:58.870099+00:00",
  "checked_out_commit": "766a0a59c54ff6a6e95f448079c2d81301d937d3",
  "integration_commit": "9c06a7a998a7040a708d9336545fbf3c9cdfd205",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": []
}
```

검사기는 manifest 자체를 changed_paths에서 제외한다. 실제 변경 목록은 Git diff로도 확인한다. 마지막 HANDOFF 커밋은 위 검사보다 뒤에 생성된다. VERIFICATION의 기존 SHA·해시를 후속 문서 커밋까지 검사한 것처럼 쓰지 않는다.

**미실시:** discovery 실행은 AF-DOT-002에 배정된 다음 단계로 남겼다. 코드 변경이 없어 전체 검사도 반복하지 않았다. 외부 후보 실행·API·통합·live 약관 재검증, Dot 생성 UI·새 웹 Pro 세션 교체·PC 종료 후 지속 실행은 이번에 확인하지 않았다. 자료 검토·저장을 막는 장애는 없다.

## 5. 판단·근거

기존 판단을 유지한다. OpenAlternative는 발견 목록, OSSInsight는 활동 지표 설계, AlternativeTo는 수동 비교의 `reference`다. Libraries.io는 `component` 후보지만 `defer`이며 접근·응답·갱신·현재 조건 확인이 남았다. AlternativeTo를 경쟁 DB 수집원으로 사용하는 것은 표본의 저장된 판단에 따라 `reject`다.

원 관측은 `2026-11-19T10:00:21Z`, 근거는 D1 문서 또는 D2 코드 관찰이다. 재열람 범위·원문 URL·반례는 REVIEW에 있다. 내부 검토를 새 웹 Pro 세션 교체 성공으로 세지 않는다. 색인 갱신은 REVIEW의 제안만 전달한다.

핵심 경계: discovery는 **별도 fixture의 출처 ID 연결**만 검사한다. 조사 원본 JSON 동기화·주장 진실성·현재 서비스·계정 권한·추천 정확성은 검사하지 않는다. 코드에 maintenance 503 분기가 있다는 사실도 live POST 관측은 아니다.

## 6. 다음 대화의 첫 행동

**AF-DOT-002: 이 인계만 받아 기존 reference-audit discovery 검사를 실제 실행하고, 검사로 확인되지 않는 사실을 구분하라.**

1. 별도의 실제 웹 Pro 세션에서 최신 진행표의 AF-DOT-001 `result_commit`을 읽고 그 정확한 커밋의 HANDOFF·REVIEW·VERIFICATION을 직접 읽는다. 이전 채팅은 전달하지 않는다. 결과 SHA가 없으면 Dot이 원격 결과를 먼저 고정한다.
2. 자기 작업 브랜치는 **그 시점 최신 통합 브랜치**에서 시작한다. AF-DOT-001의 미통합 결과 위에 만들지 않는다. 기존 브랜치·미커밋 작업은 확인·보존한다.
3. 아래로 의존 SHA를 읽고, 자기 브랜치를 선택한 뒤 manifest를 생성한다. 기존 manifest는 덮어쓰지 않는다. 다음 작업용 명령이며 AF-DOT-001에서는 실행하지 않았다. **이 준비 단계의 어느 명령이든 실패하면 뒤 명령을 실행하지 않고 원인과 재개 첫 행동을 자기 HANDOFF에 남긴다.** 아래 실제 discovery 실행이 실패한 경우에는 종료 코드·로그를 먼저 보존한다.

```sh
git fetch --no-tags origin refs/heads/chore/workspace-foundation:refs/remotes/origin/chore/workspace-foundation refs/heads/work/dot-trial-af-dot-001:refs/remotes/origin/work/dot-trial-af-dot-001
AF001_RESULT="$(git show origin/chore/workspace-foundation:docs/automation/dot-control.json | python -c 'import json,re,sys; t=next(t for t in json.load(sys.stdin)["tasks"] if t["id"]=="AF-DOT-001"); s=t.get("result_commit"); assert isinstance(s,str) and re.fullmatch("[0-9a-f]{40}",s), "AF-DOT-001 result_commit is not fixed"; print(s)')"
git show "$AF001_RESULT:docs/workstreams/dot-trial/AF-DOT-001/HANDOFF.md"
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session start af-dot-002 --allow docs/workstreams/dot-trial/AF-DOT-002/ --output docs/workstreams/dot-trial/AF-DOT-002/manifest.json --dependency "work/dot-trial-af-dot-001=$AF001_RESULT" --fetch
```

manifest를 먼저 커밋한 뒤 저장소 루트의 깨끗한 checkout에서 실행한다. 미커밋 상태로 실행했다면 receipt의 dirty 값을 그대로 남긴다. 필요한 환경은 Python 3.12 이상과 Git이며 API 키·외부 서비스 호출·배포는 필요 없다.

```sh
git rev-parse HEAD
git diff "$AF001_RESULT" HEAD -- docs/research/discovery-case-2026-11-19.json lab/reference-audit workbench
PYTHONDONTWRITEBYTECODE=1 python -m workbench run reference-audit discovery
```

실행 전 관련 파일 차이를 읽고, 바뀌었다면 이번 인계의 원본과 다르다고 기록한다. 예상 출처 수를 맞추려고 검사기나 fixture를 수정하지 않는다.

| 입력 | 이번 기준 |
| --- | --- |
| 조사 원본 — 실행기가 직접 읽지 않음 | `docs/research/discovery-case-2026-11-19.json`; SHA-256 `1341689b4c7554bebd7185ff6e93b714824feae00a57f9d148b7974192099c0f` |
| 실제 실행 입력 | `lab/reference-audit/fixtures/discovery.json`; SHA-256 `52f87db095173ee92dad09d034dbc3b3176274988a87f80787127ccdd36a3c90` |
| 명령 / 코드 | `lab/reference-audit/project.json:tasks.discovery` → `task.py fixtures/discovery.json`, 작업 디렉터리는 `lab/reference-audit` |
| 원본 소스 | `9c06a7a998a7040a708d9336545fbf3c9cdfd205`; 실제 AF-DOT-002 실행 SHA는 별도 기록 |

### 보존할 결과

- 실행기가 반환하는 `receipt` 경로를 읽는다. `.workbench/runs/reference-audit/<실행 ID>/`의 이름을 추측하지 않는다.
- 그 폴더의 `receipt.json`, `stdout.txt`, `stderr.txt`를 AF-DOT-002 허용 폴더 안에 함께 복사해 커밋한다. 빈 로그·실패·timeout도 보존한다. 임시 경로만 인계하지 않는다.
- receipt의 source.commit·dirty·returncode·Python·입력 해시를 읽는다. **조사 원본은 receipt.inputs에 없으므로 원본 SHA-256도 별도로 기록한다.**
- 성공 receipt는 `python -m workbench verify-receipt reference-audit` 뒤에 실제 복사한 receipt의 저장소 상대 경로를 붙여 해시를 확인할 수 있다. 진실성 검사는 아니다.
- 이 고정 fixture의 **예상값**은 exit 0, `ok: true`, 출처 ID 오류 없음이다. AF-DOT-001의 실제 discovery 결과가 아니다. `claim_truth_checked: false`, `network_accessed: false`의 경계를 유지한다.
- 자기 manifest에 대한 `workbench.session check ... --fetch` 결과와 다음 첫 행동을 최종 HANDOFF에 저장한다.

새 세션의 실제 복원·실행 증거가 생기기 전에는 웹 Pro 교체나 PC 종료 후 지속 실행이 확인됐다고 보고하지 않는다.
