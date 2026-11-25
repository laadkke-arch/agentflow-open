# AF-RES-244 SELF_CHECK — 자체 검토, 독립 검토 아님
## 증거·반증 검사
| 질문 | 원근거 ID | 실제 반전 탐색 및 관측 | 남은 확인/판정 |
|---|---|---|---|
| Q1 | A1–A3, A*-html, E1–E5 및 -html/-download, R1–R3, S1–S3 | 1.6 URL title vs source tag 비교; DOM 실제 section 재검사(정확 h2 Gallery examples), 전체 13 href, 1/9/3, no dup; 5/5 script blob 같음; pinned publisher HTML 8/8 일치 | 설치 SG 판/actual build receipt 미확인, source tag commit fixed; N2 정상 공석 |
| Q2 | R1–R3, S1–S9, E1–E5 | RST explicit path인지 확인: name/member args만; S4/S5 AST 및 explicit role 구별, S6 actual test positive print/role, neg literals/!; globals=False; E1 L292/296 텍스트 role; C1 first release sort | 해당 build _codeobj 미확인, actual membership exact path 후보; 보강 SG v0.19.0과 stable 비교, 설치판으로 사용 금지 |
| Q3 | E1–E5, E6–E9, I1–I3,I8,I10 | 다운로드와 tag code 대조, import vs direct vs internal; N1 direct kneighbors 0; C1 feature selector, C2 pipeline; G1 설명 k20/코드 k30 반증; E9 다른 graph API | runtime dispatch/실행 미실시; N1 optional dependency 실제 종료 원인 미확인 |
| Q4 | E1–E5, E8, I1–I12 | E8 L585–591 실제 반환 폐기, L2166 [0] 거리만; I2/I12 return_distance=False 구분. I11 positive both; C2 내부 predict→accuracy, scatter true y; E6 explicit predict grid 보강. G2 .5 대칭화와 I9 graph affinity 차이 | 공개 figure refs 확인, 독립 픽셀값 미측정; sample timing authored, rerun 0; E8 expected asserts |
| Q5 | A1–A3, E1-page–E5-page, E6–E9 (보강), SCOPE | API 인라인 method vs class 예시 분리; 5쌍 비교, 동일 API 중복 노출; 민감도: C2 internal label consumer 충분이면 C direct 1/2; G connectivity only 2/2; 거리/개별 레이블 원래 목적 유지 | 비가림, 인과 효과 아님; additional audit file costs separate |
| Q6 | M1–M8, F1–F10 | NLM DTD 250101, help 및 NLM 교육 지침; M6/M7 실제 역사 XML field Y/N, Qualifier Y 반례; M8 추가; 직접 EFetch 및 원문 format 대안 F1–F8 실패 | 현재 원천 XML 0/2 결측, 사본 2/2 직접 판독은 엄격 산입 제외; Q6 PARTIAL, 의료 판단 없음 |
| Q7 | E1–E9, I1–I12, S1,S4,S6,S7,M1–M4 | 순위/역할/목적/axis 반전; E6 C7의 explicit predict grid, E8 양 mode, N1 graph 대 tuple, G1 k30 정정, MeSH qualifier 조합 반례 | feature graph X.T는 설계 반례 미실행, actual graph output tests delegated |

## 분모·결측·구조 검토
- 표집 예정 6슬롯; 링크 도착 관측 5; 진짜 공석 1; 접근 결측 0. 3개 목록에 전체 13 고유 링크, 중복 anchor 및 cross-selected duplicate 0. 실제 5 독립 예제 work. 표 1 전체 직접 0/5, 조건부 5/5, 미확인 슬롯 0; 조건부는 목표 불충족/부분 충족이며 결측과 다름. N2 N/A. G connectivity 직접 2/2, distance 직접 0/2. 표 2 3개 목적; API 3, 예제 5, 두 면 5쌍 10 노출(고유 8), 추가 source 감사 별도.
- sources.jsonl 84행, 산입 38 unique work_id, 10 lineage_id, category API3 / example-test9 / generator9 / implementation-tutorial12 / NLM guidance5 / direct provider XML0. 실패17 + 다른 미산입29. 역사 원레코드 사본 main 2, supplementary1, 원천 제공 provenance/date 미확인; 동일 저작 raw HTML/download/Git/nlm-copy는 별도 원자료로 세지 않음. 실험적 독립 사건 count=5 도착 예제(+ 정상 공석1), 3 목적; NLM historical distinct main PMID 2, current provider observed0/2; 실제 실행 및 독립 검토 0. 총량 하한 21 충족, XML category 하한 불충족이라 PARTIAL.
- ⑤ RESULT 이전 검사 SHA bf53952d0bb5f1ffecd37a535feb3b85e2ccdcef에서 7 파일 전부 원문 읽음. JSONL parse 성공, source_id unique/필수 필드 전행, 실제 counts above; gallery 6 data rows ×11 cols, all 13 ×8, uses 6 ×15, 슬롯 일치, selected href↔all 원위치/선정 일치, uses source ID 존재. RESULT 첫 2표 각각 6/3 데이터행, 5열; 마지막 약점 4열 제목 확인. 이후 859f65559ea4c409860232d69dc5a17c4c7a0856에서 Q3/Q4 제목 분리해 Q1–Q7 각각 명시, 판정/표 수정 없음.
- 소스 재검색: 정확판 publisher commit 34aafaf61b4a20a7520817c02a5924baf026e3fe에서 API 3+destination 5 blobs 전부 일치. doc source tag f159b78dc59f250cdde8fe391a21f0bc871960ad, SG comparison tag 1a1e728df84b7b140989e9a4789c084a086dfbea. 사용한 각 source location/claim/limit은 ledger에. 17 failure entry는 empty observed result 아님. 
- 자신의 독립 블라인드 판독 없음; source path, published figure reference/serialized output, test expected assertion 및 라이브 실행 결과 구별. 정확한 실제 SG version, _codeobj path, NLM current XML, 그림 픽셀/실행 검증은 미확인. 최종 고정 결과 SHA의 전체 파일 재읽기 및 scope compare는 HANDOFF 쓰기 직전 수행하고 그 결과를 인계에 명시.
## 결론
직접성은 링크/심볼 관계와 다르다. 동일 문서 API 예시가 더 직접적인 경우, gallery가 contextual detail만 추가하는 경우, mode 한쪽만 직접인 경우를 분리했다. 자료별 하한 때문에 자체 상태 PARTIAL; 실제 호출/소비/출력에 대한 static evidence는 완료, 현재 NLM 직접 XML 재개 필요. 독립 검토 시행으로 표기하지 않는다.
