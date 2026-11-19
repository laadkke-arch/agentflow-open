# AF-DOT-002 — GitHub 인계 복원과 discovery 실행

- 작업 / 시도 / 상태: `AF-DOT-002 / 1 / REVIEW_READY`.
- 기록일: 2026-11-19. 시각은 별도 표시가 없으면 UTC.
- 시작 커밋: `34f108b9f4e4680943f1cf58fe2ded7d25f47aba` — 생성 직전 확인한 통합 브랜치 head.
- 의존 결과: [AF-DOT-001 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/HANDOFF.md).
- 실제 실행 커밋: `8ca328516facff584589c9bf7040062b8695398d`.
- 실행 증거 저장 커밋: `cd65bfd3119f8905c5244640c1805bfb3bfa20b5`.
- 증거: [receipt](execution/receipt.json), [stdout](execution/stdout.txt), [stderr](execution/stderr.txt), [검증 기록](VERIFICATION.json).

## 1. 결론

이번 지시와 GitHub의 고정 인계·참조 파일에서 목적과 남은 일을 복원하고, 기존 `reference-audit discovery`를 ChatGPT 제공 클라우드 작업공간에서 **실제로 한 번 실행했다**. 출처 ID 연결 검사는 통과했다. 네 후보의 주장 사실성·실제 서비스·이용 권한·프로젝트 적합성은 검증하지 않았다.

AF-DOT-001의 이전 채팅 원문을 요청하거나 읽지 않았다. 그 작업 결과 위에 브랜치를 만들지 않고 최신 통합 브랜치에서 시작했으며, 선행 결과는 별도 의존 SHA로 고정했다. Dot이 두 웹 Pro 세션을 만들고 모델을 선택한 과정은 여기서 관측하지 않았다. GitHub 인계 복원·실행 성공과 세션 생성·교체의 외부 관측은 구분한다.

## 2. 복원한 목적과 입력

선행 [REVIEW](https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/REVIEW.md)와 [VERIFICATION](https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/VERIFICATION.json)을 직접 읽었다. 복원한 다음 행동은 “기존 discovery를 실행하고, 출처 연결 검사와 사실 검증의 차이를 기록하라”였다. 새 후보 검색이나 미래 제품 설계는 배정되지 않았다.

기존 후보 판단은 인계된 기록으로 유지한다. OpenAlternative는 발견 목록, OSSInsight는 활동 지표 설계, AlternativeTo는 수동 비교 참고다. Libraries.io는 선택적 메타데이터 부품 후보이나 `defer`이며, AlternativeTo의 경쟁 DB 수집 용도는 저장된 판단상 `reject`다. 이것은 10:00:21Z의 원 관측과 AF-DOT-001 검토를 재사용한 것이며, AF-DOT-002가 후보나 현재 약관을 다시 확인한 결론은 아니다.

| 입력 | 실제 역할 | SHA-256 |
| --- | --- | --- |
| `lab/reference-audit/fixtures/discovery.json` | discovery가 직접 읽은 입력 | `52f87db095173ee92dad09d034dbc3b3176274988a87f80787127ccdd36a3c90` |
| `docs/research/discovery-case-2026-11-19.json` | 사람이 읽은 조사 원본. discovery·receipt 입력에 포함되지 않음 | `1341689b4c7554bebd7185ff6e93b714824feae00a57f9d148b7974192099c0f` |

실행 전 선행 결과와 현재 checkout 사이에서 위 조사 원본·`lab/reference-audit`·`workbench`의 Git diff가 비어 있음을 확인했다. 원본과 fixture 해시도 선행 HANDOFF와 같다. 이 사실로 기존 고정 자료의 동일성을 확인했으며, 후보 4개·주장 11개·출처 13개의 의미 대조를 새로 실행했다고 보고하지 않는다.

## 3. 실제 실행 결과

