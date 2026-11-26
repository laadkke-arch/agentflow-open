# 04. 구조: 구성요소, 계약, 저장, 복구

이 장의 표와 SQL은 [db/](db/)의 실행 예제와 같은 이름을 쓴다. 실행 예제는 SQLite 한 파일에 공용 장부를 두고 프로젝트 장부를 `ATTACH`로 붙인다. 제품에서 어느 저장소를 쓸지는 이 설계가 정하지 않는다. 지켜야 할 것은 4절의 소유와 참조 방향이다. **[가정]** 공용 장부 하나와 프로젝트별 장부로 나누면 권한 경계가 저장소 경계와 같아진다.

## 1. 흐름 한 장

```
Studio ──요청판──▶ ① 접수 ──▶ ② 해석 ──▶ ③ 찾기(서랍 ‖ 새 검색 네 갈래) ──▶ ④ 확인(사용자 판의 줄·실행)
                                                                              │
                                    ⑦ 노출 ◀── 봉인 확인 ◀── ⑥ 조합(1~3자리) ◀─┘ ⑤ 관문(원리만)
                                                                 │
                   공용 장부: 관측·꼬리표·대비·대체·감시   ◀─쓰기─┤
                   프로젝트 장부: 해석·탐색 기록·쪽지·답·사용  ◀─쓰기─┘

배경 시계: ⑧ 수집 흐름(청구 없는 관측) · ⑨ 채널 ID 차분 ──▶ 재확인 작업 ──▶ ⑩ 재확인 작업자 ──▶ 대체 ──▶ ⑪ 전파(사용 쪽지) ──▶ 알림
기한 시계: ⑫ 공지 기한 T-24h·T ──▶ 재확인 작업(열린 작업에 합침)
```

## 2. 구성요소와 데이터 소유

| # | 구성요소 | 하는 일 | 읽는 것 | 쓰는 것 | 시계 |
| --- | --- | --- | --- | --- | --- |
| ① | 접수 | 요청판을 한 거래로 쓴다. 조건마다 출처 도장(명시·Studio·추론·나중)을 찍는다. 칸별 필요 문장과 봉인을 함께 쓴다 | Studio 입력 | `request_rev`, `requirement`, `context_fact`, `need`, `prior_seal` | 요청 |
| ② | 해석 | 해석이 갈리면 묻기 순서를 적용하고 0번 자리의 해석 줄을 만든다 | 요청판 | `interpretation` | 요청 |
| ③ | 찾기 | 서랍(칸끼리 맞춤)과 새 검색 네 갈래를 나란히 돌리고, 맞은 토큰·우연 적중·자격을 기록한다 | `tag_fts`, `need` | `search_run`, `search_hit` | 요청 |
| ④ | 확인 | 후보를 사용자의 판에서 열거나 실행한다. 같은 판·위치의 관측이 있으면 재사용 관문을 먼저 본다 | `observation`, `watch`, `channel` | `observation`, `sighting`, `receipt`, `tag`, `contrast`, `slip` | 요청 |
| ⑤ | 관문 | 원리 후보에 ①②③과 대상 1차 문서 우선을 적용한다 | 관측, 동종 기준선 | (결과는 자리나 접힌 목록) | 요청 |
| ⑥ | 조합 | 자리 규칙대로 1~3자리를 만들고, 답·자리·사용 쪽지·접힌 목록을 한 거래로 쓴다 | 쪽지, 관측 | `answer_run`, `answer_slot`, `usage`, `folded` | 요청 |
| ⑦ | 노출 | 봉인이 있을 때만 노출을 기록한다 | `prior_seal` | `exposure` | 요청 |
| ⑧ | 수집 흐름 | 이미 읽는 소식 흐름에서 처음 본 작은 기능을 추가 열람 없이 관측과 꼬리표로 남긴다 | 소식 흐름 | `observation(via=collection)`, `tag` | 배경 |
| ⑨ | 채널 | 공급자 변경 채널을 외부 ID 집합의 차분으로 읽는다. 감시 키에 닿으면 재확인 작업을 만든다 | `channel`, `watch` | `channel_item`, `recheck_job` | 배경 |
| ⑩ | 재확인 작업자 | 작업을 임차하고 그 위치만 다시 읽는다. 바뀌면 새 관측과 대체를, 같으면 다시 본 기록을 쓴다 | `recheck_job` | `observation`, `supersession`, `sighting` | 후속 |
| ⑪ | 전파 | 대체가 생기면 사용 쪽지를 따라 인용한 자리에만 알림을 만든다. 대조 인용은 제외한다 | `supersession`, `usage` | `notice` | 후속 |
| ⑫ | 기한 | 감시의 공지 기한 24시간 전과 기한에 직접 읽는 작업을 만든다 | `watch.deadline` | `recheck_job` | 후속 |
| ⑬ | 재생 | 지난 답을 당시 문장과 인용 관측 그대로 연다. 알림은 따로 붙인다 | 답, 알림 | (없음) | 요청 |
| ⑭ | 감사 | 분기마다 관측 표본을 직접 다시 읽는다. "감시 없음" 관측은 두 배로 뽑는다 | 관측 | `sighting(via=audit)`, 대체 | 배경 |

