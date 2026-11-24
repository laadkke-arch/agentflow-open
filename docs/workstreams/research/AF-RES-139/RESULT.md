## 표 1 · 공개 진입점에서 재확인한 결과

| 패키지·함수·입력 ID | 발표순 인접판·배포 URL | 실제 실행 진입점·잠금 | 전후 출력·예외·입력 보존 | 변화·불변·미확인 | 같은 의존에서의 대조 |
| --- | --- | --- | --- | --- | --- |
| simple-statistics · quantile · `even-unsorted/0.25/direct` 및 `sorted_copy` | [6.1.0](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.1.0.tgz) → [6.1.1](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.1.1.tgz). [TAR-6.1.1](sources.jsonl#L51) | Node 24.22.1 `require("simple-statistics")` → `dist/simple-statistics.js` 양쪽. npm v3 lock `deb2a8d2` → `3790f47c`. [전체 잠금](replay/locks.json) | 2 → 2, 사본 2 → 2. 전달 배열 및 원 배열 유지. [실행·전체 입력](runs.jsonl) | 126/126셀 불변. 배열형 p는 사후 별도 경계다. [출력 전용 비교](evidence/output-pairs.csv) | 양판 런타임 직접 의존 0. [대조](evidence/matched-direct.csv) |
| simple-statistics · median 및 quantile p=0.5 · `even-unsorted` 두 전달 방식 | [6.1.1](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.1.1.tgz) → [7.0.0](https://registry.npmjs.org/simple-statistics/-/simple-statistics-7.0.0.tgz). [SS-M](sources.jsonl#L80) | 공개 require와 파일명은 같고 번들 SHA-256은 달랐다. lock `3790f47c` → `ce9f8bf4`. [로드 원장](runs.jsonl) | 두 함수 5 → 5. 원본 `[9,1,7,3]`과 정렬 사본 `[1,3,7,9]`의 순서 보존. | 126/126셀 불변. 좁은 신호는 강제 확인. | 직접 의존 0↔0. 별도 맞춤 설치 0회. [대조](evidence/matched-direct.csv) |
| simple-statistics · quantile · `empty/0.5/direct` 및 `singleton/-0.25/direct` | [6.0.0](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.0.0.tgz) → [6.0.1](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.0.1.tgz). [SS-Q](sources.jsonl#L78) | 공개 require bundle, 각 판 npm v3 lock. [배포·실행](releases.csv) | 빈 배열은 `Error`와 빈 표본 메시지 유지. 한 값의 범위 밖 p는 `Error`와 별도 범위 메시지 유지. 코드 null, 배열 보존. [위임 구현](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/quantile_sorted.js#L14-L37) · [SS-QSORT](sources.jsonl#L1) | 제시한 예외와 배열 모두 불변. API 부재 0. | 같은 빈 직접 의존 집합. [대조](evidence/matched-direct.csv) |
| simple-statistics · quantile 및 median · `nan-mixed`, quantile p=0.5 | [7.8.0](https://registry.npmjs.org/simple-statistics/-/simple-statistics-7.8.0.tgz) → [7.8.1](https://registry.npmjs.org/simple-statistics/-/simple-statistics-7.8.1.tgz). [TAR-7.8.1](sources.jsonl#L77) | 조건부 `exports["."].require`로 같은 공개 파일. lock `241b5c33` → `a8bb6b2d`. [배포](releases.csv) | 직접 2 → 2, NaN-last 정렬 사본 −0.5 → −0.5. 판 내부에서 입력 순서로 답이 갈렸고 각 배열은 보존됐다. [대조](evidence/counterexamples.json) | 판 간 불변. 전달 방식 차이는 30/30판 반복. | 직접 의존 0↔0. 두 깨끗한 경로에서 같은 값. |
| simple-statistics · 두 공개 함수 · 126셀 전부 | 6.0.0부터 7.8.1까지 발표순 29쌍. [배포 URI·순위](releases.csv) · [PKG-NPM-REG](sources.jsonl#L16) | 경로별 30/30판 공개 require. SHA-1·SHA-512 SRI와 진입점 SHA-256 확인. [판별 잠금](replay/locks.json) | 경로별 3,780셀. 값·NaN·예외 이름/코드/본문·배열 전후 모두 합의. [재생](evidence/replay.json) | 변화 0, 불변 29, 미확인 0. 발표순 3,654셀쌍과 semver순 3,654셀쌍. | 29쌍 전부 양쪽 런타임 직접 의존 0. [대조](evidence/matched-direct.csv) |

## 표 2 · 신호와 스칼라 출력의 결합

두 함수 중 한 셀 이상 변한 발표쌍을 기준으로 TP/FP/FN/TN을 계산했다. 변화 분모가 0이므로 모든 정책의 검출률은 산출 불가다. 두 순서와 함수 범위 및 실제 실행 묶음으로 각각 집계한 입력별 행이 있다. [봉인 신호](signals.csv) · [인접쌍별 판정](decisions.csv) · [입력별 점수](evidence/cell-scores.csv)

| 신호·조사 시점 | 비교 가능 쌍·미확인 | 맞는 경보·불필요 경보·놓침·맞는 생략 | 강제 확인·근거 URL | 구체적 반례 |
| --- | --- | --- | --- | --- |
| A · 매 npm 공개마다 실행 | 29·0 | 0/29/0/0 | 0. [npm 시계](https://registry.npmjs.org/simple-statistics) · [원장](sources.jsonl#L16) | 스칼라 관측은 29쌍 모두 이전과 일치했다. |
| C · 공개판의 고정 기능 절 정규화 본문 | 29·0 | 0/0/0/29 | 0. [quantile 절](https://github.com/simple-statistics/simple-statistics/blob/ebc89395f01417fcdfd809c8637902af2ab66eb8/src/quantile.js#L6-L26) · [SS-Q](sources.jsonl#L78) | 같은 절은 6.1.1의 배열형 p 수정을 구별하지 못한다. 고정 스칼라에서는 맞는 생략이다. |
| D · C 또는 공개 번들·대상 파일·직접 의존 지문 | 29·0 | 0/23/0/6 | 0. [빌드 변경](https://github.com/simple-statistics/simple-statistics/commit/7ff90cf39573a4f299d1d8ced05ac62652124ef4) · [CH-ROLLUP](sources.jsonl#L10) | 7.0.5→7.0.6은 대상 소스·좁은 신호가 같고 번들은 달랐다. 126셀 불변이다. |
| E · 배포 함수·직접 위임 본문 또는 그 판의 공지 단어 | 29·0 | 0/2/0/27 | 2. 6.1.1 번들과 소스의 대응이 미해소다. 당시 공지 편집본 미확인에 따른 강제는 0. [6.1.1 배포](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.1.1.tgz) · [TAR-6.1.1](sources.jsonl#L51) | 6.1.0→6.1.1은 스칼라 불변이고 사후 배열형 p가 바뀐다. 6.1.1→7.0.0은 두 비교 모두 불변이다. |
| F · 함수·직접 위임 단독 | 29·0 | 0/2/0/27 | 2. [공개 바인딩과 map](evidence/signal-components.jsonl) | 공지 단어를 보태도 실행 판이 같다. |
| N · 동봉 변경 기록 또는 시각이 확인된 공식 공지 단독 | 29·0 | 0/1/0/28 | 0. [NOTE-6.1.1](sources.jsonl#L88) · [PR #334](https://github.com/simple-statistics/simple-statistics/pull/334) | 6.1.1의 quantile 공지는 배열형 p를 다룬다. |
| E 공지 부재 감도 · 과거 부재를 확정할 수 없는 세 판도 강제 | 29·0 | 0/5/0/24 | 5. 7.7.6·7.8.0·7.8.1 추가. [목록](evidence/release-index.json) · [비용](evidence/cost-summary.csv) | 추가 3쌍의 378개 스칼라 셀은 불변이다. 삭제된 옛 공지 여부는 미확인이다. |

## 표 3 · 질의에 반환한 판과 비용

비용 단위는 `문서 B + 타르 B / 해시 읽은 파일·B / Node 실행 수 / CPU·경과 ms`다. 두 시간은 A 경로의 설치·실행 계측과 로컬 신호 계측을 정책이 처리하는 판에 대해 더한 모형 값이다. 경과에는 문서 열람·무결성 검사도 합쳤고 직접 타르 전송 계측은 별도 열이다. [질의·반환·CPU·전송](costs.csv) · [합계](evidence/cost-summary.csv) · [신호 계측](evidence/static-profiles.json)

| 질의 시나리오·일괄/요청 시 | 반환판·마지막 실측판 | 옳은 답·잘못 이월·보류 | 취득 바이트·읽은 파일·실행 횟수·측정 시간 | 추가 확인할 조건 |
| --- | --- | --- | --- | --- |
| 구판 고정 1회 · A 일괄 / 요청 시 | 각각 6.0.0·6.0.0 | 각 1·0·0 | 일괄 4,330 + 7,743,450 / 0·0 / 30 / 15,772·32,944<br>요청 4,330 + 250,897 / 0·0 / 1 / 692·1,220 | 정확판과 잠금이 주어졌으면 요청 시 그 진입을 한 번 실행한다. |
| 구판 고정 1회 · C·D·E 요청 시 | 각각 6.0.0·6.0.0 | 각 1·0·0 | 각각 4,330 + 250,897 / 0·0 / 1 / 692·1,220 | 첫 정확판 요청의 일괄 개별 값은 [합계](evidence/cost-summary.csv)에 있다. |
| 매 공개판 30회 · A 양쪽 | 마지막 7.8.1·7.8.1 | 각 30·0·0 | 각 128,040 + 7,743,450 / 0·0 / 30 / 15,772·33,236 | 이 표본은 매 발행판과 당시 최고 semver가 같다. |
| 매 공개판 30회 · C 양쪽 | 마지막 7.8.1·6.0.0 | 각 30·0·0 | 각 128,040 + 250,897 / 60·128,040 / 1 / 778·1,512 | 이월 29회. 절에 나타나지 않는 입력 유형은 별도 확인한다. |
| 매 공개판 30회 · D 양쪽 | 마지막 7.8.1·7.8.1 | 각 30·0·0 | 각 128,040 + 7,743,450 / 150·3,723,700 / 24 / 12,738·26,735 | 넓은 번들 지문은 무관 기능 변경에도 반응한다. |
| 매 공개판 30회 · E 양쪽 | 마지막 7.8.1·7.0.0 | 각 30·0·0 | 각 128,040 + 7,743,450 / 176·10,326,582 / 3 / 5,486·11,452 | 강제 2회, 이월 27회. 동봉 공지 27개 파일 532,105 B는 타르 안에 있다. 공지 편집 시점 미확인 강제는 0회다. |
| 끝판 교차 6회 · A 일괄 / 요청 시 | 6.0.0 및 7.8.1 각각 정확판 실측 | 각 6·0·0 | 일괄 8,591 + 7,743,450 / 0·0 / 30 / 15,772·32,948<br>요청 8,591 + 541,318 / 0·0 / 2 / 1,094·1,648 | 두 정확판만 필요할 때. 반복 4건은 응답 캐시 적중이다. |
| 끝판 교차 6회 · C 양쪽 | 6.0.0·6.0.0 및 7.8.1·6.0.0 | 각 6·0·0 | 각 128,040 + 250,897 / 60·128,040 / 1 / 778·1,512 | 마지막판에 구판 답을 3번 이월했다. 실측판과 링크 판을 각각 표시한다. |
| 끝판 교차 6회 · D 일괄 / 요청 시 | 두 끝판 각각 실측 | 각 6·0·0 | 공통 128,040 + 7,743,450 / 150·3,723,700<br>일괄 24 / 12,738·26,735, 요청 2 / 1,365·2,120 | 중간판 자료 취득 및 원 파일 판독은 두 방식에서 같다. |
| 끝판 교차 6회 · E 일괄 / 요청 시 | 처음 6.0.0 실측. 끝 반환 7.8.1의 근거는 일괄 7.0.0 / 요청 7.8.1 | 각 6·0·0 | 공통 8,591 + 7,743,450 / 176·10,326,582<br>일괄 3 / 5,486·11,164, 요청 2 / 4,635·4,023 | 요청 시 두 강제 경계를 읽고 끝판만 실행했다. A 요청도 2회이고 타르는 541,318 B다. |

## Q1 · 발표판과 배포 표면

6.0.0은 2018-04-30 21:18:24.080 UTC, 30번째 7.8.1은 2023-01-15 22:41:15.404 UTC다. 2025년 말까지 정식 후보 37개에서 첫 30판을 뽑았다. 발표순과 semver순은 30/30판 같고 동시각 집단은 0이다. 7.0.9-alpha.0은 사전판이다. Git v7.0.3과 v7.0.4의 판·시계는 현재 packument에 없고 개별 npm URI도 각각 404였다. 범위 전 4.2.0은 시계만 남았다. 두 태그의 당시 공개·철회 경위를 확인할 보존 단면은 미확인이다. [모집 봉인](evidence/roster.json) · [배포 대조](releases.csv) · [404 영수증](evidence/external-access.json) · [npm 철회 절](https://docs.npmjs.com/cli/v11/commands/npm-unpublish#description)

30/30 tar의 SHA-1과 SHA-512 SRI를 검증했다. 태그 커밋과 npm gitHead는 29/30 일치, gitHead 결측 0이다. 7.0.6 태그 `36b042f`와 npm `f9418dc`는 다른 릴리스 커밋에 닿지만 고정 기능 파일은 같다. README는 27판에서 바이트가 다르고 3판은 같다. 공개 실행 파일은 30개 태그의 Git 트리에 없고 타르에만 있다. npm 시각은 각 annotated tag 시계보다 11.494~318.525초 뒤다. 7.0.9 이후 조건부 `exports`가 등장하고 실제 공개 require 파일명은 유지된다. [배포 위치·시계](releases.csv) · [npm gitHead](https://github.com/simple-statistics/simple-statistics/commit/f9418dc09498a163e269c749ac247066f11fd279) · [태그](https://github.com/simple-statistics/simple-statistics/commit/36b042fd1a707c2697fd25a2d321cb4f40011ea0) · [Node 진입점](https://nodejs.org/download/release/v24.22.1/docs/api/packages.html#package-entry-points)

## Q2 · 링크의 함수와 입력 계약

판마다 quantile 108셀과 median 18셀이다. 빈 배열·한 값·짝/홀 비정렬·중복·음수와 소수·NaN 혼합과 단일·정렬된 대조군을 고정했다. quantile은 p=0, 0.25, 0.5, 1, −0.25, 1.25를 사용했다. p=0.5와 median의 일치 검사는 540/540이다. quantile은 범위 및 여러 분위 값을 인자로 받는 계약이 있고 median은 p=0.5로 위임한다. [고정 정의](SCOPE.md) · [quantile 절](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/quantile.js#L4-L24) · [median 구현](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/median.js#L3-L21)

직접/정렬 사본의 판 내부 대조 1,890건 중 120건에서 값이 다르다. 네 변형은 모두 `[3,NaN,-2,1]`이다. 직접/NaN-last 순서에서 quantile p=0은 −2/NaN, p=0.5는 2/−0.5, p=1은 3/1, median은 2/−0.5다. 원 배열과 실제 인수는 양쪽에서 보존됐다. NaN이 섞인 배열을 질문하는 링크에는 입력의 순서를 보여준다. quickselect의 NaN 전순서 계약은 원문에서 확인되지 않았다. [실측 대조](evidence/counterexamples.json) · [quickselect](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/quickselect.js#L17-L63) · [SS-QUICK](sources.jsonl#L2)

## Q3 · 공개시각의 신호와 오늘의 자료

두 함수의 60개 고정 기능 절 모두 배포 src와 일치했고 정규화 본문은 함수별로 계속 같았다. E/F는 58/60개에서 공개 번들 바인딩과 map의 sourcesContent를 확인했다. 6.1.1의 require map에는 sources가 0개이며 패키지 src의 두 본문과 공개 번들의 대응을 해소하지 못했다. 전후 경계 두 개를 강제로 확인했다. Acorn은 연산자·리터럴을 포함한 토큰을 남기고 주석·공백을 버린다. 함수와 직접 위임 지문은 개별 저장했다. [구성 원장](evidence/signal-components.jsonl) · [6.1.1 tar](https://registry.npmjs.org/simple-statistics/-/simple-statistics-6.1.1.tgz)

공식 release API의 연결 터널은 403이었다. 공개 HTML 목록 두 페이지의 16개 release 카드에는 모집판이 없다. 27판은 타르 CHANGELOG의 해당 발표판 본문을 읽었고 뒤 세 판은 동봉 문서와 현재 목록이 함께 비어 있다. 6.1.1만 사전 단어가 적중했다. 현재 공개 본문과 당시 편집본 여부를 다른 필드에 기록했다. 당시 본문 시각을 알 수 없는 **표본 내 공개 카드**는 0이고 3판의 과거 부재 증거는 미확인이다. 이 세 판도 강제하는 감도에서 E 매 공개 실행은 3→6회, 강제는 2→5회다. [목록·실패](evidence/release-index.json) · [당시 CHANGELOG](sources.jsonl#L88) · [감도 비용](evidence/cost-summary.csv)

## Q4 · 실행 진입, 잠금, 대조

두 npm 경로에서 각각 30/30판과 3,780셀을 재생했다. 각 경로에서 숫자 2,400건에는 NaN 390건이 포함되고 예외는 1,380건이다. undefined·API 부재·설치 실패는 각각 0이다. 빈 배열은 데이터 부족 오류, 한 값 이상에서 범위 밖 p는 별도 오류다. 직접 의존이 든 판은 없었다. 태그 전용 두 판의 현재 npm 404와 정상 설치 30판의 실측은 분모가 다르다. 다른 런타임과 ESM/번들러 진입, 당시 사용자 설치는 미확인이다. [실행](runs.jsonl) · [출력 전용 비교](evidence/output-comparison.csv) · [의존 대조](evidence/matched-direct.csv) · [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci#description)

60회의 Node CPU 합은 2.82초, 개별 경과 합은 5.50초다. 설치 CPU 합은 28.30초, 개별 경과 합은 55.59초다. 여러 프로세스가 동시에 실행됐으며 사용자 체감 벽시계와는 별도다. [원 로그](runs.jsonl)

## Q5 · 두 해석이 갈리는 행

- 29쌍 × 126셀에서 공지 없는 관측 변화, 한 단계 밖 위임으로 관측된 변화, 배열 변형만 바뀐 경우는 각각 0건이다. 미확인 쌍도 0이라 미확인 전부를 변화 또는 불변으로 놓아도 표 2의 집계가 같다. 스칼라 변화 양성쌍이 없어 C와 E의 검출력은 산출 불가다. [검출 행](evidence/cell-scores.csv) · [탐색 범위](evidence/counterexamples.json)
- 공지 적중이 있는 6.1.1은 스칼라만 묻는 경우 불필요한 경보다. 사후에 #334의 배열형 p 두 개를 30판과 두 경로에서 실행했다. `[500,468,454,469]`와 `[.25,.5,.75]`의 결과는 6.1.0의 `[NaN,461.5,484.5]`에서 6.1.1의 `[461,468.5,484.5]`가 됐다. 두 번째 벡터의 구판 첫 요소 undefined와 두 NaN도 구별했다. 이 한 경계에서 C는 생략한다. D·E·F·N은 확인하며 E/F는 공개 진입 대응 미확인이 곧 강제 사유다. 벡터를 포함하면 공지의 판정이 달라지고 고정 분모에는 포함하지 않는다. [PR #334](https://github.com/simple-statistics/simple-statistics/pull/334) · [CH-334](sources.jsonl#L7) · [사후 원자료](evidence/posthoc-array-p.json)
- 29쌍 × 두 함수에서 원 JSDoc 절 지문만 바뀐 행은 0이다. 구현 파일의 설명·포매팅과 번들 변화는 있었다. 20쌍에서는 양 함수의 대상 파일, 좁은 신호와 직접 의존이 그대로인 동안 공개 번들 바이트가 바뀌었다. Flow 제거와 7.0.6 빌드 체인 변경은 파일 차이를 의미 차이로 읽을 때 생기는 반례다. 런타임 직접 의존만 바뀐 사례는 없었다. [Flow 변경](https://github.com/simple-statistics/simple-statistics/commit/8a1486776e1e03e33bdd9cdd8783e94229d3b14a) · [CH-FLOW](sources.jsonl#L8) · [반례 원장](evidence/counterexamples.json)

## Q6 · 반환에 붙일 판과 비용

구판 6.0.0 사용자의 p=0.25에 `[9,1,7,3]`을 직접 넣으면 2이고 원순서는 유지됐다. 기능 절과 `A-6.0.0`, 2026-11-24 12:28:54.848 UTC, lock `ab01a949…`를 같이 준다. p의 형태나 NaN의 위치가 달라지면 같은 예의 적용 범위를 다시 확인한다. [6.0.0 기능 절](https://github.com/simple-statistics/simple-statistics/blob/ebc89395f01417fcdfd809c8637902af2ab66eb8/src/quantile.js#L6-L26) · [실측](runs.jsonl)

최신 표본판 사용자에게는 7.8.1의 두 고정 기능 절을 연결하고 E의 이월 근거 7.0.0·12:29:00.928 UTC를 표시한다. 정확한 판·잠금의 실측이 필요하면 `A-7.8.1`·12:29:01.904 UTC가 있다. 7.8.1은 이 모집의 끝판이다. [quantile 7.8.1](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/quantile.js#L4-L24) · [median 7.8.1](https://github.com/simple-statistics/simple-statistics/blob/4dd9bd8cc44c4bd5ad9c73270546520c8af2527a/src/median.js#L3-L18) · [실측](runs.jsonl)

두 지원판 편집자에게는 각각의 lock과 실측을 붙이고 p=0.5 및 median 값 5, NaN 혼합에서 순서를 고정할 조건을 함께 표시한다. 두 끝판 요청 시 A는 2회와 타르 541,318 B다. E는 같은 두 실행에 모든 중간판 타르까지 읽는다. 매 공개판의 E는 D보다 실행 묶음 21회를 줄였고 타르 바이트는 같다. 판·입력마다 정확판 실측의 필요와 발행 빈도가 비용 판단을 가른다. [질의 원장](costs.csv) · [합계](evidence/cost-summary.csv)

타르 30개의 7,743,450 B와 GitHub 목록 두 응답 715,885 B는 실제 취득 본문 크기다. 모형의 문서 B는 Git object에서 읽은 원 파일 크기이며 Git pack 전송량은 미확인이다. 해시 B는 캐시 안 자료의 논리 읽기다. 27개 동봉 문서 본문의 532,105 B는 타르 안에 있다. CPU·경과는 현재 계측으로 합산했다. 설치 경과의 네트워크와 따로 측정한 타르 취득 경과를 중복 합산하지 않았다. 운영 트래픽과 실제 처리시간은 미확인이다. [아카이브와 목록](evidence/release-index.json) · [계측](evidence/static-profiles.json)

## Q7 · 통계 공표판과 교통 적용일

ONS 2023년 4월 19일 기준 전일제 연간 중위 총임금 표시가 잠정 £34,963→개정 £35,004였다. 2024 bulletin의 v1과 정정 후 판에서 2024 연간 중위 £37,430이 유지됐다. 정정은 주변 National Living Wage 설명을 지목한다. ONS ZIP 두 개의 실제 시트·셀과 비반올림 값은 미확인이라 엄격한 원표 조건은 PARTIAL이다. [ONS-2023·ONS-2024·v1](sources.jsonl#L23-L25) · [Table 1](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/allemployeesashetable1) · [접근 영수증](evidence/external-access.json)

SWR 2026-09-21의 Brockenhurst 06:10발 Weymouth 방향 같은 열에서 Sway 06:15는 유지되고 New Milton은 06:20→06:21이다. 공지에 정류장별 수치가 없어 기준표와 9월 20일부터의 임시표를 직접 열었다. PDF 최초 게시 순서·해당 날짜 실제 운행·추가 당일 지시는 미확인이다. 두 분야 대조는 소프트웨어 점수와 별개다. [교통 원문·원장](sources.jsonl#L29-L31) · [비교 셀](domain-cells.csv) · [적용 한계](evidence/cross-domain.md)

34개 고유 1차 저작을 읽었다. 패키지 8, 변경 저작 8, 배포·환경 7, 통계 5, 교통 6이다. 같은 함수의 태그 사본, PR과 변경 기록의 같은 수정, 실패한 원표 접근은 고유 저작 수에서 제외했다. [출처](sources.jsonl) · [검산](SELF_CHECK.md)

| 중요한 불일치·약점 | 다음 조사·자료 또는 실험 | 결론을 바꿀 관측 |
| --- | --- | --- |
| 고정 스칼라 표본에 변화가 없고 6.1.1의 배열형 p는 달라진다. | 배열형 p와 깊은 quickselect 위임의 입력 경계를 별도 사전등록해 시험한다. [#334](https://github.com/simple-statistics/simple-statistics/pull/334) | E가 강제 확인과 정적 신호 없이 새 변화 경계를 놓치면 링크의 반환 범위를 좁힌다. |
| E는 D보다 정기 실행을 줄인다. 두 끝판 요청에서는 A와 실행 수가 같고 더 많은 자료를 읽는다. | 질문 빈도와 판별 캐시 조건을 고정해 취득·실행을 같은 배치에서 계측한다. [질의](costs.csv) | 운영 캐시가 중간판 취득을 대부분 흡수하거나 실행 단가가 바뀌면 비용 우선순위가 달라진다. |
| ONS 공표 표시값과 SWR 계획 PDF를 확인했다. Table 1 원표 셀과 실제 운행은 미확인이다. | ONS 동일 중위 연간 셀 주소·원숫값을 확인하고 해당 SWR 운행 기록을 별도로 조사한다. [접근 입력](evidence/cross-domain.md) | 원표의 판간 관계가 표시와 다르거나 당일 공지가 임시표를 덮으면 해당 분야의 재확인 근거를 바꾼다. |
