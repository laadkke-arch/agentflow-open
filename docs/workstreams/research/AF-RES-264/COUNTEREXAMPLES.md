# AF-RES-264 반례와 정정

주행렬 16회의 고정판은 `683db1be46c3d969e564b2d1a527dafe4f959dcd`다. 교차와 EPUB의 첫 관측은 `e945b0e8e9df0f14a74138cddc9a40e2b1eff707`이다. 이 파일은 날짜·ID, 위치, XML 원바이트를 따로 확인한 뒤 정리한 판이다. [쌍별 원비교](receipts/comparisons.json) · [원 PDF 판독](receipts/controls/) · [EPUB 종결 영수증](receipts/epub/)

| 깨뜨릴 수 있는 가설 | 직접 판독과 정정 | 적용할 수 있는 범위 |
|---|---|---|
| 새 writer가 필수다 | old writer + 2.3 템플릿의 생성 TeX가 2.3 기본 맞춤 TeX와 바이트 동일. new writer + old 템플릿은 old 기본과 동일. 2.3에 해당 블록만 삭제하면 `Contents`로 돌아왔다. 세 통제 모두 패스별 종료 0. | 고정 fixture·article. 두 템플릿에는 filecolor 및 Beamer 등 다른 변경도 있다. 이 입력의 제목에 대한 인과만 분리했다. |
| 제목 키를 설정하면 목차가 생긴다 | 두 판 모두 toc off + 키 있음에서 AST MetaString을 읽었다. TeX의 `contentsname` override와 `tableofcontents`, 페이지의 TOC 제목/항목은 정상 공석이다. 최종 PDF의 일반 책갈피는 4개다. | 두 릴리스의 기본 템플릿 CLI 조합. YAML의 `toc`나 맞춤 템플릿의 직접 호출은 별도 입력이다. |
| 제목·항목·탐색은 항상 함께 생긴다 | 8회의 toc on 첫 패스에서 인쇄 제목 8/8, 항목 0/8. 16회의 첫 패스에서 PDF catalog `/Outlines` 정상 부재 16/16. 모든 사례에서 다음 패스에 본문 책갈피가 생겼다. 2.3 `bookmarks=false`에서 패스 3 제목/4항목과 같은 래스터를 보존하고 정상 빈 outline을 읽었다. | 패스 진행 중 공석과 의도된 최종 공석을 분리한다. 별도 깨진 파일에서 mutool/pypdf는 각 exit 1과 stderr를 남겼다. |
| 화면의 동일한 제목과 책갈피가 목적지까지 동일함을 뜻한다 | 제목 키 변화만 비교하면 2.3 toc on에서 4 destination 이름·페이지·좌표가 유지됐다. `--toc` 자체를 켜면 Tree Title·parent는 유지되지만 첫 노드가 `section*.1` (y=549.639) → `section*.2` (y=448.947)로 바뀌었다. | 1쪽 /XYZ 좌표의 단위는 PDF pt. 노드명, 경로, 화면 기준 좌표와 파일의 raw PDF 기준 좌표를 구별한다. |
| 탐색 책갈피를 한 줄 추가해도 페이지 기하가 그대로다 | `\pdfbookmark[1]{Navigation Index 264}{af-res-264-toc}`을 TOC 전에 넣으면 5번째가 아닌 첫 루트 노드가 추가됐다. 표시 문자열과 TOC 4항목은 같고, 본문 네 목적지 y가 각각 9.035 pt 감소했다. 96 dpi 래스터와 bbox도 실제 차이를 보였다. | TOC 대상에 별도 이름을 줄 수 있다는 증거다. 페이지 위치 보존 요구에는 삽입 지점을 바꾸고 다시 조판해야 한다. |
| 제목만 제어하는 기능을 목차 깊이에도 적용할 수 있다 | `--toc-depth=1`에서는 TOC와 outline이 4→2로 함께 줄었다. `Archive Contents 264`는 유지됐다. 2.3 + v7.01l에서 인쇄 깊이를 탐색 깊이 기본값으로 공유하는 반례다. | `bookmarksdepth`를 따로 제어하면 연결을 풀 수 있다는 근거는 hyperref 코드다. 별도 override 조합은 실행 범위 밖이다. |
| PDF SHA 또는 bbox XHTML SHA가 다르면 독자에게 보이는 결과도 다르다 | 주행렬 반복 8쌍 모두 원 PDF SHA가 달랐다. 각 파일의 두 literal date와 trailer ID 값만 같은 길이로 마스킹하면 8/8 전체 바이트 일치. bbox 문서의 head에는 날짜 메타데이터가 있고 `<page>`는 8/8 동일했다. 96 dpi 래스터, 개별 목적지도 동일했다. 동일 epoch 두 새 폴더는 원 PDF 바이트까지 같았다. | 이 fixture의 pdfTeX literal 필드 전용 마스킹이다. 압축 Info 객체나 다른 PDF 엔진에는 필드 수/표현 검사가 다시 필요하다. |
| EPUB 배포본과 원파일의 다른 blob은 제목이나 탐색이 바뀌었다는 뜻이다 | 첫 ZIP 판독에서 4/4 원 blob과 달랐지만 XML 해석은 2/2 같았다. 후속 byte 검사에서 배포 XML에만 CRLF가 51/73/79/36개 있었고 LF로 치환하면 4/4 픽스처와 동일했다. Git의 자동 LF 변환은 이 소유 경로의 container 영수증에 한해 껐다. | OPF/nav 4파일 및 지정 ZIP에 한한다. PDF 출력 분모와 실제 EPUB reader UI는 별개다. |

출처 원장의 PDF 정오표 적용 한계에 붙인 사전 표기 `PDF 1.5`는 원산출물의 실제 `%PDF-1.7` header로 정정했다. Adobe PDF 32000-1 원 PDF 경로의 읽기 제한은 접근 실패로 남겼다. [정정된 원장](sources.jsonl) · [실제 PDF 정보](receipts/matrix/v23-on-unique-r1/pdfinfo.txt)

인쇄 층 변화의 반례를 찾기 위해 문서 제목·본문 제목·TOC 항목·PDF Info `/Title`·탐색 트리를 별도 필드로 비교했다. 동일 표본에서 navigation-only를 원한 사용자 사건이나 현대 다른 class에서의 출력 성공을 이 실험의 성공 건수로 더하지 않았다. 두 단독 래스터 렌더가 픽셀 수준의 GUI 동작이나 인쇄 장치별 출력까지 검증한다는 판단은 보류했다.
