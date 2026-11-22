# 교통 제공 문서 전수 판독 노트

## 범위와 판독 결과

질의 없는 `recipient/recipient_targets.jsonl`의 8개 고정 최초 원문과 `corpus.jsonl`의 transport T01–T06 전체 선택 본문을 직접 읽어 48개 대응을 판독했다. `transport.jsonl`에는 48개 고유 pair, 고정 부분 목표의 168개 mandatory 판정, 양측 고정 URL·줄·PDF 위치, 입력/변화/출력/역할 대응, 남는 접합과 새 핵심, 깨지는 조건을 남겼다. 공통 입력·원장·git은 수정하지 않았다.

엄격한 고정 부분 목표의 **support는 0/48**, 부분 단서는 19/48, 구체 대응에서 명시적 충돌은 2/48, 미확인은 27/48이다. mandatory 원자 단위에서는 local match 3/168, conflict 2/168, missing 163/168이다. 세 local match는 R04-M06의 가역 중지 상태에 대한 T02/T06 대응과 R05-M01의 혼합 서비스 허용에 대한 T04 대응이다. 나머지 mandatory와 결합하지 못하므로 pair support를 뜻하지 않는다. 소재가 다르다는 이유로 탈락시키지 않았고, 기능의 부재를 금지나 충돌로 바꾸지 않았다.

| 수신 | T01 | T02 | T03 | T04 | T05 | T06 | 합계 support / partial / conflict / unverified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | partial | conflict | unverified | unverified | unverified | unverified | 0 / 1 / 1 / 4 |
| R02 | partial | partial | partial | partial | unverified | unverified | 0 / 4 / 0 / 2 |
| R03 | partial | unverified | unverified | partial | unverified | unverified | 0 / 2 / 0 / 4 |
| R04 | partial | partial | partial | unverified | unverified | partial | 0 / 4 / 0 / 2 |
| R05 | partial | partial | unverified | partial | unverified | unverified | 0 / 3 / 0 / 3 |
| R06 | partial | partial | unverified | partial | unverified | unverified | 0 / 3 / 0 / 3 |
| R07 | unverified | unverified | unverified | unverified | unverified | unverified | 0 / 0 / 0 / 6 |
| R08 | unverified | unverified | partial | unverified | partial | conflict | 0 / 2 / 1 / 3 |

전체 설계는 별도 필드로 판정했다. 여기의 partial은 전체 설계를 완성한다는 뜻도 아니다. 완결되지 않은 부분 관계만 남고 더 큰 언어/API/인프라 설계는 새로 필요하다. 순위·검색 질의·반환 창을 전혀 보지 않은 전체 문서 판독이므로 이 숫자를 상위 검색 적중 수나 실제 웹 회수율로 사용하면 안 된다. 원 반환과 근거 창의 완결 여부는 root가 이후 별도 조인한다.

기술 명칭이 그대로 있는지를 적합 기준으로 삼지 않았다. macro·Kind·CLI 등의 단어는 수신 원문의 조건을 지칭하는 표지다. 입력 객체, 상태 변화, 출력, 권한 관계가 대응하면 분야별 자료형과 이름은 접합으로 다룬다. R05-T04 M01은 이런 구조적 일치를 인정한 예다. missing은 문서에 특정 프로그래밍 API가 없다는 이유가 아니라 필요한 상태·권한·갱신 경계의 원문 근거가 부족하다는 판정이다.

## 변별력이 있는 원문 대응