### 2.1 데이터 소유와 참조 방향

| 장부 | 무엇에 대해 말하나 | 표 | 누가 읽나 |
| --- | --- | --- | --- |
| 공용 | 원문 | `locator`, `locator_alias`, `locator_alias_cancel`, `edition`, `receipt`, `observation`, `sighting`, `tag`/`tag_fts`, `contrast`, `supersession`, `channel`, `channel_item`, `watch`, `recheck_job` | 모든 프로젝트 |
| 프로젝트 | 사용자의 필요 | `request_rev`, `requirement`, `context_fact`, `prior_seal`, `need`, `interpretation`, `search_run`, `search_hit`, `slip`, `answer_run`, `answer_slot`, `usage`, `folded`, `notice`, `exposure` | 그 프로젝트만 |

규칙은 넷이다.

1. 공용 장부는 프로젝트 장부를 참조하지 않는다.
2. 프로젝트 장부는 공용 ID(`obs_id`)를 값으로만 든다. 외래 키로 묶지 않는다.
3. 공용 꼬리표와 관측 문장에는 원문 쪽 말만 쓴다. 어느 요청에만 나오는 다섯 글자 이상 내용어가 둘 이상 들어가면 쓰기를 거절한다(`PrivacyError`).
4. 확정 기록은 덧붙이기만 한다. 관측·판·영수증·대체·꼬리표·요청판·쪽지·답 자리는 트리거로 수정과 삭제를 막는다. 고침은 새 행(대체, 취소, 새 쪽지)이다.

## 3. 입출력 계약

### 3.1 Studio에서 접수로

R1을 예로 든다. 요청 원문은 012 P03.w 한국어판이다([queries.jsonl L31][q012]). 판·환경·상태는 Studio가 채우고 출처를 단다.

```json
{
  "request_key": "R1", "rev": 1, "received_at": "2026-11-26T01:00:00Z",
  "text": "목표: 이미지 변환보다 저장 단계가 느려도 대기 작업과 동시 작업 수가 계속 늘어나지 않게 하고 싶다. …",
  "selected_part": "파이프라인: 작업 투입·완료 신호",
  "requirements": [
    {"code": "H1", "kind": "must", "text": "대기 큐 안의 항목 수는 최대 8개이고 처리 중 작업은 최대 4개여야 한다."},
    {"code": "H2", "kind": "must_not", "text": "sink가 느려지면 producer가 기다려야 하며, 모든 입력에 대해 task를 미리 만들거나 …"},
    {"code": "H3", "kind": "must", "text": "처리 완료/용량 회복을 투입 재개의 근거로 삼고 …"},
    {"code": "S1", "kind": "must", "text": "입력이 끝났음을 일꾼에게 알린다", "provenance": "inferred"},
    {"code": "X",  "kind": "out_of_scope", "text": "전체 RAM byte 상한, … 장애 복구"}
  ],
  "context": {
    "runtime":        {"value": "CPython 3.13", "provenance": "studio", "source": "프로젝트 실행 환경 설정"},
    "workers_fixed":  {"value": "yes", "provenance": "studio", "source": "선택 부분의 일꾼 생성 코드"},
    "producer_pausable": {"value": "yes", "provenance": "explicit"}
  },
  "prior": {"state": "given", "known": []},
  "needs": [
    {"slot": "input",  "lang": "en", "text": "a lazy input iterator that the producer can pause"},
    {"slot": "keeps",  "lang": "en", "text": "at most eight items wait in the queue and at most four jobs run at once"},
    {"slot": "breaks_when", "lang": "en", "text": "…"}, {"slot": "output", "lang": "en", "text": "…"}, {"slot": "summary", "lang": "en", "text": "…"}
  ]
}
```

