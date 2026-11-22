# AF-RES-033 현장 자료 재개 감사

검토 시각: 2026-11-22 17:05–17:08 UTC. 별도 모델 문맥의 검토이며 인간 독립 판독이 아니다. 수신 제안의 후속 결과·검색 순위·질의는 읽지 않았다. `field_sources.jsonl`, `field_cases.md`와 해시 고정 원문 캐시를 읽고 공식 URL도 다시 열었다. 기존 원장 수정·커밋은 통합 담당에게 남긴다.

## 결론과 수정 필요 항목

별도 현장 원문은 **4개 고유 작품, 2개 제공 분야, 3개 사건**으로 인정할 수 있다. 이 재독은 새 원문 4개로 가산하지 않는다. 다만 F02의 출처·관측 유형 설명은 수정해야 한다. 기존 원장에 고정된 PDF와 같은 바이트의 직접 재다운로드본은 인쇄 p13의 출처를 **MTA Real Time data**로 표시한다. 기존 초안의 “그 페이지는 GTFS이므로 예정 운행만 확인”은 이 고정본을 정확히 기술하지 않는다.

| 감사 ID | 자료·직접 확인 위치 | 판정 | 필요한 조치·남는 한계 |
| --- | --- | --- | --- |
| RF-A01 | F01 공식 발표, 캐시 본문 L23–30 | 단계별 적용일·대체 노선·보충 인력·공표 채널을 실제 공표했다. | 시행 계획과 운영자의 설명을 확인한 것이다. 예정 빈도·모든 실제 출발·필수 노동자의 이동 성과를 입증하지 않는다. |
| RF-A02 | F02 PDF 인쇄 p13, 하단 출처·세 날짜의 그림·우측 설명 | DCP가 MTA 실시간 자료를 인용해 사후 서비스 변화를 집계한 보고다. 직접 받은 PDF와 캐시의 해시가 같다. | 원시 feed와 집계 코드를 재실행하지 않았다. 개별 열차 운행 로그의 완전성, 실시간 예측과 실현의 구별, 3월 발표 위반은 미확인이다. 웹 스크린샷의 다른 표기를 별도 충돌로 보존한다. |
| RF-A03 | F03 v1 §5, v2 §5, 현재 정정 배너·§5 | 이전판의 여성 90세 이상 집단 문구가 현재판에서 제거됐음을 직접 대조했다. | 두 차례 정정은 한 작품이다. 그림 4·5의 정정은 발행자의 공지까지 확인했으며 그림 데이터 전체의 독립 재계산은 하지 않았다. |
| RF-A04 | F04 v1·v2 `MYE3!A9:O365`, `Correction notice!A1:A3` | 독립 OOXML 대조로 357개 고유 지역키, 39개 변경 행, 78개 변경 셀을 재현했다. | H·I열만 각 39개 변경. J·O열은 357개 전체에서 불변. 비교 범위는 이 표의 저장값이며 전체 워크북·추정 모형을 다시 계산한 것은 아니다. |

## F02의 두 도구 반환 불일치

