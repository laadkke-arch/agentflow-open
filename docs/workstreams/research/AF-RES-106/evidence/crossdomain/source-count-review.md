# AF-RES-106 — 자료 최소량의 별도 계보 대사

다른 에이전트가 작성한 ggplot2·Matplotlib의 최종 stage3 원장과 최초 봉인판 `8054c2221d4023ba03c904d96f13928219d36c3d`의 원장, 고정 AF102 입력 `092f4c5c56451bceb53e632f4bddf33db6cda168`을 별도로 읽어 대사했다. **보수적으로 사용할 수 있는 신규 1차 저작 38개**는 본문 15개, 그와 계보가 다른 실제 그림·예제 소스 6개, 공식 변경 사건 10개, IIIF/JATS 규격·실물 등 7개다.

통합 원장에 그대로 더할 숫자가 아니다. 정확한 산입 ID38개와 계보 key는 [source-count-review.json](source-count-review.json)의 `counted_ids`와 `canonical_works`를 사용한다. 이전·새판, 본문·그림·코드, 동일 사건의 개별 commit·merge를 합친다. 반복 수신 영수증과 이번 재판독은 추가 산입하지 않는다.

| 범주 | 요구량 | 보수 산입 | 대사 방법 |
|---|---:|---:|---|
| 서로 다른 논리 예제의 발행 본문 | 8 | 15 | GG6 + MP9. MP9 중 봉인판에서 이미 직접 읽어 산입했던6개를 유지하고, 새3개만 추가 |
| 위 본문과 다른 계보의 실제 그림·예제 소스 | 6 | 6 | GG `stat_unique`, `labs`, `ggtheme`의 실제 PNG3개 + MP `tick_labels_from_values`, `demo_gridspec06`, `looking_glass` source3개 |
| 발행·공식 변경/리디렉션 사건 | 6 | 10 | GG5 + MP5. MP의 동일 diff인 merge3개는 모두 중복0. 과거102에서 센 발행 트리·릴리스는 추가 산입하지 않음 |
| IIIF 규격·실물 / JATS 규격·실물 | 2 / 2 | 필수4, 추가 독립3 | Presentation+Rijksmuseum, JATS+PLOS. 별도 Content State 규격, 기관 기술 안내, Fitzwilliam 소장품은 각각 별도 저작 |
| 전체 | 24 | **38** | 계보 중복0, 산입 ID중복0, 고정102 원장의 동일 예제 경로·사건 SHA 일치0 |

## 실제 그림·소스 여섯 계보

세 GG PNG는 디코드해 직접 보았고, 세 MP Python source는 전체를 직접 읽었다. 같은 시각 구성이나 같은 repo라는 이유로 독립성을 추정하지 않았다. 원본 URL·선택 PNG/source SHA-256과 실제 보존 위치는 JSON의 각 행에 있다.

| 독립 계보 | 실제 읽은 자료와 목적 | 다른 본문 계보와 구별한 근거 |
|---|---|---|
| ggplot2 `stat_unique` | [고정 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/stat_unique-1.png): vs/am 이진 좌표의 점 겹침을 alpha로 드러내는 첫 비교 그림 | 첫 그림의 코드에는 `stat_unique()`가 아직 없다. 함수 이름만 보고 중복 제거 성공 예제로 바꾸지 않음. 본문15에는 이 계보를 포함하지 않음 |
| ggplot2 `labs` | [고정 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/labs-1.png): mpg/wt 점의 연속색 범례 이름을 Cylinders로 변경 | `labs(colour=...)` 목적, 열·범례·코드가 별도 계보이며 `ggtheme`의 범주형 gear와 다름 |
| ggplot2 `ggtheme` | [고정 PNG](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/ggtheme-1.png): gear 범주색과 title/subtitle/caption/tag를 가진 wt/mpg 기본 회색 theme | 자연적인 같은 mtcars 데이터 사용이 같은 그림/예제의 복제라는 근거가 아님. 데이터 열 방향, 범례, 설명·호출이 구별됨 |
| MP `tick_labels_from_values` | [고정 source](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/_downloads/2b7917f5efd95d93b11c49f7a421baeb/tick_labels_from_values.py): formatter callback·MaxNLocator로 tick 값에서 문자 label 선택 | main 및 control 본문9와 다른 예제. 양판 source bytes가 같아 추가3개가 되지 않음 |
| MP `demo_gridspec06` | [고정 source](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/_downloads/82f0e1275a063ac077b19c2162ab5453/demo_gridspec06.py): 4×4 바깥 grid의 각 셀에 3×3 subgridspec·바깥 spine 표시 | 실제 nested GridSpec 소스의 별도 예제. 양판 copy는0 |
| MP `looking_glass` | [고정 source](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/_downloads/3f1ecbb039cffe24c51d1499214bb495/looking_glass.py): circle clip을 button/motion event로 이동 | 정적 문서에서 상호작용이 보이지 않음을 저자 주석이 명시한다. 코드 읽기는 확인했고 GUI 실행은 미실시·미확인 |

