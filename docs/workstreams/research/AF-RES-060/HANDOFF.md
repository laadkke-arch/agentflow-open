# AF-RES-060 인계

## 상태와 고정 결과

**조사 상태: `partial_handoff`.** 확보 가능한 전수 편집·새 모집·네 조합 순위·경로 독해·반대 탐색·자체 검토를 수행하고 원격에 고정했다. 완전한 연구 수용으로 보고하지 않는다. 엄격한 창 예산, 일부 판 식별, 정확한 metadata 취득 총수, 공동 조건 직접 근거에 결손이 있다. 저장 성공·계약 검사 통과와 연구 조건 충족은 별개다.

- 저장소: `laadkke-arch/agentflow-open`
- 작업 브랜치: `work/research-af-res-060`
- 소유 경로: `docs/workstreams/research/AF-RES-060/`
- 결과 SHA: **`ccde193ec33f68fea5eaef1cc6f6cea803e1823f`**
- 실제 검사·재열람 영수증 및 갱신 수용 원장 SHA: **`4f4433960b581caad353322da298fa465258979e`**
- 실제 시작 통합 SHA: `3f4d43b19cd76d56983e6f500eebe7010eb3fa51`。계획 시점8036b862…와 구분했다.
- 인수 의존: AF-RES-056 인계 `4b7ae5ce472f3a194acaadc950190bb005289441`, 결과/고정 입력 `2f8ec01e6b52bef4fc3cd003b1690383b6496526`。
- 배정 역할은 `web-pro`; 실제 실행은 이 세션의 cloud executor와 GitHub connector 및 명시된 분담자다. 별도의 사람이 수행한 검토나 별도 UI 사용으로 표현하지 않았다.

### 첫 두 표 위치

