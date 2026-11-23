# JSON-LD 공급자 판별 — 예산 밖 진단

**봉인 경계:** 용어표 `1f63f0129207904a91ae9e01bb3e48c86415a644`, 순위·슬롯 `b765a189aa2a1f5982a4994fc0476273abbf7127` 뒤에 아래 자료를 읽었다. LD-1~LD-4의 L/V 반환은 모두 비어 있다. 아래 링크는 목록 밖에서 추가 조사한 판별 근거이며 어느 시행의 2동작 창이나 상위 세 자리에 넣지 않는다. 따라서 이 자료에서 얻은 기능명·판·옵션으로 원목록을 보충하거나 V를 재검색하지 않았다.

## 1. 맞는 기능명도 게시 필드가 없으면 반환되지 않는다

[고정 catalog.csv](../../catalog.csv)의 LD-001 원1번 `json-ld.js`와 LD-005 원5번 `PyLD`는 `function_field`가 비었고 검색 필드는 이름뿐이다. 다음 공급자 고정판에는 실제 frame API가 있다. 이 차이는 **기능을 가진 구현이 생태계에 없다는 주장에 대한 반례**다. 사용자가 정한 두 조건을 같은 판·허용 창에서 완결했다는 양성은 아니다.

| 진단 ID·고정판 | 직접 확인한 기능 | LD-3 두 조건의 판단 | 반환 역할 |
| --- | --- | --- | --- |
| D-LD-JS9 · jsonld 9.0.0, `27a2b812267fef702c0ac5260a7555d35c3af005` | [README L195–245](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/README.md#L195-L245), [frame L414–488](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js#L414-L488): compact/expand/flatten/frame 분리; frame은 확장→매칭→축약 | 값 패턴 비교 및 나머지 속성의 조건부 복사가 소스에 있다. 원 credential의 전체 remote context·@nest·옵션 조합과 C1/C2 동시 통과는 **미확인** | context/frame 교정 검토를 위한 **보완 링크** |
| D-LD-PY33 · PyLD 3.3.0, `3ac1987d9be3648c09b7c7e34865ce82d637e742` | [README Usage](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/README.md#L92-L154), [frame L732–878](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L732-L878) | 같은 소스판에서 값 패턴·explicit·@nest 동작을 읽었다. 아래 로컬 진단의 별도 노드 입력은 C1/C2=true였지만, 원 질문의 JavaScript 구현을 Python으로 교체할 의사 및 원 입력의 동시 충족은 **미확인** | 언어 교체를 별도 판단할 **보완 링크**, 완결 대안으로 반환 보류 |

두 구현은 JavaScript와 Python의 별도 처리 코드를 가지며 PyLD는 [소스 머리말 L1–5](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L1-L5)에 JavaScript 구현에서 이식했다고 명시한다. 공급자 계열과 W3C 알고리즘/시험 계보는 공통이다. 두 문서에서 같은 W3C 시험을 언급한다고 독립 실행 두 번으로 세지 않는다.

## 2. @nest와 값 선택은 다른 조건이다

[JS 확장 L1016–1038](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/expand.js#L1016-L1038)은 @nest 아래 각 객체를 기존 `expandedParent`에 처리한다. [PyLD L2761–2799](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L2761-L2799)도 같은 부모 노드로 합친다. 이는 공식 [API suite n007 기대 결과](https://github.com/w3c/json-ld-api/blob/ffdb326121ea89b7b8280e76a5caea923834bcef/tests/expand/n007-out.jsonld)와 맞는 **소스 판독**이다.

LD-3의 원문은 두 객체의 a/b/c 조합을 유지하면서 첫 객체만 원한다. 그 객체들을 @nest로 한 노드의 a/b/c 값 집합으로 합친 뒤에는 a=1과 어떤 b/c가 같은 원 객체였는지 정보가 사라질 수 있다. 따라서 framing 지원이라는 사실을 원문의 두 조건 충족으로 즉시 옮기면 잘못이다. 정확한 원 credential 전체를 실행하지 않았으므로 실제 원 입력의 오류/출력 값은 미확인으로 둔다. context 수정을 허용한 원 질문에 대해 별도 노드 경계를 가진 모델을 검토할 수 있지만, **원 credential 전체의 context 수정 실행은 미실시**다. 별도 연구자 최소 fixture의 실제 실행은 §6에 구별했다.

[JS frame L222–264](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/frame.js#L222-L264) 및 [PyLD L4518–4571](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L4518-L4571)은 `explicit=true`면 frame에 없는 속성을 생략한다. 값 조건의 참/거짓과 남길 필드의 범위는 분리해서 보아야 한다. 원문에서 요구하지 않은 자동 보정이나 최신 버전을 필수조건으로 추가하지 않는다.

## 3. 같은 판에서도 설명과 코드가 다르다

jsonld.js 9.0.0의 [JSDoc L403–406](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js#L403-L406)은 embed 기본값을 @last, requireAll을 true로 쓰지만, [실제 기본값 L420–425](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/lib/jsonld.js#L420-L425)은 @once와 false다. 이 불일치는 직접 관측했다. 실행 결과를 관측한 것은 아니다.

PyLD 3.3.0은 [options.py L108–140](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/options.py#L108-L140)와 [실제 frame 기본값 L763–779](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/lib/pyld/jsonld.py#L763-L779)이 일치한다. 필수조건을 확인하려면 명시적인 processingMode/requireAll/explicit와 실제 판을 함께 보존해야 한다.

jsonld 9.0.0의 [릴리스 기록](https://github.com/digitalbazaar/jsonld.js/blob/27a2b812267fef702c0ac5260a7555d35c3af005/CHANGELOG.md#L3-L46)은 2025-11-20, [PyLD 3.3.0 release](https://github.com/digitalbazaar/pyld/releases/tag/v3.3.0)는 2026-09-02다. 둘 다 2021년 원 질문의 당시 설치판을 복원한 것이 아니다. 현재 재탐색 진단에 한정한다.

## 4. 이름이 다른 같은 엔진의 반례

catalog LD-014 원14번의 `jsonld-cli`를 추가 진단했다. 고정 `ab35bc8b00dedcd119904f56a8904721188094b1`의 [package.json](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/package.json)은 개발판 2.0.1-0이며 `jsonld ^8.3.2` 의존성을 가진다. [bin/jsonld.js L14](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/bin/jsonld.js#L14)에서 jsonld를 가져오고 [L363–383](https://github.com/digitalbazaar/jsonld-cli/blob/ab35bc8b00dedcd119904f56a8904721188094b1/bin/jsonld.js#L363-L383)에서 frame 명령을 그 API로 위임한다.

따라서 CLI 제품 인터페이스와 processor 엔진은 구별해야 한다. 이 CLI를 별도 framing 엔진으로 세지 않는다. 의존성 범위만 확인했으므로 실제 설치된 정확한 jsonld 판은 미확인이다. 위의 jsonld 9.0.0과 같은 판이라고 합치지 않는다.

## 5. 시험 계보와 실행 경계

PyLD 3.3.0 tree는 API suite `ffdb326121ea89b7b8280e76a5caea923834bcef`, Framing suite `3bf782ba9a40dd1b143435abe386d38df64f2b47`를 submodule로 고정한다. 앞서 읽은 현재 API suite `fd4f7eb41f679fb73a54923143c473c3a1d06093`와 n007 입력/기대 출력, en01 입력은 blob이 동일했다. 이 비교는 **시험 입력판의 계보 확인**이고 PyLD에서의 통과를 보여 주지 않는다.

PyLD 자체 [@nest scoped-context 회귀시험 L388–413](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/tests/test_jsonld.py#L388-L413) 및 [frame 내부 alias 시험 L575–631](https://github.com/digitalbazaar/pyld/blob/3ac1987d9be3648c09b7c7e34865ce82d637e742/tests/test_jsonld.py#L575-L631)에는 기대 결과/보존 assert가 있다. 이 코드를 읽은 것과 실제 assertion이 통과한 것을 구별한다. 두 라이브러리의 runner는 W3C 공통 fixture를 재사용하며 skip/pending 처리도 있다. 별도 EARL 실행 보고는 확보하지 않았다.

`minimal-fixtures.json`은 연구자가 만든 로컬 문맥의 **사전 진단 입력과 예측**이다. 원 사용자 전체 입력이나 공식 W3C fixture를 대신하지 않는다. 공급자/W3C runner와 위 자체 회귀시험은 **미실시**다. 아래 연구자 로컬 진단은 직접 실행했으며 별도로 기록한다.

## 6. 로컬 실행: 양성 1건과 예측을 깨뜨린 근접 음성

`sources.jsonl`에서 01:47 UTC 문서 열람 행의 “구현 실행 미실시”는 그 행을 확인한 시점의 상태다. 아래 01:55 UTC 추가 로컬 실행은 별도 실행 행과 receipt에 기록했다. jsonld.js 실행·원 credential 실행·공식 suite/자체 회귀시험 실행은 여전히 미실시다.

2026-11-23 01:55 UTC, 고정 PyLD commit의 깨끗한 checkout을 Python 3.12.14에서 실행했다. 기존 lxml 6.1.1을 사용하고, 없던 cachetools 8.0.2와 frozendict 2.5.1은 작업 소유 `transient/deps`에만 설치했다. 정확한 wheel URL·SHA256과 환경은 [dependency-lock.json](execution-attempts/dependency-lock.json), 최초 누락 오류와 설치 명령은 [before-deps.json](execution-attempts/before-deps.json)·[pip-attempt.json](execution-attempts/pip-attempt.json)에 있다. 전역 설치는 하지 않았고 실제 입력/프레임 실행의 외부 document 요청은 0회였다.

| 진단 | 실제 관측 | 예측과의 관계·한계 |
| --- | --- | --- |
| PLAN-LD-POS: `values`를 별도 노드 집합으로 모델링 | 한 객체 `{a:1,b:2,c:3}`와 `issuer-A`를 함께 반환; 이 작은 입력의 C1=true, C2=true | 사전 예측과 일치. 원 LD-3의 remote context·credential 전체가 아니므로 원 요구 완결이나 L/V 반환 성공으로 세지 않는다. |
| PLAN-LD-NEST: 같은 입력과 프레임의 `values`를 `@nest`로 변경 | frame 확장 단계에서 `jsonld.FrameError`; 반환 출력 없음 | C1=false/C2=false의 단순 출력 실패를 예상했으나 실제는 예외였다. 따라서 [최초 runner](execution-attempts/offline-frame-attempt.json)의 **exit 1과 사전 예측 불일치를 유지**한다. 오류를 C1/C2=false 출력이라고 바꾸지 않는다. |
| DIAG-LD-NEST-CAUSE: 동일 음성 입력의 별도 원인 진단 | expand는 한 노드에 a=[1,4], b=[2,5], c=[3,6]을 모았다. 같은 frame의 내부 예외는 `colliding keywords`, keyword=`@requireAll`이다. | root와 @nest 안의 @requireAll이 같은 노드로 모이는 이 프레임 표현의 충돌이다. 모든 @nest 프레임이 불법이라는 주장이 아니다. 새 진단의 exit 0은 원인 기록 완료이며 최초 runner의 통과로 합치지 않는다. |

양성/음성의 두 frame 호출은 [offline-frame.stdout.json](execution-attempts/offline-frame.stdout.json)에, 추가 expand와 동일 음성 frame 재호출은 [nest-cause.stdout.json](execution-attempts/nest-cause.stdout.json)에 있다. 고유 연구자 입력은 2개, 최초 frame 호출 2회, 원인 확인용 expand 1회·frame 재호출 1회다. 후속 진단 때문에 원 입력·예측을 수정하지 않았다. 프레임 표현 충돌은 최초의 이론적 음성 예상이 놓친 반증이며, 실제 expand 출력은 이 입력에서 @nest가 객체 경계를 보존하지 않았음을 별도로 보여 준다.

## 7. 반환 및 다음 최소 확인

LD-1/LD-2에 이 frame API를 DOM 삽입/AEM 작성 반복의 완결 링크로 반환하지 않는다. LD-4에 Python 프레임 처리를 PHP 행 출력의 동의 기능으로 반환하지 않는다. LD-3에는 원문 조건, @nest 경계, 명시 옵션과 함께 위 고정 frame 소스를 보완 링크로 제공할 수 있다.

결론을 바꿀 최소 자료는 (a) 원 credential의 실제 remote context 판과 당시 jsonld package/lock, (b) context 수정 후 같은 구현판·같은 옵션에서 a=1 선택과 나머지 필드 보존을 함께 확인한 출력/시험 기록, (c) 별도 차수에서 기능 필드가 표시되는 목록의 사전 고정판이다. (c)는 이번 표의 사후 보정이 아니라 새로운 비교다.
