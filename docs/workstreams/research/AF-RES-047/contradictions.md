# 반례·대안 필드·실패한 가설

관측 단위는 외부 입력 하나와 고정 출력 필드 하나다. 아래에서 **같음**, **다름**, **접근 실패**, **다른 대상**, **미확인**을 나눈다. 자체 출력판·후대 감사 계산·보조 사례는 자연6/보강2의 엄격 성공으로 합치지 않는다. 원시 응답의 해시와 위치는 각 collection receipt와 sources.jsonl에 있다.

## 1. 첫 결론을 바꾼 관측

| ID·처음 가설 | 반대 관측·정확 위치 | 바뀐 판단 | 남은 최소 고리 |
| --- | --- | --- | --- |
| X01 / RJ02: 취득일만 있고 선택판 명세가 없을 수 있다 | [당대 v1.0](https://zenodo.org/records/4026589), 고정 commit07a60457의 target_meta.RDS와 data/syntax_feature_yr1998.RDS: 동일16경로 | U=1, 범위는1998 선택16개 filename/version. 공식 CRAN16/16 객체도 현재 읽었다. | 원 소비 tar 바이트/hash와 원 run ID, export/lintr 처리 연결. 정확0/386은 저자 기록 재독이다. |
| X02 / N-E02: 원 발행 원문에 더는 도달할 수 없다 | [원 NOAA index 보존본](https://web.archive.org/web/20201218094634id_/https://ruc.noaa.gov/raobs/intl/) 및 collection/essd/RUC_FOLLOWUP.md의 실제 final capture | 원 NOAA 저작은 회복했다. 발행자 원문 배당을1 늘린다. | 실제1994–2016 훈련 export는 아직 없다. 캡처된 interface/format을 소비 데이터판으로 승격하지 않는다. |
| X03 / N-E00: 첫 논문의 Group→외부 필드 연결이 없으면 소비 표본에서 제외 | [소비자 §3](https://essd.copernicus.org/articles/14/1/2022/#section3) L260–263: WoRMS로 실제 nomenclature 표준화; Group은 기능 분류 | Q1의 실제 사용과 Q3의 필드 추적성을 분리해 A01로 주 표본에 포함. | Group=Amphipoda가 어느 WoRMS 입력 필드를 거쳤는지 미확인. 원 표본·집계도 보존. |
| X04 / RUN01: 최신 crate가 같은 분석의 모든 단계 기록일 것 | [v1](https://zenodo.org/records/7676924)와 [v1.1](https://zenodo.org/records/8095888)의 prov_preprocess.log/prov_test.log, cpm-edition-comparison.json | predictions.h5와 test.log는 byte 동일하지만 preprocess ID/시각은 다르다. 최신 crate의 나중 preprocess를 원 test와 합치지 않는다. | 각 action의 input table fingerprint를 같은 실행의 출력과 다시 연결해야 한다. |

X02의 위 링크는 요청 URL일 수 있다. 실제 응답 final URL/캡처 날짜를 sources S-E059–070과 RUC_FOLLOWUP에서 우선한다. 역사적 날짜를 임의로 고정했다고 읽지 않는다.

## 2. 값·판·행의 반례

| ID·종류 | 직접 확인한 값/객체 | 왜 판정을 제한하는가 | 원문 주소·위치 |
| --- | --- | --- | --- |
| X05 / RJ03: 여러 판 같은 바이트·값 | R4.2.0과4.2.1의 iris.R 3018bytes, SHA25677af4424…691dc5c; Df=2 | 대상 멤버가 같아도 어느 release가 실제 사용됐는지 결정하지 못한다.4.2.1은 논문 뒤 공개됐다. 이전 동일내용 파일의 사용을 부정하는 증거는 아니다. | [R4.2.0](https://cran.r-project.org/src/base/R-4/R-4.2.0.tar.gz), [R4.2.1](https://cran.r-project.org/src/base/R-4/R-4.2.1.tar.gz), src/library/datasets/data/iris.R; rjournal/iris_value_comparison.json |
| X06 / RJ03: 값이 달라도 좁은 목적에는 유효 | UCI iris.data와bezdekIris.data의35·38행이 다르고 보조SumSq436.6/437.1; 주Df는모두2 | Df 예제 목적에는 차이가 영향을 안 주지만 정확 Petal.Length/ANOVA전체 재현에는 영향을 준다. 보조값으로 primary를 교체하지 않았다. | [UCI Iris](https://archive.ics.uci.edu/dataset/53/iris), Additional Information; [공식 ZIP](https://archive.ics.uci.edu/static/public/53/iris.zip)의35·38행 |
| X07 / N-E00 AUX: 같은 값·같은 셀·다른 행 대상 | IOW v1/v2 Factors Baltic Sea!B148=1 모두, A148은Hippeutis complanatus→Hirudinea. North Sea!B21=1의A21도다름 | 값과 셀주소를 키로 삼으면 다른 종을 같은 대상으로 오인한다. taxon/record ID를 보존해야 한다. | [IOW release2](https://doi.iow.de/10.12754/data-2021-0002-01), 이전판 링크; essd/iow-edition-comparison.json keyed_rows/selected_cells |
| X08 / N-E00 AUX: 합계 같음·지역 결과 달라짐 | raw record7315/13306의수치는같지만Region Baltic→North, Station OB20/40→DB20/40; 합친시트불변 | 같은 합계는 판 구별에 부족하다. 당시재현과현재지역별 사용은 판단이 달라진다. 이는 WoRMS 입력판 확인이 아니다. | 같은 IOW 두판 Raw_Single_Measurments_Factors 및지역별/합계시트; compare_iow.py |
| X09 / AUX-EARTH-01: 같은 행 다른 값·다른 필드 같은 값 | depth0.045m Age2.1→2.574kaBP,230Th310.292pg/g동일; depth3.105m Age20.4→20.391(1자리반올림20.4) | 단위/행키/정밀도/목적이 없으면 올바른 개정도 불일치로, 잘못된 후보도 일치로 분류한다. | [PANGAEA889928](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=html), [936557](https://doi.pangaea.de/10.1594/PANGAEA.936557?format=html), Data 해당depth행; 새판Comment age model revised |
| X10 / RJ02: 파일명 판과 내부 Version 다름 | acepack_1.1 내부1.0-4; class/nnet filename5.2pl005-2 내부5.2pl005-1 | 내부Version만으로 publisher와author를조인하면지목된파일을놓친다. 차이 원인/정정사유는미확인. | [acepack파일](https://cran.r-project.org/src/contrib/Archive/acepack/acepack_1.1.tar.gz), [class파일](https://cran.r-project.org/src/contrib/Old/0.61/class_5.2pl005-2.tar.gz), DESCRIPTION; rjournal/cran_1998_publisher_receipts.json |
| X11 / RUN02: 압축 bytes 다름·일부 decoded 값 같음 | publisher gzip413005346bytes, archived487611787bytes; 첫20 FASTQ records SHA동일 | 전 파일 동등성이나 생물학적 정정을 판정할 수 없다. 재압축과 양립한다. 서로 다른flowcell의동명파일도 fullpath로구별해야한다. | [NIST R1](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/140407_D00360_0017_BH947YADXX/Project_RM8398/Sample_U5c/U5c_CCGTCC_L001_R1_001.fastq.gz), [crate](https://zenodo.org/records/12622362), wetlab-fastq-prefix-comparison.json |
| X12 / RUN01: 필드/목적이 다른 값 | publisher XML polygon vertex와predictions coord_x는다른행/변환. 원소비설명prostate와CAMELYON breast lymph-node영역도다름 | 숫자가닮아도동일필드가아니다. publisher원문으로자료목적설명을정정하되 임상효능 추정은하지않는다. | [CAMELYON원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC6007545/) Data description/validation, [README](https://camelyon-dataset.s3.us-west-2.amazonaws.com/CAMELYON16/README.md) Notes, CPM logical non_index_axes |

## 3. 주소와 bytes에 관한 성공·실패·미충족

[PANGAEA TSV](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=textfile)와 [UTF-8 명시 TSV](https://doi.pangaea.de/10.1594/PANGAEA.889928?format=textfile&charset=UTF-8)는 서로 다른 정확 URL이지만 실제 GET의9394bytes/SHA256이 같다. `collection/domain/url-encoding-alias-check.json`에 각 시각·최종URL을 남겼다. 이는 URL이 다른 동일 파일의 실측 사례다.

반대로 `doi.org/...?...format=textfile` 요청은 query가 없는 HTML landing으로 이동했다. `url-alias-check.json`에 실패한 같은bytes가설을 보존했다. 응답 표현이 달랐다는 관측이며 데이터 수치 불일치가 아니다.

**고정 URL이 같은 bytes를 반환하지만 특정 실제 공개 실행이 그 파일을 읽지 않았다는 완전한 음성 사례는 확보하지 못했다.** R4.2.1의 시간적 불가능성은 그 공개release의 사용을 제한할 뿐 이전 동일내용 사용을 부정하지 않는다. CPM의 나중 preprocess/같은prediction도 입력 미사용의 직접증거는 아니다. 이 요청 조건은 수용 원장에 미충족으로 남긴다. 최소 후속은 원래 두 실행 중 하나의 input-read manifest 또는 파일 접근 영수증과 안정된 publisher bytes를 함께 확보하는 것이다.

## 4. 같은 입력의 다음판 대조 범위

| 사례 | 실제로 대조한 쌍/선정값 | 쌍의 성격 | 남은 빈자리·다음 행동 |
| --- | --- | --- | --- |
| RJ01 | 1992/2018의보조PC1proportion0.44반복 | 다른 기준기간, 정정판쌍 아님 | 같은1992 13지표의원 workbook·발행표·정정판 확보 |
| RJ02 | 1998선택16파일 현재읽기; acepack1.1→1.2-1 목록 | 전체corpus의다음판 아님; 후속파일동일필드독립계산미실시 | 원 parser/export환경과16파일 처리명세를먼저확보 |
| RJ03 | R4.2.0→4.2.1 iris.R 동일bytes/Df2 | 실제발행연속판의**후보**입력멤버쌍; 진본사용판미확인 | 원R/session/run기록으로사용판좁히기 |
| N-E00 | IOW release1→2 첫Group동일·지역/행변경 | 소비자가생산한출력쌍, WoRMS외부입력아님 |2021 WoRMS snapshot/query receipt확보 |
| N-E01 | BCO v3.0.0 존재 | 원소비판/다음판파일쌍미확인 | Fig5pairedrows와level/filemanifest확보 |
| N-E02 | RUC보존interface/format·자체출력156→235공지 | 원훈련export쌍미확인;자체출력정정값도미대조 | 원trainingexport와두19Jan출력을별개로확보 |
| RUN01 | consumercrate v1→v1.1: 같은predictions,다른preprocess | 소비기록판쌍;원CAMELYON다음판쌍아님 | 원WSI/XML→H5변환영수증과동일test 입력hash연결 |
| RUN02 | currentpublishergzip vsarchivedgzip,같은20records | 서로다른representation,발행자연속판으로확정못함 | full decoded digest와입수/재압축기록확보 |

## 5. 메타데이터만 바뀌었다는 주장도 범위를 제한한다

[PANGAEA889928 Change history](https://doi.pangaea.de/10.1594/PANGAEA.889928)는2021-09-24 author list 정정과2021-09-30 새판 게시를 분리한다. 따라서 **발행자가 기록한 메타데이터 정정 사례**는 있다. 그러나 저자목록 정정 직전·직후 payload를 모두 가져오지 못했으므로 데이터bytes까지 불변이었다는 실측 조건은 미확인이다. CPM HDF5에서 읽은33개table/index-array raw hash가같아도 모든속성/구조를비교한것은아니며, 이를순수metadata변경이라고확정하지않는다.

## 6. 적용 결론

추천 이력은 식별자 하나나 현재 해시 하나로 '실제 사용'을 표시하지 않아야 한다. 발행자의 자료/판/파일, 소비자의 사용 선언, 같은 실행의 입력 연결, 같은 행·필드·단위·변환의 값 대조를 각각 유지한다. `sensitivity.csv`는8사례×5제거를 기록한다. 그것은 보이는 근거를 제거했을 때 허용 문장을 좁히는 감사이며 실제 이용자 채택이나 무작위 평가가 아니다. 원래 미확인인 필드를 제거했으면 새 정보 손실0으로 남겼다.
