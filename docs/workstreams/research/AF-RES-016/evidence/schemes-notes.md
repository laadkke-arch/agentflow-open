# AF-RES-016 Q1/Q2 원문 비교 메모

범위: Q1 분류 체계, Q2 다른 분야의 문맥·역할 처리. 내부 별도 문헌 담당은 코딩 표본이나 새 라벨을 읽지 않았다. 아래는 분류 일치도 측정 결과가 아니라 실제 본문에서 확인한 설계 원칙이다. 확인 시점은 2026-11-20 UTC이며 주소·절·한계·실패는 [schemes-sources.json](schemes-sources.json)에 있다. 본문을 직접 읽은 핵심 자료는 **21개**다. GitHub raw를 하나의 사이트로 합쳐도 사이트당 최대 3개이다. 검색 snippet, 다른 판 중복, 안내 링크는 개수에서 제외했다.

## 1. Q1 체계 비교표

| 체계 | 역할 값·구조 | 나누는 기준 | 경계 처리 | 출처 ID |
| --- | --- | --- | --- | --- |
| SPDX 3.0.1 | SoftwarePurpose 29값; primaryPurpose 0..1, additionalPurpose 0..* | Element가 **사용되는 방식**에 관한 producer/consumer의 추정. 형태·포장·사용 목적 혼합 | 내용의 본질 속성이라고 명세가 말하지 않는다. 대표 목적과 추가 목적을 함께 기록 가능 | S01–S02 |
| CycloneDX 1.7 | component.type 13값; scope 3값; isExternal; 포함·의존 관계 | type은 주된 객체 종류, scope/isExternal은 실행·배포 관계 | 적합한 구체 type을 못 정하면 application. reusable code가 framework 특성도 가지면 framework. 포함 계층과 의존 트리는 별개 | S03 |
| PyPI Trove | Framework::생태계/프레임워크/하위 확장; Topic::분야; Environment::Plugins | release 단위 복수 facet | Framework::Django는 그 배포물이 프레임워크 자체라는 보장이 아니다. extensions/providers/recipe 하위값으로 연결 방식을 표현. 목록이므로 다중 기술 가능 | S04–S05 |
| Debian debtags | role::14값(TODO 포함); 별도 scope::application/suite/utility | 배포 package의 기능·개발/실행 단계와 범위 | devel-lib, shared-lib, plugin을 구별. source와 program도 구별. 적절한 tag가 없을 때 TODO로 vocabulary 부족 표시 | S06 |
| Libraries.io | Project, Repository, Repository Projects | Project는 package와 그 versions; repository는 소스 저장소 | 하나의 저장소를 여러 packages가 참조 가능. project=완제품, package=부품의 이분법은 공식 API와 맞지 않음 | S07–S08 |
| ecosyste.ms | Package(registry_id+name), Version, repository_url | registry 유통 단위와 저장소 연결 | 같은 repository URL을 공유하는 다른 package를 찾는 모델 함수가 존재. 패키지/저장소 경계와 전체/부분 기여를 분리해야 함 | S09–S10 |
| Wikidata software classes | P31 instance of / P279 subclass of / P361 part of / P1382 partially coincident with | 개체·집합의 포함 관계와 부분 관계 | software library는 software component의 하위 class이면서 software package와 일부 중첩. P279와 P361을 역할로 혼합하면 오류 | S11–S12 |
| NVD CPE / NIST CPE 2.3 | part: a/o/h; target_sw 별도 | applications / operating systems / hardware 제품 종류 식별 | a는 앱 대 라이브러리 대 프레임워크를 충분히 분해하지 않는다. target_sw가 실행 환경을 따로 기술 | S13 |

### 1.1 SPDX 3.0.1 enum 전체

`application`, `archive`, `bom`, `configuration`, `container`, `data`, `device`, `deviceDriver`, `diskImage`, `documentation`, `evidence`, `executable`, `file`, `filesystemImage`, `firmware`, `framework`, `install`, `library`, `manifest`, `model`, `module`, `operatingSystem`, `other`, `patch`, `platform`, `requirement`, `source`, `specification`, `test`.

