## 표 1 · 요청, 원문, 자료집의 직접 적격

| 요청·층·언어 | 원 URL·판·원문 | 바꿀 대상·보존 조건 | 직접 적격 기능 | 판정 근거·미확인 |
| --- | --- | --- | ---: | --- |
| N-B1–3 · 자연 예정 · en/ko | Blender 공식 트래커, 첫 40건 미확인 | 미확인 | — | 생성 UTC·ID 순서를 입증할 응답이 없어 세 자리 공석 |
| N-K1–3 · 자연 예정 · en/ko | KDE Bugzilla, 첫 40건 미확인 | 미확인 | — | 개별 원문은 열렸으나 검색 범위의 순서와 경계가 미확인 |
| E-B1 · 탐색 · en/ko | 2023-02-03 공개 제안, “export solely the Glare Node Result as an exr file.” [작성자 L11–19](https://blender.community/c/rightclickselect/wrZ8/) | Glare만 EXR로 저장하고 다른 렌더 결과의 혼입 방지 | 0/24 | 24개에 Glare 파일 기록 조작이 확인되지 않음. 게시 시각과 최초 본문 미확인 |
| E-B2 · 탐색 · en/ko | Blender 4.2.2/4.0.2, “they appear fine in blender in the render window, but they do not save out properly.” [#128731 L65–87](https://projects.blender.org/blender/blender/issues/128731) | UV·Mist·Cryptomatte 패스 EXR 산출, 외부 앱에서 패스 내용 보존 | 0/24 | Cryptomatte의 EXR은 입력이다. 외부 앱이 읽은 파일은 미실행 |
| E-B3 · 탐색 · en/ko | Blender 4.3 Beta/4.2, “when a mask is viewed while an unconnected Double Edge Mask is present.” [#130134 L65–97](https://projects.blender.org/blender/blender/issues/130134) | Box Mask 표시, 연결하지 않은 노드가 있어도 안정적으로 미리 보기 | 0/24 | 생성 및 기본값 분기 2개는 일부. Viewer/Backdrop GUI 미실행 |
| E-K1 · 탐색 · en/ko | Krita 5.1.5, “It is similar to ‘new layer from visible’, but only works for the selected layer.” [#464692 L55–61](https://bugs.kde.org/show_bug.cgi?id=464692#c0) | 선택층을 합친 새 레이어 한 개, 원본과 비선택층 유지 | 0/24 | Clone·Group은 일부. 원본 유지 의도는 작성자가 설명한 복제→병합에서 추론 |
| E-K2 · 탐색 · en/ko | Windows 10 공개 설명, “The contents of the file layer should match the new scale of the image.” [#467257 L58–81](https://bugs.kde.org/show_bug.cgi?id=467257#c0) | 문서·출력 축소에 맞춰 PNG File Layer를 축소하고 전체 내용 보존 | 0/24 | File Layer 모드는 일부. 기존 파일의 모드와 Advanced Export 실행 미확인 |
| E-K3 · 탐색 · en/ko | Krita 5.1.5, “Image and transform mask to scale proportionally with the new size and keep the position within the canvas.” [#470110 L56–94](https://bugs.kde.org/show_bug.cgi?id=470110#c0) | File Layer와 변형 마스크를 비례 축소하고 캔버스 상대 위치 유지 | 0/24 | File Layer의 크기 이벤트는 일부. 변형 마스크 위치 보존·두 GUI 경로 미확인 |
| C-P1 · 구성 양성 · en/ko | Manual 5.3.0의 캐릭터·빛 효과 예. [Clone Layers L8–20](https://docs.krita.org/en/reference_manual/layers_and_masks/clone_layers.html#example-uses-of-clone-layers) | 자동 갱신하는 빛 효과 복제본, 원 도색 레이어를 계속 편집 | 1/24 | K-L01. 한국어 발행판에도 영문 심벌 사용 |
| C-P2 · 구성 양성 · en/ko | Blender v5.3.0 Add의 기존값 0.25, 새 값 1, 중심 사각형. [Box Mask L76–103](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L76-L103) | 가운데 사각형 마스크를 만들고 바깥의 기존 마스크값 보존 | 1/24 | B-M03. CPU 고정 분기 검산. 매뉴얼 예는 캐시에서 확인 |
| C-N1 · 구성 음성 · en/ko | Blender v5.3.0 소켓을 교차한 문장. [Bokeh Blur L18–44](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L18-L44) | 편집 가능한 마스크를 필터에서 꺼내고 원 이미지 유지 | 0/24 | Mask는 필터 범위를 받는 소켓이고 출력은 Image |
| C-N2 · 구성 음성 · en/ko | Manual 5.3.0 편집·표시를 교차한 문장. [Filter Layer L7–11](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) | 화면 위에서만 효과 미리 보기, 원 픽셀과 레이어 구성 유지 | 0/24 | Filter Layer는 원 픽셀을 보존하며 레이어를 추가한다 |

## 표 2 · 조사에서 표시까지

| 요청·언어 | 별칭·역할 | 조사 → 표시 | 기능 ID·원어·한국어 | 지지·충돌 원절 | 누락 단계 |
| --- | --- | --- | --- | --- | --- |
| 자연 N-B1–3, N-K1–3 · en/ko | 네 조건 | — → — | 공석 | [frame](frame.csv) | 요청 모집 |
| C-P1 · ko | 00, 10, 01, 11 | 1 → 1 | K-L01 · Clone Layers · 영어 유지 | [원본 편집과 갱신 예](https://docs.krita.org/en/reference_manual/layers_and_masks/clone_layers.html#example-uses-of-clone-layers) | — |
| C-P2 · ko | 00, 01 및 목표판 10, 11 | — → — | B-M03 · Box Mask · 매뉴얼 한국어 미확인 | [Add 분기 L76–103](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L76-L103) | 조사 |
| C-P2 · ko · 보조판 | 10, 11 | 1 → 1 | B-M03 · Box Mask · 박스 마스크(UI) | [사각형·바깥 보존 L76–103](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L76-L103) | — |
| C-P2 · en/ko · 표기 보조판 역할 누락 | 11 | 1 → — | B-M03 · Box Mask · 박스 마스크(UI) | [실제 입력·출력 소켓](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) | 표시 |
| E-B2 · en | 00, 10 | 1 → 1 | B-M01 · Cryptomatte · 크립토마테(UI) | [렌더·이미지 입력 L650–677](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_cryptomatte.cc#L650-L677) | 자료집 직접 적격 0, 충돌 표시 |
| E-B2 · en | 01, 11 | 1 → — · 5 → 1 | B-M01 → K-L02 · File Layers · 영어 유지 | [EXR 입력 L650–677](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_cryptomatte.cc#L650-L677) · [외부 파일 참조](https://docs.krita.org/en/reference_manual/layers_and_masks/file_layers.html#file-layers) | 기존 충돌이 내려가고 다른 충돌이 표시 |
| E-B3 · ko · 보조판 | 10, 11 | 1 → 1 · 2 → 2 · 3 → 3 | B-M05 Double Edge Mask · 이중 에지 마스크, B-M03 Box Mask · 박스 마스크, B-M04 Ellipse Mask · 타원 마스크 | [그라디언트 분기](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_double_edge_mask.cc#L41-L74) · [Viewer 표시](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_viewer.cc#L37-L60) | 자료집 직접 적격 0, 일부 2와 충돌 1 |
| E-K2 · en | 00, 10 → 01, 11 | 1 → 1에서 1 → — | K-L02 · File Layers · 영어 유지 | [ToImageSize 분기](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/ui/kis_file_layer.cpp#L359-L403) | 자료집 직접 적격 0, 일부가 표시에서 밀림 |
| E-K3 · ko · 보조판 | 00 → 10 | — → —에서 1 → 1 | K-R02 · File Format · 파일 형식(HTML) | [PNG 중간 파일 L28–31](https://docs.krita.org/en/reference_manual/render_animation.html#export-as-image-sequence) | 자료집 직접 적격 0, 새 충돌 |
| C-N1 · en | 00 → 01 | 1 → 1에서 1 → — | B-F03 · Bokeh Blur · 보케 블러(UI) | [Mask 입력, Image 출력](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L18-L44) | 충돌만 교체 |
| C-N1 · ko · 보조판 | 10 → 11 | 1 → 1에서 1 → 1 | B-F03 · Bokeh Blur · 보케 블러(UI) | [같은 소켓의 역할 충돌](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L18-L44) | 후보 하나, 재정렬 후에도 표시 |
| C-N2 · ko · 보조판 | 10, 11 | 1 → 1 | K-L04 · Filter Layer · 필터 레이어(HTML) | [레이어와 원 픽셀 L7–11](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) | 자료집 직접 적격 0, 충돌 표시 |
| C-N2 · ko · 해당 표기 결측 | 10, 11 | — → — | K-L04 · Filter Layer | [같은 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) | 확인된 충돌이 조사에서 사라짐 |

## 표 3 · 회수, 손실, 오추천과 비용

| 방식·언어·표본층 | 적격 있는 요청 분모 | 표시 직접·신규·손실·오추천·공석 | 준비·조회 비용 | 반복 일치·미확인 |
| --- | ---: | --- | --- | --- |
| 목표판 00·10·01·11 · 각 en/ko · 자연 | 미평가 6 | 전부 미평가, 표시 예정 18 공석/방식·언어 | 0 쿼리·0 SQL | 예정 96행, 두 빈 DB의 공석 상태 일치 |
| 목표판/보조판 00·10 · en · 탐색 | 0/6 | 0·0·0·13·0. 일부 5 | 각각 6 쿼리·6 SQL | 일치, recall 계산 불가 |
| 목표판/보조판 01·11 · en · 탐색 | 0/6 | 0·0·0·15·0. 일부 3 | 각각 6 쿼리·12 SQL | 일치, recall 계산 불가 |
| 목표판 00·10/01·11 · ko · 탐색 | 0/6 | 각각 0·0·0·3·15 | 각각 6 쿼리, SQL 6/8 | 일치, 매뉴얼 PO 별칭 0 |
| 보조판 00/01 · ko · 탐색 | 0/6 | 각각 0·0·0·3·15 | 각각 6 쿼리, SQL 6/8 | 일치 |
| 보조판 10/11 · ko · 탐색 | 0/6 | 각각 0·0·0·5·11. 일부 2 | 각각 6 쿼리, SQL 6/10 | 일치, 두 충돌 신규. 4 공석에 일부 2와 충돌 2 |
| 목표판/보조판 00·10/01·11 · en · 구성 | 2/4 | 각각 2·0·0·9·0. 일부 1 | 각각 4 쿼리, SQL 4/8 | 일치 |
| 목표판 00·10/01·11, 보조판 00/01 · ko · 구성 | 2/4 | 각각 1·0·0·2·9 | 각각 4 쿼리, SQL 4/5 | 일치, B-M03은 조사 누락 |
| 보조판 10/11 · ko · 구성 | 2/4 | 각각 2·1·0·6·4 | 각각 4 쿼리, SQL 4/8 | 일치, 후보 1개짜리 충돌도 표시됨 |

**PARTIAL.** [표 1 원장](evidence/table1.csv), [표 2 전수 추적](evidence/table2.csv), [표 3 방식을 풀어 쓴 원장](evidence/table3.csv), [요청별 집계](evidence/summary.json)가 표의 근거다. 표의 비용과 성과는 첫 재생 기준이다. 신규와 손실은 같은 언어·표본층의 00과 비교한 요청–기능 쌍이며 오추천은 충돌로 확인한 행이다. 두 언어·판본을 같은 시나리오의 반복으로 계산했다.

### Q1 · 같은 기능, 다른 표기

Krita 한·영 5.3.0의 레이어와 애니메이션 출력에서 12자리를 직접 확인했다. 해당 조작의 한국어 표지는 필터 레이어, 첫 번째/마지막 프레임, 파일 형식으로 3기능 4표기다. Clone Layers를 포함한 나머지 9개 기능 표제는 한국어 HTML에서도 영어로 남았다. Git의 5.3 RST와 발행 HTML에는 출력 번호 표제와 Android 안내 차이가 있다. SVN 한국어 PO와 해당 발행 키의 대응은 0/12다. [한글 레이어 목차](https://docs.krita.org/ko/reference_manual/layers_and_masks.html) · [한글 Render Animation](https://docs.krita.org/ko/reference_manual/render_animation.html#export-as-image-sequence) · [원본 대조 X-K-PO-KEY-DIFF](sources.jsonl)

Blender 5.3의 12자리는 발행자 동일판 목차 캐시와 고정 구현을 대조했다. 영어와 한국어 발행 본문의 직접 열기 및 매뉴얼 PO 대응은 0/12다. 앱의 v5.3.0 gettext에서는 12개 심벌 이름의 한국어 문자열을 읽었다. Legacy와 현행 Cryptomatte는 각각 별개 등록 심벌과 소켓을 가진다. UI PO와 한국어 HTML의 겹침을 매뉴얼 번역 원본 검증으로 합치지 않았다. [모집 보완](evidence/recruitment-amendment.md) · [소유 카드](catalog.jsonl)

### Q2 · 작성자 요구와 볼 수 있었던 창

공식 프로젝트 두 곳의 생성순 각 첫 40개와 40/41 경계는 미확인이다. 검색·REST 대체 시도와 공개 메일 아카이브 조사 결과를 원장에 남겼다. Blender 개별 게시물 2개, Right-Click Select 제안 1개, KDE 세 게시물을 탐색층에 사용했다. 두 Krita 보고는 작성자가 다르고 연결 결함은 같다. #484353의 재생/내보내기 구분은 검토했으나 탐색 선발의 앞 세 건보다 늦었다. 번역은 별도 한국어 사용자 표본 0건이다. 카드 작성 경험을 가진 동일 작업자가 영어 단문화 뒤 번역했고, 최초 제출판은 0/6 확인했다. [접근·탈락 원장](frame.csv) · [번역·노출](queries.jsonl) · [판독 기록](evidence/assessment.md)

### Q3 · 답 공급과 증거 한계

예정 자연 144쌍은 모두 예약 공석이다. 탐색 144쌍은 직접 0, 일부 6, 충돌 138이다. 일부 판정에는 파일 레이어의 크기 신호와 Backdrop 그래프의 기본 출력 분기가 포함된다. 실제 운영 조건에서의 두 보존 조건 전체는 유보했다. 구성 96쌍은 직접 2, 일부 2, 충돌 92다. C-P2에서 기존값이 새 값보다 큰 반례의 CPU Add 동작을 확인했으므로 수치가 고정된 대조의 보존 근거에 한정했다. [자연 예정](truth.csv) · [탐색 판정](evidence/truth-exploratory.csv) · [구성 판정](evidence/truth-controls.csv) · [반례](evidence/counterexamples.md)

### Q4 · 대역어와 역할은 서로 다른 단계에 작용했다

목표 매뉴얼의 같은 키가 전부 미확인이므로 주 분석에서 A1에 입력된 별칭은 0이다. 보조판은 발행자 앱 gettext와 한국어 HTML을 사용했다. 한국어 구성 C-P2의 조사는 0→4 후보, B-M03은 첫 표시로 들어왔다. C-N1에서 입력 소켓을 산출물로 읽은 B-F03은 영어 표시에서 빠졌다. 한국어의 조사 후보가 그 하나뿐일 때 충돌 표지를 달고도 첫 자리에 남았다. 이 역할 방식은 빈 슬롯을 만드는 필터가 아니라 순위 조작이다. [카드](catalog.jsonl) · [구성 보조판](evidence/ranks-controls-publisher.csv)

역할 충돌만으로 정렬하면 서로 비교할 공통 개념이 없는 후보의 벌점이 0이다. E-B2 영어에서 B-M01의 EXR 방향을 맞게 지적하고도 File Layers와 이미지 시퀀스 설정을 올렸다. E-K2 영어에서는 File Layer의 일부 지지까지 떨어졌다. 같은 대상의 입출력 구분과 사용 가능성은 각각 증거가 필요하다. [탐색 보조판](evidence/ranks-exploratory-publisher.csv) · [File Layer 크기 경로](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/ui/kis_file_layer.cpp#L359-L403)

### Q5 · 띄어쓰기, UI 심벌, 역할 오판

한국어 변형의 이미지 시퀀스/이미지시퀀스는 둘 다 K-R02의 파일 토큰만 맞아 3점이었다. 필터 레이어/필터 레이어를 변형에서는 레이어 토큰이 후자에서 빠져 6→3점이고 필터 토큰 덕분에 순위 1이 유지됐다. 이 두 번째 표현 쌍은 조사 외 주변 표현도 바뀌었으나, 나머지 변경 토큰은 카드의 일치에 기여하지 않았다. 형태소 분석을 적용하면 달라질 수 있는 범위다. C-P1은 한국어 표지가 빈 Clone Layers를 영문 심벌로 회수했다. E-B2처럼 두 언어 모두에 직접 답이 없는 요구는 대역어가 있어도 적격을 만들지 못한다. [변형 원장](evidence/ranks-variants-publisher.csv) · [한국어 Clone Layers](https://docs.krita.org/ko/reference_manual/layers_and_masks/clone_layers.html)

Box Mask 카드에서 mask의 output 표지만 제거한 구성 교란은 두 언어에서 B-M03을 조사 1위에 유지하면서 표시 밖으로 밀어냈다. 파일·픽셀 보존 같은 다른 조건을 평가하지 않아도 불완전한 역할 태그 하나가 손실을 일으킬 수 있다. 고정 원문의 직접 적격 판정은 유지됐다. MusicXML과 MARC는 같은 값이나 이름의 표기 관점을 별도로 읽는 절차를 보여 준다. 기보 D5와 실제 C5, 통일표제와 번역판 표시를 각각 원례에서 확인했다. [교란 원장](evidence/ranks-box_role_omitted.csv) · [음악·서지 원절](evidence/counterexamples.md)

### Q6 · 어느 위치에서 사라졌나

목표 자연 48조회 × 2의 96행을 보존했고 실제 자연 조회는 0이다. 확보한 탐색을 48조회 × 2 × 두 판에서 실행했다. 탐색 여섯 쌍의 양 언어 공통 적격 분모는 0이므로 recall은 계산하지 않는다. 구성의 양 언어에서 공급이 있는 질문은 C-P1과 C-P2 두 건이다. 영어는 두 판과 네 조건 모두 2/2가 조사와 표시까지 갔다. 한국어는 목표판 1/2, 보조판에서 별칭을 켜면 2/2다. 역할 태그를 고친 원래 보조판의 구성 direct 손실은 0이고 역할 하나를 뺀 구성에서만 C-P2의 표시 손실이 발생했다. [양성 쌍·누락 단계](evidence/summary.json) · [전체 재생](costs.json)

자료 영수증 148행에는 원출처 URL 144개와 도착 URL 84개가 기록됐다. 고유 계보 36개는 기능 18, 작성자 요구 6, 변경·혼동 8, 타 분야 규격·원례 4다. 요구·변경 계보 14개다. 원절을 읽은 기록 75행, 접속 실패 61행, 검색 캐시 9행, 아카이브 셸 3행을 구별했다. 시도 수는 등록한 영수증 단위이며 HTTP 요청 총수를 계측한 값은 아니다. 같은 이슈 계보의 코드·보고·릴리스와 언어판·미러 중복은 다시 산입하지 않았다. [자료 원장](sources.jsonl)

### Q7 · 유지할 수 있는 가벼운 근거

기본 영어 카드의 문서 계보는 18개, URL·제목·메모 합계 4,539 UTF-8 바이트, 토큰 게시 행 567개다. 보조 별칭은 추가 출처 3개에서 15기능·16표지·30토큰 행을 만들고 근거 JSON 6,066바이트가 들었다. 역할 쪽은 같은 18개 카드 문서에서 87문장을 태깅했다. 탐색 요청의 역할 위치는 작성자 문서 6개에서 뽑았다. 역할 근거 바이트는 19,155다. SQLite는 기본 24,576, 별칭 테이블 4,096, 역할 45,056바이트로 73,728바이트다. 목표판의 비어 있는 별칭 테이블도 한 페이지를 차지했다. 별칭 조회는 쿼리당 한 SQL 안에서, 역할 조회는 후보가 있으면 SQL 하나가 더 들었다. 수작업 시간과 현장 지연은 미측정이다. [비용과 지문](costs.json)

사전 지정 Clone Layers는 KO 표제가 영어라 비공백에서 결측으로의 차분을 만들 수 없었다. 원래 null→null 재생은 동일하다. 사전 추가한 보조 교체에서 K-L04의 필터 레이어를 빼니 KO C-N2의 첫 표시 충돌이 사라졌다. 누락된 표제가 늘 오추천을 줄인다는 뜻을 이 한 자리에서 추론할 수 없다. [교체 계획](evidence/scenarios.json) · [교체 순위](evidence/ranks-filter_missing.csv)

자료 구축자는 공식 심벌이 이미 공유되고 원절이 짧고 명확하면 가벼운 원문으로 시작할 수 있다. 한국어 질문자의 어휘가 앱·문서의 공식 표제에 닿고 그 기능이 자료집에 존재하는 경우 별칭이 재탐색을 줄인다. 표시 세 개만 보는 독자에게는 원절의 대상과 역할이 함께 맞고 그 밖의 보존 조건도 설명되는 쪽이 도움을 준다. 조사 후보가 하나뿐이거나 역할이 파이프라인의 일부만 표현하면 단순 재정렬의 효용은 제한된다. 이 조건들은 고정 제품 필드 선택과 별개다.

| 가장 중요한 불일치·약점 | 다음 조사·직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 트래커 순차 창 0/80, 자연 요청 0/6, 최초 표현 미확인 | [재현의 API 첫 입력](reproduce.md), 공식 페이지와 원 ID의 첫 게시물 스냅샷 | 40/41 경계가 재구성되고 두 조건이 있는 첫 3건씩에서 직접 적격이 나온다 |
| 목표 매뉴얼 한·영 PO 매칭 0/24. 앱 표기 및 HTML 보조판에서만 증가를 관측 | Blender 5.3 POT·ko PO·HTML, Krita 해당 빌드의 SVN PO revision, [문서 번호 반례](sources.jsonl) | 같은 msgid·기능·판이 맞는 비공백 별칭에서 신규 직접 적격이 재현된다 |
| 역할 충돌을 낮추면서 일부도 밀어냈고 한 태그 누락이 적격을 밀어냈다 | [파일 레이어 고정 코드](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/ui/kis_file_layer.cpp#L359-L403), [Box Mask 교란](evidence/ranks-box_role_omitted.csv), 동일 원절의 독립 판독 | 같은 후보 집합에서 충돌을 낮추고 직접·일부를 보존하거나 독립 판독이 현 태그의 역할과 불일치한다 |
