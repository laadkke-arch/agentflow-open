# 후속 설계자가 따로 채택·폐기할 수 있는 링크 반환 선택지

이 파일은 [제품 연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/49f603a98188fbf2009c4c490b0539f32d124e38/docs/product/RESEARCH_BRIEF.md)의 전체/부분 설계와 목적에 맞는 링크 제공을 위한 연구 제안이다. 데이터베이스·크롤러·AgentFlow API·화면 계약을 확정하지 않는다. 주 표본의 예측·실측, 실제 열람 비용, 관측 범위는 RESULT와 원장을 우선한다.

| 독자가 해결하려는 일 | 채택할 수 있는 반환안 | 이 조사에서 지지한 실제 부분·기능/원리 | 폐기하거나 제한할 조건 |
| --- | --- | --- | --- |
| 과거 문서의 예제·그림을 정확히 인용 | 옛판 고정 절·그림·source와 판 식별을 함께 반환 | [ggplot2 3.4.0 scale_shape 고정 본문](https://github.com/tidyverse/ggplot2/blob/57852124c86f770dd443fcf5064d30ea320a4731/reference/scale_shape.html), [Matplotlib 3.6.3 barchart](https://matplotlib.org/3.6.3/gallery/lines_bars_and_markers/barchart.html#grouped-bar-chart-with-labels). 새 그림이 더 적절해 보여도 역사적 대상·데이터를 바꾸지 않는 인용 | 독자가 실제로 비교 대상 새판의 코드/API만 원하는 경우에는 옛 링크만으로 충분하지 않음. 정확 HTML 위치와 payload는 returns.csv 참조 |
| 사라진 이름의 기능을 다음 판에서 사용 | 공식 rename/삭제 기록과 새 실제 절을 확인한 뒤 새 절로 교체 | [bullseye의 실제 새 예제](https://matplotlib.org/3.7.0/gallery/specialty_plots/leftventricle_bullseye.html#left-ventricle-bullseye), [rotation mode 통합 예제](https://matplotlib.org/3.7.0/gallery/text_labels_and_annotations/demo_text_rotation_mode.html#text-rotation-mode). 정적 redirect + 새 코드 + 실제 자원의 연결이 경로 부재 NO를 뒤집음 | 제목/그림 유사성만 있고 공식 계보 또는 목적 코드가 없으면 유보. 정확 옛 fragment의 브라우저 전달은 정적 redirect 존재와 별도 미확인 |
| 시각 역할은 유지하되 구체 데이터/방법의 변경을 알고 선택 | 두 판 병기, 일반 역할·원 목적·방법의 차이를 짧게 명시 | [barchart 새판](https://matplotlib.org/3.7.0/gallery/lines_bars_and_markers/barchart.html#grouped-bar-chart-with-labels)은 같은 그림 경로에서 penguin 데이터로 바뀌고 bar/bar_label 원리는 유지. [rotation 새판](https://matplotlib.org/3.7.0/gallery/text_labels_and_annotations/demo_text_rotation_mode.html#text-rotation-mode)은 default 설명을 유지하며 bbox 강조 구현 변경 | 모든 차이를 같은 중요도로 제시하면 확인 부담만 증가. 독자 목적이 특정 데이터인지 일반 비교 구조인지 불분명하면 한쪽을 자동 대체하지 않음 |
| 전체 화면/문서의 어느 부분을 재사용할지 찾기 | 자원이 어디에 어떤 역할로 쓰이는지 연결해 반환 | [IIIF Presentation 3 Canvas](https://iiif.io/api/presentation/3.0/#53-canvas)·[AnnotationPage](https://iiif.io/api/presentation/3.0/#55-annotation-page), [실제 Rijks manifest](https://iiif.micr.io/PJEZO/manifest)의 painting/thumbnail 구별. 전체 서비스가 다른 분야여도 특정 부분의 참조 구조를 가져올 수 있음 | IIIF 객체 구조를 모든 HTML/소프트웨어에 그대로 강제하지 않음. URL 문자열만 추출하면 painting과 thumbnail·comment의 역할을 구별하지 못함 |
| 설명을 포함한 정확한 링크가 필요 | figure와 그 그림을 쓰는 설명 절을 목적에 맞게 함께 반환 | [JATS fig](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html)·[xref](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html), [PLOS Fig7](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007), [Results](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec022), [Discussion](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec025). 같은 그림도 결과 보기와 원리 설명의 문맥이 다름 | XML id를 HTML fragment로 복사하지 않음. 실제 DOM을 확인. [Table3](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-t003)의 유효하지만 의미가 어긋나는 링크는 자동 교정 근거가 아님 |
| 지금 확보한 근거로 정확한 부분 도착을 보장할 수 없음 | 전체 자료는 제공하고 부분/상태 반환은 유보 | [Fitzwilliam 실물 manifest](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json)의 Choice17과 null 영역 target32. [IIIF Content State](https://iiif.io/api/content-state/1.0/)의 Canvas+Manifest 문맥으로 확인한 범위만 전달 | 실제 viewer의 선택 상태/좌표 fallback을 봤거나 공식 유효 좌표가 생기면 유보 범위를 줄임. 존재하는 작품 전체를 삭제된 것으로 표시하지 않음 |

## 운영 방식도 선택지로 남긴다

**주소/트리만 확인하는 방식**은 후보를 싸게 나누는 데 쓸 수 있다. 이 연구에서 그 신호를 곧바로 목적 보존 판정으로 바꾸면 실제 후계 두 건을 놓쳤다. 경로 M에 대소문자 source 이동57개가 한꺼번에 들어온 ggplot2는 변경 신호가 많다는 사실이 그만큼 많은 의미 변화라는 뜻이 아님을 보여 준다. 현재 관측만으로 상시 전체 크롤러를 필수로 결정하지 않는다.

**요청 시 해당 절을 추가 확인하는 방식**은 반환하려는 목적이 분명하고 대상 수가 적을 때 채택할 수 있다. 옛 URL, 실제 새 DOM, 연결 payload와 source, 필요한 변경 기록 순으로 확인 비용을 지불한다. 최초 링크 실패만으로 삭제를 확정하지 않고, 성공 응답만으로 원 목적을 보증하지 않는다. returns.csv의 추가 성공 GET 수는 실제 조사자의 비용 기록이며 사용자 클릭 수·모델 호출 수·서비스 지연을 측정한 값은 아니다.

**판별 결과를 보존하고 변경 신호에 따라 재확인하는 방식**은 같은 예제를 반복 추천할 때 후보가 된다. 최소 보존 대상은 독자의 원 목적, 고정판 식별, 실제 절 위치, 자원과 source의 관계, 확인 시각/범위, 미확인이다. 모든 원문을 영구 저장해야 한다는 요구로 확대하지 않는다. 이 조사에서 source와 payload의 지문은 서로 다른 판의 자료를 혼동하지 않기 위한 근거였으며, 지문 동일성이 목적 동일성을 증명한 것은 아니다.

## 아직 결정하지 않은 사항

실사용자가 구체적 데이터를 목적의 필수 부분으로 보는 빈도, 허용할 추가 열람 비용, 상시 수집과 요청 시 확인 중 어느 쪽의 비용이 낮은지는 이번 정적 표본에서 측정하지 않았다. 엄밀한 ‘새 절에서 쓰이지 않는 잔류 파일’ 사례도 확인 범위에서 확보하지 못했다. 두 plotting 프로젝트의 옛 두 판과 현재 IIIF/JATS 실물로 얻은 구조적 반례를, 모든 제품·문서의 오류율로 일반화하지 않는다. 후속 설계자는 각 선택지를 따로 채택하고 실제 사용 과제로 다시 비교할 수 있다.
