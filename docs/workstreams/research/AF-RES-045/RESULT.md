# AF-RES-045 결과

## 표 1 — 봉인한 6요구 × 2후보

| 요구 ID·최초판 | 두 선택과 판별 입력 | 제공 분야·원리 | 근거 자료 주소·절 | 봉인한 정상·경계 예측 | 후속 근거 주소·판 | 지지·충돌·판별불가·미확인 | 깨지는 조건 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M01/P1 · [13430](https://github.com/matplotlib/matplotlib/issues/13430), 2019-02-13 요구의 현재 첫 본문; 불변 최초판 미확인 | A 첫 export 전 pre-draw; B 첫 raster 전체 비례 축소. 정상 Cartesian, 경계 빈 PlateCarree의 첫/둘째 저장 | 지도 인쇄·출판: 최종 합성·교정 뒤 출력 | [USGS](https://www.usgs.gov/educational-resources/topographic-mapping) L186–199; [InDesignCS6](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf) PDF657–658 preflight | 정상 상대 bbox 변화 없음; 경계는 pre-draw가 실제 extent/aspect를 정리할 때 첫 저장이 종전 둘째 배치와 일치. 필요한 pass 수는 원전에서 미결정 | [제안](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463400056)·[작성자 보고](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463401327), 2019-02-13; [관련 시험](https://github.com/SciTools/cartopy/blob/4703efc6e85a3e0e616889e29382659a741299b9/lib/cartopy/tests/mpl/test_gridliner.py#L239-L280), 2020-07-01 | **미확인**: A의 원래 간단한 예제에 정성 R보고는 있으나 정상·경계의 완전한 비교 없음 | 다른 renderer, 복잡한 artist, 필요한 갱신 누락. 원전은 정확한 call 순서·횟수를 보장하지 않음 |
| M01/P2 · [13430](https://github.com/matplotlib/matplotlib/issues/13430), 같은 본문판 | 같은 A/B; 정상 Cartesian, 경계 PlateCarree 첫/둘째 상대 기하 | 인쇄: 완성 페이지를 출력 장치에 맞춰 비례 축소 | [CSS Paged Media2013](https://www.w3.org/TR/2013/WD-css3-page-20130314/) §8.2 L819–828 | 정상 상대 배치 보존; 경계 차이가 내부 bbox/aspect면 전체 scaling으로 못 고침. canvas-fit만 문제라면 가능 | [13430 작성자 보고](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463401327)는 A만 다룸; [Cartopy1370 철회](https://github.com/SciTools/cartopy/pull/1370#issuecomment-569853924), 2019-12-31은 다른 조작 | **미확인**: B 실행 없음. A 성공으로 P2를 기각할 수 없음 | 다른 조작 선택과 반대 성공 예측을 혼동. P2 자신도 내부 기하의 실패를 이미 예상 |
| M02/P1 · [13522](https://github.com/matplotlib/matplotlib/issues/13522), 2019-02-26 요구의 현재 첫 본문; 최초판 미확인 | A legend bbox 포함; B 계산에서만 제외하고 계속 그림. 정상10개·경계30개, 10×3inch·5:1:5·글꼴 고정 | 지도 라벨: 충돌·가독성 제약에서 일부 표시를 양보 | [Maplex10.3](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm) L125–145; [QGIS2.18](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html) L545–558 | 정상 두 조작 가능; 경계 B로 데이터 axes 크기 보존·넘친 범례 clip을 목표. 지도 규칙만으로 exact bbox API는 미결정 | [set_in_layout 제안](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-467476150)·[작성자 수락](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-470121184), 2019; [문서 정정18100](https://github.com/matplotlib/matplotlib/pull/18100), 2020 | **판별불가**: P2와 같은 조건부 B. 10/30개 bbox의 동일 입력 시험은 미확인 | 지도 라벨 삭제와 legend의 layout 제외는 다름. clip된 key가 독자의 계열 해석을 해칠 수 있음 |
| M02/P2 · [13522](https://github.com/matplotlib/matplotlib/issues/13522), 같은 본문판 | 같은 A/B·입력; bbox 기준은 동일 figure에서 legend artist만 없는 대조 | 인쇄: 출력 제약에서 회전·축소·분할·자르기 대안 | [CSS2013](https://www.w3.org/TR/2013/WD-css3-page-20130314/) §8.2 L819–828 | 정상 이미 맞으면 추가 축소 없음; 경계는 font/figure와 연구자 추가 single-page·same-orientation까지 고정할 때 clip 후보 | [작성자 수락](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-470121184); [고정 문서](https://github.com/matplotlib/matplotlib/blob/8a3ec2f43e7fa287321e9f9e4c6fef24394cd2f9/tutorials/intermediate/tight_layout_guide.py#L155-L165) | **판별불가**: 같은 조작 수락은 두 후보의 판별 성공이 아님 | 제약을 풀면 다른 출력 정책 가능. CSS가 legend-only exclusion 또는 불변 bbox를 명세하지 않음 |
| M03/P1 · [13600](https://github.com/matplotlib/matplotlib/issues/13600), 2019-03-06 현재 첫 본문; 처음 제목만 제출 후 완성 | A transAxes; B 기본 data 좌표. 정상 factor .01, 경계 .001; 추가 감도 .1. text(.5,.5) | 출판: 페이지·container 기준 위치를 내용 값과 분리 | [InDesignCS6](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf) PDF300–301 anchored objects; [CSS2013](https://www.w3.org/TR/2013/WD-css3-page-20130314/) §6 Table1 | A는 정상·경계와 .1 모두 y=.5 axes fraction. 별도 None crash 해결을 예측하지 않음 | [transAxes 조언](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470153183)·[수락](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470159527); [PR13603 시험](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327) | **미확인**: 조작은 정성 R보고와 일치; 두 factor의 실제 위치는 기록되지 않음. PR시험은 다른 문제 | 중심이라는 불변조건은 원래 요구. API 조작은 당시 알려져 있었고 donor의 추가 효용은 미측정 |
| M03/P2 · [13600](https://github.com/matplotlib/matplotlib/issues/13600), 같은 본문판 | 같은 A/B·입력. B는 data값 .5를 보존 | 지도: 위치·값에 결부된 대상 참조 보존 | [Maplex10.3](https://desktop.arcgis.com/en/arcmap/10.3/map/working-with-text/a-quick-tour-of-maplex.htm) L98–111,125–145 | 실제 linear limits가 [0,99factor]일 때 정상 .50505, 경계5.0505, .1에서는 .050505. 중앙 목적 위반을 미리 예상 | [3.0.2 colorbar](https://github.com/matplotlib/matplotlib/blob/8858a0d1bdd149a0897789e8503ac586be14676d/lib/matplotlib/colorbar.py) L510–518,604–615,984–1014; [수락 댓글](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470159527) | **미확인**: 조건부 산술·정적 코드와 양립하지만 동일 입력의 후속 B 실행 없음 | 실제 y값 .5의 주석이면 B의 y-data 고정 논리가 적합할 수 있으나 x 중앙 정렬은 별도 처리 필요. 2.2.2·다른 norm에서는 좌표 대응이 달라짐 |
| AUD01/P1 · [407](https://github.com/audacity/audacity/issues/407), 2020-01-03 현재 첫 본문; 최초판 미확인 | A 새 GetTime; B 기존 Nyquist START/END의 pipe 조회. 정상[1.25,2.50]s, 경계[1.25,1.25]s | 영화 편집: 포함되는 In/Out frame 및 duration | [Avid Release9](https://resources.avid.com/SupportFiles/attach/MCGS.PDF) p82,106 | A/B 모두 정상(1.25,2.50), 경계(1.25,1.25). one-frame duration을 cursor length로 옮기지 않음 | [PR6165](https://github.com/audacity/audacity/pull/6165), merge0ffa73b9…; [기여자 보고](https://github.com/audacity/audacity/issues/407#issuecomment-2076865041), 2024-04-25 | **판별불가**: 두 후보 수치 동률. 실제 GetInfo Selection은 제3안 C | 프레임 길이 규칙은 전용 getter와 속성 전달 중 하나를 고르지 못함. track 목록이 필요한 목적이면 시간만 부족 |
| AUD01/P2 · [407](https://github.com/audacity/audacity/issues/407), 같은 본문판 | 같은 A/B·입력 | 편집·웹 미디어: sample 경계와 반열린 재생 구간의 유효성 | [PremiereCS6](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf) PDF43,289–290; [W3C2012](https://www.w3.org/TR/2012/REC-media-frags-20120925/) §4.2.1,6.2.2 | 같은 getter 값. W3C a=b는 invalid-and-ignore여서 유효한 editor point getter의 예상으로 쓰지 않음 | [고정 GetInfo 코드](https://github.com/audacity/audacity/blob/0ffa73b9f44acc339e12a350edadd96590dc4b17/src/commands/GetInfoCommand.cpp#L634-L645); [wrapper6347](https://github.com/audacity/audacity/pull/6347), mergeae0ab087… | **판별불가**: 제3안의 Start2.62385/End5.29415 보고는 봉인 입력이 아님 | 조회·재생·완전 선택 복원의 목적 차이; Nyquist 속성 존재는 pipe 전달 성공이 아님 |
| AUD02/P1 · [511](https://github.com/audacity/audacity/issues/511), 2020-05-08 생성·현재 Original report 구역; 사후 체크리스트 노출 | A 정확 RGB 보존; B 대비 보정. 정상 black/white, 경계 둘 다 #777777 | 영상 편집: range 외곽 표시와 asset label 색 | [Final Cut Pro](https://support.apple.com/guide/final-cut-pro/select-ranges-ver28cca92/mac) Select a range; [PremiereCS6](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf) PDF152 Label assets | 정상은 border를 추가해도 읽힘. 경계 border는 선택영역만 구별하고 waveform 색 정책은 미결정; 원문에 A/B 강제 없음 | [Audacity4 해결 선언](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377), 2024-10-29; [2713 유보 종료](https://github.com/audacity/audacity/issues/2713#issuecomment-1150354103), 2022-06-08 | **판별불가**: 원리도 선택 미결정, 후속도 RGB 입력 없음 | 선택 표시와 waveform 가독성은 다른 대상. contrast0 문구는 휘도차이0이며 대비비는1:1 |
| AUD02/P2 · [511](https://github.com/audacity/audacity/issues/511), 같은 본문판 | 같은 A/B·입력. 정확 RGB와 가독성 중 우선순위 필요 | 접근성: 필수 비텍스트 시각정보의 대비 | [WCAG2.1 2018](https://www.w3.org/TR/2018/REC-WCAG21-20180605/#non-text-contrast) §1.4.11 L614–625 | 정상21:1 유지. 경계1:1이므로 대비 목표 우선이면 B의 색 변경/별도 표시로3:1 이상; exact-RGB 우선이면 B 부적격 | [511 선언](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377); [독립 색 보존 비교5653](https://github.com/audacity/audacity/pull/5653), merge948a1036… | **미확인**: 동일 HEX 입력의 실제 보정·보존 결과 없음 | native 앱에 기준 적용은 연구자 가정. 사용자 선호만으로 essential 예외가 자동 성립하지 않음; 당시 Color0..3 API 제약 |
| AUD03/P1 · [644](https://github.com/audacity/audacity/issues/644), 2020-08-20 현재 첫 본문; 최초판 미확인 | A bins42..85 hard−6dB; B centered5bin log-gain 평균. Fs48000/N2048, 정상bin64, 경계bin86 | 오디오 편집·DSP: sample 경계, finite window의 제약 | [PremiereCS6](https://help.adobe.com/archive/en/premiere-pro/cs6/premiere_pro_reference.pdf) PDF289–290; [Smith](https://ccrma.stanford.edu/~jos/sasp/Rectangular_Window.html) Eq3.4 | 연구자 toy: 정상 둘 다−6dB; 경계 A0/B−2.4dB. 실제 효과 출력은 미관측 | [요구 이전 소스](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77); [2024 정리 변경](https://github.com/audacity/audacity/commit/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7) | **미확인**: local undef를 봉인 전에 놓친 오류. 실제 API 적용 가능성 해석 정정 | 시간 경계가 주파수 bin mask를 정하지 않음. 선택 효과의 표시가 없어 NR에서는 의도적으로 비활성화 |
| AUD03/P2 · [644](https://github.com/audacity/audacity/issues/644), 같은 본문판 | 같은 A/B·입력; bin86=2015.625Hz | 영화 색상·방송 자막: 경계 softness와 읽기 시간 조정 | [Final Cut Pro](https://support.apple.com/en-lamr/guide/final-cut-pro/vera699eacc8/mac) Softness step5; [Netflix](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines) §§1·2·5, 현행판 | toy 정상−6/−6; 경계 B−2.4/A0. inside-only smoothing이면 B0으로 같아짐 | [644 댓글 범위](https://github.com/audacity/audacity/issues/644); [PR6201](https://github.com/audacity/audacity/pull/6201)의 비활성 예외 유지 | **미확인**: 실제 noise profile/window/bin 출력 시험 없음. 후발·날짜불명 donor는 현대 진단 | 색 공간·시간·주파수 단위 불일치. 5bin kernel은 제공 원전이 아닌 연구자 정의. 같은 분야 Audition 참조는 이미 요구에 있음 |

## 표 2 — 요구별 판별 가능성과 반환 수준

| 요구 ID | 두 예측이 갈렸는가 | 어느 출력에서 갈렸는가 | 관측된 출력·근거 위치 | 지지 후보 | 결말 사전 노출 | 추천 가능한 용도 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M01 | 봉인 different_conditional. 조작은 다르나 성공의 반대 예측은 아님 | 첫/둘째 상대 bbox·aspect. P2도 내부 기하의 scaling 실패를 예상 | [작성자463401327](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463401327)의 간단한 원예제 A성공; B 없음 | 유일 지지 없음. P1의 제한적 조작 일치 | 명시적 결과 노출 없음; 불변 첫 본문은 미확인 | 첫 export 전 준비 순서를 묻는 조건부 진단 | 정상 대조·B출력·정량 bbox·pass수·donor채택 |
| M02 | same_conditional | 두 후보 모두 조건부 B; 판별 차이 없음 | [작성자470121184](https://github.com/matplotlib/matplotlib/issues/13522#issuecomment-470121184)의 API수락. 10/30개 출력 미기록 | 두 후보와 같은 조작 수락, 엄격 두 입력 적중은 미확인 | 명시적 결과 노출 없음; 불변판 미확인 | 기존 set_in_layout API와 가독성·정보 손실 조건 링크 | 동일 fixture bbox·완전 key 가독성·원전의 추가 효용 |
| M03 | different | factor.001의 axes fraction .5 대 조건부5.0505 | [작성자470159527](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470159527)의 A해결보고; [13603시험 L313–327](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327)은 별도 crash | 유일 지지 없음. P1조작 정성 일치 | 결과 노출 없음; 최초 제목만 제출한 이력은 후속에서 발견 | 좌표 단위/불변조건 점검 | 두 factor 실행·B후속시험·원전 채택 |
| AUD01 | same | 두 getter의 시작·끝 수치 동일 예상 | [기여자2076865041](https://github.com/audacity/audacity/issues/407#issuecomment-2076865041)의 C값2.62385/5.29415; [6165](https://github.com/audacity/audacity/pull/6165)는 제3안 | 없음. 동률이고 실제 구현도 A/B와 다름 | AUD03용2.4.2코드의 교차 노출E02;2.3.3에서 뒤에 선행 존재 확인 | 구간 의미·pipe전달 분리, 실제 getter 구현 링크 | 봉인점/구간 입력, 과거B전달, 원작성자 재시험 |
| AUD02 | underdetermined | border 규칙은 RGB정책을 못 정함. 대비규칙은 목적 우선순위에 조건부 | [511해결선언](https://github.com/audacity/audacity/issues/511#issuecomment-2445034377); [2713](https://github.com/audacity/audacity/issues/2713#issuecomment-1150354103)은 유보 | 없음 | **E01** 사후 checkedsubtask 노출. 최초제목에는selection없음 | 색 보존·대비·선택 표시를 분리할 질문과 반례 링크 | 실제 RGB API·동일색 출력·해결SHA·최초본문 |
| AUD03 | different_model | bin86의 toy0 대−2.4dB | [2.4.2 L75–77](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77)의 비활성화; [후속 e7d17d1b…](https://github.com/audacity/audacity/commit/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7)도 유지 | 없음. API해석 오류 정정; toy는 실제 관측이 아님 | 결말 직접 노출 없음; 사전 API독해 누락 발견 | 단위 대응 실패와 실행 가능한 가설의 조건 제시 | 활성API·실제kernel/noiseprofile·동일입력시험·원전채택 |

## 판정과 분야별 해석

**부분 인계다.** 표본·예측 봉인과 원문 수 조건은 충족했지만, 사전 두 선택을 구별한 입력에 대한 같은 조건의 공개 후속 시험은 확보하지 못했다. 서로 다른 원리가 실제 수신 설계에서 유일한 선택을 가려 준다는 성공 사례는 이 조사에서 확인되지 않았다. 이것은 그런 효과가 없다는 증명이 아니다. [봉인 규칙](SCOPE.md#q5q7-판정), [후속12행](outcomes.csv), [사후 정정](amendments.md#봉인-후-정정--첫-후속-열람-뒤)을 함께 보아야 한다.

표1의 **미확인7·판별불가5·완결 비교 지지0·동일 입력 충돌0**은 예측 행의 수다. 이 표는 봉인 뒤 명시한 두 입력·경쟁 조작의 완결 비교 기준으로 정리했다. 원래 SCOPE 문구를 더 관대하게 읽는 집계1건과 조작 수락만의 확대 집계2건도 아래에 보존한다. 충돌0은 모든 예측이 옳았다는 뜻이 아니다. 출력 관측 부족, A/B 밖의 구현, 같은 예측, 원리에서 결정되지 않는 조작을 서로 구별했다. 시각 사례 세 건에는 원작성자의 정성적 해결/수락 보고가 있다. 그러나 두 봉인 입력과 비교 조작을 모두 기록한 재시험으로 승격하지 않았다.

### Q1 — 표본과 결말 가림

두 공개 원장에서2019–2024 생성 이슈를 **현재 제목**으로 검색하고 생성일·번호 순 첫30개씩 기록했다. Matplotlib의 첫 문서 상태 문의13311은 조작·출력 요구가 없어 제외했으며13430·13522·13600을 골랐다. Audacity는407·511·644가 처음 세 유효 요구였다. frame60행에는 선정6·탈락1·정원 후 미판정53을 남겼다. 정원 뒤 Matplotlib13650의 본문을 우연히 본 사건도E03으로 보존했다. 목록은 [frame.csv](frame.csv), 필드별 첫 요구는 [requests.csv](requests.csv), 검색·첫 노출·탈락 근거는 [sources.jsonl](sources.jsonl)의MPL-SEARCH/AUD-SEARCH 및 원장에 있다.

생성순 표본은 당시 제목으로 검색한 역사적 목록이 아니다. [Audacity511 timeline](https://api.github.com/repos/audacity/audacity/issues/511/timeline?per_page=100)의2022년 제목 변경은 이 차이를 실제로 드러낸다. [Matplotlib13600의 본문 완성 댓글](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635)도 현재 첫 게시물을 생성순간의 불변 요구로 다루면 안 됨을 보여준다. 정확한 생성시점 본문이 검증된 사례는0/6이다.

원격 봉인은 [0d998cb…](https://github.com/laadkke-arch/agentflow-open/commit/0d998cb3503e8a7f0faf2bf2f8e62dd046a662b1)이며2026-11-22 22:19:23 UTC, 한국시간11월23일07:19:23이다. 첫 후속 열람은Audacity22:20:00.421Z, 공간 조사22:20:03Z, root22:20:09.248Z다. 가장 이른 후속 열람도 봉인보다37.421초 뒤다. 다만E01의 편집된 최초본문 노출과E02의 교차사례 API 노출, 사전학습의 잠재 노출은 이 시간 순서로 지워지지 않는다. [봉인 해시](evidence/prediction-seal.json), [열람 영수증](evidence/reveal-receipt.json), [작업별 최초 열람](evidence/audacity-outcomes.json)을 보존했다.

### Q2·Q3 — 다른 분야의 원리가 제공한 것과 연구자가 덧붙인 것

공간 사례에서 인쇄 원전은 출력 전 교정·페이지 기준 고정·매체에 맞춘 축소를 제공했다. 지도 원전은 가독성과 대상 연결을 함께 제약했다. 이들은 **어떤 양을 보존해야 하는가**를 명확히 하는 데 쓰일 수 있다. 한 번의 canvas.draw, 특정 artist의 bbox 제외, transAxes라는 API 이름까지 원전이 정해 주지는 않는다. [USGS 인쇄 절](https://www.usgs.gov/educational-resources/topographic-mapping) L186–199, [CSS §8.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/), [InDesign anchored objects](https://help.adobe.com/archive/en/indesign/cs6/indesign_reference.pdf) PDF300–301에서 수신 구현까지의 연결은 연구자가 만든 대응이다.

시간 사례에서는 프레임·표본·구간 유효성·색 공간이 서로 다른 불변조건을 가진다. [Avid p82](https://resources.avid.com/SupportFiles/attach/MCGS.PDF)의 포함 프레임과 [W3C §6.2.2](https://www.w3.org/TR/2012/REC-media-frags-20120925/)의 잘못된 temporal fragment 처리는 같은 point selection으로 환원되지 않는다. [Final Cut Pro Softness](https://support.apple.com/en-lamr/guide/final-cut-pro/vera699eacc8/mac)는 가까운 색을 선택에 포함하는 작업이며,5bin의 주파수 gain kernel을 명세하지 않는다.

| 제공 계열 | 주 사용자·조작 대상·목적 | 수신 프로젝트와의 관계 | 공개 시점의 한계 |
| --- | --- | --- | --- |
| USGS 지도 제작·InDesign 조판 | 지도 제작자/출판 편집자, 교정쇄·페이지·앵커, 정확하고 출력 가능한 지면 | Matplotlib의 renderer·axes 기하와 대응. 지도 소프트웨어와 시각화는 인접 분야 성격도 있음 | USGS 현행 페이지의 최초 공개일 미확인. CS6 PDF 생성2012/수정2017 metadata는 관측했지만 정확한 공개 게시일은 미확인 |
| CSS2013·Maplex10.3 | 페이지 엔진/지도 편집자, 종이 크기·라벨 위치, 매체 적합성과 가독성 | 출력 및 라벨 제약을 공유하나 API는 다름 | CSS는 날짜 고정 Working Draft. ArcMap판 명칭·저작권 정보만으로 정확한 최초 공개일을 단정하지 않음 |
| Avid1999·PremiereCS6 | 영화/방송 편집자, 프레임·표본·In/Out, 정해진 시간 단위 편집 | Audacity와 인접 미디어 도구. 완전히 먼 분야라고 분류하지 않음 | 판이 명시된 원전은 수신 요구보다 앞섬 |
| Netflix·Final Cut Pro 현행 | 자막/영상 편집자, 읽기 시간·색 마스크/범위 표시 | 읽기 편의와 경계 완화의 유사 사례; 음향 spectral gain과 변수 불일치 | Netflix문서 생성2020-07-27이나 확인 본문은2025수정·2026갱신; Apple판 시점 불명. 해당 텍스트를 과거 가용 원리로 소급하지 않음 |
| WCAG2.1 | 접근성 설계자, 비텍스트 시각정보, 인지 가능한 대비 | 색 가독성의 별도 관점. native waveform 적용은 연구자 조건 | 2018고정판. exact-RGB 보존과 essential 예외를 따로 해석해야 함 |

제공 원전 검색어·첫 노출·선택 이유는 [공간 탐색 노트](evidence/spatial-donor-notes.md), [시간 탐색 노트](evidence/temporal-donor-notes.md), 원장의SD/TD/SX/TF행에 있다. 같은 수신 소프트웨어 매뉴얼은 donor수에 넣지 않았다. Audacity644의 AdobeAudition은 원작성자가 이미 명명한 같은 분야 도구이며 새 타 분야 발견으로 세지 않았다.

### Q4·Q5 — 예측과 후속 근거의 단위

사전 쌍 분류는 **다름3(M01,M03,AUD03)·같음2(M02,AUD01)·판별불가1(AUD02)**로 보존한다. 그러나 M01은 다른 조작이면서 양쪽 출력 설명이 양립할 수 있고, AUD03은 실제 수신 알고리즘이 아닌 toy모델이다. 이3을 곧바로 검증 가능한 성공률의 분모로 삼지 않았다.

원래 SCOPE는 “사전 두 예측이 갈리고 같은 입력의 후속 증거가 있는 요구 수”라고 썼으며, 두 입력과 A/B 모두의 완결 비교를 명시하지 않았다. 결과를 읽은 뒤 두 봉인 입력과 경쟁 조작까지 요구한 것은 **사후에 강화한 운용 기준**이다. 이를 사전 규칙과 같다고 서술한 초안을 최종 방법 재판독에서 고쳤다. 원문과 봉인12행을 보존하고 다음 세 집계를 나란히 둔다.

| 판정 기준 | 포함 사례 | 분모 | 유일 지지 | 양쪽 기각 | 분모 안 판정불가 | 해석 |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 사후 명시한 완결 비교: 같은 조작·정상/경계 입력·목적의 경쟁 출력 | 없음 | 0 | 0 | 0 | 0 | 조건부 비율 해당 없음 |
| 원래 문구의 관대한 해석: 원예제 A의 정성적 R보고도 같은 입력으로 포함 | M01 | 1 | 0 | 0 | 1 | A의 경계 조작은 조건부 지지하나 B미관측, P2도B실패를이미예상하여 원리 유일지지는없음 |
| 입력 동일성도 완화한 조작 수락 감도 | M01·M03 | 2 | 0 | 0 | 2 | M03의factor별출력은불명. 같은 입력 검증으로 부르지 않는 operator-only확대 |

0/1과0/2는 확인된 유일 지지가 없다는 집계이며 효과가 없다는 증명이나 실패율이 아니다. M02는 조작 수락이 있어도 사전 동률이므로 세 기준 모두 판별 분모에서 제외한다. 원래6자리의 넓은3/2/1분류는 그대로다. 각 입력 일부의 정성 보고는 아래처럼 따로 보존한다.

| 사례 | 결정·명세(D/S) | 코드(C)·시험 정의(T) | 공개 실행 보고(R)·릴리스(L) | 완결 비교 근거로 올리지 않은 이유 |
| --- | --- | --- | --- | --- |
| M01 | canvas.draw제안 | Cartopy1355의공통preprocess와지도시험;1370의철회 | 원작성자 간단 예제 성공;후대 새판에서 재현불가 보고;0.18/0.19설명 | 정상 대조/B 없고 후속시험은 다른 지도 입력 |
| M02 | set_in_layout제안·후대문서18100 | 새 issue-linked코드 수정 미확인 | 작성자 수락 | 두 후보 동률;10/30개 고정bbox 시험 없음 |
| M03 | transAxes제안 | PR13603 None guard;test_collapsed | 작성자 text해결보고;PR작성자의 별도시험 통과보고;3.1.0변경목록 | 같은 이슈의 서로 다른 문제. crash시험을anchor시험으로 대체할 수 없음 |
| AUD01 | 시간과track선택 목적 논의 | 6165·6347의 제3API | 다른 입력 기여자 보고;3.6.0릴리스 | 원래A/B가 아니며 봉인점/구간 입력 없음 |
| AUD02 | Audacity4해결 선언;2713유보 | 같은RGB fixture변경 미확인 | 원작성자 동일입력 재시험 미확인 | 체크박스·닫힘·해결선언이 출력정책을 말하지 않음 |
| AUD03 | 이슈 댓글은 참여·토론 안내 | 요구 이전localundef와2024cleanup | 동일입력T/R없음 | 활성 API를 전제한 사전 판독 오류;toy를실행증거로쓸수없음 |

위 표의 개별 URL·고정판·범위는 표1과 [outcomes.csv](outcomes.csv)에 있다. R은 공개 작성자의 실행 보고를 뜻하며 본 연구자가 같은 binary를 실행했다는 뜻이 아니다. 본 연구에서는 역사적 Matplotlib/Cartopy/Audacity를 실행하지 않았다. 확인 환경은Python3.12.14·Matplotlib3.10.8이며Cartopy,Audacity,Conda/Mamba가 없었다. 설치·과거 환경 해결을 시도한 것으로 쓰지 않았다. [환경 관측](evidence/environment-execution-status.json), [정확한 재개 명령·입력](evidence/reproduction/REPRODUCE.md), [Audacity 재개 절차](evidence/reproduction/AUDACITY-REPRODUCE.md)에 남겼다.

### Q6 — 반례·관점·입력과 판 민감도

**시각 설계자와 데이터 독자.** M02에서 axes크기를 보존하는 B는 범례 일부를 잘라 계열 의미를 잃게 할 수 있다. [QGIS2.18의 겹친 점 displacement](https://docs.qgis.org/2.18/en/docs/user_manual/working_with_vector/vector_properties.html) L324–326도 표시 위치를 원좌표와 분리한다. 가독성은 좋아질 수 있어도 정확한 화면 위치는 달라진다. 같은 값을 어디에 고정하는지 명시해야 한다. M03을 중앙 설명이 아니라 실제 y값.5의 주석으로 바꾸면 y-data에 고정하는 B의 논리가 적합해진다. 다만 기본 text(.5,.5)는 x도data좌표이므로, 가로 중앙을 함께 요구하면 혼합 transform 등 별도 처리가 필요하다. B전체를 그대로 권하는 뜻은 아니다. 원래 목적을 유지한 실험으로 이 목적 변경을 섞지 않았다.

**음향 편집자와 영상 편집자.** 25fps의 한 frame은0.04초,48kHz의 한 sample은1/48000초로1920배 다르다. 같은 In/Out 표시가 한 frame을 포함하는 규칙과 길이0인 점의 조회, invalid temporal fragment는 다른 연산이다. sample에서의 정밀도 논리를 주파수 bin의 선택 범위로 그대로 옮길 수 없다. [봉인 원전](evidence/temporal-donor-notes.md), [산술 검산](evidence/verification.json)의AUD01/AUD03에 연결했다.

**유지보수자와 기능 요청자.** [Cartopy1370](https://github.com/SciTools/cartopy/pull/1370#issuecomment-569853924)은 초기 전역 범위가 데이터 자동 범위를 잃어서 철회됐다. [PR1956](https://github.com/SciTools/cartopy/pull/1956)은 다른 큰 pcolormesh입력에서 중복bbox계산 비용을 비교한 작성자 보고다.638ms와2.37ms는 해당 비교의 보고값이며 M01실행시간으로 쓰지 않았다. [Audacity의localundef](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77)는 숨은 선택 영향의 UI문제를 우선한다. 좋은 경계 원리도 수신 API가 전달하지 않는 조건에서는 실행 가능한 추천이 아니다.

**색의 의미를 보존하는 편집자와 가독성 정책.** [Audacity5653](https://github.com/audacity/audacity/pull/5653)의 copy/paste·split·판 호환 QA와 실제 색 초기화 회귀보고는 색을 지속되는 상태로 취급한다. 자동 대비 보정으로 선택색을 바꾸면 그 목적을 해칠 수 있다. 반대로 읽을 수 있는 waveform이 최우선이면 동일색1:1을 유지하기 어렵다. 외곽선이라는 제3안은 선택영역과 waveform의 서로 다른 대상을 동시에 해결한다고 보장되지 않는다.

| 변경하는 조건 | 계산·원문 관측 | 원래 결론의 유지 여부 |
| --- | --- | --- |
| M03factor .01→.001→.1, linear limits [0,99factor] 가정 | B의 y비율50/99→500/99→5/99; A는1/2 | 중심 목적에서는 A조작 가설 유지. 실제limits·출력은 미실행 |
| M03수신판3.0.2→2.2.2 | [2.2.2 _mesh L843–861](https://github.com/matplotlib/matplotlib/blob/b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68/lib/matplotlib/colorbar.py#L843-L861) 정규화좌표;3.0.2는조건부norm.inverse | B도.5중앙일수있어판별차이가사라짐. 정적판독 |
| M03vmin이0이아님 | 올바른중앙data값은vmin+(vmax−vmin)/2 | [댓글470147866](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470147866)의절반범위만으로일반화하면실패 |
| AUD03기하평균5bin→선형gain평균5bin | 경계−2.4→약−1.9330457dB | 구별은남지만고정출력은변함. 다른kernel실험 |
| AUD03feather를선택안쪽에만제한 | 바깥bin86은B도0dB | A/B경계차이소멸 |
| AUD03N2048→4096,Fs48000유지 | 첫제외bin86→171;oldbin86은1007.8125Hz로안쪽 | bin번호를고정하면다른물리입력. 새경계로재정의할때만같은toy관계 |
| AUD03Fs48000→44100,N2048유지 | 첫제외bin93,약2002.58789Hz;oldbin86은1851.85547Hz | 같은번호를같은주파수로옮기면틀림 |
| M02font/page/orientation비용제약해제 | [CSS §8.2](https://www.w3.org/TR/2013/WD-css3-page-20130314/) 회전·축소·분할대안재개 | clip만권할이유약화. 실제데이터가독성비용은미측정 |

숫자는 표준 라이브러리로 실행한 조건부 모델 검산이며 실제 수신 소프트웨어 출력이 아니다. [verify-research.py](evidence/verify-research.py)와 [verification.json](evidence/verification.json)이 입력·식·출력을 함께 남긴다. 제공 규칙은 같은데 모델의 평균 공간, 경계 정의, 목적을 바꾸어 답을 바꾼 경우를 새 관측처럼 세지 않았다.

### 노출·판 필터 감도

| 집합 | 남은 원래 자리 | 넓은 다름 / 같음 / 판별불가 | 완결 비교 분모 | 유일 지지·양쪽 기각 | 조건부 비율 |
| --- | ---: | --- | ---: | --- | --- |
| 원래전체 | 6 | 3 / 2 / 1 | 0 | 0 / 0 | 해당 없음 |
| E01노출AUD02제외 | 5 | 3 / 2 / 0 | 0 | 0 / 0 | 해당 없음 |
| 추가로E02교차판노출AUD01제외 | 4 | 3 / 1 / 0 | 0 | 0 / 0 | 해당 없음 |
| 알려진현행제공판의존AUD02·AUD03제외 | 4 | 2 / 2 / 0 | 0 | 0 / 0 | 해당 없음 |
| 정확한생성시점본문만 | 0 | 0 / 0 / 0 | 0 | 0 / 0 | 해당 없음 |

원래 문구의 관대한 분모1(M01)과 조작 수락 분모2(M01·M03)는 위의 전체·E01제외·E01+E02제외·현행판의존제외에서 각각1과2로 유지된다. 정확한생성본문필터에서는둘다0이다. 유일지지는모든집합에서0이며, 분모1/2의사례는모두판정불가다. 세 번째 필터와 네 번째 필터는 서로 다른 감도 집합이다. 현행 제공판을 빼도 USGS·ArcMap·CS6의 정확한 최초 공개일이 모두 확정되는 것은 아니다. 최초본문 필터가0이라는 이유로 원래6요구를 삭제하지 않았다. 이 감도는 회수율, 전체 개발자 집단의 비율, 표본외 예측 성능을 추정하지 않는다.

### Q7 — 반환할 링크와 주장할 수 없는 것

[카드6개](cards.md)는 세 수준을 분리한다. **완전한 원리→조작→두 판별 입력→같은 입력 후속근거 사슬은0/6**이다. M01/M02/M03은 기존 조작과 정성적 후속 수락을 연결한 조건부 진단 링크를 반환할 수 있다. AUD01은 실제 제3getter 구현과 경계 의미를 반환할 수 있지만 donor가 A/B를 골랐다고 할 수 없다. AUD02는 RGB보존·대비·범위표시의 요구 충돌을 짚는 참고, AUD03은 적용 API와 변수 대응이 깨지는 가설 카드다. AUD03/P2의 시각적 softness는 모양이 비슷한 사례 수준을 넘었다고 입증하지 못했다.

새로운 구체 선택 여부, 양쪽 후보의 같은 조작 일치, 저자 채택은 각각 분리했다. M03의 중앙 목표와M02의overflow처리는 이미 요구에 있었고, 당시 공개 API도 있었다. M01의pre-draw처럼 목표보다 상세한 제안을 했어도 외부원리를 제공하지 않은 비교조건이 없으므로 추가효용을 추정할 수 없다. 세 시각 사례의 작성자 수락은 **유지보수자 조언의 수락**이며, 여기서 제공한 인쇄·지도 원전의 채택 증거가 아니다. AUD03의Audition은 이미 알려진 참조다. 어느 사례도 역사적 영감·최초안 변경 인과·늦게 알게 된 수정노동의 감소를 측정하지 않았다.

## 자료 수·검산·재개

[sources.jsonl](sources.jsonl)에는 **159열람/탐색/재방문 기록, 최소수에 산입한 고유1차 저작30개**가 있다. 실패한 전문 접근·검색 결과·같은 저작의 다른 절·댓글·미러·재방문은 추가로 세지 않았다. 하나의 저작은 최소 배당 한 곳에만 넣었다.

| 배당 | 실제 고유 저작 | 목표 | 해석 |
| --- | ---: | ---: | --- |
| 최초 요구 | 6 | 6 | 현재첫본문;불변최초판은별도미충족 |
| 제공 원전 | 9 | 8이상 | 공간4·영화/방송4·접근성1. 시간경계원전 자체는Avid/Premiere/Netflix3 |
| 수신 후속 | 9 | 6 | Cartopy1370/1422/1355,Matplotlib18100/13603,Audacity6165/6347/2713/6201. 유보·정리·다른fixture도증거범위를명시 |
| 독립 비교 | 6 | 4 | OS,QGIS,W3C Media Fragments,Smith,Cartopy1956,Audacity5653 |
| 합계 | 30 | 24 | Audacity3.6release는6165같은변경의재게시로보수적중복처리 |

후속 저작9개를 읽었다는 수량과, 원래 입력의 후속 시험0건이라는 실질 요건은 서로 다르다. 최소수를 맞추려고 요구를 교체하거나 관련 없는 시험을 같은 입력으로 바꾸지 않았다. M01의관련시험·M03의별도crash시험·AUD01의제3API·AUD03의비활성정리는 각각 그 범위에서만 썼다.

검산은 [SELF_CHECK.md](SELF_CHECK.md), [수용 항목 원장](evidence/acceptance-evidence.json), [기계 검산](evidence/verification.json)에 연결한다. 같은 모델의 별도 문맥 판독을 받았고 root가 핵심 원문을 다시 열었다. 외부 독립 인간 판독이나 독립 실험은 수행하지 않았다. 자료 수와 구조 검사 통과를 내용상 성공으로 부르지 않는다.

재개 첫 행동은 **M03의 고정3.0.2 환경을 확보하고, 봉인 factor .01/.001에서 A/B 각각의 실제 colorbar limits·anchor를 기록**하는 것이다. [준비한 명령](evidence/reproduction/REPRODUCE.md#m03--실제-colorbar-범위anchor와-판-민감도)은 과거 공개 실행을 복원한 것이 아니라 새 연구자 검사다. 역사적 검증을 채우려면 해당 입력·판을 명시한 당시 공개 로그를 별도로 찾아야 한다. AUD03은 실행에 앞서 spectral selection을 실제로 전달하는 API/구현부터 확인해야 한다.

## 마지막 약점 3건

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 현재 첫 본문·현재 제목을 사용했고AUD02사후목록과AUD01교차판노출이 있음; 불변최초판0/6 | 완전 맹검·역사적 표본 재현·과거 가용성 | [511 timeline](https://api.github.com/repos/audacity/audacity/issues/511/timeline?per_page=100)2022rename; [13600](https://github.com/matplotlib/matplotlib/issues/13600#issuecomment-470135635); [amendments](amendments.md)E01/E02 | 선정 요구의 편집 이력·당시 본문/제목 snapshot 한 건부터 복원 | 예측에 쓰인 요구판이 해결 노출 전과 같고 당시 검색 규칙에 해당함을 확인 |
| 정상·경계와 두 조작의 같은 입력 후속시험0/6; M01은 조작 차이와 예측 대립도 다름 | 원리가 A/B를 유일하게 가른다는 성공·수정노동 절감 | [M01수락](https://github.com/matplotlib/matplotlib/issues/13430#issuecomment-463401327); [M03별도시험](https://github.com/matplotlib/matplotlib/blob/f9d8cd7e0c9a4e94962fc925c57fb678ba252f87/lib/matplotlib/tests/test_tightlayout.py#L313-L327); [outcomes.csv](outcomes.csv)12행 | M03고정3.0.2의두factor·A/B실제anchor와당시공개동일입력로그 확인 | 같은조작·입력·목적에서 예상출력을관측하고 경쟁예측을구별할수있음 |
| AUD03localundef 사전누락, toy kernel·현행영상판·단위 대응 제약 | 당대API실행가능성·타분야원리의정량예측 | [2.4.2 L75–77](https://github.com/audacity/audacity/blob/16d52f63a4183bba77ef7305d14622958dc0d1d5/src/effects/NoiseReduction.cpp#L75-L77); [2024변경](https://github.com/audacity/audacity/commit/e7d17d1bcedcb1fe75d78eb522de3b46476c94b7); [검산](evidence/verification.json)AUD03 | 실제활성API·고정window/overlap/noiseprofile와bin64/86출력 확보; 제공원전당시판 확인 | 실행가능한수신조작과제공규칙의대응이확인되고toy가아닌실제같은입력시험이추가됨 |
