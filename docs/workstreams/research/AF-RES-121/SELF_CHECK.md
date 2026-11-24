# SELF_CHECK — 작업자 자체, 독립 판독 아님

| Q | source_id | 답 | 틀릴 조건 | 실제 반례 | 미확인/이유 |
|---|---|---|---|---|---|
| Q1 | D1 D2 D3 D4 D5 D1a M1 M2 M3 M4 M5 A23 | 초기 선택 및 선행 유보 | 앞선 판본 다른 선택 | R1 폐기 유보, R2 사후 분류 | Zulip/force-push/부모 전체 |
| Q2 | E1 E2 E3 E4 E5 E6 E6a E6b E6c E6d | 당시판 및 기능 | 원 registry 날짜/기능 상충 | Self/async 뒤 릴리스, EOF 없음 | exact UTC/실제 독서판/GHC 상한 |
| Q3 | A1 A2 A3 A4 A5 A6 A7 D1a I1 | 문구와 유보 분리 | 동일 코드/시험 hunk와 이유 | 선행 1/13, parent name change | push/명시 이유 |
| Q4 | A8 A9 A10 A11 A12 A13 A14 A15 I2 M3 | 1/6 정정, 반례/TODO | 승인 제약/시험과 직접 귀속 | wrapper 독립, TODO≠제약 | 실행/이전 논의 |
| Q5 | A16 A17 A18 A19 A20 A21 A30 A31 A32 T8 T10 I9 I10 I11 I4b I5 I6 | 314초, 두 단계 API 변화 | same choice #13838 원인 | use case/Traut; July checker/728 | 6/9 공개, mailing list, 728 당시판, 독서 |
| Q6 | A23 A24 A25 A26 A27 A28 A29 D4 I7 | 대조와 실행 구분 | semantic delta/귀속 | 기존 분류/용어/회의 | 원 회의/receipt |
| Q7 | T1 T2 T3 T4 T5 T6 T7 | 남는 제약/전후 승인/역할 | 전 대안 보고서+후 monitor | July after Feb, approval≠specific choice | NG dossier/2/19 원자료/monitor |

JS로 JSON 전행 parse, source_id 고유, count_unique lineage 고유, 주장 참조 및 Q별 참조 존재 검사. 변경 단위: R1 1, P4 Feb1/Sep1/Oct2, R4 package1; TODO·상태·시험 정의 별도. 외부 실행/공식 manifest 검사/독립 reviewer 없음. 고정 SHA 후 재조회 별도.
