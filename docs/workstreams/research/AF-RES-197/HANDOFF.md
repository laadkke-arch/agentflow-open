# AF-RES-197 HANDOFF

**실제 판정: PARTIAL** — 문헌 비교와 UI/객체/서버 수신 경계까지 완료. 자연 사건 모집과 원작성자 ID 연결 미충족. DONE으로 승격하지 말 것.

- 시작 통합 SHA c860f8240ab7b7077e2d5b63e438ddd83ff69a27, 계획 SHA 050278651b11a2a3a49d45baebf41c707c06b700 대비 4 commits ahead / dot-control.json만 변경(착수판 비교). 선행 AF-RES-189 지정 6fa4492e0e1a8c0510f573e914b4288786e0e694 읽음. 배정 브랜치 work/research-af-res-197.
- 결과+자체점검이 들어 있는 직전 고정 SHA: **1f01333bcac478e879ce1c61bbd5310c4fbbc127**. RESULT 작성 commit 64fda66b55c9be18cb2326c083f6ffed8407166e. 해당 RESULT commit에서 10개 파일 재열람, 직전 SHA에서 RESULT/SELF_CHECK/sources/frame 다시 읽음. GitHub compare: 시작→직전 13 commits ahead, behind 0, 변경 11개 전부 owned_path. dot-control.json 작업 수정 없음.
- 대표 파일: [RESULT.md](RESULT.md) (요구 표 3개, Q1~7, 경쟁 설명, 대안, 마지막 약점 3행), [SELF_CHECK.md](SELF_CHECK.md), [sources.jsonl](sources.jsonl), [frame.csv](frame.csv), [requests.csv](requests.csv), [selection.csv](selection.csv), [answers.csv](answers.csv), [SCOPE.md](SCOPE.md), [body_freeze.md](body_freeze.md), [counterexamples.md](counterexamples.md), [table_draft.md](table_draft.md). 
- 산입: 44 distinct work IDs / 21 lineages / 69 ledger rows. 유형별 실제/목표: 원사건 자료 19/6, API·태그·시험 11/8(8 pinned code/test + 3 v8 family docs), 변경·소비자 8/4, QGIS 6/4. 자료 수 부족 0, excluded/failed/preview/duplicates 25. 자연 표본 확정 0/3 (잠정 #4873 1, 경계 #5695 1, 결측 1), **3 적격 순위 미확정**. 원작성자 opening body→동일 literal ID 후속/예제 0/1. 실제 server payload/receiver/processed ID 관측 0. sandbox 세 접근 실패. 정확 설치 patch 모르는 사건 및 원문 최초 revision 미복원. TanStack 일부 회신이 search 결과와 함께 먼저 노출됨; 독립 사전판정 아님. 독립 검토/실행 0.
- 요점: MUI #14070/#2672 current page 조작 P, #14074 same-filter visited selected IDs V; 저자 회신에서 batch 업무 예시와 다른 filter cleanup 수용. TanStack #4873의 persistent IDs vs loaded objects, #4555 default index aliasing, #4781 global intent vs allIds response 구별. UI로 확인한 것 이상 서버 실행을 권하지 않음. QGIS display vs layer subset vs selected export의 별도 집합. 조건 명시 P면 즉답, ambiguous all에는 한 문장 범위 질문. 최종 제품 구조·랭킹은 미정.
- 색인 반영 제안(직접 수정하지 않음): “AF-RES-197 PARTIAL — server pagination select-all target scope: page toggle vs explicit stable IDs vs filter universe/exclusions; receiver evidence missing; natural recruitment pending; path docs/workstreams/research/AF-RES-197/, result ref 1f01333bcac478e879ce1c61bbd5310c4fbbc127.” 전제: PLAN 운영자가 partial을 수락하고 별도 재개 할당. 실제 result commit은 이 HANDOFF를 포함한 브랜치 최종 SHA를 기록.

## 재개 첫 행동
1. **독립 body-only 모집부터**. GitHub 공개 discussion 검색의 정렬 목록 접근 오류 X09/X10을 우회 인증/스크래핑하지 말고, 정상 GitHub CLI/API 권한이 있는 환경에서 공개 issue/discussion 검색 응답을 날짜 범위로 나누어 확보한다. 본문만 저장하고 최초 createdAt, number 정렬·동일 원작성자/예제 중복 병합, subsequent row action 동사 표기. 첫 3 적격의 body 판정을 먼저 commit, 그 뒤 comments. MUI는 이미 body freeze 있음. 아래 명령은 실행하지 않은 재개 입력 예; 현재 세션에서 CLI/GraphQL/설치 권한 확인 못함. 이미 답에 노출된 이 세션은 독립 코더 역할 불가.
```sh
gh search issues --repo TanStack/table --created 2022-01-01..2025-12-31 --sort created --order asc --limit 1000 --json number,createdAt,url,body 'pagination "row selection"'
gh api graphql --paginate -f query='query($q:String!,$endCursor:String){search(query:$q,type:DISCUSSION,first:100,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{... on Discussion{number createdAt url body}}}}' -f q='repo:TanStack/table pagination "row selection" created:2022-01-01..2025-12-31'
```
   입력 후보는 exact row selection / rowSelection / selected rows 및 동사 retrieve/export/delete/bulk/submit/send 등으로 넓혀 합집합; 날짜 제한을 연도·월 단위로 나누어 검색 제한/누락을 기록. 그래도 API error면 공식 discussion UI에서 기간별 목록 수동 읽기, 순서가 보장되지 않으면 그대로 PARTIAL. 유사 사례로 빈 자리 메우지 않는다.
2. X05~X07 sandbox 직접 열기(정상 브라우저/공개 파일 접근). 원문의 초기 page/data/ID를 고정하고 원작성자 후속 또는 같은 예제의 literal ID를 대조; T01 #4873의 후속 literal ID는 opening body에 없어 부족 조건을 채우지 않음. 원작성자 실제 server request, handler logs 또는 export artifact가 공개된 자료만 receiver 근거로 승격. T10은 allIds server→client 보고, T13은 pagination fetch, T03 callback은 UI; 셋 다 batch 처리 수신 증거 아님.
3. **Codex 검증 후보**. 새 프로그램/벤치마크를 이 세션에서 실행하지 않음. 별도 승인/격리된 검증 환경에서 pinned worktrees로 기존 tests 먼저 식별:
```sh
git clone https://github.com/mui/mui-x.git mui-x-check
git -C mui-x-check checkout 50f9889d6ee1e45ce85a8728b10455ef3c327abd
git -C mui-x-check grep -n -E 'rowSelection.DataGridPro.test|test:unit' -- package.json packages/x-data-grid-pro
git -C mui-x-check show 883d1f82e249b977f72f083119c6ac014bed183e:packages/x-data-grid-pro/src/tests/rowSelection.DataGridPro.test.tsx
git clone https://github.com/TanStack/table.git tanstack-check
git -C tanstack-check checkout v8.5.15
git -C tanstack-check grep -n -E 'getRowId|toggleAllPageRowsSelected|getSelectedRowModel' -- packages/table-core/src
git -C tanstack-check show v8.8.4:packages/table-core/src/features/RowSelection.ts
```
   해당 판 package manager/lockfile 및 test script를 읽고 공식 설치/실행 방법 확인 후(승인된 환경에서만) D01 4 rows/size2/index1 expected size2; D02 50 rows, pageSize2, currencyPair contains usd, ID 0 → page next toggle → expected [0,3,4]; filter change [0,1,2,3]→[1] and keepNonExistentRowsSelected true alternate; D04 pinned 14df18549d1b547e7f88ac3f827d9cce68626b32 [0]→[0,2,3] expected. 정확 test command는 package scripts 확인 후 결정, 실행하지 않은 명령을 성공이라 표시하지 않는다.
   TanStack v8.5.15/v8.8.4 fixed input p1 [{id:"a"},{id:"b"}], p2 [{id:"c"},{id:"d"}]; default index vs getRowId:r=>r.id. Select a, change page, select c, deselect a. Record page rows, checked IDs, rowSelection (true only), getSelectedRowModel flatRows, onChange, outgoing payload, receiving mock actual IDs. Expect default index can select c on page flip; stable a persists in state, not loaded object. For F0=[a,b,c], all-except-b then insert d: snapshot processed [a,c], live processed [a,c,d]; receiver auth and deleted IDs/partial failures checked independently. Mock result only validates design fixture, never author incident. For QGIS use 3.44 project and layer with stable attribute feature IDs a-d; hide display vs provider filter, select expression, save selected output, compare attribute ID set, extent and output provider fid separate. Actual source data of G05/G06 not acquired. 
4. 독립 검토는 Q별 실제 반례·source location·count 확인. 부족한 자연 사건과 author ID trace 보완 전까지 PARTIAL 유지. 결과의 3개 약점과 반증 조건을 새 commit에 보존한다.
