# SELF_CHECK — AF-RES-183
자체점검 (독립 검토 아님). 판정: PARTIAL. 핵심 실행값 미확인. 고정 SHA 51bc163bc40fc326b768648957725b3d7ceaa215에서 7개 대표 파일 재열람, 구조·벡터 일관성 간단 확인(라이브러리 실행 아님).

| 질문 | 답과 근거 ID/원전 | 반증 탐색 및 확인 | 미충족 |
| --- | --- | --- | --- |
| Q1 | 8/8 유효, A/B/C, minor units, ④ A=0, ③ 동률 3개 허용. [I01](https://github.com/moneyphp/money/blob/b358727ea5a5cd2d7475e59c31dfc352440ae7ec/src/Money.php#L319-L358), [I10](https://github.com/dinerojs/dinero.js/blob/13965e2298c8f0aa5fbbd4b1bdcba449e2b9f8d1/src/services/helpers.js#L33-L39). | I05/I08 negative/all zero 거부, M05 credit는 별도. | 실제 입력 수용 16셀 실행 미확인. |
| Q2 | 8×2 N1/N2, [predictions](predictions.csv). [F01](https://docs.oracle.com/cd/E21766_01/fscm91pbr1/eng/psbooks/fspf/htm/fspf18.htm), F02. | ③ N2 3≠2; Oracle correction; N1/H 동일 5 사례. | 다른 반올림, 큰 수/부호 일반화 금지. |
| Q3 | [E01](https://www.census.gov/about/history/historical-censuses-and-surveys/census-programs-surveys/decennial-census/methods.html), [E02](https://www.census.gov/topics/public-sector/congressional-apportionment/about/computing.html). H 8벡터 고정 후 결과 개봉. | 최소 의석은 ③④에 부적합; E04/E05/E06 별도 제도; ③ 동률 ID순은 연구 선택. | ③ MoneyPHP 관련 동률 예제 노출; 정확 timestamp 미상; 원거리 단서는 계획 제공, 무단서/독립 blind 아님. |
| Q4 | [I01](https://github.com/moneyphp/money/blob/b358727ea5a5cd2d7475e59c31dfc352440ae7ec/src/Money.php#L319-L358), I02/I03/I05; [I06](https://github.com/dinerojs/dinero.js/blob/13965e2298c8f0aa5fbbd4b1bdcba449e2b9f8d1/src/dinero.js#L368-L414), I07–I10. | ②④⑥ MoneyPHP H와 Dinero N1 분리. M01 근접 설명 이미 최대 분수, N2도 3갈림에서 H와 동일. float/first-key tie 한계. | 16셀 code inference only; tag v1.9.1 정확 공개시각 별도 검증. |
| Q5 | [I05](https://github.com/moneyphp/money/blob/b358727ea5a5cd2d7475e59c31dfc352440ae7ec/tests/MoneyTest.php#L505) ③ 기대 [1,1,0]; [I08](https://github.com/dinerojs/dinero.js/blob/13965e2298c8f0aa5fbbd4b1bdcba449e2b9f8d1/test/unit/dinero.spec.js#L267-L289) 다른 입력. X02/X03/X09/X10 fixed SHA queries. | 기대/actual/code 세 층; PR checkbox/비례 fixture 문서 예제 중복 배제. X04 property file 검색. | exact fixture 15 미발견, actual 16 미발견, 분모 0, 적중률 미확인. |
| Q6 | [E04b](https://www.electoralcommission.org.uk/guidance-returning-officers-administering-a-scottish-parliament-election/verification-and-count/collation-regional-election-results-and-allocation-seats/equality-votes-regional-election), E03/E05/E06, [F03](https://docs.adyen.com/platforms/online-payments/split-transactions/split-refunds/), F01/F02/F04/F05, M05/M06. | ①② permutation; ⑤⑥ 수령자 증분 다름, ⑦⑧ 같음; 구성 (4→5,[5,3,1]) C 감소. min seat/추첨/환불 원거래 반례. | 실제 선거 동률 사건, 실거래 환불 로그 미확인; E06 PDF 화면 접근 실패, 본문 파싱 열람. |
| Q7 | [advice.csv](advice.csv), [RESULT](RESULT.md) 표3, M01/E01/E04b/F01/F03. | 합계만이면 외부 원리 불필요, 순서·tie 정책이면 조건부 추가, 환불/부호에 별도 링크. | 탐색기 실제 사용자 효용·회계 정책 정당성·차용 여부 미검증. |

## 수 대조
- 원장 44행, 고유 source_id 44; 보수 산입 고유 work 24, 구현 7+원시험2=9/8, 유지자 4/4, 선거 6/6, 금액 5/4. 재생 manifest R01/R02는 비산입. 서로 다른 원자료이지만 동일 구현/결정 계보는 독립 관측 아님. 명시적으로 식별한 실제 사건 6 (3 의석·2 유지보수·1 Stripe 변경 보고), 실제 금액 거래 관측 미확인; 고정 입력 실제 독립 공개 출력 0. 원장 실패/미열람/제외 상세 참조.
- frame 49행, predictions 24행, comparisons 16행, replay 8입력, advice 3행. JS 도구에서 저장 파일을 다시 파싱하여 벡터 길이, 합계 기록 일치, zero=0, N1/H 총액 보존, replay 예측/코드추론 벡터 일치, 관측 unknown 및 eligible false를 검사: 불일치 0. 이는 파일 일관성 검사이지 원 라이브러리 실행 또는 독립 검토 아님.
- N1/H 서로 다른 입력 ②④⑥; 8/8 예측 커밋 7b345f44fee54f60104539f43c37dabb5a410aa4. exact 기대 1/16, 관련 노출 1/16, actual 0/16 확인·16 미발견, eligible 0/16 (적중률 정의 불가). ③ N2 합계 위반(예측된 규칙 실패이지 제품 실패 아님).
- RESULT 처음 세 표 열 제목/표1 8, 표2 16, 표3 3; 마지막 약점 표 정확 3행. 출처 ID/URL은 ledger와 연결. 정확한 사전 열람 시각 기록 없음, UTC 날짜 오기는 RESULT에서 정정, E02 단계 표기 보정 후 재열람. 브랜치 보호 범위 검사는 최종 HANDOFF 직전 비교로 진행; 실제 코드 빌드/시험 및 workbench manifest/check 미실행.
- 재개 우선순위: exact public result search(미노출 ②④⑥), 없으면 새 통제 replay를 분리 실행. 탐색기 제품 설계 고정 금지.
