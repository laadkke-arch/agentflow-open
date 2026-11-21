# AF-RES-017 coding supplement

## 분류와 코드북의 명칭 차이

사용자 표의 `형태(S1)`에는 016 CODEBOOK §4 S3.form의 app/service/library/framework/standard/document/pattern/research 및 data/mixed/unknown 정의를 그대로 쓴다. 고정 016의 실제 S1은 product/component/principle이므로 `legacy_S1`에 병기한다. 요청의 명칭과 원 파일의 명칭을 혼동하지 않는다. `기여(S2)`는 016 §3 whole/part/reference/comparison/none/mixed/unknown 그대로다. whole은 프로젝트 전체가 아니라 사례의 명시된 선택 범위 전체다. `관계(013 분류)`는 같은 목적 완성품/재사용 부품/같은 분야의 다른 설계/다른 언어·생태계/다른 분야 원리/표준·논문 중 하나, 복합이면 primary와 보조 관계를 구분한다. 타 분야는 이름의 유래가 아니라 원 분야 관계와 대상 설계의 명시적 연결을 요구한다.


Independent coder receives this codebook and unlabelled packets only. Do not read CASES, coder-a, RESULT, prior labels or Git history. Return one row per id: missed_form, legacy_S1, missed_contribution, missed_relation, late_discovery_status, confidence, ambiguity, reason. Missing causal evidence means unknown. No internet lookup during coding. The packet is worker-authored summary with source locations, not raw ground truth.

## Inherited definitions (unaltered)

# AF-RES-016 — 세 분류안 코드북 v1.0

**코딩 전 동결.** 아래 모든 예는 이 연구자가 만든 가상 예다. 실제 표본에서 고르지 않았다. 특정 제품의 실제 기능을 주장하지 않는다. 원판 AF-RES-011 역할을 재코딩하는 코드북이 아니라 새 세 분류안 비교다.

## 1. 공통 규칙과 입력

한 행은 sample/units.json의 `unit_id` 하나다. `candidate`와 `candidate_description`은 대상 정보이고 `problem`, `proposal`, `configuration`, `constraints`는 문제 문맥이다. 출처 링크는 재현 위치이며 이번 코딩에서는 입력 패킷만 읽는다. 새 웹 검색, 다른 파일, 과거 라벨, 다른 코더의 응답을 읽지 않는다. 부족하면 unknown을 쓴다. 잘 아는 이름에 일반 지식이 개입할 수 있으므로 근거가 패킷보다 강한지는 confidence/reason에 밝힌다.

S1과 S3 form은 candidate/candidate_description에 한해 먼저 판단한다. 문제에 도움이 된다는 이유만으로 산출물 형태를 바꾸지 않는다. S2는 전체 패킷을 읽는다. S2의 '전체'는 **질문이 선택한 범위 전체**이며 프로젝트 전체와 다르다. 부품을 찾는 질문에서 라이브러리가 그 부품 요구 전체를 맡으면 whole이다. 역할과 사실 충족은 별개: 제약을 어기는 전체 대체 제안도 역할은 whole이며 부적합 여부는 후속 H 판정이다.

반복된 똑같은 후보 대상은 S1/form을 일관되게 붙인다. 이름만 같아도 상위 제품/특정 모듈/문서/방법이 다르면 다른 대상이다. `source URL이 문서`라는 이유로 설명 대상인 실행 소프트웨어를 document로 바꾸지 않는다. 특정 문서 자체를 참고 후보로 내놓았을 때에만 document다. 하나의 답에서 동급 후보가 여러 개면 개수가 아니라 역할/형태가 서로 다른지 본다. 동일 범주 여러 개는 mixed가 아니다.

## 2. S1 후보 속성형 — 단일 역할

이 안은 맥락 독립 분류를 일부러 운영 가능하게 만든 가설이다. product의 기준은 **독립 배포/실행과 사용자 또는 외부 시스템에 제공하는 완결 기능**이다. 다른 시스템이 사용한다는 이유만으로 서버를 component로 낮추지 않는다. 형태가 둘이면 primary 설명을 따르고, 우세가 없으면 mixed.

