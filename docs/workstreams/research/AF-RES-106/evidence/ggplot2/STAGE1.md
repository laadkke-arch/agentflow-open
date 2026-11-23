# ggplot2 옛판 잔여 모집단 — 새 트리 개봉 전

고정 발행은 `57852124c86f770dd443fcf5064d30ea320a4731`, 저자 source는 `63125db184b6e7d5516007574b5d15acbfd8f470`이다. 새판의 metadata만102에서 계승했으며 새 tree/body는 아직 열지 않았다.

공식 codeload archive 한 번을 받은 뒤 Git의 완전 tree와 모든 경로 및 reference HTML blob을 대조했다. `old-archive-receipt.json`, `old-tree-receipt.json`, `old-archive-inventory.json`이 수신과 전수 범위를 남긴다. 이 단계의 기계 스캔은195개 HTML이며 직접 원 HTML을 자세히 연 자료수와 다르다. archive의 dev/reference는 현재 정한 버전 루트의 reference가 아니므로 분모에 넣지 않았다.

`stage1-frame.csv`는195페이지 전수를 포함한다. 102의 첫40개와098 교정2개, 동일 그림·구체적 호출·데이터 매핑이 일치하는 선행 논리예제 별칭3개를 제외한다. `layer`와 `scale_continuous`의 첫 mpg displ/hwy geom_point는 선행 aes의 첫 그림과 연결된다. `theme_get`의 첫 mtcars mpg/wt geom_point는 선행 facet_null와 연결된다. 같은 그림이어도 qplot 방법은 구체적 호출이 다르므로 제외하지 않는다.

새 트리를 보기 전 별도 AI 검토가 잔여 내부의 동일 첫 예제4개를 추가로 찾았다. `geom_rug`→`geom_point`, `gg-add`→`geom_smooth`, `scale_hue` 및 `scale_viridis`→`scale_brewer`다. 동일 데이터·미적 매핑·그래프 호출과 첫 그림이 모두 같고 대입/직접표현만 다른 경우 같은 논리 예제로 취급하여 페이지 경로 사전순 첫 하나를 유지했다. 세 동일payload 그룹8행을 전수 대사했고, 같은 그림이어도 `stat_identity()`라는 구체적 호출이 다른 `stat_identity`는 유지했다. 따라서 사전 적격 분모는72에서68로 교정됐다. 이것은 새판 결과에 맞춘 수정이 아니며 새 tree/body 열람 전 변경이다. `old-logical-alias-audit.json`에 원 코드·source/payload 근거와 유지/제외 이유를 남겼다.

`translate_qplot_lattice`는 발행 HTML·그림·실행 코드가 있으므로 독자가 받은 예제로 적격이다. old source tree에는 그 문서의 동일 이름 man 파일/저자 R 링크가 이미 없다. 이 연결은 미확인으로 남기며 새 source의 삭제 신호로 오인하지 않는다. 주어진 source revision의 완전 tree에 없는 사실을 그 이전 어느 역사판에도 존재하지 않았다는 주장으로 확대하지 않는다.

첫 Examples의 실제 DOM id, section 경계, 첫 그림과 그 이전 실행 코드를 기계 추출했다. 조건문/loop 전체가 출력보다 먼저 나오는 경우 원본 code prefix에는 여러 표현식이 포함될 수 있으므로 시각 목적·구체적 방법 두 칸에서 첫 그림을 만드는 표현식을 따로 명시했다. 코드가 언급된 것은 실행했다는 뜻이 아니다. `stat_unique`의 첫 그림은 geom_point 비교 기준이며 stat_unique 결과라고 바꾸어 쓰지 않는다.

`old-purpose-annotations.json`은 옛 코드에 대한 작성자 판독이다. `stage1-original-html-review.json`의 hash순4예제는 실제 원 HTML과 remote raw bytes를 따로 대조했다. 새 결과와 무관하게 정한 최소 자료 대조이며 주 표본으로 자동 편입하지 않는다. 자료가 같으면 양판을 한 저작으로 계산한다.

새판은 부모의 묶음① 원격 확인 후 tree/path와 변경 종류만 열며 A→M→G·각2 규칙을 적용한다. 새 본문과 이동삭제 설명/patch는 부모의 묶음② 원격 봉인 전에는 열지 않는다.
