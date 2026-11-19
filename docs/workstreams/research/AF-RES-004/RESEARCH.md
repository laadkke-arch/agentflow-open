# AF-RES-004 — 후보 유용성의 문서 기반 판정팩

## 1. 결론과 사용 범위

**이름·링크·기능 설명의 정확성만으로 추천의 유용성을 판정할 수 없다.** 판정 단위는 **문제 × 후보 × 제안한 역할 × 설정 × 제공 근거**여야 한다. 출처 연결(L), 원문의 주장 뒷받침(E), 필수 요구 충족(H), 분야 간 전이 논증(T)을 나누고, 결정적인 실패나 미확인을 다른 점수로 상쇄하지 않는 작은 판정 절차를 제안한다. 이는 이번 연구의 설계 제안이며 제품 계약이나 검증된 사용자 효용이 아니다.

이 묶음은 네 개의 합성 문제와 18개 판정 행으로 그 경계를 드러낸다. 작성자의 최초 기대 판단은 문서상 직접 적합 7개, 조건부 전이 3개, 알려진 제약 위반 6개, 자료 부족 2개다. 최초 v1.0 정답표는 독립 검토 전에 커밋했고, A/B의 최종 라벨은 각각 18/18 일치했다. 그러나 세부 H 값과 적용 층위에서 이견이 나와 v1.1에 반영했고, 후속 검토의 R12 연결 누락은 현재 v1.2에서 보완했다. 특히 R03-H2·R04-H1을 pass에서 unknown으로 좁혔다. 최종 라벨은 바뀌지 않았다. 원응답·이견·수정 검토는 [REVIEW.md](REVIEW.md)에 보존한다. 이 일치는 수작업으로 구성한 표본 안의 관찰이며 실효성 수치가 아니다. `DIRECT_DOCUMENTED`는 D1 문서 기반 판단이고 설치·실행·프로젝트 적용 성공을 뜻하지 않는다.