| 값 | 정의·포함 | 제외·경계 규칙 | 표본 밖 가상 경계 예 3개 |
|---|---|---|---|
| product | 독립 실행 앱·CLI·서버·호스팅 서비스, 자체 인터페이스로 완결 작업 제공 | 프로세스 안에 링크/삽입하는 라이브러리·플러그인은 component. 설치 크기와 무료 여부는 무관 | A: CLI 변환기가 한 파일을 변환하면 product; B: 별도 프로세스 수치 저장 서버도 product; C: 웹 편집기+SDK 묶음에서 웹 사용이 주 설명이면 product |
| component | 호스트나 개발 결과물 안에 결합되는 라이브러리·프레임워크·플러그인·재사용 모듈/자료 | 독립 서버를 다른 앱이 호출한다고 component로 바꾸지 않음. 코드 없는 원리는 principle | A: 편집기 플러그인은 component; B: 웹 프레임워크는 앱 골격을 주어도 component; C: 실행 없는 좌표 데이터 파일은 재사용 부품 |
| principle | 구체 실행 대상보다 방법·규칙·패턴·설계 문서·표준·연구 관계를 제안 | 문서 URL로 설명된 실행 앱은 product/component. 단순 경험담에 재사용 조언이 없으면 unknown | A: 충돌 해결 절차 설명은 principle; B: 프로토콜 규격은 principle; C: '먼저 작은 입력으로 시험' 조언도 principle |
| mixed | 하나의 원 단위에 서로 다른 S1 역할이 대등하게 제안돼 primary 하나를 못 정함 | product 여러 개나 component 여러 개만으로 mixed 금지 | A: 완성 앱+직접 구현 원리를 대안으로 함께 권함; B: 플러그인과 별도 서버를 대등하게 제시; C: 도구 목록과 운용 패턴을 독립 대안으로 제시 |
| unknown | 패킷에 무엇을 후보로 제시했는지/독립 산출물인지 판단할 정보가 없음 | 형식이 복수인 것은 mixed, 단순히 부적합한 후보는 unknown 아님 | A: '그것을 써라'만 있음; B: 후보 없는 감사; C: 실체 설명 없는 약어만 제시 |

## 3. S2 문제 상대형 — 선택 범위에 대한 기여

우선 명시된 제안 사용 방식을 따르고, 없으면 질문과 후보 설명의 직접 연결을 읽는다. 역할은 적합성 등급이 아니다. '모든 제약을 이미 검증'해야 whole인 것이 아니다. 실제 연결이 없는데 모든 문서를 reference로 구제하지 않는다. comparison은 실제 비교 기준으로 제시된 경우만이다.

