# 감사 정정 이력

2026-11-23 UTC, root의 교차검토가 원시 Boolean 인코딩 검사의 잘못을 발견했다. 최초 `transparent-cis-audit.json` SHA256은 `3f8e0d68f2b1c6dc5de0ec9a10713a3041dfa7c516abcad2a6e46111e699472e`였다. 이 버전은 CSV의 대문자 `TRUE`/`FALSE`를 혼합형 `True`와 비교하여 모든 조건의 `raw_correctness_single_option_per_item`를 false로 기록했다.

실제 파일의 선택 토큰을 직접 확인하고 `strip().upper() == 'TRUE'`로 해석을 수정했다. 조건별 원시 토큰 목록을 출력에 추가하고 단일 선택 여부 assertion을 추가했다. 재실행 결과160명×10문항=1600평정 모두 정확히 하나의 correctness 선택지가 참이다. 이전 false는 결측/중복선택의 증거가 아니었다. 수락 종점이 없다는 J4판정, 배정 분모, 본문 동일성, 클릭 비공백 집계에는 영향이 없다.

원개수 수락을 계산하지 않았다. 정정 이후에도 원시 평정은 네 선택지를 그대로 보존하며 이분화하지 않는다.
