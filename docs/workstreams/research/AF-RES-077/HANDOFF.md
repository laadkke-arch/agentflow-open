# AF-RES-077 인계 — PARTIAL

## 결과와 종료 지점

작업 브랜치는 **work/research-af-res-077**, 수용 영수증을 포함한 결과 SHA는 **5170e3e07d2278800480e1d71cc2f2a2ce9ab01a**다. 이 HANDOFF는 그 결과를 부모로 하는 **마지막 단독 파일 커밋**이다. 최신 확인점 `2f7e07542b4a59839556e00c9e266179150b21a3` 이후의 결과·검토·검산·인계를 끝냈다. 기존 모집과 A/B 봉인을 반복하거나 초기화하지 않았다. 이전 작업공간의 미커밋 파일은 재개 근거로 사용하지 않았다.

**산출물은 완성했지만 연구 판정은 PARTIAL이다.** 첫 10건 모집의 주 표본 적격 0/3, 최초 body revision 0/3, 당시판 대상 독립 자료 3/6, 목표 실행 0/9가 남는다. 목표 통과·실패는 모두 미확인이다. 기계 검사·공통 회귀 통과로 이 결손을 채우지 않는다. 중앙 dot-control.json·다른 작업·main·통합 브랜치는 수정하지 않았다.

### 다음 첫 행동

새 검증 담당자는 아래 결과 SHA에서 [TESTS.csv](TESTS.csv)의 `native_applicability`, `checkpoint_limit`, `minimum_followup`과 [ERRATA.md](evidence/ERRATA.md)의 E2/E3/E5/E6을 먼저 읽고, **native 조작으로 표현 가능한 새 실행 입력을 별도 층에 봉인**한다. 특히 SG-E의 `Text/parts/...` 이동은 0.9.17에서 지원되지 않으므로 flat rename으로 바꾸어 기존 성공으로 세지 않는다. MS-E는 part 생성 직후 flag/list/mark를 관찰해야 하고, SC-X는 원래 비영상 bytes인 점을 유지한다. 실행 가능한 새 fixture/harness가 생기기 전에는 이 9자리를 GUI 성공으로 보고할 수 없다.

```sh
git fetch origin work/research-af-res-077
git show 5170e3e07d2278800480e1d71cc2f2a2ce9ab01a:docs/workstreams/research/AF-RES-077/RESULT.md
git show 5170e3e07d2278800480e1d71cc2f2a2ce9ab01a:docs/workstreams/research/AF-RES-077/TESTS.csv
```

주 표본을 완결하려면 별도로 원 요구 최초판·실제 affected build·두 보존 조건이 결합된 새 모집층이 필요하다. 기존 30행이나 봉인된 연구 조건을 유지보수자의 원 요구로 바꾸지 않는다.

## 핵심 결론

| 대상 | A/B 기술 대조에서 남은 결론 | 실제 자료가 제한하는 부분 |
| --- | --- | --- |
| Shotcut | 두 선택 모두 full-content provenance와 확인 전 거부 계열이다. darktable은 공유 원본과 편집 metadata를 구분하는 설명을 제공했다. | digest·snapshot·복구 순서는 연구자 제안. sample hash가 같은 비영상 middle-change는 보조 확인했지만 native preview·저장·재열기는 미실행. 완료 시 `replaceAllByHash` fan-out도 범위 보존의 구현 지점이다. |
| MuseScore | 동종 Handbook과 TEI를 받은 두 판독자 모두 local excerpt deselection을 선택했다. TEI에서 명령 역연산을 도출하는 전이는 기각했다. | 실제 2019 PR은 global copy constructor flag 제거를 병합했다. 이는 연구 선호와 다른 historical adoption이며, 우리 자료의 효과나 고정 입력 9개의 통과가 아니다. |
| Sigil | 두 선택 모두 원래 문서+fragment를 최종 대상으로 연결하는 임시 대응표를 골랐다. 영구 digest inventory는 선택하지 않았다. | OCFL은 fragment 의미·inverse split·원자 저장을 제공하지 않는다. 실제 #450은 ref와 target이 함께 이동하는 경우였고 봉인 N/E와 다르다. SG-E는 native 조작 미지원이다. |

정규화한 핵심 선택 변화는 **0/3**, 경쟁 후보 집합 차이는 2/3, 새 시험 입력은 0/9다. 원전별 설명·기각 근거는 3/3에 있다. SC-X에서 rebuild 필요와 명시적 recovery decision 대기라는 차이는 남으므로 모든 구현 정책이 동일하다는 뜻은 아니다. 독립 인과효과 분모 0, 원 개발자 작업 시간 절감은 미측정이다. [RESULT.md](RESULT.md)의 필수 표 3개·Q1–Q8·마지막 약점 정확히 3건과 [CASEBOOK.md](CASEBOOK.md)를 함께 읽는다.

