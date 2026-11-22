# 통계 분야48대응 — 판독 범위·반례·민감도

## 결과와 판독 경계

`S01–S06 × R01–R08`의48개 대응과168개 필수조건 판독을 `statistics.jsonl`에 남겼다. 엄격 `support`0, `partial`12, `conflict`3, `unverified`33이다. 전체 설계를 지지한다고 판정한 행은 없다. 이는 양성 수를 종료조건으로 삼지 않은 닫힌 집합 판독이다. 일반 웹의 원리 존재율이나 통계분야 전체의 전이 가능성으로 확대하지 않는다.

판독자는 제공 원문 감사 뒤 고정 수신 최초 본문·조건을 받았다. S/R 질의, 검색순위, 다른 분야의 판정, 수신 후속 결말은 읽지 않았다. 별도 모델 문맥의 분야 판독이며 독립 사람 실험은 아니다. 여섯 제공 문서는 선정된 전문을 직접 읽었다. 수신은 고정목표의 모든 필수조건과 주변 동기·반례 절을 직접 읽고 전체 snapshot SHA를 확인했다. 긴 최초안 전체의 모든 행을 이번에 새로 코딩한 것으로 표시하지 않았다. 정확한 범위는 `statistics-attempts.jsonl`의 STJ-READ-R01…R08에 있다.

필수조건이 여러 작동을 묶고 있을 때 그 일부만 맞으면 해당 조건의 상태는 `missing`이며 설명에 실제 단서와 남은 부분을 적었다. 따라서 `partial`행에도 완전히 `match`인 복합조건이 없을 수 있다. 부분 영감과 전이 완료를 혼합하지 않는다. 부재는 금지가 아니므로 대부분 `unverified`/`partial`로 두었다. `conflict`3개는 아래에 명시한 대응을 실제로 채택할 때 반대 작동이 발생하는 경우만 센다.

## 가장 강한 부분 대응

| 대응 | 실제로 옮길 수 있는 한 단계 | 남아 있는 핵심 | 양측 위치 |
| --- | --- | --- | --- |
| R01–S01 | 생산자가 중요한 출력/구조 변화를 사전에 알려 이용자에게 이행 준비 시간을 준다. | 옛 이름→새 이름 전달, 동일 의미 보존, 호출 시 미래 의미전환 경고는 새로 필요하다. | R01 9–10·31–33; S01 61 |
| R06–S02 | 고유 개인 인증·감사와 별도 격리 환경을 사용해 공개 접근과 제한 접근의 경계를 둔다. | 구성 객체형·두 파일의 상호금지·flag 우선순위·공유갱신의 개인값 비침범은 근거가 없다. | R06 158–159·208–223·353–356; S02 19·23·27 |
| R07–S05 | 추정과 특정 셀의 errata를 병존시키고 다음 공표라는 종료 경계를 명시한다. | 구/신 표현 생성 진리표, 값 동등검증, 소비자 권위, N+4 보완, 생성후 불변이 없다. | R07 260–294; S05 1·3·5 |

위 표는 추천 성공 목록이 아니다. 통지·격리·표현 병존이라는 구체 작동 일부를 옮길 후보이며, 핵심 경계가 모두 수신에게 남으면 완결로 세지 않았다. 원 순위는 보지 않았으므로 이 표의 순서를 검색결과 순위라고 해석하지 않는다.

## 명시 반대3개와 해석 민감도

