# AF-RES-016#1 — HANDOFF

## 0. 인계 상태

**핵심 산출물·내부 이중 코딩·수치 분석은 커밋했다. 지정 고전 원문 2편의 직접 열람은 막혀 있으므로 전체 요청을 무조건 완료로 표시하지 않는다.**

- 브랜치: `work/research-af-res-016`
- owned_path: `docs/workstreams/research/AF-RES-016/`
- source_commit: `24b22f8a068d02fa5be2aaaa0df50d241f7602a4`
- 이 HANDOFF 직전의 자기 점검 커밋: `3c95eb211d179da75b129ac9864213eefa6846cf`
- 상태: `core_artifacts_complete_with_blocked_named_original_reading`
- 첫 결과 파일: [RESULT.md](RESULT.md). 방법·수치 원본은 [AGREEMENT.md](AGREEMENT.md), [IMPACT.md](IMPACT.md), [VOCAB_MAP.md](VOCAB_MAP.md), [sources.json](sources.json).
- 산출물 구조·동결·표본 재현·수치 일관성 점검: **72개 PASS**. [SELF_CHECK.md](SELF_CHECK.md), [validation.json](evidence/validation.json)
- 미충족: **Hooper(1965)·Markey(1984) 지정 원문 본문 0/2편 확보**. 추가 32질의·10개 공개 URL 시도 뒤에도 본문이 없거나 접근 실패였다. 다른 직접 문헌으로 대체 열람했다고 세지 않았다.

사용자 지시의 보강불가 예외에 따라 막힌 이유와 답을 바꿀 최소 추가 확인을 SELF_CHECK §3에 기록한 뒤 이 인계를 작성했다. 기계 판독 [acceptance-evidence.json](evidence/acceptance-evidence.json)의 `all_named_classic_original_bodies_read=false`와 Q7의 문서 감사 범위를 함께 전달해야 한다. dot-control.json·공통 색인·제품 계약은 변경하지 않았다.

## 1. 직접 읽은 SHA

| 입력 | 고정 SHA | 읽은 핵심 내용 |
| --- | --- | --- |
| chore/workspace-foundation | `24b22f8a068d02fa5be2aaaa0df50d241f7602a4` | AGENTS.md, STATE.md, docs/DOT_AUTOMATION.md, docs/RESEARCH_WORKFLOW.md, docs/product/RESEARCH_BRIEF.md, AF-RES-016 control 항목 및 시작 지침 |
| AF-RES-011 | `478c301b693896e2c6d777f46ac441f071bfdfe8` | HANDOFF, CODEBOOK, RELIABILITY, original/blind/selection·대응 mapping, CASES의 기존 역할; 원149 재계산만 수행 |
| AF-RES-012 | `cb602858378db90adb1f085953016267f9afbd6d` | HANDOFF, corpus entries/규칙, queries, qrels·independent·설명/검토 기준 |
| AF-RES-004 | `2b798c7d2b7355b649691c18de196104ceabb0f0` | HANDOFF, PROTOCOL v1.1, CASES, EXPECTED; L/E/H/T 축은 변경하지 않음 |
| AF-RES-003 | `b13db3931b4021ff9e1ac6e404590c09526c3087` | HANDOFF, RESEARCH, CASES; 식별 어휘·저장 원리 인용. URI/SKOS/PROV/FRBR 문헌 재조사 없음 |
| AF-RES-010 | `0603f0d2990c7a501dbdfc45fbbba79155f505fc` | HANDOFF, TRANSFER_CASES, p1/p2 judgments의 T·최종판정·bucket |
| AF-RES-001 | `4d6208c08f6f2657865ba000d6768f6537e832b6` | HANDOFF, RESEARCH와 입력/제안 상태의 고정 자료; Q8에만 사용 |
| AF-RES-002 | `62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1` | HANDOFF, RESEARCH의 후보 유지·보류·중단 표현; Q8에만 사용 |

모든 선행 결과는 위 SHA에서 직접 읽었으며 통합 브랜치의 존재를 가정하지 않았다. 세부 입력 경로·해시는 [manifest.json](manifest.json), [sample/selection.json](sample/selection.json), [vocab-sources.json](evidence/vocab-sources.json)에 있다. 같은 묶음의 AF-RES-013~015 결과는 읽거나 기다리지 않았다.

## 2. 실제 실행 위치·모델·동결 순서

