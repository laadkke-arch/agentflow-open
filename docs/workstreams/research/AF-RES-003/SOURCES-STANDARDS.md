# AF-RES-003 — 표준·다른 분야·기존 표본의 원문 확인

작성: 본 작업 작성자. 확인일: **2026-11-19 UTC / 한국 2026-11-20**. 아래 R01–R12는 검색 결과가 아니라 해당 원문 또는 고정 소스 파일을 직접 열어 관련 절을 읽었다. 시각은 이 세션의 열람 구간이며 개별 요청의 초 단위 시각은 계측하지 않았다. D1은 문서 설명, D2는 코드 관찰이다. 제품 실행·배포 일치 검사는 없다. 표준의 정보 구분을 참고하되 해당 표준·RDF·식별자를 제품 전체에 채택하자는 결론은 아니다.

## 원문 원장

### R01 — RFC 3986: 주소 비교의 목적과 한계

- URL: <https://www.rfc-editor.org/rfc/rfc3986.html>.
- 고정 위치: 2005-01 RFC 3986, §6.1–6.2.4, §7.1. D1.
- 확인: URI 비교는 용도에 따라 다르며 주소 문자열이 다르다고 다른 자원이라고 단정할 수 없다. scheme/host와 다른 구성 요소의 대소문자 규칙이 다르다. 표현을 가져올지 결정하는 비교에서는 fragment를 제외할 수 있다. 같은 주소가 미래에 같은 내용을 반환한다는 보장은 없다.
- 한계: 제품·서비스·기능의 업무상 동일성을 판정하는 규칙이 아니다. redirect의 실제 동작도 이 표준만으로 특정 사례에서 확인되지 않는다.
- 연구자 적용: 요청 중복 제거용 주소와 인용 위치를 구별한다. fragment를 지워 캐시를 합치더라도 근거 절까지 지우면 안 된다. 모든 query/path를 임의로 제거하는 정규화는 이 자료로 정당화되지 않는다.

### R02 — SKOS: 유사성과 동일성의 추론을 구별

- URL: <https://www.w3.org/TR/2009/REC-skos-reference-20090818/>.
- 고정 위치: 2009-08-18 Recommendation, §10.1, §10.6.1, §10.6.3, §10.6.8. D1.
- 확인: `closeMatch`는 일부 검색 문맥에서의 유사 대응이며 추이적이라고 선언하지 않는다. `exactMatch`는 추이적이고, `owl:sameAs`와 의미가 다르다. mapping 관계만으로 출처 관리를 대체하지 않는다.
- 한계: 개념 체계 간 mapping의 표준이다. 소프트웨어 제품의 fork·교체·라이선스·호환성을 자동 판정하지 않는다.
- 연구자 적용: 유사 메커니즘 관계를 따라 제품을 연쇄 병합하지 않는다. 반대로 “모든 동일성은 비추이적”이라는 규칙도 만들지 않는다. 관계 종류와 적용 범위를 명시하는 데만 원리를 빌린다.

### R03 — DataCite: 연구 결과의 부분·버전·계승·동일

- URL: <https://support.datacite.org/docs/connecting-to-works>.
- 위치: `Related identifiers`, `Parts and versions`, `Summary of all relationTypes`. live 문서, 불변 버전 없음. D1.
- 확인: 연구 결과 연결에 관계 종류를 붙이며 part, version, new/previous version, continuation, description, derivation, identical 등을 구별한다.
- 한계: 모든 관계 종류를 이 제품에 넣어야 한다는 근거가 아니고, 식별자를 발급했다고 실제 동일성이 입증되는 것도 아니다. 읽은 표에는 `Documents` 역방향 설명의 문구 이상도 있어 모든 예를 그대로 복사하지 않는다.
- 연구자 적용: “관련됨” 한 가지로 통합하면 병합과 후계·설명 관계를 구별하지 못한다. 작은 관계 어휘로 시작하되 실제 사례가 요구한 구분만 추가한다. 저장할 관계 수는 미결정이다.

### R04 — 미국 의회도서관 BIBFRAME 2.0: 작품·출판 형태·개별 사본

