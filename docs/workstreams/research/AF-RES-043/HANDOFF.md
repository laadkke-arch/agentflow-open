# AF-RES-043#1 · 판 주소와 과거 인용의 개별 기여 — 최종 인계

## 1. 식별과 고정 결과

**상태: BLOCKED — 관측·보고·검산·원격 저장 절차는 완료했으나, 완전 연구 수용은 미충족이다.** `BLOCKED`는 아래의 자료·방법 조건을 뜻하며 Git 저장이나 세션 계약 검사의 실패를 뜻하지 않는다. 미달 사례를 다른 사례로 교체하거나 기준이 없는 값을 성공/오답 0으로 계산하지 않았다.

- 작업/시도: `AF-RES-043#1`. 배정 종류: `web-pro`.
- 실제 확인한 실행 표시: 시스템 모델명 `GPT-6 Astra Pro`, ChatGPT의 관리형 Linux 셸·공개 웹·GitHub 연결. 계정 화면의 모델/추론 설정은 **미확인**이다. 판독자 3개와 별도 감사는 같은 모델 계열의 다른 문맥이며 사람/독립 모델 재현이 아니다.
- 저장소/작업 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-043`.
- 계획 당시 통합 SHA: `785880f7b7c380dd49e0e4e6e6d90715a9b27838`.
- 실제 시작 SHA: `333e83c9a46b0c005d22efcccbb5a055b27e904e`. 원격에 작업 브랜치가 없는 것을 확인한 뒤 이 통합 HEAD에서 시작했다.
- 고정 결과 SHA, 마지막 실제 검사 대상 SHA, 이 인계 작성 직전에 원격에서 재독한 SHA: **`69060e2d1c3cf7f4502abe508679386a95bfa34e`**.
- 마지막 실제 원문 재독/무결성 증거: 고정 RESULT·수용 파일의 전체 본문과 Git blob/SHA-256 일치, `2026-11-22T21:07:54Z`.
- 세션 검사 완료: `2026-11-22T21:08:11Z`(한국시각 2026-11-23 06:08:11), exit 0 / `passed` / `remote_checked`.
- 이 검사 때 통합 HEAD: `8892cc093f7f23f6f7b029d5bc3dfa304c72f64e`. 시작 계약 해시는 유지됐고, 검사 오류·범위 밖 경로·미해결 충돌은 모두 0이다.
- PR/병합: **해당 없음**. 이 문서는 위 검사가 끝난 뒤 별도 마지막 커밋으로 작성하며, 그 커밋의 자기 SHA는 Git 이력에서 확인한다.

고정 산출물: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/RESULT.md) · [조건별 수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/evidence/acceptance-evidence.json) · [64짝](https://github.com/laadkke-arch/agentflow-open/blob/69060e2d1c3cf7f4502abe508679386a95bfa34e/docs/workstreams/research/AF-RES-043/pairs.csv).

필수 표 위치: 고정 RESULT의 **표 1은 3–36행(32개 자료행), 표 2는 40–57행(16개 층·과업·비교 집계)**이다. C/H 원관측 64행은 judgments.csv, 실제 열람/표시 109행은 reads.csv에 있다. RESULT는 200–204행의 정확히 세 약점 표로 끝난다.

## 2. 사용자 요구와 범위

목표는 소비자가 남긴 B, 추가 판/절 주소 L, 짧은 저장 발췌 X의 네 구성을 공개 참조 8건에서 비교하여 현재 용도 판단과 과거 인용 확인에 각각 무엇이 충분했는지 판독하는 것이다. 자연 표본 4건과 정정 우선 표본 4건, 카드 32개와 C/H 판독 64개를 유지했다. 과업당 발행 원문 요청 최대 2회, 실패도 1회, 로컬 X 표시는 별도로 기록했다.

착수 전에 GitHub에서 AGENTS.md, STATE.md, DOT_AUTOMATION.md, RESEARCH_WORKFLOW.md, dot-control의 AF-RES-043, 제품 연구 브리프와 의존 인계서를 읽었다. blob·경로·SHA는 [input-receipt.json](evidence/input-receipt.json)에 있다. 기준 제품문서는 [실제 시작판 RESEARCH_BRIEF](https://github.com/laadkke-arch/agentflow-open/blob/333e83c9a46b0c005d22efcccbb5a055b27e904e/docs/product/RESEARCH_BRIEF.md), 운영 규칙은 [실제 시작판 RESEARCH_WORKFLOW](https://github.com/laadkke-arch/agentflow-open/blob/333e83c9a46b0c005d22efcccbb5a055b27e904e/docs/RESEARCH_WORKFLOW.md)다.

쓰기 범위는 오직 `docs/workstreams/research/AF-RES-043/`다. dot-control.json 및 다른 연구/제품 파일의 변경은 0이다. 036의 12참조 재수집, 039의 네트워크 실행·접근 제한/전송비 회계 재실행, 사람 시간·재방문 비용 측정은 수행하지 않았다. 의존 작업은 고정 입력으로만 사용했다.

| 의존 작업 | 고정 결과 SHA·인계 |
| --- | --- |
| AF-RES-036 | [`5682b0d61a80edc159d4b510d213bbb4c69543be`](https://github.com/laadkke-arch/agentflow-open/blob/5682b0d61a80edc159d4b510d213bbb4c69543be/docs/workstreams/research/AF-RES-036/HANDOFF.md) |
| AF-RES-039 | [`cf3e62ef72b4272824873f07de3d2fe952dfb2e6`](https://github.com/laadkke-arch/agentflow-open/blob/cf3e62ef72b4272824873f07de3d2fe952dfb2e6/docs/workstreams/research/AF-RES-039/HANDOFF.md) |

## 3. 실제 변경과 중간 커밋

| 묶음 | 원격 SHA | 범위·확인 방법 |
| --- | --- | --- |
| ① 사전 규칙 | `a6cc61d4c2b6baf7cae47569c1454b371986ce47` | 첫 새 조회 전 표집층·두 목적·예산·판정 기준·예상 반례·manifest. SCOPE 해시와 원격 시각 보존. |
| ② 입력 봉인 | `b3aa200fce66f0635e74aa39c4cb008cafd86eff` | 소비 목적·날짜/판·별도 기준·sources/frame/versions·key·동일 요소 32카드. input-seal과 해시 대조. |
| ③ 판독 봉인 | `6c58c98d60351b9b125a8611887fec0972aeae1f` | 키를 받지 않은 새 문맥의 64 원판독·109 동작·실패/선행 노출. 아직 정오를 매기지 않은 read-seal. |
| ④ 대조와 수용 | `69060e2d1c3cf7f4502abe508679386a95bfa34e` | 원키 대조·64짝·두 감도·반례·RESULT/SELF_CHECK·40조건 수용 기록. 기존 원판정 필드 변경0, 표·분모·원문 재점검. |

| 파일/묶음 | 실제 내용과 이유 | 확인 |
| --- | --- | --- |
| manifest.json, SCOPE.md | 실제 배정 통합 SHA·환경·사전 규칙 | session start 성공, 사전 커밋과 입력 해시 |
| sources.jsonl, frame.csv, versions.csv, collection/ | 119개 직접 확인/실패 행, 최초 표집·탈락, 소비와 판 관계 | 필수 schema·중복군·28개 고유 1차 하한·엄격 구성 23/24 |
| components.jsonl, cards.jsonl, key.jsonl | 동일 B/L/X, 실제 카드 순서, 분리한 정답·근거 | 32개 본문/요소 해시·② 봉인 일치 |
| readers/, reads.csv, judgments.csv | 64 원판독과 실제 요청·도착·실패·로컬 표시, 추가 채점 | 원판정 기존 필드64/64 불변, 예산64/64 준수 |
| pairs.csv, analysis-summary.json, adjudication.jsonl | 사례 내 네 비교, 원규칙과 S-X/S-I 별도 계산 | 64짝·48집계 독립 산술 재계산 불일치0 |
| RESULT.md, SELF_CHECK.md, acceptance-evidence.json | 필수 표, Q1–Q7, 반증과 조건별 미달 | 구조 검사와 같은 모델 별도 문맥의 정적 감사 |
| amendments.md, normalization-log.json | 사후 발견한 표현/결측 검사 정정의 원수치·이유·영향 | 카드·키·표본·분모를 바꾸지 않음 |
| postcommit-verification.json, session-check.json/log | 결과 SHA 고정 재독과 실제 계약 검사 | 전체 본문 일치, 실제 exit 0 로그 |

## 4. 실제 검증 결과

착수 명령은 지정된 두 고정 의존 SHA와 허용 경로로 실행해 exit 0이었다. 최종 검사 대상은 ④의 고정 SHA다. GitHub 연결의 expected-SHA 조건과 force=false로 각 원격 커밋을 저장했고, 작성한 Git tree와 원격 tree가 같은 것을 확인했다.

```bash
python -B -m workbench.session start af-res-043 --allow docs/workstreams/research/AF-RES-043/ --output docs/workstreams/research/AF-RES-043/manifest.json --dependency work/research-af-res-036=5682b0d61a80edc159d4b510d213bbb4c69543be --dependency work/research-af-res-039=cf3e62ef72b4272824873f07de3d2fe952dfb2e6 --fetch
python -B docs/workstreams/research/AF-RES-043/scripts/validate_results.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-043/manifest.json --fetch
```

위 세 명령 모두 실제 exit 0이었다. 결과 연결 검사는 [validation.json](evidence/validation.json)에 `integrity_pass=true`, errors=[]로 남았다. 전체 8슬롯·32카드·64판독·64짝, 동일 요소, 키/카드 봉인, 원판정 불변, 두 필수 표, 마지막 약점3행, 공란의 명시값, 범위 밖 변경0을 확인했다. 세션 검사의 [원 로그](evidence/session-check.log)와 [구조화 로그](evidence/session-check.json)는 `passed`이며 Git 계약/소유 범위만 검사한 것이다. 연구 수용을 통과시킨 검사가 아니다.

고정 RESULT·수용 JSON을 GitHub에서 전체 재독했다. RESULT Git blob은 `dddf5c7f456096edda50fe308d53cb44e64b424d`, SHA-256은 `13687e25836b5b6cd14aba2ab5e1a656f8f43adf9032cbf7d2f87ed50a82f6c9`다. 수용 JSON의 result_sha256도 이 값과 같다. 파일별 비교·원격 URL·명령·시각은 [postcommit-verification.json](evidence/postcommit-verification.json)에 있다.

오류와 정정도 보존했다. ③의 단순 결측 검사가 원 href의 설명부가 붙은 미확인6건을 놓쳐, 둘째 요청의 원 href 미확인을1건에서7건으로 정정했다. 원HTML href 철자 확인은2/9이나 실제 부모/링크ID 연결은9/9다. 보고서 생성기의 UCLA 추가 L 링크 오류는 ④ 커밋 전에 봉인된 components.L에 맞췄다. 첫 CLI fetch는 FETCH_HEAD만 갱신해 로컬 추적 ref가③에 남았고 비교 exit1이었으므로 reset을 실행하지 않았다. 명시적 refspec fetch 후 동일 tree를 확인해 안전하게 맞췄다. 이 과정의 연구 내용 변경은0이다.

**미실시/미확인:** 사람 또는 독립 모델 재현, 실제 소비자 행동·시간·비용, 자연 소비자4건의 실제 외부판, J02의 독립 2018 문장 스냅샷, UCLA 당대본문·X, 미노출 literal href7건, 같은 URL의 과거/현재 HTTP200 직접 반복관측. 별도 사후 원문 열람20행은 수집/진단이며 ③의 요청·성과를 늘리지 않았다.

## 5. 판단·근거와 수용 상태

**현재 용도 판단과 과거 인용의 증거 수준을 분리해 보관하는 안을 제안한다.** L은 공개된 지목판에 실제 도달할 때 역사 대조를 도왔고, X는 발행자를 열지 못해도 저장 문구를 재표시하는 데 충분했다. X만으로 발행판 검증을 얻었다고 할 수는 없다. 이는 제품 요구 확정이나 모든 용도에 하나의 보관안을 채택한 결정이 아니다.

| 층·과업: 요구 근거 충족/기준 확인 | B | B+L | B+X | B+L+X |
| --- | --- | --- | --- | --- |
| 자연·현재 C | 3/3 | 3/3 | 3/3 | 3/3 |
| 자연·실제 소비판 H | **해당 없음**(기준0/4) | **해당 없음**(기준0/4) | **해당 없음**(기준0/4) | **해당 없음**(기준0/4) |
| 정정 우선·현재 C | 3/4 | 4/4 | 2/4 | 3/4 |
| 정정 우선·원키 H | 2/4 | 4/4 | 2/4 | 4/4 |

전체 C는24/28이고 원키 H는12/16이다. 자연층의 연구가 추가한 판 대조4/12는 실제 소비판 복원과 별도다. 유효 X의 H 재표시는14/14(발행판 대조도 한8건, 로컬만6건), X 추가의 발행판 대조 증가는0이다. 발행요청73회 중12회가 실패했고, 모든 과업의 요청수는1~2회였다. 로컬32동작 중 UCLA의 미확인 표시4회는 유효 X에서 제외했다.

L이 H에 기여한 정정 우선 사례는 T01과 J02다. [BEA 날짜 있는 최초 발표](https://www.bea.gov/news/2024/gross-domestic-product-first-quarter-2024-advance-estimate) L11–17은 archive 색인에서 끝나던 요청을 해당 절로 연결했다. J02에는 DOI 실패/직접 HTML 성공이 섞였다. [ONS 최초 발표](https://www.ons.gov.uk/economy/grossdomesticproductgdp/bulletins/gdpfirstquarterlyestimateuk/apriltojune2024) §2 L103은 B부터 그 발표를 가리켜 추가 L이 도착주소를 보태지 않았다. J01 H도 B를 포함한 네 구성 모두 성공했다.

[J01 정정](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0301218) L123–126은 원3716명을3806명으로 바꾼다. 옛 인용이 정확해도 그 수치의 현재 재사용은 틀릴 수 있는 반례다. 그러나 실제 소비자는 이미3806을 썼고, 이번 판독에서 X가 잘못된 주장을 확언하게 한 사건은0이다. C의 차이는 접근보류·순서/경로 선택과 함께 발생했다. [J02 정정](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0214558) L111–117,130–134는 배타적 위치 등의 주장을 제한하지만 선택한 좁은 유전자발현 역할을 철회하지 않는다. ‘정정이 있으면 모든 인용을 폐기’하는 판단도 지지하지 않는다. 원자료가 결과를 지지한다는 문장은 저자 진술이며 독립 재현 결과가 아니다.

S-X는 단서 없는 실제 X를 확인한7사례만 남겨 알려진 기준 성과24/28·12/16이 같다. S-I는 독립 옛 문장 기준이 약한 J02 H를 제외해 H10/12(B2/3, BL3/3, BX2/3, BLX3/3)다. 자연 H의0분모는 여전히 **해당 없음**이다. 두 감도를 결합한 새 주 분모로 바꾸지 않았다.

**수용40조건 중31충족·9미충족, `full_research_acceptance=false`다.** 고유 직접 1차 원문 하한28개는 전체 수량을 충족하지만, 지정 구성은 소비7/8+대상8/8+별도공지4/4+규칙4/4=23/24다. BMJ 발행자 소비본문 실패를 PMC 미러로 산입하지 않았다. 나머지 미충족은 엄격 표집 추적, 실제 X7/8, 판/발표 L5/8, 현재기준7/8, 본 H기준4/8, 카드 중립성, literal href2/9, 동일URL200의 강한 관측형이다. 각 조건의 분자/분모·파일·행·첫 재개 자료는 고정 수용 JSON에 있다.

공통 답 단서가 있는 N-S-01의4개 C판독은 규범적 보류로 원키대로 세되 일반적인 B 충분성으로 확대하지 않는다. DOI가 저작을 식별하는 것과 2018 불변 본문을 보증하는 것도 구별했다. 공개된 짧은 발췌·링크·관측 기록을 남겼으며 전체 제3자 HTML/ZIP 복제는 원격에 넣지 않았다. 다른 작업 파일이나 운영 제어 파일과의 편집 충돌은 없다.

**색인 제안:** AF-RES-043 — 판 주소의 조건부 발행판 대조와 발췌의 로컬 재표시를 분리; 현재 용도·과거 증거 수준 별도 보관 제안, 완전 표본 수용 미충족.

## 6. 다음 작업의 첫 행동과 재현 입력

첫 행동은 이 브랜치 원격 HEAD와 위 고정 결과 SHA의 차이를 확인한 뒤, **동일한 BMJ 소비 발행본의 Methods·Results·reference16을 직접 여는 것**이다. 이 문서를 뒤에 더 잘 열리는 사례로 교체하지 않는다. 성공하면 PMC에서 관측한 목적·3806과 대조해 소비7/8의 부족분만 별도 후속 증거로 평가한다. 실패하면 그 상태를 유지한다. 그 다음 UCLA의 당대 원문과 실제 소비판을 추적하며, 누락된 옛 검색순위를 새 검색으로 소급 작성하지 않는다.

원장 재검산과 계약 확인에 사용할 명령·입력은 다음과 같다. 연구 원관측을 덮어쓰는 build_inputs.py, seal_reads.py, normalize_ledgers.py를 재실행하지 않는다.

```bash
git fetch origin refs/heads/work/research-af-res-043:refs/remotes/origin/work/research-af-res-043
git show 69060e2d1c3cf7f4502abe508679386a95bfa34e:docs/workstreams/research/AF-RES-043/RESULT.md
python -B docs/workstreams/research/AF-RES-043/scripts/validate_results.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-043/manifest.json --fetch
```

현재 접근 환경에서 미완료인 BMJ 원문 재시도의 구체 입력/명령은 아래와 같다. 다음 환경에서 응답 본문을 실제 읽어 Methods·Results·reference16을 확인해야 하며 HTTP 성공만으로 본문 확인을 판정하지 않는다. 실행 결과는 기존 원관측에 덧쓰지 말고 새 증거 행에 시각·절·한계를 남긴다. 이 인계 시점에는 아래의 **후속 재시도 성공이 미확인**이다.

```bash
curl -L --fail --max-time 60 'https://bmjopen.bmj.com/content/11/2/e041022'
```

다른 최소 재개 입력은 [UCLA 옛 참조 issue808](https://github.com/statsmodels/statsmodels/issues/808#issuecomment-17410423), [Rolling Regression 원 예제](https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html), 봉인한 N-S-01 B 및 J02의 rc-029/rc-038 경로다. 방법 혼입을 분리하려면 부재 해석 문장을 제거한 새 자극·고정 요청방법·균형 순서를 별도 사전등록한 뒤 기존 카드/키에 노출되지 않은 판독자에게 읽힌다. 기존 결과를 그 새 시행으로 대체하지 않는다. 이미 지정된 두 의존 SHA는 그대로 입력으로 유지한다.

## 마지막 중요한 불일치·약점 — RESULT와 같은 세 건

| 중요한 불일치·약점 | 영향받는 판단과 근거 URL·행 | 다음 최소 조사·첫 자료 | 결과가 달라지는 조건 |
| --- | --- | --- | --- |
| 1. 필수 표본 구성과 표집 추적의 미달 | 소비 원문은7/8, 전체 필수 구성23/24. J01은 [BMJ 원문](https://bmjopen.bmj.com/content/11/2/e041022)의 발행자 접근이 실패해 PMC로 목적을 확인했다. UCLA 옛판·X는 미확인. 통계 최초10노출의 query순위와 J02 소비자 둘째검색의 상세 목록도 미확인. 근거: S-JOUR-J01-CONSUMER-PUBLISHER-HTML/FULL/PDF 및 collection/journals/consumer-search.csv; collection/statistics/search-metadata.json. | 먼저 동일 BMJ 발행자 원문 §Methods·ref16을 직접 열어 PMC의 실제 목적·3806을 대조한다. 다음으로 [statsmodels의 옛 UCLA 참조 기록](https://github.com/statsmodels/statsmodels/issues/808#issuecomment-17410423)에서 당대 발행판 보관 위치를 추적한다. 누락된 최초검색 순위는 새 검색으로 소급 복원하지 말고 새 프레임을 별도 등록한다. | 발행자 소비본문과 UCLA 당대판·X를 확보하면 필수 구성/완전요소 수용이 달라질 수 있다. 정확한 원 검색 로그가 발견되거나 별도 사전등록 표본에서 다른 유형이 먼저 나오면 표집 편향 판단도 달라진다. |
| 2. 실제 소비판·불변판과 연구가 추가한 판의 차이 | 자연4건의 실제 소비 대상판은 미확인이다. [Rolling Regression](https://www.statsmodels.org/v0.14.0/examples/notebooks/generated/rolling_ls.html) L89–111의192607값과 추가2022 archive의 일치는 전체 소비판 일치가 아니다. J02 [원저작](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201631#abstract0) Abstract L169–170은 현재 제공되는2018저작이며 독립2018스냅샷은 미확인. Crossref 정책 L165는 같은DOI의 in-situ교체도 설명한다. | 첫 자료는 Rolling Regression 원 예제의 내려받은 자료 생성일·실행환경·원파일 기록이다. 그 기록이 지목하는 판을 [발행자 archive](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors_archive.html)와 대조한다. J02는 발행자의 날짜 있는 원판 PDF/XML 보관본과 정정 전후 해당 문장을 따로 확보한다. | 소비자가 사용한 판을 직접 특정하고 해당 본문을 확인하면 자연 H의 기준 분모가 늘어난다. J02의 독립 옛 문장 또는 그 문장을 바꾼 기록이 나오면 S-I 포함 여부와 과거 대조 결론이 달라진다. |
| 3. 공통 답 단서·판독 순서·접근 방법의 혼입 | N-S-01 B의 시간 의도 부재 해석이 C보류를 암시한다(4/32C). 같은모델 판독자의 앞카드 노출, J01 DOI의 web/directHTTP 선택, J02 정정 link55실패→후행 link56성공이 남아 있다. 근거: cards.jsonl의 N-S-01 네 행; reader_b-J01-BX-C-p1; rc-029/rc-038; [J02 원문](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201631) L146. 둘째클릭 literal href도7/9 미확인이다. | 첫 자료는 봉인된 N-S-01 B와 J02의 두 정정경로 원장이다. 부재 해석을 제거한 N-S-01 네 C자극과 요청방법/정정경로를 고정한 J02 네 C자극을 새로 사전등록하고, 기존 카드·키에 노출되지 않은 판독자에게 순서를 균형배정한다. 실제 href를 노출하는 수집기로 원문자열도 보존한다. | 중립 B에서 보류가 줄거나 고정 요청방법에서 B와BL의 차이가 사라지면 현재 성과 차이의 설명이 달라진다. 같은 허용 원문을 받은 상태에서 X추가가 단정 오류를 만들 때에만 이번에 미확인인 X의 인과적 오도 주장을 지지할 수 있다. |
