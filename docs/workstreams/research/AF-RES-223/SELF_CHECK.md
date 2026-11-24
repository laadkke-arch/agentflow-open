# AF-RES-223 SELF_CHECK — PARTIAL

자체 점검 (worker 1명); 독립 검토/블라인드 재채점/실제 테스트 실행 미실시. 자료 직접 판독과 공개 spec의 기대만. 계획판과 실제 착수판의 차이 및 실패 조회는 SCOPE/P05–P12에 정정 기록. 212의 US 6, 한국어 4안은 재채점하지 않음.

| Q | 주요 근거 ID 및 검사 | 반증/경계 | 판정 |
|---|---|---|---|
| Q1 | P01–P12; AM/RM metadata; A00/R00; A37–A50; R08–R11/R29–R39/R47/R52–R62; frame 197 | A38 상속으로 최초 degree 선택 정정; A 후순위 미열람; release list 빈 배열이나 tag-only 목록 400; R2/R3 미확보 | 조건부 화면 4/6, PARTIAL |
| Q2 | A48/A51–A62, A01/A14/A17–A21, A04/A14/A22–A26, R27/R03/R41–R48 | A3-2 주소 유형의 첫 폼 확인, 후속 address 폼 미열람; R1 course는 training route부터; exact runtime URL/ID 미확인 | 소스 연결 8/12, 4 결측 |
| Q3 | A10/A11/A15/A47/A48, R14/R16/R17/R40/R46, G01–G03, W01/W04 | default Change + leading space span 확인; optional parenthetical suffix는 generic gem; override/CSS/AT 실제 결과 미확인 | 조건부 name 8/12, AX 0 관측 확보 |
| Q4 | A34/A35/A63–A65, A19/A22–A24/A54–A57, R04–R07/R21/R25/R50/R51 | selected exact written clicks + review 2/8, other 6 only helper/controller/adjacent; no execution. Feedback contrast two written clicks; final return R1 미확인 | PARTIAL |
| Q5 | A58/A01/A04/A07/A27/A43; R01/R12/R14/R27/R47; G01 | same visible name/route different field vs same full form; exact same-name+same-field simultaneous duplicate 미증명, identical dynamic labels potential only | 대조 확보, 일부 결측 |
| Q6 | W01/W02/W03/W04, G01/G02 | 2.4.4 contextual purpose ≠ unconditional isolated name uniqueness; no service-specific AT observation | 규칙/제작자 지침, 실측 없음 |
| Q7 | L01–L07 | 2012/2009 record IDs 2/2, holding IDs/request/AX 0/2; old cache list not current; L05/L06 aliases unknown | 서지 수준 PARTIAL |

## 원장/파일 일관성
- 소스 원장 최종 174행, 독립 산입 76, 실패 11행 비산입. 산입 분포: template 13(실서비스 12, 공통 gem 1), route 29, form 13, test 12, standard 5, library 4. 최소 22와 개별 범주 하한 충족. G02 generic test는 소비자 시험 하한 제외. RB/ERB/caller 같은 lineage 비산입, A47/R40/G03 같은 gem metadata 비산입, L05/L06 동일 판 alias 가능성 보수 제외. 독립 문서 76 != 독립 사용자 관측 수.
- 이전 RESULT 커밋 bb84120312dd3ec47ef78713d99b8907ecede12f의 7개 파일을 GitHub 고정 SHA로 다시 열어 readback: 158 ledger rows/158 unique IDs/76 unique counted work_ids; frame 197, anchors 12 = 8 conditional + 4 missing, returns 16 = 12+4 contrast, CSV 참조 ID 미발견 0; RESULT 첫 header 및 table2, Q1–Q7, 마지막 3건 표 확인. 이후 원장에 release/control 16개(산입 0)를 추가하고 RESULT 분모 정정, 8b3c53f7646f922cdcbc7c4a17a4e4f3df66c86c. 마지막 결과판에서 다시 확인할 것.
- 선정 4 화면/6 예정; strict 12칸 연결 실패. 일부 화면의 row-level rendered markup, exact URL, real focus, unchanged fields, end-to-end return 확인 부족. 실제 소비자 사건 공개 로그 확보 0; 실제 service screenshot/AX/AT 발화 확보 0; library reservation executed 0. 이는 모집단에서 사건이 없다는 뜻 아님. W05 mock #, R-feedback/personal shared form, A-degree later contrast, generic renderer는 빈 칸 대체 아님.
- sources.jsonl checked_utc는 원장 작성시각, 개별 처음 읽은 시각 미기록. 웹 cache/규칙 발행판 구분. 직접 열람 실패 복구 P05/P06, A70→A49, A71→A58, R63→R47, L07→L01, G04→G03.
- 자체 결론이 틀릴 수 있는 경우: R1 completed 분기에서 실제 editable false/first row 없음, CSS/ARIA가 span을 접근성 tree에서 제거/override, course label이 training route edit을 오도, same-name reference/degree collision, shared form의 JS focus가 행별 action을 구별, library hold group이 두 bibliographic IDs를 실제 하나로 합침. 반례 검사 명령과 fixture는 HANDOFF.
- 한계/정정: SCOPE 최초 커밋은 223 항목 읽기 실패였고 후속 복구. 최초 A degree를 선정 후보로 보았다가 accept-offer 상속 및 호출을 확인해 정규 슬롯 교체. 197 path frame은 직접 열람 197건으로 주장하지 않음. 라이브 배포 release/AT 환경 미확인. 일부 원자료 행은 해당 파일의 핵심 절만 판독; 파일 전체와 코드 실행을 확인했다고 주장하지 않음. 독립 리뷰 요청/실시 없음.
- 상태 PARTIAL. 직접 자료 하한은 충족하지만 12자리 엄격 표본과 Q7 holding/transaction 증거 미달; DONE으로 색인하지 않는다. 
