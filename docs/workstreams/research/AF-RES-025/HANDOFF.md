# AF-RES-025#1 인계 — REVIEW_READY_WITH_GAPS

## 1. 식별

- 작업 ID / 시도: **AF-RES-025#1**, 힌트 없이 찾는 설계 선례.
- 종류 / 담당: **web-pro**. 공개 작업자 참조는 이 브랜치의 manifest와 세 stream 기록이다. 별도 비공개 작업 조회 ID는 공개 산출물에 넣지 않는다.
- 실제 환경 / 모델: ChatGPT Linux cloud workspace `/workspace/scratch/d11ea598a19b/agentflow-open`; 세션 표기 **GPT-6 Astra Pro**. 같은 상속 모델의 별도 에이전트가 교차 판독했다. 별도 Pro UI의 모델 선택 화면이나 사람의 독립 판독은 관측하지 않았다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-025`.
- 계획 기준판: `e2d0917ccd0e0010e14627a2f919265c332cec53`.
- 배정 당시 최신 통합·시작판: `b420fb7e1e01f4a366512fa71c0f507051aa6a19`.
- 마지막 계약 재조회 통합판: `01394a47888fba39e3babf6ad0249a1a37ace76c`(2026-11-22 06:32:45 UTC), fingerprint `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc` 동일.
- **고정 결과 커밋: `1f945abb4ba72060b0df3307bf27123478a40d05`.** RESULT·SELF_CHECK·수용 근거·sources·검산·공개기록 정정 파일을 2026-11-22 **06:35:37 UTC**에 이 SHA로 원격 직접 재독했다. 그 확인 이후에 이 HANDOFF를 작성했다.
- 인계 로컬 검산 시각: 2026-11-22 **06:39:11 UTC**. 원격 결과 확인보다 뒤이며, 인계 자체의 원격 재독은 이 문서를 포함한 마지막 커밋 뒤에 수행한다.
- 최종 상태: **REVIEW_READY_WITH_GAPS**. 연구 내용의 미충족 조건 다섯 건을 숨기지 않는다. 결과 커밋에 대기 상태였던 ‘결과 원격 확인 후 인계 작성’ 게이트는 실제 재독 뒤 충족으로 갱신했다.
- 작업 창: 2026-11-22 **04:46–06:39 UTC**(인계 작성 기준). 본 검색 요청 창은 **05:05:33.538–05:25:49.178 UTC**, 최초 원문 열람은 **05:06:02.750–05:26:09.327 UTC**다. 후속·감사·보조 읽기는 별도 비용 단계다. 현재 검색을 2021년 당시 검색 결과라고 부르지 않는다.
- PR: 만들지 않았다. 자기 작업 브랜치 커밋과 인계만 수행했다. 이 인계 자체의 마지막 원격 SHA는 `git log -1 --format=%H -- docs/workstreams/research/AF-RES-025/HANDOFF.md`와 브랜치 head로 확인한다.

## 2. 사용자 요구와 작업 범위

목표는 처음 주어진 설계 전문과 목적에서 실제 반환할 기존 해법 링크를 찾아, 자유 목적 검색 G와 목적·부분 관계로 질의를 만든 R을 같은 상한에서 비교하는 것이다. 새 제품명 발견과 기존 호스트에서 놓친 부품/제약의 가치를 나누고, 원문 전체를 열었는지와 독자가 받은 인용만으로 필수 근거 전체를 확인할 수 있는지를 각각 판정했다.

공통 절차는 배정판의 AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW, CLOUD_WORKFLOW, product/RESEARCH_BRIEF, HANDOFF_TEMPLATE, dot-control의 AF-RES-025 항목에서 읽었다. 연구 입력은 지정된 **AF-RES-021@29049a5f15b6ef7cd7431f59a059598db6f5d857**와 **AF-RES-022@df80ec2406042a73c2114e316894173f66309cda** 및 각 HANDOFF로 고정했다. 이 차수 다른 작업의 결과는 사용하지 않았다. 원 URL·읽은 위치는 `evidence/internal-sources.json`과 `baseline-audit.md`에 있다.

작성 소유 경로는 **`docs/workstreams/research/AF-RES-025/`만**이다. dot-control, 공통 진행표·계약·색인은 편집하지 않았다. 기존 후보 목록, 지원 스레드, 176개 선행기술 목록, 017 성공 사례로 표본을 채우지 않았다. 실제 제품 배포나 계정 변경, 사람에게 메시지 발송도 이 범위에 없다.

## 3. 실제 변경과 고정 결과

| 산출물 | 실제 내용 | 확인 방법 |
| --- | --- | --- |
| SCOPE·manifest·frame·questions·queries | 기간/정렬/제외/상한·판정 규칙, 메타데이터425행, 최초12전문 해시,24경로72질의 | 사전 커밋 a27f88b/a4b4a02, Q08 공개 정정3bf7dc4; 입력219개 검사 |
| search-log·stream receipts | 실제 요청·UTC·제공순위·탈락·중복·재시도·실패 | 공통835이벤트와 원 요청/응답해시; 원문130호출 결과 감사 |
| returns-raw·returns·candidates | 원72슬롯과 원래 순위/인용; 사후3 URL판 별도72슬롯 | 원 인용 추가·재정렬 없음, 원8경로 URL 초과 보존 |
| blind·reviews·judgments | 경로/순위를 가린93키,104인용 묶음,337필수조건 | 주 판정 d1f506b 봉인 해시; 공급자337조건 불변, 후속 열만 추가 |
| followups | 12질문 후속 결정·diff,66고유 반환 후보의 당시판 | 태그/코드/발표일·정확한 절·공급자/질문자/연구자 분리 |
| sources·supplements | 390관측, 직접 원문 보수적 산입174; 도서관2/제조2 원문과 깨짐 조건 | 요약·차단·metadata·중복patch 제외, 별도 문서와 계보 분리 |
| pairs·metrics·literal-top1 | 질문 단위 승무패와 전체/부분·현재/당시·상위1·노출 민감도 |48개 metric행 별도 재집계 일치, 첫후보와 첫URL 구분 |
| RESULT·return-examples·SELF_CHECK·acceptance | 네 필수 표·Q1–Q7·실제 링크·반례·한계·수용 bool | 결과 고정 SHA에서 원격 재독; 통합1146개 검사 통과 |
| pending-checks·verification-inputs | 실행하지 않은 PyArrow/GCC/ScalarValue/Java 경계의 고정판·명령·입력 | 실행 영수증과 분리, 실제 통합·큰 메모리·인시 미확인 |

### 검산한 분모와 결과

| 단위 | 확정 값 | 해석 |
| --- | ---: | --- |
| 모집 메타데이터 |425행 | Arrow335 + Cargo51 + Jupyter39. 확률 표본이 아님 |
| 새 최초 설계 질문 |12 | 프로젝트당4, 전체6·부분6. 서로 다른 설계 사건이며 통계적 독립성 보장은 아님 |
| 실제 G/R 경로·질의 |24경로·72질의 | 두 경로 동일 전문/도구/영어/조회일/공개 범위 |
| 검색 제공 결과 |633 | 처음10 이내616, 밖17 제외.49질의에서104슬롯 부족 |
| 원문 최초/재시도/절 추가 |120 / 7 / 3호출 |130호출 중 본문115·접근실패8·재작성요약7; 본문 반환은 조건 충족과 다름 |
| 원 반환 슬롯 |72 | 충족2·근접 충돌14·보류53·빈3. 비빈69/고유후보66 |
| 사후3 URL판 |72 | 충족2·충돌11·보류49·빈10. 원 예산 위반을 지우는 재실행이 아님 |
| 가린 판독 |93키·104묶음·337조건 | 반환66후보 + 미반환27키, 묶음별 인용을 합치지 않음 |
| 새 대상 주 지표 |**G0/12 · R0/12** | G승0·무12·R승0. 모두 신규 완결 성공이 없는 동률 |
| 현재 기지 호스트의 새 부품 |**G2/12 · R0/12** | Q01 PyArrow 조건부 구성, Q11 ipykernel 어댑터. 정확 부품명을 저자가 알았다는 뜻은 아님 |
| 첫 고유 URL만 남김 |신규0:0; 새 부품 G1·R0 | Q01은3문서가 필요해 탈락, Q11 한 파일의 두 절은 유지. 첫후보만 남길 때는 G2 |
| 원 슬롯의 신규성 집단 | G 새 대상25·기지 새 용도11; R 새 대상25·기지 새 용도6·기지 기존2·빈3 | 새 대상 유효0/25씩, 기지 새 용도 현재G2/11·R0/6. 각 경로 전체 슬롯 분모는36 |
| 당시판 전체 기능 | supported1 / not_available19 / unknown46 |66후보. 유일한 supported는 조건부 GCC10.3 부품이며 원 인용 부족은 남음 |
| 당시 완결 검색 성공 |신규0:0; 기지 새 부품0:0 | 현재 완결 두 부품의 정확 기능은2023/2025 도입으로2021에 소급 불가 |
| 노출 제외 민감도 |좁게6질문, 메타까지4질문 |두 집단 모두 신규 G0·R0. 가림 단어 노출 질문 제외는9질문 |
| 직접 외부 원문 최소수 |**174** | 최초12·공급자99·역사 공급자32·후속 결정24·기타 원저3·보조4. 같은 계보 별도 자료도 보수적 제외한 하한 |

## 4. 실제 검증 결과와 재현

- `python -B .../tools/check_inputs.py`: **219/219**, exit0. 기록 `evidence/input-check-final.json`.
- `python -B .../tools/audit_baseline.py`: 고정021의18집계행이 저장 결과와 동일. Q11c 전체인용 조건을 적용하면2절의6/23·9/23·14/23은 **6/23·9/23·13/23**이 된다. 기록 `evidence/reproduction-checks.json`, `evidence/baseline-recount.json`.
- `python -B .../tools/validate_artifacts.py`: **1,146/1,146**, exit0. 질문/슬롯·source 참조·원 판정 바이트·인용 conjunction·표 구조·최종3약점행·공개 식별자 검사. 기록 `evidence/artifact-validation.json`.
- `PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check .../manifest.json --fetch`: **passed/exit0**, 소유 경로 밖 변경과 미해결 병합0. 기록 `evidence/session-check.json`. 계약 검사는 연구 결론이나 제품 실행 검증을 대신하지 않는다.
- 별도 같은 모델 판독자가 metric48행을 scored-slots에서 재집계해 불일치0을 확인했다. 원문 수·귀속·링크 오류와 OGC 역사판 경계 오류는 `evidence/final-review.json`, source eligibility override, JP-AMEND-001에 정정 이력을 남겼다.

### 고정 결과 확인 명령

아래는 이미 읽은 결과를 같은 SHA로 확인하는 명령이다. `git show`는 파일을 수정하지 않는다. 최신 브랜치를 결과 SHA와 혼동하지 않는다.

```bash
git fetch origin work/research-af-res-025
git show 1f945abb4ba72060b0df3307bf27123478a40d05:docs/workstreams/research/AF-RES-025/RESULT.md
git show 1f945abb4ba72060b0df3307bf27123478a40d05:docs/workstreams/research/AF-RES-025/SELF_CHECK.md
git show 1f945abb4ba72060b0df3307bf27123478a40d05:docs/workstreams/research/AF-RES-025/evidence/acceptance-evidence.json
git show 1f945abb4ba72060b0df3307bf27123478a40d05:docs/workstreams/research/AF-RES-025/evidence/source-counts.json
git log -1 --format=%H -- docs/workstreams/research/AF-RES-025/HANDOFF.md
```

원격 확인 blob은 RESULT `a50460ba3f5939e8754af93362957bd30cc804d6`, SELF_CHECK `8aef3c42e6afaf497acb590bc1a346a255f211a1`, 수용 근거 `7ecb93d5475a21fae4bb7188a0bbdcccd4356218`이다. 이 결과 커밋의 수용 배열은 연구 공백5건과 인계 순서 대기1건을 담는다. 현재 인계 커밋은 실제 원격 확인을 근거로 마지막 대기 항목만 true로 갱신한다. 연구 판정·분자·분모는 바꾸지 않는다.

전체 재집계 순서는 SELF_CHECK에 있다. 새 checkout에서는 Arrow 메일을 `streams/arrow/restore_inputs.py`로 공개 Message-ID에서 복구하고 해시를 확인한다. 원 전문을 복구하지 못하면 다른 텍스트로 대체하지 않는다. 동일 질의를 현재 다시 검색하는 것은 기존 관측의 검산이 아니라 새 실행이다.

**실행하지 않은 것:** PyArrow→Java 실제 통합, Java C Data/JNI와2GiB 초과 경계, 당시 GCC/ScalarValue runtime, 실제 사용자의 사전 지식·채택 시간. 명령과 입력은 `pending-checks.md` 및 `followups/arrow/verification-inputs/`에 있다. 문서만으로 충분하지 않은 사용 경계에는 해당 미실시를 그대로 남겼다. 토큰·실제 과금·인시 절감은 미제공/미관측이다.

## 5. 판단·근거와 진행 담당에게 제안

이번 결과는 R이 일반 검색보다 더 좋은 신규 완결 링크를 남겼다는 주장을 지지하지 않는다. 동시에0:0을 두 방식의 일반적 동등성이나 모든 선례의 부재로 해석할 근거도 없다. 고정 질의·첫 적격5원문·현재 검색·작은 목적 표본에서 어떤 필수 근거가 남았는지를 보여주는 기록이다.

현재 G에서 찾은 두 부품은 새 제품명보다 기존 호스트의 놓친 호출 경계를 드러내는 가치가 있을 수 있다. 이는 연구자의 제품 제안이며 사용자가 실제로 몰랐거나 시간을 절약했다는 관측이 아니다. Q02에서는 DataFusion 이름이 원 검색에 있었지만 필요한 `ScalarValue` 부품은 반환되지 않았다. Q07은 후속 수용 과정에서 최초 HTTPS 조건이 삭제돼 최종안을 정답키로 쓰면 안 된다. Q09는 matching 순서를 receiver 준비로 바꾸어 읽던 역사 판정을 반례로 낮췄다. 관련 정확한 원문 위치는 RESULT 표2/4와 후속 source IDs에 있다.

### 남은 다섯 수용 공백

1. 원 실행8경로의 최종3 URL 초과. 기계적 제한판을 만들었으나 원 프로토콜을 복구하지 못한다.
2. 가린3키의 경로 단어 노출, 해석 표현 잔존, G/R 공유 문맥. 별도 같은 모델 판독은 사람의 독립 실험이 아니다.
3. JEP66 더 이른 blob과 Arrow Q04 연결 branch의 최초 head를 완전히 복구하지 못했다.
4. 반환66후보 중46개의 당시 전체 필수 기능은 미확인이다. 각 행에 실제 탐색 범위·다음 최소 자료가 있다.
5. 현재 main/latest 일부 문서에 불변판이 없고 검색의 완전 재현은 보장되지 않는다. 관측 UTC·판·해시와 고정판 자료를 구분했다.

공통 색인에는 **REVIEW_READY_WITH_GAPS**, 고정 결과 SHA와 인계 SHA, 12질문/24경로/72슬롯, 신규 완결 G0·R0, 현재 기지 새 부품 G2·R0, 예산/노출 공백을 함께 연결할 것을 제안한다. ‘R 효과 없음’이나 원문 수 충족만으로 요약하면 판단 범위가 사라진다. dot-control과 색인은 진행 담당이 갱신할 사항이며 이 브랜치에서는 수정하지 않았다.

### 공개 기록 정정

Jupyter 후속 요청32개의 내부 연결 선택자가 중간 커밋 `0a61785...`에 들어간 것을 최종 검사에서 발견했다. 현재 결과판에서는 요청 필드만 가렸고 원 URL·시각·응답 해시·판정은 유지했다. 인증 토큰으로 확인된 값은 아니며, 과거 Git 이력을 재작성하지 않았으므로 과거 사본까지 삭제됐다고 주장하지 않는다. `followups/jupyter/amendments/JP-AMEND-002.json`에 영향·이전/현재 해시를 남겼다. 현재 공개 파일 검사는 해당 값 패턴0이다. 한 차례 생긴 소유 경로 밖 Python cache 세 파일도 자기 생성물임을 확인해 제거하고 `runtime-cache-cleanup.json`에 남겼다.

## 6. 다음 대화의 첫 행동

먼저 작업 브랜치의 최신 SHA와 이 HANDOFF의 마지막 커밋을 조회하고, 위 고정 결과 `1f945abb...`와 달라진 파일을 비교한다. 그다음 `evidence/acceptance-evidence.json`의 false 다섯 행을 읽는다. 새 검색을 기존 결과 위에 덮어쓰지 않는다.

첫 구체 연구 행동은 **원 URL 예산과 문맥 공유를 제거한 재실행의 사전등록**이다. 입력은 같은12개 최초 전문과 봉인된 필수 술어, 비교 기준은 이 결과의72슬롯이다. 결과를 모르는 별도 문맥에 G/R을 나누고 원문 관측만으로 새 판독 packet을 만든다. 경로당 최종 URL 세 개를 먼저 명시하고, 기존 후보명·후속 선택·보조 분야 적중을 질의 작성자에게 주지 않는다. 예산 위반0과 경로 간 노출 기록을 확인하기 전에는 기존 결과와 합산하지 않는다. 이는 진행 담당에게 제안하는 후속 조사이며 공통 작업 ID를 임의로 새로 배정하지 않았다.

이미 찾은 부품의 실제 사용을 먼저 검증한다면 `pending-checks.md`의 작은 PyArrow 입력이나 고정 ScalarValue 입력부터 실행하고, 환경/명령/출력/실패를 새 영수증으로 남긴다. 과거 API 기능을 현재판 코드로 대신하지 않는다. 의존은 지정021/022의 고정 SHA이며 다른 진행 중 연구 결과를 새 입력으로 쓰려면 별도 범위를 기록해야 한다.

| 중요한 약점 | 근거 ID·URL | 영향을 받는 결정 | 후속 조사 한 건·최소 확인 |
| --- | --- | --- | --- |
| 1. 원 비교의 통제 공백:8/24 URL 예산 위반, 가림3키 노출, G/R 공유 문맥 | [URL예산](evidence/return-url-budget.json), [가림 정정](evidence/blinding-amendment.json), [노출 원장](evidence/exposure-summary.json) | R/G 인과적 우열과 같은 비용의 범위 | 동일12전문으로 독립 문맥24경로를 새 봉인·실행. 최종3URL, 후보 선택 규칙, 결과 사전 비노출과 예산 위반0 확인 |
| 2. 기지 호스트와 기지 부품·실제 사용자 가치가 다름. 현재 유효 두 기능도2021보다 후발 | [신규성 단위](evidence/novelty-units.json), [Arrow21](https://arrow.apache.org/blog/2025/07/17/21.0.0-release/), [ipykernel6.27](https://github.com/ipython/ipykernel/releases/tag/v6.27.0) | 새 제품 탐색 vs 놓친 부품 탐색, 인시 절감 주장 | 한 실제 설계 과제에서 검색 전 제품/부품/제약 목록과 적용 후 정확도·시간을 관측. 문서 침묵을 미인지로 대체하지 않기 |
| 3. 당시판 전체 조건·최초 구현 경계와 기능 단위 추적이 미완결 | [후보 역사](candidates.csv), [Q02 후속](followups/arrow/decisions.jsonl), [실행 입력](pending-checks.md) | 당대 사용 제안과 근거 부족 후보의 보류 해제 | 당대 `ScalarValue` 고정4b7cdcb 코드·공식 테스트를 원 query3/rank4 Array 재수출 적중과 대조하고 Boolean/Utf8/List 입력 재현. 기능 링크 발견은 별도 후속 실행으로 기록 |
