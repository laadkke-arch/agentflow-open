# N-E02: 원 NOAA RUC 보존 원문 집중 탐색

## 결과

2026-11-22 22:35–22:39 UTC의 집중 탐색으로 **원 NOAA RUC/ESRL/GSL 저작의 본문, 형식 문서, station history를 회복했다.** Internet Archive 보존 경로로 직접 읽었으며, 같은 원 저작의 여러 캡처·절·파일을 추가 저작으로 세지 않는다. `sources.jsonl` S-E060 한 행만 발행자 원문 배당에1을 더한다. ESSD 배당은 소비자3 / 발행자3 / 저자 당대 기록2, 총8저작이 됐다.

**실제1994–2016 훈련 profile export, 그 판을 사용했다는 소비자 기록, 원 실행과 파일의 연결, 일평균 LWP의 독립 재계산은 확보하지 못했다. N-E02의 P/U/R/V는 모두 false 그대로다.** 발행자 원문 직접 열람의 성공과 특정 입력판의 식별은 다른 측정이다. 먼저 시도한 현행 RUC 주소는22:09:34에 실패했고, 원 발행자 본문을 실제 처음 읽은 시각은22:36:01.356013이다. 두 시각을 사례에 따로 기록했다.

## 요청·최종 주소·확인 범위

