# SELF_CHECK — AF-RES-222
상태 PARTIAL. 작업자 자체 점검, 독립 검토 미실시. 제품 구현·새 소프트웨어/API 실행·설치·자동 시험 없음.
| 질문 | 근거 | 반증/한계 |
|---|---|---|
| Q1 | U01–U06 S01–S05 | FE18 BRAKCET을 정정으로 덮지 않음; 네 code 동일; 000A placeholder |
| Q2 | U03 U05 U07 U08 U09 U12 S01 S04 I04 F01–F05 | 5.0 직전 원행 미확인; 6.0 complete-file 0행; 소비자 지원 시점 별개 |
| Q3 | U10 U11 P01–P05 | 15.1.0 vs 16.0.0, ucd_3_2_0 lookup 실패 시험 기대, 000A 역방향 실패; 런타임 미실행 |
| Q4 | I01–I07 | I06 correction only; I02 오류 상수 vs 헤더; 0xFFFF status 검사; 실제 실행 0 |
| Q5 | U01 U02 S02 S03 S04 P03 I06 | 000A placeholder/legacy/합성명; FEFF x 참조 다른 코드; annotation 동의어 금지 |
| Q6 | L01–L05 F06–F09 F18–F20 | 100/400 vs 500, n79090096 역사 전사, 동명이인 교육 사례 ≠ 실제 두 기록. PARTIAL |
| Q7 | Q1–Q6, cards.md, COUNTEREXAMPLES.md | code만의 역사 손실, 현재 alias≠과거 기능(211), 공통 부모≠child(213) |
원장 55행; 성공 35; 산입 32; 25 work_id; 10 lineage_id. UCD 10, 규격·정책 5, CPython 5, ICU 7, LOC 5; 직접 문서 하한 22 충족, LOC 실레코드 요구 미충족. U08/U09/I08 비산입. F01–F20 실패. U04 blob SHA 오기(재열람 성공 SHA 8d7222b13789c43e5ed36ddf0d3eb7ebe8d72c7b) 수정; U04/U06 6개씩 원행 재대조. 판/코드 18/18, 소비자 36/36 예상 기록(2 N/A); 6 independent Unicode 대상; 실제 0/36. 5.0/6.1 경계와 actual runtime를 혼합하지 않았다. 표 1/2는 RESULT 시작에 배치, Q1–Q7 직후, 끝 세 약점. sources.jsonl source IDs, names.csv full raw rows, history.csv, consumers.csv, cards.md 및 COUNTEREXAMPLES.md와 교차 읽음. UTC 분초 미측정. 최종 exact result SHA 재열람과 owned_path diff는 HANDOFF 직전 수행할 항목.
