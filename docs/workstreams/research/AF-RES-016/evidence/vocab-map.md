# Q8 — 판정 어휘 대응 원장

**같은 철자의 상태도 먼저 ‘무엇에 대한 판단인가’를 확인해야 한다.** 동일성, 특정 사용 방식의 요구 충족, 근거의 충분성, 분야 간 전이, 질의별 검색 관련성은 서로 다른 술어다. 원래 값은 보존하고 필요한 경우에만 비교 목적의 해석을 덧붙인다. 아래 대응은 연구자의 해석이며 공통 스키마나 자동 변환기를 확정한 결과가 아니다.

## 1. 읽은 입력과 실제 어휘

지정 일곱 HANDOFF와 아래 V01–V18의 고정 본문·코딩 자료를 직접 읽었다. URL·SHA·절·확인 내용·한계는 [vocab-sources.json](vocab-sources.json), 실제 값과 분모는 [vocab-inventory.json](vocab-inventory.json)이다. 방법/정의 문서와 고정 판정 자료라는 두 종류를 대조했다. 이 18개는 새 외부 방법·체계 문헌 25개에 더하지 않는다.

- 004의 실제 네 라벨은 `DIRECT_DOCUMENTED`, `CONDITIONAL_TRANSFER`, `SURFACE_OR_CONSTRAINT_MISMATCH`, `INSUFFICIENT`다. brief의 `DIRECT / CONDITIONAL / VIOLATION`은 이 고정판의 저장 enum이 아니다. `VIOLATION`은 표면적 작동 관계 불일치까지 담는 실제 첫 라벨을 좁게 오해하게 할 수 있다. [V06–V07]
- 001의 실제 입력 표현 키는 `A_free_text`, `B_light_structure`, `C_ai_decomposition_proposal`이다. brief의 IN-A/B/C는 이 대응표에서 쓰는 읽기용 별칭이다. 표현의 종류이지 성공·실패 상태가 아니다. [V01–V02]
- 003은 `관련`보다 정확히 **관련됨**이라고 쓰며, 같음·관련됨·보류 정의는 RESEARCH §3.2에 있다. §5는 보존해야 할 의미를 정리한다. [V04]
- 002의 유지·보류·중단은 문장 속 탐색 행위다. 이 작업이 정식 상태 enum을 제정했다고 읽지 않는다. [V03]

## 2. 필수 형식 대응표

‘조건부 대응’은 문제·대상·사용 방식·설정·근거가 같을 때의 좁은 해석이다. `없음`은 해당 원문 의미에 관한 추가 미확인이 없다는 뜻이며 제품 검증을 뜻하지 않는다.

