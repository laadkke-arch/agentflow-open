# RESULT 소프트웨어 부분 검토

검토자: `/root/software_frame` assistant 에이전트. 이 에이전트는 소프트웨어 원문 판독과 원자료 감사를 작성한 주체이므로, 이번 검토는 **자체 대조 검토**다. root가 따로 수행한 Casdoc 스키마·ID 결합 감사의 수치도 대조했지만, 이를 모든 연구에 대한 독립 심사나 독립 재채점으로 부르지 않는다.

검토 완료 기준시각: **2026-11-23T02:20:47.085703+00:00**. 아래 행 번호는 수정 전 입력판에만 적용한다. 전역 파일은 수정하지 않았고, 이 검토 파일만 작성했다.

## 1. 입력판과 범위

| 입력 | 고정 식별값 | 읽은 범위 |
| --- | --- | --- |
| `RESULT.md` | SHA-256 `b2c24bd056c110ea70bca2cb1bb538bb66233a725a40919350cca66a1a9af783`; Git blob SHA-1 `41fe21948539b4addc1a3916afef165f4184dcff`; 50,763 bytes | 표1 S01–S04 행7–10, 표2 행27–39, Q1 행52–54, Q2 행64–66, Q3 행76–84, Q6 행151·155, Q7 행171–178, 허용 문장 행222–226. 다른 사례의 결론·전체 원문 수는 이번 검토의 승인 범위가 아님 |
| `streams/software/endpoints.json` | SHA-256 `749c90318d6bd5b5170b027f58c88001a627c1f5391396a34ee1a9f2d64c5138` | S01–S04 원 시계·종점 정의 |
| `streams/software/joins.json` | SHA-256 `044d02f06ea8be4c7cb3c96b64cfd611327de085aa78af513b41d48011f38918` | 실제 연결과 미실시 연결의 구별 |
| `streams/software/bounds.json` | SHA-256 `f407a57a6737919df8b30e1aa130ae83e91f70464ee654b9b57bff6f1761498c` | Newton 보조 집계와 1차 미확인 행 |
| `streams/software/schema-audit.json` | SHA-256 `fb7ef55e43315a7621b065cefdcce41010ad01ed837006e7ada3c47d8d30762d` | Newton 24단위/588이벤트, DesignPatternDoc 21행과 시간 합 |
| `streams/software/findings.md` | SHA-256 `57850f16964f191a7261cb3ac5b9bf60afb35a81462a96708816e7fc7b5974ca` | Newton 시계 정의의 70분 표현; 행24 |
| `streams/root/casdoc-audit.json` | SHA-256 `04b75747716d80835026e3f3329eda7743e231a668a1f5771f17832228eb3fed` | 13파일/2366이벤트, 122→122 검색 조각 결합, 중복 헤더·시각 의미 |
| `endpoints.csv` | SHA-256 `a6660515b8e6bbc5db9e02c31e71dfa6936903abdafb3465d80ba270c8b67001` | S01–S04 행과 원 JSON의 대응 |
| `joins.csv` | SHA-256 `ce40bf6ae833f784948344eea1994ec0596c289453a78fc81114a3cbe781a93b` | S01–S03 실제/목표 연결 구분 |
| `bounds.csv` | SHA-256 `6991968968f36c5d988029d26263be127868bdc49c991f8dba4362057ceaf224` | S01 보조 수가 `observed_secondary_count`에 있고 1차 `observed_joint_x`에 복사되지 않았는지 |

Git blob SHA-1은 파일 내용에 Git blob 헤더를 붙여 계산한 **내용 식별값**이며, 이 초안이 원격 커밋되었다는 주장이 아니다. Git 명령은 실행하지 않았다.

## 2. 검토 결과와 수정 사항

**주요 수치·분모·결론의 방향은 일치한다.** Newton의 25분 저자 완료 6/4를 보조 종점으로 보존하면서 원 기능 판정·최종 제출 정의가 미확인인 1차 행과 분리한 처리는 타당하다. DesignPatternDoc의 45분 계획을 강제 마감으로 만들지 않았고, Casdoc의 검색 조각 연결을 배정 결과 연결로 바꾸지 않았다. Kruse의 50행과 50명도 구별되어 있다.

다음 두 표현은 수정하는 것이 정확하다. 첫 번째는 본문에 직접 나타나지 않지만 본문의 입력 원장에 남은 오류다.

