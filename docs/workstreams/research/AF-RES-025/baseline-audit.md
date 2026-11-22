# 고정 입력의 계산 감사

확인 UTC 2026-11-22T04:48:53Z. 같은 모델의 별도 에이전트가 지정 고정판을 읽고 계산을 감사했으며, root가 원 코드·Q11c 키와 실행을 다시 읽고 `tools/audit_baseline.py`로 재집계했다. 기존 판정 키를 고정한 산술 확인이다. 외부 공급자 원문의 참값을 새로 판정한 검토로 부르지 않는다. 외부 원문 최소수에 산입하지 않는다.

## 인용 완결성

[AF-RES-021 replay.py](https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/replay.py#L381-L409)의 `measures` L399는 근거 묶음을 모두 열고 인용과 교집합이 하나만 있어도 `cited`로 세었다. 이번 지표는 `any(group <= opened and group <= cited)`를 요구한다.

| 공식 지원23행 | A 기존→전체인용 | P 기존→전체인용 | M 기존→전체인용 |
| --- | --- | --- | --- |
| 1절 |2→2|6→6|9→9|
| 2절 |6→6|9→9|14→13|
| 4절 |6→6|14→13|15→14|

세 차이 모두 Q11c다. [keys.jsonl Q11c](https://github.com/laadkke-arch/agentflow-open/blob/29049a5f15b6ef7cd7431f59a059598db6f5d857/docs/workstreams/research/AF-RES-021/keys.jsonl#L41)의 허용 묶음은 E29:288–319와320–350 또는 E29:256–287와288–319다. M/2는 두 절을 열었지만 한 절만 인용했다. 원래 슬롯·필수 묶음을 보존한 계산 결과는 [baseline-recount.json](evidence/baseline-recount.json)이다.

## 발견과 기지 조건

[AF-RES-022 statistics](https://github.com/laadkke-arch/agentflow-open/blob/df80ec2406042a73c2114e316894173f66309cda/docs/workstreams/research/AF-RES-022/evidence/statistics.json)의 A는 초기 표적기지21/24, 초기인지미확인3/24, 명시 미인지0/24, 기지제약교정2/24, 엄격발견→변경0/24다. 문서에 이름이 없다는 사실은 저자가 몰랐다는 뜻이 아니다. [RESULT Q3~Q5](https://github.com/laadkke-arch/agentflow-open/blob/df80ec2406042a73c2114e316894173f66309cda/docs/workstreams/research/AF-RES-022/RESULT.md#L145-L183)는 기능 후발, 호출 경계 차이, 선택 당사자 차이, 전체 API 거절과 내부 부품 재사용을 구별한다.

025에서는 새 대상과 기지 제품의 새 용도/제약을 분리하고, 후자는 주 신규대상 분자에 합치지 않는다. 당시판 코드/릴리스와 현재판 적합을 분리한다. 공급자 조건 판정과 질문자 후속 선택도 별도 열이다. 비용은 직접 관측한 검색/열람 수와 도구시간만 보고하고 실제 인시 절감은 미확인으로 둔다.

## 재집계

저장소 루트에서 아래 명령을 실행한다. 코드 수정·외부 모델 호출 없이 고정 Git 객체를 읽어 stdout으로 JSON을 낸다.

```sh
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-025/tools/audit_baseline.py
```

021의45고정 후보 근거접근 효과를025의새 후보 발견 효과와 같은 실험으로 합치지 않는다. 같아야 할 것은 판정 단위·분모·인용 충족의 정의다.