| 작업 | 어휘 | 답하는 질문 | 대응 어휘(다른 작업) | 같은 것으로 읽으면 안 되는 이유 | 근거 위치 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | IN-A/B/C; 실제 A_free_text / B_light_structure / C_ai_decomposition_proposal | 입력을 어떤 표현으로 전달하는가(판정축 밖) | 003의 저장안 A/B/C와도 별도 | 001은 입력 표현, 003은 저장 원리다. 알파벳이 같아도 상태나 우열이 아니다. | V01 RESEARCH §3; V02 cases[*].formulations | 없음 |
| 001 | 미입력 / 명시적 모름 / 아직 미정 / 해당 없음 / 명시적 무제약 / 상충 | 근거 충분성에 앞선 입력 의미·결정 상태 | 011 absent / explicit_unknown / undecided / not_applicable는 일부 대응 | 빈칸은 무제약이 아니며, 미정은 무지와 다르고, 상충은 단순 결측이 아니다. 004 INSUFFICIENT로 일괄 변환하면 원인이 사라진다. | V01 RESEARCH §5 | 없음 |
| 001 | explicit / explicit_current / explicit_design / explicit_example / explicit_preference / explicit_unknown | 원문이 무엇을 어떤 지위로 명시했는가 | 011 정보 present 또는 질문시점/강제성 필드에 조건부 연결 | explicit은 제품 사실의 검증이 아니다. 계획·예시·선호를 현재 가동·필수로 바꾸지 않는다. | V02 cases[*].formulations.C_ai_decomposition_proposal.input_read_back[*].reading_status | 없음 |
| 001 | interpretation | 누가 원문을 해석한 문장인가 | 003 연구자 해석; 010 H 연결 해석 | 사용자 명시 요구나 검증된 적합성 라벨이 아니다. 18개 제안 중11개에서 사용했다. | V02 proposals[*].status; K05.P1 | 없음 |
| 001 | proposal_unconfirmed; user_confirmed=false | 제안이 사용자 확인을 받았는가 | 002 조건부 후보와 모두 ‘채택 전’이나 직접 동치 없음 | 미확정 제안은 근거 부족을 뜻하는004 INSUFFICIENT와 다르다. 문서 근거가 있어도 사용자 확인은 없을 수 있다. | V02 proposals[*]; K02.P2 | 없음 |
| 001 | proposal_requires_constraint_change | 현재 조건을 유지한 해법인가, 조건 변경을 가정한 새 안인가 | 004 현재 사용 방식의 H fail과 관계하나 라벨 자동 대응 없음 | 제안을 검토할 수 있다는 사실로 현재 요구의 충족 판정을 살릴 수 없다. K05.P3은 현재 입력을 변경해야 한다. | V02 cases[id=K05].formulations.C_ai_decomposition_proposal.proposals[id=K05.P3] | 없음 |
| 002 | 조건부 후보로 유지 | 탐색을 계속할 가치가 남는가 | 012 1로 투영한 사례; 004 INSUFFICIENT/CONDITIONAL_TRANSFER와 조건부 관련 | 유지에는 부족한 설정, 부분 유용성, 검토할 완성품이 섞인다. 완성품 유지가 직접 적합 확정은 아니다. | V03 RESEARCH §1·§3; V14 선행입력 투영표 | 없음 |
| 002 | 완성품 판정 보류 / 원리 참고로 남김 | 어느 역할의 판단을 보류하고 무엇을 계속 다룰 수 있는가 | 004 역할·사용 방식별 별도 행; 012 1 또는 미판정 | 하나의 후보에 대한 전면 보류가 아니다. Outpost의 팀 완성품 판단과 원리 참고는 범위가 다르다. | V03 RESEARCH §3, P2 완성품 행 | 없음 |
| 002 | 중단 | 이 발견 경로의 추가 검토를 왜 멈추는가 | 012 Jiandu P1.w의 명시0 | 접근·평가 조건 때문에 멈춘 것과 기능 위반N은 다르다. 반복 정보에 따른 탐색 중단도 후보 부적합이 아니다. | V03 RESEARCH §3·§7; V15 P1.w/jiandu | 없음 |
| 003 | 같음 | 두 기록은 어떤 범위에서 같은 대상을 가리키는가(동일성) | 직접 대응 없음; 같은 대상 ID의 조건부 연결 | 004 DIRECT_DOCUMENTED나012 2는 요구 적합성이다. 이름 변경·같은 제품 귀속이 버전/배포/기능 호환성을 보증하지 않는다. | V04 RESEARCH §3.1–3.2; V05 C01·C03 | 없음 |
| 003 | 관련됨 | 부분·포크·후계·설명·유사 원리 중 어떤 관계인가(동일성/관계) | 010 mapping이나012 1은 특정 목적에서만 부분 대응 | 관련 대상이라는 이유로 같은 속성을 복사하거나 검색 관련성을 부여하지 않는다. 관계가 모르면 관련됨으로 채우지 않는다. | V04 RESEARCH §3.2; V05 C03·C06 | 없음 |
| 003 | 보류 | 같은가 다른가를 가를 식별 근거가 충분한가 | 004 INSUFFICIENT와 ‘미결정’이라는 상위 특성만 공유 | 003은 동일성 술어, 004는 제안 사용 방식의 판정이다. 같은 대상인지 몰라도 특정 원리의 참고가 가능하고 그 역도 가능하다. | V04 RESEARCH §3.2; V05 C04 | 없음 |
| 003 | 미귀속 | 이전 근거가 분리된 어느 대상에 속하는가 | 001 원문–해석 참조, 004 E unknown과 조건부 관련 | 근거의 소유 대상이 불명한 상태이며 주장 자체가 거짓이라는 뜻이 아니다. 옛 ID를 한쪽으로 조용히 옮기지 않는다. | V04 RESEARCH §7 | 없음 |
| 004 | alternative / component / reference | 이 행은 후보를 어떤 사용 방식·역할로 제안하는가 | 011 product/component/principle; 012 corpus role과 조건부 대응 | alternative는 문제 상대적 대체 역할이다. product는 답 또는 산출물 형태 분류다. 앱도 reference가 될 수 있고 부품도 선택 부분의 직접 대안이 된다. | V06 판정 단위; V07 rows[*].role | 없음 |
| 004 | L: ok / broken / missing | 근거 위치를 찾을 수 있는가(근거 충분성의 연결 전제) | 011 accessible/redirected/failed/not_linked와 좁게 대응 | 접속 성공은 주장 뒷받침E나 요구 충족H가 아니다. blocked는 실제 broken으로 바꾸지 않는다. | V06 네 판단축; V11 §6 | 없음 |
| 004 | E: supported / contradicted / unknown | 특정 주장과 조건을 원문이 지지하는가(근거 충분성) | 011 E 반박은 참여자의 반박 사건 | 011의 E 코드는 연구자가 외부 사실 오류를 검증했다는 값이 아니다. unknown도 contradicted와 다르다. | V06 네 판단축; V11 §5 | 없음 |
| 004 | H: pass / fail / unknown / not_in_scope | 제시한 사용 방식은 각 필수조건을 만족하는가(적용 가능성) | 011 H 반박; 012 2/N과 조건부 연결 | pass는 평가 범위의 문서·논리 판단이다. not_in_scope는 최초의 좁은 참고 범위이며 실패한 전체안을 사후 면제하는 값이 아니다. | V06 네 판단축·v1.1; V07 rows[*].H | 없음 |
| 004 | T: not_needed / mapped / analogy_only / unknown | 분야 간 관계·연결·실패 조건이 설명되는가(전이) | 010 같은 T값과 같은 정의 | mapped는 최종 라벨이 아니다. 전이 대응이 명확해도 옮긴 사용 방식이 필수조건을 위반할 수 있다. | V06 T축; V09 RP1-B09-M; V10 RP2-C05-M | 없음 |
| 004 | DIRECT_DOCUMENTED | 이 구성의 필수조건에 긍정 문서근거가 있는가(적용 가능성+근거 충분성) | 012 2, 동일 구성·범위를 보존할 때 | 실제 실행·통합 성공이 아니다. 다른 구성이나 부분 질문으로 이동하면2를 그대로 복사하지 않는다. | V06 기대판정4종; V07 R01·R02; V14 투영표 | 없음 |
| 004 | CONDITIONAL_TRANSFER | 좁은 참고 관계·연결·비적용·실패 조건을 구체화했는가(전이) | 010 같은 라벨; 012 주로1, P04.2의 ct-merkle은2 | 미확인 필수전제를 ‘조건부’로 넘기는 라벨이 아니다. 질의가 좁아지면 검색등급은 달라질 수 있다. | V06 기대판정4종; V07 R17; V15 P04.w/P04.2 | 없음 |
| 004 | SURFACE_OR_CONSTRAINT_MISMATCH | 표면만 닮았거나 결정적인 알려진 요구 위반이 있는가(적용 가능성) | 010 surface_false_positive/near_miss; 012 N과 좁게 대응 | 표면 관계 불일치와 근접한 후보의 필수조건 위반을 함께 담는다. 전부 실제 사용자 거절 사건인011 근접오답과 같지는 않다. | V06 기대판정4종; V09–V10 buckets; V11 §5 | 없음 |
| 004 | INSUFFICIENT | 결정에 필요한 사실·설정이 부족하며 답에 따라 판단이 달라지는가(근거 충분성) | 010 동일 라벨; 012 1/0/미판정 중 범위에 따라 다름 | 알려진 결정적 위반은 제외한다. R05는 저장 없는 core의 부분 유용성만012에서1이다. 후보 전면 실패나 검색 관련성0을 뜻하지 않는다. | V06 기대판정4종; V07 R05·R09; V14 투영표 | 없음 |
| 010 | mapped + CONDITIONAL_TRANSFER | 대응한 관계를 좁은 설계 참고로 쓸 수 있는가(전이) | 004 동일 조합 | 원저자 역사적 전이 보고와 이번 대상의 실제 적용은 다르다. reference_design과 runtime_observation을 보존해야 한다. | V08 판정 방식; V09–V10 judgments | 없음 |
| 010 | mapped + SURFACE_OR_CONSTRAINT_MISMATCH; near_miss | 관계는 대응해도 이 사용 방식이 고정 조건을 깨는가(전이+적용 가능성) | 004 H fail; 012 N과 조건부 대응 | mapped를 적합으로 승격하면 반례3개를 뒤집는다. RP1-B09-M은 재시작 때 재허가, C08은 정당한 수정 절제, C05-M은 작은 충돌 무음삭제다. | V09 RP1-B09-M; V10 RP2-C08·RP2-C05-M | 없음 |
| 010 | analogy_only; surface_false_positive | 어휘 유사성 밖에 대응 관계가 있는가(전이) | 004 T analogy_only 및 mismatch의 일부 | 관계 미성립과 근거 부족unknown은 다르다. P2 C07의 동일인 판별은 이미 같은 ID인 수정 충돌 해법이 아니다. | V09 RP1-B07; V10 RP2-C07 | 없음 |
| 010 | new_candidate / rediscovery / technical_support / insufficient | 이번 탐색에서 어떤 발견 종류인가(검색 과정 메타데이터) | 012 origin=new/transfer와 직접 대응 없음 | new_candidate는 소프트웨어 발명·좋음 점수가 아니다. rediscovery도 유용할 수 있으며 발견 경로와 적용 판정은 별도다. | V09–V10 judgments[*].bucket | 없음 |
| 010 | implementation_H=unknown; runtime_observation=not_performed; conditional_reference | 대상 구현을 실제 확인했는가, 어느 참고범위인가(근거 충분성/적용 범위) | 004 reference_design 및 runtime_observation=not_performed | 원 분야 관계의 mapped와 대상 구현의 unknown은 공존한다. 조건부 참고는 실제 운영pass가 아니다. | V08 판정 방식; V10 RP2-C05·RP2-C06·RP2-C05-M | 없음 |
| 011 | whole / part; product / component / principle / mixed | 질문이 선택하는 범위와 답이 내놓는 대상의 역할은 무엇인가(판정축 밖) | 004 proposed role, 012 corpus role과 조건부 대응 | 질문의 크기·프로젝트 설명 길이·답의 산출물 형태가 다르다. mixed는 제품이 여러 개라는 이유만으로 부여하지 않는다. | V11 §1.1·§4; V12 answers[*].role | 사람 간 재현성 미확인(별도 사람 코딩 필요) |
| 011 | FIT / TRADEOFF / PERSONAL_USE / CROSS_DOMAIN | 답에 조건 대응·한계·사용경험·분야 연결이 표현됐는가 | 004 E/H/T의 입력 근거로 활용 가능 | FIT는 실제 H pass가 아니고 CROSS_DOMAIN은 mapped가 아니다. PERSONAL_USE도 이 문제에서의 통합 성공이 아니다. | V11 §4·v1.3 | 없음 |
| 011 | accepted=true/false/null; top_voted=true/false/null | 게시물의 채택표·최고점 표식을 관측했는가(반응 관측) | 직접 동치 없음 | accepted false와 null은 다르다. 채택된 게시물 안 일부 방안이 거절될 수 있으며 최고점은 질문자의 선택이 아니다. | V11 §4·v1.3; V12 T027 | 없음 |
| 011 | adopt / reject / try / thanks / none / unknown | 질문자가 무엇을 말했다고 관측했는가(반응 관측) | 004 적합성 라벨,012 등급과 직접 동치 없음 | 감사·시험 의향은 채택이 아니고 무응답은 거절이 아니다. adopt의 식별·계획·진행·보고된 사용·통합 단계를 별도로 유지한다. | V11 §4·v1.3; V12 outcome·adoption_stage·trial_stage | 관측 밖 사용 결과 미확인(후속 사용자료 필요) |
| 011 | L / E / H / T 반박; SURFACE_OR_CONSTRAINT_MISMATCH | 실제 반박의 이유와 추천시점 필수조건은 무엇인가 | 004 축의 질문에 대응하나 값의 자료유형이 다름 | 참여자의 반박 관측을 연구자의 기능검증으로 바꾸지 않는다. 엄격 근접오답에는 조건·시점·발화자·특정 방안의 연결이 필요하다. | V11 §5·v1.3; V12 near_misses/rejection_codes | 제품 사실의 참 미확인(당시 버전 근거 필요) |
| 011 | M / C / P / LIC / TRUST / UX / EXP / OTHER | 유지보수·커뮤니티·가격·사용권·신뢰·편의·경험·기타 선택 이유인가 | 004 H에 포함되는 것은 추천 전에 필수였을 때만 | 사후의 선호·비용 이유를 모든 경우H로 흡수하면 원래 요청을 바꾼다. 같은 이유도 긍정·부정 방향이 다를 수 있다. | V11 §5 | 없음 |
| 011 | present / absent / explicit_unknown / undecided / not_applicable / unknown; I1 captured | 정보가 어떻게 드러나거나 빠져 있는가(근거 충분성의 입력 상태) | 001의 미입력·모름·미정·해당없음과 좁게 대응 | absent는 열람 범위의 부재, unknown은 노출·시점 불명이다. captured는 연구자의 URL 확보이지 질문의 충실성이다. | V11 §1–2 | 없음 |
| 011 | accessible / redirected / archived / failed / blocked / not_linked | 현재 단회 열람에서 링크에 무엇이 관측됐는가 | 004 L의 일부 근거 | blocked와failed를 같은 링크 소실로 취급하지 않는다. archived가 모든 설치의 중지나 근거 무효를 뜻하지 않는다. | V11 §6; V12 link_status_now | 지속 상태 미확인(다른 시점 재관측 필요) |
| 012 | product / component / principle / other | 자료집 항목을 어떤 산출물/역할군으로 집계하는가(판정 메타데이터) | 011 role과 일부 겹침,004 role과 조건부 연결 | 자료당 한 역할은 질의별 기여와 다르다. role은 검색어에 쓰지 않았고,other도 자동 무관 판정이 아니다. | V13 대상과 대표 주소; entries.jsonl.role | 없음 |
| 012 | 2 | 이 질의·대상·요청 역할의 필수조건에 문서화된 경로가 있는가(검색 관련성) | 004 DIRECT_DOCUMENTED가 주 대응; 일부 좁은 CONDITIONAL_TRANSFER도 가능 | 전체 프로젝트 완성품에만 부여하지 않는다. 선택 부품이나manifest의 좁은 원리도2가 된다. | V14 판정 단위·투영표; V15 P04.2/ct-merkle | 없음 |
| 012 | 1 | 일부 기능·조건부 적용·전이·실패 경계가 유용한가(검색 관련성) | 002 조건부 유지;004 CONDITIONAL_TRANSFER 및 부분 INSUFFICIENT | 근거 부족 일반값도, 후보 형태 component도 아니다. 어떤 부분을 도울지 확인해야 한다. | V14; V15 P01.w/yjs·P04.w/ct-merkle | 없음 |
| 012 | N | 가까워 보이지만 이 질의의 구체 조건을 어기는가(검색 관련성+적용 가능성) | 004 mismatch의 근접조건 위반 일부;010 near_miss | 접근 실패·자료 부족만으로N을 주지 않는다. 011의 실제 반박 사건을 요구하지 않는 연구자 판정이다. | V14; V15 K02.w/paperless-ngx; V17 등급 정의 | 없음 |
| 012 | 명시 0 | 이 고정 근거에서 관련1/2나근접오답N을 주었는가(검색 관련성) | 직접 일대일 대응 없음 | Jiandu0은 평가·배포 근거 보류다. 다른0에는 제목·범주만 있는 경우가 있어 부적합 기능검증으로 읽을 수 없다. | V15 P1.w/jiandu·P04.2/borg; V17 등급 정의 | 새 근거 뒤 등급 미확인(대상 원문 보강 필요) |
| 012 | 미판정(행 부재); 평가에서 결손을0으로 처리 | 이 쌍을 명시적으로 판단했는가, 계산상 어떻게 다뤘는가(판정 범위) | 004 unknown/INSUFFICIENT와도 직접 동치 없음 | 계산용0과 의미상0/N은 다르다. 내부별도표에 없는 쌍도 해당 비교에서는 미판정으로 보존한다. | V13 고정 비교; V14; V18 | 개별 미판정의 실제 관련성 미확인(추가 판정 필요) |
| 012 | origin=transfer / new | 등급을 선행자료에서 옮겼는가, 이번에 작성했는가(출처 지위) | 010 new_candidate와 직접 대응 없음 | transfer는 분야 간 전이T가 아니라 판정의 출처다. new는 새로운 제품이나 원리를 발명했다는 뜻이 아니다. | V14 끝 문단; V15 origin | 없음 |