- URL: <https://www.loc.gov/bibframe/docs/bibframe2-model.html>.
- 고정 위치: `Overview of the BIBFRAME 2.0 Model`, 페이지 날짜 2016-04-21, Work/Instance/Item 설명. D1.
- 확인: 개념적 작품, 출판 형식, 실제 사본을 구별하며 출판자·형식과 사본 위치가 서로 다른 층에 속한다.
- 한계: 서지 분야의 추상화이며 소프트웨어의 제품→배포→인스턴스와 일대일 대응하지 않는다. 이 문서는 카탈로그 사용성 실험이 아니다.
- 연구자 적용: 물리 사본 위치를 작품 자체의 식별로 쓰지 않는 원리를 참고한다. 그러나 탐색기가 실제 설치 인스턴스를 관리하지 않는데도 Item에 대응하는 객체를 강제로 만드는 것은 과분할이다. **서로 다른 층을 구별하는 것과 그 층마다 저장 객체를 의무화하는 것은 다르다.**

### R05 — PROV-DM: 근거의 출처와 서로 다른 시점의 관점

- URL: <https://www.w3.org/TR/2013/REC-prov-dm-20130430/>.
- 고정 위치: 2013-04-30 Recommendation, §2.1, §2.2.2, §5.2.2–5.2.3, §5.4, §5.5.1–5.5.2. D1.
- 확인: entity/activity/agent 및 derivation을 구별한다. revision과 quotation은 파생 관계다. 날짜별 문서와 일반 문서의 관계, 같은 것의 다른 측면, 출처 기록 자체의 출처를 표현한다.
- 한계: provenance는 신뢰 판단을 돕는 기록이지 내용의 진실을 보증하지 않는다. `alternateOf`는 대체 제품이나 기능 상호교환을 뜻하는 용어가 아니다.
- 연구자 적용: 원문 주장과 연구자의 해석·정정이 어디서 생겼는지 연결한다. 같은 문서를 재인용한 링크 세 개를 독립 증거 세 개로 세지 않는다. 전체 활동 그래프를 초기에 구현할 필요는 확인되지 않았다.

### R06 — Web Annotation: 원문 부분과 당시 표현

- URL: <https://www.w3.org/TR/2017/REC-annotation-model-20170223/>.
- 고정 위치: 2017-02-23 Recommendation, §1.1, §4.2.4–4.2.5, §4.3.1–4.3.2. D1.
- 확인: 주석 본문과 대상, 대상 문서의 부분 선택, 시간·요청 표현을 구별한다. 텍스트 위치는 편집에 취약하며 상태 정보의 병용을 권한다. 문구 선택은 앞뒤 문맥을 함께 사용할 수 있다.
- 한계: selector나 확인 시각을 적어도 원문이 보관되는 것은 아니다. 동적 문서가 사라지면 당시 전체 내용을 재생할 수 없다. 원문 장문 복제를 요구하는 근거로 쓰지 않는다.
- 연구자 적용: URL과 절 이름/소스 symbol·불변 버전 또는 확인 시점·짧은 확인 요약을 함께 남긴다. 복잡한 selector는 반복된 인용 위치 손실이 실제로 생길 때 검토한다.

### R07 — Package-URL: 제품명과 패키지 좌표의 범위 차이

- URL: <https://github.com/package-url/purl-spec/blob/v1.0.0/docs/standard/specification.md>.
- 고정 위치: release tag `v1.0.0`, 읽은 blob SHA `89daef7088bcc20cff0410272ccd5c486afde505`; `Table 1`, `Rules for each PURL component`. D1.
- 확인: type·namespace·name·version·qualifiers·subpath 등으로 패키지 좌표를 구별한다. type/이름/버전의 역할과 타입별 규칙이 다르며 version은 opaque string이다.
- 한계: 태그 참조는 이동 가능하므로 blob SHA도 남겼다. 패키지 좌표의 일치는 서비스 계약·제품군·비트 내용의 동일성을 자동 보증하지 않는다. 파서 실행은 하지 않았다.
- 연구자 적용: 향후 특정 생태계 패키지를 구별해야 할 때 선택적으로 참조한다. 지금 모든 웹서비스·기능·추상 원리를 PURL로 표현하려 하지 않는다.

### R08 — SWHID: 동일 내용과 동일 문맥은 다름

