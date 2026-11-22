# 최종 통합 보고서 검토 — ESSD와 Q6

## 검토 성격과 결론

이 검토는 **같은 모델의 별도 에이전트 문맥 검토**다. ESSD 자료 수집을 담당했던 `/root/essd`가 부모의 통합 `RESULT.md`와 `contradictions.md`를 검토했다. 외부 독립 판독자·눈가림 평가·원 분석 재실행이 아니다. root 파일은 직접 수정하지 않았다.

**검토 범위에서 P/U/R/V를 바꿀 중대한 혼동이나 수치 오인용을 찾지 못했다.** JSON 내부 locator 한 건을 수정 요청했고 부모가 반영한 것을 다시 읽었다. IOW 이전판 링크가 없다는 초기 의심은 실제 HTML 재열람으로 반증되어 철회했다. 이 철회는 보고서가 틀렸다는 결론이 아니라, 추출 도구의 생략을 발행자 페이지의 사실로 잘못 읽지 않아야 한다는 검토상의 반례다.

## 점검 결과

| 점검 | 통합 보고서 위치 | 판정과 이유 |
|---|---|---|
| Q1 선정과 Q3–5 필드 계보 분리 | RESULT §2 ESSD 단락, 표1 N-E00, 표2 N-E00 A | 통과. 실제 WoRMS 이용을 이유로 포함하고 Group↔외부 입력 필드의 연결은 미확인으로 유지한다. A01의 원격 커밋이 발행자 열람 뒤인 한계와 앞선 ESSD5쪽 경계도 명시한다. |
| 자체 출력판과 WoRMS 입력판 | 표1 N-E00, 표2 N-E00 C, Q5 IOW 행, contradictions X07/X08 | 통과. IOW release2와 F5=Amphipoda 재독을 P/U/R/V 성공으로 올리지 않는다. 원시 Group/Taxa와 지역별 요약 차이도 맞는다. |
| BCO 발행판과 소비판 | 표1 N-E01, 표2 N-E01 B/C, RESULT §3 | 통과. v3.0.0 존재만 P로 인정하고 Fig5의 정확한 점/키·입력 level/파일·원 실행은 미확인이다. 자체 RAAVEN B1으로 빈칸을 채우지 않는다. |
| RUC 원문 복원과 훈련판 복원 | 표1 N-E02, 표2 N-E02 B/C, RESULT §3 원문 복원 단락, contradictions X02 | 통과. 원 NOAA 저작 복원과 배당1 증가를 실제1994–2016 훈련 export의 식별과 구별한다. 캡처 날짜·FSL1.3 형식·실제 data edition을 합치지 않는다. |
| N-E02 코드·출력 정정 | RESULT Q5 뒷단락, contradictions §4 N-E02 | 통과. 코드의 nanmean은 절차 확인이며 run receipt가 아니다. DOI156→235는 자체 radar 출력의 정정 공지이고 같은19Jan LWP 구판/신판 값은 미대조다. cloudy-only median11과 all-time median2.6817865도 혼동하지 않는다. |
| ALFRED 발표일·빈티지 | RESULT Q6 두 공식통계 행 | 통과. [Help](https://alfred.stlouisfed.org/help) L35–40의 원 발표일→제공자 날짜→FRED 최초 가용일 순서, L53–54의 반올림 level/성장률 차이를 재독했다. [Download Help](https://alfred.stlouisfed.org/help/downloaddata) L48–64의 관측일/빈티지 및 변경 없는 발표일 처리도 보고서와 맞다. |
| ALFRED GNPC96 단위 이력 | RESULT Q6 보조 단락 | 통과. [GNPC96](https://alfred.stlouisfed.org/series?seid=GNPC96) Notes/Units L85–86에2012 기준2018-07-27~2023-09-27,2017 기준2023-09-28 이후가 표시된다. 이를 개별 빈티지값이나 소비 실행 검증으로 부르지 않는다. |
| NASA CMR 계층·이전판 metadata | RESULT Q6 DOI 계층 행 | 통과. [CMR DOI](https://wiki.earthdata.nasa.gov/spaces/CMR/pages/107385989/DOI) L16–38의 collection 식별과 PreviousVersion의 기간·폐기·발행 필드를 확인했다. 특정 granule/변수/run으로의 승격을 금지한 적용 추론은 범위를 지킨다. |
| PANGAEA 값·정정 범위 | RESULT Q5 AUX-EARTH-01, Q6, contradictions X09/§5 | 통과. [889928](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=html) Data L110의 depth0.045/Age2.1/230Th310.292 pg/g, [936557](https://doi.pangaea.de/10.1594/PANGAEA.936557?format=html) Data L116의 Age2.574와 동일230Th를 재독했다. 936557 L47의 age model 개정,889928 L71·73의 저자목록 정정/새판 게시도 구별한다. 저자목록 정정 전후 payload 불변을 미확인으로 남긴 것이 적절하다. |
| CMIP6·ESGF 규칙과 실제 준수의 구별 | RESULT Q6 보조 단락 | 통과. [CMIP6 §4](https://pcmdi.llnl.gov/CMIP6/Guide/dataUsers.html) L109와 [ESGF API](https://ipsl.gitbook.io/esgf-errata-service/errata-service-api) L153–177,191–201을 재독했다. 규칙의 존재를 선정 소비자의 실제 준수로 바꾸지 않았다. |
| 동일 URL/bytes 실제 미사용 음성례 | RESULT Q6 마지막 단락, contradictions §3 | 통과. 확보하지 못한 조건을 명확히 미충족으로 남겼다. R4.2.1 공개일이나 CPM 시간 역전을 완전한 입력 미사용 영수증으로 대체하지 않는다. |
| 서로 다른 URL의 같은 bytes | RESULT Q6 마지막 단락, contradictions §3 | 저장된 `domain/url-encoding-alias-check.json`과 `pangaea-fetch.json`에서9394bytes와 동일 SHA256을 확인했다. 이번 검토에서 GET/hash를 다시 실행한 것은 아니므로 별도 독립 바이트 재측정이라고 하지 않는다. |

## 확인된 수정 1건

`contradictions.md` X07의 초기 위치 표기 `iow-edition-comparison.json keyed_rows/selected_cells` 중 `keyed_rows`는 실제 JSON 키가 아니었다. 숫자 자체는 맞지만 독자가 지정된 위치를 찾지 못한다.

정확한 경로는 다음과 같다.

- `sheet_comparisons[?sheet="Factors Baltic Sea"].same_numeric_cell_different_taxon_examples`: B148=1, taxon_v1=Hippeutis complanatus, taxon_v2=Hirudinea.
- `sheet_comparisons[?sheet="Factors North Sea"].same_numeric_cell_different_taxon_examples`: B21=1과 다른 taxon 쌍.
- `sheet_comparisons[].taxon_keyed_changes`: 지역별 요약에서 이동한 두 taxon.
- `sheet_comparisons[?sheet="Raw_Single_Measurments_Factors"].changed_region_records`: raw row7319/13310, UniqueID7315/13306.

부모가 X07을 `sheet_comparisons[].same_numeric_cell_different_taxon_examples / taxon_keyed_changes`로 고친 것을 재독했다. P/U/R/V·분모·값은 바뀌지 않는다.

## 철회한 링크 의심과 그 반증

웹 검색 open의 IOW 페이지 추출본은 두 판 모두 `Related` 제목 뒤를 비워 보였다. 이 때문에 “release2의 이전판 링크”라는 통합 보고서 표현을 잠시 의심했다. 같은 URL을 직접 GET해 HTML을 확인하자 다음 관계가 있었다.

| 실제 GET UTC | URL | SHA256 | HTML 위치에서 확인한 관계 |
|---|---|---|---|
| 2026-11-22T22:55:02.340229+00:00 | [release2](https://doi.iow.de/10.12754/data-2021-0002-01) | 68ee4ed6aec93d84a880488b0b170e944979d68139e6e173b15376e5f20a8197 | `h3 Related` 다음 `p.related`: IsNewVersionOf →10.12754/data-2021-0002 |
| 2026-11-22T22:55:02.427819+00:00 | [release1](https://doi.iow.de/10.12754/data-2021-0002) | 537f7fa9825c999b1bcc87cb4ccfde51d2217d6ecae6824da892aefb283e6771 | `h3 Related` 다음 `p.related`: IsPreviousVersionOf →10.12754/data-2021-0002-01 |

따라서 관계 링크 부재라는 의심은 **철회**한다. 보고서의 관계 설명은 유효하다. 두 DOI를 직접 병기하는 편집은 접근 편의를 높이지만, 기존 링크가 없었다는 정정 사유를 붙이면 안 된다. `final-report-review.json`의 `source_rows`에는 이 두 실제 재열람을 S-E078/S-E079, 중복·최소수 산입0으로 남겼다. 원문 전체 HTML은 저장하지 않았다.

## 검토 범위의 한계

R Journal과 실행 보강2건의 모든 원 파일을 이 검토에서 다시 감사하지 않았다. 그 부분의 상세 수치·코드·RDS/HDF5/VCF 처리에 대한 별도 전문 검토를 대신하지 않는다. ESSD 원 ZIP 값 비교는 이번 검토에서 재실행하지 않고 기존 실제 비교 receipt와 JSON 키를 대조했다. Q6는 위 원문 재독과 저장된 byte receipt 검토 범위다. 이 결과는 외부 독립 판독의 성공률이나 실제 사용자 채택 증거가 아니다.
