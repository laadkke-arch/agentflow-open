# Q7 — 패키지에 든 것, 본문이 참조한 것, 실제로 실행된 것

이 절의 **Trees EPUB와 build wheel은 보조 사례**다. 주 표본 12쌍·24자리에 넣지 않는다. 두 실물을 수신한 뒤 ZIP 멤버와 참조를 직접 대조했다. [원 영수증·범위](audit.json), [EPUB 멤버 원장](trees-audit.json), [wheel 멤버·RECORD 검산](wheel-audit.json), [자료 원장](sources.jsonl)에 주소·UTC·지문을 남겼다.

| 보조 관측 단위 | 패키지에 포함 | 실제 정적 참조 | 실행·표시·생성 | 바로 뒤집힌 추론 |
|---|---|---|---|---|
| Trees 20230704의 `EPUB/cover.jpg`와 `titlepage.xhtml#titlepage` | YES: OPF의 `cover-image`, ZIP의 JPEG 실물 | 해당 본문의 JPEG 사용 NO. 본문은 canvas와 네 JS를 참조 | EPUB reader 표시·JS 실행·그 발행의 신규 JPEG 생성은 미확인 | 표지 파일이 패키지에 있다는 사실로 본문의 canvas 그림을 그 JPEG로 반환하면 오귀속이다. |
| Trees의 `EPUB/script/tree.js`와 같은 본문 | YES | YES: `script src="script/tree.js"`; 코드가 `#canvas`의 2D context와 그리기 절차를 연결 | 실제 canvas 결과 미확인 | 본문 참조 확인은 reader 지원·실행 결과를 대신하지 않는다. |
| build 1.2.2.post1 wheel의 `build/__main__.py:entrypoint` | YES: RECORD 해시와 멤버 바이트 일치 | `console_scripts`와 `pipx.run`의 두 이름이 같은 함수에 연결됨 | 설치·호출·출력·당해 빌드 생성은 미확인 | 선언이 존재해도 함수가 실행됐다고 보고할 수 없다. |
| 같은 wheel의 `.dist-info/LICENSE` | YES: RECORD에 수록 | 두 entry point의 대상 아님 | 실행 대상이라는 주장 없음 | RECORD 멤버 수를 실행 진입점 수로 세면 틀린다. |

## 1. EPUB: cover-image와 titlepage의 canvas는 다른 관계다

