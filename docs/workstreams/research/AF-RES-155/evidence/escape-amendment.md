# ④ 보정 대조 봉인

③ 결과를 본 뒤 추가한 구성 실험이다. ②의 A/B/C와 사전 예측 및 ③ 기본값의 결과를 그대로 둔다. #15872의 현재 본문은 대입 뒤 원시 백틱이 등장한다고 보고했다. 기본 Mustache.js 4.2.0은 이를 `&#x60;`으로 바꾸었다. [Mustache.js 구현](https://github.com/janl/mustache.js/blob/bd29972ab8a0f4c592f35483615ab9a274396300/mustache.js#L657-L689)이 렌더별 escape 설정을 허용한다. 다른 라이브러리를 가정하지 않고 같은 템플릿·대입값·파서로 `config.escape = String`만 바꾼다. 알려지지 않은 저자의 구현이나 설정을 귀속하지 않는다.

새 출력 개봉 전 예상이다.

| 경로 | 예상 |
|---|---|
| X05-raw-nested-example | 원본 확장 결과는 네 백틱 안 세 백틱의 코드 한 블록. 포맷 먼저는 빈 코드 블록 두 개와 그 사이 hello 문단. |
| X05-raw-plain-boundary | 양 순서에서 hello 코드와 다음 문단의 문자 및 HTML이 같다. |
| X05-raw-nested-boundary | 원본은 코드와 한 후속 문단. 포맷 먼저는 코드(빈) → hello 문단 → 코드(빈) → 다음 문단. 동일 템플릿, plain 대입과 nested 대입에 사용한 raw 정책도 동일. |
| X05-raw-format-expanded | 확장된 문서를 포맷하면 formatter가 실제 내부 백틱을 보고 네 백틱을 유지한다. 원본과 렌더링이 같다. CRLF와 출력 LF를 바이트 차이로 별도 기록한다. |
