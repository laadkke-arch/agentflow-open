# AF-RES-071 · 종료 자체 검산

## 질문과 반례

| 질문 | 결과 위치 | 근거 행 | 반례 탐색 및 판독 |
| --- | --- | --- | --- |
| Q1 | RESULT Q1 | A3-T5-advance, A3-T5-restore, A1-T1-rename | 판 지문으로 별개 사건을 세면 복귀 사건을 잃는다. 같은 해시의 초기·복귀 판 및 새 실행 확인. |
| Q2 | RESULT Q2 | B1-T3-unopened, A1-T2-discarded_note, A3-T2-offset, B2-T2-value | 목록에만 있는 파일, 읽고 버린 주석, 날짜 조건을 통과하지 않은 스레드, 실제 보고값 기여를 각각 대조. |
| Q3 | RESULT 표 2와 Q3 | VIEW:A1-T1-rename/retained/A0, VIEW:B4-T4-policy/retained/A1, VIEW:B4-T4-policy/lost/A2 | 주소만으로 성공한 경우, 판은 맞으나 설정 미확보, 조각·설정을 저장한 성공을 비교. |
| Q4 | RESULT Q4 | scores.csv의 recheck_answer/recheck_reason/recheck_link, DEC-A1~DEC-B4 | 위치만 바뀐 반례는 재연결 대상. 미개봉·무시 주석·읽기 순서만 바뀐 16개 판정은 A1 과잉. |
| Q5 | RESULT Q5 | TX03~TX14 | 예외·프로세스 종료 뒤 재조회, 같은 키 재전송·내용 충돌 및 복귀 뒤 옛 답 검색을 직접 실행. |
| Q6 | RESULT 표 2, Q6 | costs.csv와 cost-summary.csv | 차가운 앱과 캐시 보유 상태를 각각 시행. 새 원본 통신 0을 비용 미측정과 구별. |
| Q7 | RESULT Q7 | A1-T1-rename, B2-T2-value, A3-T5-restore, LOSS01 | 주소/태그/소비 조각의 경계에 맞는 문구를 비교. 조각 한 건이 없어도 옛 스냅샷이 남는 사례 확인. |

## 구조와 분모

| 원장 | 데이터 행 | 열 | 키와 검산 |
| --- | --- | --- | --- |
| frame.csv | 19 | 14 | frame_id, 원 ID 각 고유. A 11 후보와 B 8 후보에서 4+4를 원 ID 순 선정. |
| pairs.csv | 26 | 27 | pair_id 고유, 8개 객체에 조인. 주 22와 전진 4. 층×유형 10칸 모두 서로 다른 객체 2개 이상. |
| runs.jsonl | 249 | JSONL | 실행 ID 고유. 원시 52, 독립 판독 26, 보기 156, 중단/재시도·검색 14, 조각 누락 1. |
| judgments.csv | 4,680 | 13 | pair_id, 런 2개, 보기·조건·술어 고유 조합. 주 3,960. |
| scores.csv | 1,800 | 15 | 2층×5유형×2조건×3보기×30술어. 판정과 확정 참·거짓 분모를 원행에서 재집계. |
| costs.csv | 288 | 25 | 8요청×2보존×3보기×2캐시×3회. 샘플 ID 고유. |
| cost-summary.csv | 1,944 | 10 | 객체 8+전체의 조건별 합·최소·중앙·최대 재계산. |
| sources.jsonl | 30 | JSONL | 계보 28개 산입, 목록 2개 별도. 24개 원문 open 및 4개 출판사 색인 본문. |
| search-log.jsonl | 27 | JSONL | 접근별 URL·조회 조건·수신 실패. 실패 반환수는 null. |

두 주요 표는 표 1 26행×6열, 표 2 3행×8열이다. [근거와 원행의 고정 원장](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/evidence/ledger-audit.json)

- 정답·오답·보류 합계의 분모에는 모든 해당 시험 건을 넣었다. 참/거짓 사용 분모가 0인 층·유형·술어에서는 해당 없음으로 읽는다. 재생의 구조화된 답은 참/거짓 분모 열이 비어 있고 성공/오답/보류의 분모는 그대로다.
- 오배제·오채택에서 확정 오판은 관측 0건이다. 정보 부족으로 인한 보류는 별도 수다. HTTP 요청 0은 실험 내 관측수다. 과거 발행사 원 바이트, 네트워크 아카이브 재요청량, OS 캐시 제거, 운영 동시 갱신은 미측정이다.
- D0 목록, D1 지문/스냅샷, D2 같은 실행에서 기록한 read와 위치, D3 별도 문장/기간 값 및 차이 확인을 구별했다. 로컬 영수증의 바이트 구간을 발행사 HTML 오프셋으로 쓰지 않았다.
- A4/B4의 첫 평가를 다른 사례의 사전 시험과 분리했다. 순번 4의 요청·원문·변경쌍은 실험 전에 커밋됐다. 두 건은 SQLite 보기 및 판정기 커밋 후 처음 실행됐다. [실제 첫 평가 행](https://github.com/laadkke-arch/agentflow-open/blob/abfa72b4c9482955ce8af049ff80831284d6eab8/docs/workstreams/research/AF-RES-071/evidence/run-environment.json)
- 각 출처 허용 주장은 sources.jsonl의 claim에, 판별할 수 없는 것은 limits와 counterexample_or_unknown에 기록했다. 전사 판과 기후 기간 메타데이터 외에 실제 보정 이력, 관측일의 실측값이나 원 실행을 추정하지 않았다.
- GitHub의 결과 SHA 재열람, 계약 최종 대상과 종료값은 마지막 HANDOFF.md에 기록한다. 이 문서와 실험은 같은 세션에서 자체 검토했다.
