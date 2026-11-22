# AF-RES-035 연구 범위와 판정 규칙

## 시작점

| 항목 | 기록 |
| --- | --- |
| 계획 통합판 | `d3fbd08d44fd0e2915d1f766721a81845bacc213` |
| 배정 기록을 최초로 읽은 통합판 | `c8d6761204527179e5e653321369e44989005665` |
| 첫 산출물과 manifest의 시작판 | `9668632e915d508e93ddfdc5e8fe4b88bcbfec56`. 브랜치 생성 뒤 첫 `--fetch`가 다른 세 배정의 상태 갱신을 발견했다. 파일을 커밋하기 전에 브랜치를 fast-forward하고 manifest를 다시 생성했다. 두 시작 영수증은 [setup](receipts/setup/)에 있다. |
| 배정 및 소유권 | 관리형 Codex Cloud 셸, Debian GNU/Linux 13.6 x86_64, CPython 3.12.14. 확인 가능한 모델 표기는 GPT-6 기반 Codex이며 정확한 표시 모델과 추론 등급은 미확인이다. 작업 브랜치는 `work/research-af-res-035`이고 소유 경로는 이 디렉터리다. |

AGENTS, STATE, DOT_AUTOMATION, RESEARCH_WORKFLOW 및 AF-RES-035 배정 항목을 직접 읽었다. [통합판 작업 규칙](https://github.com/laadkke-arch/agentflow-open/tree/9668632e915d508e93ddfdc5e8fe4b88bcbfec56) · [배정 항목](https://github.com/laadkke-arch/agentflow-open/blob/9668632e915d508e93ddfdc5e8fe4b88bcbfec56/docs/automation/dot-control.json#L807)

[029@03e074b 인계](https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/HANDOFF.md) · [031@b252d3b 인계](https://github.com/laadkke-arch/agentflow-open/blob/b252d3b3a0c02fb1abd101670bc23d7de918d953/docs/workstreams/research/AF-RES-031/HANDOFF.md)

## 두 원 질문의 적용 범위

| 원 질문 | 동결하는 요구 | 029 문서 판정과 선행 관측 |
| --- | --- | --- |
| Q01 · Go #56094, `NewExtParam(value interface{}, opts ...interface{})` | Q01-P1/P2의 순서, 고정 폭, 초과분 미사용, 부족분 nil. 수신 Go에서 값과 동적 타입을 모두 검사한다. 사용자 측 옵션의 후속 파싱은 별도다. Go의 새 구문은 전체 제안이며 별도다. | JS 반환 부분 지지, 전체 충돌. JS 내부 예시만 성공했다. Go에서 JS 배열을 사용할 실제 연결 부품은 선행 반환에 없었다. [029 Q01](https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/RESULT.md#L5) · [후속용 입력](https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/supplementary/pending-checks.md#3-q01--의미-일치와-실제-go-호출자-사이) |
| Q10 · NEP 47 첫안의 DLPack 부분 | Q10-P01/P02/P03의 실제 소비 배열, 지원 CPU 배열의 살아 있는 공유, NumPy 생산 역할·장치 정보를 각각 확인한다. namespace·함수·캐스팅·전체 NEP 설계는 별도다. | A 부분 지지, 전체 미확인. C·B 부분 미확인. 후속 관측은 NumPy 자체 int32 배열의 공유만 측정했다. [029 Q10](https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/RESULT.md#L14) · [내부 대조](https://github.com/laadkke-arch/agentflow-open/blob/03e074bbba8db44b2f751dbd84042f07960a23e7/docs/workstreams/research/AF-RES-029/supplementary/runtime-probes.json) |

031의 Java Binary 시험은 양쪽 행 수 0으로도 통과했다. 이 작업의 양성에는 실제 수신자의 서로 다른 값과 타입을 요구한다. 빈 배열은 구조 경계로 별도 판정한다. 원 시험이나 앞선 검색을 반복 표집하지 않는다. [031 comparison.csv](https://github.com/laadkke-arch/agentflow-open/blob/b252d3b3a0c02fb1abd101670bc23d7de918d953/docs/workstreams/research/AF-RES-031/comparison.csv) · [0/2행 대조](https://github.com/laadkke-arch/agentflow-open/blob/b252d3b3a0c02fb1abd101670bc23d7de918d953/docs/workstreams/research/AF-RES-031/REPLAY.md#java-원본-논리행-반례의-별도-재생)

## 표집 및 판정

- Go는 공식 `syscall/js`와 Go WebAssembly의 공급판을 실행 후보로 삼고, Go 호스트에 JS 엔진을 임베딩하는 Goja를 문서·고정 소스·테스트에서 비교한다. 추출 전 같은 경로를 왕복시킨다. 원 변환, 정수 태그 경로, JS 단독, Go `make`와 `copy` 대조를 분리한다. 기존 추출의 판정은 JS 고정 폭 바인딩에서만 부여한다.
- DLPack 외부 CPU 후보 순서는 PyTorch CPU, 설치 불가 시 JAX CPU다. 정규 float32, 양의 stride를 갖는 slice, 빈 view, 지원 외 dtype 또는 쓰기 조건이 첫 표본이다. 복사 대조에는 동일한 비어 있지 않은 값을 넣는다. 내부 NumPy 대조는 외부 성공의 분모에 포함하지 않는다. 포인터와 initial payload 일치는 보조 지표다. 안전한 위치에서 생산자가 바꾼 두 번째 값이 소비자에서 보일 때 공유로 판정한다. 보장된 수명 안에서만 일반 참조 해제를 사용한다.
- 한 계약은 하나의 입력·방향·가설이다. `positive`, `boundary`, `expected_rejection`, `type_loss`, `resource`, `control`은 입력의 극성이다. 최초 기대 충족과 연구 목적 성공은 별도 열이다. 실제 이행 상태는 `observed`, `rejected`, `type_loss`, `resource_limited`, `process_failure`, `objective_failure`, `unexecuted`를 사용한다. 의도적 복사와 검증기 거절은 검사 성공이며 무복사나 타입 보존 성공에 더하지 않는다.
- 직접 원문 최소 24. 초기 질문과 공급자·표준 원문을 먼저 보고, 실행 또는 후속 결말 열람 전 고정판·fixture·기대를 묶음 ②에서 봉인한다. 같은 페이지의 여러 URL, API 미러, 배포 파일의 로컬 복제본은 한 원문으로 센다. 소스, 해당 동작을 독립적으로 검증하는 시험 및 서로 다른 명세 문서는 각각 기록한다. 수문·오디오의 도메인 대조는 소프트웨어 실행 분모와 별도다.
- 첫 실행과 빈 폴더에서 복원한 실행을 비교한다. 동일 작업자의 두 번째 판독, 명명된 공급자 시험의 코드 열람, 독립 작업자의 판독은 증거 종류가 다르다. 명령 경과 시간은 준비·다운로드·설치·실행·검증으로 분리하고, 사람의 절약 시간은 미측정으로 둔다.
