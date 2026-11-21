# AF-RES-018 — 절차 P v1.0 (실행 전)

## 실행 문맥·입력

당신은 한 질문에 배정된 새 문맥 내부 실행 에이전트다. 이 규칙과 해당 questions/inputs/<qid>.json만 읽는다. gold, sources, SCOPE, 다른 질문, 다른 runs, 저장소 이력과 원 질문의 답을 읽지 않는다. 질문 파일의 summary 또는 hash 검증한 원판 질문만 입력으로 쓴다. 추가 질문을 사용자에게 하지 않는다. 출력은 배정된 runs/P/<qid>.json만, 커밋/브랜치 변경 없음. 실행 모델 표시는 GPT-6 Astra Pro(내부 별도, 사람 아님).

## 공통 한도와 순서

검색 질의12회 이하, 열린 문서/열람시도20개 이하, 출력 후보10개 이하. 검증 문서도 같은20개다. 실패시도도 센다. 실제 조회문/URL/시각/상태/읽은범위/확인내용을 저장하되 공개 본문전문과 사용자명을 저장하지 않는다. 출처당 인용25단어 이하. 원 질문, 복사본, 질문 인용페이지는 제외하고 snippet 노출도 exposures에 기록한다. 날짜 불명의 live 문서는 unknown, 질문이후자료는 post_decision으로 표시한다. 사용한 도구는 A와 같은 공개 웹·코드검색이다. 최소1회 익명공개코드검색을 시도하고 차단시 code-through-web을 명시한다. 새 유료API/로그인/설치/네트워크우회 금지.

자발적 검색이 끝나면 후보순위와 raw_response를 동결해 부모에게 알린다. 이후 부모가 제공하는 세 검사후보에 유지/제외+이유를 낸다. 검색/열람을 추가하면 같은12/20 안에서 센다. 가능하면 검색8회·문서15개 이내에서1단계를 끝내 검사용 여유를 남긴다(강제개수 아님). 검사후보를 본 뒤 자발적 후보목록·순위·원응답을 수정하지 않는다.

## 단계별 입력·출력

### 1. 입력 분해 (도구 예산0)

I1 원문/위치, I2 목적, I3 선택범위/보존할곳, I4 조건의대상·극성·강제성·이유, I5 주변입출력·경계, I6 현재/계획/예시·시점, I7 환경·버전·설정·자료형, I8 원문/해석 관계를 기록한다. 값은 원문 근거와 source_location을 붙인다. 명시/해석·미기재/모름/미정/해당없음/무제약/상충을 구별한다. 부정/금지와 예외를 보존하고 원문에 없는 조건을 생성하지 않는다. 입력이 요약이면 위치는 그 요약의 문장번호이며 원 질문의 직접 인용으로 부르지 않는다.

출력 decomposition=[{item:I1..I8,value,status,source_location,polarity,force,interpretation}]. I4는 복수 가능. 없는칸은 unknown/absent, 강제적 완성 금지.

### 2. 검색 (전체<=12질의/20문서 공유)

I2·I3에서 직접후보 질의를, I4·I5·I7에서 조건/호환성 질의를 만든다. 하나의 익숙한 후보로 멈추지 않고 합리적인 대체방식도 조사한다. 주장 검증을 검색과 같은 예산에 포함한다. 검색 결과 스니펫만이면 미열람, 후보의 공식 문서/공개 코드가 우선이다. 실제 queries와 opened_documents를 기록한다.

### 3. 후보 기록 (문서예산 공유)

형태(form: app/service/library/framework/standard/document/pattern/research/data/mixed/unknown)와 기여(contribution: whole/part/reference/comparison/none/mixed/unknown)를 별개로 적는다. S1의 product/component/principle도 필요시 보조기록. URL이 문서라는 이유로 앱을document로 바꾸지 않는다. 기여whole은 질문이 고른 범위전체이며 라이브러리질문에서 라이브러리가whole일수있다. 형태/기여가 유용성·요구충족을 대신하지 않는다. 출처 AF-RES-016 고정CODEBOOK의 S1/S2/S3 정의를 따른다.

### 4. 제외 조건 대조 (검증도전체20문서)

014 EXCLUSIONS의원칙: 원문 must만, 대상·극성보존, 독립적인복합조건만분리, 공식문서에서 적용제품/버전/설정의 unsupported 또는 required가 명시된 경우만 대조한다. must가 요구하는개념이 unsupported이거나 must가금지한개념이 required일때만충돌. 문서에언급없음·제삼자반박·옵션일부제약·버전범위불명은확인필요. 불필요는금지가아니다. 유지관리요구는명시종료/보관만으로배제하며 업데이트간격을발명하지않는다. 공식문서에 없는 지원범위를 단정하지 않는다.

각 must마다 {target,polarity,source_location,status:pass|fail|unknown,evidence_url,version_scope,reason}. 필수조건이없으면빈배열이지전부pass가아니다. 필요 확인이남은후보는삭제하지않고그사실을적는다. 알려진결정적위반후보는추천목록에서제외하되 rejected_candidates에이유를남긴다. 별도검사후보도같은규칙을적용한다.

### 5. L/E/H/T와 판정 (도구예산0, 새사실필요시공유예산)

L=ok/broken/missing: 실제출처연결. E=supported/contradicted/unknown: 정확한주장지지. H=각must별pass/fail/unknown/not_in_scope. T=not_needed/mapped/analogy_only/unknown. 합산점수로fail을상쇄하지않는다. not_in_scope는처음부터좁힌참고관계에만가능하며전체대안의실패를구제하지않는다.

판정우선순위는004그대로: (1) SURFACE_OR_CONSTRAINT_MISMATCH=결정적인알려진위반/작동관계불일치 (2) INSUFFICIENT=결정적사실·설정미확인 (3) CONDITIONAL_TRANSFER=관계/연결작업/비적용/실패조건까지구체화한좁은참고 (4) DIRECT_DOCUMENTED=제안설정의모든필수조건긍정근거. 문서확인을실행/실사용으로승격하지않는다. INSUFFICIENT는실패와별개이며추가확인한가지및답별판정변화를쓴다.

### 6. 출력

최대10개후보를유용성순서로, 각각한줄이유와원문URL,형태/기여,필수조건별충족·위반·확인필요,004축/라벨을기록한다. raw_response에는실제로만든최종추천답전부를그대로담는다. 후보수채우기금지. 가격·라이선스·플랫폼·기능등의사실은근거URL과연결하며미확인은명시한다.

## JSON 기록

case_id, baseline="P", execution_agent="internal separate context", model_label, context_inputs, started_at_utc, ended_at_utc, gold_seen=false, other_runs_seen=false, decomposition, queries, opened_documents, exposures, candidates, rejected_candidates, raw_response, checks, budget, limitations, execution_status를쓴다.

queries 각행={q,at_utc,tool,result_note}. opened_documents 각행={url,at_utc,status,sections_read,confirmed,published_or_version,date_status,post_decision}. candidates 각행={rank,name,url,reason,application_scope,constraints_or_caveat,evidence_opened,date_status,post_decision,date_evidence,form,contribution,must_checks,L,E,H,T,label}. checks는나중에받은순서를유지하며{check_id,name,decision:keep|exclude,reason,evidence_urls,verification_status,label,must_checks}. 예산은search_queries,opened_pages,candidate_count,stage1_search_queries,stage1_opened_pages. raw_response와stage1_frozen_at_utc를검사전저장한다.

## 한계

이절차는효과검정대상이며정답생성기가아니다. 문서기반판정이며사람시간·실제통합·별도제품가치·학습오염통제를측정하지않는다. 접근실패는미확인으로보존한다.
