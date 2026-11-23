# AF-RES-084 자체 점검

판정과 검토는 Codex Cloud의 같은 작업자가 했다. Q3 입력파일에서 후속 댓글과 080의 판정·정답을 거르고 ②를 커밋한 뒤 열었다. 편집 대조 #1060의 댓글은 그 전에 확인했다. 배정문과 080 인계가 알려 준 사례와 전체 결과는 판독자가 알고 있었다.

| 질문 | 원문·실행행과 주장 | 반대 가능성을 찾은 경로와 결과 | 빈자리와 최소 확인 |
| --- | --- | --- | --- |
| Q1 | [대상](fixtures/targets.json)과 [이벤트 원장](events.jsonl)의 ID·번호·UTC, 실제 닫힘. [GitHub 스키마](https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28#issuesevent) | 시간 파일 10개, 공개 Open, S3 미러, GraphQL, Wayback 및 Description 첨부를 확인. 개설 `opened` 행을 못 읽음. 이벤트 ID와 개설 해시는 null. | #1060을 포함한 실제 시간 행. [실패와 영향](attempts.jsonl) |
| Q2 | #1060 저자가 추가 편집을 명시. 복원 시험의 대상/동작/복수/누락/타인/현재 동일해시 시험 성공. [#1060 저자](https://github.com/python-attrs/attrs/issues/1060#issuecomment-1329862116) · [복원 시험](verify_events.py) | 인증 조회와 같은 이슈의 익명 null을 대조. #129의 생성 날짜와 현재 본문으로 개설판 추정을 반증했다. [인증 조회 사례](https://github.com/orgs/community/discussions/33551) · [#129](https://github.com/dear-github/dear-github/issues/129) | EDIT1060의 실제 개설 행/이력. 타이틀 풍선은 생성판을 대신할 수 없다. |
| Q3 | 가린 요구 10행, 보호 SHA `d3ff13eee67c7f81ddd39302d1f35576ef2b4423`. 확보·현재 원문 raw 일치 네 건. [가린 요구](inputs.csv) | 080 봉인에서 frames 줄끝 차이를 찾아 CRLF 해시와 Git LF 해시를 설명했다. [080 봉인](https://github.com/laadkke-arch/agentflow-open/blob/152f5261ab9a35ab675ab003931ac4dc89966b55/docs/workstreams/research/AF-RES-080/evidence/first-seal.json) | 열람 가능한 개설 본문으로 다섯 요구 항목 전부 다시 판독. |
| Q4 | 새 실행, 질문, 저자 성공 진술, 참조를 분리했다. CC01 질문판과 CN01 질문판이 명시됐다. [버전 원장](versions.jsonl) | 작성자 원 질문/후속/첨부에서 버전·실행자·stdout을 추적했다. #2276에서는 성공과 버전 변경을 발화자가 직접 연결했다. 타인 응답과 종결일은 증거로 승격하지 않았다. [#2276](https://github.com/pallets/click/issues/2276#issuecomment-1117371871) | AN01 질문 설치판, CC01·AC01 저자 성공 영수증. |
| Q5 | 16셀과 쌍을 재계산했다. 080의 판정과 10셀 일치. 근거 없는 원본문 판정 0셀. [16셀](cells.csv) · [쌍](pairs.csv) · [재계산](recalculate.py) | 고정 절의 raw 파일·절 SHA 29개를 Git 태그에서 재검사했다. AC01의 일반 훅 테스트 L46–66은 `__qualname__`을 키로 쓰는 대조로 정정했다. 공식 전용 훅 시험은 다른 파일에서 확인했다. [절 지문](fixtures/clauses.jsonl) · [test_functional.py L765](https://github.com/python-attrs/attrs/blob/7bfc49e9b22d5ba25b6e429524c3d49fee27cb36/tests/test_functional.py#L765-L781) | 새 정확판과 복원 본문이 들어올 때 각각 대응하는 쌍만 다시 계산. |
| Q6 | ③ 계획에서 새 실행 10, 상속 4, 미실행 6행을 분리했다. CN01만 명시 버전 두 입력을 직접 실행했다. [계획](fixtures/plan.json) · [실행](runs.jsonl) | 8.0.3 CliRunner가 EOF에서 시간 초과했다. 실제 stdin 파이프로 보정해 같은 예상과 입력을 유지했다. AC01 21.4.0은 저자 형태 두 키에서도 실패했다. [첫 시도](evidence/first-attempts.jsonl) · [계측 보정](evidence/fixture-correction.md) | 성공 당시 정확판에서 같은 키·플래그·서명을 실행하고 저자 로그와 구별. |
| Q7 | 원자료 91행과 31계보, 외부 30. 학술과 표준 2종에 실제 인용 포함. [자료 원장](sources.jsonl) | #1060, github-page #1, dear-github #129, Click #218·#2356, GH Archive #310은 독립 대조다. #1289에서 인용한 중복 이슈 등은 원 사건으로 묶었다. | 이슈 원문의 실질 수정 여부 및 원 작성자의 현재판 대안 채택은 별도 관측 필요. |
| Q8 | 확보 기준 참조 범위 변화 3개 양성 및 1개 반박. 최초 본문·엄격 판정은 0/16. [분모](metrics.json) · [응답 범위](RESULT.md) | 4건이 원 모집 320건의 대표 표본으로 해석되지 않게 순서와 원 분모를 남겼다. 080 기록과 이번 실행, 고정 참조판과 당시 정확판, 0건과 산출 불가를 구분했다. | 원본 복원 뒤 선행 순번을 확인해야 모집 전체 분모를 다시 채점할 수 있다. |

## 검산

- 개설 주체를 확인할 원본 없는 셀의 등재·공동 상태 승격 0건. 실제 타임라인 닫힘 ID를 개설 필드에 넣은 행 0건.
- 작성자 진술·080 재사용·이번 실행을 섞은 행 0건. 미확인 성공판 입력 여섯 행의 Python·판·출력과 종료가 모두 null.
- 새 run ID 10개와 실제 wheel 지문, 사전 계획 해시, 결과 판독을 비교했다. 080 전체 참조 8개 중 선택표에 필요한 기존 4개의 관측을 인용했다.
- 원시 입력에서 16개 고유 자리, 48개 쌍 행, 120/200 번호 있는 모집 행과 48개 선행 셀을 재생했다. 원자료 전체와 시간별 압축본은 커밋에 없다.
- 각 공식 wheel의 Python 파일을 상류 태그에서 다시 읽어 byte 비교했다. Click 8.0.3 17개, 8.1.2 16개, 8.5.1 17개, attrs 21.4.0 19개, 26.1.0 19개가 일치했다. 비Python wheel 메타데이터는 전체 wheel SHA로 확인했다.