시작 SHA는 `bdc2e052900b1658981dfcec354682f4e1fc29fb`, 작업 브랜치는 `work/research-af-res-004`, 소유 경로는 이 디렉터리다. `depends_on: []`이고 다른 새 AF-RES 작업 결과를 보지 않았다. [AF-DOT-002 인계](https://github.com/laadkke-arch/agentflow-open/blob/06a57eba60c64389c614b5ce01238d9c4e337fbf/docs/workstreams/dot-trial/AF-DOT-002/HANDOFF.md)는 출처 ID 연결 검증을 추천 유용성 검증과 구분하는 시작 경계로만 사용했다.

## 2. 읽는 순서와 증거

| 파일 | 역할 |
| --- | --- |
| [PROTOCOL.md](PROTOCOL.md) | 후보 본문 조사와 답 작성 전에 고정한 판정 기준·보류·채점·독립 절차 |
| [CASES.json](CASES.json) | 기대 답을 포함하지 않은 문제·후보·역할·구성·원문 위치, 검토 순서 A/B |
| [EXPECTED.json](EXPECTED.json) | 독립 검토 전에 고정한 작성자 답·조건별 근거·반례·최소 확인 |
| [sources.json](sources.json) | 작성자가 직접 읽은 27개 자료의 URL·확인일·읽은 범위·확인 내용·한계 |
| [methodology-notes.json](methodology-notes.json) | 별도 조사자의 평가 방법론 6개 자료와 반대 근거. 작성자도 핵심 원문을 재확인 |
| [source-pins.json](source-pins.json) | 변하는 문서의 Git 원본 10개에 대한 실제 커밋·경로·blob SHA와 대조 범위 |
| [blind-review-a.json](blind-review-a.json), [blind-review-b.json](blind-review-b.json) | 기대 답을 보지 않은 내부 검토의 원래 응답 |
| [REVIEW.md](REVIEW.md) | 작성자 기대와 독립 응답의 비교, 이견 원인과 처리 |
| [revision-review.json](revision-review.json) | v1.1 수정의 B 비블라인드 후속 검토와 발견한 잔여 이견. v1.2의 한 항목 재확인은 REVIEW에 기록 |
| [VERIFICATION.json](VERIFICATION.json) | 자료 구조·원격 저장·수정 범위 확인과 미실시 |
| [HANDOFF.md](HANDOFF.md) | 최종 상태와 다음 담당자의 첫 행동 |

외부 자료는 **33개**다. 기능·규격 자료 27개와 방법론 자료 6개이며, 그중 31개는 명시한 본문 절을 직접 읽었고 2개(M01/M03)는 공식 초록·서지만 읽었다. 전 페이지 완독을 주장하지 않는다. 검색 결과만 있는 자료·열람 실패·동일 페이지 재열람·운영 지침·원본 문서의 Git 사본은 추가 자료로 세지 않았다. 독립 검토자의 재열람도 수를 늘리지 않는다.

확인일은 UTC 2026-11-19 / 한국 2026-11-20이다. RFC와 논문은 번호·연도·절, Python/restic/Borg는 버전 경로, Reactive Streams는 v1.0.4가 가리키는 커밋을 남겼다. Automerge/Yjs/RabbitMQ 문서는 Git 원본 커밋을 추가했다. **문서 커밋 고정은 실행 바이너리 버전 고정과 다르다.** 특히 RabbitMQ 4.1 경로에도 4.3 이후 정책 변경 설명이 있어, 이 팩에서는 확인한 선언 인자 `x-delivery-limit=-1`만 사용하고 4.1의 정책 변경 기능을 추정하지 않았다. 원본 SHA 10건은 작성자도 GitHub에서 다시 읽어 blob SHA를 대조했다. 라이브 페이지 전체와 Git 파일의 byte 동일성을 주장하지 않는다. [S08/S09 및 pin P08/P09](source-pins.json)

## 3. 평가 방식의 대안과 조합

아래 비용·장단점은 읽은 연구를 이 과제에 적용한 연구자 판단이다. 실제 소요 시간이나 사용자 효과를 측정한 결과는 아니다.

| 방식 | 얻는 것 | 전제·대가·실패 조건 | 이 팩에서의 위치 |
| --- | --- | --- | --- |
| 이름/태그/출처 ID 연결 검사 | 잘못된 참조, 누락된 링크를 찾기 쉬움 | 링크가 살아 있어도 엉뚱한 버전·기능·대상을 인용할 수 있음 | L의 선행 검사에만 사용 |
| 사실·인용 지원 검사 | 주장과 원문 사이의 거짓·과장·근거 부족을 구분 | 참인 기능 설명이 해당 요구를 해결한다는 보장은 없음. 문장 분해와 복수 근거 대조가 필요 | E 축. 부분 지원을 전체 지원으로 올리지 않음 |
| 요구별 체크리스트 | 알려진 필수 제약 위반을 명확히 추적 | 문제 범위가 빠졌거나 설정이 없으면 미확인으로 남겨야 함. 모든 것을 사후 가정하면 무의미해짐 | H 축. pass/fail/unknown을 보존 |
| 관계 대응 + 반례 | 다른 분야의 원리가 어떤 부분에 도움이 되는지 설명 | 구현 연결·불변조건·실패 모델이 추가로 필요. 구조 대응만으로 실효성 입증 불가 | T 축과 조건부 전이 |
| 사용자 과제/실제 통합 시험 | 실제 설정·상호작용·업무 결과를 관측 | 더 큰 비용, 실행 환경, 사용자 모집이 필요. 이번 정적 팩으로 대신할 수 없음 | D3/D4 또는 별도 인간 평가 후속 |

[FEVER(M04)](https://aclanthology.org/N18-1074.pdf)는 지지·반박·정보 부족을 분리하며, 라벨이 맞아도 근거가 불충분할 수 있음을 보여 준다. 다른 국적을 제시했다고 특정 국적을 자동 반박할 수 없다는 사례는 “미기재=부재” 오류를 피하는 데 직접 도움이 된다. 다만 Wikipedia 사실검증의 결과를 소프트웨어 통합 성공으로 옮기지는 않는다.

[ALCE(M05)](https://aclanthology.org/2023.emnlp-main.398.pdf)는 내용 정확성·유창성·인용 품질을 구분한다. 원문 구절을 복사하는 방식은 인용 품질이 좋아도 좋은 답이 아닐 수 있다. 따라서 이 팩은 “이 기능이 있다”와 “이 문제의 이 조건을 만족한다”를 따로 기록한다. 자동 함의 판단이 실행 증거는 아니다.

[Gentner(M06)](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf)의 구조 대응은 외형 속성보다 관계와 관계의 연결을 보도록 한다. 여기서 얻는 것은 전이 가설을 설명하는 틀이다. 소프트웨어 환경의 실패·취소·시간·권한 조건을 없애 주는 실증은 아니다.

이 방식들은 경쟁하는 하나의 총점이 아니다. L→E 확인 후 각 H와 T를 기록하며, 알려진 결정적 실패는 직접 승인할 수 없다. 결정적 미확인이 남으면 자료 부족이다. 참고 역할의 조건부 전이는 원래 필수 제약을 풀어 주는 면제권이 아니다.

## 4. 네 문제에서 드러나는 경계

| 고정 문제 | 문서상 직접 적합 기대 | 조건부 참고 기대 | 위반 또는 자료 부족 기대 |
| --- | --- | --- | --- |
| P01 오프라인 공동 메모 | R01 Automerge+명시 저장 adapter, R02 Y.Doc+y-indexeddb+전달 provider | 없음 | R03 도착순 JSON Patch: 비수렴. R04 Awareness 본문: 영속성 실패. R05 저장 구성 미제공: 보류 |
| P02 중단 뒤 재처리할 작업 큐 | R06 명시한 quorum/ack/정책, R08 명시한 FIFO/보존/멱등 handler | 없음 | R07 Pub/Sub: 단절 중 손실. R09 큐 정책·ack 시점 미제공: 보류. R18 비멱등 외부 효과: 중복 반영 |
| P03 느린 sink의 작업 수 상한 | R10 유한 큐+고정 worker+await 흐름 | R11 demand→완료 credit, R12 제조 보충 신호→permit 회수 | R13 시간 기반 token bucket 단독: 처리 중 개수 상한 실패 |
| P04 로컬 암호화 백업과 부분 검증 | R14 restic, R15 Borg의 지정 구성 | R17 Merkle inclusion→manifest membership | R16 평문 단일 rsync mirror: 이전 판·암호화 실패 |

이는 **최초 및 현재 v1.2의 동일한 최종 라벨 요약**이다. v1.1에서는 R03의 재진입 복구와 R04의 오프라인 편집 수명에 대한 비결정적 H 값을 unknown으로 바로잡았다. 각 row는 입력에 선언된 구성에만 적용된다. 좋은 브랜드/나쁜 브랜드 목록이 아니다. 다른 adapter·queue policy·backup 경로·reference scope를 주면 새로운 판정 행이 된다. 전체 시스템을 대신하는 대안, 재사용 부품, 부분 참고를 같은 역할로 섞지 않는다.

### P01: 수렴과 영속성은 다른 질문

[Automerge Storage(S01)](https://automerge.org/docs/reference/repositories/storage/)는 StorageAdapter 없이 transient 상태일 수 있음을 설명한다. [Yjs Offline(S04)](https://docs.yjs.dev/getting-started/allowing-offline-editing)은 y-indexeddb와 앱 shell 캐시를 구분한다. [Yjs Awareness(S06)](https://docs.yjs.dev/getting-started/adding-awareness)는 presence 상태가 Y.Doc에 보존되지 않는다고 설명한다. 따라서 “CRDT를 쓴다”만으로 재진입 후 본문 보존을 승인할 수 없다.

[JSON Patch(S07), §3/§4.3](https://www.rfc-editor.org/rfc/rfc6902.html)의 순차 replace 의미를 사용하면, 같은 title에 A/B를 역순으로 적용한 두 replica가 다른 최종 값을 갖는 반례를 만들 수 있다. 이는 규격과 합성 trace로 도출한 논리 반례이며 실제 실행 로그가 아니다. 전역 순서를 추가하면 별도 구성이므로 현재 오답을 구제하기 위해 몰래 넣지 않는다.

### P02: 전송 중복 제거와 외부 효과는 다른 경계

[RabbitMQ Reliability(S08)](https://www.rabbitmq.com/docs/4.1/reliability)는 publisher confirm과 consumer ack의 역할 및 재전송 중복을 구분한다. [Quorum Queues(S09)](https://www.rabbitmq.com/docs/4.1/quorum-queues)는 복제·다수 생존 조건과 poison-message delivery limit을 설명한다. 그래서 R06은 단순 durable 선언보다 좁고 구체적이다. R09의 누락 설정을 기본값으로 채워 넣어 거절하거나 승인하지 않는다.

[Redis Pub/Sub(S10)](https://redis.io/docs/latest/develop/pubsub/)의 at-most-once 의미에서는 단절 중 놓친 메시지를 단순 재구독으로 복원할 수 없다. 이 실패는 Redis Streams 등 다른 제품 구성에 대한 판정이 아니다.

[SQS FIFO deduplication(S14)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)은 송신 중복 제거 구간을 설명한다. [Visibility timeout(S12)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)은 receive 후 삭제하지 않은 메시지가 다시 보일 수 있는 수명주기를 설명한다. 따라서 외부 증가→worker 중단→DeleteMessage 미실행→재전달→두 번째 증가라는 R18 반례가 가능하다. FIFO 이름이 같아도 R08에 주어진 영속 멱등 처리 경계를 제거하면 판단이 달라진다. 두 검토자가 지적한 S12의 12시간 visibility 상한을 작성자도 다시 읽었다. v1.1은 retention 24시간과 visibility 한계를 분리하고, 완료 시한을 수락부터 대기·장애·재시도를 포함한 총 경과시간 24시간 미만으로 명시한다.

### P03: 시간 비율과 진행 중 개수의 단위가 다르다

[asyncio.Queue(S15)](https://docs.python.org/3.13/library/asyncio-queue.html)는 양의 maxsize에서 full queue에 대한 put이 기다린다고 설명한다. 큐에 들어 있는 개수와 worker가 처리 중인 개수는 다르므로 R10은 각각 8과 4로 제한한다. producer가 손에 든 항목과 각 항목의 byte 크기는 별도이며 전체 RAM 상한으로 일반화하지 않는다.

[Token bucket RFC3290(S19), §5.1.3/A.4](https://www.rfc-editor.org/rfc/rfc3290.html)의 token은 시간에 따라 보충된다. 미완료 작업 4개가 멈춰 있는데 1초 뒤 4개를 더 시작할 수 있다는 반례는 rate≤4/s와 concurrency≤4가 다른 조건임을 드러낸다. rate limit은 별도의 유용한 제어지만 현재 상한을 대체하지 못한다.

### P04: 사본·과거 판·암호화·포함 증명은 서로 다른 기능

[restic 복원(S22)](https://restic.readthedocs.io/en/v0.17.3/050_restore.html)과 [설계(S23)](https://restic.readthedocs.io/en/v0.17.3/design.html), [Borg Quick Start(S24)](https://borgbackup.readthedocs.io/en/1.2.8/quickstart.html)는 선택한 판 복원과 지정 암호화 구성을 뒷받침한다. 키 보유·보존 대상 미삭제·고정 원본은 이 문제의 given이다. 최신 추천 릴리스나 보안 감사 결론을 내리지 않았다.

[rsync manpage(S25)](https://download.samba.org/pub/rsync/rsync.1)는 --delete뿐 아니라 --backup/--backup-dir도 제공한다. 이 반대 근거 때문에 “rsync는 백업으로 부적합”이라는 첫 일반화를 버리고 **이력·암호화가 없는 단일 mirror라는 R16 구성**에만 실패 판정을 한정했다.

[RFC9162(S26), §2.1.3](https://www.rfc-editor.org/rfc/rfc9162.html)의 포함 증명은 선택한 root에 leaf가 속하는지를 확인하는 관계다. 파일 데이터의 존재·암호화·복원을 보장하지 않는다. §2.1.4의 append-only consistency를 파일 삭제가 가능한 임의 snapshot 사이에 그대로 요구해서도 안 된다.

## 5. 다른 분야 원리의 전제·대가·실패

| 참고 행 | 보존하려는 관계 | 필요한 연결과 대가 | 적용하면 안 되는 경우 |
| --- | --- | --- | --- |
| R11 Reactive Streams | 누적 발행 수가 누적 demand를 넘지 않음 → 허용 credit만큼 작업 투입 | Python adapter, 완료 후 재요청, 유한 중간 buffer, 취소/실패 시 permit 회수 규칙 | 수신 즉시 credit을 돌려주며 처리 task를 계속 만드는 구성. JVM 규격을 Python 구현 증거로 취급 |
| R12 Toyota Just-in-Time | 하류가 사용한 양에 따라 상류가 보충 → 완료한 slot만 다시 허용 | 숫자 4/8은 별도 software 장부로 구현. 최종 sink 완료 event, 누수/이중 회수 방지 | pull이라는 이름만 붙이거나 큐에서 꺼낸 순간 완료라고 보는 구성. 제조 성과를 software 성능으로 전용 |
| R17 CT Merkle inclusion | 신뢰 root에 대한 leaf 포함 → 특정 backup manifest 항목의 포함 | 결정적 인코딩·순서·tree size/index·root 보관을 정하고 다른 backup 구성과 결합 | root도 검증 대상이 임의 제공. inclusion을 보존·복원으로 오인. 삭제 가능한 snapshot에 append-only 조건 강제 |

[Reactive Streams(S17), v1.0.4](https://github.com/reactive-streams/reactive-streams-jvm/blob/944163a4b2477a2bebaaada86b0ba910b6302f2f/README.md)의 수요 규칙은 발행·수신 경계의 규격이다. 완료 시점을 sink 저장 뒤로 늦추는 것은 대상 시스템의 추가 설계다. 취소도 즉시 모든 효과가 사라진다는 보장이 아니다.

[Toyota TPS(S18)](https://global.toyota/en/company/vision-and-philosophy/production-system/)에서 직접 확인한 것은 뒤 공정 인출에 따른 앞 공정 보충이다. 4개 permit을 증명하는 정리나 Python 코드가 아니다. 이 구분을 유지하면 타 분야 참고는 설계 설명에 도움이 되는 가설로 남고, 제조업의 권위를 가져온 허위 검증이 되지 않는다.

R12의 이 연결 조건은 초기 입력에서 충분히 명시되지 않아 비블라인드 수정 검토에서도 지적됐다. v1.2는 실제 producer의 대기와 선행 task·우회 무한 buffer 금지를 새로 명시한다. 숫자 장부만으로 producer 대기가 생긴다고 추정했던 설명은 충분하지 않았다. 이 변경은 대상 측 설계의 보강이며 Toyota 원문의 기능을 늘리는 일이 아니다.

세 참고 원리는 다른 부품과 조합할 수 있다. R11/R12는 R10의 admission/완료 설명을 보완할 수 있으나 실제 수치 상한은 명시된 제어 흐름에서 확인해야 한다. R17은 R14/R15 같은 보존 도구와 별개의 manifest 검증 층으로 생각할 수 있지만 이번 조사에서 그 통합을 구현하거나 비용·사용 편의의 이득을 측정하지 않았다.

## 6. 처음 결론을 깨는 검사

| 처음 떠올리기 쉬운 결론 | 찾아 확인한 반대 경우 | 남긴 판정 원칙 |
| --- | --- | --- |
| 출처가 연결되면 추천도 유효하다 | ALCE의 정확한 인용과 답변 품질 간 차이; 기능 설명은 요구 충족이 아님 | L/E/H를 분리 |
| CRDT이면 offline 저장도 된다 | Automerge adapter 미설정, Yjs Awareness의 비영속성 | 알고리즘과 저장 구성을 별도 확인 |
| durable/confirm/manual ack면 충분하다 | 복제·TTL·delivery limit·ack 시점이 다르면 보존 결과가 달라짐 | 모르는 설정은 unknown |
| FIFO exactly-once가 외부 결과도 한 번으로 만든다 | receive와 외부 효과, DeleteMessage 사이의 중단 | 효과 경계와 멱등성을 분리 |
| 초당 K개면 동시에 K개 이하이다 | task가 끝나지 않아도 시간 token은 다시 생김 | rate와 in-flight 개수 구분 |
| rsync라는 이름이면 백업 실패다 | --backup-dir 등 다른 구성은 이력 보존 경로가 될 수 있음 | 브랜드 대신 지정 구성에 라벨 |
| 같은 구조를 옮기면 성공도 전이된다 | 원 분야에 없는 취소·실패·trust anchor·인코딩이 필요 | mapping+bridge+failure를 함께 요구 |
| 모든 자료 부족은 오답이다 | 미기재 adapter/queue policy는 있을 수도 없을 수도 있음 | 보류와 명시 실패 분리 |
| 많은 사람이 동의하면 적용도 검증됐다 | 정적 내부 판정은 실제 환경·사용자의 비용/성과를 관측하지 않음 | 일치율을 실효성 수치로 부르지 않음 |

반례의 종류도 구분한다. 문서가 명시한 기능 제한, 명시된 구성에서 도출한 논리 trace, 실제 실행 관측은 서로 다르다. 이번 기능 반례는 앞의 두 종류이며 실행 관측을 만들었다고 쓰지 않았다.

## 7. 독립 평가, 보류와 합격/실패 예시

다음 절차는 이번 내부 검토에 사용하며, 이후 새 판정자도 그대로 재현할 수 있다.

1. 기준 커밋, 입력 커밋, 검토자 ID와 순서를 기록한다. 기대 답은 별도 파일·커밋으로 고정하고 검토자 문맥에 제공하지 않는다.
2. 검토자에게 PROTOCOL, CASES, 연결된 원문만 준다. 같은 문제 작성에 참여한 사람/에이전트를 블라인드 검토자로 세지 않는다.
3. 각 행의 역할·적용 범위를 먼저 고정하고 L/E/조건별 H/T와 원문 위치를 기록한다. 알려진 실패·미확인·가설을 구분한다.
4. 원래 응답을 저장한 후 기대 답과 대조한다. 라벨이 같아도 근거가 틀리면 그대로 합격시키지 않는다.
5. 이견을 자료 접근, 사실, 입력 해석, 역할 범위, 전이 가정, 절차 한계로 나눈다. 유효한 새 근거는 “정답표와 다름”만으로 버리지 않는다.
6. 원래 응답을 보존하고 작성자 판단·수정·미해결을 별도 기록한다. 이견 공개 뒤의 대화는 새 블라인드 판정으로 세지 않는다.

| 응답 예시 | 판정 |
| --- | --- |
| R05에서 “adapter 미기재이므로 저장 여부를 보류하며 초기화 구성을 요청한다” | 알려진 기능과 미확인 설정을 구분한 적절한 보류 |
| R05에서 “문서에 adapter가 있으니 이 제안도 영속적이다” | 근거 없는 확정. fail gate |
| R05에서 “설명에 adapter가 없으니 제품은 저장을 지원하지 않는다” | 미기재를 부재/제품 결함으로 바꾼 오류 |
| R13에서 token bucket의 time refill과 미완료 8개 trace를 들어 현재 요구를 거절 | 결정적인 제약을 추적한 응답 |
| R18에서 FIFO의 링크가 맞다는 이유로 단일 외부 효과를 승인 | L 통과로 H3 실패를 덮은 오류. fail gate |
| R12에서 관계·추가 장부·완료 event·실패 조건을 적고 구현 미실시를 명시 | 조건부 전이 설명의 최소 형태 |
| R17을 “Merkle tree니까 암호화 백업 대안으로 적합”이라고 판정 | 역할 변경 및 기능 과장. fail gate |

필수 gate는 결정적 위반의 직접 승인 0, 자료 부족의 검증된 효용 승격 0, 전이의 대응·연결·실패 조건 기록, 증거 수준의 정직한 표기다. 보조 점수는 근거 정확성/제약 추적/설명 유용성 각각 0~2로만 진단하고 총점을 만들지 않는다. 예를 들어 라벨만 맞고 근거가 없는 답은 근거 0·제약 추적 0 또는 1이며, 올바른 자료 부족과 답을 바꿀 구체 확인을 제시한 답은 해당 차원에서 2가 가능하다. 모든 사례를 보류하는 전략도 확인 가능한 근거를 사용하지 않았다는 별도 결함이 된다.

독립성은 새 문맥과 기대 답 비공개에 한정한다. 공유 파일시스템을 강제로 격리하지 않았고 동일 계열 내부 모델일 수 있다. 인간 평가·다른 모델 계열 검증·실제 사용자 업무 시험은 미실시다. 원래 응답과 대조 결과는 REVIEW에 근거하여 보고한다. A는 26개 자료를 읽고 미사용 S11은 열지 않았으며, B는 27개를 읽고 S11을 Standard/FIFO 범위 구분의 배경으로만 사용했다. 두 원응답을 먼저 커밋한 뒤 v1.1을 만들었다. H의 문서적 설계 충족과 실제 구현 관측을 별도 필드로 표시하는 명확화는 v1.0 블라인드 결과로 소급 검증됐다고 주장하지 않는다.

## 8. 표본, 미해결과 최소 다음 확인

[불완전 판정 연구(M02)](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=150469)는 미판정과 비관련을 섞는 문제를 다루며, 대체 지표에도 표본·판정 풀의 한계가 있음을 남긴다. 이 팩은 작성자가 고른 18행이고 세계의 적합 후보 전체를 모른다. 전체 검색 recall/precision/nDCG, 제품 승률, 방법 간 성능 우위, 누락된 유용 후보가 없다는 결론을 보고하지 않는다.

[판정 차이에 관한 M01](https://www.nist.gov/publications/variations-relevance-judgments-and-measurement-retrieval-effectiveness)의 공식 초록은 특정 TREC 실험에서 판정 차이에도 상대순위가 안정적일 수 있음을 보고한다. 이 작은 팩도 안정적이라는 근거는 아니다. [M03](https://www.nist.gov/publications/philosophy-information-retrieval-evaluation)의 통제된 비교 연구 관점 역시 실제 사용자 효용과 구별한다. 두 자료는 초록 범위까지만 확인했다.

| 미해결 | 답을 바꿀 최소 확인 | 이번 결과의 한계 |
| --- | --- | --- |
| 문서 적합 구성이 실제 환경에서도 작동하는가 | 각 EXPECTED의 minimum_next_check에 따라 고정 버전·작은 입력·실패 시점을 지정한 D3 시험 | 설치/서비스 호출/통합 실행을 하지 않음 |
| 참고 원리 설명이 실제 설계에 도움이 되는가 | 처음 보는 판정자에게 source→target mapping을 만들게 하고 필요 연결·실패를 추적. 이후 소규모 적용 비교 | 관계가 설명 가능하다는 연구 가설까지만 |
| 작성자가 의도한 반례 밖에서도 기준이 유효한가 | 기대 답을 보지 않은 다른 작성자가 새 holdout 문제와 근접 오답을 구성 | 현재 사례는 독립적으로 추출한 대표표본이 아님 |
| 설정이 빠진 후보의 실제 적합성 | R05 초기화/저장 경로, R09 queue declaration·정책·ack 위치 | 누락을 임의의 기본값으로 채우지 않음 |
| 사용자가 실제로 얻는 시간·품질 이득 | 명확한 업무와 성공 기준을 가진 사용자 과제 관측 | 인간/고객 자료/비용 절감 시험 미실시 |
| 살아 있는 웹 자료의 재현성 | 명시한 Git pin 우선, 다른 자료는 지정 절 재확인 및 변경 기록 | 모든 웹 본문을 보관한 아카이브는 아님 |

후속 D3가 현재 연구 완료의 숨은 조건은 아니다. 이 작업은 검증된 실효성을 주장하지 않고, 검증 가능한 문서 기반 기대 판단·반례·절차를 인계하는 범위다. 저장소 공통 검사 미실시와 정확한 재실행 명령은 HANDOFF와 VERIFICATION에 남긴다. 자동 평가기나 신규 검색 방식은 만들지 않았다.

## 9. 기준·입력 변경 기록과 색인 제안

| 시점 | 변경 | 이유와 영향 |
| --- | --- | --- |
| 기준 최초 동결 f4f08a0e | 4축·4라벨·fail/unknown 우선순위·표본·블라인드 절차 | 외부 후보 본문 조사·기대 답 이전의 기준. 외부 연구 등록 서비스의 사전등록은 아님 |
| 입력 최초 동결 전 | FIFO 전용 복제 문서 S27 추가, 변동 문서 Git pin 추가 | standard queue 문서를 FIFO 보존의 근거로 대신 쓰지 않기 위해 보강. extra Git 사본은 추가 자료로 세지 않음 |
| 입력 최초 동결 전 | restic의 named snapshot 표현을 식별 가능한 snapshot으로 좁힘 | 이름 붙이기를 필수 기능처럼 암시하지 않고 ID 선택이라는 실제 문서 범위를 사용 |
| 입력 b245a275 / 답 13e76552 동결 | CASES와 EXPECTED를 별도 커밋 | 입력은 기대 라벨·작성자 해석을 숨김. 답을 독립 응답보다 먼저 저장 |
| v1 원판정 보존 | A 29baa1d1 / B d0a2f23b | 각각 라벨 18/18 일치. A의 H 값 1건, B의 H 값 5건이 원 기대와 다름. 서로 겹치는 항목을 합치면 5개 조건·4개 행 |
| PROTOCOL v1.1 e36abce4 | H_assessment_scope와 runtime_observation을 구분 | reference의 설계상 pass를 구현 성공으로 읽는 모호성 해소. 축·라벨·우선순위·gate는 유지 |
| CASES v1.1 b8b965ed | P02의 시간 기산점·총 경과시간, R08의 visibility 12시간 한계, R18 S13 연결 | 두 검토자가 실제 사용한 시간 해석을 명문화. 반복 송신 dedup과 수신 후 외부 효과를 구분하는 대조는 유지 |
| EXPECTED v1.1 d74f77e6 | R03-H2와 R04-H1을 unknown으로 수정, reference의 미관측 구현 값 분리 | 독립 지적을 채택해 비결정적 과잉 확정을 제거. 최종 라벨 18개는 유지 |
| 수정 검토 d6cfd4fb | revision-review.json | B가 v1.1 변경을 확인하면서 R12의 producer 대기 연결 누락을 추가 지적. 해결됐다고 덮어쓰지 않음 |
| CASES/EXPECTED v1.2 ba1b7737 / 24640144 | R12에 실제 producer 대기·선행 task 금지·우회 무한 buffer 금지를 추가 연결 조건으로 명시 | 단순 문구 정리가 아니라 대상 설계 연결의 보강. 제조업 원문의 기능이나 v1 블라인드의 성과로 소급하지 않음. 비블라인드 한 항목 재확인은 REVIEW에 기록 |

P04는 처음부터 `applies_to`로 완성 백업과 manifest 참고 조건을 나눴다. 전체 대안의 필수 요구를 사후 면제하는 용도로 `not_in_scope`를 사용하지 않는다. 어떤 기준도 답을 맞추기 위해 조용히 완화하지 않는다.

공통 `docs/research/INDEX.md` 변경은 하지 않았다. 진행 담당에게 제안할 한 행은 다음과 같다.

| ID | 질문 | 상태 제안 | 진입점 | 의존성/경계 |
| --- | --- | --- | --- | --- |
| AF-RES-004 | 이름 유사성·요구 적합·타 분야 전이를 어떻게 구분하는가 | REVIEW_READY — 문서 기반 판정팩, 내부 독립 검토 포함 | docs/workstreams/research/AF-RES-004/RESEARCH.md | depends_on 없음; D1 기대 판단이며 D3/D4·사용자 효용 미검증 |

최종 DB/API/검색 스택이나 제품 구현 선택은 하지 않았다. 서로 다른 문서상 적합 후보와 조건부 참고를 후속 설계자가 비교·폐기·재조합할 수 있도록 보존한다.