## 인수한 기준과 범위

| 항목 | 값 |
| --- | --- |
| 사용자 계획 통합판 | `0d2b08431067e8d87212a66ecb27657c65722a59` |
| 실제 최초 시작판 | `d73c8ec85d375f37451795b575dd7d0e6b2f3594` |
| 재개 확인 HEAD | `2f7e07542b4a59839556e00c9e266179150b21a3` |
| 재개/최종 계약 확인 통합판 | `fea791175dfd1dac66b2b94bcb3ddbc12c7359a2` |
| 유일한 결과 의존 | `AF-RES-073@28dfa4d14ce33f0f98c823f83c20347d60c0e64e`의 HANDOFF·RESULT Q4/Q5·judgments |
| 계약 version / SHA256 | 2 / `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc` |
| 허용 경로 | `docs/workstreams/research/AF-RES-077/` |

AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 해당 control 항목을 현재 GitHub에서 확인했다. control의 attempt 2/RUNNING은 배정자의 상태이며 본 결과의 PARTIAL과 구분한다. 073의 최초판 모집 결함과 목표 적용 0을 이어받았고, 그 웹검색/랭킹·057의 Yjs·069의 대상을 반복하지 않았다. 다른 PLAN#19 과제의 결과·중간 파일·조사자를 전제하지 않았다. 배정 명칭은 web-pro지만 실제 증거는 현재 ChatGPT 도구 문맥과 같은 모델 계열의 분담 검토이며 특정 웹 UI 모델 선택을 증명하지 않는다.

## 완료한 산출물과 분모

| 기록 | 실제 수·의미 |
| --- | --- |
| [SOURCES.jsonl](SOURCES.jsonl) | 358행. 기존 302+재개 56. 재개 56은 외부 도구 read 50회와 보존된 원시험/fixture의 로컬 재판독 6회다. |
| 독립 원저작 | named 24 / conservative 21. 세 대상의 code/manual은 일관되게 합쳤다. 재개에 신규 산입 0. 최소 20 전체층은 충족. |
| 고정판 대상 자료 층 | named 6 / conservative 4 / 당시판 확인 3. 요구 6에 미달. 동일 codebase의 파일·시험·release로 수를 늘리지 않음. |
| [FRAME.csv](FRAME.csv) / [BRIEFS.jsonl](BRIEFS.jsonl) | 첫 10×3=30행 / 보조 3개. 주 적격 0/3·최초 body revision 0/3. tag 소스 SHA 3/3은 별도 확인. |
| [VIEWS.csv](VIEWS.csv) / readers | 보기 6개·후보 13개. A 먼저, B 나중. 각 1저작·2절 이하·원문 2,000자 이하·reader 추가 열람 0. |
| [TESTS.csv](TESTS.csv) | 입력 9개·선택안 예측 18개·모든 후보 예측 39개. source assertion·당사자 보고·원 실행·연구 보조·미실행을 분리. |
| 목표 실행 / 원 실행 영수증 | 0/9 / 0/9. 통과·실패 모두 `UNKNOWN_NOT_RUN`. |
| 연구 보조 관측 | input predicate 5/9. 완전 workflow 0/9. 기존 worker exit0, 입력/출력 hash 보존. 이번 재개에서 불필요하게 재실행하지 않음. |
| [COSTS.csv](COSTS.csv) | 30행. 재개 전 요청 구성 222, 부분 web 보고 2를 포함하면 224. 완전한 총비용은 아님. |
| 재개 비용 | 50 tool operations = GitHub 24 + web open 16 + web find 10. 위 요청 222/224와 합산하지 않음. 접근 실패 4·find 불일치 4. |
| 실제 원문 노출 | A 3,593자 / B 4,912자. 상한은 같지만 실현 노출량·역할 지시 동등성·노동 시간은 같다고 할 수 없음. |

[SELF_CHECK.md](SELF_CHECK.md)는 각 Q에 주장/미확인·원절/판·확인 내용·한계·반례·최소 후속 확인을 7열로 대응한다. [COUNTING.md](evidence/COUNTING.md), [EXPOSURE.md](evidence/EXPOSURE.md), [RESUME_REGISTRY.md](evidence/RESUME_REGISTRY.md)에 계보·비용·노출의 분모를 풀어 썼다. 삭제된 원문 cache 22건의 raw hash는 영수증 기반이며 현재 보존 파일만으로 독립 재계산했다고 주장하지 않는다.

