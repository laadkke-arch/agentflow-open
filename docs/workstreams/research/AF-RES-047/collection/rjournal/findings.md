# The R Journal 소비자 우선층: 고정 3건

관측 결과는 **발행자가 구별하는 후보판 존재 P=3/3, 소비자의 특정판·파일 선언 U=1/3, 원래 실행과 입력 연결 R=0/3, 실제 사용판의 해당 값 독립 검증 V=0/3**이다. RJ03의 발행자 후보 파일로 동일 필드를 계산한 결과는 candidate_value_checked=1/3에만 남겼다. 엄격 양성은 0/3이며, 원래 사용판·실행의 독립 기준을 전제로 하는 조건부 비율의 분모는 0이므로 **해당 없음**이다.

통합 원장 cases.json과 consumers.csv, editions.csv, runs.csv, readings.csv에는 각각 3, 3, 21, 3, 9행이 있다. P는 실제 소비한 전체 입력 행렬의 복구를 뜻하지 않는다. U는 구체적 파일 선언이고, 실제 실행에서 그 바이트를 읽었다는 R과 다르다.

## 1. 선정과 시간 순서

[2022 첫 호](https://journal.r-project.org/issues/2022-1/)의 연구글 22편과 [다음 호](https://journal.r-project.org/issues/2022-2/)의 18편을 노출해 개별 발행일·문서 식별자로 정렬했다. 첫 30노출은 첫 호 22편과 다음 호 첫 8편이다. frame_all_metadata.json은 전체 40개 메타데이터와 실제 GET 시각·해시, frame.csv는 고정 첫 30편을 보존한다. 이후 글을 더 좋은 보존 성과 때문에 교체하지 않았다.

| 순서 | 원문·위치 | 선정·제외 |
|---|---|---|
| 1 | [RJ-2022-001](https://journal.r-project.org/articles/RJ-2022-001/) §4 | 가정한 nuisance parameter와 delta로 모의자료 생성. 배경의 실제 연구 수치는 투입 자료가 아님. |
| 2 | [RJ-2022-003](https://journal.r-project.org/articles/RJ-2022-003/) §4 | LHS/Sobol/sine 생성 예제. 수학 모형 인용을 자료 소비로 세지 않음. |
| 3 | [RJ-2022-004](https://journal.r-project.org/articles/RJ-2022-004/) §2–3 | 공식 census/statistics를 사용해 RJ01 선정. |
| 4 | [RJ-2022-005](https://journal.r-project.org/articles/RJ-2022-005/) §3–4 | exp/weib 모의 생존자료와 시뮬레이션. 외부 실제 입력 확인 못 함. |
| 5 | [RJ-2022-006](https://journal.r-project.org/articles/RJ-2022-006/) §2.1/Fig1 | CRAN 코드를 실제 분석해 RJ02 선정. 서론 Table1 지침 비교는 배경이며 이 코퍼스의 출력이 아님. |
| 6 | [RJ-2022-007](https://journal.r-project.org/articles/RJ-2022-007/) §5 | Iris를 실제 통계 예제에 사용해 RJ03 선정. |

006·007·008 본문을 목차 순으로 우연히 먼저 읽은 노출은 기록했다. 판·해시·실행 성과를 본 뒤 고른 것은 아니다. 발행자 조사 전에 목적·시간·필드를 selection_freeze.json에 고정했다. RJ01의 정확 Fig2 값이 없다고 Table2의 2.40으로 교체하지 않았다. RJ03의 runtime·error·node ID는 Iris 통계값이 아니어서 첫 통계 출력 ANOVA Species/Df=2를 택했다.

정확한 최초 웹 본문 UTC는 계측하지 못했다. sources.jsonl에는 확인 가능한 첫 프로그램 GET과 정밀도 한계를 함께 적는다. 필드 고정 완료는 **2026-11-22T22:09:48.058572+00:00**, 최초 발행자 웹 열람 기록은 **22:11:02 UTC**다. A/B/C는 구성별 자료를 고정한 자체 재판독이며 눈가림 평가가 아니다.

## 2. RJ01: 발행판과 연구 입력 행렬 사이의 빈자리

[소비자 §2–3](https://journal.r-project.org/articles/RJ-2022-004/)는 census 기준연도, 34개 소도시, 13지표, 0 대치 및 표준화 PCA를 설명한다. Fig2의 첫 PC1 분산에는 정확한 숫자가 없다. Table2의 반올림된 표준편차 2.40을 제곱해 정확한 5.76이라고 보고하지 않는다.

[INS 1992 결과 원장](https://www.recensamantromania.ro/rezultate-recensamant-1992/) Volumul1 table03과 Volumul2 목록은 발행자가 구별한 census 후보판의 존재를 확인한다. 그러나 소비자 13지표 전체와 발행자 표·파일의 대응 및 취득판은 미확인이다.

[부록 ZIP](https://journal.r-project.org/articles/RJ-2022-004/RJ-2022-004.zip)에는 shrinking_cities.r 하나만 있다. 12행의 research_data.xlsx는 ZIP에 없다. 17–21행은 sheet data_1992/data_2018에서 첫 행·열을 제외한 PCA를 지정하지만 47–57행의 biplot PCA는 다른 slicing을 쓴다. 이를 같은 34행이라고 합치지 않았다. C가 알려주는 것은 의도한 파일·변환이며 원래 실행이나 정확한 값이 아니다.

1992→2018은 대상기간 변화이지 검증한 발행판 정정 계보가 아니다. 보조 Table2에서 variance proportion은 두 기간 모두 0.44지만 cumulative는 44.2%와 44.0%다. 같은 반올림값이 다른 기간·행을 가리키는 반례다.

## 3. RJ02: 부록이 특정판 선언을 늘린 반증

[§2.1의 rsync 취득일](https://journal.r-project.org/articles/RJ-2022-006/)만 읽었을 때는 U를 미확인으로 두었다. §5가 지목한 [Zenodo 4026589](https://zenodo.org/records/4026589)는 개념 DOI4026588의 v1.0, 공개일2020-09-12다. 2차 R Journal 투고 시점 코드·자료라는 설명과 [고정 commit](https://github.com/chainsawriot/rstyle/tree/07a60457c88dbb20858441047f248d61ce2955c7)이 있어 당시 입력 명세를 더 읽었다.

[target_meta.RDS](https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/target_meta.RDS)의 49,696행은 path/mtime/pkg/year/desc를 갖는다. 그중 1998행 16개는 [1998 feature record](https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/data/syntax_feature_yr1998.RDS)의 16경로와 모두 일치한다. rstyle_1998_input_manifest.csv에 그대로 옮겼다. 이 기록 때문에 초기 U미확인을 **U=true**로 변경했다. 범위는 **1998 선택표본의 16개 filename/version**이다. 전체 미러 snapshot이나 소비 바이트까지 확정한 것은 아니다.

공식 CRAN Archive/Old의 지목된 tar파일 GET은 **16/16**, 전체 현재 바이트 SHA 계산은 **16/16**, 소비자 원 tar SHA 기록은 **0/16**이다. cran_1998_publisher_receipts.json은 주소·시각·해시·DESCRIPTION·R member 목록을 보존한다. 이 독립 대조는 지목한 발행자 파일의 존재를 확인하며 과거 실행을 증명하지 않는다.

저자 feature record의 386개 exported function에서 fx_assign True는 0이다. [figures.R Fig1 블록](https://github.com/chainsawriot/rstyle/blob/07a60457c88dbb20858441047f248d61ce2955c7/rjournal_submission/figures.R)은 NULL result를 제외해 true/함수수×100을 계산한다. C의 **0/386=0%**는 A의 그래프상 약0%보다 정밀하지만 **기록 재독**이다. 원 CRAN 파일을 동일 export 선택·lintr 환경으로 처리한 독립 값 검증은 아니다. 172개 R 소스에 대한 단순 '= function(' 토큰 탐색도 0이었으나 문법·문자열·export 문제 때문에 완전 검증으로 승격하지 않았다.

| 발행 파일 | 내부 DESCRIPTION Version | 관측의 의미 |
|---|---|---|
| [acepack_1.1.tar.gz](https://cran.r-project.org/src/contrib/Archive/acepack/acepack_1.1.tar.gz) | 1.0-4 | filename과 내부 Version이 다른 키다. |
| [class_5.2pl005-2.tar.gz](https://cran.r-project.org/src/contrib/Old/0.61/class_5.2pl005-2.tar.gz) | 5.2pl005-1 | 내부 Version만으로 조인하면 다른 판으로 배정할 수 있다. |
| [nnet_5.2pl005-2.tar.gz](https://cran.r-project.org/src/contrib/Old/0.61/nnet_5.2pl005-2.tar.gz) | 5.2pl005-1 | 반복 관측이며 접근 실패가 아니다. 정정 사유는 미확인이다. |

[acepack 목록](https://cran.r-project.org/src/contrib/Archive/acepack/)에서 1.1의 날짜는1998-03-25, 다음1.2-1은1999-08-19다. 1998 스타일 분석에 다음판을 넣으면 시간 목적이 바뀐다. 한 package의 다음판을 전체16파일 코퍼스의 다음판처럼 세지 않았다.

고정 README 7행에는 이전2019 포스터의 94million/20years 제목이 남는다. 본 논문108million/21years와 같은 단계라고 자동 판단하면 안 된다. config.R 2행의 종료연도는2019지만 target_meta에는2020행도 있다. 저장된 행과 필터를 통과한 행도 구별해야 한다.

## 4. RJ03: 동일 바이트·동일 결과가 실제 사용판을 특정하지 못함

[소비자 §5](https://journal.r-project.org/articles/RJ-2022-007/)의 Species Df=2와 [부록](https://journal.r-project.org/articles/RJ-2022-007/RJ-2022-007.zip) 62–68행의 Iris→ANOVA는 확인했다. 하지만 R/datasets release, 저장 Iris Rmonad 객체, 실행 ID는 없다. 앞의 toy sessionInfo를 이 실행에 붙이지 않았고 Fig3의1–4는 그래프 내부 노드 번호로 취급했다.

[공식 목록](https://cran.r-project.org/src/base/R-4/)에서 논문2022-06-21 전후의 [R4.2.0](https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz)(2022-04-22)과 [R4.2.1](https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz)(2022-06-23)을 연구자 후보쌍으로 골랐다. 두 tar 전체는 다르지만 src/library/datasets/data/iris.R의3,018바이트는 동일하다. 멤버 SHA256은 77af4424d5361afe1c46e7fb95bc4f95681f5515a586cb41c062b111c691dc5c다.

세 species 각50행의 literal에서 Df=3−1=2를 계산했다. 논문 뒤에 공개된4.2.1 URL에서 같은 바이트를 얻었다고 그 공개 release가 원 논문의 입력이었다고 말할 수 없다. 이전 파일의 동일내용 사용까지 부정하는 것은 아니다.

[UCI 기록](https://archive.ics.uci.edu/dataset/53/iris) Additional Information은35·38행의 정정을 알린다. [ZIP](https://archive.ics.uci.edu/static/public/53/iris.zip)의 두 파일은 날짜가 매겨진 연속판으로 확인한 것이 아니라 함께 게시된 변형이다.

| 객체 | primary Df | 보조 SumSq | 35행 Petal.Width | 38행 Petal.Length |
|---|---:|---:|---:|---:|
| R4.2.0/4.2.1 iris.R | 2 | 437.1028 →437.1 | 0.2cm | 1.4cm |
| UCI bezdekIris.data | 2 | 437.1028 →437.1 | 0.2cm | 1.4cm |
| UCI iris.data | 2 | 436.6437333 →436.6 | 0.1cm | 1.5cm |

이는 R 코드를 실행하지 않고 literal/CSV를 읽어 수행한 **2026 감사 계산**이다. iris_value_comparison.json에 무필터·무결측150행, 계산식·시각·해시를 남겼다. 원 실행이 아니다. Primary Df가 정정 전후에 같으므로 판 구별에 실패한다. 같은 논문의 보조 SumSq437.1은 원 UCI iris.data를 후보에서 배제하는 데 유용하지만 R판 하나를 특정하지 못한다. 보조 필드가 유용하다고 primary를 바꾸지 않았다.

## 5. 정보 하나씩 제거한 감도

| 제거 정보 | 적용 사례 | 바뀌는 판단 |
|---|---|---|
| 시간 목적 | RJ02/RJ03 | 1999 package를1998 표본으로, 논문 이후4.2.1을 원 공개 소비판으로 잘못 대입하는 것을 막지 못한다. 최신 재사용과 당시 재현의 목적을 다시 구분해야 한다. |
| 자료 식별자 | RJ02 | 16개 filename을 빼고 취득일만 남기면 U=true에서 미확인으로 돌아간다. 내부 Version은 세 파일에서 대체키가 되지 않는다. |
| 실제 사용 근거 | RJ02 | 당대 target_meta/feature를 제거하면 발행자16파일이 존재해도 저자의 선택이라는 U가 사라진다. 현재 hash를 더해도 R은 복구되지 않는다. |
| 당시 값 | RJ02/RJ03 | 해당 필드 비교를 못 한다. 특히 RJ03 보조 SumSq를 없애면 잘못된 UCI 후보 배제 단서가 사라진다. |
| 현재 정정 | RJ03 | Df2가 같다는 이유로 Petal.Length까지 같다고 재사용하는 오류를 발견하지 못한다. |

현재 판단은 RJ01 **보류**, RJ02 **1998 filename 수준 사용 선언은 유지·실행 및 독립값은 보류**, RJ03 **Df2 후보 양립은 유지·실제 사용판은 보류**다. 정확한 측정값을 원하는 현재 용도에서 UCI의 정정하지 않은 Petal.Length를 쓰는 판단은 **정정 필요**다. Df2라는 좁은 목적에는 값이 다른 변형도 유효할 수 있다. 이것은 기록·추천 정책에 대한 적용 판단이고 실제 사용자 채택의 관측은 아니다.

## 6. 재개 첫 행동과 필요한 실행

원래 R 실행은 이 환경에서 수행하지 않았다. 다음 명령은 후대 후보 재현이며 성공해도 과거 실행의 증거가 되지 않는다.

RJ01: 먼저 당대 research_data.xlsx와13열↔발행자표·판 매핑을 확보한다. 부록17–21행의 slicing을 보존한 후보 재현 명령은 다음과 같다. 원 저자 환경과 첫 행 제외 이유는 별도로 확인해야 한다.

~~~sh
Rscript --vanilla -e 'x<-readxl::read_excel("research_data.xlsx",sheet="data_1992"); p<-prcomp(x[2:nrow(x),2:ncol(x)],scale=TRUE); dput(p$sdev[1]^2); sessionInfo()'
~~~

RJ02: 고정 commit의 data/syntax_feature_yr1998.RDS를 입력으로 다음 명령은 저자 기록 재독을 확인한다. 독립 발행자 검증에는 원 export 선택·lintr/parser 버전, baaugwo/code.db 구성과16 tarball이 필요하다. 현재 미러에서 extract_metadata.R를 돌려 새 표본을 뽑아 대체하지 않는다.

~~~sh
Rscript --vanilla -e 'x<-readRDS("data/syntax_feature_yr1998.RDS"); z<-unlist(lapply(x$function_feat,function(y) if(is.null(y$result)) NULL else y$result$fx_assign)); print(c(true=sum(z),n=length(z),percent=100*sum(z)/length(z))); sessionInfo()'
~~~

RJ03: R4.2.0 또는4.2.1 후보 환경의 명령이다. 원 사용판을 확정할 첫 행동은 당대 저장Rmonad 객체·세션·실행ID·입력해시를 찾는 것이다.

~~~sh
Rscript --vanilla -e 'data(iris); print(summary(aov(Petal.Length~Species,data=iris))); sessionInfo()'
~~~

이미 수행한 것은 공개객체 GET, 압축 멤버 읽기, 해시 계산, 비실행 RDS 파싱, Iris 수치 감사다. receipt와 관측값을 남겼다. 원시 복사본의 후속 정리는 RAW_DISPOSITION.md에 기록한다.

## 7. 검산과 원문 배당

sources.jsonl의 보수적 최소 산입은 **소비 원문3, 발행자 원문3, 당대 저자 artifact1=7저작**이다.16 tarball은 하나의 입력 코퍼스, 여러 R판/UCI변형은 하나의 Iris 자료 계보다. 개별 package component ID는 남겼다. 같은 논문 부록과 Zenodo/GitHub 동일release는 중복 산입하지 않았다. 이 분담만으로 전체24저작·모든 배당 충족을 주장하지 않는다.

메타데이터 노출·실패·의미 판독·바이트 검증은 별도 상태다. XLS extraction 미지원, INS/TEMPO 접근 실패는 값 불일치가 아니다. 최초 웹시각 정밀도 결손은 수용 검토에 남긴다. 자체 재판독과 같은 모델의 parent 검토를 외부 독립 판독이라고 부르지 않는다.

초기 예상인 “C도 사용판 선언을 못 늘릴 수 있다”는 RJ02 고정 명세가 반증했다. 반대로 “정확0%가 복구됐으니 원 실행도 확인됐다”는 승격은 거부했다. Publisher16객체와 author0/386은 확인되지만 둘을 과거 실행의 실제 입력으로 잇는 기록은 아직 없다.
