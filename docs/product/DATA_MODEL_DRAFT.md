# 관계형 데이터 모델 v0.1 — 제안, 미구현

2026-11-19. 기존 대화의 수업 과제 맥락(2–5개 관련 테이블, PK/FK, 1:N, 조회·등록·수정·삭제, 공개 접속)을 고려한 **5개 테이블 초안**이다. 실제 TiDB/Render에 생성하거나 데이터 마이그레이션을 실행한 상태가 아니다.

## 테이블

| 테이블 | 핵심 열(초안) | PK/FK와 목적 |
| --- | --- | --- |
| `resources` | `id`, `name`, `canonical_url`, `kind`, `summary`, `repo_url?`, `homepage_url?`, `license_spdx?`, `pricing_kind?`, `verified_at?`, `last_seen_at?`, `status` | PK `id`, 중복 방지 `canonical_url UNIQUE`; GitHub 저장소·웹서비스·도구의 식별자 |
| `capabilities` | `id`, `slug`, `label`, `description`, `category?` | PK `id`, `slug UNIQUE`; 기능 분류 |
| `resource_capabilities` | `resource_id`, `capability_id`, `claim_status`, `evidence_url?`, `checked_at?`, `notes?` | 복합 PK `(resource_id, capability_id)`, 두 FK; 자원이 해당 기능을 제공한다는 **검증 가능한 주장** |
| `projects` | `id`, `name`, `description`, `scope`, `created_at` | PK `id`; 사용자가 관심 있는 프로젝트 또는 조사 시나리오 |
| `project_resources` | `project_id`, `resource_id`, `relationship`, `decision`, `rationale`, `evidence_url?`, `reviewed_at?` | 복합 PK `(project_id, resource_id)`, 두 FK; 프로젝트별 채택/보류/제외와 이유 |

모든 `?` 열은 NULL/unknown을 허용하는 초안이다. `relationship` 값은 `alternative|component|reference`; `decision` 값은 `evaluate|adopt|reject` 등을 검토한다. 세부 SQL 자료형·인덱스·enum 구현은 개발 세션 B가 선택해 실제 DB 테스트로 확정한다.

## 관계

~~~text
resources 1 ── N resource_capabilities N ── 1 capabilities
projects  1 ── N project_resources     N ── 1 resources
~~~

두 연결 테이블은 두 개의 N:M 관계를 분해하여 PK/FK와 1:N 관계를 명시한다. 특정 자원은 여러 기능에, 특정 프로젝트는 여러 자원에 연결될 수 있다. 동일 자원을 프로젝트마다 다른 활용 관계·판단으로 등록 가능하다.

## 근거와 5테이블 제한의 트레이드오프

- 별도의 `sources`, `observations`, `snapshots` 테이블을 두면 다양한 시점·복수 증거를 더 잘 표현할 수 있다. 그러나 수업 제약을 우선 고려해 5개 테이블에서 시작한다.
- 따라서 초안에는 핵심 근거 URL·확인일·상태를 연결 테이블에 두고, **다수 출처·실험 로그·장기 이력은 Git 문서/JSONL**에 연결한다. 이력의 정규화와 조회 효율이 제한된다는 점은 명시적인 설계 부채다.
- 자원 기본 유형(`kind`)과 프로젝트에서의 역할(`relationship`)을 혼동하지 않는다.
- 라이선스/가격을 모르는 항목은 임의로 MIT/free로 채우지 않는다. `unknown` 또는 NULL 처리.
- `stars`, `forks` 같은 지표는 외부 시점별 스냅샷일 뿐 판단의 정답이 아니다. 넣을 경우 `metrics_checked_at`도 필요하며 DB 모델 세션에서 범위를 결정한다.
- 자원의 자료 수집 시점(`last_seen_at`)과 실제 기능 검증 시점(`verified_at`)을 분리한다.
- `resources` 중복 식별은 URL 정책이 필요하다. `lab/repo-intake`는 후보일 뿐 아직 실서비스 수집을 보장하지 않는다.

## 권장 불변 조건

1. FK는 실제 DB에서 강제하고, 참조가 남은 자원/기능/프로젝트 삭제 정책을 명시한다(무조건 CASCADE 금지).
2. 정규화된 저장소 URL을 UNIQUE로 처리하되 페이지 URL, SSH clone URL, 별도 서비스의 관계는 미리 정한 정책으로만 통합한다.
3. `evidence_url`·`rationale` 없는 `adopt` 선택은 서비스에서 경고하거나 거부하도록 검토한다.
4. 'unknown'은 '거짓'과 다르다. 한 행의 미검증 주장을 다른 기능에도 전파하지 않는다.
5. 일반 공개 사용자는 기본 **읽기만 가능**하고, CRUD의 쓰기 동작에는 관리 권한이 필요하다.
6. 단위 테스트뿐 아니라 실제 JOIN 조회, 중복 키, 삭제 참조, 권한 우회, 잘못된 URL을 시험한다.

## 확인이 필요한 결정 (설계 책임자: 데이터 세션)

- 수업 제출 환경을 **TiDB Cloud + Flask + Render**로 최종 고정할지, 배포 전에는 SQLite로 모의 실행할지. SQLite와 TiDB의 SQL·FK 동작이 완전히 같다고 가정하지 않는다.
- 라이선스와 가격을 별도 테이블로 분리할 필요가 있는지, 5테이블 과제 제한과 실제 서비스 확장을 어떻게 나눌지.
- 사용자 계정과 프로젝트별 비공개 데이터가 필요하면 새 테이블/권한 모델이 필요하다. 이 MVP는 공개 카탈로그와 내부 관리용 프로젝트 시나리오 중심이다.
- 여러 근거 URL에 대한 데이터베이스 정규화는 후속 버전으로 남길 수 있다.

이 문서는 실행한 마이그레이션·실제 스키마가 아니라 **비교·검토용 설계안**이다. 변경 제안은 `docs/workstreams/data/`에 근거와 테스트를 남기고, 공통 문서 반영은 통합 담당이 한다.
