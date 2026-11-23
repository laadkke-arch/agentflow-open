# JSON-LD 정의와 사전 반례

- [API 1.1 §§2.1–2.4](https://www.w3.org/TR/2020/REC-json-ld11-api-20200716/#features): expansion은 context를 제거해 IRI와 값을 규칙적인 표현으로 만들고, compaction은 주어진 context로 반대 방향의 축약을 한다. flattening은 노드별 속성을 합치며, RDF와 JSON-LD 사이 직렬화도 방향별로 나뉜다. 이 정의는 HTML breadcrumb 도출·script 삽입·AEM 반복 생성을 보장하지 않는다.
- [Framing 1.1 §2.1.1 및 §4.2](https://www.w3.org/TR/2020/REC-json-ld11-framing-20200716/#frame-matching): frame은 노드/값을 매칭하고 결과의 구조를 제시한다. 따라서 원문 JSON-LD frame→framing은 허용할 수 있다. 원 질문의 context가 객체 경계를 보존하는지, 출력에서 나머지 속성이 유지되는지는 구현판·옵션의 별도 증거가 필요하다.
- [Syntax 1.1 §4.4 예제 88–89](https://www.w3.org/TR/2020/REC-json-ld11-20200716/#nested-properties): @nest는 중간 객체의 속성을 바깥 노드에 접는다. 같은 키 밑의 여러 원시 값을 같은 원래 객체의 필드 조합으로 되돌릴 수 있다고 가정하면 안 된다. §4.3의 일반 배열은 자동 순서 보존도 뜻하지 않는다.

## 결과 전에 고정한 반증 질문

1. 올바른 표준 연산 이름이 게시 필드에 아예 없으면, 이 매핑은 새 구현을 반환하지 못하는가?
2. LD-3의 구현이 framing을 지원하더라도 원문의 @nest가 각 객체의 구별을 소거한다면, a=1뿐 아니라 그 객체의 b,c 보존도 함께 증명되는가?
3. LD-1/LD-2에서 JSON-LD 변환기가 단지 유효한 JSON-LD를 만든다는 사실을 DOM/AEM 실행 조건의 증거로 오인하는가?
4. LD-4의 선택과 가격 추출은 일반 PHP 배열 조작일 수 있다. 이름이 비슷한 graph 처리기가 요청자의 출력까지 해결한다는 증거가 있는가?

공식 예제는 추후 구현 실행을 대신하지 않는다. API §2.1 예제 3과 §2.2 예제 6–8은 같은 정보의 서로 다른 방향을 제시하며, compaction과 expansion을 뒤집어 같은 출력이라고 판단하는 번역을 배제한다. 확정된 구현의 양성/근접 음성 회귀시험 한 쌍은 아직 미열람이므로 Q6의 구현 검증 완료로 세지 않는다.
