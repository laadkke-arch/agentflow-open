# ggplot2 경로 신호와 예측 — 새 본문 봉인 전

최종 경로 모집 분모는68이며 A0 / M57 / G11이다. A두자리는 후보0 결원이다. M은 `scale_shape`, `geom_segment`, G는 `position_jitterdodge`, `scale_linewidth`가 hash순 첫2개다. 네 예측은 옛 대표 PNG 경로가 새 완전 tree에 남으므로 모두YES다. 이것은 사용/목적의 사후 정답이 아니다.

원격① `ccbc56bb0891a5721e4f53438e431df81fc8b2a3` 이후 처음 새 경로를 요청한 UTC는2026-11-23T23:41:17.014261Z다. 최초 man-only 해석은A0/M0/G68을 만들었다. 사용자 문언에 맞게 옛 예제와 연결된 저자 source-set도 포함하는 해석 보완을 부모가 별도 원격커밋 `1ddac4cec4532121598c3ad3deac4450fc5ac6a5`으로 봉인했다. 최초 초안은 `sensitivity-man-only/`에 그대로 남았다. 이때 새 본문·그림·commit 설명·patch는 열지 않았다.

`old-author-source-map.json`은 옛 적격68개에 동일한 검증을 적용했다.67개는 실재 Rd의 generated-header가 저자 R 파일을 지명하고 Rd에 실행 예제가 있다.1개 `translate_qplot_lattice`는 옛 source부터 미확인이다. 구현 파일 링크라는 이유만으로 source-set에 넣지 않았다. 공동 Rd 저자 파일 중 직접 `@examples`가 없는 경우도 그 차이를 필드로 보존했다.

새tree에서 옛 그림과 본문·canonical man은 모두 남지만,57개의 확인된 author source-set에는 정확 대소문자 경로가 사라진 파일이 있다. 대소문자를 정규화하여 같다고 처리하지 않았다. `author_path_signals_json`은 원 경로·존재·case-insensitive 후보를 분리한다. casefold 후보만으로 의미적 후계를 확정하지 않는다. source history의 Git `R100`는 정확blob동일의 경로변경 종류이며 전체 예제 사용을 증명하는 자료가 아니다.

보조의 2사건은 같은 old..new source DAG의 예제-linked R/man 이동·삭제 commit을 committer UTC/SHA순으로 전수 선택한 것이다. `04a5ef274e912bee76180154b25d8bca0206feb1`, `b9f43f2a7d93548b0794bc527b0f18ff0f028681`다. 실제 예제 의미는 아직 읽지 않았다. range와 utilities-table의 나머지2삭제 사건은 예제에 직접 연결되지 않으므로 보조 예제 분모에 넣지 않고 공식 변경 맥락 자료로 분리했다.

자료 하한을 위한 별도 대조3개는 주 표본을 뺀 옛 hash순 `stat_unique`, `labs`, `ggtheme`다. 네 주 본문과 다른 논리계보의 payload/source로 자료 범주를 배정한다. 주 오류율에는 넣지 않는다. 추가 old/new 내용 열람은 부모의 묶음② 원격 확인 후 진행한다.

`predictions.csv`의 URL은 검증된 반환 주소가 아닌 임시 주소다. 새 실제 fragment, 그 절의 코드/payload, 구체적 API 방법, 실제 표시, 역사적 생성G는 모두 미확인이다.
