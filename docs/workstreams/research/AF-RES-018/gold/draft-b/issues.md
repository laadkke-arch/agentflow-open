# AF-RES-018 검사 후보 준비 B — 결측과 범위

## 상태와 분모

이 파일은 실험 전 검사 후보 초안이다. A/P 검색·판정 실행이나 제품 실행을 하지 않았다. 작성자는 내부 별도 준비 작업자이며 정답의 외부 기록과 작업자 구성 후보를 JSON에서 구별했다. 고정011은 `478c301b693896e2c6d777f46ac441f071bfdfe8`, 고정014는 `42dc266dfd096bcc3c71f951fe0d9176f2eb9fd9`다.

17질문에 각각3행, 총51행을 준비했다. 현재 관측 창은 2026-11-21 UTC다. 실제 외부 답에 기반한 양성 행은15/17이고, 이 중 T054는 이름을 가진 제품이 아닌 평가 절차다. 현재 입력과 현재 공식 문서의 범위를 대응시킨 엄격 N은5/17이다. 공식 설명에서 역할이 다른 것으로 확인한 무관 후보는17/17이다. 양성·현재 엄격 N·무관의 세 역할을 모두 충족한 질문은4/17이다. 따라서 **51행 존재를 세 역할 완비로 보고해서는 안 된다.**

| 질문 | 양성 검사 후보와 근거 | 엄격 N 슬롯 | 현재 N 분모 | 결측·주의 |
|---|---|---|---|---|
| T033 | Ghost, 고정014 등급1 | GitHub Pages의 github.io 호스팅 서비스 | 예 | Enterprise Server나 별도의 블로그 엔진은 포함하지 않음 |
| T036 | JavaScript padStart, 고정014 등급1 | Lodash padStart, 0/unjudged | 아니오 | 필수 조건 없음 |
| T037 | Django, 고정014 등급1 | Jekyll 단독, 0/unjudged | 아니오 | 조합을 금지한 조건이나 공식 불지원 증거 없음 |
| T040 | Slurm, 고정014 등급1 | S3 events + 표준 Lambda 함수 | 예 | Managed Instances 및 외부 작업 위임 제외 |
| T043 | Rhasspy, 고정014 등급1 | 이미 비교 대상인 Mycroft | 예 | 과거 반박자의 삭제 계정 신원 불명 |
| T044 | MeshCentral, 고정014 등급1 | mRemoteNG, 역사적 N | 아니오 | 현재 방화벽/NAT 범위의 공식 부정 근거 부족 |
| T046 | Authentik, 고정014 등급1 | Authelia, 0/unjudged | 아니오 | 필수 조건 없음 |
| T048 | OpenZFS, 고정014 등급1 | Unraid, 0/unjudged | 아니오 | 기존 RAID5를 새 후보의 필수 조건으로 소급하지 않음 |
| T049 | OWASP File Upload Cheat Sheet, 고정014 등급2 | mime.TypeByExtension 단독 검증 | 예 | Go 전체나 내용 디코더를 결합한 파이프라인은 제외 |
| T054 | 같은 과제의4–6비트·축소 도구 집합 비교 절차, 실제 답을 작업자가 등급1로 추가 | Qwen3-Coder, 0/unjudged | 아니오 | 실제 답은 특정 모델의 성공 보증이 아니며 모델 N도 입증되지 않음 |
| T057 | Project Gemini, 고정014 등급1 | Neocities, 0/unjudged | 아니오 | 필수 조건 없음 |
| T058 | soft-serve, 고정014 등급1 | Codeberg, 0/unjudged | 아니오 | 필수 조건 없음 |
| T059 | Selenium, 고정014 등급1 | jsoup, 0/unjudged | 아니오 | 필수 조건 없음 |
| T061 | tinyMediaManager, 고정014 등급1 | Tautulli, 0/unjudged | 아니오 | 공식 소개의 비언급으로 자막·seedbox 불지원을 만들지 않음 |
| SX01 | Joplin, 양성 결측 자리의0/unjudged | NixNote2, 역사적 N | 아니오 | 실제 답3개 모두 반박됨; 현재 데이터 형식·내보내기 범위 미확인 |
| SX08 | Python str.translate 절차, 양성 결측 자리의0/unjudged | Markovify 기본 새 문장 생성 | 예 | 실제 답2개 모두 반박됨; 사용자 확장 가능성을 배제하지 않음 |
| SXR05 | FeSimpleArgs, 외부 API 채택 기록 등급2 | JCommander, 0/unjudged | 아니오 | 최초판에 임의 옵션 이름 조건 없음; 프로젝트 현재 본문 접근 불가 |