## 통합에서 반드시 중복 해소할 행

`GG106-OLD-BODY-stat_unique`는 최초 봉인 원장에서 본문 산입이었다. 최종 원장의 단일 산입을 `GG106-S3-GG-X1-new-payload`에 배정한다면 앞 행을 **같은 계보 중복0**으로 바꾸고 이유를 적어야 한다. 이것은 자료수 범주의 대사이며 봉인 표본이나 예측을 수정하는 작업이 아니다. 같은 원리를 GG old/new 본문 중복에 적용한다.

MP 봉인판에서 유지할 본문6개 ID는 다음과 같다. 대응 stage3 재판독 행은 동일 저작이므로0이다.

- `MP106-old-gallery_specialty_plots_leftventricle_bulleye`
- `MP106-old-gallery_text_labels_and_annotations_text_rotation`
- `MP106-old-gallery_spines_multiple_yaxis_with_spines`
- `MP106-old-gallery_lines_bars_and_markers_barchart`
- `MP106-old-gallery_scales_custom_scale`
- `MP106-old-gallery_mplot3d_polys3d`

추가 본문3개는 `MP106-resume-body-MP-CONTROL3`(spines_dropped), `MP106-resume-body-MP-CONTROL4`(keyword_plotting), `MP106-resume-body-MP-SUP1`(pyplot_mathtext)이다. 봉인판에서 따로 직접 읽었던 hyperlinks_sgskip·ellipse_demo는 이 보수적38개 proof set에서는 산입하지 않는다. 원장을 삭제하지 않고 범위 밖 추가 열람으로0을 유지할 수 있다.

## 공식 사건 중복 대사

| 산입한 주 commit | 추가 산입하지 않는 merge | 확인 |
|---|---|---|
| `f21219be5f7411a38b1598382f16dd7b099ffa9e` text_rotation 삭제·redirect | `dbe0ee669262350aaae877bf7c83c9e9909cd8c4` PR24490 merge | 보존 diff의 `diff --git` 이후 전체 bytes 동일 |
| `0d39834ce0c1d579703672e3890b42806eda2121` bullseye cleanup backport | `7ffc3e4a6a057d6117529163187592816830e9cf` PR24956 merge | 보존 예제 diff bytes 동일 |
| `fca4a5f6f8df0f620f77536f5a8d747da414001f` pyplot_mathtext 제거·text 교정 | `ebba21ad5e0403e3c4df15ca5e7f631428fd5e4d` PR25029 merge | 보존 예제 diff bytes 동일 |

두 barchart 변경은 동일 사건의 commit/merge 두 표현이 아니다. `89562698…`은 2022-08-27 PR23590의 Men/Women→Tea/Coffee 변경이고 `e7101231…`은 2022-12-11 PR24498의 penguin 데이터·loop 변경이다. 각 commit 메시지·실제 diff·시각을 읽었으므로 두 개의 공식 변경 사건으로 산입한다. 같은 논리 예제를 다룬다는 이유로 그 그림을 추가 본문으로 세지는 않는다.

## 재현과 검토 한계

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/crossdomain/source_count_review.py
```

이 검토는 원장 계보·동일 diff·정확 산입 ID와 여섯 그림/source의 직접 열람을 확인한다. 547개 적격 옛 HTML의 모든 예제 경계를 다른 검토자가 다시 전수 판독한 것, 모든 주 U를 독립 맹검 재채점한 것, viewer/GUI 또는 역사적 빌드를 실행한 것으로 부르지 않는다. G는 미확인이다. JSON에 세 입력 원장의 SHA-256을 기록했으므로 후속 변경이 있으면 같은 검토 결과라고 재사용하지 않는다.
