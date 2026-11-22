# AF-RES-025 기록 계약

CSV는 원래의 정렬·슬롯을 보존하는 UTF-8/LF 원장이다. 입력·관측·판정·계산은 별도 필드로 남긴다. JSON 문자열이 CSV 셀에 들어가면 csv.writer의 인용 규칙을 사용한다. 값0, 해당없음, 관측실패, 미확인을 섞지 않는다. 이 문서는 사전등록의 산술 의미를 바꾸지 않는다.

## 검색 관측

`search-log.csv`의 핵심 키는 `(question_id, route, query_index, observed_rank)`다. `event_type`으로 search_request/search_result/open_attempt/retry를 구별한다. 질의마다 요청 UTC, 원 질의 문자열, 엔진, response_length, 반환 결과 수, 관측 순위(제공도구의 출력 순서), 원 URL, 정규화 원천 URL/ID, 선택/탈락/중복/원제안 노출, 본문 열람 영수증, 실패를 기록한다. 도구가 전역 검색엔진 순위나10개를 제공하지 않으면 각각 `unknown`/실제수로 남긴다.

## 반환 슬롯

`returns.jsonl`은 질문×경로당 정확히3행이다. 빈 슬롯도 존재한다.

- question_id, route, rank(1..3), candidate_id, target_name, candidate_class(complete_product/reusable_part/same_field_design/distant_principle/empty)
- proposed_use, initial_named_target(bool), new_target(bool), new_use_in_known_target(bool)
- mandatory_predicates: 최초질문의 조건 ID 목록
- required_bundle: 조건별 필요한 `{source_id,url,section}` 목록. 복수 대체 묶음이 있으면 묶음 번호를 보존한다.
- returned_citations: 실제 반환에 붙인 URL/절 목록. 감사 후 보강을 여기 덧붙이지 않는다.
- opened_evidence: 최초 검색 단계에서 실제 읽은 URL/절 목록
- provider_status: support/conflict/hold; current_version, historical_version, historical_availability(supported/conflict/unknown)
- opened_complete, cited_complete, conflict_or_hold_reason, researcher_inference, empty_reason
- first_seen_query, first_seen_rank, search_receipt_ids, source_ids

위 bool은 판독자의 주장이다. 재집계는 조건별 필수 묶음과 인용 집합을 다시 확인하고 독립 판독과 불일치를 남긴다. 후보 union은 이름만으로 합치지 않고 canonical_target+behavior+use_boundary로 묶는다.

## 가린 판독

`blind/packets.jsonl`은 question_id, blind_key, 최초입력 위치/조건, 제안사용, 근거 목록만 갖고 route/rank/검색순서는 없다. 후보 이름은 근거의 주체를 판단해야 하므로 지우지 않는다. root는 mapping을 별도 보관하며 각 stream의 다른 에이전트가 자기 stream이 아닌4질문을 독립 판독한다. 공급자 근거와 질문자 후속선택은 두 판정원이고, 두 모델 판독자의 일치율과 혼동하지 않는다.

`judgments.csv`는 가린 키별 사용·필수 술어·주체·판·시간·반례, 공급자 판정과 후속판정, 읽은 묶음과 반환인용, self/independent 판독 결과를 담는다. 후속자료는 1차 가린판독이 봉인된 뒤에 읽어 별도 후속 열을 채운다.

## 산술

`valid_current = new_target and provider_status == support and opened_complete and cited_complete`.

`valid_historical = valid_current and historical_availability == supported`.

`top3_success(q,route)`는 원래순위1..3에서 valid가 하나 이상인 경우다. `top1_success`는 원래순위1만 본다. 반환순위를 감사 뒤 재정렬하지 않는다. 쌍별 G/R 성공유무와 유효슬롯개수 차이를 모두 보존하며, 주 승패는 성공유무로 판정한다. 불충족/미확인이 섞인 무승부를 별도로 표시한다. 노출 제외 민감도는 원제안/후속 답의 제목·요약 또는 본문이 후보 검색 중 노출된 질문을 통째로 제외한다. 표집 메타데이터 후속상태 노출은 별도 더 엄격한 민감도로 계산한다.

주 지표에서 기지제품의 새 부품/제약은 제외하되 `new_use_in_known_target` 보조표로 따로 보존한다. 당시판 미확인은 false 성공으로 채점하지만 이를 확정 기능불충족 건수로 세지 않는다. 비용은 제공된 단위만 합산하고 토큰/과금/인시를 임의 환산하지 않는다.
