# AF-RES-186 범위와 실행 계약

## 기준판과 의존

- 작업 브랜치 `work/research-af-res-186`, 시작과 작성 허용 경로 `docs/workstreams/research/AF-RES-186/`. GitHub에서 기존 원격 브랜치가 없는 것을 확인하고 최신 통합판 [fa32c7b](https://github.com/laadkke-arch/agentflow-open/commit/fa32c7b712231bd1d43974ded8072bda5196239f)에서 생성했다.
- 계획판 [128f673](https://github.com/laadkke-arch/agentflow-open/commit/128f673685ec804c526a38e3f89d4d8a43fcd299)과 최신판의 전체 diff는 `docs/automation/dot-control.json` 208줄 추가, 두 커밋이다. PLAN#42 항목을 추가했고 186을 RUNNING으로 등록했다. 실행 기준 문서·연구 색인·계약 파일은 두 판에서 동일하다. [계획판과 최신판 비교](https://github.com/laadkke-arch/agentflow-open/compare/128f673685ec804c526a38e3f89d4d8a43fcd299...fa32c7b712231bd1d43974ded8072bda5196239f)
- 중앙표의 직접 의존은 AF-RES-176 한 건이다. 중앙 DONE과 작업자 자체 PARTIAL을 구별한다. 고정 [HANDOFF.md](https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/HANDOFF.md) 및 그 커밋의 tests.csv, 보충 단언과 S27/S29/S30을 읽는다. 같은 회차 후속 작업의 산출물 의존은 없다. [중앙표](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/docs/automation/dot-control.json)
- [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/AGENTS.md), [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/STATE.md), [Dot 운영](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/docs/DOT_AUTOMATION.md), [연구 운영](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/docs/RESEARCH_WORKFLOW.md), [제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/docs/product/RESEARCH_BRIEF.md)를 적용했다. 세션 계약은 `workbench.session start --fetch`로 만든 [session.json](session.json)이다.
- [연구 색인](https://github.com/laadkke-arch/agentflow-open/blob/fa32c7b712231bd1d43974ded8072bda5196239f/docs/research/INDEX.md)에 JSON-LD, AF-RES-176, AF-RES-186의 동일 질문·출처 등록은 없었다. AF-RES-176의 시험 정의와 EARL 출처는 겹치는 선행 근거로 재사용하며 이 작업의 신규 관측 단위는 프로세스 실행이다. 색인 편집 제안은 인계에 둔다.

## 시험 범위와 예정 분모

질문은 지정한 JSON-LD 시험판에서 두 구현이 반환하는 값과 규격 오류가 두 번의 새 프로세스에서 일치하는지다. 기간은 이번 Cloud 실행의 실제 UTC 시각이다. 2020년의 보고서 날짜와 실행일은 별도 필드다. 제품 DB·수집기·검색 형식은 후속 설계 비교에 남긴다. 역사적 실행 주체·독립성 조사, 새 자연 표본 및 AF-RES-184는 이번 범위 밖이다.

- 시험판 [w3c/json-ld-api@8811ba2](https://github.com/w3c/json-ld-api/tree/8811ba2a3bcae883ac91efacffb70ef08d84e92f/tests), 구현 [json-gold@0dbcf4d](https://github.com/piprate/json-gold/tree/0dbcf4d641a409700208f66945c0d2af7754fba9)과 [jsonld.js@30f9067](https://github.com/digitalbazaar/jsonld.js/tree/30f9067c40066519c917721b8ca4a374eabf15e7).
- AF-RES-176 [tests.csv](https://github.com/laadkke-arch/agentflow-open/blob/a347a373cdd46910f2cd2cf53419849ba48ee03a/docs/workstreams/research/AF-RES-176/tests.csv)의 두 manifest 내 순서를 유지한다. Expansion 385건 중 순번 1, 2, 3, 123, 161 (`t0001,t0002,t0003,t0123,tc030`), compaction 246건 중 순번 1, 2, 3, 152, 153 (`t0001,t0002,t0003,te002,ten01`). 각 알고리즘에서 양성 3, 음성 2다. 결과에 따른 교체나 보강 표본 모집은 없다.
- 모집 키는 알고리즘 + manifest 문맥으로 해석한 완전한 test IRI다. `expand-manifest#t0001`과 `compact-manifest#t0001`은 각각 다른 입력과 기대 파일을 갖는다. 전체 631 정의의 선택·제외, 판독한 파일, 대조 및 미열람은 frame에 남긴다.
- 예정 40개 실행 = 2엔진 × 10시험 × 별도 프로세스 2회. 엔진 내 반복 비교 20쌍, 엔진 간 비교 10건, 역사적 제출과 현재 판정 비교 20건. 실행/이력/비교기의 분모는 각각 집계한다. 이번 세션의 반복 실행은 한 운영 환경에서 얻는 관측이다.
- 고유 원파일 하한 26은 입력 10, 기대 파일 6, manifest 2, 구현·의존 선언 4, 원 EARL 2, 공식 수행 규칙·비교기·문맥 중 2다. S27/S29/S30은 고정 인계 원장을 읽어 두 합성 구조 대조에만 적용한다.

## 열람 및 판정 순서

1. 배정 및 선행판 → manifest 문맥·순번·종류·링크·옵션 → 10 입력, 6 기대값, 5 로컬 compaction 문맥의 원바이트. test IRI와 입력 document IRI는 각각 보존한다.
2. 공식 suite README와 API → 엔진 checkout·API·로더·옵션·오류 코드와 의존 선언 → 원 EARL의 test/subject/release/assertor/result/date → 대조 → 실행. 출처 파일별 SHA-256, 범위, 원값, 한계와 실패를 원장에 남긴다.
3. 두 API에 원 document IRI를 넘긴다. 같은 Base(입력 IRI), JSON-LD 1.1 및 로컬 context(필요한 5건)를 사용하고 문서 로더에서 원 IRI를 해시 확인한 고정 파일에 매핑한다. 외부 fallback은 없다. `specVersion`은 suite 판 구분이며 네 음성의 명시 값은 1.1이다. 표본에는 `processingMode` 재지정과 `ordered` 설정이 없으므로 1.1을 명시하고 `ordered`는 생략한다. 엔진 내 정렬과 비교기 규칙은 별개로 기록한다.
4. 양성은 suite의 객체 비교 규칙으로 채점한다. 객체 키는 배열 순서와 무관하게 순서를 무시하며, 일반 배열은 중복을 보존한 비순서 비교, `@list` 직하 항목은 순서 비교, JSON 스칼라는 타입과 값을 비교한다. `@language`는 대소문자를 무시한다. 양성 compaction은 실제와 기대를 각각 원 base에서 그 엔진으로 재확장해 @container: @list가 감출 수 있는 순서를 추가 확인한다. 보조 재확장은 실행 40의 분모 밖이다.
5. 음성은 엔진이 보고한 규격 코드의 정확 일치를 요구한다. 코드가 다르거나 값이 반환되면 규격 시험 실패, 로더·빌드·크래시·프로토콜 실패는 비교 불가 또는 미실행이다. 로그·실행 UUID·PID·종료코드를 직접 확인한다. 비교기는 키 순서/일반 배열 양성, 목록 순서/스칼라 타입/오류 코드 음성 대조로 별도 검사한다.
6. 같은 엔진의 반복 일치와 두 엔진의 실제 반환/코드 일치를 구분한다. 역사적 EARL은 같은 시험 IRI 및 보고 엔진판의 판정만 대조한다. suite SHA·옵션·원 로그가 빠진 과거 단언은 과거의 실제 값·독립성·완전 재현을 뒷받침하지 못한다.
7. 파일별 근거·사건·실행·미확인을 검산하고 Q1–Q7과 반례를 결과 및 자기점검에 기록한 후 별도 인계를 커밋한다. 두 엔진 40개 실제 실행과 양·음 대조 및 종류별 열람 하한이 완료 기준이다. 확인된 규격 불합격은 유효한 결과다.
