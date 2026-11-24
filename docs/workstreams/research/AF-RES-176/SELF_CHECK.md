# AF-RES-176 SELF_CHECK — 자기검토, 독립 검토 아님

상태: PARTIAL. 표본/원 단언/렌더 조인 판독 완료. 과거 실제 실행의 동일 조건·독립성, 역사적 실패→성공, 환경 동일 관측행 조인 미확정. 자료를 읽은 사람이 스스로 검토한 것이며 제3자 검증으로 표시하지 않는다.

| 질문 | 근거/원장 행 | 확인 | 미충족 및 다음 최소 확인 |
|---|---|---|---|
| Q1 | S01 S03 S04 S05 S31–S33; T01–T10; H01 S25 H02 S26 | 보고 생성판 8811ba2, 385+246 test definitions, 순번과 옵션/오류/입출력 주소 | 주표본의 당시 fixture 해시/실제 mode, 동일 ID 술어 변화와 단순 이동 쌍은 미확정. 파일 역사 비교 필요. H01은 fromRdf 보강만 |
| Q2 | S02 S05–S13; A01-1…A10-6 | 원 단언 test/subject/assertedBy/outcome/mode/date와 report column; 모든 55 제출 raw/render 일치 | 전체 RDF parser/다른 7 보고 파일 및 실제 실행 로그는 미검사 |
| Q3 | S08–S24 S34–S36 | 6 별개 제출 subject/판, 11 코드·dependency 문서 | G exact release, C exact tag, 직접 port history, 실제 런타임 lock과 run ID 없음 |
| Q4 | A01…A10, D03 D05 | 30 primary pairs: 20 agree, 0 disagree, 10 missing. 30 supplement pairs: 28 agree, 2 disagree | 동일 조건 독립 run 쌍 0 확인/20 미확인; 공통 엔진 및 복제 실행의 입증 0 |
| Q5 | A04-5, S23 S24 S25 S26 H01 H02 D04 D06 | Gold 단독 fail 제출, EX ordered option과 semiauto 처리 가능, fromRdf expected 변화, 신규 expansion tdi13 제안·비교 보고 | 동일 조건 단독 실패/실패→성공 쌍·역사판 raw logs 없음. commit search 'invalid typed value', 'datatype', 't0123', '2020 report'에서 해당 이력 못 얻음. 범위 밖 사례를 주표본에 합산 안 함 |
| Q6 | S27–S30 P01 P02 E01 | NIST method stratification, NMI proficiency, USGS NWIS→WQP 출전 | 익명 실험실 원장/기기 원 로그 미확인. 동일 environmental observation row 0, feed-level 1만 |
| Q7 | S01 S02 S05 S08–S10; D01–D08 | 세 질문별 대표 원전 및 이유/허용 문장 | receipt 있는 문장은 조건부 예시이고 실제 결과 아님 |

