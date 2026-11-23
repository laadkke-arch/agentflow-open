# Root 산술·분모 교차검토

검토자: assistant 보조 조사자 `/root/baseline_methods`. 원래 두 기준 연구 분담을 수행한 뒤, root의 계산·원자료 감사 구현을 별도로 검토했다. **별도 에이전트의 계산·출처 교차검토이며, 외부 사람의 독립 심사나 독립 복제 연구가 아니다.** 검토한 파일의 SHA256과 실제 시각은 `root-review.json`에 고정했다. 원본 파일은 수정하지 않았고 이 검토의 산출물 두 파일만 썼다.

## 판정

**공동 종점의 주요 산술, 구성표, Casdoc 검색 조각 결합은 통과했다.** 잘못된 주요 결과 숫자는 찾지 못했다. 아래의 instruction 집계 이름, Blueprint 그림 위치 표현, 미확인 사유를 관측 구성처럼 쓰는 문구를 고치면 보고가 더 정확해진다. 별도 저자 계획 문서는 고유 1차 저작 열람 수에 포함할 수 있으나, 엄격한 사전등록 배당과는 분리해야 한다.

## 독립적으로 수행한 확인

Root `calculate_bounds.py`의 `main`은 실행하지 않았다. 함수만 읽어 들인 뒤 별도 구현으로 가능한 비음수 정수 2×2표 `(a,b,c,d)`를 전수 구성하고, 그 표의 `(q=a+b,t=a+c)`별 실제 최소·최대 `a`를 계산했다. N=1부터25까지 **6,200개 주변 개수 조합**에서 root 결과와 일치했다. 이 검산은 root의 `max/min` 식을 같은 식으로 한 번 더 호출하는 검사와 다르다.

| 점검 대상 | 재계산·출처 대조 | 판정 |
| --- | --- | --- |
| 2×2 극단표 | 각 표 비음수 정수, N 합, q/t 주변 합, 최소·최대 교집합이6,200조합에서 일치 | 통과 |
| 일반 반례 | 개입N10,q8,t9 → x7–8; 대조N10,q8,t8 → x6–8; 차이−1/10~1/5 | 통과. 실제 Blueprint 수치로 쓰지 않았음 |
| eXoaDocs 전체 | 저자 집계3/12−1/12=1/6=16⅔pp | 통과. 식별된 표본 기술 차이이며 CI 아님 |
| 네 과제 구성표 | `reproduce.md`에 적힌 네 표와 저장된 동적계획 witness의 N·네 주변·1111빈도를 각각 검사 | 통과. zero-intersection표는 주변만 맞고 저자 전체 집계에 모순이라고 명시됨 |
| eXoaDocs 미보고 t | eXoa의t3/t12, JavaDocs의t1/t12에서 제시한 네 표는 q/x를 유지 | 통과. 같은 관측 t의 x 극단으로 부르지 않음 |
| Blueprint q | 원래 품질 순위에 통과선을 붙이지 않았으며 clock-only외피를 원 종점의 식별값과 구별 | 통과 |
| 0인 조건부 분모 | `frechet(0,0,0)`의 비율은None, 대비는해당없음으로 반환 | 0% 성공으로 오인하지 않는 처리 |

