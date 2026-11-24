# SELF_CHECK — AF-RES-234

자체 점검, 독립 검토 아님. 상태 PARTIAL. 작업 전 SCOPE 봉인 46dd18370b65172743d2106009e5bedf304418b5, 자료 ② e0ea76fb6b88bb5b19ad9ab2014a1b7adacfd602, 표 ③ fe729dd86deea53acc4b922494acbd161bd3e68b, 반례 ④ 17350c798ad6b4b7f4f29235ea37ac64ee48b562. ⑤ 결과 commit 뒤 고정판 파일 목록·원근거 ID·표·범위를 다시 대조하여 HANDOFF에 결과를 남긴다.

| 질문 | 원문 근거 및 직접 확인 | 반증/경계 | 판정 |
|---|---|---|---|
| Q1 | M01,C02,P01–P04,P06,P07,C04,C08,C10 | 첫 경로 Debug는 2개 layer만; 공식 P full JSON F01/F02 미획득. OSM M07은 후순위 | PARTIAL |
| Q2 | M02–M06,M07–M09,M13–M14,P01–P03,D02,S04,S05 | TileJSON rank 미표기인데 M09 실제 rank 있음; maxzoom vs overzoom; PMTiles header 결측 | PARTIAL |
| Q3 | M07,M09–M11,M15,P08–P11,S02,S06,S08,S09,C05 | school_11 및 arrow 실재, 같은 index 다른 atlas bytes; missing key 0, runtime addImage 가능; DPR2·crop 미실행 | 정적 연결 완료(대조군), strict PARTIAL |
| Q4 | M07,M09,M12,P02–P05,P12–P15,D03–D04,S01,S03,S07,S10,C08–C10 | Inn 실제 문자열 일부; 12 합성; 두 PBF 같은 이름 다른 bytes; runtime local fallback 및 언어 분기 | 정적 연결, 실제 glyph 요청 미관측 |
| Q5 | M01–M06,C02–C06,C08–C10,D02 | local example CDN 포함, Athens expected는 실행 아님; 실제 배포판/영수증 결측 | PARTIAL |
| Q6 | E01–E08, F05 | font name와 manifest/CSS/file 구별; Children's Literature 시스템 폰트 후보, 실제 reader 선택 미관측 | 정적 선례/반례 확보 |
| Q7 | M01,M08,M15,P08,S01–S10,C05,C06 | 4 통제 정적 근거, 한 조건 변경 실제 실행 0; strict P 범위 미확인 | PARTIAL |

분모: 70 ledger rows, 7 실패 제외, 산입 고유 work_id 45(제작자25 / 규격6 / 소비자9 / EPUB5), lineage 15. 실패 응답, 동일 저작 절·같은 sprite pair/변형은 추가 산입하지 않음. 6 구별 사례(Debug, OSM Bright, P generator, Athens fixture, Accessible EPUB 3, Children's Literature); 서로 겹치는 계보가 있으므로 독립 실험 수는 0. strict 6 slots, 0 adopted / M confirmed vacant 3 / P full artifact missing 3; P projection 3은 채택 아님. OSM 대조군 3 static links; World 보조 3자리(아이콘 공석), strict 분모 밖. C1–C4 static-supported 4, executed 0, execution-missing 4. Icon source/actual index/PNG link in contrast, P candidate literal arrow with assets; actual feature P missing. Text feature→PBF on OSM (I,n present); P synthetic digits→PBF, real addr feature missing. Screenshot original expected C09 one; new screenshot 0; offline receipt 0. EPUB embedded file present vs system name only; reader font selection 0. Sources first-open timestamp not reconstructable; window noted; Git commit dates are not per-file initial publication date. No renderer, package installation, test suite execution, independent reviewer, or new deployment. Static PBF parsed directly from fixed blob, not SDK/browser test. No fabricated feature values for P. Actual published site date unknown except evidenced release/docs; accessibility of current source does not prove past deployment.

점검 대상: RESULT 첫 두 표 열 이름과 6/4 행 단위, Q1–Q7, 마지막 약점 3행, layers.csv 12 data rows, resources.csv 21, bundles.csv 33, examples.md; exact SHA remote reread required before HANDOFF. Core missing prevents DONE irrespective of 22-work threshold. Next worker must prioritize P full JSON export and matched archive/feature, then run controlled render tests and record receipts. 