## 정합성 자기검사 (GitHub에 다시 열어 수행)
- SCOPE c0d3f05708a3066e25a910458434b40a36782103: blob 65a6efba3c02c1964e62e508f0c9b617d61eae06, 3676자. 최초 SCOPE 2bbbba1e5889c810c59bbcc10b40895338e334d1 및 최초 frame 769685a0fe3a11e38aebd1b8df9423fd93303f08을 각각 이전 읽기에서 재열람. 생성판 보정 이유와 outcome 노출 가능성 보존.
- frame 0aee04b45a8b9f8e5f629e842af326911ded8554: blob e2f42f17208c9e2dbf66864874790fd20ca9f86c. 644행 = 385+246 tests + 13 files. 시험 10 포함 621 제외. 구현 파일 첫 3, 보강 3, 남은 7 제외.
- assertions 0809972ad37d29d85ce83d717c3366c5414ee1d9: blob f89b3bfd0a9627bcec0d690284915257e0eeab44, 60 고유 assertion-row IDs. Primary 25 passed + 5 not-submitted. Supplement 29 passed + 1 failed. 55 actual assertions; 5 vacant. 55/55 raw/render match, mismatch 0; all 60 rows join selected test IRI. Exact source lines and date preserved; vacancy rows have no assertion line.
- tests 670acc77c24eb90a6a3c91cf9e7bc8464a807616: blob cdc67efb24d6f89e3972357b569db6bf3bc50003, 10 unique test IRIs. Option field in tests.csv is manifest option not observed run option. Expected error strings are copied from manifest; input/expect fixture content not all opened.
- sources 336b61e32db5bc49554936f40cfceffb9fd2da60: blob fe61dab6142e322c104e7c18967c5f5e4ed0caef, 38 rows; counted 30 unique work_ids; no URL missing. Categories 7/6/11/2/2/2 vs min 4/6/6/2/2/2 by document type. Environmental 2 docs only describe collection/publication; strict observation-original quota not fully met. Excluded 8: revisits/failed/landing/prior/superseded. Work count not run count; 6 submission lineages, 0 verified independent historical run lineages; two proficiency report groups, 1 USGS feed relationship, 0 exact matched environmental observation rows. Individual internal file fetch/retry calls not counted as additional sources; ledger covers substantive reads, not exhaustive low-level click log.
- advice 4742986e1f621bd0f6c1876ba22c299bc4946051: blob 1b735d90fab1dc22abeae47cdc0933584e113b1e, 8 rows.
- RESULT 7d3162736d23565d72bff61d8bbda87dd0e93218: blob 8a3bb91ed12f2ed99e0b0974918d70e07022dac6, 23658 chars; 3 mandatory tables first; all Q1–Q7 present; weakness table exactly 3 data rows. No formal external independent validation.
- Programmatic check in connector JS: parsed CSV/JSONL as written, checked unique IDs, joined test IRI, recomputed pair counts, compared raw/render outcome. It is not a test suite execution, parser validation, or OS command; no local runtime tests. Source address read and row IDs in files verified above.

## 반증 시도
- 서로 다른 페이지/파일은 독립이라는 가설: S05–S07 rollup mechanism and 55 matching raw/render defeat. 
- 공통 test definition means common measured execution: NIST P01/NMI P02 measurements differ under same sample; disjoint submitters/dates/code support distinct reports but fail to prove distinct runs.
- 모든 제출이 같은 결과라는 가설: Gold A04-5 failed (vs five passes in sampled six); exact conditions missing. No dissent among 20 primary comparable reported outcome pairs. Only searched selected 60 cells, not all report or historical report versions.
- 동일 ID=동일 술어: S24 different ordered variants; S25 expected result change (outside algorithms) defeats general claim; same-ID change in main sample not established. S26 tdi13 newly added; don't use as an old ID transition.
- 5 C no entries=FAIL: S10 no matching assertion, render no compact column, S16 stated supported algorithms. Do not count as failure.
- participant consensus=independent reference: NIST/NMI assigned value source may be participant robust mean, not independent; IDMS exception in NMI.
- two web portals=two observations: S29–S30 explicit shared feed; exact environmental row remains untested.

## 남은 검증
1. Retrieve historical suite sources for each submitted date, hash input/context/expect, processingMode/options, base URL, loader rules, comparison procedure; retrieve historical EARL submission PR commits and individual execution artifact/run IDs. Distinguish same-core wrapper/port from common standard by exact runtime and source lineage.
2. Compare Gold t0123 raw outcomes in historical report versions; inspect actual test/expect diff and fix commit. Find expansion/compaction stable-ID content changes vs pure path relocation. No fail→pass claim until exact comparable pair.
3. Extract same historical USGS row from NWIS and WQP WQX2.2 for pre-2024-03-11, join organization/activity/site/analyte/method/time/units/qualifier/value; metadata alone insufficient.
4. Codex verification: use pinned build and recorded sources; repeat RDF parser join and log checks only after exact input retrieval. New suite run not historical receipt. No product DB/search/Studio change.
