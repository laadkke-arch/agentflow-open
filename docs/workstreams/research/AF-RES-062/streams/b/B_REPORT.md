# AF-RES-062 · B 모집틀 인계 — 부분 인계

**원문 접근을 부여했다는 사실과 잘못된 주장을 걸러냈다는 결과를 연결할 수 있는 공개 비교는 제한적이다.** B에서 확인한 잠정 적격은 Aslett 등의 **검색을 하도록 배정한 I2 묶음**이다. 이는 동일한 근거 절 링크의 클릭 가능성만 바꾼 실험이 아니다. 더 이른 후보의 방법 및 링크 클릭 가능성이 미해결이므로 확정된 최초 적격이라고 부르지 않는다. B02·B03은 비워 둔다. 공개 결과가 없어서 생긴 공석만이 아니라 적격 방법 확인의 결손도 포함한다.

읽기: [corrected-order.json](corrected-order.json) → [frame.csv](frame.csv) → [sources.jsonl](sources.jsonl) → [stimuli.csv](stimuli.csv) → [outcomes.csv](outcomes.csv) → [hand-checks.json](hand-checks.json). 독립 재현의 원행 결합은 [보강 담당 코드](../supplement/aggregate_aslett.py)와 [집계 원장](../supplement/aslett-aggregates.json)을 사용한다. B 담당은 원 논문 방법·자극·참값을 읽고 집계 분할·산식을 별도로 확인했으며 보강 담당의 원행 조인을 자신이 재실행했다고 주장하지 않는다.

## 두 표에 옮길 B 근거

