# GLOSSARY — 통일 어휘와 근거 수준

## §1 읽는 원칙과 보존 범위

같은 문자열부터 합치지 않고 **무엇을 판단하는 말인지**부터 구분한다. 원 값·대상·문제·제안한 사용·설정·근거 위치·시각·판정자·정의 버전을 보존한 뒤 조건부 대응을 붙인다. 아래 대응은 새 제품의 enum이나 DB 계약을 확정하는 규칙이 아니다. 원 결과를 읽고 재조합하기 위한 **H: 편집 제안**이다. [I016-VOCAB_MAP](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/VOCAB_MAP.md#L3-L12) · [판정 단위 L24](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md#L24)

016의 원 대응표 **42행·7개 한글 필드**는 JSON 값과 순서까지 그대로 보존했다. 013·014·015 추가13행은 evidence/vocab-late.json의 원 배열 그대로 보존하고, 009를 9행 더했다. 합계는 64행이며 D3 소급표·상태표·혼동 금지표는 이 수에 더하지 않는다. 기계 판독본은 [glossary-data.json](evidence/glossary-data.json)이다.

## §2 016의 원 대응표 — 42행 원형 보존

다음 표의 `V01` 등 원 근거 ID는 [원 VOCAB_MAP의 근거 위치 목록 L112–129](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/VOCAB_MAP.md#L112-L129)에 연결된다. 근거 문자열을 이 표에서 다른 의미로 바꾸지 않았다.

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

## §3 추가 어휘 — 원 표와 별도

### §3.1 013·014·015의 13행

| 작업 | 어휘 | 답하는 질문 | 대응(조건부) | 같은 것으로 읽으면 안 되는 이유 | 원 결과 위치 |
| --- | --- | --- | --- | --- | --- |
| 013 | gold / adopted / rejected / referenced | 결정 기록의 비교 대상인가, 채택 결과인가 | 014 relevance·012 grade와 직접 동치 없음 | gold176은 adopted1/rejected99/referenced76을 포함한다. 추천 승인이 아니다. | RESULT.md L97–101; cases/CASES.json; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) |
| 013 | role / match_kind | 기여 종류인가, 맞추는 실체의 단위인가 | 016 form/contribution과도 별도 정의 | 같은 분야146과 structural_design146은 수가 같아도 동일 집합이 아니다. | RESULT.md L161–166; cases/CASES.json; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) |
| 013 | strict historical / any-date match | cutoff 이전 근거로 찾았는가 | 015 then/now는 타당성 상태를 묻는 별도 축 | 현재 URL 확인이나 이름 일치가 당시 접근·적합을 증명하지 않는다. | RESULT.md L120–136; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) |
| 013 | CONDITIONAL / nongold useful | 부분 범위에 조건부 쓸모가 있는가 | 004 CONDITIONAL_TRANSFER와 범위·근거 조건을 동시 보존 | 318/342 CONDITIONAL, D4 적용0/342. gold 재발견이나 실제 성공이 아니다. | RESULT.md L134–146; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md) |
| 014 | answers / pooled / review_independent | 누가 어떤 근거로 relevance를 부여했는가 | 012 seed/pooled/review와 판정 출처 축만 대응 | 정답 출처를 합쳐 단일 truth로 덮어쓰면 LSA/RRF 순위 반전 원인을 잃는다. | RESULT.md L34–41·107; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) |
| 014 | N@10 mean / N count / n_per_slot | 질의당 개수인가, 슬롯 비율인가 | 012 near_misses_at10와 평균 개념만 대응 | .0929=17/183이며17/1830은 슬롯 비율이다. 원 결과는 둘을 구별한다. | RESULT.md L23–30; results/metrics.csv; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) |
| 014 | must / prefer / mapped / conflict / removed_relevant | 명시 강제조건인가, 기계 매핑인가, qrel 손실인가 | 004 H와 조건부 연결 | 관련1 후보의 제거가 유효 제약 충돌일 수도 있고 극성 오독일 수도 있다. | RESULT.md L67·84; results/counterexamples.json; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) |
| 014 | original / summary / raw / terms | 원 질문인가, 입력 요약인가, 검색 변환인가 | 001 formulation과 유사한 표현 축 | raw는 원문을 뜻하지 않는다. 014의 원문은0/61, raw도 요약의 무브리지 버전이다. | RESULT.md L23·126·130; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md) |
| 015 | 성립 / 약화 / 무너짐 / 판단 불가 / 이유 없음 | 특정 이유의 현재 유효성은 어떠한가 | 003 동일성 hold·004 INSUFFICIENT와 직접 동치 없음 | 원자 이유의 상태이며 제품 전체 생존 여부나 추천 적합성은 아니다. | RESULT.md L59–67; REASONS.jsonl; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) |
| 015 | 처음부터 틀림 / 후발 무너짐 | 추천 당시부터 틀렸는가, 성립하다 바뀌었는가 | 013 cutoff는 근거 시점, 별도의 진위 축 | 14/195 현재 무너짐과5/83 후발 무너짐의 분모·사건이 다르다. | RESULT.md L63–67; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) |
| 015 | 추천 속성 / 제약 또는 비교 주장 | 이유의 방향이 바뀌면 추천에 어떤 의미인가 | 014 positive/negative condition과 조건부 관계 | OpenZFS의 옛 제약 해소는 이유 붕괴이지만 기능 개선이다. | RESULT.md L67; results/cadence.json; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) |
| 015 | signal positive / TP / FN / FP / stale | 관측 신호와 내용 상태가 어떻게 대응하는가 | D3-fetch 신호와 D1 내용 확인을 분리 | archive·404는 판정 자체가 아니다. 같은 날 관계를 향후 예측률로 바꾸지 않는다. | RESULT.md L22–33; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) |
| 015 | tool seconds / human labor / detection delay | 기계 대기인가, 사람 검토인가, 재생 지연인가 | 012 run elapsed와 비용의 일부만 대응 | 사람0명·정확 사건2개. 도구 시간과 가정된 지연을 실운영 노동 절감으로 읽지 않는다. | RESULT.md L75–77; [고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md) |