| 원 발행자 주소·내용 | 요청한 캡처 → 실제 최종 캡처 | 직접 확인한 위치·내용 | 한계 |
|---|---|---|---|
| [RUC /raobs/intl/](https://ruc.noaa.gov/raobs/intl/) | 2020-12-18 09:46:34 → [같은 캡처](https://web.archive.org/web/20201218094634id_/https://ruc.noaa.gov/raobs/intl/) | Recent Activities:2020-06에2018/2019 IGRA+GSL 자료 병합,2020-07 역목록 갱신. I–III:UTC 기간·WMO/WBAN·level·풍속 단위 선택. HTML6724바이트 | 안내/쿼리 폼이다. 훈련 데이터 파일이 아님 |
| 같은 원 RUC index | 2022-01-19 05:49:55 → [2023-01-04 14:51:57](https://web.archive.org/web/20230104145157id_/https://ruc.noaa.gov/raobs/intl/) | 같은 종류의 폼과2020 갱신 공지. HTML6814바이트 | API가 제안한2022 URL을 실제2022 캡처를 읽은 것으로 기록하지 않음 |
| [General_Information.html](https://ruc.noaa.gov/raobs/General_Information.html) | 2021-12-05 08:45:51 → [같은 캡처](https://web.archive.org/web/20211205084551id_/https://ruc.noaa.gov/raobs/General_Information.html) | OVERVIEW의 REAL-TIME ARCHIVE:2007 IGRA/GTS와 GSL/ESRL 자체 관측 병합. STATION HISTORY:history 대응 항목이 있어야 sounding 출력. DATABASE ACCESS SOFTWARE:binary 보관, ASCII2종/GTS/NetCDF 출력 | 원 archive의 계보·출력 조건은 확인. 개별 훈련 export의 날짜/해시/판은 없음 |
| [inventory_2000-2020.lis](https://ruc.noaa.gov/raobs/inventory_2000-2020.lis) | 2020-12-18 요청 → [2020-12-04 23:57:09](https://web.archive.org/web/20201204235709id_/https://ruc.noaa.gov/raobs/inventory_2000-2020.lis) | Header는WMO_ID,BDATE,EDATE,TOTAL,12개월 관측 수. 반환 바이트1048576 | 정확히1MiB만 반환됨. 그 범위에서78954를 못 찾았다는 사실을 전체 inventory에 없다는 주장으로 바꾸지 않음. 이 해시는 반환된 범위의 해시 |
| [international_sites.txt](https://ruc.noaa.gov/raobs/international_sites.txt) | 2021-12-05 요청 → [2022-07-06 05:09:38](https://web.archive.org/web/20220706050938id_/https://ruc.noaa.gov/raobs/international_sites.txt) | 국제 역 이력 파일96096바이트;78954 검색 일치 없음 | General Information이 두 history 파일을 함께 요구하므로 North American 파일을 추가 확인. 단일 파일 부재를 station 부재로 세지 않음 |
| [stat2000.txt](https://ruc.noaa.gov/raobs/stat2000.txt) | 2021-12-05 요청 → [2022-07-06 05:07:41](https://web.archive.org/web/20220706050741id_/https://ruc.noaa.gov/raobs/stat2000.txt) | L90–91에 WMO78954, SEAWELL APT. raw fields13.07/59.50/56은19650730–19711026,13.07/59.50/47은19711027–99999999 | 논문 TableA1과 raw 숫자가 동일하지 않음. 좌표 부호·표기, 역사 유효기간, 캡처 시점, 실제 소비 export 선택이 달라 정정/원 분석 오류로 단정 못함 |
| [fsl_format-new.html](https://ruc.noaa.gov/raobs/fsl_format-new.html) | 2021-12-05 요청 → [2022-07-06 03:37:18](https://web.archive.org/web/20220706033718id_/https://ruc.noaa.gov/raobs/fsl_format-new.html) | FSL Rawinsonde format/LEGEND:첫4행 metadata; 결측32767(원형)/99999(신형); TEMP/DEWPT0.1°C; pressure원형mb/신형0.1mb; user가풍속단위선택; SOURCE4는NCDC+GTS병합 | schema와 단위 조건을 확인했을 뿐, 저자가 이 형식을 내려받았다는 증거는 없음 |
| [netcdf_format.html](https://ruc.noaa.gov/raobs/netcdf_format.html) | 2021-12-05 요청 → [2022-07-06 05:09:13](https://web.archive.org/web/20220706050913id_/https://ruc.noaa.gov/raobs/netcdf_format.html) | wmoStat, synTime, relTime; tpMan=kelvin, tdMan=dew-point depression kelvin, wsMan=m/s; 결측99999; global version Forecast Systems Lab1.3 | 예시 schema의 version1.3을 실제 훈련 data edition으로 바꾸지 않음 |

## 무엇이 바뀌고 무엇이 남는가

B−A는 이제 단순 접근 실패에 머물지 않는다. 원 발행자가 병합한 자료의 성격, station history가 출력 여부에 영향을 주는 조건, 형식별 단위·결측·level 선택을 알게 됐다. 현재 IGRA를 RUC와 동일한 export로 바꾸는 것이 부당하다는 이유도 발행자 원문에서 확인했다. 그러나 이 문서가 보여 주는 것은 제공자의 선택지다. 소비자가 어떤 형식/기간/역/level을 요청했고 어떤 파일을 실제 학습에 썼는지는 여전히 C의 빈자리다.

특히 세 종류의 시간을 분리해야 한다. 원문은2007 병합이나2020 갱신을 설명한다. Wayback은2020·2021·2022·2023의 서로 다른 시점에 그 문서를 캡처했다. station history는1965–1971 또는1971 이후의 유효기간을 나타낸다. 이 셋 중 어느 것도 자동으로2021 저자의 다운로드 시각이나1994–2016 훈련 데이터의 확정 판이 되지 않는다.

저자의 TableA1에 있는13.040/−59.290/56.0을 새로 읽은 station history의 숫자와 바로 대조해 오류로 단정할 수 없다. raw longitude 필드의 서경 표기 관례와 소비자 표의 부호, 좌표 표시 방식, 유효기간을 먼저 정리해야 한다. 또한 이 값은 선정된 주 필드인2020-01-19 LWP=1 g/m²의 대체 필드가 아니다. 보조 station metadata의 차이를 주 V 성공 또는 주 LWP 불일치로 승격하지 않는다.

## 실패·복구 경로

현행 `/raobs/intl/General_Information.html`과 `/raobs/intl/inventory_2000-2020.lis`는503, 같은 `/intl/` 경로의 Wayback 요청은404였다. 검색에서 발견한 공식 사용 설명의 원 URL과 루트 상대 경로를 확인해 `/raobs/General_Information.html` 및 `/raobs/inventory_2000-2020.lis`로 복구했다. 잘못된 상대 경로에서의 실패를 저장소 전체 소실로 해석하지 않았다.

웹 검색의 open 도구는 index의 Wayback URL을 열지 못했다. Python urllib로 직접 읽은 결과는 성공했고 요청 URL, 최종 URL,UTC,바이트 수, SHA256을 모두 기록했다. API나CDX에 캡처가 있다는 것만으로 성공으로 세지 않고 실제 본문을 읽었다. 원 서버의 같은 바이트와 현재 대조했다고 주장하지 않는다.

API/CDX와 검색은 `ruc-focused-searches.json`, 실제 조회는 `ruc-focused-*.json`, 총 출처 원장은 S-E059–077이다. 원문 전체 HTML이나 ZIP은 저장하지 않고 해시·행·필드·확인 내용과 한계를 남겼다.

## 재개 첫 행동

더 넓은 서비스 설명 탐색을 반복하기보다 **저자가 실제 보관한 RUC1994–2016 훈련 export를 찾는 것**이 다음 첫 행동이다. 필요한 입력은 WMO78954를 포함한 station/date/launch 키, 실제 파일 바이트와 해시, 선택한 ASCII/NetCDF 형식과 단위·level·결측 코드, 무작위 학습 분할 목록/seed/weights, 그것을 읽은 원 실행 기록이다. 파일 header의 SOURCE와 유효한 station history를 함께 보존해야 한다. 그 다음 같은 실행의 radar 출력과 Table3 집계를 연결한다.

공개 원문 재열람은 다음 입력 URL을 `urllib.request.urlopen`으로 열어 SHA256·최종 URL을 비교하면 된다. `https://web.archive.org/web/20211205084551id_/https://ruc.noaa.gov/raobs/General_Information.html` 및 `https://web.archive.org/web/20220706050741id_/https://ruc.noaa.gov/raobs/stat2000.txt`다. 예시 명령은 `python -B -c 'import urllib.request,hashlib; u="https://web.archive.org/web/20220706050741id_/https://ruc.noaa.gov/raobs/stat2000.txt"; r=urllib.request.urlopen(u); b=r.read(); print(r.url,len(b),hashlib.sha256(b).hexdigest())'`다. 이는 보존 문서 재열람 명령이고 원 분석 재현 명령이 아니다.
