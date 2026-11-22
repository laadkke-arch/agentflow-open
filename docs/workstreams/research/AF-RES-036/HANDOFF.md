# AF-RES-036 · 현재 근거를 같게 둔 이력의 추가 가치

## 인계 상태와 고정 결과

**REVIEW_READY_WITH_GAPS. 수용 조건 33개 중 28개 충족, 5개 미충족(C05/C07/C09/C15/C28).** 이력 추가의 행동 이익은 이번 표본에서0/12였으며 그 음성 결과를 보존했다. 필요한 표본·원문 최소수·48결정·짝비교·조건부 비용 계산·Q1–Q8 점검은 완료했다. 표집 편차·완전 비중복성·날짜 있는 서지 정정 사슬은 해결된 것으로 표시하지 않았다.

**결과 SHA: `ef839d30d300e20f092dd7f0d57542f0773b77f8`**

- [고정 RESULT.md](https://github.com/laadkke-arch/agentflow-open/blob/ef839d30d300e20f092dd7f0d57542f0773b77f8/docs/workstreams/research/AF-RES-036/RESULT.md)
- [고정 SELF_CHECK.md](https://github.com/laadkke-arch/agentflow-open/blob/ef839d30d300e20f092dd7f0d57542f0773b77f8/docs/workstreams/research/AF-RES-036/SELF_CHECK.md)
- [고정 수용 근거](https://github.com/laadkke-arch/agentflow-open/blob/ef839d30d300e20f092dd7f0d57542f0773b77f8/docs/workstreams/research/AF-RES-036/evidence/acceptance-evidence.json)

이 HANDOFF는 **2026-11-22 17:25:14 UTC**에 위 고정 SHA의 RESULT·SELF_CHECK·수용파일·집계·검사 본문6개를 GitHub에서 재독하여 제출 바이트와 일치함을 확인하고, **17:25:49 UTC**에 같은 SHA의 `workbench.session check --fetch`가 exit0으로 끝난 뒤 작성했다. 작성 시작 확인은17:26:09 UTC 이후다. 한국 시간으로2026-11-23 새벽에 수행했다. 자체 커밋 SHA를 파일 안에 만들어 넣지 않으며, 이 파일의 마지막 commit은 아래 git 명령으로 찾는다.

## 가장 작은 재사용 결과

| 단위 | 관측·재계산 결과 | 허용되는 해석 |
| --- | --- | --- |
| 원 참조 | G6/R6, 서로 다른 출판문서12,9프로젝트,프로젝트당최대2,공유원배포9 | GNU직접/Debian재배포와Bioconductor실제HTML을구별. 원문장·href·멤버hash 고정. |
| 목적 층 | 현재 작업7,특정판1(G03),시간의도애매4;R특정판0 | 현재7은최신판요구7이아니다. 빈층을사후추가하지않음. |
| 판독 | 48=12×4; B/BH 각각보류12; BN/BNH 각각유지11·교체1 | 동일N에서H에따른행동변화0/12. B에는이미원판·멤버·목적이있고N은필요한추가절/PDF/source까지포함한다. |
| 기준판정 | 별도문맥의추가원문확인으로KEEP11/REPLACE R01;기준보류0 | 전12개발행자/핵심본문공유. 외부독립gold0이며내부기준일치를실사용정확도로부르지않음. |
| H의후보주소 단서 | R01 BNH가rnaseqGene1.12.0 tarball을제시;verified=false | 행동개선0. 이후검증HTML대체절을판독당시주소선택성공으로소급하지않음. |
| 고유 원문 | 적격하한50=소비자12+현재10+별개과거10+보조16+기타2 | current코드/목록제외설명본문8. 원고중복·미러·검색·실패는추가산입안함. |
| 최종 원장 | sources81행·aliases144,attempts301,costs303,sensitivity612,비교집계255 | source행81은적격원문수가아니다. 후기재독18source는기존원문variants이고추가최소수0. |
| 엄격 민감도 | 수집사전노출제외10,프로젝트/target관계까지제외3,카드이력까지제외2,reported선행단서+카드이력제외1 | 각각행동변화0. 모든목적해석제외0/외부gold만0은‘해당없음’이며무효과증거가아님. |

핵심 반례는 G05다. 원 소비자의 `-MM` 규칙 목적을 현재 GCC의 정확한 절이 제공하므로 추가10.1.0 H가 행동을 바꾸지 않았다. G03은2018판 보존이 중요하지만 B와 현재2018 원문에 그 판이 이미 있어 H가 꼭 필요한 사례가 아니다. R03의현재N은함수source까지읽은증거이며HTTP200만으로기능을확인한것이아니다.

원판을 무조건 최신판으로 바꾸면안되는 보조 반례도 남겼다.2024 POSIX Shell의옛`tag_18` 후보는200이지만해당anchor가없고`tag_19`가있다. 원G01/G03 href는fragment가없으므로원링크실패수에가산하지않았다. BLS/Census는2024이전QCEW에옛county를유지하고,ONS는과거연도에2023경계를적용한다. 서지에서는SEP의1953판/Anscombe/p.222 인용과Nagoya의Takano2016에근거한명시정정을서로다른사례로보존했다. head판과ornaments판의귀속논쟁을같은사슬로합치지않았다.

## 비용과 설계에 넘길 조건

| 범위 | 실제 GET·HTTP exchanges·실패 | 받은 최종 body / 임시 full-body 저장 | 요청별 경과 합 |
| --- | --- | --- | --- |
| 원수집·카드 구성 | 157 /169 /11 | 200,386,741B /동일 | 1453.758885초 |
| 결정 봉인 뒤 기준 확인 | 59 /67 /2 | 56,698,339B /동일 | 493.333131초 |
| 재개 전 두 단계 합 | **216 /236 /13** | **257,085,080B /동일** | **1947.092016초** |
| #2 재개 원문 감사만 | 10 /12 /1 | 5,951,115B /0B(정확발췌JSON은별도보관) | 57.063329초 |
| 측정된 전체 합 | **226 /248 /14** | **263,036,195B /257,085,080B** | **2004.155345초** |

재개 웹도구24동작·로컬import실패1건은별도미계측이다. 이들을GET나0byte네트워크요청으로바꾸지않았다. 위경과합은벽시계·사람노동·모델요금이아니고, body bytes는wire/header/redirect중간body를포함하지않는다. 전체원문을Git에영구보관했다는뜻도아니다. 근거는 [실험비용 요약](evidence/cost-summary.json), [재개비용 요약](evidence/resume-cost-summary.json), [costs.csv](costs.csv)다.

두 번째 조회는 **실측하지 않은 모의**다. 같은URL/크기/상태·이미알려진locator를가정했다. 현재N내용을다시구성하는과업에서는C1/C2가모두물리17GET·24exchange·3,056,003B로같다. 같은N/H내용을모두다시구성하는과업에서만C1은29GET·37exchange·16,067,466B,C2는17GET·24exchange·3,056,003B와저장H읽기12회다. 차이12GET·13exchange·13,011,463B를실제시간·요금절감으로보고하지않는다. 참조당2GET/각30초예산의수적충족과실제timeout성공도구별했다.

실제직렬화예시는문맥+링크C1 7,754B,원판을이미포함한B C1 12,153B,B+H+provenance C2 38,145B다. 모의비교는더강한B C1을사용했다. 따라서C2추가25,992B는해당하위구성차이이며판정이력전체·원N시각·전체문서·DB/Git압축·운영비측정이아니다. C0최초제품발견·C1경로재발견·사람판독비용은미측정으로남겼다. 현재목적에는재방문C1,같은과거근거재구성에는조건부C2를선택지로남기고제품DB·자동교체정책을확정하지않았다.

## 미충족 조건과 범위

| 조건 | 남은 미충족 | 다음 최소 확인 |
| --- | --- | --- |
| C05 | G06/R04가선정전target에노출되어전체12완전미노출표집불가 | 현재10개제외민감도보존. 새독립묶음은소비자href봉인과target조회주체를분리. |
| C07 | Debian coreutils9.1-1 및R중간patch의모든fallback소진미확인 | 공식9.1-1 docartifact의HTML부터확인. 기존12를사후교체하지않음. |
| C09 | G06의stable한정은원문newest보다강함 | 원문newest만의새입력또는stable명시문장이필요. 현재봉인및제외11개분모보존. |
| C15 | N카드의이력5건과N/H/소비자원고중복이있어완전한의미분리불가 | 해당제외값과같은원문군보존. 새비중복사례의사전설계만별도수행. |
| C28 | 명시정정문구는있으나같은서지record의날짜있는전후·소비자반영사슬없음 | NULDL000040/ESTCR17253의Norton표기이전고정판과정정영수증. ornaments판R13935는별도연구. |

이중C28은확인된정정쌍보다강한역사사슬조건이다. ‘실제서지정정이없었다’고요약하면틀린다. 도서관은정정과Takano논문을명시한다. 또한모든발췌1600자이내와metadata포함카드1600자를혼동하지않는다. 전체N은G04 2113·R04 1692자이며정확입력은유지했다. [ERRATA.md](ERRATA.md)에날짜·위치·집계범위정정을모두남겼다.

## 입력·환경·커밋 순서

| 항목 | 확인 값 |
| --- | --- |
| 저장소·작업 브랜치·소유 경로 | laadkke-arch/agentflow-open · work/research-af-res-036 · docs/workstreams/research/AF-RES-036/ |
| 원 계획 기준 | chore/workspace-foundation@d3fbd08d44fd0e2915d1f766721a81845bacc213 |
| 최초 manifest 시작판 | 9668632e915d508e93ddfdc5e8fe4b88bcbfec56;기존파일바이트유지 |
| #2 재개 작업판 | f403243dbf5f097536a1fd9fda55dfce4382329a |
| 재개·인계전 확인 integration | 8dd88b74735eb512c133f1a30890ac82fbf61ecf |
| 의존 입력 | AF-RES-023@a9178ca95979564fd8801559d90d15db4ddac91b;AF-RES-032@b4dcf0a1ca3f2066629869ac1a9347ad2f5717df |
| 실제 환경·모델 표시 범위 | ChatGPT Work 공유Linux shell·GitHub connector·공개웹. 세션선언GPT-6 Astra Pro;계정모델UI·추론강도별도관측안함. 내부검토자는같은모델계열. |
| 원B/보기/결정 봉인 | bd3c17e… /442292b… /5fbde38…;전체SHA는PROGRESS.md |
| #2 원장·감사 정정 | b47d567c4285821e59af0db0081e3b79f0675f26;원격59파일본문대조 |
| #2 결과·SELF_CHECK·수용 고정 | **ef839d30d300e20f092dd7f0d57542f0773b77f8**;원격본문6개대조 |

새진행표·main병합·제품구현·유료API·계정변경은수행하지않았다. dot-control.json과공통문서·기존Studio를수정하지않았다. GitHub expected_sha와검증된fast-forward만사용했고기존브랜치나커밋을초기화하지않았다. `PROGRESS.md`의초기기록이늦게갱신되었지만실제commit순서와봉인바이트를우선한다.

## 실제 검사 영수증

| 검사 | 실제 대상·입력 | 결과 | 확인하지 않은 범위 |
| --- | --- | --- | --- |
| 원장 통합·봉인 hash·표 산술 | 결과SHA ef839d30…,원장·report exact inputhash | [audit-result-sha.json](review/resume-quant/audit-result-sha.json), **81/81,exit0** | 원문참값·실제사용자성과·외부모델재현아님 |
| 문서·필수표·Q1–Q8·수용산술·근거path·소유경로 | 같은결과SHA와입력hash | [document-check-result-sha.json](evidence/document-check-result-sha.json), **21/21,exit0** | 웹페이지영구가용성/전원문내용재검아님 |
| 계약·의존SHA·원격최신성·허용경로 | 같은결과SHA,manifest SHA256은실행영수증에있음 | [session-result-execution.json](evidence/checks/session-result-execution.json), [stdout](evidence/checks/session-result.stdout.json), **passed/remote_checked/exit0** | 제품실행·새AI대화연결검증아님 |
| 결과 원격 재독 | 같은고정SHA의RESULT/SELF_CHECK/acceptance/counts/document-check/audit-final | [result-remote-reread.json](evidence/result-remote-reread.json), **6/6본문일치** | metadata만조회한결과가아님. 그후HANDOFF작성. |
| 소프트웨어 주요 원문 재조회 | 후기9고유URL·10GET,정확발췌/offset/hash | [resume-sources audit](review/resume-sources/audit.json),기준뒤집힘0 | 전12의신규실험이나실제2회차C1/C2비교아님 |
| 비용 별도 내부 감사 | f403243의정확입력hash | [cost-audit.json](review/resume-cross-costs/cost-audit.json), **57/57,exit0** | 후속문서까지검사한값으로소급하지않음 |

이 파일 작성 후의포인터/선행영수증검사는`evidence/document-check-with-handoff.json`에별도보존한다. 그입력HEAD는결과SHA이고HANDOFF의실제hash를기록한다. 인계commit자체를이전sessioncheck가검사했다고부르지않는다.

## 재개할 첫 자료와 실행 명령

**연구내용을이어갈첫자료는NULDL000040/ESTCR17253의Norton귀속이남은날짜있는이전catalog record와정정영수증이다.** 현재정정문구를다시읽는것만으로C28을채울수없다. 현재첫접점은 [도서관record NULDL000040](https://da.adm.thers.ac.jp/en/item/n003-20230901-00040)의Note·NCID BA73420496·서지YB01560390·ESTCR17253이며, Takano2016논문과같은책판인지먼저대조한다. R13935의1680/1695/ca1700논쟁은다른판이므로별도조사한다.

원래결과를검사만할때는저장소루트에서다음명령을쓴다. 새로운출력은자기소유경로에쓰고기존영수증을덮어쓰지않는다.

```bash
git fetch --no-tags origin refs/heads/work/research-af-res-036:refs/remotes/origin/work/research-af-res-036
git show ef839d30d300e20f092dd7f0d57542f0773b77f8:docs/workstreams/research/AF-RES-036/RESULT.md
python -B -m workbench.session check docs/workstreams/research/AF-RES-036/manifest.json --fetch
python -B docs/workstreams/research/AF-RES-036/review/resume-quant/verify_ledgers.py --receipt audit-next-session.json
python -B docs/workstreams/research/AF-RES-036/scripts/verify_documents.py --handoff --receipt evidence/document-check-next-session.json
git log -1 --format=%H -- docs/workstreams/research/AF-RES-036/HANDOFF.md
git status --porcelain
```

다음원문재조회는미실시후속실행의예다. 이미한card재현검사와구별하고가변원문hash가바뀌면실패/변화를남긴다.

```bash
python -B docs/workstreams/research/AF-RES-036/collectors/gnu/reconstruct_nh.py --download-missing
python -B docs/workstreams/research/AF-RES-036/collectors/bioc/reconstruct_base.py R01
```

**기존 `scripts/assemble_ledgers.py`를최신원장위에서그대로실행하지않는다.** 그집계기는후속기준/재개원장을읽지않아보강분을없앤다. `review/resume-quant/reconcile_ledgers.py`와`integrate_resume_audits.py`는명시된before스냅샷과이번입력용이므로새자료가추가되면범위를읽고새파생산출물로실행한다. 검사기를약화하거나해시가달라진카드를조용히다시봉인하지않는다.

C1/C2실제2회차·사람판독·프로그램실행은수행하지않았다. 실제비용을재려면G05/R01의36개보관예시중해당구성만새문맥에제공하고최대2GET/각30초예산을걸어현재목적판정과동일N/H재구성을별도로기록한다. 기존모의수치로실제시간성공을대체하지않는다.

## 색인에 넣을 한 줄

**AF-RES-036 · 새 배포 참조12·네 보기48·고유 원문50: 같은현재증거N에서H추가행동변화0/12,풍부한원인용B/N조건과엄격분모0을공개;동일NH재구성에만조건부보관비용차이,REVIEW_READY_WITH_GAPS(28/33). 결과ef839d30…와이HANDOFF연결.**

색인·dot-control의반영은통합담당에게넘긴다. 이브랜치의인계commit을실제로확인하여result_commit을기록해야하며,f403243을최종결과로남기지않는다.

## 가장 중요한 약점 세 건과 다음 조사

| 가장 중요한 불일치 또는 약점 | 근거 자료 주소 | 영향을 받는 결론 | 다음 조사 제안과 첫 자료 |
| --- | --- | --- | --- |
| 풍부한B/N·겹친H·같은모델계열·특정판1개이며사전노출/추가목적한정/후보소진공백이있다. | [원장](sensitivity.csv), [G03 2018판](https://pubs.opengroup.org/onlinepubs/9699919799/mindex.html), [원배포](https://archive.debian.org/debian/pool/non-free/g/gawk-doc/gawk-doc_5.1.0-1_all.deb) | 0/12를이력일반무용·순수링크충분·실사용정확도·H인과효과로확대불가. | 첫비교는고정G05/G03의B에서판/멤버메타데이터를보존/제거한입력의별도미노출판독. 특정판재현의도가명시된새소비자묶음은별도사전봉인. |
| 반복조회는모의이며C1경로재발견·노동·C0·전체판정이력운영비를계측하지않았다. | [replay-costs.csv](replay-costs.csv), [retention-options.jsonl](retention-options.jsonl), [R01 대체절](https://bioconductor.org/packages/3.11/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html#preparing-quantification-input-to-deseq2) | 모의12GET/13,011,463B차이를실제시간·돈절감이나저장설계최적해로쓸수없음. | 첫실행은R01/G05의구성별저장파일만주고2GET/각30초로실제재취득. 현재판정·동일근거본문복원·원조회시각재현을분리측정. |
| 명시서지정정은있으나동일레코드의날짜있는전후와소비자반영이없고별개판귀속도충돌한다. | [NULDL000040](https://da.adm.thers.ac.jp/en/item/n003-20230901-00040), [Takano2016](https://nagoya.repo.nii.ac.jp/record/21891/files/01_TAKANOAkira.pdf), [R13935](https://www.grubstreetproject.net/publications/R13935/) | 현재정정문구를실제수정일·전파율·외부독립정답으로확대불가. | 첫자료는NULDL000040/ESTCR17253의Norton표기이전고정record와정정영수증. R13935는2021연구pp.827–859를확보하여다른사슬로대조. |
