# Q7 — 실제 전거 네 레코드로 확인한 이름·관계·지원 증거의 경계

조사자: `/root/authority`(동일 작업 내 보조 조사자). 관측일: 2026-11-23 UTC. 신규 Stack Overflow 본문·답·점수·공급자 기능표는 열지 않았다. 실제 읽은 범위는 아래 네 개념 레코드와 두 공식 매뉴얼의 지정 절이다. 독립된 외부 사람의 검토나 AF-RES-060 전체 실험의 독립 재현은 아니다.

## 1. 직접 확인한 네 개념

| 원저작·판 식별 | 실제 필드·위치 | 확인한 접근점과 경계 | 소프트웨어에 옮길 때의 제한 |
| --- | --- | --- | --- |
| LOC `sh85077598`, [JSON](https://id.loc.gov/authorities/subjects/sh85077598.json), [MARCXML](https://id.loc.gov/authorities/subjects/sh85077598.marcxml.xml); 005=`20130715093454.0` | XML L24–34, 150/450/550; JSON 주 @id의 variant/earlier/broader/narrower | Lithography의 450에는 Lithographs와 `$w=nne`가 있다. Prints는 `$w=g`인 550이다. JSON에서는 Offset printing이 narrower로 연결된다. | 이전 채택 표제에서 현재 표제로 가는 검색 접근점을, 모든 분야에서 행위와 산물이 같은 뜻이라는 주장으로 바꾸면 안 된다. |
| LOC `sh85094211`, [JSON](https://id.loc.gov/authorities/subjects/sh85094211.json), [MARCXML](https://id.loc.gov/authorities/subjects/sh85094211.marcxml.xml); 005=`19941003143939.9` | XML L15–39, 150/450/550; JSON의 related/narrower | Offset printing의 450 두 개는 Lithoprinting, Printing, Offset. Lithography는 상위 550이고 Lithography, Direct는 다른 550 관계다. JSON에는 Offset lithography가 narrower이다. | 이형 표제·상위·관련 개념은 서로 다른 탐색 동작이다. URI와 관계 코드를 버리고 문자열 배열로 합치면 경계가 사라진다. |
| Getty AAT `300053279`, [공식 전체 레코드](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=work&page=1&subjectid=300053279), [개념 URI](http://vocab.getty.edu/aat/300053279) | ID, Note, Terms, Related concepts; 웹 L15–31, L67–75 | 중간 표면을 거친 전사를 다루며 lithographic 원이미지인 경우 별도 용어를 안내한다. 300192900과 `distinguished from`이다. | 같은 전사 과정이 있어도 추가 조건이 있는 개념을 자동 동의어로 저장하지 않는다. |
| Getty AAT `300192900`, [공식 전체 레코드](https://www.getty.edu/vow/AATFullDisplay?find=&logic=null&note=&page=1&subjectid=300192900), [개념 URI](http://vocab.getty.edu/aat/300192900) | Note, Terms, hierarchy, Related concepts; 웹 L15–26, L45–60 | lithographic 원이미지라는 조건을 포함한다. 앞 개념과 구별되며 산물과 장비에는 각각 다른 방향의 관계를 둔다. | 관련 산물·필요 장비의 이름은 그 개념의 대체어가 아니다. 기능 이름과 입력·산출물·외부 의존물을 분리할 필요가 있다. |

LOC의 JSON과 MARCXML은 각각 하나의 같은 전거를 표현한다. JSON에 딸려온 상대 전거의 요약 노드, 외부 closeMatch 주소, Getty 레코드가 인용한 인쇄사 책은 독립적으로 읽은 저작으로 세지 않았다. Getty는 현재 동적 레코드이며 과거 판의 동일성을 주장하지 않는다. 두 HTML 응답의 SHA256과 수신 시각은 [acquisition.json](acquisition.json)에 있다. LOC 원자료·해시는 [loc-acquisition.json](loc-acquisition.json), [marc-acquisition.json](marc-acquisition.json)에 있다.

## 2. MARC 4XX/5XX를 단순 동의어/관련어라는 두 칸으로 축소할 때의 반례

[4XX 설명](https://www.loc.gov/marc/authority/ad4xx.html)은 채택되지 않은 표제형·이형 접근점을, [5XX 설명](https://www.loc.gov/marc/authority/ad5xx.html)은 다른 채택 표제와의 연결을 다룬다. [Tracings and References](https://www.loc.gov/marc/authority/adtracing.html)의 `$w/0`과 `$w/2`가 더 구체적인 구분을 담당한다. 이 세 절은 **하나의 MARC 전거 형식 저작**으로 집계했다. 표제별 지침의 표시일은 2016-11, 종합 tracing 절은 2017-05다. 직접 HTTP 캐시는 403이었지만 웹 도구가 공식 본문을 성공적으로 제공했고, 그 결과의 정의·범위 및 제어값 절을 직접 읽었다.

실제 Lithography의 `450 $w=nne`는 이름만 보면 일반 이형어처럼 보이지만 세 번째 문자 `e`는 이전 채택형이라는 이력을 담는다. Offset printing의 `550 $w=g`에서 `g`를 지우면 상위 개념과 그 밖의 연관을 구별하지 못한다. 따라서 **목록의 질의 확장에 쓸 이름**과 **관계 설명에만 쓸 이름**은 별도로 유지해야 한다. 이 주장은 실제 전거 구조의 관측에 근거하며, 소프트웨어 검색 성능 향상은 이 조사만으로 측정되지 않았다.

## 3. Getty 지침과 실제 레코드가 함께 보여 준 반증

[Terms §3.3.1.3·3.3.2.4](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.3/)는 concept/term ID와 같은 철자의 다른 개념을 구분한다. [Scope Note §3.4.1](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.4/)는 문맥 속 사용 범위를 정한다. [Associative Relationships §3.5.1–2](https://www.getty.edu/publications/vocabularies-editorial-guidelines/aat-guidelines/3_editorial_rules/3.5/)는 직접 관계·종류·방향을 요구한다. 세 절은 **Getty 편집 매뉴얼 한 저작**이며 AF-RES-056이 이미 사용한 저작의 재열람이다.

새 레코드 쌍의 근접 음성은 **중간 매체로 전사하지만 원이미지가 lithographic 방식으로 만들어지지 않은 경우**다. 이 경우 일반 전사 조건만으로 더 좁은 개념을 붙이는 결론은 범위 주석과 충돌한다. 이는 실제 인쇄 시험이 아니라 원전의 구별 조건에서 도출한 판정 예다. 두 레코드에 비슷한 철자와 공통 장비가 있다는 사실은 이 차이를 없애지 않는다.

LOC와 Getty의 편집 선택을 보편 단일 동의어표로 합치는 것도 피해야 한다. LOC 표제는 문헌의 접근점과 역사적 채택형을 포함하며 Getty는 명시적 개념 범위를 제공한다. 두 체계가 오류 없이 완전히 일치한다는 가정은 이번 자료가 지지하지 않는다. 차이가 나타난다고 어느 한쪽 전체가 틀렸다고 판정하지도 않는다.

## 4. 소프트웨어 F1에 옮길 수 있는 것과 멈출 지점

여기서 옮길 수 있는 것은 **원래 기능 표기, 개념 ID, 정의 판·절, 관계 종류·방향, 출처, 갱신 시 재확인할 경계**다. 이런 기록은 사용자 표현과 공급자 표현을 비교할 근거를 제공한다. 특정 구현의 C1·C2·환경이 같은 버전에서 함께 지원된다는 증거는 추가로 필요하다. 전거는 구현판·실행 결과·옵션을 기록한 시험 영수증의 역할을 하지 않는다.

| 관점 | 원전에서 얻는 것 | 재확인할 최소 항목 | 반환 판단에 미치는 영향 |
| --- | --- | --- | --- |
| 공급자 유지보수자 | 자기 기능 이름의 의미·방향을 명시할 표준 구조 | 구현판, 직접 지원인지 위임인지, 선택 옵션, 양성/근접음성 | 기능 목록의 문구를 공동 조건 지원 주장으로 넓히기 전에 같은 판의 근거 필요 |
| 목록 편집자 | 용어 출처·개념·관계 분리 | 기능 절 위치·원표기·정의 판·엔진 계보 | F1의 발견 증가와 완결 증가를 별도로 보고 |
| 부분 설계 질문자 | 어떤 조건까지 확인했고 무엇이 남는지 | C1/C2/금지 행동·환경·누락 guard | 같은 경로에서 둘 다 확인되면 전체 구현, 한 조건만 확인되면 조건부 보완, 나머지는 재질문·보류 |
| 표준 작성자 | 개념 및 연산 경계의 설명 | 관련 관계를 동일 개념으로 바꾸지 않았는지 | 문서의 규범적 정의가 개별 도구 지원 보증으로 쓰이는 것을 차단 |

**중단 조건:** 새 이름을 넣는 데 원문을 읽어도 판·자기 구현의 역할·정의 관계가 불명확하면 빈 필드와 이유를 남긴다. 긍정적 표현이 있다는 이유로 기능 하나를 세 조건 전체의 추천으로 바꾸지 않는다. 최종 반환 카드는 본 과제의 실제 경로 판정 원장에 따라 결정해야 하며 이 네 전거는 후보 완결 수에 더하지 않는다.

## 5. 실제 배당·비용·미확인

- 신규 실제 개념 원저작: **4/4**, LOC 2·Getty 2. AF056의 Engraving/Etching/painting과 다른 레코드다.
- 성공적으로 직접 읽은 고유 저작: **6**. 이 중 새 개념 4, 기존 매뉴얼 재사용 2. 같은 저작 여러 절·다른 표현은 추가 저작 수가 아니다.
- 성공 독해 소스 행: **12**. LOC JSON 2+MARCXML 2, Getty 개념 2, MARC 절 3, Getty 절 3. 실패 6행은 소스 원장에 보존하되 직접 읽은 저작 분모에서 제외한다.
- F1의 62행 취득 비용과 이 전거 조사 비용은 별도다. 이 하위 조사는 F1 공급자 행 편집이나 이용자의 두 행동 경로에 포함되지 않는다.
- 원문 캐시 수신 바이트는 실제 읽은 단어 수가 아니다. Getty HTML 전체를 읽었다고 하지 않으며 위에 기재한 ID·범위·용어·관계 및 지침의 지정 절을 읽었다. 필드와 관계의 재확인은 네 레코드 각각 필요하다.
- URI 안정성·응답 SHA는 과거 동일 판의 보증이 아니다. 역사적인 Getty 수정 이력 전체, 원 표제의 채택 당시 논의, 인쇄 실험, 소프트웨어 실행은 미실시다.

## 6. 결론을 뒤집을 최소 자료

이 조사에서 지지한 결론은 “공식 전거조차 이름·이력·관련 관계의 범위를 보존해야 하며, 관계만으로 소프트웨어의 공동 조건 지원을 증명하지 못한다”이다. 반증에 필요한 최소 자료는 특정 공급자판의 허용 경로 안에서 기능 이름과 C1·C2·환경의 공동 지원을 직접 연결하는 문서/입력·출력이다. 그런 자료가 나오면 그 후보의 반환 등급은 바뀔 수 있다. 네 전거의 현재 관계가 갱신되면 관계 설명도 고정 응답과 새 응답을 대조해 바꾼다. 신규 명칭 자체가 늘었음을 완결 증가의 대리값으로 삼는 것은 여전히 별도 검증이 필요하다.

세부 원장: [sources.jsonl](sources.jsonl). 기계 판독용 요약: [record-observations.json](record-observations.json). 작성·사실 확인은 이 보조 조사자가 수행했고, 루트가 아직 다시 열지 않은 사실을 별도 독립 검토 완료라고 표시하지 않았다.
