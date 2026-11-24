# AF-RES-229 · pip 24.0의 pytest 철회 파일 선택

| 요청·인덱스 | 대상 플래그·사유 | 실제 선택 파일·SHA | 경고·종료 | 선행·실행 영수증 | 미확인 |
| --- | --- | --- | --- | --- | --- |
| `pytest==8.1.0` · baseline | true · 원사유 P | `pytest-8.1.0-py3-none-any.whl` · `ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e` | 각 stderr 1건 · P · 각 종료 0 | D04/D06 · [r1](receipts/main/pin-target-baseline-r1/) · [r2](receipts/main/pin-target-baseline-r2/) | 실설치·실행 범위 밖 |
| `pytest==8.1.0` · unmarked | 속성 없음 · 사유 해당 없음 | `pytest-8.1.0-py3-none-any.whl` · `ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e` | 선택 경고 0 · 각 종료 0 | D04/D06 · [r1](receipts/main/pin-target-unmarked-r1/) · [r2](receipts/main/pin-target-unmarked-r2/) | 실설치·실행 범위 밖 |
| `pytest>=8.0.2,<8.1.1` · baseline | true · 원사유 P | `pytest-8.0.2-py3-none-any.whl` · `edfaaef32ce5172d5466b5127b42e0d6d35ebbe4453f0e3505d96afd93f6b096` | 선택 경고 0 · 각 종료 0 | D03/D06 · [r1](receipts/main/range-exclusive-baseline-r1/) · [r2](receipts/main/range-exclusive-baseline-r2/) | 실설치·실행 범위 밖 |
| `pytest>=8.0.2,<8.1.1` · unmarked | 속성 없음 · 사유 해당 없음 | `pytest-8.1.0-py3-none-any.whl` · `ee32db7af8de4629a455806befa90559f307424c07b8413ccfc30bf5b221dd7e` | 선택 경고 0 · 각 종료 0 | D04/D06 · [r1](receipts/main/range-exclusive-unmarked-r1/) · [r2](receipts/main/range-exclusive-unmarked-r2/) | 실설치·실행 범위 밖 |
| `pytest>=8.0.2,<=8.1.1` · baseline | true · 원사유 P | `pytest-8.1.1-py3-none-any.whl` · `2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/range-inclusive-baseline-r1/) · [r2](receipts/main/range-inclusive-baseline-r2/) | 실설치·실행 범위 밖 |
| `pytest>=8.0.2,<=8.1.1` · unmarked | 속성 없음 · 사유 해당 없음 | `pytest-8.1.1-py3-none-any.whl` · `2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/range-inclusive-unmarked-r1/) · [r2](receipts/main/range-inclusive-unmarked-r2/) | 실설치·실행 범위 밖 |
| `pytest==8.1.1` · baseline | true · 원사유 P | `pytest-8.1.1-py3-none-any.whl` · `2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/pin-next-baseline-r1/) · [r2](receipts/main/pin-next-baseline-r2/) | 실설치·실행 범위 밖 |
| `pytest==8.1.1` · unmarked | 속성 없음 · 사유 해당 없음 | `pytest-8.1.1-py3-none-any.whl` · `2a8386cfc11fa9d2c50ee7b2a57e7d898ef90470a7a34c4b949ff59662bb78b7` | 선택 경고 0 · 각 종료 0 | D05/D06 · [r1](receipts/main/pin-next-unmarked-r1/) · [r2](receipts/main/pin-next-unmarked-r2/) | 실설치·실행 범위 밖 |

표 1의 한 행은 요청식 하나와 페이지 하나의 독립 실행 두 번이다. 대상은 항상 8.1.0 wheel이다. P는 216 V05/I02의 원값 `See https://github.com/pytest-dev/pytest/issues/12069`이다. 선행 ID는 [출처 원장](sources.jsonl), URL·해시·플래그·로그는 [16회 행렬](matrix.csv)과 [실행 검산](receipts/main-audit.json)에 있다.

