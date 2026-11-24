# Q7 · 지도 인쇄판과 운행일

## USGS Vienna 도엽 2개

같은 Vienna, VA–MD 7.5분 도엽과 1:24,000 축척을 USGS 카탈로그에서 2/2 대조했다. 한 카탈로그의 Related Items는 1957과 다른 1966 판도 같은 도엽명으로 보여 준다. [1966 항목](https://store.usgs.gov/product/260241) · [1973 항목](https://store.usgs.gov/product/261082) · [판 구분 FAQ](https://www.usgs.gov/faqs/there-are-multiple-copies-same-map-your-historical-topographic-map-collection-all-have-same)

| 카탈로그 항목 / 스캔 ID | 목록의 Survey Date / Print Date / Version Date | GeoPDF 원면·범례 |
| --- | --- | --- |
| 260241 / 187062 | 1966 / 1971 / 1971-01-01 | [USGS GeoPDF](https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/PDF/VA/24000/VA_Vienna_187062_1966_24000_geo.pdf). 웹 파서가 본문을 반환하지 않았다. 범례·인쇄면 미확인. |
| 261082 / 187064 | 1973 / 1980 / 1980-01-01 | [USGS GeoPDF](https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/HistoricalTopo/PDF/VA/24000/VA_Vienna_187064_1973_24000_geo.pdf). 웹 파서의 크기 제한 13,889,231 B, Cloud Chromium `ERR_TUNNEL_CONNECTION_FAILED`. 범례·인쇄면 미확인. |

USGS 안내의 `Date on Map`, `Imprint Year`, `Photo Revision Year`, `Field Check Year`를 따로 보았다. 위 연도는 카탈로그 필드의 연도·날짜 정밀도다. 실제 측량, 사진 수정 시각, USGS 디지털 게시일은 각 판의 하단 식자와 XML을 읽기 전 미확인이다. USGS JPEG 미리보기 두 URL은 웹에서 주소만 반환했고 셸에서 이미지 요청은 제한된 egress로 실패했다. 1957 대체 항목은 검색 내용과 다른 maintenance 페이지가 열렸다. 과제의 Vienna 지형에 붙일 수 있는 범례·표적(예: Lake Anne 부근 도로 기호, 풍부하지 않은 도시 기호)의 인쇄판 직접 비교는 0/2다. 현장에 지금도 같은 도로·시설이 있는지는 이 지도 판·게시 시점과 별도 증거가 필요하다. [topoView 지도 정보](https://ngmdb.usgs.gov/topoview/help/) · [컬렉션 안내](https://www.usgs.gov/programs/national-geospatial-program/historical-topographic-maps-preserving-past) · [Vienna 이미지 소개](https://www.usgs.gov/media/images/change-over-time-us-geological-survey-topographic-maps)

스캔의 픽셀 변화와 종이 개정을 구별하기 위해 LoC Brooklyn Vol. 2 판 19의 공개 작업 사본을 열고 동일 입력의 재표본화를 실제로 대조했다. 839×1240, 483,115 B, SHA-256 `3a7fb4a5bc3ed3f86ab991054f74dd52b029d05c00a206f0439698612522c89e`에서 420×620, 62,153 B, SHA-256 `32776086a3287e414ddab45e3d318f21db61b0a2060da533b040f5aebfb17f56`가 됐다. 두 이미지에서 판 번호 19, CLINTON·PIERREPONT, 분홍 면과 노랑 면을 찾았다. 작은 숫자·하단 축척과 세부 약어는 작은 사본에서 판독이 약해졌다. 이 1/1 대조는 재인코딩·재표본화 실험이다. 기관이 같은 종이를 재촬영한 두 독립 스캔은 0/1쌍이고 실제 재스캔의 날짜·영수증은 미확인이다. 재스캔 가능성이 있는 자료에는 스캔 지문과 인쇄 식별자를 함께 보존하고 좁은 선·색·정정 종이의 판단에는 고해상도 원면을 연다. [인쇄면 작업 사본](https://github.com/danvk/mapsnap/blob/672c155a1289b41c9c246b8c74071b58c4e1db87/images/brooklyn_ny_1939_vol_2_p19.jpg) · [LoC 판 식별자 연결](https://github.com/danvk/mapsnap/blob/672c155a1289b41c9c246b8c74071b58c4e1db87/gallery/brooklyn_ny_1939_vol_2.iiif.json) · [LoC 색·기호·정정 설명](https://guides.loc.gov/fire-insurance-maps/sanborn-interpreting)

대조 명령은 ImageMagick 7.1.1-43에서 실행했다. 한 원면 및 파생면 각 1개를 읽었으며 바이트는 이미지 파일 크기다. Vienna 원면 2개의 취득·판독 시간과 바이트는 미확인이다. 두 분야의 Node/브라우저 실행 횟수와 합산하지 않는다.

```sh
curl -fsSL 'https://raw.githubusercontent.com/danvk/mapsnap/672c155a1289b41c9c246b8c74071b58c4e1db87/images/brooklyn_ny_1939_vol_2_p19.jpg' -o /tmp/af135-p19.jpg
magick /tmp/af135-p19.jpg -resize 50% -quality 75 /tmp/af135-p19-derivative.jpg
identify /tmp/af135-p19.jpg /tmp/af135-p19-derivative.jpg
sha256sum /tmp/af135-p19.jpg /tmp/af135-p19-derivative.jpg
```

## Washington State Ferries Seattle → Bainbridge Island

| 운행일 / 현지 날짜 | 같은 정류장·방향의 첫 오전 셀 | 예정 운행·실제 운행 |
| --- | --- | --- |
| 2026-11-24 화요일, America/Los_Angeles | Seattle 출발 → Bainbridge Island. 날짜 페이지 Leaving Seattle 첫 행 05:30. 계절 평일 표 첫 셀도 05:30. | 시간표 두 소스에서 계획 일치. 실제 출발 관측 미실시. |
| 2026-11-26 목요일 Thanksgiving, America/Los_Angeles | 동일 출발·방향. 계절 주말/휴일 표 첫 셀 06:10, 평일 대비 40분 뒤. | 11-23 08:37 게시 표기 공지가 11-26 이 노선에 휴일 표 적용을 지정했다. 11-26 날짜별 렌더 본문은 미확인, 실제 출발 관측 미실시. |

[11-24 날짜 결과](https://wsdot.com/FERRIES/SCHEDULE/scheduledetail.aspx?arrivingterm=3&departingterm=7&roundtrip=true) · [가을 노선표](https://wsdot.com/FERRIES/SCHEDULE/scheduledetailbyroute.aspx?route=sea-bi) · [11-23 개정 공지](https://wsdot.com/FERRIES/SCHEDULE/bulletin.aspx) · [날짜 선택 화면](https://wsdot.com/FERRIES/SCHEDULE/schedulebydate.aspx)

가을표의 유효 기간은 2026-09-20–12-26이다. 같은 고정 노선 주소에서 요일 범주가 둘이고 공지는 그중 공휴일을 고른다. 05:30과 06:10을 비교할 때 먼저 시간표 날짜·터미널·방향을 맞췄고, 선박 배치 번호나 자정을 넘긴 시각은 합산하지 않았다. 같은 공지가 다른 노선에는 평일 그대로 또는 일부 조정이라고 밝혀 공휴일이라는 표지만으로 추론하는 것을 반증한다. 공지를 조회한 오늘 URL은 발행 후 본문을 보존한다고 보증할 수 없다. 공공 자료의 비용은 직접 연 1차 게시물 3건(노선표·날짜 결과·공지)과 달력/API 보조 읽기, 날짜별 렌더 1/2, 예정 셀 판독 2/2다. 웹 도구는 본문 바이트와 실제 검토 시간을 제공하지 않아 미확인이다. 날짜 선택의 제출과 운항 기록 조회는 미실시다. [API의 날짜/터미널 매개변수](https://www.wsdot.wa.gov/ferries/api/schedule/rest/help)