| pair | 직접 확인한 관계 | 완결을 막는 경계 | 근거 |
| --- | --- | --- | --- |
| R03-T01 | 다른 기관이 서비스 필요를 채우고 잔여 운행 시간이 생긴 경우 재배치한다. 자원 해제의 조건을 먼저 보라는 단서다. | 전체 입력의 마지막 read 완료, early output의 독점, 초기 값 적재와 결과 복사가 없다. | T01 L503–525, 인쇄 20쪽 / 물리 24쪽; R03 L128–164, L336–360 |
| R03-T04 | 승하차 반복으로 동일 공간이 누적 이용된다. | PE.3은 측정 지표다. 지표에서 안전한 할당·쓰기 시점 규칙을 만들어 내면 안 된다. | T04 L1836–1861, 인쇄 44쪽 / 물리 46쪽; R03 L132–164, L345–360 |
| R02-T03 | Tier 1은 Tier 2 조건을 모두 충족한 뒤 추가 조건을 검사한다. | 조건의 논리곱은 암묵 상위 동명 항목을 숨기는 resolver와 다르다. 명시적 충돌 오류와 자격화 우회도 없다. | T03 L137–170, L180–207, 인쇄 24–25쪽 / 물리 25–26쪽; R02 L137–179, L315 |
| R05-T04 | 서비스 유형은 모드와 독립적이고 FTN 목표는 복수 유형의 결합으로 충족할 수 있다. | 복수 유형 결합의 수용은 국소적으로 일치한다. accepted object를 별도 provider/controller로 넘기는 단계는 없다. | T04 L201–212, L256–268, 인쇄 7·9쪽 / 물리 9·11쪽; R05 L98–117, L261 |
| R04-T02 | 접근 가능한 대체 stop을 만들지 못하면 역을 생략하고 조건 변화에 따라 복귀 여부를 재검토한다. | read-only 저장소/통신 보존과 재개 담당자·parent-team 합의가 없다. | T02 L105–119, 인쇄/물리 3쪽; R04 L112–144 |
| R04-T06 | 중단된 노선의 일부/전체 재도입과 자원 제약·수요 재검토가 기록된다. | 산출물·대화 보존, private 회고 제외와 재개 책임·합의 규칙은 없다. | T06 L21–65, L161–172, L239–256, 물리/인쇄 3–4·6–9쪽; R04 L112–144 |
| R08-T03 | 충분한 시험·평가 뒤 성공한 서비스를 정규 체계로 편입하도록 권고한다. | default flag만 바꾸고 기존 기능을 그대로 유지한다는 계약은 없다. | T03 L348–367, 인쇄 28–29쪽 / 물리 29–30쪽; R08 L55–71 |
| R01-T02 | 대체 서비스가 기존 이용자를 다른 수단으로 연결한다. | 1:1 대체를 보장하지 않고 역을 제외할 수도 있어, 이 대체를 동일 동작의 forwarding으로 쓰면 M01과 충돌한다. | T02 L14–33, 인쇄/물리 1쪽; R01 L9–10, L31–33 |
| R08-T06 | 종전 네트워크의 복원을 새 서비스 기준선으로 삼는 대응을 검사했다. | 실제 수정·신규 노선이 있으며 재원이 전부 복원되어도 같지 않을 가능성이 높다는 설명이 있다. 기능 무변경 M02와 이 구체 대응에서 충돌한다. | T06 L53–65, L239–256; R08 L55–57, L70–71 |

표의 모든 T URL과 모든 수신 고정 blob URL은 아래 원문 목록 및 각 JSONL 행에서 다시 찾을 수 있다. 부정/미확인 행에 붙은 제공 위치는 가까운 절을 확인한 위치이며, 부재 자체의 긍정 증거라는 뜻은 아니다. 전체 고정 본문을 읽은 뒤 필요한 관계를 못 찾았다는 범위를 보존했다.

## 넓은 읽기와 강도 민감도

다음 세 행을 넓게 읽으면 partial로 둘 수 있지만 본 판독은 unverified로 남긴다. 기능 무변경·last-use 배리어·휴면 대상 동일성 같은 수신 경계를 문서 밖에서 넣어야 하기 때문이다. 이 민감도에서 partial은 19→22, unverified는 27→24, conflict 2와 support 0은 그대로다.

