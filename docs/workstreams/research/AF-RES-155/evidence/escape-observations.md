# ④ 이스케이프 대조 개봉

두 추가 fresh clone의 검사 SHA는 `2cf433e1185fedc499188e786fbf2995a24f86b9`다. 설치 후 `python replay/run.py --tools TOOL_DIR --repeat W3|W4 --phase escape-contrast` 종료 0. [설치 W3](af155-W3-setup.txt) · [설치 W4](af155-W4-setup.txt). 각 네 경로에서 실행한 19개 하위 명령의 stdout, stderr, AST, HTML이 반복 간 일치했다. 실제 입력과 결과는 [runs.jsonl](../runs.jsonl)의 W3/W4에 있다. W3 분량 해시 `ba6dad3b943044ceb7e194b560b9858f2463fe3ab2169dff0fd406c876b8d749`, W4 `9040eb72f98ffd48798f41601e3ba8e902bc52d002b0e79e20150f448b651805`.

같은 템플릿과 같은 nested binding에서 escape 정책만 바꾸면 이중 중괄호가 원시 백틱을 내보낸다. 포맷 이전에 확장했을 때 네 백틱 안의 코드 본문 세 줄이 그대로 저장된다. 포맷을 먼저 했을 때 빈 코드 두 개 사이에 hello가 별도 문단으로 분리된다. 후속 sentinel 문단은 두 순서 모두 독립 문단으로 남았다. 정적 예와 plain binding은 fence 길이와 위치 값이 변하더라도 렌더링 HTML과 코드 문자가 같다. 확장부터 하고 formatter에 넘기면 실제 내부 백틱 때문에 네 개가 유지된다. 이 구성에서는 CRLF→LF로 인해 정확한 문서 바이트가 달라져도 HTML과 블록 내용이 같다.

원문 예와 같은 raw 확장 줄을 얻은 기록은 `X05-raw-nested-example`이다. 기본값 결괏값과 이 구성 결괏값을 모두 보존하며 실제 저자의 렌더러 판이나 설정은 미확인이다.
