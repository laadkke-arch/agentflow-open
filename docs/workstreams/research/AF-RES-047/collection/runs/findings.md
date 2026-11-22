# 실행 기록 우선 보강층 — RUN01·RUN02 조사 결과

## 결과와 분모

서로 다른 프로젝트의 실제 적용 실행 두 건을 읽었다. 두 건은 자연6건의 보존율 분모에 넣지 않는다. 발행자 객체 존재 P=2/2, 외부 파일 구체 사용 선언 U_external=1/2, local input 사용 선언 U_local=2/2, 기록 내부 action→input 연결 R_local=2/2다. 전체 FASTQ 후속 검사(A10)에서 RUN02의 보관 R1이 독립 발행자 checksum 목록과 일치해 R_publisher는 **0/2에서1/2로 바뀌었다**. 고정한 출력 필드를 독립 대조한 V는0/2이며, C의 답 재독은2/2다. 조건부 V|R_publisher는 이제 **0/1**이다. 원래0/2 및 분모0 집계는 before-full-fastq snapshots에 보존했다. R은 당대 runID/input 명세와 독립 publisher fingerprint의 연결이며, 별도 machine-I/O 증명을 요구하지 않는다.

| 사례 | 목적·고정 필드·값 | 보관 실행과 입력 | 독립 발행자와의 연결 | 유지/정정/보류 |
|---|---|---|---|---|
| RUN01 CPM | 실제 Camelyon16 영상 fragment를 처리한 학습/평가. predictions.h5 `/test/test_001/table`의 첫 논리 열 `coord_x=63488`, y=4096, slide=test_001. 원 기술문의 prostate carcinoma라는 목적은 입력의 실제 기관과 불일치한다. | [CPM v1.1](https://zenodo.org/records/8095888), metadata의 test CreateAction 및 `prov_test.log`; local cam16_mrxs.h5의 table hash를 지목한다. hash는 전체 HDF5 byte hash가 아니다. | [CAMELYON 원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC6007545/) Data description/validation/Tools, [공식 README](https://camelyon-dataset.s3.us-west-2.amazonaws.com/CAMELYON16/README.md) Overview/Notes, [test_001 XML](https://camelyon-dataset.s3.us-west-2.amazonaws.com/CAMELYON16/annotations/test_001.xml). 원 발행판 식별자는 없다. archive XML은 publisher XML과 좌표 정밀도·이름·hash가 다르다. 원 publisher polygon vertex와 소비자 patch 시작점은 동일 필드가 아니다. | 당시 local test 출력의 존재는 유지. prostate 입력이라는 이해는 정정. 진본 원 발행판과 coord_x 독립 대조는 보류. |
| RUN02 Wetlab2Variations | NIST GIAB NA12878 FASTQ를 사용한 chromosome1 gVCF 생성. 첫 gVCF record의 CHROM=`1`; POS1, END63267, DP0. | [Zenodo archive](https://zenodo.org/records/12622362) action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d` → collection `#dcc0e6bb-4888-4bee-bc06-e995b5d18538` → R1 File. 전체 R1SHA256이 이 File 선언과 일치한다. | [NIST MD5목록](https://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/data/NA12878/NIST_NA12878_HG001_HiSeq_300x/HG001-part2.md5) **388행**의 exact flow-cell/R1 경로 MD5 `52f3ed344d88278c703faa1280818ce1`이 실제 보관 gzip 전체와 같다. 현재 publisher gzip은 MD5 `24ba6bb88db052d4bf64ac98131d6005`로 다르지만 전체 decoded 내용은 같다. | 기록상 외부 입력 연결 R=1로 정정. CHROM 독립 출력 대조 V=0 유지. 재압축 시점·명명된 다음 발행판은 미확인. |

## Q2: 어떻게 두 건을 선정했는가

출발점 [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/)의 공개 examples 목록과 연결된 [논문 Data Availability](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210), [고정 GitHub examples 디렉터리](https://github.com/ResearchObject/workflow-run-crate/tree/89025e50dbef6960c3b3e56b15eb04cd033b888c/docs/examples)를 따랐다. 원장에38노출을 보존했으며2021–2024년31개 중 발행일·식별자 순 최초30을 남겼다. 원목록19개에서 연결된 디렉터리로 확장한 이유와 원본은 변경 원장에 있다. metadata의 실제 publication/datePublished는 때때로 export 날짜다. 최초 공개 Git 커밋 날짜를 별도로 복원하지 못했으므로 엄격한 역사적 발행순 확정에는 한계가 있다.

RUN01은5위, RUN02는18위다. earlier Promort의 input URL은 비공개 slide repository, BackTrackBB는 synthetic seismic 입력, MIRAX 예제는 interoperability fixture였다. Workflow 정의나 typed/revsort fixture를 실제 분석으로 바꾸지 않았다. CPM은 작은 fragment를 사용하지만 실제 제3자 영상의 처리·학습·평가와 산출물·실행 로그가 있으므로 응용 실행으로 포함했다. “example”라는 이름 자체는 제외 사유가 아니다.

15위 [LivePublication orchestration crate](https://livepublication.github.io/LP_Pub_OrchestrationCrate/)에는 실제 성공 실행과 입력·출력 연결이 있다. 그러나 [원 논문 §V](https://ir.canterbury.ac.nz/server/api/core/bitstreams/9355936b-5029-4b0c-8452-564bb8efad93/content)도 standard language-ID dataset이라고만 하고 제3자 공개 입력의 이름·생산자를 확인하지 못했다. 적격 **미확인**으로 남겼으며 다른 데이터셋을 추측하여 넣지 않았다. 이 앞선 사례의 공개 입력이 밝혀지면 “최초2” 선정을 뒤집을 수 있다. 따라서 프레임의 실제30노출은 충족하지만 최초2의 엄격 확정은 조건부다. 값·정정 성공을 본 뒤 두 사례를 바꾼 적은 없다.

## Q3·Q4: 판·사용·실행의 서로 다른 연결

CPM [개념 DOI 7676923](https://doi.org/10.5281/zenodo.7676923)은 최신 [v1.1 8095888](https://zenodo.org/records/8095888)로 이어진다. [v1 7676924](https://zenodo.org/records/7676924)와 v1.1의 publication_date는 모두2023-02-25이지만 생성일과 archive MD5가 다르다. 이것은 **소비자 보관물**의 판 목록이며 Camelyon 발행판 목록과 같지 않다. 원 publisher dataset DOI10.5524/100439의 존재만으로 archive 안의 transformed XML/HDF5를 그 DOI의 특정 바이트로 확정할 수 없다.

CPM test log의 table hash는 [당대 RationAI 코드](https://raw.githubusercontent.com/RationAI/crc_ml-provenance/12ab3f8f5f441e385eeab5d66f5ba1516f2cb870/rationai/utils/provenance.py) `hash_table` lines189–209에서 pandas object hash와 metadata 문자열을 함께 계산한 값이다. 파일의 SHA256과 같은 이름으로 저장하면 잘못된 불일치/일치 판정이 생긴다. 원 test는2023-02-24에 끝나며 v1.1에 보관된 preprocess는2023-03-16이다. 동일 이름 input·동일 output·서로 다른 provenance를 한 과거 실행으로 합칠 수 없다.

Wetlab GitHub export의 action `#2f5723c2-6d4f-4425-8bf7-47e240585fe9`와 Zenodo archive의 action `#bdfcc6a4-3bf4-4fd7-9e8c-cc6b0deaa43d`는 다르다. 같은 staged directory·run time·output hash는 보조 비교 정보다. 핵심 C는 **archive 안의** action·collection·local File·stdout·VCF만 연결했다. `runs.csv`는 이 export들을 별도 행으로 보존한다. 실제 계산한 VCF SHA256 `79c41a5eac5d7ebf46d91f3b802b8a79f2c92d946b46bef02828719b992c61c2`는 archive graph와 같고 SHA1은 stdout과 같았다. 이것은 같은 저자 계보의 내부 완결성 검사다.

A/B에서는 C의 실제 output 값을 누출하지 않고 visible_value=null을 유지한다. root 최종 검토에서 RUN02 A/B purpose의 chromosome1 parameter도 audit_only_full_purpose로 옮겼다. B는 publisher exact path/MD5와 현재 served gzip의 불일치를 보여 주지만 어느 소비자 파일이 목록과 맞는지는 모른다. C에서 당대 archive를 추가하면 **실측 archive MD5가 독립 publisher manifest와 일치**하여 RUN02 R을 확인할 수 있다. 출력 CHROM1은 여전히 기록 재독이며 독립 V가 아니다. readings.csv6행과 cases.json의 A/B/C에 각각의 범위를 보존한다.

## Q5·Q6: 처음 결론을 약화한 반례

1. **같은 출력 바이트, 다른 보관 입력/계보.** CPM v1/v1.1의 predictions.h5와 원 test log는 각각 전체 byte hash가 동일하다. 반면 derived cam16_mrxs.h5는 크기324181이 같아도 파일 SHA256은 서로 다르고132바이트가 달랐다. 검사한33개 primitive table/index arrays의 내용 hash는 모두 동일했다. 모든 metadata의 의미를 복호화한 것은 아니므로 “오직 timestamp 변경”이라고 단정하지 않는다. 출력값만으로 어느 preprocess/보관판을 사용했는지 결정할 수 없다는 반례다. `cpm-edition-comparison.json`, `cpm-input-edition-comparison.json` 참조.

2. **바이트 불일치가 곧 값 정정은 아니며 현재 파일만이 유일한 발행자 기준도 아니다.** 처음에는 첫20 FASTQ records만 같아 전 파일 동등성을 보류했다. 후속 전체 스트리밍에서 archived gzip487611787바이트와 현재 publisher gzip413005346바이트를 각각 끝까지 읽었다. 두 파일의 전체 decoded1409966879바이트와 SHA256 `98be27b898b6ae3c12821a30b48adc1bfec9d98903219f0175240ebac66fccf3`가 같다. 더 결정적으로 publisher MD5목록388행은 **현재 gzip과 불일치하지만 보관 gzip과 일치**한다. 따라서 현재 gzip byte mismatch만으로 원 실행의 외부 원객체 연결을 거부했던 판단을 R0→1로 바꿨다. 이 입력 쌍의 decoded 내용 정정은 관측되지 않았으며 실제 재압축 시점·명령은 알 수 없다. 최초 prefix evidence는 그대로 두고 `wetlab-full-fastq-comparison.json`, `wetlab-full-checksum-revisit.json`, `wetlab-full-fastq-interpretation.json`에 추가 근거를 보존했다.

3. **서로 다른 URL이 같은 바이트.** [regional S3 XML](https://camelyon-dataset.s3.us-west-2.amazonaws.com/CAMELYON16/annotations/test_001.xml)과 [global S3 XML](https://camelyon-dataset.s3.amazonaws.com/CAMELYON16/annotations/test_001.xml)을 각각 전체 내려받았다. final URL도 다르게 유지됐고281405바이트, SHA256 `b487308cb057d064891d082a3f088aa0a7cc260a95e9879c141bf8244ff29e67`가 같았다. 첫 URL의 MD5 `59279f7dc2b6dd4a741904aca621501a`는 publisher checksums.md5와도 같다. 주소 개수를 판 개수로 세면 안 된다. 같은 저작의 alias이므로 최소수 추가0이다.

4. **같은 filename이나 수치가 다른 행을 뜻함.** NIST MD5 목록에는 U5c_CCGTCC_L001_R1_001.fastq.gz라는 basename이 서로 다른 flow-cell path에 있으며 hash가 다르다. SampleSheet에는 같은 U5c SampleID의 Lane1·Lane2가 별도 행이다. 선택단위는 full flow-cell path와 R1이다. 또 CPM의 patch is_cancer=False와 publisher reference.csv의 whole-slide test_001=tumor는 대상 단위가 달라 모순이 아니다. 대안 필드를 이용해 사전 선택 coord_x를 바꾸지 않는다.

5. **현재 재사용의 목적이 달라지는 사례.** CAMELYON README는 normal_86 오분류를 tumor_111로 정정하고 duplicate test_049를 제거했다고 명시한다. 현재 분류 자료를 원하는 이용자에게 옛 이름·옛 category를 그대로 추천하면 안 된다. 그러나 당시 분석의 재현에는 당시 이름과 필터도 필요하다. 선택 test_001 patch의 다음 발행판 값/정정은 확인하지 못했다. 원 소비 기술문 “prostate”와 실제 sentinel lymph-node 입력의 목적 불일치 역시 checksum만으로 걸러지지 않는다.

6. **같은 고정 URL/바이트지만 이 실행은 읽지 않았다는 엄격 음성례는 미충족.** CPM 시간 역전과 동일 output hash는 계보 결정 불가능을 보인다. 다른 preprocess가 나중에 생성됐다는 사실이나 action에 객체가 없다는 사실만으로 원 실행의 미사용을 증명하지 않았다. 이 조건을 충족하려면 해당 실행 범위의 완전한 input capture/trace 또는 명시적 미사용 기록이 필요하다.

두 사례 모두 사용판과 **명명된 다음 publisher 판의 고정 출력 필드 정정 쌍**은 완결하지 못했다. CPM 소비 archive v1/v1.1을 publisher의 다음 판으로 세지 않는다. Wetlab의 사용 입력 표현은 publisher MD5로 확인했지만 현재 served 표현과의 시간적 발행 순서/다음판 이름/재압축 공지는 미확인이다. 원 입력 표현의 확인 R=1과 다음판·선정 CHROM 출력의 확인 V=0은 별도다.

## Q7: 정보 한 항목 제거 감도

| 제거 정보 | 적용 사례와 관측 | 남는 주장 / 사라지는 주장 | 판단 |
|---|---|---|---|
| 시간 목적 | RUN01의2023-02-24 test와03-16 preprocess, prostate vs 실제 lymph-node 목적 | 파일/값의 존재는 남지만 동일 역사적 실행과 용도 적합성은 판단 못 함 | 역사 재현·현재 추천을 분리하지 않으면 보류가 잘못된 유지로 바뀔 위험 |
| 자료 식별자 | RUN02 full flow-cell path와 R1 ID 제거 | 같은 basename이 다른 flow-cell의 MD5를 갖는다. 전체 내용 hash가 있어도 원 publisher 행·대상기간을 특정하는 기준이 사라진다. | U_external과 R_external의 해당 exact-path 연결을 보류로 낮춤 |
| 실제 사용 근거 | RUN02 archive action→collection→File과 CPM test log 제거 | publisher fingerprint와 archive bytes 일치는 남지만 어느 원 실행의 입력인지는 연결 못 한다. | R_local2/2→0/2, R_external1/2→0/2. V0/2는 그대로 |
| 당시 값 | RUN01 HDF5 첫 행, RUN02 VCF 첫 행 제거 | RUN02 입력 표현과 원 실행 연결 R은 남지만 고정 output coord_x63488/CHROM1 재독은 불가하다. | C 값 재독2/2→0/2. R_external1/2는 유지, V0/2는 그대로 |
| 현재 정정 | CAMELYON README Notes의 normal_86/test_049 정정 제거 | 원 기록 재현은 가능하나 최신 category 추천의 무효 사유를 잃음. 핵심 test_001의 정정 여부는 애초 미확인 | 현재 재사용 관련 경고 근거가 사라짐. 핵심 V0는 유지 |

제거 감도는 실제 보이는 근거가 허용하는 문장의 변화다. RUN02는 독립 publisher fingerprint와 당대 run 명세가 만나는 입력 연결 R을 확인했고, 그 기록을 빼면 이 주장이 사라진다. 두 사례의 선정 출력 V는 여전히 보류다. 실제 이용자의 추천 채택은 관측하지 않았다.

## 원문 수와 독립성

`sources.jsonl`에는90개 직접 열람/접근/중복 기록이 있다. 최소수에 더하는 고유 저작은8개이며 소비/원 실행보고2, publisher 자료2, author provenance 실제 사례/코드4다. 실패·미러·같은 archive의 파일/판·재방문은 추가하지 않았다. author4는 [Workflow Run RO-Crate 원 논문](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210)의 실제 case §3.5·4.2, CPM 당대 실행에 지목된 별도 RationAI 코드 저작, LivePublication 실제 orchestration artifact, WOMBAT 실제 proteomics 실행 artifact다. 원 논문/소비 archive/코드는 독립 계보 검증으로 세지 않는다. 전체 archive member/current publisher/MD5 재독3행은 같은 두 저작의 추가 범위이며 최소수 증가0이다.

보조 WOMBAT는 [Zenodo10091550 archive](https://zenodo.org/records/10091550)의 실제 action `#450004f9-05b1-43a6-9e99-9f828e44abfa` → RAW/FASTA input → protein CSV를 읽었다. CSV40행 중 첫 P05413, abundance_A_1=17.1383637394425다. 계산 SHA256은 graph와 같다. `test_data` 경로를 공개한 실제 계산이지만 외부 실험판 검증은 하지 않았으며 핵심8/보강2/자연6 어느 분모도 늘리지 않는다. `auxiliary-evidence.json`에 source·입력·출력·한계가 있다. 이 네 author 항목의 배당 적합성에 대한 외부 독립 판독은 없고 자체 재판독만 수행했다.

## 수행한 전체 입력 검사와 남은 재개 행동

전체 입력 검사는 다음 고정 명령으로 **실행했다**. wrapper 시작2026-11-22T23:00:16.442063Z, 종료23:09:38.308193Z, exit0이며 약9분22초 걸렸다. 두 gzip 전체를 디스크에 저장하지 않고 스트리밍했다. HTTP 오류나 retry는 없었다. `wetlab-full-fastq-execution-receipt.json`에 명령·입력·시각·stdout·종료코드·실행 당시 SHA를, `verify_full_fastq-executed-snapshot.py`에 실행 당시 원본을 보존했다. 후속 판단은 전체 decoded 일치만으로 자동 승격하지 않고 독립 publisher manifest의 exact-path MD5까지 다시 대조했다.

```bash
python -B docs/workstreams/research/AF-RES-047/collection/runs/verify_full_fastq.py --perform --output docs/workstreams/research/AF-RES-047/collection/runs/wetlab-full-fastq-comparison.json
```

원래 코드의 publisher_matches_read_checksum_list=false는 실행 실패가 아니라 중요한 관측이다. 목록의 MD5는 현재 gzip 대신 보관 gzip과 일치한다. 이 독립 fingerprint와 같은 archive의 원 runID/input 명세가 결합해 R=1이 된다. 다음 첫 행동은 독립 CHROM 출력 검증에 필요한 원 CWL·전체 입력/참조판·당대 컨테이너 환경을 확정하는 것이며, 취득/재압축 시점은 별도 역사 기록으로 찾는다. 서로 다른 GitHub export UUID를 이 성공으로 자동 승격하지 않았다. 원 컨테이너 분석은 재실행하지 않았으므로 V는0이다.

CPM의 작은 산출물을 재확인하는 명령과 입력은 다음과 같다. `read_zip_member.py`는 named member만 HTTP Range로 읽고4MB를 넘는 단일 요청을 거절한다. 큰 실제 workflow 재실행은 하지 않았다.

```bash
python -B docs/workstreams/research/AF-RES-047/collection/runs/read_zip_member.py https://zenodo.org/api/records/8095888/files/rocrate.zip/content 5743833272 docs/workstreams/research/AF-RES-047/collection/runs/recheck-cpm predictions.h5 cam16_mrxs.h5 prov_test.log
python -B docs/workstreams/research/AF-RES-047/collection/runs/read_h5_capi.py docs/workstreams/research/AF-RES-047/collection/runs/recheck-cpm-predictions.h5
```

당대 table hash를 다시 계산하려면 pinned `rationai/utils/provenance.py::hash_table`와 당시 pandas/PyTables 및 metadata를 먼저 확정해야 한다. 단순 `sha256sum cam16_mrxs.h5`는 대체 검사가 아니다. publisher XML/TIFF와 원 취득·변환 영수증을 얻어 해당 patch 좌표의 생성 규칙을 복원한 뒤에야 coord_x의 독립 V를 재판정할 수 있다. 실제 원 실행의 미사용을 증명하는 추가 trace와 앞선 LivePublication 입력의 공개 출처가 다음 우선 자료다.

원문 전체 복사본·임시 바이너리는 해시·주소·추출 영수증·관측 요약을 보존한 뒤 정리했다. 범위와 재생 명령은 `disposition.json`에 있다. 소스에서 받은 코드는 실행하지 않았고, 읽기/해시/형식 해석만 수행했다.
