# AF-RES-102 HANDOFF

- 상태: **COMPLETE_WITH_LIMITATIONS — 지정 모집틀·허용 결원·미확인 규칙 아래 조사·판독·별도 AI 검토·저장소 검사·고정 GitHub 재열람 완료.**
- 작성 UTC: 2026-11-23T22:49:53.327832+00:00
- 저장소/브랜치: laadkke-arch/agentflow-open · work/research-af-res-102.
- 쓰기 경로: docs/workstreams/research/AF-RES-102/만. 중앙 dot-control.json과 선행 작업은 수정하지 않았다.
- 실제 검사한 **연구 결과 SHA: 092f4c5c56451bceb53e632f4bddf33db6cda168**.
- 실행·원격 재열람 영수증 커밋/이 인계의 부모: **8552d736cb8fb1d1ca7a5de9206a0165dac20602**.
- 이 파일은 검사·재열람이 끝난 뒤 마지막 단독 커밋으로 작성한다. 이 인계와 뒤의 영수증 커밋을 결과 SHA 검사에 포함됐다고 말하지 않는다.
- 사람 검토는 없다. 주 사례와 Q7은 작성자와 다른 AI 검토자가 각각 검토했으며 독립성의 범위는 아래에 구분했다.

## 인수할 결과와 핵심 수치

[RESULT.md](RESULT.md) 첫 세 표는 **12쌍 자리 / 24판 자리 / 12쌍 반환**이다. 실제 적격 표본8쌍과 사전 규칙이 허용한 결원4쌍을 구분한다. 실제16판 자리 모두 P=YES/U=YES, G=미확인이다. 실제 새판 U 예측8개는 모두YES였고8개 모두 관측YES다. 결원4개를 NO 또는 실제 유보 예측에 넣지 않았다.

각 프로젝트의 일반층과 소스 변경층, 총4그룹은 각각 TP2/FP0/FN0/TN0·유보0·결원0·실제 양성2/음성0이다. 두 부재층은 결원2씩, 양성·음성 분모0이다. 채워진 각 층의 FNR=0/2는 계산할 수 있지만 FPR·특이도는 음성 분모0으로 산출 불가다. 세 층의 비율을 합산하지 않았다. [counts.json](counts.json), [predictions.csv](predictions.csv), [lineage.csv](lineage.csv).

보조 탐색은 각 첫40 모집틀의 남은 후보 중 고정 hash순20개씩이며 주 표본과 분리했다. 전체 사이트를 조사했다는 주장은 하지 않는다. 유형① 경로잔류/절미사용, ② 옛경로부재/후계사용, ③ 동일이름·해시/목적변경은 지정 두 판의 이 범위에서 실제 적중을 얻지 못했다. 유형④ 다른바이트/같은목적은 주8/8, GG보조19/20, MP보조20/20이다. 보조 음성이나 새 사례를 주 공석에 넣지 않았다.

MP-C1의 원 HBox 같은높이 목적은 이어지지만 제목 fragment는 hboxdivider-demo에서 hboxdivider-and-vboxdivider-demo로 바뀐다. 새 첫 HBox 그림을 가리켜야 한다. 보조 GG coord_flip는 시각적 수평boxplot 목적은 유지하면서 새 첫 코드가 다른 방법을 쓰므로, 구체적 coord_flip 방법을 찾는 독자는 새 두 번째 블록으로 보낸다. 새1·2PNG는 같은 바이트여도 코드 방법이 다르다.

현재 Matplotlib3.7.0의4개 완전 HTML은 고정 최초 발행본과 바이트가 달랐다. 실패를 보존한 뒤 exact section 텍스트·img 속성4/4, 실제1x/2xPNG8/8일치를 따로 확인했다. 따라서 과거 인용은 고정 발행 SHA, 조사한 다음 판 이용은 확인한 현재 절 링크를 쓴다. 2026년 최신 API나 미래 링크 가용성을 보장하지 않는다. [반환 결정](evidence/returns.json).

