# 기록 계약의 사후 표시 정정

원 봉인 DATA_CONTRACT.md의 바이트와 주 지표를 유지한다. 아래는 공개한 예산 해석·상위 1 민감도·신규성 단위와 후속 기록 표시의 정정이며 사전등록 준수 주장으로 사용하지 않는다.

원 실행의 반환은 `returns-raw.jsonl`과 `candidates.csv`에 보존한다. `returns.jsonl`과 `candidates-strict.csv`는 원래 순위와 인용 순서에서 처음 세 고유 URL만 남긴 사후 제한판이다. 원 실행의 8/24 경로가 3 URL을 초과했다는 사실을 이 제한판으로 지우지 않는다. 후보 이름은 남아도 인용이 모두 잘린 슬롯은 빈 슬롯으로 표시하고 원 candidate ID를 보존한다.

기존 `top1_success`는 첫 **후보**의 인용 묶음을 보존하는 보조 지표다. 사용자가 요구한 둘째·셋째 **링크** 제거는 `tools/literal_top1.py`와 `evidence/literal-top1-summary.json`에서 따로 계산한다. 원래 순서의 첫 고유 URL 하나만 남기고 그 URL에서 이미 인용한 모든 절은 유지하며, 새 근거나 재정렬은 허용하지 않는다. 이 구분은 검색 뒤의 의미 정정이므로 새 사전등록 실험으로 주장하지 않는다.

`initial_named_target`는 봉인 당시 사용한 호스트/제품군 단위다. 정확한 부품명이나 API 이름이 최초 문서에 있었음을 뜻하지 않는다. Q01의 `pyarrow`·`binary_type`·`list_type`, Q11의 `ipykernel`·`cell_meta`는 최초 전문의 문자 검색에서 발견되지 않았다(`evidence/novelty-units.json`). 저자의 주관적 인지 상태는 미확인이다. 원 지표를 사후 바꾸지 않고 알려진 호스트의 새 부품/용도 수를 별도로 보고한다.

후속 기록은 `followups/*/decisions.jsonl`의 질문당 한 행과 `candidate-history.jsonl`의 원 반환 합집합 후보당 한 행이다. `judgments.csv`의 질문자 열에는 해당 기록 경로·실제 선택·근거 ID/URL을 넣고, 최초 공급자 판정/인용 열은 바꾸지 않는다. 당시 가용성 `not_available`는 구체 기능 후발이 확인된 경우, `unknown`은 전체 필수 조건의 당시 판을 확정하지 못한 경우다. 일반 프로젝트의 존재만으로 `supported`를 부여하지 않는다.
