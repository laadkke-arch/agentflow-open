# Markdown 목적지 관측 — 주표본과 분리한 D-M1 진단

## 판정 경계

이 파일의 D-M1은 `Official` 범주의 원래 첫 여섯 링크를 보존한 **진단**이다. 자연 M-N1/M-N2는 동결한 기능명사와 주목록 제목이 맞지 않고, 보강 M-S1/M-S2는 단일 처리 목적을 표현하는 기능 절이 없어 빈 자리다. 진단의 수치를 주표본 8자리의 적중·실패 분모에 넣지 않는다. 관련 입력은 원격 봉인 `ea4fa69f841dca2c470b62c3fdf1ee4d9029712e`의 `diagnostic-pools.csv`, `diagnostic-groups.csv` 및 root `evidence/path-plan.json`이다.

관측의 세 층을 구별했다.

1. **원풀 공급자의 조건부 정답:** 현재 serializer 계보에 대해 명시한 호환 조합의 코드·시험 원문을 읽은 D2 판정이다. 원목록 밖에서 얻은 구현 근거를 계보에 연결하지만, 그것을 사용자에게 두 동작 안에 노출된 문서로 바꾸지 않는다.
2. **원풀 여섯 도착 창:** 원주소의 실제 HTTP 도착과 고정 소스 판독 창 안에서 읽은 D1 조건이다. 여섯 창 전체를 합쳐도 완결 ID는 관측 0, 조건 원자 C1만 보인다.
3. **개별 두 동작 시행:** 봉인한34개 경로와 실제 도착의 첫 두 정보 href16개를 합친50개다. 같은 시행에서 함께 읽은 근거만 합치며 서로 다른 시행의 부분조건을 합치지 않는다.

`IM-M1-current-configured`는 **remark-stringify11.0.0** 소스 `1146b3a274fc1f4607111e5d6607a3a769a0e89a`와 **mdast-util-to-markdown2.0.0** 소스 `655f117443d99a08cb839765ff7489aa759f72d0`을 연결하고 `fences=true`, `fence=backtick`, 사용자 handler/extension 덮어쓰기 없음으로 정한 구성이다. wrapper는 `unified ^11.0.0`과 utility `^2.0.0`을 선언한다. 범위에 맞는2.0.0을 정해 읽은 것이며 실제 설치가 그 판을 해석했다는 관측은 없다. utility는 rank4 구현의 계보이므로 두 번째 독립 대안 ID를 만들지 않았다. D3 실행은 하지 않았다. 근거는 `ME-GOLD-C1`, `ME-GOLD-C2`, `M-CODE-PACKAGE`, `M-CODE-COMPILER`, `M-CODE-HANDLER`, `M-TEST-UTILITY`다.

