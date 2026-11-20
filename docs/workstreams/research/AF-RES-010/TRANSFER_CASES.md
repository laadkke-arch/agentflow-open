# Q4 — 원저자가 밝힌 소프트웨어 전이와 성립 경계

## 결론과 집계

다른 분야의 원리를 소프트웨어로 옮긴 **10개 사례를 9개 원저자 저작물**에서 확인했다. 전달된 것은 분야 이름보다 관계였다. 접촉에 의한 전파, 국소 관찰의 축적, 소모 자원의 차단, 손상 영역의 분리, 지휘와 실행의 분리, 보존식, 피드백, 탐색의 확률적 제어가 구체 설계로 바뀌었다. 효과는 목표·관측 가능성·시간 척도·사람의 행동에 종속된다. 아래의 `mapped`는 이 관계를 설명할 수 있다는 뜻이며 P1/P2 전체 요구 충족을 뜻하지 않는다.

| 사례 | 출발 분야 → 소프트웨어의 특정 부분 | 원저자 확인 | 근거의 성격 | T |
| --- | --- | --- | --- | --- |
| TC01 | 역학 → 복제 데이터의 anti-entropy / rumor 전파 | Demers 외, T01 | PODC 논문, 알고리즘·시뮬레이션 | mapped |
| TC02 | 면역계 자기/비자기 → Unix 프로세스의 이상 탐지 | Forrest 외, T02 | IEEE S&P 논문, 초기 trace 실험 | mapped |
| TC03 | 개미의 간접 협력 → 패킷 경로의 확률적 갱신 | Di Caro·Dorigo, T03 | JAIR 논문, 네트워크 시뮬레이션 | mapped |
| TC04 | 전기 차단기 → 실패하는 의존 서비스의 호출 차단 | Nygard, T04 §5.2 | 원저자 설계서 | mapped |
| TC05 | 선박 격벽 → 자원 고갈의 전파 영역 제한 | Nygard, T04 §5.3 | TC04와 **동일 저작물** | mapped |
| TC06 | 비상 대응 ICS → 서비스 장애의 지휘·실행·소통 | Stribblehill, T05; 실무 사례 T11 | 당사자 운영 문서 | mapped |
| TC07 | 경제학 가격·수요와 제어 이론 → 네트워크 전송률 | Kelly·Maulloo·Tan, T06 | JORS 논문, 증명·수치 예제 | mapped |
| TC08 | 통계역학의 annealing → 조합 최적화 탐색 | Kirkpatrick 외, T07 | Science 논문, 알고리즘·계산 예제 | mapped |
| TC09 | 복식부기 → Mettle의 WODE 이벤트 원장 | 구현 조직 Mettle, T08 | 직접 구현을 설명한 기술 글 | mapped |
| TC10 | 제조 Andon → 개발팀의 도움 요청·장애 집결 | 구현자 Ayers·Cohen, T09 | 공개 발표 본문, 팀 관측 | mapped |

T10은 AWS의 차단기 반증 자료이며 새 전이 사례로 세지 않는다. T11은 TC06의 별도 사례 자료이다. 총 본문 출처는 **11개**, 이 중 동료심사 논문은 **5개**다. 두 책의 같은 사례나 같은 논문의 미러로 수를 늘리지 않았다. 생물, 의학·역학, 제조, 금융·회계가 포함되고 전기·해양 안전, 비상 대응, 물리도 포함된다. 항공 체크리스트의 소프트웨어 전이는 이번 표에서 확정하지 않는다.

기존 Reflow·SQLite·TreeDB·NASA 종이접기 및 AF-RES-004의 R11/R12/R17은 이 집계에 없다. TC10의 Andon은 R12의 Toyota JIT 수요·재고 관계와 다른 **이상 발견 → 즉시 도움 요청 → 공동 대응** 관계이다.

## 판정 방식

AF-RES-004 `2b798c7d2b7355b649691c18de196104ceabb0f0`의 PROTOCOL T축을 그대로 사용했다. 각 행의 단위는 **출처가 기술한 구현 × 좁은 참고 용도 × 명시 조건**이다. `mapping / bridge / excluded / counterexample / minimum_next_check`를 아래에 기록한다.

모든 사례의 공통 상태는 `T=mapped`, `label=CONDITIONAL_TRANSFER`, `H_assessment_scope=reference_design`, `runtime_observation=not_performed`이다. 원저자 구현·실험 보고를 읽은 것은 D1이다. 본 작업이 직접 구현한 D3 또는 P1/P2에 적용한 D4로 올리지 않는다. `H:`로 표시한 연결 제안·시험 입력은 연구자의 추론이다. 역사적 전이가 확인되었다는 주장과 그 원리가 현재 문제에 효과가 있다는 주장을 구별한다.

