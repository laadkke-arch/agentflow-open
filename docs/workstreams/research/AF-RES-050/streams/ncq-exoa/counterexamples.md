# S01/S02 · 반례와 판정 경계

| ID | 실제 확인한 반례·갈림 | 관측 단위·근거 | 해석 한계 | 다음 최소 기록 |
| --- | --- | --- | --- | --- |
| C-NA-01 | NCQ 실험2의 최종 package 선택 중앙값380/57초와 총시간 중앙값849/847초 | 저자 집계, O-NA-01/02; [원논문 §10.2](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf) | 선택 차이는 총시간 차이를 대신하지 않는다. 두 marginal median 차이를 빼서 개인별 후처리 시간을 만들 수 없다 | 같은 사람·문제·period의 시작/선택/제출 이벤트 |
| C-NA-02 | NCQ 실험1 그래프 구성 질의와 실제 DFS 요구의 의미가 달라 후보 탐색을 어렵게 한 사례; 모든 analyzed task는 명세를 충족했어도 일부 도구 시행이 더 느림 | 저자 본문 사례, [§7.2](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf), O-NA-03 | 조건마다 다른 과제이고 baseline-first라 도구 때문인지 난도/학습 때문인지 분리 불가. 개인별 raw time 미확인 | 과제/질의/후보/period와 결과 연결 |
| C-NA-03 | NCQ 공개행의 Used?=1과 Runs?=0이 동시에 관측됨 | CSV2 논리17행/물리126–127줄, 자체 ID NA-C2-trial-label-2, [고정 CSV2](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets2.csv) | 단독 snippet 실행 실패가 최종 과제 실패는 아니다. 코드 수정/부분 사용일 수 있다. T-label이 조건을 증명하지 않는다 | Used? 코드북, 원 snippet→수정본→최종 검사 연결 |
| C-NA-04 | NCQ 공개행에 실행되는 snippet도 Used?=0으로 남음 | CSV1 논리1행/물리2줄, 자체 ID NA-C1-trial-label-1, [고정 CSV1](https://raw.githubusercontent.com/Brittany-Reid/node_code_query/ce14f193f7014c120f04619826cb251818d99b0e/data/user-study/codesnippets1.csv) | 실행 가능성과 채택이 다르다. seen/visibility 행이지 읽고 이해했다는 직접 계측은 아니다 | 가시성·dwell/독해·선택·채택 event definition과 timestamp |
| C-NA-05 | NCQ 분석10명 모두 완료와 모집14명 중 세션 철회4명이 공존 | [본논문 §10.1.2](https://brittany-reid.github.io/publication/reid-2023-ncq/reid-2023-ncq.pdf)→[별도 모집 보고서 §3](https://brittany-reid.github.io/publication/reid-2022-software/reid-2022-software.pdf), J-NA-03 | 논문의 분석 대상 설명이 허위라는 뜻이 아니다. 전체 모집자의 효과로 확대할 때 누락이 생긴다. 철회가 도구 때문인지 미확인 | 세션14명의 배정·진행단계·철회사유·측정 상태 |
| C-NA-06 | eXoaDocs의 Task3 통과3/12는 JavaDocs4/12보다 적음. 대조군에도 ResultSet 수작업 예제가 있었음 | [원논문 §5.3.2 Table XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf), O-NA-08 | 전체4과제 통과3/12 대1/12와 다른 종점이다. 방향 반전이 재현되는지 개인·숙련도 원행이 없어 판정 불가 | 독립군 배정층·Task3 검사·문서 노출 표 |
| C-NA-07 | eXoaDocs 시간은 완료자만, 점수는 조건별12명 집계. 빠른 시간과 정확한 결과가 같은 사람에게 생겼는지 모름 | [§5.2 Table X와 §5.3 Table XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf), J-NA-04 | 시간의 denominator를 pass count로 대치하거나 실패자의 시간0/40분을 넣으면 선택 편향을 감춘다 | 시간표의 포함지시자, 실제 누적/제출 시각, 오답·미제출·timeout |
| C-NA-08 | eXoaDocs 예제 사용 설문10/12 대4/12는 채택·검사 결과에 연결되지 않음 | [§5.3.3 p22](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf) | self-report와 실제 읽기/복사/최종사용은 같지 않다. 일부 예제 사용은 baseline에서도 발생 | 동일 가명의 질문응답·view·copy·final provenance·test |

## 감도별 판정

- **실패 포함/완료자만:** eXoaDocs에서 조건부 시간의 전체 배정 효과는 미확인. NCQ 철회4명 포함 효과도 미확인이다. 미관측 사람에게 임의시간을 넣지 않았다.
- **부분/전체시간:** NCQ 선택과 전체시간을 별도 행으로 유지했다. eXoaDocs는 T1/T2/T3+4 누적시간이며 연속 단계의 차분을 독립 과제 소요시간이라고 자동 해석하지 않았다.
- **초보/숙련:** eXoaDocs는 층화 배정했다는 방법만 있고 strata별 시간/점수표가 없다. NCQ 사전 설문·선별은 있으나 사람별 결과 매핑이 없다. 두 군 모두 숙련도별 효과는 미확인이다.
- **훈련 포함/제외:** NCQ video/demo와 약10분 training plan은 확인되지만 실제 각자의 훈련시간이 없다. eXoaDocs의40분은 과제 전체 cap이며 정확한 훈련/타이머 원점이 공개되지 않았다.
- **같은 링크/다른 후보:** 두 군 모두 tool/document bundle과 노출 후보가 달라진다. 설명만의 효과는 식별 불가다.
- **단기/후속 수정:** 제출 후 장기 추적 event나 activity ledger가 없으므로 재작업 감소는 미확인이다.
