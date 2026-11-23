# ggplot2 3.4.0 → 3.5.0 판독

> 후속 통합 검토: 이 문서와 프로젝트 원장의 57개는 단계3 작성자 집계다. 별도 검토가 098과 같은 빌드규칙 저작5개를 찾아 최종 신규 수는 GG52개로 조정했다. 원천 원장과 단계3 커밋은 보존하며, 최종 산입은 [root 조정 원장](../source-reconciliation.json)과 [root sources](../../sources.jsonl)를 따른다. 판독·표본·U/G 판정은 바뀌지 않았다.

## 봉인과 실측 범위

예측 원격 봉인은 `f1c5d6ff927fd5fbe108565598810ca7e94c5753`이며 root가 확인한 시각은 2026-11-23T22:07:47.803Z다. 첫 새 본문 수신은 **22:08:38.727319Z**, 첫 새 PNG는 **22:08:43.091201Z**다. 새 본문을 보기 전에 선정한 일반층 2·변경층 2, 부재층 결원 2를 유지했다. 보조 20개도 봉인한 순서 그대로 읽었으며 주 표본에 넣지 않았다.

[판별 12자리](lineage.csv), [전체 관측·비교](audit.json), [보조 20개](supplemental-audit.json), [반환 결정](returns.json), [자료 원장](sources.jsonl)에 연결된다. 12자리 중 실제 주 사례는 4쌍/8자리, 부재층의 2쌍/4자리는 결원이다.

| 주 사례 | 정확한 이전/새 Examples 절 | P/U/G(두 판) | 실제 비교 |
|---|---|---|---|
| GG-G1 expansion | L122–144 / L126–148 | YES / YES / 미확인 | 첫 cylinder 막대의 아래 여백0·위 여백10% 목적과 예제 코드 유지. PNG 바이트 변경. |
| GG-G2 geom_count | L213–251 / L212–250 | YES / YES / 미확인 | 첫 cty/hwy `geom_point()` 기준 산점도 유지. 뒤 count-size 그림과 구별. PNG 바이트 변경. |
| GG-C1 annotation_custom | L133–156 / L137–160 | YES / YES / 미확인 | 빈 패널 전체를 덮는 rounded grob 예제 코드·목적 유지. PNG 바이트 변경. |
| GG-C2 geom_histogram | L329–423 / L322–416 | YES / YES / 미확인 | diamonds carat 히스토그램 목적·예제 코드 유지. 일부 bin 높이는 시각적으로 달라 보인다. 동일 수치 출력이라는 주장은 하지 않는다. |

일반층과 변경층 각각 실제 양성2개이므로 **FNR = FN/(TP+FN) = 0/2 = 0%**다. 실제 음성은 각0개여서 **FPR = FP/(FP+TN)** 및 **특이도 = TN/(TN+FP)**는 산출 불가다. 부재층은 결원2개로 양성·음성 분모가 모두0이다. 이 관측률을 일반 링크의 성능이나 옛 경로 부재 조건의 이름 변경 탐지 성능으로 확대하지 않는다.

각 주 PNG는 실제 수신한 1400×866 PNG이며 HTML 표시 크기는 700×433이다. 양판 원주소·바이트 수·전체 SHA-256·HTTP/MIME·Git blob 일치는 [audit.json](audit.json)과 [영수증](receipts/)에 있다. 주 8개 PNG를 실제 이미지 도구로 보고 내용 역할을 대조했다. 픽셀 동등 검사·R 실행·브라우저 실행은 하지 않았다.

48개 판별 본문(주8+보조40) 모두 실제 표시 버전이 선택한3.4.0/3.5.0과 맞고, 모든 직접 추적 PNG가 해당 발행 트리 blob과 일치한다. 정확한 Examples 경계 안에서 img, srcset, picture/source, script, object/embed/iframe, inline SVG, data URI를 조사했다. 첫 그림의 srcset은0, 절 내 picture/script/inlineSVG/dataURI도 모두0이다. 상대 src는 본문 URL을 기준으로 해석했고 base 태그가 있는지도 확인했다. 이는 정적 발행 본문의 사용 판정이며 브라우저 동작 시험은 아니다.

