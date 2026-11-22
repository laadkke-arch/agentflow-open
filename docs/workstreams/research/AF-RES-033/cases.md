# AF-RES-033 사례·반례와 역할별 판독

## 1. 결론과 고정된 관측 범위

**원문의 단어를 쓰는 S와 작동 관계를 쓰는 R 모두, 상위 1·3에서 고정 부분 목표의 필수조건을 한 반환창으로 완결 인용한 수신은 0/8이었다.** 전체 18문서를 각 수신에 대응한 144행에서는 R05–L06 한 쌍만 부분 목표의 `support`다. 이 쌍은 S10/R12라 두 경로 모두 상위 3에서 반환하지 못했다. 이 현재 관계 지지는 **수신 최초 본문에 이미 있는 API 접수/제공자 실현 경계를 타 분야 원문으로 인용 보완한 것**이다. 설계자에게 새 아이디어를 제시했거나 채택을 일으킨 효과는 미확인이다. 근거: [재집계 영수증](evidence/recount.json), [원 순위](rankings.csv), [원 반환](returns.jsonl), [R05 최초 고정 본문][R05-initial].

| 고정 단위 | 결과 | 해석 경계 |
| --- | --- | --- |
| 수신 집계 단위 | 8개 | 후보18·144대응·16검색과 다른 분모; R01/R03은 문제 맥락을 공유하며 통계적 독립 표본이 아님 |
| 원 검색 | S 8회 + R 8회; 상위3 반환48창 | 관계 표현이 이 폐쇄 집합에서 엄격 상위 인용 성공을 개선했다고 말할 수 없음 |
| 엄격 인용 완료 | S 상위1 0/8, S 상위3 0/8, R 상위1 0/8, R 상위3 0/8 | 양쪽 성공·S만·R만은 0개, 양쪽 미완료는 8개 |
| 전체144대응 | support 1 / partial 50 / conflict 9 / unverified 84 | 전체 설계 support는 0; partial을 support에 합치지 않음 |
| 전수 목록에 엄격 적격이 있는 수신 | 1개: R05, 후보L06 | 적격 수신에서 양쪽 상위3 누락1/1. 보수적 판독 민감도는 아래 분리 |
| 현장 검증 | 4원문 / 교통·통계 2분야 / 3사건 | F01·F02는 같은 MTA 감편 사건; 도서관 현장 사건 없음 |
| 수신 후속 | 8건 모두 직접 제공 인용·인과적 채택 미확인 | 제한된 공개 문자열·의미 판독이 미인지·미채택을 증명하지 않음 |

이 문서는 관측 봉인 `889c5e792a3db3856bf5be8c90d9486490ce8677` 이후의 통합 설명이다. 최초 검색은 `a2ce15d10415c556574d1a65af77718a81052d01`에서 후속 열람 전에 봉인됐다. 아래의 한 줄 설명은 모두 사후 작성이며 최초 질의나 최초 반환 문구가 아니다. 이 작성에서는 새 검색·Git 명령·원문/질의/순위/기존 판정 수정이 없었다. [현장·후속 상세 분석](analysis/field-and-followup.md), [별도 원문 판독](judgments/critical-review-notes.md)을 연결하되 관측 시점과 증거 층을 합치지 않는다.

## 2. Q7 대표 사례와 출처 고정 방식

| 사례ID | 대응·고정 판정 | 최초 순위·실제 반환 | 전체 문서 판독에서 확인한 범위 |
| --- | --- | --- | --- |
| X01 | R05–L06 support: 전수 목록에서만 성공 가능 | S10/R12; 양쪽 상위3 미반환 | L06의 중앙 접수 금지와 공급기관 재량 분리, 한 책의 시청각 구성요소 |
| CE01 | R01–T02 conflict | S2: W003, 40–65행·토큰401–600; R5 미반환 | 동일하지 않을 수 있는 대체서비스와 동일 macro 동작 필수조건의 충돌 |
| CE03 | R04–L03 partial: 핵심 남아 보류 | S2/R1: 모두 W005, 133–173행·토큰801–1000 | 49행 이력·213–217행 재요청은 반환창 밖. 공개 보존·복원 승인 핵심은 전수 판독에서도 없음 |

수신 URL은 SHA로 고정한 본문이다. 제공 L03/L06은 날짜 없는 가변 HTML이고 T02의 `sources.jsonl.fixed_url`도 null이므로, 제공 URL을 immutable URL로 가장하지 않는다. 공식 URL과 **봉인된 텍스트/원문 해시**를 함께 사용한다. 행 번호는 고정 캐시의 1-based inclusive 행이며 가변 웹 줄 수가 아니다. 모든 Q7 행에 양측 URL·출처ID·해시·절·행을 넣었다. [기계 판독용 9개 걸음](analysis/q7-role-walkthroughs.jsonl).

| sources.jsonl 정규ID | 고정 본문/공식 URL | 고정 텍스트의 핵심 위치 |
| --- | --- | --- |
| kubernetes-enhancements-pr-1438 (R05) | [최초 본문][R05-initial] | 98–117,261행 |
| L06 | [VPL ILL][L06] | 3,19–27,64–106행 |
| rust-lang-rfcs-pr-2843 (R01) | [최초 본문][R01-initial] | 9–10,31–33행 |
| T02 | [MBTA Diversion Standards][T02] | 14–33,63–88,136–174행 |
| rust-lang-rfcs-pr-2856 (R04) | [최초 본문][R04-initial] | 112–144,329–351행 |
| L03 | [Multnomah ILL][L03] | 39–57,105–115,193–219행 |

## 3. 세 사례 × 세 관점: 아홉 개 걸음

각 행동은 원문 관계를 검토하거나 접합할 한 단계다. 실제 수신 설계자가 이 설명을 보고 수행했다는 기록이 아니다. 현장 연결은 관계의 경계를 검사하는 별도 사건이며, 후보 정책 또는 수신 설계의 현장 채택을 증명하지 않는다.

### X01 — R05–L06: 전수 목록에서만 확인한 부분 관계 지지

두 경로 상위3 미반환. 전수 원문에서 확인한 support이며 최초 R05에 이미 있는 API/제공자 경계의 타 분야 인용 보완이다. 새 아이디어 제시/채택의 효과는 미확인.

#### Q7-01 수신 설계자

**한 줄:** 접수 성공과 실제 제공 성공을 서로 다른 상태로 유지한다.

