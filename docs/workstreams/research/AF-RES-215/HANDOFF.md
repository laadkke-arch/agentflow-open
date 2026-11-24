# AF-RES-215 HANDOFF

- **status: PARTIAL**
- 작업: RSS 리더 데이터 이관의 송신·수신·사건 연결. 현재 결과 SHA(이 HANDOFF 제외): `041af93d09f687dc008203f0a5ca04b00ec2d334`.
- 작업 브랜치: `work/research-af-res-215`; 시작 통합판 `87ffc1539bcf33da0fccf45eb15982a02d93e409`; 계획판 `bb146773bbffba5e724e8c842951e2c25198c2da` 대비 ahead 5/behind 0, dot-control만 변경. 착수 당시 AF-RES-215 RUNNING, 의존 204 중앙 DONE / 자체 PARTIAL, 의존 result SHA `1915a735edd7f432f5a6d3de858049c98a1fcf83`. 205–207 미조사(범위 밖).
- 대표 산출물: [RESULT.md](./RESULT.md), [sources.jsonl](./sources.jsonl), [fields.csv](./fields.csv), [migrations.csv](./migrations.csv), [routes.csv](./routes.csv), [frame.csv](./frame.csv), [SCOPE.md](./SCOPE.md), [REFINEMENTS.md](./REFINEMENTS.md), [SELF_CHECK.md](./SELF_CHECK.md).
- 묶음: 1 범위 `adccb800201c92bba6c13081bef4bcff4969eaa8`; 2 원장 `a5cf05ae5d351216aa62b4dc730c2e8532d97ce0`; 3 매핑/표 `9968713eb54980bd978b6d68038856e5a33eed1e`; 4 반례/정정 `db4f4a0a22e4fff189bd50fae8582f052c0d2047`; 5 결과/자체점검 `06f66e5c7e49060cc7f88ec82753105913bfdf6f`; 5b 원댓글 source Keywords 정정 `041af93d09f687dc008203f0a5ca04b00ec2d334`; 마지막 이 HANDOFF 단독 커밋.
- 마지막 result SHA에서 GitHub connector로 9개 파일 직접 다시 열어 대조했다. 47 source rows/38 unique admitted URLs/13 lineages, CSV width consistent, source ID 참조 미존재 0, 12 field rows 및 assessed frame slots, 4 fixed cases, 3 routes, 필수 표 행 12/4/3 및 마지막 weakness 3, C01 tag 정정 세 파일 확인. integration→result compare ahead 6, 변경 9 파일 전부 owned_path. dot-control 등 다른 경로 수정 없음. 이 검증은 구조적 점검이며 내용·프로그램의 독립 검증이 아니다.

