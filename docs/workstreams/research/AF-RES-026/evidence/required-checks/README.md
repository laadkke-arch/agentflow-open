# 공통 검사 · 원래 실패와 환경 보강 후 성공

검사한 커밋은 두 번 모두 `ed14e806a5a7bf4e6195fd12024c482d31768449`이다. 원 작업 트리에서 공통 검사를 실행하지 않고, 소유 경로 `docs/workstreams/research/AF-RES-026/evidence/` 아래 임시 독립 clone에서 실행했다. clone의 `origin`은 공개 저장소 `https://github.com/laadkke-arch/agentflow-open.git`으로 설정했다. `TMPDIR`도 그 임시 경로 안에 두고 `PYTHONDONTWRITEBYTECODE=1`을 적용했다. 공통 코드·검사 조건은 변경하지 않았다.

실제 공통 명령은 다음과 같다. 영수증에는 실행한 Python의 절대 경로가 기록돼 있다.

```bash
python scripts/cloud_check.py --environment chatgpt-web-pro --fetch-contract
```

| 시도 | 검사 시각 UTC | 결과 | 직접 확인한 범위 |
| --- | --- | --- | --- |
| [1차: 로컬 객체 복사](20261122T060441Z-1e7428ab/run-receipt.json) | 2026-11-22 06:04:41.534374–06:04:58.409590 | **FAILED, exit 1** | doctor 통과 뒤 acceptance의 Git bundle 생성에서 객체 `cd97243aa037c0bd83dd84710e3f944187e21226`를 읽지 못했다. sessions는 도달하지 않았다. 원본 실패 로그를 보존했다. |
| [2차: 공개 원격의 필터 없는 clone](20261122T060608Z-be6bb4f7/run-receipt.json) | 2026-11-22 06:06:17.119625–06:06:25.615240 | **PASSED, exit 0** | doctor, acceptance, research-case, original-smoke, sessions 명령이 모두 종료 코드 0이었다. 원격의 완전한 객체 집합으로 Git bundle 생성·복원 단계가 통과했다. |

첫 시도는 원 작업 트리의 Git 객체 집합을 독립적으로 복사했고, 두 번째는 깊이·필터 제한 없이 공개 GitHub에서 새로 받았다. 객체 누락 실패가 환경 보강 뒤 해소되었으며, 이를 공통 코드 수정이나 검사 생략으로 해결하지 않았다. 두 시도의 공통 검사 전후 HEAD는 위 커밋으로 같았고 Git은 clean이었다. 원 작업 트리의 HEAD도 두 번 모두 그 커밋을 유지했다. 원 작업 트리의 다른 담당자가 동시에 작성한 소유 경로 문서는 검사 clone에 포함하지 않았다.

## 통과한 검사와 통과로 바꾸지 않는 상태

2차 [원본 cloud-check.json](20261122T060608Z-be6bb4f7/checker-artifacts/cloud-check.json)과 [acceptance.json](20261122T060608Z-be6bb4f7/checker-artifacts/acceptance.json)을 함께 읽는다.

- `unittest discover`는 **55 tests, OK**, Python 3.12.14였다. 원 로그는 [check-0.log](20261122T060608Z-be6bb4f7/checker-artifacts/check-0.log)에 있다.
- repo-intake와 reference-audit의 test/demo, 프로젝트별 export와 재사용, Git bundle 복원 뒤 지정 demo가 통과했다. 이는 새로운 OS 프로세스에서의 확인이며 새로운 AI 대화 세션을 시험했다는 뜻이 아니다.
- research-case 및 original-smoke도 종료 코드 0이다. 각 명령·시각·로그 경로는 원본 cloud-check 영수증에 있다.
- **sessions의 프로세스 종료 코드 0을 실제 세션 검증 통과로 확대하지 않는다.** 그 명령의 JSON 결과는 `status=not-executed`, `reason=no_active_sessions`, `count=0`, `freshness=not_checked`다. `--fetch-contract`를 요청했어도 활성 `docs/tasks` 항목이 없어 이 경로의 원격 세션 검증은 실행되지 않았다.
- 담당 연구 manifest의 원격 계약 확인은 진행 담당이 별도로 실행한 `workbench.session check .../manifest-cli.json --fetch` 영수증과 구분한다. 이 공통 검사 영수증 자체에 `remote_checked`를 덧씌우지 않는다.
- 공통 workbench 검사는 연구 원문의 진실·완독 정확성, 제품 구현, 가상 I/C/Q 전략의 실제 효과를 시험하지 않는다.

## 보존한 파일과 정리한 임시 자료

각 시도 폴더의 `stdout.log`, `stderr.log`, `preparation.log`, `run-receipt.json`은 해당 실행에 대한 기록이다. `checker-artifacts/`에는 원래 `.workbench/` 아래 생긴 소규모 영수증과 로그를 **내용 변경 없이** 복사했다. `run-receipt.json.copied_artifacts`가 원 경로·저장 경로·바이트 수·SHA256을 대응시킨다. 원본 cloud-check 영수증 속 `.workbench/...` 경로는 이 대응표로 찾을 수 있다.

1차에는 소규모 artifact 19개를 보존했다. 2차에는 29개를 보존했고 복사 후 SHA256 재검에서 불일치 0개였다. 1차 `acceptance.json`은 bundle 생성 전에 실패했으므로 생성되지 않았다. 그것을 성공 영수증으로 대체하지 않는다.

2차에서 만든 19,015,049바이트 Git bundle은 최종 산출물에 남기지 않았다. 그 digest `5f0f46ae367bf0fdd67b9b4b374b510dc3ad047d710205a28593d2c967f0c52a`와 복원 커밋은 원본 acceptance 영수증에 남아 있다. 두 시도의 임시 clone·TMPDIR·bundle을 각 실행이 만든 정확한 경로에서만 정리했고, 두 `run-receipt.json`에 `temporary_removed=true`로 기록했다.

## 재현

[run_cloud_check.py](run_cloud_check.py)는 공통 코드를 수정하지 않는 실행·보존 wrapper다. 같은 커밋의 원 작업 트리에서 다음과 같이 실행하면 공개 원격 clone 보강 경로를 재현한다. 실제 네트워크와 원격 상태가 달라질 수 있으므로 이후 실행은 새 시각의 별도 영수증으로 판단한다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-026/evidence/required-checks/run_cloud_check.py --commit ed14e806a5a7bf4e6195fd12024c482d31768449 --remote-clone
```

이 기록을 추가한 문서 커밋은 위 검사에 포함되지 않는다. 검사 대상은 정확히 `ed14e806a5a7bf4e6195fd12024c482d31768449`의 공통 코드와 기록이며, 이후 영수증·인계 문서의 커밋은 별도로 확인한다.
