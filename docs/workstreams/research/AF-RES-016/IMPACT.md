# AF-RES-016 — 역할 불일치가 판정을 바꾸는가

## 1. 결과와 해석 범위

59개 불일치 단위를 정렬하고 균등 간격으로 고른 **고유30개**를 검토했다. 같은 문제·후보·제안 사용·설정·근거를 고정한 작업자 문서 재판정에서는 **역할명만 달라서 H/T 또는 근접 오답 여부가 바뀐 경우는0/30**이다. 구성은 알려진 실패1개, 근거 부족14개, 전체 판정 라벨 미부여15개(조언·비교10개, 필수 판정 기준이 부족한 실제 대안 제안5개)다. 이는 사람에게 역할 표지를 보여 주었을 때의 인과 실험이 아니다. 많은 unknown이 그대로라는 결과를 충분한 근거 아래 무영향이 입증된 것으로 세지 않는다.

A/B 때의 H/T 판단은 원 A/B 코더가 별도로 제출한 값이 아니다. 사례별로 양쪽 역할의 의미와 같은 요구·근거를 대조한 뒤 수기 판단 하나를 양쪽 표시에 재사용했다. 따라서0/30은 두 H/T를 독립적으로 재코딩한 실험에서 얻은 변화율이 아니다. **작업자 GPT-6 Astra Pro가 동결한 두 역할을 조건으로 작성한 사후 문서 판단(H)**이다. 004-R03의 고정 연구자 기대판정과 I01–I03 후속 공식 본문을 참조했다. 실행한 것은두 toy 반례와 잘못된 역할 필터의 계산뿐이며 실제 후보 설치·통합 성공을 주장하지 않는다.

## 2. 비교 방법