## TC01 — 전염 과정에서 복제 갱신으로

**확인(D1).** Demers 외는 역학의 감염·접촉 모형을 갱신 전파에 명시적으로 대응시킨다. 원 분야의 감염 억제와 달리 목표는 빠르고 넓은 전파이다. 실제 CIN 토폴로지에서 표 4와 표 5는 각각 250회 단일 갱신 시뮬레이션을 보고한다. anti-entropy와 유한 rumor 전파를 같은 보장으로 취급하지 않는다. [T01]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 접촉한 감염 개체가 상태를 전달 → 선택한 peer 사이 갱신 전달. 전파를 중지한 개체 → 더 이상 rumor를 보내지 않는 복제본. |
| bridge | H: peer 선택의 연결성, 버전 식별, 재접속 시 재비교, 삭제 이력의 수명을 명시해야 한다. |
| excluded | 수렴 속도가 사용자의 서로 다른 수정 의도 보존을 보장하지 않는다. P2의 충돌 표시·내보내기까지 해결하지 않는다. |
| counterexample | 저자는 dormant death certificate를 항체에 비유하지만 전파 시간이 보존 임계값을 넘으면 재활성화가 부하를 키워 파국적 피드백을 만들 수 있다고 분석한다. [T01 §2.1] |
| minimum_next_check | H: 삭제·재생성 뒤 오래 분리된 복제본을 복귀시켜 정당한 재생성과 낡은 부활을 구별하는지 확인한다. |

## TC02 — 면역계의 자기 구별에서 이상 탐지로

**확인(D1).** Forrest 외의 표현은 정상 syscall의 짧은 순서가 자기(self)를 나타내고 벗어난 순서가 이상 신호가 된다는 것이다. 112개 인공 정상 메일의 150만 회 이상 syscall로 정상 DB를 구성했다. 악성 여부를 완전 판정하는 면역 시스템을 구현했다고 주장하지 않는다. [T02]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 자기 특성과 관측 대상을 비교 → 프로세스별 정상 순서 DB와 실행 trace 비교. |
| bridge | H: 관측 단위, 정상 훈련의 범위, 소프트웨어 갱신 시 재학습, 경보와 자동 차단의 분리를 지정한다. |
| excluded | 정상과 비정상 구분을 선의와 악의 구분으로 바꿀 수 없다. 이 탐지기는 권한·암호 검증의 대체물이 아니다. |
| counterexample | 비악성 forwarding loop도 2.3% 이상 순서로 나타났으며 일부 공격 수치보다 높다. 정상 syscall 순서를 유지하는 race 공격은 놓칠 것이라고 저자들이 명시한다. [T02 §4.3/5] |
| minimum_next_check | H: 합법적 버전 갱신·희귀 작업과 순서가 정상인 공격을 함께 입력해 오탐·미탐 및 운영자 처리량을 측정한다. |

## TC03 — 개미의 stigmergy에서 AntNet으로

**확인(D1).** Di Caro·Dorigo는 개미의 환경 매개 간접 소통을 노드별 라우팅 확률·이동 시간 통계로 바꾼다. forward ant가 경로를 관찰하고 backward ant가 정보를 갱신한다. 실험은 3개 토폴로지, 조건별 10회·가상 1,000초로 수행했다. [T03 §4/6/7]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 개체의 탐색 결과가 환경에 남아 다른 개체 선택에 영향 → 탐색 패킷의 통계가 확률적 다음-hop 선택에 영향. |
| bridge | H: 관측용 agent 트래픽, 지연 추정의 수명, loop 처리와 데이터 트래픽 선택 정책을 구별한다. 실제 화학물질은 필요 없다. |
| excluded | 실험의 노드·링크 고장 확률은 0이었다. 생물 집단의 강건성이라는 말만으로 장애·공격 내성을 확대할 수 없다. |
| counterexample | NSFNET의 UP 부하에서는 BF/SPF throughput이 AntNet보다 약 10% 높았다. AntNet의 지연 성능과 지표별 trade-off를 숨기면 우위 주장이 달라진다. [T03 §7.2] |
| minimum_next_check | H: 탐색 비용을 포함하고 링크 단절·급변 부하를 주어 throughput, tail latency, 수렴 중 손실을 동시에 비교한다. |

## TC04 — 전기 차단기에서 호출 차단으로

