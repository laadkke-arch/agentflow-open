# 재개 제공 원문·추출 감사

## 범위·판독자

검토자: `/root/donor_audit`, 부모와 별도 모델 문맥. 수신 최초 본문·조건·S/R 질의·순위·수신 후속 결말을 읽지 않았다. `AGENTS.md`, `SCOPE.md`, 제공 corpus/선정/추출 자료만 사용했다. 독립 사람 평가나 다른 학습 모델의 판독은 아니다. 원 corpus·원장·코드·후보 집합을 수정하지 않았다.

검사 기준은 원격 봉인 `aba0565e5d992dc358c9c7913b2ad7868248db8d`의 corpus다. `corpus.jsonl` SHA256은 `8fefde80d6177674b14c90818e6c7a95e9a28e232f07edb87ed14d6b44c3df13`이며 현재 파일과 동일하다. 캐시는 이 checkout의 `donor/cache/`에 있고 각 행의 `cache_text_path`/`cache_raw_path`가 정확한 경로다. 캐시는 gitignored이며 해당 원격 tree에 전체 원문 캐시가 커밋되지 않았음을 확인했다.

## 확인 결과와 범위 불일치

18개 선택 원문은 분야별6개, 고유 source_id/URL/body hash 각각18개다. 모든 원표현 SHA·검색본문 SHA가 봉인값과 일치했고 `retrieval.features()`로 재계산한 문서/190창 feature는18개 모두 일치했다. 이는 신원·바이트·점수 재현 확인이며 의미적 전이의 정답 인증은 아니다.

**T02의 제목 한 행이 실제 검색본문에 남아 있다.** `cache/TRANSIT-T02-body.txt` 첫1행은 MBTA 문서의 표제이며 원 PDF 첫행과 같다. corpus의 selection_boundaries는 문서 제목을 제거했다고 기록했으므로 SCOPE의 제목 제외와 불일치한다. 사후 파일변조는 아니고 봉인된 feature에도 이미 포함돼 있었다. 원 시험을 보존하고 별도 제목 제외 민감도로 실제 영향만 계산해야 한다. 아직 질의나 순위를 보지 않았으므로 어느 경로에 유리한지, 상위3이 바뀌는지, 엄격 인용완료가 바뀌는지는 이 감사에서 주장하지 않는다.

18개 모두 첫 본문 블록 및 전체 본문의 독립 제목 문자열을 검사했다. T04의272–273행에도 문서명과 같은 문자열이 있지만 chapter2 구분면이며 직전2와 다음2.1/2.2를 통해 내부 절 제목임을 확인했다. SCOPE는 내부 절 제목을 유지하므로 T02와 구별한다. 나머지16개에는 독립 문서표제 잔존을 발견하지 못했다. 원문 안에서 문서명 자체를 설명·참조하는 문장은 제목 제거 대상으로 삼지 않았다.

### T02 민감도 입력의 정확한 조작

- 원문 URL: https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf
- 원 PDF SHA256: `306a9be24254f9ae3ac3537600dd1060e718c4a6692d7db87972ef170eeed937`
- 봉인 검색본문 SHA256: `47823d149875937c6383fa6499cc06be2cd16bb69836b7cff097fcdfe3c16815`
- 제거: 첫1행과 그 뒤 LF만 제거한다. UTF-8 69바이트, raw token 10개, stopword제거후 8개. 다른 공백·본문·순서는 바꾸지 않는다.
- 해당 조작 뒤 본문 SHA256: `72dfab28a68a892641bf7c84d85cd09900b1e6a459f2754931b8ae62e23d7afe`. 이 민감도 body는 계산만 했고 별도 파일로 만들거나 원본문을 덮어쓰지 않았다.
- `features()`를 다시 계산해야 한다. 문서길이뿐 아니라 200토큰 창 경계가 이동하므로 원창의 완결 판정을 그대로 복사하면 안 된다. 원16회 검색과 별도 비용·별도 결과로 기록한다.

## 최초 목록·중복·판 검토

다섯 candidate manifest의30개 초기/디렉터리/판 확인 프레임·424후보행을 NFKC·공백정리·소문자 제목·URL 순서로 재계산했고 정렬 불일치는 없었다. 그중 최초 발행처18프레임은55후보행(교통22)을 가진다. 424는 반복 판·표현·디렉터리 링크를 포함한 발견행 수이며 고유 원문 수가 아니다. 발행처원장24행은 주18곳선정+미개봉대체6곳이다. 제공 source ledger36행 중18개만 counted_minimum=true다. 제외·구판·다른 표현은 최소수에 추가하지 않는다. 이 검사는 실제 저장된 유한 목록의 순서를 확인한 것이며 검색엔진이 반환하지 않은 사이트 전체의 완전성을 확인하지 않는다.

원문 전체 의미 재판독을 중복하지 않았다. 아래 표는 이번 감사에서 실제로 다시 읽은 범위를 기록한다. 특히 T01/T03/T04는 전체 바이트·feature를 검증하되 의미 내용은 표시한 범위만 집중 재독했다. 이전 제공 수집자의 전체 읽기 기록과 이번 감사의 재독 범위는 구별한다.

