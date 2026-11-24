# SELF_CHECK — AF-RES-231 / PARTIAL

자체 점검이며 독립 검토 미실시. 실행 결과를 꾸미지 않았고 API 본표 원응답 없음. 결과판 고정 SHA로 재조회 검사는 HANDOFF 직전 수행/기록한다.

| Q | 근거와 위치 | 반증·누락 | 분모 및 판정 |
|---|---|---|---|
| Q1 | S06/S08/S03/S12; SCOPE 사전 정정; O00R revisions; F01–F04 | S01 OR; 최초 body/has_more/원순서 미확인; 표집 frame 불가 | cap120, 실제 모집 미확인; 0/4 배정, PARTIAL |
| Q2 | O00 current body와 revision metadata | current UPDATE는 최초 아님; tie 미지정, first revision source F09 판독 미확인; 보조 노출 | 본표 계약 및 검색 전 질의 봉인 0/4; 보정1 별도, PARTIAL |
| Q3 | S01/S02/S04/S07/S09, F02/F03; SCOPE | OR vs AND, 필터 token/원배열/제공 순서 미확인; HTML duplicate는 이동 증거 아님 | 8자리/0관측/8결측; PARTIAL |
| Q4 | S05/S10/S11 및 answers.csv/routes.csv | accepted ≠ 정확, 동일 score 2차순 정렬 없음; 실제 도착/답 없음 | 8자리/0 관측; 정상 빈 응답 여부 미확인; PARTIAL |
| Q5 | P01–P05 문서, C01–C07의 실제 절·기대; controls.sql | C03 독립 집계 오류, C04 arbitrary, C06 all-NULL 및 row/group count; tie-key 방향 | 보조 스레드7, 13통제 예측/0실행, 본표 SELECT 0/8; PARTIAL |
| Q6 | W01/W02 Tokyo, W03 Paris, W04 TR26 텍스트 | 동일 높이 3위, jump-off는 추가 관측, Paris raw 403, PDF screenshot/역사판 미확인 | 직접 결과·보고3/2사건; 규칙 보수적 미산입; PARTIAL |
| Q7 | comparison.md; D2/D3; 220 결과판(참조만) | 수렴/중복·자기 제외 실측 없음; 순위 vs payload, 공동계약 반례 | 0/4 관측 쌍; 효과 미확인, PARTIAL |

## 산입 자체 점검
- 원장 41행; 29 별도 페이지/스레드 work_id; 성공 13 lineage_id. 12 미산입(동일 도움말 1, 같은 질문 revision 1, 스포츠 규칙 PDF 1, 실패/판독 9). 페이지·절 기준 직접 자료 29이나 공통 매뉴얼/참조문서 계보 병합 기준 13이고, 필수 모집 4건 미충족. 독립 저작 22 기준 충족을 단정하지 않는다.
- 본표 모집4 중 0, 보정1, 보조 게시물7, SE 공식13페이지, PG 제작자5페이지, 공식 스포츠3 결과/보고 + 별도 규칙 텍스트. 보조/보정은 본표 점수에 미산입. 10 본표 외 사건(1+7+2), 실제 본표 사건 0. 조회 시간은 세션 시간창, 정확 개별 첫 UTC 미확인.
- frame.csv: 4 예정 자리+frame summary+calibration. routes.csv와 answers.csv: 각 8 예정 자리, 본문 방문 0, unknown. 1+1 예산의 실제 실행은 없음. 정상 API raw receipt 0; 실패 진단만 별도. 어떤 응답도 정상 empty로 분류하지 않음.
- SQL 통제 13개: 문서 예측만, PostgreSQL 16.0 미실행. D2/D3의 순위 vs 내용 별도 판정. Q5 문서와 게시자 기대/실제 결과 주장 혼합 금지. 
- 독립 검토 없음. 이후 보조 사전 노출과 겹치는 표본은 신규 판독자로 봉인 권고. 데이터 접근 장애 때문에 작업은 PARTIAL. 다음 최초 행동은 정상 네트워크에서 필터 원응답 확보와 frame API; HANDOFF 명령 참고.
