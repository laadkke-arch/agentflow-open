# AF-RES-106 Q7 — 재개 후 원문 재판독과 봉인 표본 검산

## 판정

IIIF와 JATS의 필수 규격·실물은 각각 충족했다. 최초 조사에서 보존한 14개 성공 응답은 **새로운 1차 저작 7개**로 묶이며, AF-RES-102의 고정 `sources.jsonl` 477행에는 해당 계보가 없다. 이번 검토는 그중 8개 원본 URL을 다시 수신하여 모두 HTTP 200 및 최초 보존본과 같은 SHA-256을 확인했다. 나머지 6개 자료는 최초 영수증의 SHA-256과 일치하는 보존본을 직접 다시 읽거나 이미지를 보았다. **이번 재열람이 더하는 고유 자료 수는 0이다.**

원 영수증·원 자료는 그대로 두었다. [review-network-receipts.json](review-network-receipts.json)은 2026-11-24T00:13:24Z–00:13:38Z의 HTTP 재수신 기록이고, [review-final.json](review-final.json)은 별도 에이전트가 직접 계산한 관계·분모·선택 검산이다. [sources-review.jsonl](sources-review.jsonl)은 자료별 재판독 원장이다. 여기의 현재 snapshot은 주 연구의 버전 간 이동·삭제 또는 역사 생성 G의 사례 수에 들어가지 않는다.

## 1. 자료 최소량과 중복 제외