`checks-draft.json`에서 `grade`, `judgment_status`, 각 `eligible_*_denominator`를 함께 읽어야 한다. `grade: "0"`인 미판정 보조 후보를 알려진 무관 후보와 합치지 않는다. `grade: "N"`을 보존한 역사적 후보2개도 현재 검증 분모에는 포함하지 않는다. 이를 무시하면 양성 오거절 또는 엄격 N 거절률에 거짓 정답을 주입하게 된다.

## 1. T040: 상품 범위가 달라진 시간 제한

고정011 NM06은 최대 약1시간 작업과 당시 S3 이벤트·Lambda 권고의 실행 시간 충돌이다. 현재 AWS 공식 문서의 첫 설명은 기본 함수 최대900초이며, 바로 다음 설명은 Managed Instances의 비동기 및 일부 이벤트 소스 매핑 호출에서5400초를 허용한다. 같은 문서의 범위 차이를 누락하면 구조화 절차 자체가 옳은 후보를 거절할 수 있다. [`GB-lambda`, sources.json]

검사 후보를 **“Amazon S3 events + AWS Lambda standard function (Managed Instances 제외)”**로 한정한다. 또한 한 작업을 한 번의 표준 함수 호출에서 끝내는 경우다. 외부 워커 위임, 작업 분할, Managed Instances를 포함한 Lambda 전체를 N으로 만들지 않는다. 고정011의 역사적 사건과 현재 범위 확인은 별도 필드로 보존했다.

## 2. SXR05: 최초판과 후속 수정판의 조건이 다름

`questions/generate.py --emit SXR05`를 실행해 고정된 최초판 해시 `50546f4bb913a14f597e068cb4c81d7f038a5b868a4967a502eda6eeb22d28fb`를 확인했다. 최초판에는 Java 문자열 입력, GNU getopt와 유사한 처리, 묶은 짧은 옵션, 긴 옵션, `--`, 공백 처리, 플랫폼 요구가 있다. **임의 옵션 이름을 사전 선언 없이 받는 조건은 없다.** 파일 수·작은 구현·일부 라이선스·Map 반환 등 선호도 필수와 구별해야 한다. [`GB-revision-SXR05`]

고정011 NM18·NM19는 추천 당시 이미 수정된 질문 조건과 picocli/args4j 응답의 불일치다. 이 역사적 사건을 지우지 않았지만 최초판 입력의 검사 N으로 재사용하지 않았다. 공개 댓글38049·38056·38060은 조건이 뒤에 추가된 상황을 확인하며, 2017년 picocli 반박과2019년 갱신 주장은 서로 다른 범위다. [`GB-thread-SXR05`, `GB-api-comments`, `GB-fixed011-nearmiss`]

현재 `questions/old-metadata.json`의 SXR05 `must`는 고정011의 임의 옵션 조건을 유지하고 있다. **입력은 최초판이고 메타데이터는 후속 조건이라는 차이를 통합 단계에서 명시해야 한다.** 이 작업은 지정한 `draft-b/` 밖을 수정하지 않았다. 최초판에도 다른 필수 조건이 있으므로 must 유무 자체는 유지될 수 있지만, 검사 조건·원문 위치와 명칭은 최초판을 따라야 한다.