## 재개에서 정정한 중요한 내용

- MuseScore 원 tracker의 공식 페이지 캐시 일부를 별도 검토자가 확보했다. ericfontainejazz·2019-01-08 표시·Reported version 3.0/본문 2.3.2 보고를 확인했지만 최초판·전체 이력은 아니다. 후속 두 open과 root 두 open은 403이었다. v3.0.1은 PR 이전이나 원 신고 이후판으로 정정했다. 과거 403 기록은 지우지 않았다.
- TEI `#TCAPWL`의 정확한 절 제목은 13.1.4.3 **The Witness List**다. witness identity에서 없는 inverse를 만들지 않는다.
- Shotcut의 producer-scoped 제안은 `ProxyReplacePostJobAction::doAction` → `MainWindow::replaceAllByHash`와 downstream 교체까지 검토해야 한다. frozen p2에 실제 변화가 있었다는 뜻은 아니다.
- MuseScore는 `Note::mark()`도 선택색에 영향을 주므로 색상만으로 선택을 판정하지 않는다. flag/list를 생성 직후 관찰해야 한다.
- Sigil은 원 보고의 split 위치, 공개 EPUB의 missing member를 향하는 상대 href, 0.9.17의 nested-folder 미지원 결손을 유지했다.

세 source 재검토와 결과 재검토의 지적·반영은 [REVIEW.md](evidence/REVIEW.md)에 있다. 결과의 “실패 0건”이라는 모호한 문구는 “통과·실패 미확인”으로 고쳤다. 기존 packet·reader·BRIEFS의 봉인 bytes는 그대로다.

## 실제 검사 — 마지막 결과판

아래 두 명령은 root가 **5170e3e07d2278800480e1d71cc2f2a2ce9ab01a**의 clean checkout에서 실행했다. 검사 중 새 파일을 쓰지 않았으며, 이 HANDOFF가 그 뒤의 유일한 결과 변경이다.

```sh
python -B docs/workstreams/research/AF-RES-077/evidence/verify.py --phase final
python -B -m workbench.session check docs/workstreams/research/AF-RES-077/manifest.json --fetch
```

```json
{
  "actor": "root resume agent",
  "checked_commit": "5170e3e07d2278800480e1d71cc2f2a2ce9ab01a",
  "source_clean": true,
  "mechanical_started_utc": "2026-11-23T12:53:49.907476+00:00",
  "mechanical_finished_utc": "2026-11-23T12:53:50.421770+00:00",
  "mechanical_exit": 0,
  "mechanical_checks": 6210,
  "mechanical_errors": [],
  "session_started_utc": "2026-11-23T12:53:50.421903+00:00",
  "session_finished_utc": "2026-11-23T12:53:59.392289+00:00",
  "session_exit": 0,
  "freshness": "remote_checked",
  "integration_commit": "fea791175dfd1dac66b2b94bcb3ddbc12c7359a2",
  "outside_paths": [],
  "unmerged_paths": [],
  "session_errors": [],
  "owned_changed_paths_from_original_base": 338,
  "target_application_tests_executed": 0
}
```

검사기의 detached checkout 경고는 그대로 남겼다. SHA ancestry와 허용 경로는 확인했지만, 로컬 branch 이름만으로 remote head 일치를 주장하지 않았다. GitHub의 expected-head 조건을 건 갱신과 결과 재열람을 별도로 확인했다. 이 경고는 검사 실패가 아니다. 일반 git push는 username 부족으로 실패했으므로, 승인된 GitHub 연결로 blob/tree/commit을 만들고 `expected_sha`와 `force=false`를 사용해 같은 작업 branch를 앞으로 진행시켰다. 기존 원격 history의 reset이나 force-push는 하지 않았다.

## 공통 회귀·최초 실패의 보존

공통 검사는 본문 고정판 **88ee29fd7866474500406d94ef96f17b03142096**의 별도 clean worktree에서 실행했다. 이후 결과 commit은 검사 receipt와 설명을 추가한 것이며, 공통 코드·원 source·sealed packet·검사기를 변경하지 않았다.

```sh
python -B scripts/cloud_check.py --environment chatgpt-executor --fetch-contract --require-clean
```

