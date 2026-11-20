# AF-RES-009 — 선행 시스템 지형

## 결론

**가치의 주요 부분은 이미 여러 시스템과 그 조합이 제공한다.** 선택한 코드·문서와 목적 입력, 부품 수준 검색, 링크를 붙인 설명, 출처 갱신·위험 표시는 각각 실제 선행 기능이다. 새 제품의 필요성을 주장하려면 기존 도구를 함께 쓴 기준선보다 어떤 반복 작업을 줄이는지 보여야 한다. “같은 이름의 단일 제품을 못 찾았다”는 사실로 신규성을 선언할 수 없다. [S-DE04] [S-AC31] [S-F06] [S-DE22] [S-DE25]

가장 강한 경쟁 범위는 세 가지다. 첫째, 이름이나 부품 종류를 아는 개발자는 디렉터리·awesome에서 후보 링크를 얻는다. 둘째, LLM과 기존 코드 검색을 연결하면 부분 문제를 코드 근거로 설명한다. 셋째, 제한된 전문 분야에서는 구조화 입력과 근거 관리까지 결합되어 있다. AWS의 일부 기능은 preview이고 그 링크 중 일부는 외부 해법이 아니라 현재 자원을 가리킨다는 경계를 함께 적용한다. [S-AC02] [S-AC05] [S-AC31] [S-FG22] [S-FG24] [S-FG26]

## 1. Q1 — 조사 지형과 읽는 법

| 범주 | 시스템 수 | 대표 결과 단위 |
| --- | ---: | --- |
| (a) 대안·목록 | 4 | 제품·서비스·전문 목록 |
| (b) 패키지·의존성 메타데이터 | 6 | 패키지 버전·저장소·파일·활동 |
| (c) 코드·저장소 검색 | 4 | 파일·심볼·코드 구간 |
| (d) LLM 개발 조사 | 4 | 질문별 설명·코드/웹 근거 |
| (e) 학술 발견 | 6 | 논문·관계·구현·주장별 구절 |
| (f) 패턴·참조 설계 | 5 | 상황별 패턴·대가·권고 |
| (g) 전문 분야 | 6 | 청구항/분류·임상 근거·인용의 후속 취급 |
| 합계 | **35** | 모든 행에 직접 읽은 1차 자료 |

세부 필드의 원장은 SYSTEMS.json이다. 아래 표는 Q1–Q5와 Q7을 비교하기 위해 줄인 것이다. “운영”은 현행 공식 문서상 제공 상태이고, 실제 검색 실행을 뜻하지 않는다. 역사 시스템과 상태 불명은 따로 표시한다. SCOPE에서 정한 후보 중 1차 본문이 없는 것은 sources.json의 unresearched_systems에 남겼다. AskNature는 자연의 형태·과정·생태계에서 설계 영감을 얻는 인접 프로그램으로 이름과 위치만 표시하고, TRIZ·특허 유추 방법론과 함께 깊은 조사에서 제외했다. [S-X01]

### (a) 대안·목록 디렉터리

| 시스템 | 입력 | 수집·표현·검색 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| AlternativeTo | 제품명·목적어·기능/플랫폼/라이선스 | 이용자 제출·관리자 검토; alternative 관계·태그·투표 | 설명·의견·원제품 링크; 중단 상태도 대체 탐색용으로 보존. 일부 기능 대안 문제를 인정 | [S-AC01] [S-AC02] |
| OpenAlternative | 독점 제품명·분류 | 커뮤니티 목록; 저장소 활동을 가중한 순위 | 코드 링크·짧은 소개·활동 지표. 공개 목록과 사이트 데이터의 권리는 구별 | [S-AC03] [S-AC04] |
| awesome | 분야·기술·부품명 | 사람이 선정한 전문 목록을 연결하는 메타 목록 | 짧은 설명·PR 검토·낡은 항목 제외. 장수하지만 신규 PR 검토 병목 존재 | [S-AC05] [S-AC07] [S-AC37] |
| SaaSHub | 제품명·범주·업체 제출 | 웹 비교 글·투표·알고리즘; 대안 관계 | 공급자 분기 재검증. 세 번째 SPONSORED 위치와 유료 시각 우대가 있음 | [S-AC08] [S-AC09] [S-AC10] |

AF-DOT-001의 역할 판단을 재결정하지 않았다. OpenAlternative는 발견 목록, AlternativeTo는 수동 비교 참고이며 경쟁 DB 수집은 reject로 유지한다. 새로 확인한 것은 입력·부분 대안·활동 점수·권리·갱신과 노출 방식이다. [I-DOT] [S-AC01] [S-AC02] [S-AC03]

### (b) 패키지·의존성 메타데이터

