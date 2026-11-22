# 카드 판독 지침 — 채점 기준은 전달하지 않음

이 문서는 공개된 SCOPE v1의 열람 규칙을 실행용으로 정리한다. `cards.jsonl`의 배정받은 사례만 읽는다. `key.jsonl`, `versions.csv`, `components.jsonl`, `sources.jsonl`, collection 및 다른 판독자 결과는 읽지 않는다. 기준 답이나 수집자의 판정은 사용하지 않는다.

## 순서와 두 과업

배정받은 사례에서 `presentation_index` 순으로 카드 하나씩 읽고, 카드의 `task_order` 순으로 C/H를 각각 수행한다. 같은 카드의 두 과업도 별도 시작이다. 앞 시행에서 본 링크·내용은 그 시행의 증거로 다시 쓰지 않는다. 기억을 없앴다고 주장하지 않으며 이미 노출된 사실이 있으면 적는다.

각 과업의 질문은 card.tasks에 있다. C는 목적에 따른 유지/교체/보류다. 답의 대상은 참조의 주장/방법/주소 중 질문에 명시된 것이며, 서로 다른 대상의 유지·교체를 혼동하지 않는다. 특정판을 확인하려는 목적을 최신판 사용으로 바꾸지 않는다. 시간 의도가 불명확하면 그 문제를 적는다.

H는 과거 발행판의 관련 문구 또는 레코드를 실제로 대조했는지다. X가 있으면 별도 로컬 표시로 기록한다. 실제 발행자의 판·절 확인, 발췌 재표시, 지정 원판과 충돌, 미확인을 구분한다. 후속 정정이 있어도 당시 그렇게 쓰였다는 사실은 별도다. 소비자가 실제 사용한 판이 불명확하면 그 한계도 기록한다. 연구에서 추가한 옛판을 보았다는 것을 실제 소비판의 증명으로 부르지 않는다.

## 최대 두 번의 발행 원문 열람

1. 첫 열람 URL은 해당 카드 body에 실제 보이는 URL만 선택한다. 소비 문서의 제목으로 검색하거나 다른 사례/앞 카드에서 본 URL을 끌어오지 않는다.
2. 둘째 열람은 첫 문서에서 실제 확인한 href만 가능하다. 카드의 다른 URL로 바로 점프하지 않는다. 원 href와 resolve된 URL, 도구 링크 ID/위치를 기록한다.
3. 실패도1회다. 실패 페이지에 유효 href가 없으면 종료한다. 재시도/다른도구로 같은주소 재요청도 새열람이다. 두번째요청은 첫문서 actualhref 규칙을 충족해야 한다.
4. 웹 검색은 금지한다. 첫 로드 본문 안의 `find`나 같은 문서의 line window는 카드/질문에 이미 있는 용어만 사용해 볼 수 있으며 새발행원문open이 아니다. 이 동작도 기록하되 예산0이다. PDF/ZIP 멤버를 열어 읽는 것은 다운로드한 그 문서 안의 열람이다.
5. 일반 공개 HTTP로 직접 열람할 수 있다. 웹 도구의 URL 실패 뒤 다른도구를 써서 실패를 지우지 않는다. 인증·우회·유료 API는 사용하지 않는다. 원문 응답이 캐시이면 네트워크왕복을 측정했다고 하지 않는다.
6. X는 로컬 표시1행으로 따로 기록하며 발행원문 예산을 소비하지 않는다. `미확인` 표시는 발췌 본문이 아니므로 재표시성공으로 세지 않는다.
7. 충분하거나 다음 허용href가 없으면1회로 끝낸다. 후속 진단을 원 시행에 합산하지 않는다.

## 저장 형식

배정받은 `readers/<reader_id>/` 아래 `reads.jsonl`, `judgments.jsonl`, `reader-notes.md`를 쓴다. 각 실제 동작 후 원장에 즉시 추가한다. git 조작은 하지 않는다.

`reads.jsonl`:

```
read_id, judgment_id, card_id, case_id, task, ordinal, mode,
requested_url, resolved_url, parent_read_id, href_raw, href_evidence,
outcome, observed_edition, locator, observed_fact, checked_utc,
tool_ref, budget_counted, diagnostic_only
```

mode는 publisher_open / local_X / same_document_find. publisher_open만 예산1. `href_evidence`는 첫요청이면 card-visible, 둘째면 첫본문의 실제href/링크ID/행이다. 답변 없는 필드는 `미확인`으로 쓴다. 일회응답 본문을 통째로 복제하지 않고 위치와 짧은 사실 요약을 남긴다. X 원문을 원장에 반복 인용하지 말고 카드 ID/해시로 연결한다.

`judgments.jsonl` 한 행은 카드×과업이며 배정사례당8행:

```
judgment_id, card_id, case_id, task, reader_id, order_index,
key_exposure, prior_card_exposure, visible_cues, read_ids,
publisher_opens, local_x_displayed, action,
historical_level, observed_edition, observed_locator, observed_claim,
consumer_edition_confirmed, support_state, hold_reason,
rationale, confidence, diagnostic_only
```

C action=유지/교체/보류. H historical_level=local_redisplay/publisher_edition_match/publisher_conflict/unverified. 실제 추가판본문은 대조했지만 소비자의 원판이 불명확하면 historical_level에 판대조수준을 남기고 consumer_edition_confirmed=false로 구별한다. C의 historical_level과 H의action은 해당없음. support_state=observed_support/observed_conflict/excerpt_only/insufficient/access_failed. hold_reason=normative_time_intent/criterion_requires_hold/access_failure/evidence_insufficient/edition_unknown/해당없음.

판정 후 자기 답을 채점하지 않는다. 틀린 답이 발견돼도 원관측을 덮어쓰지 않고 별도 정정 메모를 남긴다. 이 단계는 모델의 문서 판독이며 인간 사용성·시간·개인 실제 행동 관측이 아니다.