- `prior`는 결과를 보이기 전에 사용자가 이미 고려한 대안이다. 적었으면 `given`, 적기를 거절했으면 `declined`, 적을 것이 없으면 `none`이다. 이 행이 없으면 노출을 쓸 수 없다(3.7절).
- `needs`는 접수가 요청을 꼬리표와 같은 칸으로 나눈 문장이다. 비공개다. **[가정]** 접수가 이 문장을 쓸 수 있다. 세 사례에서는 손으로 썼다.
- 같은 `(request_key, rev)`에 같은 내용을 다시 보내면 같은 `req_id`가 온다. 다른 내용이면 거절하고 새 판을 요구한다.

### 3.2 답

```json
{
  "run_id": 1, "req_id": 1, "produced_at": "2026-11-26T01:00:00Z",
  "status": "complete",
  "budget": {"opens": 8, "fresh_results": 5},
  "next_action": null,
  "slots": [
    {"no": 0, "kind": "check", "ladder": "L5",
     "sentence": "해석: '처리 중 4'를 동시에 실행 중인 작업 수로, '대기 8'을 아직 꺼내지 않은 항목 수로 읽었습니다.",
     "hold": "해석이 다르면 알려 주세요"},
    {"no": 1, "kind": "direct", "ladder": "L4",
     "sentence": "투입·완료 신호를 따로 만들 필요가 없습니다. … 첫 원문: https://github.com/python/cpython/blob/v3.13.18/Lib/asyncio/queues.py#L36-L38 …",
     "cites": [{"obs": 157, "part": "first_link"}, {"obs": 158, "part": "support"}, {"obs": 161, "part": "support"}],
     "hold": "런타임이 3.13보다 낮으면 끝 신호 부분을 끝 표지로 바꾸고, 일꾼을 항목마다 만들게 되면 이 자리를 철회합니다"}
  ],
  "folded": [{"url": "…/locks.py#L355-L358", "condition": "대기 8을 대기열 길이로 지키는가", "reason": "…(H1 U)"}, "…"]
}
```

자리 문장은 고정된 틀로 만든다(`Ledger.sentence`). 순서는 동사, 첫 원문(고정판 링크와 위치), 이유(조건 ID별), 실행 결과, 근거 수준 문장, 함께 필요한 것, 철회 조건이다. 원리 자리는 빌릴 것, 대상에서 다시 확인할 것, 깨지는 입력을 더한다. 확인할 후보 자리는 먼저 열 원문, 확인할 한 가지, 보류를 쓴다.

답 상태는 여섯이고 서로 다르다.

| 상태 | 뜻 | 다음 행동 문장 |
| --- | --- | --- |
| complete | 모든 필수 조건을 L2 이상으로 채운 1번 자리가 있다 | 없어도 된다 |
| partial | 자리는 있지만 1번 자리 하한을 못 채웠거나 확인할 후보만 있다 | 필수 |
| none_verified | 검증된 후보가 없다 | 필수. 첫 확인 항목을 적는다 |
| budget_exhausted | 예산 안에서 끝내지 못했다 | 필수. 무엇이 남았나 |
| source_unreachable | 원문에 닿지 못했다 | 필수. 어느 주소가 어떻게 실패했나 |
| none_in_scope | 범위 안의 후보가 없다 | 필수. 범위 밖에 무엇이 있었나 |

### 3.3 알림과 재생

알림은 `{slot, effect, text}`다. 효과는 셋이다. `invalidates`는 "근거 무효", `changes_value`는 "값 바뀜", `confirms`는 "다시 확인됨"이다. 문장은 새 관측의 원문 쪽 한 줄과 알게 된 시각이다. 예: "근거 무효: 저장 종료, 기존 내보내기는 계속(내보내기 전용). 종료와 내보내기 전용 모드가 분리된다. (알게 된 시각 2025-07-09T00:00:00Z)". 사용자 쪽 사실이 바뀌어 지난 답이 대체될 때는 요청판 번호를 붙인 알림을 쓴다. 예: "요청판 2: 배포 런타임이 3.12로 바뀌어 끝 신호 부분(shutdown)이 성립하지 않는다. 대기열·일꾼 부분은 같은 문장이라 유지."