| 시스템 | 입력 | 수집·표현·검색 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| Libraries.io | 패키지·프로젝트·언어/라이선스 | 공개 메타데이터와 버전·의존 관계; 구판 덤프에는 manifest/lockfile 관계 | 저장소/의존 링크. 운영자는 수집 정확도 미검증을 명시; 기존 메타데이터 defer 유지 | [S-AC11] [S-AC12] [S-AC13] [I-DOT] |
| deps.dev | 생태계·패키지·버전·해시 | 레지스트리 피드/스캔; 버전별 전이 의존 그래프·원천 연결 | 라이선스·취약점·출처 관계. 환경별 실제 resolver와 차이가 날 수 있음 | [S-AC14] [S-AC15] |
| ecosyste.ms | 저장소·호스트·패키지 식별자 | 여러 원천을 서비스별로 정규화; 패키지–저장소·패치·목록 관계 | 부품 정체와 활동의 근거. 모든 원천의 공통 최신성을 약속하는 단일 SLA는 아님 | [S-AC19] [S-AC20] [S-AC35] |
| OSSInsight | 저장소·개발자·컬렉션 | GH Archive+공개 이벤트; 시계열/SQL·컬렉션 | 활동 지표 참고. About의 자연어 Explorer와 현재 부분 유지보수 공지가 다름 | [S-AC16] [S-AC17] [S-AC18] [I-DOT] |
| Software Heritage — 현재 상태 불명 | origin URL·SWHID/해시 | lister/loader/재방문; 내용 주소 Merkle DAG·origin/visit | 동일 코드와 출처를 보존. 문서 접근 실패를 종료로 판정하지 않음 | [S-AC23] [S-AC24] |
| npms — 현재 상태 불명 | 패키지명·키워드·한정자 | 변경 피드/오래된 항목 관측→큐→수집·분석→색인 | 품질·인기·유지 축. similar는 이름 유사성이고 기능 대안 판정은 아님 | [S-AC33] [S-AC34] [S-AC36] |

이 범주의 핵심 재사용 가치는 “어떤 부품인가, 무엇과 연결되는가”다. 활동량·인기·다운로드·건강 신호를 “이 설계에 맞는다”로 치환하면 안 된다. Software Heritage의 내용 보존과 deps.dev의 의존성 계산은 목적 적합성 추천과 다른 문제를 푼다. [S-AC14] [S-AC24] [S-AC36]

### (c) 코드·저장소 검색

| 시스템 | 입력 | 수집·표현·검색 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| GitHub Code Search | 문자열·regex·repo/path/language/symbol | Blackbird n-gram 역색인; 쿼리 파싱·후보 파일 재검사 | 코드/정의·참조 링크. push 기반 갱신, 기본 브랜치·파일·결과 제한 | [S-AC25] [S-AC26] [S-AC27] |
| Sourcegraph / Zoekt | 코드 검색식·revision; 자연어+scope | 연결한 코드의 shard·색인/비색인 경로; Query Assist가 검색식 제안 | 코드·변경·리비전 문맥. 자연어 입력이 이미 있으나 생성 검색식은 검토 대상 | [S-AC28] [S-AC29] [S-AC30] |
| grep.app + MCP | 부분 질문을 받은 LLM의 패턴·regex·필터 | 공개 GitHub 코드 색인; MCP가 구간과 링크 반환 | 공식 예제가 부분 문제→연속 검색→파일/행→설명을 보여 줌 | [S-AC31] [S-AC32] |
| searchcode — 재출발 | 지정 repo·하위 경로·symbol/행 | 지정 Git 저장소 분석·Boolean/regex/구조 검색 | 같은 기능의 여러 구현 비교; 옛 전역 발견 색인과 현재 분석 도구는 다름 | [S-F06] [S-F07] |

grep.app의 공식 예제는 “부분 오류 처리 문제를 해결할 구현 근거”를 찾는다. 이 기능은 D1 제작자 사례라는 이유로 없다고 낮춰 평가하지 않았다. 다만 지정 저장소 분석의 강점과 아직 모르는 후보 저장소를 발견하는 능력은 별도다. [S-AC31] [S-F06]

### (d) LLM 기반 개발 조사

| 시스템 | 입력 | 수집·표현·검색 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| Perplexity | 자연어·후속 질문·파일/프로젝트 문맥 | 여러 검색·하위 과제와 공개 웹/주어진 자료 합성 | 인용 답변·지속 문맥. 현재 문서는 Spaces→Projects 이전을 공지 | [S-DE01] [S-DE02] [S-DE03] |
| GitHub Copilot Spaces | 목표 지시+선택 파일·폴더·repo·문서 | 저장소 의미 색인; 파일 직접 첨부와 repo 검색을 구별 | 코드 문맥 설명, main/색인 갱신. IDE 경로의 지원 범위는 더 좁음 | [S-DE04] [S-DE05] [S-DE06] |
| DeepWiki / Ask Devin | repo URL·구조/함수 질문·부분 steering | repo 색인→wiki/구조도·코드 연결 | 소스 링크 설명과 새로고침. 공개 DeepWiki와 유료 Devin 경로 구별 | [S-DE07] [S-DE08] [S-DE09] |
| Exa / exa-code | 질의·필터·라이브러리/API 과제 | 웹 벡터 색인; 코드의 하이브리드 검색·예제 추출/재순위 | URL·구간·요약/코드 문맥. 호출하는 에이전트가 최종 적합성 설명 담당 | [S-DE10] [S-DE11] [S-DE12] |

선택한 일부 자료와 목적을 입력하는 것, 질문을 나누어 링크를 설명하는 것 자체는 독자적 가치가 아니다. 범용 LLM에 코드·목록 도구를 붙인 조합을 이후 비교 실험의 강한 기준선으로 사용해야 한다. [S-DE04] [S-AC31] [S-F06]

