# Apache A 계열 — 독립 표집 뒤 제안·인지·시행을 분리한 감사

## 사용 범위와 실제 분모

이 계열의 측정 단위는 **Flink 팀의 구현 선택 8건**이다. FLIP 원문 9개를 연속 검토했고 FLIP32를 FLIP28의 후속 계획으로 묶어 A12 하나로 남겼다. 다음 적격 문서 FLIP33이 A16이다. `sampling.csv`의 9행은 채택8·중복탈락1이며, 표집 대상 원문 접근 불가로 탈락한 행은 0이다. 검색 결과에 등장한 별도 FLIP·JIRA는 이 분모에 넣지 않았다.

`sources.json`에는 83행이 있으며, 그중 원문 수 하한에 산입한 고유 문서·메일·공식 코드/출시 문서는 **59개(당시 결정/제안17, 별도 후속32, 공식 버전10)**이다. 이것은 **59개의 독립 사건이 아니다**. 같은 FLIP의 초안과 개정판은 하나의 저작으로 두고 후속판은 재산입하지 않았다. 서로 다른 메일·제안·릴리스도 같은 사건의 자료이면 `ApacheFlink/Axx` 계보로 표시했다. 1.9 발표문은 A12·A13·A14에 연결되지만 자료 수에는 한 번만 더한다. 이 계열만으로 타 분야나 별도 B 표본을 대체하지 않는다.

엄격한 **미인지→발견→그 발견 때문에 선택 변경→실행** 연결은 **0/8**이다. 공개 제안과 이후 제한된 범위의 시행을 연결한 것은8/8이지만, 최초 공개 코드 commit은8건 모두 특정하지 못했다. 이는 실행 부재가 아니라 **최초 공개일 미확인**이다. 공식 표결 결과까지 연 날짜는 A11(2020-02-07)과 A16(2020-09-28)이다. 다른 행의 초안 상태, 지지 답글, JIRA 해결일은 표결일로 승격하지 않는다.

## 표집과 날짜 감사

원 모집틀은 Apache Flink Confluence FLIP 목록에서 `created`가2018-01-01..2024-12-31인 page를 UTC 생성시각 오름차순·동률이면 FLIP번호로 정렬한 metadata다. 프로젝트 상한8, 최초 적격부터 연속 선택, 순수 문서/명명/거버넌스 제외를 본문 결과 읽기 전에 고정했다. 동결 기준은 `00c2a14633e7503880f4aceb7c4909845298b3d7`의 SCOPE다. query·확인UTC·응답 hash·첫30개 metadata는 `frame_inventory.json`에 있다. 30개 모두를 내용 심사했다고 세지 않는다.

선택에 결과·revert·미인지 표현을 사용하지 않았다. 다만 이 표집틀은 **page 등록일 기준 원장**이며, 실제 최초 메일 날짜순의 전체 Apache 모집단은 아니다. 메일을 열자 날짜가 더 앞선 경우가 나왔다. 동결 뒤 사례를 결과에 맞게 재정렬·교체하지 않고 이 차이를 보존했다. 기존 페이지에서 관측창 중 다시 논의된 선택은 이 프레임 밖일 수 있다.

| 사건 | 원장 등록일 | 직접 연 앞선 제안/필요 기록 | 정밀도·주의 |
|---|---|---|---|
| A09 FLIP25 | 2018-05-02 | 2018-02-06 원 제안 AP-M25-ORIG | 날짜/시각; 이미 더 오래된 feature issue와 prototype을 언급. 사적 최초 고민일 아님 |
| A10 FLIP26 | 2018-05-09 | 2018-05-07 FLINK9312; 05-10 첫 FLIP 메일 | JIRA 날짜의 표시 TZ 미확인. 문서와 별도 내부 인증 하위 범위를 구분 |
| A11 FLIP27 | 2018-10-31 | 같은 날16:22 UTC 메일 | 오랫동안 논의했다고만 말함. 그 기간의 시작은 미확인 |
| A12 FLIP28→32 | 2018-11-29 / 2019-01-28 | 2018-06-13 Scala-free 제안; 2019-01-24 Blink 통합 계획 | 두 문서가 같은 Table 모듈 선택을 잇는다는 명시 근거 있음 |
| A13 FLIP29 | 2018-12-03 | 2018-11-01 Table API 사용성 제안 | 원문이 구체 SQL/DataStream 대안을 비교. 실제 첫 사용자 요청일 미확인 |
| A14 FLIP30 | 2019-01-07 | 2018-10-09 상위 Hive 통합 제안; 구체 Catalog v2는2019-01-08 | 상위 필요와 구체 API 선택 날짜를 합치지 않음 |
| A15 FLIP31 | 2019-01-18 | 2018-08-27 external shuffle 제안 | v1의 Accepted 표기를 최초 공식 결정으로 취급하지 않음 |
| A16 FLIP33 | 2019-02-11 | 같은 날12:17 UTC 메일 | 계측 구현을 바꾸는 선택이므로 단순 이름 변경으로 배제하지 않음 |

