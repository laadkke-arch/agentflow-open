"""Write the last handoff only after immutable result reread and contract check."""
from pathlib import Path
import datetime
import json
import subprocess

P=Path(__file__).resolve().parents[1]
ROOT=P.parents[3]
result_sha='e8c8e3b371967a029d6284fb632242aae20d69da'
reread=json.loads((P/'evidence/result-remote-reread.json').read_text())
session=json.loads((P/'evidence/checks/session-result-sha-execution.json').read_text())
verification=json.loads((P/'evidence/result-sha-check.json').read_text())
assert reread['target_sha']==result_sha
assert session['target_HEAD']==result_sha and session['exit_code']==0
assert verification['target_HEAD']==result_sha and verification['exit_code']==0
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==result_sha
doc=(P/'RESULT.md').read_text()
tables=doc.split('\n',1)[1].split('## 고정 결과와 분모',1)[0].strip()
weakness=doc.split('## 가장 중요한 불일치 또는 약점',1)[1].strip()
created=datetime.datetime.now(datetime.timezone.utc).isoformat()
head=f'''# AF-RES-032 인계

**상태: REVIEW_READY_WITH_GAPS. 결과·자체점검·수용 고정 SHA: `{result_sha}`.**

[고정 RESULT](https://github.com/laadkke-arch/agentflow-open/blob/{result_sha}/docs/workstreams/research/AF-RES-032/RESULT.md) · [고정 SELF_CHECK](https://github.com/laadkke-arch/agentflow-open/blob/{result_sha}/docs/workstreams/research/AF-RES-032/SELF_CHECK.md) · [고정 수용 판정](https://github.com/laadkke-arch/agentflow-open/blob/{result_sha}/docs/workstreams/research/AF-RES-032/evidence/acceptance-evidence.json)

| 필수 수치 | 고정 결과 |
| --- | --- |
| A 출발 표본 | 실제 배포 HTML12문서·12참조·6프로젝트·D6/R6·프로젝트당2 |
| A 실제 배포 관측 | archive123 / 멤버 상태246 = HTML211 + 멤버 부재35 |
| A 같은 목적 href 수정 | **5/12참조, 독립 소스 수정4사건** |
| 현재 추천 판단 | A 유지9·교체2·보류1 / B 유지4·교체1·보류1 |
| B 사건 우선 시도 | **6시도 / 18질의 / 후보 문서 계열17**; HTML5/6, 그중 A중복1, 추가 독립HTML4 |
| B 같은 목적 href 수정 | 중복 포함2/6시도; A중복 제외 신규1/5시도 |
| 엄격 상류 시행→소비자 출판 | **A0/12, B0/6**; 계산 조건부 분모0은 **해당 없음**; 검열0 |
| 보조 source committer→CRAN | A3참조쌍/독립2사건, B1참조쌍/1사건 |
| 고유 직접 원문 최소 산입 | **75** / 원장395행; A12·상류34·후속8·타분야8·기타1·B소비자5·B보조7 |
| 원 독자 | 같은 offline 매체 실패 사슬0; 별도 live-web 당사자 보고1 |
| 수용 판정 | **30조건 중24충족·6미충족**; 양성0 자체는 미충족 조건이 아님 |
| 확인된 기계 검사 | 결과SHA 대상 원장/형식38/38 exit0; 계약check --fetch exit0; 공통회귀는 직전6ac3d4d에서5/5 exit0 |

## 1. 배포 링크와 목적

'''
body=f'''

## 인계할 결론

실제 도움말의 같은 목적 href가 처음 바뀐 판은 확인한 계열 안에서 **Python3.8.15, PostgreSQL12.19, knitr1.30의 두 문서, dplyr1.0.2**다. B가 추가한 독립 수정은 **httr1.4.3**이다. 문서 이름이나 source diff에서 판을 추정하지 않고 실제 archive member를 읽었다. 첫 관측을 세계 전체의 최초 출판으로 확장하지 않는다.

그러나 편집자가 href를 바꾼 일과 지금 원 추천을 교체해야 하는지는 같은 판단이 아니다. RFC4180의 옛 주소는 여전히 필요한 CSV 내용을 제공한다. Python의 옛 오류 query는200이어도 동결돼 현재 열린 문서 오류 목적을 충족하지 못한다. BTS는200이어도 다른 통계 대상으로 도착한다. httr는새호스트로고친href도현재필요한anchor가없다. rmarkdown의구CSS는호환성설명목적이므로단지deprecated라는이유로새속성설명만남기지않는다. 이 근거와 반대 설명은 고정 RESULT Q3–Q8 및 각 행에 연결돼 있다.

정확한 source committer→CRAN 차이는 knitr 두 행14:36:40(같은 사건), dplyr5일21:42:26, httr03:54:04다. 상류 실제 시행 시계와 이어지지 않으므로 추천 캐시의 만료기간이나 전파 평균으로 쓰지 않는다. Python의156일00:35:47은 분 단위 공식 상태 보고→committer의 명목 차이이며 실제 시행의 상·하한이 아니다. 독자 보고도 live/3/문서와offline3.8을합치지않았다.

## 고정 입력·환경·조사 창

| 항목 | 값 |
| --- | --- |
| 저장소·브랜치 | laadkke-arch/agentflow-open / work/research-af-res-032 |
| 소유 경로 | docs/workstreams/research/AF-RES-032/ |
| 실제 시작 foundation | 172c6bc37bdf91b91c86b9b3be29cb5b44fa4971 |
| 의존027 result_commit | 42dadeeb632301108e1fc83ba393db971ec28b15; HANDOFF/references/intervals/RESULT Q4–Q8를 읽음 |
| 계약 | v2 / SHA256 19f08ce67f7b9d1914ccf214ac68112f3cefc68c95855c4aac0bbbd3393cd8bc |
| 마지막 fetch에서 본 통합 SHA | 630fa68a677d66fc59baa7bd92ea40fdc1ad3a06; 계약 동일, session check 통과. 시작 manifest를 새 SHA로 덮어쓰지 않음 |
| 담당·환경 | 배정web-pro; 실제 ChatGPT Work 공유Linux 셸·GitHub connector·웹 검색 |
| 표시 모델 | 세션이 선언한 GPT-6 Astra Pro. 계정 UI에서 별도 확인하지 않음. common gate의 codex-cloud는 호출자 label이며 Cloud 계정 연결 증거 아님 |
| 시작/원문 확인창 | 2026-11-22 07:05Z 착수; source395행의 확인UTC 07:11:58.976247–07:40:36.378887Z |
| 재독/후속 분석 | 별도archive재독07:50:37.814656Z, root freshGET07:58:20.761822Z. 그 뒤 분석·검산·원격 고정. [조사창](evidence/research-window.json) |
| 결과 원격 재독 | {reread['checked_at_utc']}; RESULT/SELF_CHECK/acceptance/검사영수증 본문을 고정SHA에서 재독, staged body 동일 |
| HANDOFF 생성 UTC | {created}; 위 원격 재독 및 결과SHA session check 이후에만 작성 |

## 검사와 원격 영수증

| 검사·구분 | 실제 대상·입력 | 결과·증거 | 확인하지 않은 것 |
| --- | --- | --- | --- |
| 원 A 봉인 | 168d90b… references12행; prefix50,326bytes, SHA256b3c2f68… | [A remote receipt](evidence/a-seal-remote.json); 최종38항목에서도 원 blob과 일치 | 목적지 상태를 봉인 전에 읽었다는 주장 없음 |
| 소비자 원문 재독 | Python19+httr8archive,HTML46,DESCRIPTION8; 당시13파일hash | [별도 내부 감사](collectors/offline/audit-root.json), 바이트/산술 결함0; 역할 설명3보강 | B03deb는이감사에서재독하지않음; 외부사람검토아님 |
| root 원문 재검 | Python3.8.14/15 실제 archive, R04원조건, D01유지본문 | [freshGET4/4](evidence/primary-reread.json), exit0 | 독자실패·실행·전원문재검아님 |
| 통합 원장 검산 | ffbce62…HEAD+당시입력hash;395source/75최소수/분모/산술 | [27/27](collectors/cran/integration-audit.json), exit0. 이후정정은별도원장 | 후기B04정규화·LF정규화를과거검사에소급하지않음 |
| RESULT 별도 내부 판독 | RESULT SHA256c2c32c79d95cddc6efa1c81f3d7bf25b13e655975e027822d2d8ab0e0eb3e59b | [16/16 감사](collectors/cross/result-review.json), 발견7건모두수정. Git/새외부조회0 | Q7/B일부수집자가참여했으므로완전독립검토아님 |
| 공통 workbench gate | 고정6ac3d4d9c11f5a750401535a05caed29ed5daf01의공식원격freshclone | [실행](evidence/checks/common-retry-execution.json)·[5/5 exit0](evidence/checks/common-retry-receipt.json) | 후기RESULT내용·제품설치·브라우저통합검사아님 |
| 공통 gate 첫 실패 | 같은6ac3d4d의localclone;git bundle에서누락object0ac611… | [exit1](evidence/checks/common-check-execution.json)·원stdout보존. freshclone으로원인만해결 | 실패를성공으로덮거나검사기를수정하지않음 |
| 형식/원장 검산 | {result_sha} HEAD;정규화된원장및RESULT/SELF_CHECK/수용파일45개입력hash | [38/38 exit0](evidence/result-sha-check.json); sourcejoin·산술·첫표18행×3·마지막3행·허용경로 | 새외부의미판독은아님 |
| 작업 계약·의존·범위 | {result_sha}; manifest hash fa1d31e47be64a2c71d6448c90c6e707c334ee2dd817210a27a460fdf37acc0b; --fetch | [결과SHA session 실행](evidence/checks/session-result-sha-execution.json)·[stdout](evidence/checks/session-result-sha.stdout.json), exit0 | 원격파일read를셸검사로칭하지않음 |
| 결과 원격 재독 | {result_sha}; RESULT/SELF_CHECK/acceptance/counts/check고정blob | [remote receipt](evidence/result-remote-reread.json); 표18/18/18,약점3,수용24/6 | metadata만읽은것이아니라본문동일성대조; actualreaderclick과무관 |
| Git whitespace | 결과직전 staged변경 | [원기록](evidence/checks/whitespace-review.json): full diff --check exit2, 문서/코드subset exit0 | rawstdout3파일의끝빈줄을원문그대로보존한경고. full명령을통과라고보고하지않음 |
| HANDOFF 포함 마지막 검사 | 이파일작성후, finalreceipt가명시하는HEAD/입력hash | [최종영수증](evidence/deliverable-check-final.json)에서실제exit/항목수확인 | 이행은후기검사의숫자를미리만들지않음;최종커밋에영수증도함께보존 |

파생 CSV6개는 저장소의 `eol=lf`와 같도록 CRLF→LF만 정리했다. [이전/이후 hash](evidence/csv-line-ending-normalization.json)와 generator의 lineterminator를 고정했고 수치·필드·가림 입력·A봉인은 그대로다. 원수집자료와 이전감사의입력hash를고쳐과거검사를재해석하지않았다.

## 남은 미확인과 첫 재개 행동

**가장 중요한 첫 자료는 Python3.8.15의 특정 HTML tarball을 명명한 공식 최초 출판 영수증이다.** [실제 archive](https://docs.python.org/ftp/python/doc/3.8.15/python-3.8.15-docs-html.tar.bz2)의 SHA256은 `ab8a202c748ffbe413a348d8fde24515951f46cdb35a17c95e399b614a56cfa5`, `python-3.8.15-docs-html/bugs.html`의 SHA256은 `8826e64961665ccf661d3fc9db216e8fee553f2f04e52ced95b03d1c1ba762a0`이다. 이 byte와공식publish영수증을연결한후실제read-only시행기록을찾는다. archive Last-Modified나소프트웨어릴리스일만다시확인해서엄격적격으로올리지않는다.

| 미충족 조건 | 마지막 확인 위치 | 다음 최소 자료·행동 |
| --- | --- | --- |
| C08 완전한 제외유형 계수 | frame.csv의선택12/외부URL없는27/추가링크11/미도달7 | 봉인한원archive의DOM후보전수를같은제외규칙으로다시계수. A표본은바꾸지않음 |
| C09 제외후보 조회 편차 | B01-C4/CB-GET30·33·34, JupyterLab3요청모두404 | 편차는지울수없음. 새탐색은제외목록을입력단계에서확인하고기존B6범위/상한을보존 |
| C17 역사본문/시행시계 | Wikipedia2020revision403·기타URI이전일미확인 | 각행unknowns의고정원문/공식시행영수증; 우선위는위Pythonarchive출판영수증과IETF RFC4180 경로config |
| C19 후속판/HTML 공백 | SQLite5/51;B03성긴3deb;B01/B06versionedweb;B04source/현재HTML | 첫미열람 [sqlite-doc-3310100.zip](https://www.sqlite.org/2020/sqlite-doc-3310100.zip)의about.html/aff_short.html. B04는2.2.0/2.2.1의날짜있는HTMLartifact1개 |
| C25 보기실험의교란 | A-D04/B03사전노출;L3현재증거+이력동시추가 | 같은현재증거를고정한current-only/이력추가카드와새비노출판독자. 여기의11/12·5/6을인과효과로재사용하지않음 |
| C29 실행/클릭 미검증 | R04조건부추천·D06도구설명;같은offline독자사슬0 | 고정IDE/Pandoc배포manifest·태그별file magic·동일매체를명명한당사자원문. 자료없음은실패나성공으로바꾸지않음 |

현재 research gaps를 모두 지우기 위해 양성 표본을 새로 고르지 않는다. 대체 발행처·판과 실패를 이미시도한기록은각collector의attempts/editions에있다. SQLite46판은접근불가로입증된판이아니라미열람판이다. B04의실패는HTMLzip404와source tarballHTML0이고대체현재HTML도과거노출매체를증명하지못했다.

## 재검·미실시 실행의 명령과 입력

다음 명령의 첫 묶음은 이 조사에서 실제 실행한 재검 형태다. 마지막 인계 이후에는 해당 실행의 새 target SHA·입력hash·exit를 새 영수증에 적고 기존 봉인 파일을 덮어쓰지 않는다.

```bash
git fetch origin work/research-af-res-032:refs/remotes/origin/work/research-af-res-032
git show e8c8e3b371967a029d6284fb632242aae20d69da:docs/workstreams/research/AF-RES-032/RESULT.md
PYTHONDONTWRITEBYTECODE=1 python -m workbench.session check docs/workstreams/research/AF-RES-032/manifest.json --fetch
PYTHONDONTWRITEBYTECODE=1 python docs/workstreams/research/AF-RES-032/scripts/verify_deliverables.py --final --receipt evidence/resumed-deliverable-check.json
```

공통 gate 원명령은 `PYTHONDONTWRITEBYTECODE=1 python scripts/cloud_check.py --environment codex-cloud --fetch-contract`다. 실제 재실행 때는 소유경로의별도clone과그안의temp디렉터리를사용했다. 준비명령·cwd·targetSHA·temp위치는 [common-check-retry-setup.json](evidence/checks/common-check-retry-setup.json)에완전히남아있다. `.workbench`가소유경로밖에생기는main checkout에서이명령을실행하지않았다.

**A-R04의 실제 바이너리 조건 검사는 미실시다.** 먼저독자가받을IDE판의정확다운로드URL·SHA256·번들Pandoc경로를고정해야한다. 이입력은현재미확인이므로임의의설치된Pandoc으로원추천의성공을대체하지않는다. 소비자입력은rmarkdown2.1 [원tarball](https://cran.r-project.org/src/contrib/Archive/rmarkdown/rmarkdown_2.1.tar.gz), SHA256 `ef450e21206c454aa78eeca9023bbc78d1b2939e0b4bed9fdec9f2bf81ee455d`, member `rmarkdown/inst/doc/pandoc.html`의조건이다. 같은판의환경을준비한뒤다음은필요한검사명령이다. 이명령자체를실행했다고보고하지않는다.

```bash
Rscript -e 'stopifnot(as.character(utils::packageVersion("rmarkdown")) == "2.1"); stopifnot(rmarkdown::pandoc_available("1.12.3")); print(rmarkdown::pandoc_version()); print(rmarkdown::pandoc_exec())'
```

이검사는버전·탐지경로의조건만보며실제구문렌더나설치성공을증명하지않는다. 해당IDE의번들경로와`pandoc_exec()`의경로가일치하는지도비교한다. 공개함수이름과동작은같은2.1 archive의NAMESPACE와R/pandoc.R에서확인했다([명령준비근거](evidence/handoff-command-source-check.json));실제R실행은하지않았다. 원preview를특별히요구했는지는편집자의원설명/고정preview문서가먼저필요하다. 특정독자클릭/실패는셸명령으로재구성할수없고같은배포판·member·href를명명한당사자기록이필요하다.

## 공통 색인 반영 제안

공통 파일은 수정하지 않았다. 통합 담당자는 docs/research/INDEX.md에 **AF-RES-032 · 실제 배포 HTML12, 같은 목적 href수정5/12, strict0/12·0/6, 원문75, WITH_GAPS**를 요약하고 고정RESULT SHA `{result_sha}`와이HANDOFF를연결할수있다. dot-control의작업상태/결과commit반영은통합담당의절차로남기며,이브랜치의마지막HANDOFF commit을확인해서기록해야한다. 이번작업자는dot-control.json을변경하지않았다.

재사용할 가장 작은 결과는 “원 URL+클릭 목적+소비자 판+실제 배포물 hash/member+별도 시계+현재 필요한 절+모르는 점/다음 자료”의 관측 단위다. A/B표본의분모와버전계열을떼고일반전파율로재사용하지않는다. 실제날짜쌍이추가될때는동일목적·동일노출매체임을먼저확인한다.

## 가장 중요한 불일치 또는 약점

'''
(P/'HANDOFF.md').write_text(head+tables+body+weakness+'\n',encoding='utf-8')
progress=P/'PROGRESS.md'
s=progress.read_text()
s += f'\n| ⑤ 결과·자체점검·수용 판정 | {result_sha} | 08:31:01Z 고정본문 재독; evidence/result-remote-reread.json; RESULT blob18fffebdc84492c2b8c3308f3a3e0dea1fb2fc10 / SELF_CHECK blob82beb12390feb0248db3ab231711aa0e700fe541 / acceptance blob7022f42e998474bd315dbdf45762bfd258fee647 | 결과SHA check --fetch 및38/38 exit0 뒤 HANDOFF 작성 |\n\n⑥ 인계는 이 파일과 HANDOFF 및 고정결과 재독/검사 영수증을 별도 마지막 commit에 둔다. 그 commit 자체 SHA는 branch HEAD와 최종 응답에서 확인한다. RESULT·SELF_CHECK·수용의 고정결과내용은 바꾸지 않는다.\n'
progress.write_text(s,encoding='utf-8')
print(json.dumps({'result_sha':result_sha,'handoff_bytes':(P/'HANDOFF.md').stat().st_size,'written_after_remote_read':True,'written_after_session_check':True,'created_at_utc':created},ensure_ascii=False))
