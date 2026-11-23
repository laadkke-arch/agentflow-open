# 자체 검토 — AF-RES-063

상태는 **부분 인계**다. 독립 원전 최소 독해와 지정 표본의 분류는 수행했지만, 최초 본문·만료 로그·역사 전체 모집 목록과 실제 로드 영수증의 결손을 완전 수용으로 바꾸지 않는다. 소유 경로 밖 수정이나 공통 상태 변경으로 이를 해결하지 않는다.

## Q별 결론·반대 증거·뒤집힐 조건

| Q | 직접 근거와 관측 범위 | 현재 판단 | 자기 결론을 깨려고 찾은 자료·결과 | 뒤집힐 조건·아직 부족한 최소 입력 |
| --- | --- | --- | --- | --- |
| Q1 실제 출력 | 자연60본문과 선택6의 댓글·편집 경로, CI15run/job, 저자노트북2, 다른분야2. [sources](sources.jsonl), [영수증](receipts.csv) | natural literal4/6, 예외/정성 포함6/6; 기계 원 stdout0/6. 보강 실제 날짜output0/4 | 원 stdout를 찾으려고15 archive·15 artifacts·추가4job logs를 열었으나13×410/2×404, artifacts0. 노트북을 찾아 A-PW1/2의 저장output은 확인. X-Z1의24노트북은output0이라 기대를 수정 | 최초 body 사본, 해당run 원stdout/저장output과 그 공개·실행시각. Expected를 실제로 바꾸지 않음 |
| Q2 입력·순간·지역 | N-P1의EDT, N-P2의i/i2, N-P3실패vsExpected, N-M1/2 parser입력, #989초/ms, PEP495. [cards](cards.md) | 보고 단위의 값과 정확 동일 호출은 다름. N-P2 전체쌍은 내부충돌; N-M2지역과UTC미확인 | 더 정확한 UTC/지역 입력이 있는 #929도 읽어 출력과판의축을분리. #989는단위/부호가판차이처럼보이는직접반례. 원문에없는fold/gap값을만들지않음 | 원 input literal+format/unit+epoch+zone/tzinfo/fold와 출력이 같은 셀/로그에 있어야 함. 반올림 전 값이 없으면 여러 순간을 유지 |
| Q3 설치와로드 | 버전별pandas/dateutil/pytz/CPython/Moment 원전, selected show_versions, A-M938/967, CIworkflow/env. [공식](sources.jsonl), [loader](evidence/pandas/official-evidence.json) | natural0/6 자료판L,0/6 H. 공식 배포판은과거설치가아님. 같은REPL의L+O-R은가능 | dataVersion를적극찾아 A-M938의2021a만있는보고와 A-M967-M의2021e+입출력발견. 절대불가능 결론철회. 다만 원저자run에유지보수자판을붙이지않음 | 동일run의resolved module/TZPATH/PYTZ_TZDATADIR/loaded-member 또는 wholepack hash, 그리고사용된입력·출력. 라벨만이면그증명강도유지 |
| Q4 후보판식별 | 새pytz2020.1/2020.5 wheel와Berlin멤버, Moment0.5.31~34공식packed멤버, dateutil세stock소스, Volgograd두전환행. [후보30행](candidate-editions.csv) | 관측과지역hash는복수판을남길수있음. 후보열거는완전하지않아유일판미확인. N-P2 offset구성요소와전체불일치쌍을구별 | Berlin두파일2298B동일, Rome/Athens/Sao_Paulo네태그의각멤버동일. #41834는pytz/zoneinfo가현대offset같음을보고. 전체판변화가보이는Volgograd반대전환행도읽음 | 당시가능한공급자/판의완전범위+동일run전체pack 또는구별되는두번째순간. Volgograd예측은두후보만가르고실행값아님 |
| Q5 두변경사건 | 선택6의모든공개댓글, #967세참가자, #40915의2021/2025, A-PW2의2020/2024. [사건](evidence/moment/receipts.json), [notebookdiff](evidence/artifacts/notebook-second-author.json) | 같은시스템·같은입력·설치연결의전후쌍관측0. 게시일/commit일/updated_at을실행일로쓰지않음 | 2024환경메타가다르지만2020output이그대로인원본을대조. #922후속은지역/변수변화, #925는format변화. 서로다른저자/과정의성공을원시스템업그레이드로읽지않음 | 동일시스템계보의두관측, 각run로드라벨/bytes, 수신·설치·재배포영수증. 둘이면구간, 하나면그점에서의값으로만반환 |
| Q6 다른분야 | Dataverse XAMFQK V1/V2·월별XLSX, Zenodo6532252 ZIP·rawoutput·24노트북, 보조G9QZOU2008log/2023code. [독해](evidence/crossfield/READING.md) | 독립선정2저작을읽었으나완전한입력·실행·출판output연결0/2. VINTAGE문자열이나같은숫자는실제입력판아님 | 더좋은패키지G9QZOU로앞선선정을교체하지않음. V1/V2전체판은달라도U_Data같음. 노트북이있다는기대와24output0을대조. 2008실행과2023코드를분리 | 전역발행순원목록/당시저자analysis log/실제read digest와run키. 현재수신hash를원실행inputhash로쓰지않음 |
| Q7 제품문장·비용 | main10×3=30보기, 자연28요청+최종감사1, 공유공식/CI비용. [views](views.csv), [cost](evidence/view-costs.json) | main10에서판귀속상승0. 보조REPL의L승격은인정하되H미확인. 사용자/유지보수자/배포담당/감사자의허용문장을분리 | 출력확정/판복수 A-M929와판라벨있음/날짜없음 A-M938를동시에유지. 좋은보조를자연분모나보강빈자리에합치지않음 | 같은실행의추가영수증이실제로기존후보를제거할때만문장강화. 읽기횟수/bytes는실측범위만비교;전체비용미측정유지 |

