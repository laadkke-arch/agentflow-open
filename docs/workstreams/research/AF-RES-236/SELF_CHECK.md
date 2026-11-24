# SELF_CHECK — PARTIAL

자체 대조(독립 검토 아님). 7d7f03080289a6392a4c50a7cd0bc5123d5b3ebc에서 7개 필수 결과 파일을 GitHub로 재열람했다. JSONL parser로 sources 100행, source_id 100 고유, counted 54 및 work_id 54 고유, 필수 키 누락 0 확인. frame.csv main 40, M1–3 3, M4–6 3 공석, S1 1 확인. RESULT 첫 줄 필수 표1 헤더, 표2, Q1–Q7 헤딩, 마지막 약점 3행 확인. comments-01~04 총 228/검색 metadata 40/40 일치, 60일 174, 빈 창 8/40를 재계산. 파일 내용 검사이며 GitHub 외부 실행, 실제 클릭/engine run, 독립 재현 아님.

| 질문 | 원근거/판정 | 반증·미확인 | 분모/미달 |
|---|---|---|---|
| Q1 | R00; before.md pre-comment SHA fb536c8fa26732e7f984e4aead61608338db21e2; I* | workaround heading 추출 오류, before-correction.jsonl은 후속 열람으로 표시; 원초 본문 미복원 | frame 40/40; 원초 edit 0/40 검증 |
| Q2 | I8785 I8793 I8803 S8903; chain permalink vs URL; D01–04 D08 | #8780/#9077 screenshot, #8769 계획 PR, #8806 code-only URL, duplicate 제외 | main URL 3/40, 3/6 자리; strict direct alternative 1/40; 보강 1/2, 16 screen 제한 |
| Q3 | D01–D08 A01–A05 P80284/P79561/P81858 | 실제 판·OS·요구 차이; alias 당시 페이지 미확인; strip != index, import != original write, tags != SIGHUP, AudioStream vs playback | 존재 main 3/3, supplement 1/1, exact full replacement unverified; 실행 0 |
| Q4 | I8785 I8793 I8803 S8903 T8785 T8793 T8803 T8903 P87165 | M1 accidental close before link, M3 third-party close, S1 explicit failure, P87165 wrong exposure | main read claim 1/3; trial 0/3 observed; adoption artifact 0/3 observed; supplement 1/1 attempted and failed by self-report, successful artifact 0/1 |
| Q5 | I8784 I8795 I8806 I8764 I8797 S9222 S9077 S8903 | named-only prior use, constraints, pre-existing knowledge, rejection; no history != ignorance | main specific linked function prior ignorance 0/3 observed; supplement prior awareness 1/1; actual unseen knowledge unknown |
| Q6 | O01 O02; O5502267 OA5502267 O5597274 OA5597274; OM* | original note/API failed, same mirror secondary, no primary confirmation of actor/action | OSM original docs 2/3; primary events 0/2 |
| Q7 | chain.csv, rivals.csv, RESULT tables, PRE* AF-RES-225 | 225 same-author patch no URL; 236 URL no verified replacement; cannot concatenate causal chains | complete causal chain observed main 0/3, supplement 0/1; causal effect not estimated |

## 누락·수정

- source ledger 54 counted distinct works: 32 main discussion + 1 supplemental discussion + 8 fixed docs + 5 code + 4 PR records + 2 process docs + 2 OSM creator docs. 46 not counted; OSM subgroup minimum and two primary events not met; total 22 met. No inflated duplicate views. 8 main bodies with no in-window discussion conservatively not counted.
- 40 sorted by created_at then issue no, 10 outside cap; current API total_count 470. Earliest 60-day window measured elapsed time inclusive. Broad/strict exposure definitions preserved separately; selection decision made by this worker since brief didn't explicitly adjudicate explanatory and follow-up links.
- All required main artifacts prepared, but no decisive full positive chain; S1 is counterexample, not a success. No additional alternate identity searches, private data, runtime tests, independent review, actual author click data.
- Latest integration vs plan comparison +6/-0; control file changed +308/-9; exact AF-RES-236 JSON entry/depends_on not accessible via connector or web. Fixed AF-RES-225 inputs read per user. Cannot claim unchanged task definition or dependency completeness. Scope is user-supplied brief; do not silently upgrade to DONE.
- UTC source acquisition windows provided, not fictitious per-page exact opening timestamps. Historical source publication times are path commits, not exact deployed HTML.
- Next worker should inspect original OSM action JSON and exact control entry first, then supplement primary cases and check artifact links. Any runtime claims remain expected/conditional; see handoff.