| pair | 넓은 읽기가 가져오는 단서 | 본 판독에서 부족한 관계 |
| --- | --- | --- |
| R03-T03 | 감축 예산을 증편 비용과 비교해 재배치한다. | 정적 비용 비교이며 이전 사용의 마지막 시점과 새 사용의 안전한 시작 조건이 없다. |
| R03-T06 | 일정한 재원에서 한 곳의 감편으로 다른 곳의 증편을 상쇄한다. | 미래 계획 제약이지 실제 자원 인계·입력 소비 완료를 증명하는 절차가 아니다. |
| R04-T05 | 노선 퇴역을 주요 결정으로 분류하고 공개 분석을 남긴다. | 같은 대상의 가역 archived 상태, 보존된 작업 공간과 재개 경로가 없다. |

R04-M07에서 outputs/process 계정을 남기는 하위절은 수신 최초 원문 L125–129의 권고 표현과 L348–350의 완곡한 의무를 포함한다. 이를 mandatory로 고정한 강도가 원문보다 센 문제를 기록한다. **그 하위절만 preference로 낮추는 민감도에서는 T01–T06 여섯 판정이 모두 변하지 않는다.** 공개 중지 통지, repository/communication read-only archive, private retrospective 제외라는 남은 M07 요건과 M08의 책임자·parent-team 합의가 충족되지 않는다. T04/T05에는 동일한 휴면 단위의 가역 상태도 없다. 고정 입력을 고치지 않고 각 행의 `r04_m07_recommendation_sensitivity`에 이 결과를 적었다.

## T04의 다단 편집과 PDF 대조

고정 원 PDF를 PyMuPDF로 직접 렌더해 물리 8, 10, 11, 16, 25, 32, 39, 46쪽을 보았다. 줄 위치는 원 corpus의 Poppler `pdftotext -layout` 추출을 그대로 사용한다. 재추출 stdout의 페이지 구분을 활용해 고유 줄로 PDF 위치를 붙였으며, 원 corpus/본문/해시는 바꾸지 않았다.

| 물리 / 인쇄 페이지 | 고정 본문 줄 | 시각적으로 확인한 구조와 판정 영향 |
| --- | --- | --- |
| 8 / 6 | L164–195 | 연간 성과 검토, 투자 계획, 지역 계획의 세 병렬 열이다. 이를 순서대로 실행하는 중단→보존→재개 절차로 만들지 않았다. |
| 10 / 8 | L214–244 부근 | 서비스 유형 표와 Special 설명 상자가 분리되어 있다. 모드와 서비스 유형을 같은 축으로 취급하지 않았다. |
| 11 / 9 | L256–268 | 왼쪽 FTN의 복수 유형 결합과 15분 기준을 위에서 아래로 읽는다. 중간 SkyTrain·오른쪽 B-Line의 설명, 특히 브랜드 갱신 문장은 별개다. |
| 16 / 14 | L529–552 | 본문은 지역 맥락에 따라 지침을 적용하며 공식을 강제하지 않는다는 설명이다. 오른쪽 reference 상자를 본문의 다음 단계로 붙이지 않았다. |
| 25 / 23 | L923–971 | load-factor 표의 Special 행은 NightBus·SeaBus·WCE 각각 다른 방식이다. SeaBus의 고정 법정 용량과 WCE의 별도 capacity 평가를 구분했다. |
| 32 / 30 | L1257–1281 | 왼쪽 정시성/배차 규칙성과 오른쪽 저빈도 timed-transfer sidebar가 다르다. timed-transfer를 모든 서비스의 동시성 배리어로 확대하지 않았다. |
| 39 / 37 | L1555–1589 | 노선 중복 회피와 경로 일관성은 병렬 원칙이다. 왼쪽 간격 논거와 오른쪽 예외 경로를 하나의 조건문으로 연결하지 않았다. |
| 46 / 44 | L1836–1861 | PE.3은 좌석/공간의 누적 재사용을 설명하는 turnover 지표다. 승하차 인계 제어의 실행 규칙은 아니다. |