## 실질 결과
1. OPML 목록만이면 피드 URL/폴더의 규격과 1.29.1 수신 경로가 연결된다. 폴더 nesting/order, existing feed, 비RSS 제한은 별도. 항목 ID/link, 별표, 사용자 태그, 읽음 상태는 OPML에 이관되지 않는다. frss:filtersActionRead나 unicityCriteria는 미래 규칙이지 상태 값이 아니다.
2. 별표: 공개 비식별화 Inoreader-derived starred.json 2개(3+2 items, S02/S03)에서 long id, portable origin.streamId, alternate/canonical, explicit star, read presence/absence, label을 직접 확인. 고정 FreshRSS 1.29.1 SHA b2c50115baa36c217e939ee3ea8ecfae52f91abd F01–F04와 정적 연결. 5/5 explicit stars, 3/5 explicit reads, 2/5 read/unread absent. 읽음 부재를 FreshRSS는 mark_when.reception에 따라 채우므로 다른 수신기의 false 기대(S04)와 달라질 가능성. 두 fixture는 송신 표본이지 FreshRSS 실행 결과나 전체 계정 전수가 아니다.
3. 고정 네 사건: 3141 Thunderbird→FreshRSS(별도 참가자 source sample; 원요구자의 완료 없음), 5583 TT-RSS→1.21.1-dev(0 favorites→patch 후 일부 도착, 중복 남음), 6581 FreshRSS backup→1.24.1(복원 보고, 중복 삭제 후 별표 손실), 4086 sender 미상 OPML(order complaint). Inoreader→FreshRSS 동일 사용자 실제 결과 0/4 사건, 0/12 필드 관측; 실패율로 표현하지 말 것. 보강 S08 Inoreader→Obsidian RSS Dashboard는 같은 사람 긍정 테스트 보고지만 다른 수신기이며 필드별 관측 없음. S01/S04는 별도 수신기 설계/기대값, 독립 평가 아님.
4. 23 이상 고유 원자료 조건 충족: 원사건 4/4, Inoreader 6/4, OPML 4/4, fixed FreshRSS 8/7, Zotero 7/4 + 보강 9. 47 행 중 제외 9; 미러·댓글 중복 산입 없음. 표준 직접 예제 두 URL timeout 재시도 실패; 고정 FreshRSS OPML 예 사용. Inoreader 전체 account ZIP/manifest/per-tag 파일·read history 범위, exact case payload와 screenshot 일부, FreshRSS 자체 import-specific expected-output fixture, Zotero 실제 RDF export specimen 미확인. 12자리 매핑과 사건 분리 완료했으나 실제 end-to-end 검증 미충족이라 PARTIAL.

## 색인 반영 제안 (직접 수정 금지)
목적→요청 필드→송신 artifact+판/원문→수신 parser+판/원문→identity join→loss gate→동일 사건 evidence. OPML feed/folder 조건부 링크와 starred.json sample+parser 링크를 서로 다른 항목으로; full account history는 HOLD/PARTIAL(미확인)로. 원자료 종료/삭제일과 파일 보유 여부는 첫 링크 선택 조건. Zotero RDF/RIS/backup은 유사 원리 링크로, RSS read state의 직접 대체 아님. 204 engine/data 조합 구분을 보존. 참고: C02, C03, C04와 S02, S03, S04의 정확한 원문 구간은 RESULT/원장. 중앙 status 변경은 통합 담당자에게 남김.

## 첫 재개 행동 / Codex 검증 (이번 세션에서 미실행)
1. **첫 행동**: 고정 sender fixture S02/S03를 열고 FreshRSS 고정 1.29.1의 F01/F06 파일을 나란히 대조한 뒤, 이미 마련된 격리 테스트 환경/사용자에서 두 reception 설정으로 실행. 전체 Inoreader 계정 ZIP 공개 비식별 manifest/README를 확보하면 해당 ZIP 전체가 아니라 먼저 파일명과 내용/범위를 목록화. 사용자 실제 계정 로그인/이관, 새 외부 계정 또는 live API 호출은 수행하지 않는다.
2. 별도 Codex 실행 환경에서, 의존 설치/환경 준비가 이미 승인된 격리 로컬 테스트 인스턴스일 때 아래 명령을 실행한다. 없는 경우 설치 승인 없이 중단하고 필요한 환경을 보고한다. 기존 계정/운영 DB에는 실행하지 않는다.