## 변경층 신호가 말하는 것

새 트리에서 40/40 옛 자원 경로가 남고 40/40 대응 `man/*.Rd` blob이 달라졌으나, 그것이 40개의 논리 예제가 바뀌었다는 뜻은 아니다. 주4개의 실제 `\\examples{...}` 블록은 모두 같다. 첫 그림 이전의 코드·캡션과 실제 그림 역할도 함께 읽었다.

- GG-G1과 GG-C1의 Rd 차이는 roxygen의 원본 R 파일명 `.r`→`.R` 한 줄이다.
- GG-G2는 원본 파일명, aesthetic 링크, computed variables 설명과 seealso 링크가 바뀌었다. 예제 블록은 같다.
- GG-C2는 원본 파일명과 computed variables 설명 표현이 바뀌었다. 예제 블록은 같다.

`man/<page>.Rd`를 사용한다는 대응 규칙은 ① 단계에서 고정했다. 이후 직접 읽은 [pkgdown2.0.6 build-reference.R](https://github.com/r-lib/pkgdown/blob/f1ec1402acacaebb87a319d945383750d6d47f13/R/build-reference.R)의 L268–269에서 `man/topic$file_in`을 입력으로 하고, L359–365에서 examples를 처리함을 확인했다. 여러 R 원본 링크 중 첫 링크만 임의로 비교한 것이 아니다.

## 고정 20개 보조 탐색과 반례

| 요청한 유형 | 실제 결과와 분모 | 의미·한계 |
|---|---|---|
| ① 경로 있음 / 정확 절은 안 씀 | 보조20개 모두 정확 Examples에서 옛 자원 경로 참조1개 이상. 발견0/20. 주4개도 같은 양성. | 파일 잔류만으로 사용을 추정한 것이 아니라 각 절의 URI·코드를 열었다. 전체사이트 일반 오류율이 아니다. |
| ② 옛 경로 없음 / 새 이름·내장으로 계속 사용 | 고정 모집40개에서 경로 부재0. 해당 조건의 관측 분모0; 부재층2쌍 결원. | 옛 경로 부재를 조건으로 한 이름 변경·내장 사례의 탐지율은 산출 불가다. 이 조건부 결손을 일반층·변경층의 FNR과 혼동하지 않는다. 아래 coord_flip는 옛 경로가 남으므로 정확히 이 유형은 아니다. |
| ③ 이름·해시는 같으나 목적 변경 | 보조의 양판 동일 첫 PNG는 fortify.lm 한 쌍이며 잔차 진단 목적도 유지. 발견0/1. | 아래 동일 새 PNG 두 개의 서로 다른 코드 해석은 보조적 경고이며, 이름·해시가 모두 같은 양판 목적 변경 사례로 세지 않는다. |
| ④ 바이트가 달라도 절 목적 유지 | 주4/4, 보조19/20. | payload identity와 설명 목적 identity를 분리한다. 19/20을 일반 링크 오류율로 확대하지 않는다. |

### GG-S13 coord_flip: 목적과 구체적 방법을 함께 보존해야 하는 경우

① 단계에 고정한 목적은 **다이아몬드 가격 boxplot의 수평 배치**다. [3.4.0 Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/57852124c86f770dd443fcf5064d30ea320a4731/reference/coord_flip.html#ref-examples)의 첫 코드 L124–130은 `coord_flip()`을 쓴다. [3.5.0 Examples](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/coord_flip.html#ref-examples)의 첫 코드 L140–143은 x/y aesthetic을 맞바꾼 방법을 우선한다. 원래 `coord_flip()` 코드는 L145–149의 두 번째 블록에 계속 있으며 저자가 같은 그림을 만드는 방법이라고 연결한다. [새 Rd](https://github.com/tidyverse/ggplot2/blob/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/man/coord_flip.Rd)와 [NEWS L49–51](https://github.com/tidyverse/ggplot2/blob/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/NEWS.md)이 이 방법 변경을 교차 지지한다.

따라서 고정된 수평 boxplot 목적의 U는 YES다. 구체적 `coord_flip()` 방법을 지금 사용할 독자는 **새 두 번째 블록과 `coord_flip-2.png`**를 받아야 한다. 같은 목적이라는 이유로 옛 구현을 새 첫 코드와 같다고 표시하지 않는다.

새 [coord_flip-1.png](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/coord_flip-1.png)와 [coord_flip-2.png](https://raw.githubusercontent.com/tidyverse/ggplot2/392175bbb00b04025aa5d17a0c18b3896adeb40f/reference/coord_flip-2.png)는 **둘 다 38,884B·SHA-256 `5b83ffa8756ebf4b4fc3cad479388874578dc018d6dc72915b90660d4020d563`**다. 같은 바이트만으로 어느 코드 방법을 설명하는지 선택할 수 없다. 옛 `coord_flip-1.png`의 해시는 다르고 옛 경로는 새 판에도 남으므로 이 관측을 정확한 유형②·③의 적중으로 올리지 않았다.

facet_null과 benchplot 역시 판마다 동일한 mtcars 산점도 바이트를 서로 다른 설명 문맥에 쓴다. 전자는 기본 단일 패널, 후자는 벤치마크 실행 출력이라는 목적을 코드·본문으로 구별했다. 해당 두 같은 이미지의 중복 산입을 제거했다.

## 발행·공식 배포·생성의 연결

공식 gh-pages 발행 SHA와 source tag를 별도로 고정했다. 모든 선택 페이지의 버전 표시는3.4.0/3.5.0이다. raw 고정 HTML은 과거 발행 파일의 소스이며 렌더된 과거 사이트로 광고하지 않는다. 현재 tidyverse.org URL로 바꾸어 열지 않았다.

[CRAN3.4.0](https://cran.r-project.org/src/contrib/Archive/ggplot2/ggplot2_3.4.0.tar.gz) **3,148,426B/888멤버**, [CRAN3.5.0](https://cran.r-project.org/src/contrib/Archive/ggplot2/ggplot2_3.5.0.tar.gz) **3,564,967B/966멤버**를 직접 받았다. 각 DESCRIPTION 버전과 주4개 Rd를 읽고 태그 소스와 **8/8 바이트 일치**를 확인했다. generated reference HTML과 주 PNG 이름은 이 소스 패키지에 없다. 이 패키지 범위의 부재는 별도의 공식 웹 발행 트리 P=YES를 부정하지 않는다. [배포 감사](distribution-audit.json).

[3.4.0 workflow](https://github.com/tidyverse/ggplot2/blob/63125db184b6e7d5516007574b5d15acbfd8f470/.github/workflows/pkgdown.yaml)와 [3.5.0 workflow](https://github.com/tidyverse/ggplot2/blob/a6f1a7c845bfe056ef952b839d2fd65b888ab5cd/.github/workflows/pkgdown.yaml)는 pkgdown 사이트 빌드 호출과 docs→gh-pages 배포 단계를 나눈다. 발행본문은 pkgdown2.0.6/2.0.7로 표시한다. 해당 버전의 원본 코드도 별도 SHA로 읽었다.

- [build-github.R](https://github.com/r-lib/pkgdown/blob/f1ec1402acacaebb87a319d945383750d6d47f13/R/build-github.R) L19–35는 로컬 산출물 청소 후 사이트 빌드를 호출한다.
- [build.R](https://github.com/r-lib/pkgdown/blob/f1ec1402acacaebb87a319d945383750d6d47f13/R/build.R) L318–322,431–438은 전체 사이트의 lazy=FALSE 기본과 참조 빌드 전달을 보인다. build_reference의 개별 lazy=TRUE 기본만 떼어 이번 호출에 적용하지 않았다.
- [build-reference.R](https://github.com/r-lib/pkgdown/blob/f1ec1402acacaebb87a319d945383750d6d47f13/R/build-reference.R) L199–205의 man/figures 복사와 L359–365의 example 처리 경로를 구별한다.
- gh-pages 배포의 `clean:false`는 [지정된 action4.1.4 README L144](https://github.com/JamesIves/github-pages-deploy-action/blob/4.1.4/README.md)와 [v4.4.1 L129](https://github.com/JamesIves/github-pages-deploy-action/blob/v4.4.1/README.md)에서 목적지 잔류 파일 삭제를 끄는 설정이다. 로컬 빌드 디렉터리 청소와 목적지 청소는 다른 단계다.

그러나 위 규칙·generator label·발행 커밋·서로 다른 PNG 해시만으로 특정 실행이 새 바이트를 생성했다고 단정하지 않았다. **원본태그2+발행SHA2 각각의 Actions runs·check-runs·combined status**, 그리고 **2022-11-06..10 및 2024-02-22..25의 created-window**를 직접 조회했다. 총14조회는 HTTP200이나 각각 실제 항목0이었다. 실제 실행·output manifest·단계별 digest로 연결되는 기록을 확보하지 못했다. [검색 범위와 영수증](build-search.json). 보존 정책이 실제 원인인지도 확인하지 못했으므로 단순히 삭제되었다고 쓰지 않았다. 주8자리 G는 모두 **미확인**이다.

## 반환과 저비용 확인

[returns.json](returns.json)의 주4개는 **두 판 병기**다. 과거 인용은 고정3.4.0 Examples와 당시 PNG, 선택한 새판 이용은 고정3.5.0 Examples와 실제 참조 PNG를 제공한다. 여기서 새판은 2026년 최신 사이트라는 뜻이 아니다. 그림의 구현을 재현할 독자는 고정 Rd·소스 tag·workflow를 추가로 받아야 하며, 정확한 당시 빌드 재현에는 아직 없는 환경·실행·산출물 manifest가 필요하다.

설명만 읽으면 정확 본문 절 한 개로 충분하다. 그림 파일을 재사용하면 실제 연결 PNG 한 개를 추가한다. G 질문이 없다면 과거 job 조사까지 비용을 늘릴 필요가 없다. 방법 지정 요청인 coord_flip는 이름만 같은 첫 PNG를 반환하지 말고 저자가 연결한 두 번째 코드 블록과 그림을 제공한다.

경고 문구: **이 주소는 선택한 발행판의 HTML 소스/그림이며, 최신사이트나 당시 생성빌드 재현을 보장하지 않습니다.**

## 자료 수와 실행 한계

최종 원장240행, 보수적 고유1차자료57개다. 실제 본문24개·그림23개·release/publication/tree3개·빌드규칙5개·소스배포1개·변경기록1개다. 같은 페이지/그림의 두 버전은 한 저작으로 합쳤고 Rd와 렌더 본문도 별도 고유자료로 세지 않았다. 서로 다른 페이지의 동일 바이트(facet_null/benchplot)는 합쳤다. 상속3.5.0 발행자료·동일 규칙의 새 버전·빈job조회·자동 모집만 한 페이지는 최소량에서 제외했다. 이 수는 독립 사례나 독립 실험의 수가 아니다.

자체 점검은 봉인 파일 불변, 실제12자리(8관측+4결원), 20보조 고정 순서, 동일 예제 블록4/4,48 본문 버전·PNG Gitblob 연결, 조건별 분모를 확인했다. 본문·코드·PNG 직접 판독 외에 브라우저/R 실행, 역사적 생성job 재현은 하지 않았다. 이 작업자의 자기 검토를 독립 검토로 부르지 않는다.
