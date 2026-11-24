# AF-RES-109 최종 인계 — PARTIAL

## 1. 식별과 고정판

| 항목 | 값 |
| --- | --- |
| 작업 / 시도 | AF-RES-109 / 1 |
| 연구 수용 | **PARTIAL** — 최초판·엄격 비교·독립성 조건 결손. 양성 발견 수는 수용 조건이 아님 |
| 운영 상태 | 현재 제공된 공개자료·환경에서 가능한 조사·원장·검산을 마침. 엄격 비교를 재개하려면 아래 결손 입력이 필요함 |
| 배정 종류 / 실제 수행 | web-pro 배정. 실제 수행은 공유 Linux 작업공간의 root 및 별도 자동 모델 문맥, 공개 검색·GitHub connector·Python/Git. native web-pro 세션을 별도로 실행했다는 근거 없음 |
| 모델 | 부모 표시 GPT-6 Astra Pro 상속. immutable backend ID·seed 미확인 |
| 저장소 / 브랜치 | `laadkke-arch/agentflow-open` / `work/research-af-res-109` |
| 계획 기준 SHA | `c40ef7723d851b628233bfb60dff8dfd292385cf` |
| 실제 시작 SHA | `0bcaf7c90f3324447fd1b8bf12c514187ca4776b` — 기존 자기 브랜치가 없어 이 당시 통합판에서 생성 |
| **검사한 결과 SHA** | **`c212aab782008f263cbee14f6304c029dc82ce3a`** |
| 검사 영수증 SHA | `a45c76dd75f4e244c60ebc9fe5dcc0e550173075` — 결과 SHA 뒤의 별도 문서·로그 변경 |
| HANDOFF 작성 직전 원격 tip | `a45c76dd75f4e244c60ebc9fe5dcc0e550173075` |
| 마지막 실제 검사 종료 | 2026-11-24T03:17:55.275456+00:00, 같은 결과 SHA의 공통 검사 재실행 exit0 |
| PR / 통합 / 중앙 원장 | PR 생성·통합 없음. `dot-control.json` 수정 없음 |
| 공개 작업자 참조 | 이 작업의 `evidence/start`, `evidence/search`, `evidence/blind`, `evidence/audit`, `evidence/validation`에 역할·노출·UTC 기록. 인간 검토0 |

이 HANDOFF는 검사와 영수증 저장 뒤 **이 파일만 마지막 단독 커밋**하는 문서다. 자신을 포함할 커밋 SHA를 파일 안에 미리 적지 않는다. 최종 tip은 `git log -1 -- docs/workstreams/research/AF-RES-109/HANDOFF.md` 또는 원격 브랜치에서 확인한다. 마지막 HANDOFF 커밋과 영수증 커밋을 검사한 결과 SHA로 혼동하지 않는다.

## 2. 목표·읽은 계약·허용 경로

부분 설계 요청을 처음 받은 모델이 가까운 대안과 작동 원리를 어디서 발견하고, 링크가 구체적인 선택·실패 시험을 추가하는지 비교했다. 검색 전략, 실제 탐색기 제품 실행, 원 개발자의 인지·채택·시간 절감을 구분했다. 쓴 경로는 `docs/workstreams/research/AF-RES-109/`뿐이다.

시작 시 배정 통합판의 AGENTS.md, STATE.md, DOT_AUTOMATION, RESEARCH_WORKFLOW, RESEARCH_BRIEF와 중앙 원장의 자기 행을 읽었다. 계획판→실제 시작판 사이 관련 변경은 중앙 dot-control뿐이었다. 검사 때 통합판은 `4fbfd8eb52c606edb528b0e85b38b1b57f181799`로 이동했지만, 허용된 필수 문서 중 dot-control만 바뀌었고 자기 행과 계약 해시는 그대로였다. [시작 범위](SCOPE.md), [검사 때 변경 대사](evidence/validation/integration-drift.json).

운영 의존은 AF-RES-105 하나다. [지정 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/1a9d75dc7ae6a179522a5a56e99b002651a2f7bd/docs/workstreams/research/AF-RES-105/HANDOFF.md)와 [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/9290320c1e9de33f30857af87640926c4d0f8cff/docs/workstreams/research/AF-RES-105/RESULT.md), 같은 결과판의 followup.csv·returns.csv를 읽었다. 105의 좁은 기능 최초인지2건과 동일 제안 학습→실행 판정분모0을 구분했다. 105의 사례·26질의·기능 두 개,018의 과거50문제·미인계 산출물, 다른 PLAN#27 자료를 재조사하거나 다른 PLAN#27 작업자에 의존하지 않았다. 이 작업 안의 검색·판독·검산 하위 문맥만 사용했다.

