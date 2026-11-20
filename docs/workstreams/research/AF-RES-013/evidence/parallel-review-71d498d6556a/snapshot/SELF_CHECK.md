# AF-RES-013 — 자기 점검

## 1. 점검 범위와 판정 기준

이 문서는 [RESULT.md](RESULT.md)의 주장, 원문·실행 기록, 판정과 분모를 대조한다. 작업자의 추출·분류·채점과 **내부 별도 검토**를 구분한다. 세션의 모델 표기는 **GPT-6 Astra Pro**이며, 내부 별도 검토는 사람이나 다른 모델의 독립 검증이 아니다. Q1–Q4는 서로 다른 종류의 출처를 확인하고, Q5–Q8의 실행 관련 답은 수치 표와 실제 사례를 함께 확인했다. 정답 일치, 문서상 참고 유용성, 실제 설계 개선을 합치지 않았다.

현재 보존된 자료는 31사례·176정답, A/B 각각31회, 후보342개다. `sources.json`의 전체 열람 원장은 핵심343행과 연결된 실행별 원장992행, 합계1335행이며, 이것을 독립 문서1335개라고 세지 않는다. 제외342건은 별도다. 최소수에 산입한 비사례 본문은26개이고 사이트 그룹은14개, 한 사이트는 최대3개다. 각 자료의 실제 주소·시각·읽은 범위·확인 내용·한계는 원장에 있다.

`JUDGMENTS.json`은 모든342개 후보의 필수 축·일치·시점·판정자를 담고, `details`는 제약 문구·이유·전이 대응·추가 확인을 보존한 실행별 상세62개로 연결한다. 출처와 판정의 분할은 내용 손실 없는 직렬화 변경이다. [최종 검증 기록](evidence/FINAL_VALIDATION.json)은 각 상세 파일 hash, 모든 유지 값, 기록 수와 출처 필드를 대조한다.

## 2. 세부 질문별 점검

