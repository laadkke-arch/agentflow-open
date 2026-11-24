# SELF_CHECK — AF-RES-210

검토자: 이 작업 작성 세션의 자체검토(독립 검토자 없음). 실제 상태 PARTIAL. 검증한 중간 결과 SHA 0fa0155e3eb36574ce804dfbc94a5dfa4e55875d. GitHub contents API로 8파일을 그 SHA에서 다시 열어 대조하고, JS로 CSV 열 수/JSON 파싱/분모/최종 표 위치를 검사했다. 코드 실행 결과로 오인하지 않는다.

| Q | 근거·판정 | 반례/반증 점검 | 결손·다음 원문/검사 |
|---|---|---|---|
| Q1 | B01/B08/B10/B11/E01/E02: 편집 최소, 이동된 함수 읽기, 3-way merge 구분 | CE7 6 vs 2 indel 모형, R2 공개 기대, CE5 표시 경계 | B08 당시 메일 및 E01/E02의 실제 입력/당시 출력, 별도 3-way 결과 |
| Q2 | A01 pp413–415 Lemma1, A02 pp2–4, A03 §2: pile/LIS 길이/복원 | CE1 [2,3,1] pile top 순서 아님; C2 길이1 동률 | A02/A01 저자 동일; A03 facsimile만 1회. origin adoption 인과 미확인 |
| Q3 | B02 L87–372/B05/B06: 지역 unique, 순서, 재귀, 분기 | C1 fallback vs R3 no common; CE6 explicit anchor lock | xpatience와 classic 내부 trace; whitespace 옵션 조합 |
| Q4 | B03/B04/B09/D01–05: A-only rare block, Myers, Breezy 반대 순회/no fallback | C2 방향 차이, C1 fallback 차이, CE3 default API | Git/Breezy 같은 LF 입력, C/Python 실제 backend, Myers tie 미실행 |
| Q5 | predictions.csv 8×4 단계 기록; 5bbe48770fbff0de4c4bb5862e4094eb9f1e3be5 M 보존 | R2 길이7·return 제외, C2 두 해, R1/R3/C4 동일 예측 | 기대·구현 선노출; 순수 M→P→I 불성립, 독립 효과 미확인. 별도 블라인드 입력 추출 |
| Q6 | C01–04 expected 및 C05/06 보강, pairs.csv 8행 | CE2/3/4/5, C1/C2, R2 same expected | R1 전체 hunk/R4 hunk 결측, 새 stdout 및 trace 없음 |
| Q7 | RESULT 목적별 표3, A01/B01/B02/D02/D04/B10 등 | 경쟁 설명 compaction/context, edit-cost, merge | 사용자 과제별 실제 성과/시간/오류, 병합 충돌 및 오병합 |

## 자료 수·분모·노출

| 종류 | 목표 | 산입 | 엄격한 지정 범위/한계 |
|---|---:|---:|---|
| A 카드/LIS 원저술 | 3 | 3 | 1993 보고/1999 리뷰는 동일 저자·계보; 별도 저술로 카운트, 독립 증언 아님. Fredman 원문 facsimile(저자 호스트 아님) 1회 |
| B Git 제작자 문서·변경·소스 | 7 | 11 | 고유 파일/커밋/문서; B11 Cohen 원설명 포함 |
| C 시험파일·입력·기대 | 6 | 6 | C01–04 지정 범위 4; C05/06 사후 보강 2. 지정 범위 엄격 하한 미달(4/6) |
| D Breezy 구현·판 | 4 | 5 | C04 시험 D 중복 산입하지 않음; 같은 구현 계보 |
| E 공개 독자 원요구 | 2 | 2 | 두 독자 원질문, 당사자 원입력·stdout·선호 없음 |
| 전체 | 22 | 27 | 25 core + 2 보강; 독립 사건/실측 27건 아님 |

원장 34행 중 27 산입, 고유 work_id 27; 비산입 7(중복/실패/범위 밖/실질 없음). 소스 원장에는 계보·판/가능한 blob SHA·확인일·구간·관측 수준·한계·산입 사유가 있다. failed 직접 자료는 하한 제외. 시험 C 하한을 같은 파일 내 inline input/expected 여러 개로 불리지 않았다. 주표본 선정은 행 텍스트에 한정한 사후 명료화(스칼라 문자열, tuple, empty excluded); 문자 단위 전체를 사전 모집했다는 주장 금지. SCOPE의 ordered byte pair와 Breezy no-LF list를 구별하며 같은 LF text로 정규화한 bytes/file 반복은 frame에 명시했다.

frame.csv 46 데이터행: selected4, duplicate19, excluded13(일부 범주 그룹), capped4, control4, posthoc2. 유효 정적 호출 위치 27=4+19+4, 고유 쌍 8=4+4, Git 15/3, Breezy 12/5. 실행 횟수가 아니며 excluded 그룹의 개별 스칼라 호출 수는 미산정. pairs.csv 8행(4 actual/4 control) JSON a/b 배열 길이와 a_count/b_count 일치. predictions.csv 32행 4단계×8, 기존 M 행 보존. mapping.csv 9행. 네 CSV 열 수 모두 일치, JSONL 파싱 성공. RESULT 제목 직후 지정 표 3개, 마지막 약점 표 3개 데이터행 확인. Q별 연결은 위 표 참조. 자료 열람과 명령 실행은 다름: 공개 expect 2 full hunk(R2/R3), 1 grep(R1), 1 matches(R4), 4 통제 기대 없음. 새 stdout 0. 독립 검토 0. 인간 선호 측정 0.

## 자체 반증 결론
"원전 추가로 정확도가 향상됐다"는 주장은 지지 못 한다. 원리가 순서 증인을 제한하는 설명상 근거는 확보했지만 특정 동일 길이 해/재귀·출력 예측은 구현 필요. M은 정답 노출 전이 아니고 P/I도 독립 순서 측정이 아니다. 실제 구현 반례는 정적 추적이며 검증 전 확정하지 않는다. 주표본/유형 하한 결손·실측 결손 때문에 PARTIAL. 범위·원장·예측·반례·결과/자체검토는 GitHub 단일파일 API에 맞춰 더 세분화된 커밋으로 보존했다.
