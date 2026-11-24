# AF-RES-241 HANDOFF

## 식별과 상태

- 상태 **DONE**. 고정 로컬 여정 16/16, 기존 A2 기대 2개, 별도 브라우저 반례 5예제, 깨끗한 양성·오류 2예제를 관측했다.
- 과제 AF-RES-241 / attempt 1 / codex-cloud. 실행 위치는 관리형 Linux Codex Cloud, 실제 선택 모델의 세부 식별자는 미확인이다.
- 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-241`, 허용 출력 `docs/workstreams/research/AF-RES-241/`.
- 시작 SHA `64e139f16309e41e30f9ec634eabe17fef908bbd`. 요청 URL의 계획판 `914dbfa789ebec97063ed97130ea2a71c2e9f503`에서는 해당 ID가 없었다. 착수판에서 지정 브랜치/경로, RUNNING / 1, 단일 선행 AF-RES-223을 확인했다.
- 선행 중앙 DONE / result_commit `27518e859181f0ece5de42dc54844d5b83688b7a`. 그 HANDOFF의 PARTIAL 및 실제 본문 결과판 `c3895c3c8ad5a7be5c94cfa112ca89ac456c18b6`을 별도 보존했다. [선행 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/27518e859181f0ece5de42dc54844d5b83688b7a/docs/workstreams/research/AF-RES-223/HANDOFF.md)
- 고정 검증 결과 `bdc7c52ba9364c29997bd70c89752a026bd732e2`. 마지막으로 이 파일만 추가하는 커밋의 부모이자 아래 모든 결과·검사의 SHA다. 최종 결과판 재열람과 검사 시간은 2026-11-24T23:39:55Z–23:40:03Z다.

## 결과와 대표 근거

| 산출물 | 재사용할 근거 |
| --- | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/bdc7c52ba9364c29997bd70c89752a026bd732e2/docs/workstreams/research/AF-RES-241/RESULT.md) | 필수 표 1·2, Q1–Q7, 마지막 약점 3건 |
| [journeys.csv](journeys.csv) · [controls.csv](controls.csv) | 16개 기본 여정·13개 대조 항목과 정상 route/런타임 영수증 |
| [sources.jsonl](sources.jsonl) · [SELF_CHECK.md](SELF_CHECK.md) | 109행 중 직접 열어 읽은 별개 원저작 78, 산입 계보 66, 실패 경로 기록 6. 관측·결측·범위 밖 집계 |
| [SCOPE.md](SCOPE.md) · [session.json](session.json) · [environment.json](environment.json) · [fixtures.md](fixtures.md) | 원표본/사전 예측, 실제 start 계약, 고정 Git/이미지 지문과 합성 입력 |
| [replay/README.md](replay/README.md) · [receipts/](receipts/) | 실행 명령, 버전·exit·stdout/stderr, 실제 DOM/AX/모델·초점, 실패 및 깨끗한 재생 |

같은 화면의 고정 두 Change는 네 화면에서 공존했고 Chromium AX suffix로 구별됐다. 16/16 첫 href·필드·저장/무저장과 실제 복귀를 확인했다. 저장 8/8에서 목표 의미값을 확인했다. 모델에서 목표 속성만 바뀐 건은 3/8이었다. 16/16 원 URL 복귀에도 R1-1은 course 섹션이 접혔다. A3-2 주소 유형을 그대로 제출하고 Back하면 나라 값이 빈 상태로 남는 반례도 있다. [R1-1](receipts/journeys/R1-1-S.json) · [A3 중간 제출](receipts/controls/C-A3-MID.json)

같은 참조 이름의 두 객체는 AX 원문이 같고 실제 ID가 달랐다. Register의 두 피드백 링크는 AX 이름이 다르고 공통 URL·같은 네 의미 입력과 BODY로 들어갔다. 도서관은 공개 서지 2/2에서 동일 예약 표시와 다른 레코드를 확인했고, 같은 연도의 별도 판은 대출로 표시됐다. [중복 참조](receipts/controls/C-A1-DUP.json) · [공유 양식](receipts/controls/C-R-F1.json) · [도서관](receipts/controls/library.json)

## 고정 결과판 실검사

아래 명령을 새 GitHub clone의 `bdc7c52ba9364c29997bd70c89752a026bd732e2`에서 실행했다. Python 3.12.14, 시작·종료 모두 깨끗한 checkout이다.

| 명령 | 종료·관측 | 범위 |
| --- | --- | --- |
| `python -m workbench.session check docs/workstreams/research/AF-RES-241/session.json --fetch` | exit 0, passed, remote_checked, outside_paths 및 unmerged_paths 빈 배열 | 고정 계약/선행 SHA/허용 범위. 조회 시 통합 SHA 02ff9f0a112a32842015386d94db104b582d5f57의 착수판 이후 차이는 중앙 진행표뿐 |
| `python scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit 0. doctor, acceptance, research-case, original-smoke 내부 exit 0 | 포함된 `scripts/check.py --require-git`의 공통 시험 55, 기존 두 lab 7·9, export 2개, Git bundle 복원, 원본 smoke와 출처 연결 확인. 전체 검사의 check-all은 `no_active_sessions` / not-executed. 위의 명시적 단일 계약 검사가 과제 pin을 확인 |
| `python docs/workstreams/research/AF-RES-241/replay/validate.py` 및 summarize CSV 재생 후 `cmp` | exit 0 각각 | 필수 경로, 16 여정·8 S/B 초기 요약행 동치, 13 controls, 근거 ID, 원장 하한, 첫 두 표·Q1–Q7·끝 3건 확인 |
| `git diff --exit-code 64e139f16309e41e30f9ec634eabe17fef908bbd HEAD -- docs/automation/dot-control.json` | exit 0. 소유 경로 외 diff 0개 | 체크아웃 결과판의 tracked 변경 146파일 모두 owned_path |

