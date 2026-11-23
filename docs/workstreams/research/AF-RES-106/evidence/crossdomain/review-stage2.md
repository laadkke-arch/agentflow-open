# Stage2 별도 경로·선정·예측 검토

검토 UTC: **2026-11-23T23:52:51.252267+00:00**. 같은 계열의 별도 AI 작업자가 ggplot2/Matplotlib 저자들의 계산을 독립적으로 다시 계산했다. 사람 검토는 없다. 허용된 새 tree의 **경로·blob ID·변경 종류 및 commit ID/시각**만 읽었다. 새 HTML·예제 source 내용·그림·patch·commit 설명은 직접 열지 않았으며 횟수는 모두 **0**이다. GG 옛 source archive와 옛 barchart 본문은 읽을 수 있는 범위로 다시 확인했다. 이 검토가 늘리는 고유 신규 자료 수는0이다.

## 1. 결론

배타적12쌍·24판 자리가 맞다. 실제 후보가 배정된 쌍8, 결원4이고, 실제8의 예측은 YES6/NO2/유보0이다. **예측의 맞고 틀림은 아직 미확인**이다. 경로만으로 판단한 단계이므로 실제 목적 양성/음성 분모나 TP/FP/FN/TN을 여기서 산출하지 않는다.

| 프로젝트 | 옛 전체 frame | 적격 | A | M | G | 실제 배정 | 결원 | 예측 YES/NO/유보 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ggplot2 | 195 | 68 | 0 | 57 | 11 | 4 | 2 | 4/0/0 |
| Matplotlib | 608 | 479 | 3 | 0 | 476 | 4 | 2 | 2/2/0 |

803행의 기존 적격·제외·옛 절·목적·API·자원·소스·지문·해시는 Stage1과 같다.547적격의 SHA256(AF106|project|old_section_path)을 독립 계산했고, A→M→G 우선순위와 층별 hash/경로 정렬 첫2를 다시 구했다. 경로 신호 불일치0, hash 오류0, 선택·예측·임시 URL 오류0이다. 임시 URL은 실제 확인된 도착주소가 아니며 새 DOM·참조·표시·목적은 **미확인**이다.

전체 계산, 입력 SHA256, source-map 검산과 source DAG 명령의 종료값은 [review-stage2.json](review-stage2.json)에 보존했다.

## 2. 선정12자리

| 자리 | 옛 절 경로 | 봉인 전 예측 | 결원·판단 근거 |
|---|---|---|---|
| GG-A1 | 결원 | 미확인 | 후보0; 예측 유보 아님 |
| GG-A2 | 결원 | 미확인 | 후보0; 예측 유보 아님 |
| GG-M1 | reference/scale_shape.html#ref-examples | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |
| GG-M2 | reference/geom_segment.html#ref-examples | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |
| GG-G1 | reference/position_jitterdodge.html#ref-examples | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |
| GG-G2 | reference/scale_linewidth.html#ref-examples | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |
| MP-A1 | gallery/specialty_plots/leftventricle_bulleye.html#left-ventricle-bullseye | NO | 완전 새 트리의 옛 대표 경로 존재/부재 |
| MP-A2 | gallery/text_labels_and_annotations/text_rotation.html#default-text-rotation-demonstration | NO | 완전 새 트리의 옛 대표 경로 존재/부재 |
| MP-M1 | 결원 | 미확인 | 후보0; 예측 유보 아님 |
| MP-M2 | 결원 | 미확인 | 후보0; 예측 유보 아님 |
| MP-G1 | gallery/spines/multiple_yaxis_with_spines.html#multiple-yaxis-with-spines | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |
| MP-G2 | gallery/lines_bars_and_markers/barchart.html#grouped-bar-chart-with-labels | YES | 완전 새 트리의 옛 대표 경로 존재/부재 |

