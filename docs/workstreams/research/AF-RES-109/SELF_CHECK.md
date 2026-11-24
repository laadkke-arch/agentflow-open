# AF-RES-109 자기검사와 반증 경로

## 범위·판·주체

이 문서는 원장의 의미와 실험의 결손을 검사한다. **연구 수용은 PARTIAL, 엄격 비교분모는0/6**이다. 검산 프로그램 exit0은 원장 일치만 뜻한다. 검색/출처 검산, 저장소 기능검사, 원 프로젝트의 제안 실행은 서로 다른 검증이다.

모집·baseline 봉인 `62997151eed37758c5634bcd72f8342710a127a8`, 전체 검색 봉인 `628e33709b0be7a19486f1bfeaef93f42e129394`, 판독·사후 자료 봉인 `ada47907ac8ee68b5e12e02e246d37cdab0930fd`를 기준으로 비교한다. 현재 결과판의 정확한 SHA는 결과 커밋 뒤 작성하는 검증 영수증과 HANDOFF가 지정한다. 이 문서가 자신을 포함한 미래 커밋 SHA를 미리 알고 있는 것처럼 쓰지 않는다.

| 검사 주체 | 실제 본 정보·가림 | 확인 시각 UTC | 확인 범위·제한 |
| --- | --- | --- | --- |
| root | 계약·원문 현재판·모집/기지 안, 이후 두 방법 전체와 판독·사후 원장 | manifest2026-11-24 01:45:14; 모집 독해01:47:09 이후; 결과 구성은 검색 봉인 뒤 | 공유 Linux의 자동 작업자. R4 댓글 일부를 검색 전 보았으므로 깨끗한 검색자·맹검 판독자가 아님 |
| 12개 검색 문맥 | 각각 자연 입력 하나·그 방식 지시만; `fork_turns=none` | 01:52:01.773–02:21:13.915, 개별 구간은costs.csv | 실제 별도 문맥. immutable backend 모델 ID·검색엔진 자동 개봉은 미관측. R2-A/R6-B 우연 노출 포함 |
| blind_r1_r3 | 중립 패킷12묶음15변형과 R1–R3 입력; 방법·순위·후속 가림 | 직접 원문 재독02:27:28–02:32:00; 판정 개별 완료시각은 원장에 없음 | 관련 본문10주소, Function comparator 실패. 제품 실행0. 개별 판정시각을 소스 독해시각으로 대신하지 않음 |
| blind_r4_r6 | 중립 패킷16묶음18변형과 R4–R6 입력; 방법·순위 가림 | 원문 재독02:27:44–02:31:23; 최종 판정02:39:39 | R6 원 issue 요약02:29:49 노출 뒤 최종 판정. R6 결과 가림 실패·잠정치 유지 |
| execution_audit | 봉인된 원 실행·입력 지문·예산; 판정 없이 실행 원장 감사 | 실행 감사02:29:03.232475 | 48개 raw 파일의 내부 기록 감사. 원 검색엔진 표시를 재연했다고 주장하지 않음 |
| execution_audit 사후 역할 | 검색 봉인 뒤 공개 댓글·timeline·PR·릴리스 | 첫 사후 독해02:33:40 이후, 각 행read_utc | 2024 행동과2026 추천 구분. 실제 브라우저/제품 시험0 |
| blind_r1_r3 사후 계보 감사 | 방법을 공개한 전역 원장·기존 판독, 별도 source_count_crosscheck | 02:52:55.149252 | 검색 당시52개 취득행과17계보를 서면 감사. 새 웹 조회·과거 raw 원문 재생 없음 |
| blind_r4_r6 사후 검산 구현 | 방법을 공개한 원장·실행 감사·가림 기록 | 결과 구성 단계; 세부 메시지가 아니라 커밋·검산 로그로 재현 | 표와 계수를 재계산하는 코드 작성. 앞선 맹검 판정을 수정하지 않음 |

