# AF-RES-098 인계 — 릴리스에 남은 파일의 배포·사용·생성 귀속

## 상태와 정확한 판

**상태: REVIEW_READY — 요청한 연구·원격 커밋·실제 검사를 완료했다.** 주 예측 6개와 두 판 12자리를 유지하고, 근거가 없는 생성 귀속과 미확보 반례는 유보로 남겼다. 연구의 미확인을 검사 실패나 파일 부재로 바꾸지 않았다.

| 필드 | 값 |
|---|---|
| 작업 / 브랜치 | AF-RES-098 / `work/research-af-res-098` |
| 결과·검사 영수증 통합판 `result_commit` | `846aa7b644bda67ef2551c3f4fb1ec6f5de9484d` |
| 실제 계약·공통·본문/PNG 검사를 실행한 `tested_result_commit` | `01fe105974365042f7efd0991cba0ddfbf07a0ba` |
| 이 인계의 부모 | `846aa7b644bda67ef2551c3f4fb1ec6f5de9484d`; 이 파일만 추가하는 마지막 단독 커밋 |
| 시작 시 최신 통합 SHA | `01177554d0fbd33a914ea9c982c348d442d1358d` |
| 배정 계획의 통합 SHA | `fcde6becc49120c5be91adf43fb5b4aa42e71d48` |
| 검사 때 fetch한 통합 SHA | `2bb12eaf77b7ad42667a7222ba1da8c802ccb2e8`; 계약 지문 유지, 작업 범위 검사 통과 |
| 운영 의존 원격 / 094 인계 입력 | `work/research-af-res-094=b09dd21acb2bf9160a5aca5b1075ad6179743e63` |
| 094 연구 결과 입력 | `082ba3b787edd92d804bf617397743e89d75c5f0`의 RESULT R2/EPUB·cards·두 evidence JSON |
| 쓰기 범위 | `docs/workstreams/research/AF-RES-098/` |

결과 표는 [RESULT.md](RESULT.md), 질문별 반증·한계는 [SELF_CHECK.md](SELF_CHECK.md), 입력과 명령은 [reproduce.md](reproduce.md)에 있다. 읽은 의존 입력 다섯 파일의 blob이 현재 운영 의존판과 같았다는 비교는 [input-contract.json](evidence/input-contract.json)에 보존했다. 통합 브랜치가 진행했어도 연구 입력을 바꾸거나 다른 신규 배정의 결과를 기다리지 않았다.

## 핵심 수치와 판단

- **6/6 사전 예측 참**, 오귀속0·놓친 연결0·유보0·결원0. 실제 음성 분모0이므로 특이도·삭제/이름 변경 탐지 성능은 추정하지 않는다.
- **12자리 모두 P=YES·U=YES, G=UNKNOWN.** 정확 판에 포함되고 정확 절에서 쓰인다는 사실과 특정 빌드가 새 바이트를 생성했다는 사실을 구분했다. G의 UNKNOWN은 NO가 아니다.
- 주6쌍 중 PNG 바이트 변경4, 동일2. MP 두 쌍은 Software 메타데이터만 다르고 픽셀은 같다. GG 두 쌍은 픽셀도 다르며 GG2 source는 동일하다. PY 두 쌍은 더 오래된 소스와도 같은 정적 이미지다.
- **164 원장 행 / 고유 1차 자료102 / 실제 예제 본문18 / payload17 / 발행·빌드·목록48 / EPUB규격·실물3 / 데이터규칙·레코드6**. 선택 publication/dataset 계보5, 규칙까지 포함한 source family12, 상속 교정1은 신규 수에서 제외한다. 주 선정 본문만의 고유 저작8과 전체 실제 읽은 본문18을 섞지 않는다.
- 모집틀은 **1,335경로**(MP612/PY515/GG208), 이것을 원문1,335개로 세지 않았다. 사전 목록7접근의 응답량14,522,038B, 주 본문·그림 판별주소28, 영수증에서 복원한 수집 접근180회 하한은 서로 다른 단위다. 마감 재검사24URL과 GitHub 재열람은 별도 회차다.

