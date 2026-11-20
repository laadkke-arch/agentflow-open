# AF-RES-016 — 역할·단위 분류의 재현성과 문제 상대성

## §1 필수 결과 표

### 표 1 — 분류안별 일치도

| 분류안 | 표본(011·012·004) | 단위 수 | 단순 일치율 | kappa 또는 alpha(95% 구간) | 주 불일치 유형 | 011 원래 값과 비교 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 후보 속성형 | 011 | 120 | 94/120 = 78.33% | κ=0.697 [0.562, 0.836] | 경계 정의 부족 16/26; 문맥 부족 6/26; 실제 다의성 4/26 | 동일120 원66/120=55.00% 대비 +23.33pp; 원149는50.34% | 미확인(새 사람·새 스레드 재코딩) |
| S1 후보 속성형 | 012 | 60 | 59/60 = 98.33% | κ=0.973 [0.908, 1.000] | 경계 정의 부족 1/1 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(무작위 질의 연결36개를 실제 제안 문맥으로 재측정) |
| S1 후보 속성형 | 004 | 18 | 17/18 = 94.44% | κ=0.915 [0.625, 1.000] | 경계 정의 부족 1/1 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(새 문제에서 반복; 현 표본4문제의 구간은 탐색적) |
| S2 문제 상대형 | 011 | 120 | 85/120 = 70.83% | κ=0.538 [0.372, 0.595] | 경계 정의 부족 23/35; 문맥 부족 7/35; 실제 다의성 5/35 | 동일120 원66/120=55.00% 대비 +15.83pp; 원149는50.34% | 미확인(새 사람·새 스레드 재코딩) |
| S2 문제 상대형 | 012 | 60 | 54/60 = 90.00% | κ=0.831 [0.698, 0.947] | 문맥 부족 4/6; 경계 정의 부족 2/6 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(무작위 질의 연결36개를 실제 제안 문맥으로 재측정) |
| S2 문제 상대형 | 004 | 18 | 18/18 = 100.00% | κ=1.000 [1.000, 1.000] | 불일치 0/18 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(새 문제에서 반복; 현 표본4문제의 구간은 탐색적) |
| S3 두 축 결합 | 011 | 120 | 75/120 = 62.50% | κ=0.561 [0.426, 0.656] | 경계 정의 부족 27/45; 문맥 부족 12/45; 실제 다의성 6/45 | 동일120 원66/120=55.00% 대비 +7.50pp; 원149는50.34% | 미확인(새 사람·새 스레드 재코딩) |
| S3 두 축 결합 | 012 | 60 | 51/60 = 85.00% | κ=0.818 [0.710, 0.915] | 문맥 부족 6/9; 경계 정의 부족 3/9 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(무작위 질의 연결36개를 실제 제안 문맥으로 재측정) |
| S3 두 축 결합 | 004 | 18 | 17/18 = 94.44% | κ=0.930 [0.725, 1.000] | 경계 정의 부족 1/1 | 다른 표본; 011과 직접 차이 추정 안 함 | 미확인(새 문제에서 반복; 현 표본4문제의 구간은 탐색적) |

### 표 2 — 불일치가 판정을 바꾸는가

| 불일치 쌍 ID | 역할 A | 역할 B | A일 때 판정 | B일 때 판정 | 판정 변화 여부 | 근거 위치 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 004-R03 | principle; standard × whole | principle; pattern × whole | P01-H1=pass; P01-H2=unknown; P01-H3=fail; T=not_needed; SURFACE_OR_CONSTRAINT_MISMATCH; 알려진 근접 오답 | P01-H1=pass; P01-H2=unknown; P01-H3=fail; T=not_needed; SURFACE_OR_CONSTRAINT_MISMATCH; 알려진 근접 오답 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 004-R03; [표본](sample/units.json); I03 RFC 6902 §3, §4.3, evidence/toy-counterexamples.json#json_patch_order, 004 EXPECTED.json R03 | 미확인(본문 복원 H2는 snapshot과 replay 입력을 추가해 확인; H3는 현재 구성의 실패를 유지한다.) |
| 011-T010-002 | mixed; mixed × part | component; framework × whole | 반응형 웹·DB·안전한 결제=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 반응형 웹·DB·안전한 결제=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T010-002; [표본](sample/units.json);  | 미확인(결제 경로·인증·DB 연결을 포함한 제안 구성 한 개를 명시한다.) |
| 011-T011-005 | product; app × whole | product; unknown × whole | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T011-005; [표본](sample/units.json);  | 미확인(실행 형태와 실제로 필요한 OS·알림 조건을 명시한다.) |
| 011-T011-007 | product; app × whole | product; service × whole | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T011-007; [표본](sample/units.json);  | 미확인(감시 대상이 내부망인지와 안정성 비교 관측을 제공한다.) |
| 011-T027-002 | component; data × whole | component; data × part | 별도 서버 예산 없음=unknown; 국가별 자동 판매 제한=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 별도 서버 예산 없음=unknown; 국가별 자동 판매 제한=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T027-002; [표본](sample/units.json);  | 미확인(위치 입력형·클라이언트 조회·판매 제한 동작을 한 사용 시나리오로 명시한다.) |
| 011-T036-005 | principle; pattern × reference | principle; pattern × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-005; [표본](sample/units.json);  | 미확인(실제 후보 두 개의 개발·교체·관리 비용 관측이 있어야 효과를 판정한다.) |
| 011-T036-008 | principle; pattern × reference | principle; pattern × mixed | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-008; [표본](sample/units.json);  | 미확인(평가 기준과 구현 조언의 주·보조 관계 및 적용 사례를 명시한다.) |
| 011-T036-014 | principle; pattern × reference | principle; pattern × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-014; [표본](sample/units.json);  | 미확인(동일 프로젝트의 직접 구현·라이브러리 사용 두 비용 기록을 확보한다.) |
| 011-T036-022 | principle; pattern × reference | principle; pattern × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-022; [표본](sample/units.json);  | 미확인(보안 중요도와 유지 기간이 다른 실제 사례에서 문턱의 실패를 관측한다.) |
| 011-T036-026 | principle; pattern × reference | principle; pattern × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-026; [표본](sample/units.json);  | 미확인(특정 후보·버전·필수 조건을 연결한 평가 행을 만든다.) |
| 011-T036-028 | mixed; mixed × reference | principle; pattern × reference | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T036-028; [표본](sample/units.json);  | 미확인(어떤 선택 문제의 어느 비용·제약에 경험을 옮기는지 연결을 명시한다.) |
| 011-T039-009 | component; library × whole | principle; pattern × reference | 오픈소스=unknown; ZooKeeper를 운영하지 않음=unknown; T=unknown; INSUFFICIENT; N 미입증 | 오픈소스=unknown; ZooKeeper를 운영하지 않음=unknown; T=unknown; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T039-009; [표본](sample/units.json);  | 미확인(실행할 큐 구현체 또는 메시지↔행·claim/ack·중단 후 재처리 설계를 제공한다.) |
| 011-T041-005 | principle; document × whole | component; data × whole | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T041-005; [표본](sample/units.json);  | 미확인(목록의 최근 갱신 시점과 필요한 주제의 항목 범위를 확인한다.) |
| 011-T041-009 | principle; document × whole | mixed; mixed × whole | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T041-009; [표본](sample/units.json);  | 미확인(각 정보원의 최신성과 문제에 필요한 범위를 별도로 확인한다.) |
| 011-T041-011 | principle; document × whole | component; data × whole | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T041-011; [표본](sample/units.json);  | 미확인(연결된 목록의 실제 범위와 갱신 시점을 확인한다.) |
| 011-T047-005 | principle; pattern × reference | principle; pattern × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-005; [표본](sample/units.json);  | 미확인(요구 전달 보장과 복잡성의 관측 기준을 명시한다.) |
| 011-T047-018 | component; library × whole | principle; pattern × reference | H: must 미제공/unclear; T=unknown; INSUFFICIENT; N 미입증 | H: must 미제공/unclear; T=unknown; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-018; [표본](sample/units.json);  | 미확인(기존 Postgres 유무, 큐 구현체·설정, 필요한 전달 보장을 제시한다.) |
| 011-T047-023 | mixed; mixed × mixed | principle; pattern × reference | H: must 미제공/unclear; T=unknown; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=unknown; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-023; [표본](sample/units.json);  | 미확인(현재 단계와 실제로 채택할 도구·설정을 선택해 별도 행으로 평가한다.) |
| 011-T047-032 | component; service × whole | product; service × whole | H: must 미제공/unclear; T=not_needed; INSUFFICIENT; N 미입증 | H: must 미제공/unclear; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-032; [표본](sample/units.json);  | 미확인(필요한 전달 보장·중단 시나리오·구체 PostgreSQL 기능과 버전을 제시한다.) |
| 011-T047-045 | mixed; mixed × reference | principle; pattern × reference | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-045; [표본](sample/units.json);  | 미확인(질문의 규모·보장 값을 측정한 뒤 한 구성을 특정한다.) |
| 011-T047-054 | product; service × whole | product; service × unknown | H: must 미제공/unclear; T=unknown; INSUFFICIENT; N 미입증 | H: must 미제공/unclear; T=unknown; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-054; [표본](sample/units.json);  | 미확인(경험의 적용 대상과 현재 질문에 권하는 사용 방식을 한 문장으로 복원한다.) |
| 011-T047-062 | principle; pattern × reference | product; service × comparison | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | H: must 미제공/unclear; T=not_needed; 전체 판정 라벨 미부여; 전체 충족 주장 없음 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T047-062; [표본](sample/units.json);  | 미확인(대상 버전과 실제 요구 복제·중단 조건을 먼저 고정한다.) |
| 011-T048-002 | principle; pattern × reference | component; library × comparison | 7디스크 RAID5와 자동 scrub/복구=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 7디스크 RAID5와 자동 scrub/복구=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T048-002; [표본](sample/units.json);  | 미확인(버전·7디스크 구성·scrub와 복구 경로를 명시한다.) |
| 011-T053-002 | component; library × whole | unknown; unknown × whole | 현재 라이브러리와 같은 목적=unknown; 활발한 유지보수=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 현재 라이브러리와 같은 목적=unknown; 활발한 유지보수=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T053-002; [표본](sample/units.json);  | 미확인(비교 기능 목록과 고정 관측 기간의 유지보수 기록을 제공한다.) |
| 011-T054-003 | mixed; mixed × mixed | component; data × whole | 라벨 대신 회로 선 연결=unknown; PCB 배선 생성=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 라벨 대신 회로 선 연결=unknown; PCB 배선 생성=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 011-T054-003; [표본](sample/units.json);  | 미확인(동일 입력 회로·도구 집합·설정에서 선 연결과 PCB 출력 결과를 검증한다.) |
| 012-origami-solar | principle; research × none | principle; document × none | 재연결·반복 worker 중단 뒤 메시지 재처리=unknown; T=unknown; INSUFFICIENT; N 미입증 | 재연결·반복 worker 중단 뒤 메시지 재처리=unknown; T=unknown; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 012-origami-solar; [표본](sample/units.json);  | 미확인(관련성을 주장하려면 접기 구조와 메시지 복구 관계의 대응·실패 조건을 별도로 제시한다.) |
| 012-otel-wal | component; library × whole | component; library × unknown | 새 별도 broker를 운영하지 않음=pass; T=not_needed; INSUFFICIENT; N 미입증 | 새 별도 broker를 운영하지 않음=pass; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 012-otel-wal; [표본](sample/units.json);  | 미확인(상위 질문의 목표·10분 중단 여부·queue/retry/디스크 조건을 복원한다.) |
| 012-pg-wal | component; service × reference | component; library × reference | 이전 파일 판을 선택해 복원=unknown; T=analogy_only; INSUFFICIENT; N 미입증 | 이전 파일 판을 선택해 복원=unknown; T=analogy_only; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 012-pg-wal; [표본](sample/units.json);  | 미확인(파일 baseline·변경 이력·보존 정책·복원 알고리즘의 대응과 실패 조건을 제시한다.) |
| 012-pypi-aiolimiter | component; library × part | component; library × none | 대기 최대 8 / 처리 중 최대 4=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 대기 최대 8 / 처리 중 최대 4=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 012-pypi-aiolimiter; [표본](sample/units.json); I02 Typical use/Bursting/API, evidence/toy-counterexamples.json#rate_not_concurrency | 미확인(limiter의 단독/보조 사용 여부와 완료 기반 permit·유한 queue 구성을 명시한다.) |
| 012-pypi-opentelemetry-exporter-otlp | component; library × part | component; library × none | Collector 외부 전송의 10분 장애·재시작 손실 감소=unknown; 새 별도 broker 금지=unknown; T=not_needed; INSUFFICIENT; N 미입증 | Collector 외부 전송의 10분 장애·재시작 손실 감소=unknown; 새 별도 broker 금지=unknown; T=not_needed; INSUFFICIENT; N 미입증 | 없음(고정 사용·같은 근거) | [impact.json](evidence/impact.json) rows 012-pypi-opentelemetry-exporter-otlp; [표본](sample/units.json); I01 OTLP Collector Setup/Dependencies/Usage | 미확인(송신자·수신자·실행 위치와 Collector queue/storage 설정을 명시한다.) |