| 대응 | 명시한 대응 가정 | 반대가 되는 작동 | 판정을 바꿀 최소 자료 |
| --- | --- | --- | --- |
| R01–S03 | 새 추정 vintage를 이름만 바뀐 동일 기능에 대응 | S03 ¶24.107·24.120–121은 새 자료/정합화로 동일 참조기간의 값까지 바꾼다. R01은 기존 효과의 동일성을 요구한다. | 원 기능을 별도 이름으로 그대로 보존하고 옛 진입점이 그 대상으로 전달하는 통계 제품/계열 개명규약 |
| R02–S03 | 여러 입력의 불일치 처리를 명시된 충돌 항목 처리에 대응 | S03 ¶24.120은 기초자료 값을 조정해 불일치를 해소한다. R02는 양쪽을 명시했을 때 모호성 오류를 유지한다. | 입력 도입이 암묵/명시인지 구별하고 명시된 둘의 모호성은 유지하며 각각 한정 접근을 보존하는 원절 |
| R07–S03 | 같은 참조기간·변수의 값을 생성된 객체의 정규값에 대응 | S03 ¶24.121·24.123·24.129에서 그 값을 소급 개정한다. R07의 동일 객체 정규필드는 불변이다. | vintage마다 별개 불변 객체를 생성하는 규칙과 구/신 소비자에 대한 양방향 표현 보완·일치검증 규약 |

이 대응 가정 자체를 거부하는 더 엄격한 판독에서는 세 행을 `unverified`로 낮출 수 있다. 파일에 이 대체 읽기를 남겼다. 이 경우 conflict0/unverified36/partial12/support0이며 엄격 양성0은 변하지 않는다. 특히 R07에서 새 vintage를 별개 객체로 잡으면 값개정과 객체불변의 직접 충돌은 사라질 수 있다. 그러나 고정목표의 같은 객체·구/신표현 계약과 필요한 변환 규칙이 새로 입증되는 것은 아니다. 소재가 통계라는 이유로 불가능하다고 판정한 것이 아니다.

## R04-M07 권고 하위절만 선호로 낮추기

R04 125–129행은 결과/과정 설명을 이상적 구성으로 말하고, 343–351행은 회고의 권고 표현을 쓴다. 요청한 민감도에서는 그 권고적인 산출물/과정 설명만 필수에서 선호로 내린다. 원 입력·원 판정은 바꾸지 않는다. 인프라 보관, 공개 중단 통지, 비공개 회고 경계 및 M06/M08을 통째로 없애는 민감도가 아니다.

| 제공 문서 | 원 판정 | 권고 하위절만 선호일 때 | 남은 결정적 미충족 |
| --- | --- | --- | --- |
| S01 | partial | partial | 활동정지-보관 전이, 읽기전용 인프라, 리더·상위합의·과거판단 재검토 뒤 복원 |
| S02 | unverified | unverified | 접근기간/인증은 집단의 보관·복원 수명주기를 정의하지 않음 |
| S03 | partial | partial | 역사계열 재개정은 집단 리더 배정·상위팀 합의와 읽기전용 인프라 복원이 아님 |
| S04 | partial | partial | 오류의 미정정/정정예정 상태는 활동집단의 보관과 승인된 재개가 아님 |
| S05 | partial | partial | 정정 통지의 유한 보존은 보관 인프라와 재개 합의를 제공하지 않음 |
| S06 | unverified | unverified | 정책 책임자/검토일은 개별 보관집단의 중단·복원 규칙이 아님 |

6행 모두 엄격지지는 여전히 없다. 권고 하위절 오분류 가능성만으로 이 분야의 양성이 생기지 않는다는 제한된 민감도다.

## 시간·신규성·채택

S01/S02/S03/S04/S06의 봉인 판 날짜는2025–2026년이고 수신8개는2020년1월이다. 따라서40대응에서 **그 고정 판**을 당시 이용 가능했다고 세지 않았다. S05는 날짜 없는 현재판이므로8대응 모두 당시 이용 가능성 미확인이다. 전이 자체의 현재 판단과 과거 이용 가능성은 각 행에 별도 열로 있다. 오래된 원리일 가능성을 부정한 것이 아니라 해당 과거판을 이번에 읽어 입증하지 않았다는 뜻이다.

