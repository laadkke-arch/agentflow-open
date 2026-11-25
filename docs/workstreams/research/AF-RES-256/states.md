# AF-RES-256 — 상태 대조 및 출판 모델 (규칙·기대, 새 실행 아님)

## 단위 및 전제
한 저장소의 일반 추적 파일 p의 내용(바이트; 모드, EOL/filter, sparse, submodule, 충돌 제외), 현재 HEAD의 p=H, index stage 0의 p=I, working tree p=W. H는 commit 자체가 아니라 그 파일 값이며 commit/ref 이동 여부는 별도 확인한다. A/B/C/D는 서로 다른 합성 내용, ∅는 해당 경로가 없음, ?는 증거 미확인(∅와 다름). `p`는 실제 한 경로 placeholder이고 `--`를 써서 branch/revision 해석을 피한다. 합성 4행을 SO 사례 파일이나 실제 실행으로 세지 않는다. 명령은 문서상 변환을 비교할 목적으로만 제시; destructive 작업 전에 `git status --short --untracked-files=all -- p`, `git diff -- p`, `git diff --cached -- p`로 확인하고 보존할 내용을 별도로 확보. HEAD 자체/다른 경로 변경 의도가 있으면 여기서 중단.

## 고정 2.45.0 변환
- Rw=`git restore --worktree -- p` 또는 `git restore -- p`: (H,I,W)→(H,I,I); source 기본 I.
- Ri=`git restore --staged -- p` 또는 `git reset HEAD -- p`: (H,I,W)→(H,H,W); source 기본 HEAD. 이전의 I를 복원하는 역연산이라는 뜻이 아님.
- Rhw=`git restore --source=HEAD --worktree -- p`: (H,I,W)→(H,I,H); HEAD 내용을 W에만. staged 변경이 I에 계속 남는다.
- Rboth=`git restore --source=HEAD --staged --worktree -- p`: (H,I,W)→(H,H,H); 둘 다 폐기. `git checkout HEAD -- p`도 같은 내용 변환(일반 파일 양쪽 존재 조건).
- `git checkout -- p`는 Rw에 대응. `git checkout <tree> -- p`는 일반 파일에서 source→I와 W 두 곳; restore의 `--source=<tree>` 단독은 source→W만. 따라서 목적지 선택은 원본 선택과 독립. H/I/W와 별도 source D를 넣으면 `git restore --source=T --worktree -- p`→(H,I,D), `--staged`→(H,D,W), 둘 다→(H,D,D); T는 D를 가진 commit. H(ref)는 이동하지 않는다. `git reset --hard <commit>`은 path 모드가 아니고 다른 파일 및 HEAD ref 이동까지 가능; 이 표의 p 한정 권고에 사용하지 않는다.

| 반례 | 시작 / status 예시 | Rw (I→W) | Ri (H→I) | Rhw (H→W) | Rboth (H→I,W) | 문서/시험 기대 및 잃는 값 |
|---|---|---|---|---|---|---|
| S1 H=I≠W | (A,A,C) / ` M p` | (A,A,A) | (A,A,C) | (A,A,A) | (A,A,A) | Rw/Rhw/Rboth 결과 내용 동일, C를 폐기. Ri는 no-op이므로 W 폐기 요청에 실패. Grestore DESCRIPTION/OPTIONS; T2022 L68–83 HEAD 복원 기대와 T2070 L30–35 기본 I 복원(후자는 H≠I일 수도 있음); T7102 L453–473 unmodified path no-op. |
| S2 H≠I=W | (A,B,B) / `M  p` | (A,B,B) | (A,A,B) | (A,B,A) | (A,A,A) | Rw는 no-op. Ri는 pending 변경만 빼고 W B 보존; Rhw는 W를 A로 바꿔도 staged B는 남음. Rboth는 B를 두 목적지에서 잃음. T2070 L66–74 staged HEAD, L76–85 both HEAD; T7102 L400–450 I만 초기화 후 W 별도 유지. |
| S3 H≠I≠W (세 값 모두 다름) | (A,B,C) / `MM p` | (A,B,B) | (A,A,C) | (A,B,A) | (A,A,A) | Rw는 C, Ri는 I의 B, Rhw는 C와 I/W 간 동일성, Rboth는 B와 C를 각각 잃는다. T2070 L37–64는 독립 source first/목적지 둘을 분리하는 공식 기대, 시작 세 값 동시 구분 fixture는 새 시험으로 남김. Ccheckout L622–647,1783–1801과 Creset L468–514. |
| S4 추적되지 않은 p, 동일 경로 과거판도 없음 | (∅,∅,U) / `?? p` | 경로 불일치 오류 예상, U 유지 | 범위 밖; I에 넣을 항목 없음, reset path는 no-op 가능; U 삭제 의도 아님 | 경로 불일치 오류 예상, U 유지 | 경로 불일치 오류 예상, U 유지 | Grestore L17–26 (추적 파일 복원), Ccheckout L572–595 pathspec match 오류, T2022 L23–44는 unrelated untracked next2 보존 기대, T7300 L212–227 dry-run U 유지. 실제 unmatched restore의 stderr/status는 미실행. `git clean -n -- p` preview만 조건부; clean 적용은 사용자가 명시적으로 삭제를 원하는 경우에만 별도 작업. |

