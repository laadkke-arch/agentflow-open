# AF-RES-054#2 소프트웨어 범위 재개 검토

검토 주체: 별도 assistant `software_review`. 외부 사람의 심사·독립 실험 복제가 아니다. 기록 시각: 2026-11-23T02:39:31.507860+00:00. 새 모집이나 S04 대체 선정은 하지 않았다.

## 입력과 확인 범위

- `RESULT.md` SHA-256: `26bc48d54dd8f4067515b49a0d2476360961587986974cd14d8df4b2fd10fcdc`. 소프트웨어 표1/2, Q1–Q3/Q5–Q7 및 허용 문장만 검토했다. 부모 편집자의 후속 변경 전체를 승인하는 해시는 아니다.
- `streams/software/endpoints.json`: `da4876b4d4a586f81265d8d676ea310733a90665f3538b2f386c5fb7478e2c4b`; `endpoints.csv`: `747e24747ccd4c0593fc1c2e870c86d6fca06ef12adfb70d10496544c27aa2d0`.
- Newton/Casdoc 저자 원논문을 웹으로 다시 열었다. DesignPatternDoc의 원격 원문 경로는 오류/확인벽이 있었고, 이미 보존된 원문 XML의 Methods·한계를 직접 읽었다. 새로 확보한 적격 연구가 아니다. 각 열람·실패는 `sources.jsonl`의15필드로 남겼고 고유저작 최소수에는 추가 산입하지 않는다.

## 수정·권고

| ID·우선도 | 위치·확인한 차이 | 권고 | 직접 근거 |
| --- | --- | --- | --- |
| RSW-C01 · 수정 필요 | `streams/software/sources.jsonl` SW-C-P에는 아직 `3명에게 최대20분 선택 연장을 허용`이라고 쓰여 있고 RESULT 표1은 전원 선택권/3명 사용으로 수정되어 있다 | 출처 원장도 `전원에게 최대20분 추가 작업 선택권;3명이 사용`으로 맞춘다. 통합 sources도 재생성한다 | [Casdoc](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf) PDF8 §3.1, 웹 추출321–328행; RSW-06 |
| RSW-C02 · 기계 원장 명료화 | S03-primary의 `deadline_seconds=2400`은 선택적20분 연장이 있음을 별도 열 없이 읽을 때 확정 hard stop처럼 해석될 수 있다 | `deadline_seconds=null`, `planned_work_seconds=2400`, `optional_extension_seconds=1200`, `extension_users=3`처럼 구분하거나 동일한 명시 주석을 붙인다. 보고서의 공동 종점 미확인 판정은 유지한다 | 같은 Methods; RSW-06/16 |
| RSW-C03 · 경미한 표현 권고 | RESULT 표1/SW-N-D는33.0–68.3분을 첫–끝 차이라고 부르며 집계 코드는max−min을 사용한다 | `로그 timestamp 범위(max−min)`로 맞추면 재현식이 명확하다. **12로그 모두 실제 첫–끝과max−min이 같음을 재검산했으므로 수치 오류는 아니다** | [Newton Experiments](https://zenodo.org/api/records/10459420/files/2.%20Experiments.zip/content), RSW-18 |

현재 RESULT의 소프트웨어 주요 분모·집계·판정에서 위 표현 차이 외에 바꿔야 할 숫자나 부호는 발견하지 못했다. 동일 품질·제시간 공동 성공률을 새로 식별했다는 결과도 없다.

## 핵심 주장 대조

**Newton:**25분 과제,12명 교차 수행, 저자 완료6/4와 짝4/2/0/6은 원문과 맞는다. 원 기능 판정식과 최종 제출 정의가 공개판에서 복구되지 않았으므로 보조 완료로 보존한 것이 타당하다. 독립 채점자 부재만을 새 요건으로 만들지 않았다. [원논문](https://users.ime.usp.br/~gerosa/papers/Newton.pdf) PDF5–6 §§4.1–4.2; RSW-04/05/15.

**DesignPatternDoc:**21명10/11 무작위군,45분 계획과2분 안내, 과제 끝 관찰자 검증 절차, 분석 후 코드·도표 미보존이 원문과 맞는다. `품질 검증을 하지 않았다`고 바꾸면 틀리지만 현재 RESULT는 그런 주장을 하지 않는다. 원래 강제 마감·최종 pass수는 복구되지 않았다. [원문 XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11419627/fullTextXML?format=xml) Study design and conduction/Participants/Procedure/Data collection; RSW-11.

**Casdoc:**전원 단일 복합 조건,8개 전부 완료를 기대하지 않은 과제 순서, 자유로운 형식 왕복이 원문과 맞는다. API 참조 자동주석이 펼친 설명에는 빠진다는 예외도 맞다. 검색 조각122개는 배정 성공 원장이 아니다. [원논문](https://www.cs.mcgill.ca/~martin/papers/2025-ese-casdoc.pdf) §§3–3.3; RSW-09/16/17.

## 원파일 합계 재검산

별도의 짧은 Python 표준라이브러리 코드로 보존 ZIP을 읽어 합계만 재계산했다. 원 연구의 notebook·Java·도구 코드는 실행하지 않았고 개인행을 출력하지 않았다. 실행 종료코드0, 실행일2026-11-23UTC.

| 입력·단위 | 재검산 |
| --- | --- |
| Newton exp폴더/원로그 |12폴더·24notebook·588이벤트; 조건순서6/6.12로그의max−min 범위1980–4098.759초 |
| DesignPatternDoc data.csv |21행·28열;21행 모두6시간열 합=TotalTime. 대조10/도구11; 평균2529.1/1178.0초;2700초 초과4/0 |
| DesignPatternDoc T22 |대조475.3초·도구483.9090909초. 전체 시간합과 반대 방향이지만 서로 다른 종점이다 |
| Casdoc phase2→phase3 ID |122→122; 각각122고유ID, 양방향 미연결0. 사람의 최종 결과 결합이 아님 |

입력 SHA256은 RSW-12/13/14/18에 기록했다. 최초 모집의 완전성, 다른 분야의 분모/원문 최소 배당, 원 연구 통계의 재현, 새 외부 참가자자료·독립 재채점·품질검사 실행은 이 검토의 범위가 아니다. 기존 로그를 최종 제출로 바꾸거나 공개 파일의 부재를 자료가 세계 어디에도 없다는 주장으로 확대하지 않았다.