FeSimpleArgs는 `https://api.stackexchange.com/2.3/answers/38872?site=softwarerecs&filter=withbody`의 `is_accepted=true`를2026-11-21T04:07:45.424747+00:00에 확인했다. 따라서 등급2는 감사 표현을 해석한 것이 아니라 외부 채택 기록이다. 공식 Bitbucket 주소는 열렸지만 읽을 수 있는 본문이0줄이었다. 채택 사실과 현재 기능의 미확인을 구별한다. [`GB-api-accepted`, `GB-excluded-fesimpleargs`]

JCommander의 묶은 짧은 옵션 불지원 여부는 자신의 공식 문서에서 명시적으로 입증하지 못했다. 경쟁 도구 비교의 검색 결과를 공식 기능 근거로 바꾸지 않아 N unavailable로 남겼다. [`GB-jcommander`, SEARCH_LOG.json의 GB-Q05–GB-Q10]

## 3. SX01·SX08: 반박된 답을 양성으로 되살리지 않음

SX01의 Laverna·Turtl·NixNote 답에는 각각 질문의 핵심 목적과 관련한 반박이 남아 있다. Laverna의 “동기화 없이 작동”처럼 보이는 댓글51286은 같은 답의 다음 댓글51287에서 저장·새 문서 실패로 정정됐다. 따라서 현재 읽힌 긍정 한 줄만 골라 grade1을 만들지 않았다. Turtl의 데이터 독립성과 NixNote의 Evernote 서버 의존 반박도 남아 있다. [`GB-thread-SX01`, `GB-api-answers`, `GB-api-comments`]

SX08의 두 답은 각각 원문 단어 길이 대응과 무제약 텍스트 생성 문제로 반박됐다. 댓글103657과103656을 확인했다. 실제 채택·미반박 양성 답은 확인되지 않았다. [`GB-thread-SX08`, `GB-api-comments`]

Joplin과 일대일 문자 매핑을 쓰는 Python `str.translate`는 공식 설명상 살펴볼 가치가 있는 후보지만, 이 스레드의 실제 답 정답은 아니다. `positive` 슬롯의 모양을 유지하기 위한 `grade0/unjudged`로만 둔다. 양성 잘못 거절률의 분모에는 넣지 않는다. [`GB-joplin`, `GB-translate`]

NixNote 현재 문서의 Evernote 클라이언트라는 소개만으로 모든 로컬 사용이나 내보내기 가능성을 부정할 수 없어 현재 엄격 N은 보류한다. 반면 Markovify의 **수정하지 않은 기본 새 문장 생성**은 단어 위치별 길이와 문장부호 보존을 수행하는 변환이 아니며 실제 반박과 대응한다. 사용자 확장·후처리를 포함한 라이브러리 전체에 이 N을 적용하지 않는다. [`GB-nixnote`, `GB-markovify`]

## 4. T054: 제품 실체가 없는 실제 답

고정011의 T054.A001·A002는 특정 모델을 시험했다고 하지 않고 양자화, 도구 수, 같은 과제의 풋프린트·저장·BOM 일치를 확인하는 절차를 제안한다. T054.A003의 모델 사용 인상도 정식 시험이 아니며 모델의 실제 정체성은 미확인이다. [`GB-fixed011-cases`]

실제 답을 보존하려고 세 답을 별도 원칙·경험 단위로 추가했으며 검사 양성은 A002의 절차를 사용했다. `candidate_url`은 원 답에 없으므로 `null`로 남겼다. 질문 스레드 URL을 후보 URL로 내보내면 누설 제외 규칙과 충돌하므로 대신 넣지 않았다. 이 절차에 등급1을 부여한 사람은 **작업자**다. 공식 KiCAD MCP 저장소는 제품 맥락 확인용이고 이 절차의 성능 검증 근거가 아니다.

