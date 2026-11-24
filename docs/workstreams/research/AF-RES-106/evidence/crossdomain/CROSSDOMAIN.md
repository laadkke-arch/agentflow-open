# AF-RES-106 Q7 — IIIF와 JATS의 링크 충분조건 대조

## 범위와 수록량

이 부분은 `/root/crossdomain`의 별도 1차 자료 판독이다. 주 표본의 ggplot2·Matplotlib 새판 본문을 열지 않고 수행했다. 같은 모델 계열의 분담 조사이며, 주 12쌍의 독립 재채점이나 다른 사람의 검토가 아니다. **주 표본의 오류율·실제 양성/음성 분모에 이 사례들을 합치지 않는다.** 두 박물관의 현재 manifest와 한 수학·그래프이론 논문의 현재 XML/HTML을 비교했다. 시간에 따른 이동·삭제 실험으로 확대 해석하지 않는다.

102의 고정 입력 `092f4c5c56451bceb53e632f4bddf33db6cda168`에 있는 `sources.jsonl` 477행을 확인했다. 이전 타 분야는 EPUB/Wheel 16행이며 IIIF/JATS URL 계보는 없었다. 확인 결과는 [inherited-crossdomain-exclusions.json](inherited-crossdomain-exclusions.json)에 남겼다.

| 구분 | 직접 수신한 서로 다른 URL | 고유 신규 1차 저작 산입 | 근거와 제외 |
| --- | ---: | ---: | --- |
| IIIF Presentation 3·Content State 1 | 2 | 2 | 서로 다른 규격. Presentation의 Canvas/AnnotationPage/thumbnail 앵커들은 합쳐 1개 |
| Rijksmuseum 공식 튜토리얼·Night Watch manifest·두 이미지 | 4 | 2 | 별도 기술 안내 저작 1개와 실제 소장품 manifest 1개. 두 크기의 그림은 같은 작품의 파생물로 제외 |
| Fitzwilliam portrait manifest·face micrograph manifest | 2 | 1 | 같은 소장품/묶음의 하위 micrograph는 중복 제외 |
| JATS 1.3 fig·xref 규격 | 2 | 1 | 두 요소 페이지를 동일 JATS 1.3 규범 저작으로 합침 |
| PLOS 수학·그래프이론 논문 XML·HTML·Fig 7·Fig 8 | 4 | 1 | 같은 논문의 표현·그림들. 원 논문 XML 하나만 산입 |
| **합계** | **14** | **7** | 성공 URL 14개와 독립 사례 수는 같지 않다. 정적 스캔 32개 Annotation·20개 xref를 자료 수로 늘리지 않음 |

자료별 원본 URL, 수신 UTC, SHA-256, 판독 위치, 한계와 산입 사유는 [sources-crossdomain.jsonl](sources-crossdomain.jsonl)에 있다. 전송 실패와 성공은 분리했다. 초기 web open 실패 및 Micrio 기본 User-Agent의 403은 [probe-failures.json](probe-failures.json)에 남겼고 고유 자료에 포함하지 않았다. 이후 일반 연구 User-Agent GET은 200으로 수신되었다. 전체 raw 원문·JSON·XML·선택 그림은 이 폴더에 보존했다. 불변 발행 URL이 보장되지 않는 현재 자료는 보존 bytes와 SHA-256을 근거로 삼는다.

## 1. 박물관: 포함된 그림과 Canvas에서 쓰는 그림