| 세부 질문 | 답 한 줄 | 붙은 출처 ID(종류 수) | 반증 시도(쓴 질의·자료와 결과) | 남은 불확실성 |
| --- | --- | --- | --- | --- |
| Q1 정답원 | 4계열 모두 문제 부분과 비교 절을 분리할 수 있으나, 빈 절·혼합 Rationale·리뷰 뒤 편집 때문에 제목만으로 정답원을 만들 수 없다. | R-TEMPLATE-INIT·R-TEMPLATE-PRIOR-MERGE·PS-T-PEP12·PS-T-SWIFT-INITIAL·K-TEMPLATE-NOW(템플릿/절차), R-TEMPLATE-HISTORY(변경 이력), M27(리뷰 원문), M06(특허 검색 평가 논문): **4종류**. [TEMPLATES](TEMPLATES.md), RESULT Q1의 31접두부·A/B 각31회와 C24 입력 분리. | CE-Q03 `site:github.com/kubernetes/enhancements "Alternatives" "None"`, CE-Q05 `site:github.com/rust-lang/rfcs "Alternatives" "None."`로 형식적 절을 찾았다. CE-K265-EMPTY·CE-K177-EMPTY·CE-R90-MISSING은 실제 빈/부재 반례다. CE-R438-FALSE-POSITIVE·CE-R1300-FALSE-POSITIVE는 본문을 열어 snippet의 None이 다른 절 소속임을 확인했다. | 템플릿 존재는 모든 문서의 충분한 대안을 보장하지 않는다. Go·ADR·IETF·TC39의 동일 수준 이력 비교는 수행하지 않았다. 답을 바꿀 최소 추가 확인은 최근 Prior art 절과 빈 절을 함께 포함한 4계열80문서의 시기별 조사다(RESULT §4.1). |
| Q2 사례 집합 | 공식 목록·번호순·사전 제외 규칙으로31사례를 보존했으며, 채택 뒤 대체·명시적 부분 번복6개를 포함한다. | PS-P0386-prefix·PS-P0386-gold·PS-P0563-gold·R0114-DOC(고정 설계 본문), PS-H-P386·R0114-PR(저장소 이력/결정 metadata), PS-R-P563-ACCEPT(결정 메일): **3종류**. [CASES](cases/CASES.json), [구성 점검](evidence/CORPUS_CHECK.json), [집계](evidence/AGGREGATES.json). | 초기 P386의 두 비교기를 합쳐 제외한 오류를 원문과 SCOPE의 분절 규칙으로 재검사해 C31을 추가했다. C14 수락 메일 날짜도 상태 반영일과 대조해 실행 전 정정했다. C10·C11·C13은 기각/초안 후 대체이므로 채택 후 변경6개에 넣지 않았다. 원래30사례 민감도는 A20/171·이전14/171, B8/171·이전2/171이다. 관련 검색·선별·건너뛰기 원장은 SAMPLING과 SEARCH_LOG에 있다. | 일부 A가 시작된 뒤 C31 적격 누락을 복구했으므로 오류 없는 단일 사전 선정은 아니다. 계열 최대9/31은 충족하지만 확률 표본은 아니다. 결정 사건의 정의와 오래된 merge object 실패를 확인하려면 CASES의 `decision_evidence` 및 판별 사유를 따라 원 PR head/결정 공고를 재확인한다. |
| Q3 항목 분류 | 176항목은 부품17·같은 분야 설계146·다른 생태계12·다른 분야1이며, 외부 실체34와 내부 구조142를 구별했다. | R0123-DOC·PS-S0018-gold 및 사례별 고정 본문(설계 제안), R-REVIEW-123·PS-R-S22-ACCEPT·M27(리뷰 원문): **2종류**. RESULT 표2/Q3, CASES의 `role`·`stance`·`reason`·`added_in_review`·`boundary_note`. | C17의 library binding 전략을 특정 제품과 구별하고, C26의 세 버전 문법 선택을 일반적인 version 조건부 기능과 구별했다. 리뷰를 열어 본문 밖7항목을 확인했으며 DRF/DataRaceFree alias를 중복 제거해 신규6개·확대 pool182개로 계산했다. C27의 리뷰 기원 항목은 이미 본문에 있어 중복 추가하지 않았다. | 작업자의 역할 코딩이며 역할 신뢰도 자체는 범위 밖이다. 모든 항목의 최초 리뷰 등장 시점을 복원하지는 못했다. 신뢰도 결론을 내려면 역할 경계 사례를 사전 표집하고, 원문을 독립 코딩한 추가 판정 및 일치/불일치 기록이 필요하다. |
| Q4 다른 분야 인용 | 기능 관계를 실제 옮긴 다른 분야 항목은 정정 후1/176(0.57%)이며 KEP1/34, 나머지0이고 A/B 모두0/1이다. | J-C05-LINGUISTIC-BOUNDARY·SR2-GOLD-C05·CE-TERM-P433(고정 설계 제안), CE-CODEL(설계 표준), M12(학술 인용 추천 개요): **3종류**. [역할 정정](evidence/ROLE_CORRECTIONS.json), RESULT 표2/Q4. | CE-Q01 `site:rfc-editor.org/rfc/rfc8289 "control theory"`, CE-Q04 `"PEP 433" "sterile"`, CE-Q02의 Polonius/Hamlet 명칭 탐색과 실제 원문을 비교했다. CoDel의 제어 전제·일정은 작동 원리, sterile·Atom은 용어 차용으로 구별했다. C05-G06은 능동태/목적어를 event field에 대응한 구조이므로 외부 언어학 논문이 없다는 초기 배제 이유를 고정 SCOPE에 대조해 정정했다. 최초0/176(회수0/0 정의 불가), PySizer까지 넓힌2/176(회수0/2)도 보존했다. | 1개는 외부 언어학 문헌의 명시 인용이나 채택 효과가 아니라 기각된 구조 차용이다. 다른 언어·생태계12개를 먼 분야로 부풀리지 않았다. 이 분모로 설계자 전체의 수요를 추정할 수 없다. 최근/빈 절 포함80문서와 분류 경계 재검토가 답을 바꿀 최소 후속 조사다. |
| Q5 기준선 A | 새 문맥31회에서204후보를 냈고 정답 동일22/176(12.50%), 결정 이전 근거16/176(9.09%)를 회수했다. | **실행 기준 충족:** RESULT 표1·표2 및 Q5의 수치, [AGGREGATES](evidence/AGGREGATES.json), [RUN_AUDIT](evidence/RUN_AUDIT.json), [A-C20](runs/A/C20.json)·[A-C23](runs/A/C23.json)의 구체 원 응답. 보조 출처 종류는 D3-run·원문/고정 코드·M02 누설 방법론. | A-C20의 `ICU MessageFormat localization plural select message formatting user guide`와 `https://grep.app/api/search?q=MessageFormat%20plural` 등 실제 query를 보존했다. C20의 L20n/gettext 회수와 C17 binding 회수를 확인했지만 C26 문서 안의 모든 문법을 원 추천에 소급하지 않았다. A-C23의 `C11 N1570 uintptr_t void pointer integer type 7.20.1.4`는 유용한 계약 참고를 찾았으나 내부 대안 적중과는 분리했다. 접근 제한이 적중을 낮춘다는 대안을 점검하여 native code HTTP200 14/31·실패/fallback17/31, 노출 기록 없는18사례의12/93·이전8/93을 따로 냈다. | 단회·한 모델·현재 웹이며 모델 학습 기억은 제거하지 못했다. 실제 전용 코드 검색 성공을 전31회라고 주장하지 않는다. 재실행 입력은 각 prefix와 BASELINE_RULES뿐이다. 가능한 공개 코드 검색 환경에서 동일 예산으로 반복하면 접근성·분산 영향을 구별할 수 있다. |
| Q6 기준선 B | 카탈로그 발견과 원문 검증을 새 문맥31회로 실행해138후보, 동일8/176(4.55%)·이전2/176(1.14%)를 얻었다. | **실행 기준 충족:** RESULT 표1·표2 및 Q6 수치, [B-C24](runs/B/C24.json)·[B-C27](runs/B/C27.json), RUN_AUDIT. 009 LANDSCAPE는 도구 선택에만 사용했다. B는 사람이 아닌 새 문맥 내부 모델 번역임을 표의 판정자 설명과 본문에 표시했다. | B-C24의 `site:github.com/akullpp/awesome-java "Bean Mapping" "Code Generators"`와 `site:github.com/vinta/awesome-python "attrs"`에서 발견 경로를 확인했다. Immutables의 비공개 속성/공개 builder 입력 경고는 거절 구조 회수1/7이지만 날짜 미확인이라 이전0/7이다. attrs의 제품 출시와 후속 기능 날짜를 구별했다. C27 Elixir name/arity는 같은 arity·다른 label 조건을 위반했다. C10 절차 이탈은 기록하고 대상 후보를 제외했다. A+B 사후 합집합24/176·이전16/176과 B만 추가한2개도 계산했다. | 사람 번역 성능과 오염이 전혀 없는 검색을 뜻하지 않는다. B의 질의17회는 B의 page25 또는20분 조건과 다르며 A의 query12 상한을 적용하지 않는다. 사람 번역 조건을 같은 과제·예산으로 실행해야 009 반대 가설B를 직접 비교할 수 있다. |
| Q7 채점 | 004의 L/E/H/T와 네 라벨로342후보를 판정하고, 항목 일치·조건부 참고·근접 오답·접근 실패를 분리했다. | **실행 기준 충족:** RESULT Q7의 4라벨 표와 표1·2, JUDGMENTS의342행, C05/C09/C24/C20의 구체 경계 판정. 고정004 PROTOCOL(프로토콜), M13·M14(생성형 인용 평가 논문), 원 응답/원문이 보조한다. | 18행 첫 검토와7행 두 번째 내부 별도 검토에서 C05의 dedup 유지와 C09 builtin range 일치를 제거하고 C24의 명시적 실패 구조를 인정했다. Jed는 같은 프로젝트가 아닌 동일 명시 메커니즘이며 제외 민감도 B7/176·이전2/176이다. C02 gVisor·C27 arity 조건 위반과 C12 RPython detector 미확인을 확인했다. 링크 감사5개 차이는 fragment/redirect 재열람으로 해소했다. 최종 깨진·가짜 링크는 A0/204·B0/138이지만 검색 중 실패와 제출 전 제외를 보존했다. | 정답 밖 유용 후보 A146/178·B105/126은 문서상 참고이며 실제 우월성 검증은0건이다. A50·B28행은 원 후보의 좁은 scope에 따라 일부 H가 범위 밖이다. 나머지 미확인 원문·날짜·제약은 각 상세 판정의 `remaining_check`가 최소 확인 방법이다. 실제 채택 효과는 대상 구현 및 설계자 검토가 필요하다. |
| Q8 009의 기각 조건 | 낮은 문서 항목 회수만으로 009의 반대 가설A/B를 공식 기각하거나 새 제품의 추가 가치를 입증할 수 없다. | **실행 기준 충족:** RESULT 표3·Q8, A22/176·이전16/176/B8/176·이전2/176 및 C24 B1/7·이전0/7 사례. 고정009 GAP §2·§3·§5(선행 연구 조건), M03·M04·M15(검색 평가 방법론), 이번 D3 실행: **3종류**. | “기존 조합이 문서의 모든 대안을 재현한다”는 강한 해석은 실제 놓침으로 반박했다. 반대로 C24 거절 구조 회수와 C23의 정답 밖 참고, 리뷰 신규6개는 낮은 본문 recall을 무용성으로 읽는 결론에 반례가 된다. 다른 분야만 떼어0/1을 제시하고 CoDel은 빈도 분모에 넣지 않았다. 새로운 절차·사람 검토 시간·결정 개선 arm이 없다는 조건을009 원문과 대조했다. | 충분성/우위의 공식 판정은 보류한다. H2 유지 가치는 측정하지 않았다. 최소 후속은 새 실제 과제12개×기존 전체 조합/카탈로그+개발자/사전 고정 새 절차3조건×3반복=108회이며, 같은 허용 오류·검토 시간과 실제 결정 변화를 기록한다(RESULT §4.3). |