**확인(D1).** Nygard는 전기 차단기의 보호 관계를 실패하는 호출로 인한 자원 소모에 적용하고 closed/open/half-open의 복귀 과정을 기술한다. [T04 §5.2]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 위험한 전류의 지속을 끊음 → 실패 의존성으로 새 호출을 보내지 않아 대기 자원 고갈을 제한. |
| bridge | H: 실패 종류·시간 창·임계값·probe·관측과 운영자 개입을 정의하고, 차단 시 사용자가 받는 결과를 정한다. |
| excluded | 호출 억제는 이미 발생한 외부 효과의 중복 제거가 아니다. P1의 같은 입력 중복 공개 방지로 직접 치환할 수 없다. |
| counterexample | Brooker는 상태 모드가 시험을 어렵게 하고 복귀를 늦출 수 있다고 보고하며 retry token budget을 제시한다. 이것은 모든 breaker의 실패라는 판정은 아니다. [T10] |
| minimum_next_check | H: 의존성이 부분 회복한 상태에서 open 유지·동시 probe·재차단이 가용성과 복귀 시간에 미치는 영향을 시험한다. |

## TC05 — 선박 격벽에서 자원 격리로

**확인(D1).** Nygard는 선박의 수밀 구획을 서버·CPU·thread 자원 분할에 대응한다. 자원 분리에는 예비 용량의 비용이 있으며 공유 DB 같은 연결이 남을 수 있다. [T04 §5.3]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 한 구획의 침수가 나머지 구획으로 번지지 않음 → 한 작업군의 자원 소모가 다른 작업군의 최소 용량을 소진하지 못함. |
| bridge | H: 실제 소모되는 pool·메모리·저장 공간별 경계를 정의하고, 공유 의존성까지 고장 영역을 그린다. |
| excluded | 논리 모듈 분할만으로 자원 격리는 성립하지 않는다. P1의 성공 결과 내구성과 재시도 중복은 추가 요구이다. |
| counterexample | H: 분리된 worker들이 같은 디스크를 채우거나 같은 DB lock을 기다리면 결과 저장 전체가 막힌다. 이는 구현에서 확인할 구체 반증 입력이다. |
| minimum_next_check | H: 한 문서에 무한 대기·메모리 고갈·저장 공간 소진을 각각 주고 다른 문서의 처리·공개가 계속되는지 확인한다. |

## TC06 — 비상 현장 지휘에서 서비스 장애 관리로

**확인(D1).** Google SRE 원저자는 시스템이 ICS에 기반한다고 명시한다. 지휘, 운영 실행, 소통 역할과 인수인계를 분리한다. 후속 Workbook은 Google 3건·PagerDuty 1건의 장애 사례를 제시한다. [T05; T11]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 여러 대응자의 자율 행동을 지휘·역할로 조정 → 변경 작업과 상황 파악·대외 소통을 분리하고 단일 변경 흐름을 유지. |
| bridge | H: incident 선언 기준, 변경 권한, 지휘권 인계의 수신 확인, 장애와 독립적인 상태 기록 채널이 필요하다. |
| excluded | 역할 이름이 장애 원인의 자동 진단이나 수정의 정당성을 보증하지 않는다. 역할 수를 조직 규모와 무관하게 복제할 필요도 없다. |
| counterexample | Workbook의 Google Home 사례는 선언·소통 지연과 잘못 추정한 원인에 대한 대응을 다룬다. 처음의 quota 완화가 문제 해결을 의미하지 않았다. [T11 사례 1] |
| minimum_next_check | H: 두 팀이 상반된 복구 변경을 제안하고 주 지휘자가 교대하는 훈련에서 명령 충돌·상태 유실을 관측한다. |

## TC07 — 경제학의 가격 조정에서 전송률 제어로

**확인(D1).** Kelly 외는 자원 shadow price와 사용자의 수요 반응을 네트워크 할당으로 수식화하고 primal/dual 제어를 분석한다. 이는 경제학 이름을 붙인 비유에 그치지 않는다. 가정한 함수·피드백 아래의 Lyapunov 증명과 지연을 포함한 수치 예제가 있다. [T06]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 희소 자원의 가격 상승이 수요를 줄임 → 혼잡 신호가 송신률을 낮추고 용량 여유가 송신률을 높임. |
| bridge | H: 효용의 정의, 표시된 가격과 실제 비용의 구별, 갱신 gain, 왕복 지연과 사용자 반응 속도를 지정한다. |
| excluded | 여기서 가격이 반드시 실제 결제를 뜻하지 않는다. 안정성이 사용자별 정당한 우선순위나 임의 업무 deadline을 보장하지 않는다. |
| counterexample | 100자원·1,000경로 예제에서 지연 최대 10, gain 0.005를 사용했고 gain이 약 0.011에 이르면 불안정해졌다. 지연 없는 안정성만 옮기는 것은 잘못이다. [T06 Examples] |
| minimum_next_check | H: 지연과 부하를 함께 바꾸며 발산·진동·기아를 확인하고, 목표 효용을 바꾸었을 때 잃는 공정성을 기록한다. |

