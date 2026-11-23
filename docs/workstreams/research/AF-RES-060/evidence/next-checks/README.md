# 미실행 후속 확인: 입력·명령·판정 변경 조건

아래는 **계획이며 이번 작업에서 실행하지 않았다.** 28쌍의84경로 주판정을 봉인한 뒤 작성했다. 설치·추가 입력 실행은 한 경로 최대 두 문서라는 주실험과 다른 예산이다. 이번 원격 결과의 완결0을 소급 수정하는 방식으로 쓰면 안 된다. 기존 SC-032/PyLD 예산 밖 시험은 재실행 대상으로 넣지 않는다.

## 재개 첫 행동 — 고정 결과와 결손부터 읽기

HANDOFF에 연결된 고정 결과 SHA에서 RESULT.md 첫 두 표, evidence/acceptance-evidence.json, evidence/paths-ld/preview-exposure.json을 읽고 이번 `partial_handoff`의 원인을 확인한다. 새로운 요청으로 실험의 클릭 경로나 조건을 바꾸려면 별도 사전 계획을 만든다. 고정 입력은5d01a6208edd9f8a20be7b31f7b545cef2200597, F1은412192e28356bee13e4c11f20511ab5ec590662c다.

## 1. JS-6의 가장 작은 추가 구현 진단

필요 입력은 원 요청의 설치 Ajv판·옵션·주변 payload다. 이 정보가 없으면 아래 고정9050ba…에 대한 연구자 진단으로만 보고하며 원 사용자의 성공으로 일반화하지 않는다. `js6-fixtures.json`은 두 양성과 numeric id 근접음성, 원문에 없던 required를 추가하지 않는 guard를 포함한다. schema는 원문의 불완전 조각을 실행 가능한 형태로 **연구자가 구성한 것**이다.

이미 공급자 코드를 검토하고 정상 빌드한 고정 checkout을 `AF060_AJV_DIR`에 지정한 환경에서 사용할 명령:

```bash
AF060_AJV_DIR="$PWD/docs/workstreams/research/AF-RES-060/evidence/next-checks/runtime/ajv"
git -C "$AF060_AJV_DIR" rev-parse HEAD
test "$(git -C "$AF060_AJV_DIR" rev-parse HEAD)" = 9050ba1359fb87cd7c143f3c79513ea7624ea443
node docs/workstreams/research/AF-RES-060/evidence/next-checks/js6-probe.cjs "$AF060_AJV_DIR/dist/ajv.js"
```

현재 위 runtime 디렉터리와 Ajv build는 만들지 않았다. 먼저 같은 SHA의 package.json·lockfile·build 명령을 검토하여 격리된 환경에서 설치/빌드해야 한다. 빌드가 없거나 해당판이 지원하는 Node가 확인되지 않으면 실행 불가를 그대로 기록한다. npm 최신판을 설치해 같은 판이라고 보고하면 안 된다. 결과를 저장할 경우 실제 Node/Ajv 버전·OS·명령·입력 해시·출력·종료코드를 함께 새 진단 영수증에 남긴다.

성공하면 이 고정판의 별도 연구자 fixture 공동 동작 증거가 생긴다. 그래도 원 Ajv판/Drupal 통합과 기존 두 행동 경로의 증거 부족은 남는다. 실패하면 옵션·설계 schema·원환경 차이를 구별하여 조건부 카드만 다시 평가한다.

## 2. 경로 예산 오염 복제

대상은 JS-4::SC-036::P3, JS-6::SC-036::P3 두 개다. 원 첫문서 SHA eeb9aa7f1fe0581ace654a9f3f4bb02192b05bac, 원 둘째 링크 `http://tools.ietf.org/html/draft-zyp-json-schema-04`와 실제 도착 영수증을 보존한다. 기존 초과 preview를 보지 않은 독자가 `evidence/paths-ld/second-windows/SC036-D3.txt`의 등록500단어와 해당 첫창만 보아 별도 판정한다. 원111단어 초과 이력은 지우지 않는다. 새 독자의 환경·표시 단어수·실제 노출·동일 문서 hash를 남긴 뒤 복제 결과를 별도 비교한다.

```bash
python -B docs/workstreams/research/AF-RES-060/evidence/paths-ld/audit_preview_exposure.py
```

위 감사 명령은 저장된 preview의611단어·SHA를 검산하는 것이며 깨끗한 독자 복제 자체를 대신하지 않는다. 기존 JS-4/SC-032 P3의 제목 없는 JSON 경계를 해소하려면056 당시 원 표시 응답·계수 영수증이 필요하다. 현재2020-12 응답을 새로 읽어 옛 경계를 고쳤다고 하지 않는다.

## 3. 원문·판·비용 결손

SC-001/004의 component release provenance, SC-010의200개 밖 릴리스 범위, SC-018/LD-022의 판·접근 결손, 편집 초기 metadata retry의 원영수증이 다음 최소 자료다. 이런 추가 자료를 확보하면 새 취득 사건으로 기록한다. 현재 태그틀 LD5자리 부족은 임의 다른 날짜 질문으로 보충하지 않는다. 버전/비용을 정확히 주장하려면 누락 자료 자체가 필요하다.

다른 후보의 미실행 fixture·입력과 조건은 requirements.json과 evidence/paths-schema/next-checks.md 및 각 observations.json의 next_minimum_check에 있다. 무매치가 구현 부재를 뜻하지 않으므로 새 공급자 탐색을 하려면 별도 목록·질의 실험으로 등록한다.
