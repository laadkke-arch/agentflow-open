# AF-RES-080 인계

**PARTIAL · 시도 1 · Codex Cloud.** 자연 120이슈와 닫힌 교정 200이슈의 생성 UTC·순번을 GitHub의 두 경로에서 대조했다. 최초 확보본에서 자연 6자리와 교정 5자리를 판독했고 Click 교정 셋째는 공석이다. 최초 게시판 미복원으로 엄격 48셀은 모두 `unknown`이다. 교정 후보에서 정확 성공 배포판은 0/5 확인됐다. [결과와 세 표](https://github.com/laadkke-arch/agentflow-open/blob/cece879e89d670a50dc64b309cb18c2f2745e60c/docs/workstreams/research/AF-RES-080/RESULT.md)

최초 확보본의 참조판 범위 대비에서는 양쪽을 판정할 수 있던 자연 5자리 중 1자리, 교정 5자리 중 3자리가 넓은 목록에서 양성이었다. 정식 사분면이 모두 관측된 최초 확보본은 자연 2/6, 교정 0/6이다. 지정한 네 자리에서 참조판의 양성·경계 8/8을 보정 후 관측했고 정확 성공판의 8계획은 미실행이다. AC01의 `slots=False` 경로는 현재판에서 올바른 두 키를 보존하지 못했고, 공식 전용 훅은 보존했다. 첫 실행의 AC02는 계측에서 원문 모듈 스코프를 함수 스코프로 옮겨 종료 1이었다. 그 영수증을 보존하고 보정본에서 같은 기대를 다시 시험했다. [실행 원장](runs.jsonl) · [보정](evidence/fixture-correction.md)

## 고정 이력

저장소 `laadkke-arch/agentflow-open` · 브랜치 `work/research-af-res-080` · 소유 경로 `docs/workstreams/research/AF-RES-080/`. 계획 기준은 `0d2b08431067e8d87212a66ecb27657c65722a59`, 실제 브랜치 출발·세션 계약은 `d73c8ec85d375f37451795b575dd7d0e6b2f3594`다. 유일한 연구 입력은 AF-RES-076@`81b8b2c5274d09505b4e98c12ddadde803a323cd`다. [시작 계약과 선행 근거](evidence/start-reading.json) · [manifest](manifest.json)

| 단계 | 고정 SHA |
| --- | --- |
| ① 모집·가림·목록 | `8720c10aa13b7c723acf9ba3e35b3bbf2a3beb7a` |
| ① 판별 확장자·분할 경로를 최초 원 글 판독 전 확정 | `f053e67a946c082ba8398c0b6297591d05b4afc9` |
| ② 요구·목록·공동 판정과 근거 위치 봉인 | `d7ff9f6dc76f3a9f77518f3900c977a533e9536b` |
| ③ 답 공개·조인, 실행 기대 봉인 | `877aa0c16691ae3827e4902cec72e8850dda6beb` |
| ④ 첫 실행 보존·계측 보정 | `a2582e9a6112a7ed8283c3ae1237580ec9eeb189` |
| ④ 결과와 자체 점검 | `cece879e89d670a50dc64b309cb18c2f2745e60c` |
| ④ 원격 재열람 및 세션 수용 근거 | `c194890b7d56f07731085e6b0642ce996786b5fe` |

## 실제 검사

빈 디렉터리에서 목록 6행이 바이트 일치했다. 48셀·중복·불명 분모, 7채점 입력, 결과의 12·48·8행, 독립 원저작 105편과 분야 밖 승인 원기록 2편을 확인했다. 공동 판독과 재판독은 동일한 작업자가 맡았다. 자연·교정 모집 및 목록 구축은 별도 역할이었다. [재현](reproduce.md) · [자체 점검](SELF_CHECK.md)

결과 SHA `cece879e89d670a50dc64b309cb18c2f2745e60c`에서 RESULT와 수용 원장을 포함한 17개 파일이 HTTP 200이었고 Git 바이트와 일치했다. 깨끗한 결과 checkout의 명시 `workbench.session check --fetch`와 일회용 checkout의 `cloud_check.py --fetch-contract --require-clean`은 모두 종료 0이었다. 공통 검사기의 자동 조회는 `no_active_sessions`였으며, 소유 경로 manifest는 명시 세션 검사에서 `passed / remote_checked`였다. [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/c194890b7d56f07731085e6b0642ce996786b5fe/docs/workstreams/research/AF-RES-080/evidence/acceptance-evidence.json)

수용 원장을 저장한 `c194890b7d56f07731085e6b0642ce996786b5fe`에서 Codex Cloud Linux x86_64의 `agent`가 CPython 3.12.14로 명시 세션 검사를 다시 실행했다. 2026-11-23T11:35:43.163265Z 종료 0, `passed / remote_checked`, 원격 통합 재조회 `d478b3e256970b5f425b23ca729369bf2f68cdfb`다. 11:35:42.791001–11:35:43.631367 UTC에 RESULT, 수용 원장, 자체 점검, 판정, 실행의 5개 원격 바이트를 재대조했다. RESULT SHA-256은 `88e3a8ff968daa8679df08ccea760e7ab0176b8b869ad720403135b9c9b37669`, 수용 원장은 `139e81f2662c8229ffde5ad3cd8006c4cfa6a96e437d42357e2786afe31ac28e`다.

```bash
p=docs/workstreams/research/AF-RES-080
python -B -m workbench.session check "$p/manifest.json" --fetch
```

## 다음 첫 행동

읽기 권한이 있는 GitHub API 환경에서 최초판 복구 통제 #1060부터 실행한다. Cloud에서 같은 공개 대조군의 GraphQL POST는 Forbidden, 종료 1이었다. GitHub가 실제 수정 이력을 반환할 때에만 같은 조회로 선택 및 선행 순번의 창설 본문을 확인한다. 미복원 상태는 현재 결과에 남겨둔다. [수정 대조군](https://github.com/python-attrs/attrs/issues/1060#issuecomment-1329862116) · [재개 입력](reproduce.md)

```bash
p=docs/workstreams/research/AF-RES-080
GH_PROMPT_DISABLED=1 gh api graphql \
  -F owner=python-attrs -F repo=attrs -F number=1060 \
  -F query=@"$p/fixtures/original_body.graphql"
```

해시가 달라지면 봉인된 모집 순번으로 다시 시작해 가린 요구를 독립 재판독한다. 성공 소비판을 확인한 경우에만 그 공식 wheel과 Python 환경을 고정해 `experiment/run_fixtures.py`의 네 자리 중 해당 양성·경계를 실행한다. 입력 경계가 필요한 첫 비교는 AC01의 두 레지스트리 키다. [정확판 및 비교 명령](reproduce.md)
