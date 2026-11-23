# 지금 반환할 네 답

관측 UTC는 응답 수신 완료 또는 명시한 요청 구간 기준이며 생성 시각·보관 시각과 구별한다. 네 답 모두 전체 assets·브라우저 JavaScript·과거 무중단 제공을 검사했다는 뜻은 아니다. 같은 목적의 사전 권고는 `586b33488f6338ee8309a671d270656d837df636:docs/workstreams/research/AF-RES-086/prerecommendations.json`에 고정돼 있다.

## P3 — v3.3.0의 enable 설정과 구계열 Python 안내

**반환 링크:** [cibuildwheel v3.3.0 options/#enable](https://cibuildwheel.pypa.io/en/v3.3.0/options/#enable), 지원 종료 Python 독자에게는 [1.x 문서](https://cibuildwheel.pypa.io/en/1.x/).

**볼 절:** 첫 링크의 `enable` 절에서 CPython 3.13 free-threading opt-in과3.14+ 기본 포함을 구별한다. 1.x root의 Python 표에는 CPython2.7·PyPy2.7이 있다. 현재 지원판의 사용법이 목적이라면 별도로 [stable/options/#enable](https://cibuildwheel.pypa.io/en/stable/options/#enable)을 읽는다. 현재 stable의 옵션 목록은3.3.0과 같지 않다.

**입증 가능한 시점:** 현재 두 응답의 수신 완료는2026-11-23T14:50:48Z. 역사 자료로 [stable/options 보관 응답](https://web.archive.org/web/20251114022628id_/https://cibuildwheel.pypa.io/en/stable/options/)은2025-11-14T02:26:28Z, [1.x 보관 응답](https://web.archive.org/web/20251114112800id_/https://cibuildwheel.pypa.io/en/1.x/)은2025-11-14T11:28:00Z다. stable/options와 현재 고정 options는 RTD version-slug 메타데이터 한 값만 다르고, 보관1.x는 현재1.x와 바이트 전체가 같다.

**보류한 주장:** 두 보관 응답은 주창2025-11-11~13 밖이며 같은 순간이 아니다. 따라서 당시 두 판을 동시에 제공했다는 주장, tag30298914·30298916 중 어느 실행이 각 파일을 만들었는지, 1.x의 영구 보존 약속은 유보한다. 같은 시점의 두 응답 또는 내용 지문을 갖춘 게시 구간 교집합이 필요하다.

**선택:** 고정판 유지. 새 근거는 보조 역사 응답과 별칭 내용 비교를 추가했으며 원 약속이나 관측창을 바꾸지 않았다. 근거: PY-P3-README, PY-P3-TAG-NOW, PY-P3-LEGACY-NOW, PY-CAP-STABLE-OPTIONS-20251114, PY-CAP-LEGACY-20251114.

## P1 — bandersnatch 7.0.1 문서

**반환 답:** 7.0.1 문서 링크 승인을 유보한다. [현재 latest 문서](https://bandersnatch.readthedocs.io/en/latest/)는8.2.0이다. 현재판을 읽는 별도 목적에는 쓸 수 있지만7.0.1이라고 소개하지 않는다. [named7.0.1](https://bandersnatch.readthedocs.io/en/7.0.1/)은현재404다.

**확인할 근거:** [선택 빌드 JSON](https://readthedocs.org/api/v3/projects/bandersnatch/builds/30720077/)과 [원 로그](https://app.readthedocs.org/api/v2/build/30720077.txt)의 Sphinx HTML 명령. 같은 source `7a9e6510ca2ca4535ba8ddd0c5e0bf1ee924af74`가 latest에서 HTML을 생성했다. 이 로그는 독자가 읽을 문서 본문을 대신하지 않는다.

**입증 가능한 시점:** 생성 명령2025-12-16T17:51:07.787761Z~17:51:12.494739Z, exit0. 현재 latest/named 응답 수신 완료2026-11-23T14:50:47Z.

**보류한 주장:** 대조창에 latest가7.0.1 내용을 반환했는지, named 경로가 과거에도404였는지는 미확인이다. 현재404에서 과거 생성 실패를 추론하지 않는다. 빌드30720077의 파일 manifest 또는 그 창의 내용 식별 가능한 HTML 응답을 확보하면 다시 판단한다.

**선택:** 유보 유지. 새 근거는 같은 소스의 생성 성공이며, 원 약속에는 named판 영구 보존이 없었다. 근거: PY-P1-README, PY-P1-BUILD, PY-P1-LOG, PY-P1-VERSION, PY-P1-LATEST-NOW, PY-P1-NAMED-NOW.

## R1 — archive 1.1.12의 archive_read

**반환 링크:** [1.1.12 생성 HTML 원문](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html), [HTML 다운로드](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html). 진입 페이지도 [고정 index HTML](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/index.html)에 보존돼 있다. **이 링크는 HTML 소스/다운로드이며 렌더링된 옛 사이트가 아니다.**

**볼 절:** navbar의 Released version1.1.12, `archive_read`의 Usage·Arguments·Examples. 선택 leaf의 SHA256은 `0c0efbe4b86a97aa6d5662af71fa2dd8bf04a91e6caf6793c08c5ccd407722b3`다. 발행자 Git blob 해시와 직접 계산한 Git blob 해시도 일치한다.

**입증 가능한 시점:** 생성 커밋의 발행자 기록2025-03-24T12:34:38Z. 연구자의 leaf 조회 구간2026-11-23T14:54:04.109964Z~14:54:09.776900Z. 현재 [공개 root](https://archive.r-lib.org/)와 [API 페이지](https://archive.r-lib.org/reference/archive_read.html)는1.1.14다.

**보류한 주장:** 선택 Pages2328795124는 입력SHA가 같고 inactive @2025-03-24T12:38:03Z 한 행이 남았지만, 이전 성공·실패 순서와 주창의 웹 응답은 없다. NEXT 생성12:37:22Z는inactive 직전, LAST16:07:18Z는이후이며 두 스냅샷의 정식 root·leaf는 그대로였다. 이것을 당시 제공 구간으로 읽지 않는다. 상태 전이·공개 경로·1.1.12 응답 지문이 연결되어야 과거 공개 제공을 승인한다.

**선택:** 유보→생성물. 당시 렌더링 서비스 보장은 계속 유보한다. 근거: R1-GENERATED-COMMIT·ROOT·LEAF, R1-DEPLOYMENT-STATUSES, R1-NEXT-ROOT·LEAF, R1-LAST-ROOT·LEAF.

## R2 — asciicast 2.3.1 예제

**반환 링크:** [현재 asciicast 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html). 역사 자료의 판을 고정하여 인용할 때는 [선택 생성 HTML 원문](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) 또는 [다운로드](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)를 함께 쓴다. 뒤의 두 주소는 렌더링된 옛 사이트가 아니다.

**볼 절:** Released version2.3.1, `init_knitr_engine` 예제, Caching, Using SVG files. 실제 JavaScript·SVG 재생 동작을 실행한 검사는 아니며 HTML의 절과 지문을 읽었다.

**입증 가능한 시점:** 현재 leaf 응답 수신 완료2026-11-23T14:49:29.299263Z. 선택 생성 커밋은2024-01-21T20:53:46Z다. 두 시점의 root·leaf 바이트는각각정확히같다. leaf SHA256은 `c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c`다.

**보류한 주장:** 이 일치는2024-01-21~24의 실제 공개 요청 응답, 연속 제공, 전체 asset 동작을 입증하지 않는다. Pages1283145596의 남은 inactive는20:58:36Z 한 행뿐이며 원 실행 로그는현재404다. 대조창의 경로 응답과 게시 상태 원행이 있어야 당시 제공을 말할 수 있다.

**선택:** 현재 예제 독자에게 이동 별칭 유지. 새 근거로 현재 두 파일의 정확한 바이트 일치 유보를 해소했다. 과거 제공 목적은 별도이므로 사전 권고 변경 건수로 세지 않았다. 근거: R2-CURRENT-ROOT·LEAF, R2-GENERATED-COMMIT·ROOT·LEAF, R2-DEPLOYMENT-STATUSES.