| 대상 / 직접 연 원문 | 확인한 관계와 값 | 반례·미확인 | 충분한 반환 위치 / 비용 |
| --- | --- | --- | --- |
| [IIIF Presentation 3.0](https://iiif.io/api/presentation/3.0/#53-canvas), [AnnotationPage](https://iiif.io/api/presentation/3.0/#55-annotation-page) | Canvas는 뷰/좌표 기준이다. Canvas `items`→AnnotationPage `items`→`motivation: painting` Annotation→`body`가 표시 자원을 연결하며 `target`이 Canvas를 지정한다. `thumbnail` 및 `annotations`는 다른 관계다. | JSON 안에서 Image URL을 찾았다는 사실만으로 Canvas painting 사용을 판정할 수 없다. 규격을 읽은 것은 viewer 실행 확인이 아니다. | 규격 앵커 두 개는 같은 저작 하나. 실제 출력은 아래 manifest/Canvas payload로 연결 |
| [Rijksmuseum 공식 안내](https://data.rijksmuseum.nl/tutorials/iiif/), [Night Watch 실제 manifest](https://iiif.micr.io/PJEZO/manifest) | 1 Canvas, 1 AnnotationPage, 1 painting Annotation. 실제 body는 `/PJEZO/full/1024,/0/default.jpg`; target은 `/PJEZO/canvas`. 별도 `thumbnail`은 `/PJEZO/full/80,100/0/default.jpg`이고 painting body가 아니다. | 두 파일은 같은 작품이지만 다른 용도·크기다. body의 수신 이미지 1024×850과 manifest에 적힌 body 치수 14645×12158도 다르다. 이 차이는 정적 관측이며 viewer의 치수 처리 오류를 실측한 것은 아니다. | manifest+Canvas 쌍. 최초 목록 신호 뒤 추가 GET 3회: manifest 1+선택 body 1+thumbnail 1. 공식 안내는 출처 연결용 별도 1회 |
| [Fitzwilliam portrait 실제 manifest](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json) | 1 Canvas의 painting body는 `Choice`; Natural Light, Raking Light, Infrared, Ultraviolet, X-ray, MA-XRF 등 **17** 이미지 선택지다. commentary page에는 **32** Annotation이 있고 모든 `target`의 fragment가 `xywh=null,null,null,null`이다. | 수록된 17개가 전부 기본 화면에 그려진다고 볼 수 없다. 원문 summary는 자연광의 색 손실과 UV에서의 형광·보수 흔적을 달리 설명한다. 동일 작품이라는 사실이 관측 방법·독자 목적 동일성을 보장하지 않는다. null 좌표를 숫자로 추정해 자동 교정하지 않았다. 실제 viewer의 choice UI와 좌표 fallback은 **미확인**. | 작품 전체 Canvas는 반환 가능. 정확 얼굴 영역 또는 UV 선택을 보장하는 링크는 **유보**. parent의 잘못된 좌표 대신 별도 face micrograph manifest가 확인됨. parent manifest 후 추가 GET 1회 |
| [Fitzwilliam face micrograph 393](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/micrograph/393/manifest.json) | 독립 하위 Manifest와 `/micrograph/393/canvas/0`가 있으며 한 face TIFF를 painting하는 구조다. parent comment의 링크에서 추적했다. | 이것은 parent Canvas의 올바른 좌표를 복원한 것이 아니다. 얼굴 확대라는 유사 목적의 별도 뷰다. 실제 TIFF 수신·웹 표시·원 그림과의 정합은 **미확인**. 같은 소장품 묶음이므로 추가 고유 자료로 세지 않음. | 정확 하위 Manifest+Canvas payload 보존. parent에서 얼굴 위치를 반드시 보여야 하는 요청이라면 아직 충분하지 않음 |

Rijksmuseum 두 JPEG를 디코드하고 로컬 이미지로 직접 확인했다. painting body는 넓은 작품 전체 이미지이고 thumbnail은 80×100의 작은 preview다. 여기서 `P=YES`는 수신/manifest 관계에 대한 말이며, 해당 역사적 빌드의 생성 `G`는 **미확인**이다.

[IIIF Content State 1.0 §2.2.5](https://iiif.io/api/content-state/1.0/#225-limitations-of-simple-uris)는 단순 Canvas URI만으로 문맥이나 부분 영역을 표현하기 어려운 경우 Manifest를 `partOf`로 함께 주도록 한다. 실제 관측 식별자로 만든 정확한 반환 payload는 [iiif-return-payloads.json](iiif-return-payloads.json)이다. 예를 들면 다음은 검증한 Night Watch manifest/Canvas 관계를 표현한다.

```json
{
  "id": "https://iiif.micr.io/PJEZO/canvas",
  "type": "Canvas",
  "partOf": [
    {
      "id": "https://iiif.micr.io/PJEZO/manifest",
      "type": "Manifest"
    }
  ]
}
```

이 JSON을 GET query로 전달할 때의 규격 인코딩도 [static-analysis.json](static-analysis.json)에 저장했다. `encodeURIComponent`→base64url→padding 제거 순서다. 실제 viewer 주소나 choice 선택 옵션을 임의로 만들어 작동한다고 주장하지 않았다. **정확한 payload 구조를 만들 수 있음**과 **선택한 viewer에서 의도한 영역/UV 그림이 표시됨**은 서로 다른 확인이다.

## 2. 학술출판: XML target과 HTML fragment, 같은 그림의 다른 설명

원 논문은 Ranieri et al., *SPectral graph theory And Random walK (SPARK) toolbox for static and dynamic characterization of (di)graphs: A tutorial*, PLOS ONE, 2025-06-05, DOI `10.1371/journal.pone.0319031`이다. [출판사 XML](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript)을 직접 받았고 `dtd-version="1.3"` 및 JATS 1.3 DTD 선언을 확인했다. 논문 분류에는 Mathematics/Graph theory, Linear algebra, Eigenvalues/Eigenvectors가 명시되어 있다. 생물학적 응용도 포함되어 있어 순수수학만의 사례로 부르지 않는다. 여기서는 수학적 그래프 지표를 설명하는 Figure 7/8 및 관련 절을 판독했다.

| 대상 / 직접 연 원문 | 실제 확인 | 목적 판정·반례 | 충분한 반환 링크와 미확인 |
| --- | --- | --- | --- |
| [JATS `fig`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html), [JATS `xref`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html) | `fig`는 graphic 외에도 텍스트·식·표를 담을 수 있다. `xref`는 문서 내부 id를 가리킨다. 여러 언어 label/caption을 같은 figure content에 붙일 수도 있다. | 그림 파일 하나가 figure 구조·설명 전체를 대표한다는 가정이 깨진다. XML의 내부 target이 HTML 변환 뒤 그대로 남는다는 규정은 확인하지 못함. | 두 규격 페이지는 동일 저작으로 1개 산입. `fig`와 `xref`만으로 실제 publisher HTML anchor를 추정하지 않음 |
| [XML](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript) / [출판사 HTML](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007) | 본문 `fig` **9개**, `xref ref-type="fig"` **20개**. 모든 XML `rid`가 내부 id에 연결된다. 그런데 9개 XML fig id는 HTML id에서 모두 **0회**이고, 점을 하이픈으로 바꾼 실제 DOM id는 각각 **1회**다. | 예: XML `pone.0319031.g007`을 그대로 URL fragment로 붙이는 방법은 정확 도착 근거가 없다. 실제 HTML은 `pone-0319031-g007`이다. | 정확 링크는 `…article?id=10.1371/journal.pone.0319031#pone-0319031-g007`. 현재 source DOM에 anchor와 href가 있음을 확인. 브라우저 스크롤·lazy loading은 **미확인** |
| 같은 Fig 7, 다른 설명 문맥 | XML `g007`은 총 5개 fig-xref를 받는다. **본문 문단 4개 참조(Results 3회, Discussion 1회)**와 **Table 3 caption 1개 참조**로 구분된다. 본문은 Results `sec022`와 Discussion `sec025`에서 같은 그림을 재참조한다. 결과 절은 분포 비교를 제시하고, 논의 절은 식(54)와 ρ가 within-cluster 연결 및 partition 차이에 미치는 설명에서 같은 그림을 쓴다. | 동일 그림을 반환해도 “분포를 보고 싶다”와 “왜 달라지는가를 설명받고 싶다”의 충분조건은 다르다. 그림 파일 해시만으로 독자가 필요한 설명 절을 정할 수 없다. Table 3의 다섯 번째 참조는 아래 의미 불일치 때문에 올바른 재사용의 근거에서 뺐다. | 결과 문맥 [§3.2](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec022)와 해석 문맥 [§4](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec025)을 목적에 맞게 병기. Fig7 단독 링크는 이 문맥 둘을 구분하지 않음 |
| [Fig 7](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007) vs [Fig 8](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g008) | PNG를 수신·디코드·직접 봤다. 둘 다 4-panel 파란 boxplot 구조이지만 Fig7은 normalized association, Fig8은 normalized cut이다. 600×359 / 600×361이고 SHA-256도 다르다. | 비슷한 시각 구성은 같은 지표/목적의 후계 근거가 아니다. Fig7과 Fig8은 다른 quantity와 방향을 보여 주므로 임의 대체 불가. 단, 이것은 버전 간 후계 NO를 채점한 사례가 아니다. | 독자의 지표에 맞는 실제 figure id와 `sec022`를 반환. 추가 GET은 XML 1+HTML 1+두 PNG 2=4회. 논문의 계산·통계 재실행과 역사 생성은 **미실시/미확인** |

### 유효한 id 연결 안에서도 발견된 의미 불일치

부모가 별도로 원 XML을 재판독해 지적한 뒤 Q7 작성자가 원 XML·HTML을 다시 대조했다. **Table 3 `pone.0319031.t003`의 caption(원 XML L518)**은 `r_Ncut` 분포를 설명하면서 `rid="pone.0319031.g007"`을 가리킨다. 그러나 Figure 7 caption과 실제 raster는 normalized association이고 Figure 8이 normalized cut이다. [실제 HTML Table 3 anchor](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-t003)도 같은 `#pone-0319031-g007` href와 XML 수식 `e494`에 대응하는 thumbnail 자원을 사용한다. HTML에서 수식은 raster로 연결되며 그 추가 수식 raster의 시각 내용은 이번에 다시 수신하지 않았다.

따라서 **id 연결의 유효성은 확인되지만 caption의 지표와 target figure 사이의 의미 일치는 성립하지 않는다.** 잘못된 부분이 caption의 지표명인지 figure target인지, 공식 저자가 어떤 수정을 의도했는지는 **미확인**이다. `Fig7→Fig8` 자동 교정은 하지 않는다. 이 불일치는 같은 그림의 올바른 설명 재사용 횟수에 합치지 않고 `4개 본문 참조 + 1개 불일치 caption 참조`로 기록한다. 원문 대조는 [plos-table3-caption-inconsistency.json](plos-table3-caption-inconsistency.json)에 보존했다. 부모의 별도 재판독은 이 한 불일치에 대한 추가 검토이며, Q7 작성자가 자기 자료 전체를 독립 검토했다는 주장은 하지 않는다.

해석에 사용한 XML source line, 각 figure의 caption·direct graphic, xref→section 대응과 실제 HTML id 수는 [static-analysis.json](static-analysis.json)의 `plos.figures`에 있다. `fig/graphic`와 caption 속 수식 대체 graphic을 구분했다. 후자를 별도 figure로 세지 않았다.

## 3. 이 묶음에서 주 연구로 옮길 수 있는 판단 규칙

1. **자원 관계를 typed edge로 읽는다.** IIIF `thumbnail`, painting body, commentary의 HTML `img`는 각각 다른 이유로 URL을 포함한다. JATS의 `fig/graphic`, `xref`, publisher HTML anchor도 구별해야 한다. URL이 존재한다는 사실은 관계와 용도를 대신하지 못한다.
2. **독자의 목적과 구체적 방법을 별도 열로 유지한다.** 같은 소장품을 natural light로 보는 것과 UV 보수 흔적을 보는 것은 방법·판독 목적이 다르다. 같은 boxplot 형식도 다른 수학 지표를 나타낼 수 있다. 동일 hash나 basename의 효과를 넘어서 절·caption·source call을 확인해야 한다.
3. **정확한 도착 위치는 목적에 필요한 설명까지 포함한다.** Figure7만으로 충분한 요청도 있지만, 변화 이유를 묻는 요청에는 Results 또는 Discussion 문맥이 더 필요하다. XML id와 HTML id의 변환처럼 주소의 계층이 바뀌는 경우 실제 DOM을 읽어야 한다.
4. **반환을 보류할 조건은 좁고 구체적으로 적는다.** Fitzwilliam의 null 좌표를 이유로 작품 전체가 사라졌다고 하지 않는다. 전체 Canvas 관계는 확인했고 정확 지역 도착이 미확인인 것이다. face micrograph는 새 후보 뷰일 뿐 parent 좌표의 복원 증거가 아니다.
5. **확인 비용은 URL 열람 수와 별개로 누적한다.** 같은 자료를 재열람하거나 동일 작품의 다른 크기 이미지 두 개를 받아도 고유 1차 저작 수는 증가하지 않는다. 여기의 비용 표는 연구자가 직접 원자료 관계를 확인하기 위해 추가한 성공 HTTP GET 수이며 실제 사용자의 클릭 수나 viewer의 내부 요청 수를 재지 않았다.

## 재계산과 검토 범위

저장한 원문에서 다음 명령으로 JSON/DOM 관계·좌표·xref 수·raster 치수를 다시 계산할 수 있다. 실행 영수증은 [static-analysis-receipt.json](static-analysis-receipt.json)에 있다. 저장된 원문/코드를 읽는 작은 분석이며 외부 source 코드는 실행하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/crossdomain/analyze_static.py
```

필요 모듈은 `lxml`, `Pillow`다. 최초 파일명을 `inspect.py`로 정해 stdlib `inspect`와 충돌한 실패(종료 1)를 기록했고 `analyze_static.py`로 이름을 바꾼 뒤 종료 0을 확인했다. 앞선 실패의 부분 stdout을 성공 영수증으로 쓰지 않았다. 이 영수증은 부모가 커밋하기 전 분석 스크립트 및 원문 SHA-256을 대상으로 하며, 최종 결과 SHA의 저장소 계약 검사를 대신하지 않는다.

원자료를 새로 받으려면 `acquire.py`의 ID별 요청을 사용할 수 있다. 다시 받은 현재 자료는 보존 원문을 덮어쓰므로 **새 별도 사본에서만** 재수신한다. 시간에 따라 현재 페이지가 바뀌면 이전 SHA-256과 다르다는 결과 자체를 보존해야 한다.

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/crossdomain/acquire.py IIIF-SPEC IIIF-STATE JATS-FIG JATS-XREF RIJKS-MANIFEST FITZ-MANIFEST PLOS-XML PLOS-HTML
```

직접 읽기는 규범의 지정 절, manifest 관계와 요약, 논문의 지정 문단·caption, 4개 raster에 한정했다. 기계적인 전수는 수신된 두 main manifest의 embedded Annotation/Choice 및 그 한 논문의 fig/xref/HTML id에 한정했다. 박물관 전체·모든 출판사·다른 논문·다른 연도의 자료를 전수 조사한 것은 아니다. 웹 viewer 실행, 당시 G, 두 시스템의 버전 이동 비교는 **미확인**이다.

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
| --- | --- | --- |
| Fitzwilliam에는 자원과 설명이 있지만 32개 target 좌표가 모두 null이며 viewer 실제 fallback을 보지 않음 | 저장된 `AGOID.29376/manifest.json`, `iiif-return-payloads.json`을 실제 IIIF 3 viewer에 입력해 natural/UV choice와 tag 393 위치를 관측 | 공식 수정 manifest의 유효 수치 좌표와 viewer가 의도한 지역/UV 선택에 도착하는 관측이 생기면 정확 부분 링크 유보를 해제 |
| PLOS Table 3는 유효한 Fig7 id를 가리키지만 caption 지표명 r_Ncut은 Fig7의 normalized association과 어긋남. 잘못된 부분의 저자 의도는 미확인 | DOI `10.1371/journal.pone.0319031`의 공식 correction/버전 기록과 t003·g007·g008 원 XML을 함께 다시 확인; 다른 publisher에는 anchor 변환을 일반화하지 않음 | 공식 수정이 caption 지표명 또는 target을 명시하면 해당 관계를 갱신. 그전에는 Fig7→Fig8 자동 교정하지 않음 |
| 이번 타 분야 실물은 현재 snapshot으로 역사적 이동·삭제 또는 생성 G를 증명하지 않음 | 같은 museum manifest/논문의 공식 이전 버전, 변경 기록, 해당 실행의 출력 매니페스트를 고정 SHA와 함께 확보 | 실제 rename/삭제와 새 사용 절이 연결되거나 출력 지문이 실행에 결박되면 후계·당시 생성의 미확인을 해당 범위에서만 갱신 |
