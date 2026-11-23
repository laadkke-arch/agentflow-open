# AF-RES-073 인계 — PARTIAL

## 결과와 다음 첫 행동

작업 브랜치 **work/research-af-res-073**에 조사·원장·반례·검사를 커밋했다. 고정 결과 SHA는 **6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9**다. 이 HANDOFF는 그 결과를 부모로 하는 **마지막 단독 파일 커밋**이다. 중앙 dot-control.json과 다른 작업의 파일은 수정하지 않았다.

**PARTIAL 사유는 최초판 모집이다.** 3개 입력·9개 보기·18개 질의·90개 순위와 직접 읽은 독립 원저작 43개는 확보했다. 그러나 모집 때 확인한 첫 main 추가판보다 앞선 PR 초안이 SPEC9와 JEP97에 있었다. 특히 JEP97에서 실험에 고정한 불변 문서·일대일 버전 대응 C2는 첫 PR에 없고 3월 14일에 추가되었다. Git 이전 창설 원고도 검증하지 못했다. 사전 질의와 순위를 이미 봉인한 뒤 발견한 결함을 원장 수정으로 없앨 수 없으므로, 최초판 3건 완료 또는 무힌트 탐색 성공으로 보고하지 않는다.

**재개 첫 행동:** [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/frame.csv)의 JEP/SPEC 각 첫 8개 후보에 대해 최초 PR의 added-file blob과 작성시각을 모아 **PR-first 모집틀을 새 층으로 봉인**한다. 현재 frame/queries/proposals는 덮어쓰지 않는다. 먼저 아래 세 원커밋을 GitHub에서 대조한다.

| 제안 | 이번 실제 입력 | 사후 확보한 첫 PR | 바로 확인할 차이 |
| --- | --- | --- | --- |
| P1 JEP122 | 2b194a3c090fd375321871c47a3de503a0758206 | 동일 | 3월 Google 초안의 당시 판은 미확보. 현재 첫 PR와 창설 원고를 구분. |
| P2 SPEC9 | 846579d4b8d5ca90ba6a9792c263574c73b9f48d | 6ddd0d85a8acf184e2e7e35899c0d80af639dc94 | C1/C2는 이미 있음. single-vendor 대안은 나중 삭제, Open Source Way Notes는 후대 추가. 모든 후보의 PR-first 순위를 다시 확인. |
| P3 JEP97 | b9ab810ae0fc50ac7494fdf9d345738e1cf6751d | 0f4510266ead738e62f1d9e412d6bb9e7eb7a97d | 첫 PR에는 immutable·일대일·const 조건 없음. e2651761a98f673d9c1e05d02e33ac4b3668c736에서 추가. 3월1일 원고 미확보. |