eXoaDocs 원문은 [§5.3.2, printed1:21](https://people.csail.mit.edu/hunkim/papers/kim-tois2013.pdf)이며, 이 검토자는 앞선 분담에서 같은 쪽의 표와 문장을 실제 PDF 이미지로 확인했다. Blueprint의 binary pass 부재 역시 [원논문 printed518](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf)을 직접 대조한 결과다.

## Casdoc 자료 감사

Root가 받은 [저자 공개 ZIP](https://zenodo.org/api/records/14868205/files/artifact.zip/content), SHA256 `02579d60c09f7fed325fa18bccd17a7b52f5510b52b29f52af341fb38cb45260`를 메모리에서 별도 파서로 읽었다. README, coding guide, intervention guide 및 과제 파일의 안내·method 선언도 직접 읽었다. Java/JAR와 제출 코드는 실행하지 않았고 참가자별 원행을 보고서에 복사하지 않았다.

| 항목 | 독립 검산 결과 | 의미 |
| --- | --- | --- |
| ZIP |36,008,605bytes; 일반 파일44개 | Root 영수증과 hash·크기 일치 |
| Phase1 |참가자 파일13개, 이벤트2,366행; 같은 파일 내 완전 중복0, 동일시각의 추가행72 | 한 시각에 여러 사건이 있는 것과 중복 행은 다름 |
| Phase2/3 |각122행·고유ID122; ID집합 동일; 미연결0 | **검색 조각에 붙인 코딩의1:1결합** |
| Phase2의 시간 |시각·음수차 검사 이상0; 초/분 component 범위도 별도 점검 | 영상시각 기준 검색구간이며 최종품 완성시간 아님 |
| Format별 조각 |Casdoc+text38, text32, Casdoc33, code-only19 | 참가자가 실제 사용한 형식의 코드. 사람의 무작위 배정군이 아님 |
| Format별 구간 합 |각6,411/2,191/2,026/592초 | 검색조각의 기술 합계. 처치 효과나 전원 총시간으로 사용하지 않음 |
| TSV 헤더 |30열 중 `code only`와 정보유형6개, 합7개 이름이 두 번씩 있음 | 이름만으로DictReader를 쓰면 앞의 동일 이름 값이 덮어써짐. Root는 위치별 열을 유지하므로 올바름 |
| 과제 소스 |objective1–8, 조건부13×8=104 | 관측된 배정104행이나 성공기회104개가 아님 |

Coding guide의 Phase2는 ID를 전 참가자에 걸친 검색조각 ID, Start/End를 영상 내 시각으로 정의한다. Phase3는 **동일 조각의 ID**에 navigation pattern을 표시한다. Phase1의 `test`는 현재 해법을 확인하려 프로그램을 실행한 사건이다. 이 세 정의를 대조했으므로, 122행 결합을 “배정×제한시간×최종품질 결합”으로 바꾸는 것은 허용되지 않는다.

과제 템플릿에는 기능 확인 코드가 있고, README는 sample solution을 유일한 정답으로 요구하지 않는다고 적는다. `final_pass` 원장이 없다는 사실과 “어떤 기능 기준도 없다”는 주장을 혼동하면 안 된다. Root 보고는 **제출 결과와 채점 원장이 없어서 목표 결합을 미실시**라고 하므로 이 구별을 지킨다. Intervention guide의40분은 알림 지침으로 쓰여 있으며, 여기서 새 개인별 pass 수를 만들지 않았다.

## 수정·명확화 요청

| ID | 발견한 문제 | 영향·최소 수정 |
| --- | --- | --- |
| RR01 | `instr-N`에만 맞는 regex가 `instr-0/instr-1` 한 행을 제외한다.63/51은 singleton code만의 집계인데 필드명에는 그 한정이 없다 | Singleton 포함0/제외0은63/51, 복합코드를 분해하면65/52다. 둘을 병기하거나 현재 이름에singleton을 명시한다. 어느 쪽도 배정·성공 분모로 승격하지 않는다 |
| RR02 | `reproduce.md`의 “Fig4의 실제 보이는 위치”는 지정CHI PDF에서그림을 찾았다고 읽힐 수 있다 | 지정PDF에는 Fig4 참조문장만 있고 그림은 없음을 명시한다. 직접 확인한 별도 순위는 dissertation printed65 Fig5.4다. 본문에서 확인한10분·9/8은 변하지 않는다 |
| RR03 | “비통과에는 잘못된 결과·미완료가 섞여있다”는 관측된 이유 분해처럼 읽힐 수 있다 | 실제 나머지9/11의 오답·미제출·철회별 분해는 미확인이라고 쓴다.2×2 나머지칸은 가능한 구성임을 유지한다 |
| RR04 | `BM-P01`의 사전성 미확인을 원 계획 문서의 고유 1차 저작 열람 수까지 부정하는 하나의flag로 사용하면 엄격 배당과 총열람 수가 섞인다 | `counted_as_primary_extra=true`, `strict_prereg_quota_eligible=false`, `prospective_registration_verified=false`를 별도로 둔다 |

RR01·RR02를 root에 전달했고 root는 두 집계 병기와 그림 표현 수정을 수락했다. 본 검토는 JSON에 고정한 수정 전 snapshot을 평가하며, 이후 변경 파일까지 자동으로 재검토했다고 주장하지 않는다.

## DOCX 고유 저작 판정

[dx6qv의 author protocol v1](https://osf.io/download/gfawy/)은41,854bytes의 전체 DOCX를 성공적으로 내려받았고 API의 SHA256 `52a803923efbfdb58ac215438d29ee9a034a2831e4e2626733b428aa4bef47bb`와 일치했다. 저자 이름, 연구 질문, Sampling Plan, Sample Size/Stopping Rule, Randomization, Data Exclusion, Missing Data 등 실질적인 계획을 직접 읽었다. 같은 계획 파일의 미러·fork를 다시 세지 않는 조건으로 **별도 원 저자 계획 문서 한 저작을 추가 1차 저작 열람 수에 산입하는 것이 타당하다.**

하지만 파일의 날짜2016-04-29에 비해 Sampling Plan은 이미4월 중순 수집이 시작됐다고 적는다. 이 공개판만으로 결과를 보기 전의 등록·동결을 확인하지 못했으므로 **엄격한 prospective preregistration 배당은 충족시키지 못한다.** 원저작성·직접열람과 등록 선후는 서로 다른 판정이다.136명 계획이나180–300의 가능한 최대치도 실제 배정 분모로 인정하지 않는다.

## 검토의 경계

공개 자료로 확인할 수 없는 participant별 최종 성공을 새로 추정하지 않았다. 이 추가 검토는 root의 산술·공개 ZIP의 구조와 코딩 의미를 점검했으며, Casdoc 논문의 모든 실험 설계 문장을 별도로 다시 심사한 것은 아니다. 정확한 공개 참가자 배정 원장과 시각·품질 키가 없는 한, 확인된 검색조각122행으로 사용자 요청의 공동 성공률을 계산할 수 없다는 결론은 유지된다.