### 표 3 — 판정 어휘 대응

| 작업 | 어휘 | 답하는 질문 | 대응 어휘(다른 작업) | 같은 것으로 읽으면 안 되는 이유 | 근거 위치 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | IN-A/B/C; 실제 A_free_text / B_light_structure / C_ai_decomposition_proposal | 입력을 어떤 표현으로 전달하는가(판정축 밖) | 003의 저장안 A/B/C와도 별도 | 001은 입력 표현, 003은 저장 원리다. 알파벳이 같아도 상태나 우열이 아니다. | V01 RESEARCH §3; V02 cases[*].formulations | 없음 |
| 001 | 미입력 / 명시적 모름 / 아직 미정 / 해당 없음 / 명시적 무제약 / 상충 | 근거 충분성에 앞선 입력 의미·결정 상태 | 011 absent / explicit_unknown / undecided / not_applicable는 일부 대응 | 빈칸은 무제약이 아니며, 미정은 무지와 다르고, 상충은 단순 결측이 아니다. 004 INSUFFICIENT로 일괄 변환하면 원인이 사라진다. | V01 RESEARCH §5 | 없음 |
| 001 | explicit / explicit_current / explicit_design / explicit_example / explicit_preference / explicit_unknown | 원문이 무엇을 어떤 지위로 명시했는가 | 011 정보 present 또는 질문시점/강제성 필드에 조건부 연결 | explicit은 제품 사실의 검증이 아니다. 계획·예시·선호를 현재 가동·필수로 바꾸지 않는다. | V02 cases[*].formulations.C_ai_decomposition_proposal.input_read_back[*].reading_status | 없음 |
| 001 | interpretation | 누가 원문을 해석한 문장인가 | 003 연구자 해석; 010 H 연결 해석 | 사용자 명시 요구나 검증된 적합성 라벨이 아니다. 18개 제안 중11개에서 사용했다. | V02 proposals[*].status; K05.P1 | 없음 |
| 001 | proposal_unconfirmed; user_confirmed=false | 제안이 사용자 확인을 받았는가 | 002 조건부 후보와 모두 ‘채택 전’이나 직접 동치 없음 | 미확정 제안은 근거 부족을 뜻하는004 INSUFFICIENT와 다르다. 문서 근거가 있어도 사용자 확인은 없을 수 있다. | V02 proposals[*]; K02.P2 | 없음 |
| 001 | proposal_requires_constraint_change | 현재 조건을 유지한 해법인가, 조건 변경을 가정한 새 안인가 | 004 현재 사용 방식의 H fail과 관계하나 라벨 자동 대응 없음 | 제안을 검토할 수 있다는 사실로 현재 요구의 충족 판정을 살릴 수 없다. K05.P3은 현재 입력을 변경해야 한다. | V02 cases[id=K05].formulations.C_ai_decomposition_proposal.proposals[id=K05.P3] | 없음 |
| 002 | 조건부 후보로 유지 | 탐색을 계속할 가치가 남는가 | 012 1로 투영한 사례; 004 INSUFFICIENT/CONDITIONAL_TRANSFER와 조건부 관련 | 유지에는 부족한 설정, 부분 유용성, 검토할 완성품이 섞인다. 완성품 유지가 직접 적합 확정은 아니다. | V03 RESEARCH §1·§3; V14 선행입력 투영표 | 없음 |
| 002 | 완성품 판정 보류 / 원리 참고로 남김 | 어느 역할의 판단을 보류하고 무엇을 계속 다룰 수 있는가 | 004 역할·사용 방식별 별도 행; 012 1 또는 미판정 | 하나의 후보에 대한 전면 보류가 아니다. Outpost의 팀 완성품 판단과 원리 참고는 범위가 다르다. | V03 RESEARCH §3, P2 완성품 행 | 없음 |
| 002 | 중단 | 이 발견 경로의 추가 검토를 왜 멈추는가 | 012 Jiandu P1.w의 명시0 | 접근·평가 조건 때문에 멈춘 것과 기능 위반N은 다르다. 반복 정보에 따른 탐색 중단도 후보 부적합이 아니다. | V03 RESEARCH §3·§7; V15 P1.w/jiandu | 없음 |
| 003 | 같음 | 두 기록은 어떤 범위에서 같은 대상을 가리키는가(동일성) | 직접 대응 없음; 같은 대상 ID의 조건부 연결 | 004 DIRECT_DOCUMENTED나012 2는 요구 적합성이다. 이름 변경·같은 제품 귀속이 버전/배포/기능 호환성을 보증하지 않는다. | V04 RESEARCH §3.1–3.2; V05 C01·C03 | 없음 |
| 003 | 관련됨 | 부분·포크·후계·설명·유사 원리 중 어떤 관계인가(동일성/관계) | 010 mapping이나012 1은 특정 목적에서만 부분 대응 | 관련 대상이라는 이유로 같은 속성을 복사하거나 검색 관련성을 부여하지 않는다. 관계가 모르면 관련됨으로 채우지 않는다. | V04 RESEARCH §3.2; V05 C03·C06 | 없음 |
| 003 | 보류 | 같은가 다른가를 가를 식별 근거가 충분한가 | 004 INSUFFICIENT와 ‘미결정’이라는 상위 특성만 공유 | 003은 동일성 술어, 004는 제안 사용 방식의 판정이다. 같은 대상인지 몰라도 특정 원리의 참고가 가능하고 그 역도 가능하다. | V04 RESEARCH §3.2; V05 C04 | 없음 |
| 003 | 미귀속 | 이전 근거가 분리된 어느 대상에 속하는가 | 001 원문–해석 참조, 004 E unknown과 조건부 관련 | 근거의 소유 대상이 불명한 상태이며 주장 자체가 거짓이라는 뜻이 아니다. 옛 ID를 한쪽으로 조용히 옮기지 않는다. | V04 RESEARCH §7 | 없음 |
| 004 | alternative / component / reference | 이 행은 후보를 어떤 사용 방식·역할로 제안하는가 | 011 product/component/principle; 012 corpus role과 조건부 대응 | alternative는 문제 상대적 대체 역할이다. product는 답 또는 산출물 형태 분류다. 앱도 reference가 될 수 있고 부품도 선택 부분의 직접 대안이 된다. | V06 판정 단위; V07 rows[*].role | 없음 |
| 004 | L: ok / broken / missing | 근거 위치를 찾을 수 있는가(근거 충분성의 연결 전제) | 011 accessible/redirected/failed/not_linked와 좁게 대응 | 접속 성공은 주장 뒷받침E나 요구 충족H가 아니다. blocked는 실제 broken으로 바꾸지 않는다. | V06 네 판단축; V11 §6 | 없음 |
| 004 | E: supported / contradicted / unknown | 특정 주장과 조건을 원문이 지지하는가(근거 충분성) | 011 E 반박은 참여자의 반박 사건 | 011의 E 코드는 연구자가 외부 사실 오류를 검증했다는 값이 아니다. unknown도 contradicted와 다르다. | V06 네 판단축; V11 §5 | 없음 |
| 004 | H: pass / fail / unknown / not_in_scope | 제시한 사용 방식은 각 필수조건을 만족하는가(적용 가능성) | 011 H 반박; 012 2/N과 조건부 연결 | pass는 평가 범위의 문서·논리 판단이다. not_in_scope는 최초의 좁은 참고 범위이며 실패한 전체안을 사후 면제하는 값이 아니다. | V06 네 판단축·v1.1; V07 rows[*].H | 없음 |
| 004 | T: not_needed / mapped / analogy_only / unknown | 분야 간 관계·연결·실패 조건이 설명되는가(전이) | 010 같은 T값과 같은 정의 | mapped는 최종 라벨이 아니다. 전이 대응이 명확해도 옮긴 사용 방식이 필수조건을 위반할 수 있다. | V06 T축; V09 RP1-B09-M; V10 RP2-C05-M | 없음 |
| 004 | DIRECT_DOCUMENTED | 이 구성의 필수조건에 긍정 문서근거가 있는가(적용 가능성+근거 충분성) | 012 2, 동일 구성·범위를 보존할 때 | 실제 실행·통합 성공이 아니다. 다른 구성이나 부분 질문으로 이동하면2를 그대로 복사하지 않는다. | V06 기대판정4종; V07 R01·R02; V14 투영표 | 없음 |
| 004 | CONDITIONAL_TRANSFER | 좁은 참고 관계·연결·비적용·실패 조건을 구체화했는가(전이) | 010 같은 라벨; 012 주로1, P04.2의 ct-merkle은2 | 미확인 필수전제를 ‘조건부’로 넘기는 라벨이 아니다. 질의가 좁아지면 검색등급은 달라질 수 있다. | V06 기대판정4종; V07 R17; V15 P04.w/P04.2 | 없음 |
| 004 | SURFACE_OR_CONSTRAINT_MISMATCH | 표면만 닮았거나 결정적인 알려진 요구 위반이 있는가(적용 가능성) | 010 surface_false_positive/near_miss; 012 N과 좁게 대응 | 표면 관계 불일치와 근접한 후보의 필수조건 위반을 함께 담는다. 전부 실제 사용자 거절 사건인011 근접오답과 같지는 않다. | V06 기대판정4종; V09–V10 buckets; V11 §5 | 없음 |
| 004 | INSUFFICIENT | 결정에 필요한 사실·설정이 부족하며 답에 따라 판단이 달라지는가(근거 충분성) | 010 동일 라벨; 012 1/0/미판정 중 범위에 따라 다름 | 알려진 결정적 위반은 제외한다. R05는 저장 없는 core의 부분 유용성만012에서1이다. 후보 전면 실패나 검색 관련성0을 뜻하지 않는다. | V06 기대판정4종; V07 R05·R09; V14 투영표 | 없음 |
| 010 | mapped + CONDITIONAL_TRANSFER | 대응한 관계를 좁은 설계 참고로 쓸 수 있는가(전이) | 004 동일 조합 | 원저자 역사적 전이 보고와 이번 대상의 실제 적용은 다르다. reference_design과 runtime_observation을 보존해야 한다. | V08 판정 방식; V09–V10 judgments | 없음 |
| 010 | mapped + SURFACE_OR_CONSTRAINT_MISMATCH; near_miss | 관계는 대응해도 이 사용 방식이 고정 조건을 깨는가(전이+적용 가능성) | 004 H fail; 012 N과 조건부 대응 | mapped를 적합으로 승격하면 반례3개를 뒤집는다. RP1-B09-M은 재시작 때 재허가, C08은 정당한 수정 절제, C05-M은 작은 충돌 무음삭제다. | V09 RP1-B09-M; V10 RP2-C08·RP2-C05-M | 없음 |
| 010 | analogy_only; surface_false_positive | 어휘 유사성 밖에 대응 관계가 있는가(전이) | 004 T analogy_only 및 mismatch의 일부 | 관계 미성립과 근거 부족unknown은 다르다. P2 C07의 동일인 판별은 이미 같은 ID인 수정 충돌 해법이 아니다. | V09 RP1-B07; V10 RP2-C07 | 없음 |
| 010 | new_candidate / rediscovery / technical_support / insufficient | 이번 탐색에서 어떤 발견 종류인가(검색 과정 메타데이터) | 012 origin=new/transfer와 직접 대응 없음 | new_candidate는 소프트웨어 발명·좋음 점수가 아니다. rediscovery도 유용할 수 있으며 발견 경로와 적용 판정은 별도다. | V09–V10 judgments[*].bucket | 없음 |
| 010 | implementation_H=unknown; runtime_observation=not_performed; conditional_reference | 대상 구현을 실제 확인했는가, 어느 참고범위인가(근거 충분성/적용 범위) | 004 reference_design 및 runtime_observation=not_performed | 원 분야 관계의 mapped와 대상 구현의 unknown은 공존한다. 조건부 참고는 실제 운영pass가 아니다. | V08 판정 방식; V10 RP2-C05·RP2-C06·RP2-C05-M | 없음 |
| 011 | whole / part; product / component / principle / mixed | 질문이 선택하는 범위와 답이 내놓는 대상의 역할은 무엇인가(판정축 밖) | 004 proposed role, 012 corpus role과 조건부 대응 | 질문의 크기·프로젝트 설명 길이·답의 산출물 형태가 다르다. mixed는 제품이 여러 개라는 이유만으로 부여하지 않는다. | V11 §1.1·§4; V12 answers[*].role | 사람 간 재현성 미확인(별도 사람 코딩 필요) |
| 011 | FIT / TRADEOFF / PERSONAL_USE / CROSS_DOMAIN | 답에 조건 대응·한계·사용경험·분야 연결이 표현됐는가 | 004 E/H/T의 입력 근거로 활용 가능 | FIT는 실제 H pass가 아니고 CROSS_DOMAIN은 mapped가 아니다. PERSONAL_USE도 이 문제에서의 통합 성공이 아니다. | V11 §4·v1.3 | 없음 |
| 011 | accepted=true/false/null; top_voted=true/false/null | 게시물의 채택표·최고점 표식을 관측했는가(반응 관측) | 직접 동치 없음 | accepted false와 null은 다르다. 채택된 게시물 안 일부 방안이 거절될 수 있으며 최고점은 질문자의 선택이 아니다. | V11 §4·v1.3; V12 T027 | 없음 |
| 011 | adopt / reject / try / thanks / none / unknown | 질문자가 무엇을 말했다고 관측했는가(반응 관측) | 004 적합성 라벨,012 등급과 직접 동치 없음 | 감사·시험 의향은 채택이 아니고 무응답은 거절이 아니다. adopt의 식별·계획·진행·보고된 사용·통합 단계를 별도로 유지한다. | V11 §4·v1.3; V12 outcome·adoption_stage·trial_stage | 관측 밖 사용 결과 미확인(후속 사용자료 필요) |
| 011 | L / E / H / T 반박; SURFACE_OR_CONSTRAINT_MISMATCH | 실제 반박의 이유와 추천시점 필수조건은 무엇인가 | 004 축의 질문에 대응하나 값의 자료유형이 다름 | 참여자의 반박 관측을 연구자의 기능검증으로 바꾸지 않는다. 엄격 근접오답에는 조건·시점·발화자·특정 방안의 연결이 필요하다. | V11 §5·v1.3; V12 near_misses/rejection_codes | 제품 사실의 참 미확인(당시 버전 근거 필요) |
| 011 | M / C / P / LIC / TRUST / UX / EXP / OTHER | 유지보수·커뮤니티·가격·사용권·신뢰·편의·경험·기타 선택 이유인가 | 004 H에 포함되는 것은 추천 전에 필수였을 때만 | 사후의 선호·비용 이유를 모든 경우H로 흡수하면 원래 요청을 바꾼다. 같은 이유도 긍정·부정 방향이 다를 수 있다. | V11 §5 | 없음 |
| 011 | present / absent / explicit_unknown / undecided / not_applicable / unknown; I1 captured | 정보가 어떻게 드러나거나 빠져 있는가(근거 충분성의 입력 상태) | 001의 미입력·모름·미정·해당없음과 좁게 대응 | absent는 열람 범위의 부재, unknown은 노출·시점 불명이다. captured는 연구자의 URL 확보이지 질문의 충실성이다. | V11 §1–2 | 없음 |
| 011 | accessible / redirected / archived / failed / blocked / not_linked | 현재 단회 열람에서 링크에 무엇이 관측됐는가 | 004 L의 일부 근거 | blocked와failed를 같은 링크 소실로 취급하지 않는다. archived가 모든 설치의 중지나 근거 무효를 뜻하지 않는다. | V11 §6; V12 link_status_now | 지속 상태 미확인(다른 시점 재관측 필요) |
| 012 | product / component / principle / other | 자료집 항목을 어떤 산출물/역할군으로 집계하는가(판정 메타데이터) | 011 role과 일부 겹침,004 role과 조건부 연결 | 자료당 한 역할은 질의별 기여와 다르다. role은 검색어에 쓰지 않았고,other도 자동 무관 판정이 아니다. | V13 대상과 대표 주소; entries.jsonl.role | 없음 |
| 012 | 2 | 이 질의·대상·요청 역할의 필수조건에 문서화된 경로가 있는가(검색 관련성) | 004 DIRECT_DOCUMENTED가 주 대응; 일부 좁은 CONDITIONAL_TRANSFER도 가능 | 전체 프로젝트 완성품에만 부여하지 않는다. 선택 부품이나manifest의 좁은 원리도2가 된다. | V14 판정 단위·투영표; V15 P04.2/ct-merkle | 없음 |
| 012 | 1 | 일부 기능·조건부 적용·전이·실패 경계가 유용한가(검색 관련성) | 002 조건부 유지;004 CONDITIONAL_TRANSFER 및 부분 INSUFFICIENT | 근거 부족 일반값도, 후보 형태 component도 아니다. 어떤 부분을 도울지 확인해야 한다. | V14; V15 P01.w/yjs·P04.w/ct-merkle | 없음 |
| 012 | N | 가까워 보이지만 이 질의의 구체 조건을 어기는가(검색 관련성+적용 가능성) | 004 mismatch의 근접조건 위반 일부;010 near_miss | 접근 실패·자료 부족만으로N을 주지 않는다. 011의 실제 반박 사건을 요구하지 않는 연구자 판정이다. | V14; V15 K02.w/paperless-ngx; V17 등급 정의 | 없음 |
| 012 | 명시 0 | 이 고정 근거에서 관련1/2나근접오답N을 주었는가(검색 관련성) | 직접 일대일 대응 없음 | Jiandu0은 평가·배포 근거 보류다. 다른0에는 제목·범주만 있는 경우가 있어 부적합 기능검증으로 읽을 수 없다. | V15 P1.w/jiandu·P04.2/borg; V17 등급 정의 | 새 근거 뒤 등급 미확인(대상 원문 보강 필요) |
| 012 | 미판정(행 부재); 평가에서 결손을0으로 처리 | 이 쌍을 명시적으로 판단했는가, 계산상 어떻게 다뤘는가(판정 범위) | 004 unknown/INSUFFICIENT와도 직접 동치 없음 | 계산용0과 의미상0/N은 다르다. 내부별도표에 없는 쌍도 해당 비교에서는 미판정으로 보존한다. | V13 고정 비교; V14; V18 | 개별 미판정의 실제 관련성 미확인(추가 판정 필요) |
| 012 | origin=transfer / new | 등급을 선행자료에서 옮겼는가, 이번에 작성했는가(출처 지위) | 010 new_candidate와 직접 대응 없음 | transfer는 분야 간 전이T가 아니라 판정의 출처다. new는 새로운 제품이나 원리를 발명했다는 뜻이 아니다. | V14 끝 문단; V15 origin | 없음 |