새 유료 API·계정 변경·외부 연락은 하지 않았다. 기존 검색 도구의 실제 금액·토큰 비용은 관측되지 않았으므로0이라고 쓰지 않았다. 단독 작업자가 같은 입력 봉인→새 문맥 검색→봉인→새 판독 문맥을 순차 수행하는 방법은 [reproduce.md](reproduce.md)에 있다.

## 3. 무엇을 저장했나

| 파일·묶음 | 내용과 확인 |
| --- | --- |
| [RESULT.md 고정 결과판](https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/RESULT.md) | 필수 표1·2·3이 먼저 나오며6/36/6행. 이어 Q1–Q7·반례·사후 외부 분야, 마지막 정확히3행 약점표 |
| SCOPE.md·frame.csv·requests.jsonl·baseline.csv | 접근 가능한2024 issue각첫80=160행, 원순위첫3씩6자리, 기지 안과원문위치·인자·hash, Studio0·최초판결손 |
| search.jsonl·evidence/search/* |12arm의원순서·상위5위·추가노출·개봉실패·시간·비용. 원48파일은검색봉인SHA와byte일치 |
| candidates.csv·choices.csv·costs.csv |36예정자리/33반환/3공석, 계보·조건·반박, 바뀐단위/순서/책임/실패처리, 최소입력·예상출력, 전체/공통소비량 |
| sources.jsonl·source-accounting·계보감사 | 결과판198개독해/실패/재열람행. 원자료재고33으로보수적산입;52검색취득행의37자체true를17계보로정리 |
| counterchecks.csv·external-transfer.csv | 다른계보반례6개와사후외부원전4개, 전이실패전제. 발견실적에추가하지않음 |
| aftermath.csv·evidence/aftermath |6요청의공개주체·시각·PR·릴리스·복구진술·실패후속. 같은사건URL을중복산입하지않음 |
| SELF_CHECK.md·acceptance-evidence.json |Q별답/반례/분모/결손/다음관측, 판독자의정보·시각, 뒤집힌행, 파일·판·주체·미달 |
| recalculate.py·result-analysis.md |원장에서세표와수치를재계산하는코드와서술원본. `--check`는원장일치검사이며제품성공검사가아님 |
| evidence/validation |고정원격15파일재독·blob대사,대표원전7개추가읽기/실패(산입0), 실제명령·종료값·실패·환경수정·재실행로그 |
| EXECUTION_PLAN.md |미실행27개시험입력을꺼내는명령, 요청별원구성·최소입력·실패대조·필요로그, 없는harness를실행했다고하지않는재개경계 |

원문 전체의 재게시 대신 공개 URL·절·원 API hash·실제 LF 정규화 hash를 보존했다. 비커밋 캐시는 인계 증거로 사용하지 않는다. 나중의 원문 hash가 달라지면 현재 웹 본문을 원 실험 입력으로 간주하지 말고 별도 판으로 취급한다.

## 4. 핵심 결과와 수용 한계

### 모집·실행·원자료

자연 공개 현재 opening post6건은 Node-RED4505/4507/4508, xyflow3757/3758/3759다. 조건이 약한 R2와 그림 topology가 불명확한 R5를 더 좋은 뒤 사례로 교체하지 않았다. 선별 전 탈락0, 뒤154행은 미선별이다. 최초 본문판 확인은0/6이며 Studio 실제 요청은0건이다. R5 제목은 생성26초 뒤 편집된 사건을 사후 확인했다.

12개 검색 문맥은 실제 분리했고 요청쌍 순서를 교대했다. 질의30회·명시개봉52회·최종링크33개·공석3개이며 각 arm3/6/3상한을 지켰다. A는15질의/23개봉/16반환, B는15질의/29개봉/17반환이다. 경과시간 합은 A1,934.069433초, B2,234.938809초지만 병렬 작업·모델 판단·대기 시간을 포함하여 절약시간으로 해석하지 않는다.

| 배당 | 목표 | 직접 독해 후 보수적 산입 | 결손 |
| --- | ---: | ---: | --- |
| 모집 원 요청 |6 |현재판6 |최초판자격0/6 |
| 검색 반환 원 설계·구현 |8 |17원저작·기능계보 |독립구현17·먼분야17·2024가용17이라는뜻아님 |
| 다른계보 반례 |6 |6 |규격·원전대조, 실제제품시험0 |
| 사후 외부 분야 |4 |4 |OCFL/PREMIS와NIST/MIL, 발견실적0 |
| 합계 |24 |33 |수량충족만으로핵심비교조건충족아님 |

### 새 선택·시험과 잘못된 채택 방지

중복을 합친 조건부 선택안12개, 제안된 판별시험27개다. R1–R5만9/22, R6은잠정3/5다. 이 수에는 유익한 근접 오답의 대조도 포함하며 완전한 해결책 수가 아니다. R1의 Edit·번역, R6의zoomOnPinch=true는 원문 기지 안이므로 새 구현으로 세지 않았다. 검색에서 발견한 먼 분야 원리의 적격 후보는0이다.

R3은 비밀값 존재와 편집 의도, 생략과 명시교체, 기존값 없는 유지표식을 구별하게 했다. 그러나 Kubernetes의 소유권별 생략 삭제는 “partial update이면 항상 보존”이라는 일반화를 반박한다. R4의 CSS hit 영역 제외는 자식 handle·bubbling·selection·delete까지 저절로 보존하지 않는다. R5의 yFiles 두 안은 같은 끝점 pair에서만 조건부이며 원 그림의 fan-out 여부가 미확인이다. R6의 합성 wheel과실제 touchpad를 분리했다. [선택 원장](choices.csv), [반례 원장](counterchecks.csv).

전체 방법별 조건부 목록은 A8선택/16시험, B8/16이다. 공통 소비량 안에서 원전 취득이 확정된 키는 A5/11, B2/7이며 R3-B의순위1/3은사건 index/UTC순서불일치로미확정이다. 이는 줄인 예산으로 제안까지 재실행한 성과가 아니다. 정확한 모델·자동 노출을 맞출 수 없고 후속 노출도 있어 엄격한 A만/B만/양쪽/무성공 판정은 하지 않으며 **6건 모두 비교불가, 분모0/6**이다.

### 실제 후속과 인과효과

공개 댓글24개·timeline76개를 읽었다. 성공 응답42개에는 빈 collection9개가 포함되고 접근실패4개를 기록했다. 패치+릴리스로 연결된 요청은 R1/R3/R6의3/6, 원 요청자의 명시 복구 진술은 R2의1/6이다. R2는 본인도 원인을 의심했다. R6은 이후 느린 zoom·초기 긍정 진술 철회가 있어 닫힘을 완전 성공으로 보지 않는다. 나머지5요청의 수정 뒤 원 요청자 재시험은 미확인이다.

이번 추천은2026년에 생성되었고 공개 후속은2024년 행동이다. **이번 추천을 배워 같은 제안을 실행한 사건의 판정분모0**, 시간 절감 미확인이다. 후보 적용·27개 제품 시험·실제 Windows touchpad·자동 탐색기 제품 실행도0이다. 저장소의 discovery fixture 통과를 자동 탐색기 제품의 실측으로 바꾸지 않았다.

### 실제 독립성과 교정

두 별도 자동 판독 문맥에 방법·순위를 가린28묶음33변형을 전달했다. 그러나 root는 R4 댓글 일부를 검색 전에 보았고, R2-A와 R6-B 검색에 같은 요청 후속이 요약으로 노출됐다. R6 판독자도02:29:49 UTC에 후속요약을 보았고02:39:39에 최종 판정하여 R6을 잠정치로 분리했다. 독립 인간 검토는 없었다.

줄바꿈 지문 차이를 원 hash 유지+실험 hash 추가로 교정했고12arm 입력 일치를 확인했다. Function comparator는독립본문검증실패로보류했다. 계보 감사에서metadata행의산입을실제본문행으로이동하고중복을합쳤다. 최종 감사는 두 인용 주소·baseline exact_location·Chromium 원검색날짜와후속재조회실패의 혼동을 지적하여수정했다. 원 raw검색과 blind판정은 바꾸지 않았다. 세부 이력은 SELF_CHECK와 evidence/adjudication-changes에 있다.

## 5. 묶음별 원격 커밋

| 묶음 | 원격 SHA | 고정한 내용 |
| --- | --- | --- |
| 모집·기지 안·계약 | `62997151eed37758c5634bcd72f8342710a127a8` | manifest start실행, 모집160/선택6·가림·예산·baseline |
| 검색 중간1 | `5f80b7b2886ba76e6d41d3f7e7c708fbf272e365` | 완료5arm봉인 |
| 검색 중간2 | `d9441e42f3da2698cfebc4df76e9511dd2fcbfd5` | 완료8arm·입력newline대사 |
| 두 검색 전체 | `628e33709b0be7a19486f1bfeaef93f42e129394` |12arm·36자리. 이뒤에판독·사후원전개봉 |
| 판독·사후 결정 | `ada47907ac8ee68b5e12e02e246d37cdab0930fd` |별도판독·계보·6반례·4외부·공개후속·원장 |
| **검사 대상 결과** | **`c212aab782008f263cbee14f6304c029dc82ce3a`** |필수표·Q1–Q7·SELF_CHECK·검산코드·미실행계획 |
| 검사 영수증 | `a45c76dd75f4e244c60ebc9fe5dcc0e550173075` |원격재독·명령/종료값·첫실패·환경수정재실행·최종수용근거 |

각 묶음은 expected-parent를 확인한 원격 ref 갱신 뒤 fetch/ls-remote 또는 고정 ref 읽기로 확인했다. 중간 tree연결의422오류도 기록 후 실제로 존재하는 committed tree에 합쳐 재시도했으며 브랜치를 잘못 갱신하지 않았다. 원격 확인 상세는 [commits.jsonl](evidence/seals/commits.jsonl)과 마지막 영수증/이표를 함께 따른다. 이 HANDOFF를 추가하는 마지막 커밋의 변경 파일은 하나여야 한다.

## 6. 실제 검사와 실패 보존

검사는 결과 SHA의 깨끗한 별도 checkout에서 실행했다. 실제 환경은 Linux/Python3.12.14이며 `codex-cloud`는 호출 라벨이다. [명령·입력·출력 hash](evidence/validation/commands.json), [설명 영수증](evidence/validation/README.md).

| 명령 | 실제 종료값 | 의미 |
| --- | ---: | --- |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-109/manifest.json --fetch` |0 |명시manifest1개,remote_checked,허용경로·고정의존·계약일치 |
| `python -B docs/workstreams/research/AF-RES-109/recalculate.py --check` |0 |raw48파일·원baseline/요청필드·표6/36/6·33원자료·12/27대사;연구PARTIAL유지 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` 첫시도 |1 |기존unittest의180초timeout;TMPDIR이소스docs아래라임시복사재귀발생 |
| 같은 공통 명령 재실행 |0 |TMPDIR만검사checkout밖·허용경로안으로이동;같은SHA·검사코드·시간제한 |

첫 실패에서 임시 workspace가자기docs안으로중첩되는실제경로를확인했다. 실패로그를보존하고이번실행이만든임시트리만제거했다. 소스·검사기·timeout을약화하지않았다. 재실행에서workbench55개,repo-intake7개,reference-audit9개테스트와export·Git bundle복원·환경smoke·고정discovery fixture가통과했다. 이71개테스트는원프로젝트27개제안시험이아니다.

공통 자동 세션발견은 `count:0`, `no_active_sessions`, `status:not-executed`, `freshness:not_checked`다. 명시manifest1개통과와합치지않는다. 진행조회용보조스크립트의KeyError·exit1도별도기록했으며gate결과가아니다. 첫실패·재실행·비gate조회오류를모두영수증에서확인할수있다.

결과판을고친재검사가아니므로검사SHA는계속c212aab이다. 이후붙인acceptance갱신·로그·이HANDOFF는이전검사에포함되지않는다. 원장·RESULT·검산코드의결과판내용은영수증작성뒤에도byte동일함을확인했다.

## 7. 막힌 이유와 다음 첫 행동

**다음 첫 행동은 여섯 공개 issue의 생성시점 본문판을 복구할 수 있는지 확인하는 것**이다. [R1](https://github.com/node-red/node-red/issues/4505), [R2](https://github.com/node-red/node-red/issues/4507), [R3](https://github.com/node-red/node-red/issues/4508), [R4](https://github.com/xyflow/xyflow/issues/3757), [R5](https://github.com/xyflow/xyflow/issues/3758), [R6](https://github.com/xyflow/xyflow/issues/3759)의 공개 edit history/당시 archive를 열고 현재판hash·원문위치와대조한다. 특히R5는 [event11365940209](https://api.github.com/repos/xyflow/xyflow/issues/events/11365940209)와원첨부의topology를확인한다. REST updated_at이나현재bodyVersion으로최초판을대신하지않는다. 복구하지못하면기존6자리의결손을유지한다.

그다음 동일immutable모델ID·엔진자동노출·단조시각을관측할수있는환경이있을때만동일입력으로새봉인·새문맥실행을한다. 제공환경에서그값이없었고일부후속노출도발생하여기존엄격분모0은소급복구할수없다. 실패사례를지우거나유리한표본을추가해서A/B비교를완성하지않는다.

### 실행할 명령과 필요한 입력

재개자는먼저원격tip과검사SHA를구분한다. 아래명령은고정결과·재현절차·미실행제품계획·시험입력원장을직접읽는다.

```sh
git fetch origin work/research-af-res-109
git show c212aab782008f263cbee14f6304c029dc82ce3a:docs/workstreams/research/AF-RES-109/RESULT.md
git show c212aab782008f263cbee14f6304c029dc82ce3a:docs/workstreams/research/AF-RES-109/EXECUTION_PLAN.md
git show c212aab782008f263cbee14f6304c029dc82ce3a:docs/workstreams/research/AF-RES-109/choices.csv
```

EXECUTION_PLAN §2의완전한Python명령은choices에서고유시험27개의minimum_input·expected_output·반례를꺼낸다. 이는시험큐추출이며제품실행명령이아니다. 제품harness가없어존재하지않는실행명령을제시하지않았다. 원프로젝트고정SHA의package scripts·기존시험을읽고해당최소입력을구현하는것이실제제품실행의다음행동이다.

필요입력은R1 Node-RED3.1.0·locale, R2문자열3.13의실제판과Node버전, R3 Node-RED3.1.3/Node16.20.2/npm8.19.4/Docker/Firefox121·synthetic비밀값, R4당시React Flow판과겹침/handle영역, R5원이미지·edge topology, R6실제Windows11 touchpad/driver/Chrome120·Edge/원예제와event trace다. 실제비밀·실사용flow를시험값으로요구하지않는다. R2/R4/R5미확인판을현행으로대체하면사후합성층으로만기록한다. 이Linux환경으로실제Windows touchpad를관측하지못했다.

공통검사를다시해야할구체적변경이생기면위§6명령을새고정결과SHA의clean checkout에서수행한다. TMPDIR은검사대상docs밖에둔다. 그대로재현하는정확한worktree/임시경로명령은 [검증 README](evidence/validation/README.md)에있다. 이번결과는충분히검사했으므로내용변경없이전체검사를반복할필요는없다.

원개발자의채택·시간절감은기존공개자료에추천노출→동일주체의선택→같은제안실행→결과/시간이연결될때만다시판정한다. 사후유사patch나연구자의새시험으로인과효과를채점하지않는다. 다른PLAN#27결과·새유료API·계정변경·외부연락·중앙원장수정은재개의전제가아니다.

| 불일치·약점 | 다음 조사·직접 열 자료 | 어느 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 최초 본문판0/6, R2 약한 조건쌍, R5 제목 편집·그림 topology 미확인으로 역사적 입력이 고정되지 않음 | 여섯 issue의 공개 최초 편집판과 R5 event11365940209·원 첨부를 직접 대조하고 baseline을 새 봉인 | 생성시점 원문에서 두 조건·기지 안이 확인되고 특히 R5가 같은 끝점 평행 edge인지 판명되면 해당 요청의 입력·적합 자격을 재판정 |
| immutable 모델·자동 개봉 미관측, R2/R6 후속 노출, R3-B prefix 순서 불일치로 엄격 비교분모0 | 동일 모델 ID·완전 노출 영수증을 제공하는 환경에서 동일6문장과 교대순서를 새 문맥으로 재실행하고 사건 순서를 원 로그로 확인 | 실제 모델·노출·순서가 검증되고 후속 가림이 유지된 쌍만 엄격분모에 포함; 원전 취득 prefix를 성공으로 소급하지 않음 |
| 선택12·시험27은 조건부·미실행이고 R6은 잠정; 당시판·원 요청자 실행·추천 인과효과가 미확인 | EXECUTION_PLAN의 원 버전·최소 입력으로 UI/credential/edge 시험과 실제 Windows touchpad 기록을 수행하고 고정 릴리스·CI·기존 당사자 진술을 직접 읽기 | 두 필수조건을 같은 실행에서 보존한 결과와 실패 대조가 나오면 기술 적합성을 갱신; 추천 노출 뒤 동일 주체 실행·시간 자료가 있어야 채택·절감 판단을 갱신 |
