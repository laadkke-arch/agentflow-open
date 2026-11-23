# AF-RES-100 재현·실행 인계

아래는 저장소 루트 기준이다. 원 연구판·원 요구·공석·판정은 봉인② `5d81bcbeb5f1248fc1dd2ce2d825cf6467353673` 그대로다. 재계산은 답을 다시 판단하거나 현재 웹 자료로 옛 corpus를 바꾸지 않는다. 원문 cache와 중간 logical ledger는 git무시이며 아래 절차로 준비한다.

## 1. 커밋된 원장의 복구와 검산

```bash
python -B docs/workstreams/research/AF-RES-100/hydrate_ledgers.py
python -B docs/workstreams/research/AF-RES-100/restore_corpus.py --restore
python -B docs/workstreams/research/AF-RES-100/restore_corpus.py --offline
python -B docs/workstreams/research/AF-RES-100/packet_builder.py --verify
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py --initial
python -B docs/workstreams/research/AF-RES-100/validate_ledger.py
python -B docs/workstreams/research/AF-RES-100/assemble_preseal.py --check
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
```

`hydrate_ledgers.py`는 커밋된 gzip의 원 SHA에 맞게49개 논리 파일을 복원한다. `restore_corpus.py`는7개 고정 공식 archive와3,488개 등록 파일만 검증/복구한다. archive 전체SHA·size, member 경로·유형·등록본문SHA·UTF8를 확인하며 다른 바이트를 대체로 수락하지 않는다. 누락 cache만 원자적으로 설치하고 기존 파일을 덮어쓰지 않는다. 외부 source나 setup을 실행하지 않는다.

이 작업에서 실제 수행한 `--offline`은3,488본문21,845,551바이트와7archive74,551,535바이트가 모두 일치했다. 네트워크요청0·설치/덮어쓰기0였다. 온라인 새cache다운로드·설치 전체경로는실제완전재현하지않았고28개메모리안전검사만별도확인했다. [cache-restore-check](evidence/audit/cache-restore-check.json)에 실제종료0과범위가있다. archive가재압축되어지문이달라져도기존판을임의로갱신하지말고중단한증거를남긴다.

본문을 읽는 래퍼 `read_packet.py`를 다시 호출하면 최초접근 원장에 새로운읽기를 섞을 수 있다. 사전판정 재현에는위 검산을 사용하고, 새읽기는 별도 명명한 후속원장에 기록한다. 이연구의 재개 흐름이 만든중복읽기도 `evidence/resume2/duplicate-reading/`에 격리했으며주32패킷·비용에포함하지않는다.

## 2. 최종 표를 다시 쓰는 절차

최종canonical집계는재개결과판b3f3694를인수한뒤의 `assemble_supplement.py`와 `recompute.py`이다. 입력원장을고치지않으면같은출력이된다.

```bash
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py
python -B docs/workstreams/research/AF-RES-100/recompute.py --write
python -B docs/workstreams/research/AF-RES-100/assemble_supplement.py --check
python -B docs/workstreams/research/AF-RES-100/recompute.py --check
```

`assemble_supplement.py`는sources·outcomes·24교체자리displacement를만든다. `recompute.py`는protocol/packets/judgments/pairs/원접근로그·sources·case-notes·REPORT_NOTES에서첫세표8/32/8,층별분모,민감도,115인용,RESULT와evidence/derived를재구성한다. `--check`는바이트일치를검사하고파일을쓰지않는다. 결과끝은정확3행약점표다.

최소자료계수는감사된46개다. 원래흐름32개와28개가겹치며원래쪽에만4개·재개쪽에만18개가있다. 32가46의부분집합은아니고두수를합산하지않는다. 최종sources에는재개160행+원래143행을보존하고추가timeline/실행계획기록도비산입으로연결한다. 오래된DockerREADME는문서하한에들지만P3의초기최신안정판공석을채우지않는다.

이전 `assemble_evidence.py`, `build_displacement.py`, `evidence/source-summary.json`, `evidence/normalized-outcomes.jsonl`은원래③계수흐름의역사적산출물이다. 최종canonical재생성에는사용하지않는다. 원래문구보다더좁게한P3부재범위와datedacceptance는최종outcomes/REPORT_NOTES와통합감사에기록했다. 원판정은봉인②에서그대로다.

## 3. 추가 자료의 재열람

원자료주소와최초취득지문·구간은 `sources.jsonl`에있다. 같은URL의현재응답이과거payload와다르면새관측으로기록한다. 답·댓글은실시간삭제/수정될수있으므로현재API수집을옛응답으로덮어쓰면안된다.

원래흐름의후속취득절차는 `evidence/outcomes/jq/fetch_outcomes.py`와 `evidence/outcomes/pandoc/collect.py`다. 이스크립트들은연구시점취득영수증을다시쓸수있으므로기존봉인checkout에서무조건실행하지않는다. 고정판에서URL·payload식별자를읽고새시점은새디렉터리에남긴다. 원래주질문과답을다시읽어도새적중으로집계하지않는다.

교차분야고정원문재확인은 `evidence/crossdomain/collect.py`와 `build_records.py`, 별도재개자료의선택적재취득은 `evidence/resume2/crossdomain/reproduce_sources.py --refetch --source gdal-warp-doc`에정의되어있다. 현재SVG보조문서XV2는비고정·비산입이며옛바이트가없으면해당검증을미확인으로남긴다.

## 4. 실행하지 않은 원 요청과 필요한 입력

원8질문을연구자예시값으로완성해실행하지않았다. 현재환경jq1.7·Pandoc3.1.11.1은연구판jq1.7.1·Pandoc3.6과다르다. Rscript와cabal은없다. 다음입력의결손을해소한뒤해당원판과연구판을분리해실행한다. 완전한원실행입력이없으면명령의종료값을성공으로기록하지않는다.

