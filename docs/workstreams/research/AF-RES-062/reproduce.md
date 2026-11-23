# 공개 자료 판·재현 명령·원개수 손검산

## 1. 작업 계약과 판

저장소 `laadkke-arch/agentflow-open`, 브랜치 `work/research-af-res-062`, 실제 시작 커밋 `1e741fd0def88ef56b1060a478d81f1985a4e760`. [manifest.json](manifest.json)과 [시작 영수증](evidence/session-start.json)은 root AI가 실제 실행한 계약의 결과다. 선행 AF-RES-058은 코호트 중복 확인에만 사용했고 기존 참가자 원행은 재분석하지 않았다. 모든 새 파일은 소유 경로 안에 있으며 원 참가자별 응답·저작권 원문 캐시는 커밋하지 않는다.

시작 명령은 배정 브랜치에서 다음과 같이 실행되어 exit0이었다.

```bash
python -B -m workbench.session start af-res-062 --allow docs/workstreams/research/AF-RES-062/ --dependency work/research-af-res-058=fefeb2146c7f63e49d0578f78989be49acd63291 --output docs/workstreams/research/AF-RES-062/manifest.json --fetch
```

최종 계약 검사는 다음 명령이며 실제 실행 SHA/시각/주체/출력은 `evidence/session-check.json`을 확인한다. 이 명령의 통과는 Git 범위·의존성 계약을 검사한 것이지 연구 정답성이나 최소 독해량을 보증한 것이 아니다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-062/manifest.json --fetch
```

## 2. Aslett Study1 — 원 배정군에 따른 관측 범주 집계

원 패키지: [SMAPPNYU/Do_Your_Own_Research, 고정 SHA 7b4ffee080be622e06f6197bfd095a3e4faebd16](https://github.com/SMAPPNYU/Do_Your_Own_Research/tree/7b4ffee080be622e06f6197bfd095a3e4faebd16). 저자 코드 [Main_text_Figures.R](https://github.com/SMAPPNYU/Do_Your_Own_Research/blob/7b4ffee080be622e06f6197bfd095a3e4faebd16/Code/Main_text_Figures.R)의 Study1 부분은 `Study_1_df_FM.csv`를 읽고 77행에서 `na.omit`한 후 문항 고정효과·사람/문항 군집을 쓰는 모델을 적합한다. 이번 작업은 그 회귀를 독립 시행처럼 다시 검정하지 않고 범주 정수만 센다. 원저의 조정된 효과 +0.057과 이번 무조정 정수 차이 +0.06415는 서로 다른 추정량이다.

| 입력 | 실제 필드와 역할 | 확인 결과/한계 |
| --- | --- | --- |
| `Data/Study_1_df_FM.csv` | `ResponseId`,`Article_day`,`Treat_Search`,`Susc_FN`, 공변량, `Likert_Evaluation` | 3966행. 공개 축약파일 전체 열의 NA 제거로 저자 분석 표본 구성. |
| `Data/Search_Exp_Misl_False.csv` | 같은 두 키, `Evaluation`=`True`/`Misl/False`/`CND`, `mode`, `True_Dummy`, `Susc_FN` | 두 키의 일대일 조인 3966/3966. 파생 이진열과 최종 범주 불일치 관측0. |
| `Data/Study_1_df_T.csv` | `Evaluation`=`T`/`FM`/`CND`, `True_Dummy`,`Article`,`Treat_Search`, 공변량 | 10783 파일행. `Article`1–5, 저자 모델 변수의 완전사례를 별도로 집계. |
| `Data/Fact_Checker_Data_Master.csv` | `Article_day`, `Pariticipant_1_Eval`…`Pariticipant_6_Eval`, `link` | 연결된 정오 항목49개의 전문가 최빈값을 원 파일의 키와 대조, 불일치 관측0. 독립 원전으로49건 모두 참값을 확증한 것은 아님. |

정주장 T/오주장 FM에 대해 수락은 최종 평가가 T인 경우다. 이는 **뉴스 주장을 참으로 받아들임**이며 AI의 행동 권고를 따름과 같은 종점이라고 일반화하지 않는다. 최종정답은 T항목에는 T, FM항목에는 FM이다. CND는 기권/판정불가라는 관측 세 번째 범주로 두므로 FM항목에서 `1−수락률`을 정확도로 쓰지 않는다. Study1에는 동일 항목의 사전 최종답이 없어 초기부터 권고와 같았던 시행은 미확인이다.

### 재현 명령

저장소 루트에서 실행한다. 첫 명령은 고정 URL을 회수하고 해시를 검사해 aggregate를 만들며 원행은 `streams/supplement/cache/`에만 저장한다. 두 번째는 root가 별도 작성한 stdlib 집계로 동일 정수인지 확인한다. 실제 실행자는 각각 supplement AI와 root AI이며 서로 다른 코드의 검산이지 인간 독립 심사나 새 참가자 복제는 아니다.

```bash
python -B docs/workstreams/research/AF-RES-062/streams/supplement/aggregate_aslett.py --fetch
python -B docs/workstreams/research/AF-RES-062/streams/root/independent_recount.py
```

입력의 SHA256은 [aslett-aggregates.json](streams/supplement/aslett-aggregates.json)의 `inputs`, 결과는 `groups`와 `contrasts`에 있다. root 검산의 입력 해시·정확한 분수·원행 위치는 [independent-calculation.json](streams/root/independent-calculation.json)에 있다. 외부 호스트가 막히면 해당 `inputs[].url`의 같은 고정 바이트를 파일명대로 제공한 뒤 `--fetch` 없이 실행하면 된다.

### 양 군 원행과 원개수 손검산

[Search_Exp_Misl_False.csv](https://github.com/SMAPPNYU/Do_Your_Own_Research/blob/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Search_Exp_Misl_False.csv)의 헤더 제외 레코드155는 `Article_day=nov 20_1`, `Treat_Search=0`, `mode=Misl/False`, `Evaluation=True`, `Susc_FN=1`이다. 레코드16은 같은 항목에서 `Treat_Search=1`, 나머지 해당 값이 같다. 두 원행 모두 축약 파일의 완전사례 키 집합에 속한다. 각각 수락1·정답0으로 세었다. 참가자 ID는 재게시하지 않고 두 키의 SHA256을 검산 JSON에 남겼다.

| 저자 완전사례 | 최종 T | 최종 FM | 최종 CND | 손으로 더한 분모 | 수락/최종정답 |
| --- | ---: | ---: | ---: | ---: | --- |
| 오주장, 통제 | 343 | 382 | 420 | 343+382+420=1145 | 수락343/1145; 정답382/1145 |
| 오주장, 검색 | 411 | 361 | 358 | 411+361+358=1130 | 수락411/1130; 정답361/1130 |
| 정주장, 통제 | 1788 | 564 | 793 | 1788+564+793=3145 | 수락=정답1788/3145 |
| 정주장, 검색 | 2002 | 459 | 663 | 2002+459+663=3124 | 수락=정답2002/3124 |

오수락 차이: `100×(411/1130−343/1145)=+6.4153495382%p`.
오주장 최종정답 차이: `100×(361/1130−382/1145)=−1.4155427600%p`.
정주장 수락/정답 차이: `100×(2002/3124−1788/3145)=+7.2323607783%p`.

공변량 결측까지 포함한 모든 **관측 범주**를 세면 오수락356/1188→420/1161(+6.20938%p), 오주장 정답387/1188→367/1161(−0.96508%p), 정주장 수락1837/3290→2046/3205(+8.00189%p)다. 이 두 표본을 합치지 않는다. 원 배정 인원 전체·정오별 배정 시행 N과 탈락 m은 미확인이다. 5개 중 미제시된 문항과 미관측이 파일 NA에 섞여 있으므로 NA818/799 등은 배정 후 결측 수가 아니다. `[a/N,(a+m)/N]` 범위는 미확인이다.

### Study5 보조 대조

같은 논문의 다른 코호트 Study5는 [aslett-aggregates.json](streams/supplement/aslett-aggregates.json)의 별도 `ASLETT2024-STUDY5` 행이다. `True_Dummy`의 관측 이진 수락만 집계하고, FM항목의 이진0에 FM와 CND가 섞이므로 최종정답은 미확인이다. 사람+항목 키는 FM파일 1개, T파일 2개가 중복된다. 원 저자 행을 보존하며 이를 유일 시행으로 속여 세거나 조용히 한 행씩 제거하지 않았다. 본문의 주 재현 표는 키 유일성이 확인된 Study1이다. Study5를 주 슬롯이나 별도 보강 슬롯으로 중복 배정하지 않는다.

## 3. SIGIR TransparentCIS — 같은 자극과 노출 필드

원 패키지는 [iai-group/sigir2024-transparentCIS, SHA065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d](https://github.com/iai-group/sigir2024-transparentCIS/tree/065ae48c802e5fcaf9f4c202fad6bfb0aaf0650d)다. [audit_transparent_cis.py](streams/a/audit_transparent_cis.py)와 [집계](streams/a/transparent-cis-audit.json)는 `Input.query_id`1–10 및 `Input.response`를 실제 비교한다. EC1↔EC9, EC3↔EC10은 각각10/10문항의 문자열이 동일하고 EC2↔EC9, EC4↔EC10은 문구가 달라 동일하다고 묶지 않는다. 각 조건16명×10문항=160평정이며 열 조건 전체는160명·1600평정이다.

perfect/imperfect는 사실 오류뿐 아니라 편향·불완전한 답변을 포함하므로 순수 정권고/오권고로 치환하지 않는다. 조건/HIT 무작위배정은 미확인이고 문항 순서 무작위화만 확인했다.

`Answer.correctness_{id}.option_{1..4}`와 `Answer.factuality_{id}.option_{1..4}`는 4점 평정이다. 최종 답/선택 수락 변수는 해당 없음이다. 문자열 `TRUE/FALSE`의 대소문자 처리를 확인한 정정 내역을 streams/a에 보존한다. `Answer.p_clicked_details`와 `Answer.p_clicked_links`의 비어 있지 않은 셀은 클릭 필드의 존재를 뜻하지만 URL 도착·체류·이해를 보증하지 않는다. 273제출 중113제외의 원행은 공개 파일에 없고, 이 파일의160명을 최초 배정 N으로 바꾸지 않는다.

## 4. Kim 2025 — 정수 회수의 경계

[원저](https://arxiv.org/pdf/2502.08554v1) §4와 [사전등록](https://aspredicted.org/bg22-yfw7.pdf)의 within-person 8조건,12문항 풀,320수집/308분석을 확인했다. Table1의 반올림된 수락/정답 평균은 직접 정수 교차표가 아니다. 알려진 분모에 백분율을 곱해 반올림해 정수를 만드는 작업은 **미실시**다. 저자는 클릭318·비클릭914시행과 클릭층 정권고164·오권고154를 직접 보고한다. 출처 제공 분모1232는318+914의 산술 합계이며308명×4조건과도 일치한다. 클릭층 수락 분자는 미확인으로 둔다. 원자료가 생기면 참가자·문항·조건·정오키·최종선택·초기선택·제외마스크를 같은 시행으로 결합해야 한다.

원문 참값의 감사는 [source-audit.md](streams/root/source-audit.md)에 있다. USGS2024-08-01 및 NLM2024-06-13 보관판을 직접 읽고 전송/본문 해시를 보존했다. 이것은 당시 가능한 원문의 확인이며 참가자의 실제 클릭 내용 복원은 아니다.

## 5. 수행하지 않은 검사와 필요한 입력

독립 참가자 모집, AF058 원행 재분석, AF054 시간 재추정, B03의8/14와 그림50% 재추정, 없는 배정/클릭 데이터의 생성, 평균에서 수락 정수 역산, 반복 시행을 독립으로 둔 유의성 검정은 수행하지 않았다. 원 실험 앱의 접속/저장 동작이 현재 살아 있는지를 실제 참가자로 재실행하지 않았다. 이러한 검사를 했다고 주장하지 않는다.

각 선정 자리에서 끊긴 자료와 재개 입력은 [SELF_CHECK.md](SELF_CHECK.md)와 [acceptance-evidence.json](evidence/acceptance-evidence.json)에 연결되어 있다. 최종 고정 결과 재열람·로컬 링크 검사는 `evidence/fixed-result-review.json`에 기록한다.
