# 사전 규약 보충 기록

| ID·시점 | 봉인본과 변경 | 이유와 먼저 본 내용 | 영향받는 행·결론 |
| --- | --- | --- | --- |
| A01 · 통계 원본의 값 및 모든 변환 관측 전 | `30f92ecc300b0579b6aa37f2147d14ad180c4355` S2의 `trends/case-hosp-death-by-boro.csv`를 해당 발행 두 판에서의 `trends/data-by-day.csv`로 정한다. 같은 발행자의 같은 날짜·지역·필드·선정 규칙을 유지한다. | GitHub tree를 두 날짜에서 확인했다. 사전 파일명은 당대 tree에 없었다. 발행자 README의 2020-11-09 crosswalk가 `boroughs-case-hosp-death.csv` → `trends/data-by-day.csv`를 지목한다. 3/20·3/24 commit 목록과 path·blob SHA·크기만 새로 봤다. | S1-1~S4-2와 S 교란·판 감도 행의 발행 주소만 수정된다. 사전 판정·분모·합·결측·반올림과 예상 변화는 동일하다. |
