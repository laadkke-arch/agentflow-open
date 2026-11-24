# 발행판과 관심 셀

[대조 CSV](../domain-cells.csv)에는 직접 확인한 표시값과 열을 담았다. ZIP과 GTFS 접근 실패는 [취득 기록](external-access.json) 및 [원장](../sources.jsonl)에 분리했다. 표에 들어간 값은 두 출처의 같은 질의 조건으로 맞췄다.

## ONS · 잠정 추정, 개정 추정, 게시판 정정

영국 전일제 근로자 일자리 중 직무를 1년 이상 유지한 집단의 50분위 연간 총임금을 골랐다. 2023년 4월 19일이 든 급여 기간을 기준으로 2023년 11월 1일 공개한 잠정 표시 £34,963과 2024년 10월 29일 공개한 같은 기간 개정 표시 £35,004를 각각 열었다. 표시 차이는 £41이다. ONS는 고소득 응답 검증 방법과 LFS 가중치 갱신을 함께 설명하며, 방법 절에 시간당 초과근무 제외 중위 £17.40→£17.52를 보고한다. 시간당 수치의 구판은 이 절에서 읽었으며 독립 원표 대조 행으로 세지 않았다. [잠정 ONS-2023](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2023#main-points-april-2023) · [개정 ONS-2024](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2024#data-sources-and-quality)

2024년 4월 17일 기준 집단과 단위를 고정했을 때 같은 bulletin의 보존 v1과 현재판에서 연간 중위 £37,430이 유지된다. 정정 공지는 Figure 4 위의 National Living Wage 서술을 지목했고 두 판에서 그 수치 문장도 대조했다. 이 정정은 관심 표본의 중위 추정을 바꾸는 개정과 구분된다. v1/현재판의 동일 표시는 원표의 미표시 소수점이나 모든 다른 셀까지 보증하지 않는다. [보존 ONS-2024-V1](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2024/previous/v1) · [정정 ONS-2024](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2024#correction)

Table 1 목록에서 2023 잠정·개정 ZIP의 자원을 각각 확인했다. 셸에서 두 URL은 연결 터널 403이었고 웹 파서는 ZIP/MIME을 열지 못했다. Figure 1 CSV 두 주소도 웹 파서가 바이트 본문을 반환하지 않았다. 독립 Excel 셀 주소와 비반올림 값은 미확인이다. 두 표시 대조가 있어도 Q7의 이 부분을 PARTIAL로 남긴다. [ONS-T1](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/allemployeesashetable1) · [실패 원장](external-access.json)

## South Western Railway · 날짜가 겹치는 기준표와 우선 적용 임시표

2026-09-21 월요일, Brockenhurst 06:10 출발 Weymouth 방향 열을 두 PDF에서 추적했다. PTT28의 표지 적용일은 9월 20일~12월 12일이다. 같은 기간의 임시표를 연결한 운영 공지가 9월 20일 추가 조정을 알린다. 공지에는 정류장별 숫자가 없다. 두 표의 비교로 Sway는 06:15 유지, New Milton은 06:20→06:21을 확인했다. 옆 정류장 Hinton Admiral의 06:24→06:25는 열 연결 대조로 썼다. [기준표 SWR-STD](https://www.southwesternrailway.com/-/media/files/plan-my-journey/timetables/september-2026/ptt28-september-2026.pdf#page=15) · [임시표 SWR-OVL](https://www.southwesternrailway.com/-/media/files/plan-my-journey/timetables/new-milton-temporary-timetable-july-2026/september-2026/london-to-weymouth-temporary-weekday-timetable---updated-september.pdf#page=1) · [SWR-NOTE](https://www.southwesternrailway.com/other/about-us/~/link.aspx?_id=1556dece39914c2d90662ef46dc6233b)

기준 PDF의 평일 페이지 추출은 한 열의 시간을 세로로 나열한다. 두 번째 SW 철도 열은 06:10부터 Weymouth 도착까지 19개 연속 시각이 있어 같은 19개 정류장 행과 맞는다. 임시표는 각 정류장 행에 여러 열을 가로로 놓는다. 해당 열은 Brockenhurst 출발행의 06:10과 Sway 06:15, New Milton 06:21, Hinton Admiral 06:25 순이다. 표지·요일·공통 기점·직접 다음 정류장을 검사해 동명이거나 인접 출발 열을 배제했다. 9월 두 PDF의 최초 게시 순서, 해당 날짜 여정 계획기의 저장 응답과 실제 운행은 미확인이다. 차이는 같은 서비스일의 두 계획 표면에 한정된다.

MBTA 아카이브는 정정 피드가 잘못된 피드를 대체할 수 있고 GTFS와 운행 성과 자료는 별도라고 명시한다. 웹에서 공식 텍스트 색인은 열렸고 셸의 압축 피드 연결은 차단됐다. 단일 색인 항목을 시간표 값으로 확장하지 않았다. [MBTA-ARCHDOC](https://github.com/mbta/gtfs-documentation/blob/02da961b963ba3d3a66042ca4d5bd19e21ce5c0a/reference/gtfs-archive.md) · [MBTA-LAMP](https://performancedata.mbta.com/) · [MBTA-INDEX](https://cdn.mbta.com/archive/archived_feeds.txt)

통계 링크는 인구·분위·기준기간·단위·표 판, 교통 링크는 서비스일·요일·방향·정류장·열·우선 적용 공지가 답의 경계다. 시각 변경이 실제 운행을 바꾸었는지는 다른 원장이 필요하고, ONS 중위의 개정은 개별 사람 임금 변화를 뜻하지 않는다. 소프트웨어의 29쌍 분모에는 이 분야의 어떤 관측도 가산하지 않았다.