## 3. 다섯 질문을 분리한 행렬

`—`는 그 값이 직접 답하지 않는 질문이다. ‘조건부’는 원래 대상·설정·근거 범위를 고정해 추가 판정해야 한다는 뜻이다.

| 원래 어휘군 | 동일성 | 적용 가능성 | 근거 충분성 | 전이 | 검색 관련성 |
| --- | --- | --- | --- | --- | --- |
| 003 같음/관련됨/보류 | 직접 판단 | — | 식별 근거의 충분성만 | 유사 원리 관계가 있으면 별도 설명 | — |
| 001 입력/제안 상태 | 대상·원문 연결의 전제 | 제안과 현재 요구를 구별 | 정보·해석·확인 상태 | — | — |
| 002 유지/보류/중단 | — | 후보 검토 여부, 확정 아님 | 다음 확인이 필요한 이유 | 원리 참고를 별도로 유지 가능 | 탐색 행위, 등급 아님 |
| 004 L/E | — | 직접 판단 아님 | 연결/주장의 뒷받침 | 전이 주장도 E 대상일 수 있음 | — |
| 004 H 및 최종 네 라벨 | — | 특정 사용 방식·조건별 판단 | INSUFFICIENT 및 unknown 보존 | 조건부 전이 라벨은 T와 연결 | 고정 질의로 투영해야 함 |
| 004/010 T | — | mapped라도 H fail 가능 | unknown은 전이 설명의 미확인 | 직접 판단 | 관계가 질의에 필요한지는 별도 |
| 011 accepted/adopt/reject | — | 사람의 반응 관측, 사실 보증 아님 | 표식/반응의 노출 범위만 | — | — |
| 011 L/E/H/T 반박 | — | 참여자 반박의 분류 | 참여자 주장과 연구자 검증 구별 | 실제 전이 반박의 관측 | 엄격 근접오답과 별도 |
| 012 corpus.role | — | — | — | principle도 mapped를 뜻하지 않음 | 역할별 집계의 범주만 |
| 012 2/1/N/0/미판정 | 동일 ID 안에서도 달라짐 | 질의·역할 안에서만 반영 | 0과미판정·N을 구별 | 1이나2로 투영 가능 | 직접 판단 |

