# 반례와 해석 경계

| ID | 먼저 떠오를 주장 | 직접 확인한 반대 증거 | 결론의 경계 | 최소 추가 기록 |
| --- | --- | --- | --- | --- |
| BC-C01 | 첫 paste가 빨라지면 작업도 완성된다 | S03 Fig4의 미완료3명도 paste를 했다. 자체ID S03-G-A=그림순번13 Blueprint, S03-G-B=19 Control은 모두600초 내 미완료 | paste는 정답선택·정확한완료와 다르다. 각 사람의 정확초수를 추출하지 않았다 | participant×task의 paste/submission/test 원장 |
| BC-C02 | 성공자 평균346/479초가 전체20명의 시간 효과다 | S03 평균분모9/8, 원배정10/10. 전체20 completion-rank p=.14는 다른 비교 | 성공자 조건부 평균으로 실패를 제거하면 목표집단이 달라진다. 유의성 차이 자체가 효과 역전은 아니다 | timeout/중단·최종제출·실패자 품질을 포함한 공통종점 |
| BC-C03 | Blueprint의 효과는 링크에 설명을 붙인 효과다 | BC-01 p518 treatment Web browser 금지, control Firefox+Adobe Community Help; context query/preview/editor기능 차이 | 후보·접근수단·화면을 함께 바꾸어 설명만의 효과 식별 불가 | 동일후보를 고정한 설명-only 조건 또는 후보노출 로그 |
| BC-C04 | CodeMend public score와361개 query가 참가자 품질/실행 원장이다 | CSV rows2–362는 case_study_no,answer,query,query_source. eval2.py score는 model score; XLS IR rank; DB codeexamples | 단위가 질의/모델이다. query_source3범주나case5개를 participant로 join하면 잘못된 다대다 | 실제20명 lab export 및 codebook |
| BC-C05 | 각 공개 그림의 같은 순번을 붙이면 time–quality가 연결된다 | Blueprint thesis Figure5.4는 종점별 독립 정렬된 조건표식 | 정렬 위치는 개인ID가 아니다. 같은 위치를 join할 수 없다 | 공통 person ID 또는 원 plot-source table |
| BC-C06 | 평균 부분과제108.70/134.12초를 전체노동 절감으로 옮길 수 있다 | CodeMend 부분과제분석이며 시간포함정책·훈련시간·timeout·활동idle 미확인 | 누적task와 전체시간/active labor는 별도. 120예정기회는 독립120명도 아니다 | person/period/task/subtask timestamp와교육·대기·중단 |
| BC-C07 | 한 예제 중심 표시는 모든 종류의 개발을 돕는다 | Blueprint thesis printed67–69는 drag/drop처럼 여러블록·설명맥락이 필요한 학습·큰수정 과제의 한계를 논의 | 단기 구현 도구효과를 학습·장기적응·재작업 감소로 일반화 못함. 수치적 역전은 미확인 | 과제유형별 동일배정 비교와 지연전이/수정 결과 |
| BC-C08 | no-paste는 설명을 읽었으나 채택하지 않은 증거다 | Blueprint thesis printed74–78의 self-selected현장로그: handcoding/확인 가능성과 일부 platform측정누락 | 노출·열람·채택·성공은 별도. 현장세션을 독립lab 분모에 합치지 않는다 | stable session artifact diff, exposure/read and adopt markers |
| BC-C09 | 공개준비 notebook이 실험판 정답지다 | CodeMend 논문 bar세번째목표 shadow, notebook hatch; UI Google callback earlyreturn과 누락taskfile | 공개version을 실험실배포version으로 확정 못함 | 실제study commit,스크린샷/지침·정답버전 |

## 출처와 위치

- BC-C01/02/03: [Blueprint CHI 논문](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf), printed518–519/Figure4. BC-01·16; own-ID 상세는 `figure-observations.json`.
- BC-C04/06/09: [CodeMend 논문](https://cond.org/codemend.pdf), PDFpp9–10 및 [공개패키지@445d5d8](https://github.com/ronxin/codemend/tree/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d); BC-02·06–15·22·23.
- BC-C05/07/08: [Brandt dissertation](https://hci.stanford.edu/publications/2010/brandt-dissertation/brandt-dissertation.pdf), printed65(Fig5.4),67–69,74–78; BC-17. 원논문과 중복되는 연구는 독립효과나 추가배당으로 세지 않음.

실제 “더 오래 걸렸지만 정답” 또는 “설명을 읽었지만 채택하지 않음”의 개인별 joint 행은 확보하지 못했다. 반례를 찾는 데 실패한 부분도 미확인으로 남긴다. 관측된 paste→미완료만 그러한 현상을 직접 기록한 사례로 사용하며, search success→test failure로 바꾸어 표현하지 않는다.
