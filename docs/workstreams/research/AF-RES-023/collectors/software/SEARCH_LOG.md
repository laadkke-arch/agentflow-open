# Homebrew 사건 조사 경로와 한계

관측 창: 2026-11-22 03:10–03:20 UTC. 모델: 부모와 같은 GPT-6 Astra Pro 계열 내부 조사자. 부모의 자료/정답 준비 담당으로 일했으며 독립 맹검 판정자가 아니다. Git 커밋은 부모만 수행한다.

## 선고정한 표집 목적

성공 중복정리/정상 이름변경, 실제 취소, 한 이름의 여러 기능 분리를 함께 찾았다. 최종 본표본 후보는 SW01, SW02, SW03, SW05, SW06이다. SW04는 취소 이유를 확인하지 못해 보충 사건으로 보존한다. 이 다섯 가지를 Homebrew 전체 오병합률의 분모로 사용하지 않는다.

## 직접 사용한 검색과 열린 ID

| 경로·질의 | 실제 열린 원문/ID | 판정·배제 |
| --- | --- | --- |
| GitHub commit search: Homebrew/homebrew-core, `"Revert" "rename"` | 8c2998215320942b1329f5b073fad7bfa33e9976; e2f98568822c4f3f9b180b77a2ef10236189e2fa/Formula/gnu-readline.rb | SW03. alias와 canonical keg의 혼동을 되돌림 이유로 설명한다. boost option rename은 catalog entity 사건과 달라 제외. |
| `"revert" "alias"` | 7f379ed5e4135654176204310ae0f24af0826eaa; 89b2018d807cca3e3f2d127a973991d680c3aa46/Formula/tinyfugue.rb; surviving tiny-fugue fixed file | SW01. 글자차이가 있는 두 recipe가 같은 upstream archive를 쓰는 실제 중복. recipe 차이까지 지우지 않는다. |
| `"eigen3"` | 2dba30d0081bd4677f8483587a2aac45e9b6d5d6; 9a5b8ba823aa4135d911b9f093f84ead00367196 | SW04 보충. 추가6분7초뒤 취소는 확인했지만 취소 이유·잘못된 병합·소비자 사용은 미확인. |
| `"renamed" "postgresql"` | 8060df9169055ee1fb9d1d69fd149c3922e864ba; PR107726 전체 diff/관련댓글; b354eba6f430f0da6b5f8e8d24c25c0411fab517/Formula/postgresql.rb | SW05. 최신버전과 기존DB 유지라는 사용목적을 분리. 2026 추가alias 검색결과는 열지 않았으므로 사건/근거 수에서 제외. |
| `"split" "formula"` | e5e819e64a3104cabb55d46ea8e80d69aaf76d5b; PR231544; 5d3c6448fe87f35290fe191a0f80b9e4c189a63d/Formula/t/tree-sitter.rb | SW06. 동일upstream tag의library/CLI 패키지분리. llvm/prrte/php 등 다른 split 후보는 본문 열람하지 않아 산입하지 않음. |
| `"rename" "pkg-config"` | eb1463eb72712952a10ecdfc201592ca4d24a20a; 4ea8a912eaa74d7606b2c7307899d7c9faf399c5/Formula/lib/libxml++3.rb; after file | SW02. rename단계의 sourceURL·SHA256 동일 대조. 나머지 검색적중은 미산입. |
| `"iojs" "merge"`; `"rename" "mariadb"` | 적중없음 | Homebrew의프로젝트실제합병 사례를 이 검색범위에서 확보하지 못함. 없다는 일반명제 아님. |
| 웹검색: `"tree-sitter" "tree-sitter-cli" "Homebrew" "split" github commit` | irlm/workbench3c93157225ada89394f8939f24fcb4baa98d8d92.patch; salesforce/agentscript issue33; fix0e9601048d83605d43f2e3b9d9d5f516a2222302 | 독립소비자SW-D02/03. issue와그fix는같은소비자기록군으로1건. |
| 웹검색: `"postgresql@14" "brew" "renamed" github` | rails/rails27cb8c618ca3a96a2817e412bfe48dc29a6acfa3.patch | SW-D01. 검색결과의재게시사이트는근거미산입; Rails공식원문patch로돌아가확인. |
| 웹검색: `"libxml++3" "libxml++@3"` | 현재formula목록 검색결과만. 이경로에서는독립옛인용정정본문 미확보 | SW02 소비자효과는미확인. Homebrew미러와같은commit복제는독립증거로세지않음. |

## 접근 실패와 대체한 공식 고정판

- GitHub search_commits는 일시 secondary-rate-limit403를 반환했다. 한 묶음에서 오류를 확인한 뒤 검색 호출을 멈추고 부모에게 알렸다. 계정전환·프록시·우회는 하지 않았다. 알려진 공식 file/commit read와 일반 웹원문으로 작업했다.
- 최초 Readline rename 해시 `adee5315265cc46aa6a3057071527abb16e1cd94`는 Homebrew/homebrew-core에서 connector422(객체없음), shell404였다. 되돌림 commit이 지정한 해시를 다른 것으로 덮지 않았다. 공식 rollback 페이지에서 parent `e2f98568822c4f3f9b180b77a2ef10236189e2fa`를 읽고 그 안의 이전 formula 본문을 확보했다.
- 웹 open은 일부GitHubcommit에 DisabledError였다. 이는그GitHub페이지의HTTP404라고기록하지않는다. 별도connector또는anonymousGET이성공한경우그경로·결과를기록한다.
- libxml++3의현재main옛파일경로404와고정전판connector본문성공을확인했다. 고정전판shellGET은503이므로200으로표기하지않는다. URL생존과엔티티의과거존재는독립관측이다.
- 현재postgresql formula URL은shell503와web404가달랐다. 어느하나를보편현재상태로선택하지않으며, 사건의역사판정은고정commit과Rails소비자수정으로한다.

## 반증 결과

1. 링크+짧은이유가항상부족한가: SW02는sourcearchive와major가그대로인rename이며, major3 wrapper라는목적은old→new mapping으로맞는다. SW01은철자가다르다는이유로모두분리하면중복을놓친다. 다만exactrecipe/build판주장은별도다.
2. 같은주소200이면같은기능인가: SW06 old URL200은현재library만가리킨다. parsergeneration 이유는CLI후계로가야한다.
3. 이력만있으면한후계가정해지는가: SW06은library/CLI중용도가필요하다. SW05 Rails는old→@14를알고도최신요구때문에@16+libpq를선택했다.
4. 정정되면모든인용이자동회복되는가: SW03의동일repo내dependent이동은diff로확인하지만외부인용잔류는미확인. SW06에서는소비자가별도표/README를수정했고, CLI이름을고쳐도0.25.x요구와당시brew0.26.x차이가남았다.
5. 되돌림은항상오병합인가: SW04는실제aliasrollback이나이유가없다. 이를오병합정정으로승격하지않는보충반례다.

## 산입과 실행 범위

`sources.json` 25행 중 본표본의 독립 원자료 산입11개: 사건5, 정책3, 하위소비자3. 전후파일·같은PR·issue의fix는연결자료로보존하되동일사건/저작을중복산입하지않았다. 본표본은SW01/02/03/05/06이며SW04보충사건은0으로센다. 정책은현행판이므로과거시점의정책준수증명이아니다.

이번실행은문서·diff·HTTP읽기와JSON작성이다. brew install, DB이동, formula수정·테스트, 사용자피해재현을실행하지않았다. 소스안의테스트코드와편집자의성공진술은이번실행증거가아니다.