각 행은 주장에 반대되는 자료 또는 판정 오류 가능성을 검사했다. 원 질의는 [SEARCH_LOG.json](SEARCH_LOG.json)의 선정·방법론·반례 원장과 각 실행의 `queries`에 그대로 남겼다. 자료를 못 연 경우는 근거 수에 넣지 않았다. 표의 불확실성은 답을 바꿀 최소 확인을 명시하며, 이미 수행한 검색을 미실시로 반복 표기하지 않는다.

## 3. 반례·자료 품질의 별도 대조

다섯 반례 모두 [COUNTEREXAMPLES.md](COUNTEREXAMPLES.md)에 검색·판정 기록이 있다. 빈 비교 절은 실제 관측했다. 본문 밖의 “더 좋은 선례”라는 강한 반례는 아직 입증하지 못했으며, 본문 밖 참고와 리뷰 신규6항목이라는 작은 누락 증거만 확인했다. 채택 뒤 변경6개와 기각/초안 대체3개는 [REVERSALS.md](REVERSALS.md)에서 후속 이유와 원 추천을 대조했다. 관련 원리를 찾았다는 이유만으로 뒤집힐 이유를 예측했다고 채점하지 않았다. 링크의 접근 실패는 가짜와 구별했고, 구조/작동 원리와 장식적 용어를 표본 안팎에서 비교했다.

