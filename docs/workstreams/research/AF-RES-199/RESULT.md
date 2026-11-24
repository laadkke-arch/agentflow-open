# AF-RES-199 — HDR 원전과 조작 대조 (핵심 초안)

| 설계 조작·사용 목적 | 2002/2005 원리·식과 원문 URL | 저자의 직접 언급 | 추가로 가른 선택 | 미확인 |
|---|---|---|---|---|
| 노출/밝기 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf#page=3) §3.1 Eq1–4: 키 a로 로그평균 휘도 스케일; [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=4) §3 Eq2–5: f=exp(-f'), k로 m 추정 | A01 Zone System의 노출 개념; A02 intensity와 contrast 분리 | key .18은 f' 0과 같은 물리량 아님 | A07 Eq1 기하평균 확인; A08 정오표 전사 원본 미확인 |
| 공간 국소 대비 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf#page=4) §3.2 Eq5–9: 주변 convolution, 크기 선택; [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=5) p17: pixel/global 보간 | A01 Adams 및 Blommaert–Martens; A02 비용 때문에 공간 평균 대신 보간, §4 별도 국소 확장 | 반경/halo 문제라면 2002 공간 알고리즘; 전역/픽셀 적응 가중치라면 2005 | Eq8 부등호 및 구현 스케일 convention; 실제 속도/화질 |
| 색/빛 적응 | [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf#page=5) Eq6–7 및 혼합식; A01 §4 luminance | A02 von Kries 스타일 및 강한 색조 제거; A01 휘도 조작 | 채널별 적응 원하면 2005; 2002 소비자는 단일 XYZ 배율 | 색순응/선호 측정 및 출력 기기 |
| 임의 지역의 작가 의도 | [D01](https://www.cincinnatiartmuseum.org/media/kjvk10uz/24_discoveringanseladams_large-print-labels-v2.pdf) Moonrise labels; A01 §3.2 | 기록기관: proof와 printing instruction; A01 자동 scale | semantic mask/manual dodge & burn 별도 설계 | 원지시 facsimile 실제 노출량 판독 못함 |

| 구현·고정판·옵션 | 실제 연산·기본값 | 대응 원문/코드 URL·위치 | 반대 판독·예외 | 관찰/추론 |
|---|---|---|---|---|
| P1 pfstmo key | .18; global white term | [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html) OPTIONS; [B07](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/tmo_reinhard02.cpp#L383-L425), A01 Eq1–4 | A01 Eq1 사본 표기 vs 코드; 출력 회색 .18 보장 아님 | 정적 코드 |
| P2 pfstmo scales/phi | off; phi1; 8 scales, 1..43 | [B07](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/tmo_reinhard02.cpp#L329-L362), [B08](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/pfstmo_reinhard02.cpp#L72-L91), A01 Eq5–9 | 논문 phi8; manual >=0 vs wrapper >0; Eq8 < vs code > | 정적 코드, 실측 없음 |
| P3 pfstmo 색/빛 | 없음; X/Y/Z 공통 L/Y | [B08](https://github.com/flyingfalling/pfstools/blob/7cd588d9ee56fee3190c82916a9fd9c9971d6a3b/src/tmo/reinhard02/pfstmo_reinhard02.cpp#L158-L188) | gamma 외부; temporal average smoothing ≠ cone adaptation | 정적 코드 |
| O1 OpenCV 4.10.0 intensity | 0; gamma1; m 자동 | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L219-L256), [B04](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/include/opencv2/photo.hpp#L389-L419), A02 Eq2–5 Fig7 | intensity member exp 변환, m setter 없음 | 정적 코드; [C07](https://github.com/opencv/opencv/pull/30498) 후속 수정에서 당사자 확인; 고정판 반복 실행 미확인 |
| O2 light_adapt | 1 pixel, 0 global | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L227-L244), A02 p17 blend | 지역 이웃/반경 없음; paper Fig9 확장은 별도 | 정적 코드 |
| O3 color_adapt | 0 shared luminance vs 1 independent | [B03](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/src/tonemap.cpp#L231-L244), A02 Eq6 | 색 포화/물리 보정과 다름 | 정적 코드 |

| 요청 | 근접 문서만 본 답 | 추가 원전과 달라진 점 | 추천 링크·범위 | 틀리는 사례 |
|---|---|---|---|---|
| 인화 원리 | B01 --scales | 공간 scale vs pixel adaptation | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf) §2,3.2; [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html) | OpenCV 이름만 보고 암실 원리 연결 |
| API 조작 | B01/B04 구문·default 충분 | f', a, c vs key 및 m 부재; call 선택은 유지 | [B01](https://manpages.debian.org/trixie/pfstmo/pfstmo_reinhard02.1.en.html), [B04](https://github.com/opencv/opencv/blob/4.10.0/modules/photo/include/opencv2/photo.hpp#L389-L419) | paper m 범위를 API에 노출했다고 판단 |
| 결과 관찰 | B01 Memorial 예제 명령; generic OpenCV HDR example | Fig8/9 vs Fig2/8/9, 서로 다른 조건 | [A01](https://w3.impa.br/~lvelho/ip02/papers/reinhard/tonemap.pdf), [A02](https://www.cs.ucf.edu/~ceh/Publications/Papers/Rendering/IEEETVCG04ReinhardDevlin.pdf), [C02](https://www.pauldebevec.com/Research/HDR/) | 입력 동일해 보여도 버전/파라미터 통제 안 됨 |
 
④ 보정 기록: 종전 Eq1 원식/코드 불일치만 기록했으나 A07 저자 후속 논문 Eq1 및 A09 저자 호스트 사본으로 기하평균 의도 확인. A08 정오표 전사는 원본 미확인으로 제외. A02 [14] 연결은 A07 서지와 확인(연도 표기 차이). 종전 intensity 반복 문제는 추론이었으나 C07 구현자 PR 본문·diff로 후속판 수정 확인; 4.10.0 자체 실행은 여전히 미확인. C05 갤러리 결과 목록, C08 고정 golden 비교 규칙을 추가하되 실제 결과 픽셀/실행 관찰로 승격하지 않음. C06 독립 비교의 장면별 역전은 고정 구현 직접성 부족으로 산입하지 않음.
