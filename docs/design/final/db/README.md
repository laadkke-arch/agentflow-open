# 확인 장부 구조 v1 · 저장 구조 실행 예제

이 디렉터리는 설계서의 저장 구조와 규칙을 고정 입력으로 끝까지 돌려 보는 실행 예제다. 제품 코드가 아니다. 보증하는 것은 "판독 결과가 주어졌을 때 기록, 재사용, 전파, 재생이 규칙대로 일어나는가"이다. 원문 판독과 꼬리표 작성의 품질은 보증하지 않는다. 그 입력은 사례 자료가 준다.

## 실행

표준 라이브러리만 쓴다(Python 3.11 이상, SQLite FTS5).

```sh
cd docs/design/final/db
python3 -I test_ledger.py -v        # 시험 40개
python3 -I cases.py                 # 세 사례 요약과 구성요소 삭제 결과
python3 -I cases.py --json > out/cases.json   # 커밋된 실행 기록과 바이트 단위로 같다
python3 receipts/r1_queue.py        # R1 실행 영수증(실행한 CPython 판의 결과를 출력)
```

`-I`로 실행해도 각 스크립트가 자기 디렉터리를 경로에 넣는다.

운영 시뮬레이션은 [../sim/](../sim/)에 있다. 이 엔진에 실제 시계·작업자·예산·여러 프로젝트를 붙여 13장면을 돌린다(`python3 -I ../sim/ops_sim.py`). 결과와 고친 내용은 [../07-review.md](../07-review.md)에 있다.

## 파일

| 파일 | 내용 |
| --- | --- |
| [schema.sql](schema.sql) | 공용 장부. 위치, 별칭과 취소, 판, 실행 영수증, 관측, 다시 본 기록, 꼬리표와 전문 색인, 대비, 대체, 변경 채널과 항목, 감시 키(층, 기한), 재확인 작업. 확정 기록은 덧붙이기만 한다(트리거) |
| [project_schema.sql](project_schema.sql) | 프로젝트 장부. 프로젝트마다 따로 붙인다. 요청판, 조건, 맥락 사실, 봉인, 필요 문장, 해석, 탐색 기록, 판정 쪽지, 답 실행과 자리, 사용 쪽지, 접힌 대안, 알림, 노출 |
| [ledger.py](ledger.py) | 엔진. 규칙 하나가 함수 하나다(아래 표) |
| [cases.py](cases.py) | 사례 A(R1), 사례 B(EVAL-X1), 장면 2(R2) 재생과 구성요소 삭제 시험 |
| [test_ledger.py](test_ledger.py) | 저장 계약, 규칙, 운영 고침(`OperationalFixes`), 세 사례, 구성요소 삭제의 기대값 |
| [receipts/](receipts/) | R1 실행 영수증 프로그램과 CPython 3.13.18·3.12.3 출력 |
| [fixtures/af-res-012/](fixtures/af-res-012/) | AF-RES-012 고정판 `cb602858`의 자료집(156항목)과 질의 사본 |
| [out/cases.json](out/cases.json) | 이 커밋에서 `cases.py --json`을 돌린 결과 |

## 규칙과 함수