```sh
git clone https://github.com/FreshRSS/FreshRSS.git /tmp/af215-freshrss
cd /tmp/af215-freshrss
git checkout --detach b2c50115baa36c217e939ee3ea8ecfae52f91abd
git rev-parse HEAD
mkdir -p /tmp/af215-fixtures/a /tmp/af215-fixtures/b
curl -fL 'https://raw.githubusercontent.com/amatya-aditya/obsidian-rss-dashboard/96e930a268ade75c61e60e8427cd101bfb2f8cae/test_files/fixtures/starred/starred.json' -o /tmp/af215-fixtures/a/starred.json
curl -fL 'https://raw.githubusercontent.com/amatya-aditya/obsidian-rss-dashboard/96e930a268ade75c61e60e8427cd101bfb2f8cae/test_files/fixtures/starred/starred-inoreader.json' -o /tmp/af215-fixtures/b/starred.json
# F06 cli/import-for-user.php: already configured disposable test user only
php cli/import-for-user.php --user="$AF215_TEST_USER" --filename=/tmp/af215-fixtures/a/starred.json
# Repeat same file after snapshot; separately run b against a clean test DB
php cli/import-for-user.php --user="$AF215_TEST_USER" --filename=/tmp/af215-fixtures/b/starred.json
```
실행 전 F06 옵션 파서에서 플래그 형태를 재확인. `AF215_TEST_USER` 및 `AF215_TEST_DB`는 이미 구성된 격리 환경에서만 지정. a와 b를 동일 실제 계정으로 합치지 말 것. 각 clean DB 또는 snapshot에서 수행. FreshRSS actual input/output을 별도 artifact로 기록. SQLite 사용 시 `sqlite3 "$AF215_TEST_DB" '.tables'`, `sqlite3 "$AF215_TEST_DB" '.schema'`로 실제 prefix 및 관계 테이블명을 확인하고 그 DB의 feed URL/category와 entry(feed_id/guid/link/is_read/is_favorite), entry-tag 관계를 추출. 표본 자체는 placeholder URL이고 네트워크 fetch/갱신은 하지 말 것. 초기 OPML test는 O03 또는 비식별 두 nested category 예를 격리 로컬 URL로 사용. 현 테스트 실행/DB schema/출력은 이번 세션 미검증.
3. 입력/기대/반전:
   - S02 a: suffix 0001 explicit read/star true; 0002 read absent, star true, Design/art labels; 0003 new feed, star true/read absent. F01 예상 missing read=mark_when.reception. reception=false/true 환경에서 0002/0003 값 비교; S04의 기대 false와 같/다름 명시. b: b1/b2 read/star true, b1 Misc. 출처별 URL/link/GUID 그대로 보존되는지 확인. raw IDs와 original RSS publisher GUID는 동일하다고 가정하지 말 것.
   - 재import 전후 row count뿐 아니라 feed URL/category, id_feed/guid/link/flags/label relation 동일성 및 unintended updates 확인. same GUID different feeds를 두 items로 복제/변형: file-wide article_to_feed 및 newGuids가 잘못 합치거나 drop한다면 partial-loss, 독립 보존되면 위험 판정 완화. canonical-only와 alternate-vs-canonical 다름, placeholder/no feed, numeric streamId, alias URL/redirect/proxy는 각각 별도 test; 실제 live redirect fetch 금지, synthetic local aliases만.
   - starred filename vs favorites vs generic .json, items vs articles wrapper, explicit star removed with label present; F09 역사판 patch와 F01 1.29.1 차이를 비교. explicit read false/absence, label URL escaping/자동 folder label, nested same-name folder, existing feed category conflict. FreshRSS OPML import first, item next, then reimport; 각 case clean/reset snapshot. 이전 데이터 지우는 방식으로 중복 해소하지 말 것. 기대는 코드 유도이며 실제 반전 결과가 우선.
   - 공개 full archive specimen을 확보하면 `unzip -l <sanitized.zip>`, `unzip -p <sanitized.zip> <README-or-manifest>`로 실제 entry 이름/개수/시점을 확인하고 개인정보 없는 범위에서 각 파일 field/path를 기록. 전체 ZIP 직접 import는 일반 JSON/미지원 형태 오해 위험이 있으므로 먼저 확인. no raw specimen이면 범위 판정 HOLD 유지.
4. 이 작업의 불일치 3건은 RESULT.md 마지막 표. 원장/결손/정정은 REFINEMENTS.md. 위 실제 명령은 Codex 검증용으로 제안만 했고 실행하지 않았다. repo 파일/CSV/JSONL structural comparison만 수행. 독립 검토/실제 사용자 실험 0. 초기 브리프에서 질문/이슈/반례 유형을 이미 받았고 사후 검색/정정 수행; blind 아님. 