| ID·우선도 | 위치·현재 표현 | 확인한 문제와 영향 | 제안 수정 | 직접 근거 |
| --- | --- | --- | --- | --- |
| **SR-01 · 수정 필요** | `streams/software/endpoints.json` S01-primary.training 및 이를 복제한 `endpoints.csv`: `separate sessioncap70min`; `streams/software/findings.md` 행24: `별도 전체 세션 상한은 70분` | 원논문은 회기가 **약70분**이었다고 기술한다. 확인한 TutorialStudy에도 70분 강제 종료는 없다. 초기 원장의 `cap`은 검토자 자신의 과한 표현이며, 25분 과제 제한과 회기 길이를 혼동하게 할 수 있다. RESULT에는 이 70분 cap 주장이 없어 본문 수치는 바뀌지 않는다 | `Newton warm-up outside the 25-minute tasks; session approximately 70 minutes, with no enforced session cap identified.` 원 JSON과 통합 CSV의 평탄화 값·details_json을 함께 일치시킬 것. findings의 해당 문장은 `전체 회기는 약70분이며 강제 회기 상한은 미확인이다`로 수정 | [Newton 원논문](https://users.ime.usp.br/~gerosa/papers/Newton.pdf) PDF5 §4.1 Study Protocol; [TutorialStudy](https://zenodo.org/api/records/10459420/files/TutorialStudy.pdf/content), 과제 지침. SW-N-P/T |
| **SR-02 · 수정 필요** | RESULT 표1 S03 행9: `40분 관찰 뒤3명에게 선택적 최대20분 연장` | 실제로는 참가자 모두에게 추가 작업 선택권을 주었고 **3명이 사용**했다. 현재 표현은 연구자가 3명에게만 연장을 배정한 것처럼 읽힐 수 있다. 형식 배정·대조가 없다는 핵심 결론은 유지된다 | `40분 작업 후 모든 참가자에게 최대20분 추가 작업 선택권; 3명이 사용. 8개 전부 완성은 기대하지 않음` | [Casdoc 원논문](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf) §3.2 Procedure, PDF8; 추출문 406–413. SW-C-P |

아래는 숫자나 식별 판정을 바꾸지 않는 명료화 권고다.

| ID | 위치 | 이유와 제안 문구 |
| --- | --- | --- |
| **SR-03 · 명료화 권고** | RESULT Q2 행66: `관찰자 검사가 작업 해답을 허용하도록 시간을 준다는 절차도 있다` | 원문은 과제 말에 정오를 알려 주고 코드·문서를 검증하며 정상 작동하는 해답을 얻는 시간을 확인한다고 기술하지만, 이 문장만으로 실제 연장·재시도 규칙을 확정할 수 없다. `관찰자가 과제 말에 결과의 정오를 알리고 코드·문서를 검증했다는 절차도 있다. 실제 종료·수정 재시도 규칙은 미확인이다`로 좁히면 안전하다. 계획45분, 최대3290초, q 미보고라는 판정은 유지한다. [DesignPatternDoc](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml) Data collection; SW-D-P |
| **SR-04 · 명료화 권고** | RESULT Q7 S02 행172의 `연습시간 제외` | 직접 확인한 것은 EG에 별도로 제공한 **2분 plugin walkthrough**다. `도구 안내2분 제외`로 맞추면 표1과 동일한 의미가 된다. 6개 시간의 합이라는 정의만으로 모든 전환·대기 시간의 포함 여부까지 확정하지 않는다. 같은 원문 Procedure; SW-D-P/T |
| **SR-05 · 명료화 권고** | RESULT Q6 행155의 Kruse 50프롬프트 행 | 현재 분모 구분은 맞다. `ad-hoc군25명이 두 함수에 대해 만든 성공 프롬프트50행이며, 전체 실험은 ad-hoc25명/사전정의25명으로 총50명`이라고 쓰면 성공적으로 생성된 프롬프트의 코딩 표라는 선택 조건까지 드러난다. [Kruse 원논문](https://arxiv.org/pdf/2408.00686) §II.D, §III.A, Table I; [패키지](https://zenodo.org/records/16413762). SW-K-P/D |
| **SR-06 · 용어 통일 권고** | RESULT Q2 행64·Q3 행76의 Newton `588개 메시지` | 원자료 감사 단위인 `588개 로그 이벤트`로 통일하면 사용자 질문, 도구 힌트, 폼 제출 등과 최종 제출의 차이를 더 분명하게 유지한다. 588이라는 수는 일치하며 새로운 결과 계산은 필요하지 않다. [Newton Experiments](https://zenodo.org/api/records/10459420/files/2.%20Experiments.zip/content); SW-N-D |

## 3. 사례별 결론 검토

### S01 Newton

원논문 Methods는 과제당25분 제한과 두 조건·자료집의 균형을 명시한다. 별도 연장 언급은 확인되지 않았다. §4.2는 두 조건 모두 완료4명, Newton만 완료2명, 대조만 완료0명, 두 조건 모두 미완료6명으로 기술한다. 따라서 **저자가 25분 과제 프로토콜에서 완료로 분류한 수6/12 대4/12**와 그 차이1/6은 허용된다. Table3의 색 표기도 이전 시각 검토와 일치한다. [원논문](https://users.ime.usp.br/~gerosa/papers/Newton.pdf) PDF5 Table3/§4.1, PDF6 §4.2; SW-N-P/VIS.

이를 원래 요청한 `시간 내 최종 제출` 주변 t로 바로 옮기지는 않는다. 저장된 notebook에는 실패한 시도도 존재하며, 저자 완료 레이블은 단순 제출 유무와 같은 사건으로 확인되지 않았다. 분류기를 만들라는 과제 목표는 있으나 **원 기능적 완료 판정식**과 최종 제출의 운영 정의가 공개판에서 복구되지 않았다. `q 미확인`의 이유는 이것이며, 독립 채점자 부재를 새 필수 조건으로 삼는 것이 아니다. 원 연구자의 기능 체크리스트가 확인되고 저자 완료 레이블이 그 판정과25분을 함께 충족한다는 대응이 확인되면, 원행 없이도 저자 공동 집계로 승격할 수 있다. 별도의 예측 정확도 문턱을 발명할 필요도 없다. [TutorialStudy](https://zenodo.org/api/records/10459420/files/TutorialStudy.pdf/content), [Woz_Script](https://zenodo.org/api/records/10459420/files/Woz_Script.pdf/content); SW-N-T/W.

24사람×조건 단위의 notebook·과제후 응답 연결과 중복/미연결0은 `schema-audit.json`과 맞는다. 이것은 독립 배정·탈락 대장이 있는 완전 추적이라는 뜻이 아니다. 로그588이벤트와 그래프457노드/796링크는 서로도 단위가 다르며 최종 제출·채점 행이 아니다. 로그 첫–끝33.0–68.3분은 검증된25분 과제 시작/종료가 없어 목표 시계로 사용할 수 없다는 뜻이다. 이 수치로 실험자가25분 제한을 어겼다고 단정하지 않았다.

RESULT 표1/2, Q1–Q3, Q6, Q7과 Newton 허용 문장은 이 구분을 지킨다. 초안에 쓰인 6/4를 삭제하거나 1차 x로 복사할 필요가 없다.

### S02 DesignPatternDoc

도구11/대조10의21명 무작위 독립군과 여섯 시간 열, 분석21행 모두의 TotalTime 일치, 대조4/10행의2700초 초과, 최대3290초는 실제 감사 값과 맞는다. 계획45분을 강제 마감으로 확정하지 않은 것은 타당하다. 수치가 완전하다는 사실은21명 전원의 품질 통과를 뜻하지 않는다. [원문](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml) Participants/Procedure/Data collection; [패키지](https://zenodo.org/records/10849702) data.csv/README; SW-D-P/D.

관찰자가 코드·문서를 확인한 **품질 검증 절차는 있다**. 따라서 “품질을 아예 검사하지 않았다”는 주장은 허용되지 않으며 초안도 그렇게 쓰지 않는다. 다만 원 코드·도표를 분석 후 보존하지 못했다는 저자의 보고, 사람 ID 연결표 부재, 개별 판정·정확한 q 미보고 때문에 요청한 공동 성공률을 공개 원행으로 계산할 수 없다. 표1/2와 허용 문장은 그 제한을 정확히 전한다.

합계 평균은1178.0−2529.1=−1351.1초, T22 평균은483.9090909−475.3=+8.6090909초다. Q6은 후자를 같은 효과의 모순이라고 부르지 않고 다른 하위 종점의 반대 방향으로 제시한다. 유의한 악화나 인과적 해악으로 확대하지 않았으므로 이 표현은 유지할 수 있다. 이 자체 검토에서 원 연구의 통계 코드는 재실행하지 않았다.

### S03 Casdoc laboratory

원문은13명 모두 같은 복합 문서 조건이었다고 명시한다. 검색 조각에서 선택한 형식은 배정 조건이 아니다. 여덟 기능목표는 순차 수행 과제이며, 전부 완성하도록 기대하지 않았으므로13×8=104를 실제 배정·완료 분모로 만드는 것도 허용되지 않는다. 초안은13명, 대조 배정 없음, 전체8개 종점 미정으로 적어 이 오류를 피했다. [원문](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf) §§3.1–3.3; SW-C-P.

13파일2366이벤트와 phase2.ID→phase3.ID의122→122, 양방향 미연결0·중복ID0은 root의 별도 감사와 일치한다. timestamp 중복초과72와 완전중복0의 구별, 반복 열 이름7종에 대한 위치 기반 판독, instr-N/test를 최종 통과로 쓰지 않은 것도 맞다. [패키지](https://zenodo.org/records/14868205) coding-guide/phase2/phase3; RC-02/04/05 및 `streams/root/casdoc-audit.json`.

원래40분 후 추가 작업은 SR-02처럼 **전원에게 제공된 선택권과3명의 사용**으로 표현하면 된다. 이 수정은 t/q를 새로 채우거나 형식 대비를 복구하지 않는다. S03을 선정 후 대비 부적격으로 남기고 다른 연구로 교체하지 않은 처리도 동결된 선정과 일치한다.

### S04와 범위 밖 Kruse 진단

S04는 빈 자리이며 참가자 성공0이나 실패0으로 해석하지 않았다. Kruse는 문서 생성·코드 이해 과제이므로 이 빈 자리를 구현 과제 연구로 채우지 않았다. [선정 기록](selection.json), [Kruse 원문](https://arxiv.org/pdf/2408.00686) §II.A/§II.D.

Kruse의 전체 실험은50명, 각 조건25명이다. 별도의 프롬프트 코딩 표50행은 ad-hoc군25명×두 함수의 성공 생성 프롬프트다. 따라서50행은50명의 구현 성공자나 두 군의 최종 결과 대장이 아니다. Q6의 현재 구분은 맞고, SR-05를 반영하면 코딩 표가 어느 군에 속하는지까지 명확해진다. 원문 Table I과 패키지의 Participant/Snippet 집계가 대응한다. 이 진단은 연구 슬롯을 바꾸거나 원래 없던 통과선을 만드는 데 사용하지 않았다.

## 4. 직접 원문 대조 판과 검토 한계

이번 검토는 이전에 직접 내려받아 읽은 **동일 판의 캐시 원문**에서 해당 Methods·결과 문장·표 위치를 다시 대조했다. 새 고유 저작을 추가로 확보했다는 주장이 아니며, 원문 최소 수에 재산입하지 않는다.

| 원문·위치 | 파일 SHA-256 |
| --- | --- |
| [Newton PDF](https://users.ime.usp.br/~gerosa/papers/Newton.pdf), PDF5–6 | `4d487ba31d2c9176a9840704815aa5a2f24919906df29becc4f1a1fc7ee9f4f3` |
| [Newton TutorialStudy](https://zenodo.org/api/records/10459420/files/TutorialStudy.pdf/content), 과제 시간·연습 지침 | `69b12a70c3bfa2cefcfa136fe95702c826a0bcfba8c3a23e1bd7ae5edfe7e797` |
| [DesignPatternDoc XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml), Empirical study | `cd402e258bd1e6f08fb68c8838882fd35f3a64de21a9764919fd682fcb197530` |
| [Casdoc PDF](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf), §§3–4 | `0029ad4ce6dd7dfc6d8263223df61652837250d200c4ade6592151e28db3518c` |
| [Kruse PDF](https://arxiv.org/pdf/2408.00686), §II.D/§III.A/Table I | `f7fccff0e8f881c3ccb073ae4a34ceb731a170c5f0e1f1861e8146e840c56e24` |

새 참가자 자료 수집, 저자 연락, notebook·Java·플러그인 실행, 독립 재채점, 통계적 표본 불확실성 재계산은 하지 않았다. 기존 원자료 감사의 입력 해시·집계를 사용해 초안 수치와 의미를 대조했다. 검토 후 root가 문구나 원장을 바꾸면 이 문서의 입력 해시는 그 수정 후 판을 승인한 것으로 해석하지 않는다. 반영 여부는 root의 수정 원장 및 최종 결과 SHA에서 별도로 확인해야 한다.