1. **12:48:16–12:48:27 UTC / exit1**. 공통 단위 시험 55개와 두 lab의 시험 각각 7개·9개는 통과했다. 그러나 shallow source.bundle을 복원할 때 시작 commit의 부모 `9bb5b7f63115b2a5d85aee3556bce6f690e2688e`가 누락돼 있었다. 전체 결과는 실패로 보존했다.
2. `git fetch --unshallow origin work/research-af-res-077 chore/workspace-foundation work/research-af-res-073`를 실행하고, shallow=false이며 누락됐던 부모가 commit으로 존재함을 확인했다. checker/gate는 변경하지 않았다.
3. **12:49:41–12:49:52 UTC / exit0**. 같은 source에서 재실행했으며 시작·종료 시점 모두 clean이었다. doctor, acceptance, research-case, original-smoke가 완료됐다. sessions 명령의 exit0은 `no_active_sessions`라는 결과이며, 새 협업 실행의 성공으로 취급하지 않는다. 이번 task-specific 계약 검사는 위에서 별도로 통과했다.

최초 실패·복구 확인·성공 receipt와 stdout/stderr 로그 14개를 `evidence/common-*`에 보존했다. temporary worktree는 필요한 로그를 복사한 뒤 제거했다. 자세한 내용은 [acceptance-evidence.json](evidence/acceptance-evidence.json)과 [common-log-manifest.json](evidence/common-log-manifest.json)에 있다. 환경 라벨은 caller 이름이며 특정 클라우드 계정 연결을 증명하지 않는다. 공통 회귀는 Shotcut/MuseScore/Sigil의 적용 시험이 아니다.

## 최종 결과 SHA를 GitHub에서 재열람

최종 결과 **5170e3e07d2278800480e1d71cc2f2a2ce9ab01a**의 필수 파일 10개를 root가 2026-11-23 **12:54:07.904–12:54:09.668 UTC**에 GitHub 연결로 다시 열었다. 반환된 UTF-8 본문에서 Git blob SHA1을 재계산하고, local commit의 blob 및 remote가 반환한 blob SHA와 대조했다. **10/10 일치**했다. 이 확인을 연구의 새 source·reader exposure·시간 단축 효과에 더하지 않는다.

| 파일 | 재계산한 remote blob SHA | bytes |
| --- | --- | ---: |
| SOURCES.jsonl | 0caa6f22b469d5dbb2d8e7fe5017966be1a216f9 | 940985 |
| FRAME.csv | 571ed03adc8b837f71c479b3f98f44a52f72cff4 | 44026 |
| BRIEFS.jsonl | 244d7953d5595dd0bcb0987c84322921c7086481 | 13291 |
| VIEWS.csv | 89af21ce2fdfafc297902473c17821731251739d | 6763 |
| CASEBOOK.md | 1851c67f28e6d262fa5699269308500afe5675ab | 19457 |
| TESTS.csv | eef9948bf6b9af054102342f4354777bb53ee932 | 216212 |
| COSTS.csv | e96f1b95748f150f4f8ce619fbe83fc2f047197f | 17443 |
| RESULT.md | fd81045bd222941ace288a547a8143d50f9eef30 | 38043 |
| SELF_CHECK.md | 1917e569b1ddc3dcf6605c5fda8b3cbb508ce25d | 24615 |
| evidence/acceptance-evidence.json | 5f948396e10e04f052c4fc17f487ed8f306b41cf | 14637 |

본문판 88ee29f의 같은 방식 재열람 receipt는 [remote-result-reread.json](evidence/remote-result-reread.json)에 있다. 이후 영수증을 포함한 결과판 5170e3e의 확인은 이 표로 구별한다. 자기 참조가 되는 최종 HANDOFF 자체의 commit SHA를 본문에 넣었다고 주장하지 않는다.

## 미실시 실행의 입력·명령·막힌 이유

**현재 막힌 이유:** pinned binaries와 Qt/MLT 개발환경·cmake/ctest가 없었다. `qmake -v`, `pkg-config` 확인은 exit1이고 target build/test를 시도해 실패한 결과가 아니다. 또한 9개 frozen case의 실제 native fixture/harness는 완성되지 않았다. 프로그램이 없는 문제와 입력이 native 조작으로 표현되지 않는 문제를 따로 남긴다. [environment.json](evidence/environment.json), [MS RUNBOOK](postseal/musescore/RUNBOOK.md).

**이미 실행된 보조 관측을 재현할 때만 사용하는 명령:** 입력은 `fixtures/research/probe-inputs.json`, SC의 3MiB A/B/C→A/D/C generator, SG-N/E/X의 XHTML 5개다. 아래는 새로운 run 이름으로 다시 기록하는 명령이며 이번 재개에서 실행하지 않았다.

```sh
python -B docs/workstreams/research/AF-RES-077/evidence/auxiliary/run_probes.py --record-run followup-077
```

이것은 sample predicate/URI·duplicate 판독만 다시 실행하며 native 실행 분모를 늘리지 않는다. 실행 전 `followup-077` 출력 경로의 존재 여부를 확인하고 기존 관측을 덮어쓰지 않는다.

