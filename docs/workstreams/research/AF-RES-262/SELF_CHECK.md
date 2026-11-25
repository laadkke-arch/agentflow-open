# AF-RES-262 자체 점검 (PARTIAL)
독립 평가자/독립 재현 없음. 아래는 작성자의 사전 규칙 대조 및 커밋된 산출물의 재열람·구조/산술 확인이다. 신규 제품 실행, 코드의 동적 시험, 모델 훈련/검색/랭킹 재현, 사람 모집·사용 실험은 하지 않았다.

| 질문 | 원근거와 위치 | 자기 결론에 대한 반례·확인 | 남은 미확인 및 다음 최소 행동 |
|---|---|---|---|
| Q1 | D01 §3, Fig. 1/2, Table 2; D02 CSV 헤더/원행; D04 evaluation | 높은 원점수는 해당 질의에 대한 사람 관련성 판단이지 새 요구 보증이 아니다. 동일 URL의 상충 점수도 보존. 논문 4026/2089와 실제 4006/2079 다름. | 독립 판정자 ID/판 차이의 원인 없음; 공개 원본 버전/변경 이력과 ID 존재 여부 확인. |
| Q2 | D02 고정 blob 98beff4e3dca397ca4f7084e584874de4e6c7bcf; D03 원줄 5/15/20/29; judgments.csv 전체 | 공백/대소문자 규칙 적용 후 네 질의 21/22/19/22행, 각각 10 URL. 0 원행 8/1/0/5. 중복/상충 삭제하지 않음. 논문 수치로 교체하지 않음. | 별도 구현으로 csv.reader 및 blob hash 재검산; 물리 줄/논리 레코드 수 구별. |
| Q3 | F-S1/S2/S3 실패 원장; F-C1/C2/C3, F-J1/J2/J3, F-R1/R2/R3의 고정 원줄(conditions.csv URL) | 원파일 9개 직접 확인, 3개 실패. 이름 write_csvs는 실제 출력 CSV가 아닌 bcolz 적재; R3 선택 함수는 라인 handler. 보강 SX4–6을 주표로 대체하지 않음. | 첫 행동: S1–3 정확 SHA/path 접근 복구, 반환 blob 동일판 확인; 다른 판은 별도 자료. |
| Q4 | P02/P03/P05–10, CPython v3.7.0 test_csv/test_unicode; F-J1/J2, F-C1/C2, F-R1/R2/R3 | J1/J2 양성인데 ensure_ascii=True 기본값으로 문자 직접 보존 실패. JSON 의미 왕복 자체는 가능. R1 splitlines/누적, R2 helper는 한 줄이나 caller는 객체 누적; C3는 적용 밖. 원평정 오류라고 부르지 않음. | 동적 실행과 실제 환경/호출자 미검증. 최소 fixture에서 불변·CSV 동일 dialect 왕복·literal unicode·read 호출/누적 확인. |
| Q5 | D02 전 원평정, F-C1 write_json L274–283; F-J1 compact_fmt L42–57; F-R1 template L1785–1787 | 3개 실제 새 후보의 동일 query+language+URL/anchor overlap 0; 이들은 다른 역할이라 조건 적용 밖. SU는 접근 실패 때문에 후보 미확인, 0점/정상 공석 아님. | S1–3 복구 후 최초 가용 모듈에서 다음/이전 공개 함수 순서 최대 5개 확인. |
| Q6 | judgments.csv, conditions.csv, denominators.md 및 RESULT 표 1/2 | 양성 확정 4 중 Y1/N2/NA1; 음성 4와 상충 4 별도. 상충의 잠재 해석 포함 공동 성공 1–4/12. U를 0으로 바꾸면 가짜 판정; 3 보강 슬롯을 0점으로 채우면 12→15 URL, 23→26행으로 분모 변질. | 접근 실패 3 및 조건 동적 검증, 판정자 ID; 어떤 실제 채택/랭킹 점수도 추정 불가. |
| Q7 | T01 NIST 판정 안내, T02 2019 DL p3/p15, T03 데이터 안내, T04 passage qrels 원줄 1/63/195 및 첫 topic block 194줄 | (19335,1017759)=0은 실제 비관련 판정, (19335,1200258)은 해당 topic block 미등재, 뒤 passage는 다른 topic에서 2점. 풀링은 전 후보 관측 아님. 등급 1의 document/passages 의미도 다름. | qrels 전체 독립 검산 미실행. 공개 249 자료의 실제 사람 배정/채택/인수/절감 관측은 0; 별도 실제 사용 사건 없이는 확장 금지. |

## 커밋 고정판 자체 검산
- 검사 대상 RESULT 고정 SHA: 5ad458c4df25501846dda70634d7283c732ef1bc. GitHub에서 SCOPE/RESULT/judgments/conditions/denominators/revisions/sources 7개 모두 다시 읽음. CSV 인용·내부 개행을 처리하는 JS 파서로 judgments.csv 84레코드(12필드), conditions.csv 16레코드(13필드) 확인. 표집 12 URL/23 원행, 0점 4 원행, 원프레임 40 URL/84행, 0점 14 원행, 빈점수 0; 질의별 위 표와 일치. 정적 재집계이지 별도 원자료 독립 판독/코드 실행 아님.
- conditions 주표 Y3/N4/U3/NA2, 양성/음성/상충 각 4; 별도 슬롯 SU/CU/JU/RU = U/NA/NA/NA. 실제 원파일 9/12, 보강 원파일 SX4–6 별도. RESULT 연속 표 블록 행 수(헤더/구분선 제외) 12,5,3; Q1–Q7 및 대안/철회 조건 존재.
- sources.jsonl JSON 파싱 37행; 성공 30, 실패 7, 산입 28 고유 work_id(4 CSN, 12 코드 파일 [주표9+별도3], 8 규격/시험, 4 NIST); 최소 접근 횟수 합 48, 전체 도구 호출 횟수와 동일하지 않음. 2 성공 자료의 중복 work 미산입, 실패 미산입. 확인 UTC는 실제 열람 구간과 원장 기록 시각이며 개별 열람 타임스탬프 정밀도 미확보. 수량 하한 충족이 본표 원파일 결손을 덮지 않음.
- GitHub compare base dc6b22120b23a6af8558bd6031ea8ff8af041dcf → RESULT SHA: ahead 7, behind 0, 7개 신규 파일 전부 owned_path. dot-control.json 수정 없음. SELF_CHECK와 이후 HANDOFF 단독 커밋을 별도로 남김.
- 상태 PARTIAL: 정확판 주표 3개 및 SU 미확인; 부가조건 판독은 정적/계약 근거, 실제 동적 검증 미실행. 새 요구는 연구자 부가 조건이고 원 CSN 라벨과 혼합하지 않음. 전체 모집단/검색 성능/실제 채택·검수/절감 시간 결론 없음.