| 경쟁 설명 | 한 변수 통제 | 실제로 뒤집힌 값 | 권고 문구 |
| --- | --- | --- | --- |
| 버전 정렬만으로 배타적 상한의 선택을 설명할 수 있다 | 같은 파일·URL·Python에서 8.1.0의 속성만 제거 | `<8.1.1`에서 8.0.2 → 8.1.0, 선택 경고는 양쪽 0 | 신규 범위는 상한과 파일 상태를 함께 확인한다. |
| 정확 핀의 결과가 같으면 경고도 같다 | `==8.1.0`에서 같은 속성 제거 | 파일과 SHA가 그대로이며 report flag true → false, stderr 선택 경고 각 1 → 0 | 원파일을 정확히 재현할 때 파일과 철회 사유를 함께 연결한다. |
| 상태를 바꾸면 다른 범위와 핀도 언제나 뒤집힌다 | 포함 상한과 다음판 핀에서 같은 제거 | 두 요청 모두 8.1.1 유지, 선택 경고 0 | 상한이 8.1.1을 허용할 때 그 파일을 대체 후보로 검토한다. |
| 사유가 비어 있으면 철회 선택 경고가 사라진다 | 같은 정확 핀에서 `data-yanked=""`로 값만 교체 | 같은 8.1.0·SHA, flag true, 경고 1, 사유 P → `<none given>`, 종료 0. [empty](receipts/controls/pin-target-empty-r1/) | 사유가 미제공인 철회도 상태와 경고를 표시한다. |
| 철회와 후보 링크 부재의 정확 핀 결과는 같다 | 같은 정확 핀에서 8.1.0 앵커만 제거 | 8.1.0/report/파일 GET → 선택 0·report 없음·파일 GET 0. 선택 경고 0, resolver 오류와 종료 1. [missing](receipts/controls/pin-target-missing-r1/) | 후보 링크 부재와 철회를 서로 다른 상태로 기록한다. |

표 2의 한 행은 경쟁 설명 하나와 그 설명을 판별하는 통제다.

## Q1. 선행 인계와 파일 입력

