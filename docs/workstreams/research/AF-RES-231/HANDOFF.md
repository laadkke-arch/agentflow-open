# AF-RES-231 HANDOFF — PARTIAL

## 상태와 고정점
- 착수 통합 SHA: 610bcdf35a3dc04bc7f55ce1ecf0a339d9d881e6. 47차 계획 914dbfa789ebec97063ed97130ea2a71c2e9f503 이후 +6 commits, dot-control만 변경; 231이 이후 추가되었고 220 result dependency 동일. 220 중앙 DONE, 자체 PARTIAL 보존.
- 고정 결과 SHA (HANDOFF 직전): b9a13af90bab17cb640305d6d24ec52d62c71b89. branch work/research-af-res-231.
- 모집 API frame/필터 원응답 모두 실패(웹 접근 불가, container curl DNS code6/HTTP000). 정상 빈 응답과 구별. 필터 토큰/원응답/has_more/실제 모집 분모 미확인. 예정 4사건/0배정, 8경로/0관측/8결측, 비교 가능 0/4쌍. 개선/동률/악화/수렴 수 미확인. A 원질문별 2–4단어 미봉인, B raw duplicate 대상 미확보. 원답 선택 미실행. 본표에 보조 사례를 끼워 넣지 않음.
- 원장 41행/29 별도 페이지 또는 스레드 work_id/13 lineage_id/12 미산입. 29는 공통 manual/API 문서의 각 절을 별도 자료로 세었으므로 엄격 독립 저작 22 충족 단정 금지. 실제 모집 질문 4의 분류 하한 미달. 보정 #138641 1, 보조 DBA 7, 스포츠 결과/보고 3 (2 독립 경기), PG 16 원문 5페이지, SE 공식 13페이지. PDF 규칙 텍스트 읽었지만 screenshot 실패·판 미확인으로 미산입. SQL 13통제 문서상 예측, 실행 0. 독립 검토 미실시.
- 대표 파일: RESULT.md(두 필수 표, Q1–Q7, 약점3), SCOPE.md(정정 포함), frame.csv, routes.csv, answers.csv, sources.jsonl, receipts/INDEX.json 및 ACCESS_FAILURES.txt, COUNTEREXAMPLES.md, comparison.md, controls.sql, control_predictions.csv, SELF_CHECK.md.
- 자체 고정 SHA 재조회: 필수/보강 13개 파일 모두 읽기 성공, JSONL 41행 parse, 29 work/13 lineage/12 미산입, 필수 원장 필드 존재. CSV frame 6행(예정4+summary+calibration), routes 8, answers 8, controls13; 각 헤더/행 열수 일치. RESULT 첫 표·두 번째 표·Q1–Q7·끝 약점 3행 확인, INDEX와 표의 0관측/8결측 일치. GitHub compare integration→result ahead6 behind0, 변경 13개 전부 owned_path, HANDOFF 아직 없음. 이 검사는 구조/일치 자체 점검이며 DB/API 실험이나 독립 검토가 아니다.
- 커밋 순서: ① c6bff08cebb19904693e5d2748979766f3d7ac39 범위; 사전 정정 8d068e444012d4e6adb6ba5052c8f30cfdcb8af4 (AND 모집, A OR 보정); ② 2acf700493d9f7d697d07222514523f4ddccdedc 원장·실패 영수증; ③ 6b7ea6e8bc503cc39647987bc98c5b1585865ec7 본표 결측; ④ dea42318ae82184060a83a003098bf6805f411a7 반례·통제; ⑤ b9a13af90bab17cb640305d6d24ec52d62c71b89 결과·자체 점검; ⑥ 이 HANDOFF 단독 커밋. 이 파일 자신의 commit SHA는 Git ref에서 읽는다.

## 다음 첫 행동 — 정상 공개 API 연결에서 filter와 모집 원응답 확보
API v2.3, site=dba. 기존 영수증을 덮어쓰지 말고 receipts/retry-<UTC>/ 아래에 보존. 아래 명령은 **재개용 미실행 명령**이며, 실제 실행 환경에서 DNS/HTTP 접근 허용 및 curl/jq 존재 확인 후 실행한다. 새 계정/키/유료 API 없음. 실패 시 exit/stderr/HTTP 원문을 남기고 중단. API backoff/quota 및 서비스 정책 준수. 아래 후보 필드는 생성 응답 included_fields로 직접 확인해야 하며 토큰을 추측하지 않는다. 필터 생성 성공이 모집 성공은 아니다.

