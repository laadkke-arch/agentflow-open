# 통합 원장 오류·과장 교차검토

검토자: 별도 assistant agent `/root/baseline_methods`. 외부 사람의 독립 심사 또는 원연구의 독립 검증을 뜻하지 않는다. 검토자는 기준 연구 원장 작성에도 참여했으므로 해당 부분은 원자료 재대조이며 독립 작성자 검토가 아니다. 통합 변환 코드·다른 연구 원장은 루트 작성과 분리해 읽었다. 전역 파일은 수정하지 않았다.

검토 기준 시각: `2026-11-23T02:08:39.325399+00:00`. 대상은 `bounds.csv` 34행, `joins.csv` 10행, `endpoints.csv` 19행, `build_ledgers.py`, `evidence/source-counts.json`과 이들이 가리키는 스트림 기록이다. 행 수는 헤더를 제외한다. 아래 위치는 CSV 헤더를 포함한 물리 행 번호다. 결과 본문 `RESULT.md`는 이 검토 시점에 아직 존재하지 않아 검토하지 않았다.

## 발견한 오류와 재확인 상태

| ID | 오류·과장 가능성 | 위치와 근거 | 영향 | 필요한 수정·현재 상태 |
| --- | --- | --- | --- | --- |
| LR-01 | eXoaDocs 과제 3의 `−1/12`를 사람 수 단위로 표시했다. 실제 값은 `(3−4)/12`인 두 군의 비율 차이다. | 최초 `bounds.csv` 9행 `B02-task3`; `build_ledgers.py`가 ID 안의 `difference` 또는 `diff-`만 검사해 `task3`를 놓침. 원문 [Table XII](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf), `BM-B02`. | 수치 자체는 맞지만 단위가 다르면 정수 성공 수와 비율 대비를 혼동한다. | 루트에 전달 후 `unit=rate difference`로 바뀐 것을 다시 읽어 확인했다. 해결됨. |
| LR-02 | Newton의 저자 완료 표시 6/4를 `observed_joint_x`에 넣었다. 별도 secondary 표기가 있어도 이 열 이름은 요청한 시간·최종 품질의 공동 성공으로 읽힌다. | 최초 `bounds.csv` 21–22행 `S01-Newton-author-completion`, `S01-Control-author-completion`; `SW-N-P`, `SW-N-VIS`, [논문 Table 3 및 §4.2](https://users.ime.usp.br/~gerosa/papers/Newton.pdf). 이 검토에서도 기존 PDF의 표 색상과 §4.2 집계를 다시 대조했다. | 실제 저자 완료 수를 사전 기능 통과 기준과 시계를 결합한 1차 종점으로 오인하게 한다. 6/4 또는 `1/6`의 산술을 부정하는 지적은 아니다. | 루트에 전달 후 `observed_joint_x=미확인`, `observed_secondary_count=6/4`로 분리되고 secondary 범위가 유지된 것을 확인했다. 해결됨. |
| LR-03 | Newton 이벤트 수 열이 `미확인`인데 같은 행에 실제 메시지 이벤트 588행이 있다. | `joins.csv` 4행 `S01-roster-artifacts`: `right_input_rows.Newton_events=588`, `event_aggregation=588messageevents →12person-level inventoryrecords`; `event_rows=미확인`. 원 스트림 `streams/software/joins.json`과 `schema-audit.json`; `SW-N-D`, `SW-N-A`. | 분석 입력 수의 평탄화 누락이다. 목표 공동 종점 결합 여부나 성공 수 결론은 바뀌지 않는다. | `event_rows=588`을 명시하고 단위를 메시지 이벤트로 유지할 것. 기준 시각에는 미반영. |

## 오류로 판정하지 않은 쟁점의 범위

eXoaDocs의 `3/12−1/12=1/6`은 원문 §5.3.2가 명시한 공동 집계에 따른 표본 내 기술적 대비다. `reproduce.md`는 주변수만 썼을 때의 `[0,3]`/`[0,1]` 및 반대 방향 구성표를 원문 전체와 모순되는 반례로 구분하고 있어, 넓은 주변수 범위를 최종 식별 범위로 남기는 오류를 발견하지 않았다. `integer_extreme_tables`의 고정 x·변동 t라는 의미도 표시되어 있다. Blueprint의 q와 1차 공동 성공 범위는 미확인이며 임의 순위 통과선을 넣지 않았다.

Newton의 24개 notebook·응답 연결은 12사람의 두 조건 재고 연결이며 24명의 독립군이 아니다. Casdoc 122행 연결은 검색 조각 ID의 연결이며 배정·최종 판정의 연결이 아니다. 전역 `target_join_performed=false`는 현재 자료의 실제 작업 범위와 맞는다. E01의 분석 231행과 원래 배정 N 미확인, 26점 점수와 이진 통과 기준 부재, 약 35분과 강제 종료 시계의 차이는 전역 열에 구분되어 있다. 별도 분석행 112의 진단 자료와 S04/D01의 빈 자리는 여덟 자리의 새 배정 연구로 바뀌지 않았다.

`sources.jsonl`을 별도로 재집계한 결과 150행·150개의 고유 source ID, `count_toward_minimum`인 23개의 고유 work ID다. 세 CSV의 출처 참조는 모두 해소됐다. 범주별 수는 기준 2, 방법 4, 복제 2, 추가 원문 4, 새 원논문 4, 저자 자료 6, 별도 개입 자료 1로 `evidence/source-counts.json`과 같다. 총 고유 수가 22를 넘는 것과 새 여섯 자리·개입 자료 배당의 충족을 동일시하지 않고 전체를 부분 충족으로 둔 판정에 수적 오류를 발견하지 않았다. BM-P01의 실질적 저자 계획 문서 열람은 인정하면서 보수적 최소 수에는 넣지 않는 정책도 표시되어 있다. 이 검토는 다른 작업자의 모든 웹 열람을 새로 반복한 심사가 아니다.

## 검토판 지문

| 파일 | SHA-256 |
| --- | --- |
| `bounds.csv` | `6991968968f36c5d988029d26263be127868bdc49c991f8dba4362057ceaf224` |
| `joins.csv` | `747939991e5a3154680f2ccc80d3f2ae5bebb849d1ce3b7d68107f35e24c0113` |
| `endpoints.csv` | `a6660515b8e6bbc5db9e02c31e71dfa6936903abdafb3465d80ba270c8b67001` |
| `build_ledgers.py` | `e169271e8902e202a8dc84930e96d34c89513569f03d0b7d1b85c968a80cdde0` |
| `evidence/source-counts.json` | `3175cca383d8e7982510be0ebfb90f879b2e266ed7ea953fd2f1152af7c7d9d1` |

수학 전수 점검과 Casdoc 파일 감사의 별도 검토 범위·재계산 기록은 같은 디렉터리의 `root-review.md`와 `root-review.json`에 있다. 이 검토에서는 불필요하게 전체 코드를 다시 실행하거나 공개 참가자 원행을 복제하지 않았다.