### §3.2 009의 9행

| 작업 | 어휘 | 답하는 질문 | 대응 어휘(다른 작업) | 같은 것으로 읽으면 안 되는 이유 | 근거 위치 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| 009 | 이미 충족 / 부분 충족 / 비어 있음 | 이번에 읽은 공식 문서의 어떤 기능 범위가 확인됐는가 | 004 H pass/fail/unknown 및 014 grade와 직접 대응 없음 | 이미 충족은 해당 분야·입력에서 문서화된 능력이다. 비어 있음은 열람 범위에서 근거 미확인이지 시스템·시장 부재 증명이 아니다. | [§1 L11–17](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L11-L17) | 미확인(고정 실제 과제의 목표 성공 여부) |
| 009 | H1 — 목적·부분·제약과 후보의 대응 기록 | 초기 탐색·검토에서 새 절차가 추가 가치를 주는가 | B09의 강한 기존 조합과 B10의 비용 가설; H2와 구별 | 일회 탐색에서 기존 조합이 동등 이상이면 H1을 기각할 수 있다. 후속 유지 부재로 그 성공을 취소하지 않는다. | [§2 L75–79; §5 L113–115](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L75-L79) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | H2 — 제공자가 바뀌어도 이어지는 근거 재검토 | 근거가 바뀐 뒤 재판정 비용이 줄어드는가 | 015의 당시/현재 이유 상태와 연결; H1의 초기 검색 성능과 별도 | 한 번 잘 찾았다는 사실은 변경 후 재검토 가치의 지지·기각이 아니다. 모든 제공자·모든 주장을 자동 유지한다는 계약도 아니다. | [§5 L117–119; §2 L79](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L117-L119) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | H3 — 기존 작업 도구 안의 작은 절차 | 별도 제품·UI를 만들어야 하는가 | ADR의 결정 기록 방식과 조건부 연결 | 기존 에이전트·문서·PR에 장부를 얹는 안은 연구자 가설이다. 자체 자료집·신규 UI·유료 제품 채택을 확정하지 않았다. | [§5 L121–125](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L121-L125) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | 반대 가설 A / 강한 기존 조합 | 범용 도구 조합이 이미 충분할 수 있는가 | 범용 LLM + 코드 검색 + 기존 목록 + 원문 확인 | LLM 단독을 이긴 결과로 기존 조합을 이겼다고 할 수 없다. 단일 시스템의 다섯 칸 공백도 조합 전체의 실패가 아니다. | [§2 L61–79](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L61-L79) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | 반대 가설 B / 목록·패턴 + 개발자 검토 | 범주를 아는 사용자의 짧은 번역만으로 충분한가 | 가벼운 자료형 구성의 비교 기준선 | 목록 데이터의 복제 제한은 사용자가 목록을 직접 사용해 답을 찾는 가설의 반증이 아니다. 후보를 전수 검색할 의무를 새로 부과하지 않는다. | [§3 L81–94](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L81-L94) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | 구축 전/후 비교(020의 정리 표현; 원 enum 아님) | 절차 도입 전후의 초기·변경 후 비용을 어떻게 나누는가 | H1은 초기 탐색, H2는 변경 후 재검토; 제품 구축 여부와 별도 축 | H1→H2는 자체 DB를 먼저 지어야 한다는 선행 관계가 아니다. 기존 도구 위의 기록 절차로도 두 비용을 비교할 수 있다. | [§5 L113–125](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L113-L125) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | 기능의 존재 / 실제 충분성 / 신규성 / 지불 가치 | 문서 기능 확인이 어떤 제품 결정을 지지하는가 | 문헌 D1·실제 적용 D4·사업 가설 H를 구분 | 기능 공백을 성능 우위로, 기능 존재를 실제 성공으로, 탐색 성공을 지불 가치로 자동 변환하지 않는다. | [판정 L5–7; §6 L129–135](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L129-L135) | 미확인(동일 예산의 실제 과제 비교 필요) |
| 009 | 근거 유지 / 원문 보존 / 후속 위험 신호 | 무엇의 상태를 어떤 방식으로 유지하는가 | 003 확인시각/불변 출처, 015 이유 상태, D3-fetch 신호 | URL 생존·원문 최신성·위치 재현·추천 이유의 현재 성립은 서로 다른 유지 대상이다. 보존이나 위험 표시가 진실성 보증은 아니다. | [§1 L17; §4 L107–109](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L107-L109) | 미확인(유지 대상별 실제 오류·노동 비용) |