### (e) 학술 발견

| 시스템 | 입력 | 수집·표현·검색 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| Semantic Scholar / S2AG | 검색어·논문 ID·긍정/부정 seed | 논문·인용 그래프; SPECTER는 인용 감독의 표현 연구 | 관련 논문/URL; snapshot·update/delete diff. 2020 모델을 현행 전체 엔진과 동일시하지 않음 | [S-DE14] [S-DE15] [S-DE16] |
| Connected Papers — 현재 상태 불명 | 한 개 또는 여러 seed 논문 | 공인용·참고문헌 겹침의 유사성 그래프 | 선행/후속 연구. 2022 Premium 전환은 비용 대응이며 종료가 아님 | [S-DE18] [S-DE19] |
| Elicit | 연구질문+PICO/선별 조건+추출 항목 | 임베딩·최신성/인용 특징→LLM 순위·screening | 주장별 원문 구절·검토/추출 기록·보고서 재생성 | [S-DE20] [S-DE21] [S-DE22] |
| ResearchRabbit | 논문 묶음·관계·주제/기간 필터 | 여러 메타데이터 공급자; 인용·저자 관계와 영향력 순위 | 그래프/알림; 저장 collection에도 Signals 위험 표시 | [S-DE23] [S-DE24] [S-DE25] [S-DE26] |
| Microsoft Academic — 종료 | 당시 검색 의도·연구 관심 | Bing에서 추출한 개체·관계 그래프·의미 추론 | 역사적 추천/알림·갱신; 2021년 말 종료 | [S-F01] [S-F02] |
| Papers with Code — 원 포털 종료·재구현 | 논문/주제·task/method/dataset | 논문–코드–평가표 분류; 현 HF README는 혼합 검색/갱신 job | 구현·평가·계보 링크. 옛 데이터와 새 코드의 권리는 별개 | [S-F12] [S-F13] [S-F14] |

“논문이 비슷하다”는 설명도 서로 다르다. SPECTER는 인용 관계를 학습 감독으로 쓰지만 새 문서 추론 때 인용이 필수는 아니다. Connected Papers의 배치는 직접 인용 트리가 아니며, ResearchRabbit의 영향력 순위는 오래된 고인용 논문을 선호하는 특성이 있다. 어느 것도 그래프의 가까운 점이 목표 구조에 옮길 수 있는 원리임을 자동 증명하지 않는다. [S-DE15] [S-DE18] [S-DE23]

### (f) 패턴·참조 아키텍처

| 시스템 | 입력/선택 | 수집·표현 | 설명과 유지 | 근거 |
| --- | --- | --- | --- | --- |
| microservices.io | 부분 설계 질문·상황 | 전문가 패턴 언어·선행/후속 관계 | context·forces·solution·consequences, 구체 선택 대가 | [S-FG01] [S-FG02] [S-FG25] |
| Enterprise Integration Patterns | 메시징 문제·기술/패턴 | 현장 경험의 65 패턴·공통 용어 | 대안·문제·결과와 Camel/Spring 등 구현 링크, 지속 추가 사례 | [S-FG03] [S-FG04] |
| Azure Cloud design patterns | 제약·위험·부분 문제 | 문제 중심 패턴 카탈로그 | 고려사항·대가·구현 예. 다른 분산 환경에도 개념 적용 가능 | [S-FG05] |
| Thoughtworks Radar | 기술/기법·범주/링 | 프로젝트 경험→전문가 선별·편집 | 짧은 경험 판단. 반기 발행; 옛 blip은 갱신하지 않음 | [S-FG06] |
| AWS Well-Architected Tool / Agent | workload·목표·IaC·pillar·선택 항목 | 질문/lens·자원·설계 분석; Agent preview | 부분별 why·신호·대가·완화·지침/자원 링크, 상태·갱신 | [S-FG19] [S-FG22] [S-FG24] [S-FG26] |

microservices/EIP/Azure 카탈로그의 입력은 사람이 자신의 문제를 설명과 대조해 패턴을 선택하는 과정이며, 설계를 자동 수용·분석한다는 뜻은 아니다. 여기에는 완성품 대안보다 작은 원리·부분 구조를 설명하는 선행 시스템이 분명히 있다. EIP는 원리에서 구현 링크로 가는 통로까지 제공한다. AWS는 구조·목표·부분 대상과 설명을 결합하지만, 내부 구성 진단과 외부 OSS 후보의 발견은 같은 범위가 아니다. [S-FG03] [S-FG04] [S-FG24] [S-FG26]

### (g) 구조화 문제와 근거 유효성을 다루는 다른 분야