실행 위치는 `/workspace/scratch/933a99540aa1/agentflow-open`이다. Linux/Bash·Python 표준 라이브러리·Git을 사용했고 저장소 원격 커밋/브랜치를 갱신했다. 세션에 표시된 모델 표기는 **GPT-6 Astra Pro**다. 숨은 backend model identity를 따로 검증한 것은 아니다.

작업자 A는 선행 연구를 읽고 표본을 준비한 같은 세션의 연구자 어시스턴트다. B는 `/root/coder_b_fresh`라는 **새 문맥의 내부 별도 코딩**으로 CODEBOOK과 sample/units.json만 제공했다. 사람, 다른 모델, OS 수준의 접근 격리라고 부르지 않는다. 입력 요약에 남은 선행 해석, 이름 지식의 일부 보충, A의 선행 라벨 노출을 한계로 남겼다.

| 동결 단계 | 커밋 | 확인 |
| --- | --- | --- |
| SCOPE/CODEBOOK | `68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0` | 코딩 전 동결; 23개 값에 표본 외 경계 예 각3개 |
| 198개 표본 | `019f0fcc6ee07946cd337aa43fb708784dd67e5a` | 011120 + 01260 + 00418; 기존 역할/판정 필드 제거 |
| A 원응답 동결 | `0981732949cdea358c4ffa27aafd4ae50d310bbe` | 198행×3안; 원 TSV와 JSON 보존 |
| B 원응답 | `674f1c8eb99e531acee7531c8f1495f721c4dffd` | A 커밋의 직접 자식; 198행×3안 원응답 보존 |

총 **594개 분류안별 대응쌍, 1,188개 코딩 응답**이다. S3는 형태×기여의 결합 한 응답으로 세며 기여는 S2와 같은 변수다. 사후 진단은 별도 adjudication.json에 저장했고 A/B 의미값과 코드북을 고치지 않았다.

## 3. Q1–Q8 결론 한 줄과 적용 한계

| 질문 | 결론 한 줄 | 적용 한계 |
| --- | --- | --- |
| Q1 | 공식 체계들은 형태·배포 단위·일반 사용 목적·관계를 서로 다르게 나누며 보편적인 단일 역할 축은 없다. | 공식 필드의 의미를 확인한 것이며 특정 문제의 whole/part를 모두 대체한다고 검증한 것은 아니다. |
| Q2 | 특허의 기능/용도, 서지 형식/주제, PICO I/C, 패턴 추상도는 안정적 대상 정보와 맥락 역할을 병행한다. | 네 분야의 원칙을 소프트웨어 추천에 이식한 성능은 미측정이다. |
| Q3 | 원011 75/149=50.34%, κ0.382는 안정적 역할 전제에 약한 근거이며 색인어 overlap과 직접 비교할 수 없다. | 지정 Hooper·Markey 원문 미확인. 다른 실증5건·방법문헌7건을 읽었으나 두 편을 읽었다고 대체하지 않는다. |
| Q4 | S1 후보 속성, S2 선택 범위 기여, S3 형태×기여를 코딩 전에 정의했다. | reference/comparison·document/data·하위 기능 단위 경계는 여전히 불완전하고 S3는 S2와 중첩된다. |
| Q5 | 198단위×3안의 이중 코딩과 A→B 동결 순서를 원응답·Git 이력으로 보존했다. | 같은 모델 내부 별도 코딩이며 사람 간 재현성이나 타 모델 일반화 실험은 아니다. |
| Q6 | Po가 높은 안은011·012에서S1,004에서S2였다. 59개 불일치 진단은35/18/6이다. | 표본·범주·과제가 다르다. 같은120의 새S1−원점차+23.33pp 구간은[−7.00,+46.55]pp로0 포함. |
| Q7 | 같은 단위의 수기 문서 판정을 두 역할에 재사용한30개 감사에서는 판단을 유지할 수 있었다. 잘못된 product 필터는 적합 후보3/7을 잃었다. | 0/30은 독립H/T 실험이나 인과 효과가 아니다. 14개INSUFFICIENT·15개라벨미부여의 영향이 크다. |
| Q8 | 동일성·적용·근거·전이·검색 관련성 및 입력/반응 지위를 나누어42행을 대응시켰다. | 공통 schema나 자동 변환기를 확정하지 않았고 대응표의 사용자 효과는 미측정이다. |

### 수치의 핵심

