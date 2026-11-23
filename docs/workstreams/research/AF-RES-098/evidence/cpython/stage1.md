# CPython: ① 이전 판 선정 봉인

상태: 이전판 선정 완료. 새 판 예제 본문·이미지·배포 목록·CI는 아직 열지 않았다. 다음 판 릴리스의 날짜와 ‘first maintenance’ 설명만 읽었다.

## 판 선택

공식 [전체 릴리스 목록](https://www.python.org/downloads/)에서 공개일을 읽었다. 안정 x.y.0 목록은 3.11.0(2022-10-24, 기간 밖), 3.12.0(2023-10-02), 3.13.0(2024-10-07), 3.14.0(2025-10-07) 순이다. 따라서 2023–2025 첫 안정판은 **3.12.0**이다. [3.12.0 발행 페이지](https://www.python.org/downloads/release/python-3120/)가 날짜와 안정판임을 확인하며, [3.12.1 발행 페이지](https://www.python.org/downloads/release/python-3121/)가 2023-12-08 및 첫 maintenance release임을 명시한다.

## 모집 경로·해석

[3.12.0 공식 다운로드](https://docs.python.org/release/3.12.0/download.html) → [HTML ZIP](https://docs.python.org/ftp/python/doc/3.12.0/python-3.12.0-docs-html.zip)으로 확보했다. ZIP URL은 www.python.org의 같은 경로로 리다이렉트했고 12,737,860B, SHA256 `87eb7fa9ffec111a02d0a0515bd219a09735942e3d488e4f88d51f5befc895fa`다. 압축파일 1,063개 엔트리의 HTML 515개 상대경로를 사전식 정렬해 [frame.csv](frame.csv)에 전부 남겼다.

적격 가족은 `c-api/`, `extending/`, `howto/`, `library/`, `reference/`, `tutorial/`이다. 테마·로고·공통 내비게이션을 제외한 주 본문에서 `img/src`, `source/src/srcset`, 로컬 이미지·데이터 다운로드 `href`를 탐색했다. 로컬 본문 이미지가 있는 적격 페이지는 6개다. 첫 둘은 `howto/logging.html`, `library/hashlib.html`; 그 뒤는 `library/pathlib.html`, `library/statistics.html`, `library/tkinter.messagebox.html`, `library/turtle.html`이다. `using/windows.html`의 설치 화면은 별도 설치 안내 가족이라 제외했으며 앞의 첫 둘 선택에 영향은 없다.

이 과제의 ‘예제 본문’은 **예제·튜토리얼·참조 페이지의 주 내용**으로 고정한다. 두 선택은 설명 그림이며 프로그램을 실행해 얻은 결과 그림이라고 분류하지 않는다. 실행 산출물로 좁게 정의하면 선택이 바뀔 수 있다는 해석상 한계를 사전에 보존한다. 단순한 코드 문자열 `open('file')`는 발행된 이미지·데이터 URI와 구분한다.

## 고정 두 사례

| ID | 옛 절·목적 | 본문이 직접 참조하는 로컬 파일 | 실제 바이트 |
|---|---|---|---|
| PY1 | [3.12.0 Logging Flow](https://docs.python.org/release/3.12.0/howto/logging.html#logging-flow); logger/handler의 전달·중단 흐름 설명 그림 | `../_images/logging_flow.png`; HTML 612행 | [PNG](https://docs.python.org/release/3.12.0/_images/logging_flow.png), 955×758, 21,907B, SHA256 `70d752f336a9ee7af4a56b8e5b3696b962b69793b274f76439165823c69cf5e0` |
| PY2 | [3.12.0 BLAKE2 Creating hash objects](https://docs.python.org/release/3.12.0/library/hashlib.html#creating-hash-objects); tree mode의 depth/offset/fanout 그림 | `../_images/hashlib-blake2-tree.png`; HTML 705행 | [PNG](https://docs.python.org/release/3.12.0/_images/hashlib-blake2-tree.png), 500×322, 11,070B, SHA256 `382828d64e88644e47e695d717ea8432ec1ef79a17f2d209b11aef4fdbfa4bf5` |

HTML과 PNG 모두 정확한 판의 직접 URL을 다시 열어 ZIP 내부 파일과 같은 바이트인지 대조했다. 두 본문에는 base 요소가 없어 문서 URL을 기준으로 상대참조를 해석했다. 두 PNG를 직접 열어 그림 내용을 확인했다. 본문과 그림에는 새 판의 생성 시점을 증명하는 정보가 아직 없다.

## 열람과 수

직접 읽은 발행 목록/기록 3, 다운로드·배포 목록 2, 선택 본문 2, 실제 PNG 2로 **9 고유 1차 자료**다. ZIP을 통해 자동 탐색한 나머지 513 HTML을 사람이 읽은 본문으로 산입하지 않는다. 같은 바이트의 ZIP 내부·직접 URL은 중복 산입하지 않는다. 실제 귀속 계보는 **CPython 문서** 1개다. 다운로드 페이지의 도구별 재열람은 같은 자료다.

근거: [sources.jsonl](sources.jsonl), [old-http-receipts.json](old-http-receipts.json), [PY1 발췌](PY1-old-excerpt.json), [PY2 발췌](PY2-old-excerpt.json), [선정 JSON](selected.json). 웹 검색 도구에서 다운로드 페이지 접근 실패가 한 번 있었지만 직접 HTTP 다운로드는 성공했다; 실패 응답은 자료 수에 넣지 않는다.

다음 첫 행동: ① 커밋 확인 후 3.12.1 공식 HTML 배포의 **파일명 목록만** 열고, `_images/logging_flow.png`, `_images/hashlib-blake2-tree.png`의 존재/동명 중복을 사전 예측으로 남긴다. 새 본문·payload·CI는 ② 예측 커밋 뒤에 연다.
