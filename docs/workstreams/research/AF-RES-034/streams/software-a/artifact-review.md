# 별도 원산출물 8개 산입 재검

검토자: SW-A 조사 에이전트. 확인 UTC: 2026-11-22T16:07:27Z. 주 작성자가 만든 산입표를 받아 별도 에이전트가 실제 내용과 모 논문의 연결을 재검했다. 이는 사람 두 명의 독립 코딩, 맹검 판독, 원 실험 재실행이 아니다. 산입을 위해 선정 규칙을 바꾸지 않았으며, `SCOPE.md` §3의 독립 내용 원산출물 기준과 `initial-selection.json`의 task/protocol/rubric/data/codebook 기준을 적용했다.

## 판정

**최소 8개라는 공개 독립 원산출물 수 조건은 제한된 의미에서 `met=true`로 기록할 수 있다.** 원저자가 별도로 공개한 과제 준비 notebook 2개, 서로 다른 내용의 자료집 3개, 원 분석/채점 절차 2개, 도구 조작 지시문 1개를 직접 읽었다. 동일 원자료의 재포맷이나 논문 쪽 분할은 없다. 각각 원래 연구군에 연결되므로 새 연구군 8개로 세지 않는다.

다만 이를 “정확한 실험 제공판 프로토콜 8개”, “사람 시간 원자료 8개”, “8개 연구의 독립 재현 자료”로 표현하면 **`met=false`**다. 두 연구군(CodeMend와 NCQ)에 집중된 8개이며, 그중 CodeMend 3개는 사람의 질의 수집과 IR 채점에 관한 자료다. 이 3개는 20명 lab 실험의 시간·완료율을 재계산하는 입력이 아니다. 이번 8개 가운데 사람별 시작·종료·중단을 함께 담은 공개 시간 자료는 **0개**다. 파일 수 충족이 제품의 링크 단독 효과나 장기 재작업 절감의 증거 강도를 올리지 않는다.

정확한 배포판을 입증해야만 산입한다는 조건은 봉인된 SCOPE에 없었다. 따라서 배포판 불확실성을 숨기지 않고 원산출물 수와 프로토콜 동일성을 별도 수용 항목으로 유지하는 것이 일관적이다. 가장 약한 1개는 NCQ 일반 조작 지시문이며, 이를 실험 전용 지시문으로 한정해 제외하면 엄격한 하위집합은 **7개**다. 최종 인계는 이 민감도와 이유를 함께 표시해야 한다.

## 실제 내용·독립성·제한

