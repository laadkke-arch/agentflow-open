# 보강층 원행·원표 재현 기록

검사 주체는 `supplement` AI와 root의 독립 재계수다. 이 파일은 공개 저자 자료를 새로 모집한 실험으로 취급하지 않는다. 원행은 `cache/`에만 두며 커밋하지 않는다. 공개 산출물은 코드·해시·집계·키 감사다. JSON의 `null`은 **미확인**이며, 정수 `0`은 해당 파일/필터에서 실제 센 **관측 0**이다. `file_response_NA_n=0`을 원 배정의 결측 0으로 읽지 않는다.

## 1. Aslett 원본과 실행

고정 저자 커밋은 [`7b4ffee080be622e06f6197bfd095a3e4faebd16`](https://github.com/SMAPPNYU/Do_Your_Own_Research/tree/7b4ffee080be622e06f6197bfd095a3e4faebd16)이다. 입력의 URL·바이트·SHA256·레코드 수·인코딩은 [aslett-aggregates.json](aslett-aggregates.json)의 `inputs`에 있다. 추출 명세와 실행 코드는 [aggregate_aslett.py](aggregate_aslett.py), 집계표는 [aslett-counts.csv](aslett-counts.csv)다.

```bash
python -B docs/workstreams/research/AF-RES-062/streams/supplement/aggregate_aslett.py --fetch
```

이미 고정 입력이 있으면 `--fetch` 없이 실행한다. 이 실행은 입력 해시와 조인·범주 검사를 수행하고 두 집계 파일만 갱신한다. 작성자가 2026-11-23 UTC에 실제 실행해 종료코드 0을 확인했다. R 회귀와 유의성 추정은 **미실시**다.

### 추출과 조인

1. `Study_1_df_FM.csv`와 `Search_Exp_Misl_False.csv`를 `(ResponseId, Article_day)`로 1:1 연결했다. 각각 3,966행이고 키 중복은 **관측 0**이다. `Evaluation`을 직접 읽어 True, Misl/False, CND, NA를 분리한다. 전 행에서 저자 `Susc_FN` 및 `True_Dummy`와 일치했다. `Susc_FN=0`은 FM 또는 CND이므로 최종정답으로 세지 않는다.
2. `Study_1_df_T.csv`는 10,783행이며 키 중복은 **관측 0**이다. `Evaluation`의 T/FM/CND를 직접 계수한다. 이 파일의 `Susc_FN`은 FM 응답이지 참인 주장 수락값이 아니다. 참인 주장 수락은 `True_Dummy`와 일치하는 T 응답이다.
3. `Fact_Checker_Data_Master.csv`의 `Article_day`로 49개 문항(오주장 13, 정주장 36)을 연결했다. `Pariticipant_1_Eval`부터 `Pariticipant_6_Eval`까지의 최빈 범주와 저자 정오키 불일치는 **관측 0**이다. 이것은 **저자 키 복원**이다. 49개 독립 참값 원전을 검증한 것이 아니다. 의견 분포는 `truth_items`에 보존했다.
4. 우선 표본은 공변량 결측과 관계없이 원래 조건값으로 나눈 관측 범주 응답이다. 별도로 논문 분석 표본을 만들었다. FM은 [`Main_text_Figures.R` 75–92행](https://github.com/SMAPPNYU/Do_Your_Own_Research/blob/7b4ffee080be622e06f6197bfd095a3e4faebd16/Code/Main_text_Figures.R)의 파일 전체 `na.omit`, T는 같은 파일 1385–1394행의 `Article∈1..5` 및 `True_Dummy,Treat_Search,Age,Dummy_Congruence,Education_Score,Gender,Income_Score,Article_day,ResponseId` 완전사례 필터를 그대로 따랐다. FM은 1410–1412행의 선택 열 필터와도 같은 키 집합이다.

### 손검산

| 표본·정오층 | 통제 수락/정답/CND | 검색권유 수락/정답/CND | 수락 차이 | 정답 차이 |
|---|---|---|---:|---:|
| 전체 관측·오주장 | 356 / 387 / 445 = 1,188 | 420 / 367 / 374 = 1,161 | +6.20938%p | −0.96508%p |
| 논문 완전사례·오주장 | 343 / 382 / 420 = 1,145 | 411 / 361 / 358 = 1,130 | +6.41535%p | −1.41554%p |
| 전체 관측·정주장 | T 1,837 / FM 582 / CND 871 = 3,290 | T 2,046 / FM 469 / CND 690 = 3,205 | +8.00189%p | +8.00189%p |
| 논문 완전사례·정주장 | T 1,788 / FM 564 / CND 793 = 3,145 | T 2,002 / FM 459 / CND 663 = 3,124 | +7.23236%p | +7.23236%p |

첫 오주장 대비의 산식은 `100 × (420/1161 − 356/1188)`이다. 최종정답 차이는 별개로 `100 × (367/1161 − 387/1188)`이다. 원행 증인은 `Search_Exp_Misl_False.csv`의 헤더 제외 레코드 16과 155다. 양 군 각각 한 행의 키·조건·범주 응답·저자 이진값을 직접 대조했다. 참가자 식별자는 산출물에 재게시하지 않았고 root는 원 캐시에서 해당 두 행을 독립 확인했다.

논문 원표 손검산은 본문 “Measuring the online search effect”의 1,145통제/1,130처리, 876/872명을 코드의 완전사례 결과와 맞춘 것이다. 1,145+1,130=2,275이며 저자 본문 분석 N과 일치한다. root가 자체 stdlib 코드로 Study1의 두 정오층·두 표본·두 조건 8행을 다시 세어 수락/정답/CND 불일치 **관측 0**을 확인했다. root 결과는 `../root/independent-calculation.json`에 있다.

### 배정 분모와 결측 경계

원 참가자 배정명부, 제시된 문항 배정 기록, 주의검사로 제거된 사람의 문항별 결과가 없다. Methods는 동의 단계·중도탈락·주의검사에 따른 미기록을 명시한다. 또한 하루 후보 5개 중 3개를 제시하므로 파일 NA에는 미제시 문항이 섞인다. 따라서 파일의 2,006/1,960 또는 5,469/5,314를 정오층 **배정 N**으로 사용할 수 없다. 원 배정의 `N`과 미관측 `m`이 미확인이므로 `[a/N,(a+m)/N]`도 **미확인**이다.

위 차이는 원래 조건에 따른 **관측 응답의 기술 대비**이며, 클릭자에만 조건화한 값은 아니다. 그래도 분석 가능한 응답자의 선택 편향과 사람·문항 반복을 없애지는 않는다. 전체 정답률을 쓰려면 정오키 확인 문항만 합친 분모라는 말을 유지해야 한다. CND/무모드 기사나 제거된 응답자를 포함한 전체 배정 정확도는 아니다.

### Study5의 추가 결손

분석 파일에서 오주장 수락은 346/877→298/608(+9.56048%p), 정주장 수락은 1,249/1,782→1,155/1,359(+14.89918%p)다. `True_Dummy`는 저자 범주 응답에서 만든 이진값이며 `Four_Ordinal`을 임의 절단한 값이 아니다. 실제 두 변수 사이에 불일치가 있어 서열 척도로 원래 범주를 대신할 수 없다.

오주장 `True_Dummy=0` 안의 FM/CND 분리는 파일에 없으므로 최종정답은 **미확인**이다. 정주장 T 수락은 곧 저자키상 정답이지만 CND는 분리되지 않는다. `ResponseId+Article_day` 중복키는 FM 파일 1개(1,485행/1,484키), T 파일 2개(3,141행/3,139키)다. 원저 행을 보존했으며 그 이유를 확정하지 않았다. 파일 레코드를 모두 독립 시행으로 부르거나 조용히 중복을 제거하지 않는다. 후속 확인 입력은 원 설문 배정·완료·재응답 명부와 원 3범주 응답이다.

## 2. Ding 표본·이벤트 사전 점검

[`AIChatbot_Trust_Data.xls`](https://osf.io/download/qfua6/)는 독립 OSF 공개 파일이며 SHA256은 `7a0954227c534c094c120328f09083b437589d37f9b6aefd30f03987d8ee7ff1`이다. [ding-schema-audit.json](ding-schema-audit.json)에 메타데이터 집계를 기록했다. pandas/xlrd로 해당 열만 읽었다. 아래 예시는 이 stream 디렉터리에서 실행하며, 재현 입력은 `cache/ding/data.xls`다.

```python
import pandas as pd
d = pd.read_excel("cache/ding/data.xls", usecols=[
    "user_id_seq", "num_citation", "random_citation", "mouseover", "mouseover1"])
print(len(d), d.user_id_seq.nunique())
print(d.groupby("num_citation").user_id_seq.nunique())
print((d.groupby("user_id_seq").num_citation.nunique() > 1).sum())
```

실제 결과는 3,040행/303개 ID, 인용 개수별 ID 108/96/101, 여러 인용 개수에 걸친 ID 2개다. 두 ID는 각각 1개 인용 9행과 0개 인용 1행을 갖는다. 따라서 본문 303과 군 합계 305를 단순 오탈자로 고치지 않는다. `num_citation`이 원 배정인지 실제 표시인지 이 예외를 해명하는 코드/배정 로그가 필요하다. 원저의 “citation checking”은 hover로 URL을 표시한 사건이며 `mouseover`는 횟수, `mouseover1`은 이진 지표다. 외부 페이지 열기·체류·독해는 **미확인**이다. 1–10 신뢰 점수를 수락 정수로 바꾸는 검사는 **미실시**이며 수행해서는 안 된다.

## 3. 나머지 패키지와 중단 이유

Fendt는 [SPSS 분석 명령](https://osf.io/download/tg6ky/) 전체와 [영문 원과제](https://osf.io/download/8k5rh/) 1·3–6쪽 및 [독일어 통제 설문](https://osf.io/download/zqe97/) 3·6쪽을 읽었다. `Data.sav` SHA256은 `e79429b6314cb6e497102b989f14f4b72a0d73be3a968e9b195f10b7d020a3bd`다. SPSS/pyreadstat가 없어 SAV 원행 파싱·원분석 실행은 **미실시**다. 다만 모든 군에 같은 원문 링크를 제공하고 신빙성 1–7을 평정하는 과제이므로, 접근 조작·범주 수락 기준의 탈락 판단에 그 실행은 필요하지 않다.

Kobayashi [Dataverse](https://doi.org/10.7910/DVN/GWISTQ)는 DOI·랜딩·공개 API를 시도했으나 403이었다. 논문에 평균·비율이 있어도 수락 정수는 역산하지 않았다. 재개 첫 행동은 정상 공개 다운로드가 가능한 저자 판본/파일 ID를 확보하여 배정, 최종 true/false, 중도탈락, 검색 대상 열을 읽는 것이다. 현재는 검색 전 주장이 달라 접근만의 적격 대비도 아니다.
