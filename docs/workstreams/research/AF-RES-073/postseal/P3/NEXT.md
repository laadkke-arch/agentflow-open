# P3 재개에 필요한 정확한 입력과 명령

**상태: 실행하지 않음.** 이번 조사에서는 고정된 옛 소비자 실행환경·의존성 lock과 실제 제품의 독자 설정을 확보하지 못했다. 아래 파일은 코드 판독을 실행 결과로 오인하지 않기 위한 재개 입력이다.

## 1. C1 최소 분리 입력

`fixtures.json`의 네 객체를 그대로 사용한다. 첫 객체는 추가 필드가 없는 대조, 둘째는 같은 4.5에 $schema만 추가, 셋째는 4.6 정규 URI, 넷째는 4.6의 ../ 비정규 URI다. URI는 원문 경계에서 구성한 문자열이며 실제 발행·해석·불변성을 검증한 URL이 아니다.

필요한 환경: nbformat `5.7.3`, 소스 commit `bbd0f83b67a126cd04c48a03ad053c52e6597d96`, Python 버전, jsonschema·fastjsonschema 등 모든 의존성 버전 및 validator 선택. 당시의 정확한 lock이 없으면 **기록한 현대 재구성 환경**이라고 표기한다. nbformat 버전만 같다고 2023년의 모든 환경을 재현한 것으로 쓰지 않는다.

저장소 루트에서 해당 환경의 Python을 사용한다.

```sh
NBFORMAT_VALIDATOR=jsonschema python -B docs/workstreams/research/AF-RES-073/postseal/P3/probe_notebook_compatibility.py > docs/workstreams/research/AF-RES-073/postseal/P3/probe-jsonschema-output.json
NBFORMAT_VALIDATOR=fastjsonschema python -B docs/workstreams/research/AF-RES-073/postseal/P3/probe_notebook_compatibility.py > docs/workstreams/research/AF-RES-073/postseal/P3/probe-fastjsonschema-output.json
```

이 probe는 raw 4.5 schema 검사, nbformat.validate, nbformat.reads를 구분하고 실행환경·schema 해시·실제 반환/오류를 출력한다. 예상 성공을 하드코딩하지 않았다. 외부 URI는 해석하지 않는다. 원 source의 예측과 출력이 다르면 예측을 수정한다. 사용자가 의미한 실제 옛 독자(예: 어떤 이름·버전의 노트북 앱)에서 같은 4개 입력을 여는 검사는 별도로 필요하다.

원래 시험의 재실행은 위 SHA의 **nbformat checkout 루트**에서 다음과 같다. 이를 수행할 경우 새 checkout과 출력도 AF-RES-073 소유 경로 아래에 둔다.

```sh
python -B -m pytest tests/test_api.py::TestAPI::test_capture_validation_error tests/test_validator.py::test_future
```

이 두 시험의 성공만으로 JEP97 $schema 입력이나 목표 앱의 성공을 입증하지 않는다. 시험 소스는 기존 일반 사례를 다룬다.

## 2. C2 최소 입력

정규 schema URI, major/minor, 발행된 내용의 해시, 고정된 resolver·검증기 구성, 허용 alias 정책을 한 묶음으로 받아야 한다. 같은 URI에 다른 내용을 제공하거나 두 URI가 같은 버전에 대응할 때 실제로 거절하는지 관측해야 한다. 한 번의 HTTP 응답이나 표준 문구만으로 영구 불변성을 입증할 수 없다. v5.7.3 probe는 C2를 측정하지 않는다.

## 3. 접근 실패 gist와 실제 적용 계보

인증된 GitHub 읽기 환경에서 다음 공개 gist API receipt를 확보한다.

```sh
gh api gists/a6e1ae13125f01ff04edf121e30a462a > docs/workstreams/research/AF-RES-073/postseal/P3/gist-receipt.json
```

필요한 필드: created_at, updated_at, history의 version·committed_at, 각 file의 filename·raw_url·truncated·content. truncated이면 해당 raw_url의 원문을 별도 연산으로 읽는다. 현재 gist만으로 최초 제안 당시 내용이 같다고 가정하지 않는다.

실제 JEP97 채택을 주장하려면 구현 PR/commit, 같은 구성의 검증 시험과 결과, 포함된 release/tag의 고정 주소가 필요하다. 이번에 확인한 PR97 수락·merge와 PR343의 별도 선행 수정 사건을 그 구현으로 대신하지 않는다.

## 4. 최초판 시간 경계

`0f4510266ead738e62f1d9e412d6bb9e7eb7a97d`는 PR97 commits 목록에서 확인한 최초 생존 added-file이다. 문서에 적힌 2023-03-01 원고 또는 그보다 앞선 원문 blob/서버 이력이 최소 입력이다. 이를 확보하면 immutable·one-to-one·const가 언제 추가됐는지 대조한다. 원 검색 입력과 점수는 덮어쓰지 않고 새 민감도 분석으로 기록한다.

