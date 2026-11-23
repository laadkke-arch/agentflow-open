# AF-RES-063#1 인수인계 — 부분 인계

## 1. 식별

- 작업 ID / 시도 번호: **AF-RES-063 / #1**.
- 배정 작업 종류: **web-pro**. 실제 조사·검사 주체: ChatGPT GPT-6 Astra Pro `/root` 및 pandas_reports / moment_reports / execution_artifacts 병렬 조사자, 제공된 Linux 클라우드 작업공간. 별도 웹 Pro UI에서의 모델 선택 확인은 미실시다.
- 공개 가능한 작업자 참조: 이 저장소의 AF-RES-063#1과 고정 커밋. 별도 비공개 작업 ID는 저장하지 않았다.
- 역할: 과거 공개 날짜 계산 출력에서 실제 시간대 자료판을 귀속할 수 있는 범위와 반례 조사.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-063`.
- 실제 시작 SHA: `1e741fd0def88ef56b1060a478d81f1985a4e760`. 계획 기준 `aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75`와 구별한다.
- 선행 인계 SHA: `e91b8abe3eee98d469ae80d7ca152ff08047c8d9`; 선행 본문 SHA: `5c975cf275b90cf8d18a6425c6f00c210febacec`.
- **고정 결과 SHA / 이 인계 작성 직전 원격에서 다시 읽은 마지막 저장 SHA: `86403f9082bfebe9eafefe00e673942380041761`**.
- 마지막 실제 진행 증거: 위 SHA에서 `workbench.session check --fetch`가 **passed / exit0 / remote_checked**, `2026-11-23T05:44:34.621395+00:00`. 같은 SHA의 통합 읽기전용 검사는 **44/44**, exit0.
- 원격 결과·수용원장 재열람: **2026-11-23 05:44:02–05:44:03 UTC**, 두 원격 blob SHA와 로컬 파일이 일치했다.
- PR 주소: 해당 없음. 작업 브랜치 커밋으로 인계한다.
- 최종 조사·검증 확인 시각(UTC): `2026-11-23T05:44:34.741639+00:00`. 이 인계 작성 UTC: `2026-11-23T05:46:55.355590+00:00`.
- 템플릿 상태: **BLOCKED / 부분 인계**. 조사·기록·내부 검증은 완료했지만 원자료 결손 때문에 완전 수용을 승인하지 않는다. HANDOFF 자체는 이 결과판 다음의 **마지막 단독 커밋**으로 저장한다. 자기 커밋 SHA를 본문에 순환 참조하지 않으며 실제 인계 커밋은 브랜치 HEAD와 이 파일의 GitHub 주소로 식별한다.

**먼저 볼 고정 결과:** [필수 표1: 자연6+보강4](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/RESULT.md?plain=1#L1) · [필수 표2: V0/V1/V2](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/RESULT.md?plain=1#L14) · [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/acceptance-evidence.json) · [자체 검토](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/SELF_CHECK.md).

## 2. 사용자 요구 / 작업 범위

목표는 “그 SDK가 그날 그 자료판으로 이 현지 날짜를 냈다”를 공개 기록으로 어디까지 승인할 수 있는지 조사하는 것이었다. 보고 우선6자리와 실행물 우선4자리를 분리하고, 원 입력·지역·호출·출력·로드 공급자·자료판을 같은 사건으로 연결하는지 점검했다. 최소20원저작 독해, 다른 분야2저작, 양방향 반례, 세 보기와 비용, 원장·필수표를 요구대로 남겼다.

기준 문서는 [제품 목적](https://github.com/laadkke-arch/agentflow-open/blob/aa1dc65e4eefa9df9a8e8ae694ffadda52a12a75/docs/product/RESEARCH_BRIEF.md) 및 실제 시작판의 [연구 운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/1e741fd0def88ef56b1060a478d81f1985a4e760/docs/RESEARCH_WORKFLOW.md)이다. AGENTS/STATE/DOT_AUTOMATION/RESEARCH_WORKFLOW와 dot-control의063·059를 먼저 읽고 선행 HANDOFF 및 지정7파일을 인수했다. [인수 URL·해시](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/intake.json).

허용 쓰기 경로는 `docs/workstreams/research/AF-RES-063/`뿐이었다. 모든 커밋 변경이 이 경로 안이다. `dot-control.json`·공통 진행표·통합 브랜치·main은 고치지 않았다. 같은 차수 다른 결과는 조사 근거로 쓰지 않았다. 사용자 PC·현재 서비스·새 사용자 로그·계정 설정·외부 사람에게 메시지를 보내는 경로는 사용하지 않았다.

059의14파일·72행, Beirut 고정 대조값, Grafana/pandas 역사 사용자프로세스0/2를 인수했고 해당 패키지·이미지·pandas릴리스·BLS/ALFRED를 재조사하지 않았다. 이번 새 후보 파일·로더·원보고는063의 새 입력을 판별하기 위해서만 읽었다.

## 3. 실제 변경

| 파일 | 변경 사항 / 이유 | 실제 확인 |
| --- | --- | --- |
| [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/SCOPE.md), [manifest.json](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/manifest.json) | 사전 모집·순서·귀속등급·조회상한·소유범위와 의존 SHA 고정 | 시작 계약 실제 실행, 통합 및 의존 최신 조회 포함 session check |
| [frame.csv](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/frame.csv), [receipts.csv](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/receipts.csv) | 자연60행 + 후보30자리 + 결과빈자리4 =94행; 영수증37행 | 처음 적격3+3, 실제CI15와빈자리15, 원키·역할·출력분류 대조 |
| [candidate-editions.csv](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/candidate-editions.csv), [views.csv](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/views.csv) | 후보비교30행, 같은10자리×3보기30셀 | 유일판 과장 없음, 공유비용·보조분모 분리 |
| [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/RESULT.md), [cards.md](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/cards.md) | 필수두표·Q1~Q7·다른분야별도2행·양방향반례·마지막정확히3약점 | 본문표 순서·행수·출처·로컬링크·자체 및 별도 검토 |
| [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/sources.jsonl) | 직접 독해110행, 중복/부적격을보수적으로제외한51독립계보 | URL·고정판·열람UTC·읽은위치·내용·한계·Q/사례·산입표시 |
| [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/SELF_CHECK.md), [수용원장](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/acceptance-evidence.json) | 조건별분자/분모/단위/결손/재개입력, Q별반증범위와뒤집힐조건 | 원자료결손을검사성공으로바꾸지않음 |
| [evidence/](https://github.com/laadkke-arch/agentflow-open/tree/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/), [WORK_LOG.md](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/WORK_LOG.md) | 공개원기록·본문해시·로그실패·배포멤버비교·독립검토·검사이력 | 하위3조사자와root의범위·정정내역·실측비용구분 |

### 고정 커밋과 이유

| 묶음 | UTC | SHA | 이유 |
| --- | --- | --- | --- |
| ① | 2026-11-23 05:06:46Z | `0e040ae7a0c419bae15e3e380aabb89636a2f627` | 본문 전 모집·귀속 계약 |
| ② | 2026-11-23 05:30:52Z | `c50882717d94d705d7fffc914ff8b7a9b22f61db` | 프레임·원본영수증·직접독해 고정 |
| ③ | 2026-11-23 05:36:42Z | `408dae00cc48b62765eb66d9a6e732106a48543c` | 후보판·세보기·비용·반례 정규화 |
| ④ | 2026-11-23 05:39:57Z | `859c9631217c2b7a10d7ff80a52d8ba255c9975a` | 필수두표·카드·수용원장·통합검사 |
| 검증 영수증 | 2026-11-23 05:43:45Z | `86403f9082bfebe9eafefe00e673942380041761` | 실제 계약검사·고정판 재열람·최종 검토·정정 기록 |

셸 HTTPS push는 자격증명 부재로 실패해 연결된 GitHub의 tree/commit/ref 도구로 같은 허용 브랜치에 게시했다. ref는 expected SHA로 확인하며 갱신했다. 원격에 없는 로컬 임시 커밋은 결과로 세지 않았다. 고정 커밋의 파일을 다시 받아 확인했으므로 로컬에만 남은 근거로 완료를 주장하지 않는다.

## 4. 실제 검증 결과

다음 명령을 **직접 실행**했다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-063/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-063/evidence/validate.py --read-only
```

