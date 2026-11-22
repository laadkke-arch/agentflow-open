# Jupyter 검색 묶음 — Q09~Q12

## 봉인과 실제 실행

권위 질의는 원격 봉인 `a4b4a028355dec8c507df304d6b1d9e0ae467d1d`의 최상위 queries.jsonl이다. stream 질의 24개를 변경 없이 system1_search_query/long으로 각각 실행했다. Q09 G→R, Q10 R→G, Q11 G→R, Q12 R→G 순서를 지켰고 첫 경로의 반환 JSON을 저장한 시각이 둘째 경로의 첫 검색보다 앞서는지 검산했다. 기계 검사 28항목은 모두 통과했다. 독립 판독은 아직 수행하지 않았다.

- 조회 24요청에서 제공된 결과 217건. 처음 10개 이내 211건, 초과 노출 6건, 10개 미만을 준 요청 14건이다. 숫자는 도구 제공 순위이며 검색엔진 전체 순위는 미확인이다.
- 경로별 URL 원문 시도 5회, 총40회. 같은 원문 절 연속 열람 3회, 재시도2회까지 합쳐 open 호출은45회다.
- 공급자 자료 행39개 중 최소수 산입37개. JP-C027은 도구가 재시도 뒤에도 rewritten summary로 표시하여 제외했다. JP-C033은 CTX 문서계보 중복으로 보수적으로 제외했다. 기존 최초판4개와 이 공급자37개는 서로 다른 원문군이다.
- 후보 관측37행, 공통 후보 ID를 합치면35개. 반환24슬롯, 빈슬롯0개. 빈슬롯0은 유효 추천24개라는 뜻이 아니다.
- 요청 벽시간 합계는 검색24.780초, open20.997초다. 병렬 요청의 합계이며 사용자 체감시간이나 인시가 아니다. 첫 검색05:05:33.538Z~마지막 반환05:23:25.363Z의 관측창에는 모델 판독·기록 작업이 포함된다. 토큰·과금·절감 인시는 미확인이다.

## 원반환 결과

| 질문 | G 상위3 | R 상위3 | 현재 신규 완결 | 해석 |
| --- | --- | --- | --- | --- |
| Q09 부분 | JP-K002 HornetQ, JP-K003 Azure, JP-K004 GCP | JP-K006 OGC, JP-K007 WebSub, JP-K003 Azure | G0/3, R0/3 | G는 일반 전달/내구성 문서, R은 구독 응답의 순서 규칙을 남겼다. OGC PDF 비규범판 경고와 WebSub 202 비동기 검증이 완결을 막았다. |
| Q10 전체 | JP-K013 3GPP, JP-K014 RFC6056, JP-K015 Winsock | JP-K009 Node APIs, JP-K010 PCP, JP-K012 TAPS | G0/3, R0/3 | R은 bind→실제주소→부모 IPC 부품을 찾았으나 후속클라이언트 manifest가 비었다. G는 registry 원자성과 OS소켓 점유가 다름, bind–listen 공백, Windows 배타성 조건을 남겼다. |
| Q11 부분 | JP-K019 ipykernel, JP-K020 NBClient, JP-K022 Datalayer | JP-K025 Precinct, JP-K027 MarkLogic, JP-K023 Codex trace | G0/3, R0/3 | G의 ipykernel 수신어댑터는 현재 근거가 완결하나 이미 알려진 Jupyter 호스트의 부품이다. R에서는 trace·descriptor·result·request metadata의 호출경계 차이가 드러났다. |
| Q12 전체 | JP-K034 app launcher, JP-K035 console:create, JP-K031 NVIDIA | JP-K029 CTX, JP-K030 Cosmo Tech, JP-K028 JSON Schema | G0/3, R0/3 | R은 schema→치환→실행 부품을 찾았으나 사용자 입력요청/enum 경계가 남았다. G의 NVIDIA는 form과 실행을 제공하지만 조합별 kernel.json 생성이 핵심 제약을 어긴다. |

주 지표 승패는 4질문 모두 무승부다. 모두 근거가 충분한 성공끼리의 무승부는 아니다. 상위1 민감도도 두 경로 모두0/4다. 당시판 주성공은0이며, 현재 전체근거부터 부족한 후보와 당시판만 미확인인 후보를 혼합해 당시 기능 부재로 단정하지 않는다.

## 반례와 해석 범위

