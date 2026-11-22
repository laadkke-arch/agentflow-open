# AF-RES-045 반환 카드

이 카드는 봉인 `0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1`의 예측을 바꾸지 않고 후속 근거의 적용 범위를 붙인다. 완전한 **원리→조작→두 판별 입력→동일 입력의 후속 시험** 연결은 0/6이다. 아래의 조건부 링크는 원리의 역사적 채택, 최초안 변경 인과, 검색 회수율을 뜻하지 않는다. 완결 비교를 요구하지 않는 원래 문구의 관대한 집계는 M01분모1·유일지지0·판정불가1, 입력동일성까지 완화한 조작 수락 감도는 M01/M03분모2·유일지지0·판정불가2다. 이 차이는 사후 기준 명시로 기록하며 효과 없음이나 실패율로 쓰지 않는다. 행별 판정은 [outcomes.csv](outcomes.csv), 모든 판·열람·한계는 [sources.jsonl](sources.jsonl)에 있다.

## M01 — 첫 Cartopy 저장 전에 기하를 준비할 것인가

**원래 요구:** [Matplotlib13430, 최초 게시 본문 Expected outcome](https://github.com/matplotlib/matplotlib/issues/13430). Matplotlib3.0.2·Cartopy0.17.0에서 첫 저장이 두 번째 저장의 올바른 배치와 같아야 한다. 정확한 생성시점 본문은 복원하지 못했다.

**돌려줄 원리 링크:** [USGS의 합성·편집·승인 후 인쇄 절](https://www.usgs.gov/educational-resources/topographic-mapping) L186–199와 [InDesignCS6 preflight](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf) PDF657–658는 최종 출력 전 검증이라는 작업 순서를 준다. 한 번의 renderer draw로 해결된다는 알고리즘은 이 원전에서 나오지 않는다. 가까운 경쟁 원리는 [CSS Paged Media2013 §8.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/#renderingpages)의 완성된 페이지 비례 축소다.

**조작과 판별 입력:** A는 첫 저장 전에 pre-draw; B는 첫 완성 raster 전체를 비례 축소해 같은 canvas에 맞춘다. 정상은 연구자가 추가한 Cartesian 대조, 경계는 원래 빈 PlateCarree axes의 두 번 저장이다. 전체 축소는 내부 상대 bbox·aspect를 바꾸지 않는다. B의 봉인 행도 이 한계를 이미 예상했으므로 A/B가 다른 조작이라는 이유로 서로 반대의 성공 예측이라고 쓰면 안 된다.

**후속:** [유지보수자의 draw 제안](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463400056)과 [원작성자의 간단한 예제 성공 보고](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463401327)는 A의 제한적 작업 조언을 뒷받침한다. B와 Cartesian 정상 대조의 출력은 없다. [Cartopy1355 고정 시험 L239–280](https://github.com/SciTools/cartopy/blob/4703efc6e85a3e0e616889e29382659a741299b9/lib/cartopy/tests/mpl/test_gridliner.py#L239-L280)은 관련 기하 준비를 시험하지만 첫/둘째 저장 비교와 다르다.

**추천 수준:** 조건부 작업 순서 진단. 새 파일을 한 번 더 쓰는 대신 pre-draw를 시도하는 구체 조작은 원래 요청의 단순 목표보다 상세하다. 당시 API에는 있었으며 제공 원전 채택 기록은 없다. 원작성자는 유지보수자의 조언을 받아들였다.

**적용 불가·뒤집힘:** [전역 범위 초기화 제안 철회](https://github.com/SciTools/cartopy/pull/1370#issuecomment-569853924)는 자동 범위 조절을 잃는다. [큰 변환 객체의 성능 비교](https://github.com/SciTools/cartopy/pull/1956)는 모든 기하를 매번 준비하는 비용을 드러낸다. 두 자료 모두 다른 조작/입력이며 A의 직접 반증으로 채점하지 않는다. 다음 최소 증거는 고정3.0.2/0.17.0에서 A/B 및 정상/경계의 상대 bbox 로그다.

## M02 — 긴 범례가 데이터 axes를 줄이도록 둘 것인가

**원래 요구:** [Matplotlib13522 최초 본문](https://github.com/matplotlib/matplotlib/issues/13522). 10×3 inch, 세 axes 폭 비율5:1:5, 고정 글꼴에서 긴 범례 때문에 다른 axes가 줄지 않기를 원한다.

**돌려줄 원리 링크:** [Maplex10.3 배치·충돌 규칙](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm) L125–145와 [CSS2013 §8.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/#renderingpages). 지도 라벨 생략과 legend bbox를 배치 계산에서 제외하는 API는 같은 조작이 아니다. CSS에서도 font·figure 외에 한 페이지·동일 방향을 연구자가 추가로 고정해야 clip fallback 해석이 가능하다.

**조작과 판별 입력:** A는 legend bbox를 포함, B는 legend를 계속 그리되 layout 계산에서 제외한다. 정상10개·경계30개, 원요구의20개는 보조 입력이다. 비교 기준 bbox는 같은 figure에서 legend artist만 없는 상태다. 두 후보는 모두 조건부 B를 예상하므로 판별 성공에서 제외한다.

**후속:** [set_in_layout(False) 제안](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-467476150)과 [원작성자 수락](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-470121184)이 있다. [2020년 문서 정정](https://github.com/matplotlib/matplotlib/pull/18100)은 API 의미를 확인하지만10/30개 fixture의 실행을 대신하지 않는다.

**추천 수준:** 기존 API를 찾는 조건부 링크. 원래 작성자는 이미 overflow를 자르고 싶다고 했으므로 목표 발견은 새롭지 않다. 정확한 API 이름은 후속 조언에 있으며 원전이 그 API를 유도했다는 기록은 없다. 두 원리 모두 같은 수락 조작과 정성적으로 맞물리지만 봉인 출력 두 개의 적중은 미확인이다.

**적용 불가·뒤집힘:** 시각 설계자는 axes 크기 보존을 원해도 데이터 독자는 잘린 범례에서 계열 의미를 잃을 수 있다. 그림 크기·글꼴·페이지 방향 제약을 풀면 확대, 축소, 회전, 분할도 가능해진다. [QGIS2.18 Point displacement](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html) L324–326은 겹친 점을 읽기 쉽게 옮기는 별도 예다. 표시 위치와 원좌표를 구별해야 하며, 가독성이 곧 정확한 위치 보존을 뜻하지 않는다.

## M03 — 색상막대 중앙인가, 값0.5인가

**원래 요구:** [Matplotlib13600 최초 게시 본문](https://github.com/matplotlib/matplotlib/issues/13600). 데이터 factor를 바꿔도 text가 colorbar 중앙에 있어야 한다. 작성자는 처음 제목만 올린 뒤 본문을 완성했다고 [댓글](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635)에서 밝혔다.

**돌려줄 원리 링크:** [InDesignCS6 anchored objects](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf) PDF300–301의 page/container 기준 위치와 [Maplex의 위치/대상 연결](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm) L98–111. 같은 .5라도 전체의 절반인지 데이터 값인지 단위가 다르다.

**조작과 판별 입력:** A는 `cb.ax.transAxes`, B는 기본 data 좌표. factor .01 정상과 .001 경계에서 A의 y비율은 .5, B는 실제 axes가 [0,99×factor]일 때 각각 .50505와5.0505다. 이 수치는 조건부 좌표식이며 실행 측정값이 아니다.

**후속:** [명시적 transAxes 조언](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470153183)을 [원작성자가 수락](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470159527)했다. 그러나 [PR13603](https://github.com/matplotlib/matplotlib/pull/13603)의 [test_collapsed L313–327](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327)은 별도 None crash다. 이 시험이 통과했다는 보고를 위치 예측의 시험으로 돌려쓰지 않는다.

**추천 수준:** 좌표 단위를 확인하는 조건부 진단 링크. 중앙이라는 불변조건은 이미 최초 요구에 있고 transAxes도 당시 API였다. 새 원리가 선택을 발견했다거나 저자가 InDesign을 읽어 채택했다고 말할 수 없다.

**적용 불가·뒤집힘:** 목표를 실제 y값 .5에 주석 달기로 바꾸면 B의 y-data 고정 논리가 적합할 수 있다. 기본 (.5,.5)는 x도 data 좌표여서 가로 중앙을 유지하려면 혼합 transform 등 별도 처리가 필요하다. B 전체를 무조건 권하지 않는다. [2.2.2 colorbar mesh L843–861](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py#L843-L861)는 정규화 좌표여서 B도 중앙일 수 있다. [3.0.2 L510–518,984–1014](https://github.com/matplotlib/matplotlib/blob/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py)는 조건에 따라 실제 단위로 환산한다. 버전이나 norm이 바뀌면 추천의 근거도 다시 검사해야 한다.

## AUD01 — 선택 구간 조회의 단위와 API 전달은 별도 문제

**원래 요구:** [Audacity407 최초 본문](https://github.com/audacity/audacity/issues/407). pipe script에서 선택 시작·끝을 읽고 싶다. 봉인 A는 새 GetTime, B는 기존 Nyquist START/END 속성을 NyquistPrompt 경로로 읽는 제안이다.

**돌려줄 원리 링크:** [Avid Release9 p82](https://resources.avid.com/SupportFiles/attach/MCGS.PDF)의 포함되는 Out-frame, [PremiereCS6 PDF43·289–290](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf)의 frame 및 audio sample 단위, [W3C Media Fragments2012 §4.2.1·6.2.2](https://www.w3.org/TR/2012/REC-media-frags-20120925/)의 반열린 구간과 invalid 경계를 함께 반환한다. W3C의 a=b는 유효한 빈 재생 구간이 아니라 무시하는 잘못된 구간이다. 선택 getter의 point selection과 혼동하지 않는다.

**조작과 판별 입력:** [1.25,2.50]초와[1.25,1.25]초를 조회하면 두 후보는 같은 경계를 예상한다. 포함 프레임의 duration 규칙은 getter를 새로 만들지 기존 속성을 전달할지를 결정하지 않는다.

**후속:** [PR6165](https://github.com/audacity/audacity/pull/6165)는 `GetInfo: Type=Selection`이라는 제3안 C를 구현했다. [고정 코드 L634–645](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645)는 selectedRegion의 양 끝을 반환한다. [기여자 시험보고](https://github.com/audacity/audacity/issues/407#issuecomment-2076865041)의 그림은2.62385/5.29415로 봉인 입력과 다르다. [PR6347](https://github.com/audacity/audacity/pull/6347)의 wrapper는 과거 B의 성공 증명이 아니다.

**추천 수준:** 구간 의미와 전달 경로를 분리하는 조건부 참고, 실제 구현을 찾는 직접 링크. 둘 중 원리가 API 선택을 판별했다는 주장은 불가하다. 원작성자의 동일 조건 재시험과 donor 채택은 미확인이다.

**적용 불가·뒤집힘:** [검토 댓글](https://github.com/audacity/audacity/pull/6165#issuecomment-2077257269)은 완전한 선택 복원에는 트랙 목록도 필요하다고 지적한다. 시간 동기화와 선택 전체 복원은 다른 목적이다. 동일 값의 두 frame mark는 한 frame 길이를 가질 수 있지만 연속 시간의 점은 길이0이며, 유효성 규칙까지 같지는 않다.

## AUD02 — 읽기 쉬운 색과 사용자가 정한 색은 같은 조건이 아니다

**원래 요구:** [Audacity511 최초 게시의 Original report 구역](https://github.com/audacity/audacity/issues/511). 현재 본문에는 사후 체크리스트가 있고 최초 제목에는 selection이 없었다. 결과 사전 노출 감도에서는 이 사례를 제외한다.

**돌려줄 원리 링크:** [Final Cut Pro의 선택 범위 표시](https://support.apple.com/guide/final-cut-pro/select-ranges-ver28cca92/mac)와 [WCAG2.1 §1.4.11](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#non-text-contrast). 외곽 표시 규칙은 waveform 전경/배경 RGB 보존과 대비 보정 중 하나를 정하지 않는다. native Audacity waveform에 WCAG의3:1을 적용한 것은 연구자 설계 기준이며, 사용자 선호만으로 essential 예외가 자동 성립하지 않는다.

**조작과 판별 입력:** A는 입력 RGB를 그대로 보존, B는 가독성 목표에 따라 대비를 보정한다. black/white 정상은21:1; 동일 #777777 경계는1:1이다. 봉인 P1에 남은 colloquial contrast0은 휘도 차이0을 뜻하며 대비비0이라는 주장으로 읽지 않는다. 당대 Color0..3 API는 임의 두 RGB를 표현하지 못한다.

**후속:** [Audacity4에서 고쳤다는 댓글](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377)에는 입력·코드·색 정책이 없다. 체크된 [2713의 종료 댓글](https://github.com/audacity/audacity/issues/2713#issuecomment-1150354103)은 오히려 post4.x로 미뤘다고 한다.

**추천 수준:** 요구 충돌을 물어볼 조건부 참고. 구체 A/B 구현 추천은 미확인. 원리가 새로운 선택을 도입하거나 채택되었다는 기록도 없다.

**적용 불가·뒤집힘:** [독립 PR5653의 QA와 회귀보고](https://github.com/audacity/audacity/pull/5653)는 색을 복사·분할·저장판 호환에서 보존할 상태로 취급한다. 자동 대비 보정은 식별 색을 잃게 할 수 있다. 같은 입력에 대해 외곽선·사용자 override라는 제3안도 가능하지만 실제 RGB 시험 없이 성공으로 추가하지 않는다.

## AUD03 — 영상의 경계를 주파수 마스크로 옮길 수 있는가

**원래 요구:** [Audacity644 최초 본문](https://github.com/audacity/audacity/issues/644). 선택 주파수 대역에 일반 효과, 특히 Noise Reduction을 적용하고 싶다는 요구다. Adobe Audition은 작성자가 이미 든 같은 분야의 사례다.

**돌려줄 원리 링크:** [PremiereCS6 audio sample 편집 PDF289–290](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf), [Smith의 rectangular window 설명](https://ccrma.stanford.edu/~jos/sasp/Rectangular_Window.html), [Final Cut Pro Color Mask Softness step5](https://support.apple.com/en-lamr/guide/final-cut-pro/vera699eacc8/mac). [Netflix timing §§1·2·5](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)는 읽기 시간 때문에 경계를 옮기는 현대 참고다. 영상 색 공간·시간·주파수는 서로 다른 변수이며 kernel이 이 원전에서 도출되지는 않는다.

**조작과 판별 입력:** 연구자 toy는 Fs48000/N2048, bins42..85의 hard gain−6dB인 A와 centered5bin log-gain 평균 B다. 정상bin64는 둘 다−6dB, 경계bin86은 A0/B−2.4dB다. bin42는984.375Hz, bin86은2015.625Hz로 연속[1000,2000]과 bin 집합도 정확히 같지 않다.

**후속과 연구자 오류:** [요구 이전2.4.2 L75–77](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77)의 local `#undef`를 봉인 전에 놓쳤다. UI에 영향이 표시되지 않는 이유로 해당 효과에서는 spectral selection을 비활성화한다. [2024 정리 변경](https://github.com/audacity/audacity/commit/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7)은 이름을 바꾸며 비활성화를 유지한다. 봉인 A/B와 toy 계산은 그대로 보존하되 실제 API 적용 가능성 해석을 정정한다.

**추천 수준:** 변수 대응이 깨지는 예와 향후 시험 가설만 반환. 실제 Noise Reduction 기능 추천으로 사용할 수 없다. 원래 요청에 없는5bin kernel은 연구자가 만들었고 공개 채택·동일 입력 시험은 없다.

**적용 불가·뒤집힘:** 평균을 선형 gain으로 바꾸면 경계 약−1.93305dB, feather를 선택 안쪽에만 두면0dB가 되어 판별이 사라진다. 실제 window·overlap·noise profile·FFT output은 별도다. 같은 숫자를 실제 음질·시간 영역 부작용으로 해석하면 안 된다.

## 공통 재개 순서

1. [예측 봉인](evidence/prediction-seal.json)의 네 고정 입력 파일 해시를 확인한다.
2. 조건부 링크의 목적·판·단위를 먼저 확인하고, [재현 입력](evidence/reproduction/REPRODUCE.md)과 [Audacity 재개 명령](evidence/reproduction/AUDACITY-REPRODUCE.md)을 사용한다. 역사 환경 실행은 이번 조사에서 하지 않았다.
3. 원래 A/B를 바꾸어야 하면 새 실험으로 구분한다. 특히 GetInfo 제3안, 전역extent 고정, spectral flag 제거는 과거 봉인 선택을 충족한 것으로 쓰지 않는다.
