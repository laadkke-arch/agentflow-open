| 결정·날짜 | 당시 대안 | 편집 전후 문구·원전 URL | 이유를 밝힌 주체·원문 | 미확인 |
|---|---|---|---|---|
| 표 1 / 2023-10-09 및 11-29/30: 작성자 문제 제기 (J01) | 채널 clip, L/H 보존 매핑, RGB 한 채널 예외 | [#9449 본문 및 댓글](https://github.com/w3c/csswg-drafts/issues/9449): 동일 L/H 작성값이 다르게 표시. oklab(.9,.36,0)의 clip 및 CSS 매핑 수치 제시 | Miriam Suzanne는 작성자의 명도 기대를, Cameron은 장치 의존성과 캔버스 일관성을, Lilley는 색차·매핑 목표를 지적 | 화면·관찰자 실험 미확인 |
| 2024-07-16: #10579 제안 (J02) | 기존 GMA, Rec2020/근사 경계, YUV 투영 등 | [제안·초기 댓글](https://github.com/w3c/csswg-drafts/issues/10579)에서 정적 색역 매핑 평가. 제안이지 규범 아님 | Cameron: 빠른 경계 탐색·색역 모양; Lilley: YUV의 U/V가 지각 균일성을 보장하지 않음 | 모든 대안의 최종 채택·기각 이유 미확인 |
| 2025-04-24 CRD (J03) | Local MINDE 이진 탐색 또는 기하식 설명 | [A01 §13.2](https://www.w3.org/TR/2025/CRD-css-color-4-20250424/#css-gamut-mapping) 단일 알고리즘, 공통 OKLCh·ΔEOK·Local MINDE; JND 0.02; 기하식에서 경계 바깥 투영과 국소 clip | CSSWG 문서: 채도 감소가 과도한 경우를 개선; [§13.1](https://www.w3.org/TR/2025/CRD-css-color-4-20250424/) 비규범 예 | JND의 구체 실험·observer·화면 미확인 |
| 2025-08-19 결의 (J04–05) | 기존 + 새 두 방법; 새 두 방법만; 기존 방법 유지 | [공식 IRC 기록](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200859856) 결의의 핵심: “require one of the three” | ChrisL: 현 알고리즘 비효율, 품질/성능 설명; Florian: 시각 유사성과 기존 선택 유지; fantasai: 시장/하드웨어 차이 허용. [Lea](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200476676) 밝은 tint clip 가설을 OOG 크기 가능성으로 수정 | 세 방식 동등한 지각 효용을 측정한 실험 없음 |
| 2026-01-22 22:45 UTC 편집 (J06) | 이전 일반 Local MINDE 문구 vs 세 알고리즘 | [f5642b9 Overview.bs diff](https://github.com/w3c/csswg-drafts/commit/f5642b931d905128daa075fdfeba6c9e74475b5a) @@5755,5788,5910: 3개 선택·사용 의무, Local MINDE를 binary subsection으로 이동, geometric 문단 주석화, EdgeSeeker/Ray Trace 추가 | [편집자 23:02 댓글](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3787184061): display mapping 선택, computed-value Rec2020는 별개; pseudocode 부담, timing 미수록; diff에 제작자 구현 링크 | 초기 EdgeSeeker Weber→A02 Ardov 정정 경위; 외부 지각 논문이 세 선택 변경을 직접 유발했는지 미확인 |
| 2026-06-23 16:33 UTC 수정 (J07) | 단일 경계 ε vs 정밀도별 ε | [24a74f8 Overview.bs diff](https://github.com/w3c/csswg-drafts/commit/24a74f8c006709dfbf0538af80ea3086b213228e) @@6300/6339/6366/6416: f64 1e-12, f32 1e-6; 부등호·변수 교정 | 수치적 교차 계산과 구현 정확성 | 수정 후 실측 및 장치 성능 미확인 |
| 2026-07-12–14 경쟁 구현 (J08) | Halley, cubic, clip, LUT EdgeSeeker | [앱 PR44](https://github.com/color-js/apps/pull/44): bracketed Halley 합병, sRGB/Rec2020 blue fold 논의; CSS 채택은 아님 | Ardov 속도·정확한 C 감소, Muse 비교 조건 및 fold 추가 비용, lloydk P3 별도 벤치 | 다른 입력·환경에서 순위 달라짐 |
| 2026-08-25 CRD (J09) | Binary Search Local MINDE, EdgeSeeker, Ray Trace | [A02 §14.2 및 Changes](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/#css-gamut-mapping): 품질/실행시간을 고려해 셋 중 선택, 요구되는 곳에서 선택한 방법 사용. 공통 상대색도, 색역 내 유지, L/H 유지 지향. §14.2.4 EdgeSeeker pseudocode placeholder, §14.2.6 Ray Trace pseudocode | CSSWG 편집 본문 및 2025 결의 반영; LUT 메모리 vs 반복 비용; [Changes](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/#changes) #10579·clip 균형화·Ray 수정 | 모든 브라우저 채택/측정 아님; 독립 알고리즘 간 시각 평가 없음 |

| 주장 | 색·매체·관찰 조건 | 자료 URL·도표 | 지각 실측·계산·규약 구분 | 경쟁 설명·반례 |
|---|---|---|---|---|
| 표 2 / 색역 내 색 유지 | 개별 SDR RGB, 목적지 내 | [A01 §13.2](https://www.w3.org/TR/2025/CRD-css-color-4-20250424/) 및 [A02 §14.2](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/) | 규약; L≥1 백, L≤0 흑. 중간 변환은 정보 보존 | 사진 전체 perceptual 처리에서는 색역 내도 변할 수 있다 |
| clip의 큰 hue 변화 vs 작은 변화 | 일반 OOG linear sRGB (.5,1,3), 별도 rec2020(.54,.9,0)→P3 | [A02 §14.1.1](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/#clipping): 265.1→196.1°; P3 clip 예 L80.72→80.79%, C.3296→.3221, h141.6→142.3° | 두 계산 예, 관찰자 0 확인(실제 수 미확인), 화면 미확인 | 근소한 음수 blue는 clip으로 충분할 수 있다. §14.1은 비규범; 독립 clip을 허용하는 규범 변경은 아니다 |
| 밝은 포화 노랑/청록 | P3 yellow(1,1,0)→sRGB; 얕거나 오목한 경계, 높은 L | [A02 §14.1.3–5](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/): sRGB(1,1,-.3463), OKLCh(.96476,.24503,110.23°), C 감소 .21094. 청록은 문장 예(입력 수치 미확인) | 계산·도표 설명; 단색의 명도/색상 보존 방향 | CIE LCH 단순 감소는 노랑 C 과감소, OKLCh만으로도 개선 예; Lea의 L-only 설명은 OOG 정도와 교란 |
| 작성자 L/H 의도 보존 | oklab(.9,.36,0), sRGB/P3; L99% tint도 보고 | [#9449 Lilley 댓글 및 matuzo 2025-04-07](https://github.com/w3c/csswg-drafts/issues/9449): clip L.6836/h338.36°, CSS L.861/h357.323° | 계산 및 당사자 보고, 관찰 조건 미상 | 둘 다 원색과 다름; 단일 RGB red의 clip은 더 자연스러운 목표일 수 있음 |
| 색상 공간의 개선 근거 | D65 정상 밝은 환경 전제, CAM16 합성쌍 및 IPT hue 자료 | [C01 원저자](https://bottosson.github.io/posts/oklab/) 비교 표 Oklab RMS ΔE00 L.20 C.81 H.49 | 계산 적합, 새 관찰 실험 아님 | CAM16 L/C 적합치 0은 구성상 유리; IPT H .48, JzAzBz H .43. 모든 항목 최고 아님 |
| 실제 지각 hue 균일성 연구 | calibrated CRT, 15 hue, OOG는 Lab50,0,0, 경험 관찰자 | [C02 Ebner/Fairchild p13 Fig10](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/6/1/art00003): 9명, 30세션, 세션당 90판단; 48° 비교 ~.75 scale unit, 144° 차이 없음 | **실측 보고**: IPT vs 두 constant-hue 데이터; 제한된 자극 | 별도 CIELAB 비교에서도 48°에 약 .5 unit 우위 보고. CSS 알고리즘 및 JND를 비교한 것이 아님 |
| JND·색차는 동일한 대상 아님 | 색쌍·조명·기준 백색, CRT와 다른 데이터 | [C03 Luo 등](https://doi.org/10.1002/col.1049), [C04 Li 등](https://doi.org/10.1002/col.22131), [C05 Sharma 등](https://hajim.rochester.edu/ece/sites/gsharma/papers/CIEDE2000CRNAFeb05.pdf): C03 3657쌍/가중 유효 11273, C04 3813/2953/1053쌍, C05 p25 mean-hue discontinuity | 실측 재분석·수학적 결과; ΔEOK .02는 A01/A02 문서 규약, Ray ε는 수치 경계 | ΔE00에 100 스케일을 적용한다고 다른 공간의 검출확률까지 동일해지지 않는다; 실제 시청 조건·분포 필요 |
| 낮은 구현 비용 | D08 constant L plane, 50×50 sRGB 계산; D04 25-pass P3 비교 | [D08 저자 비교기](https://svgees.us/Color/ok-clip-lch-explorer.html): 2500개 평균 75/4/230 μs(MINDE/clip/LCH); [D04 PR44](https://github.com/color-js/apps/pull/44): Rust random clip 28.30, Halley 98.83, Ray 227.15 ns/call | 당사자 실행 보고; 여기서는 새 실행 없음 | PR44의 P3 workload는 fold 제외, below-cusp 74.5% 보고, 코드 작성 AI 보조. 비용·목표·cache 분리해야 함 |
| blue fold 및 더 나은 경계 탐색 | sRGB #0000ff → C 증가 → 역매핑 | [D04 PR44 Ardov 7/13](https://github.com/color-js/apps/pull/44): 두 후보 #0000ff/#0031e5 ΔEOK .048 | 저자 계산, 사람이 차이를 느꼈다는 자료 없음 | first exit와 최대 feasible C는 목적이 다름. 추가 solve 비용 필요성은 미확인 |
| 사진과 인쇄의 전이 한계 | 저자 꽃/램프/튤립/보트 사진, 출판 CMYK와 용지 | [D01 원저자 예](https://bottosson.github.io/posts/gamutclipping/) α .05/.50/5; [E01 ICC Fig6](https://archive.color.org/files/WP40-Black_Point_Compensation_2010-07-27.pdf), [E02 Blurb workflow](https://support.blurb.com/hc/en-us/articles/360027277391-Preparing-color-images-for-Adobe-InDesign-or-Blurb-s-PDF-Uploader-workflows), [E03 Epson](https://epson.com/Support/wa00351) | 저자 계산/정성평가, 인쇄 작업 규칙(실제 측색·사람 표본 미확인) | 상대색도+흑점 또는 perceptual, 기기·용지·사용 목적에 따라 달라짐 |

| 설계자 목적 | 가까운 원전 | 외부 원전이 더하는 조건 | 선택이 달라지는 지점 | 남는 한계 |
|---|---|---|---|---|
| 표 3 / 허용 알고리즘 확인 | [A02 §14.2](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/#css-gamut-mapping), [A03 diff](https://github.com/w3c/csswg-drafts/commit/f5642b931d905128daa075fdfeba6c9e74475b5a), [B02 회의](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200859856) | 색과학 원문은 필수 아님; 왜 L/H인지를 요청하면 [C01](https://bottosson.github.io/posts/oklab/) | 문서판 고정; 세 선택 중 하나; clip을 일반 대체로 권하지 않음 | 엔진 구현판·기기·의사코드 보강 필요 |
| 허용 오차의 근거 | [A02 §14.2.1](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/), [A04 ε diff](https://github.com/w3c/csswg-drafts/commit/24a74f8c006709dfbf0538af80ea3086b213228e) | [C01 Oklab](https://bottosson.github.io/posts/oklab/), [C02 hue 실측](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/6/1/art00003), [C03 ΔE00](https://doi.org/10.1002/col.1049), [C04 CAM16](https://doi.org/10.1002/col.22131), [C05 수학](https://hajim.rochester.edu/ece/sites/gsharma/papers/CIEDE2000CRNAFeb05.pdf) | 수치 tolerance와 지각 threshold 분리; 매체·조명·표본·자극·거리 단위를 확인; 해당 조건의 검증 없으면 숫자를 일반화하지 않음 | 0.02 보편 JND 또는 3 GMA 사람 우열 증명 없음 |
| 인쇄나 사진의 외관 | [A02 note](https://www.w3.org/TR/2026/CRD-css-color-4-20260825/), [B05 ColorAide](https://facelessuser.github.io/coloraide/gamut/#ray-tracing-chroma-reduction) | [E01 ICC](https://archive.color.org/files/WP40-Black_Point_Compensation_2010-07-27.pdf), [D01 사진](https://bottosson.github.io/posts/gamutclipping/), [E04 darktable](https://docs.darktable.org/usermanual/5.6/en/module-reference/processing-modules/filmic-rgb/), [E02 Blurb](https://support.blurb.com/hc/en-us/articles/360027277391-Preparing-color-images-for-Adobe-InDesign-or-Blurb-s-PDF-Uploader-workflows), [E03 Epson](https://epson.com/Support/wa00351) | 점별 원색 고정→관계·계조·그림자 보존, 종이 기준 백/흑점과 profile. 사진과 인쇄의 목표도 다름 | 실제 target profile, 이미지·시청환경, 색관리 단계 필요 |

## 판정 요약

**두 CRD 및 실제 결의/편집의 연결은 성립한다.** 외부 원리로부터 L/H 보존을 목표로 삼는 이유와 모델·조건의 제한을 설명할 수 있고, 가까운 편집/구현 자료로부터 세 알고리즘을 허용한 직접적인 성능·품질·하드웨어 선택 이유를 설명할 수 있다. 2025→2026 변경에서 특정 지각 논문을 읽고 그 때문에 세 방법을 선택했다는 증거는 발견하지 못했다. 두 판에 Oklab 원저자 문헌이 규범 참고로 존재한다는 것은 직접 문헌 연결이지 그 변경의 인과 증명은 아니다.

## Q1. 판별 가능한 규범 변경과 같은 문장

| 문장 단위/역할 | 2025 §13.2 | 2026 §14.2 | 판정 |
|---|---|---|---|
| 개별 SDR, RGB 화면, 색역 밖 | 한 알고리즘 | 3 알고리즘 | 대상 유지·허용 집합 확장 |
| 선택과 사용 | 단일 알고리즘의 설명 | 품질/실행효율에 맞춘 선택, CSS 요구 시 선택 방법 사용 의무 | normative permission + obligation |
| 상대색도/색역 내 | 유지 | 유지 | 규범적 보존 |
| 인쇄 및 이미지 note | 백/흑점·이웃 픽셀 | 같은 목적 구분 | 비규범 적용 한계 |
| OKLCh 및 색차 | 공통 ΔEOK·Local MINDE | 공통 L/H 유지 지향 C 감소, ΔEOK·Local MINDE는 binary subsection | 비용/출력 선택 차이 허용; 엄격 L/H 수치 보존 보장 아님 |
| 백흑 | L≥1 백, L≤0 흑 | 유지 | 규범적 경계 |
| 국소 clip | binary의 JND 및 geometric 설명 | binary §14.2.1 JND, §14.2.2 pseudo; geometric paragraph 삭제·새 방법 소개 | JND .02 유지, 모든 방식에 강요하지 않음 |
| 추가 방법 | 별도 없음 | EdgeSeeker §14.2.3–4, Ray Trace §14.2.5–6 | LUT memory vs 예측 가능한 반복; EdgeSeeker pseudo placeholder |
| §13.1→14.1 설명/그림 | 단순 clip의 문제, 노랑/청록·blue hue | 근소 OOG clip 허용 가능한 결과 예 추가 | 비규범적 품질 설명이지 4번째 허용 알고리즘 아님 |

A01/A02 원문 및 A03 actual diff의 공통 문장 단위 대응. CRD Changes에서 #10579 알고리즘·Ray pseudocode/correction·clip 균형화가 명시됨. A04는 Ray 계산 정밀도 교정이다. A02 Changes #13157의 색 동등성 ε=0.00001와 #14207의 별도 ΔEOKr2도 구별: §14.2.1의 .02를 대체했다는 문장이 아니다. A02는 현 판의 동작을 지정하는 CRD이며 엔진별 출하 확인이나 단일 알고리즘만 남았다는 결론이 아니다. 두 판의 note는 인쇄/사진이 다른 목적임을 명시한다.

## Q2. 누구의 기준과 어떤 시간축인가

B03 2023-10-09 Miriam의 작성자 불만; 11-29 Cameron의 P3 red, canvas deterministic 문제와 표준 경계 제안; 11-30 Lilley는 입력 공간과 매핑 공간을 분리. #10579로 이어져 B01 2024-07-16 Cameron은 정적 GMA, 속도와 경계 형태를 문제 삼는다. B03 2025-06-04 jyasskin은 Rec2020 이후 clip 자유를 브라우저 구현자가 요구했다고 이해했다고 보고; 모든 엔진의 독립 확인은 아니다. B02 2025-08-19 기록: ChrisL의 비효율 제기→Florian의 시각적 유사성 질문→ChrisL의 3가지 성능·품질 notes 제안→Florian의 기존 선택 보존→fantasai의 타 시장/하드웨어 가능성→셋 중 하나 의무 결의. D07 같은 날 Lea는 밝은 tint 현상과 OOG 크기를 구분하도록 가설을 수정; Muse는 사진과 단색 타협을 구별했다. A03 2026-01-22의 diff 및 X03 편집자 확인은 결의의 구체 구현이다. A04와 A02는 추가 보정. D03/D04는 후속 구현자 경쟁과 비교 공정성 논의다. 논의에서 실제로 발언하지 않은 연구자 또는 관찰자를 의사결정자로 만들지 않는다.

## Q3. 어떤 자극/조건인가

세 층을 분리했다. (i) 목적지 안: A02 보존 규칙. (ii) 밝은 노랑/청록: A02 §14.1.3–5의 얕은/오목 경계와 P3 yellow 정량값, B03의 L99% tint. cyan의 별도 정확 좌표·측정값은 미확인. (iii) 일반 OOG: A02 clip 큰 hue shift와 작은 음수 blue 반례, B03 L.9 magenta 예. 이들은 모델 계산 또는 저작자 보고이다. D08의 50×50 비교 및 D04의 random workloads는 시간을 측정한 당사자 보고이지 색을 본 사람이 판단한 표본이 아니다. 관찰자 확인이 있는 C02의 9인 CRT 강제선택은 IPT의 hue 균일성 문제를 제한 조건 하에 검증했을 뿐 CSS 세 GMA나 현대 RGB 화면의 JND를 직접 검증하지 않았다. C03/C04는 기존 데이터 재분석이라 물리적 N과 가중 N을 구별해야 한다. 그림은 원문의 도표 설명/수치/캡션을 읽었으며 색 샘플 자체의 화면 렌더나 픽셀 판독을 하지 않았다.

## Q4. 외부 원리가 어디까지 좁히나

두 CRD의 References [Oklab]에서 C01을 직접 등재하고, C01은 IPT hue 실험 계보 및 CAM16 모델 쌍을 이용한다. C02 원논문은 실제 시각 비교를 제시하고 48°/144°에서 차이를 구별한다. C01의 선택은 정상 밝은 조건·단순 가역 변환·색상 균일성 등 목표의 절충이다. ΔEOK는 좌표 차이 계산, JND는 주어진 관찰 조건에서 감지되는 차이 개념이며, 스펙의 .02는 binary local clipping의 문서상 기준이다. C03의 색차 자료와 C04의 조명·크기별 데이터가 조건을 좁히고 C05가 수학적 경계/구현 오류를 경고한다. CIEDE2000 2와 ΔEOK .02의 스케일 관계를 모든 관찰 조건에서의 감지 확률 등가로 해석하지 않는다. ΔC/C의 관계를 포화도와 동일시하지 않는다. 색역 경계는 목적지 RGB·프로필·범위라는 규약/기하이며 그 자체가 지각 실험 결과는 아니다.

직접 연결이 하나 더 있다: A02 Sample code ΔEOKr2의 lightness toe에서 [D09 color picker 원저자 식](https://bottosson.github.io/posts/colorpicker/#intermission---a-new-lightness-estimate-for-oklab)으로 직접 연결한다. D09는 Y=1 기준 백색에서 50% lightness 대응 Y .18406(CIELab)/.18419(Lr)을 비교하고, 단순 경계와 지각 속성이 충돌함을 보여준다. 이 연결은 외부 원리가 **별도 metric 설계에 들어온 실제 출처**의 강한 근거이지만 #10579에서 세 GMA 허용 결의를 뒤집었다는 인과로 전이하지 않는다. 두 CRD의 [Oklab] 등재, A03 제작자 링크 및 D09 code comment가 실제 읽은 사슬이며, Hung/Berns 원문은 접근 실패. 원 연구→Oklab 모델→CSS 좌표 선택의 설계 근거는 성립하나 #10579에서 편집자가 특정 연구를 보고 선택을 바꿨는지는 미확인.

## Q5. 가까운 설명과 경쟁 설명

- **충분한 가까운 설명**: 동일 목표 하에서 탐색 비용·메모리·반복 횟수와 정밀도를 비교하려면 A02, A03, A04, B02, B05, D08이면 출발 가능. MINDE는 색차 반복, EdgeSeeker는 경계 LUT와 초기 메모리, Ray는 축정렬 RGB 큐브 교차→OKLCh 보정 최대 4회. 일반적 비용 차이가 곧 고정 속도 순위는 아니다. A02의 비용 이유는 구현 설계자 선택을 설명한다.
- **경쟁 설명 1 — 단순 clip 충분:** A02 근소 음수 blue 및 B03 단일 RGB red 반례. 그러나 큰 OOG, 높은 tint, 중간색은 저작 의도가 변함; 이진 MINDE 내부 clip과 독립 clip 규격 허용을 구별한다. D07의 가설 철회가 밝기만으로 분기하는 설계를 약화시킨다.
- **경쟁 설명 2 — 싼 solver가 충분:** D04 PR44에서 Halley/blue fold는 exact C 감소에 유용하나 P3 random Rust에서는 clip이 훨씬 빠르고 P3에서는 fold 제외. D03 2026-06-19 PR36은 반환 색공간 및 L 검사 공정성 수정. D06 250k Ray/cubic/cache 값은 동일 시간 절대값으로 D08과 합치지 않는다. 연구 도구는 cache, input distribution, conversion boundary, precision, target gamut, hardware를 함께 반환해야 한다.
- **경쟁 설명 3 — 원거리 원리 없이도 선택 가능:** B02 결의에 색과학 실험 데이터는 없다. 외부 원리가 주는 것은 왜 L/H 우선과 JND 조건, 왜 기기/배경이 중요한가의 설명 및 반례다. 특정 solver의 채택을 결정하는 것은 근접 구현 비용·제약이다. Oklab의 간편성/기존 지각 원리 및 CSS 2025 이전에 존재한 저자 도구(D01/D08)를 새로 발견된 원리라고 부르지 않는다.
- **문서 자체 불일치:** B04 Color.js 문서는 현재 ΔEOK 설명과 옛 CIE LCH/ΔE00<2 예를 함께 둔다. 그러므로 CSS의 고정판 규범을 먼저 사용하고 버전 불일치 가능성을 표시. A03 초기 EdgeSeeker 저자명과 A02 최종 참고문헌 저자명이 다르며 정정 근거는 미확인.

## Q6. 다른 분야로 옮길 때

단색 로고 예는 가설적 동일 입력, 실측 브랜드 사례는 아니다. 목적지 색역 안이면 보존, 밖이면 의도 L/H와 브랜드 허용차·배경에 맞게 후보. 인쇄 로고는 반사색/잉크/용지 프로필 및 proof 조건이 달라 실제 시편이 필요하다. 사진은 D01에서 노출 및 chroma를 키운 네 사진 비교와 원저자의 과도 OOG에 압축이 적절할 수 있다는 의견을 확인했다. 점별 색차를 최적화해도 가까운 두 픽셀이 같은 경계로 몰려 디테일·질감이 사라질 수 있다(설계 추론, 신규 시험 아님). E04 darktable filmic RGB의 tone/gamut/profile 의존은 점별 CSS 출력과 다른 층이다. 영상 프레임 사이 시간적 일관성은 중요할 수 있으나 별도 영상 실측 자료 미열람; 사진 결과를 영상 우위로 주장하지 않는다.

E01 ICC WP40 §2/6, Fig6 Sheetfed Coated→ISO Uncoated 사례 및 가상 Y .1–.9→.3–.7은 검은점/흰점과 계조의 대조다. 실제 출판사 E02는 perceptual, BPC, dither 및 embedded CMYK ICC를 구체적으로 지정하고 종이색 시뮬레이션은 모니터 90–120 cd/m² 조건으로 제한한다. E03 Epson은 relative 기본, 매우 포화된 사진은 perceptual, BPC, 용지와 프로필 일치, 드라이버 이중 보정 금지. 같은 인쇄에서도 목적·시스템마다 다르므로 한 intent를 정답으로 강제하지 않는다. E05 Adobe 네 intent 설명은 대조. 작업 지침은 실제 시편의 외관 측정/사람 만족도 결과가 아니다.

## Q7. 탐색기 반환에서 원문의 범위

허용 알고리즘 확인에는 A02와 §14.2 링크, 변경 이유 요청에는 B02/A03, 구현 제약에는 A04/B05/D08을 추가한다. 허용 오차 근거 요청에서는 ΔEOK/JND의 규약 범위와 C01/C02/C03/C04/C05를 함께 링크하되 관찰 조건이 없으면 실제 감지 가능성을 단정하지 않는다. 사진/인쇄 외관에는 CSS note로 전이 금지를 설명하고 실제 출력기/출판사/프로필 지침과 원저자·ICC 자료를 우선한다. 가까운 자료만으로 질문이 종결되면 외부 자료는 선택 첨부다. 외부 원전은 기존 선택을 변경하는 조건(목표/관찰/프로필/비용)을 제공할 때 붙인다. 이 연구는 데이터베이스, API, 검색순위나 일반 검색 성능을 결정하지 않는다.

## 재사용 조건 및 비용 / 후속 분석

source ledger 33행, 적격 22판·자료(21 work_id / 14 lineage_id; 두 CRD 동일 저작), A4 B5 C5 D4 E4. 나머지는 대조/접근 실패. D03의 최초 산입은 ④에서 하향, D09로 보완; 기존 자료 부족을 Git에 보존. 결정 사건은 시간축 9행(정식 결의 1, 편집 커밋 2, CRD 발행 2, 문제/제안/가설/PR 4). 이들은 9개 독립 지각 실험이 아니다. 별개 실측 연구 C02 1건(여러 세션), C03/C04는 기존 관찰 자료 분석; CSS 후보 간 독립 관찰 실험 0건 확인(존재하지 않음을 증명하는 값 아님). D01/D04/D08/D09는 서로 다른 저자 도구·계산/보고 원자료. 인쇄 E02/E03 실제 workflow, 출력 실측은 미확인.

실제 브라우저 구현·픽셀·코드 실행·대량 재생·새 지각 실험은 이번 제외. 원문 판/URI, 정확한 의도, 단위, 관찰 조건을 기록할 때 지각 실측과 계산/설계 추론 혼동을 줄인다. 스펙 두 판과 커밋을 먼저 제공하면 작은 구현 확인 비용; 외부 과학 원전은 데이터 조건을 확인할 때만 추가 비용이 정당화된다. 사용자에게 전달할 후보 링크 구성 예이며 최종 검색랭킹 선택이 아니다. 다음 단계는 실제 판별 조건을 뒤집을 자료에 한정: JND의 출처/observer protocol, EdgeSeeker 정정/코드 경로, 사진 및 프린트 실제 장치·프로필 관측. 이번 조사에서 재현 실행을 요청하지 않는다.

## 중요한 불일치 또는 약점 — 정확히 3건

| 불일치·약점 | 영향을 받는 주장 | 다음 조사와 원자료 | 판단을 뒤집을 관측 |
|---|---|---|---|
| A02 .02 규약과 C01/C02/C03의 측정 대상 차이; 특정 연구→#10579 선택 인과 불명 | 모든 화면에서 같은 JND, 새 GMA의 지각 우월성, 원거리 원리의 실제 편집 영향 | [B02 공식 기록](https://github.com/w3c/csswg-drafts/issues/10579#issuecomment-3200859856) 발언 전후 및 [C01](https://bottosson.github.io/posts/oklab/) 인용 계보, [C02 p13](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/6/1/art00003) 원 인용 연구. 특정 ΔEOK .02 관찰자/자극/표준 화면 논문 찾기 | 날짜가 고정된 설계자 발언이 직접 실험과 선택 변경을 연결하거나 동일 조건에서 검출곡선이 .02를 지지/반박 |
| 비용 비교 조건과 정확도 목표 불일치: PR36 반환 경계 보정, PR44 fold/cache, A03→A02 EdgeSeeker 저자명 | 가장 빠른 단일 solver, 구현 동일성, LUT 대비 품질 판단 | [PR36](https://github.com/color-js/apps/pull/36), [PR44](https://github.com/color-js/apps/pull/44), [A03 diff](https://github.com/w3c/csswg-drafts/commit/f5642b931d905128daa075fdfeba6c9e74475b5a), A02 EdgeSeeker reference path history; 같은 target, input, return space, cache, hardware 명시 자료 | 공정한 같은 조건의 로그가 순위를 바꾸거나 저자/구현 계보의 정확한 정정 commit이 발견 |
| 사진/인쇄 workflow는 실제이나 측색·시각 검증 없음; 청록 별도 수치 및 영상 근거 부족 | 단색 결과가 연속 이미지·인쇄에 그대로 적용된다는 주장 | [ICC WP40 Fig6](https://archive.color.org/files/WP40-Black_Point_Compensation_2010-07-27.pdf), [Blurb](https://support.blurb.com/hc/en-us/articles/360027277391-Preparing-color-images-for-Adobe-InDesign-or-Blurb-s-PDF-Uploader-workflows), [darktable](https://docs.darktable.org/usermanual/5.6/en/module-reference/processing-modules/filmic-rgb/), 공개 프로필/실제 측색 시편·이미지 평가와 청록 입력 찾기 | 동일 입력·프로필·시청 조건에서 이웃 detail/검은점 보존이 CSS 단색 목표만으로 충분하거나 실패한 실제 관측 |
