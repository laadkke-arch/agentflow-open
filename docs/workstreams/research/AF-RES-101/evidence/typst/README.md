# Typst 최초판 모집 기록

H1 질문 27건을 생성시각·숫자ID로 정렬하고 27건의 최초 공개 revision만 읽었다. API가 수신한 54개 revision 중 이후 본문은 코드로 가렸다. 답변·댓글·자기 답·채택 표지는 요청하거나 읽지 않았다. H1에서 두 층이 채워져 H2는 열지 않았다.

선정: TY-A1=77790135, TY-A2=77861495, TY-U1=77876109, TY-U2=77962057. [initial-part.json](initial-part.json)의 body_char 범위는 API revision의 HTML `body` 문자열을 Unicode 코드포인트로 센 0부터 시작하는 `[start,end)` 위치다. HTML 행은 1부터 센다. quote는 읽기 위해 HTML entity를 풀었으며 해시와 위치는 풀기 전 원 HTML을 가리킨다.

`frame-part.csv`는 27건 전부를 포함한다. 제외 #77831146은 최초판의 목표 정렬 형태가 첨부 이미지에만 있고 그 이미지가 두 CDN 철자와 web open에서 보이지 않았다. 현재 제목의 right-aligned를 최초 목적에 소급하지 않았다. #77876109의 LaTeX figure[p]는 명확한 기존 지식·목표의 예시이나 질문자가 실행했다고 말하지 않았다. 그래서 Typst 또는 LaTeX를 실제 사용한 제품으로 넣지 않았다. 이 경우를 호출이 보인다는 이유만으로 실행 시도로 바꾸는 민감도는 본 선정 규칙과 다른 규칙이다.

원 API JSON과 최초판 전문은 일시 캐시에만 있다. 커밋에는 [acquisition.json](acquisition.json)의 원 URL·UTC·bytes SHA, 짧은 발췌·위치·본문 해시, [실패 응답](initial-images.json), [단계별 노출](exposure.json)을 남겼다. `recruit.py h1`은 공개 API를 다시 읽는 스크립트이고 `code_initial.py`는 고정한 분석자 판단이다. 재실행은 현 시점의 삭제·편집을 반영할 수 있으므로 API bytes SHA가 달라져도 곧바로 최초 본문 해시가 바뀌었다고 보지 않는다.