| 규칙 | 함수 | 시험 |
| --- | --- | --- |
| 같은 판·같은 위치의 같은 내용은 새 관측이 아니라 다시 본 기록 | `Ledger.observe` | `test_same_content_is_a_sighting_other_edition_is_new` |
| 공개 꼬리표에 요청 문장을 쓰지 않는다 | `Ledger._privacy_lint` | `test_privacy_lint_blocks_request_words_in_public_tags` |
| 판이 다르면 재사용하지 않는다 | `Ledger.reusable`, `Ledger.carry_slips` | `test_a_runtime_change_reopens_only_the_new_edition` |
| 재사용 관측을 다시 열지 않는 다섯 조건 | `Ledger.reuse_gate` | `test_reuse_gate_five_conditions` |
| 묻기: 첫 절 같음, 요청판 재독, 공통 행동, 회수, 실행, 한 번 묻기, 조건부 | `Ledger.decide` | `test_clarify_rule` |
| 서랍 후보는 두 칸 이상·서로 다른 내용어 둘 이상, 기능어·숫자만 겹치면 우연 적중 | `Ledger.search_drawer` | `test_a_drawer_ranks_queue_first_and_drops_toyota_coincidence` |
| 원리 관문 ①②③과 대상 1차 문서 우선 | `Ledger.gate` | `test_gate_closes_when_target_doc_already_says_it` |
| 확인할 후보도 탐색 기록에 있는 이름만 | `Ledger.compose` | `test_check_slot_name_must_come_from_search_record` |
| 봉인이 노출보다 먼저 | `Ledger.show` | `test_exposure_needs_seal_first` |
| 채널은 외부 ID 집합의 차분만 읽는다 | `Ledger.poll` | `test_channel_uses_id_diff_not_display_window` |
| 공지 기한 24시간 전과 기한에 직접 읽고, 기한 경과만으로 무효로 하지 않는다 | `Ledger.due`, `Ledger._enqueue` | `test_deadline_job_merges_with_channel_item_and_does_not_invalidate` |
| 작업자 둘이 같은 재확인을 잡지 않는다 | `Ledger.lease`, `Ledger.release_expired` | `test_lease_prevents_double_work_and_expires` |
| 철회는 사용 쪽지를 따라 인용한 자리에만, 대조 인용은 제외 | `Ledger.propagate` | `test_b_each_event_touches_only_the_pocket_slot` |
| 그날 알던 것 | `Ledger.known_on`, `Ledger.current` | `test_b_what_we_knew_on_a_day` |
| 지난 답은 당시 문장 그대로 | `Ledger.replay` | `test_b_replay_and_no_answer` |
| 답이 없으면 상태·가장 가까운 대안·다음에 열 원문 | `Ledger.compose(status=…, next_action=…)` | `test_a_no_answer_gives_next_action_not_a_bare_abstain` |
| 취소된 별칭은 따라가지 않는다 | `Ledger.resolve` | `test_cancelled_alias_is_not_followed` |
| 일시 실패와 대체·철회된 관측은 재사용하지 않는다 | `Ledger.reusable(at=)`, `Ledger.stale`, `Ledger.reuse_gate` | `test_stale_observation_is_not_reused_or_cited`, `test_transient_failure_is_not_reusable` |
| 대체·철회된 관측 인용 금지, 원리 L2 상한, complete 조건 | `Ledger.compose` | `test_compose_rules_for_principle_and_complete` |
| 늦게 돌아온 작업자는 결과와 대체를 쓰지 못한다(임차 표지) | `Ledger.lease`, `Ledger.finish(token=, supersede=)` | `test_late_worker_is_fenced_and_supersession_is_written_once` |
| 새 원인은 대기 중 작업에만 합친다 | `Ledger._enqueue` | `test_new_cause_does_not_merge_into_a_leased_job` |
| 대체가 감시를 새 관측으로 넘긴다 | `Ledger.supersede`, `Ledger.watch` | `test_watch_moves_to_the_new_observation` |
| 잘못된 대체는 취소로 되돌린다 | `Ledger.cancel_supersession`, `Ledger.propagate` | `test_cancelled_supersession_restores_and_warns` |
| 시각은 UTC로 맞추고 형식 오류는 그 행만 건너뛴다 | `utc`, `Ledger.watch`, `Ledger.due` | `test_deadline_formats_are_normalized_or_rejected` |
| 채널 목록 중복 ID와 ID 체계 변경 | `Ledger.poll` | `test_channel_duplicates_and_id_scheme_reset` |
| 봉인은 노출보다 먼저이고 고칠 수 없다 | `Ledger.show`, `prior_seal` 트리거 | `test_exposure_needs_seal_time_and_seal_is_immutable` |
| 사생활 검사 거절문에 비공개 낱말을 넣지 않는다 | `Ledger._privacy_lint` | `test_privacy_error_does_not_echo_the_private_words` |
| 판독 주체를 남기고 판독기 하나의 관측을 다시 확인한다 | `Ledger.observe(reader=)`, `Ledger.recall_reader` | `test_reader_is_recorded_and_can_be_recalled` |
| 대체·철회된 관측에 기댄 쪽지는 옮기지 않는다 | `Ledger.carry_slips` | `test_carry_slips_drops_judgments_on_retired_observations` |
| 해석 결정은 덮어쓰지 않는다 | `Ledger.interpret` | `test_interpretation_is_not_overwritten` |
| S로 줄이는 규칙의 입력(서랍만 찾았고 답에 오른 후보) | `Ledger.drawer_contribution` | 시뮬레이션 M8 |

## 구성요소 끄기

`Ledger(features={...})`로 세 구성요소를 끈 채 같은 사례를 돌린다. 결과는 [../05-cases.md](../05-cases.md)의 5절에 있다.

- `drawer`: 공용 장부를 프로젝트와 시점 사이에 재사용한다. 끄면 프로젝트마다 따로 기억하고 서랍 검색이 빈다.
- `usage`: 답 자리에서 관측으로 가는 사용 쪽지로 철회를 전파한다. 끄면 프로젝트의 모든 답 자리에 알린다.
- `split`: 판단을 비공개 쪽지로 둔다. 끄면 판단이 공용 관측에 붙어 다른 프로젝트로 흐른다.

## 고정 자료의 한계

[cases.py](cases.py) 머리의 출처 표시를 따른다. `[고정 자료]`는 실제 검색 엔진과 판독 모델 대신 넣은 입력이다. 특히 새 검색 결과, 접수가 뽑은 칸별 필요 문장, 공급자 소식 채널 주소, ii-svn-log 제작자 글의 일본어 원문(저장소에 없음)이 그렇다. 이 값들이 실제로 그렇게 나오는지는 첫 구현에서 잰다([../06-assumptions-handoff.md](../06-assumptions-handoff.md)).
