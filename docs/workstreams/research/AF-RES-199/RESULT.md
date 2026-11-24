# AF-RES-199 — HDR 원전과 조작 대조 — PARTIAL

| 설계 조작·사용 목적 | 2002/2005 원리·식과 원문 URL | 저자의 직접 언급 | 추가로 가른 선택 | 미확인 |
|---|---|---|---|---|
| 노출/밝기 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf#page=3) §3.1 Eq1–4: 키 a로 로그평균 휘도 스케일; [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=4) §3 Eq2–5: f=exp(-f'), k로 m 추정 | A01 Zone System의 노출 개념; A02 intensity와 contrast 분리 | key .18은 f' 0과 같은 물리량 아님 | A07 Eq1 기하평균 확인; A08 정오표 전사 원본 미확인 |
| 공간 국소 대비 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf#page=4) §3.2 Eq5–9: 주변 convolution, 크기 선택; [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=5) p17: pixel/global 보간 | A01 Adams 및 Blommaert–Martens; A02 비용 때문에 공간 평균 대신 보간, §4 별도 국소 확장 | 반경/halo 문제라면 2002 공간 알고리즘; 전역/픽셀 적응 가중치라면 2005 | Eq8 부등호 및 구현 스케일 convention; 실제 속도/화질 |
| 색/빛 적응 | [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=5) Eq6–7 및 혼합식; A01 §4 luminance | A02 von Kries 스타일 및 강한 색조 제거; A01 휘도 조작 | 채널별 적응 원하면 2005; 2002 소비자는 단일 XYZ 배율 | 색순응/선호 측정 및 출력 기기 |
| 임의 지역의 작가 의도 | [D01](https://www.cincinnatiartmuseum.org/media/kjvk10uz/24_discoveringanseladams_large-print-labels-v2.pdf) Moonrise labels; A01 §3.2 | 기록기관: proof와 printing instruction; A01 자동 scale | semantic mask/manual dodge & burn 별도 설계 | 원지시 facsimile 실제 노출량 판독 못함 |

| 구현·고정판·옵션 | 실제 연산·기본값 | 대응 원문/코드 URL·위치 | 반대 판독·예외 | 관찰/추론 |
|---|---|---|---|---|
| P1 pfstmo key | .18; global white term | [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html) OPTIONS; [B07](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/tmo_reinhard02.cpp#L383-L425), A01 Eq1–4 | A01 Eq1 사본 표기 vs 코드; [A07](https://www.researchgate.net/publication/255682296_Parameter_Estimation_for_Photographic_Tone_Reproduction) Eq1; 출력 회색 .18 보장 아님 | 정적 코드 |
| P2 pfstmo scales/phi | off; phi1; 8 scales, 1..43 | [B07](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/tmo_reinhard02.cpp#L329-L362), [B08](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/pfstmo_reinhard02.cpp#L72-L91), A01 Eq5–9 | 논문 phi8; manual >=0 vs wrapper >0; Eq8 < vs code >; 첫 초과 index 사용 | 정적 코드, 실측 없음 |
| P3 pfstmo 색/빛 | 없음; X/Y/Z 공통 L/Y | [B08](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/pfstmo_reinhard02.cpp#L158-L188) | gamma 외부; temporal average smoothing ≠ cone adaptation | 정적 코드 |
| O1 OpenCV 4.10.0 intensity | 0; gamma1; m 자동 | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L219-L256), [B04](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/include/opencv2/photo.hpp#L389-L419), A02 Eq2–5 Fig7 | intensity member exp 변환, m setter 없음 | 정적 코드; [C07](https://github.com/opencv/opencv/pull/30498) 후속 수정에서 당사자 확인; 고정판 반복 실행 미확인 |
| O2 light_adapt | 1 pixel, 0 global | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L227-L244), A02 p17 blend | 지역 이웃/반경 없음; paper Fig9 확장은 별도 | 정적 코드 |
| O3 color_adapt | 0 shared luminance vs 1 independent | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L231-L244), A02 Eq6 | 색 포화/물리 보정과 다름 | 정적 코드 |

| 요청 | 근접 문서만 본 답 | 추가 원전과 달라진 점 | 추천 링크·범위 | 틀리는 사례 |
|---|---|---|---|---|
| 인화 원리 | B01 --scales | 공간 scale vs pixel adaptation | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf) §2,3.2; [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html) | OpenCV 이름만 보고 암실 원리 연결 |
| API 조작 | B01/B04 구문·default 충분 | f', a, c vs key 및 m 부재; call 선택은 유지 | [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html), [B04](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/include/opencv2/photo.hpp#L389-L419) | paper m 범위를 API에 노출했다고 판단 |
| 결과 관찰 | B01 Memorial 예제 명령; generic OpenCV HDR example | Fig8/9 vs Fig2/8/9, 서로 다른 조건; C05 결과 목록, C08 비교 테스트 규칙 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf), [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf), [C02](https://www.pauldebevec.com/Research/HDR/), [C05](https://pfstools.sourceforge.net/tmo_gallery/mpi_office.html), [C08](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/test/test_hdr.cpp#L88-L119) | 입력 동일해 보여도 버전/파라미터 통제 안 됨 |
 
④ 보정 기록: 종전 Eq1 원식/코드 불일치만 기록했으나 A07 저자 후속 논문 Eq1 및 A09 저자 호스트 사본으로 기하평균 의도 확인. A08 정오표 전사는 원본 미확인으로 제외. A02 [14] 연결은 A07 서지와 확인(연도 표기 차이). 종전 intensity 반복 문제는 추론이었으나 C07 구현자 PR 본문·diff로 후속판 수정 확인; 4.10.0 자체 실행은 여전히 미확인. C05 갤러리 결과 목록, C08 고정 golden 비교 규칙을 추가하되 실제 결과 픽셀/실행 관찰로 승격하지 않음. C06 독립 비교의 장면별 역전은 고정 구현 직접성 부족으로 산입하지 않음.


## 판정 범위

**핵심 판별: 성립. 자료별 하한: 미달(PARTIAL).** 이름/저자 및 HDR→LDR 목적이 겹쳐도 독립 원리·연산이다. 직접 읽어 산입한 고유 자료 22개(A 3/4, B 9/7, C 4/5, D 4/4, E 2/2); A·C 각각 1개 부족, B 초과로 상쇄하지 않는다. B07/B08은 명확한 고정 SHA의 재구현 파일이나 Debian 2.2.0-9의 정확한 소스 동일성은 확인하지 못했다. C05는 갤러리 원해설 목록, C08은 golden 비교 규칙, C07은 후속 수정 설명이지 새 출력 관측이 아니다. 고정판 본체 실행/실측/독립 평가 없음. 질문별 세부 근거는 sources.jsonl과 lineage.csv, 조작 6자리 operators.csv, 카드 3자리 cards.csv. 아래 링크의 식·코드에서 관측한 것과 설계 추론을 분리한다.

### Q1. 2002: 암실 인화의 계산적 치환

- [A01 §2, §3.1–3.2 Fig5,8,9](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf) (저자 호스트 동일 사본 [A09](https://jamesferwerda.com/wp-content/uploads/2015/06/j10_reinhard02_sig.pdf)): Adams의 Zone System, 장면의 key 및 인화의 국소 조정을 디지털 휘도 조절의 출발점으로 직접 언급. 암실에서 인화지의 일부를 가리면 적은 빛을 받아 밝아지는 dodge, 더 오래 노출하면 어두워지는 burn. 장면 key/카메라 노출, 인화지의 지역별 노출, 표시 픽셀 휘도는 서로 다른 물리 단계다. 디지털 알고리즘에서 인화 노출 시간을 그대로 계산하거나 작가가 선택한 영역을 재현하는 것은 아니다.
- Eq1 의도는 Lbar=exp(Σ log(δ+Lw)/N), Eq2 L=a Lw/Lbar (일반 key .18); Eq3 Ld=L/(1+L), Eq4 Ld=L(1+L/Lwhite²)/(1+L). white는 포화 처리/흰점 설정; .18은 스케일된 휘도의 key이지 최종 화면 회색 보장값/카메라 stop이 아니다. 두 PDF 사본의 Eq1은 1/N이 exp 밖에 보이는 인쇄 표기; [A07 §1 Eq1](https://www.researchgate.net/publication/255682296_Parameter_Estimation_for_Photographic_Tone_Reproduction)와 B07 L383–391이 평균을 지수 안에 넣는다. [A08 L166–173](https://studylib.net/doc/14957425/siggraph-2002-slides--ppt-) 발표자료 전사도 이 정오를 설명하나 원본 PPT 미확인으로 산입 제외. Eq1을 문자 그대로 구현하라는 링크는 보류한다.
- Eq5–7 Gaussian center/surround 및 정규화된 차이 응답 V(x,y,s); 8 스케일, 1–43 px, 논문 φ=8 및 ε=.05. Eq8의 인쇄된 < 비교와 B07 L353의 첫 > 비교는 정확히 동일한 표기/인덱스가 아님. B07은 첫 초과 **그 index**를 분모 V1에 넣음; 초과가 없으면 range-1. Gaussian pair(s, next larger scale)의 해석상 경계 탐색이라는 공통 원리까지 대응하되, 인덱스별 exact equality를 확정하지 않음. Eq9 Ld=L/(1+V1); 공간적으로 다른 분모가 원리. 저자가 시각 중심-주변 연구도 명시 차용하므로 2002=오직 암실이라는 구분은 부정확.
- Fig8 두 장면의 대비 범위 차이(정원 약 6 zones, 책 이미지 약 15 zones), Fig9 halo/규모 비교는 **저자의 예시**이다. 국소 방법이 항상 필요하다는 결론은 틀림. A07 §2 Eq4–6은 자동 key/white/국소 선택(극단 1% 제외, 11 zones 기준)을 추가하고 §3는 선호에 따른 수동 튜닝 여지를 둔다. A07 알고리즘을 pfstmo 기본 .18이 자동 채택한다고 말할 근거는 없다.

### Q2. 2005: 광수용체 반응의 적응값, 대비와 밝기를 분리

- [A02 pp13–18 §2–3 Eq1–7, Fig2,3,4,7,8](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf): 반포화 광수용체 응답을 단순 모델로 차용하고, display용 I_d=I/(I+(f I_a)^m) 형태로 구성. 생리적인 반포화값을 공학적으로 적응량과 지수에 결합; 시간 경과의 실제 망막 동역학을 시뮬레이션했다는 주장은 아님. f=exp(-f'), 기본 f'=0→1. m=.3+.7 k^1.4, k=(log_max-log_avg)/(log_max-log_min). 2002의 a=.18 및 A07의 자동 key 추정식과는 별개 양; A02 참고문헌 [14]는 Reinhard의 Parameter Estimation 논문을 참조(연도 표기 2003과 JGT 2002 권호 차이, DOI 동일 서지 확인), 장면의 key를 추정한다는 연결이지 매개변수 변환 동일성은 아님.
- I_a = a[c I+(1-c)L]+(1-a)[c I_mean+(1-c)L_mean]. I는 채널, L은 휘도; 논문 Eq3 휘도 가중치 .2125/.7154/.0721, a(빛)=1 픽셀값/0 전역 평균, c(색)=1 채널별/0 휘도 공유. a의 local은 픽셀의 값이라는 뜻, **주변 크기/이웃 픽셀은 계산하지 않는다.** c=0이라도 채널별 비선형 분수의 분자가 다르므로 색채 완전 보존을 보장하지 않는다. Fig2 서로 다른 a,c에 따른 대비와 색 차이, Fig3 .2 간격의 가중치 변화는 설정 변화 비교, 실제 망막 적응시간 측정 아님. Fig8 수동 m 예 .262/.462/.662와 f' 변화: 논문 일반 범위와 예제 값이 완전히 일치한다고 가정하지 않는다.
- 반례: [A02 §4 Fig9 p18](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=6)는 spatial bilateral/local extension도 시험했다. 따라서 2005 논문 자체를 무조건 비공간이라고 분류하면 틀린다. 다만 고정 OpenCV 구현에는 그 선택적 국소 필터가 없다. 저자는 §5/결론에서 출력의 시각적 매력을 자기 의견으로 서술; 사람 평가의 우위 또는 새 실측으로 승격하지 않음.

### Q3. pfstmo reinhard02의 배포·선택

- [B15 upstream news](https://pfstools.sourceforge.net/) 2021-08-12 2.2.0 공개; [B01 Debian trixie](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html) 2.2.0-9; [B02 Debian patches](https://sources.debian.org/patches/pfstools/2.2.0-9/)에서 해당 소스 직접 수정 목록 없음. [B07](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/tmo_reinhard02.cpp) 파일 머리에 원저자 Utah 코드 출처 및 PFS port 표시. [B08](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/pfstmo_reinhard02.cpp) 별도 wrapper. 정확한 재구현 SHA=7cd588d9ee56fee3190c82916a9fd9c9971d6a3b; [B09 CMake](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/CMakeLists.txt#L6-L9) 2.1.0 vs commit 설명 2.2.0, 따라서 official 2.2.0-9 byte identity 미확인. B12–14, B17 직접 실패. 원저자 CD-ROM 및 MPI 원 페이지도 실패(A10/A14/C01). 근거는 **공식 문서와 고정 재구현**의 조작 대응으로 한정.
- B08 L73–91,105–134: key .18, phi 1, num8, low1 high43, scales=false, temporal=false. key=0 거부, 1 허용; phi=0 거부(문서 허용 하한과 상충). B07 L383–425 geometric mean δ=.00001, L329–362 전역 white 항/국소 분모 분기. paper 기본 φ=8을 CLI 기본값으로 가져오면 틀림. --scales 없이 phi만 바꾸면 국소 분기는 여전히 off. --temporal-coherent의 통계 평활은 동영상 연속성 선택이지 시각 순응 모델 구현 주장이 아니다. B08 L161–182에서 XYZ에 같은 Lnew/Y 배율; channel adaptation/whitepoint 전용 인자 없음. Y=0 나눗셈 및 range 경계 동작 실행 미확인.
- B01 예제: memorial.hdr→pfstmo_reinhard02→pfsgamma 2.2→PNG, local 비교는 -s 추가. [C02 Debevec 원입력](https://www.pauldebevec.com/Research/HDR/)은 원 Radiance/EXR 자료 제공, 실제 binary 미열람. [C05 office 결과 목록](https://pfstools.sourceforge.net/tmo_gallery/mpi_office.html) 비교 링크는 같은 장면 이름뿐이며 설정/픽셀/판 미확인. 한 페이지가 원리·실행·결과 모두를 입증하지 않음.

### Q4. OpenCV 4.10.0 고정 소비자

- [B04 photo.hpp L389–419](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/include/opencv2/photo.hpp#L389-L419): global tone mapping, light/color adaptation, RD05 직접 인용; [B05 bibliography L898–907](https://github.com/opencv/opencv/blob/4.10.0/doc/opencv.bib#L898-L907) RD05=Reinhard & Devlin 2005. [B06 release](https://api.github.com/repos/opencv/opencv/releases/tags/4.10.0) 고정 release 정보. 2002 paper는 적합한 직접 API 원전 아님. 함수 createTonemapReinhard(gamma=1,intensity=0,light_adapt=1,color_adapt=0), intensity [-8,8], 가중치 [0,1]는 API 문서 범위; setter 강제 검증 아님(B03 L253–263). 생성자 구현의 형식 이름 contrast/sigma_color/sigma_space(L290–293)는 실제 공개 API의 intensity/light/color 순으로 전달되므로 이름만으로 contrast나 공간 sigma라고 읽으면 틀림.
- [B03 L197–293](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L197-L293): 217–218 최초 min-max normalization; 220–231 COLOR_RGB2GRAY, log clamp 및 key→map_key=m; 232 f=exp(-intensity); 240–244 위 Ia 혼합, per-channel I/(I+(fIa)^m); 249–250 gamma 및 두 번째 정규화. A02 Fig7과 대응은 핵심 수식, 전체 코드 동치가 아니다. 휘도 계수와 정규화 경계도 다름. 헤더/멤버에 m setter/국소 반경 없음. intensity를 미리 exp해서 넣으면 이중 변환이 되어 의도와 달라짐.
- 중요한 버전 반례: B03 L232는 멤버 자체를 exp(-intensity)로 바꾸며 getter L256 및 serialize L270도 그 멤버를 사용. 동일 객체의 두 번째 호출은 초깃값 0→1→exp(-1)로 바뀔 것으로 추론. [C07 PR #30498](https://github.com/opencv/opencv/pull/30498) 2026-10-29 merged, 구현자가 반복 호출/설정 저장 오류를 명시하고 local intensity_scale로 수정. [C09](https://github.com/opencv/opencv/pull/30719) 5.x 동일 port, 독립 사건 아님. 이 확인은 4.10.0에 수정이 적용됐다는 뜻이 아니다. 동일 object 사용 시 재설정/새 instance를 검토하되, 실제 output 차이와 균일 입력 log_max=log_min에서의 결과는 실행 미확인.
- [C08 fixed test L88–119](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/test/test_hdr.cpp#L88-L119): image.hdr→gamma2.2, 기본 adaptation→8bit→reinhard.png와 max absolute code value difference 3 기준. 4.10.0 test는 한 번 호출. 별도 실제 기대 이미지 binary/실행 결과는 미확인. C03 공식 HDR tutorial의 createTonemap(2.2f)은 generic, 이름/과제 유사성만으로 Reinhard 결과라 할 수 없음.

### Q5. 가까운 구현 문서 대비 원전의 증분

SCOPE 선등록 H0: 동일 성과 같은 축소 결과이면 key=intensity, scales=light_adapt, color/light 기능 동일, local 의미도 동일. 근접 문서 B01/B04/B10을 먼저 읽고 위 조작 예측을 했다(완전 blind 아님: brief와 기존 지식이 원리 구분을 이미 노출). 판별:
- P1: key로 midtone/밝기라는 예상 유지, A01 Eq1–4/A07로 값의 의미와 자동 추정/흰점 분리. O1: intensity로 밝기 유지, A02 Eq5와 B03의 exp/member side effect, m 미노출로 같은 키 전이 기각.
- P2: --scales가 공간 local, 기본 global이라는 예상 유지, A01 Eq5–9/halo 및 실제 부등호로 경계·scale 제약 구체화. O2: B04만으로 pixel/global 혼합 선택 완료; A02에서 별도 spatial local variant의 구별이 새로 중요. local 단어만 일치한다는 예상 기각.
- P3: B01 인자에 채널/빛 적응 없음(미확인 가설), B08 공통 XYZ 배율로 확인. O3: B04 independent/shared channel 가중치 선택 그대로, A02의 생리 차용과 c=0이라도 색상 완전 보존이 아니라는 한계 확인.
- 대조: 정확한 API 호출만 원하는 요청에는 원전 추가가 결정 자체를 바꾸지 않는다. B01 --key/--scales, B04 light/color defaults로 충분(정확 실행은 별도). 원전에서 소개한 m 직접 조정, Fig9 spatial adaptive gain을 OpenCV public API 기능으로 자동 반환하면 오히려 잘못된 안내. [C04 pfstmo_reinhard05](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard05.1.en.html)는 RD05의 다른 CLI로 정확한 이름 분리 사례이나 예제 -s가 선언과 맞지 않음; 이번 고정 소비자 제외.

### Q6. 사진 인화자의 지역 의도 vs 자동 연산

- [D01 Cincinnati Art Museum 2024 전시 라벨 L560–571](https://www.cincinnatiartmuseum.org/media/kjvk10uz/24_discoveringanseladams_large-print-labels-v2.pdf) Moonrise, Hernandez, New Mexico 1941 negative에 대해 proof print 및 printing instructions facsimiles 라벨 식별. 실제 인화 지시가 작품에 존재하나 여기서 원 작업자의 손글씨별 초/조리개/마스크를 직접 판독하지 못했다.
- [D02 MoMA 467.1964](https://www.moma.org/collection/works/53904) 하나의 negative에서 대비가 강화되는 다른 인화; [D03 Met 1979.585.4](https://www.metmuseum.org/art/collection/search/262580) 1941/printed ca.1978 (온라인 이미지 없음); [D04 UMMA 1988/1.87](https://umma.umich.edu/objects/moonrise-hernandez-new-mexico-1988-1-87/) 1941/printed 1981, 더 많이 노출한 하늘의 변화에 관한 작가 설명 인용. D04의 250 candles/ft²는 촬영 노출 결정에 쓰인 달의 휘도이지 암실 print 노출량/초가 아니다. **D 4개 자료, 단일 negative 사례 1개**; 별도 네 실험으로 합산 금지.
- 인화자는 작품 내 특정 하늘/구름/지면의 의도를 바꾼다. 2002 자동 local은 명암/스케일을 따르므로 의미적 영역 선택·개별 마스킹·버전별 작가 의도를 보장하지 않는다. 반대로 모든 인화가 반드시 수동이어야 한다는 결론도 부당: A07은 통계적 자동 시작점에 유용하고 편집자는 수정할 수 있다. 2005 모델 논문 저자는 생리와 공학적 조작의 타협, 라이브러리 구현자는 옵션/정규화/버전 회귀, HDR 편집자는 출력 매체/시각 의도 및 작업속도라는 다른 목적. 동일 negative의 여러 print가 하나의 객관적 정답 영상이 아님을 보여주나 자동 알고리즘 품질 순위를 측정한 사건은 아니다.

### Q7. 탐색기 반환 기준

- R1 인화 원리: A01 §2–3.2 한 링크로 논문 차용 설명 충분; 개발자 구현은 B01+B07, 예술가의 지정 지역 작업 의도는 D01+D02 추가. O2 light_adapt를 dodge mask/반경으로 연결 금지.
- R2 API 조작: pfstmo B01 또는 OpenCV B04 단독으로 기본 호출 선택 가능; 2005 m 직접 knob/반복 호출 안정성 요구가 들어오면 B03+C07+A02를 더함. 자동 m와 사용자 key를 동일 값으로 변환하지 않음. 동일 프로그램 내 reinhard05와 reinhard02 이름까지 식별.
- R3 공개 결과 관찰: A01 Fig8/9 또는 A02 Fig2/8/9(해당 paper 내부 비교만); C02 원입력; C05 같은 scene 결과 링크(판/파라미터/출력 미검증), C08 고정 회귀 사양. 4.10.0 generic tutorial이나 논문의 미리보기만으로 실제 fixed output 증명 불가. 설정, 입력, display/gamma, 출력 원본을 일치시켜야 공정 비교 가능. 링크에 role, exact version, operation, applicability, limits, evidence type을 붙이는 후보 설계. 최종 DB/순위 채택 보류.

## 경쟁 설명과 조합 비용

- [E01 Durand & Dorsey 2002 §1–3](https://pages.cs.wisc.edu/~dyer/cs534/papers/Durand-Dorsey-Bilateral.pdf) bilateral 필터로 base/detail 분해하고 base 대비만 압축한다. 암실 영감도 언급하므로 그 영감 자체는 reinhard02 식의 독점 식별자가 아니다. 에지 보존 스케일과 비용/halo 절충이 필요한 경우 대안. [E02 Fattal et al. 2002 §1–3](https://web.tecgraf.puc-rio.br/~scuri/inf1378/pub/lischinski.pdf) gradient magnitude attenuation 및 Poisson reconstruction, 사실적 HVS 모델을 목표로 하지 않음. 국소 대비 요구가 동일해도 구조적 방법·비용 다름. 어느 대안의 4.10.0과 비교한 성능 수치 없음.
- [C06 independent paper §4 Fig3–6](https://www.jstage.jst.go.jp/article/transinf/E92.D/12/E92.D_12_2487/_pdf): 자체 수치 지표의 장면별 D/E 순서 역전(41.31/20.05 vs 13.49/22.24%, 해당 논문 P>75% 비율). 정확한 fixed consumer version 불명, 사람 선호/두 소비자의 우열 아님; 주표본 C 산입 제외. 결과 한 장과 저자 인용을 성능 근거로 자동 치환하지 않는다.
- 조합 후보: scene 통계 자동 초기값→전역 톤 커브→필요할 때 주변 대비/수동 mask→감마/출력. 공간 필터/피라미드 메모리·계산·halo 검토, 전역/pixel 방법은 공간 처리 생략 대신 영역의 의미/이웃 보존 한계. 독립된 두 nonlinear tone mapping을 연달아 적용하면 이미 압축한 대비를 다시 변형하고 clipping/색 변화가 생길 수 있어 무조건 조합 추천 금지. video는 별도 temporal 상태 검토; 정지영상 결과에서 시간 안정성 일반화하지 않음.
- 추가 분석(미실행): 동일 양의 다양한 RGB 픽셀 집합을 공간 재배열했을 때 fresh OpenCV instance 출력 역순열 일치(부동소수 오차 허용) 예측 vs pfstmo --scales 공간 반응 차이 예측. 균일 입력, Y=0, phi=0, repeat getter/reset, output gamma 및 input format 통제. 코드에서 추론한 반증 가능 가설이지 측정 결과가 아니다. HANDOFF에서 pinned 입력·명령 제시. 자체 점검만 수행; 독립 평가 없음.

| 불일치·약점 | 영향을 받는 주장 | 다음 조사·열 원자료 | 판정을 뒤집을 관측 |
|---|---|---|---|
| pfstmo 2.2.0-9 소스 byte identity 미확인(B09/B12–14); Eq8의 < vs 첫 > 인덱스; A 부속 1개 부족 | 2002 식과 배포 바이너리까지 정확히 동일하다는 주장 | [Debian 2.2.0-9](https://sources.debian.org/src/pfstools/2.2.0-9/), upstream 2.2.0 tarball, [Utah 원코드](https://www.cs.utah.edu/~reinhard/cdrom/source.html), 원본 저자 정오표 | exact release source의 local branch/threshold가 mirror와 다르거나 원저자판의 index convention이 동일성을 확인·기각 |
| C 1개 부족; C05 목록/C08 golden 사양만, 4.10.0 반복·경계 입력 실행 없음 | 동일 장면 결과 비교 및 광 적응·국소 대비 선택의 실제 출력/비용 | [MPI 원예제](https://resources.mpi-inf.mpg.de/tmo/reinhard02/index.html), [OpenCV extra fixed testdata](https://github.com/opencv/opencv_extra/tree/4.10.0), [C07](https://github.com/opencv/opencv/pull/30498), 원본 binary/설정/판 식별 | 같은 입력·gamma·설정으로 공간 재배열/반복 실행에서 예측과 다른 결과 또는 명확한 독립 결과 원해설 확보 |
| D01의 원지시 이미지/초별 영역 미판독, 같은 negative 1사례; near/original 순서 비블라인드 | 실제 인화 의도의 자동화 가능성 및 원전 추가로 선택이 갈리는 빈도, 사람 선호 | [D01](https://www.cincinnatiartmuseum.org/media/kjvk10uz/24_discoveringanseladams_large-print-labels-v2.pdf), [D04](https://umma.umich.edu/objects/moonrise-hernandez-new-mexico-1988-1-87/) 식별된 printing instructions/print 고해상도 원본, 별도 가림 비교 | 원지시에서 자동 규모 탐색만으로 의도가 충분히 재현됨을 입증하거나 blind near-vs-original 결정이 현재 해석과 달라짐 |