| 값 | 정의·포함 | 제외·경계 규칙 | 표본 밖 가상 경계 예 3개 |
|---|---|---|---|
| whole | 질문이 고르려는 범위 전체를 그 후보/제안으로 맡기거나 대체 | 더 큰 프로젝트의 일부여도 질문 범위 전체면 whole. 요구 실패는 H에서 판단 | A: '압축 라이브러리 하나' 질문에 압축 라이브러리; B: 완성 출석 앱을 원하는 질문에 출석 서비스; C: 저장층을 고르는 질문에 저장 서버 |
| part | 선택 범위의 명시된 일부 기능/층만 맡고 나머지에 별도 구현·후보 필요 | 설치·통상 설정만 필요하다고 part는 아님. 선택 범위를 임의로 전체 앱으로 확대하지 않음 | A: 회계 앱 질문에 환율 API만 제공; B: 문서 검색 제품 질문에 토큰화 모듈; C: 결제 전체 질문에 영수증 템플릿 |
| reference | 실행 대체보다 설계 관계·운용 방법·주의점·타 분야 원리를 가져오는 제안 | 단순 주제 관련성은 reference가 아님. 독립 구현을 요구하는 원리라도 좁은 문제의 설계 참고면 reference | A: 식당 대기열 원리를 서버 과부하에 대응; B: 장애 처리 문서의 불변조건을 옮김; C: 경험담에서 백업 주기 선택을 배움 |
| comparison | 후보 선택/검증의 명시적 기준·대조군·비교 대상이며 도입 제안이 아님 | 알려진 제품을 추천했다는 것만으로 comparison 아님. 요구를 어기는 추천도 whole/part일 수 있음 | A: 기존 수기 방식의 처리시간을 기준으로 둠; B: 옛 버전은 회귀 비교 대상으로만 사용; C: 금지된 서비스는 필요한 기능의 비교 기준으로만 설명 |
| none | 문맥에서 채울 기능·옮길 관계·비교 기능이 드러나지 않는 자료 | 근거 부족과 확실한 무관을 혼동하지 않음. 억지 유추를 발명하지 않음 | A: 소리 편집 질문에 건축 자재 목록; B: 데이터 저장 질문에 관계 없는 글꼴; C: 맥락 없는 동음이의 제품 |
| mixed | 하나의 답에 whole/part/reference/comparison 등이 독립·동급 기여로 공존 | whole 도구를 설명하는 보조 사용법만으로 mixed 아님 | A: 완성 앱과 직접 만들 설계안을 동급 대안으로 권함; B: 일부 모듈과 별도 비교 기준을 함께 제안; C: 운영 서비스 대체와 타 분야 원리를 각각 제안 |
| unknown | 어떤 사용 방식/선택 범위인지 없어 none와 유용한 기여를 구별 못함 | 역할은 명확하지만 기능 지원이 미확인인 경우 역할을 unknown으로 바꾸지 않음 | A: '좋은 도구?'만 묻는 질문; B: 후보 이름만 있고 동명의 어느 대상인지 모름; C: 부모 답을 잃은 후속 설명 |

## 4. S3 두 축 — form × contribution

`contribution`에는 S2 값을 그대로 복사한다. 이것은 같은 의미 변수의 일관성을 유지하는 조작이며 S2와 독립된 세 번째 인지 실험이 아니다. form은 아래 단일값이다. form이 실제 다중이면 mixed, 정보 부족이면 unknown. 프레임워크는 생명주기/제어 흐름을 제공하는 확장 골격, library는 호출해 쓰는 기능 묶음으로 경계한다. 잘 모르겠으면 이름만으로 추론하지 않는다.

| form | 정의·포함 | 제외·경계 규칙 | 표본 밖 가상 경계 예 3개 |
|---|---|---|---|
| app | 사용자가 직접 실행하는 UI/CLI 프로그램 | 장기 구동 endpoint는 service; 설치 패키지는 형식 결정 근거가 아님 | A: 배치 변환 CLI; B: 데스크톱 뷰어; C: 혼자 실행하는 점검 도구 |
| service | 장기 프로세스/호스팅 endpoint로 기능 제공 | 임베디드 API는 library; 웹앱도 주 대상이 사용자 UI이면 app 가능, 설명 우선 | A: 원격 음성 변환 endpoint; B: 독립 색인 서버; C: 상주 큐 데몬 |
| library | 프로그램에서 호출/연결하는 기능 모음·호스트 플러그인 | 제어 골격을 주면 framework; 독립 서버는 service | A: 이미지 디코더; B: IDE 확장 모듈; C: 앱에 링크하는 계산 엔진 |
| framework | 앱·확장 구현의 구조/생명주기를 제공하는 골격 | 단순 함수 모음은 library; 완성 실행 서비스는 service | A: 게임 상태 생명주기 골격; B: 웹 라우팅+실행 골격; C: 테스트 실행/발견 골격 |
| standard | 상호운용/행동을 규정하는 명시 규격·프로토콜 | 규격의 구현체는 해당 실행 형태; 설명 글은 document | A: 교환 포맷 규격; B: 메시지 순서 프로토콜; C: 접근성 적합성 명세 |
| document | 안내서·기술 문서·튜토리얼·분류표 자체가 후보 | 문서가 설명하는 실행 대상을 후보로 삼으면 그 형태; 일반 원리 자체는 pattern | A: 설치 안내를 참고자료로 추천; B: 사례집을 읽기 후보로 제시; C: 설계 템플릿 문서 |
| pattern | 반복 적용하는 추상 관계·방법·경험칙·운용 절차 | 그 패턴을 연구한 논문 자체는 research; 구체 배포 코드는 해당 형태 | A: 재시도 전에 식별키 확인; B: 생산량을 소비 신호에 맞춤; C: 저장 전에 형식 확인하는 절차 |
| research | 연구 문제·방법·결과를 보고하는 논문/실험 보고서 자체 | 연구 코드의 실행물을 추천하면 해당 형태; 규격은 standard | A: 분류 일치 실험 논문; B: 알고리즘 비교 연구; C: 사용성 관찰 연구 보고서 |
| data | 호출/실행 코드 없이 재사용하는 데이터셋·목록 자료 | 목록의 작성법은 pattern; 규격 표는 standard; 읽기용 안내는 document | A: 주소 좌표표; B: 시험용 음성 집합; C: 공개 단어 사전 파일 |
| mixed | 대등한 후보들이 서로 다른 form이거나 분리 불가능한 복수 형태 | 같은 형태 후보 여러 개는 mixed 아님 | A: 앱과 라이브러리 동급 추천; B: 논문과 표준 동급 제안; C: 데이터와 실행 도구를 동급 묶음으로 제시 |
| unknown | 형태를 정할 설명이 없음 | 생소하다는 이유만으로 unknown 아님. 데이터가 충분하면 정의 적용 | A: 약어만 제시; B: 후보 없는 반응; C: 실행물인지 글인지 모르는 링크 제목 |