초기판 감사에서는 FLIP25 v1–2의 빈 본문, v3–5의 잔존 템플릿, FLIP28 v1과 FLIP32 v1의 템플릿을 분리했다. FLIP32는 v1부터 Accepted라고 적혀 있으나 substantive v2 및 실제 메일을 기준으로 읽었다. FLIP30 v2에도 일부 템플릿 문장이 남아 있어 해당 문장을 결정 근거로 쓰지 않았다. 고정판 링크는 실제 열람한 Confluence REST `status=historical&version=` 주소이며, 확인한 절을 원장에 적었다.

AF-RES-017 `34c14d6d2ad8802cf68ff9d9db4a3f810b4e057a`의 CASES ID·대상과 대조했으며 이8개의 Flink 선택은 기존40행에 재산입된 것이 아니다. 앞선40건이나 별도 기원7경로를 다시 범용 검색하지 않았다.

## 사례별 판단

| 사건 | 앞선 선택 → 확인한 이후 선택 | 인지와 반대 근거 | 최소 미확인 입력 |
|---|---|---|---|
| A09 | timer 기반 자체 TTL → timestamp를 붙인 자체 TTL 유지, 가시성/정리 분리; 1.6 배포, 1.8 정리 확장 | [초안](https://cwiki.apache.org/confluence/rest/api/content/80452561?expand=body.storage,history,version&status=historical&version=6)은 RocksDB TTL을 이미 거절. [Fabian](https://lists.apache.org/thread/0pdkltmm3noygb8lprxxk2gpp7tt049y)이 몰랐다고 인정한 것은 compliance **요구**다. [Bowen](https://lists.apache.org/thread/1tvkjsg2dr4f6kzoyozr761c8w9yqo6n)은 추가 개발을 지지 | 2월 최초 설계/원 prototype, RocksDB TTL 최초 소개에 대한 작성자 반응 |
| A10 | 기존 TLS → 내부 상호 인증 및 설정 분리 부분 구현 | [원 설계](https://cwiki.apache.org/confluence/rest/api/content/80453255?expand=body.storage,history,version&status=historical&version=1)는 YARN Servlet filter와 proxy를 이미 비교. [후속](https://lists.apache.org/thread/mz11d9svx4klwogncnqtrbbwzmc0oxf4)은 Akka classic 제약을 이유로 제한된 truststore를 유지 | PR6326 merge/diff와 전체 endpoint별 인수 기록 |
| A11 | 구 SourceFunction → 새 Enumerator/Reader API와 구 API 병존 | [초안](https://cwiki.apache.org/confluence/rest/api/content/95653746?expand=body.storage,history,version&status=historical&version=1)부터 기존 API를 알고 구조적 제약을 설명. [1.11 발표](https://flink.apache.org/2020/07/06/apache-flink-1.11.0-release-announcement/)는 새 API beta와 기존 connector 미이식을 함께 명시 | 원 prototype의 첫 공개 commit, 커넥터별 이식 기록 |
| A12 | Scala 유지 → 부분 Java 이식 → Blink 수용을 위한 API/planner 분리 | [원 메일](https://lists.apache.org/thread/b8dvfrqr9xkr282f7mc9hkk04x7c2r9z)은 Scala 장점을 알고 유지했다고 설명. [JIRA](https://issues.apache.org/jira/browse/FLINK-11063)는 Alibaba 기여 때문에 API 우선으로 범위를 줄였다고 명시 | 기여 이전/이후 동등 범위 작업 계획·인시·diff |
| A13 | SQL/UDF 또는 DataStream 우회 → Table 다중 출력 연산 추가 | [원 메일](https://lists.apache.org/thread/h1rhsoztg5onhgc07c7v4ppx06z2rzqf)은 기존 방식으로 가능한 것과 잃는 optimizer/통합 이점을 이미 비교 | 실제 사용 팀의 전후 코드와 시간 기록. 100열은 예시이지 비용 관측값 아님 |
| A14 | 기존 조회형 catalog → 읽기/쓰기·영속화 통합 API | [원 Hive 제안](https://lists.apache.org/thread/r8xolxo9x0sxgl6obnt26d74pw3b60xz)은 Spark SQL형 통합과 Hive 엔진 교체를 미리 비교. [진행 보고](https://lists.apache.org/thread/r9s7vgjoo9d1h7ls7wkwn0jyof7kh8sn)는 내부 검증 후 공개 기여의 순서를 밝힘 | 최초 공용 catalog PR와 내부 demo 판, Hive 버전별 matrix |
| A15 | TaskManager 내부 Netty shuffle → 구성요소를 재사용하는 pluggable 구조 | [후속 답글](https://lists.apache.org/thread/y28w05mogwh2s55kp2199djh7s7vqhtk)은 재사용할 기존 writer/reader를 구체화. [2021 공식 글](https://flink.apache.org/2021/01/11/exploring-fine-grained-recovery-of-bounded-data-sets-on-flink/)은 환경별 external service가 여전히 필요함을 명시 | 최초1.9 merge와 외부 서비스 실제 배포, worklog 범위 |
| A16 | histogram 포함 계측 → gauge 중심·기존 I/O 재사용, 일부 커넥터 적용 | [Chesnay](https://lists.apache.org/thread/9tkc7b5j41dwbbs3do0vkw43wv4f8bg8)의 계산 비용 반대와 [Becket](https://lists.apache.org/thread/pwzyp9bc46wbotcrnbxyrv84yo5c3nc6)의 선택적 histogram 옹호를 함께 보존. [2020 답글](https://lists.apache.org/thread/brcx7tgn9xphgyqc29cxlsx9yyb0ymx4)은 동료가 제안한 watermark 지표가 이미 추가되어 있었다고 밝힘 | 제안자 benchmark 원본과 실제 지표 도입 diff/운영 CPU 기록 |

### 인지 플래그의 뜻

`awareness_prior_known`는 **대상 대안을 제안·재결정 시 이미 알고 비교한 직접 기록**을 뜻한다. A10–A16은 true, A09의 원2월 설계 시점에서 RocksDB 내장 TTL 인지는 미확인이다. A09도5월 초에는 확실히 알고 거절했다. 따라서 넓은 `unknown_first_cognition=true`8건을 그대로 가능한 양성8건으로 합산하면 안 된다. 8건 모두 최초 인지일은 없지만, 그중7건은 표적 대안을 알고 제안했고 A09만 최초 제안 당시 모를 가능성을 배제하지 못한다. 이것도 **발견이 선택을 바꾼 인과가 있다는 뜻은 아니다**.

외부 대안 미인지 명시0건, 원 제안 뒤 실제 첫 소개임을 작성자가 확인한 사례0건이다. A09의 SQL/Table retention 소개는 대화에서 실제 존재하지만, 수신자가 처음 알았다는 진술은 없다. 같은 프로젝트의 기존 기능 소개이며 외부 라이브러리 채택으로 바뀌지도 않았다. `strict_discovery_change=false`8건과 `connected_chain=false`8건을 유지한다. 전체 A24의 범위 계산은 이 플래그를 사용하되 B와 합치지 않아야 한다.

## Q별 보강과 반증

**Q1–Q2.** 결과와 독립적인 원장으로8건을 골랐지만 원장 생성일은 실제 필요·제안일을 대리한다. 날짜의 정확도가 높아도 심리적 최초 인지나 공식 결정일이 되지는 않는다. FLIP27은 [2020-02-07 가결](https://lists.apache.org/thread/ytmfqxp43t0z0o2hhjot1wtz93dos4qy) 뒤에도 [02-25 누락 인터페이스 보완](https://lists.apache.org/thread/qv30kl6xtwmtwbjsgrmr7jxbswo3l55o)이 있었다. accepted 상태를 설계 불변·실행 완료로 읽는 결론은 반증된다.

**Q3.** 각 행의 적어도 한 기존 선택을 당시 공식 tag에서 열었다. 원 메일 날짜를 확인한 뒤 후발인1.7 Table/Catalog 문서를1.4 또는1.6으로 교체했다. RocksDB5.8.8의 `db_ttl.h`는 compaction만으로 지우고 Get이 만료 값을 반환할 수 있음을 명시한다. Hadoop2.7.4의 AmIpFilter는 Servlet 계약이다. 이미 있던 기능이라는 사실만으로 Flink의 정밀 가시성·Netty 호환 조건을 만족하지 않는다. A09의1.8 연속 정리와 A15의 완성 external service는 당시 곧바로 사용할 수 있는 해법으로 소급하지 않는다. 대안의 저장소 최초 공개일, 공개 tag 생성일, 팀 이용 가능일은 서로 다르며 미확인 부분을 남겼다.

**Q4–Q5.** 이 계열에서 변화는 실제로 있지만 외부 해법을 늦게 안 결과라는 연결은 없다. A09에서는 요구 재정의, A12에서는 공급 가능한 Alibaba 코드 기여, A16에서는 성능·지표 의미가 더 직접적인 이유다. 메일 작성자의 역할도 분리했다. 제안자가 같은 기능을 이미 넣어 놓았는데 리뷰어가 다시 제안한 A16은 ‘리뷰 댓글 날짜=결정자의 최초 인지일’이라는 추론을 반박한다. A15 상위 이슈의 Fixed와 하위 [FLINK11393 Won’t Fix](https://issues.apache.org/jira/browse/FLINK-11393)는 같은 작업의 전면 성공/실패로 압축하면 안 된다. 시험 후 철회는0건으로 남기며 이 하위 이슈를 억지 철회 양성으로 세지 않는다.

**Q6.** [FLINK10653](https://issues.apache.org/jira/browse/FLINK-10653)의 Time Tracking에 표시된 **13h 50m**만 정량 작업 기록으로 남겼다. 작업자·입력일·포함 범위가 보이지 않아 ‘결정자가 보고한 전체 투입’ 조건은 충족하지 않는다. 각 사례의 최초 제안부터 release까지 경과를 인시로 변환하지 않았다. A13의100열/100UDF 예시도 실제 투입이 아니다. A16의 benchmark는 질적 느림 보고뿐이다. A12·A15는 기존 코드가 실제로 재사용되거나 유지된 범위를 확인했으나 폐기된 코드량·비용은 없다. 모든8건에 필요한 당시 기록 하나를 `minimum_next_record`에 적었다.

**Q7.** 이8건에서는 엄격한 타 분야 구조 전이를 확인하지 못했다. A09의 Cassandra compaction filter 언급은 같은 데이터 저장 분야이고, 원 구현과 받은 팀 규칙의 두 대응을 직접 대조하지 않았다. A13의 GroupReduce/relational 연산 대응도 같은 분야다. A15의 추상화는 실제 구조적 변화지만 타 분야 유래나 최초 인지일을 증명하지 않는다. 이 부재를 다른 분야의 효과가 없다는 결론으로 일반화하지 않는다. 별도 특허·공학 자료 검토는 루트 보고서에서 합쳐야 한다.

**Q8.** 실제로 제공할 수 있었던 링크와 한계는 다음과 같다. 이를 제공했으면 바뀌었다는 직접 진술은 없다.

| 가능한 개입일·사례 | 그때 제공할 수 있던 링크·부분 | 조건·도입비용 | 기록이 허용하는 판단 |
|---|---|---|---|
| 2018-02-06 A09 | [RocksDB5.8.8 db_ttl.h](https://raw.githubusercontent.com/facebook/rocksdb/v5.8.8/include/rocksdb/utilities/db_ttl.h)17–44행 | creation/compaction 의미와 정밀 가시성 불일치. 그대로 채택해도 wrapper·검증이 필요 | 중복 구현을 막을 링크라기보다 후보 배제 이유를 일찍 명료화할 수 있었을 가능성. 실제 절감 미확인 |
| 2018-06-13 A12 | [Flink1.4 Table API](https://raw.githubusercontent.com/apache/flink/release-1.4.0/docs/dev/table/tableApi.md)Overview | Java API와 Scala 구현 의존성은 다름. 전체 Java 이식 비용 미확인 | 언어 옵션은 이미 알고 있었다. 뒤의 Blink 기여를 앞당기는 링크라고 볼 수 없음 |
| 2018-11-01 A13 | [Flink1.6 Table API](https://raw.githubusercontent.com/apache/flink/release-1.6.0/docs/dev/table/tableApi.md)Operators | 기존 표현은 가능하지만 다중 출력 사용성이 나쁨 | 기존 연산을 알았어도 새 연산을 추가할 직접 이유가 있었음 |
| 2019-01-08 A14 | [Flink1.6 ExternalCatalog](https://raw.githubusercontent.com/apache/flink/release-1.6.0/flink-libraries/flink-table/src/main/scala/org/apache/flink/table/catalog/ExternalCatalog.scala)trait | 읽기 계약을 공통 write·persistence로 확대해야 함. adapter/호환 검증비 미확인 | A13과 비슷한 Table 생태계이나 기존 계약을 대체할 이유가 다름. 하나의 링크가 양쪽 선택을 똑같이 바꾼다고 보기 어려움 |
| 2019-02-11 A16 | [Flink1.7 metrics](https://raw.githubusercontent.com/apache/flink/release-1.7.0/docs/monitoring/metrics.md)Histogram201–256행 | wrapper 존재와 낮은 연산비는 다름. 실제 workload benchmark 필요 | 후보 제공보다 비용·의미 비교가 선택을 바꾸는 정보였다는 해석. 원 benchmark 없으므로 인과효과 크기는 미확인 |

## 재현·남은 검사

`fetch_confluence.py PAGE_ID --version N`은 공개 고정판의 본문/metadata를 읽는다. `fetch_api.py NAME email '{"id":"MESSAGE_PERMALINK"}'` 또는 `thread`/`stats`는 Apache가 문서화한 공개 읽기 API를 호출한다. 상세 입력은 각 mail source의 `api_request`와 `search-log.json`에 보존했다. 이 도구들은 읽기 전용이며 로그인하지 않는다. 전체 기사/메일을 그대로 저장한 임시 cache는 인계 전에 삭제했다. 원문 전체를 다시 생성하려면 이 입력을 실행하되 원문 본문을 산출물에 중복 복제하지 않는다.

일부 lists.apache.org의 웹 추출 오류는 같은 서비스의 공식 API로 해결했다. 미해결 enrichment 접근은 PR6326의 웹 열람 오류, GitHub tree API403, 추정 shuffle 파일 경로404이다. 검색 결과나 차단 페이지는 원문 개수에 넣지 않았다. 잘못된 날짜 문법으로 얻은0건 검색도 수정 검색과 함께 원장에 남겼으며 미발견 근거로 사용하지 않는다. 검색 범위는2018–2024이고, thread 전체 메타데이터와 실제 읽은 답글 범위는 구분되어 있다.

다음 첫 행동은 **원 결과표와 이8행의 역할·날짜·분모를 합치고, 부족한 최초 구현/인지 연결을 요구 조건의 미충족으로 그대로 반영하는 것**이다. 더 보강한다면 A09의2018년 원 Google Doc version history와 prototype commit을 우선 열어 RocksDB TTL의 최초 인지와 실제 버린 작업을 확인한다. A15의 worklog를 그다음으로 열어13h50m의 귀속을 확정한다.
