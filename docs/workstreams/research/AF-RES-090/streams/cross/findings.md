# Q7 — 본문·목록·자원을 연결하는 다른 분야의 실제 대조

이 묶음은 네 프로젝트의 16판독과 별도인 보조 조사다. 모든 UTC·HTTP 상태·MIME·응답 바이트·SHA256은 `evidence/XF-*.receipt.json`에 있다. 실제 열람은 HTTP/파일 파싱·두 이미지 시각 확인이며 IIIF viewer나 EPUB reader의 JavaScript를 실행한 시험은 아니다.

## 공식 규격과 실제 저작

| 제도·실제 저작 | 직접 연 연결 | 현재 관측 | 소프트웨어 도움말에 적용할 조건·한계 |
|---|---|---|---|
| IIIF Presentation3.0 + 공식 Cookbook0001 | [규격](https://iiif.io/api/presentation/3.0/#53-canvas) → [실제 manifest](https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json) → [실제 PNG](https://iiif.io/api/presentation/2.1/example/fixtures/resources/page1-full.png) | manifest1188bytes 안에 Canvas·AnnotationPage·painting Annotation이 내장됨. 이미지128352bytes, PNG1200×1800으로 선언과 일치. | 이미 내장된 설명은 재열람0으로 읽고 외부 이미지 URI만 다음 자원으로 취급한다. 전체 id의 응답상태를 일괄 성공조건으로 삼지 않는다. [XF-IIIF-SPEC/MANIFEST/IMAGE] |
| 같은 공식 manifest의 Canvas id | [Canvas URI](https://iiif.io/api/cookbook/recipe/0001-mvm-image/canvas/p1) | HTTP301 → `https://iiif.io//404.html`; 최종HTTP200·text/html이지만 `404 Page Not Found`다. | 목록의 id를 따로 열지 못하는 현재 사례다. 그러나 Canvas의 완전한 표현은 manifest에 내장돼 있고 이미지도 읽히므로 이 별도 URI 실패만으로 예제 실패를 주장하면 틀린다. [XF-IIIF-CANVAS] |
| Internet Archive의 실제 IIIF 사건61 | [발행자 저장소의 사건](https://github.com/internetarchive/iiif/issues/61) → [당시 제시한 manifest](https://iiif.archivelab.org/iiif/naeb-b101-f02-23/manifest.json)·[tile](https://iiif.archivelab.org/iiif/naeb-b101-f02-23$0/1024,2048,1024,1024/256,/0/default.jpg) | 2024-03-04 제보는 manifest를 이용한 viewer에서 tile404를 명시한다. 이번 old-host 두 요청은 proxy503이며 당시404를 재현한 것이 아니다. 댓글의 [새 tile 주소](https://iiif.archive.org/iiif/naeb-b101-f02-23$0/1024,2048,1024,1024/256,/0/default.jpg)는301 뒤 JPEG200·25134bytes. | 필수 외부 자원은 목록만으로 충분하지 않다는 실제 제보. 협력자는 예외가404로 처리될 수 있다고 정정했으므로 ‘경로 문자열 오타’나 ‘원이미지 소실’을 원인으로 확정하지 않는다. [XF-IIIF-INCIDENT/INCIDENT-COMMENTS/NAEB-MANIFEST/OLD-TILE/NEW-TILE] |
| EPUB3.3 + IDPF/W3C 샘플 Accessible EPUB3 | [2026-01-13 규격](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-manifest-elem) → [공개 릴리스 EPUB](https://github.com/IDPF/epub3-samples/releases/download/20230704/accessible_epub_3.epub) → `META-INF/container.xml` → `EPUB/package.opf` → `cover.xhtml` → `covers/9781449328030_lrg.jpg` | 4051892bytes ZIP,38entries. 실제 OPF35항목 모두 존재, spine22개, manifest의 remote href0. 표지 XHTML에는 인라인 CSS와 같은 패키지의 JPEG 한 개가 있다. | 다운로드한 패키지 안 표지 목적에는 외부 네트워크 자료를 더 줄 필요가 없다. 규격은 일부 원격 자원을 허용하므로 모든 EPUB이 자체완결이라고 일반화할 수 없다. [XF-EPUB-SPEC/PACKAGE/ROOT/OPF/COVER/COVER-IMAGE] |

## 같은 판과 같은 바이트를 나누기

[태그20230704](https://api.github.com/repos/IDPF/epub3-samples/git/ref/tags/20230704)는 `46d7e07e1b39b2d0a0245ececaf896edcd9de4b2`를 가리킨다. 그 고정 소스의 [package.opf](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/accessible_epub_3/EPUB/package.opf), [cover.xhtml](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/accessible_epub_3/EPUB/cover.xhtml), [JPEG](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/accessible_epub_3/EPUB/covers/9781449328030_lrg.jpg)을 별도로 읽어 실제 릴리스 ZIP 멤버와 비교했다.

| 파일 | 고정 Git 소스 bytes | ZIP 멤버 bytes | 원바이트 일치 | CRLF→LF만 정규화한 일치 |
|---|---:|---:|---|---|
| META-INF/container.xml | 263 | 269 | 아니오 | 예 |
| EPUB/package.opf | 5774 | 5867 | 아니오 | 예 |
| EPUB/cover.xhtml | 552 | 568 | 아니오 | 예 |
| EPUB/covers/9781449328030_lrg.jpg | 820269 | 820269 | 예 | 예 |
| EPUB/ch04.xhtml | 4614 | 4692 | 아니오 | 예 |

본문과 그림의 원지문을 따로 보존했다. JPEG의 SHA256은 `d86dc63631ad83ca6bd27dde379771b0ebd08c291b0de1ef368d1da952580af0`; ZIP 전체는 `67f75b8e3cd1abe4bb143d91d5424191d5af3115c9d26ff029a38e19f8d16feb`다. 줄바꿈이 다르다는 관측을 다른 내용판으로 단정하거나, 정규화 뒤 같다는 사실을 원바이트 동일로 바꾸지 않았다. 소스와 ZIP에서 같은 논리 파일은 자료 개수에 두 번 산입하지 않는다. [각 asset 행의 archive_* 필드]

## 두 방향 반례와 남은 빈칸

**싼 입구가 충분한 경우:** IIIF의 내장 Canvas는 manifest 한 파일로 기술 내용을 읽을 수 있다. Accessible EPUB3의 표지는 이미 내려받은 XHTML과 JPEG로 필요한 정적 내용을 갖춘다. 후속 파일을 별도 인터넷 링크로 반환하는 비용이 항상 필요한 것은 아니다.

**싼 입구가 부족한 경우:** 실제 IIIF 사건61은 외부 tile을 못 받는 문제가 manifest의 존재와 별개임을 보여준다. 이 세션은 제보 원문을 직접 읽었고 현재 대체 tile도 읽었지만, 예전404를 이번503과 같은 증거로 취급하지 않는다. 현재 필수 이미지 연결은2쌍을 시도했고 판정 가능한1쌍(Cookbook 정상), proxy 때문에 미확인1쌍(old IA)이다. 판정 가능한 현재쌍 중 필수 이미지 실패는 **0/1**, 과거 제보를 현재 old-host 응답으로 완결해 재현한 비교는 **0/0 산출 불가**다. 별도 식별자인 Cookbook embedded Canvas의 soft4041건과 필수 외부 자원 장애 제보1건도 나누어 보존한다.

[EPUB ch04](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/accessible_epub_3/EPUB/ch04.xhtml)는 로컬 이미지와 외부 O’Reilly 웹 탐색 링크를 함께 갖는다. 표지 목적의 내장 자원 충분성을 그 외부 링크의 생존까지 확대하지 않는다. 외부 shop 링크는 열지 않았으며 미확인이다. `epub-package-audit.json`의35/35는 **manifest가 선언한 파일 존재** 분모이지 누락된 선언까지 찾은 전체 의존성 검사나 reader 성공률이 아니다.

## 적용안

독자에게 반환할 본문 링크와 필요 자원 링크는 각각의 목적에 따라 고른다. 본문/인라인 payload에서 목적이 끝나면 하나만 반환하고, 실행/그림·재생 확인에 외부 자원이 필수이면 본문과 그 실제 자원을 묶는다. 발행자는 package/tree 목록, 상대 경로의 기준, 정적 payload 해시를 함께 보존할 수 있다. 그러면 목록의 존재·현재 도달·판 동일성을 각각 점검할 수 있다. 이 안은 JavaScript 실행이나 외부 서비스의 장기 제공을 보장하지 않는다.

## 다음 최소 관측

현재 필수 자원 실패를 직접 재현하려면 사건61의 old manifest와 정확한 tile을 정상 연결 경로에서 같은 UTC 구간에 읽어 두 응답의 MIME·body·status를 함께 확보한다. proxy503만 반복되면 ‘현재 원 서비스 실패’는 계속 미확인이다. 별도 EPUB reader가 실제로 표지와 로컬 JPEG를 표시하는지를 보려면 내려받은 동일 SHA256 ZIP을 사용하고 표시/JS 여부를 따로 기록한다.