## 4. 일대일 대응을 깨뜨린 구체 사례

| 반증 시도 | 실제 입력 대조 | 결과와 제한 |
| --- | --- | --- |
| ‘부품은 부분 관련 1, 완성품은 직접 2’인지 확인 | V14 qrels NOTES; V15 P01.w 및 P04.2 | 012는 전체 질의에서도 정해진 부품이 요구를 충족하면 2를 허용한다. ct-merkle은 P04.w=1, P04.2=2다. 역할명만으로 등급을 만들 수 없다. |
| ‘같은 제품이면 같은 관련성’인지 확인 | V15 K02.1/K02.2/K02.w의 paperless-ngx | 각각 1/N/N이다. 중복 검사라는 좁은 도움과 처음 폴더 보존 위반은 서로 다른 조건이다. 후보의 고정 품질 차이가 아니다. |
| ‘mapped이면 유용한 조건부 전이’인지 확인 | V09 RP1-B09-M; V10 RP2-C08·RP2-C05-M | 25개 사용 방식 중 mapped는 13개이며, 그중 3개는 알려진 mismatch/near_miss다. 관계를 설명할 수 있다는 것만으로 좋은 사용 방식이 되지 않는다. |
| ‘004 INSUFFICIENT는 012의 0 또는 미판정’인지 확인 | V07 R05; V14 선행입력 투영표 | core의 지속 저장은 부족해도 부분 유용성만 1로 옮겼다. 판정 단위가 좁아졌음을 함께 저장해야 한다. |
| ‘0은 불합격 N’인지 확인 | V15 P1.w/jiandu, P04.2/borg·restic; V17 등급 정의 | 확인한 0 세 행은 평가 근거 보류·해당 기능 미확인이다. 기능이 불가능하다는 판정이 아니다. 0이 단일 원인을 가진 값도 아니다. |
| ‘accepted는 조건 충족’인지 확인 | V11 v1.3; V12 T027 | 게시물 채택과 그 안 특정 방안에 대한 반박이 함께 있다. T027의 전체 게시물 단위를 더 좁은 제안의 적합성으로 치환하지 않는다. |
| ‘보류는 한 가지 상태’인지 확인 | V04 §3.2 C04; V06 INSUFFICIENT; V03 Outpost | 식별 미확정, 결정적인 적용 근거 부족, 완성품 판정 보류 후 원리 참고 유지는 다르다. 공통 보류값으로 합치면 다음 확인 대상이 사라진다. |

