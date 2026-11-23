# AF-RES-100 · Pandoc 공개 후속 대조

사전 판정 원격 봉인 `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673` 뒤에만 이 파일의 자료를 열었다. 최초 답·질문 수정·현재 채택·댓글은 공개 Stack Exchange API 원문으로 직접 읽었다. `outcomes.jsonl`의 네 행과 `sources.jsonl`의 27행이 이 보고의 원장이다. **봉인된 32개 사전 판정은 바꾸지 않았다.** 아래 공식 자료 추가 열람은 반환 링크와 한계 설명에만 쓴다.

## 후속·귀속 표

| 질문 | 최초 답·수정·현재 채택 | 30일 안 질문자 후속 | 같은 판·원 입력·필수 출력 확인 | 사전 요구 해석에 주는 영향 |
| --- | --- | --- | --- | --- |
| P1 · 79692729 | 답 0. 질문자는 revision 2에서 Pandoc 옵션 설명과 태그를 추가 | 댓글 140579507에서 앞 수정함수 제안과 같은 방식을 이미 쓰고 있으며 더 쉬운 길을 원했다고 응답 | **미확인**. 원 helper 코드, SVG/EMF 실물, PPTX 결과, 설치판 없음 | helper 허용 주해석은 유지할 수 있으나 새 유용성이나 내장/easier-default 요구 충족으로 확대할 수 없음 |
| P2 · 79701174 | 답 0. 질문 revision 1만 있음 | 없음. 약 1년 뒤 제3자 댓글 141111863만 있음 | **미확인**. 원문 Typst PDF 성공과 상대 import 성공은 실패한 CeTZ→Markdown 목표와 다름 | import 보존 조건을 낮추거나 dummy workaround를 인정할 공개 근거 없음 |
| P3 · 79703916 | 답 0. 질문 revision 1만 있음 | 댓글 140597463에서 base Dockerfile부터 시작한 구성이 작동한다고 자기보고 | **미확인**. 작동 Dockerfile·image digest·custom template·PDF 결과가 공유되지 않음 | 파생 image 접근의 수용은 지지하지만 원 목표 완전 재현과 당시 최신판 규칙을 입증하지 않음 |
| P4 · 79714790 | 첫 답 79714812, revision 1 한 건, 현재 채택. 현 본문과 최초 답 본문 동일 | 답 뒤 실행 후속 없음. 답 전 질문자 용어 교정은 있음 | **미확인**. 같은 title 값과 제안은 있으나 Pandoc 2.18 원 명령 실행 로그는 없음 | 주 도구 YAML 절과 인용부호 예시가 같은 문제를 다루는 점은 일치. PDF 전체 성공으로 확대 불가 |

현재 채택은 **1/4**, 30일 안 **실질적인 질문자 댓글 후속은 2/4**, 질문자 문서 수정은 **2/4**, 둘 중 하나라도 관측된 질문은 **3/4**다. 답 전 맞춤법·용어 교정을 해결 수용으로 세지 않는다. 동일 판·동일 원 입력·동일 필수 출력의 실제 성공을 확인한 질문은 **0/4**다. 공개 댓글은 5개이며 현재 API에 남지 않은 삭제 자료까지 복원한 값이 아니다. 채택 시점은 API 현재 snapshot에서 알 수 없어 30일 내 채택으로 세지 않았다.

## P1: 사용자는 수정 방식을 이미 쓰고 있었다

