# AF-RES-099 · 입력과 판정 기준

Stack Overflow 79393445의 2025-01-28 최초판은 “I need to convert a Latex document containing Tikz pictures to HTML.”이라고 요청한다. 이어 원 명령과 그림이 빠진 HTML을 보여 준다. **C1은 HTML에서 원 그림을 읽을 수 있는가**다. 그림 뒤에도 본문이 검색 가능한 글로 남는지, 한 파일을 오프라인으로 열 수 있는지는 이 실험에서 추가로 측정한다. 당시 Pandoc·diagram·TeX 판, 이미지 형식·접근성·HTML 안의 벡터 텍스트 선택성·사용 가능한 도구의 제한은 공개 요청에 명시되어 있지 않다. [질문 최초판](https://stackoverflow.com/revisions/79393445/1) · [GUID 원문](https://stackoverflow.com/revisions/5938869D-E61B-410C-97F5-035731293446/view-source)

| 경로 | 재현할 약속 | 판정 범위 |
| --- | --- | --- |
| A | 원 질문의 Pandoc 명령과 LaTeX 입력. 필터는 연구용 diagram 023b317… 고정 | HTML 그림과 별도로 기본 LaTeX reader AST, 실제 필터의 CodeBlock 접점, 지원 입력 양성 대조 |
| B | AF-RES-096의 수정 없는 봉인 Lua, Pandoc 3.6의 latex+raw_tex → html5 및 embed-resources | TeX format/클래스 → PDF → pdf2svg → SVG → HTML 이미지와 본문. 임시 출력은 외부 계측으로 포착되면 원 출력, 별도 재실행하면 재생산품 |
| C | 공개 답의 `mutool draw -oout.svg aff2748b-266e-48f5-b2f7-7547936bb6aa.pdf` | 원 TeX로 만든 연구 PDF를 같은 이름으로 사용, 답의 독립 페이지 SVG 판정 |
| C+ | 연구자가 C의 SVG를 별도의 HTML 이미지로 배치 | 외부 SVG 유무, 내장 비교, HTML 본문 텍스트를 각각 따로 확인 |

최초 답은 웹에서 컴파일된 PDF를 입력으로 설명하며 MuPDF의 SVG 명령과 화면을 제시한다. 약 7분 뒤 수정판은 왕복 변환의 비효율과 다른 HTML에 넣을 수 있다는 설명을 덧붙인다. 공개 답에서 통합에 사용한 HTML 파일·코드, PDF 바이트, 판은 공개되지 않았다. [최초 답](https://stackoverflow.com/revisions/04B193AD-FEB3-4D6A-9618-B08ADC4315FF/view-source) · [수정판](https://stackoverflow.com/revisions/073D223B-CBA7-45F6-AEB4-9A59CA3BC841/view-source)

## 그림 생성 전에 고정한 채점표

네 상태는 왼쪽부터 `q₁, q₂, q₃, q₄`다. `q₁`은 초기·수락, `q₄`는 수락이다. `q₁` 왼쪽에는 라벨 없는 시작 화살표가 들어온다. 수락 이중원 2개와 초기 화살표는 아래 8개 전이와 별도다. TeX의 `->`와 `>=stealth'`는 방향 판독의 근거다.

| ID | 출발 → 도착 | 라벨 | 원 입력의 배치 단서 |
| --- | --- | --- | --- |
| E1 | q₁ → q₁ | a | 위 자기 루프 |
| E2 | q₁ → q₂ | b | 직선, 위 라벨 |
| E3 | q₂ → q₃ | a | 직선, 위 라벨 |
| E4 | q₂ → q₄ | b | 아래로 굽음, 아래 라벨 |
| E5 | q₃ → q₂ | a | 위로 굽음, 위 라벨 |
| E6 | q₃ → q₁ | b | 아래로 굽음, 위쪽 배치 옵션 |
| E7 | q₄ → q₄ | b | 위 자기 루프 |
| E8 | q₄ → q₃ | a | 왼쪽 직선, 위 라벨 |

판독자는 각 상태의 기호와 각 전이의 화살촉 위치·출발선·해당 라벨을 대조한다. 겹치는 선에서는 PDF를 기준으로 경로와 화살촉을 따라간다. E1/E7은 방향이 표시된 자기 루프여야 한다. 선의 픽셀 위치, 페이지 여백, 확대율은 보존 조건에 포함하지 않는다. 요소가 안 보이면 누락, 어느 전이인지 확정할 수 없으면 불명으로 기록한다. C1의 분모는 HTML 자리다. C 두 자리는 독립 SVG의 충족을 보고하고 C+는 별도 HTML 관측으로 둔다.

기대 순서는 본문 `The following is a TIKZ picture.` → 원 그림 → 본문 `The above is a TIKZ picture.`다. PDF 원문의 문장은 그림 옆 인라인에 배치될 수 있다. PDF/SVG 페이지에서 문장이 보이는 것과 HTML DOM의 두 문단을 검색할 수 있는 것을 각각 판정한다. 문자 윤곽선과 글리프 참조도 사람이 읽을 수 있으면 그림 요소 점수에 산입한다. 단일 HTML 여부는 상대 외부 SVG를 제거한 새 경로, 오프라인 브라우저의 리소스 로드와 실제 화면으로 확인한다.

## 준비 조건과 실패 위치

1. 원 코드 블록 SHA-256, 두 Lua 경로의 고정 신원 및 Pandoc 3.6 공식 바이너리 SHA-256을 실행 전에 확인한다. 비교 대상 A·B·C는 모두 같은 TeX 바이트다.
2. 각 반복은 새 작업 디렉터리, 임시 디렉터리 및 캐시를 사용한다. 공통으로 준비한 TeX format·패키지는 읽기 전용 입력으로 공유할 수 있다. 브라우저는 새 컨텍스트에서 연다.
3. 별도 양성 대조에서 작은 standalone TeX, PDF, SVG 파일, 브라우저 그림을 연결한다. A는 지원하는 TikZ 클래스의 CodeBlock도 별도로 사용한다.
4. 실패 위치는 reader 입력/형식, 필터 로드/콜백/대상 선택, TeX format·클래스·엔진, PDF→SVG 변환, HTML 표기/자원 로드, 열린 결과에서의 의미 손실이다. 실행 종료 0과 이미지 존재는 각각 단독 성공 조건이 아니다.
5. 그림 없는 원문 변형, 다른 그림이 렌더된 HTML, 외부 SVG가 없는 별도 디렉터리, 필수 변환 프로그램의 한 실행 경계 차단을 별도 대조로 둔다. 현재 환경의 최초 실패를 교정 후 결과와 함께 보존한다.

선행 AF-RES-095의 최종 산출물 판독·음성 대조만 가져온다. AF-RES-096의 P4 원 입력, diagram 핀, 바이너리 지문과 봉인 Lua를 실행 입력으로 가져온다. 선행 조사 전체를 재평가하지 않는다. [095 판독·대조](https://github.com/laadkke-arch/agentflow-open/blob/55eb703075163a84b38fdc7eb577f66207e9980e/docs/workstreams/research/AF-RES-095/evidence/probes/README.md) · [096 P4 실행](https://github.com/laadkke-arch/agentflow-open/blob/1d399f630930d2763459e16509c5224b0cded9a0/docs/workstreams/research/AF-RES-096/evidence/post-pandoc/report.md)