자료 품질에 대한 내부 별도 검토는 [SOURCE_QUALITY_REVIEW.json](evidence/SOURCE_QUALITY_REVIEW.json)에 있다. NTCIR의 “30개 시스템”이라는 단위를 제출111개 중 평가30개 **run**으로 바로잡았다. Swift25의 수락 인용 후속 글과 실제 대안 논의 원문을 같은 토론 자료 하나로 연결했고 두 문서로 부풀리지 않았다. M13·M14가009의 고정 자료에 없다는 점도 URL만이 아니라 제목·식별자를 대조했다. 열람 재시도가 실패해도 앞선 성공 열람을 없었던 것으로 바꾸지 않았으며 성공/실패 기록을 각각 보존했다.

[최종 보고서 내부 검토](evidence/FINAL_REPORT_REVIEW.json)는 수치·분모·행별 놓침·지역 링크·공식 기각 조건을 대조했다. [국소 편집 해결 기록](evidence/FINAL_REPORT_RESOLUTION.json)은 “실체”와 “동일”의 혼동, 다른 생태계12항목의 표현, Q1/Q8의 실행 연결 예시를 보완한다. 이는 원문 판정의 독립 신뢰도 검사가 아니며 집계와 원 응답은 바꾸지 않는다.

## 4. 마감 실행 결과

현재 읽은 `evidence/FINAL_VALIDATION.json`은 **data 모드19항목 통과**를 기록한다. 31접두부의 해당 커밋 내용 hash가 현재 파일과 같고 모두 최초 gold 커밋의 선조임을 검사했다. 342개 후보의 채점·62개 상세 파일의 무손실 연결·출처1335행의 필드 및 hash·owned_path 경계도 검사했다.