1. **같은 목적이지만 조건 하나 위반:** JP-K031 NVIDIA BCM은 동적 dialog와 type/oneof/default/limits를 제공한다. 그러나 §16.5.1.1, §16.6은 새 사용자 kernel.json과 Launcher 항목 생성을 명시한다. 명세 수를 늘리지 않겠다는 Q12-P1과 충돌한다.
2. **같은 단어, 다른 호출 경계:** JP-K026 OWS Context의 code는 소스코드가 아니라 GetMap 같은 동작 이름이다. JP-K024의 _meta는 tool descriptor/result이고, JP-K023은 실행 뒤 trace자료다. 이들은 셀별 실행입력 metadata와 다르다.
3. **관계는 맞지만 구현 경계 부족:** JP-K009 Node의 bind(0), address(), child IPC는 조합할 수 있지만 모든 채널을 이름으로 묶고 후속클라이언트에 게시하는 설계는 이번 원문에서 확인하지 못했다.
4. **일반 경로만 남긴 구체 부품:** JP-K019 ipykernel은 code와 metadata를 따로 받아 do_execute의 cell_meta 지원 여부에 따라 전달한다. 신규 대상이 아니므로 주분자0을 유지하되 기지 제품의 놓친 부품이라는 보조가치를 남긴다.
5. **최초 결론의 반증:** R이 더 적합할 것이라는 기대와 달리 4질문에서 신규 완결 증가가 없다. Q11에서는 G만 기지 호스트의 완결 수신부품을 찾았다. 고정된 첫5원문 규칙 때문에 후속 질의의 더 직접적인 프로토콜·CI 입력기 문서는 예산 뒤에 남았다. 이는 적합 후보가 세상에 없다는 증거가 아니다.

원거리 원리로 채점한 후보는0이다. 지리공간 표준을 발견했지만 옮긴 관계는 같은 분산소프트웨어 프로토콜이며 이를 먼 분야 원리의 적중으로 부풀리지 않았다. 별도 도서관·제조 보조 사례는 아직 열지 않았다.

## 노출과 원문 한계

원 제안/후속 결정 자체의 명확한 검색 적중은0이었다. 다른 JEP(add-schema, subshell) 제목·요약은 노출됐다. 현재 ipykernel 구현과 Q11 제안의 계보는 아직 확인하지 않았으므로 후속 답 노출 가능성은 미확인이다. Q12 NVIDIA 본문에는 Q10과 유사한 주소 회신도 노출됐지만 Q10 반환은 이미 고정되어 있었고 소급추가하지 않았다.

두 경로는 같은 모델 문맥을 공유한다. 각 질문 둘째 경로가 첫째 경로 후보를 본 상태라는 노출을 search-exposures.csv에 남겼다. 질의와 선택규칙은 사전에 봉인했고 변경하지 않았다. 이 통제는 독립 검색 사용자 실험과 같지 않다.

version이 main/latest인 원문은 고정 출시판이 아니다. HTML 문서의 버전 표제만 있고 실제 기능 최초 태그가 없는 경우 당시 이용 가능성을 unknown으로 둔다. Posit 검색제목은2026.11.0이었으나 열린 본문은2026.10.0이다. 기록은 열린 판을 따른다.

Q12-R의 JSON Schema 검증 절은 원문이 최초 open에서 회수됐으나 세부 문장 재판독은 R 반환 저장 직후에 이뤄졌다. 해당 후보는 이미 known/conflict였고 opened_complete/cited_complete=false이다. 이를 완결 인용으로 소급 고치지 않았다.

## 후속 독립 판독 입력

원래 반환 및 인용은 routes/*.json과 returns.jsonl에 보존했다. parent의 지시에 따라 이후 3 URL 제한 해석을 별도로 계산하되 원반환을 바꾸지 않는다. self-check는 의미 판정의 정답이 아니며 blind 검토에서 조건별 판단과 첫5원문 적격성에 이견이 생길 수 있다.

- JP-C006: 비규범 PDF가 가리킨 공식 규범 HTML의 같은2016판을 감사 단계에서 읽으면 OGC 판단이 바뀔 수 있다. 먼저 본 PDF의 인용을 소급 보강하지 않는다.
- JP-K019: main의 고정 commit 및 cell_meta 최초 도입 태그·제안과의 연결을 후속 단계에서 확인한다. 이는 신규 제품 여부를 바꾸지 않는다.
- JP-K029: CTX의 실제 입력 UI/CLI prompt, enum 검사 구현·테스트와 출시일을 확인하면 Q12-P2 보류가 바뀔 수 있다.
- JP-K034/Q12-P3와 JP-K032/Q12-P3도 문장상 불완전인데 missing_conditions에는 일부 조건만 나열돼 있다. 완결 bool은 이미false여서 주분자는 변하지 않는다. 원반환을 유지하고 독립 판정에서 조건을 정리한다.

재집계는 `python docs/workstreams/research/AF-RES-025/streams/jupyter/assemble_search.py`다. 이는 봉인된 route·receipt에서 파생 CSV/JSON을 다시 만들며 검색하지 않는다. parent가 검토 후4질문 묶음을 커밋해야 원격 결과가 된다. 이 stream은 Git을 변경하지 않았다.