재생(`replay(run_id, at)`)은 당시 상태·자리 문장·인용 관측·접힌 목록·대조 인용을 그대로 돌려준다. `at`까지의 알림만 붙인다. 현재 답이 필요하면 새 요청판으로 다시 조합한다. 재생은 현재 판정을 섞지 않는다.

### 3.4 근거 수준 사다리

| 단계 | 자리에 붙는 고정 문장 | 쓰이는 곳 |
| --- | --- | --- |
| L0 | 목록에 있다는 것만 확인했다 | 확인할 후보(EVAL-X1 T0의 Pocket) |
| L1 | 소개 글이나 언급만 보았다 | 확인할 후보(R2의 ii-svn-log) |
| L2 | 이 판의 원문 줄에서 방법을 확인했다 | 1번 자리 하한. 원리 자리의 상한 |
| L3 | 공개 산출물에서 그 값을 확인했다 | 결과 값을 보여 주는 예제가 목표일 때 |
| L4 | 이 판에서 실행해 값을 확인했다 | R1 직접 자리 |
| L5 | 사용자 맥락에서 확인해야 한다 | 해석 줄. 사용자 환경에서만 판정되는 조건 |

설명으로 수준을 부풀리지 않는다. 058에서 설명을 덧붙이자 틀린 권고 수락이 123/205에서 152/205로 늘었다([058 L40–48][r058], a).

### 3.5 자리 규칙

1. 0번 자리는 해석 줄이다. 해석이 하나로 정해져도 쓴다.
2. 1번 자리는 모든 필수 조건을 L2 이상으로 채워야 한다. 못 채우면 상태는 partial이고 후보는 "확인할 후보"로 내려간다.
3. 2번 자리는 둘 중 하나일 때만 연다. 첫 절이 다른 두 해석이 남았을 때, 또는 필수 묶음 요소가 자기 첫 링크를 가질 때다.
4. 3번 자리는 관문을 통과한 원리다. 원리 자리의 근거 수준은 L2를 넘지 않는다.
5. 범위 밖 실패 시험은 자리가 아니라 접힌 목록으로 간다. R1에서 카드 분실 시험은 "장애 복구가 범위에 들어오면 이 시험부터 연다"로 접혔다.
6. 근접 대안은 지우지 않고 갈린 조건과 함께 접는다.
7. 확인할 후보 자리도 그 요청의 탐색 기록에 있는 이름만 쓴다. 모델 기억에서만 나온 이름은 쓰지 않는다(`compose`가 거절한다).

### 3.6 묻기 순서

`Ledger.decide(a, b, …)`는 두 해석의 첫 절과 다섯 판별 값을 받아 하나를 돌려준다.

| 순서 | 조건 | 결정 | 사례 |
| --- | --- | --- | --- |
| 1 | 두 해석의 첫 절이 같다 | proceed | R1(두 해석 모두 Queue(8)+고정 일꾼 4) |
| 2 | 0단계: 요청판의 다른 명시 칸이 정한다 | reread. 골라서 첫 줄에 밝힌다 | EVAL-X1 T0(R2·R3·선호 칸이 읽기 API 가져오기를 정함) |
| 3 | 1단계: 두 뜻을 함께 채우는 공통 행동이 있다 | common | R2(읽기 전용으로 넘기고 지문 목록을 따로 보관) |
| 4 | Studio에서 회수할 수 있다 | fetch | |
| 5 | 실행으로 판정된다 | verify | |
| 6 | 되돌릴 수 없다 | ask_once. 한 번만 묻는다 | |
| 7 | 그 밖 | conditional. 조건부 두 링크 | |

근거는 026(물을 값이 이미 요청판에 있던 경우 8/24)과 144의 C4·Y2다([sections/request_utility.md 4절](sections/request_utility.md)).

### 3.7 오류 계약

| 상황 | 동작 |
| --- | --- |
| 같은 요청판 번호에 다른 내용 | 거절. 새 판을 요구한다 |
| 공개 꼬리표에 요청에만 있는 말 | `PrivacyError`. 꼬리표를 원문 쪽 말로 다시 쓴다 |
| 확인할 후보의 주소가 탐색 기록에 없음 | 조합 거절 |
| 봉인 없이 노출 | 거절("봉인 전에는 노출하지 않는다") |
| 확정 기록 수정·삭제 | 트리거가 막는다. 대체·취소·새 쪽지로 쓴다 |
| 같은 답 재전송 | 같은 `run_id`(멱등 키) |