004의 단위 `문제 × 후보 × 제안한 사용 × 설정 × 제공 근거`를 유지했다. `part/reference`라는 라벨만으로 원 must를 `not_in_scope`로 지우지 않았다. `prefer`를 must로 올리지 않았고, `force=unclear`이면 정확한 요구를 만들어 넣지 않았다. 원 proposal이 비어 있는012 후보에는 '이것만으로 전체 충족'이라는 주장을 추가하지 않았다. [고정004 PROTOCOL](https://github.com/laadkke-arch/agentflow-open/blob/2b798c7d2b7355b649691c18de196104ceabb0f0/docs/workstreams/research/AF-RES-004/PROTOCOL.md)

선택 ID는 [impact-selection.json](evidence/impact-selection.json)에 동결 후 규칙대로 보존했다. 59개 중 순서통계 인덱스 `round(i×58/29), i=0..29`로30개를 골랐다. 영향이 큰 행만 고른 표본은 아니나 모집단 무작위 추출도 아니다. 각 행의 이유·반박 검토·최소 다음 확인은 [impact.json](evidence/impact.json), 수기 판단을 직렬화한 원 스크립트는 [build_impact.py](evidence/build_impact.py)에 있다.

`H: must 미제공/unclear`는 pass가 아니다. `전체 판정 라벨 미부여`도004의 새로운 상태값이 아니다. 조언·비교10개와 필수 판정 기준이 부족한 실제 대안 제안5개에 전체 적합 라벨을 붙이지 않았다는 설명이다. `N 미입증`은 관련성0이나 적합 판정과 다르다.

## 3. 30개 고정 사용 비교

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

### 3.1 대표 사례의 실질 검사

**R03:** 표준인지 패턴인지 다르지만 같은 도착 순서 구성을 평가한다. local 수정은pass, log에서 본문 복원은unknown, 순서 무관 수렴은fail이다. 동일 초기문서에 A/B replace를 역순 적용해 실제 toy trace가 서로 다른 최종값을 냈다. 표준/원리라는 형태가 기능 보증을 대신할 수 없다. [I03](https://www.rfc-editor.org/rfc/rfc6902.html), [toy-counterexamples.json](evidence/toy-counterexamples.json)

**T036 비교 기준6행:** 비용·선택법을 reference로 볼지 comparison으로 볼지 다르지만, 보안·총비용은prefer이고 구체 구현 승인 주장은 없다. 기준을 제시했다는 것과 기준에 합격했다는 것은 다른 사실이다. 이 범위의 역할 불일치는 H/T 판정을 바꾸지 않는 명명 차이에 가깝다.

**T027과 T010:** 부분 기여라는 라벨로 원래의 판매 제한·안전한 결제 조건을 삭제하지 않았다. 구현 연결이 없는 것은 두 역할 모두unknown이다. 별도 좁은 데이터층/UI층의 평가를 하려면 새 사용 행을 만들어야 한다.

**Briefpanel·Iggy·ZFS:** 내부망 사용, 복제, 한 디스크씩 증설을 원 입력의 새로운 must로 추가하지 않았다. 당시 댓글의 기능 한계가 현재 버전의 사실이라는 주장도 하지 않았다. 역할 변경보다 요구·관측 창을 바꾸는 오류가 더 결정적이었다.

**aiolimiter:** part와none 중 어디에 놓든 빈 proposal은 전체 상한 보장 주장이 아니다. 다만 '시간 기반 limiter만으로 처리중≤4를 보장한다'는 별도 가정은 반례가 있다. 1초마다 하나를 들이고 각 작업이10초 지속되면4.5초 시점에5개가 처리 중이다. 이 toy는 허용 스케줄의 계산이며 실제 라이브러리를 실행한 것은 아니다. [I02](https://aiolimiter.readthedocs.io/en/stable/)

**OTLP exporter:** 후속 공식 문서 I01은 Python SDK의 전송과 Collector pipeline의 후단 exporter 구성을 구별한다. 같은 exporter라는 이름이나 component라는 역할로 Collector 내구 queue 설정을 입증할 수 없다. 원 패킷만으로 방향을 확정했던 B의 배경지식도 동결 결과에 그대로 남겼다. [I01](https://opentelemetry.io/docs/languages/python/exporters/)

## 4. 역할 해석이 사용 단위를 바꾸는 조건부 대비

SQLite 테이블 큐와 기존 Postgres 테이블/확장 큐2개는 A의 실행 부품/whole 해석과 B의 방법/reference 해석이 다른 사용 단위를 가리킬 수 있다. 다음 대비는 **연구자가 새 가정을 붙인 H 예시**이고 주0/30의 분자에 넣지 않았다.

| 원 ID | 추가 가정 A | 추가 가정 B | 조건부 T 차이 | 보존할 H | 확인이 필요한 것 |
| --- | --- | --- | --- | --- | --- |
| 011-T039-009 | 이미 실행 가능한 큐 부품과 인터페이스를 직접 사용 | DB의 행을 메시지처럼 쓰자는 참고만 있고 claim/ack·중단 복구 대응 없음 | not_needed → analogy_only | OSS·ZooKeeper 금지는 유지; 실제 큐 보장 미확인 | 원 제안이 구현체인지 원리인지, 구체 연결·실패 조건 |
| 011-T047-018 | 실제 제공된 큐 확장을 기존 인터페이스로 직접 사용 | 기존 DB 관계를 새 큐 설계로 옮기자는 거친 비유 | not_needed → analogy_only | 필요한 신뢰성 값을 먼저 명시; pass 자동 부여 금지 | 기존 Postgres 전제와 확장 구현, 메시지 상태 대응 |

원 패킷에는 이 추가 가정이 없어 T는unknown으로 남았다. 상세 대응·연결·실패 조건까지 새로 주면 다른 `reference_design`의 mapped 후보가 될 수 있지만 그때도 구현 성공은 별개다. 이는 역할명 변경의 효과가 아니라 **proposed_use와 근거가 달라졌을 때 다른 판정 질문이 된다는 사례**다. 따라서 문제 상대 역할을 저장할 때 사용 범위와 구체 제안을 함께 남겨야 한다는 권고는 유지하지만, 실제 판정 변화율2/30이라고 보고하지 않는다.

## 5. 역할 표시가 잘못된 필터가 되는 반례

'선택 범위 전체를 대체할 후보는 S1=product만 남긴다'는 잘못된 규칙을 실제18행에 적용했다. 이 규칙은 의도적으로 만든 연구자 가정(H)이며 적용 계산만D3-run이다. 정답 참조도004의 연구자 문서 EXPECTED이지 외부 금표준이 아니다.

두 코더 모두 DIRECT_DOCUMENTED7개 중 **R01·R02·R10의3/7을 탈락**시킨다. 세 후보는 component이지만 선택된 부품 범위에서는 whole이다. 반대로 product 통과 후보는A에서7개 중알려진 mismatch2개(R16·R18), B에서8개 중3개(R07·R16·R18)를 포함한다. 형태는 필수 요구 충족을 대신하지 않는다. [role-filter-counterexample.json](evidence/role-filter-counterexample.json)

S2=whole만 통과시키는 규칙도 R03 등실패 후보를 남긴다. 이번18행에서 S2 whole15개 중 DIRECT7·INSUFFICIENT2·MISMATCH6이다. 따라서 S2가004에서18/18로 재현되어도 판정 정확성의 대리 지표가 되지 않는다. 검증된 효용은 L/E/H/T와 구체 근거로 판단해야 한다.

## 6. 한계와 다음 확인

이 분석은 통제한 문서 판단의 일관성을 검사했으며, 역할 표지가 실제 사용자나 자동 판정기에 주는 영향은 시험하지 않았다.30개 중14개는INSUFFICIENT이고15개는전체 라벨 미부여다. 후자는 조언·비교10개와 필수 판정 기준이 부족한 실제 대안 제안5개로 구분된다. 이 구성에서0변화는 역할 무영향의 상한 추정도 아니다. 원인별 영향 비율이나 인과 효과를 계산하지 않는다. 내부 별도 검토 [impact-independent-review.md](evidence/impact-independent-review.md)는 이런 오판 위험을 확인한 검토이며 새로운 사람/모델 실험이 아니다.

최소 후속 확인은 실제 proposed_use가 명시된 불일치30개를 새로 모아 역할 표시 없음/A/B를 무작위 배정하고, 원 코딩을 보지 않은 평가자가 같은 H/T를 판정하는 것이다. 현재 가정2개는 원 제안의 사용 문장부터 정상 공개 원문에서 확인해야 한다. 이 작업은 수행하지 않았으므로 실행 입력·절차는 HANDOFF에 남긴다.

재현: `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/build_impact.py`; `PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-016/evidence/toy_counterexamples.py`. 이 명령들은 수기 판정을 직렬화하거나 toy 계산을 재현할 뿐 원 추천의 실효성을 시험하지 않는다.