## 분모·분류에 대한 반대 해석

- N-P1을 ‘경고 질문’으로 좁게 제외하는 사후 대안은 #39398/#40336/#40817이다. N-M3의 정성 관측을 제외하면 #929가 세 번째다. 본 선정을 바꾸지 않았다. 수치형 출력 비율은 이런 적격 해석에 민감하므로 일반 사용자 비율로 쓰지 않는다.
- 자연6은 원 작성자6계정이며 selected 이슈 계보6개다. 같은 이슈의 댓글·유지보수자 재현을 독립 자연사례로 늘리지 않았다. CI15run/13commit/8actor/68job도 구별한다. 보조 #967은 한 이슈 계보에 세 실행 보고가 있다는 뜻이다.
- 출처110행과 최소산입51계보는 다른 수다. 표본 본문60개 중 적격보고38개만 최소수에 산입한다. 불충분/비적격22본문과 원stdout 없는15CI메타는 원장에 남기되 최소수에서는 제외했다. 공식 원전8계보 중 고정 version/commit을 갖는7계보가 버전별 공식 원전≥4를 충족한다. PEP495 main 열람hash는 별도이며2021당시판으로 주장하지 않는다.
- 실행/결과계열 최소4는 ‘원CI/공개실행노트북/저자발행결과’라는 사용자의 합집합 기준이다. A-PW1/A-PW2/X-D1/X-Z1를 각각1저작으로 센다. X-D1은 출판된 숫자 자료이고 실행로그가 아니다. 더좁은 ‘실행흔적이있는결과’ 감도에서는 X-D1을 제외한3저작이며, 기간제한밖 원로그 A-XG9는 별도다. 최소독해 충족과 기간내 동일실행 입증은 별도다.
- A-PW1의 기간내 실제 셀 실행확정1/4라는 하위 초안 문구는 독립검토 후 철회했다. 기간내공개저작+저장output1건은 확인하지만 해당 셀 실행시각은 미확인이다. 수정판과 설명은 [독립검토](evidence/peer-review.json), [하위수용원장](evidence/artifacts/acceptance-artifacts.json)에 보존한다.

## 검사 주체·실행 범위

하위 실제 점검은 pandas19/19, Moment일관성점검, execution_artifacts일관성점검이며 각 하위 디렉터리에 결과가 있다. 원시 공개 사용자 프로세스를 재검증한 검사가 아니다. 루트는 JSON/CSV/출처/로컬링크/표순서/분모/소유경로 검사를 `evidence/validate.py`로 실제 수행해44/44를 통과했고 결과를 `evidence/validation.json`에 남겼다. 요구된 `workbench.session check ... --fetch`와 고정 결과·수용원장의 원격 재열람은 별도 `evidence/final-check.json`에 기록한다.

독립 검토자 moment_reports는 네 원저작 독해 수와 실제 실행증명의 차이를, pandas_reports는 통합 표의 pandas 주장·후보·분모를 읽기 전용으로 검토했다. 후자는 Berlin의부분offset양립과전체호출충돌을명확히하도록권고했고반영했다. 외부사람검수나모든원웹자료의독립복제라고주장하지않는다.

**미실시:** 신규 날짜변환 재실행, 저자 코드 실행, 신규CI, 원 사용자 접촉, 현재서비스점검, 059의금지된재조사, 역사process신원/서명 검증. 정적텍스트·JSON·CSV·XLSX·ZIP멤버의독해/해시대조는실제수행했다. 자료를다시받을수있는것과당시받아썼다는것을혼동하지않는다.

## 다음 첫 행동

`evidence/acceptance-evidence.json`에서 결손 조건을 먼저 읽고 `evidence/artifacts/pandas-log-attempts.json`의 첫15 run ID 중 하나를 선택해 **같은 원run**의 당시 stdout/환경artifact를 저자의 공개 보관처에서 찾는다. 보존입력이생기기전까지현재성공재현으로빈자리를채우지않는다. 원본이계속없으면부분인계결론을유지한다.