| 원장 ID·고정 원문 | 직접 재검한 내용 | 독립 내용의 산입 이유 | 한계와 허용하지 않는 주장 |
| --- | --- | --- | --- |
| Rt-A01 · [CodeMend lab 준비 notebook](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/user-study-prepare-0405.ipynb) | cells 0–15의 모든 source. 연습 line 변경, bar grid·45도 x-label·hatch, pie title bbox·색·90도 회전의 누적 목표 코드. | 저자의 독립 과제 준비물 1개. 논문 설명보다 구체적인 초기 코드와 목표 조작을 포함한다. cell이나 그림마다 나눠 세지 않는다. | 논문 lab 절은 bar 최종 조작을 shadow라고 하나 이 준비본은 hatch다. 따라서 정확한 참가자 제공판 동일성 미확인. 실험 코드 실행·시간 재현을 뜻하지 않는다. |
| Rt-A02 · [CodeMend crowd 자극 notebook](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/mturk_data_prepare_0302.ipynb) | cells 0–44의 모든 source. 5종 그래프마다 Before/After-1/After-2, 별도의 boxplot 지시용 예시. | lab notebook과 다른 목적·초기 코드·변경 내용의 원 자극 준비물 1개. | notebook은 10개 후보 변경쌍을 만들지만 논문 Query Collection은 5개 쌍을 보고한다. 실제 사용한 After 판은 미확인. 10개 자극이 모두 실험에 제시됐다고 쓰면 안 된다. 50명 crowd 질의 수집 자료이며 20명 lab 노동 측정 자료가 아니다. |
| Rt-A03 · [CodeMend 선별 질의/정답 CSV](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/eval-gt-2.csv) | header 및 전체 361행 기계 재계수, 각 case 첫/끝 질의·정답 직접 판독. case 수 67/64/84/72/74, query_source 수 115/211/35. | 자극 생성 코드가 아닌 실제 선별 질의와 정답의 자료집 1개. 사람의 언어 입력과 API 정답 매핑을 추가한다. | 361은 사람 수가 아니다. 논문 883개 중 제외한 522개 질의와 제외 판정 기록은 없다. participant ID·시간·미완료 필드가 없다. |
| Rt-A04 · [CodeMend eval2.py](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/eval2.py) | 전체 260행 이내 파일 판독. 질의 CSV 입력, 정답 후보 중 최고 순위, 불일치 0, MRR/top-k hit를 전체 질의 수로 나누는 규칙과 로그 필드. | CSV에 없는 채점·분모 규칙을 담은 원 분석 절차 1개. 다른 형식의 동일 데이터가 아니다. | 사람의 완료 품질 rubric이 아닌 IR 채점 코드다. 코드 명칭 P@k와 논문 R@k 차이를 구현 기준으로 설명해야 한다. 모델·backup 의존 자료를 갖춰 실행한 적은 없다. |
| Swb-A01 · [NCQ 조작 지시문](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/docs/instructions.md) | 고정 SHA GitHub API로 전체 직접 열람. install/uninstall/editor/save, package 검색 25개 단위, samples 삽입·순환과 keybinding. blob SHA `975726e152951f9d56e608bf93fb46a75c99f65d`. | 저자가 만든 독립 조작 지시문 1개. 모 논문 §7.1.5는 참가자에게 화면 오른쪽에 keys/commands 문서를 제공했다고 명시한다. 개입에 결합된 검색·삽입·실행 조건을 확인할 수 있다. | 정확히 이 커밋의 파일이 제공됐는지는 미확인. 실험 전용 task brief 또는 동의·배정 protocol이라고 이름 붙이지 않는다. 이것이 8번째 산입의 가장 약한 연결이다. |
| Swb-A02 · [NCQ study1 CSV](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets1.csv) | 전체 142행 기계 재계수, header 및 앞·뒤 사례 판독. P1–P10, T1/T2; Used 1=41, 0=100, 빈 placeholder=1. | 저자가 study1 관측으로 별도 공개한 실제 snippet 노출·사용·오류 기록 1개. | 행은 코드 조각이다. 사람 시간·군 이름·최종 정답·완전한 성공적 재사용 필드는 없다. 빈 placeholder를 실제 snippet이나 사람 실패로 세면 안 된다. |
| Swb-A03 · [NCQ study2 CSV](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) | 전체 156행 기계 재계수, header 및 앞·뒤 사례 판독. P1–P10, T1/T2; Used 1=38, 0=118. | 원저자 script가 명시한 다른 연구 코호트의 별도 기록 1개. 분석자가 한 데이터 파일을 나눠 늘린 것이 아니다. | 앞 파일과 참가자 번호가 재사용된다. study ID 없이 P번호만 조인하면 다른 사람을 같은 사람으로 만든다. 두 파일의 같은 스키마는 동일 관측임을 뜻하지 않는다. |
| Swb-A04 · [NCQ snippet 분석 script](https://github.com/Brittany-Reid/node_code_query/blob/ce14f193f7014c120f04619826cb251818d99b0e/data/scripts/user-study-snippets.js) | 고정 SHA GitHub API로 전체 직접 열람. 두 CSV와 study1/2 대응 주석, 4번째 열에 lint를 적용해 errors.length를 출력하는 절차, 첫 파일만 실행하는 main. blob SHA `b0a9f7ebfa8937f75cd0bd1550235da226914744`. | CSV의 관측 내용과 별개로 평가 실행 규칙·코호트 대응을 설명하는 원 분석 코드북 1개. | ESLint wrapper와 당시 버전까지 재현한 것은 아니다. runtime 오류, 사람 최종 과제 정답, 작업 시간 판정 코드는 아니다. 결과를 Google sheet에 옮겼다는 주석이 있어 이 파일만으로 논문 Figure28의 모든 집계를 재현했다고 주장할 수 없다. |

## 논문과의 연결을 추가 확인한 범위

[CodeMend 원문](https://cond.org/codemend.pdf)의 `Search Task Evaluation / Query Collection / Results / Lab User Study`를 로컬 원문 추출본에서 읽었다. Query Collection은 50명, 883개 중 361개 선별, 5개 plot 쌍을 보고한다. Lab은 20명, 개인별 두 과제와 균형화, 완료 subtask 46 대 41, 완료 subtask 평균 108.70 대 134.12초를 보고한다. 두 실험은 사람과 분모·결과가 다르므로 CSV의 361행을 lab 결과와 연결하지 않는다. 원장 Rt-S02의 고정 저자본과 연결된 로컬 원문이다.

[NCQ 원문](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf)은 원장 Swb-P07과 연결된 `software-b/tmp/ncq.txt`의 §7.1.1–7.1.5, §10.1, §10.4를 직접 재검했다. §7.1.5에 제공된 조작 문서와 화면 녹화·timestamped tool logs가 명시되어 있다. §10.4는 seen/attempted/successful을 구분하고, 브라우저에서 일부만 본 snippet을 제외한다고 설명한다. 두 CSV는 시간 log와 동일한 자료가 아니며, snippet 단위 오류율을 사람 단위 실패율이나 최종 산출물 품질로 대체할 수 없다. 원문 소재와 고정 주소는 Swb-NCQ 연구군의 모 논문 행을 따른다.

## 검토 영수증과 재검 범위

원본 다운로드를 저장한 조사 갈래의 파일을 읽고 아래 SHA-256을 재계산했다. 이는 통합 작성자의 파일 요약을 그대로 승인한 것이 아니라, 공개 고정판과 연결된 실제 바이트·내용을 읽은 교차 재검이다. 각 CSV 전체 행은 기계 검사하고 일부 내용을 사람이 아닌 에이전트가 판독했다. 모든 데이터 행의 독립 수동 코딩이라고 표현하지 않는다.

| 파일 | SHA-256 재확인 | 판독·검사 범위 |
| --- | --- | --- |
| CodeMend eval-gt-2.csv | `6b390e59111be1a7a1e2c88910fe85bac2160368286ff34d11a200456ad7bf5d` | 전체 361행 계수·case/source 분포, 각 case 첫·끝 질의 |
| NCQ codesnippets1.csv | `6818f6aa7de3433db538d22affe6efe9a9c44764be23afc57bca7c418c3680f5` | cp1252로 전체 142행·Used 분포·P/T 집합, 앞·뒤 내용 |
| NCQ codesnippets2.csv | `9d3438d6a54c8a9e083f9e1a8d28fb07104b9580d79df265d1aded3607b16710` | cp1252로 전체 156행·Used 분포·P/T 집합, 앞·뒤 내용 |

직접 읽은 출처 8개는 이미 통합 대상 sources에 존재하므로 SW-A sources에 다시 더하지 않았다. 이 검토 문서 자체도 외부 원산출물 수에 포함하지 않는다. notebook과 scoring script는 정적 열람만 했으며, Python 2·Matplotlib·모델 설치나 Node 패키지 설치를 통한 실행은 하지 않았다.

## 수용 파일과 HANDOFF에 권하는 문장

> 원저자의 독립 공개 원산출물 8개를 읽었다(과제/자극 준비 2, 자료집 3, 분석 절차 2, 조작 지시문 1; 2개 연구군). 그중 CodeMend IR 자료 3개는 lab 시간의 원자료가 아니다. NCQ 지시문의 정확한 실험 제공판과 CodeMend 준비본의 일부 자극 판은 미확인이다. 조작 지시문을 실험 전용 자료로만 제한해 제외하면 7개이며, 어느 경우에도 사람별 시간·미완료를 재계산할 공개 원자료 8개를 확보한 것은 아니다.

다음 최소 확인은 원문 수를 늘리는 일반 검색이 아니다. CodeMend 준비본의 bar shadow/hatch 및 crowd After-1/After-2 중 실제 제공판을 특정하는 보존 배포물 또는 실험 실행 기록을 찾고, NCQ `docs/instructions.md`의 실험 배포판과 timestamped input log의 공개 여부를 해당 저장소의 고정 commit tree·release history에서 확인해야 한다. 참여자 모집·연락은 이번 범위 밖이다.
