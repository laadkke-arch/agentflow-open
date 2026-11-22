# AF-RES-042 · HANDOFF

**수용 준비 완료.** CPython 3.10.6의 별도 pandas 1.4.4와 1.5.2 환경에서 최초 실행과 빈 환경 재생을 완료했다. 내용 수용 조건 15/15를 충족했다. 외부 1차 원문 31개를 직접 확인했고, 원 드라이버는 P04 6개·P06 8개 메서드를 각 두 번 실행했다. 독립 typed 관측 43/43행이 두 번 같았다. [고정 결과](https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/RESULT.md) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/evidence/acceptance-evidence.json)

- P04의 DMY는 문제 batch에서 1월 12·13일을, 고정 MDY는 두 번째 입력의 `ValueError`를 냈다. 1.4.4 구형 infer는 같은 batch에서 12월 1일과 1월 13일을 경고 없이 함께 반환했다. 예상 실패 1/1과 예상 밖 성공 0/1이 매회 확인됐다. [P04 원로그](evidence/logs/F-P04.driver.json) · [관측 L2–19](probe-results.csv#L2-L19)
- P06의 native guard·nullable 생성 대안은 float `3.0`을 손실 없이 저장하고, `1.5`와 `'potage'`의 각각의 오류 뒤 `[1,2,3]` 및 선언 dtype을 보존했다. 기본 Series의 float/object 승격과 NumPy·`int()`의 `1.5→1` 절삭을 관측했다. 예상 실패 3/3과 예상 밖 성공 0/3이 매회 확인됐다. [P06 원로그](evidence/logs/F-P06.driver.json) · [관측 L20–44](probe-results.csv#L20-L44)
- 독립 진단에서 무관한 연산 오류도 expectedFailure로 세어질 수 있고, ordinary test가 이를 오류로 보고한다는 점을 재현했다. import 차단 진단은 원 시험 시작 전 종료 2였다. 평가자 주석에서 P04-R3의 오류 위치 증거와 P06-R2의 실제 값 변화 증거를 보강했다. 038 작성 예시의 대응 채점 셀 18/18은 유지됐다. [루브릭 제안](rubric-delta.csv) · [자체 점검 Q5](SELF_CHECK.md#q5--expectedfailure가-다른-이유로-통과하는-반례)

색인 제안 한 줄. **AF-RES-042 — pandas 1.4.4 날짜와 1.5.2 정수의 공개판 API 재현, 최초·빈 환경 2/2, typed 관측 43/43, 원문 31개. P04 정상 거부와 혼합·P06 값/타입/오류 후 상태 구별, 채점 주석 두 곳 제안.**

## 고정 결과와 원격 커밋

저장소는 `laadkke-arch/agentflow-open`, 브랜치는 `work/research-af-res-042`, 결과 고정 SHA는 `b0675fce25d8889df12f34953c885e61bd1232c9`다. 작업 ID는 AF-RES-042 시도 1, 유일한 소유 경로는 `docs/workstreams/research/AF-RES-042/`다. 배정 직후 브랜치를 만든 SHA는 `65c60c084fe29047670ae40534939eb23c3e8fb5`이며 session start와 check의 통합 SHA는 `333e83c9a46b0c005d22efcccbb5a055b27e904e`다. 그 사이 통합판에 진행표 기록 한 건이 추가됐다. 의존은 AF-RES-038@ `5a1699b24679cd7c58242cb98c40fa9fc9c6851a`다. 관리 Linux에서 Codex 셸·GitHub를 사용했다. 세션 지침에 표시된 모델 family는 GPT-6이며 정확한 variant·effort는 미확인이다. [작업 manifest](manifest.json)

| 작업 묶음 | 원격 SHA와 변경 범위 |
| --- | --- |
| ① 실행 전 봉인 | [e8352f3e51ece2d2a9f58cfa93f1c48941dbc2d5](https://github.com/laadkke-arch/agentflow-open/commit/e8352f3e51ece2d2a9f58cfa93f1c48941dbc2d5) · manifest, 43 typed 행, 원 드라이버, 출처와 환경 계약 |
| ② 설치·최초 실행 | [40568504f9688376f3be8f59d7c1330d46c476da](https://github.com/laadkke-arch/agentflow-open/commit/40568504f9688376f3be8f59d7c1330d46c476da) · 배포 해시, 환경 지문, 최초 원로그, 실행 진입점 |
| ③ 반례와 빈 환경 재생 | [ad3c9c319d98743dec67e0000d5d8d2d71dec29d](https://github.com/laadkke-arch/agentflow-open/commit/ad3c9c319d98743dec67e0000d5d8d2d71dec29d) · 재생 원로그, first/replay `comparison.json`, 비교 CSV, 분야별 원문과 수치 |
| ④ 결과 및 수용 고정 | [b0675fce25d8889df12f34953c885e61bd1232c9](https://github.com/laadkke-arch/agentflow-open/commit/b0675fce25d8889df12f34953c885e61bd1232c9) · 결과 표, 루브릭, 자체 점검과 내용 수용 15개 |
| 마지막 인계 | 고정 결과를 부모로 하는 이 파일의 단독 커밋 |

| 빠른 판독 | 고정 파일·행 |
| --- | --- |
| 필수 표 1 · 43 입력행 | [RESULT L3–47](https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/RESULT.md#L3-L47) |
| 필수 표 2 · 두 환경과 짝 분모 | [RESULT L49–52](https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/RESULT.md#L49-L52) |
| 마지막 약점 세 행 | [RESULT L91–95](https://github.com/laadkke-arch/agentflow-open/blob/b0675fce25d8889df12f34953c885e61bd1232c9/docs/workstreams/research/AF-RES-042/RESULT.md#L91-L95) |
| 실제 명령·해시·종료코드·원로그 위치 | [실행 원장 L1–111](evidence/runs.jsonl#L1-L111) · [환경 선택·지문](environments.json) · [같은 바이트 비교](evidence/comparison.json) |
| 채점, 미확인, 출처 | [루브릭 L2–7](rubric-delta.csv#L2-L7) · [출처 78행](sources.jsonl) · [자체 점검 Q1–Q7](SELF_CHECK.md) · [수용 원장 A01–A15](evidence/acceptance-evidence.json#L11-L426) |

## 고정 SHA 재독과 계약 검사

GitHub에서 2026-11-22T20:35:37.498Z에 결과와 수용 원장 전체를 `b0675fce25d8889df12f34953c885e61bd1232c9`로 다시 열었다. 두 blob이 checkout의 SHA와 2/2 일치했다. 원격 결과의 43행·2환경·마지막 약점 3행과 수용 원장의 15/15도 확인했다.

| 파일 | 재독 Git blob SHA |
| --- | --- |
| `RESULT.md` | `0b0fd03dc810669c789f45adb10a312553e28efb` |
| `evidence/acceptance-evidence.json` | `4d067908f5f4cabba1b98cd163745e44c8f7fe1d` |

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-042/manifest.json --fetch
```

```json
{
  "exit_code": 0,
  "status": "passed",
  "freshness": "remote_checked",
  "checked_at": "2026-11-22T20:35:44.422032+00:00",
  "checked_out_commit": "b0675fce25d8889df12f34953c885e61bd1232c9",
  "task_base_commit": "65c60c084fe29047670ae40534939eb23c3e8fb5",
  "integration_commit": "333e83c9a46b0c005d22efcccbb5a055b27e904e",
  "scope_base_commit": "65c60c084fe29047670ae40534939eb23c3e8fb5",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths_count": 40,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "stderr_bytes": 0,
  "stdout_sha256": "85c80d13362dce640605f58107e909b4bd913b3f9a139f20e00dba6e73e9e4e8"
}
```

이 검사는 원격 최신성과 Git 계약·소유 경로에 대한 것이다. 차이 검사에서 고정 원 드라이버의 마지막 빈 줄은 원 상태 그대로 유지했다. 결과·수용 snapshot에 있는 Z01·Z02의 후속 증거는 이 절의 재독과 실제 검사다. Z03의 후속 증거는 이 파일만 추가한 마지막 커밋과 부모 대비 경로다.

## 재개용 명령·입력

같은 공개 배포판으로 다시 확인할 경우 저장소 root에서 한 번 새 실행·비교를 시작할 수 있다. 실제 두 실행과 비교의 각 명령은 [환경 명세](environments.json)의 `observed.commands`에 있다.

```sh
docker pull --platform linux/amd64 docker.io/library/python@sha256:c8ef926b002a8371fff6b4f40142dcc6d6f7e217f7afce2c2d1ed2e6c28e2b7c
python -B docs/workstreams/research/AF-RES-042/run_replay.py --round both --out "$(mktemp -d)/af042-rerun"
```

입력은 `inputs.jsonl`의 세 날짜 batch와 index·타입이 고정된 다섯 정수 대입이다. `upstream/replay_api_contracts.py`의 SHA-256은 `de8bad4712e00e626cccf3a6f3c6974c6c1f0797e0d91b5a2fdeb41e63bb709f`다. 두 환경의 설치 4/4, import 4/4, 원 테스트 시작 4/4, 의미 일치 4/4를 확인했다. 내용 수용 미충족은 0건이다. 최초 저자의 운영 잠금, 개별 LOC 원 MARC 046의 인코딩, 사람 채점·시간·재작업은 미확인이다. 개별 원 MARC를 필요로 할 때 첫 자료는 LOC CSV의 LCCN 2018653939·2017796981에 있는 MARCXML 링크다. [미확인 원장](evidence/acceptance-evidence.json#L467-L501) · [두 기록 ID](evidence/domain-cases.json)

## 가장 중요한 후속 조사

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| 1. 제안자 실행 환경의 잠금과 실행 기록 미확인 | 결론은 선택한 두 공개판에 해당한다. PyPI의 업로드 도구 CPython은 P04 3.10.5, P06 3.10.6이다. PDEP-6 최초판의 토론 링크는 별개 이슈로 이어진다. [P04 wheel](https://pypi.org/project/pandas/1.4.4/#files) · [P06 wheel](https://pypi.org/project/pandas/1.5.2/#files) · [실제 PDEP-6 PR](https://github.com/pandas-dev/pandas/pull/50424) · [출처 UP04/UP06/PX2](sources.jsonl) | PDEP별 예시의 최초 실행 환경을 확인할 version dump나 lock을 찾는다. 첫 자료는 [PDEP-4 토론](https://github.com/pandas-dev/pandas/pull/48621)과 [PDEP-6 토론](https://github.com/pandas-dev/pandas/pull/50424)의 작성자 코드·로그다. | 원 실행에 다른 버전·의존판·ABI가 확인되면 해당 환경에서 동일 typed 입력을 별도로 재실행한다. 결과가 다르면 역사적 해석을 수정한다. |
| 2. private helper와 입력 범위의 제한 | DMY/MDY의 non-ISO·무결측 batch와 작은 scalar만 실측했다. nullable 생성 대안은 기존 native 계약 교체에 직접 적용되지 않는다. [datetime 분기 L375–410](https://github.com/pandas-dev/pandas/blob/ca60aab7340d9989d9428e11a51467658190bb6b/pandas/core/tools/datetimes.py#L375-L410) · [masked L198–237](https://github.com/pandas-dev/pandas/blob/8dab54d6573f7186ff0c3b6364d5e4dd635ff3e7/pandas/core/arrays/masked.py#L198-L237) · [자체 점검 Q3/Q4](SELF_CHECK.md) | 해당 요구를 채택할 때 leading missing·ISO 변형 한 건과 int64 표현범위 경계 한 건을 새 분모에서 확인한다. 첫 자료는 pinned API 분기와 이번 CSV의 B1-M, F15-N이다. | 새 사용자 계약에 정밀도·결측·overflow가 포함되거나 후대 버전에서 helper 경계가 달라지면 대안 선택과 채점 근거를 다시 정한다. |
| 3. 독립 사람 채점과 시간·재작업 자료 미확인 | 038의 작성 예시 6개·요구 셀 18개의 실행 대응만 확인했다. [038 예시 L4–9](https://github.com/laadkke-arch/agentflow-open/blob/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038/examples.jsonl#L4-L9) · [루브릭 L2–7](rubric-delta.csv#L2-L7) | 인수 뒤 두 독립 채점자가 원 가림 발췌와 여섯 셀의 수정 주석을 검토한다. 첫 자료는 [038 가림 입력과 측정 기준](https://github.com/laadkke-arch/agentflow-open/tree/5a1699b24679cd7c58242cb98c40fa9fc9c6851a/docs/workstreams/research/AF-RES-038) 및 이 CSV다. | 정상 MDY를 오탈락시키거나 dtype만으로 절삭을 오통과시키면 채점 준비도를 다시 평가한다. 사람 품질·시간 결론에는 별도 관측이 필요하다. |
