# AF-RES-259 자체 점검 — PARTIAL

검토 대상: d75f262a6efcbdb89f91eb951f717e67a1524eb9 (RESULT의 출처 ID 수정판); 착수 9eeb7105c7edec2c5c4c0a1f722916b9d664b236. 독립 심사자는 없었고 같은 작업자가 자료 재조회, 원행/CSV/JSONL 비교 및 반례 판독을 수행했다. 외부 API 반복검산/ZIP 다운로드·전체 순위 재현 미실시 또는 실패.

| 질문 | 직접 근거와 정확 위치 | 반증·경쟁 설명을 확인한 곳 | 남은 미확인·최소 다음 확인 | 판정 |
|---|---|---|---|---|
| Q1 | H01 L64–65, H02 L60, H03 L65–87, H04 p4, H05 L94–102, H06 L145–149; G03 established/admin | G03 2010 vs H01 2018; M08 2018 대학과 M09 2015 협의체 별도 EQAR records인데 ROR 동일; H05 학교 2011 분할 | 원 법령/법인 scope의 ROR 판단 이유, 연구시설/소장품 별도 계승은 미확인; M08/M09와 2018 법령·등록 변경 티켓 확인 | 전환일 2/2, 범위 PARTIAL |
| Q2 | G01/G02/G03 same v2.5 RC id/status/names/admin/relationships, G04 v2.13; R01 L141–190, R03 L37–59 | M07 011htkb76 vs G02 01yvrd251; M10 ROR 표시 공석; M05/M06 Aalto 외부 ID 후보; 실패 F 계열을 ID 없음으로 세지 않음 | 현행 6자리 및 011htkb76 원행; v2.16 ZIP 추출, API default/all_status 비교 | 3/6 RC, 0/6 current, PARTIAL |
| Q3 | G01→G03, G02→G03 및 G03→G01/G02 명시; G04 predecessor 두 개 재관측; R01 L150–159 | G05 parent 3개, G04 child; successor 역 의무 없음과 active parent 역 의무 구분; Aalto는 관계 원행 미수신으로 누락이라고 못 함 | Aalto 3 원행과 4 방향, v2.16 Sorbonne 4 방향; 정상 공석 확인 시 정책 적용 | 4/8 방향, 2/4 쌍, PARTIAL |
| Q4 | P01 PDF p1 †‡, P02 PDF 텍스트 index1 L28–42, P03 PLOS L80–107, P04 PLOS L91–113 | M01 SU-INF-2018 컬렉션이 2017 출판 후대 보관, M03 Pure 2010 vs P03 publisher 2009-10-26; P02 접수 2017/발행 2018/포털 deposit 2022 | HAL/Pure 기간 전체 페이지·순서 확인 및 첫 적격 4건, P01 최종판, P02 화면 재판독. 원문 위치에 ID 표시 0/4이지 논문 전체 ID 부재 단정 아님 | 후보 4/4; 최종 0/4, PARTIAL |
| Q5 | T01/T02 2026-03 요청 및 03-31 완료; G01–03 JSON v2.5; Z01/Z02/Z03 발행 목록; G04 v2.13 | T07 #41993 완료통지 뒤 오류 인정; G07/G08 동일 ID old→new display, alias 추가; UPMC Paris VI alias 최종 행 미포함; RC≠production | Z01 v2.4, Z02 v2.5, Z03 v2.16 ZIP checksum/행 직접 비교 및 Aalto 과거 변경 이력 | 일부 변화 확인, production 0/3, PARTIAL |
| Q6 | G07/G08 동일 ID active relationships=[] 및 이름 변경; G05/G04 reciprocal parent/child; I01 AN/YD region rows, I02 §3.1.7 L1647–1658 | G06 PRISM Sorbonne→Paris 1 다른 부모, G05 여러 부모; M03 포털 과거 논문, M07/M08/M09 ID/scope 충돌; T03 개인 소속 변경은 별개 | 동일 ID rename 법적 동일성(요청자 진술), 현행 published row, 실제 사용자 오류율 미검증 | 통제 RC 2/2 + IANA 2/2, 조건부 |
| Q7 | G02/G03의 원필드 및 P01; M07 충돌, H01 기관 역사; G07/G08 rename | 동일 canonical_id로 원문 덮어쓸 때 P03·M07·G05 실패. 서로 다른 목적에 역사 링크 1 / 이중 링크 / 후보 보류 비교 | edge 삭제/withdrawn 및 scope 변경 때 조건부 철회. Aalto는 공식 홈페이지만 현행 연락 기본, ROR 외부 후보. 실제 제품 시험 없음 | 설계 후보, 사실 보증 아님 |