첫 API 입력은 `https://api.github.com/repos/jupyter/enhancement-proposals/pulls/123/commits?per_page=100`, `https://api.github.com/repos/scientific-python/specs/pulls/323/commits?per_page=100`, `https://api.github.com/repos/jupyter/enhancement-proposals/pulls/97/commits?per_page=100`다. 이미 읽은 이 세 PR는 [postseal/](https://github.com/laadkke-arch/agentflow-open/tree/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/postseal/)에 영수증이 있다. 나머지 후보도 PR 첫 added blob·rename·삭제 후 재추가를 동일하게 확인해야 한다. 문서의 머리말 날짜를 Git 최초 추가일 대신 쓰지 않는다.

## 인수한 기준과 계약

| 항목 | 고정 값 |
| --- | --- |
| 실제 시작 통합 HEAD | 817ee771ebfa63d4a177ee12f46b9818a6335308 |
| 사용자 계획 기준 | 39cadb6ecdf62d0b21c0cce67834f2aef3bf6853 |
| 유일한 결과 의존 HANDOFF | AF-RES-069 @616a1dab1b7d3ff8ff14210316c251cd5e5727b7 |
| 의존 RESULT Q2/Q7 | fb710fce01052a5b907398e2da6840b59d3cfa08 |
| 계약 version / SHA256 | 2 / 19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc |
| 허용 경로 | docs/workstreams/research/AF-RES-073/ |
| 마지막 실제 원격 계약 검사 통합 HEAD | 4d5185e75e52f405bfa7d149c32a0cd135395bbd |

AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, RESEARCH_BRIEF.md, 자기 control 항목과 고정 의존 인계·결과를 GitHub에서 읽었다. 069의 옛 이슈·FAA 사례·옛 검색 순위를 이번 표본으로 다시 조사하지 않았다. 다른 PLAN#18 결과를 기다리거나 새 의존으로 추가하지 않았다.

실제 시작 명령은 아래이며 종료 0 영수증을 [session-start.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/session-start.json)에 보존했다.

```sh
python -B -m workbench.session start af-res-073 --allow docs/workstreams/research/AF-RES-073/ --dependency work/research-af-res-069=616a1dab1b7d3ff8ff14210316c251cd5e5727b7 --output docs/workstreams/research/AF-RES-073/manifest.json --fetch
```

## 완료한 기록과 분모

| 기록 | 실제 수와 의미 |
| --- | --- |
| 모집 frame | 17행×14열. JEP8·SPEC8, MEP기간 내 공통 README1행 제외. MEP번호 제안 공석, 사전 JEP→SPEC 보충순서로 JEP97 선정. |
| 실제 검색 | 3입력·9보기·18질의,각 첫5자리 총90순위. 서로 다른 URL82개. |
| 원 검색 비용 | 검색18 + 문서작업52 = 70. A22 / B24 / C24. 제안별 공통 비용 7/7/8. |
| 원문과 순위 연결 | 직접 1차 원문 문서작업43회,연결 순위46자리(동일 URL재사용3자리 포함). 미열람22자리는 부정 결과가 아님. |
| 원장 | runs166행,sources108행,judgments90행×36열,decisions23행×32열. |
| 독립 원저작 | 보수적으로43계보. 동일 제안·PR·후속판,구현의 코드/시험/릴리스,번역·미러·재열람을 중복 산입하지 않음. |
| 사후 조사 | 62연산: 본문·코드·패치·당사자 기록40,메타데이터·서지13,검색4,접근실패4,재작성요약1. 원 검색 분자에 추가0. |
| 조건부 설계 적격 | A/B/C 모두 관측0. 최초 적격 비용은null/예산 내 미관측. |
| 적용 시험 | 목표 시스템 실행0. 성공률은 분모0으로 산출 불가. 공통 저장소 회귀 검사를 목표 적용 시험으로 세지 않음. |

자료 최소량은 넘었지만 최초판 3건과 특정 구현 유형별 목표를 충족했다고 덧붙이지 않는다. 반환된27개 1차 원저작 계보에는 완성품 기능,공급자 절차,재사용 구현,형식 규격,운영 정책과 원논문이 함께 있다. 정책 문서를 실행된 재사용 부품이라고 바꾸어 세지 않는다. 모집·원실험·사후 자료의 구분과 개별 최소량 산입 이유는 sources에 있다.

## Q1~Q8 인계

| 질문 | 충족한 답·반례 | 남은 미확인 |
| --- | --- | --- |
| Q1 | 첫 main 이력·원순번·이름 변경/경로 재사용·조건 인용 확보. 사후 첫 PR와 비교해 최초판 가정을 반증. | 창설판3건,전체 PR-first 모집순위,외부 초기 원고. |
| Q2 | 모든18질의의 원표현→동작·대상·행위자·관찰자 대응. P1기하 부품/P2승인권/P3인간 독자의 의미 이동과 C복원 확인. | 명사 복원만의 인과효과. 질의 길이와 어휘도 다름. |
| Q3 | 90순위 전부 실제 질의·도착 원문·절·원장·비용 연결. 미러/재작성/로그인실패/미열람 구분. | 열지 않은22자리와 접근 실패 원문 내용. |
| Q4 | 이동/책임수락,역할개정/공개범위,라벨유지/실제변환의 선택·최소 반례·대조 입력. P1잠정 적격1건 철회. | 수신 프로젝트 실제 효과. |
| Q5 | 같은 구성 두 조건 적격0. nbformat5.7.3코드·원시험으로 strict validation과 reads의 구별 확인. | 해당 입력의 실제 실행·과거 dependency lock·구형 앱·불변 URI운영. |
| Q6 | 대상/원리별 교집합41행. 같은 단어의 다른 대상과 다른 어휘의 부분 원리 비교. 사후 기록관리·공연진행 두 분야3독립저작. | 새 URL을 넘는 유효 선택의 추가 이득. 비소프트웨어 분야는 사용자 예시로 사전 노출. |
| Q7 | P1조직 승인,P2Matplotlib선행인지와draft승인,P3strict/permissive선행인지와proposal수락 확인. VTML은1995년12월12일 공식 세션에 등재. | P1개별권한·기술결과,SPEC9실제채택,JEP97실제구현출시,VTML저자인지. |
| Q8 | 70원실험과62사후연산 분리,실제7/7/8까지 비용 일치 비교. 0·분모없음·미측정·실패를 구분. | 사용자 시간 절감,내부 HTTP/토큰·모집지원·캐시 재판독 노동 비용. |

[RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md)는 필수3표를 맨 앞에 놓았으며 표2는90행 전부다. 뒤에 Q1~Q8과 마지막 약점3행을 둔다. [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/SELF_CHECK.md)는 각 Q의 주장·행ID·원절·반증 탐색·남은 입력을 대응한다.

## 실제 검사 — 주체·SHA·종료값

root가 실제 checkout에서 아래 두 명령을 결과 SHA **6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9**에 대해 실행했다. 둘 다 종료 0이고 evidence checker는247개 항목을 통과했다. session check의 outside_paths·unmerged_paths·errors는 모두 빈 배열이다. 검사 직전 작업 트리는 clean이었다.

```sh
python -B docs/workstreams/research/AF-RES-073/evidence/verify.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-073/manifest.json --fetch
```

```json
{
  "actor": "root research agent",
  "checked_commit": "6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9",
  "evidence_command": "python -B docs/workstreams/research/AF-RES-073/evidence/verify.py",
  "evidence_checked_utc": "2026-11-23T11:05:36.609318+00:00",
  "evidence_exit": 0,
  "evidence_checks": 247,
  "source_clean": true,
  "session_command": "python -B -m workbench.session check docs/workstreams/research/AF-RES-073/manifest.json --fetch",
  "session_checked_utc": "2026-11-23T11:05:42.690944+00:00",
  "session_exit": 0,
  "integration_commit": "4d5185e75e52f405bfa7d149c32a0cd135395bbd",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_path_count": 151,
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "remote_reread_files": 9,
  "remote_all_blob_hashes_match": true,
  "remote_body_character_counts_match": true,
  "target_application_tests_executed": 0
}
```

앞선 본문 고정 SHA `d2ed9b26bd993cad0e7e5c58788bc59dbafc0be3`의 검사 원문은 [validation-receipt.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/validation-receipt.json), [session-check.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/session-check.json)에 있다. 첫 session fetch 실패 종료 2와 정확한 refspec 진단·재시행 성공을 모두 남겼다. manifest나 검사기를 바꾸어 통과시키지 않았다.

같은 d2ed9b2 커밋의 소유 경로 내부 임시 detached worktree에서 다음 명령도 실행했다.

```sh
python -B scripts/cloud_check.py --environment chatgpt-executor --fetch-contract --require-clean
```

doctor·acceptance·research-case·original-smoke·sessions 모두 종료 0,시작과 종료 시점 모두 clean이다. [common-check.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/common-check.json)과 로그를 보존한 뒤 임시 worktree를 제거했다. 환경 이름은 호출자 표지이며 특정 클라우드 계정 연결 증거가 아니다. 이후 추가한 검사 영수증과 SELF_CHECK 변경을 앞선 공통 검사에 포함된 것으로 표시하지 않았다. 마지막 결과 SHA의 원장·계약 검사는 위에 별도로 기록했다.

## 결과 SHA를 GitHub에서 다시 연 대조

결과 SHA **6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9**에서 다음 9개 파일을 GitHub 연결로 다시 열었다. 반환 본문을 읽고 로컬 Git blob SHA·본문 문자수·JSONL 행 수·표 2의 90행·수용기록 PARTIAL을 대조했다. 모든 blob SHA와 본문 길이가 일치했다. 아래 바이트는 로컬 UTF-8 원본 기준이다. 이 검사는 연구 원문 독립 수나 원 검색 비용에 더하지 않는다.

| 파일 | GitHub에서 재확인한 blob SHA | 바이트 | 대조 |
| --- | --- | ---: | --- |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/RESULT.md) | `0f740f9dc151c54f94499b01bf3916eca4e5c882` | 124139 | 일치·본문 다시 읽음 |
| [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/sources.jsonl) | `e2317162bc86bc884d72efa81b0b5472460215c5` | 245259 | 일치·본문 다시 읽음 |
| [runs.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/runs.jsonl) | `c7ee869a6f757d05b0f91368d4333874f1659b15` | 114711 | 일치·본문 다시 읽음 |
| [judgments.csv](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/judgments.csv) | `77730ca560c354feb6b7423e093f01d856554d8a` | 94900 | 일치·본문 다시 읽음 |
| [decisions.csv](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/decisions.csv) | `13afd6aafbe3e5623af4d54d356db2f952c87f3f` | 64850 | 일치·본문 다시 읽음 |
| [queries.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/queries.jsonl) | `4b2c617b9c43bfe35125dcf66092037cfa019a1f` | 19767 | 일치·본문 다시 읽음 |
| [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/frame.csv) | `8ea15c727a92130f3e8d15abc5c9bb12a778023f` | 7171 | 일치·본문 다시 읽음 |
| [evidence/acceptance-evidence.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/evidence/acceptance-evidence.json) | `2c4281be565b7032873d4d091f54857d97532137` | 7968 | 일치·본문 다시 읽음 |
| [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/SELF_CHECK.md) | `2bafde9356a53d9d0c2dad087dbe6201ff1682fe` | 13923 | 일치·본문 다시 읽음 |