| 시스템 | 입력 | 표현·검색 | 설명·유지의 핵심 | 근거 |
| --- | --- | --- | --- | --- |
| Google Patents | 자유문·특허 번호·문단·CPC·필드; 화학 검색의 SMILES·부분구조 | 텍스트 유사성·분류·인용; 비특허 자료도 포함 | 도면·청구항·원문 링크; Similar Documents는 유사성이지 전이 판정이 아님 | [S-FG07] [S-FG08] [S-FG09] |
| EPO Espacenet / CPC | 검색어·분류·문헌/청구항 | 계층 분류·선행 인용 탐색 | 조사 지침이 자신의 신규성 주장을 깨는 탐색을 요구. 출원/등록 청구항 구분 | [S-FG10] [S-FG11] |
| PubMed Clinical Queries | 자유 검색어+연구 범주·broad/narrow | MeSH·서지/임상 필터·관련 문헌 | 수정·철회 관계, 연간 기준본+일별 변경; LinkOut은 별도 책임 | [S-FG12] [S-FG23] |
| Cochrane PICO | 용어+P/I/C/O 역할, 필요시 조건 추가 | 전문가 주석·통제어·역할별 AND/OR | 결과의 PICO 역할을 요구와 비교. 현재 주석 생산 SLA는 별개 | [S-FG13] [S-FG14] [S-FG15] |
| KeyCite | 판례·법령 인용 | 후속 취급·의존 관계·간접 overruling risk | 일부 법률 논점의 경고와 이유; 전체 판결의 무효 선언은 아님 | [S-FG16] |
| Shepard’s | 인용·연결 이력 | 후속 취급과 다단계 관계의 신호 | 분석 유무/상태를 구분. 모든 판례에 신호가 있는 것은 아님 | [S-FG17] |

## 2. Q2 — 무엇을 반드시 입력하게 하는가

| 방식 | 문서에서 확인한 요구 | 구조화 이유 | 피해야 할 일반화 |
| --- | --- | --- | --- |
| Cochrane PICO | 단일 용어로 시작하고 역할을 선택·추가할 수 있음; 네 칸 완성이 필수라는 근거 없음 | 같은 질병명도 대상인지 결과인지 구별 | “PICO이므로 네 필드 모두 필수” |
| PubMed Clinical Queries | 검색어와 연구 범주/민감도 선택 | 목적에 맞는 임상 연구 필터 적용 | 자유문 검색을 임상 판단 완료로 취급 |
| Google Patents / EPO | 번호·검색어·문단·분류, Google 화학 검색의 SMILES·부분구조 등 여러 시작 경로 | 분야 용어 차이를 분류·청구항·인용으로 보완 | 전체 청구항이 항상 필수, 검색 없음=신규성, 분자 부분구조 검색=일반 설계 목적 해석 |
| AWS | Tool의 workload/질문과 Agent의 IaC/선택 pillar·목표/항목 | 적용 환경과 검토 범위를 특정 | 선택적 도면·scope를 모든 제품 입력의 필수 스키마로 강제 |
| Copilot Spaces / Elicit | 선택 문맥+지시, 또는 질문+조건·추출 항목 | 문맥·판정 단위를 사용자가 조절 | 자유문을 받으면 구조 해석·제약 보존까지 입증됨 |

위 비교의 직접 근거는 [S-FG07] [S-FG11] [S-FG12] [S-FG14] [S-FG19] [S-FG24] [S-DE04] [S-DE21]이다. **H:** 우리 입력도 처음부터 완전한 설계도를 강제하기보다 현재 아는 부분·목적·제약·모르는 부분을 남기는 방식부터 비교할 가치가 있다. 이것은 최종 입력 스키마 결정이 아니다.

## 3. Q3 — 자료 규모·갱신·권리의 조건

규모는 전수 품질의 대용 지표가 아니다. 아래 수치는 원문의 특정 시점/제공자 표기이며 이번에 다시 계산한 값이 아니다.

| 자료 | 확인된 규모·시점 또는 갱신 | 재사용 조건의 핵심 | 근거 |
| --- | --- | --- | --- |
| OpenAlternative 공개 목록 | 2026-11-19 README의 863 프로젝트·85 범주 | 그 목록은 CC0; 사이트 전체·링크 대상 라이선스와 구별 | [S-AC04] |
| Libraries.io 구판 덤프 | 2018 배포, 34 패키지 관리자 | 데이터 CC BY-SA 4.0와 출처 표시. 현재 API 전체의 권리·최신성 아님 | [S-AC12] |
| deps.dev | 피드/스캔; 흔한 패키지 통상 한 시간 수준이라는 FAQ | 자체 생성 의존/연결 CC BY 4.0, upstream 조건·API 약관 별도 | [S-AC14] [S-AC15] |
| ecosyste.ms | Repositories 페이지의 2억8700만·1952출처 | 데이터 CC BY-SA 4.0·코드 AGPL·별도 계약 경로; 상업 사용 일률 금지라는 뜻 아님 | [S-AC20] [S-AC35] |
| GitHub 코드 검색 | 2023 엔진 글의 4500만 repo·115TB | 당시에 대한 규모. 현재 전수 커버리지나 결과의 재배포 허가 아님 | [S-AC25] |
| Semantic Scholar | 릴리스 snapshot과 update/delete diff | API·S2 Data·제3자 콘텐츠 조건 분리. 살아 있는 두 약관 문안 적용 차이는 미해결 | [S-DE14] [S-DE16] [S-DE17] |
| Elicit / ResearchRabbit | 제공자 표기 138M/310M+; 주간 메타데이터 갱신 | 서비스 열람과 논문 전문·전체 DB 재배포는 별도 | [S-DE20] [S-DE24] |
| Papers with Code | 옛 README daily는 현재 실행 증거 아님; 재구현 job 문서 | 옛 데이터 CC-BY-SA, 새 프로그램 Apache-2.0; 새 전체 catalog 권리 동일시 금지 | [S-F12] [S-F13] |
| EIP | 65 패턴·장기간 추가 사례 | 이름·아이콘·문제/해법 문장·스케치의 CC-BY와 적절한 출처 표시; 상세 책 전체 제외 | [S-FG04] |
| Google Patents / PubMed | Google 도움말의 120M+/100+관할; PubMed 일별 수정/삭제 | 자료 수록 범위·원문 권리·최신 법적/임상 판단을 구분 | [S-FG09] [S-FG12] |

