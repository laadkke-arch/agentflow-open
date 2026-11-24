# AF-RES-105 / 시도1 인계

## 1. 식별과 완료 상태

- 작업 ID / 시도: **AF-RES-105#1**.
- 배정 종류: **web-pro**. 실제 수행은 ChatGPT 공유 Linux 작업공간에서 공개 웹·GitHub API 판독과 사용 가능한 셸 실행을 병행했다. 세션에서 제공된 모델 표시는 **GPT-6 Astra Pro**다. `cloud_check --environment codex-cloud`는 사용자 지정 실행 라벨이며 별도 계정 연결이나 새 AI 세션 검증을 의미하지 않는다.
- 공개 작업자 참조: `/root`, `/root/blender_initial`, `/root/qgis_initial`, `/root/contract_prior_audit`. 외부 사람 검토는 미실시다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-105`.
- 시작 SHA: `32b6bb32989730df78d521c29a50dbebd3289b46`.
- **검사를 받은 결과 SHA: `9290320c1e9de33f30857af87640926c4d0f8cff`**. [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/RESULT.md).
- 인계문 작성 전 마지막 확인한 원격 저장 SHA: 위 결과 SHA. 원격 tip 확인 **2026-11-24T01:04:04.816824Z**, GitHub 고정판 재열람 및 blob 대사 완료 **2026-11-24T01:08:33.961304Z**.
- 마지막 실제 진행 증거: 동일 결과 SHA의 깨끗한 detached worktree에서 지정 검사2개와 원장 재집계1개 exit0; GitHub 필수3표·대표 근거/출력·재현 문서6개 재열람.
- PR: 미생성. 이 작업의 전달 단위는 자기 브랜치의 커밋된 연구 묶음이다.
- 최종 확인 UTC(이 문서 작성): **2026-11-24T01:12:40.377997+00:00**.
- **상태: REVIEW_READY.** 요청된 모집·직접 판독·반례·분모·반환·재현·자가검토와 결과판 gate를 완료했다. 시간순8+보조4 모두 실재, 결원0, 필수자료 부족0. 원 사용자 실행·판·완전한 새로움은 아래의 미확인으로 남는다.

이 HANDOFF는 결과 검사와 고정판 재열람 이후 처음 작성했다. 최종 커밋은 **HANDOFF.md 한 파일만** 포함하도록 준비한다. 자기 커밋 SHA는 자기 본문에 넣을 수 없으므로 검사 대상 결과 SHA와 이 인계문이 속한 최종 커밋을 구분한다. 최종 원격 인계 SHA는 커밋 메타데이터와 작업자의 최종 응답에서 확인한다.

## 2. 요구 범위·계약·계승

제품 전체를 익숙함으로 제외할지, 이미 시도한 조작만 표시하고 다른 단계를 제시할지 판단할 근거를 수집했다. 후속 설계자가 독립적으로 채택·폐기할 묶음이며 제품 정책의 확정이나 A/B 우월성 판정이 아니다. 허용된 변경 경로는 `docs/workstreams/research/AF-RES-105/`뿐이다. 실제 작업 검사에서 outside_paths=[]이며 dot-control.json 변경은 없다.

| 역할 | 읽은 고정판·기록 | 영향 |
| --- | --- | --- |
| 계획 기준 통합판 | `49f603a98188fbf2009c4c490b0539f32d124e38`의 [연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/product/RESEARCH_BRIEF.md)·[운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/RESEARCH_WORKFLOW.md) | 시작 실제32b6bb3과 달라진 경로는 dot-control.json뿐. 요구 읽기 파일·계약·제품 브리프·검사 스크립트 blob은 동일 |
| 실제 시작판 | `32b6bb32989730df78d521c29a50dbebd3289b46`의 AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·AF-RES-105 항목 | [시작 diff·blob 영수증](evidence/start/contract-read.json), [manifest](manifest.json) |
| 운영 의존 | `work/research-af-res-101=b29c25fe6d7375dc28c4c700da2240c1a205093d`의 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/b29c25fe6d7375dc28c4c700da2240c1a205093d/docs/workstreams/research/AF-RES-101/HANDOFF.md) | 시작과 최종 fetch에서 tip이 등록 인계와 같음. 운영 핀 변경 불필요 |
| 연구 입력 | `392ff3d651577ab6aacd65f4ed86884586b960d1`의 RESULT·candidates·followup·reconciliation | 입력→운영 인계 차이는 HANDOFF 추가뿐. 연구 입력을 새 tip으로 바꾸지 않음 |
| 최종 검사 때 통합판 | `8916e31c275f6076f8367e95d7ca36d48a28e0e4` | 시작32b6bb3 이후 diff도 dot-control.json뿐. 계약 SHA256 동일, 명시 manifest 검사 PASS. 연구 입력/소유 범위 영향 없음 |

101의18후보에서A7/B14, B에만 남은7개 중 Typst2요청의3후보가 목적 적합·실제 다른 시도였다는 판독, 전체18개의 인지 미확인을 계승했다. 101의 옛 후보 재탐색·A/B 재실행·합성 Typst 재실험·ImageMagick 오류/원 환경 복원은 하지 않았다. 접근한 것은 지정된 인계·연구 입력 및 이 과업의 공개 자료다. 다른 세션의 운영 상태를 변경하지 않았다. [인수 대사](evidence/start/inherited-reconciliation-summary.json).

## 3. 실제 변경과 묶음별 원격 봉인

| 파일 묶음 | 변경과 이유 | 확인 |
| --- | --- | --- |
| SCOPE.md·manifest.json·frame.csv·initial.csv | 모집/동일 조작/노출 계약,160최초판과22보조 적중의 범위·선별·미확인,12자리 초기 시도 | 초기8행은 de11fb2와 필드값 동일; 현재/최초 태그 차이·탈락 사유 보존 |
| proposals.csv·followup.csv | 시간순 첫 제안8 및 보조 지시대상4, 원 링크·한 부분 차이·180일 동일 주체 후속 | 제안12행은4a4aae1과 필드값 동일; 질문/후보/발언ID·시각 역추적 |
| returns.csv·RESULT.md | 세 필수표, 역할별 근거/반대 관측·한 줄·정확한 절·확인 질문, 두 모집틀의 분모 | 별도 판독으로 T/O·지시대상·Offset0 단위를 교정; 기계 대사 PASS |
| sources.jsonl·evidence/ | 원문 URL/GUID/commit·UTC·hash·절·실제 판독·실행 영수증·반례·독립 검토 | 원장304행, 필수24와 보수적 고유32, 중복/실패/연구자 실행 비산입 |
| reproduce.md·recalculate.py·SELF_CHECK.md | 고정 조회/정렬/재집계, 원 입력과 현재판 실행 구분, 미실시 명령·재개 입력, Q1–Q7 자가점검 | 깨끗한 결과 SHA에서 --check PASS; GitHub 고정판 재열람 |
| INDEX_PROPOSAL.md | 중앙 색인에 옮길 한 줄을 소유 경로에만 제안 | 중앙 색인과 dot-control.json은 수정하지 않음 |

| 단계 | 원격 SHA | 원격 확인 UTC | 변경 경로 기록 |
| --- | --- | --- | --- |
| 규칙 봉인 | `15ad66b68f974073d2a0ab880314a3130145c2c2` |2026-11-23T23:32:25.474872Z | [commits.jsonl](evidence/seals/commits.jsonl)의0단계 files |
| 묶음① 모집·초기 | `de11fb2b05c0e65cc1451826c720eebcbc3e52cd` |2026-11-23T23:43:05.543932Z | 같은 영수증의1단계 files |
| 묶음② 제안·보조4 | `4a4aae107be25f71318dbb0c7b7cfa73506c5030` |2026-11-24T00:04:06Z | 같은 영수증의2단계 changed_paths |
| 묶음③ 후속·공식·반례 | `242ccb21a00fb769b0bd40e54afc52f0a2f30fad` |2026-11-24T00:38:37Z | 같은 영수증의3단계 changed_paths |
| 묶음④ 결과·재집계·자가점검 | `9290320c1e9de33f30857af87640926c4d0f8cff` |2026-11-24T01:04:04.816824Z | 아래 결과 커밋 영수증의17경로 |
| 마지막 인계 | 이 파일만 포함하는 단독 후속 커밋 | 게시 뒤 최종 응답/커밋 메타데이터 확인 | `docs/workstreams/research/AF-RES-105/HANDOFF.md`만 |

직접 git push는 앞 단계에서 인증 정보 부재로 실패했다. GitHub 연결의 tree/commit/ref API로 예상 부모 lease를 걸어 게시한 뒤 git fetch·ls-remote로 원격을 확인했다. 묶음 사이 원격 확인 이후에만 다음 자료를 판독했다. 결과를 본 뒤 처음 선택을 바꾼 적은 없다. 보조 초기 열의 표현/출처ID 보완과 최종 표 교정은 [변경 내역](evidence/auxiliary/representation-corrections.json)에 남겼다.

## 4. 실제 검증과 고정 GitHub 재열람

결과 SHA `9290320c1e9de33f30857af87640926c4d0f8cff`의 detached worktree는 소유 경로의 무시되는 캐시 안에 만들었다. 각 명령 시작·종료에서 HEAD가 같고 git status가 깨끗했다. 검사 실행에 사용한 Python은3.12.14이며, native QGIS 연구 실행의 시스템 Python3.13.5와 구별한다.

| 명령 | UTC 시작→종료 | 종료값·범위 |
| --- | --- | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-105/manifest.json --fetch` |2026-11-24T01:04:37.283038Z→01:04:48.234917Z |0 / 명시한 작업 manifest **1개** PASS, remote_checked, outside_paths=[]·errors=[] |
| `python -B docs/workstreams/research/AF-RES-105/recalculate.py --check` |2026-11-24T01:04:48.241769Z→01:04:48.323571Z |0 / 봉인 초기8·제안12 불변,12사건/12후보,분모·24/32자료·ID/시각/중복 대사 PASS |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` |2026-11-24T01:04:48.330052Z→01:05:09.106694Z |0 / doctor·acceptance·research-case·original-smoke 명령 통과. sessions 명령 exit0이지만 실제 세션 검증은 **not-executed / no_active_sessions / count0** |

공통 acceptance 출력은 저장소55시험, repo-intake7시험, reference-audit9시험 통과를 포함한다. 이는 저장소 workbench 기능 검사다. 새 AI 세션이나 제품 추천 효과를 검증한 것은 아니다. `docs/tasks/*.json`만 자동 발견하므로 이 연구 manifest를 검사한 개별 명령1과 자동 발견0을 합쳐 쓰지 않는다. 아래에 실제 명령 영수증·공통 영수증과 stdout을 본문으로 보존한다. 커밋되지 않은 로컬 로그만을 전달 근거로 삼지 않는다.

GitHub 고정 결과판에서는 첫 세 표 전체, BL-T1 최초판·원 그림 위치, 보조4후속 전체, QGIS/GDAL 합성 출력 전체, 재현 절차 전체, 재집계의 봉인/분모/자료 수를 다시 열었다. 여섯 파일의 GitHub blob이 로컬 결과 commit의 blob과 모두 같았다. 재열람 UTC·URL·blob·읽은 범위는 아래 JSON에 있다. 검색 미리보기를 재열람으로 세지 않았다.

## 5. 판단·핵심 수치·미확인

| 지표 | 시간순 모집 | 진술 보조 모집 |
| --- | --- | --- |
| 선별 범위 | Blender80·QGIS80 최초판 직접 판독; 적격70/47, 제외10/33 | 고정26질의+API 닫힌 풀; 적중9/13=22사건 |
| 최종 단위 |8고유 질문·8후보·결원0 |4고유 질문·4후보·결원0; 시간순과 중복0 |
| 전체 조작 신규인지 | 분자0 / 판정 가능0 / 미확인8 | 분자0 / 판정 가능0 / 미확인4 |
| 좁은 변경 기능 신규인지 | 판정0·미확인8 | 신규2 / 판정2 / 미확인2; Compare Direction·GDAL with |
| 같은 고정 제안 실행 | 판정0·미확인8 | 실패 시험1·미확인3 |
| 반환 제안 | 기존 시도 표시3·질문4·유보1 | 같은 링크 다른 절1·질문2·유보1 |

전체 조작 신규인지와 ‘새로 배워 같은 조작을 뒤에 실행’은 판정 분모0이므로 **비율 산출 불가**다. 좁은 기능 신규2건을 전체 제안 신규인지로 올리지 않았고, 그 둘의 실행도 미확인이다. 보조 모집은 문구로 선별했으므로 인지 발생률·추천 효과율을 내지 않는다. 시간순8은 확인된 작성자6명+신원 미확인1자리이며 BL-T1/T2가 같은 사람이다. 보조4를 합쳐 확인된10명+미확인1자리다. [분모 대사](evidence/reconciliation.json).

필수 구성24=시간순 요청8+Blender 공식4+QGIS 공식4+두 프로젝트 상류2씩+Calc2+Audacity2를 채웠다. 보조 최초 요청·함수 도움말·GDAL·spdep의 추가8개를 합쳐 보수적 고유1차자료32개다. 같은 사건의 댓글·수정·첨부, 문서 anchor·미러, 실패 응답, 연구자 probe를 새 저작으로 늘리지 않았다. [자료 수](evidence/source-counts.json), [source ledger](sources.jsonl).

핵심 해석은 이미 아는 하위 단위와 바꾸라는 단계의 구분이다. BL-K1은 두 번째 Align을 안다고 했지만 Pivot Field를 확인하지 않았다. BL-N1은 Compare Direction만 새로 알았다고 말했다. QG-K1의 첫0.5 제안 실패와 다른 답의 성공, BL-T2의 첫 가중 curve 링크와 뒤 Power/remap 성공은 다른 대상이다. 추가 BL-C1은 기지 부분 뒤 다른 방법의 사용 보고를 지지하지만 BL-C2에서는 성공이 새인지보다 앞섰고 QG-C1의 뒤 방법은 다른 사람이 말했다. [반례 원장](evidence/auxiliary-counter/countercases.json).

원 작성자 정확한 설치판은12자리 모두 미확인이다. 감사·채택·점수·침묵은 원 사용자 실행 증거가 아니다. 공개 댓글 편집 이력, 삭제 자료, 당시 첨부 동일성, 정확한 프로젝트 입력/단위도 일부 미확인이다. QG-T1의 작성자ID가 없어서 타인 제안 대조도 미확인으로 남겼다. BL-N1의 현재 파일은 Direction/NotEqual/0, 그림은 GreaterThan/90°이고 본문3.6.5와 header400이 다르다. 기능 설명과 전체 예제의 적합성을 분리했다.

### 실패·미실시와 다시 실행할 입력

| 대상 | 실제 상태 | 실행할 명령·입력 / 첫 준비 |
| --- | --- | --- |
| Blender GN fixture2개 | 각각HTTP403, 바이트/expected geometry 미확인; 필수24에 비산입 | 아래 curl2개로 고정 test-data URL 재조회. 성공 때 먼저 hash/header·test_object/expected_object 확인. [상세 재현5절](evidence/blender-official/reproduce.md) |
| Blender C++ 상류2파일 | 입력·단언 직접 읽음; configure/build/suite 실행 미실시 | v4.0.2와 blob8a041845/0e99619d 고정. 실제 build에서 test binary를 확인한 뒤 아래 GTest filter 실행. 의존 library bundle·target 경로는 미확인. [상세4절](evidence/blender-official/reproduce.md) |
| QGIS3.34 상류2파일 | expression 단언·VRT/Warp 명령 기대값 읽음; 상류 suite 실행 미실시 | commitffbdd678의 개발 환경에서 `QT_QPA_PLATFORM=offscreen "$AF105_EXPRESSION_TEST_BIN" evaluation`; array('a','b','c')→a/빈배열→NULL. GDAL은 상세재현2.2의 동적 unittest runner로 testWarp/testBuildVrt, dem.tif·SEPARATE false/기본·resolution10 입력 |
| R/spdep | R/Rscript 없음, 독립 실행 미실시 | spdep1.3-2/commit46c90789, `Rscript --vanilla -`에 [재현3절](evidence/qgis-official/reproduce.md)의 네 단위사각형 코드를 입력. queen TRUE/FALSE·snap1e-9, 기대 무방향간선6/4는 아직 관측 아님 |
| Calc | 공식24.2.0.3와testFormulaRefUpdate의 입력·기대값 읽음, C++ 실행 미실시 | coreda48488의 준비된 빌드에서 해당 시험 실행 경로를 먼저 확인. A1=2, C3=A1, C4=$A$1, 앞 두 행 삽입/참조행 삭제 입력. 실제 target 명령 미확인, 추정 make target을 실행한 것으로 쓰지 않음 |
| Audacity | 매뉴얼3.6.4, 원 이슈3.1.3/3.3.3의 그림 판독; 앱/음원 측정 미실시 |3.1.3에서30초tone→10–20초envelope최저→AllowClipping+50dB Amplify3회; 대조는같은구간Ctrl+L뒤Amplify3회. 원주파수/envelope값·원음원미확인. [교차분야 재현](evidence/crossdomain/reproduce.md) |
| 원 작성자 환경·인지→실행 | 원 환경 복원은 제외 범위; 새로운 조작2건의 이후 실행 미확인 | 아래 다음 행동에서 같은 작성자의 공개 실행기록을 먼저 찾음. 없으면 새 연구층에서 사전·사후를 함께 수집 |

아래는 **미실행 재시도 명령**이다. 새 경로를 사용하고 다른 연구 산출물의 hash를 바꿔 맞추지 않는다.

```bash
export AF105_RETRY=/absolute/path/to/new/af105-retry
mkdir -p "$AF105_RETRY"
curl --fail --location --proto '=https' --max-time 60 --output "$AF105_RETRY/accumulate_field_column_grid.blend" 'https://projects.blender.org/blender/blender-test-data/raw/commit/221f67d71e370f251d39ea7d863b9e08a18094ed/modeling/geometry_nodes/utilities/accumulate_field_column_grid.blend'
curl --fail --location --proto '=https' --max-time 60 --output "$AF105_RETRY/sample_curves.blend" 'https://projects.blender.org/blender/blender-test-data/raw/commit/221f67d71e370f251d39ea7d863b9e08a18094ed/modeling/geometry_nodes/curves/sample_curves.blend'
```

Blender v4.0.2의 호환 의존성과 실제 test binary가 확인된 뒤에만 다음을 실행한다. test 선택0은 성공으로 세지 않는다.

```bash
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_list_tests
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_filter='math_rotation.RotateDirectionAroundAxis:math_rotation.QuaternionAngleBetween:math_rotation.QuaternionFromVector:math_rotation.QuaternionFromTracking'
"$AF105_BLENDER_BUILD/bin/blender_test" --gtest_filter='math_vector.InterpolateInt:math_vector.InterpolateFloat:math_vector.sqrt:math_vector.safe_sqrt:math_vector.rcp:math_vector.safe_rcp'
```

입력은 해당 고정 C++ 파일에 있다. 예: 방향(1,0,0)/Z축/π/2→기대(0,1,0), interpolate A(40,-100,50)·B(20,100,100)·factor0.5→기대(30,0,75). 이것은 GN 통합graph나 원 사용자 결과를 대신하지 않는다.

실제 수행한 현재판 Blender3probe, QGIS2label probe, QGIS/GDAL 함수·단위·수명 비교의 명령/입출력은 커밋된 영수증을 사용한다. QGIS 최초 enum 오류와 이후 수정 성공, GDAL 문서 리터럴의 괄호 오류, 옛URL404, 잘못 짚은 QGIS 시험경로404는 남겨 두었다. 실패 응답은 고유자료 수에서 제외했다. 새 실행과 읽기만 한 상류 단언을 혼동하지 않는다.

### 검토의 독립성

초기 Blender/QGIS는 분리된 새 문맥 판독자가80건씩 읽었다. 별도 감사 에이전트가 초기 일부·주체/시간/후속·자료 계보·최종 RESULT 전체·SELF_CHECK 전체를 대조하여 FT-F1~F5를 찾아 수정 확인했다. 그 감사자가 작성한 QGIS 보조/타 분야의 재검토는 자기검토다. root는 초기 채택 metadata 일부 노출이 있어 완전 맹검이 아니며, 전160건 이중 판독·외부 인간 검토·실제 역할별 판독 실험은 미실시다. [최종 별도 검토](evidence/independent-review/final-tables-review.md), [기계 영수증](evidence/independent-review/final-tables-review.json).

공개 원문은 위치·해시·짧은 인용·판독만 커밋했고 전체 저작/바이너리는 저장소에 다시 게시하지 않았다. 라이선스 전체 재배포를 새로 승인한 것이 아니다. 개인 신원은 공개 사건의 동일인 대조에 필요한 숫자ID만 사용했다. 별도 비용 구매·운영 서비스 변경은 없다.

## 6. 다음 대화의 첫 행동과 색인 제안

1. `work/research-af-res-105`의 최신 SHA를 다시 조회하고 이 HANDOFF가 가리키는 결과 SHA와 비교한다. 결과 이후 차이가 HANDOFF 한 파일인지 먼저 확인한다.
2. 결과를 재검사하려면 `9290320c1e9de33f30857af87640926c4d0f8cff`를 checkout하여 위 두 지정 명령과 `recalculate.py --check`를 실행한다. 현재 브랜치 tip을 과거 검사 대상 SHA로 부르지 않는다.
3. **첫 구체 조사:** BL-N1 [답313661](https://blender.stackexchange.com/questions/313644/313661#313661)의 현재 `.blend` [oDnRekJL](https://blend-exchange.com/b/oDnRekJL/)과 [작성자543409](https://blender.stackexchange.com/questions/313644#comment543409_313661)를 대조한다. 당시 보존 파일을 얻으면 Direction의 연산/각도, 실제 판, 같은 입력의 결과를 기록해 전체 예제 유보를 재평가한다. 다음은 QG-N1의GDAL판과with후속 실행이다.
4. 다음 조사 ID는 미배정이다. 입력은 위 결과 SHA, 기존12슬롯은 보존한다. 새 공개 자료가 없으면 미확인 상태를 유지하고 새 사전등록 모집에서 사전 조작·직후 실행을 함께 수집한다.
5. 추가 승인 요청은 없다. 이 연구는 기존 허용 범위 안에서 완료됐다. 의존은 AF-RES-101 운영b29c25fe/연구392ff3d6 고정이다. 새 채팅이 이 파일을 자동 기억하거나 읽는다고 가정하지 않는다.

소유 경로의 [INDEX_PROPOSAL.md](INDEX_PROPOSAL.md)에 저장한 색인 제안 한 줄:

| AF-RES-105 | 익숙한 제품과 이미 시도한 조작의 구분: 시간순8·진술4, 신규 기능2/전체 새로움 분모0 | REVIEW_READY | [RESULT](docs/workstreams/research/AF-RES-105/RESULT.md) | AF-RES-101 운영b29c25fe / 연구입력392ff3d6 고정 |

## 7. 커밋되는 실제 완료 영수증

다음 JSON과 stdout은 결과 SHA 검사·재열람 이후 읽은 실제 기록이다. 로컬 경로는 당시 실행 위치를 설명하며 별도 다운로드 파일을 약속하지 않는다. 이 본문에 포함된 기록 자체가 마지막 HANDOFF 커밋에 저장된다.

### 결과 커밋과 변경 경로

```json
{
  "remote_sha": "9290320c1e9de33f30857af87640926c4d0f8cff",
  "remote_verified_utc": "2026-11-24T01:04:04.816824+00:00",
  "remote_ref": "refs/heads/work/research-af-res-105",
  "parent_sha": "242ccb21a00fb769b0bd40e54afc52f0a2f30fad",
  "tree_sha": "555daca1775bcc3cb103368d433a9d2ece4e80b6",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-105/INDEX_PROPOSAL.md",
    "docs/workstreams/research/AF-RES-105/RESULT.md",
    "docs/workstreams/research/AF-RES-105/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-105/build_result.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/representation-corrections.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/final-tables-review.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/final-tables-review.md",
    "docs/workstreams/research/AF-RES-105/evidence/reconciliation.json",
    "docs/workstreams/research/AF-RES-105/evidence/result-tables.md",
    "docs/workstreams/research/AF-RES-105/evidence/return-perspectives.json",
    "docs/workstreams/research/AF-RES-105/evidence/seals/commits.jsonl",
    "docs/workstreams/research/AF-RES-105/merge_sources.py",
    "docs/workstreams/research/AF-RES-105/recalculate.py",
    "docs/workstreams/research/AF-RES-105/reproduce.md",
    "docs/workstreams/research/AF-RES-105/returns.csv",
    "docs/workstreams/research/AF-RES-105/sources.jsonl",
    "docs/workstreams/research/AF-RES-105/write_reports.py"
  ],
  "clean_after_sync": true,
  "transport": "GitHub tree/commit/ref expected-parent lease; git fetch and ls-remote"
}
```

### 실제 명령·UTC·종료값·출력 지문

```json
[
  {
    "name": "task-session",
    "command": [
      "python",
      "-B",
      "-m",
      "workbench.session",
      "check",
      "docs/workstreams/research/AF-RES-105/manifest.json",
      "--fetch"
    ],
    "cwd": "/workspace/scratch/fb980e912f69/agentflow-open/docs/workstreams/research/AF-RES-105/.cache/result-check-9290320",
    "result_sha": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "started_utc": "2026-11-24T01:04:37.283038+00:00",
    "clean_before": true,
    "ended_utc": "2026-11-24T01:04:48.234917+00:00",
    "exit_code": 0,
    "clean_after": true,
    "head_after": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "stdout_sha256": "68f4f7a13cf37aa30311ed232b8e9b5dd7d170a907295ec5addec9a85c6e1aa7",
    "stdout_bytes": 13953,
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "stderr_bytes": 0
  },
  {
    "name": "research-reconciliation",
    "command": [
      "python",
      "-B",
      "docs/workstreams/research/AF-RES-105/recalculate.py",
      "--check"
    ],
    "cwd": "/workspace/scratch/fb980e912f69/agentflow-open/docs/workstreams/research/AF-RES-105/.cache/result-check-9290320",
    "result_sha": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "started_utc": "2026-11-24T01:04:48.241769+00:00",
    "clean_before": true,
    "ended_utc": "2026-11-24T01:04:48.323571+00:00",
    "exit_code": 0,
    "clean_after": true,
    "head_after": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "stdout_sha256": "680ec33f425189b5226eafe0190f8a8b35f4b493b79c0a46dc4b56499fb2e282",
    "stdout_bytes": 1825,
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "stderr_bytes": 0
  },
  {
    "name": "common-cloud",
    "command": [
      "python",
      "-B",
      "scripts/cloud_check.py",
      "--environment",
      "codex-cloud",
      "--fetch-contract",
      "--require-clean"
    ],
    "cwd": "/workspace/scratch/fb980e912f69/agentflow-open/docs/workstreams/research/AF-RES-105/.cache/result-check-9290320",
    "result_sha": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "started_utc": "2026-11-24T01:04:48.330052+00:00",
    "clean_before": true,
    "ended_utc": "2026-11-24T01:05:09.106694+00:00",
    "exit_code": 0,
    "clean_after": true,
    "head_after": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "stdout_sha256": "c92b2cd96a466f8a68b19413fe6fab060cfe8d95e8a0f4758ecb30af5ca1e61c",
    "stdout_bytes": 14975,
    "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "stderr_bytes": 0
  }
]
```

### 개별 manifest 검사 결과

```json
{
  "status": "passed",
  "task_id": "af-res-105",
  "freshness": "remote_checked",
  "checked_at": "2026-11-24T01:04:48.225277+00:00",
  "checked_out_commit": "9290320c1e9de33f30857af87640926c4d0f8cff",
  "task_base_commit": "32b6bb32989730df78d521c29a50dbebd3289b46",
  "integration_commit": "8916e31c275f6076f8367e95d7ca36d48a28e0e4",
  "scope_base_commit": "32b6bb32989730df78d521c29a50dbebd3289b46",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc",
  "changed_paths": [
    "docs/workstreams/research/AF-RES-105/.gitignore",
    "docs/workstreams/research/AF-RES-105/INDEX_PROPOSAL.md",
    "docs/workstreams/research/AF-RES-105/RESULT.md",
    "docs/workstreams/research/AF-RES-105/SCOPE.md",
    "docs/workstreams/research/AF-RES-105/SELF_CHECK.md",
    "docs/workstreams/research/AF-RES-105/acquire_episodes.py",
    "docs/workstreams/research/AF-RES-105/assemble_stage2.py",
    "docs/workstreams/research/AF-RES-105/assemble_stage3.py",
    "docs/workstreams/research/AF-RES-105/build_auxiliary_followup.py",
    "docs/workstreams/research/AF-RES-105/build_blender_auxiliary.py",
    "docs/workstreams/research/AF-RES-105/build_result.py",
    "docs/workstreams/research/AF-RES-105/enrich_acquisition.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-counter/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-counter/countercases.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-counter/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/blend-headers.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/blend-inspection.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/current-endorsements.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/execution-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/followup-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/inspect_blends.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/analysis.md",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/execution-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/probe-results.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/probe_semantics.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/blender-engine-corpus-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/engine-question-screen.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/expand_frame.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/expand_initial_fields.py",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/gis-engine-corpus-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/pool-close.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/representation-corrections.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/search-results.json",
    "docs/workstreams/research/AF-RES-105/evidence/auxiliary/stage2-reconciliation.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/auxiliary-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/exposure-note.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/image-reading.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/initial-addenda.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/screening.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-auxiliary/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-episodes/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-episodes/frame-corpus-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/artifact-header-receipts.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/artifact-inspection.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/coverage-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/followup-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/inspect_originals.py",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/native-inspection-command-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-followup/validation-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/frame-part.csv",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/image-reading.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/initial-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-initial/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/controlled-probes-command-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/controlled-probes-result.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/controlled_probes.py",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/official-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/reproduce.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-official/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/exposure-note.md",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/image-reading.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/order-log.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/preproposal-addenda.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/proposals-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/blender-proposals/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/counting.json",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/findings.md",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/original-examples.json",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/pins.json",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/read_source.py",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/reproduce.md",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/crossdomain/verification.json",
    "docs/workstreams/research/AF-RES-105/evidence/endorsements/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/endorsements/current-metadata.json",
    "docs/workstreams/research/AF-RES-105/evidence/endorsements/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/final-tables-review.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/final-tables-review.md",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/phase1-denominators.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/phase1-method-review.md",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/resolutions.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/source-audit.json",
    "docs/workstreams/research/AF-RES-105/evidence/independent-review/source-audit.md",
    "docs/workstreams/research/AF-RES-105/evidence/initial-summary.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/auxiliary-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/exposure.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/initial-addenda.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/proposal-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/screening.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-auxiliary/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-episodes/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-episodes/frame-corpus-receipt.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-followup/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-followup/followup-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-followup/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-followup/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-followup/validation.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/boundary-check.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/frame-part.csv",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/initial-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/preseal-adjudication.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/screened-sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-initial/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/native-probe-attempts.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/native-probe-results.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/native_probe.py",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/official-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/reading-notes.md",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/reproduce.md",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-official/upstream-examples.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/acquisition.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/exposure-note.md",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/orderlog.csv",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/preproposal-addenda.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/proposals-part.json",
    "docs/workstreams/research/AF-RES-105/evidence/qgis-proposals/sources-part.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/reconciliation.json",
    "docs/workstreams/research/AF-RES-105/evidence/result-tables.md",
    "docs/workstreams/research/AF-RES-105/evidence/return-perspectives.json",
    "docs/workstreams/research/AF-RES-105/evidence/seals/commits.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/source-counts.json",
    "docs/workstreams/research/AF-RES-105/evidence/start/auxiliary-search-plan.json",
    "docs/workstreams/research/AF-RES-105/evidence/start/contract-read.json",
    "docs/workstreams/research/AF-RES-105/evidence/start/exposure-log.jsonl",
    "docs/workstreams/research/AF-RES-105/evidence/start/inherited-reconciliation-summary.json",
    "docs/workstreams/research/AF-RES-105/evidence/start/initial-independent-review.md",
    "docs/workstreams/research/AF-RES-105/evidence/start/method-review.md",
    "docs/workstreams/research/AF-RES-105/followup.csv",
    "docs/workstreams/research/AF-RES-105/frame.csv",
    "docs/workstreams/research/AF-RES-105/initial.csv",
    "docs/workstreams/research/AF-RES-105/merge_sources.py",
    "docs/workstreams/research/AF-RES-105/prepare_publish.py",
    "docs/workstreams/research/AF-RES-105/proposals.csv",
    "docs/workstreams/research/AF-RES-105/recalculate.py",
    "docs/workstreams/research/AF-RES-105/reproduce.md",
    "docs/workstreams/research/AF-RES-105/research_io.py",
    "docs/workstreams/research/AF-RES-105/returns.csv",
    "docs/workstreams/research/AF-RES-105/sources.jsonl",
    "docs/workstreams/research/AF-RES-105/write_reports.py"
  ],
  "outside_paths": [],
  "unmerged_paths": [],
  "errors": [],
  "boundary": "Git contract and ownership checks; not a new AI chat or product verification"
}
```

### 공통 검사 구조화 영수증

```json
{
  "schema": 1,
  "scope": "workbench checks, not product or browser integration",
  "environment": "codex-cloud",
  "environment_is_caller_label": true,
  "platform": "Linux-6.18.57-x86_64-with-glibc2.41",
  "python": "3.12.14",
  "started_at": "2026-11-24T01:04:48+00:00",
  "completed_at": "2026-11-24T01:05:09+00:00",
  "status": "passed",
  "exit_code": 0,
  "source_start": {
    "commit": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "dirty": false,
    "clean": true
  },
  "github": {
    "event_name": null,
    "event_sha": null,
    "run_id": null,
    "run_attempt": null,
    "pr_head_sha": null,
    "pr_base_sha": null,
    "checked_out_sha": "9290320c1e9de33f30857af87640926c4d0f8cff"
  },
  "contract_fetch_requested": true,
  "require_clean": true,
  "checks": [
    {
      "name": "doctor",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "-m",
        "workbench",
        "doctor"
      ],
      "timeout_seconds": 30,
      "started_at": "2026-11-24T01:04:48+00:00",
      "status": "passed",
      "exit_code": 0,
      "completed_at": "2026-11-24T01:04:48+00:00",
      "stdout_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/doctor.stdout.log",
      "stderr_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/doctor.stderr.log"
    },
    {
      "name": "acceptance",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "scripts/check.py",
        "--require-git"
      ],
      "timeout_seconds": 420,
      "started_at": "2026-11-24T01:04:48+00:00",
      "status": "passed",
      "exit_code": 0,
      "completed_at": "2026-11-24T01:05:08+00:00",
      "stdout_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/acceptance.stdout.log",
      "stderr_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/acceptance.stderr.log"
    },
    {
      "name": "research-case",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "-m",
        "workbench",
        "run",
        "reference-audit",
        "discovery"
      ],
      "timeout_seconds": 60,
      "started_at": "2026-11-24T01:05:08+00:00",
      "status": "passed",
      "exit_code": 0,
      "completed_at": "2026-11-24T01:05:08+00:00",
      "stdout_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/research-case.stdout.log",
      "stderr_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/research-case.stderr.log"
    },
    {
      "name": "original-smoke",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "workbench/verify.py"
      ],
      "timeout_seconds": 30,
      "started_at": "2026-11-24T01:05:08+00:00",
      "status": "passed",
      "exit_code": 0,
      "completed_at": "2026-11-24T01:05:09+00:00",
      "stdout_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/original-smoke.stdout.log",
      "stderr_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/original-smoke.stderr.log"
    },
    {
      "name": "sessions",
      "command": [
        "/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python",
        "-m",
        "workbench.session",
        "check-all",
        "--fetch"
      ],
      "timeout_seconds": 60,
      "started_at": "2026-11-24T01:05:09+00:00",
      "status": "passed",
      "exit_code": 0,
      "completed_at": "2026-11-24T01:05:09+00:00",
      "stdout_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/sessions.stdout.log",
      "stderr_log": ".workbench/cloud-check-logs/026f36fac3364303b9ce857f111fb619/sessions.stderr.log"
    }
  ],
  "session_validation": {
    "status": "not-executed",
    "reason": "no_active_sessions",
    "count": 0,
    "freshness": "not_checked",
    "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
  },
  "source_end": {
    "commit": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "dirty": false,
    "clean": true
  }
}
```

### GitHub 고정판 재열람 영수증

```json
{
  "result_sha": "9290320c1e9de33f30857af87640926c4d0f8cff",
  "items": [
    {
      "path": "RESULT.md",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/RESULT.md",
      "blob_sha": "f73f64f277d7b3a72a2e1487317c8b9763cc8a29",
      "read_scope": "all three required opening tables, lines1–46",
      "read_confirmed_utc": "2026-11-24T01:06:52.970Z",
      "time_precision": "confirmation recorded after tool content was read; HTTP start not separately recorded",
      "matches_result_git_blob": true
    },
    {
      "path": "evidence/blender-initial/initial-part.json",
      "started_utc": "2026-11-24T01:06:45.171Z",
      "completed_utc": "2026-11-24T01:06:45.847Z",
      "blob_sha": "65ebfd81192e5403f59d244ce7119de14705a499",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/evidence/blender-initial/initial-part.json",
      "read_scope": "BL-T1 initial case and source locators",
      "matches_result_git_blob": true
    },
    {
      "path": "evidence/auxiliary-followup/followup-part.json",
      "started_utc": "2026-11-24T01:06:45.171Z",
      "completed_utc": "2026-11-24T01:06:45.847Z",
      "blob_sha": "c3cd9374b3f5409af9b829a0c6aa9cbdc7f2b125",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/evidence/auxiliary-followup/followup-part.json",
      "read_scope": "full file",
      "matches_result_git_blob": true
    },
    {
      "path": "evidence/auxiliary-official/probe-results.json",
      "started_utc": "2026-11-24T01:06:45.171Z",
      "completed_utc": "2026-11-24T01:06:45.847Z",
      "blob_sha": "d7bea7c7d9c24cf123013d2686612fa17d80fc35",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/evidence/auxiliary-official/probe-results.json",
      "read_scope": "full file",
      "matches_result_git_blob": true
    },
    {
      "path": "reproduce.md",
      "started_utc": "2026-11-24T01:06:45.171Z",
      "completed_utc": "2026-11-24T01:06:45.847Z",
      "blob_sha": "c1a0987fec9c981b44e6aef3950a3903078d6a73",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/reproduce.md",
      "read_scope": "full file",
      "read_completed_utc": "2026-11-24T01:06:52.970Z",
      "matches_result_git_blob": true
    },
    {
      "path": "evidence/reconciliation.json",
      "started_utc": "2026-11-24T01:06:45.171Z",
      "completed_utc": "2026-11-24T01:06:45.847Z",
      "blob_sha": "a56cf986a48f24ed566336bcada55dc94605709b",
      "url": "https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/evidence/reconciliation.json",
      "read_scope": "status, frozen choices, per-frame denominators, minima",
      "matches_result_git_blob": true
    }
  ],
  "blob_verified_utc": "2026-11-24T01:08:33.961304+00:00"
}
```

### 필수 검사 stdout 원문

명시 manifest의 stdout은 위 JSON과 같다. 세 명령의 stderr는 모두0byte였다. 아래는 공통 검사에서 실제 반환된 stdout 전체다.

```text
[doctor] passed (exit 0)
{
  "python": "3.12.14",
  "supported": true,
  "projects": [
    "repo-intake",
    "reference-audit"
  ],
  "git": {
    "commit": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "dirty": false
  },
  "network_required": false,
  "agent_daemon": false
}
[acceptance] passed (exit 0)
test_registered_third_project_is_not_implicitly_executed (test_acceptance_scope.AcceptanceScopeTests.test_registered_third_project_is_not_implicitly_executed) ... ok
test_clean_gate_rejects_tracked_child_mutation_and_dirty_restart (test_cloud_check.CloudCheckEvidenceTests.test_clean_gate_rejects_tracked_child_mutation_and_dirty_restart) ... ok
test_github_context_keeps_shas_without_copying_secrets (test_cloud_check.CloudCheckEvidenceTests.test_github_context_keeps_shas_without_copying_secrets) ... ok
test_no_active_sessions_is_preserved_as_not_executed (test_cloud_check.CloudCheckEvidenceTests.test_no_active_sessions_is_preserved_as_not_executed) ... ok
test_nonzero_retains_output_and_stops_later_checks (test_cloud_check.CloudCheckEvidenceTests.test_nonzero_retains_output_and_stops_later_checks) ... ok
test_timeout_is_nonzero_and_has_a_completed_receipt (test_cloud_check.CloudCheckEvidenceTests.test_timeout_is_nonzero_and_has_a_completed_receipt) ... ok
test_workspace_alias_uses_one_canonical_root (test_path_alias.WorkspaceAliasTests.test_workspace_alias_uses_one_canonical_root) ... ok
test_bad_source_shapes_rejected (test_runtime.RuntimeTests.test_bad_source_shapes_rejected) ... ok
test_big_context_rejected (test_runtime.RuntimeTests.test_big_context_rejected) ... ok
test_budget_and_omissions_explicit (test_runtime.RuntimeTests.test_budget_and_omissions_explicit) ... ok
test_context_contains_own_not_other_project (test_runtime.RuntimeTests.test_context_contains_own_not_other_project) ... ok
test_context_search_finds_decision (test_runtime.RuntimeTests.test_context_search_finds_decision) ... ok
test_deleted_input_still_leaves_failure_receipt (test_runtime.RuntimeTests.test_deleted_input_still_leaves_failure_receipt) ... ok
test_duplicate_source_id_rejected (test_runtime.RuntimeTests.test_duplicate_source_id_rejected) ... ok
test_export_excludes_other_project_and_secrets (test_runtime.RuntimeTests.test_export_excludes_other_project_and_secrets) ... ok
test_export_rejects_workspace_child (test_runtime.RuntimeTests.test_export_rejects_workspace_child) ... ok
test_export_runs_without_original_pythonpath (test_runtime.RuntimeTests.test_export_runs_without_original_pythonpath) ... ok
test_export_will_not_overwrite (test_runtime.RuntimeTests.test_export_will_not_overwrite) ... ok
test_impossible_budget_is_not_silent (test_runtime.RuntimeTests.test_impossible_budget_is_not_silent) ... ok
test_manifest_context_cannot_escape (test_runtime.RuntimeTests.test_manifest_context_cannot_escape) ... ok
test_manifest_rejects_arbitrary_shell (test_runtime.RuntimeTests.test_manifest_rejects_arbitrary_shell) ... ok
test_manifest_rejects_unbounded_timeout (test_runtime.RuntimeTests.test_manifest_rejects_unbounded_timeout) ... ok
test_missing_context_file (test_runtime.RuntimeTests.test_missing_context_file) ... ok
test_nonzero_exit_is_not_passed (test_runtime.RuntimeTests.test_nonzero_exit_is_not_passed) ... ok
test_project_identity_mismatch (test_runtime.RuntimeTests.test_project_identity_mismatch) ... ok
test_project_registry (test_runtime.RuntimeTests.test_project_registry) ... ok
test_receipt_altered_log_detected (test_runtime.RuntimeTests.test_receipt_altered_log_detected) ... ok
test_receipt_other_project_rejected (test_runtime.RuntimeTests.test_receipt_other_project_rejected) ... ok
test_receipt_stale_after_source_edit (test_runtime.RuntimeTests.test_receipt_stale_after_source_edit) ... ok
test_receipt_success_and_verify (test_runtime.RuntimeTests.test_receipt_success_and_verify) ... ok
test_reject_parent_and_absolute_paths (test_runtime.RuntimeTests.test_reject_parent_and_absolute_paths) ... ok
test_reject_symlink_escape (test_runtime.RuntimeTests.test_reject_symlink_escape) ... ok
test_source_empty_credentials_rejected (test_runtime.RuntimeTests.test_source_empty_credentials_rejected) ... ok
test_sources_validate (test_runtime.RuntimeTests.test_sources_validate) ... ok
test_task_cannot_mutate_inputs_and_claim_pass (test_runtime.RuntimeTests.test_task_cannot_mutate_inputs_and_claim_pass) ... ok
test_timeout_is_not_retried (test_runtime.RuntimeTests.test_timeout_is_not_retried) ... ok
test_unknown_project (test_runtime.RuntimeTests.test_unknown_project) ... ok
test_unknown_search_keeps_required_handover (test_runtime.RuntimeTests.test_unknown_search_keeps_required_handover) ... ok
test_unknown_task (test_runtime.RuntimeTests.test_unknown_task) ... ok
test_changed_task_cannot_use_itself_as_the_baseline (test_session.SessionTests.test_changed_task_cannot_use_itself_as_the_baseline) ... ok
test_cli_creates_a_manifest_once_without_overwriting_it (test_session.SessionTests.test_cli_creates_a_manifest_once_without_overwriting_it) ... ok
test_committed_and_untracked_out_of_scope_changes_fail (test_session.SessionTests.test_committed_and_untracked_out_of_scope_changes_fail) ... ok
test_conflicting_worktree_merge_fails_and_can_be_aborted (test_session.SessionTests.test_conflicting_worktree_merge_fails_and_can_be_aborted) ... ok
test_empty_queue_is_not_a_collaboration_pass (test_session.SessionTests.test_empty_queue_is_not_a_collaboration_pass) ... ok
test_exact_dependency_pin_detects_a_new_remote_result (test_session.SessionTests.test_exact_dependency_pin_detects_a_new_remote_result) ... ok
test_ignored_run_outputs_do_not_become_task_changes (test_session.SessionTests.test_ignored_run_outputs_do_not_become_task_changes) ... ok
test_independent_worktrees_merge_without_borrowing_ownership (test_session.SessionTests.test_independent_worktrees_merge_without_borrowing_ownership) ... ok
test_remote_contract_drift_without_version_bump_is_detected (test_session.SessionTests.test_remote_contract_drift_without_version_bump_is_detected) ... ok
test_reusing_an_integrated_task_for_new_changes_requires_a_new_pin (test_session.SessionTests.test_reusing_an_integrated_task_for_new_changes_requires_a_new_pin) ... ok
test_duplicate (test_verify.SourceValidationTests.test_duplicate) ... ok
test_empty (test_verify.SourceValidationTests.test_empty) ... ok
test_invalid_date (test_verify.SourceValidationTests.test_invalid_date) ... ok
test_invalid_evidence (test_verify.SourceValidationTests.test_invalid_evidence) ... ok
test_invalid_urls (test_verify.SourceValidationTests.test_invalid_urls) ... ok
test_valid (test_verify.SourceValidationTests.test_valid) ... ok

----------------------------------------------------------------------
Ran 55 tests in 4.990s

OK

=== repo-intake/test stdout ===

=== repo-intake/test stderr ===
test_bad_input_container (test_task.RepositoryIdentityTests.test_bad_input_container) ... ok
test_clone_aliases (test_task.RepositoryIdentityTests.test_clone_aliases) ... ok
test_collect_preserves_indices (test_task.RepositoryIdentityTests.test_collect_preserves_indices) ... ok
test_distinct_owner_not_merged (test_task.RepositoryIdentityTests.test_distinct_owner_not_merged) ... ok
test_idempotent_canonical_identity (test_task.RepositoryIdentityTests.test_idempotent_canonical_identity) ... ok
test_reject_ambiguous_or_deceptive (test_task.RepositoryIdentityTests.test_reject_ambiguous_or_deceptive) ... ok
test_rejected_credentials_not_echoed (test_task.RepositoryIdentityTests.test_rejected_credentials_not_echoed) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK

=== repo-intake/demo stdout ===
{
  "repositories": [
    {
      "key": "github.com/other-owner/cpython",
      "input_indices": [
        7
      ]
    },
    {
      "key": "github.com/psf/requests",
      "input_indices": [
        5
      ]
    },
    {
      "key": "github.com/python/cpython",
      "input_indices": [
        0,
        1,
        2
      ]
    }
  ],
  "rejected": [
    {
      "index": 3,
      "reason": "expected exactly /owner/repository, not a subpage"
    },
    {
      "index": 4,
      "reason": "only GitHub repository roots are supported"
    },
    {
      "index": 6,
      "reason": "queries, fragments and encoded paths need manual review"
    }
  ],
  "input_count": 8,
  "existence_checked": false
}

=== repo-intake/demo stderr ===

=== reference-audit/test stdout ===

=== reference-audit/test stderr ===
test_does_not_collapse_subpages (test_task.ReferenceTests.test_does_not_collapse_subpages) ... ok
test_duplicate_id (test_task.ReferenceTests.test_duplicate_id) ... ok
test_invalid_id (test_task.ReferenceTests.test_invalid_id) ... ok
test_invalid_input (test_task.ReferenceTests.test_invalid_input) ... ok
test_missing_source (test_task.ReferenceTests.test_missing_source) ... ok
test_repeated_marker (test_task.ReferenceTests.test_repeated_marker) ... ok
test_reuses_root_identity (test_task.ReferenceTests.test_reuses_root_identity) ... ok
test_unused (test_task.ReferenceTests.test_unused) ... ok
test_valid_reference (test_task.ReferenceTests.test_valid_reference) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK

=== reference-audit/demo stdout ===
{
  "ok": true,
  "errors": [],
  "used": [
    "api-doc",
    "upstream"
  ],
  "unused": [
    "alternate-clone"
  ],
  "duplicate_repository_sources": {
    "github.com/python/cpython": [
      "upstream",
      "alternate-clone"
    ]
  },
  "claim_truth_checked": false,
  "network_accessed": false
}

=== reference-audit/demo stderr ===

WORKBENCH_ACCEPTANCE={"backup": {"commit": "9290320c1e9de33f30857af87640926c4d0f8cff", "scope": "Git objects and refs only; not issues, secrets, DB, LFS or untracked files", "sha256": "30e3ca5873a7ef363d5b267b07916e520d3fa6c40f06f5ba82dbd7bc8a9ac33a", "status": "passed"}, "exports": {"reference-audit": {"other_project_absent": true, "shared_helper_sha256": "5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a", "status": "passed"}, "repo-intake": {"other_project_absent": true, "shared_helper_sha256": "5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a", "status": "passed"}}, "new_model_session_tested": false, "projects": {"reference-audit": {"context_files": ["lab/reference-audit/STATE.md", "lab/reference-audit/BRIEF.md", "lab/reference-audit/RESEARCH.md", "lab/reference-audit/DECISIONS.md", "lab/reference-audit/sources.json"], "context_process": "fresh process, not a fresh AI session", "runs": [{"id": "20261124T010454Z-6677cff8bd57", "receipt": ".workbench/runs/reference-audit/20261124T010454Z-6677cff8bd57/receipt.json", "status": "passed", "task": "test"}, {"id": "20261124T010454Z-bb06a0675abc", "receipt": ".workbench/runs/reference-audit/20261124T010454Z-bb06a0675abc/receipt.json", "status": "passed", "task": "demo"}], "source_records": 4}, "repo-intake": {"context_files": ["lab/repo-intake/STATE.md", "lab/repo-intake/BRIEF.md", "lab/repo-intake/RESEARCH.md", "lab/repo-intake/DECISIONS.md", "lab/repo-intake/sources.json"], "context_process": "fresh process, not a fresh AI session", "runs": [{"id": "20261124T010453Z-1a2e4f44a94d", "receipt": ".workbench/runs/repo-intake/20261124T010453Z-1a2e4f44a94d/receipt.json", "status": "passed", "task": "test"}, {"id": "20261124T010453Z-c22230b6338c", "receipt": ".workbench/runs/repo-intake/20261124T010453Z-c22230b6338c/receipt.json", "status": "passed", "task": "demo"}], "source_records": 4}}, "python": "3.12.14", "schema": 1, "scope": "workbench acceptance, not discovery product", "source": {"commit": "9290320c1e9de33f30857af87640926c4d0f8cff", "dirty": false}, "status": "passed"}

[research-case] passed (exit 0)
{
  "schema": 1,
  "id": "20261124T010508Z-430f13f46784",
  "project": "reference-audit",
  "task": "discovery",
  "status": "passed",
  "returncode": 0,
  "attempts": 1,
  "tracking_error": null,
  "duration_seconds": 0.041,
  "inputs": {
    "lab/reference-audit/fixtures/discovery.json": "52f87db095173ee92dad09d034dbc3b3176274988a87f80787127ccdd36a3c90",
    "lab/reference-audit/fixtures/input.json": "e6e6f211dde2a9184a41a0078c6bb8b8f9ce1afae08017af42ea0511710ec8c4",
    "lab/reference-audit/project.json": "f8f6667a31347e33472677280e218d44780ff58c1669dc0a0f2d145ac50400e8",
    "lab/reference-audit/sources.json": "06c9b569f2237370cab87c948a655bd8c7079705ad29639acb56006c079afec4",
    "lab/reference-audit/task.py": "aa01a78fb057d55dbcd48a87f346fbc6dae2c4a6607312986bc927d4b66faf5d",
    "lab/reference-audit/test_task.py": "2155a3ed4260dcb8084f81c69387dbc947bf37c2aeb5685044cd07d38c03d5b7",
    "workbench/__init__.py": "c89288e0f257f46b5cfe1a8fb3f78cfe49f899cc82427bc9597aab3128ce4e20",
    "workbench/__main__.py": "935a1c1166b0c1ea35a82256345000bf2c73ded718d77773bc27a71ecce28f7d",
    "workbench/cli.py": "02087f34d697ef8de35473410ea684b73e5b2bc3179a3f8ca88f369ad3784ced",
    "workbench/urls.py": "5a26bd94f4aef02132d2f1f7840d6820f339d7caa7dd8d8b8d064cb679ac151a"
  },
  "source": {
    "commit": "9290320c1e9de33f30857af87640926c4d0f8cff",
    "dirty": false
  },
  "python": "3.12.14",
  "workflow_run": null,
  "stdout_sha256": "dc664ddf420fc08386ae3d4cefd2ef42ee59ebaf5bdafcbd44430c10f4ff7a8c",
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "boundary": "trusted repository tasks, not a sandbox or factual certification",
  "receipt": ".workbench/runs/reference-audit/20261124T010508Z-430f13f46784/receipt.json"
}
[original-smoke] passed (exit 0)
WORKBENCH_RECEIPT={"challenge": "agentflow-workbench-roundtrip-001", "checked_files": ["AGENTS.md", "STATE.md", "docs/WORKBENCH.md", "workbench/sources.json"], "commit": "9290320c1e9de33f30857af87640926c4d0f8cff", "limitation": "Structure checked; source truth, product and deployment NOT tested.", "run_id": null, "scope": "environment-only", "source_count": 6, "sources_sha256": "143d19ff6c09afbbc00f713486e4cedefc4225f064be8416c0b4859a6e9184bc", "status": "passed"}
[sessions] passed (exit 0)
{
  "status": "not-executed",
  "reason": "no_active_sessions",
  "count": 0,
  "freshness": "not_checked",
  "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"
}
CLOUD_CHECK_RECEIPT=/workspace/scratch/fb980e912f69/agentflow-open/docs/workstreams/research/AF-RES-105/.cache/result-check-9290320/.workbench/cloud-check.json
CLOUD_CHECK_RESULT={"status": "passed", "exit_code": 0, "checked_out_sha": "9290320c1e9de33f30857af87640926c4d0f8cff", "require_clean": true, "source_start": {"commit": "9290320c1e9de33f30857af87640926c4d0f8cff", "dirty": false, "clean": true}, "source_end": {"commit": "9290320c1e9de33f30857af87640926c4d0f8cff", "dirty": false, "clean": true}, "session_validation": {"status": "not-executed", "reason": "no_active_sessions", "count": 0, "freshness": "not_checked", "contract_sha256": "19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc"}}
```

원장 재계산 stdout:

```json
{
  "status": "PASS",
  "errors": [],
  "cases": 12,
  "counted_primary": 32,
  "required_primary": 24,
  "counts": {
    "chronological": {
      "slots": 8,
      "unique_episodes": 8,
      "candidate_count": 8,
      "verified_distinct_owner_ids": 6,
      "owner_identity_unknown_slots": 1,
      "full_new_numerator": 0,
      "full_newness_decidable": 0,
      "full_newness_unknown": 8,
      "changed_capability_new": 0,
      "changed_capability_decidable": 0,
      "changed_capability_unknown": 8,
      "fixed_proposal_execution_decidable": 0,
      "fixed_proposal_execution_unknown": 8,
      "fixed_proposal_success_numerator": 0,
      "fixed_proposal_success_decidable": 0,
      "fixed_proposal_failure_reported": 0,
      "learn_then_execute_numerator": 0,
      "learn_then_execute_decidable": 0,
      "return_actions": {
        "기존 시도 표시와 링크": 3,
        "한 가지 확인 질문": 4,
        "유보": 1
      }
    },
    "explicit_statement_auxiliary": {
      "slots": 4,
      "unique_episodes": 4,
      "candidate_count": 4,
      "verified_distinct_owner_ids": 4,
      "owner_identity_unknown_slots": 0,
      "full_new_numerator": 0,
      "full_newness_decidable": 0,
      "full_newness_unknown": 4,
      "changed_capability_new": 2,
      "changed_capability_decidable": 2,
      "changed_capability_unknown": 2,
      "fixed_proposal_execution_decidable": 1,
      "fixed_proposal_execution_unknown": 3,
      "fixed_proposal_success_numerator": 0,
      "fixed_proposal_success_decidable": 1,
      "fixed_proposal_failure_reported": 1,
      "learn_then_execute_numerator": 0,
      "learn_then_execute_decidable": 0,
      "return_actions": {
        "같은 링크의 다른 절": 1,
        "유보": 1,
        "한 가지 확인 질문": 2
      }
    }
  }
}
```

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| 전체 조작의 새로움 판정 분모가 시간순0·보조0이며, 새 기능2건의 후속 실행은 미확인 | BL-N1의 [543409](https://blender.stackexchange.com/questions/313644#comment543409_313661), QG-N1의 [780200](https://gis.stackexchange.com/questions/477944#comment780200_477957) 뒤 같은 작성자가 연결한 실행 기록을 먼저 대조; 공개 기록이 더 없으면 다음 연구에서 사전 조작·직후 실행을 함께 수집 | 동일인·동일 입력·동일 변경 단계에 대해 제안 전 미인지와 제안 뒤 실행이 연결되면 해당 결합 판정에 산입 |
| 보조 모집은 닫힌 검색 가능 범위이며, ‘I tried that’은 제안 뒤 시험도 포함 | [26개 고정 질의](evidence/start/auxiliary-search-plan.json)와 [22건 원장](frame.csv)을 유지하고, 별도 사전등록한 2024 공개 댓글 모집을 새 층으로 수행 | 현재 슬롯보다 앞선 적격 진술이 새 범위에서 확인되면 범위 의존성을 인정; 기존 봉인 슬롯과 효과율은 소급 변경하지 않음 |
| 연결 파일·문서·원 사용자 판이 다르고 Blender GN 통합 fixture 두 개는403; 상류 시험은 판독만 함 | [Blender 재현](evidence/blender-official/reproduce.md)의 고정 blob/fixture 재조회와 [QGIS 재현](evidence/qgis-official/reproduce.md)의3.34 입력을 실행; BL-N1의 당시 파일·Compare 연산·각도부터 확인 | 당시 파일이 >90°/지정판과 맞거나 같은 입력의 실패가 확인되면 전체 예제 유보를 변경; 합성 현재판 성공만으로 원 사용자 채택을 인정하지 않음 |
