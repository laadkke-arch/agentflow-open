# Jupyter 후속 결정·역사 검증

## 범위와 고정점

봉인된 주 판정 `d1f506b1dde91e706360846f4c2eac5baabe492e` 뒤에 수행한 Q09–Q12 역사 감사다. 원 검색·순위·반환·원 인용·가린 판정은 변경하지 않았다. 이 단계의 새 원문은 원 반환의 부족한 인용을 소급 보강하지 않는다. 커밋과 원격 확인은 진행 담당이 수행한다.

| 질문 | 실제 관측한 결정 | 고정 근거 |
| --- | --- | --- |
| Q09 | XPUB/iopub_welcome 계열 제안 병합. 구독 식별, 중복 구독, 버전별 대기가 구체화됨 | JP-F001–004, JP-F029; merge `5250a27540a24ca8385296891d0e4359e593df2e` |
| Q10 | 7/1/1 표결로 채택. launcher/registration socket, ACK·재시작, 두 연결 방식 병행을 명시 | JP-F005–012, JP-F030; merge `55abffe9210f316c99be60bd6c621246dddc5bc9` |
| Q11 | PR70은 아직 open. root message.metadata 방향의 수정은 있으나 최종 채택 없음 | JP-F013–021; head `0e91d84a211408c49950d8c305046597963cfd03` |
| Q12 | 8/0/1 표결로 채택. JSON Schema 경로를 유지하며 노트북 매개변수 저장을 제거하고 안전한 입력 조건 추가 | JP-F022–028; merge `9032ece0abe8aeddf2b3ab55b4e2562a175bdf83` |

채택과 출시를 구분한다. PR87의 2026-02-04 댓글은 xeus 구현을 앞으로 진행하겠다는 말이며 출시 증거가 아니다. PR70의 한 guide 예제는 `header.metadata`, reference 설명과 다른 예제는 root `message.metadata`를 사용하므로 내부 불일치를 보존했다.

## 당시 가능성과 현재 가능성

`candidate-history.jsonl`은 원 반환 24슬롯의 고유 후보 23개를 모두 포함한다. 판정은 **supported 0 / not_available 1 / unknown 22**이다. 원 주 지표의 성공 수와 같은 수치가 아니다.

- **JP-K006 OGC — 정정 JP-AMEND-001**: 2016년판의 publisher matching→응답 순서는 당시 존재했다는 partial_supported만 유지한다. Subscriber와 Receiver는 다른 행위자일 수 있고, 응답이 실제 수신 경로 준비를 관측했다는 뜻은 아니다. 별도의 receiver-ready 가정을 넣어 P1을 대체한 이전 supported 판정은 unknown으로 정정했다. 첫 출력 유실을 피하는 P2도 미확인이다. JP-H008; [정정 기록](amendments/JP-AMEND-001.json).
- **JP-K019 ipykernel**: 정확한 `do_execute(cell_meta)` 어댑터는 2023-11-21 커밋 `5b72bfe2e937790b6a7771df1ffec3e79bc5f47f`에서 추가됐고, 같은 날 11:23:54 UTC 공개된 v6.27.0에 포함된다. 2021년 코드의 일반적인 parent/init_metadata 접근과 구분했다. 최초안의 `content.metadata`를 읽는 구현도 아니다. PR1169가 PR70 채택이라는 근거는 발견하지 못했다. JP-H001–007.
- **JP-K009 Node**: 2020-12-17 v14.15.3의 바인딩·실제 주소·자식 IPC는 확인했다. 여러 커널/채널의 식별과 늦게 접속하는 클라이언트용 기록 계약은 여전히 비어 있다. JP-H010–012.
- **JP-K007 WebSub**: 2018판도 202 응답과 검증 완료를 분리한다. 과거판을 찾았다는 이유로 준비 barrier가 성립하지 않는다. JP-H009.
- **JP-K031 Bright/BCM**: 9.1 표지의 현행 PDF는 2026-04-13 개정판이다. 2021 저작권과 버전 번호는 당시 기능의 고정 증거가 아니다. 사용자 지정 뒤 새 kernelspec/launcher 항목을 만드는 경계는 현재와 이 개정판 모두에서 보존했다. JP-H013–016.

unknown은 부재가 아니다. 각 행은 실제 읽은 범위, 미확인 술어와 다음 최소 자료를 적는다. 예를 들어 RFC9622는 정확히 January2025 발행이며, 이전 Internet-Draft의 기능 계보는 미확인이다.

## 이름과 지식의 구분

최초 문서에 없는 이름을 당사자의 미인지로 해석하지 않았다. frozen known-host 분류는 유지하되, 정확한 부품 이름은 별도로 감사했다. Q11 최초판에는 literal ipykernel/IPython/NBClient가 없고 Jupyter 및 messaging 문서가 있다. ipykernel wrapper의 한계는 다음 날 issue68에서 명시된다. 현재 cell_meta API는 더 늦다.

