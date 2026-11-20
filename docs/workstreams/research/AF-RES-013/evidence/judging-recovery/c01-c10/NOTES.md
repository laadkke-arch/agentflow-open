# C01–C10 후보 판정 — 내부 별도 검토

입력은 `caa2a814727dd485ed0eb9bb8530d6b16fab9584`에 보존된 20개 A/B 원 응답, 후보 목록, 실제 열린 문서 기록, 접두부 및 정답이다. 검색 실행은 반복하지 않았다. 후보 117개를 하나씩 읽고 판정했으며, 직접 원문을 추가로 연 경계 자료는 sources.json에 별도로 기록했다. 실행자와 다른 내부 검토지만 사람·다른 모델의 검증이나 새 blind run은 아니다.

## 판정 범위

`H_assessment_scope=reference_design`이다. 모든 조건부 판정은 baseline이 실제로 제안한 부분과 연결 조건만 평가한다. `runtime_observation=not_performed`, `implementation_H=unknown`을 별도로 둔다. 새 enum/namespace/controller 구현을 실제 완성하거나 시험한 결과가 아니다. `not_in_scope`는 원 응답부터 parser·계측·admission·packaging 등 좁은 부분을 제안한 경우에만 썼다. 모든 H를 범위 밖으로 돌린 행은 없다.

`manual-decisions.json`이 수동 의미 판정의 원장이고 `build_judgments.py`는 이를 정해진 필드에 넣는 직렬화·집계 코드다. 코드가 후보의 의미를 자동 채점한 것이 아니다. 재생성 명령은 저장소 루트에서 다음과 같다.

```bash
python docs/workstreams/research/AF-RES-013/evidence/judging-recovery/c01-c10/build_judgments.py
```

## 가장 중요한 경계와 반증

1. **전체 대안 실패와 처음부터 좁힌 참고를 구별했다.** C03/B1의 실제 script는 SSH·node tools가 필요하다(JR1-001). baseline은 이 경로 자체를 일반 사용자에게 제공하자고 하지 않고 PID lookup/namespace attachment 코드만 authorized node-agent 뒤로 옮기라고 했다. 따라서 원형의 node 실행 대안(G10)을 발견했다는 회수는 인정하지만 전체 H를 통과한 완성품으로 읽지 않는다. C03/B5 privileged tracing, C03/B6 sidecar packaging도 같은 원칙을 적용했다. 이 범위 선택 때문에 strict 근접 오답은 0이다. 이는 모든 후보의 전체 적용 성공이거나 운영 위험이 없다는 뜻이 아니다.

2. **source에 기능이 있다는 사실을 후보가 그 대안을 찾았다는 판정으로 확대하지 않았다.** C01/B2의 cron library를 timer-list 적중으로 세지 않았다. C02의 Podman/LXD allocation 예는 Kubernetes에서 runtime에게 mapping 선택 권한을 넘긴다는 정책까지 제안하지 않아 G03을 주지 않았다. C06의 OCI namespace path는 target container/sandbox ID API와 구별했다. C09의 일반 generic numeric type 언급에서 input-type preservation을 추정하지 않았다. C10의 foreign enum class/code generator를 자동으로 metaclass/all-in-one 대안으로 취급하지 않았다(JR1-006).

3. **구조 일치의 남은 해석 경계는 별도 검토할 가치가 있다.** C03/A4·B1의 node nsenter G10, C04/B1의 CRD 정책 G02, C07/B2의 loop별 별도 binding G02, C08/A2·B1의 여러 for 병렬 의미 G06, C09/B3의 range entity가 가장 논쟁적이다. 원 응답의 정확한 설명과 gold의 단위를 맞춘 근거를 각 `gold_matches.rationale`에 적었다. 이 행들의 구조 회수와 외부 실체 회수를 합쳐 독립 prior-art entity 검색 성공이라고 부르면 과장이다.

4. **현행 유용성과 과거 근거를 분리했다.** 날짜를 새 열람으로 승격하지 않았다. C08/A1은 1999 grammar와 날짜 미확인 Haskell1.3 세부 의미 교차근거가 섞여 있어 원 `pre_decision` 값을 보존하면서 `nongold_historical_useful=false`로 보수적으로 제외했다. C07/B4의 현대 zip 기반 optional padding은 현행 구조 적중일 뿐, 원 결정에 독립적인 역사적 선행 구현이라는 뜻이 아니다.

5. **5개 후보의 결정적 근거 부족을 보류했다.** C02/A8 Firecracker와 B7 gVisor는 넓은 격리는 설명하지만 이번 pod identity mapping의 구체 대응이 없다. C03/B4는 CRI plugin 존재만으로 debugger namespace/reduced-capability 지원을 입증하지 못했다. C05/A5는 현행 dedup의 한계를 정확히 발견했지만 개선된 write bound와 semantic-preserving 설정은 이 후보에 없다. C10/A5는 기존 attribute의 assignment/delete는 막지만 closed set의 immutability 연결이 부족하다. 이들을 무조건 위반·무가치로 단정하지 않고 확인할 최소 자료를 남겼다.

## URL 감사