```bash
git fetch origin work/research-af-res-231
git switch work/research-af-res-231
git rev-parse HEAD
P=docs/workstreams/research/AF-RES-231
R="$P/receipts/retry-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$R"
API=https://api.stackexchange.com/2.3
# no credentials; preserve original compressed-decoded response body and headers
req() {
  local n="$1"; shift
  date -u +%FT%TZ > "$R/$n.before.utc"
  curl --compressed --connect-timeout 15 --max-time 60 --fail-with-body -sS \
    -D "$R/$n.headers" -o "$R/$n.json" "$@" 2>"$R/$n.stderr"
  local rc=$?
  printf '%s\n' "$rc" > "$R/$n.exit"
  date -u +%FT%TZ > "$R/$n.after.utc"
  return "$rc"
}
W='.items;.has_more;.quota_max;.quota_remaining;.backoff;.error_id;.error_name;.error_message'
# Create named filters in sequence. Check returned included_fields and wrapper quota/backoff
# before each subsequent call; on backoff pause the prescribed seconds, on quota exhaustion stop.
mkfilter() {
  req "filter-$1" --get "$API/filters/create" \
    --data-urlencode 'base=none' --data-urlencode "include=$W;$2"
}
mkfilter frame 'question.question_id;question.creation_date;question.tags;question.title;question.link;question.closed_date;question.closed_reason;question.last_edit_date'
# inspect filter-frame.json; required fields must be included
jq -e '.items[0] | {filter,included_fields}' "$R/filter-frame.json"
F_FRAME=$(jq -er '.items[0].filter' "$R/filter-frame.json")
req frame-p1 --get "$API/questions" --data-urlencode 'site=dba' \
 --data-urlencode 'tagged=postgresql;greatest-n-per-group' \
 --data-urlencode 'fromdate=1325376000' --data-urlencode 'todate=1735689599' \
 --data-urlencode 'sort=creation' --data-urlencode 'order=asc' \
 --data-urlencode 'pagesize=100' --data-urlencode 'page=1' \
 --data-urlencode "filter=$F_FRAME"
jq '{has_more,backoff,quota_remaining,items:(.items|length)}' "$R/frame-p1.json"
# if has_more=true, after backoff and quota checks, same request page=2; keep raw whole page.
# If same creation_date at cap120 boundary, obtain complete boundary before cutting.
# Verify both tags; normalize by (creation_date,question_id) asc. Do not prefilter closed.
```

원응답 배열 원위치와 정규화 위치, 전체 실제 분모·excluded reasons·has_more를 frame.csv에 업데이트. 동일 생성시각 경계가 더 페이지를 요구하면 원 위치 보존 후 120개 평가 대상으로 제한. has_more=false 이전에 표본이 부족하면 공석 유지. 위 filter wrapper 필드가 API 문법/필드 검증에서 거절되면 공식 S04/S07의 include 표기와 실제 included_fields에 맞춰 수정 영수증을 별도로 남긴다. 요청 오류를 정상 결과로 해석하지 않는다.

다음 필터/진입점은 실제 표본 모집 후 순차 적용. 원질문 본문과 revision을 duplicate destination/answer 노출 전 분리하여 읽는다. 사전 열람 O00/C01–C07이 표본과 겹치면 기록하고 새 독립 판독자에게 질의 봉인을 맡긴다. 닫힘 사유 확인과 본문 적격성에만 기반해 최초 4개를 선정한다. 답 선택은 표집에 사용하지 않는다.

```bash
# create filters one at a time using mkfilter, check each token/included_fields.
mkfilter body 'question.question_id;question.creation_date;question.title;question.body;question.tags;question.last_edit_date;question.closed_date;question.closed_reason'
mkfilter rev 'revision.post_id;revision.revision_guid;revision.revision_number;revision.creation_date;revision.revision_type;revision.body;revision.last_body;revision.title;revision.last_title'
mkfilter duplicate 'question.question_id;question.closed_date;question.closed_reason;question.closed_details;closed_details.original_questions;original_question.question_id;original_question.title;original_question.accepted_answer_id'
mkfilter dest 'question.question_id;question.title;question.body;question.accepted_answer_id;question.creation_date;question.last_edit_date;question.link'
mkfilter ansmeta 'answer.answer_id;answer.question_id;answer.score;answer.is_accepted;answer.creation_date;answer.last_edit_date'
mkfilter ansbody 'answer.answer_id;answer.question_id;answer.body;answer.score;answer.is_accepted;answer.creation_date;answer.last_edit_date'
# inspect all filter receipts; set F_BODY F_REV F_DUP F_DEST F_META F_ANS from returned tokens.
# QID = selected original id; query only original body and revisions before seal:
req "origin-$QID" --get "$API/questions/$QID" --data-urlencode site=dba --data-urlencode "filter=$F_BODY"
req "revisions-$QID-p1" --get "$API/posts/$QID/revisions" --data-urlencode site=dba --data-urlencode pagesize=100 --data-urlencode page=1 --data-urlencode "filter=$F_REV"
# follow has_more if needed; first revision and current body differentiated.
# COMMIT original contract and 2–4 word A_QUERY before duplicate or search target exposure.
# A, per sealed QID and A_QUERY, fixed order AB/BA/AB/BA.
req "A-$QID-p1" --get "$API/search/advanced" --data-urlencode site=dba \
 --data-urlencode 'tagged=postgresql;greatest-n-per-group' --data-urlencode "q=$A_QUERY" \
 --data-urlencode sort=relevance --data-urlencode order=desc \
 --data-urlencode pagesize=5 --data-urlencode page=1 --data-urlencode "filter=$F_FRAME"
# /advanced tagged OR; preserve raw top5, then AND subset; pages increment until 5 both-tag
# items or has_more=false. No body reads. Log metadata cost; report strict server-AND absent.
# B, after seal, original_questions FIRST element in raw array, no resort:
req "B-$QID" --get "$API/questions/$QID" --data-urlencode site=dba --data-urlencode "filter=$F_DUP"
# DEST = chosen question ID (self exclusions and duplicate reuse logged).
req "destination-$DEST" --get "$API/questions/$DEST" --data-urlencode site=dba --data-urlencode "filter=$F_DEST"
# if accepted_answer_id exists, use it; else metadata-only answers, all pages if has_more:
req "answer-meta-$DEST-p1" --get "$API/questions/$DEST/answers" --data-urlencode site=dba \
 --data-urlencode pagesize=100 --data-urlencode page=1 --data-urlencode sort=votes --data-urlencode order=desc --data-urlencode "filter=$F_META"
# choose score DESC, creation_date ASC, answer_id ASC, preserving raw positions.
# AID = single selected answer. One body read only:
req "answer-$AID" --get "$API/answers/$AID" --data-urlencode site=dba --data-urlencode "filter=$F_ANS"
```

