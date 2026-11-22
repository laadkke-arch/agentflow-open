# Q5–Q7 분야 간 보조 관측

이 파일의 사례는 AUX ID이며 소비자6·실행보강2의 분모와 분리한다. 직접 읽은 source rows는 sources.jsonl, 실제 바이트 관측은 pangaea-fetch.json 및 url-*-check.json에 있다.

## 1. 공식 통계의 세 시점

ALFRED는 관측 대상 시점, 당시 알려져 있던 빈티지, 다운로드/확인 시점을 분리한다. [발표일 결정 규칙](https://alfred.stlouisfed.org/help) §How are Release Dates determined?는 원 발행일을 우선하되 데이터 제공자 날짜, 최후에는 FRED 최초 입수일을 쓴다. 그 날짜를 자동으로 분석 실행일로 읽을 수 없다. §growth rates는 반올림된 level에서 다시 계산한 변화율이 원 발행 변화율과 다를 수 있다고 설명한다. 따라서 동일 이름의 수치라도 변환과 반올림이 대조 키에 필요하다. 근거 S-D01.

[다운로드 규칙](https://alfred.stlouisfed.org/help/downloaddata) §Vintage Dates/Output Formats에서는 관측일을 행, 빈티지를 열로 구분한다. 같은 행이 여러 빈티지에서 변하지 않을 수 있고, 변경이 없는 발표일은 개정 목록에 없을 수 있다. 날짜 변화=값 변화도, 같은 값=같은 판도 성립하지 않는다. 이 문서가 설명하는 데이터 형식은 이용자의 실제 다운로드 영수증이 아니다. 근거 S-D02.

실제 [GNPC96 레코드](https://alfred.stlouisfed.org/series?seid=GNPC96) §Notes/Units는 같은 series ID에 2012년 기준 연쇄달러 기간(2018-07-27~2023-09-27)과 2017년 기준 기간(2023-09-28 이후)을 붙인다. 관측연도만 맞춰 level을 대조하면 단위 기준이 달라질 수 있다. 이 확인은 현재 제공되는 단위 이력이며 특정 논문의 투입을 증명하지 않는다. 근거 S-D16.

## 2. 지구과학의 collection·판·파일·정정

[NASA CMR DOI 규칙](https://wiki.earthdata.nasa.gov/spaces/CMR/pages/107385989/DOI) §Element Description/Best Practices는 collection DOI와 PreviousVersion의 DOI·판·발행·제공기간·폐기일을 나눠 관리한다. collection DOI를 알더라도 특정 granule·변수·실행 ID는 별도 연결이 필요하다는 것이 이번 적용상의 추론이다. near-real-time/provisional 자료에 DOI가 없을 수 있다는 설명도 있으므로 DOI 부재 자체를 데이터 부재로 처리하지 않는다. 근거 S-D04.

[CMIP6 이용 지침](https://pcmdi.llnl.gov/CMIP6/Guide/dataUsers.html) §4는 판, 없으면 다운로드일을 인용하도록 안내한다. 이 인용 단위는 model/experiment 계층일 수 있다. [ESGF 정오표 API](https://ipsl.gitbook.io/esgf-errata-service/errata-service-api) §Simple-PID/PID Tracker는 특정판 검사와 전체 계보 탐색을 구분한다. 해당 지침이 있어도 실제 이용자가 기록을 남겼다고 가정하지 않는다. 근거 S-D07/S-D08. 이 두 문서는 주 배당을 늘리는 대체 자료가 아니라 보조 규칙이다.

## 3. AUX-EARTH-01: 같은 코어·같은 깊이에서 달라진 나이, 유지된 다른 값

대상은 SO213/2_76-2 코어의 [2018판 PANGAEA.889928](https://doi.pangaea.de/10.1594/PANGAEA.889928)과 발행자가 명시한 다음 판인 [2021판 PANGAEA.936557](https://doi.pangaea.de/10.1594/PANGAEA.936557)이다. 후자의 Comment는 age model 개정을 명시한다. 두 DOI는 같은 데이터 저작의 판이므로 최소 원문수에는 합쳐1이다.

| 동일 행 키/필드 | 2018판 | 2021판 | 확인되는 것·확인되지 않는 것 |
| --- | --- | --- | --- |
| depth0.045m / Age, ka BP | 2.1 | 2.574 | 같은 깊이의 age 값이 바뀜. 최신 age 용도이면 구판 값을 그대로 쓰기 어렵다. |
| depth0.045m / 230Th, pg/g | 310.292 | 310.292 | 이 한 값의 일치로 판을 구별할 수 없다. |
| depth0.445m / Age, ka BP | 9.5 | 10.097 | 다른 행에서도 age 변경을 확인. |
| depth3.105m / Age, ka BP | 20.4 | 20.391 | 소수1자리로 반올림하면 같은20.4지만 원값·판은 같지 않다. |
| depth0.045m와0.445m / Water mass | 둘 다 LCDW/AABW | 둘 다 LCDW/AABW | 범주만 저장하면 어느 행인지도 결정하지 못한다. |

위 값은 각 DOI의 `?format=html` Data 첫 행 및 깊이별 행, `?format=textfile`에서 직접 대조했다. 실제 다운로드 전체 바이트의 SHA256은 2018판 `94d5f727d36bcedbd41cd8bc035a0f675356a14cc28b6f96919b9bffb51da747`(9,394 bytes), 2021판 `41f5827f539a3c31cd08044b3971847ca6a82ebac4222cf635fd03ea9b06232c`(9,202 bytes)다. 이것은 이번 수집 파일의 해시다. 어느 외부 소비자가 읽은 해시라는 뜻이 아니다. 근거 S-D05/06/13/14/17/18 및 pangaea-fetch.json.

2018판 Change history의 2021-09-24 항목은 저자목록 정정, 2021-09-30 항목은 새 데이터판 게시다. 정정 종류를 구별할 수 있지만 저자목록 정정 전후의 데이터 바이트를 가져오지 않았으므로 '그때 데이터 바이트는 불변이었다'는 더 강한 주장은 미확인이다. 두 판 사이에는 age 외에 행 범위·출력 소수자리도 달라져 단일 변경이라고 쓰지 않는다.

과거 논문의 사용값 재현이 목적이라면 당시판을 보존하는 것이 맞을 수 있다. 새로운 지질 연대 판단이 목적이라면 현재 age model 확인이 필요하다. 이 목적 구분은 관측 자료에서 도출한 적용 조건이며, 실제 이용자가 이 권고를 채택했다는 관측은 없다.

## 4. AUX-URL-01: 다른 URL과 같은 바이트, 같은 DOI와 다른 표현

2026-11-22T22:06:34Z의 [기본 TSV URL](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=textfile)과 22:12:02Z의 [UTF-8 명시 URL](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=textfile&charset=UTF-8)은 모두 HTTP200, 9,394bytes, 위의 동일 SHA256이었다. 두 요청은 서로 다른 정확 URL이며 현재 동일한 파일 바이트를 확인한 사례다. 같은 저작 추가0. 근거 S-D17/S-D20, url-encoding-alias-check.json.

반대로 DOI resolver에 `?format=textfile`을 붙인 [요청](https://doi.org/10.1594/PANGAEA.889928?format=textfile)은 query가 없는 landing HTML로 도착했다. 응답175,521bytes, SHA256 `ccbc60d80b62963aecffa4373d297cf381e88c6e995dadd2dd34100143e645ea`다. 이는 수치의 불일치가 아니라 도착 표현의 차이다. 실패한 동일파일 가설도 지우지 않았다. 근거 S-D19, url-alias-check.json.

이 관측만으로 '같은 바이트를 반환하는 고정 URL을 어떤 실제 분석 실행이 읽지 않았다'는 부정 사실까지 확인할 수 없다. 그 조건에는 해당 실행이 참조한 객체와 읽은 범위를 보여 주는 별도 기록이 필요하다. 이 조건의 공개 실제 사례가 확보되지 않으면 미충족으로 남긴다. 논리적으로 가능한 반례를 실측 사례로 바꾸지 않는다.

## 5. 관점별 필요한 정보

| 관점 | 최소 기록 후보와 목적 | 사라지거나 혼동될 수 있는 근거 | 허용 주장 범위 |
| --- | --- | --- | --- |
| 발행자 | 저작/판/파일ID, 발행·개정일, 기준기간, 단위, 정정 대상 필드 | 동적 URL 교체, 옛 파일 철거, collection과granule 혼동 | 특정판·필드가 제공됐다고 말할 수 있음 |
| 분석 작성자 | 실제 실행ID와 정확 입력객체, 행/필드·변환·반올림, 취득시각 | 로컬 latest 경로, 미보관 임시파일, 실행되지 않은 취득 스크립트 | 그 실행이 해당 객체를 사용했다는 기록 수준의 주장 |
| 후대 감사자 | 서로 다른 계보의 발행자 객체와 당대 사용 기록, 같은키의 값 대조 | 논문 복사본을 독립증거로 계산, 다른 실행 로그를 합침 | 연결된 객체·필드에 한정한 재확인 |
| 최신값 이용자 | 현재 목적/기준일, 최신 정정의 영향범위, 단위·기간 | 옛 수치가 정확히 인용됐다는 이유로 현재도 유효하다고 추론 | 현재 목적에서 유지/정정/보류 결정; 실제채택은 별도 |

## 6. 반증이 바꾸는 주장

같은 DOI 또는 같은 숫자만으로 사용판을 특정한다는 가설은 AUX-EARTH-01과 AUX-URL-01이 제한한다. 그러나 그 반례가 모든 고정 링크나 모든 값 대조가 무용하다는 뜻은 아니다. 정확한 객체 식별자와 당대 소비 연결이 있으면 바이트·값 대조는 다른 고리를 확인한다. 실제8사례에서 그 연결을 얼마나 확보했는지는 최종 cases/readings 원장으로 따로 센다.