## 미실행 시험의 정확한 명령과 입력

실행하지 않은 목표 시험은 [P3 NEXT.md](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/postseal/P3/NEXT.md)에 있다. 최소 입력은 [fixtures.json](https://github.com/laadkke-arch/agentflow-open/blob/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/postseal/P3/fixtures.json)의 4개 객체다: 추가 필드 없는 4.5 대조, 4.5에 $schema만 추가, 4.6 정규 URI, 4.6의 /../ 비정규 URI. 이 URI 문자열을 실제 발행·불변성 검증 URL로 주장하지 않는다.

**먼저 필요한 입력:** nbformat 5.7.3 / commit `bbd0f83b67a126cd04c48a03ad053c52e6597d96`, Python 및 모든 의존성 버전, validator 선택, 실제 구형 앱 이름과 버전, 제안의 required 불일치에서 어느 조각을 실행할지, 고정 schema 바이트·해시·정규 URI·alias 정책. 과거 lock이 없으면 현대 재구성 환경이라고 표시한다.

저장소 루트에서 그 고정 환경으로 실행할 명령은 다음이다. 출력은 새 사후 검증층에 넣고 원 검색의 분자나 비용을 바꾸지 않는다.

```sh
NBFORMAT_VALIDATOR=jsonschema python -B docs/workstreams/research/AF-RES-073/postseal/P3/probe_notebook_compatibility.py > docs/workstreams/research/AF-RES-073/postseal/P3/probe-jsonschema-output.json
NBFORMAT_VALIDATOR=fastjsonschema python -B docs/workstreams/research/AF-RES-073/postseal/P3/probe_notebook_compatibility.py > docs/workstreams/research/AF-RES-073/postseal/P3/probe-fastjsonschema-output.json
```

정확한 nbformat SHA의 별도 checkout 루트에서는 다음 원시험을 재실행한다.

```sh
python -B -m pytest tests/test_api.py::TestAPI::test_capture_validation_error tests/test_validator.py::test_future
```

위 시험은 일반 기존 사례이므로 통과해도 JEP97의 모든 새 입력, 목표 앱, C2의 영구 불변성을 증명하지 않는다. probe는 raw schema 검사, validate, reads를 각각 출력하고 외부 URI는 가져오지 않는다. 실제 JEP97 적용을 주장하려면 구현 PR/commit, 같은 구성의 시험 결과, 포함 release/tag가 추가로 필요하다.

알려진 migration gist는 HTML/raw 두 접근 모두 실패했다. 재개 가능한 인증된 공개 GitHub 읽기 환경에서 입력 `gists/a6e1ae13125f01ff04edf121e30a462a`의 created_at, updated_at, history, version, committed_at, files.content와 raw_url을 확보해야 한다. 현재 gist를 2023년판으로 대신하지 않는다.

## 커밋 묶음과 검토 독립성

| 묶음 | 커밋 |
| --- | --- |
| 계약·범위 | dd4579fc9bf1d70ba951a9329e2a2524ae1f5377 |
| 모집·이력 | c4641c2361b0bf27e3e7d51605ca897fce7e9c33 |
| 18질의 사전 봉인 | 469d8c569e054622567ecf328150898ed384ada1 |
| 첫 원 영수증 | 005ee5d58c9fbc32e1172949840786b95352abce |
| 여섯 보기 영수증 | b3d2942214cbe830bb8d9fa81e73a683a0f161d8 |
| 원 검색 전체 봉인 | fbc05801af45f21e60d6901f3293f9af9969ef8d |
| 원 후보 판정·철회·동일비용 | a312075f89581bd6dda4fdcd472a324a9a112d11 |
| 사후 원자료·반례·결정 별도 묶음 | 8b6b349c2a8721d0d5467a936a0ec6e64029415c |
| 필수 표·Q1~Q8·검산기 | d2ed9b26bd993cad0e7e5c58788bc59dbafc0be3 |
| 실행 영수증을 포함한 고정 결과 | 6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9 |

원자료는 root와 같은 모델의 분담 작업자 3개가 읽었다. 통합 원장 검토와 결과 검토를 했으며 P3 검토는 원 조사자의 자체 재판독이다. 독립 인간 판독자는 0명이고 눈가림 인간 실험도 없었다. [review/](https://github.com/laadkke-arch/agentflow-open/tree/6713e47c3dd1fa8acfea2d2b4d3ead72bc7176a9/docs/workstreams/research/AF-RES-073/review/)에 검토 범위, 당시 보고서 해시, 수정 권고와 root의 해결을 보존했다. 로컬 git push는 초기에 자격증명 없음으로 실패하여 승인된 GitHub 연결로 expected-head 검사를 걸어 커밋과 참조를 갱신했다. 강제 push, merge, 공통 계약 수정은 없었다.

## 남은 가장 중요한 세 한계

1. **기원:** 최초판 모집의 범위가 잘못 좁혀졌다. 앞선 PR와 외부 초안을 포함한 새 모집틀과 조건 인용이 확정되어야 초기 설계 검색이라고 판단할 수 있다.
2. **일반화:** 세 입력 중 두 개가 거버넌스이고 사전 지식·보기 노출·길이 차이가 있다. 다른 실제 개발 요구와 결과를 미리 보지 않은 판독에서 같은 비용의 새로운 적격 선택이 반복되어야 일반 효율 주장이 가능하다.
3. **관측:** 미열람 22자리, 접근에 실패한 원문, 목표 실행 0회와 실제 채택 미확인이 남는다. 새 비용층의 직접 판독, 고정 입력 실행과 당사자 기록이 결론을 바꿀 수 있다.

조사 산출물의 상태는 **PARTIAL**이며 중앙 상태의 DONE 변경과 별개다. 커밋되지 않은 결과를 완료로 세지 않는다.