## TC08 — 물리적 annealing에서 탐색 제어로

**확인(D1).** Kirkpatrick 외는 비용을 에너지, 해를 배열, 온도를 제어 변수로 대응하고 확률적으로 나쁜 이동도 받아들이는 알고리즘을 구성한다. 배선 예제의 한 링크 최대 wire 수는 x/y 173/143에서 105/96으로 바뀌었다. [T07]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 온도와 냉각 속도가 에너지 장벽 탈출을 조절 → 탐색의 악화 이동 허용 확률과 schedule을 조절. |
| bridge | H: 비용·상태·허용 이동·종료 기준을 정의한다. 교환할 수 없는 항목의 정체성과 지켜야 할 제약을 상태 표현에 넣는다. |
| excluded | 좋은 비용값이 의미상 올바른 병합이나 영속성을 보장하지 않는다. finite schedule의 해를 전역 최적해로 부를 수 없다. |
| counterexample | 저자도 동일 원자의 규칙적 결정과 달리 최적화 대상은 서로 교환 불가능한 요소를 포함하여 단순 유체 유추가 깨진다고 명시한다. [T07 통계역학 설명] |
| minimum_next_check | H: 비용이 낮지만 필수 조건을 어기는 해를 생성할 수 있는지 먼저 확인하고, feasible 해 안에서 여러 seed·schedule을 비교한다. |

## TC09 — 복식부기에서 불변 이벤트 원장으로

**확인(D1).** Mettle은 회계사의 수정·기록 방식에서 관계를 찾아 자체 원장에 적용했다고 밝힌다. WODE의 돈 이동 event는 source/destination account·amount·timestamp를 가지며 서로 균형을 이룬다. 지우거나 덮어쓰는 대신 새 기록으로 보정한다. [T08]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 거래의 양변과 수정 흔적을 유지 → 단일 균형 event와 변경 불가능한 이력으로 상태를 재구성. |
| bridge | H: 중복 식별자, atomic한 event 기록, 계정·통화 범위와 보정 event 권한을 별도로 정의한다. |
| excluded | 모든 event sourcing의 역사적 기원이 복식부기라는 주장은 하지 않는다. 이 출처가 확인하는 것은 해당 조직의 구현 전이이다. |
| counterexample | H: 동일한 균형 거래를 두 번 넣어도 합계 0은 유지된다. 따라서 보존식은 P1 멱등성이나 P2 서로 다른 의도의 충돌 해결을 대신하지 못한다. |
| minimum_next_check | H: 같은 command를 재전송하고 잘못된 계정에 균형 거래를 넣어, 균형 검증과 의미·중복 검증이 구별되는지 확인한다. |

## TC10 — 제조 Andon에서 개발·운영 도움 요청으로

**확인(D1).** Excella의 도입 당사자들이 제조의 Andon을 Slack 신호·조명·팀 집결로 바꾼 과정을 발표했다. 2018년 5월 시작 후 관측한 cycle time은 약 3일, 사용이 줄었을 때 11일, 재활성화 뒤 2일이었다. 통제군 없는 당사자의 상관 관측이다. [T09]

| T축 항목 | 실제로 옮기는 관계 / 경계 |
| --- | --- |
| mapping | 결함·막힘을 발견한 작업자가 즉시 도움을 요청하고 집단이 대응 → 개발 막힘·서비스 장애 때 필요한 동료를 신속히 모음. |
| bridge | H: 누가 언제 호출하는지, 응답 기대, 불필요한 인원의 업무 복귀, 불이익 없는 도움 요청 규칙을 함께 정의한다. |
| excluded | 이 사례는 workflow 전이이지 CI 실행기의 correctness 증명은 아니다. 기존 Toyota JIT의 pull 재고 제어와도 다르다. |
| counterexample | 당사자들은 약 두 달 후 호출이 끊겼고, 모른다는 인상을 주거나 동료를 방해할까 두려웠다고 설명한다. 최종 Q&A에서도 행동이 안정화되었다고 주장하지 않았다. [T09 10:46–12:02, 28:29] |
| minimum_next_check | H: 호출 횟수 보상보다 실제 도움 도달 시간·해결까지 지연·업무 중단 비용을 함께 기록하고, 신규 구성원에서도 사용 가능한지 확인한다. |

## 반증 검색과 결론 수정

