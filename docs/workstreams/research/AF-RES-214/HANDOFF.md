# AF-RES-214 HANDOFF

- **실제 상태: PARTIAL** — 조사 및 지정 산출물 커밋 완료, 핵심 결손은 최초 제안 시점의 정확한 부모판/지원 정책과 최종 consumer 배포. 24개 고유 자료 하한 충족(33 counted), 6개 지명 자리(4 runtime+2 controls) 전부 포함. 최초 링크→동일인 선택 변경→실제 후속 행동 완전 사슬 0/4 관측(효과가 없다는 증거 아님). 
- 작업 브랜치 `work/research-af-res-214`; 시작 SHA `87ffc1539bcf33da0fccf45eb15982a02d93e409` (기준 bb146773bbffba5e724e8c842951e2c25198c2da 대비 ahead 5/behind 0, dot-control만 변화). AF-RES-203 의존 HANDOFF `68dcbe0047d2c0653e39cafe65f98d541acb9eb0` 읽음. 중앙 DONE / 203 자체 PARTIAL 구별. 205–207 의존 없음.
- **마지막 결과 SHA**: `05dcea533081c8ac4d5be584ad4da3e98f80951f` (이 HANDOFF를 제외한 5번째 연구 묶음). [고정 결과 폴더](https://github.com/laadkke-arch/agentflow-open/tree/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/)
- 대표 파일: [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/RESULT.md), [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/sources.jsonl), [changes.csv](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/changes.csv), [decisions.csv](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/decisions.csv), [support.csv](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/support.csv), [COUNTEREXAMPLES.md](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/COUNTEREXAMPLES.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/05dcea533081c8ac4d5be584ad4da3e98f80951f/docs/workstreams/research/AF-RES-214/SELF_CHECK.md), SCOPE.md, frame.csv, CORE_NOTES.md.
- 연구 묶음 1 `f27ae7e69019bdaf066e1bf71bc3d190122e9803`, 2 `e6169a63127415e525ad13d1d4bb424a1d08e40e`, 3 `37b7bf891b0f047ec88ab602d9e7a9bf2b889003`, 4 `db475e2b782aa86e3fef43f181687413d1688939`, 5 `05dcea533081c8ac4d5be584ad4da3e98f80951f`. 이후 별도 마지막 HANDOFF 커밋.
- 결과 SHA 실제 재열람: 10/10 파일 반환, ledger 60 JSON parse 성공/60 unique IDs/33 counted 및 distinct counted work_id 33; RESULT 세 필수 표 정확한 헤더, 최종 약점 표 3행, 참조 source IDs 누락 0, changes/decisions 6개 자리 누락 0, support 15행(헤더 포함); R01/R03/T04 반례와 원장/RESULT 대조. 시작→결과 GitHub compare ahead5 behind0, 파일 10개 모두 허용 경로. dot-control 미변경. 작성자 자체 검토·형식 검사만 수행, 독립 검토 미실시.
- 자료 종류 실수/목표: PR 6/6; consumer fixed 12/8; vendor/spec 5/4; dated issue 6/3; transit 4/3. 60 rows 중 7 failed, 20 read but noncounted. 같은 본문/파일 revision/댓글/커밋 메타데이터 보수적 중복 제외. 다른 분야 WMATA 1개 복귀 사건, 4문서. 네 코드 제거는 HDS/BL(DIM과 별도)/DIM 세 보수적 consumer lineages; C2와 C4 same author, dependency, diff shape/chronology, 동일 decision/copy 직접 입증 아님.

## 핵심과 색인 반영 제안
- 원래 알던 표준 + 환경 조건이 달라져 fallback이 불필요한 사례. 네 body 지원 관련 사유, DIM만 정확한 정책·버전 전환 확인: 8.19.0 Chrome109/iOS16 floor, 8.19.1 removed. HDS 4.1.0 tagged manifest/changelog #1977. BL beta3→beta4, Jan31 RubyGems publish. C4 final deploy 미확인. 3/4 tag 확인, 1/4 registry 게시 기록, 0/4 production consumer rollout 직접 관측.
- D1 원 작성자의 문서 누락 인식은 실제 발견이지만 native choice discovery 아님; D2 bundled types는 runtime과 무관. Safari14 실험 flag/15.3 모달, slot focus, type error/rollback, 상반 회귀 보고가 'API 존재=행동 동등' 반례. WMATA 공사 대체버스→9/1 4역 재개와 aggregate 이용 보고는 접근 가능 조건/실제 선택 분리의 유추. 개별 행동 없음.
- 색인 제안(직접 수정 안 함): causal discovery/availability gate와 component retirement, dependency lineage, docs/types control, release/deploy distinction 태그. 결과 링크 및 partial 상태; 정책 및 first parent, actual deployment 미확인. 조건부 native-first 추천 link F13/F14, F01/P01, B04 및 반례 R01/R03/R02. 발생빈도·인시 절약률 추정 금지.
- 노출: brief가 표본과 결과 방향을 제공. diff 먼저 확인했으나 당시 최소 정책 파일을 동결하기 전 body 노출; 독립 blind 아님. API base는 original PR parent가 아닐 수 있음(C2 실제 base가 PR 생성 후). 정확한 제안 전 상태 판정에 이 결손 반영. 답변의 어떤 링크를 본 시점/개인 인지·비공개 토론 추정 금지. 공공교통 T01/T04 phase 날짜 표기 상충도 남김.

## 첫 재개 행동 / Codex 검증 항목 (아래 명령은 실행하지 않음)
**첫 행동**: 네 PR의 실제 최초 commit SHA와 parent/committed date를 저장하고 API base와 비교, 해당 부모의 native/fallback code 및 당시에 유효한 지원 정책을 동결한다. 특히 C2 2022-10-07 vs 2023-01-31 API base 차이와 C1 historical matrix 파일 위치. 외부 서비스 정책상 접근 실패 시 상태 그대로 유지한다.

```bash
# 공개 자료 read-only, gh 인증/도구가 이미 준비된 환경에서만; 새 유료 API/로그인 변경 없음
for pair in hashicorp/design-system:1977 projectblacklight/blacklight:2828 DestinyItemManager/DIM:10386 sul-dlss/vt-arclight:542 hashicorp/design-system:2212 DefinitelyTyped/DefinitelyTyped:53072; do
  r="${pair%:*}"; n="${pair##*:}"
  gh api --paginate "repos/$r/pulls/$n/commits" --jq '.[] | {sha,parents:[.parents[].sha],date:.commit.author.date,committer:.commit.committer.date}'
  gh api "repos/$r/pulls/$n" --jq '{created_at,merged_at,base:.base.sha,head:.head.sha,merge_commit_sha}'
done
# 각 upstream 로컬 read-only checkout에서, 앞 명령 첫 부모를 FIRST_PARENT에 기록
git show "$FIRST_PARENT:packages/components/src/components/hds/modal/index.js"
git ls-tree -r --name-only "$FIRST_PARENT" | grep -Ei 'browser|for.engineer|support|browserslist'
git log --all -S 'registerDialog' -- packages/components/src/components/hds
git log --all -S 'showModal' -- packages/components/src/components/hds
# C2/C3/C4 각 repo에서 대응 경로 바꾸어 같은 명령:
# lib/generators/blacklight/assets/importmap_generator.rb; app/javascript/blacklight/modal.js
# src/app/dim-ui/useDialog.tsx; package.json
# app/javascript/application.js; config/importmap.rb; Gemfile.lock
```
기대/반전: 최초 parent에 native-shaped code 있으면 prior-team-use 보강; 없고 새 링크가 먼저 제시된 뒤 같은 당사자가 실제 선택 변경하면 discovery 분류 변경. 이후 이슈/리뷰 날짜와 최초 링크 비교(댓글 API 날짜 null이면 공개 permalink 원문 보존). C1/C2/C4 당시 정책 날짜/지원판 없는 경우 그대로 unknown. 검색 실패를 하한에 산입하지 말 것.

```bash
# scratch, repository 밖 또는 owned_path 임시 자료만; 패키지 다운로드가 허용된 환경
npm view @hashicorp/design-system-components@4.1.0 version dist.integrity
npm view @hashicorp/design-system-components time --json
npm pack @hashicorp/design-system-components@4.1.0 --ignore-scripts
gem fetch blacklight -v 8.0.0.beta4
gem unpack blacklight-8.0.0.beta4.gem
grep -R -n 'dialog-polyfill\|registerDialog' blacklight-8.0.0.beta4
npm view @types/dialog-polyfill time --json
npm view @types/dialog-polyfill versions --json
# upstream tarballs: compare v0.5.1 vs 0.5.2 vs 0.5.3, verify root declarations without executing package scripts
npm pack dialog-polyfill@0.5.1 --ignore-scripts
npm pack dialog-polyfill@0.5.2 --ignore-scripts
npm pack dialog-polyfill@0.5.3 --ignore-scripts
tar -tf dialog-polyfill-0.5.2.tgz
tar -xOf dialog-polyfill-0.5.2.tgz package/index.d.ts
# deployment records (only if public/authorized)
gh api --paginate repos/sul-dlss/vt-arclight/deployments
gh api repos/DestinyItemManager/DIM/releases/tags/v8.19.1
```
기대/반전: tagged code와 published artifact 동일해야 release 포함 판정 강화. artifact에 pin/import/register 잔존 시 수정. production deploy SHA와 merge ancestry를 확인해야 actual rollout 표시; deployment 목록 없음은 배포가 없었다는 증거 아님. D1 prod docs release 별도 기록. DT stub 시점은 registry 실제 publish data로 확인. 

**행동 fixture(미실시)**: input HTML에 외부 focusable 버튼, native `<dialog>` 내부 form method=dialog, 첫/끝 focusable 요소, close 및 cancel listener, backdrop, slotted focusable element를 두고 (A native only / B v0.5.6 fallback JS+CSS / C experimental flag partial) 비교. Safari 14 flag on/off, Safari 15.3/15.4, Firefox 97/98, DIM 지원 floor iOS16/Chrome109와 현행판에서 browser/OS/flag를 정확히 기록. 실제 기존 browser를 구할 수 없다면 결과 대신 unknown. 1) 열기 전 activeElement→showModal 이후 focus; 2) Tab/Shift-Tab boundary; 3) background click inert; 4) Esc cancel 및 close event count/returnValue; 5) close 후 이전 focus 복구; 6) show() nonmodal background 정상 여부; 7) form method=dialog 제출; 8) slot/shadow focus; 9) CSS backdrop/stacking; 10) native feature detect + close/event mismatch. 기대: support matrix 충족한 native-only에서 해당 계약 모두 충족, 아니면 추천을 조건부 fallback/테스트된 대안으로 변경. v0.5.2 type fixture는 `import dialogPolyfill from 'dialog-polyfill'; const el = document.createElement('dialog'); dialogPolyfill.registerDialog(el);`을 각 실제 unpacked version+동일 tsconfig에서 `tsc --noEmit --strict --lib es2020,dom fixture.ts` (이미 설치된 tsc)로 비교, runtime import까지 별도. 
**교통**: T01 vs T04 phase cutoff의 정확한 Takoma restoration day를 당시 공식 service advisory/날짜별 운행 기록으로 확인. 이용자 동일인 행동 필요 시 별도 동의·적법한 공개 조사 설계; 집계로 인과/인시 환산하지 않음. 
추가 독립 검토는 RESULT 표/원장/source_id 맵을 별도 검토자에게 블라인드 재코딩해 disagreements 기록. 실험 및 명령 미실시, 자료 확인 자체와 구별.