## 5. 출력과 불변성

최초 응답 JSON은 다음 구조를 따른다. reason은 그 행의 실제 입력에서 고른 단서와 경계 이유를 짧게 쓴다. 한꺼번에 자동 추천한 템플릿 이유로 대체하지 않는다. confidence는 high/medium/low, ambiguity는 boundary/context/polysemy/none 중 하나다. ambiguity는 코더의 자체 경고이며 사후 불일치 유형과 구별한다.

```json
{"coder":"a 또는 b","model":"GPT-6 Astra Pro","human":false,"codebook_version":"1.0","input_packet":"sample/units.json","read_other_labels":false,"rows":[{"unit_id":"예시","S1":"product","S2":"whole","S3":{"form":"app","contribution":"whole"},"confidence":"high","ambiguity":"none","reason":"입력에 독립 앱과 해당 선택 범위 전체 대체 제안이 명시됨"}]}
```

A는 과거 연구를 읽고 표본을 준비했으므로 `read_other_labels`에 과거 라벨 노출을 정직하게 별도 표기한다(`read_prior_study_labels=true`, `read_coder_b=false`). B만 과거/A 라벨을 보지 않는다. 패킷에는 role, form, grade, expected, outcome, near-miss, rejected 등의 기존 코딩 필드를 넣지 않는다. 기존 요약문에 남아 있는 선택·범위 해석도 원문 자체가 아니라 선행 연구자의 요약임을 기록한다.

원응답 의미값을 고치지 않는다. 추가 설명·사후 조정은 별도 파일에 둔다. S1/S2와 실제 H/T 판정은 구별하며 SCOPE의 분석 계획에 따라 비교한다.

## 6. 사전 알려진 약점

- 패킷은 선행 연구 요약에 의존한다. 원문을 새로 독립 요약한 연구가 아니다.
- S1은 product/component/principle의 고정 기준을 시험하지만 mixed/unknown을 둔다. mixed가 많은 답에서 '후보 하나'라는 전제가 깨질 수 있다.
- S2 whole/part는 질문의 선택 범위를 명확히 알아야 한다. 범위를 모호하게 남긴 입력에서 낮은 일치를 예상할 수 있으나 결과를 미리 정하지 않는다.
- S3 joint 일치는 더 세분된 범주를 요구한다. S2보다 낮아도 형태축이 쓸모없다는 증거가 아니다.
- SPDX가 맥락에 따른 목적을 이미 허용한다는 공식 명세 관찰은 이 연구의 반례 후보다. 기존 체계 전체를 본질 분류로 묶지 않는다. 상세 원문은 SCHEMES와 sources 원장에 보존한다.