| 안 | 011 120개 | 012 60개 | 004 18개 |
| --- | --- | --- | --- |
| S1 | 94/120=78.33%; κ0.697 [0.562,0.836] | 59/60=98.33%; κ0.973 [0.908,1.000] | 17/18=94.44%; κ0.915 [0.625,1.000] |
| S2 | 85/120=70.83%; κ0.538 [0.372,0.595] | 54/60=90.00%; κ0.831 [0.698,0.947] | 18/18=100%; κ1.000 [1.000,1.000] |
| S3 결합 | 75/120=62.50%; κ0.561 [0.426,0.656] | 51/60=85.00%; κ0.818 [0.710,0.915] | 17/18=94.44%; κ0.930 [0.725,1.000] |

구간은 같은 두 코딩 아래의 5,000회 cluster bootstrap이다. 01115스레드,01231질의,0044문제를 재표집했으며 작은 편의표본에서95% coverage를 검증하지 않았다. 004 S2는 미정의 κ 복제301/5000을 제외한 퇴화 [1,1]이므로 새 문제의 완전 일치 보장이 아니다. 012를 상위12문제로 묶은 민감도와 두 축별 수치는 AGREEMENT에 있다.

## 4. 가장 강한 근거 3개

1. **동결한198단위의 원코딩과 독립 산술 재계산.** A/B 원 TSV·JSON, 같은011120개에서의 원66/120과 새94/120 비교, cluster별 bootstrap·층별 민감도까지 보존했다. 별도 내부 감사가 analyze.py 함수를 재사용하지 않고 점추정·구간을 재계산해 같은 값을 얻었다. [AGREEMENT](AGREEMENT.md), [verification-audit](evidence/verification-audit.md)
2. **공식 체계가 이미 형태·사용·관계를 구별한다는 직접 원문.** SPDX 목적/추가목적, CycloneDX type/scope/isExternal, CPC의 기능·용도 동시 분류, MARC 형식/주제, PICO 비교 위치는 '모든 역할이 후보 자체의 한 속성'이라는 가정을 제한한다. [SCHEMES](SCHEMES.md), sources S01–S03·S15·S17·S18
3. **라벨을 적합성으로 치환할 수 없는 고정 사례.** 004 product-only 필터는 DIRECT7개 중3개를 제외하고 A의통과7개중mismatch2개·B의8개중3개를 남긴다. 010 mapped13/25중3개가mismatch이며, Paperless는012의질의에따라1/N/N이다. 같은 역할·대상·전이 설명도 H 또는 검색 관련성의 대리값이 아니다. [IMPACT §5](IMPACT.md), [VOCAB_MAP §4](VOCAB_MAP.md)

## 5. RESULT §4의 가장 중요한 약점 3건

1. **규칙 적용 비대칭과 중첩 과제:** A의011 comparison0개 대B14개, S3가S2를공유하는구조가 안별 차이에 섞였다. 새로운 우선 규칙과 새60단위·사람3명의 코딩으로 확인해야 한다.
2. **표본과 후보 단위:** 012의36/60 무작위질의연결,011의두스레드65/120,004의합성4문제, 실행물/문장/묶음 단위의 혼합이 일반화를 막는다. 후보30개×실제문맥3개=90단위와30개이상문제묶음이 다음 최소 설계다.
3. **사람과 표시 효과의 부재:** 내부 두 코딩과 공통 수기 H/T 감사는 사람 간 재현성·역할 표지의 인과 효과를 측정하지 않았다. 실제 불일치30개에 표시없음/A/B를 배정한 최소90판정노출·평가자3명 이상이 필요하다.

세 안 중 하나를 확정하지 않는다. S1은 선명한 배포 단위의 거친 색인, S2는 명시된 선택 범위와 사용 제안, S3는 형태·기여를 따로 설명하고 불일치를 추적하는 상황에서 각각 유용할 수 있다. 각 안의 실패 조건도 RESULT §3.1에 남겼다.

## 6. 검증한 것과 미실시