- URL: <https://www.swhid.org/specification/v1.1/6.Qualified_identifiers/>.
- 고정 위치: 명시된 specification **v1.1**, §6.1, §6.2, 특히 §6.3–6.4. 최신판이라는 주장은 하지 않는다. D1.
- 확인: core 식별자와 문맥/부분 qualifier를 나눈다. 동일 artifact의 비교와 같은 문맥에서 같은 부분의 비교를 구별한다. origin이 사라질 수 있다는 한계와 중복 qualifier 생략도 설명한다.
- 한계: 이 조사에서 아카이브에 파일을 넣거나 식별자를 계산하지 않았다. §6.2.3의 content형 예시와 유효 조건 문구가 상충해 보이므로 세부 qualifier 규칙 전체를 구현 근거로 삼지 않는다. 이번 사용은 §6.3의 내용/문맥 구별뿐이다.
- 연구자 적용: 파일 내용이 같아도 어느 제품·버전에서 왜 읽었는지는 남겨야 한다. 내용 해시로 포크나 서비스의 정체성을 통합하는 것은 별도 근거 없는 추론이다.

### R09 — OSSInsight About: 제품 소개 안의 기능 구분

- URL: <https://ossinsight.io/docs/about>.
- 위치: `Feature 1: GPT-Powered Data Exploration`, `Feature 4: Repository Analytics`, `Feature 5: Compare Projects`. live 문서. D1.
- 확인: 자연어를 SQL·시각 결과로 바꾸는 Explorer와 저장소 지표·비교 기능을 별도로 설명한다.
- 한계: 소개는 현재 가동·실제 API 응답·사용자 프로젝트 적합성의 증거가 아니다. 문서 설명을 현행 배포의 실행 사실로 바꾸지 않는다.
- 연구자 적용: Explorer 관련 주장의 주어를 OSSInsight 전체와 구별한다. R10·R11과 서로 다른 근거 역할로 연결한다.

### R10 — OSSInsight의 고정 ask 라우트

- URL: <https://github.com/pingcap/ossinsight/blob/77538008b8fe8b0dd3dc6caa3fc4ba987e10360a/apps/web/app/api/explorer/ask/route.ts>.
- 고정 위치: SHA `77538008b8fe8b0dd3dc6caa3fc4ba987e10360a`; `isExplorerUnderMaintenance`, `handlePOST` 시작 분기. D2.
- 확인: 함수가 `true`를 반환하고 `handlePOST`가 생성 모델 실행 경로보다 앞에서 maintenance 응답과 HTTP 503을 반환하도록 작성되어 있다.
- 한계: 코드를 실행하거나 API에 POST하지 않았다. 이 SHA가 현재 서비스에 배포된 SHA인지 확인하지 않았다. 소스 읽기를 서비스 응답 측정으로 표현하지 않는다.
- 연구자 적용: '고정 코드의 동작 경로'를 R11의 '웹페이지 안내'와 별개로 저장한다. 같은 결론 방향이어도 서로 다른 확인 범위를 하나의 운영 검증으로 합치지 않는다.

### R11 — OSSInsight Explorer의 열람 시점 안내

- URL: <https://ossinsight.io/explore>.
- 위치: 페이지 제목과 maintenance 본문. live HTML, 불변 버전 없음. D1.
- 확인: 열람한 페이지는 Explorer가 일시 유지보수 중이라고 안내하고 다른 분석 페이지를 가리킨다.
- 한계: 안내문 확인이다. 실제 분석 API의 성공/실패·다른 페이지 가동·언제 재개될지를 시험하지 않았다.
- 연구자 적용: Explorer 안내를 OSSInsight 전체 폐쇄로 확장하지 않는다. R09와의 차이를 단순히 제품 항목 전체의 설명 교체로 처리하면 기능별 범위를 잃는다.

### R12 — DataCite의 동일 연구 결과·복수 DOI 사례