정확한12행은 [lineage.csv](lineage.csv), 선행 예측은 [predictions.csv](predictions.csv), 모든 원주소·지문·한계·중복 근거는 [sources.jsonl](sources.jsonl), 산술은 [counts.json](evidence/counts.json)이다.

### 목적별 반환에 남긴 차이

조사한 다음판의 PY1 흐름도를 쓸 독자에게는 3.12.1 본문과 PNG를 줄 수 있다. 생성판이 미확인이라고 이용 가능한 파일까지 부정하지 않는다. 과거 GG3.5.0을 인용할 독자에게는 고정 발행 HTML 소스와 당시 PNG를 주며, raw HTML을 렌더된 과거 사이트로 표시하지 않는다. MP2를 실행할 개발자에게는 본문과 `.py`를 주고 정적 PNG의 클릭 동작을 약속하지 않는다.

상속 asciicast 교정에서는 새2.3.1의 Using SVG 설명은 읽을 수 있지만 그 절에 옛SVG 참조가 없다. 같은SVG두개가 트리에 남아 있어도 현재절 사용을 추천하지 않는다. 옛 절L140–161의 img는150·160행2개, 새절L169–209의 img/script/inlineSVG/dataURI는각0이다. [교정 감사](evidence/calibration/audit.json). 094의24경로·Moby-Dick·IIIF0009는 새사례로 세지 않았다.

EPUB는 Cole 패키지의 container→OPF→XHTML→내부JPEG를 따라갔고 두 패키지9/9이미지가 같아도 현재 참조됨을 확인했다. Corpus의 version DOI와 concept DOI는 다르며, concept의 실제 도착은 관측 때 v4.1계열이었다. 두 ZIP의 크기/MD5는 발행자 선언이며 직접 수신검증은 아직 아니다. [타 분야 감사](evidence/cross-domain/audit.json).

## 중간 커밋과 원격 저장

| 묶음 | 원격 SHA | 주요 변경·파일 기록 |
|---|---|---|
| ① 판·모집·이전 목적 고정 | `c0d31ca194e47fe69bc51dc0ef85d6e346b50774` | SCOPE/freeze/frame/manifest·이전판 영수증; 변경59파일 목록은 checkpoints.stage1 |
| ② 새 목록 예측 봉인 | `0df9ea9edbcee995d631eef54b65fd43f73c245f` | predictions·새목록·노출/봉인 기록;20파일 목록은 checkpoints.stage2 |
| ③ 본문·payload·발행·반례 | `1c22d31375c334409f859b38fee586b6c2a33b8d` | lineage·audit·sources·타분야·교정;89파일 목록은 checkpoints.stage3 |
| ④ 실제 성패·반환·검산 | `01fe105974365042f7efd0991cba0ddfbf07a0ba` | RESULT/SELF_CHECK/reproduce·독립AI검토·검증도구·중복정정;18파일 목록은 checkpoints.stage4 |
| 검사 영수증·실제 상태 설명 | `846aa7b644bda67ef2551c3f4fb1ec6f5de9484d` | 아래11파일; 실제 검사 대상은 바로 위R이며 required3tables/끝3약점은 그대로 |
| 최종 인계 | 이 파일의 단독 마지막 커밋 | `HANDOFF.md` 1파일; 부모는V |

각 묶음 직후 원격 branch ref를 갱신하고 fetch로 확인했다. 최초 `git push -u origin work/research-af-res-098`는 터미널 인증정보가 없어 종료128이었다. 연결된 GitHub의 tree/commit/ref 갱신을 expected head로 수행해 해결했고 같은 tree를 fetch해 로컬과 맞췄다. 실패 명령·로컬 미푸시 SHA와 원격 SHA의 구별은 [checkpoints.json](evidence/checkpoints.json)에 있다. force 갱신·중앙진행표 수정·원천094 수정은 하지 않았다.

검사 영수증 묶음V의 변경 파일은 다음과 같다.