## 4. 저장과 조회 예

아래 SQL은 실행 예제의 스키마([db/schema.sql](db/schema.sql), [db/project_schema.sql](db/project_schema.sql))에서 그대로 돈다. `p_A`는 프로젝트 A 장부의 별칭이다.

**같은 판·같은 위치의 관측이 있나.** 다른 프로젝트, 다른 요청이 같은 줄을 다시 판독하지 않게 하는 조회다(`Ledger.reusable`).

```sql
SELECT o.obs_id
FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)
WHERE l.url = 'https://github.com/python/cpython/blob/main/Lib/asyncio/queues.py'  -- 위치는 파일 주소
  AND e.edition_key = 'v3.13.18' AND o.position = 'L36–38'                        -- 판은 태그
ORDER BY o.obs_id DESC LIMIT 1;
-- 사례 실행에서 157. 3.12.3으로 물으면 행이 없다. 판이 다르면 그 판의 같은 위치를 다시 연다.
-- 답의 첫 링크는 판을 넣어 다시 만든다(…/blob/v3.13.18/…#L36-L38).
```

**서랍: 필요 문장 한 칸과 꼬리표를 맞춘다.** 칸이 같거나 summary인 꼬리표만 본다. 그 시각 이전에 관측된 것만 본다.

```sql
SELECT t.obs_id, t.slot, t.text, bm25(tag_fts) AS score
FROM tag_fts JOIN tag t ON t.tag_id = tag_fts.rowid JOIN observation o ON o.obs_id = t.obs_id
WHERE tag_fts MATCH '"tool" OR "exported" OR "file" OR "standalone" OR "pc"'
  AND o.observed_at <= '2027-03-02T00:00:00Z'
  AND (t.slot = 'user_without' OR t.slot = 'summary');
```

엔진은 칸별 결과를 관측별로 모은다. 맞은 토큰이 기능어·숫자뿐이면 우연 적중으로 표시한다. 두 칸 이상, 서로 다른 내용어 둘 이상이 맞아야 자격이 있다. 결과는 `search_hit`에 `matched_tokens`, `lexical_accident`, `eligible`과 함께 남는다.

**그날 알던 것.** 사용자가 "10월 9일에 알던 기한"을 물을 때다(`Ledger.known_on`).

```sql
SELECT o.statement, e.edition_key, o.observed_at
FROM observation o JOIN edition e USING(edition_id) JOIN locator l USING(locator_id)
WHERE l.url = 'https://support.mozilla.org/en-US/kb/future-of-pocket'
  AND o.observed_at <= '2025-10-09T23:59:59Z'
ORDER BY o.observed_at DESC, o.obs_id DESC LIMIT 1;
-- → "같은 안내의 내보내기 기한이 11월 6일로 갱신됐다." (rev:308355, 관측 2025-10-09T00:00:00Z)
```

**철회가 닿는 자리.** 대체 사슬의 어느 고리를 인용했어도 닿는다. 대조 인용은 빼고, 대체를 알기 전에 만든 답만 고른다(`Ledger.propagate`).

```sql
SELECT DISTINCT u.run_id, u.slot_no
FROM p_X.usage u JOIN p_X.answer_run r USING(run_id)
WHERE u.obs_id IN (/* 대체 사슬의 조상 관측들 */ 171)
  AND u.part <> 'contrast'
  AND r.produced_at <= '2025-07-09T00:00:00Z';
-- EVAL-X1 E2: (1, 1)만 나온다. 원리 자리 (1, 2)는 Pocket 관측을 contrast로만 인용했다.
```

**재확인 작업 합치기.** 같은 관측에 열린 작업이 있으면 새 작업을 만들지 않고 원인을 덧붙인다(`Ledger._enqueue`).

```sql
UPDATE recheck_job
SET merged_causes = merged_causes || ',deadline:2025-07-08T00:00:00Z#T'
WHERE obs_id = :obs AND state IN ('queued','leased');
```

**탐색 경로.** 서랍만, 새 검색만, 둘 다(`Ledger.path_log`). 이 집계가 7절의 줄이는 규칙의 입력이다.