검색 기록은 `evidence/transfer-searches.json`에 있다. `TQ01`은 차단기의 모드·복귀 문제(T10), `TQ02`는 정상 syscall을 유지하는 공격(T02), `TQ03`은 AntNet의 지표별 열세(T03), `TQ04`는 Andon 사용 중단(T09)을 찾도록 작성했다. 이 확인 때문에 다음의 강한 주장을 채택하지 않았다.

| 반박되는 주장 | 관측된 반례 | 남는 좁은 결론 |
| --- | --- | --- |
| 생물에서 강건하므로 소프트웨어에서도 자동으로 강건하다 | T01의 재활성화 부하 피드백; T02의 보이지 않는 공격 | 관측·상태 수명·부하 범위를 명세한 관계만 검토 가능 |
| 다른 분야에서 가져오면 모든 성능 지표가 좋아진다 | T03에서 throughput와 delay의 우열이 다름 | 목표 지표·trade-off가 없는 검색 결과는 판단 불가 |
| 차단·분리는 항상 회복을 돕는다 | T10의 모드와 회복 지연; T04의 용량·공유 의존성 | 차단·분리 경계와 회복 전이를 함께 설계해야 함 |
| 사람에게 신호 장치만 제공하면 사용할 것이다 | T09의 사용 중단과 미안정 행동 | 문화·응답·인센티브도 연결 조건 |

**H — 검색 결과에 남겨야 할 최소 내용.** 원 분야 명칭 다음에 `관계 1개 → 대상의 부품/상태 → 보존하는 조건 → 추가 연결 작업 → 실패 입력 → 원저자의 입증 수준`이 있어야 한다. 단어 목록만 있으면 TC09의 보존식과 멱등성처럼 서로 다른 속성을 혼동하기 쉽다. T축 밖 별도 메모로 원 연구의 크기·시간 지연·사람의 권한/행동을 붙이는 것이 유용하다. 이는 T축 재설계가 아니라 Q7 설명의 보충이다.

## 자료 연결

실제로 연 주소, 읽은 절, 확인 내용, 접근 시각과 제외 사유는 `evidence/transfer-sources.json` 및 통합 `sources.json`의 T01–T11에 있다. 원저자 자료:

- [T01 Demers 외, Epidemic Algorithms for Replicated Database Maintenance](https://www.cis.upenn.edu/~bcpierce/courses/dd/papers/demers-epidemic.pdf)
- [T02 Forrest 외, A Sense of Self for Unix Processes](https://www.ieee-security.org/TC/SP2020/tot-papers/forrest-1996.pdf)
- [T03 Di Caro·Dorigo, AntNet](https://arxiv.org/pdf/1105.5449)
- [T04 Nygard, Release It!, 1판 원문 사본](https://www.academia.edu/29742723/Release_It_Michael_Nygard)
- [T05 Stribblehill, Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [T06 Kelly 외, Rate Control for Communication Networks](https://web.stanford.edu/class/cs244/papers/ShadowPricesFairnessStability.pdf)
- [T07 Kirkpatrick 외, Optimization by Simulated Annealing](https://cgi.cse.unsw.edu.au/~cs4601/refs/papers/KirkpatrickGelattVecchi83.pdf)
- [T08 Mettle, Double Entry and Event Sourcing](https://www.mettle.co.uk/blog/innovation-at-mettle-double-entry-and-event-sourcing/)
- [T09 Ayers·Cohen, Andon Cords in Development Teams, 공개 transcript](https://videos.itrevolution.com/watch/504281981/)
- [T10 Brooker, Timeouts, Retries, and Backoff with Jitter](https://d1.awsstatic.com/builderslibrary/pdfs/timeouts-retries-and-backoff-with-jitter.pdf)
- [T11 Google/PagerDuty 저자들, Incident Response](https://sre.google/workbook/incident-response/)

## 한계

선택된 사례 집합은 성공 사례의 발생률이나 먼 유추의 평균 효과를 추정하는 표본이 아니다. 논문의 실험·증명, 원저자의 운영 보고, 조직의 소개 글을 같은 인과 증거로 묶지 않았다. T09의 영상은 로그인 요구가 있으므로 공개된 전체 transcript를 읽었고 영상을 시청했다고 기록하지 않는다. T04는 제3자 호스트의 원저자 책 본문 사본이며 2007년 1판 내용을 확인한 것이다. 알고리즘 재실행·공격 재현·서비스 부하 시험은 수행하지 않았다. 다음 단계의 구체 입력은 각 `minimum_next_check`에 기록했으며 P1/P2 실제 적용 후보의 채택 여부는 별도 RETRIAL 판정이다.