확인 절은 [SoftwarePurpose의 Description/Entries](https://spdx.github.io/spdx-spec/v3.0.1/model/Software/Vocabularies/SoftwarePurpose/)이다. 값 수는 29개다. `primaryPurpose`를 S1처럼 후보 하나의 영구적 본질로 읽으면 본문이 정한 사용 목적 의미를 잃는다. 다만 producer 관점의 일반 용도를 기록하는 것은 가능하므로, 이것이 곧 사용자 문제별 S2 역할의 정답이라는 주장도 성립하지 않는다. [SoftwareArtifact](https://spdx.github.io/spdx-spec/v3.0.1/model/Software/Classes/SoftwareArtifact/)의 추가 목적 반복성이 다의성을 남기는 방식이다.

### 1.2 CycloneDX 1.7 enum 전체와 관계

`application`, `framework`, `library`, `container`, `platform`, `operating-system`, `device`, `device-driver`, `firmware`, `file`, `machine-learning-model`, `data`, `cryptographic-asset` — 13개.

`scope`는 `required`, `optional`, `excluded` 세 값이다. optional은 런타임에서 설치되지 않았거나 접근 불가하여 호출할 수 없는 경우를 뜻하며, 설치됐으나 설정상 호출을 막은 구성은 required로 분류하는 명시 규칙이 있다. `isExternal=true`는 assembly에 포함되지 않고 배포 환경이 제공하는 런타임 구성요소를 나타낸다. 같은 library도 실제 assembly와 실행 문맥에 따라 이 관계 필드는 달라질 수 있다. [`components`](https://cyclonedx.org/docs/1.7/json/)는 부모에 포함된 조립 계층이며 dependency tree가 아니다. 따라서 type/포함/의존/사용 문맥을 하나의 product/component 라벨에 접어서는 안 된다. 이 문단의 해석은 S2의 전체 대체·부분 채움과의 동일시가 아니다.

### 1.3 Debian role enum 전체

`role::TODO`, `role::app-data`, `role::data`, `role::debug-symbols`, `role::devel-lib`, `role::documentation`, `role::dummy`, `role::examples`, `role::kernel`, `role::metapackage`, `role::plugin`, `role::program`, `role::shared-lib`, `role::source` — TODO 포함 14개. [공식 vocabulary](https://packages.debian.org/about/debtags)의 role 절을 직접 읽었다.

`devel-lib`는 개발·빌드에 쓰이는 library/header, `shared-lib`는 다른 프로그램이 쓰는 공유 라이브러리, `plugin`은 호스트 프로그램/시스템을 확장하는 연결 가능한 조각이다. `program`은 실행 가능한 프로그램이다. 이 차이는 코드베이스 이름 하나가 아니라 **어느 배포 package를 관측했는가**에 달려 있다. scope facet의 application/suite/utility는 역할과 별도로 범위 크기를 기록한다.

### 1.4 PyPI 구조의 경계 사례

Framework에는 `Apache Airflow :: Provider`, `Buildout :: Extension`, `Jupyter :: JupyterLab :: Extensions :: Prebuilt`, `OpenTelemetry :: Instrumentations` 같은 연결 종류가 있다. Topic의 `Software Development :: Libraries :: Application Frameworks` 및 `Python Modules`와 Environment의 `Plugins`가 별도로 존재한다. 이들은 hierarchy 아래의 복수 기술어이며 한 후보를 완성품/부품/원리 중 하나로 강제하는 enum이 아니다. release 단위 목록이라는 설계는 [PEP 301](https://peps.python.org/pep-0301/)에서 확인했다.

## 2. Q2 다른 분야의 원문 사례

| 분야·체계 | 기준·값 | 같은 대상의 다른 역할을 처리하는 방식 | 실제 원문 사례·위치 | 출처 ID |
| --- | --- | --- | --- | --- |
| 특허 CPC | 기능 중심 / 적용 중심; invention/additional information; 복수 분류 | 기능과 특정 사용처가 모두 본질이면 양쪽. 기능/적용 구분도 분류 장소 사이의 상대적 관계 | C08L의 고분자 조성물과 C09D coating/C09J adhesive/C09G polish; leaf spring와 차량 현가장치, GPS와 자율 제어 | S14–S16 |
| 도서관 MARC 655 | genre/form/physical characteristics; form subdivision $v, topical subdivision $x, materials specified $3 | 자료가 어떤 형식인가와 어떤 topic subdivision으로 한정되는가를 별도 필드 요소로 표현하며 대상 부분도 지정 | 655 정의와 subfields; 자료의 부분을 특정하는 $3 예 | S17 |
| 임상 연구 PICO | Population / Intervention / Comparison / Outcome; review/synthesis/study 수준 | 비교 질문을 먼저 정한다. 같은 치료의 용량·시간·기간 변화도 비교 가능하며 A/B 위치는 비교 설계의 역할 | Cochrane §3.1, §3.2.3: intervention A vs B, 같은 intervention의 조건 변화; §3.2.3.1 공동 치료 양팔 처리 | S18 |
| 소프트웨어 패턴 | pattern / idiom / framework; 지식 표현 / 구현 수준 / 반완성 응용 | pattern은 문제·문맥·해결 관계, idiom은 언어의 구체 구현, framework는 재사용 가능한 구조와 코드. idiom이 design pattern을 구현해 경계 중첩 가능 | POSA Chapter 4 §4.1; frameworks paper §3–4 | S19–S21 |

### 2.1 기능/적용을 양쪽 기록하는 CPC

IP Australia의 [공식 분류 지침](https://manuals.ipaustralia.gov.au/patent/4.2.2.3-classifying-in-function-oriented-and-application-oriented-places)은 사용처가 단지 언급되고 충분히 제시되지 않으면 기능 중심 분류를, 대상의 기능과 특정 적용이 모두 핵심이면 양쪽을 사용한다. 모호함을 언제나 단일 라벨로 해소하는 체계가 아니다. 이 원칙은 대상의 형태와 문제 기여를 분리하자는 근거이면서 **S2도 하나의 역할만 갖는다는 가정에 대한 반례**다. 하나의 장치가 조립체의 일부이면서 특정 적용의 전체 해결인 경우가 가능하다.

### 2.2 형식과 주제를 분리하는 서지 기술

[MARC 655](https://www.loc.gov/marc/bibliographic/bd655.html)는 genre/form 및 physical characteristics를 지정한다. 반복 가능한 필드, topical/form subdivisions, 적용 부분 지정은 같은 자료의 여러 서술 관점을 보존한다. 이를 S3에 적용하는 것은 연구자 추론(H)이다. 문헌은 S3가 더 잘 일치한다거나 판정을 개선한다고 말하지 않는다. 또한 읽기 실패한 MARC 650·LCGFT 교육자료를 근거로 추가 예를 만들어 넣지 않았다.

### 2.3 PICO의 역할은 비교 관계에 속한다

[Cochrane Handbook §3.2.3](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-03)은 intervention 종류만 정해서는 부족하고 비교를 정해야 한다고 한다. 고정된 약물 이름은 A 대 B 비교의 어느 위치인지 스스로 결정하지 못한다. 같은 치료의 다른 용량도 양팔이 된다. 이 사례는 후보 정체성의 안정성과 관계 역할의 안정성을 별도 질문으로 다뤄야 한다는 근거다. 실제 임상 성과·약효 주장은 이 연구와 무관하다.

### 2.4 패턴/관용구/프레임워크의 겹치는 경계

[원저 POSA §4.1](https://www.oreilly.com/library/view/pattern-oriented-software-architecture/9781118725269/9781118725269_c04.xhtml)의 공개 본문에서 idiom이 design pattern의 구체 구현을 직접 다룰 수 있으므로 둘의 선명한 경계가 없다는 설명을 읽었다. [프레임워크 논문](https://www.dre.vanderbilt.edu/~schmidt/PDF/schmidt-fosp.pdf)은 framework를 제품군 아키텍처와 협력 컴포넌트로 설명한다. 이를 단순히 '크니까 product' 또는 '재사용하니까 작은 component'로 해석하면 규모·완결성·기여 관계를 혼동한다. 형태축 자체에도 다의성이 남으므로 S3의 축 분리는 분석 투명성을 높일 가능성(H)이지 자동 일치 보장이 아니다.

## 3. 반증 검색 기록

실제 수행한 검색 주제를 재현 가능한 질의 형태로 남긴다. 결과 판정은 읽은 본문에만 의존한다.

| 반증하려 한 주장 | 검색 질의·탐색 | 열린 자료와 결과 | 이 연구에서 허용되는 결론 |
| --- | --- | --- | --- |
| 기존 SBOM은 후보의 고정 본질만 기록한다 | `SPDX 3.0 software_primaryPurpose SoftwarePurpose`; `CycloneDX component type scope dependency` | S01은 사용 방식·관점의 추정, S02 추가 목적, S03 scope/isExternal/assembly가 있다 | **반례 확보.** 기존 체계에도 사용 문맥과 복수 목적 표현이 있다 |
| project는 완성품, package는 부품을 뜻한다 | `Libraries.io project package API`; ecosyste.ms 공식 README 및 model 확인 | S07 Project=package+versions, S08/S10 저장소와 유통물 연결 | **반례 확보.** 명칭으로 완성품/부품 역할을 대체할 수 없다 |
| 기능 또는 적용 중 하나만 골라야 일관된다 | `CPC function-oriented application-oriented classification`; `C08L relationships C09D C09J` | S15 실제 고분자 용도 분기, S16 양쪽 분류 및 상대 구별 허용 | **반례 확보.** 문맥 역할도 복수일 수 있다 |
| 형태축은 언제나 명료하다 | `pattern idiom framework original POSA idioms`; 원저 Chapter 4 열람 | S21은 design pattern/idiom 사이 겹침을 명시, S20 framework의 복합성 | **개념 반례 확보.** 실제 S3 낮은 일치 표본 여부는 별도 실행으로 확인해야 한다 |
| 같은 약·장치의 역할은 항상 고정된다 | `PICO same intervention comparator Cochrane`; CPC 공식 지침 | S18 치료 A/B·용량 비교, S16 장치/조립체 기능 | **반례 확보.** 관계 역할은 문제/비교 구성이 필요하다 |
| 문맥 상대성이 존재하므로 S1은 어디서나 쓸모없다 | `Debian debtags role program documentation shared-lib`; `CPE part a o h` | S06 분명한 배포 단위, S13 안정된 상위 제품 종류 식별 | **반박 가능성 유지.** 문맥 없이 합의 가능한 형태 범주가 있을 수 있으나 거의 완전 일치는 실제 코딩으로 확인해야 한다 |
| 역할 설명을 추가하면 반드시 판단이 좋아진다 | 공식 문서에서 목적·관련성·정체성 분리 여부를 탐색 | S03 type와 scope가 다르고 S13 a는 추천 완결성이 아님; 성과 비교 실험은 이 자료들에 없음 | 개선 보장은 미확인. 역할을 필수 요구 충족의 대리 지표로 읽는 오용 경로만 확인 |

## 4. 코드북·분석에 대한 함의 (연구자 추론 H)

1. **관측 단위를 먼저 고정한다.** 저장소, 배포 package, 특정 artifact, 서비스와 문서를 같은 이름의 후보로 뭉치면 형태 분류의 불일치가 역할 이론의 실패처럼 보인다. S07–S10은 그 단위가 실제로 구별됨을 보여준다.
2. **형태·일반 목적·해당 문제 기여·적용 가능성은 다른 질문이다.** S1의 대표 목적 하나는 압축된 색인에 유용할 수 있지만, 그것만으로 H/T나 근접 오답을 결정해서는 안 된다. 이 권고는 설계 원칙으로서 H이며 Q7 실행 결과가 아니다.
3. **S3의 전체 일치와 축별 일치를 구별한다.** 두 축의 정확 일치는 각 축의 정확 일치보다 높아질 수 없다. 이 산술적 특성을 무시하면 S3가 더 풍부한 기록을 한다는 이유만으로 불리해지거나 유리해진다.
4. **문맥이 있다고 하나의 역할이 정해진다고 가정하지 않는다.** CPC와 idiom 반례는 '실제 다의성'을 '코드북 부족'과 구별할 근거다. 복수 가능성을 기록하되 이번 단일라벨 실험의 우선 규칙은 코딩 전에 동결해야 한다.
5. **문헌의 기준은 일치도 수치가 아니다.** 공식 spec은 intended semantics의 근거, 고정 코드는 implemented units의 근거다. 어느 분류안이 실제 표본에서 우세한지는 Q5/Q6로 남긴다.

## 5. 한계

이 묶음은 Q1/Q2 원문 21건을 읽은 문헌 작업이다. 50% 일치가 낮은지의 경험적 기준, 실제 198단위의 결과, 30개 판정 영향은 측정하지 않았고 다른 담당 결과를 보지 않았다. PyPI·Debian·Wikidata live vocabulary는 이후 바뀔 수 있어 열람 날짜와 절을 기록했다. 라이브러리/프레임워크/플러그인의 실제 복합 사례에서 단위 선택까지 재현되는지는 실행으로 확인해야 한다. 공식 API 문서 일부는 웹 도구가 막혔지만 공개 본문 또는 고정 공개 코드는 일반 HTTPS로 읽을 수 있었고, 인증·비공개 접근·네트워크 제한 우회는 하지 않았다. 접근 실패 또는 snippet만 본 자료는 원장의 excluded에 남겨 최소 개수에서 제외했다.