- URL: <https://support.datacite.org/docs/when-should-i-use-isidenticalto>.
- 위치: 본문의 두 원인과 DOI `10.17596/hcqn-2w70`, `10.17596/xc1g-pq91` 연결 예시. live 문서. D1.
- 확인: 같은 연구 결과를 여러 플랫폼에 두거나 이동 과정에 DOI가 중복된 경우, 식별자 사이에 `IsIdenticalTo`를 명시하는 예를 제공한다.
- 한계: 예시 DOI의 실제 데이터 파일을 내려받아 동일성을 검사하지 않았다. 이 원문이 제시한 식별 연결 사례이며 두 데이터세트의 자체 재검증이 아니다.
- 연구자 적용: 다른 주소·ID 둘을 무조건 다른 대상으로 세는 것도 오류다. 그러나 단지 주제·제목이 같다는 이유로 동일 DOI 관계를 만들 수는 없다. 소프트웨어의 별칭·mirror 판정도 귀속 근거를 요구한다.

## 다른 분야에서 옮길 것과 옮기지 않을 것

| 분야·근거 | 참고할 구분 | 그대로 적용하면 실패하는 경우 |
| --- | --- | --- |
| 연구자료 DOI (R03/R12) | 동일, 부분, 버전, 계승을 별도 관계로 말함 | 연구자 추정을 발행자의 동일성 선언으로 바꾸거나 모든 관계 어휘를 먼저 구현함 |
| 도서관 서지 (R04) | 추상 작품과 구체 발행물·사본의 속성 범위를 구별 | 설치본을 관리하지 않는 제품에 사본 객체를 의무화함 |
| 개념 사전 (R02) | 근접 대응을 추이적 병합으로 취급하지 않음 | 서로 비슷한 메커니즘을 하나의 재사용 코드로 합침 |
| 디지털 아카이브 (R08) | 내용 동일성과 출처 문맥을 분리 | 같은 파일 해시를 같은 제품·운영조건의 증명으로 사용함 |
| 주석·provenance (R05/R06) | 말한 내용, 원문 위치, 시점, 해석의 계보 | 기록 구조만으로 원문 진실·최신 상태·독립 근거 수를 보증함 |

## 실패·탐색 보조 기록 (원문 20개 집계에 추가하지 않음)

| 주소/접근 | 관측한 내용 | 한계·처리 |
| --- | --- | --- |
| <https://support.datacite.org/docs/connecting-works> | 접근 오류 | 잘못된 경로. 내용 미열람, 올바른 R03으로 이동 |
| <https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html> | Access Denied 페이지 | 본문 미열람, 우회하지 않음. 별도 공식 규격 R08 사용 |
| <https://www.softwareheritage.org/software-heritage-faq/> | 502 | 검색 snippet만으로 본문을 읽었다고 하지 않음 |
| <https://github.com/package-url/purl-spec/blob/main/PURL-SPECIFICATION.rst> | 본문이 새 docs 위치를 안내하는 7줄 파일 | 기술 규격 본문이 아님. R07 발견용 |
| <https://www.packageurl.org/docs/purl/introduction> | 실제로는 프로젝트 개요·표준·릴리스 링크를 반환 | 패키지 상세 규칙 근거는 R07에 한정 |
| <https://github.com/package-url/purl-spec/releases/tag/v1.0.0> | 릴리스 위치 확인 | 별도 사례 수로 세지 않음 |
| GitHub `/repos/package-url/purl-spec/contents/docs?ref=v1.0.0` 및 `/docs/standard?ref=v1.0.0` | 파일 경로와 blob SHA 목록 확인 | 디렉터리 메타데이터, 내용 근거는 R07 |
| IFLA LRM·Software Heritage citation/URI 페이지의 검색 결과 | 관련 원문 후보의 제목·snippet 발견 | 원문은 열지 않아 근거·원문 수에서 제외; 서지 비교는 직접 읽은 R04로 한정 |

검색은 관련 공식 문서 발견에만 사용했다. 주요 질의는 `RFC3986 comparison ladder`, `SKOS exactMatch closeMatch transitive`, `DataCite IsVersionOf IsIdenticalTo`, `SWHID qualifiers origin anchor path lines`와 공식 도메인 제한이었다. 새로운 검색 성능·후보 순위는 조사하지 않았다.

## 작성자의 추가 대조

본 작성자는 하위 조사 원장만 합치지 않고 I05/I08와 M01/M02/M03/M06/M07/M08의 공식 원문을 다시 열어 핵심 절을 읽었다. 이 재열람은 자료 수에 중복 가산하지 않는다. 별도 검토자의 원문 대조와 이견은 `REVIEW.md`에 기록한다.