```sql
SELECT r.path, h.url FROM p_B.search_hit h JOIN p_B.search_run r USING(search_id)
WHERE r.req_id = :req AND (r.path = 'fresh' OR (h.eligible = 1 AND h.lexical_accident = 0));
```

## 5. 세 시계와 예산

| 시계 | 하는 일 | 사는 목표 | 예산 [가정] | 근거 |
| --- | --- | --- | --- | --- |
| 요청 | 접수, 해석, 찾기, 확인, 조합 | 요청 지연 | 요청 하나에 원문 열람 4회 이하. 재사용 관문을 통과한 관측은 0회 | 072 요청당 4회, 152 S의 캐시 답 278/364 |
| 후속 | 채널 항목과 공지 기한마다 그 위치만 다시 읽기, 전파 | 신선도 | 168시간마다 3회 예약(98,304 B·90초). 채널 항목·기한마다 원문 1회. 남으면 요청 시계로 | 152 S 후속 26주 7~11회 |
| 배경 | 채널 ID 차분, 수집 흐름, 감사 | 희귀 발견 | 출처당 72시간마다 통지 1회. 희소·무인용 출처는 168시간. 감사 분기 32건 | 152 S·F 설정, 015 기준율 |

- **원문 열람과 위치를 따로 센다.** 사례 A의 첫 요청은 새 관측 8개를 남겼다. 원문 두 파일(`queues.py`, `locks.py`)의 네 위치와, 한 번 실행한 영수증의 네 경우다. 원문 열람으로는 2회와 실행 1회다.
- **152의 잰 배분(b).** S 높은 예산·주류 26주에서 요청 횟수로 배경 66%, 후속 3%, 요청 31%였다. 바이트로는 42%, 5%, 53%였다.
- **희귀 발견은 표시일 창을 쓰지 않는다.** P가 놓친 CF-2026-01이 표시일 창 때문이었다.

## 6. 변경, 실패, 복구

### 6.1 동시 변경

| 경우 | 처리 | 확인 |
| --- | --- | --- |
| 작업자 둘이 같은 재확인을 잡는다 | `lease`가 `state='queued'`인 행만 `leased`로 바꾼다. 둘째는 실패한다. 임차가 끝나면 `release_expired`가 되돌린다 | `test_lease_prevents_double_work_and_expires` |
| 채널 항목과 공지 기한이 같은 날 같은 관측을 가리킨다 | 열린 작업에 원인을 합친다. 작업은 하나다 | `test_deadline_job_merges_with_channel_item_and_does_not_invalidate`. EVAL-X1 E2·E3·E5 |
| 두 요청이 같은 위치를 동시에 읽는다 | 관측의 멱등 키가 (판, 위치, 결과, 인용 지문, 방법, 영수증)이다. 둘째는 다시 본 기록이 된다 | `test_same_content_is_a_sighting_other_edition_is_new` |
| 답을 쓰는 도중 실패 | 답·자리·사용 쪽지·접힌 목록을 한 거래로 쓴다. 반쯤 쓴 답은 없다 | `test_compose_is_atomic_and_idempotent` |
| 같은 요청판을 두 번 보낸다 | 같은 내용이면 같은 `req_id`. 다른 내용이면 거절 | `test_intake_retry_and_conflict` |

### 6.2 재시도

모든 쓰기에 멱등 키가 있다. 관측은 내용 지문, 영수증은 (런타임, 프로그램 지문, 입력, 출력), 답은 (요청판, 자리·접힌 목록·상태·다음 행동·해석)의 지문이다. 재시도는 같은 행을 돌려준다. 재확인 작업은 `attempts`를 세고, 원문 실패는 `outcome`(not_found, unreachable, unsupported, truncated)으로 관측에 남긴다. 실패도 관측이다. 같은 실패가 세 번 이어지면 그 관측을 인용한 자리에 "원문 접근 실패" 알림을 만든다. **[가정, 실행 예제에 없음]** 이 동작과 세 번이라는 값은 152의 재시도 구성(4시간에 2회 한도, 429, 2시간 대기)을 보고 정했고, 제품에서 재지 않았다.

### 6.3 오병합과 분리

전역 병합을 하지 않으므로 "같은 것으로 잘못 합친" 상태가 공용 관측에 생기지 않는다. 오류가 생길 수 있는 곳은 셋이다.