L344–503 부근의 문서 구성 예시는 뒤의 실제 지침 페이지 일부를 축소 재현한다. 고유 외부 원문은 여전히 한 건이며 본 판독은 가능한 실제 해당 절의 뒤쪽 위치를 사용했다. 원 검색 표현에 들어 있는 내부 반복을 삭제하지 않았다. T04 재추출 때 `Invalid Font Weight` 경고가 64줄 나왔으나 명령 종료는 0이었고 핵심 구간을 위 페이지 렌더로 확인했다. 경고를 무시하고 표를 자동 선형 절차로 해석하지 않았다.

T02의 고정 본문 첫 줄에 표제가 남아 있는 불일치는 그대로 보존했다. 제목 제거에 따른 검색 민감도는 root의 별도 작업이며, 이 판독은 원 corpus의 본문을 사용했다.

## 시간·관측·신규성의 범위

수신 최초 제안은 모두 2020년 1월이다. 고정 교통 판 가운데 당시 발행된 것은 **T04(2018-06) 하나, 즉 8개 대응**이다. T04의 현재 전이 판정은 partial 4, unverified 4이며 support 0이다. T01(2021-11-17), T02(2026-09-01로 원장 고정; URL에는 2026-09-16 표기), T03(2024-05), T05(2025-09), T06(2022-12-27)는 모두 늦은 판이므로 나머지 40개를 당시 이용 가능한 근거로 세지 않았다. 이 날짜의 작은 정밀도 차이는 2020년 이전/이후 구분을 바꾸지 않는다. 더 이른 판이 존재한다는 언급만으로 고정 판을 소급하지 않았다.

T06은 과거 운행 관측, 아직 완료하지 않은 2022 네트워크 계획, 재정 시나리오가 한 본문에 있다. L21–26과 L239–241의 중단·일부 재도입은 과거 서술, L34–61의 82%/93%는 예정 변경이 완료된 뒤의 추정치, L161–172의 2024 완료 예상과 재정 문제는 그 판 시점의 전망이다. 전부 실제 완료 성과로 세지 않았다. T01–T05는 주로 지침·정책이며 절차가 모든 현장에서 성공했다는 검증과 구분한다. 별도 field 감사 산출물은 그대로 보존했다.

모든 최초 수신 본문에서 후보 정확 URL과 발행자 이름을 대조한 결과 해당 문자열의 인용은 없었다. 이는 최초 본문에서 확인되지 않는다는 제한된 신규성이다. 작성자가 해당 원리/분야를 몰랐다는 증거도 아니고 새 알고리즘의 발명 주장도 아니다. 수신 PR 후속 결정·구현은 열지 않았으므로 실제 채택은 미확인으로 남겼다.

## 판독자와 검산

별도 모델 문맥의 판독이다. 문서 수집자·질의 작성자의 같은 문맥 자체 재검과는 구별되지만 독립된 인간 실험이나 서로 다른 학습 모델의 독립 평가로 주장하지 않는다. 표시 모델은 개발자 지침의 GPT-6 Astra Pro이며 내부 runtime model ID는 별도 관측하지 않았다. 질의 문자열·순위·반환 receipt·수신 후속은 읽지 않았다.

자동 검산 결과: 48행/48 고유 pair, 수신별 6행, 제공별 8행, 168 mandatory, ID 누락 0, 중복 predicate 0, 범위 밖 줄 0, provider 범위 조인 누락 0, 빈 PDF locator 0, 최초 URL/발행자 문자열 인용 0. 수신 8개 raw SHA와 교통 6개 body/raw SHA를 고정 메타데이터와 다시 비교해 모두 일치했다. JSONL의 판단은 사람 검증이 아닌 동일 작성자의 구조 재검이다. 실행·해시 영수증은 `transport-attempts.jsonl`에 있다.

## 고정 원문 URL

