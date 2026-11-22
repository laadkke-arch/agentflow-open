# AF-RES-030 자체 점검과 반증

판정 상태는 **REVIEW_READY_WITH_GAPS**다. 요구한 A24/B8·직접 열람 최소수·원장·필수표는 갖췄지만, 최초본문 전체를 복원하지 못했고 일부 필드별 보강은 후속 판독 뒤 작성했다. 공개 대화의 현재 관측을 원판 전체·실제 사용자 환경의 재실행·단일 질문의 인과효과로 넓히지 않았다. 원판 실패와 시점 한계는 수용 원장에 `met=false`로 남긴다. 조건부 분모0은 해당 없음으로 기록한다.

## Q별 주장·반증 원장

| Q·주장 | 근거 주소·위치 또는 탐색 실패 영수증 | 자기 결론을 뒤집을 조건 | 실제 반증을 찾은 경로와 결과 | 남은 미확인 |
| --- | --- | --- | --- | --- |
| Q1. A는 고정2분기×3원장×최초4건이며 결말을 선정키로 사용하지 않았다. 목적·작성자는 root에 연결했다. | `SCOPE.md`, `frame.csv`670행, `initial.jsonl`의 A24, `evidence/t0-summary.json`; [M01 root](https://github.com/matplotlib/matplotlib/issues/24865)에서 [D08 root](https://github.com/duckdb/duckdb/issues/12804)까지 원장별 URL | 앞선 적격 root가 빠졌거나 봇/중복/순수설치 요청을 사용·설계 요청으로 오분류한 증거 | 생성순 query 전체 metadata와 선두 root의 제외 이유를 다시 대조. X02는 test 맥락이지만 실제 S3/Zarr API 사용 목적, X07/X08은 유지관리자의 설계 요청이라는 경계를 독립 검토. `INDEPENDENT_REVIEW.md`에 다른 분류 민감도를 보존 | 공개 handle의 실제 독립 사람 여부, 미표시 삭제 root. 첫 재개: 각 quarter의 원 API query receipt와 앞선 root 본문 |
| Q2. 최초본문 전체 O0/32. 현재값을 최초값으로 대치하지 않았다. | `initial.jsonl` original_grade/limit, Matplotlib `evidence/edit-history-attempts.json`, xarray `edit-history-attempts.json`, DuckDB `evidence/edit-and-attachment-attempts.json`; [DB04 rename](https://github.com/duckdb/duckdb/issues/6943#event-8932902142) | 원 알림/공개 revision에서 실제 물은 값의 질문 전 존재가 확정되면 중복/정보량 분류가 달라짐 | 편집 endpoints·HTML의 lastEditedAt/bodyVersion·첫 답 인용·첨부버전을 읽음. [XB08](https://github.com/pydata/xarray/issues/7730#issuecomment-1499263329)의 버전표 후발추가, DB04 제목 후발변경이 실제 반례. M01/DB07의 현재중복을 확정중복0으로 낮춤 | 원판 전체, 미표시 삭제. xarray13 필드별 audit는 봉인 cache와hash일치하지만 후속 뒤 작성. 첫 재개: M01 최초 알림/공개 revision |
| Q3. 첫 broad질문8·첫 정보질문7·전체 root30정보질문8은 다른 집합이다. | 봉인 `questions.csv`, `ANALYSIS_RULES.md`, [M03 fit](https://github.com/matplotlib/matplotlib/issues/24872#issuecomment-1369957180), [X02 후발 질문](https://github.com/pydata/xarray/issues/7408#issuecomment-1369974685) | M03을 기존 환경 정보요청으로 읽거나 X07의 역할을 일반 지원과 같다고 볼 분명한 원문 근거 | 수사적 링크 질문 X03, action request D02/XB13, 역방향 X07, 새 설계 X05/X08을 원문과 대조. 실제 문장과 질문 대상·변수·종류를 question-audit에 분리. M03은 첫질문표에 남기고 strict분모만 제외 | X02 traceback 문구가 질문 처음부터 있었는지 미확인. 첫 재개: 해당 댓글 최초 revision |
| Q4. B는 상한80에서 첫 질문 기준14개 중 최초8개이며 A를 보충하지 않는다. | `evidence/b-selection.csv`, `initial.jsonl` B80, 각 stream screening-followups; `evidence/source-counts.json`의 B8/B72 | 첫 답에 직접 정보요청이 없거나 답/성공을 보고 채운 선정이 발견됨 | M의 후보평가/PR요청과 D의 patch요청을 정보질문에서 제외한 영수증 대조. XB06의16개월 뒤 첫 질문도 성공 여부를 보고 빼지 않고 B8에 유지 | 질문 첫판의 일부 편집. XB06 root30/90질문 없음은 관측된 결과이며 결측 아님. 첫 재개: XB06 최초 응답 revision |
| Q5. 엄격 기존값 직접답은 A3/B6사례, A3/B7왕복이다. 무직접답을 무응답과 구별했다. | `chains.jsonl`, `question-audit.csv`, `wait-audit.csv`; [XB13 actual local](https://github.com/pydata/xarray/issues/7754#issuecomment-1509390748), [XB14 재표현 답](https://github.com/pydata/xarray/issues/7758#issuecomment-1509899467) | 작성자·변수·대상·판 불일치, 새 실행 답을 기존값 회수로 합친 사례가 확인됨 | X04는 새 제안 실행 답, M08은 단일toolkit조건 미충족, X02는 값없는 약속, D05는 지원자추정, MB09는 새환경행동으로 분리. XB13 뒤 다른파일 성공과 XB14두변수/두왕복을 재독 | 답 편집으로 값의 실제 공개시각이 생성/수정 사이. XB03 후발 선호는 답문장 존재와 기존 선호 여부가 다름. 첫 재개: 해당 답 revision 또는 동일파일 로그 |
| Q6. 엄격 기존권고 변경은 A0/3·B0/6이며 설명 수정·첫 제안을 별도로 인정한다. | [D02 전후](https://github.com/duckdb/duckdb/issues/5818#issuecomment-1374567686), [M01 재현](https://github.com/matplotlib/matplotlib/issues/24865#issuecomment-1368556640), [X04 후 설명](https://github.com/pydata/xarray/issues/7411#issuecomment-1375736147); `ADJUDICATIONS.md` | 답 전 같은 지원자의 구체 후보가 있고, 바로 그 변수값 때문에 다른 후보/사용/다음 행동을 택했다는 원문이 발견됨 | D02를 초기에 변경으로 넓게 읽을 위험을 root가 재독해 no_prior_proposal로 정정. MB07 양성경로를 찾아 여러 매개가 있음을 확인. 공급자 PR/시험·감사·close를 사용자 실행으로 세지 않음 | 한 변수와 자발적 추가논거의 기여, 요청자 실제 실행의 전체목표. 첫 재개: D02 지원자의 명시 결정기록, X04 metadata 검증 |
| Q7. 사전5짝/미성립3을 유지하고 질문없는 실행·중복질문·미답·후발요구를 적극 찾았다. | `comparisons.csv` 봉인, `comparison-results.csv`, [M04 실행](https://github.com/matplotlib/matplotlib/issues/24874#issuecomment-1370981028), [MB21 재질문](https://github.com/matplotlib/matplotlib/issues/25673#issuecomment-1506278627) | 동일한 입력·목표·정보량·지원자 조건의 대조가 생기거나 누락된 실행이 드러남 | D05대조는 성공한D08로 바꾸지 않고 D07을 유지. M07/D05무응답, MB21확정중복, X04같은후보설명변화, MB07후발목적 후 진행, XB25무질문실행을 B80감사와 원문재독에서 확보 | 클릭/읽기/대신할 노동·순증 대기는 독립 로그 없음. 첫 재개: 동일목표의 실제 안내-실행 로그와 해당 시각 자료 |
| Q8. 질문 입력 규칙은 후보 설계이며 검증된 효과 정책이 아니다. 양끝·역할·노출·반복발신자 제외를 분리했다. | `DESIGN_RULES.md` DR01–DR10, `sensitivity.csv`, `ADJUDICATIONS.md`; [NHIS 두 방향 답변화](https://wwwn.cdc.gov/QBank/report/Wilmot_2023_NCHS_NHIS1.pdf) p9–10/17–18, [BLS1999](https://www.bls.gov/osmr/research-papers/1999/pdf/st990270.pdf) 방법/결과 | 설계 예시를 실제 발송·실행한 것으로 오인하거나, 명료화가 정확도를 높인 통제자료를 무시하는 결론이 나오면 철회 | 도서관 실제대화/평가절차와 공공통계 실제관측/프로토콜8원문을 읽음. No→Yes가 범위이해 개선인 장면과 잘못된 포함인 장면 모두 보존; 가상 training예시를 실제발화로 세지 않음. 원작성자·유지관리자·미래노출 제외 후 strict0 유지 | 서로 다른 분야의 과제를 GitHub효과로 전이할 근거 없음. 원판O0분모는 해당없음. 첫 재개: 단일변수의 전후 구체권고가 있는 공개 새 표집 |

## 재집계와 판독의 구분

| 검토 | 실제로 한 일 | 독립성/한계 |
| --- | --- | --- |
| 각 stream 자체 검사 | 사례·시간창·첫질문·직접답·실행·pagination·봉인 hash검사. 실패와수정 영수증을 보존 | 같은 작성자의 재검. Matplotlib/DuckDB CRLF 비교 및 검사스크립트 실패, xarray 영수증 스크립트 구문오류를 숨기지 않음 |
| root 정규화/재계산 | 원시 판독 배열에서 사례/변수/episode/왕복/대기·분모·민감도 산출 | 원장판정을 아는 상태; 직접값을 새로 독립 코딩한 것 아님 |
| root 원문 재독 | 핵심 질문·답·실행/보류 스레드20개, 고정판 공식자료8개. GitHub connector 원격읽기 영수증과 실제셸검사를 분리 | 별도 판독이지만 결과를 아는 상태; 전수 맹검 아님 |
| DuckDB 담당 교차감사 | M/X와전체 배열·시각을 별도Python으로32사례 재계산, 선택 공개댓글13개 재독. 자기DuckDB는 자체재검 | 기대값을 전달받은 눈가림 없는 검사. 모든46개 원문을 독립 재독한 것 아님. `INDEPENDENT_REVIEW.md` |
| Matplotlib 담당 원고검토 | 필수표32행, case URL, 성공범위, 201/46자료수, 마지막3행 등10조건 검토 | 중대한 수치오류0; 첫M03단계라벨/왕복범위/addfont범위/온라인참고상담 표현4건 정리. `evidence/result-review.json` 및 resolution |
| source compiler | canonical원문/동일문서군/판보강/후속/검색실패 분리, 이전UTC미기록20root를 직접 재독 | source집계가 추가 독립 원문 독자를 만들어내지 않음. 최신201UTC 확보, 과거T0 null보존 |

원장 직접 집계: A정보질문8→같은변수답3→엄격변경0→완전실행사슬0. B는선정8→root30질문7→직접답6→엄격변경0→완전사슬0. 정보질문 관련 작성자 반응 왕복은 A6/B9, 엄격직접답 왕복은 A3/B7이다. A질문발화8/변수9 중 traceback1은 최초시점미확인, B발화10/episode9/변수11이다. 새 한정실행은 A성공4·실패1, B성공1·실패1. 전체목표 성공은 A2/B1. root90에서 이 분자는 바뀌지 않는다.

출처원장은201 canonical기록, 필수적격46, 정확36 witness다. 공식 자료40중 필수14, 외부8, A24이며 B8와비선정72는 최소수에 보태지 않는다. 25 frame-only추가root·28제외root·21상한뒤root·337기록열람·448댓글locator·32사건은 서로 다른 단위다. core46에 frame-only나실패·검색요약을 넣지 않는다. 동일 사건의 자료 수는 `evidence/source-counts.json`의 `same_event_source_counts`와 `linked_source_counts_by_case`에 있다.

텍스트 입력 해시는 Git의 LF정규화로 비교한다. CSV 작업트리 CRLF를 의미 있는 판정변경으로 오인하지 않는다. `build_sources.py`의 입력hash도 LF정규화로 고쳐 새 checkout에서 재현되게 했으며, source201/최소46과 sources 본문hash는 변하지 않았다. frozen134개 파일의 판정 내용은 후발 수정하지 않았다.

## 실제 검사 기록과 미실시

최종 판단은 다음 영수증의 **대상 HEAD, 입력hash, 명령, 종료코드**로 확인한다. `evidence/validation.json`은 결과 작성 작업트리의 실제검사이고, 최종 결과 원격SHA를 다시 읽은 검사는 인계 commit에 `evidence/final-validation.json`과 `evidence/final-session-check.json`으로 남긴다. 원격 fetch_file은 원격 재독이며 셸 실행으로 표시하지 않는다.

- `verify.py`: 표본·봉인·소유경로·시각·왕복·source 최소수·필수표·마지막3행·분모를 검사한다.
- `workbench.session check manifest.json --fetch`: 통합과의 계약/범위/의존 SHA 및 최신 원격 상태를 검사한다. 원 manifest를 조용히 다시 고정하지 않는다.
- 제품 전체 회귀 suite/cloud_check·과거 GUI/사용자 실데이터 실행은 미실시. 제품코드를 변경하지 않았으며 이 결과는 공개대화 조사다. 필요한 고정판·입력·명령·없어서 실행할 수 없는 자료는 `PENDING_EXECUTIONS.md`에 명시했다.

원판 전체복원·전수 최초필드 맹검·사용자 환경의 독립 재실행이 충족됐다고 쓸 수 없으므로 수용 상태는 gaps로 유지한다. 반사실적 전략 효과를 공개 대화에서 추정하지 않는 것은 의도한 범위 경계이며, 양성건수를 늘리기 위한 후발 재표집을 하지 않는다.

root 첫 통합검사 `validation-first.json`은95/99 exit1이었다. 검사기가 B_screen 원장을 B밖으로 제외하고 분기 접두사 A를 통일하지 못한 것이 원인이다. 원자료·선정·판정을 바꾸지 않고 검사기만 정정한 뒤 `validation.json`99/99 exit0을 확인했다. session check --fetch도 실제 exit0이며 최신통합f1d420df41493b87be70d5362310003831074e15의 계약변경 없음이 확인됐다.
