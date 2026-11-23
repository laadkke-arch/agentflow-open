# AF-RES-069 P2 — FAA 절차의 사후 보조 비교

## 결론과 비교 범위

항공의 수신 확인·명령 재확인·실제 상태 보고 구분은 **부모 또는 중간 장치의 응답을 실제 Chime 볼륨 변경과 혼동하지 않기 위한 보조 원리**로 적절하다. 그러나 Reolink의 대상 식별, setter, 상태 조회 기능을 제공하는 구현 부품은 아니다. 정확한 Chime에 접근하는 API가 있으면 Home Assistant의 기존 Chime 엔티티와 동작이 더 직접적이다. API가 없거나 의미가 확인되지 않았으면 어느 자료도 P2의 완성 해법을 입증하지 않는다.

이 비교는 검색·초기 판정이 `de1727aada52835ebcde4ff1c92c3940db215476`에 봉인된 뒤 root가 항공 분야를 골라 수행했다. 원실험의 A/B 검색 적중, 고정 질의, 15개 순위 자리, 원문 독해 분모에 **모두 0으로 산입**한다. 동일 모델의 후속 독해이며 독립 사람 판독이나 재현 실험이 아니다. 실제 항공 업무 지침을 제안하지 않고 소프트웨어의 증거 의미만 비교한다.

- 직접 독해: FAA 원문 2건, 문서/저작 식별자 2개.
- 보수적 독립 절차 근거군: 1개. AIM/Glossary는 한 manual 계보로 보고, JO 7110.65도 해당 절에서 AIM을 직접 인용하므로 같은 관련 절차 근거군으로 묶었다. 서로 다른 문서라는 사실은 유지한다.
- 새 공식 검색: 1질의, 본문 open 2회. 추가 동일 문서 접근·실패·재시도: 각각 0회.
- 소프트웨어 통합·실행·장치 시험: 0회. 새 Reolink API 기능 입증: 0건.
- 기록 작성 확인: 2026-11-23 09:09:18 UTC.

## 실제로 읽은 공식 자료

| ID | 저자·문서·판 확인 | 직접 읽은 절 | 자료가 지지하는 범위 |
| --- | --- | --- | --- |
| AUX-FAA-01 | FAA, AIM Chapter 5 Section 3. 2026-11-23 09:03:20 UTC의 live HTML. 정확한 판/시행일은 열린 본문에 없어 미확인. | TBL 5-3-1의 응답·할당값·실제 상태 보고 항목; ATC Frequency Change Procedures의 실제/할당 고도 확인 부분. | ROGER는 수신, WILCO는 이해와 향후 이행 의사다. 할당값 확인과 실제 상태 보고는 구분된다. |
| AUX-FAA-02 | FAA, Order JO 7110.65 Chapter 2 Section 4. 2026-11-23 09:03:37 UTC의 live HTML. revision suffix/시행일 미확인. | §2-4-3 PILOT ACKNOWLEDGMENT/READ BACK, L18–L44. | readback의 항목 정확성과 대상 식별을 확인한다. 응답 이전의 불확실성을 설명하지만, 응답이 곧 완료라는 역명제는 지지하지 않는다. |

원문: [AUX-FAA-01 — FAA AIM](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap5_section_3.html), [AUX-FAA-02 — FAA JO 7110.65](https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap2_section_4.html?trk=article-ssr-frontend-pulse_little-text-block). 정확한 검색 payload, 반환 참조, 절 위치, 확인 시각, 반환 본문 해시는 [aviation-sources.jsonl](aviation-sources.jsonl)에 있다. 검색 결과에 나온 P/CG index의 판 정보를 실제 연 AIM/JO 문서에 대신 적용하지 않았다.

## 어디까지 대응할 수 있는가

다음은 FAA가 Reolink에 대해 한 주장이 아니라, 직접 읽은 구분을 P2에 적용한 분석이다.

| 확인하려는 사실 | 소프트웨어에서 대응하는 근거 | 아직 증명하지 못하는 것 |
| --- | --- | --- |
| 요청을 받았음 | HTTP/프로토콜 응답, Hub의 요청 접수 | 실제 Chime에 도달했는지, 그 속성이 바뀌었는지 |
| 요청 대상·내용을 이해했거나 수락함 | operation/target/value가 맞는 echo 또는 accepted 응답 | 실제 leaf 설정 변경 완료 |
| 요청·할당된 값이 무엇인지 | desired state, 요청 캐시, 서버의 설정 의도 | 현재 장치가 보고하는 값 |
| 실제 말단 설정이 무엇인지 | 특정 Chime에서 온 신뢰할 수 있는 최신 상태값 또는 동등한 결과 보증 | 그 값과 실제 음향 출력의 관계까지 항상 보증하지는 않음 |
| 실제 출력이 달라졌는지 | 대상 Chime을 식별한 재생·관찰 등 목적에 맞는 장치 시험 | 다른 장치·다른 펌웨어·다른 연결에서도 작동한다는 일반화 |