- `RESULT.md`
- `SELF_CHECK.md`
- `evidence/checkpoints.json`
- `evidence/cloud-check-result.json`
- `evidence/cloud-check.stderr.txt`
- `evidence/cloud-check.stdout.txt`
- `evidence/github-readback-result.json`
- `evidence/network-recheck-result.json`
- `evidence/structural-check-result.json`
- `evidence/task-check-result.json`
- `evidence/validation.json`

## 실제 검사와 한계

다음 다섯 검사는 **`01fe105974365042f7efd0991cba0ddfbf07a0ba`**에서 실행했고 각각 종료0이었다. 시작/끝UTC와 원 명령·stdout/JSON은 [validation.json](evidence/validation.json) 및 연결된 원 영수증에 있다.

| 실행한 명령·검사 | 결과 | 실제 범위 |
|---|---|---|
| `python -B .../tools/verify.py` | exit0 | 봉인20파일,1335경로,6예측,12행,source102·범주최소,필수표6/12/7,SELF Q7행 |
| `python -B -m workbench.session check docs/workstreams/research/AF-RES-098/manifest.json --fetch` | exit0 / passed / remote_checked | 통합·의존 fetch,계약·범위검사;outside_paths0/errors0 |
| `python -B scripts/cloud_check.py --environment codex-cloud --fetch-contract --require-clean` | exit0 / passed | doctor/acceptance/research-case/original-smoke; 시작·끝 clean. 제품·브라우저 통합이나 연구주장의 참 인증 아님 |
| `python -B .../tools/verify.py --network --output /tmp/af098-result-network.json` | exit0 /24중24 | 본문12·주PNG12의 실제MIME·길이·SHA·PNGsignature 재확인;브라우저/예제 실행 없음 |
| `python -B .../tools/verify_publication.py --commit 01fe105974365042f7efd0991cba0ddfbf07a0ba --output /tmp/af098-result-github-readback.json` | exit0 /19중19 | GitHub 고정 결과판의 필수표·원증거·재현문서를 다시 열어Git blob과 일치 |

**공통 검사에서 개별 세션 검사는 건너뛰어졌다.** sessions 과정의 process exit0과 달리 내용은 `status:not-executed`, `reason:no_active_sessions`, `freshness:not_checked`, count0이다. 이 owned_path의 manifest는 공통 검색 대상에 자동 포함되지 않았다. 위 표의 명시적 작업별check가 별도로 remote_checked/passed였다는 것으로 이 한계를 구별한다.

V에는 검사 영수증과 보고서의 실제검사 상태 문단만 추가했다. V·이 인계 커밋을 R에서 검사한 것처럼 표시하지 않는다. RESULT 첫세표와 마지막약점표가 R 이후 바뀌지 않았음은 validation.postcheck_report_update의 지문으로 남겼다. 문서화 도중 발생한 검사기 CRLF비교/nullable고정URL 처리 실패와 수정, report작성 마지막출력의 KeyError도 [prepublication-checks.json](evidence/prepublication-checks.json)에 구분했다.

### 최종 보고판V를 GitHub에서 다시 연 영수증

R에서 첫19파일 재열람을 마친 뒤, 검사 기록이 추가된 **V=`846aa7b644bda67ef2551c3f4fb1ec6f5de9484d`**에서도 다음을 직접 확인했다. `verify_publication.py --commit V --output /tmp/af098-final-result-github-readback.json`는 **exit0/19중19**, 추가한 validation·cloud·task·network·첫readback JSON5개는 같은 `read_one` 함수로 **exit0/5중5** Git blob일치를 확인했다. 이 인계 작성 전 완료했고 원격 오류0이었다. 아래는 그 실제 최종 읽기의 원주소·UTC·도착 바이트 지문을 이 마지막 파일 안에 보존한 것이다. 단순히V의파일목록만 보고 완료로 처리하지 않았다.