AlternativeTo 약관의 경쟁 DB 수집 금지는 우리 데이터 재사용의 제약이다. **사용자가 직접 그 서비스에서 가치를 얻는다는 반대 가설을 반박하는 근거는 아니다.** [S-AC01]

## 4. Q4 — 같은 “검색”이 보존하는 관계의 차이

| 표현 | 보존하는 관계 | 버리는/약해지는 정보 | 근거 |
| --- | --- | --- | --- |
| 대안·태그·분류 | 제품의 주목적·분야·일부 특징 | 사용자 부분 구조와 제약의 결합 | [S-AC02] [S-AC03] |
| 의존 그래프·식별자 | 버전·구성·출처 연결 | 아직 모르는 목적 적합한 대안 | [S-AC14] [S-AC15] |
| 내용 주소·방문 이력 | 코드 동일성·출처·시점 | “왜 이 설계에 맞는가” | [S-AC24] |
| 코드 역색인·검색 문법 | 구문·파일·심볼·리비전 | 자연어 목표는 별도 번역; 색인 제외 존재 | [S-AC25] [S-AC26] [S-AC28] [S-AC30] |
| 논문 임베딩·인용 유사성 | 의미/인용상의 관련성 | 구조 대응·전이 전제·인과 | [S-DE15] [S-DE18] [S-DE23] |
| 패턴 언어 | 상황·forces·대안·결과·다음 문제 | 새로운 사용자 구조의 자동 매핑 | [S-FG02] [S-FG03] |
| PICO·CPC·citator | 역할·분류·후속 취급 | 분류/신호 밖 누락과 최종 전문가 판단 | [S-FG10] [S-FG14] [S-FG16] |

이것은 최종 검색 스택 선택표가 아니다. 기존 AF-RES-002가 다룬 SOLVENT·focused abstraction·BEIR·RRF의 방법 요약은 반복하지 않는다. [I-METHODS]

## 5. Q5 — 링크가 설명을 어떻게 뒷받침하는가

결과는 (1) 후보의 이름/홈페이지, (2) 선택 기준·관계·점수, (3) 코드/원문의 특정 위치, (4) 해당 부분에서의 이유·대가, (5) 후속 변경 신호의 수준으로 구별할 수 있다. 예컨대 awesome는 짧은 선택 맥락, grep.app는 파일·행과 해결 설명, Elicit은 주장별 원문 구절, KeyCite는 후속 취급을 제공한다. 다섯 수준의 단순 서열은 아니다. 필요한 이유와 작업 범위가 다르다. [S-AC05] [S-AC31] [S-DE22] [S-FG16]

| 평가 원문 | 과제·시점 | 직접 확인한 실패 | 이 연구에 적용할 범위 |
| --- | --- | --- | --- |
| Liu et al. 2023 | 2023년 2–3월 4엔진 각각 1450 질의; 인간 판정 | 문장 완전 지지 평균 51.5%; 인용의 문장 지지 74.5% | 링크 존재와 문장 지지를 나누어 검사. 현재 제품·설계 추천 오류율 아님 |
| Tow Center 2025 | 2025년 2월 20언론사×10기사×8도구=1600 질의; 원기사/발행자/URL 식별 | 전체 60% 초과 오답; Grok3의 200 질의에서 154 인용이 오류 페이지 | 허위/깨진 URL·원문 대신 재배포본이라는 실패 형태. 일반 개발 추천에 수치 전이 금지 |
| Gao et al. ALCE 2023 | ASQA/QAMPARI/ELI5, 고정 corpus·2023 모델; 문장별 인용 지지 | 답을 먼저 쓴 뒤 인용을 붙인 조건에서 인용 품질 저하; NLI 자동 평가도 완전하지 않음 | 답의 정답성과 인용 적절성을 분리. 모든 후첨 인용이 실패한다는 보편 명제 아님 |

세 연구의 원문·방법·결과·한계는 [S-DE27] [S-DE28] [S-DE29]에 기록했다. 숫자를 평균내어 “현재 AI 검색 실패율”을 만들지 않았다.

**유료 노출 반례:** SaaSHub는 유기적 순위에 광고가 영향을 주지 않는다고 하면서도 세 번째 SPONSORED 위치와 추가 시각 요소를 판매한다. 확인한 것은 표시 위치·주목도의 유료 우대다. 비밀 유기적 순위 조작이나 SEO 스팸의 실제 효과까지 측정한 것은 아니다. AlternativeTo의 유료 우선 심사는 승인·순위 보장과도 구별한다. [S-AC08] [S-AC09] [S-AC10] [S-AC01]