**항공 readback/hearback 자체는 명령 내용을 되말하고 확인하는 절차다. 이를 소프트웨어의 실제 상태 getter와 같은 것으로 번역하면 오히려 비교 목적을 어긴다.** 이 사례에서 더 유용한 대응은 readback이라는 이름보다 **desired/assigned 값과 actual/observed 값의 구분**이다. 상태 보고 역시 독립 계측이나 물리 효과의 무조건적 보증으로 올려 읽지 않는다. 이 제한은 [AUX-FAA-01의 실제/할당 확인 부분](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap5_section_3.html)과 [AUX-FAA-02 §2-4-3](https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap2_section_4.html)에서 허용되는 좁은 해석이다.

응답을 준 endpoint가 부모/Hub라는 사실만으로 그 응답이 무효인 것도 아니다. Hub가 정확한 leaf로 전달하고 그 결과를 보증하는 계약을 실제로 제공한다면, 부모를 통한 결과도 유효할 수 있다. 반대로 응답에 Chime ID와 요청값이 함께 있어도 단순 echo라면 부족하다. 판별 기준은 응답 위치가 아니라 **대상, 값의 출처, 최신성, 완료 의미를 뒷받침하는 API 계약과 관찰**이다. 이 문헌 독해에서는 그런 Reolink 계약을 확인하지 않았다.

## Home Assistant 동종 기능과의 비교

