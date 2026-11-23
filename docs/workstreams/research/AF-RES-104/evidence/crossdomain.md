# Q7 · SQLite 재귀 CTE와 CSS Grid의 반례

두 사례의 발췌는 봉인 후에 구성했다. 고정 원 파일마다 W1의 실재 코드포인트 예산을 W2에 그대로 줬다. 원 질문 8건의 분자·분모에는 들어가지 않는다. [구간·검사할 원문 경계와 점수](crossdomain-windows.json)

## SQLite

**질문.** 재귀 CTE 안의 LIMIT 0 또는 음수와 ORDER BY 유무가 결과 행과 작업 큐에 각각 어떤 제약을 두는가?

- 양성 기대는 LIMIT 0이면 재귀 테이블에 행을 추가하지 않고, 양수는 추가 행 수의 한도이며, 음수는 한도를 두지 않는다는 것이다. 내부 ORDER BY는 큐에서 꺼내는 순서를 정한다. 반대 기대는 ORDER BY를 생략한 상태에서 현재의 FIFO 관측을 SQL 계약으로 쓸 수 없다는 것이다. 공식 렌더는 Debian의 버전 고정 SQLite 문서 패키지에서 `./usr/share/doc/sqlite3/lang_with.html`로 읽었다. [공식 설명 §3](https://sqlite.org/lang_with.html#recursive_common_table_expressions) · [고정 운송본](https://deb.debian.org/debian/pool/main/s/sqlite3/sqlite3-doc_3.46.1-7%2Bdeb13u2_all.deb)
- 판별 fixture에서는 5.2.3이 같은 내부 ORDER/한도와 양수 OFFSET을 함께 사용하며 5.3은 LIMIT 5로 정확히 다섯 행을 검증한다. 9.2와 9.8은 0과 음수, 11.1–11.3은 순회 차이를 시험한다. 11.3의 FIFO 기대는 이 코드 버전의 회귀 확인이다. 로컬 3.53.1의 별도 미니 입력 5개는 예상과 일치했다. Tcl 원 suite는 미실행이다. [고정 원 fixture](https://github.com/sqlite/sqlite/blob/f3d536d37825302e31ed0eddd811c689f38f85a3/test/with1.test#L456-L485) · [미니 실행 명령·입력·결과](sqlite-runtime.json)
- 전체 공식 파일의 기본 질의에서 W1 `U[3761,4961)`은 목차 부근이다. W2 `U[249197,249797)`와 `U[249995,250595)`는 내부 LIMIT의 행 수와 ORDER BY의 큐 효과를 보인다. 첫 W2 구간은 음수 LIMIT 문장 중간에서 끝나고, 두 번째는 구현 FIFO 설명의 마지막 경고 앞에서 끝난다. ORDER 생략 시 인출 순서 미정이라는 앞 문장은 살아 있으므로 FIFO 보장을 추론할 근거가 생기지 않는다.
- 같은 파일로 한 사후 스트레스 질의에서는 W1 `U[249586,250786)`에 0·음수와 ORDER BY 및 FIFO 경고가 함께 있다. W2 `U[249686,250286)`, `U[253532,254132)`는 균형 점수 `(2,4)→(2,7)`을 얻으면서 ORDER 규칙·FIFO 경고를 모두 잃었다. 두 번째 구간은 LIMIT을 종료 상한으로 쓰는 후속 예다. 한 질의의 단어가 늘어도 다른 조건의 예외가 사라질 수 있다. 이 프로필은 관측 뒤 골랐으므로 손실 빈도를 추정하지 못한다.
- 원 시험 파일 자체의 두 창은 5.3, 9.2·9.8의 완전한 입력과 기대 짝을 각각 보여주지 않았다. W2는 5.2.3의 명령을 시작하지만 앞 문맥 경계가 테스트 전체 지문을 통과하지 못한다. 시험에 대한 부분 일치를 문서 조건 충족으로 합치지 않았다. [선택·참조 범위](crossdomain-windows.json)

## CSS Grid

**질문.** 자동 최소가 가능한 단일 auto-min 트랙과 scrollable overflow, 고정 0 최소 또는 다중 span의 flex 트랙을 어떻게 구별하는가?

- 양성 기대는 해당 축에서 overflow가 비스크롤 값이고 auto 최소인 트랙을 포함하면 단일 트랙의 자동 최소가 content-based라는 것이다. 반대 기대는 해당 축의 scrollable overflow, auto-min 트랙 부재 또는 flex 포함 다중 span에서 자동 최소가 0이라는 것이다. bare `1fr`와 `minmax(0,1fr)`의 **최소 트랙 함수**가 다르다. 이 규칙은 자손의 그리기나 explicit min-width를 판정하지 않는다. [고정 W3C CSS Grid 1](https://github.com/w3c/csswg-drafts/blob/804b7b0055e80dfaba091e7f32a4bca303e569e3/css-grid-1/Overview.bs#L1285-L1305) · [공표된 W3C Grid 2 §6.6](https://www.w3.org/TR/2025/CRD-css-grid-2-20250326/#min-size-auto)
- 규격의 W1은 서문, W2 `U[1135,1735)`와 `U[51052,51652)`는 빌드 메타데이터의 minmax 일치와 §6.6 조건 목록을 보인다. 두 번째 구간은 그 목록이 적용되는 본문의 첫 문장을 잘랐고 §7.2.1의 bare fr 해석도 빠졌다. 점수 `(1,2)→(5,10)`은 유용한 위치로 이동하는 단서지만 질문 전체의 근거는 아직 부분이다.
- overflow-001은 앞 1,004자로 visible/auto/hidden 세 기대와 스타일을 읽을 수 있어 W1로 충분하다. 현재 spec의 조건은 계산된 스크롤 overflow에 관한 것이고 이 fixture의 visible 문구는 해당 입력 세 가지에 한한다. 단일 축 fixture는 hidden/clip 교차의 기대 4개를 명시한다. 창에 있는 축 설명을 전체 rect 실행으로 환산할 수 없다. [overflow fixture](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/css/css-grid/grid-items/grid-item-min-size-auto-overflow-001.html) · [단일 축 fixture](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/css/css-grid/grid-items/grid-item-minimum-size-single-axis-scroll-container.html#L29-L60)
- WPT 012는 `minmax(0px, auto)`와 200×200 자손을, 018은 `minmax(auto, 500px)`와 100×100 자손을 구별한다. 고정 0 최소와 auto 최소에서 고정 최대에 의한 clamp는 서로 다른 조건이다. 두 픽스처의 해당 스타일과 green/no red 기대는 W1에서 보인다. 로컬 Chromium은 브라우저 샌드박스 오류 또는 startup timeout으로 상류 assertion 0개를 관측했다. 시각 비교와 다중 span/1fr은 실행 미확인이다. [012 fixture](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/css/css-grid/grid-items/grid-minimum-size-grid-items-012.html) · [018 fixture](https://github.com/web-platform-tests/wpt/blob/03d41fe0fe3338c66cb56644b8a1705fe2e7247b/css/css-grid/grid-items/grid-minimum-size-grid-items-018.html) · [브라우저 시도](wpt-runtime.json)

| 담당 | 이 자료를 쓸 수 있는 범위 |
| --- | --- |
| 검색 담당 | 빠른 W1로 단일 fixture의 구체 기댓값을 보낼 수 있다. 규격에서 W2가 더 많은 단어를 찾더라도 내부/외부 절, 스코프와 예외를 연결하는 비용을 따로 계량한다. |
| 독자 | SQLite는 §3의 숫자 예외와 FIFO 경고가 한 절에 필요하다. Grid는 §6.6의 여는 문장과 분기 전체 및 §7.2.1의 최소 트랙 함수를 함께 본다. |
| 유지관리자 | SQLite판 변경 시 규범 문구와 test 9·11의 차이를 확인한다. Grid판 변경 시 overflow 값의 분류, span 분기, 고정 최대 조건 및 연관 fixture의 expected rect와 브라우저 결과를 대조한다. |