신호 원자료 URL은 [GG 새 발행 tree](https://api.github.com/repos/tidyverse/ggplot2/git/trees/392175bbb00b04025aa5d17a0c18b3896adeb40f?recursive=1), [GG 새 source tree](https://api.github.com/repos/tidyverse/ggplot2/git/trees/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd?recursive=1), [MP3.7.0 전체 배포 tree](https://api.github.com/repos/matplotlib/matplotlib.github.com/git/trees/94eb9c8195d36c3cc1a36876409629a115b5a9ae?recursive=1), [MP 실제 발행 source revision tree](https://api.github.com/repos/matplotlib/matplotlib/git/trees/235131a6bc2527aee7eea370fd5f94564a48c20d?recursive=1)다. 수신 JSON들은 truncated=false이고 루트 버전을 제외한 정확한 경로로 대조했다. 대소문자·확장자·옛 fragment를 합치지 않았다.

GG G11에는 옛 source부터 연결이 불명인 translate_qplot_lattice1개가 있다. 이것을 새 삭제로 만들지 않았고 source-map 미확인으로 보존했다. 선택된 G2개는 이 미확인 행이 아니다. 자원 존재가 알려졌으므로 source 관계 미확인과 경로 예측 유보를 혼동하지 않는다.

## 3. source-set 교정과 옛 source-map 검산

원격① ccbc56bb0891a5721e4f53438e431df81fc8b2a3은23:40:33에 확인됐다. 새 경로는 GG23:41:17, MP23:41:31부터 읽었다. source-set 교정1b 1ddac4cec4532121598c3ad3deac4450fc5ac6a5의 원격 확인23:46:44는 부모가 전달한 기록이다. 검토자는 이 커밋의 원격을 별도 네트워크로 재조회한 것은 아니며 현 METHOD_AMENDMENT.md를 읽었다.

이 교정은 **경로·초안 선택 노출 뒤, 새 본문·정답 판독 전**이다. man-only A0/M0/G68 및 잠정 G선택을 본 뒤 확인된 R 저자 소스를 포함하도록 고쳤다. 완전한 사전 신호 비노출 등록으로 표현하면 안 된다. 좁은 기준 초안은 sensitivity-man-only에 보존됐다. 원 예측은 아직 원격 봉인 전이었고 새 결과에 따라 이전 봉인 예측을 덮어쓴 것은 아니다.

GG source-map68행 중67개는 옛 Rd 생성 입력과 문서 source 관계가 확인됐고1개는 미확인이다. 옛 source archive962개 경로와 완전 옛 source tree를 대사했다.67개 Rd의 지문·generated header·examples 존재,91개 author 관계의 원 바이트 SHA256/Git blob/header 연결에서 오류0이다.91은 관계 수이며 독립 저작 수가 아니다. 그중24관계의 R 파일에는 독립 @examples marker가 없으므로 모든 파일이 첫 예제의 모든 줄을 직접 썼다고 확대하지 않는다. 여기서 적용한 연결은 교정 규칙이 허용한 **Rd 생성 provenance+그 문서의 실행 examples**다.

이 결과 source-set을 전체68개에 같은 방식으로 적용해 M57/G11을 얻었다. `.r→.R` 이동은 모집 신호이고 U/API 실패의 증거가 아니다.

## 4. 보조 사건 순서·중복·대조 자료

| 검산 | ggplot2 | Matplotlib |
|---|---:|---:|
| old..new source DAG commit 수 | 352 | 1374 |
| 차이 DAG 안 shallow 경계 | 0 | 0 |
| 읽은 D/R 경로 metadata 사건 | 4 | 14 |
| 옛 적격 source에 연결된 사건 | 2 | 6 |
| 시각 UTC/SHA순 최대10 선택 | 2 | 6 |
| 선택·정렬 불일치 | 0 | 0 |
| 선택 사건에 연결된 유일 옛 예제 | 57 | 3 |
| 그중 주표본 밖 옛 예제 | 55 | 1 |

검토자가 `git rev-list OLD..NEW`를 실행한 종료값은 두 프로젝트 모두0이다. 결과 ID들과 shallow 경계의 교집합은0이고 metadata 사건들은 모두 해당 DAG에 포함된다. commit message/patch는 열지 않았다. 보조 후보의 시간 정렬은 원 문자열이 아니라 timezone을 UTC로 변환한 뒤 SHA순으로 수행했다.

GG04a5ef274e912bee76180154b25d8bca0206feb1은57개 옛 페이지에 연결되며 주 M1 scale_shape와 M2 geom_segment를 포함한다. b9f43f2a7d93548b0794bc527b0f18ff0f028681의 guide_axis는 앞 사건과 같은 옛 예제 계보다. 처음 기록에서 주 겹침·사건 간 겹침 필드가 빠져 작성자에게 수정을 요청했고,23:50:58 재생성판에 main_overlap/prior_event_overlap와 상세 대표 register_theme_elements/guide_axis가 추가됐다. **사건2건을 독립 예제2건으로, 연결57개를 상세 판독57개로 세지 않는다.** 두 다른 helper 사건은 예제 사건 분모에 합치지 않는 official-change context로 분리했다.

MP6commit은 text_rotation, leftventricle_bulleye, pyplot_mathtext의3경로 사건을 각각 일반 commit과 merge가 반복한 것이다. text_rotation/leftventricle의4commit은 주 A2/A1과 겹친다. 새 보조 논리예제는 주 밖 pyplot_mathtext1개다. merge를 독립 예제로 세면 안 된다. 첫 text_rotation 사건의 committer 날짜가 옛 발행 날짜보다 앞서지만 지정 old..new DAG의 멤버라는 사실을 별도로 보존했으므로 단순 달력 기간으로 탈락시키지 않는다.

자료 하한용 대조도 봉인 전 해시순을 다시 계산했다. GG는 주4를 뺀 첫3인 stat_unique/labs/ggtheme다. MP는 주4를 뺀 첫4인 custom_scale/polys3d/spines_dropped/keyword_plotting, 별도 source-only는 주·본문 대조·이미 직접 본 본문을 뺀 첫3인 tick_labels_from_values/demo_gridspec06/looking_glass다. 모두 실제 파일과 일치했고 주 오류율 분모에 들어가지 않는다.

## 5. barchart 평가 대상·타임라인

옛 원문 [barchart#grouped-bar-chart-with-labels](https://raw.githubusercontent.com/matplotlib/matplotlib.github.com/f3ac5407f8ffc861cae1ea87eddd06c63b222e4b/3.6.3/gallery/lines_bars_and_markers/barchart.html#grouped-bar-chart-with-labels)을 다시 읽었다. 저자 prose는 grouped bar를 만들고 값 label을 붙이는 설명이라고 명시한다. 코드의 구체 대상은 G1..G5, Men/Women, Scores다. 따라서 일반 시각역할과 구체 데이터 목적을 구별할 옛 근거는 있다.

Stage1 원 purpose_visual은 “G1~G5의 Men/Women 점수를 나란한 막대와 수치 라벨로 비교”다. 이 문구와 API는 현 frame/predictions에서 바뀌지 않았다. 일반 grouped-bar 역할·구체 API·literal data의 추가 선언은23:46:41이며 당시 새 본문·정답0 기록이다. 관측된 로그에는 **post-label 변경이라는 증거가 없다.** 다만 경로와 표본을 본 뒤 평가 대상을 더 추상적으로 읽는 실질적 해석 추가이며 단순 표기 변경도, Stage1부터 유일하게 고정된 대상도 아니다.

검토자는 기존 구체 목적 U와 일반 시각역할 U를 둘 다 판정하고 다르면 혼동표·분모를 나누도록 요청했다. 부모의 [EVALUATION_TARGETS.md](../../EVALUATION_TARGETS.md)는 U_original_purpose/U_visual_role/method_inherited/literal_data_identity를 구별하고 두 U의 혼동표를 따로 남기며 원 prediction_U를 소급 축소하지 않겠다고 명시했다. 이 문서가 묶음②에 함께 봉인되는 조건에서 조용한 목표 교체 우려는 해소된다. 실제 사후 판정이 이 계약을 지키는지는 아직 **미확인**이다.

## 6. root 통합·남은 범위

root frame803행, predictions12행과 프로젝트 산출물의 주요 목적·선정·예측·hash를 대사했다. 의미 필드 불일치는0이다. 검토 직전 GG 작성자의23:50:58 재생성으로 root frame의 signal_read_utc만68행 이전 값이었으며 부모에게 최신 프로젝트 파일로 재조립하도록 알렸다. 이 시각 차이는 후보·예측을 바꾸지 않지만 최종 원격 봉인 전에 같은 판본으로 맞춰야 한다. 부모 재조립 후 최종 재검사에서 모든 공통 필드 불일치0으로 동기화가 확인됐다. 최초 시각 차이68행과 최종 재검사 UTC·입력 지문은 JSON에 함께 보존했다.

원격② 확인은 검토 당시 아직 전이며, 사후 DOM·후계·방법·당시 생성G·반환 fragment·오류율은 이번 검토가 검증하지 않았다. 타임라인의 열람0은 작업자 기록과 허용된 읽기 범위에 근거하며 모델의 사전 학습 지식까지 완전히 차단했다는 뜻이 아니다. 자기 검토와 별도 판독을 구별하고 고유1차 자료 수를 검토 재열람으로 늘리지 않는다.
