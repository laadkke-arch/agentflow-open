# R 두 자리 — 고정 HTML과 다음 자료의 현재 읽기

## 실행 결과와 대조 분모

후속 후보는 `c2a3f387cc962abd1ef383e39f750cc23ee5e51a`에서 원격 봉인한 후 열었다. 주 분모는 네 목적의 A/B **8판독·4쌍**, 실제 문서/자원 열람은 **9회**, 응답 본문은 **683,868bytes**다. 각 판독은 최대2회이며 실패3개는 입구1회에서 끝났다. HTTP200 6응답·503 3응답이다. 최초 후보 봉인, 주작성자의 실제 브라우저 관측, fixed tree/source 대조는 주 분모 밖이다.

| 목적·경로 | 실제 순서·횟수 | 관측 | 본문판 / 후속 / 같은 판 |
|---|---|---|---|
| R1-body A | [현재 archive_read](https://archive.r-lib.org/reference/archive_read.html) 1회 | HTTP200; Released1.1.14, Usage/Examples 코드 읽힘 | refuted / NA / refuted |
| R1-body B | [고정 GitHub HTML](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) 1회 | 주 실행은 HTTP503 GitHub 오류형 HTML; 소스 미도달 | inaccessible / NA / unconfirmed |
| R1-next A | [현재 archive_read](https://archive.r-lib.org/reference/archive_read.html) → [system.file](https://rdrr.io/r/base/system.file.html), 2회 | Examples 첫 함수 링크의 실제 도움말200; 외부 R base 문서는 원문 링크에 판 고정 없음 | refuted / confirmed / unconfirmed |
| R1-next B | [고정 GitHub HTML](https://github.com/r-lib/archive/blob/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html) 1회 | HTTP503으로 봉인한 수동 URI 복사 단계에 도달하지 못함 | inaccessible / inaccessible / unconfirmed |
| R2-body A | [현재 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html) 1회 | HTTP200;2.3.1, #example의 init_knitr_engine와 #using-svg-files 읽힘 | confirmed / NA / confirmed |
| R2-body B | [고정 GitHub HTML](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) 1회 | HTTP503; 이 판독은 source 미도달 | inaccessible / NA / unconfirmed |
| R2-next A | [현재 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files) 1회 | 첫 인라인 pre 출력 읽힘, 추가0회. 실제 SVG/재생 payload 명시 경로 없음 | confirmed / no_explicit_path (static_output confirmed) / confirmed(HTML only) |
| R2-next B | [고정 GitHub HTML](https://github.com/r-lib/asciicast/blob/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html) 1회 | HTTP200 source 안 동일 정적 인라인 출력 읽힘, 추가0회 | confirmed / no_explicit_path (static_output confirmed) / confirmed(HTML only) |

HTTP503 세 응답은 `2026-11-23T16:36:22~16:36:41Z` 구간이며56,635bytes·SHA256 `5ea81d0616df061a931781c3bd05697a347da318f9871b9ca82e04a6b2467e0f`로 같다. 제목은 `Unicorn! · GitHub`, 서비스 오류를 알리는 짧은 문구와 GitHub Status 링크가 있다. 접근 제한이나 quota를 명시한 문구는 없었다. `server: envoy` 및 서로 다른 GitHub request ID는 남지만 발생 원인이 GitHub, 중계, 일시 상태 중 무엇인지는 미확인이다. 최초 봉인 시 같은 URL에서200을 받았고 별도 브라우저도 source를 읽었다는 사실을 main 실패 응답 대신 쓰지 않는다. 새 재조회는 새 UTC의 별도 관측이어야 한다. [R-R1-body-B-1; R-R1-next-B-1; R-R2-body-B-1]

엄격한 후속 자원축은 confirmed1, no_explicit_path2, inaccessible1, not_applicable4다. R2의 두 인라인 정적 출력은 별도 static_output=confirmed이며 SVG/재생 성공으로 합산하지 않는다. 교차검토에 따른 코딩 의미의 수정과 이전값은 evidence/R-coding-adjustment.json에 보존했다. 원 freeze·원본·요청 순서는 바뀌지 않았다.

## Q1–Q2: 원 목적과 봉인한 다음 자료

R1 [고정 DESCRIPTION](https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/DESCRIPTION)은 Version1.1.12와 archive 문서 root를 명시한다. archive_read의 Usage와 Examples를 그 판으로 읽으려는 목적, 첫 동작 참조를 추가로 읽는 목적은 이번 연구 조건이다. 발행자가 고정 HTML의 모든 외부 참조까지 같은 과거판으로 보장했다는 약속은 이 자료에 없다. [R1-DESCRIPTION]

R1의 봉인 범위는 `#ref-examples`다. 첫 동작 관련 href는 `system.file`의 `https://rdrr.io/r/base/system.file.html`이며 `read.csv`, `mtcars.csv` 또는 Arguments의 libarchive options를 먼저 선택하지 않았다. `system.file(package = "archive", "extdata", "data.zip")`의 data.zip은 설치된 R package의 로컬 경로 표현이며 웹 href가 아니다. Generated HTML은 `<base>`를 두지 않는다. [R1-FIXED-HTML; freeze.json]

R2 [고정 DESCRIPTION](https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/DESCRIPTION)은 Version2.3.1과 문서 root, screencast/SVG/knitr 기능을 기술한다. [고정 예제 HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)의 `#using-svg-files`에는 첫 `options(asciicast_knitr_svg = TRUE)` 설정과 두 정적 `div.asciicast > pre` 출력이 있다. 해당 절에 `<svg>`, `<img>`, `<object>`, `<iframe>`, cast JSON이나 player script가 없다. 그러므로 **인라인 출력의 정적 읽기는 확인**, **실제 SVG/재생 자원의 명시 경로는 없음**, **재생 성공은 미실시**다. 첫 options 함수 도움말은 SVG/재생 자원이 아니므로 후속 목표로 바꾸지 않았다. [R2-DESCRIPTION; R2-FIXED-HTML; R2-INLINE-STATIC]

## Q3–Q4: 소스 읽기, Raw, 상대 경로

GitHub blob URL의 HTTP200은 프로젝트 안내를 렌더링한 페이지가 아니라 GitHub 소스보기다. 첫 보조 관측의 embedded rawLines는 R2 전체286행이 Raw의 splitlines와 같고 R1은 끝의 빈 줄 한 줄만 생략했다. 브라우저에서 실제 source textbox와 Raw 버튼이 보였다는 주작성자 관측은 `streams/ui/freeze.json`에 별도로 있다. 원문 안 절대 URI는 그 source 화면의 진짜 `a[href]`가 아니므로 **완전 URI 복사**와 **상대 경로 조립**을 구별한다. R1의 봉인된 B-next 대안은 source에서 완전 URI를 수동 복사하는2회 경로였고 경로 재조립이 필요하지 않았지만, 본 실행의 입구503 때문에 실제 두 번째 요청은 없었다. Raw를2회째 열고 다시 후속에 가면3회가 되므로 main 성공으로 세지 않는다.

R2의 봉인된 관측 대상은 문서 안 정적 출력이며, 엄격한 SVG/재생 자원 목적은 명시 경로 없음이다. source view나 Raw가 source 텍스트를 제공해도 그 데이터는 같은 파일에 포함된다. 시각적인 애니메이션과 같은 성공은 주장하지 않는다. Raw MIME은 `text/plain; charset=utf-8`이며 source를 브라우저가 문서 HTML로 실행했다는 증거가 아니다.

## Q5: 같은 본문·다른 판, 같은 HTML·달라진 연결 원문

1. **판이 달라도 지정 코드 설명은 같은 실제 반례.** 현재 R1은1.1.14이고 고정 HTML은1.1.12지만 `#ref-usage`와 `#ref-examples`의 첫 pre에서 태그를 제거하고 HTML entity를 해제한 텍스트는 각각 완전히 같다. 정규화 SHA256은 Usage `6a00a56833cedbc969e8d61efd9c9728897be7567e28bc4b2cd0d7003adf7feb`, Examples `2af2944df4fb0981f7c0086e138046346742c9ff51782340e5b4f282a8e373b1`. 따라서 특정 코드 설명을 읽는 데 현재 입구가 충분할 수 있으나 지정판 인용 성공과 같지 않다. 전체 HTML이나 전체패키지 동작의 동일성으로 확대하지 않는다. [R1-ENTRY-A; R1-FIXED-HTML; evidence/R1-section-comparison.json]
2. **동일 HTML도 연결된 소스판을 고정하지 않는 실제 반례.** R2 current/fixed article은15974bytes·`c812426f5a97f8361e64a7a3beb8a35d5dde4bd2270b70dc1f1567080471ca0c`로 동일하다. 그러나 Source href는 [blob/HEAD/vignettes/asciicast-demo.Rmd](https://github.com/r-lib/asciicast/blob/HEAD/vignettes/asciicast-demo.Rmd)다. [선택2.3.1 source](https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/vignettes/asciicast-demo.Rmd)는4419bytes·`f8103ef0fa26552206305a84deab6362b19b27bbd6082f1555622b79d24cae1a`; [현재 소스를 a0076449에 고정한 파일](https://raw.githubusercontent.com/r-lib/asciicast/a0076449feec11c835ff46f7934fe75232f7d759/vignettes/asciicast-demo.Rmd)은4440bytes·`ed5e966fe593c9acdcf730b45f36db04ecfdb7ad4f5a2cd0fcacb1c646849cc5`다. R chunk 옵션이 `#|` YAML 줄로 바뀐 원문을 직접 읽었다. 현재 HEAD 응답과 이 고정 파일도 일치했다. 이는 **Source 링크의 commit/bytes 변화**이며 named package version이나 생성 HTML의 당시 배포 이력 변화를 추정하지 않는다. 주 목적의 SVG 자원을 이 Source 링크로 교체하지 않았다. [R2-RMD-FIXED; R2-RMD-HEAD; R2-RMD-HEAD-PINNED; R2-SOURCE-HEAD-COMMIT]
3. **추가 파일이 실제 같은 경우도 보존.** [init_knitr_engine fixed HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/reference/init_knitr_engine.html)과 [현재 reference](https://asciicast.r-lib.org/reference/init_knitr_engine.html)는10917bytes·`dac96abf66bbf0b253a9f23d924690e3269669759c42ec4a96c8d1ff947d98b5`로 같다. [fixed pkgdown.js](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/pkgdown.js)와 [현재 script](https://asciicast.r-lib.org/pkgdown.js)도4406bytes·`603f213b0cd6f3eef19593be002356296c20ab4dc9a81f39c4b98a4099eae722`로 같다. 각각 고정 tree의 Git blob SHA1과 실제 계산도 맞는다. 두 파일의 일치는 모든 assets의 동일성이나 JS 실행 성공이 아니다. [R2-REFERENCE-*;R2-PKGDOWN-*]
4. **정적 본문은 충분하지만 수동 웹 경로가 실패하는 보조 사례.** R2 `#casting-a-script-from-a-file`의 문자 `../inst/examples/hello.R`을 문서 URL 기준으로 조립한 [웹 경로](https://asciicast.r-lib.org/inst/examples/hello.R)는404였다. 이는 원래 클릭 가능한 링크가 아니다. 생성 tree442항목에 파일이 없지만 [고정 source tree의22byte script](https://raw.githubusercontent.com/r-lib/asciicast/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/inst/examples/hello.R)는 존재하고 `print("Hello world!")`를 읽었다. 본문의 인라인 Hello world 출력은 후속 파일 없이도 읽힌다. selected SVG 목표를 이 예제로 바꾸지 않았다. [R2-HELLO-WEB-LITERAL;R2-HELLO-FIXED;R2-GENERATED-TREE;R2-SOURCE-TREE]
5. **파일 존재와 독자 도달은 별개.** R1 selected source의 [data.zip](https://raw.githubusercontent.com/r-lib/archive/a4c6ec37fc8737a189ca7ec7095ec0161888f9e8/inst/extdata/data.zip)은929bytes, 세 CSV 멤버가 있고 예제에 출력된 열·첫 행과 대응한다. generated docs tree에는 이 ZIP이 없다. 이것은 원래 frozen next(system.file 도움말)를 대신한 성공이 아니고 source package 자원의 별도 보조 확인이다. [R1-DATA-ZIP;R1-SOURCE-TREE;R1-GENERATED-TREE; evidence/R1-zip-members.json]

## Q6: 바로 반환할 수 있는 범위

- **R1 현재 사용 설명:** [현재 archive_read의 Usage/Examples](https://archive.r-lib.org/reference/archive_read.html#ref-examples)만으로 코드와 결과를 읽을 수 있다. 현재1.1.14이며 코드텍스트가 selected1.1.12와 같다는 관측까지 말할 수 있다. 이를1.1.12 문서라고 표시하지 않는다.
- **R1 과거판 인용:** [고정 Raw HTML](https://raw.githubusercontent.com/r-lib/archive/45e0d9ebc168cf3632bc2d737c9db2318668a826/reference/archive_read.html)을 source text로 반환하면 보조대조에서1.1.12의 본문이 확인됐다. GitHub blob의 이번 main503 및 별도 browser200을 함께 남긴다. 시스템 파일 찾기 동작이 필요한 독자에게 [실제 첫 도움말](https://rdrr.io/r/base/system.file.html)을 추가하되 build-time R 판까지 고정됐다고 말하지 않는다. [현재 공식 R base4.6.0 도움말](https://stat.ethz.ch/R-manual/R-devel/library/base/html/system.file.html)은 설명의 원저작 대조이며 옛 R 판의 증거가 아니다.
- **R2 정적 사용법과 출력 읽기:** [현재 예제](https://asciicast.r-lib.org/articles/asciicast-demo.html#using-svg-files) 한 링크로2.3.1의 설정·정적 출력까지 읽힌다. 고정 인용이 필요하면 [fixed HTML](https://raw.githubusercontent.com/r-lib/asciicast/92fecbc0ce019cc03086d5fc3f5b9e1a788a84c1/articles/asciicast-demo.html)을 사용한다. 추가 SVG 주소를 만들어 제공하지 않는다.
- **R2 source 재사용 독자:** article의 HEAD 링크 대신 [선택 release source](https://github.com/r-lib/asciicast/blob/f992b26f3cb30c799fbb95f6148852d8ae8a7f18/vignettes/asciicast-demo.Rmd)를 추가할 이유가 있다. 이 경우 두번째 자료가 필요한 이유는 실제로 달라진 source를 재사용하기 위해서다. 정적 예제만 읽는 독자에게는 불필요한 추가 링크다.

## 기록 비용·범위와 재검산

이 stream은33개 직접 HTTP 응답·1,754,371본문bytes를 계측했다. 그중9회·683,868bytes가 주 판독이다. 헤더/TLS/브라우저 자동 assets 및 주작성자의 UI 비용은 이 수치에 포함하지 않는다. 사람 소요 시간은 측정하지 않았다. 자료 원장33행 중17자료가 적격이며17개는 publisher_source7, followup_resource5, supporting_manifest5로 나뉜다. 후자의5개는 요구한 네 종류 최소24개 구성에서 별도 부가 자료로 처리할 수 있다. 독립 계보는 archive·asciicast·R base manual의3개다. GitHub/Raw, current/fixed 동등 bytes, 재조회, 오류응답은 추가 적격 수로 올리지 않았다.

각 HTTP 응답은 receipt로 UTC·주소·상태·MIME·bytes·SHA256·Git blob SHA1을 남겼으며, 공개 영수증에서는 cookie 및 무관한 session/policy 헤더를 제거했다. SHA는 응답 entity 전체를 읽어 계산했지만 원 전체페이지를 결과 원문처럼 다시 게시하지 않고 짧은 발췌·관측·지문을 보존한다. `evidence/raw/`는 임시 계산 캐시다. tree 완전성, hash·ZIP 멤버·주판독 행수 및 예산은 별도 `evidence/R-validation.json`으로 확인한다. 이 검산은 사실 전체, rendered UI, R 또는 JavaScript 실행을 검증하지 않는다.

## 남는 핵심 미확인

- GitHub503 세 판독: 원인·지속기간 미확인. 다음 입력은 같은 blob 주소이며 새 UTC의 source 응답이 있어야 새로운 독자 도달 판단이 가능하다. 이미 실패한 분모를 덮어쓰지 않는다.
- R1 system.file의 build-time R판: external URI에 판이 없고 package Depends도 최소판 조건이다. 발행자 고정 R판과 그 manual 원문 지문이 있어야 같은 빌드의 후속이라고 판단할 수 있다.
- R2 SVG/재생 payload: 현재 selected 절의 정적 출력만 있다. 실제 SVG XML/cast JSON 또는 발행자가 고정한 player 자원을 추가 관측해야 재생 자료가 보존됐다는 판단을 할 수 있다. 그 전에는 정적 읽기 확인과 실행 미확인을 유지한다.