| 사례 | 실행할 원 명령/절차의 보존 위치 | 필요한 입력과 확인할 출력 |
| --- | --- | --- |
| J1 | `judgments.jsonl` 패킷`cc86f215a28e`의 `proposed_answer`에 원JOIN/INDEX구조를유지한debug절차·stderr출력명령을보존 | 실제 `file1.json`,`file2.json` 전체·jq판·성공기대JOIN값. `trace.log`의마지막소비위치와중간pair를확인. `input`→`inputs`만바꾸어정상종료한것은완료아님. |
| J2 | 원revision77962A23…의pipeline, 패킷`b6aad97ea044`·`14f044b30814`의조건부jq변환 | 실제EVTX/XML,각단계출력,유효한전체Events/Eventenvelope,content결손의기대의미. 모든Event의동일Name/content대응과null/요구값을대조. yq대체답은별도경로. |
| J3 | 원revisionC0FE71BE…의Bashscript와패킷`a13997d37fef`의partial제안; 사후Bash근거는별도 | 원settings/Grape JSON·실제환경변수또는파일명인수·Bash판. 확장후argv와 `.new`경로,기존필드보존을확인. filename-argument대안을원JSON내용변수명령과섞지않음. |
| J4 | 패킷`a0007d0fb17a`·`837da1ed6706`의jq변환 | 원describe-volumes응답전체·jq/AWS판. 같은volume의VolName,원Iops유무를확인. 없으면null로남기며공식예시100/300을채우지않음. |
| P1 | 패킷`2c39a224e483`의helper정의및실제호출명변경 | 원Rmd·JPEG/SVG/EMF실물·R/knitr/rmarkdown/Pandoc판·선호설정. 선택경로와PPTX결과를별도확인. 기존 `knitr::include_graphics`를그대로두는대조는helper를호출하지않음. |
| P2 | 원revision245AC802…의 `test1.typ`,`relimport.typ`,`test2.typ` 및원Pandoc명령 | 원CeTZ0.3.4패키지전체/hash,Typst0.13.1/Pandoc3.1.3와연구3.6을분리. 실제import유지·a=123·같은Markdown을대조. 빈dummy/import삭제로통과시키지않음. |
| P3 | 원revision8AA85F98…의build.sh/TEST-includes.txt;첫행동은당시image발행/digest→source확인 | 질문자의실제Dockerfile,6개Markdown,custom TEST-eisvogel.tex,두filter판·pdflatex,실행image digest. 같은디렉터리/mount/entrypoint에서원build.sh실행후단일PDF를확인. 그전에는B공석을임의채우지않음. |
| P4 | 원revisionC5257A15…의title/Markdown입력과패킷`ac9beb264939`의quotedtitle수정 | Pandoc2.18에서같은title의metadata/AST와parse종료값. 전체PDF는외부filters/TeX/원문입력추가확인이필요하며이과제에서렌더링하지않음. |

네개의고정원시험을실행하려면 [upstream-execution-plan.md](evidence/audit/upstream-execution-plan.md)의실제runner명령·archive입력·준비조건을사용한다. 현재그suite통과를주장하지않는다. GDAL/Sphinx 원시험의정확pytest node·fixture값·한계는 [crossdomain/unrun.md](evidence/crossdomain/unrun.md)에있다. 특히GDAL135s는먼저원문그대로trace를보존하고,생성grid경로가실제로전달되었는지확인한다.

## 5. 실제 수행된 교차분야 보조 실행의 범위

별도재개흐름은원8요청과별개로아래프로그램을실행했다. 이미기록된runtime.json을기존관측으로보존하며재실행은새관측으로분리한다.

```bash
/usr/bin/python3 -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_gdal_fixture.py
python -B docs/workstreams/research/AF-RES-100/evidence/resume2/crossdomain/run_graphviz_probe.py
```

GDAL3.10.3/PROJ9.6.0의파생입력5조건과Graphviz2.42.4의별도DOT→SVG probe였다. 고정원문GDAL3.10.0/PROJ9.5.1의상류pytest suite나Sphinx8.1.3빌드가아니다. Sphinx부재로원Sphinxfixture는미실시했다. runtime영수증의다른workspace절대경로는원실행기록이며이checkout에존재하는입력으로오인하지않는다. runner가자기실행위치아래에파생입력을만드는지먼저확인해야한다.

## 6. 작업 계약과 공통 검사

결과판을커밋하고원격SHA를확인한뒤실행한다. 실제검사대상SHA·종료값·범위·공통검사에서개별계약이skip되었는지는 `evidence/result-checks.json`과최종HANDOFF에남긴다.

```bash
python -B -m workbench.session check docs/workstreams/research/AF-RES-100/manifest.json --fetch
python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean
```

공통검사의환경라벨은계정연결의증명이아니다. 공통검사가성공해도이research manifest의개별검사가건너뛰어졌다면위직접 `check --fetch`의별도종료값으로범위를확인한다. GitHub검사는고정결과SHA의RESULT·원장·재현문서를실제로재열람하고파일blob을대조한다. 중앙지표·096자료를수정해검사를통과시키지않는다.

검사실행의표준경로는 `run_result_checks.py --target <40자리결과SHA>`다. 공통검사의고정 `.workbench`출력을owned_path안에두기위해,같은결과SHA의수정없는detachedworktree를 `evidence/_cache/verification-<SHA앞12자리>/`에만들고위두명령을그안에서실행한다. checker를패치하거나계약을우회하지않으며영수증에실제cwd·HEAD·clean시작/종료·stdout/stderr·skip사유를보존한다. 임시시험디렉터리도owned_cache아래TMPDIR를사용한다.