위 수치는 전부 지정 고정 입력의 재집계다. 새 사람 코딩이나 새 제품 실행을 수행한 것으로 세지 않는다. 010의 25행은 자료 25개가 아니라 **사용 방식25개**다.

## 5. 조립할 때 보존할 최소 정보 — 연구자 제안(H)

공통 상태 하나로 바꾸기 전에 `원작업·원어휘 / 판단 대상 / 문제·선택 범위 / 제안한 사용 방식·설정 / 근거 수준·시점 / 판정자 / 미확인과 다음 확인`을 함께 둔다. 의미가 같은 부분만 새 표의 열에 투영하고 원래 값을 덮어쓰지 않는다. 역할·판정·반응·자료의 출처 지위는 서로 독립된 정보다.

예를 들어 `003:보류`를 받으면 다음 확인은 동일성 근거다. `004:INSUFFICIENT`를 받으면 다음 확인은 판정을 바꾸는 구성/기능 근거다. `012:미판정`을 받으면 해당 질의–자료 쌍을 판정한 기록부터 필요하다. ‘다음 무엇을 확인해야 하는지’가 보존되지 않는 대응은 같은 것으로 취급하지 않는다.

## 6. 한계

이 표는 일곱 고정 연구의 어휘 대조다. 외부 전체 분류 표준이나 제품 DB를 정하지 않는다. 작성자가 만든 기대 판정·실제 대화 반응의 코딩·검색 qrels를 구별했고, 그 셋을 사람 정답·실제 기능·현재 운영 보증으로 승격하지 않았다. 001/002는 Q8에만 사용했다. 003의 URI·SKOS·PROV·FRBR 문헌을 다시 조사하지 않았다. 어휘 대응의 설계자 판단 개선 효과는 미측정이며, 다음 확인은 동일 사례에서 판정 대상·범위를 복원하는 독자 과제다.

