# 같은 두 행동 창의 판정과 예산 밖 진단

판정 담당은 root다. 원격 순위 `b765a189aa2a1f5982a4994fc0476273abbf7127` 뒤에만 공급자 문서를 읽었다. 같은 후보의 대표 하나/대표→첫 정보 링크/대표→둘째 정보 링크를 각각 독립 시행으로 만들었다. 실제 이용자의 클릭이나 채택을 관측한 실험은 아니다.

## 본표의 한 후보와 세 시행

[고정 README](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md)의 첫 본문 제목은 L3이고500번째 whitespace 단어는 L99에서 끝난다. 이는 최초 raw Markdown500단어 창(v1)이다. 팀내 감사 뒤 원래 지정한 렌더링 텍스트500단어로 기계 추출을 정정한 v2는 L106의 첫 단어까지다(v1은 실제 표시487단어). 같은 응답의 앞선 설명과 추가 빌드 안내는 판정을 바꾸지 않는다. 이 창은 C++·draft7·version2와 일반 검증/빌드 안내를 보여 준다. `pii`의 동적 열 이름 제한(C1)이나 `column_datatype`의 세 값 enum(C2)은 보이지 않는다. 보이지 않는 것과 전체 구현에서 불가능한 것은 구별한다.

| 시행 ID | 동작1 | 동작2 | 판정 |
| --- | --- | --- | --- |
| JS-4-V-P1 | SC-032 README 렌더500단어 v2 | 없음 | C1/C2 미확인; 완결·부분 관측0 |
| JS-4-V-P2 | 같은 README 응답 | 첫 정보 링크 `http://json-schema.org/` → [현재 소개](https://json-schema.org/), 렌더500단어 v2(L6–105; v1표시479단어) | 일반 소개/커뮤니티 정보이며 구현판 증거 없음; 미확인 |
| JS-4-V-P3 | 같은 README 응답 | 둘째 정보 링크 `http://json-schema.org/schema` → [2020-12 meta-schema](https://json-schema.org/draft/2020-12/schema) | 제목 없는 JSON으로 사전 경계 미정; 두 조건 미확인 |

세 번째 링크인 nlohmann/json은 첫 두 정보 링크에 속하지 않아 본표에서 열지 않았다. JSON 응답은 웹 도구의 MIME 실패 후 같은 URL의 일반 HTTP GET으로 복구했고168단어다. 이를 제목 없는 문서의 첫500단어로 사후 허용해도 특정 구현의 C1/C2 근거가 아니므로 결론은 같다. 그 감도를 본표 규칙으로 소급하지 않는다.

이 과정에서 대표 구현은1개, URL 도착은3개, 경계 확정 고유 창은2개(구현 README1+일반소개1), 경계 미확인 JSON1개다. 독립 시행은3개이고 논리적 행동 행은1+2+2=5다. 한 시행에서5번 읽었다는 뜻이 아니다. 나머지47슬롯은 빈 반환45/매치풀 소진2로 분리했다. [windows.csv](../../windows.csv)의52행과 [judgments.csv](../../judgments.csv)의 본표18행(빈 비교15+시행3)이 이 단위를 보존한다.

본표에서 두 조건 또는 한 조건을 입증한 기여 문서는0이다. 후보 관련 설명 문서1을 기능 입증 문서1로 올리지 않는다. C++와 원문의 Python3 환경 차이는 확인되지만 대체 언어 허용 여부가 명시되지 않았으므로 이를 곧바로 어휘 `validation`의 의미 오류라고 하지 않는다.

## 추가로 확인한 구현판과 반례

이후 [CMakeLists.txt](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/CMakeLists.txt#L14)에서 build판2.4.1을 확인했다. [enum 코드](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/src/json-validator.cpp#L551-L560)는 schema의 고정값과 instance를 비교한다. 첫500단어 밖에서 얻은 이 근거는 본표의 부분 점수로 넣지 않았다.

같은 고정 소스와 nlohmann/json v3.12.0@`55f93686c01528224f448c19128836e7df245f72`를 g++14.2.0으로 직접 빌드했다. CMake와 시스템 nlohmann header가 없어 명시적인 include 경로와 소스파일 목록으로 컴파일했다. [실행기](run_sc032_diagnostic.py), [연구자 fixture](schema_fixture.cpp), [실제 출력·환경·시각·exit](sc032-execution.json)을 보존했다. 최초 실행 후 실행기에 dependency SHA 일치 assertion만 추가했으며 fixture·빌드 명령·관측 출력은 바꾸지 않았다.

| 연구자 입력 | 고정 C2-only schema의 실제 결과 | 두 분석조건의 기대(전체 guard 제외) | 해석 |
| --- | --- | --- | --- |
| `field1.column_datatype=string`, `pii=[field1]` | 수락 | 수락 | 작은 양성 입력 |
| 같은 입력에서 datatype=`array` | 거절 | 거절 | C2 근접 음성 구별 |
| datatype=`string`, `pii=[missing_column]` | 수락 | 거절 | enum 지원만으로 C1을 해결했다는 주장 반증 |

build/run 모두 exit0은 위 사전 예상 결과와 일치했다는 뜻이다. 원문 Python 프로그램 전체, 값 존재 guard, C1 구현, 전체 적합성 suite를 통과한 것이 아니다. 임의 사전처리/확장으로 C1을 구현할 가능성도 배제하지 않는다.

[README 후반의 성적 설명](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/README.md#L271-L280)과 같은 판의 [known-failures](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/test/JSON-Schema-Test-Suite/known-failures.json)를 함께 읽었다. 후자는 `$ref`/정수 처리 등 예상 실패를 열거한다. [공급자 시험 운영 README](https://github.com/pboettch/json-schema-validator/blob/d5199551f758ba067612979ae32ec35693640ccf/test/JSON-Schema-Test-Suite/README.md)는 vendored suite와 예상실패 처리의 계보를 밝힌다. 포괄적 성적 문구·기대값·실제 실행 로그는 별개다.

## 정확한 재개 명령과 입력

아래 경로가 없는 새 checkout에서 실행한다. 모두 과제 소유 경로 안에 생성하며 전역 설치가 필요 없다. 두 clone의 SHA가 다르면 실행기가 멈춘다.

```bash
git clone --no-checkout https://github.com/pboettch/json-schema-validator.git docs/workstreams/research/AF-RES-056/evidence/transient/sc032-build
git -C docs/workstreams/research/AF-RES-056/evidence/transient/sc032-build checkout --detach d5199551f758ba067612979ae32ec35693640ccf
git clone --depth 1 --branch v3.12.0 https://github.com/nlohmann/json.git docs/workstreams/research/AF-RES-056/evidence/transient/nlohmann-json
python -B docs/workstreams/research/AF-RES-056/evidence/windows/run_sc032_diagnostic.py
```

같은 원문 요구의 완결 여부를 바꾸려면 원래 Python 환경/제품판과 동적 columns 조건의 구현, 값 존재의 정확한 의미, 동일 입력의 양성·근접 음성을 추가 확보해야 한다. 이것은 현재 README500단어를 사후 확장하는 작업과 구별한다.

## 감사 뒤 해석 정정

원래 fixture와 stdout의 `desired_full_contract_accept`라는 키 이름은 범위를 과하게 표현한다. 해당 bool은 연구자가 정한 C1/C2 두 분석조건의 oracle이며, 원문의 title/description 등 모든 기존 요구와 값 존재 guard를 포함하는 전체 계약이 아니다. 원래 입력·예측·출력은 소급 수정하지 않았고 이 해석을 `fixture-scope-correction.json`에 고정했다.

README와 홈페이지의 v1은 raw Markdown500을 세어 표시단어487/479만 포함했다. 고정 응답 그대로 pandoc3.1.11.1 GFM→HTML text node로 재계산한 v2는 각500이며 README L106/홈페이지 web L105까지다. 첫2링크·상위3·조건판정은 동일하다. root는 원래 지정한 렌더본문 규칙을 구현하는 추출결함 정정으로 v2를 최종 창 원장에 사용하며, 감사자의 처음 보수적 감도-only 권고와 사후전체본문노출 사실은 `evidence/review/window-audit.md`와 SCOPE에 보존한다. v1영수증은 그대로 남긴다. 각 hash의 terminalLF 포함/제외는 review v2JSON에 명시했다.