근거: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md) 98–117,261행 (Proposal; activation status) ↔ [L06](https://www.vpl.ca/borrowing/interlibrary-loans) 3,19–27,64–106행 (VPL intermediation; requestability versus availability).

**옮길 한 단계:** 이미 있는 API 접수→controller 전달 경계를 한 객체의 혼합 허용과 downstream 실현 판단의 두 단계로 명시한다. **깨질 한 조건:** 한 대상 안의 혼합 허용이 필요하다. 여러 독립 자료형의 목록이나 공급자 재량만 남기면 R05-M01이 빠진다.

사후 연결: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/pull/1438#discussion_r367654556) — review discussion_r367654556: 첫 protocol 오적용·오류 미고지 우려. [F04](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires) — MYE3 357지역키·39변경키·78 H/I셀·J/O불변은 입력 경계를 생략하면 안 된다는 별도 현장 반례. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-02 절차 운영자

**한 줄:** 외부 제공자가 보내지 못하는 것은 중앙에서 요청 자체를 금지하는 것과 다르다.

근거: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md) 98–117,261행 (Proposal; activation status) ↔ [L06](https://www.vpl.ca/borrowing/interlibrary-loans) 3,19–27,64–106행 (VPL intermediation; requestability versus availability).

**옮길 한 단계:** 접수 담당·중계 기능·실제 공급자의 권한과 결과를 따로 기록한다. **깨질 한 조건:** 공급자의 복합 책 재량을 API의 혼합 자체 거절 권한으로 옮기면 R05-M01을 깨뜨린다.

사후 연결: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/pull/1438#discussion_r367654556) — review discussion_r367654556: 첫 protocol 오적용·오류 미고지 우려. [F04](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires) — MYE3 357지역키·39변경키·78 H/I셀·J/O불변은 입력 경계를 생략하면 안 된다는 별도 현장 반례. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-03 반례 검토자

**한 줄:** 복합 책 항목을 빼면 공급자 재량만 남고 혼합 요청 허용의 지지는 사라진다.

근거: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md) 98–117,261행 (Proposal; activation status) ↔ [L06](https://www.vpl.ca/borrowing/interlibrary-loans) 3,19–27,64–106행 (VPL intermediation; requestability versus availability).

**옮길 한 단계:** 복합 항목의 목록 소속과 공급자 재량을 동시에 대조하고 106행 없이도 M01을 주장하는지 검사한다. **깨질 한 조건:** 106행을 삭제하거나 단독 시청각자료 금지를 복합 책에 자동 확장하면 support의 근거가 사라진다.

사후 연결: [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/pull/1438#discussion_r367654556) — review discussion_r367654556: 첫 protocol 오적용·오류 미고지 우려. [F04](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires) — MYE3 357지역키·39변경키·78 H/I셀·J/O불변은 입력 경계를 생략하면 안 된다는 별도 현장 반례. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

### CE01 — R01–T02: 구체적 대응 아래 동일성 조건 충돌

S2로 W003(40–65행, 토큰401–600)만 실제 반환; R5 미반환. 전체 문서의 14–33/63–88행을 읽은 충돌 설명을 최초 반환창의 완결 판독으로 소급하지 않는다.

#### Q7-04 수신 설계자

**한 줄:** 대체 경로가 있어도 동일 실행 결과가 보장되지 않으면 안전한 forwarding이 아니다.

근거: [rust-lang-rfcs-pr-2843](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md) 9–10,31–33행 (Identical renamed macro; forwarding and warning) ↔ [T02](https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf) 14–33,63–88,136–174행 (Overview; availability/frequency/span; Customer Information).

**옮길 한 단계:** 옛 호출→새 구현 연결에서 이름·통지보다 먼저 이전 입력/출력 의미의 동일성을 확인한다. **깨질 한 조건:** T02의 일부 역 무제공과 시간·빈도 차이는 R01-M01의 동일 동작 보존에 위배된다.

사후 연결: [OUT-R01-rename-implementation](https://github.com/rust-lang/rust/pull/68404) — PR body second paragraph: forwarding을 구현하되 의존자 이주 때문에 deprecation 보류. [F01](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8) — F01.txt 23–30: 계획 발표·대체서비스·공지 채널. [F02](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13) — printed p13/PDF index12: MTA Real Time 기반 사후 집계. MTA 사건이며 MBTA T02 정책 이행 증거는 아님. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-05 절차 운영자

**한 줄:** 예외가 있는 대체 서비스는 동일 구현의 무손실 별칭이 아니다.

근거: [rust-lang-rfcs-pr-2843](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md) 9–10,31–33행 (Identical renamed macro; forwarding and warning) ↔ [T02](https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf) 14–33,63–88,136–174행 (Overview; availability/frequency/span; Customer Information).

**옮길 한 단계:** 고정노선 평가→부족 구간 보완→변경 공지를 운영하되 보장의 상한을 함께 기록한다. **깨질 한 조건:** 중단된 정규 노선을 새 실행 대상으로 뒤집어도 동일 동작 보장이 생기지 않는다.

사후 연결: [OUT-R01-rename-implementation](https://github.com/rust-lang/rust/pull/68404) — PR body second paragraph: forwarding을 구현하되 의존자 이주 때문에 deprecation 보류. [F01](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8) — F01.txt 23–30: 계획 발표·대체서비스·공지 채널. [F02](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13) — printed p13/PDF index12: MTA Real Time 기반 사후 집계. MTA 사건이며 MBTA T02 정책 이행 증거는 아님. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-06 반례 검토자

**한 줄:** 1:1 보장 부정 문장을 지워도 서비스 제외와 운영시간 예외는 남는다.

근거: [rust-lang-rfcs-pr-2843](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md) 9–10,31–33행 (Identical renamed macro; forwarding and warning) ↔ [T02](https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf) 14–33,63–88,136–174행 (Overview; availability/frequency/span; Customer Information).

**옮길 한 단계:** 주 충돌 절을 제거한 반사실 판독에서 다른 명시적 예외가 같은 불변조건을 깨는지 확인한다. **깨질 한 조건:** 예외를 빼고 대체·고지라는 말만 남기면 실제 제공 계약보다 강한 동일성 보장을 만든다.

사후 연결: [OUT-R01-rename-implementation](https://github.com/rust-lang/rust/pull/68404) — PR body second paragraph: forwarding을 구현하되 의존자 이주 때문에 deprecation 보류. [F01](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8) — F01.txt 23–30: 계획 발표·대체서비스·공지 채널. [F02](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13) — printed p13/PDF index12: MTA Real Time 기반 사후 집계. MTA 사건이며 MBTA T02 정책 이행 증거는 아님. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

### CE03 — R04–L03: 관련 단서는 있으나 핵심 절차가 남아 보류

S2/R1로 양쪽 W005(133–173행, 토큰801–1000)가 반환. 49행 이력 및 213–217행 재요청은 그 창 밖이다. 전체 문서 partial을 엄격 반환창 support로 올리지 않는다.

#### Q7-07 수신 설계자

**한 줄:** 과거 요청 조회와 재요청은 같은 그룹의 승인된 복원을 대신하지 못한다.

근거: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md) 112–144,329–351행 (Archive; infrastructure; restore; retrospective privacy) ↔ [L03](https://multcolib.org/interlibrary-loan) 39–57,105–115,193–219행 (Prior requests; cancellation; active requests; renewal/re-request).

**옮길 한 단계:** 종료 상태 기록이라는 단서를 가져오되 공개 보존·read-only 기반시설·복원 승인을 미해결 핵심으로 남긴다. **깨질 한 조건:** 요청자의 재신청을 liaison/shepherd 지정과 부모팀 합의로 대체하면 R04-M08이 빠진다.

사후 연결: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/pull/2856#discussion_r404969272) — review discussion_r404969272: Restoration이 형성 단계를 생략하는 것은 아님. [F03](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/) — 정정 배너75–82, §5 159행: 발행자 버전 이력은 소비자 복구·그룹 재개를 보장하지 않음. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-08 절차 운영자

**한 줄:** 계정의 6개월 이력과 재시도에는 공개 archive와 상위팀의 복원 권한이 없다.

근거: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md) 112–144,329–351행 (Archive; infrastructure; restore; retrospective privacy) ↔ [L03](https://multcolib.org/interlibrary-loan) 39–57,105–115,193–219행 (Prior requests; cancellation; active requests; renewal/re-request).

**옮길 한 단계:** 종료·이력 조회·재요청의 범위를 표시하고 같은 객체 복원에 필요한 별도 승인 권한을 확인한다. **깨질 한 조건:** 이용자와 기관을 부모팀/그룹으로 뒤집어도 합의·리더 지정은 생기지 않으며 계정 삭제를 전체 자료 파기로 확대할 수 없다.

사후 연결: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/pull/2856#discussion_r404969272) — review discussion_r404969272: Restoration이 형성 단계를 생략하는 것은 아님. [F03](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/) — 정정 배너75–82, §5 159행: 발행자 버전 이력은 소비자 복구·그룹 재개를 보장하지 않음. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

#### Q7-09 반례 검토자

**한 줄:** 이력 절을 빼도 완결 지지로 올라가지 않으며 archival이라는 단어만으로 연결되지 않는다.

근거: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md) 112–144,329–351행 (Archive; infrastructure; restore; retrospective privacy) ↔ [L03](https://multcolib.org/interlibrary-loan) 39–57,105–115,193–219행 (Prior requests; cancellation; active requests; renewal/re-request).

**옮길 한 단계:** 49행 없이 남는 취소·재요청 단서와 빠진 보존·승인 핵심을 다시 구분한다. **깨질 한 조건:** 151행 archival material을 그룹 archive 행위로 바꾸거나 계정 삭제를 유일 보존본 파기로 단정하면 원문을 넘어선다.

사후 연결: [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/pull/2856#discussion_r404969272) — review discussion_r404969272: Restoration이 형성 단계를 생략하는 것은 아님. [F03](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/) — 정정 배너75–82, §5 159행: 발행자 버전 이력은 소비자 복구·그룹 재개를 보장하지 않음. 이 연결을 원래 반환창의 내용이나 직접 제공 원리 채택으로 소급하지 않는다.

### 판독 교란: 원문·검색 수정 실험이 아님

다음 결과는 동결된 [critical-review.jsonl](judgments/critical-review.jsonl)의 민감도를 가져온 **반사실 판독 교란**이다. 원문·질의·검색기를 수정하거나 재검색한 실험, 사람 대상 효과 시험, 실행 시뮬레이션으로 부르지 않는다. 한 절을 지워도 다른 근거가 남으면 분류가 유지된다.

| 사례·기준 | 같은 용어만 남김 | 역할 뒤집기 | 근거절 하나 삭제 |
| --- | --- | --- | --- |
| X01 support | available/request/library만으로 단계와 복합 대상이 없어 unverified | 공급자 재량을 중앙 접수 거절 권한으로 옮기면 conflict; 공급 실패와 접수 실패를 혼동한 매핑 | L06:106 삭제 시 한 대상의 혼합 근거가 없어 partial; 중계/공급 분리는 남음 |
| CE01 conflict | replacement/service/information만으로 동일 실행·warning이 없어 unverified | 중단된 정규 노선을 새 실행 대상으로 놓아도 동일 동작 보장이 없어 conflict | T02:21–33 삭제 후 63–67 무제공·81–88 운영시간 예외가 남아 conflict |
| CE03 partial | archival/requests만으로는 unverified; 151행 archival material은 자료 종류 | 요청자/승인자 역할을 바꿔도 합의·리더 지정이 생기지 않아 partial | L03:49 삭제로 이력 근거는 약해지지만 취소·재요청 단서는 남아 partial |

## 4. RESULT와 공통인 반례 식별자

| ID | 대응·고정 판정 | 막는 과대해석 | 양측 원문 위치 |
| --- | --- | --- | --- |
| CE01 | R01–T02 conflict | 비슷한 대체와 공지가 있으면 동일 동작 forwarding이다. | [R01][R01-initial] 9–10,31–33 ↔ [T02][T02] 14–33,63–88 |
| CE02 | R07–S03 conflict | 일관성을 위해 값을 고치는 절차가 immutable 표현 호환에 그대로 맞는다. | [R07][R07-initial] 260–294 ↔ [S03][S03] 1,37–39,59–67; 단락24.107,24.120–129. 같은 논리 객체 개정이라는 주 매핑 아래 판정 |
| CE03 | R04–L03 partial | 과거 요청 기록과 재신청이 공개 archive 및 승인된 같은 그룹 복원을 완성한다. | [R04][R04-initial] 112–144,329–351 ↔ [L03][L03] 39–57,105–115,193–219 |
| CE04 | R05–L03 partial | 기록물의 예인 mixed collections 제외는 혼합 자체의 금지다. | [R05][R05-initial] 98–117 ↔ [L03][L03] 137–153,203–219. 공급자 재량은 맞지만 복합 객체 접수 허용은 부족; 금지 이유를 혼합만으로 확정하지 않음 |
| CE05 | R08–T06 conflict | 정책 목표·기준선이라는 표현이 같으면 기능 무변경 default-on 승격과 같다. | [R08][R08-initial] 55–71 ↔ [T06][T06] 53–57,68–74,124–149,243–256. 실제 서비스 변경을 새 기준선으로 삼는 구체적 매핑 아래 판정 |

CE04는 별도5행 판독의 대상이 아니며 원 library 판독에 근거한다. 기록물이라는 범주의 제외를 모든 혼합의 금지로 확대하지 않고 M01의 부족을 유지한다. [library 판정](judgments/library.jsonl), [transport 판정](judgments/transport.jsonl), [statistics 판정](judgments/statistics.jsonl). 원문이 없는 핵심을 채워 support로 만들지도, 단어만으로 conflict를 만들지도 않는다.

## 5. 현장 4원문·2분야·3사건의 통합

아래 관측의 직접 열람·재계산 범위는 [현장·후속 담당 분석](analysis/field-and-followup.md)과 [RF-A01–RF-A04 감사](field/resume-field-audit.md)에 기록된 범위다. 이 통합 작성에서 원시 feed나 357행 워크북 전체를 다시 계산했다고 주장하지 않는다. sources.jsonl 정규 ID는 F01–F04이며 FIELD-* 명칭은 별도 새 원문이 아니다.

F01·F02는 발행 기관과 작품은 다르지만 동일한 감편 과정을 다룬다. DCP가 MTA 자료를 집계했으므로 독립적으로 측정한 두 운행 실적은 아니다. F03의 여러 이전판과 F04의 두 XLSX·목록은 각각 한 작품으로 묶었다. 현장·후속 담당 판독의 재독·해시 대조도 고유 원문 수에 추가하지 않는다. 네 현장 자료는 수신 최초 제안의 2020년 1월 이후 사건/정정이므로, 현재 전이 검토용 현장 증거와 당시 이용 가능성을 구분한다. F04의 2023-12-19는 정정일이며 최초 발행일은 원장에서 미확인이다.

| 원장 ID·사건·분야 | 사건과 원문 위치 | 실제 확인 | 예외·반대 해석 | 옮길 수 있는 관계와 남는 핵심 |
| --- | --- | --- | --- | --- |
| F01 / FIELD-TRANSIT-PLAN / 교통 사건 1 | [MTA 2020-03-24 발표][f01], Subways and buses / Long Island Rail Road and Metro-North / communication channels. 캐시 F01.txt L23–30; RF-A01. | 단계별 적용일, 운행 중단 노선을 보완하는 local service, 필요시 서비스 보충 인력·차량, 웹·앱·역 표시를 공표. | 발표는 시행 의사·운영자의 설명이다. 모든 이후 출발, 충분한 빈도, essential-worker의 이동 성과는 확인하지 않음. | 변화 권한을 가진 주체가 새 상태·전환일·대체 경로·고지 채널을 연결한다는 절차는 검토 가능. 동일한 공지를 만들면 실제 실행 권한이나 여분 자원이 생긴다는 가정은 버려야 함. |
| F02 / FIELD-TRANSIT-EXCEPTION / 교통 사건 1 | [NYC DCP 2020-04-21 PDF][f02], 인쇄 p13 / PDF page index 12, Subway System Service Changes. 그래프의 2/13·3/12·4/16 및 우측 설명·하단 출처; RF-A02. | 해시가 고정된 PDF는 **MTA Real Time data**를 출처로 명시. DCP는 시간대별 정차 집계에서 첨두 서비스 감소와 주간 첨두/비첨두 구분 약화를 보고. | 이전 GTFS/정적 예정 운행 해석은 철회. 반대로 real-time이라는 말만으로 원시 feed·집계 코드·실제 운행 전수가 재검증됐다고 할 수도 없음. F01과 날짜·척도가 달라 즉시 약속 위반으로 계산하지 않음. | 공표 계획과 이후 집계를 다른 증거 층으로 연결할 수 있음. 옮길 핵심은 운영 관측의 별도 수집·판독. 데이터가 예측인지 실현인지, 누락/취소를 어떻게 센 것인지는 다음 확인이 필요. |
| F03 / FIELD-STATS-HISTORY / 통계 사건 2 | [ONS 이전판 v1][f03-v1] §5 첫 문단, F03-v1.txt L152; [v2][f03-v2] L156; [정정된 현재 캡처][f03-current] §5 L159 및 정정 배너 L75–82; RF-A03. | v1·v2의 ‘여성 90세 이상도 낮은 추정’이라는 설명이 이후 본문에서 제거됐음을 대조. 2023-02-28의 그림 4·5 지역 라벨 순서 정정과 2023-03-01 문장 정정은 다른 공지로 연결됨. | 이전판을 보존하고 차이를 설명한 사실은 소비자가 업데이트를 보거나 사본을 자동 취소했다는 증거가 아님. 그림 데이터 전체의 독립 재계산은 하지 않음. | 이전/이후 주장, 수정 위치, 이유, 시점을 연결하는 구조는 재사용 가능. 발행자의 수정 권한을 downstream 소비자의 변경/회수 권한으로 대체하면 깨짐. |
| F04 / FIELD-STATS-BOUNDARY / 통계 사건 3 | [ONS 공식 전후판 목록][f04-index] Reason for update, 캐시 L98–101; v1·v2 XLSX의 MYE3!A9:O365와 v2 Correction notice!A1:A3. [v1][f04-v1] / [v2][f04-v2]; RF-A04. | 기존 감사는 지역코드 357개로 조인해 39행·78셀의 H/I 변경, J/O 불변을 재현. 현장·후속 담당 판독도 A/B/H/I/J/O 9–12행 및 정정 공지를 두 워크북의 저장값에서 직접 대조. | 변하지 않은 최종 순이동/인구가 중간 구성값의 정확성을 보장하지 않음. 전 워크북 또는 추정 모형 재현이 아님. 357개 전수 수치 재검산은 기존 RF-A04에 의존하며 이번 표본 셀 재독과 구별. | 같은 경계 내부 이동을 총 유입·유출에서 제외해야 한다는 역할/범위 조건을 검사할 수 있음. 표면적으로 최종 출력이 같다는 이유로 입력·경계·중간 상태를 생략하면 대응을 잘못 판정함. |

### F02 정정의 근거와 영향

[현장 정정 원장](field/resume-field-correction.json)은 F01·F02 설명 수정 전 행과 파일 해시를 보존한다. 고정 PDF SHA256은 b3e6689d94b496817a35f072d175b5b4be9149429a87d8adcaf7c8ff5e904bcc다. 기존 캐시의 텍스트·로컬 렌더·동일 바이트 직접 재다운로드는 MTA Real Time 표기로 일치했고, 웹 screenshot은 해시를 제공하지 않은 GTFS 표기를 반환했다. 현장·후속 담당 판독은 [재개 감사의 확인 경로별 표](field/resume-field-audit.md)를 인용하며, 네트워크를 다시 요청하지 않았다.

이 정정은 ‘정적 시간표만 보았다’는 낮은 증거 분류를 바로잡는다. 그래도 DCP의 사후 집계 보고를 원시 실제 출발 로그와 동일시하지 않는다. 고정 검색 순위·적합 분자·원문 수·사건 수는 수정하지 않는다. 다음 자료는 2020-02-13·03-12·04-16 보존 feed, 당시 DCP 집계 코드, 예측과 실현 운행을 가른 규칙이다. 현재 API 페이지를 열어도 그 과거 판·분모가 복원되는 것은 아니다.

### F04에서 최종 출력만 비교할 때 놓치는 것

| 원문 좌표·지역 | v1 유입 / 유출 | v2 유입 / 유출 | 전후 순이동 J열 | 전후 인구 O열 |
| --- | --- | --- | --- | --- |
| MYE3!H9:O9, England and Wales | 3,768,798 / 3,778,598 | 47,924 / 57,724 | −9,800 | 60,238,038 |
| MYE3!H10:O10, England | 3,628,364 / 3,648,816 | 112,337 / 132,789 | −20,452 | 57,106,398 |
| MYE3!H11:O11, North East | 133,150 / 123,406 | 66,260 / 56,516 | 9,744 | 2,683,040 |
| MYE3!H12:O12, County Durham | 29,011 / 23,640 | 29,011 / 23,640 | 5,371 | 528,127 |

출처는 [v1 XLSX][f04-v1]와 [v2 XLSX][f04-v2]의 표시 좌표다. 워크북 정정 공지는 큰 지역 안의 이동을 총 유입·유출에서 제거해야 했으며 순이동과 인구 총계에는 영향이 없었다고 설명한다. 수치 대조는 이 설명을 MYE3 저장값 범위에서 뒷받침한다. 따라서 “같은 출력이면 같은 원리”라는 판정 규칙의 반례는 유지된다. 반례의 범위를 표의 모든 통계 추정이 틀렸다는 주장으로 넓힐 수는 없다.


## 6. 수신8건 후속: 승인·구현·인용·실제 채택

아래 표는 [현장·후속 상세 분석](analysis/field-and-followup.md)의 8건을 합성한 것으로, 최초 후속 조회는 검색 봉인 이후인 2026-11-22 17:14:22.179–17:14:28.621 UTC였다. 원 PR 병합5/미병합종료3을 설계 성공/실패 분자에 합치지 않는다. 정규 출처ID와 고정 최초본문 연결은 다음과 같다. OUT-*는 sources.jsonl의 후속 원문 ID이며 초기 설계 본문과 별개다.

| 수신 | sources.jsonl 최초본문 정규ID·고정 URL |
| --- | --- |
| R01 | [rust-lang-rfcs-pr-2843](https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md) |
| R02 | [rust-lang-rfcs-pr-2845](https://github.com/rust-lang/rfcs/blob/6fb5bd5a6132b15bfe2d9dade6a48d7a77eb2b24/text/0000-supertrait-item-shadowing.md) |
| R03 | [rust-lang-rfcs-pr-2850](https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md) |
| R04 | [rust-lang-rfcs-pr-2856](https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md) |
| R05 | [kubernetes-enhancements-pr-1438](https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md) |
| R06 | [kubernetes-enhancements-pr-1439](https://github.com/kubernetes/enhancements/blob/50f8b89cb8f0b3d10b1b0d5bc278122abbd23c84/keps/sig-cluster-lifecycle/wgs/20200108-instance-specific-componentconfig.md) |
| R07 | [kubernetes-enhancements-pr-1444](https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md) |
| R08 | [kubernetes-enhancements-pr-1450](https://github.com/kubernetes/enhancements/blob/2cef2aacc29238c4fffad906b429cedef2dba21d/keps/sig-scheduling/20200114-taint-based-evictions.md) |

현재 문서는 2026-11-22 17:19:27 UTC에 캡처한 가변 페이지다. OUT-DOC-*의 raw_sha256으로 이 판을 식별한다. 현재 문서가 설명하는 동작과 2020년 최초 설계의 모든 필수 조건을 같게 취급하지 않는다. ‘직접 인용 미확인’은 각 PR의 기계 검색 0건과 한정된 의미 판독을 뜻하며, 개인의 지식 부재를 뜻하지 않는다.

| 수신 ID·최초 목적 | 후속 결정과 정확 근거 | 구현·동작에서 실제 확인한 범위 | 제공 원리 직접 인용·채택 | 남는 미확인과 결론을 바꿀 첫 자료 |
| --- | --- | --- | --- | --- |
| R01 — asm! 이름을 바꾸되 기존 호출을 연결하고 이후 경고 | RFC #2843은 2020-03-20 병합. [수락 댓글 601564223][r01-accept]과 outcome-observations:R01 메타데이터. | [구현 PR #68404][r01-impl] 본문 두 번째 문단은 기존 asm!을 llvm_asm!으로 forwarding하되, stdarch 등 하위 모듈 이주 때문에 deprecation은 아직 하지 않는다고 명시. 2020-03-27 병합 메타데이터까지 확인. 원장 OUT-R01-rename-implementation. | 직접 제공 인용·인과적 채택 모두 미확인. 댓글/리뷰 36기록·32본문 및 현재 PR 본문에서 도메인 일치 0. 수락/구현은 제공 자료의 영향 증거가 아님. | 최초 요구의 경고 조건까지 완료됐다고 할 수 없음. 첫 자료는 수락 댓글이 연결한 [추적 이슈 #70173][r01-track]와 #68404 뒤의 실제 deprecation 변경·컴파일 진단 시험. 어느 릴리스에서 경고가 추가됐는지를 확인하면 단계 완료 판정을 바꿀 수 있음. |
| R02 — 하위 trait의 항목 선택과 명시적 충돌을 구분 | RFC #2845는 2021-09-21 병합. [댓글 720705642][r02-choice]는 supertrait 변경의 호환성 동기와 호출자 disambiguation을 지지. [댓글 910114408][r02-boundary]의 첫 답변 문단은 명시적 Sub + Super와 무관한 trait 충돌의 일관성·사용 지점의 문법을 논함. 원장 outcome-observations:R02. | 이 조사에서 컴파일러 구현 PR, 배포 버전, 실행 결과는 확인하지 않음. 현재 PR 본문과 승인 토론은 설계 의사결정 근거다. | 직접 제공 인용·인과적 채택 미확인. 40기록·40본문 및 현재 PR 본문에서 도메인 일치 0. 유사한 선택 규칙이 다른 분야에서 보인다고 기원을 확정할 수 없음. | 다음 첫 자료는 [병합된 RFC #2845][r02-pr]에서 연결되는 구현·추적 기록. implicit Sub, explicit Sub + Super, fully qualified 두 호출을 같은 고정 컴파일러에서 비교할 시험·출시 커밋이 필요. 병합 사실만으로 실행 의미가 모두 구현됐다는 결론은 달라지지 않음. |
| R03 — inline asm의 입력·출력과 lateout 재사용 경계 | 최초 #2850은 2020-03-03 미병합 종료. [댓글 593702000][r03-continue]은 긴 토론을 #2873으로 이어 간다고 명시. [후속 #2873][r03-replacement]은 2020-07-20 병합. 원장 outcome-observations:R03, OUT-R03-replacement-rfc. | [Rust Reference의 in/out/lateout 절][r03-doc]은 입력 초기값, 출력 목적지 복사, 모든 입력을 읽은 뒤에만 lateout 입력 레지스터 재사용을 설명. 원장 OUT-DOC-ASM, web-reader L333–414. 이 연구는 실행하지 않음. | 직접 제공 인용·인과적 채택 미확인. 최초 PR의 429기록·267본문 및 현재 PR 본문에서 도메인 일치 0. 현재 의미가 최초 일부 조건과 닮음은 독립 유사성을 보일 수 있으나 ‘독립 발생’을 입증하지도 않음. | 미병합 종료를 설계 거절로 세는 해석은 이미 반증됨. 다음 첫 자료는 #2873 본문이 연결한 [구현 #69171][r03-implementation]과 고정 버전의 allocator/compiletest. 2020년 전체 설계가 그대로 출시됐다는 주장은 여전히 미확인. |
| R04 — 프로젝트 그룹의 중단·보존·재개 | RFC #2856은 2020-05-21 병합. [수락 댓글 632236575][r04-accept]. [리뷰 404969272][r04-restoration]은 Restoration이 형성 단계를 생략하는 경로를 뜻하지 않는다고 설명. 원장 outcome-observations:R04. | 규칙의 채택은 확인. 실제 중단 그룹 한 곳의 저장소 보존·프라이버시 처리·연락 역할·상위 팀 합의·재개 사건은 추적하지 않음. | 직접 제공 인용·인과적 채택 미확인. 171기록·116본문 및 현재 PR 본문에서 도메인 일치 0. 통계의 보존/정정 공지가 이 governance 규칙의 기원이라는 근거는 없음. | 첫 자료는 [#2856 Restoration 토론][r04-restoration]에서 이름이 확인되는 실제 프로젝트 그룹의 중단/재개 공지와 해당 팀 회의록. 동일 그룹 ID의 중단일·read-only 저장·새 연락자/합의·재개일을 연결해야 실제 절차 적용 판정을 바꿀 수 있음. 이름이 예로 든 traits 그룹이 실제 이번 조건대로 재개됐다고 먼저 가정하지 않음. |
| R05 — mixed-protocol Service를 허용하되 제공자 능력에 맡김 | KEP #1438은 2020-07-14 병합. [리뷰 367654556][r05-gcp]은 API 필터를 제거하면 당시 GCP 구현이 첫 protocol을 모든 포트에 적용하고 오류를 알리지 않을 위험을 지적. [리뷰 445056251][r05-aws]은 UDP 지원을 넣은 AWS 구현도 mixed TCP/UDP에는 추가 작업이 필요하다고 지적. 원장 outcome-observations:R05. | [현재 Service 문서][r05-doc]의 mixed protocol 절은 API 허용과 cloud-provider 추가 제한을 함께 기술하고 1.26 이후 stable로 표시. 원장 OUT-DOC-MIXED, web-reader L1283–1291. 실제 cloud-provider 실행·패킷 시험은 하지 않음. | 직접 제공 인용·인과적 채택 미확인. 184기록·127본문 및 현재 PR 본문에서 도메인 일치 0. 수신 원문이 이미 알고 있던 API/제공자 경계를 후속에서 확인한 것임. | 첫 자료는 리뷰가 연결한 [AWS 변경 #92109와 discussion_r439730341][r05-aws-next], 이어 동일 Service의 TCP/UDP 각 포트 결과와 provider 버전이 있는 시험. API 객체 수락과 실제 프로토콜 노출이 갈릴 수 있으므로 ‘검증 완화=문제 해결’ 결론을 바꿀 수 있음. |
| R06 — 공유 설정과 인스턴스 설정을 나눔 | KEP #1439는 2021-07-09 미병합 종료. [댓글 763190786][r06-kyaml]은 KYaml 2-way merge 대안을 제안. [763476786][r06-semantics]과 [775880476][r06-spec]은 보조 라이브러리 구현에 API를 맡기기보다 병합 의미의 명세를 요구. [877198773][r06-close]은 rotten 비활성 종료. 원장 outcome-observations:R06. | 이 PR에서 API가 승인·구현됐다는 근거 없음. 논의된 대안과 lifecycle 종료를 확인했을 뿐 다른 경로의 구현 부재는 검사하지 않음. | 직접 제공 인용·인과적 채택 미확인. 165기록·123본문 및 현재 PR 본문에서 도메인 일치 0. 격리·인증 원리의 부분 유사성이 구성 필드 우선순위/보존 알고리즘을 제공하지 않음. | 첫 자료는 [763476786의 KYaml 명세 요청][r06-semantics]에 응답한 고정 알고리즘 문서·테스트. 두 Kind의 파일 혼합, 명령행 덮어쓰기, 원격 공유 갱신에서 로컬 값 보존 사례가 필요. 이를 갖춘 대체 구현이 나오면 ‘다른 경로는 미확인’에서 이동 가능. |
| R07 — AppArmor annotation에서 전용 필드로 넘어가는 버전 호환 | 최초 #1444는 2022-07-07 미병합 종료. [댓글 1178154542][r07-supersede]은 #3298이 대체한다고 말함. [#3298][r07-replacement] 본문도 supersedes #1444이나 현재 메타데이터는 2024-01-19 미병합 종료. 원장 outcome-observations:R07, OUT-R07-replacement-kep. | [현재 AppArmor 문서][r07-doc]는 appArmorProfile 필드와 1.30 이전 annotation API, 1.31 이후 stable을 설명. 원장 OUT-DOC-APP, web-reader L908–959. 최초의 7개 skew/변환/불변성 조건 전부가 그대로 배포됐다는 확인은 없음. | 직접 제공 인용·인과적 채택 미확인. 257기록·186본문 및 현재 PR 본문에서 도메인 일치 0. 기능 존재는 특정 초기 PR이나 통계 개정 원리의 채택을 증명하지 않음. | 첫 자료는 #3298이 연결한 [KEP 이슈 #24][r07-track]에서 실제 최종 병합판을 확인하고, 1.29–1.31 경계의 API/kubelet 변환·일치검사·annotation update·immutability 시험을 최초 7조건과 대조하는 것. N+4 보존 창은 따로 확인해야 함. |
| R08 — 기존 taint-based eviction을 동작 변경 없이 GA로 승격 | KEP #1450은 2020-01-20 병합. [추적 이슈 #87161][r08-tracking]은 2020-03-12 닫혔고 본문 Tasks의 KEP·시험·feature gate 정리·문서가 완료 체크되어 있음. 원장 outcome-observations:R08, OUT-R08-ga-tracking. | 유지관리자의 완료 기록과 연결된 작업을 확인. 이 연구가 클러스터를 실행해 기본 on 및 기존 동작 동일성을 검증한 것은 아님. | 직접 제공 인용·인과적 채택 미확인. 33기록·22본문 및 현재 PR 본문에서 도메인 일치 0. 단계 명칭 변경과 실제 상태 변화/수정은 다른 관계임. | 첫 자료는 #87161 Tasks가 연결한 [시험 #88152][r08-tests]와 [feature gate 정리 #87487][r08-gate]. 고정 1.18 빌드의 이전·이후 taint/tolerationSeconds 동작과 기본값 시험으로 ‘이 연구의 실행 미확인’을 줄일 수 있음. |

위 표에서 확인한 최초 PR 병합 5/8, 후속 대체 PR 중 병합 1/2 등의 수는 **후속 분류**다. 폐쇄 후보 18문서의 회수 성공률, 전이 적합 분자 또는 실제 웹 전체 검색 성능과 합산하지 않는다. 수신 팀의 직접 원리 인용 및 실제 채택은 8/8 미확인이다. ‘미확인’ 8건을 ‘채택하지 않은’ 8건으로 바꾸지 않는다.


### 공개 인용 문자열 검사와 의미 판독의 구별

[도메인 검사 영수증](evidence/followup-citation-screen.json)은 35개 입력 캐시에서 댓글·리뷰1,315기록 중 비어 있지 않은913본문 및 현재 PR 본문8개에 제공기관 도메인18개의 소문자 literal substring을 검사해 일치0건을 기록했다. 이는 별칭·간접 의미 인용·연결 구현 전체·비공개 대화·사전 지식의 검사 결과가 아니다. 현장·후속 분석의 제한된 의미 판독과 이 기계검사 범위를 합쳐 913본문의 독립 의미 판독으로 부풀리지 않는다. 적절한 결론은 정해진 공개 본문 범위의 제공기관 도메인 문자열 일치가 없었다는 것이다. 직접 제공 인용과 인과적 채택은 8/8 미확인이지, 미채택8 또는 독립 발명8이 아니다.

## 7. 후속·현장이 추가한 반증: FF-C 식별자 유지

FF-C01–FF-C08은 현장·후속 분석의 반례ID이며, 위 CE01–CE05의 수신×후보 대응ID와 별도다. 다음 경계 검사는 원 검색 순위나 144행 분자를 바꾸지 않는다.

| 반례 ID | 성급한 결론 | 맞지 않는 관측·정확 근거 | 현장·후속 분석이 유지하는 판정 |
| --- | --- | --- | --- |
| FF-C01 | 승인·병합됐으므로 최초 요구의 모든 조건이 구현됐다. | R01 [#68404 본문 두 번째 문단][r01-impl]이 deprecation을 명시적으로 미룸. | 승인, forwarding 구현, 경고 완료는 별도 단계. 경고 완료는 미확인. |
| FF-C02 | 최초 PR이 닫혔으므로 설계가 거절됐다. | R03 [593702000][r03-continue]과 #2873 병합, R07 [1178154542][r07-supersede]와 #3298의 대체 연결. | 종료 원인을 확인하고 대체 경로를 따로 기록. R07의 현 기능 존재로 #3298 병합을 꾸며내지 않음. |
| FF-C03 | API가 입력을 허용하면 제공자가 의미대로 실행한다. | R05 [367654556][r05-gcp]은 잘못된 protocol 적용과 오류 미고지 가능성을, [445056251][r05-aws]은 UDP 지원과 mixed 지원의 차이를 지적. | 수락 단계와 실행 책임을 분리. 실제 provider 시험 미확인. |
| FF-C04 | 원리 이름이나 구현 라이브러리를 찾으면 필요한 명세도 얻는다. | R06 [763476786][r06-semantics], [775880476][r06-spec]은 병합 의미 명세를 요구. | 모듈·원리 이름은 부분 단서일 수 있음. 우선순위와 불변조건의 핵심 설계가 남으면 완결로 올리지 않음. |
| FF-C05 | real-time 표기이므로 모든 실제 운행을 검증했다. | F02 [p13][f02]은 집계 보고이고 raw feed·집계 코드·실현 판별을 이 연구가 재실행하지 않음; RF-A02. | GTFS 오분류는 철회하되 사후 집계와 원시 운행 재현의 차이는 유지. |
| FF-C06 | 기록을 보존하고 공지했으므로 모든 소비자 상태가 복구됐다. | F03 [정정 배너/이전판][f03-current]은 발행자 쪽 변경·이력을 보여 줄 뿐 소비자의 상태 이력을 제공하지 않음. | 추적 가능성과 실제 전달/적용/회수 성공을 분리. 부재를 실패로 단정하지 않고 미확인. |
| FF-C07 | 최종 숫자가 같으므로 입력 경계와 과정도 맞는다. | F04 [v1][f04-v1] / [v2][f04-v2], MYE3 H/I 변경과 J/O 불변. | 출력 외에 입력·범위·상태·주체를 검토할 필요가 있다는 실제 반례. |
| FF-C08 | 공개 도메인 검색 0건이므로 수신 팀은 원리를 몰랐다. | [followup-citation-screen.json](evidence/followup-citation-screen.json)의 literal substring과 제외 범위. | 직접 제공 인용은 확인되지 않음. 사적 지식·간접 영향·독립 발생·실제 채택은 미확인. |

이 반례들은 서로 다른 경계를 공격한다. R01은 구현의 시간 단계, R05는 행위 주체의 능력, F03은 수정 권한과 downstream 반영, F04는 입력 경계와 출력 동일성이다. 따라서 한 가지 성공 요건으로 합쳐 성공률을 만들지 않는다. 같은 원리 후보라도 필요한 경계 조건이 달라지면 판정이 달라져야 한다는 검토 기준으로 쓴다.


FF-C03은 X01이 처음부터 가진 접수/실현 경계를 후속으로 재확인하지만 L06의 영향 증거를 추가하지 않는다. FF-C06은 CE03에 남는 실제 복원 절차를 보존/공지의 표면적 유사성으로 채울 수 없게 한다. FF-C07은 CE04처럼 입력 경계를 출력의 유사성만으로 생략할 수 없다는 점을 보강한다. F01/F02의 MTA 사건은 T02의 MBTA 정책이 실제로 시행됐음을 증명하는 사례가 아니다.

## 8. 별도5행 판독 일치와 민감도

[critical-review.jsonl](judgments/critical-review.jsonl)의 R05–L06 support, R01–T02 conflict, R04–L03 partial, R07–S03 conflict, R08–T06 conflict는 원 분야 판독과 **5/5 일치**했다. 당시 이 문맥은 실제 S/R 질의·질의별 순위·기존 판정·후속 결과를 보지 않고 고정 목표와 원문을 읽었고, 지금의 통합 작성은 그 뒤에 진행했다. 그러나 같은 모델의 별도 문맥이며 독립 인간 평가가 아니다. 초기 corpus 출력 범위가 넓어 제공 발견/선정 메타데이터와 고정 빈도 벡터가 노출된 사실은 [CR-A007](judgments/critical-review-attempts.jsonl)에 남아 있다. 완전 무노출이나 모델·사람 간 재현으로 주장하지 않는다. 선택된5행의 일치로 144행 전체의 신뢰도나 모든 가능한 매핑의 합의를 추정할 수 없다.

**R05 보수적 판독.** L06의 요청 불가 목록과 공급 가능성 목록 구별이 복합 책의 접수 허용을 함의한다고 인정한 것이 X01의 근거다. 명시적으로 복합 책을 접수한다는 별도 문장만 요구하면 partial이다. 그 민감도에서 strict eligible 수신 분모는 **1→0**, 적격 수신에 조건부인 양쪽 누락률은 **해당 없음**이다. 원8수신의 상위 엄격 완료0/8은 유지되고, 원장 support1/partial50/conflict9/unverified84는 수정하지 않는다. 최초 본문에 이미 있는 관계의 타 분야 인용 보완이라는 신규성 제한도 그대로다.

**R07 객체 정체성 판독.** 같은 참조기간 추정치를 같은 논리 객체로 대응하면 ABS 개정 절차는 immutable Pod field와 충돌한다. 각 vintage를 별개 새 객체로 놓으면 이 충돌이 약해져 partial로 볼 수 있지만 creation 네 분기·양방향 복사·N+4·annotation update 무시의 근거가 생기는 것은 아니다. [CE02 원 판정](judgments/statistics.jsonl)과 [별도 판독](judgments/critical-review.jsonl)은 민감도를 기록하면서 기본 판정을 유지한다.

**R04 보존 범위 판독.** L03의 6개월 계정 삭제를 기관의 모든 기록 파기로 확대하지 않았다. 유일 공개 보존본이라는 추가 동일시를 해야 강한 충돌을 만들 수 있어 주 판정은 partial이다. 공개 archive와 승인된 동일 그룹 복원이라는 미충족 핵심을 무단으로 추가하여 support로 만드는 것도 허용하지 않는다.

## 9. 인계: 무엇을 알았고 무엇이 더 필요한가

이번 실행의 유일한 현재 관계 지지는 수신에 이미 적힌 경계의 타 분야 인용 보완이다. 새 아이디어 도입의 성공 사례로 쓰지 않는다. 폐쇄 후보18·독립 수신8·이 검색기에서 엄격 상위 인용 성공이 관측되지 않았다는 결과는 웹 전체 탐색의 불가능성이나 모든 관계 표현의 무용성을 뜻하지 않는다.

다음 최소 판별 자료는 X01의 복합 책 단일 접수/전달을 명시하는 공식 절차, R01 warning 완료 변경, R07 최종 변환/불변성 규약, 실제 R04 그룹의 승인된 재개 기록, F02의 과거 보존 feed와 집계·실현 판별 규칙이다. 실제 채택을 주장하려면 제공 문서ID·인지 시점·결정 변화가 연결된 공개 설계 기록 또는 참여자 확인이 필요하다. 이번 작성은 이런 자료를 새로 찾지 않았고 원 검색을 수정하지 않았다.

검증 범위는 Q7의 X01/CE01/CE03 각3관점=9행, 정규 출처ID와 양측 URL/행/해시 조인, 원 순위·실제 반환창 대조, 기존5행 판독의 일치 확인이다. 두 산출물 외의 보호된 입력·원장·순위·판정 파일의 해시를 대조했다. JSON·ID·경로 검사는 의미 타당성이나 인간 검증의 인증이 아니다.

[seal]: https://github.com/laadkke-arch/agentflow-open/commit/a2ce15d10415c556574d1a65af77718a81052d01
[r01-accept]: https://github.com/rust-lang/rfcs/pull/2843#issuecomment-601564223
[r01-impl]: https://github.com/rust-lang/rust/pull/68404
[r01-track]: https://github.com/rust-lang/rust/issues/70173
[r02-pr]: https://github.com/rust-lang/rfcs/pull/2845
[r02-choice]: https://github.com/rust-lang/rfcs/pull/2845#issuecomment-720705642
[r02-boundary]: https://github.com/rust-lang/rfcs/pull/2845#issuecomment-910114408
[r03-continue]: https://github.com/rust-lang/rfcs/pull/2850#issuecomment-593702000
[r03-replacement]: https://github.com/rust-lang/rfcs/pull/2873
[r03-implementation]: https://github.com/rust-lang/rust/pull/69171
[r03-doc]: https://doc.rust-lang.org/reference/inline-assembly.html#asm.operand-type.supported-operands-lateout
[r04-accept]: https://github.com/rust-lang/rfcs/pull/2856#issuecomment-632236575
[r04-restoration]: https://github.com/rust-lang/rfcs/pull/2856#discussion_r404969272
[r05-gcp]: https://github.com/kubernetes/enhancements/pull/1438#discussion_r367654556
[r05-aws]: https://github.com/kubernetes/enhancements/pull/1438#discussion_r445056251
[r05-aws-next]: https://github.com/kubernetes/kubernetes/pull/92109#discussion_r439730341
[r05-doc]: https://kubernetes.io/docs/concepts/services-networking/service/#load-balancers-with-mixed-protocol-types
[r06-kyaml]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-763190786
[r06-semantics]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-763476786
[r06-spec]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-775880476
[r06-close]: https://github.com/kubernetes/enhancements/pull/1439#issuecomment-877198773
[r07-supersede]: https://github.com/kubernetes/enhancements/pull/1444#issuecomment-1178154542
[r07-replacement]: https://github.com/kubernetes/enhancements/pull/3298
[r07-track]: https://github.com/kubernetes/enhancements/issues/24
[r07-doc]: https://kubernetes.io/docs/tutorials/security/apparmor/#securing-a-pod
[r08-tracking]: https://github.com/kubernetes/kubernetes/issues/87161
[r08-tests]: https://github.com/kubernetes/kubernetes/pull/88152
[r08-gate]: https://github.com/kubernetes/kubernetes/pull/87487
[f01]: https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8
[f02]: https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf#page=13
[f03-v1]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v1
[f03-v2]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v2
[f03-current]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/
[f04-index]: https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires
[f04-v1]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv1%2Fmye22tablesew2023geogs.xlsx
[f04-v2]: https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpopulationandmigration%2Fpopulationestimates%2Fdatasets%2Festimatesofthepopulationforenglandandwales%2Fmid20222023localauthorityboundaires%2Fprevious%2Fv2%2Fmye22tablesew2023geogsv2.xlsx
[R01-initial]: https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md
[R04-initial]: https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md
[R05-initial]: https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md
[R07-initial]: https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md
[R08-initial]: https://github.com/kubernetes/enhancements/blob/2cef2aacc29238c4fffad906b429cedef2dba21d/keps/sig-scheduling/20200114-taint-based-evictions.md
[L03]: https://multcolib.org/interlibrary-loan
[L06]: https://www.vpl.ca/borrowing/interlibrary-loans
[T02]: https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf
[S03]: https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/australian-system-national-accounts-concepts-sources-and-methods/edition-8/chapter-24-quality-national-accounts/revisions
[T06]: https://www.sfmta.com/media/33758/download?inline