원 출처는 [NYC DCP 2020-04-21 보고서](https://www.nyc.gov/assets/planning/download/pdf/planning-level/transportation/covid19-transportation/20200421.pdf)이다. 대상 위치는 인쇄 p13, 0부터 센 PDF 페이지 12, “Subway System Service Changes”이다.

| 확인 경로 | 표시된 하단 출처 | 바이트 동일성·해석 |
| --- | --- | --- |
| 이전 작업이 저장한 `field/cache/F02.pdf`의 텍스트 추출 | MTA Real Time data, api.mta.info | 기존 receipt의 SHA256과 일치 |
| 같은 로컬 PDF를 PyMuPDF로 실제 렌더 | MTA Real Time data, api.mta.info | 텍스트층과 시각층이 일치. 이 바이트 내부의 레이어 충돌이 아니다. |
| URL을 Python urllib로 다시 GET한 PDF의 추출·렌더 | MTA Real Time data, api.mta.info | HTTP 200, 4,044,782 bytes, 아래 해시로 기존 캐시와 완전 일치 |
| 웹 도구의 PDF 텍스트 반환 | MTA Real Time data, api.mta.info | 고정 바이트의 추출과 같은 출처 표기 |
| 웹 도구의 PDF screenshot 반환 | GTFS, transitfeeds | 도구가 원 바이트의 해시를 반환하지 않았다. 다른 스냅샷·렌더 경로인지는 미확인이며 고정본의 출처로 채택하지 않는다. |

고정/재다운로드 PDF SHA256: `b3e6689d94b496817a35f072d175b5b4be9149429a87d8adcaf7c8ff5e904bcc`. 서버가 반환한 Last-Modified는 `Mon, 18 Mar 2024 16:13:17 GMT`였고 ETag는 `"65f8681d-3db7ee"`였다. 이 HTTP 메타데이터만으로 문서의 원 발행일이나 수정 사건을 추정하지 않는다. 날짜가 붙은 URL도 영구 불변 URL로 간주하지 않는다.

통합 시 권고 문구는 다음과 같다.

> F02는 MTA 실시간 자료를 출처로 명시한 DCP의 사후 집계 보고다. 세 날짜의 정차 패턴과 감편을 비교하지만 이 연구가 원시 feed나 실제 출발 로그를 재현한 것은 아니다. 웹 스크린샷이 GTFS라는 다른 출처 표기를 반환한 사실은 별도 불일치로 보존하며, 해시가 고정된 직접 PDF를 판독 기준으로 쓴다.

이는 F01의 당초 공표 목적과 F02의 이후 집계를 나눠 확인하는 사례로 사용할 수 있다. 발표와 관측은 시점·척도가 다르므로 곧바로 약속 위반으로 계산할 수 없다. F02를 단순 정적 시간표라고 낮추는 해석도 이 고정본에는 근거가 없다. 다음 최소 자료는 **해당 2020-02-13·03-12·04-16 원시 feed의 보존본, 당시 DCP 집계 코드, 실시간 예측을 실현 운행으로 판별한 규칙**이다. 현재 API 주소만 열어 과거 재현을 달성했다고 하지 않는다.

## F04 독립 수치 검산

기존 `compare_ons.py`를 다시 호출한 결과를 독립 검산으로 부르지 않았다. 새 판독은 Python 표준 라이브러리 `zipfile`·`xml.etree`로 두 XLSX의 workbook 관계·shared strings·MYE3 셀을 직접 읽고 A열 지역코드로 조인했다. 중복키를 먼저 검사하고 각 행 A:O의 명시적 좌표를 비교했다. 원 파일을 저장하거나 다시 계산하지 않았다.

- 원본 SHA256: `9f38b7c38589577be701c7a8a9a9bc37857d78af0a04f37325e6c0870a252e79`.
- 정정본 SHA256: `7dea3da9e8000f1ba4b5d9b702c364b751c6142fce504521d3f4a8e02146034f`.
- 두 판 모두 357개 고유 지역코드이며 키 집합이 같다. 검산한 MYE3의 수식 셀 수는 두 판 모두 0이다.
- 39개 지역에서 H·I가 각각 하나씩 바뀌어 78셀이다. 기존 `ons-correction-comparison.json`의 `(지역코드, 좌표, 이전값, 정정값)` 집합과 정확히 같다.
- J열 순이동과 O열 인구는 357개 지역에서 모두 같다. 이것은 다른 시트가 불변이거나 전체 추정 과정이 정확하다는 증거가 아니다.

[공식 전후판 목록](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales/mid20222023localauthorityboundaires)의 정정 이유와 워크북의 정정 공지는 큰 지역 내부의 이동을 총 유입·유출에 잘못 포함했다고 설명한다. 최종 순이동 값이 같아도 구성값의 경계가 틀릴 수 있다는 기존 반례는 유지된다. 정정일 2023-12-19를 최초 발행일로 바꾸지 않는다.

## 나머지 원문과 최소수

[F01 발표](https://apps.cio.ny.gov/apps/mediaContact/public/view.cfm?parm=926C019C-DE79-DD17-D6493016DF74143F_5D9C1A27-C9C7-90C0-217C93A974EEA6D8)와 F02는 기관·작품이 다른 두 문서이지만 같은 감편 과정이다. DCP가 MTA 자료를 사용했으므로 서로 독립적으로 측정한 운행 실적 두 벌로 취급하지 않는다. 독립 사건 수는 1이다.

F03의 [v1](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v1)·[v2](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/v2)·[현재 캡처 URL](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/articles/reconciliationofmidyearpopulationestimateswithcensus2021englandandwales/2023-02-28/previous/)은 한 작품으로 센다. v2는 2월 28일 그림 정정 이후지만 3월 1일 문장 정정 이전이다. 현재 URL은 가변이고 과거 두 URL은 판별 주소라는 기존 원장 구별은 타당하다. 원문 L152/v2 L156/현재 L159에서 문장 변경을 확인했다.

F04의 두 워크북·목록도 한 데이터세트로 센다. F03의 보고서 문장·그림 정정과 F04의 다른 데이터세트·다른 날짜의 수치 정정은 서로 다른 작품과 사건이다. 두 통계 사건은 모두 ONS가 발행했으므로 외부 기관의 독립 평가 두 건이라고 부르지 않는다.

4개 `duplicate_group`은 서로 다르며 18개 봉인 후보의 원 URL과 직접 중복되는 주소가 없다. 8개 원 바이트 receipt(F01 1, F02 1, F03 3, F04 3)의 SHA256이 모두 기존 기록과 일치한다. 복수 판·재열람·스크린샷·본 감사는 고유 원문 분자에 더하지 않는다. 별도 보강 원문을 추가할 필요는 없어 `resume-field-supplements.jsonl`은 빈 원장이다.

## 통합 담당에게 넘기는 조치

1. F02 `kind`, `observed`, `limitations`와 FIELD-TRANSIT-EXCEPTION의 “GTFS/예정 운행만” 설명을 위 고정본 판정으로 수정한다. 수정 전 초안 해시/영향을 기록한다. 반환 순위나 적합 분자를 사후 수정하는 자료로 사용하지 않는다.
2. 발표 F01 → 사후 집계 F02 → 원시 로그 미확인이라는 증거 범위를 유지한다. 단어 “real-time”만으로 지연·취소·모든 열차 실현을 입증하지 않는다.
3. `resume-field-attempts.jsonl`의 독립 OOXML 검산 및 원격 PDF 동일성 영수증을 공통 시도 원장에 연결한다. 통계 수치·원문 최소수는 유지된다. 수신 팀의 원리 인용·실제 채택은 이 현장 감사의 검토 대상이 아니다.

이번 감사에서 canonical 원장이나 이전 기록은 변경하지 않았으며 git add/commit/push도 실행하지 않았다.