요청 본문의 `react-stringify10.0.2; unified10.1.1`은 원문대로 남겼다. 이를 `remark-stringify`로 고치거나 현재판의 기능을2022년 환경 성공으로 소급하지 않는다. 따라서 역사판 완결은 **미확인**이다. [원요청](https://github.com/remarkjs/remark/issues/941), [선언한 현재판과 의존 범위](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/package.json#L8-L12), [utility의 code 동작 시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L794-L979).

## 정확 도착·판독 창·화면의 차이

여섯 **정확 URL**은 모두 HTTP200으로 직접 열렸고 최종 URL은 요청 URL과 같았다. GitHub 패키지 경로를 웹 읽기 도구로 열 때의 도구 오류는 별도 요청 실패다. 이후 같은 정확 주소의 HTTP HTML을 열어 성공했으며, 다른 소스 주소를 성공한 도착으로 바꾼 것이 아니다. GitHub HTML의 README와 내장 `currentOid`를 소스 SHA에 연결했다. HTTP·HTML 해시·창의 해시·첫 두 href는 `arrivals.jsonl`에 있다.

800단어는 SCOPE에서 정한 **원본 순서의 소스 판독 투영**이다. 실제 브라우저 화면의 viewport, 스크롤 시간, 사용자가 펼친 UI 또는 사람의 이해를 측정한 것이 아니다. 소스에 접힌 `<details>` 내용이 있으면 그 노출은 별도 한계이고, 접힌 내용에서 얻은 조건은 1동작 양성으로 세지 않았다. 유일한 양성인 rank4 `fence/fences` 옵션 원문 L160–167은 정확 HTML에서 `<details>` 조상이0개임을 확인했다(`visibility-check.json`). 첫 두 정보 href도 접힌 예제보다 앞에 있다. 다른 창에는 양성 조건이 없어 접힌 본문의 포함 여부로 현재 완결 수가 늘지 않는다.

fragment는 실제 존재하는 `user-content` anchor와 원문의 해당 절을 확인했다. 코드 fence 안에 예시로 들어간 Markdown 제목은 절 경계가 아니다. `Syntax tree`의 올바른 범위는 L408–432이며, 초안의 경계 helper가 코드 예시를 제목으로 해석한 오류는 새 관측 파일을 제출하기 전에 수정했다. 봉인한 규칙·배열이나 결론은 변하지 않았다.

도착의 첫 두 링크에서 **로컬 Contents 링크는 정보 절 도착**으로 센다. 후보 풀에서 Contents를 제외한 규칙과 다르다. 따라서 parser의 둘째 링크는 `#what-is-this`이고, 연구자가 더 아래에서 발견한 serializer 링크나 유용한 옵션 링크로 바꾸지 않았다. Contents를 제외하면 어떤 링크가 새로2위가 되는지에 대한 감도는 실행하지 않았으며 결과로 주장하지 않는다. `paths.csv`의 `outside_original_pool_urls`는 fragment까지 포함한 정확 URL 이탈을, `outside_original_pool_work_urls`는 다른 저작으로의 이탈을 따로 기록한다. 자체 fragment는 앞 열에만 들어가며 새로운 공급자·구현을 뜻하지 않는다.

## 여섯 도착의 근거

| 도착 ID·원순번 | 실제 문서·절 | 창의 도움 | 첫 두 정보 목적지 | 결손·독립성 |
| --- | --- | --- | --- | --- |
| MA-R1 ·1 | remark README L2–231 | 네 패키지를 소개하지만 C1/C2는 미확인 | 자체 Syntax L398–407; Syntax tree L408–432 | 라우팅에서 같은 전문·창이 먼저 노출됨; 패키지 이름 수는 완결 구현 수가 아님 |
| MA-R2 ·2 | remark.js.org 정적 소개 | C1/C2 미확인 | CommonMark help; unifiedjs.com | playground 미실행; 제품판 미표시 |
| MA-R3 ·3 | remark-parse README L2–284 | Markdown→AST 입력 parser와 serializer 조합 안내 | remark root; 자체 What is this L30–38 | AST→Markdown 요구를 단독 충족하지 않음; C1/C2 출력은 미확인 |
| MA-R4 ·4 | remark-stringify README L2–210; 옵션 L160–167 | 현재 C1 지지: backtick marker와 항상 fence 출력 | remark root; 자체 What is this L28–38 | 일반 serializer 정의만으로 언어·내용 유지 C2를 확정하지 않음 |
| MA-R5 ·5 | remark-cli README L2–212 | 설정·tree 입출력 소개 | remark root; 자체 What is this L26–37 | 같은 계보의 CLI; C1/C2 창 근거 미확인 |
| MA-R6 ·6 | mdast README L2–358; Code L205–268 | lang/value 데이터 모델 설명 | unist#syntax-tree; unist root | 명세이며 실행 구현 아님; 예시는 Markdown→AST 방향 |

근거 URL과 저작·한계는 `observation-sources.jsonl`의 `M-VENDOR-*` 행에 있다. [stringify 옵션](https://github.com/remarkjs/remark/blob/1146b3a274fc1f4607111e5d6607a3a769a0e89a/packages/remark-stringify/readme.md#L160-L167)과 [mdast Code 명세](https://github.com/syntax-tree/mdast/blob/c034ec9ddb8ca2ab16de90d668433624bdd92179/readme.md#L205-L268)는 역할과 출력 방향을 구별해야 하는 직접 반례다.

## 같은 예산의 짝 비교

| 원장 ID·방식 | 대표·숨은 형제 | 직접 완결 ID | ≤2동작 완결 ID 합집합 | 한 시행 최대 | 부분조건의 차이 | 원풀 저작 밖 도착 |
| --- | --- | --- | --- | --- | --- | --- |
| D-M1-A ·18경로 |1,2,3 ·없음;4,5,6은 잘림 | 관측0 | 관측0 |0 | C1/C2 창 근거 미확인 | CommonMark, unified; 완결 관측0 |
| D-M1-B ·14경로 |1,6 ·1의 형제2,3,4,5 | 관측0 | 관측0 |0 | `D-M1-B-P08`의 그룹→4에서 C1만 추가 | unist; 완결 관측0 |
| D-M1-C ·18경로 |1,2,3 ·없음;4,5,6은 잘림 | 관측0 | 관측0 |0 | 판 및 다른 필드 결측으로 A와 동일 | CommonMark, unified; 완결 관측0 |

완결0은 이 문서·경로에서 모든 조건의 근거가 함께 보이지 않았다는 관측이다. 공급자의 실제 기능이 없다는 판정이 아니다. 역사판 ID 집합은 별도로 미확인이다. 원풀 조건부 현재 정답1, 원풀 도착 창 완결0, 직접 완결0, 두 동작 시행 합집합0, 한 시행 최대0, 원풀 밖 완결0을 같은 숫자로 섞지 않았다. 구체 경로50행은 `paths.csv`, 구현 조건15행은 `evidence.csv`에 있다.

B는 rank6의 별도 상류를 눈앞으로 올렸지만 그것은 mdast **명세**였다. 현재 요구를 충족하는 두 번째 독립 runtime은 관측하지 못했다. 동시에 B의 형제 경로가 rank4 옵션을 두 동작 안에 열어 **C1 원자**를 추가했다. 따라서 완결 ID 증감이0이라고 해서 모든 유용한 증거의 증감도0이라고 결론내릴 수 없다. 이 양성은 `Official` 진단에 한정되며 주표본의 양성으로 올리지 않는다.

## 반례 탐색과 감도

| 조사 ID | 반대 가능성 | 실제 관측·방향을 바꾸는 조건 |
| --- | --- | --- |
| MC-01 | 네 번째 이후 URL이 독립 대안인가 | rank6은 별도 상류지만 데이터 명세다. 같은 목적을 만족하는 실행 가능한 별도 공급자가 첫6 안에 있고 노출 창에 두 조건이 함께 있어야 완결 승격이 양성으로 바뀐다. |
| MC-02 | 대표 하나가 이미 여러 구현을 설명하는가 | root L154–177은 네 패키지를 소개한다. parser/serializer/결합/CLI라는 역할 설명이지 두 개의 완결 serializer를 입증하지 않는다. |
| MC-03 | C의 판 결측 때문에 A와 같아졌는가 | 모든 제품판이 목록에서 미상이다. 판만 동일 sentinel로 완화해도 역할·용도 결측 또는 부품 차이가 남아 C=A다. 나머지 필드를 목적지 의미로 채워 결론을 만들지 않았다. |
| MC-04 | 보완 설명이 숨겨져 요구가 손상되는가 | B에서 rank4는 형제로 숨겨지지만2동작으로 C1에 도달한다. A/C에서는4위 잘림과 첫 두 href 제한 때문에 그 원자가 보이지 않는다. 완결 손실은 관측0이며 C2를 임의로 보충하지 않았다. |
| MC-05 | 뒤쪽 병합만으로 첫 세 대표가 유지되는가 | 엄격 C에서는 병합 자체가0이다. 실제로 뒤쪽만 병합된 양성 예시는 이 진단에서 관측하지 못했다. |
| MC-06 | 세 자리를 네 자리로 바꾸면 충분한가 | A/C에 rank4가 직접 나타나 C1을1동작으로 확인할 수 있다. 같은 창의 C2는 여전히 미확인으로 완결 ID 증감0. B는 두 그룹에서 소진돼 대표 변화 없음. |
| MC-07 | 의미가 같은 출력이면 근접 정답인가 | CommonMark 안내는 들여쓰기 코드도 허용하지만 사용자의 backtick 조건을 깨뜨린다. utility 시험의 `fences=false` 또는 tilde marker 설정도 조건을 깨는 직접 반례다. |
| MC-08 | 릴리스 설명을 그대로 믿어도 되는가 |15.0.0 릴리스의 default=true 기록은 시대 차이를 보여준다. 같은 문장의 false 설정에 대한 설명은 옵션 문서·코드·시험과 반대여서 마이그레이션 지침으로 쓰지 않았다. |

감도4행은 `sensitivity-observations.csv`다. [들여쓰기 분기](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/lib/util/format-code-as-indented.js#L11-L20), [기본 및 반례 시험](https://github.com/syntax-tree/mdast-util-to-markdown/blob/655f117443d99a08cb839765ff7489aa759f72d0/test/index.js#L810-L819), [현재판의 기본 변경 릴리스](https://github.com/remarkjs/remark/releases/tag/15.0.0)가 MC-07/08의 직접 근거다.

## 사용 가능한 결론·미실행

**확인된 사실:** 같은 원순서에서 상류 묶음은 별도 공급자의 정보 문서를 올릴 수 있다. 그 문서가 runtime인지와 모든 필수조건을 입증하는지는 별도 판정이다. 부분조건 노출 차이는 완결 ID 차이가 없어도 존재할 수 있다. 제품판 결측을 그대로 둔 C가 A와 같을 수 있다.

**조건부 제안:** serializer를 찾는 독자에게는 문서 역할·입출력 방향·확인한 필수조건을 표시하고, root/CLI/명세를 하나의 실행 대안으로 세지 않는 카드가 유용할 가능성이 있다. 이 연구는 실제 독자의 선택이나 이해를 측정하지 않아 채택 증가를 주장할 수 없다. 카드 예시는 `cards.md`다.

**미확인:** 역사 패키지 식별과 최초 생성 본문, CodeSandbox 첨부, 동일 설치의 실제 실행, UI에서의 노출·행동, primary Markdown 풀에서의 요구별 완결 차이. 다음 최소 조사는 원요청의 패키지 lockfile 또는 보존된 첨부로 `react-stringify` 정체와 정확 설치판을 확정하는 것이다. 현재 조합의 재현을 원하면 격리된 환경에서 utility2.0.0을 정확 pin하고 `M-N1`의 두 code 노드를 하나의 root로 넣어 두 옵션 및 반례를 실행해야 한다. 본 조사에서는 설치·실행하지 않았다.

자료 원장은 `observation-sources.jsonl`14행(기존 root 저작 중복1행 포함), `release-test-sources.jsonl`3행이다. 배당 가능한 별도 공급자 문서5저작(정적 홈페이지 포함), 릴리스/행동시험3저작을 직접 열었다. 더 엄격히 홈페이지를 제외해도 공급자 문서4저작이다. 같은 fragment·HTML/raw mirror·route 재독은 별도 저작으로 세지 않는다.
