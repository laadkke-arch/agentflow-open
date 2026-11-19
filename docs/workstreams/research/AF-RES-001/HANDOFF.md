# AF-RES-001 — 최종 인계

## 1. 식별

- **작업 ID / 시도:** AF-RES-001 / 1.
- **작업 종류:** 배정값 `web-pro`; 웹 연구와 GitHub 연결, 제공된 클라우드 작업공간을 사용했다.
- **실제 모델/실행 위치:** 세션 지시의 모델 표기는 GPT-6 Astra Pro. 계정의 모델 선택 UI·요금제는 별도로 조회하지 않았다. 작업공간은 `/workspace/scratch/7eda60c481ca`이며 전체 저장소 checkout은 하지 않았다.
- **공개 작업자 참조:** 별도 native 작업 URL은 확인하지 못했다. 조회 키는 `AF-RES-001#1 / laadkke-arch/agentflow-open / work/research-af-res-001`.
- **역할:** 입력 연구 작성·편집; 두 분야의 별도 근거 조사와 내부 별도 에이전트의 독립 검토를 사용했다. 사람의 검토 또는 다른 모델 간 블라인드 평가로 세지 않는다.
- **저장소/브랜치:** [laadkke-arch/agentflow-open · work/research-af-res-001](https://github.com/laadkke-arch/agentflow-open/tree/work/research-af-res-001).
- **시작/source SHA:** `11137686f238b7a7f66e7fdeb72f5f6c49565486`. 시작 때 작업 브랜치가 없어 당시 최신 foundation의 이 커밋에서 만들고 같은 SHA를 확인했다.
- **마지막 확인·원격 재열람한 저장 SHA:** `b09bd4d10d68aea9ca856c8d52c4cc6a4e7f39fd` (이 HANDOFF의 부모). 본문·사례·검토의 핵심 결과 SHA는 `40f53bec864da98ace69bbfa31c0493c6783dad7`.
- **결과 커밋 식별:** 이 HANDOFF를 추가한 마지막 자식 커밋이 최종 결과다. 자기 커밋 SHA를 본문에 미리 넣지 않으며, 아래 §6의 명령으로 정확한 SHA를 읽는다.
- **마지막 실제 진행 증거:** 연구 11개 파일 원격 blob 일치, 검증 파일 2개 원격 본문 일치, `b09bd4d…`의 Collaboration contract success; 확인 시각 **2026-11-19 15:35:03 UTC**.
- **PR:** 생성하지 않음.
- **최종 인계 작성 시각:** 2026-11-19 15:35:03 UTC / 사용자 날짜 **2026-11-20 KST**.
- **상태: REVIEW_READY.** 문서 연구를 통합 담당에게 넘길 준비가 됐다. dot-control.json의 상태나 result_commit은 이 작업자가 수정하지 않았다.

## 2. 사용자 요구/작업 범위

전체·부분 설계와 목적을 어떤 입력으로 받아 원뜻을 보존할지 조사했다. 같은 합성 원문을 자유문 유지, 가벼운 구조화, AI 분해를 가정한 제안으로 표현해 누락·추측 추가·목적의 잘못된 축소를 대조했다. 필수/선택 정보, 추가 질문이 실제로 답을 바꾸는 조건, 답 없이 할 수 있는 범위와 추측 정지 조건을 남겼다.

고정 입력은 [INPUT_LOCK.json](INPUT_LOCK.json)의 **13개 저장소 문서와 blob SHA**다. AGENTS·STATE·DOT_AUTOMATION·RESEARCH_WORKFLOW·dot-control AF-RES-001 및 [RESEARCH_BRIEF의 input](https://github.com/laadkke-arch/agentflow-open/blob/11137686f238b7a7f66e7fdeb72f5f6c49565486/docs/product/RESEARCH_BRIEF.md)을 직접 읽었다. `depends_on=[]`이므로 읽어야 할 선행 작업 result_commit/HANDOFF는 없었다.

허용 경로는 **`docs/workstreams/research/AF-RES-001/` 하나**다. 공통 색인·계약·진행표·제품 코드·기존 AgentFlow Studio·main은 수정하지 않았다. 검색 엔진·순위·식별 체계·최종 DB/API·AgentFlow 연동 계약의 확정, 배포, 새 유료 모델 API 호출은 수행하지 않았다.

마지막에 foundation이 `46c874671c6d066292750401d75af50136ef95d6`로 이동한 것을 확인했다. 시작 이후 AF-RES-002 배정 기록만 dot-control에 추가된 차이였고 AF-RES-001 항목의 JSON 값은 같았다. 연구 기준을 덮어쓰거나 새 작업 결과를 의존성으로 삼지 않았다.

## 3. 실제 변경

| 파일 | 변경 사항/이유 | 실제 확인 |
| --- | --- | --- |
| [SCOPE.md](SCOPE.md), [INPUT_LOCK.json](INPUT_LOCK.json) | 시작 범위·권한·원문 SHA 고정 | 고정 GitHub 원문과 태스크 대조; 원격 재열람 |
| [RESEARCH.md](RESEARCH.md) | 조건별 대안·정보 후보의 오류 근거·질문/정지 조건·조합·미해결·색인 제안 | 별도 검토와 문장별 사례 대조 |
| [CASES.json](CASES.json) | 6개 합성 입력, 36개 원문 문장, 18개 표현, 문장별 대응·축약 손실, 18개 합성 반례, 12개 조건부 질문 | 원문 동일성·참조 검사 및 별도 의미 대조 |
| [evidence/architecture.md](evidence/architecture.md)와 대응 sources JSON | 구조·관점·인터페이스 자료 A01–A09 | 공식 문서 9개 본문 관련 절 직접 열람 |
| [evidence/clarification.md](evidence/clarification.md)와 대응 sources JSON | 공공 양식·요구공학·출처 모델·정보검색/HCI 자료 B01–B09 | 원문 9개 직접 열람; 효과 일반화 한계 기록 |
| [evidence/software.md](evidence/software.md)와 대응 sources JSON | 실제 소프트웨어·프로토콜 반례 C01–C10 | 10개 문서/코드 직접 열람; Paperless 버전/커밋 고정 |
| [REVIEW.md](REVIEW.md) | 독립 검토의 초기 지적·최소 반례·수정 확인을 보존 | 발견 8건 모두 수정 확인; 남은 범위 한계 기록 |
| [VALIDATION.md](VALIDATION.md), [VALIDATION.json](VALIDATION.json) | 실제 명령·입력 해시·종료 코드·원격 비교·CI 관측·미실시 | 기록에 실린 코드도 다시 추출해 실행, 원격 본문 재열람 |
| HANDOFF.md | 최종 인계와 다음 첫 행동 | 마지막 단독 파일 커밋 대상으로 작성 |

묶음별 커밋:

1. `6fc0e2ffcc48cd29ac72a5544e83d8950dedf0fb` — 범위/입력 고정.
2. `884ccd3cb267d7b42f69a8297e3f615f4dcea64f` — 출처 28개 근거·한계.
3. `40f53bec864da98ace69bbfa31c0493c6783dad7` — 같은 원문 세 표현, 비교 본문, 독립 검토 수정.
4. `b09bd4d10d68aea9ca856c8d52c4cc6a4e7f39fd` — 검증·재현 기록.
5. 이 파일을 추가한 마지막 커밋 — HANDOFF.

## 4. 실제 검증 결과

- **자료 열람:** 서로 다른 실제 자료 **28개**를 본문 관련 범위까지 열어 읽었다. 검색 결과·목차만 본 자료·열람 실패·같은 문서 버전/절은 신규 개수에 더하지 않았다. 각 출처의 URL·확인일·고정 버전 또는 절·확인 내용·한계가 evidence에 있다. 문서 설명 D1과 코드 관찰 D2를 실행 D3·적용 D4로 올리지 않았다.
- **로컬 구조 검사:** Python 3.12.14, [VALIDATION.md §2](VALIDATION.md)의 실제 명령. CASES 원문과 A 일치, B/C 참조, source ID, 제안의 미확인 상태, 36개 수작업 손실 기록 존재, 상대 링크를 확인했다. 마지막 해당 실행의 종료 코드 **0**. 입력 SHA-256과 stdout 요약은 VALIDATION.json.
- **검사 과정 오류:** 검사기가 K05의 조건 변경 제안 상태를 허용 집합에서 빠뜨려 첫 실행 코드 1; 의미가 다른 그 상태를 명시한 뒤 통과했다. 원격 대조의 INPUT_LOCK 줄바꿈 1개 차이는 로컬을 기커밋 원본과 맞춰 해결했다. 두 실패를 검증 기록에 남겼다.
- **독립 검토:** 여섯 외부 핵심 주장 묶음과 여섯 사례를 별도로 대조했다. 높음 2·중간 4·낮음 2, 총 **8건** 모두 수정본을 재열람해 확인했다. 28개 자료 전체의 모든 주장을 독립 재검증했다고 주장하지 않는다.
- **원격 저장:** `40f53bec…`에서 연구 11개 파일 본문을 다시 받아 로컬과 Git blob SHA가 모두 같음을 확인했다. `b09bd4d…`의 VALIDATION 두 파일도 제출 문자열과 원격 본문이 정확히 같았다.
- **변경 범위:** 기준→연구 커밋 compare의 변경 파일은 모두 owned_path 아래다. 마지막 HANDOFF 커밋 뒤에도 범위를 재조회한다.
- **자동 CI:** [연구 SHA의 run 44555557113](https://github.com/laadkke-arch/agentflow-open/actions/runs/44555557113) 및 [검증 SHA의 run 44556153708](https://github.com/laadkke-arch/agentflow-open/actions/runs/44556153708)의 Collaboration contract는 completed/success. workflow 명령은 `python -m workbench.session check-all --fetch`. 앞 run의 job/step과 workflow 원문도 읽었다. stdout/receipt나 숫자 종료 코드는 확보하지 않았으며 의미 보존·검색 품질·전체 환경 검사 통과로 부르지 않는다.
- **이 HANDOFF 작성 후 최종 상대 링크 검사:** 2026-11-19 15:35:26 UTC에 VALIDATION.md §2의 코드를 문서에서 추출해 다시 실행했다. 연구 디렉터리 파일 14개, JSON 문법, 내부 상대 링크를 확인했고 `pending_final_file=[]`, 종료 코드 **0**이었다. 이 검사도 의미 정확도의 자동 판정은 아니다.
- **미실시:** 로컬 전체 저장소/workbench/cloud_check, 제품 실행·배포, 추가 분해 모델 실행, 검색 정확도/순위, 사용자 시간·질문 답변 가능성, 실제 새 대화 인계 시험. 문서 연구에는 제품 실행이 필수 전제가 아니며 실행된 것처럼 보고하지 않는다. 통합 담당이 전체 검사를 요구할 때의 명령·입력은 VALIDATION.md §4에 있다.

## 5. 판단·근거

**채택할 연구 판단:** 원문을 되찾을 수 있게 유지하면서, 이미 제공된 목적·선택 범위·조건의 **대상, 부정, 시점, 강제성, 명시/해석 지위**를 보존하는 쪽을 우선 검토한다. 모든 정보를 첫 입력에 필수로 받는다는 결론은 아니다. 추가 질문은 답이 바꾸는 구체 판단이 있을 때만 후보가 되며, 답이 없으면 원리 비교 등 가능한 범위는 계속하고 그 적합성 주장만 보류할 수 있다.

**보류:** A/B/C의 우열, 고정 입력 필드/enum, 자동 분해 효과, 최적 질문 수. 여섯 사례는 정돈한 6문장 합성 입력이고 K01도 전체 경로의 짧은 요약이다. 실제 장문·그림·잘린 대화·복잡한 설계 전체에 대한 효율이나 충실성을 입증하지 않는다.

**수정·제외한 초기 판단:** source_span이 붙었다는 이유로 제안의 의미 보존이 됐다고 세면 안 된다. 직접 작성한 제안에서도 금지·시간 조건이 빠졌다. 36문장별 참조 유무와 실제 손실을 나누어 기록했다. “제안만 전달”이나 default 사용 자체를 보편적으로 금지하지 않고, 필수 의미를 잃거나 근거 없이 확정하는 경우로 실패 조건을 좁혔다.

주요 반례와 근거를 재사용할 때:

- **위치·부작용:** Paperless 내부 원본 보관과 처음 입력한 폴더의 파일 유지가 다르다. 중복 옵션의 개발/이전 버전 의미와 일부 삭제 코드를 함께 보아야 한다. C03–C05·C10은 고정 커밋 URL·위치를 [software.md](evidence/software.md)에 기록했다. 특정 설치에서 실행된 사실은 아니다.
- **관점·시점:** [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0), [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html), [HTTP 202](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.3)는 관점·설계 관계·접수/완료를 구별할 근거다. 합성 K03의 jobId/콜백은 원문에 둔 조건이며 HTTP 202에서 추론해 만든 것이 아니다.
- **조건의 차이:** [Automerge의 네트워크 동기화](https://automerge.org/docs/tutorial/network-sync/)는 단절 중 작업과 재연결 이후를 나눈다. 이것을 영구 무통신과 같은 것으로 읽으면 안 된다. K05의 양립 불가 판단은 원문 두 조건에 대한 논리 추론이다.
- **질문/요구의 한계:** GOV.UK·NASA·W3C·Qulac·mixed-initiative HCI 근거 B01–B09에서 참고 원리와 일반화 한계를 분리했다. 질문이 항상 이득이거나, 목적 중심이라는 이유로 명시 기술 제약을 지워도 된다고 결론 내리지 않았다.

출처 확인일은 **2026-11-19 UTC / 2026-11-20 KST**다. 합성 사용자 문장, 공개 구현 사실, 연구자 해석과 제안을 구분했다. 모든 C 제안의 `user_confirmed=false`, 사례 질문의 `asked_to_user=false`를 유지한다.

다른 세션과 파일 충돌은 owned_path 제한으로 피했다. 입력 연구의 용어를 다른 AF-RES 결과와 합칠 때에도 이 문서의 정보 후보를 최종 API/DB 계약으로 승격하지 말아야 한다. 공통 색인 반영 제안은 **RESEARCH.md §12의 한 행**이며 직접 수정하지 않았다. 저장한 외부 자료는 URL과 요약·관찰이며 원문 전체·비공개 자료·인증정보를 포함하지 않는다. 설치/배포·권한·새 유료 API 비용 변경은 없다.

## 6. 다음 대화의 첫 행동

**진행·통합 담당의 첫 작업은 이 연구를 다시 시작하는 것이 아니라, 정확한 마지막 커밋을 읽고 완료 근거와 색인 제안을 검토하는 것이다.** 이 작업자에게 남은 차단 사유는 없다.

```sh
git fetch origin chore/workspace-foundation work/research-af-res-001
git rev-parse origin/work/research-af-res-001
git log -1 --format=%H origin/work/research-af-res-001 -- docs/workstreams/research/AF-RES-001/HANDOFF.md
git show origin/work/research-af-res-001:docs/workstreams/research/AF-RES-001/HANDOFF.md
git diff --name-only 11137686f238b7a7f66e7fdeb72f5f6c49565486 origin/work/research-af-res-001
```

전체 checkout이 없는 환경에서는 GitHub의 해당 브랜치 HEAD/ref와 이 파일을 직접 fetch하면 된다. 위에서 얻은 HANDOFF 커밋이 최종 `result_commit` 후보이며, 태스크 진행표의 반영 여부는 진행 담당이 판단한다. PR은 생성하지 않았으므로 새 PR 존재 여부는 필요한 시점에 조회한다.

그다음 [RESEARCH.md](RESEARCH.md)의 **3·5·6·11·12절**과 [REVIEW.md](REVIEW.md)의 **2·3·6·7절**, 필요 사례만 읽는다. 핵심 비교 입력은 `40f53bec864da98ace69bbfa31c0493c6783dad7:docs/workstreams/research/AF-RES-001/CASES.json`이다. 기대 결과는 대안의 적용 조건을 보존한 연구 인수 및 공통 색인 반영 판단이다. 문서 상태 REVIEW_READY를 제품안 채택이나 자동 DONE으로 해석하지 않는다.

답을 바꿀 가장 작은 후속 확인은 **공개 장문 원문 1개와 그 선택 부분 1개를 고정하고, 같은 원문의 A/B/C에서 별도 독자가 금지·대상·시간 조건을 되찾는지 대조하는 것**이다. 원문에 없는 정보를 추가했는지와 확인에 든 부담을 함께 기록한다. 이번 6문장 비교가 보여 주지 못한 조건에서 B/C가 도움 되는지 판단할 수 있다. 새 유료 모델 호출이나 다른 과제 완료를 이 확인의 선행조건으로 두지 않는다.

새 작업 ID는 배정하지 않았다. `depends_on=[]`이며 다른 작업의 미완성 산출물 의존은 없다. 이번 문서 연구 안에 추가 승인 대기는 없다. 최종 제품 계약 변경·배포 등 범위 밖 행동을 이 인계만으로 시작하지 않는다.

