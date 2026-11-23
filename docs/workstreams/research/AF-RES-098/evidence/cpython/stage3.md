# CPython: ③ 정적 참조·실물·발행 계보 판별

② 예측은 `0df9ea9edbcee995d631eef54b65fd43f73c245f`에서 원격 봉인됐다. 그 뒤 첫 새 본문 요청은 **2026-11-23T19:46:14.413029Z**다. [lineage.csv](lineage.csv)는 주 4자리, [audit.json](audit.json)은 속성·지문·판정·비용을 담는다. 예제 프로그램 실행, Python 문서 재빌드, 브라우저 런타임 네트워크 계측은 하지 않았다.

**정정:** ① `stage1.md`의 PY2 치수 `500×322`는 사람이 작성한 요약의 오기다. 원 `selected.json`, 원 PNG IHDR 및 이번 재확인은 모두 **500×320**이다. 별도 AI 교차검토가 이를 발견했다. 봉인된 ① 파일은 보존하며 최종 판정에는 500×320을 사용한다.

## 네 자리의 세 축

P=정확한 판에 포함, U=정확한 절에서 사용, G=이번 빌드가 이 바이트를 생성.

| 자리 | 생성 본문의 참조·범위 | 직접 받은 payload와 ZIP 멤버 | P / U / G |
|---|---|---|---|
| PY1·3.12.0 | [Logging Flow](https://docs.python.org/release/3.12.0/howto/logging.html#logging-flow), HTML 612행 `../_images/logging_flow.png` | [PNG](https://docs.python.org/release/3.12.0/_images/logging_flow.png), 955×758, 21,907B, SHA256 `70d752f336a9ee7af4a56b8e5b3696b962b69793b274f76439165823c69cf5e0` | YES / YES / UNKNOWN |
| PY1·3.12.1 | [Logging Flow](https://docs.python.org/release/3.12.1/howto/logging.html#logging-flow), HTML 613행의 같은 src | [PNG](https://docs.python.org/release/3.12.1/_images/logging_flow.png), 위와 같은 바이트 | YES / YES / UNKNOWN |
| PY2·3.12.0 | [Creating hash objects](https://docs.python.org/release/3.12.0/library/hashlib.html#creating-hash-objects), HTML 705행 `../_images/hashlib-blake2-tree.png` | [PNG](https://docs.python.org/release/3.12.0/_images/hashlib-blake2-tree.png), **500×320**, 11,070B, SHA256 `382828d64e88644e47e695d717ea8432ec1ef79a17f2d209b11aef4fdbfa4bf5` | YES / YES / UNKNOWN |
| PY2·3.12.1 | [Creating hash objects](https://docs.python.org/release/3.12.1/library/hashlib.html#creating-hash-objects), HTML 706행의 같은 src | [PNG](https://docs.python.org/release/3.12.1/_images/hashlib-blake2-tree.png), 위와 같은 바이트 | YES / YES / UNKNOWN |

네 HTML·PNG 직접 URL은 모두 200이며 해당 문서/이미지 GET에는 리다이렉트가 없다. 각각 같은 판의 공식 ZIP 멤버와 바이트가 같다. ZIP 다운로드 URL은 docs.python.org에서 www.python.org로 301 이동한다. 모든 문서에 base 요소가 없으므로 문서 URL 기준 상대참조를 해석했다. MIME은 실제 HTTP `image/png`, 내부 signature도 PNG다. 두 정확한 절 전체의 `img src/srcset`, `picture/source`, `href` 및 다운로드·data 속성, data URI, inline SVG, script를 조사했다. 각각 img 1개이며 picture/source/script/inline SVG/data URI는 0이다. PY2에는 기존 설명의 문서·외부 규격 href가 있지만 다른 이미지 선택 로직은 없다. 이 범위에서 JS가 정한 이미지 요청을 주장하지 않는다.

두 **사전 U 예측은 참 2/2**, 거짓·유보·관측 불가 0/2다. 본 연구 전체의 6쌍 분모는 그대로 유지해야 하며 CPython 성적을 전체 발행 문서의 정확도로 일반화하지 않는다.

## P와 U가 있어도 G가 남는 이유

고정 소스 커밋은 [3.12.0 `0fb18b02…`](https://github.com/python/cpython/tree/0fb18b02c8ad56299d6a2910be0bab8ad601ef24)과 [3.12.1 `2305ca51…`](https://github.com/python/cpython/tree/2305ca51448552542b2414186252123a8dc87db7)이다. Git 태그를 실제 조회해 각각의 peeled commit/직접 commit을 확인했다.

- [logging.rst 420행](https://github.com/python/cpython/blob/2305ca51448552542b2414186252123a8dc87db7/Doc/howto/logging.rst#L420)과 [hashlib.rst 466행](https://github.com/python/cpython/blob/2305ca51448552542b2414186252123a8dc87db7/Doc/library/hashlib.rst#L466)은 이름 있는 PNG를 각각 image/figure 지시문으로 참조한다. 두 판의 이 소스 파일은 배포 ZIP `_sources/...rst.txt`와 **4/4 일치**한다.
- 해당 태그의 원 PNG와 실제 HTTP/ZIP 출력은 **4/4 일치**한다. 더 이전 [3.11.0 소스의 logging PNG](https://raw.githubusercontent.com/python/cpython/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/howto/logging_flow.png)와 [BLAKE2 PNG](https://raw.githubusercontent.com/python/cpython/deaf509e8fc6e0363bd6f26d52ad42f976ec42f2/Doc/library/hashlib-blake2-tree.png)도 같은 바이트다. 그러므로 현재 참조는 예전 바이트의 실제 재사용과 양립한다.
- HTML footer는 두 판 모두 Sphinx 4.5.0이라고 표시한다. [Sphinx 4.5.0 HTML builder의 719–729행](https://github.com/sphinx-doc/sphinx/blob/v4.5.0/sphinx/builders/html/__init__.py#L719)은 소스 그림을 출력 이미지 디렉터리로 복사한다. [3.12.1 Doc/Makefile 169–179행](https://github.com/python/cpython/blob/2305ca51448552542b2414186252123a8dc87db7/Doc/Makefile#L169)은 HTML을 만들고 `build/html`을 판 이름을 가진 배포 디렉터리로 복사해 ZIP을 만든다. 이는 보존된 정적 그림이 새 판의 정당한 설명 자료가 될 수 있는 구체 경로다.
- `.buildinfo`는 두 판의 config hash와 동일한 tags hash를 담는다. **이미지별 지문이나 생성 job ID를 담지 않는다.** 3.12.1 footer는 2023-12-07 20:47 UTC, 릴리스 공개일은 12월 8일이다. footer·mtime·같은 SHA만으로 실제 이미지 생성 시각을 판정하지 않는다.

특정 실행이 두 PNG를 만들었다는 로그나 이미지별 산출물 manifest는 확보하지 못했다. 바이트가 이전판과 같다고 **이번에 동일하게 재생성되지 않았다**고 단정할 수도 없다. 따라서 정확한 표현은 ‘이 판에 포함되고 이 절이 사용함; 기존 소스 그림과 같은 바이트이며 복사 규칙이 있음; 이번 생성 job은 미확인’이다.

## 캐시·복사·잔류 가능성의 별도 규칙

공식 [docsbuild-scripts의 역사 README](https://github.com/python/docsbuild-scripts/blob/f0a570aec824c7d775ea9d345a89d1b10d0f11b2/README.md)는 docs.python.org 자동 발행용 저장소임을 밝힌다. 3.12.1 footer 시각 이전의 마지막 공개 커밋을 찾아 [build_docs.py](https://github.com/python/docsbuild-scripts/blob/f0a570aec824c7d775ea9d345a89d1b10d0f11b2/build_docs.py)를 읽었다. **이 커밋이 해당 릴리스 서버에서 실행됐다는 증거로는 사용하지 않는다.**

649–661행의 실행 경로는 branch/tag 선택 뒤 필요한 경우만 빌드·발행한다. 920–949행은 문서 소스가 변하지 않으면 재빌드를 건너뛸 수 있다. 853–872행의 full publish에는 삭제 옵션이 있고 partial publish에는 없다. 960–980행의 로컬 state는 CPython SHA와 빌드 시간을 기록하지만 이미지별 생성 지문은 기록하지 않는다. 이는 존재 목록이 사용/신규생성과 다를 수 있는 **공식 구현 경로**다. 이 규칙만으로 선택된 두 ZIP에 잔류물이 있었다고 주장하지 않는다.

## 반례 탐색

| 유형 | 실제 확인 | 범위·한계 |
|---|---|---|
| 같은 이름·다른 바이트 | [2018 optipng](https://github.com/python/cpython/commit/c6cd164cffedb306a4c6644d9d03072f24da246d)와 [2022 IMGbot](https://github.com/python/cpython/commit/ba650af7d660084e08859dd1ee1917cccee24e88). `logging_flow.png`는 22,058→21,907B, BLAKE2 PNG는 11,146→11,070B이고 SHA256도 각각 다르다. | 압축·최적화 사건이다. 그림 의미가 바뀐 사례라고 확대하지 않는다. 주 6쌍 외 보조 사건 1개이며, 파일 2개를 독립 발행 사건 2개로 부풀리지 않는다. |
| 이름 변경·같은 바이트 | 두 PNG 경로의 v3.12.1까지 GitHub history는 각각 3개 커밋. 최초 등장·2018·2022의 파일 상태를 읽었다. | 최초 [logging 2013](https://github.com/python/cpython/commit/f186911e247b287d555852ce73afb721f8eb79b9)와 [BLAKE2 2016](https://github.com/python/cpython/commit/121b9487d13b7dcd5a864a6067c4a5c88ba15b5d)은 `added`, 최적화는 `modified`; 해당 파일 `previous_filename` 없음. 이 좁은 범위에서는 rename+same-byte 사례를 확보하지 못했다. 저장소 전체 부재 주장은 아니다. |
| 옛 파일의 현재 의도적 사용 | 이전 3.11.0 source PNG와 3.12.0/1의 src·payload 일치; 복사 규칙 확인. | 오래된 바이트임을 이유로 현재판 추천을 거부하면 이 양성을 놓친다. G는 여전히 유보한다. |
| 잔류·참조 소멸 / 내장 data URI | 선택된 네 절에서는 관측하지 않았다. 위 partial publish 규칙에는 잔류 가능성이 있다. | 실제 잔류 사건으로 세지 않는다. 교정 사건/다른 분야 사례와 분모를 분리한다. |

첫 세 GitHub commit 상세의 직접 REST 요청은 403이었다. 같은 공개 commit을 승인된 GitHub connector로 읽어 추가·수정 상태를 확인했다. 실패와 해결 경로 모두 [영수증](stage3-http-receipts.json)에 남기고 실패를 자료 수에서 뺐다. 역사 README 확장자를 `.rst`로 시도한 404도 남겼으며 실제 `.md` 원문을 확인했다.

## 목적별 반환

개발자가 Logging Flow 그림을 이해하려면 판을 명시한 [3.12.1 본문](https://docs.python.org/release/3.12.1/howto/logging.html#logging-flow) 하나가 첫 링크다. 그림 파일 자체를 저장·사용할 목적이면 [3.12.1 PNG](https://docs.python.org/release/3.12.1/_images/logging_flow.png)를 추가한다. 이 경우 정확한 현재 참조와 사용 가능한 실물은 확인됐고 생성판만 미확인이다.

과거판을 인용하는 독자에게는 [3.12.0 본문](https://docs.python.org/release/3.12.0/howto/logging.html#logging-flow)을 우선하고 필요하면 같은 판 ZIP/지문을 준다. 새 판과 PNG가 같다는 이유로 인용 본문의 판을 바꾸지 않는다. 발행 재현이 목적이면 ZIP, 고정 소스, 빌드 규칙이 필요하지만 이것만으로 특정 생성 job의 재현을 완료했다고 말할 수 없다. 매번 세 링크를 주면 단순 독자에게 소스·job 조사 비용을 전가한다. 본문 하나만 주면 파일의 판·지문·포함 여부를 독자가 따로 찾아야 한다.

## 수·검산·재현

현재 이 부분 원장은 43행이며 보수적 고유 자료는 **20개**다. 실제 선택 본문은 **2개**, PNG payload는 현재 2개와 인코딩이 다른 2018판 2개로 **4개**다. 새판 HTML은 wrapper와 footer가 달라 전체 지문이 다르지만 두 주 본문은 각각 이전판과 정확히 같다. 새판 본문 2개와 PNG 2개를 중복 산입하지 않았다. 소스 rst도 같은 저작의 별도 표현으로 하한에서 제외했다. 두 이미지 최적화를 하나의 발행 사건으로 묶는다.

주 판별의 직접 HTTP 본문/이미지 요청은 **8회**, 공식 ZIP 다운로드는 **2회**다. 후보 자동 탐색은 옛 ZIP의 **515 HTML**을 읽었고, 사람이 자세히 읽은 자료수와 구별한다. 감사에 읽은 내부 고유 멤버는 옛 판 520개(515 HTML+2 PNG+2 rst+1 buildinfo), 새 판 7개(2 HTML+2 PNG+2 rst+1 buildinfo)다. 반복 I/O 호출 수가 아닌 **고유 멤버 수**다. 주요 내용 외 HTTP/connector 요청 수와 실패는 `audit.json.cost`의 명시된 영수증 범위에서 센다. 사람 클릭 수·시간은 측정하지 않았다.

공유 가능한 재현 명령은 다음과 같다. 첫 명령은 저장한 네 행과 속성·지문·판정을 검산한다. 두 번째 명령은 정확한 HTML/PNG/ZIP/소스 URL을 직접 다시 열어 저장 지문과 비교한다. 두 번째 네트워크 재확인은 이번에 반복하지 않았다. 오류 시 접근 실패를 해결한 후 같은 입력을 다시 사용해야 하며 실패를 자원 부재로 해석하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-098/evidence/cpython/verify_lineage.py
python -B docs/workstreams/research/AF-RES-098/evidence/cpython/verify_lineage.py --network
```

저장 근거 검산은 실제 **종료 0**이었다. `build_stage3.py`는 수집 시 임시 캐시에서 기록을 생성한 분석 도구다. 원래 실행 중 최초 commit 상세 응답 파일이 403으로 없어서 첫 시도는 종료 1이었다. connector로 실제 원문을 확인한 뒤 작은 속성 발췌를 저장하고 다시 실행해 4행, P=4 YES, U=4 YES, G=4 UNKNOWN, 사전 예측 참 2/2를 출력했다. 이 처리는 예제·발행 코드를 실행하지 않는다. 원 외부 저작 전체는 커밋하지 않았고 영수증에는 재열람 URL·길이·지문이 있다. connector 메타데이터의 원 HTTP 바이트 지문은 제공되지 않아 null로 남긴다. `build_stage2.py`는 사전 목록 단계 재현용이므로 사후 검산에서 봉인 예측을 덮어쓰지 않는다.
