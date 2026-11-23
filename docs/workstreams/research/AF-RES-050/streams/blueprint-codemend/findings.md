# Blueprint·CodeMend 원자료 연결 감사

이 파일의 범위는 고정 주표본 S03 Blueprint와 S04 CodeMend다. 034의 집계 숫자는 배경으로만 유지했다. 새 관측은 배정·시간·채점 연결 가능성, 그림의 관측 단위, 공개 패키지의 실제 필드와 누락이다. 사전 규칙 봉인 SHA는 `f3c8de473b52a64c92c862cc64927ce787525c1a`다.

| 연구군·층 | 과제·배정 단위 | 링크·설명의 차이 | 배정 인원·시행 | 시간 시작·종료·단위 | 품질 기준 | 원자료 URL·파일·키 | 연결된 행/대상 행 | 미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S03 Blueprint·주표본; BC-J01/02 | 사람별 독립군; directed URLLoader와 exploratory chart, tutorial 후 고정 순서 | query context·code preview·editor integration이 함께 다름. Blueprint군은 Web browser 금지; control Firefox+Adobe Community Help | 20명, 10/10; 각 directed 1회·exploratory 1회; 무작위화 미확인 | directed 시작→첫 paste 및 완료, 초; 600초 제한. exploratory 고정900초; 훈련시간 별도 미보고 | engineer의 기능·오류처리·불필요문장·style 순위; designer의 차트타입·전체data·미관 순위 | [논문 p518–519 Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); 원표 파일 미획득. figure position은 quality key가 아님 | 그래프 위치20/20은 paste·완료상태 연결. 원표 time–quality join은 미실행/20 directed 대상; 행수 미확인 | 정확 시간·개인 quality key·훈련시간·blind/rater reliability·사후재작업 |
| S04 CodeMend·주표본; BC-J03/04 | 동일인 bar/pie 각1과제, 각3누적 subtask; 두 조건을 교차 수행; task counterbalance | 추천·코드 강조·nested edit·preview+Google 대 동일 환경의 Google-only; 같은 링크 설명만의 차이 아님 | 20명,40 person-task,120 예정 subtask기회; 조건당60 예정기회; 실제 시도수 미확인 | subtask 시간 평균을 초로 보고. 시작/종료 이벤트·전체task시간·timeout·훈련시간 미확인 | 목표 plot 변형 완료수; 세부 채점·실제 제출물 미공개 | [package@445d5d8](https://github.com/ronxin/codemend/tree/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d); `eval-gt-2.csv`는 query 원장, lab원장 아님 | raw lab join 미실행/40task·120subtask 대상. query361행의 전체키360개·중복1쌍은 별도 IR 감사 | participant/sequence/condition/event/grade 키; 미완료와 미도달 분리; 실제 실행판 |

| 연구·비교 조건 | 비교 가능 단위·분모 | 선택시간 | 총 과제시간 | 활동시간 | 품질·실패·제한시간 | 추정치·불확실성 또는 미산출 이유 | 반증·근거 주소 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S03 directed 첫 paste; BC-O01 | 독립군10/10; 저자 집계+Fig4 전원20 확인 | 첫 paste 평균57/121초; 선택·정답 검증과 같지 않음 | 해당 행의 종점 아님 | 미확인 | Fig4 미완료3명도 paste | 저자 p<.01. 정확 원값·분산·grade key 없어 새 joint raw estimate 없음 | [p518–519 Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| S03 directed 완료자; BC-O02 | 완료자9/8; 원배정10/10 별도 유지 | 별도 종점 | 완료자 평균346/479초 | 미확인 | 미완료1/2가 성공자 평균에서 제외;600초 | 저자 전체20 completion-rank p=.14를 성공자 평균의 CI로 쓰지 않는다. 순위·성공자 평균은 다른 estimand | [p518–519](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| S03 directed 완료 여부; BC-O03 | 원배정10/10; 저자 집계 | 별도 | 정확 개별시간 미획득 | 미확인 |600초 내 완료9/10대8/10. 공개 자동검사·개인 grade 원장 없음 | 집계 완료수는 비교 가능. 균등품질 시간쌍은 아님 | [Fig4](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf) |
| S03 품질; BC-O04 | task별 독립군10/10; 저자 ordinal rank | 해당 없음 | exploratory 고정900초, 완료시간 contrast 아님 | 미확인 | directed engineer rank p=.02; chart rank sums94/116, p=.21 | 비유의 차이는 동등성 증거 아님. 별도 정렬된 그림은 identity join 불가 | [thesis p65 Fig5.4](https://hci.stanford.edu/publications/2010/brandt-dissertation/brandt-dissertation.pdf) |
| S04 subtask시간; BC-O05 | 사람20 교차설계; 실제 시간분석행수 미확인 | 미보고 | 전체가 아닌 부분시간108.70/134.12초 | 미확인 | 실패·미도달 포함정책과 상한 미확인 | 저자 비유의 결과. 60예정기회를 독립60명으로 계산하거나 부분시간을 총시간으로 바꿀 수 없음 | [PDF pp9–10](https://cond.org/codemend.pdf) |
| S04 subtask완료; BC-O06 | 조건당60 예정기회; 시도분모 미확인 | 미보고 | 미보고 | 미확인 | 완료46/41. 예정기회 대비 잔여14/19는 오답·timeout·미도달 구별 불가 | 조건당60은 20×3의 protocol분모. 3개 모두 성공한 person-task수·품질연결시간 미확인 | [논문](https://cond.org/codemend.pdf), [preparation notebook](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/user-study-prepare-0405.ipynb) |

## Q1: 무엇을 조작했는가

**확인된 사실.** Blueprint는 편집기 통합, context를 더한 검색, 예제 코드 preview와 검색 수단 제한이 묶인 비교다. 논문 p518은 treatment가 Web browser를 쓸 수 없다고 명시한다. 기존034의 요약에서 browser 허용으로 읽힐 수 있던 부분을 `baseline.json.baselineCorrection`에 정정했고 기존 파일은 고치지 않았다. 양군 tutorial의 안내도 같다 할 수 없다. control은 지정 검색 결과와 쓸 줄을 알려준다. directed 속도와 exploratory 품질에는 각각 상금 유인이 있었다. 독립군 사이의 사람을 짝짓지 않는다. 근거: BC-01 방법 pp518–519.

CodeMend는 모든 참가자에게 짧은 video와 interactive tutorial을 먼저 제공한다. 같은 참가자는 bar와 pie 작업을 각기 다른 조건에서 수행한다. 두 조건 모두 Google 사용이 허용되고 control도 같은 환경을 쓴다. 다만 추천 기능 전체를 교체하므로 동일 후보·동일 링크에 붙은 설명만의 효과는 아니다. 배정 순서표가 없어 counterbalance의 실제 균형·period effect는 재검증할 수 없다. 근거: BC-02 PDF pp9–10.

## Q2: 실제로 어떤 키를 찾았는가

Blueprint 저자 publication page, project page, software link, DOI 관계 metadata, 같은 연구의 technical report와 dissertation을 열었다. Adobe software는404였다. Fig4에는 사람20명의 그래프 위치 안에서 first paste와 completion/timeout이 함께 있다. 이는 **일부 관측의 연결**이지 원자료 표의 확보가 아니다. 정확 초수를 digitize하지 않았고 quality와 공통키가 없다. Dissertation Fig5.4는 각 종점마다 조건 표식을 독립 정렬하므로 같은 x좌표 순번을 같은 사람으로 간주할 수 없다. [BC-03·04·16·17·18 및 BC-F04·M01]

CodeMend package의 전206개 tree entry, 공개3개 commit,1 branch,0tag/0release를 확인했다. 이전2개 commit은 README-only다. `log-mode.txt`, `code-samples/user-study/{practice,task1,task2}.py`, `before_afters/before1.py` 및 분석 로그 출력이 공개 tree에 없다. `start_server.py`62–69는 logging이 주석 처리되어 있고 `.gitignore`는 `log-*.txt`를 제외한다. **이는 공개판의 상태**이며 논문의 “interactions를 기록했다”는 진술을 부정하지 않는다. [BC-05·09–12·22]

실제 `eval-gt-2.csv`361행을 읽었다. 열은 `case_study_no,answer,query,query_source`뿐이다. 전체4열 조합이360개이며 원행163–164가 정확 중복이다. 사례5개와 출처범주3개는 사람ID가 아니다. 해당 값으로 lab participant join을 하면 다대다 혼동을 만든다. XLS2개의 시트도 query×model rank표, SQLite는 `example(func_id,code,svg)` 콘텐츠 테이블뿐이다. `eval2.py`의 `score`는 추천 모델 점수다. 사람 산출물 품질 점수로 대체할 수 없다. [BC-07·08·13–15·23, `artifact-inspection.json`]

저자 사이트의 Markdown+figures ZIP도 열어 중앙 디렉터리를 확인했다. 파일9개는 PNG8개와 원논문 Markdown1개로, 별도 lab data가 아니다. CodeMend thesis는429, OSF·Zenodo 조회는 접근 실패였다. 따라서 결론은 **감사한 경로에서 lab 원장을 확보하지 못했다**이며 공개 자료가 세상 어디에도 없다는 주장이 아니다. 실패·재개 최소자료는 source 실패 행에 있다.

## Q3: 시간의 의미

Blueprint 첫 paste는 선택·복사 행동에 가까운 이정표다. task 전체600초와 별개이며, 함수가 올바르게 동작하거나 사용자가 이해했다는 관측이 아니다. Fig4의 미완료3명 모두 paste를 했다는 직접 반례가 있다. tutorial 시간·휴지·대기·후속 작업은 first-paste endpoint에 포함된 것으로 볼 수 없다. CodeMend는 부분과제의 평균시간만 준다. 누적3개 부분작업 합이 전체과제시간과 같은지, 미도달/미완료를 어떻게 넣었는지 알 수 없다. 두 연구 모두 이 감사에서 active/idle 계측을 발견하지 못했으므로 **활동시간/실제 노동 절감은 미확인**이다.

## Q4: 품질과 실패자는 어디에 있는가

Blueprint directed task는 URLLoader로 URL의 내용을 textbox에 넣는 목표다. 원배정20명 중 완료17명과 미완료3명의 관측을 보존한다. 별도 전문가가 코드를 순위화하지만 개인 time–grade 키를 확보하지 못했다. 차트 품질은 또 다른 과제의 또 다른 평가자에 의한 순위다. directed와 chart 품질을 합치거나 p=.21을 동등품질로 선언하지 않는다.

CodeMend는 목표 그림을 맞추는 누적 부분과제다. 준비 notebook은 실행 가능한 목표코드를 제공하지만 참가자 제출·채점 판정이 아니다. 논문은 bar의 세 번째 목표를 shadow라 서술하고 notebook은 hatch를 사용한다. 이 판 차이가 실제 참가자에게 무엇이 보였는지 바꿀 수 있어, notebook을 곧바로 실험 정답지로 확정하지 않았다. 60예정기회 중46/41완료라는 집계의 잔여14/19는 미도달, 오답, timeout, 미제출을 분리하지 못한다.

## Q5: 허용 비교와 미산출 항

공개 집계의 분모가 분명한 Blueprint 첫 paste와600초 완료수는 독립군 집계로 기술할 수 있다. 완료자 평균은 성공자에 조건을 건 값이므로 전체배정 시간 절감과 다르다. CodeMend는 사람 교차설계이고 각 조건의 task 내용도 다르다. person/task/period를 보존한 분석이 필요하다. 부분과제60개를 독립60명처럼 쓰거나 bar 첫 subtask와 pie 첫 subtask를 동일과제로 가짜 짝짓지 않는다.

새 raw자료 기반 사람 시간·품질 공동효과는 **산출 가능한 사례 관측0/2 연구군**이다. raw join 전후 행수는 missing이므로 `null/미확인`이다. 이것을0행 결측 또는0초 효과로 표시하지 않았다. `joins.json`은 target단위(20명,40task,120예정subtask), 누락키, 최소파일을 명시한다. `outcomes.json`은 저자 집계·그림 연결·식별 불가를 분리한다. 개인 정밀값·배정/순서·점수·실패 처리 규칙이 없으므로 새 CI나 동일품질 시간쌍을 만들지 않는다.

## Q6: 반대 증거를 얼마나 찾았는가

핵심 반례는 세 종류다. 첫째, Blueprint의 paste 후600초 내 미완료 관측3개는 “빨리 고르면 완성도 빨라진다”의 자동연결을 깨뜨린다. 둘째, 완료자 평균과 전체20명 completion-rank 검정은 포함 집단과 종점이 달라 같은 주장으로 합칠 수 없다. 셋째, Blueprint thesis pp67–69는 여러 code block과 설명 맥락을 요구하는 학습·적응 과제에서 한 예제를 좁게 보여주는 방식의 한계를 설명한다. 이들은 tool효과가 어떤 문제에서 약해질지 보여주지만 정량적 역전 크기는 제공하지 않는다.

CodeMend의 저숙련 참가자에서 이득이 컸다는 저자 서술은 subgroup n·원값이 없어 정량 감도분석 불가다. 도구의 새로움에 의한 학습 지연 가능성도 있다. 실제로 설명을 읽었지만 채택하지 않은 개인 기록은 확보하지 못했다. Blueprint 현장세션의 no-paste는 손으로 코드 입력·확인만 했을 가능성과 계측누락 때문에 비채택으로 해석할 수 없다. [BC-17 printed74–78; 같은 self-selected 현장관측은 lab비교 분모에 합치지 않음]

## Q7: 다른 설계 작업으로 옮길 수 있는 한계

**조건부 제안.** 설계자가 “자료를 빨리 골랐다”를 주장하려면 후보 노출, 첫 선택, 열람과 채택의 정의가 필요하다. 실험 참가자가 “정확히 끝냈다”를 뒷받침하려면 원배정 전원, 과제별 제출·timeout·정답/루브릭이 연결되어야 한다. 채점자는 버전이 고정된 요구사항과 독립 판정·실패 분류를 남겨야 한다. “나중의 재작업이 줄었다”에는 같은 산출물의 후속 수정·추적 기간이 추가로 필요하다. 두 소프트웨어 군에서는 그러한 follow-up을 확보하지 못했다. 이 분담은 분야 대조2군을 분석하지 않았으며, 그 표본을 소프트웨어 분모에 합치지 않는다.

## 직접 열람 수와 실행

직접 열람 기록25개에는 구성파일과 metadata가 포함된다. 고유 primary publication은 원논문2개와 Brandt dissertation1개이고 별도 저자 구현package1개다. 합계4개 고유 출판물/패키지 중, 엄격 배당은 같은 Blueprint 시험을 재수록한 thesis를 제외한 **3개(원논문2, 구현1)**다. 독립 supplement6개 배당을 이 분담에서 채웠다고 주장하지 않는다. 실패12개, 검색, 같은 논문 변환본, 같은repo 여러파일은 최소수에 포함하지 않는다. 세부는 `source-counts.json`.

읽기 전용 구조 감사 실행 명령:

```sh
"$CODEX_PRIMARY_RUNTIME_PYTHON" -B docs/workstreams/research/AF-RES-050/streams/blueprint-codemend/audit_public_release.py
```

저자 코드/모델은 실행하지 않았다. CSV키·XLS구조·SQLite schema를 메모리에서 읽었고 참가자 raw를 복사하지 않았다. 최초 unauthenticated GitHub API403 뒤 기존 connector로 공개tree를 읽어 SHA고정 snapshot을 보존했다. 성공 실행의 실제 exit0와 stdout은 `execution.json`·`execution-output.json`에 있다. 이것은 lab 원자료 분석 실행을 의미하지 않는다.

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·행 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 두 군 모두 배정–시간–품질 공통 lab키 미획득 | 동일품질 총시간·실제 노동 절감은 식별 불가 | [Blueprint Fig4·p518](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); [CodeMend eval-gt-2.csv rows2–362](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/eval-gt-2.csv) | person/task/condition/period/time/status/grade가 함께 있는 공개lab파일 찾기 | 공통키와 완전한 실패 분모가 확인되면 raw 공동분석 가능 |
| Blueprint browser 금지·복합tool, CodeMend 기능묶음과 과제판 차이 | 같은 링크의 설명만이 만든 효과로 귀속 불가 | [Blueprint p518](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); [CodeMend preparation notebook cells0–15](https://github.com/ronxin/codemend/blob/445d5d822174aa7cdfd7ceb16ce5db18f4e2b69d/codemend/models/user-study-prepare-0405.ipynb) | 실험 실행판·조건별 지침·후보노출 목록 확인 | 동일후보·동일링크·설명만 다른 arm과 배정표가 존재하면 설명효과 별도판정 |
| 제한시간 실패·훈련·활동·후속수정 기록 부족 | 부분시간·완료자 시간에서 총 노동/재작업 절감으로 확대 불가 | [Blueprint p519](https://hci.stanford.edu/publications/2010/blueprint/brandt_chi10_blueprint.pdf); [CodeMend PDFpp9–10](https://cond.org/codemend.pdf) | 실패/미도달·tutorial·idle/wait와 추적수정 원장 확인 | 모든 배정대상의 동일종점·활동정의·추적기간이 채워지면 확대 주장 재평가 |
