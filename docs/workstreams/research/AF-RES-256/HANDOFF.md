# AF-RES-256 HANDOFF

**작업자 자체 상태: PARTIAL.** 고정 결과 SHA: [fb0033829282ebf9f91e96772c094a6d0dca93e9](https://github.com/laadkke-arch/agentflow-open/commit/fb0033829282ebf9f91e96772c094a6d0dca93e9). 최종 인계 단독 커밋은 이 SHA의 다음 커밋(인계 파일 자체의 순환 SHA는 적지 않음). 통합 진행표에는 손대지 않았다.

## 읽는 순서
- [RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/RESULT.md): 두 필수 표, Q1–Q7, 대안·철회 조건 및 끝의 세 약점.
- [routes.csv](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/routes.csv): 네 지명 자리, 원판 GUID·표시시각, H/I/W 전후와 first section.
- [replies.csv](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/replies.csv): 30일 안/후 요약·작성자/답변자/타인 event.
- [states.md](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/states.md): 네 상태와 소스/목적지, 당시/현대, WordPress 출판자/편집자 비교.
- [sources.jsonl](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/sources.jsonl): 원근거·위치·한계와 접근 실패.
- [SCOPE.md](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/SCOPE.md), [SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/fb0033829282ebf9f91e96772c094a6d0dca93e9/docs/workstreams/research/AF-RES-256/SELF_CHECK.md): 입력 고정, 최초/복구 봉인, 자체 검토와 미달.

## 완료 및 미달
- 지명 원판 직접 확인 3/4 (#348170, #52704, #14075581), 미확인 #67673016. 첫 접근 실패 뒤 결측 4행을 먼저 봉인했으나 복구에는 현행 답변 선노출이 있어 가림 유효 0/4. 원판의 존재 자체와 가림 실험 성공을 혼동하지 않는다. 실제 최초판 raw UTC 초/owner ID와 설치 Git 판 미확인. 당시 2008년 v1.6.0/2012년 v1.8.0 문서와 2019년 v2.23.0 restore 도입을 분리, 최신 권고 2.45.0.
- 잠정 경로: #348170 pending index만 HEAD로, W 보존은 추론(후속으로 한 파일/이전 commit 명시). #52704 staged를 남기고 W만 I로 복원, 뒤의 타인 편집은 staged 맥락을 없앰. #14075581 이미 hard reset 시도 후 파일 존재 주장: status 확인 질문 우선, 추적/미추적/clean 구분 후 문서 절. #67673016 원판 없이 경로 선택하지 않음.
- 30일 이내 유지 0, 반전 0, 변수응답 미관측 3, 자료결측 1; 이후 유지 1(#348170), 반전 0, 변수응답 미관측 2, 자료결측 1. 두 댓글을 같은 사례로 집계. 채택 3은 별개. 전체 답변/숨은 댓글/삭제 댓글 전수 확인 및 동일인 감사-only·보존 반전 미확보. 실제 질문 전송/회신 실험 0, 성공률 N/A.
- 원장 68행(성공48/실패20), 고유 산입 25: 지명3/4 **미달**, 독립사건4/4, 매뉴얼·릴리스6/5, 시험·구현6/5, WP6/4. 총22 초과만으로 개별 하한을 대체하지 않음. 25 work_id/lineage_id 고유, 68 source_id 고유, 필드 누락0, 산입 실패0. 정확 호출횟수는 미집계(원장 행과 다름).
- 네 상태/4명령(16 기대 대조)와 독립 source D, WP 6.8 코드 대조는 규칙·공식 시험의 **기대**. 새 실행·빌드·독립 검토 0. WP 도움말은 현행(7.0+ 화면)이고 고정 6.8 코드는 비교 선택, 판 차이 명시. 정확한 모델 라우팅/Extra High 여부는 작업자가 확인할 수 없음.
- 결과 고정판에 대한 GitHub compare: base 2ff3a62fb0baf7fc874f65923a4a7ee56b06feae → fb0033829282ebf9f91e96772c094a6d0dca93e9, ahead12 behind0, 7파일 added, 모두 소유 경로. dot-control.json 변경 없음. 기존 필수 파일 및 원장 파싱·열 수 확인은 SELF_CHECK 참조. 최종 HANDOFF 추가 후 재검사 예정(인계 파일 자체 이후 쓰지 않음).

## 재개 첫 행동: 원판 결측과 사전 가림 복구
네 지명의 다른 답변이나 현행 본문을 보지 않은 독립 판독자를 별도로 배정할 것. 먼저 공개 원자료 [#67673016 revisions](https://stackoverflow.com/posts/67673016/revisions) 및 Stack Exchange API로 최초 revision title/body/GUID/creation_date/owner를 복구. 해당 접근이 실패하면 공개 Stack Exchange Data Explorer의 PostHistory(삭제 글은 없을 수 있음). 원본 결측을 유사 질문으로 채우지 않는다. 이 세션에서 API 접속 및 DNS 실패, 직접 revision/timeline/StackPrinter/검색 경유 실패 기록 있음. 아래 명령은 **미실행 인계**이며 네트워크 가능한 환경에서만 수행.

```sh
# 공개 API, 1페이지부터 has_more=false까지 순차 수집.
# 각 요청의 UTC 시각, headers, HTTP 상태, URL/필터, 원 JSON 및 sha256 보존.
for id in 67673016 348170 52704 14075581; do
  curl --fail --show-error --silent --get \
    -D "revision-$id-p1.headers" \
    -o "revision-$id-p1.json" \
    "https://api.stackexchange.com/2.3/posts/$id/revisions" \
    --data-urlencode 'site=stackoverflow' \
    --data-urlencode 'filter=withbody' \
    --data-urlencode 'pagesize=100' --data-urlencode 'page=1'
done
# jq로 has_more, backoff, quota 및 실제 field 확인; page 증가, backoff 존중.
# 필요한 필드가 없다면 공식 API filter 문서를 확인하여 필터 생성 후 재요청.
# 실패는 JSON/헤더·exit status에 기록. 임의로 원문을 복원하지 말 것.
```

SEDE에서 독립 확인할 공개 읽기 전용 질의(실제 실행 전 schema 확인):
```sql
SELECT PostId, PostHistoryTypeId, RevisionGUID, CreationDate, UserId, Text
FROM PostHistory
WHERE PostId IN (348170,52704,67673016,14075581)
  AND PostHistoryTypeId IN (1,2,3,4,5,6)
ORDER BY PostId, CreationDate, Id;
```
최초 title/body/태그 및 동일 revision의 GUID를 확인하고 후편집과 분리. 67673016이 dataset에도 없으면 삭제의 증거로 단정하지 말고 dataset version·커버리지/결측을 기록. 네 원판만 독립 판독자에게 제공, 현재 routes의 정답·후속을 차단하고 새 사전 CSV를 커밋. 그 뒤 질문/각 답변의 comments 및 timeline을 paginated API로 전수 조회, 동일인 raw user_id와 생성 epoch→UTC 확인. 질문 owner는 /questions/{ids}, 답 목록 /questions/{id}/answers, 원 댓글 /posts/{id}/comments, timeline /questions/{id}/timeline 공식 endpoint를 확인. 공개 API에 댓글이 존재하지 않는 경우 실제 미응답 확정 불가; 누락/삭제·pagination 한계 분리. 당시 Git 설치판은 원문에 명시된 값만. 유지/반전/감사-only/채택과 무응답·접근 실패를 별도 기록한다. 결과가 달라지면 새 판에서 표1/분모 수정하고 이전 판 보존.

## Codex 인계: 실제 시험은 아직 0건
아래는 승인된 **격리 시험 저장소/DB**에서만 실행할 명령·입력·기대값이다. 본 연구 저장소나 사용자 저장소, 실제 서비스에는 적용하지 말 것. 모든 raw receipt 및 후속 수정 파일은 연구 소유 경로 안에 두고 임의로 통합 진행표를 바꾸지 말 것.

### Git 2.45.0
```sh
# 임시 경로에서 고정 소스 확보 및 빌드(설치 의존성이 이미 승인된 환경).
git clone --depth 1 --branch v2.45.0 https://github.com/git/git.git /tmp/af256-git
cd /tmp/af256-git
git rev-parse HEAD
git describe --tags --exact-match
make -j2
./git --version
for t in t2070-restore.sh t7102-reset.sh t2022-checkout-paths.sh t7300-clean.sh; do
  (cd /tmp/af256-git/t && sh "./$t" -v)
  # 각 stdout/stderr/exit code를 별도 보존; 실패도 기록.
done
```
기존 시험 기대는 states.md의 exact line 참조. 다음 합성은 각각 새 임시 repo에서 독립 실행. GIT245=/tmp/af256-git/git 사용(실제 2.45.0 출력·tag SHA 확인), 별도 HOME/GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_SYSTEM=/dev/null, LC_ALL=C. 사용자/원 연구 repo에 명령 실행 금지. 각 셀마다 reset으로 되감지 말고 새 repo를 만드는 이유는 이전 stage·object·config 교란을 피하기 위해서다.

```sh
GIT245=/tmp/af256-git/git
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null LC_ALL=C
# 각 (scenario,action)에 새 tmp dir:
cd "$(mktemp -d)"
export HOME="$(mktemp -d)"
"$GIT245" init -q
"$GIT245" config user.name 'AF256 fixture'
"$GIT245" config user.email 'af256-fixture@example.invalid'
"$GIT245" config core.autocrlf false
printf 'A\n' > sentinel
# S1~S3는 p=A, S4는 p 없이 sentinel만 커밋한다.
# 선택된 경우에만 실행: printf 'A\n' > p
"$GIT245" add -- .
"$GIT245" commit -qm 'base'
# S1: printf 'C\n' > p
# S2: printf 'B\n' > p; "$GIT245" add -- p
# S3: printf 'B\n' > p; "$GIT245" add -- p; printf 'C\n' > p
# S4: printf 'U\n' > p
# 각 command 전후 동일하게 snapshot:
"$GIT245" rev-parse HEAD
"$GIT245" show HEAD:p
"$GIT245" show :p
cat p
"$GIT245" status --porcelain=v1 --untracked-files=all
# 정확히 하나 실행 후 exit code, stdout/stderr, 위 snapshot 반복:
# Rw:    "$GIT245" restore --worktree -- p
# Ri:    "$GIT245" restore --staged -- p
# Rhw:   "$GIT245" restore --source=HEAD --worktree -- p
# Rboth: "$GIT245" restore --source=HEAD --staged --worktree -- p
# 대조(새 repo): "$GIT245" reset HEAD -- p
# S4 별도 preview: "$GIT245" clean -n -- p
```
위 주석의 초기화/시나리오/명령을 셀별 실제 명령으로 선택하는 수동 템플릿이다. snapshot의 없는 경로 exit !=0은 정상 부재 후보이며 실패를 숨기지 말 것. 기대 행렬 (H,I,W): S1 (A,A,C)→Rw(A,A,A), Ri(A,A,C), Rhw(A,A,A), Rboth(A,A,A); S2 (A,B,B)→(A,B,B),(A,A,B),(A,B,A),(A,A,A); S3 (A,B,C)→(A,B,B),(A,A,C),(A,B,A),(A,A,A). S4 (∅,∅,U) pure untracked에서 U 보존, restore 경로 오류 예상·Ri/reset no-op 여부 실측 필요. preview 후 U가 남아야 함; 삭제 실행하지 않음. 모든 셀 HEAD commit ID와 sentinel 불변 기대. 바이트 SHA256·내용·existence 및 index stage를 기록하고 source D 대조는 최초 커밋 p=D → 두 번째 p=A → I=B/W=C로 만든 새 repo에서 `--source=HEAD^`와 worktree/staged/both 각각 실행하여 (A,B,D),(A,D,C),(A,D,D) 기대. source에서 p가 없는 별도 no-overlay 삭제 경계도 독립 fixture에서만 검증 가능.
반전 조건: 기대값 불일치, HEAD 이동, 다른 경로 변화, pure untracked U 삭제, prior staged 값 회수 보장 등 문서 주장과 실측 충돌. exit/status 경로가 예상과 다르면 결과를 그대로 기록 후 first-section 계약 수정. 원영수증 JSONL 필드: case/action, git tag SHA/version, env/config, UTC, cwd fixture ID(비밀 없음), argv, before/after HEAD ref와 path blob/존재/내용 SHA256/stage, status, stderr/stdout 원문 파일 및 hash, exit, expected, actual, match, deviation. 새 실행은 고유 원자료 수에 소급 합산하지 않음.

### WordPress 6.8
고정 소스 https://github.com/WordPress/wordpress-develop/tree/6.8 , [Tests_Post_Revisions](https://github.com/WordPress/wordpress-develop/blob/6.8/tests/phpunit/tests/post/revisions.php) 클래스 존재 확인. 승인된 disposable test DB와 해당 tag의 공식 개발 환경을 준비해야 한다(환경 설정/빌드 미실행).
```sh
git clone --depth 1 --branch 6.8 https://github.com/WordPress/wordpress-develop.git /tmp/af256-wp
cd /tmp/af256-wp
git rev-parse HEAD
# 공식 6.8 개발환경 준비 및 composer 의존성 확보 후, 테스트 DB만 연결:
vendor/bin/phpunit -c phpunit.xml.dist --filter Tests_Post_Revisions
# autosaves REST 관련 공식 시험 파일 경로/클래스는 고정판 목록 확인 후 선택.
# 별도 실행: 설치 완료된 6.8 disposable WP에서 아래 fixture.php를 wp eval-file로 실행.
wp --path=/tmp/af256-wp-install core version
wp --path=/tmp/af256-wp-install eval-file fixture.php publish
wp --path=/tmp/af256-wp-install eval-file fixture.php draft
wp --path=/tmp/af256-wp-install eval-file fixture.php restore
```
PHPUnit 및 WP-CLI/DB 설치와 config는 미확인 선행조건; 위 설치 경로는 지정 예시이며 실제 격리 경로 확인 후 대체한다. 사용 환경의 WP tag/core 버전, PHP, DB, hooks/plugins, WP_POST_REVISIONS 값을 기록. 각 모드는 새 프로세스·새 post(가능하면 fresh DB)에서 실행하며 DOING_AUTOSAVE의 전역 효과를 서로 공유하지 않게 한다. fixture.php 내용 제안(미실행):
```php
<?php
$mode = $args[0] ?? 'publish';
$uid = wp_insert_user(array('user_login'=>'af256_'.uniqid(),
    'user_pass'=>wp_generate_password(32), 'role'=>'administrator'));
if (is_wp_error($uid)) { throw new Exception($uid->get_error_message()); }
wp_set_current_user($uid);
$id = wp_insert_post(array('post_title'=>'A title','post_content'=>'A',
    'post_excerpt'=>'A excerpt','post_status'=>$mode==='draft'?'draft':'publish',
    'post_author'=>$uid,'post_type'=>'post'), true);
if (is_wp_error($id) || !$id) { throw new Exception('post insert failed'); }
function af256_snapshot($id) {
    $p = get_post($id);
    $r = array_values(wp_get_post_revisions($id, array('check_enabled'=>false)));
    return array('id'=>$p->ID,'status'=>$p->post_status,'author'=>$p->post_author,
        'title'=>$p->post_title,'content'=>$p->post_content,'excerpt'=>$p->post_excerpt,
        'revisions'=>array_map(function($x) {
            return array('id'=>$x->ID,'parent'=>$x->post_parent,
                'name'=>$x->post_name,'author'=>$x->post_author,
                'title'=>$x->post_title,'content'=>$x->post_content,
                'excerpt'=>$x->post_excerpt,'date_gmt'=>$x->post_date_gmt);
        },$r));
}
$before = af256_snapshot($id);
if ($mode === 'restore') {
    // 명시적으로 A의 revision을 확보하고 id 검증; 없으면 별도 실패.
    wp_save_post_revision($id);
    $r = array_values(wp_get_post_revisions($id));
    $target = 0;
    foreach ($r as $x) if ($x->post_content === 'A' && !wp_is_post_autosave($x->ID)) {
        $target=$x->ID; break;
    }
    if (!$target) throw new Exception('A revision missing; inspect configuration');
    wp_update_post(array('ID'=>$id,'post_title'=>'B title','post_content'=>'B',
        'post_excerpt'=>'B excerpt'), true);
    $before = af256_snapshot($id);
    $res = wp_restore_post_revision($target);
    $action=array('target'=>$target,'result'=>$res);
} else {
    $req = new WP_REST_Request('POST','/wp/v2/posts/'.$id.'/autosaves');
    $req->set_param('title','B title');
    $req->set_param('content','B');
    $req->set_param('excerpt','B excerpt');
    $res = rest_do_request($req);
    $action=array('status'=>$res->get_status(),'data'=>$res->get_data());
}
echo wp_json_encode(array('mode'=>$mode,'version'=>get_bloginfo('version'),
    'before'=>$before,'action'=>$action,'after'=>af256_snapshot($id)), JSON_PRETTY_PRINT);
```
기대: publish autosave 부모 내용 A/공개 상태 유지, per-author autosave B 별도; 잠금 없는 same-author draft는 부모 B로 갱신하고 일반 revision 추가 억제(비테스트 REST DOING_AUTOSAVE 경로 확인). restore A는 동일 부모 ID, 기존 status/author 유지 및 title/content/excerpt A 복원. revision 수는 설정·변경 여부·hook/retention에 조건부; count 자체를 실측. per-author autosave overwrite는 두 동일 author 호출과 다른 author를 사용한 독립 대조를 추가하고 각 parent 및 child ID를 비교. actual WP_RUN_CORE_TESTS 상수·DOING_AUTOSAVE 분기 확인. 코드/REST 응답/DB 행이 기대와 다르면 공개 경계 또는 새 판 생성 권고 철회. 원영수증: tag SHA, WP/PHP/DB/CLI version, config, UTC, 명령, input fixture sha256, stdout/stderr/exit, REST request/response 및 before/after parent·revision/autosave ID, author/status/fields/count, expected vs actual. 테스트 계정 비밀번호, DB 접속정보 등 비밀은 수집하지 말 것.

## 색인 제안 / 커밋 순서
색인: "Git path restore (H/I/W source vs destination, preserve masks), original-revision provenance, delayed author followup, WordPress published/draft autosave contrast; PARTIAL: missing #67673016 + contaminated blind seal". AF-RES-243은 선행 비교일 뿐 재조사하지 않았으며 242/251/254/255는 의존·입력에서 제외.
사전 범위 82dddda35c734fc50344850f91c8976229139ffd → 결측 봉인 c8985c51fdd120a9cc61b474deee0e5bd1050f27 → 복구 판정 63eeda7a3669470f71bc5136940db6bb675cacf1 → named/other ec743b6df538f1f12399275340a8128b22984a34 → Git 42c91a3d216c38bea2ee124f8cc6dbf6938e8eef → WP 0577aa77dca2c62fea682149540b797b173ba4ca → 보강 763f2cccfb5d776ea4db30934dc3466e94a95df0 → followup f790fafad7259f75ca71b1028ed93ccf520ed094 → scope addendum 378e85d421de33589f320f561773e1c56f24f445 → states 5339c44ffba35b8213cd1df28501113172d8cd8d → RESULT e5206e02dbe1e28de95011ffaa4b3fa4c6a62624 → SELF_CHECK fb0033829282ebf9f91e96772c094a6d0dca93e9 → HANDOFF 단독 커밋. 상태 판단을 DONE으로 상향하지 않는다.
