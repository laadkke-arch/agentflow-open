## 표 1 · 기능과 검증 경계

| 제품·기능 주장 | 마지막 구판·첫 신판과 URL | 소스·실측 범위 | 입력 및 전후 출력 | 적용할 절·미확인 |
| --- | --- | --- | --- | --- |
| **OL-F** · 목록에 든 단일 Point에서 filter 거부 | [6.6.1](https://github.com/openlayers/openlayers/blob/a8b949a802c4d79ce6fbdcbb2fe3828a83e375b3/src/ol/interaction/Translate.js#L44-L63) → [6.7.0](https://github.com/openlayers/openlayers/blob/b64b8af2eaa9a8efd949d9e8239c169d5cd51851/src/ol/interaction/Translate.js#L44-L63) | 발표판 64/64 소스 적격·판독, 4/64판 선행 브라우저. 경계 ④ 원 로그 4/4행 | features에 포함, filter 거부, layers 허용. Δgeometry (0,0) → (+72,−40), Δcenter (−64,+36) → (0,0). down의 filter 1 → 0회 | 판 고정 Options. EPSG:3857 지도 단위. 복수 피처·다른 렌더러 미확인. [④ 구판 raw](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.6.1-04-r1.json) · [④ 신판 raw](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.7.0-04-r1.json) |
| **OL-L** · 목록에 든 단일 Point에서 layers 거부 | [6.6.1](https://github.com/openlayers/openlayers/blob/a8b949a802c4d79ce6fbdcbb2fe3828a83e375b3/src/ol/interaction/Translate.js#L44-L63) → [6.7.0](https://github.com/openlayers/openlayers/blob/b64b8af2eaa9a8efd949d9e8239c169d5cd51851/src/ol/interaction/Translate.js#L44-L63) | 동일 예정·열람·적격 64판, 4판 실측. 경계 ⑤ 4/4행 | features에 포함, filter 허용, layers 거부. Δgeometry (0,0) → (+72,−40), Δcenter (−64,+36) → (0,0). down의 layers 3 → 0회 | 당시 Options와 목록의 소유 경로. [⑤ 구판 raw](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.6.1-05-r1.json) · [⑤ 신판 raw](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/browser/main/main-6.7.0-05-r1.json) |
| **OL-CF / OL-CL** · 같은 거부에서 목록 생략 | [6.6.1](https://github.com/openlayers/openlayers/blob/a8b949a802c4d79ce6fbdcbb2fe3828a83e375b3/src/ol/interaction/Translate.js) ↔ [6.7.0](https://github.com/openlayers/openlayers/blob/b64b8af2eaa9a8efd949d9e8239c169d5cd51851/src/ol/interaction/Translate.js), 관측 경계 0 | 64/64판, 배포 Translate 지문 16개에서 생략·hit 경로. 네 판의 관련 ②·③ 16/16행 재판독 | ② filter 거부 또는 ③ layers 거부. 두 경계판 각 Δgeometry (0,0), Δcenter (−64,+36) | Options와 hit 경로. 다른 이벤트 순서에서 pan 수치 미확인. [생략 소스 판독](evidence/ol-controls-source.json) · [고정 원 로그](runs.jsonl) |
| **D3-MISS** · 기본 결측과 사용자 지정 unknown | [2.1.2](https://github.com/d3/d3-scale/blob/dcc51a199f74f6fd9c2182155141907c4c157bad/README.md) → [2.2.0](https://github.com/d3/d3-scale/blob/8641fadb2aafd79aa65fb6365b1a4406867fe4c1/README.md#continuous_unknown) | 27/27 정식판 열람·적격·Node 실행, 26/26 인접쌍 대응 실행 | undefined, NaN의 기본 NaN → undefined. unknown 부재 → 지원. 새 판에서 undefined·NaN은 “∅”, null은 숫자 0 유지 | 정의한 수치 domain/range. 색·객체 range 미실시. [구현 변경](https://github.com/d3/d3-scale/commit/4d89464a40ef753ad22413b3e9ce5eea3413792e) · [실행](runs.jsonl) |
| **D3-NULL** · null 처리 변경 | [3.2.3](https://github.com/d3/d3-scale/blob/c7efc99bf1b11d1fd4086e8300445d49be00349f/src/continuous.js#L77-L96) → [3.2.4](https://github.com/d3/d3-scale/blob/8afe6bd4af7a1f0be6b4d231126bdc8a83659ab5/src/continuous.js#L77-L96) | 27/27판·26/26쌍, 26/26 같은 공유 의존 대조. 해당 경계 README 전체 일치 | 기본 null 숫자 0 → undefined. unknown(“∅”)을 설정한 null 숫자 0 → “∅”. NaN·undefined 기본과 사용자 지정값 유지 | README와 3.2.4 공지·코드 같이 반환. [발행 노트](https://github.com/d3/d3-scale/releases/tag/v3.2.4) · [대조 원장](evidence/output-comparison.csv) |
| **D3-NUM** · 기본, clamp, invert | [1.0.0](https://github.com/d3/d3-scale/blob/8d1e283b44b1e5a290ee182107af7a049301956f/README.md#scaleLinear) ↔ [4.0.2](https://github.com/d3/d3-scale/blob/83555bd759c7314420bd4240642beda5e258db9e/README.md#scaleLinear), 경계 0 | 27/27판, 26/26쌍, 숫자 입력 7셀의 변화 0 | [0,10]→[0,100]. 5/−2/12에서 기본 50/−20/120, clamp 50/0/100. invert(50)은 5 | 이 domain/range와 Node v24.22.1. 비수치 range·비단조 domain 미실시. [입력](replay/inputs.json) · [실행](runs.jsonl) |

## 표 2 · 공개 순서의 경보 성능

안별 수치는 **맞게 재확인 / 불필요 재확인 / 놓침 / 맞게 생략** 순이며 각각 인접 공개쌍 개수다. 같은 공개에서 여러 입력 변화가 있어도 ‘하나 이상 변화’에서 한 쌍으로 센다. 미확인 두 극단은 이 표의 관측 집계와 같다.

| 제품·입력·신호 | 예정·열람·적격·비교 가능 인접쌍과 변화/불변 | 맞게 재확인·불필요 재확인·놓침·맞게 생략 | 미확인·강제 확인 | 구체적 반례 URL |
| --- | --- | --- | --- | --- |
| OL-F·OL-L 각각, 소스 기준 하나 이상도 동일 | 63/63/63/63쌍, 1/62 | A 1/62/0/0, B 0/0/1/62, C 1/5/0/57, D 1/31/0/31 | 0쌍/0쌍 | [같은 Options의 실제 우선순위 변경](https://github.com/openlayers/openlayers/commit/207fc99295cc6a126425dd5fcb3aaec1865bd424) |
| OL-CF·OL-CL 각각, 소스 기준 | 63/63/63/63쌍, 0/63 | A 0/63/0/0, B 0/0/0/63, C 0/6/0/57, D 0/32/0/31 | 0쌍/0쌍, 변화 검출률 산출 불가 | [Options 표현 변경과 동일 생략 계약](https://github.com/openlayers/openlayers/commit/5695df3c02b155981e0f3b200935d2925db37763) |
| d3-scale 14셀 중 하나 이상, 또는 unknown.null 단독 | 26/26/26/26쌍, 2/24 | A 2/24/0/0, B 0/0/2/24, C 1/5/1/19, D 2/23/0/1 | 0쌍/0쌍 | [README 그대로인 null 변경](https://github.com/d3/d3-scale/pull/241) |
| d3-scale default.null | 26/26/26/26쌍, 1/25 | A 1/25/0/0, B 0/0/1/25, C 0/6/1/19, D 1/24/0/1 | 0쌍/0쌍 | [3.2.4의 결측 처리](https://github.com/d3/d3-scale/commit/116ac06cd455b253b8df8ed42a3db402e59b401f) |
| d3-scale 기본 undefined·NaN, unknown 지원·undefined·NaN 각각 | 26/26/26/26쌍, 1/25 | A 1/25/0/0, B 0/0/1/25, C 1/5/0/20, D 1/24/0/1 | 0쌍/0쌍 | [원안의 보간기 반례](https://github.com/d3/d3-scale/issues/97) |
| d3-scale 숫자·clamp·invert 7셀 각각 | 26/26/26/26쌍, 0/26 | A 0/26/0/0, B 0/0/0/26, C 0/6/0/20, D 0/25/0/1 | 0쌍/0쌍, 변화 검출률 산출 불가 | [공개 진입 형식 변경에도 수치 유지](https://github.com/d3/d3-scale/releases/tag/v4.0.0) |

## 표 3 · 같은 질의 순서의 검증 비용

괄호 안은 **문서 취득 B / 해시 읽은 파일 수 / 해시 읽은 B / Node 실행 수 / 지도 소스 재판독 수 / 읽은 기능 절 묶음 수**다. 첫 요청 비용과 반복 비용을 더했다. 일괄 초도 비용에는 첫 요청까지 이미 처리한 공개판이 들어간다. tar 바이트와 캐시 재사용을 별도 합산한 48/48 비용 행과 840/840 재생 요청이 있다. [비용](evidence/costs.csv) · [저장 질의와 반환](evidence/query-replay.csv)

| 사용자·요청 시나리오 | 저장·조회할 자료 | 최초·반복의 바이트·파일·실행·절 | 보존한 답·놓친 변화 | 채택 조건 |
| --- | --- | --- | --- | --- |
| d3 구판 고정 1회, A 일괄 / 요청 시 | 1.0.0의 기능 절, lock과 11:24:04.437 UTC 실측 | 일괄 (2,129,101/0/0/27/0/27), 요청 (64,925/0/0/1/0/1), 반복 각 0 | 양쪽 1/1. 기본 null=0, NaN·undefined는 NaN, unknown 부재 | 정확판과 의존이 고정돼 있으면 요청 시 A 1회로 해당 입력 확인. [1.0.0 절](https://github.com/d3/d3-scale/blob/8d1e283b44b1e5a290ee182107af7a049301956f/README.md#scaleLinear) |
| d3 최신판 매 공개 27회, B 두 방식 | 주소와 제목 해소, 마지막 실측판 1.0.0 재사용 | (64,925/0/0/1/0/1) + (2,064,176/0/0/0/0/0) | 양쪽 12/27, 15회 답 불일치. 변경쌍 2/26 놓침 | 입력별 의미를 추가 확인할 탐색 링크 |
| d3 최신판 매 공개 27회, C 두 방식 | 고정 README 절, 문서 지문, 마지막 실측판 3.2.0 | (64,925/1/64,925/1/0/1) + (2,064,176/26/2,064,176/6/0/6) | 양쪽 22/27, 5회 null 답 불일치. 변경쌍 1/26 놓침 | 이전 답을 이월할 때 확인판과 미실측 표시 |
| d3 최신판 매 공개 27회, A / D 두 방식 | 타르와 직접 의존 지문, 4.0.2 절 및 3.2.4 이후 null 경계 | A (64,925/0/0/1/0/1) + (2,064,176/0/0/26/0/26). D (64,925/17/134,023/1/0/1) + (2,064,176/327/3,388,052/25/0/25) | 각 27/27. A 마지막 실측 4.0.2, D는 4.0.1 이월. D가 1회 줄이고 3,522,075 B 해시 읽기 | 파일 해시 비용과 실행 묶음 비용을 비교. [4.0.2 절](https://github.com/d3/d3-scale/blob/83555bd759c7314420bd4240642beda5e258db9e/README.md#scaleLinear) |
| d3 편집자 두 지원판 교차 6회, C | 1.0.0·4.0.2 고정 절과 결측별 반환 | 일괄 (2,129,101/27/2,129,101/7/0/7) + 0. 요청 (64,925/1/64,925/1/0/1) + (2,064,176/26/2,064,176/1/0/1). 반복 요청 캐시 적중 각각 4회 | 일괄 3/6, 4.0.2에 3.2.0의 답을 이월. 요청 6/6, 두 끝판을 실측 근거와 함께 반환 | 두 지원판을 직접 확인하는 경우. 중간판 적용은 별도 확인 |
| OL 최신판 매 공개 64회, C | 10.11.0 Options, 단일 hit와 features 조건, 해당판 기존 Chromium | 두 방식 (9,766/1/9,766/0/1/1) + (756,647/62/756,647/0/6/6). 캐시 적중 1회 | 각 64/64 소스 답. 10.7.2 공개 때 요청판은 10.8.0 유지 | 문구에도 경계가 담긴 이 입력. 네 판 이외 브라우저 적용은 미확인. [10.11.0 Options](https://github.com/openlayers/openlayers/blob/v10.11.0/src/ol/interaction/Translate.js) |
| OL 구판 6.0.0 고정 1회 / 두 지원판 6회, A 요청 시 | 각 판의 고정 Options와 기존 실측, 목록 제공 유무 | 둘 다 첫 (9,766/0/0/0/1/1). 구판 반복 0. 편집자 반복 (13,502/0/0/0/1/1), 캐시 적중 4회 | 1/1 및 6/6 소스 답. 두 끝판 모두 기존 실측 있음 | 판·입력을 구별할 때 적용. [선행 실행 범위](https://github.com/laadkke-arch/agentflow-open/blob/5cf6899ec26ec40045a62b4352076477793bd45a/docs/workstreams/research/AF-RES-131/evidence/acceptance/RECEIPT.md) |

## Q1 · 반환 답을 바꾸는 입력

지도는 **설치판·목록 제공 여부·거부 옵션·hit한 피처 종류**, 축척은 **설치판·해결된 의존·입력 종류·range 타입**이 답을 가른다. 현재 앱의 판과 입력을 알면 고정 절을 직접 반환할 수 있다. 지도 64판 중 소스만 판독한 판은 60개, 기존 브라우저 실행판은 4개다. 축척 정식판 27개는 모두 Node에서 실행했다. [출력 전 고정한 범위](https://github.com/laadkke-arch/agentflow-open/blob/912a1122a7b4b0e20f03e9232ef0959fb5468068/docs/workstreams/research/AF-RES-135/SCOPE.md) · [배포 원장](releases.csv)

d3-scale 27/27 아카이브의 SHA-1, SHA-512 SRI, 버전·진입점을 확인했다. 27개 태그 중 26개는 npm gitHead와 일치하고 3.2.2의 gitHead가 비었다. 3.2.2는 npm에 태그 시계보다 18.750초 먼저 기록됐다. 공개시각 순위와 semver 순위는 27/27 같고 사전판 3개(3.3.0-rc.1~3)는 레지스트리 메타데이터만 읽었다. 아카이브 지문 27개, 공개 진입점 지문 25개, 배포 continuous.js 지문 5개다. 한 시점 packument에서 동일 판 번호 반복 발행은 미확인이다. npm의 이름·판 번호 재사용 제한과 스냅샷의 개별 지문은 별개 근거다. [사전판](evidence/d3-prereleases.csv) · [등록소 시계](https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md) · [철회 문서](https://github.com/npm/cli/blob/v11.9.0/docs/lib/content/commands/npm-unpublish.md#L17-L29)

## Q2 · 당시 신호와 현재 접근

A–D는 알려진 지도 소스 경계에서 정했다. d3-scale의 Node 실행 전에 91개 입력 행의 논리 위치·permalink·소스 구성과 의존 잠금, 공개시각순·semver 경보를 GitHub에 봉인했다. 배포 노트와 구현은 당시 열람 가능 신호를 만드는 데 쓰였으며 미리 읽은 자료로 코드 동작을 예상할 수 있었다. C는 JSDoc 장식, 줄끝, 공백, 독립 버전 배너를 정규화하고 설명 내부 URL·버전은 보존한다. D의 파일 단위 지문에는 번들 배너와 관련 파일에 든 다른 기능도 섞일 수 있다. 경로 이동·필수 파일 결측에서 B–D는 강제로 확인한다. [봉인 신호](https://github.com/laadkke-arch/agentflow-open/blob/1db7e6785e6ade12d598766ba740a2d4886ebf57/docs/workstreams/research/AF-RES-135/signals.csv) · [구성 파일](evidence/components.jsonl)

91/91 정적 기능 절이 해소돼 강제 확인은 0쌍이다. OpenLayers의 현재 생성 API에서 10.11.0 옵션을 읽었고 과거판 6.6.1·6.7.0의 생성 API 본문은 열리지 않았다. 셸 터널 오류의 403은 원 서버 응답과 구별했다. 현재 d3의 README 2곳은 GET 200이었지만 v4.0.2(91,532 B)에만 기능 절이 있고 main(805 B)에서 공식 사이트로 옮겨졌다. 2023년의 이동은 모집 기간 밖의 관측 사례다. 2회 현재 접근의 HTTP 상태를 확인했고 과거 서버 응답은 미확인이다. [HTTP 영수증](evidence/current-http.json) · [지도 API](https://openlayers.org/en/latest/apidoc/module-ol_interaction_Translate-Translate.html) · [README 이동](https://github.com/d3/d3-scale/commit/d6904a4bde09e16005e0ad8ca3e25b10ce54fa0d)

수집 계획/열람/적격은 지도의 Options 파일 64/64/64, README 64/64/64, 예제 HTML 64/64/64이며 파일 유형당 취득 URL 63개다. d3 README는 Git에서 최종 추출 27/27/27회와 앵커 탐색 이름을 고치기 전 27회다. 배포본 안의 README도 d3 27/27판에서 별도로 열었다. 타르의 초기 취득 단위는 지도 64개와 축척 27개다. 문서 추출 두 통과에서 각각 이 91개 타르를 열었고 신호 계산에서 로컬 캐시로 91개를 다시 열었다. Q4의 깨끗한 실행 경로 두 곳은 118개 타르씩 따로 받았다. Git clone 전송량, HTTP 헤더, 사람 판독 시간은 미확인이다. [문서·아카이브 행](evidence/sections.jsonl) · [수집 기록](evidence/acquisition.json) · [재생](evidence/replay.json)

## Q3 · 지도 전환과 불변 구간

16개 배포 Translate 지문에서 구형 15판, 신형 49판과 소스 계약 변화 1/63쌍을 확인했다. 기존 브라우저판 6.0.0·6.6.1·6.7.0·10.11.0의 ②–⑤ 포인터 원 로그에 해당하는 32/32행을 다시 열었다. 양끝 모두 브라우저 실행인 인접쌍은 6.6.1↔6.7.0이다. 6.6.1 ④의 down은 Translate가 거부하고 pan이 수락한다. 6.7.0 ④는 Translate 수락 후 pan down 없이 geometry가 이동한다. ②·③ 생략 대조에서 두 판의 거부와 center 이동은 같다. 새 지도 브라우저 실행은 0회다. [고정 원 로그](runs.jsonl) · [공식 시험](https://github.com/openlayers/openlayers/blob/b64b8af2eaa9a8efd949d9e8239c169d5cd51851/test/browser/spec/ol/interaction/translate.test.js#L154-L288)

2021-08-21의 구현·JSDoc 변경 13:57:11 UTC, 예제의 복수 선택 설명만 바꾼 14:11:57, 08-22 병합 10:29:27, 09-09 정식 npm 17:33:58.060은 각각의 사건이다. Shift 설명 변경은 부모 대비 HTML만 바꿨으며 다음 6.7.0 배포에는 두 hunk가 함께 들어갔다. #12638 원 앱의 장애는 당사자도 재현하지 못했다. 복수 피처 일괄 이동과 Modify의 이벤트 소비는 각각 다른 원인 후보였다. [예제 변경](https://github.com/openlayers/openlayers/commit/3c1e3dcfd554693726ba5160c35538fd0ed49ec5) · [시계 원장](evidence/chronology.csv) · [원 보고](https://github.com/openlayers/openlayers/issues/12638#issuecomment-902683255)

10.7.1 → 10.8.0 → 10.7.2로 공개됐다. 10.7.2는 10.8.0보다 4시간 48분 12.550초 뒤였고 유지보수자가 10.7.0 태그 계보를 확인했다. 네 판의 Translate 지문은 같다. 10.8.0 → 10.7.2에서 C는 생략, D는 직접 위임 묶음 변화로 재확인했다. 소스 계약은 유지됐다. semver 순서에서도 A–C의 합계와 D의 변화 검출은 같다. D의 불필요 재확인은 31→32쌍, 맞게 생략은 31→30쌍이다. 6.3.0 npm→태그 시계 역전은 −426.785초다. [유지보수자 응답](https://github.com/openlayers/openlayers/issues/17326#issuecomment-3886327724) · [두 순서](signals.csv)

## Q4 · 축척의 실제 출력과 원인

Node v24.22.1에서 설치된 공개 패키지명을 사용했다. 1.x–3.x 24/27판은 UMD CommonJS로 build 또는 dist를 로드했고, 4.x 3/27판은 ESM의 src/index.js를 로드했다. 별도 두 설치 경로에서 각각 79/79회 실행했다. 기본 27판, 공유 직접 의존을 맞춘 26쌍 × 2판이다. 같은 79행의 모듈·의존·아카이브와 14셀 재생 불일치는 0행이고 경로당 1,106/1,106개 응답이다. 실행 UTC 순서는 병렬 실행의 관측값이고 공개 순서와 독립이다. [재생 영수증](evidence/replay.json) · [Node 공개 진입점](https://nodejs.org/download/release/v24.22.1/docs/api/packages.html#package-entry-points) · [4.0.0 공지](https://github.com/d3/d3-scale/releases/tag/v4.0.0)

2.1.2→2.2.0은 6/14셀, 3.2.3→3.2.4는 2/14셀에서 변했다. 앞 경계의 공유 5개 의존에 d3-interpolate 1.3.2, d3-array 1.2.4가 있으며 구판의 d3-collection 1.0.7은 신판 직접 의존에 없다. 뒤 경계의 직접 의존 5개는 모두 맞췄고 d3-interpolate 2.0.1과 d3-array 2.12.1을 공유했다. 숫자 0, NaN, undefined, null, 예외, 메서드 부재의 직렬화 코드를 구별했다. 3.2.4는 보간 전에 null을 검사한다. 같은 공유 의존에서도 변화 셀과 두 경계는 그대로다. 사용자의 실제 lockfile과 다른 Node·번들러 출력은 미확인이다. [의존 잠금](replay/locks.json) · [null diff](https://github.com/d3/d3-scale/commit/116ac06cd455b253b8df8ed42a3db402e59b401f) · [수치 보간기](https://github.com/d3/d3-interpolate/blob/v2.0.1/src/number.js#L1-L5)

## Q5 · 놓침과 반증

C의 불필요 재확인 사례는 OpenLayers 9.2.4→10.0.0의 관사 수정 및 d3-scale 1.0.3→1.0.4의 소스 링크 추가다. C가 놓친 3.2.4에서는 README 전체 SHA와 위치가 같은데 null 반환이 달랐다. 별도 릴리스 노트는 그 변경을 알렸다. 3.3.0→4.0.0은 진입 바이트와 형식이 달라졌고 14/14셀의 출력이 유지됐다. 진입 지문은 다르고 답은 같은 공개쌍은 전체 26개 중 22개다. D는 d3의 변화 2/2를 잡고 25/26쌍을 다시 확인하라고 했다. [반례 원장](evidence/counterexamples.json) · [README diff](https://github.com/d3/d3-scale/compare/v1.0.3...v1.0.4) · [3.2.4 릴리스 노트](https://github.com/d3/d3-scale/releases/tag/v3.2.4)

처음과 끝이 같은 세 판에서 중간 값이 다른지도 입력별로 조사했다. 지도 순서 보존 삼중조합 41,664개 중 양끝 값이 같은 적격 조합은 조건마다 18,879–41,664개다. 축척 2,925개 중 350–2,925개다. 두 제품에서 중간 값 이탈은 0건이었다. 사전판과 의존만 달라진 실제 사용자 락은 이 탐색 범위 밖이다. [삼중 비교](evidence/counterexamples.json)

브라우저 실측만 요구하면 지도 63쌍 중 비교 가능 1쌍, 미확인 62쌍이다. ‘하나 이상 변화’에서 62쌍을 전부 변화로 놓았을 때와 전부 불변으로 놓았을 때의 TP/FP/FN/TN은 A 63/0/0/0 ↔ 1/62/0/0, B 0/0/63/0 ↔ 0/0/1/62, C 6/0/57/0 ↔ 1/5/0/57, D 32/0/31/0 ↔ 1/31/0/31이다. 축척은 설치·출력·의존 대조 미확인 0쌍이라 두 극단이 표 2와 같다. 과거 생성 HTML 응답의 증거를 요구하는 경로에서는 B–D의 강제 확인을 적용하며 이 비용은 위 고정 소스 기반 경보에서 빠진다. [조건과 순서별 판정](decisions.csv) · [분모와 극단](evidence/scores.json)

## Q6 · 요청자와 편집자에게 반환

- 최신 사용자에게는 실제판과 입력을 기준으로 기능 절과 최근 실측판을 붙인다. 4.0.2 실행은 2026-11-24 11:24:05.456 UTC이고 숫자·null·undefined·NaN을 검사했다. 4.0.1 실행을 이월한 D의 모델은 마지막 실측판 4.0.1과 4.0.2 경보 생략을 명시한다. 결측 질문에는 기능 문서와 함께 null 처리 코드를 동봉한다. [4.0.2 절](https://github.com/d3/d3-scale/blob/83555bd759c7314420bd4240642beda5e258db9e/README.md#scaleLinear) · [실행 원장](runs.jsonl)
- 구판 프로젝트의 1.0.0 절에는 2026-11-24 11:24:04.437 UTC 실행과 같은 의존 핀을 연결한다. 숫자 0과 null을 구별해야 하는 요청에서는 null→0과 unknown 부재를 돌려준다. 지도에서 판과 목록 유무를 아는 경우는 해당 Options를 반환한다. 목록과 레이어를 동시에 관리하는 6.7.0 이후 편집자는 목록 구성 단계에서 멤버 자격을 확인한다. [1.0.0 절](https://github.com/d3/d3-scale/blob/8d1e283b44b1e5a290ee182107af7a049301956f/README.md#scaleLinear) · [두 지도 옵션](https://github.com/openlayers/openlayers/blob/b64b8af2eaa9a8efd949d9e8239c169d5cd51851/src/ol/interaction/Translate.js#L44-L63)
- 두 지원판 편집자에게는 두 고정 절과 입력별 차이를 함께 준다. d3 1.0.0·4.0.2에 5를 넣으면 모두 50이고 null 기본값과 메서드 지원은 다르다. C의 일괄 검증 마지막 판 3.2.0의 null=0을 이월하면 4.0.2 요청 3회에서 답이 달랐다. 요청 시에는 사이에 경보가 하나 이상 있으면 요청된 끝판을 직접 확인해 6/6회 일치했다. 두 끝판의 검증 범위를 중간판에 확대하지 않는다. [질의 순서](replay/inputs.json) · [행별 반환](evidence/query-replay.csv)

고정 자료의 파일 크기를 사용한 시뮬레이션이다. 불변 URL 당 문서·타르 본문 취득 한 번, 해시 읽기 및 검증용 절은 별도다. d3 최신 A는 tar 3,129,598 B, D는 3,125,990 B이며 D는 실행을 1회 줄이고 해시용 344개 파일을 읽는다. 실제 두 방식의 운영 트래픽, 처리 시간과 통화 비용은 미확인이다. [캐시·tar·검증 비용](evidence/costs.csv)

## Q7 · 인쇄일과 운행 적용일

USGS Vienna에서 같은 1:24,000 도엽의 Survey 1966/Print 1971과 Survey 1973/Print 1980 및 스캔 ID 187062/187064를 2/2 카탈로그에서 확인했다. 고해상도 원면은 0/2다. LoC 작업 사본을 다른 디지털 크기로 다시 저장한 1/1 대조에서 같은 판 번호·도로·색 면의 픽셀이 달라졌다. Vienna의 기관 재스캔 원본 쌍과 범례·현장은 미확인이다. WSDOT 같은 출발·방향에서 2026-11-24 날짜표 첫 셀은 05:30이고 11-26에 공지가 지정한 휴일표 첫 셀은 06:10이다. 공휴일 자체의 날짜별 화면 및 실제 운항은 미확인이다. [두 분야의 직접 근거와 재개 입력](evidence/cross-domain.md)

총 후보 48건에서 필요한 부분을 열람한 자료가 42건이고 중복 계보 등을 제외한 적격 고유 원전이 32건이다. 범주별 요구/적격은 d3·직접 의존 8/11, OpenLayers 6/7, 배포·환경 4/5, 역사 지도 발행기관 3/5, 시간표·서비스일 3/4다. 소프트웨어 두 표본에서 얻은 채택 조건은 고정 입력과 배포판에 한정한다. Q7의 원면 직접 대조가 남아 **PARTIAL**이다. [출처 원장](sources.jsonl) · [검산](SELF_CHECK.md)

| 중요한 불일치·약점 | 다음 조사·원문 또는 실험 | 판단을 바꿀 관측 |
| --- | --- | --- |
| 3.2.4의 null을 C가 놓쳤고 D는 25/26 공개쌍을 요청했다. | [3.2.4 발행 노트](https://github.com/d3/d3-scale/releases/tag/v3.2.4)를 추가 신호로 봉인하고 다른 패키지의 숫자·결측·위임 대조에서 재평가한다. | 새 경계 검출을 유지하면서 바이트·파일·실행 비용이 줄면 사용할 조합을 좁힌다. |
| OpenLayers 소스 63쌍과 양쪽 브라우저 실측 1쌍의 분모가 다르다. | [원장](runs.jsonl)의 입력을 다른 렌더러·복수 멤버로 확장할 경우 실제 전달 이벤트를 함께 기록한다. | 단일 Point와 달리 다른 멤버의 geometry 또는 거부 조건의 전파가 바뀌면 반환 조건을 좁힌다. |
| Vienna GeoPDF 원면 0/2, 기관 재스캔 쌍 0/1 및 Thanksgiving 날짜별 화면 1/2가 남았다. | [두 원면 및 서비스일 입력](evidence/cross-domain.md)을 열고 하단 범례, 서비스 날짜와 같은 방향 터미널 셀을 보존한다. | 같은 식별자의 새 스캔에서 인쇄판이 유지되거나 휴일 날짜 직접 표시가 계절표와 다르면 분야별 재확인 조건을 고친다. |
