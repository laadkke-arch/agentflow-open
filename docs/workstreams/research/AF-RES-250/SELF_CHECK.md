# SELF_CHECK — AF-RES-250 (자체 점검)

## 분모/완료 판정

- 예상 6 고정 묶음 → 6/6 좁은 주장 원문 연결, 미연결 0. 직접 사례 원산출물 19: 230=2, 233=5, 234=6, 235=2, 236=2, 237=2. 6개 사건/관측 단위는 서로 다른 분야의 목적 표본이며 6 독립 실험이 아님. 선행 central DONE 6/6, 자체 PARTIAL 6/6을 그대로 표기. 238–242 결과/입력/정답 없음.
- 원장 72행, 72 고유 source_id, 산입 38 unique work_id, 23 lineage_id(산입행 기준), 그룹 19/10/5/4 vs 하한 8/6/4/4(표준 S01 Note 제외 시에도 4 Recommendations), 각 사례 최소 1 충족. 산입 제외 34행(19 내부, 7 실패/역사 alias 미복구 등, 나머지 지침·동일 저작 판/설명/재전재). 출처별 최초 시각 미재구성 → 공통 확인 UTC 시간창 표시, 공개일 미확인은 version/날짜란에 unknown 표시. 읽은 원문의 판/섹션/관측값 및 한계를 기록. 내부 원표는 외부 38에 포함하지 않음. 실제 서로 다른 결정 계보/연구 계보 숫자는 원저작 개수와 별개.
- pair 15/15 unique; complement10 independent5 hard-dependency0 contradiction0(이 표본에서 관측된 것만). directions A↔B no directed need 및 각 방향 삭제 효과. source IDs 공통 경험 원천 없음. 사례 내부 raw evidence dependencies 보존. 
- leave-one-out 12/12 (L6/X6), 각 5 retained; 재개1 local decision + joint generalization hold; 복구 추가 읽기 합 L5/X12 계획. 모델 실험/실제 시간 측정 0(범위 밖), 독립 사용자 평가 0(미실시). 코드/원자료 static parse 일부 수행(C04/C05), 실제 PCM, GUI render, 제품/도구 실행 0(미실시). W-I normal vacancy 8 layers 중 icon-image 0; index/feature 공석(정상), 다른 3 strict vacancy / 3 strict missing은 선행 범위. F01 post-review 0은 관측값, reviewer/acceptance unknown. B physical title page·raw MARC 미확인, E historical stable bytes/actual click or choice 미확인, A output/build 미확인. no observed ≠ 실제 없음.
- 결론: 지명된 좁은 판단·두 조합·직접 자료 하한·원표/조건 복구 요구 충족. 자체 연구 산출물 범위 DONE 가능; 강한 주장(실제 사용/성공/총노동/독립 성능)이나 선행 PARTIAL 완료로 확장 금지. 독립 검토 미시행, 자체 검토만.

## Q별 근거/반례/남은 불확실성

| Q | 근거 ID·정확 위치 | 실제 반증/오류를 어디서 찾았나 | 남은 미확인·변경 조건 |
|---|---|---|---|
| Q1 | A01 comment1746468973, A02 diff1020; B03/04 roles; C01 layer92 C04 id40551996 C02 key C05 IHDR; D01/02/03 #parsing; E01 reply1877111832 E02 heading; F01 dev655 rows1/2 F02 Data Spec; I230/233/234/235/236/237-3 원표 | B05 L57–68 복수 authority; E01 읽었으나 불명확; F01 0 | exact A build/PCM, E usage, C render; 각 카드의 보류 이유 |
| Q2 | S01 §3.1–3.6, S02 §5.2; S05 L895–914/qualified relations; H01 §4.6.2; A01/I230-3, B05, C01–05, D01/02, E01, F01/02 | 동일 B05 서지의 복수 역할, H05/H06 같은 DOI, H03 L495 follow-up reports | 서로 다른 사례가 실제 공유 evidence 있음 확인 시 관계 갱신 |
| Q3 | relations.csv 15, A01/E01 actor IDs, C01/C06 style file, B05 role, D01/D02 version | A와 E는 actor와 사건 달라 사슬 조립 불가; C06 8 layer 아이콘 없음 | 강한 필요 edge 0은 제한된 표본; 공유 원문/required condition 발견 시 재개 |
| Q4 | S03 §4.2.4–5, S04 previousVersion; I234-4 19/20 row, C06 fixed style; A/B/C/D/E/F locator | W-I column shift + World actual zero, C04 JS wire parse name encoding 오류, E timestamps inherited | 판/위치 바뀌면 quote/selector/State 재대조; PNG pixel/CRC 및 artifact 실행 없음 |
| Q5 | P01–P11 actual decisions (P04 uncounted), P12/P13/P14 process | PEP622 superseded/634 split; PEP703 rollback, P10 링크 자유서술 parsing 단점, P11 result-first logic 단점 | 명시 재개 조건 없는 ADR에 새 trigger는 제안; current compiler status 미확인 |
| Q6 | H01 ch4 §4.6.2 H02 ch5 §5.2.1/5.5.4 H03 results/history H04 history H05 Box1/2 | H03 2 follow-up reports added to existing study, conclusion unchanged; subgroup nonpooling; H04 substantive change vs format | H04의 실제 이전/이후 conclusion 원수치 미확인, 개별 trial 원문 별도 필요 |
| Q7 | packets.md, assemblies.md, removals.csv, RESULT tables1/2; P09–11, H05 reporting | ③ L 초안에 X 세부 주장이 섞였음을 발견 → ④ L narrow 축소, lost_claim 정정 | 모델/사용자 성능, 실제 추가 열람 시간·link failures 미측정; 독립 사용자 실험은 별도 |

## 원격 재열람 예비 검사(⑤ RESULT 고정 SHA)

29c48aff9817f43db2d303c5200c470832ccb278에서 SCOPE, sources, packets, relations, assemblies, removals, COUNTEREXAMPLES, RESULT 8/8 file contents read back. JSONL 71 parse 성공/71 unique IDs/required keys 누락0; group/case counts 위와 일치; pair CSV 15 unique data rows/모든 row 10 columns, removal CSV 12 unique data rows/모든 row 10 columns/retainedEach5, 비용 5/12. RESULT first header exact, rows6/12 and width5, Q1–7 headings, 마지막 표 실제 pipe rows 3 data/4 columns(끝 trailing newline 제외); W-I 정정 행 20 cols. L 6 narrow rows, packet 6 headings. ④에서 README Data Spec locator의 잘못된 guessed anchor 제거, 원파일 heading으로 연결. 
첫 SELF_CHECK 커밋 fecddc151d1df8dd1413708d93bd5123030afce8에서 9/9 재열람, JSONL71/37, 누락0, source IDs 미등록0, 링크 ledger 미대응0, table widths/rows [6,12,8,6,9,3], W-I20, scope ahead12 behind0 outside0 확인. 추가 자체 점검에서 Primer는 비규범 Note라는 경계 발견. S05 PROV-O 2013-04-30 Recommendation 직접 읽고 원장/RESULT 보강, H04 발행일/저자 보정. 최종 SELF_CHECK 새 커밋 SHA에서 위 검사 재실행 후 HANDOFF만 단독 커밋할 것. 결과 SHA/파일/경로 비교의 실제 관측을 HANDOFF에 기록. 중앙표 diff 금지. 독립 reviewer가 같은 근거를 검토하지 않았으며 자체 점검을 독립 검토로 표시하지 않는다.