저장소 루트에서 아래 명령을 실행했다. manifest는 그 전에 커밋되어 있었고, receipt의 `source.dirty`는 `false`다.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m workbench run reference-audit discovery
```

| 항목 | 관측 |
| --- | --- |
| 실행 ID | `20261119T135149Z-7f42efebea05` |
| 실행 위치 / Python | ChatGPT 제공 Linux 클라우드 작업공간 / 3.12.14 |
| runner / 자식 명령 종료 코드 | 0 / 0 |
| receipt 상태 / 시도 수 | `passed` / 1 |
| stdout | `ok: true`, `errors: []`, 인식된 고유 출처 ID 13개 |
| 추가 진단 | `unused: []`, `duplicate_repository_sources: {}` |
| 검사 경계 | `claim_truth_checked: false`, `network_accessed: false` |
| stderr | 0바이트 |
| 입력 변경 감지 | `tracking_error: null`; 실행 전후 선언 입력·HEAD 변경 감지 없음 |
| receipt 재검사 | `verify-receipt` 종료 코드 0, `status: matched` |

반환된 receipt 경로를 읽고 세 원본 파일을 `execution/`에 바이트 그대로 복사했다. 해시를 대조했고, 증거 커밋의 네 파일을 GitHub에서 다시 읽어 로컬 내용과 같음을 확인했다. 임시 `.workbench/runs/` 경로만 인계하지 않는다.

이 실행은 GitHub Actions 실행이 아니며 사용자 Codex 계정으로 위임된 실행도 아니다. `workflow_run`은 `null`이다. 내부 검사 코드의 실제 실행 결과를 외부 후보 실행의 D3/D4 근거로 올리지 않는다.

## 4. 성공이 확인하는 것과 확인하지 않는 것

[project.json의 `tasks.discovery`](https://github.com/laadkke-arch/agentflow-open/blob/8ca328516facff584589c9bf7040062b8695398d/lab/reference-audit/project.json)는 `lab/reference-audit`에서 `task.py fixtures/discovery.json`을 실행한다. [`audit()`](https://github.com/laadkke-arch/agentflow-open/blob/8ca328516facff584589c9bf7040062b8695398d/lab/reference-audit/task.py)의 진입부가 읽는 것은 fixture의 `document`와 `sources`다. `case_path`는 조사 원본을 실제로 여는 지시가 아니다.

| 결과 | 허용되는 해석 | 확대하면 안 되는 해석 |
| --- | --- | --- |
| `ok: true`, `errors: []` | 등록 ID 형식·중복과 인식된 표식의 미등록 ID 오류가 없었다. | 모든 주장에 인용이 있고 인용 문장이 참이다. |
| `used` 13개, `unused: []` | 등록한 13개 ID가 인식 가능한 표식에 등장했다. | 모든 원문·주장이 빠짐없이 포함되거나 근거가 충분하다. |
| `duplicate_repository_sources: {}` | 지원하는 GitHub 저장소 루트 URL에서 중복 그룹이 검출되지 않았다. | 파일·문서·이슈·외부 URL을 포함한 모든 출처에 중복이 없다. |
| receipt `passed` | 자식 종료 코드 0이고 선언 입력 해시·HEAD 변경이 감지되지 않았다. | runner가 stdout JSON의 의미나 충분성을 검증했다. |
| `verify-receipt: matched` | 현재 선언 입력과 동봉 로그의 해시가 receipt와 일치한다. | 실행을 재현했거나 receipt의 진위를 인증했다. |

잘못된 형식의 인용 표식과 인용 없는 주장은 `audit()`가 완전성 검사하지 않는다. `checked_at_utc`, `level`, `revision`, `schema`, `case_path`의 의미·정합성도 판정하지 않는다. 미사용 출처·저장소 루트 중복은 정보 출력이며 실패 조건이 아니다. 루트 URL 판정의 범위는 [`repository_key()`](https://github.com/laadkke-arch/agentflow-open/blob/8ca328516facff584589c9bf7040062b8695398d/workbench/urls.py)에 제한된다.

[실행기의 `tracked_inputs()`, `run_task()`, `verify_receipt()`](https://github.com/laadkke-arch/agentflow-open/blob/8ca328516facff584589c9bf7040062b8695398d/workbench/cli.py)도 직접 읽었다. receipt의 입력 10개에는 실행하지 않은 `test_task.py`가 포함된다. 해시 목록에 있다는 이유로 단위시험을 실행한 것으로 세지 않는다. 반대로 조사 원본·HANDOFF·manifest·의존 SHA는 이 입력 목록에 없다. 원본 해시는 별도로 보존하고 작업 계약은 별도 명령으로 확인했다.

`verify-receipt()`는 현재 HEAD와 `source.commit`의 일치를 요구하지 않으며, dirty checkout도 그 사실만으로 거절하지 않는다. 이번 실제 실행은 별도로 `8ca328…`와 `dirty: false`를 확인했다. 후속 문서 커밋까지 그때 실행했다고 쓰지 않는다.

`claim_truth_checked`와 `network_accessed`는 `audit()`가 고정 반환하는 필드다. 읽은 검사 코드에 네트워크 요청은 없지만 이를 패킷 관측·OS 격리의 증거로 해석하지 않는다. GitHub 읽기·fetch·저장은 네트워크를 사용하는 별도 작업이다.

## 5. 독립 검토와 연결 시험의 판정

별도 읽기 전용 내부 에이전트가 고정 커밋의 선행 HANDOFF, fixture·project, `audit()`, `repository_key()`, 실행기·receipt 검사기를 독립 정적 검토했다. 선행 인계 해석에서 실행을 막을 오류는 찾지 못했다. 표식 누락, 정보성 진단, 실행하지 않은 테스트의 입력 해시, receipt 진위·HEAD 한계, 네트워크 플래그 한계를 위에 보완했다. 이 검토를 새 웹 Pro 세션 생성 시험으로 세지 않는다.

| 완료 조건 | 이 작업이 남긴 증거 / 남은 경계 |
| --- | --- |
| GitHub 인계로 내용 복구 | 고정 HANDOFF·REVIEW·VERIFICATION 직접 열람, 목적·다음 명령 복원, 의존 SHA 고정. |
| 실제 클라우드 검사 | 커밋된 입력에서 discovery 1회, 원본 receipt·stdout·stderr 보존. |
| 결과 검토 | 출처 연결 성공과 사실·서비스 검증의 차이를 코드와 출력으로 구분. |
| 원격 결과 커밋 | manifest·실행 증거는 원격 재열람 완료. 최종 인계 커밋은 HANDOFF 저장 뒤 진행 담당이 확인한다. |
| 두 번째 실제 웹 Pro 세션 / 선택 모델 | 이 세션에 제공된 모델 표기는 `GPT-6 Astra Pro`. Dot의 배정·세션 생성·모델 선택 UI와 두 세션의 별도 식별은 직접 관측하지 않았으므로 진행 담당의 기록 대조가 필요하다. |
| PC 종료 후 지속 실행 | PC 종료 시각·오프라인 상태를 관측하지 않았다. 이 실행은 사용자 PC를 사용하지 않았다는 범위까지만 확인했다. |

작업 자료 복원·실행·저장에 장애는 없다. 외부에서만 확인 가능한 연결 증거를 완료로 승격하지 않고 `REVIEW_READY`로 인계한다. `dot-control.json`과 공통 상태·색인은 변경하지 않았다.

## 6. 다음 행동과 색인 제안

진행 담당은 최종 HANDOFF 커밋과 실행 증거를 읽고, 자신의 비공개 배정 기록에서 AF-DOT-001과 AF-DOT-002의 세션 식별·선택 모델을 대조한다. 확인한 범위만 진행표에 기록하고 두 작업 연결 시험을 마친다. PC 종료 후 지속 실행은 종료 시각 이후의 생성·실행·커밋 시각을 별도로 대조할 자료가 있을 때만 판정한다.

코드와 입력이 그대로라면 전체 검사나 discovery를 다시 실행할 필요는 없다. 필요 시 저장된 receipt를 `verify-receipt`로 대조하고 자기 manifest를 개별 `check --fetch`한다. 이 폴더의 manifest는 기본 `check-all`이 자동 발견하지 않는다.

색인 담당자에게 제안할 행: `AF-DOT-002 | GitHub 인계 복원 및 discovery 실측·검사 경계 | 실행·검토 완료, 세션 배정 증거는 진행 담당 확인 | docs/workstreams/dot-trial/AF-DOT-002/RESULT.md | 의존 ba62d1fa…, 실행 8ca32851…`. 새 제품 연구나 세 번째 작업은 배정하지 않는다.