## 6. Q7 — 완성품 외의 부분·원리 연결

| 확인된 경로 | 이미 하는 일 | 아직 같은 것으로 볼 수 없는 일 | 근거 |
| --- | --- | --- | --- |
| grep.app + LLM | 부분 문제→코드 검색→파일/행→설명 | 주어진 목표 제약을 보존하는 정확도·일관성과 장기 근거 유지 | [S-AC31] |
| Sourcegraph / searchcode | 자연어+scope·부분 코드·기능 구현 비교 | 입력하지 않은 외부 저장소 후보를 목적에 맞춰 자동 발견하는 기능의 확인 | [S-AC30] [S-F06] |
| Exa / DeepWiki | API 예제·선택 repo의 구조/구간 설명 | 어떤 새 부품을 채택할지의 최종 적합성 | [S-DE07] [S-DE12] |
| EIP / microservices / Azure | 부분 문제의 패턴·대가·구현 링크 | 사용자 구조와 다른 분야 원리의 자동 대응 | [S-FG02] [S-FG04] [S-FG05] |
| PWC | task/method/데이터/논문에서 구현·평가표로 연결 | 현재 설계의 기능·비기능 제약 충족 | [S-F12] |
| AWS | 일부 자원/구조·목표의 진단과 이유/대가 | 외부 OSS·부품·타 분야 원리의 범용 발견 | [S-FG24] [S-FG26] |
| Cochrane / Elicit | 부분 질문을 역할·조건·원문 구절과 대응 | 소프트웨어 설계에 그대로 적용한 효과 | [S-FG14] [S-DE21] [S-DE22] |

**부분 연결 기능이 없다는 주장은 기각한다.** EIP는 서로 다른 메시징 제품의 용어·구성 대응도 설명하므로 타 영역 연결의 일부로 인정한다. 분야 사이의 거리를 새 조건으로 넣지 않는다. 사용자 목적에서 다른 영역의 원리를 찾아 적용 전제·반례까지 판정하는 범용 기능은 위 문서들만으로 확인하지 못했다. [S-FG03] 이것은 열람 범위에 한정한 판단이다. 여러 분야를 색인하는 것과 논문 유사성만으로 원리·관계 대응이 설명됐다고 세지 않았다. AskNature 등 유추 시스템은 이번 깊은 조사에서 제외했으므로 이 칸을 우리만의 시장 공백으로 사용할 수도 없다.

P1/P2/P03 원문은 고정 result_commit에서 읽었지만 공개 제품에 질의를 제출하지 않았다. 문서의 제작자 예제와 우리 D3 실행을 섞지 않는다. [I-PROTOCOL] [I-CASES]

## 7. 범주마다 무엇을 가져다 쓸 수 있는가

| 범주 | 데이터·API·방식의 재사용 후보 | 조건과 다음 확인 | 근거 |
| --- | --- | --- | --- |
| a | 허용된 CC0 목록·카테고리 탐색·기여 심사 방식 | 목록별 권리 확인; 경쟁 DB 수집 금지 존중; 부분 질문은 사람이 번역하는 기준선 포함 | [S-AC01] [S-AC04] [S-AC05] [S-AC07] |
| b | 패키지/버전/의존/저장소 정규화 API, content hash·origin/visit 원리 | endpoint·원천·릴리스별 권리/갱신 조건 확인; metadata를 적합도 점수로 전환하지 않음 | [S-AC12] [S-AC15] [S-AC20] [S-AC24] |
| c | 기존 코드색인·문법·revision scope·MCP/저장소 분석 | 계정/허용 범위와 코드 라이선스; 누락/분기 제한; 파일·행만 아닌 고정 버전 필요성 시험 | [S-AC25] [S-AC27] [S-AC29] [S-AC31] [S-F06] |
| d | 기존 LLM UI·파일 문맥·검색/본문 API | 새 유료 호출 없이 문서상 후보만 기록; 특정 과제 정확도·보존·수출 조건은 후속 확인 | [S-DE04] [S-DE10] [S-DE12] |
| e | 추천 API·논문/구현 연결·update/delete diff·주장별 근거 확인 방식 | API/데이터/본문 권리 분리; 상충 약관 해결; 재구현 현재성 확인 | [S-DE14] [S-DE16] [S-DE17] [S-DE22] [S-F13] |
| f | 문제·forces·대가·구현 링크 패턴; 부분 범위 검토 | EIP 허용 항목만 출처 표시하여 활용; 전체 책 복제 금지; 특정 클라우드 범위와 preview 구분 | [S-FG03] [S-FG04] [S-FG24] |
| g | 역할별 입력, 분류 확장, 후속 취급·재검토 신호의 운영 원리 | 의료/법률 데이터 자체를 새로 수집하지 않음; 전문분야 신호를 진실 보증으로 복제하지 않음 | [S-FG11] [S-FG14] [S-FG16] [S-FG17] |

## 8. 다섯 관점과 PLAN#1으로 넘길 문제