## 자료와 검토

최종 [sources.jsonl](sources.jsonl)은477행, 신규 고유 1차 자료 **111개**다. 본문46·payload45·발행/변경/규칙15·EPUB2·wheel3으로 요구8/8/8/2/2를 모두 충족한다. 같은 저작의 두 판·같은 바이트·미러·패키지 멤버·미열람 스캔·빈job조회·실패·098 계승 자료를 중복 산입하지 않았다.

단계3 작성자 집계116에서 별도 검토가 GG 계승 빌드규칙5개(동일 SHA2개 포함)를 찾아111로 정정했다. 원천 GG ledger57은 당시 기록으로 보존하고 최종 root에서는52로 계산했다. MP54와 Q7 5를 더한 수다. [정확한 제외 대응](evidence/source-reconciliation.json), [해결 기록](evidence/review-resolutions.json).

- 주 연구의 모집·봉인·사후 판독·최종 표/집계: [stage1](evidence/cross-domain/review-stage1.md), [stage2](evidence/cross-domain/review-stage2.md), [stage3](evidence/cross-domain/review-stage3.md), [final](evidence/cross-domain/review-final.md)의 별도 AI 검토.
- Q7은 cross-domain 작성자의 자기 검토를 독립 검토로 부르지 않는다. 다른 GG 작성자의 [교차 분야 검토](evidence/ggplot2/review-cross-domain.md)가 Trees 멤버와 wheel RECORD를 독립 재검산했다.
- 최종 독립 검토 판정은 PASS_WITH_MINOR_DOCUMENTATION_ISSUE_RESOLVED, 중단할 결함0이다. 재현 스크립트의 실제 쓰기 동작과 공식 발행 목록/자동 스캔의 구별 문구를 고쳤다.
- 자체 검토는 [SELF_CHECK.md](SELF_CHECK.md)의 Q1~Q7 일곱 행이다. 해석과 반대 근거·미확인·판단을 바꿀 최소 확인을 함께 남겼다.

새 교차 분야 사례는 IDPF Trees EPUB20230704와 build1.2.2.post1 wheel이다. Trees cover.jpg는 수록돼도 선택 titlepage의 정적 본문 참조가 아니며, reader 책장 표지의 별도 표시 여부는 미확인이다. wheel의19RECORD행/18해시가 맞아도 entrypoint 선언은 설치·호출 증거가 아니다. [실물 감사](evidence/cross-domain/audit.json).

## 계약·원격 커밋

시작 최신 통합판은 ac7abc85e12b3a5b5f87b694d00e9511332fe272다. 계획 ace1a06a13ea435f5cb6a3e340ad24f03f68ecae와의 차이는 중앙 진행표뿐이고 기준 브리프·연구 규칙은 같은 blob이었다. 운영 의존 끝5022d581d8d7a4a359250797d55c79f6b67d219c과 연구 입력846aa7b644bda67ef2551c3f4fb1ec6f5de9484d를 구별했다. 실제 인수한 예측·lineage·counts·RESULT 네 blob은 두 선행 끝에서 같았다. [시작 대조](evidence/input-contract.json), [session start](evidence/session-start.json).

검사 시 통합 끝은7440dfcc7c7a6c6772b437877c422e70b9aab9f1로 이동했으나 바뀐 파일은 dot-control.json 하나이고 AF-RES-102 항목도 그대로였다. AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·RESEARCH_BRIEF와 운영 의존 끝은 변하지 않았다. [종료 시 대조](evidence/validation/end-contract.json). 시작 계약과 고정 연구 범위를 유지했다.