위 변수 QID/A_QUERY/DEST/AID 및 F_*는 실제 raw 값과 봉인 결과로 채울 것. 스크립트 예시를 그대로 일괄 실행하지 말고 각 요청의 quota/backoff/exit/field 검증 후 이어갈 것. 모든 실패/정상 빈 배열/동일 도착/자기/재게재를 분리하며, 각 경로 1질문+1답 외 본문 추가 열람은 본표와 분리. #138641 초기 source revision 판독과 실제 API original_questions 배열은 별도 보정. 스포츠 TR26 당시 시행판 및 Paris 공식 raw 결과 접근도 보강 가능.

## Codex 실행 인계 — SQL
PostgreSQL 16.0(정확한 서버판 server_version_num=160000) 설치되어 있고 실행 허용된 환경에서 먼저 `psql --version`, 접속 서버의 `SHOW server_version; SHOW server_version_num;`를 확인. 다른 minor는 별도 실험으로 표시. 신규 서비스 설치/권한 요청 없이 기존 승인된 테스트 DB만 사용. 정상 진입:
```bash
psql -X -v ON_ERROR_STOP=1 -f docs/workstreams/research/AF-RES-231/controls.sql > af231-sql.out 2> af231-sql.err
printf '%s\n' "$?"
```
임시 테이블/ROLLBACK, 두 그룹 6행의 정확한 입력은 파일에 있음. 예상 D0–M2 13개는 control_predictions.csv, 반전/계약은 COUNTEREXAMPLES.md. 특히 D2→D3 payload winner 변경, rank 공동1위, all-NULL B 그룹 배제/보존, independent aggregate의 nonexistent pair를 실제 비교. 실행된 exact 판/exit/stdout/stderr를 owned_path 내 receipt로 보존. 첫 답에 실제 SELECT가 확보되면 각 답의 그룹키/날짜/동률/NULL/열 계약을 별도 fixture로 적용하여 게시자의 실제 제시 결과와 문서 기대 및 실측을 구분.

## 중요 약점과 색인 제안
1. 원 API 모집/필터가 실패해 핵심 4쌍 효과 검정 자체 미실시. 정상 네트워크의 첫 filter/frame이 재개점.
2. advanced OR 및 보조 노출로 엄격 AND relevance와 가림을 보장 못함. raw/AND 부분수열과 비용 분리 및 독립 원문 판독 필요. 현재 duplicate는 과거 경로의 증거 아님.
3. tie/NULL 계약 미명시 및 actual answer SELECT/PG 실행/역사 경기 규칙 판 미확인. D2/D3, C03/C06, Tokyo/Paris 반례와 재실행 조건 보존.

통합 담당 색인에 제안: AF-RES-231 = PARTIAL / result b9a13af90bab17cb640305d6d24ec52d62c71b89 / handoff는 branch HEAD에서 확인 / 모집 API 접근 실패로 본표 0/4 및 0/8, 효과 미확인 / 공식 API AND-OR 정정, 13개 SQL 통제 예측, 공동 순위/점프오프 비교 / next=정상 API에서 filter→frame→원질문 계약 사전 봉인. dot-control.json은 수정하지 않았다.