1. [RESULT.md §1 — 고정48비교](https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/RESULT.md#1-고정-48비교-같은-경로의-두-조건): 12자리×4조건, 전체 매치·상위3원순번·같은 경로의 구현판/근거·판정·빈 사유.
2. [RESULT.md §2 — 12요구 네 조건 대조](https://github.com/laadkke-arch/agentflow-open/blob/ccde193ec33f68fea5eaef1cc6f6cea803e1823f/docs/workstreams/research/AF-RES-060/RESULT.md#2-12요구의-네-조건-차이와-반환-판단): 필드/질의의 효과·두 축 동시 필요·진입/탈락·비용·반환 링크와 다음 확인.

[수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/4f4433960b581caad353322da298fa465258979e/docs/workstreams/research/AF-RES-060/evidence/acceptance-evidence.json)은38기준의 계획/실제 분자·분모·단위·파일/행·결손·다음 최소 확인을 기록한다. [카드](cards.md), [재현 절차](reproduce.md), [자체 검토](SELF_CHECK.md), [출처 원장](sources.jsonl), [최종 별도 감사](evidence/review/final-audit.md)를 함께 인수한다.

## 핵심 결과

기능 필드는 **발견되는 후보를 늘렸지만 두 문서 이하로 확인한 완결 구현을 늘리지 못했다.** 모든 조합에서 완결0이다. 구현이 실제로 지원하지 않는다는 결론은 아니다.

| 후보가 있는 요구 / 층 분모 | L×F0 | V×F0 | L×F1 | V×F1 |
| --- | --- | --- | --- | --- |
| 기존 튜닝8 | 0/8 | 1/8 | 3/8 | 4/8 |
| 새 모집4 | 0/4 | 1/4 | 0/4 | 2/4 |
| 전체12 | 0/12 | 2/12 | 3/12 | 6/12 |

전체 매치 발생43, 고유 요구×게시행28쌍, 게시행20, 경로84다. 144슬롯 중18이 채워졌고111은 관측 무매치,15는 후보 풀 소진이다. 28쌍은 **완결0 / 조건부 부분1 / 확정오답0 / 미확인27**이다. 채운18슬롯은 부분1·미확인17이다. 전체 요구의 진위가 확인된 후보분모0이므로 정확도·오탐률은 산출할 수 없다. 확정오답0을0%오류로 해석하지 않는다.

부분1은 새 JS-6/Ajv다. 고정9050ba…의 허용 첫창에서 object.properties.bar의 string 제약과 compile(schema)를 직접 읽었고, **bar→id라는 일반 이름 변경만 조건부 전이**로 인정했다. 데이터 속성 type의 처리(C1), 원 Ajv판·Drupal통합, numeric id 거부의 실제 실행은 미확인이다. literal 예제만 인정하면 부분도0이다. 이 때문에 반환 카드는 **전체 구현0 / 조건부 보완1 / 재질문·보류11**이다.

V를 고정하고 F0→F1로 바꾸면 SC-032가 JS-4에서1→11위, JS-6에서1→5위로 밀렸다. F1에서 L→V를 바꾸면 JS-4의 SC-016이3→6위로 밀렸다. 모두 기존 미확인 후보이며 완결 후보 손실이라고 판정하지 않았다. 반대 사례로, JS-6의 검색 풀에 없는 SC-035가 같은 허용창 안에 string property 메커니즘을 갖고 있음을 별도로 기록했다. 이를29번째 주후보로 추가하거나 Kotlin을 원 Ajv 환경과 같은 것으로 처리하지 않았다.

## 실제 확보량과 비용

- 외부 취득·열람 사건193, 실질 직접독해165, 계보로 합친 원저작113, 그중 신규95. 내부 인수·실패·snippet·metadata/front matter만 읽은 자료는 substantive 최소 수에서 제외했다.
- 실제 자료군은 요청본문35, 공급자저작59(목록57+도착 utility2), 표준/시험7, 고정목록/계약2, 실제 LOC/Getty전거4, 기타 지침/홈/benchmark6이다. 최소22와 지정 자료군 배당을 모두 확인했다. 서로 다른 저작 수는 독립 엔진 수가 아니다.
- 현재 태그틀은 Schema20/20·LD15/20. 없는5자리는 그대로 보존했고, first2 적격씩 새4요구는 모두 선정했다. 답·댓글·점수·공급자표를 선정 입력에 넣지 않았다. 당시 태그 모집단 복원을 주장하지 않는다.
- 62행 전체 편집 중54행에154원표기, F0 중복2개를 제외하면152새 문자열을 추가했다. 빈8행을 구현 기능 부재로 해석하지 않았다.
- F1 본문72물리요청,78논리행동,75읽힌 창,30,943논리 표시단어. 고유 저장창은28,943단어다. 정정 추가노출1,411단어와 metadata 최소190요청을 별도 보존했다.
- 사용자 경로는 새130+인수5=135논리행동, 알려진 지정창51,095+인수2,000=53,095단어와 인수 JSON1창 미확인이다. 새 본문29요청·metadata6요청이며 같은 응답 재사용은 네트워크 비용에 중복 청구하지 않았다. 사람의 시간·채택·돈·token은 측정하지 않았다.

## 부분 판정의 원인과 막힌 지점

1. **엄격한 노출 예산:** JS-4/JS-6의 SC-036 P3에서 원 preview611단어를 실제로 읽어500한도를111단어 초과했다. 같은 실제 노출이 두 경로에 영향을 주므로 논리초과는222단어다. 원문·SHA·계수를 보존했고500만 보았다고 정정하지 않았다. 별도로 JS-4/SC-032 P3의 인수 JSON 경계가 미확인이다. 엄격 예산 확인 경로는81/84다.
2. **편집/판/비용:** F1 추출 해석을 새 본문·순위 전에 정정하면서1,411단어가 추가 노출됐다. 일부 component의 마지막 정식판과 정확한 F0 당일 응답을 입증하지 못했다. 초기 metadata retry 영수증 일부가 없어190은 하한이다. 현재 LD틀5자리 부족도 그대로다.
3. **구현 지원 증거:** 같은 경로의 같은 구현판에서 두 조건과 환경을 함께 확인한 직접 근거가 없다. 실제 supplier 설치·실행은0, 원 요청자의 성공 관측도0이다. 원 코드 보존에서 읽은 C2와 prose 요청을 구분했다. 직접링크 경로 변경의 이득은 별도 미실시이며 F1의 성과로 합치지 않았다.

이 결손은 유리한 문서로 링크를 바꾸거나 현재판을 옛판으로 대입해서 해소할 수 없다. 상위4·기능명1개·잘못된 파생형/넓은말 확장·literal-only 감도는 주표 뒤에 분리했다. 기존80본문 재선별,62행 순서 복원,LD 역사적 태그 회수,SC-032/PyLD 예산 밖 시험은 재조사하지 않았다.

## 재개 첫 행동과 필요한 명령·입력

**첫 행동:** 위 결과 SHA의 첫 두 표와 갱신 수용 원장을 읽고 `evidence/paths-ld/preview-exposure.json`의 실제 노출 결손을 확인한다. 다음 실험은 기존 초과 이력을 덮어쓰는 수리가 아니라 별도 복제로 등록한다.

가장 작은 구현 후속 자료는 **JS-6의 원 Ajv판·옵션·주변 payload**, 같은판에서 type=article/id="1"과 id="2"의 두 양성, numeric id=1의 근접음성, 데이터 불변성을 확인한 결과다. 입력과 실행 driver는 [evidence/next-checks/js6-fixtures.json](evidence/next-checks/js6-fixtures.json), [js6-probe.cjs](evidence/next-checks/js6-probe.cjs)에 있다. **이번에는 실행하지 않은 연구자 fixture**다. 원문의 불완전 schema를 자동으로 고친 사용자 성공이 아니다.

정상 빌드한 고정 Ajv checkout이 준비된 환경에서 사용할 명령은 다음과 같다. 현재 runtime 디렉터리나 설치물은 만들지 않았다. 설치/빌드 명령은 해당판 package/lockfile과 지원 Node를 먼저 확인해야 하므로 최신 npm판으로 대신하지 않는다.

```bash
AF060_AJV_DIR="$PWD/docs/workstreams/research/AF-RES-060/evidence/next-checks/runtime/ajv"
git -C "$AF060_AJV_DIR" rev-parse HEAD
test "$(git -C "$AF060_AJV_DIR" rev-parse HEAD)" = 9050ba1359fb87cd7c143f3c79513ea7624ea443
node docs/workstreams/research/AF-RES-060/evidence/next-checks/js6-probe.cjs "$AF060_AJV_DIR/dist/ajv.js"
```

성공해도 이는 추가 예산의 연구자 입력 실행이며 기존 두 행동 경로를 소급 완결로 바꾸지 않는다. 원 환경 성공의 범위도 별도로 남긴다. 깨끗한 예산 복제는 초과 preview를 보지 않은 독자가 stage3의 같은 두 경로·500단어 창을 읽고 판정해야 한다. 누락된 component release/metadata 원영수증도 별도 확보해야 한다. 상세 입력·재개 조건은 [다음 확인](evidence/next-checks/README.md), 각 observations.json의 next_minimum_check에 있다.

## 실제 검사·고정판 재열람

시작 때 지정한 session start 명령을 실제 실행해 manifest를 만들었다. 9핵심 인수 파일의 바이트, 기존16비교, 현재48순위·144슬롯, 첫 표48행·둘째12행·마지막 약점3행, source/condition ID 연결을 다시 확인했다. 원격 결과와 수용 원장의 실제 content를 받아 Git blob으로 로컬 바이트와 대조했다.

지정 검사는 다음 명령 그대로 실제 실행했다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-060/manifest.json --fetch
```

- 실행 주체: root cloud executor.
- 검사 HEAD: `ccde193ec33f68fea5eaef1cc6f6cea803e1823f`。
- 시작/종료 UTC: `2026-11-23T04:31:45.517400+00:00` / `2026-11-23T04:31:56.244706+00:00`。
- 실제 결과: **종료코드0, status=passed, freshness=remote_checked, outside_paths=[], unmerged_paths=[], errors=[], stderr=""**。
- 검사 시 통합판은 `23430e47e068d6889b792b5f11fd750913d975fa`였으며 시작판과 구분했다. 계약·소유 경로 검사 통과이고 연구 가설이나 구현 실행의 인증은 아니다.
- 전체 stdout/stderr·명령·SHA는 [session-check.json](evidence/verification/session-check.json)에 있다. 첫 원격 재열람 영수증은 [remote-reread.json](evidence/verification/remote-reread.json)에 있다.

영수증 커밋4f443396…에서도 RESULT와 갱신 수용 원장을 **다시 원격 열람·파싱**했고, 2026-11-23T04:33:37Z까지 로컬과 일치함을 확인했다. RESULT Git blob은 `7bbf898f1501444c84f28cebbd697126080cc797`, SHA256은 `a9ef912fcc66cbe4619a0801de388f6329af230de57e12f578ed01723485fcb7`이다. 갱신 수용 원장 Git blob은 `262a3cf0e7fd84494c1ab11b7d155d5a676ac57c`, SHA256은 `65257d183dd176b72b54b60861f309f08e8f4287b56f7a4e8dfae8f7ab75bbc8`이다. 수용 원장의 두 최종 검사 게이트는 observed_pass로 바뀌었고 연구 상태는 부분을 유지한다.

## 검토 주체·발행 이력

자체 종합은 root, 전수 공급자/경로 독해는 features_schema와 features_ld, 별도 순위·원장 감사와35새본문/4실제전거 독해는 authority가 수행했다. 추가 검토는 LD4쌍12경로10창, Schema의 Ajv/Blaze6창 범위다. 같은 모델 계열과 일부 공유 문맥을 갖는 검토이며 외부 사람의 눈가림 재현이라고 하지 않는다. [final-audit](evidence/review/final-audit.md)는 실제 범위와 당시 미수행이던 원격 발행 게이트를 구분했고, 이후 root가 위 실제 게이트를 수행했다.

| 묶음 | 원격 SHA | 커밋 UTC / 한국시간 | 고정한 내용 |
| --- | --- | --- | --- |
| 1 | 87818991045cfa221e1b52a9b50c7550301d037b | 2026-11-23 03:19:24 / 12:19:24 KST | 62행·추출 규칙·새 모집/채점 계획 |
| 2 | 412192e28356bee13e4c11f20511ab5ec590662c | 2026-11-23 03:39:14 / 12:39:14 KST | 기능 필드·비용, 새 본문 열기 전 |
| 3 | 5d01a6208edd9f8a20be7b31f7b545cef2200597 | 2026-11-23 03:55:35 / 12:55:35 KST | 새 요구·용어·48순위·경로 계획, 조건 판정 전 |
| 4 | ccde193ec33f68fea5eaef1cc6f6cea803e1823f | 2026-11-23 04:31:01 / 13:31:01 KST | 실제 창·반례·네 조합 비교·두 표·자체 검토 |
| 검사 영수증 | 4f4433960b581caad353322da298fa465258979e | 2026-11-23 04:32:56 / 13:32:56 KST | 실제 원격 재열람·session check·수용 원장 갱신 |

이 HANDOFF는 위 점검 후 작성한 **마지막 단독 파일 커밋**으로 발행한다. 그 커밋의 SHA/시각은 Git 메타데이터에서 확인하며 자기 커밋 SHA를 본문 안에 순환 참조하지 않는다. 마지막 ref를 게시한 뒤 변경 파일이 이 HANDOFF 하나인지, 로컬 tracked/untracked 산출물이 남지 않았는지 확인한다. 원시 임시 cache는 출판 근거로 세지 않았고, 필요한 독해 창·해시·판·관측·원장은 커밋했다. `dot-control.json`을 수정하지 않았고 소유 경로 밖 변경도 없다.