| 구분 | 실제 수행 또는 남은 것 | 증거 수준·주의 |
| --- | --- | --- |
| 본문 열람 | 방법·체계38건 직접 읽음: 핵심36+추적2. 보수적 사이트당3개 상한 후 최소계상34건 | D1/D2. 고정 선행입력18건·후속 후보 공식본문3건은 이 최소수에 더하지 않음 |
| 최소 구성 | 공식 소프트웨어8체계, 다른 분야4종, 색인 실증5건, 소프트웨어 실증1건, 지표 문헌7건 | sources.json의 source_type·sections_read·limits와 source-audit.json |
| 표본 재현 | 고정 Git 입력에서 sample/select.py를 메모리 내 재실행; units/baseline/selection/LIST 바이트 동일 | D3-run. 원149의 원 라벨 재코딩은 안 함 |
| 코딩 보존 | A/B 각198행, raw↔JSON 의미 동일, S3기여=S2, freeze/provenance 해시 동일 | D3-run 구조/보존 검사; 역할의 외부 정답 검증 아님 |
| 수치 | Po/κ·5,000회cluster구간·동일120차이·012층별 및상위문제민감도·유형59개 | D3-run 계산. 진단 유형35/18/6은 사후 연구자 해석 |
| 판정 영향 | 실제 불일치30개를 수기 검토, 동일 판단의 두 역할 표시 재사용. 내부 별도 검토에서3표현문제를 고쳐 로그 보존 | H 문서 감사. 독립 H/T 재코딩 또는 사람 판단의 변화 실험 아님 |
| 반례 실행 | RFC replace 도착 역순 toy, 시간 기반 진입의 처리중5개 toy, 잘못된 역할필터36행(18×2) 계산 | D3-run 수학/규칙 예시. RFC 전체·aiolimiter 라이브러리·실제제품통합을 실행한 것은 아님 |
| 어휘 대조 | 7연구42행,00418행·01025사용방식·012235/277판정행 재집계 | 고정 연구자 판정·관측코딩. 외부 금표준 아님 |
| 미실시 | 사람·다른모델 재현성, 완전 문맥가림S1, 실제 역할표지 인과실험, 후보 실제통합(D4) | 질문별 적용 한계와 최소 후속 설계를 RESULT §4에 기록 |
| 막힌 지정 원문 | Hooper1965·Markey1984 본문 미확보; Cohen1960도 직접읽은원문으로표시하지 않음 | 실패·snippet52시도 기록 제외. 공백은최소개수충족과별도로유지 |

내부 별도 검토는 사람 검토라고 부르지 않는다. 프로필·사용자명·공개 게시물 본문 전문을 새로 저장하지 않고 URL/ID/짧은 요약을 남겼다. 신규 유료 API·계정·로그인·권한 변경·배포·상시 수집·네트워크 제한 우회는 수행하지 않았다.

## 7. 재현 명령과 미실시 확인의 입력

### 7.1 이미 수행한 산술·보존 검사의 재현

입력은 아래7개 선행 SHA의 Git 객체, 동결 CODEBOOK.md, sample/units.json·baseline.json, coder-a/b.json이다. 저장소 루트에서 다음 명령을 실행한다. clone에 선행 객체가 없으면 `git fetch origin <위 §1의 해당 SHA>`로 정확한 객체만 가져온다.

```bash
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/analyze.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/build_impact.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/toy_counterexamples.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/vocab-inventory.py
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/validate_delivery.py
```

`build_impact.py`는 수기 판단의 직렬화이고 재코딩 모델 호출이 아니다. `validate_delivery.py`는 validation.json의 실행 시각·현재 HEAD를 갱신하므로 새 검사를 수행한 경우 그 새 기록도 별도로 커밋한다. 원 A/B, CODEBOOK, frozen sample을 변경하지 않는다.

### 7.2 막힌 원문 열람을 재개할 입력과 명령

현재 빠진 입력은 **정상 접근 가능한 원문 본문 URL**이다. 서지·검색 입력은 이미 reliability-supplement.json의 target_status/search_log에 있다.

- Hooper: `Indexer Consistency Tests`,1965. TR95-56과TR-95-96 표기를 원표지에서 먼저 구별해야 한다. 공개 IBM/FID 원스캔이 필요하다.
- Markey: `Interindexer consistency tests: A literature review and report of a test of consistency in indexing visual materials`, *Library & Information Science Research*6(2):155–177,1984. 공개 저자판/기관판 또는 정상 접근 가능한 발행사 본문이 필요하다.

새 공개 URL을 확보한 뒤 같은 검색 도구에서 실행할 명령 형태는 다음과 같다. placeholder는 실제 원문 URL로 교체해야 하며, 지금 확보했다고 주장하는 주소가 아니다.

```javascript
await tools.mcp__codex_apps__search_service_web_run({
  open: [{ref_id: "NEW_PUBLIC_ORIGINAL_URL"}],
  response_length: "long"
});
```

