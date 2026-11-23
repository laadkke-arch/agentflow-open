# 공식 정의·목록 재열람

## STD-SC-CORE07

validation은 제약검사 행위이고 meta-schema는 schema를 기술하는 schema다. assertion과 annotation의 역할을 구분한다. validation→Validator 파생형 및 실제 구현의 동적 C1/C2 지원은 이 정의가 증명하지 않는다.

출처: https://json-schema.org/draft-07/draft-handrews-json-schema-01 · §3.1; §4.3.1–2

## STD-SC-VALID07

enum은 정해진 배열 원소와 값의 동등성을 검사한다. contains는 어느 위치의 한 원소 이상이다. default는 schema에 연관된 기본값 annotation이다. 다른 instance에서 동적으로 값 가져오기, 마지막 자리 전용 제약, 실제 값 삽입을 표준명과 동의 처리할 수 없다.

출처: https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01 · §6.1.1–3; §6.4.1/6.4.6; §10.2

## STD-LD-API11

expansion은 context를 제거해 IRI/값 표현을 일정하게 하고 compaction은 주어진 context로 표현한다. flattening은 같은 node의 속성을 하나에 모은다. DOM 생성·AEM 반복·PHP 출력·값필터링과 같지 않다. 공식 예제는 특정 공급자판의 실행 성공이 아니다.

출처: https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/ · §2.1–2.3 공식 입출력, §5.1 개요

## STD-LD-FRAME11

framing은 frame으로 node를 매칭하고 출력 형태를 정한다. requireAll과 explicit 포함 옵션의 차이는 동일 framing 이름 아래에서도 조건과 남기는 필드를 바꾼다. 원 credential 및 @nest 객체경계의 공동 충족을 이 원리만으로 판정하지 않는다. 처리모드1.0/1.1과 옵션을 유지해야 한다.

출처: https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/ · §2.1/2.1.1/2.1.4; §2.3.2/2.3.5

## CAT-SCHEMA-CONTRACT

기능분류·언어·위임엔진·준수설정은 별개 필드다. 필수값은 name/toolingTypes이다. 데이터 계약은 실제 화면노출과 구현의 개별조건 충족을 보증하지 않는다. F0 재구성은 하지 않았다.

출처: https://github.com/json-schema-org/website/blob/1a415f9d36c34fe0eae271c05f86a459746ed00b/data/tooling-data.schema.json · properties/toolingTypes,languages,dependsOnValidators,compliance; required

## CAT-LD-INDEX

고정 공식 목록은 이름/저장소/언어/JSON-LD판/일부상태·CLI분류를 가진다. 독립 공급자기능명 필드는 없다. 22행을 인수한 원순서로 사용하며 현재페이지·과거태그 순서를 재조사하지 않았다.

출처: https://github.com/json-ld/json-ld.org/blob/f9e9288d7c41db5643386effff1ff2a3fe820237/index.yaml · implementations 전체22행의 키 구조

## IN056-REQUIREMENTS

기존8요구·62행·16비교·유일 후보SC032 미확인을 고정 인수. 원규칙으로16비교 재생 일치. 기존80질문/62행 순서/예산밖 SC032·PyLD 실행은 새로 조사하지 않음. 내부 자료이며 외부저작 최소수에서 제외.

출처: https://github.com/laadkke-arch/agentflow-open/blob/4b7ae5ce472f3a194acaadc950190bb005289441/docs/workstreams/research/AF-RES-056/HANDOFF.md · HANDOFF,RESULT,requirements,catalog,vocabulary,matches,windows,judgments,SCOPE plus schema/LD detailed requirement files

HTTP 전체응답은 해시/취득영수증을 보존하며 원문 전문을 별도 저작으로 더하지 않는다. 본문 정의와 예시를 직접 읽었으며 공급자 실행은 하지 않았다.