시작 통합판 `f3895893e32e2c055cefde446d34f1467fa27b4c`의 `tasks`에서 229는 216에 의존한다. 216은 DONE이고 중앙 `result_commit` 및 원격 216 브랜치 head가 `9a306b74e785dc98cb82fa000a10e497208309a6`로 일치했다. 그 SHA의 HANDOFF가 가리킨 실증 결과판은 `e2b767089a72c2e58c1a360d524f2b0d71df8ca9`이다. 계획판 이후 경로 차이 한 건과 중앙 상태 변화는 SCOPE에 있다. [D00 중앙](https://github.com/laadkke-arch/agentflow-open/blob/f3895893e32e2c055cefde446d34f1467fa27b4c/docs/automation/dot-control.json) · [D01 고정 인계](https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/HANDOFF.md) · [착수 범위](SCOPE.md)

| 파일판 | version JSON의 파일 원값·수신 UTC | Simple JSON의 같은 파일 원값·수신 UTC | 조인 근거 |
| --- | --- | --- | --- |
| 8.0.2 | V04 `/urls/0` `false`·`null`, 2026-11-24 21:32:17.135650 | I02 `/files/309` `false`, 2026-11-24 21:32:18.135115 | D03/D06, D07 L84 |
| 8.1.0 | V05 `/urls/0` `true`·P, 2026-11-24 21:32:17.340073 | I02 `/files/311` 문자열 P, 2026-11-24 21:32:18.135115 | D04/D06, D07 L86 |
| 8.1.1 | V06 `/urls/0` `false`·`null`, 2026-11-24 21:32:17.544187 | I02 `/files/313` `false`, 2026-11-24 21:32:18.135115 | D05/D06, D07 L88 |

한 행은 `py3-none-any` wheel 하나다. V04–V06은 `application/json`의 `yanked`·`yanked_reason`, I02는 `application/vnd.pypi.simple.v1+json` 1.4의 boolean/string `yanked`다. 원 HTTP 본문 네 개를 gzip 해제해 D08의 byte 수·SHA-256에 맞췄다. 세 포인터의 정확한 filename, 해시, URL, 크기, Python 제약과 업로드 UTC가 두 API 및 CSV와 일치한다. 비동시 스냅샷이므로 해당 수신 시점의 상태를 뒷받침하며 첫 철회 전파 UTC는 미확인이다. [고정 값·원포인터](inputs.json) · [재확인](receipts/predecessor.json) · [D08 시간·본문 해시](https://github.com/laadkke-arch/agentflow-open/blob/9a306b74e785dc98cb82fa000a10e497208309a6/docs/workstreams/research/AF-RES-216/receipts/api/http.json)

## Q2. 공개 wheel과 로컬 표현

216이 기록한 공식 HTTPS 주소 세 곳에서 각각 HTTP 200으로 333,984 B·335,525 B·337,359 B를 받았다. 본문 SHA-256은 표 1과 일치한다. 내부 METADATA 2.1의 Name·Version·Requires-Python은 `pytest`·각 릴리스·`>=3.8`이다. WHEEL은 1.0, Root-Is-Purelib true, Tag `py3-none-any`다. 세 METADATA 바이트의 SHA-256은 I02의 같은 파일 `core-metadata.sha256`과도 같다. 별도 pip 24.0 bootstrap wheel 1개도 공식 공개 해시·메타데이터를 검증했다. [입수 HTTP와 실제 내부 형식](receipts/wheel-fetch.json) · [원 I02 위치와 지문](inputs.json) · [R08 WHEEL 사양](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)

기준 HTML에는 각 등록 파일의 해시 fragment와 Python 제약을 옮겼다. 두 `false` 파일은 `data-yanked` 속성 부재로, 대상의 문자열은 그 값이 있는 속성으로 표현했다. `empty`에는 속성이 존재하고 그 값이 비어 있다. JSON의 무사유 표시에는 bool `true`를 쓰며 규격상 문자열은 non-empty다. 사유 없는 HTML과 빈 JSON 문자열을 그대로 복사하면 의미가 바뀐다. 세 실제 wheel의 전체 다운로드를 비교하기 위해 모든 로컬 페이지에서 sidecar 속성을 생략했다. 공개 Simple의 전체 후보와 sidecar 제공은 범위 밖이다. [R03 HTML/JSON](https://packaging.python.org/en/latest/specifications/simple-repository-api/) · [P03 24.0 링크 해석](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/models/link.py#L262-L363) · [고정 HTML](index/)

## Q3. 규격, 해당 pip 판, 사용 옵션

규격은 비철회 파일로 제약을 충족할 수 있으면 철회 파일을 배제하도록 한다. 설치기는 철회 파일을 거부할 수 있고, 정확한 `==`/ `===` 또는 기존 lock이 요청한 파일의 예외는 제시된 정책이다. 선택할 때 경고가 권고된다. pip 24.0의 기본 인덱스 resolver는 적용 후보가 모두 철회되고 핀이 정확할 때 철회 후보를 보존한다. `==x.*`는 핀에서 제외한다. PackageFinder에도 별도 hash·yank·version 정렬 순서가 있다. 선택은 인덱스가 실제로 공급하는 제약 충족 파일에 의존한다. [R01 PEP 592](https://peps.python.org/pep-0592/#installers) · [R02 현행 규격](https://packaging.python.org/en/latest/specifications/file-yanking/#installers) · [P01 resolver 조건](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/resolution/resolvelib/factory.py#L296-L339) · [P04 finder 순위](https://github.com/pypa/pip/blob/ef78c129b1a966dbbbdb8ebfffc43723e89110d1/src/pip/_internal/index/package_finder.py#L548-L586)

P02는 선택 링크의 상태로 메시지를 만들고 P08은 기본 경고를 stderr에 보낸다. P05와 P09는 report와 dry-run의 반환 순서를 설명한다. P06·P07·P10은 정확 핀의 경고, 범위에서 철회 제외, report `is_yanked`, 빈 사유 처리를 각기 기대한다. 이 업스트림 테스트는 정적으로 열람했다. 첫 커밋에서 이 근거로 선택·경고·종료 예측을 봉인했다. 24.0 판정에는 고정 태그 문서·소스 및 실제 출력을 사용했다. [SCOPE 예측](SCOPE.md#실행-전-봉인한-예측) · [R04–R09·P01–P10 위치](sources.jsonl)

## Q4. 네 요청의 실제 선택

16/16이 종료 0, report v1의 등록 한 건 및 GET 2건으로 끝났다. 각 실행에서 `/simple/pytest/`와 선택된 wheel의 `/files/…`를 200으로 한 번씩 보았다. report의 version·URL·SHA 및 `is_direct=false`·`requested=true`가 해당 요청과 파일 지문에 맞고, 제공한 응답 바이트 수와 SHA도 맞는다. 정확한 두 핀의 선택은 각각 8.1.0과 8.1.1로 유지됐다. 상한을 배타적으로 지정한 범위만 기준 8.0.2와 제거 통제 8.1.0으로 갈렸다. 포함 상한 범위는 양쪽에서 8.1.1을 골랐다. [행렬 16회](matrix.csv) · [실행 명령·시각](receipts/main-command.json) · [report·stderr·HTTP 대조](receipts/main-audit.json)

Linux x86_64, CPython 3.12.14, pip 24.0을 사용했다. 매 시행 새 venv에 지문을 맞춘 pip만 설치했다. dry-run에 `--ignore-installed --no-deps --only-binary=:all: --no-cache-dir`를 고정했다. 로컬 단일 URL, 설정 파일 무시, 검사용 환경의 외부 pip 변수·프록시 제외, pip 버전 검사 해제를 확인했다. 16회가 같은 loopback 포트에서 페이지 상태만 교체했고 원로그에는 로컬 페이지·파일 GET만 기록됐다. 외부 패킷에 대한 독립 캡처는 범위 밖이다. [실험 입력](inputs.json) · [정상 진입점](run.py) · [실행 환경·지문](receipts/main/suite.json)

## Q5. 경고 원채널과 과거 기록

기준의 `==8.1.0`이 두 번 모두 같은 wheel을 선택하며 stderr에 선택 경고 한 건과 `Reason for being yanked:` 원사유 줄을 냈다. 경고의 버전과 파일 URL은 같은 실행의 report와 맞는다. 나머지 기본 14개 시행의 stderr는 0 B다. 보조 empty의 stderr 경고는 한 건이고 사유는 `<none given>`이다. missing에는 선택 경고 0건과 두 resolver ERROR 줄이 있다. stdout에는 선택 경고 0건이다. 통과한 실행은 `Would install`을 출력했고 설치 목록은 실행 전후 모두 pip 24.0 한 건이었다. [원사유 stderr](receipts/main/pin-target-baseline-r1/stderr.txt) · [같은 report](receipts/main/pin-target-baseline-r1/report.json) · [빈 사유 stderr](receipts/controls/pin-target-empty-r1/stderr.txt) · [거절 stderr](receipts/controls/pin-target-missing-r1/stderr.txt)

2024년 3월 9일 H01 공개 제보는 정확 핀·같은 공개 파일 URL의 경고 및 캐시된 wheel 사용과 설치 성공을 보고했다. 그 로그의 pip 판·캐시 파일 해시·첫 서버 제공 시각은 미확인이다. 유지자의 3월 4일 조치 발언(H03)과 현재 Key dates(D10)는 최초 소비자 경고를 고정하지 않는다. H04에는 실제로 설치된 8.1.0의 특정 plugin hook 실패가 있고, H02에는 하류 fork가 정확 핀을 8.0.2로 바꾼 diff가 있다. 개발자 명령 선택·프로젝트 런타임·당시 배포를 각각 해당 근거 범위에서 판단한다. [H01 당시 캐시 로그](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847) · [H04 당시 hook 오류](https://github.com/pytest-dev/pytest/issues/12061) · [H02 하류 변경](https://github.com/hrushikesh-s/atomate2/commit/4e90106a626a0697a04baf5f9b1c9907bde4006b)

## Q6. 반전 통제와 재생

실행기는 기준의 바이트에서 대상 속성 하나를 삭제했을 때 `unmarked`와, 그 값만 비웠을 때 `empty`와, 앵커 한 줄만 삭제했을 때 `missing`과 각각 완전히 같은지 확인한다. 파일은 검증된 동일 바이트 배열에서 제공하며 URL 경로도 고정한다. 기본과 보조의 최초 실행은 그룹별 포트가 달랐고 재생에서는 네 페이지를 한 loopback 서버에서 실행했다. 기준/제거 쌍의 파일 명단 3/3과 wheel 바이트·해시가 같다. [fixture](index/) · [사전검사와 서버 구현](run.py) · [보조 2회](matrix-controls.csv)

링크 부재에서 Simple GET 자체는 200이다. 정확판의 적용 가능한 후보가 0개이며 파일 GET과 report도 0이다. 저장된 wheel과 파일 route는 유지했으므로 미러의 후보 누락이 원인이다. `empty`에서 같은 파일이 선택되는 결과는 이유의 비어 있음과 후보/속성의 부재를 구분한다. 최초 18개 시행과 재생 18개를 비교했고 URL의 임시 포트와 로그 시각·임시 경로를 정규화한 선택·SHA·경고·종료 및 GET 수에 불일치 0개였다. [두 조건의 원출력](receipts/controls/) · [재생 검산](receipts/replay-audit.json) · [재생 원출력 아카이브](receipts/replay-raw.tar.gz)

## Q7. 식별이 이어지는 경우의 안내

PLOS One의 전체 철회 사례에서 원 DOI `10.1371/journal.pone.0208143`의 원문이 열리고 2025-04-14 철회 공고 `10.1371/journal.pone.0322666`이 연결된다. 별도 공고의 Reference 1도 원문을 가리킨다. Retraction Watch의 고정 행 9947은 Record ID 64500, 원 DOI와 공고 DOI, `RetractionNature=Retraction`을 제공한다. 이 데이터의 `0:00`은 날짜 필드 표기다. Crossmark 대화창과 PubMed의 렌더링은 미확인이고, 실제 색인 값은 Crossref가 배포한 고정 CSV에서 직접 확인했다. [X01 공고](https://doi.org/10.1371/journal.pone.0322666) · [X02 원 DOI](https://doi.org/10.1371/journal.pone.0208143) · [X03 색인 행과 지문](receipts/publication-index.json)

또 하나의 실사례에서는 원 DOI `10.1371/journal.pone.0291840`과 정정 DOI `10.1371/journal.pone.0313792`가 연결된다. 공고는 특정 파일과 그림·분석 및 한계를 고쳤고, 편집위원은 결론이 계속 뒷받침된다고 기록했다. 별도 DOI 관계만으로 전체 철회처럼 처리하면 이 사례의 상태가 틀린다. 전체 철회 원문이 계속 열려도 새 근거로 쓸 때에는 철회 공고 상태를 적용한다. 발행사 정책에는 내용을 내리고도 식별 메타데이터를 남기는 예외가 있다. 설치기의 구체 선택은 해당 코드와 실행으로 확인했다. [X05 정정](https://doi.org/10.1371/journal.pone.0313792) · [X06 원문](https://doi.org/10.1371/journal.pone.0291840) · [X07 발행사 정책](https://journals.plos.org/plosone/s/corrections-expressions-of-concern-and-retractions) · [X04 Crossref 관계](https://www.crossref.org/documentation/principles-practices/best-practices/versioning/)

정확 재현에는 고정 파일과 해시를 첫 링크로 주고, 관측 날짜와 철회 사유를 붙인다. 새 범위에는 해당 상한 아래의 비철회 후보를 먼저 준다. 공개 저장소, 사용 중인 미러, 실제 잠금 또는 실행 환경이 달라지면 서로 다른 조건을 다시 확인한다. [목적별 문구와 링크](advice.md)

## 관점과 유지 비용

| 관점 | 함께 보존하면 해석 가능한 값 | 비용과 실패 조건 |
| --- | --- | --- |
| 정확 재현 사용자 | 요청식, 파일 URL·SHA, 원 플래그·사유, 관측 시점 | 파일이나 일치 지문을 확보하지 못하면 재현 불가로 표시한다. 정확 핀이 허용된 뒤에도 plugin과 환경을 별도로 확인한다. |
| 새 범위 사용자 | 상·하한, 후보별 제약·상태, 현재 선택과 유효한 대체판 | 배타 상한에 8.1.1을 넣으면 잘못된 추천이다. 8.1.1의 사설 API 제보는 이 후보의 프로젝트 검증이 필요함을 보여 준다. |
| 저장소 운영자 | 등록 키와 파일 콘텐츠, 전송 형식별 상태, 미러 수신 시각 | 릴리스별 상태만 저장하면 같은 파일의 해시와 실제 노출에 연결하기 어렵다. 파일 지문과 응답 관측을 함께 유지하는 비용이 생긴다. 미러가 숨긴 파일은 별도 상태다. |
| 출판사·색인 | 원 DOI, 공고 DOI, 업데이트 유형·영향 범위 | 색인과 발행사의 표면이 다를 수 있다. 원문 DOI가 열리는지만으로 새 근거 채택을 판단하면 철회와 정정을 구분하기 어렵다. |

직접 원자료 산입은 34개로 계획 하한 22개를 충족했다. 17개 출처 계보에서 자료를 읽었고 실증 사건은 pytest 철회 1건, PLOS 전체 철회 1건, PLOS 정정 1건이다. 기본 16회, 보조 2회, 별도 재생 18회는 문헌 수 밖이다. [분모와 자체 점검](SELF_CHECK.md)

| 중요한 불일치 또는 약점 | 영향을 받는 판단 | 다음에 볼 특정 자료·검사 | 판정이 뒤집힐 관측 |
| --- | --- | --- | --- |
| HTML 한 형식, 최대판 8.1.1, Linux x86_64의 pip 24.0으로 가둔 시뮬레이션 | 다른 클라이언트·공개 인덱스에서의 선택과 경고 | [I02 고정 포인터](inputs.json)를 바탕으로 같은 세 wheel을 Simple JSON 1.4 및 sidecar 제공 조건에서, 다른 명시 pip 판과 함께 비교 | 같은 후보·핀에서 다른 파일 SHA를 고르거나 빈 사유·철회 경고가 달라짐 |
| 의존성과 런타임을 제외한 dry-run이며 8.1.1도 일부 사설 API가 바뀜 | 실제 프로젝트의 정확 재현과 8.0.2 또는 8.1.1 대체 | [H04의 ixmp 환경·hook](https://github.com/pytest-dev/pytest/issues/12061)과 [H05의 private hook 제보](https://github.com/pytest-dev/pytest/issues/12069)에서 정확한 환경 핀을 구해 세 버전별 설치·hook 테스트 | wheel 선택이 같아도 한 환경에서 제약 충돌, hook 실패 또는 정상 회복이 확인됨 |
| 당대 H01은 캐시된 출력이며 216 원응답은 나중의 시점 | 철회 직후 최초 무캐시 선택·경고 UTC | [H01 게시 시점](https://github.com/pytest-dev/pytest/issues/12069#issuecomment-1986989847)과 2024-03-04 전후를 잇는 보존 Simple 응답·serial·무캐시 명령 로그 | 현재 스냅샷과 다른 파일 노출·플래그 또는 실제 사용자 경고가 시간과 해시로 고정됨 |
