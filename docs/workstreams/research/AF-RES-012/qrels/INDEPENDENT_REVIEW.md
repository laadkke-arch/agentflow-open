# AF-RES-012 내부 별도 검토

검색 실행과 앞선 판정의 결과를 보지 않고 합의한 15개 질의에 대해 자료집 156개를 모두 검토했다. 같은 질의·항목에 판정 1개를 부여했다. 고정 입력은 다음과 같다.

- 자료집 SHA-256 `0e4b6454ed2b479b14ab286f06100aa77c252ba40348abdf4414420ee945c8ac`
- 질의 파일 SHA-256 `dc1c19adf87ec618da661f13f98bbee17c94d909267de122b2707f15cf619834`

한국어와 영어를 함께 읽었다. 질의가 지정한 완성품이나 일부 기능의 핵심 조건을 확인할 수 있으면 2, 문서로 뒷받침되는 부분 기능·조건부 적용·전이 원리는 1로 잡았다. 명시된 설정을 구현할 수 있는 근거가 있으면 기본값의 실패와 구분했다. 이름이나 범주가 가깝고 필수 조건을 어기는 방식은 N이다. 근거가 제목과 범주에 그치거나 기전이 맞지 않으면 0이다. TSV는 2·1·N 전체와 판단 경계에 유용한 0 일부를 담았다. 나머지 이 검토 범위의 쌍에는 2·1·N을 부여하지 않았다.

K05.w에는 2가 없다. 신규 변경을 영구 격리된 원격 단말로 즉시 보낼 수 없으며, 질의가 허용한 로컬 편집·저장 참고는 1이다. P1.w에서 전체 요구를 충족한다고 판정하려면 입력마다 영속 결과를 중복 없이 공개하면서 실패 결과를 다시 처리하는 근거가 필요하다. K06.w의 한국어 결과는 해당 시스템이 만들어야 할 문장에 대한 요건이다. 운영팀에 보여 줄 새 설명을 한국어로 제공하는지까지 확인된 검색·기록 부품은 없었다.

## 부분 질의의 해석

- P01.1은 정상적인 저장 완료 후 탭 재진입에서 **본문**이 남는지를 묻는다. 독립 문장에는 앱 shell 캐시가 명시되어 있지 않다. 2는 본문 저장층에 주었고 앱이 오프라인에서 열릴 수 있어야 한다. 일반 IndexedDB 도구는 본문 로딩의 제품 설정이 남아 1이다.
- P02.2는 재연결까지 1시간을 명시한다. 중단 횟수·전체 경과시간의 상한은 독립 문장에 없으므로 일반적인 유한 중단과 그 기간을 넘는 설정의 복구 메커니즘에 2를 주었다. 무기한 보존으로 읽으면 유한 TTL의 SQS는 해당하지 않는다. P02.w에서는 별도로 명시된 30회와 24시간 미만 및 중복 처리 허용을 적용했다. 기본 RabbitMQ 재전달 제한 20회로는 이 사례를 충족할 수 없다. [RabbitMQ 4.1 quorum queue 정책](https://www.rabbitmq.com/docs/4.1/quorum-queues#configuring-the-limit)
- P03.2는 느린 sink가 회복될 때까지 생산자가 기다리면서 무제한 대기를 만들지 않는 한 조건으로 판정했다. 언어와 8/4 상한은 포함하지 않았다. permit을 task 생성 **전에** 획득하는 Semaphore는 이 조건을 충족한다. P03.w에서 실제 대기 큐를 요구한다고 해석하여 Semaphore 단독은 1이다. 대기 0개도 허용하는 설계라면 조기 획득과 저장 후 반납 방식은 2로 다시 검토할 수 있다.
- P04.w의 두 역할은 각각 독립적으로 평가했다. 포함 증명은 선택한 판의 신뢰 root와 결정적 leaf 표현을 전제로 확인했다. 로컬 폴더 복원과 암호화는 완성 백업 도구에만 적용했다.

## 사실 대조

자료집의 D-a·D-b·D-c와 대표 URL, 원장 참조를 썼다. 정책 경계는 AF-RES-001의 소프트웨어 원장 C01–C10, 아키텍처 A01–A09, 명확화 B03–B05와 AF-RES-004의 S01–S19, S24–S27에 대조했다. 앞선 작업의 후보 판정, EXPECTED, 이번 실험 qrels, 순위, 결과 파일은 열지 않았다. [AF-RES-001 고정 증거 경로](https://github.com/laadkke-arch/agentflow-open/tree/4d6208c08f6f2657865ba000d6768f6537e832b6/docs/workstreams/research/AF-RES-001/evidence), [AF-RES-004 고정 원장](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/sources.json)

등록 자료의 요약이 모호할 때 같은 버전 주소의 메타데이터 본문을 확인했다. 이름이 비슷한 OTLP Python 패키지는 pip 하위 패키지 모음이었다. pymerkle 설명서 예제는 지정 leaf의 포함 증명을 만들고 state root·위치·크기로 검증한다. aiojobs는 await spawn을 보여 주며 Janus는 asyncio 대기열 설계를 따른다. borgmatic의 Borg 기반 암호화, Duplicity의 암호화 증분 볼륨과 로컬 대상, rdiff-backup의 로컬 역증분 저장은 설명에 있었고 세 도구 모두 질문의 전체 조건까지 원문으로 확인한 것은 아니다. [OTLP](https://pypi.org/pypi/opentelemetry-exporter-otlp/1.45.2/json), [pymerkle](https://pypi.org/pypi/pymerkle/7.0.0/json), [aiojobs](https://pypi.org/pypi/aiojobs/1.4.0/json), [Janus](https://pypi.org/pypi/janus/2.1.1/json), [borgmatic](https://pypi.org/pypi/borgmatic/2.2.0/json), [Duplicity](https://pypi.org/pypi/duplicity/3.2.2/json), [rdiff-backup](https://pypi.org/pypi/rdiff-backup/2.2.7/json)

## 검토 범위

| 질의 | 2 | 1 | N | 명시 0 |
|---|---:|---:|---:|---:|
| K01.w | 1 | 8 | 7 | 1 |
| K02.w | 0 | 10 | 3 | 3 |
| K03.w | 0 | 8 | 0 | 3 |
| K04.w | 1 | 17 | 2 | 1 |
| K05.w | 0 | 13 | 9 | 1 |
| K06.w | 0 | 12 | 1 | 3 |
| P1.w | 0 | 33 | 5 | 2 |
| P2.w | 1 | 20 | 2 | 1 |
| P01.w | 2 | 14 | 2 | 1 |
| P02.w | 3 | 12 | 5 | 2 |
| P03.w | 1 | 5 | 6 | 2 |
| P04.w | 5 | 6 | 1 | 1 |
| P01.1 | 2 | 6 | 3 | 1 |
| P02.2 | 3 | 8 | 5 | 0 |
| P03.2 | 3 | 5 | 4 | 1 |
| 합계 | 22 | 177 | 55 | 23 |

명시 판정 277건 중 112건은 레지스트리에서 추가한 항목이다. 도구 실행이나 배포 상태는 검토 범위 밖이다. 레지스트리 설명이 짧아 0으로 둔 항목은 새 근거가 있으면 바뀔 수 있다.
