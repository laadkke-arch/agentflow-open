## 표 1 · 고정 요구와 조사

| 요구·층·언어 | 작성자 원문 또는 구성 입력 | 조작·대상 / 보존 | 자료집 직접/일부/충돌/미확인 | 조사 크기 / 집합 ID 접두 | 근거·미확인 |
| --- | --- | --- | --- | --- | --- |
| N-B1–3, N-K1–3 · 자연 예정 · en/ko | [114 모집 원장](https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/frame.csv) | 공석 · 범위가 확인된 작성자 입력 없음 | 미평가 | en 0 · ko 0 | 6개 요청 예정, 각 언어별 실행 0 |
| E-B1 · 탐색 · en/ko | [원문·구성](https://blender.community/c/rightclickselect/wrZ8/) L11–19, L34–36 | Glare 노드 결과를 EXR 파일로 내보내기 / 다른 렌더 결과를 출력에 섞지 않기 | 0/0/2/22 | en 12 / `8c3dcd59` · ko 0 / `4f53cda1` | S-I-GLARE · Glare 단독 산출. Glare 및 File Output은 자료집 밖. |
| E-B2 · 탐색 · en/ko | [원문·구성](https://projects.blender.org/blender/blender/issues/128731) L65–87, 작성자 첫 게시물 | UV·Mist·Cryptomatte 렌더 패스를 EXR로 기록하기 / 외부 앱에서 열어도 각 패스의 렌더 내용과 구별을 유지하기 | 0/0/5/19 | en 11 / `122c72e8` · ko 2 / `8a6d6f50` | S-I-EXR · 종전 고정 문장 사용. 작성자 직접 본문 재개봉 미확인. |
| E-B3 · 탐색 · en/ko | [원문·구성](https://projects.blender.org/blender/blender/issues/130134) L65–97, 작성자 첫 게시물 | Box Mask 결과를 Viewer에 표시하기 / 연결하지 않은 Double Edge Mask가 그래프에 남아 있어도 멈추거나 크래시하지 않기 | 0/2/0/22 | en 11 / `e04fc8d7` · ko 4 / `19002bac` | S-I-PREVIEW · 생성·비연결 분기는 일부. 해당판 안정성 미확인. |
| E-K1 · 탐색 · en/ko | [원문·구성](https://bugs.kde.org/show_bug.cgi?id=464692#c0) L24–43, L55–61 | 고른 레이어들만 합쳐서 새 레이어를 한 번에 만들기 / 선택하지 않은 레이어를 합치지 않고 기존 레이어는 유지하기 | 0/2/0/22 | en 9 / `93267328` · ko 0 / `4f53cda1` | S-I-MERGE · 원본 유지 의도는 복제 후 병합에서 추론. |
| E-K2 · 탐색 · en/ko | [원문·구성](https://bugs.kde.org/show_bug.cgi?id=467257#c0) L58–81 | 문서 크기나 내보내기 크기를 줄일 때 연결된 파일 레이어도 축소하기 / 파일 레이어의 내용 전체를 유지하고 잘라내지 않기 | 0/1/0/23 | en 11 / `22843681` · ko 1 / `5ff4cf34` | S-I-FILE-SCALE · ToImageSize 일부. Advanced Export 미확인. |
| E-K3 · 탐색 · en/ko | [원문·구성](https://bugs.kde.org/show_bug.cgi?id=470110#c0) L56–94 | 파일 레이어와 변형 마스크를 문서/내보내기 크기에 비례해 축소하기 / 옮겨 둔 상대 위치를 캔버스 안에서 유지하기 | 0/1/0/23 | en 12 / `7cfd790d` · ko 1 / `634c20fc` | S-I-FILE-MASK · 상대 위치와 두 경로의 보존 미확인. |
| C-P1 · 114 구성 · en/ko | [원문·구성](https://docs.krita.org/en/reference_manual/layers_and_masks/clone_layers.html#example-uses-of-clone-layers) L8–20, paint layer → clone → HSV/blur masks | 소스 편집에 따라 빛 효과 복제 레이어 갱신 / 원래 도색 레이어에 계속 그릴 수 있음 | 1/2/0/21 | en 7 / `c37d7f3c` · ko 6 / `61aa490a` | S-K-CLONEDOC · 114 구성 양성, 한국어판 영문 표제. |
| C-P2 · 114 구성 · en/ko | [원문·구성](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L76-L103) 공식 Add 예시 설명과 L76–103 CPU 분기. 중심 (0.5, 0.5), 값 1, 기존 바깥 0.25 → 바깥 0.25 | 박스 마스크 Add의 가운데 사각형을 덧붙인 마스크 산출 / 사각형 밖 기존 마스크 값 유지 | 1/0/2/21 | en 10 / `9d7bb6f9` · ko 4 / `1531b09f` | S-B-BOX · 114 구성 양성, Add 바깥 값. |
| C-N1 · 114 구성 · en/ko | [원문·구성](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L18-L44) L18–44 input Mask and output Image | Bokeh Blur에서 편집 가능한 마스크 산출 / 원 이미지 유지 | 0/0/1/23 | en 12 / `6e7c50a1` · ko 1 / `d9427abd` | S-B-BOKEH · 114 구성 음성, Mask 입력/Image 출력. |
| C-N2 · 114 구성 · en/ko | [원문·구성](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) L7–11 whole canvas Filter Layer and replaceable settings | 편집 개체를 만들지 않고 표시 오버레이로 효과 미리 보기 / 원본 픽셀과 레이어 구성 동시 유지 | 0/0/1/23 | en 12 / `bec0f5ab` · ko 1 / `9c7bd1f3` | S-K-FILTERDOC · 114 구성 음성, 새 레이어가 필요한 경로. |
| H-B1 · 신규 구성 · en/ko | [원문·구성](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/tests/python/compositing_node_group.py#L9-L20) L9-L20 | 기존 지오메트리 그룹을 합성 루트에 사용 / 기존 소켓과 그룹 유형 유지 | 0/0/0/24 | en 12 / `a9c25480` · ko 0 / `4f53cda1` | S-B-ROOT · RuntimeError 정적 단언. 범위가 다른 그룹을 구별. |
| H-B2 · 신규 구성 · en/ko | [원문·구성](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/blenkernel/intern/cryptomatte_test.cc#L79-L93) L79-L93 | Cryptomatte 스탬프 경로에서 레이어 식별자 추출 / 불완전 키에 레이어 ID를 부여하지 않음 | 0/0/2/22 | en 12 / `ae974366` · ko 2 / `1736409a` | S-B-HASH · 정상·불완전 키의 검사. 해시 노드 출력 미지원. |
| H-B3 · 신규 구성 · en/ko | [원문·구성](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/blenkernel/intern/image_test.cc#L247-L284) L247-L284,L291-L318 | 외부 멀티레이어 EXR을 가져와 패스에 접근 / Combined·Albedo 등 개별 패스 이름을 보존 | 0/1/0/23 | en 12 / `81ce3491` · ko 0 / `4f53cda1` | S-B-IMPORT · 기대 이름 16개. 고정 EXR 본체 미확인. |
| H-K1 · 신규 구성 · en/ko | [원문·구성](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/image/tests/kis_adjustment_layer_test.cpp#L53-L69) L53-L69 | 빈 선택을 반전한 필터 레이어를 캔버스에 적용 / 원래 캔버스 경계 안으로 유지 | 1/1/0/22 | en 11 / `380e2381` · ko 1 / `7e6d89fa` | S-K-ADJ · 선택 경계 검사. 효과 픽셀 미실행. |
| H-K2 · 신규 구성 · en/ko | [원문·구성](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/image/tests/kis_clone_layer_test.cpp#L786-L862) L786-L862 | 복제본을 가진 그룹을 Clone Layers로 복제 / 복제본의 흐림 마스크에도 합성 완료 | 1/2/0/21 | en 12 / `eb4239c2` · ko 2 / `971a7cd6` | S-K-CLONE · with/without blur 기준 PNG 같은 계보. |
| H-K3 · 신규 구성 · en/ko | [원문·구성](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/image/tests/kis_filter_mask_test.cpp#L27-L99) L27-L99 | 한 페인트 레이어의 선택 범위만 Filter Mask로 반전 / 비선택 영역 및 빈 선택일 때 원본 픽셀 유지 | 1/0/1/22 | en 12 / `8ae9c7ee` · ko 1 / `7e6d89fa` | S-K-MASK · 선택 0·최대 단언. 한국어 조사에서 적격 누락. |

자료집의 네 범주는 [기준판독](judgments.csv)의 같은 24개 기능이다. [표 1 원장](evidence/table1.csv)에 언어별 전체 조사 ID, 순위 12개, 동률 집단, 공석, 조사 밖 직접 적격을 보존했다.

## 표 2 · 조사 원순위에서 표시 정책까지

| 요구·언어·정책·순번 | 원 조사→스캔 순위 · 후보 ID | 사용 가능한 URL·절 | 표시·조건부·공석 이유 | 채점 기준 | 사라짐·대체 | 채점 결과 |
| --- | --- | --- | --- | --- | --- | --- |
| E-B2 en · A 1 | 5→1 · K-L02 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/file_layers.html#file-layers) L5–28 | A 순서대로 표시 | 114 및 원절 | — | 충돌 |
| E-B2 en · A 2 | 6→2 · K-R01 | [카드 원절](https://docs.krita.org/en/reference_manual/render_animation.html#general) L17–25 | A 순서대로 표시 | 114 및 원절 | — | 미확인 |
| E-B2 en · A 3 | 7→3 · K-R02 | [카드 원절](https://docs.krita.org/en/reference_manual/render_animation.html#export-as-image-sequence) L28–31 | A 순서대로 표시 | 114 및 원절 | — | 미확인 |
| E-B2 en · B 1 | 6→2 · K-R01 | [카드 원절](https://docs.krita.org/en/reference_manual/render_animation.html#general) L17–25 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | 빠짐 K-L02 | 미확인 |
| E-B2 en · B 2 | 7→3 · K-R02 | [카드 원절](https://docs.krita.org/en/reference_manual/render_animation.html#export-as-image-sequence) L28–31 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | 위치 이동 K-R01 | 미확인 |
| E-B2 en · B 3 | 8→4 · K-R03 | [카드 원절](https://docs.krita.org/en/reference_manual/render_animation.html#export-as-image-sequence) L33–36 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | 대체 K-L02 (충돌) | 미확인 |
| E-B2 en · C 1 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 K-L02 | 공석 |
| E-B2 en · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 K-R01 | 공석 |
| E-B2 en · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 K-R02 | 공석 |
| E-B3 en · A 1 | 9→1 · K-L01 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/clone_layers.html#example-uses-of-clone-layers) L6–32 | A 순서대로 표시 | 114 및 원절 | — | 미확인 |
| E-B3 en · A 2 | 1→2 · B-M05 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_double_edge_mask.cc#L13-L37) L13–37 | A 순서대로 표시 | 114 및 원절 | — | 일부 |
| E-B3 en · A 3 | 2→3 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | A 순서대로 표시 | 114 및 원절 | — | 일부 |
| E-B3 en · B 1 | 9→1 · K-L01 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/clone_layers.html#example-uses-of-clone-layers) L6–32 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | — | 미확인 |
| E-B3 en · B 2 | 1→2 · B-M05 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_double_edge_mask.cc#L13-L37) L13–37 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | — | 일부 |
| E-B3 en · B 3 | 2→3 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | — | 일부 |
| E-B3 en · C 1 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 K-L01 | 공석 |
| E-B3 en · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 B-M05 | 공석 |
| E-B3 en · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 B-M03 | 공석 |
| C-P2 ko · A 1 | 1→1 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | A 순서대로 표시 | 114 및 원절 | — | 직접 |
| C-P2 ko · A 2 | 2→2 · B-M04 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_ellipse_mask.cc#L30-L61) L30–61 | A 순서대로 표시 | 114 및 원절 | — | 충돌 |
| C-P2 ko · A 3 | 3→3 · B-M05 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_double_edge_mask.cc#L13-L37) L13–37 | A 순서대로 표시 | 114 및 원절 | — | 충돌 |
| C-P2 ko · B 1 | 1→1 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | — | 직접 |
| C-P2 ko · B 2 | 4→4 · B-M06 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_id_mask.cc#L19-L31) L19–31 | 카드에서 명시 충돌이 확인되지 않아 표시 | 114 및 원절 | 대체 B-M04 (충돌) | 미확인 |
| C-P2 ko · B 3 | 공석 | — | 비충돌 후보가 3개 미만 | 114 및 원절 | 빠짐 B-M05 | 공석 |
| C-P2 ko · C 1 | 1→1 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | 조작·대상과 보존 확인 | 114 및 원절 | — | 직접 |
| C-P2 ko · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 B-M04 | 공석 |
| C-P2 ko · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 B-M05 | 공석 |
| C-N1 ko · A 1 | 1→1 · B-F03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L18-L44) L18–44 | A 순서대로 표시 | 114 및 원절 | — | 충돌 |
| C-N1 ko · A 2 | 공석 | — | 조사 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| C-N1 ko · A 3 | 공석 | — | 조사 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| C-N1 ko · B 1 | 공석 | — | 비충돌 후보가 3개 미만 | 114 및 원절 | 빠짐 B-F03 | 공석 |
| C-N1 ko · B 2 | 공석 | — | 비충돌 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| C-N1 ko · B 3 | 공석 | — | 비충돌 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| C-N1 ko · C 1 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | 빠짐 B-F03 | 공석 |
| C-N1 ko · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| C-N1 ko · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 114 및 원절 | — | 공석 |
| H-K1 ko · A 1 | 1→1 · K-L04 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) L5–14 | A 순서대로 표시 | 봉인한 공식 시험 | — | 직접 |
| H-K1 ko · A 2 | 공석 | — | 조사 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K1 ko · A 3 | 공석 | — | 조사 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K1 ko · B 1 | 1→1 · K-L04 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) L5–14 | 카드에서 명시 충돌이 확인되지 않아 표시 | 봉인한 공식 시험 | — | 직접 |
| H-K1 ko · B 2 | 공석 | — | 비충돌 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K1 ko · B 3 | 공석 | — | 비충돌 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K1 ko · C 1 | 1→1 · K-L04 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) L5–14 | 빈 선택 반전 후 범위가 기존 캔버스와 일치하는지 확인 | 봉인한 공식 시험 | — | 직접 |
| H-K1 ko · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K1 ko · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 봉인한 공식 시험 | — | 공석 |
| H-K3 en · A 1 | 1→1 · K-L05 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_masks.html#filter-masks) L5–18 | A 순서대로 표시 | 봉인한 공식 시험 | — | 직접 |
| H-K3 en · A 2 | 2→2 · K-L04 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer) L5–14 | A 순서대로 표시 | 봉인한 공식 시험 | — | 충돌 |
| H-K3 en · A 3 | 3→3 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | A 순서대로 표시 | 봉인한 공식 시험 | — | 미확인 |
| H-K3 en · B 1 | 1→1 · K-L05 | [카드 원절](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_masks.html#filter-masks) L5–18 | 카드에서 명시 충돌이 확인되지 않아 표시 | 봉인한 공식 시험 | — | 직접 |
| H-K3 en · B 2 | 3→3 · B-M03 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L32-L63) L32–63 | 카드에서 명시 충돌이 확인되지 않아 표시 | 봉인한 공식 시험 | 빠짐 K-L04 | 미확인 |
| H-K3 en · B 3 | 4→4 · B-M04 | [카드 원절](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_ellipse_mask.cc#L30-L61) L30–61 | 카드에서 명시 충돌이 확인되지 않아 표시 | 봉인한 공식 시험 | 대체 K-L04 (충돌) | 미확인 |
| H-K3 en · C 1 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 봉인한 공식 시험 | 빠짐 K-L05 | 공석 |
| H-K3 en · C 2 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 봉인한 공식 시험 | 빠짐 K-L04 | 공석 |
| H-K3 en · C 3 | 공석 | — | 조작·대상 근거 후보가 3개 미만 | 봉인한 공식 시험 | 빠짐 B-M03 | 공석 |

위는 서로 다른 결과를 보인 사례다. [표 2 전수 원장](slots.csv)에 44개 요청–언어 행의 3정책×3자리를 모두 기록했다. 활성 요청의 288자리와 미모집 요청의 108 예정 자리를 포함한다. [정책 스캔 원장](evidence/policy-scans.csv)은 후보의 빠진 조작·역할·보존 근거를 보여 준다.

## 표 3 · 표시 후 회수, 비용과 공석

| 층·언어·정책 | 요청 / 직접 적격 요청 / 직접 적격 쌍 | 직접 회수 요청/쌍 / A 대비 손실 요청/쌍 | 충돌 · 일부 · 미확인 요청/쌍 | 공석 / 전부 보류 (후보가 있었던 보류) | 공유 SQL / 근거 조회 / UTF-8 바이트 | 반복 일치·비교 불가 |
| --- | --- | --- | --- | --- | --- | --- |
| 114 구성 · en · A | 4 / 2 / 2 | 2/2 / 0/0 | 1/2 · 1/1 · 3/7 | 0 / 0 (0) | 8 / 0 / 0 | 일치 |
| 114 구성 · en · B | 4 / 2 / 2 | 2/2 / 0/0 | 0/0 · 1/1 · 4/9 | 0 / 0 (0) | 8 / 14 / 38,399 | 일치 |
| 114 구성 · en · C | 4 / 2 / 2 | 2/2 / 0/0 | 0/0 · 0/0 · 0/0 | 10 / 2 (2) | 8 / 41 / 97,010 | 일치 |
| 114 구성 · ko · A | 4 / 2 / 2 | 2/2 / 0/0 | 3/4 · 0/0 · 1/2 | 4 / 0 (0) | 8 / 0 / 0 | 일치 |
| 114 구성 · ko · B | 4 / 2 / 2 | 2/2 / 0/0 | 0/0 · 0/0 · 2/3 | 7 / 2 (2) | 8 / 9 / 25,327 | 일치 |
| 114 구성 · ko · C | 4 / 2 / 2 | 2/2 / 0/0 | 0/0 · 0/0 · 0/0 | 10 / 2 (2) | 8 / 12 / 31,376 | 일치 |
| 탐색 · en · A | 6 / 0 / 0 | 0/0 / 0/0 | 2/2 · 2/3 · 6/13 | 0 / 0 (0) | 12 / 0 / 0 | 일치 · 회수율 계산 불가 |
| 탐색 · en · B | 6 / 0 / 0 | 0/0 / 0/0 | 0/0 · 2/3 · 6/15 | 0 / 0 (0) | 12 / 20 / 42,462 | 일치 · 회수율 계산 불가 |
| 탐색 · en · C | 6 / 0 / 0 | 0/0 / 0/0 | 0/0 · 0/0 · 0/0 | 18 / 6 (6) | 12 / 66 / 142,941 | 일치 · 회수율 계산 불가 |
| 탐색 · ko · A | 6 / 0 / 0 | 0/0 / 0/0 | 1/2 · 1/2 · 3/3 | 11 / 2 (0) | 10 / 0 / 0 | 일치 · 회수율 계산 불가 |
| 탐색 · ko · B | 6 / 0 / 0 | 0/0 / 0/0 | 0/0 · 1/2 · 3/3 | 13 / 3 (1) | 10 / 7 / 21,130 | 일치 · 회수율 계산 불가 |
| 탐색 · ko · C | 6 / 0 / 0 | 0/0 / 0/0 | 0/0 · 0/0 · 0/0 | 18 / 6 (4) | 10 / 8 / 23,633 | 일치 · 회수율 계산 불가 |
| 신규 구성 · en · A | 6 / 3 / 3 | 3/3 / 0/0 | 2/3 · 1/1 · 6/11 | 0 / 0 (0) | 12 / 0 / 0 | 일치 |
| 신규 구성 · en · B | 6 / 3 / 3 | 3/3 / 0/0 | 0/0 · 1/1 · 6/14 | 0 / 0 (0) | 12 / 21 / 59,212 | 일치 |
| 신규 구성 · en · C | 6 / 3 / 3 | 2/2 / 1/1 | 0/0 · 0/0 · 0/0 | 16 / 4 (4) | 12 / 71 / 169,470 | 일치 |
| 신규 구성 · ko · A | 6 / 3 / 3 | 2/2 / 0/0 | 2/2 · 0/0 · 2/2 | 12 / 2 (0) | 10 / 0 / 0 | 일치 |
| 신규 구성 · ko · B | 6 / 3 / 3 | 2/2 / 0/0 | 0/0 · 0/0 · 2/2 | 14 / 3 (1) | 10 / 6 / 20,045 | 일치 |
| 신규 구성 · ko · C | 6 / 3 / 3 | 2/2 / 0/0 | 0/0 · 0/0 · 0/0 | 16 / 4 (2) | 10 / 6 / 20,045 | 일치 |
| 자연 예정 · en, ko · A, B, C 각각 | 0 / 미평가 / 미평가 | 미평가 | 미평가 | 18 공석 / 비교 불가 | 0 / 0 / 0 | 예약 행만 일치 |

[표 3 원장](evidence/table3.csv)과 [집계](metrics.json)에 요청 단위와 요청–기능 단위, 회수율 분모, 준비행과 읽은 글자 수를 모두 두었다. 공통 준비는 역할 87행, 발행 표기 16행, 카드 근거 주석 23행, 요구 주석 16행이다. 온라인 정책 조회는 0이다. A의 0은 표시 판단에서 카드 본문을 읽는 단계가 없다는 측정값이며 반환 링크의 렌더 비용은 제외했다.

**PARTIAL.** 고정 32개 요청–언어에서 C는 확인된 충돌 15자리와 근거 미확인 38자리를 모두 비웠다. 동시에 A가 보여 준 직접 적격 9쌍 중 1쌍과 일부 근거 7쌍이 사라졌다. B는 직접 9쌍과 일부 7쌍을 보존했고 근거 미확인 표시를 38→46으로 늘렸다. 전체 35개 고유 저작을 직접 읽었다. 필수 작성자 요구는 5/6 직접 개봉, 신규 비교는 6자리 중 1자리의 EXR 입력 본체가 미확인이다. [집계](metrics.json) · [출처 원장](sources.jsonl) · [보류 원장](heldout.csv)

## Q1 · 같은 후보와 순서

**직접 관측.** 114 공식 보조판의 두 순위 파일에서 11을 추린 40행과 새 계산의 어휘 조사 12개, 역할 순서, 실제 상위 3개, 공석이 맞았다. 언어별 20개 요청의 중복 실행 2회다. C-P2 한국어 원 조회에서 B-M04/B-M05/B-M06은 각각 3점으로 동률이고 ID 순서가 유지됐다. E-B2 영어는 K-L02가 원 조사 5위에서 역할 순서 1위, C-N1 영어는 B-F03이 원 조사 1위에서 표시 밖이다. C-N1 한국어는 B-F03 하나만 조회돼 A에 표시됐다. 12 밖의 후보와 조사 안에서 3 밖으로 밀린 후보를 각각 기록했다. 조사 제한 밖의 동률 점수는 선행 원장에 없다. [대사](evidence/baseline-reconciliation.json) · [표 1 원장](evidence/table1.csv) · [114 고정 코드](https://github.com/laadkke-arch/agentflow-open/blob/4e0d3f8dc2ba1f982f4a5dc8e99e4c351603b450/docs/workstreams/research/AF-RES-114/tools/replay.py#L104)

## Q2 · 무관한 링크와 원절로 반박되는 링크

**발행자 진술 및 직접 판독.** Bokeh Blur의 Mask는 범위를 제어하는 입력이고 산출 소켓은 Image다. C-N1에는 동일 명칭이 반대 방향으로 붙었으므로 명시 충돌이다. Box Mask는 Mask 입력과 출력을 각각 선언한다. Add의 바깥은 기존 값을 복사한다. Double Edge Mask는 inner/outer 입력으로 경계 사이 그라디언트를 만들어 E-B3의 한 부품이 된다. Viewer에 이미지를 쓰는 호출은 따로 있어 mask/output 태그만으로 Viewer 표시나 비연결 노드 안정성을 증명할 수 없다. [Bokeh Blur L17–44](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_bokeh_blur.cc#L17-L44) · [Box Mask L30–103](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L30-L103) · [Viewer L37–45](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_viewer.cc#L37-L45)

**작업자 판독.** Defocus의 카드에 있는 mask/input 태그에서 이름 그대로의 Mask 소켓은 미확인이다. 고정 선언에는 Image와 Z 입력이 있다. Z 비사용 분기에 값을 연결할 수 있는 방식과 Bokeh Blur의 명시 Mask 소켓은 적용 범위가 다르다. [Defocus L32–40](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_defocus.cc#L32-L40) · [역할 원장 S-B-BOKEH, S-B-DEFOCUS](sources.jsonl)

**발행자 진술과 상충 사례.** File Layers는 외부 파일을 참조하며 Scale to Image Size 같은 별도 모드가 있다. 고정판은 ToImageSize에서 캔버스 크기의 변화에 따라 다시 읽는다. 이전 요구의 기존 PNG, Advanced Export와 변형 마스크의 위치까지 보존하는지는 미확인이다. 이 일부 근거가 고정 카드의 짧은 메모에 빠져 C가 보류한다. Filter Layer는 아래 레이어에 효과를 입히는 별도 레이어다. C-N2의 새 레이어 전제에서는 구성이 변한다. 이미 필터 레이어가 있는 문서에서 가시성을 토글하는 경우에는 스택 보존 판정이 달라질 수 있다. [File Layers](https://docs.krita.org/en/reference_manual/layers_and_masks/file_layers.html#file-layers) · [크기 변경 분기](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/ui/kis_file_layer.cpp#L345-L413) · [Filter Layer](https://docs.krita.org/en/reference_manual/layers_and_masks/filter_layers.html#filter-layer)

## Q3 · 같은 조사 안에서 사라진 것

**직접 관측.** 전체 32개 요청–언어의 A/B/C 직접 회수는 9/9/8쌍이다. 확인된 충돌은 15/0/0, 일부 근거는 7/7/0, 미확인 표시는 38/46/0, 공석은 27/34/88자리다. 114 탐색 6요구×24카드의 기준은 직접 0, 일부 6, 충돌 138이다. 같은 144쌍을 이번 명시 원절 틀에 놓으면 직접 0, 일부 6, 명시 충돌 7, 미확인 131이다. 114는 기능 불일치까지 충돌에 포함했다. [기준판독](judgments.csv) · [정책 스캔](evidence/policy-scans.csv) · [집계](metrics.json)

B에서 제거된 확인 충돌을 미확인 후보로 채운 경우가 6개 요청–언어의 8자리다. 그중 기존 표본의 5자리는 114 기준에서 충돌을 다른 충돌로 바꿨다. E-B2 영어에서 파일을 참조하는 K-L02가 빠지고 애니메이션 시퀀스의 이미지 디렉터리를 정하는 K-R03이 들어온다. E-B3 영어에서 C는 B-M05와 B-M03의 일부 근거를 모두 잃는다. 노드를 연결하지 않아도 안정적으로 미리 보는 요구에는 마스크 생성 외에 Viewer 동작의 증거가 필요하다. [표 2 전체](slots.csv) · [Krita 이미지 시퀀스 옵션](https://docs.krita.org/en/reference_manual/render_animation.html#export-as-image-sequence) · [Blender #130134](https://projects.blender.org/blender/blender/issues/130134)

## Q4 · 새 대조와 결과의 독립성

**구성 대조.** 먼저 기록한 목록의 Blender 시험 입력과 기준 PNG는 LFS 데이터가 전달되지 않았다. 같은 5.3 고정판의 테스트 정의에서 루트 그룹에 GeometryNodeTree 대입 예외, 정상·짧은 Cryptomatte 키의 결과, 외부 EXR의 16개 패스명 단언을 순서대로 읽었다. 세 번째는 기대 이름과 포인터까지 확인했다. Cryptomatte 커널 검사는 qwerty 형태의 구간도 추출한다. 16진 해시 검증 또는 노드 소켓 출력은 미확인이다. Krita는 빈 선택 반전, Clone 중첩+blur, Filter Mask의 MIN/MAX_SELECTED를 선택했다. Clone의 기준 PNG 두 장과 Filter Mask의 원본·반전 PNG를 직접 열었다. 같은 시험의 두 입력은 각각 한 사건이다. [모집 순서](evidence/heldout-file-order.jsonl) · [함수 순서](evidence/heldout-symbol-order.jsonl) · [보류 및 기대값](heldout.csv)

보류층은 영어와 한국어 각각 3/6 요청에 직접 적격이 있다. 모두 Krita다. 영어 A/B는 3건, C는 2건을 표시했고 두 건 모두 조건부다. 한국어에서 H-K3의 K-L05는 자료집에 있으나 조사에 들어오지 않았다. 영어에서는 K-L05가 조사·A 표시 1위였고 C에서 빠졌다. 빈 선택의 동일성과 최대 선택의 반전을 공식 검사가 단언한다. 고정 카드에는 Invert가 이름으로 주어지지 않았다. 6쌍은 한 작업자가 썼으며 기준은 정책 실행 전에 커밋했다. 프로그램 입력에서 기준 열을 차단했고, 작업자 자신은 114 결과와 공식 기대값을 읽었다. [Filter Mask 고정 시험](https://github.com/KDE/krita/blob/148ce5cfc24252922e3866e67af91c12f17b2e08/libs/image/tests/kis_filter_mask_test.cpp#L27-L99) · [기준판독](judgments.csv) · [입력 경계](policy-view.jsonl)

## Q5 · 역할과 표제의 결측

**직접 관측.** Box Mask의 mask/output 한 행을 없애도 고정 조사와 A/B는 그대로다. C-P2의 C는 두 언어에서 B-M03을 잃고 0개가 된다. 114 재조회부터 시작하면 원 어휘 조사 순위는 그대로이고 역할 스캔 순서는 3개 요청–언어에서 움직였다. C-P2 영어 A·B에서 B-M03이 빠졌고 한국어 A에서도 빠졌다. 한국어 B는 B-M06 뒤에 B-M03을 남겼다. [교란 전수](evidence/perturbations.csv) · [출력 소켓](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L30-L63)

발행 표제 행 박스 마스크만 없애면 고정 조사에서 정책 입력 해시와 화면이 완전히 같다. 재조회하면 한국어 C-P2와 E-B3의 조사에서 B-M03이 빠진다. C-P2는 A/B/C 모두 기존 직접 적격을 잃고, 원래 C가 비운 E-B3는 그대로다. K-L01의 한국어 Manual 화면은 영문 Clone Layers를 보여 준다. C-P1과 H-K2의 한글 요구에 이 영문 심벌이 포함됐다. 한국어만 쓰는 질문에서의 회수는 미검증이다. [Blender 발행 PO](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/locale/po/ko.po#L45122-L45123) · [Krita 한국어 화면](https://docs.krita.org/ko/reference_manual/layers_and_masks/clone_layers.html)

## Q6 · 세 사용자의 비용

**직접 계수.** 원장에 올린 후보 URL은 73, 본문 또는 포인터가 도착한 원장 행은 53, 직접 읽은 본문·바이너리 행은 46, 사건 중복 제거 뒤 고유 저작은 35다. 그중 시험 본문 6, 기능 원전 19, 도서관과 통계의 명세·실기록 각 2다. 선행 작성자 요구는 5문서를 직접 개봉했고 중복 수정 계보를 합쳐 고유 4로 셌다. #128731은 직접 시도가 막힌 상태에서 공식 검색 캐시의 작성자 내용을 확인했으며 개봉 산입에서 제외했다. 판독 범위는 73,752글자와 UTF-8 74,705바이트, PNG 검증에 입력한 별도 바이너리는 1,031,322바이트다. 반복 조회는 같은 원장 행에 합쳤다. [출처](sources.jsonl) · [수치와 분모](metrics.json)

- 이용자는 96자리 중 A의 69링크, B의 62링크, C의 8링크를 받는다. C의 4링크에는 별도 확인 항목이 붙고, A/B의 미확인 추천 자리는 각각 38/46이다. 실제 클릭과 이해 시간은 미측정이다. [표시 원장](slots.csv)
- 번역 편집자는 발행 표제 16행과 색인 30행을 유지한다. 선행 역할 데이터는 87행이고 발행 별칭 근거는 6,066바이트다. Blender UI 표제 확인은 PO 응답 3,456,968바이트를 가져와 필요한 10줄을 읽었다. 같은 기능의 영어 표제 잔류와 미번역을 기록할 필요가 있다. [S-B-ALIAS, S-K-CLONEKO](sources.jsonl) · [색인 비용](evidence/baseline-reconciliation.json)
- 검색 운영자는 세 정책에 공통 32회 조회와 60 SQL문을 쓴다. 카드 어절 23행과 요청 정의 16행이 추가 준비다. B는 77 후보 조회와 201,171글자/206,575바이트를, C는 204 후보와 477,293글자/484,475바이트를 검사했다. 온라인 조회는 두 정책 모두 0이다. 이 단위는 직렬화 내용의 반복 입력량이다. [집계](metrics.json)

**분야 대조.** 일본 국립국회도서관의 전거 모델은 prefLabel, altLabel, 읽는 법을 별도 속성으로 둔다. 실기록 00435632는 라틴 전거형에 일본어·키릴문자·다른 라틴 표기를 연결하고 이전 표제의 변경 이력을 남긴다. 이 방식은 표제 검색에는 옮길 수 있다. 같은 명칭의 입력·출력 소켓과 기능 판의 변화는 추가 근거가 필요하다. [NDL RDF 모델](https://id.ndl.go.jp/information/model_en/) · [NDL 00435632](https://id.ndl.go.jp/auth/ndlna/00435632)

Statistics Canada 명세는 기간 결측 두 점, 비공표 x, 적용 불가 세 점을 분리한다. 실제 표 5-13 Yukon의 지역 간 이전 행에는 Naphtha specialties 0.0, Asphalt 결측, Lubricating oils and greases 비공표가 함께 나온다. 공석의 사유를 드러내는 방식은 제품에 옮길 수 있다. 공개 숫자 0도 반올림일 수 있어 검색 결과 0이 자료집 밖의 기능 부재를 증명하지 못하는 경우와 맞닿는다. 통계의 값은 조사 설계에 따른 관측이고 제품의 공석은 질문 해석·색인·판독에도 의존한다. [기호 명세](https://www.statcan.gc.ca/en/concepts/definitions/guide-symbol) · [Table 5-13](https://www150.statcan.gc.ca/n1/pub/57-003-x/2019002/tbl/tbl-5-13-eng.htm)

## Q7 · 한 자리만 읽을 때와 세 자리를 읽을 때

**직접 관측.** 이 표의 수치는 32개 요청–언어에서의 표시된 요청–기능 쌍이다. 마지막 열만 요청–언어 수다. 조건부로 표시된 네 쌍은 별도 기준에서는 모두 직접 적격이었다.

| 정책·열람 폭·독해 | 직접 추천으로 읽힌 쌍 | 충돌 / 일부 / 미확인 추천 쌍 | 별도로 읽힌 조건부 | 추천이 0인 요청–언어 |
| --- | ---: | --- | ---: | ---: |
| A · 첫 자리 · 두 독해 동일 | 9 | 7 / 2 / 10 | 0 | 4 |
| A · 세 자리 · 두 독해 동일 | 9 | 15 / 7 / 38 | 0 | 4 |
| B · 첫 자리 · 두 독해 동일 | 9 | 0 / 2 / 13 | 0 | 8 |
| B · 세 자리 · 두 독해 동일 | 9 | 0 / 7 / 46 | 0 | 8 |
| C · 첫 자리 또는 세 자리 · 모든 반환을 추천으로 읽음 | 8 | 0 / 0 / 0 | 0 | 24 |
| C · 첫 자리 또는 세 자리 · 조건부 분리 | 4 | 0 / 0 / 0 | 4 | 28 |

여기서는 직접 적격을 모두 첫 자리에서 만났다. 세 자리를 읽을 때 늘어난 것은 A/B의 일부 부품과 충돌·미확인이다. C의 조건부 네 건은 H-K1과 H-K2의 두 언어다. B에서 제거한 충돌만 집계하면 K-R03의 유입을 놓친다. C의 H-K3 공석은 적격 카드가 조사에 들어온 경우에도 생겼다. E-B1 한국어는 A부터 후보가 하나도 없었다. 현재 고정 소스의 Glare 단독 소켓과 File Output을 연결하면 카탈로그 밖의 조작 단서가 생긴다. 연결해 실제 EXR을 쓰는 결과는 추론이며 외부 호환은 미실행이다. [열람별 집계](metrics.json) · [Glare 출력](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_glare.cc#L87-L106) · [File Output의 pass 기록](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_file_output.cc#L542-L584)

## 적용할 선택과 비용

**작업자 추론.** 카드가 조작과 대상의 원절을 제공할 때는 보존 확인 여부를 붙인 C가 유력하다. 확인되지 않은 세 번째 자리는 보류 사유를 붙일 수 있다. 제작 부품 탐색이 목적이면 Viewer와 연결될 마스크처럼 확인된 하위 조작을 명시한 링크에 가치가 있다. 현재 C의 요청 단위 기준에서는 일부 근거 7개가 빠졌다. 부품 경로를 별도로 시험할 때 원 요청, 하위 조작과 사용자 확인 비용을 함께 추적해야 한다.

B의 관대한 채우기는 넓은 탐색 목록에서 후보를 노출하는 용도에 쓸 수 있다. 검증 비용을 독자에게 넘기는 경우에는 근거 미확인임을 드러낸다. 상위 유효 카드가 역할 누락으로 빠지는 경우에는 공식 소켓 절에 다시 대조하는 비용과 회수를 측정할 수 있다. 현 재생의 C는 B보다 127번 더 조회했고, 보존의 확인을 사용자에게 넘기는 링크를 4번 표시했다.

활성 표본의 자료집 직접 적격 10쌍 중 9쌍이 조사에 들어왔다. 영어/한국어 탐색층의 직접 적격은 모두 0으로 회수율 계산이 불가능하다. 이 사실과 자연 계층 미모집 때문에 사람의 탐색 성과나 언어별 선호를 일반화할 수 없다. [재현](reproduce.md) · [자가 점검](SELF_CHECK.md)

| 가장 중요한 불일치·약점 | 다음 조사와 직접 열 자료 | 어떤 관측이면 판단이 바뀌나 |
| --- | --- | --- |
| 일부 링크 7개와 직접 링크 1개가 C에서 사라졌다 | Krita Filter Mask Invert와 Blender Viewer의 정확한 소켓 절을 카드에 연결한 소규모 독립 재판독 | 원절을 한 줄 보완해 직접 적격을 복구하고 일부 부품의 조건부 표시에 오확정이 늘지 않는다 |
| Blender 작성자 원문 1건과 보류 EXR 바이트가 미확인이다 | #128731 공식 HTML, #108980 EXR의 LFS OID와 CPU filter 기준 PNG부터 연다 | 고정 입력을 검증한 외부 EXR 해석에서 기존 보존 판독이 달라진다 |
| 두 언어가 같은 작성자의 구성 짝이며 탐색에서 직접 적격이 0이다 | 직접 적격 후보가 있는 고정 요구를 독립 한국어 독자에게 주고 한 자리 및 세 자리의 클릭과 조건부 이해를 관측 | 조건부 확인 성공과 비용이 사용자의 후보 탐색 가치 또는 오추천 손실을 바꾼다 |