| V에서 직접 다시 연 파일·원주소 | UTC | 바이트 | SHA-256 | HTTP/일치 |
|---|---|---:|---|---|
| [RESULT.md](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/RESULT.md) | 2026-11-23T20:21:17.058683+00:00 | 46121 | `174881809fd24f54ec15681a50db5aebb28adbc945a9cf68d9c0d5d10ab47fec` | 200 / YES |
| [SELF_CHECK.md](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/SELF_CHECK.md) | 2026-11-23T20:21:17.056768+00:00 | 13118 | `6d81281fd9391fd12ed99c9b3a706827e33510fef26641ba41104b58c5254820` | 200 / YES |
| [reproduce.md](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/reproduce.md) | 2026-11-23T20:21:17.057726+00:00 | 12145 | `aa6354f45c87a46e7a6726cd079650e75b7419cefdcec42b389126e9e8d74123` | 200 / YES |
| [SCOPE.md](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/SCOPE.md) | 2026-11-23T20:21:17.062190+00:00 | 8478 | `fd959cf3140c59149705341a7c213b75444041406c502862d2b7bba24a74f536` | 200 / YES |
| [freeze.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/freeze.json) | 2026-11-23T20:21:17.061365+00:00 | 5086 | `7f5954e605661ed9bde3dc3fb4e15a578b0aba36485adf606f55f55c80ffbfd9` | 200 / YES |
| [frame.csv](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/frame.csv) | 2026-11-23T20:21:17.069503+00:00 | 731665 | `6a9eed9c967ceb9c1f0f6cbac9b944e35b238b3b89073931b4193b35841316ff` | 200 / YES |
| [predictions.csv](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/predictions.csv) | 2026-11-23T20:21:21.299006+00:00 | 4310 | `b40e72f14fd4239d698979528331aca54d4dc089d0b88cf6b837347899902ced` | 200 / YES |
| [lineage.csv](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/lineage.csv) | 2026-11-23T20:21:21.332419+00:00 | 14408 | `064023d7326d877f1f4cc5391858af3e26c8cc6f136c744078b843138d7f794d` | 200 / YES |
| [sources.jsonl](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/sources.jsonl) | 2026-11-23T20:21:21.332298+00:00 | 207444 | `f732eba92757d4d9edcfd758d4e9a3d03c704bacc0c94bbbd047336e05028e2d` | 200 / YES |
| [evidence/counts.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/counts.json) | 2026-11-23T20:21:21.340328+00:00 | 2618 | `8cea2d6a5bf3ade8e760be6f9511da22b929bec522091413dc07e7919a9953a2` | 200 / YES |
| [evidence/input-contract.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/input-contract.json) | 2026-11-23T20:21:21.343223+00:00 | 1645 | `9154d035c592ea7b7a0385bc68d4a54b6f2632456b306904c7488c31bfed5c09` | 200 / YES |
| [evidence/prediction-seal.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/prediction-seal.json) | 2026-11-23T20:21:21.383553+00:00 | 690 | `d0e4b7f96a04257b22b83adea74a0396ce1d8e448e057b2a7bb01ece7d8cfad1` | 200 / YES |
| [evidence/matplotlib/audit.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/matplotlib/audit.json) | 2026-11-23T20:21:27.562745+00:00 | 55151 | `c50591e938e4c850f8fd4a628a8aed2fecf9d00a03627933ab1e8bc5144a5ba2` | 200 / YES |
| [evidence/cpython/audit.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/cpython/audit.json) | 2026-11-23T20:21:27.642583+00:00 | 21929 | `97a235ea98c33868b43e4bc33a01830ffc5fb98e2a902353335f952678761c1e` | 200 / YES |
| [evidence/ggplot2/audit.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/ggplot2/audit.json) | 2026-11-23T20:21:28.009391+00:00 | 30033 | `229789a52d5061968a9ec5779109fbfd5d80d99e11379dd13102f913b07fc23e` | 200 / YES |
| [evidence/calibration/audit.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/calibration/audit.json) | 2026-11-23T20:21:28.033423+00:00 | 7554 | `642c7c22319bd1d02896b4992396568fcef2248bb98a3fbb1f2bf7d846098b11` | 200 / YES |
| [evidence/cross-domain/audit.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/cross-domain/audit.json) | 2026-11-23T20:21:28.042036+00:00 | 54035 | `c2f7a1efd71e2ed13ecad66e56cd8a95ce2b3eb22e1b67e575f4742e6a96f623` | 200 / YES |
| [evidence/cross-review/final-review.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/cross-review/final-review.json) | 2026-11-23T20:21:28.122172+00:00 | 18012 | `a4dad6fe53298393091d3c1eea53d80ebfbb37c5f79188692f41107aca2a4ec4` | 200 / YES |
| [evidence/cross-review/source-count-review.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/cross-review/source-count-review.json) | 2026-11-23T20:21:31.633595+00:00 | 10719 | `14bbdcb5c6662f8403e4d64de66400c874da4d786282e098c34840f24d37de1f` | 200 / YES |
| [evidence/validation.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/validation.json) | 2026-11-23T20:21:50.449663+00:00 | 8652 | `1951ba1a304eabbebd0a8c6e3d1a8de181a225150c98e0581f23e13f6d0e2730` | 200 / YES |
| [evidence/cloud-check-result.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/cloud-check-result.json) | 2026-11-23T20:21:50.446815+00:00 | 4167 | `e60489683cc92f1a0d3368e7782630b44812d83701b73f7be0f1211d369484ec` | 200 / YES |
| [evidence/task-check-result.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/task-check-result.json) | 2026-11-23T20:21:50.446094+00:00 | 14894 | `56335523558c4e4d1460cb8ace5b2f99751afcfba567bdb1048402e9ab82debb` | 200 / YES |
| [evidence/network-recheck-result.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/network-recheck-result.json) | 2026-11-23T20:21:50.450407+00:00 | 34700 | `28426542679c62fd254994c83adf9db49ccb3fb370d92420119a48656e734303` | 200 / YES |
| [evidence/github-readback-result.json](https://raw.githubusercontent.com/laadkke-arch/agentflow-open/846aa7b644bda67ef2551c3f4fb1ec6f5de9484d/docs/workstreams/research/AF-RES-098/evidence/github-readback-result.json) | 2026-11-23T20:21:50.446010+00:00 | 17607 | `2541f03c0076f2ebe3f4d631c5ed872be7830977ae6fd604461c6a55d8f67deb` | 200 / YES |

## 자기 검토와 별도 검토

작성자 자체 검산과 별도 AI검토를 구분했다. [모집·봉인 검토](evidence/cross-review/review.md), [최종내용 검토](evidence/cross-review/final-review.md), [source수·비용 검토](evidence/cross-review/source-count-review.md)에 실제 읽은 입력·지문·한계를 남겼다. 사람 검토는 수행하지 않았다. 타분야 작성자의Q6점검과 GG작성자의GG점검은 자기검토이며 독립 검토로 세지 않았다.

실제 수정한 불일치는 PY2 크기요약500×322→500×320, calibration 절경계·HTMLParser행오프셋, 잘못된calibration index링크, GG빈claim3개, MP주본문 중복2개, 협업전체의최초새PNG시각, 후속Corpus명령의MD5실패종료 전파다. 최종자료수는102/본문18이며 초기104/본문20을 최종값으로 쓰지 않는다. 봉인파일·예측·12자리·세축결론은 그대로다.

## 미실시와 재개 첫 행동

**재개 첫 행동:** MP발행 `dbd81bd88621dbfee4c0da45e62a5aeb5722378c` 또는 GG발행 `3ab6b4a05b3bde422ccc9adbfd1131bbdef64a3c`에 대응하는 보존된 실제 job/manifest를 확보하고, source·환경·output digest가 [lineage.csv](lineage.csv)의 해당PNG SHA를 직접 연결하는지 읽는다. 공개 Actions조회0건이나403을 생성job의과거부재로 취급하지 않는다. 그 입력이 없으면 G=UNKNOWN을 유지한다. 파이프라인 규칙만 다시 읽거나 같은SHA를 재확인하는 것으로 G를 올리지 않는다.

이번범위에서 예제프로그램 빌드·클릭실행, browser DPR/JS실행, EPUBreader 실행·패키지 재빌드, Corpus ZIP전송/MD5·의미집합비교, 역사적생성job재현은 미실시다. 사용자는 예제빌드를 요구하지 않았고, 정적배포·참조와발행귀속을검사했다. Corpus의전체파일검증은 합계3,235,117,257B의추가전송이필요하므로 선언메타데이터 관측으로범위를명시했다. 미실시를통과로세지않았다.

Corpus파일실물을후속검사할정확한명령과입력은아래와같다. 현재실행한명령이아니다. concept/latest주소로대체하지않는다. 내부인용ID집합비교는 ZIP내실제스키마를먼저읽어야하므로 다음단계로분리한다.

```sh
(
  set -eu
AF098_CORPUS_DIR="$(mktemp -d /tmp/af-res-098-corpus.XXXXXX)"
curl --fail --location --show-error \
  'https://zenodo.org/api/records/11196859/files/2024-01-30-data-citation-corpus-v1.0.zip/content' \
  --output "$AF098_CORPUS_DIR/2024-01-30-data-citation-corpus-v1.0.zip"
curl --fail --location --show-error \
  'https://zenodo.org/api/records/11216814/files/2024-05-10-data-citation-corpus-v1.1.zip/content' \
  --output "$AF098_CORPUS_DIR/2024-05-10-data-citation-corpus-v1.1.zip"
  cd "$AF098_CORPUS_DIR"
  md5sum --check <<'CHECKSUMS'
7e56ae579f62d432b2fac135d924ac70  2024-01-30-data-citation-corpus-v1.0.zip
e2e191e9573a9ee729413df872edd96b  2024-05-10-data-citation-corpus-v1.1.zip
CHECKSUMS
  wc -c 2024-01-30-data-citation-corpus-v1.0.zip 2024-05-10-data-citation-corpus-v1.1.zip
)
```

이름 변경·동일 바이트는 GG 두발행판의dev제외1,285옛경로와PY두자원의각3이력에서 찾지못했다. 다음보조모집은 ggplot2 v3.4.0→v3.5.0의공식release/발행트리에서삭제·이동후보를먼저봉인한다. 본문을먼저본뒤주6사례를교체하지않으며 새후속분모를별도로둔다.

**색인 제안 한 줄:** 요청 목적·고정판·정확 절·참조 관계·payload 지문과 P/U/G 근거 수준을 한 판단 단위로 저장하고, 본문/파일/발행기록 링크는 확인된 목적에 필요한 것만 펼친다.

| 가장 중요한 불일치·약점 | 다음에 열 자료 또는 실행할 입력 | 어떤 관측이면 결론을 바꿀지 |
|---|---|---|
| 12/12 자리에서 현재 사용은 확인했으나 이번 빌드의 바이트 생성은 미확인이다. | MP dbd81bd…·GG 3ab6b4…·PY 3.12.1 배포에 대응하는 실제 job/attestation과 source·환경·output digest manifest를 연다. | 특정 실행이 해당 SHA 바이트를 새로 생성한 연결을 제시하면 G를 YES로, 복사만 명시하면 재사용의 근거 수준을 갱신한다. |
| 주 6쌍이 모두 양성이며 이름 변경·동일 바이트 반례를 확보하지 못했다. | 별도 모집으로 ggplot2 v3.4.0→v3.5.0의 공식 발행 트리에서 삭제/이름 변경 후보를 먼저 봉인하고 양쪽 본문·파일을 연다. | 경로 존재인데 절 참조가 없거나, 경로가 없어졌지만 새 이름을 현재 참조하는 사례가 나오면 오귀속·놓친 연결 수와 적용 범위를 갱신한다. |
| Corpus 두 ZIP의 크기·MD5는 발행 목록 선언이며 전체 payload와 인용 집합은 미검증이다. | 11196859/11216814의 정확한 files content URL에서 ZIP을 받아 MD5를 재계산하고 내부 인용 ID 집합을 비교한다. 명령·입력은 reproduce.md에 둔다. | 수신 MD5가 선언과 다르거나 v1.1의 인용 추가·삭제가 발견되면 파일 일치 또는 발행 설명에 대한 판단을 바꾼다. |
