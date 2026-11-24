# SELF_CHECK — AF-RES-175 (자기 검토, 독립 검토 아님)
고정 점검 입력: RESULT commit 3a3a1d382a10dc05d064419073417460f9b54ed2. GitHub API에서 해당 SHA의 원장·결과 재열람. 작업자 판정 PARTIAL.

| 질문 | 직접 대조한 원장/원 위치 | 충족/첫 결측 및 다음 확인 |
|---|---|---|
| Q1 | G1–G4, S1–S4; R01/R11/R07, D06/07/13/14 | 모델명, 원 송신판, 결과 단위 확인; GD01–15 파일 목록. 참가자/원 파일 지문 불명, D09 xlsx/ D15 PDF 추출 먼저. |
| Q2 | G1–G4, S1–S4; R01/R03/R11/R07/N09/N11 | 50 kN/m, 25 kN은 보고된 명목량; 직접 keyed 원값 0. 원 입력 접근 및 ID/단위 assignment 조회. |
| Q3 | SC1-A–E, SC2, GC1–4; N01/N03/N04/N10/R08/R09 | 정확 제품 release pair는 S만 명시; 옵션 충돌/수신 객체별 수치 결측; A→B→A 0. 로그·MVD 확인. |
| Q4 | GC1–4, GD01–15; R03/R04/R12/D13/D14 | 본문 7/16, 원면 14열(잠정), 누락 후보 7열; 실제 제출 join 0. 동수/외관 차이와 -718/+718 확인; 동수/수치 차이 미확인. |
| Q5 | SC1-A–E; R07/R08/N03/N09/N10 | 양 방향 하중 E/P 및 재료 P/F; 별도 native 입력, 물리량/부호/대상 일치 미확인. 원 IFC·양방향 수신값 필요. |
| Q6 | AV1–4, MARC1–5, REF1–3; A01/02/04, M04–09, R14–16 | FADGI 두 프로젝트 및 BFI/Kromer, LC pilot/규격 직접 읽음; 개별 파일/필드 acceptance 0. 보충 첫 두 공개 시험 적격 0/2. |
| Q7 | A-VIEW/A-ATTR1/A-ATTR2/A-EDIT/A-UNIT/A-ANALOG; advice.csv | 사양/구현/관측 구분; 조건부 2, 보류 3, 분야 전이 제안 1. 확정 호환성 권고 0. |

## 분모 및 행 검사
- GitHub API에서 3a3a1d...의 sources.jsonl 57 JSON 행 파싱, source_id 57 고유, include_unique_read=yes의 work_id 23 고유. 열람 행 ≠ 문서 수 ≠ 독립 시험 수. 데이터 다운로드/랜딩/미러/재열람 별도 산입하지 않음.
- 모델·방향·권고 원장에서 R/D/N/A/M 두 자리 source ID를 추출하여 source_id set과 대조: 결측 0. 이는 기계적 참조검사이지 해당 사실 독립 검증 아님.
- frame.csv 34 데이터행(원 모집 8, 지정/보충/재판독 포함); models.csv 29(8 primary + 6 designated + 15 directory-only); directions.csv 10(9 지정 방향/자기 재수입 포함 행 및 SC2; 개별 제출 10건으로 세지 않음); advice.csv 6. RESULT 표1 8/8 원보고 판독, 0/8 완전 조인; 표2 8+5 지정+2 보충, 동일 객체 실측 0; 표3 IFC 5 + 분야 비유 1 별도. G4 load 공개표 미측정, S2 단위별 grade 미측정, 다른 값 미확인은 측정 실패로 단정하지 않음.
- 엄격 범주별: 주 연구 원보고 3/4(G 결과/설계, S; G 동일 계보), 추가 연구 R14–16 3개는 공개 시험 자격 미확인, 첫 2 적격 연구 0/2. 파일 본문/개별 제출 원값 0/6(목록 1 별도); 역사판 계열 문서 3/6(N03,N09,N10; exact two-product option snapshots 0); AV 보고서 3 work/4 프로젝트, 개별 입력·기대·실제 인수 0/3; MARC 문서 6 work, 같은 필드의 실제 수용 0/3. 폭넓은 23개 하한과 요청 층별 하한 다름. 두 핵심 독립 시험 계보 G/S 2; 탐색 포함 관측 계보 후보 10(G,S,Aksamija,Aleksandrov,Arroyo,BFI,Kromer,SIA,NARA,LC pilot). 기관/시험 계보 후보를 독립 판정 근거 10으로 과장하지 않음.
- 원표 G Table7 본문 7/16, 14 표시열 잠정 전사; 제품 후보 7열, 동일 제출 ID 매칭 0. S 방향별 버전 쌍 4, self 별도. 실제 원도구 cross-tool 재수입 0.

## 반증 시도
1. “entity 손실 = 의미/값 손실” 반례 GC4 벽 -718/+718, GC2 동일 개수와 site 외관 이상. 동일 물리량 단위 재표현이 가능해 unit 수를 값 손실로 일반화하지 않음. 동일 수/다른 실제 수치 사례 미확보.
2. “순방향 성공 = 역방향·복귀 성공” SC1-C/D 하중 P, 재료 F, 순방향 재료 P; 서로 다른 원 제작 입력이고 MVD 충돌 때문에 방향 자체의 인과 확정은 보류. self reimport를 왕복에서 배제.
3. “불완전 변환은 언제나 실패” SC2 reference block, AV3 ISO vs MPEG2 메뉴 기능, M04 nac/ignore, M09 linkage known issue. 목적별 의도된 손실과 결함을 구분. 동일 바이트/값이 보존된 반대 사례는 직접 파일 비교 없어서 미확인.

## 남은 일/제약
웹 소스 추출 400/429, 원 데이터 사이트 접속 실패, ZIP 원바이트 미판독. R14 publisher PDF text only / screenshot 실패 표시. 새 변환/설치 없음, GitHub API 기반 파일 재열람만, checkout session check/로컬 git diff --check 미실행. 독립 검토 없음. 실험용 제품 DB/검색/연동 선택 없음. HANDOFF에 첫 재개 명령과 남은 원자료 명시.
