# Markdown 목록·대표 봉인 기록

**현재판 v2:** 아래 초기 기록은 v1 보존이며, 말미 정정이 현재 판정이다. 주표 M-S1/M-S2는 미충원; Official6은 D-M1 진단이다.

## 출발과 판

주목록은 [awesome-remark 고정판](https://github.com/remarkjs/awesome-remark/blob/82427708991528ad21475151aea2311f2699d549/readme.md)이다. remark README의 플러그인 발견 링크는 L210, L212, L214 순서로 선별 목록, 전체 목록, topic을 안내한다. 사전 SCOPE의 첫 목록 규칙에 따라 첫 링크를 사용했다. 후보 수·승격 여부를 보고 전체 플러그인 목록으로 바꾸지 않았다.

- 주목록 commit: `82427708991528ad21475151aea2311f2699d549`, blob: `ea5a8dd29e0fcf0d241584cc6484021bf15380c5`, commit시각: 2024-10-03T09:29:37Z.
- 출발 README commit: `1146b3a274fc1f4607111e5d6607a3a769a0e89a`, blob: `73cd48204e544806f24fb0533792f02c2ff50871`, commit시각: 2026-09-27T13:21:39Z.
- 두 자연 요구는 2022년에 생성되었다. 확보한 목록판은 요청 뒤이므로 **현재 재탐색**이며 당시 가용 목록 재현이 아니다.
- 주목록은 remark 생태계 자원을 선별한 목록이다(L7-L23). 공식 부품, 플러그인, remark 위에 만든 도구, remark를 쓰는 프로젝트, 다른 목록으로 나눈다. 정렬 기준 설명은 없고 소스 편집 순서만 확인했다.
- Contents는 제목 TOC의 복제이고 License는 비정보 링크라 스캔에서 제외했다. 나머지 제목 5개를 파일 순서대로 스캔했다. Related lists는 routing 성격임을 별도 표시했다. 이것이 사전 operational heading 정의의 소진이며 임의로 패키지별 소제목을 만들지 않았다.

## 자연층과 보강층

| 슬롯 | 사전 요구 | 결정 | 근거 |
| --- | --- | --- | --- |
| M-N1 | issue941: AST code→Markdown, lang-null backticks와 lang정보 보존 | 제목 무매치, 관측 후보0 | 고정 기능명사 code/code block/lang/backticks/string 중 같은 철자 제목 또는 발행 별칭 없음 |
| M-N2 | issue955: inline/block code의 HTML entity 출력 | 제목 무매치, 관측 후보0 | code block/span/raw result/greater-than signs 제목 또는 발행 별칭 없음 |
| M-S1 | M-N1 재사용 | 첫 절 Official, 후보6 | L36-L41의 첫6 실제 정보 URL. 총8href 중6상한; r1~5 같은 remark 상류, r6 mdast |
| M-S2 | 없음 | C기회 관측0, 보강 빈자리 | 첫5절 모두 제품판이 명시되지 않아 strict C key 충돌 없음 |

M-S1의 목적 연결은 M-N1이 첫 적격 요구이면서 Official에 입력 파서·출력 생성기·AST 명세가 명시되어 있어서다. 이는 목록 설명 수준의 적격성이고 실제 필수조건 충족 판단은 아직 하지 않았다. M-N1과 M-S1의 공통 요구 ID는 M-N1이다. 목록에 보이는 r6는 명세로 소개되며 실행 가능한 독립 구현으로 선분류하지 않는다.

## 대표와 키

`pools.csv`의 6행이 정확 URL, 명칭, 설명 길이, 상류/부품/용도/판/역할을 고정한다. `groups.csv`는 4슬롯×3방식 12행이며 미관측·빈자리도 유지한다.

- A 대표 원순번은 1,2,3; 뒤4,5,6은 슬롯 밖이다.
- B 대표는 1,6; 첫 그룹의 숨은 형제는2,3,4,5이다. 두 그룹만 있으므로 세 번째 자리는 비어 있다.
- C 대표는1,2,3; 모든 제품판 미상, 특히1/2의 공개 용도도 목록만으로 명시되지 않아 원멤버 단독이다.
- B 상류는 단순 `remarkjs` 조직이 아니다. r1~5는 같은 `remarkjs/remark` 프로젝트의 저장소/웹사이트/monorepo 부품으로 목록이 귀속한다. r6는 별도 `syntax-tree/mdast` 명세다.
- 목록 commit SHA, main, 홈페이지를 제품판으로 쓰지 않았다.
- 4슬롯 감도: A/C는 r4 stringify를 직접 대표로 올린다. B는 같은2그룹이다. C판미상만 sentinel로 완화해도 나머지 부품·용도값이 달라 r1~5를 함께 합치지 않는다.

## 봉인 전 노출의 정확한 예외

**M-S1-R1과 라우팅 README는 같은 저작이다.** 후보 배열을 만들기 전에 remark README 전체를 라우팅 입력으로 읽었다. 그 안의 본문 L8 이후와 예시·패키지 설명 L28-L184가 R1의 도착 본문과 겹친다. R1을 목적지 비노출이라고 주장할 수 없다. 최초800단어 창 안의 내용도 이미 노출되었다. HTML 브라우저 화면을 읽은 것은 아니며 고정 raw Markdown 본문을 읽었다.

이 노출은 source `M-LIST-ROUTE`와 pool row `M-S1-R1`에 기록했다. R1의 배열·상류 키는 주목록 라벨/URL에 근거하고 body의 적합성 정보를 키에 추가하지 않았다. R2~R6의 목적지 본문은 아직 열지 않았다. r2가 나중에 r1로 redirect하더라도 실제 redirect를 지금 가정하지 않는다. 따라서 전원 목적지 이전 봉인 수용조건은 R1 때문에 **부분 충족**이다.

보조 `doc/plugins.md`의 목록 설명도 이 단계에 읽었으나 거기에서 후보를 모집하지 않았다. 별도 work_id 한 건으로 범위·호환성 표시·기여 규칙만 기록했다.

## 기록 파일

`catalog-receipts.json`, `catalog-link-inventory.json`, `section-scan.csv`, `slot-status.csv`, `pools.csv`, `groups.csv`, `sensitivity-arrays.csv`가 목적지 이전 고정 입력이다. 출처 본문 전문은 cache에만 있고 Git 제출 자료는 URL·SHA·해시·행·자체 요약이다.


## v2 사전 정정 — 기능 절과 편집 분류를 구별

v1은 원격 `cd940aa340a5396611d028002ffc7150981f853a`에 남겨 두었다. 목적지를 추가로 열기 전에 기능 절을 ‘제목 또는 바로 이어지는 설명이 하나의 검증 가능한 처리 목적을 말하는 절’로 명확히 했다. 위 v1의 Official 보강 선정은 철회한다. Official은 공식 귀속, Plugins는 부품 분류, Built on은 구현 계보, Built with는 채택 관계, Related lists는 다른 목록 탐색이다. 모두 공통 기능 목적이 없어 적격 기능 절 **관측0**이다. 5개 편집 제목의 원문/링크 수는 바꾸지 않았다.

- M-S1/M-S2 본표 자리는 미충원이다. 모집 대상 기능 절이 없으므로 실제 적격 풀의 기회/완결을 0개 후보 성공률로 바꾸지 않는다.
- Official의6href와 A/B/C는 `D-M1` 진단으로 보존하며 본표8자리·자연/보강 분모에서 제외한다. 공유 목적은 M-N1 그대로다.
- `pools.csv`는 header-only, `groups.csv`는 본표4자리×3방식의 빈 배열12행이다. diagnostic 파일들은 예전 원풀을 보존한다.
- bare 저장소/웹사이트/package-directory URL은 문서역할을 overview라고 단정할 수 없어 C 역할 미상으로 정정했다. r6은 목록이 명세라고 직접 밝혀 reference를 유지했다. 제품판은 모두 미상이다. C=A 결론은 그대로다.
- D-M1-R1의 라우팅 README 선노출은 그대로 유지한다. 나머지 목적지 본문은 아직 읽지 않았다. 이 정정은 정답 결과를 보고 고른 것이 아니다.
- 목록 편집 분류와 기능별 요구를 구분하지 않은 v1 운용정의가 원인이다. `function-scan.json`과 `section-scan.csv`가 영향행/이유를, root CORRECTIONS가 전역 변경을 보존한다.
