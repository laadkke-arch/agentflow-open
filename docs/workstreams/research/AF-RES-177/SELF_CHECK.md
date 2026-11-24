# AF-RES-177 SELF_CHECK — 작업자 자기점검

상태 PARTIAL, 독립 판독·검토 없음. GitHub 원격 저장물의 구조와 행 수를 다시 읽어 확인했으며 제품 실행이나 저장소 checkout/테스트는 수행하지 않았다.

| 질문 | 근거 행 | 확인한 결론 / 미확인 |
| --- | --- | --- |
| Q1 | R-M1–M5,R-B1–B5,R-S1–S4 | 목표, output, environment, OR/AND, 시간·조건 구별. 10 자연 후보; earliest 불명, 원문 편집 이전 버전 0, S2 명시 OR 미달. |
| Q2 | F-M1–M5,F-B1–B5,F-S1–S4 | 14 thread 후속: 작성자 해결/감사/진단, 유지자 설명, 제3자 구별. M1 해결, M2 포괄 해결, 그 외 최종 요구·실행 확인 부족. 정답률 계산하지 않음. |
| Q3 | D1–D8,J1,J2,J3,J12 | 태그/문서 blob 8, 정확 요청 당시 설치판은 일부만 확인. HTML/print/PDF/cold offline/복사 구분. 파일만 존재≠품질·자산 보존. |
| Q4 | C07–09,C13–20,J5,J6,J7,J8,J9,J10,J12 | 양 순서 실패 J5, PDF 성공 뒤 outline 실패 J6, 조건부 양성 J7/J9. 두 정확 설치판과 동일 산출물 직접 확인 0. |
| Q5 | responses.csv M1–M5,B1–B5,S1–S4,K1–K2 | 16행×3 표현, 동일 후보 링크 2씩. 오승인/배제/보류는 사례 해석이지 실험 결과 아님. 저자 확인 없는 사례 정확도 분모 제외. |
| Q6 | E1,E2,A1–A5,X1–3,X6–7 | 2 연도 공고, 5 NARA 원자료(4 규정, 1 실제 인수), UTA PDF 화면 timeout, 실제 이수 기록 0. 역사 인수 138+137=275, 누락 1; 정책 예외라고 추정하지 않음. |
| Q7 | C01,C06,C07,C08,C09,C14,C15,C16, responses M2/B1/B3 | 단독 M1, OR B2, 공동 충돌 B4/B5 및 J5/J6; 공동 양성 J7은 자연 표본 아님; 자연 두 링크 필수+충족 확인 0. |

## 분모 교차 검산 (원격 fixed SHA)
- sources.jsonl 62행: counted 40 unique work, 33 lineage. R14(자연 10+보충4), D8, J11, E2, A5. 제외 22행=14 후속 재열람 + 1 재등록(J11) + 7 실패 그룹. J4/J10은 실제 산출물 없는 운영/순서 보고로 공동 결과 분모 제외; J1–3,5–9,12는 원보고 본문, 일부 로그나 파일 미열람. 교육 2 연도는 동일 계보, NARA A1–4 같은 규정 계보, A5 별도 인수 계보. D1/D2, D3/D4 동일 문서 계보; M1/M3 같은 작성자 사례 계보. 원천 22개 최소수는 문헌 수 기준 넘었으나 필수 적격성/완전 모집은 미충족. 실제 클릭·실패 재시도 수 전체를 복원하지 못했다. 62는 원장 행 수만.
- frame.csv 281 data: 포함 14, 배제/보조 27, 미판독 240. query_frame 9 조회 기록. 원문 날짜별 최초 5 확정 전 240행 전체를 개별 adjudicate하지 않았고 검색 래퍼 날짜 필드 누락, HTML 100개 제한. 전체 범위 검색의 첫 시도 원순번을 별도로 전부 보존하지 못했다.
- requirements.csv 14 행; 초기 판독 후 댓글을 append했고 최초 구절·논리 필드 유지. combinations.csv 20행, responses.csv 16행; K1/K2 제외 자연/보충 14. 모든 response 2 links. RESULT 표1 14, 표2 20, 표3 16, Q1–7 모두 있음, 마지막 약점 3행. sources 15 필수 키 전행 있음. URL 112회 등장(중복 포함); 원장 기록 URL 기준 매핑. 독립 판독 정확도나 실제 검색 성능은 계산하지 않음.
- 실제 시도에서 반대 가설: 개별 지원→공동 양립(J5/J6 깨짐), 전판 공동 불가능(J7/J9 조건부 양성), 두 출력→두 플러그인 필요(M1 단독, D6 수동 저장), 파일 생성→기능 정상(B4/B5/J12), 규정→사건(A5 자료 1개 누락). 조건별로만 변경. 
- 미확인 핵심: 자연 모집 240행, S2 엄밀한 OR 보충 1자리, 초기 편집 이력 14건, 자연 2-link 공동성공 1종, 정확판 공동실행 0건, 교육 실제 이수 1종, PDF screenshot 4회 실패, Smithsonian 3 URL 실패. 별도 소스 클릭 로그 및 원장 일부 누락. B1 관련 #463 원문 계보 미판독.
- 실행 명령 및 입력 준비 게이트 RESULT의 추가 분석에 기록. exact release tuple과 최소 fixture가 확보되기 전 실제 빌드 검증을 위임하지 않음. 저장소 검사 필요 시 checkout 후 `git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..HEAD`, `git diff --check 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..HEAD`, `python scripts/check.py --require-git` (실행 안 함).

## 원격 재열람
- ① bf28e0e49d9d0f057eedc1c9a629490516b9d1d9 SCOPE, blob f3378b0d02bc803ebf2dd9f3db533ec2e6ca42ab.
- ② ba814d1654d6234e69e292e8a015646e11f86b1f frame, f324ae8d860c3fdedb1fc263788b0c91c1b7ef0d; c956ae7863360883be0f8ab4f318ae875fff2239 query_frame, b37a6343efc01d159fb0de52ac8861b01c431a87; cd231622415bb36a963f90fb846cd0d3b4330aed requirements, 449aca47ccc02db7e3f7ef464c0f4505a5736ec0; d159d6ca537a9c5c1c7e7b7e1cc6832de6a6c30a sources, e2c13acd82d9247d8287d651e7397b59f55eb09c.
- ③ 41e8d6fedfd1581a5a5f92aa811629c28be60ea9 sources, 9f3ddd470f04247f76a3d613e4584113b35abc93; 4463c11d1a904ee39b31c25a4951b50c56fec484 requirements, 294ff0e72890f58cd30338dd90047a0302c9b7f5.
- ④ 90ae5e6d49330dcc284265b95d6b11d9048607cc sources, 334015c77a86b1402bdfb790240488a9a297544a; 7c3c8fd20b3ce593e0d81479983adbd1c8798e57 combinations, 37627993661456b33509cd2779f3d3f0a095c0c2; a46a86f9c9dbbb7c001aa5a27db3315a24f38e43 responses, a33535f355947bb6fb163951d68ff514fb2600fb; b7eb4254d3ad879fc216df47c5ece733cf72aa3a SCOPE 보정, e175b39d4bb9263aa5967d320aa39527353c3936.
- ⑤ f577ce10ff9a9720d54dde4f9a8c68e66077b386 RESULT, 8b01b725490592df36994c1339353e158b3cc54e. RESULT 행 14/20/16, 3 약점 확인.