| 관점 | 이 조사에서 바뀌는 질문 | 사례 |
| --- | --- | --- |
| 사용하는 개발자 | 찾을 부품명을 아는가, 알려진 repo를 이해하는가, 아직 모르는 후보를 찾는가를 나눈다 | awesome·grep.app·searchcode [S-AC05] [S-AC31] [S-F06] |
| 운영자 | 편집 비용·색인 비용·수익·조직 우선순위를 따로 본다 | Connected Papers·searchcode·MAS [S-DE19] [S-F05] [S-F01] |
| 권리·라이선스 | 열람/코드/메타데이터/본문/계약을 구분하고 릴리스를 고정한다 | Libraries.io·S2·EIP [S-AC12] [S-DE16] [S-DE17] [S-FG04] |
| 정보검색 연구 | 관련성·출처 지지·목표 적합성을 다른 지표로 잰다 | SPECTER·ALCE·Liu [S-DE15] [S-DE29] [S-DE27] |
| 다른 분야 전문가 | 반증 탐색·역할 구분·후속 취급을 검색 과정에 포함한다 | EPO의 조사 지침·Cochrane의 Information Specialists·citator [S-FG11] [S-FG13] [S-FG16] |

**H — scope 연구 출발점:** 소프트웨어 목록의 폭만 늘리기보다 제품·패키지 버전·코드 구간·패턴·논문 근거를 각각 다른 단위로 다루는 것이 유용한지 시험한다. **H — maintenance 연구 출발점:** URL 생존, 원문/색인 최신성, 인용 위치의 재현성, 특정 주장에 영향을 주는 후속 변화는 다른 유지 업무다. PubMed·S2·KeyCite·Radar가 서로 다른 선택을 보여 준다. 이 문서는 최종 DB/API/검색 스택을 확정하지 않는다. [S-FG12] [S-DE14] [S-FG16] [S-FG06]

## 한계

모든 외부 시스템 판단은 D1 본문 조사이며 이번 D2 코드 고정 검증·D3 제품 질의·D4 목표 과제 성공 실험은 없다. 2023/2025 평가 수치, 역사적 규모, 제작자의 성능 주장과 현재 문서 상태를 구분했다. 공식 문서만으로 실제 운영 정확도·수익·지원 SLA를 확정하지 않았으며 모르는 사항은 SYSTEMS.json의 unknowns와 sources.json의 limits에 구체적으로 남겼다. blocked/JS shell/snippet은 excluded에 보존했고 근거 수에서 뺐다. 방법론 심층 조사와 사람 Q&A 내용 분석은 범위 밖이다.

## 출처 링크