분리 판독은 실제로 수행했지만 사람의 독립 검토는0회다. 같은 상속 모델의 여러 문맥은 모델 계열의 독립성이나 이중 인간 판독이 아니다. 한 요청의 모든 후보를 서로 다른 두 판독자가 중복 채점한 설계도 아니다. 최종 원장 감사는 방법·순위를 아는 감사로 명시한다.

## Q별 답·증거·반증·분모·다음 관측

| Q | 답·미확인 | 원문 URL·절 또는 실행 행 | 결론이 틀릴 반례를 찾은 경로·결과 | 실제 분모·중복·결손 | 다음 관측 |
| --- | --- | --- | --- | --- | --- |
| Q1 부분과 보존 | 현재판6건의 부분·조건을 명시; 최초판0/6, Studio0. R2 조건쌍 약함, R5 topology 미확인 | requests.jsonl R1–R6의exact_location; frame.csv160행; [R5 편집 사건](https://api.github.com/repos/xyflow/xyflow/issues/events/11365940209) | 검색 전 별도 판독자가 R2/R5를 뒤 표본으로 교체하려는 안을 반박하여 첫3을 유지. 사후 R5 제목이 생성26초 뒤 바뀐 실제 예 확인 | 저장소2×첫80=160; 실제 선택6; 앞 탈락0; 뒤154 미선별. 현재판6은 최초판6과 같지 않음 | 공개 최초 본문판과 R5 원 그림을 읽어 같은 필수조건인지 비교. 없으면 현6자리 결손 유지 |
| Q2 기지 안 | 원문 링크·시도·실패·인자·버전 봉인. 미언급은 사전 목록에 없음만 판정 | baseline.csv 원래8열과 추가6열; R1/R3/R4/R6원문; evidence/start/input-newline-reconciliation.json | R1 Edit·번역과 R6 zoomOnPinch=true가 이미 원문에 있으므로 새 구현 제외. R2 원 버전3.13 및 후속 Node18.6/원문18.16.1 불일치 보존 | 자연 요청6, 합성 요청0. 제안 시험 입력은 사후 합성/진단. baseline 원래8열은629971판과 동일 | 최초판 복구 후 기지 안 재대조. 당사자 미인지 진술 없이 신규 인지로 승격하지 않음 |
| Q3 같은 입력의 검색 |12arm 실제 실행,30q/52명시개봉,33반환+3공석; 엄격분모0 | search.jsonl108행; evidence/search/*/events.jsonl; costs.csv; execution-audit.json 각pair | B 관계형 질의의 단어 유사 drift와 A의 자유 재질의도 보존. 자동 후속 노출, R3-B 순서 불일치, 실제 개봉23vs29를 검토 | 6쌍 탐색 기록, strict0. 상위5위150자리 중 R2-B event5의4공석. 자동개봉·tokens·금액null | 모델ID·자동 노출 계수·단조 사건시각을 관측하는 환경에서 새 문맥·새 봉인으로 재실행 |
| Q4 계보와 형태 |33반환을28요청-URL묶음/26고유URL로 가려 판독. 검색 고유산입17계보 | candidates.csv; source-accounting.json; source-genealogy-audit.json52dispositions; 원전절은sources.jsonl | yFiles API/데모, Chromium 두revision, React Flow 동일기능 반복을 합침. i18next재작성·unpkg미러·Function본문실패 제외; metadata행을 실제 본문행으로 이동 | raw52취득/37자체true→global17. 원저작17은 구현17·분야17이 아님. blind재독·실패0추가 | 특정 계보가 실제 다른 원저작이라는 원 저자·버전·구현 증거가 생길 때만 분리; URL 차이만으로 늘리지 않음 |
| Q5 바뀐 선택과 시험 |선택12·시험27은 조건부·제안, 실제 실행0. R6선택3/시험5잠정. 원 조건 전체 해법12개가 아님 | choices.csv33행의 old_approach/changed_unit_order_responsibility/preserved_condition/minimum_input/expected_output/broken_source_assumption | [Kubernetes SSA](https://kubernetes.io/docs/reference/using-api/server-side-apply/)의 소유권별 생략 삭제로 보존 일반화 반박. [Qt](https://doc.qt.io/qt-6/qgraphicsitem.html) mousePress/setAcceptedMouseButtons로 hit 통과와 drag 보존 분리. [Cytoscape bezier](https://js.cytoscape.org/#style/bezier-edges)로 평행pair와fan-out 구분 |15새구현결정행+12시험만행+5근접오답행+1근거부족행=33. flags는키중복제거 후12/27; R1–R5만9/22. 먼분야발견0 | EXECUTION_PLAN의 최소 입력과 같은 구성의 실패 대조를 실제 원 프로젝트에서 실행 |
| Q6 시점·조건 |현재 적합성·역사적가용성 별도. R5 yFiles는동일끝점 해석에서만조건부. 원판검증 미완 | candidates.csv historical_judgment와conditional_target_fit; CSS UI4 §6.2, Vault versioned1.15, Chromiumcommit, RF12.4.2 |2026 Auxx/Vendure/CSS를2024로 소급하지 않음. Vault1.15경로본문과no-pre1.16내비게이션 충돌. [GNU msgcmp](https://www.gnu.org/software/gettext/manual/html_node/msgcmp-Invocation.html)§10.7, [Playwright](https://playwright.dev/docs/actionability)Visible/Editable/Receives Events, [UIEvents2019](https://www.w3.org/TR/2019/WD-uievents-20190530/)trusted/deltaMode/cancelability를 원전 반례로 읽음 |각33후보의 역사판 열 유지; 두 조건 무조건 충족·당시가용 엄격성공0판정가능. 6반례는 사후층·실행0 | 요청시점 고정tag/commit/문서snapshot과 동작 구성을 함께 확보. 누락은미확인 |
| Q7 누가 실행했나 |패치+릴리스3/6, 원 요청자복구진술1/6, 추천을배워실행한 인과효과분모0, 절약시간미확인 | aftermath.csv6행; [PR4506](https://github.com/node-red/node-red/pull/4506), [PR4526](https://github.com/node-red/node-red/pull/4526), [PR4230](https://github.com/xyflow/xyflow/pull/4230); R2comment1874067118 |R6긍정진술철회·Windows실패·후속느린zoom을 읽어 closed=완전성공 반박. R4selected:false와R2버전불일치 원문 유지. 2024행동은2026추천의 결과가 아님 |6issue,24댓글,76timeline events;42성공응답(빈9포함),4실패. 사건내PR·패치·릴리스 중복산입0. 원 요청자의수정후확인 R1/R3/R4/R5/R6미확인 |기존 공개원전의 당사자재시험·CI·정확한릴리스 읽기. 추천노출뒤같은주체실행·시간기록이 없으면인과/절감판정 보류 |

## 반대 근거로 달라지거나 보류된 행

| 변경 | 앞선 표현·문제 | 최종 처리와 근거 |
| --- | --- | --- |
| 모집 R2·R5 | 조건이 약하다는 이유로 뒤 요청 대체를 고려 | 검색 전 원순위 첫3으로 교정; 뒤154행은 미선별. 규칙이 기준이며 풍부함이 선별 기준이 아님 |
| 입력 지문6쌍 | raw CRLF hash와 actual LF hash를 동일한 것으로 기록 | 원 hash 유지+실제 실험 hash 추가;12arm 일치. 원문 내용 수정·재검색 없음 |
| R2-B3 Function comparator | 원 검색자는 operative source를 읽었다고 기록 | 독립 본문 검증503/raw차단으로 채택 보류;새구현0·시험0. 원 검색 기록을 삭제하지 않음 |
| 검색 원자료 산입 | 작업자37개 true를 합산할 위험 |14원래carrier유지+3본문행이전=17;23원래true제외/통합. 감사52행 전부 유지 |
| R5-B2/B3 | blind yes/yes가 전체 원요청 성공으로 오해될 위험 | `same_pair_interpretation_only`;원그림topology미확인. 원 blind판정은수정하지 않고root해석별도열 |
| R6 전체 | 방법·순위 가림을 후속 가림까지 완전하다고 오해 |02:29:49 노출,02:39:39최종판정.6반환행과choice/test전부잠정치. 노출자료를 인용에서 빼도 가림복구 안됨 |
| R3-B 공통 소비 |event index와UTC시작순이 일치한다고 가정 |후보1/3 indeterminate;확정common후보0. 두 순서별prefix원장보존 |
| R5 최초판 |현재제목이최초제목이라고 가정할 위험 |사후 rename event26초차이 확인;현재입력유지·최초판미확인 강화 |
| R6-B1 판 날짜 | 독립 재조회 실패를 전체 날짜 미확인으로 요약 | 원 검색R6-B-S6의tree2018-10-12표시와나중조회실패를병기;배포·시간대미확인.원판독은유지 |
| 후속 출처 ID/실패주소 |조립 중 AFTER를중복접두사하거나실패요청URL을도착주소로 채울 위험 |raw후속의AFTER-ID를보존;실패actual_url:null. 최종독립원장감사에외래키검사 |

## 원자료 하한과 단위별 대사

| 단위 | 목표·예정 | 실제 | 결손·중복 처리 |
| --- | ---: | ---: | --- |
| 자연 공개 요청 |6 |6현재판 |최초판0; Studio0은별도층 |
| 합성 모집 요청 |0 |0 |원문 없는값합성없음 |
| 검색 실행 |12 |12 |질의30·명시개봉52, 재실행0 |
| 예정 최종자리 |36 |33반환+3공석 |원순위1–3전부유지 |
| 검색 반환 원 설계·구현 |8 |17보수적계보 |52취득행,같은기능·원전·실패·미러중복제거 |
| 다른 계보 반례 |6 |6 |모두사후직접원전, 실행실험과별도 |
| 외부 분야 원전 |4 |4 |OCFL/PREMIS와NIST/MIL;PROV보조0추가 |
| 총원자료 |24 |33 |6요청현재판+17검색+6반례+4외부;역사적자격과별도 |
| 새 선택·시험 |양성수완료조건없음 |12선택·27시험 |동일키중복제거,근접오답포함조건부;R6잠정3/5 |
| 실제 후보·제품 시험 |실행시증거필수 |0 |미실시명령·입력은EXECUTION_PLAN |
| 원 요청자후속 |6사건조회 |명시복구1 |나머지5수정후본인확인미관측 |
| 추천학습→같은제안실행 |판정가능사건 |0 |시간절감도미확인 |

## 재현 검산과 인계 순서

`recalculate.py --write`로 필수표6/36/6행과 RESULT를 만들고 `--check`로 같은 원장에서 다시 비교한다. 48개 raw검색파일은628e337판과 byte일치, baseline원래8열·requests원래필드는629971판과값일치를 검사한다. 로컬구성검산은통과했으며 이것은아직원격고정결과SHA검사의영수증이아니다.

결과판커밋→원격고정RESULT/원장/대표원전/재현절차다시읽기→manifest --fetch/공통cloud_check --require-clean/작업별--check→별도영수증커밋→HANDOFF단독커밋순서를지킨다. 고정검사는내용이동일한깨끗한별도checkout에서실시하고 검사결과를원결과판내용과구분한다. 자동발견세션수와명시manifest검사수를실제출력에서기록한다. 0개자동발견은본manifest검사통과가아니다. 공통workbench테스트는후보실행시험이아니다.

최종 gate 결과와 정확한 검사 SHA는 `evidence/validation/`의 영수증 및 HANDOFF를 따른다. 검사 뒤 추가한 파일이 이전 결과 SHA에서 검사되었다고 표현하지 않는다. 자료 수를 채웠어도 핵심 비교·독립성·최초판 자격이 미달이므로 PARTIAL을 유지한다.