009 원문은 [GAP §1–6](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L9-L135), [LANDSCAPE §6–한계](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/LANDSCAPE.md#L177-L207), [HANDOFF 상태·미실시](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/HANDOFF.md#L110-L127)에서 직접 확인했다. 여기서 “구축 전/후”는 020의 비교 설명이며 009의 원 enum으로 위장하지 않는다.

## §4 근거 수준과 D3 하위 유형

D0–D4는 모든 주장에 적용되는 일직선 품질 점수가 아니다. 문서의 정의는 D1로 충분할 수 있고, URL 응답만 확인한 D3-fetch가 그 문서의 내용을 더 참으로 만들지는 않는다. H는 관측 등급과 분리한 가설 표시다. `H(가설)`와 `004.H(요구 충족)`도 별도 이름공간으로 읽는다.

| 표기 | 확인한 것 | 뒷받침 가능한 범위 | 자동으로 뜻하지 않는 것 |
| --- | --- | --- | --- |
| D0 | 검색 snippet·목차 등 본문 미열람 | 발견 경로·열람 대기 목록 | 문헌 최소 개수·본문 주장 근거 |
| D1 | 문서·논문 본문 직접 확인 | 정의·작성자의 주장·문서에 기록된 사례 | 이번 작업의 실행·목표 적용 성공 |
| D2 | 고정 판의 코드 확인 | 해당 SHA 코드의 구조·분기 | 그 판이 배포됐음·해당 분기가 실제 실행됐음 |
| D3-search | 검색 결과 화면 관측 | 지정 질의·시각·화면에서 반환된 결과 | 전역 recall·후보 사실·제품 실행 성공 |
| D3-fetch | 페이지·API 응답 관측 | 지정 시점의 응답·표시·접근 상태 | 후보 기능 실행·지속 가용성·내용 진실성 |
| D3-run | 직접 실행한 코드·검사·실험 결과 | 명시 입력·환경·범위의 실행 산출 | 검사 밖 의미 정확성·다른 환경·사용자 목표 효과 |
| D4 | 목표 문제에 실제 적용한 결과 | 그 적용 범위·관측 창의 효과 | 다른 문제·사용자·운영 창에 대한 자동 일반화 |
| H | 연구자의 해석·가설·조립 제안 | 선택지·반증 조건·후속 확인의 설계 | 관측된 효과·원 작성자 발언·자동 채택 |

### §4.1 001~012 주요 주장에 대한 소급 표시

이번 표는 **고정 원 결과의 분류를 명료하게 붙인 것**이다. 과거 검색·제품 실험을 다시 수행했다는 보고가 아니다. 이번 JSON/CSV 재계산은 별도 audit-numeric-late.json에 있으며 원 연구의 실행과 구분한다. AF-RES-005~008은 이번 고정 입력 목록에 없으므로 내용을 추정하지 않았다.

| 원 작업·주장 | 소급 근거 수준 | 분류 이유 | 고정 원 결과 위치 | 승격하면 안 되는 결론 |
| --- | --- | --- | --- | --- |
| AF-RES-001 — 6사례×3표현·18개 비교용 표현 | D1/D2 근거 + 수작업 표현·손실 해석 H | C는 실제 분해 모델 출력이 아니라 주 작성자가 AI 분해를 가정해 작성했다. | [§2–3 L25–47](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/RESEARCH.md#L25-L47) | 실제 모델 오류율·사용자 질문 부담 |
| AF-RES-001 — CASE 참조·JSON·상대 링크 검사 | D3-run(로컬 산출물 검사만) | 입력·구조·참조 검사 종료0과 제품 기능 검증은 별개다. | [§4 L53–61](https://github.com/laadkke-arch/agentflow-open/blob/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/HANDOFF.md#L53-L61) | 분해 모델 실행·검색 순위·D4 |
| AF-RES-002 — P1/P2 고정 질의·화면의 발견 경로 | D3-search; 후보 본문 D1·고정 코드 D2 | 고유 문자열·제출 횟수·호출 수가 다르고 초기 혼합 반환을 공유 집합으로 기록했다. | [방법·단위 L35–43](https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/RESEARCH.md#L35-L43) | 제품 D3-run·전역 검색 recall·D4 통합 |
| AF-RES-003 — 9수작업 저장 표현·동일성 정책 | D1/D2 기반 H | 저장안 구현·마이그레이션·잘못된 병합률·작성 시간은 측정하지 않았다. | [연구 범위 L28–31; 확장 조건 L138–142](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md#L28-L31) | 운영 식별 정확률·저장 효율 실행 |
| AF-RES-003 — Explorer maintenance 공지와 코드의503 분기 | 공지 내용 D1; 응답·표시 관측 D3-fetch; 고정 분기 D2 | 공개 페이지의 안내와 코드의 조기503을 구별한다. 실제 POST와 배포 SHA는 미확인이다. | [최소 표현 예 L99–111](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md#L99-L111) | POST 실행으로503을 관측했다는 주장 |
| AF-RES-004 — 18행 기대 판정·참고 설계의 H/T | D1 + 명시된 합성 조건의 논리·전이 H | reference_design 판단과 implementation의 미확인을 함께 보존한다. 문서 DIRECT는 설치·통합 성공이 아니다. | [판정 단위·증거 경계 L24–46](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md#L24-L46); [미실시·실행 상한 L76–91](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/HANDOFF.md#L76-L91) | 후보 런타임 D3-run·목표 적용 D4 |
| AF-RES-009 — 35시스템의 문서상 다섯 요소 | D1 정적 지형; H1/H2/H3는 H | 제작자 예제·기능 문헌을 읽었으나 고정 P1/P2/P03을 제품에 제출하지 않았다. | [§6–한계 L177–207](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/LANDSCAPE.md#L177-L207); [미실시 L110–125](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/HANDOFF.md#L110-L125) | 35제품 실행·새 절차의 우위·시장 부재 |
| AF-RES-010 — 일반 웹·AskNature 표현별 검색 | D3-search; 기록된 페이지/API 응답만 D3-fetch | 검색 질의·창·관측을 실행했지만 표현별 통제 정밀도나 목표 구현 효과는 측정하지 않았다. | [상태 L5–7](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/HANDOFF.md#L5-L7) | 통제 검색 성능·목표 소프트웨어 runtime |
| AF-RES-010 — 역사적 원리 전이·현재 용도 매핑 | 원저자 보고 D1; 목표 대응 판단 H | 원저자 실행을 읽은 것과 이번 목표에 직접 구현한 것을 구별한다. | [판정 방식 L24–28](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/TRANSFER_CASES.md#L24-L28) | 이번 D3-run·P1/P2 D4 |
| AF-RES-011 — URL281회·accepted 메타데이터 관측 | D3-fetch; 집계 산출 D3-run | 단회 응답·채택 표식은 제품 기능이나 통합 성과가 아니다. | [표본·URL L34–39](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md#L34-L39); [URL 수준 L70; accepted API L88](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CODEBOOK.md#L70-L88) | 제품 기능 실행·지속 링크 생존·D4 |
| AF-RES-011 — whole/part·역할·반응 단계 해석 | 원문 D1; 작업자 코딩·추론 H | 대답 없음·채택 표시·계획·사용 보고를 서로 다른 변수로 읽는다. | [범위·반응 L11–44](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/CODEBOOK.md#L11-L44); [적용 한계 L146–148](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md#L146-L148) | 사람 재현성·부분 질문의 통합 성공률 |
| AF-RES-012 — BM25/LSA/RRF 검색·풀링·clean replay | D3-run(로컬 검색 실험) | 27개 순위 파일 재현은 고정 데이터·판정·환경의 실행 동일성이다. 레지스트리 자료 획득은 D3-fetch, 본문 해석은 D1/H다. | [범위·재현 L108–123](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md#L108-L123); [workload·pooled_replay·clean_replay](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/VERIFICATION.json) | 새 사용자 적용 D4·독립 사람 정답 |
| AF-RES-012 — E5 가중치 접근 실패 | D3-fetch의 차단 관측; E5-run 없음 | 모델 이름·revision은 실행 결과가 아니다. 실제 검색은 TF-IDF+LSA 대체다. | [model.blocked_probes·executed_revision=null](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/VERIFICATION.json); [차단·재개 L74–87](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/HANDOFF.md#L74-L87) | 학습형 임베딩 효과의 지지·반증 |

## §5 원 인계 상태·진행 상태·내용 채택

세 상태축을 합치지 않는다. foundation의 정책은 완료에 `saved_result_and_task_acceptance_evidence`를 요구한다. 같은 고정 진행표에는 지정12작업이 DONE으로 표시되어 있지만,013의 원 인계는 BLOCKED이고016에는 지정 원문 미열람이 남아 있다. **이 정합성은 별도 인수 기록으로 확인해야 하며, DONE을 단순 파일 배송으로 정의하거나 원 미충족을 지우지 않는다.** [policy.completion; tasks의 지정12작업 status](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/automation/dot-control.json) · [완료 확인 L57–64](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/DOT_AUTOMATION.md#L57-L64)

| 어휘 | 축 | 정확한 의미 | 진행표와의 대응 | 같게 읽으면 안 되는 것 |
| --- | --- | --- | --- | --- |
| REVIEW_READY | 원 연구 인계 | 해당 요청의 검토 가능한 인계 준비 상태 | 결과 커밋·수용 근거를 진행 담당이 대조한다. DONE과 자동 동치가 아니다. | 설계 채택·외부 사실 전체 보증·효과 검증 |
| REVIEW_READY_WITH_GAPS | 이번 조립의 정규화 인계 | 사용 가능한 결과와 차단·자료 부재의 미충족 목록을 함께 인계 | 미충족 조건·범위·재개 입력을 보존해 별도 인수 판단한다. | 모든 조건 충족·기각·자료 전체 무용 |
| BLOCKED | 원 연구 인계 또는 진행 차단 | 핵심 질문 또는 명시 인수 조건을 충족하지 못한 사유가 있음 | 차단 이유와 보존 산출물을 따로 읽는다. 다른 축의 DONE을 근거로 원 BLOCKED를 지우지 않는다. | 파일 없음·모든 분석 실패 |
| DONE | 진행표 처리 | 진행 담당이 기록한 작업 상태. 정책의 완료 기준은 saved_result_and_task_acceptance_evidence다. | 원 인계·acceptance 증거와의 정합성은 별도로 확인한다. 파일 배송만을 뜻하는 규정으로 축소하지 않는다. | 내용 채택·효과 입증·무조건 수용 |
| 검토됨 / accepted / 채택 | 검토 또는 설계 결정 | 어떤 검토·선택을 누가 어떤 범위에서 했는지 추가 식별 필요 | 진행 상태에 합치지 않는다. ADR accepted도 특정 결정에 대한 합의다. | REVIEW_READY·DONE·D4·모든 사실 참 |

### §5.1 원 상태를 보존하는 사례

| 작업 | 원 인계 문자열 | 고정 진행표 | 이번 정규화·해석 제안(H) | 미충족 또는 범위 | 원 위치 |
| --- | --- | --- | --- | --- | --- |
| AF-RES-009 | REVIEW_READY | DONE | REVIEW_READY(문서 연구 범위) | 목표 효과·지불 가치 미측정은 해당 문서연구 밖; 제품 채택 아님 | [식별 L18; 미실시 L110–127](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/HANDOFF.md#L18) |
| AF-RES-013 | BLOCKED — SITE_CAP_CASES | DONE | 원 BLOCKED를 보존; 활용 가능한 내용과 인수 정합성 검토를 별도 표시 | 당시 사례 사이트 상한 적용으로 strict_acceptance blocked. 이번 brief의 방법/사례 구분이 과거 인수를 소급 완료시키지 않음 | [인계 상태 L6–18](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/HANDOFF.md#L6-L18) |
| AF-RES-016 | core_artifacts_complete_with_blocked_named_original_reading | DONE | REVIEW_READY_WITH_GAPS에 해당하는 내용으로 제안하되 원 문자열 유지 | 지정 고전 원문0/2, 72개 구조·수치 PASS는 unqualified_task_complete와 다름 | [인계 상태 L5–16](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/HANDOFF.md#L5-L16) |

**H — 편집 제안:** REVIEW_READY이고 해당 요청의 acceptance 항목이 모두 충족됐는지를 확인한 뒤 진행 담당이 DONE 여부를 검토하도록 연결한다. 이는 기존 공통 계약을 새 규칙으로 수정했다는 뜻도, 이 연구가 진행표를 갱신했다는 뜻도 아니다. `검토됨`이 선택 완료나 사실 전체의 보증이 아니라는 원 운영 규칙을 유지한다. [§4 L74–76](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/RESEARCH_WORKFLOW.md#L74-L76) · [색인 기록 항목 L30–34](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/research/INDEX.md#L30-L34)

## §6 같은 것으로 읽으면 안 되는 쌍

| 표현 A | 표현 B | 차이·반례 | 원 위치 |
| --- | --- | --- | --- |
| 후보 form | 문제 상대 contribution | 라이브러리라는 형태가 선택 범위 전체/일부/비교에 쓰이는 기여를 정하지 않는다. | [S1/S2/S3 L9–43](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/CODEBOOK.md#L9-L43) |
| role | proposed_use | 같은 component라도 색인·동기화·복원에 쓰는 제안은 다르다. 004 HANDOFF L80은 이 축을 축약해 실제 전달 불일치를 남겼다. | [판정 단위 L24](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md#L24); [핵심 제안 L80](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/HANDOFF.md#L80) |
| gold | adoption / nongold useful | 013 gold에는 채택1·기각99·참조76이 있다. 검색 회수 기준과 적용 성공·부분 쓸모가 다르다. | [Q1·Q4 L97–101·134–146](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md#L97-L101) |
| 같은 분야146 | structural_design146 | 서로 다른 축이며 교집합142, 각각만4개다. 같은 분모로 보고7/146과8/146을 충돌로 만들지 않는다. | [gold_items.role × match_kind](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/cases/CASES.json); [표4 L161–166](https://github.com/laadkke-arch/agentflow-open/blob/eb569f07a3a34ffacf114384ae9b06ad062f5396/docs/workstreams/research/AF-RES-013/RESULT.md#L161-L166) |
| 부분 질문 반응 합집합10/33 | 통합 성공률 | 명시 선택·사용6와 accepted5의 중복1을 뺀 질문 집계다. 실제 통합 검증이 아니다. | [Q7 L116–128](https://github.com/laadkke-arch/agentflow-open/blob/478c301b693896e2c6d777f46ac441f071bfdfe8/docs/workstreams/research/AF-RES-011/HANDOFF.md#L116-L128) |
| N 개수/질의·조건 | N 비율/슬롯 | 012는85/216→163/216, 014는17/183→11/183의 평균 개수다. 각각 슬롯2160·1830으로 나눈 비율과10배 다르다. | [지표 정의 L5–9·49–53](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/RESULTS.md#L49-L53); [지표 분모 L23–30](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md#L23-L30) |
| 0/30 동일 판정 재사용 | 라벨 표시의 인과 효과0 | 016은 공통 판단을 양쪽 표시값에 복사한 문서 감사다. 14정보부족·15라벨미부여를 포함한다. | [serialization_note·summary](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/evidence/impact.json); [Q7 L170](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/RESULT.md#L170) |
| checked_at timestamp | 당시 원문 아카이브 | 확인 시각은 과거 내용을 복원하지 않는다. 불변 판·허용된 snapshot·근거 위치의 보존 여부를 따로 기록한다. | [원문 보존 최소안 L107–111](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md#L107-L111) |
| 처음부터 틀린 이유 | 성립하다 바뀐 이유 | 015 현재무너짐14/195와 후발5/83·정확답날짜2/77은 다른 조건 집합이다. | [Q2 L63–67](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md#L63-L67) |
| 이유 붕괴 | 추천 악화 | 옛 제약이 해소되는 변화도 이유가 거짓이 된 사례다. OpenZFS는 기능 개선에 해당한다. | [후발 사건 L67](https://github.com/laadkke-arch/agentflow-open/blob/e39d23c9a7307ba83c974580f60115d90e221084/docs/workstreams/research/AF-RES-015/RESULT.md#L67) |
| D3-fetch | D3-run / D4 | 응답을 받았다는 사실·코드가 실행됐다는 사실·목표에서 효과를 얻었다는 사실은 서로 다르다. | [model·executions](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/VERIFICATION.json); [한계 L141–143](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md#L141-L143) |
| REVIEW_READY / DONE | 설계 채택 / 효과 입증 | 인계 준비·진행 처리·내용 선택·실제 적용은 별도 축이다. 013/016의 원 상태와 DONE 정합성을 인수 기록에서 확인해야 한다. | [§4 L74–76](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/RESEARCH_WORKFLOW.md#L74-L76); [policy.completion; tasks[id=AF-RES-013/016].status](https://github.com/laadkke-arch/agentflow-open/blob/7b4334e55a0563225295618eaf3ad299b415d9f7/docs/automation/dot-control.json) |
| H(연구자 가설) | 004의 H(요구 충족 축) / 009의 H1·H2 | 같은 문자라도 근거 지위·판정 질문·가설 식별자다. qualified key 없이 합치지 않는다. | [네 판단축 L28–37](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md#L28-L37); [§5 L113–125](https://github.com/laadkke-arch/agentflow-open/blob/7f627a81199f06da7f7b15f979e7fef25dd17602/docs/workstreams/research/AF-RES-009/GAP.md#L113-L125) |
| 014 raw 질의 | 원문 original 질의 | raw는 기술어 브리지 적용 전 요약이다. 원문0/61을 raw61/61로 대체해 원문 성능이라 부르지 않는다. | [입력 L23; 변환 L126](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md#L23); [mode/source summary61](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/queries/metadata.json) |
| 010 T=mapped | 014 must mapped / 012 origin=transfer | T는 관계 대응, must mapped는 기계 개념 대응, origin transfer는 앞선 판정 재사용이다. | [010·012 대응 L42–61](https://github.com/laadkke-arch/agentflow-open/blob/3b43c41ae8e9f8d41ea740669a6e5b3625f7d7cc/docs/workstreams/research/AF-RES-016/VOCAB_MAP.md#L42-L61); [필터 L67](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md#L67) |
| 279/290 전체 일치 | 관련 판정 합집합의 공통3/12 | 희소 양성에서 음성 일치가 전체 비율을 높일 수 있다. 목적에 맞는 분모를 함께 보존한다. | [판정 출처 표3·Q5 L41·107](https://github.com/laadkke-arch/agentflow-open/blob/42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9/docs/workstreams/research/AF-RES-014/RESULT.md#L41) |

## §7 다른 분야의 기록 방식과 연결 — H

Q7의 근거 종류는 고정 내부 연구 결과(D1)와 외부 방법 원문(D1) 두 종류다. 외부 방법이 이 어휘를 검증한 것은 아니다. 아래 연결은 정의·근거·선택·이력을 분리하기 위한 연구자의 조립 제안이며, 원 방법의 등급·상태를 기계적으로 이식하지 않는다.

| 원문 ID | 확인한 기록 원리 | 이번 어휘표에 반영하는 방식(H) | 적용 한계 |
| --- | --- | --- | --- |
| [X08](https://www.researchgate.net/profile/Victoria_Bellotti/publication/233367028_Questions_Options_and_Criteria_Elements_of_Design_Space_Analysis/links/00b7d53211940ad48e000000/Questions-Options-and-Criteria-Elements-of-Design-Space-Analysis.pdf) | QOC는 질문·대안·기준을 나눠 비교한다. 요소의 이름이 같다고 IBIS와 같은 의미가 되거나 찬성 수로 자동 선택되는 것은 아니다. | H: 용어마다 답하는 질문과 판단 대상을 적고, 묶음·관계·채택을 각각 분리한다. | 원 42행에 QOC의 상태를 덮어쓰지 않음 |
| [X10](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | ADR은 맥락·결정·상태·결과를 남기고 뒤집힌 결정을 삭제하지 않는다. | H: 원 인계 상태와 정규화 상태를 함께 남기고 바뀐 판단은 후속 기록으로 연결한다. | ADR accepted는 연구 근거의 확실성·작업DONE·제품효과가 아님 |
| [X12](https://ilcor.org/uploads/Tools-GRADE-guidelines-Evidence-to-Decision-Tables.pdf) | EtD는 질문·관점, 근거, 기준별 판단, 결론을 나눠 명시한다. | H: D0–D4/H는 획득 방식, L/E/H/T는 판정 질문, 채택은 선택으로 따로 기록한다. | 의료 틀의 기록 원리를 빌린 것으로 D등급을 GRADE 확실성 등급으로 치환하지 않음 |

## §8 검토·한계·다음 확인

검토자는 GPT-6 Astra Pro, 같은 모델 계열의 내부 별도 검토다. 원42행 배열의 깊은 동일성과 행수·키를 실제 JSON으로 확인했다. 009의 의미, 초기 작업의 D3 경계,013·016 원 인계는 지정 SHA에서 직접 대조했다. 017~019 결과는 읽지 않았으며 대기 중인 입력으로 남겼다.

새 용어를 하나의 enum으로 합치기 전에 같은 후보·같은 역할·다른 사용 방식3쌍을 복원하고, comparison/reference 경계30개를 동일 문맥에서 재판정한다. 상태 대응은 진행 담당의 인수 근거를 먼저 확인한다. 자료와 정의가 달라진 경우 원 라벨을 덮어쓰지 말고 대응 버전과 이유를 추가한다.

한계: 어휘 대응은 의미 손실을 줄이는 제안이다. 실제 판정자 간 재현성·편집 노동 절감·사용자 성능 개선을 새로 측정하지 않았다. 016의 comparison0/120 대14/120은 이 표를 만든 사실만으로 해소되지 않는다. 현재 공통 색인·계약·진행표는 수정하지 않았다.
