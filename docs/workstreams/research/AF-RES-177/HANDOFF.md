# AF-RES-177 HANDOFF

**작업자 판정 PARTIAL · 수용 상태 REVIEW_REQUIRED (독립 검토 미실시)**

시도 1, 웹 ChatGPT 작업자. 저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-177`, 소유 경로 `docs/workstreams/research/AF-RES-177/`. 계획 통합 `53eaa286136019510f052179f5f51d901bdac858`, 실제 시작 `2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc` (ahead 2, 관련 변경 진행표). 선행 고정 [AF-RES-146 HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/9bf267b71a0000aae5f098e82eab3f84c0dd7714/docs/workstreams/research/AF-RES-146/HANDOFF.md) 직접 열람. 작업자 COMPLETE / REVIEW_READY와 배정문에서 준 중앙 DONE은 구분. 최신 진행표 전체 본문 크기 제한, latest patch의 177 RUNNING/depends_on/경로 확인, 146 중앙 행 직접 확인 못 함. dot-control.json 수정 없음.

## 설계 판단에 넘기는 내용
- [RESULT](RESULT.md) 표1 14행(자연 후보 10+보충 4), 표2 20, 표3 16(자연10+보충4+구성2). 최초 원문 논리와 후속 관측을 분리. M1은 단독 core 설정 해결 보고, B2 명시 OR, S3 시간범위, S4 부정 조건. 원저자 확인 없는 정확도 계산 없음.
- 부분 지원이 둘이어도 공동 양립은 별도 근거가 필요. C14/J5 print-site+privacy 두 순서에도 asset 누락, C15/J6 PDF 성공 뒤 outline 실패. C16/J7 동일 config 유지자 양성 보고, 원작성자가 제공 PDF sidebar outline 확인(본문 TOC 아님); C17/J9 다른 사용자의 fork 우회. 정확 버전·산출물 직접 재현은 없음.
- [sources.jsonl](sources.jsonl) 62 기록행, counted 40 고유 저작/판/원 사건, 33 계보(자연 10, 보충 4, tagged docs 8, 추가 이슈/토론 11, 교육 2, 기록관 5). 원장 미포함 검색/재시도 있어 전체 클릭 수 아님. A5 실제 NARA 인수 보고 138 데이터+137 전자 문서, 275 파일; 규정과 사건 구분. 교육 실제 이수 미확인.
- 제안: goal/expression/scope/source span/followup event; 각 후보의 per-atom evidence와 same-build composition evidence 별도. unknown은 wildcard 아님. OR는 한 branch로 충분, AND는 동일 범위와 조합 근거 요구, priority/IF/NOT 유지.

## 원격 커밋과 확인

| 묶음 | 커밋 SHA | 대표 파일 및 원격 blob |
| --- | --- | --- |
| ① 사전 계약 | bf28e0e49d9d0f057eedc1c9a629490516b9d1d9 | SCOPE.md f3378b0d02bc803ebf2dd9f3db533ec2e6ca42ab |
| ② 모집 | ba814d1654d6234e69e292e8a015646e11f86b1f | frame.csv f324ae8d860c3fdedb1fc263788b0c91c1b7ef0d |
| ② 검색원순번 | c956ae7863360883be0f8ab4f318ae875fff2239 | query_frame.csv b37a6343efc01d159fb0de52ac8861b01c431a87 |
| ② 초기 판독 | cd231622415bb36a963f90fb846cd0d3b4330aed | requirements.csv 449aca47ccc02db7e3f7ef464c0f4505a5736ec0 |
| ② 초기 출처 | d159d6ca537a9c5c1c7e7b7e1cc6832de6a6c30a | sources.jsonl e2c13acd82d9247d8287d651e7397b59f55eb09c |
| ③ 직접 자료 | 41e8d6fedfd1581a5a5f92aa811629c28be60ea9 | sources.jsonl 9f3ddd470f04247f76a3d613e4584113b35abc93 |
| ③ 후속 분리 | 4463c11d1a904ee39b31c25a4951b50c56fec484 | requirements.csv 294ff0e72890f58cd30338dd90047a0302c9b7f5 |
| ④ 인수 반례 | 90ae5e6d49330dcc284265b95d6b11d9048607cc | sources.jsonl 334015c77a86b1402bdfb790240488a9a297544a |
| ④ 조합 | 7c3c8fd20b3ce593e0d81479983adbd1c8798e57 | combinations.csv 37627993661456b33509cd2779f3d3f0a095c0c2 |
| ④ 응답 | a46a86f9c9dbbb7c001aa5a27db3315a24f38e43 | responses.csv a33535f355947bb6fb163951d68ff514fb2600fb |
| ④ 범위 보정 | b7eb4254d3ad879fc216df47c5ece733cf72aa3a | SCOPE.md e175b39d4bb9263aa5967d320aa39527353c3936 |
| ⑤ 결과 | f577ce10ff9a9720d54dde4f9a8c68e66077b386 | RESULT.md 8b01b725490592df36994c1339353e158b3cc54e |
| ⑤ 자기점검/결과 고정 SHA | c497934b4ee9c840fa4f3105741ef80dc9b39242 | SELF_CHECK.md 76bab5ec88f140cbd4550c780ac20d6a65ec08d5 |

각 대표 파일을 GitHub fixed commit에서 재열람. RESULT 14/20/16 및 Q1–7, 약점 3행; SELF_CHECK 및 source count 확인. GitHub compare 실제 시작→결과 SHA: ahead 13 behind 0, 변경 9개 파일 모두 소유 폴더. 마지막 HANDOFF 커밋은 자기점검 후 별도 생성; 자신의 SHA를 파일 내부에 자기참조하지 않고 이 결과 SHA로 고정.

## 미충족 및 다음 첫 행동
- frame 281행: 14 포함, 27 제외/보조, 240 미판독. earliest 5×2 확정 못 함. 최초 수정 전 판 14건 미확인. S2 명시 OR 보충 1건 미달. 원작성자 최종 요구 확인 미완료. 자료 원장 일부 검색/재시도 누락. 교육 실제 이수 사건 미확보, UTA PDF 페이지 screenshot 4회 timeout, Smithsonian 3 URL 접근 실패. 같은 정확 설치판·공동 산출물 직접 검증 0건. 자연 표본에서 두 링크 필수와 공동 성공 동시 확인 0건.
- 첫 재개: [frame.csv](frame.csv) 미판독 240행을 기간별 공식 검색/원 이슈 원문으로 재검토. MkDocs #2241, mdBook #828 이전 eligible 중 더 이른 사건부터 정렬·동률·제외 기록 확정, mdBook #463 계보 및 explicit OR 보충 별도 확보. 원저자 변경 전 구절/후속 답 확인. 그 뒤 J5/J7의 고정 fork 및 정확판 두 개를 확보한 경우에만 공동 출력 시험으로 전달.
- 실행 미실시: checkout에서 `git diff --name-only 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..HEAD`, `git diff --check 2ca38b464dcf72fc2570d77f44cc29ee7c9a4cbc..HEAD`, `python scripts/check.py --require-git`. 제품 검사는 RESULT.md 추가 분석의 최소 문서, 설정 순서, expected artifact 및 명령 참조. 정확판 및 lock 미확보라 실행 위임 전제 미충족. 실제 제품·저장소 검사 성공 주장 없음.

색인 제안 한 줄 — AF-RES-177 PARTIAL: 요구 논리/범위와 조합 양립 별도 gate, 10+4 잠정 원요청·40 고유 원자료·20 조합·16 응답; print/privacy 및 PDF/outline 실패와 조건부 양성, 모집 및 공동판 확인 남음.