S1에서 I와 H가 동일하면 'index 또는 HEAD 중 어디서 가져올까?'만 묻는다고 첫 절이 달라지지 않는다(동일 목적지일 때). 비용 이득 0. S2에서 동일한 W와 I 내용이어도 어떤 상태를 남겨야 하는지에 따라 I만 변경/Rboth 결과가 달라진다. S3에서 I=B를 남길 때도 W의 새 값이 B인지 A인지 질문할 수 있다. H≠I≠W 기호는 여기서 pairwise distinct로 썼지만 H=W≠I 상태도 실제 가능(예: S2에서 Rhw); 새 독립 모집 사례 아님.

### 반례와 철회 조건
1. stage 이전 스냅샷 I_old=B를 새 add가 C로 덮었다면 H=A, I=C, W=C이고 Ri→(A,A,C). 이는 I_old=B를 돌려주는 연산이 아니다. #348170 답변 [timeline](https://stackoverflow.com/posts/348234/timeline) L50–51,70에서 타인 leonbloy가 문제를 지적하고 Peter Schneider/iolsmit가 dangling object 검사 가능성을 제안. I_old가 object에 남아 있을 수 있으나 GC/정확한 object 식별/시간·파일 불명; 회수 성공 보장하지 않음. 사용자 목표가 commit 제외가 아닌 이전 staged snapshot이면 문서 경로를 철회하고 별도 회수 가능성 조사/변경 중지.
2. explicit source T에 추적 p가 없으면 restore 기본 no-overlay가 추적 p를 제거해 source를 맞춘다. checkout 기본 overlay와 다름. [restore OPTIONS L125–130](https://github.com/git/git/blob/v2.45.0/Documentation/git-restore.txt#L125-L130), [checkout OPTIONS L317–320](https://github.com/git/git/blob/v2.45.0/Documentation/git-checkout.txt#L317-L320), [T2022 L23–44](https://github.com/git/git/blob/v2.45.0/t/t2022-checkout-paths.sh#L23-L44). S4는 T에도 p가 없는 경우에 한정; 다른 T에 p가 있는 경우는 별도 충돌/overwrite 가능성(위 예측 적용 철회). `git reset --hard`는 추적 경로 쓰기를 방해하는 미추적 파일도 지울 수 있으나 일반 미추적 파일 청소 명령은 아님. [reset L71–75](https://github.com/git/git/blob/v2.45.0/Documentation/git-reset.txt#L71-L75).
3. Git 충돌에서 index는 다중 stage(1/2/3)일 수 있어 I 하나로 표현 못 한다. T2070 L87–110은 restore . 실패 및 ignore-unmerged로 공통 파일만 복원 기대; L141–159는 merge conflict 재구성. branch 전환/새 commit/`git revert`도 이 경로 복원 모델 밖. S4의 미추적/ignored 구분은 [status L189–201](https://github.com/git/git/blob/v2.45.0/Documentation/git-status.txt#L189-L201) 및 [clean OPTIONS](https://github.com/git/git/blob/v2.45.0/Documentation/git-clean.txt#L26-L77); -x, 전체 루트 clean 자동 권고 금지.

## 기존 공식 시험과 별도 검증
- [t2070-restore.sh](https://github.com/git/git/blob/v2.45.0/t/t2070-restore.sh#L30-L85): 명시 source의 W-only/I-only/both, staged default HEAD, both default HEAD. test_cmp/assert는 공식 기대이며 실행 영수증 아님.
- [t7102-reset.sh](https://github.com/git/git/blob/v2.45.0/t/t7102-reset.sh#L400-L473): 파일 p 하나 및 여러 경로의 staged/unstaged 비교, 영향 범위.
- [t2022-checkout-paths.sh](https://github.com/git/git/blob/v2.45.0/t/t2022-checkout-paths.sh#L23-L44), [t7300-clean.sh](https://github.com/git/git/blob/v2.45.0/t/t7300-clean.sh#L212-L244): untracked 보존, clean preview와 삭제 기대. 후자 setup은 clean.requireForce=no이므로 기본 설정으로 실제 실행과 동일하지 않음.
- [builtin/checkout.c](https://github.com/git/git/blob/v2.45.0/builtin/checkout.c#L1783-L1801) 목적지 기본값, source; [checkout.c L622–647](https://github.com/git/git/blob/v2.45.0/builtin/checkout.c#L622-L647) 조건부 index 갱신, [builtin/reset.c L468–514](https://github.com/git/git/blob/v2.45.0/builtin/reset.c#L468-L514) 경로 있으면 HEAD ref reset 하지 않는 조건. 정적 판독, 실제 CI 통과 확인 없음. 별도 4상태 x 4 명령 및 source D 독립 검증은 HANDOFF의 Codex 계획에 인계. 새 실행 0/예정 16+분기, 관측 0.

## 당시판과 현대판
| 사건 | 당시 공개된 기준판 | 당시 문서상 가능한 경로 | 현대 2.45.0 | 미확인 |
|---|---|---|---|---|
| #348170 2008-12-07 | Git 1.6.0 2008-08-17 발표, [reset L17–27](https://github.com/git/git/blob/v1.6.0/Documentation/git-reset.txt#L17-L27) | 기존 HEAD+추적 p: `git reset HEAD -- p` I만; 당시 unborn HEAD와 add 신규 경계는 별도 | reset 경로 절 또는 restore --staged | 실제 local 판/당시 파일 내용. 2013 댓글로 이전 commit 있었음만 확인 |
| #52704 2008-09-09 | Git 1.6.0, [checkout L25–32](https://github.com/git/git/blob/v1.6.0/Documentation/git-checkout.txt#L25-L32) | `git checkout -- p` I→W | `git restore --worktree -- p` | local 판, 동일 파일 staged+unstaged 여부 |
| #67673016 | ? | 미선택 | 미선택 | 날짜/판/원문 모두 미확인 |
| #14075581 2012-12-28 | Git 1.8.0 2012-10-21 발표, [reset L63–71](https://github.com/git/git/blob/v1.8.0/Documentation/git-reset.txt#L63-L71), [checkout L48–57](https://github.com/git/git/blob/v1.8.0/Documentation/git-checkout.txt#L48-L57) | 이미 reset --hard 했다는 진술. 상태 확인 후 추적 한 경로면 checkout HEAD -- p, 전체 추적 변경 폐기는 reset --hard HEAD(명시적 전체 요청 때만); 미추적 별도 | status 후 필요하면 restore 양쪽; clean preview만 조건부 | 파일 존재는 변경 여부를 말하지 않음, 실제 로컬 판/status 미확인 |

[Git v2.23.0 release notes L61–65](https://github.com/git/git/blob/v2.23.0/Documentation/RelNotes/2.23.0.txt#L61-L65)와 [2019-08-16 발표](https://github.blog/open-source/git/highlights-from-git-2-23/)로 restore/switch 도입 확인. [1.6.0 발표](https://lkml.iu.edu/0808.2/0481.html), [1.8.0 발표 원메일 보관](https://lwn.net/Articles/521075/), [2.45 발표](https://github.blog/open-source/git/highlights-from-git-2-45/). 단순히 당시 사용 가능했던 기준판이지 최신 patch/설치판은 확인 안 됨. 2008/2012 사건에 restore 명령을 소급하지 않는다. 2.45 docs L31도 experimental 표기를 유지. 

## 출판 분야 대조: WordPress
코드는 [wordpress-develop tag 6.8](https://github.com/WordPress/wordpress-develop/tree/6.8) 2025-04-15 고정판. 도움말 [Revisions](https://wordpress.org/documentation/article/revisions/)은 2026-09-28 편집판, 7.0+ 새로운 revision screen 및 6.9 이하 classic screen 분리. 공개 사이트 방문자, 편집 권한, 공개 저장된 리비전 레코드를 구분; 일반 독자가 내부 리비전을 공개 열람할 수 있다고 가정하지 않는다.

| 관점/시나리오 | 원본과 대상 | 무엇을 남기는가/새 판 | 첫 진입점 및 조건 |
|---|---|---|---|
| 출판자 P, published parent=B, 과거 R1=A, R2=B | R1의 허용 revisioned fields→동일 parent ID | title/content/excerpt 기본 복원, 기존 ID·post_status·post_author 자체는 기본 복원 필드가 아님. published 상태인 parent가 갱신되어 공개 내용 바뀔 수 있음. 변경이고 revisions enabled, hooks 정상일 때 새 revision A가 추가될 기대; 기존 R2 보존은 retention 한도 내. | 도움말 Restore a revision(7.0+), Classic Revisions(≤6.9); 6.8 admin route edit_post 권한+lock+nonce 및 disabled 조건. |
| 게시글 편집 중 브라우저 crash, published parent=B, 사용자 U autosave=C | (U,post_id)의 autosave C | autosave 때 published B 유지; 동일 U의 새 autosave D는 기존 C를 덮을 수 있고 별도 모든 시점 이력 아님. 명시 restore는 parent를 C로 갱신할 수 있음. | Autosaves, [REST L375–423](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/rest-api/endpoints/class-wp-rest-autosaves-controller.php#L375-L423); 다른 사용자의 autosave는 독립. |
| 기존 초안 B, 원저자 U, unlock, REST autosave C | 같은 post parent 자체→C | 별도 autosave revision 생성하지 않고 부모 초안 갱신. published content 경계와 다르며 B가 자동으로 history에 남는다고 보장 못 함. 6.8 일반 요청 DOING_AUTOSAVE=true로 save revision도 return. | 6.8 REST [L211–244](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/rest-api/endpoints/class-wp-rest-autosaves-controller.php#L211-L244); 다른 author/lock/draft status면 경로 다름. |
| 이미 동일한 content/title/excerpt restore, revision 제한 | source revision과 latest 동일 | 새 revision 0 가능, force-save filter 예외. 이전 history retention에 의해 사라질 수 있음. | [revision.php L130–229](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/revision.php#L130-L229), [tests L70–133](https://github.com/WordPress/wordpress-develop/blob/6.8/tests/phpunit/tests/post/revisions.php#L70-L133). |

원근거: [revision.php L22–55](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/revision.php#L22-L55) 기본 복원 필드/금지 필드; [L462–503](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/revision.php#L462-L503) parent ID로 wp_update_post 및 _edit_last; [default-filters.php L431–433](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-includes/default-filters.php#L431-L433) 업데이트 hook; [wp-admin/revision.php L36–83](https://github.com/WordPress/wordpress-develop/blob/6.8/src/wp-admin/revision.php#L36-L83) 권한, 잠금, nonce; [tests L27–64](https://github.com/WordPress/wordpress-develop/blob/6.8/tests/phpunit/tests/post/revisions.php#L27-L64) Author→Editor→Admin restore 후 _edit_last=Admin. 첫 시험이 restore 후 새 revision 개수를 직접 assert하지 않으므로 새 판 기대는 hooks+코드의 조건부 추론. 
문서 L151은 author도 변경 기록 대상으로 설명하나 6.8 core L41–45는 parent post_author를 기본 복원 필드에서 제외. 누가 편집했는지 revision metadata와 소유자 필드 복원은 다른 축. 단순 'HEAD=published, index=draft, W=autosave' 매핑은 틀림: draft 자체가 parent일 수 있고 사용자별 autosave 여러 개, 권한과 retention, restore가 부모 저장 및 조건부 새 revision을 만든다. Git은 ordinary path restore에서 새 commit을 만들지 않음. WordPress의 공개 여부/동일 ID/새 revision 여부라는 세 축이 필수.

실제 WP 실행·DB 영수증은 0. 코드/시험 기대와 도움말 판 차이를 분리했으며 사용자 현장과 동일하다고 주장하지 않는다.
