# AF-RES-047#1 — 공개 분석의 사용판·실행 입력·정정값 부분 인계

**결과는 검토 가능한 상태로 저장했으며, 전체 수용은 부분 충족이다.** 소비자 우선6건과 실행 보강2건, A/B/C24구성, 정보 제거40행을 보존했다. 직접 읽은 고유 저작은31개, 필수 역할에 배당한 저작은27개다. 마지막 전체 파일 대조가 최초 결론을 바꿨다. RUN02에서는 원 실행이 지목한 R1 입력과 발행자 체크섬을 연결했지만, 선정 출력 CHROM의 독립 값 검증은 남았다. 불확실한 표본 선정·정확값·음성례를 성공으로 바꾸지 않았다.

## 1. 식별

- 작업 ID / 시도: **AF-RES-047 / 1**. 배정 종류: `web-pro`.
- 실제 확인 가능한 모델 표시: **GPT-6 Astra Pro**라는 세션 지시. UI 모델 선택기는 독립 확인하지 않았다. 실행 위치는 클라우드 Linux 셸·GitHub 연결·웹 검색/열람이다. 사용자 PC를 사용하지 않았다.
- 공개 작업자 식별: 저장소·브랜치·작업 ID로 조회한다. 별도 공개 작업 URL/PR은 없다. 같은 모델의 별도 문맥 분담·검토이며 외부 독립 판독이 아니다.
- 저장소 / 브랜치: `laadkke-arch/agentflow-open` / `work/research-af-res-047`.
- 계획 기준: `1f722bfb7360ff9c8d221284d7b1b6484c6fa692`.
- 실제 시작 통합 SHA: **`4492dd8e9978087b32897ec2685110d24f510473`**. `manifest.json`의 시작값을 후대 통합 SHA로 바꾸지 않았다.
- 의존 결과: AF-RES-043 **`3e0b1433e95cf8fdd5a930db97afa3ae8e3ab1f3`**의 [HANDOFF](https://github.com/laadkke-arch/agentflow-open/blob/3e0b1433e95cf8fdd5a930db97afa3ae8e3ab1f3/docs/workstreams/research/AF-RES-043/HANDOFF.md)를 읽었다. 같은 차수 결과를 기다린 단계는 없다.
- **고정 결과 SHA: `235724aa3189712d65c710d2192dd9c703c1f57e`.** [RESULT](https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/RESULT.md)와 [수용 원장](https://github.com/laadkke-arch/agentflow-open/blob/235724aa3189712d65c710d2192dd9c703c1f57e/docs/workstreams/research/AF-RES-047/evidence/acceptance-evidence.json)을 이 SHA로 다시 열었다.
- 마지막 확인한 원격 저장 SHA / 이 인계의 부모: **`bbf9fad206acfcb45be4e65a5996c59a1eb8371c`**. 고정 결과 재독과 마지막 세션 검사 영수증을 저장한 커밋이다. 이 문서는 그 뒤 `HANDOFF.md` 하나만 담는 마지막 커밋으로 게시한다. 자기 자신의 아직 생성되지 않은 SHA를 본문에 넣지 않으며, 실제 최종 SHA는 브랜치 ref와 마지막 커밋 diff로 확인한다.
- 마지막 세션 검사: **2026-11-22T23:28:45.408070Z–23:28:54.308078Z**, exit0, `passed`, `outside_paths=[]`, `unmerged_paths=[]`, `errors=[]`.
- 최종 인계 작성 기준 확인 시각: **2026-11-22T23:30:25Z**. 상태: **REVIEW_READY — 부분 인계, 전체 수용 미충족**.

## 2. 사용자 요구와 작업 범위

목표는 “그 판에 그 값이 있었다”와 “그 분석의 그 실행이 그 판을 읽었고 그 값을 산출했다”를 구별하는 공개 근거를 찾는 것이다. [고정 제품 브리프](https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/product/RESEARCH_BRIEF.md), [연구 운영 규칙](https://github.com/laadkke-arch/agentflow-open/blob/1f722bfb7360ff9c8d221284d7b1b6484c6fa692/docs/RESEARCH_WORKFLOW.md), 시작 통합판의 AGENTS/STATE/DOT_AUTOMATION 및 dot-control의 배정을 읽었다. 원문 열람 영수증은 `evidence/input-receipt.json`이다.

편집은 **`docs/workstreams/research/AF-RES-047/`만** 수행했다. `dot-control.json`은 변경하지 않았다. 통합 브랜치·다른 연구 경로·운영 서비스·main은 수정하지 않았다. 039의 네트워크 비용,043의32카드·UCLA 옛 페이지·DOI 성공률을 반복 조사하지 않았다. 제안은 추천 이력의 증거 구분에 관한 설계 입력이며 제품 DB나 최종 구현 결정을 확정하지 않는다.

## 3. 실제 변경과 읽을 순서

| 파일/묶음 | 변경 사항과 이유 | 확인 위치 |
| --- | --- | --- |
| `manifest.json`, `SCOPE.md`, `frame.csv` | 실제 시작 환경·계약·의존 SHA, 표본/필드 규칙, 첫30노출×3 | 최초 봉인5c75f357 및 노출 봉인6b74510d; 원 선택과 변경 원장은 별도 보존 |
| `consumers.csv`, `editions.csv`, `sources.jsonl` | 소비 주장8건, 발행판/파일 기록30행, 접근/열람311행 | 고유 저작31 / 필수 역할27; `source-count-summary.json`으로 중복·배당 재계산 |
| `runs.csv`, `readings.csv`, `sensitivity.csv` | 실행/결측12행,8×3근거 구성,8×5정보 제거 | 원 실행·local 파일·외부 발행자 객체·선정값을 별도 축으로 기록 |
| `RESULT.md`, `SELF_CHECK.md`, `evidence/acceptance-evidence.json` | 필수 표·Q1–Q7·반증·수용/미수용 조건 | 고정 결과235724aa. RESULT의 **첫 표는 §표1(7행부터), 둘째 표는 §표2(22행부터)**. 실제 데이터 행은8/24개이며 마지막 표는3행 |
| `collection/runs/wetlab-full-*`, 실행 스크립트 스냅샷 | 전체 R1 파일 두 개의 대조로 외부 입력 연결 R0→1을 정정 | 같은 archive action, 발행자 MD5388행, 전체 gzip/decoded digest와 실제 실행 영수증 |
| `amendments.md`, `contradictions.md`, `evidence/pre-full-fastq/` | 선정 해석·구성 누출·필드 순서 정정, 이전 결론과 반례 보존 | A01–A10. 원 ESSD 선정과 RUN02 이전 R0 집계를 현재 결론으로 덮어 숨기지 않음 |
| `evidence/fixed-result-reread.json`, `session-check.json`, `finalization-evidence.json` | 결과 커밋의 원격 재열람과 최종 검사 | 검증 커밋bbf9fad2. 결과 수용 원장의 시간상 pending과 실제 후속 완료를 구별 |

### 중간 원격 커밋

| 묶음 | 원격 SHA | 주요 파일 |
| --- | --- | --- |
| 1 / 사전 규칙 | `5c75f3571ab8473f3fba72d92a70bd201c0cf189` | manifest/SCOPE/예정 frame/시작 영수증 |
| 1b / 노출·필드 | `6b74510d9b660fc1a3fe76c9f7845d727b930297` | collection의 frame/selection freeze |
| 1c / 선정 정정 | `26a6dcb72fac3642384e8c36bb6e385120c0d982` | A01과 원 선택 보존 |
| 2 / 소비·발행 | `cd20785b782cb588cf231c4dc8473bab846b5714` | consumers/editions/sources와 각 collection 원장 |
| 3 / 실행·반례 | `0e9735ec2e488139b83c8aa40c946c5c097a5975` | runs/readings/sensitivity/contradictions와 수집 증거 |
| 4 / 고정 결과 | `235724aa3189712d65c710d2192dd9c703c1f57e` | RESULT/SELF_CHECK/수용 원장, 전체 R1 검사·A10·최종 검토 |
| 검증 영수증 | `bbf9fad206acfcb45be4e65a5996c59a1eb8371c` | commits.jsonl/fixed-result-reread/session-check/finalization-evidence |

각 게시 때 로컬 Git tree와 GitHub tree의 일치를 확인했다. 셸 push 인증은 사용할 수 없어 승인된 저장소 연결의 expected-SHA 조건부 ref 갱신을 사용했다. 파일 내용과 최종 tree를 비교한 기록은 `evidence/commits.jsonl`이다. CSV의 작업 사본 CRLF는 저장소 text 규칙으로 Git에서 LF가 되며, 원문 HTTP 바이트 hash는 이 정규화와 별도다. 검증 커밋 자체의 파일 목록은 위 표와 그 커밋 diff에 있다.

## 4. 실제 검증 결과와 미실시 범위

시작 명령은 아래 그대로 수행했고,2026-11-22T22:02:16Z–22:02:26Z에 완료했다. 실제 argv·stdout·시각은 `evidence/session-start.json`에 있다.

```sh
python -B -m workbench.session start af-res-047 --allow docs/workstreams/research/AF-RES-047/ --output docs/workstreams/research/AF-RES-047/manifest.json --dependency work/research-af-res-043=3e0b1433e95cf8fdd5a930db97afa3ae8e3ab1f3 --fetch
```

다음 원장 생성·검산 명령을 실행했다. 최종 구조검사는 **61/61 통과**다. 판정이 맞다는 일반 보증이 아니라 필수 표8/24/끝3행, CSV40/90행, 원문 중복/배당, 축별 집계, 구성의 정보 범위, 결측 분모, 소유 경로의 검산이다. 검사한 내용은235724aa에 고정됐으며 RESULT SHA256은 `07ce5a039ae9a257ac57aa38900af6c1b26527ca4fcff932b077f1d94da6e7fb`다.

```sh
python -B docs/workstreams/research/AF-RES-047/scripts/consolidate.py
python -B docs/workstreams/research/AF-RES-047/scripts/build_sensitivity.py
python -B docs/workstreams/research/AF-RES-047/scripts/build_report.py
python -B docs/workstreams/research/AF-RES-047/scripts/validate.py
python -B docs/workstreams/research/AF-RES-047/scripts/build_acceptance.py
```

고정 SHA의 RESULT와 수용 원장을 GitHub에서 직접 재열람했다. 전체 문자열·Git blob·내용 SHA, 표 행수와 판정·미충족 항목을 확인했다. 수용 원장 SHA256은 `e0b6207ff322d8e245f910229fbb622f00589246d7680e7d30e67a0458508712`다. 수용 원장의 `fixed_result_remote_reread=pending`은 결과 커밋을 만들 당시의 상태이며, bbf9fad2의 재열람 영수증에서 충족으로 해소된다. 마지막 HANDOFF 커밋은 자기 SHA를 미리 만들 수 없으므로 최종 ref/diff로 확인하는 항목이다.

마지막에 다음 검사를 **고정 결과 SHA235724aa에서 실제 실행**했다. exit0/`passed`이며 범위 밖 변경·충돌·오류는 모두 빈 목록이다. 그때 통합 브랜치는 `7658ae6c0f6eca65ea9991bcf167d131d86460e6`까지 진행됐지만 입력 계약은 유지됐고 시작 기준4492dd8은 변경하지 않았다.

```sh
python -B -m workbench.session check docs/workstreams/research/AF-RES-047/manifest.json --fetch
```

RUN02 전체 입력 검사는 다음 명령을 **실행 완료**했다. 시작2026-11-22T23:00:16.442063Z, 종료23:09:38.308193Z, exit0이다. archive Range63개와 발행자 전체 GET1개로 압축파일 두 개를 끝까지 스트리밍하고 해제된 전체 내용을 hash했다. 실행 당시 스크립트 SHA256은 `a94b06e7c85b4c3aa69e010edde97f7a3f7ce88e5026d18b415c4d5c8ba6bb3a`이며 `verify_full_fastq-executed-snapshot.py`에 원본을 남겼다.

```sh
python -B docs/workstreams/research/AF-RES-047/collection/runs/verify_full_fastq.py --perform
```

입력은 [Zenodo full archive](https://zenodo.org/api/records/12622362/files/wetlab2variations_full.zip/content)의 `inputs/U5c_CCGTCC_L001_R1_001.fastq.gz`와 [발행자 R1](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz)이다. 전체 대형 payload를 저장하지 않았으며 전송·hash·입력URL·실행 출력은 영수증으로 남겼다.

원 과학 분석의 R 환경, ANN 훈련, 병리 분류, variant-calling 전체를 재실행하지 않았다. 현재 확인한 것은 공개 객체와 저장된 원 실행 기록의 대조다. 자체 재판독, 동일 모델 별도 문맥 검토, 발행자/소비자 증거의 독립 계보를 서로 구별했다. A10의 마지막 변경 검토는 R Journal 분담26/26, 실행 분담12/12였으며 **외부 독립 판독이나 실제 사용자 채택 시험은 아니다**.

## 5. 판단과 근거

| 층 | 사례수 | 구별 가능한 후보 발행판 P | 외부 특정판/파일 사용 선언 U | local 실행 연결 | 외부 발행자 객체까지 실행 연결 R | 진본 사용판의 선정 필드 독립 검증 V |
| --- | --- | --- | --- | --- | --- | --- |
| 소비자 우선 자연층 | 6 | 4/6 | 1/6 | 0/6 | 0/6 | 0/6 |
| 실행 기록 보강층 | 2 | 2/2 | 1/2 | 2/2 | 1/2 | 0/2 |

자연층과 보강층을 합친 보존율로 일반화하지 않는다. R 확인 사례 중 V는 자연층에서 분모0으로 **해당 없음**, 보강층에서 **0/1**이다. C의 추가 답 재독4/8과 RJ03 후보값 대조1/8도 V에 합치지 않는다. 필수 역할 배당은 소비/원실행8, 발행자8, 저자 당대 기록/실제 provenance7, 공식통계2, 지구과학2이며 별도 보조4는 배당 부족을 채우는 데 쓰지 않았다.

가장 강한 새 관측은 RUN02다. 같은 Zenodo archive action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`가 지목한 R1의 전체 gzip487,611,787bytes는 crate SHA256과 일치하고, MD5 `52f3ed344d88278c703faa1280818ce1`은 [발행자 HG001-part2.md5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) **388행의 정확한 전체 경로**와 일치했다. 현재 gzip413,005,346bytes는 다른 MD5지만 두 파일의 해제 내용1,409,966,879bytes/SHA256은 같다. 이로써 선택 R1의 **기록상 외부 입력 연결**을 확인했다. 다른 GitHub UUID, 나머지 입력, 원 시스템의 모든 I/O로 확대하지 않는다. CHROM1은 파생 출력 재독이어서 V는0이다.

다른 반증도 남겼다. RJ02의 당대16파일 명세는 “부록이 사용판을 더 좁히지 못한다”는 예상을 반박했다. Iris는 값/bytes가 같아도 사용 release를 특정할 수 없고, 측정값이 달라도 Df 예제 목적에는 유효할 수 있다. IOW는 같은 셀·숫자가 다른 종을 가리키며 전체 합계가 같아도 지역별 결과가 바뀐다. ALFRED의 발표일/빈티지와 PANGAEA의 메타데이터/나이모형 정정은 과거 재현과 현재 재사용의 목적을 나눠야 함을 보여 줬다. 정확 주소·위치는 RESULT Q3–Q7 및 contradictions X01–X13에 있다.

전체 수용을 막는 것은 원장에 남긴 다음 여섯 조건이다: 완전 사전 고정된 최초 소비 표본, 완전히 확정된 최초 실행 보강 표본, RJ01/N-E01의 정확 주 값, 일부 최초 열람 UTC의 정확초, 순수 메타데이터 정정 직전/직후 payload 불변, 고정 URL/같은 bytes를 특정 실제 실행이 사용하지 않았다는 직접 음성례. 역사적 사전봉인·최초시각 결손은 지금 문구를 바꿔 복구할 수 없다. 앞선 적격 사례의 공개 입력이나 원 당대 기록을 확보해야 바뀌는 판단과 분리한다.

추천 이력에는 시간 목적, 자료/판/파일 식별자, 실제 사용 근거, 당시 값·변환, 현재 정정의 다섯 항목을 별도로 두는 방안을 제안한다. 정보 제거40행에서 상태표시17개가 바뀌었고, 원래 결측인6행은 새 손실0이었다. RUN02의 식별자 또는 사용 근거를 빼면 R1→0이다. 이 결과는 근거를 제거한 규칙적 감사이며 사용자의 실제 오류율이나 설계 수정 노동 절감 효과를 관측한 것은 아니다.

## 6. 재개 첫 행동과 필요한 입력·명령

**재개 첫 행동:** 고정 결과235724aa와 이 인계를 읽고, RJ02의 `collection/rjournal/rstyle_1998_input_manifest.csv`에 있는16경로를 기준으로 [당대 rstyle v1.0](https://zenodo.org/records/4026589) / [고정 commit07a60457](https://github.com/chainsawriot/rstyle/tree/07a60457c88dbb20858441047f248d61ce2955c7)에서 **원 입력 fingerprint·run 영수증과 export/lintr 환경**을 찾는다. 새 CRAN 미러를 다시 내려받는 것만으로 원 소비판을 확인했다고 하지 않는다. 기대 결과는 자연층 한 사례의 사용 선언을 실행·발행자 객체까지 연결할 수 있는지에 대한 판정이다. 새 작업 ID는 통합 담당이 배정하며 이 인계가 자동 후속 실행을 만든 것은 아니다.

다음 세 R 명령은 이번에 원 환경에서 실행하지 않았다. 정확 입력을 먼저 확보하고 저자 release 추출 경로에서 실행할 후보 확인이다. 성공해도 원 실행 증거가 새로 생기는 것은 아니다.

| 사례 | 먼저 필요한 입력/환경 | 실행의 의미와 한계 |
| --- | --- | --- |
| RJ01 | 당대 `research_data.xlsx`, `data_1992`,13열↔INS 발행표 매핑, 원 결측/첫행 제외 규칙 및 R 환경 | 원 PCA 후보 재현. 부록의 slicing을 보존하며 반올림2.40으로 정확 분산을 만들지 않음 |
| RJ02 | 고정 release의 `data/syntax_feature_yr1998.RDS`; 독립 재계산에는16 tar·원 export/lintr/parser·code.db 구성과 입력 fingerprint 추가 | 아래 명령은 저자 기록0/386 재독만 확인. 발행자 독립 재계산 명령은 원 환경/선택 절차를 확인한 뒤 고정 |
| RJ03 | R4.2.0 또는4.2.1 후보 환경; 진본 판정에는 당대 Rmonad 객체/session/run/input hash 추가 | ANOVA 후보 값 확인. 어느 R release를 원 논문이 사용했는지는 별도 |

```sh
Rscript --vanilla -e 'x<-readxl::read_excel("research_data.xlsx",sheet="data_1992"); p<-prcomp(x[2:nrow(x),2:ncol(x)],scale=TRUE); dput(p$sdev[1]^2); sessionInfo()'
Rscript --vanilla -e 'x<-readRDS("data/syntax_feature_yr1998.RDS"); z<-unlist(lapply(x$function_feat,function(y) if(is.null(y$result)) NULL else y$result$fx_assign)); print(c(true=sum(z),n=length(z),percent=100*sum(z)/length(z))); sessionInfo()'
Rscript --vanilla -e 'data(iris); print(summary(aov(Petal.Length~Species,data=iris))); sessionInfo()'
```

ESSD와 실행층의 남은 일은 다음 자료가 먼저다. N-E00은2021 WoRMS snapshot/query와 Taxa→Group 변환 기록, N-E01은Fig5 paired-point table과 BCO level/file manifest, N-E02는1994–2016 RUC export·station00078954·split/seed/weights와2020-01-19 radar 출력이다. N-E02의 [고정 V1 코드](https://zenodo.org/records/5714474/files/calc_mean_max_min_LWP_paper.py?download=1)는 로컬 `latest/with_DOI/daily_intake`에 의존한다. 이 원 입력을 복원한 뒤의 실행 진입점은 `python calc_mean_max_min_LWP_paper.py`이며, 현재 경로만 새 자료에 맞춰 실행한 결과를 원 실행으로 세지 않는다.

RUN01은 publisher WSI/XML→H5 변환 영수증과 원 test의 table fingerprint가 필요하다. RUN02 전체 R1 대조는 완료됐으므로 반복 전송이 첫 행동이 아니다. 남은 V를 시험하려면 원 CWL, 나머지 입력·참조판, 당대 컨테이너와 원 실행 인자를 확정하고 같은 CHROM 행을 독립 검증해야 한다. 원 전체 재실행 명령을 현재 근거로 확정하지 못했으므로 임의 명령을 만들지 않았다. 당대 명령 탐색의 첫 입력은 저장된 `wetlab-output-meta__outputs___1693335046__stderr.txt`85/105–114행과 `wetlab-small-ro-crate-metadata.json`이다. 재압축 시각·행위자·공식 사유는 별도의 역사 기록이 필요하다.

선정의 미확인은 앞순위 ESSD5쪽의 입력 생산자·공개성, LivePublication `input_data.txt`의 외부 원출처·최초 공개일을 확인하는 것으로 재개한다. 음성례에는 특정 원 실행의 배타적인 input-read manifest와 같은 publisher bytes가 필요하다. 당사자 연락·추가 계정 접속·사용자 채택 실험은 수행하지 않았다. 공개 근거의 후속 읽기는 가능하지만 없는 역사 기록을 현재 실행으로 대신할 수 없다.

색인 제안: **AF-RES-047 | 발행판·사용 선언·원 실행·보고값을 분리한6+2사례 감사; RUN02 입력 연결1건, 선정값 독립검증0건·부분 인계 | docs/workstreams/research/AF-RES-047/RESULT.md | AF-RES-043@3e0b1433 의존.**

| 불일치 또는 약점 | 영향받는 결론 | 근거 주소·위치 | 다음 최소 조사 | 판정이 바뀌는 조건 |
| --- | --- | --- | --- | --- |
| 선정 해석의 사후 정정·앞선 적격 미확인·일부 최초시각 정밀도 결손 | 완전 사전 고정된 최초6+2 및 모집단 보존율 일반화 | [ESSD14-1 §3](https://essd.copernicus.org/articles/14/1/2022/#section3), [실행 목록](https://www.researchobject.org/workflow-run-crate/), amendments A01/A04/A06/A08 | ESSD5쪽 입력 생산자와 LivePublication 공개 입력/발행일 확인; 역사적 봉인 결손은 보존 | 앞선 후보 적격·날짜가 독립 자료로 확정되면 표본 확실성 수정. 사전성/정확초 주장은 별도 전향 반복 없이는 승격하지 않음 |
| RUN02 외부 입력 R1은 확인했으나 선정 필드 독립 V0, 정확 주 값2건 결측 | 그 분석이 그 판의 그 값을 실제 사용했다는 엄격 양성 및 정정값 대조 | [RJ02 archive](https://zenodo.org/records/4026589) target_meta/feature, [Wetlab](https://zenodo.org/records/12622362) action/input, [NIST MD5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5)388행 | 당대 입력 명세/실행과 같은 행·변환·필드의 독립 대조, 원 그림 숫자 확보 | publisher 객체와 당대 run이 선정 필드 값까지 만나면 해당 V만 승격. 다른 UUID·필드·후대 실행은 대체 불가 |
| 고정 URL·동일 bytes의 실제 미사용 음성례 및 metadata-only 전후 payload 미확보 | 주소/해시와 사용의 구별에 대한 요청된 실증 범위 | [PANGAEA889928 Change history](https://doi.pangaea.de/10.1594/PANGAEA.889928), [CPM v1.1](https://zenodo.org/records/8095888) 원 로그, contradictions §3/5 | 원 실행의 배타적 read 영수증과 동일 파일, 메타데이터 정정 직전/직후 파일 확보 | 실제 미사용과 파일 동일성 또는 정정 전후 payload 불변을 각각 직접 확인하면 해당 미충족 조건만 해소 |