## 7. 재현

저장소 루트에서 `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/vocab-inventory.py`를 실행한다. 입력은 스크립트에 고정한 일곱 SHA다. 출력은 이 폴더의 vocab-inventory.json뿐이며 원판정 파일은 수정하지 않는다. 실제 실행은 종료 0; 004 18행, 010 25행, 012 초기 235행·별도 277행을 확인했다.

## 8. 고정 출처 주소

| 출처 ID | 종류 | 직접 읽은 고정 원문 |
| --- | --- | --- |
| V01 | prior_research_analysis | [AF-RES-001 RESEARCH.md](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/RESEARCH.md) |
| V02 | fixed_research_coding | [AF-RES-001 CASES.json](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/CASES.json) |
| V03 | prior_research_analysis | [AF-RES-002 RESEARCH.md](https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/RESEARCH.md) |
| V04 | prior_research_protocol | [AF-RES-003 RESEARCH.md](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md) |
| V05 | fixed_research_case_analysis | [AF-RES-003 CASES.md](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/CASES.md) |
| V06 | prior_research_protocol | [AF-RES-004 PROTOCOL.md](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md) |
| V07 | fixed_research_coding | [AF-RES-004 EXPECTED.json](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/EXPECTED.json) |
| V08 | prior_research_case_analysis | [AF-RES-010 TRANSFER_CASES.md](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/TRANSFER_CASES.md) |
| V09 | fixed_research_coding | [AF-RES-010 evidence/p1-judgments.json](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/p1-judgments.json) |
| V10 | fixed_research_coding | [AF-RES-010 evidence/p2-judgments.json](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/p2-judgments.json) |
| V11 | prior_research_protocol | [AF-RES-011 CODEBOOK.md](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CODEBOOK.md) |
| V12 | fixed_observational_coding | [AF-RES-011 CASES.json](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CASES.json) |
| V13 | prior_research_protocol | [AF-RES-012 corpus/RULES.md](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/corpus/RULES.md) |
| V14 | prior_research_protocol | [AF-RES-012 qrels/NOTES.md](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/NOTES.md) |
| V15 | fixed_research_coding | [AF-RES-012 qrels/qrels.tsv](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/qrels.tsv) |
| V16 | fixed_research_coding | [AF-RES-012 qrels/independent.tsv](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/independent.tsv) |
| V17 | prior_research_protocol | [AF-RES-012 qrels/INDEPENDENT_REVIEW.md](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/INDEPENDENT_REVIEW.md) |
| V18 | prior_research_protocol | [AF-RES-012 qrels/REVIEW_PROTOCOL.md](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/REVIEW_PROTOCOL.md) |
