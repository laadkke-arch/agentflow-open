# Q6 · EPUB와 연구 데이터에서 읽어야 하는 관계

주 모집 6건과 분리한 보조 조사다. **새 출판물·데이터 계보는 2개**다: Thomas Cole EPUB, Data Citation Corpus. Moby-Dick·IIIF 0009·094의 네트워크 경로는 재계수하지 않았다. 원응답을 내려받아 XML/JSON·내장 파일을 읽었으며, EPUB reader·예제 프로그램·발행 스크립트는 실행하지 않았다. 구체적 속성·지문은 [audit.json](audit.json), 요청·UTC·리다이렉트는 [receipts.json](receipts.json)과 [additional-receipts.json](additional-receipts.json), 자료별 한계와 보수적 중복 제거는 [sources.jsonl](sources.jsonl)에 있다.

## 1. EPUB: 목록, 본문 사용, 과거 바이트의 현재 사용

| 관측 대상 | 20170606 패키지 | 20230704 패키지 | 판정 범위 |
|---|---|---|---|
| 공식 실물 | [2017 EPUB](https://github.com/IDPF/epub3-samples/releases/download/20170606/cole-voyage-of-life.epub), 970,934B, SHA256 `721a9c4ab1834aad69f9d19c0a69c043df81012d3dae936935be0a180c6c2867` | [2023 EPUB](https://github.com/IDPF/epub3-samples/releases/download/20230704/cole-voyage-of-life.epub), 970,980B, SHA256 `e38ed606ff604e638f737efaf66e0fd0b2997c3eab7432bcba9a00a81a925cf3` | 두 공개 산출물의 실제 바이트를 각각 수신했다. HTTP MIME은 `application/octet-stream`, ZIP 내부 `mimetype`은 `application/epub+zip`이다. |
| 판 식별 | EPUB 선언 3.0, 내부 `EPUB/cole.opf` | 같은 선언·경로·고유 식별자 | 내부 규격판 3.0, 샘플 발행 태그 2017/2023, 그림의 생성 시점은 서로 다른 축이다. |
| 포함 관계 | ZIP 24파일, manifest 21/21, spine 10 | ZIP 24파일, manifest 21/21, spine 10 | OPF가 열거한 모든 로컬 자원을 실제 ZIP에서 찾았다. |
| Childhood 본문 | `EPUB/xhtml/1b-childhood-painting.xhtml`, `body#b1`, `img#i1` | 같은 위치 | 두 본문 모두 `src="../images/1-childhood-1024.jpg"`다. 본문 파일의 디렉터리를 기준으로 해석하면 `EPUB/images/1-childhood-1024.jpg`다. |
| Childhood 실물 | JPEG 149,915B, SHA256 `9c7fabbe74287ddd02b1473f6c7927ec2ca0d932a8ed4535bc372cc3bc898aea` | 동일 바이트·동일 현재 참조 | 해당 판에 포함됨=확인, 해당 본문이 사용함=확인, 2023 빌드가 새 그림 바이트를 생성함=미확인. |
| 나머지 그림 | 본문 `img` 9개, 모두 내부 JPEG | 9/9 그림 지문이 이전 패키지와 동일하고 현재 본문에서도 참조 | 이전 파일의 현재 사용은 실제 양성이다. 동일 SHA만으로 복사와 결정적 재생성을 구별하지 않았다. |
| 수정 메타데이터 | `2012-03-20T11:37:00Z` | 같은 값 | 2023 패키지의 본문 4파일은 2017과 바이트가 다르다. OPF 수정 날짜만으로 패키지 발행 또는 모든 자원의 생성 날짜를 정하면 틀린다. |

**발행 기록.** [release API](https://api.github.com/repos/IDPF/epub3-samples/releases/tags/20230704)의 공개일은 `2023-07-04T16:09:10Z`, `cole-voyage-of-life.epub`의 asset ID는 `115540658`, 업로드 시각은 `16:00:44Z`, 크기는 `970980`이다. asset digest 필드는 비어 있었다. 이 기록은 패키지 발행을 지지하지만 JPEG 생성 job은 지목하지 않는다. 태그가 가리키는 소스 커밋은 `46d7e07e1b39b2d0a0245ececaf896edcd9de4b2`다.

**본문→파일.** [고정 XHTML](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/xhtml/1b-childhood-painting.xhtml)의 9–11행과 [OPF](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/cole.opf)의 `j1_1024` 항목이 같은 자원으로 합류한다. [고정 JPEG](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/images/1-childhood-1024.jpg)를 별도로 받았고 두 EPUB 내부의 JPEG와 정확히 일치했다.

**정확한 바이트와 텍스트 동등성의 차이.** 소스 XHTML은 511B/SHA `158d88e6…`, 패키지 XHTML은 524B/SHA `11728de7…`이다. OPF도 3,641B 대 3,692B로 다르다. 둘은 CRLF를 LF로 정규화한 뒤에만 일치한다. JPEG는 정규화 없이 일치한다. 원바이트 지문과 정규화 비교를 다른 필드에 저장했다.

**빌드 규칙의 범위.** 같은 소스판의 [pack-single.sh](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/pack-single.sh)는 확장된 EPUB 디렉터리를 `epubcheck.jar … -mode exp -save`로 묶는다. 정적 파일을 입력으로 하는 문서화된 포장 경로를 확인한 것이며, 2023 release asset과 연결된 job 실행 영수증을 발견한 것은 아니다. 따라서 “2023판에서 쓰는 기존 그림”을 권할 수 있지만 “2023 빌드에서 새로 만든 그림”이라고 권하지 않는다.

**외부 주소가 필요 없는 범위.** 패키지를 받은 뒤 Childhood 그림을 확인하는 데 필요한 것은 내부 `container.xml → cole.opf → 1b-childhood-painting.xhtml → JPEG` 4파일이다. 이 그림에는 추가 인터넷 요청이 필요 없다. 조사한 11개 XHTML의 `img/src`, `href`, `data` 속성에서 외부 HTTP(S) 링크와 data URI는 0개였고, OPF 메타데이터에는 라이선스·출처 외부 링크 2개가 따로 있다. 이 수치는 모든 EPUB·CSS·스크립트의 네트워크 동작에 대한 일반 부재 판정이 아니다.

**규칙 비교.** [EPUB 3.3 고정 권고](https://www.w3.org/TR/2026/REC-epub-33-20260113/) §4.2.5·§5.2는 OPF와 본문의 상대 URI 해석 기준을 구분한다. §5.6은 rendering resource 목록과 metadata link를 구분하며 §3.7은 data URI의 내장을 설명한다. 이번 샘플은 EPUB 3.0을 선언하므로 이 비교를 3.3 완전 적합성 검사로 부르지 않았다.

## 2. 연구 데이터: 버전 DOI, 전체 계보 DOI, 파일 링크

Data Citation Corpus는 연구 데이터의 인용 10,006,058건을 담았다고 발행자가 설명하는 데이터셋이다. 소프트웨어 릴리스 ZIP만 조사한 사례가 아니다. 생산자는 DataCite·Make Data Count, 저장소는 Zenodo다.

| 자료 | 판·관계 | 파일 목록에서 직접 읽은 속성 | 한계 |
|---|---|---|---|
| [v1.0 레코드](https://zenodo.org/records/11196859), [API](https://zenodo.org/api/records/11196859), [DOI](https://doi.org/10.5281/zenodo.11196859) | 공개일 2024-01-30, version `v1.0`; concept DOI `10.5281/zenodo.11196858` | `2024-01-30-data-citation-corpus-v1.0.zip`; 1,400,187,243B; 선언 MD5 `7e56ae579f62d432b2fac135d924ac70` | 대용량 ZIP 전체는 내려받지 않았다. 크기·MD5는 발행 목록의 선언이며 독립 재계산값이 아니다. |
| [v1.1 레코드](https://zenodo.org/records/11216814), [API](https://zenodo.org/api/records/11216814), [DOI](https://doi.org/10.5281/zenodo.11216814) | 공개일 2024-05-10, version `v1.1`; 같은 concept; `isNewVersionOf`→v1.0 | `2024-05-10-data-citation-corpus-v1.1.zip`; 1,834,930,014B; 선언 MD5 `e2e191e9573a9ee729413df872edd96b` | 인용 추가·삭제가 없다는 설명은 발행자 주장이다. 두 ZIP의 의미 비교는 하지 않았다. |
| [v1.0 DataCite 등록](https://api.datacite.org/dois/10.5281/zenodo.11196859) | `IsVersionOf`→concept | DOI 등록의 관계 유형을 직접 읽었다. | ZIP 파일을 받은 결과가 아니다. Zenodo API와 같은 판 사건을 보수적으로 중복 처리했다. |
| [v1.1 DataCite 등록](https://api.datacite.org/dois/10.5281/zenodo.11216814) | `IsNewVersionOf`→v1.0; `IsVersionOf`→concept | succession과 instance 관계가 별개다. | 생성기·빌드 job·payload SHA를 제공하는 관계가 아니다. |
| [concept DataCite 등록](https://api.datacite.org/dois/10.5281/zenodo.11196858), [concept DOI](https://doi.org/10.5281/zenodo.11196858) | `HasVersion` 6개에 v1.0·v1.1 포함 | 관측 시 concept DOI는 302 두 번을 거쳐 `/records/16901115`로 갔다. 반면 v1.1 DOI는 `/records/11216814`로 갔다. | concept의 관측 메타데이터에는 version `v4.1`과 여러 `IsNewVersionOf`도 있다. 필드 이름 하나만으로 concept을 고정판으로 바꾸지 않는다. 이후 target은 바뀔 수 있다. |

**관계의 전이가 깨지는 구체적 예.** v1.1과 v1.0이 같은 concept의 버전이라는 사실에서 두 ZIP의 바이트 동일성은 따라오지 않는다. 두 발행 목록의 파일명·길이·MD5가 다르다. 발행자가 같은 인용 집합이라고 설명하더라도 표현·패키징의 바이트까지 같다는 뜻은 아니다. concept DOI가 v1.1을 포괄한다는 사실에서도 그 주소를 열면 v1.1을 받는다는 결론은 따라오지 않는다. 이번 실제 도착은 v4.1 계열 레코드였다.

**규칙과의 대조.** [DataCite Schema 4.5 관계 정의](https://datacite-metadata-schema.readthedocs.io/en/4.5/appendices/appendix-1/relationType/)는 `HasVersion`/`IsVersionOf`, `IsNewVersionOf`, `IsIdenticalTo`, `IsCompiledBy`를 구별한다. 읽은 데이터 등록에는 버전 관계가 있지만 정확한 생성 job 관계는 없었다. [Zenodo DOI FAQ](https://zenodo.org/help/versioning)는 정확한 연구 산출물 인용과 전체 계보 인용을 구별한다. [Manage versions](https://help.zenodo.org/docs/deposit/manage-versions/)의 이전 파일 import 규칙은 신규 판에서 기존 파일을 재사용할 수 있음을 명시한다. 이것은 가능한 발행 방식의 1차 근거이며, 선택한 Corpus ZIP이 실제 그 기능으로 재사용됐다는 증거로 격상하지 않았다.

## 3. 목적별 반환과 추가 비용

| 요청 | 우선 반환할 주소와 볼 곳 | 더 필요한 확인 | 유보할 주장 |
|---|---|---|---|
| “2023 EPUB의 Childhood 그림을 보겠다” | [2023 EPUB](https://github.com/IDPF/epub3-samples/releases/download/20230704/cole-voyage-of-life.epub), 내부 `1b-childhood-painting.xhtml` | 패키지 1회 수신 뒤 내부 4파일 검사. 별도 인터넷 JPEG 요청은 필수 아님. | 이 연구에서는 EPUB reader의 표시 동작을 실행하지 않았다. |
| “그 절의 이미지 바이트를 따로 쓰겠다” | 패키지 위치와 [동일 SHA의 고정 JPEG](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/30/cole-voyage-of-life/EPUB/images/1-childhood-1024.jpg) | 별도 JPEG 1회 수신은 편의 선택. 본문과의 매핑을 함께 유지한다. | JPEG URL만 주면 어느 본문·판에서 쓰였는지 잃는다. |
| “2023 빌드에서 새로 생성한 그림을 보존하겠다” | 위 본문·JPEG에 [release 기록](https://api.github.com/repos/IDPF/epub3-samples/releases/tags/20230704), [포장 규칙](https://raw.githubusercontent.com/IDPF/epub3-samples/46d7e07e1b39b2d0a0245ececaf896edcd9de4b2/pack-single.sh)을 조건부 추가 | 이미지 생성 입력과 산출물 지문이 포함된 job·attestation이 추가로 필요하다. | 현재 사용·기존 바이트 보존은 확인했지만 신규 생성판은 미확인. |
| “분석에 쓴 Corpus v1.1을 인용하겠다” | [v1.1 DOI](https://doi.org/10.5281/zenodo.11216814)와 `v1.1` 표시 | 실제 데이터가 필요할 때만 레코드가 제공한 [ZIP content](https://zenodo.org/api/records/11216814/files/2024-05-10-data-citation-corpus-v1.1.zip/content) 및 선언 MD5를 추가. | DOI의 성공은 ZIP 전체 다운로드·검증 성공을 의미하지 않는다. |
| “Corpus 전체 계보를 계속 찾겠다” | [concept DOI](https://doi.org/10.5281/zenodo.11196858) | 이전판이 필요하면 Versions 또는 DataCite `HasVersion`에서 원하는 판을 명시적으로 고른다. | 최신 landing을 v1.1 고정 인용으로 쓰지 않는다. |

세 주소를 매번 주면 패키지만으로 끝나는 독자에게 불필요한 직접 파일·발행 기록이 늘어난다. 반대로 단일 파일 주소만 주면 본문에서의 사용과 역사적 판 관계를 확인할 수 없다. 주소 수는 목적에 맞추되, 현재 사용과 신규 생성의 판단은 별도로 보존해야 한다.

## 4. 재현과 검토 범위

`collect.py`는 Python 표준 라이브러리로 공개 자료를 GET하고 ZIP/XML/JSON을 검사한다. 원 파일은 시스템 임시 폴더 `af098-cross-domain-cache`에만 두고 이 경로에는 요약·지문·속성만 남긴다. 비공개 데이터·인증정보는 사용하지 않는다. 패키지 생성·코드 실행은 하지 않는다.

```sh
# 새 임시 위치에서 재조회하여 기존 관측 파일을 덮어쓰지 않는다.
mkdir -p /tmp/af098-cross-recheck
cp docs/workstreams/research/AF-RES-098/evidence/cross-domain/collect.py /tmp/af098-cross-recheck/collect.py
python -B /tmp/af098-cross-recheck/collect.py
```

재조회 시 DOI API의 최신 메타데이터와 응답 지문은 바뀔 수 있다. 고정 release 패키지·소스 commit은 기존 지문과 비교하고, 새 UTC 영수증을 별도 회차로 유지한다. 결과는 자료 수집자의 자기 검산이며, 독립된 사람의 검토나 reader 실행 시험으로 부르지 않는다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 현재 참조와 동일한 과거 이미지 바이트는 확인했지만, 이미지 생성 job은 없다. | 20230704 release의 실행 로그 또는 이미지 입력·출력 SHA를 포함한 발행 attestation. | 해당 job이 `9c7fabbe…` 바이트를 새로 생성한 과정을 지목하면 생성 축을 갱신한다. 단순 복사라면 재사용 근거를 강화한다. |
| Corpus 파일 길이·MD5는 발행 목록의 값이며 ZIP 전체 바이트는 미검증이다. | 두 version API가 제공한 정확한 content URL에서 ZIP을 내려받아 MD5를 계산하고 필요시 내부 JSON을 대조한다. | 수신 MD5가 선언과 다르거나 v1.1에 인용 추가·삭제가 확인되면 payload 또는 발행 설명 판정을 바꾼다. |
| EPUB reader 동작과 concept DOI의 미래 도착은 이 정적 관측으로 보장하지 못한다. | 고정 EPUB에서 Childhood를 실제 reader로 열고, concept DOI를 새 UTC 회차에 다시 조회한다. | 내부 그림 표시가 실패하면 이용 가능성의 범위를 줄이고, concept 도착판이 바뀌면 현재 경로 기록을 갱신한다. |