| 묶음 | 원격 commit | 변경 파일 수 | 원격 확인 UTC |
|---|---|---|---|
| 1 | [5f664a87df16f453151ec985e9ad37913e3bda90](https://github.com/laadkke-arch/agentflow-open/commit/5f664a87df16f453151ec985e9ad37913e3bda90) | 189 | 2026-11-23T22:03:18.088Z |
| 2 | [f1c5d6ff927fd5fbe108565598810ca7e94c5753](https://github.com/laadkke-arch/agentflow-open/commit/f1c5d6ff927fd5fbe108565598810ca7e94c5753) | 33 | 2026-11-23T22:07:47.803Z |
| 3 | [be9c4cfa09a59da937d40f71cdf7c675fb42c0fa](https://github.com/laadkke-arch/agentflow-open/commit/be9c4cfa09a59da937d40f71cdf7c675fb42c0fa) | 403 | 2026-11-23T22:24:55.653Z |
| 4 | [092f4c5c56451bceb53e632f4bddf33db6cda168](https://github.com/laadkke-arch/agentflow-open/commit/092f4c5c56451bceb53e632f4bddf33db6cda168) | 32 | 2026-11-23T22:42:10.833Z |
| 검증 영수증 | [8552d736cb8fb1d1ca7a5de9206a0165dac20602](https://github.com/laadkke-arch/agentflow-open/commit/8552d736cb8fb1d1ca7a5de9206a0165dac20602) | 22 | 아래 고정 GitHub3파일 재열람 완료 2026-11-23T22:47:38.279736+00:00 |

① 판·이전 예제·일반층, ② 새 경로·층·예측 봉인, ③ 사후 본문/파일/발행/반례, ④ 층별 집계/반환/자가검산 순서다. 원격 예측 봉인은2026-11-23T22:07:47.803Z이며 첫 새 GG본문 요청22:08:32.363481Z, MP본문 요청22:08:40.563576Z보다 앞선다.

단계별 전체 변경 파일·Git blob·SHA-256·원격 tree는 [checkpoints.json](evidence/checkpoints.json)에 있다. 터미널 git push 인증 실패 뒤 인증된 GitHub Git-data API를 사용했고, staged index tree와 만든 remote tree가 정확히 같은지 확인한 후 expected-SHA ref를 갱신했다. 원격 commit을 다시 fetch해 확인했다. [발행 경로 기록](evidence/publish-path.json). 통합/main 병합이나 중앙 색인 변경은 하지 않았다.

## 실제 검사 결과와 범위

| 검사 | 정확 명령 | UTC 시작 → 종료 | 종료값 |
|---|---|---|---|
| research_structure | python -B docs/workstreams/research/AF-RES-102/tools/verify.py | 2026-11-23T22:42:13.668617+00:00 → 2026-11-23T22:42:13.839968+00:00 | 0 |
| session_check | python -B -m workbench.session check docs/workstreams/research/AF-RES-102/manifest.json --fetch | 2026-11-23T22:42:13.840031+00:00 → 2026-11-23T22:42:24.665596+00:00 | 0 |
| cloud_check | python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean | 2026-11-23T22:42:24.665665+00:00 → 2026-11-23T22:42:37.173435+00:00 | 0 |

연구 구조 검사45개가 통과했다. 명시적 session check는 outside_paths=[], unmerged_paths=[], errors=[]였다. cloud_check의5명령은 모두 종료0이지만, 자동 세션 발견 결과는 **not-executed / no_active_sessions / count=0**이다. 명시적 작업별 check가 이 manifest를 따로 검사했다. 공통 세션 탐색의 종료0을 이 작업의 자동 검증으로 바꾸어 보고하지 않는다.

검사는 시작·종료 모두 결과 SHA 092f4c5c56451bceb53e632f4bddf33db6cda168, clean=true에서 수행했다. 검사 후에 영수증 파일을 저장했다. [실행 run.json](evidence/validation/run.json), [공통 원 영수증](evidence/validation/cloud-check.receipt.json), [검증 설명](VALIDATION.md)에 명령·입력/출력 지문·stdout/stderr·범위가 있다. 공통 검사의 실제 acceptance에는 scripts/check.py --require-git가 포함된다. 이 검사는 저장소/workbench 범위이며 제품·브라우저·역사적 생성의 검증은 아니다.

결과 SHA의 GitHub 재열람은 2026-11-23T22:42:53.274697+00:00부터 2026-11-23T22:43:39.232389+00:00까지 실행했고, **22/22 HTTP200·커밋 바이트 일치, 종료0**이다. RESULT의 필수3표, 대표 audit와 원PNG4개, 재현 절차를 포함한다. [원 영수증](evidence/validation/readback.json).

영수증 커밋 8552d736cb8fb1d1ca7a5de9206a0165dac20602에서도 다음3파일을 직접 열어 같은 Git blob 바이트인지 확인했다. 실행 UTC는 2026-11-23T22:47:30.573799+00:00 → 2026-11-23T22:47:38.279736+00:00, 종료0이다. 아래는 마지막 인계에 함께 남기는 해당 추가 수신 영수증이다.

| 고정 URL | HTTP | bytes | SHA-256 |
|---|---|---|---|
| [VALIDATION.md](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/8552d736cb8fb1d1ca7a5de9206a0165dac20602/docs/workstreams/research/AF-RES-102/VALIDATION.md) | 200 | 5665 | d5d61bd236cbd84d5f221389a16c816016de147dda2478c88bd73a36b36ab5a4 |
| [evidence/validation/run.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/8552d736cb8fb1d1ca7a5de9206a0165dac20602/docs/workstreams/research/AF-RES-102/evidence/validation/run.json) | 200 | 6484 | 5a93e141425b082ba189fa00f481cd79aa13b087e4848eb17201a50082eba2e6 |
| [evidence/validation/readback.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/8552d736cb8fb1d1ca7a5de9206a0165dac20602/docs/workstreams/research/AF-RES-102/evidence/validation/readback.json) | 200 | 19950 | f1e064f1c0745baa1b424992bbccc6ca90733842ef3d1dd3c453d86250616665 |

검증 영수증 커밋의 변경22개는 VALIDATION.md, checkpoints.json, evidence/validation/ 아래 기록뿐이다. RESULT·SELF_CHECK·CSV·집계·재현 코드와 대표payload는 검사한 결과 SHA에서 바뀌지 않았다. 이 HANDOFF가 추가된 뒤 공통 검사를 다시 수행했다고 주장하지 않는다.

## 실패·미실시·결손

최종 결과 SHA의 필수 계약/공통 검사와 원격 재열람에서 실패한 항목은 없다. 연구 필수 자료 범주는 모두 확보했고 허용 결원4쌍의 이유·재개 입력을 남겼으므로, 자료 접근 때문에 핵심 비교를 중도 포기한 PARTIAL 상태는 아니다. 아래 미확인은 결과의 실제 한계다.

- 실제16판 자리 G는 미확인이다. GG14·MP22개 정확 SHA/날짜 창 조회는 HTTP200·보이는 실행0이었다. 보존 job·입력 환경·단계별 output manifest/digest·발행 copy 연결이 없으며, 과거 생성이 없었다는 NO도 아니다.
- 네 부재층 자리는 후보0에 따른 결원이다. 이 범위의 실제 음성0을 일반 링크 오류율0이나 이름 변경 탐지 성공으로 해석할 수 없다.
- R/Python 예제 실행, 브라우저/EPUB reader/JS 실행, wheel 설치·entrypoint 호출, 역사적 생성job 재현, 사람 검토는 미실시다. 정적 참조 확인과 실행 관측을 구분한다.
- 앞선 구조 검사기2회 실패·CSV 줄끝 교정·최초 push 인증 실패·live HTML4개 불일치·실패 HTTP는 해당 영수증에 보존했다. 최종 검사 성공이 이 실패 관측을 지우지 않는다.

G에 필요한 재개 입력은 [GG build-search.json](evidence/ggplot2/build-search.json)과 [MP generation-search.json](evidence/matplotlib/generation-search.json)의 정확 source/docs/pub SHA·날짜 창에 연결되는 **보존된 실제 run ID, environment lock, output manifest/digest**다. 해당 입력이 없어서 역사적 생성 실행 명령을 확정할 수 없다. 현재 재빌드 명령을 그 대신 적지 않았다. 실제 누락 job을 다시 찾을 때 사용할 읽기 명령의 예시는 다음과 같다.

~~~sh
gh api 'repos/tidyverse/ggplot2/actions/runs?head_sha=a6f1a7c845bfe056ef952b839d2fd65b888ab5cd&per_page=100'
gh api 'repos/matplotlib/matplotlib/actions/runs?head_sha=235131a6bc2527aee7eea370fd5f94564a48c20d&per_page=100'
~~~

이 두 endpoint의 HTTP 원조회는 이미 수행했고0항목이었다. 위 CLI를 다시 실행하는 것 자체가 결손 해결이나 G의 증거는 아니다. 새로 발견한 보존 실행·출력 연결을 검사해야 한다.

## 색인 제안과 다음 첫 행동

색인에 넣을 한 줄: **AF-RES-102 — 두 판의 경로 생존과 실제 절 사용·생성 귀속: 주8실측쌍/4결원, 음성0·G16미확인, 고유111자료, 목적별 두 판/절 반환과 앵커·동일바이트 다른방법 반례; RESULT 092f4c5c56451bceb53e632f4bddf33db6cda168; 완료·한계 보존.**

다음 작업자의 첫 행동은 다음 고정 결과를 읽어 세 번째 반환 표와 Q6의 분모를 확인하는 것이다.

~~~sh
git show 092f4c5c56451bceb53e632f4bddf33db6cda168:docs/workstreams/research/AF-RES-102/RESULT.md
git show 092f4c5c56451bceb53e632f4bddf33db6cda168:docs/workstreams/research/AF-RES-102/evidence/returns.json
~~~

음성·새이름 후계의 근거가 필요하면 기존 공석을 채우지 말고, 같은 고정 두 발행판에서 첫40 밖의 후보를 새 범위로 사전 등록한다. 일반 이용에는 이미 확인한 정확 절과 실제 payload를 쓸 수 있으며, G를 주장하거나 2026최신판으로 확대하려면 별도 확인이 필요하다. [reproduce.md](reproduce.md)에 사전예측부터 사후자료까지의 분리 절차와 실제 명령이 있다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 주8쌍이 모두 양성이고 부재층4쌍은 결원이다. 보조 탐색도 첫40 내부의 남은20개씩으로 한정된다. | 같은 고정 두 판의 첫40 밖 목록에서 부재·잔류 후보를 새로 사전 등록하고, exact section과 모든 대체 참조를 연다. | 옛 경로가 남지만 U=NO인 FP, 또는 옛 경로가 없는데 후계 표현 U=YES인 FN을 직접 확인하면 조건별 판단을 수정한다. |
| 실제16판 자리의 G는 모두 미확인이다. 빈 Actions/check/status 조회는 과거 생성 부재를 입증하지 않는다. | 14개 GG·22개 MP 조회의 정확 SHA/날짜 창에 해당하는 보존 job, 입력·환경 lock, 단계별 출력 manifest/digest와 복사 기록을 확보한다. | 실제 실행이 선택 PNG를 새로 만들었다는 입력→실행→출력 digest→발행 연결이 생기면 G=YES; 복사만 했음이 입증되면 해당 실행의 G=NO로 바꾼다. |
| 같은 설명 목적과 같은 방법·주소는 다르다. HBox fragment 변경, coord_flip의 동일 새 PNG 두 방법, 가변 live HTML이 확인됐다. | 독자가 시각적 목적과 구체적 API 방법 중 무엇을 보존하려는지 명시하고, MP C1 실제 fragment와 GG coord_flip 두 코드 블록을 다시 대조한다. | 고정한 구체적 방법의 후계가 없거나 반환 절·참조 PNG가 바뀐다는 관측이면 U의 목적 단위와 현재 링크 결정을 재검토한다. |
