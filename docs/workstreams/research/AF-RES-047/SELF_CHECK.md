# AF-RES-047 자체 검산과 반증 점검

## 검토의 성격과 결론

이 검토는 조사자의 자체 재판독 및 **동일 모델의 별도 문맥 검토**다. 외부 독립 판독자, 눈가림 평가, 실제 사용자 채택 시험은 수행하지 않았다. 분담자는 각각 자신이 조사한 사례를 다시 검토했고, R Journal 분담자는 통합 원장·다른 층의 위험 행도 읽었다. 관측 원문이 서로 다른 계보인지와 검토자가 외부 독립적인지는 별개의 축이다.

수량 조건은 자연6+보강2, A/B/C24행, 정보 제거40행, 첫30노출×3이다. 최소수는 보수적으로31저작이며, 필수 역할만27저작이다. 배당은 소비/원실행8, 발행자8, 당대 기록/실제 provenance7, 공식통계2, 지구과학2다. 중복·실패·재방문을 더하지 않았다. 원장 행수는 추가 재독/실패까지 포함하므로 최종 sources.jsonl과 source-count-summary.json에서 다시 센다.

**전체 수용은 부분 충족이다.** 발행판·선언·실행·값을 분리하는 관측과 반례는 확보했지만, 초기 선정 해석 정정과 앞선 적격 미확인, 고정 URL/동일 bytes의 실제 미사용 음성례, 진본 사용판의 동일 필드 대조는 남았다. 정확한 주 값은 RJ01과 N-E01에서 결측이다. 이를 다른 필드나 여러 판의 같은 숫자로 채우지 않았다.

## Q1 — 판 보존 성과 이전에 소비자를 선택했는가?

답: 공개 목차의 날짜·식별자 순서와 실제 외부 입력 이용을 기준으로 정했다. R Journal3건은004/006/007, 현재 ESSD3건은1/19/33쪽이다. frame.csv의90행은 관측 metadata 노출이며90편 모두의 전문을 읽었다는 뜻이 아니다. 최초 사전90슬롯은5c75f357에 남고, 실제 노출은 후속 frame으로 분리했다.

