# P2 입력 출처와 재생성

1. `P2-original.qmd`는 ekstroem의 [질문 최초판](https://stackoverflow.com/revisions/0a5a0ed2-f43b-4ae1-8c8d-3e4e47d61cdf/view-source), 2024-04-11 14:27:37 UTC, CC BY-SA 4.0의 코드다. 092는 최초판 API의 HTML code를 추출했다. 여기서는 그 Git blob을 그대로 가져오고 최초판 view-source 코드 줄을 LF로 직렬화해 215바이트 일치를 확인했다. 게시글의 네이티브 업로드 원본 파일은 미확인이다.
2. `P2-sealed-macros.qmd`는 092 연구자가 본문으로 넣은 무인수 빈 재정의다. `P2-answer-macros.qmd`는 tarleb의 [답 최초판](https://stackoverflow.com/revisions/c8a5c488-3b9e-4260-9c49-0750d75a0653/view-source), 2024-04-12 05:45:31 UTC, CC BY-SA 4.0의 코드 두 줄을 같은 위치에 넣은 092 파생본이다. 파생 두 파일 모두 원본 8번째 빈 줄 하나를 두 정의로 바꿨다. 답 최초판 코드와 파생본 8–9행은 LF 포함 61바이트가 일치했다.
3. `*-dual.qmd`는 해당 한 표 파일을 바이트 단위 접두어로 유지하고 [대조 표 본문](appendix.md)을 그대로 붙인 095 파생본이다. 원 표의 첫 행 두 빈 칸은 구조상 헤더 후보이고 Name/Number는 Markdown 구분선 다음 첫 데이터 행이다. 두 번째 표는 값이 있는 헤더를 둔다. [AF-RES-092 입력 지위 및 고정 파일](https://github.com/laadkke-arch/agentflow-open/tree/707216d8a7f2f09948bb79bfb30e9b2d62cde9ef/docs/workstreams/research/AF-RES-092/evidence/next-inputs)

`python -B docs/workstreams/research/AF-RES-095/fixtures/prepare.py --check`는 원/파생 차이를 검사하고 커밋한 부착 파일을 재계산해 대조한다. `--check` 없이 실행하면 부착 파일을 재생성한다. 원 질문 및 답 코드가 포함된 파일의 배포는 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)을 따른다.
