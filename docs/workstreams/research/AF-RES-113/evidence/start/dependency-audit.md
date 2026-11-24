# AF-RES-109 고정 의존 감사

- 담당: AF-RES-113의 별도 자동 모델 문맥 `dependency_audit`. 독립 인간 검토가 아니다.
- 확인 UTC: 2026-11-24T04:01:43Z. 이 시각은 마지막 원문 독해 뒤 확인 시각이며 각 파일 최초 읽기 시각을 소급한 값이 아니다.
- 방법: 공개 저장소를 가져온 작업 사본에서 `git show <고정 SHA>:<경로>`로 본문을 직접 읽고 Python 표준 `csv`로 수치를 재계산했다. 파일·브랜치·커밋 변경 없이 감사한 뒤 이 메모 하나만 저장한다.
- 노출 경계: 신규 librosa/scikit-image 원 이슈·API·예제·논문은 열지 않았다. 다른 회차 과제 결과도 읽지 않았다.
- 한계: 109 원장과 보고서의 일관성을 감사했다. 그 안에 인용된 모든 외부 원문을 다시 열어 재검증하지 않았으며 109의 실행 검사를 다시 수행하지 않았다. 아래 외부 주장·검사 완료 내용은 109 기록에서 확인한 범위다.

## 실제 읽은 고정 자료

| 파일 | 고정 URL | 읽은 범위 |
| --- | --- | --- |
| HANDOFF.md | https://github.com/laadkke-arch/agentflow-open/blob/e547d88834ff8adfcea9039e32c48b5be97e1eb3/docs/workstreams/research/AF-RES-109/HANDOFF.md | 전체 148행. 특히 70–86행 결과·독립성, 104–117행 검사 범위, 121–142행 재개 경계 |
| RESULT.md | https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/RESULT.md | 전체 194행을 1–65, 66–135, 136–194로 나누어 직접 읽음. 필수 3표, 수용 판정, Q1–Q7, 외부 분야, 검산 경계와 마지막 3행 포함 |
| costs.csv | https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/costs.csv | 헤더와 12 arm 전부 |
| choices.csv | https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/choices.csv | 헤더와 33 후보 전부. 후보 ID, 기존 안, 변경 단위·순서·책임, 최소 입력·예상, 실패 전제, novelty/flag/key, 역사판·prefix·가림·실행 상태를 읽음 |
| external-transfer.csv | https://github.com/laadkke-arch/agentflow-open/blob/c212aab782008f263cbee14f6304c029dc82ce3a/docs/workstreams/research/AF-RES-109/external-transfer.csv | 헤더와 4행 전부: EXTERNAL-OCFL, EXTERNAL-PREMIS-XSD, EXTERNAL-NIST, EXTERNAL-MIL1916 |

아래 CSV 레코드 번호는 헤더를 1로 센 논리 레코드 번호다. 이는 CSV 필드 내부 줄바꿈이 있을 때의 물리 행번호와 구분한다.

## 수치 재계산과 일치 범위

| 항목 | A | B | 합계·해석 |
| --- | ---: | ---: | --- |
| 질의 | 15 | 15 | 30 |
| 명시 개봉 | 23 | 29 | 52 |
| 반환 링크 | 16 | 17 | 33 |
| 예정 자리 공석 | 2 | 1 | 3/36 |
| arm 경과 초 합계 | 1934.069433 | 2234.938809 | 병렬·대기·판단 포함. 전체 벽시계나 절약시간이 아님 |
| 전체 조건부 선택 / 시험 | 8/16 | 8/16 | 양쪽 중복을 합친 고유 수 12/27 |
| 공통 소비량에서 원전 취득 확인된 선택 / 시험 | 5/11 | 2/7 | 줄인 예산으로 제안까지 재실행한 성과가 아님 |
| 엄격 비교 적격 arm | 0/6 | 0/6 | 12행 모두 strict_comparison_eligible=False |

costs의 자동 열람·토큰·금액은 모두 미확인이다. 0으로 환산하면 안 된다. R3-B 순위 1·3은 `common_indeterminate_ranks=[1,3]`이고, 전 행 `common_result_semantics`는 원전 취득 자격만 나타내며 컷오프 시점의 제안 완성을 증명하지 않는다고 명시한다.

choices의 빈 값 제외 모든 `choice_key` 고유 수는 18개지만 `new_implementation_flag == "1"`을 적용한 키만 고유 12개다. `new_test_flag == "1"`의 고유 `test_key`는 27개다. 진단·부정 대조·시험 전용 키가 존재할 수 있으므로 키 존재만 세면 구현 선택을 과대계산한다. `novelty_class`만으로 합산하는 것도 RESULT Q5가 경고한다. 원 판정 행은 새 구현결정 15, 새 판별시험만 12, 근접 오답 5, 근거 부족 1이며 행 수와 고유 선택 수는 다르다.

```python
choices = {r['choice_key'] for r in rows if r['new_implementation_flag'] == '1'}
tests = {r['test_key'] for r in rows if r['new_test_flag'] == '1'}
```

R1–R5는 고유 선택 9 / 시험 22, 잠정 R6은 3/5다. 33행 모두 `experiment_executed=False`, `observed_application_result=미확인`, `new_distant_domain_principle=False`, `strict_comparison_eligible=False`다. RESULT 표3의 요청별 수 0/3, 0/4, 3/5, 2/5, 4/5, 잠정 3/5와 일치한다. 모든 요청은 비교불가, 엄격 비교분모 0/6이다.

