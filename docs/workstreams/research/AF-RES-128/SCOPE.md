# AF-RES-128 SCOPE — 판독 전 동결

기준 5c0eca97d41e084a76bddd7cb0e976e5e9f792e8 (계획 4a92e22c5356dc7ea2b715f671077e8ab63b2835). 지정 브랜치 생성 확인. 통합 AGENTS/STATE/START_HERE/RESEARCH_BRIEF/RESEARCH_WORKFLOW/DOT_AUTOMATION 열람; dot-control 파일은 contents 빈 응답으로 blob 71a6140048f6d33851acd56356ca726ebbca0c94를 도구 내부 파싱해 128 RUNNING, depends_on 124 DONE, result_commit 0c1b5733c8ddc76341c6da872e8b405e6ed38963 확인. 124 HANDOFF/RESULT/score는 봉인 뒤 읽음. 결과 입력 7dd19f7fdac69b9dad4d6170ea247580b857f9b4, 요청·면 보관판 de99023970ca060e8227594c41448e6938efed23. 사전 노출: 지시문·위 상태와 파일 스키마 및 행 수·해시 집계만. 채점·결과 본문 미열람. 동일 모델의 다른 작업 기억은 사례별 판정 자료로 사용하지 않는다. 원격 GitHub 커넥터로 읽고 씀; git ls-remote는 DNS 실패, checkout/정식 session CLI 미실행.

## Q1 투영
- prior/after-first/final에서 case_id로 조인만 하고 answer 문자열만 출력. packets의 자연층 issue_body를 같은 사건에서 고정(중복 본문 동일성 확인). trails의 실제 anchor_url, offset/end/characters 및 stage만 조인; 원답 0, 첫 답 첫 면, 최종 실제 열린 면 전부. 행을 열람 결정과 구별(좌표가 일치하는 면만 포함, 중복/누락 시 차단). natural-views의 body를 정확히 연결, codepoint 길이·end-offset·FNV1a 32비트(각 Unicode codepoint XOR, 곱 16777619, 초기 2166136261)를 검사. 보관판 56/56 길이 및 FNV 일치(도구 내부 계산). 원 요청 본문 자체에 들어 있는 링크/정보는 원 요청이므로 보존.
- 판독 화면 허용 키 id/request/answer/views[].id,body만. 링크 미리보기·타 답·case_id·stage·group·change·confidence·provisional_self_assessment·score·gold·선택 이유·사후 출력 금지. 본문 안에 있는 URL은 자료 자체이며 숨기면 원문을 바꾸므로 별도 명시. 원 요청 및 면수/답 문구 재등장으로 단계/사건 유추 가능. 독립 세션 18개가 아니며 독립 사람 평가 아님. 판독자에게 답 하나씩 반환하고 판정 후 다음 답. 노출 의심은 분리.
- 정렬된 case_id × (prior,after-first,final) 배열에서 LCG seed 1282026, state=(1664525*state+1013904223) mod 2^32, Fisher-Yates 뒤에서부터 j=state%(i+1), 결과 순서 B01..B18. 타이브레이크 원문 URL 사전순, 짧은 구간 우선; Q5는 동일 판/동일 입력/보존/예외 직접성 우선, 짧은 구간 다음 URL. 실제 단계는 봉인 뒤 복원.

## Q2 판정
주장 단위 O(조작/대상), P(필수 보존값), V(판/입력/예외), E(실행 또는 확정 진술). Q: 작성자 사실(문제/원하는 값 자체만; 동작 입증 아님), H: 가설/조건부 처방, X: 실행 확인 진술(당시 면에서 입증 필요). 주장별 D 직접 지지, C 조건부/일부, R 명시 반박, U 근거 공석. 질문이 원하는 값과 실제 동작은 다른 축. 면이 없는 원답의 처방은 정확해 보이더라도 D가 아님. 의도/보존/예외 원자화; 독자가 하지 않은 주장도 필수 공석으로 기록. 판정 4등급 F=필수 조건 전부 직접 지지, P=일부 지지와 필수 조건 공석(핵심 유보 없고 확정도 없음), H=핵심을 명시 유보(부분 지지와 공존하면 H 우선, 지지축 별도), O=필수 미지지/반박된 처방을 확정하거나 실측을 근거 없이 주장(O는 H/P보다 우선; 단 'try' 등 제안 자체를 확정으로 간주하지 않음). 답 전체에 정확성 축은 개봉 뒤 별도 판정; 현재는 근거 충분성만. D/C/R/U 및 발화 태도 분리.

## Q3–Q7 규칙
봉인 뒤만 124 HANDOFF/RESULT/scores/assignments/projection-remote-check와 작성자 실제 원문을 연다. 6×3 복원, 기존과 새 등급 정의 차이 표시. 두 탐색 경로 사건당 각각 3개 이하 본문: 동판 공식 문서→구현/시험, 원 요청→첨부/연결 예/이력. 같은 저작 여러 절은 하나. 22개 이상(6 질문/6 정의·구현/6 독립 시험·예/각 분야 2). F 고정, F+O 실제 둘째, F+N 새 둘째; 각 면 최대 1500 Unicode codepoint, 두 면 3000, 연속 구간, 3회째 제외. O/N 공석은 0자와 구별. 최소 두 음성 대조(판/방향/예외), 한 F 충분 주장, 한 다른 경계 민감도; 독자 응답 추측 금지. 작성자 입력의 존재와 동작 입증 분리, 사후 실행 소급 금지. 타 분야 판·매체/이조 악기 총보·파트 확인. 원문/후속 공개일 확인, 미확인 표시. 결과/자기검산/인계 모두 PARTIAL/BLOCKED 기준 엄수.

## 투영 소형 누출 시험 (실제 JS 실행)
입력에 view.score=999, anchor_url=LEAK_URL, group=LEAK_GROUP을 심음. 투영 출력: {"id":"B00","request":"request","answer":"answer","views":[{"id":"E1","body":"allowed"}]}. 허용 키·금지 표지 검사: PASS. 가짜 score 등 금지 키를 top-level에도 넣더라도 명시 생성만 허용하는 방식. 구조적 필드 가림만 입증, 본문 의미 노출·독립 판단은 보장하지 않음. 다음으로 실제 데이터 투영 검산.