후속 댓글의 Enterprise Gateway, IPython Parallel, KSMM은 주 검색 적중으로 세지 않았다. JSON Schema/react-jsonschema-form은 Q12 최초판에 이미 있다. 후속 처음 명시는 **조사한 현재 공개 문서 집합에서의 최초 명시**이며, 모든 과거 언급의 최초나 작성자의 최초 인지를 뜻하지 않는다.

## 자료·영수증·비용

- [decisions.jsonl](decisions.jsonl): 질문별 결정, 최초판 대비 변화, 후보별 명시 단계 4행.
- [candidate-history.jsonl](candidate-history.jsonl): 고유 원 반환 후보 23행.
- [sources.json](sources.json): 51개 자료 관측. 추가 최소수 산입은 보수적으로 10건이며, 후속 결정 사건은 4질문을 각각 포함한다. 동일 원문·다른 판·원문 미열람 요약은 중복 산입하지 않는다.
- [diff-observations.json](diff-observations.json): 4개 고정 first→head diff의 경로·날짜·해시와 변경 관측.
- [inspected-collections.json](inspected-collections.json): 받은 댓글 164개의 ID·날짜·본문 해시와 보고서용 전문 판독 여부. 이름 검색과 전문 판독은 구분한다.
- [historical-search-log.json](historical-search-log.json): 이 단계에서 추가한 2검색의 제공 순위 13행. 원 검색 예산에 섞지 않는다.
- [costs.json](costs.json), [receipts/](receipts/): 실제 요청 53개. GitHub fetch 31, commit search 1, web 21회. web에는 검색 2질의, open 15명령, find 4명령, click 1명령이 있다.

조회 창은 2026-11-22T05:51:40.641Z–2026-11-22T05:59:24.582Z이다. 호출별 벽시간의 합은 25.626초이며 병렬 호출을 합한 값이다. 읽기·판단·작성의 총 인시나 시간 절감이 아니다. 토큰, 모델 연산비, 실제 절감 인시는 제공되지 않았으며 미확인이다. 런타임 검증은 수행하지 않았다.

generic GitHub search/commits 요청의 도구 거절 1회, v5.5.3 태그 404 1회, Bright 목록 페이지의 빈 본문 1회를 남겼다. 각각 전용 검색, 날짜 제한 파일 이력, 직접 PDF/릴리스 노트로 대체했다. 거절된 범위를 우회해 권한을 넓히지 않았다.

## 재집계와 재개 명령

저장소 루트에서 다음을 실행한다. 검산은 JSON 스키마·분모·ID·필수 조건 배열·영수증·출처 참조를 검사하며, 사실 판독을 독립 재현하지는 않는다.

```bash
python -B docs/workstreams/research/AF-RES-025/followups/jupyter/validate.py
```

ipykernel의 정확한 입력은 아래 고정판이다. 파일 비교는 주 반환을 바꾸지 않는 역사 재확인이다.

```bash
curl --fail --location --silent --show-error 'https://raw.githubusercontent.com/ipython/ipykernel/91b935f964ee5a3808a7fa3234bb84ae15efb2ea/ipykernel/kernelbase.py' | rg -n 'def execute_request|def do_execute|cell_meta|init_metadata'
curl --fail --location --silent --show-error 'https://raw.githubusercontent.com/ipython/ipykernel/v6.27.0/ipykernel/kernelbase.py' | rg -n 'def execute_request|def do_execute|cell_meta|init_metadata'
curl --fail --location --silent --show-error 'https://api.github.com/repos/ipython/ipykernel/releases/tags/v6.27.0'
```

접근이 계속 막히면 GitHub fetch에서 같은 URL을 입력한다. 각 나머지 후보의 구체적인 재개 입력은 `candidate-history.jsonl.next_minimum_check`에 있다. Node의 빈 P3는 자체 예제를 작성해 과거 공급자 기능처럼 채우지 말고, 당시 배포된 구현/테스트 또는 연결 파일 계약을 먼저 찾는다.

## 남은 핵심 약점 3건

1. **당시/현재 및 host/component 경계**: JP-K019은 정확한 어댑터가 후발이다. 다음 조사는 2021년 고정된 wrapper subclass와 클라이언트의 root metadata 전달을 함께 읽어, 당시 가능한 대체 사용을 별도 후보로 명세하는 것이다. 기존 원 반환에는 소급하지 않는다.
2. **22개 역사 완전성 미확인**: JP-K006의 matching 규칙은 수신 준비 관측을 보장하지 않고, JP-K009의 P3도 비어 있다. 다음 조사는 v14.15.3 시대의 두 자식·여러 채널·늦은 클라이언트 연결 기록을 가진 공식 예제/테스트 한 건이다.
3. **살아 있는 버전별 문서**: JP-K031의 9.1 문서는 개정일이 후대다. 다음 조사는 2022-02-10 이전 날짜가 고정된 Bright 패키지/매뉴얼과 두 매개변수 조합의 kernelspec 생성 결과를 함께 확인하는 것이다.
