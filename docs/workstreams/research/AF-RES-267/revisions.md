# AF-RES-267 반례와 정정 기록

사전판 [SCOPE](https://github.com/laadkke-arch/agentflow-open/blob/9298b59b07c1f64c4792211db0c4d0e8a6bcf7a7/docs/workstreams/research/AF-RES-267/SCOPE.md)에서 확인 가능한 예상과 노출을 고정했다. 이 기록은 249의 원판과 이번 실행을 각각 보존하며 해석을 갱신한다.

| 전 판정 또는 예상 | 반증 입력·원행 | 실행 이후 판단 |
| --- | --- | --- |
| 입문 예시가 맞고 정렬이 계속된다면 B가 적합할 수 있다 | [왼쪽 통제 B1](receipts/controls/runs/left_ties/grader/stdout.jsonl#L2) 통과, [B2](receipts/controls/runs/left_ties/grader/stdout.jsonl#L3) 1/3, B3 0/3, B6 2/4, B7 1/3 | 동률이 없는 B0/B1/B4/B5는 방향을 식별하지 못한다. 왼쪽 통제 bytes는 F t24와 같으며 별도 실행하였다. |
| 키별 payload를 순서대로 모으면 A를 풀 수 있다 | [전역 묶음 A2](receipts/controls/runs/global_groups/grader/stdout.jsonl#L3), [A4](receipts/controls/runs/global_groups/grader/stdout.jsonl#L5), [A5](receipts/controls/runs/global_groups/grader/stdout.jsonl#L6) | 입력 첫 등장 순서를 보존해도 떨어진 같은 key를 합치면 계약을 위반한다. A4도 빈 문자열의 비연속성을 식별한다. |
| 0/1과 값이 같으면 B의 위치를 반환했다 | [bool B0](receipts/controls/runs/bool_indices/grader/stdout.jsonl#L1), [B1 직접 타입](receipts/controls/runs/bool_indices/reference/stdout.jsonl#L2) | 값 동등성과 정확한 타입이 갈린다. B0/B1/B4/B5는 bool 때문에 실패했다. |
| `unchanged=true`가 입력 수정 금지를 충족한다 | [복원 B2 원 판정](receipts/controls/runs/restore_input/grader/stdout.jsonl#L3)과 [동일 B2 호출 중 관찰](receipts/controls/runs/restore_input/reference/stdout.jsonl#L3) | 8/8 반환 시점은 같았고 8/8 호출 중 쓰기와 복원이 관찰됐다. 입력 변경 금지를 전 호출의 제약으로 읽으면 오통과다. 종료 상태만 요구한다면 이 통제의 통과는 맞다. |
| `exit=1`이면 반환값 불일치다 | [함수 예외 B2 원행](receipts/controls/runs/raise_on_tie_vector/grader/stdout.jsonl#L3)과 [F t24 B2](receipts/r1/runs/F-t24/grader/stdout.jsonl#L3) | 둘 다 프로세스 종료 1. 예외에는 `exception`과 `pass`가 있고 `got/type_ok/unchanged`는 미기록이다. 값 불일치에는 그 반환 필드가 있다. B3–B7은 예외 대조에서도 계속 실행됐다. |
| 249 인계의 ‘A1/B1 공개 예시’ 문구 | [원 인계 L60](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/HANDOFF.md#L60), [자극 A L6–19](receipts/original/stimuli.md#L6-L19), [원 실행기 L8–18](receipts/original/verify_vectors.py#L8-L18) | 참가자 공개 예시는 벡터 A6/B1. A1은 단일 행 벡터이자 별도 네임스페이스의 후보 카드명이다. 원 벡터 ID·순서·입력과 실행 수는 보존했다. |
| 합성 사례표에서 서술된 검수·인수자 이름으로 원 이벤트에 바로 조인할 수 있다 | [사례표 4행](receipts/original/worked-traces.csv#L2-L5), [F의 reviewer/acceptor 원행](receipts/original/worked-events.jsonl#L19-L20), K/N/R의 대응 원행 L37–38/L58–59/L76–77 | 네 사례 모두 `syn-r01…04` / `syn-ac01…04`와 `syn-r-K/N/R/F` / `syn-ac-K/N/R/F`가 다르다. alias 대응표 미확인. snapshot의 author/phase/SHA 조인은 12/12 맞았다. 독립 품질·인수 실측은 0. |

비동률 통과와 고정 벡터 전체 통과를 구별한다. 같은 bytes인 N t0와 F t0/t12−는 다른 사건·시점이어도 같은 출력이었다. 이 관측을 작성자 인증이나 인과 식별에 사용할 수 없다.