- C09/B1: 원 실행은 공식 `/documentation/lw51/CLHS/Body/m_loop.htm`를 열었으나 후보에는 정규 HyperSpec 주소를 썼다. 추가 판정에서 후보의 정확한 URL을 직접 열고 grammar를 확인했다(JR1-004). 원 baseline에 그 fetch가 있었다고 소급하지 않는다.
- C10/B2: `/better-enums`와 `/better-enums/`는 trailing slash 차이다. 정확한 후보 URL도 직접 열렸다(JR1-005). 깨진·가짜 링크가 아니다.
- 실패한 API/date fetch는 실제 후보 URL이 모두 깨졌다는 뜻이 아니다. 후보의 실제 본문 확인과 역사판/metadata 접근 실패를 분리했다.

## 다른 분야 역할 정정

K0383-G06은 능동태의 행위자·직접/간접 목적어를 Event 필드에 대응시키므로 단순 명명 장식보다 강한 구조 전이다. SCOPE의 명시적 비소프트웨어 관계 전이 기준에 따라 역할 정정을 권고한다. 외부 언어학 문헌이나 제품을 인용한 것은 아니며, 그 대안은 거절됐다. 따라서 `role=다른 분야 원리`, `transfer_kind=structure`, `external_source_citation=false`, `stance=rejected`를 분리해 보존한다. correction.json에 최초 값·이유·원문 위치가 있다. 실제 CASES는 이 shard에서 수정하지 않았다.

원문 Overview는 자동 분석을 목표로 말하면서, 해당 대안 절은 인간만 소비한다고 거절한다. 이 내부 긴장은 설계 문서의 완전하고 일관된 정답원 가정에 대한 반례다. 독립적인 사용 효과나 최종 구현 의도는 이 텍스트만으로 결정할 수 없다. A/B 모두 active-voice 역할 매핑을 제안하지 않아 이 항목은 미적중이다.

## C07 채택 후 변경 이유의 회수

후속 고정판 `6e249d895555a5e330718a661678ef3827fa708a`의 `Subsequent Change to zip()`를 직접 읽었다(JR1-014). 변경은 `zip()`의 무인수 호출이 TypeError 대신 빈 리스트를 반환하도록 한 부분 번복이다. 가변 인수 펼침으로 역변환·전치를 표현할 때 입력 레코드가 0개인 기저 사례도 같은 연산으로 처리하려는 이유였다. 전체 zip 설계 폐기나 Python 3의 iterator 변경과는 별개다.

동결된 원 응답 A의 5개 후보와 B의 4개 후보 중 이 관계를 실제로 제안한 것은 각각 0개다(0/5, 0/4; 총 0/9). 결정 전 판이 확보된 후보만 보아도 0/5(A 2개+B 3개)다. Haskell의 두 인수 중 하나가 빈 리스트인 경우의 종료는 인수가 아예 없는 호출과 다르다. A의 SRFI variadic interface도 원 응답에 무인수 처리·전치·역변환의 빈 입력이라는 관계가 없으므로 후속 변경 이유의 회수로 올리지 않았다. 원문에 그 기능이 잠재적으로 있을 수 있다는 사실로 반환 후보의 제안을 보충하지 않는다. 자세한 단위와 판정은 REVERSAL_NOTES.json에 남겼다.

추가 확인은 새로운 실행에서 `0개 시퀀스`, `빈 시퀀스 1개`, `빈 레코드 집합의 전치`를 구분하는 경계 입력을 주고 관측하는 것이다. 이 질문을 본 뒤 답을 기존 실행에 소급 추가해서는 안 된다.

## C11–C20 경계 행 교차검토

다른 내부 판정의 11행을 원 응답·열람 기록·접두부·gold와 다시 대조했다(CROSS_REVIEW.json). 10행의 결론에 동의하고 C14/A2의 H4를 pass에서 not_in_scope로 바꾸도록 권고했다. SQLAlchemy 후보는 처음부터 lifecycle/namespace 부분 참고로 제시됐고, 실제 tagged code는 결과에 ORM class/SQL-expression 제약을 적용한다. 임의 annotation 계약을 새로 설계해야 한다는 조건은 그 조건을 이미 통과했다는 증거가 아니다. 담당 내부 검토가 동의하여 자기 판정 파일에서 수정하기로 했고, conditional 라벨·gold 회수는 바뀌지 않는다.

나머지 주요 경계는 PyPy method cache와 특정 CPython issue의 외부 실체 동일성, generic callback과 Python 함수 지역 상태 보존의 구조 차이, intrinsic attribute와 redeclaration 정책의 차이, 전체 match 표현식과 procedural pattern 재작성의 차이다. 구현 속성을 알고 있다는 사실만으로 원 응답에 없던 gold 회수를 추가하지 않았다. Jep의 clean README만으로 isolation lifetime 계약을 통과시키지 않은 보류에도 동의했다.

## 한계

엄격 gold 일치는 공개 설계 문서 저자의 모든 유용한 참고를 뜻하지 않는다. 구조 대안을 잘 설명한 외부 자료도 문서 내부의 특정 대안과 다르면 미적중이고, 유용한 후속 자료라도 역사적 선행 근거가 되지 않는다. 부분 참고를 조건부 유용으로 코딩하는 범위 자체에 연구자 해석이 있다. 이 shard의 유용 수는 구현·사용자 채택·우월성 점수가 아니다.
