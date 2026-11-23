# CSS와 Calc의 별도 대조

## CSS

Chromium 156.0.8078.79의 700×460 픽셀에서 표 한 개당 파란 바깥쪽 수평 밴드를 세었다. 합성 표는 모든 조건에서 Alpha/411·Beta/522, Delta/633·Epsilon/744를 보존했다. `table`에 숨김을 주면 2/2선이 0/0으로, `table.suppress`면 0/2로 바뀌었다. 첫 표 셀이 solid를 내는 경우 table의 `none`은 첫 표 선을 남겼고 `hidden`은 눌렀다. [합성 입력](../../fixtures/cross/scope.html) · [조건별 규칙·화면 좌표와 값](css.json) · [한 표 출력](one-hidden.png) · [none 충돌 화면](none-conflict.png)

Mozilla 1520138의 고정 [WPT 입력](https://github.com/web-platform-tests/wpt/blob/0ba12e737fd832416b9a29dae9f200b311147517/css/css-tables/border-conflict-resolution.html)과 [기대 화면 입력](https://github.com/web-platform-tests/wpt/blob/0ba12e737fd832416b9a29dae9f200b311147517/css/css-tables/border-conflict-resolution-ref.html)을 같은 브라우저에서 읽어 RGB 픽셀 차이 0을 확인했다. 원 소스와 기대값의 SHA는 css.json에 있다. 최초 실행은 baseline의 빈 스타일 문자열을 Playwright가 거절했다. baseline을 효과 없는 CSS 주석으로 표현한 뒤 같은 입력으로 전체 5조건을 실행했다.

## Calc

LibreOfficeDev 26.8.0.0.alpha0 `2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`에서 두 시트를 포함한 ODS 4개를 독립 사용자 프로필과 같은 `calc_pdf_Export`로 변환했다. 각 PDF는 2page이고 Alpha/411·Beta/522, Delta/633·Epsilon/744를 그대로 읽었다. 공유 Grid 스타일을 둘 다 지정했을 때 검은 격자 path는 페이지별 5·5, 공통 Plain으로 바꾸면 0·0, 서로 다른 Grid/Plain은 5·0이었다. Plain 두 시트의 첫 셀 범위에만 넣은 붉은 상·하단은 첫 페이지에 3개 원 path와 2개 고유 수평선, 두 번째 페이지에 0개였다. 첫 페이지의 아래 선 path가 같은 좌표로 중복됐다. [지문·값·원 path](calc.json) · [공유 격자 PDF](shared-on.pdf) · [격리 PDF](one-explicit.pdf)

합성 ODS는 [생성 코드](../../cross_domain.py)에 고정했다. 공식 [Calc 범위 도움말](https://help.libreoffice.org/latest/en-US/text/scalc/01/05070500.html)과 [셀 테두리 도움말](https://help.libreoffice.org/latest/en-US/text/scalc/guide/borders.html)을 각각 대조했다. 26.2 고정 [원 셀 회귀 코드](https://github.com/LibreOffice/core/blob/afbbd0df0edb6d40b450b0337ac646b0913a760c/sc/qa/unit/subsequent_filters_test.cxx#L958-L1011)는 모델의 테두리를 단언하며 실제 원 C++ 회귀 실행은 미실시다.