| ID | 이번 직접 재독 위치 | 확인한 내용·경계 | 제목 판정 | 원문 |
| --- | --- | --- | --- | --- |
| L01 | 1–31 전체 | 요청 횟수 제한·불가 자료·요청/확인 경로. 접수 상태를 말하지만 전 과정 승인·회수 규약은 제공하지 않는다. | 본문 설명으로 시작; 문서 제목 없음 | [공식 원문](https://www.spl.org/books-and-media/interlibrary-loans) |
| L02 | 1–70 전체 | 접수와 도착 이후 계정의 경계, 미처리 요청만 수령지 변경, 취소 시 활성 종료, 대여기관의 갱신 권한. | 본문 설명으로 시작; 문서 제목 없음 | [공식 원문](https://denverlibrary.org/ILL) |
| L03 | 1–219 전체 | 상태표시·In process 취소·계정 병합·연체 후 신규 제한·대여기관 재량을 모두 확인했다. 소유목록은 대여 약속이 아니다. | 계정 절로 시작; 문서 제목 없음 | [공식 원문](https://multcolib.org/interlibrary-loan) |
| L04 | 1–49 전체; 웹리더191–239 | 기관 이용 지침이며 개인 이용 지침과 구분한다. 대여제한·상호요금·다른 코드의 OTP 처리만 확인되며 개명 절차가 아니다. | 대상 이용자 설명으로 시작; 문서 제목 없음 | [공식 원문](https://tpl.ca/using-the-library/services/interlibrary-loan/interlibrary-loan-information-for-other-libraries/) |
| L05 | 1–39 전체 | 계정 자격·없는 서지의 빈 양식·성공 알림/실패 메모가 있다. 전체 협력기관의 실시간 상태보장은 없다. | 계정 절로 시작; 문서 제목 없음 | [공식 원문](https://www.hclib.org/about/borrowing/mnlink-instructions) |
| L06 | 1–136 전체 | 상한비용 초과 취소·가용 통지 뒤 수령지 변경 금지·취소 후에도 운송 중 비용 부담. 상단 승인/총기간 추정은 동일 값이 아니다. | 주의문으로 시작; 문서 제목 없음 | [공식 원문](https://www.vpl.ca/borrowing/interlibrary-loans) |
| S01 | 1–81 전체; §§1–6 | 공표 시각·일정 변경 설명·정정 배너·요청자료 동시 공개·예외적 사전 접근을 구분. 정정 상세정책은 별도 링크다. | §1 내부 제목 유지; 문서 제목 없음 | [공식 원문](https://www.ons.gov.uk/aboutus/transparencyandgovernance/releasepracticepolicy) |
| S02 | 1–29 전체; Technology/Process/Need-to-know | 격리 환경·고유 식별·접근 추적·사전동의·제한된 역할과 사전 공개 금지. 공식 정책 자체와 그 공개 설명문은 다르다. | 본문 설명으로 시작; 문서 제목 없음 | [공식 원문](https://www.statcan.gc.ca/en/trust/revisions-policy-official-release) |
| S03 | 1–79 전체; ¶24.107–24.131 | 추정 개정은 오류와 동의어가 아니며 정상 개정창/역사 개정/계절재분석의 범위가 다르다. 구판·절은 별도 원문 수로 세지 않는다. | ¶24.107로 시작; 전체 매뉴얼 제목 없음 | [공식 원문](https://www.abs.gov.au/statistics/detailed-methodology-information/concepts-sources-methods/australian-system-national-accounts-concepts-sources-and-methods/edition-8/chapter-24-quality-national-accounts/revisions) |
| S04 | 1–5 전체 | 오류 알림·정정 완료/예정·작고 결론을 바꾸지 않는 오류의 미정정 예외. 프로그램별 세부 구현은 제공하지 않는다. | 본문 설명으로 시작; 문서 제목 없음 | [공식 원문](https://www.bls.gov/about-bls/bls-error-correction-policy.htm) |
| S05 | 1–5 전체 | 중요성·시점·출처·새 자료에 따른 정정 통지/정기개정 선택, 작은 표 오류의 셀 지정, 다음 공표까지 통지 유지. | 본문 설명으로 시작; 문서 제목 없음 | [공식 원문](https://www.bea.gov/about/policies-and-information/correction) |
| S06 | 1–67 전체; embedded PageBlocks | 공표 책임자·동등 접근·사전 일정·적시성 원칙, 효력일2026-03-31. 연결된 embargo 절차는 본문 밖이다. | FeaturedText로 시작; 문서 제목 없음 | [공식 원문](https://www.stats.govt.nz/about-us/legislation-policies-and-guidelines/release-practices-policy/) |
| T01 | 1–98 집중 재독; 전체594행 해시/feature검증; 인쇄8–22/PDF12–26 | 정기 변경과 긴급 변경의 시기·승인권자·규모 예외, 혼잡/신뢰성/성장 우선순위를 확인. 이번 감사에서 모든594행을 새로 의미 판독하지 않았다. | 선정 chapter 내부 제목; 전체 문서 제목 없음 | [공식 원문](https://cdn.kingcounty.gov/-/media/king-county/depts/metro/documents/about/policies/2021-11-17-metro-service-guidelines.pdf?hash=6CEF5D1B785F7119A8A02D92A7C70E77&rev=d5a012b52b0b47ba8e477c46bd9f1969) |
| T02 | 1–178 전체; PDF/인쇄1–5 | 대체 운행은1:1 보증이 아니며 기존 대안 우선·셔틀 보완·안전/접근 예외·고객 통지의 차이를 확인. | 첫1행 실제 문서 제목 잔존: 범위 불일치 | [공식 원문](https://cdn.mbta.com/sites/default/files/2026-09/2026-09-16-mbta-diversion-service-standards-for-subway-regional-rail-and-ferry-accessible.pdf) |
| T03 | 1–140 집중 재독; 전체367행 해시/feature검증; 인쇄21–29/PDF22–30 | 경미/중대 변경의 자원·권한 구분, 고객 전체 편익, 부하 임계값과 연속6개월 조건, 공청 범위를 확인. | §5 내부 제목; 전체 문서 제목 없음 | [공식 원문](https://cdn.ttc.ca/-/media/Project/TTC/DevProto/Documents/Home/About-the-TTC/Projects-Landing-Page/Transit-Planning/Service-Standards_May-2024.pdf?rev=6c96a85cc0a64147ad424f949dabce64) |
| T04 | 1–160 및258–292 집중 재독; 전체2249행 해시/feature검증; 인쇄2–53/PDF4–55 | 기준은 최소치·자원 제약 조건이며 안전/접근성 등 별도 기준을 참조한다. 다단 편집이 텍스트 순서를 끊는 사례를 확인했다. | 272–273행 제목일치=chapter2 구분면; 허용 내부 제목 | [공식 원문](https://www.translink.ca/-/media/translink/documents/plans-and-projects/managing-the-transit-network/transit-oriented-communities/transit-services-guidelines-public-summary.pdf) |
| T05 | 1–283 전체; 인쇄24–30/PDF33–39 | 변경 임계값·누적 삭감·긴급/실험180일 예외·대안/완화·정당화 절차. 전체 문서 draft 표기와 정책파트 승인 진술의 긴장은 유지한다. | PartII 내부 제목; 전체 문서 제목 없음 | [공식 원문](https://trimet.org/civilrights/pdf/titlevi-program-2025.pdf) |
| T06 | 1–289 전체; PDF/인쇄2–10 | 수요·재원·인력에 따른 조건부 계획과 연3회 자원중립 조정. 시나리오·예상치·제안 부록을 실적/확정규칙으로 바꾸지 않는다. | chapter1 내부 제목; 전체 문서 제목 없음 | [공식 원문](https://www.sfmta.com/media/33758/download?inline) |

## 별도 공식 재요청

`resume-donor-attempts.jsonl`에 각 시도와 결과를 남겼다. L04 웹리더는 공식 본문191–239행을 다시 제공했으며 정책일이 없는 점도 동일했다. T04 웹리더는2018년6월64쪽판, T05 웹리더는2025년9월78쪽판으로 동일한 문서 신원을 확인했다. 직접 HTTP로 L01·T02·T05를 재요청한 원바이트 SHA는 봉인값과 완전히 같았다.

S06 웹리더는 iframe만 반환해 이번 그 응답을 본문 확인으로 세지 않았다. 공식 HTTP 원바이트가 달라 추가 비교했으며 `#pageViewData`의 정책 JSON 전체는 봉인원본과 동일했다(양쪽 SHA256 `0c34843f115c4af08482a8b8a6176753d91b114d21c3d5e7b9a93264abc2f8c3`, 달라진 최상위 키0개). 따라서 외피 HTML변경을 정책변경으로 오인하지 않는다. 원 캐시는 갱신하지 않았다.

## 남는 주의·다음 최소 확인

- T04처럼 다단/표를 Poppler layout으로 추출하면 같은 줄에 본문과 사이드바가 끼어든다(예:66–114행). 해시·토큰 순위는 재현되지만 문장/역할 연결은 원 PDF페이지와 대조해야 한다. 200토큰창이 조건의 절반만 담으면 전체 문서 판독을 원 반환의 성공으로 소급하지 않는다.
- T05 전체 보고서에는 draft 표기가 남아 있는 반면 선정 정책파트는 Board-approved라고 서술한다. 정책파트의 텍스트 존재는 확인되지만 전체 보고서 최종 채택은 이 자료만으로 확정하지 않는다. S06 구CMS PageDate도 실제 효력일을 대체하지 않는다. 각 현재판을 과거 최초 설계의 이용 가능 자료로 세려면 당시 판을 따로 확보해야 한다.
- 제목 누락 민감도는 반드시 원 시험과 별도 출력으로 실시한다. 본문18개를 새 후보나 나중에 발견한 유리한 절로 교체할 근거는 발견하지 못했다. 원 source 수나 양성 개수를 높이는 수정은 하지 않았다.