[질문자 댓글 140579507](https://stackoverflow.com/questions/79692729#comment140579507_79692729)은 `2025-07-10T10:54:35Z` 작성이며 owner `7981566`이 질문 owner와 일치한다. `reply_to_user=903061`은 [Gregor Thomas의 댓글 140574340](https://stackoverflow.com/questions/79692729#comment140574340_79692729), `2025-07-08T16:11:09Z`와 연결된다. 원문·정확한 HTML body·응답 지문은 Git에서 제외된 `_cache/comments.json`과 커밋 가능한 `retrieval-receipts.json`, source `POST-COMMENT-140579507`에 대응한다.

핵심 짧은 원문은 **“Yes, this is actually what I'm currently doing.”**이다. 앞 댓글은 `include_graphics` 수정 버전에 파일 형식 선호·존재하는 파일 탐색·출력 형식별 선택을 넣는 아이디어를 제안했다. 따라서 질문자의 말이 이 제안에 대한 포괄적 긍정이라는 점은 확인된다. 그러나 실제 코드가 없어서 전역 helper를 정의했는지, 각 파일의 확장자를 수동 선택하는지, 제안한 자동 선택의 모든 세부를 구현했는지까지 확정할 수 없다. 질문자는 더 쉬운 방법을 원했다고 이어 말한다. 이 말은 **새 helper를 도입하여 처음 성공했다는 보고가 아니다.**

사전 주해석은 전역 설정 또는 한 번 등록한 helper를 허용했다. 따라서 BF의 문서 근거 완결 판정을 사후에 지우지 않는다. 동시에 이 한 사례를 “인접 링크가 질문자에게 새 해결책을 제공했다” 또는 “내장 기본 옵션 요구를 충족했다”라고 부르면 후속과 어긋난다. native-only 민감도와 사용자에게 실제로 새 도움이 되었는지는 분리해야 한다.

고정 knitr 1.50 [API 설명](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/man/include_graphics.Rd#L6-L24)과 [구현](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R#L435-L459)은 `auto_pdf`가 LaTeX 출력에서 존재하는 PDF로 치환하는 범위임을 확인시킨다. 범용 SVG/EMF 내장 선호 옵션이나 실제 PPTX 출력 성공을 보여 주는 자료는 아니다. 두 파일은 같은 저작 계보의 API 설명과 구현이며 독립 사건 둘로 세지 않는다.

질문자의 [revision 2](https://stackoverflow.com/revisions/CAA8E83F-E796-4E6E-B94E-D4AB802B07F0/view-source)는 `2025-07-08T10:45:08Z`에 Pandoc 옵션 시도와 태그를 추가했다. 이것은 최초 본문에 Pandoc이 없었다는 모집 표시를 사후에 바꾸는 근거가 아니다. 옵션이 확장자가 없는 Markdown 이미지에만 맞고 knitr 출력에는 확장자가 있다는 설명은 질문자의 보고로 귀속하며, 표기된 YAML/CLI를 실제 실행한 것으로 취급하지 않는다.

## P2: late suggestion은 해결 관측이 아니다

현재 질문은 수정되지 않았고 답도 없다. 댓글 141111863은 `2026-07-14T20:30:34Z`, 작성자는 `15685387`이며 질문자 `5443120`과 다르다. Showman README의 CeTZ 예를 가리키며 해당 명령이 안 되는지 묻는 내용이다. 30일 범위 밖이고, 실행 성공·질문자 수용·유지관리자의 확인 중 어느 것으로도 분류하지 않았다. 연결된 가변 README는 이번 결과의 판정 근거로 새로 가져오지 않았다.

[고정 Pandoc 3.6 reader](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Readers/Typst.hs#L56-L79)는 parsing 뒤 evaluator에 파일 읽기 동작을 제공한다. 이 한 파일만으로 evaluator 전체의 패키지 지원 부재까지 증명하지 않는다. [CeTZ 연구판 package](https://github.com/cetz-package/cetz/blob/f91db3185576a92fd121d15d2cd893e18133fd42/typst.toml#L1-L7)는 버전 0.4.0, compiler 0.13.1, entrypoint를 명시하지만 질문이 요청한 0.3.4의 실제 import 성공을 대신하지 않는다.

빈 파일이나 더미 모듈로 오류를 피하면서 결과 텍스트만 같게 만드는 안은 원 library import 의미를 보존했다고 볼 수 없다. 이것은 사전 고정 조건에 따른 해석이다. 공개 후속에 그런 dummy 해법이 제시되었거나 사용자가 허용했다고 주장하지 않는다. 실제 import와 상대 값 123 및 동일 Markdown을 보존한 공개 실행 관측은 여전히 없다.

## P3: 파생 image 수용과 원 PDF 재현은 다르다

[질문자 댓글 140597463](https://stackoverflow.com/questions/79703916#comment140597463_79703916)은 `2025-07-17T15:23:20Z`, owner `14262988`이며 질문 owner와 일치한다. 앞 댓글 140594940은 official image를 base로 확장하는 방향을 제안했다. 질문자는 단순한 base Dockerfile부터 시작하고 명령을 추가하는 방법이 더 쉬웠고 작동하는 Dockerfile이 있다고 응답했다. 그 파일을 공유할 의향은 밝혔지만 공개 thread에는 파일 자체가 없다.

이것은 문제 접근을 바꾸어 작업했다는 자기보고다. 원 custom template·여섯 Markdown 파일·두 filter·동일 image 판·동일 PDF 출력이 확인되지 않아 정확한 원 목표 성공으로 세지 않았다. 반대로 원 목표와 다른 일을 했다고 단정할 수도 없다. 최초 질문에서 이미 보고한 EPUB 성공은 요청한 custom PDF의 성공과 명확히 분리한다.

사후 보조 자료로 읽은 source는 **확인된 오래된 공식 image `3.7.0.0-ubuntu`에 연결된 `7f10864aea88fc746c727f12a61a24cdc0eb93d5`**다. 당시 최신 안정판 source라고 주장하지 않는다. 사전 P3의 latest-stable 결손·비교불가 상태는 유지한다.

- [README](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/README.md)는 volume·user·Pandoc ENTRYPOINT를 설명하고, 파생 image와 공유 data directory의 확장 방법을 제시한다. 일반적인 연결 방법의 근거이며 원 custom PDF의 실행 증거가 아니다.
- [Ubuntu extra Dockerfile](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/ubuntu/extra/Dockerfile#L7-L44)은 LaTeX image에서 파생하고 Python requirements 및 Eisvogel 3.2.0을 설치한다. 사용자 수정 template은 이 기본 template과 동일하다고 가정하지 않는다.
- [추가 Python requirements](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/common/extra/requirements.txt#L8-L10)에는 `pandoc-latex-environment`가 있지만 `pandoc-latex-unlisted`는 명시되지 않는다. 이 목록 하나의 이름 부재만으로 image 전체에 실행 파일이 없다고 단정하지 않는다. 두 번째 filter의 제공 여부는 미확인으로 남긴다.

`ubuntu/minimal/Dockerfile`은 HTTP 404였다. 실패를 자료 수에 넣지 않았고 다른 source를 사전 packet 빈자리로 채우지 않았다. image 실행·PDF 렌더·연구자 예시 입력 생성은 하지 않았다.

## P4: 채택 답은 주 도구의 같은 절을 가리킨다

[답 79714812의 최초 revision](https://stackoverflow.com/revisions/62EA7585-728E-44A7-9606-64E44A9A4864/view-source)은 `2025-07-25T13:34:48Z`, 작성자 Xan (`934239`)이다. 현재 유일 답이며 현재 채택되어 있다. 첫 revision과 현재 본문은 바이트가 같다. 답변자를 Pandoc 유지관리자라고 확인하지 않았다.

답은 YAML escaping 설명과 같은 title 값을 인용부호로 감싸는 예를 제시한다. [연구판 Pandoc 3.6 MANUAL의 해당 절](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L4925-L4934)에서도 같은 규칙과 예를 직접 확인했다. 외부 filter의 설명이 필요한 문제로 바꾸지 않아도 된다.

질문자의 revision 2는 답이 게시되기 전 `semicolon`을 `colon`으로 고쳤고 revision 3은 다른 편집자가 표시 형식을 다듬었다. 둘 다 사용자 설치판 2.18의 원 명령 성공 로그가 아니다. 질문·답 댓글은 현재 API에 없으며 실제 PDF 결과는 읽거나 생성하지 않았다.

## 반환할 링크와 관점

아래는 요청당 최대 두 링크다. 링크 수를 줄였다는 이유로 원 조건 전체를 충족한 것으로 만들지 않는다.

| 질문 | 링크·볼 절 | 실패 조건 한 줄 | 독자 관점 | 유지관리자 관점 | 검색 결과 편집자 관점 |
| --- | --- | --- | --- | --- | --- |
| P1 | [knitr API](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/man/include_graphics.Rd#L6-L24), [구현](https://github.com/yihui/knitr/blob/01bf7eff974903d1498e76e92a3e4b3bf9273cf5/R/plot.R#L435-L459) | 내장/easier-default 요구나 원 SVG/EMF/PPTX 성공은 helper 근거로 대체할 수 없음 | 내장 옵션 범위와 helper 허용을 구별 | 일반 선호형식 API가 필요한지 확인 | 이미 쓰는 우회법을 신규 해결로 표시하지 않음 |
| P2 | [Pandoc reader](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/src/Text/Pandoc/Readers/Typst.hs#L56-L79), [CeTZ package](https://github.com/cetz-package/cetz/blob/f91db3185576a92fd121d15d2cd893e18133fd42/typst.toml#L1-L7) | 실제 0.3.4 import와 동일 Markdown 실행을 보존하지 않으면 미확인 | 실행 가능한 완성 해법이라고 소개하지 않음 | evaluator/package 경계를 원판으로 확인 | 늦은 제안·dummy 통과를 채택/지원으로 승격하지 않음 |
| P3 | [image README](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/README.md#L66-L93) 및 L119–141·174–181, [extra Dockerfile](https://github.com/pandoc/dockerfiles/blob/7f10864aea88fc746c727f12a61a24cdc0eb93d5/ubuntu/extra/Dockerfile#L7-L44) | 당시 최신판·custom 원 파일·두 filter 제공 여부가 미확인 | mount/ENTRYPOINT/파생 image 설명부터 읽음 | 실행 파일과 입력·image digest를 고정 | 자기보고와 완전 재현을 구분하고 오래된 source임을 표시 |
| P4 | [고정 MANUAL](https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/MANUAL.txt#L4925-L4934), [같은 title의 채택 예시](https://stackoverflow.com/revisions/62EA7585-728E-44A7-9606-64E44A9A4864/view-source) | YAML 수정의 타당성을 전체 PDF·filter 성공으로 확대하지 않음 | 짧은 공식 절과 동일 입력 예시 | 문서 예시의 발견 가능성을 유지 | 인접 이름이 있다는 이유만으로 반환 범위를 확장하지 않음 |

## 원장 재계산과 한계

`python -B docs/workstreams/research/AF-RES-100/evidence/outcomes/pandoc/assemble.py`는 내려받은 무시 대상 `_cache`에서 원장과 수치를 재계산한다. 공개 재열람은 `collect.py`로 가능하지만 현재 채택·댓글·본문이 바뀔 수 있으므로 기존 관측을 덮어쓴 새 관측과 혼동하지 않는다. 공개 source 재열람 URL과 모든 response/body SHA-256 및 범위는 source/receipt 원장에 있다. 캐시 전체 원문은 외부 저작 재배포를 피하기 위해 커밋하지 않는다. 캐시 없는 재현자는 API 원본을 다시 받아 고정 revision ID·body SHA-256·구간과 먼저 대조해야 한다. 응답 전체 SHA-256은 당시 획득 영수증이며 quota·현재 metadata가 달라지면 재조회 시 바뀔 수 있다.

최초 답·현재 답·현재 질문·질문 revision·댓글은 각각 구별했지만 동일 원문의 반복 열람을 독립 자료로 세지 않았다. 본 폴더의 모든 source 행은 최소 자료 수 산입을 false로 두었다. 후속 시점 뒤 보조 공식 파일을 읽은 사실은 기록했으며, 그 내용으로 사전 packet 범위를 바꾸지 않았다. 이 대조는 별도 사후 조사자의 작업이며 사용자 실제 실행 검토나 사람의 독립 독해 시험을 수행한 것은 아니다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
| --- | --- | --- |
| P1 broad helper 완결이 사용자에게 새롭거나 더 쉬운 해결이라는 뜻은 아님 | 질문자가 실제 쓰던 helper/선택 코드, 내장 방식 요구 확인, 원 SVG/EMF/PPTX와 설치판 | 전역 helper의 실제 범위와 내장/easier-default 충족 또는 동일 자산의 새 성공이 확인될 때 |
| P2 무후속과 P3 working Dockerfile 자기보고를 정확한 원 목표 성공으로 판단할 수 없음 | P2 실제 CeTZ 0.3.4 import와 test2 출력; P3 공개 working Dockerfile·digest·custom 입력·PDF 결과 | 동일 판·동일 원 입력·필수 출력이 역할을 확인한 사람의 기록에서 일치할 때 |
| P3 확인된 옛 image source가 질문 당시 최신 안정판이라는 근거는 없음 | 당시 build/publish 기록과 해당 image digest→source 연결 | 질문 이전 최신 안정 image의 최초 공개 시점과 source가 확정될 때 strict version 비교를 재구성 |
