# 표본 목록

선정은 sample/select.py, seed=2026112016. 과거 라벨은 baseline.json에 격리했다.

| 단위 ID | 표본 | cluster | 후보/내용 요약 |
|---|---|---|---|
| 004-R01 | 004 | P01 | Automerge Repo + IndexedDBStorageAdapter |
| 004-R02 | 004 | P01 | Yjs Y.Doc + y-indexeddb + network provider |
| 004-R03 | 004 | P01 | RFC 6902 JSON Patch를 도착 순서로 적용 |
| 004-R04 | 004 | P01 | Yjs Awareness CRDT에 메모 본문 저장 |
| 004-R05 | 004 | P01 | Automerge 사용 제안 — 저장 구성 미제공 |
| 004-R06 | 004 | P02 | RabbitMQ 4.1 quorum queue의 명시 구성 |
| 004-R07 | 004 | P02 | Redis PUBLISH/SUBSCRIBE |
| 004-R08 | 004 | P02 | Amazon SQS FIFO의 명시 구성 |
| 004-R09 | 004 | P02 | RabbitMQ 지속 큐 제안 — 정책 미제공 |
| 004-R10 | 004 | P03 | asyncio.Queue(maxsize=8) + 고정 worker 4개 |
| 004-R11 | 004 | P03 | Reactive Streams 1.0.4의 demand 규칙 |
| 004-R12 | 004 | P03 | Toyota Just-in-Time의 뒤 공정 인출→앞 공정 보충 |
| 004-R13 | 004 | P03 | Token bucket R=4/s, B=4만으로 작업 제어 |
| 004-R14 | 004 | P04 | restic 0.17.3 local repository |
| 004-R15 | 004 | P04 | Borg 1.2.8 encrypted local archives |
| 004-R16 | 004 | P04 | rsync -a --delete의 단일 mirror |
| 004-R17 | 004 | P04 | RFC 9162 Merkle inclusion proof |
| 004-R18 | 004 | P02 | R08과 같은 Amazon SQS FIFO 구성 |
| 011-T010-001 | 011 | T010 | 익숙한 언어·커뮤니티·디자인 분리 |
| 011-T010-002 | 011 | T010 | Spring / Django / Bootstrap 및 학습 |
| 011-T011-001 | 011 | T011 | Web Alert |
| 011-T011-002 | 011 | T011 | ChangeDetection / Visualping |
| 011-T011-003 | 011 | T011 | urlwatch / Specto |
| 011-T011-004 | 011 | T011 | curl+해시+필터 / 버전 관리 |
| 011-T011-005 | 011 | T011 | sitestalker |
| 011-T011-006 | 011 | T011 | Huginn |
| 011-T011-007 | 011 | T011 | Briefpanel |
| 011-T012-001 | 011 | T012 | GnuCash / ledger / Plain Text Accounting |
| 011-T012-002 | 011 | T012 | Mifos |
| 011-T014-001 | 011 | T014 | DaVinci Resolve + JDownloader |
| 011-T014-002 | 011 | T014 | FlexClip |
| 011-T023-001 | 011 | T023 | Form Tools |
| 011-T023-002 | 011 | T023 | Form Tools |
| 011-T024-001 | 011 | T024 | Args |
| 011-T024-002 | 011 | T024 | argparse |
| 011-T026-001 | 011 | T026 | SpecFlow |
| 011-T026-002 | 011 | T026 | Fluent Assertions |
| 011-T027-001 | 011 | T027 | 위치 DB 조회 또는 사용자 국가 입력 |
| 011-T027-002 | 011 | T027 | GeoIP/GeoLiteCountry 또는 MaxMind |
| 011-T036-001 | 011 | T036 | 표준 라이브러리 우선·필요 코드 이해 |
| 011-T036-002 | 011 | T036 | 통합 시간과 직접 구현 시간 비교 |
| 011-T036-003 | 011 | T036 | 복잡한 파서는 라이브러리·성숙도 확인 |
| 011-T036-004 | 011 | T036 | 큰 기능은 재사용·작은 기능은 직접 |
| 011-T036-005 | 011 | T036 | 개발뿐 아니라 교체·관리 시간 예측 |
| 011-T036-006 | 011 | T036 | 핵심 사업 코드만 직접 구현 |
| 011-T036-007 | 011 | T036 | 범위·업그레이드 비용·위험 비교 |
| 011-T036-008 | 011 | T036 | 변동성·신뢰·API 격리와 통합 테스트 |
| 011-T036-009 | 011 | T036 | 고성능·좋은 API이면 재사용 |
| 011-T036-010 | 011 | T036 | 표준 기능·낮은 변경률 우선 |
| 011-T036-011 | 011 | T036 | 라이브러리를 복사·선별 관리 |
| 011-T036-012 | 011 | T036 | 무조건 직접 구현 대신 덜 복잡한 대안 |
| 011-T036-013 | 011 | T036 | 성숙·표준적 라이브러리만 사용 |
| 011-T036-014 | 011 | T036 | 기회비용과 유지비용 비교 |
| 011-T036-015 | 011 | T036 | 보안·운영은 재사용, 차별화 핵심은 직접 |
| 011-T036-016 | 011 | T036 | 관리 중단 후 감당 가능하면 사용 |
| 011-T036-017 | 011 | T036 | 직접 책임질 코드 최소화 |
| 011-T036-018 | 011 | T036 | 가능하면 항상 재사용 |
| 011-T036-019 | 011 | T036 | 작은 npm 코드는 인라인·게시자 신뢰 고려 |
| 011-T036-020 | 011 | T036 | 활동·소스·인기도·문서로 선택 |
| 011-T036-021 | 011 | T036 | 장기 버전 지원·OSS·사용 비중 |
| 011-T036-022 | 011 | T036 | 대략 한 시간 이상이면 재사용 |
| 011-T036-023 | 011 | T036 | 사업 차별성·총소유비용으로 판단 |
| 011-T036-024 | 011 | T036 | 입력 파일 증가로 CSV 구현을 교체 |
| 011-T036-025 | 011 | T036 | 차별화·하드웨어 가속 때 직접 구현 |
| 011-T036-026 | 011 | T036 | 기능·플랫폼·라이선스·가격 적합성 |
| 011-T036-027 | 011 | T036 | 예상 수명·운영 위험에 따라 선택 |
| 011-T036-028 | 011 | T036 | React PDF의 경직성으로 pdf.js 직접 조합 |
| 011-T039-001 | 011 | T039 | Beanstalkd·Go라면 NATS 삽입 |
| 011-T039-002 | 011 | T039 | Blockqueue |
| 011-T039-003 | 011 | T039 | Redis 사용 |
| 011-T039-004 | 011 | T039 | ZeroMQ |
| 011-T039-006 | 011 | T039 | ElasticMQ |
| 011-T039-007 | 011 | T039 | NATS 단일 바이너리 |
| 011-T039-008 | 011 | T039 | 같은 호스트 IPC면 POSIX 큐·Redis |
| 011-T039-009 | 011 | T039 | SQLite 테이블로 큐 구현 |
| 011-T039-010 | 011 | T039 | RabbitMQ |
| 011-T041-001 | 011 | T041 | AlternativeTo |
| 011-T041-002 | 011 | T041 | selfh.st/apps |
| 011-T041-003 | 011 | T041 | awesome-selfhosted / ChatGPT / XDA |
| 011-T041-004 | 011 | T041 | Data Hoarding resources |
| 011-T041-005 | 011 | T041 | awesome-selfhosted |
| 011-T041-006 | 011 | T041 | Openalternative |
| 011-T041-007 | 011 | T041 | Baserow |
| 011-T041-008 | 011 | T041 | selfh.st 주간 뉴스레터 |
| 011-T041-009 | 011 | T041 | Self hosted newsletter / awesome-selfhosted |
| 011-T041-010 | 011 | T041 | Openalternatives |
| 011-T041-011 | 011 | T041 | 서브레딧 설명의 기존 목록을 사용 |
| 011-T047-001 | 011 | T047 | Rabbit/Kafka/Redis경험으로메시지유형·배포환경에따라관리형서비스선택. |
| 011-T047-003 | 011 | T047 | Kafka는경험없으면어렵다는운영비판. |
| 011-T047-005 | 011 | T047 | NATS를단순한도구로만취급하는전제에이의. |
| 011-T047-006 | 011 | T047 | NATS·Kafka·JetStream·Rabbit의전달방식비교,작으면Postgres테이블도대안. |
| 011-T047-007 | 011 | T047 | 서비스통신은NATS,지속성은JetStream으로보완. |
| 011-T047-008 | 011 | T047 | NATS임베딩과저장기능을기존서비스조합대신사용한경험. |
| 011-T047-010 | 011 | T047 | 서비스분리는부분실패·확장에이점이있다는반론. |
| 011-T047-013 | 011 | T047 | 구조화된단일앱에NATS를넣어향후분산을준비. |
| 011-T047-014 | 011 | T047 | Postgres와Watermill로충분했던직접경험. |
| 011-T047-018 | 011 | T047 | 이미Postgres가있다면테이블·확장으로큐구현. |
| 011-T047-019 | 011 | T047 | NATS임베딩·워커구성이쉬웠다는경험. |
| 011-T047-021 | 011 | T047 | NATS임베딩설명스레드링크만제시. |
| 011-T047-022 | 011 | T047 | MQTT호환성을활용한회사이전경험. |
| 011-T047-023 | 011 | T047 | MVP·성장·대규모단계별DB/모듈형앱/Kafka선택경험. |
| 011-T047-026 | 011 | T047 | Kafka운영·분산시스템조정은복잡하다는반박. |
| 011-T047-028 | 011 | T047 | 자가호스팅보다관리형Kafka또는Redpanda권유. |
| 011-T047-031 | 011 | T047 | 성능조정경험과RedisStreams작업큐추천. |
| 011-T047-032 | 011 | T047 | 기존Postgres에서pub/sub활용. |
| 011-T047-033 | 011 | T047 | NATS+JetStream. |
| 011-T047-036 | 011 | T047 | Kafka. |
| 011-T047-038 | 011 | T047 | NSQ. |
| 011-T047-040 | 011 | T047 | 동기처리부터검토;필요하면관리형큐또는파일·버킷을메시지전달로사용. |
| 011-T047-045 | 011 | T047 | 전달보장·규모부터묻고Postgres·측정부터시작;이른Rabbit도입후회. |
| 011-T047-046 | 011 | T047 | 작은부하는Redis큐. |
| 011-T047-048 | 011 | T047 | 태스크·잠금과스트림을구별하여NATS/Rabbit/Redis/Kafka선택. |
| 011-T047-052 | 011 | T047 | 모듈형앱에MQTT·Postgresnotify·ZeroMQ를역할별사용. |
| 011-T047-053 | 011 | T047 | Temporal을써서직접메시지큐를만들라는권유. |
| 011-T047-054 | 011 | T047 | 회사의Kafka사용경험. |
| 011-T047-055 | 011 | T047 | Riverqueue사용이쉬웠다는경험. |
| 011-T047-056 | 011 | T047 | 운영사고로Rabbit/NATS를피하고PG/Temporal선호;Kafka복제·대역폭비용우려. |
| 011-T047-057 | 011 | T047 | NATS/JetStream편리하나메시지크기제한을조건으로제시. |
| 011-T047-060 | 011 | T047 | Temporal링크만제시. |
| 011-T047-061 | 011 | T047 | ApacheIggy. |
| 011-T047-062 | 011 | T047 | Iggy복제가없어아쉽다는반박. |
| 011-T047-063 | 011 | T047 | Iggy복제개발중이라고보충. |
| 011-T047-064 | 011 | T047 | 과거NATS사용이좋았다는경험. |
| 011-T047-065 | 011 | T047 | NATS·Rabbit이단순하다는추천. |
| 011-T048-001 | 011 | T048 | Ubuntu+ZFS/btrfs,직접구성할의향에따른선택. |
| 011-T048-002 | 011 | T048 | ZFS는나중에디스크하나씩늘리지못한다는당시제약설명. |
| 011-T048-003 | 011 | T048 | 용량이금방차는경험을설명. |
| 011-T048-004 | 011 | T048 | Xpenology. |
| 011-T048-005 | 011 | T048 | Unraid. |
| 011-T048-006 | 011 | T048 | Xubuntu+mergerfs/SnapRAID·mdadm을직접구성한경험. |
| 011-T048-007 | 011 | T048 | OMV+ZFS와SnapRAID의동기화·무결성범위를설명. |
| 011-T048-008 | 011 | T048 | Windows유지시SnapRAID+DrivePool,증설이쉽다는추천. |
| 011-T048-009 | 011 | T048 | 자신은스크립트로주3회동기화한다는설명. |
| 011-T053-001 | 011 | T053 | vue-promise-modals 링크를 가능성으로 제시하며 조건이나 검증을 설명하지 않는다. |
| 011-T053-002 | 011 | T053 | vue-layerx 영문 README 링크와 사용 권유만 제공한다. |
| 011-T054-001 | 011 | T054 | 특정 로컬 모델은 시험하지 않았다고 밝히고 긴 도구 스키마·충분한 문맥·도구 경고 읽기, 덜 압축한 모델과 도구 수 축소를 제안한다. 회로 라벨·누락된 풋프린트·저장 거절 등을 구별하고 서버 버전을 되묻는다. |
| 011-T054-002 | 011 | T054 | 질문자의 Qwen 후보 반문에 시험하지 않은 모델명을 보증하지 않는다. 4–6비트 수준과 작은 도구 집합을 제안하고 같은 과제로 풋프린트·저장·BOM 요약의 일치를 확인하는 평가 절차를 준다. |
| 011-T054-003 | 011 | T054 | 후속 댓글에서는 Qwen 3.8 변형의 사용 인상이 가장 좋았다고 덧붙이되 정식 시험이 아니라고 한정한다. 추론 모드의 문맥 소비와 양자화·도구 수를 함께 바꾸어 보라고 한다. |
| 012-alternativeto | 012 | K06.2 | AlternativeTo |
| 012-arc42 | 012 | K06.1 | arc42 |
| 012-automerge-repo | 012 | P01.1 | Automerge Repo with IndexedDBStorageAdapter |
| 012-bazel-cache | 012 | P1.2 | Bazel Remote Cache |
| 012-beir | 012 | P01.2 | BEIR |
| 012-bibframe | 012 | P03.1 | BIBFRAME 2.0 |
| 012-celery | 012 | P02.w | Celery |
| 012-couch-conflicts | 012 | K04.1 | CouchDB Replication Conflict Model |
| 012-docspell | 012 | K02.1 | Docspell |
| 012-docspell-joex | 012 | P1.2 | Docspell JOEX |
| 012-event-sourcing | 012 | K06.w | Event Sourcing |
| 012-git-merge | 012 | K04.w | Git Three-Way Merge |
| 012-gov-needs | 012 | K06.w | GOV.UK Understand User Needs |
| 012-grafana-agent | 012 | K06.1 | Grafana Agent |
| 012-grafana-alloy | 012 | K04.2 | Grafana Alloy |
| 012-jiandu | 012 | P1.w | Jiandu |
| 012-librariesio | 012 | K02.2 | Libraries.io |
| 012-mixed-initiative | 012 | K05.w | Mixed-Initiative User Interfaces |
| 012-npm-bottleneck | 012 | P1.2 | bottleneck |
| 012-npm-lowdb | 012 | P04.w | lowdb |
| 012-npm-merkle-tree | 012 | P03.1 | merkle-tree |
| 012-npm-merkletreejs | 012 | P03.1 | merkletreejs |
| 012-npm-p-queue | 012 | P01.2 | p-queue |
| 012-npm-sharedb | 012 | P03.w | sharedb |
| 012-npm-y-webrtc | 012 | P2.2 | y-webrtc |
| 012-npm-y-websocket | 012 | P04.2 | y-websocket |
| 012-origami-solar | 012 | P02.2 | JPL Origami Solar Deployment |
| 012-otel-collector | 012 | K01.w | OpenTelemetry Collector |
| 012-otel-wal | 012 | K01.2 | OpenTelemetry Collector Persistent Sending Queue |
| 012-outpost | 012 | P2.1 | Outpost Offline Notes |
| 012-paperless-original | 012 | K06.w | Paperless |
| 012-pg-wal | 012 | P04.1 | PostgreSQL Write-Ahead Logging |
| 012-postgrest | 012 | K03.2 | PostgREST |
| 012-purl | 012 | P04.1 | Package URL |
| 012-pypi-aio-pika | 012 | K02.w | aio-pika |
| 012-pypi-aiolimiter | 012 | P03.1 | aiolimiter |
| 012-pypi-apscheduler | 012 | K04.2 | apscheduler |
| 012-pypi-arq | 012 | K04.w | arq |
| 012-pypi-borgmatic | 012 | K05.2 | borgmatic |
| 012-pypi-dedupe | 012 | P02.1 | dedupe |
| 012-pypi-dulwich | 012 | K03.1 | dulwich |
| 012-pypi-fastapi | 012 | P04.2 | fastapi |
| 012-pypi-huey | 012 | K06.w | huey |
| 012-pypi-janus | 012 | P02.1 | janus |
| 012-pypi-kombu | 012 | K02.1 | kombu |
| 012-pypi-opentelemetry-api | 012 | P04.1 | opentelemetry-api |
| 012-pypi-opentelemetry-exporter-otlp | 012 | K01.w | opentelemetry-exporter-otlp |
| 012-pypi-pdfplumber | 012 | P03.w | pdfplumber |
| 012-pypi-peewee | 012 | P03.2 | peewee |
| 012-pypi-pytesseract | 012 | K05.1 | pytesseract |
| 012-pypi-tenacity | 012 | K02.2 | tenacity |
| 012-pypi-unstructured | 012 | K05.2 | unstructured |
| 012-pypi-watchdog | 012 | P2.1 | watchdog |
| 012-qulac | 012 | K06.w | Qulac |
| 012-rabbit-confirms | 012 | P02.2 | RabbitMQ Publisher Confirms and Consumer Acks |
| 012-rsync | 012 | P04.w | rsync |
| 012-spring-batch | 012 | P1.w | Spring Batch |
| 012-sqs-standard | 012 | K01.w | Amazon SQS Standard |
| 012-uri | 012 | P2.1 | URI Syntax and Comparison |
| 012-web-annotation | 012 | K06.2 | W3C Web Annotation |