| 계보 | 직접 연 공식 자료 | 이 과제의 고유 신규 저작 | 이번 검토에서의 처리 |
|---|---|---:|---|
| IIIF Presentation 3 | [Canvas·AnnotationPage 규격](https://iiif.io/api/presentation/3.0/) | 1 | Canvas, painting body/target, `items`와 `annotations` 구분을 재판독. 앵커마다 별도 산입하지 않음 |
| IIIF Content State 1 | [Content State 규격](https://iiif.io/api/content-state/1.0/) | 1 | Canvas와 Manifest 문맥을 함께 담는 payload와 GET 인코딩 규칙을 재판독. Presentation과 다른 규격 |
| Rijksmuseum 기술 안내 | [기관의 IIIF 안내](https://data.rijksmuseum.nl/tutorials/iiif/) | 1 | 보존 원문 Step 4/5 재판독. 실제 소장품 manifest와 별개의 기술 설명 저작 |
| Rijksmuseum Night Watch | [PJEZO manifest](https://iiif.micr.io/PJEZO/manifest), [body](https://iiif.micr.io/PJEZO/full/1024,/0/default.jpg), [thumbnail](https://iiif.micr.io/PJEZO/full/80,100/0/default.jpg) | 1 | manifest와 두 크기 그림은 같은 작품의 계보로 하나만 산입. 그림 둘을 직접 봄 |
| Fitzwilliam portrait | [작품 manifest](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json), [face micrograph](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/micrograph/393/manifest.json) | 1 | 하위 얼굴 확대 manifest는 같은 소장품 묶음이므로 추가 산입하지 않음 |
| JATS Publishing 1.3 | [`fig`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html), [`xref`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html) | 1 | 다른 요소 페이지 두 개를 동일 규범 저작 하나로 계산 |
| PLOS SPARK 논문 | [출판사 XML](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript), [HTML](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031), Fig7·8 PNG | 1 | XML/HTML/그림을 같은 논문 계보 하나로 계산. Mathematics/Graph theory 분류를 원 XML에서 확인 |
| 합계 | 14개 최초 성공 URL·8개 이번 HTTP 재수신 | **7** | 필수 최소 묶음은 Presentation+Rijksmuseum 및 JATS+PLOS의 **4개**. 추가 독립 규격·안내·소장품 3개는 별도 계보이며 필수 하한과 구별 |

최초 산입 ID는 `CD106-I01/I02/I03/I04/I05/J01/J03`이다. 원장에 동일 SHA-256 또는 같은 논문·작품·규격의 표현을 별도 저작으로 추가하지 않았다. IIIF 규격과 JATS 규격이 선행 102에서 이미 산입된 것처럼 잘못 처리하지도 않았다. 별도 Git 원문 읽기에서 102 원장에 IIIF/JATS 관련 URL이 0개임을 재확인했다.

## 2. IIIF: 수록 관계와 실제 표시·영역 도착

| 원자료·위치 | 재판독 값 | 지지하는 판단 | 판단 한계·반대 관측 |
|---|---|---|---|
| [Presentation 3 §5.3](https://iiif.io/api/presentation/3.0/#53-canvas), [§5.5](https://iiif.io/api/presentation/3.0/#55-annotation-page) | Canvas `items`의 AnnotationPage에 포함된 `motivation=painting`의 body가 Canvas 표시 자원이다. 비painting 주석은 `annotations`에 속한다. | JSON 안에서 발견한 이미지 URL을 모두 Canvas 표시 자원으로 분류하면 안 된다. | 규범 관계를 읽은 것이 실제 viewer 실행 확인은 아니다. 표시와 G는 **미확인** |
| [Rijksmuseum PJEZO](https://iiif.micr.io/PJEZO/manifest), `/items/0/items/0/items/0` | Canvas 1, AnnotationPage 1, painting Annotation 1. target은 `https://iiif.micr.io/PJEZO/canvas`. body는 `…/full/1024,/0/default.jpg`, thumbnail은 `…/full/80,100/0/default.jpg` | 동일 작품의 미리보기 URL과 표시 body의 역할이 다르다. body와 thumbnail을 따로 수신·디코드했다. | 두 파일을 같은 작품이라고 보는 것은 manifest 관계와 실물에 근거한다. thumbnail의 존재만으로 상세 해석이나 원 크기 표시를 보장하지 않음 |
| [Fitzwilliam AGOID.29376](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/manifest.json), painting body·commentary | body는 `Choice`이며 **17개** 이미지 선택지. commentary Annotation **32개** 모두 target의 `xywh=null,null,null,null`. summary는 자연광 색 손실과 UV 형광·보수 흔적을 다르게 설명한다. | 같은 소장품 안에서도 관측 방법과 독자 목적이 다르다. 전체 Canvas 도착과 특정 얼굴 영역·UV 선택 도착을 나눠야 한다. | 실제 viewer의 기본 Choice, 좌표 fallback, 클릭 동작은 **미확인**. 원 좌표를 임의 숫자로 고치지 않음 |
| [face micrograph 393](https://miniatures-iiif.fitzmuseum.cam.ac.uk/AGOID.29376/micrograph/393/manifest.json), `/items/0` | `…/micrograph/393/canvas/0` 및 face TIFF Choice가 별도로 존재한다. | 원 parent의 잘못된 좌표와 별개로 얼굴 확대 후보의 구조를 확인했다. | 하위 TIFF 자체는 이번 검토에서 수신·표시하지 않았다. parent의 원하는 좌표를 복구했다는 증거가 아니며 실제 확대 표시와 정합은 **미확인** |

[iiif-return-payloads.json](iiif-return-payloads.json)의 Manifest+Canvas 입력은 정적 관계에 맞다. Night Watch는 Canvas `https://iiif.micr.io/PJEZO/canvas`와 Manifest `https://iiif.micr.io/PJEZO/manifest`를 함께 전달할 수 있다. Fitzwilliam의 정확 얼굴 위치를 요구하면 parent의 null 좌표 때문에 **유보**한다. 별도 얼굴 micrograph를 대안으로 표시하더라도 원 영역과의 정합이 확인됐다고 하지 않는다.

추가 열람 비용은 최초 원장과 이번 재열람을 나눈다. 최초 Night Watch 실물 검토는 manifest/body/thumbnail 3개 GET, 별도 기술 안내 1개 GET이었다. 이번 검토의 manifest 재GET 1회와 보존 그림 2개 열람은 신규 저작을 늘리지 않으며, 실제 사용자의 클릭 수를 측정한 값도 아니다.

## 3. JATS: 유효한 id와 정확한 의미는 별도다

| 원자료·위치 | 재판독 값 | 판단과 정확 반환 위치 | 미확인·반대 관측 |
|---|---|---|---|
| [JATS `fig`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/fig.html), `#text` Usage/Remarks | figure는 그림 파일뿐 아니라 텍스트·식·표를 포함할 수 있다. 한 content에 여러 언어 label/caption도 가능하다. | figure 구조와 특정 graphic 파일을 같은 것으로 취급하지 않는다. | 이 규격은 출판사 HTML anchor 변환을 보증하지 않음 |
| [JATS `xref`](https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/xref.html), `#text` | xref는 내부 `id` 대상이며 `ref-type`은 참조 대상 종류를 보존한다. | 내부 참조 해석 후 실제 HTML fragment를 별도 확인한다. | 내부 id 유효성만으로 캡션의 지표·독자 목적 일치를 판단하지 않음 |
| [PLOS XML](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0319031&type=manuscript), `fig`·`xref` | `dtd-version=1.3`, figure **9개**, figure xref **20개**, 모든 `rid`는 XML 내부에서 유일한 id로 연결된다. 9개 점 구분 XML id는 HTML id로 0회이며, 하이픈 HTML id는 각각 1회다. | Fig7의 실제 반환은 [#pone-0319031-g007](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007). XML `#pone.0319031.g007`을 그대로 붙이지 않는다. | DOM 정적 확인이다. 브라우저의 스크롤·lazy loading은 **미확인** |
| XML L514, L517, L691의 Fig7 본문 xref | 본문 xref **4회**, 서로 다른 본문 문단 **3개**. Results `sec022` 2문단에 3회, Discussion `sec025` 1문단에 1회다. | 그림 비교에는 [§3.2 #sec022](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec022), 원인 해석에는 [§4 #sec025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#sec025)를 그림과 함께 준다. | 최초 보고서의 “본문 문단 4개 참조”는 **4회 참조/3개 문단**으로 명확히 한다. 새 독립 자료나 독립 사례 4개가 아니다 |
| XML L518 Table3 caption, L515 Fig7 caption, L556 Fig8 caption | Table3는 `r_Ncut`을 쓰면서 Fig7 `rid`를 가리킨다. Fig7은 normalized association이고 Fig8은 normalized cut이다. 실제 PNG 두 장의 제목도 이를 확인한다. | [Table3 #pone-0319031-t003](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-t003)의 id 연결은 유효하지만 의미 대응은 어긋난다. 이 참조는 올바른 재사용 4회와 따로 기록한다. | 잘못된 부분이 Table3의 지표명인지 Fig target인지 저자 의도는 **미확인**. Fig7→Fig8 자동 교정을 제안하지 않음 |
| [Fig7](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g007)·[Fig8](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0319031#pone-0319031-g008) PNG | 둘 다 네 패널의 파란 boxplot이나 지표명과 값의 방향이 다르다. Fig7은 association, Fig8은 cut이다. | 비슷한 시각 형식만으로 같은 목적의 대체 그림을 고르면 안 된다. | 같은 논문 안의 대조 사례이며, 시간적 후계 판정이나 주 표본 FN/FP 분모에 합치지 않는다 |

## 4. 봉인 표본의 별도 계산

결과 본문 판독과 독립적으로, **이미 봉인된 원장만** `git show 8054c222…`로 읽어 모든 잔여 적격 행의 SHA-256과 층별 앞2개 선택을 다시 계산했다. `frame.csv`, `predictions.csv`, `SCOPE.md`, `EVALUATION_TARGETS.md`의 현재 바이트는 모두 해당 봉인판과 같았다. 고정 102 적격 페이지와 겹치는 잔여 적격 `page_path`는 0개다. 별칭·절 경계의 모든 원 HTML을 이 검토자가 다시 전수 판독한 것은 아니다.

| 프로젝트 | 적격 잔여 | A·M·G 후보 수 | 12자리 중 채움·결원 | 해시·선택 결과 |
|---|---:|---|---|---|
| ggplot2 | 68 | 0·57·11 | 4·2 | 적격 68개 해시 일치; M/G 각 앞2개와 봉인 선택 일치 |
| Matplotlib | 479 | 3·0·476 | 4·2 | 적격 479개 해시 일치; A/G 각 앞2개와 봉인 선택 일치. 프로젝트 문자열 `Matplotlib`의 대문자를 보존해야 재현됨 |
| 합계 | 547 | 서로 다른 모집단으로 보존 | **8·4 = 12자리** | 서로 다른 case ID 12개. 4결원을 예측 유보 4개로 합산하지 않음 |

확인된 방법론 한계는 기존 봉인 문서에 이미 공개돼 있다. ggplot2 source-set 해석은 경로를 본 뒤·새 본문 전 수정되었고, Matplotlib의 일반 시각 역할 축도 선택 뒤·새 본문 전에 추가됐다. 그러므로 “경로도 전혀 모른 상태에서 모든 정의를 사전 등록했다”는 표현은 틀리다. 일반 역할의 성공을 원 구체 목적 성공으로 합치지 않아야 한다. 이번 검산은 그 제한을 없애지 않으며, 주 예제 U의 별도 맹검 재채점도 아니다.

재계산 명령은 다음과 같다. 저장한 원문 관계·지문 및 봉인 Git blob을 읽고 자기 검토 JSON 하나를 갱신하며, 봉인 원장이나 새 예측은 수정하지 않는다.

```sh
python -B docs/workstreams/research/AF-RES-106/evidence/crossdomain/review_validate.py
```

| 가장 중요한 불일치·약점 | 다음 조사 제안·직접 열 자료 또는 실행할 입력 | 어떤 관측이면 판단을 바꿀지 |
|---|---|---|
| Fitzwilliam 32개 region target의 좌표는 null이며 실제 viewer의 Choice·fallback은 미확인 | 보존한 `AGOID.29376/manifest.json`과 Manifest+Canvas payload를 실제 IIIF3 viewer에 입력해 얼굴·UV 선택을 관측 | 유효한 공식 region 좌표와 의도한 영역·UV 이미지에 도착한 관측이 확보되면 정확 부분 링크 유보를 해제 |
| PLOS Table3의 유효한 Fig7 id와 Ncut 캡션 지표는 불일치하며 저자 의도는 미확인 | 공식 correction/버전 기록과 t003·g007·g008 원 XML을 함께 열기 | 저자가 caption 지표 또는 target의 수정을 명시하면 그 관계만 갱신; 유사 그림만으로 자동 교정하지 않음 |
| 표본 해시·순위는 맞지만 source-set 및 일반 목적 축은 경로/선택 노출 뒤 수정되었고 Q7은 현재 snapshot이다 | 기존 최초 man-only 계산을 민감도로 병기하고, 다음 버전 비교에는 목적·source-set를 경로 열람 전 봉인 | 독립 사전 고정 반복에서 같은 오류 양상이 재현되고 실제 버전 간 변경·실행 출력 연결이 확보되면 일반화·G의 범위를 확대 |
