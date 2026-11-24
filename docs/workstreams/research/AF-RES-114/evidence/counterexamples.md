# 반대 사례 원절

| 계보 | 같은 이름이나 어구 | 원절에서 확인한 경계 | 연결 행 |
| --- | --- | --- | --- |
| Blender Mask 입력 | Mask | Mask 데이터블록과 프레임을 읽어 스칼라 마스크를 계산한다. 그래프상의 소켓과 편집할 스플라인은 다른 대상이다. [L183–203](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_mask.cc#L183-L203) | X-B-mask · C-N1 |
| Blender Viewer | Image | 입력 영상을 이미지 편집기나 Backdrop에 표시한다. [L37–60](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_viewer.cc#L37-L60) | X-B-viewer · E-B3 |
| Blender File Output | Image, passes, EXR | single/multilayer와 포맷·쓰기 경로를 구별하고 직렬화한다. 타 앱이 EXR을 해석하는 방법은 이 절에서 미확인이다. [L442–482](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_file_output.cc#L442-L482) | X-B-file_output · E-B2 |
| Krita Transparency Mask | Mask | 검정과 흰색을 칠해 레이어의 투명도와 가시 영역을 바꾼다. [마스크 추가 예 L7–17](https://docs.krita.org/en/reference_manual/layers_and_masks/transparency_masks.html#how-to-add-a-transparency-mask) | X-K-TRANSP · C-N2 |
| Krita Selection Mask | Mask | 선택을 저장·복구하며 한 레이어에 선택을 여러 개 붙일 수 있다. [L7–18](https://docs.krita.org/en/reference_manual/layers_and_masks/selection_masks.html) | X-K-SELECT · C-N1 |
| Krita Reference Images | Reference / file | 참조 이미지를 이동 가능한 표시로 올린다. 임베드, 디스크 링크, 보기 명령이 역할을 드러낸다. [저장 모드와 View L53–67](https://docs.krita.org/en/reference_manual/tools/reference_images_tool.html#tool-options) | X-K-REFERENCE · E-K2 |
| Krita 5.2 FFmpeg | Export | 번들 기본 경로와 외부 바이너리 선택이 공존한다. 당시 Android 지원 범위는 달랐다. [Animation L10–20](https://krita.org/en/release-notes/krita-5-2-release-notes/#animation) | X-K-FFMPEG · K-R02 |
| Krita 5.3 Fast Color Overlay | Overlay | normal/tint가 처리한 스케치 픽셀의 입력과 출력을 보여 준다. [발행 예](https://krita.org/en/release-notes/krita-5-3-release-notes/) | X-K-FASTCOLOR · C-N2 |

Blender 5.3.0 UI의 Blur는 문맥 없는 compositor 표기와 Operator·ID 항목에서 모두 블러로 번역된다. Box Mask도 문맥 없는 항목과 Operator 표기가 같다. 현행 Cryptomatte의 크립토마테와 레거시 이름의 크립토매트는 철자뿐 아니라 등록 심벌과 입력도 다르다. [한국어 PO](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/locale/po/ko.po#L45306-L45332) · [현행 등록](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_cryptomatte.cc#L905-L922) · [레거시 등록](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_cryptomatte.cc#L1025-L1038)

Box Mask CPU에서 Add는 사각형 안의 새 값과 입력값 중 큰 값을 쓰고, 밖에서는 기존 값을 쓴다. 입력값이 이미 새 값보다 높으면 안쪽을 무조건 새 값으로 대체한다는 설명과 어긋날 수 있다. 구성 대조는 기존값 0.25, 새 값 1, 사각형 바깥 보존에 한정했다. [L76–103](https://github.com/blender/blender/blob/02f0899d78e374b63e7181d9061e1f7ab03419cc/source/blender/nodes/composite/nodes/node_composite_box_mask.cc#L76-L103)

MusicXML 4.0의 transpose는 기보음에 더해 실음을 얻는 값이고 staff 범위를 가질 수 있다. 실제 72b 시험 파일에서 E♭ 클라리넷의 A4에 +3 반음, B♭ 클라리넷의 D5에 −2 반음을 더하면 둘 다 C5다. 표준의 concert-score 예는 실음 총보와 파트용 표시를 따로 담는다. 검사는 파트 ID, 값의 관점, 이조 방향과 범위를 확인한 뒤 음을 비교한다. [MusicXML 규격](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/transpose/) · [XML 입력](https://github.com/cuthbertLab/music21/blob/40e95ae567fe8b8e35317447dc74d5cdbb2fb83d/music21/musicxml/lilypondTestSuite/72b-TransposingInstruments-Full.xml#L69-L124) · [실음 총보 예](https://www.w3.org/2021/06/musicxml40/musicxml-reference/examples/concert-score-and-for-part-elements/)

MARC 21의 240은 해당되는 주요 명의 아래의 통일표제, 245는 해당 판의 표제와 책임표시, 041의 a와 h는 자료 언어와 원본 언어다. 실제 2000년 영어판 DLC 99050439는 240에 Petit prince. English, 245에 The little prince, 041에 eng와 fre가 있다. 제목을 함께 찾되 240의 작품 접근점과 245의 판본 표시, 041 언어의 귀속을 대조한다. 이 레코드의 범위는 2000년 출판물이다. [240](https://www.loc.gov/marc/bibliographic/concise/bd240.html) · [245](https://www.loc.gov/marc/bibliographic/concise/bd245.html) · [041](https://www.loc.gov/marc/bibliographic/concise/bd041.html) · [실제 MARC 레코드](https://catalog.kent-school.edu/cgi-bin/koha/opac-MARCdetail.pl?biblionumber=29427)

음악에서는 악기의 파트와 이조 방향을 읽어야 같은 실음을 검증할 수 있다. 서지에서는 작품과 개별 판 중 대상이 무엇인지 확인해야 표지의 귀속을 정할 수 있다. 이 자료의 배당과 기능 수는 원장에서 별개다.