실제 stderr는 session/cloud/audit 세 명령 모두 비어 있었다. stdout 전체 SHA-256은 session `62f7211ce8ac9690a57c98303c8264efd5be900025753f26b1b2eeb4a84cdfe2`, cloud `107f5d3a279af463975fce1cc5a191a659003b22ba665f8f6bbd63b505deb4f0`, audit `0c2282c8db1c66ebace9d6854dc62059a75b2ae2e36fa8f9a3fe6c0c4ecd1506`이다. 검사 핵심 stdout은 다음과 같다.

```text
session: passed, remote_checked, outside_paths=[], unmerged_paths=[], errors=[]
cloud: passed, exit_code=0, checked_out_sha=bdc7c52ba9364c29997bd70c89752a026bd732e2, require_clean=true
cloud session_validation: not-executed, no_active_sessions, count=0
{"control_rows": 13, "count_by_category": {"library": 10, "route_form_fixture": 35, "standard": 5, "test_setup": 10, "view": 18}, "counted_lineages": 66, "counted_works": 78, "journeys": 16, "ledger_rows": 109, "same_initial_summary_pairs": 8, "source_and_result_checks": "passed", "tab_max": 20, "tab_min": 12}
```

Apply 초기 radio 선택 오류 3건, Register 초기 날짜 검증 오류 1건, 설치 시도 오류를 원영수증으로 보존했다. 화면 조건과 입력을 고정하고 회복했다. 최종 Apply 12예제 및 Register 4예제, 새 DB 양성·오류 2예제의 exit는 각각 0이다. 고정 결과판 자체 검토는 실시했고 독립 검토는 미실시다. [기본 실행](receipts/attempts/) · [깨끗한 재생](receipts/controls/apply-clean-final.stdout)

## 미확인과 다음 첫 행동

스크린리더 실제 발화 및 사용자 선택률, 도서관 두 레코드의 holding·예약 풀·거래는 미확인이다. A2 내부 wizard 객체는 캐시 조회가 nil이어서 확인하지 못했다. 후속 환경에서 다른 브라우저·AT, Register Publish 경로 및 코스 재확인까지 같은 결과일지는 열려 있다.

이 결과를 이용하는 검토자는 고정판 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/bdc7c52ba9364c29997bd70c89752a026bd732e2/docs/workstreams/research/AF-RES-241/RESULT.md)의 마지막 표와 [R1-1](receipts/journeys/R1-1-S.json), [A1 중복](receipts/controls/C-A1-DUP.json)을 먼저 대조한다. 실제 AT 판단이 필요하면 고정 Apply 중복 fixture를 먼저 재생하고, 새 Chromium+NVDA 세션에서 두 Name 링크의 Elements List 발화와 도착 reference ID를 한 관측씩 기록한다. Safari/VoiceOver 등은 별도 입력으로 유지한다.

```bash
git fetch origin work/research-af-res-241
git show bdc7c52ba9364c29997bd70c89752a026bd732e2:docs/workstreams/research/AF-RES-241/RESULT.md
git show bdc7c52ba9364c29997bd70c89752a026bd732e2:docs/workstreams/research/AF-RES-241/receipts/controls/C-A1-DUP.json
```

색인 반영 제안은 AF-RES-241 DONE / 고정 결과 `bdc7c52ba9364c29997bd70c89752a026bd732e2` / 여덟 앵커 16개 브라우저 여정 / AF-RES-223 선행 핀 / [결과와 대조](RESULT.md)다. 진행표 갱신은 통합 담당에게 넘긴다.