| 오류 | 복구 |
| --- | --- |
| 잘못 붙인 주소 별칭 | 취소 행(`locator_alias_cancel`)을 쓴다. `resolve`는 취소된 별칭을 따라가지 않는다(`test_cancelled_alias_is_not_followed`). 별칭을 따라 만든 답 자리는 사용 쪽지로 찾아 알린다 |
| 다른 판을 같은 판으로 기록 | 판 키가 다르면 다른 관측이다. 같은 키로 잘못 기록했으면 바른 판의 새 관측과 대체(`invalidates`)를 쓴다. 앞 관측은 남는다 |
| 잘못된 대체 | 대체는 수정할 수 없다. 반대 방향의 새 관측과 `confirms` 대체로 되돌린다. 알림이 두 번 간다. "근거 무효" 뒤에 "다시 확인됨"이다 |

**분리 쪽 위험.** 같은 대상의 두 주소가 다른 관측으로 남아, 같은 답의 서로 다른 자리에 같은 것이 두 번 나올 수 있다. 세 사례에서는 일어나지 않았다. 운영에서 분기 1건 이상 생기면 150 C의 범위 붙은 같음 관계(목적·판 범위가 있는 방향 관계 행)를 넣는다. 그때도 공용 관측은 합치지 않고 관계 행만 더한다.

### 6.4 사실이 바뀔 때: 두 방향

| 바뀐 쪽 | 예 | 경로 | 지난 답 |
| --- | --- | --- | --- |
| 사용자 쪽 | R1의 배포 런타임 3.13 → 3.12 | 새 요청판. 지난 쪽지 중 요건 사실이 같고 판이 맞는 것만 옮긴다(`carry_slips`). 나머지 판은 같은 위치만 다시 연다 | 당시 문장 그대로. 요청판 번호가 붙은 알림 1건 |
| 원문 쪽 | Pocket 도움말 개정 | 채널 차분이나 기한이 재확인 작업을 만들고, 새 관측과 대체가 생긴다. 사용 쪽지를 따라 알림이 간다 | 당시 문장 그대로. 자리별 알림 |

## 7. 운영 지표와 줄이는 규칙

| 지표 | 경보 임계 [가정] | 자동 동작 |
| --- | --- | --- |
| 서랍만 찾은 적격 후보 수 | 두 분기 연속 0 | 꼬리표·대비 작성을 멈추고 S의 표현(주소·판·위치·한 줄)으로 줄인다. 관측·쪽지·사용 쪽지는 유지한다 |
| 우연 적중 비율 | 서랍 적중의 30% 초과 | 기능어 목록과 꼬리표 작성 규칙을 점검한다 |
| 채널 커서 나이 | 주기의 2배 초과 | 그 채널의 관측은 재사용 때 다시 연다(재사용 관문 조건 1) |
| 겹침 구간 결번 | 직전 ID가 48시간 겹침에 없음 | 전체 목록을 1회 읽는다 |
| 재확인 큐 최고령 | 활성 답 항목이 72시간 초과 | 다음 요청 시계로 당긴다 |
| 예산 보류율 | 주간 요청의 5% 초과 | 후속·배경 몫을 줄이고 운영자에게 알린다 |
| 감사 숨은 무효 | 32건 중 2건 이상 | 그 공급자의 감시 층을 넓힌다 |
| 재확인 정밀도 | 분기 5% 미만 | 감시 키를 좁힌다 |
| 대조 인용 알림 | 0이 아니면 | 버그로 다룬다. 원리 자리는 대조 관측의 변화로 철회되지 않는다 |
| 같은 대상 중복 자리 | 분기 1건 이상 | 범위 붙은 같음 관계를 넣는다(6.3절) |

임계값의 출처는 [sections/discovery_ops.md 4절](sections/discovery_ops.md)에 있다. 보류율 5%는 152 S 낮은 예산·희소의 25/364(6.9%)보다 낮게 잡았다. 정밀도 5%는 024 S의 86/913(9.4%)보다 낮다. 감사 2/32는 015에서 당시 성립한 이유 83개 중 5개(6.0%)가 이후 무너진 기준율에서 왔다.

[q012]: https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/queries/queries.jsonl#L31
[r058]: https://github.com/laadkke-arch/agentflow-open/blob/fefeb2146c7f63e49d0578f78989be49acd63291/docs/workstreams/research/AF-RES-058/HANDOFF.md#L40-L48