직접 재독 근거는 [RJ006 §2.1 L40–44](https://journal.r-project.org/articles/RJ-2022-006/)와 [ESSD14-1 §3 L260–263](https://essd.copernicus.org/articles/14/1/2022/#section3)이다. 후자는 실제 WoRMS nomenclature 이용과 기능적 Group을 구별한다. root 최종 재독은 ROOT-FINAL-01/02/09/10, 원 선택 freeze와 metadata 날짜는 collection의 frame/selection 파일에 있다.

반대 관측: 처음에는 Group의 외부 필드 연결이 불명확하다는 이유로 ESSD 첫 소비자를 건너뛰었다. 이는 후속 추적성 기준을 선정 조건으로 끌어오는 편향이다. A01로 고쳤으며 처음의 N-E01/02/03도 보존했다. 두 표본의 P/U/R/V 집계는 같지만 사례가 같다는 주장은 하지 않는다. 변경 결정은 WoRMS 열람 전, 원격 변경 커밋은 열람 뒤였다. 완전 사전등록 준수는 미충족이다. RJ006/007/008의 우연한 선행 본문 노출과 RUN01 물리 저장순/논리 열순의 정정도 원장에 있다.

판정을 뒤집을 최소 자료: ESSD5쪽의 현장 기상자료가 제3자 공개 입력이었음을 보여 주는 생산 주체/입수 문서가 나오면 첫3 확정을 다시 해야 한다. 현재 빠진 출력 필드 연결이 확인되는 것만으로 선정 기준을 다시 바꾸지는 않는다.

## Q2 — 실행 보강이 정의·fixture·자기 자료 게시에 그치지 않는가?

답: 원 목록 및 연결 저장소에서 실제 실행 ID→입력 객체가 있는 사례를 먼저 찾았다. RUN01은 CAMELYON 영상에 적용한 CPM 분석, RUN02는 NIST NA12878 공개 FASTQ에 적용한 variant-calling 실행이다. 실제 외부 자료를 사용한 방법 시연은 포함하고 synthetic/정의-only/비공개 입력은 구별했다. 이2건은 자연6 분모에 합치지 않았다.

재독 근거는 [PLOS 실제 사례 §3.5 L498–505](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210#sec008)와 §4.2 L659–701,788–790이다. ROOT-FINAL-15/16에서 staging과 retrospective 기록, 복수 실행, local HDF5와 action ID, 입력 전단계 provenance 미포함을 직접 읽었다. archive member 원관측은 collection/runs/runs.csv의6개 실행 기록과 같은 archive의 graph/log/output receipt다. 원서버 재독에서 Zenodo 두 landing의 웹 도구 접근 실패도 ROOT-FINAL-03/04로 남겼고 과거 성공을 지우거나 현재 성공으로 바꾸지 않았다.

반대 관측: LivePublication는 실제 실행이지만 input_data.txt의 제3자 공개 생산자·자료명을 확인하지 못했다. 더 앞선 적격 후보일 수 있어 “최초2가 완전히 확정됐다”는 주장은 보류한다. embedded datePublished는 export 날짜일 수 있다. 같은 날 timestamp 순을 날짜+식별자 순으로 고친 A08 전후 첫30 구성과 선정5/18위는 같다. CPM의 prostate 기술과 실제 CAMELYON 입력의 분야도 달라 목적 설명을 정정해야 한다.

최소 뒤집기 자료: LivePublication 원 입력의 생산자/공개 URL과 그 실행에 연결된 파일 명세, 각 사례의 실제 최초 발행일이다. 이것이 나오면 선정 순서만 재평가하고 값 대조 성공을 기준으로 교체하지 않는다.

## Q3 — 발행자가 구별한 판과 소비자의 지목은 동일한가?

답: 동일하다고 볼 수 없는 경우가 대부분이다. 자연층 P4/6와 U1/6, 보강 P2/2와 U_external1/2를 분리했다. U는 구체적인 외부 파일 사용 선언이며 검증된 실제 bytes를 뜻하지 않는다. RUN01의 local H5 선언은 U_local로 남기고 외부 U에 넣지 않았다. 실행 기록상 local 연결2/2와 외부 publisher R1/2도 구별했다. RUN02의 전체 파일 검사는 초기 R0/2를 바꾸는 반증이었다.

직접 근거는 [BCO 발행자 §4](https://essd.copernicus.org/articles/13/491/2021/#section4)와 Assets/DOI137의v3.0.0, [소비자 Fig5](https://essd.copernicus.org/articles/14/19/2022/#section4), [RJ02 당대 archive](https://zenodo.org/records/4026589)의 target_meta/feature, [RUC 보존 General Information](https://web.archive.org/web/20211205084551id_/https://ruc.noaa.gov/raobs/General_Information.html)의 OVERVIEW/STATION HISTORY다. 원문 ID는 S-E010, RJ-A-RSTYLE, S-E060 등이다.

반대 관측: RJ02는 취득일만 있을 것이라는 예상과 달리 당대 명세가16개 filename/version을 지목했다. 반대로 현재 CRAN16개에 도달한 성공은 원 소비 바이트/실행을 입증하지 않는다. 세 tar의 내부 Version과 filename도 서로 달라 단일 키 조인이 틀릴 수 있다. RUC의 실제 원 발행자 문서를 복원했으나 interface 캡처·schema version·station history를 훈련 데이터판으로 읽지 않았다.

최소 뒤집기 자료: 원 소비 파일의 fingerprint, 동일 실행의 입력 명세, 발행자의 같은 객체 대응표다. checksum이 파일 전체인지 decoded content인지 table+metadata인지 알고리즘·범위를 함께 알아야 한다.

이 조건이 실제 충족된 RUN02의 새 근거는 [HG001-part2.md5](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) **388행의 전체 경로**, [archive](https://zenodo.org/records/12622362)의 action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`→Collection→R1, 같은 archive stderr85/105–114다. 전체 보관 gzip의 MD5 `52f3ed344d88278c703faa1280818ce1`이 독립 발행자 목록과 일치했다. 현재 gzip의 MD5는 다르나 전체 decoded bytes는 같다. A10과 pre-full-fastq 스냅샷에 전후 판정을 남겼다. 선택 R1의 기록상 입력 연결을 확인한 것이며 원 과학 실행의 독립 syscall 관측은 아니다.

## Q4 — A/B/C에서 새로 확인한 사실은 무엇인가?

답: B는 후보 발행판을6/8에서 확인하고 RJ03의 후보 Df를 대조했다. C는 외부 파일 선언2/8, local 실행 연결2/8, 외부 발행자 객체까지의 연결1/8, 추가 답 재독4/8을 보여 줬다. 독립 V는0이다. RUN02의 A/B에는 원 실행이 포함되지 않으므로 R0, C에서만 R1이다. N-E01의 C 추가 슬롯은 결측이고, code-only와 output-only를 실제 입력/실행으로 올리지 않았다. 표2와 readings.csv24행에 주소·위치·보이는 값·빠진 고리를 고정했다.

재독 위치는 [RJ007 §5 L246–270](https://journal.r-project.org/articles/RJ-2022-007/)의 runtime/node 설명과 ANOVA Df, [RJ006 §5 L271–273](https://journal.r-project.org/articles/RJ-2022-006/)의 archive 링크, [CPM/WfExS 사례](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210) §3.5/4.2다. ROOT-FINAL-10/13/15/16 및 collection 원관측과 대응한다.

반대 관측: 초안은 RUN A/B visible_values를 막았지만 field/target_time/missing_reason과 RUN02 purpose에 C 정보를 남겼다. 별도 문맥 검토로 발견하고 packet과 audit_only_*를 분리했다(A07/A09). RUN01.C의 local U와 canonical external U 이름 충돌도 고쳤다. 누적 주소·값이 눈가림을 보장하지 않으므로 성능 향상률/인과효과로 해석하지 않는다.

최소 뒤집기 자료: C 선언을 검증하는 다른 계보의 publisher 객체/값 또는 별도 원 실행 영수증이다. 같은 저자의 출력 hash 재독은 그 기준을 채우지 못한다.

## Q5 — 과거 재현과 최신 사용의 판단을 분리했는가?

답: 각 핵심 사례에 원사용/다음판 대조 슬롯을 두고 미확인 사유를 썼다. 발행 연속판의 동일 선정필드 후보쌍은 RJ03의R4.2.0→4.2.1이다. 실제 사용판이 확인되지 않았으므로 진본 사용판 다음판 성공이라고 하지 않는다. IOW 출력판, CPM 소비 crate판, UCI 동시 게시 변형, 서로 다른 시기의 census/GNIP를 같은 종류의 다음 입력판으로 묶지 않았다.

독립 원문 재독은 [PANGAEA936557 Data L116–129](https://doi.pangaea.de/10.1594/PANGAEA.936557?format=html), 이전판889928의 같은depth행, [IOW release1](https://doi.iow.de/10.12754/data-2021-0002)과 [release2](https://doi.iow.de/10.12754/data-2021-0002-01)의 raw/지역별 시트다. PANGAEA depth0.045m의Age2.1→2.574,230Th310.292 불변을 확인했다. IOW 같은B148=1은 두 판에서 다른 종을 가리킨다. 같은 셀·값만 보존하면 같은 행인지도 모른다.

반대 관측: Df2는 UCI 정정 전후 모두 같고 보조 SumSq는436.6/437.1로 다르다. 좁은 Df 예제는 유효할 수 있지만 정확 측정값 재사용은 다르다. N-E02의 cloudy-only median과 all-time median을 불일치로 세지 않았다. RUC format의0.1°C/kelvin, 결측코드, station 유효기간도 소비 export와 분리했다. Wetlab의 처음20 read 일치 뒤 전체 검사를 실제 수행했다. archive/current gzip은487,611,787/413,005,346bytes로 다르나 전체 decoded1,409,966,879bytes와 SHA256은 같다. 발행자 MD5 목록은 archive representation과 일치한다. 다만 현재 표현이 날짜가 확정된 다음 발행판인지, 재압축의 시점·이유는 미확인이다. CHROM1은 FASTQ의 직접 필드가 아니므로 V는 올리지 않았다.

최소 뒤집기 자료: 실제 사용판과 다음 발행판의 같은 행키/필드/단위, 원 반올림·필터·결측·변환, 당사자 정정사유다. 다른 기준기간/표현/필드와의 숫자 차이는 이 조건을 대신하지 않는다.

## Q6 — 다른 분야의 관행과 요구한 음성례를 확인했는가?

답: 공식통계2원문과 지구과학2원문은 직접 읽었다. [ALFRED help L35–40,53–65](https://alfred.stlouisfed.org/help)는 발표일 대체 순서와 반올림 growth를, [download L46–69](https://alfred.stlouisfed.org/help/downloaddata)는 observation/vintage를 구별한다. [NASA CMR DOI](https://wiki.earthdata.nasa.gov/spaces/CMR/pages/107385989/DOI)의 PreviousVersion와 [PANGAEA 실제 판](https://doi.pangaea.de/10.1594/PANGAEA.936557)은 collection/file/정정 계보를 시험한다. ROOT-FINAL-05/06/07/12/14와 ES-REVIEW 재독이 연결된다.

반대 관측: 같은 DOI/숫자/고정 URL은 실제 사용을 증명하지 않는다. 서로 다른 PANGAEA exact URL의 전체bytes 동일성은 실측했지만, 특정 실제 실행이 같은 파일을 **읽지 않았다는** 음성 영수증은 확보하지 못했다. 미래 R release의 시간 제한과 CPM의 시간역전은 그 부정 사실을 대신하지 못한다. PANGAEA metadata 정정 공지는 읽었지만 직전/직후 payload 불변은 미확인이다.

검토 중 또 다른 반증도 있었다. IOW Related가 추출 화면에서 비어 보여 관계 링크가 없다고 의심했으나, raw HTML 재열람에서는 IsNewVersionOf/IsPreviousVersionOf가 모두 있었다(S-E078/079). 도구의 추출 누락을 사이트의 사실 부재로 단정하지 않았다.

최소 뒤집기 자료: 실제 실행의 배타적인 input-read manifest/접근 영수증과 동일한 publisher bytes, metadata 정정 전후 payload다. 두 조건을 각각 수용 원장의 미충족으로 남겼다.

## Q7 — 정보 제거가 어떤 문장을 바꾸며, 독립 기준은 무엇인가?

답: sensitivity.csv40행은 다섯 항목을 하나씩 제거한 근거 감사다. 기록문장의 유지/정정/보류 표시는17행에서 바뀌고, 원래 결측이라 새 손실0인 행은6개다. RUN02의 자료 식별자 또는 실제 사용 근거를 제거한2행에서는 외부 입력 연결 R1→0이다. 선정값까지 확인하는 엄격 V는 제거 전후0이다. 현재 정정 제거의 상태표시 변화0을 “정정 정보가 쓸모없다”는 결과로 해석하지 않았다. 이미 보류였던 사례와 좁은 역사적 목적의 유지가 많기 때문이다.

재독 근거는 [RJ02 §2.1와§5](https://journal.r-project.org/articles/RJ-2022-006/) 및 당대16파일명세, [UCI Iris 정정](https://archive.ics.uci.edu/dataset/53/iris), [IOW 두판](https://doi.iow.de/10.12754/data-2021-0002-01), [N-E02 §5](https://essd.copernicus.org/articles/14/33/2022/#section5)의 자체 출력 정정 공지다. 파일별 evidence IDs와 제거 후 잃는 문장, 최소 복구 자료를 sensitivity.csv 각 행에 적었다.

반대 관측: 구체 명세를 빼면 RJ02 U1→0, fullflowcellpath를 빼면 RUN02의 동명파일을 구별하지 못한다. 현재 정정 공지를 빼면 역사적 인용은 유지해도 현재 지역별 요약/LWP/측정값의 잘못된 재사용을 거르기 어렵다. 숫자 일치만으로 여러 후보판을 하나로 줄이지 않았다.

독립 기준은 **서로 다른 계보의 발행자 객체/정정문과 당대 사용 기록이 같은 객체 및 선정 필드에서 만나는 것**이다. 입력 객체의 교집합은 RUN02에서 확인됐지만 선정 필드까지의 교집합은 아직0이다. 원 실행 입력이 확인된 사례 중 V는 자연층 분모0으로 해당 없음, 보강층0/1이다. 실제 사용자 채택이나 설계 수정 노동 절감은 관측하지 않았다. 최소 후속은 같은 필드의 독립 변환·값 대조이며, 사람이 실제 추천을 채택했는지는 별도 연구다.

## 검산 명령과 재실행 범위

다음은 저장된 근거의 구조와 집계를 검산하는 명령이다. 이미 공개된 과학 분석을 원 환경에서 다시 실행하는 명령이 아니다.

```sh
python -B docs/workstreams/research/AF-RES-047/scripts/consolidate.py
python -B docs/workstreams/research/AF-RES-047/scripts/build_sensitivity.py
python -B docs/workstreams/research/AF-RES-047/scripts/build_report.py
python -B docs/workstreams/research/AF-RES-047/scripts/validate.py
python -B -m workbench.session check docs/workstreams/research/AF-RES-047/manifest.json --fetch
```

실제 시작 명령/시각/출력은 evidence/session-start.json, 결과 전 세션 검사는 evidence/session-check-before-result.json이다. 후자는2026-11-22T22:58:23Z에exit0/passed, outside_paths=[]를 반환했다. 검사 당시 통합 HEAD는89203e81a83d51e581ef81fb04c7573753f87234로 진행됐지만 시작 기준4492dd8과 입력 계약은 유지되고 검사에 통과했다. manifest의 실제 시작 SHA를 현재 SHA로 바꾸지 않았다. 최종 커밋 후 검사 출력은 evidence/session-check.json에 추가하고, 고정 RESULT/수용 파일 원격 재열람은 evidence/fixed-result-reread.json으로 보존한다. HANDOFF는 그 뒤 마지막 단독 커밋이다.

원 실행 미수행 항목의 입력·명령은 각 collection/findings.md에 있다. RJ01은 research_data.xlsx와13열 매핑이 먼저 필요하고, RJ02는당대 export/lintr 환경과원입력fingerprint가 필요하다. N-E01은Fig5 paired-point table, N-E02는원RUC export/분할/seed/weights가 필요하다. RUN01은WSI/XML→H5변환영수증이 필요하다. RUN02의 선택 R1 publisher→local representation 연결은 전체 검사로 완료됐고, 나머지 입력/변환/고정 CHROM행의 독립 검증과 당대입수시각은 남았다. 후대 실행 성공을 원 실행 성공으로 쓰지 않는다.

실제 수행한 전체 파일 명령은 `python -B docs/workstreams/research/AF-RES-047/collection/runs/verify_full_fastq.py --perform`이다. 시작2026-11-22T23:00:16.442063Z, 종료23:09:38.308193Z, exit0이며 wetlab-full-fastq-execution-receipt.json에 실행 당시 script SHA를 남겼다. verify_full_fastq-executed-snapshot.py가 그 원본이다. 별도 문맥 판독은 collection/rjournal/review-adjudication.md/json에 있고 외부 독립 실행 재현은 아니다.

## 수용 원장과 최종 재독

evidence/acceptance-evidence.json은 항목마다 충족/미충족, 분자·분모·단위, evidence 파일/행 또는source ID, 최소 후속을 갖는다. 구조검사는 표8/24/종결3행, CSV8×3/40/90, source ID와고유저작배당, axes 일치, C누출금지, 결측0분모 처리, 소유경로를 확인한다. 콘텐츠의 미확인은 구조검사 통과로 사라지지 않는다.

고정 결과의 SHA·blob·표 행수 재독은 별도 영수증으로 남기고 HANDOFF에 그 SHA를 적는다. 이 문서를 쓰는 시점의 미충족을 나중에 조용히 충족으로 바꾸지 않으며, 추가 증거가 생기면 원 판정과 변경 이유를 함께 보존한다.