최종 검사 소스는 `86403f9082bfebe9eafefe00e673942380041761`이며 두 명령 모두 종료 코드0이었다. session status=`passed`, freshness=`remote_checked`, integration=`1e741fd0def88ef56b1060a478d81f1985a4e760`, outside_paths=[], unmerged_paths=[], errors=[]이다. 실행 구간은 `2026-11-23T05:44:25.178537+00:00`~`2026-11-23T05:44:34.741639+00:00`. 검사 전후 `git status --porcelain`은 모두 빈 문자열이었다. 통합검사 결과는 passed 44/44, failures=[]다. 이전 동일범위 검사의 원 stdout은 [session-check-bundle4.json](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/session-check-bundle4.json), [final-check.json](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/final-check.json), [validation.json](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/validation.json)에 있다. 이 인계에는 그 후 **최종 결과 SHA에서 다시 실행한 실제 결과**를 위와 같이 기록했다.

| 최종 고정 파일 | 원격 Git blob SHA = 로컬 Git blob SHA | SHA256 |
| --- | --- | --- |
| RESULT.md | `112aad4ca49075e46e5b3dac422bb3bfa9eb78d3` | `eaf8458a8e583bb9b2479ccfd97ecf59a789aa0c02b4ce5c5a2f301bfece19b1` |
| evidence/acceptance-evidence.json | `99280c7e0ce9472d182d992df23111e55269b711` | `4822ced11825893bb6b514ce852d6eac92b5cf6063ad87f5cd153b77333dc6cd` |

