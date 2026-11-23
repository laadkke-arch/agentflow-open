# 독립 검토 중 출처 연결 정정

S03 Blueprint의 `studies.json.raw_search_sources`에 CodeMend 열람 실패 BC-F01·BC-F05를 잘못 넣은 것을 제거하고, Blueprint dissertation 최초 timeout인 BC-F06를 추가했다. 원 자료 출처 행 자체와 본문 판정, 표본·배정·시간·품질 수치는 바뀌지 않았다. 영향은 S03 탐색 경로의 실패 출처 ID뿐이다. root의 명시적 요청에 따라 이 분담 파일만 수정했다.

- 종전: ["BC-03", "BC-04", "BC-F01", "BC-F03", "BC-F04", "BC-F05", "BC-M01", "BC-17", "BC-18", "BC-F11"]
- 정정: ["BC-03", "BC-04", "BC-F03", "BC-F04", "BC-M01", "BC-17", "BC-18", "BC-F11", "BC-F06"]