[S-DE04]: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/copilot-spaces/create-copilot-spaces
[S-AC31]: https://vercel.com/blog/grep-a-million-github-repositories-via-mcp
[S-F06]: https://searchcode.com/
[S-DE22]: https://elicit.com/solutions/reports
[S-DE25]: https://learn.researchrabbit.ai/en/articles/15888747-exploring-article-risk-with-signals-indicators
[S-AC02]: https://alternativeto.net/faq/
[S-AC05]: https://github.com/sindresorhus/awesome
[S-FG22]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent.html
[S-FG24]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-architecture-reviews.html
[S-FG26]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/agent-view-rec.html
[S-X01]: https://asknature.org/about/
[S-AC01]: https://alternativeto.net/about/terms/
[S-AC03]: https://openalternative.co/about
[S-AC04]: https://github.com/piotrkulpinski/open-source-alternatives
[S-AC07]: https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md
[S-AC37]: https://api.github.com/repos/sindresorhus/awesome
[S-AC08]: https://www.saashub.com/about
[S-AC09]: https://www.saashub.com/featured-products
[S-AC10]: https://www.saashub.com/faq.html
[I-DOT]: https://github.com/laadkke-arch/agentflow-open/blob/ba62d1fa8ce5ff9631c20167a9fa4dc61cd1daea/docs/workstreams/dot-trial/AF-DOT-001/REVIEW.md
[S-AC11]: https://support.tidelift.com/for-subscribers/references/understanding-the-difference-between-data-from-libraries-io-and-the-tidelift-subscription/
[S-AC12]: https://zenodo.org/records/1196312
[S-AC13]: https://github.com/librariesio/libraries.io
[S-AC14]: https://docs.deps.dev/faq/
[S-AC15]: https://docs.deps.dev/api/v3/
[S-AC19]: https://docs.ecosyste.ms/docs/usage/
[S-AC20]: https://docs.ecosyste.ms/docs/usage/licences/
[S-AC35]: https://docs.ecosyste.ms/docs/services/data-services/repositories/
[S-AC16]: https://ossinsight.io/docs/about
[S-AC17]: https://ossinsight.io/docs/faq
[S-AC18]: https://ossinsight.io/explore
[S-AC23]: https://github.com/SoftwareHeritage/swh-model
[S-AC24]: https://upsilon.cc/~zack/research/publications/ipres-2017-software-heritage.pdf
[S-AC33]: https://github.com/npms-io/npms-analyzer
[S-AC34]: https://github.com/npms-io/queries
[S-AC36]: https://github.com/npms-io/npms-analyzer/blob/master/docs/architecture.md
[S-AC25]: https://github.blog/engineering/the-technology-behind-githubs-new-code-search/
[S-AC26]: https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax
[S-AC27]: https://docs.github.com/en/search-github/github-code-search/about-github-code-search
[S-AC28]: https://sourcegraph.com/docs/admin/search
[S-AC29]: https://sourcegraph.com/docs/code-search
[S-AC30]: https://sourcegraph.com/docs/code-search/query-assist
[S-AC32]: https://grep.app/
[S-F07]: https://boyter.org/posts/searchcode-has-been-rebooted/
[S-DE01]: https://www.perplexity.ai/help-center/en/articles/10352903-what-is-pro-search
[S-DE02]: https://www.perplexity.ai/changelog/shared-workspaces-personal-computer-for-windows-and-model-council
[S-DE03]: https://www.perplexity.ai/en-GB/hub/products/deep-research
[S-DE05]: https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing
[S-DE06]: https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/use-copilot-spaces
[S-DE07]: https://docs.devin.ai/work-with-devin/deepwiki
[S-DE08]: https://github.com/CognitionAI/deepwiki
[S-DE09]: https://docs.devin.ai/work-with-devin/ask-devin
[S-DE10]: https://exa.ai/docs/reference/search
[S-DE11]: https://exa.ai/blog/building-web-scale-vector-db
[S-DE12]: https://exa.ai/blog/exa-code
[S-DE14]: https://webflow.semanticscholar.org/product/api/tutorial
[S-DE15]: https://aclanthology.org/2020.acl-main.207.pdf
[S-DE16]: https://webflow.semanticscholar.org/product/api/license
[S-DE18]: https://medium.com/connectedpapers/announcing-connected-papers-a-visual-tool-for-researchers-to-find-and-explore-academic-papers-89146a54c7d4
[S-DE19]: https://medium.com/connectedpapers/announcing-premium-accounts-multi-origin-graphs-and-more-92e8dbd66848
[S-DE20]: https://elicit.com/solutions/search
[S-DE21]: https://support.elicit.com/en/articles/14759154-systematic-reviews-in-elicit
[S-DE23]: https://learn.researchrabbit.ai/en/articles/12454660-how-researchrabbit-builds-and-ranks-your-map
[S-DE24]: https://learn.researchrabbit.ai/en/articles/12454605-the-researchrabbit-database
[S-DE26]: https://learn.researchrabbit.ai/en/articles/12454495-what-is-researchrabbit
[S-F01]: https://www.microsoft.com/en-us/research/articles/microsoft-academic-to-expand-horizons-with-community-driven-approach/
[S-F02]: https://www.microsoft.com/en-us/research/project/academic/
[S-F12]: https://github.com/huggingface/paperswithcode
[S-F13]: https://github.com/paperswithcode/paperswithcode-data
[S-F14]: https://www.linkedin.com/feed/update/urn:li:activity:7354483119762153472/
[S-FG01]: https://microservices.io/patterns/
[S-FG02]: https://microservices.io/post/architecture/2023/03/13/better-decision-making-with-patterns.html
[S-FG25]: https://microservices.io/about.html
[S-FG03]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/Introduction.html
[S-FG04]: https://www.enterpriseintegrationpatterns.com/patterns/messaging/
[S-FG05]: https://learn.microsoft.com/en-us/azure/architecture/patterns/
[S-FG06]: https://www.thoughtworks.com/radar/faq
[S-FG19]: https://docs.aws.amazon.com/wellarchitected/latest/userguide/tutorial.html
[S-FG07]: https://support.google.com/faqs/answer/7049475?hl=en
[S-FG08]: https://support.google.com/faqs/answer/7049724?hl=en
[S-FG09]: https://support.google.com/faqs/answer/7049585?hl=en
[S-FG10]: https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/classification/cpc
[S-FG11]: https://www.epo.org/en/learning/learning-resources-profile/business-and-ip-managers/inventors-handbook/novelty-and-prior-art
[S-FG12]: https://pubmed.ncbi.nlm.nih.gov/help/
[S-FG23]: https://www.nlm.nih.gov/databases/download/pubmed_medline.html
[S-FG13]: https://www.cochrane.org/about-us/news/try-new-cochrane-pico-search-beta-cochrane-library
[S-FG14]: https://assets.wiley.com/image/upload/v1786361551/how-to-use-pico-search-updated-2023.pdf?_s=public-apps
[S-FG15]: https://help.cochrane.org/kb/article/27-how-can-i-access-cochrane-evidence/
[S-FG16]: https://www.thomsonreuters.com/en-us/help/drafting-assistant/westcheck/keycite-status-flags
[S-FG17]: https://www.lexisnexis.com/en-us/support/lexis/faqs/shepards-signal-indicators.page
[S-DE17]: https://api.semanticscholar.org/license/
[I-METHODS]: https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/METHODS.md
[S-DE27]: https://aclanthology.org/2023.findings-emnlp.467.pdf
[S-DE28]: https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php
[S-DE29]: https://aclanthology.org/2023.emnlp-main.398.pdf
[I-PROTOCOL]: https://github.com/laadkke-arch/agentflow-open/blob/62b4aa6f95fee546a3cfb017d1ee8afc79ee87d1/docs/workstreams/research/AF-RES-002/PROTOCOL.md
[I-CASES]: https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/CASES.json
[S-F05]: https://boyter.org/posts/searchcode-is-being-rebooted/