봉인된 A-P2-S02에서 이미 읽은 [Home Assistant Reolink 공식 문서](https://www.home-assistant.io/integrations/reolink)는 `Chime volume` number entity와 `reolink.play_chime` 동작을 명시한다. 카메라/문벨/Hub 볼륨과 구분되는 동일 분야의 제어 인터페이스이므로 직접성이 높다. 다만 그 문서의 기능 목록만으로 정확한 **Home Hub Mini → Battery Doorbell → paired Chime** 연결의 발견·setter·readback 경로까지 검증된 것은 아니다. 이 자료는 기존 독해의 재사용이며 이번 새 FAA 독해 수에 더하지 않는다.

기존 A-P2-S03의 [Reolink 연결 설명](https://support.reolink.com/articles/28092829337497-How-to-Connect-Reolink-Video-Doorbell-Battery-to-a-Chime/)은 Mini에서 Doorbell 내부 Chime 페어링을, 일반 Hub/Pro에서는 별도 등록 경로를 구분한다. A-P2-S05의 [Reolink 설정 설명](https://support.reolink.com/articles/11613761961241-Configuration-Guide-How-to-Set-Up-Reolink-Chime/)에는 Chime의 별도 Sound 설정과 Test가 있다. 이는 대상과 검증 지점을 좁히는 동종 근거지만 HA의 정확한 API 지원을 증명하지 않는다.

| 실제 API 전제 | Home Assistant 쪽 직접성 | FAA 비교의 보조 역할 | P2 판정 한계 |
| --- | --- | --- | --- |
| 정확한 leaf 발견·setter와 신뢰할 수 있는 최신 leaf 상태값이 모두 있음 | 기존 Chime entity/action을 연결하고 같은 대상의 전후 값을 확인하는 가장 직접적인 후보 | 접수·의도·관찰 결과의 근거를 분리 | 실제 대상 조합에서 구현·실행 전에는 완성품 합격 아님 |
| setter 응답 자체가 실제 leaf 결과를 보증함 | 확인된 계약에 따라 그 반환을 결과 근거로 쓸 수 있음. 별도 GET을 무조건 요구할 이유는 없음 | 일반 ACK와 결과 보증 응답을 구분 | 실제 계약·대상 식별·freshness는 별도 확인 필요 |
| setter는 있지만 신뢰할 getter/결과 보증이 없음 | 쓰기 시도는 가능하나 성공 ACK만으로 실제 변경 판정 불가 | 증거가 멈춘 단계를 명시 | 권한 있는 대상 장치 시험 등 추가 관찰 필요 |
| 실제 상태 getter는 있지만 setter가 없음 | vendor에서 바꾼 상태 관찰 가능성만 있음 | 관찰과 제어 능력 분리 | HA에서 제어한다는 C2는 아직 충족하지 않음 |
| 부모 볼륨·Hub의 일반 ACK·root 목록만 확인됨 | 먼저 leaf 발견/주소 지정/명령 경로를 확인해야 함 | 부모 성공을 leaf 성공으로 올려 읽는 오류 방지 | 비어 있는 root 목록만으로 모든 하위 leaf의 존재·부재 또는 제어 가능성을 단정하지 않음 |

C1은 기존 연결을 유지한 채 정확한 Chime에 접근하는가, C2는 그 Chime의 볼륨을 제어하는가다. FAA 문헌은 두 조건을 직접 support하는 제품 근거가 아니다. 조건 판정에 사용할 관찰의 종류를 더 명확히 하는 **이전 조건이 필요한 타분야 원리**다.

## 최소 반례와 다음 확인

최소 소프트웨어 반례는 다음과 같다. 목표 Chime C의 현재 값은 2이고 요청값은 0이라고 하자. Hub가 `C, 0`을 접수하고 올바르게 echo하지만 leaf 전달이 실패해 C는 2를 유지한다. 수신·대상 확인·요청 내용 일치는 모두 성립해도 실제 설정 변경은 실패한다. getter가 실제 장치 대신 요청 캐시의 0을 돌려주면 형식상 readback까지 통과할 수 있다. 이는 자료에서 관찰된 Reolink 고장 사례가 아니라, “응답/echo만 있으면 성공”이라는 판정을 기각하는 분석용 반례다.

이전 자체의 최소 실패 조건은 **접근 가능한 target setter가 없거나, 결과의 의미를 판별할 수 없는 경우**다. 수신·의도·결과라는 이름을 붙여도 빠진 제어 경로가 생기지는 않는다. 반대로 실제 leaf 결과를 보증하는 API가 확인되면 별도의 항공식 표현이나 단계 추가 없이 기존 동종 기능만으로 충분할 수 있다.

후속 구현 검토에 사용할 수 있는 확인 항목은 다음과 같다. 모두 제안이며 이번에 실행하지 않았다.

1. Hub, Doorbell/channel, Chime 식별의 연결을 확인하고 실제 쓰기 대상과 결과 대상이 같은지 비교한다. 잘못된 Chime에 같은 값을 쓰면 실패로 남긴다.
2. setter 반환이 접수, 수락, 요청 echo, 실제 결과 중 무엇인지 문서/코드/실행 관찰로 확인한다. 완료의 의미를 이름으로 추정하지 않는다.
3. 값의 출처가 desired 캐시인지 실제 장치인지 확인한다. 요청 이전 값이나 다른 대상 값을 성공 근거로 섞지 않는다.
4. C2를 “말단 설정값 변경”으로 주장하면 그 수준의 관찰을, “실제 소리 크기 변화”까지 주장하면 그 효과를 뒷받침하는 관찰을 남긴다. 단순히 Hub나 Doorbell 자체가 울린 결과로 대체하지 않는다.

이 비교가 추가한 것은 위와 같은 **검증 질문의 구체화**다. 새로운 Reolink endpoint, 실행 코드, 작동 결과는 얻지 못했다. 원실험 이후 선택한 분야이므로 B 검색의 효과, 원래 질의의 우수성, 또는 타분야 이전이 해결률을 높였다는 인과 증거로 쓰지 않는다.

## 감사 가능한 접근 기록

- 검색 시작/완료: 2026-11-23 09:02:58 / 09:02:59 UTC.
- 정확한 질의: `site:faa.gov Pilot Controller Glossary ROGER WILCO received understand comply`.
- 엔진/제약: `system1_search_query`, `domains: ["faa.gov"]`, `response_length: "long"`; 공개 공식 문서만.
- AUX-FAA-01: 검색 ref `turn318192495search5` → open ref `turn358342761view0`, 09:03:20 UTC.
- AUX-FAA-02: 검색 ref `turn318192495search4` → open ref `turn665510037view0`, 09:03:37 UTC.
- 검색 서비스의 실제 엔진 HTML URL은 제공되지 않았다. 이를 만들지 않고 `tool_query:` 식별자와 정확한 payload를 JSONL에 보존했다.
- 총 웹 도구 호출 3회(검색 1 + open 2). 기존 원실험 파일 수정 및 Git 커밋 없음.