RESULT·HANDOFF·세 원장 사이에서 위 계산·수용 PARTIAL·잠정 R6·사후 외부 4개 발견실적 0이라는 주장에는 불일치를 찾지 못했다. RESULT는 결과 커밋 후 검사를 실행할 예정이라고 쓰고 HANDOFF는 이후 실행과 영수증을 보고한다. 이것은 시점에 따른 차이이며 모순이 아니다. RESULT에 적힌 예정 명령을 자체 실행 증거로 사용하지 않는다.

## 원장에 실제로 남은 반대 근거

| 위치 | 확인한 판단 경계 | AF-RES-113에서 이어받을 점 |
| --- | --- | --- |
| choices 레코드 11, R2-B-3 | Function-node comparator는 metadata만 확인하고 해당 본문 재개봉 실패. insufficient_evidence, new_test_flag=0 | 초록·metadata·재작성 요약을 본문 독해로 승격하지 않는다. 대체 경로는 원 클릭 성공으로 소급하지 않는다 |
| choices 레코드 13–15, R3-A-2/B-1/B-2 | mask 제거 후 전체 대체하면 생략된 기존 값이 지워질 수 있고 기존 값 없는 retain 표식은 별도 실패 | 같은 용어보다 저장 단위·처리 순서·전제를 비교한다 |
| choices 레코드 17·19·20, R4 | CSS target routing은 실제 React Flow 선택·삭제·drag 보존을 증명하지 않음 | 원자료 관측과 목표 구현 예상값을 나눈다 |
| choices 레코드 27–28, R5 | 같은 끝점 pair 평행 edge에서만 yFiles 안이 조건부 적합. fan-out에는 그대로 적용 불가 | 원전 입력 구조와 대상 구조를 대응시키고 깨지는 입력을 남긴다 |
| choices 레코드 29–34, R6 | synthetic wheel과 실제 Windows touchpad는 다름. ctrlKey가 물리 pinch를 유일하게 식별하지 않음 | 규칙적 표본·기기 조건을 목표 입력으로 옮길 때 불일치를 명시한다 |

HANDOFF 84행과 RESULT Q3–Q4는 별도 문맥이 있어도 root 일부 댓글, R2-A·R6-B 검색 후속 요약, R6 판독자 후속 노출이 있었다고 적는다. 별도 문맥의 존재만으로 가림 성공을 주장할 수 없다. 노출된 자료의 인용을 지워도 문맥이 다시 깨끗해지는 것은 아니다.

## 사후 분야 자료의 역할

external-transfer 4행 전부 `phase=postsearch`, `executed=False`, `discovery_credit=False`다.

- OCFL: 객체·version·state·digest 구분은 상태 보존 점검에 도움을 주지만 런타임 의미·원자성 보장은 아니다.
- PREMIS XSD: event·outcome·agent의 구분은 결손을 표시하지만 schema-valid 사건이 행위자·성공·인과성을 보장하지 않는다.
- NIST: 인수·거절·추가관측 구분은 참고할 수 있으나 제조 lot 무작위 표집 전제가 동적인 웹 순위에는 없다.
- MIL-STD-1916: 부적합 뒤 격리·수정·재검증 구조는 참고하지만 군납 수치·규칙을 제품에 강제하지 않았다.

RESULT의 추가 분석은 PREMIS PDF 접근실패와 공식 XSD 대체를 구별하고, W3C PROV-DM 추가 읽기는 배당에 산입하지 않았다고 명시한다. 4개 사후 저작은 검색 전략이 먼 분야를 발견했다는 실적이 아니다. 113의 사후 음향 측정·영상/지도 표본화 비교도 같은 분리를 유지해야 한다.

## 운영·인과·검사 경계

109의 검사 대상 결과는 `c212aab782008f263cbee14f6304c029dc82ce3a`, 영수증은 `a45c76dd75f4e244c60ebc9fe5dcc0e550173075`, 마지막 HANDOFF는 `e547d88834ff8adfcea9039e32c48b5be97e1eb3`다. HANDOFF 108–117행에 manifest·작업별 검산 exit0과 공통 검사 최초 실패/재실행 exit0을 구분했다. 이 감사는 그 실행을 다시 수행하지 않았다.

첫 공통 검사 실패는 TMPDIR이 소스 docs 아래라 임시 복사가 재귀화된 사건이었다. 113 검사에서도 임시 복사 디렉터리를 검사 checkout 밖에 두어야 한다. 검사 코드·timeout을 약화하지 않는다. 공통 자동 세션 발견 count0과 명시 manifest1개의 통과는 별개이며, 공통 71개 테스트를 원 프로젝트 제안 시험 27개의 성공으로 사용하지 않는다.

RESULT Q7과 HANDOFF 78–80행은 공개 patch+release 3/6, 원 요청자 명시 복구 진술 1/6, 이번 추천을 배워 동일 제안을 실행한 사건의 판정분모 0을 구분한다. 2026년 이번 추천을 2024년 행동의 원인으로 해석할 수 없다. 원 사용자 채택·절약시간은 미확인이다.

113은 고정 문서판을 읽는 현재 시점의 추가 본문 지지와 같은 작업자의 판독을 허용한다. 따라서 109의 역사 최초판·엄격 모델 비교 결손을 113의 실패로 자동 상속할 필요는 없다. 대신 실제 노출·본문 문자수·공통 입력·사전 봉인·빈 경로를 남기고 새 독자 학습효과나 과거 작성 당시 사실로 확대하지 않아야 한다. 링크 도달 / 추가 선택 / 제안 시험 / 실제 실행 / 후속 채택은 별도 열과 분모로 유지한다.