표지·판/보고서번호 → 계수 정의 → 표본/비교쌍 → 결과표 순서로 읽고, 새 출처 항목의URL·시각·절·확인내용·한계를 기록한다. 참여자 수 등 후속 문헌의 차이를 먼저 대조한다. 전문을 저장하거나 접근 제한을 우회하지 않는다. 원문을 실제 읽기 전에는 `original_body_read`나 acceptance의false를true로바꾸지 않는다.

### 7.3 사람·표시 효과 확인을 위한 최소 실행 입력

사람의 재현성/판정 실험은 이 세션에서 수행하지 않았다. 입력은 RESULT §4의새60단위 또는후보30×문맥3단위와, 실제 사용·설정·필수조건·문서근거가 갖춰진불일치30개다. 각 행에는 `candidate_id, problem_id, selected_scope, proposed_use, configuration, evidence, label_condition`이 필요하다. 현재 sample/units.json의빈proposal을사실인것처럼채우면안된다.

역할표시없음/A/B를 고정시드로 배정하고 같은 평가자가 같은 사례의 다른 표지를 보지 않게 한다. H 조건별값·T·근접오답·근거·판정시간을 원응답으로 보존한다. 이는 사람이 필요한 실행 절차이며지금의0/30값으로대신하지 않는다. 제품계약이나DB/API를확정한입력 schema 제안은아니다.

## 8. 색인 변경 제안 — 한 행

| 제안 항목 | 연결할 결과 | 함께 남길 제한 |
| --- | --- | --- |
| AF-RES-016: 후보 형태·문제 기여·판정 상태의 분리와 재현성 | 이 브랜치의 RESULT.md·AGREEMENT.md·IMPACT.md·VOCAB_MAP.md·SELF_CHECK.md·HANDOFF.md | 내부198단위3안; 안별조건부결론; Q7수기감사; 지정Hooper/Markey원문미확인. 공통색인실제수정은하지않음 |

## 9. 다음 첫 행동

**Markey(1984) 또는 Hooper(1965)의 정상 공개 원문 URL 하나를 확보해 원표지와 방법·결과를 직접 읽는 것부터 시작한다.** 이미 읽은 후속 인용을 더 모으거나 기존198개를다시코딩하는것으로이공백을대체하지않는다. 원문을확보하지못하면현재수치·원응답을유지하고막힌자료상태를그대로남긴다.

원문 공백 뒤의 가장 가치 있는 새 실행은 후보 단위와 실제 사용 문맥을 고정한90단위 및 역할표시30사례 실험이다. 현재 코드북을 사후 개선해 원198개에 덮어쓰지 말고 새 버전·새표본으로 시작한다.

## 10. 커밋 묶음과 원격 확인

| 묶음 | 커밋 | 내용 |
| --- | --- | --- |
| 1 | `68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0` | SCOPE·CODEBOOK 코딩 전 동결 |
| 2 | `523ea6a1a57b3fcd444455a7a50793b158650b71` | SCHEMES·체계 원문 |
| 3 | `019f0fcc6ee07946cd337aa43fb708784dd67e5a` | 고정시드198표본 |
| 4 | `0981732949cdea358c4ffa27aafd4ae50d310bbe` | coder-a 원응답 동결 |
| 5 | `674f1c8eb99e531acee7531c8f1495f721c4dffd` | 새문맥 coder-b 원응답 |
| 6 | `146805164c24781115d4e5ac5562921242ddd51a` | AGREEMENT·IMPACT·진단·방법문헌·분석 |
| 7 | `e78a067a6aeecf46b3f9f4a3ec4becda82b4cd07` | VOCAB_MAP·RESULT |
| 8 | `3c95eb211d179da75b129ac9864213eefa6846cf` | SELF_CHECK·검증·수치감사·acceptance·PROGRESS |
| 9 | 이 HANDOFF를 추가한 마지막 커밋 | HANDOFF.md만 단독 커밋 |

각 묶음은 끝날 때 원격 브랜치에 반영했다. 이 파일의 커밋 후 원격 파일 본문을 다시 읽어 로컬 UTF-8 본문 및 Git blob SHA와 비교하고, 마지막 커밋의 변경 파일이 HANDOFF.md 하나인지와 작업트리가 비었는지 확인한다. 이 사후 확인 결과와 최종 SHA는 실행 로그·최종 응답에 남긴다. 확인 전 결과를 이 파일에 미리 성공으로 적지 않는다.