manifest 파일 SHA256은 `52e275ee7d1983df8523947bfa7f79994bc2005c56eb5aa078e15cf4b0dca87d`, 계약 SHA256은 `19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc`이다. 원격 고정판에서 source_rows110, independent_works51, 상태부분인계를 다시 읽었다. 두 필수표는 같은10자리·각10행이고, 최종 약점표는 정확히3행이다. 로컬 링크·CSV/JSON 구문·계보중복·표본순서·분모·소유경로를 점검했다. 이 검사는 역사 사용자 프로세스의 신원·서명이나 원 자료의 진실성 검사가 아니다.

첫 통합검사42/44에서 탈락본문의 빈case_ids와 보조라벨 판정 검사 범위를 발견했다. canonical원장에는 원프레임ID를 연결했고, 보조L라벨 두 행과 유일H판정을 구별해 수정했다. [실패와수정](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/validation-attempts.jsonl). pandas19/19 및 다른 하위 일관성검사도 각 디렉터리에 있다. 별도검토 후 A-PW1의 기간내실행1/4 초안표현은 철회했고, Berlin의 부분offset양립과 전체호출충돌을 분리했다. [검토기록](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/peer-review.json).

**미실시/미확인:** 신규 날짜변환·저자 코드·신규CI 실행, 전체제품 테스트, 역사process 신원확인, 최초이슈body독립복원, 실제로드바이트 영수증, 최신서비스 점검. 자료수집/정적독해/해시대조와 현재계약검사는 수행했지만, 현재재현으로과거실행을대체하지 않았다. 이후HANDOFF문서단독커밋을이전검사의소스에포함된것처럼표현하지않는다.

## 5. 판단·근거

### 확인 / 미확인과 분모

| 단위 | 확인 결과 | 남은 한계 |
| --- | --- | --- |
| 독립 직접독해 | 51계보 ≥20; 보고38, 공식8(버전고정7), 저장노트북2, 다른분야2+보조1 | 원장110행과독립저작수는다름; 댓글·미러·개정은중복제외 |
| 실행/결과계열 최소독해 | A-PW1/A-PW2/X-D1/X-Z1의4저작 | 저자발행결과를포함한합집합; 완전동일실행사슬0/4. X-D1은실행로그아님 |
| 자연6보고 | 추적6/6; literal날짜·offset4/6; 예외·정성포함관측6/6 | 실제사용자료판L0/6, 판+입력+출력동시0/6, H0/6. 실행시각·최초body미확인 |
| 보강4자리 | 날짜출력으로배정된사례0/4, 네빈자리보존 | 보조좋은사례로교체하지않음 |
| pandas보강원후보 | 원run15/15;13commit·8actor·68job | 날짜stdout0/15, 사용판0/15, 둘동시0/15; logs13×410+2×404, artifacts15개모두빈목록 |
| Moment보강원후보 | 조회가능원metadata관측0 | 역사전체분모미확인;0/0비율계산해당없음 |
| 별도A-M967-M | 같은REPL의Sao_Paulo입력·출력과2021e자기보고L+O-R | H와외부실행시각미확인; 자연·보강분모에합치지않음 |
| 다른분야선정2 | 월/시나리오·저자발행결과·deposit해시독해2/2 | 실제입력·실행·출판결과완전연결0/2 |

