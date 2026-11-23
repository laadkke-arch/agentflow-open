# SC-032: 기존 판정 인수와 새 JS-6의 경로

기존 JS-4는 AF-RES-056의 세 경로와 미확인 판정을 그대로 인수했다. 첫 README와 소개의 500단어 v2 경계, 제목 없는 JSON의 당시 경계 미확인을 유지한다. 기존 C++/PyLD 실행은 재수행하지 않았다. 인수 영수증은 `inputs/af-res-056/user-windows/`, 원래 판정은 `inputs/af-res-056/judgments.csv`에 있다.

새 JS-6에서는 단계3 원격 봉인 후 같은 `d5199551f758ba067612979ae32ec35693640ccf` README 응답의 첫500단어를 직접 읽었다. C++·draft7·오류처리·thread-safety·숫자 범위 한계는 보이지만 데이터 속성 이름 `type`과 `id:string`을 공동 지원하는 직접 근거는 없다. 원문의 Ajv 웹앱을 이 C++ 라이브러리로 바꿀 수 있다는 전제도 주어지지 않았다. 언어 차이만으로 라이브러리의 조건 구현 불가능을 단정하지 않는다.

| 새 경로 | 실제 도착 | 같은 경로 판정 |
|---|---|---|
| P1 | [고정 README](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md), 첫 제목부터500 표시단어 | C1·C2 미확인 |
| P2 | 같은 README → 원링크 `http://json-schema.org/` → [일반 소개](https://json-schema.org/), 첫 제목부터500단어 | 둘째 문서는 특정 구현의 지원 증거가 아니므로 C1·C2 미확인 |
| P3 | 같은 README → `http://json-schema.org/schema` → [2020-12 meta-schema](https://json-schema.org/draft/2020-12/schema), 제목 없는 JSON168단어 | README의 링크 설명은 draft7지만 목적지는2020-12이며 구현이 아니다. C1·C2 미확인 |

세 새 창은 `windows/README.txt`, `HOME.txt`, `META.txt`에 있다. README는 단계2 캐시를 재사용했고 두 외부 목적지는 HTTP→HTTPS 이동을 포함해 각각 한 요청으로 성공했다. 새 물리 취득2, 재사용1, 고유 창3/1,168단어다. 독립 P1/P2/P3의 논리적 비용은5행동/2,168단어다. 기존 세 경로의 논리적 비용5행동은 별도이며, 당시 JSON 창의 미확인 경계를 새168단어 창으로 소급 덮어쓰지 않았다.

정의나 소개 페이지를 따라갔다고 구현 지원이 확인되는 것은 아니다. 이 사례는 안정된 링크 표기와 실제 도착 판도 다를 수 있음을 보여 준다. 원문의 `{"type":"article","id":1}` 근접음성이 실제 후보에서 어떻게 처리되는지는 미실시다. 그 입력의 실패나 성공을 이 문서 관측에서 발명하지 않는다.

HTML의 표시단어는 사전 정의한 text-node/블록 경계 추출 결과다. 브라우저 CSS 배치의 물리적 줄바꿈·버튼 간격을 측정한 것은 아니다. 이 차이가 창 끝을 조금 옮길 수 있으므로 정확한 브라우저 시야와 동등하다고 주장하지 않는다. 현재 판정은 둘째 문서의 역할과 구현 근거 부재에 의존하며 행사 목록의 끝부분에서 지원 증거를 찾지 않았다.

세부 경로는 `observations.json`, 취득과 원응답 해시는 `acquisition.json`, 출처와 독해 범위는 `sources.jsonl`, 분모는 `summary.json`에 기록했다. 작성자는 루트이며 외부 독립 실행 검토는 없다.