**마감 검사 대기:** 이 SELF_CHECK를 쓴 시점에는 `--final` 및 repository session check를 아직 실행하지 않았다. 진행 담당은 RESULT의 국소 편집을 재생성한 뒤 다음 명령을 실행하고, 실제 결과로 이 절과 아래 마지막 gate를 갱신해야 한다. 미실행 검사를 통과로 간주해 HANDOFF를 쓰면 안 된다.

```bash
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-013/manifest.json --fetch
python docs/workstreams/research/AF-RES-013/tools/validate_deliverables.py --final
```

최종 검사와 SELF_CHECK를 별도 묶음으로 커밋한 뒤에만 HANDOFF를 작성한다. HANDOFF는 마지막 단독 커밋으로 남기고 원격 본문과 로컬 hash를 대조한다. 원격 재열람·최종 clean-tree 검사는 HANDOFF 커밋 이후의 별도 마감 관측이며, 이 문서를 쓰는 시점에 이미 수행했다고 주장하지 않는다.

## 5. 끝내도 되는 조건 — acceptance_evidence

| 조건 | 충족 여부(예/아니오) | 근거 위치 및 적용 범위 |
| --- | --- | --- |
| 4개 이상 계열·30개 이상 사례·대체된 결정5개 이상 | 예(사전 등록한 독립 제안서 단위) | CASES: 31개, KEP6/PEP9/Rust8/Swift8, 최대9/31. REVERSALS: 채택 뒤 대체·부분 번복 C07·C12·C14·C21·C29·C31의6개. 기각/초안 뒤 대체3개는 분모에서 제외. 사이트 상한 해석은 아래 별도 행 참조. |
| 사례마다 정답 항목3개 이상 | 예 | CASES와 CORPUS_CHECK; 최소3·최대19, 총176. 이름 반복과 alias를 중복 항목으로 세지 않음. |
| 모든 사례 A 원 응답, B20개 이상 | 예 | runs/A 31개·204후보, runs/B 31개·138후보. RUN_AUDIT의 coverage/missing/errors와 원 응답·query·열람·시각·예산을 대조. |
| 접두부 커밋이 정답 커밋보다 앞섬 | 예 | 접두부 `8cb2b8e58f7d4278c11073956b31b30ad43aff18`, C14 정정 `c9936188a885848a16b55b4e11ac965bd2d0b204`, C31 추가 `ba1cc08705e4a1c56fcdb1a8062193ca4748992e` 모두 gold `f6f59a85949a001792b80260dd454c3fcc714a70`의 선조. PREFIX_MANIFEST와 FINAL_VALIDATION의 각 SHA/hash. |
| 표1–3 지정 열·미확인 칸별 확인 방법 | 예(문서 검토 완료; 마감 자동 검사 대기) | RESULT §1의31사례·6역할·주장 표, FINAL_REPORT_REVIEW의682개 사례 필드 및 미확인 설명 대조. `remaining_check`는 JUDGMENTS의 상세 연결을 통해 보존. 마감 --final은 §4에서 별도 확인. |
| Q1–Q8에 서로 다른 출처2종류 또는 실행 수치표+구체 사례 | 예 | 이 문서 §2의8행. Q1–Q4는 템플릿/이력/설계/리뷰/논문/표준을 구별했고 Q5–Q8은 수치와 실제 C사례를 함께 제시. |
| 다른 분야의 독립 정답원 평가3건 원문 비교 | 예 | evidence/methods/CROSSFIELD.md: 특허 M05·M07, 법률 M09, 학술 M12; 실제 인용·심사관 인용과 관련성·자기/관행 인용·pool 누락을 구별. M06·M08·M10·M11은 추가 대조. |
| 반례5가지 각각 찾으려 한 기록 | 예 | COUNTEREXAMPLES §1–5, SEARCH_LOG, evidence/counterexamples/SEARCH_LOG의 CE-Q01–06, REVERSALS, runs 및 링크 재확인 원장. 더 나은 후보·실제 효과의 미확인은 숨기지 않음. |
| RESULT §4에 정확히3건의 약점과 다음 조사 | 예 | §4.1 내부 선택 중심·시기/역할 경계(80문서), §4.2 조건부 참고와 실제 효용 간격(20사례·100후보·설계자5명), §4.3 현재 웹 단회와 충분성 비교 간격(12과제×3조건×3회). 각 항목의 근거·결론 영향·질문·자료·최소 규모를 확인. |
| SELF_CHECK 통과 뒤 HANDOFF 작성 | 아니오(최종 마감 검사 대기) | 현재 SELF_CHECK의 내용 점검과 data19항목은 완료. §4의 session check 및 --final 실제 결과를 갱신하고 SELF_CHECK 묶음을 커밋한 뒤에만 HANDOFF를 작성한다. |
| 사례 외 본문20개 이상·한 사이트 최대3개 | 예(비사례 최소수에 대한 사전 해석) | SOURCE_COUNT의26개/14사이트/최대3개, 모든 산입 항목 D1. SAMPLING의 첫 커밋부터 비사례에 상한을 적용한다고 명시. 같은 자료의 재열람·다른 endpoint는 새 최소수로 세지 않음. |
| 사례 호스팅에도 사이트당3개 상한을 적용하는 문자적 해석 | 아니오 | 대부분 사례가 GitHub 고정 판이므로 이 해석으로 사례30개를 충족했다고 할 수 없다. SAMPLING과 RESULT §5에 공개한 방법 해석의 한계다. 본문 근거를 덜 읽은 문제가 아니라 집계 단위의 차이이며, 사전 계획을 이 사후 점검에서 숨기거나 바꾸지 않는다. |
| 템플릿·절차4개 이상 | 예 | R-TEMPLATE-PRIOR-MERGE, PS-T-PEP12, PS-T-SWIFT-INITIAL, K-TEMPLATE-NOW. TEMPLATES는 각 절의 원 이력도 별도 확인. |
| 테스트 컬렉션·풀링·누설 방법론4개 이상 | 예 | M01·M02·M03·M04·M15·M16의6개, SOURCE_COUNT와 CROSSFIELD/방법론 비교. 논문의 실험 재실행을 주장하지 않음. |
| 다른 분야 검색 평가 개요3개 이상 | 예 | 특허 M05·M07, 법률 M09, 학술 M12의4개 개요/3분야. 도메인별 정답원 편향과 이번 본문 gold의 대응을 기록. |
| 009에 없는 생성형 인용 정확성 평가2개 이상 | 예 | M13 CiteEval·M14 correctness/faithfulness 논문. SOURCE_QUALITY_REVIEW에서 고정009 자료13파일의 제목·식별자와 대조. |
| 리뷰 토론 원문5개 이상 | 예 | M22·M23·M24·M27·PS-R-S25-DECISION. M25 수락 공고는5개 토론 원문과 별도. S25 root 토론과 /131의 인용 결정은 자료1개로 셈. |
| 질문자·설계자·리뷰어·IR 평가·특허 조사 관점 | 예(문헌을 바탕으로 한 분석) | RESULT §3와 CROSSFIELD의 관점별 한계·편향 대응. 대상 사용자 인터뷰 또는 실제 채택 반응으로 부르지 않음. |
| 필수 축·판정자·시점·정답 밖 후보 분리 | 예 | JUDGMENTS342행/상세62파일, 동일/역사 적중, nongold_useful 및 실제 실행 미실시 표시. 004의 네 라벨을 유지했고 임의 종합 점수를 만들지 않음. |
| owned_path 이외 쓰기·공통 제어 변경 금지 | 예(현재 데이터 검사 범위) | FINAL_VALIDATION의 source_commit 대조와 git status 경계 검사, dot-control.json 차이 없음. 결과는 AF-RES-013 아래만 작성. HANDOFF 후 clean-tree는 마지막에 별도 확인. |

### 한계와 마감 판단

연구 결과의 판정·표·반증 기록은 위 근거로 검토했다. 단, 마지막 자동/세션 검사와 HANDOFF 이후 원격 대조는 수행 시점에만 완료로 바꾼다. 사이트 상한의 문자적 해석 차이는 검사로 해소할 수 없는 범위 해석이며, 조건부 충족이라는 점을 최종 HANDOFF에 그대로 옮겨야 한다. 실제 설계자의 유용성·우월성, 사람 번역, 새 절차 대조, 역할 신뢰도, 모델 학습 누설 제거는 완료한 것으로 표시하지 않는다.