## 분모 및 원장 검산
- 원장 재조회: 73행 JSON.parse 성공, success 47, failure 26. counted=true 43행, 서로 다른 work_id 43, lineage_id 14. 중복 산입하지 않은 성공 4(G04, G08, H05, M11). 필수 키 17종 누락 0. 정확 시각은 개별 영수증 미제공(UTC 날짜만). 원장은 직접 판독/실패 묶음이며 전체 HTTP 호출 수는 미확인.
- 그룹별 (하한): 지명 원행 3(6), 운영자 10(4), 기관 역사 5(4), 당시 원문 후보 4(4), 통제 11(4), 보조 10(하한 없음). 요구 그룹 33개이나 대상 원행 3 미달. 당대 원문 후보 4는 읽었으나 사전 표집 합격 0/4. 자료 총수 초과로 핵심 미달 상쇄하지 않음.
- orgs.csv 6개 데이터 행/22열; attributions.csv 4개 데이터 행/16열; 각 행 CSV 따옴표 필드 수 일치. ror-release-records.json 6 records (지명 원행 3 + SU 후속 1 + 통제 2); rename-records.json 3 records(두 Sumy 판과 Helwan 추가). 실제 raw relationships 필터로 SU 4방향, v2.13 역방향 2 및 Neuro-SU child/parent, PRISM 다른 부모, Sumy 두 판 공석을 다시 확인. 소유 원행의 JSON 본문은 upstream SHA/path/blob 동반. 생산 파일 재다운로드/byte equality 검증 아님.
- 지명 기관 6자리 중 RC 명시 3, 원행 미수신 3; 최신 발행판/API 원행 0/6. 지정 관계 8방향 중 v2.5 RC 명시 4/8, 정상 공석 0/8, 미수신 4/8. EQAR M10 표시 누락 1은 ROR 공석과 별도. 통제 rename [] 2판 및 active parent/child 2방향은 8방향 분모 밖. IANA AN/YD는 두 region 행, 등록부 한 원저작.
- 필수 표 두 개가 RESULT 첫 부분에 위치하고 열명 일치. 표1 지명 6행+통제 2행, 표2 후보 4행. 표 아래 각각 분모. Q1~Q7 및 대안/철회 조건 뒤 최종 약점 3행으로 종료. 외부 링크 클릭/재호출 전수 확인은 하지 않았고, 원장 URL 및 원행 path와 비교했다.
- 검토 중 RESULT의 출처 ID R02/R03, T03/T07 혼동 정정(d75f262a6efcbdb89f91eb951f717e67a1524eb9); URL은 동일. 앞선 orgs.csv UPMC EQAR 후보 자리 수정 이력은 changes.md에 남김. 원자료 성공과 실패, 공석과 미수신, 해당 없음, 미실행을 구분.
- GitHub compare base→검토 대상: ahead 11 / behind 0, 추가 파일 8개 모두 docs/workstreams/research/AF-RES-259/ 내부(SCOPE, RESULT, sources, orgs, attributions, changes, 두 원행 JSON), 외부 경로·dot-control 변경 0. 이 SELF_CHECK 커밋 후 결과 SHA 고정 및 경로 재확인 후 HANDOFF 단독 추가.

**합격표 결론: PARTIAL.** 직접 열람과 반례, 설계 대안은 결과로 사용 가능. 6자리 원행, 8방향, 생산판 전후, 4건 최초 적격 표집은 미완료. 두 사례의 모든 역사적 소속을 현재 ROR로 교체한다는 결론은 지지되지 않는다. 독립 검토/실행 검사는 별도 후속.
