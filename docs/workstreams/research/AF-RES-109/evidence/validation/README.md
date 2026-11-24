# 고정 결과판 검증 영수증

**검사 대상 결과 SHA: `c212aab782008f263cbee14f6304c029dc82ce3a`.** 이 디렉터리는 그 결과판을 검사한 뒤 붙인 영수증이다. 여기의 파일, 이후 갱신된 acceptance-evidence.json, 마지막 HANDOFF가 결과 SHA에 포함되어 검사된 것처럼 해석하지 않는다. 연구 수용은 계속 **PARTIAL**이다.

## 실제 주체·환경·입력

root 자동 작업자가 공유 Linux `Linux-6.18.57-x86_64-with-glibc2.41`, Python3.12.14에서 실행했다. 결과 SHA로 detached checkout한 별도 worktree는 각 검사 전후 clean이었으며 SHA가 바뀌지 않았다. `codex-cloud`는 공통 검사에 넘긴 라벨이다. native web-pro 계정·별도 클라우드 서비스 연결이나 새로운 AI 세션을 이 라벨로 증명하지 않는다.

GitHub connector에서 고정 ref의 RESULT, 모집·기지 안·검색·후보·선택·비용·출처·후속 원장과 SELF_CHECK·수용 근거·검산 지표·미실행 계획·재현 절차를 다시 읽었다. 핵심15파일의 원격 Git blob과 고정 checkout 객체가 모두 일치했다. 원격 본문을 다시 파싱한 결과도 요청6, frame160, baseline6, 검색108이벤트, 후보36, 선택33, 비용12, 후속6, 출처198행/고유산입33이었다. [remote-fixed-reread.json](remote-fixed-reread.json).

대표 원전 CSS UI §6.2와 yFiles ParallelEdgeLayouter §Concept/Features를 다시 열어 hit target의 한계와 same-pair 전제를 확인했다. 두 GitHub PR은 웹 도구가 차단했지만 GitHub connector의 공개 REST 응답으로 다시 읽었다. PR4526의 merge 책임, PR4230의 merge 시각, R2 원 요청자의 원인 불확실성을 재확인했다. 이 추가7개 열람/실패 기록은 [sources.jsonl](sources.jsonl)에 있고 원저작·발견 산입은 모두0이다. 원 결과의33개 재고를 늘리지 않는다.

## 실제 명령·종료값

| 명령 | UTC 시작→종료 | 종료값·관측 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-109/manifest.json --fetch` | 03:13:20.690821→03:13:33.623695 | 0, passed, remote_checked; 명시 manifest1개 |
| `python -B docs/workstreams/research/AF-RES-109/recalculate.py --check` | 03:13:33.638094→03:13:33.952046 | 0, 원장 일치; 연구 PARTIAL·strict0·제품시험0 유지 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` 첫 실행 | 03:13:33.966167→03:16:34.317060 | 1, unittest 하위 프로세스180초 timeout; 환경의 임시 경로 설정 오류 |
| 같은 공통 명령, 임시 경로 수정 뒤 재실행 | 03:17:43.687264→03:17:55.275456 | 0, 소스·검사 코드·시간제한 변경 없음; 같은 결과 SHA |

모든 시각의 날짜는2026-11-24, 시간대는UTC다. 명령 배열·주체·환경·시작/종료 clean·stdout/stderr SHA256은 [commands.json](commands.json)에 있다. 첫 실패의 [cloud-check.json](cloud-check.json)과 재실행의 [cloud-check-retry.json](cloud-check-retry.json)을 함께 보존한다.

## 첫 실패와 필요한 재실행

첫 TMPDIR을 검사 대상 checkout의 `docs` 아래에 뒀다. 기존 `workbench/test_runtime.py`와 `test_path_alias.py`는 `ROOT/docs`를 `TemporaryDirectory`로 복사하면서 `__pycache__`만 제외한다. 실제로 임시 workspace 안에 같은 임시 workspace가 반복 중첩된 경로를 관측했고 약7,193,456KiB의 임시 복사 트리가 생겼다. `scripts/check.py`의 기존180초 제한에 걸렸다. [environment-retry.json](environment-retry.json)에 중첩 경로 예와 원인을 기록했다.

실패 로그를 남긴 뒤 이번 실행이 만든 임시 트리만 제거하고, TMPDIR을 **검사 대상 checkout 바깥이면서 AF-RES-109 허용 경로 안**으로 옮겼다. 공통 검사 코드를 고치거나 timeout을 늘리지 않았다. 같은 소스 SHA에서 같은 명령을 재실행했고11.6초 안에 종료값0을 얻었다. 이후에는 같은 이유로 반복 검사하지 않았다.

다른 작업공간에서 같은 배치를 만들 때의 명령은 다음과 같다. 첫 명령의 작업 디렉터리는 원 저장소 루트이며, 아래 worktree가 이미 있으면 새로 만들지 말고 SHA/clean을 확인한다.

```sh
AF109_OWNER_ROOT="$PWD/docs/workstreams/research/AF-RES-109"
git worktree add --detach "$AF109_OWNER_ROOT/.cache/validation-checkout" c212aab782008f263cbee14f6304c029dc82ce3a
mkdir -p "$AF109_OWNER_ROOT/.cache/common-temp-outside-checkout"
cd "$AF109_OWNER_ROOT/.cache/validation-checkout"
TMPDIR="$AF109_OWNER_ROOT/.cache/common-temp-outside-checkout" python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

진행 조회용 보조 스크립트도 한 번 아직 생성되지 않은 `stdout_log` 키를 읽어 KeyError·exit1을 냈다. 이 조회는 gate가 아니며 검사 프로세스나 원장을 바꾸지 않았다. [monitoring-notes.json](monitoring-notes.json)에 구분했다.

## 공통 검사와 실제 연구의 경계

재실행은 doctor, acceptance, reference-audit discovery fixture, original smoke, sessions 명령까지 도달했다. workbench55개·repo-intake7개·reference-audit9개 테스트가 통과했고 export의 다른 프로젝트 제외·공유 helper 일치, Git bundle 복원도 통과했다. Git bundle의 범위는 Git 객체와 ref이며 issue·비밀·DB·LFS·untracked 자료의 백업이 아니다. [retry-acceptance.stdout.log](retry-acceptance.stdout.log).

공통 `check-all`은 종료값0이지만 자동 발견은 **count0 / no_active_sessions / freshness:not_checked / status:not-executed**다. 명시적으로 실행한 연구 manifest1개의 remote_checked 통과와 합쳐 쓰지 않는다. [retry-sessions.stdout.log](retry-sessions.stdout.log), [manifest.stdout.log](manifest.stdout.log).

reference-audit의 discovery는 저장소의 고정 fixture 실행이며 새 웹 검색이나 자동 탐색기 제품 검증이 아니다. 원 smoke도 환경 구조 검사다. 이71개 테스트와 기타 공통 검사는 후보27개 시험, Windows touchpad, 원 개발자의 채택·시간 절감 근거를 제공하지 않는다. [retry-research-case.stdout.log](retry-research-case.stdout.log), [retry-original-smoke.stdout.log](retry-original-smoke.stdout.log).

manifest fetch 때 통합판은 시작0bcaf7c에서4fbfd8e로 이동했다. 허용된 필수 문서만 비교한 결과 중앙 dot-control만 변경되었고 AF-RES-109 자기 행과 계약 해시는 그대로다. [integration-drift.json](integration-drift.json). 다른 PLAN#27 파일이나 중간 결과를 연구 입력으로 사용하지 않았다.