T054는 제품명 실체 recall에서 제외하고 원 답 단위·절차 포함 평가에서 다뤄야 한다. 제품형 양성만을 요구하는 민감도 분석에서는 양성 거절률 분모도15에서14로 줄어든다. Qwen3-Coder 소개로 KiCAD 과제의 실패를 추정하지 않았으므로 N도 미판정이다. [`GB-kicadmcp`, `GB-qwen`]

## 5. 공식 문서의 침묵을 실패로 바꾸지 않음

T036·T046·T057·T058·T059에는 고정 입력의 필수 조건이 없다. 이들에 가격·언어·호스팅·사이트 기능을 사후로 덧붙여 N을 만들지 않았다. T037의 Jekyll은 정적 생성기이나 외부 백엔드 조합을 문제에서 금지하지 않았고 공식 개요의 비언급만 읽었다. T048의 기존 저장 구조도 새 후보가 반드시 동일하게 제공할 조건이라고 단정하지 않았다. [`GB-jekyll`, `GB-unraid`, `GB-fixed014-rules`]

T044는 014 EXCLUSIONS에서 `클라이언트PC` 비교가 보류되는 항목이다. mRemoteNG의 공식 소개는 연결 관리자라는 범위를 확인하지만 구체 구성의 방화벽·NAT 도달성 불가능을 명시하지 않는다. 과거 NM10은 남기되 현재 N 분모에는 넣지 않는다. [`GB-mremoteng`, `GB-fixed014-rules`]

T061의 NM11은 이미 고정011에서 다른 독자가 뒤에 밝힌 필수성 때문에 엄격 N에서 제외됐다. MediaManager를 억지로 N으로 되살리지 않았다. Tautulli가 Plex 통계 중심이라는 사실만으로 외부 스크립트를 포함한 자막·seedbox 지원의 부재를 입증할 수도 없다. [`GB-fixed011-nearmiss`, `GB-tautulli`]

## 재현과 통합

이 초안은 다음 명령으로 저장된 근거 요약과 고정 파일에서 재생성할 수 있다. 네트워크 페이지를 다시 읽거나 A/P 실험을 실행하지 않는다.

```bash
python docs/workstreams/research/AF-RES-018/gold/draft-b/build_draft.py
```

최초판 재확인 입력은 다음과 같다. 본문은 터미널에만 표시되고 해당 명령이 저장된 해시를 대조한다.

```bash
python docs/workstreams/research/AF-RES-018/questions/generate.py --emit SX01
python docs/workstreams/research/AF-RES-018/questions/generate.py --emit SX08
python docs/workstreams/research/AF-RES-018/questions/generate.py --emit SXR05
```

실행 에이전트에 검사 후보를 공개할 때에는 `check_id`도 중립 ID로 바꾸고, `name`과 후보 `url` 및 필요한 범위만 전달해야 한다. `POS/N/ZERO`, 정답, `expected_action`, 누설이 되는 원 스레드·댓글 주소와 출처 라벨은 전달하지 않는다. 양 조건에는 동일한 후보 범위를 준다. 역사적 N과 미판정 행에 임의 정답을 만들어 주지 않는다.

## 한계

공식 문서 본문50개, 고정 연구 파일3개, 공개 스레드3개, 최초판 API3개, 답·댓글 API3개를 읽어 근거62항목으로 기록했다. 이는 사례·검사 후보 준비 자료이며 **방법 문헌25편 분모에는0개**다. 단순 제품 소개는 후보 정체성만 뒷받침하며 실제 사용 성공·보안·성능·전 조건 충족을 입증하지 않는다. 시간은 개별 도구가 초를 노출하지 않은 열람의 경우 UTC 관측 구간으로 남겼고 실제 API 응답에서 확보한 시각은 따로 남겼다. 실패한 공식 페이지와 경쟁 제품 검색 결과는 `sources.json.excluded`에 있어 본문 근거 수에 넣지 않는다. 익명 요청의 숫자 응답 코드는 `NETWORK.json`에 따로 기록한다. 사용자의 이름과 공개 본문 전문은 저장하지 않았다.