- **T01** King County Metro Service Guidelines: https://cdn.kingcounty.gov/-/media/king-county/depts/metro/documents/about/policies/2021-11-17-metro-service-guidelines.pdf?hash=6CEF5D1B785F7119A8A02D92A7C70E77&rev=d5a012b52b0b47ba8e477c46bd9f1969 — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T01-body.txt, 인쇄 8–22쪽.
- **T02** MBTA Diversion Service Standards for Subway, Regional Rail and Ferry: https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T02-body.txt, 인쇄 1–5쪽.
- **T03** TTC Service Standards: https://cdn.ttc.ca/-/media/Project/TTC/DevProto/Documents/Home/About-the-TTC/Projects-Landing-Page/Transit-Planning/Service-Standards_May-2024.pdf?rev=6c96a85cc0a64147ad424f949dabce64 — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T03-body.txt, 인쇄 21–29쪽.
- **T04** Transit Service Guidelines: https://www.translink.ca/-/media/translink/documents/plans-and-projects/managing-the-transit-network/transit-oriented-communities/transit-services-guidelines-public-summary.pdf — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T04-body.txt, 인쇄 2–53쪽.
- **T05** TriMet Title VI Program 2025 Update: https://trimet.org/civilrights/pdf/titlevi-program-2025.pdf — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T05-body.txt, 인쇄 24–30쪽.
- **T06** Fiscal Year 2022-23 Short Range Transit Plan — Narrative: https://www.sfmta.com/media/33758/download?inline — 고정 선택 본문 docs/workstreams/research/AF-RES-033/donor/cache/TRANSIT-T06-body.txt, 인쇄 2–10쪽.

- **R01** llvm_asm: https://github.com/rust-lang/rfcs/blob/d5fe87812fc95f2699e770993848179b6c071f2c/text/0000-llvm-asm.md
- **R02** supertrait_item_shadowing: https://github.com/rust-lang/rfcs/blob/6fb5bd5a6132b15bfe2d9dade6a48d7a77eb2b24/text/0000-supertrait-item-shadowing.md
- **R03** asm: https://github.com/rust-lang/rfcs/blob/5559913ccacbe1e6c6c5d26d33a08f9b09641c5e/text/0000-inline-asm.md
- **R04** Project Group RFC: https://github.com/rust-lang/rfcs/blob/c80e28415d8a7f94448661badb963d3d6fc9efb2/text/0000-project-groups.md
- **R05** Different protocols in the same Service definition with type=LoadBalancer: https://github.com/kubernetes/enhancements/blob/6d97b64e59854ec7744d8bc3bfb9fadac29b52fe/keps/sig-network/20200103-mixed-protocol-lb.md
- **R06** Instance-Specific ComponentConfig: https://github.com/kubernetes/enhancements/blob/50f8b89cb8f0b3d10b1b0d5bc278122abbd23c84/keps/sig-cluster-lifecycle/wgs/20200108-instance-specific-componentconfig.md
- **R07** AppArmor to GA: https://github.com/kubernetes/enhancements/blob/63f35ac4f5d381ffae6bb5f9bacd67dfd93ba7a7/keps/sig-node/20200110-apparmor-ga.md
- **R08** Promote Taint Based Evictions to GA: https://github.com/kubernetes/enhancements/blob/2cef2aacc29238c4fffad906b429cedef2dba21d/keps/sig-scheduling/20200114-taint-based-evictions.md

## 후속 조인의 첫 행동

`pair_id`로 원 순위·실제 반환 창을 조인하고 `provider_evidence_line_ranges`의 필요한 구간이 그 창 안에 있는지 확인한다. 전체 본문 판독의 partial을 창 안에서 인용 완료된 성공으로 자동 올리지 않는다. 이 48행에는 strict support가 없으므로 순위가 바뀌어도 교통 고정 목표의 완결 지지 수는 0이다. 부분 단서의 인용 가능성, 두 경로가 모두 놓친 후보, 기간 부적격 문서의 영향은 별도로 집계해야 한다.
