# AF-RES-106 Matplotlib 재개 판독·대사

이 파일은 재개 세션의 별도 AI 판독 결과다. 기존 `STAGE3.md`/`MP_RESULT.md`의 결론을 그대로 인수하지 않고 보존된 원 HTML·실제 PNG·공개 다운로드 소스·공식 diff를 다시 읽었다. 표본/예측은 원격 `8054c2221d4023ba03c904d96f13928219d36c3d` 그대로다. 이 검토는 사람 검토나 새 브라우저/예제 실행이 아니다. 봉인 파일은 수정하지 않았다.

## 주 6자리의 결과

| 자리 | 경로 예측 → 원 구체 목적 / 일반 시각 역할 | 실제 새 절 | P / legacy P / 옛 fragment | 구체 방법·조건 | 반환 |
|---|---|---|---|---|---|
| MP-A1 | NO → YES / YES | [고정 HTML](https://github.com/matplotlib/matplotlib.github.com/blob/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/specialty_plots/leftventricle_bullseye.html#L1026) · `left-ventricle-bullseye` | YES / NO / 미확인 | sealed구체방법 YES; coreAPI YES; 원 recipe NO | 새 절로 교체 |
| MP-A2 | NO → YES / YES | [고정 HTML](https://github.com/matplotlib/matplotlib.github.com/blob/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/text_labels_and_annotations/demo_text_rotation_mode.html#L1026) · `text-rotation-mode` | YES / NO / NO | sealed구체방법 NO; coreAPI YES; 원 recipe NO | 두 판 병기 |
| MP-M1 | 결원 | 미확인 | 미확인 | M후보0; 유보 예측 아님 | 유보 |
| MP-M2 | 결원 | 미확인 | 미확인 | M후보0; 유보 예측 아님 | 유보 |
| MP-G1 | YES → YES / YES | [고정 HTML](https://github.com/matplotlib/matplotlib.github.com/blob/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/spines/multiple_yaxis_with_spines.html#L1026) · `multiple-y-axis-with-spines` | YES / YES / NO | sealed구체방법 YES; coreAPI YES; 원 recipe YES | 새 절로 교체 |
| MP-G2 | YES → NO / YES | [고정 HTML](https://github.com/matplotlib/matplotlib.github.com/blob/410d8388303fab638bbedbd1d2eace0e5efb0de9/3.7.0/gallery/lines_bars_and_markers/barchart.html#L1026) · `grouped-bar-chart-with-labels` | YES / YES / YES | sealed구체방법 YES; coreAPI YES; 원 recipe NO | 두 판 병기 |

`lineage-final.json`은 결원 포함 12판 자리다. `returns-final.json`은 6자리의 고정 HTML·실제 DOM id·발행 PNG·소스와 판정을 바꿀 조건, 읽기 비용을 제공한다. 반환의 live version URL은 3.7.0 비교판의 편의 링크이며 현재 최신판 보장이 아니다. raw HTML의 `#fragment`는 DOM 위치 식별 기록이다. raw endpoint가 HTML을 렌더한다는 뜻이 아니므로 GitHub의 고정 `#L행`과 실제 version 사이트의 DOM fragment를 나누어 둔다.

### A1: 경로 소멸 뒤의 명시적 rename

[공식 변경](https://github.com/matplotlib/matplotlib/commit/0d39834ce0c1d579703672e3890b42806eda2121)은 `leftventricle_bulleye.py`를 `leftventricle_bullseye.py`로 88% 유사도 rename하고 `redirect-from`을 추가한다. 실제 새 절·소스는 `bullseye_plot`, polar `pcolormesh`, 경계선 `plot`, 데이터 1…17, 세 색상표와 강조 분절을 보존한다. 소스·명시적 변경·새 절이 연결되므로 이미지 외형 또는 파일명만으로 후계라고 판단한 것이 아니다. 옛 PNG 경로는 새 완전 트리에 없지만 U는 YES다.

새 그림은 1000×500이고 옛 그림은 1200×800이다. 원 colorbar 배치의 `fig.add_axes`는 `Axes.inset_axes`와 constrained layout으로 바뀐다. 17분절을 만드는 핵심 방법과 이 보조 배치 recipe를 분리한다. 새판 독자가 17분절 방법을 찾는 조건에서는 새 절로 교체한다. 옛 절의 배치를 인용하려는 조건이면 보존된 옛판 고정 URL을 쓴다.

옛 새판 경로의 HTML은 `meta refresh`만 있고 fragment id는 없다. redirect target에는 옛 `left-ventricle-bullseye` id가 있으나 브라우저의 fragment 전달·실제 이동은 미실시이므로 옛 주소 도착은 미확인이다. 새 target과 정확 id를 직접 반환할 수 있다는 사실과 구별한다.

### A2: 설명 목적의 통합과 방법 일부 교체

[삭제 변경](https://github.com/matplotlib/matplotlib/commit/f21219be5f7411a38b1598382f16dd7b099ffa9e)은 두 예제의 내용 중복을 명시하고 더 완전한 `demo_text_rotation_mode` 예제로 redirect한다. 새 HTML의 목록 항목은 default mode가 먼저 회전한 뒤 회전된 bounding box를 정렬한다고 설명한다. 코드의 default 분기와 실제 그림의 default/anchor 비교를 읽었다. 이것은 옛 설명 목적을 계승한다.

다만 봉인된 specific target은 `Axes.text rotation 값과 ha/va/bbox, default rotation mode`라는 결합이다. 새 default 분기는 bbox keyword를 넘기지 않고, canvas draw 후 `get_window_extent`와 `Rectangle`로 외접 사각형을 그린다. 그래서 **`method_specific=NO`, `method_core_api=YES`**다. 다섯 각도/두 행을 그대로 재현하는 recipe도 계승하지 않는다. 이 조건을 보고 두 판 병기로 반환한다. `method_original_exact`는 문자 그대로 전체 코드가 동일한지를 측정하는 지표가 아니라 이 옛 구체 recipe의 계승 여부다.

`default-text-rotation-demonstration`은 redirect stub과 후계 HTML 모두에 없다. 새 `text-rotation-mode`를 써야 한다. 화면 실제 표시와 G는 미확인이다.

### G1: 경로·목적·방법이 남아도 fragment는 달라짐

양판은 공유 x축·Density/Temperature/Velocity의 세 y축 데이터, `twinx()` 두 번, `spines.right.set_position(("axes",1.2))`를 보존한다. 새 제목의 표기 변경으로 DOM id는 `multiple-yaxis-with-spines`에서 `multiple-y-axis-with-spines`로 바뀐다. 고정 전체 HTML에 옛 id는 없으므로 새 id가 있는 절로 교체한다. 색과 설정 문법이 변한 것을 목적 실패로 세지 않았다.

### G2: 같은 주소의 다른 구체 내용

[첫 공식 변경](https://github.com/matplotlib/matplotlib/commit/895626981706e301923cc23aa079b5c0a8774bf7)은 Men/Women을 Tea/Coffee로 바꾸고, [후속 변경](https://github.com/matplotlib/matplotlib/commit/e71012316e7271799a064ce09ea9285f3edb47a7)은 penguin species 자료와 반복문으로 바꾼다. 새 고정 본문의 제목·코드·실제 그림은 Adelie/Chinstrap/Gentoo의 세 속성이다. 옛 Men/Women, G1…G5, Scores 비교는 이어가지 않는다.

그럼에도 grouped bars+numeric labels라는 일반 역할과 `Axes.bar` offset/`bar_label`이라는 핵심 API는 유지된다. 원 `±width/2`의 두 bar 호출과 두 bar_label 호출이라는 recipe는 없어졌다. 따라서 원 목적에서는 FP, 일반 역할에서는 TP이며, 원 recipe에서는 NO, 일반 API에서는 YES다. 추가 일반 역할은 경로/선택 노출 후·새 본문 전 봉인된 해석이라는 방법상 한계가 있다.

**이것은 미사용 잔류 자원 반례가 아니다.** 새 절은 같은 `_images/sphx_glr_barchart_001.png`를 계속 참조하며 그 경로의 내용이 바뀌었다. 원 목적의 의미 교체 FP를 ‘옛 경로 남음·새 절에서 미사용’으로 바꾸어 보고하면 잘못이다.

NO를 준 범위는 새 고정 gallery의 522개 Python 예제에 대한 basename·caption/토큰·원 값·Men/Women/G1/score·bar_label 특징 검색, 그 결과 및 의미상 후보 10개 본문/코드, 두 공식 교체 diff다. 다른 버전·외부 글·모든 의미상 별칭의 완전 부재를 증명하지 않는다. `misc/demo_agg_filter.py`의 `drop_shadow_patches`는 비슷한 값과 두 막대를 재사용하지만 양 축을 숨기고 그림자 filter를 시연하며 Men/Women·G1…G5·숫자라벨이 없다. 비슷한 코드와 그림이 다른 목적이라는 반대 관측이다.

## 모집·분모와 탐색 범위

옛 gallery HTML은608개다. 색인/실행요약51개, redirect별칭36개를 제외한 실예제는521개이며, AF102 적격40개와 과거 교정예제2개를 제외하면479개다. 자동 HTML 판독515개와 고유 직접 열람 자료 수는 합치지 않는다. 완전 경로 집합에서 A3/M0/G476을 얻었고 봉인 주표는 A2+G2, M결원2다.

| 축·층 | TP | FP | FN | TN | 실제 양성 | 실제 음성 | 실측 미확인 | 결원 | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 원 구체 목적/A | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 산출 불가 |
| 원 구체 목적/M | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 산출 불가 |
| 원 구체 목적/G | 1 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 1.0 |
| 일반 시각 역할/A | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 산출 불가 |
| 일반 시각 역할/M | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 산출 불가 |
| 일반 시각 역할/G | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 산출 불가 |

G층 원 목적 FPR1/1은 한 음성 사례의 조건부 값이다. 일반 역할과 모든 A층은 실제 음성이0이라 FPR 산출 불가다. 층/주표/보조/대조를 합친 전체 성능률을 만들지 않는다.

보조 경로는 source revision의 ancestry 차이1374 commits에서 path-change metadata14건, 옛 적격 예제를 건드린 D/R6건을 시각·SHA순으로 모두 읽은 것이다. 기본 `git show`가 merge3건의 patch를 비워 반환한 영수증을 보존하고 first-parent diff로 보완했다.6건은3사건이고,2사건은 A1/A2와 겹친다. 새 독립 사례는 `pyplot_mathtext`→`pyplot_text`1쌍이다. 수학식을 텍스트에 넣는 목적은 통합 후계에 남지만 옛 alpha/beta/무한합 literal은 달라진다. 이 별도 표본은 NO→YES FN1이고 주 혼동표에 합치지 않는다. `supplemental-final.json`에2판이 있다.

직접 상세 판독한 경로잔류 일반 사례는 주G2개+사전등록 대조4개=6개다. 이6개에서는 옛 대표 경로의 새 절 미사용을 확인하지 못했다. 나머지G470개 본문을 전수 판독한 것이 아니며, M0은 경로 신호의 전수 결원일 뿐 모든 의미적 잔류 파일이 없다는 증명이 아니다.

## 원본·자료 수와 검증 범위

`resume-original-review.json`은 main8판+control8판+aux2판, 총18판의 보존 원 HTML을 다시 열어 고정 body SHA256, 정확 DOM id, 코드, src/srcset, payload SHA256/Git blob, 공개 소스 지문을 대사한 영수증이다. 실제 원문은 고정 외부 URL과 보존 section snapshot에 연결된다. base/picture/source/inlineSVG의 존재도 관측 JSON에 남는다. 새 history query나 예제 실행을 가장하지 않는다.

재개 중 이전 세션으로 보이는 동시 쓰기가 발견되어 원 작업 사본의 쓰기를 중지했고, 안정된 복사본에서 계속했다. 이 판독의 source admission 기준은 mutable component ledger가 아니라 **봉인8054의 Matplotlib sources.jsonl**이다. `sources-stage3.jsonl`의 work_key를 전체 작업 원장과 다시 중복 제거해야 한다. 이 파일만 더하면 봉인 이후 신규 본문3저작, 별계보 실제 source3저작, 공식 nonmerge 변경5사건이다. 기존 봉인 본문8저작은 새판을 읽어도 다시 세지 않는다. root 단계는 더 보수적인 official3 또는 다른 프로젝트 자료를 택할 수 있다.

별계보 source3개는 `tick_labels_from_values`, `demo_gridspec06`, `looking_glass`이며 모두 AF102 sources에 없고 여기서 counted body와 다른 예제다. old/new 코드는 같은 SHA256이므로 한 저작씩 센다. 첫 코드는 tick값→알파벳 함수와 MaxNLocator, 둘째는 중첩 GridSpec과 외곽 spine 조건, 셋째는 mouse event→clip_path 갱신을 제공한다. 특히 looking_glass는 정적 그림만으로 상호작용을 검증할 수 없는 반례다. 실행은 미실시다.

현재 version 사이트의8본문과8PNG 수신 기록은 기존 `live-url-verification.json`에 있다. A1-old/G2-new는 fixed payload와 byte SHA가 다르다. `live-byte-vs-pixel-review.json`에서 크기·모드·decoded pixel bytes가 같고 live에는 fixed의 Software/dpi metadata가 없음을 확인했다. live 표현이 불변 byte 인용이라는 의미는 아니며 G를 증명하지 않는다.

## 재현·통합 안내

1. 원격8054의 predictions/frame은 유지한다.
2. `python -B docs/workstreams/research/AF-RES-106/evidence/matplotlib/finalize_resume.py`는 원본 캐시·보존 파일과 고정 관측을 읽어 `lineage-final.json`12행, `returns-final.json`6행, 혼동표, 자료원장과 재개 대사 영수증을 만든다. 네트워크 조회나 연구 대상 예제 실행은 하지 않는다.
3. 재생에는 ignored `.cache`의 원 HTML도 필요하다. 영구 복원 시 각 observation의 hops.receipt→원URL을 받아 동일 SHA256을 대조하거나 보존 section snapshot으로 DOM/code 참조를 점검한다. 원 HTML 전체 재수신을 못 하면 그 부분은 미실시로 남긴다.
4. root가 새 결과 SHA를 고정한 후 실제 반환 id와 대표 원근거를 다시 열고 저장소 계약/공통 검사를 시행한다. 이 하위 판독은 root 검사나 최종 원격 재열람을 시행했다고 주장하지 않는다.

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
|---|---|---|
| 미사용 잔류 파일 방향은 G6개 상세검사·D/R3사건에서 미관측 | 고정3.7.0 G잔여470개 실제 절/후계의 src/srcset/code 참조를 새 사전등록으로 검사 | 옛 경로가 남지만 대응 목적 절에서 미사용인 적격 사례가 나오면 방향 결원 해소 |
| G2의 구체 목적·원 recipe와 일반 역할·핵심API가 서로 다름 | 고정 gallery source522와 후보10, 공식 두 변경을 독립 재판독 | Men/Women G1…G5 점수의 정확 후계가 나오면 원 U NO/FP를 YES로 수정 |
| 정적 id/PNG와 실제 이동·당시 생성은 별개 | 정확 반환 fragment의 브라우저 이동 및 당시 build run의 manifest/출력지문 연결 | 실제 이동이 다르면 arrival 수정; 실행별 출력과 발행 연결이 있으면 G 미확인 해소 |
