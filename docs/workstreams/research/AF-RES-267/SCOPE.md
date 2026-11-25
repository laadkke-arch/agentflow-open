# AF-RES-267 실행 범위 및 사전 판정표

## 착수판과 입력

- 저장소 `laadkke-arch/agentflow-open` · 작업 `work/research-af-res-267` · 시도 1 · 편집 경로 `docs/workstreams/research/AF-RES-267/`. 원격에 해당 작업 브랜치가 비어 있음을 확인했다. 제공 checkout의 로컬 `work` ref와 이름이 충돌해, 별도 checkout에서 최신으로 확인한 통합 SHA `9eeb7105c7edec2c5c4c0a1f722916b9d664b236`를 부모로 브랜치를 만들었다. 착수 확인 2026-11-25 01:00:26 UTC.
- [착수 진행표](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/docs/automation/dot-control.json#L6181) blob `8dc2966dac2d8c18c68a2684fbf0843cfd6fcfb5`에서 AF-RES-267은 `RUNNING`, `codex-cloud`, `attempt=1`, `manifest_id=af-res-267`, `source_commit=null`, `result_commit=null`, `depends_on=[AF-RES-249]`였다. [요청 시 기준 진행표](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/automation/dot-control.json)에는 267 행이 없었다. 진행표의 GitHub contents 본문이 비어 원격에서 가져온 Git blob을 직접 열었다.
- 통합 브랜치의 [AGENTS.md](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/AGENTS.md), [STATE.md](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/STATE.md), [Dot 절차](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/docs/DOT_AUTOMATION.md), [연구 운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/docs/RESEARCH_WORKFLOW.md), 계획판의 [연구 브리프](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/product/RESEARCH_BRIEF.md)와 [연구 운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/933a0f7d534314470c083b0aa284044a9ad45443/docs/RESEARCH_WORKFLOW.md)을 기준으로 삼았다.
- [AF-RES-249 진행표 행](https://github.com/laadkke-arch/agentflow-open/blob/9eeb7105c7edec2c5c4c0a1f722916b9d664b236/docs/automation/dot-control.json#L5761)은 중앙 `DONE`, `result_commit=a61cee2b8882e79226f383217440ab71f2637f8c`이다. 이 커밋에서 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/HANDOFF.md)를 열었다. 자체 DONE은 설계 범위다. HANDOFF가 가리킨 고정 설계 결과 `8c8c7b760c65dbca32fbe1094418eda47454b602`와 중앙 인계 `a61cee2b8882e79226f383217440ab71f2637f8c`를 구별한다. 이 작업은 요청에 명시된 인계 커밋에서 [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/RESULT.md), [원 실행기](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/verify_vectors.py), [코드 행](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/trace-artifacts.jsonl), [사례 표](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/worked-traces.csv), [과제 자극](https://github.com/laadkke-arch/agentflow-open/blob/a61cee2b8882e79226f383217440ab71f2637f8c/docs/workstreams/research/AF-RES-249/stimuli.md)과 관련 양식을 읽는다.
- `workbench.session start`가 생성한 [세션 핀](session.json)의 계약 버전은 2, `freshness_at_start=remote_checked`다. 시작 명령과 입출력은 [착수 영수증](receipts/session-start/command.txt)에 있다. manifest는 작업자에게 허용된 소유 경로 안에 두었다.

## 표집과 분모

| 단위 | 예정 | 포함 기준 |
| --- | ---: | --- |
| 합성 사건 | 4 | K/N/R/F 전수 |
| 스냅샷 귀속 행 | 12 | 각 사건의 t0·t12−(`t12minus`)·t24. 같은 UTF-8 bytes도 좌석별로 실행하고 고유 SHA256 수를 따로 산출 |
| 원 검증기 벡터 | 15 | 과제 A 7개(A0–A6), 과제 B 8개(B0–B7) |
| 스냅샷×벡터 | 90/회 | K/R의 A 6×7, N/F의 B 6×8. 서로 다른 빈 폴더 두 회차에 각각 12 프로세스 |
| 공개 단일 변경 통제 | 4 | 동률 방향, 전체 그룹화, bool/int, 변경 후 복원. 별도 함수 예외 대조 1개 |
| 고유 직접 원자료 | ≥20 | AF-RES-249 산출물 ≥6, v3.12.0 구현·문서·시험 ≥7, 언어·복사·로딩 ≥4, nbgrader 원 자료 ≥3. 파일·저작과 계보를 별도 집계 |
| 실제 사람 | 0 | 모집·연락·배정·실험·링크 열람 수집·품질 검수·인수·사람 노동 측정 범위 밖. 249의 잠재 사람 설계(24명×2과제)는 계획값 |

- 실행 대상은 249의 고정 JSONL 내 합성 소스와 이 과제의 명시적 공개 통제뿐이다. 과제 계약·원 평가·프로토콜·비교연구는 고정한다. 242 지역통계, 251 Audacity, 254 DBA, 255 CSS를 의존·표집에서 제외한다.
- 상태값을 분리한다. 예정에 없고 적용 대상 밖인 값은 `NA`, 의도적으로 비워 둔 대상 자리라면 `정상 공석`, 예정 관측물이 들어오지 않았으면 `미수신`, 호출이 없으면 `미실행`, 근거가 없어 분류할 수 없으면 `미확인`이다. 실제 사람 0은 이번 작업 범위의 계수이며 사람 단위 통과율·비용의 분모는 없다.
- Git 객체에서 원 파일을 가져오고, JSON 문자열의 UTF-8을 newline까지 그대로 재인코딩해 SHA256을 계산한다. 사건별 actor/assignment/session/task/phase와 직접 parent, worked-traces 참조를 별도로 대조한다. 코드 bytes 위상과 합성 행동 주장은 별도 행으로 남긴다. 원 실행기의 파일 자체는 수정 없이 해시로 비교한다.

## 결과 노출과 사전 판정

2026-11-25 00:57–01:00 UTC 착수 문서 및 249 HANDOFF 열람 중 `F t24`의 네 동률 실패(`B2/B3/B6/B7`), 나머지 코드 예상 통과, 합성 사례별 채택/거절 해석을 이미 보았다. 요청에도 타입·변경 후 복원·시점 중복 반례가 제시돼 있었다. 아래 표는 이런 노출을 포함한 재현 기대이며 블라인드 가설이 아니다. 이 범위 커밋 전에는 249의 코드 스냅샷, 실행기 원문, worked-traces/RESULT와 실제 벡터 출력은 보지 않았다. CPython 배포 페이지, 패치가 움직이는 3.12 라이브 문서와 공식 소스 빌드는 착수 중 확인했다. 과제 코드는 아직 호출하지 않았다.

| 판별 | 사전 기대 | 경쟁 예측과 판정 변경 조건 |
| --- | --- | --- |
| 원 설계 재현 | 매 회 K/N/R 전 시점, F t0/t12− 전 벡터 통과. F t24 B2/B3/B6/B7 실패. 회차 합계 86 통과/4 실패 | 행·태스크 매핑이나 원 기대가 다를 수 있다. 먼저 bytes/hash·runner SHA와 A/B 키 확인 후 원행을 보존하고 기대를 수정 이력으로 분리 |
| 실행판 | 정확한 CPython `3.12.0 final`, 공식 태그 commit과 실제 실행파일 SHA256을 함께 기록 | 원 실행기의 판 검사는 3.12.0을 보장하지 않을 수 있다. 소스 조건과 호스트 3.12.x를 읽어서 분리하고 정확판 이외 실행을 분모에서 제외 |
| 독립 판독 | 연속 경계와 `<= x` 원소 수를 기준으로 A/B 값을 재계산. 공개 벡터 전부에서 원 기대와 수기 답의 일치 기대 | 중첩 타입·입력 보존을 값과 따로 보고, runner와 참조가 다르면 하나로 덮지 않는다. 참조판은 공개 과제의 입력 도메인 안에서만 판단 |
| 단일 변경 | 왼쪽·전체 그룹화는 분리 벡터에서만 실패. bool은 0/1과 값이 같아도 형식 실패. 호출 중 변경 후 복원은 반환 시점 동일 비교에서 통과 가능 | 정상 대응 코드와 동일 입력을 비교한다. 복원 반례의 중간 쓰기는 별도 계측으로 측정하고, 계측의 관찰 범위를 기록 |
| 예외/재생 | 예외, 타입, 값 오답, 미실행을 서로 다른 증거로 분리. 두 빈 폴더에 같은 bytes를 다시 물리화 | 함수 예외 처리 경계, 모듈 로딩 실패 범위, stdout 비결정성 등을 출구/출력 형태에서 확인. 재현 실패를 성공으로 집계하지 않음 |
| 사람 근거 | 독립 품질·인수·사람 활동은 별도 키가 필요하다는 가설 | nbgrader 공식 테스트·루브릭·수동 점수 원필드에서 자동 점수와 사람 판단 연결·차이를 확인. 교육 채점의 사례로 적용 범위를 제한 |

합격표는 12 좌석, 15 벡터 정의, 90 벡터/회, 네 통제, 함수 예외, 빈 폴더 재생을 각각 확인한다. 같은 판정의 반복이라도 원영수증은 회차·스냅샷에 귀속한다. GitHub에서 읽을 수 있는 고정 결과와 각 검사의 대상 SHA·명령·종료를 확인한 뒤 마지막에 HANDOFF를 단독 커밋한다.
