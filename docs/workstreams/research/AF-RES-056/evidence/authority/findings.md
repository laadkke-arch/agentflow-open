# Q7 · 전거 관계를 기능명 연결에 옮길 수 있는 조건

작성자: `/root/authority_records` 하위 에이전트. 독립 외부 검토나 독자 실험이 아니라, AF-RES-056 안에서 분담한 원문 조사다. 구현 목록·구현 공급자 목적지는 읽지 않았으며 소프트웨어 후보 선정이나 L/V 순위를 만들지 않았다.

## 직접 확인한 네 개의 배당 레코드

| 사례·출처 ID | 정확한 개념·원문 | 같은 개념의 표현 | 상하위와 연관 관계 | 확인 경계 |
| --- | --- | --- | --- | --- |
| AUTH-LC1 | [Engraving / sh85043995](https://id.loc.gov/authorities/subjects/sh85043995.json) | `skos:prefLabel`은 Engraving. `altLabel`에는 Engravings와 Line-engraving 등 5개가 있다. | `broader`: Graphic arts, Prints. `narrower`: Bamboo engraving 등. `related`: Etching의 sh85045046. | 이형어·상하위·연관은 서로 다른 필드다. 관계가 있다는 사실을 동일 처리 방식이나 대체 가능성으로 승격하지 않는다. |
| AUTH-LC2 | [Etching / sh85045046](https://id.loc.gov/authorities/subjects/sh85045046.json) | Etching이 표준표목이고 Etchings가 이형어다. | `broader`: Art, Prints. `narrower`: Aquatint 등. `related`: Engraving의 sh85043995. | 같은 표목의 JSON·HTML·연례 발행본은 한 레코드다. 연결된 모든 표목을 별도 읽은 것으로 세지 않았다. |
| AUTH-AAT1 | [paintings (visual works) / 300033618](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=&subjectid=300033618) | 복수 선호어와 단수 `painting (visual work)`가 같은 레코드에 있다. | Objects 계층에 속한다. 제작 행위 300054216으로 `produced by`가 붙는다. | 범위 주석은 안료를 적용해 만들어진 작품을 설명한다. 제작 행위 자체의 동의어가 아니다. |
| AUTH-AAT2 | [painting (image-making) / 300054216](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300054216) | 선호어와 `painted (image-making)`라는 문법적 대체표현이 같은 레코드에 있다. | Activities 계층이다. 작품 300033618로 `produces`, coating 300161986으로 `distinguished from`이 붙는다. | 이미지 제작 목적과 표면 보호·일반 착색 목적을 범위 주석이 구분한다. 관련 목적이나 같은 어근만으로 합치면 틀린다. |

AAT의 두 canonical URI는 각각 `http://vocab.getty.edu/aat/300033618`, `http://vocab.getty.edu/aat/300054216`이다. 실제로 읽은 URL은 Getty가 제공하는 Full Record Display다. semantic-view URL의 웹 도구 403과 Full Record Display의 정상 HTTP200을 함께 보존했다. 레코드 상세창은 상위 경로를 보이지만 직접 하위어를 열거하지 않았으므로, 하위어가 없다고 판정하지 않는다.

`authority-records.json`은 관계와 범위를 구조화한 발췌이며 `*.receipt.json`은 실제 응답 시간·URL·HTTP 상태·바이트 수·SHA-256이다. LOC 원문 JSON 세 개는 미국 정부 전거 데이터로 보존했다. Getty 원문 전체·인용 사전 전문은 저장하지 않았다. Getty 두 영어 범위 주석의 출처는 레코드 내 Note 항목에서 각각 VP와 Grove/Oxford 자료, VP와 Grove/Legacy AAT 자료로 표시된다. 인용된 사전 자체는 열지 않았으므로 별도 원문 배당에 넣지 않는다.

## 같은 철자를 다른 개념으로 잘못 연결할 뻔한 반례

검색 경로에서 얻은 [Etching / sh00005643](https://id.loc.gov/authorities/subjects/sh00005643.json)은 공개 JSON을 읽자, 개별 재료나 재료 종류 아래에 붙이는 주제 세목이라는 사용 주석이 드러났다. 표준표목의 철자는 sh85045046과 같지만 URI와 사용 범위가 다르다. 반면 Engraving 레코드가 실제 `related`로 연결하는 대상은 sh85045046이다. 따라서 처음 발견한 URI를 이름만 보고 채택하지 않고 두 JSON의 구조를 대조했다. sh00005643은 추가 진단이며 필수 4개 배당을 채우는 주표본과 구분한다.

이는 이번 과제의 구체적 반례다. 올바른 철자를 얻어도 **레코드의 역할·범위가 다르면 같은 기능으로 번역되지 않는다.** 또한 Engraving과 Etching 사이의 `related`를 동의 관계로 읽으면 두 개념을 잘못 합친다. 이 관측은 소프트웨어 L/V 오탐 수에 합산하지 않는다.

## 공식 편집 규칙에서 가져올 수 있는 것

[Getty 계층 규칙 §3.1.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.1/)은 상하위 관계와 표시용 가이드 표제를 구분한다. 대괄호 모양의 가이드 표제 아래에 함께 있다는 이유만으로 그 소속 항목들이 같은 개념인 것은 아니다. [용어 규칙 §3.3.1·3.3.3·3.3.4·3.3.15](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/)는 개념 ID·용어 ID·선호어·한정어·용어 출처를 구별한다. [연관 규칙 §3.5.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.5/)은 동의·계층 관계에 들어가지 않는 직접적인 연관을 별도로 관리한다. 세 절은 같은 편집 매뉴얼 하나이며 세 저작으로 세지 않았다.

소프트웨어로 옮길 제안은 다음 조건에 한정한다.

1. **동일한 개념·입출력·범위를 지지하는 근거가 있는 표현**만 V의 같은/정의 관계로 추가한다. 같은 어근, 연관, 상하위라는 사실만으로는 허용하지 않는다.
2. 표준 명칭뿐 아니라 개념 URI·해당 절·판·입출력 방향을 함께 남긴다. 작품과 제작 행위의 관계처럼 처리와 산출물은 서로 관련되어도 치환 가능한 표현이 아니다.
3. 표목의 이형어는 그 전거의 검색·목록 목적에 맞는 접근점이다. 이를 소프트웨어 동작의 엄격한 동일성 증명으로 그대로 복제하지 않는다. 특히 LOC의 이형어 집합에 놓였다는 사실만으로 알고리즘·옵션의 동일성까지 판단하지 않는다.
4. 목록에 기능 필드가 없을 때, 좋은 전거를 추가해도 후보에 그 기능이 게시되었다고 만들 수는 없다. 이는 전거 관측에서 얻은 설계 제안이며 이번 L/V 실측 효과를 대신하지 않는다.

## 사용자·편집자·유지보수자에게 남길 링크

| 독자 | 먼저 확인할 근거와 링크 | 소프트웨어 적용 시 필요한 추가 근거 |
| --- | --- | --- |
| 사용자 | [제작 행위의 범위 주석과 구분 관계](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300054216): 결과물·처리 목적을 구분하는 예 | 본인 질문의 원문·입력·출력·부정 조건. 표준명이 의도를 바꾸지 않았는지 확인할 수 있어야 한다. |
| 목록 편집자 | [용어·한정어·용어 출처 규칙](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/), [Engraving의 필드별 관계](https://id.loc.gov/authorities/subjects/sh85043995.json) | 게시 필드에 붙인 별칭의 발행자 근거·동일 개념 여부·목록판·원순서. 목적지 판정 결과를 목록 필드에 역으로 채우지 않는다. |
| 구현 유지보수자 | [같은 Etching 철자의 세목 레코드](https://id.loc.gov/authorities/subjects/sh00005643.json)와 [독립 표목 레코드](https://id.loc.gov/authorities/subjects/sh85045046.json) 대조 | 표준판·구현판·환경·옵션·같은 입력의 결과가 있어야 한다. 같은 기능명만으로 구현의 두 조건 충족을 보장하지 않는다. |

## 수용·반증·최소 재개 자료

핵심 전거 배당은 LOC 2개와 AAT 2개로 4/4다. 추가 LOC 세목 1개는 진단이다. 출처 로그는 성공·실패·동일 레코드 재표현을 분리하며, 자료 수는 `source-counts.json`을 따른다. 확인 시점은 현재 재탐색이며 2021~2024 질문 시점의 당시판 재구성이 아니다.

결론을 뒤집을 조건은 다음과 같다. 해당 URI가 병합·폐기되었거나 원문 관계를 다른 의미로 판독했음이 밝혀지면 사례별 분류를 다시 해야 한다. 더구나 표현이 같아도 소프트웨어의 실제 두 조건을 보존하지 못하면 V에 추가할 수 없다. 후속 작업의 최소 입력은 해당 표준판의 정의·양성 및 근접 음성 입출력, 게시 목록 필드, 구현판별 판정 자료다. 전거 예제만으로 L/V의 완결률·오탐률 증가나 일반 분야 성능을 주장하지 않는다.