| 연구·표본층 | 배정 단위·N | 같은 항목·권고 근거 URL | 원문 제공 방식·동시 개입 | 실제 열람 측정 | 원문·참값 URL | 식별 범위·미확인 |
| --- | --- | --- | --- | --- | --- | --- |
| B01 잠정 · Aslett S1 | 사람 무작위화; 모집 3,006. 정오층별 원배정 N 미확인. 관측 정주장 C3,290/T3,205; 오주장 C1,188/T1,161 | [Methods Surveys/Study1](https://www.nature.com/articles/s41586-023-06883-y); 같은 날 동일 pool의 기사 중 3/5 배정; [Article_day 조인](../supplement/aslett-aggregates.json) | 양군 모두 평가할 원 기사 사이트를 봄. T만 별도 근거를 검색하고 질의·출처·URL을 보고. I2; 지시·노력이 함께 달라짐 | S1 보고 URL·검색어; 특정 원문의 로드/체류/독해 연결은 미확인 | [49기사/전문 검증자 키](https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Fact_Checker_Data_Master.csv); 독립 검증 원문의 실제 도착 절은 B에서 미확인 | 원배정 조건별 관측 응답 비교. 전체 ITT·고정 절 링크 효과·실제 독해 효과는 식별 못 함. 앞선 미해결 후보 때문에 최초 순번도 미확인 |
| B02 · 공석 | 미확인 | [프레임 심사](frame.csv) | 미확인 | 미확인 | 미확인 | 관측되지 않은 셀을 0/0으로 채우지 않음 |
| B03 · 공석 | 미확인 | [프레임 심사](frame.csv) | 미확인 | 미확인 | 미확인 | 같은 DOI의 별도 표·그림을 새 주 연구로 승격하지 않음 |
| 별도 반복 근거 · Aslett S5, B01 논문 내 다른 코호트 | 사람 배정; 공개 분석 행 오주장 C877/T608, 정주장 C1,782/T1,359. 원배정 N 미확인 | [Methods Study5](https://www.nature.com/articles/s41586-023-06883-y); 같은 24시간에 같은 기사 평가 | Google 검색 지시·보상 조건; 서로 다른 browser extensions. I2 | Google SERP를 ≥5초 유지해야 결과 캡처. URL 기록과 SERP 노출은 특정 출처 독해가 아님 | [고정 저자 패키지](https://github.com/SMAPPNYU/Do_Your_Own_Research/tree/7b4ffee080be622e06f6197bfd095a3e4faebd16) | 추가 주 자리로 세지 않음. 공개 이진값의 0은 거짓 판정과 판단 불가가 섞임. person-item 반복 키가 있어 분석 행을 독립 시행으로 단정하지 않음 |

C=검색 격려 없음, T=검색 격려. 아래 `수락`은 뉴스 중심주장을 **true라고 평가한 것**이며 AI 권고를 따른 행동과 동일한 종점은 아니다. 정오 키는 저자 전문 검증자 다수판정이다. 배정 N과 m은 모두 미확인이므로 `[a/N,(a+m)/N]`의 ITT 범위도 미확인이다.

| 코호트·조건·비교 | 정오층 | 배정·판정가능·결측 수 | 권고 수락 n/N | 최종정답 n/N | 조건차 %p | 원행·원표 URL과 위치 | 반대 해석·미확인 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B01 S1 관측 범주 응답 · C→T | 정주장 | 배정/결측 미확인; 관측 3,290→3,205 | 1,837/3,290→2,046/3,205 | 동일 | 수락/정답 +8.00189 | [Study_1_df_T.csv](https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Study_1_df_T.csv); [집계](../supplement/aslett-aggregates.json) groups | CND 871→690. 참주장 수락 개선을 오주장 선별 개선으로 바꿀 수 없음 |
| B01 S1 관측 범주 응답 · C→T | 오주장 | 배정/결측 미확인; 관측 1,188→1,161 | 356/1,188→420/1,161 | 387/1,188→367/1,161 | 오수락 +6.20938; 정답 −0.96508 | [Search_Exp_Misl_False.csv](https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Search_Exp_Misl_False.csv); Evaluation/Treat_Search/Article_day | CND 445→374. `수락하지 않음`은 FM+CND여서 정답과 다름 |
| B01 S1 저자 complete-case 감도 · C→T | 정주장 | 배정/결측 미확인; 분석 3,145→3,124 | 1,788/3,145→2,002/3,124 | 동일 | +7.23236 | 같은 고정 저자 파일; [보강 코드](../supplement/aggregate_aslett.py) complete-case 필터 | 공변량 완비 사례만의 분석. 원래 모집/배정 분모가 아님 |
| B01 S1 저자 complete-case 감도 · C→T | 오주장 | 배정/결측 미확인; 분석 1,145→1,130 | 343/1,145→411/1,130 | 382/1,145→361/1,130 | 오수락 +6.41535; 정답 −1.41554 | 같은 파일/코드; [손검산](hand-checks.json) | 논문 모집 N을 분모로 사용하거나 필터 결손을 0으로 처리하지 않음 |
| B01 논문 S5 별도 코호트 · C→T | 정주장 | 배정/결측 미확인; 분석 행 1,782→1,359 | 1,249/1,782→1,155/1,359 | 동일 | +14.89918 | [Study_5_df_T.csv](https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Study_5_df_T.csv) True_Dummy | 분석 행에 person-item 반복 키 있음; 초대·탈락 분모와 다름 |
| B01 논문 S5 별도 코호트 · C→T | 오주장 | 배정/결측 미확인; 분석 행 877→608 | 346/877→298/608 | 미확인 | 오수락 +9.56048; 정답차 미확인 | [Study_5_df_FM.csv](https://raw.githubusercontent.com/SMAPPNYU/Do_Your_Own_Research/7b4ffee080be622e06f6197bfd095a3e4faebd16/Data/Study_5_df_FM.csv) True_Dummy | `True_Dummy=0`을 정답으로 치환하지 않음. CND 수와 실제 독해 여부 미확인 |
| B02/B03 · 공석 | 정권고 | 미확인 | 미확인 | 미확인 | 미확인 | [frame.csv](frame.csv) | 확인되지 않은 분모 |
| B02/B03 · 공석 | 오권고 | 미확인 | 미확인 | 미확인 | 미확인 | [frame.csv](frame.csv) | 확인되지 않은 분모 |

## 모집·독해 분모와 정정

후보 메타데이터는 `10de6313282ba8cfeeec75057050056ef8b74bad`의 [candidate-freeze.json](candidate-freeze.json)에 고정됐다. COR의 실제 보이는 연구 8건, DIG 연구 목록 50개 제목 중 주제에 맞는 19건, 추가 출판사/저자 경로의 14건을 합쳐 후보 33행을 기록했다. 제목 자체에 결과 방향이 포함되거나 검색 초록이 결과를 노출했으므로 완전한 결과 눈가림이라고 부르지 않는다. 본격 결과표 독해 전의 적격 규칙·메타데이터 고정이다.

최종 발행 창 안의 논문은 원동결 기준 27건이었고 그 첫 25건을 심사 대상으로 삼았다. 이후 **Internet or Archive**의 출판사 Notes 1–2가 2019 Expertise와 같은 참가자임을 명시하여 합쳤다. **See Something**과 **I Do Not Believe You**는 동일한 2016년 봄 613명 모집·같은 학교·반복참여 43명 제외·Notes1의 서로 보완되는 플랫폼/출처/알고리즘 조건 제외를 명시하여 한 계보로 보수적으로 합쳤지만 개인 식별자 교차표는 미확인이다. C45/social48 정수는 Bode 논문에만 명시되어 두 논문 간 셀 정수 일치를 직접 확인했다고 부르지 않는다. 이 두 정정으로 원래 26·27번인 Badrinathan 및 Brown이 corrected first25에 들어왔다. Ziv/Bene의 실제 2022년 11월 권호를 확인해 연도만 있던 정렬 placeholder도 수정했다. 모두 [정정 전후 원장](corrected-order.json)에 남겼다.

정정 후 **25단위**의 직접 방법 검토 상태는 다음과 같다.

| 상태 | 실제 단위 수 | 의미 |
| --- | ---: | --- |
| 원저의 방법 직접 독해 | 14 | 저자/출판사판 또는 신원이 제한된 공개 fulltext mirror; 출처별 provenance 명시 |
| 저자 전구 보고서 및/또는 원 자극만 독해 | 2 | Civic Preparation 전구판, district 전구판/부록. 최종판 동일성이 일부 미확인 |
| 저자 원 질문지의 방법만 독해 | 1 | Fendt; 세 군 모두 링크 제공을 명시하므로 접근 개입 제외 근거 확보, 논문 완독은 아님 |
| 개념 리뷰 본문 독해 | 1 | Critical Ignoring; 새 사람 연구 없음 |
| 리뷰 metadata만 확인 | 1 | Teaching Lateral Reading; 본문 독해 수에서 제외 |
| 원저 방법 접근 실패 | 6 | Learning to Evaluate, Who Is Behind This, Challenging Approaches, Guiding Their Thinking, Conversations After Lateral Reading, Misinformation Is Contagious |

따라서 완료한 25건의 원저 방법 완독으로 보고할 수 없다. **잠정 적격 I2 1, 보류 8, 제외 16**이다. 보류 8은 접근 실패 6, Vraga 실제 클릭 가능성 1, district 최종판 방법/표본 차이 1이다. Civics와 HKS 2024의 부분 코호트 중복 가능성, curriculum report와 최종판의 464 대 499명 차이도 추가 연대/분모 불확실성이다. 반대로 모든 링크가 같았던 교육 연구를 일부러 적격으로 만들어 빈자리를 채우지 않았다.

접근 복구는 출판사, DIG/COR/저자 연구목록, UMD TRAILS, Stanford SDR/IIIF, LMU·Technion 저자 저장소, OpenAlex OA 위치, SSRN, 공개 본문 mirror까지 실제 시도했다. 저자 연락은 하지 않았다. 복구 경로와 실패는 [search-log-addendum.jsonl](search-log-addendum.jsonl), 실제 HTTP 상태·해시는 [retrieval-log.jsonl](retrieval-log.jsonl), OA 원장은 [openalex-recovery.json](openalex-recovery.json)에 있다. 검색 도구가 질의별 반환 수/네이티브 URL을 제공하지 않은 경우 `미확인`으로 기록했다. post-read UTC 상한은 정확한 최초 열람 시각으로 가장하지 않았다.

B 자료 원장은 22행, 계보를 보수적으로 합친 최소량 산입은 **17저작**이다. 그중 사람 원저 보고서 14, 사람을 실험하지 않은 도서관 지침 원분석 1, 독립 참값 원전 2다. 한 논문 부록, Fendt OSF 패키지(보강 담당과 중복), 동일 코호트 논문, 리뷰는 별도 저작 수로 더하지 않았다. 최종 공동 원장의 계보 통합이 우선한다. 이 수는 연구 코호트 수·적격 대비 수·관측 시행 수와 다르다.

## Q1 · 무엇이 실제로 같았는가

Aslett S1은 같은 일자의 원 기사 pool, 같은 최종 범주 척도, 사람별 조건을 확인할 수 있다. 그러나 사람마다 3/5 기사를 받아 모두 같은 문항을 전부 본 것은 아니다. 검색자는 같은 원 기사에서 출발하더라도 후속 검색 결과·근거 URL을 자유롭게 선택했다. 검색 지시와 시간 부담도 조건에 포함된다. I1 고정 원문 링크만의 효과라고 옮길 수 없다. [B-S08, Methods Surveys/Study1](https://www.nature.com/articles/s41586-023-06883-y)

Vraga의 같은 오정보·반박 문구에서 Snopes/CDC preview를 넣은 조건은 더 가까운 후보지만 **실제로 클릭 가능한 링크였는지**를 공개한 화면/실험 앱에서 확인하지 못했다. 부록의 Facebook-with-source 한 장과 Twitter-without-source 한 장은 같은 플랫폼의 모든 문항이 동일하다는 검증이 아니다. 아무것도 바로잡지 않은 control은 아예 오정보 post가 없어 그 비교를 동일 주장 노출로 해석해서도 안 된다. [B-S01 Methods1342–44/Appendix1353](https://lbode.wordpress.com/wp-content/uploads/2021/01/vraga-and-bode-2018-i-do-not-believe-you-how-providing-a-source-corrects-health-misperceptions-across-social-media-platforms.pdf)

Panizza와 Fendt는 양군/세 군 모두 외부 원문 접근이 가능했다. 전자는 popup/incentive, 후자는 교육·연습·서로 다른 소요시간을 바꿨다. 교육 전체가 효력을 보였더라도 링크를 제공한 효과와 다르다. [B-S05 Experiment1 Design](https://www.nature.com/articles/s41598-022-09168-y), [B-S22 pp1,3–6](https://osf.io/download/8k5rh/)

**자기 결론 반증 경로:** 최초에는 source correction·lateral reading 연구가 접근 효과의 직접 근거일 가능성을 열어 두었다. 원 화면과 지시에서 “같은 접근+추가 교육”을 발견하여 제외했다. Vraga의 실제 배포 앱/Qualtrics export에서 클릭 가능한 외부 URL과 no-source counterpart가 확인되면 이 보류는 뒤집힐 수 있다.

## Q2 · 원문의 어떤 절이 검증하는가

Zika 연구에 실린 Snopes 및 CDC URL은 정확히 추출했지만 현재 각각 402/404였고, 2016 Wayback CDX 조회도 도구 접근 실패였다. 이를 당시에도 막혔다고 해석하지 않았다. 해당 논문 참고문헌의 WHO 2016 원문은 별도 mirror에서 읽었다. GMO 모기가 브라질 Zika/소두증을 일으켰다는 근거가 없다는 절은 연구의 부정 키와 일치한다. 이는 Snopes/CDC의 실제 도착 절 검증을 대체하지 않는다. [B-S11 WHO p2](https://app.mhpss.net/?get=285/Dispelling-Rumours.pdf)

Wineburg 교사 과제는 AMF를 검색하고 GiveWell의 호의적인 평가를 찾도록 안내한다. 2018년 GiveWell 역사판은 효과·비용효과성을 호의적으로 평가하면서 조사 품질·늦은 모니터링·살충제 저항의 불확실성을 명시한다. 과제 키의 좁은 문장을 지지하지만 “이 사이트의 모든 보건 주장도 참”으로 일반화할 근거가 아니다. 과제에는 정확한 GiveWell 판 URL이 없으므로 우리가 확인한 2018판을 실제 학생 도착지라고 부르지 않는다. [B-S13 p4](https://supp.apa.org/psycarticles/supplemental/edu0000740/EDU_2020_0630_Supplemental_Materials.pdf), [B-S21 Summary/Major open questions](https://www.givewell.org/charities/amf/November-2018-Version)

Aslett의 전문 검증자 다수 키는 저자 참값의 연결 근거다. 이를 독립 원문이 실제로 그 기사의 모든 중심주장을 확정했다는 사실과 구별한다. Fendt 질문지는 참/거짓 기사 인덱스를 주지만 마지막 해설은 매체를 신뢰/의심 범주로 나누는 설명이다. 개별 주장의 독립 검증 원문을 그 해설만으로 복원할 수 없다. [B-S22 pp7–8](https://osf.io/download/8k5rh/)

**뒤집힐 최소 증거:** 실험 당시 URL 스냅숏·도착 절·주장 범위의 직접 연결, 검증자 판단의 이유/정정. 현재의 발행자 홈이나 로고는 대체 입력이 아니다.

## Q3 · 배정, 열기, 읽기

S1은 사람에게 추가 검색을 **배정**했고 입력된 검색어/근거 URL을 수집했다. 그 URL 입력만으로 브라우저가 독립 출처를 로드하고 해당 절을 읽었다고 확정할 수 없다. S5의 Google 결과 캡처 역시 ≥5초 SERP 조건이지 읽기 이해 측정이 아니다. control의 URL historian와 treatment의 SERP saver가 달라 측정 도구/참여 부담도 동시 변경됐다. S5의 postconsent 탈락은 C20%/T62%로 저자가 보고한다. 방법의 653개 T 평가 중 508개 trace와 최종 608개 T 분석 평가도 다른 모집단일 수 있으므로 하나의 동일 분모로 강제하지 않았다. [B-S08 Study5/Digitaltrace Methods](https://www.nature.com/articles/s41586-023-06883-y)

COR 교육 보고서의 서술형 답안에서 lateral reading을 코딩하는 것은 관찰 가능한 결과다. 그 코딩이 실제 브라우저 이벤트나 이해를 직접 측정한 것인지는 별도다. Expertise 연구처럼 화면 녹화를 한 관찰 연구도 있지만, 전문 factchecker와 학생의 차이는 원문 접근을 배정한 효과가 아니다. [B-S15 Methods](https://stacks.stanford.edu/file/druid%3Ayk133ht8603/Wineburg%20McGrew_Lateral%20Reading%20and%20the%20Nature%20of%20Expertise.pdf)

**반증 시도와 남은 입력:** event dictionary와 screen flow를 찾아 배정과 실행이 같은지 확인했다. 로그가 없는 연구의 읽기는 미확인으로 남았다. 재개하려면 배정 명단→예정 item→페이지 load→외부 URL/절→최종 응답이 연결되는 공개 이벤트 정의가 필요하다.

## Q4·Q5 · 정오별 정수와 분모

S1의 `ResponseId + Article_day`로 범주 응답, 배정 `Treat_Search`, 저자 truth key를 조인한 결과를 보강 담당이 제공했다. `Evaluation`의 T/FM/CND는 7점 평균을 임의 절단한 값이 아니다. 원저 전체모집 N=3,006을 정오층 분모로 쓸 수 없고, 파일의 NA에는 배정되지 않은 3/5 바깥 문항도 섞인다. 탈락 및 attention 제외 원배정 명단이 없어 m 역시 미확인이다. [원행 결합 코드](../supplement/aggregate_aslett.py), [패키지 판/해시/조인 검사](../supplement/aslett-aggregates.json)

오주장 관측 응답의 손검산은 C `356+387+445=1,188`, T `420+367+374=1,161`이다. 거절 수는 C `387+445=832`, T `367+374=741`이므로 거절을 정답으로 세면 오답/판단 불가를 정답에 더한다. 저자 complete-case에서도 C `343+382+420=1,145`, T `411+361+358=1,130`으로 따로 맞춘다. [hand-checks.json](hand-checks.json)

단순한 조건차는 `100*(aT/DT-aC/DC)`이며 사람/문항 군집을 무시한 유의성 추정을 새로 하지 않았다. 관측 전체 정확도는 S1 C `2,224/4,478=49.66503%`, T `2,413/4,366=55.26798%`로 +5.60295%p지만, 동시에 오주장 수락은 +6.20938%p다. 이 비교도 관측된 문항 구성과 원배정 결손에 조건부다. “전체 정확도 상승이면 잘못된 주장을 더 잘 걸렀다”는 결론을 반증하는 구체적인 정수 예다. [조건별 집계](../supplement/aslett-counts.csv)

S5의 공개 `True_Dummy`는 범주 T 수락을 나타내나 0에 FM/CND가 섞이므로 오주장의 최종정답은 미확인이다. 같은 person-item 중복 키도 남아 있다. 고정 저자 행을 임의 삭제하거나 서로 독립인 시행이라 부르지 않고 별도 반복 근거로 보존한다. 초기 판단을 가진 S2는 S1 control과 겹쳐 새 독립 코호트로 더하지 않았다.

## Q6 · 기대에 맞지 않는 자료

가장 직접적인 반례는 Aslett의 검색 격려에서 잘못된 주장 수락이 늘어난 결과다. 저자 설명은 신뢰 낮은 검색 결과로 이어지는 경우를 제시하지만 **노출된 결과의 질별 하위층은 무작위 배정되지 않았다**. 따라서 “낮은 질 결과가 증가 전부를 유발했다”는 기제 확정으로 높이지 않는다. [B-S08 main/Study5/ExtendedData](https://www.nature.com/articles/s41586-023-06883-y)

Vraga의 논문 제목/서술만 보면 source 제공이 오류를 줄인다고 읽히기 쉽지만, 직접적인 **source 있음 대 없음** 비교는 Bonferroni 보정 후 p=.24로 유의하지 않았다. source 있음 대 아무 오정보도 보지 않은 control 비교의 차이를 같은 주장에 링크만 붙인 효과로 대신하지 않았다. 이는 저자 평정 지수의 null 대비이고 수락 정수는 아니다. [B-S01 Results1344](https://lbode.wordpress.com/wp-content/uploads/2021/01/vraga-and-bode-2018-i-do-not-believe-you-how-providing-a-source-corrects-health-misperceptions-across-social-media-platforms.pdf)

다른 분야의 교육 보고서도 “밖으로 나갔다=올바로 판정했다”를 지지하지 않는다. 영양학 수업 87명 중 post의 lateral reading 시도는 67명이나 그중 올바른 결론은 36명, 틀리거나 무관한 결론은 31명이었다. 이는 자발적으로 시도한 층의 서술형 코딩이며 접근 배정 효과가 아니다. [B-S04 Finding2](https://misinforeview.hks.harvard.edu/article/lateral-reading-college-students-learn-to-critically-evaluate-internet-sources-in-an-online-course/)

Panizza E1의 popup은 전략 보고를 바꿨으나 accuracy는 저자 보고상 null이었다. Badrinathan의 factchecker 명칭 조건은 실제 fact-check 링크를 주지 않았다는 한계가 Discussion에 명시돼 있다. 이런 null을 “원문 접근이 소용없다”의 증거로 쓰는 것도 과장이다. Brown의 정확성 prime null도 같은 링크 비교가 아니므로 진단층에 남겼다. [B-S05 Discussion](https://www.nature.com/articles/s41598-022-09168-y), [B-S09 p15](https://pimlab.org/wp-content/uploads/2023/04/19401612231158770.pdf), [B-S19 Methods/Discussion](https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjdp.12559)

반증 탐색은 유익한 교육 논문만 모으지 않고 검색 격려 역효과, 링크 없는 출처명 correction, 잘못된 출처 추론, 교실 사전/사후·관찰 전문가 비교, 내용 오류 대 외관 오류 과제를 함께 읽었다. “맞는 권고도 더 거절했다”는 동일 고정 절 접근 대비의 직접 정수 셀은 회수하지 못했다. 그 방향이 존재하지 않는다는 뜻이 아니며, 정주장 수락이 줄어드는 독립 반복이나 미해결 초기 논문의 원자료가 있으면 결론은 달라진다.

## Q7 · 설계자에게 허용되는 문장

| 관점 | 근거가 허용하는 판단 | 넘으면 안 되는 추론 | 다음 최소 공개 입력 |
| --- | --- | --- | --- |
| 소프트웨어·검색 UI | 특정 주장에 검증할 외부 원문/절을 제공했다는 UI 상태를 기술할 수 있다 | 전체 정확도·신뢰도 상승만으로 오권고 선별 향상이라 부르기 | 같은 항목·권고·순위·문구의 링크만 다른 조건과 최종 정오층 정수 |
| 수업 출처 검증자 | 교육 뒤 외부 출처를 사용한 답안이 늘었고 잘못된 추론도 남았다고 기술 | 교육/연습/시간 전체를 원문 링크 한 기능의 효과로 환산 | 동일 문제·접근 조건을 고정한 교육 성분 구분, 실제 도착 URL/근거 절과 채점 근거 |
| 뉴스 factchecker | 검색을 배정해도 오정보 endorsement가 늘 수 있어 출처가 주장을 실제 지지하는지 확인 필요 | 그럴듯한 매체명·현재 홈페이지·다수 판정만으로 역사적 중심주장을 자동 확정 | 기사 당시판, 독립 검증 원전, 검증자 불일치·정정·CND를 함께 보존 |
| 실험 방법론자 | 원배정 조건에 따른 관측 응답 정수를 보고하고 클릭층을 별도로 기술 | 자발 클릭층이 원래 달랐을 가능성·탈락을 지운 인과효과 | 배정 명단, 예정/노출 문항, 순서/기간, 초기 응답, 탈락 사유, 이벤트 사전과 최종 응답 |

“제공했다”는 전달·UI 상태, “열었다”는 적절히 정의된 로드/클릭 기록, “오류를 걸러냈다”는 잘못된 주장 수락의 감소를 따로 입증해야 한다. 부품 선택·채택·재작업·시간으로 옮기려면 해당 도메인의 실제 공개 시행에서 추천 방향, 참값과 대안의 기능적 적합성, 최초 일치, 최종 선택/기권, 수정·재작업을 함께 연결해야 한다. 이것은 **다음 자료 요건**이지 이번에 새 참가자를 모집하거나 기존 AF058 원행을 재분석했다는 결과가 아니다.

## 검사와 재개

B 범위의 JSON/JSONL parse, CSV row counts, source ID 연결, 원동결33행 보존, corrected25 상태 분모, 정오층 수락/정답/기권 산술을 검토했다. 통합 `workbench.session check`·Git 커밋·원격 고정판 재열람은 부모 담당이다. B는 git mutation을 하지 않았다. 원자료와 저작 전체 PDF는 ignored cache에만 있으며 공개 집계·요약·출처/해시만 인계한다.

가장 먼저 [corrected-order.json](corrected-order.json)의 보류 8과 [search-log-addendum.jsonl](search-log-addendum.jsonl)을 연다. 자동 생성 표는 소유 경로 안에서 `python docs/workstreams/research/AF-RES-062/streams/b/build_records.py`, `build_tables.py`, `build_evidence.py`, `record_recovery.py` 순으로 재생성할 수 있다. `build_evidence.py`는 보강 담당 집계 파일을 읽으며 원행을 추가 분석하지 않는다. 판정 변경 시 원동결을 덮지 말고 correction 항목을 추가해야 한다.

| 불일치·약점 | 영향받는 주장 | 직접 근거 URL·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 더 이른 6논문 방법 실패, source preview 클릭성 미확인, 최종판/전구판 464 대 499 불일치 | B의 최초 적격과 빈자리 확정 | [frame.csv](frame.csv), [정정 원장](corrected-order.json), [Vraga Appendix1353](https://lbode.wordpress.com/wp-content/uploads/2021/01/vraga-and-bode-2018-i-do-not-believe-you-how-providing-a-source-corrects-health-misperceptions-across-social-media-platforms.pdf) | 보류 DOI 저자 수락원고·실험 screen flow·원 앱 export 회수 | 앞선 적격 동일항목/독립원문 접근 대비가 확인되거나 실제 클릭 불가가 확정됨 |
| Aslett 원배정 정오층 N/m·개별 독해·일부 독립 참값 도착 절 미확인 | ITT 수락률 범위, 읽기의 인과효과, 링크 절 자체의 효과 | [Methods Study1/5](https://www.nature.com/articles/s41586-023-06883-y), [조인 감사](../supplement/aslett-aggregates.json) | 배정/노출 roster, event dictionary, 당시 독립 원문 및 정정판 | 결손을 포함한 정수와 고정 절 접근 대비가 결합되며 관측 방향이 유지/반전됨 |
| 교육·출처명·관찰 그룹과 원문 접근을 혼합할 위험; 수락 종점도 AI 권고가 아님 | 제품의 오판/채택/재작업 감소라는 이식 주장 | [Panizza Design](https://www.nature.com/articles/s41598-022-09168-y), [Fendt pp3,5](https://osf.io/download/8k5rh/), [Badrinathan p15](https://pimlab.org/wp-content/uploads/2023/04/19401612231158770.pdf) | 같은 권고·같은 항목의 공개 시행에서 링크·초기 선택·최종 결정·기권·재작업 연결 | 접근 성분과 판단 정오가 분리되어 제품에 해당하는 분모가 직접 회수됨 |