8개 최초본문의 전체 문자열에서 여섯 제공 도메인·발행처 이름을 검사한48쌍은 일치0이었다. 관련 절·기지 해결책 목록에서도 직접 인용을 발견하지 못했다. 이 검사는 설계자의 미인지, 다른 이름으로 이미 아는 동일 원리, 새로운 발명을 증명하지 않는다. 수신 후속을 열지 않았으므로 실제 채택이나 구현 성과는 모두 미확인이다.

## 재검과 다음 첫 확인

48개 고유 pair, 질문별6개, 필수조건168개, URL/원문해시, 제공 행 범위가 본문길이 이내임을 검사했다. `support`를 부여할 때 모든 필수조건이 match여야 한다는 검사는 양성0인 현재 표에서도 유지한다. 이 구조검사는 의미 판정의 정확성을 인증하지 않는다.

다음 검토자는 R01–S01, R06–S02, R07–S05의 부분 단서가 실제 접합비용을 줄이는지 각각 양측 원절을 먼저 읽어 판단할 수 있다. S03의 세 반례는 실제 수정 방향과 논리 객체의 신원을 확인하는 데 사용한다. 제공 문서를 더 유리한 절이나 다른 문서로 교체하거나 후속 결과를 보고 현재 원 판정을 올리지 않는다.

## 원문 연결

- R01: [고정 최초본문](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md)
- R02: [고정 최초본문](https://github.com/rust-lang/rfcs/blob/6fb5bd5a6132b15bfe2d9dade6a48d7a77eb2b24/text/0000-supertrait-item-shadowing.md)
- R03: [고정 최초본문](https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md)
- R04: [고정 최초본문](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md)
- R05: [고정 최초본문](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md)
- R06: [고정 최초본문](https://github.com/kubernetes/enhancements/blob/50f8b89cb8f0b3d10b1b0d5bc278122abbd23c84/keps/sig-cluster-lifecycle/wgs/20200108-instance-specific-componentconfig.md)
- R07: [고정 최초본문](https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md)
- R08: [고정 최초본문](https://github.com/kubernetes/enhancements/blob/2cef2aacc29238c4fffad906b429cedef2dba21d/keps/sig-scheduling/20200114-taint-based-evictions.md)
- S01: [공식 제공 원문](https://www.ons.gov.uk/aboutus/transparencyandgovernance/releasepracticepolicy) — 봉인본 2026-04-16, 검색본문 SHA256 `9487ac8853395bab13e9118a4842c10b1247cae3b8c1c9435829a8c907697dec`
- S02: [공식 제공 원문](https://www.statcan.gc.ca/en/trust/revisions-policy-official-release) — 봉인본 2025-12-23, 검색본문 SHA256 `bbe8ef61459892335641dee81e0f71a52fdd649835cb677684379a243847cb53`
- S03: [공식 제공 원문](https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/australian-system-national-accounts-concepts-sources-and-methods/edition-8/chapter-24-quality-national-accounts/revisions) — 봉인본 2026-01-20, 검색본문 SHA256 `d8c72bda2e9a662c238b3069f187ba4062b718ba5b6a68e966fc7a09b6156947`
- S04: [공식 제공 원문](https://www.bls.gov/about-bls/bls-error-correction-policy.htm) — 봉인본 2026-08-28, 검색본문 SHA256 `c007fcb253a57a69d780d01b0745e5501e41c1929b16a700d2bb0b058f2ffcb0`
- S05: [공식 제공 원문](https://www.bea.gov/about/policies-and-information/correction) — 봉인본 발행일 미상, 검색본문 SHA256 `3a0bf413e5b8fa927adb08834b7fff1a634dad3e4ac53dec33ed7ab09486197a`
- S06: [공식 제공 원문](https://www.stats.govt.nz/about-us/legislation-policies-and-guidelines/release-practices-policy/) — 봉인본 2026-03-31, 검색본문 SHA256 `e0686c5eb1ad0f2ce97b8f306b4986671bb3e27d949c26d633b82f4e2eb7ae85`
