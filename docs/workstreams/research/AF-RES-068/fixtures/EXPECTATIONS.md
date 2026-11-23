# 실행 전 입력·예측

A01 → A02 → L01 → L02 순서와 정상 G1, C1 근접음성 G2, C2 근접음성 G3, 경계·보존 G4를 고정했다. 실험의 기대값은 각 JSON의 `expectation`이다. 문서 예측은 봉인한 표시창에서 도출한다. 관련 API 소개만 있는 동작은 U다. 원 보고가 요구와 다르면 JSON의 `reported_counterexample`과 `basis`를 따로 읽는다.

- A01은 명시 범위의 하한 8.8.2다. G3이 보고서의 호출·스키마·입력 조합이다. G1/G2의 2019 선언은 두 draft를 비교하기 위한 새 입력이다. G4는 draft-07 컴파일 대조다. [원 요청 9–55행](https://github.com/ajv-validator/ajv/issues/1872)
- A02의 exact 8.9.0에서 G1/G3의 함수와 문자열을 재구성한다. JavaScript 함수는 JSON 파일에 저장되는 검증 데이터 대신 `input_kind`에서 로컬로 복원한다. 함수 body, name, typeof, own enumerable field before/after를 보존한다. [원 요청 21–37행](https://github.com/ajv-validator/ajv/issues/1875)
- L01은 비교판 5.2.0이고 원 보고가 명시하지 않은 API는 `toRDF`로 정했다. G1/G3은 저자 두 JSON과 동등한 내용을 유지한다. 별칭의 RDF 조건은 predicate, 객체 타입, 객체 값, quad 수를 검사한다. [원 요청 두 JSON과 두 출력](https://github.com/digitalbazaar/jsonld.js/issues/465)
- L02는 비교판 5.2.0에서 저자의 TS 예제를 JS 호출로 재구성한다. G1의 문서/컨텍스트는 원 예제 값이다. C1 alias 결과와 C2 구조를 분리해, full IRI로 나온 경우에도 배열/스칼라/ID 참조 형식이 살아 있는지 확인한다. [원 요청 예제와 관측](https://github.com/digitalbazaar/jsonld.js/issues/466)

Node v24.22.1/npm 11.9.0 클라우드 환경, 공식 npm tarball, script 실행을 생략한 임시 설치, JSON-LD의 로컬-only documentLoader를 쓴다. 패키지판 일치, fixture 배치 성공, 기능 성립, 요청자 원 환경 일치는 각각 기록한다.
