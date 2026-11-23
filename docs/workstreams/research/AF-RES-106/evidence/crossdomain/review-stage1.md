# Stage1 별도 판독·검산 기록

검토 기준 UTC: **2026-11-23T23:41:13.451253+00:00**. 검토자는 Q7 작성자이며 ggplot2/Matplotlib 모집 코드 작성자와 별개인 동일 계열 AI다. 사람 검토는 없었다. **Q7 전체를 독립 검토했다고 부르지 않는다.** 별도 검토 대상은 주 연구의 옛판 모집·제외·해시·목적 기록이다. 새판 tree·본문·소스 내용·변경 diff의 직접 열람은 모두 **0**이다. 아래 방법 해석 의견은 부모가 전달한 경로 관측에 대한 검토이며, 검토자가 새 트리를 연 것이 아니다.

## 1. 결과와 범위

두 프로젝트 합계803개 frame 행을 기계적으로 대사했다. 현재 파일에서 산술·경로·지문·해시·필수 목적 빈칸의 남은 blocker는 찾지 못했다. 의미 판독은 아래15개 옛 HTML과 동일 첫 payload 묶음에 제한된다. 자동 추출한 모든 목적문을 직접 확인한 것으로 확대하지 않는다. 선택된 행의 정확한 옛 예제 경계·두 목적은 새 본문 개봉 전에 다시 직접 확인할 필요가 있다.

| 검산 | ggplot2 | Matplotlib |
|---|---:|---:|
| 완전 옛 트리 내 모집 경로 | 195 reference HTML | 608 gallery HTML |
| 유일 frame 행 | 195 | 608 |
| 적격 | **68** | **479** |
| 제외 | 127 | 129 |
| 인수한 첫40 제외 | 40 | 40 |
| 이미 교정한 예제 제외 | 2 | 2 |
| 적격 목적 빈칸 | 0 | 0 |
| 선정 hash 재계산 불일치 | 0 | 0 |
| 적격 index/실행요약 페이지 | 0 | 0 |
| SHA-256 및 Git blob을 원 바이트와 대조한 HTML | 195 | 515 |
| HTML 지문 불일치 | 0 | 0 |
| 적격 대표 자원 옛 트리 부재 | 0 | 0 |
| 대응 소스의 옛판부터 존재 불명 | 1 | 0 |
| 대표 외부 그림 | 68 | 440 |
| 대표 Python download | 0 | 39 |

원문·입력 파일 SHA-256·자동 검산값·15개 수동 판독 receipt는 [review-stage1.json](review-stage1.json)에 있다. 검산에서 새 고유 1차 자료 수 증가는 **0**이다.803개 행이나710개 지문 검사를 직접 읽은 독립 저작 수로 세지 않는다.

GG 옛 배포 archive 파일3076개 경로는 완전 Git tree의 blob 경로와 정확히 같았다. 모든195 reference HTML이 frame에 한 번씩 있고 누락/추가가 없다. MP의608 gallery 경로도 완전 고정판 tree와 같았다. MP 실제 HTML 지문 검사는479적격+36리디렉션=515개이며, 첫40+교정2+index/실행요약51을 다시 직접 읽은 것으로 계산하지 않는다.

