# 처음 결론을 뒤집을 수 있는 관측과 경계

아래의 방향은 이득이 보편적이라는 해석을 검토하기 위한 것이다. 출판 집계의 유의성, 관측된 반례, 새 계산 불가를 구분했다. 원 수치의 재계산을 새 효과로 제시하지 않는다.

| ID·연구 | 직접 관측 또는 저자 보고 | 뒤집히거나 제한되는 해석 | 최소 추가 기록·판정이 바뀌는 조건 |
| --- | --- | --- | --- |
| C-01 NCQ; O-NA-01/02 | 선택380→57초와 총849→847초 중앙값이 공존(NA-001 §10.2) | 선택 이득을 총시간·노동 이득으로 복사 불가; marginal median 차를 사람별 후반시간으로 분해 불가 | person×task×period 원시 event와 최종검사; 동일 종점의 공동분포 |
| C-02 NCQ; J-NA-03 | 예약14, 성공 세션10, 진행 중 철회4(NA-004 §3) | 분석10명 전원 완료가 예약/배정 전원 완료라는 뜻 아님 | 철회 stage·조건·훈련·시행 ledger; 예약과 무작위 배정의 분모 구별 |
| C-03 NCQ; O-NA-SNIPPET1/2 | 공개 파일에 Used=0/Runs=1 및 Used=1/Runs=0 존재; CSV2 logical17/physical126–127은 후자 | 보임·열독·사용·실행·최종 정답이 같다는 해석 반증 | condition codebook, exposure/adoption 정의, 최종 산출물 검사키. snippet 자체 실행 실패를 과제 실패로 바꾸지 않음 |
| C-04 eXoaDocs; O-NA-07/08 | 전체 통과3/12 대1/12지만 Task3은3/12 대4/12; 대조 문서에도 ResultSet 수작업 예제(NA-002 TableXII) | 모든 과제의 품질 우위·순수 예제 있음/없음 비교가 아님 | 원 과제별 제출/검사/예제 노출과 TableX 시간 포함자 연결 |
| C-05 Blueprint; BC-J02 | Fig4의20명 전원 first paste, 그중 미완료3명(BC-16) | 붙여넣기 성공을 제한시간 내 정확한 완료로 대체 불가 | exact first-paste/stop/censor/grade keyed file; 그래프 위치를 품질 순위와 연결 금지 |
| C-06 Blueprint; BC-O02/04A/B | 완료자9/8시간과 전체10/10 순위 검정의 분모 다름; thesis Fig5.4 종점별 독립 정렬(BC-17 p65) | 성공자 평균과 전체 효과 혼합·그림순번 person join·비유의 chart점수=동등성 불가 | 원 사람키·정확한 quality rank와 실패자 시간 |
| C-07 CodeMend; BC-O05/06 | 부분시간 포함행 미확인, 예정60/조건 중 완료46/41; 공개 CSV361행은 질의자료(BC-23) | 분모60을 독립 사람수나 실패자 확정 수로 사용 불가; 부분시간을 전체로 대체 불가 | 실제 배정·3subtask reached/start/stop/verdict·period. 준비 notebook의 hatch와 본문shadow 차이도 실제판으로 해결 |
| C-08 Unakite; O-US-01/02 | 연구1은 interaction/total 비율; 연구2는 세 번째 정당한 설명까지. 교육·사전 표작성 비용 별도(US-01 pp8–10) | 분율 감소나 수신자 설명시간을 전체 노동·작성자 비용 절감으로 확대 불가 | 총시각·video구간·표작성/교육·코드 구현/검사 비용. 목표문턱과 전체품질 분리 |
| C-09 Strata; O-US-03/05 | 완료/진행불가 종료와 올바른 이유 개수 구별; 무효 이유는 집계표에서 생략. 표90.1%/그림91.0% 불일치(US-02/11) | 전원600초 내 완료를 전원 정확함으로 읽거나 품질 수치를 임의 선택 불가 | 이유별 gold/validity/score, omitted invalid counts, workbook공식 |
| C-10 Chan2011; O-RT-01 | far-field novelty 이득과 quantity 비용; 30분고정,1321→1066 concept 필터(RT-P01) | 창의성 이득=시간 절감·완성품 품질·사람 성공률이 아님 | person/phase/concept/coder키, 필터 이유, 실제 완성·후속 수정 관측 |
| C-11 Schwonke2009; O-RT-02/03 | E1 점수 비유의, E2훈련 변화; 저자 프로젝트의 별도 Study3은 검출된 시간 이득 없음(RT-P02/A01) | 통합효과·동등품질·모든 집단 전이 일반화 불가 | cohort별 시간·item score, margin/CI, 같은 cohort 지연검사 |
| C-12 전체 | 후보·도구 기능·훈련·순서가 함께 다름; 실제 activity/follow-up join 미확인 | 같은 링크의 설명만으로 전체 재작업이 줄었다는 제품 효과 귀속 미확인 | 동일 후보·설명 배정, adoption→test→revision, 추적기간·activity 정의 |

## 감도별 현재 계산 경계

| 감도 축 | 가능한 판정 | 미확인·다음 입력 |
| --- | --- | --- |
| 실패자 포함/성공자만 | Blueprint9/8완료자 vs10/10배정자, eXoaall-pass집계 구별 | 실패자 clock·제출·timeout·미도달 분리 부족 |
| 부분/전체 시간 | NCQ 두 종점 및 Blueprint paste/complete 구별; CodeMend는부분만 | 같은 시행 원시시각·전체종료·단계중복 정보 |
| 초보/숙련 | eXoa숙련층 배정, NCQ/도구 경험 설문 존재 | 개인별 층×시간×점수 파일 없어 새 상호작용효과 미산출 |
| 교육 포함/제외 | 알려진 교육·연습 유무/계획시간만 기록 | 실제 교육시간을 전체 과제시간에 더하지 않음 |
| 같은 링크/다른 후보 | Unakite/Strata는 공통 source/table 기반이지만 기능 묶음 다름; NCQ/Blueprint/eXoa후보·자원도다름 | 설명 하나만 변한 독립 arm 확인되지 않음 |
| 읽기/사용 | NCQ Used/Runs 불일치, Unakite 구현의highlight/save/insert구별, Blueprintpaste/미완료 반례 | 열독·이해는 event이름만으로 입증 불가; 실제노출→선택→검사 연결 |
| 후속 재작업 | 고정8군에서 해당 공개 연결비교는 관측0 | 추적 자체는 미확인; 기간0·수정0으로 대치하지 않음 |

상세 원문 주소·행은 `sources.jsonl`과 각 ID의 `outcomes.csv`에 있다. 분담의 긴 관찰 메모는 `streams/*/counterexamples.md`에 보존했다.