직접 받은 [Trees 공식 패키지](https://github.com/IDPF/epub3-samples/releases/download/20230704/trees.epub)는 **75,717B**, SHA-256 `4fbaa5713555ea104b2aed8fc6182700225416b0ab5369f0cb7293d486bb718f`다. HTTP 응답의 MIME은 `application/octet-stream`이지만 ZIP의 `mimetype` 멤버는 `application/epub+zip`이다. 패키지에는 12멤버, OPF manifest에는 9항목, spine에는 3항목이 있다. [수신 영수증](receipts/trees.epub.json).

확인한 경로는 다음과 같다. 모든 상대 경로는 패키지 내부에서 해석했다.

| 단계 | 실제 위치·값 | 그 값이 확인하는 범위 |
|---|---|---|
| container | `META-INF/container.xml`: `full-path="EPUB/package.opf"` | 패키지 루트에 대한 OPF 위치. `META-INF/EPUB/...`로 잘못 이어 붙이지 않음 |
| OPF manifest | `EPUB/package.opf` L15–25; L20의 `href="cover.jpg" properties="cover-image"` | JPEG가 표지 자원으로 선언됨 |
| spine | 같은 OPF L26–30: `ttl`, `c1`, `c2` | `titlepage.xhtml`, `c1.xhtml`, `c2.xhtml`의 기본 읽기 순서 |
| titlepage | `EPUB/titlepage.xhtml` L28–41, `body#titlepage`; L29의 `canvas#canvas` | 선택 본문의 그림 표현은 canvas |
| 실제 의존 | titlepage L6–9: jQuery, SnakeCollection, Snake, tree JS | 본문이 사용하는 프로그램 자원 네 개 |
| 그리기 연결 | `script/tree.js` L10–23/L33–47; `script/Snake.js` L39–50 | canvas 선택→2D context→그리기 예약 및 arc/fill. JPEG 참조와 구별 |

`cover.jpg`는 **32,681B**, JPEG **400×393**, SHA-256 `85e2083c66d98ac55253c438e387111a0b2cc6a67f1b16920275979c56b1ff75`다. 로컬 이미지 판독에서는 흰 바탕 위 검은 나무 실루엣을 확인했다. 세 XHTML 전체는 각각 canvas 하나·script src 네 개이며 `img`, `picture`, `srcset`, SVG `image`, `object`, `data:` 참조는 모두 0이다. 세 XHTML·CSS 하나·JS 네 개에서 `cover.jpg` 문자열이 없고, 표지 이름은 OPF에만 있다. 저자 JS의 실제 그리기 절차도 JPEG를 가져오는 코드가 아니다. [완전한 범위·참조 형식별 수](audit.json)의 `epub.reference_form_counts`, `literal_cover_hits`를 참조한다.

이것은 **선택한 본문이 그 JPEG를 사용하지 않는다는 음성**이다. EPUB reader가 책장 아이콘이나 별도 표지 보기에서 `cover-image`를 사용하는 가능성까지 부정하지 않는다. 본문 소스에 선언된 참조와 독립된 reader UI 사용을 합치지 않는다.

[EPUB core 규격](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-package-doc)의 container·manifest·spine 규칙으로 패키지 내부 위치를 해석했다. [Reading Systems 3.3 §6.4](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/#sec-scripted-content)는 스크립트 지원 조건을 별도로 다룬다. 따라서 ZIP 검사와 canvas 실행은 별개다. 이 오래된 실물은 EPUB `version="3.0"`을 선언한다. 이번 작업은 링크와 자원 관계를 읽은 것이며 EPUB 3.3 전체 적합성 검사가 아니다.

### 소스와 ZIP 멤버의 바이트도 자동으로 같지는 않다

공식 tag `20230704`는 `46d7e07e1b39b2d0a0245ececaf896edcd9de4b2`를 가리킨다. 이 고정판의 [titlepage 소스](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/trees/EPUB/titlepage.xhtml)와 [OPF](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/trees/EPUB/package.opf)를 추가로 열었다.

| 파일 | 고정 source | ZIP member | 실제 비교 |
|---|---|---|---|
| titlepage.xhtml | 1,375B, SHA-256 `db0c2bac7bcced434345ba6910705fb917de07283cca67774ad602e80c192d0d` | 1,416B, SHA-256 `70fb79f076295e26032ebd203074ff5dee34dbe408f979e9200997c2903f7c52` | 바이트 다름. ZIP의 CRLF 41개를 LF로 바꾸면 소스와 정확히 같음 |
| package.opf | 2,080B | 2,080B | 바이트 같음: SHA-256 `6c363f4886cbf6a90c54f1ab876d1d409a25af841f945eab5397776b8b5a75b3` |

줄바꿈이 바뀐 원인이나 실제 실행 job은 확보하지 않았다. 관측한 것은 두 바이트의 관계이며, 어느 빌드가 이 변환을 했다는 생성 귀속이 아니다.

### 먼저 찾았으나 성립하지 않은 반례

[Children’s Literature 20230704](https://github.com/IDPF/epub3-samples/releases/download/20230704/childrens-literature.epub)도 실제 열었다. 10멤버·manifest 7·spine 3이며 세 XHTML은 모두 spine에 있어, “XHTML이 manifest에만 있고 spine에는 없다”는 반례는 얻지 못했다. 이 탐색을 [별도 감사](childrens-literature-audit.json)에 보존하고, 최소 자료 수와 주 표본에 산입하지 않았다. Trees도 XHTML 세 개 모두 spine에 있다. 성공한 반례는 **본문의 그림과 표지 메타데이터의 구별**이며 spine 누락을 발견했다고 바꾸어 말하지 않는다.

## 2. Wheel: RECORD와 entry_points는 이력 로그가 아니다

[공식 PyPI의 build 1.2.2.post1 레코드](https://pypi.org/pypi/build/1.2.2.post1/json)에서 선택한 [wheel 실물](https://files.pythonhosted.org/packages/84/c2/80633736cd183ee4a62107413def345f7e6e3c01563dbca1417363cf957e/build-1.2.2.post1-py3-none-any.whl)은 **22,950B**, SHA-256 `1d61c0887fa860c01971625baae8bdd338e517b836a2f70dd1f7aa3a6b2fc5b5`다. 수신한 해시는 PyPI 선언과 같았다. 최신판 추천이 아니라 지정 실물에 대한 검사다.

ZIP의 19멤버가 RECORD의 19행에 모두 대응한다. RECORD 자신의 행은 해시·크기가 비어 있고, 나머지 **18/18**의 URL-safe base64 SHA-256과 크기가 실제 멤버에 맞았다. 빠진 ZIP 멤버와 불일치 행은 0이다. [Wheel 규격](https://packaging.python.org/en/latest/specifications/binary-distribution-format/#the-dist-info-directory)의 관련 규칙을 [고정 source](https://raw.githubusercontent.com/pypa/packaging.python.org/5b31c28208dbcef1b089fdf9018910e611d2600f/source/specifications/binary-distribution-format.rst) L234–254에서도 읽었다.

| 파일·위치 | 직접 확인한 값 | 확인하지 않은 것 |
|---|---|---|
| `build-1.2.2.post1.dist-info/entry_points.txt` | `console_scripts`의 `pyproject-build` → `build.__main__:entrypoint`; `pipx.run`의 `build` → 같은 함수 | 실제 명령 설치·호출 |
| `build/__main__.py` L444–445 | `entrypoint` 함수가 존재하며 `main(sys.argv[1:])`를 호출하는 소스 | 함수 실행·빌드 출력 |
| 같은 모듈 L448–449 | `__main__` 조건에서 별도 호출 경로가 있음 | 그 조건을 만족한 실제 프로세스 |
| ZIP 전체 멤버 목록 | `pyproject-build` 명령 wrapper 파일은 없음 | 설치자가 나중에 만든 wrapper와 PATH 노출 |

[Entry points 규격](https://packaging.python.org/en/latest/specifications/entry-points/#use-for-scripts)과 그 [고정 source](https://raw.githubusercontent.com/pypa/packaging.python.org/5b31c28208dbcef1b089fdf9018910e611d2600f/source/specifications/entry-points.rst) L126–146은 선언·설치 wrapper·명령 호출의 관계를 구분한다. 실물에서도 **19개 수록 멤버와 1개 console script, 2개 entry-point 이름, 1개 고유 대상 함수**는 다른 단위다. LICENSE는 수록돼 있지만 진입점 대상이 아니다. 메타데이터가 있는 wheel을 ZIP으로 읽은 사실로 설치나 과거 실행을 인정할 수 없다.

검사 프로그램은 ZIP/XML/CSV/INI를 읽고 Python 소스를 AST로 파싱했다. 다운로드한 `build` 패키지를 import하거나 설치·실행하지 않았다. 이 작업에서 실행하지 않았다는 사실과 다른 장소의 과거 실행 여부 미확인은 구분한다.

## 3. 목적별로 돌려줄 링크

| 요청 목적 | 반환 링크와 볼 위치 | 더 싼 확인으로 충분한 조건 | 틀렸을 때 보여 줄 한 줄 |
|---|---|---|---|
| Trees의 과거 본문·표지를 인용 | [정확 release EPUB](https://github.com/IDPF/epub3-samples/releases/download/20230704/trees.epub) + `EPUB/titlepage.xhtml#titlepage` 또는 `EPUB/cover.jpg`를 구별하여 지문 병기 | 특정 패키지/멤버 인용이면 reader 실행 없이 패키지 해시와 내부 위치까지 확인 | “표지 JPEG는 본문 canvas의 출력이라는 근거가 없습니다.” |
| 선택 판의 canvas 예제를 이용 | 같은 EPUB + `titlepage.xhtml#titlepage`와 `script/tree.js`를 함께 안내 | 코드·구조를 읽는 목적이면 정적 참조 추적으로 충분; 동작을 요구하면 실제 reader/JS 시험 필요 | “본문과 스크립트 참조는 확인했지만 이 reader에서의 실행은 미확인입니다.” |
| EPUB 생성 빌드 재현 | 고정 tag [source tree](https://github.com/IDPF/epub3-samples/tree/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/trees) + release EPUB 지문 | 필요한 bytes 확보까지만이면 둘로 충분; 생성 귀속에는 빌드 환경·명령·출력 digest가 추가로 필요 | “소스와 패키지의 줄바꿈 차이는 확인했지만 이를 만든 실행은 미확인입니다.” |
| build wheel의 역사적 배포를 인용 | [정확 wheel](https://files.pythonhosted.org/packages/84/c2/80633736cd183ee4a62107413def345f7e6e3c01563dbca1417363cf957e/build-1.2.2.post1-py3-none-any.whl) + RECORD/entry_points 내부 위치 | 수록 파일과 선언된 명령 질문이면 다운로드와 정적 검사로 충분 | “배포본과 선언은 확인했으며 설치·실행 성공은 이 자료가 증명하지 않습니다.” |
| 선택 wheel의 명령 경로를 이용·재현 | wheel + `entry_points.txt` → `build/__main__.py:entrypoint`; 실제 실행이 필요하면 환경별 설치·호출 영수증 추가 | 명령 이름/대상 함수 안내는 정적 확인으로 충분; 실행 결과 요구는 별도 | “호출 가능한 대상으로 선언됐지만 실제 wrapper·환경·호출 결과는 미확인입니다.” |

## 4. 자료 수·실패·재검산

원장 16행 중 보수적으로 신규 최소량에 산입하는 것은 **5개**다: EPUB Reading Systems 규격 1 + Trees 실물 1, wheel 규격 2 + wheel 실물 1. [집계](source-counts.json). 이미 AF-RES-098에서 읽었던 EPUB core 규격·동일 20230704 release 사건은 제외했다. 같은 규격의 HTML/RST, 같은 package의 source/member, PyPI 레코드와 배포 실물을 각각 더하지 않았다. Children’s Literature 탐색도 제외했다. 이 다섯 자료가 다섯 독립 실험이라는 뜻은 아니다.

실패는 [failures.jsonl](failures.jsonl)에 구분했다. 처음 추정한 EPUB Reading Systems의 `20260113` URI는 HTTP 404였다. 공식 발행 이력을 확인하여 실제 20241017판을 열었으며, 실패 응답은 자료 수에 넣지 않았다. 최초 환경에서 `requests` 모듈이 없어 외부 요청 전에 종료한 실행은 표준 라이브러리 `urllib.request`로 대체했다. 이 환경 오류는 외부 자료 부재가 아니다.

읽기 전용 재검산은 `python -B docs/workstreams/research/AF-RES-102/evidence/cross-domain/analyze.py`다. 실행 영수증은 [analysis-receipt.json](analysis-receipt.json)에 있다. 프로그램은 이 디렉터리의 audit 파일을 다시 쓰므로, 원 결과를 보존하려면 별도 체크아웃에서 실행한다. 캐시가 없으면 지정한 EPUB·wheel 및 고정 source 두 개를 다시 받는다. 규격 자체 재열람은 `collect.py fetch --key 새키 --url 위의 고정 규격 주소`로 별도 수행한다. 모든 원 수신 영수증과 원 지문은 커밋에서 다시 읽을 수 있다.

자기 검산 10항목은 모두 통과했다. 이것은 별도 사람/독립 모델의 내용 검토가 아니다. 최초 보조 EPUB 파서의 fragment-only URL 처리 오류를 발견하여 현재 문서를 유지하도록 고쳤고 보조 원장을 다시 만들었다. Trees와 wheel의 선택·결론에는 영향이 없었다.