**채택 가능한 판단:** 버전표기만으로 제품에 확정된 과거 실행 사실을 붙이지 않는다. 보고주체·기록종류·증명강도를 명시한 문장을 반환한다. 공개기록에서 언제나 불가능한것도아니다. [A-M967-M 원REPL](https://github.com/moment/moment-timezone/issues/967#issuecomment-1019463236)은2021e라고자기보고한공급자의입출력을같은문맥에남겼다. 실제공식바이트사용의H증명과구별해야한다.

**반례:** 출력이정확히보고돼도판은여럿인[A-M929](https://github.com/moment/moment-timezone/issues/929), 판라벨2021a는있으나날짜출력은없는[A-M938](https://github.com/moment/moment-timezone/issues/938), 두전체pytz판의동일Berlin멤버,2020과2024의모든저장output이같은A-PW2를직접대조했다. 이자료때문에처음의‘불가능’/‘지역hash면유일’/‘새파일환경이면재실행’추정을제한했다.

자연 사례 보기 비용은28요청(성공25/실패3), 최종원문감사1회를더하면29요청(성공26/실패3)이다. 공통공식자료·CI120월질의와대체아카이브비용은따로뒀다. Moment HTML689,109B만부분실측했으며전체HTTPbyte비용은미확인이다. [비용](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/view-costs.json).

설계제안은 D/K/I/L/H와출력종류·같은run키를분리한제품문장규칙이다. 사용자가확정한새제품사양이나배포변경이아니다. 공통색인·다른작업과의통합판정은배정담당의몫이다. 공개원자료의필요사실·짧은값·해시·위치만남겼고인증정보·비공개원문을저장하지않았다. 유료서비스·새계정·원저자연락은사용하지않았다.

## 6. 다음 대화의 첫 행동

1. 브랜치HEAD와이HANDOFF를GitHub에서다시읽고, 고정결과 `86403f9082bfebe9eafefe00e673942380041761`와새변경을구별한다. 첫파일은 [수용원장](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/acceptance-evidence.json), 이어서 [첫15run의실패영수증](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/artifacts/pandas-log-attempts.json)이다.
2. 위최종검사SHA와새변경파일을비교한다. 재개검사는위두명령을사용한다. 현재검사를미래변경까지통과한것으로취급하지않는다.
3. 첫구체조사: 고정첫15 pandas run 중예를들어 `20441074943 / attempt1 / head554f9c61deef5d32dd07b6274bac9838d0f308c8`의 **당시 stdout와환경artifact**를저자의공개보관처에서찾는다. 최초공식URL은 https://api.github.com/repos/pandas-dev/pandas/actions/runs/20441074943/logs 이며이번에는410이었다. [전체입력ID](https://github.com/laadkke-arch/agentflow-open/blob/86403f9082bfebe9eafefe00e673942380041761/docs/workstreams/research/AF-RES-063/evidence/artifacts/frozen-pandas-runs.json)를바꾸지않는다. 원본이계속없으면부분인계를유지한다.
4. 새작업ID는배정담당이정한다. 입력은이결과SHA와059의고정의존SHA다. 기대결과는동일원run의입력·지역·실제공급자·판·출력이이어지는보관영수증1건또는원본불가의추가증거다. 새사용자에게로그를요구하거나현재서비스를점검할필요가없다. 추가사용자승인요청은없다.
5. 이미확인한공식로그URL을다시열필요가생기면아래명령과입력을쓸수있다. **재개용명령으로이번최종검사뒤실행하지않았다.** 과거410을같은현재성공재현으로바꾸지않는다. 이명령은URL을받아읽고상태/해시를기록할뿐저자코드를실행하지않는다.

```bash
python -B docs/workstreams/research/AF-RES-063/evidence/retrieve.py   'https://api.github.com/repos/pandas-dev/pandas/actions/runs/20441074943/logs'   'run-20441074943-attempt-1-logs.zip'
```

원자료가 다른저자보관URL에서확보되면그확인된원주소를같은retrieve의첫입력으로주고, runID/attempt/headSHA와본문입출력을조인한다. 새로실행한값은원역사출력분모에넣지않는다. 원본문최초판이없다는문제도따로유지한다.

**색인 추가 제안(담당자에게 인계, 이 작업에서는 수정 안 함):** 공통 연구색인에 `AF-RES-063 / 부분 인계 / 출력-판-동일run의독립축 / natural4/6literal·0/6판 / reinforcement0/4 / A-M967-M은L+O-R보조 / 고정SHA 86403f9082bfebe9eafefe00e673942380041761`와위필수두표링크를추가할수있다. 선행059의배포파일검증을소비자실행확인으로승격하지않는후속관계도함께표시한다.

### 가장 중요한 세 약점과 바로 다음 조사

- **원로그·최초본문·역사목록 결손** → 고정15run의당시stdout/환경artifact또는첫공개body사본을원저자공개아카이브에서찾고동일run/attempt와조인한다.
- **복수판·동일지역멤버와N-P2호출충돌** → 원셀순서·입력상태와같은run의wholepack/로드지문을확보하고, 필요하면이미읽은Volgograd두전환행을가르는보관두번째입력을대조한다.
- **발행일·고정파일·저장숫자와실제분석실행의단절** → 날짜/PID순의완전원목록및원분석log·실제read digest·셀/run키를확보해X-D1/X-Z1/A-PW2의빠진연결을검증한다.