### 표 4 — 주장 표

| 주장 | 근거 자료 주소 | 확인한 내용 | 반증 시도 | 미확인 |
| --- | --- | --- | --- | --- |
| 이 표본의 Po 우세안은 011·012 S1, 004 S2다. 보편 우승안은 아니다. | [evidence/agreement.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/agreement.json) | S1 94/120·59/60, S2 18/18; κ와 95% 구간을 함께 계산했다. | 012 무작위 연결 층·S3 축별·012 상위 문제 cluster로 다시 비교했다. | 미확인(새 실제 제안과 사람 코딩으로 재현) |
| 011 원값과 같은 120개를 비교해야 한다. | [sample/baseline.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/sample/baseline.json); [evidence/agreement.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/agreement.json) | 원 149는 75/149=50.34%; 같은 120은 66/120=55.00%; 새 S1은 94/120. | 새 S1 − 원 120 Po 차이 +23.33pp의 cluster 구간 [−7.00,+46.55]pp는 0을 포함한다. | 미확인(코드북 효과와 코더·요약 효과 분리) |
| 후보 속성형이 잘 맞는 영역도 있다. | [evidence/agreement.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/agreement.json); [M09](https://files.eric.ed.gov/fulltext/ED413903.pdf) | registry-origin 27개 S1 27/27; 서지 main-entry 99/106의 높은 일치도 확인했다. | 문맥 상대성이 있으니 S1은 무용하다는 결론을 검토했다. registry S2는 25/27이나 κ=0이다. | 미확인(문제 자체를 가린 S1 재코딩; 현 코더는 문제를 보았다) |
| 문맥·두 축을 추가해도 경계 불일치는 남는다. | [coding/adjudication.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/coding/adjudication.json); [M01](https://informationr.net/ir/16-4/paper502.html) | T036 S2 17/28·S3 16/28; T041 S3 5/11. M01에서 세밀한 도구가 단순 목록보다 높은 일치를 보장하지 않았다. | reference/comparison 규칙 적용 비대칭(A 0/B 14)과 document/data 경계를 따로 추적했다. | 미확인(새 코드북의 우선 규칙을 새 표본에서 검증) |
| S3 결합과 S2를 같은 난도로 비교할 수 없다. | [evidence/agreement.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/agreement.json); [M09](https://files.eric.ed.gov/fulltext/ED413903.pdf) | 011 form 94/120, contribution 85/120, joint 75/120. joint는 두 축의 교집합이다. | S3 κ 0.561 > S2 κ 0.538인데 Po는 낮은 이유를 Pe 0.146/0.369로 확인했다. | 미확인(두 축 기록의 사용자 효용·코딩 비용) |
| 기존 SBOM도 사용 문맥을 일부 표현한다. | [S01](https://spdx.github.io/spdx-spec/v3.0.1/model/Software/Vocabularies/SoftwarePurpose/); [S02](https://spdx.github.io/spdx-spec/v3.0.1/model/Software/Classes/SoftwareArtifact/); [S03](https://cyclonedx.org/docs/1.7/json/) | SPDX 목적은 사용 관점이며 추가 목적을 허용한다. CycloneDX는 type 외 scope/isExternal/구성 관계를 둔다. | 기존 체계가 고정 본질만 표현한다는 가정을 원 schema로 반박했다. | 미확인(이 필드들만으로 특정 문제의 whole/part를 완전 표현할 수 있는지) |
| 문제 상대 역할과 안정적인 형태는 공존할 수 있다. | [S15](https://www.cooperativepatentclassification.org/cpc/definition/C/definition-C08L.pdf); [S17](https://www.loc.gov/marc/bibliographic/bd655.html); [S18](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-03); [S21](https://www.oreilly.com/library/view/pattern-oriented-software-architecture/9781118725269/9781118725269_c04.xhtml) | CPC 기능/용도 동시 분류, MARC 형식/주제 구분, PICO I/C 위치, pattern/idiom 겹침을 확인했다. | 각 분야가 한 대상에 단일 고정 역할을 강제하는지 읽었고 복수 축·관계 위치·범위 규칙을 확인했다. | 미확인(이 네 분야의 규칙을 소프트웨어 추천에 그대로 이식한 성능) |
| 50.34%를 다른 색인 연구의 overlap과 비교해 보통이라고 정당화할 수 없다. | [M01](https://informationr.net/ir/16-4/paper502.html); [M10](https://www.researchgate.net/publication/235290123_Inter-indexer_consistency_in_graphic_materials_indexing_at_the_National_Library_of_Wales); [M14](https://yunus.hacettepe.edu.tr/~tonta/yayinlar/indxcons.htm); [M15](https://www.ideals.illinois.edu/items/4065/bitstreams/14485/data.pdf) | 색인어 집합 겹침과 단일 명목 라벨 정확 일치는 분모·판정 질문이 다르다. 원 011 κ는 0.382다. | 낮은 색인 일치·높은 main-entry 일치·GitHub topic alpha 0.68을 함께 비교했다. | 미확인(Hooper 1965·Markey 1984 지정 원문을 정상 공개 경로로 확보) |
| 30개 역할 불일치에서 고정 단위의 문서 판정은 유지할 수 있었다. | [evidence/impact.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/impact.json); [V06](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md) | 수기 공통 판정의 역할별 재사용 감사 0/30 변화; 실패 1·INSUFFICIENT 14·라벨 미부여 15. | prefer→must, part→요구 면제, 역사적 기능→현재 사실, 빈 proposal→단독 전체 주장을 사례별 배제했다. | 미확인(독립 H/T 재코딩과 사람에게 보여 주는 역할 표지의 인과 효과) |
| 역할을 적합성 필터로 쓰면 문서상 적합 후보도 잃는다. | [evidence/role-filter-counterexample.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/role-filter-counterexample.json); [V07](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/EXPECTED.json) | S1 product-only 규칙은 두 코더 모두 DIRECT 7개 중 3개를 제외한다. A의 통과 7개 중 mismatch 2개, B의 통과 8개 중 3개다. | S2 whole-only도 15개 중 mismatch 6개를 통과시켰다. 잘못된 두 필터를 고정 18행에 직접 적용했다. | 미확인(실제 사용자 손실; 현재는 연구자 규칙의 계산 반례) |
| 동일 후보의 관련성은 질의에 따라 바뀐다. | [V15](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/qrels.tsv); [V14](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/NOTES.md) | Paperless-ngx K02.1=1, K02.2/K02.w=N; ct-merkle P04.w=1/P04.2=2. | 같은 후보면 한 관련성 등급을 갖는다는 대응을 실제 qrel 행에서 반박했다. | 미확인(이전 qrels의 외부 금표준 타당성; 연구자 판정으로 한정) |
| mapped·보류·INSUFFICIENT·미판정은 단일 상태로 합치면 안 된다. | [V04](https://github.com/laadkke-arch/agentflow-open/blob/b13db3931b4021ff9e1ac6e404590c09526c3087/docs/workstreams/research/AF-RES-003/RESEARCH.md); [V06](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md); [V09](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/p1-judgments.json); [V10](https://github.com/laadkke-arch/agentflow-open/blob/0603f0d2990c7a501dbdfc45fbbba79155f505fc/docs/workstreams/research/AF-RES-010/evidence/p2-judgments.json); [V15](https://github.com/laadkke-arch/agentflow-open/blob/cb602858378db90adb1f085953016267f9afbd6d/docs/workstreams/research/AF-RES-012/qrels/qrels.tsv) | 010 mapped 13/25 중 3개는 mismatch; 003 보류는 동일성, 004 INSUFFICIENT는 적용 근거, 012 미판정은 질의 쌍 판정 부재다. | 철자가 비슷한 어휘를 같은 질문으로 읽을 수 있는지 42행과 7 구체 반례를 대조했다. | 미확인(대응표가 실제 독자의 오독을 줄이는지) |
| project/package라는 명칭만으로 완성품/부품을 결정할 수 없다. | [S07](https://libraries.io/api); [S08](https://raw.githubusercontent.com/librariesio/libraries.io/335f0b0c82b3785c8aa8c418f6592ef0cc7e1f0c/app/models/project.rb); [S09](https://raw.githubusercontent.com/ecosyste-ms/packages/3d09272099381444a65a73d89cfe2682af87ef05/README.md); [S10](https://raw.githubusercontent.com/ecosyste-ms/packages/3d09272099381444a65a73d89cfe2682af87ef05/app/models/package.rb) | Libraries.io Project는 package와 versions를 다루고 ecosyste.ms는 저장소와 배포 package를 구별한다. | package면 component, project면 product라는 가정을 API 설명과 고정 모델 코드로 대조했다. | 미확인(모든 생태계의 배포물 경계를 동일 규칙으로 적용할 수 있는지) |
| 최소 문헌 수는 충족했지만 지정 고전 원문 일부는 미확인이다. | [sources.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/sources.json); [evidence/source-audit.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/source-audit.json); [evidence/reliability-supplement.json](https://github.com/laadkke-arch/agentflow-open/blob/146805164c24781115d4e5ac5562921242ddd51a/docs/workstreams/research/AF-RES-016/evidence/reliability-supplement.json) | 방법·체계 직접 본문 38건 중 핵심 36·사이트 상한 후 34 계상; 별도 후속 후보 문서 3. 지정 고전 2편은 미확인으로 분리. | 동일 사이트 상한을 GitHub Pages/raw까지 합치고 실패·snippet 52 기록을 최소 수에서 제외했다. | 미확인(Hooper·Markey 원문; Cohen 1960 원문도 읽었다고 계상하지 않음) |

표 1은 원 198단위와 동결 두 코딩의 값이다. S3는 형태 × 기여의 정확 결합이며 기여 축은 S2와 같다. 95% 구간은 011 스레드 15·012 질의 31·004 문제 4개의 5,000회 cluster bootstrap으로, 작은 편의표본에서 모집단 coverage를 보장하지 않는다. 004의 [1,1]은 관측 18/18을 재표집한 퇴화 결과다. 표 2는 **작업자가 작성한 사후 문서 판단(H)**을 두 역할 조건에 재사용한 감사이며 독립 H/T 실험이 아니다. 같은 역할이 다른 판단 단위로 읽히는 경우는 별도 가정으로 분리했다. 표 3은 원 어휘의 대상·범위가 맞는 경우에만 연결하는 해석이며 자동 변환 규칙이 아니다. 출처 ID의 URL·절·한계는 [sources.json](sources.json)에 있다.

## §2 세부 질문별 답

### Q1. 기존 체계는 무엇을 분류하는가

**하나의 보편적 ‘역할’ 축이 아니다.** SPDX는 일반 사용 목적, CycloneDX는 구성요소 유형과 포함/사용 관계, PyPI는 Framework/Topic 같은 복수 검색 facet, Debian은 배포 package의 role와 별도 scope, Libraries.io·ecosyste.ms는 project/package/repository의 관측 단위, Wikidata는 instance/subclass/part 관계, CPE는 application/OS/hardware 제품 구분을 다룬다. [S01–S13; SCHEMES §1](SCHEMES.md)

SPDX의 primary purpose만 고집할 필요는 없고 추가 목적을 기록할 수 있다. CycloneDX는 핵심 기능이 framework인 경우 library보다 framework를 택하는 규칙과 scope를 별도로 제공한다. Debian의 개발 library/shared-library/plugin은 모두 package 경계를 전제로 하며, PyPI의 Framework 태그는 해당 프로젝트가 framework라는 형태 판정과 다르다. Wikidata에서 part-of를 subclass로 읽는 것도 잘못이다. 이런 경계 처리 자체가 library/app/plugin의 중첩을 인정한다. 공식 의미 규칙(D1)과 고정 모델 코드(D2)를 함께 대조했다. 후보의 형태와 이 문제에서의 기여를 같은 필드에 넣기 전에 후보가 저장소·배포물·서비스·하위 기능 중 무엇인지 정해야 한다. 이것은 최종 DB 계약이 아닌 연구자 권고(H)다.

### Q2. 다른 분야는 같은 대상의 맥락별 역할을 어떻게 다루는가

네 분야는 서로 다른 해결 방식을 보였다. CPC는 기능 분류와 적용 분류를 상호 배타적인 철학으로 두지 않는다. 실제 C08L/C09D 지침에서 코팅 용도만 청구하면 C09D, 조성물 자체와 코팅 용도 모두를 청구하면 C08L과 C09D 양쪽 분류를 허용하고 검색은 관련 양쪽을 본다. [S14–S16](SCHEMES.md)

MARC 655는 자료의 장르/형식과 주제 세분을 구별하고 자료의 어느 부분에 적용하는지도 표현한다. PICO는 같은 치료를 비교 설계 안의 Intervention/Comparison 위치로 둔다. 용량·시점의 비교도 가능하므로 I/C가 약 자체의 종류일 수 없다. 디자인 패턴·관용구·프레임워크는 추상도·구현 범위·확장 방식으로 구별하지만 POSA는 idiom과 design pattern의 겹침을 명시하고 framework는 부분 완성 구현과 확장 구조를 함께 가진다. [S17–S21](SCHEMES.md)

따라서 문제 상대성은 객체의 모든 속성이 맥락에 따라 변한다는 뜻이 아니다. 안정적인 배포/형식 정보와 문제 안의 위치, 여러 기능이 공존할 수 있다. 공식 분류 지침·서지 형식·임상 방법·저자 설계 문헌이라는 4종류의 1차 본문을 비교했다. 이 사례들은 S2/S3의 성공을 보증하지 않으며 그 검사는 Q6에서 별도했다.

### Q3. 50% 일치는 낮은가, 보통인가

011 원 149개를 재계산하면 75/149=50.34%, κ=0.382다. 고정 역할을 안정적으로 재현한다는 전제를 지지하기에는 약하다. 하지만 도서관 색인의 낮은 overlap을 기준으로 보통이라고 할 수도 없다. 색인어 집합의 교집합/합집합과 단일 라벨의 정확 일치는 서로 다른 측정이다. M01·M03·M09·M10·M14의 색인 실증 5건과 소프트웨어 topic 분류 M02, 내용 분석 방법 M04·M05·M11·M13을 구별해 읽었다. [AGREEMENT §7](AGREEMENT.md), [reliability-notes §2](evidence/reliability-notes.md)

상반된 사례도 있다. M09는 main-entry 99/106의 높은 일치와 subject 44/106의 낮은 일치를 동시에 보였다. M01은 설명·계층을 더한 색인 도구가 단순 descriptor list보다 높은 일치를 보장하지 않았다. M02는 동일 3,000 topic을 세 명이 판정해 alpha 0.68이지만 쌍별 0.52–0.79와 양성 빈도의 차이가 컸다. 기준은 보편 합격선 하나가 아니라 판정 목적·범주 분포·혼동 방향·후속 손해다. 0.667/0.8의 관례를 본 작업의 자동 통과선으로 채택하지 않았다. [M01·M02·M04·M09·M13]

### Q4. 세 분류안은 어떻게 정의했는가

| 안 | 질문과 값 | 경계 처리 | 적합한 용도와 이번 비교의 제약 |
| --- | --- | --- | --- |
| S1 후보 속성형 | product/component/principle/mixed/unknown | 독립 실행 완결 기능과 삽입 형태 구별; 복수 이름만으로 mixed 아님; 후보 설명만 사용하도록 지시 | 조밀한 색인·선명한 배포물; 문제 기여나 적합성은 표현하지 못함 |
| S2 문제 상대형 | whole/part/reference/comparison/none/mixed/unknown | 선택 범위 전체인지 묻고 whole을 프로젝트 전체로 확장하지 않음; 역할과 H 충족 분리 | 제안 사용과 선택 범위가 명시될 때; 평가 기준/reference 중첩이 남음 |
| S3 두 축 분리형 | form(app/service/library/framework/standard/document/pattern/research/data/mixed/unknown) × S2 contribution | 문서 URL과 실행 후보 구별; framework의 제어 흐름, service의 독립 실행; data 추가 이유 명시 | 이관·진단 시 어느 축에서 갈렸는지 보존; 결합 정확 일치는 더 엄격 |

[CODEBOOK.md](CODEBOOK.md)의 각 값에는 정의·포함/제외·표본 외 합성 경계 예 3개를 붙였다. SCOPE와 함께 코딩 전 커밋 `68d1ee68bf2b0a6e636970ce71c89d2bba2b9bd0`에 동결했고 원 코딩 뒤에 규칙을 고치지 않았다. 공식 schema의 facet 분리와 패턴/프레임워크 저자 문헌이 설계 근거이고, 실제 예의 재현 여부는 수치 표와 T036·T041 사례로 검사했다. [S01–S06·S20–S21; AGREEMENT §4]

### Q5. 이중 코딩은 어떻게 수행했는가

198단위(011 120 + 012 60 + 004 18)에 대해 각 코더가 3안을 모두 제출해 **594개 분류안별 대응쌍, 총 1,188개 응답**을 얻었다. S3의 form/contribution은 하나의 결합 응답으로 센다. 작업자 A의 동결 커밋 `0981732949cdea358c4ffa27aafd4ae50d310bbe`는 내부 별도 B 원응답 커밋 `674f1c8eb99e531acee7531c8f1495f721c4dffd`의 직접 부모다. B는 새 문맥에서 CODEBOOK과 표본만 읽었고 원판 라벨/A 코딩은 비공개로 두었다. 원 TSV와 JSON을 모두 보존했다. [coding/](coding/), [sample/](sample/)

이는 **같은 모델의 내부 별도 코딩**이다. 파일 접근을 OS에서 강제 격리한 것은 아니며 지시와 문맥을 분리했다. 작업자 A는 선행 라벨에 노출됐고, 양쪽 일부 행에서 후보 이름 지식의 보충을 스스로 밝혔다. 따라서 사람 간 재현성을 직접 측정한 것으로 표현하지 않는다. 대표 사례는 011-T053-002의 형태 unknown 대 library와 004-R03의 규격 대 절차 해석이며, 코딩 실패나 결측으로 행을 빼지 않았다.

### Q6. 어느 안이 더 일치하고 왜 갈리는가

표 1의 Po 점추정은 011에서 S1 78.33% > S2 70.83% > S3 62.50%, 012에서 98.33% > 90.00% > 85.00%, 004에서 S2 100% > S1=S3 94.44%다. **이번 표본의 Po 점추정은 S1이 항상 열등하다는 주장을 지지하지 않는다.** 동시에 S3는 두 축 결합이라 낮은 Po가 정의상 예상되고, 형태만 보면 011 78.33%다. S3 정보 구조의 쓸모와 결합 일치의 우열을 분리한다. [AGREEMENT §§1·5]

59개 고유 불일치의 사후 지배 진단은 경계 정의 부족 35·문맥 부족 18·실제 다의성 6이다. T036의 comparison 기준 적용이 대표적인 경계 문제이고, otel-wal은 금지 조건만 남은 문맥 부족, T054-003은 모델과 설정 조언이 함께 있는 복수 대상이다. 내부 별도 진단 원본과 작업자 수용/유보 메모를 남겼으며 합의값으로 A/B를 고치지 않았다. [coding/adjudication.json](coding/adjudication.json)

011 같은 120의 원 55.00% 대비 S1 점증가는 23.33pp지만 차이 95% 구간은 [−7.00,+46.55]pp다. 기존 149의 50.34%를 직접 분모로 한 개선 주장은 하지 않는다. 012의 무작위 연결 36개는 S2 34/36이나 κ 0.321로 높은 none 일치가 큰 몫을 한다. 이 반례까지 보면 새 기준이 항상 우월하다는 주장도 성립하지 않는다. [AGREEMENT §§3–4]

### Q7. 불일치가 실제 판정을 바꾸는가

30개에서 동일 단위의 판정을 유지할 수 있는지 사례별 검토했다. 기록된 0/30은 공통 수기 H/T 판정을 역할별 표시에 재사용한 **문서 감사**다. 알려진 실패 1개(R03), INSUFFICIENT 14개, 라벨 미부여 15개(조언/비교 10·필수 판정 기준 부족 대안 5)의 구성을 함께 보고한다. 역할 표지가 사람이나 판정 모델에 미치는 효과가 0이라는 실험 결과는 아니다. [IMPACT §§1–3](IMPACT.md), [impact-independent-review.md](evidence/impact-independent-review.md)

R03에서 standard/pattern은 같은 순서 의존 실패를 바꾸지 않고, 목록 document/data나 비용 조언 reference/comparison 차이는 고정 사용에서 H 면제나 성공 근거가 되지 않았다. 반대로 SQLite/Postgres 큐의 실행 부품 대 참고 관계 해석은 proposed_use가 달라질 수 있다. 이를 T not_needed 대 analogy_only의 **추가 가정 2개**로 기록했지만 원 패킷에는 실제 의도가 없어 관측 변화로 세지 않았다. [IMPACT §4]

정확한 형태 라벨도 판정을 그르칠 수 있는 오용 경로는 계산으로 확인했다. product-only 필터는 004의 DIRECT 7개 중 component인 3개를 놓치며, A의 product 통과 7개 중 알려진 mismatch 2개, B의 통과 8개 중 3개가 남는다. whole 필터도 15개 중 mismatch 6개를 남긴다. 따라서 역할은 발견·설명 정보로 쓰되 H/T를 대신하지 않게 하는 조건이 필요하다. 이것은 실제 사용자 시험이 아닌 고정 판정 팩에 대한 반사실 규칙 계산이다. [IMPACT §5]

### Q8. 어휘는 어떻게 대응해야 하는가

42행을 동일성/적용 가능성/근거 충분성/전이/검색 관련성에 따라 대조했다. 입력의 확정 상태·사용자 반응·탐색 중단처럼 이 5질문 바깥의 지위도 억지로 합치지 않았다. 003의 보류는 동일성의 보류, 004 INSUFFICIENT는 특정 사용의 결정 근거 부족, 012 미판정은 질의–자료 쌍에 판정 기록이 없는 상태다. 001 proposal_unconfirmed는 사용자 확인 여부이고 002 중단은 탐색 행위라 모두 다르다. [VOCAB_MAP §§2–3](VOCAB_MAP.md)

010에서 mapped 13/25 중 3개는 알려진 mismatch다. 대응 관계를 설명한 것만으로 전이안이 좋지는 않다. 012 Paperless의 1/N/N과 ct-merkle의 1/2는 후보 동일성과 검색 관련성의 분리를 보여준다. 011의 게시물 accepted와 그 안 개별 제안 반박도 동시에 존재할 수 있다. 프로토콜/정의 문서와 실제 고정 판정 JSON·TSV라는 두 종류를 읽어 이 대응을 검사했다. [VOCAB_MAP §4; V04·V06–V07·V09–V10·V12·V15–V16]

## §3 추가 분석

### 3.1 세 안의 적합 조건과 실패 조건

| 안 | 적합할 수 있는 조건 | 실패하기 쉬운 조건 | 이 작업이 뒷받침하는 범위 |
| --- | --- | --- | --- |
| S1 | 배포물·독립 서비스·문서의 경계가 명시되고 거친 색인이 목적일 때 | 하위 기능과 제품 전체가 섞인 후보; 특정 문제의 대체 가능성을 추정할 때 | 012 59/60·registry 27/27라는 내부 일치; 사람/문맥 가림 검증은 아님 |
| S2 | 문제의 선택 범위와 제안 사용이 명시되고 그 기여를 표시할 때 | 목표 없는 부정 제약; 비교 기준과 참고 방법 중첩; 기여를 기능 충족과 혼동할 때 | 004 18/18의 명시된 구성; 실제 발화 011은 85/120 |
| S3 | 형태와 기여를 별도 설명·인계하고 불일치 원인을 추적할 때 | 문서/data·app/service 경계 부족; compound 후보; joint 점수를 단일 축과 순위화할 때 | 011에서 형태 일치 94와 기여 일치 85를 분리해 남길 수 있음; 사용자 효용은 미측정 |

어떤 안도 최종 확정하지 않는다. 현 근거로는 형태 정보를 기여·판정과 구별해 보존할 이유가 있고, 저장·표시의 세분화 정도는 사용 목적과 코딩 비용으로 다시 평가해야 한다. 기존 004는 이미 proposed_use를 판정 단위에 넣었다. 이 결과는 새 H/T 축을 제안하는 것이 아니라 그 사용 단위를 역할 라벨 뒤에 숨기지 말라는 조건을 보강한다.

### 3.2 요구된 반례 다섯 가지

| 반례 요구 | 실제 사용한 조사·검사 | 찾은 결과 | 주장 범위 |
| --- | --- | --- | --- |
| 문제 문맥 없이도 거의 일치할 역할 | Debian role/CPE part 조사(S06/S13); registry URL 층의 S1 | 27/27 일치(component 26/product 1) | 후보 정보만 쓰라는 지시하의 반례. 문제를 실제로 가린 재실험은 미실시 |
| S2/S3에도 낮은 일치 | T036·T041 cluster별 재계산, M01 상세 도구 반례 | T036 S2 17/28·S3 16/28; T041 S3 5/11 | 실제 다의성 6/59와 규칙 적용 문제를 분리. 전부 본질적 다의성이라고 하지 않음 |
| 역할 불일치가 판정을 안 바꾸는 영역 | 30개 고정 사용 감사; R03·T036·T041의 요구 대조 | 라벨별 공통 판정 유지 0/30 변화 | 문서 감사이며 unknown 보존이 많음. 실제 사용자 효과는 미확인 |
| SPDX/CycloneDX의 문제 상대 표현 | SoftwarePurpose usage/SoftwareArtifact additionalPurpose, component scope/isExternal 확인 | 일반 사용 목적·추가 목적·환경/조립 관계가 이미 존재 | 특정 문제의 whole/part를 완전히 대체한다는 뜻은 아님 |
| 역할 표시가 판단을 그르치는 경우 | 고정 18행에 product-only와 whole-only 가정 필터 적용 | product-only가 DIRECT 3/7 누락, whole-only가 mismatch 6/15 통과 | 실제 규칙 적용 계산 반례; 사람의 화면 실수 관측은 아님 |

체계·방법 반증 질의는 [schemes-notes](evidence/schemes-notes.md), [reliability-notes §5](evidence/reliability-notes.md), [reliability-supplement](evidence/reliability-supplement.json)에 보존했다. 실행 반증은 고정 시드·ID·스크립트와 결과 파일로 남겼다.

### 3.3 분류 체계 설계자·색인자·방법론자·추천 사용자 관점

체계 설계자는 후보 ID가 가리키는 배포/소스 단위와 복수 facet의 의미를 명시할 수 있다. 색인자는 기준을 더 상세히 써도 항상 더 일치하지 않으며 주요 대상을 무엇으로 고르는지가 문제임을 보여준다. 내용 분석 방법론은 주변 분포와 체계적 편향, 복수 필드 결합, cluster 구조를 보지 않은 headline 계수를 경계한다. 추천을 받는 설계자는 ‘부품’이라는 형태를 보고 전체 대안에서 제외하거나 ‘전이 설명 있음’을 보고 필수 조건을 승인하면 손해를 입을 수 있다. 마지막 관점은 이번 필터 반례와 문서 감사에서 얻은 설계 가설이지 인터뷰나 제품 사용 시험이 아니다. [S01–S13; M01·M09·M13; IMPACT §5]

### 3.4 판정 상태를 보존하는 조립 원칙(H)

원 작업·원 어휘, 그 어휘가 답하는 질문, 판정 대상, 문제·선택 범위, proposed_use·설정, 근거 위치·시점·수준, 판정자, 미확인과 다음 확인을 함께 남기는 것을 제안한다. 원 라벨을 공통 라벨로 덮어쓰지 않는다. 이는 어휘 대응의 정보 손실을 줄이는 연구 제안이며 공통 색인·DB/API 계약은 이번 작업에서 변경하지 않았다.

## §4 가장 중요한 불일치·약점 3건과 다음 조사 제안

### 1. S2의 낮은 점수에는 코드북 적용 비대칭과 과제 차이가 섞여 있다

**무엇이 어긋나거나 약한가:** A는 011에서 comparison을 0개, B는 14개 사용했다. comparison 정의는 명시적 기준도 포함하지만 A는 여러 기준을 reference로 읽었다. S3는 S2를 한 축으로 공유하는 결합 응답이므로 세 안이 독립된 동일 난도 처치도 아니다.

**근거 위치:** AGREEMENT §§4.2·5, agreement.json의 011 S2 주변 분포, adjudication.json의 T036-005·014·022.

**이것이 틀리면 바뀌는 결론:** 비교 기준 우선 규칙을 맞춘 새 표본에서 S2가 상승하면 현재의 S1>S2 점순위는 분류안 본질보다 작업자 적용 차이였다. 반대로 엄격화해도 낮으면 실제 경계 중첩의 비중이 커진다.

**다음 조사 제안:** “비교 기준/설계 참고의 우선 규칙을 고정하면 실제 새 표본의 일치가 오르는가?” 새 코드북 버전·표본 외 훈련 예·새 비용/기준 30개와 실행/정보원 30개, 최소 60단위와 독립 사람 코더 3명이 필요하다. 원 198개는 재훈련 평가에 쓰지 않고 A/B 원판을 보존한다.

### 2. 실제 추천 문맥의 재현성을 표본 구성과 후보 단위가 제한한다

**무엇이 어긋나거나 약한가:** 012의 36/60은 무작위 질의 연결이며 S2 none의 일치가 높다. 011은 T036/T047이 65/120이고, 004는 의도적으로 명시한 합성 4문제다. 실제 같은 후보의 여러 문제 반복도 희소하고 후보 단위가 실행물·문장·묶음으로 섞인다.

**근거 위치:** sample/selection.json, design-audit.md, agreement.json의 strata_012·small_repeated_target_checks; AGREEMENT §§2·4.3·8.

**이것이 틀리면 바뀌는 결론:** 실제 제안만 남기고 후보 단위를 맞췄을 때 S1/S2 순위가 바뀌면 현재 차이는 문제 상대성보다 쉬운 음성 연결·요약 단위 때문이다. 좁은 질의의 높은 일치를 실제 검색 환경 성능으로 옮길 수 없다.

**다음 조사 제안:** “같은 배포물의 형태를 고정하고 실제 문제 3개를 바꾸면 기여 역할만 바뀌는가?” 후보 30개 × 실제 제안 문맥 3개 = 최소 90단위, 최소 30개 독립 문제 묶음, 후보 배포 정보와 각 제안의 사용·설정을 명시한 자료가 필요하다. 문맥 가림 S1과 문맥 제공 S2/S3의 순서를 무작위 배정한다.

### 3. 사람 간 재현성과 역할 표시의 판단 효과는 아직 측정하지 않았다

**무엇이 어긋나거나 약한가:** 두 코딩은 같은 모델의 내부 별도 코딩이며 A는 선행 라벨을 읽었다. Q7의 0/30은 공통 수기 판정의 재사용 감사이고, 1개 실패 외에는 근거 부족/라벨 미부여가 많다. product 필터 반례도 사람의 실제 실수를 관측한 것이 아니다.

**근거 위치:** coding/coder-a-freeze.json·coder-b-provenance.json; IMPACT §§1·5·6; impact-review-response.json.

**이것이 틀리면 바뀌는 결론:** 사람이 서로 다른 관점으로도 같은 형태/기여에 동의하거나 역할 표지가 H 위반 누락을 크게 줄이면 내부 일치보다 실용성이 높을 수 있다. 반대로 표지가 범위 면제·후보 누락을 늘리면 현재의 분리 표시 권고도 더 제한해야 한다.

**다음 조사 제안:** “명시된 사용과 충분한 근거를 고정했을 때 역할 표지가 H/T 오판을 줄이는가?” 실제 불일치 30개와 조건별 판정 근거를 준비하고 표시 없음/A/B의 3조건을 배정한다. 최소 90개 판정 노출, 사람 평가자 3명 이상, 같은 평가자에게 동일 사례의 다른 표지를 반복 노출하지 않는 설계가 필요하다. 원 역할 코딩을 보지 않은 판정과 근접 오답 누락/불필요 제외를 함께 기록한다.

## §5 한계

이번 결과는 고정 시점의 연구 요약·내부 코딩·문서 판정이다. 공개 사이트의 현재 제품 지원 범위를 포괄하지 않고 실제 후보 통합(D4)을 하지 않았다. 인간 색인자 모집단이나 새 모델에 대한 일반화, 역할 표시의 인과 효과, 정답 qrels의 외부 타당성은 남아 있다. 높은 일치가 곧 맞는 판정은 아니며 같은 잘못된 가정에도 두 코더가 동의할 수 있다.

방법·체계 본문은 38건을 직접 읽었고 그중 핵심 36건, 동일 사이트 상한을 보수적으로 적용한 최소 개수는 34건이다. 후속 후보 검증 본문 3건은 이 최소 개수에 더하지 않았다. 소프트웨어 공식 8체계, 다른 분야 4종, 색인 실증 5건, 소프트웨어 실증 1건, 지표 문헌 7건을 포함한다. 실패·차단·snippet만 본 52개 시도는 제외 목록에 있다. [sources.json](sources.json), [source-audit.json](evidence/source-audit.json)

**Hooper 1965와 Markey 1984의 지정 원문은 미확인이다.** 최초 조사에 이어 32개 질의·10개 공개 URL을 추가 시도했으나 본문을 확보하지 못했다. Leonard 1977은 직접 읽었고 다른 색인 실증 5건으로 최소 개수는 충족하지만, 지정 고전 2편을 읽었다고 대체 계상하지 않는다. Cohen 1960 원논문도 미열람이며 Cohen 1986 저자 회고와 다른 방법 원문을 구별했다. 정상 공개 기관 스캔/저자판을 확보해 표지·측정식·표본·결과 절을 대조하는 것이 이 문헌 공백을 해소할 최소 행동이다. [reliability-supplement.md](evidence/reliability-supplement.md)

세 안 중 하나를 확정하지 않는다. 현재의 결론은 **후보의 형태를 표시하는 일과 이 문제에서의 기여를 표시하는 일을 구별할 근거는 있지만, 그 구별을 더 세분하면 항상 더 잘 일치하거나 더 좋은 판단을 한다는 증거는 없다**는 범위에 머문다.