**MuseScore 원시험:** `06a66a2206fc5f3c2c33d7ee4123badf496bc4dd`와 당시 Qt·audio/font 개발환경, private prefix에 구성한 build가 필요하다. 전체 준비 명령은 원 source에서 확인한 [RUNBOOK](postseal/musescore/RUNBOOK.md)에 있다. 준비된 `build.debug/mtest`에서의 원시험 명령은 다음이며 이 조사에서는 미실행이다.

```sh
QT_QPA_PLATFORM=vnc xvfb-run -a ctest -j2 --output-on-failure \
  -R '^(tst_parts|tst_links|tst_exchangevoices|tst_readwriteundoreset|tst_element)$'
```

`result.xml`, stdout/stderr, exit, 환경 버전·source/fixture hash를 함께 읽어야 한다. 이 원시험 명령이 MS-N/E/X의 m1/u1·pitch·P2·save/reopen 조건을 이미 실행한다고 하지 않는다. 실제 score와 pitch command, 생성 직후 flag/list/mark 관찰을 구현하는 harness가 선행한다. MS-X는 empty undo/current 62에서 시작하며 이전 60을 다른 입력에서 가져오지 않는다.

**Sigil 원 fixture:** `postseal/sigil/originals/test_split2.epub`을 원 bytes 그대로 사용한다. full source pin은 `30419827123d533d10ad482b1634dcec05ff0e1b`다. `docs/Building_on_Linux.md`에 있는 미실행 build 순서는 아래와 같다. 의존 환경 준비는 이 조사에서 수행하지 않았다.

```sh
git clone https://github.com/Sigil-Ebook/Sigil.git sigil-src
git -C sigil-src checkout --detach 30419827123d533d10ad482b1634dcec05ff0e1b
mkdir sigil-build
cd sigil-build
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ../sigil-src
make -j4
```

그 고정 binary에서 원 EPUB의 import 전 archive, import 직후 document, 실제 hr marker로 split한 직후 href, 저장된 archive, 재열기 대상을 차례로 기록한다. 현재 literal href가 없는 member를 가리킨다는 결손을 원본에서 수정하지 않는다. native import가 정규화하는지도 관측해야 한다. SG-N의 comment marker와 SG-E의 nested move는 이 역사적 fixture와 다른 입력이므로 별도 harness/후속 case가 필요하다.

**Shotcut native 입력:** pinned 20.09.13과 MLT/Qt 환경, RED/BLUE를 실제 디코딩으로 구별할 유효 영상, producer p1/p2와 원본/proxy 정보를 담은 실제 MLT project가 필요하다. SC-E의 candidate order를 QDir/GUI 관찰에 연결하고 dialog 수락과 identity confirmation을 구분해야 한다. 완료 post-job의 hash 전파까지 추적한다. 이런 fixture/harness가 아직 없으므로 존재하지 않는 SC-N/E/X 실행 명령을 만들어 놓지 않았다. 실행 가능한 첫 행동은 이 매핑을 생성하고 입력 hash를 고정하는 것이다. SC-X의 비영상 byte probe를 유효 영상 성공으로 대체하지 않는다.

## 커밋 묶음

| 묶음 | 원격 커밋 |
| --- | --- |
| 원 규칙·범위 | e1e0e993c85686cc597b3cc625bd6e803b9af513 |
| 모집·고정판 | b3fee8986841c3dbda82a4a3093d2316c915e9c5 |
| 공통 입력·원문 보기 | 9518c3dccbd21cda72cec715afe47eebd4dba543 |
| A 선택·예측 | 7c1df93b11e06ca8b7f44ac5b7ff996879aebd09 |
| B 선택·예측 | 7bc2d1f84c04b47711d72e7c110b8f927d97f4ad |
| 원전 원장 | 924a030d593501c4736d8f84f20335be86d868f4 |
| 사례·원시험·보조 관측 | 2f7e07542b4a59839556e00c9e266179150b21a3 |
| 정확한 재개점 기록 | 134b127bbc1cdeb9934a9a83c3b376623f7c92e5 |
| 결과·재검토·정정 | 88ee29fd7866474500406d94ef96f17b03142096 |
| 실제 수용 영수증을 포함한 결과 | **5170e3e07d2278800480e1d71cc2f2a2ce9ab01a** |
| 최종 인계 | 이 파일만 변경하는 바로 다음 커밋 |

최종 PARTIAL은 연구자료의 수용 범위다. 중앙 진행표의 DONE 변경과 동일하지 않다. 이 인계 뒤에 자동으로 계속 실행되는 작업이나 예약을 만들지 않았다.
