# 후보 판정 실행 지침

이 파일은 SCOPE §5–6에 고정한 일치 규칙과 AF-RES-004 PROTOCOL v1.1의 적용 안내다. 새 점수나 라벨을 만들지 않는다. 원 기준은 고정 SHA `2b798c7d2b7355b649691c18de196104ceabb0f0`에서 읽는다. 기준선 원 응답은 절대 수정하지 않는다.

## 입력과 단위

판정 단위는 사례 × A/B 후보 순위 × 원 응답에서 제안한 사용 방식이다. CASES의 접두부 제약과 runs의 실제 조회·열람 요약을 읽고 판단한다. 후보가 주장하지 않은 사용 방식을 사후에 보충해 적합으로 올리지 않는다. 경계 사례는 실제 후보 URL의 해당 절을 추가 열람하고, 그 URL·시각·읽은 절·확인 내용·한계를 별도 검증 원장에 기록한다. 추가 검증을 기준선 실행 예산에 소급 섞지 않는다.

## 항목 일치

- 문서 gold는 저자가 기록한 비교 대상이며, 채택을 권장하는 정답이 아니다. 거절된 대안의 회수와 필수 제약 위반은 동시에 기록할 수 있다.
- 이름이 같은 프로젝트만으로 인정하지 않는다. 필요한 구성요소·구조·역할을 후보 이유와 열람 근거에서 확인한다.
- 공식 별명, 동일 저장소·하위체계, DOI/표준 식별자, 동일 명시 메커니즘은 일치 근거가 될 수 있다.
- 문서 내부 대안은 구조와 핵심 조건의 대응을 적는다. 외부 실체 적중과 `structural_design` 적중을 분리한다. 단순히 같은 단어나 일반 주제가 나온 것은 불일치다.
- 후보 하나가 여러 항목을 회수한 경우 각각의 독립 구조를 실제로 제시해야 한다. 문서 전체에 잠재적으로 등장할 수 있다는 이유로 확장하지 않는다.
- 모든 primary gold 분모는 동결된 CASES 그대로다. review-only 항목과 정답 밖 후보는 따로 판정한다. DRF처럼 본문 항목의 별명은 확대 분모에도 중복 추가하지 않는다.

## L/E/H/T와 라벨

L: `ok / broken / missing`. 실제 연결이 열리지 않은 경우 broken은 관측 상태이며, 확실한404/410·다른 대상과403/timeout/도구차단을 link_status로 구별한다. 차단을 허위 링크로 세지 않는다.

E: `supported / contradicted / unknown`. 검색 snippet만으로 supported를 주지 않는다. 원문 열람 기록이 주장한 메커니즘을 뒷받침하는지 확인한다. 현재 문서와 과거 존재 증거는 별개다.

H: CASES의 각 필수조건에 `pass / fail / unknown / not_in_scope`. `not_in_scope`는 원 응답부터 좁게 제시한 참고 부분에만 허용한다. 모든 조건을 범위 밖으로 미뤄 무관한 후보를 유용하게 만들지 않는다. 알려진 위반과 자료 부족을 구별한다.

T: `not_needed / mapped / analogy_only / unknown`. mapped이면 출발 요소·관계→대상 부분, 필요한 연결, 실패·비적용 조건을 명시한다. 구현 여부는 `runtime_observation: not_performed`로 남긴다. 실제 통합 성공으로 읽지 않는다.

우선순위는 `SURFACE_OR_CONSTRAINT_MISMATCH` → `INSUFFICIENT` → `CONDITIONAL_TRANSFER` → `DIRECT_DOCUMENTED`다. 단순 미구현만으로 reference_design을 모두 INSUFFICIENT로 만들지 않고, 반대로 알려지지 않은 결정적 전제를 conditional이라는 말로 통과시키지 않는다.

## 시간·노출·유용성

- primary match는 원 응답의 후보가 어떤 gold 항목과 일치하는가다. strict historical hit는 일치하고, 후보 근거가 결정 전으로 확인되고, 제외 문서가 아닌 경우다. 사후와 날짜 미확인 일치는 별도 수로 남긴다.
- 검색 중 정답 관련 snippet 노출도 run exposure다. 후보를 제거했다고 실행자의 노출이 사라지지 않는다. 노출 없는 실행의 부분집합을 별도 민감도로 보고한다.
- date unknown은 실패나 사후와 동의어가 아니다. 이 자료만으로 시간 적격성을 증명하지 못했다는 뜻이다.
- 정답 밖 유용 후보는 primary gold 일치가 없고, L ok/E supported이며 결정적 H fail/unknown이 없고, DIRECT_DOCUMENTED 또는 구체 mapped CONDITIONAL_TRANSFER인 경우다. 현재 문서 조건 통과와 당시 존재 확인을 분리한다.
- ‘더 낫다’는 별도 비교 주장이다. 단지 유용한 미인용 후보를 발견한 경우에 이 표현을 쓰지 않는다.
- 판정자는 `작업자` 또는 `내부 별도 검토`로 표기한다. 동일 모델의 내부 검토를 사람·타 모델·사용자 효용 검증으로 부르지 않는다.

## 기록 필드

`case_id, baseline, rank, candidate_name, candidate_url, gold_matches[{gold_id,match_kind,rationale}], review_matches, L,E,H[{constraint_id,value,reason}],T,transfer_mapping,H_assessment_scope,runtime_observation,label,link_status,date_status,strict_historical_gold_ids,post_decision_gold_ids,date_unknown_gold_ids,nongold_useful,nongold_historical_useful,near_miss,broken_or_fake,exclusion,judge,evidence_locations,remaining_check`를 후보마다 남긴다. 근거가 불충분한 경우 remaining_check에 무엇을 읽거나 실행하면 판정이 바뀌는지 구체적으로 적는다.

## 한계

원문 저자와 독립된 정답원을 사용해도 항목 분절·일치·효용 판정은 연구자의 코딩이다. 이 기록은 모든 선행기술의 완전한 관련성 판정이나 구현·사용자 성공 평가가 아니다.