원자료: [GG 고정 발행 reference](https://github.com/tidyverse/ggplot2/tree/57852124c86f770dd443fcf5064d30ea320a4731/reference), [MP 고정 발행 gallery](https://github.com/matplotlib/matplotlib.github.com/tree/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/gallery), [102 고정 frame](https://github.com/laadkke-arch/agentflow-open/blob/092f4c5c56451bceb53e632f4bddf33db6cda168/docs/workstreams/research/AF-RES-102/frame.csv).102의 eligible=YES40집합과 대사했고 두 프로젝트 모두 기존40이 다시 적격으로 들어온 행은0이다.

## 2. 발견한 결함과 교정

### R1 — GG 내부 논리 예제 중복4개: 봉인 전 교정

처음 잔여72에는 첫 출력의 데이터·시각 목적·API 방법이 같은 페이지 별칭4개가 있었다. 옛 HTML에서 첫 그림까지 code/data/API를 읽었고 같은 PNG라는 사실만으로 제외하지 않았다. 부모와 GG 작성자가 새판 tree/body 개봉 전에 수정하여 현재 적격은68이다. canonical은 옛 page_path 사전순 최소로 정했고 해시순이나 새판 결과로 고르지 않았다.

| 유지 canonical | 제외 별칭 | 같은 첫 논리 예제 근거 | 반대 경우·경계 |
|---|---|---|---|
| geom_point | geom_rug | mtcars의 wt/mpg, geom_point baseline, 동일 첫 payload | stat_identity는 같은 그림이어도 구체 호출이 달라 유지 |
| geom_smooth | gg-add | mpg의 displ/hwy, geom_point+geom_smooth 기본 loess, 동일 첫 payload | 페이지 전체 later examples·제목 기준으로 합치지 않음 |
| scale_brewer | scale_hue, scale_viridis | seed596, diamonds sample1000, carat/price, colour=clarity, geom_point | 뒤 palette API 차이는 이번 첫 baseline 예제와 구별 |

제목만 보면 geom_rug는 rug, scale_brewer는 Brewer palette를 이미 쓴 예제로 오판하기 쉽다. 실제 첫 적격 출력은 해당 later-method 사용 전일 수 있다. `stat_unique`도 첫 출력은 `geom_point(alpha=.1)`이고 다음 출력에서 stat_unique가 추가된다. 현재 frame은 첫 출력 방법을 기록한다. qplot과 상속된 facet_null/theme_get의 동일 그림도 API가 달라 qplot은 유지하는 규칙을 대사했다. qplot 원 HTML 추가 재열람은15개 목록 밖이므로 이 부분은 GG 작성자 alias audit에 의존한다.

기존40 별칭 aes/layer/scale_continuous 첫 산점도의 code/data는 직접 확인했다. theme_get 제외는 frame·작성자의 기존 근거를 대사했고 이번15개 원 HTML 직접 판독에는 포함하지 않았다.

### R2 — MP hyperlinks 목적 API 빈칸: 부모 발견, 옛 원문으로 별도 확인

부모가 hyperlinks_sgskip 목적 API 빈칸을 발견했고 MP 작성자가 옛판만 읽어 고쳤다. 검토자는 imports 다음 첫 실제 동작을 확인했다. 첫 예제는 `plt.scatter` → `PathCollection.set_urls([BBC,Google,None])` → `Figure.savefig("scatter.svg")`다. 후반의 imshow → set_url → image.svg를 첫 방법에 섞지 않았다. 시각 목적은 SVG 산점도 점마다 외부 링크를 붙이는 것이다. SVG 출력·브라우저 클릭은 실행하지 않았고 **미확인**이다.

frame_grabbing_sgskip도 그림은 없지만 writer.saving과100회 writer.grab_frame을 사용하는 실행 source download가 연결돼 적격이다. generic source-code 링크만 있는 문서와 다르다. ffmpeg/Python을 실행하지 않았으므로 당시 동영상 생성·GUI 표시를 확인한 것은 아니다.

### R3 — MP 제외규칙 문장: 경미한 모호성

검토 당시 STAGE1_RULES.md에는 “`index.html`, `sg_execution_times.html`, 첫 설명용 그림…”이라는 연결이 있어 ‘는 제외한다’라는 동사가 빠져 있었다. 저자에게 명시하도록 전달했다. 실제 해당51개 제외·적격 index0은 정상이며 산술·선택을 바꾸는 blocker가 아니다. 후속 수정 여부는 부모가 최종 파일에서 확인한다.

## 3. 직접 판독한 원 HTML

모두 고정 옛 발행판에서 이미 수신한 원 바이트를 다시 읽었다. 새 네트워크 요청·신규 자료로 계산하지 않는다. 원 HTML과 첫 코드/자원·리디렉션의 실제 receipt는 JSON manual 배열의 같은 path다.

| 프로젝트 | 원문 URL | 실제 절/위치 | 직접 확인 범위 |
|---|---|---|---|
| ggplot2 | [`reference/aes.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/aes.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/layer.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/layer.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/scale_continuous.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_continuous.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/geom_point.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_point.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/geom_rug.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_rug.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/geom_smooth.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/geom_smooth.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/gg-add.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/gg-add.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/scale_brewer.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_brewer.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/scale_hue.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_hue.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/scale_viridis.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_viridis.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/stat_identity.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/stat_identity.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| ggplot2 | [`reference/stat_unique.html`](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/stat_unique.html) | ref-examples | 원 HTML의 첫 그림까지 code/data/API·별칭 경계 |
| Matplotlib | [`gallery/animation/frame_grabbing_sgskip.html`](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/gallery/animation/frame_grabbing_sgskip.html) | frame-grabbing | 그림 없는 실행 source download·첫 예제 목적 |
| Matplotlib | [`gallery/misc/hyperlinks_sgskip.html`](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/gallery/misc/hyperlinks_sgskip.html) | hyperlinks | 그림 없는 실행 source download·첫 예제 목적 |
| Matplotlib | [`gallery/lines_bars_and_markers/scatter_symbol.html`](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/gallery/lines_bars_and_markers/scatter_symbol.html) | meta refresh | 명시적 meta refresh로 별칭 제외 |

GG `reference/translate_qplot_lattice.html`는 옛 발행 HTML·그림·실행 코드가 있으나 대응 같은 이름 man/저자 source가 지정 옛 source tree부터 없다. source_mapping_limit로 남긴 점은 타당하다. **옛판부터 연결이 불명인 것을 새판에서 삭제됐다고 만들면 안 된다.**

## 4. 경로 관측 뒤 소스 정의에 관한 방법 의견

부모는 경로만 본 뒤 “man 경로는 유지되지만 옛 HTML이 가리킨 R/*.r 다수가 *.R로 rename됐다”고 전달했다. 검토자는 새 트리나 새 코드/정답을 열지 않았다. 이 시점 예측 원격 봉인은 아직 없었다.

사용자 Q2는 ‘예제 소스 경로가 사라지거나 이동’을 M 조건으로 삼고 대소문자를 보존하라고 했다. 옛 예제와 저자 R의 @examples/첫 코드/생성 관계가 확인되면 R 경로의 .r→.R 이동도 M에 포함하는 것이 요구에 더 충실하다. man-only 기준을 주 결과에 고수하고 관측한 저자 이동을 보조로만 돌리는 것보다 다음과 같은 명시적 해석 교정을 권한다.

1. 원격 묶음①은 그대로 보존한다.
2. 원래 man-only 문구, 지금까지 노출된 경로 사실, 새 본문·정답0, 변경 이유·UTC를 기록한다.
3. 연결이 확인된 옛 example source set 전체에 같은 규칙을 적용한다. 단순 구현파일이라는 이유만으로 모든 R 링크를 자동 포함하지 않는다. 연결 불명은 **미확인**이다.
4. 해석 교정 커밋을 원격 확인하고 모든68행의 M/G를 재계산한 후 선정·예측을 봉인한다. 원래 man-only 층은 민감도 부록으로 보존한다.
5. ‘경로 집합 노출 뒤·정답 열람 전 교정’으로 명시한다. 완전 사전등록으로 부르지 않는다. 대소문자 이동은 표집 신호이고 U/API 소멸의 증거가 아니다.

이 의견은 실제 새로운 M 분모·선택 결과를 확인한 판독이 아니다. 부모가 채택한 규칙·원격 커밋·source-example 연결 완전성은 후속 기록에서 확인해야 한다. 자세한 판단과 시각은 JSON stage2_source_rule_interpretation_review에 남겼다.

## 5. 남은 한계

모집 경로·합계·지문·해시는 전수 기계 검산했지만 모든547개 적격(68+479)의 의미·첫 예제 경계를 수동 전수 판독한 것은 아니다. MP의 source-blob-only 별칭 판단은 현 잔여에서 실제 후보0이므로 현재 false exclusion을 찾지 못했지만 같은 source 파일 안에 다른 예제가 있을 수 있어 무조건적인 동일성 규칙으로 확장하면 안 된다. 현재 동일 eligible source blob 그룹은 두 프로젝트 모두0이다.

새 본문/정답을 보지 않았으므로 P/U/API/G 사후 판정, 새 fragment 도착, 예측 오류율·반환 선택은 검증 범위 밖이며 **미확인**이다. 원문 표시와 예제 code 실행도 미실시다. 자료 직접 열람 최소량에 이 검토 재열람을 더하지 않는다.
