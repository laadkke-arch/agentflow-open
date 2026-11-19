# AF-DOT-002 — 다음 세션 인수인계

## 1. 식별

- 작업 ID / 시도 / 상태: `AF-DOT-002 / 1 / REVIEW_READY`.
- 작업 종류: `web-pro-new-session`. 세션에 제공된 모델 표기: `GPT-6 Astra Pro`.
- 실제 실행 위치: ChatGPT 제공 Linux 클라우드 작업공간, Python 3.12.14. GitHub Actions·사용자 Codex 계정 실행으로 표시하지 않는다.
- 공개 조회 참조: `AF-DOT-002#1`, 저장소·브랜치. 비공개 대화 URL·서비스 작업 ID는 저장하지 않았다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/dot-trial-af-dot-002`.
- 시작 SHA: `34f108b9f4e4680943f1cf58fe2ded7d25f47aba` — 생성 직전 확인한 `chore/workspace-foundation` head.
- 의존 작업 / 결과 SHA: `AF-DOT-001` / `ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea`.
- 마지막 확인·원격 재열람 커밋: `2976e24b951687b8ec74d602e4c768057e39d3f7`.
- 인계 직전 실제 검사 시각: `2026-11-19T13:56:08.320498+00:00`.
- PR: 생성하지 않음.
- **최종 결과는 이 HANDOFF를 추가한 커밋이다.** 진행 담당은 저장 후 작업 브랜치 head와 이 파일을 다시 읽고 그 정확한 SHA를 `result_commit`에 고정한다. 위 직전 커밋이나 실제 실행 커밋을 최종 결과와 혼동하지 않는다.

자료 복원·실행·저장에 장애는 없다. Dot의 두 세션 생성·별도 식별·모델 선택 UI와 PC 종료 후 지속 실행은 이 작업에서 직접 관측하지 않았다. 이 외부 관측이 남았으므로 연결 시험 전체를 무조건 완료로 표시하지 않는다.

## 2. 사용자 요구 / 작업 범위

지정된 다섯 문서와 진행표 AF-DOT-002 항목을 GitHub에서 직접 읽었다. 진행표가 지정한 선행 결과의 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/HANDOFF.md), REVIEW, VERIFICATION 및 참조 파일에서 목적·남은 작업을 복원했다. 이전 AF-DOT-001 채팅 원문을 요청하거나 읽지 않았다.

복원한 과제는 **기존 reference-audit discovery를 실제 실행하고, 출처 연결 검사와 사실 검증의 차이를 기록하는 것**이다. 새 후보·제품 전체 조사나 구현은 시작하지 않았다.

작업 브랜치가 없음을 확인한 뒤 최신 통합 커밋에서 만들었다. AF-DOT-001의 미통합 결과 위에서 만들지 않았다. 허용 쓰기 경로는 `docs/workstreams/dot-trial/AF-DOT-002/` 하나다. `dot-control.json`, 공통 문서·색인·계약, 검사기·fixture·제품 코드를 수정하지 않았다. main·통합 브랜치 병합, 기존 AgentFlow Studio 변경, 배포·유료 자원·자동 작업 생성은 하지 않았다.

## 3. 실제 변경과 커밋

| 파일 | 변경 / 확인 |
| --- | --- |
| [manifest.json](manifest.json) | 시작 SHA·계약 v2·허용 경로·AF-DOT-001 의존 SHA를 `session start --fetch`로 고정. |
| [execution/receipt.json](execution/receipt.json) | 실제 discovery 실행기가 반환한 원본 receipt. |
| [execution/stdout.txt](execution/stdout.txt) | 원본 출력: 출처 ID 13개, 오류 없음, 사실 검증 미실시. |
| [execution/stderr.txt](execution/stderr.txt) | 원본 0바이트 로그도 보존. |
| [VERIFICATION.json](VERIFICATION.json) | 실행 명령·환경·해시·복원 입력·receipt 검사·초기 계약 검사·관측 한계. |
| [RESULT.md](RESULT.md) | 실행 결과 해석, 코드 근거, 독립 검토, 연결 시험의 남은 관측, 색인 제안. |
| `HANDOFF.md` | 마지막 커밋의 인계 파일. |

저장 순서:

1. `8ca328516facff584589c9bf7040062b8695398d` — manifest. 이 깨끗한 커밋에서 discovery를 실행했다.
2. `cd65bfd3119f8905c5244640c1805bfb3bfa20b5` — receipt·stdout·stderr·VERIFICATION.
3. `2976e24b951687b8ec74d602e4c768057e39d3f7` — 결과·검사 경계 검토.
4. 이 HANDOFF 추가 커밋 — 최종 인계.

1~3의 파일을 GitHub에서 다시 읽어 로컬과 일치함을 확인했다. 독립 검토자는 최종 RESULT·VERIFICATION·manifest·로그의 수치와 SHA 구분을 대조했고 수정할 과장·혼동을 찾지 못했다. 내부 독립 검토는 새 웹 Pro 세션 교체의 증거가 아니다.

manifest는 사용자 지정 경로를 우선해 이 폴더에 만들었다. 기본 `check-all`은 이를 자동 발견하지 않으므로 **개별 `check`**를 사용한다.

## 4. 실제 검증 결과

| 실제 명령 / 확인 | 대상과 결과 |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench context reference-audit --query discovery` | 시작 SHA에서 exit 0. BRIEF·STATE·fixture 읽음, omitted 없음. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session start af-dot-002 --allow docs/workstreams/dot-trial/AF-DOT-002/ --output docs/workstreams/dot-trial/AF-DOT-002/manifest.json --dependency work/dot-trial-af-dot-001=ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea --fetch` | 시작 SHA에서 exit 0, `remote_checked`. |
| `git diff ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea HEAD -- docs/research/discovery-case-2026-11-19.json lab/reference-audit workbench` | 실행 전 관련 파일 차이 없음. 이후 이름 목록으로도 다시 확인. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench run reference-audit discovery` | `8ca328516facff584589c9bf7040062b8695398d`, `dirty: false`, runner·자식 exit 0, 1회. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench verify-receipt reference-audit docs/workstreams/dot-trial/AF-DOT-002/execution/receipt.json` | 복사된 원본 입력·로그 해시 일치, exit 0, `matched`. |
| `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/dot-trial/AF-DOT-002/manifest.json --fetch` | 최초 증거 파일 보존 시와 아래 인계 직전 커밋에서 각각 exit 0. |
| `git diff --check 34f108b9f4e4680943f1cf58fe2ded7d25f47aba HEAD` | `2976e24b…`에서 exit 0. 전체 변경 경로 6개가 허용 폴더 안이고 checkout은 clean. |
| `dot-control.json` blob 대조 | 시작 SHA와 `2976e24b…`의 blob `94e00b7ed7df71a200f8156abe695620b78ead9a` 동일. |

실행 ID는 `20261119T135149Z-7f42efebea05`다. stdout의 `ok: true`, `errors: []`, `used` 13개, `unused: []`, `duplicate_repository_sources: {}`를 직접 읽었다. `claim_truth_checked: false`, `network_accessed: false`를 보존했다. stderr는 0바이트다.

직접 실행 입력은 `lab/reference-audit/fixtures/discovery.json`이며 SHA-256은 `52f87db095173ee92dad09d034dbc3b3176274988a87f80787127ccdd36a3c90`이다. 조사 원본 `docs/research/discovery-case-2026-11-19.json`은 실행기가 읽지 않으므로 SHA-256 `1341689b4c7554bebd7185ff6e93b714824feae00a57f9d148b7974192099c0f`을 VERIFICATION에 별도로 보존했다. 둘 다 선행 인계와 같다.

인계 직전 개별 계약 검사:

```json
{
  "returncode": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "checked_at": "2026-11-19T13:56:08.320498+00:00",
  "checked_out_commit": "2976e24b951687b8ec74d602e4c768057e39d3f7",
  "integration_commit": "34f108b9f4e4680943f1cf58fe2ded7d25f47aba",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": []
}
```

이 계약 검사는 3번 커밋의 manifest·증거·결과 문서를 대상으로 한다. **마지막 HANDOFF 커밋은 이 검사보다 뒤에 생성된다.** 최종 저장 뒤의 원격 head·파일 재열람 및 경로 확인과 구별한다. discovery를 후속 문서 커밋에서 재실행한 것으로 쓰지 않는다.

## 5. 판단·근거·미확인

출처 ID 연결 검사는 통과했다. 다만 잘못된 형식의 표식, 인용 없는 주장, 원본과 fixture의 의미 동기화, URL 생존·원문 의미·현재 조건·후보 적합성은 검사하지 않는다. 미사용 출처와 저장소 루트 중복은 실패 조건도 아니다. 코드 근거와 최소 해석은 [RESULT §4](RESULT.md#4-성공이-확인하는-것과-확인하지-않는-것)에 있다.

receipt의 입력 10개에 `test_task.py`가 있어도 이번에 단위시험을 실행한 것은 아니다. `verify-receipt`는 해시 일치 검사이며 실행 진위·검사 충분성·현재 HEAD와 실행 SHA의 동일성을 보증하지 않는다. 네트워크 플래그도 패킷 관측이나 격리 검사의 결과가 아니다.

**미실시:** 전체 cloud_check·단위시험·export·bundle 복원 반복, 외부 후보 API·접근 권한·현재 약관·운영·제품 통합 확인, Dot의 생성·모델 선택 UI 관측, 두 웹 Pro 세션의 독립 식별 확인, PC 종료 후 지속 실행 관측. 코드 변경이 없어 전체 검사를 반복하지 않았다.

기존 후보 판단·미확인은 선행 검토 수준으로 유지한다. 새로운 외부 사실이나 이용 허가로 승격하지 않았다. 색인 변경은 RESULT의 제안으로 남겼으며 공통 문서에 직접 반영하지 않았다.

## 6. 다음 첫 행동

**진행 담당 Dot이 `work/dot-trial-af-dot-002`의 head와 그 커밋의 이 HANDOFF·receipt를 다시 읽고, 정확한 최종 SHA를 AF-DOT-002 결과에 고정한다.** 이 작업자는 `dot-control.json`을 수정하지 않는다.

1. 입력은 이 HANDOFF를 추가한 최종 커밋, 의존 결과 `ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea`, 실제 실행 SHA `8ca328516facff584589c9bf7040062b8695398d`다. 실행 SHA 이후의 변경은 증거·결과·인계 문서뿐인지 대조한다.
2. 진행 담당 자신의 비공개 배정 기록에서 AF-DOT-001과 AF-DOT-002가 서로 다른 실제 웹 Pro 세션인지, 실제 선택 모델이 무엇인지 확인한다. 이 파일의 모델 표기만으로 UI 관측이 완료됐다고 쓰지 않는다.
3. 확인된 복원·실행·커밋·세션 배정 증거만 진행표와 시험 결과에 반영한 뒤 두 작업 연결 시험을 끝낸다. 확인할 배정 기록이 없다면 해당 항목만 미확인으로 남긴다. PC 종료 후 지속 실행은 종료 시각·후속 생성/실행/커밋 시각을 실제로 대조할 자료가 있을 때만 판정한다.
4. 새 제품 연구·세 번째 작업·새 예약·배포를 자동 시작하지 않는다. 이번 산출물을 수락하는 데 추가 비용·권한·사용자 PC 설치는 필요 없다.

필요한 경우, 최종 커밋을 읽는 깨끗한 checkout의 저장소 루트에서 다음 두 명령으로 보존 파일과 계약을 확인한다. 명령 실패 시 로그를 보존하고 해당 원인부터 확인하며 검사기나 fixture를 바꾸지 않는다.

```sh
PYTHONDONTWRITEBYTECODE=1 python -m workbench verify-receipt reference-audit docs/workstreams/dot-trial/AF-DOT-002/execution/receipt.json
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/dot-trial/AF-DOT-002/manifest.json --fetch
```

discovery 재실행이 필요한 구체적인 입력·코드 변경이 생긴 경우에만 `python -m workbench run reference-audit discovery`를 새 실행으로 수행하고 새로운 SHA·receipt를 보존한다. 기존 검증 결과를 새 커밋의 실행으로 덮어 쓰지 않는다.
